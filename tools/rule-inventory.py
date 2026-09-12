#!/usr/bin/env python3
"""
rule-inventory.py -- FRC Game Manual rule taxonomy extractor.

Extracts every numbered rule (G/R/H/E/I/T/S/C/A/Q prefixes) from archived FRC
Game Manual PDFs, captures full rule body text, then does cross-year analysis:

  1. per-year rule counts by prefix
  2. rule-ID presence matrix across years
  3. year-over-year body-text similarity for same-ID rules  -> evergreen vs churn
  4. content-based best-match linking ACROSS renumbering breaks (2023->2024)
  5. change report with before/after text for meaningfully-changed rules

Primary extraction path: PyMuPDF span geometry. Modern FRC manuals put the rule
ID in a bold span at the left text margin, followed by a bold headline span,
followed by regular body text. Fallback path: pdftotext -layout line regex
(needed for 2015-era manuals whose IDs are not bold left-margin spans).

Usage:
    python tools/rule-inventory.py                     # all years found
    python tools/rule-inventory.py --years 2022-2026
    python tools/rule-inventory.py --no-extract        # reuse cached JSONL
    python tools/rule-inventory.py --out DIR           # write somewhere else

Outputs land in research/rule_inventories/ unless --out is given. Every run rewrites the
cross-year tables for the requested window, so a narrow window replaces the published
2015-2026 tables. tools/rebuild-corpus.sh therefore runs this with --out and copies back
only <year>_bodies_v2.jsonl and the two _changes reports. A one-year window writes that
year's per-year files and leaves the cross-year tables alone.
"""

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

try:
    import pymupdf
except ImportError:  # older name
    import fitz as pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_DIR = os.path.join(ROOT, "manuals", "archive", "frc")
OUT_DIR = os.path.join(ROOT, "research", "rule_inventories")

# Rule prefixes seen across FRC history:
#   G game rules      R robot rules       H human rules (pre-2024)
#   E event rules (2024+, absorbed H)     I inspection rules
#   T tournament rules                    S safety rules (2016-2021)
#   C conduct/general (pre-2024) / C301 "wear your buttons" (2024+)
#   A arena/awards (2015-2018)            Q qualification (2024+, rare)
PREFIXES = "GRHEITSCAQ"
# 2017-2021 manuals zero-pad the number and suffix a period ("S01."); 2022+ do
# not ("G101"). Trailing "\s|$" rejects sub-item refs like "G15-A." and "G01-1.".
ANCHOR_RE = re.compile(r"^([" + PREFIXES + r"])(\d{1,3})\.?(?:\s|$)")
# fallback (text-mode) anchor: rule id at start of a line
FALLBACK_RE = re.compile(
    r"^\s{0,12}([" + PREFIXES + r"])(\d{1,3})\.?\s+(\*?\S.*)$")

HEADER_MARGIN = 46.0   # pts from top of page to ignore (running header)
FOOTER_MARGIN = 42.0   # pts from bottom to ignore (page number / version)

SECTION_RE = re.compile(r"^\d{1,2}(\.\d{1,2}){0,3}\s")


# ----------------------------------------------------------------- extraction

def find_manuals():
    """Map year -> path of the Game Manual PDF."""
    out = {}
    if not os.path.isdir(PDF_DIR):
        return out
    for fn in sorted(os.listdir(PDF_DIR)):
        if not fn.lower().endswith(".pdf"):
            continue
        if "GameManual" not in fn:
            continue
        if "Section" in fn:          # 2021 per-section splits; use the whole one
            continue
        m = re.match(r"^(\d{4})_", fn)
        if not m:
            continue
        year = int(m.group(1))
        out[year] = os.path.join(PDF_DIR, fn)
    return out


ROW_TOL = 4.0   # pts: two PDF "lines" this close vertically are one visual row


def page_spans(page):
    """Return visual rows, header/footer stripped.

    PyMuPDF often splits one printed line into several `line` records (the rule
    ID at x=36 and its headline at x=72 are separate records with near-equal y).
    Sorting purely by y then x mis-orders them whenever the y differs by a
    fraction of a point, which silently reattaches a rule's headline to the
    PRECEDING rule's body. So cluster lines into rows by y, then order by x.

    Each row is (y0, x0, spans) where spans is the row's spans left-to-right."""
    h = page.rect.height
    d = page.get_text("dict")
    lines = []
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            y0 = min(s["bbox"][1] for s in spans)
            if y0 < HEADER_MARGIN or y0 > h - FOOTER_MARGIN:
                continue
            x0 = min(s["bbox"][0] for s in spans)
            lines.append((y0, x0, spans))
    lines.sort(key=lambda t: (t[0], t[1]))
    rows = []
    for y0, x0, spans in lines:
        if rows and abs(y0 - rows[-1][0]) <= ROW_TOL:
            rows[-1][2].extend(spans)
        else:
            rows.append([y0, x0, list(spans)])
    out = []
    for y0, x0, spans in rows:
        spans.sort(key=lambda s: s["bbox"][0])
        out.append((round(y0, 1), round(spans[0]["bbox"][0], 1), spans))
    return out


def anchor_columns(doc):
    """Left-margin x0 values at which bold rule-ID spans start.

    Returns a set, not a single value: some manuals put different rule families
    in different indent columns (2016: G/R at x=57, T at x=75)."""
    xs = Counter()
    for pno in range(len(doc)):
        for y0, x0, spans in page_spans(doc[pno]):
            s = spans[0]
            t = s["text"].strip()
            if ANCHOR_RE.match(t) and "Bold" in s["font"] and s["bbox"][0] < 220:
                xs[round(s["bbox"][0])] += 1
    if not xs:
        return set()
    top = xs.most_common(1)[0][1]
    return {x for x, c in xs.items() if c >= max(5, top * 0.05)}


def near(x, cols, tol=4.0):
    return any(abs(x - c) <= tol for c in cols)


def extract_pymupdf(path):
    """Return list of rule dicts using span geometry."""
    doc = pymupdf.open(path)
    cols = anchor_columns(doc)
    if not cols:
        doc.close()
        return []
    rules = []
    cur = None
    for pno in range(len(doc)):
        printed = printed_page_number(doc[pno])
        for y0, x0, spans in page_spans(doc[pno]):
            s0 = spans[0]
            t0 = s0["text"].strip()
            m = ANCHOR_RE.match(t0)
            is_anchor = (
                m is not None
                and "Bold" in s0["font"]
                and near(s0["bbox"][0], cols)
            )
            line_text = " ".join(s["text"] for s in spans)
            line_text = re.sub(r"\s+", " ", line_text).strip()
            if is_anchor:
                if cur:
                    rules.append(cur)
                rid = m.group(1) + str(int(m.group(2)))  # strip 2017-era zero pad
                # headline = bold spans after the ID span, up to first non-bold
                head = []
                for s in spans[1:]:
                    if "Bold" in s["font"]:
                        head.append(s["text"])
                    elif head:
                        break
                headline = re.sub(r"\s+", " ", "".join(head)).strip()
                if not headline:
                    headline = line_text[len(t0):].strip()[:120]
                rest = line_text
                if rest.startswith(t0):
                    rest = rest[len(t0):].lstrip(" .")
                cur = {
                    "id": rid,
                    "raw_id": m.group(1) + m.group(2),
                    "prefix": m.group(1),
                    "num": int(m.group(2)),
                    "pdf_page": pno + 1,
                    "page": printed or (pno + 1),
                    "headline": headline.lstrip("*").strip(),
                    "starred": headline.startswith("*") or rest.startswith("*"),
                    "body": [rest],
                }
            elif cur is not None:
                # stop at a numbered section heading in bold at left margin
                if (
                    "Bold" in s0["font"]
                    and near(s0["bbox"][0], cols)
                    and SECTION_RE.match(t0 + " ")
                ):
                    rules.append(cur)
                    cur = None
                    continue
                cur["body"].append(line_text)
    if cur:
        rules.append(cur)
    doc.close()
    return rules


PAGENUM_RE = re.compile(r"\b(\d{1,3})\s+of\s+\d{1,3}\b")


def printed_page_number(page):
    h = page.rect.height
    txt = page.get_text()
    m = PAGENUM_RE.search(txt)
    if m:
        return int(m.group(1))
    return None


def extract_fallback(path):
    """pdftotext -layout line-regex path, for manuals PyMuPDF geometry misses."""
    try:
        raw = subprocess.run(
            ["pdftotext", "-layout", path, "-"],
            capture_output=True, text=True, errors="replace", timeout=300
        ).stdout
    except Exception as e:
        print(f"  ! pdftotext failed: {e}", file=sys.stderr)
        return []
    rules = []
    cur = None
    page = 1
    for line in raw.splitlines():
        if "\f" in line:
            page += line.count("\f")
            line = line.replace("\f", "")
        m = FALLBACK_RE.match(line)
        if m and len(m.group(3).strip()) > 8:
            if cur:
                rules.append(cur)
            rid = m.group(1) + str(int(m.group(2)))
            rest = m.group(3).strip()
            cur = {
                "id": rid, "raw_id": m.group(1) + m.group(2),
                "prefix": m.group(1), "num": int(m.group(2)),
                "pdf_page": page, "page": page,
                "headline": rest.lstrip("*").split(".")[0][:110].strip(),
                "starred": rest.startswith("*"),
                "body": [rest],
            }
        elif cur is not None:
            s = line.strip()
            if s:
                cur["body"].append(s)
    if cur:
        rules.append(cur)
    return rules


def finalize(rules):
    """Collapse body lines, normalize, dedupe repeat anchors (keep longest)."""
    best = {}
    for r in rules:
        body = re.sub(r"\s+", " ", " ".join(r["body"])).strip()
        body = body.replace("�", "'")
        r["text"] = body
        r["norm"] = normalize(body)
        r["sha1"] = hashlib.sha1(r["norm"].encode("utf8")).hexdigest()[:12]
        r["chars"] = len(body)
        r.pop("body", None)
        prev = best.get(r["id"])
        if prev is None or r["chars"] > prev["chars"]:
            best[r["id"]] = r
    return sorted(best.values(), key=lambda r: (r["prefix"], r["num"]))


WS = re.compile(r"[^a-z0-9 ]+")


def normalize(s):
    s = s.lower()
    s = WS.sub(" ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ------------------------------------------------------------------- analysis

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


_TOK_CACHE = {}


def _words(s):
    w = _TOK_CACHE.get(s)
    if w is None:
        w = s.split()[:900]
        _TOK_CACHE[s] = w
    return w


def ratio(a, b):
    """Word-level similarity. Char-level difflib is quadratic and far too slow
    on 3000-char rule bodies; token-level gives the same ranking ~100x faster."""
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, _words(a), _words(b),
                                   autojunk=False).ratio()


def tokset(norm):
    return set(norm.split())


def main():
    global OUT_DIR
    ap = argparse.ArgumentParser(
        description="FRC Game Manual rule taxonomy extractor. The manual PDFs are not in "
                    "the public repository: bash tools/rebuild-corpus.sh --fetch downloads them.")
    ap.add_argument("--years", default="2015-2026",
                    help="year window, e.g. 2022-2026 or 2027 (default 2015-2026)")
    ap.add_argument("--no-extract", action="store_true",
                    help="reuse <year>_bodies_v2.jsonl where it exists")
    ap.add_argument("--out", default=OUT_DIR,
                    help="output directory, also where --no-extract looks for cached JSONL "
                         "(default research/rule_inventories)")
    ap.add_argument("--classify", action="store_true", help="run stage 7 only")
    ap.add_argument("--crosswalk", action="store_true", help="run the concept crosswalk only")
    args = ap.parse_args()
    OUT_DIR = os.path.abspath(args.out)
    if args.classify:
        classify()
        return
    if args.crosswalk:
        crosswalk()
        return

    lo, hi = (args.years.split("-") + [args.years])[:2]
    lo, hi = int(lo), int(hi)

    manuals = {y: p for y, p in find_manuals().items() if lo <= y <= hi}
    cached = set()
    if args.no_extract and os.path.isdir(OUT_DIR):
        for fn in os.listdir(OUT_DIR):
            m = re.match(r"^(\d{4})_bodies_v2\.jsonl$", fn)
            if m and lo <= int(m.group(1)) <= hi:
                cached.add(int(m.group(1)))
    # Check before anything is written: a run with no inputs used to truncate the
    # published cross-year tables and then crash.
    if not manuals and not cached:
        sys.exit("MISSING: manuals/archive/frc/<year>_<GAME>_GameManual.pdf for %d-%d "
                 "(not in the public repository; run: bash tools/rebuild-corpus.sh --fetch)"
                 % (lo, hi))
    os.makedirs(OUT_DIR, exist_ok=True)
    data = {}

    for year in sorted(set(manuals) | cached):
        jl = os.path.join(OUT_DIR, f"{year}_bodies_v2.jsonl")
        if args.no_extract and os.path.exists(jl):
            data[year] = [json.loads(l) for l in open(jl, encoding="utf8")]
            print(f"{year}: cached {len(data[year])} rules")
            continue
        path = manuals[year]
        rules = finalize(extract_pymupdf(path))
        mode = "spans"
        if len(rules) < 40:
            fb = finalize(extract_fallback(path))
            if len(fb) > len(rules):
                rules, mode = fb, "layout"
        data[year] = rules
        with open(jl, "w", encoding="utf8") as f:
            for r in rules:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        tsv = os.path.join(OUT_DIR, f"{year}_rules_v2.tsv")
        with open(tsv, "w", encoding="utf8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["rule_id", "prefix", "num", "page", "chars", "starred",
                        "sha1", "headline"])
            for r in rules:
                w.writerow([r["id"], r["prefix"], r["num"], r["page"], r["chars"],
                            int(r["starred"]), r["sha1"], r["headline"]])
        print(f"{year}: {len(rules):4d} rules via {mode}  ({os.path.basename(path)})")

    years = sorted(data)
    if len(years) < 2:
        print(f"\none year in the window ({years[0]}): wrote its per-year files only. "
              "The cross-year tables need at least two years and were left untouched.")
        return

    # ---- 1. counts by prefix -------------------------------------------------
    allpfx = sorted({r["prefix"] for y in years for r in data[y]})
    with open(os.path.join(OUT_DIR, "_counts_by_prefix.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year"] + allpfx + ["TOTAL", "body_chars"])
        for y in years:
            c = Counter(r["prefix"] for r in data[y])
            w.writerow([y] + [c.get(p, 0) for p in allpfx] + [len(data[y]),
                        sum(r["chars"] for r in data[y])])
    print("\n--- RULE COUNTS BY PREFIX ---")
    hdr = "year  " + "  ".join(f"{p:>4}" for p in allpfx) + "   TOTAL   chars"
    print(hdr)
    for y in years:
        c = Counter(r["prefix"] for r in data[y])
        print(f"{y}  " + "  ".join(f"{c.get(p,0):4d}" for p in allpfx) +
              f"   {len(data[y]):5d}  {sum(r['chars'] for r in data[y]):6d}")

    # ---- 2. presence matrix --------------------------------------------------
    idx = {y: {r["id"]: r for r in data[y]} for y in years}
    allids = sorted({i for y in years for i in idx[y]},
                    key=lambda s: (s[0], int(s[1:])))
    with open(os.path.join(OUT_DIR, "_presence_matrix_v2.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rule_id"] + [str(y) for y in years] + ["n_years"])
        for rid in allids:
            row = [1 if rid in idx[y] else 0 for y in years]
            w.writerow([rid] + row + [sum(row)])

    # ---- 3. same-ID year-over-year similarity --------------------------------
    sim_rows = []
    for rid in allids:
        present = [y for y in years if rid in idx[y]]
        if len(present) < 2:
            continue
        pair_sims = []
        for a, b in zip(present, present[1:]):
            if b - a != 1:
                pair_sims.append((a, b, None))
                continue
            pair_sims.append((a, b, round(ratio(idx[a][rid]["norm"],
                                                idx[b][rid]["norm"]), 4)))
        vals = [s for _, _, s in pair_sims if s is not None]
        sim_rows.append({
            "rule_id": rid,
            "prefix": rid[0],
            "years": ",".join(str(y) for y in present),
            "n_years": len(present),
            "contiguous": int(present == list(range(present[0], present[-1] + 1))),
            "min_yoy": round(min(vals), 4) if vals else "",
            "mean_yoy": round(sum(vals) / len(vals), 4) if vals else "",
            "last_yoy": vals[-1] if vals else "",
            "headline_last": idx[present[-1]][rid]["headline"],
            "yoy_detail": ";".join(f"{a}->{b}:{s}" for a, b, s in pair_sims),
        })
    with open(os.path.join(OUT_DIR, "_similarity_v2.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sim_rows[0].keys()))
        w.writeheader()
        w.writerows(sim_rows)

    # ---- 4. content-based cross-year lineage (survives renumbering) ----------
    # link every rule in the newest year back through each earlier year
    newest = years[-1]
    toks = {y: {r["id"]: tokset(r["norm"]) for r in data[y]} for y in years}
    lineage = []
    for r in data[newest]:
        rt = toks[newest][r["id"]]
        row = {"id_%d" % newest: r["id"], "headline": r["headline"]}
        scores = []
        for y in years[:-1]:
            cands = sorted(
                ((jaccard(rt, toks[y][o["id"]]), o) for o in data[y]
                 if o["prefix"] in (r["prefix"], "H", "E", "C", "S", "A")),
                key=lambda t: -t[0])[:5]
            best_id, best_sc = "", 0.0
            for j, o in cands:
                sc = ratio(r["norm"], o["norm"])
                if sc > best_sc:
                    best_sc, best_id = sc, o["id"]
            row[f"m{y}"] = best_id
            row[f"s{y}"] = round(best_sc, 4)
            scores.append(best_sc)
        row["min_match"] = round(min(scores), 4) if scores else 0.0
        row["mean_match"] = round(sum(scores) / len(scores), 4) if scores else 0.0
        lineage.append(row)
    fields = ([f"id_{newest}", "headline"] +
              [k for y in years[:-1] for k in (f"m{y}", f"s{y}")] +
              ["min_match", "mean_match"])
    with open(os.path.join(OUT_DIR, "_lineage_v2.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(lineage)

    # ---- 5. consecutive-year CONTENT links (survive renumbering) -------------
    # FIRST renumbers rule blocks (2021->2022 wholesale; 2023->2024 the G/H/E
    # restructure; 2024->2025 the R4xx BUMPER block). Same-ID diffing therefore
    # lies at those boundaries, so link by best text match instead.
    links = []           # (yearA, yearB, idA, idB, sim, kind)
    # free[] is the SAME best-match search without the one-to-one constraint.
    # When FIRST splits one rule into two (2024 R408 BUMPER construction ->
    # 2025 R402/R403/R404/R405), the exclusive matcher can only give the
    # ancestor to one child and labels the siblings NEW, which would wrongly
    # read as "brand new rule". Chain-walking therefore uses free links; the
    # exclusive links stay the authority on splits, merges and drops.
    free = []
    for a, b in zip(years, years[1:]):
        if b - a != 1:
            continue
        used = set()
        pairs = []
        for r in data[b]:
            rt = toks[b][r["id"]]
            cands = sorted(((jaccard(rt, toks[a][o["id"]]), o) for o in data[a]),
                           key=lambda t: -t[0])[:8]
            best_sc, best = 0.0, None
            for j, o in cands:
                sc = ratio(r["norm"], o["norm"])
                if sc > best_sc:
                    best_sc, best = sc, o
            pairs.append((best_sc, r, best))
        for sc, r, o in pairs:
            free.append((a, b, o["id"] if o is not None else "", r["id"],
                         round(sc, 4)))
        for sc, r, o in sorted(pairs, key=lambda t: -t[0]):
            if o is None or sc < 0.40 or o["id"] in used:
                links.append((a, b, "", r["id"], round(sc, 4), "NEW"))
                continue
            used.add(o["id"])
            kind = ("VERBATIM" if sc >= 0.97 else
                    "MINOR" if sc >= 0.85 else
                    "REWRITTEN")
            if o["id"] != r["id"]:
                kind += "+RENUMBERED"
            links.append((a, b, o["id"], r["id"], round(sc, 4), kind))
        for o in data[a]:
            if o["id"] not in used:
                links.append((a, b, o["id"], "", 0.0, "DROPPED"))
    with open(os.path.join(OUT_DIR, "_links_v2.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year_a", "year_b", "id_a", "id_b", "sim", "kind",
                    "headline_b"])
        for a, b, ia, ib, s, k in links:
            hb = idx[b][ib]["headline"] if ib else idx[a][ia]["headline"]
            w.writerow([a, b, ia, ib, s, k, hb])
    with open(os.path.join(OUT_DIR, "_links_free_v2.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year_a", "year_b", "id_a", "id_b", "sim"])
        for a, b, ia, ib, s_ in free:
            w.writerow([a, b, ia, ib, s_])
    kindcount = Counter((f"{a}->{b}", k.split("+")[0]) for a, b, _, _, _, k in links)
    print("\n--- CONSECUTIVE-YEAR CONTENT LINK CLASSES ---")
    for a, b in zip(years, years[1:]):
        if b - a != 1:
            continue
        row = {k[1]: v for k, v in kindcount.items() if k[0] == f"{a}->{b}"}
        renum = sum(1 for x in links
                    if x[0] == a and "RENUMBERED" in x[5])
        print(f"{a}->{b}  verbatim={row.get('VERBATIM',0):3d} "
              f"minor={row.get('MINOR',0):3d} rewritten={row.get('REWRITTEN',0):3d} "
              f"new={row.get('NEW',0):3d} dropped={row.get('DROPPED',0):3d} "
              f"renumbered={renum:3d}")

    # ---- 6. change report for the modern block ------------------------------
    modern = [y for y in years if y >= 2022]
    changes = []
    for rid in allids:
        pres = [y for y in modern if rid in idx[y]]
        if len(pres) < 2:
            continue
        for a, b in zip(pres, pres[1:]):
            if b - a != 1:
                continue
            s = ratio(idx[a][rid]["norm"], idx[b][rid]["norm"])
            if s < 0.97:
                changes.append((round(s, 4), rid, a, b,
                                idx[a][rid]["text"], idx[b][rid]["text"]))
    changes.sort()
    # Both reports need two modern years; with fewer they are not written at all.
    if len(modern) >= 2:
        with open(os.path.join(OUT_DIR, "_changes_v2.md"), "w", encoding="utf8") as f:
            f.write(f"# Same-ID year-over-year rule text changes ({modern[0]}-{modern[-1]})\n")
            f.write(f"{len(changes)} same-ID transitions with similarity < 0.97\n\n")
            for s, rid, a, b, ta, tb in changes:
                f.write(f"\n## {rid}  {a} -> {b}   sim={s}\n")
                f.write(f"\n**{a}:** {ta[:2600]}\n")
                f.write(f"\n**{b}:** {tb[:2600]}\n")

        # content-linked change report (the trustworthy one)
        with open(os.path.join(OUT_DIR, "_changes_linked_v2.md"), "w",
                  encoding="utf8") as f:
            f.write("# Content-linked year-over-year rule changes\n\n")
            for a, b, ia, ib, s, k in sorted(
                    [x for x in links if x[0] >= 2022 and x[2] and x[3]
                     and x[4] < 0.97], key=lambda x: x[4]):
                f.write(f"\n## {ia} -> {ib}   {a}->{b}   sim={s}  [{k}]\n")
                f.write(f"\n**{a} {ia}:** {idx[a][ia]['text'][:2600]}\n")
                f.write(f"\n**{b} {ib}:** {idx[b][ib]['text'][:2600]}\n")

    # ---- summary -------------------------------------------------------------
    with open(os.path.join(OUT_DIR, "_summary_v2.txt"), "w", encoding="utf8") as f:
        f.write("years: %s\n" % years)
        for y in years:
            c = Counter(r["prefix"] for r in data[y])
            f.write(f"{y} total={len(data[y])} {dict(sorted(c.items()))}\n")
        allyr = [r for r in sim_rows if r["n_years"] == len(years)]
        f.write(f"\nIDs present in ALL {len(years)} years: {len(allyr)}\n")
        for r in sorted(allyr, key=lambda r: -(r["min_yoy"] or 0)):
            f.write(f"  {r['rule_id']:6s} min_yoy={r['min_yoy']} "
                    f"mean={r['mean_yoy']} :: {r['headline_last'][:70]}\n")
    print(f"\nwrote outputs to {OUT_DIR}")
    if len(modern) >= 2:
        print(f"changes (<0.97 sim, same ID, {modern[0]}-{modern[-1]}): {len(changes)}")
    else:
        print("change reports skipped: they need at least two years from 2022 on")




# ============================================================ classification
# Stage 7 (run with --classify, after the extraction/analysis pass above).
#
# WHY A SEPARATE STAGE: stages 1-6 are descriptive. This stage is prescriptive:
# it answers "on kickoff day, which slots of the new manual can I skip and which
# must I read word-by-word?"
#
# WHY CHAINS AND NOT DIRECT 2026-vs-YEAR-Y SIMILARITY: an evergreen rule that
# absorbs a 3% edit every season lands at ~0.75 direct similarity against a
# 9-year-old ancestor purely from accumulated drift, and would be misfiled as
# game-specific. What actually distinguishes evergreen from game-specific is
# whether ANY SINGLE year-over-year step rewrote it. So we walk the consecutive
# -year content links (stage 5, which survive FIRST's renumbering) backwards
# from each newest-manual rule and score the individual steps.
#
# Step similarity bands (word-level difflib ratio on normalized rule body):
#   >= 0.97  verbatim      -- whitespace/typo/cross-reference only
#   >= 0.80  edited        -- a clause moved, a noun or number swapped
#   <  0.80  rewritten     -- the rule now says something different
VERBATIM = 0.97
EDITED = 0.80

# 2015 and 2016 expose only G/R/T rules to the bold-gutter parser, so a chain
# cannot legitimately reach them for the conduct/inspection/safety families.
# 2017 is the first season in which every family parses, so "reaches 2017" is
# the evergreen bar.
EVERGREEN_YEAR = 2017


def _read_csv(path):
    with open(path, encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))


def _read_tsv(path):
    try:
        with open(path, encoding="utf8", newline="") as f:
            return list(csv.DictReader(f, delimiter="\t"))
    except FileNotFoundError:
        return []


CHAIN_FLOOR = 0.40   # below this the "ancestor" is noise, so the chain ends


def build_chains(links_rows, newest):
    # back[year_b][id_b] = (id_a, sim); links_rows are the FREE (non-exclusive)
    # best matches, so a rule that was split off a parent still inherits the
    # parent as its ancestor instead of being mislabelled brand new.
    back = defaultdict(dict)
    for r in links_rows:
        if not r["id_a"] or not r["id_b"]:
            continue
        if float(r["sim"]) < CHAIN_FLOOR:
            continue
        back[int(r["year_b"])][r["id_b"]] = (r["id_a"], float(r["sim"]))
    chains = {}
    ids_newest = {r["id_b"] for r in links_rows
                  if int(r["year_b"]) == newest and r["id_b"]}
    for rid in sorted(ids_newest):
        cur, y, steps, path = rid, newest, [], [(newest, rid)]
        while y in back and cur in back[y]:
            prev, sim = back[y][cur]
            steps.append((y - 1, y, sim, prev, cur))
            path.append((y - 1, prev))
            cur, y = prev, y - 1
        chains[rid] = {"steps": steps, "path": path,
                       "earliest": y, "depth": len(steps)}
    return chains


def classify():
    for fn in ("_links_v2.csv", "_links_free_v2.csv"):
        if not os.path.isfile(os.path.join(OUT_DIR, fn)):
            sys.exit("MISSING: %s (run python tools/rule-inventory.py first)"
                     % os.path.join(OUT_DIR, fn))
    links = _read_csv(os.path.join(OUT_DIR, "_links_v2.csv"))
    freelinks = _read_csv(os.path.join(OUT_DIR, "_links_free_v2.csv"))
    newest = max(int(r["year_b"]) for r in links)
    oldest = min(int(r["year_a"]) for r in links)
    chains = build_chains(freelinks, newest)
    # exclusive-match verdict for the newest transition: NEW here + a good free
    # ancestor = the rule was SPLIT off an existing rule, not invented.
    excl = {r["id_b"]: r["kind"] for r in links
            if int(r["year_b"]) == newest and r["id_b"]}

    heads = {}
    for r in _read_tsv(os.path.join(OUT_DIR, "%d_rules_v2.tsv" % newest)):
        heads[r["rule_id"]] = r["headline"]
    for rid in heads:
        chains.setdefault(rid, {"steps": [], "path": [(newest, rid)],
                                "earliest": newest, "depth": 0})

    rows = []
    for rid in sorted(heads, key=lambda s: (s[0], int(s[1:]))):
        c = chains[rid]
        sims = [s[2] for s in c["steps"]]
        verb = sum(1 for s in sims if s >= VERBATIM)
        edit = sum(1 for s in sims if EDITED <= s < VERBATIM)
        rewr = sum(1 for s in sims if s < EDITED)
        renum = sum(1 for s in c["steps"] if s[3] != s[4])
        reaches = c["earliest"] <= EVERGREEN_YEAR
        if reaches and rewr == 0:
            cls = "EVERGREEN"
        elif reaches:
            cls = "EVERGREEN-CONCEPT"
        elif c["depth"] >= 2 and rewr == 0:
            cls = "ANCHORED"
        elif c["depth"] >= 2:
            cls = "ANCHORED-CONCEPT"
        else:
            cls = "GAME-SPECIFIC"
        # churn over the three most recent transitions (2023->24->25->26)
        recent = sims[:3]
        rows.append({
            "rule_id": rid, "prefix": rid[0], "headline": heads[rid],
            "class": cls, "excl_kind_newest": excl.get(rid, ""),
            "depth": c["depth"], "earliest_year": c["earliest"],
            "verbatim_steps": verb, "edited_steps": edit,
            "rewritten_steps": rewr, "renumber_steps": renum,
            "min_step_sim": round(min(sims), 4) if sims else "",
            "recent3_moved": sum(1 for s in recent if s < VERBATIM),
            "recent3_rewritten": sum(1 for s in recent if s < EDITED),
            "steps": " ".join("%d>%d:%s=%.2f" % (a, b, ib if ia == ib else
                                                 "%s>%s" % (ia, ib), s)
                              for a, b, s, ia, ib in c["steps"]),
        })
    with open(os.path.join(OUT_DIR, "_taxonomy_%d.csv" % newest), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    tot = len(rows)
    print("--- CONTENT-CHAIN CLASS OF EVERY %d RULE (chains walked back to %d) ---"
          % (newest, oldest))
    cc = Counter(d["class"] for d in rows)
    ORDER = ("EVERGREEN", "EVERGREEN-CONCEPT", "ANCHORED", "ANCHORED-CONCEPT",
             "GAME-SPECIFIC")
    for k in ORDER:
        print("  %-18s %4d  (%4.1f%%)" % (k, cc.get(k, 0), 100.0 * cc.get(k, 0) / tot))
    print("  %-18s %4d" % ("TOTAL", tot))

    pf = sorted({d["prefix"] for d in rows})
    print("\n--- CLASS x PREFIX ---")
    print("%-18s " % "class" + "".join("%5s" % p for p in pf) + "  TOTAL")
    for k in ORDER:
        row = Counter(d["prefix"] for d in rows if d["class"] == k)
        print("%-18s " % k + "".join("%5d" % row.get(p, 0) for p in pf)
              + "%7d" % sum(row.values()))
    print("%-18s " % "TOTAL" + "".join(
        "%5d" % sum(1 for d in rows if d["prefix"] == p) for p in pf)
        + "%7d" % tot)

    # ---- hundred-block profile: where does churn actually live? ------------
    print("\n--- CHURN BY HUNDRED-BLOCK (%d manual) ---" % newest)
    print("block   n   evergreen+concept  anchored  game-spec   mean_recent3_moved")
    blocks = defaultdict(list)
    for d in rows:
        blocks[d["rule_id"][0] + str(int(d["rule_id"][1:]) // 100) + "xx"].append(d)
    for bk in sorted(blocks):
        b = blocks[bk]
        ev = sum(1 for d in b if d["class"].startswith("EVERGREEN"))
        an = sum(1 for d in b if d["class"].startswith("ANCHORED"))
        gs = sum(1 for d in b if d["class"] == "GAME-SPECIFIC")
        mv = sum(d["recent3_moved"] for d in b) / float(len(b))
        print("%-6s %3d   %8d          %8d  %8d        %.2f"
              % (bk, len(b), ev, an, gs, mv))

    # ---- read-first ranking ----------------------------------------------
    #   QA  teams could not parse it        (scraped official Q&A, 2024-2026)
    #   TU  FIRST could not leave it alone  (Team Updates, 2024-2026)
    #   GS  it is rewritten for the game    (chain class)
    #   MV  its text moved in the last 3 transitions (content-linked, so it is
    #       not fooled by the 2025 R4xx/G4xx renumbering)
    qa = {}
    for r in _read_tsv(os.path.join(OUT_DIR, "qa_heat_slots.tsv")):
        try:
            qa[r["rule_id"]] = sum(int(r[y]) for y in ("2024", "2025", "2026"))
        except (KeyError, ValueError, TypeError):
            pass
    tu = {}
    tp = os.path.join(ROOT, "research", "teamupdate_analysis",
                      "slot_churn_allseasons.tsv")
    for r in _read_tsv(tp):
        try:
            tu[r["rule_id"]] = int(r["total_mentions_2024plus"])
        except (KeyError, ValueError, TypeError):
            pass

    def nz(v, mx):
        return 0.0 if not mx else min(1.0, float(v) / mx)

    qamax = max(qa.values()) if qa else 1
    tumax = max(tu.values()) if tu else 1
    rank = []
    for d in rows:
        rid = d["rule_id"]
        q, t = qa.get(rid, 0), tu.get(rid, 0)
        gs = {"GAME-SPECIFIC": 1.0, "ANCHORED-CONCEPT": 0.6,
              "EVERGREEN-CONCEPT": 0.3}.get(d["class"], 0.0)
        mv = d["recent3_moved"] / 3.0
        score = 3.0 * nz(q, qamax) + 2.0 * nz(t, tumax) + 1.5 * gs + 1.5 * mv
        rank.append({"rule_id": rid, "prefix": d["prefix"], "class": d["class"],
                     "qa_2024_26": q, "tu_2024_26": t,
                     "recent3_moved": d["recent3_moved"],
                     "recent3_rewritten": d["recent3_rewritten"],
                     "score": round(score, 4), "headline": d["headline"]})
    rank.sort(key=lambda d: (-d["score"], d["rule_id"]))
    with open(os.path.join(OUT_DIR, "_readfirst_rank.csv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rank[0].keys()))
        w.writeheader()
        w.writerows(rank)
    print("\n--- READ-FIRST COMPOSITE (top 30 of %d) ---" % len(rank))
    print("rk rule  score  QA  TU mv rw  class              headline")
    for i, d in enumerate(rank[:30], 1):
        print("%2d %-5s %5.2f %3d %3d %2d %2d  %-18s %s"
              % (i, d["rule_id"], d["score"], d["qa_2024_26"], d["tu_2024_26"],
                 d["recent3_moved"], d["recent3_rewritten"], d["class"],
                 d["headline"][:50]))

    # ---- the evergreen core listing ---------------------------------------
    ever = [d for d in rows if d["class"] == "EVERGREEN"]
    ever.sort(key=lambda d: (d["prefix"], int(d["rule_id"][1:])))
    with open(os.path.join(OUT_DIR, "_evergreen_core.tsv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(ever)
    gsp = [d for d in rows if d["class"] in ("GAME-SPECIFIC", "ANCHORED-CONCEPT")]
    gsp.sort(key=lambda d: (d["prefix"], int(d["rule_id"][1:])))
    with open(os.path.join(OUT_DIR, "_gamespecific_core.tsv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(gsp)
    print("\nwrote _taxonomy_%d.csv _evergreen_core.tsv _gamespecific_core.tsv "
          "_readfirst_rank.csv -> %s" % (newest, OUT_DIR))


# --------------------------------------------------- concept crosswalk stage
# The chain stage above measures whether a rule's BODY survived. This stage
# measures whether its CONCEPT survived, by matching HEADLINES across years.
# The two answer different questions and the gap between them is the single
# most useful fact for kickoff triage: FRC keeps the concepts and moves the
# numbers. Run with --crosswalk.

def crosswalk():
    import unicodedata

    def rd(y):
        p = os.path.join(OUT_DIR, "%d_rules_v2.tsv" % y)
        with open(p, encoding="utf8", newline="") as f:
            return list(csv.DictReader(f, delimiter="\t"))

    def nh(s):
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
        s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
        return re.sub(r"\s+", " ", s).strip()

    years = []
    for fn in sorted(os.listdir(OUT_DIR)):
        m = re.match(r"^(\d{4})_rules_v2\.tsv$", fn)
        if m:
            years.append(int(m.group(1)))
    years = [y for y in years if y >= 2022]
    if len(years) < 2:
        sys.exit("MISSING: %s/<year>_rules_v2.tsv for two or more years from 2022 on "
                 "(run python tools/rule-inventory.py first)" % OUT_DIR)
    newest = years[-1]
    D = {y: rd(y) for y in years}
    H = {y: {r["rule_id"]: nh(r["headline"]) for r in D[y]} for y in years}

    rows, stats = [], defaultdict(Counter)
    for r in D[newest]:
        rid = r["rule_id"]
        h = H[newest][rid]
        row = {"rule_id": rid, "prefix": rid[0], "headline": r["headline"]}
        for y in years[:-1]:
            best, bs = "", 0.0
            for oid, oh in H[y].items():
                s = difflib.SequenceMatcher(None, h.split(), oh.split()).ratio()
                if s > bs:
                    bs, best = s, oid
            row["id%d" % y] = best if bs >= 0.60 else ""
            row["h%d" % y] = round(bs, 3)
            if bs >= 0.60:
                stats[y]["concept_recurs"] += 1
                stats[y]["same_slot" if best == rid else "moved_slot"] += 1
            else:
                stats[y]["concept_new"] += 1
        rows.append(row)
    fields = (["rule_id", "prefix", "headline"] +
              [k for y in years[:-1] for k in ("id%d" % y, "h%d" % y)])
    with open(os.path.join(OUT_DIR, "_concept_crosswalk.tsv"), "w",
              encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    n = len(D[newest])
    print("--- CONCEPT PERSISTENCE vs SLOT PERSISTENCE (%d rules of %d) ---"
          % (n, newest))
    print("vs year   concept recurs   same slot #   slot moved   concept is new")
    for y in years[:-1]:
        s = stats[y]
        print("%7d   %5d (%4.1f%%)   %5d (%4.1f%%)  %5d (%4.1f%%)  %5d (%4.1f%%)"
              % (y, s["concept_recurs"], 100.0 * s["concept_recurs"] / n,
                 s["same_slot"], 100.0 * s["same_slot"] / n,
                 s["moved_slot"], 100.0 * s["moved_slot"] / n,
                 s["concept_new"], 100.0 * s["concept_new"] / n))

    print("\n--- SAME QUESTION, BY PREFIX, %d vs %d ---" % (newest, newest - 1))
    y = newest - 1
    pf = sorted({r["prefix"] for r in rows})
    print("prefix    n   recurs  same slot  moved  new")
    for p in pf:
        sub = [r for r in rows if r["prefix"] == p]
        rec = [r for r in sub if r["id%d" % y]]
        same = [r for r in rec if r["id%d" % y] == r["rule_id"]]
        print("%6s %4d %8d %10d %6d %4d"
              % (p, len(sub), len(rec), len(same), len(rec) - len(same),
                 len(sub) - len(rec)))
    print("\nwrote _concept_crosswalk.tsv -> %s" % OUT_DIR)


if __name__ == "__main__":
    main()
