#!/usr/bin/env python3
"""
cycle-model.py -- game-agnostic cycle-time / expected-value model for an FRC season.

WHY THIS EXISTS
---------------
On kickoff day the question is never "what scores the most points?" It is:

    Given OUR cycle time, how many points does each strategy actually produce in 150 seconds,
    and what does a fixed-value action (a climb, an endgame task) cost us in forgone cycles?

Teams answer this with vibes and pick the flashy mechanism. It is arithmetic. A LEVEL 3 climb
worth 30 points is only worth building if it costs less than 30 points of cycles -- and that
depends entirely on YOUR cycle time, which is a property of your team, not of the game.

The model is deliberately game-agnostic: you describe the season in a small YAML/JSON file and
it does the rest. `--game rebuilt` runs the built-in 2026 REBUILT definition as a worked,
validated example so you can see the shape before BIOCORE exists.

USAGE
  python tools/cycle-model.py --game rebuilt
  python tools/cycle-model.py --game rebuilt --cycle 9 --auto-scored 4
  python tools/cycle-model.py --game rebuilt --sweep            # cycle-time sensitivity table
  python tools/cycle-model.py --game mygame.json                # your own season

GAME FILE SCHEMA (JSON)
  {
    "name": "...",
    "auto_s": 20, "teleop_s": 140, "endgame_s": 30,
    "cycle_actions": [ {"name":"FUEL","points_auto":1,"points_teleop":1,"per_cycle":5} ],
    "fixed_actions":  [ {"name":"Climb L3","points":30,"time_s":12,"phase":"endgame"} ],
    "rp": [ {"name":"ENERGIZED","metric":"FUEL","threshold":100} ]
  }

Pure stdlib. No dependencies.
"""
import sys, json, re, argparse, os

# ---------------------------------------------------------------- built-in worked example
# 2026 REBUILT, from the manual: Table 6-4 point values, Table 6-5 BONUS RP thresholds,
# Table 5-4 audio cues (AUTO 0:20; TELEOP+TRANSITION 2:20; END GAME 0:30).
# Verified against manuals/archive/frc/2026_REBUILT_GameManual.pdf s6.5.3.
REBUILT = {
    "name": "REBUILT (2026)",
    "auto_s": 20, "teleop_s": 140, "endgame_s": 30,
    "cycle_actions": [
        {"name": "FUEL -> active HUB", "points_auto": 1, "points_teleop": 1, "per_cycle": 5},
    ],
    "fixed_actions": [
        {"name": "TOWER L1 (AUTO)",    "points": 15, "time_s": 4,  "phase": "auto"},
        {"name": "TOWER L1 (TELEOP)",  "points": 10, "time_s": 8,  "phase": "endgame"},
        {"name": "TOWER L2 (TELEOP)",  "points": 20, "time_s": 12, "phase": "endgame"},
        {"name": "TOWER L3 (TELEOP)",  "points": 30, "time_s": 18, "phase": "endgame"},
    ],
    "rp": [
        {"name": "ENERGIZED",    "metric": "FUEL -> active HUB", "threshold": 100,
         "note": "Regional/District; 240 DCMP, 360 Champs -- 3.6x escalation"},
        {"name": "SUPERCHARGED", "metric": "FUEL -> active HUB", "threshold": 360,
         "note": "360 Regional/DCMP, 500 Championship"},
        {"name": "TRAVERSAL",    "metric": "TOWER points",       "threshold": 50,
         "note": "50 at every tier"},
    ],
}
BUILTINS = {"rebuilt": REBUILT}


def load_game(spec):
    if spec.lower() in BUILTINS:
        return BUILTINS[spec.lower()]
    with open(spec, encoding="utf-8") as fh:
        g = json.load(fh)
    validate_game(g, spec)
    return g


def validate_game(g, spec):
    """Fail loudly on the things this model silently ignored before (rehearsal 3.1)."""
    ca = g.get("cycle_actions") or []
    if not ca:
        sys.exit(f"SCHEMA ERROR [{spec}]: cycle_actions is empty. At least one is required.")
    if len(ca) > 1:
        print(f"  [!] SCHEMA WARNING [{spec}]: {len(ca)} cycle_actions given, but this model "
              f"uses ONLY cycle_actions[0] ('{ca[0].get('name')}').", file=sys.stderr)
        print("      Entries 1..n are IGNORED. To model a second repeatable scoring action, "
              "run the model once per action and add the results by hand, or move the "
              "second action into fixed_actions if it happens once per match.", file=sys.stderr)
    for rp in (g.get("rp") or []):
        if not rp_is_fixed_based(g, rp) and rp.get("basis") is None:
            pass  # cycle-based is the default and is fine
    return g


def rp_is_fixed_based(g, rp):
    """Is this RP counted off a fixed/endgame action rather than the cycle action?

    Was a hard-coded `"TOWER" in rp["metric"]` -- a 2026-REBUILT noun compiled into a
    game-agnostic tool (rehearsal 3.1). Now: an explicit `basis` field wins; otherwise
    the metric string is matched against the fixed_actions' own names.
    """
    basis = str(rp.get("basis", "")).strip().lower()
    if basis in ("fixed", "endgame"):
        return True
    if basis in ("cycle", "cycle_action"):
        return False
    metric = str(rp.get("metric", ""))
    toks = [t for t in re.split(r"[^A-Za-z0-9]+", metric) if len(t) > 2]
    for f in (g.get("fixed_actions") or []):
        name = str(f.get("name", "")).lower()
        if any(t.lower() in name for t in toks):
            return True
    return False


def model(g, cycle_s, auto_scored, fixed_choice=None, endgame_reserve=None):
    """Return a dict describing one strategy's expected match output."""
    ca = g["cycle_actions"][0]
    fixed = None
    if fixed_choice:
        for f in g["fixed_actions"]:
            if f["name"] == fixed_choice:
                fixed = f
                break
    # endgame reserve = time you stop cycling to go do the fixed action
    reserve = endgame_reserve if endgame_reserve is not None else (fixed["time_s"] if fixed else 0)
    cycling_s = max(0.0, g["teleop_s"] - reserve)
    cycles = cycling_s / cycle_s if cycle_s > 0 else 0
    teleop_units = cycles * ca["per_cycle"]
    teleop_pts = teleop_units * ca["points_teleop"]
    auto_pts = auto_scored * ca["points_auto"]
    fixed_pts = fixed["points"] if fixed else 0
    # AUTO fixed actions are additive (they don't consume teleop time)
    auto_fixed = [f for f in g["fixed_actions"] if f.get("phase") == "auto"]
    return {
        "cycle_s": cycle_s, "cycles": cycles,
        "units": teleop_units + auto_scored,
        "auto_pts": auto_pts, "teleop_pts": teleop_pts,
        "fixed": fixed["name"] if fixed else "(none)", "fixed_pts": fixed_pts,
        "reserve_s": reserve,
        "total": auto_pts + teleop_pts + fixed_pts,
        "auto_fixed_available": [f["name"] for f in auto_fixed],
    }


def fmt_row(r):
    return (f"{r['fixed']:<22}{r['cycle_s']:>6.1f}{r['cycles']:>8.1f}{r['units']:>9.1f}"
            f"{r['auto_pts']:>8.0f}{r['teleop_pts']:>9.1f}{r['fixed_pts']:>8.0f}{r['total']:>9.1f}")


def report(g, cycle_s, auto_scored):
    ca = g["cycle_actions"][0]
    print(f"\n{'='*78}\n {g['name']}  --  cycle model\n{'='*78}")
    print(f" Match: AUTO {g['auto_s']}s + TELEOP {g['teleop_s']}s"
          f"   [endgame window {g['endgame_s']}s is INFORMATIONAL ONLY]")
    print("   endgame_s enters no arithmetic anywhere. The cost of an endgame action is")
    print("   fixed_actions[].time_s, which is subtracted from teleop_s. teleop_s must")
    print("   therefore be the FULL teleop period INCLUSIVE of the endgame window.")
    print(f" Cycle action: {ca['name']}  =  {ca['per_cycle']} unit(s)/cycle "
          f"@ {ca['points_teleop']} pt(s) each  ->  {ca['per_cycle']*ca['points_teleop']} pts/cycle")
    print(f" Your cycle time: {cycle_s}s     AUTO units scored: {auto_scored}")
    echo_constants(g, cycle_s, auto_scored)

    print(f"\n--- Strategy comparison (what each endgame choice is really worth) ---\n")
    print(f"{'endgame choice':<22}{'cycle':>6}{'cycles':>8}{'units':>9}{'autoP':>8}{'teleP':>9}{'fixP':>8}{'TOTAL':>9}")
    print("-" * 79)
    rows = [model(g, cycle_s, auto_scored, None, 0)]
    for f in g["fixed_actions"]:
        if f.get("phase") == "auto":
            continue
        rows.append(model(g, cycle_s, auto_scored, f["name"]))
    for r in rows:
        print(fmt_row(r))

    base = rows[0]["total"]
    print(f"\n--- Break-even: is the fixed action worth the cycles it costs? ---\n")
    ppc = ca["per_cycle"] * ca["points_teleop"]
    print(f"{'action':<22}{'pts':>6}{'time':>7}{'cycles lost':>13}{'pts lost':>10}{'NET':>8}  verdict")
    print("-" * 82)
    for f in g["fixed_actions"]:
        if f.get("phase") == "auto":
            continue
        lost_cycles = f["time_s"] / cycle_s
        lost_pts = lost_cycles * ppc
        net = f["points"] - lost_pts
        verdict = "WORTH IT" if net > 0 else "costs more than it pays"
        print(f"{f['name']:<22}{f['points']:>6}{f['time_s']:>6}s{lost_cycles:>13.2f}"
              f"{lost_pts:>10.1f}{net:>+8.1f}  {verdict}")

    print(f"\n--- Sensitivity: what is 1 second of cycle time worth? ---\n")
    a = model(g, cycle_s, auto_scored, None, 0)["total"]
    b = model(g, cycle_s + 1, auto_scored, None, 0)["total"]
    print(f" Going from {cycle_s}s to {cycle_s+1}s costs {a-b:.1f} points/match.")
    print(f" Over a 12-match qualification schedule: {12*(a-b):.0f} points.")
    print(f" -> Driver practice and a faster intake are worth ~{a-b:.1f} pts/s/match. "
          f"Compare that to the {ppc} pts/cycle a new mechanism might add.")

    if g.get("rp"):
        print(f"\n--- Ranking Point feasibility at {cycle_s}s cycle ---\n")
        print(f"{'RP':<16}{'threshold':>10}{'you (alone)':>13}{'w/ alliance x3':>16}  reachable?")
        print("-" * 74)
        solo = model(g, cycle_s, auto_scored, None, 0)["units"]
        for rp in g["rp"]:
            th = rp["threshold"]
            if rp_is_fixed_based(g, rp):
                print(f"{rp['name']:<16}{th:>10}{'n/a':>13}{'n/a':>16}  (fixed/endgame-action based; see break-even above)")
                continue
            trio = solo * 3
            ok = "YES alliance" if trio >= th else "NO"
            if solo >= th:
                ok = "YES solo"
            print(f"{rp['name']:<16}{th:>10}{solo:>13.0f}{trio:>16.0f}  {ok}")
        for rp in g["rp"]:
            if rp.get("note"):
                print(f"   {rp['name']}: {rp['note']}")


def sweep(g, auto_scored):
    ca = g["cycle_actions"][0]
    print(f"\n--- Cycle-time sweep: {g['name']} (AUTO units = {auto_scored}) ---\n")
    choices = [None] + [f["name"] for f in g["fixed_actions"] if f.get("phase") != "auto"]
    hdr = "".join(f"{(c or 'no endgame')[:13]:>15}" for c in choices)
    print(f"{'cycle s':>8}{hdr}")
    print("-" * (8 + 15 * len(choices)))
    for cs in [4, 5, 6, 7, 8, 10, 12, 15, 20]:
        cells = ""
        for c in choices:
            cells += f"{model(g, cs, auto_scored, c)['total']:>15.1f}"
        print(f"{cs:>8}{cells}")
    print("\nRead down a column to see how sensitive a strategy is to cycle time.")
    print("A strategy whose column is flat is cycle-insensitive -- that is a SMALL-TEAM strategy:")
    print("it pays the same whether your drivers are elite or average.")


# ------------------------------------------------------------------ provenance / priors
# Rehearsal grade §1: "A cycle model that is never checked against a season of results is a
# rhetoric generator." The model was fed median_alliance_score=120 ("a pure guess"; reality
# 147.0) and an invented 8 FUEL / 8.0 s. Nothing printed a warning. Now everything does.

def _src(obj, key):
    """The declared source for a constant, or None. Convention: `<key>_source`, then `_source`."""
    if not isinstance(obj, dict):
        return None
    for k in (f"{key}_source", "_source", "source"):
        v = obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def echo_constants(g, cycle_s, auto_scored):
    """Echo EVERY user-supplied constant beside its source. No source -> [UNSOURCED].

    A constant with no source is a guess. Guesses are allowed -- silently laundering them
    into a point estimate is not.
    """
    rows = []   # (label, value, source_or_None)

    # Constants supplied on the command line have no file to carry a source.
    rows.append(("--cycle (your cycle time, s)", cycle_s,
                 "CLI argument -- a ROBOT-DESIGN ASSUMPTION, not a manual value"))
    rows.append(("--auto-scored (AUTO units)", auto_scored,
                 "CLI argument -- a ROBOT-DESIGN ASSUMPTION, not a manual value"))

    for k in ("auto_s", "teleop_s", "endgame_s"):
        if k in g:
            rows.append((k, g[k], _src(g, k)))
    for i, ca in enumerate(g.get("cycle_actions") or []):
        tag = f"cycle_actions[{i}]"
        for k in ("per_cycle", "points_auto", "points_teleop"):
            if k in ca:
                rows.append((f"{tag}.{k}  ({ca.get('name','?')})", ca[k], _src(ca, k)))
    for i, f in enumerate(g.get("fixed_actions") or []):
        tag = f"fixed_actions[{i}] {f.get('name','?')}"
        for k in ("points", "time_s"):
            if k in f:
                rows.append((f"{tag}.{k}", f[k], _src(f, k)))
    for i, rp in enumerate(g.get("rp") or []):
        if "threshold" in rp:
            rows.append((f"rp[{i}] {rp.get('name','?')}.threshold", rp["threshold"], _src(rp, "threshold")))
    for k in ("median_alliance_score", "mean_alliance_score"):
        if k in g:
            rows.append((k, g[k], _src(g, k)))

    print("\n--- CONSTANTS IN THIS MODEL AND WHERE THEY CAME FROM ---\n")
    print(f"{'constant':<52}{'value':>10}  source")
    print("-" * 108)
    unsourced = 0
    for label, val, src in rows:
        if src is None:
            unsourced += 1
            src = "[UNSOURCED] <- a GUESS. Add a `_source` sibling naming a manual "\
                  "section or a research/predictive_tba/ column."
        print(f"{label:<52}{val:>10}  {src}")
    if unsourced:
        print(f"\n  [!] {unsourced} of {len(rows)} constants are UNSOURCED. Every number below "
              f"inherits their error.")
        print("      The 2026 rehearsal shipped 5 unsourced constants and was graded D for it.")
    print("      Priors for the scoring constants: `python tools/score-priors.py priors`.")


def load_score_priors():
    """Import score-priors.py (hyphenated -> importlib) and return its cross-season band."""
    import importlib.util
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "score-priors.py")
    if not os.path.exists(p):
        return None
    try:
        spec = importlib.util.spec_from_file_location("score_priors", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        meds = [m.season_stats(y)["median"] for y in m.SEASONS]
        return {"lo": min(meds), "mid": m.pct(meds, .5), "hi": max(meds),
                "years": m.SEASONS, "meds": meds}
    except Exception as e:                       # data missing, columns renamed, anything
        print(f"  [!] could not load priors from score-priors.py: {e}", file=sys.stderr)
        return None


def report_range(g, cycle_s, auto_scored, lo_mult, hi_mult):
    """Low / likely / high band instead of a false point estimate.

    A point estimate from unsourced constants is a lie with a decimal place on it. The band
    is driven by the constant the team controls and knows least well at kickoff: cycle time.
    """
    ca = g["cycle_actions"][0]
    print(f"\n{'='*78}\n {g['name']}  --  cycle model  [RANGE MODE]\n{'='*78}")
    print(" Kickoff reality: you have no outcome data for this game. Every number here rests")
    print(" on assumed constants. This mode reports a BAND. Do not quote the middle column")
    print(" alone -- quote the band, and quote it as a PRIOR.")
    echo_constants(g, cycle_s, auto_scored)

    c_hi, c_mid, c_lo = cycle_s * hi_mult, cycle_s, cycle_s * lo_mult   # slow cycle = low score
    print(f"\n--- Band driver: cycle time  {c_lo:.1f}s (optimistic) / {c_mid:.1f}s (likely) / "
          f"{c_hi:.1f}s (pessimistic) ---")
    print(f"    multipliers {lo_mult:g}x / 1x / {hi_mult:g}x on your assumed {cycle_s:g}s. "
          f"Override with --range-low / --range-high.")
    print("    Rationale: a rookie-to-veteran driver spread of roughly 2x on cycle time is the")
    print("    single largest uncontrolled term in this model at kickoff.\n")

    choices = [None] + [f["name"] for f in (g.get("fixed_actions") or [])]
    print(f"{'endgame choice':<24}{'LOW':>10}{'LIKELY':>10}{'HIGH':>10}{'band':>12}")
    print("-" * 66)
    for ch in choices:
        t_lo = model(g, c_hi, auto_scored, ch, 0)["total"]
        t_mid = model(g, c_mid, auto_scored, ch, 0)["total"]
        t_hi = model(g, c_lo, auto_scored, ch, 0)["total"]
        name = ch or "(no fixed action)"
        print(f"{name:<24}{t_lo:>10.0f}{t_mid:>10.0f}{t_hi:>10.0f}{t_hi-t_lo:>11.0f}p")

    best_mid = max(model(g, c_mid, auto_scored, ch, 0)["total"] for ch in choices)
    best_lo = max(model(g, c_hi, auto_scored, ch, 0)["total"] for ch in choices)
    best_hi = max(model(g, c_lo, auto_scored, ch, 0)["total"] for ch in choices)

    pri = load_score_priors()
    print("\n--- Reality check against prior seasons (source: tools/score-priors.py) ---\n")
    if pri:
        yrs = "  ".join(f"{y}:{v:.0f}" for y, v in zip(pri["years"], pri["meds"]))
        print(f"  median alliance score, {pri['years'][0]}-{pri['years'][-1]}:  {yrs}")
        print(f"  PRIOR BAND for a 2027 median alliance score: "
              f"{pri['lo']:.0f} / {pri['mid']:.0f} / {pri['hi']:.0f}")
        print(f"  This robot ALONE, best strategy:              "
              f"{best_lo:.0f} / {best_mid:.0f} / {best_hi:.0f}")
        print(f"  Three such robots (crude alliance proxy):     "
              f"{3*best_lo:.0f} / {3*best_mid:.0f} / {3*best_hi:.0f}")
        if 3 * best_lo > pri["hi"] or 3 * best_hi < pri["lo"]:
            ratio = (3 * best_mid) / pri["mid"] if pri["mid"] else float("nan")
            print(f"\n  !! PRIOR CONFLICT: the 3-robot band does NOT overlap the prior band.")
            print(f"     Your model implies an alliance {ratio:.1f}x the 4-season median. At least")
            print("     one constant is wrong -- check per_cycle and cycle time FIRST, then confirm")
            print("     the scoring action actually reaches the scoring aperture (the BOM does not).")
            print("     DO NOT publish these totals until this reconciles or you can defend the gap.")
        else:
            print("\n  OK: the 3-robot band overlaps the prior band. Not a validation -- only the")
            print("  absence of an order-of-magnitude error.")
        print("\n  READ IT LIKE THIS: if the 3-robot band does not overlap the prior band, one of")
        print("  your constants is wrong -- most often per_cycle or cycle time. That is the check")
        print("  the 2026 rehearsal skipped when it used 120 against a real 147.")
        print(f"  The prior band itself spans {pri['hi']-pri['lo']:.0f} points across 4 seasons, so")
        print("  it can only catch an order-of-magnitude error. It is a smoke alarm, not a scale.")
    else:
        print("  [!] priors unavailable -- run `python tools/score-priors.py priors` by hand.")
    print("\n  *** THIS OUTPUT EXPIRES AT WEEK 1. *** Once real 2027 results exist, re-run")
    print("      score-priors.py on 2027, replace the assumed constants with measured ones,")
    print("      and re-run WITHOUT --range. A band is what you publish when you do not know;")
    print("      it is not a permanent hedge.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="rebuilt", help="builtin name ('rebuilt') or path to a JSON game file")
    ap.add_argument("--cycle", type=float, default=8.0, help="your cycle time in seconds")
    ap.add_argument("--auto-scored", type=float, default=3, help="units scored during AUTO")
    ap.add_argument("--sweep", action="store_true", help="print the cycle-time sensitivity table")
    ap.add_argument("--range", action="store_true", dest="do_range",
                    help="report a low/likely/high BAND instead of a false point estimate "
                         "(use this at kickoff, before any outcome data exists)")
    ap.add_argument("--range-low", type=float, default=0.7,
                    help="optimistic cycle-time multiplier (default 0.7)")
    ap.add_argument("--range-high", type=float, default=1.5,
                    help="pessimistic cycle-time multiplier (default 1.5)")
    a = ap.parse_args()
    try:
        g = load_game(a.game)
    except FileNotFoundError:
        print(f"No such game file: {a.game}   (builtins: {', '.join(BUILTINS)})")
        return 1
    if a.sweep:
        sweep(g, a.auto_scored)
    elif a.do_range:
        report_range(g, a.cycle, a.auto_scored, a.range_low, a.range_high)
    else:
        report(g, a.cycle, a.auto_scored)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
