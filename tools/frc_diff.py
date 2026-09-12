#!/usr/bin/env python3
"""
frc_diff.py -- diff two frc_spans.py extractions and mine the new one for the two
signals a student reader always misses:

  1. WHAT ACTUALLY CHANGED. Rule-id set diff (ADDED / REMOVED) plus, for every id
     present in both, a text-similarity score on the rule body (CHANGED). A rule that
     kept its number but lost one clause is the single most expensive thing to miss,
     and it is invisible to an id-set diff.
  2. ALL-CAPS TERMS USED BUT NEVER DEFINED. FRC s1.6 promises "Key words that have a
     particular meaning ... are defined in the Glossary and indicated in ALL CAPS".
     Every ALL-CAPS token in the body with no glossary entry is either a typo, an
     acronym, or -- the interesting case -- a load-bearing term FIRST forgot to define.
     Undefined terms are where rule arguments get won.

Usage:
  python frc_diff.py --new  WORKDIR/spans \
                     --base BASEDIR/spans \
                     --outdir WORKDIR \
                     [--stoplist tools/caps_stoplist_frc.txt] \
                     [--changed-threshold 0.995]

Inputs are the output directories of frc_spans.py (rules.json + lines.txt + sections.tsv).

Outputs (in --outdir):
  rules_ADDED.txt            ids in NEW, absent from BASE       <- read every one
  rules_REMOVED.txt          ids in BASE, absent from NEW       <- what got deleted, and why
  rules_CHANGED.tsv          id  ratio  class  headline_base -> headline_new
  rules_CHANGED_DETAIL.txt   unified diff of every changed rule body
  rules_UNCHANGED.txt        ids whose body text is byte-identical
  rules_GAMESPECIFIC.tsv     blue-headline rules = THIS SEASON'S GAME
  rules_EVERGREEN.tsv        green-asterisk rules = carried over
  glossary_ADDED.txt         new defined terms = the new game's nouns
  glossary_REMOVED.txt       terms FIRST stopped defining
  glossary_CHANGED.tsv       term  ratio  base_definition -> new_definition
  UNDEFINED_CAPS.tsv         token  count  first_page  sample line
  UNDEFINED_CAPS_PHRASES.tsv phrase count  first_page  undefined_words
"""
import argparse
import difflib
import io
import json
import os
import re
import sys
from collections import Counter, OrderedDict

RULE_ID = re.compile(r"^[QGRITHSEC]\d{3}$")
CAPS_PHRASE = re.compile(r"\b[A-Z][A-Z0-9’'\-]{2,}(?:\s+[A-Z][A-Z0-9’'\-]{2,})*\b")
LOOKS_LIKE_ID = re.compile(r"^[A-Z]\d+$|^\d+$|^[A-Z]{1,2}\d{2,}$")
# Vendor part numbers and rule sub-clause pointers: VH-109, WCP-0941, REV-11-1850,
# NP18-12B, OM5P-AC, R504-B, B12ME522. Anything with a digit AND a hyphen, or an
# alpha prefix immediately followed by digits, is hardware, not game vocabulary.
PART_NUM = re.compile(r"^(?=.*\d)[A-Z0-9]+(?:-[A-Z0-9]+)+$|^[A-Z]{2,}\d[A-Z0-9]*$")
PAGE_MARK = re.compile(r"^<<<PAGE (\d+)>>>$")


def load(dirname):
    if not os.path.isfile(os.path.join(dirname, "rules.json")):
        sys.exit("MISSING: %s (run tools/frc_spans.py on the manual first; "
                 "bash tools/rebuild-corpus.sh rebuilds the published validation run)"
                 % os.path.join(dirname, "rules.json"))
    with io.open(os.path.join(dirname, "rules.json"), encoding="utf-8") as fh:
        return json.load(fh)


def norm(text):
    return re.sub(r"\s+", " ", (text or "")).strip()


def read_stoplist(path):
    stop = set()
    if path and os.path.isfile(path):
        with io.open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    stop.add(line.upper())
    return stop


def base_token(tok):
    """Strip possessives and line-break hyphens: ALLIANCE’S -> ALLIANCE, FIELD- -> FIELD."""
    t = tok.upper().strip()
    t = re.sub(r"[’'’]S$", "", t)
    t = t.rstrip("-’'’")
    return t


def singularish(term):
    """Return the variants of a term that should count as 'the same term'."""
    out = {term}
    if term.endswith("’S") or term.endswith("'S"):
        out.add(term[:-2])
    if term.endswith("S") and len(term) > 3:
        out.add(term[:-1])
    if term.endswith("ES") and len(term) > 4:
        out.add(term[:-2])
    out.add(term + "S")
    out.add(term + "ES")
    return out


def glossary_key(gloss):
    keys = set()
    for t in gloss:
        keys |= singularish(t.upper())
        for w in t.upper().split():
            keys |= singularish(w)
    return keys


def glossary_start_page(spans_dir):
    path = os.path.join(spans_dir, "sections.tsv")
    if not os.path.isfile(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3 and re.search(r"\bGlossary\b", parts[2], re.I):
                try:
                    return int(parts[1])
                except ValueError:
                    return None
    return None


def undefined_caps(spans_dir, gloss, stop, outdir):
    """Every ALL-CAPS token/phrase used in the body but absent from the glossary."""
    defined = glossary_key(gloss)
    gloss_page = glossary_start_page(spans_dir)
    tok_count, tok_page, tok_sample = Counter(), {}, {}
    phr_count, phr_page = Counter(), {}
    page = 0
    with io.open(os.path.join(spans_dir, "lines.txt"), encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = PAGE_MARK.match(line)
            if m:
                page = int(m.group(1))
                continue
            if gloss_page and page >= gloss_page:
                continue                      # the glossary defines terms; don't mine it
            if not line.strip():
                continue
            for mm in CAPS_PHRASE.finditer(line):
                phrase = mm.group(0).strip()
                words = phrase.split()
                undef = []
                for raw in words:
                    w = base_token(raw)
                    if not w or RULE_ID.match(w) or LOOKS_LIKE_ID.match(w) or PART_NUM.match(w):
                        continue
                    if w in stop or raw.upper() in stop:
                        continue
                    if w in defined:
                        continue
                    undef.append(w)
                    tok_count[w] += 1
                    tok_page.setdefault(w, page)
                    tok_sample.setdefault(w, norm(line)[:160])
                if len(words) > 1 and phrase.upper() not in defined and undef:
                    phr_count[phrase] += 1
                    phr_page.setdefault(phrase, page)
    with io.open(os.path.join(outdir, "UNDEFINED_CAPS.tsv"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write("token\tcount\tfirst_page\tsample\n")
        for t, c in tok_count.most_common():
            fh.write("%s\t%d\t%d\t%s\n" % (t, c, tok_page[t], tok_sample[t]))
    with io.open(os.path.join(outdir, "UNDEFINED_CAPS_PHRASES.tsv"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write("phrase\tcount\tfirst_page\n")
        for p, c in phr_count.most_common():
            fh.write("%s\t%d\t%d\n" % (p, c, phr_page[p]))
    return len(tok_count), len(phr_count)


def main():
    ap = argparse.ArgumentParser(description="diff two frc_spans.py extractions")
    ap.add_argument("--new", required=True, help="frc_spans outdir for the new manual")
    ap.add_argument("--base", required=True, help="frc_spans outdir for the baseline manual")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--stoplist", default=None)
    ap.add_argument("--changed-threshold", type=float, default=0.995)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    new, base = load(a.new), load(a.base)
    nr, br = new["rules"], base["rules"]
    ng, bg = new.get("glossary", {}), base.get("glossary", {})

    def w(name):
        return io.open(os.path.join(a.outdir, name), "w", encoding="utf-8", newline="\n")

    added = sorted(set(nr) - set(br))
    removed = sorted(set(br) - set(nr))
    shared = sorted(set(nr) & set(br))

    with w("rules_ADDED.txt") as fh:
        for rid in added:
            fh.write("%s\t%s\t%s\n" % (rid, nr[rid]["class"], norm(nr[rid]["headline"])))
    with w("rules_REMOVED.txt") as fh:
        for rid in removed:
            fh.write("%s\t%s\t%s\n" % (rid, br[rid]["class"], norm(br[rid]["headline"])))

    changed, unchanged = [], []
    for rid in shared:
        a_txt, b_txt = norm(br[rid]["body"]), norm(nr[rid]["body"])
        ratio = difflib.SequenceMatcher(None, a_txt, b_txt).ratio()
        if ratio >= a.changed_threshold and norm(br[rid]["headline"]) == norm(nr[rid]["headline"]):
            unchanged.append(rid)
        else:
            changed.append((ratio, rid))
    changed.sort()
    with w("rules_CHANGED.tsv") as fh:
        fh.write("id\tsimilarity\tclass\theadline_base\theadline_new\n")
        for ratio, rid in changed:
            fh.write("%s\t%.3f\t%s\t%s\t%s\n" % (rid, ratio, nr[rid]["class"],
                                                 norm(br[rid]["headline"]),
                                                 norm(nr[rid]["headline"])))
    with w("rules_UNCHANGED.txt") as fh:
        for rid in unchanged:
            fh.write(rid + "\n")
    with w("rules_CHANGED_DETAIL.txt") as fh:
        for ratio, rid in changed:
            fh.write("=" * 78 + "\n%s   similarity %.3f   class %s\n" % (rid, ratio, nr[rid]["class"]))
            fh.write("BASE headline: %s\nNEW  headline: %s\n\n" % (norm(br[rid]["headline"]),
                                                                   norm(nr[rid]["headline"])))
            d = difflib.unified_diff(norm(br[rid]["body"]).split(". "),
                                     norm(nr[rid]["body"]).split(". "),
                                     "BASE/" + rid, "NEW/" + rid, lineterm="", n=1)
            fh.write("\n".join(d) + "\n\n")

    with w("rules_GAMESPECIFIC.tsv") as fh:
        fh.write("id\tpage\tclass\theadline\n")
        for rid in new["order"]:
            r = nr[rid]
            if r["class"] != "EVERGREEN":
                fh.write("%s\t%d\t%s\t%s\n" % (rid, r["page"], r["class"], norm(r["headline"])))
    with w("rules_EVERGREEN.tsv") as fh:
        fh.write("id\tpage\theadline\n")
        for rid in new["order"]:
            r = nr[rid]
            if r["class"] == "EVERGREEN":
                fh.write("%s\t%d\t%s\n" % (rid, r["page"], norm(r["headline"])))

    g_added = sorted(set(ng) - set(bg))
    g_removed = sorted(set(bg) - set(ng))
    with w("glossary_ADDED.txt") as fh:
        for t in g_added:
            fh.write("%s\t%s\n" % (t, norm(ng[t])))
    with w("glossary_REMOVED.txt") as fh:
        for t in g_removed:
            fh.write("%s\t%s\n" % (t, norm(bg[t])))
    g_changed = []
    for t in sorted(set(ng) & set(bg)):
        ratio = difflib.SequenceMatcher(None, norm(bg[t]), norm(ng[t])).ratio()
        if ratio < 0.995:
            g_changed.append((ratio, t))
    g_changed.sort()
    with w("glossary_CHANGED.tsv") as fh:
        fh.write("term\tsimilarity\tbase_definition\tnew_definition\n")
        for ratio, t in g_changed:
            fh.write("%s\t%.3f\t%s\t%s\n" % (t, ratio, norm(bg[t]), norm(ng[t])))

    ntok, nphr = undefined_caps(a.new, ng, read_stoplist(a.stoplist), a.outdir)

    print("   rules: new=%d base=%d  ADDED=%d  REMOVED=%d  CHANGED=%d  identical=%d"
          % (len(nr), len(br), len(added), len(removed), len(changed), len(unchanged)))
    print("   class: gamespec=%d  evergreen=%d"
          % (sum(1 for r in nr.values() if r["class"] != "EVERGREEN"),
             sum(1 for r in nr.values() if r["class"] == "EVERGREEN")))
    print("   glossary: new=%d base=%d  ADDED=%d  REMOVED=%d  CHANGED=%d"
          % (len(ng), len(bg), len(g_added), len(g_removed), len(g_changed)))
    print("   undefined ALL-CAPS: %d distinct tokens, %d distinct phrases" % (ntok, nphr))


if __name__ == "__main__":
    main()
