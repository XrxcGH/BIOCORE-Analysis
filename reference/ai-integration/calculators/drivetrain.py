#!/usr/bin/env python3
"""
drivetrain.py -- speed / torque / current / brownout for an FRC drivetrain.

Answers the four questions a kickoff-day drivetrain argument actually turns on:
  1. How fast does it go, really (not the free-speed number on the box)?
  2. Can it push, or does it slip first?
  3. What does a full-throttle push cost in AMPS, and does the bus brown out?
  4. Which gear ratio should we order, given we get exactly one order?

USAGE
  python drivetrain.py                                   # 4x Kraken X60, 6.12:1, 4in, 125 lb
  python drivetrain.py --motor neo_vortex --ratio 5.5 --weight 120 --limit 50
  python drivetrain.py --sweep                           # gear-ratio table, the useful one
  python drivetrain.py --json

MODEL, honestly stated
  * Motor: V = I*R_m + ke*w, tau = kt*I_stator, with R_m = 12/I_stall and kt = tau_stall/I_stall.
  * STATOR vs SUPPLY CURRENT -- the distinction most spreadsheets get wrong. A motor controller is
    a buck converter. The 60 A you set as a "current limit" is STATOR current. What the battery and
    the 120 A main breaker see is SUPPLY current = duty * I_stator, and at low speed duty is small.
    A 4-motor drivetrain stalled at 60 A/motor pulls ~240 A of stator current but only ~35 A off the
    battery. This is why current-limited robots do not trip the main breaker on contact, and why
    a model that reports 240 A at the breaker is wrong by a factor of seven.
  * Bus sag: V = Voc - I_supply_total*(R_batt + R_wire), fixed-point, damped. NOT a transient model.
    It does NOT model the inductive spike on a direction reversal, which is what actually browns
    out real robots. Treat a "pass" here as necessary, not sufficient.
  * Traction: one coefficient of friction, all wheels equally loaded. Real robots transfer weight
    (see cg_tip.py) and real carpet varies by venue.
  * No aero drag. One constant rolling-resistance term.
"""
import argparse, json, math, sys
from motors import get, bus_voltage, BATTERY, LBF_PER_N, IN_PER_M, G_MS2

# Coefficient of friction on FRC carpet by tread. [H] community-consensus planning values,
# NOT measured in this corpus. Measure yours with a fish scale before betting a match on it.
COF = {"blue_nitrile": 1.10, "black_nitrile": 1.05, "roughtop": 1.15, "colson": 1.00,
       "plaction": 0.90, "omni": 0.60, "billet_tread": 1.20, "mecanum": 0.55}


def analyze(motor_key="kraken_x60", n_motors=4, ratio=6.12, wheel_in=4.0, weight_lb=125.0,
            cof=1.10, current_limit=60.0, efficiency=0.92, aux_amps=25.0,
            drive_wheels_fraction=1.0, rolling_resist=0.015, dt=0.002, t_max=4.0,
            sprint_m=3.048):
    m = get(motor_key)
    r = (wheel_in / 2.0) / IN_PER_M
    mass = weight_lb / LBF_PER_N / G_MS2
    normal_n = weight_lb / LBF_PER_N * drive_wheels_fraction

    r_m = 12.0 / m["stall_a"]                       # winding resistance, ohms
    kt = m["stall_nm"] / m["stall_a"]               # Nm per stator amp
    ke = (12.0 - m["free_a"] * r_m) / m["w_free"]   # V per rad/s

    v_free = m["w_free"] / ratio * r
    f_traction = cof * normal_n
    tau_at_limit = kt * current_limit
    f_motor_limit = n_motors * tau_at_limit * ratio * efficiency / r
    f_motor_stall = n_motors * m["stall_nm"] * ratio * efficiency / r
    f_roll = rolling_resist * weight_lb / LBF_PER_N

    def operating_point(w_motor, v_bus):
        """Return (torque Nm, stator A, supply A, duty) at full throttle."""
        i_nat = max(0.0, (v_bus - ke * w_motor) / r_m)
        i_st = min(current_limit, i_nat)
        tau = kt * i_st
        f = n_motors * tau * ratio * efficiency / r
        if f > f_traction:                          # slipping: back off to the traction limit
            tau = f_traction * r / (n_motors * ratio * efficiency)
            i_st = tau / kt
        duty = min(1.0, (i_st * r_m + ke * w_motor) / max(v_bus, 0.1))
        return tau, i_st, duty * i_st, duty

    # --- steady push into a wall: shaft speed zero ---
    v_push = BATTERY["v_oc"]
    tau_p = i_st_p = i_sup_p = duty_p = 0.0
    for _ in range(30):
        tau_p, i_st_p, i_sup_p, duty_p = operating_point(0.0, v_push)
        i_tot_p = n_motors * i_sup_p + aux_amps
        v_push = 0.5 * v_push + 0.5 * bus_voltage(i_tot_p)
    push_amps = n_motors * i_sup_p + aux_amps
    f_push = min(n_motors * tau_p * ratio * efficiency / r, f_traction)
    # and the same push with the limit switched OFF -- the case that trips the breaker
    v_nolimit = BATTERY["v_oc"]
    for _ in range(30):
        i_nl = v_nolimit / r_m
        tau_nl = kt * i_nl
        f_nl = n_motors * tau_nl * ratio * efficiency / r
        if f_nl > f_traction:
            i_nl = (f_traction * r / (n_motors * ratio * efficiency)) / kt
        duty_nl = min(1.0, i_nl * r_m / max(v_nolimit, 0.1))
        i_tot_nl = n_motors * duty_nl * i_nl + aux_amps
        v_nolimit = 0.5 * v_nolimit + 0.5 * bus_voltage(i_tot_nl)

    # --- sprint simulation ---
    v = x = t = 0.0
    peak_supply = peak_stator = 0.0
    min_v = BATTERY["v_oc"]
    t_sprint = None
    trace = []
    v_bus = BATTERY["v_oc"]
    settled = 0
    while t < t_max:
        w_motor = (v / r) * ratio
        for _ in range(20):
            tau, i_st, i_sup, duty = operating_point(w_motor, v_bus)
            v_bus = 0.5 * v_bus + 0.5 * bus_voltage(n_motors * i_sup + aux_amps)
        i_tot = n_motors * i_sup + aux_amps
        f_m = min(n_motors * tau * ratio * efficiency / r, f_traction)
        a = (f_m - f_roll) / mass
        v += a * dt
        x += v * dt
        t += dt
        peak_supply = max(peak_supply, i_tot)
        peak_stator = max(peak_stator, n_motors * i_st)
        min_v = min(min_v, v_bus)
        if not trace or t - trace[-1][0] >= 0.25:
            trace.append((t, v, i_tot, v_bus))
        if t_sprint is None and x >= sprint_m:
            t_sprint = t
        settled = settled + 1 if (a < 0.05 and v > 0.5) else 0
        if settled > 40:
            break

    return dict(
        stator_push_a=n_motors * i_st_p, push_duty=duty_p,
        nolimit_push_amps=i_tot_nl, nolimit_bus_v=v_nolimit,
        sprint_peak_stator_a=peak_stator,
        motor=m["name"], motor_src=m["src"], n_motors=n_motors, ratio=ratio, wheel_in=wheel_in,
        weight_lb=weight_lb, cof=cof, current_limit=current_limit, efficiency=efficiency,
        free_speed_fps=v_free * IN_PER_M / 12.0,
        sim_top_speed_fps=v * IN_PER_M / 12.0,
        speed_realism_pct=(100.0 * v / v_free) if v_free else 0.0,
        traction_limit_lbf=f_traction * LBF_PER_N,
        motor_force_at_limit_lbf=f_motor_limit * LBF_PER_N,
        motor_force_at_stall_lbf=f_motor_stall * LBF_PER_N,
        traction_limited=bool(f_motor_limit > f_traction),
        push_force_lbf=f_push * LBF_PER_N,
        push_total_amps=push_amps, push_bus_v=v_push,
        sprint_10ft_s=t_sprint, sprint_peak_amps=peak_supply, sprint_min_bus_v=min_v,
        brownout_v=BATTERY["brownout_v"],
        brownout_verdict=("BROWNOUT RISK" if min(v_push, min_v) < BATTERY["brownout_v"] else "pass"),
        breaker_verdict=("OVER 120 A MAIN BREAKER" if push_amps > BATTERY["main_breaker_a"]
                         else "under 120 A main breaker"),
        nolimit_breaker_verdict=("OVER 120 A -- breaker trips" if i_tot_nl > BATTERY["main_breaker_a"]
                                 else "under 120 A"),
        trace=trace,
    )


def fmt(rs):
    L = []
    P = L.append
    P("=" * 79)
    P("DRIVETRAIN ANALYSIS  --  %d x %s" % (rs["n_motors"], rs["motor"]))
    P("  motor data: %s" % rs["motor_src"])
    P("=" * 79)
    P("CONFIG  ratio %.2f:1 | wheel %.1f in | robot %.0f lb | COF %.2f | %.0f A/motor | eta %.2f"
      % (rs["ratio"], rs["wheel_in"], rs["weight_lb"], rs["cof"], rs["current_limit"],
         rs["efficiency"]))
    P("")
    P("SPEED")
    P("  theoretical free speed .................. %6.2f ft/s   <- the number on the box"
      % rs["free_speed_fps"])
    P("  simulated top speed (loaded, sagging) ... %6.2f ft/s   (%.0f%% of free)"
      % (rs["sim_top_speed_fps"], rs["speed_realism_pct"]))
    P("  0 -> 10 ft .............................. %s"
      % (("%.2f s" % rs["sprint_10ft_s"]) if rs["sprint_10ft_s"] else "not reached in window"))
    P("")
    P("FORCE  (whichever is smaller decides whether you push or spin)")
    P("  traction limit (COF x weight) ........... %6.1f lbf" % rs["traction_limit_lbf"])
    P("  motor force at %3.0f A limit ............. %6.1f lbf"
      % (rs["current_limit"], rs["motor_force_at_limit_lbf"]))
    P("  motor force at true stall (no limit) .... %6.1f lbf" % rs["motor_force_at_stall_lbf"])
    if rs["traction_limited"]:
        P("  --> TRACTION-LIMITED. Wheels slip before motors stall. Correct design point.")
    else:
        P("  --> TORQUE-LIMITED. You stall and cook motors before you slip. GEAR DOWN.")
    P("")
    P("CURRENT / BROWNOUT   (Systemcore brownout threshold UNVERIFIED -- see motors.py)")
    P("  PUSH INTO A WALL, limit ON:")
    P("    stator current (what heats the motor) . %6.1f A total, duty %.0f%%"
      % (rs["stator_push_a"], 100 * rs["push_duty"]))
    P("    SUPPLY current (what the breaker sees)  %6.1f A total, bus %.2f V"
      % (rs["push_total_amps"], rs["push_bus_v"]))
    P("    sustained push force .................. %6.1f lbf" % rs["push_force_lbf"])
    P("    main breaker .......................... %s" % rs["breaker_verdict"])
    P("  PUSH INTO A WALL, limit OFF (do not do this):")
    P("    SUPPLY current ........................ %6.1f A, bus %.2f V --> %s"
      % (rs["nolimit_push_amps"], rs["nolimit_bus_v"], rs["nolimit_breaker_verdict"]))
    P("  SPRINT:")
    P("    peak supply current ................... %6.1f A, bus min %.2f V"
      % (rs["sprint_peak_amps"], rs["sprint_min_bus_v"]))
    P("    peak stator current ................... %6.1f A" % rs["sprint_peak_stator_a"])
    P("  brownout threshold (roboRIO 1) .......... %6.2f V  --> %s"
      % (rs["brownout_v"], rs["brownout_verdict"]))
    if rs["brownout_verdict"] != "pass":
        P("    FIX [S]: drop the per-motor limit to ~%.0f A, or slew-rate-limit the joystick so"
          % (rs["current_limit"] * 0.65))
        P("    all four motors never command full throttle from a standstill simultaneously.")
    P("")
    P("SPRINT TRACE    t(s)   v(ft/s)   I_total(A)   V_bus")
    for (t, v, i, vb) in rs["trace"][:9]:
        P("               %5.2f   %7.2f   %10.1f   %5.2f" % (t, v * IN_PER_M / 12.0, i, vb))
    return "\n".join(L)


def sweep(args):
    print("GEAR-RATIO SWEEP  --  %d x %s, %.1f in wheel, %.0f lb, COF %.2f, %.0f A limit"
          % (args.motors, get(args.motor)["name"], args.wheel, args.weight, args.cof, args.limit))
    print("%7s %10s %10s %9s %10s %9s %8s  %s"
          % ("ratio", "free ft/s", "top ft/s", "0-10ft s", "traction", "F@limit", "push A",
             "verdict"))
    for ratio in [4.0, 4.5, 5.0, 5.5, 6.0, 6.12, 6.75, 7.5, 8.5, 10.0]:
        r = analyze(args.motor, args.motors, ratio, args.wheel, args.weight, args.cof,
                    args.limit, args.efficiency, args.aux)
        v = "traction-limited OK" if r["traction_limited"] else "TORQUE-LIMITED"
        print("%7.2f %10.2f %10.2f %9s %10.1f %9.1f %8.0f  %s"
              % (ratio, r["free_speed_fps"], r["sim_top_speed_fps"],
                 ("%.2f" % r["sprint_10ft_s"]) if r["sprint_10ft_s"] else "  --",
                 r["traction_limit_lbf"], r["motor_force_at_limit_lbf"], r["push_total_amps"], v))
    print("")
    print("PICK RULE [S]: take the FASTEST ratio still traction-limited at your current limit,")
    print("then step one slower for margin. Speed you cannot put on the carpet is not speed.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--motor", default="kraken_x60")
    p.add_argument("--motors", type=int, default=4)
    p.add_argument("--ratio", type=float, default=6.12)
    p.add_argument("--wheel", type=float, default=4.0)
    p.add_argument("--weight", type=float, default=125.0, help="lb WITH bumpers + battery")
    p.add_argument("--cof", type=float, default=COF["blue_nitrile"])
    p.add_argument("--limit", type=float, default=60.0, help="A per motor, supply-side")
    p.add_argument("--efficiency", type=float, default=0.92)
    p.add_argument("--aux", type=float, default=25.0, help="A drawn by everything not drive")
    p.add_argument("--sweep", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.sweep:
        sweep(a)
        sys.exit(0)
    res = analyze(a.motor, a.motors, a.ratio, a.wheel, a.weight, a.cof, a.limit,
                  a.efficiency, a.aux)
    if a.json:
        res.pop("trace")
        print(json.dumps(res, indent=2))
    else:
        print(fmt(res))
