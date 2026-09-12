#!/usr/bin/env python3
"""
award_patterns.py -- normalize 5 seasons of scraped TBA award rows and answer the two
questions a small team actually needs answered:

  Q1  Is this award reachable by a robot that is NOT a top-8 qualifier?
      -> distribution of the winner's qualification-rank percentile at that event.
  Q2  How contested is it / is it even given at every event?
      -> award-per-event coverage rate.

Input : research/awards_tba/tba_awards_*.csv  (from tools/tba_award_scrape.py)
Output: research/awards_tba/award_rank_profile.csv  + stdout report
"""
import csv
import glob
import os
import re
import statistics
import sys
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "research", "awards_tba")

# --- canonical names ----------------------------------------------------------------
# Sponsors churn every year or two; strip them and fold historical renames together.
RENAMES = [
    (r"^district |^regional |^district championship |^championship division |^championship ", ""),
    (r"\s+sponsored by .*$", ""),
    (r"\s+in honor of .*$", ""),
]
FOLD = {
    "chairman's award": "FIRST Impact Award",
    "first impact award": "FIRST Impact Award",
    "rookie inspiration award": "Rising All-Star Award",   # renamed for 2025
    "rising all-star award": "Rising All-Star Award",
    "rookie all star award": "Rookie All-Star Award",
    "rookie all-star award": "Rookie All-Star Award",
    "first dean's list finalist award": "FIRST Leadership Award Finalist",
    "first leadership award finalist": "FIRST Leadership Award Finalist",
    "dean's list semi-finalist": "FIRST Leadership Award Semi-Finalist",
    "first leadership award semi-finalist": "FIRST Leadership Award Semi-Finalist",
    "judge's award": "Judges' Award",
    "judges award": "Judges' Award",
    "judges' award": "Judges' Award",
}
# Awards decided by match play, not judges -- used as the "was this a top robot" signal.
FIELD = re.compile(
    r"winner|finalist|wildcard|highest rookie seed", re.I)
# The robot-adjacent judged awards this document is about.
MACHINE = {"Autonomous Award", "Creativity Award", "Excellence in Engineering Award",
           "Industrial Design Award", "Innovation in Control Award", "Quality Award"}
TEAM_ADJ = {"Imagery Award", "Judges' Award", "Rookie All-Star Award",
            "Rising All-Star Award", "Team Spirit Award", "Gracious Professionalism Award",
            "Team Sustainability Award", "Engineering Inspiration Award",
            "FIRST Impact Award"}


def canon(name: str) -> str:
    n = name.strip()
    low = n.lower()
    for pat, rep in RENAMES:
        low = re.sub(pat, rep, low).strip()
    if low in FOLD:
        return FOLD[low]
    # title-case fallback, preserving FIRST and lowercase function words
    small = {"in", "of", "the", "by", "for", "and", "on"}
    words = low.split()
    out = " ".join(
        w if w.isupper() else (w if (i and w in small) else w.capitalize())
        for i, w in enumerate(words))
    out = out.replace("First ", "FIRST ")
    return out


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "tba_awards_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            r["canon"] = canon(r["award"])
            r["is_field"] = bool(FIELD.search(r["award"]))
            rows.append(r)
    return rows


def pct(r):
    try:
        return float(r["rank_pct"])
    except (ValueError, KeyError):
        return None


def main():
    rows = load()
    print(f"loaded {len(rows)} award rows, "
          f"{len(set(r['event'] for r in rows))} events, "
          f"{len(set(r['year'] for r in rows))} seasons\n")

    # --- which events are "real" competition events (have rankings) ---
    events = set(r["event"] for r in rows if r["n_teams"])
    per_year_events = Counter(e[:4] for e in events)

    # --- Q2 coverage: what fraction of events gave this award? ---
    gave = defaultdict(set)
    for r in rows:
        if r["event"] in events:
            gave[r["canon"]].add(r["event"])

    # --- Q1 rank percentile of the winning team ---
    prof = defaultdict(list)
    top8 = defaultdict(lambda: [0, 0])       # canon -> [in_top8, total]
    for r in rows:
        if r["is_field"] or r["event"] not in events:
            continue
        p = pct(r)
        if p is None:
            continue
        prof[r["canon"]].append(p)
        try:
            rk = int(r["qual_rank"])
        except ValueError:
            continue
        top8[r["canon"]][1] += 1
        if rk <= 8:
            top8[r["canon"]][0] += 1

    # --- also: did the judged-award winner ALSO win/finalist the event? ---
    field_teams = defaultdict(set)
    for r in rows:
        if r["is_field"]:
            field_teams[r["event"]].add(r["team"])
    also = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["is_field"] or r["event"] not in events:
            continue
        also[r["canon"]][1] += 1
        if r["team"] in field_teams.get(r["event"], ()):
            also[r["canon"]][0] += 1

    out = []
    order = sorted(prof, key=lambda a: -len(prof[a]))
    hdr = (f"{'award':<38}{'n':>5}{'evt%':>6}{'medRank%':>9}"
           f"{'top8%':>7}{'btm50%':>8}{'alsoElim%':>10}")
    print(hdr)
    print("-" * len(hdr))
    for a in order:
        v = prof[a]
        if len(v) < 30:
            continue
        cover = 100.0 * len(gave[a]) / len(events)
        med = statistics.median(v)
        t8 = 100.0 * top8[a][0] / top8[a][1] if top8[a][1] else 0
        btm = 100.0 * sum(1 for x in v if x > 50) / len(v)
        ae = 100.0 * also[a][0] / also[a][1] if also[a][1] else 0
        cat = "MACHINE" if a in MACHINE else ("TEAM" if a in TEAM_ADJ else "")
        print(f"{a:<38}{len(v):>5}{cover:>6.0f}{med:>9.1f}{t8:>7.0f}{btm:>8.0f}{ae:>10.0f}")
        out.append({
            "award": a, "category": cat, "n_winners_with_rank": len(v),
            "pct_events_awarded": round(cover, 1),
            "median_rank_pct": round(med, 1),
            "mean_rank_pct": round(statistics.mean(v), 1),
            "pct_winners_qual_top8": round(t8, 1),
            "pct_winners_bottom_half": round(btm, 1),
            "pct_winners_also_elim_award": round(ae, 1),
        })

    path = os.path.join(DATA, "award_rank_profile.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"\nwrote {path}")

    # --- name drift table ---
    print("\n--- raw award name by season (robot-adjacent only) ---")
    seen = defaultdict(lambda: defaultdict(set))
    for r in rows:
        if r["canon"] in MACHINE or r["canon"] in ("Rookie All-Star Award", "Judges' Award",
                                                   "Imagery Award", "Rising All-Star Award"):
            seen[r["canon"]][r["year"]].add(re.sub(r"^(District|Regional|Championship)"
                                                   r"( Championship)?( Division)? ", "",
                                                   r["award"]))
    for a in sorted(seen):
        print(f"\n{a}")
        for y in sorted(seen[a]):
            for nm in sorted(seen[a][y]):
                print(f"   {y}  {nm}")

    print(f"\nevents per season: {dict(sorted(per_year_events.items()))}")


if __name__ == "__main__":
    main()
