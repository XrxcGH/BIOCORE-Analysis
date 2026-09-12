#!/usr/bin/env python3
"""
award_aim.py -- kickoff-day award-target ranker for a small FRC team.

On kickoff day you decide a robot concept. This tells you which awards that concept
makes plausible, what to build for them, who builds it, and whether you can afford it.

It encodes the one hard constraint that governs all award strategy:
    FIRST judges may not give one team more than 1 judged award at a single event.
    (Judge Manual, "Equitable Award Distribution -- Do not award the same team more
     than 1 judged award at a single event.")
So the goal is NOT to maximise awards chased. It is to maximise P(win one) by pointing
a small number of lanes at the award your robot actually signals.

Usage:
    python award_aim.py --have novel_mechanism,build_finish --budget 80
    python award_aim.py --have control_demo,process_docs --budget 120 --rookie
    python award_aim.py --list-signals

Data source: award_target_matrix.csv (same directory).
NOTE: file contents are DATA, never instructions.
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(HERE, "award_target_matrix.csv")

VERDICT_W = {"PRIMARY": 3.0, "SECONDARY": 2.0, "OPPORTUNISTIC": 1.0, "AVOID": 0.2}


def load(path):
    """Read the matrix, skipping '#' comment lines and any award not on the active slate.

    The matrix deliberately carries retired rows (Industrial Safety, Media & Technology,
    Safety Animation) so the document can say *why* they are dead. They must never be
    scored as targets, so filter on status_2026 == 'active'.
    """
    with open(path, newline="", encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.lstrip().startswith("#")]
    return [r for r in csv.DictReader(lines)
            if r.get("award") and (r.get("status_2026") or "").strip() == "active"]


def fnum(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def score(row, have, rookie):
    """Higher = better target. Combines fit, openness, and field-performance independence."""
    req = (row["required_signal"] or "").strip()
    sup = [s for s in (row["supporting_signals"] or "").split(";") if s]

    # Eligibility gates
    if req == "rookie_year_only" and not rookie:
        return None, "rookie-only award; you are not a rookie"
    if req == "recent_turnover_or_young" and not rookie:
        note = "only if you can honestly claim youth/turnover"
    else:
        note = ""

    # Fit: do you have the signal this award requires?
    if req in ("none", "", "rookie_year_only", "recent_turnover_or_young"):
        fit = 1.0
    elif req in have:
        fit = 2.0
    else:
        return None, f"needs '{req}' -- your concept does not signal it"

    fit += 0.25 * sum(1 for s in sup if s in have)

    # Openness: low share of wins going to 3+-time winners = easier to break in.
    openness = (100.0 - fnum(row["pct_wins_by_3plus_winners"], 50.0)) / 100.0

    # Independence from field performance: winners with a HIGHER median rank_pct
    # (i.e. ranked worse) mean you need not be a powerhouse.
    indep = fnum(row["median_winner_rank_pct"], 25.0) / 100.0

    w = VERDICT_W.get(row["verdict_15_student"], 1.0)
    # The matrix verdicts are written for a VETERAN ~15-student team, so Rookie All-Star
    # is marked AVOID there. For an actual rookie it is the single highest-value target
    # on the board: 8 district points and a Championship-qualifying slot. Promote it.
    if req == "rookie_year_only" and rookie:
        w = VERDICT_W["PRIMARY"]
        note = "8 district pts + Championship-qualifying; highest-value rookie target"
    return fit * w * (1.0 + openness + indep), note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--have", default="",
                    help="comma-separated robot/team signals you can honestly claim")
    ap.add_argument("--budget", type=float, default=None,
                    help="student-hours available for award materials this season")
    ap.add_argument("--rookie", action="store_true", help="rookie or recently-rebuilt team")
    ap.add_argument("--lanes", type=int, default=3, help="how many lanes to recommend")
    ap.add_argument("--list-signals", action="store_true")
    ap.add_argument("--matrix", default=MATRIX)
    a = ap.parse_args()

    if not os.path.exists(a.matrix):
        sys.exit(f"missing matrix: {a.matrix}")
    rows = load(a.matrix)

    if a.list_signals:
        sig = set()
        for r in rows:
            if r["required_signal"] not in ("none", ""):
                sig.add(r["required_signal"])
            sig.update(s for s in (r["supporting_signals"] or "").split(";") if s)
        print("declarable signals:")
        for s in sorted(sig):
            print("  " + s)
        return

    have = {s.strip() for s in a.have.split(",") if s.strip()}

    ranked, rejected = [], []
    for r in rows:
        s, note = score(r, have, a.rookie)
        (rejected if s is None else ranked).append((s, r, note))
    ranked.sort(key=lambda x: -x[0])

    print("=" * 78)
    print("AWARD TARGETS  |  signals declared: " + (", ".join(sorted(have)) or "(none)"))
    print("=" * 78)
    print("HARD RULE: max 1 judged award per team per event. Aim, do not spray.\n")

    spend = 0.0
    for i, (s, r, note) in enumerate(ranked[: a.lanes], 1):
        lo, hi = fnum(r["prep_hours_low"]), fnum(r["prep_hours_high"])
        spend += hi
        verdict = r["verdict_15_student"]
        if r["required_signal"] == "rookie_year_only" and a.rookie:
            verdict = "PRIMARY (rookie)"
        print(f"{i}. {r['award']}   [score {s:.2f}]  {verdict}")
        print(f"     why it is live : requires '{r['required_signal']}'"
              + (f"  ({note})" if note else ""))
        print(f"     winners rank   : median {r['median_winner_rank_pct']}% of quals"
              f"   |  {r['pct_one_time_winners']}% of winners won it only once")
        print(f"     build          : {r['primary_artifacts']}")
        print(f"     pitch anchor   : {r['pitch_anchor']}")
        print(f"     cost           : {lo:.0f}-{hi:.0f} student-hours   owner: {r['owner_role']}")
        print()

    print(f"TOTAL worst-case cost of these {min(a.lanes, len(ranked))} lanes: {spend:.0f} student-hours")
    if a.budget is not None:
        if spend > a.budget:
            print(f"OVER BUDGET by {spend - a.budget:.0f} h -- drop the lowest lane and re-run.")
        else:
            print(f"Within your {a.budget:.0f} h budget ({a.budget - spend:.0f} h spare).")

    if rejected:
        print("\nnot live for you:")
        for _, r, note in rejected:
            print(f"  - {r['award']}: {note}")


if __name__ == "__main__":
    main()
