#!/usr/bin/env python3
"""
score-priors.py -- DATA-GROUNDED priors for the kickoff cycle model.

WHY THIS EXISTS
---------------
The 2026 rehearsal fed `cycle-model.py` a hand-guessed median_alliance_score of 120.
The real 2026 number was 147.0 median / 182.7 mean across 30,352 alliance-scores that were
sitting in this repo the whole time. The graded verdict was blunt:

    "A cycle model that is never checked against a season of results is a rhetoric generator."

THE KICKOFF CONSTRAINT (read this before you use the output)
------------------------------------------------------------
On 2027-01-09 there is NO BIOCORE outcome data. Week 1 is ~8 weeks away. So the fix cannot be
"validate against this season". It is:

    1. DERIVE priors from prior seasons (2023-2026).
    2. STATE them as priors, with their spread, and let the spread size the uncertainty band.
    3. SCHEDULE the re-run for Week 1, when real 2027 rows exist.

A prior is not a measurement. If the cross-season spread is wide, the honest kickoff output is a
RANGE, not a number -- see `cycle-model.py --range`.

SOURCES (all local, all in-repo)
  research/predictive_tba/tba_matches_<year>.csv    alliance scores (red_score, blue_score)
  research/predictive_tba/tba_rankings_<year>.csv   per-team-event component averages
  research/predictive_tba/tba_alliances_<year>.csv  which teams were PICKED

USAGE
  python tools/score-priors.py distributions 2026
  python tools/score-priors.py priors
  python tools/score-priors.py endgame-check 2026
  python tools/score-priors.py endgame-check 2027     # the Week-1 re-run, once data exists

Pure stdlib. No dependencies.
"""
import sys, os, csv, math, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TBA  = os.path.join(ROOT, "research", "predictive_tba")

SEASONS = [2023, 2024, 2025, 2026]

# TBA ranking column names are game-specific. This map IS the game-to-column binding; when
# 2027 data lands, add the BIOCORE row and nothing else in this file changes.
AUTO_COL = {
    2023: "Avg Auto",       2024: "Avg Auto",
    2025: "Avg Auto",       2026: "Avg Auto Fuel",
}
END_COL = {
    2023: "Avg Charge Station",  # CHARGED UP  docking/engaging
    2024: "Avg Stage",           # CRESCENDO   onstage/trap
    2025: "Avg Barge",           # REEFSCAPE   cage climb
    2026: "Avg Tower",           # REBUILT     tower climb
}
GAME = {2023: "CHARGED UP", 2024: "CRESCENDO", 2025: "REEFSCAPE", 2026: "REBUILT"}

# Unit caveats that must travel with the numbers.
UNIT_NOTE = {
    2026: "2026 'Avg Auto Fuel' is a FUEL COUNT, not a point total. REBUILT scores 1 pt/FUEL "
          "so count ~= points, but treat the 2026 AUTO share as APPROXIMATE.",
}


def path(kind, year):
    p = os.path.join(TBA, "tba_%s_%d.csv" % (kind, year))
    if not os.path.exists(p):
        sys.exit("NO DATA: %s\n  -> for a future season this is expected; the priors are all you "
                 "have until Week 1. Re-run this command once TBA has %d rows." % (p, year))
    return p


def alliance_scores(year):
    out = []
    with open(path("matches", year), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            for k in ("red_score", "blue_score"):
                v = (r.get(k) or "").strip()
                if v not in ("", "-1", "None"):
                    try:
                        out.append(float(v))
                    except ValueError:
                        pass
    return out


def rankings(year):
    """{(event, team): {col_name: value}} for the numeric columns we care about."""
    want = set([c for c in ("Avg Match", AUTO_COL.get(year), END_COL.get(year)) if c])
    rows = {}
    with open(path("rankings", year), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            cn = r["col_name"]
            if cn not in want:
                continue
            try:
                v = float(r["value"])
            except (ValueError, TypeError):
                continue
            rows.setdefault((r["event"], r["team"]), {})[cn] = v
    return rows


def picked_set(year):
    s = set()
    with open(path("alliances", year), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            s.add((r["event"], r["team"]))
    return s


def pct(vals, q):
    if not vals:
        return float("nan")
    v = sorted(vals)
    i = (len(v) - 1) * q
    lo, hi = math.floor(i), math.ceil(i)
    return v[lo] if lo == hi else v[lo] + (v[hi] - v[lo]) * (i - lo)


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def corr(xs, ys):
    if len(xs) < 3:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return float("nan")
    return sxy / math.sqrt(sxx * syy)


# ------------------------------------------------------------------ 1. distributions
def season_stats(year):
    sc = alliance_scores(year)
    rk = rankings(year)
    ac, ec = AUTO_COL.get(year), END_COL.get(year)
    match_v = [d["Avg Match"] for d in rk.values() if "Avg Match" in d]
    auto_v  = [d[ac] for d in rk.values() if ac in d]
    end_v   = [d[ec] for d in rk.values() if ec in d]
    m_mean = mean(match_v)
    return {
        "year": year, "game": GAME.get(year, "?"),
        "n_scores": len(sc), "n_teamevents": len(rk),
        "median": pct(sc, .50), "mean": mean(sc),
        "p10": pct(sc, .10), "p50": pct(sc, .50), "p90": pct(sc, .90),
        "auto_col": ac, "end_col": ec,
        "auto_mean": mean(auto_v), "end_mean": mean(end_v), "match_mean": m_mean,
        "auto_share": mean(auto_v) / m_mean if m_mean else float("nan"),
        "end_share":  mean(end_v)  / m_mean if m_mean else float("nan"),
        "end_zero_pct": 100.0 * sum(1 for v in end_v if v == 0) / len(end_v) if end_v else float("nan"),
    }


def cmd_distributions(year):
    s = season_stats(year)
    print("\n=== ALLIANCE-SCORE DISTRIBUTION -- %d %s ===" % (s["year"], s["game"]))
    print("  source: research/predictive_tba/tba_matches_%d.csv  (n = %s alliance-scores)"
          % (year, format(s["n_scores"], ",")))
    print("    median alliance score   %8.1f" % s["median"])
    print("    mean   alliance score   %8.1f" % s["mean"])
    print("    p10 / p50 / p90         %8.1f / %.1f / %.1f" % (s["p10"], s["p50"], s["p90"]))
    if s["p10"]:
        print("    p90/p10 spread          %8.2fx" % (s["p90"] / s["p10"]))
    print("\n  COMPONENT SHARES -- source: tba_rankings_%d.csv  (n = %s team-events)"
          % (year, format(s["n_teamevents"], ",")))
    print("    method: mean(component) / mean('Avg Match') over the same population;")
    print("            NOT a per-row ratio, so low-scoring rows cannot blow the denominator up.")
    print("    mean Avg Match          %8.2f" % s["match_mean"])
    print("    AUTO    '%s'  mean %.2f  ->  share %5.1f %%"
          % (s["auto_col"], s["auto_mean"], 100 * s["auto_share"]))
    print("    ENDGAME '%s'  mean %.2f  ->  share %5.1f %%"
          % (s["end_col"], s["end_mean"], 100 * s["end_share"]))
    print("    team-events with ZERO endgame points: %.1f %%" % s["end_zero_pct"])
    if year in UNIT_NOTE:
        print("\n  [!] UNIT CAVEAT: %s" % UNIT_NOTE[year])
    print("")
    return s


# ------------------------------------------------------------------ 2. priors
def cmd_priors():
    stats = [season_stats(y) for y in SEASONS]
    print("\n=== KICKOFF PRIORS -- adopt these BEFORE any 2027 data exists ===")
    print("  These are PRIORS from 4 prior seasons, not measurements of BIOCORE.")
    print("  On kickoff day there is no 2027 outcome data and Week 1 is ~8 weeks out.")
    print("  Every number below is a starting belief to be REPLACED at Week 1, not a finding.\n")
    print("  %-5s%-11s%8s%8s%7s%7s%8s%7s  %s"
          % ("yr", "game", "median", "mean", "p10", "p90", "AUTO%", "END%", "endgame column"))
    print("  " + "-" * 86)
    for s in stats:
        print("  %-5d%-11s%8.1f%8.1f%7.0f%7.0f%8.1f%7.1f  %s"
              % (s["year"], s["game"], s["median"], s["mean"], s["p10"], s["p90"],
                 100 * s["auto_share"], 100 * s["end_share"], s["end_col"]))

    def band(key, scale=1.0):
        v = [s[key] * scale for s in stats]
        lo, hi, mu = min(v), max(v), mean(v)
        return lo, pct(v, .5), hi, mu, ((hi - lo) / mu if mu else float("nan"))

    print("\n  --- PRIOR 1: median alliance score ---")
    lo, med, hi, mu, rng = band("median")
    print("    historical range   %.0f .. %.0f     median-of-medians %.0f   mean %.0f"
          % (lo, hi, med, mu))
    print("    season-to-season movement: %.0f pts = %.0f %% of the mean" % (hi - lo, 100 * rng))
    print("    trajectory: " + "  ->  ".join("%d:%.0f" % (s["year"], s["median"]) for s in stats))
    print("    ADOPT AS: low %.0f / likely %.0f / high %.0f  -- a BAND, not a point estimate."
          % (lo, med, hi))
    print("    (The rehearsal's guess of 120 sits BELOW this entire 4-season range.)")

    print("\n  --- PRIOR 2: AUTO share of alliance score ---")
    alo, amed, ahi, amu, arng = band("auto_share", 100.0)
    print("    historical range   %.1f %% .. %.1f %%   typical (median) %.1f %%   mean %.1f %%"
          % (alo, ahi, amed, amu))
    print("    season-to-season movement: %.1f pp = %.0f %% of the mean" % (ahi - alo, 100 * arng))
    print("    trajectory: " + "  ->  ".join("%d:%.1f%%" % (s["year"], 100 * s["auto_share"])
                                             for s in stats))
    print("    ADOPT AS: AUTO is worth roughly %.0f-%.0f %% of a match. In 4 seasons it has NEVER"
          % (alo, ahi))
    print("    been negligible. An AUTO workstream is the safest prior-backed bet on the board.")

    print("\n  --- PRIOR 3: ENDGAME share of alliance score ---")
    elo, emed, ehi, emu, erng = band("end_share", 100.0)
    print("    historical range   %.1f %% .. %.1f %%   typical (median) %.1f %%   mean %.1f %%"
          % (elo, ehi, emed, emu))
    print("    season-to-season movement: %.1f pp = %.0f %% of the mean  <-- the WIDEST prior"
          % (ehi - elo, 100 * erng))
    print("    trajectory: " + "  ->  ".join("%d:%.1f%%" % (s["year"], 100 * s["end_share"])
                                             for s in stats))
    print("    ADOPT AS: NOTHING. A %.0fx swing across 4 seasons means the endgame share is simply"
          % (ehi / elo if elo else float("nan")))
    print("    NOT PREDICTABLE from priors. Endgame value is a GAME-SPECIFIC question every season.")
    print("    Do not assume the 2027 endgame matters, and do not assume it does not.")
    print("    Resolve it with `endgame-check 2027` at Week 1 -- never with a kickoff guess.")

    print("\n  --- HOW STRONG ARE THESE PRIORS? (spread / mean) ---")
    for name, r in (("median alliance score", rng), ("AUTO share", arng), ("ENDGAME share", erng)):
        verdict = ("STRONG (narrow) -- a point estimate is defensible" if r < .25 else
                   "MODERATE -- report a band" if r < .60 else
                   "WEAK (wide) -- MUST be reported as a RANGE, never a number")
        print("    %-24s %5.0f %%   -> %s" % (name, 100 * r, verdict))
    print("\n  RULE: a WEAK prior must never be presented as a point estimate. Feed the")
    print("  low/likely/high band into `cycle-model.py --range` and report the band. CLAUDE.md Step 4.")
    print("\n  *** RE-RUN CHECKPOINT -- AFTER WEEK 1 OF THE 2027 SEASON ***")
    print("      1. add 2027 to SEASONS, AUTO_COL and END_COL at the top of this file")
    print("      2. python tools/score-priors.py distributions 2027")
    print("      3. python tools/score-priors.py endgame-check 2027")
    print("      4. REPLACE every prior above with the measured 2027 value, re-run cycle-model")
    print("         WITHOUT --range, and re-rank BEFORE the first pick list is built.\n")
    return stats


# ------------------------------------------------------------------ 3. endgame-check
def cmd_endgame_check(year):
    ec, ac = END_COL.get(year), AUTO_COL.get(year)
    if ec is None or ac is None:
        sys.exit("NO COLUMN MAP for %d. Add the season's endgame/AUTO ranking column names to "
                 "END_COL / AUTO_COL at the top of this file, then re-run." % year)
    rk = rankings(year)
    pk = picked_set(year)
    keys = [k for k, d in rk.items() if ec in d and "Avg Match" in d and ac in d]
    if not keys:
        sys.exit("No rows for %d with all three columns. Check the column map." % year)
    end    = [rk[k][ec] for k in keys]
    match  = [rk[k]["Avg Match"] for k in keys]
    auto   = [rk[k][ac] for k in keys]
    picked = [1.0 if k in pk else 0.0 for k in keys]

    print("\n=== ENDGAME REALITY CHECK -- %d %s ===" % (year, GAME.get(year, "?")))
    print("  THE CHECK THE 2026 REHEARSAL SKIPPED. It made the endgame the spine of its")
    print("  recommendation in a season where the endgame correlated 0.003 with match score.\n")
    print("  METHOD (re-runnable verbatim on 2027 at Week 1):")
    print("    population : every team-event row in tba_rankings_%d.csv carrying all three columns" % year)
    print("    endgame    : '%s'" % ec)
    print("    AUTO       : '%s'" % ac)
    print("    outcome    : 'Avg Match'  (the alliance score the team averaged)")
    print("    picked     : (event, team) appears in tba_alliances_%d.csv = selected to an alliance" % year)
    print("    statistic  : Pearson r, unweighted, one row per team-event")
    print("    n          : %s team-events   (%s picked = %.1f %%)"
          % (format(len(keys), ","), format(int(sum(picked)), ","), 100 * mean(picked)))
    print("")

    r_em, r_ep = corr(end, match), corr(end, picked)
    r_am, r_ap = corr(auto, match), corr(auto, picked)
    r_mp = corr(match, picked)
    m_mean = mean(match)
    share = mean(end) / m_mean if m_mean else float("nan")

    print("  %-34s%16s%14s" % ("signal", "r vs Avg Match", "r vs picked"))
    print("  " + "-" * 64)
    print("  %-34s%16.3f%14.3f" % ("ENDGAME  " + ec, r_em, r_ep))
    print("  %-34s%16.3f%14.3f" % ("AUTO     " + ac, r_am, r_ap))
    print("  %-34s%16s%14.3f" % ("Avg Match (benchmark)", "--", r_mp))
    print("\n  endgame share of alliance score : %.1f %%  (mean %s %.2f / mean Avg Match %.2f)"
          % (100 * share, ec, mean(end), m_mean))
    print("  team-events scoring ZERO endgame : %.1f %%"
          % (100.0 * sum(1 for v in end if v == 0) / len(end)))

    print("\n  VERDICT:")
    if abs(r_em) < 0.05 and share < 0.03:
        print("    ENDGAME IS NOT LOAD-BEARING in %d. r=%.3f against match score is" % (year, r_em))
        print("    indistinguishable from zero and it is %.1f %% of all scoring." % (100 * share))
        print("    DO NOT put an endgame mechanism in BUILD THIS on this evidence.")
    elif abs(r_em) < 0.15:
        print("    WEAK. r=%.3f, %.1f %% of scoring. A second-pick differentiator at best;"
              % (r_em, 100 * share))
        print("    not a reason to spend a workstream.")
    else:
        print("    LOAD-BEARING. r=%.3f, %.1f %% of scoring. Worth a workstream."
              % (r_em, 100 * share))
    if abs(r_ap) > abs(r_ep):
        print("    AUTO out-predicts ENDGAME on pick rate (%.3f vs %.3f). Rank AUTO above ENDGAME."
              % (r_ap, r_ep))
    if abs(r_am) > 0.90:
        print("    [!] AUTO r vs Avg Match = %.3f is implausibly high for an independent signal."
              % r_am)
        print("        Most likely '%s' and 'Avg Match' share the same underlying" % ac)
        print("        scoring element, so the AUTO column is partly INSIDE the outcome column.")
        print("        Treat the AUTO-vs-match figure as CONTAMINATED; the AUTO-vs-picked figure")
        print("        (%.3f) is the one to trust, and it is the honest comparison to endgame."
              % r_ap)
    print("    CAUTION: r is association, not causation, and 'picked' is a scouting-committee")
    print("    decision, not a measure of value. Use this to VETO an over-weighted channel, not")
    print("    to size one.")
    print("")
    return {"r_end_match": r_em, "r_end_picked": r_ep, "share": share, "n": len(keys)}


def main():
    ap = argparse.ArgumentParser(description="Data-grounded priors for the kickoff cycle model.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("distributions", help="per-season alliance score + component shares")
    d.add_argument("year", type=int)
    sub.add_parser("priors", help="cross-season kickoff priors, with spread")
    e = sub.add_parser("endgame-check", help="is the endgame load-bearing? corr vs match + picked")
    e.add_argument("year", type=int)
    a = ap.parse_args()
    if a.cmd == "distributions":
        cmd_distributions(a.year)
    elif a.cmd == "priors":
        cmd_priors()
    else:
        cmd_endgame_check(a.year)


if __name__ == "__main__":
    main()
