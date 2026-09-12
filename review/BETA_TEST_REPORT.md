# Beta test — end-to-end, 2026-08-23

**Purpose:** run the kickoff autorun exactly as it will run on 2027-01-09, against two real manuals,
and record what broke. Four defects found and fixed; one design correctly rejected by its own gates.

**Companion:** `review/BETA_20260824T023107Z/` (the working review dir) ·
`review/REHEARSAL_GRADE.md` (the prior grading this build on)

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Observed in a real run in this repo; reproducible |
| **[S]** SPECULATION | Inference. Flagged as such |

---

## 1. What was tested

| # | Manual | Baseline | Purpose | Result |
|---|---|---|---|---|
| A | 2026 REBUILT (166 pp, TU22) | REBUILT (default) | self-diff behaviour | **defect found → fixed** |
| B | 2019 DEEP SPACE (133 pp) | REBUILT | out-of-era layout | **defect found → fixed** |
| C | 2026 REBUILT | 2025 REEFSCAPE | full phase 1 + 2 + review | **passed**, 2 defects found → fixed |

The user supplied both manuals; both are byte-identical to archived copies
(`845e7140a97f`, `cd1d15c6650d`), so extraction differences are attributable to the tooling, not the file.

## 2. Defects found and fixed [C]

### 2.1 Silent self-diff — test A

Feeding the manual that *is* the baseline produced `rules: 227 added=0 removed=0 changed=0` and
reported `PHASE 1 COMPLETE`. Every diff section rendered empty and a careless reader would report
"no rules changed" as a finding. `CLAUDE.md` told the reader to notice; nothing enforced it.

**Fix:** `RUN-KICKOFF.sh` now detects the zero-diff signature, prints `*** SELF-DIFF DETECTED ***`,
and prepends a banner to the briefing pack naming which sections are meaningless and which remain
valid, plus the `BASELINE=` command to get a real diff.

### 2.2 Silent extraction failure — test B *(the serious one)*

The 2019 manual ran **clean** and produced a 349-line briefing pack containing:

| | REBUILT | DEEP SPACE 2019 |
|---|--:|--:|
| rules | 227 | **0** |
| violations | 80 | **0** |
| glossary | 100 | 16 |
| section map | 138 | (empty) |

`tools/frc_spans.py` keys on the modern gutter geometry and the 2023+ colour encoding; on a pre-2023
manual it matches nothing and returns empty — and every downstream section still rendered. A review
could have been written on **nothing**.

Note `tools/rule-inventory.py` parses 2019 fine (169 rules), so this is specific to the span parser
the ingest path uses.

**Fix:** a new **extraction sanity gate** (phase 1, step 1b) hard-fails when the parse is implausible.
Thresholds calibrated from the corpus — every FRC season 2016–2026 has **124–228 rules**, so the floor
is 100; violations < 20, sections < 20, glossary < 30 also fail. The error names the likely cause
(layout change), tells the reader to cross-check with `rule-inventory.py`, and says plainly: *if FIRST
changed the 2027 layout, fixing `frc_spans.py` is the first kickoff-day task.*

**Why this matters for BIOCORE [S]:** FRC changed rule numbering in 2024 and manual formatting in
2023. A 2027 layout change is a live possibility, and this was the failure mode that would have
produced a confident, empty review.

### 2.3 Aperture parse mangled by an inline comment — test C

Preflight printed `aperture_height_in = 72#manuals5.4/03_ARCHETYPE_CORPUS.mds2.4item4...` — the YAML
comment was concatenated onto the number. It passed only because the mangled string was non-empty.

**Fix:** strip `#...` before the quote/whitespace trim. Now prints `= 72`.

### 2.4 The stub taught a source key the tool cannot read — test C

`cycle-model.py` flags unsourced constants and looks for a sibling `<key>_source`. The generated stub
demonstrated **`_per_cycle_source`** — with a leading underscore — while the same stub's header says
*"keys beginning with `_` are notes and are ignored by every tool."* The stub was self-defeating: 17
of 19 constants reported `[UNSOURCED]` even when documented conscientiously.

**Fix:** stub now shows `per_cycle_source` (no underscore), adds `auto_s_source` / `teleop_s_source` /
`endgame_s_source`, and a `_sourcing` note stating the rule explicitly — including that a top-level
`_sources` map does **not** work. After correction: **19/19 constants sourced**, assumptions labelled
`ASSUMPTION` rather than laundered as facts.

## 3. What worked [C]

- **Extraction on a supported manual:** 227 rules, 80 violations, 138 sections, 100 glossary terms.
- **Real cross-season diff:** REBUILT vs REEFSCAPE → **7 added, 9 removed, 153 changed**, 12
  game-specific isolated by headline colour.
- **Geometry gate:** `single_flywheel reaches 108 in (shoot)` vs a 72 in aperture → **PASS**. The
  hopper-dump case that the grade called fatal now fails with the shortfall in inches.
- **The ranking inversion is gone.** The graded rehearsal put the TOWER climber in `BUILD THIS` and
  the fixed-zone shooter 10th. This run:

  | Strategy | Corpus verdict | Beta result |
  |---|---|---|
  | B2 Fixed-zone bulk FUEL shooter | R2 "highest-value small-team play" | **BUILD THIS, T1, rank 3** |
  | B3 AUTO specialist | R5 "captain-tier multiplier" | **BUILD THIS, T1, rank 5** |
  | B6 TOWER climb specialist | 1.1 % of match score, r = 0.003 | **DELETE, gated** |
  | B8 Do-everything | "where 15-student teams lose the season" | **TRAP, gated** |

  Caveat [S]: achievability was hand-scored by the same agent writing the review, so this shows the
  instrument *permits* the right answer, not that it *forces* it. The gates fired independently.

- **The BOM rejected the reviewer's own design**, which is the system working:

  ```
  [PASS] GEOMETRY (REACH)   single_flywheel reaches 108 in    limit 72 in
  [FAIL] BUDGET             $2,609.71 discretionary            limit $2,500
  [FAIL] TOOLING FLOOR      mill_lathe                         limit bandsaw_drillpress
  [FAIL] NOVEL MECHANISMS   3                                  limit 2
  ```

  Correct outcome: the *strategy* is right and the *build* is over-scoped. The resolution is to
  descope the launcher, not to overrule the gate.

## 4. Regression after all fixes [C]

- Back-test: **27/30 = 90 %**, unchanged. No rubric weight touched.
- `cycle-model.py`, `bom-builder.py`, `score-priors.py`, `scouting-plan.py`, `teamupdate-diff.py`,
  `score-strategy.py`: all pass.
- Sanity gate does not false-positive: REBUILT passes at `rules=227 violations=80 sections=138 glossary=100`.

## 5. Known limitations

- **`frc_spans.py` is era-limited to ~2017+.** Pre-2017 manuals fail the sanity gate by design. This
  is now loud rather than silent, but it is not fixed — fixing it means new x-position/colour rules.
- **The sanity thresholds are heuristics**, calibrated on 11 seasons. A genuinely tiny BIOCORE manual
  would false-positive; the error message says how to confirm.
- **Nothing forces the ranker to consult `score-priors.py`.** Still an instruction, not a gate — the
  one place the 2026 D-grade failure mode could recur.
- ~~**Test C's `REVIEW.md` was not written**; the beta stopped at verified phase-2 output. The nine-section
  review remains exercised only by the earlier rehearsal.~~
  **Superseded 2026-08-24, recorded 2026-09-04.** The run immediately after this one wrote it:
  `review/DEEPSPACE_20260824T032851Z/REVIEW.md`, a complete nine-section review of 2019 DEEP SPACE
  produced by the autorun, 291 lines, with the era note about the pre-2023 colour convention stated
  in the output rather than left for the reader to notice. `review/LATEST` points at it. The
  pipeline has now been exercised end to end, ingest through review, on a game whose answers are
  known. The other three limitations above stand unchanged.

## Files written by this pass
- `review/BETA_TEST_REPORT.md` (this file)
- `tools/RUN-KICKOFF.sh` — self-diff banner, extraction sanity gate, aperture parse fix, stub sourcing fix
- `review/BETA_20260824T023107Z/` — working review dir with all three schemas filled and phase-2 results
