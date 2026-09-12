#!/usr/bin/env python3
"""Extract the award-ceremony roster from an FRC Game Manual text extraction, and
diff it season-over-season.

The FRC manual's playoff schedule table (section 10.6 in REBUILT) interleaves
"15-minute awards break: <comma-separated award names>" lines with the Finals
matches. That list is the complete set of JUDGED awards presented at a
single-division event -- which makes it a primary-source, offline, season-taggable
award roster with no web dependency.

    python manual_award_order.py <manual.txt> [...]     # print roster per file
    python manual_award_order.py --diff <a.txt> <b.txt> # diff two seasons

Verified against 2024 CRESCENDO / 2025 REEFSCAPE / 2026 REBUILT extractions in
manuals/archive/frc/_txt/ (not in the public repository; bash tools/rebuild-corpus.sh
regenerates them). 2022 and 2023 manuals do not name awards in the
schedule table, so this method only reaches back to 2024.
"""
import os
import re
import sys

BREAK_RE = re.compile(r"^\s*15-minute awards break:\s*(.*)$", re.I)
FINAL_RE = re.compile(r"^\s*Awards:\s*(.*)$", re.I)
# Continuation lines: a break list can wrap onto the next non-blank line.
STOP_RE = re.compile(r"^\s*(Finals|\d|\*|Round|Upper|Lower)", re.I)

CANON = {
    "rookie all star": "Rookie All-Star Award",
    "rookie all-star": "Rookie All-Star Award",
    "rising all star": "Rising All-Star Award",
    "rising all-star": "Rising All-Star Award",
    "rookie inspiration": "Rookie Inspiration Award",
    "dean's list": "Dean's List Award",
    "first leadership award": "FIRST Leadership Award",
    "engineering inspiration": "Engineering Inspiration Award",
    "imagery": "Imagery Award",
    "gracious professionalism": "Gracious Professionalism Award",
    "team spirit": "Team Spirit Award",
    "autonomous": "Autonomous Award",
    "creativity": "Creativity Award",
    "quality": "Quality Award",
    "industrial design": "Industrial Design Award",
    "innovation in control": "Innovation in Control Award",
    "excellence in engineering": "Excellence in Engineering Award",
    "team sustainability": "Team Sustainability Award",
    "judges": "Judges Award",
    "finalists": "Finalist (robot performance)",
    "winners": "Winner (robot performance)",
    "first impact award": "FIRST Impact Award",
    "remaining awards": None,          # placeholder phrase, not an award
}


def canon(tok: str):
    t = tok.strip().strip("*").strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"^(and|the)\s+", "", t, flags=re.I)
    key = t.lower().replace(" award", "").strip()
    if key in CANON:
        return CANON[key]
    if t.lower() in CANON:
        return CANON[t.lower()]
    return t or None


def roster(path: str):
    lines = open(path, encoding="ascii", errors="replace").read().split("\n")
    out, seen = [], set()
    for i, line in enumerate(lines):
        m = BREAK_RE.match(line) or FINAL_RE.match(line)
        if not m:
            continue
        blob = m.group(1)
        # absorb a single wrapped continuation line
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and lines[j].strip() and not STOP_RE.match(lines[j]) \
                and not BREAK_RE.match(lines[j]) and len(lines[j].strip()) < 60 \
                and "  " not in lines[j].strip():
            blob += " " + lines[j].strip()
        for tok in re.split(r",| and ", blob):
            nm = canon(tok)
            if nm and nm not in seen:
                seen.add(nm)
                out.append(nm)
    return out


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) > 1 else 2
    args = [a for a in sys.argv[1:] if a != "--diff"]
    if "--diff" in sys.argv and len(args) != 2:
        print("--diff needs exactly 2 manual .txt files")
        return 2
    for p in args:
        if not os.path.isfile(p):
            print(f"MISSING: {p} (the manual text is not in the public repository; "
                  "rebuild it with: bash tools/rebuild-corpus.sh)", file=sys.stderr)
            return 1
    if "--diff" in sys.argv:
        a, b = roster(args[0]), roster(args[1])
        na, nb = os.path.basename(args[0]), os.path.basename(args[1])
        print(f"{na}: {len(a)} awards   ->   {nb}: {len(b)} awards")
        for x in b:
            if x not in a:
                print(f"  + ADDED  in {nb}: {x}")
        for x in a:
            if x not in b:
                print(f"  - GONE   from {na}: {x}")
        if set(a) == set(b):
            print("  no change")
        return 0
    for p in args:
        print(f"=== {os.path.basename(p)} ===")
        for x in roster(p):
            print(f"  {x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
