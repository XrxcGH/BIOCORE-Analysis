#!/usr/bin/env python3
"""
award-text.py -- regenerate reference/awards/_text/*.txt from the award PDFs in
reference/awards/pdfs/.

The text files are copies of FIRST's documents, so they are not in the public repository.
Each one is rebuilt with the command that made the original:
  pdftotext -layout       12 files. fla-guide.txt and dla-judging-guidelines.txt are the
                          FIRST Leadership Award guide and judging guidelines, saved again
                          under the names of their download URLs.
  PyMuPDF get_text()      technical-judging-tips.txt
  PyMuPDF find_tables()   award-workbook-TABLES.txt ("=== PAGE n tables:k" headers, cells
                          joined with " || ", in-cell line breaks as " / ", "---" after
                          each table)
The originals were made with the xpdf pdftotext 4.06 that ships with Git for Windows and
PyMuPDF 1.28.2, and text-mode newlines. Other pdftotext builds can differ in whitespace.

Usage:  python tools/award-text.py [--force] [--pdfs DIR] [--out DIR]

Prints one line per file: built, skip (already present; --force rebuilds it), MISSING
(with what it needs) or FAILED. Exits 1 if any file is still absent afterwards.
"""
import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AWARDS = os.path.join(ROOT, "reference", "awards")

# (text file, source PDF, method)
JOBS = [
    ("award-workbook.txt", "award-workbook.pdf", "pdftotext"),
    ("best-practices-for-teams.txt", "best-practices-for-teams.pdf", "pdftotext"),
    ("dla-judging-guidelines.txt", "first-leadership-award-judging-guidelines.pdf", "pdftotext"),
    ("fia-definitions.txt", "fia-definitions.pdf", "pdftotext"),
    ("fia-documentation-form.txt", "fia-documentation-form.pdf", "pdftotext"),
    ("fia-judging-guidelines.txt", "fia-judging-guidelines.pdf", "pdftotext"),
    ("fia-video-consent.txt", "fia-video-consent.pdf", "pdftotext"),
    ("first-leadership-award-guide.txt", "first-leadership-award-guide.pdf", "pdftotext"),
    ("fla-guide.txt", "first-leadership-award-guide.pdf", "pdftotext"),
    ("inside-look-at-judging-process.txt", "inside-look-at-judging-process.pdf", "pdftotext"),
    ("judge-manual.txt", "judge-manual.pdf", "pdftotext"),
    ("sibling-teams-guidelines.txt", "sibling-teams-guidelines.pdf", "pdftotext"),
    ("technical-judging-tips.txt", "technical-judging-tips.pdf", "page-text"),
    ("award-workbook-TABLES.txt", "award-workbook.pdf", "tables"),
]


def rel(path):
    try:
        r = os.path.relpath(path, ROOT)
    except ValueError:
        return path
    return path if r.startswith("..") else r.replace(os.sep, "/")


def page_text(pdf, out):
    import pymupdf
    doc = pymupdf.open(pdf)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    with open(out, "w", encoding="ascii", errors="replace") as fh:
        fh.write(text)


def tables(pdf, out):
    import pymupdf
    doc = pymupdf.open(pdf)
    lines = []
    for pno, page in enumerate(doc, 1):
        found = page.find_tables().tables
        lines.append("=== PAGE %d tables:%d" % (pno, len(found)))
        for table in found:
            for row in table.extract():
                lines.append(" || ".join((cell or "").replace("\n", " / ") for cell in row))
            lines.append("---")
    doc.close()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="rebuild files that already exist")
    ap.add_argument("--pdfs", default=os.path.join(AWARDS, "pdfs"))
    ap.add_argument("--out", default=os.path.join(AWARDS, "_text"))
    a = ap.parse_args()

    have_pdftotext = shutil.which("pdftotext") is not None
    try:
        import pymupdf  # noqa: F401
        have_mupdf = True
    except ImportError:
        have_mupdf = False

    os.makedirs(a.out, exist_ok=True)
    absent = 0
    for name, src, how in JOBS:
        dst = os.path.join(a.out, name)
        pdf = os.path.join(a.pdfs, src)
        if os.path.isfile(dst) and not a.force:
            print("  skip     %s" % rel(dst))
            continue
        need = None
        if not os.path.isfile(pdf):
            need = "needs %s; run: bash tools/rebuild-corpus.sh --fetch" % rel(pdf)
        elif how == "pdftotext" and not have_pdftotext:
            need = "needs pdftotext (poppler-utils or xpdf)"
        elif how != "pdftotext" and not have_mupdf:
            need = "needs PyMuPDF: python -m pip install pymupdf"
        if need:
            print("  MISSING  %s  (%s)" % (rel(dst), need))
            absent += 1
            continue
        try:
            if how == "pdftotext":
                subprocess.run(["pdftotext", "-layout", pdf, dst], check=True,
                               capture_output=True)
            elif how == "page-text":
                page_text(pdf, dst)
            else:
                tables(pdf, dst)
        except Exception as exc:                          # noqa: BLE001
            if os.path.exists(dst):
                os.remove(dst)
            print("  FAILED   %s  (%s)" % (rel(dst), exc))
            absent += 1
            continue
        print("  built    %s" % rel(dst))
    return 1 if absent else 0


if __name__ == "__main__":
    sys.exit(main())
