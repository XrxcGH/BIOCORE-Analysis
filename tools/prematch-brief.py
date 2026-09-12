#!/usr/bin/env python3
"""
prematch-brief.py -- one index card per match, generated from public data + your gap scouting.

WHAT IT IS FOR
--------------
Between matches a drive team has about 90 seconds of attention. A dashboard is useless to them; a
spreadsheet is worse. What they can use is five lines: what to do differently, who not to collide
with, which single opposing robot decides the match, the fallback, and how confident we are.

This tool produces those five lines DETERMINISTICALLY from data, so the numbers are right, and
leaves a marked slot for the one judgement call a human must make. An LLM can then polish the
wording (analysis-prompts.md D1) -- but it must never be the thing that computes the numbers.

DATA
    research/predictive_tba/tba_copr_<year>.csv     mu per team (component OPR)
    research/predictive_tba/tba_resid_<year>.csv    sigma per team (match-to-match volatility)
    research/predictive_tba/tba_matches_<year>.csv  the schedule (and, post-hoc, results)
    OPTIONAL  --scouting <csv>   your 22-field gap data; any of:
              team,breakdown,defense_quality,driver_skill,known_weaknesses,notes

USAGE
    python tools/prematch-brief.py 2026 --event 2026mndu --us 3267 --match 12
    python tools/prematch-brief.py 2026 --event 2026mndu --us 3267 --all --sigma-scale 0.592
    python tools/prematch-brief.py 2026 --event 2026mndu --red 3100,2823,11223 \
           --blue 5348,2503,7797 --us 3100

Pure stdlib. Reads only local CSVs -- runs on venue wifi, or none.
"""
import argparse, csv, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ms = __import__("importlib").import_module("importlib.util")
_spec = _ms.spec_from_file_location("match_sim", os.path.join(HERE, "match-sim.py"))
match_sim = _ms.module_from_spec(_spec)
_spec.loader.exec_module(match_sim)

ROOT = os.path.dirname(HERE)


def load_scouting(path):
    """-> {team: {field: [values]}} from any CSV that has a `team` column."""
    out = {}
    if not path:
        return out
    if not os.path.exists(path):
        sys.exit("scouting file not found: %s" % path)
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            t = (row.get("team") or row.get("Team") or "").strip()
            if not t:
                continue
            d = out.setdefault(t, {})
            for k, v in row.items():
                if k and k.lower() != "team" and v not in (None, ""):
                    d.setdefault(k, []).append(v)
    return out


def scout_line(team, scout):
    """One clause from gap scouting, or an explicit statement that we have none."""
    d = scout.get(team)
    if not d:
        return "NO GAP-SCOUTING DATA -- public numbers only"
    bits = []
    for key, label in (("breakdown", "breakdown"), ("defense_quality", "def"),
                       ("driver_skill", "driver"), ("known_weaknesses", "weakness")):
        vals = d.get(key)
        if not vals:
            continue
        nums = []
        for v in vals:
            try:
                nums.append(float(v))
            except ValueError:
                pass
        if nums:
            bits.append("%s %.1f/%d" % (label, statistics.fmean(nums), len(nums)))
        else:
            bits.append("%s: %s" % (label, vals[-1][:40]))
    return "; ".join(bits) if bits else "scouted, no scored fields"


def brief(td, us, red, blue, scout, n, scale, match_label):
    ours = "RED" if us in red else "BLUE"
    allies = [t for t in (red if ours == "RED" else blue) if t != us]
    opps = blue if ours == "RED" else red
    R = [td[t] for t in red]
    B = [td[t] for t in blue]
    res = match_sim.simulate(R, B, n=n, seed=11, scale=scale)
    p_us = res["p_red"] if ours == "RED" else res["p_blue"]
    # the threat: highest mu on the opposing alliance
    threat = max(opps, key=lambda t: td[t]["mu"])
    # our alliance's biggest variance risk
    risk = max(red if ours == "RED" else blue, key=lambda t: td[t]["sigma"])

    L = []
    L.append("=" * 68)
    L.append("MATCH %-12s  us %s on %s        P(win) = %.2f" % (match_label, us, ours, p_us))
    L.append("=" * 68)
    L.append("ONE-LINE PLAN: ____________________________________  <- HUMAN WRITES THIS")
    for a in allies:
        L.append("PARTNER %-6s mu %6.1f  sigma %5.1f  | %s" % (a, td[a]["mu"], td[a]["sigma"], scout_line(a, scout)))
    L.append("THREAT  %-6s mu %6.1f  sigma %5.1f  | %s" % (threat, td[threat]["mu"], td[threat]["sigma"],
                                                           scout_line(threat, scout)))
    L.append("OUR RISK %-5s highest sigma on our alliance (%.1f) -- the match swings on this robot"
             % (risk, td[risk]["sigma"]))
    L.append("SCORE   us p10/p50/p90 %6.1f /%6.1f /%6.1f    them %6.1f /%6.1f /%6.1f"
             % ((res["red_p10"], res["red_p50"], res["red_p90"], res["blue_p10"], res["blue_p50"], res["blue_p90"])
                if ours == "RED" else
                (res["blue_p10"], res["blue_p50"], res["blue_p90"], res["red_p10"], res["red_p50"], res["red_p90"])))
    L.append("IF IT GOES WRONG: _________________________________  <- HUMAN WRITES THIS")
    L.append("CONFIDENCE: model knows scoring rate and volatility only. It does NOT know")
    L.append("            reliability, defense or driver skill. Trust your scouts over this line.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year")
    ap.add_argument("--event", required=True)
    ap.add_argument("--us", required=True)
    ap.add_argument("--match", help="qual match number from tba_matches_<year>.csv row order")
    ap.add_argument("--all", action="store_true", help="every match our team is in")
    ap.add_argument("--red"); ap.add_argument("--blue")
    ap.add_argument("--scouting", help="CSV of your gap-scouting data")
    ap.add_argument("--n", type=int, default=8000)
    ap.add_argument("--sigma-scale", type=float, default=1.0)
    a = ap.parse_args()

    teams, matches = match_sim.load(a.year, a.event)
    if a.event not in teams:
        sys.exit("no COPR data for event %s in year %s" % (a.event, a.year))
    td = teams[a.event]
    scout = load_scouting(a.scouting)

    if a.red and a.blue:
        red = [t.strip() for t in a.red.split(",")]
        blue = [t.strip() for t in a.blue.split(",")]
        for t in red + blue:
            if t not in td:
                sys.exit("team %s not at %s" % (t, a.event))
        print(brief(td, a.us, red, blue, scout, a.n, a.sigma_scale, "manual"))
        return

    ours = []
    for i, m in enumerate(matches, 1):
        red = [m["red1"], m["red2"], m["red3"]]
        blue = [m["blue1"], m["blue2"], m["blue3"]]
        if a.us in red + blue and all(t in td for t in red + blue):
            ours.append((i, red, blue))
    if not ours:
        sys.exit("team %s has no fully-resolvable matches at %s" % (a.us, a.event))
    sel = ours if a.all else [x for x in ours if not a.match or str(x[0]) == str(a.match)]
    if not sel:
        sel = ours[:1]
    for i, red, blue in sel:
        print(brief(td, a.us, red, blue, scout, a.n, a.sigma_scale, "#%d" % i))
        print()


if __name__ == "__main__":
    main()
