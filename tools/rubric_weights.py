#!/usr/bin/env python3
"""
rubric_weights.py -- kickoff-day weight setter for the BIOCORE achievability rubric.

Reads an FRC game manual (PDF or already-extracted .txt) and prints the five
GAME-CONDITIONAL adjustments that reference/04_PREDICTIVE_FACTORS.md derives
from the 2022-2026 evidence base. Everything it keys on is a fact that is
printed in Section 6 of every modern manual, so it runs in seconds on the
manual you download at 12:00 p.m. ET on 2027-01-09.

What it extracts, and why each one moves a weight:

  AUTO-gated Ranking Point?    -> AUTO weight. Across 2023-2026 the partial
                                  correlation of AUTO score with qualification
                                  rank, holding total match score fixed, is
                                  ~0.05 in the three seasons with no AUTO RP
                                  and 0.26 in 2025 REEFSCAPE, the one season
                                  that had one. Auto only buys rank beyond its
                                  face point value when an RP is gated on it.
  Foul point values            -> DEFENSE weight. Cost of a defensive mistake,
                                  expressed as a share of a typical score.
  PIN count seconds            -> DEFENSE weight. 5s (2022-2024) vs 3s (2025-26).
  "protection" G-rules         -> DEFENSE weight. Protected zones are where
                                  defense is illegal; more of them = less
                                  defensible field.
  "1 defender at a time"       -> DEFENSE weight. Present only in 2025.
  Scoring rows in Table 6-x    -> SCOPE weight. Proxy for how many distinct
                                  scoring actions a robot could chase.

Usage:
    python tools/rubric_weights.py manuals/archive/frc/2026_REBUILT_GameManual.pdf
    python tools/rubric_weights.py research/rule_inventories/_text/2025.txt
    python tools/rubric_weights.py <manual> --json

Validated against 2022-2026 -- see the dry-run section of
reference/04_PREDICTIVE_FACTORS.md.
"""
import argparse
import json
import os
import re
import sys

# Any Ranking Point / Bonus whose NAME references the autonomous period.
# Positive controls in this corpus: 2018 POWER UP "Auto-Quest", 2025 REEFSCAPE
# "AUTO RP". Negative controls: 2016-2017, 2019-2024, 2026.
AUTO_RP = re.compile(r"\bAuto(?:nomous)?[A-Za-z]*[- ]?(?:RP\b|Bonus\b|Ranking Point\b|Quest\b)",
                     re.I)
RP_NAME = re.compile(r"\b([A-Z][A-Za-z\-]{2,18})\s+(?:RP\b|BONUS\b|Bonus\b)")
RP_NOISE = {"MATCH", "FIELD", "Ranking", "Definition", "BONUS", "Kickoff", "ROBOT",
            "REBUILT", "LINE", "The", "This", "A"}


def load(path):
    if path.lower().endswith(".pdf"):
        try:
            import pymupdf
        except ImportError:
            sys.exit("need pymupdf, or pass a pre-extracted .txt")
        d = pymupdf.open(path)
        return "\n".join(p.get_text() for p in d)
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def flat(t):
    """Whitespace-normalise AND punctuation-normalise. pdftotext and pymupdf
    disagree about curly quotes and dashes; every regex below assumes ASCII."""
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-"), ("−", "-"), ("�", "'")):
        t = t.replace(a, b)
    return " ".join(t.split())


def foul_values(t):
    """-> {'minor': n, 'major': n}.

    Column geometry in the penalty table is unreliable once the PDF is
    flattened (2023 and 2026 both interleave the penalty names and their
    descriptions differently). What IS stable across 2015-2026 is the ORDER:
    the first 'a credit of N points' after the 'Rule violations' caption is the
    small foul, the second is the big one. Verified against all five seasons in
    the source-shorthand list."""
    T = flat(t)
    m = re.search(r"Rule violations(.{0,900})", T)
    seg = m.group(1) if m else T
    vals = [int(x) for x in re.findall(r"a credit of\s*(\d+)\s*points", seg)][:2]
    out = {}
    if len(vals) >= 1:
        out["minor"] = vals[0]
    if len(vals) >= 2:
        out["major"] = vals[1]
    return out


def pin_seconds(t):
    m = re.search(r"There'?s a (\d+)-count on PINS", flat(t))
    if m:
        return int(m.group(1))
    m = re.search(r"may not PIN an opponent'?s ROBOT for more than (\d+) seconds", flat(t))
    return int(m.group(1)) if m else None


def protection_rules(t):
    """Names of the season's protected zones/structures.

    Keyed on the TITLE ('<THING> protection'), not on the rule id: in 2024 the
    manual's two-column layout wraps a neighbouring rule id between a rule
    number and its own title, so an id-anchored regex finds only 1 of the 3."""
    T = flat(t)
    ids = []
    for m in re.finditer(r"\b([A-Z][A-Z/ ]{2,30}?)\s+protection\b", T):
        name = m.group(1).strip()
        if name and name not in ids:
            ids.append(name)
    return sorted(ids)


# A protection rule that only switches on for a terminal time window protects
# the ENDGAME structure. One with no window (or an explicit "prior to the last
# N seconds") protects a place the opponent SCORES or LOADS for most of TELEOP.
# That distinction, not the raw count of protection rules, is what separates
# the seasons where defense worked from the seasons where it did not.
ENDGAME_WINDOW = re.compile(
    r"(?:during|in|within)\s+the\s+(?:last|final)\s+\d+\s+seconds", re.I)
PRIOR_TO_WINDOW = re.compile(r"prior to\s+the\s+(?:last|final)\s+\d+\s+seconds", re.I)
# 2022 states its HANGAR ZONE protection only in the ARENA timing table, as
# "HANGAR ZONE protection engaged 0:30". No G-rule carries the phrase.
TIMER_ENGAGED = re.compile(r"engaged\s+\d+:\d\d")


def protection_scope(t):
    """-> [(name, 'teleop-wide'|'endgame-only'), ...] and the summary flag.

    Validated against all five seasons in the source-shorthand list:
      2022 HANGAR ZONE  endgame-only  ('protection engaged 0:30' / 'final 30 seconds')
      2023 (none)
      2024 PODIUM       teleop-wide   ('Prior to the last 20 seconds ...')
           SOURCE/AMP   teleop-wide   (no time window at all)
           STAGE        endgame-only  ('during the last 20 seconds')
      2025 ZONE (REEF/BARGE) teleop-wide  (no time window -- the primary
                                           CORAL scoring structure)
           CAGE         endgame-only  ('during the last 20 seconds')
      2026 TOWER        endgame-only  ('during the last 30 seconds')
    """
    T = flat(t)
    out = []
    for name in protection_rules(t):
        segs = []
        for m in re.finditer(re.escape(name) + r"\s+protection\b(.{0,700})", T):
            seg = m.group(1)
            # Stop at the rule's own Violation: line. Without this the window
            # runs on into the NEXT protection rule -- which is exactly how
            # 2025's ZONE protection inherited CAGE protection's "last 20
            # seconds" and got mis-scored as endgame-only.
            cut = seg.find("Violation:")
            segs.append(seg[:cut + 40] if cut != -1 else seg[:450])
        # Prefer the occurrence that is actually the rule, not a cross-reference
        # or the ARENA timing table.
        rule_segs = [s for s in segs if "Violation:" in s or "may not contact" in s]
        scope = "endgame-only"
        for seg in (rule_segs or segs):
            if TIMER_ENGAGED.search(seg):          # ARENA timing table form
                scope = "endgame-only"
                break
            if PRIOR_TO_WINDOW.search(seg) or not ENDGAME_WINDOW.search(seg):
                scope = "teleop-wide"
                break
        out.append((name, scope))
    return out


POSSESSION = [
    r"may not(?:\s+simultaneously)?\s+CONTROL more than (\d+)",
    r"CONTROL of more than (\d+)",
    r"may not have greater-than-MOMENTARY CONTROL of more than (\d+)",
]


def possession_limit(t):
    """Smallest per-ROBOT SCORING ELEMENT possession cap the manual states, or
    None if the game has no cap. A cap is the single most reliable
    'playing field leveler' in John Bottenberg's taxonomy (see the doc):
    it puts a hard ceiling on how far an elite cycle machine can pull away.
      2022 -> 2   2023 -> 1   2024 -> 1   2025 -> 1   2026 -> None (uncapped)
    """
    T = flat(t)
    vals = []
    for p in POSSESSION:
        vals += [int(x) for x in re.findall(p, T)]
    return min(vals) if vals else None


def one_defender(t):
    T = flat(t)
    return bool(re.search(r"1 defender at a time", T, re.I) or
                re.search(r"[Nn]o more than 1 ROBOT may be on the opponent", T))


def regardless_count(t):
    return len(re.findall(r"regardless of who initiates", flat(t)))


def ranking_points(t):
    """Candidate Ranking-Point / Bonus names, plus the AUTO-gating verdict.

    The name list is a HUMAN CHECK, not a decision input -- manuals name RPs
    inconsistently and the list picks up a few match-point bonuses. The only
    thing that feeds the weights is auto_gated, which fires when a Ranking
    Point or Bonus is NAMED after the autonomous period."""
    T = flat(t)
    names = sorted({m.group(1) for m in RP_NAME.finditer(T)} - RP_NOISE)
    hits = sorted({flat(m.group(0)) for m in AUTO_RP.finditer(T)})
    return names, hits


def scoring_rows(t):
    """Count point-value rows in the season's point table (a scope proxy: how
    many distinct scoring actions the game offers)."""
    T = flat(t)
    m = re.search(r"Table \d+-\d+:? [A-Z][A-Za-z ]{0,25}point values(.{0,2600})", T)
    if not m:
        return None
    seg = m.group(1)
    rows = re.findall(r"[a-z\)]\s+(\d{1,3})(?:\s+(\d{1,3}))?(?=\s+[A-Z*])", seg)
    return len(rows) if rows else None


# ------------------------------------------------------------------ weighting
BASE = {
    "drive_practice": 90,
    "reliability": 85,
    "scope_discipline": 85,
    "scoring_output": 80,
    "drivetrain_choice": 45,
    "cots_leverage": 55,
    "auto_vision": 40,
    "defense_capability": 35,
}


def adjust(f):
    """Apply the game-conditional deltas from 04_PREDICTIVE_FACTORS.md Sec 10."""
    w = dict(BASE)
    notes = []

    if f["auto_gated_rp"]:
        w["auto_vision"] += 25
        notes.append(f"AUTO-gated RP present ({', '.join(f['auto_gated_rp'])}): auto_vision +25")
    else:
        notes.append("no AUTO-gated RP: auto_vision unchanged (auto is worth face value only)")

    d = 0
    if f["pin_seconds"] is not None:
        if f["pin_seconds"] >= 5:
            d += 10
            notes.append(f"{f['pin_seconds']}s PIN count (permissive): defense +10")
        else:
            notes.append(f"{f['pin_seconds']}s PIN count (tight): defense +0")

    # v2: scope matters far more than count. A rule that protects where the
    # opponent SCORES, for most of TELEOP, removes the defensive play entirely.
    # A rule that only fires in the closing seconds costs a defender almost
    # nothing. v1 counted rules at -8 each and mis-ordered 2026 as a result.
    wide = [n for n, s in f["protection_scope"] if s == "teleop-wide"]
    endg = [n for n, s in f["protection_scope"] if s == "endgame-only"]
    if wide:
        d -= 20
        notes.append(f"scoring/loading area protected through TELEOP ({', '.join(wide)}): defense -20")
    else:
        notes.append("no TELEOP-wide protected area: defense -0 (defense is legal where points happen)")
    if endg:
        d -= 4 * len(endg)
        notes.append(f"{len(endg)} endgame-only protection(s) ({', '.join(endg)}): defense {-4 * len(endg):+d}")

    if f["one_defender_rule"]:
        d -= 15
        notes.append("'1 defender at a time' rule present: defense -15")

    if f["foul"].get("major") and f["typical_score"]:
        share = 100.0 * f["foul"]["major"] / f["typical_score"]
        # v2: banded, not a cliff. v1 used a single 10% threshold and 2026
        # landed at 10.5%, taking the full penalty on a 0.5pp margin.
        if share >= 12:
            d -= 10
            band = "expensive"
        elif share >= 8:
            d -= 5
            band = "moderate"
        else:
            d += 5
            band = "cheap"
        notes.append(f"MAJOR foul = {share:.1f}% of a typical alliance score ({band}): "
                     f"defense {(-10 if share >= 12 else -5 if share >= 8 else 5):+d}")
    w["defense_capability"] = max(0, min(100, w["defense_capability"] + d))

    lim = f["possession_limit"]
    if lim is None:
        notes.append("NO SCORING ELEMENT possession limit: uncapped cycle game, "
                     "elite teams pull away -- treat the event-selection and "
                     "second-pick paths as the realistic ceiling")
    else:
        notes.append(f"possession limit {lim} per ROBOT: a playing-field leveler is present")

    n = f["scoring_rows"]
    if n and n >= 8:
        w["scope_discipline"] = min(100, w["scope_discipline"] + 10)
        notes.append(f"{n} scoring rows (wide game): scope_discipline +10")
    elif n:
        notes.append(f"{n} scoring rows: scope_discipline unchanged")
    return w, notes


def extract(path, typical_score=None):
    t = load(path)
    names, auto_gated = ranking_points(t)
    return {
        "source": os.path.basename(path),
        "foul": foul_values(t),
        "pin_seconds": pin_seconds(t),
        "protection_rules": protection_rules(t),
        "protection_scope": protection_scope(t),
        "possession_limit": possession_limit(t),
        "one_defender_rule": one_defender(t),
        "n_regardless_of_who_initiates": regardless_count(t),
        "ranking_points": names,
        "auto_gated_rp": auto_gated,
        "scoring_rows": scoring_rows(t),
        "typical_score": typical_score,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manual")
    ap.add_argument("--typical-score", type=float, default=None,
                    help="median alliance match score, if known (week-1 estimate is fine)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.manual):
        how = ("bash tools/rebuild-corpus.sh --fetch" if a.manual.lower().endswith(".pdf")
               else "bash tools/rebuild-corpus.sh")
        sys.exit("MISSING: %s (not in the public repository; run: %s)" % (a.manual, how))
    f = extract(a.manual, a.typical_score)
    w, notes = adjust(f)
    if a.json:
        print(json.dumps({"facts": f, "weights": w, "notes": notes}, indent=2))
        return
    print(f"== {f['source']} ==")
    print(f"  foul values          : {f['foul']}")
    print(f"  PIN count            : {str(f['pin_seconds']) + 's' if f['pin_seconds'] else 'not found'}")
    print(f"  protected zones      : "
          f"{', '.join(f'{n} [{s}]' for n, s in f['protection_scope']) or 'none'}")
    print(f"  possession limit     : {f['possession_limit'] if f['possession_limit'] else 'NONE (uncapped)'}")
    print(f"  1-defender rule      : {f['one_defender_rule']}")
    print(f"  'regardless of who initiates' : {f['n_regardless_of_who_initiates']}")
    print(f"  RP/BONUS names (eyeball these) : {', '.join(f['ranking_points']) or 'not parsed'}")
    print(f"  AUTO-gated RP        : {f['auto_gated_rp'] or 'NONE'}")
    print(f"  scoring rows         : {f['scoring_rows']}")
    print("  -- weights --")
    for k in sorted(w, key=lambda k: -w[k]):
        print(f"    {k:<20} {w[k]:>3}")
    print("  -- why --")
    for n in notes:
        print(f"    * {n}")


if __name__ == "__main__":
    main()
