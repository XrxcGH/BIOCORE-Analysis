#!/usr/bin/env python3
"""
award_target_rank.py -- rank the robot-adjacent FRC judged awards by expected value
for THIS team, given (a) an honest projection of where the robot will finish in
qualification and (b) which design signals the robot will actually carry.

No third-party dependencies (no pyyaml, no pandas). Python 3.8+.

INPUTS
  reference/awards/award_band_shares.csv     empirical P(award | winner's qual-rank band),
                                             2022-2026 TBA data, 5 seasons, 1,025 ranked events
  reference/awards/award_accessibility.csv   per-award accessibility + district/regional points
  reference/awards/team_profile.txt          THE ONLY FILE YOU EDIT. key: value, one per line.

OUTPUT
  Ranked award targets on stdout, with the gate that is failing for anything ruled out,
  the artifacts to build, the owner, and the student-hour cost.

USAGE
  python tools/award_target_rank.py
  python tools/award_target_rank.py --profile reference/awards/team_profile.txt --band mid50_75
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
AW = os.path.join(ROOT, "reference", "awards")

BANDS = ["top8", "top25pct", "mid25_50", "mid50_75", "bottom25pct"]

# --- The award model -----------------------------------------------------------------
# gates   : ALL must be true in the profile or the award is not a live target.
# boosts  : each true signal adds to fit; fit = 0.5 + 0.5 * (boosts_met / boosts_total).
# hours   : [S] estimated student-hours to prepare the judged-award materials only
#           (NOT the hours to build the robot feature itself).
# owner   : who on a 15-student team does it.
# See reference/awards/01_AWARD_WINNING_PATTERNS.md for the sourcing of every line.
MODEL = {
    "Autonomous Award": dict(
        gates=["auto_scores_multiple_actions", "auto_uses_closed_loop_sensing",
               "auto_reliability_logged"],
        boosts=["auto_runs_in_teleop_too", "auto_selector_ui", "auto_sim_or_replay"],
        hours=25, owner="programmer + 1 scout (reliability log)",
        artifacts="auto reliability table (attempt/success per match), sensor block diagram, "
                  "auto path overlay, laptop replay/sim loop"),
    "Creativity Award": dict(
        gates=["one_mechanism_unlike_the_field", "conception_traceable_to_a_decision"],
        boosts=["risk_mitigation_documented", "mechanism_works_on_field",
                "prototype_photos_exist"],
        hours=18, owner="mechanical lead + 1 pit rep",
        artifacts="one-pager on THE mechanism, prototype-to-final photo strip, "
                  "the rejected alternative on the table, 30-second bench demo"),
    "Excellence in Engineering Award": dict(
        gates=["design_process_documented", "robot_functional_on_field"],
        boosts=["problem_statement_written", "trade_study_with_numbers",
                "subsystems_integrate_cleanly", "build_blog_public"],
        hours=45, owner="2 documentation students + mechanical lead",
        artifacts="tabbed technical binder (problem -> requirement -> trade study -> "
                  "CAD -> test -> result), public build blog, CAD exploded views"),
    "Industrial Design Award": dict(
        gates=["whole_robot_visually_coherent", "serviceable_in_3_minutes"],
        boosts=["wire_management_planned", "consistent_material_finish",
                "ergonomics_considered", "manufacturing_repeatable"],
        hours=20, owner="fabrication lead + 1 media student",
        artifacts="CAD render vs. real-robot photo pair, wire-routing diagram, "
                  "3-minute service demo, finish/branding spec sheet"),
    "Innovation in Control Award": dict(
        gates=["novel_control_feature", "control_feature_explainable_by_a_student",
               "control_data_exists"],
        boosts=["custom_operator_interface", "fast_and_accurate_motion",
                "control_writeup_published", "sensor_fusion_or_estimator"],
        hours=30, owner="programmer + electrical student",
        artifacts="one-sheet control summary judges can carry, step-response / "
                  "error plot, live dashboard on a laptop, control block diagram",),
    "Quality Award": dict(
        gates=["written_quality_plan", "low_field_failure_rate"],
        boosts=["designed_in_redundancy", "spares_for_every_wear_part",
                "torque_marks_and_loctite", "preventive_maintenance_checklist"],
        hours=15, owner="pit crew chief + 1 student",
        artifacts="maintenance/failure log, spares board, PM checklist on the pit wall, "
                  "cutaway of one joint showing fastener strategy"),
    "Imagery Award": dict(
        gates=["team_theme_exists", "theme_on_robot_and_pit_and_uniform"],
        boosts=["theme_has_an_origin_story", "pit_is_photogenic",
                "robot_paint_or_wrap_is_deliberate"],
        hours=25, owner="media student + 1 helper",
        artifacts="theme origin card, matched robot/pit/uniform palette, "
                  "photo wall, mascot"),
    "Judges' Award": dict(
        gates=["one_singular_story_no_other_award_covers"],
        boosts=["story_is_verifiable", "every_student_can_tell_it"],
        hours=6, owner="whole team (it is a by-product, not a project)",
        artifacts="none dedicated -- this is the residual award; it lands on teams "
                  "judges remember for one specific thing"),
    "Team Spirit Award": dict(
        gates=["visible_sustained_enthusiasm"],
        boosts=["spirit_exists_outside_competition", "team_acts_as_a_unit"],
        hours=10, owner="spirit lead",
        artifacts="chants, matching kit, stands presence"),
    "Gracious Professionalism Award": dict(
        gates=["documented_help_given_to_other_teams"],
        boosts=["gp_story_at_this_event", "gp_story_year_round"],
        hours=8, owner="whole team",
        artifacts="log of parts/help lent, named beneficiary teams"),
    "Team Sustainability Award": dict(
        gates=["people_prosperity_planet_plan_written"],
        boosts=["budget_tracked", "recruitment_and_succession_plan", "risk_register"],
        hours=30, owner="business lead",
        artifacts="budget + risk register + succession plan, 3-year trend charts"),
    "Rising All-Star Award": dict(
        gates=["team_had_a_new_beginning"],
        boosts=["growth_is_measurable", "role_model_for_young_teams"],
        hours=12, owner="team captain",
        artifacts="before/after numbers on membership, facility, process"),
    "Rookie All-Star Award": dict(
        gates=["team_is_a_rookie_this_season"],
        boosts=["built_a_robot_appropriate_to_the_game", "sponsor_partnership_real"],
        hours=20, owner="team captain",
        artifacts="rookie story + partnership evidence + a robot that plays the game"),
}


def load_csv(path, key):
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row[key]] = row
    return out


def load_profile(path):
    """key: value, one per line. '#' comments. Values true/false/yes/no/1/0 or free text."""
    prof = {}
    if not os.path.exists(path):
        return prof
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            v = v.strip().lower()
            prof[k.strip()] = v in ("true", "yes", "y", "1") if v in (
                "true", "yes", "y", "1", "false", "no", "n", "0") else v.strip()
    return prof


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=os.path.join(AW, "team_profile.txt"))
    ap.add_argument("--band", default=None,
                    help="override projected_qual_band: " + "|".join(BANDS))
    ap.add_argument("--event-type", default=None, choices=["district", "regional"])
    args = ap.parse_args()

    prof = load_profile(args.profile)
    band = args.band or prof.get("projected_qual_band", "mid50_75")
    if band not in BANDS:
        sys.exit(f"projected_qual_band must be one of {BANDS}, got {band!r}")
    etype = args.event_type or prof.get("event_type", "district")

    shares = load_csv(os.path.join(AW, "award_band_shares.csv"), "award")
    access = load_csv(os.path.join(AW, "award_accessibility.csv"), "award")

    rows = []
    for name, m in MODEL.items():
        if name not in shares:
            continue
        share = float(shares[name]["share_pct_" + band])
        n_band = int(shares[name]["n_" + band])
        missing = [g for g in m["gates"] if not prof.get(g, False)]
        met = sum(1 for b in m["boosts"] if prof.get(b, False))
        fit = 0.0 if missing else (0.5 + 0.5 * met / max(1, len(m["boosts"])))
        pts = int(access[name]["district_points" if etype == "district"
                              else "regional_points"])
        score = share * fit
        rows.append(dict(award=name, share=share, n=n_band, fit=fit, score=score,
                         pts=pts, hours=m["hours"], owner=m["owner"],
                         artifacts=m["artifacts"], missing=missing,
                         btm=float(access[name]["pct_winner_bottom_half"]),
                         top8=float(access[name]["pct_winner_qual_top8"])))

    live = sorted([r for r in rows if r["score"] > 0], key=lambda r: -r["score"])
    dead = sorted([r for r in rows if r["score"] == 0], key=lambda r: -r["share"])

    print(f"\nPROJECTED QUAL BAND: {band}    EVENT TYPE: {etype}"
          f"    PROFILE: {os.path.basename(args.profile)}")
    print("Empirical base: 23,162 TBA award rows, 1,025 ranked events, seasons 2022-2026.")
    print("HARD CONSTRAINT: judges may not give one team more than 1 judged award at one "
          "event (2026 Judge Manual p.29). Pick ONE machine lane and ONE team lane.\n")

    hdr = (f"{'#':>2}  {'award':<34}{'score':>7}{'band%':>7}{'fit':>6}"
           f"{'pts':>5}{'hrs':>5}{'btmHalf%':>9}  owner")
    print(hdr); print("-" * (len(hdr) + 20))
    for i, r in enumerate(live, 1):
        print(f"{i:>2}  {r['award']:<34}{r['score']:>7.2f}{r['share']:>7.2f}"
              f"{r['fit']:>6.2f}{r['pts']:>5}{r['hours']:>5}{r['btm']:>9.1f}  {r['owner']}")
    # Lane assignment: machine judges and team judges are different judge pairs
    # (Split Judging / Split Awards models), so you get one nomination shot in each.
    MACHINE = {"Autonomous Award", "Creativity Award", "Excellence in Engineering Award",
               "Industrial Design Award", "Innovation in Control Award", "Quality Award"}
    mach = [r for r in live if r["award"] in MACHINE]
    team = [r for r in live if r["award"] not in MACHINE and r["award"] != "Judges' Award"]
    print("\nRECOMMENDED LANE ASSIGNMENT  (machine judges and team judges are separate "
          "pairs -- you get one nomination shot in each lane):")
    print(f"  MACHINE lane : {mach[0]['award'] if mach else 'NONE -- no machine gate passes yet'}"
          + (f"   ({mach[0]['hours']} h, owner: {mach[0]['owner']})" if mach else ""))
    print(f"  TEAM lane    : {team[0]['award'] if team else 'NONE -- no team gate passes yet'}"
          + (f"   ({team[0]['hours']} h, owner: {team[0]['owner']})" if team else ""))
    print("  BACKUP       : " + (mach[1]["award"] if len(mach) > 1 else "-")
          + "  (same artifacts, different framing -- costs ~0 extra hours)")
    print("  Judges' Award is NOT a lane. It is the residual. Do not spend hours on it.")

    picks = ([mach[0]] if mach else []) + ([team[0]] if team else []) \
        + ([mach[1]] if len(mach) > 1 else [])
    tot = sum(r["hours"] for r in picks)
    print(f"\nThat lane set costs {tot} student-hours of judging prep "
          f"({tot/15:.1f} h per student on a 15-student team).")
    print("\nARTIFACTS TO BUILD:")
    for r in picks:
        print(f"  - {r['award']}: {r['artifacts']}")
    if dead:
        print("\nNOT LIVE TARGETS -- failing gate(s):")
        for r in dead:
            print(f"  - {r['award']:<34} needs: {', '.join(r['missing'])}")
    print()


if __name__ == "__main__":
    main()
