# FRC Structures That Have No FTC Analogue

**Written 2026-08-22 by the audit pass.** Created to close the largest content gap in this workbench: the project contained **zero** mentions of district points, double-elimination playoffs, backup robots, or practice matches, and only glancing mentions of stop-build and event weeks. Every one of those changes what "a good BIOCORE robot" means.

Every fact below is `[VERIFIED]` against the local 2026 REBUILT Game Manual (`manuals/archive/frc/2026_REBUILT_GameManual.pdf`, Version TU22, 166 pp.) with the rule/section and manual page cited, or against a linked primary source. That PDF is not in the repository, because FIRST's documents are not redistributed; `bash tools/rebuild-corpus.sh --fetch` downloads it. **These are 2026 priors, not 2027 facts.** Re-verify each against the BIOCORE manual at kickoff; the section numbers are stable across seasons, the values are not.

---

## 1. There is no bag day. There is no stop-build day.

`[VERIFIED]` The strings "bag and tag", "stop build", "withholding allowance", and "bag day" appear **zero times** in the 2026 manual (full-text search of the extracted manual). FIRST eliminated the bag/stop-build model after the 2019 season and has not reinstated it.

**What this means, and it is the single biggest FTC→FRC mindset change:**

- The robot is legal to modify **continuously, all season, up to and including between matches at an event**. There is no sealed period.
- Therefore **iteration between events is the dominant competitive strategy in FRC**, in a way it is not in FTC. A team that competes Week 1 and Week 4 gets three weeks of live-data-driven rework. Plan the build calendar around *two robots' worth of iteration*, not one build-then-freeze cycle.
- The corollary trap: **your Week 1 robot is a prototype**. Teams that treat the first event as the finish line under-invest in the rework capacity that actually decides their season.
- Re-inspection governs what you may change at an event — see §5.

`[INFERENCE]` Nothing in the 2027 calendar or any 2026 blog suggests a return. Confirm against BIOCORE §4/§5 and the I-rules at kickoff, then stop thinking about it.

---

## 2. Districts vs. Regionals — two different games above the robot

This is a genuine fork in season strategy and it is invisible in the game manual's G-rules.

| | **Regional model** | **District model** |
|---|---|---|
| Where | Most of the world outside district territories | MI, MAR, NE, PNW, CHS, FIT, FIM, ISR, ONT, PCH, FNC, IN, and others |
| Season registration `[VERIFIED]` | $6,500 includes **one** Regional | $6,500 includes **two** District events |
| Advancement | Win/award at a single Regional | **Cumulative district points** across the season |
| Second chances | Each Regional is independent — a bad event is survivable by attending another | Points accumulate; a bad event **permanently lowers your season total** |

### 2.1 The district points table `[VERIFIED — 2026 manual §11.1, Table 11-1, p. 133]`

Teams are ranked on points earned at their **first 2 home District events plus their District Championship**:

| Category | Points |
|---|---|
| Qualification round performance | Normal distribution, **22 (top) down to 4 (bottom)** by an equation (§11.1.1). Max 22 at any event size; typically min 4. |
| ALLIANCE CAPTAIN | **17 − captain number** (Alliance #3 captain → 14) |
| Draft order acceptance | **17 − draft acceptance number** (5th accepted → 12) |
| Playoff advancement | By round participation and whether the alliance advances (§11.1.3) |
| Team judged awards | **10** FIRST Impact · **8** each Engineering Inspiration and Rookie All Star · **5** each all other team judged awards |
| Team age | **10** for that-season rookies · **5** for prior-season rookies |

> **District Championship points are multiplied by ×3** and added to the district-event total. `[VERIFIED]` §11.1, p. 133.

### 2.2 Why this belongs in a *scoring strategy* review

Three consequences a game-manual-only reading never surfaces:

1. **Awards are worth robot-performance points.** FIRST Impact = 10 points, the same order as a strong qualification finish. In the district model, the business/outreach team is scoring in the same currency as the drive team. Any BIOCORE strategy review that optimizes only match points is optimizing a fraction of the objective. Cross-reference `reference/team-ops/05_business_awards_sustainability.md` and `reference/awards/`.
2. **Getting picked is worth almost as much as winning.** Draft acceptance at slot 5 = 12 points; being Alliance #3 captain = 14. **Being a robot other teams want to pick is a scoring strategy.** This is what makes scouting-legible, single-role reliability so valuable in FRC — and it is why "do one thing flawlessly" beats "do everything adequately" more decisively here than in FTC.
3. **The ×3 District Championship multiplier makes late-season peak form worth triple.** Combined with no stop-build (§1), the optimal district build curve is deliberately back-loaded relative to what FTC intuition suggests.

`[INFERENCE]` New for BIOCORE `[VERIFIED — see 03 §6]`: Regional-level teams may register for District events at **$1,000** from Nov 5, 2026, but **cannot earn Regional Points, cannot advance directly to Championship, and cannot win Cultural Awards** at them. Read those events as practice/scouting only.

---

## 3. Event weeks, Week 0, and the schedule-as-strategy

`[VERIFIED — FIRST Calendar]` The 2027 regular season is **7 weeks**: Week 0 **Feb 20**, then Weeks 1–7 starting **Mar 3, Mar 10, Mar 17, Mar 24, Mar 31, Apr 7, Apr 14**, with the season closing **Apr 18**. Championship **Apr 28 – May 1, 2027**, George R. Brown Convention Center, Houston (`[VERIFIED]` committed **through 2034**).

Why the week number is a strategic variable:

- **Scores inflate across the season.** Week 1 winning scores and Week 6 winning scores are different games. `research/predictive_tba/` holds the week-by-week inflation data — use it, do not eyeball it.
- **Week 1 is an information event.** Rules get tested, Q&A answers land, Team Updates react. A Week 1 team pays for the privilege of discovering the game's real meta and then gets weeks to exploit it. A Week 5/6 team inherits a solved meta and must arrive already competitive.
- **Week 0** is an unofficial scrimmage-style event, not a qualifying event — it is a field-test opportunity, and the only chance to touch an official field before it counts.
- **Team Update cadence is asymmetric** `[VERIFIED — 2026 §1.8, p. 11]`: Tuesday **and** Friday from the first Tuesday after Kickoff until the Tuesday before Week 1; **Tuesdays only** from Week 1 onward. The rule-volatility window is the build season, and it closes right as events start.

---

## 4. Playoffs: 8 alliances, 3 teams, double elimination

`[VERIFIED — 2026 manual §10.6, p. ~126]`

- Alliance selection produces **8 ALLIANCES of 3 teams** (§10.6.1). Round 1 picks descend Alliance 1→8; round 2 ascends.
- Playoffs are a **double-elimination bracket**. Teams do not earn Ranking Points in playoffs; they advance on win/loss/tie.
- A team that **declines** an invitation is ineligible to be a **BACKUP TEAM** and is out of the playoff tournament.
- **DISQUALIFICATION** in a playoff match zeroes the whole alliance's match points.

**Strategic consequences absent from the rest of this workbench:**

- Double elimination means **one bad match does not end your event**. Risk tolerance in the first playoff match should be higher than single-elimination intuition suggests; risk tolerance in the lower bracket should be lower.
- The **3rd robot on an alliance is a real role**, and it is usually a specialist — defense, a specific scoring lane, or an endgame guarantee. Design so that your robot is *legible* as one of those. Whatever BIOCORE's equivalent of "the thing an alliance still needs" turns out to be, that is the pick-me niche.
- **Backup robot rules matter** to teams that get picked and to teams planning for mechanical failure. Find BIOCORE's T-rule analogue.

### Ranking Score

`[VERIFIED — 2026 §10.5]` Rank is by **Ranking Score (RS)** = total RP across qualification matches ÷ matches scheduled (excluding SURROGATE matches), to 2 dp. **It is an average, not a sum** — so a surrogate match or a match you were not scheduled for does not dilute you, but a zero-RP match does, permanently.

---

## 5. The FRC inspection flow

FRC inspection is a gated, repeatable process, not a one-time check. `[VERIFIED — 2026 manual §9, I-rules, pp. 115+]`

| Rule | Substance |
|---|---|
| **I101** | The ROBOT and its MAJOR MECHANISMS must be built by the team ("it's your team's robot") |
| **I102** | **Get inspected before playing a Qualification MATCH** — no inspection, no qual play |
| **I103** | **Bring it all to inspection** — the OPERATOR CONSOLE *and* the ROBOT, including every mechanism that might be used in any configuration |
| **I104** | **Any change to a ROBOT must get re-inspected**, unless it is on the enumerated exception list |
| **I105** | **Don't exploit re-inspection** — the anti-abuse rule that closes the I104 loophole |
| **I107** | **No STUDENT, no inspection** — at least one student must accompany the robot |

`[VERIFIED — §9, p. 115]` **The Lead ROBOT INSPECTOR (LRI) has final authority on the legality of any COMPONENT, MECHANISM, or ROBOT**, and inspectors may **re-inspect at any time**.

**What this means for design strategy:**

1. **I103 is the weight trap.** All mechanisms for all configurations weigh in *together*. A swappable-mechanism strategy is priced at the sum of every swappable part, not the heaviest single configuration. 2026 R103 = **115.0 lb** bare (excluding BUMPERS, battery + its Anderson half, and event location tags); R408 = **135.0 lb** with BUMPERS.
2. **I104/I105 govern in-event iteration.** Because there is no bag day (§1), the real constraint on between-match changes is the re-inspection rule, not a sealed bag. Read the I104 exception list on kickoff day — it defines how fast you are allowed to iterate at an event.
3. **The checklist is not the manual.** `[VERIFIED — see 02 §5]` The Inspection Checklist is the *operationalization* of the R-rules. **R-rules present in the manual but absent from the checklist are effectively self-reported.** On kickoff day, diff the BIOCORE checklist against the full R-rule list and flag every unchecked R-rule. Local checklists 2013, 2015–2026 are in `manuals/archive/supplemental/`.

---

## 6. Q&A: timing is the whole game

`[VERIFIED]` Official Q&A opens **Jan 13, 2027** (4 days after kickoff) and closes **Apr 21, 2027**.

`[VERIFIED — 2026 §1.9, p. 11]` Three properties FTC experience does not prepare you for:

- **Q&A jurisdiction is wider than the manual.** It clarifies the Game Manual, the **Awards webpages**, the **official FIELD drawings**, and the **District and Regional Events webpage**. Those webpages are rule-bearing.
- **Q&A answers do not supersede the manual.** Referees and inspectors remain the ultimate authority.
- **Q&A can *cause* manual revisions**, communicated via Team Updates. This is the lever: a well-constructed question filed in the first two weeks is the cheapest route to getting an ambiguity resolved in writing. Questions filed late get answered but rarely produce a Team Update.

**Therefore Phase 4 of the playbook has a real deadline.** Draft questions during the kickoff review and file them in week 1, before the queue floods. See `reference/QA-AMBIGUITY-HOTSPOTS.md` for where questions historically concentrate — bumpers and in-match contact, every year.

---

## 7. Quick FTC→FRC translation table

| FTC concept | FRC equivalent | Difference that bites |
|---|---|---|
| StarterBot | **KitBot** | Different schedule, different purpose; released at/around kickoff, iteration guide included |
| Control Hub / Driver Hub | **Systemcore** (2027) replacing roboRIO | Full control-system replacement year — see `reference/team-ops/03_programming_stack.md` |
| Competition Manual with pre-released sections | **No FRC preview exists** | The entire BIOCORE manual drops at once, Jan 9, 2027 |
| League play / meets | **Districts** (points) or **Regionals** (independent) | Cumulative vs. independent scoring above the robot |
| Inspection at each event | Same, plus **I104 re-inspection on any change** | No bag day means re-inspection is the real iteration governor |
| Ranking by OPR/TBP tiebreakers | **Ranking Score = mean RP** | It is an average; sort criteria are manual-defined, per season |
| — | **District points for awards and for being picked** | Awards and pickability are literally scoring |

---

## Open questions to answer from the BIOCORE manual

1. Does BIOCORE tier its BONUS RP thresholds by event level, as REBUILT did (ENERGIZED 100 / 240 / 360)? See `research/04_biocore_community_intel.md` §1.
2. What is in the I104 change-without-re-inspection exception list for 2027?
3. Does the 2027 district points table change? (It has been stable for years, but the Regional-team-at-District change for 2027 touches §11.)
4. What is the 2027 playoff bracket — still 8 alliances of 3, still double elimination?
5. Does the BIOCORE Inspection Checklist cover the Systemcore-specific R-rules, or are they self-reported in year one?
