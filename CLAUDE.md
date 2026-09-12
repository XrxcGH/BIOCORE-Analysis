# BIOCORE Analysis — standing instructions

FRC **BIOCORE presented by Haas** (2027 game, FIRST CANOPY season). **Kickoff: January 9, 2027, 12:00 p.m. ET.**

## ⚡ KICKOFF-DAY AUTORUN — the one thing this project exists for

**TRIGGER.** A new `*GameManual*.pdf` or `*BIOCORE*.pdf` appears in this folder or in
`manuals/2026-27_BIOCORE/`, **and** the user points you at it (*"run kickoff"*, *"the manual is up"*,
a bare path). A file named `NOT-BIOCORE_*` is a rehearsal artifact and is **never** a trigger.

**When triggered, execute all five steps below without stopping to ask.** The user's single step is
supplying the manual. Do not ask which analyses to run, do not ask permission between phases, do not
summarise a plan and wait. Run it. Only stop early if a command hard-fails twice.

**`review/<dir>` means: the path written in `review/LATEST`.** Phase 1 writes that file. Every later
step reads it. Never guess "the newest directory" and never rely on scrollback.

---

### Step 1 — Mechanical extraction

```bash
bash tools/RUN-KICKOFF.sh <path-to-manual.pdf> V1
```

Creates `review/V1_<stamp>/` with `BRIEFING_PACK.md` and three schema stubs, and writes that path to
`review/LATEST`. If the manual is not downloaded yet, get it first:
`bash tools/probe-2027-manual.sh --download`. **If the probe fails, do not stall** — ask the user for
a direct URL or a local file and continue; it is the only network-dependent step in the autorun.

**On a fresh clone, do a one-time setup before the first run:** `bash tools/rebuild-corpus.sh --fetch`,
then `bash tools/rebuild-corpus.sh`. FIRST's manuals and the text extracted from them are not tracked
in the repository, and the ingest diffs against the 2026 REBUILT manual (the `BASELINE` default in
`tools/ingest-manual.sh`), which stops the run when that file is missing. See `README.md`, "What is
not in this repository".

### Step 2 — Read

1. `review/<dir>/BRIEFING_PACK.md` — **the whole thing.** Game-specific rules (isolated by FIRST's
   headline colour), added/removed rules vs. the 2026 REBUILT baseline, new glossary nouns, undefined
   ALL-CAPS, every `Violation:` clause, scored-when evidence, ambiguity tripwires.
   *If the rule/glossary diff reads `added=0 removed=0 changed=0`, you are running against the
   baseline itself — a rehearsal, not kickoff. Say so and do not present those sections as findings.*
2. The manual PDF — game overview, scoring, and the game rules (G). Roughly 60 pages; budget 20–35 min.
3. **The R4xx bumper block, plus R1xx perimeter and extension — and read it BEFORE any CAD.**
   Bumper geometry constrains the frame perimeter, not the other way round: the bumper zone height,
   corner coverage, backing thickness and the weight-with-bumpers limit set the frame dimensions that
   every later drawing inherits. Read these after the chassis is drawn and you redraw the chassis.
   Pull the block with the rule inventory, diff it against REBUILT, and build a **dimensioned bumper
   drawing on day 1**; anything the text does not resolve exactly becomes an axis-(b) Q&A question in
   §8. Rationale and counts: `reference/QA-AMBIGUITY-HOTSPOTS.md` §2.1,
   `reference/RULE-CHURN-WATCHLIST.md` §4 (Tier INSPECTION).

**Draft `REVIEW.md` §§1, 6, 7 and 8 now.** They need only the manual, and Step 4 is running compute
you are not waiting on. Do not leave all the writing to the end.

### Step 3 — Fill the three schemas *(this is ~70% of the day — 60–120 min)*

In `review/<dir>/`. **No `FILL_ME` may remain** — phase 2 refuses to run otherwise.

| File | What it needs | Where the answer is |
|---|---|---|
| `game_def.json` | phase lengths, every scoring action + value, endgame actions + time cost, RP thresholds | manual §6 scoring tables |
| `candidates.yaml` | every strategy the game permits, hand-scored A1–A13 / V2–V5 | enumerate per `STRATEGY-RANKING-SYSTEM.md` §2 (**§2.7's checklist is what produces the defense / feeder / minimal rows**); anchors in `reference/ACHIEVABILITY-RUBRIC.md` §2 |
| `bom_config.yaml` | the `target:` block (scoring aperture height + stand-off) **first**, then the mechanisms the design implies (`python tools/bom-builder.py --list`) | aperture: manual §5-ish field/scoring section, per `reference/03_ARCHETYPE_CORPUS.md` §2.4 item 4 · mechanisms: `reference/bom/06_MECHANISM_CATALOG.md` |

**Read the stub comments.** Every field that has ever been filled in wrong now carries its legal
token list, its units, and its source convention inline. In particular: `mfg_floor` accepts only
`hand | bandsaw+drill | 3dprint | router | CNC` (the `team_capacity.yaml` spellings are aliased);
anything else is a hard schema error, not a gate. `median_alliance_score` comes from
`research/predictive_tba/tba_matches_*.csv`, never from a guess.

**FIND THE SCORING APERTURE HEIGHT BEFORE YOU CHOOSE ANY MECHANISM.** Extract from the manual how
far off the carpet the scoring opening sits, and how far back a robot must stand to use it, and put
those two numbers in `bom_config.yaml` as

```yaml
target: {name: "HUB upper opening", aperture_height_in: 72, aperture_range_in: 0, source: "manual §5.4"}
```

`reference/03_ARCHETYPE_CORPUS.md` §2.4 item 4 — *"the scoring lip is the mechanism gate… in BIOCORE,
find this number first."* It is the reason a shooter out-ranks a lift, and a lift out-ranks a dump.
Choose mechanisms **after** you know it: `bom-builder.py` now runs a **GEOMETRY (REACH)** gate that
hard-fails when nothing in the config can deliver into that aperture and prints the shortfall in
inches. **Omitting `target:` now aborts phase 2 in preflight (exit 1) — it is not skippable**, and a
`target:` whose `aperture_height_in` is missing or `0` aborts too, because a zero aperture clears
every mechanism and reinstates the exact blindness the gate exists to end. Historically it printed a
**WARNING that feasibility was never checked**,
which is exactly the silence that put a 30-inch hopper dump against a 72-inch HUB lip in the 2026
rehearsal (`review/REHEARSAL_GRADE.md` §5). Each mechanism's envelope lives in the `delivery:` block
in `reference/bom/mechanism_catalog.yaml`; an envelope marked `evidence: UNVERIFIED` is a planning
figure, not a measurement — say so in the review.

**Write these files with the file-write tool, never with a shell heredoc.** Git Bash on Windows
breaks quoted heredocs on an apostrophe and truncates the file with no error.

**Enumerate strategies exhaustively before scoring** — by scoring action, field zone, match phase,
alliance role, RP path, and opponent denial. Include the ones a student never proposes: pure defense,
pure auto, feeder/support, deliberately-simple-and-flawless. A missing candidate cannot be ranked.
Start from `reference/examples/candidates_seed.yaml` if it exists and edit rather than author.

**Every candidate row must name its `corpus_archetype`** from `reference/03_ARCHETYPE_CORPUS.md` §2
and carry that archetype's verdict. The corpus is scored against five real seasons. A row that
finishes far from its archetype's verdict must be defended by name in §3 or corrected.

Score achievability **honestly against the anchors**, not aspirationally. The rubric assumes two
independent scorers who then reconcile; **you are one agent and cannot do that.** Compensate: score
against the anchor text, not from memory, and treat any score you assigned without opening the anchor
table as `[SPECULATION]`.

### Step 4 — Quantitative pass

#### 4a. Priors FIRST — before you fill in `game_def.json`

```bash
python tools/score-priors.py priors                 # cross-season kickoff priors + their spread
python tools/score-priors.py distributions 2026     # most recent season, in detail
python tools/score-priors.py endgame-check 2026     # was the endgame load-bearing? (2026: no)
```

**Do this before writing a single constant into `game_def.json`.** The 2026 rehearsal invented
`median_alliance_score = 120` when `research/predictive_tba/tba_matches_2026.csv` said **147.0
median / 182.7 mean** across 30,352 alliance-scores in this repo, and was graded **D**:

> *"A cycle model that is never checked against a season of results is a rhetoric generator."*

**The kickoff constraint, stated plainly:** on **2027-01-09 there is no BIOCORE outcome data** and
Week 1 is ~8 weeks away. You therefore **cannot** validate against this season. What you can do is
**derive priors from 2023–2026, label them as priors, and schedule the re-run.** Never present a
prior as a measurement.

What the priors currently say (re-run to confirm; do not quote from memory):

| Prior | 4-season range | Strength |
|---|---|---|
| Median alliance score | **50 → 147** (2024 → 2026) | **WEAK**, spread = 103 % of mean → report a RANGE |
| AUTO share of score | **20.1 % → 36.9 %** | WEAK, but **never negligible in 4 seasons** |
| Endgame share of score | **1.1 % → 29.0 %** (a 27× swing) | **WORTHLESS as a prior.** Endgame value is a per-game question; resolve it at Week 1, never at kickoff |

#### 4b. Every constant carries its source

Give every number in `game_def.json` a `_source` sibling (`per_cycle_source`, `time_s_source`, …)
naming **either a manual section or a `research/predictive_tba/` column**. `cycle-model.py` now
echoes every constant beside its source and prints **`[UNSOURCED]`** next to any that lacks one, with
a count. An unsourced constant is a guess; that is allowed, but it must be **visible in the review**,
not laundered into a decimal place. Reproduce the CONSTANTS block in `REVIEW.md` §2.

#### 4c. Run the model as a RANGE at kickoff

```bash
bash tools/RUN-KICKOFF.sh --phase2                  # uses review/LATEST
python tools/cycle-model.py --game review/<dir>/game_def.json --range
```

Runs the cycle/EV model, the cycle-time sweep, strategy ranking (quadrant + tier + binding
constraint), and the costed BOM with gate checks and order-by dates.

**At kickoff, publish `--range` output, not the point estimate.** All three priors are WEAK, so a
single number is false precision. `--range` reports low/likely/high, and cross-checks a 3-robot
alliance proxy against the 4-season prior band. **If it prints `!! PRIOR CONFLICT`, stop** — a
non-overlapping band means a constant is wrong (check `per_cycle` and cycle time first). The built-in
REBUILT example fires this deliberately: it implies **4.0×** the 4-season median, which is exactly the
"roughly 2× hot" error the grade identified.

**Before you believe any of it:** the BOM checks dollars, hours, workstreams, motors **and now
reach**. The GEOMETRY (REACH) gate needs the `target:` block from Step 3, and **phase 2 now refuses
to start without it (exit 1)** — so an unchecked design can no longer reach the results. If you ever
see `*** NOT CHECKED ***` or the geometric-feasibility WARNING banner, treat it as a defect in the
tooling and stop; do not proceed on an unchecked design. And sanity-check the cycle model against `research/predictive_tba/` outcome
data: a scoring channel worth ~1% of a real match score must not end up as your headline
recommendation.

#### 4d. The re-run checkpoint — MANDATORY, not optional

Kickoff output has an **expiry date**. Book it now and write it into `REVIEW.md` §2:

> **After Week 1 of the 2027 season** (checkpoint **C6** in `STRATEGY-RANKING-SYSTEM.md` §7.1,
> ≈ D+42): add 2027 to `SEASONS` / `AUTO_COL` / `END_COL` in `tools/score-priors.py`, then run
> `distributions 2027` and `endgame-check 2027`. **Replace every prior with the measured 2027
> value, re-run `cycle-model.py` without `--range`, and re-rank — before the first pick list.**

Nothing built on priors survives contact with Week 1 unexamined. `endgame-check` is the specific
check the rehearsal skipped; run it on 2027 before any endgame mechanism reaches BUILD THIS.

### Step 5 — Write the review

Write `review/<dir>/REVIEW.md` and tell the user it exists. Required sections:

1. **Game summary** — phases, every scoring action and value, zones, field elements, ranking formula, endgame.
2. **Scoring strategy** — from `results/cycle_model.txt` + `cycle_sweep.txt`: points/cycle, break-even
   for every endgame option, what one second of cycle time is worth per match and per 12-match
   schedule, RP feasibility solo vs. alliance. **State every invented constant** (`per_cycle`, each
   `time_s`, `median_alliance_score`) and its source beside the number it drives.
3. **Ranked strategies** — the quadrant matrix from `results/strategy_ranking.txt`. For each:
   quadrant, tier, **binding constraint**, corpus archetype, and a plain-English "what this means for
   a 15-student team". **The quadrant is the decision; the tier is only a delivery-risk badge, and the
   two can contradict each other** — see the operating rule at the top of
   `reference/ACHIEVABILITY-RUBRIC.md`, and reproduce the tool's QUADRANT/TIER DISAGREEMENTS block.
   Never print a tier without its quadrant beside it.
4. **Recommended design + BOM** — from `results/bom.md`: cost, hours, gate status, **earliest order-by
   date**, and one sentence on how the design reaches the scoring aperture.
5. **Two awards for each strategy in the top tier** (not all of them — pairings for every row is not a
   useful artifact), plus one team-level row. Via `reference/awards/AWARD-ALIGNMENT.md`; use only
   names verified in `reference/awards/00_AWARD_LIST_VERIFIED.md` (**Dean's List is retired → FIRST
   Leadership Award**; Chairman's → FIRST Impact). **Cross-check any availability or awards-per-event
   figure against `reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`** — the VERIFIED file's
   availability column sums some awards with their Finalist/Semi-Finalist variants and overstates
   them (FIRST Leadership: 10 events, not 192). Include the materials checklist and who builds it.
   Run `bash reference/awards/kickoff_award_check.sh` (exit 0 == award names current) before writing
   this section.
6. **Loopholes and edge cases** — the highest-value section. It has **TWO MANDATORY AXES and BOTH
   must be covered.** A hunt that covers only one is incomplete: send it back, do not publish it.

   **Axis (a) — STRATEGIC ambiguity.** *Can I score this, and is the penalty cheaper than the points?*
   Families: scoring validity and SCORING ELEMENT delivery · zones and protected zones · robot-to-robot
   contact and defense · AUTO interaction · timing, counts and thresholds. Mostly **G4xx**, plus the
   G2xx conduct rules.
   Required checklist — carry each slot forward by number and say what it maps to in BIOCORE, or say
   plainly that it has no analogue: **G403** (AUTO interaction) · **G413** (expansion limits) ·
   **G415** (stay out of other ROBOTS) · **G416** (this isn't combat robotics) · **G418** (PIN count) ·
   **G419** (collusion) · **G420** (protected zone) · **G425** (SCORING ELEMENT delivery) ·
   **G427** (storage limit) · **G210** · **G211** (egregious/exceptional).

   **Axis (b) — INSPECTION / CONSTRUCTION ambiguity.** *Will this robot be allowed on the field at
   all?* Families: **bumpers (R4xx)** · **robot perimeter (R1xx)** · extension and volume limits ·
   weight · safety.
   Required checklist — same treatment: **R401** (bumpers almost all around) · **R402** (bumper
   construction) · **R404** (bumpers must be soft) · **R405** (bumpers interact with bumpers) ·
   **R408** (weight limit with bumpers) · **R409** (bumpers passive) · **R101** (perimeter must be
   fixed) · **R105** / **R106** (extension) · **R107**.

   **Why axis (b) is not optional — state this to the team in these terms:** a strategic misread costs
   you *points in one match*; an inspection failure costs you *matches*. The robot does not play until
   it is fixed, and it is fixed in the pits with the schedule running. It is also, on the record, the
   single largest cluster of genuine confusion in FRC: the six bumper rules drew **116 Q&A questions
   across 2024–2026**, more than any other topic by a wide margin, and R402 is still *rising*
   (3 → 9 → 16). In 2026, six inspection-cluster rules — R402 (16), R401 (12), R404 (9), R405 (8),
   R101 (6), G425 (6) — carried **57 questions, 19.5% of the entire season's Q&A**, and the rehearsal
   hunt named **none of them**. It scored A− purely on axis (a). One axis is not a pass.

   Work **both** axes from:
   - `BRIEFING_PACK.md` **undefined ALL-CAPS** — terms used in scoring rules but never defined
   - **game-specific rules with no REBUILT analogue** — historically where the season's exploits live
   - `reference/RULE-CHURN-WATCHLIST.md` — Tier 1 (G413, R106, G403, G420, G427), Tier 2 (the
     never-stable G415, G416, G211, R402, G409, G210, G425), and **§4 Tier INSPECTION** (the R4xx/R1xx
     block) — Tier INSPECTION is axis (b)'s spine
   - `reference/QA-AMBIGUITY-HOTSPOTS.md` — **read §2.1 (bumpers, the #1 ambiguity zone) before §2.2**
   - **the penalty-arbitrage audit**: for each rule, is the penalty cheaper than the points gained?

   **Minimum filing: at least 2 of the week-1 Q&A questions in §8 must come from axis (b).** One is
   not enough — the 2026 blind spot was six rules deep, not one.
7. **Pitfalls** — what this team specifically will get wrong.
8. **Q&A questions to file in week 1** — ranked by leverage. Q&A answers are binding and early ones
   get answered fastest. Four hard rules on this list:
   - **Every question must name the G/R rule ID it attaches to.** Not a section, not a concept — a
     rule ID. A question that cannot name its rule is not a question, it is a hunch: find the rule or
     cut it. This is what makes the list falsifiable against the Q&A record afterwards.
   - **Questions attached to historically hot rules outrank speculative ones.** Rank by the evidence
     behind the *rule*, not by the size of the prize you imagine behind the *exploit*. A question on a
     rule with prior Q&A volume (`reference/QA-AMBIGUITY-HOTSPOTS.md` §1) or prior Team Update churn
     (`reference/RULE-CHURN-WATCHLIST.md`) outranks any exploit whose value comes from nothing but
     your own arithmetic. In the 2026 rehearsal the **#1 slot went to a speculative timing exploit
     attached to no rule at all** and valued at "~110–140 points per season" from an invented
     constant, while **R402 — 16 real questions, rank 2 for the season — went unmentioned.** That
     ordering was exactly backwards.
   - **At least 2 questions must come from §6 axis (b)** — bumpers, perimeter, extension.
   - Tag any question whose value rests on your own estimate `[SPECULATION]` and rank it **below**
     every evidence-backed question. Show the rule's prior question count beside each entry so the
     ordering can be checked.
9. **Scored betting sheet** — grade **every prediction** in `research/04_biocore_community_intel.md`
   against the real manual (the count changes; do not assume it), and say what the misses imply.

Then: **name the endgame structure**, because that fixes the free-data shape for scouting
(`reference/SCOUTING-PLAN.md` — FMS publishes `Avg <endgame>` every season, 4/4).

---

## Hard facts — do not get these wrong

- **BIOCORE is FRC. BIOBUZZ is FTC.** "Pollen", "StarterBots", "Skill Builders" are **FTC BIOBUZZ**,
  never BIOCORE. September 12, 2026 was the *FTC* kickoff. See `research/00_PREMISE_CORRECTION.md`.
- **2027 replaces the roboRIO with Systemcore** — biggest control-system change since the cRIO.
  Never recommend investing training time in the roboRIO stack for 2027.
- **FIRST permits AI** with attribution, and judges may not rank a team lower for it.
  `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` is the authority.
- **Team = ~15 students**, limited budget. `reference/team_capacity.yaml` is the authority for
  **hours, headcount, and budget** — and for nothing else. It is **not** the authority for gate
  vocabulary or scoring: `reference/achievability_rubric.yaml` is what `tools/score-strategy.py`
  actually reads, and the two files spell the manufacturing floor differently on purpose.
- **Key dates:** Kit & Kickoff selection opens **2026-09-24**, Pre-Kickoff Virtual Kit Release
  **2026-11-12**, selection closes **2026-11-17**, BOM order-by **2026-11-21**, kickoff **2027-01-09**.

## Evidence tags — use them on every factual claim

`[VERIFIED]` primary source or extracted from a local manual with rule + page ·
`[COMPUTED]` derived by a script here, reproducible · `[COMMUNITY]` named credible non-FIRST source ·
`[INFERENCE]` chained off verified facts · `[SPECULATION]` pattern-matching · `UNVERIFIED`.

**Everything in this project is a prior, not a fact about BIOCORE. When the manual contradicts a file
here, the manual wins and the file gets corrected.**

## Navigation

`INDEX.md` is the full map. `README.md` is the entry point. `KICKOFF_PLAYBOOK.md` has the deep
phase-by-phase method behind the autorun; `STRATEGY-RANKING-SYSTEM.md` has the ranking pipeline.
`review/REHEARSAL_FINDINGS.md` + `REHEARSAL_GRADE.md` are the worked dry run — read them if a
pipeline output looks odd.

## Working style here

- Prefer local data: 242 manuals (1992–2026), 11 seasons of rule inventories, Q&A heat maps, Team
  Update churn, TBA CSVs 2022–2026. Most questions are answerable from disk.
- Never invent a part number, price, URL, team number, or award name. Mark `UNVERIFIED` instead.
- Windows 11 + Git Bash. Prefix python with `PYTHONIOENCODING=utf-8` when printing manual text.
  **Write YAML/JSON with the file-write tool, never a shell heredoc** — an apostrophe in the content
  silently truncates the file.
