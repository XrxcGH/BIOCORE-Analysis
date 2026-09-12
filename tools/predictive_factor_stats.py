#!/usr/bin/env python3
"""
predictive_factor_stats.py -- turn the TBA scrape into the numbers cited in
reference/04_PREDICTIVE_FACTORS.md.

Input : research/predictive_tba/tba_{rankings,alliances,events}_<YEAR>.csv
Output: research/predictive_tba/predictive_factors.yaml  (machine-readable)
        plus a human-readable dump on stdout.

Every number this script prints is derived from The Blue Alliance's public event
pages. Nothing is estimated or modelled.
"""
import csv, os, statistics as st, sys, collections, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(ROOT, "research", "predictive_tba")
YEARS = [2023, 2024, 2025, 2026]
WEEK_ORDER = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7",
              "FIRST Championship"]


def load_rankings(y):
    """-> {(event, team): {colname: value}}, {event: week}"""
    tbl = collections.defaultdict(dict)
    wk = {}
    with open(os.path.join(D, f"tba_rankings_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tbl[(r["event"], r["team"])][r["col_name"]] = r["value"]
            tbl[(r["event"], r["team"])]["_rank"] = int(r["rank"])
            wk[r["event"]] = r["week"]
    return tbl, wk


def load_alliances(y):
    rows = []
    with open(os.path.join(D, f"tba_alliances_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def fnum(s):
    try:
        return float(s)
    except Exception:
        return None


def pct(x, n):
    return round(100.0 * x / n, 1) if n else None


out = {"source": "The Blue Alliance public event pages", "years": {}}

for y in YEARS:
    tbl, wk = load_rankings(y)
    alli = load_alliances(y)
    Y = {}

    # ---------------------------------------------------------------- ALLIANCE SELECTION
    slots = collections.defaultdict(list)
    for r in alli:
        if not r["rank_pct"]:
            continue
        slots[r["slot"]].append(float(r["rank_pct"]))
    sel = {}
    for slot in ("captain", "pick1", "pick2", "backup"):
        v = slots.get(slot, [])
        if not v:
            continue
        sel[slot] = {
            "n": len(v),
            "median_rank_pct": round(st.median(v), 1),
            "mean_rank_pct": round(st.mean(v), 1),
            "p10_rank_pct": round(sorted(v)[int(0.10 * len(v))], 1),
            "p90_rank_pct": round(sorted(v)[int(0.90 * len(v))], 1),
            "pct_from_top_25pct_of_field": pct(sum(1 for x in v if x <= 25), len(v)),
            "pct_from_bottom_half_of_field": pct(sum(1 for x in v if x > 50), len(v)),
        }
    Y["alliance_selection_rank_pct"] = sel

    # what absolute qual rank does the last picked robot have?
    lastpick = collections.defaultdict(int)
    byevent = collections.defaultdict(list)
    for r in alli:
        if r["qual_rank"]:
            byevent[r["event"]].append((int(r["alliance"]), r["slot"], int(r["qual_rank"]),
                                        int(r["n_teams"])))
    deepest = []
    for ev, rows in byevent.items():
        n = rows[0][3]
        picked = [rk for _, slot, rk, _ in rows if slot != "captain"]
        if picked:
            deepest.append(100.0 * max(picked) / n)
    Y["deepest_pick_rank_pct"] = {
        "n_events": len(deepest),
        "median": round(st.median(deepest), 1),
        "p90": round(sorted(deepest)[int(0.9 * len(deepest))], 1),
        "pct_events_reaching_bottom_half": pct(sum(1 for x in deepest if x > 50), len(deepest)),
        "pct_events_reaching_bottom_quartile": pct(sum(1 for x in deepest if x > 75), len(deepest)),
    }

    # ---------------------------------------------------------------- WHO WINS EVENTS
    winners = collections.Counter()
    for ev, rows in byevent.items():
        pass
    wc = collections.Counter()
    seen_ev = set()
    with open(os.path.join(D, f"tba_events_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["winning_alliance"]:
                wc[int(r["winning_alliance"])] += 1
                seen_ev.add(r["event"])
    tot = sum(wc.values())
    Y["event_winner_by_alliance_seed"] = {
        "n_events": tot,
        "pct": {str(k): pct(v, tot) for k, v in sorted(wc.items())},
        "pct_seed_1": pct(wc.get(1, 0), tot),
        "pct_seed_1_to_2": pct(wc.get(1, 0) + wc.get(2, 0), tot),
        "pct_seed_5_to_8": pct(sum(wc.get(k, 0) for k in (5, 6, 7, 8)), tot),
    }

    # ---------------------------------------------------------------- AUTO SHARE
    autocol = "Avg Auto" if y < 2026 else "Avg Auto Fuel"
    ratios, autos, matches = [], [], []
    top_auto_rank, all_pairs = [], []
    for (ev, team), d in tbl.items():
        m, a = fnum(d.get("Avg Match", "")), fnum(d.get(autocol, ""))
        if m and a is not None and m > 0:
            ratios.append(100.0 * a / m)
            autos.append(a)
            matches.append(m)
            all_pairs.append((d["_rank"], a, m))
    Y["auto"] = {
        "auto_column": autocol,
        "n_team_events": len(ratios),
        "median_auto_pct_of_match_score": round(st.median(ratios), 1),
        "mean_auto_pct_of_match_score": round(st.mean(ratios), 1),
        "median_avg_match_score": round(st.median(matches), 1),
        "median_avg_auto": round(st.median(autos), 1),
    }

    # Spearman-ish: is auto or match score the better rank predictor?
    def rank_corr(idx):
        pairs = [(p[0], p[idx]) for p in all_pairs]
        n = len(pairs)
        if n < 30:
            return None
        xs = sorted(range(n), key=lambda i: pairs[i][0])
        ys = sorted(range(n), key=lambda i: pairs[i][1])
        rx = [0] * n
        ry = [0] * n
        for r, i in enumerate(xs):
            rx[i] = r
        for r, i in enumerate(ys):
            ry[i] = r
        mx, my = st.mean(rx), st.mean(ry)
        num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
        den = (sum((rx[i] - mx) ** 2 for i in range(n)) ** .5) * (sum((ry[i] - my) ** 2 for i in range(n)) ** .5)
        return round(-num / den, 3) if den else None  # negate: rank 1 = best

    Y["auto"]["spearman_rank_vs_avg_auto"] = rank_corr(1)
    Y["auto"]["spearman_rank_vs_avg_match"] = rank_corr(2)

    # ---------------------------------------------------------------- WEEK TREND
    perev = collections.defaultdict(list)
    perev_auto = collections.defaultdict(list)
    for (ev, team), d in tbl.items():
        m = fnum(d.get("Avg Match", ""))
        a = fnum(d.get(autocol, ""))
        if m:
            perev[ev].append(m)
        if a is not None:
            perev_auto[ev].append(a)
    week_scores = collections.defaultdict(list)
    week_auto = collections.defaultdict(list)
    week_top = collections.defaultdict(list)
    for ev, v in perev.items():
        w = wk.get(ev, "")
        if w:
            week_scores[w].append(st.mean(v))
            week_top[w].append(max(v))
    for ev, v in perev_auto.items():
        w = wk.get(ev, "")
        if w:
            week_auto[w].append(st.mean(v))
    Y["week_trend"] = {}
    for w in WEEK_ORDER:
        if w in week_scores:
            Y["week_trend"][w] = {
                "n_events": len(week_scores[w]),
                "mean_event_avg_match_score": round(st.mean(week_scores[w]), 1),
                "mean_event_top_team_avg_score": round(st.mean(week_top[w]), 1),
                "mean_event_avg_auto": round(st.mean(week_auto[w]), 1) if w in week_auto else None,
            }
    if "Week 1" in Y["week_trend"] and "Week 5" in Y["week_trend"]:
        w1 = Y["week_trend"]["Week 1"]["mean_event_avg_match_score"]
        w5 = Y["week_trend"]["Week 5"]["mean_event_avg_match_score"]
        Y["week_trend"]["w1_to_w5_score_inflation_pct"] = round(100.0 * (w5 - w1) / w1, 1)
        t1 = Y["week_trend"]["Week 1"]["mean_event_top_team_avg_score"]
        t5 = Y["week_trend"]["Week 5"]["mean_event_top_team_avg_score"]
        Y["week_trend"]["w1_to_w5_top_team_inflation_pct"] = round(100.0 * (t5 - t1) / t1, 1)

    # ---------------------------------------------------------------- RELIABILITY PROXY
    # "Played" below the event mode = matches missed / not played.
    missed = collections.Counter()
    tot_te = 0
    byev_played = collections.defaultdict(list)
    for (ev, team), d in tbl.items():
        p = fnum(d.get("Played", ""))
        if p:
            byev_played[ev].append((team, p, d["_rank"]))
    ranks_of_full, ranks_of_short = [], []
    n_short = 0
    n_tot = 0
    for ev, rows in byev_played.items():
        mode = collections.Counter(p for _, p, _ in rows).most_common(1)[0][0]
        nteams = len(rows)
        for team, p, rk in rows:
            n_tot += 1
            if p < mode:
                n_short += 1
                ranks_of_short.append(100.0 * rk / nteams)
            else:
                ranks_of_full.append(100.0 * rk / nteams)
    Y["played_shortfall"] = {
        "n_team_events": n_tot,
        "pct_teams_played_fewer_than_modal_quals": pct(n_short, n_tot),
        "median_rank_pct_full_schedule": round(st.median(ranks_of_full), 1) if ranks_of_full else None,
        "median_rank_pct_short_schedule": round(st.median(ranks_of_short), 1) if ranks_of_short else None,
    }

    # DQ
    dqs = []
    for (ev, team), d in tbl.items():
        v = fnum(d.get("DQ", ""))
        if v is not None:
            dqs.append(v)
    Y["dq"] = {"n_team_events": len(dqs),
               "pct_with_at_least_one_dq": pct(sum(1 for x in dqs if x >= 1), len(dqs)),
               "mean_dq_per_team_event": round(st.mean(dqs), 3) if dqs else None}

    # ---------------------------------------------------------------- CEILING vs FLOOR
    # For picked vs unpicked teams: compare Avg Match percentile against rank percentile.
    picked = set()
    for r in alli:
        picked.add((r["event"], r["team"]))
    ev_scores = collections.defaultdict(list)
    for (ev, team), d in tbl.items():
        m = fnum(d.get("Avg Match", ""))
        if m:
            ev_scores[ev].append((team, m, d["_rank"]))
    pick_score_pct, pick_rank_pct = [], []
    for ev, rows in ev_scores.items():
        n = len(rows)
        order = sorted(rows, key=lambda t: -t[1])
        spct = {t: 100.0 * (i + 1) / n for i, (t, _, _) in enumerate(order)}
        for team, m, rk in rows:
            if (ev, team) in picked:
                pick_score_pct.append(spct[team])
                pick_rank_pct.append(100.0 * rk / n)
    Y["picked_teams"] = {
        "n": len(pick_score_pct),
        "median_score_percentile": round(st.median(pick_score_pct), 1),
        "median_rank_percentile": round(st.median(pick_rank_pct), 1),
        "pct_picked_outside_top_third_by_score": pct(sum(1 for x in pick_score_pct if x > 33.3),
                                                    len(pick_score_pct)),
    }

    out["years"][y] = Y

# ---------------------------------------------------------------------- print + write
print(json.dumps(out, indent=2))
with open(os.path.join(D, "predictive_factors.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("\nwrote", os.path.join(D, "predictive_factors.json"), file=sys.stderr)
