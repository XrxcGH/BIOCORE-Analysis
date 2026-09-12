#!/usr/bin/env python3
"""
frc_qa_scrape.py -- bulk-export the FIRST Robotics Competition official Q&A.

WHY THIS EXISTS
---------------
https://frc-qa.firstinspires.org is a Meteor (DDP-over-SockJS) single-page app. It has:
  * no REST/JSON API,
  * no "export" button,
  * no season selector -- it serves exactly ONE season at a time and is wiped at rollover,
  * no useful web.archive.org copy (the SPA renders client-side, so snapshots are empty shells).
FIRST publishes a prose PDF export only AFTER the season ends. During the season the ONLY way
to get the whole corpus in machine-readable form is to speak DDP to the app's own publications.

PUBLICATIONS (read-only, unauthenticated)
    qa              accepts a raw Mongo selector + options {sort, limit, skip}. The server caps
                    a single response at 150 documents -- paginate with skip. NOTE: `sort` must
                    use the ARRAY-OF-PAIRS form, e.g. [["asked","asc"]]; the object form
                    {"asked": 1} is rejected server-side with a bare `nosub` (error: None).
    manualSections  no arguments; every manual section used to file questions
    tags            no arguments; the controlled tag vocabulary
    rules           no arguments; the rule list the UI links questions to

Transport: SockJS XHR-polling, stdlib urllib only (no requests / websocket dependency).

Usage
    python tools/frc_qa_scrape.py --out manuals/archive/supplemental/2027_QA --season 2027
Outputs
    <season>_QA_full_export.json   raw documents, one array
    <season>_QA_index.csv          qa_number, manual_section, tags, title, asked, answered
    <season>_QA_full_export.md     readable Q/A text
    <season>_QA_tags.json / _manual_sections.json / _rule_index.json
"""
import argparse
import csv
import json
import os
import random
import string
import sys
import time
import urllib.request

BASE = "https://frc-qa.firstinspires.org"
UA = {"User-Agent": "Mozilla/5.0 (FRC team research archival)"}


def _rand(n, pool=string.ascii_lowercase + string.digits):
    return "".join(random.choice(pool) for _ in range(n))


class DDP:
    """Minimal DDP client over SockJS XHR-polling."""

    def __init__(self, base=BASE):
        self.url = "%s/sockjs/%d/%s" % (base, random.randint(100, 999), _rand(8))
        self._open()

    def _post(self, path, body=None):
        data = body.encode() if body else b""
        headers = dict(UA)
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.url + path, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", "replace")

    def _open(self):
        first = self._post("/xhr")
        if not first.startswith("o"):
            raise RuntimeError("SockJS did not open: %r" % first[:120])
        self.send({"msg": "connect", "version": "1",
                   "support": ["1", "pre2", "pre1"]})
        for _ in range(10):
            for m in self.recv():
                if m.get("msg") == "connected":
                    return
        raise RuntimeError("DDP connect timed out")

    def send(self, obj):
        self._post("/xhr_send", json.dumps([json.dumps(obj)]))

    def recv(self):
        """One poll -> list of decoded DDP messages."""
        raw = self._post("/xhr")
        out = []
        if raw.startswith("a"):
            for s in json.loads(raw[1:]):
                try:
                    out.append(json.loads(s))
                except json.JSONDecodeError:
                    pass
        return out

    def subscribe(self, name, params=None, timeout=90):
        """Subscribe, drain until 'ready', return {collection: {id: doc}}."""
        sub_id = _rand(17)
        self.send({"msg": "sub", "id": sub_id, "name": name, "params": params or []})
        store = {}
        deadline = time.time() + timeout
        while time.time() < deadline:
            for m in self.recv():
                t = m.get("msg")
                if t == "added":
                    d = dict(m.get("fields") or {})
                    d["_id"] = m["id"]
                    store.setdefault(m["collection"], {})[m["id"]] = d
                elif t == "changed":
                    coll = store.setdefault(m["collection"], {})
                    coll.setdefault(m["id"], {"_id": m["id"]}).update(m.get("fields") or {})
                elif t == "nosub":
                    raise RuntimeError("publication %r refused: %s" % (name, m.get("error")))
                elif t == "ready" and sub_id in (m.get("subs") or []):
                    self.send({"msg": "unsub", "id": sub_id})
                    return store
            time.sleep(0.25)
        raise RuntimeError("publication %r never signalled ready" % name)


def fetch_all_qa(page=150):
    """Server caps a response at 150 docs; walk with skip until a page comes back short.

    A fresh DDP connection is opened per page: the server intermittently answers `qa` with a
    bare `nosub` when the connection already carries other subscriptions, and reconnecting is
    cheaper and far more reliable than trying to keep one session healthy.
    """
    docs = {}
    skip = 0
    while True:
        store = DDP().subscribe(
            "qa", [{}, {"sort": [["asked", "asc"]], "limit": page, "skip": skip}])
        got = store.get("qa", {})
        new = {k: v for k, v in got.items() if k not in docs}
        docs.update(got)
        print("  skip=%-5d returned=%-4d new=%-4d total=%d" % (skip, len(got), len(new), len(docs)),
              file=sys.stderr)
        if len(got) < page or not new:
            return docs
        skip += page


def _dt(v):
    try:
        return time.strftime("%Y-%m-%d", time.gmtime(v["$date"] / 1000))
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--season", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    def p(n):
        return os.path.join(a.out, "%s_QA_%s" % (a.season, n))

    for pub, fname in (("tags", "tags.json"),
                       ("manualSections", "manual_sections.json"),
                       ("rules", "rule_index.json")):
        try:
            st = DDP().subscribe(pub)
            coll = list(st.values())[0] if st else {}
            with open(p(fname), "w", encoding="utf-8") as f:
                json.dump(sorted(coll.values(), key=lambda d: str(d.get("_id"))), f,
                          indent=1, ensure_ascii=False, default=str)
            print("%s: %d" % (pub, len(coll)), file=sys.stderr)
        except Exception as e:
            print("%s: FAILED %s" % (pub, e), file=sys.stderr)

    print("qa:", file=sys.stderr)
    qa = fetch_all_qa()

    def key(d):
        return (int(d["_id"]) if str(d["_id"]).isdigit() else 10 ** 9, str(d["_id"]))

    rows = sorted(qa.values(), key=key)
    with open(p("full_export.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1, ensure_ascii=False, default=str)

    with open(p("index.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["qa_number", "manual_section", "tags", "title", "asked", "answered"])
        for d in rows:
            w.writerow([d.get("_id"),
                        (d.get("section") or {}).get("section", ""),
                        ", ".join(t.get("name", "") for t in (d.get("tags") or [])),
                        d.get("title", ""),
                        _dt(d.get("asked") or {}),
                        _dt((d.get("published") or {}).get("date") or {})])

    with open(p("full_export.md"), "w", encoding="utf-8") as f:
        f.write("# FRC %s Q&A -- full export (%d published)\n\n" % (a.season, len(rows)))
        for d in rows:
            f.write("## Q%s -- %s\n\n" % (d.get("_id"), d.get("title", "")))
            f.write("*Section:* %s  \n" % (d.get("section") or {}).get("section", ""))
            f.write("*Tags:* %s  \n" % ", ".join(t.get("name", "") for t in (d.get("tags") or [])))
            f.write("*Asked by:* %s  *Answered:* %s\n\n"
                    % (d.get("askerTeam", ""), _dt((d.get("published") or {}).get("date") or {})))
            f.write("**Q:** %s\n\n" % d.get("question", ""))
            f.write("**A:** %s\n\n---\n\n" % (d.get("published") or {}).get("answer", ""))
    print("wrote %d Q&A to %s" % (len(rows), a.out), file=sys.stderr)


if __name__ == "__main__":
    main()
