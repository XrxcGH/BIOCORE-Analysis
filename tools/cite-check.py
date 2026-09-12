#!/usr/bin/env python3
"""
cite-check.py -- verify every rule citation in an AI-generated document against the
extracted Game Manual, and fail loudly on the ones that do not exist.

THE PROBLEM THIS SOLVES
-----------------------
An LLM asked "which rule governs X" will, some of the time, return a rule ID that is
plausible, well-formatted, adjacent to real rule numbers, and does not exist. It will do
this most often for the rules you most want -- edge cases and interactions, i.e. exactly
the loophole-hunt output of KICKOFF_PLAYBOOK.md Phase 4. Reading the answer will not catch
it. Grepping will.

This converts hallucination from a SILENT failure into a LOUD one. It is the single
cheapest safeguard in the whole AI-for-analysis stack: one command, exit code 1.

WHAT IT CHECKS
  1. EXISTS   -- every [A-Z]\\d{1,3} token in the doc is a real rule ID that season.
  2. QUOTED   -- any text inside "double quotes" immediately after a rule ID actually
                 appears in that rule's extracted body (normalised whitespace/quotes).
  3. DRIFT    -- optionally, whether that rule ID also existed in the baseline season, so
                 you can see when the model is answering from last year's manual.

INPUTS
  research/rule_inventories/<year>_rules_full.txt   (written by tools/rules-full.py; not in
                                                     the public repository, so run
                                                     bash tools/rebuild-corpus.sh first)

USAGE
  python tools/cite-check.py 2026 notes/loophole_pass.md
  python tools/cite-check.py 2027 strategies/BRIEF.md --baseline 2026
  python tools/cite-check.py 2026 --stdin < answer.txt
  echo "G410 says \\"a ROBOT may not\\"" | python tools/cite-check.py 2026 --stdin

Exit 0 = every citation verified. Exit 1 = at least one failed. Pure stdlib.
"""
import argparse, io, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "research", "rule_inventories")

# FRC rule IDs: one letter prefix + 1-3 digits. G/R/H/E/I/T/S/C/A/Q per rule-inventory.py.
RULE_RE = re.compile(r"\b([GRHEITSCAQ]\d{1,3})\b")
# a rule ID followed (within ~40 chars) by a double-quoted span = a claimed quotation
QUOTE_RE = re.compile(r"\b([GRHEITSCAQ]\d{1,3})\b[^\"“\n]{0,40}[\"“]([^\"”\n]{8,240})[\"”]")
STOP = {"G1", "R1", "T1", "E1", "I1", "S1", "A1", "C1", "H1", "Q1"}  # too generic to trust


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def load_rules(year):
    path = os.path.join(INV, "%s_rules_full.txt" % year)
    if not os.path.exists(path):
        sys.exit("MISSING: research/rule_inventories/%s_rules_full.txt (not in the public "
                 "repository; rebuild it with: bash tools/rebuild-corpus.sh)" % year)
    text = io.open(path, encoding="utf-8", errors="replace").read()
    rules, order = {}, []
    for m in re.finditer(r"### ([GRHEITSCAQ]\d{1,3})\s+\(p\.(\d+), (\d{4})\)\n=+\n(.*?)(?=\n=+\n### |\Z)",
                         text, re.S):
        rid, page, body = m.group(1), m.group(2), m.group(4)
        if rid not in rules:
            order.append(rid)
        rules[rid] = {"page": page, "body": body, "norm": norm(body)}
    if not rules:
        sys.exit("parsed 0 rules from %s -- inventory format changed?" % path)
    return rules, order


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year")
    ap.add_argument("doc", nargs="?", help="file to check (or use --stdin)")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--baseline", help="prior season to drift-check against, e.g. 2026")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    a = ap.parse_args()

    if a.stdin or not a.doc:
        doc = sys.stdin.read()
        label = "<stdin>"
    else:
        doc = io.open(a.doc, encoding="utf-8", errors="replace").read()
        label = a.doc

    rules, _ = load_rules(a.year)
    base = load_rules(a.baseline)[0] if a.baseline else None

    cited = sorted({r for r in RULE_RE.findall(doc)} - STOP,
                   key=lambda r: (r[0], int(r[1:])))
    missing = [r for r in cited if r not in rules]
    ok = [r for r in cited if r in rules]

    bad_quotes = []
    for m in QUOTE_RE.finditer(doc):
        rid, quoted = m.group(1), m.group(2)
        if rid in STOP:
            continue
        if rid not in rules:
            continue                      # already reported as missing
        if norm(quoted) not in rules[rid]["norm"]:
            bad_quotes.append((rid, quoted))

    drift = []
    if base:
        drift = [r for r in ok if r in base and norm(base[r]["body"])[:400] != rules[r]["norm"][:400]]
        only_baseline = [r for r in missing if r in base]
    else:
        only_baseline = []

    print("CITE-CHECK  doc=%s  season=%s  rule IDs cited=%d" % (label, a.year, len(cited)))
    if not a.quiet and ok:
        print("  VERIFIED (%d): %s" % (len(ok), " ".join(ok)))
    if missing:
        print("  !! DOES NOT EXIST IN %s (%d): %s" % (a.year, len(missing), " ".join(missing)))
        for r in only_baseline:
            print("     %s exists in %s but NOT %s -- the model answered from the OLD manual."
                  % (r, a.baseline, a.year))
    if bad_quotes:
        print("  !! QUOTE NOT FOUND IN RULE BODY (%d):" % len(bad_quotes))
        for rid, q in bad_quotes:
            print("     %s <- %r" % (rid, q[:110]))
    if drift and not a.quiet:
        print("  ~~ TEXT CHANGED vs %s (%d): %s" % (a.baseline, len(drift), " ".join(drift)))
        print("     Re-read these before relying on any %s-era reasoning about them." % a.baseline)
    fails = len(missing) + len(bad_quotes)
    print("  VERDICT: %s" % ("ALL CITATIONS VERIFIED" if not fails else "%d CITATION FAILURE(S)" % fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
