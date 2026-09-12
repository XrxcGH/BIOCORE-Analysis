#!/usr/bin/env python3
"""For a target URL, list ALL wayback captures and try each until a valid PDF lands.
Usage: wb_tryall.py OUTNAME URL [minkb] [--dest DIR]
Default --dest is manuals/archive/frc under the repository root (the parent of this
script's directory)."""
import argparse, subprocess, sys, os, urllib.parse, json

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "manuals", "archive", "frc")

def cdx(url):
    q = ("http://web.archive.org/cdx/search/cdx?url=" + urllib.parse.quote(url, safe="") +
         "&fl=timestamp,statuscode,length,original&limit=60")
    r = subprocess.run(["curl","-s","-m","90",q], capture_output=True, text=True)
    rows=[]
    for line in r.stdout.splitlines():
        p=line.split()
        if len(p)>=4 and p[1]=="200":
            rows.append((p[0], int(p[2]), p[3]))
    rows.sort(key=lambda x:-x[1])
    return rows

def validate(path, minkb):
    import pymupdf
    if not os.path.exists(path): return False,"none"
    sz=os.path.getsize(path)
    with open(path,'rb') as f: h=f.read(5)
    if h!=b'%PDF-': return False,f"not pdf {sz}B"
    if sz<minkb*1024: return False,f"small {sz}B"
    try:
        d=pymupdf.open(path); n=d.page_count; d.close()
    except Exception as e: return False,f"unreadable {e}"
    return (n>0), f"{sz}B {n}p"

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outname")
    ap.add_argument("url")
    ap.add_argument("minkb", nargs="?", type=int, default=40)
    ap.add_argument("--dest", default=DEST)
    a = ap.parse_args()
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        sys.exit("pymupdf missing: python -m pip install pymupdf")
    out, url, minkb = a.outname, a.url, a.minkb
    os.makedirs(a.dest, exist_ok=True)
    caps = cdx(url)
    print(f"# {url}: {len(caps)} 200-captures; top lengths {[c[1] for c in caps[:6]]}")
    tmp = os.path.join(a.dest, out+".part")
    for ts,ln,orig in caps[:8]:
        wb=f"https://web.archive.org/web/{ts}id_/{orig}"
        subprocess.run(["curl","-sL","--compressed","--retry","2","-m","300","-o",tmp,wb],
                       capture_output=True)
        ok,msg=validate(tmp,minkb)
        print(f"  try {ts} len={ln} -> {msg}")
        if ok:
            os.replace(tmp, os.path.join(a.dest,out)); print(f"OK  {out} <- {wb}"); return
    if os.path.exists(tmp): os.remove(tmp)
    print(f"FAIL {out} (no good capture)")

main()
