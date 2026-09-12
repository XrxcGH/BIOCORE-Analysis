# FRC 2026 Award List — derived empirically from actual event results

> **[AUDIT 2026-08-22] SUPERSEDED AS THE AUTHORITY — and see the availability correction.**
> This file is a *descriptive* record of what TBA shows judges handed out in 2026. The authoritative
> award list — official names, sponsors, published criteria, eligibility, 2027 deadlines,
> advancement, **and availability** — is
> [`00_AWARD_LIST_VERIFIED.md`](00_AWARD_LIST_VERIFIED.md) §2.1a, with companion
> [`awards.yaml`](awards.yaml). Cite that file, not this one. `Judges' Award` is printed by FIRST as
> **Judges Award** on the authority page.
>
> **What changed on 2026-08-22, and which file was wrong.** The earlier version of this banner said
> the verified file "aggregates Engineering Inspiration / FIRST Impact / FIRST Leadership per-event
> counts across Regional + District + District Championship tiers." That aggregation was a **defect,
> not a convention**, and the verified file has now been corrected: it publishes **distinct events
> per exact award name**, never an award summed with its Finalist or Semi-Finalist tier. The two
> files now agree.
>
> **Read every "Times given" number below as a ROW COUNT, not an event count.** They are not the same
> thing for any multi-recipient award. Corrected event counts from
> `python tools/award_availability.py`:
>
> | this file prints (rows) | distinct events | per event |
> |---|---:|---:|
> | `FIRST Leadership Award` 10 | **1** (`2026cmptx`) | 10.00 |
> | `FIRST Leadership Award Finalist` 172 | **71** | 2.42 |
> | `District Championship FIRST Leadership Award Semi-Finalist` 218 | **120** | 1.82 |
> | `District Championship FIRST Impact Award` 30 | **15** | 2.00 |
> | `District Championship Engineering Inspiration Award sponsored by SpaceX` 22 | **15** | 1.47 |
> | `Woodie Flowers Finalist Award` 79 | **71** | 1.11 |
>
> Every other row below is 1 row = 1 event. **Never add these rows together.** 10 + 172 + 218 = 400
> over 192 events = "2.08 per event" is the retracted figure; it overstated the FIRST Leadership
> Award's own availability by 192x.

**Purpose:** settle what awards FRC *actually gave out* in 2026, so the BIOCORE award-alignment system
targets real awards under their real names. Derived from The Blue Alliance award records, not from a
marketing page — this is what judges actually handed out at 208+ events.

**Companion file:** `research/awards_tba/tba_awards_2026.csv` (4,993 award rows, 2026 season).

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Present in TBA 2026 award records at in-season event volume |
| **[H]** HISTORICAL-PATTERN | Seen in prior seasons; not confirmed for 2027 |
| **[S]** SPECULATION | Inference. Flagged as such |

**Method.** `tools/tba_award_scrape.py` pulled every award from every 2026 event. An award given
**~200+ times** is offered at essentially every event and is part of the standard slate. Awards with
counts of 1–2 are **offseason events using custom names** — noise, not the official list.

---

## 1. The headline change: Dean's List → **FIRST Leadership Award** [C]

The 2023→2026 diff is unambiguous:

- **Gone in 2026:** `FIRST Dean's List Award`, `FIRST Dean's List Finalist Award`,
  `District Championship Dean's List Semi-Finalist`
- **New in 2026:** `FIRST Leadership Award` (10 rows / **1 event**), `FIRST Leadership Award
  Finalist` (172 rows / **71 events**), `District Championship FIRST Leadership Award Semi-Finalist`
  (218 rows / **120 events**) — three separate awards. **Do not sum them.**

**Any document referring to "Dean's List" for the BIOCORE season is out of date.**
The individual-student award is now the **FIRST Leadership Award**.

Also renamed/unsponsored since 2023: `Chairman's Award` → **FIRST Impact Award**;
`Industrial Design Award sponsored by General Motors` → **Industrial Design Award** (no sponsor in 2026).

## 2. The standard event slate [C]

Given at essentially every 2026 event. **These are the realistic targets.**

| Award (exact 2026 name) | Times given | Type |
|---|---:|---|
| Gracious Professionalism Award | 211 | Culture |
| Industrial Design Award | 210 | **Robot/design** |
| Team Spirit Award | 210 | Culture |
| Judges' Award | 209 | Discretionary |
| Quality Award | 209 | **Robot/design** |
| Autonomous Award sponsored by Google.org | 208 | **Robot/software** |
| Creativity Award sponsored by Rockwell Automation | 208 | **Robot/design** |
| Excellence in Engineering Award sponsored by Littelfuse | 208 | **Robot/process** |
| Imagery Award in honor of Jack Kamen | 208 | Robot/brand |
| Innovation in Control Award sponsored by nVent | 208 | **Robot/software** |
| Team Sustainability Award sponsored by Dow | 208 | Business |
| Rising All-Star Award | 204 | Rookie-adjacent |
| Rookie All Star Award | 133 | Rookie only |

## 3. The advancing / prestige awards [C]

*Times given = **rows**. The `Distinct events` column is the availability figure; use it, not the row count.*

| Award | Times given (rows) | Distinct events |
|---|---:|---:|
| District Championship FIRST Leadership Award Semi-Finalist | 218 | **120** |
| FIRST Leadership Award Finalist | 172 | **71** |
| District Engineering Inspiration Award sponsored by SpaceX | 123 | **123** |
| District FIRST Impact Award | 122 | **122** |
| Woodie Flowers Finalist Award | 79 | **71** |
| Regional FIRST Impact Award | 56 | **56** |
| Regional Engineering Inspiration Award sponsored by SpaceX | 56 | **56** |
| District Championship FIRST Impact Award | 30 | **15** |
| District Championship Engineering Inspiration Award sponsored by SpaceX | 22 | **15** |

Engineering Inspiration is **sponsored by SpaceX** as of 2026 [C].

## 4. The seven robot-linkable awards — the ones a design choice can aim at

These are the awards where **the robot itself is the evidence**, so they are the ones the
design→award pairing system should key on:

1. **Industrial Design Award** — coherent, manufacturable, visually resolved machine
2. **Quality Award** — robustness, build quality, reliability
3. **Excellence in Engineering Award** (Littelfuse) — the engineering *process*
4. **Creativity Award** (Rockwell) — a genuinely novel mechanism or approach
5. **Innovation in Control Award** (nVent) — demonstrable, explainable control + data
6. **Autonomous Award** (Google.org) — autonomous performance
7. **Imagery Award** (Jack Kamen) — robot + brand visual integration

For a ~15-student team these are the realistic robot-award targets; Impact and Engineering
Inspiration are separate, business/outreach-driven tracks that a robot design does not influence.

## 5. Carry-forward risk for 2027 [S]

Award names have churned **every single season** 2023→2024→2025→2026. Treat this list as the
**2026 baseline**, not a 2027 guarantee. **Re-run `tools/tba_award_scrape.py` after the first 2027
events** and diff before finalizing any award materials.

## Files written by this pass
- `reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md` (this file)

## Known limitations
- TBA award *names* are event-reported; offseason events invent their own (the count-1 entries).
- Counts reflect events indexed by TBA, so a handful of unindexed events may be missing.
- This is **descriptive** (what was given) not **prescriptive** (published criteria). Criteria must
  still come from FIRST's official award guides.
