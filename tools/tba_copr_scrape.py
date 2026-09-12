#!/usr/bin/env python3
"""
tba_copr_scrape.py -- pull COMPONENT OPR and per-MATCH alliance scores from The Blue
Alliance's PUBLIC, UNAUTHENTICATED event pages.

WHY THIS EXISTS
---------------
04_PREDICTIVE_FACTORS.md pass 5 carried two large evidence gaps:
  (a) vision / auto component contribution was [S] because Statbotics (the usual source
      of component EPA) has returned HTTP 500 on every data endpoint since 2026-08-21;
  (b) reliability was measured only through DQ, a *rules* event, so mechanical failure
      -- the thing the factor is actually about -- was invisible.

Both are recoverable from the public event page without an API key. Every TBA event page
embeds, inline:
    const coprs = JSON.parse('{"OPR": [[team, value], ...], "autoPoints": [...], ...}')
        -> per-team Component Offensive Power Rating for every column of the season's
           score breakdown (autoPoints, teleopPoints, endgame*, foulPoints, rp, ...)
    <table id="qual-match-table"> ... </table>
        -> every qualification MATCH: the 3 red teams, the 3 blue teams, both scores

(a) comes straight off the coprs blob. (b) is reconstructed: for each match, the residual
    actual_alliance_score - sum(OPR of its 3 members)
is the part of the score the linear OPR model did not predict. A robot that died in one
match shows up as a large negative residual in that match. Per team we keep the mean,
the standard deviation and the minimum of its residuals.

Endpoints used (all GET, unauthenticated HTML):
    https://www.thebluealliance.com/event/<KEY>

Outputs into --out:
    tba_copr_<YEAR>.csv     year,event,week,team,opr,auto,teleop,endgame,foul,rp,total
    tba_resid_<YEAR>.csv    year,event,week,team,n_matches,resid_mean,resid_sd,resid_min
    tba_matches_<YEAR>.csv  year,event,week,match,red1,red2,red3,blue1,blue2,blue3,red_score,blue_score

Usage:
    python tools/tba_copr_scrape.py 2023 2024 2025 2026 --out research/predictive_tba/
"""
import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
BASE = "https://www.thebluealliance.com/event/"

# Component keys differ by season. These are the season-independent buckets we want,
# matched against the coprs keys in priority order (first hit wins).
BUCKETS = {
    "auto": ["autoPoints"],
    "teleop": ["teleopPoints"],
    "endgame": ["endGameBargePoints", "endGamePoints", "endgamePoints",
                "endGameTotalStagePoints", "endGameChargeStationPoints"],
    "foul": ["foulPoints"],
    "rp": ["rp", "RP"],
    "total": ["totalPoints"],
}

COPR_RE = re.compile(r"const coprs = JSON\.parse\('(.*?)'\)", re.S)
# TBA renders qual match rows as a <tr> whose team cells carry frc#### links and whose
# score cells are the last two numeric <td>s.
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TEAM_RE = re.compile(r"/team/(\d+)")
NUM_RE = re.compile(r">\s*(\d+)\s*<")


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                return None
            time.sleep(1.5 * (i + 1))
    return None


def parse_coprs(html):
    m = COPR_RE.search(html)
    if not m:
        return None
    try:
        raw = m.group(1).encode().decode("unicode_escape")
        return json.loads(raw)
    except Exception:
        return None


def parse_qual_matches(html):
    """Return [(match_label, [red1,red2,red3], [blue1,blue2,blue3], red_score, blue_score)]."""
    i = html.find('id="qual-match-table"')
    if i < 0:
        return []
    j = html.find("</table>", i)
    block = html[i:j if j > 0 else len(html)]
    out = []
    for rm in ROW_RE.finditer(block):
        row = rm.group(1)
        teams = TEAM_RE.findall(row)
        if len(teams) < 6:
            continue
        # the two alliance scores are the last two standalone integers in the row
        nums = NUM_RE.findall(row)
        if len(nums) < 2:
            continue
        red, blue = teams[:3], teams[3:6]
        try:
            rs, bs = int(nums[-2]), int(nums[-1])
        except ValueError:
            continue
        out.append((red, blue, rs, bs))
    return out


def residuals(matches, opr):
    """team -> list of per-match residuals (actual alliance score - sum of member OPRs)."""
    acc = {}
    for red, blue, rs, bs in matches:
        for side, score in ((red, rs), (blue, bs)):
            if not all(t in opr for t in side):
                continue
            pred = sum(opr[t] for t in side)
            r = score - pred
            for t in side:
                acc.setdefault(t, []).append(r)
    return acc


def do_event(args):
    year, key, week = args
    html = fetch(BASE + key)
    if not html:
        return key, None, None, None
    coprs = parse_coprs(html)
    matches = parse_qual_matches(html)

    copr_rows, resid_rows, match_rows = [], [], []

    opr = {}
    if coprs and "OPR" in coprs:
        opr = {str(t): float(v) for t, v in coprs["OPR"]}
        picked = {}
        for bucket, cands in BUCKETS.items():
            for c in cands:
                if c in coprs:
                    picked[bucket] = {str(t): float(v) for t, v in coprs[c]}
                    break
        for t, o in opr.items():
            copr_rows.append(dict(
                year=year, event=key, week=week, team=t, opr=round(o, 3),
                **{b: (round(picked[b][t], 3) if b in picked and t in picked[b] else "")
                   for b in BUCKETS},
            ))

    for red, blue, rs, bs in matches:
        match_rows.append(dict(year=year, event=key, week=week,
                               red1=red[0], red2=red[1], red3=red[2],
                               blue1=blue[0], blue2=blue[1], blue3=blue[2],
                               red_score=rs, blue_score=bs))

    if opr and matches:
        for t, rl in residuals(matches, opr).items():
            if len(rl) < 4:
                continue
            resid_rows.append(dict(
                year=year, event=key, week=week, team=t, n_matches=len(rl),
                resid_mean=round(statistics.fmean(rl), 3),
                resid_sd=round(statistics.pstdev(rl), 3),
                resid_min=round(min(rl), 3),
            ))
    return key, copr_rows, resid_rows, match_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("years", nargs="+", type=int)
    tba = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "research", "predictive_tba")
    ap.add_argument("--out", default=tba)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--events-csv", default=os.path.join(tba, "tba_events_{y}.csv"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for year in a.years:
        src = a.events_csv.replace("{y}", str(year))
        if not os.path.exists(src):
            print(f"[{year}] no {src}; skipping", file=sys.stderr)
            continue
        with open(src, newline="", encoding="utf-8") as f:
            evs = [(year, r["event"], r["week"]) for r in csv.DictReader(f)]
        print(f"[{year}] {len(evs)} events", file=sys.stderr)

        C, R, M = [], [], []
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            for n, (key, c, r, m) in enumerate(ex.map(do_event, evs), 1):
                if c is None:
                    print(f"  ! {key} failed", file=sys.stderr)
                    continue
                C += c; R += r; M += m
                if n % 25 == 0:
                    print(f"  {n}/{len(evs)}  {time.time()-t0:.0f}s  "
                          f"copr={len(C)} resid={len(R)}", file=sys.stderr)

        for name, rows in (("copr", C), ("resid", R), ("matches", M)):
            if not rows:
                continue
            p = os.path.join(a.out, f"tba_{name}_{year}.csv")
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            print(f"[{year}] wrote {p} ({len(rows)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
