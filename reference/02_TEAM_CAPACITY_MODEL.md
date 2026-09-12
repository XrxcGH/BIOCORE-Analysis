# Team Capacity Model — what "~15 students" is actually worth in BIOCORE

**Purpose:** every achievability score downstream is denominated in this team's capacity, so capacity
has to be a *number*, not an adjective. This file converts ~15 students into effective build hours,
maps 15 bodies onto the fourteen functions an FRC season demands, and derives the single most
load-bearing parameter in the whole project — **how many mechanisms can be developed in parallel**.
Every figure is produced by `tools/capacity_model.py`, which is re-runnable with your own inputs.

**Companion file:** [`team_capacity.yaml`](team_capacity.yaml) — the calibrated constants the rubric
consumes. Model source: [`../tools/capacity_model.py`](../tools/capacity_model.py).

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model assumption. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

**Source shorthand**

`REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO · `CHRG` = 2023 CHARGED UP ·
`RAPD` = 2022 RAPID REACT. All in `manuals/archive/frc/`, which is not in the repository because
FIRST's documents are not redistributed; `bash tools/rebuild-corpus.sh --fetch` downloads them.
`PF` = [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md), the measured factor weights.
`CAL` = the 2027 FIRST season calendar as transcribed in
[`../research/03_biocore_official_intel.md`](../research/03_biocore_official_intel.md) §2.

> **Scope guard.** BIOCORE is **FRC**, kickoff **2027-01-09 12:00 ET**. Nothing here draws on FTC
> BIOBUZZ; "Pollen", StarterBots and Skill Builders are BIOBUZZ things and appear nowhere in this
> model. BIOCORE's rules and scoring element are not public as of 2026-08-22 — see
> [`../research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md). **This file contains
> no game-specific claims.** It is a model of the *team*, which is knowable today.

---

## 0. The 60-second workflow

Everything in this document regenerates from one script. Run this before you argue with any number in
it, and again on kickoff day with the schedule you actually committed to.

```bash
# Run from the repository root.

# ---- 1. the whole model, four scenarios, plus the calibrated constants (~2 s) ----
python tools/capacity_model.py --yaml

# ---- 2. YOUR numbers: substitute your real roster and your real meeting schedule --
#         --deadline is the event week you are actually registering for.
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week1
python tools/capacity_model.py --students 15 --hours-per-week 15 --deadline week4

# ---- 3. THE SINGLE MOST IMPORTANT LINE IN THE OUTPUT -----------------------------
#         "BINDING (min of the three)" -- that is novel_mechanisms_max.
#         If your kickoff-day strategy needs more mechanisms than that number,
#         the strategy is wrong, not the model.
python tools/capacity_model.py | grep -A1 "BINDING"

# ---- 4. the slack check ----------------------------------------------------------
#         "SLACK IN THE WHOLE PLAN" is what you have left after the eight mandatory
#         lines are funded. At 15 h/wk into a Week 1 event it is ZERO (Sec 3.3).
python tools/capacity_model.py | grep "SLACK IN THE WHOLE PLAN"

# ---- 5. sanity-check against the measured factor weights -------------------------
#         PF weights drive practice at 90 -- the highest in the corpus. Confirm the
#         budget actually funds it (Sec 3.4 shows the baseline does NOT, adequately).
python tools/capacity_model.py | grep "drive practice"
```

**Read the output in this order:** the milestone table first (it sets the deadline), then
`EFFECTIVE veteran-equivalent hours`, then `BINDING`, then `SLACK`. If `SLACK` is at or below zero
and you are targeting Week 1, stop and re-read §7.4 before you scope anything.

---

## 1. The calendar — what the 2027 season actually gives you

All dates **[C]** from `CAL`. Verbatim from the script:

```
weeks from kickoff to each 2027 milestone:
   weekzero  2027-02-20    6.00 weeks ( 42 days)
   week1     2027-03-03    7.57 weeks ( 53 days)
   week2     2027-03-10    8.57 weeks ( 60 days)
   week3     2027-03-17    9.57 weeks ( 67 days)
   week4     2027-03-24   10.57 weeks ( 74 days)
   week6     2027-04-07   12.57 weeks ( 88 days)
   champs    2027-04-28   15.57 weeks (109 days)
```

Three consequences worth naming:

1. **"The six-week build season" maps to Week Zero, not to your first event.** Kickoff → Week Zero is
   **exactly 6.00 weeks**; kickoff → Week 1 events is **7.57 weeks**. If your team's folklore says six
   weeks, it is 1.5 weeks pessimistic about the real deadline and exactly right about the deadline
   that matters for a shakedown.
2. **There is no bag day and no stop-build day** — **[C]**, verified by zero-hit full-text search of
   the 2026 manual and the 2027 calendar
   ([`FRC_VS_FTC_ORIENTATION.md`](FRC_VS_FTC_ORIENTATION.md) §1). Build access is continuous from
   kickoff to your last match. Capacity is therefore bounded by *hours you can staff*, never by a
   sealed robot.
3. **Choosing Week 4 over Week 1 adds 3.00 calendar weeks — 40% more season.** `PF` §10 measures that
   this costs approximately nothing competitively: a Week 5 field scores 24–38% more, and a team that
   plays both improves 37–46%, netting a rank-percentile change of **under 2 points**. §7.4 prices
   what those three weeks are worth in effective hours. It is the largest free lever in this document.

---

## 2. Nominal hours → effective hours

### 2.1 The unit: a veteran-equivalent hour (veq-h)

One **veq-h** = one hour of a competent, returning student who can be handed a task and left alone.
Every other student-hour is converted into veq-h by a productivity coefficient. This is the only way
to make "15 students" comparable to "8 students" or "40 students" without lying.

### 2.2 The derating chain, in order

| Step | Factor | Value | Justification |
|---|---|---:|---|
| a | Scheduled shop hours per week | 15.0 | 3 weeknights × 3 h + Saturday × 6 h. The modal small-team schedule **[S]** |
| b | Mentor soft cap on marginal hours | ≤16 h at 1.00, above at 0.75 | §6: hours past ~16/wk land on weekends and on a single mentor's fatigue. **[S]** |
| c | Calendar factor | **×0.88** | Semester finals (mid-late Jan), MLK weekend, Presidents' Day (2027-02-15), snow days, standardized testing, competing club obligations. 12% of scheduled sessions lost or gutted **[S]** |
| d | Attendance, by tier | 85% / 65% / 50% | The brief's 50–70% band, resolved by tier rather than averaged. Core members show up; first-years do not **[S]**, consistent with the brief |
| e | Productivity coefficient, by tier | 1.00 / 0.55 / 0.35 | §2.3 |
| f | First-year training tax | −0.50 / −0.25 / −0.10 veteran-h per first-year attended-h, weeks 1–2 / 3–4 / after | §2.4 |

Steps c–f are all **[S]** — they are model calibration, not measurement. §9.2 back-tests the composite
against two independent external anchors, which is the only validation available.

### 2.3 Skill distribution across 15 students

The brief specifies "2–4 real builders, 1–3 real programmers, rest learning". Resolved to the midpoint:

| Tier | n | Who they are | Attendance | Coefficient | Why that coefficient |
|---|---:|---|---:|---:|---|
| **Core technical** | **5** | 3 builders (Y3–Y4) + 2 programmers (Y2–Y4) | 85% | **1.00** | Definition of the unit. Works unsupervised, produces finished work |
| **Contributing veteran** | **4** | Y2 students who execute well-specified tasks | 65% | **0.55** | Needs the task defined and a check-in; cannot own a mechanism |
| **First-year** | **6** | Y1, includes non-technical recruits | 50% | **0.35** | Produces real work only on supervised, bounded tasks |

**[S]** This 5/4/6 split is the assumption the entire model rests on. It is the first thing to change
if your roster differs, and the script takes it as data.

### 2.4 First-years are net-negative early — the explicit arithmetic

A first-year does not merely produce less; in the first fortnight they **consume** veteran and mentor
hours faster than they generate output. Modelled as a draw of 0.50 veteran-hours per first-year
attended-hour in weeks 1–2, 0.25 in weeks 3–4, 0.10 thereafter.

Over the 7.57 weeks to a Week 1 event, six first-years:

| Quantity | Value |
|---|---:|
| Hours each attends | 50.0 |
| Gross output, 6 students @ coef 0.35 | **+104.9 veq-h** |
| Training tax drawn out of the veteran pool | **−73.5 veq-h** |
| **Net contribution of all six first-years** | **+31.4 veq-h** |

**Six first-years are worth about 31 effective hours before your first event — roughly one long
Saturday from one good veteran.** They are not a build-season resource. They are next season's core
technical tier, and the correct place to pay for them is **September–December 2026**, when the tax
falls on hours that have no competing use (§7.5).

The same six over the longer run to a Week 4 event net **+61.1 veq-h** — the tax is paid once, so
every additional week roughly doubles their net worth from a very low base.

### 2.5 The result — verbatim model output

```
--- BASELINE -> Week 1: 15 students, 15 sched h/wk, 7.57 weeks ---
  scheduled h/wk after mentor soft cap : 15.00
  calendar hours available per student : 99.9   (x0.88 calendar factor)
  tier                                      n   att    h ea  coef    veq-h
  core technical (3 build + 2 program)      5   85%    85.0  1.00    424.8
  contributing veteran                      4   65%    65.0  0.55    142.9
  first-year                                6   50%    50.0  0.35    104.9
  gross                                                              672.6
  less first-year training tax                                       -73.5
  EFFECTIVE veteran-equivalent hours                                 599.1
  nominal person-hours                 : 1704
  EFFECTIVE / NOMINAL multiplier       : 0.352
  effective veq-hours per week         : 79.1
```

### 2.6 The headline table

| Scenario | Sched h/wk | Weeks | **Nominal person-h** | **Effective veq-h** | Multiplier | veq-h / week |
|---|---:|---:|---:|---:|---:|---:|
| **LEAN → Week 1** | 10 | 7.57 | 1,136 | **399** | 0.352 | 52.7 |
| **BASELINE → Week 1** | 15 | 7.57 | 1,704 | **599** | 0.352 | 79.1 |
| **STRETCH → Week 1** | 22 | 7.57 | 2,499 | **819** | 0.328 | 108.1 |
| **BASELINE → Week 4** | 15 | 10.57 | 2,379 | **854** | 0.359 | 80.8 |

**The number to remember: 15 students × 15 scheduled hours = 225 nominal person-hours per week, and
79 effective ones. The multiplier is 0.35.** Anyone who plans against 225 is planning against a team
that does not exist. Note also that the STRETCH multiplier *falls* to 0.328 — the marginal hours past
16/wk are the least productive hours you own (§6.3).

---

## 3. Where the 599 hours go

### 3.1 The effective-hour budget, kickoff → Week 1

These eight lines are not a wish list; they are the minimum set of activities that must happen for a
robot to compete at all. Verbatim from the script:

| Line | veq-h | % | Note |
|---|---:|---:|---|
| Strategy / rule reading / game analysis | 25.0 | 4.2% | Kickoff weekend + the first Q&A week (Q&A opens **2027-01-13**, `CAL`) |
| CAD + design | 74.9 | 12.5% | |
| Fabrication + assembly | 129.8 | 21.7% | The largest single line |
| Electrical + pneumatics | 49.9 | 8.3% | Includes the 2027 control-system rebuild |
| **Programming (incl. SystemCore port)** | **134.8** | **22.5%** | Inflated ~40 h by the 2027 platform change — see §3.2 |
| Integration, debug, reliability hardening | 84.9 | 14.2% | `PF` weights reliability at **88** |
| **Drive practice** | **54.9** | **9.2%** | `PF` weights this at **90**, the highest in the corpus — see §3.4 |
| Awards / business / media / scouting prep | 44.9 | 7.5% | Partly runs outside shop hours |
| **TOTAL** | **599.1** | 100% | |

### 3.2 Programming is the tightest role in 2027, and it is not close

**[C]** The 2027 season replaces the roboRIO with **SystemCore**, and **WPILib 2027 is
Systemcore-only** and *"incompatible with the Rio"* (`PF` §6.3, quoting
[Latest controller information for FRC and FTC?](https://www.chiefdelphi.com/t/523342), 2026-08-14).
Whether the roboRIO remains legal in 2027 is **UNVERIFIED**. The 134.8 h decomposes **[S]**:

| Programming sub-line | veq-h | 2027 delta |
|---|---:|---|
| SystemCore/WPILib 2027 toolchain, deploy, new Driver Station | 40 | **+30 vs a normal year** |
| Drivetrain code + controls tuning | 35 | — |
| Mechanism control + sensors | 30 | — |
| Auto routines | 20 | `PF` §6.1: keep to one path unless an RP is AUTO-gated |
| Dashboard / logging / telemetry | 10 | — |

Now the supply side:

```
  programmer supply  (2 core x 85.0 h) :   169.9 h
  programmer demand                     :   134.8 h   -> 79% utilisation
```

**Two programmers are 79% pre-committed before a single bug exists.** Queueing behaviour at 79%
utilisation on a single-server resource is already bad; the effective utilisation is worse because
programmer time is also the resource that supports drive practice, in-pit debugging and match-day
code changes. **Action with a date on it: develop a third programmer between 2026-09 and 2026-12**,
on the 2026 robot and on SystemCore hardware as soon as it exists. That is the highest-return item
in this entire document and it costs zero dollars and zero build-season hours.

### 3.3 The plan closes with exactly zero slack

```
  non-programming supply                :   429.2 h
  non-programming demand                :   464.3 h   -> shortfall +35.1 h
  SLACK IN THE WHOLE PLAN               : +0.0 h
```

The mechanical side is **35 h short**, and it is covered precisely by the programmers' 35 h of
surplus — i.e. your programmers must spend a fifth of their time doing fabrication, which is what
actually happens on small teams. The plan balances. **It balances at zero.**

*(Honesty note: the eight allocation fractions were chosen to sum to 1.00, so "total = 599" is
arithmetic, not discovery. The finding is the one below it: when each of the eight mandatory lines is
priced at a rate that produces a working robot, the eight consume the entire budget and no line can be
cut without cutting a required activity. See Known Limitations.)*

**Every one of these puts a Week 1 robot behind:** one failed prototype iteration; a two-week
SystemCore hardware delay; one snow week; one core-technical student leaving; a shipping delay on a
motor. There is no reserve. §7.4 is the response.

### 3.4 The drive-practice line is the model's most alarming output

`PF` weights drive practice at **90 — the single highest factor in the measured corpus** — on the
finding that in-season improvement moves rank percentile by less than 2 points, so the only
improvement that buys relative position happens *before event 1*.

The budget funds it at **54.9 veq-h**. Convert that to actual driver seat-time:

| Step | Value |
|---|---:|
| Budgeted drive-practice veq-h | 54.9 |
| People a practice session occupies simultaneously (driver, operator, field reset, spotter/coach) | ÷ 3.5 |
| **Session-hours of a robot actually moving** | **≈ 15.7 h** |
| Fraction of those that occur *after* the robot is reliable enough to be worth driving | ×0.6 **[S]** |
| **Meaningful driver hours before event 1** | **≈ 9 h** |

**Nine hours.** That is the realistic pre-event driver experience of a 15-student team on a 15 h/week
schedule targeting Week 1 — against a factor the data says is the most important one available.

Three responses, in order of cost:

1. **Move the first event to Week 3–4.** +255 veq-h (§7.4), and the extra weeks land *after* the robot
   exists, which is exactly when practice hours are worth the most.
2. **Use the free substitutes** `PF` §7 names: field-oriented control in the simulator,
   controller-in-hand rehearsal, driving along with recorded matches. These cost zero shop hours
   because they run outside the 15 h/wk.
3. **Build the drivebase first and drive it while the mechanism is still in CAD.** Converts dead
   waiting-for-parts hours into the highest-weighted factor in the rubric.

---

## 4. Role coverage — 15 people onto 14 functions

### 4.1 The functions that must be covered

| # | Function | Must exist by | Can it be shared? | Minimum bodies |
|---|---|---|---|---:|
| 1 | Strategy / game analysis / rule expertise | Kickoff +2 days | Yes — with CAD & drive coach | 2 |
| 2 | Design / CAD | Week 1 | Yes — with fabrication | 2 |
| 3 | Fabrication & assembly | Week 1 | Yes — with CAD, electrical | 4 |
| 4 | Electrical / wiring / pneumatics | Week 3 | Yes — with pit crew | 2 |
| 5 | Programming / controls | Week 1 | **Partly** — see §3.2 | 2 (3 wanted) |
| 6 | Systems integration & test | Week 5 | Yes — with CAD lead | 1 |
| 7 | **Drive team: driver** | Week 6 | **No** | 1 |
| 8 | **Drive team: operator** | Week 6 | **No** | 1 |
| 9 | Drive team: human player | Event | Yes — with a scout | 1 |
| 10 | Drive coach | Event | **Mentor role** | 0 students |
| 11 | Pit crew / repair | Event | Yes — with electrical, fab | 3 |
| 12 | Scouting | Event | **Constrained** — see §4.3 | 3–6 |
| 13 | Awards / business / Impact submission | **2027-02-11 15:00** (`CAL`) | Yes — with media, scouting | 2 |
| 14 | Safety captain | Event | Yes — with pit crew | 1 |
| 15 | Media / documentation / outreach | Rolling | Yes — with awards | 1 |
| 16 | Logistics (travel, food, tools, spares, inventory) | Event | **Offload to parents/mentors** | 0 students |

Raw minimum bodies with no sharing: **26**. You have 15. Sharing is not an optimisation, it is
mandatory, and the whole question is *which* shares are safe.

### 4.2 A concrete 15-person roster

| # | Slot | Build-season primary | Build-season secondary | Event-day role |
|---:|---|---|---|---|
| 1 | Core tech A | **Primary mechanism lead** | CAD | Pit crew chief |
| 2 | Core tech B | **Drivetrain + frame + bumpers lead** | Fabrication | Pit crew |
| 3 | Core tech C | **CAD lead / integration owner** | Mechanism support | **Operator** |
| 4 | Core tech D | **Controls lead / SystemCore port** | Electrical | Pit (code) |
| 5 | Core tech E | **Auto + telemetry + logging** | Scouting data pipeline | Scouting lead |
| 6 | Veteran F | Electrical + pneumatics lead | Fabrication | Pit crew (electrical) |
| 7 | Veteran G | Fabrication | **Safety captain** | Pit crew / safety |
| 8 | Veteran H | **Driver** (starts driving Week 3) | Fabrication | **Driver** |
| 9 | Veteran I | **Business / awards lead** | Media | Impact presenter |
| 10 | First-year J | Fabrication support | Inventory | Scout |
| 11 | First-year K | Fabrication support | — | Scout |
| 12 | First-year L | Fabrication support | — | Scout |
| 13 | First-year M | Media / photo / build blog | Outreach | Human player |
| 14 | First-year N | Scouting system + data entry | Awards support | Scout |
| 15 | First-year O | Awards / Impact research | Media | Impact presenter #2 |
| — | **Mentor** | Design review, safety supervision, ordering | | **Drive coach** |

### 4.3 What can double up, and what cannot

**Safe doublings** — same person, different phase or same physical location:

| Pair | Why it is safe |
|---|---|
| CAD ↔ fabrication | Sequential within a week; the person who drew it should cut it |
| Electrical ↔ pit crew | The electrical owner *must* be in the pit; this is the strongest natural pairing |
| Safety captain ↔ pit crew | Safety is a pit-located judged role |
| Awards/business ↔ scouting | Scouting gives business students the match narrative the Impact submission needs |
| Media ↔ outreach | Same artefacts |
| Auto programmer ↔ scouting data owner | Both are data-shaped, both idle during opposite parts of the day |
| **Logistics ↔ parents/mentors** | Offload it entirely. Highest-leverage delegation available and it costs zero student hours |

**Unsafe doublings** — these fail, and they fail on match day:

| Pair | Why it fails |
|---|---|
| **Driver ↔ operator** | Physically impossible. Two humans, always |
| **Drive team ↔ scouting** | The drive team is on the field precisely when scouting must happen |
| **Pit crew ↔ scouting** | Same collision, offset by one match |
| **Lead programmer ↔ sole mechanical fixer** | A single point of failure that gets hit during elimination repairs |
| **Impact presenter ↔ pit crew** | Impact judging is scheduled *inside* the qualification block; presenters are gone for ~90 min |
| **Drive coach ↔ a student role** | Coach must watch the whole field, not the robot. Mentor role. Non-negotiable |

### 4.4 The event-day arithmetic — and the scouting problem

Realistic event attendance for a 15-student team is **12**, not 15 (school, family, cost). During a
match cycle:

| Occupied | Bodies |
|---|---:|
| Drive team (driver, operator, human player) | 3 |
| Pit crew on standby / repair | 3 |
| Safety captain (shared with pit, counted once) | 1 |
| **Subtotal unavailable** | **7** |
| **Available for scouting** | **5** |
| …minus Impact presenters during their judging window | **3** |

**Full manual scouting requires 6 — one per robot on the field. You have 3 to 5.** This is a hard,
structural consequence of the roster and it is not solvable by working harder.

Four viable schemes, all of which fit inside 3–5 scouts **[S]**:

1. **Two robots per scout, one metric each.** 3 scouts × 2 robots, tracking a single number
   (scoring actions) plus a binary (did it break). Crude, but `PF` §4.3 shows captains buy **average
   delivered points** — which is exactly the crude number.
2. **Scout your own alliance colour only.** 3 scouts cover 3 robots; you learn your partners, not
   your opponents. Adequate for a team whose realistic path is being *picked*, not picking.
3. **Join a scouting alliance.** Costs zero bodies, costs a data-sharing agreement made in the pits
   on Thursday. The single best return on 15 minutes of social effort at an event.
4. **Public data + one qualitative scout.** TBA rankings after quals give the quantitative column for
   free; assign **one** student to the column public data never has — defence quality, cycle path,
   breakdown recovery, pit professionalism.

**Rubric consequence:** any strategy that *depends on out-scouting the field* is out of reach for
this roster and should be scored down accordingly.

---

## 5. PARALLEL WORKSTREAMS MAX — the load-bearing number

### 5.1 Definition

A **workstream** is an independent development thread that requires all five of:

1. its own design decision, made once and then defended;
2. its own prototype → test → revise loop;
3. its own slot in the fabrication queue;
4. its own student lead who can work **unsupervised**;
5. its own integration into the whole robot, with its own failure modes.

By this definition, "add a limelight" is not a workstream. "Add a second scoring mechanism" is.

### 5.2 Three independent derivations, converging

Verbatim from the script:

```
--- PARALLEL WORKSTREAMS, three independent routes (BASELINE -> Week 1) ---
  route A  unsupervised student leads : 5 total, 3 mechanical, minus drivetrain => 2 novel mechanisms
  route B  residual CAD+fab hours     : 205 h / 90 h per mechanism => 2.27 novel mechanisms
  route C  single-machine shop queue  : => 2 novel mechanisms
  BINDING (min of the three)          : 2.00
```

**Route A — the student-lead constraint.** Criterion 4 above is the scarcest input. You have 5
core-technical students; 2 are the programmers and software is itself a workstream that never rides
free. That leaves **3 mechanical leads**. The drivetrain permanently consumes one — even a KoP
chassis needs an owner for frame, bumpers, wheels, gearing and the mechanical half of the electrical
board. **→ 2 novel mechanisms.**

**Route B — the hours constraint.** Of the 599 h, the CAD + fabrication lines total **205 h**. A
novel mechanism, taken from prototype through CAD, fabrication, mounting, iteration and reliability
hardening, costs a small team **90 veq-h** **[S]** — a number chosen to be *generous*, because 90 h
is roughly two full weeks of the entire team's mechanical output. **→ 2.27 novel mechanisms.**

**Route C — the fabrication queue.** One 3D printer, one bandsaw, one drill press, one mentor
qualified to supervise the mill. Two mechanism streams contend for the same saw at the same moment
on the same Tuesday. A single-server queue at >70% utilisation has wait times that grow without
bound; two active streams already saturate it. **→ 2 novel mechanisms.** Note that this route is
**insensitive to headcount** — see §5.5.

**Three routes with no shared assumptions land on 2, 2.27 and 2.** That convergence is the reason to
trust the number.

### 5.3 The answer

```yaml
parallel_workstreams_max: 3      # concurrent development threads
novel_mechanisms_max:     2      # mechanisms beyond the drivetrain
novel_mechanisms_recommended: 1  # plus one COTS-derived or trivial second
```

The **3** concurrent workstreams are:

| # | Workstream | Lead | Mandatory? |
|---|---|---|:---:|
| 1 | Drivetrain + frame + bumpers + electrical | Core tech B (+F) | **Yes** |
| 2 | **The primary scoring mechanism** | Core tech A (+C) | **Yes** |
| 3 | Software / controls / SystemCore | Core tech D (+E) | **Yes** |

A **second scoring mechanism, or an endgame mechanism, or a vision-based pose-estimation stack, is
workstream #4** and is over the line. Workstream #4 does not fail loudly; it fails by starving
workstream #2 of the last 30% of its reliability work, which `PF` §8 prices at roughly halving your
probability of being picked.

### 5.4 Defending the number against the obvious objections

| Objection | Response |
|---|---|
| *"Everybody builds an intake AND a shooter AND a climber."* | Those are the teams `PF` §5.3 measures pulling away — P90/P50 EPA ratio went 1.38 → 2.35. They have 40 students and 6 mentors. At 15 students the observable comparison class is the Everybot |
| *"The Everybot has 2–3 mechanisms."* | Correct, and its mechanisms are **published, pre-solved and non-novel** — a released design is not a workstream by criterion 1 or 2. Copying one costs fabrication hours, not design hours. That is exactly why 118's programme works |
| *"We did 3 mechanisms last year."* | Then check whether all three were reliable in every match. `PF` §4.1: a 3-link chain at 90% each is **72.9%** reliable, and martinma's team nailed 9 of 10 subsystems and landed in *"the lower EPA percentile"* |
| *"Just work more hours."* | STRETCH (22 h/wk) buys +220 veq-h, which route B turns into +2.4 mechanisms — but routes A and C are unmoved, so `BINDING` stays **2**. Hours are not the binding constraint on mechanism count |
| *"Recruit more students."* | §5.5 |

### 5.5 More students does **not** raise this number

Re-run the model at 20 students, same tier proportions:

| Route | 15 students | 20 students | Moved? |
|---|---:|---:|:---:|
| A — unsupervised leads | 2.0 | 3.7 | yes |
| B — CAD+fab hours | 2.27 | 3.0 | yes |
| C — fabrication queue | **2.0** | **2.0** | **no** |
| **BINDING** | **2.0** | **2.0** | **no** |

**Adding five students buys zero additional mechanisms.** It buys more hours *inside* the two
mechanisms you already have — which is genuinely valuable, because that is where reliability lives —
but it does not widen the robot. The only things that widen the robot are **machine capacity** and
**outsourced fabrication**, both of which are bought with money (§7.3).

### 5.6 The two 2027-specific deductions

Both come straight out of `PF` and both reduce the number:

1. **SystemCore inflates the software workstream.** `PF` §6.3, **[C]**: WPILib 2027 is
   Systemcore-only and incompatible with the roboRIO; no production units existed as of 2026-08-14.
   The software stream is worth ~1.4 normal streams in 2027, and §3.2 shows programming already at
   79% utilisation. **[S]** Deduct 0.4 from the mechanical side.
2. **A first-year swerve adoption counts as a mechanism, not a drivetrain upgrade.** `PF` §3.4,
   verbatim: *"A team switching to swerve in the same season it attempts a two-mechanism robot is
   spending its scope budget twice."*

| 2027 configuration | Novel mechanisms available |
|---|---:|
| Known drivetrain (tank/KoP or returning swerve), SystemCore port | **2** |
| Known drivetrain, SystemCore port, **+ vision-based pose estimation** | **1** |
| **First-year swerve** + SystemCore port | **1** |
| First-year swerve + SystemCore port + vision | **0** — this configuration builds a drivebase and nothing else |

**[S]** The last row is the failure mode to name out loud on kickoff day. It is an entirely
reasonable-sounding plan and it produces no scoring robot.

---

## 6. Mentor supervision capacity — a separate, harder-bound resource

### 6.1 Why it gets its own section

Mentor time is not student time discounted. It is a **different resource with different substitution
rules**: it cannot be replaced by more students, it cannot be bought quickly, it does not scale with
roster size, and it is the only resource that gates *safety-critical* activity. The brief specifies
one experienced mentor.

### 6.2 The attention budget

**[S]** for every line; this is a model, not a measurement.

| Quantity | Value |
|---|---:|
| Mentor attendance at a 15 h/wk schedule | 90% → **13.5 h/wk in shop** |
| Out-of-shop mentor load (ordering, registration, travel, parent comms, paperwork) | ~5 h/wk |
| **Total mentor commitment** | **~18.5 h/wk** |

Of the 13.5 shop hours:

| Consumer | Share | h/wk | Delegable? |
|---|---:|---:|---|
| Tool/safety supervision that cannot be delegated | 25% | 3.4 | **No** — insurance, school policy, competence |
| Direct teaching of first-years | 30% | 4.1 | Partly — to core-technical students, at their cost |
| In-meeting logistics (parts hunt, ordering, cleanup direction) | 20% | 2.7 | **Yes** — to a parent volunteer |
| **Design review and unblocking decisions** | **25%** | **3.4** | **No** |

**The team's real mentor capacity is 3.4 hours per week of decision-unblocking.**

### 6.3 The unblock threshold — an independent reproduction of §5

**[S]** A stuck mechanical workstream needs roughly **45–60 minutes** of mentor attention to be
unstuck *within the same meeting*. Below that, the block carries to the next meeting, costing 2–3
calendar days. At 15 h/wk over 7.57 weeks you get about **23 meetings**; a stream that blocks weekly
loses 7 of them.

| Concurrent streams | Mentor minutes per stream per week | Above the 45-min unblock threshold? |
|---:|---:|:---:|
| 2 | 101 | **Yes**, comfortably |
| **3** | **68** | **Yes** |
| 4 | 51 | Marginal |
| 5 | 41 | **No** |
| 6 | 34 | **No** |

**A completely different resource, with no shared assumptions, reproduces `parallel_workstreams_max = 3`.**
This is the strongest validation in the document (§9.1).

It is also the derivation of the 16 h/wk soft cap in §2.2: past ~16 scheduled hours, the marginal
hours are weekend hours where a single mentor either is not present or is present and tired, so the
supervision-gated fraction of work stops happening. That is why the STRETCH multiplier falls to 0.328.

### 6.4 The mentor multiplier — the cheapest capacity you can buy

| Technical mentors | Unblock h/wk | Streams above threshold | Practical cap after routes A/C |
|---:|---:|---:|---:|
| 1 | 3.4 | 3 | **3** |
| 2 | 6.8 | 6 | 4 (route A binds) |
| 3 | 10.1 | 9 | 4 (route C binds) |

> **One additional competent technical mentor is worth more than five additional students.**
> Five students move `BINDING` from 2.0 to 2.0 (§5.5). One mentor moves the unblock capacity from
> 3.4 to 6.8 h/wk, which is what lets the two mechanisms you *do* build actually reach reliability —
> the factor `PF` weights at 88.

**Action with a date on it:** recruit the second technical mentor **before 2026-11-17** (season
registration deadline, `CAL`), so they are present for the fall training programme (§7.5) rather than
being onboarded during build season, when onboarding costs the very resource you are trying to add.

### 6.5 What the mentor must not do

**[S]** The failure mode for an experienced mentor on a small team is absorbing the shortfall
personally — building the mechanism, writing the code, driving the design. It produces a better robot
this season and a worse team next season, and it is invisible in every metric this project measures
until the mentor's own capacity becomes the ceiling. The 3.4 h/wk unblock budget is the mentor's job
description. Anything beyond it is borrowed from 2028.

---

## 7. The constraint hierarchy — what binds first

### 7.1 The order

For a 15-student, one-mentor, COTS-path team at 15 h/wk targeting a Week 1 event:

| Rank | Constraint | Quantity | What it binds | In-season elasticity | Cost to relax |
|---:|---|---|---|---|---|
| **1** | **Mentor unblock attention** | **3.4 h/wk** | how many streams stay unstuck; whether mechanisms reach reliability | **None** | Recruit a 2nd technical mentor, Sept–Nov 2026. **$0** |
| **2** | **Unsupervised student leads** | **5** (3 mech + 2 prog) | `parallel_workstreams_max` directly | **None** in-season; high in the fall | Fall training programme. $0 + fall hours |
| **3** | **Effective hours** | **599 h** to Week 1 | total scope; whether the plan has any reserve | Partial, capped by (1) | +7 h/wk → +220 h, at real burnout cost; **or move to Week 4 → +255 h free** |
| **4** | **Machine access / fab queue** | ~**2** streams | novel-mechanism throughput | **High — via money** | SendCutSend / outsourced 2D sheet, a few hundred dollars |
| **5** | **Money** | ~**$2,500** discretionary | which parts you may buy | Low in-season; high with 6 months' notice | Grants, sponsors, `PF` §5.1 COTS path |

### 7.2 Money binds **last** — and this is the counter-intuitive finding

Folk wisdom says a small team is money-limited. For a **COTS-path** team it is not, and `PF` §5.1
measures why: a complete competitive Everybot is **~$1,500 over the Kit of Parts**, it needs *"only
common tools, a basic 3D printer, items purchased from your local hardware store"*, and in 2026 the
COTS path produced **441 True Everybots**, **100 alliance captains** and **21 event wins** — a 22%
captaincy rate against a 21.8% population base rate for two-event teams. **[C]**

At $2,500 of discretionary robot budget you can buy every part of a two-mechanism COTS robot. You
cannot buy a second mentor, you cannot buy three more unsupervised student leads, and you cannot buy
back the 3 calendar weeks you spent choosing a Week 1 event.

### 7.3 …unless you commit to custom fabrication, at which point money jumps to #1

`PF` §5.1, **[C]** as a first-hand mentor account: a district-competitive **custom tank** robot cost
**~$13,000**; the same robot on swerve, **~$17,000**. That is an order of magnitude over the COTS
path. The moment a team commits to custom fabrication, the hierarchy inverts:

| Constraint | COTS path | Custom path |
|---|---:|---:|
| Money | **#5** (~$2,500) | **#1** (~$13,000–17,000) |
| Machine access | #4 | #2 |
| Mentor attention | **#1** | #3 |
| Effective hours | #3 | #4 |

**Choosing a fabrication strategy is choosing which constraint governs your season.** For this team,
the COTS path is not a compromise; it is the choice that puts the binding constraint on a resource
that can be relaxed for $0 (a second mentor) rather than one that needs a $13,000 sponsor.

### 7.4 The single highest-return decision: event week

```
--- DELTA: what buys more hours? ---
  +7 scheduled h/wk (15 -> 22), same Week 1 event : +220 veq-h
  same 15 h/wk, Week 1 event -> Week 4 event      : +255 veq-h
```

**Moving from a Week 1 event to a Week 4 event buys more effective hours than adding seven meeting
hours per week — and costs nothing in fatigue, attendance decay, mentor burnout or family goodwill.**

And `PF` §10 shows the competitive cost is approximately zero: the field is 24–38% stronger by Week 5,
your own team improves 37–46% over the same span, and the net rank-percentile change is under 2
points. The two effects cancel; the three weeks are free.

**But there is a countervailing constraint, and it must be checked before acting on this.** `PF` §11
measures the largest effect in the entire corpus: at the same relative rank, a team is **3–20× more
likely to be picked at a sub-36-team event than at a 61+-team event** (bottom-quarter band, 2026:
60.8% vs 3.1%). Field size dominates event week. **Optimise field size first; among the events that
survive that filter, take the latest one.** Round 1 event preferencing opens **2026-09-24 12:00 ET**
and all registration closes **2026-11-17 12:00 ET** (`CAL`) — a *four-month-before-kickoff* decision
that outranks any mechanism decision made in January.

### 7.5 The fall programme this all implies

Every top-ranked constraint is relaxable only before kickoff. Between **2026-08-22 and 2027-01-09**
you have ~20 weeks with no game and no deadline pressure:

| Action | Relaxes | Deadline |
|---|---|---|
| Recruit a 2nd technical mentor | **Constraint #1** | 2026-11-17 |
| Train a 3rd programmer on SystemCore hardware as it becomes available | §3.2, the 79% utilisation | 2027-01-09 |
| Promote 2 contributing veterans to unsupervised leads | **Constraint #2** | 2027-01-09 |
| Pay the first-year training tax now, on hours with no competing use | §2.4 (−73.5 veq-h) | 2026-12 |
| Pick events by **field size first, then latest week** | §7.4 | **2026-09-24** |
| Establish the outsourced-fabrication account and run one test order | Constraint #4 | 2026-12 |
| Start driver practice on the 2026 robot | `PF` factor #1, weight 90 | ongoing |

**[S]** Executing this list is worth more than any strategy chosen on kickoff day. Every item moves a
constant in `team_capacity.yaml`, and every constant in that file is cited by every downstream score.

---

## 8. The calibrated constants

These are the values written to [`team_capacity.yaml`](team_capacity.yaml). Baseline profile:
**15 students, 15 scheduled h/wk, one experienced technical mentor, COTS path, Week 1 event.**

| Constant | Value | Derived in | Confidence |
|---|---:|---|---|
| `effective_build_hours` | **599** | §2.5 | **[S]** model; calendar inputs **[C]** |
| `effective_build_hours_week4` | **854** | §2.6 | **[S]** |
| `effective_hours_multiplier` | **0.352** | §2.6 | **[S]** |
| `parallel_workstreams_max` | **3** | §5.2, independently §6.3 | **[S]**, triple-derived |
| `novel_mechanisms_max` | **2** | §5.2 `BINDING` | **[S]**, triple-derived |
| `cad_hours` | **75** | §3.1 | **[S]** |
| `programming_hours` | **135** | §3.1–3.2 | **[S]**; SystemCore premise **[C]** |
| `fabrication_hours` | **130** | §3.1 | **[S]** |
| `drive_practice_hours` | **55** (≈9 h of real seat time) | §3.4 | **[S]** |
| `awards_hours` | **45** | §3.1 | **[S]** |
| `budget_usd.season_registration` | **6500** | `CAL` | **[C]** |
| `budget_usd.robot_discretionary` | **2500** | §8.1 | **[S]** planning target |
| `budget_usd.season_total_planning` | **11500** | §8.1 | **[S]** composite |
| `mentor_unblock_hours_per_week` | **3.4** | §6.2 | **[S]** |

### 8.1 The budget lines

| Line | USD | Evidence |
|---|---:|---|
| **Season registration** | **6,500** | **[C]** — includes team number, Kit of Parts, award eligibility, and participation at **one Regional or two District events** ([FIRST Cost & Registration](https://www.firstinspires.org/robotics/frc/cost-and-registration), via `CAL`) |
| Kickoff Kit shipping, ground US/Canada | 50–315 | **[C]** for 2026 reference figures; **2027 TBA** |
| Sales tax | assume **7%** | **[C]** that tax practice changed for 2026-27 and that *event registrations may now be taxable*; **[S]** on the rate. Budget for it |
| **Robot BOM over the KoP — floor** | **1,500** | **[C]** — Everybot 2026 all-in, `PF` §5.1 |
| **Robot BOM over the KoP — planning target** | **2,500** | **[S]** — floor + one novel mechanism + spares |
| Robot BOM — custom-fabrication path | 13,000–17,000 | **[C]** as a first-hand district-mentor account, `PF` §5.1. **Out of reach; named so it is not accidentally assumed** |
| 2027 control system (SystemCore) | **UNVERIFIED** | No price published as of 2026-08-22. **Do not assume the roboRIO carries over** (`PF` §6.3) |
| Spares + consumables | 400–600 | **[S]** |
| Local event travel / food (no hotel) | ~1,200 | **[S]** |
| Regional teams playing a District event | 1,000 | **[C]**, new for 2027 (`CAL`) |
| **Composite minimum viable season** | **~9,000** | **[S]** — registration + shipping + tax + Everybot + spares, no travel |
| **Composite planning target** | **~11,500** | **[S]** — the number to fundraise against |

**Which number the rubric should use.** `season_registration` is a fixed cost that does not trade
against any design decision. The number that governs design trades is
**`robot_discretionary = $2,500`**. Score strategies against that, not against the $11,500.

---

## 9. Validation / dry run

### 9.1 Internal: three-route convergence, plus a fourth

`parallel_workstreams_max` is derived four times from four resources with no shared inputs:

| Route | Resource | Result |
|---|---|---:|
| A | Unsupervised student leads (headcount + skill) | 2 novel mechanisms |
| B | CAD + fabrication effective hours (time) | 2.27 |
| C | Single-machine shop queue (capital) | 2 |
| **D** | **Mentor unblock attention (§6.3)** | **3 total streams = 2 novel** |

Four independent derivations, four agreeing answers. Any one of them could be miscalibrated; all four
being miscalibrated in the same direction is unlikely.

### 9.2 External: two anchors the model must not contradict

**Anchor 1 — the Everybot must be buildable.** 118's Everybot is drivetrain + 1–2 pre-solved
mechanisms, ~$1,500 over the KoP, common tools plus a 3D printer, and **441 teams built one in 2026**
(**[C]**, `PF` §4.4). The model says a 15-student team has 599 veq-h, 205 of them in CAD+fabrication,
against a pre-solved design that costs fabrication hours but almost no design hours. **Predicted:
comfortably achievable with reserve.** Observed: 441 teams, 100 alliance captains, 21 event wins,
**22% captaincy versus a 21.8% base rate**. ✅ **Consistent.**

**Anchor 2 — the 10-subsystem robot must fail.** `PF` §4.1 quotes a district-level mentor with ~10
students, ~4 mentors and a ~$20k budget: *"we nailed 9 out of 10 subsystems perfectly on the first
try… One mistake / oversight out of 10 subsystems… now without coming up with a solution **we are the
lower EPA percentile**."* (**[C]** as a first-hand account.)

Run that team through the model: 4 mentors relaxes constraint #1 to ~13.6 unblock h/wk; $20k relaxes
constraint #5; but 10 students at a similar tier mix yields ~3–4 mechanical leads and a single-shop
queue. **Predicted `BINDING`: 2–3 novel mechanisms. They attempted 10.** The model predicts failure by
scope even for a better-resourced team than ours, and it predicts the *specific* failure mode — a
serial-reliability miss, not a design miss. That is what happened. ✅ **Consistent.**

**Anchor 3 — the drive-practice figure must be recognisable.** The model outputs ~9 hours of real
driver seat-time before a Week 1 event (§3.4). Compare a driver's own account, **[C]**, `PF` §7:
*"with this being our first year with swerve, I actually got no practice because we had lots of
problems when building, so in our first comp I was not actually driving."* ✅ **Consistent** — and the
model shows why: drive practice is the *last* line in the budget and the first to be consumed by
overruns in the seven lines above it.

### 9.3 Reproducibility

```bash
python tools/capacity_model.py --yaml
```
Deterministic; no network, no data files, no randomness. Every table in §1, §2.4, §2.5, §2.6, §3.1,
§3.3, §5.2 and §7.4 is verbatim script output, and the script's constants are the ones written to
`team_capacity.yaml`. Re-run after changing any assumption and the whole document's arithmetic moves
with it.

### 9.4 Sensitivity — which assumption matters most

| Assumption perturbed | Change | `effective_build_hours` | `novel_mechanisms_max` |
|---|---|---:|---:|
| baseline | — | 599 | **2.00** |
| Core technical tier 5 → 4 | −1 lead (→ contributing) | 550 (−8%) | **1.00** ← catastrophic |
| Core technical tier 5 → 6 | +1 lead | 648 (+8%) | 2.00 (route C binds) |
| Attendance 85/65/50 → 75/55/40 | −10 pp each | 521 (−13%) | 1.98 |
| Calendar factor 0.88 → 0.80 | ~1 more lost week | 545 (−9%) | 2.00 |
| Roster 15 → 20 students | +5 bodies | 799 (+33%) | **2.00** (route C binds) |
| Schedule 15 → 22 h/wk | STRETCH | 819 (+37%) | 2.00 (routes A, C bind) |
| Week 1 → Week 4 event | +3.00 weeks | **854 (+43%)** | 2.00 (routes A, C bind) |

*(All rows recomputed with `tools/capacity_model.py`, 2026-08-22. `novel_mechanisms_max` is the min
of routes A, B and C at each perturbation.)*

**Read the last column, not the middle one.** Six of the eight perturbations — including *adding five
students* and *adding seven hours a week* — leave `novel_mechanisms_max` at exactly 2. Only one moves
it, and it moves it **down by half**: losing a single unsupervised lead, because route A drops from 2
to 1 and becomes the binding route on its own. Note the asymmetry — losing a lead costs 1.0
mechanisms; gaining one costs nothing because route C (the shop queue) catches it.

That single row is the whole argument for the fall programme in §7.5. Promoting one contributing
veteran to unsupervised-lead status is worth more than any amount of scheduling; **losing one to
graduation, burnout or a competing commitment is the largest uninsured risk this team carries**, and
it is the one the rubric should treat as a named schedule risk rather than a rounding error.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/02_TEAM_CAPACITY_MODEL.md` | this document |
| `reference/team_capacity.yaml` | the calibrated constants, machine-readable, consumed by the achievability rubric |
| `tools/capacity_model.py` | **new** — the model. Every number in this file is its output; re-runnable with your own roster and schedule |

Nothing marked DONE was modified. [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md),
[`04_predictive_factors.yaml`](04_predictive_factors.yaml) and everything under `reference/awards/`
were read and cited, not edited.

---

## Known limitations

- **Almost every coefficient in §2 is [S], not measured.** No public dataset of FRC team attendance,
  meeting schedules, skill distribution or hours-to-mechanism exists — nobody records it, which is the
  same gap `PF` §7 hits on practice hours. The model is calibrated to be *internally consistent* and
  to reproduce two external anchors (§9.2); it is not fitted to data, because there is no data.
- **The zero-slack result in §3.3 is partly constructed.** The eight allocation fractions were chosen
  to sum to 1.00, so "total = 599" is definitional. What is *not* definitional is that each of the
  eight lines, priced at a rate that produces a working robot, is already at or below the minimum —
  most visibly drive practice at 9 real hours (§3.4). Treat §3.3 as "the mandatory lines exhaust the
  budget", not as a measured surplus of zero.
- **The 90 veq-h per novel mechanism is a single point estimate** and it drives route B directly. It
  is deliberately generous. A genuinely novel mechanism with an unfamiliar actuation scheme can cost
  double; a copied, published mechanism costs a third. Route B is therefore the *least* trustworthy of
  the four convergent routes — which is why the answer rests on A, C and D as well.
- **The `parallel_workstreams_max = 3` / `novel_mechanisms_max = 2` split assumes software is exactly
  one workstream.** In 2027 it is more (§5.6) and the deduction of 0.4 is an unvalidated guess. If
  SystemCore turns out to be a smooth port, the mechanical capacity is better than stated; if
  production units slip past kickoff, it is much worse. **Re-run this section once SystemCore hardware
  is in hand.** Whether the roboRIO remains legal in 2027 is **UNVERIFIED**.
- **SystemCore's price is UNVERIFIED**, so `budget_usd` carries a control-system line with no number
  in it. That is a real hole in the season budget, not a rounding error. Re-check the FIRST and vendor
  pages after the **2026-11-12 Pre-Kickoff Virtual Kit Release** (`CAL`).
- **All budget figures except the $6,500 season registration and the $1,000 inter-district fee are
  planning estimates.** Kickoff Kit shipping figures are 2026 references; 2027 shipping and the sales
  tax rate are not published. Travel and food are entirely team-specific.
- **Event-day attendance of 12 of 15 is assumed, not observed**, and it drives the whole scouting
  conclusion in §4.4. A team that reliably brings all 15 gets a fourth and fifth scout and the
  conclusion softens — but it does not reverse, because 6 scouts requires 15/15 attendance plus zero
  Impact judging overlap.
- **The model says nothing about BIOCORE.** It contains no game-specific claim of any kind, by design
  — the game is not public until **2027-01-09**. What it does is fix the denominator so that on
  kickoff day the only open variable is the game. If BIOCORE's scoring requires three mechanisms to
  play meaningfully, this model does not tell you that you can build three; it tells you that you
  cannot, and that the right response is `PF` §4.4's second-pick path, not a fourth workstream.
- **Sensitivity was computed by re-running the script with perturbed constants, by hand**, and §9.4's
  figures are rounded. The script does not yet have a `--sweep` mode. It should.

---

## Security note

Every source read for this pass was a local file in this project or a FIRST/vendor page already
transcribed into `research/03_biocore_official_intel.md` by an earlier pass. All of it was treated as
**data**. None contained text addressed to an AI assistant or any attempt to issue instructions. No
authentication was used or attempted, and no external endpoint was contacted while writing this file.
