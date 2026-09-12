#!/usr/bin/env python3
"""
cg_tip.py -- centre of gravity roll-up and tip-over analysis.

The two questions this answers, both of which are decided in CAD and discovered on carpet:
  1. Where is the CG, and does the weight budget close? (2026 R103: 115.0 lb bare; R408: 135.0 lb
     with BUMPERS -- a [H] BASELINE, the BIOCORE limits do not exist until 2027-01-09.)
  2. At what acceleration / ramp angle does it tip -- with the mechanism DOWN and with it UP?

The load-bearing insight the tool exists to produce: on a well-designed FRC robot you should
SLIDE before you TIP. If the tipping acceleration is below the traction-limited acceleration
(mu * g), the robot tips instead of slipping, and no amount of driver skill fixes that.

USAGE
  python cg_tip.py                              # built-in worked example
  python cg_tip.py --parts myrobot.json
  python cg_tip.py --extend "arm_extended,14,0,26,0"    # name,mass_lb,x,y,z of a moved mass
  python cg_tip.py --json

PARTS FILE FORMAT (JSON list). Coordinates in INCHES, origin at the centre of the frame
footprint at CARPET level. +x forward, +y left, +z up.
  [{"name":"drivetrain","mass_lb":38,"x":0,"y":0,"z":3.0}, ...]
"""
import argparse, json, math, sys

G = 32.174  # ft/s^2

# A worked example: a plausible 2-mechanism COTS robot for a 15-student team, consistent with
# reference/bom/mechanism_catalog.yaml architectures. Masses are [S] planning estimates.
DEFAULT_PARTS = [
    {"name": "swerve modules + drive motors (4)", "mass_lb": 34.0, "x": 0.0, "y": 0.0, "z": 3.0},
    {"name": "frame + belly pan + tube",          "mass_lb": 16.0, "x": 0.0, "y": 0.0, "z": 3.5},
    {"name": "bumpers (4 sides)",                 "mass_lb": 18.0, "x": 0.0, "y": 0.0, "z": 5.5},
    {"name": "battery",                           "mass_lb": 12.9, "x": -8.0, "y": 0.0, "z": 4.0},
    {"name": "electrical board + PD + Systemcore", "mass_lb": 8.0, "x": -4.0, "y": 0.0, "z": 6.0},
    {"name": "elevator frame (static)",           "mass_lb": 11.0, "x": 2.0, "y": 0.0, "z": 22.0},
    {"name": "elevator carriage + end effector",  "mass_lb": 14.0, "x": 6.0, "y": 0.0, "z": 12.0},
    {"name": "intake",                            "mass_lb": 9.0, "x": 13.0, "y": 0.0, "z": 7.0},
    {"name": "pneumatics / misc / fasteners",     "mass_lb": 6.0, "x": 0.0, "y": 0.0, "z": 8.0},
]

# 2026 baseline limits [H]. BIOCORE values UNKNOWN until 2027-01-09.
LIMIT_BARE_LB = 115.0     # 2026 R103, excluding BUMPERS, battery, event location tags
LIMIT_BUMPERED_LB = 135.0  # 2026 R408


def cg(parts):
    m = sum(p["mass_lb"] for p in parts)
    if m <= 0:
        raise SystemExit("total mass is zero")
    return (m,
            sum(p["mass_lb"] * p["x"] for p in parts) / m,
            sum(p["mass_lb"] * p["y"] for p in parts) / m,
            sum(p["mass_lb"] * p["z"] for p in parts) / m)


def analyse(parts, wheelbase_in=24.0, track_in=24.0, cof=1.10, label="baseline"):
    m, x, y, z = cg(parts)
    half_wb = wheelbase_in / 2.0
    half_tr = track_in / 2.0
    d_fwd = half_wb - x
    d_rev = half_wb + x
    d_left = half_tr - y
    d_right = half_tr + y
    zz = max(z, 1e-6)

    def tip_a(d):
        return d / zz            # in g

    def tip_angle(d):
        return math.degrees(math.atan2(d, zz))

    bumpered = m
    bare_est = m - sum(p["mass_lb"] for p in parts
                       if "bumper" in p["name"].lower() or "battery" in p["name"].lower())
    slides_first = cof < min(tip_a(d_fwd), tip_a(d_rev), tip_a(d_left), tip_a(d_right))
    return dict(
        label=label, total_lb=m, cg_x=x, cg_y=y, cg_z=z,
        wheelbase_in=wheelbase_in, track_in=track_in, cof=cof,
        bumpered_lb=bumpered, bare_estimate_lb=bare_est,
        limit_bare=LIMIT_BARE_LB, limit_bumpered=LIMIT_BUMPERED_LB,
        weight_verdict_bare=("OVER 2026 R103 BY %.1f lb" % (bare_est - LIMIT_BARE_LB))
        if bare_est > LIMIT_BARE_LB else "under 2026 R103 by %.1f lb" % (LIMIT_BARE_LB - bare_est),
        weight_verdict_bumpered=("OVER 2026 R408 BY %.1f lb" % (bumpered - LIMIT_BUMPERED_LB))
        if bumpered > LIMIT_BUMPERED_LB else
        "under 2026 R408 by %.1f lb" % (LIMIT_BUMPERED_LB - bumpered),
        tip_g={"forward (braking)": tip_a(d_rev), "backward (accelerating)": tip_a(d_fwd),
               "left": tip_a(d_right), "right": tip_a(d_left)},
        tip_angle_deg={"pitch fwd": tip_angle(d_rev), "pitch back": tip_angle(d_fwd),
                       "roll left": tip_angle(d_right), "roll right": tip_angle(d_left)},
        traction_a_g=cof, slides_before_tips=slides_first,
        min_tip_g=min(tip_a(d_fwd), tip_a(d_rev), tip_a(d_left), tip_a(d_right)),
        wheel_load_static={"front": 0.5 * m * (1 + x / half_wb) if half_wb else 0,
                           "rear": 0.5 * m * (1 - x / half_wb) if half_wb else 0},
        parts=parts,
    )


def fmt(r, alt=None):
    L = []
    P = L.append
    P("=" * 79)
    P("CG + TIP-OVER  --  %s" % r["label"])
    P("=" * 79)
    P("  %-42s %8s %7s %7s %7s" % ("component", "mass lb", "x in", "y in", "z in"))
    for p in r["parts"]:
        P("  %-42s %8.1f %7.1f %7.1f %7.1f" % (p["name"][:42], p["mass_lb"], p["x"], p["y"],
                                               p["z"]))
    P("  %-42s %8.1f" % ("TOTAL", r["total_lb"]))
    P("")
    P("CENTRE OF GRAVITY   x %+.2f in (fwd+)   y %+.2f in (left+)   z %.2f in (above carpet)"
      % (r["cg_x"], r["cg_y"], r["cg_z"]))
    P("  CG height as a fraction of half-track ... %.2f  (lower is better; < 1.0 is healthy [S])"
      % (r["cg_z"] / (r["track_in"] / 2.0)))
    P("")
    P("WEIGHT vs the 2026 BASELINE limits [H] -- BIOCORE limits UNKNOWN until 2027-01-09")
    P("  with bumpers ......... %6.1f lb  vs %.1f lb (2026 R408)  --> %s"
      % (r["bumpered_lb"], r["limit_bumpered"], r["weight_verdict_bumpered"]))
    P("  bare estimate ........ %6.1f lb  vs %.1f lb (2026 R103)  --> %s"
      % (r["bare_estimate_lb"], r["limit_bare"], r["weight_verdict_bare"]))
    P("  (bare estimate = total minus anything named 'bumper' or 'battery'. Crude. Weigh it.)")
    P("")
    P("TIP-OVER   wheelbase %.1f in, track %.1f in" % (r["wheelbase_in"], r["track_in"]))
    P("  %-26s %12s %14s" % ("direction", "tips at (g)", "static ramp (deg)"))
    keys = [("forward (braking)", "pitch fwd"), ("backward (accelerating)", "pitch back"),
            ("left", "roll left"), ("right", "roll right")]
    for a, b in keys:
        P("  %-26s %12.2f %14.1f" % (a, r["tip_g"][a], r["tip_angle_deg"][b]))
    P("")
    P("  traction-limited acceleration (COF %.2f) .. %.2f g" % (r["cof"], r["traction_a_g"]))
    P("  worst tipping acceleration ................ %.2f g" % r["min_tip_g"])
    if r["slides_before_tips"]:
        P("  --> SLIDES BEFORE IT TIPS. This is the design target. Margin %.0f%%."
          % (100 * (r["min_tip_g"] / r["traction_a_g"] - 1)))
    else:
        P("  --> TIPS BEFORE IT SLIDES. The driver CANNOT fix this. Fixes, in order of cost:")
        P("      1. move the battery low and toward the light corner (free)")
        P("      2. widen track/wheelbase to the frame perimeter maximum (cheap)")
        P("      3. lower the mechanism's stowed height (design)")
        P("      4. slew-rate-limit the drivetrain (software band-aid; costs cycle time)")
    if alt:
        P("")
        P("-" * 79)
        P("EXTENDED / SCORING CONFIGURATION: %s" % alt["label"])
        P("  CG moves to x %+.2f, y %+.2f, z %.2f in (was %+.2f, %+.2f, %.2f)"
          % (alt["cg_x"], alt["cg_y"], alt["cg_z"], r["cg_x"], r["cg_y"], r["cg_z"]))
        P("  worst tipping acceleration ................ %.2f g   (was %.2f g, %+.0f%%)"
          % (alt["min_tip_g"], r["min_tip_g"],
             100 * (alt["min_tip_g"] / r["min_tip_g"] - 1) if r["min_tip_g"] else 0))
        P("  worst static ramp angle ................... %.1f deg"
          % min(alt["tip_angle_deg"].values()))
        P("  --> %s" % ("still slides before it tips" if alt["slides_before_tips"] else
                        "TIPS BEFORE IT SLIDES WHEN EXTENDED. Interlock the drivetrain speed "
                        "against mechanism height in software, and say so in the design review."))
    P("")
    P("NEXT: feed the traction number into  python drivetrain.py --cof %.2f --weight %.0f"
      % (r["cof"], r["total_lb"]))
    return "\n".join(L)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--parts", help="JSON file of components")
    p.add_argument("--wheelbase", type=float, default=24.0)
    p.add_argument("--track", type=float, default=24.0)
    p.add_argument("--cof", type=float, default=1.10)
    p.add_argument("--extend", default="elevator carriage + end effector,14,6,0,52",
                   help="name,mass_lb,x,y,z -- REPLACES the same-named part to model deployment")
    p.add_argument("--no-extend", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    parts = json.load(open(a.parts)) if a.parts else [dict(q) for q in DEFAULT_PARTS]
    base = analyse(parts, a.wheelbase, a.track, a.cof, "stowed / driving configuration")
    alt = None
    if not a.no_extend and a.extend:
        f = a.extend.split(",")
        nm, ml, x, y, z = f[0], float(f[1]), float(f[2]), float(f[3]), float(f[4])
        parts2 = [dict(q) for q in parts]
        hit = False
        for q in parts2:
            if q["name"] == nm:
                q.update(mass_lb=ml, x=x, y=y, z=z)
                hit = True
        if not hit:
            parts2.append({"name": nm, "mass_lb": ml, "x": x, "y": y, "z": z})
        alt = analyse(parts2, a.wheelbase, a.track, a.cof, nm)
    if a.json:
        out = {"stowed": {k: v for k, v in base.items() if k != "parts"}}
        if alt:
            out["extended"] = {k: v for k, v in alt.items() if k != "parts"}
        print(json.dumps(out, indent=2))
    else:
        print(fmt(base, alt))
