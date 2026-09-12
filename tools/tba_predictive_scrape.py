#!/usr/bin/env python3
"""
tba_predictive_scrape.py -- pull the evidence base for 04_PREDICTIVE_FACTORS.md
from The Blue Alliance's PUBLIC, UNAUTHENTICATED event pages.

WHY NOT THE APIv3: https://www.thebluealliance.com/api/v3 requires an X-TBA-Auth-Key
that can only be minted from a TBA account. This harness has no key. The public event
page embeds, in one document:
    * the qualification RANKINGS table  (#rankingsTable) -- rank, team, RS, the
      season-specific sort columns (e.g. 2025 "Avg Auto"), record, DQ, played
    * the playoff ALLIANCES table       (#event-alliances) -- captain / pick1 / pick2 / backup
    * the playoff bracket rows          (alliance-name winner spans)

Endpoints used (all GET, all unauthenticated HTML):
    https://www.thebluealliance.com/events/<YEAR>    -> event keys grouped by week
    https://www.thebluealliance.com/event/<KEY>      -> rankings + alliances + bracket

Outputs (one CSV per table) into --out:
    tba_rankings_<YEAR>.csv    year,event,week,rank,team,rs,record_w,record_l,record_t,dq,played,<sortcols...>
    tba_alliances_<YEAR>.csv   year,event,week,alliance,slot,team,qual_rank,n_teams,rank_pct
    tba_events_<YEAR>.csv      year,event,week,n_teams,n_alliances,winning_alliance

Usage:
    python tools/tba_predictive_scrape.py 2024 2025 2026 --out research/predictive_tba/
"""
import argparse
import csv
import gzip
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://www.thebluealliance.com"
UA = "BIOCORE-Analysis/1.0 (FRC team strategy research; contact via project owner)"

TAG_RE = re.compile(r"<[^>]+>")
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TEAM_RE = re.compile(r'href="/team/(\d+)')

# Weeks we care about: official in-season play only.
WEEK_HEAD_RE = re.compile(r"<h[23][^>]*>\s*(Week \d+|FIRST Championship|Preseason|Offseason)", re.S)


def txt(s: str) -> str:
    s = TAG_RE.sub("", s)
    for a, b in (("&#39;", "'"), ("&amp;", "&"), ("&quot;", '"'),
                 ("&nbsp;", " "), ("&#x27;", "'")):
        s = s.replace(a, b)
    return " ".join(s.split())


def fetch(url: str, tries: int = 3) -> str:
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=90) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            if attempt == tries - 1:
                sys.stderr.write(f"FAIL {url}: {e}\n")
                return ""
            time.sleep(2 * (attempt + 1))
    return ""


def event_keys(year: int):
    """Return [(event_key, week_label)] for official in-season events only."""
    h = fetch(f"{BASE}/events/{year}")
    out = []
    # split the document on week headings, then harvest event links inside each block
    parts = WEEK_HEAD_RE.split(h)
    # parts = [pre, label, block, label, block, ...]
    for i in range(1, len(parts) - 1, 2):
        label = parts[i].strip()
        block = parts[i + 1]
        if label in ("Preseason", "Offseason"):
            continue
        for k in re.findall(rf'href="/event/({year}[a-z0-9]+)"', block):
            out.append((k, label))
    # dedupe preserving order
    seen = set()
    ded = []
    for k, w in out:
        if k not in seen:
            seen.add(k)
            ded.append((k, w))
    return ded


def parse_event(year: int, key: str, week: str):
    h = fetch(f"{BASE}/event/{key}")
    if not h:
        return None
    res = {"event": key, "week": week, "rank_cols": [], "rankings": [],
           "alliances": [], "winner": ""}

    # ---- rankings ------------------------------------------------------------
    i = h.find('id="rankingsTable"')
    if i != -1:
        tbl = h[i:h.find("</table>", i)]
        head = re.search(r"<thead>(.*?)</thead>", tbl, re.S)
        cols = [txt(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", head.group(1), re.S)] if head else []
        res["rank_cols"] = cols
        body = re.search(r"<tbody>(.*?)$", tbl, re.S)
        if body:
            for row in ROW_RE.findall(body.group(1)):
                cells = [txt(c) for c in CELL_RE.findall(row)]
                if len(cells) >= 3 and cells[0].isdigit():
                    res["rankings"].append(cells)

    # ---- alliances -----------------------------------------------------------
    i = h.find('id="event-alliances"')
    if i != -1:
        tbl = h[i:h.find("</table>", i)]
        for row in ROW_RE.findall(tbl):
            if "<th" in row:
                continue
            cells = CELL_RE.findall(row)
            if not cells:
                continue
            label = txt(cells[0])
            m = re.match(r"Alliance (\d+)", label)
            if not m:
                continue
            anum = int(m.group(1))
            slot_names = ["captain", "pick1", "pick2", "backup"]
            for j, c in enumerate(cells[1:]):
                t = TEAM_RE.search(c)
                if t:
                    res["alliances"].append(
                        (anum, slot_names[j] if j < len(slot_names) else f"slot{j}", t.group(1)))

    # ---- playoff winner (last "winner" alliance seed listed in the bracket) ---
    seeds = re.findall(r'<td class="winner">\s*(\d+)\s*</td>', h)
    if seeds:
        # the finals winner is the seed that appears most often as a winner
        from collections import Counter
        res["winner"] = Counter(seeds).most_common(1)[0][0]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("years", nargs="+", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="cap events per year (0=all)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for year in a.years:
        keys = event_keys(year)
        if a.limit:
            keys = keys[: a.limit]
        sys.stderr.write(f"{year}: {len(keys)} official events\n")
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            results = list(ex.map(lambda kw: parse_event(year, kw[0], kw[1]), keys))
        results = [r for r in results if r]

        # rankings CSV -- keep a normalized core + the raw season-specific columns
        rp = os.path.join(a.out, f"tba_rankings_{year}.csv")
        with open(rp, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["year", "event", "week", "col_index", "col_name", "rank", "team", "value"])
            for r in results:
                cols = r["rank_cols"]
                for row in r["rankings"]:
                    rank, team = row[0], row[1]
                    for ci, val in enumerate(row):
                        if ci < 2 or ci >= len(cols):
                            continue
                        w.writerow([year, r["event"], r["week"], ci, cols[ci], rank, team, val])

        # alliances CSV
        ap_ = os.path.join(a.out, f"tba_alliances_{year}.csv")
        with open(ap_, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["year", "event", "week", "alliance", "slot", "team",
                        "qual_rank", "n_teams", "rank_pct", "won_event"])
            for r in results:
                rankof = {row[1]: int(row[0]) for row in r["rankings"]}
                n = len(r["rankings"])
                for anum, slot, team in r["alliances"]:
                    qr = rankof.get(team, "")
                    pct = round(100.0 * qr / n, 2) if (qr and n) else ""
                    w.writerow([year, r["event"], r["week"], anum, slot, team,
                                qr, n, pct, int(str(anum) == r["winner"])])

        # events CSV
        ep = os.path.join(a.out, f"tba_events_{year}.csv")
        with open(ep, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["year", "event", "week", "n_teams", "n_alliances",
                        "winning_alliance", "rank_cols"])
            for r in results:
                w.writerow([year, r["event"], r["week"], len(r["rankings"]),
                            len({x[0] for x in r["alliances"]}), r["winner"],
                            "|".join(r["rank_cols"])])
        sys.stderr.write(f"  wrote {rp}, {ap_}, {ep}\n")


if __name__ == "__main__":
    main()
