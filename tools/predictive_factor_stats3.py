#!/usr/bin/env python3
"""
predictive_factor_stats3.py -- corrected version of the pick-order analysis.

FIX vs predictive_factor_stats2.py: raw "Avg Match" is NOT comparable across events
(week-6 events score far more than week-1 events, and field size varies). Everything
here is normalised WITHIN each event: a team's score percentile is its rank among that
event's teams by "Avg Match" (1 = highest scorer at that event).

Questions answered:
  A. P(picked | qual-rank band) stratified by FIELD SIZE   -- how good must we be, at OUR size of event
  B. within-event score/auto percentile of the winning alliance's 3 robots
  C. picked vs unpicked in the same qual-rank band, compared on WITHIN-EVENT score percentile
  D. P(win event | seed) x slot  -- the "last pick of the 1 alliance" number
"""
import csv, os, collections, statistics as st, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "research", "predictive_tba")
YEARS = [2023, 2024, 2025, 2026]
AUTOCOL = {2023: "Avg Auto", 2024: "Avg Auto", 2025: "Avg Auto", 2026: "Avg Auto Fuel"}


def fnum(s):
    try:
        return float(s)
    except Exception:
        return None


def band(p):
    for lo, hi in ((0, 10), (10, 25), (25, 33), (33, 50), (50, 66), (66, 75), (75, 90), (90, 101)):
        if lo < p <= hi:
            return f"{lo}-{min(hi,100)}%"
    return "0-10%"


def sizebucket(n):
    if n < 36:
        return "small (<36 teams)"
    if n < 46:
        return "medium (36-45)"
    if n < 61:
        return "large (46-60)"
    return "huge (61+)"


out = {}
for y in YEARS:
    ac = AUTOCOL[y]
    tbl = collections.defaultdict(dict)
    with open(os.path.join(P, f"tba_rankings_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["event"], r["team"])
            tbl[k][r["col_name"]] = r["value"]
            tbl[k]["_rank"] = int(r["rank"])
    ev_teams = collections.defaultdict(list)
    for (ev, t) in tbl:
        ev_teams[ev].append(t)

    slot_of, seed_of, won = {}, {}, {}
    with open(os.path.join(P, f"tba_alliances_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slot_of[(r["event"], r["team"])] = r["slot"]
            seed_of[(r["event"], r["team"])] = int(r["alliance"])
            won[(r["event"], r["team"])] = int(r["won_event"])

    # within-event percentiles for Avg Match and the auto column
    spct, apct = {}, {}
    for ev, teams in ev_teams.items():
        sc = [(t, fnum(tbl[(ev, t)].get("Avg Match", ""))) for t in teams]
        sc = [x for x in sc if x[1] is not None]
        n = len(sc)
        for i, (t, _) in enumerate(sorted(sc, key=lambda z: -z[1])):
            spct[(ev, t)] = 100.0 * (i + 1) / n
        au = [(t, fnum(tbl[(ev, t)].get(ac, ""))) for t in teams]
        au = [x for x in au if x[1] is not None]
        n = len(au)
        for i, (t, _) in enumerate(sorted(au, key=lambda z: -z[1])):
            apct[(ev, t)] = 100.0 * (i + 1) / n

    Y = {}

    # ---- A. P(picked | rank band) x field size -------------------------------
    tot = collections.Counter()
    pk = collections.Counter()
    for (ev, t), d in tbl.items():
        n = len(ev_teams[ev])
        if n < 20:
            continue
        key = (sizebucket(n), band(100.0 * d["_rank"] / n))
        tot[key] += 1
        if (ev, t) in slot_of:
            pk[key] += 1
    A = collections.defaultdict(dict)
    for key in sorted(tot, key=lambda k: (k[0], float(k[1].split("-")[0]))):
        if tot[key] >= 40:
            A[key[0]][key[1]] = {"n": tot[key], "pct_picked": round(100.0 * pk[key] / tot[key], 1)}
    Y["p_picked_by_field_size_and_rank_band"] = dict(A)

    # ---- B. winning alliance profile -----------------------------------------
    prof = collections.defaultdict(lambda: {"rank": [], "score": [], "auto": []})
    for (ev, t), w in won.items():
        if not w or (ev, t) not in tbl:
            continue
        n = len(ev_teams[ev])
        s = slot_of[(ev, t)]
        prof[s]["rank"].append(100.0 * tbl[(ev, t)]["_rank"] / n)
        if (ev, t) in spct:
            prof[s]["score"].append(spct[(ev, t)])
        if (ev, t) in apct:
            prof[s]["auto"].append(apct[(ev, t)])
    Y["winning_alliance_profile"] = {}
    for s, d in prof.items():
        if not d["rank"]:
            continue
        Y["winning_alliance_profile"][s] = {
            "n": len(d["rank"]),
            "median_qual_rank_pctile": round(st.median(d["rank"]), 1),
            "median_score_pctile": round(st.median(d["score"]), 1) if d["score"] else None,
            "median_auto_pctile": round(st.median(d["auto"]), 1) if d["auto"] else None,
            "pct_qual_rank_in_bottom_half": round(100.0 * sum(1 for x in d["rank"] if x > 50) / len(d["rank"]), 1),
            "pct_score_pctile_in_bottom_half": round(100.0 * sum(1 for x in d["score"] if x > 50) / len(d["score"]), 1) if d["score"] else None,
        }

    # ---- C. picked vs unpicked, within-event score percentile -----------------
    comp = collections.defaultdict(lambda: {"p": [], "u": [], "pa": [], "ua": []})
    for (ev, t), d in tbl.items():
        n = len(ev_teams[ev])
        if n < 20 or (ev, t) not in spct:
            continue
        b = band(100.0 * d["_rank"] / n)
        tag = "p" if (ev, t) in slot_of else "u"
        comp[b][tag].append(spct[(ev, t)])
        if (ev, t) in apct:
            comp[b][tag + "a"].append(apct[(ev, t)])
    Y["picked_vs_unpicked_within_event_pctile"] = {}
    for b in sorted(comp, key=lambda s: float(s.split("-")[0])):
        d = comp[b]
        if len(d["p"]) < 40 or len(d["u"]) < 40:
            continue
        Y["picked_vs_unpicked_within_event_pctile"][b] = {
            "n_picked": len(d["p"]), "n_unpicked": len(d["u"]),
            "median_score_pctile_picked": round(st.median(d["p"]), 1),
            "median_score_pctile_unpicked": round(st.median(d["u"]), 1),
            "score_pctile_gap": round(st.median(d["u"]) - st.median(d["p"]), 1),
            "median_auto_pctile_picked": round(st.median(d["pa"]), 1) if d["pa"] else None,
            "median_auto_pctile_unpicked": round(st.median(d["ua"]), 1) if d["ua"] else None,
            "auto_pctile_gap": round(st.median(d["ua"]) - st.median(d["pa"]), 1) if (d["pa"] and d["ua"]) else None,
        }

    # ---- D. P(win event | seed, slot) ----------------------------------------
    wtot = collections.Counter()
    wwin = collections.Counter()
    for k, s in seed_of.items():
        key = (s, slot_of[k])
        wtot[key] += 1
        wwin[key] += won.get(k, 0)
    Y["p_win_event_by_seed_and_slot_pct"] = {
        f"seed{sd}_{sl}": round(100.0 * wwin[(sd, sl)] / wtot[(sd, sl)], 1)
        for (sd, sl) in sorted(wtot) if wtot[(sd, sl)] >= 25 and sd <= 3}

    out[y] = Y

print(json.dumps(out, indent=2))
with open(os.path.join(P, "predictive_factors3.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
