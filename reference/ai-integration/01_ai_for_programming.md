# AI for Robot Programming — buying down the 79% programmer utilisation

**Purpose.** [`02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §3.2 says the tightest role
on this team in 2027 is programming: **two core programmers supply 169.9 veq-h, the season demands
134.8 h — 79% utilisation before a single bug exists**, and that demand is *inflated by roughly 40 h
purely by the roboRIO→Systemcore platform change*. This file is the plan for attacking those two
numbers with AI, without producing code that hurts somebody. It covers which tools to buy (§1), the
repo contract that makes them safe (§2), the uses ranked by payoff (§3), the uses that will burn you
(§4), the hard gate before anything actuates (§5), how students end up knowing *more* rather than
less (§6), and a runnable post-match log→report pipeline (§7).

**Companion files**
- [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) — **authoritative** on FIRST's
  AI policy. AI is permitted; attribution is mandatory. Quoted, never re-litigated, here.
- [`templates/frc-robot-CLAUDE.md`](templates/frc-robot-CLAUDE.md) — the drop-in repo contract.
- [`templates/programming-prompts.md`](templates/programming-prompts.md) — 13 paste-ready prompts.
- [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md) — the Systemcore /
  WPILib 2027 / AdvantageKit / simulation stack. **This file does not repeat it.** Where that file
  says "do X", this file says "here is how AI makes X cost less".
- [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml)
  — every hours claim below is denominated in these. **[C]** against that file.
- [`../../tools/log-report.py`](../../tools/log-report.py) — written by this pass; see §7.

**Evidence labels**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source, fetched and read on the date given |
| **[H]** HISTORICAL-PATTERN | Observed in prior seasons / prior tool generations; not stated for 2027 |
| **[S]** SPECULATION | Inference or model assumption. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked against a primary source |

> **Scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game, kickoff **2027-01-09 12:00 ET**.
> Nothing here is drawn from FTC BIOBUZZ. Pollen, StarterBots and Skill Builders are FTC things and
> appear nowhere in this document.

> **Verification standard.** Vendor pricing and education-programme claims in §1 were fetched on
> **2026-08-22**. Anything I could not pull from a first-party page is marked **UNVERIFIED** and you
> should re-check it before spending money. Prices and free-tier programmes in this category changed
> at least twice in the twelve months before this file was written — see §1.5.

---

## §0. The 60-second workflow

Run this in the off-season, once, on the machine that will hold the robot repo. It costs about a
minute and it is the entire setup.

```bash
# ---- 0. where you are -----------------------------------------------------------
# (the repository root: every path below is relative to it)

# ---- 1. re-read the constraint you are attacking ---------------------------------
python tools/capacity_model.py | grep -i -A2 "programm"
#   expect: programmer supply 169.9 h / demand 134.8 h -> 79% utilisation
#   If your real roster differs, re-run with --students N --hours-per-week H first.

# ---- 2. drop the repo contract into the robot repo (NOT this repo) ---------------
#         Substitute your real robot-code path.
ROBOT=~/frc/BIOCORE-2027
cp reference/ai-integration/templates/frc-robot-CLAUDE.md "$ROBOT/CLAUDE.md"
$EDITOR "$ROBOT/CLAUDE.md"        # fill the 6 TODO(team) fields at the top. Takes 3 minutes.

# ---- 3. prove the assistant reads it ---------------------------------------------
cd "$ROBOT" && claude
#   > What Java package do imports use in this project, and what must you never do
#   > without a human in the loop? Answer only from CLAUDE.md.
#   Correct answer names org.wpilib.* and the §9 never-list. If it says
#   edu.wpi.first.*, the file is not being read -- fix that before anything else.

# ---- 4. the single highest-payoff first task (see Sec 3, rank 1) ------------------
#   > Read src/test/java/. If there is no test that constructs RobotContainer,
#   > write one following the pattern in CLAUDE.md Sec 6. Do not touch src/main.
./gradlew test

# ---- 5. attribution, once, permanently (FIRST policy -- 00_FIRST_AI_POLICY) ------
cd "$ROBOT"
printf '\n## AI attribution\n\nPortions of this codebase were developed with AI assistance\n(Anthropic Claude Code). All code was reviewed, tested in simulation, and\nverified on hardware by Team TODO(team) students and mentors before use.\n' >> README.md
git add README.md CLAUDE.md && git commit -m "Add AI repo contract and attribution"
```

**Read the results in this order:** step 3 first (if the contract is not being read, nothing else in
this document works), then step 4 (the smoke test is the highest return-on-effort item in
`03_programming_stack.md` §7 and AI writes it in ninety seconds), then step 5 (zero-cost policy
compliance, and forgetting it is the only way this whole plan can cost you an award).

---

## §1. The 2026 tooling landscape, priced for a high-school team

### 1.1 What you are actually choosing between

Four products, three different shapes. The shape matters more than the brand.

| Shape | Products | What it does well | What it does badly |
|---|---|---|---|
| **Agentic CLI** — reads/writes many files, runs `./gradlew`, reads the error, iterates | **Claude Code** | Multi-file refactors, migrations, "make the tests pass", log analysis, repo-wide review | Easy to let it run unsupervised; a student can accept 400 lines they cannot explain |
| **IDE-embedded assistant** — chat + edits inside the editor, sees open files | **Claude in the IDE** (VS Code / JetBrains extension), **GitHub Copilot Chat**, **Cursor** | Explaining the file in front of you, targeted edits, staying inside the student's working context | Weaker at "change 14 files consistently" |
| **Inline completion** — ghost-text as you type | **GitHub Copilot**, **Cursor Tab** | Boilerplate typing speed, constants tables, getters | **Actively harmful to learning** if it is the student's first exposure — see §6.4 |

For this team the honest ranking is: **one agentic CLI seat for the mentor and the lead programmer,
free Copilot for every student who qualifies, and inline completion switched OFF for first-years.**

### 1.2 Cost and education programmes — verified 2026-08-22

| Tool | Consumer price | Education / nonprofit path | Label |
|---|---|---|---|
| **Claude Code** | Included in Claude **Free**, **Pro** ($20/mo monthly, $17/mo billed annually), **Max 5x** (from $100/mo), **Max 20x** | An institution-wide **Education plan** exists ("a comprehensive university-wide plan for an institution, including its students, faculty, and staff"); **no published price**, and it is described in university terms — whether a K-12 district or a robotics team qualifies is not stated | **[C]** prices/inclusion from [claude.com/pricing](https://claude.com/pricing), fetched 2026-08-22. Education plan applicability to a high-school team: **UNVERIFIED** |
| **Claude in the IDE** | Same subscription — it is a front-end on the same account, not a separate SKU | Same as above | **[C]** same source |
| **GitHub Copilot** | Paid Pro/Pro+ tiers | **Free for verified students and teachers** via **GitHub Education**. Eligibility per GitHub's docs: at least **13 years old** and enrolled in "a degree- or diploma-granting program, such as a **high school**, college, university, or homeschool" | Eligibility **[C]** from [docs.github.com](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student), fetched 2026-08-22. The exact 2026 benefit bundle (which Copilot tier, credit allowances) is **UNVERIFIED** — secondary sources describe unlimited completions plus a monthly AI-credit allowance for chat/agent use; confirm on GitHub's own page before planning around it |
| **Cursor** | Free tier; paid Pro | **The legacy student discount is closed to new sign-ups as of 2026-06-25.** Cursor's own students page now says only "Anyone can get started with Cursor for free" and points at campus/online event promotions. Existing holders keep their rate until expiry | Closure date and current page wording: **[C]-ish** — the closure date comes from Cursor community/forum discussion and is **UNVERIFIED** against a first-party announcement; the current [cursor.com/students](https://cursor.com/students) page text is **[C]**, fetched 2026-08-22, and notably **does not offer a free student year** |

**Do not budget on the Cursor student year.** It was the standard advice in FRC circles through
early 2026 and it is no longer available to new applicants. This is exactly the kind of claim that
rots; re-verify in November.

### 1.3 The recommendation, with dollars

| Line | Who | Cost | Rationale |
|---|---|---|---|
| **1× Claude Pro** ($17/mo annual, $204/yr — or $20/mo for the 5 months Nov–Mar = $100) | Mentor account, used for repo-wide work, migration, log analysis, review | **$100–204** | This is the seat that buys down the ~40 h Systemcore-port inflation (§3, rank 2). Month-to-month for Nov–Mar is the cheaper shape for a seasonal team and you can cancel in April |
| **GitHub Copilot via GitHub Education** | Every student ≥13 in a diploma-granting programme | **$0** | Free, and the verification is a school email or student ID. Do this in **October**, not January — verification is not instant |
| **Cursor** | — | **$0** | Free tier only. Do not pay; do not plan on a student discount |
| **Claude Max** | — | **$0** | **Do not buy.** Max is a throughput product for people who hit Pro limits daily. A team burning 134.8 programming hours across a whole season will not. Revisit only if the Pro seat actually rate-limits during week 4 |

**Total AI tooling budget: $100–204.** Against `robot_discretionary: 2500` in
[`team_capacity.yaml`](../team_capacity.yaml) that is **4–8% of the discretionary robot budget**, and
it is competing with real parts. Justify it against §3 rank 1–3 or don't spend it.

### 1.4 Things a school district will ask you, that this file cannot answer

`00_FIRST_AI_POLICY_VERIFIED.md` is explicit that FIRST's permission covers **eligibility and
judging only**. Three open items, all **UNVERIFIED**, all of which need a human answer before
students create accounts:

1. **District AI policy.** Usually stricter than FIRST's. Check it in September, in writing.
2. **Minimum ages and account terms.** GitHub Education states 13+. The other vendors' minimum ages
   and parental-consent requirements were not verified for this file. Read each vendor's terms.
3. **Whose account.** A mentor-owned seat that students use under supervision has very different
   data and consent implications from fifteen student-owned accounts. Decide deliberately.

### 1.5 Why every number in §1.2 has a shelf life

In the twelve months before this file was written, the following changed: Copilot's student sign-ups
were paused and then reopened; Cursor's student discount closed to new applicants; Claude's pricing
page moved domains (`anthropic.com/pricing` now 301s to `claude.com/pricing`). **Treat §1.2 as a
snapshot, not a fact.** Re-verify at the **2026-11-12** Pre-Kickoff Virtual Kit Release checkpoint,
when you are already re-checking the vendor-library table in `03_programming_stack.md` §0.

---

## §2. The repo contract: why `CLAUDE.md` is the whole safety story

An AI assistant with no project context will write `edu.wpi.first.wpilibj2.command.SubsystemBase`,
call `motor.set(0.5)`, use `MathUtil.clamp()`, override `robotInit()`, and construct an
`XboxController` — **five API errors in one file**, every one of them correct for 2026 and wrong for
2027. It does this because every tutorial, every Chief Delphi post, and every public FRC repo in its
training data is 2026-or-earlier. `03_programming_stack.md` §0 names this directly: *"Every import in
every tutorial, Chief Delphi post, and AI model output is wrong."*

`CLAUDE.md` is a file at the repo root that the assistant reads before it does anything. It is where
you tell it the five things above, plus your architecture, your units convention, and the list of
actions it may never take without a human. **[`templates/frc-robot-CLAUDE.md`](templates/frc-robot-CLAUDE.md)
is a complete, fill-in-six-blanks version of that file.** It is the single highest-leverage artifact
in this whole document, and copying it costs three minutes.

Two things about it that matter:

- **It is read by more than Claude Code.** Cursor reads `CLAUDE.md`-style rules files; Copilot reads
  `.github/copilot-instructions.md`. If you use both, symlink or duplicate. **[S]** on the exact
  behaviour of each product's rules-file discovery in its 2026 build — verify by asking the
  assistant to quote the file back at you (§0 step 3), which is the only test that actually proves it.
- **It is judging evidence.** A repo with a written AI contract, an attribution line, and a
  pre-actuation checklist is a concrete artifact for a judge asking how your team manages engineering
  process — see [`../awards/AWARD-ALIGNMENT.md`](../awards/AWARD-ALIGNMENT.md).

---

## §3. High-value uses, ranked by payoff

**How the ranking works.** *Payoff* = hours returned against the **134.8 h programming budget**
(`team_capacity.yaml`, `hours.allocation.programming`). *Risk* = what happens if the AI is wrong and
nobody catches it. **Every hours figure is [S]** — a model estimate, not a measurement — and is
stated as a fraction of that 134.8 h so it stays honest. Nothing here can be [C] until you run a
season and measure it; §10 tells you how.

| # | Use | Est. hours returned **[S]** | % of 134.8 h | Risk if wrong | Verify by |
|---|---|---|---|---|---|
| **1** | **Simulation + unit tests** (§3.1) | 18–30 | 13–22% | **Low** — a wrong test fails loudly, or passes and teaches you nothing. It never moves a motor | `./gradlew test`; read the assertions yourself |
| **2** | **roboRIO→Systemcore / WPILib 2027 port** (§3.2) | 15–25 | 11–19% | **Medium** — a mis-ported unit or sign is a real hazard | Compile + sim + §5 gate |
| **3** | **Scaffolding subsystems & commands from a written spec** (§3.3) | 12–20 | 9–15% | **Medium** | §5 gate |
| **4** | **Log analysis: WPILOG / AdvantageScope → engineering report** (§7) | 8–15 | 6–11% | **Low** — read-only, produces prose | Cross-check one claim against AdvantageScope by hand |
| **5** | **Code review for classic FRC bugs** (§3.4) | 6–12 | 4–9% | **Low** — finds bugs, does not create them. False positives cost minutes | Human triages every finding |
| **6** | **Porting vendor examples** into your architecture (§3.5) | 5–10 | 4–7% | **High** — hallucinated vendor APIs live here | Javadoc/vendor-docs check, every symbol |
| **7** | **Explaining vendor APIs & diffing WPILib versions** (§3.6) | 4–8 | 3–6% | **Medium** — confident wrong explanations | Ask for the doc URL; open it |
| **8** | **Characterisation data → constants** (SysId) (§3.7) | 3–6 | 2–4% | **High** — bad kV/kA drives hard into a hard stop | Sim first, then §5 gate |
| **9** | **Auto path / routine scaffolding** (§3.8) | 3–6 | 2–4% | **Medium** | Sim, then a slow-speed field run |
| **10** | **Onboarding docs & code explanations for the wiki** (§3.9) | 3–5 | 2–4% | **Low** | A student who was not in the room reads it and it makes sense |
| | **Total, if you do all of it** | **77–137** | **57–102%** | | |

**Read that total honestly.** It is not credible that AI returns your entire programming budget.
Ranks overlap, estimates are optimistic by construction, and every hour "returned" is partly spent
on review. **A defensible planning number is the top four only: 53–90 h, or 39–67% of the programming
budget.** That is still, against 79% pre-committed utilisation (§3.2 of the capacity model), the
difference between a team that can absorb a week-5 mechanism change and one that cannot.

### 3.1 Rank 1 — simulation and unit tests

**Why this is number one for *this* team specifically.** You have no 2027 robot, no 2027 game, and
`03_programming_stack.md` §7 already establishes that simulation is the largest equaliser available
to a small team. The bottleneck on simulation is not knowledge — it is that writing an `*IOSim`
class and a JUnit harness is tedious, unglamorous work that competes with building the robot. That
is precisely the work to hand to an assistant: **mechanical, well-specified, verifiable by running
it, and incapable of hurting anyone because no motor is attached.**

Three concrete jobs, in order:

1. **The `createRobotContainer()` smoke test.** `03_programming_stack.md` §7 calls this the highest
   return-on-effort item in that document — it is 6328's *entire* public test suite. AI writes it in
   under two minutes including the `HAL.initialize(500, 0)` boilerplate. Do it in the first hour.
2. **`*IOSim` implementations** from the WPILib physics classes (`FlywheelSim`, `ElevatorSim`,
   `SingleJointedArmSim`, `DCMotorSim`). You supply the gearing, moment of inertia and motor type;
   the assistant writes the plumbing. **You must supply the physical numbers** — see §4.3.
3. **Command-level tests** using the 1678 `TestUtil.tick(int)` pattern (verbatim in
   `03_programming_stack.md` §7). "Run this command for 2 s and assert the mechanism arrived" is a
   test shape an assistant produces reliably, and it is the shape that catches the bugs that cost
   matches.

**The trap.** An AI will happily generate a test that asserts what the code *does* rather than what
it *should do* — a tautology that passes forever and protects nothing. Guard: **the student writes
the assertion values from the spec before the AI writes the test body.** Prompt template #3.

### 3.2 Rank 2 — the roboRIO→Systemcore port (the 2027-specific case)

This is the single most 2027-shaped use of AI on this team, and the capacity model quantifies the
prize: **programming demand is inflated by roughly 40 h purely by the platform change**
(`02_TEAM_CAPACITY_MODEL.md` §3.1–3.2). That is 30% of the programming budget spent on translation
rather than on winning matches.

**Why AI is unusually good at this specific job.** The 2027 migration is dominated by *mechanical,
high-volume, low-judgement* transformations — exactly the class of work where an assistant with a
written rule table outperforms a tired student at 11 PM:

| Transformation | Judgement required | Good AI job? |
|---|---|---|
| `edu.wpi.first.*` → `org.wpilib.*` (Java); `frc::` → `wpi::` (C++) | None | **Yes** — but a `sed` also does it; use AI for the cases `sed` misses |
| `motorController.set(x)` → `setThrottle(x)`; `stopMotor()` → `disable()` | None | **Yes** |
| `MathUtil.clamp()` → `Math.clamp()` | None | **Yes** |
| `robotInit()` → `Robot()` constructor | Low — ordering can matter | **Yes, with review** |
| `XboxController`/`PS4Controller`/`PS5Controller` → unified `Gamepad` | Low | **Yes, with review** |
| `PIDCommand` / `ProfiledPIDCommand` / `TrapezoidProfileCommand` removed → use controllers directly | **Medium** — this is a redesign, not a rename | **Draft only** |
| `RamseteController` → **LTV Unicycle Controller** | **Medium** — different tuning semantics | **Draft only** |
| Mutable Java units → immutable units | Low–Medium | **Yes, with review** |
| `Timer.getFPGATimestamp()` → `Timer.getTimestamp()` (also a replay-determinism rule) | Low | **Yes** |
| **`Rotation2d.getRadians()/getDegrees()/getRotations()` now return *wrapped* angles** | **HIGH** | **NO — human only. See below** |
| Removed hardware: `Servo`, `Ultrasonic`, `Relay`, `Counter`, `SPI`, Analog Gyro/Output/Trigger, DMA, Interrupts | **HIGH — mechanical consequences** | **NO — this is a design decision** |

**The two red rows are the whole point of doing this with a checklist rather than a bulk prompt.**

- **Wrapped `Rotation2d` getters** are the nastiest change in WPILib 2027 because *the code still
  compiles and still runs*. Any turret, arm, or climber logic that accumulated continuous rotation
  from those getters silently changes behaviour. An assistant asked to "migrate this file" will
  translate the imports and leave the bug. **Instruct it to find and flag, not to fix**: prompt
  template #2 makes the assistant produce a *report* of every `Rotation2d` getter call site with its
  surrounding context, which a human then reads. That is a fifteen-minute human job on a real repo,
  and it is the fifteen minutes that prevents a turret unwinding itself into a wire harness.
- **Removed hardware is a mechanical problem wearing a software costume.** `Servo` is gone because
  Systemcore cannot power hobby servos. If your intake gate is a servo, the answer is not a code
  change, it is a different actuator, and that lands in `fabrication_assembly` (129.8 h) not
  `programming` (134.8 h). **An AI told to "make this compile" will delete the servo code and hand
  you a robot with no gate.** The correct instruction is *"list every removed-API usage and what
  hardware it drives; propose nothing."*

**The off-season action.** `03_programming_stack.md` §0 already tells you to install WPILib 2027
alpha and build a skeleton now. Add this: **use one October session to have the assistant produce a
migration rule table from the WPILib "New for 2027" and "Removed features for 2027" pages, verify
every row against those pages yourself, and paste the verified table into `CLAUDE.md` §3.** The
template already ships with a starting version. Once that table is in the repo contract, every
subsequent generation is 2027-correct by default instead of 2026-correct by default — which is the
difference between AI helping and AI generating forty hours of subtle rework.

There is also a real migration tool to read rather than reinvent: **[FRC3476/2027-Migrator](https://github.com/FRC3476/2027-Migrator)**
(cited in `03_programming_stack.md` §0). Have the assistant *explain* it; do not have it rewrite it.

### 3.3 Rank 3 — scaffolding subsystems and commands from a spec

The pattern that works, and the ordering is not optional:

```
student writes the spec  →  AI writes the boilerplate  →  student reviews and owns it
```

A **spec** is not "make an intake." It is the six things prompt template #1 demands: mechanism
purpose, actuators and their controllers/CAN IDs, sensors, the state machine (named states and legal
transitions), the safety limits (current limit, soft limits, what happens on disable), and the
units of every public method. **Writing that spec is the engineering.** It takes a student twenty
minutes and it is the part they should never delegate. The 300 lines of `SubsystemBase` plumbing,
`@AutoLog` inputs class, IO interface, sim implementation and config object that follow are
transcription, and that is the part to delegate.

**This composes with the 2910 base-subsystem pattern** in `03_programming_stack.md` §7 far better
than it composes with hand-rolled subsystems. Once `RollerMotorSubsystem` and `ServoMotorSubsystem`
exist — written once, in December, by humans, carefully — a new mechanism is a config object plus a
state machine, and *that* is a 40-line generation a student can actually review line by line. **Build
the base classes yourself; generate the mechanisms.** Inverting that is how you end up with a repo
nobody understands.

### 3.4 Rank 5 — code review for classic FRC bugs

This is the best risk-adjusted use in the whole list: it **finds** defects and cannot **create**
them. Point the assistant at a diff with the checklist below (prompt template #5). Every one of
these is a bug class that has cost real teams real matches:

| Bug class | What it looks like | Why AI catches it well |
|---|---|---|
| **Unit errors** | degrees into a radians parameter; rotations vs. rotations-of-the-mechanism after gearing; inches into a metres API | Pattern-matchable at the call site; WPILib's `Units` types make the mismatch visible |
| **Inverted motors / sensors** | a follower not inverted; encoder sign opposite the motor; `setInverted` applied after config is applied | Structural — the assistant compares the two motors' configs |
| **Unclamped setpoints** | `setPosition(joystickValue * 100)` with no soft limit | Trivially detectable: a setpoint path with no clamp between input and output |
| **Missing deadbands** | drivetrain creeps because a stick rests at 0.02 | Detectable at the input boundary |
| **Blocking calls in `periodic()`** | `Thread.sleep`, `while` loop, `.get()` on a future, file or network I/O, a `System.out.println` flood | Very reliable — a syntactic search with semantic judgement |
| **CAN flooding** | status-frame periods left at default on 30 devices; `getX()` called repeatedly per loop instead of cached | Detectable by counting calls per loop; needs a human to judge the budget |
| **Unsafe defaults** | no default command on a subsystem that holds position; no current limit; motor `NeutralMode` unset; `setSafetyEnabled` assumptions | Checklist-shaped |
| **Replay determinism violations** | `Timer.getFPGATimestamp()`, `Math.random()`, `HashMap` iteration, NT reads as inputs, threads in robot logic | The list in `03_programming_stack.md` §3 is finite and mechanical — perfect for automated review |

**Run this on every PR before merge, and on the whole repo once in the week before your event.**
Cost: minutes. It is also the review that is *most* worth having when your one confident programmer
is the person who wrote the code.

### 3.5 Rank 6 — porting vendor examples

Vendor examples (CTRE Phoenix 6, REVLib, PathPlannerLib, PhotonVision) are written as standalone
demos. Getting them into an IO-layer architecture is real work, and an assistant does the
restructuring well. **It is rank 6 and not rank 3 because this is where hallucinated vendor APIs
live** — see §4.1. Hard rule: **the assistant may only use vendor symbols that appear in the example
you pasted, or that it cites a documentation URL for.** Prompt template #10 is the verification
prompt; use it on every unfamiliar symbol.

### 3.6 Rank 7 — explaining APIs and diffing WPILib versions

"What does `odometryUpdateFrequency` default to on CAN FD?" "What is the difference between
`estimateCoprocMultiTagPose` and `estimateLowestAmbiguityPose`?" "What changed in `TrapezoidProfile`
between 2025 and 2026?" These are genuinely useful and genuinely fast. **They are also where a
confident wrong answer costs you the most, because you will not test an explanation.** Guard: ask
for the documentation URL with every answer, and open it. If the assistant cannot produce a URL, the
answer is a guess. Prompt template #10 builds this in.

### 3.7 Rank 8 — characterisation data → constants

SysId produces kS, kV, kA, kG. Turning a `SysIdRoutine` log into a populated `Constants` block is
mechanical and AI does it fine. **It is ranked low because the failure mode is severe:** a kV off by
10× produces a mechanism that slams into its hard stop at full voltage. **Never** let generated
feedforward constants reach hardware without (a) sim first, (b) the §5 gate, (c) a first run at
reduced voltage limit with a hand on the disable. Prompt template #8.

### 3.8 Rank 9 — auto path and routine scaffolding

`03_programming_stack.md` §5 recommends PathPlanner for 2027, partly because its GUI auto-builder
lets a *student* compose autos without touching Java. **That recommendation and this section are in
tension, and the GUI wins.** Use AI for the Java side only: registering named commands, writing the
`SendableChooser` wiring, generating the mode-aware selection logic, and — the actually valuable bit
— writing the **test** for auto selection (1678 ships an `AutoModeSelectorTest` and an
`AutoPlannerTest`; copy that). Do not use AI to invent path waypoints; it has no idea where your
field elements are.

### 3.9 Rank 10 — onboarding docs

Low hours, but note that YETI 3506's public engineering wiki is called out in
`03_programming_stack.md` §6 as a cheap, high-value practice that doubles as judging evidence. An
assistant turning `subsystems/` into a readable "how our robot code works" page is a twenty-minute
job that produces an award-submission artifact. Cross-reference
[`../awards/01_AWARD_WINNING_PATTERNS.md`](../awards/01_AWARD_WINNING_PATTERNS.md).

---

## §4. Low-value and dangerous uses — the blunt section

The user of this document makes budget decisions from it. So: **here is what AI does badly, stated
without hedging.**

### 4.1 Hallucinated vendor APIs — the single most common failure

Ask for Phoenix 6 or REVLib code and you will get a method that does not exist, with a plausible
name, correct-looking parameters, and total confidence. It happens because vendor APIs churn every
season, the training data contains four generations of them simultaneously, and the model has no way
to know which one your `vendordeps/` pins.

It is **worse in 2027 than in any prior season**, because `03_programming_stack.md` §0 documents that
every 2027 vendor library is in *alpha*: Phoenix 6 `v26.50.0-alpha-1`, REVLib `v2027.0.0-alpha-2`,
PathPlannerLib `v2027.0.0-alpha-3`. Alpha APIs are not in training data at all, and the model will
substitute the 2026 API it does know. **AdvantageKit's own package name moved from
`org.wpilib.commands3` to `org.wpilib.command3` between alphas** — a one-character difference that no
model can be expected to know and that produces an import error at best and a wrong-class match at
worst.

**Mitigations, in order of effectiveness:**
1. **Compile early and often.** A hallucinated symbol is a compile error, and compile errors are the
   cheapest bugs in existence. Any workflow where generated code is not compiled within sixty
   seconds is broken.
2. **Paste the actual API surface into context** — the vendor's example file, or the Javadoc page —
   rather than asking from memory.
3. **Demand a citation** for every unfamiliar symbol (prompt #10).
4. **Pin your vendordeps in `CLAUDE.md`** with exact versions. The template has a slot for this.

### 4.2 Subtly wrong control math

This is more dangerous than §4.1 because **it compiles**. Categories seen repeatedly:

| Failure | What it produces |
|---|---|
| Feedforward and feedback summed in different units (volts vs. duty cycle) | A mechanism that is either inert or violent, depending on sign |
| Gearing applied once, twice, or not at all between motor rotations and mechanism units | Setpoints off by the gear ratio — often 9×, 25×, 100× |
| Sign conventions: motor positive vs. mechanism positive vs. encoder positive | Positive feedback loop. The mechanism accelerates away from its setpoint until something breaks |
| Continuous-input / wrapping on a turret PID left off, or on where it should be off | Turret takes the long way around, or unwinds its wiring |
| `Rotation2d` wrapped getters (2027) used where continuous angle was assumed | Silent behaviour change, compiles clean — see §3.2 |
| Trapezoid profile constraints in the wrong units | Profile completes "instantly" and the controller commands a step input |
| Integral term with no anti-windup, on a mechanism against a hard stop | Integrator winds up while stalled; releases catastrophically |

**The general rule: AI is good at code shape and bad at physical quantity.** It does not know your
gear ratio, your moment of inertia, your motor's free speed under load, or which direction "up" is
on your elevator. **If a number describes the physical world, a human supplies it.** Put that
sentence in your `CLAUDE.md` — the template does.

### 4.3 Why untested generated code near a competition robot is a safety issue

Per `00_FIRST_AI_POLICY_VERIFIED.md`, the 2026 mass limits were **115.0 lb bare** (R103, excluding
bumpers, battery, event tags) and **135.0 lb with bumpers** (R408). **[H]** for 2027 — re-verify
against the BIOCORE manual on kickoff day. Either way:

- A swerve drivetrain accelerates a 135 lb mass to competitive speeds in about a second.
- An elevator carrying a mechanism, driven by a Kraken through a 9:1 reduction, has enough authority
  to remove a finger and to destroy itself against a hard stop.
- A flywheel at several thousand RPM stores real energy and does not stop when the code does.

**A sign error is not a bug in this environment. It is a hazard.** The specific pathology of
AI-generated code is that it *looks* reviewed: consistent style, sensible names, plausible comments,
no obvious smell. Human code that is wrong usually looks wrong. **Generated code that is wrong looks
finished.** That is the entire safety argument, and it is why §5 exists as a gate rather than as
advice.

### 4.4 Uses that are simply not worth the hours

| Don't | Why |
|---|---|
| Generate a whole robot project from a game description on kickoff day | You cannot review it, you will not understand it in week 5, and it will encode 2026 APIs |
| Ask AI for BIOCORE game strategy or rule interpretations | The game is not public. Anything it says is invented. Use [`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md) and the manual |
| Have AI tune PID gains from a description | It has never seen your mechanism. Use SysId (§3.7) and sim |
| Let AI write the base subsystem library (§3.3) | Written once, used everywhere, must be understood by everyone. Highest-value human code in the repo |
| Use inline completion to teach a first-year Java | §6.4. It short-circuits exactly the struggle that produces understanding |
| Ask for "the fastest auto" | Physics, field geometry, and your robot's real acceleration are all unknown to it |
| Debug a hardware problem in chat | CAN faults, brownouts, and loose crimps are not in the code. Go look at the robot |

---

## §5. The gate: what a human must verify before anything actuates

**This is the non-negotiable part of the document.** `00_FIRST_AI_POLICY_VERIFIED.md` states it
plainly: *"No policy makes unverified generated code safe... Human review before anything actuates
remains non-negotiable."*

Print this. Tape it above the programming bench. It is reproduced verbatim in the `CLAUDE.md`
template (§9) so the assistant itself will refuse to skip it.

### The five-gate pre-actuation checklist

**No AI-influenced code drives a motor on real hardware until all five are signed off by a named
human. Not the AI. A person, whose name goes in the commit message.**

| Gate | Question | Passed when |
|---|---|---|
| **G1 — Comprehension** | Can the student who owns this subsystem explain every line without the assistant open? | They explain it out loud to a second person. If they cannot, the code does not ship — regardless of whether it works. See §6.5 |
| **G2 — Units & signs** | Is every physical quantity's unit stated, and is every sign convention checked against the actual mechanism? | A human has written the units in the code (WPILib `Units` types or a suffixed name) **and** physically pushed the mechanism by hand to confirm the encoder increases in the expected direction |
| **G3 — Limits** | Current limit set? Soft limits set on both ends? Setpoints clamped between input and output? Behaviour on disable defined? | Each of the four is pointed at in the diff. "It's in the config somewhere" does not pass |
| **G4 — Simulation** | Has it run in sim, and does a test assert the intended behaviour? | `./gradlew simulateJava` shows sane behaviour **and** `./gradlew test` passes with an assertion a human wrote |
| **G5 — First motion** | Is the first real-hardware run bounded? | Reduced voltage/output limit, mechanism clear of people and structure, **a hand on the disable**, and one person watching who is not the person driving |

**Nothing in this checklist is AI-specific.** It is ordinary FRC safety discipline. AI's contribution
is that it makes it dramatically easier to produce a large volume of finished-looking code that
nobody has actually reasoned about, which is exactly the condition the checklist defends against.

**Enforcement that costs nothing:** a PR template with the five gates as checkboxes, and a rule that
`main` only takes reviewed PRs. Cost: one file. It is also, again, judging evidence.

---

## §6. Student learning: protocols so students end up knowing *more*

`00_FIRST_AI_POLICY_VERIFIED.md` is direct about this: *"Permission to use a tool is not a reason to
skip the thinking."* The team goal in this project is to move student hours **toward** hands-on work,
not to remove students from the intellectual work.

There is also a hard capacity fact behind this section. `02_TEAM_CAPACITY_MODEL.md` §3.2 sets an
action with a date on it: **develop a third programmer between 2026-09 and 2026-12.** A third
programmer is worth ~85 veq-h and would take programming from 79% to ~53% utilisation. **AI that
makes it easier to ship code without understanding it actively prevents that from happening**, and
therefore costs you more hours than it saves. The protocols below exist to make AI *produce* the
third programmer instead of *substituting* for them.

### 6.1 Protocol A — Explain Before Generate

**Rule: the assistant explains what it is about to write, and the student approves the plan, before
any code appears.**

Mechanically: start every session with a plan request, not a code request. Prompt template #6 does
this. The student must be able to answer "why that approach and not the other one" before the code
is written. This costs about ninety seconds per task and it is the difference between a student who
directed the work and a student who received it.

### 6.2 Protocol B — Student writes the spec, AI writes the boilerplate, student reviews

The division of labour from §3.3, stated as a rule:

| Student owns | AI may do | Never AI |
|---|---|---|
| The spec: purpose, states, transitions, limits, units | Boilerplate: IO interface, inputs class, config object, plumbing | The base subsystem library |
| Every physical number: gear ratios, MOI, limits, setpoints | Repetitive translation (imports, renames) | Physical numbers |
| The assertion values in tests | The test harness around those assertions | The safety-limit values |
| The final read-through and the commit | The first draft | The decision to run it on hardware |

**The spec is the deliverable.** A student who writes a good subsystem spec has done the engineering
whether or not they typed the `SubsystemBase` boilerplate. A student who typed 300 lines of
boilerplate but could not have written the spec has learned typing.

### 6.3 Protocol C — AI as Socratic tutor, not answer machine

The highest-value educational mode, and it needs an explicit instruction because the default
behaviour of every assistant is to answer. Prompt template #6 sets it up: the assistant is told to
ask questions, give hints at increasing specificity, and **not** to produce the answer until the
student asks three times.

This is the mode for:
- "Why is my PID oscillating?" → questions about gains, sensor noise, loop rate, mechanical slop
- "Why won't this command end?" → questions about `isFinished()`, requirements, interruption
- "What's a `Trigger`?" → an explanation with a question back to check it landed

It is *not* the mode for week-5 debugging at 10 PM. Have both prompts saved and switch deliberately.

### 6.4 The inline-completion problem, stated plainly

**Turn inline/ghost-text completion OFF for students in their first season of Java.**

The mechanism of harm is specific: completion fires *before* the student has formed the intent. The
struggle of "what do I even type next" is the exact moment learning happens, and completion removes
it and replaces it with a recognition task ("does this look right?"). A student can produce a
working file for a full season without ever having generated a line of Java from their own model of
the language. **[S]** — this is a pedagogical judgement, not a measured finding, and reasonable
people disagree. It is also cheap to reverse and expensive to discover you got wrong in April.

Chat and agentic modes do not have this problem, because the student must state the intent to get
anything at all.

Suggested policy: completion off for Y1, student's choice from Y2, always on for the mentor.

### 6.5 Assessing whether a student actually understands their code

Five assessments, cheapest first. Use them, because "the code works" is not evidence of anything.

| # | Assessment | How | What a pass looks like |
|---|---|---|---|
| **1** | **Explain it cold** | Close the laptop. "Walk me through what happens when the driver presses A." | They narrate the trigger → command → subsystem → IO chain in their own words |
| **2** | **Change it** | "Make it hold position instead of stopping when the button is released." | They know which file, which method, and what breaks |
| **3** | **Break it** | Mentor introduces one bug (flip a sign, remove a clamp, change a unit). "Find it." | Found in under ten minutes, and they can say *why* it was wrong |
| **4** | **Justify the numbers** | Point at any constant. "Where did this come from?" | "SysId, run on 2026-12-14, log is in `logs/`" — or an honest "I don't know", which is a finding |
| **5** | **The G1 test** | The gate in §5. Explain every line to a second person, no assistant open | The other person can then answer question 1 |

**Run assessment 3 on every student before your first event.** It takes ten minutes per student and
it is the closest thing to a real measure of whether your software knowledge is one deep or three
deep — which, per `02_TEAM_CAPACITY_MODEL.md` §6, is a named single-point-of-failure risk on this
team ("Lead programmer ↔ sole mechanical fixer").

### 6.6 What to do when a student cannot pass

Not "don't use AI." **Reduce the scope of what the AI produced** until the student can explain it,
then let them extend it themselves. A 40-line subsystem a student owns beats a 400-line one they
host. This also happens to be the right answer for the repo.

---

## §7. The post-match log-analysis pipeline

**The goal:** between matches, a student dumps the log off the robot, runs one command, and gets an
engineering report the drive team and the programmers can act on before the next match. This is
rank 4 in §3, it is read-only, and it is the best demonstration in this document of AI absorbing
desk work so students can be on the field.

### 7.1 The pipeline

```
  Systemcore / USB stick                     laptop in the pit
  ┌──────────────────┐   1. copy    ┌───────────────────────────────┐
  │  *.wpilog        │ ───────────► │ tools/log-report.py --extract │
  │  (DataLogManager │              │   WPILOG -> flat CSV + JSON   │
  │   or AdvantageKit)│              │   summary of key signals      │
  └──────────────────┘              └──────────────┬────────────────┘
                                                   │ 2. summarise
                                                   ▼
                                    ┌───────────────────────────────┐
                                    │ claude -p "$(cat prompt.md)"  │
                                    │   summary JSON in context     │
                                    └──────────────┬────────────────┘
                                                   │ 3. report
                                                   ▼
                                    ┌───────────────────────────────┐
                                    │ reports/match-NN.md           │
                                    │  - what happened, timestamped │
                                    │  - anomalies + evidence       │
                                    │  - ranked actions before next │
                                    └───────────────────────────────┘
```

**Design decision that makes this work: never send the raw log to the model.** A match log at 50 Hz
across a few hundred signals is far too large, and the model is bad at arithmetic over long numeric
sequences anyway. **The script does the numerics; the model does the interpretation.** That split is
what makes the output trustworthy — every number in the report came from Python, not from a
language model.

### 7.2 The script

Written by this pass to [`../../tools/log-report.py`](../../tools/log-report.py). It is a pure-Python
WPILOG reader (no WPILib install needed) plus a signal summariser. Usage:

```bash
# 1. Extract and summarise. Produces reports/match-07.summary.json + .csv
python tools/log-report.py extract logs/match-07.wpilog --out reports/match-07

# 2. What signals does this log even have? (run this the first time, always)
python tools/log-report.py entries logs/match-07.wpilog | head -50

# 3. Summarise only the signals you care about, with your own thresholds
python tools/log-report.py extract logs/match-07.wpilog --out reports/match-07 \
    --include "Drive/*" --include "*Current*" --include "*/Setpoint" \
    --brownout-volts 6.3 --loop-overrun-ms 20

# 4. Hand the SUMMARY (not the log) to the assistant
claude -p "$(cat reference/ai-integration/templates/programming-prompts.md \
             | sed -n '/### 7\./,/^### 8\./p')  \
           $(cat reports/match-07.summary.json)" > reports/match-07.md
```

**⚠ PARTLY VERIFIED — test it against a real log before you depend on it.** The WPILOG binary
format used by `log-report.py` is implemented from the published WPILOG specification (magic
`WPILOG`, u16 version, extra-header string; then records of
`[bitfield][entry id][payload size][timestamp][payload]`, with control records on entry 0 carrying
Start/Finish/SetMetadata).

- **Verified on 2026-08-22:** the reader round-trips a hand-built, spec-conformant log — header,
  Start records, `double` and `boolean` data, variable-width id/size/timestamp fields — and produces
  correct statistics and a correct low-voltage event. The script runs; the logic is sound.
- **Not verified:** it has **never been run against a real robot log.** The synthetic test proves the
  reader agrees with *my reading of the spec*; it cannot catch a misreading of the spec.

**Run `python tools/log-report.py entries <a real 2026 .wpilog>` in October** (§9). If the format
differs, the fix is contained to `_read_header` / `_read_records`. Do not discover this in the pit.

### 7.3 What the report should contain, and what it must not

| The report SHOULD | The report MUST NOT |
|---|---|
| Timeline of match phases with timestamps | Assert a cause it cannot see (mechanical slop, a loose crimp) |
| Every loop overrun, with duration and what ran | Invent a number not present in the summary JSON |
| Brownout events with voltage floor and preceding current draw | Recommend a gain change without saying what evidence supports it |
| Commands scheduled/interrupted, with times | Claim the robot "should have" scored without knowing the game |
| Setpoint vs. measured error, per mechanism, with max and settle time | Speak about BIOCORE rules — it does not know them |
| Pose-estimator discontinuities and vision-measurement rejections | |
| CAN utilisation and any device that dropped off the bus | |
| **A ranked list of ≤5 actions before the next match** | |

**Every claim in the report must cite a timestamp.** Put that in the prompt — template #7 does. A
report you cannot audit against AdvantageScope is worse than no report, because it is confident.

### 7.4 Where the human stays

Read the report, then **open AdvantageScope and look at the top-ranked finding yourself.** The report
is a search-space reducer, not a conclusion. Budget five minutes per match; you have between six and
twelve matches at an event and this is a `drive_practice` / `integration_debug` activity, not a
`programming` one (54.9 h and 84.9 h respectively in `team_capacity.yaml`).

---

## §8. Attribution and policy compliance — the zero-cost part

Per [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) (authoritative), FIRST permits
AI and requires credit: *"Proper Credit can look like this: 'Essay created by Team XXXX and ChatGPT.'"*
Judges may not rank a team lower for using AI.

**Three artifacts, ten minutes total, done once in October:**

1. **`README.md` attribution block** — §0 step 5 writes it.
2. **Commit trailers.** If a commit contains AI-assisted code, say so in the trailer. This is not
   required by FIRST, it is cheap, and it makes the repo self-documenting for the judge who asks.
3. **A one-paragraph team AI policy** naming: which tools, who may use them, the §5 gate, the §6
   learning protocols, and the district policy you checked. Cross-link from
   [`../team-ops/05_business_awards_sustainability.md`](../team-ops/05_business_awards_sustainability.md).

**The failure mode is forgetting, not overusing.** Cost of compliance ≈ zero; cost of
non-compliance is an integrity finding.

---

## §9. The off-season calendar for this file

Slotted against the dates in [`../../INDEX.md`](../../INDEX.md) and the fall programme in
`02_TEAM_CAPACITY_MODEL.md` §7.5.

| When | Action | Owner | Cost |
|---|---|---|---|
| **Sept 2026** | Check district AI policy in writing (§1.4). Decide account model | Mentor | 1 h |
| **Sept 2026** | GitHub Education verification for every eligible student (§1.2) — start early, it is not instant | Students | 0.5 h each |
| **Oct 2026** | Drop `CLAUDE.md` into the 2027 skeleton repo; run §0 step 3 | Lead programmer | 0.5 h |
| **Oct 2026** | Build the verified 2027 migration rule table into `CLAUDE.md` §3 (§3.2) | Mentor + lead | 2 h |
| **Oct 2026** | Run `tools/log-report.py entries` against a real 2026 log; fix the format reader if needed (§7.2) | Programmer #2 | 1 h |
| **Oct–Dec 2026** | **Third-programmer development using §6 protocols** — this is the capacity-model action item | Mentor | 1 h/wk |
| **Nov 12 2026** | Re-verify §1.2 pricing and education programmes at the Kit Release checkpoint (§1.5) | Mentor | 0.5 h |
| **Dec 2026** | Humans write the 2910-style base subsystem library. **Not AI.** (§3.3) | Both programmers | 8–12 h |
| **Dec 2026** | Generate `*IOSim` + tests for the base library using §3.1 | Programmers | 3 h |
| **Jan 9 2027** | Kickoff. §0 step 4 on the new repo within the first hour | Lead | 0.2 h |
| **Every PR** | §5 five-gate checklist; §3.4 review prompt | Whoever reviews | 10 min |
| **Every match** | §7 pipeline | Programmer in the pit | 5 min |

---

## §10. Validation — how you know any of this was true

**None of the hours estimates in §3 are measurable today.** They are **[S]**. Here is the cheapest
way to convert them to **[C]** by April 2027:

1. **Log every AI-assisted task** in one line: task, minutes of AI time, minutes of human review,
   whether it shipped. A three-column text file. Thirty seconds per task.
2. **Count G-gate rejections.** Every time the §5 checklist stops something, record which gate and
   what the defect was. If G2 (units/signs) dominates, §4.2 was right and your `CLAUDE.md` units
   section needs strengthening. If G1 (comprehension) dominates, §6 is failing and you are
   generating faster than you are learning.
3. **Measure the third-programmer outcome.** By 2026-12-31, can a third student pass §6.5
   assessment 3? That is the capacity-model action item and it is binary.
4. **Compare actual programming hours to 134.8.** Run `python tools/capacity_model.py` in April with
   your real logged hours. If programming came in under budget, this document worked. If it came in
   over *and* you used AI heavily, §4 was the more important half of this file.

**Falsifiers — things that would prove parts of this document wrong:**

| Claim | Falsified if |
|---|---|
| §3 rank 1 (tests are the top payoff) | You write the tests and still burn >134.8 programming hours |
| §3.2 (AI buys down the port cost) | The migration takes ≥40 h anyway, i.e. AI returned nothing on the platform change |
| §4.1 (hallucinated vendor APIs are the top failure) | Your G-gate log shows unit/sign errors dominating instead |
| §6.4 (inline completion harms first-years) | A first-year using completion all season passes assessment 3 |
| §1.3 (Pro is enough; Max is unnecessary) | You hit rate limits during week 4 with one seat |

---

## Files written by this pass

| Path | What it is |
|---|---|
| [`reference/ai-integration/01_ai_for_programming.md`](01_ai_for_programming.md) | This file |
| [`reference/ai-integration/templates/frc-robot-CLAUDE.md`](templates/frc-robot-CLAUDE.md) | Complete drop-in repo contract for an FRC Java robot repo on WPILib 2027 / Systemcore. Six `TODO(team)` fields to fill |
| [`reference/ai-integration/templates/programming-prompts.md`](templates/programming-prompts.md) | 13 ready-to-paste prompt templates, each with when-to-use, the paste block, and what you must check afterward |
| [`tools/log-report.py`](../../tools/log-report.py) | Pure-Python WPILOG reader + signal summariser feeding the §7 pipeline. 511 lines, no dependencies. Round-trips a synthetic log; **untested against a real one — see §7.2** |

---

## Known limitations

1. **Every hours figure in §3 is [S].** They are model estimates denominated in the 134.8 h
   programming budget, not measurements. §10 is how you fix that. Do not present them to a sponsor
   or a judge as findings.
2. **`tools/log-report.py` has never been run against a real WPILOG file.** It is verified to
   round-trip a hand-built spec-conformant log (§7.2), which proves the code works but not that my
   reading of the spec is right. It is scheduled for October validation in §9. **Treat it as a
   working tool against an unproven assumption**, and validate it before an event, not at one.
3. **§1.2 pricing and education programmes rot fast.** Three of the four rows changed within twelve
   months of writing. The Copilot Education benefit *bundle* (which tier, what credit allowance) is
   **UNVERIFIED** — only eligibility is confirmed. Cursor's student-discount closure date comes from
   community discussion, not a first-party announcement.
4. **No 2027 vendor API is stable.** Everything in §3.2's rule table is derived from WPILib's
   published "New for 2027" / "Removed features for 2027" pages as summarised in
   `03_programming_stack.md`. Those pages are for a product in alpha and will change before kickoff.
   The table in `CLAUDE.md` §3 must be re-verified in November and again at kickoff.
5. **§6.4 (inline completion harms first-year learners) is a judgement, not a study.** It is marked
   **[S]** and it has a named falsifier in §10. If your students are already fluent Java
   programmers, it likely does not apply.
6. **This file says nothing about the BIOCORE game**, because BIOCORE's rules are not public as of
   2026-08-22. Any AI assistance related to game strategy, scoring, or rules belongs in
   [`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md) and
   [`../QA-AMBIGUITY-HOTSPOTS.md`](../QA-AMBIGUITY-HOTSPOTS.md), and must be driven by the actual
   manual, not by a model's guess.
7. **Minors' data and vendor account terms are an open item**, exactly as
   `00_FIRST_AI_POLICY_VERIFIED.md` flags. §1.4 names it; it does not resolve it. That requires a
   human reading each vendor's terms of service and your district's policy.
8. **Model behaviour is not a stable input.** Everything in §4 describes failure modes observed in
   the 2026 generation of these tools. They will change. §5's gate is deliberately written so that
   it stays correct even if the models get much better — because the hazard is a 135 lb robot, not a
   model.
