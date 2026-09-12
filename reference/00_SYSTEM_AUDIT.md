# System Audit — is the ranking + BOM system actually sound?

**Purpose.** An adversarial correctness pass over the whole workbench, run 2026-08-22. Every tool was
executed and its real output pasted. Every award name was checked against the naming authority. Every
vendor URL was curled. The rubric was attacked with a purpose-built stress set. Nothing here is a
summary of intent — it is a record of what the code did when it was run.

**Companion file:** [`00_system_audit.yaml`](00_system_audit.yaml) · navigation: [`../INDEX.md`](../INDEX.md)

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Executed / curled / grepped in this pass; output pasted below |
| **[H]** HISTORICAL-PATTERN | Prior-season behaviour, not stated for BIOCORE |
| **[S]** SPECULATION | Inference, flagged as such |
| **UNVERIFIED** | Could not be checked |

Source shorthand: `REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO ·
`CHRG` = 2023 CHARGED UP · `RAPD` = 2022 RAPID REACT.

---

## Verdict up front

| Question | Answer | Evidence |
|---|---|---|
| Is the ranking system sound and usable on kickoff day? | **Yes**, with one class of caveat (§3.6) | §2, §3 |
| Rubric back-tested hit rate | **27/30 = 90%** vs corpus hand labels; the corpus's own risk predicate scores 21/30 = 70% | §2.1 |
| Do the gates actually fire, and can they be gamed by optimistic scoring? | **They fire; they cannot be gamed** — an all-5s candidate with impossible gate inputs is still `T4 GATED` | §3.2 |
| Does a 6-mechanism vision-dependent robot land in the worst tier? | **Yes** — ACH 6.0/100, TRAP quadrant, `T4 GATED` | §3.1 |
| Does a trivial robot show low value? | **Yes** — VAL 0.0/100, CHEAP INSURANCE quadrant. But its *tier* reads `T2 STRETCH`, which is misleading | §3.3 (defect) |
| Part-URL pass rate | 2026-08-22: **73 / 75 = 97.3%**. 2026-09-04 re-run: **68 / 80 live, 0 regressions**. The 2026-08-22 figure undercounted, see §10.2 | §5, §10.2 |
| Do the BOM rollups recompute? | **Yes**, to the cent, from the line-item CSV | §7 |
| Is there any FTC contamination? | **None.** 41 hits, all correctly attributed to FTC/BIOBUZZ | §4 |
| Are any award names stale? | **None used as current.** All old names appear only inside explicit rename/migration tables | §1 |

**Three defects fixed in this pass:** (1) `score-strategy.py` silently accepted malformed candidate
files and silently skipped *all* hard gates when `gates_input` was absent — validation added;
(2) `award_alignment_matrix.yaml` carried a stale note asserting `team_capacity.yaml` does not exist —
it does; (3) the VEX flex-wheels page status was recorded as HTTP 403 (bot-blocked) when it is now
HTTP 404 (gone) — re-labelled UNVERIFIED.

---

## §0 — Re-run this whole audit in 60 seconds

`[AUDIT 2026-09-04]` **Three of these five commands did not do what the comment beside them claimed.**
Checks 2 and 3 can never return zero, because this audit file and `00_system_audit.yaml` both quote
the search terms, so each check matches its own record and every re-runner sees a false alarm. Check 4
has no stated expected value and its output is not pass/fail. All three are corrected below. The
substance of the three findings was and remains unchanged: no FTC contamination, no retired award name
used as current, no dead vendor URL that the data does not already flag. §10 records the re-run.

```bash
# Run from the repository root.

# 1. all four tools must run clean
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml | grep agreement
python tools/bom-builder.py reference/bom/examples/simple.yaml    | grep VERDICT
python tools/bom-builder.py reference/bom/examples/moderate.yaml  | grep VERDICT
python tools/bom-builder.py reference/bom/examples/ambitious.yaml | grep VERDICT
python tools/cycle-model.py --game rebuilt | grep -c .
python tools/teamupdate-diff.py slots | tail -1

# 2. no FTC contamination presented as FRC fact.
#    The audit records themselves quote the search terms, so they are excluded -- without that the
#    check matches its own evidence. Whatever survives is read in context: a hit is a defect only
#    when it presents an FTC fact as an FRC one.
grep -rniE "pollen|starterbot|skill.?builder|september 12" --include=*.md --include=*.yaml . \
  | grep -v "^./manuals/" \
  | grep -vE "00_SYSTEM_AUDIT|00_system_audit.yaml|00_AUDIT.md|INDEX.md" \
  | grep -viE "ftc|biobuzz|tech challenge"
#    2026-09-04: 17 surviving lines, every one read in context. Four are the firewall warnings
#    inside the BOM data, one is the forbidden_nouns stoplist, five are rows of the FRC-vs-FTC
#    comparison table in 00_PREMISE_CORRECTION.md (which names FTC in the column header rather than
#    on the row), and the rest are community-intel prose about why Pollen does not transfer.
#    0 defects. The raw count before filtering moves every time this file is edited, which is
#    exactly why it is not the number to watch.

# 3. no retired award name used as current. Also a read-in-context check, not a zero check:
#    the awards corpus deliberately retains retired names so it can map them, and a context filter
#    cannot tell a rename table from a recommendation. Read what survives.
grep -rniE "dean's list|chairman's|entrepreneurship award|rookie inspiration" \
  --include=*.md --include=*.yaml reference/ \
  | grep -vE "00_SYSTEM_AUDIT|00_system_audit.yaml|00_AUDIT.md" \
  | grep -viE "renamed|retired|gone|no longer|former|formerly|folded into|will be known as|→|->|migration|out of date"
#    2026-09-04: 79 raw hits in reference/, 17 surviving the filter. Twelve are the rename and
#    drift-detector tables in 00_AWARD_LIST_VERIFIED.md, four are the `retired:` block of
#    awards.yaml, one is the sentence forbidding the old name. None is a recommendation. 0 defects.

# 4. every vendor URL still resolves. This is not pass/fail.
#    Compare the output against parts_drivetrain.yaml's unverified_registry and the per-part
#    `status:` lines. A non-200 already recorded there is not a regression; a non-200 that is NOT
#    recorded there is. A rate-limiting vendor answers a parallel sweep with 429 -- re-run those
#    serially, and check the vendor's home page, before calling any page dead. See §5.
grep -hoE 'https?://[^ ",]+' reference/bom/parts_*.yaml | sed 's/[.,)}]*$//' | sort -u \
  | while read u; do printf '%s  %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 "$u")" "$u"; done \
  | grep -v '^200'
#    2026-09-04: 80 unique URLs, 68 live, 12 non-200 -- 7 already in the registry, 5 from one
#    rate-limiting vendor. 0 regressions.

# 5. rubric stress set (see section 3 for the file)
python tools/score-strategy.py --candidates <your-stress-file>.yaml

# 6. has the 2027 CDN started staging? After kickoff this is the highest-value line in the block.
bash tools/probe-2027-manual.sh     # exit 0 = game manual live, 1 = nothing published yet
```

---

## 1. Award-name audit `[C]`

**Authority:** [`awards/00_AWARD_LIST_VERIFIED.md`](awards/00_AWARD_LIST_VERIFIED.md) +
[`awards/awards.yaml`](awards/awards.yaml) (42 name strings, current **and** deliberately-retained retired
names for migration mapping).

**Method.** Case-insensitive grep across every `.md`, `.yaml`, `.py`, `.sh` in the project for the
retired-name set: `Dean's List`, `Chairman's`, `Entrepreneurship Award`, `Rookie Inspiration`,
`Highest Rookie Seed`, `Wildcard`, `Industrial Design Award sponsored by General Motors`,
`Autonomous Award sponsored by Ford`, `Excellence in Engineering` (unsponsored).
Every hit was then read in context and classified.

| Retired name | Hits outside `manuals/` | All hits historical/migration context? | Any used as a *current* recommendation? |
|---|---:|---|---|
| `FIRST Dean's List Award` (+ Finalist, + DCMP Semi-Finalist) | 14 | **Yes** | **No** |
| `Chairman's Award` / `District Chairman's Award` | 5 | **Yes** | **No** |
| `Entrepreneurship Award` | 2 | **Yes** | **No** |
| `Rookie Inspiration Award` | 3 | **Yes** | **No** |
| `Highest Rookie Seed` | 2 | **Yes** | **No** |
| `Wildcard` | 2 | **Yes** | **No** |
| `Industrial Design ... General Motors` | 2 | **Yes** | **No** |
| `Autonomous Award sponsored by Ford` | 1 | **Yes** | **No** |

**Result: 0 defects.** Every retired name occurs only inside a rename table, an award-migration matrix,
a true-positive drift-detector result, or an explicit "this is out of date" warning. Representative:

- [`awards/00_AWARD_LIST_VERIFIED.md`](awards/00_AWARD_LIST_VERIFIED.md) §1.1 — the rename table itself.
- [`awards/00_AWARD_LIST_VERIFIED.md`](awards/00_AWARD_LIST_VERIFIED.md) L436 — `dla-judging-guidelines.pdf`
  ("dla" = Dean's List Award) is still the **URL** for the FIRST Leadership Award guidelines; the file
  explicitly warns not to read the filename as evidence the award survives. Correct handling.
- [`../KICKOFF_PLAYBOOK.md`](../KICKOFF_PLAYBOOK.md) L899 — failure-mode #25 is *"Referring to the Dean's List"*.
  The name appears in order to forbid it.

**Names actually used as live recommendations** (from `archetype_corpus.yaml` `award_pairing`,
`award_alignment_matrix.yaml`, and `05_RUBRIC_BACKTEST.md`) — all current, all matching the authority:

`Quality Award` · `Industrial Design Award` · `Excellence in Engineering Award sponsored by Littelfuse` ·
`Team Spirit Award` · `Innovation in Control Award sponsored by nVent` ·
`Autonomous Award sponsored by Google.org` · `Creativity Award sponsored by Rockwell Automation` ·
`Gracious Professionalism Award` · `Imagery Award in honor of Jack Kamen` · `Judges Award` ·
`Rising All-Star Award` · `Rookie All-Star Award` · `Team Sustainability Award sponsored by Dow` ·
`FIRST Impact Award` · `FIRST Leadership Award` · `Engineering Inspiration Award sponsored by SpaceX` ·
`Woodie Flowers Finalist Award`.

**One cosmetic variance, not a defect.** `Rookie All-Star` vs `Rookie All Star` (hyphen) —
`WEB-T` writes the hyphen, `TBA` and the `REB` ceremony line do not. Both spellings are in the
drift-detector stoplist. Documented at `00_AWARD_LIST_VERIFIED.md` L518.

---

## 2. Code execution `[C]`

All four required tools ran to completion with exit status 0 on Windows 11 / CPython. No fixes were
required to make them run; the one fix made (§3.6) was to make one of them *safer*, not to make it work.

### 2.1 `tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml`

Ranks all 30 calibration archetypes and back-tests against the corpus's hand labels.

```
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

--- Back-test against archetype_corpus.yaml hand labels ---

 agreement: 27/30 = 90%   (the corpus's own risk predicate scores 21/30 = 70%)

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
C1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
P1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
R7   MARGINAL      T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
```

**Reading the 3 disagreements.** All three are the *same* disagreement: the human labelled a
3-novel-mechanism design "conditional/marginal", the rubric hard-gates it at `novel_mechanisms_max: 2`.
The rubric is **more conservative than the human in every disagreement, and never less**. For a
15-student team that is the correct direction to be wrong in — a false "no" costs a forgone design, a
false "yes" costs the season. `[S]` on the desirability, `[C]` on the direction.

**Also verified:** the back-test does not silently sit at 90% because the rubric agrees with everything.
`F1`, `R1`, `G2`, `P3` are labelled `NO` by hand and gated by the rubric; `R5`, `G3`, `F3` are labelled
`YES` and land `T1 GREEN`. The instrument discriminates.

### 2.2 `tools/bom-builder.py` — all three worked examples

| Example | Gate verdict | Discretionary $ | Build h | Design h | Prog h | Workstreams | Novel | Motors |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `simple.yaml` | **ALL GATES PASS** | 2230.78 / 2500 | 89.0 / 129.8 | 34.0 / 74.9 | 56.0 / 134.8 | 3 / 3 | 2 / 2 | 5 / 12 |
| `moderate.yaml` | **FAILS 5** — budget, build h, design h, workstreams, novel | 6348.23 / 2500 | 159.0 / 129.8 | 80.0 / 74.9 | 115.0 / 134.8 | 4 / 3 | 4 / 2 | 12 / 12 |
| `ambitious.yaml` | **FAILS 8 of 8** | — | 295.0 / 129.8 | 170.0 / 74.9 | 254.0 / 134.8 | 5 / 3 | 6 / 2 | 17 / 12 |

Real output, `simple.yaml`:

```
GATE CHECKS  (vs reference/team_capacity.yaml)
==============================================================================
  [PASS] BUDGET               $2230.78 discretionary (gross $4461.78 - KOP credit $2231.00) limit $2500.00
  [PASS] TOOLING FLOOR        bandsaw_drillpress           limit bandsaw_drillpress
  [PASS] BUILD HOURS          89.0 h                       limit 129.8 h
  [PASS] DESIGN HOURS         34.0 h                       limit 74.9 h
  [PASS] PROGRAMMING HOURS    56.0 h                       limit 134.8 h
         2027 is a Systemcore port year -- this line is already inflated ~40 h
  [PASS] PARALLEL WORKSTREAMS 3 effective (5 mechanisms)   limit 3
         effective: drivetrain, scoring, software; absorbed (0 motors, <=12 build h): passive_latch_climber
  [PASS] NOVEL MECHANISMS     2                            limit 2
  [PASS] MOTOR COUNT          5 motors / 5 controllers     limit 12
         propulsion cap is separately 4 (2026 R502; 2027 UNVERIFIED)

  VERDICT: ALL GATES PASS

  EARLIEST ORDER-BY: 2026-11-21  -- anything high-stockout must be on a PO by this date.
```

Real output, `ambitious.yaml` (the kickoff-day fantasy robot):

```
  [FAIL] TOOLING FLOOR        mill_lathe                   limit bandsaw_drillpress
         needs outsourcing or shop upgrade: deploying_intake (mill_lathe), variable_hood_shooter
         (router_cnc), turret (router_cnc), double_jointed_arm (mill_lathe),
         telescoping_climber (mill_lathe) | outsourcing_available: true (budget $400, +2 wk lead)
  [FAIL] BUILD HOURS          295.0 h                      limit 129.8 h
  [FAIL] DESIGN HOURS         170.0 h                      limit 74.9 h
  [FAIL] PROGRAMMING HOURS    254.0 h                      limit 134.8 h
  [FAIL] PARALLEL WORKSTREAMS 5 effective (11 mechanisms)  limit 3
  [FAIL] NOVEL MECHANISMS     6                            limit 2
  [FAIL] MOTOR COUNT          17 motors / 17 controllers   limit 12

  VERDICT: FAILS 8 GATE(S)
```

**The order schedule is the most operationally useful output** and it is identical across all three
examples on its binding line: `EARLIEST ORDER-BY 2026-11-21`, driven by the 6-week-lead
`baseline_electrical_package` with `stockout=high`. That date sits **9 days after the Nov 12 Virtual Kit
Release and 4 days after the Nov 17 Kit & Kickoff selection close** — i.e. the schedule is real and the
November decisions are on the critical path, seven weeks before anyone sees the game.

### 2.3 `tools/cycle-model.py --game rebuilt`

```
 REBUILT (2026)  --  cycle model
 Match: AUTO 20s + TELEOP 140s (endgame window 30s)
 Cycle action: FUEL -> active HUB  =  5 unit(s)/cycle @ 1 pt(s) each  ->  5 pts/cycle
 Your cycle time: 8.0s     AUTO units scored: 3

endgame choice         cycle  cycles    units   autoP    teleP    fixP    TOTAL
-------------------------------------------------------------------------------
(none)                   8.0    17.5     90.5       3     87.5       0     90.5
TOWER L1 (TELEOP)        8.0    16.5     85.5       3     82.5      10     95.5
TOWER L2 (TELEOP)        8.0    16.0     83.0       3     80.0      20    103.0
TOWER L3 (TELEOP)        8.0    15.2     79.2       3     76.2      30    109.2

--- Break-even: is the fixed action worth the cycles it costs? ---
action                   pts   time  cycles lost  pts lost     NET  verdict
----------------------------------------------------------------------------------
TOWER L1 (TELEOP)         10     8s         1.00       5.0    +5.0  WORTH IT
TOWER L2 (TELEOP)         20    12s         1.50       7.5   +12.5  WORTH IT
TOWER L3 (TELEOP)         30    18s         2.25      11.2   +18.8  WORTH IT

--- Sensitivity: what is 1 second of cycle time worth? ---
 Going from 8.0s to 9.0s costs 9.7 points/match.
 Over a 12-match qualification schedule: 117 points.

--- Ranking Point feasibility at 8.0s cycle ---
RP               threshold  you (alone)  w/ alliance x3  reachable?
--------------------------------------------------------------------------
ENERGIZED              100           90             272  YES alliance
SUPERCHARGED           360           90             272  NO
TRAVERSAL               50          n/a             n/a  (climb-based; see above)
```

**Arithmetic spot-check `[C]`.** `(none)`: 140 s ÷ 8.0 s = 17.5 cycles × 5 pts = 87.5 teleop + 3 auto
= 90.5. ✔ `TOWER L3`: 18 s consumed ⇒ 122 s ÷ 8 = 15.25 cycles × 5 = 76.2 + 3 + 30 = 109.2. ✔
Break-even net for L3: 30 − (2.25 × 5) = 30 − 11.25 = **+18.75 ≈ +18.8**. ✔ Sensitivity: at 9 s,
140/9 = 15.56 cycles × 5 = 77.8; 87.5 − 77.8 = **9.7 pts**. ✔ All four internally consistent.

### 2.4 `tools/teamupdate-diff.py slots`

```
G211           3      8     2     1     5
R402           3      7     1     4     2
G403           3      7     3     1     3
G420           3      6     3     2     1
R501           3      6     3     1     2
G301           3      6     4     1     1
...
wrote research/teamupdate_analysis/slot_churn_allseasons.tsv
```

Reads: rule slot, seasons touched, total amendments, then per-season counts. `G211` is the most-amended
slot on disk (8 amendments across 3 seasons). This is the predictive input behind
[`RULE-CHURN-WATCHLIST.md`](RULE-CHURN-WATCHLIST.md) — **do not commit a design to a `G2xx` behaviour
before Team Update 3.** `[H]`

---

## 3. Rubric sanity — what broke when attacked

An adversarial candidate set (8 probes) was written specifically to break the instrument. Real output:

```
id   strategy                             ACH   VAL   idx  quadrant        tier        binding constraint
----------------------------------------------------------------------------------------------------------------------
X3   ADVERSARY - all 5s on every facto  100.0 100.0 100.0  BUILD THIS      T4 GATED    GATE G1 MACHINE: needs 'cnc'
X4   UPPER BOUND - perfect and legal    100.0 100.0 100.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 5/5
X5   SINGLE-ZERO probe (A9 = 0)          94.7 100.0  97.1  BUILD THIS      T2 STRETCH  A9 manufacturing_floor = 0/5 [zero]
X8   A4-EXCLUSION probe (A4 = 0)         89.5 100.0  94.2  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity
X6   DOUBLE-ZERO probe (A9 = A11 = 0)    87.7 100.0  93.3  BUILD THIS      T3 RED      A11 iteration_count = 0/5 [zero]
X7   MALFORMED - A1=9, A13 absent        67.6  60.0  64.2  BUILD THIS      T2 STRETCH  A13 schedule_critical_path_risk
X2   Trivial robot (drives, nothing)    100.0   0.0  55.0  CHEAP INSURANCE T2 STRETCH  A1 build_hours_fit = 5/5
X1   SIX-mechanism vision-dependent       6.0  95.2  46.1  TRAP            T4 GATED    GATE G1 MACHINE: needs 'cnc'
```

### 3.1 Six-mechanism vision-dependent robot → worst tier. **PASS** `[C]`

`X1` scores **ACH 6.0/100** — the lowest achievability the instrument produced against any input,
including the corpus's own worst archetype (`G2` at 14.9). It lands in **TRAP** (high value, unreachable)
and is **`T4 GATED`** by G1 MACHINE. This is exactly the behaviour the rubric exists to produce, and it
produces it before any human argument can start.

### 3.2 Gates cannot be gamed by optimistic scoring. **PASS** `[C]`

`X3` was written as the attack: **every one of the 13 achievability factors and all 5 value factors set
to 5** — a perfect 100.0/100.0 — combined with gate inputs that are physically impossible
(9 workstreams, 9 novel mechanisms, $99,000, 9,000 h). Result: **`T4 GATED`**. The gates are evaluated
independently of the weighted means, so a team that talks itself into optimistic factor scores still
cannot talk itself past a gate. This is the single most important structural property of the instrument
and it holds.

### 3.3 **DEFECT — trivial robot reports `T2 STRETCH`** `[C]`

`X2` (drives, touches nothing, all 13 achievability factors = 5, all 5 value factors = 0) produces
**ACH 100.0, VAL 0.0, combined 55.0 → `T2 STRETCH`**.

The **quadrant is right** (CHEAP INSURANCE) and the value axis is right (0.0). But `T2 STRETCH` is
defined in [`achievability_rubric.yaml`](achievability_rubric.yaml) as *"possible, and only possible, if
you spend a specific named thing to buy it: a Week 3-4 event, a second technical mentor…"*. A robot that
does nothing needs no enabler. The cause is structural: **tiers are computed from the combined index,
which mixes value into an achievability-flavoured label.** `0.55 × 100 + 0.45 × 0 = 55`, which lands in
the T2 band by arithmetic accident.

*Severity:* **low in practice, real in principle.** The printed decision rule already says
*"RANK BY [the index], DECIDE BY THE QUADRANT"*, and the quadrant is correct. But a tired student at
2 a.m. reads the tier column. **Recommended reading rule, adopted here:** when quadrant is
CHEAP INSURANCE or DELETE, the tier column is meaningless — ignore it. Recorded rather than patched,
because changing the tier formula would invalidate the 90% back-test in §2.1 and that trade is not
worth making four months before kickoff.

### 3.4 **DEFECT — quadrant and tier can flatly contradict each other** `[C]`

`X6` (two achievability zeros) prints **quadrant = BUILD THIS, tier = `T3 RED`**. `T3 RED` reads
*"Do not build this"*. `BUILD THIS` reads "build this". The `no_zeros_in_green` rule caps the **tier**
but does not touch the **quadrant**, so the two output columns disagree on the same row.

*Severity:* **medium.** Unlike §3.3 the two columns give opposite instructions rather than one being
merely uninformative. *Mitigation, adopted here:* **a `T3 RED` or `T4 GATED` tier always overrides the
quadrant.** The tier is the veto; the quadrant is the reason. Not patched, for the same back-test-
stability reason as §3.3; recorded in §9 as a known limitation and in `00_system_audit.yaml`.

### 3.5 Zero-handling behaves exactly as documented. **PASS** `[C]`

| Probe | Zeros | Documented behaviour | Observed | |
|---|---|---|---|---|
| `X5` | A9 only | one zero caps tier at T2 | `T2 STRETCH` (index 97.1 would otherwise be T1) | ✔ |
| `X6` | A9 + A11 | two or more cap at T3 | `T3 RED` (index 93.3) | ✔ |
| `X8` | A4 only | A4 is **excluded** (it has gate G6); must not cap | `T1 GREEN` | ✔ |

The A4 exclusion is the subtle one and it is implemented correctly. Without it every defense archetype
the corpus labels `YES` would be wrongly capped.

### 3.6 **DEFECT FIXED — malformed candidate files were scored silently** `[C]`

`X7` was written with three deliberate errors: `A1: 9` (outside the 0–5 anchor range), `A13` absent
entirely, and **no `gates_input` block at all**. Before the fix the tool printed a confident
`ACH 67.6 / T2 STRETCH` with **no warning of any kind**, and — critically — **skipped every hard gate**,
because `c.get("gates_input", {})` defaults to an empty dict and `run_gates({})` fires nothing.

This is the most dangerous behaviour found in the audit. Candidate files are hand-typed on kickoff day
under time pressure; a single omitted block silently converts the gate system into a no-op while still
printing a plausible tier.

**Fix applied** to [`../tools/score-strategy.py`](../tools/score-strategy.py) — a `_validate_candidate()`
pass that warns to stderr on missing factors, unknown keys, out-of-range scores, and absent
`gates_input`. Post-fix output:

```
[WARN] candidate X7:
        - missing achievability factor(s) A13 -> scored as 0
        - achievability A1=9 is outside the 0-5 anchor range
        - no gates_input -> EVERY HARD GATE IS SKIPPED for this candidate
```

**Regression check:** `--from-corpus` still reports `agreement: 27/30 = 90%`, and
`--candidates reference/examples/candidates_example.yaml` still produces the same three rows with the
same tiers. The fix warns; it does not change any score.

### 3.7 Weight sums `[C]`

| Axis | Factors | Raw weight sum | Normalised? |
|---|---:|---:|---|
| Achievability | 13 | 856 | **Yes** — `100 * Σ(wᵢsᵢ) / (5 · Σwᵢ)` |
| Value | 5 | 290 | **Yes** — `100 * Σ(vⱼtⱼ) / (5 · Σvⱼ)` |

Weights are *not* authored to sum to 1 or 100; the aggregation formula divides by `Σw` explicitly, so
the sums are arbitrary by design and adding a factor cannot silently rescale the axis. Confirmed by the
`X4` probe: all-5s produces exactly **100.0** on both axes, which is only possible if normalisation is
correct. Combined index `0.55·ACH + 0.45·VAL` — the 55/45 split is documented and justified in
`achievability_rubric.yaml → aggregation.combined_weighting_rationale`.

---

## 4. FTC contamination sweep `[C]`

**Method.** `grep -rniE "pollen|starterbot|skill.?builder|september 12"` across every `.md`, `.yaml`,
`.py`, `.sh` outside `manuals/`. **41 hits. Every single one read in context.**

| Bucket | Hits | Assessment |
|---|---:|---|
| Explicit firewall / warning ("these are FTC BIOBUZZ, not BIOCORE") | 19 | **Correct** |
| Scope-guard headers in reference docs | 9 | **Correct** |
| FTC-sourced factual record (POLLEN specs, StarterBot vendors, Sept 12 FTC kickoff), labelled FTC | 11 | **Correct** |
| Comparison table mapping FTC → FRC (`StarterBot` → `KitBot`) | 1 | **Correct** |
| BIOBUZZ project cross-reference by path | 1 | **Correct** |
| **Attributed to BIOCORE / FRC** | **0** | — |

**Result: 0 violations, 0 fixes required.** Representative correct handling:

- [`../research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md) L13–16 — a two-column
  table putting FTC BIOBUZZ and FRC BIOCORE side by side; `StarterBots` row reads **"No. Not an FRC
  concept for 2027"**.
- [`FRC_VS_FTC_ORIENTATION.md`](FRC_VS_FTC_ORIENTATION.md) L137 — `StarterBot` → **KitBot**, with the
  note that the schedule and purpose differ.
- [`bom/parts_electronics.yaml`](bom/parts_electronics.yaml) L774 — machine-readable `scope_warning`
  carried inside the parts data itself, so a downstream consumer of the YAML inherits the firewall.
- [`../research/04_biocore_community_intel.md`](../research/04_biocore_community_intel.md) §0.1 —
  POLLEN's real specs are recorded **because** they are the thing not to transfer, and the file cites
  the Chief Delphi post where the community itself flags Pollen as *"the FTC game for next year."*

**The date discipline is also correct.** Every `September 12` hit either says it is the FTC kickoff or
says *"there is no FRC event of any kind on September 12, 2026."* The nearby FRC date (Sept 24,
registration only) is stated separately and never conflated with a game reveal.

---

## 5. Part / price URL spot-check `[C]`

**Method.** Every `http(s)` URL extracted from `reference/bom/parts_drivetrain.yaml`,
`parts_manipulation.yaml`, `parts_electronics.yaml`; deduplicated; trailing YAML punctuation stripped;
each fetched with `curl -sIL --max-time 20` following redirects, with a desktop UA.

**82 raw URLs → 75 unique testable → 73 HTTP 200 → pass rate 97.3%.**

| Vendor | URLs | 200 | Note |
|---|---:|---:|---|
| AndyMark (`andymark.com` + `www.`) | 21 | 21 | Includes the BIOCORE scoring-element pre-order `am-5901` page |
| REV Robotics | 16 | 16 | All `rev-XX-XXXX` SKU pages resolve |
| CTR Electronics | 10 | 10 | Kraken X60/X44, Minion, Talon FXS, Pigeon 2, CANcoder, CANrange |
| The Thrifty Bot | 8 | 7 | **1 dead** — see below |
| WCP (`wcproducts.com` + `docs.`) | 11 | 11 | |
| Swerve Drive Specialties | 2 | 2 | MK4i, MK4n |
| VEX Robotics | 1 | 0 | **1 dead** — see below |
| Limelight / FIRST / Chief Delphi | 6 | 6 | |

**The two failures:**

| URL | Status | Already flagged before this audit? | Action |
|---|---|---|---|
| `https://www.thethriftybot.com/collections/drivetrain` | **404** | **Yes** — `parts_drivetrain.yaml` L275 + L758 record it as HTTP 404 on 2026-08-22, and `bom/01_DRIVETRAIN.md` L286 marks TTB gearboxes **UNVERIFIED** | None needed. Correct pre-existing handling |
| `https://www.vexrobotics.com/flex-wheels.html` | **404** | **Partially** — recorded as HTTP **403** (bot-blocked) | **FIXED.** Re-labelled: 403 to the BOM pass, **404 to this audit's re-curl** — treat the page as gone, not merely bot-blocked. `UNVERIFIED` |

**No priced line item depends on either dead URL for its price.** TTB drivetrain parts are already
carried as UNVERIFIED with no price; the VEX flex-wheel entry carries `price_note` rather than a
verified price. The BOM totals in §7 contain no unverifiable-priced line.

**Prices were not independently re-verified in this pass.** URL liveness ≠ price accuracy. See §9.2.

---

## 6. Internal consistency — `team_capacity.yaml` `[C]`

[`team_capacity.yaml`](team_capacity.yaml) is the single source of truth. Every downstream citation was
grepped and compared.

| Constant | `team_capacity.yaml` | Cited in | Agrees? |
|---|---:|---|---|
| `students` | 15 | 38 occurrences of "15 students" across `.md` | ✔ |
| `effective_build_hours` | 599 | `achievability_rubric.yaml:42` (599), `award_alignment_matrix.yaml` (599.1), `02_TEAM_CAPACITY_MODEL.md:697` (599), `score-strategy.py` banner (599) | ✔ |
| `effective_build_hours_week4` | 854 | `achievability_rubric.yaml:43` (854), `02_TEAM_CAPACITY_MODEL.md` ×3 (854), `AWARD-ALIGNMENT.md:782` (853.7), `award_alignment_matrix.yaml:860` (853.7) | ✔ — 853.7 is the unrounded figure, 854 the rounded. Not a conflict |
| `effective_hours_multiplier` | 0.352 | `award_alignment_matrix.yaml` (0.352) | ✔ |
| `available_build_hours` | 129.8 | every `bom-builder.py` BUILD HOURS gate line | ✔ |
| `available_design_hours` | 74.9 | DESIGN HOURS gate | ✔ |
| `available_programming_hours` | 134.8 | PROGRAMMING HOURS gate | ✔ |
| `robot_discretionary` | 2500 | 24 `$2,500` mentions; `score-strategy.py` banner; BUDGET gate | ✔ |
| `novel_mechanisms_max` | 2 | `award_alignment_matrix.yaml` (2.00), gate G2, `05_RUBRIC_BACKTEST.md` ×3 | ✔ |
| `parallel_workstreams_max` | 3 | PARALLEL WORKSTREAMS gate | ✔ |
| `technical_mentors` | 1 | `score-strategy.py` banner "1 mentor" | ✔ |

**Three `~10 students` mentions checked and cleared:** `02_TEAM_CAPACITY_MODEL.md:766` (a
counterfactual — "10 students *at a similar tier mix* yields…"), `04_PREDICTIVE_FACTORS.md:168` (a cited
first-hand account of a *different* team), `team-ops/05_business_awards_sustainability.md:573` (a stated
program-viability floor). None claims to describe this team.

### 6.1 **DEFECT FIXED — stale "file does not exist" note** `[C]`

[`awards/award_alignment_matrix.yaml`](awards/award_alignment_matrix.yaml) L851 asserted:

> *"reference/team_capacity.yaml does NOT exist on disk (UNVERIFIED). CM names it as a companion but
> only tools/capacity_model.py is present."*

It **does** exist and is the canonical source for every number in that block. The note was written
before `team_capacity.yaml` was created and never revised. **Corrected in place**, with the 853.7 → 854
rounding relationship stated explicitly so the next reader does not re-open it as a discrepancy.

---

## 7. Arithmetic — BOM rollups recomputed from the part lists `[C]`

**Method.** `python tools/bom-builder.py reference/bom/examples/simple.yaml --csv <out>.csv` writes one
row per line item (47 rows, 27 COTS / 14 FABRICATED / 5 MATERIAL_STOCK / 1 TOTAL). Extensions were
re-summed independently from the CSV and compared to the printed subtotals and the gate figure.

| Mechanism | Recomputed from line items | Printed subtotal | Δ |
|---|---:|---:|---:|
| `kop_chassis` | 1600.00 | 1600.00 | 0.00 |
| `bumpers_frame` | 257.00 | 257.00 | 0.00 |
| `baseline_electrical_package` | 1979.40 | 1979.40 | 0.00 |
| `over_bumper_intake` | 380.39 | 380.39 | 0.00 |
| `passive_latch_climber` | 244.99 | 244.99 | 0.00 |
| **Gross** | **4461.78** | **4461.78** | **0.00** |

Gate arithmetic: `4461.78 − 2231.00 (KoP credit) = 2230.78` against a `2500.00` limit → **PASS**. ✔
Recomputed independently; matches to the cent.

Sub-check on `kop_chassis`: `940.00 (AM14U6) + 4 × 42.50 (NEO) + 4 × 100.00 (SPARK MAX) = 940 + 170 +
400 = 1510.00 COTS`, `+ 90.00 material = 1600.00`. ✔

Cycle-model arithmetic independently recomputed in §2.3 — four checks, all exact.

### 7.1 **Finding — the CSV does not reconcile to the BUILD HOURS gate** `[C]`

The CSV's `hours` column sums to **63.0 h** (FABRICATED lines only). The gate reports **89.0 h**. The
26 h difference is *by design*: mechanism-level `build_hours` come from `mechanism_catalog.yaml`, while
the itemised FABRICATED rows are illustrative fabrication detail, not an exhaustive decomposition — the
tool labels this explicitly per mechanism, e.g. `HOURS build 12.0 ... (fab-detail 7.0)`.

**But anyone re-deriving hours from the CSV alone gets 63 h and concludes there is a 67 h margin when
there is a 41 h margin.** Recorded in §9 as a limitation. The CSV also contains a `TOTAL` row inline with
the item rows, so a naive `sum(ext_price)` over the file double-counts (8923.56 instead of 4461.78) —
filter `mechanism_id != 'TOTAL'`.

---

## 8. Files written / changed by this pass

| File | Change |
|---|---|
| [`../INDEX.md`](../INDEX.md) | **Created** — project navigation, key dates, FRC-vs-FTC block, kickoff-day ordering |
| [`00_SYSTEM_AUDIT.md`](00_SYSTEM_AUDIT.md) | **Created** — this file |
| [`00_system_audit.yaml`](00_system_audit.yaml) | **Created** — machine-readable audit result |
| [`../README.md`](../README.md) | **Edited** — links `INDEX.md` |
| [`../tools/score-strategy.py`](../tools/score-strategy.py) | **Fixed** — `_validate_candidate()` added (§3.6). No scoring change; regression-checked at 27/30 |
| [`awards/award_alignment_matrix.yaml`](awards/award_alignment_matrix.yaml) | **Fixed** — stale "team_capacity.yaml does not exist" note corrected (§6.1) |
| [`bom/parts_manipulation.yaml`](bom/parts_manipulation.yaml) | **Fixed** — VEX flex-wheels status 403 → 404, re-labelled UNVERIFIED (§5) |
| `research/teamupdate_analysis/slot_churn_allseasons.tsv` | Regenerated by running `teamupdate-diff.py slots` |

---

## 9. Known limitations

1. **The tier column is not trustworthy on its own (§3.3, §3.4).** Two structural issues remain
   unpatched because patching them would invalidate the 90% back-test: a zero-value robot can read
   `T2 STRETCH`, and a `BUILD THIS` quadrant can pair with a `T3 RED` tier. **Operating rule:
   `T3`/`T4` always vetoes the quadrant; when the quadrant is CHEAP INSURANCE or DELETE, ignore the
   tier.** Revisit after kickoff, when re-back-testing is cheap.
2. **URL liveness is not price verification (§5).** 73 pages returned HTTP 200; their *prices* were not
   re-scraped in this pass. Prices in `parts_*.yaml` carry their own `verified_date` (2026-08-22) and
   should be re-run through [`bom/recheck_prices.sh`](bom/recheck_prices.sh) before the
   **2026-11-21** order-by date. FRC vendor pricing moves in the autumn.
3. **The BOM CSV under-reports hours (§7.1)** and contains an inline `TOTAL` row. Do not re-derive gate
   figures from it without filtering.
4. **Every BIOCORE-specific number is pre-manual.** The 90% back-test is against *past* seasons; it
   measures whether the instrument reproduces expert judgement on RAPD→REB archetypes, **not** whether
   it will rank BIOCORE strategies correctly. Re-run `--from-corpus` after adding BIOCORE archetypes.
5. **Systemcore is the largest unquantified risk.** The programming line already carries a ~40 h
   Systemcore-port inflation `[S]`, but 2027 is the first season without the roboRIO since 2015 and
   `available_programming_hours: 134.8` is an estimate made before any team has shipped on the platform.
   If the port costs 80 h instead of 40, `simple.yaml` still passes (56.0 / 134.8) but `moderate.yaml`
   moves from 1 passing hour-gate to 0.
6. **Gate G2's `novel_mechanisms_max: 2` is where the rubric disagrees with humans (§2.1).** All three
   back-test misses are that gate. If BIOCORE turns out to reward a 3-mechanism robot, this is the
   parameter to revisit first — and the one most likely to be wrong.
7. **`manuals/2026-27_BIOCORE/` holds no BIOCORE source.** Nothing in this audit validates any
   BIOCORE claim, because there are no BIOCORE primary sources yet. Re-run the whole of §0 on
   2027-01-09. `[AUDIT 2026-09-04]` It is no longer empty: the 2026-08-23 beta test left
   `ingest_DEEPSPACE_20260824T032851Z/` there, a full ingest of the **2019 DEEP SPACE** manual, plus
   an empty `sections/`. Both are correctly named and neither claims to be BIOCORE, but the kickoff
   ingest writes into this directory, so the leftover is labelled by `manuals/2026-27_BIOCORE/README.md`
   rather than left to be recognised at 12:30 p.m. on kickoff day.
8. **The audit did not execute the other 34 tools.** Only the four named tools plus the BOM/award
   helpers were run. `tools/predictive_factor_stats*.py` and the TBA scrapers were not re-executed;
   their outputs on disk were taken as given. `[AUDIT 2026-09-04]` Narrowed, not closed: the
   2026-08-23 beta test (`../review/BETA_TEST_REPORT.md`) additionally ran `score-priors.py`,
   `scouting-plan.py`, `frc_spans.py`, `RUN-KICKOFF.sh` end to end against two real manuals, and
   found four defects that this audit did not reach, including `frc_spans.py` returning an empty
   parse on a pre-2023 manual while every downstream section still rendered. The TBA scrapers remain
   unexecuted since their outputs were written.

9. **`frc_spans.py` is era-limited to roughly 2017 and later** `[AUDIT 2026-09-04]`, found by the
   beta test rather than by this audit. It keys on the modern gutter geometry and the 2023-and-later
   colour encoding, and on an older manual it matches nothing and returns empty rather than failing.
   `RUN-KICKOFF.sh` now hard-fails on an implausible parse (fewer than 100 rules, 20 violations, 20
   sections or 30 glossary terms; every FRC season 2016-2026 has 124-228 rules). **If FIRST changes
   the 2027 layout, fixing `frc_spans.py` is the first kickoff-day task**, and `rule-inventory.py`
   parses older layouts and is the cross-check.


---

## §10. Re-run, 2026-09-04 `[C]`

**Why.** URLs rot and a remembered number is not evidence. Everything in §0 that is cheap to re-run
was re-run 13 days after the original pass and 127 days before kickoff. **Nothing regressed.** Three
things were found: the §0 commands were partly self-defeating (fixed in place, above), §5 undercounted
its own URL set (§10.2), and three file counts stated in `../README.md` and `../research/00_AUDIT.md`
are stale (§10.4).

### 10.1 Tools: all clean, all unchanged

| Command | 2026-08-22 | 2026-09-04 |
|---|---|---|
| `score-strategy.py --from-corpus` | `agreement: 27/30 = 90%` | **`agreement: 27/30 = 90%`** |
| `bom-builder.py … simple.yaml` | ALL GATES PASS | **ALL GATES PASS** |
| `bom-builder.py … moderate.yaml` | FAILS 5 | **FAILS 5**: BUDGET, BUILD HOURS, DESIGN HOURS, PARALLEL WORKSTREAMS, NOVEL MECHANISMS |
| `bom-builder.py … ambitious.yaml` | FAILS 8 of 8 | **FAILS 8**, the same eight |
| `cycle-model.py --game rebuilt` | 60 lines | **60 lines** |
| `teamupdate-diff.py slots` | regenerated `slot_churn_allseasons.tsv` | **regenerated, same tail row `G427 3 3 1 1 1`** |

The back-test rate has now held across four independent passes: the tuning pass, the audit, the
remediation verify and this one. The three misses are the same three (C1, P1, R7), all on gate G2.

**The larger thing that happened since this audit was written, and it is not in this file.** On
2026-08-23 and 2026-08-24 the kickoff autorun was run end to end against two real manuals. It found
four defects this audit did not reach, the worst of them `frc_spans.py` returning an empty parse on a
pre-2023 manual while every downstream section still rendered, so a review could have been written on
nothing. All four were fixed and the back-test was unmoved. The run after the beta then produced
`../review/DEEPSPACE_20260824T032851Z/REVIEW.md`, a complete nine-section kickoff review of 2019
DEEP SPACE: 133 pages ingested, 169 rules diffed against 2018 POWER UP, strategies ranked, a BOM that
converged through three gate failures, awards, loopholes, Q&A questions and a betting sheet.
**The pipeline this audit checked in pieces has now been run whole, on a game whose answers are
known.** See [`../review/BETA_TEST_REPORT.md`](../review/BETA_TEST_REPORT.md).

### 10.2 Vendor URLs: 68 live of 80, **0 regressions**, and §5's own count was low

Re-curled 2026-09-04 with the §0 command, 12-way parallel, desktop UA, 25 s timeout; every non-200
re-run serially afterward.

| | 2026-08-22 (§5) | 2026-09-04 |
|---|---|---|
| Unique URLs from `parts_*.yaml` | 75 "testable" | **80** |
| HTTP 200 | 73 | **68** |
| Non-200 | 2 | **12** |
| Of those, already recorded as dead/unverified in the data | 2 | **7** |
| Of those, undetermined because the vendor rate-limits | 0 | **5** |
| **Live URLs the project claims are live** | 73 / 73 | **68 / 68** |

**The last row is the one that matters, and it is clean in both passes.** No URL that any part entry
relies on has gone dead since 2026-08-22.

**§5 undercounted.** The command in §0 extracted 80 unique URLs from those three files on
2026-09-04, and
those files have not been modified since 2026-08-22 11:21. Five of the URLs §5 did not report sit in
`parts_drivetrain.yaml`'s `unverified_registry`, the block that exists precisely to record dead
pages, so §5's "75 unique testable / 2 dead" was reporting the live set while implying it was the
whole set. The corrected reading is: **80 URLs, 7 of them recorded dead or unverifiable before either
pass ran, 68 of the remaining 73 confirmed live and 5 undetermined.**

The twelve non-200 results, each checked against the data:

| URL | 2026-09-04 | Already flagged? | Verdict |
|---|---|---|---|
| `thethriftybot.com/collections/drivetrain` | 404 | Yes, `parts_drivetrain.yaml` L275, L758 | Unchanged |
| `wcproducts.com/collections/robot-drive/products/wcd-kit` | 404 | Yes, `unverified_registry` L759 | Unchanged |
| `andymark.com/products/6-in-higrip-wheel-options` | 404 | Yes, `unverified_registry` L760 | Unchanged |
| `andymark.com/products/frc-bumper-kit` | 404 | Yes, `unverified_registry` L761 | Unchanged |
| `revrobotics.com/maxswerve/` | 404 | Yes, `unverified_registry` L762 | Unchanged |
| `vexrobotics.com/versaplanetary.html` | 403, then 404 on retry | Yes, `unverified_registry` L757 | Unchanged; see below |
| `vexrobotics.com/flex-wheels.html` | 403 | Yes, `parts_manipulation.yaml` L310 | See below |
| 5 × `thethriftybot.com/products/*` | 429 | No | **Undetermined, not dead.** See below |

**VEX is inconsistent and the honest label is UNVERIFIED, which is what the data already says.** The
same two pages returned 403 to one request and 404 to the next in this pass. §5 recorded them moving
403 → 404 and concluded "gone, not merely bot-blocked". That conclusion is not supported: a host that
answers 403 and 404 to identical requests minutes apart is running bot mitigation, and neither code is
evidence about the page. The `price_note` in `parts_manipulation.yaml` has been corrected to say so.
No priced line depends on either page.

**The Thrifty Bot rate-limits, and 429 is not 404.** Five TTB product pages returned 429 to the
parallel sweep. Retried serially at 30 s intervals they still returned 429, **and so did
`thethriftybot.com/` itself**, the vendor's home page. A home page is not gone, so the 429 is this
client being throttled and says nothing about the five products. Two other TTB URLs in the same sweep
returned 200, which is what an intermittent throttle looks like. Recorded as undetermined. Anything
that turns on a TTB price should be confirmed in a browser before the 2026-11-21 order-by date.

**One stale negative corrected the other way.** `docs.wcproducts.com/greyt-elevator-cascade` is
recorded in `parts_manipulation.yaml` as "HTTP 404 at the URL tried". It returned **200** on
2026-09-04. Corrected in the data.

**Still not price verification.** Liveness is not price accuracy, and §9.2 stands unchanged: run
[`bom/recheck_prices.sh`](bom/recheck_prices.sh) before **2026-11-21**. That date is 78 days out and
is the only hard deadline this workbench owns before kickoff.

### 10.3 `frc2027` CDN: nothing staged, confirmed twice

`bash tools/probe-2027-manual.sh`, 2026-09-04: **every probe 404, exit 1, nothing live.** Unchanged
from 2026-08-22. Container listing is still disabled server-side, so this is evidence of nothing
published under a *known name shape*, not proof of absence.

Cross-checked against a second, independently written probe, `tools/manual-probe.mjs` in the Trellis
suite, which also reports nothing live for 2027. **The two probes agreed on the result and disagreed
on the question**: they swept 42 name shapes between them and shared only 7.

**That comparison found a real gap in this script, and the gap was in the season just gone.** FIRST
moved two document classes to kebab case for 2026, and this probe was still asking for the 2024 and
2025 names:

| Document | What this probe asked for | What 2026 actually served |
|---|---|---|
| Field drawings | `FieldAssets/2026FieldDrawings.pdf` (404) | `FieldAssets/2026-field-dimension-dwgs.pdf` (200, 29,125 KB) |
| Field assembly manual | not probed at all | `FieldAssets/field-manual.pdf` (200, 36,239 KB) |
| AprilTag guide | `AprilTags/2026AprilTagLayout.pdf` (404) | `FieldAssets/2026-apriltag-images-user-guide.pdf` (200) |
| Manual, HTML edition | not probed at all | `Manual/HTML/2026GameManual.htm` (200) |

Every one of those URLs is in this project's own `logs/fetch_*.log`, because the archive fetcher
found them. **The evidence to fix the probe was already on disk and the probe had never been checked
against it.** Corrected 2026-09-04, and the shape list now also carries the shapes the Trellis probe
had. Self-tested against 2026 after the merge: **11 live files, up from the 2 the README's
self-test recorded**. Against `frc2027` it still correctly reports nothing, exit 1.

The reciprocal fix went the other way. The Trellis probe reported **zero team updates for 2026**,
a season with twenty-four of them live, updates 00 through 22 and the combined PDF, because it did
not know about the `REBUILT_TeamUpdate01.pdf` game-name
prefix that this project documents in its own script comments. It now finds 30 files across all five
document types for 2026 where it found 2. Written up in that suite's `docs/05-COMPANIONS.md` §4.2.
**Nothing was integrated and neither project gained a dependency. What crossed was evidence.**

### 10.4 Three stated file counts are stale `[C]`

`../README.md` and `../research/00_AUDIT.md` §5 both say the archive holds "242 PDFs" and "426 files"
for 668 documents. Recounted 2026-09-04, and **no file in `manuals/` has been modified since
2026-08-22 except the beta-test ingest**, so these were already wrong when written: the gap-fill fetch
at 11:01 on 2026-08-22 landed after `research/00_AUDIT.md` was written at 03:09 and the README copied
the older number.

| | Stated | Actual, 2026-09-04 |
|---|---:|---:|
| `manuals/archive/frc/` PDFs | 242 | **316** live, plus 16 quarantined in `_rejected_mislabeled/` and `_truncated_unrecoverable/` |
| `manuals/archive/supplemental/` files | 426 | **433**, across 32 subdirectories |
| Total | 668 | **749** |
| Consecutive FRC seasons | 1992-2026, none missing | **Confirmed: 35 seasons, 1992-2026, none missing** |

The claim the counts were supporting, that archive coverage is complete and needs no work before
kickoff, is unaffected and is if anything stronger. Corrected in both files. `manuals/` is not in
the published repository, because FIRST's documents are not redistributed: a fresh clone gets the
PDFs the analysis reads by running `bash tools/rebuild-corpus.sh --fetch` from the repository root.

### 10.5 What this re-run did not do

- **No price was re-verified.** Only liveness. See §9.2.
- **The TBA scrapers were not re-executed.** §9.8 still applies to them.
- **No BIOCORE claim was validated**, because there are still no BIOCORE primary sources. §9.7.
- **The five undetermined TTB URLs were not resolved**, because the vendor throttles automated
  fetches and resolving them means opening a browser.

### 10.6 Files changed by this pass

| File | Change |
|---|---|
| [`00_SYSTEM_AUDIT.md`](00_SYSTEM_AUDIT.md) | §0 checks 2, 3 and 4 corrected so they can be re-run without false alarms; check 6 added; §9.7 and §9.8 updated; §9.9 added; this §10 |
| [`bom/parts_manipulation.yaml`](bom/parts_manipulation.yaml) | VEX flex-wheels `price_note` corrected: 403/404 is bot mitigation, not proof the page is gone; `docs.wcproducts.com/greyt-elevator-cascade` 404 → 200 |
| [`bom/parts_drivetrain.yaml`](bom/parts_drivetrain.yaml) | `unverified_registry` gains a re-check date and the TTB 429 finding |
| [`../research/00_AUDIT.md`](../research/00_AUDIT.md) | §6 gaps 3, 4 and 5 closed with the tool and date that closed them; archive counts corrected |
| [`../README.md`](../README.md) | archive counts corrected; re-run summary added above the fold; the probe's 2026 misses recorded |
| [`../INDEX.md`](../INDEX.md) | archive counts corrected |
| `../manuals/2026-27_BIOCORE/README.md` | **Created**, says what the leftover DEEP SPACE ingest is, so kickoff day does not have to work it out |
| [`../tools/probe-2027-manual.sh`](../tools/probe-2027-manual.sh) | **Fixed**, 17 name shapes added, taking the 2027 sweep from 22 URLs to 39, including the kebab case field drawings and AprilTag guide that 2026 actually served and this probe was missing. Self-test against 2026: 11 live, up from 2. See §10.3 |
| [`../review/BETA_TEST_REPORT.md`](../review/BETA_TEST_REPORT.md) | §5's fourth limitation marked superseded: the nine-section `REVIEW.md` was written by the run after the beta |
