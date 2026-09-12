#!/usr/bin/env python3
"""Award AVAILABILITY, recomputed directly from TBA 2026 award rows.

AVAILABILITY DEFINITION (the whole point of this script):
    availability(A) = number of DISTINCT events at which an award row whose
                      award name is EXACTLY A appears.

Never sum an award with its "... Finalist" or "... Semi-Finalist" variants, and
never sum Regional/District/District Championship tiers into one line. Those are
separate awards with separate ballots. Summing them produced the retracted
"FIRST Leadership Award: 192 events @ 2.08/event" figure (10 + 172 + 218 = 400
rows / 192 events), a 19x overstatement of a 10-event award.

Usage:
  python tools/award_availability.py                       # full table
  python tools/award_availability.py --min-events 5        # drop offseason noise
  python tools/award_availability.py --check FILE.md       # assert no figure in
        FILE exceeds the distinct-event count for that exact award name
"""
import argparse, csv, io, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "research", "awards_tba", "tba_awards_2026.csv")


def load(path=CSV):
    """-> {exact award name: {"events": set, "rows": int}}"""
    agg = defaultdict(lambda: {"events": set(), "rows": 0})
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            name = (r.get("award") or "").strip()
            if not name:
                continue
            agg[name]["events"].add((r.get("year", "").strip(), (r.get("event") or "").strip()))
            agg[name]["rows"] += 1
    return agg


def table(agg, min_events=1):
    rows = []
    for name, d in agg.items():
        ev = len(d["events"])
        if ev < min_events:
            continue
        rows.append((name, ev, d["rows"], d["rows"] / ev))
    rows.sort(key=lambda t: (-t[1], t[0]))
    return rows


# families that MUST stay disaggregated -- summing these is the known defect
FAMILIES = {
    "FIRST Leadership Award": ["FIRST Leadership Award", "FIRST Leadership Award Finalist",
                               "District Championship FIRST Leadership Award Semi-Finalist"],
    "FIRST Impact Award": ["Regional FIRST Impact Award", "District FIRST Impact Award",
                           "District Championship FIRST Impact Award"],
    "Engineering Inspiration Award sponsored by SpaceX": [
        "Regional Engineering Inspiration Award sponsored by SpaceX",
        "District Engineering Inspiration Award sponsored by SpaceX",
        "District Championship Engineering Inspiration Award sponsored by SpaceX"],
    "Woodie Flowers": ["Woodie Flowers Finalist Award", "Woodie Flowers Award"],
}


EVENT_COL = re.compile(r"event|offered", re.I)
BACKTICK = re.compile(r"`[^`]*`")
INT = re.compile(r"(?<![\d.])(\d{1,4})(?![\d.])")


def _cells(line):
    line = line.lstrip("> ").strip()
    if not line.startswith("|"):
        return None
    return [c.strip() for c in line.strip("|").split("|")]


def _fam_ceiling(agg):
    """exact-or-family display name -> max distinct events across the family.

    A figure attached to a family name may legitimately be any single tier's
    event count, but never more than the largest tier. It may NEVER be the sum.
    """
    ceil = {n: len(d["events"]) for n, d in agg.items()}
    for fam, members in FAMILIES.items():
        present = [m for m in members if m in agg]
        if present:
            ceil[fam] = max(len(agg[m]["events"]) for m in present)
    for fam, members in (("Winner", ["Regional Winners", "District Event Winner",
                                     "District Championship Winner", "Championship Division Winner"]),
                         ("Finalist", ["Regional Finalists", "District Event Finalist",
                                       "District Championship Finalist",
                                       "Championship Division Finalist"])):
        present = [m for m in members if m in agg]
        if present:
            ceil[fam] = max(ceil.get(fam, 0), max(len(agg[m]["events"]) for m in present))
    return ceil


def check(agg, path):
    """Two assertions over a markdown file.

    A. EQUALITY -- any table row shaped `| `Exact Award Name` | int | int | float |`
       must reproduce the CSV's distinct-event count and row count exactly.
    B. CEILING  -- in any table column whose HEADER mentions "event"/"offered",
       no integer may exceed the distinct-event count of the longest exact award
       name (or DO-NOT-SUM family) named on that row. This is what catches a
       summed figure: 192 > 120, the biggest FIRST Leadership tier.

    Column-header awareness is the point. Without it the check fires on row
    numbers, row counts and percentages and is useless.
    """
    exact = {n: (len(d["events"]), d["rows"]) for n, d in agg.items()}
    ceil = _fam_ceiling(agg)
    names_by_len = sorted(ceil, key=len, reverse=True)
    bad, hdr = [], []
    lines = io.open(path, encoding="utf-8").read().splitlines()
    for i, line in enumerate(lines, 1):
        cells = _cells(line)
        if cells is None:
            hdr = []
            continue
        if set("".join(cells)) <= set("-: "):        # separator -> previous row was the header
            prev = _cells(lines[i - 2]) or []
            hdr = prev
            continue
        # --- A. equality on the canonical availability row shape
        c0 = cells[0].strip("*")
        if len(cells) >= 3 and c0.startswith("`") and c0.endswith("`"):
            name = c0.strip("`")
            if name in exact and re.fullmatch(r"\*{0,2}\d+\*{0,2}", cells[1])                              and re.fullmatch(r"\*{0,2}\d+\*{0,2}", cells[2]):
                ev, rows = exact[name]
                got_ev, got_rows = int(cells[1].strip("*")), int(cells[2].strip("*"))
                if (got_ev, got_rows) != (ev, rows):
                    bad.append((i, name, f"row states {got_ev} events / {got_rows} rows; "
                                         f"CSV says {ev} events / {rows} rows", line.strip()[:100]))
                continue
        # --- B. ceiling in event-labelled columns
        row_name = next((n for n in names_by_len if n and n in line), None)
        if not row_name:
            continue
        limit = ceil[row_name]
        for j, cell in enumerate(cells):
            if j >= len(hdr) or not EVENT_COL.search(hdr[j]):
                continue
            for m in INT.finditer(BACKTICK.sub(" ", cell)):
                v = int(m.group(1))
                if v > limit:
                    bad.append((i, row_name,
                                f"column '{hdr[j].strip()}' claims {v} events, but no exact award "
                                f"name in that family exceeds {limit} distinct events "
                                f"(summed availability?)", line.strip()[:100]))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-events", type=int, default=1)
    ap.add_argument("--check", metavar="FILE")
    ap.add_argument("--csv", default=CSV)
    a = ap.parse_args()
    agg = load(a.csv)

    if a.check:
        bad = check(agg, a.check)
        for ln, name, why, txt in bad:
            print(f"FAIL {a.check}:{ln}  [{name}] {why}")
            print(f"     {txt}")
        print(f"{'FAIL' if bad else 'PASS'}: {len(bad)} availability overstatement(s) in {a.check}")
        return 1 if bad else 0

    allev = set()
    for d in agg.values():
        allev |= d["events"]
    print(f"# Award availability, 2026 -- distinct events per EXACT award name")
    print(f"# source: {os.path.relpath(a.csv, ROOT)}   distinct events in file: {len(allev)}   "
          f"distinct award names: {len(agg)}")
    print(f"{'events':>6} {'rows':>6} {'per_ev':>7}  award (exact name)")
    print("-" * 96)
    for name, ev, rows, per in table(agg, a.min_events):
        print(f"{ev:>6} {rows:>6} {per:>7.2f}  {name}")

    print("\n# DO-NOT-SUM families (each line is a separate award with its own ballot)")
    for fam, members in FAMILIES.items():
        print(f"\n  {fam}:")
        for m in members:
            d = agg.get(m)
            if d:
                print(f"    {len(d['events']):>4} events  {d['rows']:>4} rows   {m}")
            else:
                print(f"    {'--':>4}           (absent)   {m}")
        tot_rows = sum(agg[m]["rows"] for m in members if m in agg)
        tot_ev = len(set().union(*[agg[m]["events"] for m in members if m in agg]) or set())
        print(f"    [the WRONG rollup would print: {tot_ev} events @ "
              f"{tot_rows/tot_ev:.2f}/event -- do not publish this]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
