# Rubric Back-test — does the achievability instrument actually predict what a 15-student team can build?

**Purpose:** [`ACHIEVABILITY-RUBRIC.md`](ACHIEVABILITY-RUBRIC.md) is only worth running on kickoff day
if it has been shown to reproduce outcomes it was not told. This file scores **all 30 archetypes**,
compares the ranking against **what actually happened** to small and mid teams in 2022–2026, reports a
**hit rate with the misses named and diagnosed**, **tunes** `achievability_rubric.yaml` in place to fix
the one systematic miss, and ends with the **worked end-to-end example** the team follows on
2027-01-09.

**Companion files:** [`05_rubric_backtest.yaml`](05_rubric_backtest.yaml) — machine-readable results,
changelog and uncertainty register · [`achievability_rubric.yaml`](achievability_rubric.yaml) — **the
file this pass edited (v1 → v2)** · [`../tools/score-strategy.py`](../tools/score-strategy.py) — the
scorer, patched to read the new graded-gate keys · [`archetype_corpus.yaml`](archetype_corpus.yaml) —
the 30-record test set.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus (manual text or scraped TBA data) |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model calibration. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

**Source shorthand**

`REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO · `CHRG` = 2023 CHARGED UP ·
`RAPD` = 2022 RAPID REACT (all in `manuals/archive/frc/_txt/`) ·
`RUB` = [`ACHIEVABILITY-RUBRIC.md`](ACHIEVABILITY-RUBRIC.md) / [`.yaml`](achievability_rubric.yaml) ·
`ARCH` = [`03_ARCHETYPE_CORPUS.md`](03_ARCHETYPE_CORPUS.md) / [`.yaml`](archetype_corpus.yaml) ·
`PF` = [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md) ·
`CAP` = [`02_TEAM_CAPACITY_MODEL.md`](02_TEAM_CAPACITY_MODEL.md) ·
`TBA` = `research/predictive_tba/tba_{copr,alliances}_{2023..2026}.csv`.

> **Scope guard.** BIOCORE presented by Haas is the **FRC 2027** game, kickoff **2027-01-09 12:00 ET**.
> BIOBUZZ is the **FTC** sibling game; "Pollen", StarterBots and Skill Builders are BIOBUZZ things and
> appear nowhere in this file. BIOCORE's rules and scoring element are **not public** as of 2026-08-22
> — see [`../research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md). **No number in
> this back-test is derived from a BIOCORE rule.** The `REB` worked example in §7 is a *template*, run
> against a manual that exists, so the team knows exactly what to do with a manual that does not yet.
> **2027 replaces the roboRIO with SystemCore**; §7's programming score prices that, §6 lists it as an
> open uncertainty.

---

## §0. The 60-second workflow — reproduce this whole file

```bash
# Run from the repository root.

# ---- 1. the tuned back-test (v2). This is the headline number. ------------------
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml
#   -> 30-row ranked table, the 2x2, then: agreement 27/30 = 90%

# ---- 2. the UNTUNED baseline (v1) -- the file is kept for exactly this ----------
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
       --rubric reference/.achievability_rubric.v1.bak
#   -> agreement 24/30 = 80%.   90 - 80 = what section 5's three tunes bought.

# ---- 3. the money sensitivity: does buying a fab account rescue anything? -------
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
       --set outsourced_2d_account=true
#   -> still 27/30. Money moves the binding constraint, it does not move the answer.

# ---- 4. one row, factor by factor ----------------------------------------------
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail R2
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail G1

# ---- 5. the independent TBA test of the VALUE axis (section 3.2) ----------------
#   below-median-COPR teams who are nonetheless top-quartile in ABSOLUTE auto or
#   endgame COPR: pick rate 45-56% against a 31-33% base rate. 2023-2025 only.
#   Script: tools/backtest_specialists.py  (written by this pass)
python tools/backtest_specialists.py
```

**Read the output in this order.** The **confusion matrix** (§4.1) first — it answers the only question
that matters on kickoff day, *"can this thing hand us a green light on a design that will kill the
season?"* Then the **three residual misses** (§4.3). The 90% headline **last**, and never on its own:
it is an in-sample number and §6 says why.

---

## §1. What a back-test of this kind can and cannot prove

| | Claim | Status |
|---|---|---|
| ✅ | The instrument is **internally consistent**: it reproduces 30 expert labels it was not given | Measurable, and measured below |
| ✅ | It is **strictly better than the predicate `ARCH` ships**: 90% vs 70% on `ARCH`'s own test set | Measured |
| ✅ | It **never issues a false green**: 0 of 12 T1 GREEN rows is anything but a hand-labelled YES | Measured — the safety property |
| ✅ | Its **value axis matches independent TBA data** it was never fitted to (§3.2) | Measured, 2023–2025, n ≈ 11,300 team-events |
| ❌ | It is **accurate out of sample** | **Not shown.** The anchors were calibrated against this set. §6 |
| ❌ | 90% is a **probability** the team will succeed | **No.** It is agreement with 30 hand labels, nothing more |
| ❌ | Anything here is **a BIOCORE claim** | **No.** The game is not public. §7 is a template, not a prediction |

The honest framing: **this is a regression test, not a validation study.** Its job is to stop the
instrument silently drifting when a weight is edited, and to make the *disagreements* visible so they
can be argued about. The out-of-sample test is 2027 — score the candidates on kickoff day, seal the
file, and reopen it in April.

---

## §2. Every archetype scored — the tuned (v2) ranked table

Verbatim `tools/score-strategy.py`, run 2026-08-22 on this machine, against the **tuned**
`achievability_rubric.yaml` (v2). Sorted by combined index, which is the ordering only — **the
quadrant is the decision.**

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml

======================================================================================================================
 BIOCORE ACHIEVABILITY x VALUE  --  ~15 students, 1 mentor, $2,500 discretionary, 599 effective h
======================================================================================================================
id   strategy                             ACH   VAL   idx  quadrant        tier        binding constraint              corpus
----------------------------------------------------------------------------------------------------------------------
C5   AUTO Specialist                     80.2  83.8  81.8  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
P5   QUINTET AUTO Specialist             83.3  78.3  81.0  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
R5   AUTO Specialist                     86.9  72.8  80.5  BUILD THIS      T1 GREEN    A7 programming_complexity = 1/5 YES
F5   AUTO Specialist                     80.2  78.3  79.3  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
G3   CHARGE STATION Specialist           82.7  74.1  78.9  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity = YES
C6   Defense Specialist                  86.4  65.2  76.8  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
F3   Processor Cycler                    73.2  75.2  74.1  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
F6   ALGAE Defender / Reef Clearer       81.0  65.2  73.9  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
P2   LOWER HUB Dumper                    93.7  49.0  73.6  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 4/5        YES
R2   Fixed-Zone Bulk Shooter             73.2  72.8  73.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
G4   HYBRID-Row Filler / LINK Facilita   90.6  49.0  71.9  CHEAP INSURANCE T1 GREEN    A6 graceful_degradation = 3/5   YES
R6   Shift Defender / HUB Denier         80.1  59.7  70.9  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
G5   Defense / Floor-Intake Support      81.0  56.9  70.2  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = CONDITIONAL
R3   Neutral-Zone Herder / Feeder        86.4  49.3  69.7  CHEAP INSURANCE T1 GREEN    A4 drive_practice_sensitivity = YES
R4   TOWER Climber Specialist (LEVEL 3   72.1  63.1  68.0  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity = YES
F2   L1 Trough Filler                    73.2  57.2  66.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
G1   Cube-Only Top-Row Cycler            51.2  80.7  64.5  TRAP            T2 STRETCH  A1 build_hours_fit = 1/5  [soft YES
C2   AMP Feeder / Amplification Manage   73.2  51.7  63.6  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 2/5        YES
C3   Subwoofer Camper (fixed-distance    70.2  54.8  63.3  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 2/5        YES
R8   Minimal Flawless (plow + LEVEL 1    87.9  32.4  62.9  CHEAP INSURANCE T1 GREEN    A4 drive_practice_sensitivity = YES
C1   SPEAKER Cycler (variable distance   37.3  89.0  60.6  TRAP            T4 GATED    GATE G2 WORKSTREAMS: 3 novel me CONDITIONAL
P4   MID-RUNG Climber + Low CARGO        73.2  40.7  58.6  CHEAP INSURANCE T2 STRETCH  A1 build_hours_fit = 2/5        YES
P1   UPPER HUB Cycler                    37.3  83.4  58.1  TRAP            T4 GATED    GATE G2 WORKSTREAMS: 3 novel me CONDITIONAL
F1   L4 Branch Specialist                30.8  89.0  57.0  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
F4   Deep CAGE Climber                   54.6  57.6  56.0  TRAP            T3 RED      A1 build_hours_fit = 1/5  [soft CONDITIONAL
C4   STAGE Climber + TRAP                53.7  57.6  55.5  TRAP            T3 RED      A1 build_hours_fit = 1/5  [soft CONDITIONAL
R7   Depot Cycler / Lift Dumper          45.0  61.0  52.2  TRAP            T4 GATED    GATE G2 WORKSTREAMS: 3 novel me MARGINAL
R1   Cycle Cannon (turreted high-rate    22.0  89.0  52.2  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
G2   Full-Grid CONE + CUBE Scorer        14.9  92.8  50.0  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
P3   TRAVERSAL Climber                   19.0  69.0  41.5  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
----------------------------------------------------------------------------------------------------------------------
 quadrant thresholds: ACH >= 60, VAL >= 55   |   tiers: T1 >= 62, T2 >= 48, T3 < 48, T4 = any hard gate
 combined index = 0.55*ACH + 0.45*VAL. RANK BY IT, DECIDE BY THE QUADRANT.

            +----------------------------------+----------------------------------+
            |            VALUE < 55            |            VALUE >= 55           |
            +----------------------------------+----------------------------------+
ACH >= 60   |         CHEAP INSURANCE          |            BUILD THIS            |
            |       P2 G4 R3 C2 C3 R8 P4       | C5 P5 R5 F5 G3 C6 F3 F6 R2 R6 G5 |
            |                                  |               R4 F2              |
            +----------------------------------+----------------------------------+
ACH <  60   |              DELETE              |               TRAP               |
            |                -                 | G1 C1* P1* F1* F4 C4 R7* R1* G2* |
            |                                  |                P3*               |
            +----------------------------------+----------------------------------+
  * = a hard gate fired; the quadrant is shown for information, the tier is T4 GATED.

--- Back-test against archetype_corpus.yaml hand labels ---

 agreement: 27/30 = 90%   (the corpus's own risk predicate scores 21/30 = 70%)

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
C1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
P1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
R7   MARGINAL      T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
```

### 2.1 The same 30, sorted by ACHIEVABILITY, against ground truth

The ranking test proper. `hand` = `ARCH`'s expert `small_team_verdict`; `outcome` = the competitive
result the archetype actually achieved somewhere, for some team, in that season **[C]**.

| # | id | season | ACH | VAL | idx | tier (v2) | hand | outcome | inv |
|--:|---|--:|--:|--:|--:|---|---|---|---|
| 1 | P2 | 2022 | 93.7 | 49.0 | 73.6 | T1 GREEN | YES | third-pick | I7 |
| 2 | G4 | 2023 | 90.6 | 49.0 | 71.9 | T1 GREEN | YES | third-pick | I7 |
| 3 | R8 | 2026 | 87.9 | 32.4 | 62.9 | T1 GREEN | YES | third-pick | I7 |
| 4 | R5 | 2026 | 86.9 | 72.8 | 80.5 | T1 GREEN | YES | **captain-tier** | I5 |
| 5 | C6 | 2024 | 86.4 | 65.2 | 76.8 | T2 STRETCH | YES | second-pick | I3 |
| 6 | R3 | 2026 | 86.4 | 49.3 | 69.7 | T1 GREEN | YES | second-pick | I6 |
| 7 | P5 | 2022 | 83.3 | 78.3 | 81.0 | T2 STRETCH | CONDITIONAL | **captain-tier** | I5 |
| 8 | G3 | 2023 | 82.7 | 74.1 | 78.9 | T1 GREEN | YES | second-pick | I4 |
| 9 | F6 | 2025 | 81.0 | 65.2 | 73.9 | T2 STRETCH | YES | second-pick | I3 |
| 10 | G5 | 2023 | 81.0 | 56.9 | 70.2 | T2 STRETCH | CONDITIONAL | third-pick | I3 |
| 11 | C5 | 2024 | 80.2 | 83.8 | 81.8 | T2 STRETCH | CONDITIONAL | **captain-tier** | I5 |
| 12 | F5 | 2025 | 80.2 | 78.3 | 79.3 | T2 STRETCH | CONDITIONAL | **captain-tier** | I5 |
| 13 | R6 | 2026 | 80.1 | 59.7 | 70.9 | T2 STRETCH | YES | second-pick | I3 |
| 14 | F3 | 2025 | 73.2 | 75.2 | 74.1 | T1 GREEN | YES | **first-pick** | I1 |
| 15 | R2 | 2026 | 73.2 | 72.8 | 73.0 | T1 GREEN | YES | **first-pick** | I1 |
| 16 | F2 | 2025 | 73.2 | 57.2 | 66.0 | T1 GREEN | YES | second-pick | I6 |
| 17 | C2 | 2024 | 73.2 | 51.7 | 63.6 | T1 GREEN | YES | second-pick | I6 |
| 18 | P4 | 2022 | 73.2 | 40.7 | 58.6 | T2 STRETCH | YES | second-pick | I7 |
| 19 | R4 | 2026 | 72.1 | 63.1 | 68.0 | T1 GREEN | YES | second-pick | I4 |
| 20 | C3 | 2024 | 70.2 | 54.8 | 63.3 | T1 GREEN | YES | second-pick | I7 |
| 21 | F4 | 2025 | 54.6 | 57.6 | 56.0 | T3 RED | CONDITIONAL | second-pick | I4 |
| 22 | C4 | 2024 | 53.7 | 57.6 | 55.5 | T3 RED | CONDITIONAL | second-pick | I4 |
| 23 | G1 | 2023 | 51.2 | 80.7 | 64.5 | T2 STRETCH | YES | **first-pick** | I1 |
| 24 | R7 | 2026 | 45.0 | 61.0 | 52.2 | **T4 GATED** | MARGINAL | third-pick | I1 |
| 25 | C1 | 2024 | 37.3 | 89.0 | 60.6 | **T4 GATED** | CONDITIONAL | **event-winning** | I1 |
| 26 | P1 | 2022 | 37.3 | 83.4 | 58.1 | **T4 GATED** | CONDITIONAL | **event-winning** | I1 |
| 27 | F1 | 2025 | 30.8 | 89.0 | 57.0 | T4 GATED | NO | event-winning | I1 |
| 28 | R1 | 2026 | 22.0 | 89.0 | 52.2 | T4 GATED | NO | event-winning | I1 |
| 29 | P3 | 2022 | 19.0 | 69.0 | 41.5 | T4 GATED | NO | first-pick | I4 |
| 30 | G2 | 2023 | 14.9 | 92.8 | 50.0 | T4 GATED | NO | event-winning | I2 |

**Spearman rank correlations, computed over all 30 records:**

| Pair | ρ | Reading |
|---|--:|---|
| ACHIEVABILITY vs hand verdict (YES=0 … NO=3) | **−0.709** | Strong. Higher achievability → more likely hand-labelled buildable. **This is the load-bearing correlation** |
| VALUE vs corpus outcome (event-winning=0 … unpicked=5) | **−0.899** | Strong — but **partly circular**: the corpus auto-scorer derives V3 and V5 *from* `outcome`. See §6.4 |

**The single most important line in the table** is the top-to-bottom shape of the `inv` column: the
top 20 rows are I3/I4/I5/I6/I7 — defense, endgame, AUTO, feeder, minimal — and the bottom 7 are all
I1-at-full-spec plus the one I2. The rubric was never told about invariants. It reconstructed `ARCH`'s
central finding from 13 capacity factors.

---

## §3. What actually happened — the rubric's ranking against reality

### 3.1 Corpus ground truth, grouped

`ARCH` records, for each archetype, the **best competitive outcome it is known to have produced**
**[C]** and an expert **small-team verdict** **[H]/[S]**. Grouping the 30 by what the rubric said:

| Rubric said | n | Corpus outcomes in that group | Hand verdicts |
|---|--:|---|---|
| **T1 GREEN** (build it) | 12 | 1 captain-tier, 2 first-pick, 6 second-pick, 3 third-pick | **12 YES, 0 anything else** |
| **T2 STRETCH** (buy an enabler) | 7 | 3 captain-tier, 1 first-pick, 3 second/third-pick | 5 YES, 4 CONDITIONAL *(9 rows incl. G1, P4)* |
| **T3 RED** (do not build) | 2 | 2 second-pick | 2 CONDITIONAL |
| **T4 GATED** (cannot be built here) | 7 | 4 event-winning, 1 first-pick, 1 third-pick | 4 NO, 2 CONDITIONAL, 1 MARGINAL |

Three things follow:

1. **Nothing the corpus calls anything but YES ever reaches T1 GREEN.** Zero false greens in 30. On
   kickoff day the failure mode that ends a season is a green light on a design that eats it — that
   rate is measured at **0/12** here.
2. **T4 GATED is where the event-winning robots are.** Four of the seven gated archetypes *won
   events*. That is not a contradiction, it is the point: `ARCH`'s **I1-at-full-spec is 0/4 for small
   teams** and **6/9 restricted to the fixed-range variant**. The gate is saying *"that robot wins
   events, and not for you, as specified"* — and §5's descope prompt says what to score instead.
3. **The rubric is conservative on the way down, not on the way up.** Both T3 RED rows (F4, C4) are
   hand-labelled CONDITIONAL and did reach second-pick. Cost of the error: two endgame designs the
   team would skip. Cost of the opposite error: a season.

### 3.2 An independent test the rubric was never fitted to — TBA component COPRs **[C]**

The corpus labels are expert judgement. This is not. From `TBA` component-COPR data, for every
team-event where the team's **total COPR was below the event median** — i.e. a team that is not a
high-volume scorer, which is the profile this rubric is built for — what happens to their alliance-
selection rate if they are nonetheless **top-quartile at that event in absolute AUTO COPR** or
**absolute ENDGAME COPR**?

```
$ python tools/backtest_specialists.py

yr    n_below_med  base_pick  hiAUTOabs      n   hiENDabs      n   neither      n
2023         3566      32.9%      53.5%     99      43.2%    475     30.7%   3000
2024         3763      30.7%      45.5%    110      45.4%    425     28.5%   3244
2025         3960      31.8%      54.7%    150      55.7%    366     28.6%   3461
2026            1       nan%       nan%      0       nan%      0      nan%      0
```

| Season | Base pick rate, below-median-COPR team | Top-quartile **AUTO** COPR | Top-quartile **ENDGAME** COPR | Neither |
|---|--:|--:|--:|--:|
| 2023 `CHRG` | 32.9% (n=3,566) | **53.5%** (n=99) | **43.2%** (n=475) | 30.7% |
| 2024 `CRES` | 30.7% (n=3,763) | **45.5%** (n=110) | **45.4%** (n=425) | 28.5% |
| 2025 `REEF` | 31.8% (n=3,960) | **54.7%** (n=150) | **55.7%** (n=366) | 28.6% |
| 2026 `REB` | — | — | — | — |

**Reading.** A below-median-scoring robot that is top-quartile in *absolute* auto output is picked
**1.4–1.7× more often** than its peers, in every season measured. Same for endgame. This is a direct,
independent confirmation of the two archetype families the rubric ranks highest:

- **I5 AUTO Specialist** — rubric rows **C5 (81.8), P5 (81.0), R5 (80.5), F5 (79.3)**: the four
  highest combined indices in the entire file. `ARCH` calls it *"the best points-per-dollar play in the
  corpus."* TBA says a small team that does it is picked 45–55% of the time against a 31% base.
- **I4 Endgame Specialist** — rubric rows **G3 (78.9), R4 (68.0)**. Same magnitude of lift.

**Caveats, stated plainly.** ⓐ **2026 `REB` produces no rows** — the scraped `tba_copr_2026.csv` has
empty `auto`/`teleop`/`endgame` columns for all 8,160 team-events (TBA's 2026 score-breakdown keys
differ from 2023–2025); the test therefore covers three seasons, not four, and **not** the season the
corpus calibrates on. ⓑ Component COPR cannot distinguish *"deliberately specialised"* from *"only
managed to do the auto"*. ⓒ Being picked is not the same as being *useful* — but `PF` measures
`pct_picked` as the terminal outcome the whole corpus predicts, so it is the right dependent variable.
ⓓ Selection effects: teams that are good at auto may be good generally in ways total COPR under-
measures. This is **suggestive [C] evidence, not a causal claim.**

### 3.3 What small teams attempted and failed — the counter-evidence

| Archetype | What happened | Rubric verdict | Agrees? |
|---|---|---|---|
| **G2** Full-Grid CONE + CUBE (`CHRG`, I2) | The do-everything robot. `ARCH`: **0/5 small-team success across five seasons** | ACH **14.9** — lowest in the file; T4 GATED on CNC | ✅ and by the largest margin available |
| **R1** Cycle Cannon (`REB`, I1 full spec) | Event-winning **for resourced teams**. `ARCH`: *"where 15-student teams lose the season"* | ACH 22.0, T4 GATED | ✅ |
| **P3** TRAVERSAL Climber (`RAPD`, I4) | First-pick, and the highest-risk endgame in five seasons | ACH 19.0, T4 GATED, lowest index (41.5) | ✅ |
| **F1** L4 Branch Specialist (`REEF`) | Event-winning; CNC, 3 mechanisms, $2,600 | ACH 30.8, T4 GATED on CNC **and** G3 budget | ✅ |
| **G1** Cube-Only Top-Row (`CHRG`) | **First-pick, and hand-labelled YES** — a genuine small-team success | v1 said T4 GATED ✗ · **v2 says T2 STRETCH** ✓ | fixed in §5 |
| **R7** Depot Cycler (`REB`) | Third-pick, MARGINAL | T4 GATED — **still a miss**, §4.3 | ❌ |

### 3.4 The base rate that makes all of this actionable **[C]**

From `ARCH` `base_rates`, derived from `TBA`: the share of **event-winning alliances that carried a
below-median-OPR robot** is **64% (2023) · 69% (2024) · 68% (2025) · 78% (2026)**, and the share of
**rank-1 seeds** that did is **71 · 68 · 71 · 81%**. The second- and third-pick slots the rubric's
T1 GREEN population targets are the **statistically normal** route onto a winning alliance for this
team, not a consolation prize. *(Upper bound: OPR percentile cannot tell a deliberate support robot
from a broken one.)*

---

## §4. Hit rate — where the rubric was right, and where it missed

### 4.1 The confusion matrix (v2, tuned)

Agreement mapping, from `score-strategy.py`: `YES → {T1,T2}` · `CONDITIONAL → {T2,T3}` ·
`MARGINAL → {T2,T3}` · `NO → {T3,T4}`.

| rubric ↓ / hand → | YES | CONDITIONAL | MARGINAL | NO |
|---|--:|--:|--:|--:|
| **T1 GREEN** | **12** | 0 | 0 | 0 |
| **T2 STRETCH** | **5** | **4** | 0 | 0 |
| **T3 RED** | 0 | **2** | 0 | 0 |
| **T4 GATED** | 0 | *2* | *1* | **4** |

**Hit rate: 27/30 = 90%.** (Baseline: v1 rubric 24/30 = 80%; `ARCH`'s own four-term risk predicate
21/30 = 70%.) The matrix is **monotone** — every off-diagonal cell is adjacent to the diagonal — and
the three errors are all in one cell, over-gating.

**Error asymmetry, which is the design intent:**

| Error type | Count | Consequence |
|---|--:|---|
| **False GREEN** (rubric says build, corpus says don't) | **0 / 30** | Would be a lost season. Does not occur |
| **False GATE** (rubric says impossible, corpus says conditional) | **3 / 30** | A design skipped that a determined team could have run. Recoverable |

### 4.2 Hit rate by season and by invariant

| Season | n | hits | rate | Misses |
|---|--:|--:|--:|---|
| 2026 `REB` | 8 | 7 | 88% | R7 |
| 2025 `REEF` | 6 | 6 | **100%** | — |
| 2024 `CRES` | 6 | 5 | 83% | C1 |
| 2023 `CHRG` | 5 | 5 | **100%** | — |
| 2022 `RAPD` | 5 | 4 | 80% | P1 |

| Invariant | n | hits | rate |
|---|--:|--:|--:|
| I1 reliable high-volume single-task scorer | 9 | 6 | **67%** ← all three misses live here |
| I2 do-everything | 1 | 1 | 100% |
| I3 defense specialist | 4 | 4 | 100% |
| I4 endgame specialist | 6 | 6 | 100% |
| I5 AUTO specialist | 4 | 4 | 100% |
| I6 feeder / support | 3 | 3 | 100% |
| I7 minimal flawless | 4 | 4 | 100% |

**Diagnosis in one line: the instrument is at 100% everywhere except I1, the family where the whole
question is *"which variant of this?"* — which is precisely the failure mode `ARCH` predicted for any
predicate that scores the family instead of the variant.**

### 4.3 The three residual misses, each diagnosed

| id | Design | Hand | Rubric | Fired |
|---|---|---|---|---|
| **C1** | `CRES` SPEAKER Cycler (variable distance) | CONDITIONAL | T4 GATED | G2 WORKSTREAMS: 3 novel mechanisms > max 2 |
| **P1** | `RAPD` UPPER HUB Cycler | CONDITIONAL | T4 GATED | G2 WORKSTREAMS: 3 novel mechanisms > max 2 |
| **R7** | `REB` Depot Cycler / Lift Dumper | MARGINAL | T4 GATED | G2 WORKSTREAMS: 3 novel mechanisms > max 2 |

**All three are the same miss.** Every one is a `mechanism_count: 3` design that G2 rejects.

**Root cause — a missing factor, not a bad weight.** The corpus auto-scorer maps
`novel_mechanisms := mechanism_count`, and `ARCH`'s own schema defines `mechanism_count` as
*"powered subsystems BEYOND the drivetrain"* — **not** *"subsystems this team must invent."* For C1,
the intake and the flywheel had released, documented, copyable precedents by 2024; only the variable-
range indexer/aim stack was genuinely novel. G2's constant is right (`novel_mechanisms_max = 2` is
derived four independent ways in `CAP` §5.2 and §6.3); **its input is wrong.**

**Why this pass did not "fix" it.** The correct fix is
`novel_mechanisms = mechanism_count − (mechanisms with a released COTS or open design)`, which
requires a per-mechanism COTS field that **`archetype_corpus.yaml` does not have** — the same gap
`RUB`'s own limitations already confess (*"A10 `cots_availability` has no source field in
`archetype_corpus.yaml`, and is proxied from `mfg_floor`; it is the weakest mapping in the
instrument"*). Fabricating that field for 30 records to move a number from 27 to 30 would be **tuning
the test set, not the instrument.** It stays a miss, and §6.1 states what would resolve it.

**Consolation: on a real candidate, this miss cannot occur**, because a human scoring a real design
against `RUB` §2 A2's five-part tie-break test (*"its own design decision, its own prototype→test→revise
loop, its own fab-queue slot, its own unsupervised student lead, its own integration failure mode"*)
already answers the COTS question. The miss is an artefact of the auto-scorer, which `RUB` explicitly
labels *"a regression-test harness, not a scoring method."*

### 4.4 Misses that v1 had and v2 fixed

| id | Hand | v1 tier | v2 tier | Why v1 was wrong |
|---|---|---|---|---|
| **G1** `CHRG` Cube-Only Top-Row Cycler | YES | T4 GATED (G1 router) | **T2 STRETCH** ✓ | A `router` floor is not a capability wall — 2D profile cutting is buyable as a service. And its 243 h estimate is 19% over a pool whose input `ARCH` itself brackets at ±40% |
| **F4** `REEF` Deep CAGE Climber | CONDITIONAL | T4 GATED (G1 router) | **T3 RED** ✓ | Same |
| **C4** `CRES` STAGE Climber + TRAP | CONDITIONAL | T4 GATED (G1 router) | **T3 RED** ✓ | Same |

---

## §5. The tune — changelog, before/after, and what each change is worth

Three changes, all in [`achievability_rubric.yaml`](achievability_rubric.yaml), **plus** a
backwards-compatible patch to `tools/score-strategy.py` so it reads the new keys. The v1 file is kept
verbatim at `reference/.achievability_rubric.v1.bak` and the v1 scorer at
`tools/.score-strategy.py.pretune.bak`, so every "before" number in this document is re-runnable.

### 5.1 Changelog

| # | Key | v1 | v2 | Principle it enforces | Evidence |
|---|---|---|---|---|---|
| **A** | `gates.checks[G1].grading` | *(absent — floor was a binary)* | `hard_floors: [CNC]`, `soft_floors: [router]`, one-tier downgrade | A gate must distinguish *"a machine that cannot be bought as a service"* from *"a machine that can."* CNC mill/lathe on a load-bearing part is the former; 2D profile cutting is the latter | **[S]**, implementing `ARCH`'s own stated fix: *"make mfg_floor a graded term rather than a binary"* |
| **B** | `gates.checks[G4].soft_band_multiplier` | *(absent, effectively 1.0)* | **1.25** — hard above 256 h, soft between 205 h and 256 h | **A hard gate must not fire inside its own input's error bar.** `CAP` calls `hours_per_novel_mechanism = 90` *"deliberately generous"*; `ARCH` states its effort/cost bands are **±40%**. 205 < est ≤ 256 h is not *"unbuildable"*, it is *"needs an enabler bought"* — which is the definition of T2 STRETCH | **[S]** |
| **C** | `gates.soft_downgrade_max_tiers` | *(absent, unbounded stacking)* | **1** | T2 STRETCH already **means** *"possible only if you buy a specific named enabler."* Two soft flags = two enablers, still STRETCH. Stacking to T3 RED asserts un-buildability, which is what a **hard** gate is for | **[S]** |
| **D** | `meta.version` | 1 | **2**, + `tuned:` and `tuning_record:` fields | Provenance | — |

**What was NOT changed, deliberately:** every one of the 13 achievability weights, all 5 value
weights, the 0.55/0.45 split, the 60/55 quadrant thresholds, the 62/48 tier cuts, the no-zeros rule,
and gates G2/G3/G5/G6. **No weight was touched.** A weight change would be indistinguishable from
curve-fitting the test set; a gate *grading* change is a statement about the physical world that is
checkable independently of the 30 records.

### 5.2 Scorer patch (required to read the new keys — defaults reproduce v1 exactly)

| Function | Change |
|---|---|
| `run_gates()` | Now returns `(hard_gates, soft_gates)` instead of `(hard_gates, bool)`. Reads `G1.grading.soft_floors` (default `[]` → v1 behaviour) and `G4.soft_band_multiplier` (default `1.0` → v1 behaviour). G6 became an entry in the same soft list |
| `evaluate()` | Applies `min(len(softs), gates.soft_downgrade_max_tiers)` one-tier downgrades (default cap `99` → v1 behaviour) |
| `print_detail()` | Prints every soft gate with its reason, instead of a hardcoded G6 line |
| binding-constraint string | `[+G6 drive-hours]` → `[soft G1,G4,G6]`, listing whichever fired |

**Backwards-compatibility was verified before the yaml was edited:** the patched scorer run against
the *unmodified* v1 yaml reproduces `agreement: 24/30 = 80%` and an identical 30-row table.

### 5.3 Before / after

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
        --rubric reference/.achievability_rubric.v1.bak      # v1, UNTUNED
 agreement: 24/30 = 80%

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
G1   YES           T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
C1   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
P1   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
F4   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
C4   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
R7   MARGINAL      T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['

$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml   # v2, TUNED
 agreement: 27/30 = 90%

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
C1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
P1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
R7   MARGINAL      T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
```

| Metric | v1 | v2 | Δ |
|---|--:|--:|--:|
| Agreement with 30 hand labels | 24/30 = 80% | **27/30 = 90%** | **+3** |
| False GREEN rate | 0/12 | **0/12** | unchanged — the safety property held |
| Rows changing tier | — | **6** (G1, F4, C4 fixed; C1, P1, R7 re-diagnosed to a different gate) | |
| Distinct root causes among misses | 1 (router) | **1 (novel-mechanism counting)** | The tune converted one systematic error into a different, smaller, named one |
| `ARCH` predicate baseline | 21/30 = 70% | 21/30 = 70% | — |

**The re-diagnosis is worth as much as the fix.** C1, P1 and R7 are still misses — but v1 said
*"you need a machine you do not own"* (relaxable with money, `CAP` constraint **#5 of 5**) and v2 says
*"you need more unsupervised student leads than you have"* (`CAP` constraint **#2**, in-season
elasticity **None**). The second statement is the true one, and it is the one that changes what the
team does in the fall.

### 5.4 Sensitivity: does buying the outsourced-fabrication account change the answer?

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
        --set outsourced_2d_account=true
 agreement: 27/30 = 90%
 misses: C1, P1, R7  -- all GATE G2 WORKSTREAMS
```

**Unchanged, and that is the finding — now stronger than it was in v1.** In v1, flipping this constant
moved the misses' binding constraint from G1 to G4/G2. In v2 the router grading has *already* absorbed
the machine question, so buying the account moves **nothing at all**: the surviving blocker was never
money. `CAP` §7.1's constraint hierarchy — mentor attention #1, unsupervised leads #2, effective hours
#3, machines #4, **money #5** — is reproduced by the rubric from a completely independent direction.

---

## §6. Genuinely uncertain cases — and what would resolve each

Five. Each is a real hole, and each has a named, cheap, *pre-kickoff* resolution.

### 6.1 The novel-mechanism count (C1 / P1 / R7) — **the live one**

**Uncertainty.** Is a 3-mechanism design 3 novel workstreams, or 2 novel + 1 copied? G2 currently
assumes the former, which makes it the strictest gate in the instrument and the source of all three
residual misses.

**What would resolve it.** Add a per-mechanism `cots_status: [released_design | vendor_kit | bespoke]`
field to `archetype_corpus.yaml` for all 30 records and set
`novel_mechanisms = count(bespoke)`. **Cost: about two hours** against the five manuals plus the
mechanism catalog already on disk at [`bom/06_MECHANISM_CATALOG.md`](bom/06_MECHANISM_CATALOG.md).
**Do this before kickoff, not on kickoff day**, and re-run this file. If agreement goes to 30/30 the
diagnosis was right; if it does not, G2's constant is the thing to question. **[S]**

### 6.2 F4 and C4 at T3 RED — over-correction or correct caution?

**Uncertainty.** The `REEF` Deep CAGE Climber and the `CRES` STAGE Climber + TRAP both landed at
T3 RED (indices 56.0 and 55.5 — *inside* the 48–62 STRETCH band, pushed down by one soft downgrade).
The mapping counts CONDITIONAL → {T2, T3} so they score as hits, but a T3 RED on a design that reached
second-pick is uncomfortable. Both are I4 endgame designs, and I4 is otherwise 6/6.

**What would resolve it.** Two things, both checkable: ⓐ how many *parts* actually need the router
floor — `RUB` §2 A9's own tie-break says *"one router part is a purchase order, eight is a fabrication
programme"*, and neither corpus record states a part count; ⓑ whether soft-gate downgrades should
apply **below** the T1 boundary at all, given they encode *"buy an enabler"* and T3 RED means *"do not
build"*. A defensible v3 change is to make soft downgrades apply only to T1→T2. **Not made in this
pass** — it moves nothing on the current test set, so there is no evidence to choose it. **[S]**

### 6.3 The AUTO specialists' A7 = 0 under SystemCore

**Uncertainty.** C5, P5 and F5 are held at **T2 STRETCH** solely by the no-zeros rule firing on
`A7 programming_complexity = 0/5`, which is itself produced by the `systemcore_adjustment` table. If
SystemCore + WPILib 2027 turn out to be *easier* than the mature roboRIO stack for path-following
autos, these three become T1 GREEN and the rubric's top-4 rows all turn green at once. If SystemCore
hardware **has not shipped at kickoff**, they get worse, not better — `RUB` §11 already floors A13 at
1 in that case.

**What would resolve it.** Three dated, checkable facts, all before kickoff: **(i)** has SystemCore
hardware shipped to teams; **(ii)** does WPILib 2027 ship a working path-follower on SystemCore;
**(iii)** is the roboRIO still legal in 2027 (**UNVERIFIED** as of 2026-08-22). This is the single
largest source of variance in the whole instrument, because it moves the family with the four highest
combined indices. **[C]** that the control system changes; **[S]** on the direction of the difficulty
delta.

### 6.4 The VALUE-axis correlation is partly circular

**Uncertainty.** ρ = −0.899 between VALUE and corpus `outcome` looks like a triumph and is not one:
the corpus auto-scorer derives **V3 `alliance_selection_appeal`** and **V5 `ceiling`** *directly from*
the `outcome` field (`V3_from_outcome`, `V5_from_outcome` in the yaml). Those two carry 120 of the 290
value weight — **41%**. The genuinely independent parts of that correlation are V1 (points/match, from
`points_per_cycle × cycles`) and V2/V4.

**What would resolve it.** Recompute ρ using **V1 only** against `outcome`, and separately re-derive
V3 from `TBA` pick data rather than from the corpus label. The §3.2 TBA test is the first instalment
of exactly that and it holds up — but it tests the *archetype family*, not the per-record V3.
**Treat the −0.899 as decoration; the load-bearing number is ACH ρ = −0.709.** **[S]**

### 6.5 2026 `REB` is absent from the only non-circular test

**Uncertainty.** §3.2's component-COPR test — the one piece of evidence in this file that was never
fitted to anything — covers 2023–2025 only, because `tba_copr_2026.csv` has empty
`auto`/`teleop`/`endgame` columns for **all 8,160** team-events. 2026 is the corpus's
`primary_calibration_season` and the manual `ARCH` says BIOCORE most plausibly resembles, so the
season that matters most is the one missing from the independent test.

**What would resolve it.** Re-run `tools/tba_copr_scrape.py` with the 2026 score-breakdown keys mapped
(the `REB` breakdown does not use the 2023–2025 `autoPoints`/`endGamePoints` names). Verify against
`manuals/archive/frc/_txt/2026_REBUILT.txt` Table 6-4 for which fields exist. **Cost: under an hour.**
Until then, §3.2 is a **three-season** result. **[C]** that the data are missing; **[S]** that the 2026
result would match.

---

## §7. Worked end-to-end example — `REB` 2026, the template for kickoff day

This is the exact sequence to run on **2027-01-09** with the BIOCORE manual open. It is worked against
the **2026 REBUILT** manual, which exists and is on disk, so every step is real. **Nothing below is a
BIOCORE claim.**

### 7.1 Step 1 — the manual excerpt (20 minutes, two people, before anyone draws anything)

From the 2026 REBUILT manual **[C]**, cut to what this step needs. The full text is
`manuals/archive/frc/_txt/2026_REBUILT.txt`, which is not in the repository because FIRST's text is
not redistributed; `bash tools/rebuild-corpus.sh` rebuilds it locally.

> **§6.4.1 HUB Status (p. 44):** *"FUEL scored in an active HUB is worth MATCH points but FUEL scored
> in an inactive HUB will not earn any points… During the ALLIANCE SHIFTS, only one ALLIANCE HUB will
> be active while the other ALLIANCE'S HUB becomes inactive."* Both HUBs are active during AUTO, the
> TRANSITION SHIFT and END GAME.

> **Table 6-4 (scoring)** — FUEL in an active HUB: **1 point** (AUTO and TELEOP). FUEL in an inactive
> HUB: **0**. TOWER: LEVEL 1 **15** AUTO / **10** TELEOP (max 2 robots in AUTO), LEVEL 2 **20**,
> LEVEL 3 **30**.

> **Table 6-5 (BONUS RP thresholds)** — ENERGIZED **100** at Regional/District · SUPERCHARGED **360** ·
> TRAVERSAL **50**.

Plus, from `ARCH` `season_facts.2026` **[C]**: HUB opening **72 in** off the carpet, **41.7 in**
hexagonal, **158.6 in** from the alliance wall; **504** FUEL staged per match; **no possession cap**;
AUTO 20 s, TELEOP 140 s; own HUB active for **~110 s of 160** **[S]**.

**The eight `RUB` §11 slots this fills:** `median_alliance_score_estimate` = **147** (`ARCH`
`base_rates`, 2026) · `scoring_table_rows` = **7** · `auto_gated_ranking_point` = **no** ·
`protected_zone_rule_count` = **1** (TOWER only) · `one_defender_at_a_time` = **no** ·
`pin_count_seconds` = **3** · `foul_values_minor_major` — read from §8 · `systemcore_shipping` = n/a
for 2026.

### 7.2 Step 2 — the candidate strategy, written as a *variant*, not a family

> **R2 · Fixed-Zone Bulk Shooter.** A floor intake feeds a single fixed-angle flywheel by gravity and
> a roller — **no powered indexer, no turret, no hood articulation**. The robot drives to **one
> surveyed spot** in the neutral zone, dumps its load into the active HUB in a burst, and returns.
> One hood angle, one RPM setpoint, encoder feedback only. 2 mechanisms beyond the drivetrain.
> **~12 points per trip × 5 trips = 60 points/match.**

The **descoped variant** of `ARCH` I1 — and the whole trick. Write **"turreted variable-range shooter"**
and **"fixed-position bulk shooter"** as **two rows**, never one. `ARCH` measures I1 at **0/4 at full
spec and 6/9 restricted to the fixed-range variant**. The full-spec sibling on this same test set is
**R1 Cycle Cannon: ACH 22.0, T4 GATED.**

### 7.3 Step 3 — factor by factor, with the justification written down

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail R2

==============================================================================
 R2  Fixed-Zone Bulk Shooter
==============================================================================
 ACHIEVABILITY 73.2   VALUE 72.8   index 73.0   BUILD THIS   T1 GREEN
 points/match 60.0  (share of median 0.41)   source: corpus points_per_cycle x cycles

factor                              w  score     w*s  deficit
--------------------------------------------------------------
A1 build_hours_fit                 85      2     170      255
A2 parallel_workstream_demand      85      3     255      170
A3 mentor_supervision_load         80      4     320       80
A4 drive_practice_sensitivity      90      3     270      180
A5 reliability_exposure            88      4     352       88
A6 graceful_degradation            66      5     330        0
A7 programming_complexity          70      4     280       70
A8 sensing_vision_dependence       30      5     150        0
A9 manufacturing_floor             45      4     180       45
A10 cots_availability              55      4     220       55
A11 iteration_count                60      4     240       60
A12 marginal_cost                  40      3     120       80
A13 schedule_critical_path_risk    62      4     248       62
--------------------------------------------------------------
V1 points_per_match_share          80      4     320
V2 rp_contribution                 55      4     220
V3 alliance_selection_appeal       75      4     300
V4 defense_resistance              35      1      35
V5 ceiling                         45      4     180
--------------------------------------------------------------
 BINDING CONSTRAINT: A1 build_hours_fit = 2/5
```

**Every score, justified against the `RUB` §2 anchor. This is the column the team argues about.**

| # | Factor | w | s | Justification against the anchor |
|---|---|--:|:-:|---|
| **A1** | build_hours_fit | 85 | **2** | 2 mechanisms at `90 h × 0.8` bandsaw factor + `15 h × 2` programming ≈ **174 h**. Anchor 2 = "≤205 h, exactly consumes the pool, nothing left for overrun." **This is the binding constraint** |
| **A2** | parallel_workstream_demand | 85 | **3** | 1 new stream — this *is* the primary scoring mechanism, the second of the three mandatory ones. Anchor 3. Normal, not free |
| **A3** | mentor_supervision_load | 80 | **4** | `40 min × 2 mechanisms = 80 min/wk`, no machine supervision beyond the bandsaw. 39% of the 204 min budget → anchor 4 ("a check-in and a design review") |
| **A4** | drive_practice_sensitivity | 90 | **3** | `med`. One repeated path to one surveyed spot; a driver learns it in 2–3 h. Tie-break: at 9 h seat time we get ~50% of ceiling → 3. **Highest weight in the instrument** |
| **A5** | reliability_exposure | 88 | **4** | Serial chain = intake → flywheel. `0.93² = 0.865` → anchor 4 (0.85–0.89). *Write the element list, then compute* |
| **A6** | graceful_degradation | 66 | **5** | `ARCH`: *"One setpoint, one distance. Failure = the burst misses until the driver re-acquires the spot. GRACEFUL."* Rate drops, scoring continues |
| **A7** | programming_complexity | 70 | **4** | Base difficulty 2, sensing `encoders` → SystemCore delta **+0.0**. Adjusted ≈ 2 → anchor 4. **For BIOCORE, add +0.5 if any closed loop and +1.0 if odometry, and treat vision as unavailable in weeks 1–3** |
| **A8** | sensing_vision_dependence | 30 | **5** | Encoders only. Nothing to stop working if the coprocessor never boots |
| **A9** | manufacturing_floor | 45 | **4** | `bandsaw+drill` on stock tube/plate. Owned — but one of each, so queue contention with the drivetrain stream |
| **A10** | cots_availability | 55 | **4** | Vendor sells the hard part (flywheel gearbox, compliant rollers) and build guides exist; the geometry around it is ours. **Score this by hand — the corpus proxies it from `mfg_floor` and it is the weakest mapping in the instrument** |
| **A11** | iteration_count | 60 | **4** | ~2 fabricating loops: one rough shooter to find the setpoint, one final. Ball-handling would push this to 3 if the game piece is compliant |
| **A12** | marginal_cost | 40 | **3** | `$600–1,100` band; use the **high** end → $1,100, roughly half the $2,500 discretionary. Anchor 3 |
| **A13** | schedule_critical_path_risk | 62 | **4** | One dependency (the gearbox order), satisfiable from stock or a 1-week lead. **In 2027 this floors at 1 if SystemCore has not shipped** |
| **V1** | points_per_match_share | 80 | **4** | 60 pts against a 2026 median alliance score of **147** = **0.41**. Anchor band 0.30–0.44 → 4. Above the 0.33 one-robot-of-three parity line |
| **V2** | rp_contribution | 55 | **4** | ENERGIZED needs **100** FUEL (Table 6-5); 60/match is a countable share the alliance reaches together, and two such robots clear it alone |
| **V3** | alliance_selection_appeal | 75 | **4** | Corpus outcome `first-pick`. *Captains buy points* — `PF` measures Avg Match as the best separator of picked from unpicked, AUC 0.801–0.872, all four seasons |
| **V4** | defense_resistance | 35 | **1** | **The exposure, priced in the same row as the strength.** One surveyed shooting position is exactly what a defender parks on. `REB`'s neutral zone is unrestricted — only the TOWER is protected |
| **V5** | ceiling | 45 | **4** | First/second-pick tier; practice keeps paying but plateaus once the setpoint is dialled |

### 7.4 Step 4 — the quadrant and the tier

| | |
|---|---|
| **ACHIEVABILITY** | **73.2** (≥60) |
| **VALUE** | **72.8** (≥55) |
| **Quadrant** | **Q1 · BUILD THIS** |
| Combined index | 73.0 — *ordering only* |
| Hard gates | none. `bandsaw+drill` owned · 2 mechanisms = max · $1,100 < $2,500 · 174 h < 205 h · 80 min < 204 min |
| Soft gates | none. `A4 = 3`, not 0, so G6 does not fire |
| Zeros | none |
| **Tier** | **T1 GREEN** |
| **Binding constraint** | **A1 `build_hours_fit` = 2/5** — weighted deficit **255**, the largest in the row |

**What the binding constraint means, and it is not what the team expects.** At ~174 h against a 205 h
pool, the thing that will beat this design is **hours**, not money and not difficulty. The lever is
therefore the **event week, not the design**: `CAP` §7.4 measures Week 1 → Week 4 as **+255 effective
hours, free**. Round-1 event preferencing opens **2026-09-24**. *The highest-leverage decision on this
robot is made four months before anyone touches it.*

**Q1 decision rule, applied:** commit on kickoff weekend · **unsupervised lead assigned by day 3** ·
**CAD-freeze by day 10** · second mechanism only if `novel_mechanisms_max` still has room after the
2027 deductions (vision pose-estimation **or** a first-year swerve adoption each drop it from 2 to 1;
both together drop it to **0**).

### 7.5 Step 5 — two recommended awards

Award names verified against [`awards/00_AWARD_LIST_EMPIRICAL_2026.md`](awards/00_AWARD_LIST_EMPIRICAL_2026.md),
which is built from real TBA 2026 award records **[C]**. Do **not** paraphrase an award name in a
submission.

| Award | 2026 events offering it **[C]** | Why this robot, specifically |
|---|--:|---|
| **Quality Award** | **209** | `ARCH` I1 `award_pairing`, first entry. The thesis writes itself from A5/A6: a **2-element serial chain at 0.865 expected reliability**, one setpoint, one distance, and a failure mode that is *graceful* — the burst misses, the robot keeps playing. *"It never failed"* is a submission, not a consolation. Bring the match-by-match reliability log |
| **Industrial Design Award** | **210** | `ARCH` I1 `award_pairing`, second entry. The submission is the **descope decision itself**: show the turreted variable-range concept, show the fixed-position variant, and show the arithmetic that chose the second — 174 h against a 205 h pool. Judges reward a design that is *obviously the right size for the team that built it* |

**Two the team should *not* chase with this robot:** *Creativity Award sponsored by Rockwell
Automation* (208 events) — a deliberately unsurprising mechanism is the opposite of its thesis; and
*Autonomous Award sponsored by Google.org* (208) — that award belongs to the **I5 AUTO Specialist**
rows, which are the four highest-index designs in this file and a **different candidate**.

### 7.6 Step 6 — materials checklist

Sourced from [`bom/parts_manipulation.yaml`](bom/parts_manipulation.yaml) and
[`bom/03_LAUNCHERS_ELECTRONICS.md`](bom/03_LAUNCHERS_ELECTRONICS.md). **Prices are 2026 USD and were
verified at the time those files were written — re-verify against live vendor pages before ordering
(`bom/recheck_prices.sh`).** Vendor codes: `AM` = AndyMark, `TTB` = The Thrifty Bot, `WCP` = WestCoast
Products, `MMC` = McMaster-Carr. **No part number is invented here; entries without a verified SKU are
marked UNVERIFIED and must be resolved before the order goes out.**

| # | Item | Vendor | Unit | Ev. | Note |
|---|---|---|---|---|---|
| 1 | Compliant Wheels, 4 in. — intake roller | AM | **$11.00** | **[C]** | Also 2 in. $6.20 · 2¼ in. $7.20 · 3 in. $8.40 |
| 2 | Roller surface — polycord / surgical tubing / silicone over ½ hex | MMC | — | **UNVERIFIED** | `parts_manipulation.yaml` carries no resolved price. Pick **one** and price it before ordering |
| 3 | ½ hex 22-tooth #25 sprocket, qty 2 | TTB | **$19.99** | **[C]** | |
| 4 | #25 chain tensioner, qty 1 | TTB | **$14.99** | **[C]** | |
| 5 | ½ inch hex coupler, qty 2 | TTB | **$22.99** | **[C]** | |
| 6 | Flywheel motors + gearbox | — | — | **UNVERIFIED** | Choose from [`bom/03_LAUNCHERS_ELECTRONICS.md`](bom/03_LAUNCHERS_ELECTRONICS.md) and verify live |
| 7 | 2×1 aluminium tube + 1/8 plate, bandsaw stock | — | — | **[H]** | The **A9 = 4** commitment. If any part needs a router, it is a **different candidate** — re-score it |
| 8 | Encoders (through-bore or integrated) | — | — | **UNVERIFIED** | The **A8 = 5** commitment: encoders only, no camera in the critical chain |
| 9 | **SystemCore control system** | — | — | **[C] for 2027, n/a for this 2026 example** | **Order the day it is orderable.** If it has not shipped at kickoff, `A13` floors at **1** for everything that touches it |
| 10 | Spare flywheel wheel set + spare intake roller | AM | ~**$11–22** | **[C]** | The Quality Award submission is *"it never failed"*; that requires spares to exist before event 1 |

**Budget check against gate G3:** the `ARCH` band for this archetype is **$600–1,100** beyond a base
drivetrain and control system. Use the **high** end. **$1,100 < $2,500** → G3 does not fire, and
roughly **$1,400 remains** for the second mechanism, spares and overrun. Excluded by construction:
drivetrain, control system, registration ($6,500) and travel — those do not trade against design
decisions.

### 7.7 The one-page kickoff-day loop, condensed

1. Read the manual for the eight `RUB` §11 numbers. Twenty minutes, two people. **Before anyone draws.**
2. Apply the `PF` game-conditional weight deltas (`tools/rubric_weights.py`).
3. Enumerate candidates **and their descoped variants** — two rows, never one.
4. Score achievability by hand, **two people independently**, against `RUB` §2. Reconcile gaps >1 by
   re-reading the tie-break, not by splitting the difference.
5. Run `cycle-model.py` at **your** cycle time; let `score-strategy.py` consume it for V1.
6. Run the scorer. **Quadrant first, binding constraint second, index last.**
7. For every T2 STRETCH row you intend to build, **write down which enabler you are buying.**
8. Re-run at Week 3 with real hours spent. A1 and A13 move fastest.

---

## §8. Validation / dry run

### 8.1 Reproducibility

```bash
# Run from the repository root.
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml                       # 27/30
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
       --rubric reference/.achievability_rubric.v1.bak                                             # 24/30
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
       --set outsourced_2d_account=true                                                            # 27/30
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail R2
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail G1
python tools/score-strategy.py --candidates reference/examples/candidates_example.yaml
python tools/backtest_specialists.py
```

Deterministic. No network, no randomness. Requires PyYAML. `cycle-model.py` is imported by path and
degrades to a warning if absent.

### 8.2 Regression assertions — run these after **any** future edit to the rubric

| # | Assertion | Current |
|---|---|---|
| R1 | `--from-corpus` agreement ≥ **27/30** | 27/30 ✅ |
| R2 | **False-GREEN count = 0** — no T1 GREEN row whose hand label is not YES | 0/12 ✅ |
| R3 | All four `NO` records (F1, R1, G2, P3) are T3 RED or T4 GATED | 4/4 ✅ |
| R4 | `G2` (Full-Grid, I2 do-everything) has the **lowest** ACH in the file | 14.9 ✅ |
| R5 | Patched scorer + **v1 yaml** still reproduces exactly **24/30** | ✅ verified |
| R6 | Confusion matrix is **monotone** — no off-diagonal cell more than one step from the diagonal | ✅ |
| R7 | ACH↔hand-verdict Spearman ρ ≤ **−0.65** | −0.709 ✅ |
| R8 | Every miss's binding constraint names the **same** gate (one root cause, not many) | G2 ×3 ✅ |

### 8.3 Hand-authored candidates still work end to end

```
$ python tools/score-strategy.py --candidates reference/examples/candidates_example.yaml

            +----------------------------------+----------------------------------+
            |            VALUE < 55            |            VALUE >= 55           |
            +----------------------------------+----------------------------------+
ACH >= 60   |         CHEAP INSURANCE          |            BUILD THIS            |
            |                -                 |              S2 S1               |
            +----------------------------------+----------------------------------+
ACH <  60   |              DELETE              |               TRAP               |
            |                -                 |               S3*                |
            +----------------------------------+----------------------------------+
```

S3 is the deliberate control — `ARCH` invariant **I2**, 0/5 small-team success in five seasons, the
highest VALUE score in the candidate file, three simultaneous hard gates. It is still gated after the
tune. **The tune did not soften the instrument where it matters.**

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/05_RUBRIC_BACKTEST.md` | **new** — this document |
| `reference/05_rubric_backtest.yaml` | **new** — machine-readable results, v1→v2 changelog, regression assertions, uncertainty register |
| `tools/backtest_specialists.py` | **new** — the §3.2 independent TBA component-COPR test |
| `reference/achievability_rubric.yaml` | **EDITED v1 → v2** — G1 graded (`hard_floors`/`soft_floors`), G4 `soft_band_multiplier: 1.25`, `gates.soft_downgrade_max_tiers: 1`, `meta.version: 2`. **No weight, threshold or anchor was changed** |
| `reference/.achievability_rubric.v1.bak` | **new** — verbatim v1, so every "before" number here is re-runnable |
| `tools/score-strategy.py` | **EDITED** — `run_gates()` returns a soft-gate list; reads the new yaml keys; defaults reproduce v1 exactly (verified) |
| `tools/.score-strategy.py.pretune.bak` | **new** — verbatim pre-patch scorer |

Nothing marked DONE was modified. [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md),
[`02_TEAM_CAPACITY_MODEL.md`](02_TEAM_CAPACITY_MODEL.md), [`03_ARCHETYPE_CORPUS.md`](03_ARCHETYPE_CORPUS.md),
[`archetype_corpus.yaml`](archetype_corpus.yaml), the `awards/` files and the `bom/` files were **read
and cited, not edited**. `ACHIEVABILITY-RUBRIC.md` was not edited either — its §9 now describes the
**v1** back-test, and this file supersedes it; the §9 numbers remain reproducible via
`--rubric reference/.achievability_rubric.v1.bak`.

---

## Known limitations

- **90% is in-sample.** The `RUB` anchors were calibrated so `ARCH`'s YES records fall right of the
  achievability line, and this pass tuned three gate parameters against the same 30 records. 27/30 is
  a **consistency floor, not a measurement of accuracy.** The honest out-of-sample test is 2027: score
  the candidates on kickoff day, seal the file, compare in April.
- **Three tunes, three parameters, thirty records.** The ratio is defensible but not comfortable.
  Mitigations actually applied: no weight was touched; each tune states a principle checkable
  independently of the test set; each is a **one-line revert** (`soft_floors: []`,
  `soft_band_multiplier: 1.0`, `soft_downgrade_max_tiers: 99`); backwards compatibility was verified
  *before* the yaml was edited.
- **The scorer was patched, not just the yaml.** The task called for editing the rubric yaml in place;
  new yaml keys need code that reads them. Every default reproduces v1 exactly, and R5 in §8.2 asserts
  it, but this is a code change and is disclosed as one.
- **The `soft_floors: [router]` pricing is UNVERIFIED.** *"2D profile cutting is buyable as a service
  at $50–200/order, 5–10 business day lead"* is a plausible market claim written from general
  knowledge; **no vendor page was checked for this pass.** Verify before the fall fabrication-account
  deadline (`CAP` §7.5, **2026-12**). If it is materially wrong, revert tune A.
- **All three residual misses share one unfixable-today cause** — `mechanism_count ≠ novel_mechanisms`
  (§6.1). The fix needs a corpus field that does not exist. It was deliberately **not** fabricated.
- **`auto_score_from_corpus` is a regression harness, not a scoring method.** Every factor score in
  §2 is machine-derived from corpus metadata and is **[S]**. Real candidates are scored by hand
  against `RUB` §2 — §7 is the demonstration of that, and its A10 note flags the one factor the
  harness proxies badly.
- **The §3.2 TBA test covers 2023–2025 only.** 2026 `REB` — the corpus's primary calibration season —
  has empty component-COPR columns for all 8,160 team-events. §6.5 states the fix.
- **The VALUE↔outcome correlation is partly circular** (§6.4): V3 and V5 are derived from the
  `outcome` field, and carry 41% of the value weight. Use ACH ρ = −0.709 as the headline.
- **The corpus's `outcome` field is "this archetype achieved this somewhere, for some team"**, not
  "this team would achieve it". It carries no team-size or budget qualifier.
- **`reference/team_capacity.yaml` still does not exist on disk**, so `team_constants` remains
  hand-transcribed from `CAP` §8. Every gate threshold in this back-test inherits that. Regenerate
  with `python tools/capacity_model.py --yaml` and diff before trusting any downstream number.
- **Nothing here is a BIOCORE claim.** No weight, gate, threshold or anchor derives from any BIOCORE
  rule; the game is not public until **2027-01-09 12:00 ET**. §7 is a procedure demonstrated on a
  manual that exists, so the team knows what to do with one that does not yet.
- **The `REB` §7 example predates SystemCore.** Its `A7 = 4` and `A13 = 4` are 2026 values. For 2027,
  add the `systemcore_adjustment` delta before banding A7, and floor A13 at **1** if SystemCore
  hardware has not shipped at kickoff. §6.3 is the largest single uncertainty in the instrument.

---

## Security note

Every source read for this pass was a local file in this project: five FRC manuals in
`manuals/archive/frc/_txt/`, the TBA CSVs in `research/predictive_tba/`, and the `reference/` and
`tools/` files cited above. All of it was treated as **data**. None contained text addressed to an AI
assistant or any attempt to issue instructions. **No network request was made**, no external endpoint
was contacted, and no authentication was used or attempted, while writing this file or producing any
output pasted into it. The two files edited (`achievability_rubric.yaml`, `tools/score-strategy.py`)
were backed up verbatim first, and both changes are one-line reversible.
