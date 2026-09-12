#!/usr/bin/env python3
"""log-report.py -- WPILOG -> summary JSON/CSV for the AI post-match report pipeline.

Companion doc: reference/ai-integration/01_ai_for_programming.md section 7.

WHY THIS EXISTS
    A 2.5-minute match log at 50 Hz across a few hundred signals is far too large to
    hand to a language model, and models are bad at arithmetic over long numeric
    sequences anyway.  So: **Python does the numerics, the model does the
    interpretation.**  This script produces a compact statistical summary; you paste
    that summary (never the raw log) into prompt #7 of
    reference/ai-integration/templates/programming-prompts.md.

    Every number in the resulting engineering report therefore came from Python.

STATUS -- READ THIS BEFORE YOU DEPEND ON IT     [PARTLY VERIFIED, 2026-08-22]
    The WPILOG reader below is implemented from the published WPILOG binary-format
    specification, NOT from a vendor library.

    VERIFIED : it round-trips a hand-built, spec-conformant WPILOG (header, Start
               control records, double and boolean data records, variable-width
               entry-id / size / timestamp fields) and produces correct stats and a
               correct low-voltage event.  That proves the reader is self-consistent
               with the spec AS I UNDERSTAND IT.
    NOT VERIFIED : it has **never been run against a real robot log** -- no 2027
               Systemcore log exists yet, and no 2026 log was available to the pass
               that wrote this.  A misunderstanding of the spec would not be caught by
               the synthetic test above.

    ACTION (scheduled for October 2026, see 01_ai_for_programming.md section 9):
        python tools/log-report.py entries <some 2026 .wpilog>
    If that prints sensible entry names, the reader works.  If it does not, the fix is
    contained to _read_records() / _read_header().  Do not discover this in the pit.

FORMAT IMPLEMENTED
    header   : b"WPILOG" | u16 version (LE) | u32 extra-header len | extra-header utf8
    record   : bitfield u8 | entry-id | payload-size | timestamp-us | payload
               bitfield bits 0-1 -> entry-id length - 1   (1..4 bytes, LE)
                        bits 2-3 -> payload-size length - 1 (1..4 bytes, LE)
                        bits 4-6 -> timestamp length - 1  (1..8 bytes, LE)
    control  : entry id 0.  payload[0] = 0 Start / 1 Finish / 2 SetMetadata
               Start: u32 entry | u32+utf8 name | u32+utf8 type | u32+utf8 metadata

USAGE
    python tools/log-report.py entries logs/match-07.wpilog
    python tools/log-report.py entries logs/match-07.wpilog --include "Drive/*"

    python tools/log-report.py extract logs/match-07.wpilog --out reports/match-07
    python tools/log-report.py extract logs/match-07.wpilog --out reports/match-07 \
        --include "Drive/*" --include "*Current*" --include "*/Setpoint" \
        --brownout-volts 6.3 --loop-overrun-ms 20 --csv

    # then hand ONLY the summary to the assistant:
    claude -p "$(cat reports/match-07.summary.json)  <paste prompt 7 above this>"

No third-party dependencies.  Python 3.9+.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import math
import os
import struct
import sys
from typing import Any, Dict, Iterator, List, Optional, Tuple

MAGIC = b"WPILOG"
CONTROL_ENTRY = 0
CTRL_START, CTRL_FINISH, CTRL_SET_METADATA = 0, 1, 2

# Signals whose *names* suggest they matter for a match report.  Used only to build the
# default --include set when the user gives none; never used to hide data from `entries`.
DEFAULT_INTEREST = [
    "*Voltage*", "*Volt*", "*Current*", "*Amp*",
    "*Setpoint*", "*Goal*", "*Target*", "*Measured*", "*Position*", "*Velocity*",
    "*Pose*", "*Odometry*", "*Vision*", "*Tag*",
    "*Command*", "*State*", "*Mode*", "*Fault*", "*Error*",
    "*LoopCycleTime*", "*Overrun*", "*CAN*", "*Brownout*", "*Enabled*", "*Match*",
]


# --------------------------------------------------------------------------------------
# binary reading
# --------------------------------------------------------------------------------------

class LogFormatError(RuntimeError):
    pass


def _u32(buf: bytes, off: int) -> Tuple[int, int]:
    if off + 4 > len(buf):
        raise LogFormatError(f"truncated u32 at {off}")
    return struct.unpack_from("<I", buf, off)[0], off + 4


def _sized_str(buf: bytes, off: int) -> Tuple[str, int]:
    n, off = _u32(buf, off)
    if off + n > len(buf):
        raise LogFormatError(f"truncated string ({n} bytes) at {off}")
    return buf[off:off + n].decode("utf-8", errors="replace"), off + n


def _varint_le(data: bytes, off: int, nbytes: int) -> Tuple[int, int]:
    if off + nbytes > len(data):
        raise LogFormatError(f"truncated {nbytes}-byte int at {off}")
    return int.from_bytes(data[off:off + nbytes], "little", signed=False), off + nbytes


def _read_header(data: bytes) -> int:
    if data[:6] != MAGIC:
        raise LogFormatError(
            f"not a WPILOG file: magic is {data[:6]!r}, expected {MAGIC!r}. "
            "If this is an AdvantageKit .wpilogxz it must be decompressed first."
        )
    version = struct.unpack_from("<H", data, 6)[0]
    off = 8
    extra, off = _sized_str(data, off)
    major, minor = version >> 8, version & 0xFF
    if major != 1:
        print(f"[warn] WPILOG major version {major}.{minor} -- reader was written for 1.x. "
              "Output may be wrong. See the STATUS block at the top of this file.",
              file=sys.stderr)
    return off


def _read_records(data: bytes, off: int) -> Iterator[Tuple[int, int, bytes]]:
    """Yield (entry_id, timestamp_us, payload)."""
    n = len(data)
    while off < n:
        bitfield = data[off]
        off += 1
        id_len = (bitfield & 0x03) + 1
        size_len = ((bitfield >> 2) & 0x03) + 1
        ts_len = ((bitfield >> 4) & 0x07) + 1
        entry_id, off = _varint_le(data, off, id_len)
        payload_size, off = _varint_le(data, off, size_len)
        timestamp, off = _varint_le(data, off, ts_len)
        if off + payload_size > n:
            print(f"[warn] truncated final record at byte {off}; stopping.", file=sys.stderr)
            return
        yield entry_id, timestamp, data[off:off + payload_size]
        off += payload_size


def _decode(payload: bytes, typ: str) -> Any:
    """Decode a payload for the scalar/array types this script summarises.

    Unknown or struct/protobuf types return None; they are counted but not analysed.
    """
    try:
        if typ == "double":
            return struct.unpack("<d", payload)[0]
        if typ == "float":
            return struct.unpack("<f", payload)[0]
        if typ == "int64":
            return struct.unpack("<q", payload)[0]
        if typ == "boolean":
            return bool(payload[0])
        if typ in ("string", "json"):
            return payload.decode("utf-8", errors="replace")
        if typ == "double[]":
            return list(struct.unpack(f"<{len(payload)//8}d", payload))
        if typ == "float[]":
            return list(struct.unpack(f"<{len(payload)//4}f", payload))
        if typ == "int64[]":
            return list(struct.unpack(f"<{len(payload)//8}q", payload))
        if typ == "boolean[]":
            return [bool(b) for b in payload]
    except (struct.error, IndexError, UnicodeDecodeError):
        return None
    return None


# --------------------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------------------

class Entry:
    __slots__ = ("eid", "name", "type", "metadata", "samples")

    def __init__(self, eid: int, name: str, typ: str, metadata: str):
        self.eid, self.name, self.type, self.metadata = eid, name, typ, metadata
        self.samples: List[Tuple[float, Any]] = []   # (seconds, value)


def load(path: str) -> Dict[int, Entry]:
    with open(path, "rb") as fh:
        data = fh.read()
    off = _read_header(data)
    entries: Dict[int, Entry] = {}
    for eid, ts_us, payload in _read_records(data, off):
        t = ts_us / 1_000_000.0
        if eid == CONTROL_ENTRY:
            if not payload:
                continue
            kind, o = payload[0], 1
            if kind == CTRL_START:
                start_id, o = _u32(payload, o)
                name, o = _sized_str(payload, o)
                typ, o = _sized_str(payload, o)
                meta, o = _sized_str(payload, o)
                entries[start_id] = Entry(start_id, name, typ, meta)
            elif kind == CTRL_SET_METADATA:
                mid, o = _u32(payload, o)
                meta, o = _sized_str(payload, o)
                if mid in entries:
                    entries[mid].metadata = meta
            # CTRL_FINISH: nothing to do, the entry keeps its samples
            continue
        e = entries.get(eid)
        if e is None:
            continue  # data before its Start record; malformed but survivable
        v = _decode(payload, e.type)
        if v is not None:
            e.samples.append((t, v))
    return entries


def matches(name: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatch(name, p) for p in patterns)


# --------------------------------------------------------------------------------------
# summarising
# --------------------------------------------------------------------------------------

def _num_stats(vals: List[float]) -> Dict[str, float]:
    n = len(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / n
    s = sorted(vals)
    def pct(p: float) -> float:
        k = min(n - 1, max(0, int(round(p * (n - 1)))))
        return s[k]
    return {
        "n": n,
        "min": round(min(vals), 6),
        "max": round(max(vals), 6),
        "mean": round(mean, 6),
        "stdev": round(math.sqrt(var), 6),
        "p05": round(pct(0.05), 6),
        "p50": round(pct(0.50), 6),
        "p95": round(pct(0.95), 6),
        "first": round(vals[0], 6),
        "last": round(vals[-1], 6),
    }


def summarise_entry(e: Entry, args) -> Optional[Dict[str, Any]]:
    if not e.samples:
        return None
    times = [t for t, _ in e.samples]
    out: Dict[str, Any] = {
        "name": e.name,
        "type": e.type,
        "samples": len(e.samples),
        "t_first_s": round(times[0], 3),
        "t_last_s": round(times[-1], 3),
    }
    if e.metadata:
        out["metadata"] = e.metadata[:200]

    v0 = e.samples[0][1]
    if isinstance(v0, bool):
        transitions = [
            {"t_s": round(t, 3), "to": bool(v)}
            for (pt, pv), (t, v) in zip(e.samples, e.samples[1:]) if pv != v
        ]
        out["kind"] = "boolean"
        out["transitions"] = transitions[: args.max_events]
        out["transition_count"] = len(transitions)
        true_time = sum(
            t2 - t1 for (t1, v1), (t2, _) in zip(e.samples, e.samples[1:]) if v1
        )
        out["seconds_true"] = round(true_time, 3)

    elif isinstance(v0, (int, float)):
        vals = [float(v) for _, v in e.samples]
        out["kind"] = "numeric"
        out["stats"] = _num_stats(vals)
        # extremes with timestamps -- the model needs a timestamp to cite
        lo = min(e.samples, key=lambda s: s[1])
        hi = max(e.samples, key=lambda s: s[1])
        out["min_at_s"] = round(lo[0], 3)
        out["max_at_s"] = round(hi[0], 3)

    elif isinstance(v0, str):
        changes = [
            {"t_s": round(t, 3), "value": str(v)[:120]}
            for (pt, pv), (t, v) in zip(e.samples, e.samples[1:]) if pv != v
        ]
        out["kind"] = "string"
        out["change_count"] = len(changes)
        out["changes"] = changes[: args.max_events]

    elif isinstance(v0, list):
        out["kind"] = "array"
        out["array_len_first"] = len(v0)
        # arrays are usually poses / module states; report the update rate only
    else:
        out["kind"] = "other"

    span = times[-1] - times[0]
    out["update_hz"] = round(len(e.samples) / span, 2) if span > 0 else None
    return out


def find_anomalies(entries: Dict[int, Entry], args) -> Dict[str, Any]:
    """Derived findings.  Name-based heuristics -- ALWAYS verify in AdvantageScope."""
    anomalies: Dict[str, Any] = {
        "_note": "Heuristic, name-based. Verify each finding in AdvantageScope before acting.",
    }

    # --- brownouts: any numeric signal whose name looks like battery voltage ---
    brown: List[Dict[str, Any]] = []
    for e in entries.values():
        if not e.samples or not fnmatch.fnmatch(e.name.lower(), "*volt*"):
            continue
        if not isinstance(e.samples[0][1], (int, float)):
            continue
        in_event = False
        floor = None
        start = None
        for t, v in e.samples:
            v = float(v)
            if v < args.brownout_volts and not in_event:
                in_event, floor, start = True, v, t
            elif in_event:
                floor = min(floor, v)
                if v >= args.brownout_volts:
                    brown.append({"signal": e.name, "start_s": round(start, 3),
                                  "end_s": round(t, 3), "floor_v": round(floor, 3)})
                    in_event = False
        if in_event:
            brown.append({"signal": e.name, "start_s": round(start, 3),
                          "end_s": None, "floor_v": round(floor, 3)})
    anomalies["low_voltage_events"] = brown[: args.max_events]
    anomalies["low_voltage_threshold_v"] = args.brownout_volts

    # --- loop overruns: from a cycle-time signal if present, else from sample gaps ---
    over: List[Dict[str, Any]] = []
    limit_s = args.loop_overrun_ms / 1000.0
    cycle = [e for e in entries.values()
             if fnmatch.fnmatch(e.name, "*LoopCycleTime*") or fnmatch.fnmatch(e.name, "*CycleTime*")]
    for e in cycle:
        for t, v in e.samples:
            if isinstance(v, (int, float)):
                # heuristic: values > 1 are probably ms, values < 1 probably seconds
                secs = float(v) / 1000.0 if float(v) > 1.0 else float(v)
                if secs > limit_s:
                    over.append({"signal": e.name, "t_s": round(t, 3),
                                 "cycle_ms": round(secs * 1000.0, 2)})
    if not cycle:
        # fall back: gaps in the highest-rate numeric signal
        best = max((e for e in entries.values() if len(e.samples) > 50),
                   key=lambda e: len(e.samples), default=None)
        if best:
            for (t1, _), (t2, _) in zip(best.samples, best.samples[1:]):
                if t2 - t1 > limit_s * 1.5:
                    over.append({"signal": f"(gap in {best.name})", "t_s": round(t2, 3),
                                 "cycle_ms": round((t2 - t1) * 1000.0, 2)})
    anomalies["loop_overruns"] = sorted(over, key=lambda d: -d["cycle_ms"])[: args.max_events]
    anomalies["loop_overrun_threshold_ms"] = args.loop_overrun_ms

    # --- high current draw ---
    hot: List[Dict[str, Any]] = []
    for e in entries.values():
        if not e.samples or not fnmatch.fnmatch(e.name.lower(), "*current*"):
            continue
        if not isinstance(e.samples[0][1], (int, float)):
            continue
        peak = max(e.samples, key=lambda s: abs(float(s[1])))
        if abs(float(peak[1])) >= args.current_flag_amps:
            hot.append({"signal": e.name, "peak_a": round(float(peak[1]), 2),
                        "t_s": round(peak[0], 3)})
    anomalies["high_current"] = sorted(hot, key=lambda d: -abs(d["peak_a"]))[: args.max_events]
    anomalies["current_flag_threshold_a"] = args.current_flag_amps

    # --- signals that stopped updating mid-log (a device that fell off the bus) ---
    if entries:
        t_end = max((e.samples[-1][0] for e in entries.values() if e.samples), default=0.0)
        stalled = []
        for e in entries.values():
            if len(e.samples) < 20:
                continue
            gap = t_end - e.samples[-1][0]
            if gap > args.stall_seconds:
                stalled.append({"signal": e.name, "last_update_s": round(e.samples[-1][0], 3),
                                "silent_for_s": round(gap, 3)})
        anomalies["signals_that_stopped_updating"] = \
            sorted(stalled, key=lambda d: -d["silent_for_s"])[: args.max_events]
        anomalies["stall_threshold_s"] = args.stall_seconds

    return anomalies


# --------------------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------------------

def cmd_entries(args) -> int:
    entries = load(args.logfile)
    pats = args.include or ["*"]
    rows = [e for e in entries.values() if matches(e.name, pats)]
    rows.sort(key=lambda e: e.name)
    print(f"{len(rows)} entries (of {len(entries)}) in {args.logfile}\n")
    print(f"{'name':<58} {'type':<12} {'n':>7}  {'t0':>8}  {'t1':>8}")
    print("-" * 100)
    for e in rows:
        t0 = f"{e.samples[0][0]:.2f}" if e.samples else "-"
        t1 = f"{e.samples[-1][0]:.2f}" if e.samples else "-"
        print(f"{e.name[:57]:<58} {e.type[:11]:<12} {len(e.samples):>7}  {t0:>8}  {t1:>8}")
    return 0


def cmd_extract(args) -> int:
    entries = load(args.logfile)
    pats = args.include or DEFAULT_INTEREST
    selected = [e for e in entries.values() if matches(e.name, pats)]
    if args.exclude:
        selected = [e for e in selected if not matches(e.name, args.exclude)]
    selected.sort(key=lambda e: e.name)

    signals = [s for s in (summarise_entry(e, args) for e in selected) if s]
    all_times = [t for e in entries.values() for t, _ in e.samples]
    summary = {
        "meta": {
            "source_log": os.path.abspath(args.logfile),
            "generated_by": "tools/log-report.py",
            "reader_status": "UNVERIFIED against a real WPILOG file -- see script header",
            "entries_in_log": len(entries),
            "signals_summarised": len(signals),
            "log_duration_s": round(max(all_times) - min(all_times), 3) if all_times else 0.0,
            "include_patterns": pats,
            "exclude_patterns": args.exclude or [],
        },
        "anomalies": find_anomalies(entries, args),
        "signals": signals,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    jpath = f"{args.out}.summary.json"
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    size_kb = os.path.getsize(jpath) / 1024.0
    print(f"wrote {jpath}  ({size_kb:.1f} KB, {len(signals)} signals)")
    if size_kb > 400:
        print("[warn] summary is large; narrow it with --include before pasting into a prompt.",
              file=sys.stderr)

    if args.csv:
        cpath = f"{args.out}.csv"
        with open(cpath, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["t_s", "signal", "value"])
            for e in selected:
                for t, v in e.samples:
                    w.writerow([f"{t:.4f}", e.name, v])
        print(f"wrote {cpath}")

    a = summary["anomalies"]
    print(f"\n  low-voltage events : {len(a.get('low_voltage_events', []))}")
    print(f"  loop overruns      : {len(a.get('loop_overruns', []))}")
    print(f"  high-current flags : {len(a.get('high_current', []))}")
    print(f"  stopped updating   : {len(a.get('signals_that_stopped_updating', []))}")
    print("\nNext: paste ONLY the .summary.json into prompt #7 of")
    print("      reference/ai-integration/templates/programming-prompts.md")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="WPILOG -> summary JSON/CSV for the AI post-match report pipeline.",
        epilog="See reference/ai-integration/01_ai_for_programming.md section 7.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("entries", help="list every entry in the log (run this first)")
    pe.add_argument("logfile")
    pe.add_argument("--include", action="append", help="glob on signal name; repeatable")
    pe.set_defaults(func=cmd_entries)

    px = sub.add_parser("extract", help="summarise the log to JSON (+ optional CSV)")
    px.add_argument("logfile")
    px.add_argument("--out", required=True, help="output path prefix, e.g. reports/match-07")
    px.add_argument("--include", action="append", help="glob on signal name; repeatable")
    px.add_argument("--exclude", action="append", help="glob on signal name; repeatable")
    px.add_argument("--csv", action="store_true", help="also write a long-format CSV")
    px.add_argument("--brownout-volts", type=float, default=6.3,
                    help="Systemcore default brownout is 6.3 V (configurable). Default: 6.3")
    px.add_argument("--loop-overrun-ms", type=float, default=20.0,
                    help="robot loop period in ms. Default: 20")
    px.add_argument("--current-flag-amps", type=float, default=60.0,
                    help="flag any current signal peaking above this. Default: 60")
    px.add_argument("--stall-seconds", type=float, default=2.0,
                    help="flag a signal silent for this long before the log ends. Default: 2")
    px.add_argument("--max-events", type=int, default=40,
                    help="cap on listed events per category, to keep the JSON promptable")
    px.set_defaults(func=cmd_extract)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except LogFormatError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("The WPILOG reader in this script is UNVERIFIED -- see the header block.",
              file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
