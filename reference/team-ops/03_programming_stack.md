# Elite FRC Software Practice — Architecture a Small Team Can Actually Copy

**Scope:** what top teams' software looked like in the 2026 season (REBUILT), and what changes for **BIOCORE presented by Haas** (2027, FIRST CANOPY, kickoff **Jan 9 2027**).
**Written:** 2026-08-21 (off-season). **Audience:** experienced mentor, small/underfunded team.
**Research basis:** WPILib docs (stable=2026 and 2027 branches), AdvantageKit/AdvantageScope docs, vendor docs, GitHub API metadata, and direct inspection of team repositories cloned and read line-by-line.

**Verification standard used here:** every GitHub repo in this document was queried through the GitHub API on 2026-08-21 and returned live metadata. Every documentation URL was fetched and returned HTTP 200. Code excerpts are pasted from shallow clones, not reconstructed from memory. Prices are quoted from vendor pages on 2026-08-21. Anything I could not verify is tagged **[UNVERIFIED]**.

---

## 0. Read this first: 2027 is a control-system reset, and that is your single biggest advantage

The most important fact in this entire document is not about AdvantageKit or swerve libraries. It is this:

> **The roboRIO is gone in 2027.** It is replaced by **Systemcore**, and WPILib 2027 is a breaking rewrite: Java packages move from `edu.wpi.first` to `org.wpilib`, C++ namespaces from `frc::` to `wpi::`, Java 25 and C++23 are required, NetworkTables v3 is removed, and Shuffleboard / SmartDashboard / PathWeaver / RobotBuilder / LabVIEW are all removed.
> — [New for 2027, WPILib docs](https://docs.wpilib.org/en/latest/docs/yearly-overview/yearly-changelog.html), [Removed features for 2027](https://docs.wpilib.org/en/2027/docs/yearly-overview/removed-features.html)

WPILib itself calls this "the biggest control system update since the introduction of the cRIO."

**Why this is good news for you.** Every powerhouse team's accumulated code library — the 8-year-old `frc.robot.util` package, the hand-tuned roboRIO performance hacks, the institutional muscle memory — is partially invalidated on January 9, 2027. Teams with 30,000 lines of legacy Java have a migration project. You have a blank page. In 2027 the gap between a well-prepared small team and a powerhouse is the smallest it has been in a decade, **but only if you spend this off-season learning the 2027 stack instead of the 2026 stack.**

The counter-risk is equally real: **it is an alpha ecosystem right now** and some libraries you want will not be ready.

### Vendor library readiness, August 2026

From the compatibility table in [wpilibsuite/SystemcoreTesting](https://github.com/wpilibsuite/SystemcoreTesting) (175★, pushed 2026-08-19), plus release data I pulled directly from each project's GitHub releases API:

| Library | Latest 2027-compatible release | Notes |
|---|---|---|
| CTRE Phoenix 6 | v26.50.0-alpha-1 | tracks WPILib alpha-5/6 |
| REVLib | v2027.0.0-alpha-2 | tracks alpha-5/6 |
| ReduxLib | v2027.0.0-alpha-6 | tracks alpha-5/6 |
| PathPlannerLib | v2027.0.0-alpha-3 | tracks alpha-5/6 |
| **ChoreoLib** | **none current** | had a `2027.0.0-alpha-1` against WPILib alpha-2; **no release tracking alpha-5/6** |
| AdvantageKit | v27.0.0-alpha-4 (2026-06-26) | **no template projects yet — see §3** |
| ThriftyLib | v2027.0.0-alpha-1 | tracks alpha-5/6 |
| **PhotonVision** | v2027.0.0-alpha-2 (2026-05-27) | *not in WPILib's table*; prerelease only, no vendordep — see §6 |
| **Elastic** | v2027.0.0-alpha8 (2026-05-08) | actively tracking 2027 |
| **maple-sim** | **none** | last release of any kind `v0.4.0-beta`, **2026-01-17** — see §7 |

Read that table honestly. **Two things you may want to depend on — ChoreoLib and maple-sim — have no 2027 story as of today.** maple-sim has not cut *any* release since January 2026, though the repo is still being pushed to (2026-07-08). That is a project-health signal, not proof of abandonment, but it means you should not architect a 2027 season around it in August.

Everything in that table will move before kickoff. **Re-check it in November and again the week of kickoff.** This is a recurring calendar item, not a one-time read.

### Systemcore hardware, verified

From the [Limelight Systemcore specification PDF](https://downloads.limelightvision.io/documents/systemcore_specifications_june15_2025_alpha.pdf) (alpha spec, dated 6-15-2025, revised 10/1/25) and the [WPILib Systemcore introduction](https://docs.wpilib.org/en/latest/docs/software/systemcore-info/systemcore-introduction.html):

| | Systemcore | roboRIO 2 (for contrast) |
|---|---|---|
| Host CPU | Raspberry Pi CM5, quad-core ARM Cortex-A76 @ 2.4 GHz (BCM2712) | dual-core ARM Cortex-A9 @ 866 MHz |
| RAM | 4 GB LPDDR4X-4267 | 512 MB |
| Storage | 16 GB eMMC | microSD |
| OS | LIMELIGHT OS — Linux 6.6 with `PREEMPT_RT` patches | NI Linux Real-Time |
| Real-time I/O | RP2350, dual Cortex-M33 @ 150 MHz, firmware loaded by host every boot | FPGA |
| CAN | **5 unique interfaces**, FD-capable, up to 8 Mbps, built-in 120Ω termination | 1 bus, 1 Mbps |
| I/O ports | 6 reconfigurable at runtime: DIO, PWM in/out, analog in (12-bit, ~8.75–9 ENOB), addressable LED\*, quadrature\* | fixed DIO/PWM/AI/relay |
| I2C | 2 interfaces, 100 kHz / 400 kHz | 1 |
| USB | 4× USB 3.0 Type-A, 5 Gbps shared, 2 A shared | 2× USB 2.0 |
| Ethernet | 1 Gbps | 10/100 |
| Expansion | PCIe 2.0 M.2 **A+E key, 30 mm** | none |
| IMU | onboard: 400 Hz quaternion, fused robot yaw, 3-axis accel + gyro | none |
| Display | 128×64 monochrome OLED (IPs, faults, team number, versions) | none |
| Power | 5–26 V buck-boost, 6 W idle / 40 W max, brownout 6.3 V (configurable) | 6.8 V brownout |
| Size / weight | 135.5 × 71.5 × 28.1 mm, 215 g | larger, heavier |

Items marked \* are flagged "in progress or subject to change" in the alpha spec.

**What this buys you concretely:**

1. **~10× the CPU.** The entire discipline of "optimize the robot loop so we don't overrun" mostly evaporates. See §3 for why 6328 built a distributed-computing framework in 2026 just to escape this, and why you should not.
2. **5 CAN buses, FD.** No more CANivore purchases to split a saturated bus. A direct dollar saving.
3. **Onboard IMU.** You do not buy a Pigeon 2 or navX. Straight savings, one less CAN device, one less failure point.
4. **Integrated Limelight vision.** Systemcore is built by Limelight Vision and runs their OS. FIRST's announcement states it "integrates Limelight vision technology, allowing teams to access powerful vision processing by plugging in a webcam" ([Introducing the Future Mobile Robot Controller](https://community.firstinspires.org/introducing-the-future-mobile-robot-controller)). **If this ships as described, it is the biggest budget win in this document** — see §6.
5. **M.2 A+E slot.** An accelerator (e.g. Hailo) or NVMe can go here. Do not budget for this in year one.
6. **Price.** FIRST states it is "on target to meet their goal of offering Systemcore at a lower price than the roboRIO" but has not published a number ([2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027)). **Treat Systemcore price as unknown; do not build a budget on a guess.**

### ⚠ What Systemcore *removes* — read this before you design a mechanism

This is the section most teams will miss, and it has **mechanical** consequences, not just software ones. Per [Removed features for 2027](https://docs.wpilib.org/en/2027/docs/yearly-overview/removed-features.html), the following are **not supported on Systemcore at all**:

| Removed | WPILib's stated reason | What it costs a small team |
|---|---|---|
| **Servo** | *"Systemcore doesn't have the ability to give servos the power they demand."* | **The big one.** Hobby servos are the cheap team's favorite actuator: hood adjusters, ratchet releases, climber latches, gamepiece gates, funnel flaps. Design around this or plan external power. |
| **Ultrasonic** | depends on `Counter`, which is removed | Cheap distance sensing (MB1013, HC-SR04) is gone. Use a CAN ToF sensor (CANrange, Redux Canandcolor) or vision. |
| **Relay** | not supported | Spike relays are gone. |
| **Counter** | not supported | Anything counting edges — flow sensors, cheap tachometers, ultrasonics. |
| **SPI** | not supported | **Kills ADIS16448, ADIS16470, ADXL345, ADXRS450.** Any SPI IMU you own is e-waste for 2027. |
| **Analog Gyro** | not supported | Legacy analog gyros gone. |
| **Analog Output** | not supported | — |
| **Analog Trigger**, **DMA**, **Interrupts**, **DigitalGlitchFilter**, **DigitalSource** | not supported / architectural change | Advanced DIO patterns must be rewritten. |
| **Axis Camera** | removed | Use `HttpCamera`. |
| **Nidec Dynamo Brushless** | *"zero teams used it"* | — |

**Practical consequence:** you have an onboard IMU (good — free, no SPI needed), and your sensing budget shifts from cheap analog/DIO parts toward **CAN sensors**. Since Systemcore gives you 5 CAN buses, that is a coherent design direction, but it is a *different* cost structure than 2026 and you should price it in the fall, not in week 2.

[UNVERIFIED workaround] The Systemcore spec lists PWM output among its 6 reconfigurable I/O ports, so an *externally powered* servo driven by a PWM signal may remain physically possible even though the WPILib `Servo` class is removed. **Do not plan on this** until someone demonstrates it on real hardware; the removal reason is about power delivery, and there may be no supported API. Treat it as a question to ask on Chief Delphi in the fall, not as a design assumption.

Also removed from the software side:

- **`PIDCommand`, `ProfiledPIDCommand`, `TrapezoidProfileCommand`** — *"removed for being poor abstractions."* Use the underlying controllers directly. (This is a good change; those classes taught bad habits.)
- **`RamseteController` / `RamseteCommand`** — replaced by the **LTV Unicycle Controller** for "more intuitive tuning."
- **`SwerveControllerCommand` / `MecanumControllerCommand`** — removed.
- **Mutable Java units** — removed in favor of immutable units; "Systemcore has sufficient memory."
- **`robotInit()`** — use the `Robot()` constructor.
- **`MathUtil.clamp()`** → `Math.clamp()` (Java 21+ built-in).
- **`Pose2d/3d.exp(Twist2d/3d)`** → `Pose.plus(Twist.exp())`.

### The 2027 API changes that will actually bite you

| Change | Impact |
|---|---|
| `edu.wpi.first.*` → `org.wpilib.*` (Java); `frc::` → `wpi::` (C++) | Every import in every tutorial, Chief Delphi post, and AI model output is wrong. See §11. |
| Java **25** and C++**23** required | Your dev machines need a current JDK; WPILib's installer handles it. |
| `MotorController.set()` → `setThrottle()`; `StopMotor()` removed → use `Disable()` | Mechanical rename, easy, but it is everywhere. |
| "Test" mode renamed **"Utility"** mode | Affects DS habits and any `isTest()` checks. |
| Individual gamepad classes → one **`Gamepad`** class (with touchpad) | `XboxController`/`PS4Controller`/`PS5Controller`/`StadiaController` code changes. |
| **`Rotation2d.getRadians()/getDegrees()/getRotations()` now return *wrapped* angles** | **Subtle and dangerous.** Any code that accumulated continuous rotation from these getters silently changes behavior. Audit turret/arm wrap logic. |
| Geometry classes are now **final** | You cannot subclass `Pose2d` etc. |
| `Rotation3d` interpolation now **slerp** (was lerp) | More correct; may change tuned behavior. |
| New `ChassisAccelerations` + drivetrain acceleration classes | New capability, worth knowing for feedforward. |
| FPGA clock → **monotonic clock** (steady clock on Systemcore) | `Timer` semantics; see the AdvantageKit determinism rules in §3. |
| NetworkTables v3 **removed** | Any NT3 tool dies. |
| GradleRIO **9.4.1**, **ZGC** default garbage collector | Fewer GC pauses; a real quality-of-life win. |
| **Commands v3** (Java) available alongside v2 | See below. |
| **OpMode framework** | An FTC-style alternative to command-based. |

### Commands v3 — what it actually is, and whether you should use it

This is the one genuinely new *programming model* in 2027, and the existing FRC commentary on it is thin, so here is the substance. Primary sources: the [WPILib commands-v3 design doc](https://github.com/wpilibsuite/allwpilib/blob/main/design-docs/commands-v3.md), the [2027 Javadoc](https://github.wpilib.org/allwpilib/docs/2027/java/org/wpilib/command3/Command.html), and the [Chief Delphi discussion thread](https://www.chiefdelphi.com/t/wpilib-commands-v3-imperative-function-bodies-with-coroutines/500699).

**The problem it solves.** In Commands v2, a command is split across `initialize()` / `execute()` / `isFinished()` / `end()`. Every new programmer's instinct is to write a `while` loop inside `execute()` — which blocks the scheduler and freezes the entire robot. v2's structure fights how people naturally think about a sequence of actions.

**How v3 works.** It uses **Java 21 continuations** — a JDK primitive that snapshots a function's call stack and resumes it later. A v3 command is *one function*:

```java
void commandBody(Coroutine coroutine) {
  initialize();
  while (!isFinished()) {
    execute();
    coroutine.yield();      // <-- hands control back to the scheduler
  }
  end();
}
```

The scheduler runs each command until it hits `coroutine.yield()`, then unmounts it, runs everything else, and remounts it next cycle exactly where it left off. **The `while` loop that was a catastrophic bug in v2 is the correct idiom in v3.**

Key API:
- `Coroutine.yield()` — cede control for one cycle.
- `Coroutine.await(Command)` — schedule a command and block until it finishes (async/await, as in JS/Python/C#).
- `Coroutine.fork(Command)` — schedule a command in parallel.

**Other v3 differences worth knowing:**

| Aspect | v2 | v3 |
|---|---|---|
| Structure | split init/execute/end | single function body |
| Nesting | needs proxy commands; children hidden from scheduler | children stay visible to scheduler |
| Naming | optional | **mandatory** (builders enforce it) |
| Telemetry | lists command names | maps commands → requirements with unique IDs |
| Priority | none | **priority levels**; higher-priority commands can't be interrupted by lower |
| Suspend/resume | none | commands can be suspended and auto-resumed |
| Scoping | global only | **Global / OpMode / Command** scopes for trigger bindings and defaults |

That scoping model is genuinely useful: an autonomous routine can register triggers that are cleaned up automatically when it exits, instead of polluting global state. And v3 fixes v2's "uncommanded state" problem where a parallel group owns mechanisms it never actually commands.

It also adds compile-time checks for unsafe coroutine usage, and a **declarative state machine API** alongside the imperative one.

**A concrete illustration of how green this is:** the Javadoc package moved from `org.wpilib.commands3` (alpha-3) to `org.wpilib.command3` (alpha-5/6) — the old path now 404s. A one-character package rename between alphas is normal for pre-release software, and it is exactly why you should learn the *concepts* now and write production code against v2.

**Recommendation for your team: learn Commands v2 first, plan to move to v3.**

Reasoning: every public repo in §10, every tutorial, every AdvantageKit template, and every Chief Delphi answer is v2. Your students will be reading v2 code all season. v3 is available in 2027 but the ecosystem around it will be near-empty at kickoff. The *concepts* — subsystem, requirement, trigger, composition — transfer completely. Adopt v3 when the templates and community examples catch up, most realistically the 2028 off-season. **Do try it in the off-season on a toy project**, because the coroutine model is genuinely easier to teach a first-year student, and if it clicks for your team the calculus changes.

### Your off-season action, stated plainly

Install the **[2027 Alpha WPILib](https://github.com/wpilibsuite/allwpilib/releases/tag/v2027.0.0-alpha-6)** on one machine and build a skeleton project against it *now*. You do not need Systemcore hardware to compile and run simulation. One mentor-hour a week from September through December, and you walk into kickoff already fluent in the API that every other team meets for the first time on January 9.

Also relevant: **[FRC3476/2027-Migrator](https://github.com/FRC3476/2027-Migrator)** — "Migration tool for importing 2026 WPILib projects to 2027 Alpha 6," a real Java tool from Team 3476 (BSD-3-Clause, last pushed 2026-08-18). Not needed if you start clean, but useful to read to understand the shape of the migration.

---

## 1. WPILib 2026 baseline (what you are migrating *from*, and what still applies)

### Language choice

**Java is the correct answer for a small team.** Not close.

- Every reference repo in §10 is Java or Kotlin. Every AdvantageKit template is Java. Every tutorial assumes Java.
- **C++** is used at the elite fringe: 6328's 2026 roboRIO layer is C++, 971 runs a C++ codebase. It buys deterministic memory and a bit of speed. On Systemcore's 4 GB / quad-A76 — with ZGC now default — that advantage collapses. C++ costs you students.
- **Python (RobotPy)** is real and supported, and is the fastest onramp for a student who already knows Python. But the vendor and community library ecosystem is thinner, AdvantageKit's Python analog is far less proven than the Java original, and **2027 renames every function camelCase→snake_case**. Use Python only if your students' existing Python fluency is the binding constraint on your season.
- **Kotlin** works (Team 3636 ships it — [FRC3636/frc-2026](https://github.com/FRC3636/frc-2026)) and is pleasant, but you inherit a smaller pool of people who can help you at 11 PM in week 5.

**Verdict: Java.**

### Command-based framework and project structure

[Command-based programming](https://docs.wpilib.org/en/stable/docs/software/commandbased/index.html) is the WPILib-blessed architecture and effectively universal at the top. The structure is consistent across every repo I inspected:

```
src/main/java/frc/robot/
  Robot.java              // lifecycle only; keep it nearly empty
  RobotContainer.java     // subsystem construction, button bindings, auto chooser
  Constants.java          // or a constants/ package
  subsystems/             // one package per mechanism
  commands/               // multi-subsystem coordination
  util/                   // helpers
src/test/java/frc/robot/  // JUnit 5 — yes, you will use this (§7)
```

Team 1678 adds a genuinely worth-stealing refinement: a `frc/lib/` tree separate from `frc/robot/`, holding reusable, season-independent infrastructure (`lib/io/vision/`, `lib/logging/`, `lib/math/`, `lib/sim/`) with only game-specific code in `frc/robot/`. That boundary is what lets a team carry real code between seasons instead of rewriting. **For a small team this is the highest-value structural decision you can make on day one, and it costs nothing.**

Team 2910 goes further and turns that idea into a labor multiplier — see §7, which is where I document their reusable base-subsystem pattern with real code. If you read only one architectural idea in this document, read that one.

### What changed in WPILib 2026

Per [New for 2026](https://docs.wpilib.org/en/stable/docs/yearly-overview/yearly-changelog.html) — and note WPILib's own framing: *"the WPILib team is heavily working on the 2027 Systemcore control system, and thus there are less changes for 2026 than in previous years."* 171 commits by 51 contributors since 2025.3.2.

- **Deprecations announced for 2027 removal:** Shuffleboard (no maintainer), SmartDashboard (NT3-only), PathWeaver (no swerve support), RobotBuilder (declining usage).
- **`Command.schedule()` deprecated** → `CommandScheduler.getInstance().schedule()`.
- New `Subsystem.idle()`.
- `Preferences.getNetworkTable()`; superclass field/method logging in Epilogue; protobuf-serializable type logging.
- Math: Eigen 5.0.0; `Pose3d.nearest()` / `Translation3d.nearest()`; `copyDirectionPow` joystick shaping; circular joystick deadband variants; `InchesPerSecondPerSecond`.
- **Bug fixes that matter:** TrapezoidProfile velocity limiting, **PoseEstimator teleportation on reset**, Rotation3d interpolation. If you ever saw a pose estimator jump on reset, that was this.
- `DCMotor` gains X44 and Minion. XRP gains RP2350 board support.
- Dropped: 32-bit Windows, macOS ≤12, Ubuntu 18.04/20.04, Windows 7/8.1. **Windows 10 support ends after the 2026 season** — budget for Windows 11 on programming laptops before 2027.
- 2025 projects must be re-imported due to GradleRIO changes. Same will be true 2026→2027.

---

## 2. Vendor libraries — what teams actually installed in 2026

Rather than speculate, here are the `vendordeps/` directories from repos I cloned. This is ground truth about the 2026 elite stack:

| Team | vendordeps |
|---|---|
| **6328** ([repo](https://github.com/Mechanical-Advantage/RobotCode2026Public)) | Phoenix6, REVLib, GrappleFRC *(AdvantageKit wired manually in `build.gradle` — see §3)* |
| **2910** ([repo](https://github.com/FRCTeam2910/2026CompetitionRobot-Public)) | **AdvantageKit**, BLine-Lib v0.8.4, PathPlannerLib 2026.1.2, Phoenix6 26.1.3, WPILibNewCommands, **maple-sim** |
| **1678** ([repo](https://github.com/frc1678/C2026-Public)) | ChoreoLib2026, Phoenix6, WPILibNewCommands, photonlib 2026.1.1 |
| **StuyPulse 694** ([repo](https://github.com/StuyPulse/StuyPlus-2026)) | **AdvantageKit**, **DogLog** 2026.5.0, PathPlannerLib, Phoenix6 26.3.0, **maple-sim** 0.4.0-beta |
| **YETI 3506** ([repo](https://github.com/yeti-robotics/rebuilt-2026)) | **AdvantageKit**, PathPlannerLib, Phoenix6, **URCL**, photonlib 2026.1.1, PlayingWithFusion |

Signals to read from this: **Phoenix 6 is universal. AdvantageKit is majority-but-not-unanimous. PathPlanner outnumbers Choreo. maple-sim showed up in its first season and immediately got adopted by serious teams. Nobody in this sample used YAGSL.**

Note also that **1678 uses no logging vendordep at all** — they wrote `frc/lib/logging/` themselves. And StuyPulse runs *both* AdvantageKit and DogLog, with a CI job literally named `doglog-replacement.yml`, which reads like a migration in progress.

**On BLine-Lib:** 2910's vendordep points at `com.github.edanliahovetsky:BLine-Lib:v0.8.4` via JitPack ([vendordep JSON](https://raw.githubusercontent.com/FRCTeam2910/2026CompetitionRobot-Public/main/vendordeps/BLine-Lib.json), [repo](https://github.com/edanliahovetsky/BLine-Lib), [JitPack artifact](https://jitpack.io/com/github/edanliahovetsky/BLine-Lib/v0.8.4/) — all verified live). BLine is a polyline-based path suite for holonomic drivetrains, introduced in [this Chief Delphi thread](https://www.chiefdelphi.com/t/introducing-bline-a-new-rapid-polyline-autonomous-path-planning-suite/509778). Team 3476 maintains a fork at [FRC3476/BLine-Lib-2](https://github.com/FRC3476/BLine-Lib-2). WPILib's own 2027 removed-features page names **"Choreo, PathPlanner, or Bline"** as PathWeaver's replacements — real institutional recognition for a young project. **Watch it; don't bet a season on it.**

---

## 3. THE ELITE STACK: AdvantageKit and AdvantageScope

Canonical source: **Team 6328 Mechanical Advantage**. [Docs](https://docs.advantagekit.org/) · [AdvantageKit repo](https://github.com/Mechanical-Advantage/AdvantageKit) (255★) · [AdvantageScope repo](https://github.com/Mechanical-Advantage/AdvantageScope) (286★) · [team software page](https://www.littletonrobotics.org/software/)

### What log replay actually is, and why it changes debugging

Conventional logging: you decide in advance what to record. Match goes wrong. You discover the one value you needed was not logged. You wait for the next match.

AdvantageKit logs **every input crossing the boundary into your robot code** — every sensor reading, every joystick axis, every DS packet, every CAN status frame, once per cycle. Afterward you re-run *the actual robot code* in a simulator, fed from the log. Because inputs are identical and the code is deterministic, all internal logic reproduces exactly. You can then add logging of a value you never recorded, change a constant, or modify an algorithm, and see what would have happened — **on real match data, at your desk, without the robot.**

The [log replay comparison page](https://docs.advantagekit.org/theory/log-replay-comparison/) gives hard numbers:

- AdvantageKit replays at roughly **50× real time**: a 10-minute match log replays in **12 seconds**.
- **598 teams** used AdvantageKit in 2025.
- The page demonstrates with real 6328 log data that with *non*-deterministic replay, within "a few seconds" of an autonomous routine "the state of the robot has completely diverged between real and replay." Determinism is not a nicety; without it, replay tells you nothing you can trust.

**For a small team this is the highest-value thing in this document after simulation.** You get roughly one hour of robot access for every ten a powerhouse gets. Log replay converts robot-time debugging into desk-time debugging. That is precisely the trade you need to make.

### The IO abstraction pattern (this is the whole architecture)

Per [IO interfaces](https://docs.advantagekit.org/data-flow/recording-inputs/io-interfaces/), every subsystem splits three ways:

```
subsystems/flywheel/
  Flywheel.java          // SubsystemBase: control logic ONLY. No vendor calls.
  FlywheelIO.java        // interface + @AutoLog inputs class
  FlywheelIOTalonFX.java // real hardware
  FlywheelIOSim.java     // physics sim
```

The inputs class carries public fields and an `@AutoLog` annotation, which generates `toLog()` / `fromLog()`. Every subsystem's `periodic()` begins:

```java
io.updateInputs(inputs);
Logger.processInputs("Flywheel", inputs);
```

Hard rules:
- **In the IO layer:** all sensor reads, all motor commands, all vendor-library calls.
- **In the subsystem:** all control logic, all decisions, all interpretation of `inputs`.
- Selection in `RobotContainer`: `Robot.isReal() ? new FlywheelIOTalonFX() : new FlywheelIOSim()`, with an empty `new FlywheelIO() {}` for replay.

This discipline is the cost, and it is also the benefit: it is *exactly* the abstraction that makes simulation (§7) work. You do not pay for it twice.

### What breaks replay — memorize this list

From [non-deterministic data sources](https://docs.advantagekit.org/getting-started/common-issues/non-deterministic-data-sources/):

| Do not | Do instead |
|---|---|
| `Timer.getFPGATimestamp()` | `Timer.getTimestamp()` |
| Read NetworkTables as an input (including dashboard values) | Route through an IO layer / `LoggedDashboard*` |
| `Math.random()` or any RNG | Seed deterministically, or eliminate |
| Iterate unordered collections (`HashMap`) | Use ordered collections |
| Read robot filesystem ad hoc | Treat file data as an input |
| Multithreading in robot logic | Keep logic single-threaded |
| **Use YAGSL or the Phoenix 6 swerve API** | Use AdvantageKit's swerve templates |

That last row is load-bearing and the docs are explicit: large libraries "like YAGSL or Phoenix 6 swerve" *"interact with hardware directly instead of through an IO layer."* **You cannot have both plug-and-play swerve and log replay.** This is the central architectural fork of §4.

### What's new in AdvantageKit 2026

From [What's New](https://docs.advantagekit.org/whats-new/): unit metadata on all logging interfaces (feeding AdvantageScope's unit-aware graphs); automatic `SystemStats` logging of NT clients (dashboards, vision coprocessors — connection status, IP, protocol) with no user code; console logging now captures **exceptions thrown during robot execution**, so you can debug a crash without digging through DS logs; `LoggedMechanism2d.generate3dMechanism()` for automatic 3D component poses; `Color` logging as hex triplets; TalonFXS and CANdi variants in the swerve template.

### ⚠ The 2027 status problem — corrected

AdvantageKit has a 2027 alpha (`v27.0.0-alpha-4`, published 2026-06-26). But the [installation docs](https://docs.advantagekit.org/getting-started/installation/) state plainly:

> **"Template projects are not currently available for the 2027 alpha versions of AdvantageKit."**

That is stronger than "only the skeleton is available," and it matters, because **"just clone the AdvantageKit swerve template" — the standard advice, and the recommendation this document would otherwise make — does not currently work for 2027.** The [template projects page](https://docs.advantagekit.org/getting-started/template-projects/) lists six templates (2026 KitBot, Differential Drive, Spark Swerve, TalonFX(S) Swerve, Vision, Skeleton), all for 2026 and earlier.

**How to plan around this honestly:**

1. **Most likely case:** templates ship before or shortly after kickoff. AdvantageKit has shipped templates every year; the library alpha exists; this is a "not yet" not a "never." [UNVERIFIED — no published commitment or date from 6328 that I could find.]
2. **Your off-season work is unaffected.** Build on the **2026** AdvantageKit swerve template now. You are learning the *pattern* — IO interfaces, `@AutoLog`, sim implementations, replay discipline. That knowledge ports directly; only the imports change.
3. **Set a decision date: mid-December.** If the 2027 swerve template exists, use it. If not, your fallback is the CTRE/REV vendor swerve (§4) and you accept losing replay on the drivetrain *only* — keeping the IO pattern for every other mechanism, which is where most of your debugging pain lives anyway.
4. **Do not let this block you.** The worst outcome is waiting for a template and arriving at kickoff with nothing built.

### Cost of adoption — honest accounting

**Real costs**
- **Dollars: $0.** AdvantageKit and AdvantageScope are free.
- **Concept load:** a first-year student meets an interface, an inputs class, dependency injection, and an annotation processor before writing a line of control logic. A genuine teaching cost. Budget for it.
- **File count:** ~4 files per subsystem instead of 1. (§7 shows how 2910 collapses this back down.)
- **Discipline tax:** the rules above are unforgiving. Violate one and replay silently produces plausible-but-wrong output, which is worse than no replay.
- **Log volume:** logging everything at 50 Hz produces large files. 6328 wrote a custom XZ-compressed writer (`.wpilogxz`, "~5x" reduction) because their 200 Hz logs were unmanageable. You will not hit that at 50 Hz, but plan USB-stick storage.

**Non-costs (things people wrongly worry about)**
- Performance on Systemcore: irrelevant. On a quad-A76 with 4 GB and ZGC, AdvantageKit's overhead is noise. This was a legitimate concern on the roboRIO; in 2027 it is not.

**Licensing note:** the AdvantageKit repo's license is reported by GitHub as `NOASSERTION`, meaning it is not a standard SPDX identifier GitHub recognizes. **Read `LICENSE` in the repo before you redistribute anything derived from it.** (6328's *robot code* repos are plain MIT.)

### AdvantageScope

The log viewer, and it is superb. Free, cross-platform, shipped inside the WPILib installer. Tabs: Line Graph, 2D Field, 3D Field, Table, Console, Statistics, Video (sync log to match video), Joysticks, Swerve, Mechanism, Points, Metadata.

2026 improvements ([What's New](https://docs.advantagescope.org/whats-new/)): unit-aware graphing with axis labeling and conversion; **log downloads from roboRIO 2–4× faster** (FTP instead of SFTP, up to 80 Mb/s); download from subfolders (fixes the CTRE Signal Logger workflow); REV `.revlog` support; basic CSV import; odometry and 3D field promoted to default tabs; correct visualization of cameras with nonzero roll; per-object colors; [AdvantageScope XR](https://docs.advantagescope.org/tab-reference/3d-field/advantagescope-xr/) stability improvements on iOS/iPadOS 26.

**Use AdvantageScope even if you reject AdvantageKit.** It reads plain WPILOG files from `DataLogManager` and connects live over NT4. There is no downside and no cost. Repo pushed 2026-08-20 — actively maintained.

### Do NOT copy 6328's 2026 architecture

6328's 2026 robot "Darwin" runs its **primary Java robot code on a Mac mini**, with a thin C++ client on the roboRIO, joined by a custom Protobuf-over-UDP framework called **Project Idun**. It has an annotation processor generating matching Java and C++ IO implementations, 64-bit build IDs verified across both devices, packet-loss tracking, a macOS `launchd` service, Mach-kernel real-time thread priority for the JVM loop, generational ZGC, `pmset` power management, and a "local drive" failover so the roboRIO can drive alone if the Mac mini dies. ([Idun README](https://github.com/Mechanical-Advantage/RobotCode2026Public/blob/main/idun/README.md); [build thread post](https://www.chiefdelphi.com/t/frc-6328-mechanical-advantage-2026-build-thread/509595/616))

Their motivation, from that build-thread post, is the clearest existing statement of why the roboRIO was the binding constraint on elite FRC software: unpredictable loop overruns risking auto routines, optimization work that could not be offloaded to simulation, and an inability to assess the risk of code changes at events because "seemingly small changes to one part of the code could have a large impact on unrelated parts."

They are also unambiguous about what you should do:

> "For the 2027 FRC season, [Systemcore](https://community.firstinspires.org/introducing-the-future-mobile-robot-controller) provides vastly improved performance compared to the roboRIO without the complexity and risks of Idun."
> — Idun README, with an explicit warning that the software "does not come with any promise of support or long-term maintenance"

**Idun is a monument to a problem that ceases to exist on January 9, 2027.** Read it for the engineering; copy none of it.

(One rules note worth knowing regardless: 6328 cite **R701**, which permits controlling motors directly from a coprocessor *provided the enable/disable signal originates from the roboRIO*. **Verify the equivalent rule in the 2027 manual** before designing anything around a coprocessor — the rule number and wording will change with the new control system.)

---

## 4. SWERVE: the central architectural fork

### The options

**1. Vendor generator — [CTRE Tuner X Swerve Project Generator](https://v6.docs.ctr-electronics.com/en/stable/docs/tuner/tuner-swerve/index.html) / [Phoenix 6 SwerveDrivetrain](https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/mechanisms/swerve/swerve-overview.html)**
Requires all-CTRE hardware: Kraken/Falcon/TalonFXS, Pigeon 2, CANcoder. You answer a GUI wizard; it emits a working project with odometry on a high-rate background thread. Fastest possible path to a driving swerve — realistically one build session.

Concrete detail worth knowing, from the [swerve builder API docs](https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/mechanisms/swerve/swerve-builder-api.html): the `SwerveDrivetrain` constructor takes an `odometryUpdateFrequency` parameter, and *"if unspecified or set to 0 Hz, this is **250 Hz on CAN FD**, and **100 Hz on CAN 2.0**."* That high-rate odometry thread is a genuine accuracy advantage over naive 50 Hz odometry, and it is a large part of why the vendor solution performs well. **On Systemcore, every CAN bus is FD-capable**, so the 250 Hz path is available to you by default in 2027.

*Cost:* vendor lock-in, and **it is not AdvantageKit-replay-compatible** (it touches hardware directly).

**2. [YAGSL](https://docs.yagsl.com/)** — Yet Another Generic Swerve Library. JSON-configured, hardware-agnostic (mix REV/CTRE/Thrifty), aims to make swerve "as easy as a `DifferentialDrive`."
*Important:* YAGSL has moved. The old `BroncBotz3481/YAGSL` now redirects to [`Yet-Another-Software-Suite/YAGSL_old`](https://github.com/Yet-Another-Software-Suite/YAGSL_old) (161★, archived state, last push 2025-03-19); the current repos are [`Yet-Another-Software-Suite/YAGSL`](https://github.com/Yet-Another-Software-Suite/YAGSL) (LGPL-2.1, pushed 2026-08-21 — actively developed) and [`YAGSL-Example`](https://github.com/Yet-Another-Software-Suite/YAGSL-Example) (86★). There is an active [2027/SystemCore-era beta](https://www.chiefdelphi.com/t/beta-yagsl-2026-8-18-the-2027-systemcore-era-beta/523434). Install via the WPILib vendordep tab; configure at `config.yagsl.com`.
*Cost:* same replay incompatibility, plus a config-file debugging model that hides the math from students. **None of the five elite repos I inspected use it.** That is not proof it is bad — YAGSL's stated audience is rookie-to-mid teams — but note where the top of the field actually is. **Note also the LGPL-2.1 license**, which carries different obligations than the MIT/BSD licenses on most FRC libraries; if you care about that, read it.

**3. [AdvantageKit swerve templates](https://docs.advantagekit.org/getting-started/template-projects/talonfx-swerve-template/)** ([Spark version](https://docs.advantagekit.org/getting-started/template-projects/spark-swerve-template/)) — a complete working swerve with the IO abstraction already built, including sim implementations, so replay and simulation work from hour one. **2026 only as of today — see the §3 warning.**

**4. [REV MAXSwerve template](https://github.com/REVrobotics/MAXSwerve-Java-Template)** (56★, BSD-3-Clause) — for MAXSwerve modules (2× SPARK MAX, NEO drive, NEO 550 turn, Through Bore absolute encoder). Fine and simple; same replay caveat.

### Recommendation for a small team

**Primary: the AdvantageKit swerve template matching your motor vendor — *if it exists for 2027 by mid-December*.** Reasoning:

- The plug-and-play appeal of YAGSL/CTRE is "swerve working fast." The AdvantageKit template *is also* a working swerve you clone and configure — the gap is one build session, not weeks.
- In exchange you get replay and working sim from day one, worth far more than that session to a team with limited robot access.
- Taking a vendor generator permanently forfeits the highest-leverage debugging tool in FRC for a benefit you consume once.

**Fallback if the 2027 template does not land: CTRE vendor swerve, and keep the IO pattern everywhere else.** This is not a defeat. Team 1678 — a Einstein-caliber program — runs the **Phoenix 6 swerve API with no AdvantageKit at all**, and still unit-tests their drivetrain in simulation (§7). You lose replay *on the drivetrain*. You keep it on the shooter, the intake, the elevator, the vision pipeline — which is where most of your season's debugging actually happens.

**Buy the module, don't build it.** MAXSwerve, SDS MK4/MK4i/MK4n, WCP SwerveX, ThriftySwerve. Building modules is a mechanical rabbit hole that returns nothing on the field. [UNVERIFIED: current module prices; historically ~$300–500/module, so ~$1,200–2,000 for a drivetrain. Re-price in November — see the BOM document.]

### Odometry, pose estimation, SysId

**Odometry** ([docs](https://docs.wpilib.org/en/stable/docs/software/kinematics-and-odometry/swerve-drive-odometry.html)) integrates module states + gyro into a pose. It drifts, always. Update rate matters: 250 Hz on CAN FD measurably beats 50 Hz, especially through hard accelerations in auto.

**Pose estimation** ([docs](https://docs.wpilib.org/en/stable/docs/software/advanced-controls/state-space/state-space-pose-estimators.html)) fuses odometry with absolute vision measurements in a Kalman filter. `SwerveDrivePoseEstimator` handles timestamped, latency-delayed vision via `addVisionMeasurement(pose, timestamp, stdDevs)`. **Getting the standard deviations right is most of the work** — see §6.

Two notes: the PoseEstimator "teleportation on reset" bug is fixed in 2026, and on Systemcore your gyro is the onboard 400 Hz fused-yaw IMU rather than a purchased device.

**SysId** ([docs](https://docs.wpilib.org/en/stable/docs/software/advanced-controls/system-identification/index.html)) determines feedforward gains by statistical fit: **kS** (static friction), **kV** (velocity), **kA** (acceleration), **kG** (gravity — elevators and arms only). Built-in mechanism types: simple motor (flywheel, turret, slider), elevator, arm. The `SysIdRoutine` API runs quasistatic and dynamic tests, logs to WPILOG, and you analyze in the SysId tool or AdvantageScope.

**For a small team:** run SysId on the drivetrain and on any elevator/arm. It takes ~20 minutes of robot time and replaces days of guess-and-check PID tuning. It is the single best hours-to-performance trade in FRC tuning. **Do it the first day the mechanism moves under its own power** — and write the `SysIdRoutine` into the subsystem in December, so that day costs you zero programming time.

---

## 5. AUTONOMOUS + PATHING

### PathPlanner vs Choreo — they solve different problems

**[PathPlanner](https://pathplanner.dev/)** ([repo](https://github.com/mjansen4857/pathplanner), 489★, MIT, latest stable `v2026.1.2`) — GUI path editor plus a full **auto-routine builder**, event markers, named commands, and — critically — **on-the-fly path generation** ([pathfinding docs](https://pathplanner.dev/pplib-pathfinding.html)). Maximum control over path shape, plus the ability to generate a path to an arbitrary target at runtime.

**[Choreo](https://github.com/SleipnirGroup/Choreo)** (195★, BSD-3-Clause, pushed 2026-08-17; docs at `choreo.autos`, reached via [sleipnirgroup.github.io/Choreo](https://sleipnirgroup.github.io/Choreo/)) — a **time-optimal** trajectory optimizer, described by its own repo as a "time-optimal drivetrain trajectory planner for the FIRST Robotics Competition." You give it waypoints and drivetrain constraints; it solves for the fastest physically-followable trajectory. The design goal is to eliminate the tweak-test-tweak loop: the output is, by construction, something the robot can actually track.

The distinction, cleanly stated by the community: PathPlanner "gives you a lot more control over your path compared to Choreo, but as a result, you can make a path the robot just can't physically follow." Choreo's paths are always followable but are **pre-generated only** — it cannot regenerate to match your actual starting state, so a robot that starts off-position will track a trajectory built for a position it isn't in. ([Choreo vs PathPlanner, Chief Delphi](https://www.chiefdelphi.com/t/choreo-vs-pathplanner/467373); [PathPlanner v. Choreo](https://www.chiefdelphi.com/t/pathplanner-v-choreo/484118))

**They compose.** PathPlannerLib can follow Choreo trajectories, standalone or inside GUI-built autos ([Choreo interop](https://pathplanner.dev/pplib-choreo-interop.html)). A common elite pattern: Choreo for the fast fixed auto trajectories; PathPlanner's pathfinding for teleop auto-align and on-the-fly moves.

### Recommendation

**PathPlanner, for a small team, in 2027.** Three reasons:

1. **PathPlannerLib tracks the current WPILib 2027 alpha (`v2027.0.0-alpha-3`); ChoreoLib does not.** ChoreoLib had a `2027.0.0-alpha-1` against WPILib alpha-2 but has no release tracking alpha-5/6. That may change by kickoff, but on August 2026 evidence PathPlanner is the safer bet.
2. On-the-fly pathfinding gives you teleop auto-align, a large driver-performance win per hour invested.
3. Its GUI auto-builder with named commands lets a *student* compose and modify auto routines without touching Java. For a team where the one confident programmer is a bottleneck, that is decisive.

Revisit in December: if ChoreoLib has a solid 2027 release, adding Choreo trajectories inside PathPlanner autos is a cheap upgrade, not a rewrite.

### Multi-path autos with real-time selection

The pattern used across strong teams:

1. Build several autos in the PathPlanner GUI (or as Choreo trajectory groups).
2. Register subsystem actions as **named commands** so paths trigger them via event markers.
3. Populate a `SendableChooser` on the dashboard ([Elastic](https://github.com/Gold872/elastic_dashboard)) so the drive team picks the auto behind the glass, after seeing the alliance's plan.
4. Add a second chooser for start position, and — the elite refinement — make selection *mode-aware*: 1678's test suite contains an `AutoModeSelectorTest` and an `AutoPlannerTest`, meaning their auto selection logic is important enough to have dedicated unit tests. Copy that idea.

Instrument this. Log the selected auto name, commanded vs. actual pose throughout, and each event marker firing. Auto failures are almost always a pose problem, and AdvantageScope's odometry tab shows it in ten seconds.

### Does auto decide matches?

In 2026 REBUILT, yes, structurally: **winning auto changed the game state for the rest of the match.** The alliance scoring the most Fuel in AUTO made the opponent's Hub Inactive for Shifts 1 & 3 and Active for Shifts 2 & 4 ([2026 Game Manual](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf); community summary at [frcmanual.com/2026/game-details](https://www.frcmanual.com/2026/game-details)). Ranking points came from Energized (100 Fuel), Supercharged (360 Fuel), and Traversal (50 Tower points).

The 2027 BIOCORE rules are unknown. But the multi-year trend — AprilTag localization from 2023, dynamic autos in 2024, autos that alter mid-match state in 2026 — is that auto is where software converts into ranking. **A small team with a reliable, well-tested 3-piece auto out-ranks a bigger team with a flashy, flaky 5-piece one.** Reliability is cheaper than ambition, and it is where simulation pays.

---

## 6. VISION

### The options

**[PhotonVision](https://docs.photonvision.org/)** ([repo](https://github.com/PhotonVision/photonvision), 420★, GPL-3.0, pushed 2026-08-20) — free, open-source, flashed onto a coprocessor you supply, paired with USB cameras. Maximum flexibility, real setup labor, excellent simulation support.

**Limelight 3/3A/3G/4** — self-contained smart camera. Plug in, configure in a web UI, read poses off NT. More expensive per unit, much less of your time. Limelight 4 is CM5-based and per the vendor "twice as powerful as Limelight 3G."

**Custom** (e.g. 6328's "Northstar") — do not. A full engineering project that buys you nothing over PhotonVision unless you are solving a problem PhotonVision does not.

### ⚠ PhotonVision's 2027 status is rough right now

PhotonVision is **not** in WPILib's SystemcoreTesting compatibility table. Its only 2027 artifact is **`v2027.0.0-alpha-2`, published 2026-05-27** and marked prerelease (verified via the GitHub releases API). There is no official vendordep.

Team YETI 3506 documents the current workaround on their **public engineering wiki** ([Current Solution for PhotonVision 2027](https://wiki.yetirobotics.org/books/robot-software/page/current-solution-for-photonvision-2027)): pull the `photonlib-offline` artifact from the 2027 branch in PhotonVision's GitHub Actions tab, extract it twice, copy the JSON into `vendordeps/`, and copy the maven folder into WPILib's local maven directory. It works, and it is exactly as fragile as it sounds.

**Two takeaways.** First, if you are betting on PhotonVision for 2027, budget mentor hours for manual dependency management until an official release lands, and re-check in November. Second — and this is a process point, not a software one — **YETI maintains a public team wiki documenting their engineering decisions.** That is a cheap, high-value practice for a small team, and it doubles as judging evidence (§9).

### Verified prices, August 2026

| Item | Price | Source |
|---|---|---|
| Limelight 4 | **$449.00** | [limelightvision.io/collections/products](https://limelightvision.io/collections/products) |
| Limelight 3 | **$400.00** | same |
| Limelight 3G | **$400.00** — **sold out** | same |
| **Limelight 3A** | **$189.00** — **sold out as of 2026-08-21** | same |
| Hailo-8 / 8L upgrade kit for LL4 | from **$95.00** | same |
| Arducam OV9281 USB camera (am-5749) | **$58.00** | [AndyMark](https://andymark.com/products/arducam-camera) |
| Orange Pi 5 4GB | **[UNVERIFIED]** — pricing and stock erratic in 2026; a 4 GB Plus variant was listed at $224.99 and out of stock in March 2026. Historic launch price ~$60. **Do not budget on the old number.** | vendor listings |
| Raspberry Pi 5 2GB | [UNVERIFIED] ~$50 | — |
| SparkFun XRP Kit (KIT-27644) | **$119.95**, FIRST team discount via support@sparkfun.com | [SparkFun](https://www.sparkfun.com/experiential-robotics-platform-xrp-kit.html) |

**Note the availability risk:** both the 3G and the 3A are showing sold out. The 3A is the budget recommendation below, so **if it comes back in stock and you are confident you need it, buying early is defensible** — but see the timing advice first.

PhotonVision's [recommended hardware](https://docs.photonvision.org/en/latest/docs/quick-start/common-setups.html):
- **Orange Pi 5 4GB** — 2 object-detection streams + 2 AprilTag streams @ 1280×800/30fps. *The only currently supported device for object detection.*
- **Raspberry Pi 5 2GB** — up to 2 AprilTag streams @ 1280×800/30fps.
- Cameras: **OV9281** for AprilTags, **OV9782** for object detection, either for driver cam.
- Industrial-grade SD card (they specifically name Sandisk SDSDQAF3-016G-I).
- Power: Pololu S13V30F5 or Redux Zinc-V regulator. **Do not skip this** — an unregulated Pi browning out mid-match is the classic vision failure.

### Budget guidance

**Do not buy vision hardware before November 2026.** The Systemcore claim — that it integrates Limelight vision and you can plug in a webcam — may eliminate the coprocessor line item entirely. Watch [wpilibsuite/SystemcoreTesting](https://github.com/wpilibsuite/SystemcoreTesting) and the WPILib 2027 docs, and re-price in November.

If you must plan today:

- **Tier 0 (~$0–120):** one webcam into Systemcore's built-in vision, if it delivers as announced. Assume this is the 2027 baseline until proven otherwise.
- **Tier 1 (~$190–380):** one or two **Limelight 3A** ($189 each). Best dollars-per-outcome in FRC vision for a small team: configured in a browser, no Linux administration, no SD-card corruption at 11 PM on Friday. Two cameras is meaningfully better than one for multi-tag geometry, so **2× 3A ($378) beats 1× LL4 ($449)** for pose estimation. Stock permitting.
- **Tier 2 (~$280–350):** Orange Pi 5 + 2× OV9281 ($116) + regulator, running PhotonVision — *if* you can source the Pi at a sane price, you have a student who genuinely wants to learn Linux, **and** you accept the 2027 prerelease situation above. Otherwise Tier 1 is a strictly better use of your hours.
- **Tier 3 ($449+):** Limelight 4, optional Hailo kit. Only if the 2027 game creates a specific object-detection requirement.

**The honest framing:** vision hardware is not your bottleneck. **Calibration and standard-deviation tuning are.** A well-calibrated $189 camera beats a badly-calibrated $449 one, every time.

### Making it actually work

**Camera calibration** ([PhotonVision calibration docs](https://docs.photonvision.org/en/latest/docs/calibration/calibration.html)) is mandatory, unglamorous, and the most-skipped step in FRC vision. An uncalibrated camera produces poses that are confidently, consistently wrong. Calibrate at the resolution you will run. Re-calibrate if you change lenses or resolution. Budget an hour; save a season.

**Multi-tag** is the big accuracy win. [PhotonPoseEstimator](https://docs.photonvision.org/en/latest/docs/programming/photonlib/robot-pose-estimator.html) offers nine strategies; the docs are direct about the choice:

> **Coprocessor MultiTag** (`estimateCoprocMultiTagPose`) — "Calculates a new robot position estimate by combining all visible tag corners. **Recommended for all teams as it will be the most accurate.**"

Others: `estimateLowestAmbiguityPose` (single-tag fallback), `estimatePnpDistanceTrigSolvePose` (uses distance from the best tag; requires `addHeadingData()`), `estimateConstrainedSolvepnpPose` (constrains the solve to a drivebase flat on the floor). `estimateRioMultiTagPose` is explicitly described as older, slower, and not recommended. Limelight's equivalent is [MegaTag2](https://docs.limelightvision.io/docs/docs-limelight/pipeline-apriltag/apriltag-robot-localization-megatag2), which uses robot yaw to disambiguate — feed it your gyro heading.

**Latency compensation** is why timestamps matter more than poses. Vision results arrive tens of milliseconds late. `EstimatedRobotPose` carries the timestamp at which the pose was *observed*; `SwerveDrivePoseEstimator.addVisionMeasurement(pose, timestamp, stdDevs)` rewinds its internal history to that instant, applies the correction, and replays odometry forward. If you pass `Timer.getTimestamp()` instead of the vision timestamp, the filter is being told a lie and your pose will lag and oscillate. **This is the #1 vision bug in FRC.**

**Standard deviations** control trust. The pattern strong teams use: scale them with tag distance and count — tight (trust vision heavily) with 2+ tags close in, loose with 1 tag far away — and reject outright any measurement that is off-field, more than ~1 m from the current estimate, or has high ambiguity. Tune these by replaying real logs, not by guessing.

**Field-variant tag layouts.** The 2026 game uses **36h11** AprilTags, and 6328's repo carries three separate layouts — `apriltags/welded`, `apriltags/andymark`, `apriltags/hq` — because field variants differ measurably. **Handle field-variant selection in code; do not hardcode one layout.** This is a real, match-losing detail that small teams routinely miss.

**Vision in simulation is real and free.** [PhotonVision simulation](https://docs.photonvision.org/en/latest/docs/simulation/index.html) renders simulated camera views of the tag field so your entire pose-estimation pipeline runs on a laptop. 1678's repo has `lib/io/vision/sim/photon/` as first-class code. This is how you debug vision in December.

---

## 7. SIMULATION + TESTING — the highest-leverage section in this document

**This is where a small team wins.** Powerhouse teams have three robots, a full field, and unlimited shop hours. You cannot buy that. You *can* have a simulator that runs on every student's laptop, at no cost, twelve months a year — and the gap between "we have one robot for six weeks" and "every student can develop and test any time" is the largest single equalizer available to you.

### The layers, cheapest first

**Layer 1 — WPILib Simulation GUI** ([docs](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/simulation-gui.html))
`./gradlew simulateJava`. Robot code runs on your laptop; a GUI exposes DS state, joysticks (plug a real controller into your laptop), and simulated device I/O. **Cost: zero. Setup: zero.** Works today, on any project, with no libraries.
*What it gets you:* enable/disable logic, button bindings, command scheduling, state machines, auto sequencing, dashboard layout. Roughly 60% of the bugs that eat robot time are found here.

**Layer 2 — Physics simulation** ([docs](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/physics-sim.html))
WPILib ships `FlywheelSim`, `ElevatorSim`, `SingleJointedArmSim`, `DCMotorSim`, `DifferentialDrivetrainSim` — physics models you drive with your commanded voltage, whose outputs you feed back as sensor readings. **This is where the AdvantageKit IO layer pays for itself:** your `*IOSim` class *is* the physics model, and nothing above it knows the difference. Your PID and feedforward tuning becomes approximately right before the mechanism exists. [Device sim](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/device-sim.html) covers vendor device simulation.

**Layer 3 — [maple-sim](https://shenzhen-robotics-alliance.github.io/maple-sim/)** ([repo](https://github.com/Shenzhen-Robotics-Alliance/maple-sim), 115★, BSD-3-Clause)
A rigid-body physics engine for FRC: the robot has mass, momentum, and friction, collides with field elements and other robots, and interacts with game pieces. It ships pre-integrated AdvantageKit swerve templates for both [Spark](https://github.com/Shenzhen-Robotics-Alliance/AdvantageKit-SparkSwerveTemplate-MapleSim) and [TalonFX](https://github.com/Shenzhen-Robotics-Alliance/AdvantageKit-TalonSwerveTemplate-MapleSim) hardware.

**Adoption check:** Team 2910 and StuyPulse both shipped it in 2026 vendordeps; Team 254 maintains [a fork](https://github.com/Team254/maple-sim). That is strong validation.

**⚠ Honest risk assessment, and this one changed since the last review.** 2026 was maple-sim's first season, and the maintainers warn to expect "occasional instability, bugs, and API changes." StuyPulse ran `maple-sim-0.4.0-beta`. But the harder fact from the releases API: **maple-sim's most recent release of any kind is `v0.4.0-beta`, dated 2026-01-17.** No stable release, no 2027 release, nothing in seven months — though the repo is still receiving pushes (2026-07-08).

**What to do with that:** use maple-sim in the off-season, because it is free and the driver-practice value is real today. **Do not make it a dependency of your 2027 season plan**, and do not let a competition auto depend on its numbers being right. If it has no 2027 release by mid-December, drop it and fall back to Layer 2, which is WPILib built-in and will always work.

**Layer 4 — Unit tests** ([docs](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/unit-testing.html))
JUnit 5 (Java) / Google Test (C++), in `src/test/java/`. In `build.gradle`:
```gradle
test {
    useJUnitPlatform()
    systemProperty 'junit.jupiter.extensions.autodetection.enabled', 'true'
}
```
The non-negotiable rule: **`HAL.initialize(500, 0)` must run before any WPILib hardware object is constructed.** Gotchas from the docs: always use a `DELTA` on floating-point assertions; the first failing assertion aborts the test; tests run on desktop only; and tests run by default on deploy (there is a "Skip Tests On Deploy" setting — you generally *want* them running).

**Layer 5 — Hardware-in-the-loop.** Real, but expensive at full scale: a bench with real motor controllers on a test board, deployed to like the robot. **For a small team, the 80/20 version costs almost nothing:** one motor + encoder bolted to a plank, wired to a spare controller and a spare power distribution path. You almost certainly already own the spares. It gets you real CAN behavior, real encoder noise, real current limiting, and real deploy cycles — the three things simulation cannot give you — and a first-year can own it without touching the competition robot. Build it in October.

### Three patterns to steal outright

#### (a) The 20 ms tick helper — Team 1678

Verified from a clone; this is the complete file at `src/test/java/frc/lib/TestUtil.java`:

```java
package frc.lib;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.wpilibj.simulation.SimHooks;
import edu.wpi.first.wpilibj2.command.CommandScheduler;

public class TestUtil {
	/**
	 * Advances the world by 20ms per iteration.
	 * This triggers periodic() methods and updates timers.
	 */
	public static void tick(int iterations) {
		for (int i = 0; i < iterations; i++) {
			CommandScheduler.getInstance().run();
			SimHooks.stepTiming(0.020);
		}
	}

	// tests all necessary pose things
	public static void testPose(Pose2d targetPose, Pose2d currentPose) {
		assertEquals(targetPose.getX(), currentPose.getX(), 0.2, "X out of tolerance");
		assertEquals(targetPose.getY(), currentPose.getY(), 0.2, "Y out of tolerance");
		assertEquals(
				targetPose.getRotation().getDegrees(),
				currentPose.getRotation().getDegrees(),
				5.0,
				"Rotation out of tolerance");
	}

	// to test poses without causing tests to fail
	public static boolean testCurrentPose(Pose2d targetPose, Pose2d currentPose) {
		return Math.abs(targetPose.getX() - currentPose.getX()) <= 0.2
				&& Math.abs(targetPose.getY() - currentPose.getY()) <= 0.2
				&& Math.abs(targetPose.getRotation().getDegrees()
								- currentPose.getRotation().getDegrees())
						<= 5.0;
	}
}
```

Thirty lines that let you write "run this command for 2 seconds and assert the robot arrived" as a unit test. Tolerances: 0.2 m and 5°. Their whole test suite is small and pointed: `DriveTest`, `AutoModeSelectorTest`, `AutoPlannerTest`, `TestUtil`. That is the right scope — **test the logic that has decided matches, not everything.**

#### (b) The test that teaches — Team 1678's `DriveTest`

This is worth copying not just for the assertions but because **the file is documentation and test in one artifact.** Its actual header:

```java
/**
 * FRC UNIT TESTING GUIDE FOR SWERVE DRIVE
 * =========================================
 *
 * KEY CONCEPTS:
 * 1. HAL INITIALIZATION: Must be done ONCE per test suite using @BeforeAll (static)
 * 2. ROBOT STARTUP: RobotBase.startRobot() initializes subsystems and their constructors
 * 3. SCHEDULER: CommandScheduler must be created after HAL/Robot initialization
 * 4. PER-TEST SETUP: Use @BeforeEach for state reset between individual tests
 * 5. SIMULATION MODE: !Robot.isReal() enables mocked hardware behavior
 *
 * STRUCTURE:
 *   @BeforeAll (static) → HAL + Robot initialization (runs ONCE)
 *   @BeforeEach → Reset state for each test (runs BEFORE EACH TEST)
 *   @Test → Individual test case (Arrange → Act → Assert pattern)
 */
```

And the mechanics:

```java
@Tag("Drive")
public class DriveTest {

	@BeforeAll
	static void setupHAL() {
		// This must happen BEFORE any WPILib or CTRE objects are created
		assert HAL.initialize(500, 0) : "HAL initialization failed";
	}

	@BeforeEach
	void setupBeforeEachTest() {
		assertNotNull(Drive.mInstance, "Drive subsystem should be initialized");
		assertNotNull(Drive.mInstance.getPose(), "Drive has not updated pose");
	}

	@Test
	void testInitialPoseIsSet() {
		TestUtil.testPose(Pose2d.kZero, Drive.mInstance.getPose());
	}

	@Test
	void testPeriodicTelemetry() {
		assertDoesNotThrow(
				() -> Drive.mInstance.periodic(), "Periodic telemetry output should not crash in simulation");
	}
	// ... testSwerveRequestUpdate, testDriveStateUpdate, testResetPoseCommand
}
```

**Note what this proves.** 1678 imports `com.ctre.phoenix6.swerve.SwerveRequest` — they run the **vendor** Phoenix 6 swerve, not AdvantageKit — and they still unit-test it in simulation. **Choosing a vendor swerve does not cost you testability.** It costs you log replay, and nothing else on this list.

#### (c) The smoke test — Team 6328

```java
@Test
public void createRobotContainer() {
    DriverStation.silenceJoystickConnectionWarning(true);
    try {
        new RobotContainer();
    } catch (Exception e) {
        e.printStackTrace();
        fail("Failed to instantiate RobotContainer, see stack trace above.");
    }
}
```

That is 6328's **entire** unit test suite in the public 2026 repo — one test proving the robot code can construct itself. StuyPulse ships the identical pattern. 2910 and YETI ship **zero** tests.

**Do not miss the lesson.** The best teams in FRC are not running 400-test suites. They run one test that catches "someone renamed a constant and now the robot won't boot" — the most common and most expensive competition failure — and it costs ten minutes to write. **Write this test in your first hour. It is the highest return-on-effort item in this entire document.**

### 🔑 The labor multiplier: 2910's reusable base subsystems

This is the single best structural idea I found in any 2026 repo, and it is the direct answer to "AdvantageKit means 4 files per subsystem, and we don't have the labor."

Verified from a clone of [FRCTeam2910/2026CompetitionRobot-Public](https://github.com/FRCTeam2910/2026CompetitionRobot-Public) (MIT licensed — you may legally copy this):

```
subsystems/base/
  MotorIO.java                 // ONE IO interface for every motor on the robot
  MotorIOTalonFX.java          // ONE real implementation
  SimMotorIOTalonFX.java       // ONE sim implementation
  BaseMotorConfig.java
  FusedCanCoderIO.java
  roller/
    RollerMotorSubsystem.java          // velocity/voltage control, no position limits
    RollerMotorSubsystemConfig.java
    RollerWithFollowersSubsystem.java
  servo/
    ServoMotorSubsystem.java           // position control, with limits + homing
    ServoMotorSubsystemConfig.java
    ServoWithFusedCanCoderSubsystem.java
```

**The insight:** almost every FRC mechanism is one of exactly two things.

- A **roller** — spins, you care about velocity, there is no meaningful end stop. Intakes, flywheels, indexers, feeders.
- A **servo** — moves to a position, has a min and max, usually needs homing. Arms, elevators, pivots, turrets, hoods.

2910 wrote each of those **once**, against **one** `MotorIO` interface, with **one** sim implementation. Their real mechanisms then become thin composition. Verbatim from `IntakeSubsystem.java`:

```java
public class IntakeSubsystem extends ServoMotorSubsystem {
    private final RollerMotorSubsystem rightRoller;
    private final RollerMotorSubsystem leftRoller;

    private boolean isHomed = false;
    private static final double deployAngle = Constants.IntakeConstants.INTAKE_MAX_ANGLE;
    private static final double retractAngle = 10.0;
    private static final double homingDutyCycle = -0.07;
    private static final double homingVelocityThreshold = 0.5;
    private static final double homingSettleTime = 0.1;
    // ...
    public enum WantedState { ... }
```

An intake — a deploy pivot plus two rollers — is **one class extending a base and composing two more**, plus constants and a state machine. No new IO interface. No new sim class. No new `@AutoLog` inputs class.

**Why this matters more to you than to 2910.** The standard objection to AdvantageKit is "4 files per subsystem × 6 subsystems = 24 files we don't have time to write." This pattern collapses that to **~6 shared files written once, then a config object and a state machine per mechanism.** You pay the abstraction cost one time, in the off-season, on a season-independent library — and in January you add mechanisms in an afternoon.

**Build this in December.** It is entirely game-independent. Whatever BIOCORE turns out to be, it will have rollers and it will have position-controlled joints.

Two further details worth stealing from their implementation:

1. **Homing is built into the base class.** `ServoMotorSubsystem` carries a homing routine parameterized by duty cycle, velocity threshold, and settle time. Every arm and elevator needs homing; writing it once is a large real saving, and it is the kind of code that is easy to get subtly wrong at 1 AM in week 5.
2. **They log the API calls, not just the state.** Every setter records what was commanded:
   ```java
   logKeySetVoltageOutput = motorName + "/API/setVoltageOutput/voltage";
   // ...
   Logger.recordOutput(logKeySetVoltageOutput, voltage);
   io.setVoltageOutput(voltage);
   ```
   When you are debugging "why did the arm go there," knowing *what your code asked for* — separately from what the mechanism did — cuts the search space in half.

Note their `MotorIO` also contains a delightful piece of honest engineering culture: `public String mechanismEndUnit = "David Units";` — a logged unit label defaulting to a joke, which tells you they hit real unit-confusion bugs and built the fix into the inputs class. Copy the fix, not the joke.

### Developing before the robot exists — your December plan

This is the concrete payoff. From kickoff (Jan 9) you have roughly six weeks; the robot typically doesn't move under its own power until week 3. Powerhouse teams absorb that with a second chassis. You absorb it with simulation.

Off-season (now through December), with no 2027 robot and no 2027 game:

1. **Build a swerve project on WPILib 2027 alpha.** Use the 2026 AdvantageKit swerve template as your teacher, port the pattern by hand. Get it driving in the sim GUI with a real controller.
2. **Write the reusable base subsystems** (roller + servo + one `MotorIO`), copying 2910's structure. This is the highest-value December work.
3. **Write the smoke test and the `tick()` helper.** Both game-independent, both carry forward forever.
4. **Build one generic mechanism end-to-end** using your base classes — a pivot with `SingleJointedArmSim`, a SysId routine, and a unit test. **Whatever BIOCORE is, you will need an elevator or a pivot.** In January you fill in constants instead of writing architecture.
5. **Stand up PhotonVision sim** against the 2026 tag field. The tag layout changes for 2027; the pipeline does not.
6. **Build the HIL plank** — one motor, one encoder, one spare controller.
7. **Practice the log-replay loop.** Record a sim log, replay it, add a logged value that was not originally recorded, confirm it appears. Do this until it is boring.
8. **Optionally add maple-sim** for driver practice — with the release-cadence caveat above.

Every one of those is game-agnostic. On January 9 you are configuring, not architecting — and you will be a week ahead of teams with three times your budget.

**The XRP option ($119.95, [SparkFun KIT-27644](https://www.sparkfun.com/experiential-robotics-platform-xrp-kit.html), FIRST discount available).** A small differential-drive robot that runs WPILib code. For teaching a first-year the deploy→test→iterate loop on real hardware without competing for robot time, this is $120 well spent. WPILib 2026 added RP2350 board support. Buy one or two; they are also excellent for outreach demos.

---

## 8. LOGGING + TELEMETRY

### What to use

**[DataLogManager](https://docs.wpilib.org/en/stable/docs/software/telemetry/datalog.html)** — WPILib built-in. Two lines in the `Robot()` constructor and every NT value plus DS state is written to a WPILOG on the USB stick. **If you adopt nothing else in this document, adopt this.** Free, essentially no CPU cost, and the difference between "the robot did something weird in QM47" and knowing exactly what happened.

**NetworkTables 4** ([docs](https://docs.wpilib.org/en/stable/docs/software/networktables/index.html)) — the pub/sub protocol between robot, dashboards, and coprocessors. **NT3 is removed in 2027**; any tool speaking NT3 dies.

Two NT4 practices worth adopting deliberately:

1. **Keep publisher/subscriber handles; do not call `getEntry()` in a loop.** Per the [publish and subscribe docs](https://docs.wpilib.org/en/stable/docs/software/networktables/publish-and-subscribe.html), *"Publishers are only active as long as the Publisher object exists"* — so store them as instance fields:
   ```java
   final DoublePublisher dblPub;
   public Example(DoubleTopic dblTopic) {
     dblPub = dblTopic.publish();
   }
   public void periodic() {
     dblPub.set(1.0);
   }
   ```
   In Java you must `close()` to stop publishing; C++ destructors handle it.

2. **Use struct publishers for geometry types.** `StructPublisher` and `StructArrayPublisher` ([Javadoc](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/networktables/StructPublisher.html), [array version](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/networktables/StructArrayPublisher.html)) publish `Pose2d`, `SwerveModuleState`, `ChassisSpeeds` and friends as binary structs rather than as loose arrays of doubles. This is both more bandwidth-efficient and — the part that matters day to day — **it is what makes AdvantageScope's 2D/3D Field and Swerve tabs light up automatically.** Publishing `SwerveModuleState[]` as a struct array gets you a live swerve visualization for free.

**Dashboards** ([choosing a dashboard](https://docs.wpilib.org/en/stable/docs/software/dashboards/dashboard-intro.html)):
- **[Elastic](https://github.com/Gold872/elastic_dashboard)** (146★, MIT, pushed 2026-08-21) — the driver dashboard. Flutter-based, now the most widely used driver dashboard in FRC, maintained by Nadav of FRC 353. Windows/macOS/Linux/Web. **Already shipping 2027 alphas (`v2027.0.0-alpha8`, 2026-05-08)** — one of the healthier 2027 stories in this document. 6328 ships a `2026_Elastic.json` layout in their repo root — **version-control your dashboard layout alongside your code**, which you should copy.
- **AdvantageScope** — the *analysis* tool. Not a driver dashboard. Use both; they are complementary.
- **Shuffleboard / SmartDashboard — dead.** Deprecated in 2026, removed in 2027. **Do not build a 2027 dashboard on them.** If your layouts live in Shuffleboard, port to Elastic this off-season.

**[Epilogue](https://docs.wpilib.org/en/stable/docs/software/telemetry/robot-telemetry-with-annotations.html)** — WPILib's annotation-based telemetry. Add `@Logged` to a class and its fields are logged automatically. 2026 added superclass field/method logging and protobuf-type support. **If AdvantageKit is too much for your team's skill level, Epilogue + DataLogManager is the right lighter-weight answer** — you lose replay, you keep good logs.

**Alternatives worth knowing:** **[DogLog](https://doglog.dev)** ([repo](https://github.com/jonahsnider/doglog), pushed 2026-08-21) — deliberately simple logging, minimal ceremony, no replay. Used by StuyPulse alongside AdvantageKit. **[URCL](https://github.com/Mechanical-Advantage/URCL)** (Unofficial REV-Compatible Logger, MIT) — captures SPARK data REVLib doesn't expose; used by YETI. If you run SPARKs, URCL is nearly free value.

### What to log

- **Everything crossing the IO boundary** (AdvantageKit does this automatically): every motor voltage/current/temperature/position/velocity, every encoder, every limit switch, every gyro axis.
- **Every setpoint alongside every measurement.** A measurement without its setpoint is nearly useless for tuning.
- **What your code commanded**, separately from what happened — 2910's `/API/` logging pattern (§7).
- **Estimated pose, odometry-only pose, and each vision measurement with its timestamp, tag count, and ambiguity.** This is how you debug the pose estimator, and you will need to.
- **Command scheduling events** — which commands started, ended, were interrupted.
- **Auto selection, and each event marker firing.**
- **Battery voltage and total current.** Brownouts explain a startling share of "the code broke."
- **Loop timing.** Less critical on Systemcore but still the first thing to check when behavior gets weird.
- **[Persistent alerts](https://docs.wpilib.org/en/stable/docs/software/telemetry/persistent-alerts.html)** — surface "CANcoder 12 not responding" on the dashboard *before* the match, not in the log afterward. Cheap, and it catches failures that actually cost matches.
- **Build metadata** — git hash, branch, dirty flag, build time. When a log shows odd behavior the first question is always "which code was this?"

### Post-match log review as a routine

This is a *process* recommendation, and the one most teams skip.

**After every single match, before the next one:**
1. Pull the log (USB stick, or download over NT — AdvantageScope's download is 2–4× faster in 2026 via FTP, up to 80 Mb/s).
2. Open AdvantageScope. Check three things, in order, every time:
   - **Odometry tab:** did the estimated pose track reality through auto? Any teleport or drift?
   - **Line graph:** any brownout, any loop overrun, any current spike?
   - **Console tab:** any exception? (2026 AdvantageKit captures exceptions thrown during robot execution — you no longer have to dig through DS logs.)
3. Log a one-line entry in a shared doc: match number, anything anomalous, action taken.

Assign this to **one named student as their competition role.** It takes five minutes per match and it is the mechanism by which a small team appears to have a large software team. Championship teams do this reflexively; the practice, not the headcount, is what you are copying.

Use the **Video tab** to sync log data against match video from The Blue Alliance. Watching the robot and the graph simultaneously turns "it seemed sluggish" into "the flywheel never reached setpoint because current limited at 3.2 s."

---

## 9. ENGINEERING PROCESS

### Git workflow

Use GitHub. Free for public repos; free private repos with unlimited collaborators. [UNVERIFIED: current nonprofit/education terms — verify at github.com/nonprofit.]

**Branch model (deliberately minimal):**
- `main` is always deployable. Protect it: no direct pushes.
- One branch per feature or per student: `elevator-pid`, `auto-3piece`, `vision-stddev`.
- PR into `main`. Require CI green and one review.
- Tag every competition-deployed commit: `git tag week1-qm47`. **When something breaks at an event, you need to get back to known-good in 60 seconds, not archaeology.**

**Event discipline:** at competition, branch protection stays on but the reviewer can be a mentor at the pit table. What you must never lose is the ability to answer "what code is on the robot right now?" That is what tags and logged build metadata are for.

**Steal this from YETI 3506** — [`.github/workflows/auto-pr.yml`](https://github.com/yeti-robotics/rebuilt-2026): pushing any new non-`main` branch automatically opens a **draft PR** from a PR template. Students get a review surface without having to remember to create one. Ten lines of YAML that changes team behavior.

### ⚠ The pit workflow nobody documents: build offline

Competition venues have hostile or absent Wi-Fi, and Gradle's default behavior is to try to reach the internet for dependency resolution. A build that works in your shop can hang for minutes or fail outright in the pit.

**The fix is one flag:**

```bash
./gradlew deploy --offline
```

Per [GradleRIO's README](https://github.com/wpilibsuite/GradleRIO/blob/main/README.md), you must be online for the *first* build so dependencies are cached; after that, `--offline` prevents Gradle from attempting to update or download anything. IntelliJ and Eclipse expose the same setting in their Gradle preferences.

**Make this a pre-event checklist item:**
1. The week before the event, on every programming laptop: do a full online build, then **verify a clean `--offline` build succeeds.** Discovering a missing cached artifact in your shop is free; discovering it in the pit costs a match.
2. Do this again after *any* vendordep change.
3. Bring the vendordep JSONs and, if you can, an offline maven copy — this is exactly what YETI's PhotonVision workaround (§6) depends on.
4. 6328's `build.gradle` runs deploy with `-x spotlessApply` so formatting never blocks a competition deploy, and wraps deploy in a **retry loop** with `maxRetries` because pit networking is bad. Both are small, competition-tested touches worth copying.

### CI: GitHub Actions building robot code

Every serious team does this and it is nearly free (GitHub Actions is free on public repos, with a monthly minute allowance on private ones). The pattern is identical across teams — here is 1678's, verbatim in structure:

```yaml
name: Build
on:
  push: { branches: [main] }
  pull_request:
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-22.04
    container: wpilib/roborio-cross-ubuntu:2025-22.04   # bump for 2027
    steps:
      - uses: actions/checkout@v4
      - name: Cache Gradle
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle', 'vendordeps/**/*.json') }}
          restore-keys: ${{ runner.os }}-gradle-
      - name: Add repository to git safe directories
        run: git config --global --add safe.directory $GITHUB_WORKSPACE
      - run: chmod +x gradlew
      - run: ./gradlew build
```

Run **three jobs**: `./gradlew build`, `./gradlew test`, `./gradlew spotlessCheck`. 1678 splits them into `build.yml` / `tests.yml` / `formatter.yml`; 2910 runs `build` and `spotless` as two jobs in one `main.yml`. Either is fine. The Gradle cache and `concurrency.cancel-in-progress` keep CI fast enough that students don't route around it.

**Note:** the container tag needs a 2027 equivalent, and the Systemcore toolchain differs from `roborio-cross`. Watch [wpilibsuite](https://github.com/wpilibsuite) for the 2027 image. [UNVERIFIED: no 2027 cross-compile container published as of 2026-08-21.]

### Formatting and linting: Spotless

Non-negotiable, and it costs one line. 6328 uses `com.diffplug.spotless` `6.25.0` in `build.gradle`. Configure `googleJavaFormat()`, run `spotlessApply` locally, enforce `spotlessCheck` in CI.

**Why it matters more for a small team than a big one:** it ends 100% of formatting arguments in code review, and it makes diffs show *what changed* rather than what got reindented. With three programmers you cannot afford to spend review attention on whitespace.

### Code review with students

- **Review is teaching, not gatekeeping.** The mentor comment that matters is "what happens here if the encoder returns NaN?" not "add a space."
- **Small PRs.** A 40-line PR gets a real review; a 900-line PR gets "LGTM."
- **Require the author to explain the change in the PR description** in plain English. This is where they discover they don't understand their own code.
- **Rotate reviewers.** Second-year students should review first-years. Reviewing teaches more than being reviewed.
- **Use a PR template** (see YETI's auto-PR above) so the description is structured rather than blank.

### The bus-factor problem, named

Small teams almost always end up with **one student who can actually debug the robot**, and that student graduates. This is a bigger threat to your program than any library choice in this document. Mitigations that cost nothing:

- **Two people touch every subsystem.** Enforce it through PR assignment, not exhortation.
- **The post-match log review (§8) belongs to a *different* student than the one who writes the most code.** It is the cheapest way to build a second person who understands robot behavior.
- **Write the December infrastructure work as a teaching exercise**, not as a mentor solo project. The base subsystems in §7 are ideal for this: regular, reviewable, and the student who writes them understands the whole architecture by construction.
- **Keep a team wiki.** YETI's public [wiki.yetirobotics.org](https://wiki.yetirobotics.org/books/robot-software/page/current-solution-for-photonvision-2027) is a working example. A wiki page for "how to deploy," "how to calibrate a camera," "how to pull a log" turns tribal knowledge into an asset that survives graduation — and it is direct evidence for judged awards.

### Onboarding a first-year programmer

An 8-week path, one meeting a week, that produces someone who can contribute:

| Week | Activity |
|---|---|
| 1 | [Zero to Robot](https://docs.wpilib.org/en/stable/docs/zero-to-robot/introduction.html). Install WPILib. Build and *simulate* the example project. No robot needed. |
| 2 | Git: clone, branch, commit, push, PR. Have them submit a PR that changes a comment. The point is the mechanics, not the content. |
| 3 | XRP ($119.95) or the HIL plank: write a command that drives forward for 2 seconds. Deploy it. Watch it work. |
| 4 | Command-based concepts: subsystem, command, requirement, trigger. Bind a button. |
| 5 | Read a real subsystem from your codebase together. Have them trace one value from sensor to motor output. |
| 6 | AdvantageScope: open a log from last season, find the flywheel setpoint vs. measurement, explain the gap. |
| 7 | Write the smoke test (§7). Genuinely useful, ~15 lines, teaches JUnit. |
| 8 | Own one small mechanism end-to-end using the base subsystems: config, state machine, sim. Ship it through a PR. |

**Design principle:** every step produces something that runs and that they can *see*. Nothing in weeks 1–4 requires competing for robot access. This is only possible because of the simulation investment in §7 — which is the real argument for it.

### Academic integrity / student-learning flags

- **If a student cannot explain the code in their PR, it does not merge.** This one rule handles copy-paste from other teams, from Chief Delphi, and from AI, uniformly, without singling out any source. It is the only integrity policy you need.
- **Copying open-source team code is encouraged in FRC culture** and is what §10 is for — but with attribution in a comment, and with understanding. **Check each repo's license before copying:** 6328's robot code, 2910, 1678-adjacent, 254, StuyPulse, 341, and 1540 repos are MIT or similar; **YAGSL is LGPL-2.1**; **PhotonVision is GPL-3.0**; the AdvantageKit library itself reports as `NOASSERTION` and needs a manual read. Licensing is also a genuinely good teaching moment about professional engineering.
- **FIRST awards rest on student *understanding*.** The **FIRST Leadership Award** (renamed from Dean's List for 2026; `reference/awards/00_AWARD_LIST_VERIFIED.md`), Woodie Flowers, and Engineering Inspiration are evaluated by judges asking *students* how things work. Architecture that no student can explain is a liability in the judging room even when it works on the field. This is a real cost of over-adopting sophisticated infrastructure, and it should temper how much of this document you take on in one season.

---

## 10. REAL REPOS TO STUDY — verified live, August 2026

All URLs queried through the GitHub API on 2026-08-21; language, stars, last push, and license are as returned that day.

| # | Team | Repo | Lang | ★ | Last push | License | Steal this |
|---|---|---|---|---|---|---|---|
| 1 | **6328** Mechanical Advantage | [Mechanical-Advantage/RobotCode2026Public](https://github.com/Mechanical-Advantage/RobotCode2026Public) | Java | 82 | 2026-08-19 | MIT | The canonical AdvantageKit codebase. Subsystem structure (`drive`, `launcher`, `hopper`, `kicker`, `vision`, `sensors`, `leds`). Three AprilTag layouts (`welded`/`andymark`/`hq`). Deploy-with-retry. `replayWatch` Gradle task. The `RobotContainerTest` smoke test. Read `idun/README.md` for the engineering; **do not copy Idun** (§3). |
| 2 | **6328** (2025) | [Mechanical-Advantage/RobotCode2025Public](https://github.com/Mechanical-Advantage/RobotCode2025Public) | Java | 66 | 2025-10-15 | MIT | **Start here, not with 2026.** "Manta" is a clean, single-processor AdvantageKit codebase — the architecture to actually imitate, without the Mac mini distraction. |
| 3 | **2910** Jack in the Bot | [FRCTeam2910/2026CompetitionRobot-Public](https://github.com/FRCTeam2910/2026CompetitionRobot-Public) | Java | 13 | 2026-06-07 | MIT | **The most valuable repo in this list for a small team.** `subsystems/base/roller` + `subsystems/base/servo` — reusable base subsystems over a single `MotorIO` (§7). Built-in homing. `/API/` call logging. Dedicated `simulation/` package, clean `config/` vs `constants/` split. Simple 2-job CI. |
| 4 | **1678** Citrus Circuits | [frc1678/C2026-Public](https://github.com/frc1678/C2026-Public) | Java | 14 | 2026-06-01 | NOASSERTION | **The best testing example in FRC public code.** `TestUtil.tick()`, `testPose()` tolerances, `DriveTest` as documentation, `AutoModeSelectorTest`, `AutoPlannerTest`. The `frc/lib` vs `frc/robot` split. `lib/io/vision/` abstracting Limelight *and* PhotonVision *and* sim behind one interface. Uses vendor Phoenix 6 swerve, no AdvantageKit — **proof that disciplined architecture beats any specific library.** |
| 5 | **254** The Cheesy Poofs | [Team254/FRC-2025-Public](https://github.com/Team254/FRC-2025-Public) | Java | 43 | 2025-09-09 | MIT | 2026 code not public as of Aug 2026 (254 traditionally releases in the off-season — check back). Study 2025 for control abstractions. Also [FRC-2024-Public](https://github.com/Team254/FRC-2024-Public) (40★) and their [maple-sim fork](https://github.com/Team254/maple-sim). |
| 6 | **694** StuyPulse | [StuyPulse/StuyPlus-2026](https://github.com/StuyPulse/StuyPlus-2026) | Java | 20 | 2026-07-25 | MIT | Very readable commands tree (`commands/swerve/driveAligned`, `commands/swerve/PIDtoPose` — auto-align patterns worth lifting directly). Runs AdvantageKit **and** DogLog, with a `doglog-replacement.yml` workflow documenting a live migration. A `javadoc.yml` workflow that publishes docs. |
| 7 | **3506** YETI | [yeti-robotics/rebuilt-2026](https://github.com/yeti-robotics/rebuilt-2026) | Java | 5 | 2026-08-13 | NOASSERTION | **Best process automation in this list.** `auto-pr.yml` auto-opens draft PRs from a template. `skill-review.yml` runs an AI reviewer ([yeti-robotics/frc-reviewer](https://github.com/yeti-robotics/frc-reviewer)) on `@frc-reviewer` comments. A `subsystems/battery` subsystem most teams skip. Plus a genuinely good [public engineering wiki](https://wiki.yetirobotics.org/). |
| 8 | **3636** Generals | [FRC3636/frc-2026](https://github.com/FRC3636/frc-2026) | Kotlin | 6 | 2026-07-27 | NOASSERTION | The serious Kotlin reference. Worth reading even if you stay in Java, to see how much boilerplate the language removes. |
| 9 | **341** Miss Daisy | [Team341/FRC2026-Public](https://github.com/Team341/FRC2026-Public) | Java | 2 | 2026-05-19 | MIT | A veteran team's clean, non-exotic season release — a realistic target for what a strong small-team codebase looks like. |
| 10 | **1540** Flaming Chickens | [flamingchickens1540/robot2026](https://github.com/flamingchickens1540/robot2026) | Java | 4 | 2026-05-15 | MIT | Mid-size team, well-maintained, an accessible read. |
| 11 | **971** Spartan Robotics | [frc971/971-Robot-Code](https://github.com/frc971/971-Robot-Code) | C++ | 71 | 2025-07-20 | Apache-2.0 | A different universe: Bazel, custom realtime middleware, C++. **Not a model to copy.** Read it to see the far end of the distribution, then don't go there. (GitHub is a mirror; primary development is elsewhere.) |

**Reading order for a small team:** #2 (6328 2025, for the AdvantageKit pattern) → #3 (2910, for the labor-saving structure) → #4 (1678, for testing) → #7 (YETI, for process). That is four repos and roughly a weekend, and it is most of the value in this list.

**Infrastructure repos worth reading:**
[wpilibsuite/allwpilib](https://github.com/wpilibsuite/allwpilib) (1294★) · [wpilibsuite/SystemcoreTesting](https://github.com/wpilibsuite/SystemcoreTesting) (175★ — **the 2027 primary source; bookmark it**) · [wpilibsuite/GradleRIO](https://github.com/wpilibsuite/GradleRIO/blob/main/README.md) · [Mechanical-Advantage/AdvantageKit](https://github.com/Mechanical-Advantage/AdvantageKit) (255★) · [Mechanical-Advantage/AdvantageScope](https://github.com/Mechanical-Advantage/AdvantageScope) (286★) · [mjansen4857/pathplanner](https://github.com/mjansen4857/pathplanner) (489★) · [SleipnirGroup/Choreo](https://github.com/SleipnirGroup/Choreo) (195★) · [PhotonVision/photonvision](https://github.com/PhotonVision/photonvision) (420★) · [Shenzhen-Robotics-Alliance/maple-sim](https://github.com/Shenzhen-Robotics-Alliance/maple-sim) (115★) · [Gold872/elastic_dashboard](https://github.com/Gold872/elastic_dashboard) (146★) · [Yet-Another-Software-Suite/YAGSL](https://github.com/Yet-Another-Software-Suite/YAGSL) · [REVrobotics/MAXSwerve-Java-Template](https://github.com/REVrobotics/MAXSwerve-Java-Template) (56★) · [FRC3476/2027-Migrator](https://github.com/FRC3476/2027-Migrator) · [LimelightVision/systemcore-os-public](https://github.com/LimelightVision/systemcore-os-public) (29★) · [wpilibsuite/FirstDriverStation-Public](https://github.com/wpilibsuite/FirstDriverStation-Public) (36★)

---

## 11. AI in the 2026/2027 FRC software workflow — an honest assessment

You are making budget decisions from this, so here is the unvarnished version.

### Where AI genuinely earns its keep

- **IO-layer boilerplate.** AdvantageKit's pattern is ~4 files of highly regular code per subsystem. Generating `FlywheelIO` / `FlywheelIOTalonFX` / `FlywheelIOSim` from a description is exactly the mechanical transformation LLMs do well, and it removes the main ergonomic objection to AdvantageKit. **This is the strongest AI use case in FRC software.** (Note that 2910's base-subsystem pattern in §7 removes most of this work *architecturally* — which is better, because it removes the code rather than generating it faster.)
- **Test scaffolding.** Generating JUnit tests around an existing subsystem, given the `tick()` helper pattern, works well.
- **Log analysis scripting.** "Write a Python script that reads this WPILOG and plots flywheel setpoint vs. measurement for every match" is a solid, verifiable task.
- **Explaining code to students.** Genuinely useful as a patient tutor for a first-year reading an unfamiliar subsystem — *with the caveat below*.
- **Documentation.** Turning a working subsystem into a README, a wiki page, or a judging-binder page.
- **Automated PR review.** Real teams ship this today: YETI's [frc-reviewer](https://github.com/yeti-robotics/frc-reviewer) runs on `@frc-reviewer` in a PR comment. Useful as a **first-pass** reviewer catching obvious problems before mentor time is spent — not a replacement for the mentor.

### Where it does not work, and where it is actively dangerous

- **THE 2027 TRAINING-DATA PROBLEM — read this twice.** Every FRC code example ever written uses `edu.wpi.first.*`, `frc::`, `robotInit()`, `MotorController.set()`, `XboxController`, `PIDCommand`, and Commands v2. **All of that is wrong in 2027.** Models will confidently emit 2026-shaped code that does not compile, or worse, compiles against something deprecated and misbehaves. Expect AI assistance for WPILib to be **substantially less reliable in early 2027 than it was in 2026**, and to stay that way until enough 2027 code exists publicly — realistically well past kickoff. **Budget mentor hours accordingly and verify every AI-suggested WPILib API against [docs.wpilib.org/en/2027/](https://docs.wpilib.org/en/2027/).**
- **The subtle-semantics trap.** Some 2027 changes are *renames* (loud, caught by the compiler) and some are *behavior changes* (silent). `Rotation2d.getDegrees()` now returning a wrapped angle is the dangerous kind: AI-generated 2026-style turret-wrap code will compile perfectly in 2027 and be wrong. **The compiler is not your safety net for this class of change.**
- **Constants and tuning.** An AI cannot tell you your kV. Only SysId and your actual mechanism can. Numbers produced by a model are fabrications with the syntax of measurements — the most dangerous failure mode in this list.
- **Hallucinated APIs.** Vendor libraries (Phoenix 6, REVLib, PhotonLib) change yearly and models blend versions. Every vendor call needs checking against current docs.
- **Physical intuition.** "Why does the arm oscillate at the top?" is a question about backlash, gravity, and sensor placement. The model has never seen your arm.
- **Anything safety-adjacent.** Current limits, soft limits, brownout behavior. Verify by hand, always.

### Rules to adopt before January

1. **No AI-generated code merges unless a student can explain every line.** Applies identically to code copied from Chief Delphi or from the repos in §10. Enforced at PR review.
2. **AI never sets a number that describes physical reality.** Gains, limits, gear ratios, field dimensions come from measurement, SysId, or the game manual.
3. **Verify every WPILib/vendor API against the 2027 docs.** Assume the model's version is stale.
4. **Log what AI wrote.** Not for punishment — so that when something behaves oddly you know which code got human scrutiny.
5. **Judging is about students.** A judge asks the student. Architecture no student can explain costs you awards even when it wins matches. This is not hypothetical; it is how the **FIRST Leadership Award** (formerly Dean's List) and Engineering Inspiration are actually evaluated.

**Net assessment:** in 2026, AI is a genuine multiplier on FRC boilerplate and documentation — plausibly worth 20–40% of programming labor on the mechanical parts of the job [UNVERIFIED estimate; no rigorous FRC-specific measurement exists]. It is not a multiplier on tuning, debugging physical systems, or design judgment, and **the 2027 API break temporarily degrades even the parts that work.** Plan your season assuming AI helps with typing and hurts with WPILib recall.

---

## 12. The decision summary

| Decision | Recommendation | Why |
|---|---|---|
| Language | **Java** | Ecosystem, examples, every reference repo |
| Framework | **Command-based v2** now; try **v3** in off-season, adopt when examples exist | v2 is what all examples use; concepts transfer completely |
| Control system | **Systemcore** (no choice) | Prepare now — it is your equalizer |
| Sensing plan | **Re-architect around CAN sensors** | Servo, ultrasonic, relay, counter, SPI, analog gyro all removed in 2027 |
| Logging | **AdvantageKit** (fallback: Epilogue + DataLogManager) | Replay converts robot-hours into desk-hours |
| Analysis | **AdvantageScope** | Free, best-in-class, no downside, use it regardless |
| Driver dashboard | **Elastic** | Shuffleboard/SmartDashboard removed in 2027; Elastic already on 2027 alphas |
| Swerve | **AdvantageKit swerve template if it ships for 2027; else CTRE vendor swerve** | Decision date mid-December. Vendor swerve costs replay only — 1678 proves it's survivable |
| Modules | **Buy** (MAXSwerve / MK4i / SwerveX / Thrifty) | Building modules returns nothing on the field |
| Architecture | **2910's roller + servo base subsystems** | Collapses AdvantageKit's file count; the single best labor saving here |
| Pathing | **PathPlanner** | Tracks current 2027 alpha; ChoreoLib doesn't; on-the-fly pathfinding; students can edit autos |
| Physics sim | **maple-sim for off-season practice only** | No release since Jan 2026, no 2027 build — don't make it load-bearing |
| Vision | **Wait until Nov 2026.** Then Systemcore built-in, else **2× Limelight 3A ($378)** | Systemcore may zero out this line item; PhotonVision's 2027 story is rough today |
| Characterization | **SysId** on drivetrain + every arm/elevator | ~20 min of robot time replaces days of guessing |
| CI | **GitHub Actions**: build + test + spotlessCheck | Free, ~40 lines, copy 1678's |
| Formatting | **Spotless** + googleJavaFormat | Ends formatting arguments permanently |
| Testing | **Smoke test on day one.** Then 1678's `tick()` helper. | Best effort-to-value ratio in this document |
| Pit readiness | **Verify `./gradlew deploy --offline` before every event** | Cheapest possible insurance against venue Wi-Fi |
| Post-match | **Named student, 5 min, every match** | How a small team looks like a big one |
| Knowledge | **Team wiki + two people per subsystem** | Bus factor is a bigger threat than any library choice |

### Off-season calendar, Aug 2026 → Jan 9 2027

| When | Do |
|---|---|
| **Sept** | Install WPILib 2027 alpha. Build a skeleton project. Get it to compile and simulate. Set up the GitHub repo, Spotless, and CI. Read the four repos in §10's reading order. |
| **Oct** | Swerve project in sim, driving with a real controller. Write the smoke test and `tick()` helper. Build the HIL plank. Buy an XRP. |
| **Nov** | **Re-check the vendor compatibility table** (AdvantageKit templates? ChoreoLib? maple-sim? PhotonVision?). **Re-check Systemcore pricing, availability, and built-in vision — then place vision/electronics orders.** Audit your parts bin for now-unsupported sensors. |
| **Dec** | Build the reusable base subsystems (roller + servo + `MotorIO` + sim). Build one mechanism end-to-end with SysId routine and unit test. Onboard first-years through the week 1–8 path. Port Shuffleboard layouts to Elastic. Practice log replay until boring. **Mid-Dec: make the swerve decision.** |
| **Early Jan** | Verify offline builds on every laptop. Tag a known-good baseline. |
| **Jan 9** | Fill in constants. Everyone else starts writing architecture. |

---

## Sources

**WPILib official**
[New for 2026](https://docs.wpilib.org/en/stable/docs/yearly-overview/yearly-changelog.html) · [New for 2027](https://docs.wpilib.org/en/latest/docs/yearly-overview/yearly-changelog.html) · [Removed features for 2027](https://docs.wpilib.org/en/2027/docs/yearly-overview/removed-features.html) · [2027 docs root](https://docs.wpilib.org/en/2027/) · [2027 command-based](https://docs.wpilib.org/en/2027/docs/software/commandbased/index.html) · [Commands v3 design doc](https://github.com/wpilibsuite/allwpilib/blob/main/design-docs/commands-v3.md) · [Commands v3 Javadoc](https://github.wpilib.org/allwpilib/docs/2027/java/org/wpilib/command3/Command.html) · [Systemcore introduction](https://docs.wpilib.org/en/latest/docs/software/systemcore-info/systemcore-introduction.html) · [Command-based](https://docs.wpilib.org/en/stable/docs/software/commandbased/index.html) · [Simulation GUI](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/simulation-gui.html) · [Physics sim](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/physics-sim.html) · [Device sim](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/device-sim.html) · [Unit testing](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/unit-testing.html) · [SysId](https://docs.wpilib.org/en/stable/docs/software/advanced-controls/system-identification/index.html) · [Swerve odometry](https://docs.wpilib.org/en/stable/docs/software/kinematics-and-odometry/swerve-drive-odometry.html) · [Pose estimators](https://docs.wpilib.org/en/stable/docs/software/advanced-controls/state-space/state-space-pose-estimators.html) · [DataLogManager](https://docs.wpilib.org/en/stable/docs/software/telemetry/datalog.html) · [NetworkTables](https://docs.wpilib.org/en/stable/docs/software/networktables/index.html) · [NT publish and subscribe](https://docs.wpilib.org/en/stable/docs/software/networktables/publish-and-subscribe.html) · [StructPublisher Javadoc](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/networktables/StructPublisher.html) · [StructArrayPublisher Javadoc](https://github.wpilib.org/allwpilib/docs/release/java/edu/wpi/first/networktables/StructArrayPublisher.html) · [Epilogue](https://docs.wpilib.org/en/stable/docs/software/telemetry/robot-telemetry-with-annotations.html) · [Persistent alerts](https://docs.wpilib.org/en/stable/docs/software/telemetry/persistent-alerts.html) · [Choosing a dashboard](https://docs.wpilib.org/en/stable/docs/software/dashboards/dashboard-intro.html) · [Zero to Robot](https://docs.wpilib.org/en/stable/docs/zero-to-robot/introduction.html) · [Git getting started](https://docs.wpilib.org/en/stable/docs/software/basic-programming/git-getting-started.html) · [GradleRIO README](https://github.com/wpilibsuite/GradleRIO/blob/main/README.md)

**FIRST official**
[Introducing the Future Mobile Robot Controller](https://community.firstinspires.org/introducing-the-future-mobile-robot-controller) · [2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027) · [2026 Game Manual (PDF)](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)

**Systemcore / 2027**
[wpilibsuite/SystemcoreTesting](https://github.com/wpilibsuite/SystemcoreTesting) · [Systemcore specification PDF](https://downloads.limelightvision.io/documents/systemcore_specifications_june15_2025_alpha.pdf) · [WPILib 2027.0.0-alpha-6 release](https://github.com/wpilibsuite/allwpilib/releases/tag/v2027.0.0-alpha-6) · [FirstDriverStation-Public](https://github.com/wpilibsuite/FirstDriverStation-Public) · [systemcore-os-public](https://github.com/LimelightVision/systemcore-os-public) · [FRC3476/2027-Migrator](https://github.com/FRC3476/2027-Migrator)

**AdvantageKit / AdvantageScope**
[AdvantageKit docs](https://docs.advantagekit.org/) · [Installation (2027 template statement)](https://docs.advantagekit.org/getting-started/installation/) · [Template projects](https://docs.advantagekit.org/getting-started/template-projects/) · [What's New 2026](https://docs.advantagekit.org/whats-new/) · [Log replay comparison](https://docs.advantagekit.org/theory/log-replay-comparison/) · [IO interfaces](https://docs.advantagekit.org/data-flow/recording-inputs/io-interfaces/) · [Non-deterministic data sources](https://docs.advantagekit.org/getting-started/common-issues/non-deterministic-data-sources/) · [AdvantageScope docs](https://docs.advantagescope.org/) · [AdvantageScope What's New 2026](https://docs.advantagescope.org/whats-new/) · [AdvantageScope XR](https://docs.advantagescope.org/tab-reference/3d-field/advantagescope-xr/) · [6328 software page](https://www.littletonrobotics.org/software/) · [Project Idun README](https://github.com/Mechanical-Advantage/RobotCode2026Public/blob/main/idun/README.md)

**Swerve / pathing / vision / sim**
[YAGSL docs](https://docs.yagsl.com/) · [YAGSL 2027 beta thread](https://www.chiefdelphi.com/t/beta-yagsl-2026-8-18-the-2027-systemcore-era-beta/523434) · [CTRE Tuner X Swerve Generator](https://v6.docs.ctr-electronics.com/en/stable/docs/tuner/tuner-swerve/index.html) · [Phoenix 6 Swerve overview](https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/mechanisms/swerve/swerve-overview.html) · [Phoenix 6 Swerve builder API (odometry rates)](https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/mechanisms/swerve/swerve-builder-api.html) · [Phoenix 6 signal logging](https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/api-usage/signal-logging.html) · [PathPlanner docs](https://pathplanner.dev/) · [PathPlanner pathfinding](https://pathplanner.dev/pplib-pathfinding.html) · [Choreo interop](https://pathplanner.dev/pplib-choreo-interop.html) · [Choreo repo](https://github.com/SleipnirGroup/Choreo) · [PhotonVision hardware setups](https://docs.photonvision.org/en/latest/docs/quick-start/common-setups.html) · [PhotonPoseEstimator](https://docs.photonvision.org/en/latest/docs/programming/photonlib/robot-pose-estimator.html) · [PhotonVision calibration](https://docs.photonvision.org/en/latest/docs/calibration/calibration.html) · [PhotonVision simulation](https://docs.photonvision.org/en/latest/docs/simulation/index.html) · [PhotonVision prerelease install](https://docs.photonvision.org/en/latest/docs/advanced-installation/prerelease-software.html) · [YETI wiki: PhotonVision 2027](https://wiki.yetirobotics.org/books/robot-software/page/current-solution-for-photonvision-2027) · [Limelight MegaTag2](https://docs.limelightvision.io/docs/docs-limelight/pipeline-apriltag/apriltag-robot-localization-megatag2) · [Limelight store](https://limelightvision.io/collections/products) · [maple-sim](https://shenzhen-robotics-alliance.github.io/maple-sim/) · [DogLog](https://doglog.dev)

**Chief Delphi**
[6328 2026 build thread — Project Idun (post 616)](https://www.chiefdelphi.com/t/frc-6328-mechanical-advantage-2026-build-thread/509595/616) · [Commands V3 — imperative function bodies with coroutines](https://www.chiefdelphi.com/t/wpilib-commands-v3-imperative-function-bodies-with-coroutines/500699) · [Commands v3 Championship Conference](https://www.chiefdelphi.com/t/wpilib-commands-v3-championship-conference/519702) · [Choreo vs PathPlanner](https://www.chiefdelphi.com/t/choreo-vs-pathplanner/467373) · [PathPlanner v. Choreo](https://www.chiefdelphi.com/t/pathplanner-v-choreo/484118) · [Introducing BLine](https://www.chiefdelphi.com/t/introducing-bline-a-new-rapid-polyline-autonomous-path-planning-suite/509778) · [YAGSL vs CTRE Swerve Generator](https://www.chiefdelphi.com/t/swerve-yagsl-yet-another-generic-swerve-library-verses-ctre-swerve-project-generator/477634)

**Retail**
[AndyMark Arducam OV9281 (am-5749)](https://andymark.com/products/arducam-camera) · [SparkFun XRP Kit](https://www.sparkfun.com/experiential-robotics-platform-xrp-kit.html)

---

## Appendix: what changed in this revision, and what to re-verify

**Corrections made against the previous draft** (both were materially wrong and would have misled a planning decision):

1. **AdvantageKit 2027 templates.** Previously stated "only the skeleton template project is currently available for 2027." The [installation docs](https://docs.advantagekit.org/getting-started/installation/) actually say **"Template projects are not currently available for the 2027 alpha versions of AdvantageKit."** None, not one. This weakens the headline swerve recommendation and §3/§4 now handle it with an explicit fallback and a December decision date.
2. **maple-sim project health.** Previously presented as "young but validated." Its last release of any kind is `v0.4.0-beta` from **2026-01-17** — seven months stale, no 2027 build. Demoted from "use it" to "off-season practice only, not load-bearing."

**Material added:** the Systemcore *removed hardware* table (§0) and its mechanical consequences; Commands v3 explained properly (§0); 2910's reusable base-subsystem pattern with verified code (§7); 1678's `DriveTest` as a teaching artifact (§7); Phoenix 6 odometry rates, 250 Hz CAN FD / 100 Hz CAN 2.0 (§4); NT4 publisher handles and struct publishers (§8); offline pit builds (§9); the bus-factor section (§9); PhotonVision's 2027 prerelease situation and YETI's documented workaround (§6); per-repo licenses (§10).

**Re-verify in November 2026** (set a calendar reminder):

- [ ] Vendor compatibility table at [SystemcoreTesting](https://github.com/wpilibsuite/SystemcoreTesting) — especially ChoreoLib and AdvantageKit templates
- [ ] AdvantageKit template projects for 2027 — [installation page](https://docs.advantagekit.org/getting-started/installation/)
- [ ] maple-sim — any release after `v0.4.0-beta`?
- [ ] PhotonVision — official 2027 release and vendordep?
- [ ] Systemcore price, availability, and whether built-in vision shipped as announced
- [ ] Limelight 3A stock (sold out as of 2026-08-21)
- [ ] Swerve module prices (all currently [UNVERIFIED] here)
- [ ] A 2027 GitHub Actions cross-compile container from wpilibsuite
- [ ] Whether the R701 coprocessor rule has an equivalent in the 2027 manual

*Every GitHub and documentation URL in this document was verified to resolve on 2026-08-21; repo metadata came from the GitHub API the same day; code excerpts came from shallow clones read directly. Prices are as listed on vendor pages on 2026-08-21 and will change. Anything I could not verify is tagged **[UNVERIFIED]**.*
