#!/usr/bin/env python3
"""
predictive_factor_stats4.py -- the WITHIN-EVENT evidence pass for
reference/04_PREDICTIVE_FACTORS.md.

Why a 4th pass: predictive_factor_stats{1,2,3}.py pooled every team-event in a
season into one bucket. That is wrong for anything score-based, because match
scores are not comparable across events (different fields, different weeks,
different opponent quality). Everything here is computed WITHIN an event and
then aggregated across events, which is the only way a score comparison means
anything.

Inputs (already scraped by tools/tba_predictive_scrape.py):
    research/predictive_tba/tba_rankings_<Y>.csv    long form: col_name,value
    research/predictive_tba/tba_alliances_<Y>.csv
    research/predictive_tba/tba_events_<Y>.csv

IMPORTANT DATA CAVEAT, stated once and inherited by every number below:
    TBA's "Avg Match" and "Avg Auto" ranking columns are ALLIANCE averages over
    the matches a team played -- they are NOT that team's own contribution.
    A team's own quality is roughly 1/3 of the signal; the other 2/3 is its
    randomly-assigned partners. So every score coefficient here is ATTENUATED
    (biased toward zero) relative to the true team-level effect. They are still
    the right numbers for one specific purpose: they are exactly what an
    ALLIANCE CAPTAIN sees on the public rankings screen if they do not scout.

Outputs (--out dir):
    pf4_captaincy_base_rates.csv
    pf4_auto_within_event.csv
    pf4_pick_auc.csv
    pf4_multi_event_growth.csv
    pf4_reliability.csv
    pf4_summary.json

Usage:
    python tools/predictive_factor_stats4.py --data research/predictive_tba \
        --out research/predictive_tba --years 2023 2024 2025 2026
"""
import argparse
import csv
import json
import math
import os
import statistics
from collections import defaultdict

YEARS = (2023, 2024, 2025, 2026)
AUTO_ALIASES = ("Avg Auto", "Avg Auto Fuel")


# ---------------------------------------------------------------- stats utils
def _ranks(xs):
    """Average-tie ranks, 1-based."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    return pearson(_ranks(xs), _ranks(ys))


def partial(r_xy, r_xz, r_yz):
    """Partial correlation of x,y controlling for z."""
    if None in (r_xy, r_xz, r_yz):
        return None
    d = (1 - r_xz ** 2) * (1 - r_yz ** 2)
    if d <= 1e-12:
        return None
    return (r_xy - r_xz * r_yz) / math.sqrt(d)


def auc(scores, labels):
    """Mann-Whitney AUC. labels 1 = positive. Higher score => predicts 1."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return None
    rk = _ranks(scores)
    sp = sum(r for r, l in zip(rk, labels) if l)
    n1, n0 = len(pos), len(neg)
    return (sp - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def q(xs, p):
    if not xs:
        return None
    s = sorted(xs)
    k = (len(s) - 1) * p
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return s[lo] if lo == hi else s[lo] + (s[hi] - s[lo]) * (k - lo)


def num(s):
    try:
        return float(str(s).replace(",", "").strip())
    except Exception:
        return None


# ---------------------------------------------------------------- data loading
def load_year(data, year):
    """-> events{key:{week,n_teams,winning_alliance}},
          teams{(event,team):{col:val, rank:int}},
          alli{(event,team):slot}"""
    events = {}
    p = os.path.join(data, f"tba_events_{year}.csv")
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            events[r["event"]] = {
                "week": r["week"],
                "n_teams": num(r["n_teams"]),
                "winner": r.get("winning_alliance", ""),
            }
    teams = defaultdict(dict)
    p = os.path.join(data, f"tba_rankings_{year}.csv")
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["event"], r["team"])
            teams[k]["rank"] = num(r["rank"])
            teams[k][r["col_name"]] = r["value"]
    alli = {}
    p = os.path.join(data, f"tba_alliances_{year}.csv")
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            alli[(r["event"], r["team"])] = r["slot"]
    return events, teams, alli


def autocol(row):
    for a in AUTO_ALIASES:
        if a in row:
            return a
    return None


# ------------------------------------------------------------------- analyses
def a_captaincy(data, years):
    """P(team ever captains / is ever picked), split by how many events it played.
    This is the base rate any claim like '22% of Everybot teams captained an
    alliance' has to be measured against."""
    rows = []
    for y in years:
        events, teams, alli = load_year(data, y)
        n_ev = defaultdict(int)
        cap = defaultdict(int)
        pick = defaultdict(int)
        for (ev, tm) in teams:
            n_ev[tm] += 1
            slot = alli.get((ev, tm))
            if slot == "captain":
                cap[tm] += 1
            if slot in ("captain", "pick1", "pick2", "backup"):
                pick[tm] += 1
        buckets = defaultdict(list)
        for tm, n in n_ev.items():
            b = str(n) if n <= 3 else "4+"
            buckets[b].append(tm)
        for b in ("1", "2", "3", "4+", "ALL"):
            tms = (list(n_ev) if b == "ALL" else buckets.get(b, []))
            if not tms:
                continue
            rows.append({
                "year": y, "events_attended": b, "n_teams": len(tms),
                "pct_ever_captain": round(100 * sum(1 for t in tms if cap[t]) / len(tms), 1),
                "pct_ever_on_alliance": round(100 * sum(1 for t in tms if pick[t]) / len(tms), 1),
                "captaincies_per_team": round(sum(cap[t] for t in tms) / len(tms), 3),
            })
    return rows


def b_auto(data, years):
    """WITHIN-EVENT rank correlations for auto vs the rest of the score, and the
    partial correlation of auto with rank once total score is held fixed."""
    rows = []
    for y in years:
        events, teams, alli = load_year(data, y)
        by_ev = defaultdict(list)
        for (ev, tm), row in teams.items():
            by_ev[ev].append(row)
        s_match, s_auto, s_rest, s_part, share = [], [], [], [], []
        for ev, rws in by_ev.items():
            ac = autocol(rws[0])
            if not ac:
                continue
            rk, mt, au = [], [], []
            for r in rws:
                a, b, c = r.get("rank"), num(r.get("Avg Match")), num(r.get(ac))
                if None in (a, b, c):
                    continue
                rk.append(-a)          # negate so "higher = better rank"
                mt.append(b)
                au.append(c)
            if len(rk) < 12 or max(mt) <= 0:
                continue
            rest = [m - a for m, a in zip(mt, au)]
            r_rm, r_ra, r_rr = spearman(rk, mt), spearman(rk, au), spearman(rk, rest)
            r_ma = spearman(mt, au)
            if None in (r_rm, r_ra, r_ma):
                continue
            s_match.append(r_rm)
            s_auto.append(r_ra)
            if r_rr is not None:
                s_rest.append(r_rr)
            p = partial(r_ra, r_rm, r_ma)
            if p is not None:
                s_part.append(p)
            share.append(100 * statistics.median(au) / statistics.median(mt))
        rows.append({
            "year": y, "n_events": len(s_match),
            "median_spearman_rank_vs_avgmatch": round(statistics.median(s_match), 3),
            "median_spearman_rank_vs_avgauto": round(statistics.median(s_auto), 3),
            "median_spearman_rank_vs_nonauto": round(statistics.median(s_rest), 3) if s_rest else None,
            "median_partial_auto_given_total": round(statistics.median(s_part), 3) if s_part else None,
            "median_auto_share_of_score_pct": round(statistics.median(share), 1),
        })
    return rows


def c_pick_auc(data, years):
    """Within each event, how well does each public rankings column separate the
    teams that got picked from the teams that did not? AUC, 0.5 = coin flip.
    Restricted to the CONTESTED middle of the field (rank pct 25-90), because
    the top of the field is picked with probability ~1 and adds no information."""
    rows = []
    for y in years:
        events, teams, alli = load_year(data, y)
        by_ev = defaultdict(list)
        for (ev, tm), row in teams.items():
            by_ev[ev].append((tm, row))
        acc = defaultdict(list)
        for ev, pairs in by_ev.items():
            n = len(pairs)
            if n < 24:
                continue
            ac = autocol(pairs[0][1])
            if not ac:
                continue
            sel = []
            for tm, r in pairs:
                rk = r.get("rank")
                if rk is None:
                    continue
                pct = 100.0 * (rk - 1) / max(1, n - 1)
                if not (25.0 <= pct <= 90.0):
                    continue
                m, a, rs = num(r.get("Avg Match")), num(r.get(ac)), num(r.get("Ranking Score"))
                if None in (m, a, rs):
                    continue
                lab = 1 if alli.get((ev, tm)) in ("captain", "pick1", "pick2", "backup") else 0
                sel.append((rk, m, a, rs, lab))
            if len(sel) < 10 or len({s[4] for s in sel}) < 2:
                continue
            labs = [s[4] for s in sel]
            for name, idx, sign in (("qual_rank", 0, -1), ("avg_match", 1, 1),
                                    ("avg_auto", 2, 1), ("ranking_score", 3, 1)):
                v = auc([sign * s[idx] for s in sel], labs)
                if v is not None:
                    acc[name].append(v)
        for name, vs in acc.items():
            rows.append({"year": y, "predictor": name, "n_events": len(vs),
                         "median_auc_picked": round(statistics.median(vs), 3),
                         "p25": round(q(vs, .25), 3), "p75": round(q(vs, .75), 3)})
    return rows


def d_growth(data, years):
    """Paired within-team growth: teams that played an EARLY event (Wk1-2) and a
    LATE event (Wk4+) in the same season. Same robot, same team, so this removes
    the 'later events just have better teams' confound that ruins the raw
    week-by-week score curve."""
    rows = []
    EARLY = {"Week 1", "Week 2"}
    LATE = {"Week 4", "Week 5", "Week 6", "Week 7"}
    for y in years:
        events, teams, alli = load_year(data, y)
        per_team = defaultdict(dict)
        for (ev, tm), r in teams.items():
            wk = events.get(ev, {}).get("week")
            ac = autocol(r)
            m, a = num(r.get("Avg Match")), (num(r.get(ac)) if ac else None)
            rk, n = r.get("rank"), events.get(ev, {}).get("n_teams")
            if None in (m, rk, n) or not n:
                continue
            pct = 100.0 * (rk - 1) / max(1.0, n - 1)
            if wk in EARLY:
                per_team[tm].setdefault("early", []).append((m, a, pct))
            elif wk in LATE:
                per_team[tm].setdefault("late", []).append((m, a, pct))
        gm, ga, gp = [], [], []
        for tm, d in per_team.items():
            if "early" not in d or "late" not in d:
                continue
            e = d["early"][0]
            l = d["late"][-1]
            if e[0] > 0:
                gm.append(100.0 * (l[0] - e[0]) / e[0])
            if e[1] and l[1] and e[1] > 0:
                ga.append(100.0 * (l[1] - e[1]) / e[1])
            gp.append(l[2] - e[2])
        if not gm:
            continue
        rows.append({
            "year": y, "n_teams_early_and_late": len(gm),
            "median_pct_growth_avg_match": round(statistics.median(gm), 1),
            "median_pct_growth_avg_auto": round(statistics.median(ga), 1) if ga else None,
            "median_change_rank_pctile": round(statistics.median(gp), 1),
            "pct_teams_rank_pctile_improved": round(100 * sum(1 for x in gp if x < 0) / len(gp), 1),
        })
    return rows


def e_reliability(data, years):
    """What the public rankings screen can and cannot tell you about breakdowns."""
    rows = []
    for y in years:
        events, teams, alli = load_year(data, y)
        by_ev = defaultdict(list)
        for (ev, tm), r in teams.items():
            by_ev[ev].append((tm, r))
        dq_any = dq_tot = n = 0
        short = 0
        winpct_top, winpct_bot = [], []
        pct_dq, pct_clean = [], []
        picked_dq = picked_clean = n_dq = n_clean = 0
        for ev, pairs in by_ev.items():
            played = [num(r.get("Played")) for _, r in pairs if num(r.get("Played")) is not None]
            if not played:
                continue
            modal = statistics.mode(played)
            nt = len(pairs)
            for tm, r in pairs:
                n += 1
                d = num(r.get("DQ")) or 0
                dq_tot += d
                pct = 100.0 * (r["rank"] - 1) / max(1, nt - 1)
                on_alliance = alli.get((ev, tm)) in ("captain", "pick1", "pick2", "backup")
                if d > 0:
                    dq_any += 1
                    pct_dq.append(pct)
                    n_dq += 1
                    picked_dq += 1 if on_alliance else 0
                else:
                    pct_clean.append(pct)
                    n_clean += 1
                    picked_clean += 1 if on_alliance else 0
                p = num(r.get("Played"))
                if p is not None and p < modal:
                    short += 1
                rec = (r.get("Record (W-L-T)") or "").split("-")
                if len(rec) == 3:
                    try:
                        w, l, t = (int(x) for x in rec)
                        tot = w + l + t
                        if tot:
                            if pct <= 25:
                                winpct_top.append(100.0 * w / tot)
                            elif pct >= 75:
                                winpct_bot.append(100.0 * w / tot)
                    except ValueError:
                        pass
        rows.append({
            "year": y, "n_team_events": n,
            "pct_team_events_with_any_DQ": round(100 * dq_any / n, 2) if n else None,
            "mean_DQ_per_team_event": round(dq_tot / n, 3) if n else None,
            "pct_team_events_short_of_modal_played": round(100 * short / n, 2) if n else None,
            "median_winpct_top_quartile_rank": round(statistics.median(winpct_top), 1) if winpct_top else None,
            "median_winpct_bottom_quartile_rank": round(statistics.median(winpct_bot), 1) if winpct_bot else None,
            "median_rank_pctile_with_DQ": round(statistics.median(pct_dq), 1) if pct_dq else None,
            "median_rank_pctile_no_DQ": round(statistics.median(pct_clean), 1) if pct_clean else None,
            "pct_picked_with_DQ": round(100 * picked_dq / n_dq, 1) if n_dq else None,
            "pct_picked_no_DQ": round(100 * picked_clean / n_clean, 1) if n_clean else None,
        })
    return rows


def write_csv(path, rows):
    if not rows:
        return
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print("wrote", path, f"({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    tba = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "research", "predictive_tba")
    ap.add_argument("--data", default=tba)
    ap.add_argument("--out", default=tba)
    ap.add_argument("--years", nargs="*", type=int, default=list(YEARS))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    out = {}
    for name, fn in (("captaincy_base_rates", a_captaincy),
                     ("auto_within_event", b_auto),
                     ("pick_auc", c_pick_auc),
                     ("multi_event_growth", d_growth),
                     ("reliability", e_reliability)):
        rows = fn(a.data, a.years)
        out[name] = rows
        write_csv(os.path.join(a.out, f"pf4_{name}.csv"), rows)
    with open(os.path.join(a.out, "pf4_summary.json"), "w", encoding="utf-8") as f:
        json.dump({"source": "The Blue Alliance public event pages, scraped by "
                             "tools/tba_predictive_scrape.py", "tables": out}, f, indent=2)
    print("wrote", os.path.join(a.out, "pf4_summary.json"))


if __name__ == "__main__":
    main()
