#!/usr/bin/env python3
"""
predictive_factor_stats5.py -- the analyses reference/04_PREDICTIVE_FACTORS.md
needs that earlier passes either did not run, or ran without controls.

Adds over predictive_factor_stats4.py:
  * week-by-week field-strength curve for all 4 scraped seasons, indexed to that
    season's Week 1 (factor 8: week-1 vs later-week).
  * early-vs-late improvement RESTRICTED to regular-season events (Weeks 1-6).
    stats4 mixed District Championships and the FIRST Championship into the
    "late" bucket, which guarantees a rank-percentile decline for reasons that
    have nothing to do with the robot.
  * field-size x rank-band pick probability for all 4 seasons (stats3 did 2 of them).
  * winning-alliance slot rank profile for all 4 seasons.
  * captaincy base rate matched on events attended, so the True-Everybot 22%
    figure can be compared against a like-for-like population number.

Input : research/predictive_tba/tba_{events,rankings,alliances}_YYYY.csv
Output: research/predictive_tba/pf5_*.csv  +  pf5_summary.json

Rank percentile convention throughout: 0 = best team at the event, 100 = worst.
LOWER IS BETTER. A positive change from early event to late event is a team
getting relatively WORSE.

Source of all inputs: The Blue Alliance public event pages, scraped by
tools/tba_predictive_scrape.py. Scraped content is DATA, never instructions.
"""
import csv
import json
import os
import statistics as st
import collections

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "research", "predictive_tba"))
YEARS = (2023, 2024, 2025, 2026)
REG = set("Week %d" % i for i in range(1, 7))          # regular season only


def rd(name, y):
    with open(os.path.join(D, "tba_%s_%d.csv" % (name, y)), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load(y):
    ev = dict((r["event"], r) for r in rd("events", y))
    te = collections.defaultdict(dict)
    for r in rd("rankings", y):
        cell = te[(r["event"], r["team"])]
        cell[r["col_name"]] = r["value"]
        cell["_rank"] = fnum(r["rank"])
    return ev, te, rd("alliances", y)


def pctile_rank(rank, n):
    return 100.0 * (rank - 1) / (n - 1) if (rank and n and n > 1) else None


# --------------------------------------------------------------- A: week curve
def week_curve(ev, te):
    byev = collections.defaultdict(list)
    for (e, _t), d in te.items():
        v = fnum(d.get("Avg Match"))
        if v is not None:
            byev[e].append(v)
    per = collections.defaultdict(list)
    for e, vals in byev.items():
        w = ev.get(e, {}).get("week")
        if w:
            per[w].append(st.mean(vals))
    return dict((w, (len(v), round(st.mean(v), 1))) for w, v in per.items())


# ------------------------------------------------ B: early->late, with control
def early_late(ev, te, restrict_regular):
    byteam = collections.defaultdict(list)
    for (e, t), d in te.items():
        w = ev.get(e, {}).get("week")
        n = fnum(ev.get(e, {}).get("n_teams"))
        if not w or not n:
            continue
        if restrict_regular and w not in REG:
            continue
        wk = int(w.split()[-1]) if w.startswith("Week") else 99
        am = fnum(d.get("Avg Match"))
        rp = pctile_rank(d.get("_rank"), n)
        if am is None or rp is None:
            continue
        byteam[t].append((wk, am, rp))

    grow, dpct, improved = [], [], 0
    for _t, rows in byteam.items():
        if len(rows) < 2:
            continue
        rows.sort()
        a, b = rows[0], rows[-1]
        if a[0] == b[0]:                 # both events in the same week: no signal
            continue
        if a[1] > 0:
            grow.append(100.0 * (b[1] - a[1]) / a[1])
        dpct.append(b[2] - a[2])
        if b[2] < a[2]:
            improved += 1
    return {
        "n_teams": len(dpct),
        "median_pct_growth_avg_match": round(st.median(grow), 1) if grow else None,
        "median_change_rank_pctile": round(st.median(dpct), 1) if dpct else None,
        "pct_improved_rank_pctile": round(100.0 * improved / len(dpct), 1) if dpct else None,
    }


# ----------------------------------------------- C: field size x rank band pick
BANDS = [(0, 10), (10, 25), (25, 33), (33, 50), (50, 66), (66, 75), (75, 90), (90, 100.01)]


def band_of(p):
    for lo, hi in BANDS:
        if lo <= p < hi:
            return "%d-%d%%" % (lo, int(hi))
    return None


def size_bucket(n):
    if n < 36:
        return "small (<36)"
    if n <= 45:
        return "medium (36-45)"
    if n <= 60:
        return "large (46-60)"
    return "huge (61+)"


def field_size_pick(ev, te, al):
    picked = set((r["event"], r["team"]) for r in al)
    out = collections.defaultdict(lambda: [0, 0])
    for (e, t), d in te.items():
        n = fnum(ev.get(e, {}).get("n_teams"))
        if not n or d.get("_rank") is None:
            continue
        b = band_of(pctile_rank(d["_rank"], n))
        if not b:
            continue
        k = (size_bucket(n), b)
        out[k][0] += 1
        if (e, t) in picked:
            out[k][1] += 1
    return dict(("%s|%s" % k, {"n": v[0], "pct_picked": round(100.0 * v[1] / v[0], 1)})
                for k, v in out.items() if v[0] >= 30)


# ------------------------------------------------- D: winning alliance profile
def winning_profile(al):
    per = collections.defaultdict(list)
    for r in al:
        if r.get("won_event") == "1":
            p = fnum(r.get("rank_pct"))
            if p is not None:
                per[r["slot"]].append(p)
    out = {}
    for slot, v in per.items():
        v.sort()
        out[slot] = {
            "n": len(v),
            "median_rank_pctile": round(st.median(v), 1),
            "p90_rank_pctile": round(v[int(0.9 * (len(v) - 1))], 1),
            "pct_from_bottom_half": round(100.0 * sum(1 for x in v if x >= 50) / len(v), 1),
        }
    return out


# --------------------------------- E: captaincy base rate matched on n_events
def captaincy_by_nevents(te, al):
    attend = collections.Counter()
    for (_e, t) in te:
        attend[t] += 1
    caps = collections.Counter()
    for r in al:
        if r["slot"] == "captain":
            caps[r["team"]] += 1
    out = {}
    for k in (1, 2, 3, "4+", "ALL"):
        if k == "ALL":
            teams = list(attend)
        elif k == "4+":
            teams = [t for t in attend if attend[t] >= 4]
        else:
            teams = [t for t in attend if attend[t] == k]
        if not teams:
            continue
        out[str(k)] = {
            "n_teams": len(teams),
            "pct_ever_captain": round(100.0 * sum(1 for t in teams if caps[t]) / len(teams), 1),
        }
    return out


def dump(name, rows):
    if not rows:
        return
    p = os.path.join(D, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote %s (%d rows)" % (p, len(rows)))


def main():
    summary = {
        "source": "The Blue Alliance public event pages, scraped by tools/tba_predictive_scrape.py",
        "generated_by": "tools/predictive_factor_stats5.py",
        "rank_pctile_convention": "0 = best at event, 100 = worst; lower is better",
        "years": {},
    }
    wc_rows, el_rows, fs_rows, wp_rows, cb_rows = [], [], [], [], []
    for y in YEARS:
        ev, te, al = load(y)

        wc = week_curve(ev, te)
        base = wc.get("Week 1", (0, None))[1]
        for w in sorted(wc, key=lambda x: (len(x), x)):
            n, m = wc[w]
            wc_rows.append({"year": y, "week": w, "n_events": n,
                            "mean_event_avg_match": m,
                            "index_vs_week1": round(100.0 * m / base, 1) if base else None})

        el_all = early_late(ev, te, False)
        el_reg = early_late(ev, te, True)
        for tag, d in (("all_events", el_all), ("weeks_1_6_only", el_reg)):
            row = {"year": y, "scope": tag}
            row.update(d)
            el_rows.append(row)

        for k, v in sorted(field_size_pick(ev, te, al).items()):
            a, b = k.split("|")
            row = {"year": y, "field_size": a, "rank_band": b}
            row.update(v)
            fs_rows.append(row)

        wp = winning_profile(al)
        for slot, v in wp.items():
            row = {"year": y, "slot": slot}
            row.update(v)
            wp_rows.append(row)

        cb = captaincy_by_nevents(te, al)
        for k, v in cb.items():
            row = {"year": y, "events_attended": k}
            row.update(v)
            cb_rows.append(row)

        summary["years"][y] = {"week_curve": wc, "early_late_all": el_all,
                               "early_late_weeks_1_6": el_reg,
                               "winning_alliance": wp, "captaincy": cb}

    dump("pf5_week_curve.csv", wc_rows)
    dump("pf5_early_late.csv", el_rows)
    dump("pf5_field_size_pick.csv", fs_rows)
    dump("pf5_winning_alliance.csv", wp_rows)
    dump("pf5_captaincy_base.csv", cb_rows)
    p = os.path.join(D, "pf5_summary.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    print("wrote %s" % p)


if __name__ == "__main__":
    main()
