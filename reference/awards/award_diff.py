#!/usr/bin/env python3
"""Extract the CURRENT FRC award-name list from the FIRST authority webpages and
diff it against the locked baseline in awards_baseline.txt.

    python award_diff.py            # diff live snapshots in _web/ vs baseline
    python award_diff.py --emit     # print the extracted list (used to rebuild baseline)

Extractor logic (verified against the 2026-08-21 snapshots):
  * machine-awards / team-awards / submitted-awards pages render each award as an
    accordion header line immediately followed by a line that is exactly
    "Updated" or "Updates". That pairing is an exact, noise-free award-name test.
  * frc-awards-main renders the flat "All Awards" list as
    "<Award Name> - <lowercase description>"; used as a cross-check so that
    awards with no accordion (Finalist, Winner, Volunteer of the Year,
    Digital Animation Award) are still captured.

The _web/ snapshots are not in the public repository. python fetch_award_pages.py (or
bash tools/rebuild-corpus.sh --fetch from the repository root) writes them.

Exit code 0 = no change vs baseline, 1 = drift detected (or files missing).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "_web")
BASELINE = os.path.join(HERE, "awards_baseline.txt")

ACCORDION_PAGES = ["machine-awards", "team-awards", "submitted-awards"]
FLAT_PAGE = "frc-awards-main"

# Lines on the flat list read "<Name> - celebrates ..." / "- presented ..." etc.
FLAT_RE = re.compile(
    r"^(?P<name>[A-Z][^-]{2,79}?)\s+-\s+"
    r"(celebrates|presented|outstanding|during the course|the most prestigious)",
    re.I,
)
# Junk the accordion test can pick up if FIRST re-templates a page.
DROP = {"Deadlines", "Awards", "Award", "Dates", "Description"}


def norm(s: str) -> str:
    s = s.replace("(R)", "").replace("(TM)", "")
    s = re.sub(r"\s+", " ", s).strip(" . ")
    return s


def extract() -> set:
    found = set()
    for page in ACCORDION_PAGES:
        path = os.path.join(WEB, page + ".txt")
        if not os.path.exists(path):
            continue
        lines = open(path, encoding="ascii", errors="replace").read().split("\n")
        for i in range(len(lines) - 1):
            if lines[i + 1].strip() in ("Updated", "Updates"):
                nm = norm(lines[i])
                if nm and nm not in DROP and "Award" in nm:
                    found.add(nm)
    flat = os.path.join(WEB, FLAT_PAGE + ".txt")
    if os.path.exists(flat):
        for line in open(flat, encoding="ascii", errors="replace"):
            m = FLAT_RE.match(line.strip())
            if m:
                nm = norm(m.group("name"))
                if nm and nm not in DROP:
                    found.add(nm)
    return found


def main() -> int:
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__)
        return 0
    # All four snapshots are required. Diffing a partial set used to report every
    # baseline name as GONE, a false drift alarm.
    absent = [p for p in ACCORDION_PAGES + [FLAT_PAGE]
              if not os.path.isfile(os.path.join(WEB, p + ".txt"))]
    if absent:
        more = f" and {len(absent) - 1} more" if len(absent) > 1 else ""
        print(f"MISSING: reference/awards/_web/{absent[0]}.txt{more} (not in the public "
              "repository; fetch with: bash tools/rebuild-corpus.sh --fetch)", file=sys.stderr)
        return 1
    cur = extract()
    if "--emit" in sys.argv:
        for a in sorted(cur):
            print(a)
        return 0
    if not os.path.exists(BASELINE):
        print(f"MISSING BASELINE: {BASELINE}")
        return 1
    base = {norm(l) for l in open(BASELINE, encoding="ascii", errors="replace")
            if l.strip() and not l.startswith("#")}
    added = sorted(cur - base)
    removed = sorted(base - cur)
    print(f"baseline={len(base)}  live={len(cur)}")
    for a in added:
        print(f"  + NEW / RENAMED-TO : {a}")
    for a in removed:
        print(f"  - GONE / RENAMED-FROM: {a}")
    if not added and not removed:
        print("  no change -- 00_AWARD_LIST_VERIFIED.md is still accurate")
        return 0
    print("  >>> AWARD LIST DRIFTED. Update 00_AWARD_LIST_VERIFIED.md and awards.yaml.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
