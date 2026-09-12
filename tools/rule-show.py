#!/usr/bin/env python3
"""rule-show.py -- print reconstructed rule text from the inventory dumps
(research/rule_inventories/<year>_rules_full.txt).

Usage:
  python tools/rule-show.py YEAR:ID [YEAR:ID ...]
  python tools/rule-show.py YEAR:/regex/         search that year's headlines
  python tools/rule-show.py YEAR ID [ID ...]     same as YEAR:ID for each ID
  python tools/rule-show.py ID [ID ...]          newest year that has a _rules_full.txt

RS_LIMIT=<chars> caps the printed body (default 1800).
The _rules_full.txt files are not in the public repository. bash tools/rebuild-corpus.sh
regenerates them from the game manual PDFs."""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "research", "rule_inventories")
LIMIT = int(os.environ.get("RS_LIMIT", "1800"))


def missing(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    sys.exit("MISSING: %s (not in the public repository; rebuild it with: "
             "bash tools/rebuild-corpus.sh)" % rel)


def newest_year():
    ys = []
    if os.path.isdir(D):
        for fn in os.listdir(D):
            m = re.match(r"(\d{4})_rules_full\.txt$", fn)
            if m:
                ys.append(m.group(1))
    return max(ys) if ys else None


args = sys.argv[1:]
if not args or args[0] in ("-h", "--help"):
    print(__doc__)
    sys.exit(0 if args else 2)

year, shown, texts = None, 0, {}
for arg in args:
    if re.fullmatch(r"\d{4}", arg):
        year = arg
        continue
    if ":" in arg:
        y, sel = arg.split(":", 1)
    else:
        y, sel = year or newest_year(), arg
        if y is None:
            missing(os.path.join(D, "<year>_rules_full.txt"))
    path = os.path.join(D, "%s_rules_full.txt" % y)
    if not os.path.isfile(path):
        missing(path)
    if path not in texts:
        texts[path] = open(path, encoding="utf-8").read()
    t = texts[path]
    shown += 1
    if sel.startswith("/"):
        pat = re.compile(sel.strip("/"), re.I)
        for m in re.finditer(r"### ([GRITHSECA]\d{1,3})\s+\(p\.(\d+), \d{4}\)\n=+\nSTATEMENT: (.*?)(?=\n)", t):
            if pat.search(m.group(3)):
                print(f"[{y}] {m.group(1)} p.{m.group(2)}  {m.group(3)[:150]}")
        continue
    m = re.search(r"### " + sel + r"\s+\(p\.(\d+), \d{4}\)\n=+\n(.*?)(?=\n=+\n### |\Z)", t, re.S)
    print(f"\n{'#'*70}\n### {y} {sel}" + (f"  (manual p.{m.group(1)})" if m else ""))
    print(m.group(2).strip()[:LIMIT] if m else "NOT FOUND")

if not shown:
    print(__doc__)
    sys.exit(2)
