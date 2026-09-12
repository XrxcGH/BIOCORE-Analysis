# Programming prompt templates — paste-ready

**Purpose.** Thirteen prompts a student or mentor can paste without thinking. Each one carries the
guardrails from [`../01_ai_for_programming.md`](../01_ai_for_programming.md) inside the prompt text,
so the guardrail travels with the prompt instead of living in someone's memory.

**Companion files:** [`../01_ai_for_programming.md`](../01_ai_for_programming.md) (the ranking and
the reasoning) · [`frc-robot-CLAUDE.md`](frc-robot-CLAUDE.md) (the repo contract these assume is in
place) · [`../00_FIRST_AI_POLICY_VERIFIED.md`](../00_FIRST_AI_POLICY_VERIFIED.md) (attribution).

**How to use this file**
- Everything inside a fenced block is the prompt. Everything outside it is for you, not the model.
- `<ANGLE BRACKETS>` are fill-ins. **If you leave one unfilled you will get invented content.**
- Every prompt assumes `CLAUDE.md` is at the repo root. If it is not, prompts 1–5 and 8–13 will
  produce 2026-API code. Run §0 step 3 of the main file first.
- The **"What you must check"** section under each prompt is not optional. It is the part that
  makes the prompt safe.

**Rank** below refers to the payoff ranking in `01_ai_for_programming.md` §3.

| # | Prompt | Rank | Risk |
|---|---|---|---|
| 1 | Subsystem scaffold from a written spec | 3 | Medium |
| 2 | WPILib 2027 / Systemcore migration audit (**report only**) | 2 | Medium |
| 3 | Simulation + unit test writer | **1** | Low |
| 4 | `*IOSim` physics implementation | **1** | Low |
| 5 | FRC bug-hunt code review | 5 | Low |
| 6 | Socratic tutor / explain-before-generate | — (learning) | Low |
| 7 | Post-match log → engineering report | 4 | Low |
| 8 | SysId characterisation → constants | 8 | **High** |
| 9 | Auto routine + auto-selection test scaffolding | 9 | Medium |
| 10 | API reality check (citation demand) | 7 | Medium |
| 11 | Onboarding doc from the repo | 10 | Low |
| 12 | Pre-actuation safety review (the G-gate prompt) | — (gate) | — |
| 13 | Vendor example → our IO architecture | 6 | **High** |

---

### 1. Subsystem scaffold from a written spec

**When:** a student has written the spec and wants the boilerplate. **Not before the spec exists.**
The spec is the engineering; this prompt only transcribes it.

**Payoff:** rank 3. ~12–20 h across a season **[S]**.

```
Read CLAUDE.md first, then scaffold a subsystem from the spec below.

SPEC (written by a student -- treat every value here as authoritative, and do not
invent any value that is not here):

  Mechanism name: <NAME>
  Shape:          <ROLLER (velocity, no end stop) | SERVO (position, has limits)>
  Purpose:        <one sentence: what it does on the robot>
  Actuators:      <motor(s), controller type, CAN ID(s), gear ratio, inverted?>
  Sensors:        <encoder type, absolute or relative, CAN ID, conversion factor>
  States:         <named states, e.g. IDLE / INTAKING / HOLDING / EJECTING>
  Transitions:    <which state goes to which, and on what condition>
  Limits:         <current limit A, soft min, soft max, units>
  On disable:     <what the mechanism must do>
  Public API:     <method names WITH UNITS, e.g. setHeightMeters(double), getAngleRad()>

RULES:
- Follow the architecture in CLAUDE.md sec 2. If this mechanism is a roller or a servo,
  COMPOSE OR EXTEND the existing base class in lib/subsystems/base/. Do not create a new
  IO interface unless the spec genuinely does not fit either shape -- and if it does not,
  say so and stop before writing anything.
- WPILib 2027 API only (CLAUDE.md sec 3). org.wpilib.*, setThrottle, Math.clamp,
  no robotInit, unified Gamepad, no removed classes.
- Every physical constant that is NOT in the spec above: write
  `TODO(human): measure` with a comment saying what to measure and in what units.
  Do not invent a plausible number.
- Units per CLAUDE.md sec 5. SI internally. Unit in every name or a WPILib Units type.
- Apply the safety rules in CLAUDE.md sec 7: current limit, soft limits both ends,
  setpoint clamp, deadband if there is an operator input, defined disable behaviour.

DELIVERABLE ORDER:
1. First, a plain-English plan: what files, what each does, and one sentence on why
   this shape. STOP THERE and wait for me to approve.
2. Only after I approve: the code.
3. After the code: a numbered list of everything I must verify before this runs on
   hardware, and every assumption you made that the spec did not cover.
```

**What you must check:** every `TODO(human)`; that it used the base class rather than a new IO
interface; that the units in the public API match the spec exactly; that the state machine has no
state you cannot leave.

---

### 2. WPILib 2027 / Systemcore migration audit (report only)

**When:** you have 2026-era code (yours, a vendor example, a public repo) and need it on 2027.

**Payoff:** rank 2 — this is the prompt that attacks the ~40 h of platform-change inflation named in
`02_TEAM_CAPACITY_MODEL.md` §3.2.

**This prompt deliberately produces a REPORT, not a diff.** Run it first. Only after you have read
the report do you ask for edits, file by file.

```
Read CLAUDE.md sec 3 (WPILib 2027 API rules) before doing anything.

Audit the following for WPILib 2027 / Systemcore compatibility:
<PATHS, or paste the file>

Produce a REPORT ONLY. Change no files. Output four tables:

TABLE A -- MECHANICAL RENAMES (safe, no judgement needed)
  file | line | old | new
  Cover: edu.wpi.first.* -> org.wpilib.*; set() -> setThrottle(); stopMotor() ->
  disable(); MathUtil.clamp -> Math.clamp; robotInit() -> Robot() constructor;
  XboxController/PS4Controller/PS5Controller/StadiaController -> Gamepad;
  Command.schedule() -> CommandScheduler.getInstance().schedule();
  Timer.getFPGATimestamp() -> Timer.getTimestamp(); mutable units -> immutable;
  pose.exp(twist) -> pose.plus(twist.exp()); isTest() -> Utility mode.

TABLE B -- REDESIGNS (compiles differently, behaves differently, needs a human decision)
  file | line | what | why it is not a rename | what the human must decide
  Cover: PIDCommand / ProfiledPIDCommand / TrapezoidProfileCommand removed;
  RamseteController -> LTV Unicycle; SwerveControllerCommand /
  MecanumControllerCommand removed; Rotation3d interpolation now slerp;
  geometry classes now final.

TABLE C -- SILENT BEHAVIOUR CHANGES (compiles clean, does the wrong thing) -- HIGHEST PRIORITY
  file | line | context (5 lines) | is this angle used as CONTINUOUS or WRAPPED? | risk
  Every call site of Rotation2d.getRadians() / .getDegrees() / .getRotations().
  For each, quote the surrounding code and say what the value feeds into.
  DO NOT propose a fix. A human decides each one.

TABLE D -- REMOVED HARDWARE (this is a MECHANICAL problem, not a software one)
  file | line | removed API | what physical device it drives | consequence
  Cover: Servo, Ultrasonic, Relay, Counter, SPI (ADIS16448/16470, ADXL345,
  ADXRS450), Analog Gyro / Output / Trigger, DMA, Interrupts,
  DigitalGlitchFilter, DigitalSource, Axis Camera, NetworkTables v3.
  Do NOT propose deleting the code. Say what hardware decision this forces.

Then: a one-paragraph summary saying which of the four tables carries the real risk,
and roughly how many human-hours each table represents.

If you are not certain whether a symbol changed in 2027, put it in a fifth
"UNCERTAIN -- verify against docs" table with the doc page to check. Do not guess.
```

**What you must check:** **read Table C line by line yourself.** That is the fifteen minutes that
prevents a turret unwinding into its wire harness. Table D goes to the mechanical lead, not the
programmers.

---

### 3. Simulation + unit test writer

**When:** always. This is rank 1 and it is the first thing to do in any repo.

**Payoff:** rank 1. ~18–30 h **[S]**, at the lowest risk in the whole list — a test cannot move a
motor.

```
Read CLAUDE.md sec 6 (testing) first.

Write JUnit 5 tests for: <CLASS OR COMMAND>

The behaviour being tested, and the EXPECTED VALUES, are given by me below. Use these
values. Do not read the implementation and assert what it currently does -- a test that
mirrors the implementation passes forever and protects nothing.

  Scenario 1: given <INPUT/STATE>, after <N> seconds, expect <VALUE> +/- <TOLERANCE>
  Scenario 2: <...>
  Scenario 3 (failure case): given <BAD INPUT>, expect <SAFE BEHAVIOUR>

RULES:
- HAL.initialize(500, 0) in a static @BeforeAll, before any WPILib or vendor object.
- Use the TestUtil.tick(int) helper (20 ms per iteration: CommandScheduler.run() then
  SimHooks.stepTiming(0.020)). If it does not exist in src/test, write it first.
- DELTA on every floating-point assertion. Never assertEquals on a raw double.
- Reset state in @BeforeEach.
- WPILib 2027 API only.
- Include the smoke test if src/test does not already have one:
  assertDoesNotThrow(RobotContainer::new).
- Do not modify anything in src/main. If a test cannot be written without changing
  production code, say what change is needed and why, and stop.

After the tests, tell me: which of my expected values you found suspicious and why,
and what behaviour is NOT covered by these tests.
```

**What you must check:** run `./gradlew test`. Then read each assertion and confirm the expected
value is *yours*, from the spec — not something the model derived from the implementation.

---

### 4. `*IOSim` physics implementation

**When:** you have an `*IO` interface and hardware implementation and want to develop before the
robot exists.

**Payoff:** rank 1, and the enabler for everything in `03_programming_stack.md` §7.

```
Read CLAUDE.md sec 2 (IO layer) and sec 5 (units).

Write the simulation implementation <NAME>IOSim for the interface <NAME>IO.

PHYSICAL PARAMETERS (measured by a human -- use exactly these, invent nothing):
  Motor:          <DCMotor type and count, e.g. DCMotor.getKrakenX60(2)>
  Gear ratio:     <X : 1, motor rotations per mechanism rotation/metre>
  Moment of inertia / carriage mass: <VALUE UNITS>   (elevator: kg; arm/flywheel: kg*m^2)
  Arm length / drum radius:          <VALUE m>       (if applicable)
  Travel limits:  <MIN> to <MAX> <UNITS>
  Starting state: <VALUE UNITS>
  Simulate gravity: <YES/NO>

RULES:
- Use the appropriate WPILib physics class: FlywheelSim / ElevatorSim /
  SingleJointedArmSim / DCMotorSim. Say which you chose and why.
- The sim must respect the SAME soft limits and current limit as the real IO, so that
  behaviour in sim predicts behaviour on hardware. If the real IO has a limit the sim
  cannot express, say so.
- Update at the same 20 ms period as the robot loop.
- Populate the SAME inputs fields as the real implementation, in the same units.
- WPILib 2027 API only.

If any parameter above is missing or looks physically implausible (e.g. an MOI that
would make the mechanism accelerate impossibly), say so and stop rather than
substituting a value.
```

**What you must check:** run it in `./gradlew simulateJava` and ask "does this move at a speed a
human would believe?" A sim that settles instantly or takes thirty seconds is telling you a
parameter is wrong.

---

### 5. FRC bug-hunt code review

**When:** every PR before merge, and once over the whole repo in the week before your event.

**Payoff:** rank 5, best risk-adjusted use in the document — it finds defects and cannot create them.

```
Read CLAUDE.md, then review this diff/code as an experienced FRC mentor would.
Change nothing. Report only.

<PASTE DIFF, or: review the diff between <BRANCH> and main>

Check for EVERY item below. For each finding give: file, line, the bug class, what
goes wrong physically on the robot, and a severity of HAZARD / MATCH-LOSING / ANNOYING.

  1. UNIT ERRORS -- degrees into a radians parameter; inches into a metres API;
     motor rotations vs mechanism rotations; gear ratio applied twice or zero times;
     feedforward in volts summed with feedback in duty cycle.
  2. INVERTED MOTORS/SENSORS -- follower not inverted; encoder sign opposite the
     motor; setInverted applied after the config was applied.
  3. UNCLAMPED SETPOINTS -- any path from an operator input, dashboard entry, vision
     measurement, or computed value to a motor setpoint with no Math.clamp between.
  4. MISSING DEADBANDS -- any joystick axis read without a deadband.
  5. BLOCKING CALLS IN periodic()/execute() -- Thread.sleep, while loops, .get() on a
     future, file or network I/O, unbounded printing.
  6. CAN FLOODING -- the same sensor getter called more than once per loop; hardware
     objects constructed outside subsystem construction; default status frame periods
     left unconsidered on a large device count.
  7. UNSAFE DEFAULTS -- subsystem with no default command that holds position; missing
     current limit; neutral mode not set explicitly; undefined behaviour in
     end(interrupted=true) or on disable.
  8. REPLAY DETERMINISM -- Timer.getFPGATimestamp(); Math.random(); HashMap/HashSet
     iteration; NetworkTables read as an input; threads in robot logic.
  9. WPILIB 2027 -- any 2026 API (see CLAUDE.md sec 3); any removed class; any
     Rotation2d wrapped-getter site used as a continuous angle.
 10. INTEGRAL WINDUP -- an I term with no anti-windup on a mechanism that can stall
     against a hard stop.

Order the findings by severity, HAZARD first. If you find nothing in a category, say
so explicitly -- I want to know the category was checked.

Then list, separately, anything you were UNSURE about and why. Do not pad the report
with style opinions; I asked about defects.
```

**What you must check:** triage every finding yourself. Expect false positives — they cost a minute
each. A single true HAZARD finding pays for the whole practice.

---

### 6. Socratic tutor / explain-before-generate

**When:** a student is learning, or is stuck, and it is **not** competition day. This prompt
deliberately withholds the answer.

**Payoff:** this is the prompt that produces the third programmer named in
`02_TEAM_CAPACITY_MODEL.md` §3.2 — worth ~85 veq-h, more than any code-generation use in this file.

```
You are tutoring a high-school student in their <FIRST/SECOND> year of Java and FRC.

TOPIC / PROBLEM: <what they are stuck on>
WHAT THEY HAVE TRIED: <their own words>

RULES FOR THIS CONVERSATION:
- Do NOT give the answer. Do NOT write the code.
- Start by asking what they EXPECTED to happen and what they OBSERVED. The gap between
  those two is the lesson.
- Then ask questions that narrow the problem. One question at a time.
- Give hints at increasing specificity only after they answer. A hint names where to
  look, not what to write.
- If they ask directly for the answer, ask once whether they want to keep working it,
  then give it -- with an explanation of the reasoning, not just the fix.
- After anything is resolved, ask them ONE question that checks whether they can now
  predict what would happen if a related thing changed.
- Never make them feel stupid. They are learning Java and control theory at the same
  time, on a deadline.
- If this is competition day and they say so, drop all of the above and just help.
```

**Companion — "explain before generate", for when you do want code:**

```
Before you write any code for <TASK>:
1. Describe your plan in plain English: what files, what each one does, and what the
   control flow is.
2. Name one alternative approach and say in one sentence why you did not choose it.
3. Ask me the single question whose answer would most change your plan.
Then STOP and wait for me to approve. Write nothing until I do.
```

**What you must check:** that the student can still answer §6.5 assessment 1 in the main file — walk
through what happens when the driver presses a button, laptop closed.

---

### 7. Post-match log → engineering report

**When:** between matches at an event, and after every practice session.

**Payoff:** rank 4. Feed it the **summary JSON** from `tools/log-report.py`, **never the raw log** —
see `01_ai_for_programming.md` §7.1 for why.

```
You are an FRC software mentor writing a between-matches engineering report.

INPUT: the JSON below is a statistical summary produced by tools/log-report.py from a
single match's WPILOG. It is the ONLY data you have. Every number in your report must
come from it. If something is not in the JSON, you do not know it.

MATCH CONTEXT: <event, match number, alliance, anything the drive team reported>

<PASTE reports/match-NN.summary.json>

Produce a Markdown report with exactly these sections:

  1. TIMELINE -- match phases with timestamps in seconds from enable.
  2. ANOMALIES -- every loop overrun (duration, when), every brownout (voltage floor,
     current draw before it), every device that dropped off CAN, every command that
     was interrupted. Each with a timestamp.
  3. MECHANISM PERFORMANCE -- for each mechanism in the data: setpoint vs measured,
     max error, settle time, whether it ever failed to reach a commanded state.
  4. POSE / VISION -- pose-estimator discontinuities, vision measurements accepted vs
     rejected, and any period where odometry and vision disagreed.
  5. TOP 5 ACTIONS BEFORE THE NEXT MATCH -- ranked, each with the timestamp and signal
     name that justifies it, and an estimate of how long it takes to do.

HARD RULES:
- EVERY claim cites a timestamp and a signal name. A claim I cannot audit against
  AdvantageScope is worthless.
- Never invent a number that is not in the JSON.
- Never assert a MECHANICAL cause (slop, a loose crimp, a broken belt) -- you cannot
  see mechanical things. You may say "consistent with" and name what to inspect.
- Never recommend a gain change without saying which signal justifies it.
- You do not know the 2027 BIOCORE game rules. Do not comment on scoring, strategy, or
  whether the robot "should have" done something.
- If the data is insufficient to answer a section, write "INSUFFICIENT DATA" and say
  which signal would need to be logged next time. That is a useful finding.
```

**What you must check:** open AdvantageScope and verify the top-ranked finding yourself. The report
is a search-space reducer, not a conclusion. Budget five minutes.

---

### 8. SysId characterisation → constants

**When:** you have just run a `SysIdRoutine` and have the analysed gains.

**Payoff:** rank 8 — low hours, **high consequence**. A kV off by 10× drives a mechanism into a hard
stop at full voltage.

```
Read CLAUDE.md sec 5 (units) and sec 7 (safety).

I ran SysId on <MECHANISM> and the analysis tool produced:

  kS = <VALUE> V
  kV = <VALUE> V/(<UNIT>/s)
  kA = <VALUE> V/(<UNIT>/s^2)
  kG = <VALUE> V              (elevator/arm only; omit otherwise)
  Mechanism type: <simple motor | elevator | arm>
  Units the analysis was run in: <rotations | radians | metres>
  Date run: <YYYY-MM-DD>   Log file: <path>

Tasks:
1. Write the Constants block. Every constant gets a unit in its name AND a comment
   naming the date, the log file, and the units the analysis used.
2. Write the feedforward construction (SimpleMotorFeedforward / ElevatorFeedforward /
   ArmFeedforward as appropriate), WPILib 2027 API.
3. SANITY-CHECK the numbers against physics and tell me if anything looks wrong:
   - Does kV imply a free speed consistent with <MOTOR> through <GEAR RATIO>?
   - Is kS plausible for this mechanism's friction?
   - Is kG plausible for a <MASS> kg load?
   Show your arithmetic. If a number is off by a factor of ~2pi, ~60, or the gear
   ratio, say so loudly -- those are unit-conversion mistakes, not measurements.
4. State what the FIRST hardware run must look like: what output limit, what to watch,
   what would indicate the gains are wrong.

Do NOT change any existing gains, limits, or clamps. Do not touch PID gains at all.
```

**What you must check:** the arithmetic in step 3 yourself. Then sim. Then the §5 G-gate. Then first
motion at reduced output with a hand on disable.

---

### 9. Auto routine + auto-selection test scaffolding

**When:** building autos. Note: build the *paths* in the PathPlanner GUI — a student can do that
without Java, which is the point. Use this prompt for the Java side only.

**Payoff:** rank 9. The test is worth more than the routine.

```
Read CLAUDE.md.

I have built these paths in the PathPlanner GUI: <LIST BY EXACT FILE NAME>
My subsystems expose these commands: <LIST WITH SIGNATURES AND UNITS>

Tasks (Java side only -- do not invent waypoints, poses, or field coordinates; you do
not know where the field elements are):
1. Register the named commands so the GUI paths can trigger them via event markers.
2. Build the SendableChooser wiring: one chooser for auto mode, one for start position.
3. Log the selected auto name, the commanded pose, and each event marker firing.
4. Write JUnit tests (CLAUDE.md sec 6) for the SELECTION LOGIC:
   - every chooser combination produces a non-null command
   - no combination throws
   - an invalid/missing selection falls back to a safe do-nothing auto
   - the fallback auto does not command any motion
5. Tell me what happens if the robot starts in the wrong position, and whether the
   current code detects that.

WPILib 2027 API. No SwerveControllerCommand (removed). If a path file name I gave you
does not exist in the repo, say so -- do not create it.
```

**What you must check:** run the tests; then run the auto in simulation; then on the field at reduced
speed with the field clear.

---

### 10. API reality check (citation demand)

**When:** any time an unfamiliar vendor or WPILib symbol appears — in generated code, in a Chief
Delphi post, or in your own memory.

**Payoff:** this is the prompt that defends against `01_ai_for_programming.md` §4.1, the most common
AI failure in FRC. **All 2027 vendor libraries are alpha and are not in any model's training data.**

```
I need to know whether these APIs actually exist in the versions this repo pins.

Repo's pinned versions (from vendordeps/): <PASTE>

Symbols to verify:
  <FULLY QUALIFIED SYMBOL 1>
  <FULLY QUALIFIED SYMBOL 2>

For EACH symbol, answer in this exact form:

  SYMBOL:      <name>
  STATUS:      EXISTS / RENAMED / REMOVED / I-AM-NOT-CERTAIN
  EVIDENCE:    <the documentation or Javadoc URL where this can be checked>
  SIGNATURE:   <full signature, if you are confident>
  2026 vs 2027: <what changed, if anything>
  CONFIDENCE:  HIGH / MEDIUM / LOW, and one sentence on why

RULES:
- "I-AM-NOT-CERTAIN" is a correct and useful answer. Use it freely. These are alpha
  libraries and your training data predates them.
- If you cannot produce a URL a human can open, your confidence is LOW by definition.
  Say so.
- Do not write example code using a symbol you rated below HIGH.
```

**What you must check:** **open every URL.** If there is no URL, the answer was a guess. This is a
two-minute habit that removes an entire failure class.

---

### 11. Onboarding doc from the repo

**When:** October (for the fall training programme) and again in February (as judging evidence).

**Payoff:** rank 10 in hours, but it produces an award-submission artifact — see
[`../../awards/01_AWARD_WINNING_PATTERNS.md`](../../awards/01_AWARD_WINNING_PATTERNS.md).

```
Read the repo, then write docs/how-our-robot-code-works.md for a student who joins the
team in September and has written some Java at school but has never seen FRC code.

Structure:
1. The 60-second version -- what happens between the driver pressing a button and a
   motor turning. Name the actual classes in THIS repo.
2. The file map -- what lives where and why lib/ is separate from robot/.
3. One subsystem, end to end -- pick the simplest real one and walk through it.
4. How to run it without a robot -- the exact commands.
5. The five things a new programmer will get wrong, and how to notice.
6. Glossary -- every FRC/WPILib term used above, one line each.

RULES:
- Describe what the code ACTUALLY does. If something is confusing or inconsistent, say
  so plainly in a "known rough edges" section -- do not describe the code as tidier
  than it is.
- No code blocks longer than 15 lines.
- Every claim must be checkable against a real file path in this repo.
- Do not describe the 2027 game. It is not public.
```

**What you must check:** hand it to a student who was not in the room. If they can follow it, it is
good. If they ask three questions, fix those three answers into the doc.

---

### 12. Pre-actuation safety review (the G-gate prompt)

**When:** before the first hardware run of any new or substantially changed mechanism code. This is
the prompt form of the five-gate checklist in `01_ai_for_programming.md` §5.

**This prompt does not replace the human gate. It prepares the human for it.**

```
Read CLAUDE.md sec 7 and sec 9.

This code is about to move a mechanism on a ~135 lb robot for the first time:
<PASTE the subsystem + the command that will run>

Mechanism: <NAME>. Actuator: <MOTOR through GEAR RATIO>. Travel: <MIN> to <MAX> <UNITS>.

Walk the five gates and, for each, tell me EXACTLY what to point at in the code, or
that it is missing:

  G2 UNITS & SIGNS
    - list every physical quantity crossing a boundary and its unit
    - state which direction of encoder increase the code assumes is "positive"
    - state what physically happens if that assumption is backwards
  G3 LIMITS
    - where is the current limit set? (quote the line)
    - where are the soft limits, both ends? (quote)
    - where is the setpoint clamped between input and output? (quote)
    - what happens on disable, and on end(interrupted=true)? (quote)
    Any of these missing is a BLOCKER. Say BLOCKER.
  G4 SIMULATION
    - what test or sim run covers this behaviour? if none, say so
  G5 FIRST MOTION
    - propose a bounded first run: output limit, expected motion, what would indicate
      a sign error within the first 0.5 seconds, and where the person on the disable
      button should be looking

Finally: the ONE thing most likely to go wrong on the first run, and how we would know
within half a second.

Do not modify any code. Do not tell me it is safe -- a human decides that.
```

**What you must check:** G1 is not in this prompt on purpose. **G1 is a human asking a student to
explain the code with the laptop closed**, and no model can run that gate for you.

---

### 13. Vendor example → our IO architecture

**When:** adapting a CTRE / REV / PathPlanner / PhotonVision example into this repo.

**Payoff:** rank 6, **high risk** — this is where hallucinated vendor APIs live.

```
Read CLAUDE.md sec 2 (architecture) and sec 3 (2027 API).

Below is a vendor example. Restructure it into this repo's architecture.

<PASTE THE ENTIRE VENDOR EXAMPLE FILE -- do not summarise it, paste it>

Vendor library and EXACT version from vendordeps/: <NAME> <VERSION>

RULES -- the first one is absolute:
- YOU MAY ONLY USE VENDOR SYMBOLS THAT APPEAR IN THE PASTED EXAMPLE ABOVE. If the
  restructuring needs a vendor call that is not in the example, STOP and tell me which
  symbol you need and what documentation page would confirm it. Do not write it from
  memory. This library version is in alpha and is not in your training data.
- All vendor calls go in the *IO implementation. Zero vendor imports above that layer.
- Control logic goes in the subsystem, expressed in mechanism units, not vendor units.
- Apply CLAUDE.md sec 3 renames to any WPILib (non-vendor) API in the example.
- Keep the example's configuration values, but flag any that are clearly placeholders
  (CAN ID 0, gear ratio 1.0, a current limit of 0 or absent) as
  `TODO(human): this is the vendor's placeholder, not our robot`.
- Preserve the vendor's comments where they explain WHY. Delete tutorial narration.

Deliver: the restructured files, then a table of every vendor symbol you used with
where in the pasted example it appeared, then a list of everything you were unsure of.
```

**What you must check:** the symbol table — every row must trace to a line in what you pasted.
Then compile immediately. A hallucinated symbol is a compile error, which is the cheapest bug there
is; the dangerous case is a symbol that exists but means something different, and only the docs
catch that.

---

## Files written by this pass

| Path | What it is |
|---|---|
| `reference/ai-integration/templates/programming-prompts.md` | This file |

## Known limitations

1. **Prompts are not a substitute for the gate.** Every prompt here that produces code is upstream
   of the five-gate checklist in `01_ai_for_programming.md` §5. Nothing in this file makes generated
   code safe; the human review does.
2. **Prompt 7 depends on `tools/log-report.py`**, which round-trips a synthetic spec-conformant log
   but has **never been run against a real WPILOG file**. Validate it in October before you rely on
   the pipeline at an event.
3. **These prompts assume `CLAUDE.md` is at the repo root and is actually being read.** If it is
   not, prompts 1–5 and 8–13 will produce 2026-API code that looks correct. Verify with §0 step 3 of
   the main file before trusting any of them.
4. **Prompt wording is tuned for the 2026 generation of these tools** and for Claude Code
   specifically. Other assistants may need the rules restated more forcefully, or may ignore the
   "stop and wait" instruction entirely — check that behaviour before relying on it.
5. **No prompt here touches the BIOCORE game**, deliberately. The game is not public as of
   2026-08-22, and any model output about its rules or scoring is invented.
