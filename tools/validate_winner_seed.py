#!/usr/bin/env python3
"""
validate_winner_seed.py -- back-test the "winning alliance seed" heuristic used by
tools/predictive_factor_stats.py, and recompute the seed->win distribution from an
INDEPENDENT source (the event's Winner award roster) rather than from the bracket.

Heuristic under test : the alliance seed appearing most often in <td class="winner">
                       cells on the TBA event page is the event champion.
Independent truth    : research/awards_tba/tba_awards_<YEAR>.csv rows whose award name
                       ends in "Winner"/"Winners" -- the teams FIRST recorded as champions.

A match = every winner-award team at that event is on the alliance the heuristic picked.
"""
import csv, os, collections, statistics as st, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "research", "predictive_tba")
A = os.path.join(ROOT, "research", "awards_tba")
YEARS = [2023, 2024, 2025, 2026]
WINNER_AWARDS = {"Regional Winners", "District Event Winner", "District Championship Winner",
                 "Championship Division Winner", "Championship Winner", "Winner",
                 "Event Winner", "Winner (1st Place)"}

report = {}
for y in YEARS:
    # alliance rosters + heuristic winner
    roster = collections.defaultdict(lambda: collections.defaultdict(set))  # ev -> seed -> teams
    seedof = collections.defaultdict(dict)                                   # ev -> team -> seed
    with open(os.path.join(P, f"tba_alliances_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            roster[r["event"]][int(r["alliance"])].add(r["team"])
            seedof[r["event"]][r["team"]] = int(r["alliance"])
    heur = {}
    weeks = {}
    with open(os.path.join(P, f"tba_events_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["winning_alliance"]:
                heur[r["event"]] = int(r["winning_alliance"])
            weeks[r["event"]] = r["week"]

    # truth from awards
    truth_teams = collections.defaultdict(set)
    with open(os.path.join(A, f"tba_awards_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["award"] in WINNER_AWARDS:
                truth_teams[r["event"]].add(r["team"])

    agree = dis = nocheck = 0
    true_seed = collections.Counter()
    for ev, teams in truth_teams.items():
        if ev not in roster:
            nocheck += 1
            continue
        seeds = {seedof[ev].get(t) for t in teams if t in seedof[ev]}
        seeds.discard(None)
        if len(seeds) != 1:
            nocheck += 1
            continue
        s = seeds.pop()
        true_seed[s] += 1
        if heur.get(ev) == s:
            agree += 1
        else:
            dis += 1
    tot = agree + dis
    n = sum(true_seed.values())
    report[y] = {
        "events_checked": tot,
        "heuristic_agreement_pct": round(100.0 * agree / tot, 1) if tot else None,
        "events_unresolvable": nocheck,
        "true_seed_distribution_pct": {str(k): round(100.0 * v / n, 1)
                                       for k, v in sorted(true_seed.items())},
        "true_pct_seed_1": round(100.0 * true_seed.get(1, 0) / n, 1),
        "true_pct_seed_1_or_2": round(100.0 * (true_seed.get(1, 0) + true_seed.get(2, 0)) / n, 1),
        "true_pct_seed_5_to_8": round(100.0 * sum(true_seed.get(k, 0) for k in (5, 6, 7, 8)) / n, 1),
        "n_events_with_resolved_winner": n,
    }

print(json.dumps(report, indent=2))
with open(os.path.join(P, "winner_seed_validation.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
