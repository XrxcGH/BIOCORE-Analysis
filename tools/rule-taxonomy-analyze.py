#!/usr/bin/env python3
"""
rule-taxonomy-analyze.py -- second pass over the output of rule-inventory.py.

WHY A SECOND PASS
-----------------
rule-inventory.py extracts rules structurally from each PDF and writes
research/rule_inventories/<year>_rules_full.txt.  Its ID-keyed stability tables are
misleading, because FIRST renumbered the rulebook FOUR times in the window
(2017->2019, 2021->2022, 2023->2024, 2024->2025 for the E series).  Comparing
"H506 in 2022" to "H506 in 2023" compares two unrelated rules.

This pass therefore ignores rule IDs entirely and matches rules SEMANTICALLY:
for every rule in year B, find the year-A rule whose normalized text is most
similar.  A rule is EVERGREEN if it has a high-similarity ancestor in every
year, regardless of what it was numbered.

It also excludes 2016 from the evergreen floor: the 2016 STRONGHOLD manual
carried only G and R rules in the bold-gutter format (the T/I/S/C sections used a
different typography the structural parser does not see), so every conduct rule
would falsely score 0 against 2016.

OUTPUTS (research/rule_inventories/)
    evergreen_semantic.tsv     every 2026 rule x its best ancestor in 2017..2025
    evergreen_5yr.tsv          same, restricted to the 2022..2025 window
    churn_semantic.tsv         year-over-year matched / edited / new counts
    churn_pairs_<a>_<b>.tsv    every year-A rule -> its year-B counterpart + sim
    volatility_2023_2026.tsv   rules tracked 2023->2024->2025->2026 with per-step sim

Usage: python tools/rule-taxonomy-analyze.py [--root <project root>]
"""

import argparse
import difflib
import os
import re
import sys
from collections import Counter, defaultdict

RULE_HDR = re.compile(r"^### ([GRITHSECA]\d{1,3})\s+\(p\.(\d+),\s*(\d{4})\)")
_WORD = re.compile(r"[a-z0-9]+")

# Similarity bands used throughout the report.
EVERGREEN_FLOOR = 0.75      # near-verbatim in every year checked
PERSISTENT_FLOOR = 0.55     # same concept, materially reworded
MATCH_FLOOR = 0.55          # below this, "no counterpart"

CMP_CAP = 1200              # difflib is O(n^2); the normative opening carries the ID
SHORTLIST = 6               # Jaccard prefilter width


def log(m):
    print(m, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ parsing
def parse_full(path):
    """Read a <year>_rules_full.txt back into {rule_id: {...}}."""
    rules, cur, field = {}, None, None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = RULE_HDR.match(line)
            if m:
                cur = {"id": m.group(1), "prefix": m.group(1)[0],
                       "num": int(m.group(1)[1:]), "page": int(m.group(2)),
                       "statement": "", "violation": "", "inset": ""}
                rules[cur["id"]] = cur
                field = None
                continue
            if cur is None:
                continue
            if line.startswith("STATEMENT: "):
                field = "statement"; cur[field] = line[11:]
            elif line.startswith("VIOLATION: "):
                field = "violation"; cur[field] = line[11:]
            elif line.startswith("BLUEBOX/NOTES: "):
                field = "inset"; cur[field] = line[15:]
            elif line.startswith("=") or not line.strip():
                field = None
            elif field:
                cur[field] += " " + line.strip()
    for r in rules.values():
        # headline = the bolded lead phrase, i.e. text before the first sentence stop
        h = r["statement"].lstrip("*").strip()
        r["headline"] = h.split(". ")[0][:110]
        r["body"] = " ".join(p for p in (r["statement"], r["violation"]) if p)
    return rules


def normalize(text):
    """Strip everything that renumbers or renames yearly, keep the normative core."""
    t = text.lower()
    t = re.sub(r"\b[grithseca]\d{1,3}\b", " <ref> ", t)          # cross-references
    t = re.sub(r"\btable\s*\d+[-\u2013]\d+\b", " <table> ", t)
    t = re.sub(r"\bfigure\s*\d+[-\u2013]\d+\b", " <figure> ", t)
    t = re.sub(r"[\u2018\u2019\u201c\u201d]", "'", t)
    t = re.sub(r"[^a-z0-9<>\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def toks(norm):
    return set(_WORD.findall(norm))


def ratio(a, b):
    return difflib.SequenceMatcher(None, a[:CMP_CAP], b[:CMP_CAP],
                                   autojunk=False).ratio()


def best_match(src_norm, src_tok, pool):
    """pool: [(id, norm, tokset)] -> (best_id, best_sim)."""
    if not pool:
        return None, 0.0
    scored = []
    for rid, nrm, tk in pool:
        u = len(src_tok | tk)
        scored.append((len(src_tok & tk) / u if u else 0.0, rid, nrm))
    scored.sort(key=lambda z: -z[0])
    best_id, best = None, 0.0
    for _, rid, nrm in scored[:SHORTLIST]:
        r = ratio(src_norm, nrm)
        if r > best:
            best_id, best = rid, r
    return best_id, best


def band(sim):
    if sim >= EVERGREEN_FLOOR:
        return "EVERGREEN"
    if sim >= PERSISTENT_FLOOR:
        return "PERSISTENT"
    return "GAME-SPECIFIC"


# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    root = args.root.replace("\\", "/").rstrip("/")
    d = f"{root}/research/rule_inventories"

    data = {}
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.match(r"(\d{4})_rules_full\.txt$", fn)
        if m:
            y = int(m.group(1))
            data[y] = parse_full(f"{d}/{fn}")
            log(f"loaded {y}: {len(data[y])} rules")
    years = sorted(data)
    if len(years) < 2:
        log(f"MISSING: research/rule_inventories/<year>_rules_full.txt (found {len(years)} "
            "year(s), need at least 2; rebuild them with: bash tools/rebuild-corpus.sh)")
        return 1

    norms = {y: {r: normalize(v["statement"]) for r, v in data[y].items()} for y in years}
    tk = {y: {r: toks(norms[y][r]) for r in data[y]} for y in years}
    pools = {y: [(r, norms[y][r], tk[y][r]) for r in data[y]] for y in years}

    # ---- 1. per-year counts by prefix ------------------------------------
    used = "GRITHSECA"
    print("\n=== 1. RULE COUNT BY PREFIX ===")
    print("year   " + "  ".join(f"{p:>4}" for p in used) + "   TOTAL")
    for y in years:
        c = Counter(r[0] for r in data[y])
        print(f"{y}   " + "  ".join(f"{c.get(p,0):>4}" for p in used)
              + f"   {len(data[y]):>5}")

    # ---- 2. year-over-year semantic churn --------------------------------
    print("\n=== 2. YEAR-OVER-YEAR SEMANTIC CHURN "
          "(ID-independent; every year-B rule matched back into year A) ===")
    print(f"{'pair':<12}{'B rules':>8}{'verbatim':>10}{'edited':>8}{'rewritten':>11}"
          f"{'new/none':>10}")
    churn_rows = []
    for a, b in zip(years, years[1:]):
        rows, cnt = [], Counter()
        for rid in sorted(data[b], key=lambda r: (r[0], int(r[1:]))):
            mid, sc = best_match(norms[b][rid], tk[b][rid], pools[a])
            rows.append((rid, mid, sc))
            cnt["verbatim" if sc >= 0.95 else
                "edited" if sc >= 0.75 else
                "rewritten" if sc >= MATCH_FLOOR else "new"] += 1
        with open(f"{d}/churn_pairs_{a}_{b}.tsv", "w", encoding="utf-8") as fh:
            fh.write(f"{b}_id\t{a}_ancestor\tsim\t{b}_headline\n")
            for rid, mid, sc in sorted(rows, key=lambda z: z[2]):
                fh.write(f"{rid}\t{mid or 'NONE'}\t{sc:.3f}\t{data[b][rid]['headline']}\n")
        churn_rows.append((a, b, len(data[b]), cnt))
        print(f"{a}->{b:<7}{len(data[b]):>8}{cnt['verbatim']:>10}{cnt['edited']:>8}"
              f"{cnt['rewritten']:>11}{cnt['new']:>10}")
    with open(f"{d}/churn_semantic.tsv", "w", encoding="utf-8") as fh:
        fh.write("from\tto\tto_rules\tverbatim_ge95\tedited_75_95\trewritten_55_75\tnew_lt55\n")
        for a, b, n, c in churn_rows:
            fh.write(f"{a}\t{b}\t{n}\t{c['verbatim']}\t{c['edited']}\t{c['rewritten']}"
                     f"\t{c['new']}\n")

    # ---- 3. evergreen scoring over the full-coverage window --------------
    newest = years[-1]
    # 2016 lacks T/I/S/C/H sections in the structural extraction -> would falsely
    # zero every conduct rule. Start the floor at the first year with >=5 prefixes.
    full_cov = [y for y in years
                if len({r[0] for r in data[y]}) >= 5 and y != newest]
    log(f"evergreen floor computed over {full_cov}")

    def score_window(window, path):
        rows = []
        for rid in sorted(data[newest], key=lambda r: (r[0], int(r[1:]))):
            per = {}
            for y in window:
                per[y] = best_match(norms[newest][rid], tk[newest][rid], pools[y])
            sims = [s for _, s in per.values()]
            rows.append({"id": rid, "prefix": rid[0],
                         "head": data[newest][rid]["headline"],
                         "min": min(sims), "mean": sum(sims) / len(sims),
                         "per": per,
                         "n_ge": sum(1 for s in sims if s >= EVERGREEN_FLOOR)})
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("rule_id\tprefix\tmin_sim\tmean_sim\tband\tyears_ge_0.75\t"
                     + "\t".join(f"{y}_id\t{y}_sim" for y in window) + "\theadline\n")
            for r in sorted(rows, key=lambda z: -z["min"]):
                cells = []
                for y in window:
                    mid, sc = r["per"][y]
                    cells += [mid or "-", f"{sc:.3f}"]
                fh.write(f"{r['id']}\t{r['prefix']}\t{r['min']:.3f}\t{r['mean']:.3f}\t"
                         f"{band(r['min'])}\t{r['n_ge']}/{len(window)}\t"
                         + "\t".join(cells) + f"\t{r['head']}\n")
        return rows

    rows_full = score_window(full_cov, f"{d}/evergreen_semantic.tsv")
    win5 = [y for y in years if newest - 4 <= y < newest]
    rows_5 = score_window(win5, f"{d}/evergreen_5yr.tsv")

    print(f"\n=== 3. EVERGREEN CLASSIFICATION of all {len(rows_full)} {newest} rules ===")
    for label, rows, win in (("full window", rows_full, full_cov),
                             ("5-year window", rows_5, win5)):
        b = Counter(band(r["min"]) for r in rows)
        print(f"  {label} {win[0]}-{win[-1]} ({len(win)} yrs): "
              f"EVERGREEN(min>={EVERGREEN_FLOOR}) {b['EVERGREEN']:>3} | "
              f"PERSISTENT {b['PERSISTENT']:>3} | GAME-SPECIFIC {b['GAME-SPECIFIC']:>3}")
        bp = defaultdict(Counter)
        for r in rows:
            bp[r["prefix"]][band(r["min"])] += 1
        print("     prefix  EVERGREEN  PERSISTENT  GAME-SPECIFIC   total")
        for p in used:
            if p in bp:
                c = bp[p]
                print(f"       {p}     {c['EVERGREEN']:>7}  {c['PERSISTENT']:>9}"
                      f"  {c['GAME-SPECIFIC']:>12}   {sum(c.values()):>6}")

    print(f"\n--- EVERGREEN CORE: {newest} rules with min sim >= {EVERGREEN_FLOOR} "
          f"across {full_cov[0]}-{full_cov[-1]} ---")
    ever = [r for r in rows_full if r["min"] >= EVERGREEN_FLOOR]
    for r in sorted(ever, key=lambda z: (z["prefix"], int(z["id"][1:]))):
        oldest = r["per"][full_cov[0]][0] or "-"
        print(f"   {r['id']:<6} min={r['min']:.2f} mean={r['mean']:.2f} "
              f"{full_cov[0]}={oldest:<6} {r['head'][:62]}")

    print(f"\n--- MOST GAME-SPECIFIC {newest} rules (lowest floor, full window) ---")
    for r in sorted(rows_full, key=lambda z: z["min"])[:55]:
        print(f"   {r['id']:<6} min={r['min']:.2f} mean={r['mean']:.2f}  "
              f"{r['head'][:66]}")

    # ---- 4. volatility of the last four seasons ---------------------------
    tail = [y for y in years if y >= newest - 3]
    if len(tail) == 4:
        chain = []
        for rid in sorted(data[newest], key=lambda r: (r[0], int(r[1:]))):
            steps, cur_y, cur_norm, cur_tok, path = [], newest, norms[newest][rid], \
                tk[newest][rid], [rid]
            ok = True
            for y in reversed(tail[:-1]):
                mid, sc = best_match(cur_norm, cur_tok, pools[y])
                steps.append(sc)
                if mid is None or sc < 0.30:
                    ok = False
                    path.append("NONE")
                    break
                path.append(mid)
                cur_norm, cur_tok = norms[y][mid], tk[y][mid]
            chain.append({"id": rid, "path": path, "steps": steps,
                          "min": min(steps) if steps else 0.0,
                          "head": data[newest][rid]["headline"], "complete": ok})
        with open(f"{d}/volatility_{tail[0]}_{newest}.tsv", "w", encoding="utf-8") as fh:
            fh.write("rule_id\tmin_step_sim\tchain_" + "_".join(str(y) for y in
                     reversed(tail)) + "\tstep_sims\theadline\n")
            for r in sorted(chain, key=lambda z: z["min"]):
                fh.write(f"{r['id']}\t{r['min']:.3f}\t{' <- '.join(r['path'])}\t"
                         f"{','.join(f'{s:.2f}' for s in r['steps'])}\t{r['head']}\n")
        print(f"\n=== 4. YEAR-CHAIN VOLATILITY {tail[0]}->{newest} "
              f"(each {newest} rule walked back one year at a time) ===")
        print("   most volatile rules that nonetheless exist in all four years:")
        stable_chain = [r for r in chain if r["complete"] and min(r["steps"]) >= 0.30]
        for r in sorted(stable_chain, key=lambda z: z["min"])[:35]:
            print(f"   {r['id']:<6} minstep={r['min']:.2f} "
                  f"[{','.join(f'{s:.2f}' for s in r['steps'])}] "
                  f"{' <- '.join(r['path'])}  {r['head'][:50]}")

    print(f"\nOutputs -> {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
