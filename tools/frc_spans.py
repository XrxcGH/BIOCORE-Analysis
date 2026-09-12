#!/usr/bin/env python3
"""
frc_spans.py -- font/colour-aware extraction pass for FIRST Robotics Competition
game manuals (2022-2027 typesetting era, i.e. BIOCORE and its recent ancestors).

Why this exists: `pdftotext -layout` silently mis-attributes rule bodies (a rule's
wrapped text is emitted under the PREVIOUS rule id) and throws away the two signals
FIRST encodes in the *typography* rather than in the words:

  * EVERGREEN vs GAME-SPECIFIC.  Manual s1.6: "Evergreen rules ... are indicated with
    a leading asterisk and their rule number and headline are presented in bold green
    text ... All other rule headlines use bold blue text."  Green (g>b) => evergreen
    (low review priority, stable for years).  Blue => THIS SEASON'S GAME, read it all.
  * The glossary is a two-column table.  Terms are bold at x~41; definitions are
    regular at x~202.  Any line-oriented reader interleaves them into nonsense.

Outputs (all UTF-8, LF, tab-separated where tabular):
  spans.tsv        page  x0  y0  font  size  color  flags  text     (every span)
  lines.txt        reading-order text, one visual line per line, page markers
  rules.tsv        id  page  class  color  headline
  rules.json       {id: {page, class, color, headline, body, violations[]}}
  rule_ids.txt     sorted unique rule ids
  glossary.tsv     term  definition
  glossary.txt     terms only, sorted
  violations.tsv   rule_id  page  clause          (every "Violation:" clause)
  sections.tsv     level  page  title             (PDF bookmarks, else regex)

Usage:  python frc_spans.py <manual.pdf> --outdir DIR [--quiet]
Verified: Python 3.14 / PyMuPDF 1.28.2 against the 2022-2026 FRC Game Manuals.
"""
import argparse
import io
import json
import os
import re
import sys
from collections import Counter, OrderedDict

try:
    import pymupdf
except ImportError:                      # older wheels expose the same API as fitz
    import fitz as pymupdf

# Rule-letter prefixes FRC has used. 2026 REBUILT s1.6 declares Q,G,R,I,T,C,E.
# H and S are kept for older manuals and for anything BIOCORE invents.
PREFIXES = "QGRITHSEC"
# Rule-id token at the head of a gutter line. THREE eras, all supported:
#
#   2024-2026  "G416"        3 digits, id alone in the span, headline in the NEXT span, x~36
#   2022-2023  "G103"        3 digits, id alone in the span, headline in the NEXT span, x~72
#   2016-2021  "G1." / "G17. Don't ..."
#              1-2 digits AND a trailing period. Two sub-variants in the same manual:
#                (A) single-digit ids extract as their own span, headline on the FOLLOWING line
#                (B) two-digit ids extract with the headline glued into the SAME span
#              Beta test 2026-08-23: the old `^([PFX])(\d{3})$` full-match rejected every
#              pre-2024 id, so the 2019 manual yielded 0 rules and the pipeline reported success.
#
# Group 1 = prefix, group 2 = digits, group 3 = anything glued on after the id (variant B).
RULE_ID = re.compile(r"^([%s])(\d{1,3})\.?(?:\s+(.*))?$" % PREFIXES)
# The enforcement clause. Matched anywhere inside a paragraph, not just at its start:
# 2025 REEFSCAPE sets the clause with normal leading, so it merges into the preceding
# paragraph and a start-anchored pattern finds ~5 of ~90. "Violations of this rule ..."
# has no colon, so requiring the colon keeps prose out.
VIOLATION = re.compile(r"Violation[s]?\s*:", re.I)
FOOTER = re.compile(r"^Section\s+\d+.*Version:|^Version:\s*\S+\s+\d+\s+of\s+\d+")

YTOL = 3.0          # pts: baselines closer than this are the same visual line
PARA_GAP = 20.0     # pts: vertical gap that ends a paragraph (body leading is ~14.5)
# Rule-id column: x~36 in 2024-2026, x~72 in 2022-2023. Body cross-references to rules
# are regular weight, never bold, so a generous x cap costs nothing.
ID_XMAX = 120.0
GLOSS_XMAX = 150.0  # glossary term column x~41.6; definition column x~202.5


def is_bold(span):
    return "Bold" in span["font"] or bool(span["flags"] & 2 ** 4)


def classify_color(color_int):
    """FRC s1.6: bold GREEN headline = EVERGREEN, bold BLUE headline = game-specific."""
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    if g > b and g >= r:
        return "EVERGREEN"
    if b > g and b > r:
        return "GAMESPEC"
    return "UNKNOWN"


def page_lines(page):
    """Cluster spans into visual lines, in reading order.

    PyMuPDF emits the rule-id column and its headline as separate 'line' dicts whose
    baselines differ by ~0.5pt. Rounding y into fixed buckets (the obvious fix) drops
    them either side of a bucket edge and reverses their order -- which is exactly how
    a parser ends up pairing rule N's id with rule N-1's headline. Greedy clustering
    with a tolerance is order-stable.
    """
    spans = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk["lines"]:
            for sp in ln["spans"]:
                if sp["text"].strip():
                    spans.append(sp)
    spans.sort(key=lambda s: (s["bbox"][1], s["bbox"][0]))
    lines, cur, cur_y = [], [], None
    for sp in spans:
        y = sp["bbox"][1]
        if cur_y is None or abs(y - cur_y) <= YTOL:
            cur.append(sp)
            cur_y = y if cur_y is None else min(cur_y, y)
        else:
            lines.append(cur)
            cur, cur_y = [sp], y
    if cur:
        lines.append(cur)
    for ln in lines:
        ln.sort(key=lambda s: s["bbox"][0])
    return lines


def line_text(spans):
    out = ""
    for sp in spans:
        t = sp["text"]
        if out and not out.endswith((" ", "-")) and not t.startswith(" "):
            out += " "
        out += t
    return re.sub(r"[ \t]+", " ", out).strip()


def parse_glossary(doc):
    """Return OrderedDict{term: definition} read out of the two-column glossary table."""
    # The heading appears only on the FIRST glossary page; continuation pages carry no heading.
    # Collecting only heading-matching pages truncated the 2019 glossary to 16 of its terms
    # (it runs pp.129-133) and produced 0 for 2017/2018. The glossary is conventionally the
    # last section of an FRC manual, so take a contiguous run from the first heading to the
    # end of the document. Non-glossary lines are filtered by the term/definition column test
    # below, so over-reach costs nothing.
    gloss_pages = []
    for i, p in enumerate(doc):
        head = p.get_text()[:300]
        if re.search(r"^\s*(?:Section\s+)?\d*\s*Glossary\b", head, re.M | re.I):
            gloss_pages = list(range(i, doc.page_count))
            break
    gloss = OrderedDict()
    term = None
    for i in gloss_pages:
        for spans in page_lines(doc[i]):
            txt = line_text(spans)
            if re.match(r"^(?:Section\s+)?\d*\s*Glossary\b", txt) or FOOTER.match(txt):
                continue
            left = [s for s in spans if s["bbox"][0] < GLOSS_XMAX]
            right = [s for s in spans if s["bbox"][0] >= GLOSS_XMAX]
            if left and is_bold(left[0]):
                cand = line_text(left).strip()
                if re.fullmatch(r"[A-Z][A-Z0-9 &/'’()\.\-]{1,44}", cand):
                    term = cand.strip()
                    gloss.setdefault(term, [])
                else:
                    left, right = [], spans
            if term is not None and right:
                gloss[term].append(line_text(right))
    return OrderedDict((t, re.sub(r"\s+", " ", " ".join(d)).strip()) for t, d in gloss.items())


def parse_rules(all_lines):
    """Walk the reading-order line stream and cut it into rules."""
    rules, order = OrderedDict(), []
    cur = None
    prev_y, prev_page = None, None
    pending = None          # a rule whose headline lives on the FOLLOWING line (pre-2024 variant A)
    for pno, y, x0, txt, spans in all_lines:
        first = spans[0]
        m = RULE_ID.match(first["text"].strip())
        if m and is_bold(first) and first["bbox"][0] < ID_XMAX:
            rid = m.group(1) + m.group(2)     # normalised: no trailing period
            inline = (m.group(3) or "").strip()
            headline, color, tail = "", None, []
            xid = first["bbox"][0]
            if inline:
                # variant B: id and headline extracted as one span.
                headline = inline
                color = first["color"]
            for sp in spans[1:]:
                if is_bold(sp) and sp["bbox"][0] > xid + 4 and not tail:
                    headline += sp["text"]
                    if color is None:
                        color = sp["color"]
                else:
                    tail.append(sp)
            headline = headline.strip()
            if color is None and first["color"]:
                color = first["color"]   # 2022-2023: the id token itself carries the colour
            klass = classify_color(color) if color is not None else "UNKNOWN"
            if headline.startswith("*") and klass != "EVERGREEN":
                klass = "EVERGREEN"      # asterisk is the documented tie-breaker
            cur = {"id": rid, "page": pno, "class": klass,
                   "color": ("#%06x" % color) if color is not None else "",
                   "headline": headline, "body": [], "violations": []}
            rules[rid] = cur
            order.append(rid)
            # Pre-2024 variant A: the id sits alone in the gutter and the headline is the NEXT
            # visual line, indented to the body column. Arm a one-line lookahead.
            pending = cur if not headline else None
            cur["_xid"] = xid
            rest = line_text(tail)
            if rest:
                cur["body"].append(rest)
        elif pending is not None and not FOOTER.match(txt) and txt.strip():
            # Resolve the armed lookahead. Accept the line as the headline when it is indented
            # past the id column; take the colour from it too, since in this layout the headline
            # carries the styling. Otherwise fall through and treat it as ordinary body.
            if x0 > pending.get("_xid", 0) + 4:
                pending["headline"] = txt.strip()
                if spans and spans[0].get("color") is not None and not pending["color"]:
                    pending["color"] = "#%06x" % spans[0]["color"]
                    k = classify_color(spans[0]["color"])
                    if k != "UNKNOWN":
                        pending["class"] = k
                if pending["headline"].startswith("*"):
                    pending["class"] = "EVERGREEN"
            else:
                pending["body"].append(txt)
            pending = None
        elif cur is not None and not FOOTER.match(txt):
            gap = None if prev_page != pno or prev_y is None else y - prev_y
            cur["body"].append(("\n" if (gap is not None and gap > PARA_GAP) else "") + txt)
        prev_y, prev_page = y, pno

    for r in rules.values():
        r.pop("_xid", None)

    for rid, r in rules.items():
        # Body lines were collected with a leading "\n" ONLY where the vertical gap said
        # "new paragraph". Join with spaces so a wrapped sentence stays one paragraph --
        # joining with "\n" would make every wrapped line its own paragraph and would cut
        # two-line Violation clauses in half.
        body = " ".join(r["body"])
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n+", body) if p.strip()]
        if paras:
            paras[0] = paras[0].lstrip(". ").strip()   # headline punctuation is a separate span
        for p in paras:
            hits = [mm.start() for mm in VIOLATION.finditer(p)]
            for k, start in enumerate(hits):
                end = hits[k + 1] if k + 1 < len(hits) else len(p)
                r["violations"].append(p[start:end].strip())
        r["body"] = "\n\n".join(paras)
    return rules, order


def extract(pdf_path, outdir, quiet=False):
    doc = pymupdf.open(pdf_path)
    os.makedirs(outdir, exist_ok=True)

    def out(name):
        return io.open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n")

    # ---- pass 1: every span + the reading-order line stream -----------------
    all_lines = []
    fh_spans, fh_lines = out("spans.tsv"), out("lines.txt")
    fh_spans.write("page\tx0\ty0\tfont\tsize\tcolor\tflags\ttext\n")
    for pno, page in enumerate(doc, 1):
        fh_lines.write("<<<PAGE %d>>>\n" % pno)
        for spans in page_lines(page):
            for sp in spans:
                fh_spans.write("%d\t%.1f\t%.1f\t%s\t%.1f\t#%06x\t%d\t%s\n" % (
                    pno, sp["bbox"][0], sp["bbox"][1], sp["font"], sp["size"],
                    sp["color"], sp["flags"], sp["text"].replace("\t", " ").rstrip()))
            txt = line_text(spans)
            fh_lines.write(txt + "\n")
            all_lines.append((pno, spans[0]["bbox"][1], spans[0]["bbox"][0], txt, spans))
    fh_spans.close()
    fh_lines.close()

    # ---- pass 2: glossary ---------------------------------------------------
    gloss = parse_glossary(doc)
    with out("glossary.tsv") as fh:
        fh.write("term\tdefinition\n")
        for t, d in gloss.items():
            fh.write("%s\t%s\n" % (t, d))
    with out("glossary.txt") as fh:
        for t in sorted(gloss):
            fh.write(t + "\n")

    # ---- pass 3: rules, violations -----------------------------------------
    rules, order = parse_rules(all_lines)
    nviol = 0
    with out("violations.tsv") as fh:
        fh.write("rule_id\tpage\tclause\n")
        for rid in order:
            r = rules[rid]
            for v in r["violations"]:
                fh.write("%s\t%d\t%s\n" % (rid, r["page"], v.replace("\t", " ")))
                nviol += 1
    # ---- era guard on the EVERGREEN/GAMESPEC colour split, BEFORE anything is written ----
    # The green=evergreen / blue=game-specific encoding is a 2023+ convention (manual s1.6).
    # Older manuals set every rule headline in ONE decorative colour and classify_color()
    # reads that single hue as a verdict: 2018 came out "185 GAMESPEC" and 2020/2021 "164
    # GAMESPEC" -- every rule flagged new-this-season, which is false and more dangerous
    # than saying nothing. Self-calibrating: the encoding is only real if BOTH classes
    # actually appear; if every rule lands in one class the colour is decorative.
    klass = Counter(r["class"] for r in rules.values())
    colour_encoding = klass.get("EVERGREEN", 0) > 0 and klass.get("GAMESPEC", 0) > 0
    if rules and not colour_encoding:
        for r in rules.values():
            r["class"] = "UNKNOWN"

    with out("rules.tsv") as fh:
        fh.write("id\tpage\tclass\tcolor\theadline\n")
        for rid in order:
            r = rules[rid]
            fh.write("%s\t%d\t%s\t%s\t%s\n" % (
                rid, r["page"], r["class"], r["color"], r["headline"].replace("\t", " ")))
    with out("rule_ids.txt") as fh:
        for rid in sorted(rules):
            fh.write(rid + "\n")
    with out("rules.json") as fh:
        json.dump({"source": os.path.basename(pdf_path), "pages": doc.page_count,
                   "order": order, "rules": rules, "glossary": gloss},
                  fh, indent=1, ensure_ascii=False)

    # ---- pass 4: section map ------------------------------------------------
    toc = doc.get_toc()
    with out("sections.tsv") as fh:
        fh.write("level\tpage\ttitle\n")
        if toc:
            for lvl, title, pg in toc:
                fh.write("%d\t%d\t%s\n" % (lvl, pg, re.sub(r"\s+", " ", title).strip()))
        else:
            seen = set()
            for pno, y, x0, txt, spans in all_lines:
                m = re.match(r"^(\d{1,2}(?:\.\d{1,2}){0,2})\s+(\S.*)$", txt)
                if m and is_bold(spans[0]) and spans[0]["size"] >= 12 and m.group(1) not in seen:
                    seen.add(m.group(1))
                    fh.write("%d\t%d\t%s %s\n" % (m.group(1).count(".") + 1, pno,
                                                  m.group(1), m.group(2)[:90]))

    klass = Counter(r["class"] for r in rules.values())   # post-guard, matches what was written
    pref = Counter(rid[0] for rid in rules)
    stats = {"pages": doc.page_count, "lines": len(all_lines), "rules": len(rules),
             "glossary": len(gloss), "violations": nviol, "toc": len(toc),
             "colour_encoding": colour_encoding,
             "class": dict(klass), "prefix": dict(pref)}
    if not quiet:
        print("   pages=%d  lines=%d  rules=%d  glossary=%d  violations=%d  toc=%d"
              % (stats["pages"], stats["lines"], stats["rules"], stats["glossary"],
                 stats["violations"], stats["toc"]))
        print("   class:    " + "  ".join("%s=%d" % kv for kv in sorted(klass.items())))
        if not colour_encoding and rules:
            print("   [!] NO EVERGREEN/GAMESPEC COLOUR ENCODING in this manual (pre-2023 era).")
            print("       Every rule is reported UNKNOWN. The 'which rules are new this season'")
            print("       split is UNAVAILABLE here -- derive it from the rule-id diff instead.")
        print("   prefixes: " + "  ".join("%s=%d" % kv for kv in sorted(pref.items())))
    with out("stats.json") as fh:
        json.dump(stats, fh, indent=1)
    doc.close()
    return stats


def main():
    ap = argparse.ArgumentParser(description="font/colour-aware FRC manual extractor")
    ap.add_argument("pdf")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.pdf):
        sys.exit("no such file: %s (FIRST's manuals are not in the public repository; "
                 "download them with: bash tools/rebuild-corpus.sh --fetch)" % a.pdf)
    extract(a.pdf, a.outdir, a.quiet)


if __name__ == "__main__":
    main()
