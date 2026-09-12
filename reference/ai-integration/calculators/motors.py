#!/usr/bin/env python3
"""
motors.py -- the shared FRC motor table for every calculator in this directory.

EVIDENCE LABELS ON EVERY ROW. `src` is one of:
  [C] parts_electronics.yaml   -- transcribed from a live vendor page 2026-08-22 by the BOM pass.
                                  This is the ONLY tier you should quote in a design review.
  [H] vendor motor curve       -- widely published motor-curve values, NOT re-verified in this
                                  corpus on 2026-08-22. Treat as planning-grade. Check before
                                  you commit a gear ratio to a machinist.
  UNVERIFIED                   -- legality for 2027 not established (R501 Table 8-1 is a 2026
                                  reference; the BIOCORE motor list does not exist until
                                  2027-01-09).

MODEL: the standard linear brushed/BLDC approximation used by every FRC design calculator.
    tau(w)  = tau_stall * (1 - w/w_free)
    I(w)    = I_free + (I_stall - I_free) * (1 - w/w_free)
    kt      = tau_stall / (I_stall - I_free)      [Nm per amp of *torque-producing* current]
It is a straight line through two measured endpoints. It is good to roughly +/-10% in the
region teams actually operate (20-70% of free speed) and it is WRONG near stall for a
thermally soaked motor. See "Known limitations" in 02_ai_for_design_and_cad.md.
"""
import math

NM_PER_INLB = 0.112984829
G_MS2 = 9.80665
LBF_PER_N = 0.224808943
IN_PER_M = 39.3700787

MOTORS = {
    # key                name                         free_rpm stall_nm stall_a free_a  src
    "kraken_x60":   dict(name="Kraken X60 (trapezoidal)", free_rpm=6000, stall_nm=7.09, stall_a=366, free_a=2.0,
                         src="[C] parts_electronics.yaml:125 (WCP motor-performance page)"),
    "kraken_x60_foc": dict(name="Kraken X60 (FOC)",       free_rpm=5800, stall_nm=9.37, stall_a=483, free_a=2.0,
                         src="[C] parts_electronics.yaml:126"),
    "kraken_x44":   dict(name="Kraken X44 (trapezoidal)", free_rpm=7758, stall_nm=4.11, stall_a=279, free_a=3.0,
                         src="[C] parts_electronics.yaml:146"),
    "kraken_x44_foc": dict(name="Kraken X44 (FOC)",       free_rpm=7368, stall_nm=5.01, stall_a=329, free_a=3.0,
                         src="[C] parts_electronics.yaml:147"),
    "neo_vortex":   dict(name="REV NEO Vortex",           free_rpm=6784, stall_nm=3.60, stall_a=211, free_a=3.6,
                         src="[C] parts_electronics.yaml:162 (free_a [H], not listed)"),
    "neo":          dict(name="REV NEO v1.1 (empirical)", free_rpm=5676, stall_nm=2.60, stall_a=105, free_a=1.8,
                         src="[C] parts_electronics.yaml:178 (free_a [H], not listed)"),
    "neo_theo":     dict(name="REV NEO v1.1 (theoretical)", free_rpm=5676, stall_nm=3.75, stall_a=150, free_a=1.8,
                         src="[C] parts_electronics.yaml:179 -- OPTIMISTIC, do not size to this"),
    "neo550":       dict(name="REV NEO 550",             free_rpm=11000, stall_nm=0.97, stall_a=100, free_a=1.4,
                         src="[C] parts_electronics.yaml:192 (free_a [H], not listed)"),
    "cim":          dict(name="CIM (FR801-001)",          free_rpm=5330, stall_nm=2.41, stall_a=131, free_a=2.7,
                         src="[H] vendor motor curve, NOT re-verified in this corpus"),
    "minicim":      dict(name="MiniCIM",                  free_rpm=5840, stall_nm=1.41, stall_a=89,  free_a=3.0,
                         src="[H] vendor motor curve, NOT re-verified in this corpus"),
    "falcon500":    dict(name="Falcon 500 (DISCONTINUED)", free_rpm=6380, stall_nm=4.69, stall_a=257, free_a=1.5,
                         src="[H] vendor motor curve, NOT re-verified. UNVERIFIED for 2027 legality"),
    "775pro":       dict(name="775pro",                   free_rpm=18730, stall_nm=0.71, stall_a=134, free_a=0.7,
                         src="[H] vendor motor curve, NOT re-verified in this corpus"),
}

# Battery / bus model. All [S] planning values -- see Known limitations.
BATTERY = dict(
    v_oc=12.7,            # open-circuit of a healthy, freshly charged MK/Interstate-class SLA [S]
    r_internal_ohm=0.015, # 11-20 mOhm for a healthy FRC SLA; degrades hard with age/cycles [S]
    r_wiring_ohm=0.008,   # main breaker + 6 AWG + PD board + Anderson connectors [S]
    brownout_v=6.8,       # roboRIO 1 threshold. roboRIO 2 = 6.3 V.
                          # SYSTEMCORE BROWNOUT THRESHOLD IS **UNVERIFIED** as of 2026-08-22.
    main_breaker_a=120,   # Eaton Bussmann CB285-120, parts_electronics.yaml:335 [C]
)


def get(key):
    if key not in MOTORS:
        raise SystemExit("unknown motor %r. known: %s" % (key, ", ".join(sorted(MOTORS))))
    m = dict(MOTORS[key]); m["key"] = key
    m["w_free"] = m["free_rpm"] * 2 * math.pi / 60.0
    m["kt"] = m["stall_nm"] / (m["stall_a"] - m["free_a"])
    m["peak_w"] = m["stall_nm"] * m["w_free"] / 4.0
    return m


def torque_at(m, rpm, v_bus=12.0, current_limit=None):
    """Available torque (Nm) at a shaft speed, derated for bus voltage and a current limit."""
    scale = max(0.0, v_bus / 12.0)
    frac = min(1.0, max(0.0, abs(rpm) / (m["free_rpm"] * scale))) if scale > 0 else 1.0
    tau = m["stall_nm"] * scale * (1.0 - frac)
    cur = m["free_a"] + (m["stall_a"] - m["free_a"]) * (1.0 - frac)
    if current_limit is not None and cur > current_limit:
        cur = current_limit
        tau = min(tau, m["kt"] * max(0.0, current_limit - m["free_a"]))
    return tau, cur


def bus_voltage(total_amps, batt=BATTERY):
    return batt["v_oc"] - total_amps * (batt["r_internal_ohm"] + batt["r_wiring_ohm"])


def table():
    print("%-28s %8s %9s %8s %7s %8s %8s  %s" %
          ("motor", "free RPM", "stall Nm", "stall A", "free A", "kt Nm/A", "peak W", "source"))
    for k in MOTORS:
        m = get(k)
        print("%-28s %8d %9.2f %8d %7.1f %8.4f %8.0f  %s" %
              (m["name"], m["free_rpm"], m["stall_nm"], m["stall_a"], m["free_a"],
               m["kt"], m["peak_w"], m["src"]))


if __name__ == "__main__":
    print("FRC motor table -- shared by drivetrain.py, elevator_arm.py, fourbar.py, cg_tip.py\n")
    table()
    print("\nBattery/bus model [S]: Voc=%.2f V, R_total=%.3f ohm, brownout=%.1f V (roboRIO 1)."
          % (BATTERY["v_oc"], BATTERY["r_internal_ohm"] + BATTERY["r_wiring_ohm"], BATTERY["brownout_v"]))
    print("SYSTEMCORE BROWNOUT THRESHOLD: **UNVERIFIED** as of 2026-08-22. Re-check after the")
    print("2026-11-12 Pre-Kickoff Virtual Kit Release before trusting any brownout verdict below.")
