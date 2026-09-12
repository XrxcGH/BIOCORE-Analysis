# Tuning, Testing & Competition Ops — the half of the season that happens after the robot works

**Purpose:** every other file in this project helps you *decide what to build*. This one is about the
period after the mechanism moves — tuning it, proving it, driving it, and keeping it alive for
twelve qualification matches. It is the phase small teams under-invest in, and the measured factor
weights say it is the phase that decides where you finish:
[`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) weights **drive practice at 90** and
**reliability at 88** — the top two factors in the entire corpus, ahead of scope, ahead of swerve,
ahead of auto, ahead of vision. This document converts those two weights into a practice field, a
practice-robot decision, a driver programme, a checklist, a spares list, a battery rotation and a
pick list — all of them priced against the 599 effective hours and the $2,500 the team actually has.

**Companion file:** [`04_competition_ops.yaml`](04_competition_ops.yaml) — every list, cost and
rule reference in this document, machine-readable.

**Authorities this file must not contradict**

| Authority | What it governs here |
|---|---|
| [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml) | every hours and headcount figure. 599 veq-h, 54.9 h drive practice, 84.9 h integration/debug, $2,500 discretionary |
| [`../bom/03_LAUNCHERS_ELECTRONICS.md`](../bom/03_LAUNCHERS_ELECTRONICS.md) + [`../bom/`](../bom/) | every part price |
| [`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) | the scouting data schema and the free-vs-gap-data argument. **§8 links to it and does not repeat it** |
| [`03_programming_stack.md`](03_programming_stack.md) | simulation, logging, AdvantageScope, the Systemcore port |
| [`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md) | FIRST permits AI use with attribution |

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus (quoted file path given) |
| **[H]** HISTORICAL-PATTERN | Observed across prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model assumption. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked in this corpus |

> **Scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game (FIRST CANOPY season), kickoff
> **2027-01-09 12:00 ET**. Nothing here comes from FTC BIOBUZZ; Pollen, StarterBots and Skill
> Builders are BIOBUZZ things and appear nowhere in this file. **BIOCORE's field, scoring elements
> and rules are not public as of 2026-08-22.** Every field-element and rule reference below is a
> 2026 REBUILT example held up as the *shape* of the 2027 problem, and every rule number must be
> re-verified against the 2027 manual on kickoff day (§10.3 tells you how, in one command).
>
> **2027 also replaces the roboRIO with Systemcore.** Where that changes a spare, a checklist line or
> a diagnostic, it is called out inline and marked.

---

## §0 — The 60-second workflow

Five commands. Run them in this order; each one answers a question this document then explains.

```bash
# Run from the repository root.

# ---- 1. WHAT IS A SECOND OF CYCLE TIME WORTH? (the drive-practice argument, ~1 s) ----
#      Read down a column: how sensitive each strategy is to driver skill.
#      A FLAT column is a small-team strategy -- it pays the same with average drivers.
python tools/cycle-model.py --game rebuilt --sweep

# ---- 2. THE HEADLINE NUMBER -----------------------------------------------------------
#      At an 8 s cycle, ONE SECOND = 9.7 pts/match = 117 pts across 12 quals.
python tools/cycle-model.py --game rebuilt --cycle 8   # 90.5 pts
python tools/cycle-model.py --game rebuilt --cycle 9   # 80.8 pts   -> delta 9.7

# ---- 3. HOW MANY REAL DRIVER HOURS DO YOU ACTUALLY HAVE? -------------------------------
#      54.9 veq-h / 3.5 people / x0.6 usable  =  ~9 hours before a Week 1 event.
python tools/capacity_model.py | grep -i "drive practice"

# ---- 4. WHAT THE PRACTICE FIELD COSTS -------------------------------------------------
#      The 2026 Team Test Element build instructions ARE the shopping list. Open one:
ls manuals/archive/supplemental/FieldElements_LowCost/2026_TE-*.pdf

# ---- 5. RE-VERIFY EVERY RULE NUMBER IN THIS FILE AGAINST THE 2027 MANUAL (kickoff day) --
bash tools/probe-2027-manual.sh          # is the manual up yet?
bash tools/ingest-manual.sh              # pull it into manuals/archive/frc/
python tools/rule-inventory.py --season 2027 --rules R401,R601,R603,R604,R606,R607,R612,R709,T601,T602,T603,T604,T605,T606
```

**Read the outputs in this order:** the sweep first (it prices driver skill), then your real driver
hours (it tells you how little you have), then the Team Test Element PDFs (they tell you what a
practice field costs in lumber). If the sweep column for your likely strategy is steep and your
driver hours are 9, §3 is the most important section in this file for you. If the column is flat,
§4 is.

---

# 1. The practice field

## 1.1 FIRST's own vocabulary: *test* is not *practice* — and the distinction is load-bearing

**[C]** FIRST formalised this in
`manuals/archive/supplemental/webpages/blog/FRCblog_2026-01-06_PracticeFieldTeamElementChanges.html`
(FIRST Robotics Competition Blog, "Practice Field & Team Element Changes", 2026-01-06). Verbatim
paraphrase of the two definitions:

| Term | FIRST's definition | What it needs |
|---|---|---|
| **Test** | validating or improving *a single robot function*, without simulating match conditions; typically one field element, limited driving | one element, a corner of the shop |
| **Practice** | simulating *realistic field or match conditions* to improve the robot **including the drive team** — full match simulations, full autos, timed driver-operated scoring, real or simulated defence, all functions exercised, high-speed driving | space, elements, a clock, a second robot or a defender, people |

**Why this matters more than it looks.** Almost every small team believes it "has a practice field"
when what it has is a **test element**. Test elements make the mechanism work. They do not make the
*driver* work, and drive practice is the factor weighted 90. The team that builds one scoring
structure and calls it done has bought the 88-weight factor and skipped the 90-weight one.

**Rule of thumb for this team:** you need *test* capability from Week 2 of build and *practice*
capability from Week 4. They are different purchases and they belong on the calendar separately.

## 1.2 The four official resource tiers — what FIRST actually publishes

**[C]**, verbatim category names and fidelity ratings from the same blog post:

| Category | Element name | Fidelity | Resources FIRST provides | Fabrication needed | Fits this team? |
|---|---|---|---|---|:---:|
| **Test Elements** | **Team Test Elements** | Low | CAD **+ Build Instructions** | **Common power tools** | ✅ **This is your tier** |
| Test Elements | Event Test Elements | Low/Medium | CAD + drawing package | CNC router / plywood | ❌ no router |
| **Practice Elements** | Team Practice Elements | Medium | **CAD only** | CNC router / plywood | ❌ no router, no instructions |
| Practice Elements | Wood Practice Perimeter | Medium | **CAD only** | CNC router / plywood | ⚠️ outsource or buy |

FIRST's own footnote **[C]**: *"a 'High Fidelity' item would be a Field Element that is built
directly from the official drawings for the parts used on the official playing fields."* Nobody at
this budget builds high fidelity, and nobody needs to.

Three things in that table are worth reading twice:

1. **Only Team Test Elements come with build instructions.** The other three ship CAD or drawings
   only. For a team with one mentor and 3.4 unblock hours a week (capacity §6.2), "CAD only" means
   "someone has to design the build", which is a workstream you cannot afford. **Take the tier with
   the instructions.**
2. **Team Test Elements are explicitly designed against FIRST's own Tool & Fabrication
   Expectations** — lumber, hardware-store materials, common hand and power tools. **[C]** That is a
   deliberate match to your shop (`team_capacity.yaml: tooling.level = bandsaw_drillpress`).
3. **Event Test Elements were made public starting in 2026** **[C]** — new that season. They are
   optimised for *shipping and teardown*, not for team use, and they "often incorporate real field
   components that are difficult for teams to replicate." **[C]** Read them for geometry; do not
   try to build them.

## 1.3 What is already on this machine

On a machine that already holds the archive, do not go looking online for these. A fresh clone of this
repository has none of them, because FIRST's documents are not redistributed: run
`bash tools/rebuild-corpus.sh --fetch` from the repository root, and save anything it does not fetch
from FIRST's website to the path shown.

| Path | What it is | Use it for |
|---|---|---|
| `manuals/archive/supplemental/FieldElements_LowCost/2026_TE-26000-build-instructions.pdf` | OUTPOST Team Test Element | the *format* of a 2027 TE package; the shopping list shape |
| `…/2026_TE-26100-build-instructions.pdf` | BUMP | traversal obstacle pattern |
| `…/2026_TE-26200-build-instructions.pdf` | TRENCH | low-clearance pattern |
| `…/2026_TE-26300-build-instructions.pdf` | HUB (v2) | scoring-structure pattern; uses **real polycarbonate field panels** |
| `…/2026_TE-26500-build-instructions.pdf` | TOWER (v2) | endgame/hang pattern |
| `…/2026_TE-26600-build-instructions.pdf` | DEPOT | game-piece source pattern |
| `…/2025_TeamElements.zip`, `2024_…ReadMes.zip`, `2023_…ReadMe.zip` | three prior seasons of the same | how much the format changes year to year: **very little** |
| `…/2020_TeamDrawing-HalfField.pdf`, `…-MinimalField.pdf` | **FIRST's own reduced-field drawings** | the official precedent for "you do not need a whole field" |
| `manuals/archive/supplemental/2026_FieldDimensionDrawings.pdf` | official dimensioned drawings | true dimensions for tape-out (§1.7) |
| `manuals/archive/supplemental/Drawings/2026_FieldDrawings-Evergreen.pdf` | the parts that **do not change** season to season | perimeter, driver stations, carpet — buildable **before kickoff** |
| `manuals/archive/supplemental/2026_FieldManual.pdf` | how FIRST builds the real field | carpet, marking, tolerances (§1.7) |
| `manuals/archive/supplemental/2024_3DPrintedFieldInstructions.pdf` + `2024_3DPrintedFieldFiles.zip` | 3D-printed scale field | the cheapest strategy prop there is (§6.2) |

**The single highest-value item in that list is the Evergreen drawings.** Evergreen = the field
geometry that is *the same every year*. The field perimeter, the driver station wall, the carpet
dimensions and the alliance-station sightlines do not wait for kickoff. **You can build and tape
those in November 2026.** Nothing about BIOCORE's rules changes them.

## 1.4 What elite teams build, and the cost ladder down from there

**[H]/UNVERIFIED as a census** — no public dataset records what fraction of teams own a practice
field. What is verifiable is the *ladder*, and the cost of each rung at hardware-store prices:

| Rung | What it is | Rough cost **[S]** | Space | Who does this |
|---|---|---:|---|---|
| 5 | Full official field, welded perimeter, real elements | $30k–$60k+ | 30 × 60 ft | a handful of teams; usually a sponsor's warehouse |
| 4 | Half field, official-drawing elements, real carpet | $6k–$15k | 30 × 30 ft | strong, well-funded programmes |
| 3 | Wood Practice Perimeter + Team Practice Elements + carpet | $1,500–$3,500 | 30 × 30 ft | mid-size teams with a CNC router |
| **2** | **Team Test Elements + taped outline + used carpet** | **$250–$600** | **25 × 40 ft** | **← this team** |
| 1 | Two elements on bare shop floor, no carpet | $80–$200 | a bay | rookie/minimum |
| 0 | Simulator + a taped rectangle | **$0** | a hallway | the fallback that is better than nothing |

**[S]** on every dollar figure except rung 2's element costs, which are computed from the real
shopping lists in §1.5.

**The finding worth acting on:** the jump from rung 0 to rung 2 costs roughly **$400**, which is
**16% of `robot_discretionary` ($2,500)**. The jump from rung 2 to rung 3 costs about five times as
much and buys *fidelity*, not *practice hours*. Practice hours are the thing weighted 90. Buy rung 2
early and spend the difference on batteries (§7) and spares (§5.3).

## 1.5 The real shopping list — 2026 Team Test Elements, verbatim

**[C]** from the build-instruction PDFs listed in §1.3. Held here as the **shape** of a 2027 build
package, not as a 2027 claim — BIOCORE's elements do not exist yet.

| Element | Lumber | Fasteners | Notes |
|---|---|---|---|
| **TE-26000 OUTPOST** | 6 × 2×4×8, 1 × 1×2×8, 1 × 4'×8'×½" ply | ~54 × #8×2.5", ~16 × #8×1.5", 4 × #8×1", 2 × ¼-20×3.5" bolt + wing nuts | the biggest single element |
| **TE-26100 BUMP** | 5 × 2×4×8, 1 × 4'×8'×½" ply | ~60 × #8×2.5", ~24 × #8×1.5" | traversal obstacle |
| **TE-26200 TRENCH** | 3 × 2×4×8, 1 × 4'×4'×½" ply | ~30 × #8×2.5", ~8 × #8×1.5" | low clearance |
| **TE-26600 DEPOT** | 1 × 4'×4'×½" ply | wood glue | trivially cheap |
| **TE-26300 HUB v2** | — | — | **uses the same polycarbonate funnel panels as the real field (GE-26329)** — purchasable rather than fabricated |
| **TE-26500 TOWER v2** | — | — | for practising hanging; AndyMark sold a TOWER RUNG in the **same material and length as the official RUNG**, unpainted and undrilled |

**Read the last two rows.** They are the pattern that repeats every season: **the one geometry that
must be exact — the interface your mechanism physically touches — is sold as a real part by a
vendor, and everything else is plywood.** Budget for one real interface part and lumber for the rest.

**Total lumber for all four wooden elements above:** 14 × 2×4×8, 1 × 1×2×8, 2 × 4'×8' half-inch ply,
1 × 4'×4' half-inch ply, ~200 wood screws. At August-2026 US big-box prices that is roughly
**$180–$260** **[S]** — the estimate is [S] because lumber and sheet-goods prices are regional and
volatile, and this project does not have a verified 2027 price source. **Price it locally in
November, not in January.**

## 1.6 THE REDUCTION — you only need these three elements

This is the section to act on. On kickoff day the temptation is to build the whole released TE
package because FIRST published it. **Do not.** Build these three, in this order, and defer the rest
until a specific test demands them.

| # | Element | Why it is non-negotiable | Deliverable |
|---:|---|---|---|
| **1** | **One copy of the primary scoring structure** — at the exact height, exact opening, exact approach angle | You cannot tune a scoring mechanism against a guess at its geometry. Every prototype iteration, every shooter/placement trajectory, every alignment sensor threshold is calibrated against this one surface | the mechanism's tuning target |
| **2** | **One copy of the game-piece source / floor pickup zone** | The other end of every cycle. **Half of every cycle-time measurement you will ever take.** A team that builds only the scoring end can measure "time to score" but never "cycle time", which is the number in §3.3 | the intake's tuning target |
| **3** | **A taped floor outline at true dimensions, plus a driver-station sightline stand-in** | Distance and sightline are what the *driver* learns. A 6-ft plywood wall with a cutout at real driver-station eye height, placed at the real distance, teaches more about driving than a perfect HUB does | the driver's training environment |

**Element 3 is the one small teams skip and it is the one that maps to the 90-weight factor.** It
costs one sheet of plywood, two 2×4s and a roll of gaffer tape. A driver who has only ever driven
standing next to the robot has learned a completely different task from the one they will do at the
event — where they are behind a polycarbonate wall, 25 feet away, looking at their robot from
outside the field with a wall of noise between them and their operator.

**Deferred until a specific test demands it** — with what to build instead:

| Deferred | Build this instead | When to reconsider |
|---|---|---|
| Obstacles (BUMP / TRENCH analogues) | nothing; a 2×4 laid flat tests most traversal | only if the game *requires* traversal to score |
| The endgame structure | a **dimensional jig**: two pieces of extrusion holding the exact interface geometry at the exact height, clamped to a wall | when the endgame mechanism exists and needs repetitions |
| The second alliance's half of the field | nothing | never, for this team |
| AprilTag placement rig | print the tags at correct size and tape them at correct height (`…/2026_AprilTag_Images_and_User_Guide.pdf`) | only if you run vision pose estimation — which capacity §5.6 says costs you a mechanism |
| A full carpet field | one 12 × 12 ft carpet remnant under the scoring structure | when the drivetrain's traction tuning stops matching event behaviour |

**The generalisation:** *build the geometry your mechanism touches; tape the geometry your driver
navigates; buy the one part whose material properties matter; skip everything else.*

## 1.7 Carpet — the thing nobody budgets for and everybody is surprised by

**[C]**, `manuals/archive/supplemental/2026_FieldManual.pdf` §3.2 *Carpet Installation*, verbatim:
the playing field carpet is **74 ft × 30 ft**, laid from **two gray carpet rolls, 74 ft long**, and
the tools required are **carpet tape (1 roll), 3" black gaffer's tape (3 rolls), 100 ft chalk line,
carpet knife, utility knife, 100 ft tape measure**. FIRST's own instructions add: *"Minimize bumps
and ripples as much as possible"* and *"Accurate chalking and taping are paramount"*, and
**gaff tape is for carpet marking, not for queuing**.

Why you care, in three points:

1. **Traction on carpet is not traction on a shop floor.** Every wheel-tread decision, every
   current-limit, every autonomous drive constant and every skid-steer turning calibration is
   carpet-dependent. A robot tuned on sealed concrete arrives at the event with the wrong constants
   and the team spends Thursday re-tuning instead of practising.
2. **You do not need 74 × 30.** You need enough carpet under the *scoring approach* and the
   *pickup approach* that the drivetrain sees carpet during the two moments that matter. A
   **12 × 12 ft remnant** is enough to calibrate traction and to run drill D1 (§3.6).
3. **Sourcing [S]:** carpet stores and flooring installers discard usable remnants continuously, and
   "we are a school robotics team" is an unusually effective ask. Also ask your event's host venue in
   March — fields get rebuilt and old carpet is consumable. Budget **$0–$150** and treat any spend
   above that as a failure of asking.

**The tape-out, which is free and which you should do in November:** chalk-line and gaffer-tape the
true field outline on your shop floor using
`manuals/archive/supplemental/Drawings/2026_FieldDrawings-Evergreen.pdf`. Evergreen geometry does not
change with the game. This is the single cheapest thing in this document and it converts your shop
into element 3 of §1.6.

## 1.8 Practising with no field at all

Ranked by value per dollar. All of these cost **$0** and none of them consume shop-queue capacity
(capacity §5.2 route C), which is why they are the small team's real practice budget.

| Method | What it actually trains | Evidence |
|---|---|---|
| **Field-oriented control in the simulator** | driver's mental model of heading vs. field frame — the hardest thing to learn and the thing that transfers most completely | **[C]** named by drivers in [ChiefDelphi #521233 post 13](https://www.chiefdelphi.com/t/521233/13), cited in `PF` §7.2. See [`03_programming_stack.md`](03_programming_stack.md) §7 for the sim stack |
| **Controller-in-hand rehearsal of the button map** | operator's motor memory for the button sequence — eliminates the "which button was the intake" pause that costs 1–2 s per cycle | **[C]** same thread |
| **Driving along with recorded matches** | strategic pattern recognition: where robots queue, when to bail on a cycle, where defence comes from | **[C]** same thread |
| **A taped rectangle + two traffic cones + last year's robot** | raw drivetrain control (drills D1, D2, D6) | **[S]** |
| **A 3D-printed scale field on a table** | *strategy* rehearsal and alliance-partner briefings, not driving | **[C]** files exist: `…/2024_3DPrintedFieldFiles.zip` |

**The honest limit:** none of these trains *scoring*, because scoring is a physical interaction with
a real surface at a real height. Simulation trains navigation; only element 1 of §1.6 trains scoring.
Plan for both.

## 1.9 Who builds the practice field — and the capacity trick hidden in it

Capacity §2.4, **[S]**: six first-years are worth **+31.4 net veq-h** before a Week 1 event, because
the training tax they draw (−73.5 veq-h) nearly cancels their gross output (+104.9). They are not a
build-season resource for the *robot*.

**But the practice field is a perfect first-year work package**, for four reasons that all come from
the capacity model:

1. It is **bounded and instructed** — FIRST ships step-by-step build instructions (§1.2), so it
   consumes almost none of the mentor's 3.4 h/wk unblock budget.
2. It uses **wood tools, not the shop queue** — a circular saw and a drill/driver, not the bandsaw
   and the 3D printer that capacity §5.2 route C says are already saturated by two mechanisms.
3. It is **not on the robot's critical path** — if it slips three days nothing downstream slips.
4. It **can be done off-site**, in a garage or a second room, which is the only way to get more than
   two workstreams' worth of people usefully busy in one shop.

**Assign it on kickoff day + 3, due kickoff day + 10.** That is `2027-01-12 → 2027-01-19`. Give it
to three first-years and one contributing veteran as owner. It is the only work package in the season
where a first-year can produce a finished, useful, non-critical artefact — which is also how you
find out which first-years become next year's core-technical tier.

---

# 2. The practice robot

## 2.1 The honest framing

"Every good team builds a practice robot" is the most expensive folk belief in FRC. What good teams
actually have is **a robot that is finished early enough to be driven**, and the second robot is how
well-funded teams buy that. It is a *symptom* of the advantage, not the cause.

For this team the arithmetic is brutal and short: a second full robot costs **$1,500–$2,500**, which
is **60%–100% of `robot_discretionary` ($2,500)** (`team_capacity.yaml`). Spending it means the first
robot gets no spares, no batteries and no second scoring mechanism. **It is out of reach and the
decision takes ten seconds.**

## 2.2 The five options, priced

| Option | Cost **[S]** | Hours cost | What it buys | Verdict |
|---|---:|---|---|---|
| **A. Full second robot** | $1,500–$2,500 | ~130 veq-h of fabrication (= the entire `fabrication_assembly` line) | continuous driving + a spare for every part | ❌ **OUT OF REACH.** Also needs a second Systemcore, price **UNVERIFIED** |
| **B. Identical drivetrain only** | **$500–$900** | ~25 veq-h | drivetrain code, autos, drills D1/D2/D6, driver conditioning — all while the superstructure is still in CAD | ✅ **RECOMMENDED** |
| **C. Swap-superstructure** (one drivebase, two tops) | $0–$400 | ~15 veq-h of interface design | lets you iterate the mechanism without tearing the robot down | ⚠️ situational — only when the superstructure *is* the thing you are iterating |
| **D. Last year's robot** | **$0** | ~4 veq-h to recommission | driver conditioning, drill practice, first-year training, demo/outreach robot | ✅ **DO THIS ON 2026-09-01** |
| **E. Simulation** | **$0** | in the `programming` line already | drivetrain code, autos, field-oriented control, button-map rehearsal | ✅ **MANDATORY IN 2027** — see [`03_programming_stack.md`](03_programming_stack.md) §7 |
| **F. Finish the real robot two weeks earlier** | $0 | scope discipline | everything a practice robot buys, for free | ✅ **the actual elite advantage** |

## 2.3 Why option B is the right one, specifically

A second **drivetrain** — not a second robot — is the cheapest way to decouple the two things that
compete for the robot in weeks 4–7:

- **the programmers** need the drivetrain to develop drive code, odometry and autos;
- **the driver** needs the drivetrain to accumulate the seat time in §3;
- **the mechanical team** needs the *whole robot* on the bench to mount, align and iterate.

With one robot these three are strictly serial and the driver always loses, because the driver's need
is the only one without a deadline. With a second drivetrain they are parallel, and the driver's
hours come out of *calendar time* instead of out of *robot time*.

**What "identical" has to mean:** same wheel diameter, same gear ratio, same motor count, same
weight class within ~15 lb, same controller mapping. It does **not** need the same frame material,
the same electronics quality, or bumpers. **[S]** A KoP-class chassis with four propulsion motors, a
board with a PD, a Systemcore, a radio and a battery is the whole build.

**The 2027 catch, stated plainly:** option B needs a **second Systemcore**, and Systemcore's price is
**UNVERIFIED** as of 2026-08-22 (capacity §8.1). Until the **2026-11-12 Pre-Kickoff Virtual Kit
Release** you cannot cost this option. **Action:** re-price option B on 2026-11-13, before the
**2026-11-21 BOM order-by**. If a second Systemcore is expensive, option B degrades to "a second
drivetrain you tether-test and swap the control board into", which still works but halves the
parallelism benefit.

## 2.4 Option D is free and you are not doing it

Last year's robot is sitting in the shop right now, on 2026-08-22, with 4.5 months of runway. It
teaches:

- **driving** — every drill in §3.6 except D4/D5 (which need this year's cycle) runs on last year's robot;
- **the pre-match checklist** (§4.2) as a *rehearsed ritual* rather than a January novelty;
- **battery rotation and load testing** (§7) on real hardware;
- **first-year electrical and mechanical fundamentals** on a robot nobody is afraid of breaking;
- **the pit-crew choreography** in §6.4, which is pure muscle memory.

**[S]** Recommissioning cost is roughly 4 veq-h and one battery. Capacity §7.5 already puts "start
driver practice on the 2026 robot" on the fall list as an ongoing item. This section is the argument
for why it outranks almost everything else on that list: **it is the only fall activity that buys the
90-weight factor directly, and it costs nothing.**

---

# 3. Driver development

## 3.1 Selecting drivers — a protocol, not a popularity contest

**[S]** for the whole protocol; there is no published FRC driver-selection standard. What follows is
designed to be *measurable*, because the alternative — seniority or the loudest advocate — reliably
picks the wrong person and cannot be defended to the person who was not picked.

**When:** first tryout **2026-10-01** on last year's robot; final selection **no later than
2027-02-05** (~Week 4 of build), so the chosen pair gets every remaining practice hour.

**The tryout, 20 minutes per candidate, on a taped course:**

| Test | Measure | Weight |
|---|---|---:|
| Timed slalom, 5 gates, best of 3 | seconds | 20% |
| Stop-on-a-mark, 10 reps | count within ±2 in | 20% |
| **Blind-side approach** — score with the robot between candidate and target | success rate over 10 | **25%** |
| **Recovery after an induced fault** — mentor kills a motor mid-run | seconds to adapt and continue | **20%** |
| Coachability — follow three verbal corrections in 60 s under noise | subjective 1–5, two assessors | 15% |

**What the weights are saying [S]:** raw speed is 20% of the score. **Blind-side and recovery
together are 45%**, because that is where matches are actually lost — the driver whose robot is
between them and the goal, and the driver who freezes when something breaks. A fast driver who
freezes is worth less than a medium driver who adapts.

**Two hard rules:**

- **Pick a pair, not two individuals.** Driver and operator are a single unit. Test the top three
  candidates in all three pairings and pick the *pair* with the best D4 median (§3.6).
- **Pick a designated backup and give them 20% of the practice hours.** Capacity §4.3 lists
  driver ↔ operator as an *unsafe doubling* and the drive team as unshareable. A team of 15 that
  brings 12 to an event has no slack: one flu, one family emergency, one college visit and you are
  fielding an untrained driver in your first qualification match. **[S]** 20% is the cheapest
  insurance in this document.

## 3.2 How many hours drivers actually get — the honest numbers

**This is where published data does not exist, and saying so is more useful than inventing a
number.** `PF` §7.2, **[C]**: *"No dataset of practice hours vs outcome exists — nobody records it."*
Any claim you read that "elite drivers get 100 hours" is **UNVERIFIED**. What *is* computable:

| Quantity | Value | Source |
|---|---:|---|
| Your budgeted drive-practice line | **54.9 veq-h** | `team_capacity.yaml: hours.allocation.drive_practice` **[S]** |
| People a practice session occupies at once (driver, operator, field reset, spotter/coach) | ÷ 3.5 | capacity §3.4 **[S]** |
| → session-hours of a robot actually moving | **≈ 15.7 h** | |
| Fraction after the robot is reliable enough to be worth driving | × 0.6 | capacity §3.4 **[S]** |
| **→ real driver seat-time before a Week 1 event** | **≈ 9 h** | capacity §3.4 |
| **→ real driver seat-time before a Week 4 event** | **≈ 13.4 h** | same fractions on 854 veq-h |
| **Seat time you get at the event itself** | **≈ 30 min** | 12 quals × ~2.5 min **[H]** |
| Seat time across a two-event season including playoffs | **≈ 1.2 h** | **[H]** |

**Three findings fall straight out of that table.**

1. **Competition is not practice.** A full season of matches gives your driver about **72 minutes**
   of driving. Whatever skill they show in March was built in the shop, not at events. This is the
   mechanism behind `PF` §7.2's headline result **[C]**: teams improve 37–46% between their first and
   second event and move **under 2 rank percentile points**, because *everyone* improves at the same
   rate. **The only improvement that buys relative position happens before event 1.**
2. **Moving from a Week 1 to a Week 4 event raises real driver seat time from ~9 h to ~13.4 h — a
   49% increase, for $0.** Capacity §7.4 already identifies event week as the single highest-return
   decision (+255 veq-h vs +220 for seven extra meeting hours a week). This is a second, independent
   reason for the same choice, and it lands on the highest-weighted factor. **The decision window is
   2026-09-24 to 2026-11-17** — before kickoff, before the game exists. Note capacity §7.4's
   countervailing constraint: **optimise field size first** (`PF` §11 measures a 3–20× pick-rate
   difference between small and large events), *then* take the latest week among the survivors.
3. **The 0.6 usable-fraction is the lever nobody pulls.** Forty percent of your budgeted practice
   time is consumed driving a robot too unreliable to learn anything from. Every hour of §4's
   reliability work converts directly into usable practice hours. **Reliability (88) and practice
   (90) are not competing line items — reliability is a multiplier on practice.**

## 3.3 What a second of cycle time is worth — run the numbers

`tools/cycle-model.py --game rebuilt --sweep`, verbatim (AUTO units = 3):

```
 cycle s     no endgame  TOWER L1 (TEL  TOWER L2 (TEL  TOWER L3 (TEL
--------------------------------------------------------------------
       4          178.0          178.0          183.0          185.5
       5          143.0          145.0          151.0          155.0
       6          119.7          123.0          129.7          134.7
       7          103.0          107.3          114.4          120.1
       8           90.5           95.5          103.0          109.2
      10           73.0           79.0           87.0           94.0
      12           61.3           68.0           76.3           83.8
      15           49.7           57.0           65.7           73.7
      20           38.0           46.0           55.0           63.5
```

Differencing the first column gives the **marginal value of one second**, which is the number this
whole section exists to establish:

| Cycle improves from → to | Δ pts / match | **Δ pts across 12 quals** | Comment |
|---|---:|---:|---|
| 5 s → 4 s | **35.0** | **420** | elite territory; a second is worth a whole endgame |
| 6 s → 5 s | 23.3 | 280 | |
| 7 s → 6 s | 16.7 | 200 | |
| **8 s → 7 s** | **12.5** | **150** | |
| **9 s → 8 s** | **9.7** | **117** | ← **the anchor figure** |
| 10 s → 9 s | 7.8 | 93 | |
| 12 s → 10 s | 5.9 /s | 140 total | |
| 15 s → 12 s | 3.9 /s | 139 total | |
| 20 s → 15 s | 2.3 /s | 140 total | |

**The anchor:** at an 8 s cycle, **one second of cycle time is 9.7 points per match — 117 points
across a 12-match qualification schedule.** For scale, that is more than a Level 3 endgame climb
(30 pts) delivered in every single match, four times over.

**The non-obvious finding — a second is not worth the same to everyone.** The value of a second is
**15× higher at a 4 s cycle than at a 20 s cycle** (35.0 vs 2.3 pts/match). Two consequences that
point in opposite directions and must both be held:

- **If your robot is fast, drive practice is the best investment you can make.** Nothing else in
  this project returns 35 points a match.
- **If your robot is slow (12–20 s cycles), a second of driver skill is worth only 2–4 points a
  match**, and the *fixed-value* strategies pay far better: at a 20 s cycle the L3 endgame is worth
  **+25.5 pts** (63.5 vs 38.0), whereas at a 4 s cycle the same endgame is worth **+7.5**. That is
  the tool's own advice, verbatim from its output: *"A strategy whose column is flat is
  cycle-insensitive — that is a SMALL-TEAM strategy: it pays the same whether your drivers are elite
  or average."*

**Therefore the kickoff-day sequence is: estimate your cycle time first, then decide how much drive
practice to buy.** Not the other way round. A team with a 15 s cycle that spends its slack on driver
hours instead of on a fixed-value endgame is optimising the flattest part of the curve.

## 3.4 The break-even: drive practice hours vs a second mechanism

The trade that actually comes up in Week 4 is: *"we have ~60 spare hours — a second mechanism, or
double the driver's seat time?"* Here is the arithmetic, stated so you can check it.

**Cost side.** Capacity §5.2 route B prices a novel mechanism at **90 veq-h [S]**. Ninety veq-h
routed into drive practice instead buys 90 ÷ 3.5 × 0.6 = **15.4 additional real driver hours**,
taking the driver from ~9 h to **~24 h — a 171% increase**.

**Benefit side.** For those 15.4 hours to beat a mechanism worth, say, 20 pts/match, they must
improve the cycle by:

| Starting cycle | Cycle needed to gain 20 pts/match | Required improvement |
|---:|---:|---:|
| 8 s | ≈ 6.6 s | **17%** |
| 12 s | ≈ 8.6 s | **28%** |
| 15 s | ≈ 10.4 s | **31%** |

**The verdict, honestly stated [S]:** a 17% cycle improvement from tripling a *rookie* driver's
hours is entirely plausible. The same improvement from a driver who already has 30 hours is not —
learning curves flatten. **So the answer is not universal; it depends on where your driver is on the
curve, and you can measure that with drill D4 (§3.6) rather than guess it.**

**Two thumbs on the scale, both favouring practice:**

1. **The mechanism's 20 points are conditional on it working.** `PF` §4.1, **[C]**: a three-link
   chain at 90% reliability each is **72.9%** reliable end-to-end. A mechanism available in 70% of
   matches is worth 14 points, not 20 — and the required cycle improvement drops accordingly.
2. **The mechanism is workstream #4 and you are allowed three.** Capacity §5.3 is unambiguous:
   `novel_mechanisms_max = 2`, and workstream #4 *"fails by starving workstream #2 of the last 30%
   of its reliability work."* Drive practice is **not a workstream** — it needs no design decision,
   no fabrication-queue slot, no mentor unblock time and no unsupervised lead. **It is the only
   high-weight investment that does not consume the resource that binds this team.**

**And one thumb the other way, which you should not ignore:** drive practice occupies **3.5 people**
per session. That is its real cost, and it is why the 90-weight factor gets 9% of the budget. The
mitigation is in the next paragraph.

**The staffing trick.** Two of those 3.5 seats — **field reset and spotter** — require no technical
skill. Capacity §2.4 says six first-years net **+31.4 veq-h** all season because their training tax
nearly eats their output. **Field reset does not draw a training tax.** Staffing practice sessions
with first-years converts your least productive labour into the highest-weighted factor, and it is
the single best use of a first-year in January.

## 3.5 The ten drills

From [`04_competition_ops.yaml`](04_competition_ops.yaml) `drive_practice.drills`. Each has a
**number** attached, because a drill you do not score is a drill you cannot improve at.

| # | Drill | Min | What you record | Trains |
|---|---|---:|---|---|
| **D1** | Straight-line stop-on-a-mark | 10 | reps within ±2 in, out of 10 | throttle discipline, deceleration model |
| **D2** | Figure-eight around two cones | 10 | lap time, best of 5 | turning coordination, momentum |
| **D3** | **Blind-side approach** — robot between driver and target | 10 | scores out of 10 | the hardest real skill; 25% of the tryout score |
| **D4** | **Full cycle, stopwatch** | 20 | **median of 10 cycles — THE number** | everything; this is your cycle time |
| **D5** | **Cycle under contact** — a defender robot present | 15 | median cycle with defence | what a real match feels like |
| **D6** | Recover from a dropped game piece | 10 | seconds to re-acquire | the most common in-match error |
| **D7** | Auto handoff | 10 | teleop first-cycle start latency | the 2–4 s everybody loses at 0:15 |
| **D8** | Endgame under a 20 s clock | 15 | success rate over 10 attempts | the highest-variance points on the field |
| **D9** | Brownout recovery | 10 | seconds from stall to moving again | what the driver does when voltage sags (§7) |
| **D10** | Comms-loss drill | 10 | what the driver does with a dead radio | the panic case; the answer is *hands off, wait* |

**D4 is the drill that matters.** It produces the single number that feeds `cycle-model.py`, which
feeds every strategy comparison in [`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md).
Record the **median of 10**, not the best — the best is a story, the median is a forecast.

**D5 is the drill nobody runs and everybody needs.** `PF` §9.1 finds the payoff to defence is real
and growing. Your cycle time under contact is a different number from your cycle time alone, and it
is the number that applies in playoffs. Run D5 with last year's robot as the defender; that is a
second free use for option D of §2.

**D9 and D10 are 20 minutes total and they convert a match-ending panic into a rehearsed response.**
Both failure modes are in §4.6. A driver who has practised D10 knows that a comms loss means
*hands off the sticks and wait*, not *mash everything*, which is what an unrehearsed driver does and
which is how robots hurt themselves when comms return.

## 3.6 A structured 90-minute practice session

**[S]** The shape matters more than the exact minutes. The failure mode is a "practice session" that
is really an unstructured driving-around session — fun, and worth about a third of this.

| Min | Block | Who |
|---:|---|---|
| 0–5 | **Pre-match checklist rehearsal** (§4.2), out loud, timed | driver + one pit crew |
| 5–15 | Warm-up: D1 then D2 | driver, operator |
| 15–35 | **D4 — ten timed cycles, recorded** | + field reset (first-year), + timer (first-year) |
| 35–50 | One rotating skill drill: D3 / D5 / D6 / D7 / D8 by week | full 3.5-person crew |
| 50–70 | **Two full match simulations** — 2:30 on a clock, score kept, autos run | everyone |
| 70–80 | **Fault injection**: mentor pulls a breaker or a controller mid-run → D9/D10 | everyone |
| 80–90 | **Debrief + log** (§6.5) and **failure log entries** (§5.1) | driver, operator, coach |

**Two rules that make the difference:**

- **The clock runs.** FIRST's own definition of practice **[C]** includes *"driver-operated scoring
  while timing or tracking score"* and *"full match simulations"*. Driving without a clock is
  testing, not practising.
- **The debrief is not optional.** Ten minutes of writing down what happened is what turns 80 minutes
  of driving into a trend you can see (§3.7).

## 3.7 Measuring improvement — the one chart to keep

Keep a single CSV. Nothing more.

```csv
date,session_no,driver,operator,robot,drill,reps,median_s,best_s,worst_s,notes
2027-01-24,3,H,C,practice-dt,D4,10,14.8,12.9,19.2,"intake miss on 3 of 10"
2027-01-31,6,H,C,comp,D4,10,12.1,10.8,15.0,"new intake geometry"
```

Plot **median D4 time against session number** and read three things off it:

| What you see | What it means | What to do |
|---|---|---|
| Curve still falling steeply | driver is on the steep part of the learning curve | **buy more hours** — §3.4's break-even favours practice |
| Curve flattened for 3+ sessions | driver has converged; further hours return little | shift hours to reliability (§4) or a fixed-value strategy (§3.3) |
| **Spread (worst − best) not shrinking** | the *robot* is inconsistent, not the driver | this is a §4 problem, and no amount of practice fixes it |

**That last row is the most useful diagnostic in this section.** A driver improves by lowering the
median. A robot improves by shrinking the spread. If the spread is not shrinking, you are burning
90-weight hours on an 88-weight problem, and the hours are wasted.

---

# 4. Reliability engineering

## 4.1 What reliability is measurably worth

`PF` §8, **[C]**, from `research/predictive_tba/pf4_reliability.csv` across **30,986 team-events**:

| Season | team-events | % picked, **no DQ** | % picked, **≥1 DQ** | median rank %ile, no DQ | median rank %ile, ≥1 DQ |
|---|---:|---:|---:|---:|---:|
| 2023 | 7,208 | 62.9% | **41.6%** | 48.9 | 75.7 |
| 2024 | 7,605 | 61.7% | **22.5%** | 50.0 | 86.0 |
| 2025 | 8,013 | 62.1% | **22.8%** | 49.1 | 86.4 |
| 2026 | 8,160 | 64.7% | **39.4%** | 49.2 | 74.6 |

**One DQ roughly halves your chance of being picked and moves your median finish from mid-field to
bottom quartile.** And `PF` §8 is explicit that this is a **lower bound**: DQ is a *rules* event, so
the mechanical failures this section is actually about — a dead battery, a snapped intake, a robot
that does not move — are **invisible in this dataset**. The true cost is larger than the table shows.

Practitioner consensus on how reliability is bought, **[C]** as testimony from
[How do you make a reliable robot](https://www.chiefdelphi.com/t/520378), quoted in `PF` §8:
drive it into a wall at full speed on purpose; re-check every fastener every 30–60 minutes of
driving; run a written pre-match checklist; **make a spare of every part outside the frame
perimeter**; overbuild anything outside the frame perimeter and ignore its weight; design for
repairability. The rest of §4 is that list, made executable.

## 4.2 The pre-match checklist — a real one

**Print this on card stock. Laminate it. Two copies: one in the pit, one on a lanyard that goes to
the field.** It runs **in the queue line, every match, out loud, two people** — one reads, one
touches the thing and answers. Target **4 minutes**. Rule numbers are **[C]** from the 2026 manual
(`manuals/archive/supplemental/2026_GameManual_HTML.htm`) and **must be re-verified for 2027** (§0
command 5).

### POWER

- [ ] Fresh battery installed; **battery number logged on the match sheet** (§7.4)
- [ ] Battery strap tight — battery cannot move if the robot is tipped (**R606**: must not dislodge *"if the ROBOT is turned over or placed in any arbitrary orientation"*)
- [ ] Battery and main-breaker terminals fully insulated (**R607**)
- [ ] **SB50 fully seated** — listen for the click, then tug the **cable**, not the housing
- [ ] 120 A main breaker seated, and **accessible from the exterior** (**R612**)
- [ ] All PD breakers seated; **none warm to the touch** from the last match *(a warm breaker is a current problem, not a breaker problem)*
- [ ] **Robot Signal Light illuminates on power-up** (**R709** — 1–2 RSLs, P/N `855PB-B12ME522` and/or `am-3583`, visible from 36.0 in away)

### MECHANICAL

- [ ] Every fastener outside the frame perimeter re-checked — **torque-mark line unbroken** (§4.3)
- [ ] Chain / belt tension checked on **every** driven stage
- [ ] No cracked 3D-printed part; no elongated bolt hole; no fresh bare metal (= something moved)
- [ ] Bumpers: correct alliance colour, all fasteners in, **no gap ≥ 1.25 in between adjacent segments** (**R401**), hard parts not more than 1.25 in out from the perimeter (**R404**)
- [ ] Robot in legal **STARTING CONFIGURATION** — nothing outside the vertical projection of the perimeter (**R102**)

### ELECTRICAL

- [ ] **Wiggle test**: every Anderson/PowerPole, every CAN pigtail, every encoder connector — grab and shake, watch the dashboard
- [ ] No wire crossing a moving joint without a **service loop and strain relief** (§4.5)
- [ ] Radio LEDs visible to field staff (**R708**); radio mount fasteners present

### CONTROL

- [ ] Driver Station laptop > 50% battery or on mains; correct FMS profile
- [ ] **Correct code version deployed**, confirmed by a **version string printed on the dashboard** *(not "we think we deployed it")*
- [ ] **CAN device count on the dashboard equals the expected count** ← **the single best 30-second test on this list**
- [ ] Auto routine selected on the dashboard and **read back out loud** to the coach
- [ ] Controllers in the correct USB order; cables strain-relieved to the console, not hanging

### HUMAN

- [ ] Driver, operator, human player, coach all present and know the alliance plan (§6.2)
- [ ] Safety glasses on all four
- [ ] **The 6-minute kit and the spares bag are at the field, not in the pit** (§6.4)

**Why the CAN-count line is starred.** It is a single integer that tests the entire electrical
harness end to end in three seconds. If it is right, nearly every wiring failure mode in §4.6 is
excluded. If it is wrong, you know *before* the match instead of at 0:14 into it. **[S]** but it
follows directly from the failure taxonomy below.

## 4.3 Torque marking — the cheapest reliability tool that exists

**What it is:** after a fastener is tightened to its final torque, draw a single line of paint pen or
lacquer marker **across the bolt head and onto the substrate beneath it**. If the line is ever broken
or offset, the fastener has moved.

**Why it beats re-torquing everything:** re-torquing 200 fasteners takes 40 minutes and is never
done. **Reading 200 torque marks takes 90 seconds and is a visual scan any first-year can do.** It
converts a skilled, slow, unrepeatable task into an unskilled, fast, repeatable one — which is
exactly the conversion a 15-student team needs everywhere it can get it.

**[S]** Mark, in this priority order: (1) every fastener outside the frame perimeter, (2) gearbox and
motor mounting bolts, (3) drivetrain wheel and hub hardware, (4) anything holding a battery,
electronics board or bumper bracket. Do **not** bother marking fasteners you routinely remove.

Cost: one paint pen, roughly $4. **[S]**

## 4.4 Threadlocker and fastener policy

| Situation | Use | Why |
|---|---|---|
| Fastener never serviced during the season | **Blue (242) threadlocker** | vibration-proof, still removable with hand tools |
| Fastener serviced routinely (access panels, battery bracket) | **Nylock nut**, no threadlocker | threadlocker on a serviced joint is a repair-time tax you pay in the pit |
| Anything into plastic or 3D print | **no threadlocker** (it attacks some plastics), use a washer + nylock or a heat-set insert | chemical compatibility |
| Anything structural you might want back | Blue, never red | **[S]** red (271) generally needs heat to remove; you will not have heat at 0:06 on the field |
| Set screws on shafts | Blue + a **flat** on the shaft | a set screw on a round shaft walks; the flat is the fix, the threadlocker is the backup |

**The policy statement to put on the shop wall:** *every fastener on this robot is either blue-Loctited
and torque-marked, or nylock and on the service list. There is no third category.* **[S]**

## 4.5 Strain relief and service loops

Three rules that eliminate most of §4.6's electrical failure modes:

1. **Every connector is mechanically supported before it is electrically loaded.** The connector is
   never what holds the cable. A zip tie 2 in behind every connector, anchored to structure.
2. **Every cable crossing a moving joint gets a service loop** — enough slack that the cable is never
   in tension at either extreme of travel — **and the loop is zip-tied to the moving member, not to
   the frame.** A cable tied to the frame is repeatedly bent at the same point; a cable tied to the
   moving member travels with it.
3. **Never route CAN with power.** Separate the runs physically. Bundled with a 40 A motor lead, CAN
   picks up exactly the noise it was twisted to reject.

**[S]** for all three as stated; they are standard practice, not measured findings.

## 4.6 The classic failure modes, with the design-out for each

The eight failures that end small-team matches. Sources: `04_competition_ops.yaml: failure_modes`,
`PF` §8 practitioner consensus **[C]**, and the manual rules cited. Root causes and design-outs are
**[S]** engineering judgement unless marked.

| # | Failure | Symptom in a match | Root cause | **Design it out** | Pit fix (≤ 6 min) |
|---:|---|---|---|---|---|
| 1 | **Anderson SB50 / PowerPole** | intermittent total power loss; robot "dies" and comes back | cold-crimped contact, or a spring-fatigued housing that has been mated hundreds of times | **Hex crimper, never pliers.** Pull-test every crimp to ~20 lb. **Retire any SB50 that inserts without resistance.** Keep 2 pre-crimped spare pairs in the pit | swap in the pre-crimped spare pair |
| 2 | **CAN bus** | devices drop off the dashboard at random; a motor stops responding | one bad daisy-chain joint, a missing terminator, a shorted twisted pair inside a drag chain | **Split the bus by subsystem** — Systemcore exposes **5 native CAN-FD ports** (see [`03_programming_stack.md`](03_programming_stack.md)), so a single bad node no longer takes the robot down. Label every node. Never route CAN with power | bypass the suspect node; re-check CAN count |
| 3 | **Encoder cable** | one mechanism runs away, or refuses to home | flex fatigue at the connector on a moving stage | Service loop; tie to the **moving** member. **Prefer absolute encoders** so a mid-event reboot does not require a homing ritual | swap cable; re-zero |
| 4 | **Belts** | skipped teeth, then a snapped belt mid-match | over-tension, pulley misalignment, or debris | Tensioner with a **repeatable setting** (not "feels right"), matched-width pulleys, guard against debris | spare belt of that exact length, taped inside the toolbox lid |
| 5 | **Chain** | thrown chain, usually drivetrain, usually after contact | slack from wear, no retention | Tensioner block + **chain guard**; record master-link locations on the robot with a paint dot | master link + 3 in of chain |
| 6 | **Brownout** | robot slows or stops when several mechanisms run together | battery internal resistance too high, **or** simultaneous current draw | **Load-test and retire batteries (§7.3)**; current-limit in software; **stagger mechanism start-up in code**; never run a battery two matches in a row | swap battery; note the battery number in the failure log |
| 7 | **Fastener back-out** | a mechanism drifts out of alignment across the day | vibration | Blue 242 + **torque marks** (§4.3–4.4) | re-torque, re-mark |
| 8 | **Bumpers** | inspection failure, or a mid-event bumper repair | wood screws into end-grain plywood; no positive retention | **Through-bolt the backing**; pin-and-bracket retention rather than screws. Carry a spare fastener set and a staple gun | re-staple fabric; replace bracket |

**The pattern across all eight:** *the failure is almost never in the part; it is in the joint between
two parts.* Crimps, connectors, cable exits, belt/pulley interfaces, master links, bolted joints,
bumper attachments. **[S]** Design reviews should spend their time on interfaces, not on components.

**The 2027-specific one to watch.** Systemcore's electrical topology differs from the roboRIO's, and
[`03_programming_stack.md`](03_programming_stack.md) documents what Systemcore *removes*. Every item
in row 2 above is written against the 5-port CAN-FD architecture and should be re-verified once
hardware is in hand. Whether the roboRIO remains legal in 2027 is **UNVERIFIED**.

## 4.7 The 30–60 minute re-check ritual

`PF` §8 **[C]** records the practitioner rule as *"re-check every fastener every 30–60 minutes of
driving."* Made operational:

- **Every practice session, at the halfway point**, stop the robot for **5 minutes**. Two people: one
  reads torque marks, one wiggle-tests connectors. Log anything found in the failure log (§5.1).
- **Every event day, at lunch.** Same 5 minutes. This is the highest-yield 5 minutes of an event day
  and it is always the first thing cut.
- **After any collision hard enough to hear.** Not "if it seems fine". `PF` §8 also records the
  advice to *drive it into a wall at full speed on purpose* — which is a test you run **once, in the
  shop, deliberately**, and then inspect. Do it in Week 5. Better to find it on your floor.

## 4.8 Design for repairability — four rules

**[S]**, from the same practitioner consensus:

1. **No repair may require full disassembly.** If replacing the intake roller means removing the
   elevator, the roller will not be replaced during an event.
2. **Access holes over access panels.** A hole you can get a hex key through beats a panel you have
   to unbolt.
3. **Overbuild anything outside the frame perimeter and ignore its weight.** **[C]** as practitioner
   consensus, `PF` §8. Everything outside the perimeter gets hit; nothing inside does.
4. **Every part outside the frame perimeter has a spare** (§5.3). This is the same rule, stated as
   inventory instead of as design.

## 4.9 Use the Inspection Checklist as a reliability tool, not a compliance chore

The archive holds inspection checklists for **2013, 2015–2026**
(`manuals/archive/supplemental/20XX_InspectionChecklist.pdf`), plus a
`2022_InspectionChecklist_Abbreviated.pdf`. **[C]** they exist.

**[S]** Two uses beyond passing inspection:

- **Self-inspect in Week 5, from the previous year's checklist.** The evergreen items — bumper
  construction, battery retention, breaker accessibility, RSL, wiring gauge, sharp edges — change
  very little year to year. Finding them in your shop in February costs an hour. Finding them at the
  inspection table on Thursday costs your practice-match slot, which is your only event-day
  drive-practice hour.
- **Diff the 2027 checklist against 2026 the day it is published**, with `tools/teamupdate-diff.py`.
  Every changed line is a design constraint someone on your team has not heard of yet.

---

# 5. Failure logging, spares, and the pit

## 5.1 The failure log — one CSV, kept all season

**This is the highest-value, lowest-cost practice in this entire document, and almost no small team
does it.** Without it, "what broke this season" is an argument between people's memories. With it, it
is a `sort | uniq -c`.

**Schema** — keep it at `logs/failures_2027.csv`:

```csv
date,context,match,subsystem,part,symptom,root_cause,fix,minutes_lost,battery_no,recurrence,logged_by
2027-02-14,practice,,drivetrain,left front chain,thrown chain,slack after 3 h driving,added tensioner block,25,,1,B
2027-03-06,quals,Q17,intake,roller belt,skipped teeth then snapped,over-tensioned,replaced belt + set tensioner mark,6,B4,2,F
2027-03-06,quals,Q22,electrical,SB50,robot died 0:40 then returned,cold crimp on the + contact,swapped spare pair,0,B4,1,F
```

| Field | Why it is there |
|---|---|
| `context` | `practice` / `quals` / `playoff` / `pit` — separates "things that break under practice load" from "things that break under match load"; they are different populations |
| `subsystem` | the grouping you will actually count by |
| `root_cause` | **fill this in later if you must, but fill it in.** "It broke" is not a root cause |
| `minutes_lost` | converts failures into the currency the capacity model uses |
| `battery_no` | ties brownouts to specific batteries (§7.4). This one column is why brownout diagnosis is possible |
| `recurrence` | 1 = first time, 2+ = it has happened before. **Any row with recurrence ≥ 2 is a design defect, not an incident** |

**The analysis, at the end of the season and at the end of each event:**

```bash
# Run from the repository root.
# what breaks most
cut -d, -f4 logs/failures_2027.csv | tail -n +2 | sort | uniq -c | sort -rn
# where the time goes
python -c "import csv;r=list(csv.DictReader(open('logs/failures_2027.csv')));\
import collections;d=collections.Counter();[d.update({x['subsystem']:int(x['minutes_lost'] or 0)}) for x in r];\
print(sorted(d.items(),key=lambda k:-k[1]))"
# the design defects: anything that happened twice
awk -F, 'NR>1 && $11>=2' logs/failures_2027.csv
```

**What a season of this buys you [S]:**

- the **spares list for next season**, derived rather than guessed;
- the **pre-match checklist for next season** — every recurrence ≥ 2 becomes a checklist line;
- **evidence for judged awards.** [`../awards/AWARD-ALIGNMENT.md`](../awards/AWARD-ALIGNMENT.md) and
  [`05_business_awards_sustainability.md`](05_business_awards_sustainability.md) both want
  demonstrated engineering process. A failure log with root causes and design changes is the most
  credible process artefact a small team can produce, and it costs ten minutes a week;
- an honest answer to *"is our robot getting more reliable?"* — plot `minutes_lost` per event.

**Who owns it:** the safety captain (Veteran G in capacity §4.2). It is a natural pairing — the
person already walking the pit looking for hazards is the person who sees the failures.

## 5.2 The spares list

Governing rule, **[C]** as practitioner consensus (`PF` §8): **make a spare of every part that lives
outside the frame perimeter.** Prices marked **[C]** are verified in
[`../bom/03_LAUNCHERS_ELECTRONICS.md`](../bom/03_LAUNCHERS_ELECTRONICS.md); the rest are **[S]**
quantities without a verified 2027 price.

**Electrical**

| Item | Qty | Unit | Note |
|---|---:|---:|---|
| SB50 connector + 6 AWG contacts | 2 | **$6.60** **[C]** | pre-crimp them in the shop, not in the pit |
| 40 A snap-action breaker | 4 | — **[S]** | |
| 30 A / 20 A breakers | 4 | — **[S]** | |
| **120 A main breaker** (CB285-120 class) | 1 | — **[C]** part class | **long lead time — put it on the 2026-11-21 order** |
| Motor controller, most-used model | 1 | — **[S]** | one, not one per type; pick the model you have most of |
| CAN pigtail, per vendor | 2 | — **[S]** | |
| Encoder + cable, each type on the robot | 1 | — **[S]** | |
| Limit switch | 2 | — **[S]** | |
| 12 / 14 / 18 AWG wire, red + black | 10 ft ea | — **[S]** | |
| Ferrules + WAGO-compatible tips | 1 bag | — **[S]** | |
| Ethernet cable, short | 2 | — **[S]** | |
| **Robot Signal Light** (`am-3583`) | 1 | **$70.00** **[C]** | required by **R709**; a dead RSL is an inspection failure |

**Mechanical** — one of each: every belt length on the robot · chain + master links (3 ft) · intake
roller / compliant wheels (1 set) · **every 3D-printed part outside the frame perimeter** ·
drivetrain wheel + hub · gearbox pinion + shaft key · bumper fastener set + spare fabric panel ·
**the whole primary-mechanism assembly, if it is small enough to duplicate**.

**Consumables** — blue (242) threadlocker · zip ties 4 in and 8 in · gaffer, electrical and
double-sided tape · sandpaper and files · shop towels and isopropyl (wheel cleaning between matches
is real and it is free grip) · **spare safety glasses for visitors**.

**Budget:** `team_capacity.yaml: budget_usd.spares_consumables = $500` **[S]** (the 400–600 midpoint).
That is **20% of `robot_discretionary`**, and §4.1's table is the argument for why it is not the line
to cut.

**The one thing to 3D-print in December:** every printed part that will live outside the frame
perimeter, printed **twice**, the day the design freezes. The printer is a route-C bottleneck
(capacity §5.2) in January and idle in December.

## 5.3 The pit tool list

**Hand:** metric + imperial hex keys (**two full sets, one on a lanyard**) · ratcheting wrench set ·
screwdrivers incl. #1/#2 Phillips and a small flat · needle-nose + diagonal cutters + wire strippers ·
**hex crimper for 6 AWG (SB50)** and a ratcheting ferrule crimper · torque wrench or a marked breaker
bar · tape measure, calipers, machinist square.

**Power:** **two cordless drills** (one drilling, one driving — never re-chuck mid-repair) · impact
driver · soldering iron + solder + heat-shrink + heat gun · rotary tool + cutoff wheels.

**Diagnostic:** multimeter (continuity + DC volts) · **battery load tester / internal-resistance
meter** (§7.3) · **laptop with the full toolchain installed OFFLINE** (see
[`03_programming_stack.md`](03_programming_stack.md) — event wifi is not a build environment) ·
spare USB-A and USB-C cables + a hub.

**Infrastructure:** power strip + 25 ft extension cord · **multi-bank battery charger** (≤ 6 A
average per **R604**, with the Anderson SB connector installed per **R603**) · a cart or hand truck
rated for the robot · labelled parts bins, **one bin per subsystem** · printed pit banner with the
team number · fire-safe battery tray.

**The two-drills line is not padding.** In a 6-minute repair (§6.4), stopping to change a bit is 40
seconds of a 360-second budget — 11%.

## 5.4 Pit layout

**[S]** entirely. The 10 × 10 ft footprint is the modal FRC pit and is **UNVERIFIED for 2027** —
confirm on your event page before building anything to fit it.

```
        <------------------- ~10 ft -------------------->
   ^    +----------------------------------------------+
   |    |  [ BANNER / TEAM NUMBER — visible from aisle ]|
   |    +----------------------------------------------+
   |    | BATTERY   |                    |  TOOL CART   |
   |    | STATION   |                    |  + BINS      |
  ~10ft | charger   |      ROBOT         |  (1 bin per  |
   |    | tray, log |      CART          |   subsystem) |
   |    | 6 slots   |    (centre, so     |              |
   |    | LABELLED  |    you can walk    |  6-MIN KIT   |
   |    |           |    all 4 sides)    |  (grab bag)  |
   |    +-----------+--------------------+--------------+
   |    | SAFETY / FIRE EXTINGUISHER | STANDING SPACE   |
   v    |  + first aid + glasses     | FOR JUDGES (keep |
        |                            |  ~3x3 ft CLEAR)  |
        +----------------------------+------------------+
                    ^ open side faces the aisle ^
```

Five rules that make the layout work **[S]**:

1. **The robot cart is central and reachable from four sides.** Three people working one robot is the
   whole point of a pit; a robot against a wall is a one-person repair.
2. **Batteries live in one place with the charger and the log** (§7.4). Batteries scattered around the
   pit is how a partially charged battery gets into a match.
3. **Keep ~3 × 3 ft of floor genuinely clear.** Judges arrive unannounced, and a pit you cannot stand
   in is a judging conversation you have in the aisle. This is a *judged* space —
   [`../awards/01_AWARD_WINNING_PATTERNS.md`](../awards/01_AWARD_WINNING_PATTERNS.md) is the
   authority on what they are looking for.
4. **The 6-minute kit is a physical grab bag by the aisle**, not a drawer (§6.4).
5. **One bin per subsystem, labelled.** Searching is the hidden cost of every event repair.

---

# 6. Match operations

## 6.1 The match-day clock

**[S]** A qualification day is roughly 12 matches over 8 hours — about **40 minutes per match cycle**,
of which about 2.5 minutes is driving. What you do with the other 37 minutes is the job.

| T− | Action | Who |
|---|---|---|
| **T−25 min** | Battery on charge is pulled and rested (§7.3); next battery selected from the rotation | battery owner |
| **T−20 min** | **Pre-match checklist part 1** (POWER, MECHANICAL, ELECTRICAL) in the pit | 2 pit crew |
| **T−15 min** | **Alliance strategy meeting** (§6.2) — 3 minutes, standing, with the partners | drive coach + driver |
| **T−10 min** | Robot to the queue | pit crew |
| **T−6 min** | **Pre-match checklist part 2** (CONTROL, HUMAN) in the queue line, out loud | driver + 1 |
| **T−2 min** | Robot on the field, in starting configuration; auto read back out loud | drive team |
| **T+0** | Match | drive team |
| **T+3 min** | Robot off the field; **immediate visual damage scan before the cart moves** | pit crew |
| **T+8 min** | **Post-match debrief** — 90 seconds, four questions (§6.5) | drive team + coach |
| **T+10 min** | Failure log entries (§5.1); battery goes to the *bottom* of the rotation | safety captain |

**The two lines people skip are T+3 and T+8**, and they are the two that compound. The damage scan
finds the crack before it becomes a broken part next match. The debrief is the only feedback loop the
drive team has.

## 6.2 The alliance strategy script — 3 minutes, standing

You get about three minutes with two partners you have never met, in a loud room. Freeform
conversation wastes it. **Use the same script every time**; partners notice, and it is a substantial
part of how a small team gets a reputation as a good partner — which is how a small team gets picked
(§8.4).

> **1. Identity (15 s).** *"We're [team #]. Our robot does **X**. Our cycle time is about **N**
> seconds. We're reliable at X and we do not do Y."*
> — **Lead with the honest limitation.** A partner who plans around your limitation is worth far more
> than one who is surprised by it in the match.
>
> **2. Ask, don't tell (30 s).** *"What does your robot do best? What's your auto? Where do you start?"*
> — **Starting position first.** Two robots in the same start slot is the most common and most
> avoidable auto collision.
>
> **3. Auto plan (30 s).** Agree start positions and first paths out loud. Draw it if there is a
> whiteboard or the 3D-printed field (§1.3).
>
> **4. Teleop lanes (45 s).** Assign *space*, not tasks: *"we'll work the left side, you take the
> right, [third team] feeds."* Robots collide over territory far more than over strategy.
>
> **5. Endgame trigger (30 s).** *"We leave for endgame at 0:25. Call it if you need us earlier."*
> A named clock time prevents the classic two-robots-in-the-same-place-at-0:10 failure.
>
> **6. Defence (15 s).** *"If we're up, do you want us to play defence? We'd rather cycle."*
> — `PF` §9.1 finds the defence payoff is real and growing, but it is an **alliance** decision, not a
> unilateral one.
>
> **7. Read-back (15 s).** One person repeats the whole plan in four sentences. **If the read-back is
> wrong, the plan was never agreed.**

**Bring a physical prop.** A laminated field diagram and a dry-erase marker, or the 3D-printed scale
field (`manuals/archive/supplemental/2024_3DPrintedFieldFiles.zip`, **[C]** the files exist). Pointing
at geometry is faster and less ambiguous than describing it, and it works across a language barrier.

## 6.3 In-match communications

Four people, one job, one loud room. **[S]** but it follows directly from capacity §4.3's rule that
the drive coach is a **mentor** role and must watch the whole field, not the robot.

| Role | Watches | Says | Never says |
|---|---|---|---|
| **Driver** | their own robot only | *"stuck", "we're up", "need reset"* — short status only | strategy |
| **Operator** | the mechanism + the dashboard | *"ready", "jammed", "voltage"* | driving instructions |
| **Drive coach** (mentor) | **the whole field and the clock** | *targets, timing, endgame call* | *"go faster"* |
| **Human player** | their own station + the coach | acknowledgement | anything else |

**Four protocol rules:**

1. **One voice at a time, and the coach owns the clock.** *"Twenty seconds — leave for endgame now."*
2. **Nobody tells the driver how to drive during a match.** They cannot act on it and it costs
   attention. Corrections go in the debrief.
3. **Call the endgame at a fixed clock time, agreed pre-match.** Not "when it feels right".
4. **Practise the comms in D5 and D8** (§3.5). Comms is a skill and it degrades under noise. Have a
   mentor stand next to the drive team and shout unrelated things during practice — it sounds silly
   and it is exactly what an event sounds like.

## 6.4 The 6-minute repair

Between matches you sometimes get very little time. **[S]** for the 6-minute figure as a planning
number — **the 2026 manual export in this corpus does not contain a playoff turnaround table or a
timeout rule, so playoff turnaround times and timeout availability are UNVERIFIED and must be read
out of the 2027 manual §10 at kickoff.** Plan for six minutes; be delighted by more.

**The 6-minute kit** — a physical grab bag that goes to the field with the robot, every match:

| Contents | For |
|---|---|
| Pre-crimped **spare SB50 pair** | failure mode 1 |
| **Spare battery**, charged and rested | failure mode 6 |
| Hex key set on a lanyard + a driver with a bit already chucked | failures 5, 7 |
| Zip ties (both sizes), electrical tape, gaffer tape | everything |
| Spare belt of the most-loaded length + 3 in of chain + master links | failures 4, 5 |
| Bumper fastener set + a few staples | failure 8 |
| The **laminated checklist** and a paint pen (re-mark what you re-torque) | §4.2–4.3 |

**The protocol, rehearsed until it is choreography:**

| Sec | Action |
|---:|---|
| 0–30 | **Diagnose out loud.** One person names the failure; nobody touches anything yet |
| 30–45 | **Decide: repair, bypass, or play degraded.** The coach decides, not the fixer |
| 45–300 | **Two people on the repair, maximum.** A third fetches. A fourth is in the way |
| 300–330 | **Re-run the POWER and CONTROL blocks** of the checklist. Every one |
| 330–360 | **Re-mark torque, log it** (§5.1), go |

**The decision at 0:30 is the whole thing.** *"Play degraded"* is a legitimate and frequently correct
answer: a robot that drives and plays defence scores more alliance points than a robot that misses
the match while being perfectly repaired. **[S]**, but it follows from §4.1 — the measured cost of
unreliability is *not being on the field*.

## 6.5 The post-match debrief — 90 seconds, four questions

Same four questions every time. Ninety seconds. Standing. **Somebody writes the answers down.**

1. **What did the robot do that it was not supposed to do?** → failure log (§5.1)
2. **What did we (the humans) do that we did not intend?** → drill selection for the next practice (§3.5)
3. **What did we learn about a partner or an opponent?** → the scouting sheet — see
   [`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) for the schema; do not invent a second one
4. **What are we changing before the next match?** → exactly one thing, with an owner and a time

**Rule 4 is the discipline.** Small teams leave a debrief with six changes, make none, and arrive at
the next match with the same robot and lower morale. **One change, one owner, one deadline.**

**[S]** the format; the value is that it is *short, fixed and written*. An unwritten debrief is a
conversation, and a conversation is not a feedback loop.

---

# 7. Battery management

## 7.1 The rules

**[C]** from `manuals/archive/supplemental/2026_GameManual_HTML.htm`. **Re-verify for 2027** — these
numbers are stable across seasons **[H]** but "stable" is not "guaranteed".

| Rule | Requirement |
|---|---|
| **R601** | Exactly **1** non-spillable **sealed lead acid** battery. **12 V nominal**; **17 Ah min, 18.2 Ah max** at the 20-hour rate; rectangular; nominal **7.1 × 3.0 × 6.6 in** (±0.1 in each); **11.0–14.5 lb**; **nut-and-bolt terminals**; vents unobstructed during charging |
| **R602** | COTS USB battery packs ≤ 100 Wh with 5 V/5 A or 12 V/5 A max output per USB-PD port, and batteries integral to a COTS computing device or self-contained camera, are separately allowed **for cameras/computers only** |
| **R603** | Any charger used on a robot battery **must have the corresponding Anderson SB connector installed** |
| **R604** | A charger **may not exceed 6 A average charge current** |
| **R605** | **Batteries are not ballast** — no extra batteries on the robot, powered or not |
| **R606** | Battery secured so it will not dislodge *"if the ROBOT is turned over or placed in any arbitrary orientation"* |
| **R607** | Battery, main-breaker and their lug/wire connections **fully insulated at all times** |

The manual names **Enersys NP18-12 / NP18-12B** among examples meeting R601 **[C]**. The
`04_competition_ops.yaml` standard part is **MK Battery ES17-12** at **$58–$60/unit** (AndyMark and
REV two-packs, **[C]**).

## 7.2 How many you actually need — the arithmetic

The rule everyone states is *"never run a battery two matches in a row"*, and it is the right rule
(failure mode 6). Here is what it costs:

| Constraint | Consequence |
|---|---|
| A 12-match qualification day, ~40 min per cycle | ~12 discharge events |
| A battery needs roughly a **full match-cycle interval** of charge **[S]** at ≤ 6 A (**R604**) | ~1 battery finishing charge per cycle |
| Plus **30 minutes of rest** off the charger before use **[S]** | one battery always resting |
| Playoffs add back-to-back matches with short turnarounds | +1 buffer |

```
  1 in the robot
+ 1 on the charger
+ 1 resting (just off charge)
+ 3 in the rotation, cooling
------------------------------
= 6 batteries  ← the minimum for a self-sufficient qualification day
```

**Six is the number.** At $58–$60 each **[C]** that is **$350–$360**, or **14% of
`robot_discretionary`**. Against §4.1's finding that unreliability roughly halves your pick
probability, and §4.6's finding that brownout is a top-three failure mode, this is the least
regrettable $350 in the budget.

**If you cannot afford six**, the honest degradations, best first: (a) borrow — battery lending
between teams at events is routine and costs a conversation; (b) run four and accept that two will
be reused warm, and **log which ones** (§5.1) so you know what caused the brownout; (c) **[S]** run a
multi-bank charger so charge throughput, rather than battery count, is the constraint. Never (d):
run three and hope.

## 7.3 Load testing — the only way to know a battery is dead

**Resting voltage lies.** A battery with high internal resistance reads 12.8 V at rest and collapses
to 9 V under a 100 A drivetrain draw. **[S]** but it is the physics of the failure and it is why
brownouts feel random.

| Test | When | Instrument | Reject if |
|---|---|---|---|
| **Internal resistance** | start of season, mid-season, end of season, **and after any brownout** | battery internal-resistance meter (§5.3) | **> 18 mΩ** — retire from competition, demote to practice **[S]** |
| **Load test** | same schedule | load tester | voltage sags below the brownout threshold under rated load |
| **Charge-acceptance** | any battery that "charges instantly" | charger readout | reaches full in far less time than its siblings — the classic sulfation signature **[S]** |

**The 18 mΩ threshold is [S]** — a planning value, not a measured or FIRST-published limit. What is
not [S] is the *practice*: measure, log, and rank. Even without a defensible absolute threshold, the
**relative** ranking across your own six batteries tells you which one to put in an elimination
match and which one goes to the practice robot.

**Do this on 2026-12-15**, before the **2026-11-21** BOM order-by has passed — actually, invert that:
**load-test in early November, order replacements by 2026-11-21.** A battery ordered in January
arrives after you needed it.

## 7.4 Rotation and labelling

Four hard rules, from `04_competition_ops.yaml: batteries.hard_rules`:

1. **Never run a battery two matches in a row.**
2. **Number every battery with a permanent label** — big, readable from 6 ft, on **two** faces — **and
   log the number on every match sheet.** This is what makes the `battery_no` column in §5.1 work,
   and it is the only way to ever answer *"was that brownout the battery or the code?"*
3. **Load-test at the start and end of the season and log internal resistance each time.** A rising
   resistance trend is a battery telling you it is about to end a match.
4. **A battery that ever browned out the robot gets tested before it is trusted again.** No
   exceptions and no "it was probably the code".

**The rotation, physically:** six numbered slots on the battery station (§5.4), used **strictly
left to right**. A battery coming off the robot goes to the **rightmost empty slot**; the next
battery comes from the **leftmost full slot**. It is a FIFO queue implemented in plywood, it needs no
tracking, and a first-year can run it perfectly.

**Rest 30 minutes after charge** before use **[S]**. A battery straight off the charger has a
surface charge that reads high and is not real capacity.

## 7.5 Chargers

**[C] R603**: the charger must have the corresponding **Anderson SB connector installed**. **[C]
R604**: **≤ 6 A average charge current**. Practical consequences **[S]**: a multi-bank charger is
worth more than a faster single-bank one, because R604 caps the rate and only bank count moves
throughput; and every charger you own needs the SB connector fitted before the event, not at it.

**Budget [S]:** 6 × ES17-12 at $58–$60 = **$350–$360** **[C]** unit prices; plus a multi-bank charger
and leads, **UNVERIFIED** price. Put both on the **2026-11-21** order.

---

# 8. Alliance selection

## 8.1 What this section does *not* do

**It does not restate the scouting system.** [`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) is the
authority and it already covers: what FMS publishes for free **[C]**, the **22-field gap schema**
(13 match + 9 pit) for the things free data never has, the staffing consequence, and
`tools/scouting-plan.py` (`free` · `schema` · `picklist`). It also carries the warning this section
is built on, verbatim:

> Rank order from free data reflects **scoring**, not reliability, defense, or driver skill.
> Fuse it with gap-scouting before drafting.

**This section covers only what happens on Saturday morning**: the mechanics, the ordering logic, and
the fact that you are far more likely to be *picked* than to *pick*.

## 8.2 The mechanics — get these right or lose your slot

**[C]** from the 2026 manual §10.6.1 and rules T601–T606. **Re-verify against the 2027 manual.**

| Item | Value | Rule |
|---|---|---|
| Top **8** ranked teams become ALLIANCE Leads; each picks 2 | | §10.6.1 |
| Break before selection | **8 minutes** after the last qual scores post | §10.6.1 |
| **Round 1 pick timer** | **45 seconds** | T605 |
| **Round 2 pick timer** | **1:30** | T605 |
| Round 1 order | descending, ALLIANCE 1 → 8 | §10.6.1 |
| Round 2 order | ascending, ALLIANCE 8 → 1 | §10.6.1 |
| Representatives | **1–3 STUDENTS**, must report to the ARENA **before selection starts** | **T601** — *violation: team is ineligible for the Playoff Tournament* |
| Adults | a non-STUDENT may attend **only** alongside **exactly two** STUDENTS | T602 |
| The mic | **only a STUDENT** may accept/decline, and **only one** | T603 — *violation: assumed to have declined* |
| Inviting | **only the ALLIANCE CAPTAIN** may invite | T604 |
| Timer expiry | ALLIANCE is skipped and revisited; if it is the last pick of a round, they receive the next highest-ranked unselected team | T605 |
| **Declining** | a team that declines **cannot be picked later and is ineligible as a BACKUP TEAM** | **T606** |
| BACKUP TEAMS | highest-ranked unselected teams are eligible | §10.6.3 |

**Three ways small teams lose here, all avoidable:**

1. **T601 — nobody shows up in time.** The penalty is *ineligibility for the entire playoff
   tournament*. Your representatives leave the pit **before the last qualification match finishes**,
   not after. Put it on the match-day clock as a hard event.
2. **T603 — the wrong person speaks.** Only a student, only one. Brief them: **one designated
   speaker, one designated backup, everyone else silent.**
3. **T606 — declining is nearly always wrong for a team like this.** Declining removes you from the
   playoff entirely *and* from the backup pool. There are legitimate reasons (a robot that genuinely
   cannot play, a safety issue) and they are rare. **Decide your decline policy on Thursday, in the
   pit, calmly — not at the microphone with 45 seconds on the clock.**

## 8.3 Building the pick list

**Timing:** Friday night or Saturday before selection, **45 minutes, capped.** A pick-list meeting
that runs two hours produces a worse list than one that runs 45 minutes, because the marginal hour is
spent re-litigating teams you will never reach.

**Inputs, in order:**

1. `python tools/scouting-plan.py picklist` — the free-data starting point
   ([`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) §5). **It is a starting point, not a ranking**: by
   design it has no reliability or defence input.
2. Your **gap-scouting** columns (the 22-field schema) — reliability, defence quality, cycle path,
   breakdown recovery, pit professionalism.
3. Your **failure log** (§5.1) — including what you saw break on *other* robots.

**Produce three lists, not one:**

| List | Length | Purpose |
|---|---:|---|
| **A. Ranked pick list** | 24 | if you are a captain (unlikely — §8.4) |
| **B. "Do not pick"** | short | §8.5 |
| **C. Compatibility notes** | per team in top 12 | *"pairs badly with us — same scoring zone"* |

**List C is the one small teams skip and it is where the value is.** A pick list is not a global
ranking of robot quality; it is a ranking of *robots that make our alliance better*. The best robot
at the event may be a poor partner for you if you both occupy the same field space or both need the
same game-piece source.

## 8.4 First pick vs second pick logic

| | **First pick** | **Second pick** |
|---|---|---|
| You are choosing for | **capability** — the highest expected points you can add | **fit and reliability** — the gap in the alliance |
| Weight most heavily | delivered points, consistency, cycle time | **reliability**, defence ability, "never breaks" |
| Ignore | pit polish, reputation | raw scoring, which is mostly gone by round 2 |
| The classic error | picking the highest-EPA robot that plays the same role you do | picking a scorer when what you need is a defender |
| `PF` says | §4.3: captains buy **average delivered points** — the crude number | §8: a single DQ **halves** pick probability. In round 2, reliability *is* the product |

**The second-pick heuristic that works [S]:** by round 2, the scoring robots are gone. Ask *"which
remaining robot most reduces the variance of our alliance?"* — usually a robot that never breaks,
plays clean defence, and has a reliable auto. A 100%-reliable robot that scores modestly beats a
70%-reliable robot that scores well, because a three-robot alliance's availability is the
**product** of three availabilities (`PF` §4.1's chain arithmetic, applied to teams instead of
mechanisms): three robots at 90% is **72.9%** of matches with a full alliance.

## 8.5 Who to avoid

| Avoid | Why | How you know |
|---|---|---|
| **Any robot with a DQ this event** | `PF` §8 **[C]**: measured, four seasons, 30,986 team-events | free FMS data |
| A robot that has not moved in ≥ 1 match | availability dominates everything | your scouts' "did it break" binary |
| A robot whose *cycle path* collides with yours | you will spend the match negotiating floor space | list C (§8.3) |
| A robot that needs the same game-piece source at the same time | same problem, worse | list C |
| A team whose drive team you saw arguing at the field | in-match comms failure is contagious across an alliance **[S]** | direct observation |
| A robot you cannot get a straight answer about in the pit | if they will not tell you their failure rate on Saturday, you will discover it in the semifinal | pit scouting (9 fields, `SCOUTING-PLAN.md` §3) |

**One thing that is *not* a reason to avoid a team:** a low rank at a **large** event. `PF` §11 — the
largest measured effect in the corpus — finds that at the same relative rank, a team is **3–20× more
likely to be picked at a sub-36-team event than at a 61+-team event**. Rank is heavily confounded by
field size and by schedule luck. **Availability and delivered points are the signal; rank is noise
with a signal in it.**

## 8.6 The realistic posture: you are being picked, not picking

Capacity §4.4 is blunt about the staffing: you have **3–5 scouts against a requirement of 6**, and
*"any strategy that depends on out-scouting the field is out of reach for this roster."* Combined
with `PF` §11's field-size effect, the honest planning assumption for a 15-student team is: **you
will be a second-round pick, not a captain.** Plan for that.

**What being picked actually requires** — and note that all four are things you already have to do:

1. **Be available.** §4.1: a DQ halves your pick probability, and the measured effect understates
   mechanical failure. Reliability is the pick strategy.
2. **Be legible.** Captains pick what they can *see* in the data. `PF` §4.3 **[C]**: captains buy
   **average delivered points** — which is the crude number your own scouts can measure. A robot that
   does one thing consistently is easier to pick than a robot that does three things sometimes.
3. **Be a known quantity.** Every strategy meeting in §6.2 is a sales call. The team that runs a
   crisp three-minute plan and then does exactly what it said is remembered by six other teams per
   match.
4. **Be findable on Saturday morning.** A one-page pit card — what we do, cycle time, auto, what we
   do **not** do, contact — handed to the top 8 captains on Friday evening. Costs one sheet of paper.

**The 30-second pitch**, for when a captain's scout appears at your pit:

> *"We [team #] score **X**, about **N** seconds a cycle, and we've done it in every match today —
> here's our match-by-match count. Our auto does **A** from position **P**. We don't do **Y**. We're
> happy to play defence and we've practised it. Anything you need us to be, tell us and we'll
> rehearse it tonight."*

Every clause is a fact you already have if you did §3.7, §5.1 and §6.5. **That is the argument for
this whole document: the reliability log and the cycle-time chart are not paperwork — they are the
pick pitch.**

---

# 9. The calendar this implies

From `04_competition_ops.yaml: fall_2026_calendar`, with the ones that cost money marked.

| Date | Action | $ |
|---|---|---|
| **2026-09-01** | **Recommission last year's robot. Start driving it — one hour, twice a week, forever.** (§2.4) | $0 |
| 2026-10-01 | First driver tryouts on last year's robot (§3.1) | $0 |
| **2026-09-24** | **Event preferencing opens. Field size first (`PF` §11), then the latest week (§3.2).** | — |
| 2026-10-15 | Tape the evergreen field outline on the shop floor; source carpet (§1.7) | $0–150 |
| **2026-11-12** | **Pre-Kickoff Virtual Kit Release — re-price Systemcore, the spares list and practice-robot option B** (§2.3) | — |
| 2026-11-10 | **Load-test all batteries; rank by internal resistance** (§7.3) | $0 |
| **2026-11-17** | Kit & Kickoff selection closes; **2nd technical mentor recruited by now** (capacity §6.4) | — |
| **2026-11-21** | **BOM order-by: 6 batteries, multi-bank charger, SB50s, 120 A main breaker, spare RSL** (§5.2, §7.5) | ~$500–700 |
| 2026-12-15 | Print two of every outside-the-perimeter 3D part; the printer is idle now and saturated in January (§5.2) | ~$20 |
| 2026-12 | Rehearse the pre-match checklist and the 6-minute repair on last year's robot until it is choreography (§4.2, §6.4) | $0 |
| **2027-01-09** | **KICKOFF** | — |
| 2027-01-12 | **Assign the practice-element build package to three first-years + one veteran owner** (§1.9) | ~$200–260 |
| 2027-01-19 | Practice elements done — the three from §1.6, nothing else | — |
| 2027-02-05 | **Final driver/operator pair selected; backup named and given 20% of hours** (§3.1) | $0 |
| ~2027-02-20 | Week Zero: self-inspect against the 2027 checklist (§4.9); drive-into-a-wall test (§4.7) | $0 |
| Event Thursday | Decline policy agreed in the pit, in writing (§8.2) | $0 |
| Event Friday PM | Pit cards to the top 8 captains; pick-list meeting, 45 min capped (§8.3–8.4) | $0 |

**Nine of the seventeen items cost nothing and eight of them happen before kickoff.** That is the
shape of this whole document.

---

# 10. Validation / dry run

## 10.1 Every number here reconciles to an authority

| Claim in this file | § | Reconciles to | ✅ |
|---|---|---|:---:|
| 54.9 veq-h drive practice | 3.2 | `team_capacity.yaml: hours.allocation.drive_practice` | ✅ |
| ~9 real driver hours to Week 1 | 3.2 | capacity §3.4, same ÷3.5 ×0.6 chain | ✅ |
| 13.4 h to Week 4 | 3.2 | 854 veq-h × 0.09163 ÷ 3.5 × 0.6 = 13.4 | ✅ |
| 9.7 pts per second at 8 s | 3.3 | `cycle-model.py --cycle 8` (90.5) − `--cycle 9` (80.8) | ✅ |
| 117 pts over 12 quals | 3.3 | 9.72 × 12 = 116.7 | ✅ |
| 90 veq-h per novel mechanism | 3.4 | capacity §5.2 route B | ✅ |
| $2,500 discretionary | 2.1, 7.2 | `team_capacity.yaml: budget_usd.robot_discretionary` | ✅ |
| Second robot = 60–100% of the budget | 2.1 | $1,500–2,500 ÷ $2,500 | ✅ |
| 6 batteries = $350–360 = 14% of budget | 7.2 | 6 × $58–60 ÷ $2,500 | ✅ |
| Spares $500 = 20% of budget | 5.2 | `team_capacity.yaml: budget_usd.spares_consumables` | ✅ |
| First-years are ideal field-reset labour | 3.4, 1.9 | capacity §2.4 (+31.4 net veq-h) | ✅ |
| Practice field does not consume the shop queue | 1.9 | capacity §5.2 route C | ✅ |

## 10.2 The internal cross-check that could have failed

**Does the practice programme fit in the hours it is allocated?** §3.6 specifies a 90-minute session
occupying 3.5 people = **5.25 veq-h per session**. The budget is 54.9 veq-h → **10.5 sessions**
before a Week 1 event, or ~15.7 hours of robot-moving time, which is exactly capacity §3.4's figure.
Ten sessions across the ~4 weeks the robot is drivable is **2–3 sessions a week**. ✅ **Consistent,
and tight** — it means a single cancelled practice is 10% of the season's drive practice.

**Does the checklist fit the match cycle?** §4.2 targets 4 minutes split across two blocks; §6.1
allocates T−20 and T−6. ✅ Consistent, with the caveat that the T−6 block must fit in a queue line,
which is why CONTROL and HUMAN — the two blocks needing no tools — are the ones placed there.

**Does the spares + battery + practice-field spend fit $2,500?** $500 spares + ~$500
batteries-and-charger + ~$400 practice field + ~$700 practice drivetrain = **$2,100**, against a
robot BOM whose floor is **$1,500** (`PF` §5.1, Everybot all-in). Total wanted **$3,600** against
**$2,500** available. ❌ **It does not fit — the overrun is $1,100.** This is a real, named conflict:
**the practice drivetrain (option B, §2.2) and the full spares list cannot both be bought at $2,500.**
The resolution is in §10.4. Reproduce it from
[`04_competition_ops.yaml`](04_competition_ops.yaml) `budget_reconciliation`.

## 10.3 Re-verify every rule number at kickoff — one command

Every rule cited here is **[C] for 2026** and **[S] for 2027**. Rule numbers move between seasons.

```bash
# Run from the repository root.
bash tools/probe-2027-manual.sh
bash tools/ingest-manual.sh
python tools/rule-inventory.py --season 2027 \
  --rules R102,R401,R404,R601,R602,R603,R604,R605,R606,R607,R612,R708,R709,T601,T602,T603,T604,T605,T606
python tools/teamupdate-diff.py --from 2026 --to 2027   # what changed
```

Then update **§4.2's checklist card** and **§8.2's mechanics table** — those are the two places where
a stale rule number does real damage. See also
[`../RULE-CHURN-WATCHLIST.md`](../RULE-CHURN-WATCHLIST.md) for which rules historically move.

## 10.4 The one conflict this document cannot resolve, stated plainly

§10.2 shows the recommended purchases total **$3,600** against **$2,500** — an overrun of **$1,100**.
**The ranking, in the order to cut [S]:**

| Rank | Item | $ | Cut it? |
|---:|---|---:|---|
| 1 | 6 batteries + multi-bank charger | ~$500 | **Never.** Brownout is a top-three failure mode and batteries are also a *safety* item |
| 2 | Spares list | ~$500 | **Never fully** — but it is compressible to ~$250 by spare-ing only what is outside the frame perimeter, which is the actual rule |
| 3 | Practice field, 3 elements | ~$400 | **Compressible to ~$150** by building only elements 1 and 3 of §1.6 and deferring element 2 to Week 3 |
| 4 | **Practice drivetrain (option B)** | ~$700 | **This is the cut.** Degrade to option D (last year's robot, $0) + option E (simulation, $0) |

Cutting ranks 2–4 as described recovers **$1,200** ($250 + $250 + $700), which closes the $1,100 gap
with $100 to spare. **So the honest recommendation for a $2,500 budget is: options D + E + F, not
option B.** §2.2 lists
option B as "recommended" because it is the right answer *if the money exists*. At this team's actual
budget it does not, and the fallback — last year's robot from September plus a simulator plus
finishing the real robot two weeks early — costs **$0** and delivers most of the driver hours.
**Option B becomes correct the moment a sponsor adds ~$1,000, and that is a concrete, specific,
$1,000 ask a business team can put in front of a sponsor** — see
[`05_business_awards_sustainability.md`](05_business_awards_sustainability.md).

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/team-ops/04_tuning_testing_competition_ops.md` | this document |
| `reference/team-ops/04_competition_ops.yaml` | its machine-readable companion — lists, costs, rule references, drills, calendar |

Nothing marked DONE was modified. [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md),
[`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md),
[`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md),
[`03_programming_stack.md`](03_programming_stack.md),
[`05_business_awards_sustainability.md`](05_business_awards_sustainability.md),
[`../bom/`](../bom/) and [`../awards/`](../awards/) were read and cited, not edited.

**Suggested new artefacts this document implies but does not create:** `logs/failures_2027.csv`
(§5.1 schema) and a printed, laminated copy of §4.2. Both are team artefacts, not repo files.

---

## Known limitations

- **BIOCORE's field, elements and rules do not exist yet.** Every field-element example is 2026
  REBUILT. §1.6's *reduction* — scoring structure, game-piece source, taped outline — is designed to
  be game-independent, but the specific TE part numbers, the lumber lists and the polycarbonate panel
  are 2026 artefacts and will not carry forward. **Re-derive §1.5 from the 2027 TE build instructions
  the week they are released.**
- **Every rule number is [C] for 2026 and [S] for 2027.** §10.3 is the re-verification command. The
  bumper gap in particular is **1.25 in (R401, 2026)** — an earlier draft of the companion YAML said
  1.5 in and was wrong; it has been corrected. Treat every other number here with the same suspicion.
- **Playoff turnaround times and timeout rules are UNVERIFIED.** The 2026 manual HTML export in this
  corpus does not contain a playoff match-schedule table or a timeout rule, so §6.4's "6 minutes" is
  a **planning number [S]**, not a rule. Read §10 of the 2027 manual and the
  `…_PlayoffAllianceCommunication.pdf` for your event tier before relying on it.
- **No public dataset of driver practice hours exists**, and this document does not invent one.
  `PF` §7.2 is explicit: *"nobody records it."* Every "elite teams get N hours" claim you encounter,
  including any this document might have been expected to supply, is **UNVERIFIED**. What is
  computable — your own ~9 hours, and the ~30 minutes of driving an event gives you — is what §3.2
  uses instead, and it is enough to make the argument.
- **§3.4's break-even is a break-even, not a prediction.** It tells you *how much* cycle improvement
  drive practice must buy to beat a mechanism. It does **not** tell you that N hours buys that
  improvement, because no learning-curve data exists for FRC drivers. §3.7's chart is the substitute:
  measure your own curve rather than assume one.
- **The 18 mΩ battery retirement threshold is [S]** and is not a FIRST or manufacturer figure. Use
  the *relative* ranking of your own batteries, which is defensible, rather than the absolute number,
  which is not.
- **All practice-field and practice-robot dollar figures are [S]** except the two verified unit prices
  (SB50 $6.60, RSL $70.00, battery $58–60, all **[C]** in the BOM files). Lumber and sheet-goods
  prices are regional and volatile; price them locally in November 2026.
- **Systemcore changes an unknown amount of §4.6 and §5.2.** The CAN-splitting advice assumes the
  5-port CAN-FD architecture documented in `03_programming_stack.md`; the spares list assumes a
  roboRIO-shaped electrical bill of materials; **Systemcore's price is UNVERIFIED**, which is why
  §2.3's practice-drivetrain option cannot be costed until after **2026-11-12**. Re-run §2.2 and §5.2
  once hardware is in hand.
- **The pit footprint (10 × 10 ft) is UNVERIFIED for 2027.** It is the modal FRC pit size **[H]**;
  confirm on your event's page before building anything dimensioned to it.
- **§10.4's conflict is real and unresolved by money.** The recommended purchases exceed the $2,500
  discretionary budget by ~$960. This document states the cut order rather than pretending the
  budget closes. If your budget differs, re-rank — but batteries stay at rank 1.
- **Everything about drive-team selection, drills, session structure, comms protocol and pit layout
  is [S].** It is designed to be *measurable* and *falsifiable by your own logs* (§3.7, §5.1), which
  is the honest substitute for evidence that does not exist. After one season of failure logs and
  D4 medians, replace these sections with your own data.

---

## Security note

Every source read for this pass was a local file in this project: the archived 2026 Game Manual and
Field Manual, the archived FIRST blog and Playing Field webpage snapshots, the Team Test Element
build instructions, and the project's own reference files and tools. All of it was treated as
**data**. The archived webpages and PDFs contained no text addressed to an AI assistant and no
attempt to issue instructions. No authentication was used or attempted, and no external endpoint was
contacted while writing this file. The two ChiefDelphi URLs cited were not fetched during this pass —
they are quoted second-hand from [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md), which
transcribed them in an earlier pass.
