#!/usr/bin/env python3
"""
defense_rule_trend.py -- quantify how hostile the FRC rulebook has become to a
defense-first strategy, across the 5-season corpus.

Counts, per manual:
  * protected-zone rules      : G-rules whose headline is "<X> protection."
                                (no-contact zones where the DEFENDER is penalised
                                regardless of who initiated contact)
  * pin_seconds               : the PIN allowance in G4xx
  * foul occurrences          : MAJOR/MINOR (2025+) vs TECH/regular FOUL (<=2024)
  * "not a violation" carve-outs for single-robot blocking
  * count of G-rules in the ROBOT-vs-ROBOT block

Usage:
    python tools/defense_rule_trend.py            # table to stdout
    python tools/defense_rule_trend.py --csv out.csv
"""
import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# pdftotext -layout of each game manual. Not in the public repository;
# bash tools/rebuild-corpus.sh regenerates it from the PDFs.
TXT = os.path.join(ROOT, "manuals", "archive", "frc", "_txt")

SEASONS = [
    ("RAPD", "2022", "2022_RAPIDREACT.txt"),
    ("CHRG", "2023", "2023_CHARGEDUP.txt"),
    ("CRES", "2024", "2024_CRESCENDO.txt"),
    ("REEF", "2025", "2025_REEFSCAPE.txt"),
    ("REB",  "2026", "2026_REBUILT.txt"),
]

# Rule numbers frequently land on a different text line than the rule headline
# in the pdftotext flattening, so match the headline anywhere and back-fill the
# nearest preceding G-number.
PROT_RE = re.compile(r"([A-Z][A-Z/ ]{1,24}) protection\.")
GNUM_RE = re.compile(r"\b(G\d{3})\b")
# "for more than 5\n      seconds" occurs in 2022/2023 -- allow the line break.
PIN_RE = re.compile(r"PIN an opponent'?s? ROBOT for more than (\d+)\s+seconds?")
SINGLE_BLOCK_RE = re.compile(
    r"single ROBOT blocking access to a particular area of the FIELD", re.I)
DEFENSE_WORD_RE = re.compile(r"\bdefen[cs]e\b", re.I)
REGARDLESS_RE = re.compile(r"regardless of who initiates contact")


def load(fn):
    with open(os.path.join(TXT, fn), encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    a = ap.parse_args()

    absent = [fn for _, _, fn in SEASONS if not os.path.isfile(os.path.join(TXT, fn))]
    if absent:
        more = " and %d more" % (len(absent) - 1) if len(absent) > 1 else ""
        sys.exit("MISSING: manuals/archive/frc/_txt/%s%s (not in the public repository; "
                 "rebuild with: bash tools/rebuild-corpus.sh)" % (absent[0], more))

    rows = []
    for short, year, fn in SEASONS:
        t = load(fn)
        prot = []
        for m in PROT_RE.finditer(t):
            gs = GNUM_RE.findall(t[: m.start()])
            prot.append((gs[-1] if gs else "G???", m.group(1).strip()))
        pin = PIN_RE.search(t)
        # foul vocabulary changed in 2025: TECH FOUL -> MAJOR FOUL, FOUL -> MINOR FOUL
        major = len(re.findall(r"\bMAJOR FOUL\b", t)) + len(re.findall(r"\bTECH FOUL\b", t))
        minor = len(re.findall(r"\bMINOR FOUL\b", t))
        if not minor:  # pre-2025 wording
            minor = len(re.findall(r"(?<!TECH )\bFOUL\b", t)) - major
        rows.append({
            "season": year,
            "short": short,
            "n_protection_rules": len(prot),
            "protection_rules": "; ".join(f"{g} {n.strip()}" for g, n in prot),
            "pin_seconds": pin.group(1) if pin else "",
            "n_regardless_of_who_initiates": len(REGARDLESS_RE.findall(t)),
            "n_major_or_tech_foul_mentions": major,
            "n_minor_foul_mentions": max(minor, 0),
            "single_robot_block_explicitly_legal": bool(SINGLE_BLOCK_RE.search(t)),
            "n_defense_word": len(DEFENSE_WORD_RE.findall(t)),
        })

    hdr = ["season", "short", "n_protection_rules", "pin_seconds",
           "n_regardless_of_who_initiates", "n_major_or_tech_foul_mentions",
           "n_minor_foul_mentions", "single_robot_block_explicitly_legal",
           "n_defense_word", "protection_rules"]
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=hdr)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {a.csv}")
    for r in rows:
        print(f"{r['short']:5} {r['season']}  prot={r['n_protection_rules']} "
              f"pin={r['pin_seconds']}s  regardless={r['n_regardless_of_who_initiates']}  "
              f"major/tech={r['n_major_or_tech_foul_mentions']:3}  "
              f"minor={r['n_minor_foul_mentions']:3}  "
              f"singleblock_legal={r['single_robot_block_explicitly_legal']}  "
              f"defense_word={r['n_defense_word']}")
        if r["protection_rules"]:
            print(f"        -> {r['protection_rules']}")


if __name__ == "__main__":
    main()
