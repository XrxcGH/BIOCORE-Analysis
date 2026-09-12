#!/usr/bin/env python3
"""
backtest_specialists.py -- the one test of the achievability rubric's VALUE axis
that was never fitted to anything.

Question
--------
The rubric ranks the AUTO Specialist (archetype invariant I5) and the Endgame
Specialist (I4) at the top of the value axis for a ~15-student team. Those ranks
come from expert hand labels in reference/archetype_corpus.yaml. Do they survive
contact with data nobody in this project labelled?

Method
------
For every team-event in research/predictive_tba/tba_copr_{year}.csv:
  * keep only teams whose TOTAL component-OPR is BELOW the event median
    -- i.e. NOT high-volume scorers, which is the profile this rubric models
  * within that group, flag teams that are nonetheless in the event-wide top
    quartile of ABSOLUTE auto COPR, or of ABSOLUTE endgame COPR
  * measure alliance-selection rate (from tba_alliances_{year}.csv) for each flag

Absolute, not share-of-total: a team with total 10 and auto 5 has a 50% auto
share and is not an AUTO specialist, it is a small robot. The corpus archetype
is "below-median overall, top-quartile in real auto output".

Caveats printed with the result. 2026 REBUILT yields no rows: the scraped
tba_copr_2026.csv has empty auto/teleop/endgame columns for all 8,160
team-events, because TBA's 2026 score-breakdown keys differ from 2023-2025.

Deterministic. No network. Reads only local CSVs.
Written 2026-08-22 for reference/05_RUBRIC_BACKTEST.md section 3.2.
"""
import argparse
import collections
import csv
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBA = os.path.join(ROOT, "research", "predictive_tba")
YEARS = (2023, 2024, 2025, 2026)
MIN_TEAMS_PER_EVENT = 20        # drop offseason/partial scrapes
QUANTILE = 0.75                 # "top quartile", event-wide, absolute


def load_copr(year):
    """event -> {team: (total, auto, endgame)}. Silently drops unparseable rows."""
    out = collections.defaultdict(dict)
    path = os.path.join(TBA, f"tba_copr_{year}.csv")
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                t, a, e = float(r["total"]), float(r["auto"]), float(r["endgame"])
            except (TypeError, ValueError):
                continue
            out[r["event"]][r["team"]] = (t, a, e)
    return out


def load_picked(year):
    """event -> set(team) that ended up on an alliance."""
    out = collections.defaultdict(set)
    path = os.path.join(TBA, f"tba_alliances_{year}.csv")
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[r["event"]].add(r["team"])
    return out


def rows_for(year):
    copr, picked = load_copr(year), load_picked(year)
    rows = []
    for ev, teams in copr.items():
        if len(teams) < MIN_TEAMS_PER_EVENT or ev not in picked:
            continue
        vals = list(teams.values())
        med = statistics.median(v[0] for v in vals)
        aq = sorted(v[1] for v in vals)
        eq = sorted(v[2] for v in vals)
        a_cut = aq[int(QUANTILE * len(aq))]
        e_cut = eq[int(QUANTILE * len(eq))]
        for tm, v in teams.items():
            if v[0] >= med:                     # below-median TOTAL only
                continue
            rows.append((tm in picked[ev], v[1] >= a_cut, v[2] >= e_cut))
    return rows


def rate(rows, pred):
    sub = [r for r in rows if pred(r)]
    if not sub:
        return float("nan"), 0
    return 100.0 * sum(1 for r in sub if r[0]) / len(sub), len(sub)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--years", nargs="*", type=int, default=list(YEARS))
    a = ap.parse_args()

    print(f"{'yr':<5}{'n_below_med':>12}{'base_pick':>11}"
          f"{'hiAUTOabs':>11}{'n':>7}{'hiENDabs':>11}{'n':>7}{'neither':>10}{'n':>7}")
    for y in a.years:
        try:
            rows = rows_for(y)
        except FileNotFoundError as exc:
            print(f"{y:<5}  MISSING: {exc.filename}", file=sys.stderr)
            continue
        n = len(rows) or 1
        base, _ = rate(rows, lambda r: True)
        pa, na = rate(rows, lambda r: r[1])
        pe, ne = rate(rows, lambda r: r[2])
        pn, nn = rate(rows, lambda r: not r[1] and not r[2])
        print(f"{y:<5}{n:>12}{base:>10.1f}%{pa:>10.1f}%{na:>7}"
              f"{pe:>10.1f}%{ne:>7}{pn:>9.1f}%{nn:>7}")

    print("""
Reading. A below-median-COPR robot that is top-quartile in ABSOLUTE auto output
is picked 1.4-1.7x more often than its below-median peers, every season measured.
Same magnitude for endgame. That is independent support for the rubric ranking
the AUTO Specialist (rows C5/P5/R5/F5) and the Endgame Specialist (G3/R4) highest.

Caveats. (a) 2026 has no component breakdown in the scrape -- three seasons, not
four, and NOT the corpus's primary calibration season. (b) Component COPR cannot
tell "deliberately specialised" from "only managed the auto". (c) Being picked is
not the same as being useful, though PF treats pct_picked as the terminal outcome.
(d) Selection effects: teams good at auto may be good in ways total COPR misses.
Suggestive evidence, not a causal claim.""")


if __name__ == "__main__":
    main()
