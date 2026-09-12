#!/usr/bin/env python3
"""
elevator_arm.py -- motor sizing under GRAVITY LOAD for elevators and arms, plus the two things
teams forget until the robot falls on itself: HOLDING torque and COUNTERBALANCE sizing
(ratchet / gas spring / constant-force spring).

Why gravity loads need their own tool: a drivetrain that is 20% undersized is slow. An elevator
that is 20% undersized does not hold position, cooks a motor at 0 rpm, and drops a mechanism on
the floor between matches. The failure is asymmetric, so the margin should be too.

USAGE
  python elevator_arm.py elevator
  python elevator_arm.py elevator --mass 18 --travel 48 --stages 2 --ratio 12 --pulley 1.75 \
                                  --motors 2 --motor kraken_x60 --limit 40 --time 1.0
  python elevator_arm.py arm --mass 12 --length 22 --ratio 100 --motors 1 --motor neo --limit 40
  python elevator_arm.py arm --gas-spring          # sweep gas-spring force + geometry
  python elevator_arm.py --json elevator

DEFINITIONS THAT MATTER
  * CONTINUOUS-RIGGED (cascade) elevator: carriage moves n_stages x drum surface speed, so the
    drum sees n_stages x the carriage force. Getting this backwards is the single most common
    elevator sizing error.
  * HOLDING current at 0 rpm produces ZERO back-EMF, so all of it is I^2*R heat with no airflow.
    A motor that is fine at 30 A while moving will fail thermally at 30 A held for 30 seconds.
    The tool reports holding current as a fraction of stall and flags it.
  * BACK-DRIVE: a worm/hypoid or a very high spur ratio will not back-drive; a 9:1 planetary will.
    The tool estimates it and tells you when you need a ratchet, not an opinion.
"""
import argparse, json, math, sys
from motors import get, LBF_PER_N, IN_PER_M, G_MS2, BATTERY

# Thermal guidance [S] -- planning heuristics, not a manufacturer spec. No public duty-cycle
# curve for these motors exists in this corpus. Verify against your own smoke test.
THERMAL = [
    (0.10, "safe indefinitely"),
    (0.20, "OK for a match; motor gets warm"),
    (0.35, "OK for <30 s bursts only. Add a ratchet or a counterbalance"),
    (1.01, "WILL COOK. Ratchet, brake mode is not enough, redesign the ratio"),
]


def thermal_verdict(frac):
    for lim, txt in THERMAL:
        if frac <= lim:
            return txt
    return THERMAL[-1][1]


def elevator(mass_lb=18.0, travel_in=48.0, stages=2, ratio=12.0, pulley_in=1.75,
             n_motors=2, motor_key="kraken_x60", current_limit=40.0, efficiency=0.85,
             target_time_s=1.0, friction_factor=1.25):
    m = get(motor_key)
    kt = m["stall_nm"] / m["stall_a"]
    mass = mass_lb / LBF_PER_N / G_MS2
    r_drum = (pulley_in / 2.0) / IN_PER_M
    travel = travel_in / IN_PER_M

    f_grav = mass * G_MS2 * friction_factor          # N at the carriage, incl. friction allowance
    f_drum = f_grav * stages                          # continuous rigging multiplies force at drum
    tau_hold = f_drum * r_drum / (ratio * efficiency)
    i_hold = tau_hold / kt / n_motors

    # trapezoidal profile: accel 1/3, cruise 1/3, decel 1/3 of target_time
    t3 = target_time_s / 3.0
    v_cruise = travel / (2.0 * t3)                    # area of the trapezoid = travel
    a_req = v_cruise / t3
    f_accel = mass * a_req * stages
    tau_accel = (f_drum + f_accel) * r_drum / (ratio * efficiency)
    i_accel = tau_accel / kt / n_motors

    # kinematic ceiling
    w_free = m["w_free"]
    v_max = w_free / ratio * r_drum * stages
    t_min_kin = travel / v_max if v_max else float("inf")

    tau_avail = kt * current_limit * n_motors
    tau_stall_avail = m["stall_nm"] * n_motors
    return dict(
        kind="elevator", motor=m["name"], motor_src=m["src"], n_motors=n_motors, ratio=ratio,
        pulley_in=pulley_in, stages=stages, mass_lb=mass_lb, travel_in=travel_in,
        current_limit=current_limit, efficiency=efficiency, friction_factor=friction_factor,
        carriage_force_lbf=f_grav * LBF_PER_N,
        drum_force_lbf=f_drum * LBF_PER_N,
        tau_hold_nm=tau_hold, tau_accel_nm=tau_accel, tau_available_nm=tau_avail,
        tau_stall_avail_nm=tau_stall_avail,
        i_hold_a=i_hold, i_accel_a=i_accel,
        hold_frac_of_stall=i_hold / m["stall_a"],
        hold_thermal=thermal_verdict(i_hold / m["stall_a"]),
        accel_ok=bool(tau_accel <= tau_avail),
        torque_margin=(tau_avail / tau_accel) if tau_accel else 0.0,
        v_max_ips=v_max * IN_PER_M, t_min_kinematic_s=t_min_kin,
        target_time_s=target_time_s, a_req_ips2=a_req * IN_PER_M,
        # counterbalance sizing
        cf_spring_lbf=f_grav * LBF_PER_N / max(1, 1),   # force a constant-force spring must supply
        gas_spring_pairs=[(round(f_grav * LBF_PER_N * frac / 2, 1), frac)
                          for frac in (0.5, 0.75, 1.0)],
        i_hold_with_80pct_cb=i_hold * 0.20,
        ratchet_torque_nm_at_drum=f_drum * r_drum,
        ratchet_torque_inlb_at_drum=f_drum * r_drum / 0.112984829,
    )


def arm(mass_lb=12.0, length_in=22.0, ratio=100.0, n_motors=1, motor_key="neo",
        current_limit=40.0, efficiency=0.75, target_time_s=1.2, sweep_deg=(-30.0, 105.0),
        gs_force_lbf=None, gs_arm_r_in=4.0, gs_ground_x_in=-6.0, gs_ground_y_in=-4.0):
    m = get(motor_key)
    kt = m["stall_nm"] / m["stall_a"]
    mass = mass_lb / LBF_PER_N / G_MS2
    L = length_in / IN_PER_M
    I_arm = mass * L * L                              # point mass at the CG radius -- conservative

    tau_avail = kt * current_limit * n_motors * ratio * efficiency
    tau_stall_avail = m["stall_nm"] * n_motors * ratio * efficiency
    tau_grav_max = mass * G_MS2 * L                   # horizontal, cos(0) = 1
    i_hold_max = (tau_grav_max / (ratio * efficiency)) / kt / n_motors

    sweep = []
    worst = 0.0
    for d in range(int(sweep_deg[0]), int(sweep_deg[1]) + 1, 15):
        th = math.radians(d)
        tg = mass * G_MS2 * L * math.cos(th)
        gs = 0.0
        if gs_force_lbf:
            gs = _gas_spring_torque(th, gs_force_lbf / LBF_PER_N, gs_arm_r_in / IN_PER_M,
                                    gs_ground_x_in / IN_PER_M, gs_ground_y_in / IN_PER_M)
        net = tg - gs
        worst = max(worst, abs(net))
        sweep.append((d, tg, gs, net, (abs(net) / (ratio * efficiency)) / kt / n_motors))

    sweep_rad = math.radians(sweep_deg[1] - sweep_deg[0])
    t3 = target_time_s / 3.0
    w_cruise = sweep_rad / (2.0 * t3)
    alpha = w_cruise / t3
    tau_accel = I_arm * alpha + tau_grav_max
    w_free_out = m["w_free"] / ratio
    return dict(
        kind="arm", motor=m["name"], motor_src=m["src"], n_motors=n_motors, ratio=ratio,
        mass_lb=mass_lb, length_in=length_in, current_limit=current_limit, efficiency=efficiency,
        tau_grav_max_nm=tau_grav_max, tau_grav_max_inlb=tau_grav_max / 0.112984829,
        tau_available_nm=tau_avail, tau_stall_avail_nm=tau_stall_avail,
        tau_accel_required_nm=tau_accel,
        static_margin=tau_avail / tau_grav_max if tau_grav_max else 0.0,
        dynamic_margin=tau_avail / tau_accel if tau_accel else 0.0,
        i_hold_a=i_hold_max, hold_frac_of_stall=i_hold_max / m["stall_a"],
        hold_thermal=thermal_verdict(i_hold_max / m["stall_a"]),
        free_sweep_time_s=(sweep_rad / w_free_out) if w_free_out else 0.0,
        target_time_s=target_time_s,
        backdrive=_backdrive(ratio),
        sweep=sweep, worst_net_nm=worst,
        gs_force_lbf=gs_force_lbf, gs_arm_r_in=gs_arm_r_in,
        gs_ground=(gs_ground_x_in, gs_ground_y_in),
    )


def _gas_spring_torque(theta, force_n, r_arm, gx, gy, mount_offset_deg=-90.0):
    """Moment about the arm pivot from a gas spring: arm anchor at radius r_arm, offset from the
    arm centreline by mount_offset_deg; ground anchor at (gx, gy). Gas springs are ~constant force
    over their stroke (that is the whole point of them), so |F| is treated as constant."""
    phi = theta + math.radians(mount_offset_deg)
    ax, ay = r_arm * math.cos(phi), r_arm * math.sin(phi)
    dx, dy = gx - ax, gy - ay
    ln = math.hypot(dx, dy)
    if ln < 1e-6:
        return 0.0
    ux, uy = dx / ln, dy / ln            # unit vector from arm anchor toward ground anchor
    return -(ax * (force_n * uy) - ay * (force_n * ux))   # z-component of r x F


def _backdrive(ratio):
    if ratio >= 200:
        return "very unlikely to back-drive; a ratchet is probably unnecessary [S]"
    if ratio >= 80:
        return "marginal. Brake mode may hold it cold and fail warm. Ratchet recommended [S]"
    return "WILL back-drive. Brake mode is not a holding strategy. Ratchet or counterbalance [S]"


def optimise_gas_spring(a_kwargs):
    """Scan gas-spring force and arm-anchor radius; report the pair that minimises peak net
    torque across the sweep. This is the calculation that turns a 100:1 arm into a 40:1 arm."""
    best = None
    rows = []
    for r_in in (2.0, 3.0, 4.0, 5.0, 6.0):
        for f_lb in range(10, 210, 10):
            res = arm(gs_force_lbf=float(f_lb), gs_arm_r_in=r_in, **a_kwargs)
            rows.append((r_in, f_lb, res["worst_net_nm"]))
            if best is None or res["worst_net_nm"] < best[2]:
                best = (r_in, f_lb, res["worst_net_nm"])
    base = arm(**a_kwargs)["tau_grav_max_nm"]
    return best, base, rows


def fmt_elevator(r):
    L = []
    P = L.append
    P("=" * 79)
    P("ELEVATOR SIZING  --  %d x %s @ %.1f:1, %.2f in drum, %d-stage continuous rig"
      % (r["n_motors"], r["motor"], r["ratio"], r["pulley_in"], r["stages"]))
    P("  motor data: %s" % r["motor_src"])
    P("=" * 79)
    P("LOAD    carriage+game piece %.1f lb, travel %.0f in, friction allowance x%.2f"
      % (r["mass_lb"], r["travel_in"], r["friction_factor"]))
    P("  force at carriage ....................... %7.1f lbf" % r["carriage_force_lbf"])
    P("  force at drum (x %d stages) .............. %7.1f lbf" % (r["stages"], r["drum_force_lbf"]))
    P("")
    P("TORQUE")
    P("  to HOLD position ........................ %7.3f Nm  (%.1f in-lb)"
      % (r["tau_hold_nm"], r["tau_hold_nm"] / 0.112984829))
    P("  to ACCELERATE to %.2f s full travel ..... %7.3f Nm"
      % (r["target_time_s"], r["tau_accel_nm"]))
    P("  available at %.0f A limit ................. %7.3f Nm" % (r["current_limit"], r["tau_available_nm"]))
    P("  available at true stall (no limit) ...... %7.3f Nm" % r["tau_stall_avail_nm"])
    P("  --> dynamic margin ...................... %7.2f x  %s"
      % (r["torque_margin"], "OK" if r["torque_margin"] >= 1.5 else
         ("THIN -- want >= 1.5x" if r["torque_margin"] >= 1.0 else "FAILS -- will not lift")))
    P("")
    P("SPEED")
    P("  kinematic max carriage speed ............ %7.1f in/s" % r["v_max_ips"])
    P("  fastest possible full travel ............ %7.2f s  (target %.2f s)"
      % (r["t_min_kinematic_s"], r["target_time_s"]))
    if r["t_min_kinematic_s"] > r["target_time_s"]:
        P("  --> GEARED TOO SLOW for the target regardless of torque. Raise ratio numerator.")
    P("")
    P("HOLDING CURRENT -- the line that decides whether you need a ratchet")
    P("  current per motor to hold ............... %7.1f A  (%.0f%% of stall current)"
      % (r["i_hold_a"], 100 * r["hold_frac_of_stall"]))
    P("  thermal verdict [S] ..................... %s" % r["hold_thermal"])
    P("")
    P("COUNTERBALANCE / RATCHET SIZING")
    P("  constant-force spring to fully null gravity ... %.1f lbf at the carriage"
      % r["cf_spring_lbf"])
    P("  gas springs (a PAIR, one per side), by counterbalance fraction:")
    for f, frac in r["gas_spring_pairs"]:
        P("      %3.0f%% counterbalance -> 2 x %6.1f lbf gas springs" % (100 * frac, f))
    P("  holding current at 80%% counterbalance ......... %.1f A/motor (%s)"
      % (r["i_hold_with_80pct_cb"], thermal_verdict(r["i_hold_with_80pct_cb"] /
                                                    get("kraken_x60")["stall_a"])))
    P("  RATCHET/pawl must hold ........................ %.2f Nm (%.0f in-lb) at the DRUM shaft"
      % (r["ratchet_torque_nm_at_drum"], r["ratchet_torque_inlb_at_drum"]))
    P("  NOTE: spec the ratchet at the DRUM, not at the motor. At the motor it is %.0fx smaller"
      % r["ratio"])
    P("        and a slipping gearbox between ratchet and load makes the ratchet decorative.")
    return "\n".join(L)


def fmt_arm(r):
    L = []
    P = L.append
    P("=" * 79)
    P("ARM SIZING  --  %d x %s @ %.0f:1, %.1f lb at %.1f in CG radius"
      % (r["n_motors"], r["motor"], r["ratio"], r["mass_lb"], r["length_in"]))
    P("  motor data: %s" % r["motor_src"])
    P("=" * 79)
    P("  worst-case gravity torque (arm horizontal) .. %7.2f Nm  (%.0f in-lb)"
      % (r["tau_grav_max_nm"], r["tau_grav_max_inlb"]))
    P("  available at %.0f A limit ..................... %7.2f Nm"
      % (r["current_limit"], r["tau_available_nm"]))
    P("  available at true stall ...................... %7.2f Nm" % r["tau_stall_avail_nm"])
    P("  torque to also ACCELERATE (%.1f s sweep) ...... %7.2f Nm"
      % (r["target_time_s"], r["tau_accel_required_nm"]))
    P("  STATIC margin ................................ %7.2f x  %s"
      % (r["static_margin"], "OK" if r["static_margin"] >= 2.0 else "THIN -- want >= 2x on an arm"))
    P("  DYNAMIC margin ............................... %7.2f x  %s"
      % (r["dynamic_margin"], "OK" if r["dynamic_margin"] >= 1.5 else "THIN/FAILS"))
    P("  free-speed sweep time (no load) .............. %7.2f s  (target %.2f s)"
      % (r["free_sweep_time_s"], r["target_time_s"]))
    P("  holding current .............................. %7.1f A/motor (%.0f%% of stall)"
      % (r["i_hold_a"], 100 * r["hold_frac_of_stall"]))
    P("  thermal verdict [S] .......................... %s" % r["hold_thermal"])
    P("  back-drive ................................... %s" % r["backdrive"])
    P("")
    hdr = "  angle  gravity Nm"
    if r["gs_force_lbf"]:
        hdr += "  gasspring Nm     net Nm   hold A"
        P("  GAS SPRING: %.0f lbf at %.1f in on the arm, ground anchor (%.1f, %.1f) in from pivot"
          % (r["gs_force_lbf"], r["gs_arm_r_in"], r["gs_ground"][0], r["gs_ground"][1]))
    else:
        hdr += "                            net Nm   hold A"
    P(hdr)
    for (d, tg, gs, net, ih) in r["sweep"]:
        P("  %5d  %11.2f  %13.2f %10.2f %8.1f" % (d, tg, gs, net, ih))
    P("  (0 deg = horizontal, +90 = straight up. Worst |net| = %.2f Nm)" % r["worst_net_nm"])
    return "\n".join(L)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["elevator", "arm"], nargs="?", default="elevator")
    p.add_argument("--mass", type=float, default=None, help="lb, carriage+load or arm+game piece")
    p.add_argument("--travel", type=float, default=48.0, help="in, elevator only")
    p.add_argument("--stages", type=int, default=2, help="continuous-rig stage multiplier")
    p.add_argument("--pulley", type=float, default=1.75, help="in, drum/sprocket pitch dia")
    p.add_argument("--length", type=float, default=22.0, help="in, arm CG radius")
    p.add_argument("--ratio", type=float, default=None)
    p.add_argument("--motors", type=int, default=None)
    p.add_argument("--motor", default=None)
    p.add_argument("--limit", type=float, default=40.0)
    p.add_argument("--efficiency", type=float, default=None)
    p.add_argument("--time", type=float, default=None)
    p.add_argument("--gas-spring", action="store_true", help="arm: optimise gas-spring force")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.kind == "elevator":
        r = elevator(mass_lb=a.mass or 18.0, travel_in=a.travel, stages=a.stages,
                     ratio=a.ratio or 12.0, pulley_in=a.pulley, n_motors=a.motors or 2,
                     motor_key=a.motor or "kraken_x60", current_limit=a.limit,
                     efficiency=a.efficiency or 0.85, target_time_s=a.time or 1.0)
        print(json.dumps(r, indent=2) if a.json else fmt_elevator(r))
    else:
        kw = dict(mass_lb=a.mass or 12.0, length_in=a.length, ratio=a.ratio or 100.0,
                  n_motors=a.motors or 1, motor_key=a.motor or "neo", current_limit=a.limit,
                  efficiency=a.efficiency or 0.75, target_time_s=a.time or 1.2)
        if a.gas_spring:
            best, base, rows = optimise_gas_spring(kw)
            print("GAS-SPRING OPTIMISATION  (minimise peak |net torque| over the sweep)")
            print("  uncounterbalanced peak gravity torque .. %.2f Nm" % base)
            print("  best: %.0f lbf gas spring at %.1f in arm radius -> peak net %.2f Nm"
                  % (best[1], best[0], best[2]))
            print("  reduction .............................. %.0f%%"
                  % (100 * (1 - best[2] / base)))
            print("")
            print("  arm r (in)   spring (lbf)   peak net Nm")
            for (ri, fl, w) in rows:
                if fl % 40 == 0 and ri in (3.0, 4.0, 5.0):
                    print("  %9.1f   %12d   %11.2f" % (ri, fl, w))
            print("")
            print("  Then re-run with --ratio reduced by roughly the same factor: a %.0f%%%% torque"
                  % (100 * (1 - best[2] / base)))
            print("  reduction lets a 100:1 arm become ~30:1, which is 3x faster for free.")
            r = arm(gs_force_lbf=float(best[1]), gs_arm_r_in=best[0], **kw)
            print("")
            print(fmt_arm(r))
        else:
            r = arm(**kw)
            print(json.dumps({k: v for k, v in r.items() if k != "sweep"}, indent=2)
                  if a.json else fmt_arm(r))
