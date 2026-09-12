# REMEDIATION VERIFY — did the four fixes actually fix what `REHEARSAL_GRADE.md` found?

**Verified:** 2026-08-22 · **Verifier:** independent pass, adversarial posture
**Spec:** `review/REHEARSAL_GRADE.md` (grades: loophole A−, awards B−, BOM C−, scoring D, ranking D)
**Method:** every claim below was re-derived by running the tool or re-counting the source CSV/TSV.
No fix was accepted on the strength of its own patch note.

| # | Defect from the grade | Verdict |
|---|---|---|
| 0 | REGRESSION GUARD — back-test rate | **PASS — 27/30 = 90 %, unmoved** |
| 1 | BOM has no geometric feasibility check (grade §5, fix 3) | **PASS** |
| 2 | Cycle-model priors invented, never checked against TBA (grade §1, fix 4) | **PASS — and the tool is more correct than the grade** |
| 3 | Loophole hunt blind to inspection rules (grade §3, fix 5) | **PASS** |
| 4 | Award availability sums an award with its Finalist tiers (grade §4, fix 6) | **PASS — and it corrects the grade's own number** |
| 5 | End-to-end pipeline still completes | **PASS** |

---

## 0. REGRESSION GUARD — back-test

Run before any inspection and again after all verification work and cleanup. Identical both times.

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml

--- Back-test against archetype_corpus.yaml hand labels ---

 agreement: 27/30 = 90%   (the corpus's own risk predicate scores 21/30 = 70%)

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
C1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
P1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
R7   MARGINAL      T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
```

**27/30 = 90 %. Unchanged from the documented rate.** The three misses are the same three
(C1/P1/R7 — all hand-labelled CONDITIONAL/MARGINAL, all gated on the same 3-novel-mechanism
workstream gate). No rubric weight, threshold or factor was touched by this pass and none needed to
be. **No justification of a moved number is required, because the number did not move.**

The matrix also still prints the `!! QUADRANT/TIER DISAGREEMENTS` block and still names
`G1 Cube-Only Top-Row Cycler (TRAP but T2 STRETCH)` — the patch-6 documented-not-retuned defect is
still visible, still non-scoring.

---

## 1. GEOMETRIC GATE — **PASS**

The grade's fatal §5 finding: a hopper dump was costed, gated, scheduled and ordered against a HUB
whose scoring lip is 72 in off the carpet, and *no tool objected*.

### 1a. Independently reconstructed failing case

I did not run the shipped `geom_fail_2026_hopper.yaml` as the proof. I wrote my own config from
scratch (over-bumper intake + hopper, 72 in aperture) so the gate could not be passing a
purpose-built fixture:

```yaml
name: "INDEP -- intake + hopper dump vs 72in HUB"
target:
  name: "HUB upper opening"
  aperture_height_in: 72
  aperture_range_in: 0
  source: "manual s5.4 via 03_ARCHETYPE_CORPUS 2.4"
mechanisms: [kop_chassis, bumpers_frame, baseline_electrical_package, over_bumper_intake, hopper]
```

```
  [FAIL] GEOMETRY (REACH)     best reach 30 in (hopper)    limit 72 in
         HUB upper opening: aperture 72 in up, 0 in out (manual s5.4 via 03_ARCHETYPE_CORPUS 2.4)
         | NOTHING IN THIS CONFIG CAN REACH THE SCORING TARGET. Tallest delivery is hopper at
         30 in -- SHORT BY 42 INCHES. This robot would be fully costed, gated, scheduled and
         ordered -- and would score zero. Change the mechanism, not the gate.

  VERDICT: FAILS 1 GATE(S): GEOMETRY (REACH)
```

Process **exit code 1**. The shortfall is named in inches (72 − 30 = 42), the reaching mechanism is
named, and the message forbids the obvious wrong repair. This is exactly the defect the grade
described, and it now hard-fails.

### 1b. Shooter config passes the reach gate

Same intake, `single_flywheel` swapped in for the hopper:

```
  [PASS] GEOMETRY (REACH)     single_flywheel reaches 108 in (shoot) limit 72 in
```

The gate discriminates on the mechanism, not on the config. (My shooter config still fails an
*unrelated* `TOOLING FLOOR` gate — the flywheel needs shop capability the team lacks. That is a
different, correct gate firing, and the shipped `geom_pass_2026_shooter.yaml` behaves identically.
Reach itself is PASS in both.)

### 1c. The three example configs still work

```
simple      VERDICT: ALL GATES PASS
moderate    VERDICT: FAILS 5 GATE(S): BUDGET, BUILD HOURS, DESIGN HOURS, PARALLEL WORKSTREAMS, NOVEL MECHANISMS
ambitious   VERDICT: FAILS 8 GATE(S): BUDGET, TOOLING FLOOR, BUILD HOURS, DESIGN HOURS, PROGRAMMING HOURS, PARALLEL WORKSTREAMS, NOVEL MECHANISMS, MOTOR COUNT
```

None of these declares a `target:`, so GEOMETRY does not appear among their failures — the new gate
did **not** silently break the existing descope-demonstration ladder. `simple.yaml` still passes
everything, as it must.

### 1d. No-target WARNING fires

A config with no `target:` block at all:

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!  WARNING -- GEOMETRIC FEASIBILITY WAS NOT CHECKED
!!  This configuration declares no  target:  block, so NOTHING here verifies
!!  that the robot can physically reach the scoring aperture. Dollars, hours,
!!  workstreams and motors were all checked. Reach was not.
!!  ... Find this number FIRST -- reference/03_ARCHETYPE_CORPUS.md 2.4 item 4.
!!  The 2026 rehearsal costed a hopper dump (30 in rim) against a 72 in HUB
!!  lip and shipped an order schedule for it. No tool objected. This is that
!!  tool objecting.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

The gate row reads `[PASS] GEOMETRY (REACH)  *** NOT CHECKED ***`, exit 0, `VERDICT: ALL GATES PASS`.

**This is the one place the fix is soft, and it is deliberate.** Omitting `target:` warns loudly but
does not fail. Three things blunt it:

1. The phase-1 stub in `RUN-KICKOFF.sh` **emits a `target:` block with `aperture_height_in: 0`**, and
   the gate hard-fails a declared-but-zero aperture (`TARGET DECLARED BUT NOT ANSWERED`). So the
   default path from a fresh run cannot reach a pass without a real number.
2. `CLAUDE.md` Step 3 line 59 makes the `target:` block the **first** thing filled in
   `bom_config.yaml`, and Step 4 lines 157–159 forbid proceeding on `*** NOT CHECKED ***`.
3. The warning names the 2026 failure by name, so it cannot be read as boilerplate.

Residual risk stated plainly: **a run that deletes the stub's `target:` block still emits
`ALL GATES PASS`.** See "still worries me", below.

---

## 2. PRIORS — **PASS**, and the tool beats the grade

`tools/score-priors.py` has three modes; all three were run.

### `priors` (no argument) — cross-season kickoff priors

```
  yr   game         median    mean    p10    p90   AUTO%   END%  endgame column
  2023 CHARGED UP     87.0    95.1     44    139    27.2   29.0  Avg Charge Station
  2024 CRESCENDO      50.0    53.9     23     87    36.9   10.2  Avg Stage
  2025 REEFSCAPE      93.0   107.9     41    169    20.1   10.9  Avg Barge
  2026 REBUILT       147.0   182.7     44    374    20.2    1.1  Avg Tower
```

- **median 147.0 / mean 182.7 for 2026 — matches the grade exactly.**
- **endgame share 1.1 % in 2026 vs 10.9 % in 2025 — matches the grade exactly.**
- The tool refuses to emit a point estimate: every prior is scored WEAK (spread/mean 103 %, 64 %,
  218 %) and must be reported as a band. The endgame prior's verdict is literally `ADOPT AS: NOTHING`
  — a 27x swing across four seasons is declared unpredictable rather than averaged into a number.
  That is the correct response to the grade's §1 finding and stronger than the fix list asked for.
- It names the rehearsal's error inline: *"The rehearsal's guess of 120 sits BELOW this entire
  4-season range."*

### `distributions <year>`

```
=== ALLIANCE-SCORE DISTRIBUTION -- 2026 REBUILT ===
  source: research/predictive_tba/tba_matches_2026.csv  (n = 30,352 alliance-scores)
    median alliance score      147.0
    mean   alliance score      182.7
  COMPONENT SHARES -- source: tba_rankings_2026.csv  (n = 8,160 team-events)
    mean Avg Match            178.75
    AUTO    'Avg Auto Fuel'  mean 36.02  ->  share  20.2 %
    ENDGAME 'Avg Tower'  mean 1.92  ->  share   1.1 %
    team-events with ZERO endgame points: 36.4 %
```

n = 30,352 and n = 8,160 are the grade's own population counts; mean Avg Match 178.75, Avg Tower
1.92, and 36.4 % zero-tower all reproduce the grade line for line. 2025 returns `Avg Barge` 10.48 /
`Avg Match` 96.04 → **10.9 %**, again the grade's number.

### `endgame-check <year>`

```
  signal                              r vs Avg Match   r vs picked
  ENDGAME  Avg Tower                           0.003         0.045
  AUTO     Avg Auto Fuel                       0.955         0.100
  Avg Match (benchmark)                           --         0.139

  VERDICT: ENDGAME IS NOT LOAD-BEARING in 2026. ... DO NOT put an endgame mechanism in
  BUILD THIS on this evidence. AUTO out-predicts ENDGAME on pick rate (0.100 vs 0.045).
```

**`corr(Avg Tower, Avg Match) = 0.003` — matches the grade exactly.** So do 0.045, 0.100 and 0.139.

**Where the tool disagrees with the grade, the tool is right.** The grade quoted
`corr(Avg Auto Fuel, picked) = 0.100` as evidence AUTO was the discriminator, and never examined
AUTO against match score. The tool computes `r = 0.955` against match score and then **flags its own
number as contaminated** — `Avg Auto Fuel` is a FUEL count inside the same 1 pt/FUEL scoring channel
as `Avg Match`, so the columns are not independent. It instructs the reader to use the 0.100
pick-rate figure instead. It applies the same unit caveat to the 2026 AUTO *share*. That is a caveat
the grade should have carried and did not. **Tool right, grade incomplete.** No number in the tool
contradicts the grade; it adds one the grade missed.

Every figure in every mode carries its source file and row count. Nothing is hand-entered.

---

## 3. INSPECTION AXIS — **PASS**

### `CLAUDE.md` requires both axes

- Line 204: `Axis (a) — STRATEGIC ambiguity.`
- Line 214: `Axis (b) — INSPECTION / CONSTRUCTION ambiguity. Will this robot be allowed on the
  field at all?` Families: **bumpers (R4xx)**, **robot perimeter (R1xx)**, extension and volume.
- Line 217: required checklist names **R401** (bumpers almost all around) and **R402** (bumper
  construction) by rule ID.
- Line 229: `The hunt ... named none of them. It scored A− purely on axis (a). One axis is not a
  pass.`
- Line 39 pulls the R4xx block forward: *"read it BEFORE any CAD."*

### `CLAUDE.md` requires >= 2 inspection-family Q&A questions

Stated **twice**, in the loophole step and again in the Q&A-filing step:

- Line 240: `Minimum filing: at least 2 of the week-1 Q&A questions in §8 must come from axis (b).`
- Line 256: `At least 2 questions must come from §6 axis (b) — bumpers, perimeter, extension.`
- Line 254 carries the accountability sentence: `R402 — 16 real questions, rank 2 for the season —
  went unmentioned.`

Both requirements are present, both are hard ("must"), and both name the rule families rather than
gesturing at "inspection".

### The two reference files agree on the R4xx numbers — and both agree with ground truth

`RULE-CHURN-WATCHLIST.md` §4 (Tier INSPECTION) vs `QA-AMBIGUITY-HOTSPOTS.md` per-rule table vs
`research/rule_inventories/qa_heat_2026.tsv`:

| Rule | WATCHLIST (total / 2026) | HOTSPOTS (total / 2026) | qa_heat_2026.tsv (2026) | agree? |
|---|---|---|---:|---|
| R402 | 28 / **16** (rank 2 of 91) | 28 / **16** (3→9→16) | **16** | yes |
| R401 | 22 / **12** (rank 3) | 22 / **12** (8→2→12) | **12** | yes |
| R404 | 19 / 9 | 19 / 9 (2→8→9) | 9 | yes |
| R405 | 19 / 8 | 19 / 8 (1→10→8) | 8 | yes |
| R408 | 16 / 0 | 16 / 0 (13→3→0) | *(absent = 0)* | yes |
| R409 | 12 / 5 | 12 / 5 (6→1→5) | 5 | yes |
| R101 | 15 / 6 | 15 / 6 (5→4→6) | 6 | yes |
| R106 | 12 / **12** | 12 / **12** (0→0→12) | **12** | yes |

Both files independently assert **"the bumper six drew 116 questions across 2024–2026"** and both
assert **"R402 is rising: 3 → 9 → 16."** Arithmetic check on the shared claim:
28 + 22 + 19 + 19 + 16 + 12 = **116**. Row-total check on the rising claim: 3 + 9 + 16 = **28**,
matching R402's total column in both files.

`QA-AMBIGUITY-HOTSPOTS.md` line 73 also carries the grade's indictment verbatim: the review *"named
zero of R402/R401/R404/R405/R101/G425 — 57 questions, 19.5 % of the season."* Recount from
`qa_heat_2026.tsv`: 16 + 12 + 9 + 8 + 6 + 6 = **57**.

**Zero discrepancies between the two documents, and zero discrepancies against the source TSV.**

---

## 4. AWARDS — **PASS**, and the fix is more accurate than the grade

### Machine check: no availability figure exceeds its own distinct-event count

I parsed every three-column markdown table row in `reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`
whose first cell is an **exact** award name present in `research/awards_tba/tba_awards_2026.csv`, and
recomputed `rows` and `COUNT(DISTINCT event)` from the CSV:

```
empirical table rows checked: 9   mismatches: 0
```

Every published pair reproduces from the CSV, and in every case `distinct_events <= rows`, which is
the invariant the old rollup violated.

I also swept `reference/awards/*.md` for any integer in an award-named table row exceeding that
award's row or event count. Twelve hits surfaced; **all twelve are false positives of my own
parser** — they are the `Distinct winners` column of the openness table in `AWARD-ALIGNMENT.md`
lines 133–141 (e.g. `Creativity ... 706`) and the winner-forensics table in
`00_AWARD_LIST_VERIFIED.md` line 477 (`Engineering Inspiration ... 948 / 556 / 3558`). Those are
*team* counts and rank statistics pooled over 2022–2026, not availability. **No availability figure
anywhere in `reference/awards/` exceeds its distinct-event count.**

### Three awards spot-checked by hand against the TBA CSV

Counted directly from `research/awards_tba/tba_awards_2026.csv`:

| Exact award name | CSV rows | CSV distinct events | Repo says | Match |
|---|---:|---:|---|---|
| `FIRST Leadership Award` | **10** | **1** (`2026cmptx`) | "10 rows / **1 event**" (EMPIRICAL L24, L59; VERIFIED §2.1a) | yes |
| `FIRST Leadership Award Finalist` | **172** | **71** | "172 rows / **71 events**" (EMPIRICAL L60, L96) | yes |
| `District Championship FIRST Leadership Award Semi-Finalist` | **218** | **120** | "218 / **120**" (EMPIRICAL L61, L95) | yes |

Sum check on the retracted figure: 10 + 172 + 218 = **400 rows**, and the union of their events is
the discredited **192**. 400 / 192 = **2.08** — the rollup is fully explained and correctly retracted.

### The remediation corrects the grade

**The grade itself is wrong here.** `REHEARSAL_GRADE.md` §4 states: *"The actual FIRST Leadership
Award was handed out at 10 events."* The CSV says **10 rows at 1 event** — ten students at
`2026cmptx`, the Championship. The repo has it right and the grade does not:

> `| FIRST Leadership Award (the award itself) | 1 (2026cmptx, Championship) | 10 | 10.00 |`
> "The FIRST Leadership Award proper was given at **one event in the entire 2026 season**, not 192.
> ... The winnable tier is the **Finalist** (71 events)."

The overstatement is therefore **192x, not 19x** as the grade computed. The retraction is present in
five places (`00_AWARD_LIST_VERIFIED.md` §2.1 / §2.1a / the `†1` footnote,
`00_AWARD_LIST_EMPIRICAL_2026.md`, `awards.yaml` lines 632/646 with a dated CORRECTED note, and a
warning in `kickoff_award_check.sh`), and `AWARD-ALIGNMENT.md` line 213 re-labels the Leadership lane
to the reachable **Finalist** tier. Every surviving mention of "192 / 2.08" sits inside an explicit
retraction.

---

## 5. END-TO-END — **PASS**

Phase 1 against a prior-season manual (`manuals/archive/frc/2025_REEFSCAPE_GameManual.pdf`, label
`VERIFY`) — this also exercises the fix-list item 5 REEFSCAPE diff path:

```
== 1. Ingest (rules, glossary, diff, tripwires) ==   OK  ingest-manual.sh
== 2. Assemble briefing pack ==                      OK  briefing pack: 482 lines
== 3. Write schema stubs ==                          OK  game_def.json · candidates.yaml · bom_config.yaml
== PHASE 1 COMPLETE ==      exit 0
```

**The poisoned-slot guard held.** The REEFSCAPE PDF landed as
`manuals/2026-27_BIOCORE/NOT-BIOCORE_2025_REEFSCAPE_GameManual.pdf` — prefixed, therefore not an
autorun trigger.

**Preflight correctly refused to run on unfilled stubs.** I first copied the stubs from the earlier
`NOT-BIOCORE-REEFSCAPE_20260823T021245Z` run; those still contain 16 / 4 / 2 `FILL_ME` markers and
phase 2 stopped dead:

```
== Phase 2 preflight ==
!! game_def.json still contains FILL_ME placeholders. Fill it before phase 2.
```

That is a real guard, not a formality — it caught a stub set that *looked* complete.

Phase 2 with genuinely filled stubs (from the `V1_20260823T014011Z` worked example; 0 `FILL_ME`),
invoked with **no path argument** so `review/LATEST` was exercised:

```
$ bash tools/RUN-KICKOFF.sh --phase2
...
== 4. Team Update watch (season-long) ==   No Team Updates on disk for 2027.
== PHASE 2 COMPLETE ==      exit 0
   results -> review/VERIFY_.../results
     cycle_model.txt · cycle_sweep.txt · strategy_ranking.txt · strategy_ranking.json · bom.md / bom.csv
```

Zero crashes across both phases. The geometric-feasibility WARNING banner fired in the middle of
phase 2 (§1d) because the V1 worked-example `bom_config.yaml` carries no `target:` block — the new
gate is wired into the pipeline, not just the standalone tool.

### Cleanup — verified clean

Removed: `review/VERIFY_20260823T023632Z/`,
`manuals/2026-27_BIOCORE/ingest_VERIFY_20260823T023633Z/`, and
`manuals/2026-27_BIOCORE/NOT-BIOCORE_2025_REEFSCAPE_GameManual.pdf`. `review/LATEST` was backed up
before the run and restored to its prior value afterwards.

```
$ ls -A manuals/2026-27_BIOCORE/
sections

$ ls review/
LATEST  NOT-BIOCORE-REEFSCAPE_20260823T021245Z  REHEARSAL_FINDINGS.md  REHEARSAL_GRADE.md  V1_20260823T014011Z
```

**No manual PDF of any kind in `manuals/2026-27_BIOCORE/`.** The directory holds `sections/` only,
exactly as the patch pass left it. Back-test re-run after cleanup: **27/30 = 90 %.**

---

## What is still broken or still worries me

1. **The geometry gate is opt-in at the last mile.** Deleting `target:` from `bom_config.yaml`
   yields `ALL GATES PASS` plus a warning banner. The 2026 failure was not a wrong number, it was an
   *absent* check — and the repair leaves one path where the check is absent again. It is mitigated
   three ways (the stub ships `aperture_height_in: 0`, which hard-fails; `CLAUDE.md` orders it filled
   first; `CLAUDE.md` forbids proceeding on `*** NOT CHECKED ***`) but all three are instructions to
   a reader, not a gate on a tool. **Recommended hardening: make a missing `target:` block a phase-2
   preflight failure**, the same way `FILL_ME` is. That is a small change to `RUN-KICKOFF.sh` and it
   moves no ranking output.
2. **Nothing forces the strategy ranker to consult the priors.** `score-priors.py` is excellent and
   entirely passive. `score-strategy.py` will still happily put an endgame archetype in BUILD THIS;
   the only thing stopping it is `CLAUDE.md` telling the assistant to look. Grade fix 1 — *"a ranker
   that would have put a 1.1 %-of-score channel in BUILD THIS must fail its own regression test"* —
   is **still not built**, and it was the grade's number-one priority. This is the largest remaining
   gap, and it is genuinely deferred rather than papered over: the patch pass said so in writing.
3. **`corpus_archetype` is required by schema but not enforced by tool.** `CLAUDE.md` and the
   candidates stub mandate it on every row; I found no check that refuses a row lacking it.
4. **The 27/30 back-test is 30 hand-labelled corpus records, not a season of outcomes.** It proves
   the rubric reproduces the corpus's judgement. It does **not** prove the rubric would have
   rejected the 2026 climber — the corpus is the same document the ranking ignored. Treating 90 % as
   evidence of predictive validity would repeat the original error in a new place.
5. **The three back-test misses are all the same gate** (G2 workstreams, 3 novel mechanisms), all in
   the CONDITIONAL/MARGINAL band. Benign, but it means the rate is really 27/30 on one axis, not
   thirty independent trials.
6. **`probe-2027-manual.sh` remains untestable** until the season opens, and the 2027 Team Update
   watch has nothing on disk to exercise (phase 2 reported this cleanly rather than crashing).

## Verdict for the 2027-01-09 autorun

**GO, conditional.**

All four remediations under verification are genuinely fixed. Each was tested by re-deriving its
claim from the underlying data rather than by reading its patch note, and two of them
(priors, awards) turn out to be **more accurate than `REHEARSAL_GRADE.md` itself**. The back-test
guard held at 27/30 = 90 % before and after. The pipeline completes both phases against a
prior-season manual with zero crashes and leaves no poisoned artifact behind.

The one condition: **item 1 above should be closed before kickoff.** A geometric check that a
distracted operator can omit is the same class of defect as a geometric check that does not exist,
and it is the defect that earned the C−. It is a preflight change, it touches no rubric weight, and
it cannot move a ranking output.

Item 2 (the TBA back-test gate on the ranker) is correctly out of scope for a repair pass and should
be scheduled as new analysis before the ranking is trusted on a live season — but it does not block
the autorun, because `score-priors.py` now gives a reader everything needed to veto an
over-weighted channel by hand, and `CLAUDE.md` requires that check.
