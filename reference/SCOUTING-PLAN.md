# Scouting Plan — scout only what FMS does not already publish

**Purpose:** a ~15-student team cannot run a 12-scout operation. It does not need to. FIRST already
publishes a per-team scoring breakdown for every team at every event. This file identifies exactly
which data is free, forecasts the BIOCORE version of it, and defines a scouting schema that collects
**only the gaps** — so scouting labour goes where it actually changes a draft decision.

**Companion file:** `tools/scouting-plan.py` (tested against 2023–2026 TBA data in `research/predictive_tba/`).

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Computed from TBA event data in this repo; reproducible |
| **[H]** HISTORICAL-PATTERN | Holds 4/4 seasons 2023–2026; not stated for BIOCORE |
| **[S]** SPECULATION | Inference. Flagged as such |

---

## §0 60-second workflow

```bash
# Run from the repository root.

python tools/scouting-plan.py free                       # what you get for free + BIOCORE forecast
python tools/scouting-plan.py schema                     # the 22 gap fields to actually collect
python tools/scouting-plan.py schema --json > scouting_schema.json   # feed your app builder
python tools/scouting-plan.py picklist 2026 --event 2026mndu --top 25
```

## 1. What FMS publishes for free [C]

The event rankings table, mirrored by The Blue Alliance, is identical in shape every season:

| Season | Component columns published | Events with this exact set |
|---|---|---|
| 2023 | Ranking Score · Avg Match · **Avg Auto** · **Avg Charge Station** | 179 / 185 |
| 2024 | Ranking Score · **Avg Coop** · Avg Match · Avg Auto · **Avg Stage** | 185 / 190 |
| 2025 | Ranking Score · **Avg Coop** · Avg Match · Avg Auto · **Avg Barge** | 198 / 203 |
| 2026 | Ranking Score · Avg Match · **Avg Auto Fuel** · **Avg Tower** | 208 / 215 |

Plus `Record (W-L-T)`, `DQ`, `Played`, `Total Ranking Points` in every season.

**The invariant [H]:** *Ranking Score · Avg Match · Avg Auto · Avg &lt;endgame structure&gt; · Record · DQ · Played · Total RP.*
Four seasons out of four. FIRST names one column after the season's endgame structure —
Charge Station, Stage, Barge, Tower.

### BIOCORE forecast [S]

```
Rank | Team | Ranking Score | Avg Match | Avg Auto | Avg <BIOCORE endgame> | Record (W-L-T) | DQ | Played | Total RP
```

On kickoff day, name the endgame structure from the manual and you already know the shape of the free
data — **before a single scout is trained.** Confirm at week 1 by re-running `scouting-plan.py free`.

## 2. Why this matters more than it sounds

Free data already answers *"who scores?"*, *"who autos?"*, *"who does the endgame?"* and
*"who gets disqualified?"* — the four questions most rookie scouting systems are built to answer.

A worked example from `2026mndu` [C]:

| Team | Avg Match | Avg Tower |
|---|--:|--:|
| 3100 | **205.7** | 2.3 |
| 3267 | 143.1 | **23.6** |
| 7797 | 140.9 | **24.6** |

3100 outscores 3267 by 63 points a match, but 3267 and 7797 are the **climb specialists** — visible
instantly, for free, with zero scouts. If your robot cannot climb, 3267 is a more complementary
first pick than the higher-scoring 3100. That inference cost nothing.

**DQ is also free** and nobody uses it: 12.5% of teams at `2026tuis` had at least one DQ. That is a
rules-risk signal on every potential partner, already published.

## 3. The gap schema — 22 fields [C]

What FMS **cannot** tell you, and therefore what your scouts exist to capture.

### Match scouting (13 fields)

| Field | Type | Why it cannot be had for free |
|---|---|---|
| `breakdown` | enum none/partial/dead | FMS publishes points scored, never whether the robot stopped working |
| `breakdown_cause` | text | Drivetrain vs mechanism vs electrical vs comms changes pick value entirely |
| `defense_played_s` | seconds | A low Avg Match may mean a great defender, not a bad scorer |
| `defense_quality` | 1–5 | Not published in any form. The most under-scouted dimension in FRC |
| `defended_against` | bool | Without it you misread a good robot as weak |
| `cycle_count` | int | FMS gives the total, not the rate |
| `intake_misses` | int | Acquisition reliability; predicts performance under pressure |
| `endgame_attempted` | bool | FMS shows success only — attempt-vs-success is the reliability signal |
| `endgame_time_s` | seconds | Feeds the break-even in `tools/cycle-model.py` |
| `driver_skill` | 1–5 | Best predictor of playoff performance; entirely unpublished |
| `starting_position` | enum | Auto compatibility for alliance planning |
| `auto_path_note` | text | Two teams with identical Avg Auto may have incompatible paths |
| `notes` | text | The thing no field anticipated |

### Pit scouting (9 fields)

`drivetrain` · `weight_lb` · `mechanism_count` · `can_score_where` · `climb_levels` ·
`spare_parts_depth` · `programming_language` · `vision_used` · `known_weaknesses`

> `spare_parts_depth` predicts whether a breakdown ends their event — a strong playoff signal.
> `known_weaknesses` is the highest information-per-minute question in the pits. **Teams will tell
> you. Almost nobody asks.**

## 4. Staffing consequence

22 fields, not 60. A **6-scout rotation** covers the match set; pit scouting is **one person for one
morning**. For a 15-student team that is the difference between scouting being affordable and
scouting cannibalising the drive team.

Reclaimed hours should go to drive practice — at an 8-second cycle, one second of cycle time is worth
**9.7 points/match, 117 points across a 12-match schedule** (`tools/cycle-model.py`). Scouting labour
spent re-deriving `Avg Match` buys nothing; the same hours in drive practice buy points.

## 5. Building the pick list

`picklist` fuses free data into a ranked starting point, reporting the component columns present that
season, plus mean/median/max and the DQ rate. It deliberately stops short of a final ranking:

> Rank order from free data reflects **scoring**, not reliability, defense, or driver skill.
> Fuse it with gap-scouting before drafting.

## Files written by this pass
- `reference/SCOUTING-PLAN.md` (this file)
- `tools/scouting-plan.py` — `free` · `schema` · `picklist`; tested on 2023–2026 TBA data

## Known limitations
- The free-data shape is **[H] from 4 seasons**, not a FIRST commitment. Re-verify at week 1 of BIOCORE.
- `Avg Match` semantics vary; some events report alliance-level rather than team-contribution figures
  (one 2026 event shows a 365.0 outlier against a 102.0 mean). Sanity-check outliers before trusting them.
- The picklist is a *starting point*, not a ranking — it has no reliability or defense input by design.
- TBA data here is a snapshot; refresh with `tools/tba_predictive_scrape.py` before the 2027 season.
