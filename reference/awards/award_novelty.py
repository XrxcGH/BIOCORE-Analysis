#!/usr/bin/env python3
"""Find award names in an FRC Game Manual text extraction that a baseline list does
not already know. On 2027-01-09 this is the offline, no-web check that the BIOCORE
manual has not introduced, renamed, or retired an award.

    python award_novelty.py <manual.txt> [manual.txt ...]
    python award_novelty.py --baseline known_awards_2026.txt <manual.txt>
    python award_novelty.py --baseline-from <older_manual.txt> <newer_manual.txt>   # back-test

Why not a bare grep: `grep -oE "[A-Z][A-Za-z' ]+ Award"` left-extends across sentence
text ("Any team who wins the FIRST Impact Award") and across PDF table columns
("Impact Leadership Inspiration Star Award"), producing ~15 false positives per manual.
This trims leading sentence glue and rejects column bleed, which takes 2026 REBUILT
from 14 false positives to 0. See the dry runs in 00_AWARD_LIST_VERIFIED.md Sec.7.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASELINE = os.path.join(HERE, "known_awards_2026.txt")

# Award-name candidate: up to 5 Capitalised/ALLCAPS tokens then "Award(s)".
CAND = re.compile(r"((?:[A-Z][A-Za-z'\u2019\-]*\s+){1,5}Awards?)\b")
# Leading tokens that mean we ran off the front of the real name into prose or a
# neighbouring table column. Trim them from the left, repeatedly.
GLUE = {
    "The", "A", "An", "At", "To", "For", "From", "And", "Any", "This", "That",
    "Team", "Teams", "Winners", "Finalists", "Message", "Wins", "Who", "Each",
    "District", "Districts", "Regional", "Championship", "Division", "Divisions",
    "Section", "Table", "Points", "Award", "Awards", "One", "Two", "Both", "All",
    "Remaining", "Other", "Judged", "Culture", "Cultural", "Machine", "Submitted",
    "Star",  # column bleed from "Rookie All-Star Award" headers
}
# A real award name never ends up this short after trimming.
MINWORDS = 2


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().rstrip(".,;:")


def say(msg: str) -> None:
    """Windows consoles default to cp1252; PDF extractions carry U+FFFD. Never crash."""
    enc = (sys.stdout.encoding or "ascii")
    sys.stdout.write(msg.encode(enc, "replace").decode(enc, "replace") + chr(10))


def trim(name: str) -> str:
    w = name.split()
    while len(w) > MINWORDS and w[0] in GLUE:
        w.pop(0)
    return " ".join(w)


def harvest(path: str):
    """-> {award name: first line it was seen on}"""
    out = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = norm(raw)
            if "Award" not in line:
                continue
            # PDF column bleed shows up as 3+ spaces between tokens on the RAW line.
            bleed = "   " in raw.rstrip("\n")
            for m in CAND.finditer(line):
                nm = trim(norm(m.group(1)))
                if len(nm.split()) < MINWORDS:
                    continue
                if nm.split()[0] in GLUE:
                    continue
                if bleed and not nm.endswith(("Award", "Awards")):
                    continue
                if bleed and len(nm.split()) > 4:
                    continue
                out.setdefault(nm, line[:110])
    return out


def load(path: str) -> set:
    s = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for l in fh:
            l = l.strip()
            if l and not l.startswith("#"):
                s.add(norm(l))
                s.add(norm(l) + "s")
    return s


def main() -> int:
    a = sys.argv[1:]
    base_path, base_from = DEFAULT_BASELINE, None
    if "--baseline" in a:
        i = a.index("--baseline"); base_path = a[i + 1]; del a[i:i + 2]
    if "--baseline-from" in a:
        i = a.index("--baseline-from"); base_from = a[i + 1]; del a[i:i + 2]
    if not a:
        print(__doc__); return 2
    base = set(harvest(base_from)) if base_from else load(base_path)
    for b in list(base):                       # singular <-> plural are the same award
        base.add(b + "s" if not b.endswith("s") else b[:-1])
    label = os.path.basename(base_from or base_path)
    rc = 0
    for path in a:
        novel = {k: v for k, v in harvest(path).items() if k not in base}
        say("=== %s   (baseline: %s, %d known) ===" % (os.path.basename(path), label, len(base)))
        if not novel:
            say("  no novel award names -- roster matches baseline")
        for k in sorted(novel):
            say("  NEW/RENAMED: %-42s | first seen: %s" % (k, novel[k]))
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
