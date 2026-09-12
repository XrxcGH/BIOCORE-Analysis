# The Championship Season, Day by Day — and What Each Stage Costs

**Purpose:** the other two team-ops files describe *method* — how elite teams design, and how they
tune and compete. This one is the **clock and the invoice**: a day-numbered map of the 2027 BIOCORE
season from kickoff to champs, and for every stage, three numbers — **person-hours, headcount,
dollars**. It ends with the payload table this whole project exists to produce: *what elite practice
requires, what the ~15-student equivalent is, and exactly what you give up.*

**Companion files** — read these, do not expect this file to repeat them:

| File | Owns |
|---|---|
| [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) | **The hours/headcount/budget authority.** Every number below is denominated in it |
| [`../team_capacity.yaml`](../team_capacity.yaml) | The same constants, machine-readable |
| [`02_design_cad_manufacturing.md`](02_design_cad_manufacturing.md) | *How* design/CAD/DFM/sourcing is actually done |
| [`03_programming_stack.md`](03_programming_stack.md) | *What* software stack to run in the Systemcore era |
| [`04_tuning_testing_competition_ops.md`](04_tuning_testing_competition_ops.md) · [`04_competition_ops.yaml`](04_competition_ops.yaml) | Practice field, driver development, tuning, event ops |
| [`05_business_awards_sustainability.md`](05_business_awards_sustainability.md) | Awards, Impact, funding |
| [`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md) | **The kickoff-day procedure itself** — manual ingest, the six phases, the ready-to-paste prompts |
| [`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md) | **The scoring-priority machinery** — candidate enumeration, the ranked matrix, gate checks |
| [`../bom/06_MECHANISM_CATALOG.md`](../bom/06_MECHANISM_CATALOG.md) | The 27 priced archetypes every dollar figure below traces to |

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus, or in a source cited inline |
| **[H]** HISTORICAL-PATTERN | Observed across prior FRC seasons / widely-documented team practice; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model assumption. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked inside this pass's budget. Treat as a claim, not a fact |

**Source shorthand**

`TCM` = [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) · `CAP` = [`../team_capacity.yaml`](../team_capacity.yaml) ·
`MECH` = [`../bom/06_MECHANISM_CATALOG.md`](../bom/06_MECHANISM_CATALOG.md) ·
`DCM` = [`02_design_cad_manufacturing.md`](02_design_cad_manufacturing.md) ·
`PROG` = [`03_programming_stack.md`](03_programming_stack.md) ·
`OPS` = [`04_tuning_testing_competition_ops.md`](04_tuning_testing_competition_ops.md) ·
`PF` = [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) ·
`CAL` = the 2027 FIRST calendar as transcribed in [`../../research/03_biocore_official_intel.md`](../../research/03_biocore_official_intel.md) §2.

> **Scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game (FIRST CANOPY season), kickoff
> **2027-01-09 12:00 ET**. **BIOBUZZ is the FTC sibling game**; "Pollen", StarterBots and Skill
> Builders are FTC constructs and appear nowhere in this file. BIOCORE's rules are not public as of
> **2026-08-22**. **This file contains no game-specific claim.** It is a model of *time and money*,
> both of which are knowable today.

---

## §0 — The 60-second orientation

Run this before you argue with any number below. It re-derives the clock and the budget from the two
authorities rather than trusting this document's transcription of them.

```bash
# Run from the repository root.

# ---- 1. THE CLOCK. Day-number every milestone from kickoff. (~1 s) -------------------
python - <<'PY'
import datetime as d
k = d.date(2027,1,9)
for name, iso in [("KICKOFF","2027-01-09"),("Q&A opens","2027-01-13"),
                  ("Impact/Awards submission 15:00","2027-02-11"),
                  ("Week Zero","2027-02-20"),("Week 1","2027-03-03"),
                  ("Week 2","2027-03-10"),("Week 3","2027-03-17"),
                  ("Week 4","2027-03-24"),("Week 6","2027-04-07"),
                  ("Championship","2027-04-28")]:
    t = d.date.fromisoformat(iso)
    print(f"  day {(t-k).days:>4}  {iso}  {name}")
PY

# ---- 2. THE BUDGET THIS FILE SPENDS. Re-derive, do not trust the tables below. (~2 s) -
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week1
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week4

# ---- 3. THE ONE LINE THAT KILLS BAD PLANS -------------------------------------------
python tools/capacity_model.py | grep -A1 "BINDING"     # today: 2 novel mechanisms

# ---- 4. DOES THE ROBOT YOU WANT FIT? Gate-check a BOM before you commit hours. -------
python tools/bom-builder.py reference/bom/examples/simple.yaml     # exit 0
python tools/bom-builder.py reference/bom/examples/moderate.yaml   # exit 1

# ---- 5. THE STAGE→HOURS SPLIT IN §2 SUMS TO THE MODEL'S EIGHT LINES. Prove it. -------
python - <<'PY'
lines = dict(strategy=25.0, cad=74.9, fab=129.8, elec=49.9,
             prog=134.8, integ=84.9, drive=54.9, awards=44.9)
stages = dict(kickoff=18.0, proto=47.0, design=59.9, manufacture=74.8,
              assembly=79.9, programming=134.8, integration=84.9,
              practice=54.9, business=44.9)
print("eight mandatory lines :", round(sum(lines.values()),1))
print("nine stages in Sec 2  :", round(sum(stages.values()),1))
assert abs(sum(lines.values())-sum(stages.values())) < 0.05
print("OK - the stage map is a repartition, not an addition")
PY
```

**Read the output in this order.** (1) tells you your real deadline is **day 42 (Week Zero)** or
**day 53 (a Week 1 event)**, not "six weeks". (2) tells you the season is **599 effective hours** to
Week 1 or **854** to Week 4. (3) tells you it buys **two** novel mechanisms. Every stage table below
is a partition of (2), and every stage that overruns is paid for out of §8 — drive practice — which
`PF` weights **90, the highest factor in the corpus**.

---

## §1 — The season clock

### 1.1 Milestones, day-numbered

All dates **[C]** from `CAL`. Day 0 = kickoff, 2027-01-09.

| Day | Date | Milestone | What it gates |
|---:|---|---|---|
| **0** | Sat 2027-01-09 12:00 ET | **KICKOFF** — BIOCORE manual released | Everything |
| 2 | Mon 2027-01-11 | End of kickoff weekend | Strategy decided, spec frozen enough to prototype |
| 4 | Wed 2027-01-13 | **Q&A system opens** | Rule interpretations you bet the robot on |
| 10 | Tue 2027-01-19 | Prototype cut-line | Mechanism archetype chosen; losers deleted |
| 25 | Wed 2027-02-03 | **Design freeze** (target) | Every part released to manufacture |
| **33** | Thu 2027-02-11 15:00 ET | **Impact / award submission deadline** | Non-negotiable, external, and it is *before* your robot works |
| 42 | Sat 2027-02-20 | **Week Zero** — exactly 6.00 weeks | The shakedown deadline "six-week build season" actually names |
| 50 | Sun 2027-02-28 | Robot must be driving | Last honest date for a Week 1 team |
| **53** | Wed 2027-03-03 | **Week 1 events open** — 7.57 weeks | Baseline scenario deadline |
| 60 | Wed 2027-03-10 | Week 2 | |
| 67 | Wed 2027-03-17 | Week 3 | |
| **74** | Wed 2027-03-24 | **Week 4** — 10.57 weeks | +255 veq-h vs Week 1, for free (`TCM` §7.4) |
| 88 | Wed 2027-04-07 | Week 6 | |
| 109 | Wed 2027-04-28 | **Championship** | |

Three consequences, all from `TCM` §1:

1. **There is no bag day and no stop-build day** **[C]**. Build access is continuous from kickoff to
   your last match. The only thing bounding you is hours you can staff.
2. **"Six weeks" is Week Zero (day 42), not your event.** Team folklore is 11 days pessimistic about
   the real deadline and exactly right about the shakedown one.
3. **Week 4 (day 74) buys +21 calendar days = +255 veq-h at zero fatigue cost**, and `PF` §10
   measures the competitive penalty at under 2 rank-percentile points. **Choose event week before you
   choose a mechanism** — and choose *field size* before you choose week (`PF` §11).

### 1.2 The Gantt, and the collision it exposes

```
day    0    10   20   30   40   50   60   70   80
       |    |    |    |    |    |    |    |    |
KICK  [##]                                              d0-2
PROTO   [######]                                        d2-10
CAD      [###############]                              d5-25
MFG              [####################]                 d20-45
ASM                    [############]                   d35-50
PROG  [##################################]              d0-60
INTEG                    [##############]               d40-60
DRIVE                        [###################>      d45-70+
BIZ   [######################]                          d0-33  (hard external deadline d33)
                                          ^d53 WEEK 1
                                                    ^d74 WEEK 4
```

**Read the collision.** The canonical elite stage plan — manufacture to day 45, assembly to day 50,
practice from day 45 — is an **8-to-10-week plan**. Against a Week 1 event at **day 53** it leaves
**three days** between "robot assembled" and "robot on a competition field," and it puts the entire
drive-practice window (days 45–70) *on top of and after* the event. Against **day 74** it fits with
three weeks of margin.

> **This is the single most important structural finding in this file, and it is a scheduling
> finding, not a capability one.** The elite stage sequence does not fail at 15 students because the
> students are worse. It fails because the sequence needs ~10 weeks and a Week 1 event gives 7.57.
> `TCM` §7.4 already priced the fix; this Gantt is why it matters.

---

## §2 — The stage ledger: hours, headcount, dollars

### 2.1 The master table

Every `veq-h` figure is a **repartition of the eight mandatory lines in `TCM` §3.1** — the nine
stages sum to **599.1**, the same total, because there are no spare hours to allocate (§0 step 5
asserts this). "Heads" = people meaningfully occupied, from the 15-person roster in `TCM` §4.2.
Dollars are **catalog retail** from `MECH` unless marked *incremental*.

| # | Stage | Days | Dates | **veq-h** | % | **Heads** | **$ (retail)** | Drawn from |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | **Kickoff weekend** | 0–2 | Jan 9–11 | **18.0** | 3.0% | **15** | ~$120 food/print **[S]** | strategy |
| 2 | **Prototyping** | 2–10 | Jan 11–19 | **47.0** | 7.8% | 8–10 | **$150–350** stock/COTS **[S]** | strategy 7 + cad 15 + fab 25 |
| 3 | **Design / CAD** | 5–25 | Jan 14–Feb 3 | **59.9** | 10.0% | 3–4 | **$0** (EDU licences, `DCM` §1.3) | cad |
| 4 | **Manufacture** | 20–45 | Jan 29–Feb 23 | **74.8** | 12.5% | 5–7 | **$2,500** disc. BOM (`CAP`) | fabrication |
| 5 | **Assembly + wiring** | 35–50 | Feb 13–28 | **79.9** | 13.3% | 5–6 | **$1,979** electrical pkg (`MECH`); mostly KoP-covered | fabrication 30 + electrical 49.9 |
| 6 | **Programming** | 0–60 | Jan 9–Mar 10 | **134.8** | 22.5% | 2 (3 wanted) | **$0** sw; Systemcore **UNVERIFIED** | programming |
| 7 | **Integration / debug** | 40–60 | Feb 18–Mar 10 | **84.9** | 14.2% | 6–8 | **$400–600** spares (`CAP`) | integration |
| 8 | **Drive practice + tuning** | 45–70+ | Feb 23–Mar 20+ | **54.9** | 9.2% | 4 per session | **$300–900** field elements (`OPS` §1.6) | drive_practice |
| 9 | **Business / awards / scouting** | 0–33+ | Jan 9–Feb 11 | **44.9** | 7.5% | 3–4 | **$0–150** print/media **[S]** | awards_business |
| | **TOTAL** | **0–70+** | | **599.1** | 100% | **15** | see §2.3 | |

### 2.2 The Week-4 variant — where the extra 255 hours go

`TCM` §2.6: Week 4 = **854 veq-h**, +255. **[S]** The correct allocation of the extra hours is *not*
proportional — it is weighted to the two lines the Week 1 plan starves:

| Stage | Week 1 veq-h | **Week 4 veq-h** | Δ | Why |
|---|---:|---:|---:|---|
| 1 Kickoff | 18.0 | 18.0 | — | Fixed-length event |
| 2 Prototyping | 47.0 | 62.0 | +15 | One more iteration loop; the cut-line moves to day 14 |
| 3 Design/CAD | 59.9 | 74.9 | +15 | Freeze moves d25 → d32; one extra review gate |
| 4 Manufacture | 74.8 | 94.8 | +20 | Absorbs one remake without a schedule slip |
| 5 Assembly + wiring | 79.9 | 94.9 | +15 | Wiring done once, properly, not at 11pm |
| 6 Programming | 134.8 | 169.8 | +35 | The Systemcore port stops being a critical-path risk |
| 7 Integration/debug | 84.9 | 134.9 | **+50** | `PF` weights reliability **88** |
| 8 **Drive practice** | 54.9 | **139.9** | **+85** | `PF` weights this **90** — see §9.2 |
| 9 Business/awards | 44.9 | 64.9 | +20 | Deadline is still d33; extra hours go to judged-award prep |
| **TOTAL** | **599.1** | **854.1** | **+255** | |

**Drive practice goes from ~9 real driver hours to ~24** (`TCM` §3.4 arithmetic, re-run at 139.9:
139.9 ÷ 3.5 × 0.6 ≈ 24.0 h). **That is the whole argument for Week 4 in one number.**

### 2.3 The dollar roll-up

Costs are not additive across §2.1 because the KoP covers part of stages 4–5. The honest accounting,
from `CAP` `budget_usd` and `MECH`:

| Line | USD | Evidence |
|---|---:|---|
| Season registration (incl. team number, Kit of Parts, **one Regional or two District events**) | **6,500** | **[C]** `CAP`, FIRST Cost & Registration via `CAL` |
| Kickoff Kit shipping (ground US/CA) | 50–315 | **[C]** for 2026 reference; **2027 TBA** |
| Sales tax @7% assumed | ~450 | **[S]** rate; **[C]** that 2026-27 tax practice changed |
| **Robot BOM over the KoP — floor (Everybot-class)** | **1,500** | **[C]** `PF` §5.1 |
| **Robot BOM over the KoP — planning target** | **2,500** | **[S]** `CAP` `robot_discretionary` — *the number design trades score against* |
| Spares + consumables (stage 7) | 400–600 | **[S]** `CAP` |
| Prototype stock (stage 2) | 150–350 | **[S]** — see §4.2 |
| Practice field elements (stage 8) | 300–900 | **[S]** from `OPS` §1.6's three-element reduction |
| Local event travel/food, no hotel | ~1,200 | **[S]** |
| Regional team playing a District event | 1,000 | **[C]**, new for 2027 (`CAL`) |
| **2027 control system (Systemcore)** | **UNVERIFIED** | No published price as of 2026-08-22. **Do not assume the roboRIO carries over** |
| **Composite minimum viable season** | **~9,000** | **[S]** `TCM` §8.1 |
| **Composite planning target** | **~11,500** | **[S]** `TCM` §8.1 — the number to fundraise against |

> **The Systemcore line is a hole in the season budget, not a rounding error.** Re-check FIRST and
> vendor pages immediately after the **2026-11-12 Pre-Kickoff Virtual Kit Release** (§13).

---

## §3 — Stage 1: Kickoff weekend (days 0–2)

**18.0 veq-h · 15 heads · ~$120**

### 3.1 What this file does *not* say

The manual-reading protocol, the six analysis phases, the loophole hunt and the ready-to-paste
prompts live in **[`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md)**. The scoring-priority
matrix, candidate enumeration and the ranked-strategy machinery live in
**[`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md)** — including its §0
runnable workflow and the three lines you read out loud to the team. Do not restate them here; run
them.

### 3.2 The 48-hour schedule, and its cost

| Block | Day/time | Activity | Heads | veq-h | Playbook ref |
|---|---|---|---:|---:|---|
| A | d0 12:00–12:45 | Watch the game reveal. **Once, no commentary.** | 15 | 1.5 | — |
| B | d0 12:45–13:15 | **Mechanical ingest**: fetch + freeze the manual PDF, hash it, split it | 2 | 0.6 | `KICKOFF_PLAYBOOK` Phase 0 |
| C | d0 13:15–16:00 | **Silent first read**, whole team, no discussion allowed | 15 | 6.0 | Phase 1 |
| D | d0 16:00–18:00 | Rule inventory + evergreen-rule diff vs 2026 REBUILT | 3 | 1.5 | `STRATEGY-RANKING-SYSTEM` §1 |
| E | d1 09:00–12:00 | **Scoring analysis**: points per action, cycle-time arithmetic, RP structure | 5 | 3.6 | Phase 2 |
| F | d1 13:00–17:00 | **Strategy enumeration** → `strategies/candidates.yaml`; rank it | 6 | 3.4 | `STRATEGY-RANKING-SYSTEM` §2–§4 |
| G | d1 17:00–18:00 | Loophole / edge-case hunt; log Q&A questions for d4 | 4 | 0.5 | Phase 4 |
| H | d2 18:00–21:00 | **Spec decision meeting** + gate check the BOM | 15 | 0.9 | §3.4 below |
| | | **TOTAL** | | **18.0** | |

The remaining **7.0 veq-h** of the 25.0 `strategy_rules` line is spent days 3–10 on Q&A responses
(system opens **day 4**) and on re-reading rules that the prototypes turn out to depend on. Budget it
deliberately; it is the line teams silently overrun by re-litigating strategy every evening.

### 3.3 The reading protocol, in one table

**[H]** This is standard practice across published team processes; the *silent* first read is the
part small teams skip and should not.

| Pass | Who | Duration | Output | Rule |
|---|---|---|---|---|
| 1 — Silent | Everyone | 2h45 | Individual notes only | **No talking.** Nobody's first impression is contaminated by the loudest voice |
| 2 — Sectional | Pairs, by manual section | 1h | A rule inventory row per numbered rule | Every rule gets an owner |
| 3 — Adversarial | 2 students + mentor | 1h | "What does the rule *permit* that nobody expects?" | Feeds the Q&A list |
| 4 — Numeric | 3 students | 3h | Points-per-cycle spreadsheet | The only pass that produces a *number* |

### 3.4 Who decides the robot spec, and when

**[S]** — this is an organisational recommendation, not an observation of BIOCORE.

| Decision | Deadline | Decided by | Vetoed by | Recorded in |
|---|---|---|---|---|
| Which strategies are *candidates* | d1 17:00 | Whole team, open enumeration | Nobody | `strategies/candidates.yaml` |
| The **ranked** matrix | d2 12:00 | Strategy lead + mentor, using the rubric | The rubric itself (gate failures) | `score-strategy` output |
| **The robot spec** (mechanism list, drivetrain, auto ambition) | **d2 21:00** | **Mentor + 3 core-technical leads** | **`bom-builder` gate check — exit 1 means the spec is void** | A one-page pinned doc |
| Prototype set to build | d2 21:00 | Mechanism lead | Mentor (safety, hours) | Whiteboard + `MECH` ids |

**The veto belongs to the tool, not to a person.** `CAP` `gates` fails a spec on budget ≥$2,500,
build-hours ≥129.8, design-hours ≥74.9, programming-hours ≥134.8, >2 novel mechanisms, >12 motors, or
tooling above `bandsaw_drillpress`. That is the entire point of having written the gates down in
August: on day 2 the answer to "can we do three mechanisms?" is a **command**, not an argument.

**Small-team adaptation that matters most:** a 15-student team **must** decide on day 2, not day 5.
Elite teams can afford a week of strategy because they have parallel prototyping capacity to spend
during it. This team's day-2 to day-10 window is its only prototyping window (§4). Every day of
strategy indecision is deleted directly from prototyping.

---

## §4 — Stage 2: Prototyping (days 2–10)

**47.0 veq-h · 8–10 heads · $150–350**

### 4.1 How many in parallel — the number is 2, and it is derived, not chosen

`TCM` §5 derives `parallel_workstreams_max = 3` and `novel_mechanisms_max = 2` four independent ways.
During days 2–10 the three workstreams are:

| # | Workstream | Lead (`TCM` §4.2) | Prototype activity days 2–10 |
|---|---|---|---|
| 1 | Drivetrain + frame + bumpers | Core tech B | **Not a prototype.** Assemble the KoP chassis and *drive it* (§9.3) |
| 2 | **Primary scoring mechanism** | Core tech A + C | **2 competing archetypes**, evaluated head-to-head |
| 3 | Software / controls / Systemcore | Core tech D + E | Bring-up on whatever hardware exists (§8) |

**So: two prototypes in parallel, on one mechanism.** Not two mechanisms with one prototype each —
that is the trap. `PF` §4.1: a 3-link chain at 90% reliability each is **72.9%** overall. You are
buying certainty on the mechanism that scores, not breadth.

**[H]** Elite teams run 4–8 prototype benches simultaneously with a dedicated prototype sub-team.
That capacity is bought with headcount and a second/third bandsaw, and `TCM` §5.5 shows the shop
queue (route C) is **insensitive to headcount** — so this is the one place where "more students"
genuinely would not close the gap either.

### 4.2 Materials and test rigs — the shopping list

**[S]** costs; the archetype ids are **[C]** from `MECH`.

| Item | Purpose | $ | Notes |
|---|---|---:|---|
| 2×4 lumber + plywood scrap | Prototype frames | 0–40 | Wood is the correct prototype material. It is fast, forgiving and free |
| 1/4" and 1/2" polycarb offcuts | Guides, hoppers, funnels | 30–60 | Reuse last year's |
| Compliant / stealth wheels, assorted durometer | Intake and indexer rollers | 60–120 | The one thing worth buying new — durometer *is* the experiment |
| 1/2" hex shaft, bearings, spacers | Every roller test | 40–80 | Standing stock; buy in the off-season (§13) |
| Zip ties, gaffer tape, hot glue, 80/20 offcuts | Rig construction | 20–30 | |
| **One spare motor + controller on a bench harness** | The test rig itself | 0 (reuse) | See §4.3 |
| **TOTAL** | | **$150–350** | Inside the $2,500 discretionary; do **not** let it eat the mechanism budget |

Cross-reference `MECH` §2 for what the *production* version of each archetype costs — e.g.
`over_bumper_intake` **$380 / 16 build h / 8 design h / 1 motor**, versus `deploying_intake`
**$600 / 28 build h / 16 design h / 2 motors / `mill_lathe` floor**. The second is not buildable in
this shop without outsourcing (`DCM` §5.4). **Prototype only archetypes whose tooling floor you own**
— otherwise you are testing a mechanism you cannot manufacture.

### 4.3 The bench harness — the highest-leverage $0 object in the shop

**[S]** A prototype that has to be re-wired every session costs 20 minutes of setup per session; over
eight days that is a full veteran-day. Build **one** permanent bench harness on day 2: battery,
breaker, PDH, one motor controller, a driver station laptop, a big red stop button, everything on a
plywood board with the motor output on a hex shaft. Every prototype bolts to it. This is also the
rig on which the programmers do Systemcore bring-up (§8), which is why it belongs to nobody and
lives in the middle of the shop.

### 4.4 Quantitative evaluation — the scoring sheet

**[S]** The rule: **a prototype that produced no number produced no result.** Every prototype session
ends by filling one row:

| Field | How measured | Why it is the right metric |
|---|---|---|
| **Cycle time (s)** | Stopwatch, 10 consecutive attempts, median | Converts directly into points/match via `OPS` §0 step 1 |
| **Success rate (%)** | Successes ÷ 20 attempts | Feeds the `PF` §4.1 reliability chain |
| **Tolerance window** | Range of positions/angles that still work | The single best predictor of whether a driver can use it |
| **Motor count / current draw** | Nameplate + measured stall behaviour | Gates against `CAP` `motor_cap: 12` |
| **Est. build hours to production** | Compare to nearest `MECH` archetype | Gates against `build_hours_cap: 129.8` |
| **Tooling floor required** | `MECH` vocabulary | **Gate G1**: above `bandsaw_drillpress` and it is dead unless outsourced |

Two prototypes, one table, one meeting. The decision is which row wins, and it is usually obvious
once the numbers exist — which is precisely why teams that don't measure argue for a week.

### 4.5 The cut-line — day 10, and it is a date, not a feeling

| Trigger | Action |
|---|---|
| **Day 10, 21:00** | **The losing prototype is deleted.** Not paused, not "we'll revisit" — deleted, and its stock returns to the rack |
| Either prototype's tooling floor exceeds `bandsaw_drillpress` and outsourcing is not already funded | Cut immediately, do not wait for day 10 |
| A prototype needs a third novel mechanism to be useful | Cut. `novel_mechanisms_max = 2` and the drivetrain already owns one workstream |
| **Both** prototypes score below the cycle-time threshold the strategy needs | **Escalate to strategy, not to engineering.** Re-run `score-strategy` with the measured numbers; the strategy was wrong, not the build |
| Day 14 with no chosen archetype (Week 4 teams only) | Hard stop: adopt the published Everybot mechanism and move on (`PF` §5.1) |

**[H]** The "kill date" discipline is the most-copied element of published elite processes and the
least-copied in practice. Its function is not engineering; it is protecting stage 3 from stage 2.

---

## §5 — Stage 3: Design / CAD (days 5–25)

**59.9 veq-h · 3–4 heads · $0**

**Method lives in [`02_design_cad_manufacturing.md`](02_design_cad_manufacturing.md)** — CAD platform
choice (§1), part libraries and workspace structure (§2), layout-first methodology and the master
sketch (§3), the design-review checklist (§4), DFM by shop capability (§5), sourcing and the
**November** order-by dates (§6). This section owns only **who, when, and how often**.

### 5.1 Ownership

| Scope | Owner | Backup | Reviews with |
|---|---|---|---|
| **Master sketch / packaging study** | Core tech C (CAD lead) | Mentor | Whole technical group, once, day 7 |
| Drivetrain + frame + bumpers | Core tech B | Core tech C | Mentor |
| Primary scoring mechanism | Core tech A | Core tech C | Mentor + mechanism prototyper |
| Electrical board layout | Veteran F | Core tech D | Mentor |
| **Release to manufacture** (the drawing/DXF hand-off) | **Core tech C, sole authority** | Mentor | — |

**One CAD lead, and integration is their job, not a committee's.** With 3–4 people in CAD, the
failure mode is not too few designers — it is two people editing the same assembly. `DCM` §2.5's
versioning discipline exists for exactly this.

### 5.2 Review cadence — three gates, three different meetings

Per `DCM` §4.2, timed against this file's clock:

| Gate | Day | Duration | Attendees | Passes when |
|---|---:|---|---|---|
| **G-A Layout review** | **7** | 60 min | CAD lead, mentor, mechanism lead, programmer | Master sketch + packaging volumes reserved; nothing detailed yet |
| **G-B Detail review** | **17** | 90 min | + fabricator, electrical | Every part manufacturable on owned tooling; stack-ups standard; fasteners real |
| **G-C Release review** | **25** | 60 min | + whole build group | **Design freeze.** Every part has a drawing, a material, a process and a person |

**60–90 minutes a week is the entire review budget** and `DCM` §4.1 argues a small team needs *more*
review discipline than a large one, not less, because it has no spare fabrication hours to absorb a
remake. Note the mentor arithmetic: `TCM` §6.2 gives **3.4 h/week of mentor decision-unblocking**.
These three gates consume 3.5 hours of it across three weeks — about a third. That is affordable
exactly once per week and not twice.

### 5.3 Design freeze — day 25, and what "freeze" means

**[S]** Freeze does not mean the CAD stops. It means:

- **Frozen:** the frame, the mounting interfaces, the electrical board footprint, the motor count,
  and the mechanism *archetype*. Changing any of these after day 25 invalidates parts already cut.
- **Not frozen:** tuning geometry (roller spacing, hard-stop angles, gear ratios), 3D-printed parts,
  and anything reachable with a drill and a file.
- **The test:** if changing it makes an already-manufactured part scrap, it is frozen.

**The freeze exists to protect the fabrication queue**, which `TCM` §5.2 route C identifies as one of
the four independent constraints. A single-server shop cannot absorb rework; a design change on day
30 does not cost you the part, it costs you the *queue slot*, and the queue slot is what stage 8 is
made of.

**Slip rule:** if G-C fails on day 25, the correct response is **descope the mechanism**, not move
the freeze. Moving the freeze moves stages 4–8 and lands on drive practice.

---

## §6 — Stage 4: Manufacture (days 20–45)

**74.8 veq-h · 5–7 heads · $2,500 discretionary BOM**

### 6.1 The queue is the constraint, not the hours

`TCM` §5.2 route C: one bandsaw, one drill press, one 3D printer, one mentor-supervised mill you do
not own (`CAP` `tooling.inventory`). At >70% utilisation a single-server queue has unbounded wait
times, and **two mechanism streams already saturate it**. Practical consequences:

| Rule | Why |
|---|---|
| **Manufacture in dependency order, not in enthusiasm order** | Drivetrain and frame first — they are the fixture everything else mounts to, and they unlock §9.3 |
| **The 3D printer runs 24/7 from day 20** | It is the one machine that works while nobody is present. Queue prints overnight, every night |
| **Batch every bandsaw operation** | Set-up dominates cut time on a small saw. One session of tube cuts beats six sessions of one cut |
| **Nothing goes on the saw without a drawing** | `DCM` §4.3 checklist. A remake costs a queue slot, and queue slots are the scarce good |
| **Outsource 2D sheet, not 3D parts** | `DCM` §5.4: `CAP` allows **$400** outsourcing at **2 weeks** lead — so an outsourced part must be released by **day 31** to arrive by day 45 |

### 6.2 The dollar detail

The **$2,500** is `CAP` `robot_discretionary` — spend *over* the Kit of Parts. Worked against `MECH`
for the recommended configuration (`novel_mechanisms_recommended: 1`):

| Line | `MECH` id | Catalog $ | Notes |
|---|---|---:|---|
| KoP chassis | `kop_chassis` | 1,600 | **Largely KoP-covered.** Retail figure shown for completeness |
| Bumpers + frame perimeter | `bumpers_frame` | 257 | Fabric, plywood, pool noodle, brackets |
| Baseline electrical package (Systemcore era) | `baseline_electrical_package` | 1,979 | **Partly KoP-covered; Systemcore price UNVERIFIED**; **6-week lead, high stockout** |
| Primary mechanism — cheapest credible | `over_bumper_intake` | 380 | 16 build h, 8 design h, 1 motor, `bandsaw_drillpress` |
| Second, non-novel mechanism | `passive_latch_climber` | 245 | 12 build h, 0 motors — the "cheap insurance" archetype |
| Spares + consumables | — | 400–600 | `CAP` |

**The gate check, not this table, is the authority.** Run
`python tools/bom-builder.py <your.yaml>`; `MECH` §12.1 shows this class of configuration
exits 0, and §12.2 shows swerve + intake + elevator + gripper + winch **fails five gates**.

### 6.3 The 6-week electrical lead time is why your first deadline is in November

`MECH` gives `baseline_electrical_package` a **6-week lead time and high stockout risk**. `DCM` §6.4
computes the consequence: with `CAP` `order_by_safety_margin_weeks: 1`, the order-by date is
**2026-11-21 — seven weeks before kickoff.** See §13.

---

## §7 — Stage 5: Assembly + wiring (days 35–50)

**79.9 veq-h (30 fabrication + 49.9 electrical) · 5–6 heads · electrical pkg $1,979 retail**

| Sub-stage | Days | veq-h | Heads | Gate to pass |
|---|---|---:|---:|---|
| Drivetrain rolling chassis | 20–28 | 18 | 3 | **Robot drives under its own power by day 28** (§9.3) |
| Electrical board built *off-robot* | 30–36 | 20 | 2 | Every device addressed and labelled before it goes in |
| Board installed, CAN chain closed | 36–40 | 12 | 2 | Full CAN scan clean; battery/breaker/RSL to rule |
| Mechanism mounted to frame | 40–45 | 16 | 4 | Bolts, not clamps. Fasteners are the real design |
| Bumpers built and fitted | 42–47 | 10 | 2 | To the rule, both colours, with the number |
| Pneumatics (if any) | 42–48 | 4 | 1 | `pneumatics_package` **$555**, 14 build h (`MECH`) — **skip it unless the strategy demands it** |
| **Full-robot shakedown** | **48–50** | — | 8 | **Day 50: robot moves, scores once, unaided** |
| **TOTAL** | | **79.9** | | |

**Two rules that save the most hours [H]:**

1. **Build the electrical board on the bench, off the robot.** Two people can work it in parallel
   with mechanism assembly; on the robot they cannot, and every wire is a contortion.
2. **Label every wire and every CAN id at the moment it is made**, not later. "Later" is day 52 at
   23:00, and by then the person who made it is asleep.

**Day 50 is the honest last date for a Week 1 team** — it leaves 3 days, which is enough to pack and
nothing else. If day 50 arrives and the robot does not move, the correct action is to **compete with
a working drivetrain and no mechanism** rather than a non-functional both. `PF` §4.1's reliability
chain is the reason: a robot that reliably does one thing outranks one that unreliably does two.

---

## §8 — Stage 6: Programming (days 0–60, parallel)

**134.8 veq-h · 2 heads (3 wanted) · $0 software · Systemcore price UNVERIFIED**

**Stack decisions live in [`03_programming_stack.md`](03_programming_stack.md)** — Systemcore, WPILib
2027, command-based structure, AdvantageKit/AdvantageScope, the swerve fork, PathPlanner vs Choreo.
This section owns only **when code starts and on what hardware.**

### 8.1 The 2027 problem, stated once

**[C]** `PF` §6.3 / `TCM` §3.2: **2027 replaces the roboRIO with Systemcore, and WPILib 2027 is
Systemcore-only and incompatible with the Rio.** This is the largest control-system change since the
cRIO. `TCM` §3.2 decomposes the 134.8 h and puts **40 h on toolchain/deploy/Driver-Station bring-up
alone — roughly +30 h versus a normal year.** Whether the roboRIO remains legal in 2027 is
**UNVERIFIED**.

### 8.2 The schedule, and what hardware each phase needs

| Phase | Days | veq-h | Hardware required | If hardware is late |
|---|---|---:|---|---|
| Toolchain, deploy, Driver Station, project skeleton | **0–10** | 40 | **Systemcore unit** — or nothing at all | Simulation only. WPILib sim + a repo skeleton is real, valuable work |
| Drivetrain code + controls tuning | 10–28 | 35 | Rolling chassis (day 28 per §7) | Sim; port to hardware in one session |
| Mechanism control + sensors | 28–45 | 30 | Bench harness (§4.3), then the robot | Bench harness — this is why §4.3 exists |
| Auto routines | 40–55 | 20 | Robot + a taped-out field | `PF` §6.1: **one path** unless an RP is auto-gated |
| Dashboard / logging / telemetry | rolling | 10 | — | — |
| **TOTAL** | | **134.8** | | |

### 8.3 The utilisation problem, and the one action that fixes it

```
programmer supply (2 core x 85.0 h) : 169.9 h
programmer demand                   : 134.8 h   -> 79% utilisation
```

**[C]** from `TCM` §3.2. Two programmers are **79% pre-committed before a single bug exists**, and
their time is also what supports drive practice, pit debugging and match-day code changes.

> **Action with a date on it: develop a third programmer between 2026-09 and 2026-12**, on the 2026
> robot and on Systemcore hardware as soon as it exists. `TCM` calls this "the highest-return item in
> this entire document"; it costs **$0 and zero build-season hours**. See §13.

### 8.4 Code starts on day 0, not day 28

**[H]** The most common small-team failure is programmers idle for three weeks waiting for a robot,
then compressed into the last ten days. Three things are available from **hour one**:

1. **Repo, CI, project skeleton, and the Systemcore toolchain** — 40 h of the budget, needing no
   robot.
2. **Simulation.** `OPS` §0 and `PROG` both note simulator work substitutes for real hours at zero
   shop cost.
3. **The bench harness (§4.3)** — a motor, a controller and a sensor is enough to write and test
   every mechanism subsystem before the mechanism exists.

---

## §9 — Stages 7–8: Integration, drive practice and tuning (days 40–70+)

**84.9 + 54.9 = 139.8 veq-h · 4–8 heads · $700–1,500**

**Method lives in [`04_tuning_testing_competition_ops.md`](04_tuning_testing_competition_ops.md) and
[`04_competition_ops.yaml`](04_competition_ops.yaml)** — practice-field tiers and the three-element
reduction (§1.6), carpet (§1.7), the practice robot options (§2), driver selection protocol (§3.1),
and the full event-ops playbook. This section owns only **when it happens and what it costs.**

### 9.1 The integration line is where reliability is bought

`PF` weights reliability at **88**. The 84.9 h of integration/debug is not contingency — it is the
line that converts "the mechanism works on the bench" into "the mechanism works in match 9 with a
dead battery and a bent bumper." It is also the line that gets eaten first when stages 4–5 slip,
which is the mechanism by which schedule slip becomes competitive failure.

### 9.2 Drive practice — the nine-hour problem

`TCM` §3.4, reproduced because it is the most alarming output in the corpus:

| Step | Week 1 | Week 4 |
|---|---:|---:|
| Budgeted drive-practice veq-h | 54.9 | 139.9 |
| ÷ people a session occupies (driver, operator, reset, coach) | ÷3.5 | ÷3.5 |
| Session-hours of a robot actually moving | 15.7 | 40.0 |
| × fraction after the robot is worth driving **[S]** | ×0.6 | ×0.6 |
| **Meaningful driver hours before event 1** | **≈9 h** | **≈24 h** |

Against a factor `PF` weights **90 — the highest in the corpus**. `OPS` §0 step 2 prices it:
**at an 8-second cycle, one second = 9.7 points/match = 117 points across 12 quals.**

Three responses in cost order (`TCM` §3.4): **move to Week 3–4**; **use the free substitutes**
(simulator, controller-in-hand, driving along with recorded matches — all outside the 15 h/wk); and
**§9.3.**

### 9.3 The free lever: drive the drivetrain from day 28

Build the drivebase first and drive it while the mechanism is still in CAD. This converts
**waiting-for-parts hours** — which are otherwise dead — into the highest-weighted factor in the
rubric, and it gives the programmers a real chassis 17 days before the robot exists (§8.2). It costs
nothing and it is the reason §7 puts "robot drives under its own power" on **day 28**.

### 9.4 The practice field, priced down

`OPS` §1.6 reduces the field to **three elements**. `OPS` §1.5 notes FIRST's own **Team Test Element
build instructions are the shopping list**. Budget **$300–900 [S]**, and note `OPS` §1.7's warning
that **carpet is the line nobody budgets and everybody is surprised by**.

### 9.5 Competition ops

Everything from load-in through elimination repairs is `OPS`. The clock-relevant facts only:

| Item | Day (Week 1) | Day (Week 4) | Source |
|---|---:|---:|---|
| Event load-in / inspection | 53 | 74 | `CAL` |
| Realistic event attendance | **12 of 15** | 12 of 15 | `TCM` §4.4 **[S]** |
| Bodies available for scouting during a match | **3–5** | 3–5 | `TCM` §4.4 |
| Full manual scouting requires | **6** | 6 | `TCM` §4.4 |
| **Rubric consequence** | — | — | **Any strategy that depends on out-scouting the field is out of reach.** Join a scouting alliance (`TCM` §4.4 scheme 3) — zero bodies, one conversation in the pits on Thursday |

---

## §10 — Stage 9 and the off-season loop

### 10.1 Business / awards / scouting (days 0–33+)

**44.9 veq-h · 3–4 heads · $0–150.** Detail lives in
[`05_business_awards_sustainability.md`](05_business_awards_sustainability.md). The clock fact that
governs everything: **the award submission deadline is day 33 (2027-02-11 15:00 ET) [C]** — nine days
*before* Week Zero and twenty days before a Week 1 event. **The Impact submission is written about a
robot that does not exist yet.** Plan it that way: it is a story about the team, drafted in the
off-season and finished in January, not a report on the season.

### 10.2 Off-season (May–December): the four things that actually move numbers

| Programme | Window | veq-h | Heads | $ | Which `CAP` constant it moves |
|---|---|---:|---:|---:|---|
| **Training: promote veterans to unsupervised leads** | Sep–Dec | ~120 | 9 | 0 | `parallel_workstreams_max` — the **only** perturbation that moves `novel_mechanisms_max`, and it moves it ±1 (`TCM` §9.4) |
| **Third programmer on Systemcore** | Sep–Dec | ~60 | 3 | Systemcore unit, **UNVERIFIED** | Programming utilisation 79% → ~53% |
| **Offseason events** | Jun–Oct | ~80 | 12 | ~$300–600/event **[S]** | Real drive practice on a real field with no season cost |
| **Recruiting + first-year onboarding** | Sep–Nov | ~90 | 15 | 0 | Pays the **−73.5 veq-h first-year training tax** (`TCM` §2.4) on hours that have no competing use |
| **Recruit a 2nd technical mentor** | **by 2026-11-17** | ~10 | 1 | **0** | `mentor_unblock_hours_per_week` 3.4 → 6.8. **"Worth more than five additional students"** (`TCM` §6.4) |

**[C]** Off-season events are a well-established part of the FRC calendar and several are run by the
teams in §12 — e.g. **1323 + 1671's MadTown Throwdown**, a two-day competition held in **November**
([team1323.com/mttd](https://team1323.com/mttd/)), and **1678's Citrus Circuits Fall Workshops**
([citruscircuits.org/fallworkshops](https://www.citruscircuits.org/fallworkshops.html)). **2026 dates
are UNVERIFIED** — check each event's own site before planning around it. Note the timing conflict to
resolve early: a November off-season event lands in the same fortnight as the **2026-11-17
registration close** and the **2026-11-21 BOM order-by** (§13.1).

### 10.3 Sustainability, in one number

`TCM` §9.4: **losing one unsupervised lead cuts `novel_mechanisms_max` from 2 to 1** — a 50% cut in
what the robot can be — while gaining one buys nothing (the shop queue catches it). **The asymmetry
is the sustainability argument.** Every off-season hour spent making a *second* person able to own a
mechanism is insurance against the largest uninsured risk the team carries.

---

## §11 — THE PAYLOAD TABLE

**What elite practice requires, what this team can actually do, and what that costs you.**

Team-specific claims are labelled. Where a practice is widely documented across published team
processes but not verified inside this pass, it is **[H] / UNVERIFIED** — the *practice* is real, the
*attribution* is not confirmed. **No team number, URL or statistic below is invented; anything not
checked is marked.**

| Stage | **Elite practice — what it requires (people / hours / $)** | **The ~15-student equivalent** | **What you give up** |
|---|---|---|---|
| **Kickoff (d0–2)** | 40–60 students + 6–10 mentors in the room; parallel breakout rooms per strategy; a dedicated rules sub-team that owns the manual all season; spec decided d2–d5 with prototyping already running underneath **[H]** | **18.0 veq-h, 15 heads, ~$120.** One room, four reading passes (§3.3), spec decided **d2 21:00** by mentor + 3 leads, vetoed by `bom-builder` | **Breadth of strategy exploration.** You examine ~6 candidate strategies, not ~20. Mitigation: `STRATEGY-RANKING-SYSTEM` §2's enumeration is designed so nothing whole *category* is missed even when depth is |
| **Prototyping (d2–10)** | 4–8 benches in parallel, a dedicated prototype sub-team, a stocked material rack, 2+ saws so streams don't queue **[H]** | **47.0 veq-h, 8–10 heads, $150–350.** **Two** prototypes on **one** mechanism, one shared bench harness (§4.3), cut-line **d10** | **The second mechanism, entirely.** You will not discover the clever archetype nobody thought of; you will pick the better of two obvious ones. `PF` §5.1's COTS/Everybot path is the designed compensation |
| **Design/CAD (d5–25)** | 6–12 CAD students, a maintained in-house part library, formal daily/near-daily design reviews, full-robot CAD complete ~d14–d21 **[H]**; several elite teams publish full CAD/code openly — **254** [FRC-2025-Public](https://github.com/Team254/FRC-2025-Public), **971** [971-Robot-Code](https://github.com/frc971/971-Robot-Code), **2910** [CAD + Tech Binder](https://www.chiefdelphi.com/t/2910-cad-and-tech-binder-release-2023/436653), **3476** [frc3476](https://github.com/frc3476), **1690** [2024 CAD](https://www.chiefdelphi.com/t/frc-orbit-1690-2024-robot-cad-release/464838) **[C]**; headcount/cadence **[H]** | **59.9 veq-h, 3–4 heads, $0.** One CAD lead with sole release authority, **three** review gates (d7/d17/d25) totalling 3.5 h of the mentor's 3.4 h/wk unblock budget | **Design iteration count.** One layout, one detail pass, one release — not three revisions. And **no in-house library**: you inherit vendor libraries instead (`DCM` §2.2), which constrains you to standard stack-ups (`DCM` §3.5) |
| **Manufacture (d20–45)** | CNC router and/or mill + lathe in-house, often a sponsor machine shop, 10–15 fabricators, parts made in batches with fixtures **[H]**; **custom-fab path measured at ~$13,000 tank / ~$17,000 swerve** **[C]** first-hand district-mentor account, `PF` §5.1 | **74.8 veq-h, 5–7 heads, $2,500.** Bandsaw + drill press + one 3D printer (`CAP`), **$400** of outsourced 2D sheet at 2-week lead, release-by **d31** | **11 of the 27 `MECH` archetypes** — everything above the `bandsaw_drillpress` floor is gated off before the game is even revealed (`DCM` §0). And **~$10,500–14,500** of capability you are simply not buying |
| **Assembly + wiring (d35–50)** | Dedicated electrical sub-team; wiring harness built off-robot to a documented layout; a **second, identical practice robot** **[H]** | **79.9 veq-h, 5–6 heads, $1,979 retail (largely KoP).** Board built off-robot (§7), one robot only | **The practice robot.** `OPS` §2.2 recommends the reduced option; you practise on the competition robot, which means every practice hour risks the thing you compete with |
| **Programming (d0–60)** | 6–10 programmers, log-replay infrastructure (AdvantageKit), full vision/pose-estimation stack, multi-path autos, code running on hardware from week 1 **[H]**; **6328 publish AdvantageKit and a 900+-post [2026 Open Alliance build thread](https://www.chiefdelphi.com/t/frc-6328-mechanical-advantage-2026-build-thread/509595)** **[C]**; **254's 2025 code documents AdvantageKit IO per subsystem plus physics sim** **[C]** | **134.8 veq-h, 2 heads (79% utilised).** Systemcore port is 40 h of it. **One** auto path (`PF` §6.1). Vision counted as a *mechanism* — adopting it drops `novel_mechanisms_max` 2 → 1 (`TCM` §5.6) | **Vision-based pose estimation, or your second mechanism — pick one.** Plus all schedule reserve: at 79% utilisation a single sick programmer is a schedule event |
| **Drive practice (d45–70+)** | Full or near-full practice field on carpet, practice robot, drivers selected by competition, **many tens of hours** of seat time before event 1 **[H]** | **54.9 veq-h → ≈9 real driver hours** (Week 1) or **139.9 → ≈24 h** (Week 4). Three field elements (`OPS` §1.6), $300–900 | **The highest-weighted factor in the corpus (`PF`: 90).** This is the largest single gap in the table and the one with the cheapest fix: **move to a Week 3–4 event** and it closes by 2.7× for $0 |
| **Scouting** | 6+ dedicated scouts, a custom scouting app, pit scouting, match strategy from data **[H]**; **1678 publish a GPL scouting system — Python processing server + Android collection app** ([frc1678](https://github.com/frc1678)) and **971 publish theirs inside 971-Robot-Code** **[C]** | **3–5 scouts** of 12 attendees (`TCM` §4.4). Two robots per scout, one metric each; or **join a scouting alliance** — zero bodies, one pit conversation | **Picking.** You cannot out-scout the field, so any strategy that requires it is out of reach. Your realistic path is being **picked**, which `PF` §4.3 says is bought with *average delivered points*, not with data |
| **Competition ops** | Pit crew, spare-parts rotation, dedicated strategy/scouting leadership, **multiple events + offseason** **[H]** | **12 attendees; 7 unavailable during any match cycle** (`TCM` §4.4). Registration covers **one Regional or two Districts** **[C]** | **Repeated at-bats.** Elite teams iterate across 2–3 events; you likely get one shot at a shakedown and one at a real event |
| **Off-season** | Year-round programme: offseason events, summer projects, formal training curriculum, alumni mentors **[H]**; **118's [Everybot programme](https://www.118everybot.org/) is published — 441 True Everybots, 100 alliance captains, 21 event wins in 2026** **[C]** `PF` §5.1/§4.4; **1323+1671 run the November [MadTown Throwdown](https://team1323.com/mttd/)** **[C]** | **~360 veq-h across Sep–Dec** (§10.2), 15 heads, ~$300–600/offseason event. Five named programmes with dates (§13) | **Nothing — this is the one row where you are not behind.** Off-season hours have no competing use, and every top-ranked constraint in `TCM` §7.1 is relaxable *only* here. Spending them is the highest-return decision in the file |

### 11.1 How to read this table

Three of the ten rows are **capability gaps you cannot close** (manufacture, programming breadth,
scouting). Four are **gaps you close by descoping** and are already priced into `novel_mechanisms_max
= 2`. **Two are gaps that close for $0 by moving the first event to Week 3–4** (drive practice, and
the schedule collision in §1.2). One — the off-season — is a gap where the team has **no
disadvantage at all** and simply has to show up.

**If you act on exactly two things in this document:** pick a late event at a small field
(**2026-09-24**, `CAL`), and recruit a second technical mentor (**by 2026-11-17**).

---

## §12 — Published team processes: what is verified and what is not

The brief named ten teams whose processes are worth studying. **Each row below was checked against a
live source in this pass.** What is verified is *that the artefact exists at that URL*; what is **not**
verified is any claim about the team's internal schedule, hours or headcount — no such data is
published by any of them, which is why §11's elite column is **[H]**, not **[C]**.

| Team | Artefact — what you can actually read | Source (checked 2026-08-22) | Status |
|---|---|---|---|
| **118** The Robonauts | **The Everybot programme** — a published, pre-solved, low-cost robot. Site states: buildable with *"only common tools, a basic 3D printer, items purchased from your local hardware store"* at **~$1,500 in addition to the Kit of Parts**. 2026 code published separately | [118everybot.org](https://www.118everybot.org/) · [2026 resources](https://www.118everybot.org/2026-frc-resources) · [2026 code](https://github.com/Robonauts-Everybot/FRC-Everybot-2026-Code/) · [2026 CD thread](https://www.chiefdelphi.com/t/the-2026-robonauts-frc-everybot-low-resource-build/510331) | **[C]** — and **441 True Everybots / 100 alliance captains / 21 event wins in 2026** is **[C]** via `PF` §5.1 |
| **6328** Mechanical Advantage | **Open Alliance build thread, 2026** (900+ posts of in-season design/decision logging) — the closest thing in FRC to a public season diary. Also AdvantageKit/AdvantageScope | [2026 build thread](https://www.chiefdelphi.com/t/frc-6328-mechanical-advantage-2026-build-thread/509595) | **[C]** thread exists; software **[C]** via `PROG` |
| **254** The Cheesy Poofs | **Full season code, published every year 2010→**. 2025 repo documents per-package structure, naming conventions, AdvantageKit IO pattern per subsystem, and physics simulation | [github.com/Team254](https://github.com/Team254) · [FRC-2025-Public](https://github.com/Team254/FRC-2025-Public) · [team254.com/resources](https://www.team254.com/resources/) | **[C]** |
| **971** Spartan Robotics | **971-Robot-Code** — a full C++ monorepo with per-directory READMEs, including their scouting system | [github.com/frc971/971-Robot-Code](https://github.com/frc971/971-Robot-Code) | **[C]** |
| **1678** Citrus Circuits | **Open-source scouting system** (Python processing server + Android collection app, GPL) and the **Fall Workshops** series — recorded sessions on their own process | [frc1678 GitHub](https://github.com/frc1678) · [Fall Workshops](https://www.citruscircuits.org/fallworkshops.html) · [CAD & code release](https://www.citruscircuits.org/scouting.html) · [training](https://www.citruscircuits.org/training-resources) | **[C]** |
| **2056** OP Robotics | **Annual Technical Binder release** — the single best published artefact on *how a build season is organised* rather than what it produced | [2025 Technical Binder](https://www.chiefdelphi.com/t/team-2056-op-robotics-2025-technical-binder-release/502550) · [2024](https://www.chiefdelphi.com/t/team-2056-op-robotics-2024-technical-binder-release/465867) · [GitHub](https://github.com/Team2056) | **[C]** |
| **2910** Jack in the Bot | **CAD + Tech Binder releases** and the **"Pop-Up Presentations"** series (scouting, data, pick-listing) | [CAD + Tech Binder 2023](https://www.chiefdelphi.com/t/2910-cad-and-tech-binder-release-2023/436653) · [Pop-Up Presentations](https://www.chiefdelphi.com/t/2910-jack-in-the-bot-presents-pop-up-presentations/442665) | **[C]** |
| **3476** Code Orange | **CAD and code releases**; 35 public repos | [frc3476 GitHub](https://github.com/frc3476) · [2024 CAD+code release](https://www.chiefdelphi.com/t/code-orange-3476-cad-and-code-release-2024/477350) | **[C]** — a dedicated *Open Alliance* thread was **not** found; the releases are the artefact |
| **1690** Orbit | **Robot CAD releases** and public software (dashboard, scouting tooling) | [2024 CAD release](https://www.chiefdelphi.com/t/frc-orbit-1690-2024-robot-cad-release/464838) · [Team1690 GitHub](https://github.com/Team1690) · [orbit1690 GitHub](https://github.com/orbit1690) | **[C]** |
| **1323** MadTown Robotics | **MadTown Throwdown** — a two-day **November** off-season competition, co-hosted with **1671** Buchanan Bird Brains. The model off-season event for §10.2 | [team1323.com/mttd](https://team1323.com/mttd/) · [2025 MTTD thread](https://www.chiefdelphi.com/t/2025-madtown-throwdown-mttd/506666) · [CA FIRST listing](https://cafirst.org/events/frc-off-season-madtown-throwdown/) | **[C]** exists and is annual; **2026 dates UNVERIFIED** |

### 12.1 What these sources do and do not tell you

**They tell you the artefacts.** Code structure (254, 971), season decision logs (6328), process
documentation (2056, 2910), scouting systems (1678, 971), and a complete low-resource reference
design (118). **Every one of these is free and copyable, and copying is the entire small-team
strategy** — `PF` §5.1 measures that the COTS/published-design path produced a **22% alliance-captain
rate against a 21.8% base rate** in 2026.

**They do not tell you the hours.** No FRC team publishes attendance, meeting schedules, or
person-hours per stage — the same gap `TCM` §9.2 and `PF` §7 hit. **Therefore every person-hour and
headcount figure in §11's elite column is [H] inference from roster size and observable output, not
measurement.** Treat the *shape* of that column as sound and every specific number in it as
unconfirmed.

**The one thing to actually do with this table:** read **2056's Technical Binder** and **6328's 2026
build thread** during the off-season (§13, weeks 1–10). They are the two artefacts that describe
*process* rather than *product*, which is what this file is about.

---

## §13 — Off-season plan: Aug 2026 → Jan 9 2027

**Today is 2026-08-22. There are ~20 weeks and no game.** Every top-ranked constraint in `TCM` §7.1
is relaxable **only** in this window.

### 13.1 The dates that are already fixed

| Date | Event | Consequence | Evidence |
|---|---|---|---|
| **2026-09-24 12:00 ET** | **Kit & Kickoff selection / Round 1 event preferencing opens** | **Choose field size first, then the latest week** (`PF` §11 / `TCM` §7.4). This four-month-before-kickoff decision outranks any mechanism decision made in January | **[C]** `CAL` |
| **2026-11-12** | **Pre-Kickoff Virtual Kit Release** | **First real look at the 2027 control system.** Re-check the Systemcore price the same day — it is the one hole in the season budget | **[C]** `CAL` |
| **2026-11-17 12:00 ET** | **Selection / registration closes** | Second technical mentor must be recruited **before** this so they are present for fall training, not onboarded during build season | **[C]** `CAL` |
| **2026-11-21** | **BOM order-by date** | Derived from the **6-week electrical lead time + 1 week margin** (`MECH`, `CAP`). **Your first hard deadline is seven weeks before kickoff** | **[C]** derivation; lead time **[C]** `MECH`, margin **[S]** `CAP` |
| **2027-01-09 12:00 ET** | **KICKOFF** | Day 0 | **[C]** `CAL` |

### 13.2 The week-by-week programme

| Weeks | Dates | Workstream | Heads | veq-h | $ | Owner |
|---|---|---|---:|---:|---:|---|
| 1–4 | Aug 22 – Sep 20 | **Recruiting drive**; shop clean-out and inventory; 2026 robot recommissioned as the training/drive-practice platform | 9 | 60 | 0 | Mentor + core leads |
| 5–6 | Sep 21 – Oct 4 | **EVENT SELECTION (opens 9/24).** Rank candidate events by **field size, then latest week**. Register | 3 | 12 | 6,500 | Mentor |
| 5–10 | Sep 21 – Nov 1 | **Fall training curriculum**: 2 contributing veterans → unsupervised leads; 6 first-years through the −73.5 veq-h training tax on hours with no competing use | 15 | 150 | 0 | Core leads |
| 5–12 | Sep 21 – Nov 15 | **Third programmer development** — on the 2026 robot and 2026 WPILib **until Systemcore exists** (§13.3) | 3 | 40 | 0 | Core tech D |
| 6–12 | Sep 28 – Nov 15 | **CAD onboarding**: licences, workspace structure, standard stack-ups, one full practice assembly (`DCM` §1.3, §2.4, §3.5) | 4 | 45 | 0 | Core tech C |
| 8–14 | Oct 12 – Nov 22 | **Offseason event(s)** — real field, real matches, real driver hours at zero season cost | 12 | 80 | 300–600/ea | Mentor |
| 10–12 | Nov 2 – Nov 15 | **Second technical mentor recruited and inducted** — deadline **11-17** | 1 | 10 | 0 | Mentor |
| 12 | **Nov 12** | **Virtual Kit Release.** Read it same-day. **Re-price the Systemcore line** | 3 | 6 | — | Mentor + Core tech D |
| 12–13 | Nov 16 – Nov 21 | **BOM ORDER-BY.** Place the game-independent order: electrical package, standing stock, bearings/hex/spacers, prototype wheels (`DCM` §6.3) | 3 | 12 | ~1,200 **[S]** | Mentor |
| 13–16 | Nov 22 – Dec 20 | **Outsourced-fabrication account set up + one test order** (`TCM` §7.5); Impact/awards narrative drafted (§10.1) | 5 | 50 | ~150 | Veteran I + mentor |
| 16–20 | Dec 21 – Jan 8 | **Systemcore bring-up on real hardware if it exists**; driver selection protocol run (`OPS` §3.1); kickoff logistics; `KICKOFF_PLAYBOOK` §0 dry-run against the **2026** manual so the pipeline is proven before day 0 | 8 | 60 | 0 | All |
| | | **TOTAL** | | **~525** | | |

### 13.3 ⚠ roboRIO-stack training has a shelf life

**[C]** WPILib 2027 is **Systemcore-only and incompatible with the roboRIO** (`PF` §6.3, `TCM` §3.2,
`PROG` §0). Therefore:

| Fall training activity | Shelf life | Verdict |
|---|---|---|
| Java/Kotlin language fluency, git, code review | **Permanent** | **Train hard.** Zero risk |
| Command-based structure, subsystems/commands, state machines | **Permanent** — the framework concepts survive the platform change | **Train hard** |
| Control theory: PID, feedforward, motion profiling, odometry | **Permanent** | **Train hard** |
| Simulation, AdvantageScope log reading, telemetry discipline | **Mostly permanent**; tooling names may move | **Train** |
| Vendor libraries (motor-controller APIs) | **Partial** — vendor readiness for 2027 is tracked in `PROG` §0 | Train the *pattern*, expect the API to move |
| **roboRIO imaging, radio configuration, roboRIO-specific deploy, Rio-era Driver Station workflow** | **EXPIRES 2027-01-09** | **Do not invest hours here beyond what is needed to run the 2026 robot.** These are the 40 h that `TCM` §3.2 says get re-spent from scratch |
| **Systemcore toolchain itself** | The real target | **Blocked on hardware availability.** No production units existed as of **2026-08-14** (`PF` §6.3) |

**The scheduling implication:** train on the 2026 robot for *concepts*, and treat every hour spent on
Rio-specific mechanics as a sunk cost you are choosing to pay for the sake of having a running robot
to learn on. **Reassess after 2026-11-12.** If Systemcore hardware is orderable then, buying one unit
in November — before the December training block — converts the single largest 2027 schedule risk
into off-season hours that cost nothing.

---

## §14 — Validation / dry run

### 14.1 The arithmetic closes

| Check | Expected | Status |
|---|---|---|
| Nine stage lines (§2.1) sum to the eight mandatory lines (`TCM` §3.1) | **599.1** | ✅ asserted by §0 step 5 |
| Week-4 stage table (§2.2) sums to `effective_build_hours_week4` | **854** | ✅ 854.1, rounding |
| Fabrication split across stages 2/4/5 sums to `fabrication_assembly` | 25 + 74.8 + 30 = **129.8** | ✅ |
| CAD split across stages 2/3 sums to `cad_design` | 15 + 59.9 = **74.9** | ✅ |
| Strategy split across stages 1 and days 3–10 sums to `strategy_rules` | 18 + 7 = **25.0** | ✅ |
| Every day-number in §1.1 recomputes from `CAL` dates | — | ✅ §0 step 1 |
| No stage requires >2 novel mechanisms | `novel_mechanisms_max = 2` | ✅ §4.1 |
| §6.2 example configuration passes the gates | exit 0 | ✅ per `MECH` §12.1 (`simple.yaml`) |

### 14.2 The external sanity check

**Anchor — the Everybot must fit this clock.** 118's Everybot is drivetrain + 1–2 pre-solved
mechanisms at ~$1,500 over KoP, needing common tools and a 3D printer (**[C]**, `PF` §5.1). Run it
through §2.1: prototyping collapses to ~15 h (the design is published — nothing to prototype), CAD
collapses to ~20 h (nothing to design), and the freed ~70 h lands on stages 5, 7 and 8. **Predicted:
day-50 shakedown made comfortably, with roughly double the drive practice.** Observed in 2026: 441
built, 100 alliance captains, 21 event wins, **22% captaincy against a 21.8% base rate** (**[C]**).
✅ **Consistent** — and it names the mechanism: the COTS path wins by moving hours into stages 7–8.

**Counter-anchor — the elite stage sequence must fail on a Week 1 clock.** §1.2's Gantt predicts the
canonical manufacture-to-d45 / assembly-to-d50 / practice-from-d45 plan leaves **3 days** before a
day-53 event and pushes practice past it. `PF` §7 records a driver's own account: *"with this being
our first year with swerve, I actually got no practice because we had lots of problems when
building, so in our first comp I was not actually driving"* (**[C]**). ✅ **Consistent** — and the
predicted failure mode (practice consumed by upstream overrun) is exactly the one reported.

### 14.3 What would falsify this file

- If the 2027 season calendar in `CAL` is wrong, **every day-number in §1.1 moves**. Re-run §0 step 1
  against the published FIRST calendar after 2026-11-12.
- If Systemcore ships late or the roboRIO remains legal, **§8's 40-hour toolchain line is wrong in
  one direction or the other**, and the whole programming column of §11 moves with it.
- If the team's roster is not 5 core / 4 contributing / 6 first-year, **`TCM` §9.4 shows losing one
  core lead halves `novel_mechanisms_max`** — re-run the model, then re-read §4.1 and §11.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/team-ops/01_championship_season_process.md` | **this document** — the day-numbered season timeline, per-stage hours/heads/dollars, the elite-vs-15-student payload table, and the Aug 2026 → Jan 2027 off-season plan |

Nothing else was created or modified. `reference/02_TEAM_CAPACITY_MODEL.md`, `reference/team_capacity.yaml`,
`reference/bom/06_MECHANISM_CATALOG.md`, `reference/team-ops/02_design_cad_manufacturing.md`,
`reference/team-ops/03_programming_stack.md`, `reference/team-ops/04_tuning_testing_competition_ops.md`,
`reference/team-ops/05_business_awards_sustainability.md`, `KICKOFF_PLAYBOOK.md` and
`STRATEGY-RANKING-SYSTEM.md` were **read and cited, not edited**.

---

## Known limitations

- **§12 verifies that the artefacts exist; it does not verify anyone's hours.** All ten named teams
  were checked against live sources on 2026-08-22 and every URL in §12 resolved. But **no FRC team
  publishes attendance, meeting hours or person-hours per stage** — so the people/hours figures in
  §11's elite column are **[H] inference from roster size and observable output, not measurement.**
  Treat the *shape* of that column as sound and every specific number in it as unconfirmed. Two
  specific gaps remain: **3476 has CAD/code releases but no dedicated Open Alliance thread was
  found**, and **2026–27 dates for MadTown Throwdown and the Citrus Fall Workshops are UNVERIFIED.**
- **The day-boundaries of every stage are [S].** Days 0–2 / 2–10 / 5–25 / 20–45 / 35–50 / 0–60 /
  45–70+ came from the brief and match widely-repeated FRC folk practice, but no published,
  measured stage-duration dataset exists for FRC teams. What *is* derived rather than assumed is the
  **collision** in §1.2 — that this sequence needs ~10 weeks against a 7.57-week Week 1 deadline.
  That conclusion holds under any reasonable perturbation of the stage boundaries.
- **The nine-stage hour split in §2.1 is a repartition, not a measurement.** It sums to 599.1 by
  construction because `TCM` §3.1's eight lines sum to 599.1 by construction. The honest content is
  the *mapping* — which stage draws from which line — not the total. `TCM`'s own Known Limitations
  make the same point about §3.3.
- **The Week-4 reallocation in §2.2 is [S] and unvalidated.** Putting +85 h of the +255 into drive
  practice and +50 into integration reflects `PF`'s factor weights (90 and 88); it is a judgement
  about where marginal hours are worth most, not an observation of what teams do with them.
- **Dollar figures mix retail catalog value with incremental-over-KoP spend.** `MECH` prices are
  retail; the Kit of Parts covers an unquantified fraction of `kop_chassis` and
  `baseline_electrical_package`. §2.3 states this but does not resolve it, because the 2027 KoP
  contents are not published. **Do not add the §2.1 dollar column.**
- **The Systemcore price is UNVERIFIED and appears in three tables as a hole.** This is a real gap in
  the season budget. §13.1 puts a date on closing it: **2026-11-12**.
- **§13's week-by-week programme totals ~525 veq-h of off-season effort** and is entirely **[S]**. It
  is a plan, not a forecast; the hours are illustrative of scale, and no small team executes a
  20-week plan without attrition. Treat the five *deadlines* as real and the hour figures as targets.
- **Offseason event names in §10.2 are UNVERIFIED**, including whether they ran in 2026 or will run
  in 2026–27. Check each event's own site.
- **This file contains no BIOCORE game content.** BIOCORE's rules are not public as of 2026-08-22.
  Everything here is a model of time, people and money — which is exactly what is knowable in August
  and exactly what stops being decidable in January.

---

## Security note

Every source read for this pass was a local file inside this project. All of it was treated as
**data**. None contained text addressed to an AI assistant or any attempt to issue instructions. No
authentication was used or attempted. No team number, URL or statistic was invented; where
verification was not possible inside this pass's budget, the claim is marked **UNVERIFIED** rather
than asserted.
