# The Workflow Map — for every task we do, what is the AI-assisted way to do it?

**Purpose.** One table you can open on any day of the 2027 season and answer: *is there a faster way
to do this, what does a human still have to check, and what breaks if the machine is wrong?* Every
other file in `reference/ai-integration/` is depth on one column of this table. This file is the
index and the arithmetic.

**Companion files (this file does not repeat them — it points at them):**

| File | What it owns |
|---|---|
| [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) | **The policy authority.** AI is permitted; attribution is mandatory. Do not re-litigate |
| [`01_ai_for_programming.md`](01_ai_for_programming.md) | Systemcore port, sim/tests, log analysis, the five-gate PR check |
| [`02_ai_for_design_and_cad.md`](02_ai_for_design_and_cad.md) | Design math, calculators, DFM, the honest text-to-CAD verdict |
| [`03_ai_for_analysis_and_scouting.md`](03_ai_for_analysis_and_scouting.md) | Manual ingest, TBA/Statbotics, scouting, pre-match briefs, pick lists |
| [`04_ai_for_docs_and_business.md`](04_ai_for_docs_and_business.md) | Build thread, DDRs, awards, sponsors, the knowledge base |
| [`05_ai_infrastructure_and_policy.md`](05_ai_infrastructure_and_policy.md) | Accounts, tiers, automation, the `ops/ai-hours.tsv` log, kill criteria |
| [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml) | **`CM` — the hours authority.** Every number in §1 is reconciled to it |
| [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) | **`PF`** — drive practice weighted 90, reliability 88. The destination for saved hours |
| [`../ACHIEVABILITY-RUBRIC.md`](../ACHIEVABILITY-RUBRIC.md) · [`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) | Scope gate; scouting scheme referenced by rows 46–49 |
| [`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md) · [`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md) | The kickoff schedule §3.A slots into; the ranking §3.A step 8 runs |

## Evidence labels

| Label | Meaning | Where it appears here |
|---|---|---|
| **[C]** CONFIRMED | Verified against a primary source or a run of our own tool | Dates, FIRST policy, tool behaviour, cycle-model output |
| **[H]** HISTORICAL-PATTERN | True of past seasons; expected but not guaranteed for 2027 | Season shape, event-day rhythms |
| **[S]** SPECULATION | Model output or a calibrated estimate | **Every hours figure in §1.** All of them. Without exception |
| **UNVERIFIED** | Named so you do not accidentally trust it | 2027 Systemcore pinouts, 2027 rules, 2027 award deadlines |

> **The single most important caveat in this document.** *Traditional hours* and *AI-assisted hours*
> in §1 are **[S]** planning estimates, not measurements. Nobody has run a season this way and
> measured it. `05_ai_infrastructure_and_policy.md` §8 and §5 of this file tell you how to convert
> them to **[C]** by April 2027. Until then, treat the totals as a *hypothesis you are testing*, and
> make no purchase you would regret if the hypothesis is half true.

---

## §0. The 60-second workflow

```bash
# Run from the repository root.

# ---- 1. What does the season actually give us? (2 s) ------------------------------
python tools/capacity_model.py            # the 599 effective-hour budget and the 8 lines
                                          # THE number to remember: zero slack at 15 h/wk -> Week 1

# ---- 2. What is one second of cycle time worth? (1 s) -----------------------------
python tools/cycle-model.py --game rebuilt --cycle 8
#   -> "Going from 8.0s to 9.0s costs 9.7 points/match."      [C, run 2026-08-22]
#   -> "Over a 12-match qualification schedule: 117 points."
#   This is the exchange rate that makes SECTION 2 an argument instead of an opinion.

# ---- 3. Open the table --------------------------------------------------------------
#   Section 1 below. Find your task. Read columns 6, 7, 8 -- tool, verification, risk.
#   If your task is NOT in the table, the default answer is "do it by hand" (see 4.1).

# ---- 4. Start the ledger. Today. -----------------------------------------------------
mkdir -p ops
[ -f ops/ai-hours.tsv ] || printf 'date\twho\tarea\trow\ttask\test_solo_min\tactual_min\treview_min\tverified_by\taccepted\tnotes\n' > ops/ai-hours.tsv
#   Two weeks of UN-assisted baseline first (05_ai_infrastructure sec 8.4). Then turn AI on.

# ---- 5. The compliance one-liner (zero cost, non-negotiable) --------------------------
#   Put this in the repo README and on every award submission:
#   "Portions of this work were created by Team <NNNN> with AI assistance (Claude)."
#   Source: 00_FIRST_AI_POLICY_VERIFIED.md. [C]
```

---

## §1. The master table

**How to read the columns.**

- **Bucket code** in the Task cell: **(R)** = the saving is *returned* into the 599 h in-season
  budget · **(D)** = the saving *relieves demand* that was never going to fit anyway (the artifact
  now exists; no transferable hour appears) · **(O)** = off-season, outside the 599 h model
  entirely · **(0)** = **no saving, listed on purpose** so nobody imagines this compresses.
- **Traditional h** = unassisted task demand **[S]**. It is *demand*, not *funded hours*. Several
  lines below demand more than `CM` funds — that is the real finding, not an error.
- **Hours saved** = Traditional − AI-assisted, and it is **capped per line** in §1.9. Read §1.9
  before quoting any total.
- Grouping follows the eight mandatory lines of `CM` §3.1 so the reconciliation is checkable.

### 1.1 Game analysis, rules, strategy — charged to `strategy_rules` (25.0 h)

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | **(R)** Kickoff manual ingest + section map | Strategy lead + mentor | 6.0 | 2.5 | **3.5** | `tools/ingest-manual.sh` → text; then a 3-pass LLM read (scoring / constraints / edge cases) per `03` §1 | Every rule number quoted must be opened in the PDF. Spot-check 10 | **Severe.** Fabricated rule numbers are the #1 documented failure (`04` §8.1). A phantom rule sends you down a strategy dead end for a week |
| 2 | **(R)** Rule inventory + scoring-rule extraction | Strategy #2 | 4.0 | 1.5 | **2.5** | `tools/rule-inventory.py`, `tools/rule-show.py` — deterministic, not an LLM | Row count vs. the manual TOC | Low — the tool is deterministic; failure is loud |
| 3 | **(R)** Author the BIOCORE game file for the EV model | Strategy lead | 5.0 | 2.0 | **3.0** | LLM reads manual scoring section → emits `mygame.json`; run `tools/cycle-model.py --game mygame.json` | **Every point value, by hand, against the manual.** Then `--sweep` and check the shape | **Severe.** Wrong point values → wrong mechanism priority → wrong robot |
| 4 | **(R)** Strategy ranking + archetype shortlist | Strategy + mentor | 4.0 | 1.5 | **2.5** | `tools/score-strategy.py` + `STRATEGY-RANKING-SYSTEM.md`; LLM fills inputs, the script ranks | The inputs, not the output. Garbage in is invisible | Medium — a plausible ranking built on invented capability estimates |
| 5 | **(R)** Q&A ambiguity triage, weekly ×7 | Strategy #2 | 5.0 | 2.0 | **3.0** | `tools/frc_qa_scrape.py` + `tools/qa-rule-heat.py` → LLM clusters into `QA-AMBIGUITY-HOTSPOTS.md` | Read the actual Q&A answer for anything you act on | Medium — an LLM paraphrase of a Q&A answer is not the answer |
| 6 | **(R)** Team Update diff, weekly ×7 | Strategy #2 | 4.0 | 1.0 | **3.0** | `tools/teamupdate-diff.py` (deterministic diff) + LLM impact note | The diff is trustworthy; the impact note is not | Low–medium |
| 7 | **(R)** Rule-churn / penalty watchlist upkeep | Safety captain | 2.0 | 0.8 | **1.2** | LLM maintains `RULE-CHURN-WATCHLIST.md` from the diffs | Mentor reads it before each event | Medium — a missed rule change is an inspection failure |
| 8 | **(0)** Game-strategy decision meeting (kickoff Sat–Sun) | Whole team | 8.0 | 8.0 | **0.0** | **None. The machine does not attend** | — | **The most important eight hours of the season.** Any tool that shortens this is doing damage |
| | **Subtotal** | | **38.0** | **19.3** | **18.7** | Budget **25.0 h** — unassisted demand is **152%** of the line | | |

### 1.2 Design, CAD, design math — charged to `cad_design` (74.9 h)

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 9 | **(R)** Gear ratio / free-speed / current-draw math | Design math | 6.0 | 2.0 | **4.0** | **`calculators/drivetrain.py`, `calculators/motors.py`** — deterministic Python, *not* an LLM doing arithmetic | Re-run with a second set of inputs; check units | Low if you use the calculators. **High if you let the model do arithmetic in prose** (`02` §3) |
| 10 | **(R)** Arm / elevator torque + load sanity check | Design math | 5.0 | 2.5 | **2.5** | `calculators/elevator_arm.py`, `calculators/fourbar.py`, `calculators/cg_tip.py` | Independent hand-check of one load case; mentor signs | **High.** An under-torqued arm is a season-long tuning nightmare; a tip-over is a safety event |
| 11 | **(R)** Motor / gearbox selection trade study | Design + mentor | 5.0 | 2.0 | **3.0** | LLM builds the option matrix; `reference/bom/mechanism_catalog.yaml` supplies real parts and prices | **Every price and part number against the vendor page** | Medium–high — a fabricated part number wastes an order cycle you do not have |
| 12 | **(0)** CAD modelling of custom parts | CAD lead | 30.0 | 28.0 | **2.0** | Essentially none. `02` §2 is unambiguous: **text-to-CAD does not produce competition-ready geometry in 2026.** AI helps only with macro/script boilerplate and naming | All of it | **This row exists to kill a specific fantasy.** Budgeting CAD savings you will not get is how a season goes wrong |
| 13 | **(R)** COTS part selection + fit check | CAD | 6.0 | 3.0 | **3.0** | LLM queries `reference/bom/*.yaml` (local, already-verified data) rather than the open web | Vendor page for stock and price, every line | Medium — stale price/stock rather than fabrication, if you keep it to local YAML |
| 14 | **(R)** Assembly drawings / build instructions | CAD | 5.0 | 3.0 | **2.0** | AI writes the *prose* around your exported views; it cannot make the views | A builder follows it once, cold | Low |
| 15 | **(R)** DFM review against our tooling level | CAD + mentor | 4.0 | 2.0 | **2.0** | Prompt includes `tooling.level: bandsaw_drillpress` from `team_capacity.yaml`; AI flags anything needing a mill/CNC | Mentor. Always | Medium — a part you cannot make is discovered at the saw, not at the screen |
| 16 | **(R)** Design Decision Records ×10 | Design lead | 5.0 | 1.5 | **3.5** | `04` §2.2 DDR template; AI drafts from a 5-minute voice note | The Decision line and the Evidence line must be human-written | Low — and DDRs are direct award evidence (`awards/AWARD-ALIGNMENT.md`) |
| | **Subtotal** | | **66.0** | **45.0** | **21.0** | Budget **74.9 h**. The most optimistic block in the table — see §1.11 and Limitation 3 | | |

### 1.3 Manufacturing planning + fabrication — charged to `fabrication_assembly` (129.8 h)

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 17 | **(R)** Cut lists + stock-length optimisation | Build lead | 4.0 | 1.5 | **2.5** | LLM from the CAD BOM; demand the arithmetic be shown | Total stock length by hand; measure twice anyway | Medium — wasted extrusion is money out of a $2,500 discretionary line |
| 18 | **(R)** Manufacturing plan / build order / critical path | Build lead + mentor | 5.0 | 1.5 | **3.5** | LLM sequences from the DDRs + real lead times; mentor edits | The critical path, against actual vendor lead times | Medium — a bad sequence idles the shop |
| 19 | **(R)** Jig + fixture design for a bandsaw/drill-press shop | Build | 4.0 | 2.5 | **1.5** | Conversational design review, not generation | Build it and test on scrap | Medium |
| 20 | **(0)** Machining, drilling, riveting, assembly | Build team | 100.0 | 100.0 | **0.0** | **None. AI does not turn wrenches.** The largest single line in `CM`, and untouched | — | — |
| 21 | **(R)** Outsourced-part packet prep (DXF / tolerance checks) | CAD + build | 3.0 | 1.5 | **1.5** | LLM checklist against the vendor's stated capabilities | The vendor's own DFM checker | Medium — a rejected order costs 2 weeks (`team_capacity.yaml: outsourcing_lead_time_weeks: 2`) |
| 22 | **(R)** Spares + consumables list | Build | 2.0 | 0.5 | **1.5** | LLM from the BOM against `spares_consumables: $500` | Mentor scans for the obvious omission | Low |
| | **Subtotal** | | **118.0** | **107.5** | **10.5** | Budget **129.8 h**. **8.9% saved — the lowest ratio in the table, and that is correct** | | |

### 1.4 Wiring + electrical — charged to `electrical_pneumatics` (49.9 h)

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 23 | **(R)** Wiring diagram + CAN topology + power budget | Electrical lead | 6.0 | 2.5 | **3.5** | LLM drafts a device / CAN-ID / breaker table; keep it in the repo as text so it diffs | Every device against its own datasheet | Medium–high |
| 24 | **(R)** Systemcore harness + connector/pinout plan | Electrical + mentor | 5.0 | 2.5 | **2.5** | LLM structures the plan; **it does not know 2027 pinouts** | **UNVERIFIED until the 2026-11-12 Kit Release and the 2027 docs.** Verify every pin against FIRST/vendor documentation | **Severe.** A wrong pinout is released magic smoke on a control system you may not be able to replace |
| 25 | **(R)** Breaker + wire-gauge sizing check | Electrical | 3.0 | 1.0 | **2.0** | `calculators/motors.py` current figures → gauge table; AI cross-reads the rule | The rule text and an ampacity table | **High.** Under-gauged wire is a fire risk and an inspection failure |
| 26 | **(0)** Physical wiring, crimping, labelling, routing | Electrical team | 30.0 | 30.0 | **0.0** | **None** | — | — |
| 27 | **(R)** Pneumatics sizing, if used | Electrical | 3.0 | 1.5 | **1.5** | `02` §3 calculators + LLM narration | Cylinder force by hand | Medium–high |
| 28 | **(R)** Pre-inspection electrical self-check | Electrical + safety | 3.0 | 1.0 | **2.0** | AI turns the inspection checklist into a per-robot punch list | **The official checklist — not the AI's memory of it** | High — an inspection failure on Thursday costs you Friday |
| | **Subtotal** | | **50.0** | **38.5** | **11.5** | Budget **49.9 h** — unassisted demand is exactly the line, with zero margin | | |

### 1.5 Programming, simulation, testing — charged to `programming` (134.8 h)

> `CM` §3.2: this is **the tightest line in 2027 and it is not close** — inflated ~40 h purely by the
> Systemcore platform change. It is also where AI pays the most. Those two facts together are the
> whole reason this project exists.

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 29 | **(R)** roboRIO → Systemcore / WPILib 2027 port | Lead programmer | 40.0 | 22.0 | **18.0** | `01` §3.2 — mechanical, well-specified translation with a compiler as the oracle. Rule table lives in `templates/frc-robot-CLAUDE.md` | Compile + sim + the five-gate check (`01` §5) | **Medium–high.** A mis-ported unit or sign moves a real mechanism the wrong way |
| 30 | **(R)** Subsystem scaffolding from a written spec | Programmer 2 | 20.0 | 12.0 | **8.0** | `01` §3.3 + `templates/programming-prompts.md`. **The student writes the spec first** | Five-gate check; the student explains it at review | Medium |
| 31 | **(R)** `*IOSim` classes + JUnit tests | Programmers | 26.0 | 8.0 | **18.0** | `01` §3.1 — **rank-1 payoff.** WPILib physics sims; the `createRobotContainer()` smoke test in the first hour | `./gradlew test`, and **read the assertions yourself** | **Low — nothing actuates.** The one real risk is a tautological test. Student writes assertion values from the spec *first* |
| 32 | **(R)** Porting vendor examples into our architecture | Programmers | 10.0 | 6.0 | **4.0** | `01` §3.5 | **Every symbol against the vendor Javadoc** | **High.** Hallucinated vendor APIs live here — the most common code failure mode |
| 33 | **(R)** Auto routine + path scaffolding | Programmers | 10.0 | 6.5 | **3.5** | `01` §3.8 | Sim, then a slow-speed field run | Medium |
| 34 | **(R)** Code review for classic FRC bugs | Mentor + lead | 8.0 | 4.0 | **4.0** | `01` §3.4 review prompt on every PR | A human triages every finding; false positives cost minutes | **Low — it finds bugs, it does not create them** |
| 35 | **(R)** SysId characterisation → constants | Programmer + mentor | 5.0 | 3.0 | **2.0** | `01` §3.7 | Sim first, then five-gate | **High.** A fabricated kV/kA drives a mechanism into a hard stop at full authority |
| 36 | **(R)** Post-match WPILOG review, per match | Pit programmer | 8.0 | 3.0 | **5.0** | `tools/log-report.py` → signal summary → LLM engineering note (`01` §7). Runbook §3.C | Cross-check one claim in AdvantageScope by hand | **Low — read-only, produces prose.** But `log-report.py` is **untested against a real log** (`01` §7.2) |
| 37 | **(R)** Vision / localisation bring-up | Programmers | 12.0 | 9.0 | **3.0** | Config and calibration narration only | On-field measurement | Medium |
| 38 | **(0)** On-robot debugging in the shop | Programmers | 20.0 | 20.0 | **0.0** | **None. AI cannot see your robot**, hear the gearbox, or feel the backlash | — | — |
| | **Subtotal** | | **159.0** | **93.5** | **65.5** | Budget **134.8 h** — unassisted demand is **118%** of the line. This block decides the season | | |

### 1.6 Integration, tuning, testing — charged to `integration_debug` (84.9 h)

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 39 | **(R)** Test plan + reliability checklist authoring | Mentor + lead | 5.0 | 1.5 | **3.5** | LLM from `team-ops/04_tuning_testing_competition_ops.md`; `PF` weights reliability **88** | Mentor edits; run it once and prune | Low |
| 40 | **(R)** Failure log → ranked root-cause hypotheses | Whole team | 6.0 | 2.5 | **3.5** | LLM ranks hypotheses from the failure log + match logs. **It proposes; you test** | You test the hypothesis. Never "fix" on an unverified diagnosis | **Medium–high.** A confident wrong diagnosis burns a whole build night |
| 41 | **(0)** Actual integration, tuning, hardening | All | 70.0 | 70.0 | **0.0** | **None** | — | — |
| 42 | **(R)** Match-replay / video-note triage | Strategy | 5.0 | 3.0 | **2.0** | Humans timestamp, AI structures the notes. `03` §4: **automated match-video analysis is not realistic in 2026** — do not build a pipeline | Watch the clip | Low if kept to note-structuring; **high value destroyed** if you build the pipeline instead |
| | **Subtotal** | | **86.0** | **77.0** | **9.0** | Budget **84.9 h** | | |

### 1.7 Driver practice — charged to `drive_practice` (54.9 h)

> **This is the one line we are trying to make bigger, not smaller.** `CM` §3.4 converts the 54.9 h
> budget into **≈9 meaningful driver hours before event 1** and calls it the model's most alarming
> output. `PF` weights drive practice at **90 — the highest factor in the measured corpus.**

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 43 | **(R)** Practice-plan design + drill sequencing | Drive coach | 4.0 | 1.5 | **2.5** | LLM builds a drill ladder from the cycle-model output, targeting the specific second you are trying to buy | The coach owns it; drills must be measurable with a stopwatch | Low |
| 44 | **(R)** Driver performance review from cycle logs | Drive coach | 4.0 | 1.5 | **2.5** | `tools/log-report.py` cycle times → LLM trend note | The stopwatch | Low |
| 45 | **(0)** Driving, field reset, spotting, coaching | Drive team | 47.0 | 47.0 | **0.0** | **None, and no simulator substitutes for the last hour before a match.** (`CM` §3.4 *does* endorse sim and controller-in-hand rehearsal as **free** additions outside the 15 h/wk) | — | — |
| | **Subtotal** | | **55.0** | **50.0** | **5.0** | Budget **54.9 h**. **The 4.9 h of headroom stays in this line as seat time** | | |

### 1.8 Scouting, match strategy, awards, business, outreach, admin — charged to `awards_business` (44.9 h)

> `04` §7 already found the honest version of this: unassisted demand here runs several times the
> funded line. That is why small teams simply do not produce these artifacts. AI does not return
> hours here so much as it makes the artifacts *exist at all*.

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 46 | **(D)** Scouting schema + data dictionary | Scouting lead | 5.0 | 1.5 | **3.5** | `tools/scouting-plan.py` + `SCOUTING-PLAN.md`; AI proposes fields from the manual on kickoff day | Field count vs. **3–5 available scouts** (`CM` §4.4). Cut ruthlessly | Medium — an over-wide schema produces no usable data at all |
| 47 | **(D)** Scout training + assignment sheets | Scouting lead | 3.0 | 1.0 | **2.0** | LLM writes the one-page scout card | Run one mock match against video | Low |
| 48 | **(D)** Match data → pick list | Strategy + scouting | 8.0 | 3.0 | **5.0** | `tools/tba_*.py` + `tools/match-sim.py` → ranked list. Runbook §3.D | **Eyes on every top-24 robot.** Data ranks; humans pick | **High.** A pick made on bad data is unrecoverable — see §4.6 |
| 49 | **(D)** Pre-match opponent / partner briefs ×12 | Strategy | 6.0 | 1.5 | **4.5** | `tools/prematch-brief.py` (`03` §5) | The drive coach reads it *before*, not during, the match | Low–medium |
| 50 | **(R)** Alliance-selection decision prep | Strategy + mentor | 4.0 | 2.0 | **2.0** | `03` §7 — AI assists the *preparation*; **the pick stays human** | The whole thing | High if delegated; low if used as prep |
| 51 | **(D)** Build thread + social posts, 7 weeks | Media | 8.0 | 2.3 | **5.7** | `04` §2.1 from meeting notes. Runbook §3.E | Read before posting. Public and permanent | Medium — a wrong technical claim in public is an award liability |
| 52 | **(D)** Meeting minutes → knowledge base | Rotating | 4.5 | 1.2 | **3.3** | `04` §6 KB structure. **Charge this to the meeting it happens inside** | Skim | Low |
| 53 | **(D)** Impact / Engineering Inspiration essay | Awards lead | 16.0 | 6.5 | **9.5** | `04` §3 — **AI as editor and coach, never ghostwriter.** Students supply every fact | Every claim, number and name | **Severe.** A fabricated outreach statistic in an award essay is an integrity finding, not a typo |
| 54 | **(D)** Executive summaries (character-limited) | Awards | 3.0 | 1.0 | **2.0** | Compression is a genuine AI strength. The 500-char limit is **[C] for 2026**, **UNVERIFIED for 2027** | Character count, by machine | Low |
| 55 | **(0)** Judge Q&A + pit interview rehearsal | Whole team | 5.0 | 5.0 | **0.0** | AI can play the judge in a mock; it cannot answer for you (`04` §3) | — | **Judges talk to students.** Any hour "saved" here should go straight back in |
| 56 | **(D)** Sponsor letters, thank-yous, stewardship | Business | 8.0 | 3.0 | **5.0** | `04` §4; `templates/docs-business-prompts.md` | Names, amounts, spellings. Every one | Medium–high — a misspelled sponsor name costs a sponsor |
| 57 | **(D)** Grant applications | Business + mentor | 6.0 | 2.5 | **3.5** | Boilerplate reuse + tailoring | Every factual claim; eligibility rules | **High** — false statements on a grant application are serious |
| 58 | **(D)** Outreach planning + media | Outreach lead | 16.0 | 4.0 | **12.0** | `04` §5 | Event details against reality | Low–medium |
| 59 | **(D)** Pit ops: layout, packing list, event checklists | Pit boss | 4.0 | 1.5 | **2.5** | `team-ops/04_tuning_testing_competition_ops.md` → AI generates a per-event packing list | Physically check the crate against it | Medium — a missing part at an event is an unforced loss |
| 60 | **(R)** Registration, travel, forms, parent comms | Mentor | 10.0 | 6.0 | **4.0** | Drafting and tracking only. **Never let AI submit anything** | The mentor submits, always | **Deadlines are hard.** Kit & Kickoff selection closes **2026-11-17**; BOM order-by **2026-11-21** [C] |
| | **Subtotal** | | **106.5** | **42.0** | **64.5** | Budget **44.9 h** — unassisted demand is **237%** of the line | | |

### 1.9 The reconciliation — what the totals actually mean

**A saving inside a line can only be *returned* up to the point where the assisted work fits inside
the funded line.** Beyond that, the saving is real but it was relieving demand that never fit. Both
are valuable; only one is a transferable hour.

| `CM` line | Budget | Trad. demand | AI-assisted | Nominal saved | **Returned** = min(saved, budget−assisted) | Demand relieved |
|---|---:|---:|---:|---:|---:|---:|
| `strategy_rules` | 25.0 | 38.0 | 19.3 | 18.7 | **5.7** | 13.0 |
| `cad_design` | 74.9 | 66.0 | 45.0 | 21.0 | **21.0** | 0.0 |
| `fabrication_assembly` | 129.8 | 118.0 | 107.5 | 10.5 | **10.5** | 0.0 |
| `electrical_pneumatics` | 49.9 | 50.0 | 38.5 | 11.5 | **11.4** | 0.1 |
| `programming` | 134.8 | 159.0 | 93.5 | 65.5 | **41.3** | 24.2 |
| `integration_debug` | 84.9 | 86.0 | 77.0 | 9.0 | **7.9** | 1.1 |
| `drive_practice` | 54.9 | 55.0 | 50.0 | 5.0 | **4.9** | 0.1 |
| `awards_business` | 44.9 | 106.5 | 42.0 | 64.5 | **2.9** | 61.6 |
| **TOTAL, in-season** | **599.1** | **678.5** | **472.8** | **205.7** | **≈105.6 h** | **≈100.1 h** |

### 1.10 Off-season rows — outside the 599 h model entirely

Hours between now (2026-08-22) and kickoff (2027-01-09) are *not* in `CM`'s 599. They are separately
scarce, and they are the cheapest hours you will ever spend. **[H]**

| # | Task | Owner | Trad. h | AI h | Saved | AI tool + how | Human must verify | Risk if AI is wrong |
|---|---|---|---:|---:|---:|---|---|---|
| 61 | **(O)** Team handbook, safety plan, shop checklists | Mentor + safety | 10.0 | 2.5 | **7.5** | `04` §2.6 | Mentor + school sign-off | Medium — safety documents must be right |
| 62 | **(O)** Onboarding curriculum + training lessons | Mentor | 12.0 | 4.0 | **8.0** | `05` §7 four-session curriculum. **Anything roboRIO-API-specific has a shelf life — teach concepts, not APIs** | Mentor teaches it once and edits | **Medium.** Training students on a stack that dies in January is wasted time |
| 63 | **(O)** `CLAUDE.md` repo contract + KB skeleton | Lead prog + mentor | 6.0 | 2.0 | **4.0** | `templates/frc-robot-CLAUDE.md` — six `TODO(team)` fields | Fill the TODOs honestly | Low cost, high leverage |
| 64 | **(0)** Base subsystem library | Programmers | 12.0 | 12.0 | **0.0** | **Humans write this. Not AI.** (`01` §9, December 2026) | — | **This is the learning.** Generating it is anti-pattern §4.2 |
| 65 | **(O)** Sponsor list, grant boilerplate, business plan | Business | 10.0 | 4.0 | **6.0** | `team-ops/05_business_awards_sustainability.md` + `04` §4 | Every name and figure | Medium |
| 66 | **(O)** Preseason BOM / vendor research, KoP gap list | Mentor + build | 8.0 | 3.0 | **5.0** | `tools/bom-builder.py` against `reference/bom/*.yaml`; **Virtual Kit Release 2026-11-12** [C] | Vendor pages; `reference/bom/recheck_prices.sh` | Medium — stale prices distort the $2,500 plan |
| | **Subtotal** | | **58.0** | **27.5** | **30.5** | Do this work **now**. It is the only kind of hour you can still create | | |

### 1.11 GRAND TOTAL

| Quantity | Hours | As a fraction |
|---|---:|---|
| **Effective hours returned into the 599 h in-season budget** | **≈105.6** | **17.6% of 599.1** |
| Demand relieved — artifacts that now exist; not transferable hours | ≈100.1 | — |
| Off-season hours freed (outside the model) | ≈30.5 | — |
| Nominal "hours saved" if you naively add every row — **do not quote this** | 236.2 | — |
| **Rows in the table** | **66** | of which **9 save nothing, by design** |

### 1.11a Reconciliation with the other two files that state a season total — read this

`[AUDIT 2026-08-22, team-ops + AI audit]` Three files in this project stated a season total and they
did not agree. They now say the same thing, and it is this:

| Number | What it is | Where |
|---:|---|---|
| **≈106 h** | **Ceiling.** Every one of the 57 saving rows delivers its **[S]** estimate in full, capped per `CM` line | §1.9 / §1.11 of this file |
| **40–70 h** | **The number to plan and budget against.** A 40–65% realisation rate on the ceiling | `05_ai_infrastructure_and_policy.md` §8.2 · `../../SMALL_TEAM_PLAYBOOK.md` §"Season total" |
| **0 h** | What you get if nobody keeps `ops/ai-hours.tsv` | §5 |

**Why a realisation rate below 1.0 is the honest default [S]:** rows are estimated one at a time and
optimistically; review time is under-counted for the person who has to read the output cold; some
rows will be abandoned after two attempts; and the 2027 alpha-API problem (`01` §4) makes the
programming rows — the largest block — worse than a normal year, not better. Nobody has run an FRC
season this way and measured it. Assume 40–70 h, be pleased at 106.

**So: the number to quote is 40–70 hours, or roughly 7–12% of the season**, with ≈106 h as the
ceiling you are testing against. It is **[S]**. At the midpoint (55 h) it is roughly **1.2 weeks of
team output** at 44 nominal person-hours/week. **It is not a third mechanism** — §2.4.

---

## §2. Where the saved hours should go

### 2.1 The allocation

The table below allocates the **≈106 h ceiling**. The right-hand column is the same allocation at the
**55 h planning midpoint** (§1.11a) — that is the one to actually schedule. Either way the rule is the
same: **enough to change one thing decisively or four things marginally. Change one thing.** If you
only get 40 h, fund the drive-practice row and stop.

| Destination | Hours | New line total | Why this and not something else |
|---|---:|---|---|
| **Drive practice** | **+40.0** | 54.9 → **94.9** | `PF` weights it **90**, the highest measured factor in the corpus. `CM` §3.4 shows the baseline funds ≈9 meaningful driver hours. Highest-return hour available |
| **Prototyping / fabrication iteration** | **+30.0** | 129.8 → **159.8** | ≈3 more full prototype–test–revise cycles at 8–12 h each **[S]**. Iteration count separates a mechanism that works from one that mostly works |
| **Integration + reliability hardening** | **+20.0** | 84.9 → **104.9** | `PF` weights reliability **88**. A robot that plays 12 clean matches out-ranks a faster robot that plays 9 |
| **Programming reserve (unallocated)** | **+10.0** | held in reserve | `CM` §3.3: the plan closes with **zero slack**. A reserve is what lets you absorb a week-5 mechanism change instead of shipping something broken |
| **Awards / business residual** | **+5.6** | 44.9 → **50.5** | Enough to actually rehearse the pit interview (row 55) |
| **Total** | **105.6** | | |

**At the 55 h planning midpoint**, the same priority order gives: drive practice **+21 h**,
prototyping **+16 h**, integration/reliability **+10 h**, programming reserve **+5 h**, awards
residual **+3 h**. §2.2's break-even is recomputed for this case immediately below.

### 2.2 The drive-practice argument, in points

Apply `CM` §3.4's own conversion to the new number:

| Step | Baseline | With +40 h |
|---|---:|---:|
| Drive-practice veq-h | 54.9 | **94.9** |
| ÷ 3.5 people a practice session occupies | 15.7 | 27.1 |
| × 0.6 (sessions after the robot is worth driving) | **≈9.4 h** | **≈16.3 h** |
| **Meaningful driver hours before event 1** | **≈9** | **≈16** |

That is **+7 hours of real driver seat time — a 73% increase** in the highest-weighted factor in the
corpus. `[AUDIT 2026-08-22]` **At the 55 h planning midpoint the +40 h becomes +21 h**, which is
54.9 → 75.9 veq-h → ≈13 meaningful driver hours, i.e. **+4 h and a 43% increase** rather than +7 h
and 73%. Both are large relative to a 9-hour baseline; plan the smaller one. Now price it, using our own model **[C, run 2026-08-22]**:

```
$ python tools/cycle-model.py --game rebuilt --cycle 8
  Going from 8.0s to 9.0s costs 9.7 points/match.
  Over a 12-match qualification schedule: 117 points.
```

**The break-even.** For the +40 h reallocation to be the best trade on the table, those 7 extra
driver hours need to buy **1.0 second** of cycle time — **0.14 s per additional driver hour**, early
on the learning curve where improvement is steepest. If they buy it you gain **≈9.7 points per match
and ≈117 points across 12 quals** — comparable to adding a whole scoring mechanism, at zero dollars
and zero mentor-supervision cost.

**Stated as a falsifiable claim so you can check it in March:** *seven additional pre-event driver
hours will move our average cycle time by at least one second.* **[S]** Measure it with a stopwatch
at your first practice and again at your last. If it does not, this section is wrong and the 40
hours belonged in prototyping.

The sweep shows the trade gets *better* the slower you currently are — which is exactly the
situation of a 15-student team in week 6 **[C, `--sweep`, 2026-08-22]**:

| Your cycle | Points/match, no endgame | Approx. value of the next second saved |
|---:|---:|---:|
| 15 s | 49.7 | ~+3.9 |
| 12 s | 61.3 | ~+6.7 |
| 10 s | 73.0 | ~+7.8 |
| **8 s** | **90.5** | **+9.7** |
| 6 s | 119.7 | ~+12.5 |

### 2.3 The prototyping argument

`CM` §5 caps you at **2 novel mechanisms** (`novel_mechanisms_max: 2`, recommended **1**). Given a
fixed mechanism count, the only remaining lever on mechanism *quality* is iteration count. Thirty
hours ≈ **3 additional prototype cycles [S]**. Against `ACHIEVABILITY-RUBRIC.md`, a mechanism that
has been through five iterations and one that has been through two are not the same mechanism, and
the difference shows up as reliability — `PF` weight **88**.

### 2.4 What these hours explicitly do **not** buy

**They do not buy a third mechanism.** `CM` §5.4 is explicit: +220 veq-h moves derivation route B but
routes A and C are unmoved, so `BINDING` stays at **2**. The binding constraint is **mentor unblock
attention at 3.4 h/wk** (`CM` §7.1, constraint #1), and *no amount of AI-returned student hours
relaxes it.* If you want a third workstream, recruit a second technical mentor between September and
November 2026 — cost **$0**, and it is the highest-leverage action available to this team. **AI is
the second-best thing you can do this fall, not the first.**

They also do not buy: more shop days (the calendar is fixed), a bigger budget (the $2,500
`robot_discretionary` line is untouched by everything in this file — which is the good news), or a
higher tooling level.

---

## §3. The five workflows that matter most

### 3.A — Kickoff manual analysis (Sat 2027-01-09 12:00 ET → Sun 18:00)

Runs alongside `KICKOFF_PLAYBOOK.md`; it does not replace it. Target: **≈2.5 h of what a 6 h manual
read traditionally costs**, with better coverage. Owner: strategy lead + mentor.

| Step | When | Command / action | Output | Gate |
|---|---|---|---|---|
| 1 | T+0:00 | `bash tools/probe-2027-manual.sh`, then `bash tools/ingest-manual.sh <pdf>` | Plain text + section index | Did the text extract cleanly? If not, stop and fix — a bad extract poisons every downstream pass |
| 2 | T+0:20 | `python tools/rule-inventory.py` | Deterministic rule inventory | Row count vs. the PDF table of contents |
| 3 | T+0:30 | **Pass 1 — scoring only.** *"From this text only, list every scoring action, its point value, and the manual section. If a value is not stated in the text, write UNKNOWN. Do not infer."* | Scoring table | **Every point value checked against the PDF by a second student.** Non-negotiable |
| 4 | T+1:00 | **Pass 2 — constraints.** Robot size, weight, motor limits, extension rules, protected zones | Constraint list | Mentor opens each cited rule |
| 5 | T+1:30 | **Pass 3 — ambiguity.** *"What in this text is ambiguous enough that a reasonable team could read it two ways?"* | Seeds `QA-AMBIGUITY-HOTSPOTS.md` | These become your Q&A questions when Q&A opens |
| 6 | T+2:00 | AI drafts `mygame.json` from the pass-1 table; **a human corrects every number**; then `python tools/cycle-model.py --game mygame.json --sweep` | Points-per-strategy by cycle time | Does the sweep shape make physical sense? |
| 7 | T+2:30 | `python tools/scouting-plan.py`; AI proposes scouting fields | Draft schema | **Cut to what 3–5 scouts can actually record** (`CM` §4.4) |
| 8 | T+3:00 | `python tools/score-strategy.py` on 3–5 archetypes from `03_ARCHETYPE_CORPUS.md` | Ranked archetypes | Mentor sanity-checks against `ACHIEVABILITY-RUBRIC.md` and `novel_mechanisms_max: 2` |
| 9 | **Sat PM – Sun** | **The strategy meeting. No laptops with chatbots open.** (row 8) | The decision | Humans only. AI output is *input to* this meeting, never a substitute for it |
| 10 | Sun 18:00 | AI drafts DDR #1 from the meeting notes | `docs/ddr/001-*.md` | Decision and Evidence lines are human-written |

**Failure mode to watch:** the team treats the pass-1 scoring table as authoritative *because it is
tidy*. It is the least trustworthy artifact of the weekend. Two students, independently, against the
PDF, before anyone designs anything.

### 3.B — Subsystem: written spec → tested in simulation

Owner: programmer #2, reviewed by lead + mentor. Target ≈40–60% of the unassisted time (rows 30–31).

1. **A human writes the spec first.** One page: what it does, ranges of motion, sensors, units,
   failure behaviour, and **the acceptance numbers**. If the student cannot write this, they do not
   understand the mechanism, and no amount of generation fixes that.
2. **The human writes the assertion values** into an empty test file — from the spec, before any
   generation. (`01` §3.1: this is the guard against tautological tests.)
3. **AI generates the IO interface + `*IOSim`** using `templates/programming-prompts.md`. Supply the
   real gearing, moment of inertia and motor type yourself — the `02` §3 calculators produce them.
4. **AI generates the subsystem + commands** against the spec.
5. `./gradlew test` — **the tests you wrote the assertions for must pass, and you must be able to say
   why each one passes.**
6. **The five-gate PR check** (`01` §5). G1 is comprehension: *the student explains every line to a
   reviewer.* A PR that fails G1 is closed, not patched.
7. Simulation run: full range of motion, both limits, and one deliberately bad input.
8. **Only now** does it touch hardware — reduced output, mentor present, a hand on the disable.

**Never skip step 1 to "save time".** Every hour claimed in row 30 assumes the spec exists. Without
it the generation is a guess dressed as code, and reviewing it takes longer than writing it would
have.

### 3.C — Post-match log review (5 minutes, in the pit, every match)

Owner: pit programmer. `01` §7. The highest-frequency AI workflow of the season.

| Step | Action | Time |
|---|---|---|
| 1 | Pull the WPILOG off the robot as soon as it is back on the cart | 1 min |
| 2 | `python tools/log-report.py <logfile>` — deterministic signal summary: currents, temperatures, brownouts, loop overruns, cycle times | 1 min |
| 3 | Paste **the summary, not the raw log**, into the assistant with match context: what the drivers reported, what you saw | 1 min |
| 4 | Ask for **ranked hypotheses, each with the signal that would confirm it** — never "what's wrong?" | 1 min |
| 5 | **Test the top hypothesis before changing anything.** Cross-check one number in AdvantageScope by hand | 1 min |
| 6 | Log the outcome in `ops/ai-hours.tsv` with `accepted=y/n` | 15 s |

**Hard rule: no code change between matches on an AI hypothesis alone.** The failure mode is a
confident, plausible, wrong diagnosis that costs you the next two matches instead of one.
**Caveat [C]:** `tools/log-report.py` round-trips a synthetic log but is **untested against a real
WPILOG** (`01` §7.2). Test it in October, not in the pit.

### 3.D — Scouting data → pick list

Owner: scouting lead + strategy lead + mentor. `03` §7 and `SCOUTING-PLAN.md`.

1. **Friday night:** export the day's scouting data; run `tools/tba_*.py` for official results;
   Statbotics for EPA-class metrics. All free, all keyed to your own account.
2. **Reconcile:** AI cross-checks scouted numbers against official scores and **flags disagreements**
   — the genuinely good use, because it finds *your* data-entry errors, not theirs.
3. **`python tools/match-sim.py`** for alliance-combination outcomes (`03` §6).
4. **AI drafts a ranked list with an explicit reason per robot**, in a fixed format. Each reason must
   cite a number from your data, not a vibe.
5. **Humans watch every robot in the top 24.** Non-negotiable. Data ranks; eyes decide. A robot that
   scores well and breaks every third match looks identical to a good robot in a spreadsheet.
6. **Mentor and strategy lead build the final list on paper**, with tiers and a "do not pick" line,
   and they can defend every position out loud.
7. On the field, **a student makes the pick.** `03` §7 draws this line and it stays drawn.

### 3.E — Build thread / documentation from meeting notes

Owner: media lead, rotating. `04` §2.1–2.2 and §6. The highest-ROI documentation workflow on the
team.

1. **During the meeting**, one student keeps a scratch file: what we tried, what happened, what we
   decided, what is still open. Bullet fragments. Five minutes total.
2. **Photos** — three per meeting, named `YYYY-MM-DD-what.jpg`. AI cannot invent an image of your
   robot, and a build thread without photos is not a build thread.
3. **AI expands** the fragments into a build-thread post plus a KB entry in the house format. It must
   add no fact that is not in the notes — say so in the prompt, explicitly, every time.
4. **The student who was in the room reads it** and deletes anything that did not happen. This step
   catches the real failure mode: models smooth over gaps with plausible engineering narrative.
5. **Attribution line** on anything public (`00_FIRST_AI_POLICY_VERIFIED.md`).
6. If the meeting produced a decision, it also produces a **DDR** (`04` §2.2). DDRs are the single
   most reusable artifact you will make — they feed award essays, the Impact submission, judge
   conversations, and next year's team.

---

## §4. Anti-patterns — how teams lose with AI

Unsparing, because the user makes budget decisions from this file.

### 4.1 Using it for the tasks it is worst at, because those are the annoying ones

The instinct is to hand over whatever is most tedious. But tedium correlates with *physical* work —
wiring, machining, driving — which is exactly the untouched portion of the table (rows 8, 12, 20, 26,
38, 41, 45, 55, 64 save **zero** by design). Teams that try anyway produce a wiring diagram that does
not match the robot and a build plan nobody follows. **If your task is not in §1, the default answer
is "do it by hand."**

### 4.2 Generating the code your students were supposed to learn from

Row 64 exists for this. Generating the base subsystem library in December means that in February,
when something breaks at 11 p.m. before an event, nobody on the team knows how it works. FIRST's own
policy is careful here: permission to use a tool is not a reason to skip the thinking
(`00_FIRST_AI_POLICY_VERIFIED.md`). **Symptom:** five-gate G1 (comprehension) starts failing.
**Response:** stop solo AI work entirely until `05` §7 Session 2 is re-run.

### 4.3 Trusting anything FRC-specific the model states from memory

`04` §8.1 documents this as the highest-frequency, highest-damage failure: **rule numbers, award
names, deadlines, part numbers, prices, vendor URLs, team numbers, KoP contents.** Models produce all
of these fluently and wrongly. 2027 makes it worse — the training data is saturated with roboRIO, and
2027 is Systemcore. **Every FRC-specific fact gets opened in its source before it is acted on.**
Assume anything Systemcore-specific stated from memory is wrong.

### 4.4 Building the tool instead of using the tool

Two named traps, both of which have eaten real seasons:

- **Writing your own scouting app.** `03` §9 is blunt: it draws on `programming` (134.8 h, the
  tightest line in 2027). Six free open-source apps already exist. **Use one.**
- **Building an automated match-video analysis pipeline.** `03` §4: not realistic in 2026. Negative
  expected value against a Systemcore-constrained programming budget.

The generalisation: AI makes building things *feel* cheap, which makes tool-building look attractive
at the exact moment your programming line is 118% subscribed.

### 4.5 Letting AI write award essays

`04` §3 draws the line at editor-and-coach. Judges interview students. An essay whose claims a student
cannot expand on in person is worse than a plainer essay they wrote themselves. A fabricated statistic
— outreach numbers are the classic — is an integrity finding, not a typo. FIRST explicitly warns that
**AI-detection tools are inaccurate and should not be used** (`00_FIRST_AI_POLICY_VERIFIED.md`), so
the risk is not detection: it is a student who cannot answer a follow-up question.

### 4.6 Picking alliance partners from a spreadsheet

Row 48 and §3.D step 5. Reliability, driver skill and defence-resistance decide elimination matches
and are the qualities *least* visible in scouting data. A team that picks purely on ranked numbers
picks the robot with the best average and the worst variance.

### 4.7 Not measuring, and finding out in April

`05` §8: if you cannot answer "did this return hours?" in April, you spent the money on a feeling.
The specific failure is skipping the **two-week un-assisted baseline in September** — without it the
April number is unfalsifiable. **A rejection rate under 10% does not mean the AI is good; it means
nobody is checking.**

### 4.8 Spending the hours you saved on more desk work

The most common quiet failure. Hours returned from documentation flow into more documentation; hours
returned from strategy flow into longer strategy meetings. **The entire thesis of §2 is that the
hours go to the practice field, the prototype bench, and the saw.** If drive practice comes in under
the 54.9 h baseline in April, the investment failed on its own terms *even if the ledger looks
great* (`05` §8.3, kill criterion 4).

### 4.9 Pasting the whole manual, log, or dataset into the chat

Cost scales with passes, and long contexts degrade recall on exactly the details you need. Use the
deterministic tools to *reduce* first (`log-report.py`, `rule-inventory.py`, `teamupdate-diff.py`),
then hand the model the summary. This is a quality argument first and a cost argument second.

### 4.10 Letting one student become "the AI person"

Then the team has a single point of failure with a laptop, the other fourteen learn nothing, and the
capacity model's assumption of parallel workstreams quietly breaks. `05` §7's curriculum is for
everybody. **Rotate the ledger-keeping role weekly.**

### 4.11 Using AI to shorten the strategy meeting

Row 8 saves zero hours on purpose. The kickoff strategy decision is where a small team's season is
won or lost, and it is made of argument, physical intuition, and knowing your own shop. A summary
document is an input to that argument. It is not a shortcut through it.

### 4.12 Believing this document's own hours estimates

Every figure in §1 is **[S]**. The nominal 236 h is not a number to quote — it double-counts
overlapping work, assumes review is free, and assumes every workflow works the first time. **106 h
returned** is the defensible planning figure and it is still a hypothesis. §5 is how you find out.

---

## §5. The student-hours ledger

One tab-separated file, appended by hand, ~15 seconds an entry. Deliberately compatible with `05` §8
so there is one ledger on this team, not two.

### 5.1 The file — `ops/ai-hours.tsv`

```
date	who	area	row	task	est_solo_min	actual_min	review_min	verified_by	accepted	notes
2026-09-08	AH	baseline	--	write flywheel sim by hand	90	95	0	self	y	BASELINE WEEK - no AI
2026-10-14	AH	programming	31	generate FlywheelIO + sim	90	25	10	mentor	y	tests passed, student explained
2026-10-16	RS	awards_business	54	cut exec summary to char limit	45	20	5	mentor	y
2026-10-21	JT	programming	35	tune shooter kV from SysId	60	55	20	mentor	n	fabricated kV, redone properly
2027-01-09	MK	strategy_rules	1	kickoff manual pass 1	360	150	45	2 students	y	3 point values were wrong
```

**The rules that make the ledger honest:**

1. `est_solo_min` is written **before starting**, by the student doing the work. It is a guess. Over
   40 entries the error averages out; the discipline is the point.
2. `review_min` counts **as cost**, not as free. Net saved = `est_solo_min − actual_min −
   review_min`. Most published AI-savings figures omit review. Ours does not.
3. `area` is one of the eight `CM` lines; `row` is the §1 row number. This is what makes the ledger
   reconcile to the capacity model instead of floating free.
4. **`accepted = n` rows are the most valuable rows in the file.** Never delete one.
5. Two weeks of `baseline` rows in **September**, before AI is switched on.

### 5.2 The weekly five-minute review (mentor, Sunday)

| Check | How | Healthy | Action if not |
|---|---|---|---|
| Entries logged | `wc -l ops/ai-hours.tsv` | ≥5/week in-season | The ledger is dying. Assign a rotating keeper |
| Net hours returned | Σ(`est_solo_min`−`actual_min`−`review_min`)÷60 | tracking toward **40–70 h** by April (§1.11a); ≈106 h is the ceiling, not the target | Re-read §1 — which rows are not delivering? |
| Rejection rate | `accepted=n` ÷ total | **15–30%** | **<10%: nobody is checking.** >50%: wrong tasks |
| Source of savings | group by `area` | Concentrated in `programming`, `strategy_rules`, `awards_business` | Savings appearing in `fabrication_assembly` means something is mislabelled — AI does not turn wrenches |
| **Drive-practice hours logged** | separate tally vs. 54.9 baseline / 94.9 target | **on track for 94.9** | **This is the one that matters.** See §4.8 |
| Mentor unblock load | count of "mentor was the blocker" events | ↓ vs. September | The scarcest resource on the team is 3.4 h/wk (`CM` §7.1) |
| Comprehension | one spot-check at a PR review | **100%** | Stop solo AI work; re-run `05` §7 Session 2 |

### 5.3 The scoreboard — fill this in; it is the deliverable of the whole AI programme

| Metric | Target **[S]** | Sept baseline | Dec 15 | End of build | Post-event 1 | April |
|---|---|---|---|---|---|---|
| Net hours returned | **40–70** (ceiling ≈106) | 0 | ≥15 | | | |
| Rejection rate | 15–30% | — | | | | |
| Drive-practice hours logged | ≥94.9 | — | | | | |
| Prototype iterations completed | ≥3 above baseline | — | | | | |
| Avg. cycle time, stopwatch (s) | −1.0 s vs. first practice | — | | | | |
| Students who can explain merged code | **100%** | — | | | | |
| Total AI spend ($) | ≤ $700 (`05` §1) | | | | | |
| **Cost per net hour returned** | **< $20/h** | | | | | |

### 5.4 Kill criteria — decide these in September, before you are invested

Restated from `05` §8.3 so they live next to the ledger:

- **Rejection rate > 50% for three consecutive weeks** → cut back to boilerplate and documentation
  only.
- **Any student cannot explain merged code at a PR review** → stop solo AI work entirely until
  `05` §7 Session 2 is re-run.
- **Fewer than 15 net hours returned by 2026-12-15** → cancel the January tier upgrade. The evidence
  is not there.
- **Drive practice below 54.9 h in April** → the hours went somewhere other than the field. The
  programme failed on its own terms regardless of what the ledger says.

---

## §6. Validation / dry run

**What was actually executed on 2026-08-22:**

```bash
python tools/cycle-model.py --game rebuilt --sweep      # -> the sweep table reproduced in 2.2   [C]
python tools/cycle-model.py --game rebuilt --cycle 8    # -> "8.0s to 9.0s costs 9.7 pts/match"  [C]
python tools/cycle-model.py --game rebuilt --cycle 9    # -> "9.0s to 10.0s costs 7.8 pts/match" [C]
ls reference/ai-integration/calculators/                # -> cg_tip, drivetrain, elevator_arm,
                                                        #    fourbar, motors                     [C]
ls reference/ai-integration/templates/                  # -> 6 prompt/policy templates            [C]
cat reference/team_capacity.yaml                        # -> every budget figure used in 1.9      [C]
```

**Internal consistency checks this file passes:**

| Check | Result |
|---|---|
| Every §1 subtotal's *assisted* hours ≤ its `CM` line budget | **Pass**, all eight lines |
| Σ returned (105.6) ≤ Σ(budget − assisted) | **Pass** — 105.6 vs. 126.3 aggregate headroom; capped per line, not in aggregate |
| Programming nominal saving (65.5 h) inside `01` §3's defensible band (53–90 h) | **Pass** |
| `awards_business` unassisted demand far exceeds the funded line | **Pass** — 237% here on a narrower scope than `04` §7, consistent in direction and cause |
| No claim that saved hours raise `novel_mechanisms_max` | **Pass** — §2.4 says the opposite, per `CM` §5.4 |
| No claim against the $2,500 `robot_discretionary` line | **Pass** — nothing in this file spends the BOM |
| Attribution obligation stated, not re-litigated | **Pass** — §0 step 5, sourced to the policy file |

**Falsifiers — what would prove sections of this document wrong:**

| Claim | Falsified if |
|---|---|
| §1.11: ≈106 h returned | The April ledger shows <40 net hours with the ledger honestly kept |
| §2.2: drive practice is the right destination | +7 driver hours move average cycle time by <0.3 s |
| §1.5: programming is where AI pays most | Savings concentrate in `awards_business` *and* programming still overruns 134.8 h |
| §1.2 row 12: text-to-CAD is unusable | A student produces competition-ready geometry from a text prompt and the part survives an event |
| §4.4: do not build a scouting app | No off-the-shelf app can record your 2027 schema *and* a custom one takes <10 h |
| §2.4: hours do not buy a third mechanism | You successfully field three novel mechanisms with one technical mentor |
| §4.3: FRC-specific recall is unreliable | A season of G-gate logs shows zero fabricated rules, prices, or APIs |

---

## Files written by this pass

| Path | What it is |
|---|---|
| [`reference/ai-integration/00_WORKFLOW_MAP.md`](00_WORKFLOW_MAP.md) | This file. The 66-row master table, the hours reconciliation, five runbooks, twelve anti-patterns, the ledger template |

No other files were created or modified. Every tool, calculator and template cited above already
existed; this pass ran them and cited their real paths.

---

## Known limitations

1. **Every hours figure is [S].** Not one has been measured. The whole of §1 is a planning
   hypothesis. §5 exists because of this, and §5 is the most important section for the mentor.
2. **The `min(saved, budget − assisted)` capping rule in §1.9 is a modelling convention invented for
   this file.** It is conservative and checkable, but it is not derived from `CM`. A reasonable
   person could argue for counting the full 205.7 h; this file does not, because those hours were
   never funded.
3. **The task list is not exhaustive.** Real seasons contain rework, waiting for parts, illness, snow
   days, and meetings about meetings. Enumerated traditional demand (678.5 h) both overshoots the
   599 h budget — it is task demand, not effective veq-h — and undershoots reality, because overhead
   is unenumerated. **Do not read 678.5 − 472.8 as free capacity.** Read only the §1.9 *Returned*
   column.
4. **The cycle-model figures come from the 2026 REBUILT worked example**, not BIOCORE. The exchange
   rate (≈9.7 pts/s at an 8 s cycle) illustrates *shape*, not a BIOCORE prediction. Re-run §3.A step
   6 on the real game file on kickoff day and re-derive §2.2 from it.
5. **0.14 s of cycle time per additional driver hour is an assumption**, deliberately stated as a
   break-even rather than asserted as a rate, because nobody has measured it.
6. **The Systemcore rows (24, 29) are the least reliable in the table.** The platform is not present
   in any model's training data in mature form; 2027 pinouts and APIs are **UNVERIFIED** until the
   2026-11-12 Kit Release and the 2027 documentation. Row 29's 18 h saving is simultaneously the
   largest single line item in the table and the one built on the least evidence.
7. **`tools/log-report.py` is untested against a real WPILOG** (`01` §7.2). Workflow §3.C depends on
   it. Test it in October.
8. **Owner labels are functional roles**, mapped to `CM` §4.1–4.2's fourteen functions, not to named
   students. On a 15-person team most people hold two roles; the table does not model that, and it
   does not model the event-day body count in `CM` §4.4.
9. **No 2027 rule, deadline, award name, or character limit in this file is confirmed for 2027.** The
   2026 figures are labelled where used. Re-verify at the 2026-11-12 Kit Release and again at
   kickoff.
10. **This file assumes the FIRST AI policy holds for 2027.** It is [C] as of 2026-08-21 from the 2026
    materials (`00_FIRST_AI_POLICY_VERIFIED.md`). Re-check when the 2027 award resources publish.
11. **Nothing here addresses minors' data or vendor account terms**, which
    `00_FIRST_AI_POLICY_VERIFIED.md` flags as an open item. Check each vendor's terms and your
    district's policy directly before creating student accounts.
