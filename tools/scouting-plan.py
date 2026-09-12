#!/usr/bin/env python3
"""
scouting-plan.py -- scout only what FMS does not already publish.

THE CORE INSIGHT
----------------
FIRST's FMS publishes a per-team scoring breakdown in the event rankings, and The Blue Alliance
mirrors it. Across 2023-2026 the shape is identical every season:

    Rank | Team | Ranking Score | Avg Match | Avg Auto | Avg <endgame> | Record | DQ | Played | Total RP
    2023 Avg Charge Station · 2024 Avg Stage (+Avg Coop) · 2025 Avg Barge (+Avg Coop) · 2026 Avg Tower (+Avg Auto Fuel)

So every team's AUTO average, ENDGAME average, MATCH average and win/loss record are FREE, for
every team at every event, with zero scouting labour.

A 15-student team that sends 6 scouts to record "how many game pieces did 254 score" is spending
its scarcest resource re-deriving a number FIRST already published. The scarce, un-published,
decision-relevant data is:

    reliability · variance · defense quality · driver skill · failure modes · what a team CANNOT do

This tool (a) reports what is free, (b) emits a scouting schema covering only the gaps, and
(c) builds a pick list that fuses free FMS data with your own gap-scouting.

USAGE
  python tools/scouting-plan.py free                 # what FMS published, 2023-2026 + BIOCORE forecast
  python tools/scouting-plan.py schema               # the complementary scouting schema (markdown)
  python tools/scouting-plan.py schema --json        # same, machine-readable
  python tools/scouting-plan.py picklist 2026 --event 2026tuis
  python tools/scouting-plan.py picklist 2026 --top 25

Pure stdlib. Reads research/predictive_tba/*.csv already in this repo.
"""
import sys, os, csv, io, json, argparse, collections, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBA = os.path.join(ROOT, "research", "predictive_tba")

# ---------------------------------------------------------------- the gap schema
# Only fields FMS/TBA does NOT publish. Each carries why it cannot be derived for free.
GAP_SCHEMA = {
    "match_scouting": [
        {"field": "breakdown", "type": "enum[none,partial,dead]",
         "why": "FMS publishes points scored, never whether the robot stopped working."},
        {"field": "breakdown_cause", "type": "text",
         "why": "Drivetrain vs mechanism vs electrical vs comms changes pick value entirely."},
        {"field": "defense_played_s", "type": "int_seconds",
         "why": "A low Avg Match may mean a great defender, not a bad scorer. Invisible in FMS data."},
        {"field": "defense_quality", "type": "scale_1_5",
         "why": "Not published in any form. The single most under-scouted dimension."},
        {"field": "defended_against", "type": "bool",
         "why": "Contextualises a low score. Without it you misread a good robot as weak."},
        {"field": "cycle_count", "type": "int",
         "why": "FMS gives the total, not the rate. Cycles + time gives consistency."},
        {"field": "intake_misses", "type": "int",
         "why": "Reliability of acquisition; predicts performance under defensive pressure."},
        {"field": "endgame_attempted", "type": "bool",
         "why": "FMS shows success only. Attempt-vs-success is the reliability signal."},
        {"field": "endgame_time_s", "type": "int_seconds",
         "why": "A 25-second climb costs cycles; see tools/cycle-model.py break-even."},
        {"field": "driver_skill", "type": "scale_1_5",
         "why": "Best predictor of playoff performance; entirely unpublished."},
        {"field": "starting_position", "type": "enum[left,center,right]",
         "why": "Auto compatibility for alliance planning. Never published."},
        {"field": "auto_path_note", "type": "text",
         "why": "Two teams with identical Avg Auto may have incompatible paths."},
        {"field": "notes", "type": "text", "why": "Catch-all for the thing no field anticipated."},
    ],
    "pit_scouting": [
        {"field": "drivetrain", "type": "enum[swerve,tank,mecanum,other]", "why": "Not published."},
        {"field": "weight_lb", "type": "float", "why": "Not published."},
        {"field": "mechanism_count", "type": "int", "why": "Complexity proxy for reliability."},
        {"field": "can_score_where", "type": "multi", "why": "Capability, vs. observed performance."},
        {"field": "climb_levels", "type": "multi", "why": "Capability ceiling vs typical."},
        {"field": "spare_parts_depth", "type": "scale_1_5",
         "why": "Predicts whether a breakdown ends their event. Strong playoff signal."},
        {"field": "programming_language", "type": "text", "why": "Auto-compat conversations."},
        {"field": "vision_used", "type": "bool", "why": "Predicts auto consistency."},
        {"field": "known_weaknesses", "type": "text",
         "why": "Teams will tell you. Nobody asks. Highest information-per-minute question in the pits."},
    ],
}

FREE_FIELDS = [
    ("Ranking Score", "the season's RP-based sort key"),
    ("Avg Match", "average match points contributed"),
    ("Avg Auto", "average autonomous points  (2026 split out as 'Avg Auto Fuel')"),
    ("Avg <endgame>", "2023 Charge Station · 2024 Stage · 2025 Barge · 2026 Tower"),
    ("Avg Coop", "when the season has a coopertition mechanic (2024, 2025)"),
    ("Record (W-L-T)", "win/loss/tie"),
    ("DQ", "disqualification count -- a rules-risk signal, free"),
    ("Played", "matches played; denominator for every rate"),
    ("Total Ranking Points", "cumulative RP"),
]


def load_events(year):
    p = os.path.join(TBA, f"tba_events_{year}.csv")
    if not os.path.exists(p):
        return []
    return list(csv.DictReader(io.open(p, encoding="utf-8", errors="replace")))


def cmd_free():
    print("\n=== What FMS/TBA publishes for FREE (no scouting labour) ===\n")
    for y in (2023, 2024, 2025, 2026):
        evs = load_events(y)
        if not evs:
            continue
        c = collections.Counter(e["rank_cols"] for e in evs)
        top, n = c.most_common(1)[0]
        cols = [x for x in top.split("|") if x not in ("Rank", "Team")]
        print(f"  {y}  ({n}/{len(evs)} events identical)")
        print(f"       {' · '.join(cols)}")
    print("\n=== The invariant, 4/4 seasons  [H] ===\n")
    for f, why in FREE_FIELDS:
        print(f"  {f:<22} {why}")
    print("\n=== BIOCORE forecast  [S, from a 4/4 pattern] ===\n")
    print("  Rank | Team | Ranking Score | Avg Match | Avg Auto |")
    print("  Avg <BIOCORE endgame structure> | Record (W-L-T) | DQ | Played | Total RP")
    print("\n  On kickoff day, name the endgame structure from the manual and you already know")
    print("  the shape of the free data. Design the scouting app around the GAPS, not around this.")
    print("\n  Confirm at week 1: python tools/scouting-plan.py free   (after refreshing TBA data)\n")


def cmd_schema(as_json=False):
    if as_json:
        print(json.dumps(GAP_SCHEMA, indent=2))
        return
    print("\n=== Gap scouting schema -- collect ONLY what FMS does not publish ===\n")
    for section, fields in GAP_SCHEMA.items():
        print(f"## {section}  ({len(fields)} fields)\n")
        print(f"{'field':<22}{'type':<26}why it cannot be had for free")
        print("-" * 108)
        for f in fields:
            print(f"{f['field']:<22}{f['type']:<26}{f['why']}")
        print()
    n = sum(len(v) for v in GAP_SCHEMA.values())
    print(f"{n} fields total. A 6-scout rotation can capture the match set comfortably;")
    print("pit scouting is one person for one morning.\n")
    print("Deliberately NOT collected: anything in `scouting-plan.py free`. Do not pay students")
    print("to re-derive published numbers -- spend those hours on defense and reliability instead.\n")


def cmd_picklist(year, event=None, top=25):
    p = os.path.join(TBA, f"tba_rankings_{year}.csv")
    if not os.path.exists(p):
        print(f"No rankings file: {p}")
        return 1
    rows = list(csv.DictReader(io.open(p, encoding="utf-8", errors="replace")))
    if event:
        rows = [r for r in rows if r["event"] == event]
        if not rows:
            print(f"No rows for event {event}.")
            return 1
    # team -> {col_name: value}
    teams = collections.defaultdict(dict)
    for r in rows:
        try:
            teams[(r["event"], r["team"])][r["col_name"]] = float(r["value"])
        except (ValueError, KeyError):
            pass
    # which component columns exist this season
    cols = collections.Counter()
    for v in teams.values():
        cols.update(v.keys())
    # "Avg Match" gets its own column, so keep it out of the component list
    comp = [c for c, _ in cols.most_common() if c.startswith("Avg") and c != "Avg Match"]
    scope = event or f"all {year} events"
    print(f"\n=== Free-data pick-list inputs: {scope} ===")
    print(f"    {len(teams)} team-events · components available: {', '.join(comp)}\n")

    recs = []
    for (ev, tm), v in teams.items():
        if "Avg Match" not in v:
            continue
        rec = {"event": ev, "team": tm, "match": v.get("Avg Match", 0.0)}
        for c in comp:
            rec[c] = v.get(c, 0.0)
        rec["played"] = v.get("Played", 0.0)
        rec["dq"] = v.get("DQ", 0.0)
        recs.append(rec)
    if not recs:
        print("No usable rows.")
        return 1
    recs.sort(key=lambda r: -r["match"])

    hdr = f"{'team':>7}{'event':>12}{'AvgMatch':>10}"
    for c in comp[:3]:
        hdr += f"{c[:11]:>12}"
    hdr += f"{'played':>8}{'DQ':>5}"
    print(hdr)
    print("-" * len(hdr))
    for r in recs[:top]:
        line = f"{r['team']:>7}{r['event']:>12}{r['match']:>10.1f}"
        for c in comp[:3]:
            line += f"{r.get(c, 0.0):>12.1f}"
        line += f"{r['played']:>8.0f}{r['dq']:>5.0f}"
        print(line)

    ms = [r["match"] for r in recs]
    print(f"\n  Avg Match across {len(recs)} team-events: mean {statistics.mean(ms):.1f}, "
          f"median {statistics.median(ms):.1f}, max {max(ms):.1f}")
    dqs = [r for r in recs if r["dq"] > 0]
    print(f"  Teams with >=1 DQ: {len(dqs)} ({100*len(dqs)/len(recs):.1f}%) -- free rules-risk signal.")
    print("\n  THIS IS ONLY HALF A PICK LIST. Rank order here reflects scoring, not reliability,")
    print("  defense, or driver skill. Fuse with your gap-scouting data before drafting:")
    print("    python tools/scouting-plan.py schema\n")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("free")
    s = sub.add_parser("schema"); s.add_argument("--json", action="store_true")
    p = sub.add_parser("picklist"); p.add_argument("year", type=int)
    p.add_argument("--event", default=None); p.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    if a.cmd == "free":
        cmd_free()
    elif a.cmd == "schema":
        cmd_schema(a.json)
    else:
        return cmd_picklist(a.year, a.event, a.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
