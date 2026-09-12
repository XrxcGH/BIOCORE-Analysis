#!/usr/bin/env python3
"""
award_winner_forensics.py -- answer "what did teams that ACTUALLY won this award look like?"

Consumes the 5-season TBA award corpus already scraped by tools/tba_award_scrape.py
(research/awards_tba/tba_awards_2022..2026.csv) plus the event/alliance corpus from
tools/tba_predictive_scrape.py, and emits per-award winner forensics:

  - qualification-rank percentile of the winner (median / quartiles / share top-8)
  - co-occurrence with a FIELD award (Winners / Finalists) at the SAME event
  - repeat concentration: what share of wins go to teams that won that award >1x in 5 yrs
  - VIRGIN RATE: share of wins by a team with NO prior judged award anywhere in the window
    (this is the single most useful number for a first-time small team)
  - team-number cohort of winners (proxy for team age/veteran status)
  - cross-award migration: given a team won award X once, what else did they win?

Output:
  research/awards_tba/award_winner_forensics.csv
  research/awards_tba/award_migration_matrix.csv
  stdout report

Usage: python tools/award_winner_forensics.py
"""
import csv
import glob
import os
import re
import statistics
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "research", "awards_tba")
PRED = os.path.join(HERE, "..", "research", "predictive_tba")

RENAMES = [
    (r"^district championship |^district |^regional |^championship division |^championship ", ""),
    (r"\s+sponsored by .*$", ""),
    (r"\s+in honor of .*$", ""),
]
FOLD = {
    "chairman's award": "FIRST Impact Award",
    "first impact award": "FIRST Impact Award",
    "rookie inspiration award": "Rising All-Star Award",
    "rising all-star award": "Rising All-Star Award",
    "rookie all star award": "Rookie All-Star Award",
    "rookie all-star award": "Rookie All-Star Award",
    "industrial design award": "Industrial Design Award",
    "quality award": "Quality Award",
    "creativity award": "Creativity Award",
    "excellence in engineering award": "Excellence in Engineering Award",
    "innovation in control award": "Innovation in Control Award",
    "autonomous award": "Autonomous Award",
    "imagery award": "Imagery Award",
    "judges' award": "Judges' Award",
    "judges award": "Judges' Award",
    "team spirit award": "Team Spirit Award",
    "team sustainability award": "Team Sustainability Award",
    "gracious professionalism award": "Gracious Professionalism Award",
    "engineering inspiration award": "Engineering Inspiration Award",
    "safety award": "Safety Award",
    "industrial safety award": "Safety Award",
    "media and technology innovation award": "Media & Technology Award",
    "media and technology award": "Media & Technology Award",
    "innovation award": "Innovation Award",
}
# Awards that are field-earned, not judged.
FIELD = {"event winner", "event finalist", "winners", "finalists",
         "division winner", "division finalist", "winner", "finalist"}

MACHINE = ["Industrial Design Award", "Quality Award", "Excellence in Engineering Award",
           "Creativity Award", "Innovation in Control Award", "Autonomous Award"]
TEAMISH = ["Imagery Award", "Judges' Award", "Rookie All-Star Award", "Rising All-Star Award",
           "Team Spirit Award", "Team Sustainability Award", "Gracious Professionalism Award",
           "Engineering Inspiration Award", "FIRST Impact Award", "Safety Award",
           "Media & Technology Award", "Innovation Award"]
TRACKED = MACHINE + TEAMISH


def canon(name: str) -> str:
    n = name.strip()
    low = n.lower()
    for pat, rep in RENAMES:
        low = re.sub(pat, rep, low)
    low = low.strip()
    if low in FOLD:
        return FOLD[low]
    if low in FIELD:
        return "__FIELD__"
    return n.strip()


def load():
    rows = []
    for path in sorted(glob.glob(os.path.join(DATA, "tba_awards_*.csv"))):
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                try:
                    team = int(r["team"])
                except (ValueError, KeyError):
                    continue
                rank_pct = None
                try:
                    rank_pct = float(r["rank_pct"]) if r.get("rank_pct") else None
                except ValueError:
                    pass
                rows.append({
                    "year": int(r["year"]), "event": r["event"],
                    "award_raw": r["award"], "award": canon(r["award"]),
                    "team": team, "rank_pct": rank_pct,
                })
    return rows


def q(xs, p):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main():
    rows = load()
    print(f"loaded {len(rows)} award rows, {len(set(r['year'] for r in rows))} seasons")

    # index -----------------------------------------------------------------
    by_award = defaultdict(list)
    field_at = set()                       # (year,event,team) won a field award
    judged_by_team_year = defaultdict(set)  # team -> {(year, award)}
    judged_events = defaultdict(set)        # (year,event) -> set(award)
    for r in rows:
        if r["award"] == "__FIELD__":
            field_at.add((r["year"], r["event"], r["team"]))
            continue
        by_award[r["award"]].append(r)
        judged_by_team_year[r["team"]].add((r["year"], r["event"], r["award"]))
        judged_events[(r["year"], r["event"])].add(r["award"])

    # chronological order for "virgin" detection
    year_order = sorted(set(r["year"] for r in rows))
    first_judged_year = {}
    for team, s in judged_by_team_year.items():
        first_judged_year[team] = min(y for (y, _e, _a) in s)

    out = []
    for aw in TRACKED:
        recs = by_award.get(aw, [])
        if not recs:
            continue
        ranks = [r["rank_pct"] for r in recs if r["rank_pct"] is not None]
        n = len(recs)
        # repeat concentration
        c = Counter(r["team"] for r in recs)
        wins_by_repeaters = sum(v for v in c.values() if v > 1)
        top10 = sum(v for _t, v in c.most_common(10))
        # co-occurrence with field award at the same event
        cofield = sum(1 for r in recs if (r["year"], r["event"], r["team"]) in field_at)
        # virgin rate: this award is the team's FIRST judged award in the 5-yr window
        virgin = 0
        for r in recs:
            prior = [ (y,e,a) for (y,e,a) in judged_by_team_year[r["team"]]
                      if y < r["year"] ]
            if not prior:
                virgin += 1
        teamnums = sorted(r["team"] for r in recs)
        out.append({
            "award": aw,
            "n_wins_2022_2026": n,
            "unique_teams": len(c),
            "median_rank_pct": round(statistics.median(ranks), 1) if ranks else "",
            "p25_rank_pct": round(q(ranks, .25), 1) if ranks else "",
            "p75_rank_pct": round(q(ranks, .75), 1) if ranks else "",
            "pct_winner_top25pct_qual": round(100 * sum(1 for x in ranks if x <= 25) / len(ranks), 1) if ranks else "",
            "pct_winner_bottom_half_qual": round(100 * sum(1 for x in ranks if x > 50) / len(ranks), 1) if ranks else "",
            "pct_also_won_field_award_same_event": round(100 * cofield / n, 1),
            "pct_wins_by_repeat_winners": round(100 * wins_by_repeaters / n, 1),
            "pct_wins_by_top10_teams": round(100 * top10 / n, 1),
            "pct_wins_by_first_time_judged_team": round(100 * virgin / n, 1),
            "median_winner_team_number": int(statistics.median(teamnums)),
            "p25_winner_team_number": int(q(teamnums, .25)),
            "p75_winner_team_number": int(q(teamnums, .75)),
        })

    outp = os.path.join(DATA, "award_winner_forensics.csv")
    with open(outp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {outp}")

    hdr = f"{'award':34s} {'n':>5s} {'medRk%':>7s} {'top25%':>7s} {'bot50%':>7s} {'+field':>7s} {'repeat':>7s} {'1sttime':>8s} {'medTeam#':>9s}"
    print("\n" + hdr)
    print("-" * len(hdr))
    for r in out:
        print(f"{r['award']:34s} {r['n_wins_2022_2026']:5d} {r['median_rank_pct']:>7} "
              f"{r['pct_winner_top25pct_qual']:>7} {r['pct_winner_bottom_half_qual']:>7} "
              f"{r['pct_also_won_field_award_same_event']:>7} {r['pct_wins_by_repeat_winners']:>7} "
              f"{r['pct_wins_by_first_time_judged_team']:>8} {r['median_winner_team_number']:>9d}")

    # --- cross-award migration matrix ------------------------------------
    # For teams that ever won award X, what fraction ALSO ever won award Y (any event/year)?
    teams_by_award = {a: set(r["team"] for r in by_award.get(a, [])) for a in TRACKED}
    mpath = os.path.join(DATA, "award_migration_matrix.csv")
    with open(mpath, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["won_X"] + ["also_won_" + a for a in MACHINE] + ["n_teams_X"])
        for x in TRACKED:
            tx = teams_by_award[x]
            if not tx:
                continue
            row = [x]
            for y in MACHINE:
                if y == x:
                    row.append("")
                    continue
                row.append(round(100 * len(tx & teams_by_award[y]) / len(tx), 1))
            row.append(len(tx))
            w.writerow(row)
    print(f"\nwrote {mpath}")

    # --- how many machine awards does a machine-award-winning team collect? ----
    print("\nmachine-award breadth (2022-2026, teams that won >=1 machine award):")
    breadth = Counter()
    allmach = set().union(*[teams_by_award[a] for a in MACHINE])
    for t in allmach:
        k = sum(1 for a in MACHINE if t in teams_by_award[a])
        breadth[k] += 1
    tot = sum(breadth.values())
    for k in sorted(breadth):
        print(f"  won {k} distinct machine award type(s): {breadth[k]:5d} teams ({100*breadth[k]/tot:.1f}%)")

    # --- event slate reality check ---------------------------------------
    nev = len(judged_events)
    print(f"\njudged-award events in corpus: {nev}")
    for a in MACHINE:
        k = sum(1 for s in judged_events.values() if a in s)
        print(f"  {a:36s} offered at {k:4d} events ({100*k/nev:.1f}%)")


if __name__ == "__main__":
    main()
