#!/usr/bin/env python3
"""Fetch + flatten the FIRST Robotics Competition award webpages that FIRST itself
declares authoritative, and write ASCII text snapshots into reference/awards/_web/.

Usage:  python fetch_award_pages.py [outdir]
        python fetch_award_pages.py --list    # print the file names it writes; no download

No third-party deps beyond the stdlib. Safe to re-run; overwrites snapshots.
Every page below states on its own face that it is "considered the authority"
(machine / team / submitted award pages) or is the season-eligibility source.
"""
import html
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request

PAGES = {
    "frc-awards-main": "https://www.firstinspires.org/robotics/frc/awards",
    "machine-awards": "https://www.firstinspires.org/resources/library/frc/machine-awards",
    "team-awards": "https://www.firstinspires.org/resources/library/frc/team-awards",
    "submitted-awards": "https://www.firstinspires.org/resources/library/frc/submitted-awards",
    "award-tips": "https://www.firstinspires.org/resources/library/frc/award-tips",
    "frc-championship-eligibility": "https://www.firstinspires.org/resources/library/frc/championship-eligibility",
    "safety-animation-award": "https://www.firstinspires.org/resources/library/safety",
    "digital-animation-award": "https://www.firstinspires.org/resources/library/digital-animation-award",
    "first-leadership-award-winners": "https://www.firstinspires.org/resources/library/frc/first-leadership-award-winners",
}

SUBS = {
    "​": "", "®": "(R)", "’": "'", "‘": "'",
    "–": "-", "—": "--", "“": '"', "”": '"',
    "™": "(TM)", " ": " ",
}


def flatten(raw: str) -> str:
    s = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", raw)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</(p|div|li|h[1-6]|tr|td)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    for k, v in SUBS.items():
        s = s.replace(k, v)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s


UA = "Mozilla/5.0"


def get(url: str) -> str:
    """curl first: the FIRST CDN throttles urllib to ~45 s/request from some networks,
    which turns this script from 5 s into 7 min. urllib stays as the fallback."""
    curl = shutil.which("curl")
    if curl:
        p = subprocess.run([curl, "-sSL", "--max-time", "60", "-A", UA, url],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode == 0 and len(p.stdout) > 512:
            return p.stdout.decode("utf-8", "replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120, context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8", "replace")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for name in PAGES:
            print(name + ".txt")
        return 0
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "_web")
    os.makedirs(outdir, exist_ok=True)
    rc = 0
    for name, url in PAGES.items():
        try:
            raw = get(url)
        except Exception as exc:                      # noqa: BLE001
            print(f"FAIL {name}: {exc}")
            rc = 1
            continue
        path = os.path.join(outdir, name + ".txt")
        with open(path, "w", encoding="ascii", errors="replace") as fh:
            fh.write(flatten(raw))
        print(f"ok   {name}  {os.path.getsize(path)} bytes")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
