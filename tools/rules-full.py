#!/usr/bin/env python3
"""
rules-full.py -- write research/rule_inventories/<year>_rules_full.txt, the flat per-rule
text that tools/rule-show.py, tools/cite-check.py and tools/rule-taxonomy-analyze.py read.

WHY THIS EXISTS
  KICKOFF_PLAYBOOK.md section 0.2C built this file inline from <year>.json, and no tool in
  the repository writes <year>.json. This script reads <year>_bodies_v2.jsonl instead,
  which tools/rule-inventory.py writes from the game manual PDF. The script that wrote the
  2016-2026 files was never saved, so a file rebuilt here matches the original format but
  not its bytes: the v2 extractor finds a slightly different rule set (2026: 224 rules
  against 225), and blue-box notes stay inside the statement or violation text instead of
  a separate BLUEBOX/NOTES field.

INPUT   research/rule_inventories/<year>_bodies_v2.jsonl   (--from-json: <year>.json)
OUTPUT  research/rule_inventories/<year>_rules_full.txt
        --tsv         also <year>_rules.tsv        (the section 0.2C index; it replaces a
                                                    published file for 2016-2026)
        --violations  also <year>_violations.tsv   (the section 0.2G violation ladder)

None of these files is in the public repository, because each one carries the manual's
rule text. bash tools/rebuild-corpus.sh runs this script for every season it can.

FORMAT (one block per rule, same as section 0.2C)
    ==============================================================================
    ### G101  (p.55, 2026)
    ==============================================================================
    STATEMENT: <rule text before the first "Violation:">

    VIOLATION: Violation: <the rest of the rule text>

USAGE
  python tools/rules-full.py 2027
  python tools/rules-full.py 2016-2026
  python tools/rules-full.py 2027 --tsv --violations
"""
import argparse
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "research", "rule_inventories")
BAR = "=" * 78


def rel(path):
    try:
        r = os.path.relpath(path, ROOT)
    except ValueError:
        return path
    return path if r.startswith("..") else r.replace(os.sep, "/")


def parse_years(specs):
    years = []
    for spec in specs:
        m = re.fullmatch(r"(\d{4})(?:-(\d{4}))?", spec)
        if not m:
            sys.exit("not a year or year range: %s" % spec)
        lo = int(m.group(1))
        hi = int(m.group(2) or lo)
        years.extend(range(lo, hi + 1))
    return sorted(set(years))


def load_v2(year, d):
    """-> (source label, [(id, prefix, num, page, headline, text)])"""
    path = os.path.join(d, "%d_bodies_v2.jsonl" % year)
    rules = []
    with io.open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                rules.append((r["id"], r["prefix"], r["num"], r["page"],
                              r["headline"], r["text"]))
    pdfs = [p for p in glob.glob(os.path.join(ROOT, "manuals", "archive", "frc",
                                              "%d_*GameManual*.pdf" % year))
            if "Section" not in os.path.basename(p)]
    label = os.path.basename(path)
    if pdfs:
        label = "%s via %s" % (os.path.basename(sorted(pdfs)[-1]), label)
    return label, rules


def load_json(year, d):
    """The older <year>.json schema: rules[] of {id, prefix, num, page, title, body}."""
    path = os.path.join(d, "%d.json" % year)
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    rules = [(r["id"], r["prefix"], r["num"], r["page"], r["title"], r["body"])
             for r in data["rules"]]
    return data.get("source", os.path.basename(path)), rules


def split(body):
    m = re.search(r"Violation:", body)
    if not m:
        return body.strip(), ""
    return body[:m.start()].strip(), body[m.start():].strip()


def write_full(year, d, source, rules, tsv):
    full_path = os.path.join(d, "%d_rules_full.txt" % year)
    with io.open(full_path, "w", encoding="utf-8", newline="\n") as full:
        full.write("# FRC %d game manual -- reconstructed rule text\n" % year)
        full.write("# source: %s   rules: %d\n" % (source, len(rules)))
        index = []
        for rid, prefix, num, page, headline, body in rules:
            stmt, viol = split(body)
            full.write("\n%s\n### %s  (p.%s, %d)\n%s\n" % (BAR, rid, page, year, BAR))
            full.write("STATEMENT: %s\n" % stmt)
            if viol:
                full.write("\nVIOLATION: %s\n" % viol)
            index.append("%s\t%s\t%s\t%s\t%d\t%d\t%s\n"
                         % (rid, prefix, num, page, len(stmt), len(viol), headline))
    print("wrote %s  (%d rules)" % (rel(full_path), len(rules)))
    if tsv:
        tsv_path = os.path.join(d, "%d_rules.tsv" % year)
        with io.open(tsv_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("rule_id\tprefix\tnum\tpage\tstmt_chars\tviol_chars\theadline\n")
            fh.writelines(index)
        print("wrote %s" % rel(tsv_path))
    return full_path


def write_violations(year, d, full_path):
    """Section 0.2G: one row per rule that has a Violation clause, with penalty flags."""
    text = io.open(full_path, encoding="utf-8").read()
    out_path = os.path.join(d, "%d_violations.tsv" % year)
    n = 0
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("rule\tpage\tminor\tmajor\tyellow\tred\tdq\tverbal\tescalating\tviolation_text\n")
        pat = r"### ([GRITHSECA]\d{1,3})\s+\(p\.(\d+), %d\)\n=+\n(.*?)(?=\n=+\n### |\Z)" % year
        for m in re.finditer(pat, text, re.S):
            rid, page, body = m.group(1), m.group(2), m.group(3)
            v = re.search(r"VIOLATION:(.*?)(?=\n\n|\Z)", body, re.S)
            if not v:
                continue
            s = " ".join(v.group(1).split())

            def flag(p):
                return "1" if re.search(p, s, re.I) else ""
            fh.write("\t".join([rid, page, flag(r"MINOR FOUL|\bFOUL\b(?! )"),
                                flag(r"MAJOR FOUL|TECH(NICAL)? FOUL"), flag(r"YELLOW CARD"),
                                flag(r"RED CARD"), flag(r"DISQUALIF"), flag(r"VERBAL WARNING"),
                                flag(r"subsequent|each additional|per .*occurrence|repeated"),
                                s[:400]]) + "\n")
            n += 1
    print("wrote %s  (%d rules with a Violation clause)" % (rel(out_path), n))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("years", nargs="+", help="a year (2027) or a range (2016-2026)")
    ap.add_argument("--tsv", action="store_true", help="also write <year>_rules.tsv")
    ap.add_argument("--violations", action="store_true",
                    help="also write <year>_violations.tsv")
    ap.add_argument("--violations-only", action="store_true",
                    help="write <year>_violations.tsv from the existing <year>_rules_full.txt")
    ap.add_argument("--from-json", action="store_true",
                    help="read <year>.json (the older schema) instead of <year>_bodies_v2.jsonl")
    ap.add_argument("--dir", default=INV,
                    help="input and output directory (default research/rule_inventories)")
    a = ap.parse_args()

    missing = 0
    for year in parse_years(a.years):
        if a.violations_only:
            full_path = os.path.join(a.dir, "%d_rules_full.txt" % year)
            if not os.path.isfile(full_path):
                print("MISSING: %s (not in the public repository; rebuild it with: "
                      "bash tools/rebuild-corpus.sh)" % rel(full_path), file=sys.stderr)
                missing += 1
            else:
                write_violations(year, a.dir, full_path)
            continue
        name = ("%d.json" if a.from_json else "%d_bodies_v2.jsonl") % year
        src = os.path.join(a.dir, name)
        if not os.path.isfile(src):
            print("MISSING: %s (not in the public repository; rebuild it with: "
                  "bash tools/rebuild-corpus.sh)" % rel(src), file=sys.stderr)
            missing += 1
            continue
        source, rules = (load_json if a.from_json else load_v2)(year, a.dir)
        full_path = write_full(year, a.dir, source, rules, a.tsv)
        if a.violations:
            write_violations(year, a.dir, full_path)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
