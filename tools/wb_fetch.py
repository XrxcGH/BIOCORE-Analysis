#!/usr/bin/env python3
"""Wayback/direct PDF fetcher with validation.

Usage: python tools/wb_fetch.py JOBS.tsv [--dest DIR] [--log FILE] [--skip-existing]
TSV: outname<TAB>url[<TAB>minkb]   (url may be a raw https URL or wayback id_ URL)
Validates %PDF header, >40KB (or minkb), and pymupdf page_count>0. Deletes junk.
Defaults: --dest manuals/archive/frc and --log logs/fetch_archive_gapfill.log, both
resolved from the repository root (the parent of this script's directory)."""
import argparse, subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "manuals", "archive", "frc")
LOG = os.path.join(ROOT, "logs", "fetch_archive_gapfill.log")

def fetch(url, path):
    cmd = ["curl","-sL","--compressed","--retry","3","--retry-delay","2","-m","300",
           "-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64) FRC-archive-research",
           "-o",path,"-w","%{http_code}",url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip()

def validate(path, minkb=40):
    import pymupdf
    if not os.path.exists(path): return False, "no file"
    sz = os.path.getsize(path)
    with open(path,"rb") as f: head = f.read(5)
    if head != b"%PDF-": return False, f"not a PDF ({sz}B head={head!r})"
    if sz < minkb*1024: return False, f"too small ({sz}B)"
    try:
        d = pymupdf.open(path); n = d.page_count; d.close()
    except Exception as e:
        return False, f"unreadable: {e}"
    if n == 0: return False, "0 pages"
    return True, f"{sz}B {n}p"

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs")
    ap.add_argument("--dest", default=DEST)
    ap.add_argument("--log", default=LOG)
    ap.add_argument("--skip-existing", action="store_true",
                    help="leave a file that is already on disk untouched")
    a = ap.parse_args()
    if not os.path.isfile(a.jobs):
        sys.exit(f"no such jobs file: {a.jobs}")
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        sys.exit("pymupdf missing: python -m pip install pymupdf")
    jobs=[]
    for line in open(a.jobs, encoding="utf-8"):
        line=line.strip()
        if not line or line.startswith("#"): continue
        parts=line.split("\t")
        name,url = parts[0],parts[1]
        minkb = int(parts[2]) if len(parts)>2 else 40
        jobs.append((name,url,minkb))
    os.makedirs(a.dest, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.log)), exist_ok=True)
    log=open(a.log,"a",encoding="utf-8")
    for name,url,minkb in jobs:
        path=os.path.join(a.dest,name); tmp=path+".part"
        if a.skip_existing and os.path.isfile(path) and os.path.getsize(path) > 0:
            print(f"SKIP {name}"); continue
        code=fetch(url,tmp)
        ok,msg=validate(tmp,minkb)
        if ok:
            os.replace(tmp,path); status="OK  "
        else:
            if os.path.exists(tmp): os.remove(tmp)
            status="FAIL"
        line=f"{status} {name}\t{msg}\thttp={code}\t{url}"
        print(line); log.write(line+"\n"); log.flush()
    log.close()

main()
