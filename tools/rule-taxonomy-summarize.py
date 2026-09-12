#!/usr/bin/env python3
"""rule-taxonomy-summarize.py -- turn evergreen_semantic.tsv into the taxonomy buckets.

A flat "min similarity across all years" mislabels any rule whose SECTION did not
exist for the whole window (the E-series Event Rules were only folded into the game
manual in 2024; before that they lived in the separate Event Experience document).
So for each 2026 rule we find the FIRST year an ancestor appears at all (sim>=0.55)
and score stability only from that year forward:

    EVERGREEN   ancestor in every year of the window AND min sim >= 0.75
    ANCHORED    ancestor since year Y < 2026 AND min sim from Y >= 0.75
    PERSISTENT  ancestor in every year but min sim 0.55-0.75 (concept survives, text churns)
    GAME-SPECIFIC  no stable ancestor chain
"""
import argparse, io, os, re, sys
from collections import Counter, defaultdict

argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "research", "rule_inventories")
if not os.path.isfile(os.path.join(D, "evergreen_semantic.tsv")):
    sys.exit("MISSING: research/rule_inventories/evergreen_semantic.tsv "
             "(write it with: python tools/rule-taxonomy-analyze.py)")
rows = [l.rstrip("\n").split("\t") for l in open(f"{D}/evergreen_semantic.tsv", encoding="utf-8")]
hdr, rows = rows[0], rows[1:]
# Per-year columns only: the header also carries min_sim and mean_sim.
years = [int(h[:4]) for h in hdr if re.fullmatch(r"\d{4}_sim", h)]
idx = {y: hdr.index(f"{y}_sim") for y in years}
ididx = {y: hdr.index(f"{y}_id") for y in years}

out = []
for r in rows:
    sims = {y: float(r[idx[y]]) for y in years}
    ids = {y: r[ididx[y]] for y in years}
    first = None
    for y in years:
        if sims[y] >= 0.55:
            first = y
            break
    if first is None:
        cls, floor, since = "GAME-SPECIFIC", max(sims.values()), None
    else:
        tailyrs = [y for y in years if y >= first]
        floor = min(sims[y] for y in tailyrs)
        gaps = [y for y in tailyrs if sims[y] < 0.55]
        since = first
        if gaps:
            cls = "GAME-SPECIFIC"
        elif floor >= 0.75:
            cls = "EVERGREEN" if first == years[0] else "ANCHORED"
        else:
            cls = "PERSISTENT"
    out.append({"id": r[0], "prefix": r[1], "cls": cls, "floor": floor,
                "since": since, "head": r[-1], "sims": sims, "ids": ids})

print("=== TAXONOMY BUCKETS (each 2026 rule vs its best semantic ancestor per year) ===")
print(f"window: {years[0]}-{years[-1]} + 2026\n")
b = Counter(o["cls"] for o in out)
for k in ("EVERGREEN", "ANCHORED", "PERSISTENT", "GAME-SPECIFIC"):
    print(f"  {k:<15}{b[k]:>4}")
print("\n  prefix   EVERGREEN  ANCHORED  PERSISTENT  GAME-SPECIFIC  total")
bp = defaultdict(Counter)
for o in out:
    bp[o["prefix"]][o["cls"]] += 1
for p in sorted(bp):
    c = bp[p]
    print(f"    {p}      {c['EVERGREEN']:>7}  {c['ANCHORED']:>8}  {c['PERSISTENT']:>10}"
          f"  {c['GAME-SPECIFIC']:>13}  {sum(c.values()):>5}")

for k in ("EVERGREEN", "ANCHORED", "PERSISTENT"):
    sel = [o for o in out if o["cls"] == k]
    print(f"\n--- {k} ({len(sel)}) ---")
    for o in sorted(sel, key=lambda z: (z["prefix"], int(z["id"][1:]))):
        anc = o["ids"][o["since"]]
        print(f"  {o['id']:<6} floor={o['floor']:.2f} since={o['since']} "
              f"({o['since']}:{anc:<6}) {o['head'][:70]}")

sel = [o for o in out if o["cls"] == "GAME-SPECIFIC"]
print(f"\n--- GAME-SPECIFIC ({len(sel)}), sorted by peak similarity to any prior year ---")
for o in sorted(sel, key=lambda z: -z["floor"]):
    print(f"  {o['id']:<6} best={o['floor']:.2f}  {o['head'][:74]}")

with open(f"{D}/taxonomy_buckets.tsv", "w", encoding="utf-8") as fh:
    fh.write("rule_id\tprefix\tclass\tfloor_sim\tancestor_since\tancestor_id\theadline\n")
    for o in sorted(out, key=lambda z: (z["cls"], z["prefix"], int(z["id"][1:]))):
        fh.write(f"{o['id']}\t{o['prefix']}\t{o['cls']}\t{o['floor']:.3f}\t"
                 f"{o['since'] or '-'}\t{o['ids'].get(o['since'],'-')}\t{o['head']}\n")
print(f"\nOutput -> {D}/taxonomy_buckets.tsv")
