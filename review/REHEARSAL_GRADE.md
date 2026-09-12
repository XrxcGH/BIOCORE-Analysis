# REHEARSAL GRADE — the pipeline's REBUILT advice vs. what actually happened

**Graded:** 2026-08-22 · **Subject:** `review/V1_20260823T014011Z/REVIEW.md` and `review/REHEARSAL_FINDINGS.md`
**Ground truth used:** `research/predictive_tba/tba_rankings_2026.csv` (8,160 team-events),
`tba_alliances_2026.csv` (5,245 picked slots, 664 winner slots), `tba_matches_2026.csv` (30,352
alliance-scores), `research/teamupdate_analysis/2026_tu_churn.tsv` (104 amendments),
`research/rule_inventories/qa_heat_2026.tsv` (293 questions / 91 rules),
`reference/03_ARCHETYPE_CORPUS.md` §2.

| § | Section | Grade |
|---|---|---|
| 1 | Scoring analysis / cycle model | **D** |
| 2 | Strategy ranking | **D** |
| 3 | Loophole hunt | **A−** |
| 4 | Awards | **B−** |
| 5 | BOM | **C−** (one fatal design error) |

The rehearsal's own `REHEARSAL_FINDINGS.md` graded the *plumbing* and graded it honestly. Nobody
graded the *answer*. The answer was wrong in the one place it matters most.

---

## 1. SCORING ANALYSIS — **D**

### What it claimed

> "The TRAVERSAL arithmetic is the whole strategic answer... 2 ROBOTS × AUTO L1 (15) + 2 × TELEOP L1
> (10) = **exactly 50**, using only LEVEL 1 climbs... **Build for that.**" (REVIEW §2.5)

Break-even table (§2.3): L1 net **+2**, L2 net **+5**, L3 net **+5**, AUTO L1 **+15** — "the best
climb in the game," "the highest-value-per-hour action in REBUILT for a small team."

### What actually happened

| Measure | Value |
|---|---:|
| Mean alliance **Avg Match** (rankings) | **178.75** |
| Mean alliance **Avg Tower** | **1.92** |
| TOWER as share of match score | **1.1 %** |
| Median team-event Avg Tower | **0.91** |
| p75 / p90 / p99 Avg Tower | 2.50 / 4.58 / **16.67** |
| Team-events with Avg Tower = 0 | **2,973 / 8,160 (36.4 %)** |
| 2025 comparator: Avg Barge / Avg Match | 10.48 / 96.04 = **10.9 %** |

**TOWER points were one percent of the game.** The 2025 endgame was ten times more load-bearing. The
"cheapest legal path to 50 TRAVERSAL" required an alliance to average 50 TOWER points; the 99th
percentile *team* averaged 16.67 and the mean alliance averaged 1.92. TRAVERSAL was, in practice,
close to unearnable — and the review made it the spine of the entire recommendation.

**Climbing predicted nothing.**

- `corr(Avg Tower, Avg Match) = **0.003**` — statistically indistinguishable from zero.
- `corr(Avg Tower, picked) = 0.045` vs `corr(Avg Match, picked) = **0.139**` and
  `corr(Avg Auto Fuel, picked) = **0.100**`.
- Event **winners** averaged Avg Tower **2.0** — the league average of 1.9. Winning alliances did not
  climb more than anyone else.
- Teams with Avg Tower ≥ 5 (n = 768, top ~9 %) averaged **177.4** match points — dead-on the league
  mean 178.7. Climbers were not better robots; they were average robots that also climbed.
- Teams with **zero** tower but above-median score were picked **72.5 %** of the time — *more* often
  than the climbers (71.1 %).

### The model inputs were guesses and they were off

| Input | Review | Reality |
|---|---|---|
| `per_cycle` / cycle time | 8 FUEL / 8.0 s → **1 pt/s** | Corpus R2 (fixed-zone shooter): 8–15 FUEL per trip, 5–6 trips in 110 s ≈ **0.5 pt/s**; R1: 25–40/trip |
| `median_alliance_score` | **120** ("a pure guess") | **147.0** median, 182.7 mean (n = 30,352) |
| Solo corrected total | 93 pts | Individual COPR median **38.5**, p90 153.4 |

### Credit where due

- The **HUB duty-cycle catch is genuinely excellent** and independently confirmed: the review's 90 s
  of 140 s TELEOP matches the corpus's 110 s of 160 s full-match derivation exactly. Refusing to
  quote the raw 143 was right.
- "**L3 is not worth more than L2**" was right, and reality was harsher than the review's version —
  neither was worth building.
- "REBUILT is cycle-bound; no column is flat" was correct and the review then ignored its own finding.

### Verdict

The arithmetic inside the model is sound. The model was fed invented constants, was never validated
against the 8,160 rows of 2026 outcome data sitting in the same repo, and its output was used to
justify the one investment the data says returned nothing. **A cycle model that is never checked
against a season of results is a rhetoric generator.**

---

## 2. STRATEGY RANKING — **D**

The ranking is **inverted at both ends** relative to `03_ARCHETYPE_CORPUS.md` §2.3 — a file already
in the repo, already scored against 2026, and never consulted by the ranking.

| Corpus archetype | Corpus verdict (2026 REBUILT) | Pipeline row | Pipeline rank |
|---|---|---|---:|
| **R2** Fixed-Zone Bulk Shooter | "**the highest-value small-team play in REBUILT.** Same points as R1 at ⅓ the cost." **first/second-pick** | S2 Fixed-position FUEL scorer, T2 STRETCH | **10 / 14** |
| **R5** AUTO Specialist | "**captain-tier multiplier**... best pts-per-dollar in the corpus" | S3 AUTO-only, T2 STRETCH | **9 / 14** |
| **R6** Shift Defender | "**REBUILT is the strongest defense season in this corpus**"; 78 % of 2026 winners carried a below-median robot | S4 / S12, T2 STRETCH | 6, 7 |
| **R4** TOWER Climber | second-pick, TRAVERSAL-gating | **S10 — the only BUILD THIS row** | **4 (top tier)** |

The two archetypes the corpus calls the best small-team plays in this specific game were ranked
**9th and 10th**. The archetype the outcome data shows was worth ~1 % of a match score was the sole
occupant of BUILD THIS.

**Auto was the discriminator the ranking demoted.** Avg Auto Fuel: unpicked **33.3**, picked
**37.5**, event winners **48.3**. Among below-median scorers, top-quartile Auto Fuel was picked
59.1 % vs 47.7 % for the bottom quartile — a wider spread than tower's 57.5 % vs 48.8 %.

**Where TRAP / DELETE was called, was it right?**

- **S13 do-everything (TRAP, ACH 4.9)** — correct. Corpus R1 at full spec: "**NO**... where 15-student
  teams lose the season."
- **S9 L3 telescoping (TRAP)** — correct, and for a better reason than given: 36 % of team-events
  never scored a single tower point.
- **S1 full-field volume cycler (DELETE)** — **defensible but the most consequential call in the
  document.** Corpus R1: "**event-winning** — top-COPR robots in 2026 are all FUEL-volume." Gating it
  on workstreams is right for 15 students; labelling it DELETE and then failing to route the team to
  R2 (the cheap version of the same idea) is how the ranking ended up with no scoring plan at all.
- **S11 ENERGIZED chaser (DELETE)** — the escalation logic (100 → 240 → 360) is real and the call is
  reasonable for a Week-1 district team.

**Right calls:** S5 feeder (corpus R3 = YES) and S6 minimal-flawless (R8 = YES) in the top three;
forcing defense onto the board at all. But R3's corpus verdict is "pick equity is weak **alone**;
**pair with R4**" — and the review's own #1 pick is a strategy the corpus says does not stand alone.

---

## 3. LOOPHOLE HUNT — **A−**

**This is the section that justifies the project.** It worked.

### Rule churn — what FIRST actually had to amend (104 amendments across 22 Team Updates)

| Rule | Amendments | Named in REVIEW? |
|---|---:|---|
| G416 | 6 | **YES** (×3, §6.2/6.4) |
| G211 | 5 | **YES** (×2, §6.4/6.5) |
| G415 | 5 | **YES** (×3) |
| R106 | 5 | **YES** (×3, §6.3) |
| G403 | 3 | **YES** (×3, §6.5) |
| G413 | 3 | **YES** (×6 — the most-cited rule in the document, and Q&A #4) |
| R105 | 3 | **YES** |
| R107 | 3 | **YES** |

**8 of the top 8. 100 % hit rate on the rules FIRST actually rewrote.** §6.3 predicted "G413, R106,
G403, G420, G427 — a 5-for-5 hit" and §6.4 predicted "G415, G416, G409, G211 — 4 for 4." Both
self-assessments check out against the churn file. The named-rule set covers **39.4 % of all 2026
amendments** from ~17 rules out of ~60 that churned at all.

### Q&A heat — what teams actually could not parse (293 questions)

Hit **5 of the top 7**: G416 (18), R106 (12), G211 (12), G415 (12), G413 (11). Coverage **36.5 % of
all questions** from ~17 named rules of 91.

**The miss, and it is a real one:** the entire bumper-construction cluster.

| Missed rule | Questions | Subject |
|---|---:|---|
| **R402** | **16 (rank 2)** | BUMPER construction |
| **R401** | **12 (rank 3)** | BUMPERS almost all around |
| R404 | 9 | BUMPERS must be soft |
| R405 | 8 | BUMPERS interact with BUMPERS |
| R101 | 6 | ROBOT PERIMETER must be fixed |
| G425 | 6 | SCORING ELEMENT delivery |

**57 questions — 19.5 % of the entire season's Q&A — from six rules the review named zero times.**
§6.4 is literally headed "Bumpers (R4xx) and contact (G41x)" and then discusses only the *contact*
half; not one R4xx rule ID appears anywhere in the document and not one of the eight filed Q&A
questions touches inspection or construction. The hunt was tuned for **strategic** ambiguity and
blind to **inspection** ambiguity — which is where the largest single cluster of real confusion was,
and which is the cluster that actually stops a robot from playing.

Also note: the review's **#1-ranked Q&A question** (the 3-second FUEL assessment tail, valued at
"~110–140 points per season") is not attached to any G/R rule and appears nowhere in the heat table.
It is unfalsifiable from the local record. The top slot went to a speculative exploit while R402 —
16 real questions — went unmentioned.

**Grade A−, not A**, purely for the bumper blind spot. The core claim of the project — that manual
churn and Q&A heat are predictable from priors on disk — is **validated**.

---

## 4. AWARDS — **B−**

Pairings are plausible and correctly category-aligned against
`reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`: Excellence in Engineering (Robot/process) +
Quality (Robot/design) for a mechanism-led strategy; Autonomous sponsored by Google.org +
Innovation in Control sponsored by nVent for the AUTO row; Gracious Professionalism + Team Spirit
(Culture) for the support rows. Sponsor names, the Dean's List → **FIRST Leadership Award** rename,
and the Industrial Design de-sponsoring are all correct. Deadlines (Impact 2027-02-11, Leadership
2027-02-04) are correctly surfaced as the only hard dates before a Week-1 event.

**One material error:**

> "FIRST Leadership Award is offered at **192 events** with a **2.08 awards-per-event** rate — the
> highest availability on the board."

That figure comes from `00_AWARD_LIST_VERIFIED.md` line 160 and is an artifact of summing three
different awards: `FIRST Leadership Award` (**10 events**) + `Finalist` (172) +
`DCMP Semi-Finalist` (218) = 400 ÷ 192 = 2.08. The empirical 2026 file flags this explicitly. **The
actual FIRST Leadership Award was handed out at 10 events.** A team told it is "the highest
availability on the board" would staff a submission against a 19× overstated hit rate.

**Second-order problem:** the awards were paired to the strategies §3 got wrong. Excellence in
Engineering was hung on S10 — the climber the data says nobody successfully built.

---

## 5. BOM — **C−**, with one fatal design error

**The numbers are credible.** Every line sits inside `reference/team_capacity.yaml`: build 91.0 h of
129.8; design 36.0 of 74.9; programming 62.0 of 134.8 (already inflated ~40 h for Systemcore);
$2,154.99 discretionary of $2,500; 7 motors of 12; 3 workstreams of 3. For 15 students at 15
scheduled h/wk with one technical mentor, a KOP chassis + one intake + one passive latch at ~91
build hours is realistic — arguably still optimistic on assembly rework, but within reason. The
order schedule (electrical on a PO **2026-11-21**, seven weeks before kickoff) is the single most
actionable line in the whole review and it is right.

**The descope logic is the best judgement in the document.** Forcing "you may have a scoring
mechanism *or* an active climber, not both" out of a gate model, rather than out of an argument, is
exactly what this pipeline is for.

**And the robot it priced cannot score.**

> "**Design:** KOP chassis + under-bumper roller intake feeding a **hopper dump into the HUB** from a
> surveyed ALLIANCE ZONE position."

The HUB's top opening has its **front edge 72 inches off the carpet** (`03_ARCHETYPE_CORPUS.md` §2.1,
manual §5.4). **A hopper dump cannot deliver FUEL over a 72-inch lip.** There is no shooter and no
lift in the BOM. The corpus calls this number out by name — §2.4 item 4: "**72 in scoring lip is the
mechanism gate.** Any archetype delivering FUEL must clear 72 in. That is why R7 (lift) rates below
R2 (shoot). In BIOCORE, find this number first."

The pipeline costed, gate-checked, scheduled, and ordered parts for a robot with no legal path to the
scoring opening — and then computed all of §2 (8 FUEL per 8.0 s cycle) as that robot's throughput.
The BOM model has no geometric feasibility check whatsoever: it validates dollars, hours,
workstreams, and motors, and has no concept of *whether the mechanism can reach the target*.

---

## What the pipeline would have told the team that was WRONG

Stated as the team would have heard it on kickoff day.

1. **"Build for TRAVERSAL. Two L1 climbs in AUTO plus two in TELEOP equals exactly 50 — a full bonus
   RP that costs a Championship alliance the same as it costs you."**
   TOWER points were **1.1 %** of the average match (Avg Tower 1.92 vs Avg Match 178.75). 36 % of
   team-events scored zero tower points ever. Winning alliances climbed at *exactly* the league
   average. This was the document's headline recommendation, its only BUILD THIS row, and its award
   strategy — and it pointed at the least consequential scoring channel in the game.

2. **"The small-team play is not to compete on cycle rate at all."** (§2.4)
   REBUILT was an uncapped 1-point-per-element rate game with a 4.1× p99/median spread. The corpus's
   verdict on the cheap version of rate — R2, fixed-zone bulk shooter, $600–1,100, bandsaw+drill —
   is "**the highest-value small-team play in REBUILT.**" The pipeline ranked it **10th of 14** and
   dismissed it in one clause ("a defender parks on it").

3. **"Build this robot: intake + hopper dump."**
   It cannot reach a 72-inch opening. The team would have ordered parts on **2026-11-21** for a robot
   that cannot score, seven weeks before anyone could check.

4. **"One second of cycle time is worth ~10 points per match."**
   Derived from an invented 8 FUEL / 8.0 s (1 pt/s). The corpus's fixed-zone shooter runs ~0.5 pt/s.
   Every sensitivity number in §2.4 is roughly 2× hot, on top of a design that delivers 0 pt/s.

5. **"AUTO-only is rank 9 — a spectator for 140 seconds."**
   Avg Auto Fuel was the strongest single-column pick and win signal available: 33.3 unpicked → 37.5
   picked → **48.3 for event winners**. The corpus calls R5 a "captain-tier multiplier" and the best
   points-per-dollar archetype in five seasons.

6. **"FIRST Leadership Award has the highest availability on the board — 192 events, 2.08 per event."**
   10 events. The 192/2.08 figure sums the Award with its Finalist and Semi-Finalist variants.

7. **"Defense is ruinously expensive in seat time" (S4/S12 at rank 6–7, A4 = 0/5).**
   Directionally under-weighted: 2026 was the strongest defense season in the five-season corpus
   *because* of the SHIFT mechanic the review itself discovered — for 50 s your HUB is dead, so
   defense costs you nothing. The review found the mechanic and did not propagate it into the
   achievability score for defense.

8. **Not wrong, and worth protecting:** the duty-cycle correction, "L3 = L2," the do-everything
   rejection, the descope, the 2026-11-21 order date, and **the entire loophole section**.

---

## Prioritised fix list

1. **Backtest the strategy ranker against `tba_rankings_*.csv` before it is allowed to emit a
   ranking.** For every prior season, compute the correlation between each scoring channel and
   (a) match score, (b) pick rate, (c) winning. A ranker that would have put a 1.1 %-of-score channel
   in BUILD THIS must fail its own regression test. *This is the fix; everything below is smaller.*

2. **Make `03_ARCHETYPE_CORPUS.md` a mandatory input to Step 3, not background reading.** Every
   candidate row should carry the corpus archetype it maps to and that archetype's verdict. S2 would
   have carried "R2 — highest-value small-team play" and could not have finished 10th.

3. **Add a geometric feasibility gate to `bom-builder.py`.** A `delivery_height_in` on each scoring
   mechanism and a `scoring_aperture_height_in` in `game_def.json`, hard-failing when the mechanism
   cannot reach. The 72-inch lip is exactly the number the corpus tells you to find first, and
   nothing in the pipeline consumes it.

4. **Source `median_alliance_score` and cycle-rate priors from TBA automatically.** `game_def.json`
   should refuse a hand-guessed 120 when `tba_matches_2026.csv` says 147. Same for `per_cycle` and
   `fixed_actions[].time_s` — require a `_source` field naming either a manual citation or a TBA
   column, and print `[UNSOURCED]` beside every derived number that lacks one.

5. **Extend the loophole hunt to inspection rules (R1xx/R4xx).** Add "bumpers, perimeter, extension,
   and inspection" as a required subsection with at least one Q&A filed. This one blind spot cost
   19.5 % of the season's real Q&A volume.

6. **Reconcile `00_AWARD_LIST_VERIFIED.md` against `00_AWARD_LIST_EMPIRICAL_2026.md`** and delete or
   footnote the availability column that sums an award with its Finalist and Semi-Finalist variants.

7. **Then, and only then, the `REHEARSAL_FINDINGS.md` fixes** — the `mfg_floor` alias map, the
   REEFSCAPE diff rehearsal, the conditional-scoring schema, and deleting
   `manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf`. They are all real. They are all about the
   pipeline producing *an* answer. Fixes 1–3 are about it producing a *right* one.

> The rehearsal concluded: "the pipeline works; the judgement layer around it does not yet defend
> itself." That is correct and understated. The mis-gating bug it found deleted three good rows and
> was caught. The failure graded here deleted nothing, crashed nothing, printed no warning, and put
> the wrong robot in the BUILD THIS box with a citation next to it.


---

## Patches applied — 2026-08-22

Everything below is in place in the repo. Back-test re-run after every change:
`python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml` → **27/30 = 90%,
unchanged. No rubric weight, threshold, or factor was touched.**

## 1. `tools/score-strategy.py` — the `mfg_floor` mis-gate (Finding 2.1, the headline defect)

| | |
|---|---|
| **Before** | `mfg = gi.get("mfg_floor", "hand")` then `if mfg not in owned: fire G1`. Any unrecognised string — including every token in the vocabulary `CLAUDE.md` blessed — fired a hard capability gate and printed `needs '<your string>'; shop has [...]`, which reads like a legitimate finding. Five of fourteen candidates were falsely `T4 GATED`, including the #1-ranked strategy. |
| **After** | New `MFG_ALIASES` map + `legal_mfg_floors(rub)` (derived from the rubric itself, so it cannot go stale) + `normalize_mfg()`. `hand_tools`→`hand`, `bandsaw_drillpress`→`bandsaw+drill`, `router_cnc`/`outsourced`/`waterjet`→`router`, `mill_lathe`/`cnc`→`CNC`, `3d_print`→`3dprint`. **An unrecognised token now `sys.exit`s with a `SCHEMA ERROR` naming every legal and aliased token** — it can never again fire G1. |
| **Proved** | `mfg_floor: hand_tools` → was `T4 GATED`, now **`BUILD THIS / T1 GREEN`**. `mfg_floor: mill_lathe` → correctly aliases to `CNC` and still gates. `mfg_floor: hand_toolz` → hard schema failure, no ranking emitted. Back-test 27/30 unchanged. |

## 2. `tools/cycle-model.py` — three silent-ignore bugs (Finding 3.1)

| | Before | After |
|---|---|---|
| `rp[].metric` | `if "TOWER" in rp["metric"]` — a 2026-REBUILT game noun compiled into a game-agnostic tool. Naming a 2027 RP metric anything else silently modelled a climb RP as a cycle count. | New `rp_is_fixed_based()`. An explicit `basis: cycle\|fixed` field wins; otherwise the metric is token-matched against `fixed_actions[].name`. **Verified identical classification on REBUILT** (TRAVERSAL → fixed, ENERGIZED/SUPERCHARGED → cycle) with the noun removed. |
| `cycle_actions[1..n]` | Silently ignored. A game with two repeatable scoring actions could not be modelled and gave no hint. | `validate_game()` prints a `SCHEMA WARNING` naming the ignored entries and what to do instead; empty `cycle_actions` is now a hard error. |
| `endgame_s` | Printed in the banner, used in no arithmetic. Readers could not tell whether `teleop_s` was inclusive of it. | Banner now states it is **informational only**, that the real cost is `fixed_actions[].time_s`, and that `teleop_s` must be the full teleop period **inclusive** of the endgame window. |

## 3. `tools/RUN-KICKOFF.sh` — schema stub under-specification (Findings 3.1–3.3) and `review/<dir>`

- **`review/LATEST`** (Finding 2.4). Phase 1 now writes the run directory to `review/LATEST`; phase 2
  accepts **no argument at all** and reads it. Before: `review/<dir>` was undefined and only
  recoverable from phase-1 stdout. Proved: `bash tools/RUN-KICKOFF.sh --phase2` ran the full pass with
  no path, and fails with `run phase 1 first` when `LATEST` is absent.
- **`game_def.json` stub** — every field the rehearsal called unclear now carries an inline `_note`:
  `teleop_s` is endgame-**inclusive**; `endgame_s` is informational; only `cycle_actions[0]` is
  modelled; `per_cycle` and every `time_s` are **robot-design assumptions with no manual source** and
  now have required `_source` siblings; `points_auto`/`points_teleop` cannot express a phase-only
  action (split into two rows); `rp[].basis` replaces the magic string; `rp[].threshold` is a single
  scalar at *your* event tier; and a `_known_gaps` key states plainly that duty cycles, conditional
  multipliers and zero-point phases **cannot be expressed** and must be hand-derated.
- **`candidates.yaml` stub** — `mfg_floor` legal + aliased token lists inline; `new_workstreams`
  documented as *on top of the three mandatory streams* with an explicit warning that
  `bom-builder.py` uses a different convention and the numbers should differ by ~3;
  `novel_mechanisms` reconciliation rule (builder wins); `drive_practice_sensitivity` legal enum
  `low\|med\|high\|extreme`; `cycle_model.game` path resolution stated; `cycle: 999` named as the
  non-scoring sentinel; `median_alliance_score` pointed at `research/predictive_tba/tba_matches_*.csv`
  with the 2026 value (147) beside the graded guess (120); and a new **required `corpus_archetype`
  field** on every row.
- **`bom_config.yaml` stub** — the invisible workstream-absorption heuristic is now stated, and the
  `notes` field **requires** a sentence on how the design physically reaches the scoring aperture,
  with a pointer to the corpus's "find this number first". *(The geometric gate itself is not built —
  see "not fixed", below.)*

## 4. `tools/ingest-manual.sh` — the poisoned BIOCORE slot (Finding 2.3)

**Before:** any PDF handed to it was copied to `manuals/2026-27_BIOCORE/BIOCORE_GameManual_<label>.pdf`
— so the rehearsal left a 2026 manual under a 2027 name, in the exact folder `CLAUDE.md` watches,
satisfying the autorun trigger. **After:** the copy takes the BIOCORE name only if the filename or the
PDF's first five pages contain "BIOCORE"; otherwise it is copied as `NOT-BIOCORE_<source name>` with a
warning on stderr, and `CLAUDE.md` now states that a `NOT-BIOCORE_*` file is never a trigger. Proved on
REBUILT. **The stray `BIOCORE_GameManual_V1.pdf` and both rehearsal ingest directories are deleted;
`manuals/2026-27_BIOCORE/` now contains only `sections/`.**

## 5. `CLAUDE.md` — rewritten where it was ambiguous, wrong, or impossible

| Was | Now |
|---|---|
| *"`team_capacity.yaml` is the authority… never contradict it"* — following this produced the wrong answer | authority for **hours, headcount and budget, and nothing else**; `achievability_rubric.yaml` named as what the scorer actually reads |
| `review/<dir>` used in three steps, never defined | *"`review/<dir>` means: the path written in `review/LATEST`"*, stated once at the top |
| *"grade the 10 predictions"* (there are 11) | *"grade **every prediction** … the count changes; do not assume it"* |
| *"Two awards per strategy"* (28 pairings for 14 rows) | *"Two awards for each strategy **in the top tier**"*, plus one team-level row |
| `kickoff_award_check.sh` never mentioned | required before writing §5 |
| award availability quoted from `00_AWARD_LIST_VERIFIED.md` | cross-check against `00_AWARD_LIST_EMPIRICAL_2026.md` mandated, with the 10-vs-192 error named inline |
| trigger = any `*BIOCORE*.pdf` in the folder | same, **plus** "a `NOT-BIOCORE_*` file is never a trigger" |
| no guidance on writing schema files | *"write with the file-write tool, never a shell heredoc"* — the Git Bash apostrophe truncation, stated twice |
| ranking read as one column | quadrant/tier operating rule; **never print a tier without its quadrant** |
| corpus was background reading | `corpus_archetype` mandatory on every candidate row, defended by name in §3 |
| loophole hunt = strategic rules | **required inspection subsection** (R4xx, perimeter, extension) with at least one filed Q&A — the 19.5%-of-Q&A blind spot |
| no acknowledgement that the rubric assumes two scorers | states the two-scorer procedure is impossible for one agent and what to do instead |
| step 5 written last | §§1, 6, 7, 8 drafted during step 2, while compute runs |
| probe failure = pipeline does not start | explicit fallback: ask for a URL or local file, do not stall |
| BOM output trusted | states the BOM has **no geometric feasibility check** and the cycle model must be sanity-checked against `research/predictive_tba/` |

## 6. The known unpatched defect: tier contradicting quadrant — **documented, not retuned**

**Decision: documented.** The tier thresholds (62/48 on the blended index) are what the 30-record
back-test was calibrated against at 27/30. Any threshold change to remove the contradiction
invalidates that calibration, and the brief forbids retuning without re-proving the rate. So:

- **`reference/ACHIEVABILITY-RUBRIC.md`** now opens — above everything, before the companion-files
  line — with a blockquoted **⚠ OPERATING RULE — THE QUADRANT DECIDES, THE TIER ONLY WARNS**,
  including the worked case that a zero-value trivially-buildable robot reads `T2 STRETCH`
  (ACH 100, VAL 0 → C = 55), and a pair-by-pair reading table for the four contradictory
  combinations.
- **`CLAUDE.md` §Step 5 ¶3** carries the same rule and forbids printing a tier without its quadrant.
- **`tools/score-strategy.py`** now computes a non-scoring `conflict` field and prints an
  **`!! QUADRANT/TIER DISAGREEMENTS`** block under the matrix. It changes no tier, no score and no
  gate — back-test verified unchanged at 27/30. On the corpus it immediately names `G1 Cube-Only Top-Row
  Cycler` (TRAP / T2 STRETCH); on the rehearsal's own candidates it names `S11 ENERGIZED RP chaser`
  (DELETE / T2 STRETCH). Both were previously silent.

## 7. Pipeline re-run end to end

Phase 1 (`RUN-KICKOFF.sh <manual> V2`) → 458-line briefing pack, three stubs, `review/LATEST` written.
Phase 2 (`RUN-KICKOFF.sh --phase2`, **no path argument**) → cycle model, sweep, ranking, BOM
(`ALL GATES PASS`, earliest order-by 2026-11-21). Zero crashes. Test artifacts removed afterwards;
`review/V1_20260823T014011Z/` (the worked example) left in place.

## What was deliberately NOT fixed

1. **The TBA back-test gate on the strategy ranker** (grade fix 1) and **automatic sourcing of
   `median_alliance_score` / cycle priors from TBA** (fix 4). These are new analysis, not repairs, and
   fix 4 in particular would change ranking outputs — which cannot be done without re-deriving the
   back-test. Mitigated for now by instruction: the stub points at the CSVs and gives the 2026 value,
   and `CLAUDE.md` requires the sanity check.
2. **The geometric feasibility gate in `bom-builder.py`** (grade fix 3, the robot that cannot reach a
   72-inch lip). A real schema change to both `game_def.json` and the mechanism catalog. Mitigated by
   making the aperture-clearance sentence a required field in `bom_config.yaml.notes` and stating in
   `CLAUDE.md` §Step 4 that the BOM performs no such check.
3. **Conditional-scoring support in `game_def.json`** (duty cycles, positional multipliers). Mitigated
   by the `_known_gaps` key, which names the gap and prescribes the hand-derate.
4. **Rubric weights, thresholds and factors.** Untouched by design; the 27/30 rate is intact.
5. **The 2025 REEFSCAPE diff rehearsal** (Finding 2.2) — the rule/glossary diff is still unexercised
   against a genuinely different manual. It is a five-minute run and it is the largest remaining
   untested path.
6. **`probe-2027-manual.sh` against a live 2027 URL** — untestable before the season opens.
