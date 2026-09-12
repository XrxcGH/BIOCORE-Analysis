#!/usr/bin/env python3
"""
predictive_factor_stats6.py -- pass-6 analyses for reference/04_PREDICTIVE_FACTORS.md.

Closes the two gaps pass 5 declared largest:
  * component contribution (auto / teleop / endgame) per team, previously [S] because
    Statbotics has been HTTP 500 since 2026-08-21 -- now measured from TBA Component OPR;
  * reliability as MECHANICAL consistency rather than DQ -- measured as the spread of
    per-match residuals around the OPR least-squares fit.

Inputs  (research/predictive_tba/):
    tba_copr_<Y>.csv       year,event,week,team,opr,auto,teleop,endgame,foul,rp,total
    tba_resid_<Y>.csv      year,event,week,team,n_matches,resid_mean,resid_sd,resid_min
    tba_alliances_<Y>.csv  year,event,week,alliance,slot,team,qual_rank,n_teams,rank_pct,won_event
    tba_rankings_<Y>.csv   year,event,week,col_index,col_name,rank,team,value

Outputs (research/predictive_tba/):
    pf6_component_share.csv     component share of OPR by OPR decile
    pf6_component_auc.csv       AUC for "was picked" from each component, raw and OPR-controlled
    pf6_consistency.csv         pick rate and rank by within-event consistency quartile
    pf6_consistency_auc.csv     does penalising variance improve a pure-output picklist?
    pf6_deadmatch.csv           frequency + cost of a team's single worst match
    pf6_summary.json
"""
import csv
import json
import os
import statistics as st
from collections import defaultdict

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "research", "predictive_tba")
YEARS = [2023, 2024, 2025, 2026]
# season -> was a Ranking Point gated on an autonomous accomplishment? (verified in §13.2)
AUTO_RP = {2023: False, 2024: False, 2025: True, 2026: False}


def load(name, year):
    p = os.path.join(OUT, f"tba_{name}_{year}.csv")
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def auc(pairs):
    """Mann-Whitney AUC. pairs = [(score, label 0/1)]. Ties count half."""
    pos = sorted(s for s, y in pairs if y == 1)
    neg = sorted(s for s, y in pairs if y == 0)
    if not pos or not neg:
        return None
    # rank-sum with tie correction
    allv = sorted(pos + neg)
    ranks = {}
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1] == allv[i]:
            j += 1
        r = (i + j) / 2.0 + 1
        ranks[allv[i]] = r
        i = j + 1
    rsum = sum(ranks[s] for s in pos)
    n1, n0 = len(pos), len(neg)
    return (rsum - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def main():
    summary = {}
    comp_share_rows, comp_auc_rows, cons_rows, cons_auc_rows, dead_rows = [], [], [], [], []

    for year in YEARS:
        copr = load("copr", year)
        resid = load("resid", year)
        alli = load("alliances", year)

        picked = {(a["event"], a["team"]) for a in alli}
        # rank percentile from the rankings table (0 = best)
        rankpct, nteams = {}, {}
        for r in load("rankings", year):
            if r["col_name"] != "Ranking Score":
                continue
            rankpct[(r["event"], r["team"])] = int(r["rank"])
        for ev, g in _group(copr, "event").items():
            nteams[ev] = len(g)

        # ---------- 1. component share of OPR, by OPR decile -------------------
        by_ev = _group(copr, "event")
        deciles = defaultdict(lambda: defaultdict(list))
        for ev, rows in by_ev.items():
            rows = [r for r in rows if fnum(r["opr"]) is not None]
            rows.sort(key=lambda r: fnum(r["opr"]))
            n = len(rows)
            if n < 20:
                continue
            for i, r in enumerate(rows):
                d = min(9, int(10 * i / n))
                o = fnum(r["opr"])
                if o is None or o <= 0:
                    continue
                for c in ("auto", "teleop", "endgame"):
                    v = fnum(r[c])
                    if v is not None:
                        deciles[d][c].append(100.0 * v / o)
        for d in sorted(deciles):
            row = {"year": year, "opr_decile": d + 1}
            for c in ("auto", "teleop", "endgame"):
                vals = deciles[d][c]
                row[c + "_pct_of_opr"] = round(st.median(vals), 1) if vals else ""
            row["n"] = len(deciles[d]["auto"])
            comp_share_rows.append(row)

        # ---------- 2. does a component predict PICK beyond total output? ------
        # Restricted to the contested middle of each event (rank 25%-85%) exactly as
        # pass 4 did for pf4_pick_auc, so the numbers are comparable.
        raw = defaultdict(list)
        ctrl = defaultdict(list)   # within-OPR-quintile, component residualised
        for ev, rows in by_ev.items():
            n = len(rows)
            if n < 24:
                continue
            rows = [r for r in rows if fnum(r["opr"]) is not None]
            rk = [(rankpct.get((ev, r["team"])), r) for r in rows]
            rk = [(a, b) for a, b in rk if a]
            rk.sort()
            lo, hi = int(0.25 * len(rk)), int(0.85 * len(rk))
            mid = [b for a, b in rk[lo:hi]]
            if len(mid) < 8:
                continue
            for c in ("opr", "auto", "teleop", "endgame"):
                for r in mid:
                    v = fnum(r[c])
                    if v is None:
                        continue
                    raw[c].append((v, 1 if (ev, r["team"]) in picked else 0))
            # OPR-controlled: split mid into OPR terciles, AUC of component inside each
            mid2 = sorted([r for r in mid if fnum(r["opr"]) is not None],
                          key=lambda r: fnum(r["opr"]))
            k = max(1, len(mid2) // 3)
            for t in range(3):
                chunk = mid2[t * k:(t + 1) * k] if t < 2 else mid2[2 * k:]
                for c in ("auto", "teleop", "endgame"):
                    for r in chunk:
                        v = fnum(r[c])
                        if v is None:
                            continue
                        ctrl[(c, t)].append((v, 1 if (ev, r["team"]) in picked else 0))
        row = {"year": year, "auto_rp": AUTO_RP[year]}
        for c in ("opr", "auto", "teleop", "endgame"):
            a = auc(raw[c])
            row[c + "_auc"] = round(a, 3) if a else ""
            row["n_" + c] = len(raw[c])
        for c in ("auto", "teleop", "endgame"):
            aa = [auc(ctrl[(c, t)]) for t in range(3)]
            aa = [x for x in aa if x]
            row[c + "_auc_within_opr_tercile"] = round(st.fmean(aa), 3) if aa else ""
        comp_auc_rows.append(row)

        # ---------- 3. consistency: residual spread around the OPR fit ---------
        rmap = {(r["event"], r["team"]): r for r in resid}
        omap = {(r["event"], r["team"]): fnum(r["opr"]) for r in copr}
        # normalise resid_sd within event (event scoring scales differ hugely by season)
        ev_sd_med = {}
        for ev, rows in _group(resid, "event").items():
            v = [fnum(r["resid_sd"]) for r in rows]
            v = [x for x in v if x is not None]
            if v:
                ev_sd_med[ev] = st.median(v)
        quart = defaultdict(lambda: {"n": 0, "picked": 0, "opr": [], "rank": []})
        for ev, rows in _group(resid, "event").items():
            if ev_sd_med.get(ev, 0) <= 0 or len(rows) < 20:
                continue
            # rank teams by OPR into 3 output bands, then by consistency inside each band
            rows = [r for r in rows if omap.get((ev, r["team"])) is not None]
            rows.sort(key=lambda r: omap[(ev, r["team"])])
            n = len(rows)
            for i, r in enumerate(rows):
                band = min(2, int(3 * i / n))
                rel = fnum(r["resid_sd"]) / ev_sd_med[ev]
                r["_band"], r["_rel"] = band, rel
            for band in range(3):
                b = sorted([r for r in rows if r["_band"] == band], key=lambda r: r["_rel"])
                m = len(b)
                if m < 6:
                    continue
                for i, r in enumerate(b):
                    q = min(3, int(4 * i / m))
                    key = (band, q)
                    quart[key]["n"] += 1
                    quart[key]["picked"] += 1 if (ev, r["team"]) in picked else 0
                    quart[key]["opr"].append(omap[(ev, r["team"])])
        for (band, q), d in sorted(quart.items()):
            cons_rows.append({
                "year": year,
                "output_band": ["low", "mid", "high"][band],
                "consistency_quartile": ["Q1 most consistent", "Q2", "Q3",
                                         "Q4 most erratic"][q],
                "n": d["n"],
                "pct_picked": round(100.0 * d["picked"] / d["n"], 1),
                "median_opr": round(st.median(d["opr"]), 1),
            })

        # ---------- 4. does penalising variance beat raw output on a picklist? --
        for k in (0.0, 0.25, 0.5, 1.0):
            pairs = []
            for ev, rows in _group(resid, "event").items():
                if ev_sd_med.get(ev, 0) <= 0:
                    continue
                sc = ev_sd_med[ev]
                rr = [(rankpct.get((ev, r["team"])), r) for r in rows]
                rr = [(a, b) for a, b in rr if a]
                rr.sort()
                lo, hi = int(0.25 * len(rr)), int(0.85 * len(rr))
                for _, r in rr[lo:hi]:
                    o = omap.get((ev, r["team"]))
                    s = fnum(r["resid_sd"])
                    if o is None or s is None:
                        continue
                    # score in units of the event's own scale
                    pairs.append((o - k * (s / sc) * (o if False else sc),
                                  1 if (ev, r["team"]) in picked else 0))
            a = auc(pairs)
            cons_auc_rows.append({"year": year, "variance_penalty_k": k,
                                  "auc_pick": round(a, 4) if a else "", "n": len(pairs)})

        # ---------- 5. the single worst match ----------------------------------
        rel_min, both = [], []
        for ev, rows in _group(resid, "event").items():
            if ev_sd_med.get(ev, 0) <= 0:
                continue
            sc = ev_sd_med[ev]
            for r in rows:
                mn = fnum(r["resid_min"])
                if mn is None:
                    continue
                z = mn / sc
                rel_min.append(z)
                both.append((z, 1 if (ev, r["team"]) in picked else 0, ev, r["team"]))
        # bucket by how bad the worst match was, in event-sigma units
        buckets = [(-1e9, -3.0, "worst match <= -3 sigma"),
                   (-3.0, -2.0, "-3 to -2 sigma"),
                   (-2.0, -1.0, "-2 to -1 sigma"),
                   (-1.0, 1e9, "> -1 sigma")]
        for lo, hi, label in buckets:
            g = [b for b in both if lo <= b[0] < hi]
            if not g:
                continue
            dead_rows.append({
                "year": year, "worst_match_bucket": label, "n": len(g),
                "pct_of_field": round(100.0 * len(g) / len(both), 1),
                "pct_picked": round(100.0 * sum(b[1] for b in g) / len(g), 1),
            })

        summary[year] = {
            "team_events": len(copr),
            "auto_rp": AUTO_RP[year],
            "median_resid_sd": round(st.median([fnum(r["resid_sd"]) for r in resid
                                                if fnum(r["resid_sd"]) is not None]), 2),
        }

    for name, rows in (("component_share", comp_share_rows),
                       ("component_auc", comp_auc_rows),
                       ("consistency", cons_rows),
                       ("consistency_auc", cons_auc_rows),
                       ("deadmatch", dead_rows)):
        p = os.path.join(OUT, f"pf6_{name}.csv")
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print("wrote", p, len(rows), "rows")

    with open(os.path.join(OUT, "pf6_summary.json"), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "component_auc": comp_auc_rows,
                   "consistency": cons_rows, "consistency_auc": cons_auc_rows,
                   "deadmatch": dead_rows, "component_share": comp_share_rows},
                  f, indent=1)
    print("wrote", os.path.join(OUT, "pf6_summary.json"))


def _group(rows, key):
    d = defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


if __name__ == "__main__":
    main()
