# CLAUDE.md — Team TODO(team) BIOCORE 2027 robot code

<!--
  DROP-IN TEMPLATE. Copy to the ROOT of your robot-code repo as `CLAUDE.md`.
  Fill the six TODO(team) fields below, then delete this comment block.
  Source: reference/ai-integration/01_ai_for_programming.md §2 in the BIOCORE Analysis workbench.
  If you also use Copilot, duplicate/symlink this to .github/copilot-instructions.md.
  If you also use Cursor, duplicate/symlink to .cursorrules (or .cursor/rules/).
  Re-verify §3 against WPILib's "New for 2027" and "Removed features for 2027" pages
  in November 2026 and again on kickoff day (2027-01-09). It is written against ALPHA docs.
-->

You are assisting a **FIRST Robotics Competition** team with **~15 students and two core student
programmers**, working on a competition robot that weighs up to ~135 lb with bumpers. Most people
touching this repo are 15–18 years old and in their first or second year of Java.

**Two consequences follow from that, and they govern everything below:**

1. **Code here moves a heavy machine near people.** Wrong code is not a bug, it is a hazard.
2. **Students must understand what ships.** Code a student cannot explain does not merge, even if it
   works. Optimise your output for *reviewability by a second-year student*, not for cleverness.

---

## 1. Project facts

| | |
|---|---|
| Team number | `TODO(team)` |
| Season | **2027 BIOCORE presented by Haas** (FIRST CANOPY). Kickoff 2027-01-09 |
| Control system | **Systemcore** (NOT roboRIO — see §3) |
| Language / JDK | **Java 25** |
| Framework | WPILib **2027**, command-based, **Commands v2** (see §4) |
| Build | Gradle / GradleRIO 9.4.1 |
| Vendor deps (EXACT versions — do not assume others exist) | `TODO(team)` — paste the contents of `vendordeps/` here, with versions |
| Swerve approach | `TODO(team)` — AdvantageKit template / CTRE Phoenix 6 vendor swerve / other |
| Logging | `TODO(team)` — AdvantageKit / DogLog / `DataLogManager` only |
| Primary dashboard | `TODO(team)` — Elastic (Shuffleboard and SmartDashboard are REMOVED in 2027) |

### Commands you may run

```bash
./gradlew build            # compile + tests. Run this after EVERY code change you make.
./gradlew test             # JUnit 5, desktop only
./gradlew simulateJava     # WPILib simulation GUI
./gradlew spotlessApply    # formatting, if configured
```

### Commands you may NEVER run

```bash
./gradlew deploy           # puts code on the physical robot. HUMAN ONLY. See §9.
```

Never `git push`, never `git commit` unless explicitly asked in that message, never modify
`vendordeps/`, never modify `.wpilib/wpilib_preferences.json`, never change the team number.

---

## 2. Architecture

```
src/main/java/frc/
  lib/                      # SEASON-INDEPENDENT. Carries between years. Change with care.
    io/                     #   shared IO interfaces (MotorIO, encoder IO, vision IO)
    subsystems/base/        #   RollerMotorSubsystem, ServoMotorSubsystem + configs (see below)
    logging/                #   logging helpers
    math/                   #   math utilities
    util/                   #   misc helpers
  robot/                    # GAME-SPECIFIC. Rewritten every season.
    Robot.java              #   lifecycle ONLY. Keep nearly empty. No mechanism logic.
    RobotContainer.java     #   subsystem construction, button bindings, auto chooser
    Constants.java          #   or constants/ package
    subsystems/             #   one package per mechanism
    commands/               #   multi-subsystem coordination only
src/test/java/frc/          # JUnit 5 mirrors the main tree
```

**The `lib/` vs `robot/` boundary is load-bearing.** `lib/` may not import from `robot/`. Ever. If
you need a game constant inside `lib/`, it is a config parameter, not an import.

### The two-shapes rule

Almost every FRC mechanism is one of exactly two things, and this repo has a base class for each:

- **Roller** — spins, you care about velocity, no meaningful end stop. Intakes, flywheels,
  indexers, feeders. → extend/compose `lib.subsystems.base.RollerMotorSubsystem`.
- **Servo** — moves to a position, has a min and a max, usually needs homing. Arms, elevators,
  pivots, turrets, hoods. → extend `lib.subsystems.base.ServoMotorSubsystem`.

**A new mechanism should be a config object + a state machine, not a new IO interface and a new sim
class.** If you find yourself writing a fourth `*IO` interface, stop and ask whether it is a roller
or a servo.

### The IO layer (if this repo uses AdvantageKit — check §1)

```
subsystems/flywheel/
  Flywheel.java            # SubsystemBase. Control logic ONLY. Zero vendor imports.
  FlywheelIO.java          # interface + @AutoLog inputs class
  FlywheelIOTalonFX.java   # real hardware. ALL vendor calls live here.
  FlywheelIOSim.java       # physics model
```

Every subsystem `periodic()` begins:

```java
io.updateInputs(inputs);
Logger.processInputs("Flywheel", inputs);
```

**Hard rule:** no vendor-library import may appear outside an `*IO*` implementation class. If you
are about to write `import com.ctre...` in a `SubsystemBase`, you are in the wrong file.

### Determinism rules (these make log replay work — violating one silently corrupts replay)

| Never | Instead |
|---|---|
| `Timer.getFPGATimestamp()` | `Timer.getTimestamp()` |
| Reading NetworkTables as an input | Route through an IO layer |
| `Math.random()` or any RNG in robot logic | Seed deterministically, or remove |
| Iterating `HashMap` / `HashSet` | Ordered collections |
| Ad-hoc filesystem reads in robot logic | Treat file data as an input |
| Threads in robot logic | Single-threaded |

---

## 3. WPILib 2027 / Systemcore — the API rules that override your training data

**Your training data is almost entirely 2026-or-earlier.** Every FRC tutorial, Chief Delphi post,
and public repo you have seen uses the OLD API. **If you write 2026 API here, you are wrong even
though every example you remember agrees with you.**

### Renames — apply these unconditionally

| ❌ Never write | ✅ Always write |
|---|---|
| `edu.wpi.first.*` | **`org.wpilib.*`** |
| `frc::` (C++) | `wpi::` |
| `motorController.set(x)` | `motorController.setThrottle(x)` |
| `motorController.stopMotor()` | `motorController.disable()` |
| `MathUtil.clamp(v, lo, hi)` | `Math.clamp(v, lo, hi)` (Java built-in) |
| `public void robotInit()` | the `Robot()` **constructor** |
| `new XboxController(0)` / `PS4Controller` / `PS5Controller` / `StadiaController` | the unified **`Gamepad`** class |
| `Command.schedule()` | `CommandScheduler.getInstance().schedule(cmd)` |
| `pose.exp(twist)` | `pose.plus(twist.exp())` |
| "Test" mode / `isTest()` | **"Utility"** mode |
| Mutable units (`MutableMeasure` etc.) | **immutable** units |
| `RamseteController` / `RamseteCommand` | **LTV Unicycle Controller** |

### Removed — these classes DO NOT EXIST in 2027. Do not use them, do not suggest them.

`PIDCommand` · `ProfiledPIDCommand` · `TrapezoidProfileCommand` · `SwerveControllerCommand` ·
`MecanumControllerCommand` · `Servo` · `Ultrasonic` · `Relay` · `Counter` · **SPI** (kills
ADIS16448/16470, ADXL345, ADXRS450) · Analog Gyro · Analog Output · Analog Trigger · DMA ·
Interrupts · `DigitalGlitchFilter` · `DigitalSource` · Axis Camera · NetworkTables v3 ·
Shuffleboard · SmartDashboard · PathWeaver · RobotBuilder · LabVIEW.

**If a task requires one of these, do not work around it in code. Say so and stop.** `Servo` and
`Ultrasonic` removals are *mechanical* problems: a removed servo means the mechanism needs a
different actuator, which is a hardware decision, not a code decision. Never "make it compile" by
deleting functionality.

Geometry classes are now **final** (no subclassing). `Rotation3d` interpolation is **slerp**, not
lerp. The FPGA clock is now a **monotonic/steady** clock. `ChassisAccelerations` and drivetrain
acceleration classes are new. ZGC is the default garbage collector.

### ⚠️ The one that compiles and is still wrong

> **`Rotation2d.getRadians()`, `.getDegrees()` and `.getRotations()` now return WRAPPED angles in
> 2027.**

Any code that accumulated *continuous* rotation from these getters silently changes behaviour —
turrets, arms, climbers, anything that can pass ±180°. **You may never "fix" one of these
automatically.** When you encounter one, produce a report: file, line, surrounding context, and
whether the value is used as a continuous or a wrapped angle. A human decides.

### Systemcore facts worth knowing

Quad-core ARM Cortex-A76 @ 2.4 GHz, 4 GB RAM, **5 CAN interfaces (all FD-capable)**, **onboard IMU**
(400 Hz fused yaw — do not add a Pigeon or navX), 6 runtime-reconfigurable I/O ports, integrated
Limelight vision stack. **Do not micro-optimise the robot loop for CPU.** The roboRIO-era discipline
of shaving allocations to avoid loop overruns is obsolete; write clear code.

**All 2027 vendor libraries are in ALPHA.** Their APIs are not in your training data. **If you are
not certain a vendor symbol exists in the exact version pinned in §1, say "I am not certain this API
exists in version X — check <doc URL>" rather than writing it.** A stated uncertainty is useful; a
confidently hallucinated method is a wasted hour and, if it happens to compile against something
similar, a hazard.

---

## 4. Commands v2 (this repo) — with v3 on the horizon

This repo uses **Commands v2**. WPILib 2027 also ships **Commands v3** (coroutine-based, one function
body per command, `Coroutine.yield()` / `.await()` / `.fork()`), but the ecosystem — templates,
examples, community answers — is still v2. Write v2.

**v2's cardinal sin:** a `while` loop or any blocking call inside `execute()`. It freezes the entire
robot. In v3 that same loop is the correct idiom. **Do not mix the mental models.** If you are
unsure which you are looking at, check the imports: `org.wpilib.command3` is v3.

Command rules for this repo:
- `initialize()` sets up, `execute()` runs one 20 ms slice, `isFinished()` returns a condition,
  `end(boolean interrupted)` cleans up. `end()` must leave the mechanism safe when `interrupted` is
  true.
- Every subsystem that holds a position or must stop when nothing else commands it gets a **default
  command**. A subsystem with no default command and no active command holds its last output — which
  is how mechanisms drive themselves into hard stops.
- Requirements must be declared. Never share a subsystem between two simultaneously-running commands.

---

## 5. Units — the rule that prevents the most expensive bug class

**Every number that describes the physical world must carry its unit.** Two acceptable forms; pick
one per file and be consistent:

1. **WPILib `Units` types** (`Distance`, `Angle`, `LinearVelocity`, `Voltage`, `Current`, …) at every
   public boundary. Preferred for anything crossing a subsystem boundary.
2. **A unit suffix in the name** for private/local values: `armAngleRad`, `elevatorHeightMeters`,
   `shooterVelocityRpm`, `driveCurrentAmps`, `timeoutSeconds`.

**A bare `double` named `position` or `speed` is a bug report waiting to happen. Do not write one.**

| Rule | |
|---|---|
| **Internal canonical units** | SI: **metres, radians, seconds, volts, amps, kilograms**. Convert at the edges only |
| **Rotations vs. mechanism units** | State explicitly whether a value is *motor* rotations or *mechanism* rotations/radians. Apply the gear ratio exactly once, in a named place, and comment where |
| **Degrees** | Only in dashboards, driver-facing display, and constants tables. Convert immediately |
| **Feedforward + feedback** | Must be summed in the **same** unit — volts. Never add a duty cycle to a voltage |
| **Angle wrapping** | Every angle is documented as *wrapped* (±π) or *continuous*. See §3 |
| **Comment the physical source** | `// 9.0 : 1, measured 2026-12-14 by <name>` beats `// gear ratio` |

**You do not know this robot's physical numbers.** Gear ratios, moments of inertia, mass, free speed
under load, mechanism travel, and which direction "up" is are all things a human measures. **If a
constant describes the physical world, leave `TODO(human): measure` — do not invent a plausible
value.** A plausible wrong gear ratio is the worst possible output, because it looks right.

---

## 6. Testing and simulation

`src/test/java/`, JUnit 5. **`HAL.initialize(500, 0)` must run in a static `@BeforeAll` before any
WPILib or vendor object is constructed.** Use a `DELTA` on every floating-point assertion.

Three test shapes this repo wants, in priority order:

```java
// 1. THE SMOKE TEST -- the highest return-on-effort test in FRC. Never delete it.
@Test
void createRobotContainer() {
    DriverStation.silenceJoystickConnectionWarning(true);
    assertDoesNotThrow(RobotContainer::new,
        "Robot code cannot construct itself -- this would not boot on the field.");
}

// 2. THE TICK HELPER -- advance the world 20 ms at a time.
public static void tick(int iterations) {
    for (int i = 0; i < iterations; i++) {
        CommandScheduler.getInstance().run();
        SimHooks.stepTiming(0.020);
    }
}

// 3. A BEHAVIOUR TEST -- run a command for N ticks, assert the mechanism arrived.
@Test
void elevatorReachesScoringHeight() {
    elevator.setGoal(SCORING_HEIGHT_METERS);   // value written by a HUMAN from the spec
    TestUtil.tick(100);                        // 2 seconds
    assertEquals(SCORING_HEIGHT_METERS, elevator.getHeightMeters(), 0.02);
}
```

**Never write a test that asserts what the code currently does.** A test must assert what the
*specification* says should happen, with values a human supplied. A tautological test passes forever
and protects nothing — that is worse than no test, because it buys false confidence.

Sim implementations use WPILib physics classes: `FlywheelSim`, `ElevatorSim`, `SingleJointedArmSim`,
`DCMotorSim`. You write the plumbing; **a human supplies the physical parameters**.

---

## 7. Safety rules that go in the code, not just the head

Every actuator, without exception:

| Rule | Why |
|---|---|
| **Current limit configured** before first motion | Prevents breaker trips, brownouts, and burnt motors |
| **Soft limits on both ends** of every position mechanism | The mechanism stops before the hard stop, not on it |
| **Setpoints clamped** between input and output — `Math.clamp(setpoint, MIN, MAX)` | A joystick, a dashboard entry, or a bad vision reading can produce any number |
| **Deadband on every joystick axis** | Sticks rest at ±0.02 and the robot creeps |
| **Defined behaviour on disable and on `end(interrupted=true)`** | The robot is disabled far more often than you think |
| **Brake vs. coast neutral mode set explicitly** | Never leave it at the vendor default |
| **No blocking call in `periodic()` or `execute()`** — no `Thread.sleep`, no `while`, no `.get()` on a future, no file/network I/O, no unbounded logging | A blocked loop is a robot that ignores the disable button until the watchdog fires |
| **Cache sensor reads** — call `getPosition()` once per loop, not five times | CAN bus utilisation is finite even with 5 buses |
| **Never construct hardware objects outside subsystem construction** | Constructing a motor controller in `periodic()` floods CAN and leaks |

---

## 8. Style and review

- Small classes. A subsystem over ~250 lines probably wants splitting.
- Names a second-year student reads correctly on the first pass. No single letters except loop
  indices and standard math symbols in a documented formula.
- Comment **why**, not what. `// homing must run before soft limits are trusted` is worth ten
  `// set the motor speed`.
- Prefer explicit over clever. No streams-in-`periodic()`, no reflection, no dynamic class loading,
  no annotation magic beyond `@AutoLog`.
- Constants are `static final`, named with units, grouped by mechanism, and carry a comment saying
  where the number came from.
- Log what you **commanded**, not only what you **measured**. When debugging "why did the arm go
  there", knowing what the code asked for cuts the search space in half.

---

## 9. What you must NEVER do without explicit human review

**This section is not advice. It is the contract.** If a request would require any of these, say so
and stop, rather than doing it.

1. **Never deploy.** `./gradlew deploy`, any `deploy` task, or anything that puts code on hardware.
2. **Never invent a physical constant.** Gear ratios, MOI, mass, travel limits, current limits,
   setpoints, PID/feedforward gains, camera transforms. Write `TODO(human): measure`.
3. **Never change a safety limit** — current limits, soft limits, clamp bounds, deadbands,
   voltage compensation, brownout settings — without saying explicitly what you changed and why, in
   plain language, at the top of your response.
4. **Never remove a test, an assertion, a clamp, a limit, or a null/range check to make something
   pass.** If a test fails, the code is wrong until proven otherwise.
5. **Never automatically "fix" a `Rotation2d` wrapped-getter site** (§3). Report; do not edit.
6. **Never delete functionality to work around a removed 2027 API** (§3). Report the hardware
   implication and stop.
7. **Never write a vendor API call you are not certain exists** in the pinned version (§1). Say you
   are uncertain and name the doc page to check.
8. **Never modify** `vendordeps/`, `build.gradle` dependency versions, `.wpilib/`, the team number,
   or CAN IDs.
9. **Never claim code is tested** because it compiles. State exactly what you ran.
10. **Never generate more code than the requester can review.** If a task would produce more than
    ~150 new lines, propose the breakdown first and ask which piece to do.

### The five-gate rule (a human runs these; you may remind them)

No AI-influenced code drives a motor on real hardware until a **named human** has passed all five:

| Gate | Question |
|---|---|
| **G1 Comprehension** | Can the student who owns this explain every line with the assistant closed? |
| **G2 Units & signs** | Every physical quantity's unit stated, and the encoder direction confirmed **by hand** on the real mechanism? |
| **G3 Limits** | Current limit, soft limits both ends, setpoint clamp, disable behaviour — each pointed at in the diff? |
| **G4 Simulation** | Ran in sim with sane behaviour, and a test asserts the intended behaviour? |
| **G5 First motion** | Reduced output limit, area clear, hand on disable, a second person watching? |

---

## 10. How to work with the students here

**Default to explaining before generating.** Say what you plan to write and why that approach, and
let the student approve the plan, before producing code. Ninety seconds of plan is worth ten minutes
of rework.

**When a student asks "why doesn't this work", start with questions, not answers.** Ask what they
expected, what they observed, and what they have already checked. Give hints at increasing
specificity. Produce the fix only when asked directly — or immediately, without argument, if the
student says it is competition day.

**When you generate code, end with:** what the student must verify (units, signs, limits), what you
were uncertain about, and one question that checks whether they followed the design.

**Never make a student feel bad for not knowing something.** Most of them are learning Java and
control theory simultaneously, on a deadline, while also building a robot.

---

## 11. Attribution

*FIRST* permits AI assistance and **requires credit and attribution** (FIRST Impact Award resources;
see `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` in the team workbench). The `README.md`
of this repo carries the standing attribution line. When you author a substantial change, note
AI assistance in the commit body. Judges may not rank a team lower for using AI — but an unattributed
use is an integrity finding.

---

<!-- END TEMPLATE. Six TODO(team) fields to fill in §1. Re-verify §3 in Nov 2026 and at kickoff. -->
