#!/usr/bin/env python3
"""
capacity_model.py -- effective-hours, role-coverage and parallel-workstream model
for a small FRC team.  Companion to reference/02_TEAM_CAPACITY_MODEL.md and
reference/team_capacity.yaml.

Every number printed by this script is derived, not asserted.  Change the inputs
on the command line and the whole model moves with them.

Usage
  python tools/capacity_model.py                      # full scenario table
  python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week1
  python tools/capacity_model.py --yaml               # + the calibrated constants
"""
import argparse, datetime as dt, json

# ---------------------------------------------------------------- 2027 calendar
# All [C] from research/03_biocore_official_intel.md (FIRST 2027 season calendar).
KICKOFF = dt.date(2027, 1, 9)
MILESTONE = {
    "weekzero": dt.date(2027, 2, 20),   # Week Zero
    "week1":    dt.date(2027, 3, 3),    # Week 1 competition events begin
    "week2":    dt.date(2027, 3, 10),
    "week3":    dt.date(2027, 3, 17),
    "week4":    dt.date(2027, 3, 24),
    "week6":    dt.date(2027, 4, 7),
    "champs":   dt.date(2027, 4, 28),
}

# ---------------------------------------------------------------- model constants
# Tier: (label, headcount, attendance_rate, productivity_coefficient)
# Coefficient 1.00 == one hour of a competent veteran student who works unsupervised.
TIERS_15 = [
    ("core technical (3 build + 2 program)", 5, 0.85, 1.00),
    ("contributing veteran",                 4, 0.65, 0.55),
    ("first-year",                           6, 0.50, 0.35),
]

CALENDAR_FACTOR   = 0.88   # exams, MLK, Presidents Day, snow, testing, club conflicts
MENTOR_SOFT_CAP_H = 16.0   # scheduled h/wk past which marginal hours are worth less
MARGINAL_HOUR_VAL = 0.75   # value of a scheduled hour above the soft cap

# training tax: veteran-hours consumed per first-year attended-hour, by season phase
TAX = [(2, 0.50), (4, 0.25), (999, 0.10)]   # (through week N, draw rate)

HOURS_PER_NOVEL_MECHANISM = 90   # prototype -> CAD -> fab -> mount -> iterate -> reliable

# effective-hour budget lines, kickoff -> first event (fractions of the total)
ALLOCATION = [
    ("strategy / rule reading / game analysis", 0.0417),
    ("CAD + design",                            0.1250),
    ("fabrication + assembly",                  0.2167),
    ("electrical + pneumatics",                 0.0833),
    ("programming (incl. SystemCore port)",     0.2250),
    ("integration, debug, reliability",         0.1417),
    ("drive practice",                          0.0917),
    ("awards / business / media / scouting",    0.0750),
]


def weeks_between(a, b):
    return (b - a).days / 7.0


def scheduled_per_week(h):
    """Mentor-supervision soft cap: hours above MENTOR_SOFT_CAP_H are worth less."""
    return min(h, MENTOR_SOFT_CAP_H) + max(0.0, h - MENTOR_SOFT_CAP_H) * MARGINAL_HOUR_VAL


def training_tax_per_first_year(attended_h, weeks):
    """Veteran-hours drawn out of the pool by ONE first-year over the whole span."""
    drawn, prev = 0.0, 0.0
    for thru, rate in TAX:
        wk = min(thru, weeks) - prev
        if wk <= 0:
            break
        drawn += attended_h * (wk / weeks) * rate
        prev = min(thru, weeks)
    return drawn


def model(students=15, hpw=15.0, weeks=7.57, tiers=None):
    tiers = tiers or TIERS_15
    scale = students / sum(t[1] for t in tiers)
    sched_wk = scheduled_per_week(hpw)
    scheduled = sched_wk * weeks
    available = scheduled * CALENDAR_FACTOR
    nominal = students * hpw * weeks

    rows, total, tax_total, fy_gross = [], 0.0, 0.0, 0.0
    for label, n, att, coef in tiers:
        n_scaled = n * scale
        attended = available * att
        veq = attended * coef * n_scaled
        rows.append((label, n_scaled, att, attended, coef, veq))
        total += veq
        if label.startswith("first-year"):
            fy_gross = veq
            tax_total = training_tax_per_first_year(attended, weeks) * n_scaled
    net = total - tax_total
    return {
        "students": students, "hpw": hpw, "weeks": weeks,
        "sched_hpw_effective": sched_wk,
        "scheduled_h": scheduled, "available_h": available,
        "nominal_person_h": nominal,
        "rows": rows,
        "gross_veq_h": total, "training_tax_h": tax_total,
        "effective_veq_h": net,
        "veq_per_week": net / weeks,
        "multiplier": net / nominal,
        "first_year_net_h": fy_gross - tax_total,
    }


def workstreams(m, tiers=None):
    tiers = tiers or TIERS_15
    leads = tiers[0][1] * (m["students"] / sum(t[1] for t in tiers))
    mech_leads = leads - 2          # 2 of the 5 core are the programmers
    route_a = mech_leads - 1        # drivetrain permanently consumes one lead
    budget = m["effective_veq_h"]
    residual = budget * (ALLOCATION[1][1] + ALLOCATION[2][1])   # CAD + fabrication
    route_b = residual / HOURS_PER_NOVEL_MECHANISM
    return {"leads": leads, "mech_leads": mech_leads,
            "route_a_novel_mechanisms": route_a,
            "residual_mech_h": residual,
            "route_b_novel_mechanisms": route_b,
            "route_c_novel_mechanisms": 2.0}   # single-machine shop queue saturation


def print_scenario(name, m):
    print("")
    print("--- %s: %d students, %.0f sched h/wk, %.2f weeks ---"
          % (name, m["students"], m["hpw"], m["weeks"]))
    print("  scheduled h/wk after mentor soft cap : %.2f" % m["sched_hpw_effective"])
    print("  calendar hours available per student : %.1f   (x%.2f calendar factor)"
          % (m["available_h"], CALENDAR_FACTOR))
    print("  %-38s %4s %5s %7s %5s %8s" % ("tier", "n", "att", "h ea", "coef", "veq-h"))
    for label, n, att, attended, coef, veq in m["rows"]:
        print("  %-38s %4.0f %4.0f%% %7.1f %5.2f %8.1f"
              % (label, n, att * 100, attended, coef, veq))
    print("  %-38s %4s %5s %7s %5s %8.1f" % ("gross", "", "", "", "", m["gross_veq_h"]))
    print("  %-38s %4s %5s %7s %5s %8.1f"
          % ("less first-year training tax", "", "", "", "", -m["training_tax_h"]))
    print("  %-38s %4s %5s %7s %5s %8.1f"
          % ("EFFECTIVE veteran-equivalent hours", "", "", "", "", m["effective_veq_h"]))
    print("  nominal person-hours                 : %.0f" % m["nominal_person_h"])
    print("  EFFECTIVE / NOMINAL multiplier       : %.3f" % m["multiplier"])
    print("  effective veq-hours per week         : %.1f" % m["veq_per_week"])
    print("  net contribution of the %.0f first-years : %+.1f veq-h over the whole span"
          % (m["rows"][2][1], m["first_year_net_h"]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--students", type=int, default=15)
    p.add_argument("--hours-per-week", type=float, default=15.0)
    p.add_argument("--deadline", default=None, choices=list(MILESTONE))
    p.add_argument("--yaml", action="store_true")
    a = p.parse_args()

    print("BIOCORE team-capacity model  --  kickoff 2027-01-09")
    print("weeks from kickoff to each 2027 milestone:")
    for k, d in MILESTONE.items():
        print("   %-9s %s   %5.2f weeks (%3d days)"
              % (k, d, weeks_between(KICKOFF, d), (d - KICKOFF).days))

    if a.deadline:
        w = weeks_between(KICKOFF, MILESTONE[a.deadline])
        m = model(a.students, a.hours_per_week, w)
        print_scenario("custom / " + a.deadline, m)
        ws = workstreams(m)
        print("  novel mechanisms -- lead-limited %.1f | hour-limited %.2f | shop-limited %.1f"
              % (ws["route_a_novel_mechanisms"], ws["route_b_novel_mechanisms"],
                 ws["route_c_novel_mechanisms"]))
        return

    w1 = weeks_between(KICKOFF, MILESTONE["week1"])
    w4 = weeks_between(KICKOFF, MILESTONE["week4"])
    scen = [
        ("LEAN     -> Week 1", model(15, 10, w1)),
        ("BASELINE -> Week 1", model(15, 15, w1)),
        ("STRETCH  -> Week 1", model(15, 22, w1)),
        ("BASELINE -> Week 4", model(15, 15, w4)),
    ]
    for name, m in scen:
        print_scenario(name, m)

    base = scen[1][1]
    ws = workstreams(base)
    print("")
    print("--- PARALLEL WORKSTREAMS, three independent routes (BASELINE -> Week 1) ---")
    print("  route A  unsupervised student leads : %.0f total, %.0f mechanical, "
          "minus drivetrain => %.0f novel mechanisms"
          % (ws["leads"], ws["mech_leads"], ws["route_a_novel_mechanisms"]))
    print("  route B  residual CAD+fab hours     : %.0f h / %d h per mechanism "
          "=> %.2f novel mechanisms"
          % (ws["residual_mech_h"], HOURS_PER_NOVEL_MECHANISM,
             ws["route_b_novel_mechanisms"]))
    print("  route C  single-machine shop queue  : => %.0f novel mechanisms"
          % ws["route_c_novel_mechanisms"])
    print("  BINDING (min of the three)          : %.2f"
          % min(ws["route_a_novel_mechanisms"], ws["route_b_novel_mechanisms"],
                ws["route_c_novel_mechanisms"]))

    print("")
    print("--- EFFECTIVE-HOUR BUDGET, BASELINE -> Week 1 ---")
    tot = base["effective_veq_h"]
    acc = 0.0
    for label, frac in ALLOCATION:
        h = tot * frac
        acc += h
        print("  %-42s %7.1f h   %5.1f%%" % (label, h, frac * 100))
    print("  %-42s %7.1f h" % ("TOTAL", acc))
    prog_supply = base["rows"][0][3] * 2     # 2 core programmers, coef 1.0
    prog_demand = tot * ALLOCATION[4][1]
    mech_supply = tot - prog_supply
    mech_demand = tot - prog_demand
    print("")
    print("  programmer supply  (2 core x %.1f h) : %7.1f h" % (base["rows"][0][3], prog_supply))
    print("  programmer demand                     : %7.1f h   -> %.0f%% utilisation"
          % (prog_demand, 100 * prog_demand / prog_supply))
    print("  non-programming supply                : %7.1f h" % mech_supply)
    print("  non-programming demand                : %7.1f h   -> shortfall %+.1f h"
          % (mech_demand, mech_demand - mech_supply))
    print("  SLACK IN THE WHOLE PLAN               : %+.1f h"
          % ((prog_supply - prog_demand) - (mech_demand - mech_supply)))

    print("")
    print("--- DELTA: what buys more hours? ---")
    d_sched = scen[2][1]["effective_veq_h"] - base["effective_veq_h"]
    d_event = scen[3][1]["effective_veq_h"] - base["effective_veq_h"]
    print("  +7 scheduled h/wk (15 -> 22), same Week 1 event : %+.0f veq-h" % d_sched)
    print("  same 15 h/wk, Week 1 event -> Week 4 event      : %+.0f veq-h" % d_event)

    if a.yaml:
        print("")
        print("--- calibrated constants ---")
        print(json.dumps({
            "effective_build_hours_week1": round(base["effective_veq_h"]),
            "effective_build_hours_week4": round(scen[3][1]["effective_veq_h"]),
            "effective_hours_multiplier": round(base["multiplier"], 3),
            "veq_hours_per_week": round(base["veq_per_week"], 1),
            "parallel_workstreams_max": 3,
            "novel_mechanisms_max": 2,
        }, indent=2))


if __name__ == "__main__":
    main()
