# INDEX — BIOCORE Analysis workbench

**Purpose.** One line per document, grouped by track, so anything in this project can be found in
under ten seconds. This is navigation, not analysis: every claim lives in the file it links to.
Written 2026-08-22 by the index + audit pass.

**Companion file:** [`reference/00_SYSTEM_AUDIT.md`](reference/00_SYSTEM_AUDIT.md) — the correctness
check behind everything listed here (tools executed, award names verified, part URLs curled).

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source held in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference, flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

Source shorthand used across the project: `REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE ·
`CRES` = 2024 CRESCENDO · `CHRG` = 2023 CHARGED UP · `RAPD` = 2022 RAPID REACT.

---

## FRC vs FTC — never confuse these

> **BIOCORE™ presented by Haas is the *FRC* game. Kickoff Saturday, January 9, 2027, 12:00 p.m. ET.**
> **BIOBUZZ™ presented by RTX is the *FTC* game. Kickoff September 12, 2026.** Different program,
> different field, different presenting sponsor, different repository
> ([`XrxcGH/BIOBUZZ-Analysis`](https://github.com/XrxcGH/BIOBUZZ-Analysis)).

| Term | Belongs to | Never say |
|---|---|---|
| **Pollen** | FTC BIOBUZZ scoring element | "BIOCORE's game piece is Pollen" |
| **StarterBot / StarterBot Base** | FTC BIOBUZZ (AndyMark, goBILDA, REV, Studica) | "FRC StarterBot". FRC's analogue is the **KitBot** |
| **Skill Builders** | FTC, hosted on FIRST Training | "BIOCORE Skill Builders" |
| **September 12, 2026** | FTC BIOBUZZ kickoff | "FRC kickoff". There is **no FRC event that day** |
| **`am-5901`** | FRC BIOCORE scoring element pre-order — **name and specs not public** | any dimension, mass, or material claim about it |

Full firewall: [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) ·
structural differences: [`reference/FRC_VS_FTC_ORIENTATION.md`](reference/FRC_VS_FTC_ORIENTATION.md).

---

## Key dates

| Date | What | Why it binds |
|---|---|---|
| **2026-09-24, 12:00 ET** | Kit & Kickoff registration + Event Registration Round 1 preferencing opens | **[C]** Miss it and you take leftover event slots, not your first choice |
| **2026-11-12** | Pre-Kickoff Virtual Kit Release | **[C]** First look at KoP contents; the last input before BOM commitment |
| **2026-11-17** | Kit & Kickoff selection closes | **[C]** Hard deadline. After this the KoP order is fixed |
| **2026-11-21** | **Earliest order-by date** computed by `tools/bom-builder.py` | **[S]** The 6-week-lead electrical package must be on a PO by here |
| **2027-01-09, 12:00 ET** | **KICKOFF — BIOCORE game reveal, Game Manual V1 drops** | **[C]** Everything in this repo is input to that day |
| 2027-02-04 | FIRST Leadership Award + Woodie Flowers Finalist submissions due | **[C]** [`reference/awards/00_AWARD_LIST_VERIFIED.md`](reference/awards/00_AWARD_LIST_VERIFIED.md) |
| 2027-02-11 | FIRST Impact Award submission due | **[C]** Same source; the strongest advancing award |

---

## §0 — Start here on kickoff day (runnable, 60 seconds)

```bash
# Run from the repository root. On a fresh clone, run the corpus rebuild first
# (bash tools/rebuild-corpus.sh --fetch, then bash tools/rebuild-corpus.sh; see README.md).

# 1. Is the manual live? (FRC CDN container listing is disabled; this sweeps known filename shapes)
bash tools/probe-2027-manual.sh --download

# 2. Ingest it (takes a LOCAL pdf path; downloads nothing)
bash tools/ingest-manual.sh "manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf" V1

# 3. Sanity-check the ranking engine against its calibration corpus (expect 27/30 = 90%)
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml

# 4. Score YOUR whiteboard candidates (copy the example first, then edit)
cp reference/examples/candidates_example.yaml strategies.yaml
python tools/score-strategy.py --candidates strategies.yaml

# 5. Price and gate the winning strategy's BOM
python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown

# 6. Point value of a cycle vs a fixed endgame action (swap in real BIOCORE numbers)
python tools/cycle-model.py --game rebuilt --sweep
```

### Reading order on kickoff day

| # | Read | Time | Why now |
|---|---|---|---|
| 1 | [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) | 3 min | Firewall. Prevents the single most likely contamination |
| 2 | [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md) Phases 0–1 | 15 min | The operating document. Hour-by-hour clock |
| 3 | [`research/03_biocore_official_intel.md`](research/03_biocore_official_intel.md) — the 33 open questions | 10 min | Read the questions *before* the manual, so you read the manual for answers |
| 4 | [`research/04_biocore_community_intel.md`](research/04_biocore_community_intel.md) — the betting sheet | 5 min | Score the predictions against the manual; a wrong one shows where your priors are broken |
| 5 | **Game Manual V1** (ingested) | 90 min | The only source that matters |
| 6 | [`STRATEGY-RANKING-SYSTEM.md`](STRATEGY-RANKING-SYSTEM.md) | 20 min | The pipeline: manual in → ranked strategy + BOM + award plan out |
| 7 | [`reference/ACHIEVABILITY-RUBRIC.md`](reference/ACHIEVABILITY-RUBRIC.md) | 20 min | How to score each whiteboard idea; run `score-strategy.py` alongside |
| 8 | [`reference/RULE-CHURN-WATCHLIST.md`](reference/RULE-CHURN-WATCHLIST.md) + [`reference/QA-AMBIGUITY-HOTSPOTS.md`](reference/QA-AMBIGUITY-HOTSPOTS.md) | 10 min | Which rules will move in Team Updates — do not design against those |
| 9 | [`reference/bom/06_MECHANISM_CATALOG.md`](reference/bom/06_MECHANISM_CATALOG.md) | 15 min | Pick mechanisms by hour-cost, not by excitement |
| 10 | [`reference/awards/AWARD-ALIGNMENT.md`](reference/awards/AWARD-ALIGNMENT.md) | 10 min | Lock the two awards you chase *at kickoff*, not in Week 5 |

---

## Track 1 — Manual analysis and rules

| File | Lines | One line |
|---|---:|---|
| [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) | 68 | **Read first.** The FRC-vs-FTC firewall; kills the Pollen / StarterBot / Sept-12 contamination |
| [`research/02_supplemental_docs_index.md`](research/02_supplemental_docs_index.md) | 505 | Document precedence chain (Manual, then Team Updates, then Q&A), kickoff-day URL fetch list, version-drift trap |
| [`research/03_biocore_official_intel.md`](research/03_biocore_official_intel.md) | 452 | Every published BIOCORE fact plus 33 open questions the manual will answer |
| [`research/04_biocore_community_intel.md`](research/04_biocore_community_intel.md) | 403 | Chief Delphi corpus, shipping-rate geometry inference, 11-item falsifiable betting sheet |
| [`reference/QA-AMBIGUITY-HOTSPOTS.md`](reference/QA-AMBIGUITY-HOTSPOTS.md) | 109 | Which rules teams provably cannot parse, computed from 3 seasons of Q&A volume |
| [`reference/RULE-CHURN-WATCHLIST.md`](reference/RULE-CHURN-WATCHLIST.md) | 115 | Three triangulated signals for where BIOCORE's amendments will land |
| [`reference/FRC_VS_FTC_ORIENTATION.md`](reference/FRC_VS_FTC_ORIENTATION.md) | 153 | FRC structures with no FTC analogue: districts, event weeks, double elim, inspection, no bag day |
| [`research/00_AUDIT.md`](research/00_AUDIT.md) | 266 | Prior adversarial audit trail: what was verified, what was wrong, what is still missing |
| [`research/rule_inventories/`](research/rule_inventories/) | — | 2015–2026 structured rule corpus: `*_rules_v2.tsv`, `*_rules_full.txt` (not tracked; [rebuilt locally](README.md#what-is-not-in-this-repository)), `evergreen.tsv`, crosswalks, `qa_heat_*.tsv` |
| [`research/teamupdate_analysis/`](research/teamupdate_analysis/) | — | `2026_tu_churn.tsv`, `slot_churn_allseasons.tsv` — which rule slots get amended after the manual ships |
| [`manuals/archive/frc/`](manuals/README.md) | — | FRC game manual PDFs, plus `_txt/` extractions for 2022–2026. Not tracked; [rebuilt locally](README.md#what-is-not-in-this-repository) |
| [`manuals/archive/supplemental/`](manuals/README.md) | — | Team Updates, Q&A exports, inspection checklists, field drawings. Not tracked; [rebuilt locally](README.md#what-is-not-in-this-repository) |
| [`manuals/2026-27_BIOCORE/`](manuals/) | — | **Empty until kickoff.** `ingest-manual.sh` output lands here |

## Track 2 — Strategy ranking

| File | Lines | One line |
|---|---:|---|
| [`STRATEGY-RANKING-SYSTEM.md`](STRATEGY-RANKING-SYSTEM.md) | 1043 | **The pipeline.** Manual in → ranked strategy + BOM + award plan out. Start here for the whole system |
| [`strategy_ranking_system.yaml`](strategy_ranking_system.yaml) | — | Machine-readable companion to the above |
| [`reference/ACHIEVABILITY-RUBRIC.md`](reference/ACHIEVABILITY-RUBRIC.md) | 846 | 13 achievability factors × 5 value factors, weights, hard gates, quadrant and tier definitions |
| [`reference/achievability_rubric.yaml`](reference/achievability_rubric.yaml) | — | The weights and gates `score-strategy.py` actually reads |
| [`reference/02_TEAM_CAPACITY_MODEL.md`](reference/02_TEAM_CAPACITY_MODEL.md) | 876 | What "~15 students" is worth: 599 effective build hours, an 8-line allocation, 2 novel mechanisms maximum |
| [`reference/team_capacity.yaml`](reference/team_capacity.yaml) | — | **Single source of truth for team numbers.** Consumed by `bom-builder.py` gate checks |
| [`reference/03_ARCHETYPE_CORPUS.md`](reference/03_ARCHETYPE_CORPUS.md) | 627 | 30 hand-labelled strategies from RAPD/CHRG/CRES/REEF/REB — the rubric's calibration set |
| [`reference/archetype_corpus.yaml`](reference/archetype_corpus.yaml) | — | Machine-readable corpus, with an `award_pairing` per archetype |
| [`reference/04_PREDICTIVE_FACTORS.md`](reference/04_PREDICTIVE_FACTORS.md) `DONE` | 889 | What empirically predicts small-team success, from TBA 2023–2026. The rubric's weights derive from here |
| [`reference/04_predictive_factors.yaml`](reference/04_predictive_factors.yaml) | — | Machine-readable factor weights |
| [`reference/05_RUBRIC_BACKTEST.md`](reference/05_RUBRIC_BACKTEST.md) | 889 | Does the rubric predict? 27/30 = **90%** agreement, vs the corpus's own risk predicate at 70% |
| [`reference/05_rubric_backtest.yaml`](reference/05_rubric_backtest.yaml) | — | Machine-readable back-test result |
| [`reference/examples/candidates_example.yaml`](reference/examples/candidates_example.yaml) | — | **Copy this on kickoff day** and edit it into your whiteboard candidates |
| [`reference/SCOUTING-PLAN.md`](reference/SCOUTING-PLAN.md) | 133 | Scout only what FMS does not already publish — 15 students cannot afford to duplicate TBA |
| [`research/predictive_tba/`](research/predictive_tba/) | — | TBA rankings / alliances / matches / COPR CSVs 2023–2026 plus derived `pf4_*` and `pf5_*` tables |

## Track 3 — Awards

| File | Lines | One line |
|---|---:|---|
| [`reference/awards/00_AWARD_LIST_VERIFIED.md`](reference/awards/00_AWARD_LIST_VERIFIED.md) `DONE` | 575 | **The naming authority.** 25 current award names, submission deadlines, advancement, rename history |
| [`reference/awards/awards.yaml`](reference/awards/awards.yaml) | — | Machine-readable award list: check any award name against this. Held back until its FIRST quotes are trimmed; [see README](README.md#what-is-not-in-this-repository) |
| [`reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`](reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md) `DONE` | 110 | Descriptive record of the real 2026 slate from TBA; **superseded as authority** by the VERIFIED file |
| [`reference/awards/01_AWARD_WINNING_PATTERNS.md`](reference/awards/01_AWARD_WINNING_PATTERNS.md) `DONE` | 1082 | What actually wins each robot-adjacent award, with winner-seed forensics. Held back until its FIRST quotes are trimmed; [see README](README.md#what-is-not-in-this-repository) |
| [`reference/awards/AWARD-ALIGNMENT.md`](reference/awards/AWARD-ALIGNMENT.md) | 1135 | Which **two** awards each robot archetype should chase, and the hour cost of each |
| [`reference/awards/award_alignment_matrix.yaml`](reference/awards/award_alignment_matrix.yaml) | — | Machine-readable archetype → award mapping |
| [`reference/team-ops/04_tuning_testing_competition_ops.md`](reference/team-ops/04_tuning_testing_competition_ops.md) | 1539 | Tuning, testing and competition ops: practice field/robot, drive practice, reliability, spares, match day, batteries, alliance selection. Companion `04_competition_ops.yaml` |
| [`reference/team-ops/05_business_awards_sustainability.md`](reference/team-ops/05_business_awards_sustainability.md) | 730 | The non-robot deliverables: FIRST Impact submission, business plan, sustainability |
| [`research/awards_tba/`](research/awards_tba/) | — | TBA award records 2022–2026 plus `award_migration_matrix.csv`, `award_winner_forensics.csv`, `award_rank_profile.csv` |

## Track 4 — BOM and mechanisms

| File | Lines | One line |
|---|---:|---|
| [`reference/bom/06_MECHANISM_CATALOG.md`](reference/bom/06_MECHANISM_CATALOG.md) | 943 | **Start here.** Mechanism archetypes, each priced, hour-costed, and tooling-gated |
| [`reference/bom/mechanism_catalog.yaml`](reference/bom/mechanism_catalog.yaml) | — | The catalog `bom-builder.py` reads |
| [`reference/bom/01_DRIVETRAIN.md`](reference/bom/01_DRIVETRAIN.md) | 603 | Verified COTS drivetrain options — KoP chassis, WCD, swerve — and what each really costs a 15-student team |
| [`reference/bom/02_MANIPULATION_ELEVATION.md`](reference/bom/02_MANIPULATION_ELEVATION.md) | 856 | Intakes, elevators, arms, grippers: parts, architectures, hours |
| [`reference/bom/03_LAUNCHERS_ELECTRONICS.md`](reference/bom/03_LAUNCHERS_ELECTRONICS.md) | 1033 | Launchers, and the **2027 Systemcore transition** — the biggest control-system change since the cRIO |
| [`reference/bom/parts_drivetrain.yaml`](reference/bom/parts_drivetrain.yaml) | — | Priced drivetrain parts with vendor URLs |
| [`reference/bom/parts_manipulation.yaml`](reference/bom/parts_manipulation.yaml) | — | Priced manipulation parts |
| [`reference/bom/parts_electronics.yaml`](reference/bom/parts_electronics.yaml) | — | Priced electronics, including the Systemcore-era control system |
| [`reference/bom/examples/simple.yaml`](reference/bom/examples/simple.yaml) | — | Worked BOM that **passes all 8 gates** — the shape to aim for |
| [`reference/bom/examples/moderate.yaml`](reference/bom/examples/moderate.yaml) | — | Fails 5 gates. What "one mechanism too many" looks like numerically |
| [`reference/bom/examples/ambitious.yaml`](reference/bom/examples/ambitious.yaml) | — | Fails 8 of 8 gates. The kickoff-day fantasy robot, priced |
| [`reference/bom/recheck_prices.sh`](reference/bom/recheck_prices.sh) | — | Re-curls every vendor URL in `parts_*.yaml` and reports dead links |

## Track 5 — Team ops

**Read in this order:** `SMALL_TEAM_PLAYBOOK.md` (what a 15-student team does differently) →
`01` (the season shape) → `02`/`03`/`04` (the three technical lanes) → `05` (the non-robot half).
[`reference/team-ops/00_AUDIT.md`](reference/team-ops/00_AUDIT.md) is the correctness receipt for
this track **and** for Track 6.

| File | Lines | One line |
|---|---:|---|
| [`SMALL_TEAM_PLAYBOOK.md`](SMALL_TEAM_PLAYBOOK.md) | 896 | **Start here for the team, not the game.** What ~15 students do differently from a 60-student powerhouse, lane by lane, with the hour cost of each substitution |
| [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md) | 1197 | **The operating document.** Phases 0–6, ready-to-paste prompts, kickoff-day clock, failure-mode list |
| [`reference/team-ops/00_AUDIT.md`](reference/team-ops/00_AUDIT.md) `NEW` | 674 | **Adversarial audit of Tracks 5 + 6.** 5/5 scripts run, 50/50 URLs real, 0 fabrications, 5 fixes applied with before→after, the AI-hours reconciliation, and the 13-item unverified register |
| [`reference/team-ops/01_championship_season_process.md`](reference/team-ops/01_championship_season_process.md) | 907 | How a championship-calibre season is actually run — phases, gates, design reviews, and §13.3's roboRIO-training shelf-life warning |
| [`reference/team-ops/02_design_cad_manufacturing.md`](reference/team-ops/02_design_cad_manufacturing.md) | 949 | Design → CAD → manufacturing for a bandsaw-and-drill-press shop, incl. outsourcing and the Systemcore packaging change |
| [`reference/team-ops/03_programming_stack.md`](reference/team-ops/03_programming_stack.md) `DONE` | 1102 | Elite software practice a small team can actually copy, under the 2027 Systemcore / WPILib transition |
| [`reference/team-ops/04_tuning_testing_competition_ops.md`](reference/team-ops/04_tuning_testing_competition_ops.md) | 1539 | Practice field, practice robot, driver development, reliability, spares/pit, match ops, batteries, alliance selection |
| [`reference/team-ops/04_competition_ops.yaml`](reference/team-ops/04_competition_ops.yaml) | — | Machine-readable companion: checklists, spares list, match-day timings |
| [`reference/team-ops/05_business_awards_sustainability.md`](reference/team-ops/05_business_awards_sustainability.md) `DONE` | 730 | The non-robot deliverables: FIRST Impact submission, business plan, sponsors, Team Sustainability Award evidence |
| [`reference/02_TEAM_CAPACITY_MODEL.md`](reference/02_TEAM_CAPACITY_MODEL.md) | 876 | Also the ops document: hours, roster, budget, tooling floor |
| [`reference/SCOUTING-PLAN.md`](reference/SCOUTING-PLAN.md) | 133 | Minimum-viable scouting for 15 students |
| [`ops/ai-hours.tsv`](ops/ai-hours.tsv) `NEW` | — | **Start this in September.** The AI time ledger every kill criterion in Track 6 reads from |
| [`ops/ATTRIBUTION.md`](ops/ATTRIBUTION.md) `NEW` | — | The one FIRST-compliant AI attribution line, copy-pasted and never retyped |
| [`README.md`](README.md) | — | Project entry point, layout, and evidence-label conventions |
| [`INDEX.md`](INDEX.md) | — | This file |

## Track 6 — AI integration

> **The season total, settled.** AI returns **40–70 effective hours** across the season — **7–12% of
> the 599 h** the capacity model says exist — against a per-row **ceiling of ≈106 h**. All **[S]**.
> It does **not** raise `novel_mechanisms_max`; it buys depth inside two mechanisms, not a third one.
> Reconciliation: [`00_WORKFLOW_MAP.md`](reference/ai-integration/00_WORKFLOW_MAP.md) §1.11a ·
> audit: [`reference/team-ops/00_AUDIT.md`](reference/team-ops/00_AUDIT.md) §9.

| File | Lines | One line |
|---|---:|---|
| [`reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md) | 74 | **The policy authority.** FIRST's official stance: AI is explicitly permitted; attribution is the one binding obligation; judges may not penalise AI use. Do not re-litigate |
| [`reference/ai-integration/00_WORKFLOW_MAP.md`](reference/ai-integration/00_WORKFLOW_MAP.md) | 710 | **Start here.** 66 tasks × traditional vs AI-assisted hours, mapped onto the 8 capacity lines; §1.11a reconciles the season total; 9 rows deliberately save nothing |
| [`reference/ai-integration/01_ai_for_programming.md`](reference/ai-integration/01_ai_for_programming.md) | 792 | Systemcore port, sim and tests, log analysis, the five-gate PR check, and why 2027 alpha APIs make model recall worse |
| [`reference/ai-integration/02_ai_for_design_and_cad.md`](reference/ai-integration/02_ai_for_design_and_cad.md) | 1293 | Design math and DFM — and the honest text-to-CAD verdict: it does not produce competition-ready geometry |
| [`reference/ai-integration/03_ai_for_analysis_and_scouting.md`](reference/ai-integration/03_ai_for_analysis_and_scouting.md) | 820 | Manual ingest, TBA/Statbotics, scouting pipelines, pre-match briefs, pick lists |
| [`reference/ai-integration/04_ai_for_docs_and_business.md`](reference/ai-integration/04_ai_for_docs_and_business.md) | 989 | Build thread, design decision records, award essays (AI as editor, never ghostwriter), sponsors, the knowledge base |
| [`reference/ai-integration/05_ai_infrastructure_and_policy.md`](reference/ai-integration/05_ai_infrastructure_and_policy.md) | 819 | Accounts and the **18+ problem**, three price tiers, nonprofit/EDU programs, scheduled automation, the `ops/ai-hours.tsv` ledger, kill criteria |
| [`reference/ai-integration/templates/frc-robot-CLAUDE.md`](reference/ai-integration/templates/frc-robot-CLAUDE.md) | 385 | Drop-in `CLAUDE.md` for the robot repo: 2027 API rules, the no-physical-numbers rule, the FRC-vs-FTC firewall. Six `TODO(team)` fields |
| [`reference/ai-integration/templates/team-ai-policy.md`](reference/ai-integration/templates/team-ai-policy.md) | 132 | **One page. Print it, sign it, send it home.** Matches the policy authority verbatim |
| [`reference/ai-integration/templates/programming-prompts.md`](reference/ai-integration/templates/programming-prompts.md) | 635 | Ready-to-paste programming prompts with their verification steps |
| [`reference/ai-integration/templates/design-prompts.md`](reference/ai-integration/templates/design-prompts.md) | 424 | Design-math and DFM prompts, pinned to `team_capacity.yaml`'s tooling level |
| [`reference/ai-integration/templates/analysis-prompts.md`](reference/ai-integration/templates/analysis-prompts.md) | 432 | Manual-ingest, Q&A-triage, scouting and pick-list prompts |
| [`reference/ai-integration/templates/docs-business-prompts.md`](reference/ai-integration/templates/docs-business-prompts.md) | 836 | Award, sponsor, grant and build-thread prompts, with the award-name and FTC firewalls baked in |
| [`reference/ai-integration/calculators/drivetrain.py`](reference/ai-integration/calculators/drivetrain.py) | 249 | Speed, traction vs torque limit, current draw, brownout trace. **Answers "gear down?"** |
| [`reference/ai-integration/calculators/elevator_arm.py`](reference/ai-integration/calculators/elevator_arm.py) | 336 | Elevator/arm torque, holding current, ratchet and gas-spring sizing |
| [`reference/ai-integration/calculators/fourbar.py`](reference/ai-integration/calculators/fourbar.py) | 303 | Four-bar Grashof check, transmission angle, coupler path, peak crank torque |
| [`reference/ai-integration/calculators/cg_tip.py`](reference/ai-integration/calculators/cg_tip.py) | 193 | CG, weight vs limits, tip-over stowed **and extended** |
| [`reference/ai-integration/calculators/motors.py`](reference/ai-integration/calculators/motors.py) | 111 | The shared motor table the other four import. Systemcore brownout threshold **UNVERIFIED** |
| [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md) | — | Contains the ready-to-paste LLM prompts for manual review, one per phase |
| [`STRATEGY-RANKING-SYSTEM.md`](STRATEGY-RANKING-SYSTEM.md) | — | Defines where a model is allowed to score and where a human must decide |

**All five calculators execute with no arguments and no dependencies beyond the standard library**
(`python reference/ai-integration/calculators/drivetrain.py`). Verified 5/5 on 2026-08-22 —
[`reference/team-ops/00_AUDIT.md`](reference/team-ops/00_AUDIT.md) §2.

## Track 7 — Tools (47 scripts in `tools/`, plus 7 award scripts under `reference/awards/`)

Run everything from the project root.

| Script | What it does |
|---|---|
| [`tools/probe-2027-manual.sh`](tools/probe-2027-manual.sh) | Sweeps known FRC CDN filename shapes for the 2027 manual (container listing is disabled, so the name must be guessed) |
| [`tools/ingest-manual.sh`](tools/ingest-manual.sh) | Takes a **local** manual PDF: text, rule inventory, diff vs prior season |
| [`tools/fetch-frc-manuals.sh`](tools/fetch-frc-manuals.sh) | Bulk-fetches historical manuals into `manuals/archive/frc/` |
| [`tools/rebuild-corpus.sh`](tools/rebuild-corpus.sh) | Rebuilds what this repository leaves out: `--fetch` downloads the FIRST PDFs, a bare run regenerates the excluded text from them, and `--help` lists the steps |
| [`tools/rules-full.py`](tools/rules-full.py) | Writes `<year>_rules_full.txt` from `<year>_bodies_v2.jsonl` |
| [`tools/award-text.py`](tools/award-text.py) | Extracts `reference/awards/_text/` from the award PDFs |
| [`tools/score-strategy.py`](tools/score-strategy.py) | **Ranking engine.** ACH × VAL, hard gates, quadrant, tier, binding constraint. `--from-corpus` back-tests |
| [`tools/bom-builder.py`](tools/bom-builder.py) | Mechanism list → priced BOM, 8 gate checks vs `team_capacity.yaml`, order-by schedule |
| [`tools/cycle-model.py`](tools/cycle-model.py) | Game-agnostic cycle-time / expected-value model; break-even on fixed endgame actions |
| [`tools/teamupdate-diff.py`](tools/teamupdate-diff.py) | `season <yr>` = what each Team Update changed; `slots` = which rule numbers churn across all seasons |
| [`tools/rule-inventory.py`](tools/rule-inventory.py) · [`tools/rule-show.py`](tools/rule-show.py) | Build and query the structured rule corpus |
| [`tools/rule-taxonomy-analyze.py`](tools/rule-taxonomy-analyze.py) · [`tools/rule-taxonomy-summarize.py`](tools/rule-taxonomy-summarize.py) | Classify rules by kind and summarise the distribution |
| [`tools/qa-rule-heat.py`](tools/qa-rule-heat.py) | Q&A volume per rule → the ambiguity hotspot map |
| [`tools/frc_qa_scrape.py`](tools/frc_qa_scrape.py) · [`tools/frc_diff.py`](tools/frc_diff.py) · [`tools/frc_spans.py`](tools/frc_spans.py) | Q&A scrape, manual diff, section-span extraction |
| [`tools/capacity_model.py`](tools/capacity_model.py) | Regenerates the hour allocation in `team_capacity.yaml` |
| [`tools/rubric_weights.py`](tools/rubric_weights.py) | Derives rubric weights from `04_predictive_factors.yaml` |
| [`tools/backtest_specialists.py`](tools/backtest_specialists.py) · [`tools/validate_winner_seed.py`](tools/validate_winner_seed.py) | Back-test harnesses for the specialist thesis and the seed→win claims |
| `tools/predictive_factor_stats*.py` (6 files) | Successive TBA statistical passes behind `04_PREDICTIVE_FACTORS.md` |
| [`tools/tba_predictive_scrape.py`](tools/tba_predictive_scrape.py) · [`tools/tba_copr_scrape.py`](tools/tba_copr_scrape.py) · [`tools/tba_award_scrape.py`](tools/tba_award_scrape.py) | TBA ingestion |
| [`tools/award_patterns.py`](tools/award_patterns.py) · [`tools/award_target_rank.py`](tools/award_target_rank.py) · [`tools/award_winner_forensics.py`](tools/award_winner_forensics.py) | Award analysis |
| [`reference/awards/award_diff.py`](reference/awards/award_diff.py) · [`award_novelty.py`](reference/awards/award_novelty.py) · [`award_aim.py`](reference/awards/award_aim.py) · [`kickoff_award_check.sh`](reference/awards/kickoff_award_check.sh) | Award-name drift detection — run `kickoff_award_check.sh` against Manual V1 |
| [`reference/awards/fetch_award_pages.py`](reference/awards/fetch_award_pages.py) · [`fetch_award_pdfs.py`](reference/awards/fetch_award_pdfs.py) · [`manual_award_order.py`](reference/awards/manual_award_order.py) | Award source fetchers and ceremony-order extraction |
| [`tools/defense_rule_trend.py`](tools/defense_rule_trend.py) | Long-run trend in defense-related rules |
| [`tools/scouting-plan.py`](tools/scouting-plan.py) | Generates the scouting sheet from what FMS does not publish |
| [`tools/cd_fetch.py`](tools/cd_fetch.py) · [`tools/wb_fetch.py`](tools/wb_fetch.py) · [`tools/wb_tryall.py`](tools/wb_tryall.py) | Chief Delphi and Wayback fetchers |
| [`tools/RUN-KICKOFF.sh`](tools/RUN-KICKOFF.sh) | The one kickoff-day command: phase 1 mechanical extraction, self-diff banner, extraction sanity gate |
| [`tools/cite-check.py`](tools/cite-check.py) · [`tools/cad-linkcheck.sh`](tools/cad-linkcheck.sh) | Verify rule citations against the extracted manual; verify CAD and sourcing URLs still resolve |
| [`tools/score-priors.py`](tools/score-priors.py) · [`tools/match-sim.py`](tools/match-sim.py) | Data-grounded priors for the cycle model; Monte Carlo match simulator |
| [`tools/prematch-brief.py`](tools/prematch-brief.py) · [`tools/log-report.py`](tools/log-report.py) | One index card per match from public data; WPILOG to summary JSON/CSV |
| [`tools/award_availability.py`](tools/award_availability.py) | Award availability recomputed from TBA 2026 award rows |

---

## Validation / dry-run

Confirm the workbench is intact before kickoff. Every command below was executed 2026-08-22; the
expected output is recorded in [`reference/00_SYSTEM_AUDIT.md`](reference/00_SYSTEM_AUDIT.md).

```bash
# Run from the repository root. On a fresh clone, run the corpus rebuild first
# (bash tools/rebuild-corpus.sh --fetch, then bash tools/rebuild-corpus.sh; see README.md).
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml | tail -8   # expect 27/30 = 90%
python tools/bom-builder.py reference/bom/examples/simple.yaml    | grep VERDICT         # ALL GATES PASS
python tools/bom-builder.py reference/bom/examples/ambitious.yaml | grep VERDICT         # FAILS 8 GATE(S)
python tools/cycle-model.py --game rebuilt | grep -A4 Break-even
python tools/teamupdate-diff.py slots | tail -3
bash reference/bom/recheck_prices.sh          # vendor URL sweep
bash reference/awards/kickoff_award_check.sh  # award-name drift vs the manual

# Track 5 + 6 audit: calculators, FTC sweep, retired-award sweep (team-ops/00_AUDIT.md sec 0)
for f in reference/ai-integration/calculators/*.py; do python "$f" >/dev/null && echo "PASS $f"; done
grep -rniE "pollen|starterbot|skill.?build|september 12" reference/team-ops reference/ai-integration
```

## Files written by this pass

| File | What |
|---|---|
| `INDEX.md` | This file |
| `reference/00_SYSTEM_AUDIT.md` | Audit of award names, code execution, rubric stress tests, FTC contamination, part URLs, arithmetic |
| `reference/00_system_audit.yaml` | Machine-readable audit result |
| `README.md` | Edited to link `INDEX.md` |
| `reference/team-ops/00_AUDIT.md` | Audit of Tracks 5 + 6: scripts executed, URLs curled, hours reconciled, FTC and Systemcore sweeps, fixes with before→after |
| `INDEX.md` (Tracks 5 + 6) | Expanded to list every team-ops, AI-integration, template, calculator and playbook file |

## Known limitations

1. **Line counts are as of 2026-08-22.** They drift as files are edited; they are a size hint, not a checksum.
2. **`manuals/2026-27_BIOCORE/` is empty until kickoff.** Every BIOCORE-specific claim in this repo is
   pre-manual and must be re-checked on 2027-01-09.
3. **The Sept 24 / Nov 12 / Nov 17 dates are FIRST-published season dates** and have moved in past
   seasons. Re-verify against firstinspires.org before treating any as a hard PO deadline.
4. **This index does not judge quality.** A file being listed is not a claim that it is right — that is
   what [`reference/00_SYSTEM_AUDIT.md`](reference/00_SYSTEM_AUDIT.md) is for.
5. `research/rule_inventories/` and `manuals/` are summarised at directory level; individual TSVs and
   PDFs are not enumerated here.
6. **Two files are listed under more than one track on purpose.** `team-ops/04` and `team-ops/05`
   appear under both Awards and Team ops; `KICKOFF_PLAYBOOK.md` and `SMALL_TEAM_PLAYBOOK.md` appear
   under both Team ops and AI integration. They are single files, not duplicates.
7. **The 40–70 h AI figure in Track 6 is [S] and untested.** It is a planning hypothesis with a
   documented falsification procedure (`ops/ai-hours.tsv`, settled April 2027), not a measurement.
