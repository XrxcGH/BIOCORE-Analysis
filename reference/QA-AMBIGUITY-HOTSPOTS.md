# Q&A Ambiguity Hotspots — where FRC rules are actually unclear

**Purpose:** the GDC Q&A system is a public record of *every rule teams could not parse on their own*.
Aggregating question volume per rule across the 2024–2026 numbering era produces an empirical map of
where BIOCORE's rules will be ambiguous — i.e. where the loopholes live. This is the highest-signal
loophole predictor in the project because it is behavioural data, not opinion.

**Companion files:** `research/rule_inventories/qa_heat_2024..2026.tsv`, `qa_heat_slots.tsv`,
built by `tools/frc_qa_scrape.py` + `tools/qa-rule-heat.py`. ·
`reference/RULE-CHURN-WATCHLIST.md` **§4 Tier INSPECTION** carries the same bumper/perimeter cluster
with Team Update churn beside the question counts; §2.1 below and that tier are the same cluster
counted two ways and must agree.

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Counted directly from scraped FRC Q&A records |
| **[H]** HISTORICAL-PATTERN | Pattern across 2024–2026; not stated for BIOCORE |
| **[S]** SPECULATION | Inference. Flagged as such |

**Source shorthand:** `REB`=2026 REBUILT (166pp) · `REEF`=2025 REEFSCAPE (164pp) · `CRES`=2024 CRESCENDO (153pp).
**Era note:** FRC renumbered every rule in 2024. Only **2024–2026** are ID-comparable, and BIOCORE will
use this same scheme — so this table maps directly onto the BIOCORE manual. [C]

---

## 1. The hotspot table [C]

Questions asked per rule, 2024–2026 combined.

| Rule | '24 | '25 | '26 | Total | Headline (2026) |
|---|--:|--:|--:|--:|---|
| **R402** | 3 | 9 | 16 | **28** | BUMPER construction |
| **G211** | 5 | 9 | 12 | **26** | Egregious or exceptional violations |
| **G416** | 4 | 1 | 18 | **23** | This isn't combat robotics |
| **R401** | 8 | 2 | 12 | **22** | BUMPERS almost all around |
| **G413** | 6 | 5 | 11 | **22** | Expansion limits |
| **G409** | 6 | 13 | 1 | **20** | ROBOTS must be safe |
| **R404** | 2 | 8 | 9 | **19** | BUMPERS must be soft |
| **R405** | 1 | 10 | 8 | **19** | BUMPERS interact with BUMPERS |
| **G415** | 4 | 1 | 12 | **17** | Stay out of other ROBOTS |
| **R408** | 13 | 3 | 0 | **16** | Weight limit with BUMPERS |
| **R101** | 5 | 4 | 6 | **15** | ROBOT PERIMETER must be fixed |
| **G406** | 5 | 9 | 1 | **15** | Don't abuse SCORING ELEMENTS |
| **G419** | 0 | 9 | 5 | **14** | Don't collude with partners to shut down major parts of gameplay |
| **R409** | 6 | 1 | 5 | **12** | BUMPERS should be passive |
| **G411** | 6 | 4 | 2 | **12** | Don't damage the FIELD |
| **G425** | 5 | 1 | 6 | **12** | SCORING ELEMENT delivery |
| **R203** | 5 | 4 | 3 | **12** | General safety |
| **G210** | 0 | 7 | 5 | **12** | Don't expect to gain by doing others harm |
| **G418** | 0 | 4 | 8 | **12** | There's a 3-count on PINS |
| **R106** | 0 | 0 | 12 | **12** | Horizontal extension — one direction at a time |
| **G403** | 7 | 0 | 4 | **11** | Limited AUTO opponent interaction |
| **G302** | 3 | 3 | 4 | **10** | Limit what you use during a MATCH |

## 2. The three clusters that matter

### 2.1 BUMPERS are the #1 ambiguity zone [C]

**R401, R402, R404, R405, R408, R409 together drew 116 questions** — more than any other topic by a
wide margin, and the count is *rising* (R402: 3 → 9 → 16).

Bumpers are deceptively hard: they are geometrically constrained, interact with the frame perimeter,
carry a weight rule, and every season adds game-specific interactions with field elements. They are
also the **most common inspection failure**, so ambiguity here costs you matches, not just points.

> **Kickoff action:** read the BIOCORE R4xx block *first*, before any CAD — bumper geometry
> constrains the frame perimeter, so a chassis drawn first is a chassis drawn twice. Build a
> dimensioned bumper drawing on day 1 and submit a Q&A question on anything the text does not resolve
> exactly. [S]

**This is mandatory axis (b) of the loophole hunt** (`CLAUDE.md` §Step 5 ¶6): a strategic misread
costs points in one match, an inspection failure costs matches. The 2026 rehearsal hunt scored A− on
strategic rules and named **zero** of R402/R401/R404/R405/R101/G425 — 57 questions, **19.5% of the
whole season's Q&A**. The prior was already in this file and simply was not consulted. At least two
week-1 Q&A questions must now come from this cluster. See `reference/RULE-CHURN-WATCHLIST.md` §4.

### 2.2 Robot-to-robot contact and defense [C]

**G416** (combat robotics), **G415** (stay out of other ROBOTS), **G418** (3-count on PINS),
**G210** (gain by doing harm), **G403** (AUTO interaction) — **75 questions combined**.

G416's spike from 1 → 18 in a single season shows how sharply contact interpretation shifts when the
game's geometry changes. This is where "is the penalty cheaper than the points" analysis lives, and
where referee inconsistency is highest.

### 2.3 Extension and volume limits [C]

**G413** (expansion limits, 22) plus **R106** (horizontal extension, 12 in 2026 alone) plus **R101**
(fixed perimeter, 15).

**R106 is the tell:** 0 questions in 2024 and 2025, then **12 in its first year of existence**. A newly
written rule generated immediate confusion. [C] BIOCORE will introduce its own new
game-specific rules, and *those* are where the first-week questions — and the exploits — will concentrate. [S]

### 2.4 The catch-all: G211 [C]

**G211 "Egregious or exceptional violations" (26 questions)** is the referee's discretionary escalation
rule. Teams repeatedly ask where the line is because the rule is deliberately unbounded. Treat any
strategy whose viability depends on *not* being judged egregious as carrying real referee risk.

## 3. How to use this on kickoff day

1. Run the rule inventory on the BIOCORE manual and pull the **R4xx (bumpers)**, **G41x/G42x
   (contact/scoring)**, and **G413/R101/R106 (extension)** blocks first — statistically the ambiguity core.
2. For each, diff against the REB text (`research/rule_inventories/2026_rules_full.txt`, which is not
   in the repository because FIRST's text is not redistributed; `bash tools/rebuild-corpus.sh`
   rebuilds it locally). **Changed wording in a historically hot rule is the highest-value thing in
   the manual.** [S]
3. Draft Q&A questions the same week — Q&A answers are binding and early questions get answered before
   the field is crowded.
4. Re-run `tools/frc_qa_scrape.py` through the BIOCORE season to watch where questions concentrate in
   real time; that is a live map of what everyone else is confused about.

## Files written by this pass
- `reference/QA-AMBIGUITY-HOTSPOTS.md` (this file)

## Known limitations
- Question *volume* measures confusion, not exploitability — a hot rule may be merely wordy. Pair this
  with the loophole case book before acting.
- 2008–2023 columns exist in `qa_heat_slots.tsv` but use pre-2024 rule IDs and are **not** comparable
  to the table above without the crosswalk files.
- Scrape coverage depends on the Q&A archive remaining reachable; counts are lower bounds.
