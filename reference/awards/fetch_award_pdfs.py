#!/usr/bin/env python3
"""Download every award rubric/guide PDF that firstinspires.org currently links for
FIRST Robotics Competition into reference/awards/pdfs/, plus MANIFEST.csv
(file, url, bytes, sha256, fetched).

Usage:  python fetch_award_pdfs.py [outdir]
        python fetch_award_pdfs.py --list     # print the file names it writes; no download

Re-run on 2027-01-09 and after every Team Update that touches an Awards webpage, then
`git diff` / eyeball MANIFEST.csv: a changed sha256 means FIRST silently revised a rubric,
a FAIL means FIRST moved or retired the document. Both are news.

Uses curl (present on Windows 10+ / Git-Bash / macOS / Linux). urllib is used as a
fallback but the FIRST hubfs CDN throttles it to ~45 s per file, so curl is preferred.

URL note: FIRST renamed Dean's List -> FIRST Leadership Award in Feb 2026 but did NOT
rename the judging-guidelines file. dla-judging-guidelines.pdf is still the live link on
the Awards page; fla-judging-guidelines.pdf 404s. Do not "fix" this.
Sibling-team guidance lives under /frc/reg/, not /frc/awards/.
"""
import datetime, hashlib, os, shutil, ssl, subprocess, sys, urllib.request

A = "https://www.firstinspires.org/hubfs/web/program/frc/awards/"
R = "https://www.firstinspires.org/hubfs/web/program/frc/reg/"
PDFS = {
    "judge-manual.pdf":                              A + "judge-manual.pdf",
    "award-workbook.pdf":                            A + "award-workbook.pdf",
    "best-practices-for-teams.pdf":                  A + "best-practices-for-teams.pdf",
    "inside-look-at-judging-process.pdf":            A + "inside-look-at-judging-process.pdf",
    "technical-judging-tips.pdf":                    A + "technical-judging-tips.pdf",
    "fia-judging-guidelines.pdf":                    A + "fia-judging-guidelines.pdf",
    "fia-definitions.pdf":                           A + "fia-definitions.pdf",
    "fia-documentation-form.pdf":                    A + "fia-documentation-form.pdf",
    "fia-video-consent.pdf":                         A + "fia-video-consent.pdf",
    "first-leadership-award-guide.pdf":              A + "fla-guide.pdf",
    "first-leadership-award-judging-guidelines.pdf": A + "dla-judging-guidelines.pdf",
    "sibling-teams-guidelines.pdf":                  R + "sibling-teams-guidelines.pdf",
}
UA = "Mozilla/5.0"


def get(url: str) -> bytes:
    curl = shutil.which("curl")
    if curl:
        p = subprocess.run([curl, "-sSL", "--max-time", "60", "-A", UA, url],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode == 0 and p.stdout.startswith(b"%PDF"):
            return p.stdout
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120, context=ssl.create_default_context()) as r:
        return r.read()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for name in sorted(PDFS):
            print(name)
        return 0
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "pdfs")
    os.makedirs(out, exist_ok=True)
    today = datetime.date.today().isoformat()
    rows, rc = [], 0
    for name, url in sorted(PDFS.items()):
        try:
            blob = get(url)
            if not blob.startswith(b"%PDF"):
                raise ValueError("not a PDF (%d bytes) - moved, retired, or 404" % len(blob))
        except Exception as exc:                       # noqa: BLE001
            print("FAIL %-46s %s" % (name, exc)); rc = 1; continue
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(blob)
        sha = hashlib.sha256(blob).hexdigest()
        rows.append((name, url, len(blob), sha, today))
        print("ok   %-46s %8dB  %s" % (name, len(blob), sha[:16]))
    with open(os.path.join(out, "MANIFEST.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("file,url,bytes,sha256,fetched\n")
        for r in rows:
            fh.write("%s,%s,%d,%s,%s\n" % r)
    print("\nmanifest: %s  (%d ok, %d failed)" % (
        os.path.join(out, "MANIFEST.csv"), len(rows), len(PDFS) - len(rows)))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
