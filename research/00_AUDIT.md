# 00 — Adversarial Completeness & Accuracy Audit

**Run 2026-08-22.** Scope: every file under `research/`, `reference/`, `tools/`, plus `KICKOFF_PLAYBOOK.md`, the (previously absent) `README.md`, and the manual archive.

**Method.** Every internal file reference resolved against the filesystem. Every external URL probed (385 unique). Every cited rule ID cross-checked against the 2016–2026 rule inventories. Every computed number re-derived from its source data. Fifteen-plus factual claims re-verified against primary sources — FIRST webpages, the FIRST calendar, AndyMark product JSON, the Limelight Systemcore spec PDF, WPILib docs, and page-level text extraction from the local 2026 REBUILT manual PDF. The kickoff-day ingest pipeline was executed end to end.

**Headline:** the analytical content is unusually sound — **every computed number in the project reproduced exactly** — but the *operational* layer had a defect that would have cost 15–30 minutes at kickoff, and the project had **no README and no coverage of the FRC-only structures** (district points, double elimination, no bag day) that a mentor arriving from FTC most needs.

---

## 1. What was verified and held up

### 1.1 Computed assets — reproduced exactly, zero drift

| Asset | Check | Result |
|---|---|---|
| `reference/QA-AMBIGUITY-HOTSPOTS.md` | All 22 rules × 3 seasons of Q&A counts re-derived from `research/rule_inventories/qa_heat_20{24,25,26}.tsv` | **22/22 exact.** R402 3→9→16=28, G211 5→9→12=26, G416 4→1→18=23, R106 0→0→12=12. Every subtotal (bumpers 116, contact 75, extension 49) re-added correctly. |
| `reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md` | All counts re-derived from `research/awards_tba/tba_awards_2026.csv` (4,993 rows, 65 distinct awards) | **Exact.** FIRST Leadership Award 10 / Finalist 172 / DCMP Semi-Finalist 218; Gracious Professionalism 211; Industrial Design 210; Autonomous/Creativity/Excellence/Imagery/Innovation/Sustainability all 208. **"Dean's List" appears zero times in 2026** — the rename claim is correct. |
| 2026 Q&A structured export | Re-counted both pulls | **221 Q&As / 211 rules / 86 sections / 101 tags**, and the independent re-pull in `2026_QA_live_recheck/` matches at 221. Claim of a frozen, reproducible dataset confirmed. |
| Rule citations across all docs | Every `[GRHSCIET]\d{3}` ID extracted and checked against the season it is attributed to | **58/58 valid.** Only `G433` is absent from 2026 — correctly, because it is cited as a *2025* rule in a 2025→2026 churn statement. Every headline quoted matches the inventory. |
| External links | All 385 unique URLs probed | **377 live.** The 8 non-200s are all template placeholders (`frc<YEAR>`, `TE-26NNN`, `<YEAR>`), the deliberately-documented `frc2027` 404, or artifacts of my own regex truncating a closing paren. **No genuine dead link found.** |

### 1.2 Primary-source spot checks (18 claims)

| # | Claim | Verdict |
|---|---|---|
| 1 | Kickoff Sat Jan 9, 2027, 12:00 p.m. ET | ✅ [FRC Game & Season](https://www.firstinspires.org/programs/frc/game-and-season) |
| 2 | Q&A opens Jan 13, 2027; closes Apr 21, 2027 | ✅ [FIRST Calendar](https://www.firstinspires.org/programs/calendar) |
| 3 | Week 0 Feb 20; Weeks 1–7 Mar 3 → Apr 18, 2027 (**7-week season**) | ✅ Calendar; corroborated by FIRST Chesapeake publishing Week 5 as Apr 2–4 |
| 4 | Championship Apr 28 – May 1, 2027, George R. Brown, Houston | ✅ Calendar |
| 5 | GRB committed **through 2034** | ✅ [Update: Future of FIRST Championship](https://community.firstinspires.org/update-future-of-first-championship), Jan 22, 2026 |
| 6 | Fees $6,500 / $3,200 / $4,000 / $6,000 | ✅ [Cost & Registration](https://www.firstinspires.org/robotics/frc/cost-and-registration) — but see Fix 4 |
| 7 | AndyMark BIOCORE `am-5901_kop` $70.00, `am-5901_partial` $169.00; created 2026-06-03, published 2026-06-08 12:00:14 ET | ✅ product JSON pulled live |
| 8 | Scoring-element blog verbatim quotes (one type; holding limit > 1; KoP qty > holding limit; no FIRST Choice; quantities intentionally unspecified; ships Jan 11) | ✅ all six verbatim |
| 9 | Logo palette `#5FB1D6` 15.96%, `#EDD9B4` 8.05%, `#0F1821` 5.27%, plus `#BEDAE8`, `#0081BA`, `#F7E100` | ✅ **re-sampled the 2000×2000 asset pixel-by-pixel; every hex and every percentage exact.** `#F7E100` confirmed as the dominant yellow at 0.039% |
| 10 | Systemcore 215 g / 0.475 lb; CM5 quad Cortex-A76; 4 GB | ✅ [spec PDF](https://downloads.limelightvision.io/documents/systemcore_specifications_june15_2025_alpha.pdf) — but see Fix 2 |
| 11 | WPILib 2027: Java 25 / C++ 23, `edu.wpi.first`→`org.wpilib`, `frc::`→`wpi::`, NT v3 removed, Shuffleboard/SmartDashboard/PathWeaver/RobotBuilder removed, Commands v3, OpMode, new Driver Station, full removed-hardware list | ✅ every item, [New for 2027](https://docs.wpilib.org/en/latest/docs/yearly-overview/yearly-changelog.html) |
| 12 | Global Head Referees Browne + Corrington (replacing Zawislak); Senior HRs Burch, Verbrugge, + Douglas, Hollowell; Aug 6, 2026 | ✅ verbatim |
| 13 | REBUILT FUEL 5.91 in, 0.448–0.5 lb, High Density Polyurethane Foam; `am-5801` $2.00, kop = 10, `am-5801_42` = 42 = 1/12 field → **504** per field | ✅ AndyMark JSON + manual |
| 14 | REBUILT holding limit 8 | ✅ manual: *"it fully and solely supports not more than 8 FUEL"* |
| 15 | 2026 manual = **166 pp.**, Version TU22 | ✅ pymupdf page count |
| 16 | Precedence-chain quotes at pp. 9, 10, 11, 17, 36, 52, 115 | ✅ **9 of 10 exact**, footer-confirmed — see Fix 6 |
| 17 | `firstfrc.blob.core.windows.net/frc2027` → 404 | ✅ re-probed 2026-08-22; still 404. `frc2026/Manual/2026GameManual.pdf` → 200, confirming the URL shape to try first |
| 18 | R103 = 115.0 lb bare; R408 = 135.0 lb with bumpers | ✅ manual — but see Fix 5 |

### 1.3 The kickoff pipeline actually works

`tools/ingest-manual.sh` was **executed end to end** against `2025_REEFSCAPE_GameManual.pdf` with the 2026 REBUILT baseline. It completed cleanly (exit 0) and produced every artifact it advertises: 164 pp., 229 rules, 9 added / 7 removed / 153 changed, 19 game-specific vs. 210 evergreen, 88 glossary terms, 49 undefined ALL-CAPS tokens, 87 violation clauses, 446 tripwire hits, and a 137-entry section map. `frc_spans.py`'s colour-based evergreen/game-specific detection works. **Test artifacts were deleted after the run.** This is the most important positive finding in the audit: the tooling is real and it runs.

---

## 2. What was wrong, and what I changed

### Fix 1 — CRITICAL: the first command of kickoff day did not work
**File:** `KICKOFF_PLAYBOOK.md` §Step 1

**Before:** documented `bash tools/ingest-manual.sh` with no arguments, plus `--url` and `--file` flags, and stated *"The script probes the `frc2027` CDN container, downloads the manual plus every supplemental it can find."*

**Reality:** the script contains **zero network code** — no `curl`, no `wget`, no URL of any kind. It takes a **local PDF path** as `$1`. Executed live:
- no args → `line 39: 1: usage: ingest-manual.sh <manual.pdf> [label]`
- `--url …` → `!! no such file: --url`

**After:** Step 1 split into **1a Fetch and freeze** (a working `curl` block, with the verified `frc2026/Manual/2026GameManual.pdf` URL shape tried first and a third candidate name added) and **1b Ingest** (correct positional syntax, plus the `BASELINE=` env-var form for diffing BIOCORE against itself after each republish). The false CDN-probing claim is removed and replaced with an explicit warning. Also fixed: the old fallback block `cp`'d the manual unconditionally even when the download loop failed, and wrote to `/tmp` — now uses `mktemp -d` and guards on success.

**Impact if unfixed:** three failed commands and a confidence hit during the highest-value 15 minutes of the season.

---

### Fix 2 — Systemcore dimension wrong
**File:** `research/03_biocore_official_intel.md` §4

**Before:** `135.3 × 71.5 × 28.13 mm`
**After:** `135.5 × 71.5 × 28.13 mm` — the [spec PDF](https://downloads.limelightvision.io/documents/systemcore_specifications_june15_2025_alpha.pdf) reads `135.5mm x 71.5mm x 28.13mm (5.3" x 2.8" x 1.1")`.

Also **added** specs the doc had not captured: BCM2712 quad Cortex-A76 @ 2.4 GHz, 4 GB LPDDR4X-4267, **16 GB eMMC**, RP2350 dual Cortex-M33 @ 150 MHz / 520 KB SRAM, USB 3.0 5 Gbps shared, 1 Gbps Ethernet, USB-C LINK is USB 2.0, BRIDGE port Molex Micro-Fit+ 206832-0401.

---

### Fix 3 — Field dimensions materially wrong
**File:** `research/03_biocore_official_intel.md` §5

**Before:** *"Full field = 2 rolls of 15 ft × 74 ft covering 30 ft × 74 ft … `[INFERENCE]` Field footprint stays **30 ft × 74 ft** — a same-size field is effectively confirmed."*

**Reality:** 30 × 74 ft is the **carpet purchase footprint**, which covers the field *plus* driver stations and margin. 2026 manual §5.2 (p. 18): *"Each FIELD for REBUILT is an approximately **317.7in** (~8.07m) by **651.2in** (~16.54m) carpeted area bounded by inward facing surfaces of the ALLIANCE WALLS, OUTPOSTS, TOWER WALLS, and guardrails."* That is **26.5 ft × 54.3 ft** — the stated figure was over-long by ~20 ft and over-wide by ~3.5 ft.

**After:** correction block added distinguishing carpet order from FIELD, with the verbatim §5.2 quote. The *inference* (unchanged carpet order ⇒ unchanged footprint) is preserved and is arguably strengthened; only the number is corrected, with an explicit "do not write 30 × 74 on any drawing." Also added the real 2026 carpet spec (Shaw Neyland II 20 "66561 Medallion", **not purchasable**; equivalent Shaw Profusion 20 Style 54933).

**Impact if unfixed:** a practice-field build or any spatial reasoning anchored to a field 36% longer than reality.

---

### Fix 4 — Registration fee omitted the district branch
**File:** `research/03_biocore_official_intel.md` §6

**Before:** `$6,500 season registration (includes 1 Regional event)`
**After:** includes **one Regional event *or* two District events** — the branch that applies to most district teams, and load-bearing for the district-points analysis now in the new orientation file.

---

### Fix 5 — Wrong robot weight in the AI policy doc
**File:** `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`

**Before:** *"unverified generated code safe on a **125 lb** robot"* — matches neither FRC limit.
**After:** **115.0 lb** bare (2026 R103, excluding BUMPERS, battery + its Anderson half, and event location tags) and **135.0 lb** with BUMPERS (2026 R408).

Also filled the blank R408 cell in the `KICKOFF_PLAYBOOK.md` §3.2 constraint table with the 135 lb prior and the R103 exclusion list.

---

### Fix 6 — A prior correction log corrected in the wrong direction
**File:** `research/02_supplemental_docs_index.md` §1.2

The existing correction log claimed the *"English pdf … is the commanding version"* quote moved **p. 10 → p. 11**. It is on **p. 10**; the "correction" introduced the error. Verified by matching each quoted string to its PDF page index and cross-checking the page's own `N of 166` footer.

**After:** citation fixed to p. 10, and a full 10-row verification table added showing every precedence quote with its footer-confirmed page. The other nine were correct as cited. Root cause noted: §1.6/§1.7 straddle the p. 10/11 break — §1.7's *heading* is near the break, its *text* is on p. 10.

---

### Fix 7 — Three dangling file references (fabricated "this file exists" claims)

| Claimed | Claimed in | Reality |
|---|---|---|
| `../SMALL_TEAM_PLAYBOOK.md` | `research/00_PREMISE_CORRECTION.md` | **Does not exist anywhere** |
| `reference/robot_construction_rules.md` | `KICKOFF_PLAYBOOK.md` doc map ×3 | **Does not exist anywhere** |
| `reference/loopholes_and_exploits.md` | `KICKOFF_PLAYBOOK.md` doc map ×3 | **Does not exist anywhere** |
| `05_ai_infrastructure_and_policy.md` | `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` | **Does not exist anywhere** |

Worse, the playbook contained a note saying the two `reference/` files *"are produced by parallel passes and may land in `reference/` or `research/`. If a link is dead, Glob before assuming it does not exist."* That instruction would have burned kickoff-day minutes hunting for files that were never written.

**After:** all four references replaced with explicit **DOES NOT EXIST** markers naming a concrete substitute — `research/rule_inventories/2026_rules.tsv` (R-prefix rows carry headline + page) for the R-rule source, and `QA-AMBIGUITY-HOTSPOTS.md` + `churn_semantic.tsv` for the loophole case book. The misleading "Glob before assuming" note is replaced with the audit result.

---

### Fix 8 — REBUILT calibration numbers were the Regional-tier slice only
**File:** `research/04_biocore_community_intel.md` §1

**Before:** *"three-rung Tower climb (10/20/30); RPs: Energized (≥100), Supercharged (≥360), Traversal (≥50)"*

**Reality**, from the local manual (Tables 6-4 / 6-5):
- TOWER points are **period-dependent**: LEVEL 1 = **15 in AUTO, 10 in TELEOP**; L2 = 20; L3 = 30. The flat "10/20/30" hid the AUTO premium.
- BONUS RP thresholds **escalate by event tier**:

  | BONUS RP | Regional / District | District Championship | *FIRST* Championship |
  |---|---|---|---|
  | ENERGIZED | 100 | 240 | **360** |
  | SUPERCHARGED | 360 | 360 | **500** |
  | TRAVERSAL | 50 | 50 | 50 |

**After:** both corrected, with the full table and an explicit carry-forward question for the BIOCORE review. This matters strategically: a **3.6× jump** in the ENERGIZED threshold between a Regional and Championship means a robot tuned to clear the Regional bar is not tuned to clear the Championship one. That is exactly the kind of structure the kickoff review must look for and would have missed.

---

### Fix 9 — File-count drift
**File:** `research/02_supplemental_docs_index.md`

`KOP/` 32 → **33**; `crossseason/` 18 → **19**; `FieldElements_LowCost/` 11 → **25**. Cosmetic, but the index's credibility rests on being literally checkable.

---

### Fix 10 — No README
The project root had **no `README.md`** — no entry point, no reading order, no statement of the tagging convention. **Created**, with the September-12 answer in the first screenful, the corrected two-command kickoff sequence, the real directory layout, and the tag legend.

---

## 3. What I added: the largest content gap

**New file: [`reference/FRC_VS_FTC_ORIENTATION.md`](../reference/FRC_VS_FTC_ORIENTATION.md)**

Coverage audit of the whole project before this pass:

| Concept | Mentions across all docs |
|---|---|
| district points | **0** |
| double elimination | **0** |
| backup robot | **0** |
| practice match | **0** |
| bag day / stop build | 1–2, buried inside one `[INFERENCE]` |

For a mentor whose recent frame is FTC, these are precisely the load-bearing differences. The new file covers, all cited to the 2026 manual with rule + page:

1. **There is no bag day and no stop-build day** — verified by zero-hit full-text search. Iteration between events is FRC's dominant strategy; your Week 1 robot is a prototype.
2. **District points** (§11.1, Table 11-1, p. 133) with the full table, including the **×3 District Championship multiplier**. The strategic consequence nobody had written down: **FIRST Impact is worth 10 points and draft acceptance at slot 5 is worth 12** — awards and being *pickable* score in the same currency as match performance. A review that optimizes only match points optimizes a fraction of the objective.
3. **Event weeks and score inflation**, Week 0, and the asymmetric Team Update cadence (Tue+Fri until Week 1, then Tuesdays only — the rules-volatility window closes as events start).
4. **8 alliances × 3 teams, double elimination**, declining teams ineligible as BACKUP, playoff DQ zeroes the alliance. Plus **Ranking Score is a mean, not a sum**.
5. **The I101–I107 inspection flow**, including the I103 weight trap (all mechanisms for all configurations weigh in together) and the point that **R-rules absent from the Inspection Checklist are effectively self-reported**.
6. **Q&A timing as a lever** — jurisdiction extends to the Awards and Event Experience webpages; Q&A can *cause* manual revisions via Team Updates, so week-1 questions are the cheap ones.
7. An FTC→FRC translation table and five open questions for the manual.

Wired into the `KICKOFF_PLAYBOOK.md` document map as read-first, and into `README.md`.

---

## 4. The September 12 question — answered, correctly, and now prominently

**Answer: there is no FRC event of any kind on September 12, 2026.** That is the **FTC BIOBUZZ** kickoff. FRC BIOCORE kickoff is **January 9, 2027, 12:00 p.m. ET**. The nearby FRC date is **September 24, 2026, 12:00 ET** — Kit & Kickoff Registration plus Event Registration Round 1 preferencing, a registration deadline with no game content.

**Status before this pass:** correct and well-sourced, but stated in `research/00_PREMISE_CORRECTION.md` and `research/03_biocore_official_intel.md` only — neither of which a user necessarily opens first, because there was no README pointing at them.

**Status now:** ✅ correct in all four files that mention it, and now **the first thing in `README.md`**, above the fold. `00_PREMISE_CORRECTION.md` gained a side-by-side date table (Sept 1 / Sept 12 / Sept 24 / Nov 12 / Jan 9) with a "does a game get revealed?" column, which is the form that actually prevents the confusion recurring.

**One live consequence:** Sept 24, 2026 is ~4 weeks away and is a real deadline. Missing Round 1 preferencing costs event choice.

---

## 5. Manual archive coverage

**35 consecutive FRC seasons on disk: 1992 → 2026. No season missing.** `[AUDIT 2026-09-04]` **316 PDFs** in `manuals/archive/frc/` (plus 16 quarantined in `_rejected_mislabeled/` and `_truncated_unrecoverable/`) plus **433 files** across 32 subdirectories of `manuals/archive/supplemental/` = **749 archived documents**. This file originally said 242 / 426 / 668; those were counted at 03:09 on 2026-08-22 and the gap-fill fetch landed at 11:01 the same morning, so the numbers were stale within eight hours and were then copied into `README.md` and `INDEX.md`. Recounted 2026-09-04; nothing in `manuals/` has been modified since 2026-08-22. The 35-season claim is unchanged and re-verified.

`[AUDIT 2026-09-12]` The archive is not in the public repository, because FIRST's documents are not redistributed; `bash tools/rebuild-corpus.sh --fetch` downloads the PDFs the text corpus is built from, then `bash tools/rebuild-corpus.sh` rebuilds the `_txt/` extractions locally.

| Era | Coverage |
|---|---|
| 1992–1995 | Competition manuals + update packets; plus a 1992–2012 all-seasons game summary |
| 1996–2007 | Chapter-split manuals (game / robot / arena / awards / admin / appendices), 7–20 PDFs per season |
| 2008–2015 | Consolidated Game Manuals + Team Updates + Q&A archives; Admin Manuals 2011–2016 |
| 2016–2026 | Game Manual + Q&A export + Team Updates for **every** season; 2021 additionally section-split ×12 |
| Text layer | `_txt/` full extractions for 2022–2026 (317–403 KB each) |
| Supplemental | Team Updates individually + combined 2012–2026 · Inspection Checklists 2013, 2015–2026 · Field Drawings 2018–2026 · Layout & Marking 2012–2025 · Field CAD/STEP 2023–2026 · low-cost team elements 2012–2026 · KoP checklists 2020–2026 · KitBot 2024–2026 · AprilTag guides 2024–2026 · Playoff Alliance Communication 2022–2025 · 19 cross-season docs (Bumper Guide, Pneumatics Manual, Safety, Judge Manual, Award Workbook, Effective Strategies, Scoring Analysis, Kickoff Game Breakdown Worksheet) · 31 blog snapshots · 8 webpage snapshots |

**Gap-fill attempted.** I probed the CDN for the four remaining holes — 2016 Q&A full archive, 2014 and 2017 Inspection Checklists, 2017/2019 evergreen field drawings — across every naming convention the fetch logs reveal FIRST has used (`frc2016manuals/GameManual/`, `frc<Y>/Manual/`, `frc<Y>/AuxDocx/`, `frc<Y>/PlayingField/`, kebab-case and CamelCase). **All 404.** The one candidate that returned 200 (`frc2021/PlayingField/2021FieldDrawings-Evergreen.pdf`) is already held locally. These files are not on the CDN under any guessable name; recovering them means Wayback spelunking for marginal value, since 2016 Q&A *heat* data is already derived and present in `research/rule_inventories/qa_heat_2016.tsv`.

**Conclusion: archive coverage is effectively complete and needs no further work before kickoff.**

---

## 6. What remains missing, and why

`[AUDIT 2026-09-04]` **Gaps 3, 4 and 5 are closed.** All three were closed later on 2026-08-22, hours
after this list was written at 03:09, and the list was never revised. The Status column below is the
2026-09-04 re-check; every tool named in it was executed in that pass. **Every gap that could be
closed before a BIOCORE manual exists is now closed.** What remains is blocked on FIRST publishing
something, and that is the honest state of this project.

| # | Gap | Status, 2026-09-04 | Why |
|---|---|---|---|
| 1 | **No BIOCORE game content exists** | **Still open, and uncloseable** | Genuinely unpublished. Both this project's probe and Trellis's independently written one report `frc2027` 404 across every known name shape as of 2026-09-04. Nothing can close this before 2027-01-09 |
| 2 | **`research/01_*` and `reference/team-ops/01/02/04_*` were never written** | **Still open, deliberately** | The numbering implies files that do not exist. Nothing references them and nothing is broken. Renumbering churns every cross-reference in the project to fix a cosmetic gap; it is not worth doing four months before kickoff. Recorded rather than done |
| 3 | ~~**No scouting-data schema**~~ | **CLOSED**: [`../tools/scouting-plan.py`](../tools/scouting-plan.py) + [`../reference/SCOUTING-PLAN.md`](../reference/SCOUTING-PLAN.md) | Three subcommands: `free` reports what FMS and TBA already publish, `schema` emits a 13-field match and 9-field pit schema covering **only** what FMS does not publish, `picklist` fuses the two. Ran clean 2026-09-04. It is game-agnostic, which is what made it worth building before kickoff |
| 4 | ~~**No strategy-simulation tooling**~~ | **CLOSED**: [`../tools/cycle-model.py`](../tools/cycle-model.py) and [`../tools/match-sim.py`](../tools/match-sim.py) | `cycle-model.py --game rebuilt` prints cycles, points and an explicit break-even table for each endgame choice; its arithmetic was independently recomputed in the system audit §2.3, four checks, all exact. Ran clean 2026-09-04 |
| 5 | ~~**Team Update diffing is manual**~~ | **CLOSED, with one honest qualification**: [`../tools/teamupdate-diff.py`](../tools/teamupdate-diff.py) | `season <year>` indexes every rule id and manual section each Team Update touched, in date order, with a churn ranking; `slots` does it across all seasons on disk and is predictive of where BIOCORE's amendments will land; `--watch` prints only what is new since the last run. **The qualification:** it does not parse the yellow-highlight and strikethrough convention this gap named. It works from rule ids and section references, which is what makes the 22-updates-a-season problem tractable, and the highlight parsing was not needed to close it. Ran clean 2026-09-04 |
| 6 | **No 2016 Q&A archive, 2014/2017 inspection checklists** | **Still open; correctly skipped** | Not on the CDN under any known name (§5). Low value |
| 7 | **Systemcore is untested by this team** | **Still open, and still the season's biggest schedule risk** | 2027 is a full control-system replacement. `reference/team-ops/03_programming_stack.md` documents it thoroughly, but documentation is not hands-on time. Watch for a beta announcement |
| 8 | **Pneumatics decision unresolved** | **Still open; resolves on its own** | FIRST said explicitly it may **remove pneumatics entirely** for 2027. Any off-season prototyping that assumes pneumatics may be wasted. Resolved by the Robot Rules Preview, expected **late Oct 2026** |

**One gap this list did not know about, found later and now closed** `[AUDIT 2026-09-04]`. The
2026-08-23 beta test ran the kickoff autorun against two real manuals and found that
`tools/frc_spans.py` returns an **empty parse** on a pre-2023 manual while every downstream section
still renders, so a review could have been written on nothing. `RUN-KICKOFF.sh` now hard-fails on an
implausible parse. See [`../review/BETA_TEST_REPORT.md`](../review/BETA_TEST_REPORT.md) §2.2 and
`../reference/00_SYSTEM_AUDIT.md` §9.9. It is the most consequential defect either pass found, and
this list would never have found it, because it was a testing gap rather than a missing feature.

---

## 7. Do this next — prioritized

`[AUDIT 2026-09-04]` **Re-checked, 13 days on. Items 4, 5 and 6 are done; item 1 is 20 days away and
is the only near-term deadline this project owns.** The list is kept below as written, with the
current state of each item stated first, because a plan that quietly loses its history is not a plan.

| # | Item | State on 2026-09-04 |
|---|---|---|
| 1 | Calendar **Sept 24, 2026**, Kit & Kickoff registration and Round 1 preferencing | **Open, 20 days out.** The only hard FRC deadline before November. Not a code task and nothing in this repository can do it |
| 2 | Read `FRC_VS_FTC_ORIENTATION.md` now, not at kickoff | **Open.** A reading task, unchanged |
| 3 | Monitor late Oct 2026 for the Robot Rules Preview, and `frc2027/` for staging | **Open.** `frc2027` re-probed 2026-09-04: nothing live. Re-run `tools/probe-2027-manual.sh` on a timer |
| 4 | Build the scouting schema and the cycle/EV model before December | **DONE**: `tools/scouting-plan.py`, `tools/cycle-model.py`, `tools/match-sim.py`. §6 gaps 3 and 4 |
| 5 | Build the Team Update differ | **DONE**: `tools/teamupdate-diff.py`. §6 gap 5 |
| 6 | Dry run the full playbook against the 2026 REBUILT manual, end to end | **DONE, twice over, and it paid for itself.** `review/REHEARSAL_*` and `review/BETA_TEST_REPORT.md`: three runs against REBUILT and 2019 DEEP SPACE, **four defects found and fixed**, including the silent empty parse in §6's note. The beta stopped short of writing the nine-section `REVIEW.md`; the run **after** it did not. `review/DEEPSPACE_20260824T032851Z/` (which `review/LATEST` points at) is a complete kickoff-morning output: 133-page manual ingested, 169 rules diffed against 2018 POWER UP, ranked strategies, a BOM that converged through three gate failures, awards, loopholes, Q&A questions and a betting sheet. **The whole pipeline has now been run end to end on a game whose answers are known** |
| 7 | Re-run `tools/tba_award_scrape.py` after the first 2027 events | **Open by design.** Cannot run before events exist. Award names have churned every season 2023→2026 |
| 8 | **Nov 12, 2026**, Pre-Kickoff Virtual Kit Release | **Open, 69 days out.** The largest pre-kickoff information drop, and the first official confirmation of Systemcore KoP distribution, which is currently only a `[COMMUNITY]` claim |

**Add one date this list did not carry: 2026-11-21**, the earliest order-by that `bom-builder.py`
computes on all three worked examples, driven by the 6-week-lead electrical package. Re-run
`reference/bom/recheck_prices.sh` before it. FRC vendor pricing moves in the autumn, and the
2026-09-04 URL re-curl deliberately did not re-verify a single price.

The original list, unedited:

1. **Calendar Sept 24, 2026, 12:00 p.m. ET, with a reminder a week out.** Kit & Kickoff registration plus Round 1 event preferencing. New for BIOCORE: you **must** include an event in your home country in Round 1. This is the only hard FRC deadline inside the next month.
2. **Read [`reference/FRC_VS_FTC_ORIENTATION.md`](../reference/FRC_VS_FTC_ORIENTATION.md) now, not at kickoff.** Especially §2 (district points) — if you are in a district, awards and pickability are worth up to 14 points each and nothing else in this project told you that.
3. **Set a monitor for late Oct 2026: the Robot Rules Preview.** 2026's landed Oct 24, 2025. In a control-system transition year it will be unusually large, and it resolves the pneumatics question, the legacy motor-controller removals, and the A301's FRC legality. Also watch `firstfrc.blob.core.windows.net/frc2027/` — **the moment it returns anything but 404, kickoff assets are staging.**
4. **Build the scouting schema (gap 3) and the cycle/EV model (gap 4) before December.** Both are game-agnostic. Building them on kickoff day costs you the hours you most need for the manual.
5. **Build the Team Update differ (gap 5).** Twenty-two updates a season, each one able to silently change a rule you designed around. The manual-diff half already exists in `frc_diff.py` and `frc_spans.py`.
6. **Do a dry run of the full playbook against the 2026 REBUILT manual, end to end.** The ingest step is proven; Phases 1–4 are not. Running the prompts against a game whose answers you already know is the cheapest possible way to find the next Fix-1-class defect. Budget an afternoon.
7. **Re-run `tools/tba_award_scrape.py` after the first 2027 events.** Award names have churned every season 2023→2026; the current list is a 2026 baseline, not a 2027 guarantee.
8. **Nov 12, 2026 — Pre-Kickoff Virtual Kit Release.** The largest pre-kickoff information drop and the first place Systemcore's KoP distribution gets officially confirmed (currently only a `[COMMUNITY]` claim from Chief Delphi).

---

## 8. Files changed by this pass

| File | Change |
|---|---|
| `README.md` | **created** — entry point, reading order, Sept-12 answer above the fold, tag legend |
| `reference/FRC_VS_FTC_ORIENTATION.md` | **created** — FRC-only structures, all cited to the 2026 manual |
| `research/00_AUDIT.md` | **created** — this file |
| `KICKOFF_PLAYBOOK.md` | Step 1 rewritten (Fix 1); doc map dangling refs marked (Fix 7); R408 constraint row filled (Fix 5); orientation file added to map |
| `research/00_PREMISE_CORRECTION.md` | dangling `SMALL_TEAM_PLAYBOOK.md` ref replaced (Fix 7); side-by-side September date table added |
| `research/02_supplemental_docs_index.md` | p. 11 → p. 10 citation fixed + 10-row verification table (Fix 6); three file counts corrected (Fix 9) |
| `research/03_biocore_official_intel.md` | Systemcore dimensions + added specs (Fix 2); field-dimension correction block (Fix 3); registration fee (Fix 4) |
| `research/04_biocore_community_intel.md` | REBUILT Tower points and tiered BONUS RP thresholds (Fix 8) |
| `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` | weight limits corrected (Fix 5); dangling `05_*` ref replaced (Fix 7) |

Nothing was deleted. Every correction is marked inline with `[AUDIT 2026-08-22]` and states what the previous text said, so the review can audit the auditor.
