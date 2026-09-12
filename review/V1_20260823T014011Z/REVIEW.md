# REVIEW — REHEARSAL (2026 REBUILT standing in for BIOCORE)

**Label:** REHEARSAL · **Manual:** `manuals/archive/frc/2026_REBUILT_GameManual.pdf` (version TU22, 166 pp.)
**Run:** `review/V1_20260823T014011Z/` · **Generated:** 2026-08-22

> **This is a dress rehearsal, not a BIOCORE analysis.** Every game fact below is REBUILT. The
> purpose was to test whether `CLAUDE.md`'s five-step autorun is self-sufficient. It is not, in
> three specific ways — see `review/REHEARSAL_FINDINGS.md`, which is the actual deliverable.
> **The most important defect: `mfg_floor` accepted an undocumented vocabulary and silently
> mis-gated 5 of 14 candidates, including the top three, with no error.** Findings §2.

---

## 1. Game summary

### 1.1 Phases `[VERIFIED Table 6-2, p.44]`

| Period | Timeframe | Duration | Timer |
|---|---|---:|---|
| AUTO | AUTO | 20 s | 0:20 – 0:00 |
| TELEOP | TRANSITION SHIFT | 10 s | 2:20 – 2:10 |
| TELEOP | SHIFT 1 | 25 s | 2:10 – 1:45 |
| TELEOP | SHIFT 2 | 25 s | 1:45 – 1:20 |
| TELEOP | SHIFT 3 | 25 s | 1:20 – 0:55 |
| TELEOP | SHIFT 4 | 25 s | 0:55 – 0:30 |
| TELEOP | END GAME | 30 s | 0:30 – 0:00 |

Total 2:40. TELEOP is 140 s **inclusive** of the 30 s END GAME.

### 1.2 The mechanic that defines the game: HUB duty cycle `[VERIFIED §6.4.1 + Table 6-3, p.44]`

FUEL scored in an **active** HUB is worth points; FUEL scored in an **inactive** HUB is worth
**nothing**. Both HUBS are active during AUTO, the TRANSITION SHIFT, and END GAME. During SHIFTS
1–4 exactly one ALLIANCE HUB is active and they alternate. **The ALLIANCE that scores more FUEL in
AUTO has its HUB set inactive for SHIFT 1** — an explicit anti-snowball inversion. Ties are broken
by FMS random selection, relayed through FMS Game Data at the start of TELEOP.

Consequence: **each alliance's HUB is active for only 10 + 50 + 30 = 90 s of the 140 s TELEOP
(64.3%)** `[COMPUTED]`. Every raw FUEL number the cycle model prints is inflated by 1.56×. This is
corrected by hand throughout §2 — the `game_def.json` schema cannot express a duty cycle.

### 1.3 Every scoring action and value `[VERIFIED Table 6-4, p.47]`

| Action | AUTO | TELEOP |
|---|---:|---:|
| FUEL scored in an **active** HUB | 1 | 1 |
| FUEL scored in an **inactive** HUB | — | — |
| Each ROBOT at TOWER **LEVEL 1** (max 2 ROBOTS in AUTO) | 15 | 10 |
| Each ROBOT at TOWER **LEVEL 2** | — | 20 |
| Each ROBOT at TOWER **LEVEL 3** | — | 30 |
| Win / Tie | 3 RP / 1 RP | |

**TOWER eligibility `[VERIFIED §6.5.2, p.46]`:** L1 = not touching carpet or TOWER BASE. L2 =
BUMPER covers completely above the LOW RUNG. L3 = completely above the MID RUNG. The ROBOT must
contact at least one RUNG and/or UPRIGHT **on their own TOWER**, and may additionally contact only
the TOWER WALL, support structure, FUEL, and/or another ROBOT. **A ROBOT may earn L1 only in AUTO,
and only a single LEVEL during TELEOP. A ROBOT that earned in AUTO may still earn in TELEOP.**

**Scoring criterion `[VERIFIED §6.5.1]`:** a FUEL is scored once it passes through the top opening
of the HUB and through the sensor array. TOWER points are judged by **human volunteers**, not
sensors — "make it obvious and unambiguous."

### 1.4 Zones and field elements

FIELD ≈ 317.7 in × 651.2 in. Named elements in the manual body: **HUB** (DMX-lit to show active
status), **TOWER** (TOWER BASE, TOWER WALL, LOW RUNG, MID RUNG, UPRIGHTS), **ALLIANCE ZONE**,
**NEUTRAL ZONE**, **OUTPOST** (has a storage limit, G427), **DEPOT**, **CHUTE** (HDPE CHUTE DOOR on
a pivot, retains ~25 FUEL), **TRENCH** (AprilTags centred on the opening), **ALLIANCE AREA**
(≈360 in × 134 in, infinitely tall). `[VERIFIED §5]`

### 1.5 Ranking formula `[VERIFIED §6.5.3, Table 6-5]`

Win 3 · Tie 1 · ENERGIZED 1 · SUPERCHARGED 1 · TRAVERSAL 1 → max 6 RP/match. Ranking is by
average RP; first tiebreak is average ALLIANCE MATCH points **excluding fouls**.

| BONUS RP | Metric | Regional/District | DCMP | Champs |
|---|---|---:|---:|---:|
| ENERGIZED | FUEL in an active HUB | 100 | 240 | 360 |
| SUPERCHARGED | FUEL in an active HUB | 360 | 360 | 500 |
| **TRAVERSAL** | **TOWER points in the MATCH** | **50** | **50** | **50** |

**TRAVERSAL is the only BONUS RP that does not escalate.** ENERGIZED escalates 3.6×. This single
row drives the entire recommendation in §4.

### 1.6 Endgame — **named**

**The endgame structure is a three-LEVEL TOWER CLIMB.** For scouting, that fixes the free-data
shape: FMS/TBA will publish a per-team **`Avg TOWER points`**-class column plus per-match endgame
LEVEL, available for all four teams without a scout in the stands
(`reference/SCOUTING-PLAN.md`, 4/4 seasons). Scout the two things FMS does *not* publish: **which
SHIFT a team scores in** (the duty-cycle mechanic is invisible in aggregate FUEL totals) and
**climb time**.

---

## 2. Scoring strategy `[COMPUTED — results/cycle_model.txt, results/cycle_sweep.txt]`

Baseline: 8 units/cycle, 8.0 s cycle, 3 FUEL in AUTO.

### 2.1 Points per cycle
8 FUEL × 1 pt = **8 pts/cycle**. Flat — REBUILT has no scoring gradient for FUEL, so there is no
"go higher for more points" axis. The only multiplier in the game is *whether the HUB is on*.

### 2.2 Raw vs duty-cycle-corrected totals

| | raw model | corrected (90 s active) |
|---|---:|---:|
| TELEOP cycles | 17.5 | 11.25 |
| TELEOP FUEL pts | 140 | **90** |
| AUTO FUEL pts | 3 | 3 |
| **Total, no climb** | **143** | **93** |

**Use the corrected column.** The raw column is what a kickoff-day team would have quoted at a
whiteboard and it is 54% too high.

### 2.3 Break-even for every endgame option

Because FUEL pays exactly 1 pt and a cycle is 8 pts / 8.0 s, **one second of active-HUB scoring
time is worth exactly 1 point** — which makes the break-even arithmetic unusually clean.

| Endgame | Points | Time cost | Cycles lost | Points lost | **NET** | Verdict |
|---|---:|---:|---:|---:|---:|---|
| TOWER L1 (TELEOP) | 10 | 8 s | 1.00 | 8 | **+2** | worth it, barely |
| TOWER L2 (TELEOP) | 20 | 15 s | 1.88 | 15 | **+5** | worth it |
| TOWER L3 (TELEOP) | 30 | 25 s | 3.12 | 25 | **+5** | worth it, no better than L2 |
| No climb | 0 | 0 s | 0 | 0 | 0 | — |
| TOWER L1 (**AUTO**) | **15** | ~6 s | — | — | **+15 vs +2** | **the best climb in the game** |

**The three headline conclusions:**

1. **L3 is not worth more than L2.** Both net +5. L3 costs a mill/lathe floor, a second novel
   mechanism, and 10 more seconds; L2 costs a winch. `[COMPUTED]` **Anyone who argues for L3 on
   points is wrong on the arithmetic.** L3's only real value is TRAVERSAL headroom (§2.5).
2. **AUTO L1 pays 15 and TELEOP L1 pays 10 for the same physical act.** A 50% premium for doing it
   20 seconds earlier, capped at 2 ROBOTS per alliance. This is the highest-value-per-hour action
   in REBUILT for a small team.
3. **A robot can bank both.** §6.5.2 explicitly allows an AUTO climber to also earn TELEOP points.
   A robot that climbs L1 in AUTO (15) and L2 in TELEOP (20) contributes **35 TOWER points alone**
   — 70% of TRAVERSAL by itself.

### 2.4 What one second of cycle time is worth

| | per match | per 12-match qual schedule |
|---|---:|---:|
| Raw model (8.0 → 9.0 s) | 15.6 pts | 187 pts |
| **Duty-cycle corrected** | **~10 pts** | **~120 pts** |

Read the sweep columns for flatness. `no endgame` runs 283 → 59 across 4 s → 20 s cycle (−79%);
`TOWER L3` runs 263 → 79 (−70%). **No REBUILT column is flat**, because FUEL is the only volume
scorer and everything is cycle-bound. That is itself a finding: REBUILT is a *bad* game for a
small team, and the small-team play is not to compete on cycle rate at all but to take the flat,
cycle-independent points — the climb — and to be the third robot (§3).

### 2.5 RP feasibility, solo vs alliance `[COMPUTED, corrected]`

| RP | Threshold | You alone | Alliance ×3 | Reachable? |
|---|---:|---:|---:|---|
| ENERGIZED (Reg/Dist) | 100 | 93 | 279 | **YES, alliance** — not solo. Raw model said "YES solo"; that is wrong. |
| ENERGIZED (DCMP) | 240 | 93 | 279 | Yes, but only with three competent scorers |
| ENERGIZED (Champs) | 360 | 93 | 279 | **NO** at this robot quality |
| SUPERCHARGED (all tiers) | 360–500 | 93 | 279 | **NO.** Not a design target at any tier. |
| **TRAVERSAL** | **50 TOWER pts** | up to 35 | — | **YES, cheaply** |

**The TRAVERSAL arithmetic is the whole strategic answer.** Cheapest legal path to 50:
2 ROBOTS × AUTO L1 (15 each) = 30, plus 2 ROBOTS × TELEOP L1 (10 each) = 20 → **exactly 50, using
only LEVEL 1 climbs.** No L2. No L3. No elevator. A passive latch and a good AUTO path clear a
full BONUS RP that costs Championship-calibre alliances the same 50 points it costs a district
rookie. **Build for that.**

---

## 3. Ranked strategies `[COMPUTED — results/strategy_ranking.txt]`

14 candidates, enumerated across all six generators of `STRATEGY-RANKING-SYSTEM.md` §2 (31 raw,
de-duplicated to 14). All ten §2.7 anti-blind-spot boxes have a row.

```
ACH >= 60  |         CHEAP INSURANCE          |          BUILD THIS          |
           |   S5 S6 S7 S14 S4 S12 S8 S3 S2   |             S10              |
ACH <  60  |             DELETE               |             TRAP             |
           |            S11 S1*               |          S9* S13*            |
```

| # | id | Strategy | ACH | VAL | idx | Quadrant | Tier | Binding constraint | What it means for 15 students |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | S5 | Feeder/support — herd NEUTRAL ZONE FUEL to the CHUTE | 93.1 | 39.0 | 68.7 | CHEAP INSURANCE | T1 GREEN | A4 drive practice | Zero mechanisms, zero dollars, and the corpus's **5/5** small-team archetype. Nobody on your team will propose it. It is the highest-achievability row on the board. |
| 2 | S6 | Deliberately simple and flawless — KOP + hopper dump + passive L1 | 90.1 | 40.3 | 67.7 | CHEAP INSURANCE | T1 GREEN | A4 drive practice | The `ARCH` I7 archetype, **5/5**. Never breaks, always contributes, gets picked third. |
| 3 | S7 | ENDGAME anchor, LOW tier — L1 only, passive latch | 88.3 | 34.5 | 64.1 | CHEAP INSURANCE | T1 GREEN | A6 graceful degradation 3/5 | 40 h, $250, and it delivers 15 AUTO + 10 TELEOP points every single match. |
| 4 | **S10** | **TRAVERSAL RP specialist — reliable L2 + coach partners to 50** | **67.7** | **58.6** | **63.6** | **BUILD THIS** | **T1 GREEN** | **A5 reliability 3/5** | **The only candidate in the BUILD THIS quadrant.** It is the only row whose value comes from an RP that never escalates. |
| 5 | S14 | Uncontested-window scorer — score only while own HUB is active | 73.4 | 42.8 | 59.6 | CHEAP INSURANCE | T2 STRETCH | A2 workstreams | Correct read of the game, but still a scoring mechanism, so it costs a stream. |
| 6 | S4 | Pure defense — zero scoring mechanisms | 86.4 | 25.5 | 59.0 | CHEAP INSURANCE | T2 STRETCH | A4 = 0/5 | Free to build, impossible to drive. Soft gate G6: needs the driver hours you do not have. |
| 7 | S12 | Choke-point denial — speed-only, owns the TRENCH lane | 85.5 | 25.5 | 58.5 | CHEAP INSURANCE | T2 STRETCH | A4 = 0/5 | Same. Defense is cheap in dollars and ruinously expensive in seat time. |
| 8 | S8 | ENDGAME anchor, MID tier — L2 winch | 65.6 | 49.7 | 58.4 | CHEAP INSURANCE | T2 STRETCH | A4 drive practice | S10 without the RP framing. Strictly dominated by S10. |
| 9 | S3 | AUTO-only specialist | 78.2 | 33.1 | 57.9 | CHEAP INSURANCE | T2 STRETCH | **A6 = 1/5** | Highest points-per-second in the match, but a spectator for 140 s. In a **Systemcore port year** score A7 pessimistically; this is the row most exposed to the control-system transition. |
| 10 | S2 | Fixed-position FUEL scorer | 73.2 | 35.5 | 56.2 | CHEAP INSURANCE | T2 STRETCH | A2 workstreams | V4 = 1: one surveyed shooting spot is exactly what a defender parks on. |
| 11 | S11 | ENERGIZED RP chaser | 57.5 | 41.7 | 50.4 | DELETE | T2 STRETCH | A4 drive practice | Chases the RP that triples at DCMP. Right at Week 1, wrong in April. |
| 12 | S9 | ENDGAME anchor, TOP tier — L3 telescoping | 39.6 | 57.9 | 47.9 | TRAP | **T4 GATED** | **G1: needs `CNC`** | Nets the same +5 as L2 (§2.3) for a machine you do not own. The definitive TRAP row. |
| 13 | S1 | Full-field FUEL volume cycler | 31.7 | 53.1 | 41.3 | DELETE | **T4 GATED** | **G2: 2 novel mechanisms + 2 new streams** | The idea the whiteboard produces in twenty minutes. It is a DELETE. |
| 14 | S13 | DO-EVERYTHING (swerve + turret + L3) | 4.9 | 70.0 | 34.2 | TRAP | **T4 GATED** | **G2: 4 novel mechanisms** | Recorded so it can be **rejected on the record**. `ARCH` I2: **0/5**. Highest value on the board, lowest achievability by a factor of eight. |

**Decision:** build **S10**, fall back to **S7**, and instruct the drive coach to play **S5** in any
match where a partner out-cycles us. S10 and S7 share a mechanism; S5 costs nothing.

---

## 4. Recommended design + BOM `[COMPUTED — results/bom.md]`

**Design:** KOP chassis + under-bumper roller intake feeding a hopper dump into the HUB from a
surveyed ALLIANCE ZONE position + **passive latch climber** for TOWER L1/L2.

| Gate | Status | Value | Limit |
|---|---|---|---|
| BUDGET | PASS | **$2,154.99** discretionary (gross $4,385.99 − KOP credit $2,231.00) | $2,500 |
| TOOLING FLOOR | PASS | bandsaw_drillpress | bandsaw_drillpress |
| BUILD HOURS | PASS | 91.0 h | 129.8 h |
| DESIGN HOURS | PASS | 36.0 h | 74.9 h |
| PROGRAMMING HOURS | PASS | 62.0 h | 134.8 h (already inflated ~40 h for the Systemcore port) |
| PARALLEL WORKSTREAMS | PASS | 3 effective (drivetrain, scoring, software; passive_latch_climber absorbed) | 3 |
| NOVEL MECHANISMS | PASS | 2 (under_bumper_intake, passive_latch_climber) | 2 |
| MOTOR COUNT | PASS | 7 motors / 7 controllers | 12 |

**VERDICT: ALL GATES PASS.**

**This required a descope.** The first BOM — intake + hopper + **winch** climber — **failed three
gates**: BUDGET $2,773.98, PARALLEL WORKSTREAMS 4, NOVEL MECHANISMS 3. Dropping the separate hopper
and swapping the winch for a passive latch cleared all three. **The gate model will not let this
team build a scoring mechanism and an active climber in the same season.** That is not a bug; it is
the model telling the truth about 15 students.

### Order schedule (counted back from kickoff 2027-01-09)

| Order by | Item | Lead | Stockout risk |
|---|---|---|---|
| **2026-11-21** | **baseline_electrical_package** (incl. Systemcore) | **6 wk** | **HIGH** |
| 2026-12-19 | bumpers_frame · under_bumper_intake · passive_latch_climber | 2 wk | low |
| 2027-01-02 | kop_chassis | 0 wk | low |

**EARLIEST ORDER-BY: 2026-11-21** — the same date `CLAUDE.md` lists as the project's BOM order-by,
and **seven weeks before kickoff**. The Systemcore line is the only high-stockout item and it must
be on a PO before anyone has seen the game. Price is `UNVERIFIED` (~$450 placeholder).

---

## 5. Two awards per strategy `[VERIFIED reference/awards/00_AWARD_LIST_VERIFIED.md]`

Names used are the verified current ones. **Dean's List is retired → FIRST Leadership Award.
Chairman's → FIRST Impact Award.**

| Strategy | Award 1 | Award 2 | Materials checklist | Who builds it |
|---|---|---|---|---|
| **S10** TRAVERSAL specialist | **Excellence in Engineering Award sponsored by Littelfuse** | **Quality Award** | Climb-reliability log (attempts/successes per match), the §2.3 break-even table showing L2 = L3, tolerance stack on the latch | Two students + the engineering notebook lead; pit interview, no pre-submission |
| **S7** L1 endgame anchor | **Quality Award** | **Industrial Design Award** | Passive-latch drawing set, "why no motor" one-pager, failure-mode table | One student; 4 h of prep |
| **S6** simple-and-flawless | **Gracious Professionalism Award** | **Team Spirit Award** | Match-uptime record, help-log of other teams assisted in the pits | Whole team; costs zero build hours |
| **S5** feeder/support | **Gracious Professionalism Award** | **Judges Award** | Alliance-partner testimonials, before/after partner cycle rates | Drive coach + scouting lead |
| **S3** AUTO-only | **Autonomous Award sponsored by Google.org** | **Innovation in Control Award sponsored by nVent** | AUTO path video, Systemcore migration writeup (**AI use must be attributed — `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`; judges may not rank you lower for it**) | Both programmers |
| Any (team-level, run in parallel) | **FIRST Impact Award** — pre-submission **2027-02-11** | **FIRST Leadership Award** — pre-submission **2027-02-04** | Essay + exec summary + 12-min interview script; Leadership is a student submission | Non-build students, starting week 1 — these are the only awards with hard deadlines before your event |

**Note the leverage:** FIRST Leadership Award is offered at 192 events with a **2.08 awards-per-event**
rate — the highest availability on the board — and it is decided by submission, not by the robot.

---

## 6. Loopholes and edge cases

**The highest-value section.** Worked from the BRIEFING_PACK's undefined ALL-CAPS list, the 12
game-specific rules, `RULE-CHURN-WATCHLIST.md`, and `QA-AMBIGUITY-HOTSPOTS.md`.

### 6.1 The 3-second assessment tail — the best exploit in REBUILT `[VERIFIED §6.5, p.45]`

> "Assessment of FUEL scored in the HUB continues for **3 seconds after the HUB deactivates** to
> account for FUEL processing time."

FUEL in flight or in the sensor array when your HUB switches off **still scores**. There are four
SHIFT boundaries plus the AUTO→TELEOP and SHIFT4→ENDGAME transitions. A team that deliberately
launches a full hopper into the final second of an active shift harvests up to **3 extra seconds of
scoring per boundary**. At 1 pt/s of active time that is **up to ~9–12 free points per match**, or
**~110–140 points over a 12-match schedule** — comparable to shaving a full second off cycle time,
for zero hardware. It is explicitly sanctioned by the rule text. **File a Q&A anyway** (§8 Q1) to
confirm the tail applies at every shift boundary and not only at 0:00, because the rule's stated
*reason* (processing time) applies everywhere but its stated *scope* lists only AUTO and TELEOP end.

### 6.2 Undefined ALL-CAPS — morphological variants of defined terms

§1.6 promises ALL CAPS = a glossary term. These are used in scoring and penalty rules and are
**not** in the glossary `[VERIFIED BRIEFING_PACK]`:

| Token | Where it bites | The argument |
|---|---|---|
| **CONTROLLED** (3×, p.65) | G408's FUEL rule: *"until that FUEL contacts anything else besides that ROBOT or FUEL CONTROLLED by that ROBOT"* | The glossary defines **CONTROL** (a state), not **CONTROLLED** (a past participle applied to a *pile*). Is a hopper of 25 FUEL one CONTROLLED mass or 25 CONTROLLED objects? G408's violations are "per instance and not per FUEL CONTROLLED" — the rule text itself has to disclaim the ambiguity. |
| **PINNING / PINNED** (5×, p.72) | G418's 3-count | G418 defines PINNING inline (*"preventing the movement of an opponent ROBOT by contact"*) but the term is not glossary-defined and G418-C uses **PINNED** — a different grammatical object. Whether a pinner who is himself pinned resets the count is decided by a participle. |
| **REPEATEDLY** vs **REPEATED** | G409-E (bumpers leaving the BUMPER ZONE), G415/G416 examples | REPEATED **is** defined (*"more than once within a MATCH"*). REPEATEDLY is not. If they are the same word the definition should be used; if they are not, G409's DISABLED penalty has no threshold. |
| **MOMENTARILY** vs **MOMENTARY** | G413's expansion exceptions (p.68) | MOMENTARY **is** defined (<~3 s). MOMENTARILY is not. G413's blue box then invents a *third* tier — "**less than** MOMENTARY" — and says such an action carries no penalty. **A rule whose exception is graded on an undefined adverb is where the season's expansion arguments will be won.** |
| **DISABLE** vs **DISABLED** (p.29) | AUTO rules | DISABLED is a defined state; DISABLE as a verb applied to an opponent is not. |

### 6.3 Game-specific rules with no REBUILT analogue

All 12 blue-headline rules are new-for-2026: G403, G407, G408, G413, G414, G420, G427, R104–R108.
**Five of them are on the `RULE-CHURN-WATCHLIST` predicted-contentious list — G413, R106, G403,
G420, G427 — a 5-for-5 hit.** `[COMPUTED]` The watchlist's predictions are good; use it.

- **G427 (OUTPOST storage limit)** — MINOR FOUL, MAJOR if CONTINUOUS. The only rule in the game
  that caps a *resource*, and the cheapest one to violate. See §6.5.
- **G420 (TOWER protection)** — the only rule whose violation *awards* points to the opponent.
- **G414 (don't climb on each other)** — penalty is not a foul at all: *"Supported ROBOTS become
  ineligible for TOWER points for the remainder of the MATCH."* Note it punishes the **supported**
  robot. A robot that climbs onto a partner's climber costs its partner nothing and itself
  everything — but a **defender** who wedges under an opponent mid-climb may make the opponent
  "supported." **File this** (§8 Q2).
- **R105/R106/R107/R108** — four separate extension rules where 2025 had fewer. R106
  ("one direction at a time") is the `QA-AMBIGUITY-HOTSPOTS` prediction and is the rule G413's
  never-stable exception ladder hangs off.

### 6.4 Bumpers (R4xx) and contact (G41x) — the historic core

`QA-AMBIGUITY-HOTSPOTS.md` predicts these carry the Q&A load, and REBUILT confirms the shape:
G415/G416/G417 all hinge on *"unable to drive"*, defined only as **"approximately ~20+ seconds"**
and **"generally"** — a referee-perception standard with a hedge word in the definition itself.
G409-E hinges on BUMPERS leaving the BUMPER ZONE **REPEATEDLY** (undefined, §6.2). These are the
`RULE-CHURN-WATCHLIST` never-stable slots G415, G416, G409, G211 — **4 for 4.**

### 6.5 Penalty-arbitrage audit — is the penalty cheaper than the points?

MINOR FOUL = **5** points to the opponent. MAJOR FOUL = **15**. `[VERIFIED Table 6-6, p.48]`

| Rule | Penalty | Points denied / gained | Arbitrage? |
|---|---|---|---|
| **G427** OUTPOST storage limit | **MINOR (5)**, MAJOR if CONTINUOUS | Overfilling the OUTPOST to starve the opponent's CHUTE for a 25 s shift denies up to ~25 FUEL | **YES — the clearest arbitrage in the game.** 5 points buys a >10-second denial of a resource worth 1 pt/s. Escalation to MAJOR only at CONTINUOUS (>~10 s) makes the first 10 seconds cost 5 points. |
| **G408** don't catch FUEL | MINOR (5); MAJOR (15) + warning **if strategic** | Intercepting a burst near the HUB | **Marginal.** Priced at 5 if it looks accidental, 15 if it looks deliberate. FIRST clearly saw this coming and put the intent test in. |
| **G418** PIN 3-count | MINOR (5), then MAJOR every 3 s | A 3 s pin of a scorer during their active shift denies ~3 FUEL | **Break-even at 3 s, ruinous after.** A 15 s pin costs 5 + 6×15 = **95 points** to deny ~15. Correctly priced. |
| **G420** TOWER protection | MAJOR (15) **+ opponent awarded LEVEL 3 (30)** = **45** | Denying a climb worth at most 30 | **NO.** The only rule in the manual that prices its own violation *above* the maximum gain. Model rule design. |
| **G407** score only in your ALLIANCE ZONE | MAJOR (15) | Would need 16 FUEL per violation to pay | **NO.** |
| **G403** limited AUTO opponent interaction | MAJOR **per instance of contact** | Denying an AUTO L1 climb (15) | **NO** — per-instance stacking makes a single AUTO ram cost ≥15 and usually more. |

**The cross-cutting arbitrage nobody will notice:** foul points credit the **opponent's MATCH point
total**, but the BONUS RPs count **FUEL scored** (ENERGIZED, SUPERCHARGED) and **TOWER points**
(TRAVERSAL) — *not* match points. **Fouling an opponent therefore never advances their bonus RPs.**
And the first ranking tiebreak explicitly excludes fouls (§6.5.3). So the true cost of a foul is
lower than the sticker price in every context except winning the match itself. Combined with G427's
5-point ceiling, **a disciplined foul-and-deny strategy is under-priced in REBUILT** — which is
exactly why G206 exists (*"ineligible for the BONUS RPs"*) and why G210/G211 are the referee's
catch-all. Expect a Team Update.

---

## 7. Pitfalls — what *this* team specifically will get wrong

1. **Quoting the raw cycle number.** 143 vs 93. Someone will design to the whiteboard number and be
   50% over on expected score all season. The duty cycle is invisible unless you read Table 6-3.
2. **Building for L3.** It is the tallest thing on the field and it is worth **the same net +5 as
   L2** (§2.3). Fifteen students will vote for L3 and the vote will be wrong.
3. **Skipping the AUTO L1 climb.** It pays **15** — more than L2's net gain — and is capped at 2
   robots per alliance, so it is also a *scarce* action worth claiming early in alliance strategy.
4. **Chasing ENERGIZED.** It triples at DCMP. TRAVERSAL never moves. The team will chase the
   FUEL number because it is the one on the big screen.
5. **Proposing the do-everything robot (S13).** ACH 4.9/100. It is in this document specifically so
   it can be rejected with a number instead of an argument.
6. **Not proposing S5, S4, or S12.** The three highest-achievability rows are the three archetypes
   no student proposes. The corpus says feeder/support is **5/5** and defense **3/4** for small teams.
7. **Under-costing the Systemcore port.** The programming line is already inflated ~40 h and it
   still passed with 72 h to spare — but only because the recommended design has a *passive*
   climber. Any closed-loop mechanism eats that margin. **Never invest training time in roboRIO.**
8. **Missing 2026-11-21.** The electrical package must be ordered **seven weeks before kickoff**,
   before anyone has seen the game. This is the single date on which the whole plan can fail
   silently.
9. **Letting the two award submissions slip.** FIRST Leadership **2027-02-04** and FIRST Impact
   **2027-02-11** are hard deadlines that arrive during peak build. They need non-build students
   assigned in week 1.

---

## 8. Q&A questions to file in week 1, ranked by leverage

Early questions get answered fastest and the answers are binding.

1. **Does the 3-second FUEL assessment tail (§6.5) apply at every SHIFT boundary, or only at the
   end of AUTO and TELEOP?** — Highest leverage in the document. Worth ~110–140 points per season
   for zero hardware, and the rule's scope list and its stated rationale disagree.
2. **G414: if an opponent defender causes our ROBOT to be "supported" during a climb, do we lose
   TOWER eligibility?** — The penalty falls on the supported robot. If the answer is yes, G414 is a
   free denial tool and TRAVERSAL is not safe.
3. **G427: what is the OUTPOST storage limit numerically, and when does "CONTINUOUS" start
   counting?** — This is the §6.5 arbitrage. A number turns it from a strategy into a foul.
4. **G413: is "less than MOMENTARY" a defined duration?** — The exception ladder that decides every
   expansion argument this season hangs on an undefined adverb.
5. **G408: is a hopper of N FUEL one instance of CONTROL or N?** — Determines whether a bulk-dump
   robot risks one MINOR or twenty-five.
6. **Does FMS Game Data publish the SHIFT schedule before the match, or only at TELEOP start?** —
   Determines whether AUTO strategy can be conditioned on the resulting HUB order.
7. **G409-E: does "REPEATEDLY" carry the glossary definition of REPEATED (>1 per MATCH)?** — If yes,
   two bumper excursions in one match is a DISABLED.
8. **Are TOWER points assessed if the human volunteer's view is obstructed by a partner ROBOT?** —
   §6.5.2 permits contacting another ROBOT; §6.5 says TOWER is human-judged. Those two combine badly.

---

## 9. Scored betting sheet `[research/04_biocore_community_intel.md]`

**This section cannot be scored honestly in a rehearsal.** The 11 predictions are about **BIOCORE**;
the manual under test is **REBUILT**. Scoring them against REBUILT would be scoring the answer key
against the wrong exam. What follows is instead **what each prediction would look like if REBUILT
were the target** — a calibration check on the *shape* of the predictions, not their truth.

| # | Prediction | Against REBUILT | Note |
|---|---|---|---|
| P1 | Element is not a ≤3.5 in sphere | **Would FAIL** — FUEL is a ball | Correctly flagged as contradicting the task brief's premise |
| P2 | <150 elements on the field; 36–90 | **Would FAIL** — REBUILT's field is ~500 FUEL (2/6 field = 168) | Load-bearing by the author's own admission |
| P3 | Holding limit is 2–4 | **Would FAIL** — REBUILT is *uncapped* ("may control any amount") | The G427 OUTPOST limit is a *field* storage cap, not a robot one — a distinction the prediction does not make |
| P4 | Placement economy, not flywheel launching | **Would FAIL** — REBUILT is a shooter game | |
| P5 | ≥3 scoring locations of differing value | **Partial** — one FUEL value, but 3 TOWER LEVELs | The gradient landed in the *endgame*, not the cycle |
| P6 | Endgame is a multi-tier climb worth ≥15% of a winning score | **HIT, precisely** — 3-tier TOWER climb; 50 TRAVERSAL / ~150 typical = **~20–33%** | The strongest prediction on the sheet |
| P7 | 2–3 objective RPs + Win/Tie, ≥1 volume threshold | **HIT, exactly** — ENERGIZED + SUPERCHARGED + TRAVERSAL, two of them volume thresholds | |
| P8 | Element is neutral, not alliance-coloured | **HIT** — FUEL is neutral | |
| P9 | Rigid/semi-rigid moulded plastic | **Partial** — FUEL is a compliant ball; author already flagged this as a coin flip | Self-assessed as the most likely miss; that self-assessment is correct |
| P10 | Explicit numeric CONTROL rule, top-5 foul source, definitional loopholes around "control"/"herding" | **Structurally HIT** — G408 is exactly this rule, complete with a "bulldozing" herding exception and a per-instance disclaimer, though the cap is not numeric | **The single most useful prediction in the file.** It named the loophole class before the manual existed, and §6.2 found it. |
| P11 | Nesting/stackable geometry | **Would FAIL** — spheres | Newest and least evidenced |

**Calibration read `[COMPUTED]`:** the predictions about **game structure** (P6, P7, P8, P10 — and
P5 in shape) are 4–5 hits out of 5. The predictions about **element physics** (P1, P2, P3, P9, P11)
would all miss, and they are the ones chained off AndyMark pricing and shipping arithmetic.

**What the misses imply:** the shipping/price inference chain is the weakest instrument in the
project and everything downstream of P2 should be treated as decoration, not input. The
**structural** priors — RP shape, endgame shape, control-rule shape — are drawn from 11 seasons of
manual inventory on disk and they are the ones that hold. On kickoff day, **trust the structural
priors and re-derive every physical number from the manual.** Note also that the author's own
confidence ordering was right: P9 was self-flagged as a coin flip and would indeed miss.

---

*Evidence tags per `CLAUDE.md`. Every REBUILT fact carries a page or table citation. Every model
output is reproducible from `results/`. Nothing here is a fact about BIOCORE.*
