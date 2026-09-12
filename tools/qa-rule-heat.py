#!/usr/bin/env python3
"""qa-rule-heat.py -- how many official Q&A questions cite each rule, per season.

Q&A volume per rule is the single best public proxy for "this rule's wording is
ambiguous enough that hundreds of teams could not agree what it meant" -- which is
exactly where kickoff-day loophole hunting pays. Reads the *_QandA.pdf archive.

Writes research/rule_inventories/qa_heat_<year>.tsv and qa_heat_slots.tsv

The Q&A text is cached as research/rule_inventories/_text/qa_<year>.txt, which is the
output of `pdftotext -layout`. Neither the PDFs nor the cache are in the public
repository: bash tools/rebuild-corpus.sh --fetch downloads the PDFs, and
bash tools/rebuild-corpus.sh regenerates the cache.
"""
import argparse, io, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict

argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = f"{ROOT}/manuals/archive/frc"
OUT = f"{ROOT}/research/rule_inventories"
CACHE = f"{OUT}/_text"

QSPLIT = re.compile(r"^Q(\d+)\s", re.M)
RID = re.compile(r"\b([GRITHSEC])(\d{2,3})\b")

# A season counts if its Q&A PDF is on disk, or if its text cache already is.
years = {}
for fn in sorted(os.listdir(PDF)) if os.path.isdir(PDF) else []:
    m = re.match(r"(\d{4})_[A-Z]+_QandA\.pdf$", fn)
    if m:
        years[int(m.group(1))] = fn
for fn in sorted(os.listdir(CACHE)) if os.path.isdir(CACHE) else []:
    m = re.match(r"qa_(\d{4})\.txt$", fn)
    if m:
        years.setdefault(int(m.group(1)), None)
if not years:
    sys.exit("MISSING: manuals/archive/frc/<year>_<GAME>_QandA.pdf (no Q&A PDFs or text "
             "caches on disk; run: bash tools/rebuild-corpus.sh --fetch)")
need_pdftotext = [y for y, fn in years.items() if not os.path.exists(f"{CACHE}/qa_{y}.txt")]
if need_pdftotext and not shutil.which("pdftotext"):
    sys.exit("MISSING: pdftotext (needed to extract the Q&A text for %s; install poppler-utils "
             "or xpdf, or regenerate the caches with bash tools/rebuild-corpus.sh)"
             % ", ".join(map(str, sorted(need_pdftotext))))
os.makedirs(CACHE, exist_ok=True)

slot_hits = defaultdict(dict)
for y, fn in sorted(years.items()):
    txt = f"{CACHE}/qa_{y}.txt"
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", f"{PDF}/{fn}", txt],
                       check=True, capture_output=True)
    raw = open(txt, encoding="utf-8", errors="replace").read()
    parts = QSPLIT.split(raw)
    # parts = [pre, num, body, num, body, ...]
    qs = [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    c = Counter()
    for _, body in qs:
        for rid in {f"{a}{b}" for a, b in RID.findall(body)}:
            c[rid] += 1
    with open(f"{OUT}/qa_heat_{y}.tsv", "w", encoding="utf-8") as fh:
        fh.write("rule_id\tn_questions\tpct_of_qs\n")
        for rid, n in c.most_common():
            fh.write(f"{rid}\t{n}\t{100*n/max(len(qs),1):.1f}\n")
    print(f"\n=== {y} ({fn or 'qa_%d.txt' % y}): {len(qs)} Q&A entries, "
          f"{sum(c.values())} rule citations, {len(c)} distinct rules ===")
    print("   top 25 most-questioned rules:")
    for rid, n in c.most_common(25):
        print(f"     {rid:<6} {n:>4}  ({100*n/len(qs):.1f}% of all questions)")
    for rid, n in c.items():
        slot_hits[rid][y] = n

with open(f"{OUT}/qa_heat_slots.tsv", "w", encoding="utf-8") as fh:
    ys = sorted(years)
    fh.write("rule_id\t" + "\t".join(str(y) for y in ys) + "\ttotal\n")
    for rid in sorted(slot_hits, key=lambda r: (r[0], int(r[1:]))):
        row = [str(slot_hits[rid].get(y, 0)) for y in ys]
        fh.write(f"{rid}\t" + "\t".join(row) + f"\t{sum(slot_hits[rid].values())}\n")
print(f"\nOutputs -> {OUT}")
