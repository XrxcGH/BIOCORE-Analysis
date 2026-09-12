#!/usr/bin/env python3
"""
tba_award_scrape.py -- pull FRC award winners + qualification rank from The Blue Alliance.

WHY NOT THE APIv3: https://www.thebluealliance.com/api/v3 requires an X-TBA-Auth-Key that can
only be minted by creating/logging into a TBA account. This harness has no key, so it reads the
same data off TBA's PUBLIC, UNAUTHENTICATED event pages, which embed the awards table, the
qualification rankings table and the playoff alliances in one document.

Endpoints used (all unauthenticated HTML, all GET):
    https://www.thebluealliance.com/events/<YEAR>      -> list of event keys for that season
    https://www.thebluealliance.com/event/<EVENTKEY>   -> awards + rankings + alliances

Output: one row per (year, event, award, team) with that team's qualification rank at that event.

Usage:
    python tools/tba_award_scrape.py 2023 2024 2025 2026 --out research/awards_tba/
"""
import argparse
import csv
import gzip
import io
import os
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

BASE = "https://www.thebluealliance.com"
UA = "BIOCORE-Analysis/1.0 (FRC team strategy research; contact via project owner)"

# --- HTML fragments -----------------------------------------------------------------
# Awards live in a <tr><td>AWARD NAME</td><td> <a href="/team/NNNN/YYYY">NNNN</a> ... </td></tr>
ROW_RE = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", re.S)
TEAM_RE = re.compile(r'href="/team/(\d+)')
TAG_RE = re.compile(r"<[^>]+>")


def unesc(s: str) -> str:
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
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            if attempt == tries - 1:
                sys.stderr.write(f"FAIL {url}: {e}\n")
                return ""
            time.sleep(1.5 * (attempt + 1))
    return ""


def event_keys(year: int):
    html = fetch(f"{BASE}/events/{year}")
    return sorted(set(re.findall(r'href="/event/(%d[a-z0-9]+)"' % year, html)))


def slice_tab(html: str, tab_id: str) -> str:
    """Return the chunk of HTML starting at a given bootstrap tab-pane id."""
    i = html.find('id="%s"' % tab_id)
    if i < 0:
        return ""
    j = html.find('<div class="tab-pane"', i + 10)
    return html[i:j if j > 0 else len(html)]


def parse_rankings(html: str):
    """-> {team:int -> rank:int}"""
    chunk = slice_tab(html, "rankings")
    out = {}
    for cells in ROW_RE.finditer(chunk):
        rank_txt = unesc(cells.group(1))
        teams = TEAM_RE.findall(cells.group(2))
        if rank_txt.isdigit() and len(teams) == 1:
            out.setdefault(int(teams[0]), int(rank_txt))
    return out


def parse_awards(html: str):
    """-> list of (award_name, team:int). Non-team awards (people) are skipped."""
    chunk = slice_tab(html, "awards")
    out = []
    for cells in ROW_RE.finditer(chunk):
        name = unesc(cells.group(1))
        if not name or name.lower() in ("rank", "team", "award"):
            continue
        for t in TEAM_RE.findall(cells.group(2)):
            out.append((name, int(t)))
    return out


def scrape_event(key: str):
    html = fetch(f"{BASE}/event/{key}")
    if not html:
        return []
    ranks = parse_rankings(html)
    n = len(ranks)
    rows = []
    for award, team in parse_awards(html):
        r = ranks.get(team)
        rows.append({
            "year": key[:4],
            "event": key,
            "award": award,
            "team": team,
            "qual_rank": r if r else "",
            "n_teams": n if n else "",
            "rank_pct": round(100.0 * r / n, 1) if (r and n) else "",
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("years", nargs="+", type=int)
    ap.add_argument("--out", default=".")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    for year in args.years:
        keys = event_keys(year)
        sys.stderr.write(f"{year}: {len(keys)} events\n")
        rows = []
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for i, res in enumerate(ex.map(scrape_event, keys)):
                rows.extend(res)
                if (i + 1) % 25 == 0:
                    sys.stderr.write(f"  {i+1}/{len(keys)} events, {len(rows)} rows\n")
        path = os.path.join(args.out, f"tba_awards_{year}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[
                "year", "event", "award", "team", "qual_rank", "n_teams", "rank_pct"])
            w.writeheader()
            w.writerows(rows)
        sys.stderr.write(f"{year}: wrote {len(rows)} rows -> {path}\n")


if __name__ == "__main__":
    main()
