#!/usr/bin/env python3
"""
teamupdate-diff.py -- what did FIRST change AFTER the manual shipped?

WHY THIS EXISTS
---------------
The Game Manual is not the rules. The rules are (manual + every Team Update + every Q&A answer).
FIRST published 23 Team Updates in 2026. Each one can silently redefine a rule you already
designed around. `ingest-manual.sh` diffs manual-vs-manual; this covers the other half.

TWO MODES
---------
  season   For one season: every rule id and manual section each Team Update touched, in
           date order, plus a churn ranking (a rule amended 3 times was contentious, and
           contentious rules are where strategy leverage and referee variance live).

  slots    Across ALL seasons on disk: which rule-number slots get amended most often.
           This is predictive -- it says where BIOCORE's amendments will probably land.

USAGE
  python tools/teamupdate-diff.py season 2026
  python tools/teamupdate-diff.py season 2026 --since 03      # only TU03 onward
  python tools/teamupdate-diff.py slots
  python tools/teamupdate-diff.py season 2027 --watch         # print only NEW since last run

OUTPUT
  research/teamupdate_analysis/<season>_tu_index.tsv     tu, date, rule_ids, sections
  research/teamupdate_analysis/<season>_tu_churn.tsv     rule_id, n_updates, which TUs
  research/teamupdate_analysis/slot_churn_allseasons.tsv rule_id, seasons_touched, total
  .watch_state.json                                      for --watch

Requires: pymupdf.
"""
import sys, os, re, json, glob, argparse, collections, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUP = os.path.join(ROOT, "manuals", "archive", "supplemental")
OUTDIR = os.path.join(ROOT, "research", "teamupdate_analysis")

# FRC rule ids. Post-2024 are 3-digit (G416, R402, E101); pre-2024 were 1-2 digit (G17, R54).
RULE_RE = re.compile(r"\b([GRITHSECQ])(\d{1,3})\b")
# Manual section headings cited by Team Updates, e.g. "6.5.2", "5.12", "9.4"
SECT_RE = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){1,3})\s+(\S.*)$", re.M)
DATE_RE = re.compile(
    r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2},\s+\d{4})\b")

# Tokens that look like rule ids but aren't, in Team Update prose.
FALSE_POSITIVE = {"Q1", "Q2", "Q3", "Q4", "S1", "S2", "S3", "T1", "T2", "R1", "R2", "C1", "C2",
                  "E1", "E2", "G1", "H1", "I1", "I2"}


def pdf_text(path):
    import pymupdf
    try:
        d = pymupdf.open(path)
    except Exception as e:
        return ""
    try:
        return "\n".join(p.get_text() for p in d)
    finally:
        d.close()


def tu_number(path):
    m = re.search(r"TeamUpdate[-_ ]?(\d{1,2})", os.path.basename(path), re.I)
    return int(m.group(1)) if m else None


def season_files(year):
    d = os.path.join(SUP, f"{year}_TeamUpdates")
    if not os.path.isdir(d):
        return []
    out = []
    for f in glob.glob(os.path.join(d, "*.pdf")):
        if "combined" in os.path.basename(f).lower() or "_ALL" in os.path.basename(f):
            continue          # the combined file would double-count every update
        n = tu_number(f)
        if n is not None:
            out.append((n, f))
    return sorted(out)


def analyse_tu(path):
    txt = pdf_text(path)
    if not txt:
        return None
    rules = collections.Counter()
    for pre, num in RULE_RE.findall(txt):
        rid = f"{pre}{num}"
        if rid in FALSE_POSITIVE:
            continue
        # a 1-digit id in a 3-digit era is almost always a list marker, not a rule
        if len(num) == 1:
            continue
        rules[rid] += 1
    sects = []
    for sec, title in SECT_RE.findall(txt):
        title = title.strip()[:60]
        if len(sec.split(".")) >= 2 and title and not title[0].isdigit():
            sects.append((sec, title))
    dm = DATE_RE.search(txt)
    return {"date": dm.group(1) if dm else "", "rules": rules,
            "sections": sorted(set(sects))[:12], "chars": len(txt)}


def cmd_season(year, since=None, watch=False):
    files = season_files(year)
    if not files:
        print(f"No Team Updates on disk for {year}.")
        print(f"  expected: manuals/archive/supplemental/{year}_TeamUpdates/TeamUpdateNN.pdf")
        print(f"  fetch with: bash tools/rebuild-corpus.sh --fetch   (2022-2026)")
        print(f"          or: YEAR={year} bash tools/probe-2027-manual.sh --download   (once the season opens)")
        return 1
    os.makedirs(OUTDIR, exist_ok=True)

    state_path = os.path.join(OUTDIR, ".watch_state.json")
    state = {}
    if os.path.exists(state_path):
        state = json.load(io.open(state_path, encoding="utf-8"))
    seen = set(state.get(str(year), []))

    rows, churn = [], collections.defaultdict(list)
    new_only = []
    for n, f in files:
        if since is not None and n < since:
            continue
        a = analyse_tu(f)
        if not a:
            continue
        tag = f"TU{n:02d}"
        if tag not in seen:
            new_only.append(tag)
        rows.append((n, tag, a))
        for rid in a["rules"]:
            churn[rid].append(tag)

    if watch:
        if not new_only:
            print(f"{year}: no new Team Updates since last run.")
            return 0
        print(f"{year}: NEW since last run -> {', '.join(new_only)}")
        rows = [r for r in rows if r[1] in new_only]

    print(f"\n=== {year} Team Updates: {len(rows)} analysed ===\n")
    print(f"{'TU':<6}{'date':<20}{'rules touched':<46}sections")
    print("-" * 118)
    for n, tag, a in rows:
        rl = " ".join(sorted(a["rules"], key=lambda r: (r[0], int(r[1:]))))
        sc = " ".join(s for s, _ in a["sections"][:6])
        print(f"{tag:<6}{a['date']:<20}{rl[:44]:<46}{sc[:44]}")

    # ---- churn ranking
    ranked = sorted(churn.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    print(f"\n=== Most-amended rules in {year} (churn = contentious) ===\n")
    print(f"{'rule':<8}{'#TUs':>5}  updates")
    print("-" * 70)
    for rid, tus in ranked[:20]:
        if len(tus) < 2:
            continue
        print(f"{rid:<8}{len(tus):>5}  {' '.join(tus)}")
    multi = sum(1 for _, t in ranked if len(t) > 1)
    print(f"\n{len(ranked)} distinct rules amended; {multi} amended more than once.")

    idx = os.path.join(OUTDIR, f"{year}_tu_index.tsv")
    with io.open(idx, "w", encoding="utf-8", newline="") as fh:
        fh.write("tu\tdate\trule_ids\tsections\n")
        for n, tag, a in rows:
            fh.write(f"{tag}\t{a['date']}\t{','.join(sorted(a['rules']))}\t"
                     f"{','.join(s for s, _ in a['sections'])}\n")
    ch = os.path.join(OUTDIR, f"{year}_tu_churn.tsv")
    with io.open(ch, "w", encoding="utf-8", newline="") as fh:
        fh.write("rule_id\tn_updates\ttus\n")
        for rid, tus in ranked:
            fh.write(f"{rid}\t{len(tus)}\t{','.join(tus)}\n")
    print(f"\nwrote {idx}\nwrote {ch}")

    state.setdefault(str(year), [])
    state[str(year)] = sorted({r[1] for r in rows} | seen)
    json.dump(state, io.open(state_path, "w", encoding="utf-8"), indent=1)
    return 0


def cmd_slots():
    years = []
    for d in glob.glob(os.path.join(SUP, "*_TeamUpdates")):
        m = re.match(r"(\d{4})_TeamUpdates", os.path.basename(d))
        if m:
            years.append(int(m.group(1)))
    years.sort()
    if not years:
        print("No Team Update directories found under manuals/archive/supplemental/.")
        print("  fetch with: bash tools/rebuild-corpus.sh --fetch")
        return 1
    os.makedirs(OUTDIR, exist_ok=True)

    per_year, totals = {}, collections.Counter()
    for y in years:
        c = collections.Counter()
        for n, f in season_files(y):
            a = analyse_tu(f)
            if a:
                for rid in a["rules"]:
                    c[rid] += 1
        per_year[y] = c
        for rid, k in c.items():
            totals[rid] += k
        print(f"  {y}: {len(season_files(y)):>2} updates, {len(c):>3} distinct rules amended")

    # Only the 2024+ era is ID-comparable to BIOCORE (FRC renumbered every rule in 2024).
    modern = [y for y in years if y >= 2024]
    mod = collections.Counter()
    seasons_hit = collections.Counter()
    for y in modern:
        for rid, k in per_year[y].items():
            mod[rid] += k
            seasons_hit[rid] += 1

    print(f"\n=== Rule slots most amended in the 2024+ numbering era ({', '.join(map(str, modern))}) ===")
    print("    (BIOCORE uses this numbering, so these slots are the forward-looking prediction)\n")
    print(f"{'rule':<8}{'seasons':>8}{'total':>7}  {'  '.join(str(y) for y in modern)}")
    print("-" * 60)
    for rid, tot in sorted(mod.items(), key=lambda kv: (-seasons_hit[kv[0]], -kv[1]))[:25]:
        per = "  ".join(f"{per_year[y].get(rid, 0):>4}" for y in modern)
        print(f"{rid:<8}{seasons_hit[rid]:>8}{tot:>7}  {per}")

    out = os.path.join(OUTDIR, "slot_churn_allseasons.tsv")
    with io.open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write("rule_id\tseasons_touched_2024plus\ttotal_mentions_2024plus\t" +
                 "\t".join(str(y) for y in years) + "\n")
        for rid, tot in sorted(mod.items(), key=lambda kv: (-seasons_hit[kv[0]], -kv[1])):
            fh.write(f"{rid}\t{seasons_hit[rid]}\t{tot}\t" +
                     "\t".join(str(per_year[y].get(rid, 0)) for y in years) + "\n")
    print(f"\nwrote {out}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("season"); s.add_argument("year", type=int)
    s.add_argument("--since", type=int, default=None)
    s.add_argument("--watch", action="store_true")
    sub.add_parser("slots")
    a = ap.parse_args()
    if a.cmd == "season":
        return cmd_season(a.year, a.since, a.watch)
    return cmd_slots()


if __name__ == "__main__":
    sys.exit(main())
