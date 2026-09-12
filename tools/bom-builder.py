#!/usr/bin/env python3
"""bom-builder.py -- compose a robot BOM from mechanism archetypes and gate it against team capacity.

Reads:
    reference/bom/mechanism_catalog.yaml   the archetype catalog (COTS + fabricated + hours)
    reference/team_capacity.yaml           the gate thresholds for THIS team
    <input.yaml>                           mechanism ids + an optional target: block
                                           (see reference/bom/examples/)

Writes to stdout:
    per-mechanism BOM (COTS lines and FABRICATED lines), rollups, GATE CHECKS,
    delivery envelopes vs the declared scoring target, and an order-by schedule counted back
    from kickoff (2027-01-09).

The GEOMETRY (REACH) gate: if the input declares
    target: {name:, aperture_height_in:, aperture_range_in:, source:}
then at least one mechanism must be able to deliver into that aperture, or the run FAILS and
names the shortfall in inches. If no target is declared the run prints a loud WARNING -- that
silence is what let the 2026 rehearsal cost, gate, schedule and order parts for a hopper dump
aimed at a 72 in HUB lip (review/REHEARSAL_GRADE.md sec 5).

Usage:
    python tools/bom-builder.py reference/bom/examples/simple.yaml
    python tools/bom-builder.py <input.yaml> --markdown
    python tools/bom-builder.py <input.yaml> --csv out.csv
    python tools/bom-builder.py <input.yaml> --catalog X.yaml --capacity Y.yaml
    python tools/bom-builder.py --list

Exit codes: 0 = all gates pass, 1 = at least one gate FAILS, 2 = bad input.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("bom-builder.py requires PyYAML:  pip install pyyaml\n")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_CATALOG = os.path.join(ROOT, "reference", "bom", "mechanism_catalog.yaml")
DEFAULT_CAPACITY = os.path.join(ROOT, "reference", "team_capacity.yaml")

TOOLING_RANK = {
    "hand_tools": 1,
    "bandsaw_drillpress": 2,
    "router_cnc": 3,
    "mill_lathe": 4,
    "outsourced": 5,
}

BAR = "=" * 78
SUB = "-" * 78


# --------------------------------------------------------------------------- io
def load_yaml(path: str) -> dict:
    if not os.path.exists(path):
        sys.stderr.write("ERROR: file not found: %s\n" % path)
        sys.exit(2)
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def resolve_requests(spec: dict, catalog: dict) -> list:
    """Accept either a bare list of ids or a list of {id:, note:} dicts."""
    raw = spec.get("mechanisms")
    if not raw:
        sys.stderr.write("ERROR: input yaml has no non-empty 'mechanisms:' list\n")
        sys.exit(2)
    by_id = {m["id"]: m for m in catalog["mechanisms"]}
    out, missing = [], []
    for item in raw:
        if isinstance(item, str):
            mid, note = item, None
        elif isinstance(item, dict):
            mid, note = item.get("id"), item.get("note")
        else:
            missing.append(repr(item))
            continue
        if mid not in by_id:
            missing.append(mid)
            continue
        out.append((by_id[mid], note))
    if missing:
        sys.stderr.write("ERROR: unknown mechanism id(s): %s\n" % ", ".join(map(str, missing)))
        sys.stderr.write("Run with --list to see valid ids.\n")
        sys.exit(2)
    return out


# ------------------------------------------------------------------- computation
def line_price(part: dict):
    """Returns (unit, is_estimate). Never promotes an estimate into a price field."""
    if part.get("unit_price") is not None:
        return float(part["unit_price"]), False
    if part.get("est_unit_price") is not None:
        return float(part["est_unit_price"]), True
    return 0.0, True


def order_by_date(mech: dict, kickoff: dt.date, margin_weeks: int) -> dt.date:
    weeks = int(mech.get("lead_time_weeks") or 0) + int(margin_weeks)
    return kickoff - dt.timedelta(weeks=weeks)


def build(requests, catalog, capacity):
    kickoff = dt.date.fromisoformat(str(capacity["lead_time"]["kickoff_date"]))
    margin = int(capacity["lead_time"].get("order_by_safety_margin_weeks", 0))
    r = {
        "mechanisms": [],
        "cots_total": 0.0, "material_total": 0.0, "grand_total": 0.0,
        "estimated_dollars": 0.0, "verified_dollars": 0.0,
        "build_hours": 0.0, "design_hours": 0.0, "programming_hours": 0.0, "fab_hours": 0.0,
        "motors": 0, "controllers": 0, "kop_credit": 0.0, "discretionary_total": 0.0,
        "verified_lines": 0, "unverified_lines": 0,
        "pneumatics": False,
        "max_tooling_rank": 0, "max_tooling": "hand_tools",
        "kickoff": kickoff,
    }
    for mech, note in requests:
        cots_lines, cots_sum = [], 0.0
        for p in mech["cots_parts"]:
            unit, est = line_price(p)
            ext = unit * p["qty"]
            cots_sum += ext
            cots_lines.append({
                "vendor": p.get("vendor") or "UNVERIFIED", "item": p["item"],
                "sku": p.get("sku") or "-", "qty": p["qty"], "unit": unit, "ext": ext,
                "url": p.get("url") or "-", "verified": bool(p.get("verified")), "estimated": est,
            })
            if p.get("verified"):
                r["verified_lines"] += 1
                r["verified_dollars"] += ext
            else:
                r["unverified_lines"] += 1
                r["estimated_dollars"] += ext
        fab_lines = [{
            "part": f["part"], "material": f["material"], "process": f["process"],
            "machine": f["machine_required"], "qty": f["qty"], "hours": f["est_hours"],
        } for f in mech["fabricated_parts"]]

        rank = TOOLING_RANK.get(mech["tooling_floor"], 9)
        if rank > r["max_tooling_rank"]:
            r["max_tooling_rank"], r["max_tooling"] = rank, mech["tooling_floor"]

        entry = {
            "mech": mech, "note": note, "cots": cots_lines, "fab": fab_lines,
            "cots_sum": cots_sum, "material": float(mech["material_cost_usd"]),
            "total": cots_sum + float(mech["material_cost_usd"]),
            "fab_hours": sum(f["hours"] for f in fab_lines),
            "order_by": order_by_date(mech, kickoff, margin),
            "kop_credit": float(mech.get("kop_credit_usd") or 0.0),
        }
        r["mechanisms"].append(entry)
        r["cots_total"] += cots_sum
        r["material_total"] += entry["material"]
        r["grand_total"] += entry["total"]
        r["kop_credit"] += entry["kop_credit"]
        r["build_hours"] += mech["build_hours"]
        r["design_hours"] += mech["design_hours"]
        r["programming_hours"] += mech["programming_hours"]
        r["fab_hours"] += entry["fab_hours"]
        r["motors"] += mech["motors_required"]
        r["controllers"] += mech["controllers_required"]
        r["pneumatics"] = r["pneumatics"] or bool(mech["pneumatics_required"])

    r["discretionary_total"] = r["grand_total"] - r["kop_credit"]
    r["novel"] = [e for e in r["mechanisms"] if e["mech"].get("counts_as_novel")]
    r["workstreams"] = sorted({e["mech"]["workstream"] for e in r["mechanisms"]})
    # A mechanism that is cheap in attention -- no motors AND <=12 build hours -- is absorbed
    # into an adjacent workstream rather than opening a new one. See 02_TEAM_CAPACITY_MODEL sec 5.
    heavy = [e for e in r["mechanisms"]
             if e["mech"]["motors_required"] > 0 or e["mech"]["build_hours"] > 12]
    r["effective_workstreams"] = sorted({e["mech"]["workstream"] for e in heavy})
    r["absorbed"] = [e["mech"]["id"] for e in r["mechanisms"] if e not in heavy]
    return r


# ------------------------------------------------- geometric feasibility (reach)
def geometry_check(r, spec):
    """Can anything in this config physically deliver into the declared scoring aperture?

    Returns a dict describing the outcome. `checked` False means the config declared no
    `target:` block -- which is NOT a pass. It is the exact silence that let the 2026 rehearsal
    cost, gate, schedule and order parts for a hopper dump aimed at a 72 in HUB lip.

    Reach model:
      * a mechanism with requires_carrier gets its height from the tallest carrier in the
        config (provides_carrier) plus its own small offset; alone it reaches ~nothing;
      * every other mechanism stands on its own delivery envelope;
      * a mechanism clears the target when
            min_height_in <= aperture_height_in <= max_height_in   and
            max_range_in  >= aperture_range_in.
    """
    tgt = spec.get("target")
    mechs = [e["mech"] for e in r["mechanisms"]]
    with_delivery = [m for m in mechs if isinstance(m.get("delivery"), dict)]
    no_delivery_scoring = [m["id"] for m in mechs
                           if not isinstance(m.get("delivery"), dict)
                           and [c for c in (m.get("game_piece_classes") or []) if c != "none"]]

    carriers = [m for m in with_delivery if m["delivery"].get("provides_carrier")]
    best_carrier = max((m["delivery"].get("max_height_in") or 0 for m in carriers), default=0)
    carrier_id = None
    for m in carriers:
        if (m["delivery"].get("max_height_in") or 0) == best_carrier:
            carrier_id = m["id"]
            break

    rows = []
    for m in with_delivery:
        d = m["delivery"]
        own_hi = float(d.get("max_height_in") or 0)
        own_lo = float(d.get("min_height_in") or 0)
        rng = float(d.get("max_range_in") or 0)
        via = None
        if d.get("requires_carrier"):
            if not carriers:
                hi, lo = own_hi, own_lo
                via = "NO CARRIER IN CONFIG"
            else:
                hi, lo, via = best_carrier + own_hi, own_lo, "carried by %s" % carrier_id
        else:
            hi, lo = own_hi, own_lo
        rows.append({"id": m["id"], "mode": d.get("mode", "?"), "lo": lo, "hi": hi,
                     "range": rng, "via": via, "evidence": d.get("evidence", "?")})

    res = {"checked": bool(tgt), "rows": rows, "target": tgt,
           "no_delivery_scoring": no_delivery_scoring,
           "best_reach": max((x["hi"] for x in rows), default=0.0),
           "best_id": None, "clears": [], "shortfall_in": None, "range_short_in": None,
           "unverified": sorted({x["id"] for x in rows if x["evidence"] == "UNVERIFIED"})}
    for x in rows:
        if x["hi"] == res["best_reach"]:
            res["best_id"] = x["id"]
            break
    if not tgt:
        return res

    ah = float(tgt.get("aperture_height_in") or 0)
    ar = float(tgt.get("aperture_range_in") or 0)
    res["clears"] = [x for x in rows if x["lo"] <= ah <= x["hi"] and x["range"] >= ar]
    if not res["clears"]:
        res["shortfall_in"] = round(ah - res["best_reach"], 1)
        tall = [x for x in rows if x["lo"] <= ah <= x["hi"]]
        if tall:
            res["range_short_in"] = round(ar - max(x["range"] for x in tall), 1)
    return res


def geometry_gate(geo):
    """One gate row, in the same shape as gate_checks() rows."""
    if not geo["checked"]:
        return {"gate": "GEOMETRY (REACH)", "pass": True,
                "actual": "*** NOT CHECKED ***",
                "limit": "no target: declared",
                "msg": "NO GEOMETRIC FEASIBILITY WAS CHECKED. Declare target: {name, "
                       "aperture_height_in, aperture_range_in, source} in the bom_config. "
                       "Silence here is what shipped a hopper dump against a 72 in HUB in the "
                       "2026 rehearsal (review/REHEARSAL_GRADE.md sec 5)."}
    t = geo["target"]
    ah = float(t.get("aperture_height_in") or 0)
    ar = float(t.get("aperture_range_in") or 0)
    if ah <= 0:
        # A declared target with a zero/absent height is not an answer -- it would let every
        # config clear a 0 in aperture and reinstate exactly the silence this gate exists to end.
        return {"gate": "GEOMETRY (REACH)", "pass": False,
                "actual": "aperture_height_in = %s" % t.get("aperture_height_in"),
                "limit": "> 0 in required",
                "msg": "TARGET DECLARED BUT NOT ANSWERED: aperture_height_in is missing or 0, so "
                       "every mechanism would 'clear' it. Read the scoring opening height off the "
                       "carpet out of the manual and put it here -- reference/03_ARCHETYPE_CORPUS.md "
                       "2.4 item 4: find this number FIRST. (2026 REBUILT HUB lip = 72 in.)"}
    label = "%s: aperture %.0f in up, %.0f in out (%s)" % (
        t.get("name", "unnamed target"), ah, ar, t.get("source", "SOURCE NOT CITED"))
    if geo["clears"]:
        best = max(geo["clears"], key=lambda x: x["hi"])
        return {"gate": "GEOMETRY (REACH)", "pass": True,
                "actual": "%s reaches %.0f in (%s)" % (best["id"], best["hi"], best["mode"]),
                "limit": "%.0f in" % ah,
                "msg": "%s | clears by %.0f in: %s" % (
                    label, best["hi"] - ah, ", ".join(x["id"] for x in geo["clears"]))}
    msg = ("%s | NOTHING IN THIS CONFIG CAN REACH THE SCORING TARGET. Tallest delivery is %s at "
           "%.0f in -- SHORT BY %.0f INCHES." % (label, geo["best_id"], geo["best_reach"],
                                                 geo["shortfall_in"]))
    if geo["range_short_in"] is not None and geo["range_short_in"] > 0:
        msg += (" Height is met by some mechanism but standoff is short by %.0f in."
                % geo["range_short_in"])
    msg += (" This robot would be fully costed, gated, scheduled and ordered -- and would score "
            "zero. Change the mechanism, not the gate.")
    return {"gate": "GEOMETRY (REACH)", "pass": False,
            "actual": "best reach %.0f in (%s)" % (geo["best_reach"], geo["best_id"]),
            "limit": "%.0f in" % ah, "msg": msg}


def geometry_banner(geo, markdown=False):
    L = []
    if not geo["checked"]:
        if markdown:
            L += ["", "> ## WARNING -- GEOMETRIC FEASIBILITY NOT CHECKED", ">",
                  "> This BOM declares no `target:`. The builder validated dollars, hours, "
                  "workstreams and motors and has **no idea whether this robot can reach the "
                  "scoring aperture.**",
                  "> Add to the bom_config:",
                  "> ```yaml",
                  "> target:",
                  ">   name: \"HUB upper opening\"",
                  ">   aperture_height_in: 72",
                  ">   aperture_range_in: 0",
                  ">   source: \"manual s5.4\"",
                  "> ```",
                  "> Find the number FIRST -- `reference/03_ARCHETYPE_CORPUS.md` 2.4 item 4."]
        else:
            L += ["", "!" * 78,
                  "!!  WARNING -- GEOMETRIC FEASIBILITY WAS NOT CHECKED",
                  "!!",
                  "!!  This configuration declares no  target:  block, so NOTHING here verifies",
                  "!!  that the robot can physically reach the scoring aperture. Dollars, hours,",
                  "!!  workstreams and motors were all checked. Reach was not.",
                  "!!",
                  "!!  Add to the bom_config:",
                  "!!      target:",
                  "!!        name: \"HUB upper opening\"",
                  "!!        aperture_height_in: 72        # from the manual, not from memory",
                  "!!        aperture_range_in: 0          # 0 = may be approached at contact",
                  "!!        source: \"manual s5.4\"",
                  "!!",
                  "!!  Find this number FIRST -- reference/03_ARCHETYPE_CORPUS.md 2.4 item 4.",
                  "!!  The 2026 rehearsal costed a hopper dump (30 in rim) against a 72 in HUB",
                  "!!  lip and shipped an order schedule for it. No tool objected. This is that",
                  "!!  tool objecting.", "!" * 78]
        return L
    if geo["no_delivery_scoring"]:
        line = ("NOTE: no delivery envelope in the catalog for piece-handling mechanism(s): %s "
                "-- they were excluded from the reach check." % ", ".join(geo["no_delivery_scoring"]))
        L += ["", ("> " if markdown else "  ") + line]
    if geo["unverified"]:
        line = ("CAUTION: reach envelope is UNVERIFIED for %s -- the number gating this decision "
                "is a planning figure, not a vendor spec." % ", ".join(geo["unverified"]))
        L += ["", ("> " if markdown else "  ") + line]
    return L


# ------------------------------------------------------------------- gate checks
def gate_checks(r, capacity):
    g = capacity["gates"]
    team_rank = TOOLING_RANK.get(g["tooling_level"], 2)
    out = []

    def add(name, ok, actual, limit, msg):
        out.append({"gate": name, "pass": ok, "actual": actual, "limit": limit, "msg": msg})

    add("BUDGET", r["discretionary_total"] <= g["budget_cap_usd"],
        "$%.2f discretionary (gross $%.2f - KOP credit $%.2f)"
        % (r["discretionary_total"], r["grand_total"], r["kop_credit"]),
        "$%.2f" % g["budget_cap_usd"],
        "robot_discretionary is the number design trades score against (02_TEAM_CAPACITY_MODEL sec 8.1)")

    over = [e["mech"]["id"] + " (" + e["mech"]["tooling_floor"] + ")"
            for e in r["mechanisms"]
            if TOOLING_RANK.get(e["mech"]["tooling_floor"], 9) > team_rank]
    outsourceable = capacity["tooling"].get("outsourcing_available", False)
    add("TOOLING FLOOR", not over, r["max_tooling"], g["tooling_level"],
        ("needs outsourcing or shop upgrade: " + ", ".join(over)) if over else "every mechanism is within shop capability")
    if over and outsourceable:
        out[-1]["msg"] += " | outsourcing_available: true (budget $%s, +%s wk lead)" % (
            capacity["tooling"].get("outsourcing_budget_usd"),
            capacity["tooling"].get("outsourcing_lead_time_weeks"))

    add("BUILD HOURS", r["build_hours"] <= g["build_hours_cap"],
        "%.1f h" % r["build_hours"], "%.1f h" % g["build_hours_cap"],
        "fabrication_assembly line, kickoff -> Week 1 (02_TEAM_CAPACITY_MODEL sec 3.1)")
    add("DESIGN HOURS", r["design_hours"] <= g["design_hours_cap"],
        "%.1f h" % r["design_hours"], "%.1f h" % g["design_hours_cap"], "cad_design line")
    add("PROGRAMMING HOURS", r["programming_hours"] <= g["programming_hours_cap"],
        "%.1f h" % r["programming_hours"], "%.1f h" % g["programming_hours_cap"],
        "2027 is a Systemcore port year -- this line is already inflated ~40 h")

    add("PARALLEL WORKSTREAMS", len(r["effective_workstreams"]) <= g["parallel_mechanisms_cap"],
        "%d effective (%d mechanisms)" % (len(r["effective_workstreams"]), len(r["mechanisms"])),
        "%d" % g["parallel_mechanisms_cap"],
        "effective: " + ", ".join(r["effective_workstreams"])
        + ("; absorbed (0 motors, <=12 build h): " + ", ".join(r["absorbed"]) if r["absorbed"] else ""))
    add("NOVEL MECHANISMS", len(r["novel"]) <= g["novel_mechanisms_cap"],
        "%d" % len(r["novel"]), "%d" % g["novel_mechanisms_cap"],
        "novel = " + (", ".join(e["mech"]["id"] for e in r["novel"]) or "none"))
    add("MOTOR COUNT", r["motors"] <= g["motor_cap"],
        "%d motors / %d controllers" % (r["motors"], r["controllers"]), "%d" % g["motor_cap"],
        "propulsion cap is separately %d (2026 R502; 2027 UNVERIFIED)" % capacity["motors"]["propulsion_motor_cap"])
    return out


# ------------------------------------------------------------------------ output
def money(x):
    return "$%9s" % ("%.2f" % x)


def render_text(r, gates, spec, capacity, geo):
    L = []
    A = L.append
    A(BAR)
    A("BOM BUILDER -- %s" % (spec.get("name") or "unnamed configuration"))
    A("catalog: reference/bom/mechanism_catalog.yaml   capacity: reference/team_capacity.yaml")
    if spec.get("notes"):
        A("notes: %s" % spec["notes"])
    A(BAR)

    for e in r["mechanisms"]:
        m = e["mech"]
        A("")
        A("### %s  [%s / %s]" % (m["name"], m["category"], m["workstream"]))
        A("    id=%s  tooling=%s  motors=%d  lead=%dwk  stockout=%s  evidence=%s"
          % (m["id"], m["tooling_floor"], m["motors_required"], m["lead_time_weeks"],
             m["stockout_risk"], m.get("evidence", "?")))
        if e["note"]:
            A("    note: %s" % e["note"])
        A(SUB)
        A("  COTS")
        A("    %-26s %-34s %-16s %3s %10s %10s %s"
          % ("VENDOR", "ITEM", "SKU", "QTY", "UNIT", "EXT", "V"))
        for c in e["cots"]:
            A("    %-26s %-34s %-16s %3d %10s %10s %s"
              % (c["vendor"][:26], c["item"][:34], str(c["sku"])[:16], c["qty"],
                 ("~%.2f" % c["unit"]) if c["estimated"] else ("%.2f" % c["unit"]),
                 "%.2f" % c["ext"], "v" if c["verified"] else "U"))
            if c["url"] != "-":
                A("        %s" % c["url"])
        A("  FABRICATED")
        A("    %-32s %-30s %-18s %-20s %3s %6s"
          % ("PART", "MATERIAL", "PROCESS", "MACHINE", "QTY", "HOURS"))
        for f in e["fab"]:
            A("    %-32s %-30s %-18s %-20s %3d %6.1f"
              % (f["part"][:32], f["material"][:30], f["process"][:18], f["machine"][:20],
                 f["qty"], f["hours"]))
        A("  SUBTOTAL  cots %s  material %s  total %s"
          % (money(e["cots_sum"]), money(e["material"]), money(e["total"])))
        A("  HOURS     build %5.1f  design %5.1f  programming %5.1f  (fab-detail %4.1f)"
          % (m["build_hours"], m["design_hours"], m["programming_hours"], e["fab_hours"]))
        A("  ORDER BY  %s   (kickoff %s minus %d wk lead + %d wk margin)"
          % (e["order_by"], r["kickoff"], m["lead_time_weeks"],
             capacity["lead_time"].get("order_by_safety_margin_weeks", 0)))

    A("")
    A(BAR)
    A("ROLLUP")
    A(BAR)
    A("  COTS subtotal                 %s" % money(r["cots_total"]))
    A("  Material / raw stock          %s" % money(r["material_total"]))
    A("  GRAND TOTAL (gross)           %s" % money(r["grand_total"]))
    A("  less KOP-supplied credit      %s" % money(-r["kop_credit"]))
    A("  DISCRETIONARY SPEND           %s   <-- the number the budget gate uses"
      % money(r["discretionary_total"]))
    A("      of which price-verified   %s   (%d COTS lines)" % (money(r["verified_dollars"]), r["verified_lines"]))
    A("      of which ESTIMATED        %s   (%d COTS lines, marked ~ and U)"
      % (money(r["estimated_dollars"]), r["unverified_lines"]))
    A("")
    A("  Build hours       %6.1f      Design hours   %6.1f      Programming hours %6.1f"
      % (r["build_hours"], r["design_hours"], r["programming_hours"]))
    A("  Motors            %6d      Controllers    %6d      Pneumatics        %6s"
      % (r["motors"], r["controllers"], "YES" if r["pneumatics"] else "no"))
    A("  Mechanisms        %6d      Novel          %6d      Workstreams       %6d (eff %d)"
      % (len(r["mechanisms"]), len(r["novel"]), len(r["workstreams"]),
         len(r["effective_workstreams"])))
    A("  Highest tooling floor required: %s" % r["max_tooling"])

    for ln in geometry_banner(geo):
        A(ln)
    if geo["checked"]:
        A("")
        A(BAR)
        A("DELIVERY ENVELOPES  (vs target %s)" % geo["target"].get("name", "?"))
        A(BAR)
        A("  %-26s %-6s %9s %9s %9s  %s"
          % ("MECHANISM", "MODE", "MIN_H_IN", "MAX_H_IN", "RANGE_IN", "EV / VIA"))
        for x in sorted(geo["rows"], key=lambda z: -z["hi"]):
            A("  %-26s %-6s %9.0f %9.0f %9.0f  %s"
              % (x["id"][:26], x["mode"], x["lo"], x["hi"], x["range"],
                 x["evidence"] + ("  " + x["via"] if x["via"] else "")))
        A("  TARGET  %s -- %.0f in up, %.0f in out   source: %s"
          % (geo["target"].get("name", "?"), float(geo["target"].get("aperture_height_in") or 0),
             float(geo["target"].get("aperture_range_in") or 0),
             geo["target"].get("source", "SOURCE NOT CITED")))

    A("")
    A(BAR)
    A("GATE CHECKS  (vs reference/team_capacity.yaml + the declared scoring target)")
    A(BAR)
    for g in gates:
        A("  [%s] %-20s %-28s limit %-16s" % ("PASS" if g["pass"] else "FAIL", g["gate"],
                                              g["actual"], g["limit"]))
        A("         %s" % g["msg"])
    failed = [g["gate"] for g in gates if not g["pass"]]
    A("")
    A("  VERDICT: %s" % ("ALL GATES PASS" if not failed else "FAILS %d GATE(S): %s"
                         % (len(failed), ", ".join(failed))))

    A("")
    A(BAR)
    A("ORDER SCHEDULE  (counted back from kickoff %s)" % r["kickoff"])
    A(BAR)
    for e in sorted(r["mechanisms"], key=lambda x: x["order_by"]):
        A("  %s   %-30s %2d wk lead   stockout=%s"
          % (e["order_by"], e["mech"]["id"], e["mech"]["lead_time_weeks"], e["mech"]["stockout_risk"]))
    earliest = min(e["order_by"] for e in r["mechanisms"])
    A("")
    A("  EARLIEST ORDER-BY: %s  -- anything high-stockout must be on a PO by this date." % earliest)
    A("  Note: no bag day since 2020, so build continues to the event; these dates protect")
    A("  the kickoff-to-Week-1 window, not a bag deadline.")
    if not geo["checked"]:
        for ln in geometry_banner(geo):
            A(ln)
    return "\n".join(L)


def render_markdown(r, gates, spec, capacity, geo):
    L = []
    A = L.append
    A("# BOM -- %s" % (spec.get("name") or "unnamed configuration"))
    A("")
    A("Generated by `tools/bom-builder.py` from `reference/bom/mechanism_catalog.yaml`")
    A("and gated against `reference/team_capacity.yaml`. Kickoff **%s**." % r["kickoff"])
    if spec.get("notes"):
        A("")
        A("> %s" % spec["notes"])
    for e in r["mechanisms"]:
        m = e["mech"]
        A("")
        A("## %s" % m["name"])
        A("")
        A("`%s` | %s / %s | tooling **%s** | %d motors | %d wk lead | stockout **%s**"
          % (m["id"], m["category"], m["workstream"], m["tooling_floor"],
             m["motors_required"], m["lead_time_weeks"], m["stockout_risk"]))
        A("")
        A("| Vendor | Item | SKU | Qty | Unit | Ext | Verified |")
        A("|---|---|---|---:|---:|---:|:---:|")
        for c in e["cots"]:
            A("| %s | %s | `%s` | %d | %s%.2f | %.2f | %s |"
              % (c["vendor"], c["item"], c["sku"], c["qty"], "~$" if c["estimated"] else "$",
                 c["unit"], c["ext"], "yes" if c["verified"] else "**UNVERIFIED**"))
        A("")
        A("| Fabricated part | Material | Process | Machine | Qty | Hours |")
        A("|---|---|---|---|---:|---:|")
        for f in e["fab"]:
            A("| %s | %s | %s | `%s` | %d | %.1f |"
              % (f["part"], f["material"], f["process"], f["machine"], f["qty"], f["hours"]))
        A("")
        A("**Subtotal** COTS $%.2f + material $%.2f = **$%.2f** | build %.1f h, design %.1f h, "
          "programming %.1f h | **order by %s**"
          % (e["cots_sum"], e["material"], e["total"], m["build_hours"], m["design_hours"],
             m["programming_hours"], e["order_by"]))
    A("")
    A("## Rollup")
    A("")
    A("| Metric | Value |")
    A("|---|---:|")
    A("| COTS subtotal | $%.2f |" % r["cots_total"])
    A("| Material | $%.2f |" % r["material_total"])
    A("| Grand total (gross) | $%.2f |" % r["grand_total"])
    A("| KOP-supplied credit | -$%.2f |" % r["kop_credit"])
    A("| **Discretionary spend** | **$%.2f** |" % r["discretionary_total"])
    A("| Price-verified dollars | $%.2f (%d lines) |" % (r["verified_dollars"], r["verified_lines"]))
    A("| Estimated dollars | $%.2f (%d lines) |" % (r["estimated_dollars"], r["unverified_lines"]))
    A("| Build hours | %.1f |" % r["build_hours"])
    A("| Design hours | %.1f |" % r["design_hours"])
    A("| Programming hours | %.1f |" % r["programming_hours"])
    A("| Motors / controllers | %d / %d |" % (r["motors"], r["controllers"]))
    A("| Mechanisms / novel / effective workstreams | %d / %d / %d |"
      % (len(r["mechanisms"]), len(r["novel"]), len(r["effective_workstreams"])))
    A("| Highest tooling floor | %s |" % r["max_tooling"])
    A("")
    for ln in geometry_banner(geo, markdown=True):
        A(ln)
    if geo["checked"]:
        A("")
        A("## Delivery envelopes")
        A("")
        A("Target **%s** -- aperture **%.0f in** above the carpet, **%.0f in** standoff (source: %s)."
          % (geo["target"].get("name", "?"), float(geo["target"].get("aperture_height_in") or 0),
             float(geo["target"].get("aperture_range_in") or 0),
             geo["target"].get("source", "SOURCE NOT CITED")))
        A("")
        A("| Mechanism | Mode | Min h (in) | Max h (in) | Range (in) | Evidence | Note |")
        A("|---|---|---:|---:|---:|:---:|---|")
        for x in sorted(geo["rows"], key=lambda z: -z["hi"]):
            A("| `%s` | %s | %.0f | %.0f | %.0f | %s | %s |"
              % (x["id"], x["mode"], x["lo"], x["hi"], x["range"], x["evidence"], x["via"] or ""))
        A("")
    A("## Gate checks")
    A("")
    A("| Gate | Result | Actual | Limit | Note |")
    A("|---|:---:|---|---|---|")
    for g in gates:
        A("| %s | %s | %s | %s | %s |"
          % (g["gate"], "PASS" if g["pass"] else "**FAIL**", g["actual"], g["limit"], g["msg"]))
    failed = [g["gate"] for g in gates if not g["pass"]]
    A("")
    A("**Verdict: %s**" % ("ALL GATES PASS" if not failed else "FAILS -- " + ", ".join(failed)))
    A("")
    A("## Order schedule")
    A("")
    A("| Order by | Mechanism | Lead (wk) | Stockout |")
    A("|---|---|---:|---|")
    for e in sorted(r["mechanisms"], key=lambda x: x["order_by"]):
        A("| %s | `%s` | %d | %s |" % (e["order_by"], e["mech"]["id"],
                                       e["mech"]["lead_time_weeks"], e["mech"]["stockout_risk"]))
    return "\n".join(L)


def write_csv(r, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["mechanism_id", "mechanism_name", "line_type", "vendor_or_material",
                    "item_or_part", "sku_or_process", "machine", "qty", "unit_price",
                    "ext_price", "hours", "verified", "url", "order_by"])
        for e in r["mechanisms"]:
            m = e["mech"]
            for c in e["cots"]:
                w.writerow([m["id"], m["name"], "COTS", c["vendor"], c["item"], c["sku"], "",
                            c["qty"], "%.2f" % c["unit"], "%.2f" % c["ext"], "",
                            "yes" if c["verified"] else "UNVERIFIED", c["url"], e["order_by"]])
            for f in e["fab"]:
                w.writerow([m["id"], m["name"], "FABRICATED", f["material"], f["part"],
                            f["process"], f["machine"], f["qty"], "", "", "%.1f" % f["hours"],
                            "n/a", "", e["order_by"]])
            w.writerow([m["id"], m["name"], "MATERIAL_STOCK", "raw stock allowance", "", "", "",
                        1, "%.2f" % e["material"], "%.2f" % e["material"], "", "estimate", "",
                        e["order_by"]])
        w.writerow([])
        w.writerow(["TOTAL", "", "", "", "", "", "", "", "", "%.2f" % r["grand_total"],
                    "%.1f" % r["build_hours"], "", "", ""])


# -------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Build and gate an FRC robot BOM from mechanism archetypes.")
    ap.add_argument("input", nargs="?", help="input yaml listing mechanism ids")
    ap.add_argument("--catalog", default=DEFAULT_CATALOG)
    ap.add_argument("--capacity", default=DEFAULT_CAPACITY)
    ap.add_argument("--markdown", action="store_true", help="emit markdown instead of text")
    ap.add_argument("--csv", metavar="PATH", help="also write a flat CSV of every line")
    ap.add_argument("--list", action="store_true", help="list every mechanism id in the catalog and exit")
    a = ap.parse_args(argv)

    catalog = load_yaml(a.catalog)
    if a.list:
        print("%-30s %-11s %-10s %10s %6s %6s %6s" %
              ("ID", "CATEGORY", "TOOLING", "TOTAL$", "BUILD", "PROG", "MOTORS"))
        for m in catalog["mechanisms"]:
            print("%-30s %-11s %-10s %10.2f %6.0f %6.0f %6d" %
                  (m["id"], m["category"], m["tooling_floor"][:10], m["total_cost_usd"],
                   m["build_hours"], m["programming_hours"], m["motors_required"]))
        return 0
    if not a.input:
        ap.error("input yaml is required (or use --list)")

    capacity = load_yaml(a.capacity)
    spec = load_yaml(a.input)
    requests = resolve_requests(spec, catalog)
    r = build(requests, catalog, capacity)
    gates = gate_checks(r, capacity)
    geo = geometry_check(r, spec)
    gates.append(geometry_gate(geo))

    print(render_markdown(r, gates, spec, capacity, geo) if a.markdown
          else render_text(r, gates, spec, capacity, geo))
    if a.csv:
        write_csv(r, a.csv)
        sys.stderr.write("wrote CSV: %s\n" % a.csv)
    return 0 if all(g["pass"] for g in gates) else 1


if __name__ == "__main__":
    sys.exit(main())
