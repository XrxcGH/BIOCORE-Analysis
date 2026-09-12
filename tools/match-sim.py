#!/usr/bin/env python3
"""
match-sim.py -- Monte Carlo FRC match simulator, calibrated on real data.

WHY THIS EXISTS
---------------
"Team EPAs" alone give a point estimate. A point estimate cannot answer the two questions
that actually decide an alliance-selection room:
    1. What is the PROBABILITY this alliance beats that one?  (not "by how many points")
    2. Which single pick moves that probability most?          (the marginal-value question)
Both require a distribution, which requires a variance model, which requires calibration.

THE MODEL
---------
    alliance_score = sum_over_3_members( mu_i + Normal(0, sigma_i) ) + Normal(0, sigma_shared)

  mu_i     = team i's expected point contribution      -> COPR/OPR (or Statbotics EPA)
  sigma_i  = team i's match-to-match volatility        -> per-team residual SD (tba_resid_*.csv)
  sigma_shared = alliance-level noise the per-team terms miss (fouls, field faults, defense
             interactions). Fitted by `calibrate` so simulated margin SD matches observed.

The per-team sigma is the whole point. Two robots with the same 60-point average are NOT the
same pick if one has sigma=12 and the other sigma=45. Free FMS data (SCOUTING-PLAN.md sec 1)
gives you mu. It does not give you sigma. This tool derives sigma from public match results.

DATA (already in this repo -- no API key, no network)
    research/predictive_tba/tba_copr_<year>.csv     team, opr, auto, teleop, endgame, foul, rp
    research/predictive_tba/tba_resid_<year>.csv    team, n_matches, resid_mean, resid_sd, resid_min
    research/predictive_tba/tba_matches_<year>.csv  red1..3, blue1..3, red_score, blue_score
Refresh with:  python tools/tba_copr_scrape.py 2027 --out research/predictive_tba/

USAGE
  python tools/match-sim.py calibrate 2026
  python tools/match-sim.py backtest  2026 --event 2026mndu --n 400
  python tools/match-sim.py sim 2026 --event 2026mndu --red 3100,3267,7797 --blue 2264,2470,4009
  python tools/match-sim.py marginal 2026 --event 2026mndu --us 3100 --partner 3267 \
         --candidates 7797,2264,2470 --field-sample 40

Pure stdlib. Python 3.9+.
"""
import argparse, csv, math, os, random, statistics, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBA = os.path.join(ROOT, "research", "predictive_tba")


# ------------------------------------------------------------------ data loading
def _rows(path):
    if not os.path.exists(path):
        sys.exit("MISSING: %s\n  run: python tools/tba_copr_scrape.py <year> --out research/predictive_tba/" % path)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def load(year, event=None):
    """-> teams[event][team] = {mu, sigma, auto, endgame, foul, rp, n}, matches[]"""
    teams = collections.defaultdict(dict)
    for r in _rows(os.path.join(TBA, "tba_copr_%s.csv" % year)):
        if event and r["event"] != event:
            continue
        teams[r["event"]][r["team"]] = {
            "mu": _f(r.get("opr")), "auto": _f(r.get("auto")), "endgame": _f(r.get("endgame")),
            "foul": _f(r.get("foul")), "rp": _f(r.get("rp")), "sigma": None, "n": 0,
        }
    for r in _rows(os.path.join(TBA, "tba_resid_%s.csv" % year)):
        t = teams.get(r["event"], {}).get(r["team"])
        if t:
            t["sigma"] = _f(r.get("resid_sd"))
            t["n"] = int(_f(r.get("n_matches")))
    matches = [r for r in _rows(os.path.join(TBA, "tba_matches_%s.csv" % year))
               if (not event or r["event"] == event)]
    # median sigma per event backfills teams with no residual row (played too few matches)
    for ev, td in teams.items():
        known = [t["sigma"] for t in td.values() if t["sigma"]]
        med = statistics.median(known) if known else 25.0
        for t in td.values():
            if not t["sigma"]:
                t["sigma"] = med
    return teams, matches


# ------------------------------------------------------------------ core simulation
def draw(members, rng, shared=0.0, scale=1.0):
    s = 0.0
    for m in members:
        s += m["mu"] + rng.gauss(0.0, m["sigma"] * scale)
    if shared:
        s += rng.gauss(0.0, shared)
    return max(0.0, s)


def simulate(red, blue, n=10000, shared=0.0, seed=0, rp_thresholds=None, scale=1.0):
    rng = random.Random(seed)
    rw = bw = tie = 0
    rs, bs, marg = [], [], []
    rp_hits = collections.Counter()
    for _ in range(n):
        r = draw(red, rng, shared, scale)
        b = draw(blue, rng, shared, scale)
        rs.append(r); bs.append(b); marg.append(r - b)
        if r > b:
            rw += 1
        elif b > r:
            bw += 1
        else:
            tie += 1
        for name, thr in (rp_thresholds or {}).items():
            if r >= thr:
                rp_hits[name] += 1
    q = lambda xs, p: sorted(xs)[min(len(xs) - 1, int(p * len(xs)))]
    return {
        "p_red": rw / n, "p_blue": bw / n, "p_tie": tie / n, "n": n,
        "red_mean": statistics.fmean(rs), "blue_mean": statistics.fmean(bs),
        "red_p10": q(rs, .10), "red_p50": q(rs, .50), "red_p90": q(rs, .90),
        "blue_p10": q(bs, .10), "blue_p50": q(bs, .50), "blue_p90": q(bs, .90),
        "margin_mean": statistics.fmean(marg), "margin_sd": statistics.pstdev(marg),
        "rp": {k: v / n for k, v in rp_hits.items()},
    }


# ------------------------------------------------------------------ commands
def cmd_calibrate(a):
    teams, matches = load(a.year, a.event)
    obs_margin, pred_margin, model_sd, used = [], [], [], 0
    for m in matches:
        ev = m["event"]
        R = [teams[ev].get(m["red%d" % i]) for i in (1, 2, 3)]
        B = [teams[ev].get(m["blue%d" % i]) for i in (1, 2, 3)]
        if any(x is None for x in R + B):
            continue
        used += 1
        obs_margin.append(_f(m["red_score"]) - _f(m["blue_score"]))
        pred_margin.append(sum(x["mu"] for x in R) - sum(x["mu"] for x in B))
        model_sd.append(math.sqrt(sum(x["sigma"] ** 2 for x in R + B)))
    if not used:
        sys.exit("no usable matches")
    err = [o - p for o, p in zip(obs_margin, pred_margin)]
    obs_sd = statistics.pstdev(err)
    mdl_sd = statistics.fmean(model_sd)
    scale = obs_sd / mdl_sd if mdl_sd else 1.0
    gap = obs_sd ** 2 - mdl_sd ** 2
    shared = math.sqrt(gap / 2.0) if gap > 0 else 0.0
    print("CALIBRATION  year=%s  event=%s  matches used=%d" % (a.year, a.event or "ALL", used))
    print("  observed  margin-error SD    : %8.2f pts" % obs_sd)
    print("  model     margin SD (raw)    : %8.2f pts   (sqrt of summed per-team resid_sd^2)" % mdl_sd)
    print("  mean |margin error|          : %8.2f pts" % statistics.fmean([abs(e) for e in err]))
    print("  fitted SIGMA SCALE           : %8.3f       --> pass  --sigma-scale %.3f" % (scale, scale))
    print("  residual SHARED noise        : %8.2f pts   --> pass  --shared %.1f" % (shared, shared))
    if scale < 0.95:
        print("  WHY < 1: tba_resid_*.csv resid_sd is an ALLIANCE-level residual replicated onto")
        print("        each of the 3 members, so summing 6 of them in quadrature over-disperses by")
        print("        ~sqrt(3) = 1.732 (1/1.732 = 0.577). The fitted scale recovers the truth from")
        print("        data instead of assuming it. ALWAYS pass --sigma-scale; the raw model is wrong.")


def cmd_sim(a):
    teams, _ = load(a.year, a.event)
    ev = a.event or next(iter(teams))
    td = teams[ev]

    def pick(spec):
        out = []
        for t in spec.split(","):
            t = t.strip()
            if t not in td:
                sys.exit("team %s not at event %s" % (t, ev))
            td[t]["_team"] = t
            out.append(td[t])
        return out

    R, B = pick(a.red), pick(a.blue)
    thr = {}
    for spec in (a.rp_threshold or []):
        k, v = spec.split("=", 1)
        thr[k] = float(v)
    res = simulate(R, B, n=a.n, shared=a.shared, seed=a.seed, rp_thresholds=thr, scale=a.sigma_scale)
    print("MONTE CARLO  %s   n=%d   sigma_scale=%.3f  shared=%.1f" % (ev, res["n"], a.sigma_scale, a.shared))
    print("  %-5s %-24s %8s %8s" % ("", "teams", "sum mu", "sd"))
    for lbl, side in (("RED", R), ("BLUE", B)):
        print("  %-5s %-24s %8.1f %8.1f" % (lbl, ",".join(x["_team"] for x in side),
              sum(x["mu"] for x in side), a.sigma_scale * math.sqrt(sum(x["sigma"] ** 2 for x in side))))
    print("  RED  score  p10/p50/p90 : %7.1f %7.1f %7.1f" % (res["red_p10"], res["red_p50"], res["red_p90"]))
    print("  BLUE score  p10/p50/p90 : %7.1f %7.1f %7.1f" % (res["blue_p10"], res["blue_p50"], res["blue_p90"]))
    print("  margin  mean %+.1f   SD %.1f" % (res["margin_mean"], res["margin_sd"]))
    print("  P(RED win) = %.3f    P(BLUE win) = %.3f    P(tie) = %.3f"
          % (res["p_red"], res["p_blue"], res["p_tie"]))
    for k, v in sorted(res["rp"].items()):
        print("  P(RED %s) = %.3f" % (k, v))


def cmd_backtest(a):
    """Does the distribution beat the point estimate? Accuracy + Brier + calibration curve."""
    teams, matches = load(a.year, a.event)
    seed = 0
    hit_pt = hit_mc = n = 0
    brier_mc = brier_flat = 0.0
    bins = collections.defaultdict(lambda: [0, 0])
    for m in matches:
        ev = m["event"]
        R = [teams[ev].get(m["red%d" % i]) for i in (1, 2, 3)]
        B = [teams[ev].get(m["blue%d" % i]) for i in (1, 2, 3)]
        if any(x is None for x in R + B):
            continue
        rs, bs = _f(m["red_score"]), _f(m["blue_score"])
        if rs == bs:
            continue
        n += 1; seed += 1
        red_won = 1.0 if rs > bs else 0.0
        if (sum(x["mu"] for x in R) > sum(x["mu"] for x in B)) == (red_won == 1.0):
            hit_pt += 1
        p = simulate(R, B, n=a.n, shared=a.shared, seed=seed, scale=a.sigma_scale)["p_red"]
        if (p > 0.5) == (red_won == 1.0):
            hit_mc += 1
        brier_mc += (p - red_won) ** 2
        brier_flat += (0.5 - red_won) ** 2
        k = round(min(0.95, max(0.05, p)) * 10) / 10
        bins[k][0] += 1; bins[k][1] += red_won
    if not n:
        sys.exit("no decided matches")
    print("BACKTEST  year=%s  event=%s  decided=%d  sims/match=%d  sigma_scale=%.3f  shared=%.1f"
          % (a.year, a.event or "ALL", n, a.n, a.sigma_scale, a.shared))
    print("  point-estimate accuracy (higher COPR sum wins) : %.4f" % (hit_pt / n))
    print("  Monte-Carlo  accuracy (p_red > 0.5)            : %.4f" % (hit_mc / n))
    print("  Brier score  Monte Carlo                       : %.4f   (lower is better)" % (brier_mc / n))
    print("  Brier score  always-0.5 baseline               : %.4f" % (brier_flat / n))
    print("  CALIBRATION CURVE  (predicted -> observed red win rate)")
    for k in sorted(bins):
        cnt, won = bins[k]
        if cnt >= 10:
            print("    p~%.1f   n=%5d   observed %.3f   %s" % (k, cnt, won / cnt,
                  "OK" if abs(won / cnt - k) < 0.10 else "MISCALIBRATED"))


def cmd_marginal(a):
    """Which candidate 3rd pick raises P(win) most, averaged over plausible opponents?"""
    teams, _ = load(a.year, a.event)
    ev = a.event or next(iter(teams))
    td = teams[ev]
    for t in [a.us, a.partner] + a.candidates.split(","):
        if t.strip() not in td:
            sys.exit("team %s not at event %s" % (t.strip(), ev))
    base = [td[a.us], td[a.partner]]
    pool = sorted(td.items(), key=lambda kv: -kv[1]["mu"])[:a.field_sample]
    rng = random.Random(a.seed)
    opp_sets = [[kv[1] for kv in rng.sample(pool, 3)] for _ in range(a.opponents)]
    rows = []
    for cand in [c.strip() for c in a.candidates.split(",")]:
        ps = [simulate(base + [td[cand]], opp, n=a.n, shared=a.shared, seed=a.seed + i,
                       scale=a.sigma_scale)["p_red"]
              for i, opp in enumerate(opp_sets)]
        rows.append((cand, statistics.fmean(ps), td[cand]["mu"], td[cand]["sigma"], td[cand]["endgame"]))
    rows.sort(key=lambda r: -r[1])
    print("MARGINAL PICK VALUE  %s   us=%s partner=%s   vs %d random top-%d opponent alliances"
          % (ev, a.us, a.partner, a.opponents, a.field_sample))
    print("  %-8s %11s %9s %9s %9s" % ("cand", "mean P(win)", "mu", "sigma", "endgame"))
    for c, p, mu, sd, eg in rows:
        print("  %-8s %11.3f %9.1f %9.1f %9.2f" % (c, p, mu, sd, eg))
    if len(rows) > 1:
        print("  spread, best vs worst candidate: %+.3f win probability" % (rows[0][1] - rows[-1][1]))
    print("  NOTE: mu / sigma / endgame are PUBLIC data. Reliability, defense and driver skill")
    print("        are NOT in this model. Fuse with the 22 gap fields (SCOUTING-PLAN.md sec 3).")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("year")
        p.add_argument("--event")
        p.add_argument("--n", type=int, default=4000)
        p.add_argument("--shared", type=float, default=0.0)
        p.add_argument("--sigma-scale", type=float, default=1.0,
                       help="multiplier on every per-team sigma; get it from `calibrate`")
        p.add_argument("--seed", type=int, default=7)

    c = sub.add_parser("calibrate"); common(c); c.set_defaults(fn=cmd_calibrate)
    s = sub.add_parser("sim"); common(s)
    s.add_argument("--red", required=True)
    s.add_argument("--blue", required=True)
    s.add_argument("--rp-threshold", action="append",
                   help='e.g. --rp-threshold "AUTO_RP=45" (repeatable)')
    s.set_defaults(fn=cmd_sim)
    b = sub.add_parser("backtest"); common(b); b.set_defaults(fn=cmd_backtest)
    m = sub.add_parser("marginal"); common(m)
    m.add_argument("--us", required=True)
    m.add_argument("--partner", required=True)
    m.add_argument("--candidates", required=True)
    m.add_argument("--field-sample", type=int, default=24)
    m.add_argument("--opponents", type=int, default=30)
    m.set_defaults(fn=cmd_marginal)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
