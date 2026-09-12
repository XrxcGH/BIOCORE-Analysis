# The Small-Team Playbook — matching championship deliverables with 15 students and no money

**Purpose.** Everything else in this project measures one thing at a time: hours
([`02_TEAM_CAPACITY_MODEL`](reference/02_TEAM_CAPACITY_MODEL.md)), dollars ([`bom/`](reference/bom/)),
awards ([`awards/AWARD-ALIGNMENT`](reference/awards/AWARD-ALIGNMENT.md)), code
([`team-ops/03_programming_stack`](reference/team-ops/03_programming_stack.md)), AI
([`ai-integration/`](reference/ai-integration/)). This file is the **synthesis**: what a
~15-student, one-mentor, limited-budget team actually *does*, in what order, between today
(**2026-08-22**) and the first BIOCORE event — and what it deliberately does **not** do.

It is opinionated on purpose. Small teams do not fail from lack of information; they fail from
attempting the union of everyone's good ideas. Every section below tells you what to skip.

**Companion files** — this document *routes*, it does not restate. Every number here is traceable:

| Shorthand | File | What it is authoritative for |
|---|---|---|
| `CAP` | [`reference/02_TEAM_CAPACITY_MODEL.md`](reference/02_TEAM_CAPACITY_MODEL.md) + [`team_capacity.yaml`](reference/team_capacity.yaml) | **Hours, headcount, roles, budget.** Nothing here may contradict it |
| `PF` | [`reference/04_PREDICTIVE_FACTORS.md`](reference/04_PREDICTIVE_FACTORS.md) | Measured factor weights (drive practice 90, reliability 88) |
| `RUB` | [`reference/ACHIEVABILITY-RUBRIC.md`](reference/ACHIEVABILITY-RUBRIC.md) · [`05_RUBRIC_BACKTEST.md`](reference/05_RUBRIC_BACKTEST.md) | Kickoff-day scoring of strategy candidates |
| `MECH` | [`reference/bom/06_MECHANISM_CATALOG.md`](reference/bom/06_MECHANISM_CATALOG.md) + [`mechanism_catalog.yaml`](reference/bom/mechanism_catalog.yaml) | **Part costs, build/design/programming hours per mechanism** |
| `OPS` | [`reference/team-ops/01_championship_season_process.md`](reference/team-ops/01_championship_season_process.md) · [`04_tuning_testing_competition_ops.md`](reference/team-ops/04_tuning_testing_competition_ops.md) | Stage ledger, practice field, event ops |
| `SW` | [`reference/team-ops/03_programming_stack.md`](reference/team-ops/03_programming_stack.md) | Systemcore / WPILib 2027, simulation, swerve fork |
| `BIZ` | [`reference/team-ops/05_business_awards_sustainability.md`](reference/team-ops/05_business_awards_sustainability.md) · [`awards/AWARD-ALIGNMENT.md`](reference/awards/AWARD-ALIGNMENT.md) | Awards lanes, sponsorship, sustainability |
| `AI` | [`reference/ai-integration/`](reference/ai-integration/) — [`00_FIRST_AI_POLICY_VERIFIED.md`](reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md) is the **policy authority** | What AI absorbs, what it costs, what it breaks |
| `KICK` | [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md) · [`STRATEGY-RANKING-SYSTEM.md`](STRATEGY-RANKING-SYSTEM.md) | The 48 hours after 2027-01-09 12:00 ET |
| `SCOUT` | [`reference/SCOUTING-PLAN.md`](reference/SCOUTING-PLAN.md) | Scouting with 3–5 bodies |

**Evidence labels**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source held in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model output. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

> **Scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game (FIRST CANOPY season), kickoff
> **2027-01-09 12:00 ET**. **BIOBUZZ** is the FTC sibling (kickoff 2026-09-12); *Pollen*,
> *StarterBots* and *Skill Builders* are FTC things and appear nowhere in this file. BIOCORE's rules,
> field and scoring element are **not public as of 2026-08-22**. This document contains **zero
> game-specific claims** — it is a plan for the team, which is knowable today.

---

## §0 — The 60-second workflow

Run this before you argue with any number below. It regenerates the constants this whole file is
denominated in.

```bash
# Run from the repository root. On a fresh clone, run the corpus rebuild first
# (bash tools/rebuild-corpus.sh --fetch, then bash tools/rebuild-corpus.sh; see README.md).

# ---- 1. YOUR capacity. Substitute your real roster + real meeting schedule. (~2 s) --------
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week1
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week4

# ---- 2. THE ONE NUMBER. If your plan needs more mechanisms than this, the plan is wrong. --
python tools/capacity_model.py | grep -A1 "BINDING"        # expect: 2.00

# ---- 3. THE SLACK CHECK. At 15 h/wk into a Week 1 event this prints +0.0. ----------------
python tools/capacity_model.py | grep "SLACK IN THE WHOLE PLAN"

# ---- 4. Price a robot before you commit hours to it. Gate-fails over $2,500. -------------
python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown

# ---- 5. Awards: which lanes are even open to this roster. --------------------------------
bash reference/awards/kickoff_award_check.sh

# ---- 6. Scouting sized to 3-5 bodies, not 6. --------------------------------------------
python tools/scouting-plan.py --scouts 4

# ---- 7. OFF-SEASON ONLY (today): is the 2027 manual up yet? Is the vendor stack moving? --
bash tools/probe-2027-manual.sh          # expect: nothing, until 2027-01-09
```

**Read the output in this order:** `BINDING` (how wide the robot may be) → `SLACK` (whether the plan
has any reserve — it does not) → the BOM gate (whether you can afford what you drew).

---

## §1 — The gap, quantified

The honest comparison class is not "a championship team", it is "a championship team's *deliverables*".
You can match most of the deliverables. You cannot match the process that produces them, and pretending
otherwise is how small teams burn a season.

**Elite reference profile [S], assembled from `PF` §4–5 and `CAP` §9.2:** ~40 students, 4–6 technical
mentors, custom fabrication, a practice field, two or three robots (competition + practice + often a
programming chassis), $13,000–17,000 on the robot alone **[C]** as a first-hand district-mentor account
(`PF` §5.1: custom tank ≈ $13k, the same robot on swerve ≈ $17k).

| # | Elite deliverable | What it costs them **[S]** | The small-team equivalent | Cheaper / faster by | What you actually give up |
|---:|---|---|---|---|---|
| 1 | **Custom-fabricated robot**, CNC'd from scratch | $13k–17k · 1,500+ person-h · mill/CNC/lathe | **COTS-path robot**: KoP or COTS swerve + published mechanism designs | **~5–7×** cheaper; ~40% fewer fabrication hours | Bespoke geometry. You take the mechanism the field already solved, not the one only you could build |
| 2 | **3 mechanisms + endgame**, all reliable | 4–6 leads, 4 mentors, ~360 CAD+fab h | **1 novel mechanism done excellently** + 1 COTS-derived second (`CAP` §5.3) | Fits in 205 CAD+fab h | Ceiling. You will not be a #1 alliance captain at a 60-team event. You *can* be a first-round pick |
| 3 | **Second (practice) robot** | +$8k–13k, +1 fabrication cycle | **Simulation + a hardware-in-the-loop plank** (`SW` §7, Layer 5) | ~$0 vs ~$10k | Physical iteration on the real mechanism. Sim tunes control, not sheet metal |
| 4 | **Full practice field** | $5k–20k + a gym they own | **3 field elements, the ones your mechanism touches** (`OPS` §1.6, $300–900) | **~10–20×** cheaper | Full-field driving lines and true cycle timing. Buy the *interaction*, not the field |
| 5 | **Log replay + full telemetry** | 3–5 programmers, an established codebase | **AdvantageKit IO pattern from day one on a blank 2027 page** (`SW` §3) | Same capability, ~0 legacy cost | Nothing — this is the one line where 2027 hands you parity (see §3.4) |
| 6 | **6-scout full-field scouting** | 6–10 dedicated students | **3-scout crude scheme + scouting alliance + TBA** (`CAP` §4.4, `SCOUT`) | 3 bodies instead of 8 | Opponent modelling. You learn your partners, not the field. `PF` §4.3: captains buy *average delivered points* anyway |
| 7 | **Impact Award campaign** | ~150+ student-h, multi-year narrative | **Do not chase it.** Run 2 robot-award lanes + the free lanes (`BIZ` §5.1, §6.3) | 46 in-season h vs 150+ | The advancing award. `AWARD-ALIGNMENT` §5.1 is explicit that chasing it with an unsupported story is an anti-pattern |
| 8 | **Written design documentation** | Dedicated documentation students | **AI-assisted decision record + one-page handout** (`AI` 04 §3.2, ~9.5 h saved) | ~2× faster | Depth. The one-pager must still be defensible for 90 s without the paper |
| 9 | **20+ h of drive practice pre-event** | 2nd robot + own field + no travel | **~9 h at Week 1; ~24 h at Week 4** (`CAP` §3.4, `OPS` §2.2) | Free — it is a *scheduling* decision (§3.6) | Nothing, if you pick a Week 3–4 event. Everything, if you pick Week 1 |
| 10 | **Custom swerve, tuned over 3 seasons** | Institutional knowledge you cannot buy | **COTS modules, vendor or template code** — or **tank**, honestly (§3.3) | $2,032 cheapest credible vs building modules | Top-end agility. `CAP` §5.6: first-year swerve *is* your novel mechanism |

### 1.1 The three gaps that do **not** close, at any budget

Say these out loud in September so nobody is surprised in February.

| Gap | Why money does not fix it | Source |
|---|---|---|
| **`novel_mechanisms_max` = 2** | Derived four independent ways; +5 students moves it 2.0 → 2.0, +7 h/wk moves it 2.0 → 2.0. Only *machine capacity* and *outsourced fab* move it, and only to ~3 | `CAP` §5.2, §5.5, §9.1 |
| **Mentor unblock attention = 3.4 h/wk** | Cannot be bought quickly, does not scale with roster, gates all safety-critical work. **One extra technical mentor is worth more than five students** | `CAP` §6.2, §6.4 |
| **Zero slack in the build plan** | The eight mandatory lines consume all 599 veq-h. One failed prototype, one snow week, or one departing core student eats the whole reserve, because there isn't one | `CAP` §3.3 |

### 1.2 The gap that is smaller than folklore says

**[C]** `PF` §5.1: the 2026 Everybot cost **~$1,500 over the Kit of Parts**, needed *"only common
tools, a basic 3D printer, items purchased from your local hardware store"*, and produced **441 True
Everybots, 100 alliance captains and 21 event wins** — a **22% captaincy rate against a 21.8%
population base rate** for two-event teams. A cheap, pre-solved, well-executed robot performs at the
population average. That is the whole thesis of this document.

Against that: `PF` §5.3 measures the top pulling away — the **P90/P50 EPA ratio moved 1.38 → 2.35**.
The middle is not collapsing; the top is escaping. Aim at *being picked*, not at picking.

---

## §2 — The 80/20, ranked and opinionated

Ranked by **competitive result per hour**, using `PF`'s measured weights as the numerator and `CAP`'s
hour budget as the denominator. Do them **in this order**. Items 1–5 are worth more than everything
below them combined.

| Rank | Practice | Why it ranks here | Cost | Do it by |
|---:|---|---|---|---|
| **1** | **Pick your event by field size first, then the latest week available** | `PF` §11 — largest effect in the corpus: at equal relative rank you are **3–20× more likely to be picked at a sub-36-team event than at a 61+-team event** (2026 bottom quarter: 60.8% vs 3.1%). Week 4 over Week 1 then adds **+255 veq-h free** (`CAP` §7.4) | **$0** and one afternoon | **2026-09-24** (preferencing opens) |
| **2** | **Recruit a second technical mentor** | Moves the #1 constraint from 3.4 → 6.8 unblock h/wk. Worth more than five students | $0 | **2026-11-17** |
| **3** | **Train a third programmer, on the 2027 stack** | Programming is **79% pre-committed** before a single bug exists (`CAP` §3.2). A third programmer takes it to ~53% | $0, fall hours | 2027-01-09 |
| **4** | **Build the drivebase first and drive it while the mechanism is in CAD** | Drive practice is `PF`'s **highest-weighted factor (90)** and the budget funds only ~9 real seat-hours. This converts waiting-for-parts time into the top factor | $0 | d10–d14 |
| **5** | **One mechanism, done to reliability** | `PF` weights reliability **88**; a 3-link chain at 90% each is **72.9%** end-to-end (`PF` §4.1). Two excellent beats four adequate, arithmetically | It *is* the budget | — |
| **6** | **Copy a published design** (Everybot, Open Alliance, released CAD) | Converts *design* hours into *fabrication* hours. `CAP` §5.4: "a released design is not a workstream" — it costs ~⅓ of the 90 veq-h a novel mechanism costs | $0 | d2–d10 |
| **7** | **Simulation-first programming** | The largest equalizer available (`SW` §7). Every student develops on a laptop, 12 months a year, while the robot does not exist | $0 | **September** |
| **8** | **Log everything from day one** (WPILOG / AdvantageKit) | Converts robot-time debugging into desk-time debugging at ~10:1 (`SW` §3) — the exact trade a team with one robot needs | ~4 h setup | d0–d14 |
| **9** | **SysId on every powered mechanism the first day it moves** | ~20 min of robot time replaces days of guess-and-check PID (`SW` §4). Write the routine in **December** so it costs zero in January | $0 | December |
| **10** | **Two award lanes, sharing one artifact library** | `BIZ` §2.5 pairs the archetype to the award automatically; the shared library makes the SECONDARY lane nearly free (6–22 marginal h) | 34–60 student-h | rolling |
| **11** | **AI on the desk work, humans on the robot** | Frees ~30–60 veq-h across the season (§3.8), **all of which must be reinvested in drive practice** | ~$300–700/season, funded from business, **never** from the robot line | September |
| **12** | **Join a scouting alliance in the pits on Thursday** | Costs zero bodies, solves a structural 6-vs-3 shortfall (`CAP` §4.4) | 15 minutes | event day 1 |

### 2.1 What to consciously **SKIP** — this list is the more important half

| Skip | Why | Cite |
|---|---|---|
| **A third mechanism / an endgame add-on** | Workstream #4 does not fail loudly. It starves workstream #2 of its last 30% of reliability work, which roughly **halves your probability of being picked** | `CAP` §5.3, `PF` §8 |
| **First-year swerve *and* a Systemcore port *and* vision** | `CAP` §5.6, verbatim: this configuration "builds a drivebase and nothing else". It is the most reasonable-sounding bad plan available on kickoff day | `CAP` §5.6 |
| **Machining your own swerve modules** | "A mechanical rabbit hole that returns nothing on the field." Buy the module | `SW` §4 |
| **Writing your own scouting app** | Every hour there is an hour not spent on Systemcore, the tightest line in 2027. Use an off-the-shelf app | `AI` 03 §9 |
| **An AI video-scouting pipeline** | Team-number recognition from broadcast video is *"the step that fails"*, and everything downstream depends on it. **Do not start** | `AI` 03 §4, §8 |
| **The FIRST Impact Award** | 150+ h against a 46 h in-season budget, and retrofitting a story is a named anti-pattern. Run the free lanes instead | `BIZ` §5.1, §6.3 |
| **A full practice field** | Buy the 3 elements your mechanism touches. The other 90% of the field teaches you driving lines you will re-learn at the event anyway | `OPS` §1.6 |
| **Full 6-scout manual scouting** | Structurally impossible with 12 event-day bodies. Any strategy that *depends* on out-scouting the field should be scored down in `RUB` | `CAP` §4.4 |
| **Copying 6328's 2026 architecture** | Named explicitly: do not. It is built for a program with five programmers and eight years of libraries | `SW` §3 |
| **A 5th prepared award lane** | `BIZ` §5.3 "spreading thin". Four lanes, one artifact library, done | `BIZ` §5.3 |
| **AI-generated code that nobody on the team can explain** | Fails the FIRST attribution/judging posture *and* the safety posture. Student explanation rate target is **100%, non-negotiable** | `AI` 00, `AI` 05 §metrics |

### 2.2 The opinion, in one paragraph

**Your season is won in October and lost in February.** Every constraint that binds in February
(mentor attention, unsupervised leads, programmer depth, driver hours, event choice) is relaxable only
before kickoff, at zero dollars. Every constraint you *can* relax in February (money, parts) is ranked
last (`CAP` §7.1). So the correct posture from today is: **spend the fall buying capacity, spend
January spending it on one mechanism, and refuse the fourth workstream out loud on kickoff day.**

---

## §3 — Force multipliers, quantified

Each is scored on **what it returns against the 599 veq-h / $2,500 discretionary baseline** (`CAP`).

### 3.1 COTS-first fabrication

| Metric | Custom path | **COTS path** |
|---|---:|---:|
| Robot cost **[C]** `PF` §5.1 | $13,000–17,000 | **~$1,500–2,500** |
| Which constraint governs the season `CAP` §7.3 | **Money (#1)** | **Mentor attention (#1)** — relaxable for $0 |
| Tooling floor | mill/lathe/CNC | **bandsaw + drill press + 3D printer** |
| Design hours per mechanism | ~90 veq-h | ~30 veq-h (published design) |

**The real argument is not price, it is which constraint you are choosing to live under.** COTS puts
the binding constraint on something a second mentor fixes for free. Custom puts it on a $13,000
sponsor you do not have. **Multiplier: ~5–7× on dollars, ~3× on design hours.**

### 3.2 One mechanism done excellently

`PF` §4.1 arithmetic, restated because it is the whole game: a chain of *n* subsystems at 90%
individual reliability delivers **0.9ⁿ**. Three links = **72.9%**. Four = 65.6%. Meanwhile the
district-mentor account in `CAP` §9.2 nailed *"9 out of 10 subsystems perfectly on the first try"*
and landed in **the lower EPA percentile** because of the tenth.

| Robot shape | End-to-end reliability at 90%/link **[S]** | Matches out of 10 where the scoring path works |
|---|---:|---:|
| Drivetrain + 1 mechanism | **81%** | 8 |
| Drivetrain + 2 mechanisms | 72.9% | 7 |
| Drivetrain + 3 mechanisms + endgame | 59.0% | 6 |

**Multiplier: +2 working matches out of 10 for every mechanism you *don't* build.**

### 3.3 The swerve-or-not decision — decide this in **October**, not January

This is the single largest scope decision on the robot (`MECH`, `swerve_drivetrain`
`buy_vs_make_recommendation`), and it is a *capacity* decision, not a performance decision.

| | **COTS swerve** | **KoP chassis / tank** |
|---|---:|---:|
| Cost `MECH` (verified 2026-08-22) | $2,605 catalog · **cheapest credible $2,032** | KoP chassis **$1,600** · tank/WCD **$1,300** |
| Against `robot_discretionary` $2,500 | **Consumes 81–104% of it** | 52–64% |
| Programming hours `MECH` | **45 h** | 10–12 h |
| …as % of the 134.8 h programming line | **33%**, on top of a platform rewrite | ~8% |
| Motors / controllers | 8 / 8 | 4 / 4 |
| Tooling floor | bandsaw + drill press | KoP: hand tools · WCD: **mill/lathe** |
| Effect on `novel_mechanisms_max` | **First-year adoption: 2 → 1** (`CAP` §5.6) | none |

**The decision rule.** Adopt swerve in 2027 **only if all four are true**: (a) you ran swerve in 2026
and the same students are back; (b) you have three programmers, not two; (c) the modules are on a PO
by **2026-11-21** (`MECH` lead time 4 weeks, stockout risk **high**); (d) you accept that swerve *is*
your second workstream. Otherwise: **KoP chassis, and spend the difference on the mechanism and on
drive practice.** Note `MECH`'s own note — even *buying* modules, swerve costs 45 programming hours in
a year that is already a rewrite.

**One 2027-specific sweetener [C] `SW` §4:** on Systemcore **every CAN bus is FD-capable**, so the
250 Hz odometry path in CTRE's swerve API is available by default rather than 100 Hz. That improves
swerve if you run it; it does not change the capacity arithmetic above.

### 3.4 Simulation-first programming — the biggest equalizer, and 2027 makes it bigger

**[C]** `SW` §0: the roboRIO is gone; WPILib 2027 is a breaking rewrite — Java packages
`edu.wpi.first` → `org.wpilib`, C++ `frc::` → `wpi::`, **Java 25 / C++23 required**, NetworkTables v3
removed, and **Shuffleboard, SmartDashboard, PathWeaver, RobotBuilder and LabVIEW all removed**
([New for 2027](https://docs.wpilib.org/en/latest/docs/yearly-overview/yearly-changelog.html),
[Removed features for 2027](https://docs.wpilib.org/en/2027/docs/yearly-overview/removed-features.html)).
WPILib calls it *"the biggest control system update since the introduction of the cRIO."*

**Why this is the best news a small team has had in a decade:** every powerhouse's 8-year-old utility
library and roboRIO muscle memory is partially invalidated on 2027-01-09. They have a migration
project; you have a blank page. **But only if you spend this off-season on the 2027 stack, not the
2026 one.**

| Layer `SW` §7 | What it gives you | Cost | Robot needed? |
|---|---|---:|:---:|
| 1 · WPILib Simulation GUI (`./gradlew simulateJava`) | DS state, real controller on your laptop, simulated I/O | **$0, zero setup** | No |
| 2 · Physics sim (`FlywheelSim`, `ElevatorSim`, `SingleJointedArmSim`, `DCMotorSim`) | PID/FF approximately right **before the mechanism exists** | $0 | No |
| 3 · PhotonVision simulation | The whole pose pipeline debugged in December | $0 | No |
| 4 · Unit tests | Regression safety on a codebase 2 people maintain | $0 | No |
| 5 · **Hardware-in-the-loop plank** — one motor + encoder + spare controller bolted to a board | Real CAN, real encoder noise, real current limiting, real deploys | **~$0, you own the spares** | No |

**Quantified `AI` 01 §2:** simulation + unit tests is ranked the **#1 AI-assisted use** at
**18–30 h returned** against the 134.8 h programming line (13–22%), at **low risk** — a wrong test
fails loudly and never moves a motor. `SW` §7 states the structural case plainly: you get roughly
**one hour of robot access for every ten a powerhouse gets**, and log replay + sim converts robot-time
debugging into desk-time debugging.

**Multiplier: ~1 additional effective programmer, for $0.**

### 3.5 Borrowing published designs & Open Alliance participation

| Action | Return | Cost |
|---|---|---|
| Build a published mechanism (Everybot / released CAD) | Design hours ~90 → ~30 veq-h **[S]** `CAP` §5.4 | attribution + fab hours |
| Read Open-Alliance build threads weekly in Jan–Feb | Free failure-mode intelligence on the mechanism you chose | ~1 h/wk |
| **Publish your own build thread** | `BIZ` nudge N13: pre-season collaboration is judged evidence, and it is **the cheapest award material there is** | ~1 h/wk |
| Copy an architecture from the four repos in `SW` §10 (e.g. **2910** `2026CompetitionRobot-Public`, MIT) | Reusable `MotorIO`-based base subsystems, homing built in, clean sim package | reading time |

Licence discipline: the repos named in `SW` §10 are MIT/BSD; **YAGSL is LGPL-2.1** — different
obligations. FIRST's AI policy requires you to *"respect intellectual property rights and licenses"*
**[C]** (`AI` 00), and the same sentence covers borrowed CAD and code. Credit it in the README.

### 3.6 The event-week and field-size lever — the largest free thing in this document

```
+7 scheduled h/wk (15 -> 22), same Week 1 event : +220 veq-h   (at real burnout cost)
same 15 h/wk, Week 1 event -> Week 4 event      : +255 veq-h   (free)
```

Where the +255 lands (`OPS` §2.2) is the point: **drive practice +85 h** (≈9 → **≈24 real driver
hours**) and **integration/debug +50 h** — the two lines `PF` weights **90** and **88**. Competitive
cost, `PF` §10: the field is 24–38% stronger by Week 5, your own team improves 37–46%, net rank
percentile change **under 2 points**. The effects cancel.

**But field size dominates event week** (`PF` §11). **Filter on field size first; among surviving
events, take the latest.** This decision is made **2026-09-24 → 2026-11-17**, four months before
kickoff, and it outranks every mechanism decision made in January.

### 3.7 Off-season pre-building

The first-year training tax is **−73.5 veq-h** during build season (`CAP` §2.4) — six first-years net
**+31.4 veq-h before a Week 1 event**, about one good Saturday from one veteran. Paid in
September–December instead, it falls on hours with **no competing use**.

| Pre-build in the fall | Returns in January |
|---|---|
| Assemble a KoP/spare chassis and *drive it* | Driver hours against `PF`'s 90-weight factor, before the season |
| Wire a complete practice electrical board | The 49.9 h electrical line starts from a known-good reference |
| Build the HIL plank (`SW` §7 Layer 5) | Programmers stop competing for the robot |
| Cut and cover a spare set of bumpers | `MECH` `bumpers_frame` = **19 build h**, all of it schedulable in November |
| Write the `SysIdRoutine` into a template subsystem | ~20 min of robot time in Feb instead of days of tuning |

### 3.8 AI absorbing desk work — the honest ledger

**Policy first, and it is unambiguous [C]** (`AI` 00, the authority — quoted, not re-litigated):

> Teams are permitted to use Artificial Intelligence (AI) to assist in the creation of award
> submissions, handouts, writing robot code, etc. *FIRST* views AI resources as tools available to
> students in the same way that CAD programs, Programming Languages, and 3D printers are tools
> available for their use.

The one binding obligation is **attribution** — *"Essay created by Team XXXX and ChatGPT."* Adopt a
standing attribution line in the repo README and on every submission. And **[C]**: *"Judges should not
discredit a team who uses AI or rank them lower simply for using the tool."*

| Budget line (`CAP` §3.1) | veq-h | **Realistic AI saving [S]** | Source |
|---|---:|---:|---|
| Strategy / rules / game analysis | 25.0 | **−6 to −10** | `AI` 02 §6.3 |
| CAD + design | 74.9 | **−8 to −15** | `AI` 02 §6.3 |
| **Fabrication + assembly** | 129.8 | **0** | Chips are cut by humans |
| Electrical + pneumatics | 49.9 | −2 | |
| Programming | 134.8 | −20 to −40 realistic (77–137 h *if you do all ten uses*) | `AI` 01 §2 |
| Integration / debug | 84.9 | **0 to −3** | Debugging needs the robot in front of you |
| **Drive practice** | 54.9 | **0** | The top-weighted factor is untouched by AI |
| Awards / business / media | 44.9 | **−9.5** (with ~3 h reinvested into judge Q&A drilling) | `AI` 04 §3.2 |

**Season total: roughly 40–70 veq-h, ~7–12% of the season.** `[AUDIT 2026-08-22]` This is the number
to plan against, and it is now the agreed figure across the project: `AI` 00 §1.11a computes a
per-row **ceiling** of ≈106 h and states plainly that 40–70 h is a 40–65% realisation of it; `AI` 05
§8.2 uses the same range as its measurement target. Real, worth having, **not
transformative** — and `AI` 02 §6.3 states the counter-intuitive part explicitly: **those hours do not
raise `novel_mechanisms_max`**, because routes A and C still bind at 2. AI buys you *depth inside two
mechanisms*, not a third one.

**What AI does badly — read before budgeting** (`AI` 01 §4, 03 §8, 04 §8):

| Failure | Why it is worse in 2027 | Mitigation |
|---|---|---|
| **Hallucinated vendor APIs** — the #1 failure | Every 2027 vendor lib is in **alpha** (Phoenix 6 `v26.50.0-alpha-1`, REVLib `v2027.0.0-alpha-2`, PathPlannerLib `v2027.0.0-alpha-3`). Alpha APIs are **not in training data**; the model substitutes the 2026 API it knows. AdvantageKit's own package moved `org.wpilib.commands3` → `org.wpilib.command3` between alphas | **Compile within 60 seconds.** Paste the real API surface into context |
| **Inventing rule IDs, award names, deadlines, part numbers, prices, URLs, team numbers** | The BIOCORE manual is brand new in January; model output about it will be *worse* and equally confident | `tools/cite-check.py` on **every** rules answer |
| **Arithmetic over pasted tables** | — | Never let it compute. Make it write a query **you** run |
| **Confident prose from thin data** | — | Print *n* everywhere |
| **Displacing the learning** | — | **The one that actually matters.** Spot-check at PR review: can the student explain it? Target **100%** |

**Cost** (`AI` 05 §1.4): Tier 1 ≈ **$24–39/month** (~$192–312 over 8 months, **2.7%** of the $11,500
planning total). Recommended pattern: Tier 1 from September, add **one** burst seat on **kickoff
morning** for whoever does the most Systemcore migration, cancel it the week after your last event —
lands near **$700**, or 6.1%. **Fund it from the business/sponsorship line, never from
`robot_discretionary`** — $700 out of $2,500 is a swerve module.

---

## §4 — Three complete annual program budgets

All figures **[S]** planning estimates unless labelled. Fixed anchors: **season registration $6,500
[C]** — includes team number, Kit of Parts, award eligibility, and participation at **one Regional or
two District events** ([FIRST Cost & Registration](https://www.firstinspires.org/robotics/frc/cost-and-registration)).
**Regional teams playing a District event: +$1,000 [C], new for 2027.** Part prices are `MECH`,
verified against live vendor pages **2026-08-22** — re-run `reference/bom/recheck_prices.sh` before any
PO; FRC vendor prices moved mid-season in 2026.

> ⚠ **The Systemcore price is UNVERIFIED** as of 2026-08-22. Every tier below carries a placeholder
> line. This is a **hole in the budget, not a rounding error**. Re-check FIRST and vendor pages
> immediately after the **2026-11-12 Pre-Kickoff Virtual Kit Release**.

### 4.1 Tier A — $6,000 · "survival, with the registration offset"

**Read this first: $6,000 does not cover a season at list price.** Registration alone is $6,500. Tier A
is only reachable if a grant or sponsor covers registration in whole or part — a rookie/veteran grant,
a state or district STEM grant, or a single sponsor who pays the entry fee directly. Budget the
*offset*, do not pretend the fee is smaller.

| Line | $ | Notes |
|---|---:|---|
| Season registration **[C]** | 6,500 | |
| **less grant / sponsor-paid registration offset** | **−3,500** | **[S]** the assumption Tier A stands on. If it fails, Tier A fails |
| Kickoff Kit shipping (ground US/CA) **[C] 2026 ref** | 150 | 2027 TBA |
| Sales tax @ 7% **[S]** rate | 120 | **[C]** that 2026-27 tax practice changed |
| **Robot BOM over KoP** | **1,500** | Everybot-class floor **[C]** `PF` §5.1. KoP chassis + 1 published mechanism |
| Systemcore / control system | **UNVERIFIED** | Placeholder — see warning above |
| Spares + consumables | 300 | Below the 400–600 band; you will feel it |
| Prototype stock | 150 | Cardboard, plywood, scrap |
| Practice field elements | 300 | One element, the one your mechanism touches |
| Tools | 0 | **You use the school shop or the mentor's garage** |
| Software / AI | 200 | `AI` Tier 1, 8 months, nonprofit rate |
| Travel / food, local, no hotel | 300 | Parents drive; potluck pit food |
| **TOTAL** | **~6,020** | |

**What Tier A gives up:** the second event, all travel, spares depth, and any tooling growth. It is a
**one-event, one-mechanism, KoP-chassis season** — which `PF` §5.1 says still produces a 22% alliance
captaincy rate. It is not a bad season. It is a season with **zero financial reserve**, so a broken
gearbox in week 5 is a strategy change.

### 4.2 Tier B — $15,000 · **the recommended plan**

This is `CAP` §8.1's ~$11,500 planning composite plus a real reserve. **Fundraise against this number.**

| Line | $ | Notes |
|---|---:|---|
| Season registration **[C]** | 6,500 | one Regional **or two District** events |
| Second event / district-event fee for a Regional team **[C]** | 1,000 | new for 2027; buys the second competitive data point |
| Kickoff Kit shipping **[C] 2026 ref** | 200 | |
| Sales tax @ 7% **[S]** | 450 | |
| **Robot BOM over KoP — planning target** | **2,500** | **`robot_discretionary`, the number every design trade is scored against** (`CAP` §8.1). `tools/bom-builder.py` gate-fails above it |
| Systemcore / control system | **UNVERIFIED** | Placeholder. Reserve is where it comes from |
| Spares + consumables | 500 | `CAP` midpoint |
| Prototype stock | 300 | `OPS` stage 2 |
| Practice field elements | 700 | `OPS` §1.6 — 3 elements |
| Tools (incremental: blades, bits, taps, a second drill, safety glasses) | 500 | You already own bandsaw + drill press + 3D printer |
| Outsourced 2D fabrication account | 400 | `CAP` `tooling.outsourcing_budget_usd`. **Run one test order in December** |
| Software / AI | 700 | Tier 1 + one burst seat Jan–Apr (`AI` 05 §1.4) |
| Awards / media / print (handouts, pit display) | 250 | `BIZ` |
| Travel / food, local, no hotel | 1,200 | **[S]** `CAP` §8.1 |
| **Reserve (10%)** | **1,300** | **The line Tier A does not have.** Do not spend it before week 5 |
| **TOTAL** | **~16,500** → trim reserve/travel to land at **~15,000** | |

**Robot BOM at $2,500, priced from `MECH` (verified 2026-08-22):**

| Item | $ | Note |
|---|---:|---|
| KoP chassis (`kop_chassis`) | 1,600 | 12 build h · 10 programming h · hand tools |
| Bumpers + frame (`bumpers_frame`) | 257 | 19 build h |
| Over-bumper intake (`over_bumper_intake`) — **the one novel mechanism** | 380 | 16 build · 8 design · 4 programming h · 1 motor |
| Indexer / conveyor (`indexer_conveyor`) — the COTS-derived second | 411 | 20 build · 14 programming h |
| **Subtotal** | **2,648** | ~6% over the gate → drop the indexer to a passive hopper (`hopper`, $325, 2 programming h) → **$2,562**, or trim spares |

*(Note `MECH`'s `baseline_electrical_package` at $1,979 is **mostly KoP-covered** — `OPS` §2.3. Do not
double-count it against `robot_discretionary`, and do not assume it is free either. Reconcile it
against the actual KoP contents on **2026-11-12**.)*

**Swap-in if you run swerve:** `swerve_drivetrain` cheapest credible **$2,032** replaces the $1,600
KoP chassis (+$432) **and** costs +35 programming hours. At Tier B that fits on money and **does not
fit on hours** unless you have a third programmer. See §3.3.

### 4.3 Tier C — $30,000 · "two events, travel, and a practice robot"

| Line | $ | Notes |
|---|---:|---|
| Season registration **[C]** | 6,500 | |
| Second/third event | 4,000 | second Regional, or district events + playoff travel |
| Kickoff Kit shipping + tax | 700 | |
| **Robot BOM over KoP** | **5,000** | COTS swerve ($2,032–2,605) + 2 mechanisms + climber |
| Systemcore / control system + a **spare** control set | **UNVERIFIED** + 1,000 **[S]** | A spare control system is the single best reliability purchase at this tier |
| **Practice / programming chassis (second drivebase)** | 2,000 | Removes the robot-access constraint that §3.4 solves with software |
| Spares + consumables | 900 | Duplicate every single-point-of-failure part |
| Prototype stock | 600 | |
| Practice field elements | 1,500 | 5–6 elements; still not a full field |
| **Tooling step-up** | **2,500** | A CNC router moves `tooling_floor` from `bandsaw_drillpress` → `router_cnc`, unlocking `variable_hood_shooter` / `turret` class mechanisms in `MECH` — **and it is the only purchase that moves `novel_mechanisms_max`** (`CAP` §5.5, route C) |
| Outsourced fabrication | 1,000 | |
| Software / AI | 800 | |
| Awards / media / print | 500 | |
| Travel + hotel (one overnight event) | 3,000 | |
| **Reserve (10%)** | 3,000 | |
| **TOTAL** | **~33,000** → trim travel/tooling to land at **~30,000** | |

**Honest warning about Tier C.** Money is constraint **#5** (`CAP` §7.1). Tripling the budget without
adding a **second technical mentor** and **two more unsupervised student leads** buys a nicer version
of the same two mechanisms. `CAP` §9.2 back-tests exactly this case: a team with ~10 students, ~4
mentors and a **~$20k budget** attempted 10 subsystems, nailed 9, and landed in *"the lower EPA
percentile"*. **Spend Tier C's marginal dollars on the CNC router and the spare control system, and
its marginal *effort* on mentor recruitment.**

### 4.4 Fundraising milestones to hit Tier B

| By | Milestone | Cite |
|---|---|---|
| 2026-09-15 | Sponsor packet + one-pager refreshed; last year's sponsors thanked **before** being asked | `BIZ` |
| 2026-09-30 | **$6,500 committed or credibly pledged** — registration must be payable at selection | — |
| 2026-10-31 | Grant applications filed (school/district/corporate STEM). `AI` 04 §5: ~6 h of boilerplate now saves ~1.5 h per application | `AI` 04 |
| **2026-11-17** | **Registration paid.** Kit & Kickoff selection closes | **[C]** |
| **2026-11-21** | **BOM order-by** for long-lead electrical/drivetrain | **[S]** `tools/bom-builder.py` |
| 2026-12-15 | $2,500 robot discretionary in the account, unspent | `CAP` |
| 2027-02-01 | Travel/food funded; reserve untouched | — |

---

## §5 — Headcount models: covering 16 functions with 8, 15, or 30 students

`CAP` §4.1 enumerates **16 functions**; raw minimum bodies with **no sharing is 26**. Sharing is
mandatory at every roster size below 26 — the only question is *which* shares are safe.

### 5.1 The three rosters, side by side

Effective hours computed the same way for all three (`CAP` §2.6 method: nominal × **0.352** at 15
scheduled h/wk to a Week 1 event). `novel_mechanisms_max` re-derived by `CAP` §5.2's three routes.

| | **8 students** | **15 students (baseline)** | **30 students** |
|---|---:|---:|---:|
| Nominal person-hours to Week 1 | 908 | 1,704 | 3,407 |
| **Effective veq-h [S]** | **~320** | **599** | **~1,199** |
| Core technical (unsupervised leads) **[S]** | 3 | 5 | 9–10 |
| …of which mechanical, after 2 programmers | 1 | 3 | 7–8 |
| Route A — leads, minus drivetrain | **1** | 2 | 6–7 |
| Route B — CAD+fab hours ÷ 90 | 1.2 | 2.27 | 4.6 |
| Route C — **single-machine shop queue** | 2 | 2 | **2** |
| **BINDING `novel_mechanisms_max`** | **1** | **2** | **2** ← route C, unchanged |
| Event-day bodies (assume 80% attend) | 6 | 12 | 24 |
| Scouts available during a match cycle | **0–1** | 3–5 | 12+ |
| Award lanes that fit | 1 + free lanes | 2 + free lanes | 3 + Impact plausible |

**The 30-student row is the important one.** Doubling the roster does **not** widen the robot —
route C (one bandsaw, one drill press, one 3D printer, one mentor qualified on the mill) binds at 2
regardless (`CAP` §5.5). Thirty students buys **depth inside two mechanisms**, a real scouting
operation, and a third award lane. To widen the robot you must buy **machine capacity or outsourced
fabrication** (§4.3's CNC router line), or add mentors.

### 5.2 Org chart — 8 students

```
                        MENTOR (drive coach, safety, ordering)
                              |
        +---------------------+---------------------+
        |                     |                     |
   CORE A                 CORE B                CORE C
   drivetrain +           THE mechanism         controls / Systemcore
   frame + bumpers        + CAD                 + auto + telemetry
   + electrical           (also OPERATOR)       (also pit code)
   (pit chief)                |                     |
        |                     |                     |
   VET D (fabrication,   VET E (DRIVER from    F/G/H first-years:
   safety captain)       week 3, fabrication)  fab support · media/awards ·
                                               human player · 1 scout
```

| Function | Who | Note |
|---|---|---|
| Strategy | Core B + C + mentor | Kickoff weekend only |
| Scouting | **Effectively none** | Join a scouting alliance on day 1, or use TBA + one qualitative scout post-quals. This is not optional at 8 |
| Awards | One first-year + mentor | **Judges Award + Rising All-Star** are the correct targets — near-zero materials (`BIZ` §6.3 lanes 3–4) |
| Logistics | **Parents, entirely** | `CAP` §4.3: highest-leverage delegation available, costs zero student hours |

**The 8-student rule:** *one* novel mechanism, KoP chassis, no vision, no swerve. Anything else and
route A drops you to zero.

### 5.3 Org chart — 15 students (the baseline; full roster in `CAP` §4.2)

```
                     MENTOR (3.4 h/wk of unblocking -- the binding constraint)
                              |
   +----------------+---------+---------+----------------+
   |                |                   |                |
 WS1 DRIVETRAIN   WS2 MECHANISM      WS3 SOFTWARE     BUSINESS/AWARDS
 Core B (lead)    Core A (lead)      Core D (lead)    Vet I (lead)
 + Vet F (elec)   + Core C (CAD/     + Core E (auto,  + FY M (media)
 + Vet G (fab)      integration)       telemetry)     + FY O (research)
 + FY J,K,L                                           + FY N (scouting sys)
        \               |                    /
         +--------- Vet H: DRIVER from week 3 ---------+
```

**Three workstreams. Not four.** (`CAP` §5.3.) The fourth — a second scoring mechanism, an endgame,
or a vision-based pose stack — starves WS2 of its reliability work.

**Safe doublings** (`CAP` §4.3): CAD↔fabrication · electrical↔pit crew · safety captain↔pit crew ·
awards↔scouting · media↔outreach · auto programmer↔scouting data owner · **logistics→parents**.
**Unsafe, and they fail on match day:** driver↔operator · drive team↔scouting · pit crew↔scouting ·
lead programmer↔sole mechanical fixer · Impact presenter↔pit crew · **drive coach↔any student role**.

### 5.4 Org chart — 30 students

```
                 MENTOR TEAM (2-3 technical + 1 business)   <- recruit these, not more students
                              |
  +-----------+-----------+---+-------+-----------+-----------+
  |           |           |           |           |           |
 WS1         WS2         WS3      SCOUTING     AWARDS      OUTREACH
 drivetrain  mechanism   software  8-10 stu.   3-4 stu.    4-5 stu.
 5-6 stu.    6-7 stu.    4-5 stu.  (full 6-    (3 lanes,   (Impact
 (+ practice (+ a real   (+ vision  scout       incl.       becomes
  chassis)    prototype   + a 3rd   coverage +  Impact)     plausible)
              cell)       programmer) strategist)
```

At 30, the marginal student's best use is **not** a fourth mechanism (route C forbids it). It is:
**full 6-scout coverage** (worth more than a mechanism at a large event, `PF` §11), a **real
prototyping cell** that iterates while WS2 fabricates, and the **Impact Award** becoming a
defensible lane rather than an anti-pattern.

### 5.5 Which roles AI can partially absorb

| Function | AI absorbs | Human must still | Net **[S]** |
|---|---|---|---|
| Rules / manual reading | Ingest, index, extract constraints, generate the scouting schema on kickoff day | **Decide.** Verify every rule ID with `tools/cite-check.py` | −6 to −10 veq-h |
| CAD / design | Repetitive parametric parts, DFM review, mass estimates | Layout, the actual mechanism concept | −8 to −15 veq-h |
| **Fabrication** | **Nothing** | Everything | **0** |
| Programming | Sim + unit tests (#1 use), the Systemcore port, subsystem scaffolding, log→report | Compile in 60 s; review every symbol against vendor docs; own the design | −20 to −40 veq-h |
| Scouting admin | Schema design, post-quals summaries, prematch briefs | Watch the matches. Enter the data | frees ~1 body |
| Awards / business | Criteria gap analysis, outline, structural critique, character-budget surgery, **mock judge Q&A** | **Write it.** Model never rewrites student prose | −9.5 h, ~3 h reinvested |
| Documentation / KB | Meeting notes → decision record, onboarding docs | Capture must be someone's **role**, not a virtue | ~5 h over the build |
| **Drive practice** | **Nothing** | Everything | **0** |

**The measurement that matters** (`AI` 05): *hours reinvested* — drive-practice hours logged versus the
54.9 h budgeted. Hours saved at a desk are only a win if they show up on the practice field.

---

## §6 — The off-season plan: 2026-08-22 → 2027-01-09

~20 weeks, no game, no deadline pressure — and **every top-ranked constraint is relaxable only here**
(`CAP` §7.5). Dates marked **[C]** are official; the rest are this plan's own deadlines.

### 6.1 The eight dates that bind

| Date | Event | Consequence of missing it |
|---|---|---|
| **2026-09-24 12:00 ET** **[C]** | Kit & Kickoff registration + **Event Registration Round 1 preferencing opens** | You take leftover event slots — i.e. you lose the §3.6 lever, the largest free thing in this document |
| 2026-10-29 12:00 ET **[C]** | FLA / WFFA submission portal opens | — |
| **2026-11-12** **[C]** | **Pre-Kickoff Virtual Kit Release** | Last input before BOM commitment. **Re-check the Systemcore price here** |
| **2026-11-17 12:00 ET** **[C]** | **Kit & Kickoff selection closes** · all registration closes | KoP order fixed. Registration not paid = no season |
| **2026-11-21** **[S]** | **BOM order-by** for 4–6-week-lead items (`tools/bom-builder.py`) | Long-lead electrical/swerve arrives after you needed it |
| 2027-01-09 12:00 ET **[C]** | **KICKOFF** — game reveal, Game Manual V1 | — |
| 2027-02-04 15:00 ET **[C]** | FIRST Leadership Award + Woodie Flowers Finalist close | Two free lanes gone (`BIZ` §6.3 — neither is blocked by the one-award-per-event rule) |
| 2027-02-11 15:00 ET **[C]** | FIRST Impact Award due | Not chased at this roster size (`BIZ` §5.1) |

### 6.2 Month by month

#### AUGUST 2026 (from today) — decide the posture

| Do | Owner | Why |
|---|---|---|
| Read `CAP` §5 and §7 with the whole leadership team. **Say `novel_mechanisms_max = 2` out loud** | mentor + core | Every January argument is pre-settled here |
| Start the **second-mentor** search: alumni, parents in trades/engineering, the sponsor's shop floor | mentor | Constraint #1; 12 weeks of lead time |
| Install **WPILib 2027 alpha** on one machine; compile and *simulate* a skeleton project | Core D | `SW` §0.4: "one mentor-hour a week Sept–Dec and you walk into kickoff fluent in the API everyone else meets on January 9" |
| Open the sponsor stewardship loop: thank last year's sponsors **before** asking | Vet I | `BIZ` |
| Start the **event shortlist** — historical field sizes from TBA (`tools/tba_*.py`) | mentor + Core E | `PF` §11 is the largest measured effect in the corpus |

#### SEPTEMBER 2026 — infrastructure and the event decision

| Do | Owner | Deadline |
|---|---|---|
| **Event preferencing: field size first, then latest week** | mentor | **2026-09-24 [C]** |
| Apply for the nonprofit/school AI rate (~3 min, saves ~$200/season); GitHub Education for every student | mentor | `AI` 05 §1.5 |
| Stand up the repo: WPILib 2027 alpha skeleton, Spotless, CI, `CLAUDE.md`, **AI attribution trailer check** | Core D | `AI` 05 §3, template at `reference/ai-integration/templates/frc-robot-CLAUDE.md` |
| Adopt the team AI policy (template: `reference/ai-integration/templates/team-ai-policy.md`) and check your **district's** policy — usually stricter than FIRST's | mentor | `AI` 00 |
| Programmer #3 recruited and started on the sim ladder | Core D | `CAP` §3.2 |
| $6,500 registration committed or credibly pledged | Vet I | 09-30 |
| **Watch the safety page weekly** — the Safety Animation window likely opens ~Oct **[H]** | Vet I | `BIZ` §6.3 lane 7 |

**Programming curriculum, weeks 1–4** (`SW` §9): every step produces something that *runs and can be
seen*, and **nothing requires robot access**. Zero-to-Robot → simulate the example → a subsystem with
an IO layer → a physics-sim mechanism → a unit test that fails for the right reason.

#### OCTOBER 2026 — build the practice apparatus

| Do | Owner | Why |
|---|---|---|
| **Build the HIL plank**: one motor + encoder + spare controller + spare PDP path on a board | Core D + a first-year | `SW` §7 Layer 5. Real CAN, real encoder noise, real deploys — the three things sim cannot give you |
| Assemble/refurbish a spare chassis and **start driver practice on it** | Vet H + Core B | `PF` factor #1, weight **90** |
| Prove the AI automations run **unattended for a month** before depending on them | mentor | `AI` 05 §1.5 |
| Write the **off-season robot** plan: one mechanism, on the 2026 game, start to finish in 5 weeks | Core A | Rehearses the exact January loop with no consequences |
| Safety Animation, if the window is open | Vet I + FY M | ~20 h, **zero build-season hours** |
| Draft the **judged-award artifact library** skeleton (`BIZ` §3.9) | Vet I | Off-season hours are outside the 599 h model |

#### NOVEMBER 2026 — the commitment month

| Date | Do | Cite |
|---|---|---|
| Nov 1–11 | Finalize the mechanism-archetype shortlist against `MECH` and `RUB`. **Price three candidate BOMs with `tools/bom-builder.py` and see which gate-fail** | `RUB` §9 |
| Nov 1–11 | **Swerve decision, final** (§3.3). Write it down. It is not reopened in January | `CAP` §5.6 |
| **Nov 12 [C]** | **Pre-Kickoff Virtual Kit Release.** Reconcile the KoP against `MECH`'s `baseline_electrical_package`. **Re-check the Systemcore price and re-check the vendor-library readiness table** (`SW` §0) | `SW` §0 |
| **Nov 17 [C]** | **Kit & Kickoff selection closes. Registration paid.** Second technical mentor onboarded by today | `CAP` §6.4 |
| **Nov 21 [S]** | **BOM order-by** for 4–6-week-lead items: swerve modules (**stockout risk high**), motor controllers, long-lead electrical | `MECH` |
| Nov 30 | Off-season robot drives. Bumpers cut and covered for the spare chassis | — |

#### DECEMBER 2026 — rehearse January

| Do | Why |
|---|---|
| **Run one test order through the outsourced-fabrication account** ($400 budgeted) | Relaxes constraint #4. Discovering the vendor's file requirements in February costs 2 weeks |
| Write `SysIdRoutine` into the template subsystems | ~20 min of robot time in Feb instead of days of PID guessing (`SW` §4) |
| **Full kickoff dry run**: score last year's game with `tools/score-strategy.py`, build a BOM, gate-check it, present it in 10 minutes | `KICK`. The muscle you need on d0–d2 |
| Vision decision: PhotonVision **[C]** is prerelease-only for 2027 with **no vendordep** as of 2026-08-22, and **ChoreoLib and maple-sim have no 2027 story at all**. Re-check; if still absent in December, **cut vision from the plan** | `SW` §0, §6 |
| Promote 2 contributing veterans to unsupervised-lead status — give them the off-season robot's last mechanism, alone | `CAP` §7.5, constraint #2 |
| Pay down the first-year training tax: 6 first-years trained now cost **−73.5 veq-h** in January if you don't | `CAP` §2.4 |
| Award drafts opened: FLA nominations, WFFA student essay | `BIZ` §6.3 lanes 5–6 |

#### JANUARY 1–8, 2027 — the last week

| Do |
|---|
| **Re-check the vendor-library table one final time** (`SW` §0). Alpha → beta status will have moved |
| Print the kickoff-day kit: `RUB` scoring sheets, `KICK` agenda, blank BOM template, the `novel_mechanisms_max = 2` sign for the wall |
| Confirm `tools/probe-2027-manual.sh` and `tools/ingest-manual.sh` run clean |
| Add the burst AI seat **on kickoff morning, not before** (`AI` 05 §1.5) |
| Shop cleaned, stock inventoried, 3D printer running a test print, bandsaw with a fresh blade |

### 6.3 The off-season scoreboard

By 2027-01-08, these should be true. Each maps to a constant in `team_capacity.yaml`.

| # | Check | Moves |
|---:|---|---|
| 1 | Second technical mentor confirmed | `mentor_unblock_hours_per_week` 3.4 → 6.8 |
| 2 | Three programmers, all of whom have deployed to Systemcore or its simulator | programming utilisation 79% → ~53% |
| 3 | Five unsupervised leads (2 newly promoted) | route A holds at 2, does **not** collapse to 1 |
| 4 | Event chosen: smallest credible field, latest week | +255 veq-h, +3–20× pick probability |
| 5 | Registration paid, $2,500 discretionary banked and unspent | gate check passes |
| 6 | Long-lead parts ordered 2026-11-21 | no week-3 stockout |
| 7 | Driver has ≥10 h of seat time **before kickoff** | doubles the season's practice total |
| 8 | Outsourced-fab account tested with a real order | route C relaxable |
| 9 | Sim + HIL plank + logging working on a skeleton project | robot-access constraint neutralized |
| 10 | FLA/WFFA drafts open; artifact library skeleton exists | ~25 h moved out of the in-season budget |

**If you hit 7 of 10 you have bought more competitive result than any decision made on kickoff day.**

---

## §7 — The BIOCORE build season: Jan 9 → Week 1

Day-numbered from **d0 = Saturday 2027-01-09**. Hours per stage are `OPS` §2.1, which repartitions
`CAP` §3.1's eight mandatory lines — **they sum to 599.1 because there are no spare hours**.

**How to read the AI column.** Everything in it is *desk work that would otherwise consume a student
hour*. Everything in the human column is either (a) a decision, (b) something physical, or (c)
something a judge will ask a student to explain. FIRST permits the AI column **[C]**; the attribution
line is mandatory (`AI` 00).

| Day | Date | Stage / milestone | **AI does this** | **Humans do this** | veq-h |
|---:|---|---|---|---|---:|
| **d0** | Sat Jan 9 | **KICKOFF 12:00 ET.** Manual V1 drops | `probe-2027-manual.sh` → `ingest-manual.sh`; rule inventory; first-pass constraint extraction; **generate the scouting schema** | Watch the reveal together. Read the manual **yourselves** — pass 1 is human, no exceptions | 8 |
| d1 | Sun Jan 10 | Strategy convergence | Score whiteboard candidates with `score-strategy.py`; draft the cycle model | **Decide the archetype.** Write `novel_mechanisms_max = 2` on the board and enforce it | 6 |
| **d2** | Mon Jan 11 | **Robot spec frozen (`OPS` §3.4)** · prototyping opens | Price 3 candidate BOMs; run the `bom-builder.py` gate | Mentor + 3 leads sign the spec. **The pairing to an award lane is now automatic** (`BIZ` §2.5) | 4 |
| d2–d10 | Jan 11–19 | **Prototyping** — cardboard, plywood, scrap | DFM review of sketches; motor/gearing math via `reference/ai-integration/calculators/` | **Build the ugly version.** Touch the game piece. This is the only week iteration is cheap | 47 |
| **d4** | Wed Jan 13 | **Q&A opens [C]** | Draft questions; watch the Q&A feed daily (`tools/frc_qa_scrape.py`) | Ask the ones that change your design. Verify every rule ID with `cite-check.py` | — |
| d5–d25 | Jan 14–Feb 3 | **Design / CAD** (3–4 people) | Repetitive parametric parts; DFM pass; BOM roll-up; mass estimate | Layout. The mechanism concept. **The design review** | 59.9 |
| **d7** | Sat Jan 16 | **Drivebase moving under its own power** | Deploy pipeline, logging on from hour one | **DRIVE IT.** Vet H starts seat time now, not in week 5 | — |
| d10 | Tue Jan 19 | **Prototype cut line** | Summarise which prototype won and why → into the decision record | **Kill the losing prototype.** Do not carry two | — |
| d14 | Sat Jan 23 | Mechanism v1 in CAD; **SysId on the drivetrain** | Log → engineering report | 20 min of robot time replaces days of tuning | — |
| d20–d45 | Jan 29–Feb 23 | **Manufacture** ($2,500 BOM lands here) | Cut lists, drill schedules, the outsourced-fab order package | Every chip. AI absorbs **0%** of this line — it is the largest one | 74.8 |
| **d25** | Wed Feb 3 | **CAD freeze.** Design review gate | Diff the CAD against the frozen spec; flag scope creep by name | **Say no to the fourth workstream, again** | — |
| **d26** | **Thu Feb 4 [C]** | **FLA + WFFA close 15:00 ET** | Structural critique of the student's WFFA draft; character-budget surgery | Student writes it. Mentor writes the FLA. **Submit Wednesday, not Thursday** | 6 |
| d28 | Sat Feb 6 | Mechanism v1 on the robot | | Integration. Everything is 3 mm off; that is normal | — |
| d33 | Thu Feb 11 | *(FIA deadline — **not chased**, `BIZ` §5.1)* | — | Nothing. This is a deliberate skip | — |
| d35–d50 | Feb 13–28 | **Assembly + wiring** | Wiring diagram, label sheet, CAN ID map | Wire it **once, properly**, not at 11 pm. Electrical owner is the pit-crew owner | 79.9 |
| d0–d60 | Jan 9–Mar 10 | **Programming — 134.8 h, the tightest line** | Sim + unit tests (#1 use); Systemcore port; subsystem scaffolding; log→report; code review for classic FRC bugs | **Compile within 60 s of every generated line.** Own the architecture. Explain it to a judge | 134.8 |
| **d38** | Tue Feb 16 | **One-page handout drafted** (`BIZ` N09) | Criteria gap analysis; outline from raw material | Front thesis, back annotated photo. Students must defend it for 90 s without the paper | 8 |
| d40–d60 | Feb 18–Mar 10 | **Integration / debug / reliability** — `PF` weight **88** | Log analysis; failure-mode triage lists | The robot must be in front of you. AI absorbs **~0** here | 84.9 |
| **d42** | **Sat Feb 20** | **WEEK ZERO — 6.00 weeks exactly from kickoff** | Prematch brief generation (`tools/prematch-brief.py`) | **Play matches.** Find the failures now, while it is free | — |
| d45–d70+ | Feb 23–Mar 20+ | **Drive practice + tuning** — `PF` weight **90** | Nothing. **Zero.** This line is untouchable by AI | 4 people per session. ~9 real driver hours at Week 1; ~24 at Week 4 | 54.9 |
| **d49** | Sat Feb 27 | Pit display assembled; rehearsals 2–3 | Mock judge Q&A drill (12-min timed, hostile-but-fair) | Answer out loud, alone, no notes. **The highest-value 3 h in the award lane** | 8 |
| d50 | Sun Feb 28 | **Robot done. Spares bagged. Tool crate packed** | Pack list, spares checklist | The scouting alliance pitch, rehearsed | — |
| **d53** | **Wed Mar 3** | **WEEK 1 EVENTS OPEN** | Post-quals summaries; pick-list arithmetic | Drive. Scout 3 robots crudely. Update the reliability scoreboard **between every match** | — |

### 7.1 The four gates — pass or re-scope, no third option

| Gate | Day | Pass condition | If it fails |
|---|---:|---|---|
| **G1 Spec** | d2 | ≤2 novel mechanisms; BOM ≤ $2,500; tooling floor ≤ `bandsaw_drillpress` | Cut a mechanism. Not "start and see" |
| **G2 Prototype** | d10 | One prototype demonstrably touches the game piece and repeats | Fall back to the published/Everybot-class design. **Decided in advance, not debated** |
| **G3 CAD freeze** | d25 | Every part drawn, sourced, and either cut or ordered | Simplify the mechanism, not the schedule |
| **G4 Robot complete** | d50 | Drives, scores, survives a 20-match dry run | You are shipping a robot you have not driven. Cancel scope, not practice |

### 7.2 The rule that protects the whole calendar

**Drive practice is the last line in the budget and the first thing consumed by overruns in the seven
lines above it** (`CAP` §3.4, validated against a real driver's account: *"in our first comp I was not
actually driving."*). So: **from d45, drive practice is a fixed appointment, not a residual.** If the
robot is not ready, you drive the spare chassis. If the mechanism is not on, you drive without it.

---

## §8 — Failure modes, and the countermeasure for each

Ranked by how often they end a small team's season, with the specific instrument that catches each.

| # | Failure mode | What it looks like | Countermeasure | Detected by |
|---:|---|---|---|---|
| **1** | **Scope: the fourth workstream** | "It's just a small climber." WS2 loses its last 30% of reliability work, halving pick probability | `novel_mechanisms_max = 2` written on the wall on d0; **G1 gate at d2** | `RUB` A2 (weight 85), `tools/bom-builder.py` gate |
| **2** | **First-year swerve + Systemcore + vision** | An entirely reasonable plan that **produces a drivebase and nothing else** | Swerve decided in **November** (§3.3), not January. Vision cut in December if PhotonVision 2027 is still prerelease | `CAP` §5.6 |
| **3** | **Losing one unsupervised lead** | Graduation, burnout, a competing commitment. `novel_mechanisms_max` drops **2 → 1** — the only perturbation in `CAP` §9.4 that moves it | Promote **two** spare leads in the fall. Treat this as a named schedule risk, not a rounding error | `CAP` §9.4 |
| **4** | **Programmer saturation** | 2 programmers, 79% pre-committed, then a bug appears. Everything queues behind one person | Third programmer by January (§6.2). AI on sim/tests/port, **not** on architecture | `CAP` §3.2 |
| **5** | **No drive practice** | ~9 real seat-hours against `PF`'s highest-weighted factor. Discovered at the event | Week 3–4 event (+85 h to this line). Drivebase by **d7**. Fixed appointments from d45 | `CAP` §3.4, `OPS` §2.2 |
| **6** | **Reliability chain math** | 3 subsystems × 90% = 72.9%. "It works on the bench" | Integration budget defended (84.9 h). 20-match dry run at G4. Reliability scoreboard in the pit — **it is also award evidence** | `PF` §4.1, `BIZ` N07 |
| **7** | **Mentor absorbs the shortfall** | Mentor builds the mechanism / writes the code. Better robot this season, worse team next | The 3.4 h/wk unblock budget **is** the job description. Anything beyond it is borrowed from 2028 | `CAP` §6.5 |
| **8** | **Late parts** | Swerve modules have **high stockout risk** and 4-week lead times | **2026-11-21 order-by.** One week of safety margin baked in | `MECH`, `CAP` `lead_time` |
| **9** | **Money spent on the wrong constraint** | $3k of tools for a team short on mentors. Or AI funded out of `robot_discretionary` | Money is constraint **#5**. Fund AI from the business line. The only purchase that widens the robot is **machine capacity** | `CAP` §7.1, `AI` 05 §1.4 |
| **10** | **Award scatter** | Five lanes, none evidenced. Or chasing Impact with a retrofitted story | Two lanes + a shared artifact library + the free non-judged lanes. **Protect the awards lead's time or halve the plan** | `BIZ` §5.3, §6.4 |
| **11** | **Scouting collapse** | A 6-scout plan staffed by 3 people, abandoned by match 20 | Design for **3 scouts** from day one: one metric + one binary per robot, plus a scouting alliance | `CAP` §4.4, `SCOUT` |
| **12** | **AI-induced confidence** | Hallucinated vendor API compiles in a student's head but not in Gradle; a fabricated rule number in a strategy doc | Compile in 60 s. `cite-check.py` on every rules answer. **100% student-explanation rate at PR review** | `AI` 01 §4, `AI` 03 §8 |
| **13** | **Legacy-stack training** | Students spend the fall mastering the roboRIO stack, which **WPILib 2027 makes incompatible** | Everything from September is on the **2027 alpha**. Shuffleboard/SmartDashboard/PathWeaver/LabVIEW are **removed** — do not teach them | `SW` §0 |
| **14** | **Week 1 event chosen by habit** | The plan that closes at 0.79× budget at Week 4 runs **1.26× over** at Week 1 | The event decision is made **2026-09-24 → 11-17**, on field size then week | `PF` §10–11, `BIZ` §6.5 |
| **15** | **Zero-slack surprise** | One snow week / one failed prototype / one shipping delay, and there is no reserve — because there is none | Build the reserve **into the calendar** (Week 4) rather than into the hours. A 10% cash reserve (Tier B) | `CAP` §3.3 |

---

## §9 — Validation

### 9.1 Every quantitative claim traces to a companion file

| Claim in this file | Source | Consistent? |
|---|---|:---:|
| 599 veq-h to Week 1; 854 to Week 4; multiplier 0.352 | `CAP` §2.5–2.6 | ✅ |
| `novel_mechanisms_max` = 2; `parallel_workstreams_max` = 3 | `CAP` §5.2–5.3, `team_capacity.yaml` | ✅ |
| Mentor unblock 3.4 h/wk; 1 mentor > 5 students | `CAP` §6.2, §6.4 | ✅ |
| $6,500 registration **[C]**; $2,500 `robot_discretionary`; $11,500 planning composite | `CAP` §8.1, `team_capacity.yaml` | ✅ |
| KoP chassis $1,600 · swerve $2,032–2,605 · intake $380 · bumpers $257 | `mechanism_catalog.yaml`, verified 2026-08-22 | ✅ |
| Drive practice weight 90; reliability 88; pick-probability 3–20× on field size | `PF` §4, §7, §11 | ✅ |
| 46 in-season award student-hours; 6 lanes; 2 prepared | `BIZ` §6.2–6.3 | ✅ |
| AI savings 40–70 veq-h season-wide, and they do **not** raise `novel_mechanisms_max` | `AI` 01 §2, 02 §6.3, 04 §3.2 | ✅ |
| WPILib 2027 breaking changes; alpha vendor libraries; Systemcore CAN FD | `SW` §0 **[C]** | ✅ |

### 9.2 The three headcount models reproduce the model's own sensitivity result

`CAP` §9.4 finds that **six of eight perturbations leave `novel_mechanisms_max` at exactly 2**, and
only *losing a lead* moves it (down to 1). §5.1 re-derives this independently at three roster sizes:
8 students → **1** (route A binds), 15 → **2**, 30 → **2** (route C binds). The 30-student row is the
check: if this playbook's arithmetic disagreed with `CAP` §5.5, it would show up as a 30-student team
building three mechanisms. It does not. ✅

### 9.3 The budget tiers close against the BOM

Tier B's robot line is priced from `mechanism_catalog.yaml` at **$2,648** for KoP chassis + bumpers +
intake + indexer — **6% over the $2,500 gate**, which `tools/bom-builder.py` would fail. That is the
correct behaviour and it is shown, not hidden: the fix (swap the indexer for a passive hopper →
**$2,562**, or trim spares) is stated in §4.2. A budget that closed exactly would mean the gate was
never tested. ✅

### 9.4 The award plan does not close at Week 1 — and this file says so

`BIZ` §6.5 totals **58 in-season student-hours** against a **46 h** budget: **1.26× over** at Week 1,
**0.79×** at Week 4. This playbook does not paper over that. It appears as failure mode #14 and as
force multiplier §3.6, and it is the same scheduling decision in both places. ✅

### 9.5 Reproduce

```bash
python tools/capacity_model.py --yaml                                   # §1, §5 arithmetic
python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown  # §4 gate behaviour
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml  # expect 27/30
bash reference/awards/kickoff_award_check.sh                            # §2 lane availability
```

---

## Files written by this pass

| Path | Contents |
|---|---|
| `SMALL_TEAM_PLAYBOOK.md` | this document |

**Nothing else was modified.** `reference/02_TEAM_CAPACITY_MODEL.md`, `reference/team_capacity.yaml`,
`reference/bom/*`, `reference/team-ops/*`, `reference/ai-integration/*`, `reference/awards/*`,
`reference/ACHIEVABILITY-RUBRIC.md`, `KICKOFF_PLAYBOOK.md` and `STRATEGY-RANKING-SYSTEM.md` were read
and cited, not edited. Add a link to this file from `INDEX.md` when convenient — this pass did not
edit the index.

---

## Known limitations

- **This file contains no BIOCORE game claim, and it cannot.** The rules, field and scoring element
  are not public as of 2026-08-22. Every mechanism named in §4 is a *placeholder priced from `MECH`*,
  not a recommendation about BIOCORE. Re-run §0 on 2027-01-09 with the real manual.
- **Almost every hour figure is [S].** `CAP`'s own Known Limitations apply in full here: no public
  dataset of FRC team attendance, meeting schedules or hours-to-mechanism exists. The model is
  internally consistent and reproduces three external anchors; it is **not fitted to data**.
- **The 8- and 30-student rows in §5.1 are this pass's extrapolation** of `CAP`'s method, not output
  from `tools/capacity_model.py` runs at those roster sizes with re-tiered skill mixes. The tier
  proportions were held constant, which is optimistic for 8 (small teams skew veteran-heavy *or*
  rookie-heavy, rarely proportional) and pessimistic for 30. Re-run the script with real rosters.
- **The three budget tiers are planning estimates.** Only the **$6,500 registration** and the
  **$1,000 Regional-plays-District fee** are **[C]**. Kickoff Kit shipping figures are 2026
  references; the 7% sales-tax rate is **[S]**; travel and food are entirely team-specific; the
  Tier A registration offset is an **assumption**, and Tier A collapses without it.
- **The Systemcore price is UNVERIFIED and appears as a placeholder in all three tiers.** This is a
  real hole. Re-check after **2026-11-12**.
- **Part prices were verified 2026-08-22 and FRC vendor prices moved mid-season in 2026.** Treat every
  figure as ±10% and run `reference/bom/recheck_prices.sh` before any PO.
- **The 2027 software ecosystem is in alpha and will move before kickoff.** ChoreoLib and maple-sim
  had **no 2027 release** as of 2026-08-22; PhotonVision was prerelease with no vendordep; AdvantageKit
  had no 2027 template projects. §6.2 schedules re-checks in November, December and kickoff week
  because any of those could invert a recommendation here.
- **Whether the roboRIO remains legal in 2027 is UNVERIFIED.** The plan assumes it does not matter,
  because WPILib 2027 is Systemcore-only **[C]** — but a legality carve-over would change the training
  calculus, not the training *target*.
- **AI savings are [S] estimates that have never been measured on this team.** `AI` 01 §10 describes
  how to measure them. Until you run a season, treat 40–70 veq-h as a hypothesis, and treat the
  reinvestment metric (drive-practice hours logged vs. 54.9 budgeted) as the only number that proves
  it worked.
- **This playbook cannot tell you the game is winnable with two mechanisms.** If BIOCORE's scoring
  requires three to play meaningfully, the correct response is `PF` §4.4's second-pick path — do one
  thing at a level that makes you worth picking — not a fourth workstream.

---

## Security note

Every source read for this pass was a local file inside this project. All of it was treated as
**data**. None contained text addressed to an AI assistant or any attempt to issue instructions. No
network request was made, no authentication was used or attempted, and no external endpoint was
contacted while writing this file. URLs quoted above were transcribed from files in this corpus that
recorded them as verified on 2026-08-21/22; they were **not** re-fetched by this pass.
