# BIOCORE Rule Watchlist — three independent signals, triangulated

**Purpose:** predict, before the manual exists, which BIOCORE rules will be ambiguous, contentious,
and strategically exploitable. Three unrelated datasets are combined; where they agree, the signal is
strong, because each measures a different kind of failure.

**Companion files:** `reference/QA-AMBIGUITY-HOTSPOTS.md` (the Q&A-volume view of the same rules;
§2.1 there and §4 here are the same cluster counted two ways and must agree) ·
`research/rule_inventories/qa_heat_*.tsv` ·
`research/teamupdate_analysis/{2026_tu_churn,slot_churn_allseasons}.tsv` ·
`reference/validation/ingest_dryrun_REBUILT_vs_REEFSCAPE/rules_GAMESPECIFIC.tsv`

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Computed from primary data in this repo; reproducible |
| **[H]** HISTORICAL-PATTERN | Holds across 2024–2026; not stated for BIOCORE |
| **[S]** SPECULATION | Inference. Flagged as such |

**Era note [C]:** FRC renumbered every rule in 2024. Only **2024–2026** are ID-comparable, and
**BIOCORE uses this same scheme** — so these slot numbers map forward directly.

---

## 1. The three signals

| # | Signal | What it measures | Source |
|---|---|---|---|
| **A** | **Q&A heat** | Teams *could not parse the rule* and had to ask | 3 seasons of scraped Q&A |
| **B** | **Team Update churn** | *FIRST could not leave it alone* and amended it mid-season | 67 Team Updates, 2024–26 |
| **C** | **Game-specific flag** | The rule is **new this season**, not evergreen | headline colour, manual §1.6 |

A measures reader confusion. B measures author regret. C measures novelty. A rule scoring on all
three is where a high-school team gets blindsided and a prepared team gets an edge.

## 2. Tier 1 — high on **all three** signals [C]

These are the archetypes to watch for in BIOCORE. Same rule *numbers*, new game nouns.

| Rule | Q&A '24–26 | TU amendments | Game-specific? | 2026 headline |
|---|--:|--:|:--:|---|
| **G413** | 22 | 3 | ✅ | Expansion limits |
| **R106** | 12 | 5 | ✅ | Horizontal extension — one direction at a time |
| **G403** | 11 | 7 | ✅ | Limited AUTO opponent interaction |
| **G420** | — | 6 | ✅ | TOWER protection *(the season's protected-zone rule)* |
| **G427** | — | 3 | ✅ | The OUTPOST has a storage limit |

**R106 is the case study.** It did not exist before 2026. In its first season it drew **12 Q&A
questions** (0 in each of the two prior years) *and* was amended in **5 separate Team Updates**
(TU02, TU03, TU06, TU13, TU14). A brand-new game-specific constraint that neither teams nor FIRST
could pin down. **BIOCORE will have its own R106.** [S]

## 3. Tier 2 — evergreen but permanently contentious [C]

These are *not* new each year, yet they generate confusion and amendments every single season. They
are load-bearing and never settle.

| Rule | Q&A '24–26 | TU amendments (seasons hit) | 2026 headline |
|---|--:|--:|---|
| **G415** | 17 | **12** (3/3) | Stay out of other ROBOTS |
| **G416** | 23 | **6 in 2026 alone** | This isn't combat robotics |
| **G211** | 26 | 8 (3/3) | Egregious or exceptional violations |
| **R402** | 28 | 7 (3/3) | BUMPER construction |
| **G409** | 20 | 8 (3/3) | ROBOTS must be safe |
| **G210** | 12 | 5 (3/3) | Don't expect to gain by doing others harm |
| **G425** | 12 | 5 (3/3) | SCORING ELEMENT delivery |

**G416 was amended six times in one season** (TU00, TU03, TU14, TU16, TU17, TU19) — more than any
other rule in the 2026 corpus. Robot-to-robot contact is the least stable area of FRC rules, full
stop. Any strategy whose value depends on a particular contact interpretation is built on sand. [S]

## 4. Tier INSPECTION — the cluster that stops the robot playing at all [C]

Tiers 1 and 2 are read through a *strategic* lens: which rule will cost me points or a penalty. This
tier is the other axis, and it was the 2026 rehearsal's blind spot — the loophole hunt named **zero**
of these rules while they carried **19.5% of the season's Q&A**. It is broken out separately so it
cannot be skipped again. `CLAUDE.md` §Step 5 ¶6 makes it mandatory axis (b) of the loophole hunt.

Q&A columns are from `reference/QA-AMBIGUITY-HOTSPOTS.md` §1; TU columns from
`research/teamupdate_analysis/slot_churn_allseasons.tsv` (2024+ era only).

| Rule | Q&A '24–26 | Q&A 2026 | TU amendments (seasons hit) | 2026 headline |
|---|--:|--:|--:|---|
| **R402** | **28** | **16** *(rank 2 of 91)* | **7** (3/3) | BUMPER construction |
| **R401** | **22** | **12** *(rank 3)* | 3 (2/3) | BUMPERS almost all around |
| **R404** | 19 | 9 | 2 (2/3) | BUMPERS must be soft |
| **R405** | 19 | 8 | 1 (1/3) | BUMPERS interact with BUMPERS |
| **R408** | 16 | 0 | 2 (1/3) | Weight limit with BUMPERS |
| **R409** | 12 | 5 | 4 (2/3) | BUMPERS should be passive |
| **R101** | 15 | 6 | 3 (2/3) | ROBOT PERIMETER must be fixed |
| **R106** | 12 | **12** | **5** (1/3) | Horizontal extension — one direction at a time |
| **R105** | — | — | 3 (1/3) | Extension limits |
| **R107** | — | — | 3 (1/3) | Extension limits |
| **G425** | 12 | 6 | 5 (3/3) | SCORING ELEMENT delivery *(sits across both axes)* |

**The bumper six — R401, R402, R404, R405, R408, R409 — drew 116 Q&A questions across 2024–2026**,
more than any other topic by a wide margin, and R402's count is *rising*: 3 → 9 → 16. [C]

**Why this tier gets its own heading.** Tier 1 and Tier 2 rules cost you points or a penalty inside a
match you are still playing. These cost you the match itself: bumpers are the most common inspection
failure, and a robot that fails inspection does not play until it is fixed. The confusion is
structural, not incidental — bumpers are geometrically constrained, they interact with the frame
perimeter and the weight limit simultaneously, and every season adds new game-specific interactions
with field elements. That is also why the R4xx block is read **before any CAD** (`CLAUDE.md` §Step 2
item 3): bumper geometry constrains the frame perimeter, so a chassis drawn first is a chassis drawn
twice. [C→S]

**Kickoff action:** dimensioned bumper drawing on day 1; **at least two** week-1 Q&A questions filed
from this tier.

## 5. What this predicts for BIOCORE

1. **Bumpers (R4xx) and contact (G41x) will be the ambiguity core again.** [H] They have been in
   every season measured. Read them first, before CAD — see **§4 Tier INSPECTION** for the per-rule
   numbers and `reference/QA-AMBIGUITY-HOTSPOTS.md` §2.1 for the Q&A-volume view.
2. **The protected-zone rule will churn.** G420 was TOWER protection in 2026 and was amended in all
   three seasons under some name. BIOCORE will have a protected zone; its rule will move. [S]
3. **The newest game-specific rule will be the most confusing one.** [C→S] R106's pattern.
   On kickoff day, the rules flagged game-specific by `ingest-manual.sh` that have **no analogue in
   REBUILT** are the highest-risk, highest-opportunity text in the manual.
4. **Amendment volume is rising:** 41 distinct rules amended in 2019 → 102 in 2024 → 66 in 2026,
   across a stable ~22 updates/season. Expect **60–100 rules amended during BIOCORE.** [C]
5. **Design margin, not design-to-the-line.** Because these rules move mid-season, a robot built
   exactly to a stated limit can be made illegal by a Team Update in February. Build in margin on
   extension, bumper geometry, and anything near a protected zone. [S]

## 6. How to run this during the BIOCORE season

```bash
# Run from the repository root.

# Kickoff: which rules are game-specific (blue headline)?  -> the new game
bash tools/ingest-manual.sh manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf V1

# Weekly through the season: what did FIRST change this week?
python tools/teamupdate-diff.py season 2027 --watch

# Any time: which slots churn historically?  -> where to expect the next amendment
python tools/teamupdate-diff.py slots
```

`--watch` records what it has already reported, so a weekly run prints **only new updates**. Any rule
you designed around appearing in that output is a design review, not a footnote.

## Files written by this pass
- `reference/RULE-CHURN-WATCHLIST.md` (this file)
- `tools/teamupdate-diff.py` — tested on 23 × 2026 updates and 168 updates across 2019–2026
- `research/teamupdate_analysis/{2026_tu_index,2026_tu_churn,slot_churn_allseasons}.tsv`

## Known limitations
- Rule IDs are harvested by regex from Team Update prose. A TU that changes a rule **without naming
  its ID** (prose-only, or a table edit) is invisible here. Section-number capture partly covers this.
- 2015–2018 Team Update directories exist but hold only combined PDFs, which are skipped to avoid
  double-counting; per-update granularity for those seasons is unavailable.
- Mention count ≠ magnitude. A one-word typo fix and a rule rewrite both count as one amendment.
  Use this to **rank what to read**, then read the actual diff.
- Q&A and TU signals both lag: they describe 2024–2026. BIOCORE's own game-specific rules have no
  history, which is exactly why signal **C** matters.
