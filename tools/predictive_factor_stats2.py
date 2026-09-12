#!/usr/bin/env python3
"""
predictive_factor_stats2.py -- the second half of the evidence base for
reference/04_PREDICTIVE_FACTORS.md.

Answers, from The Blue Alliance public event pages only:
  A. P(picked at all | qualification rank band)            -> "how good must we be to get picked"
  B. rank profile of the 3 robots on the WINNING alliance  -> "what does a banner-winning 3rd robot look like"
  C. picked vs unpicked inside the same rank band, compared on Avg Match and Avg Auto
     -> does the pick reward SEED (reliability) or SCORE (ceiling)?
  D. P(win the event | slot, seed)
  E. auto share of score by rank decile -> is auto a luxury of good teams or a leveller?
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
            return f"{lo}-{hi if hi <= 100 else 100}%"
    return "0-10%"


out = {}
for y in YEARS:
    ac = AUTOCOL[y]
    # rankings
    tbl = collections.defaultdict(dict)
    with open(os.path.join(P, f"tba_rankings_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["event"], r["team"])
            tbl[k][r["col_name"]] = r["value"]
            tbl[k]["_rank"] = int(r["rank"])
    nteams = collections.Counter()
    for (ev, t) in tbl:
        nteams[ev] += 1

    # alliances
    slot_of = {}
    seed_of = {}
    won = {}
    with open(os.path.join(P, f"tba_alliances_{y}.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slot_of[(r["event"], r["team"])] = r["slot"]
            seed_of[(r["event"], r["team"])] = int(r["alliance"])
            won[(r["event"], r["team"])] = int(r["won_event"])

    Y = {}

    # ---- A. P(picked | rank band) --------------------------------------------
    picked_ct, total_ct = collections.Counter(), collections.Counter()
    for (ev, t), d in tbl.items():
        n = nteams[ev]
        if n < 20:
            continue
        b = band(100.0 * d["_rank"] / n)
        total_ct[b] += 1
        if (ev, t) in slot_of:
            picked_ct[b] += 1
    Y["p_picked_by_rank_band_pct"] = {
        b: round(100.0 * picked_ct[b] / total_ct[b], 1) for b in sorted(total_ct, key=lambda s: float(s.split("-")[0]))
    }
    Y["n_by_rank_band"] = {b: total_ct[b] for b in Y["p_picked_by_rank_band_pct"]}

    # ---- B. winning alliance roster profile ----------------------------------
    winroster = collections.defaultdict(list)
    for (ev, t), w in won.items():
        if w and (ev, t) in tbl:
            n = nteams[ev]
            winroster[slot_of[(ev, t)]].append(100.0 * tbl[(ev, t)]["_rank"] / n)
    Y["winning_alliance_rank_pct"] = {
        s: {"n": len(v), "median": round(st.median(v), 1),
            "p90": round(sorted(v)[int(.9 * len(v))], 1),
            "pct_from_bottom_half": round(100.0 * sum(1 for x in v if x > 50) / len(v), 1)}
        for s, v in winroster.items() if v
    }

    # ---- C. picked vs unpicked inside the same band ---------------------------
    comp = collections.defaultdict(lambda: {"picked_score": [], "unpicked_score": [],
                                            "picked_auto": [], "unpicked_auto": []})
    for (ev, t), d in tbl.items():
        n = nteams[ev]
        if n < 20:
            continue
        b = band(100.0 * d["_rank"] / n)
        m, a = fnum(d.get("Avg Match", "")), fnum(d.get(ac, ""))
        if m is None:
            continue
        key = "picked" if (ev, t) in slot_of else "unpicked"
        comp[b][key + "_score"].append(m)
        if a is not None:
            comp[b][key + "_auto"].append(a)
    Y["picked_vs_unpicked_in_band"] = {}
    for b, d in sorted(comp.items(), key=lambda kv: float(kv[0].split("-")[0])):
        if len(d["picked_score"]) < 30 or len(d["unpicked_score"]) < 30:
            continue
        ps, us = st.median(d["picked_score"]), st.median(d["unpicked_score"])
        pa, ua = (st.median(d["picked_auto"]) if d["picked_auto"] else None,
                  st.median(d["unpicked_auto"]) if d["unpicked_auto"] else None)
        Y["picked_vs_unpicked_in_band"][b] = {
            "n_picked": len(d["picked_score"]), "n_unpicked": len(d["unpicked_score"]),
            "median_avg_match_picked": round(ps, 1), "median_avg_match_unpicked": round(us, 1),
            "score_premium_pct": round(100.0 * (ps - us) / us, 1) if us else None,
            "median_avg_auto_picked": round(pa, 1) if pa is not None else None,
            "median_avg_auto_unpicked": round(ua, 1) if ua is not None else None,
            "auto_premium_pct": round(100.0 * (pa - ua) / ua, 1) if (pa is not None and ua) else None,
        }

    # ---- D. P(win event | slot) ----------------------------------------------
    slot_win = collections.Counter()
    slot_tot = collections.Counter()
    for k, s in slot_of.items():
        slot_tot[s] += 1
        slot_win[s] += won.get(k, 0)
    Y["p_win_event_by_slot_pct"] = {s: round(100.0 * slot_win[s] / slot_tot[s], 1)
                                    for s in sorted(slot_tot)}

    # ---- E. auto share by rank decile ----------------------------------------
    dec = collections.defaultdict(list)
    for (ev, t), d in tbl.items():
        n = nteams[ev]
        if n < 20:
            continue
        m, a = fnum(d.get("Avg Match", "")), fnum(d.get(ac, ""))
        if m and a is not None and m > 0:
            dec[min(9, int(10.0 * (d["_rank"] - 1) / n))].append(100.0 * a / m)
    Y["auto_pct_of_score_by_rank_decile"] = {
        f"decile_{k+1}": round(st.median(v), 1) for k, v in sorted(dec.items())}

    out[y] = Y

print(json.dumps(out, indent=2))
with open(os.path.join(P, "predictive_factors2.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
