# Launchers & Electronics — BOM, rules, and the 2027 Systemcore transition

**Purpose:** two halves that a 15-student team must get right before it can score anything.
The launcher half is *speculative* — BIOCORE's scoring element is not public, and no launcher is
confirmed relevant. The electronics half is *not* speculative: it is the most rule-constrained
subsystem in FRC, and 2027 changes its foundation by replacing the roboRIO with **Systemcore**.
Legal-parts tables below are quoted from the actual 2026 REBUILT manual with rule numbers.

**Companion files:** `reference/bom/parts_electronics.yaml` (machine-readable SKU/price table) ·
`tools/cycle-model.py` (cycle-time / EV model — do not duplicate its math here) ·
`reference/RULE-CHURN-WATCHLIST.md` · `reference/QA-AMBIGUITY-HOTSPOTS.md` ·
`reference/team-ops/03_programming_stack.md` · `manuals/archive/frc/2026_REBUILT_GameManual.pdf`

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Quoted from the 2026 manual, or read off a live vendor product page on 2026-08-22 |
| **[H]** HISTORICAL-PATTERN | Recurs across ≥3 seasons of FRC; not stated for BIOCORE |
| **[S]** SPECULATION | Engineering inference or design judgement. Flagged as such |
| **UNVERIFIED** | Not confirmed against a live source in this pass. **Do not buy against it.** |

**Source shorthand:** `REB`=2026 REBUILT (166pp) · `REEF`=2025 REEFSCAPE · `CRES`=2024 CRESCENDO ·
`SC`=Systemcore · `WPILib`=wpilib docs · `FIRSTcom`=community.firstinspires.org.

**Pricing epoch:** all prices marked [C] were read on **2026-08-22** from the vendor's live product
page. FRC vendors reprice at kickoff (Jan) and after tariff changes. **Re-verify every price the
week of 2027-01-09 before committing budget.** [H]

> ⚠️ **2027 discontinuity.** Everything in §2–§9 below is quoted from the **2026** manual. The 2026
> manual says "roboRIO" in ~40 places (R615, R701, R703, R711–R717). All of those rule bodies must
> be rewritten for Systemcore. **Assume the rule *numbers* survive and the *text* changes** — that
> is exactly the pattern `reference/RULE-CHURN-WATCHLIST.md` documents. [S]

---

## §0 — 60-second workflow (runnable)

```bash
# Run from the repository root.

# 1. Re-read the legal motor table straight from the manual (10s)
python tools/rule-show.py 2026 R501 R504 R505 2>/dev/null \
  || grep -o "STATEMENT: R50[0-9]\*.\{0,2000\}" research/rule_inventories/2026_rules_full.txt

# 2. Legal power/pneumatics rules, verbatim
grep -o "STATEMENT: R6[0-9][0-9]\*.\{0,900\}" research/rule_inventories/2026_rules_full.txt
grep -o "STATEMENT: R8[0-9][0-9]\*.\{0,900\}" research/rule_inventories/2026_rules_full.txt

# 3. Diff 2026 electrical rules vs 2025 — tells you which ones churn
python tools/frc_diff.py 2025 2026 --prefix R6 2>/dev/null | head -40

# 4. Does a launcher pay for itself? Answer arithmetically, not by vibes.
python tools/cycle-model.py --game rebuilt --sweep

# 5. Machine-readable parts list (prices + verification status)
python -c "import yaml,sys; d=yaml.safe_load(open('reference/bom/parts_electronics.yaml')); \
print(len(d['parts']),'parts;',sum(1 for p in d['parts'] if p.get('verified')),'live-verified')"
```

Expected: step 1 prints Table 8-1 (the motor allowance table); step 4 prints a cycle-time
sensitivity sweep; step 5 prints a parts count. If step 1 prints nothing, re-extract with
`pdftotext -layout manuals/archive/frc/2026_REBUILT_GameManual.pdf`. Steps 1 and 2 and §11 read
`research/rule_inventories/2026_rules_full.txt`, which is not in the repository because FIRST's rule
text is not redistributed; `bash tools/rebuild-corpus.sh --fetch` and then
`bash tools/rebuild-corpus.sh` rebuild it locally.

---

# PART A — LAUNCHERS  *(all [S] until BIOCORE's scoring element is public)*

> **Scope warning.** BIOCORE's scoring element name, mass, size, and compliance are **not public**
> (`research/00_PREMISE_CORRECTION.md`). "Pollen", "StarterBots", and "Skill Builders" belong to the
> **FTC BIOBUZZ** game and have nothing to do with BIOCORE. Nothing below is a prediction that
> BIOCORE has a launcher. It is a *readiness* document: if kickoff reveals a projectile game, you
> have 6 hours to pick an architecture, and this is the decision table.

## §1.1 — How often does FRC actually have a launcher game? [H]

| Season | Game | Projectile? | Dominant architecture |
|---|---|---|---|
| 2026 | REBUILT | Yes (FUEL → HUB) | flywheel / turret |
| 2025 | REEFSCAPE | No (CORAL/ALGAE placement + toss) | manipulator, low-arc lob |
| 2024 | CRESCENDO | Yes (NOTE) | dual flywheel + variable pivot |
| 2023 | CHARGED UP | No | arm/intake |
| 2022 | RAPID REACT | Yes (CARGO) | flywheel + hood |
| 2020/21 | INFINITE RECHARGE | Yes (POWER CELL) | flywheel + hood + turret |
| 2019 | DEEP SPACE | No | manipulator |
| 2017 | STEAMWORKS | Yes (FUEL) | flywheel |
| 2016 | STRONGHOLD | Yes (BOULDER) | flywheel/catapult |

**Base rate: ~5-6 of the last 10 seasons had a launcher-rewarding game.** That is a coin flip, not
a certainty. Budget the launcher decision at 6 hours on kickoff day; do not pre-build one. [H]

## §1.2 — Flywheel wheel selection

The wheel is the single highest-leverage launcher choice: it sets exit velocity per RPM, shot
consistency, and how much the mechanism drifts as it wears.

| Wheel type | Typical OD | Durometer / feel | Grip | Wear | Best for |
|---|---|---|---|---|---|
| **Colson Performa** | 4in, 3in, 2in | ~80A polyurethane on nylon hub | Medium-high | **Excellent** — the reason it's the FRC default | Single-flywheel shooters, hooded shots, anything you must tune once and forget |
| **Compliant wheel** (VEX/AndyMark style) | 4in, 3in, 2in | 30A–60A soft, hollow spokes | Very high | Poor–medium; spokes take a set | Compression-hungry balls, dual flywheel, low-speed feeders |
| **Fairlane / blue nitrile roller** | 2in–4in | ~70A nitrile | High | Good | Intake rollers and feeders more than flywheels |
| **BaneBots T81 / T40** | 3.875in, 2.875in | 40A / 30A urethane | High | Medium — chunks under high slip | Cheap dual flywheel, indexers |
| **Stealth / traction wheel** | 4in | hard plastic + tread | Low–medium | Excellent | Poor flywheel choice; listed to rule out |

**Rules of thumb** [S]:
- **Compression 0.25–0.50in** on a compliant ball is the usual working band. Under-compression →
  slip, velocity scatter, and a shot that changes with ball wear. Over-compression → the flywheel
  eats energy deforming the ball and recovery time balloons.
- **Colson is the default for a 15-student team.** Compliant wheels shoot beautifully in week 1 and
  differently in week 6; Colsons shoot the same in April. Consistency beats peak performance when
  you cannot afford a re-tune between every match. [S]
- Do **not** mix wheel diameters on a shared shaft unless you intend a spin gradient.
- Wheel mass is a *feature*: it is your flywheel inertia (see §1.4). A 4in Colson is a usable
  flywheel by itself; a 4in compliant wheel is not — it needs an added inertia disc.

**Part numbers:** UNVERIFIED in this pass. AndyMark, VEX/VEXpro, WCP, and The Thrifty Bot all
stock Colson-family and compliant wheels; verify the exact SKU and bore (½in hex vs ⅜in hex vs
round) on the live product page before ordering. Bore mismatch is the #1 wasted-shipping error. [H]

## §1.3 — Single vs dual flywheel, backspin, and the hood

```
SINGLE FLYWHEEL + HOOD                 DUAL OPPOSED FLYWHEEL
                                       
   hood (fixed or variable)              (top wheel, ω1)
      ╭──────────────╮                        ●
     ╱                ╲                      ↓↓
  ● ─── ball ────────►                 ball ────────►
 wheel (ω)                                  ↑↑
                                            ●
 v_ball ≈ ½ · ω · r   (ball rolls)   (bottom wheel, ω2)
 heavy BACKSPIN (free)                v_ball ≈ ½(ω1+ω2)·r
                                      spin ∝ (ω1 − ω2)
```

| | **Single flywheel + hood** | **Dual opposed flywheels** |
|---|---|---|
| Exit velocity per RPM | ~½ wheel surface speed | ~full wheel surface speed (both wheels driving) |
| Spin | Backspin comes free from the rolling contact | Zero spin at matched RPM; **spin is commandable** via Δω |
| Parts count | Fewer — 1 motor group, 1 hood | 2 independent motor groups, 2 controllers, 2 tunings |
| Energy per shot into wheel | Higher (½ speed ⇒ needs ~2× surface speed ⇒ ~4× stored energy for same ball speed at same inertia) | Lower per wheel |
| Tuning surface | 2 knobs (RPM, hood angle) | 3+ knobs (ω1, ω2, compression) |
| **15-student verdict** [S] | **Start here.** Fewer knobs, backspin for free, one closed loop to tune. | Only if the game *needs* spin control (e.g. a bank shot or a spin-sensitive target). |

**Why backspin matters:** backspin creates a Magnus force that pushes the ball *up*, flattening the
trajectory and making range less sensitive to velocity error. It also kills bounce-out on a rim
shot — the ball grabs the far rim and drops in instead of ricocheting. Any launcher game where
"bounce-out" is a scoring failure mode rewards backspin heavily. [H, observed 2016/2017/2020/2022]

**Fixed vs variable hood:**

| | Fixed hood | Variable hood |
|---|---|---|
| Complexity | 1 sheet-metal / 3D-printed arc | Servo or motor + absolute encoder + limits + a second closed loop |
| Range strategy | **Pick one shooting spot** and drive to it every cycle | Shoot from anywhere in a zone |
| Cost | ~$0–30 | ~$60–140 (motor/servo + through-bore encoder + hardware) |
| Failure mode | You lose matches where your spot is defended | The hood jams/slips mid-event and you cannot make *any* shot |
| **15-student verdict** [S] | **Week 1: fixed hood, one spot, tuned to death.** A repeatable one-spot shooter out-scores an unreliable everywhere-shooter, and it is inspectable, debuggable, and teachable. | Week 4–6 upgrade *only if* the fixed-spot version already works and is being defended. |

The strongest small-team pattern is **"fixed hood + variable RPM"**: hold the hood angle constant,
regress RPM against distance from vision, and interpolate a lookup table. One degree of freedom,
one calibration afternoon, no mechanism to break. [S, but consistent with `reference/04_PREDICTIVE_FACTORS.md`
which finds mechanism *reliability* dominates mechanism *capability* for small teams.]

## §1.4 — Motors for flywheels, and why recovery time beats peak RPM

### The arithmetic that actually decides the design [S]

A flywheel stores `E = ½ I ω²`. A shot removes some energy `ΔE`. Because `dE = I ω dω`:

```
    Δω / ω  =  ΔE / (2 E)          ← fractional RPM droop per shot
    t_recover ≈ ΔE / P_available    ← time to put that energy back
```

Two consequences that most teams learn too late:

1. **Droop is set by the inertia you bought, not the motor.** If your flywheel stores 120 J and a
   shot transfers 15 J, droop is `15/(2·120)` = **6.25%**. A 6% RPM error on shot 2 of a 5-ball
   volley is often the difference between a made and missed shot. *Fix: add inertia (a steel or
   aluminium disc), don't add motors.*
2. **Recovery time is set by available electrical power, and power is capped by the rules, not the
   motor spec sheet.** R621 + Table 8-3 cap a motor-controller branch at a **40A breaker**. At 12V
   that is ~480 W electrical per controller, call it ~330–380 W mechanical after losses. Putting
   15 J back at 350 W is ~43 ms *in theory*; real measured recovery is 150–500 ms because the
   controller current-limits, the battery sags, and the control loop is not ideal.

### Why recovery time dominates cycle time [S]

Take a 5-shot volley. Recovery per shot of **0.8 s** costs 3.2 s of dead time inside the cycle;
**0.25 s** costs 1.0 s. Over a 135-second teleop with a 10 s cycle, that difference is worth
roughly **2 extra cycles ≈ a full scoring volley**. Feed the two candidate cycle times into
`tools/cycle-model.py --sweep` and read the point delta directly — *do not re-derive it here.*

```bash
python tools/cycle-model.py --game rebuilt --cycle 9  --sweep
python tools/cycle-model.py --game rebuilt --cycle 12 --sweep
```

**Peak RPM is almost never the constraint.** Every legal brushless motor can spin a 4in wheel far
faster than any FRC-scale shot requires. What separates a good shooter from a bad one is (a) RPM
*stability under load*, (b) recovery rate, (c) shot-to-shot repeatability. Choose the motor for
its **torque-at-speed and closed-loop quality**, not its free speed. [S]

### Legal brushless candidates for a flywheel

Specs and prices below — see §2 for the full legal list and §3 for the controller pairing.

| Motor | Free speed | Stall torque | Stall current | Price | Controller | Flywheel notes |
|---|---|---|---|---|---|---|
| **Kraken X60** (WCP-0940) | **6000 RPM** trap / **5800** FOC [C] | **7.09 Nm** trap / **9.37** FOC [C] | **366 A** trap / **483** FOC [C] | **$217.99** edu [C] | **integrated Talon FX** | 1108 W peak (1405 FOC), **413 W @ 40 A**, 87% max efficiency. Highest power density in the legal set; integrated controller = 1 device, 1 CAN node. Best-in-class closed loop. |
| **Kraken X44** (WCP-0941) | **7758 RPM** trap / **7368** FOC [C] | **4.11 Nm** trap / **5.01** FOC [C] | **279 A** trap / **329** FOC [C] | **$217.99** edu [C] | **integrated Talon FX** | 835 W peak (966 FOC). Smaller/lighter, and *higher free speed* than the X60 — genuinely good for a flywheel where you want direct drive. **Same price as the X60**, so buy the X44 only when size/weight or speed is the reason. |
| **NEO Vortex** (REV-21-1652) | **6784 RPM** [C] | **3.6 Nm** [C] | **211 A** [C] | **$90.00** [C] | SPARK Flex (docks to motor) | Best-value brushless flywheel motor. 640 W peak, integrated high-res encoder, through-hex rotor. Dockable Flex removes wiring work. |
| **NEO (v1.1)** (REV-21-1650) | **5676 RPM** [C] | **2.6 Nm** (empirical) [C] | **105 A** (empirical) [C] | **$50.00** list / **$42.50** sale [C] | SPARK MAX / SPARK Flex / Thrifty Nova | The economy option. Perfectly adequate for a flywheel — 2× NEO on one shaft is a classic, cheap, reliable shooter. |
| **Minion** (24-777378) | UNVERIFIED | **3.1 Nm** [C] (610 W peak) | UNVERIFIED | **$79.99** [C] | Talon FXS (separate) | Standalone brushless, SplineXS shaft. Cheaper than Kraken but needs a separate $119.99 controller — total cost lands *above* NEO Vortex + Flex. |

**Gear-ratio consequences** [S]. Surface speed of a 4in wheel:
`v = π · 0.1016 m · (RPM/60)`. So **4in @ 6000 RPM ≈ 31.9 m/s** surface, giving a single-flywheel
ball speed of ≈16 m/s — far more than most FRC shots need. Practical implications:

| Ratio | Effect on the shot | Effect on recovery |
|---|---|---|
| **Direct drive (1:1)** | Simplest; wheel inertia is *all* your inertia | Motor sees the wheel directly — best torque authority, fastest recovery **if** inertia is adequate |
| **Overdrive (e.g. 1:1.5 up)** | Smaller wheel reaches the same surface speed | **Worse:** reflected inertia at the motor drops as ratio², droop rises, and you lose torque authority. Avoid unless packaging forces it |
| **Reduction (e.g. 1.5:1 down)** | Bigger wheel, lower RPM | **Better recovery authority** (more motor torque at the wheel) but bigger/heavier. Often the right answer with a heavy inertia disc |

Rule of thumb: size the ratio so the flywheel runs at **60–80% of motor free speed** at the shot
setpoint. Below 50% you are wasting motor; above 90% you have no headroom to recover from droop. [S]

## §1.5 — Turrets

A turret decouples aiming from driving. It is also the single most common small-team overreach. [S]

**What a turret needs, minimum:**

| Element | Options | Notes |
|---|---|---|
| **Bearing** | Lazy-susan turntable, large thin-section bearing, or 3–6 V-groove rollers on a plate edge | Roller-on-plate is the cheapest and the most forgiving of machining error. A true thin-section bearing is $$$. |
| **Drive** | Pinion → large gear/ring, or a timing belt around the turret plate | Backlash is the enemy of aiming. A belt wrap or an anti-backlash pinion is worth the effort. |
| **Motor** | NEO 550 / Kraken X44 / BAG through a big reduction (~100:1+) | Turret needs torque and precision, not speed. |
| **Absolute position** | REV Through Bore absolute, CTRE CANcoder, or a limit switch + relative encoder homing sequence | An absolute sensor removes the home-on-boot ritual and survives brownouts. |
| **Wrap limit** | Hard stops + soft limits in code | **Mandatory.** A turret that can rotate past its wire loom will eventually shear its own harness mid-match. |
| **Slip ring** | Only if you need continuous rotation | R623 explicitly permits **COTS slip rings** as intermediate branch-circuit elements. Adds cost, adds a failure mode, and is almost never needed — a ±200° wrap limit covers every real aiming case. |

> **R623 (REB) [C]:** *"Branch circuits may include intermediate elements such as COTS connectors,
> splices, COTS flexible/rolling/sliding contacts, and COTS slip rings, as long as the entire
> electrical pathway is via appropriately gauged/rated elements."*

**15-student verdict [S]: skip the turret in weeks 1–4.** A turret costs ~8–12 lb, one motor, one
absolute encoder, a machining budget you don't have, and a whole second aiming control loop. The
same aiming accuracy is available for free by **turning the drivetrain** — especially with swerve,
and even with a good tank drive plus a vision-driven heading PID. Build the turret in the offseason
and bring it back in 2028 if the game repeats.

## §1.6 — Feeders and kickers (the part teams under-budget)

The launcher is not the hard part. **Getting exactly one ball into it at a repeatable speed and
orientation is the hard part.** [S]

| Element | Purpose | Typical implementation | Failure mode |
|---|---|---|---|
| **Intake** | Ground pickup | Compliant/BaneBots roller on a deployed arm, NEO 550 or BAG | Jams on a double-pickup |
| **Indexer / serializer** | Queue and single-file the balls | Belt or roller tunnel, 1–2 motors, beam breaks between stations | Two balls arrive at once and the shooter double-feeds |
| **Feeder / kicker** | Inject *one* ball into the flywheel nip on command | A short-burst roller (most common), a pneumatic kicker, or a stopper that retracts | Feeds before the flywheel is at setpoint ⇒ a wild shot |
| **Beam breaks** | Know where each ball is | Through-beam IR sensor pairs, one per station | False triggers from arena lighting; use modulated sensors |

**The single most valuable line of code in a shooter:**
`if (flywheel.atSetpoint() && flywheel.isStable(3, 50ms)) feeder.run();`
Gate the feeder on *stable* velocity, not on *reached* velocity. This alone converts a 50%-accuracy
shooter into an 85%-accuracy shooter and costs nothing. [S]

## §1.7 — Alternatives to the flywheel

| Architecture | How it works | Energy source | Pros | Cons | Small-team fit [S] |
|---|---|---|---|---|---|
| **Catapult / launcher arm** | A spring or surgical-tubing-loaded arm slings the element; a motor+winch cocks it | Stored elastic energy (legal: **R608-C** "storage achieved by deformation of ROBOT parts") | Enormous instantaneous power; no droop; works on non-round elements | **Fixed range** unless you build a variable stop; slow re-cock; violent, hard on the frame; hard to tune finely | Good when the target is a big, close, forgiving goal. Bad when range must vary. |
| **Pneumatic puncher** | A cylinder strikes the element directly | Compressed air (**R607/R608-A**, ≤60 psi working per **R808**) | Instant, repeatable, zero spin-up | Air is a *finite budget* — see §9. Shot count per match is limited by tank volume, not by will | Only for a **low shot count** game (≤10 shots/match) or a single endgame action |
| **Linear launcher (rack/lead-screw)** | A motor drives a carriage that accelerates the element along a rail | Motor directly | Precise, quiet, variable energy | Low power density; long stroke needed for useful speed; slow reset | Rarely competitive in FRC. Listed to rule out. |
| **Passive lob / dump** | Drive to the target and eject at low speed | Motor | Trivially reliable | Only works at contact range | **Always evaluate this first.** In REEF (2025) and CHARGED UP (2023) the low-tech ejector was competitive. |

**Decision rule [S]:** run `tools/cycle-model.py` with each architecture's realistic cycle time
*including reset*, and pick the one with the highest points/match — not the one with the highest
theoretical range. A catapult with a 4-second re-cock loses to a flywheel with a 0.3-second recovery
in almost every high-shot-count game, and wins in almost every low-shot-count one.

## §1.8 — Do not duplicate the cycle model

`tools/cycle-model.py` already answers: *given our cycle time, how many points does each strategy
produce in 150 seconds, and what does a fixed-value endgame action cost us in forgone cycles?*
It is game-agnostic (JSON/YAML season definition) and ships with a validated 2026 REBUILT example.

```bash
python tools/cycle-model.py --game rebuilt                 # baseline
python tools/cycle-model.py --game rebuilt --sweep          # cycle-time sensitivity
python tools/cycle-model.py --game biocore.json             # after kickoff
```

**Launcher decisions feed the model as a cycle time.** Do not re-derive EV in this document.

---

# PART B — ELECTRONICS & CONTROL

## §2 — The legal motor table, quoted from the 2026 manual [C]

> **R501 (REB p. 92): "Allowable motors."** Only the motors and actuators in **Table 8-1 Motor
> allowances** are permitted, in any quantity.

The rows of **Table 8-1** for the motors this document prices. The other 13 rows are brushed motors
from AndyMark, BaneBots, Playing with Fusion, REV, The Thrifty Bot, VEX, WCP and the KOP automotive
suppliers; read them in R501 in the manual, or in `2026_rules_full.txt` once §0's rebuild has run.

| Motor name (as printed) | Part numbers listed in Table 8-1 |
|---|---|
| CIM | FR801-001, M4-R0062-12, AM802-001A, 217-2000, PM25R-44F-1005, PM25R-45F-1004, PM25R-45F-1003, PMR25R-45F-1003, PMR25R-44F-1005, am-0255 |
| **CTR Electronics Minion** | **24-777378**, WCP-1691 |
| CTR Electronics/VEX Falcon 500 | 217-6515, am-6515, 19-708850, am-6515_Short |
| **REV Robotics NEO Brushless** | **REV-21-1650** (v1.0 or v1.1), REV-21-1653, am-4258, am-4258a |
| **REV Robotics NEO 550** | **REV-21-1651**, am-4259 |
| **REV Robotics NEO Vortex** | **REV-21-1652**, am-5275 |
| **West Coast Products Kraken x44** | **WCP-0941** |
| **West Coast Products Kraken x60** | **WCP-0940**, am-5274 |

Plus, per R501 [C]: fans ≤120 mm and ≤10 W continuous at 12 VDC; hard-drive motors inside a legal
COTS computing device; factory vibration/autofocus motors in COTS computing devices; **PWM COTS
rotational servos with stall current ≤4 A and mechanical output ≤8 W at 6 V**; **PWM COTS linear
servos with max stall current ≤1 A at 6 V**; motors integral to a COTS sensor (LIDAR etc.);
**1 compressor** compliant with R806; and COTS brushed motors / linear actuators / electrical
solenoid actuators / electromagnets rated for 12 V wired downstream of a **≤20 A breaker**
(24 V solenoids/electromagnets must be rated for 24 V).

**R502 — "Only 4 propulsion motors."** [C] Four motors max may be used for propulsion. This is what
makes a 4-motor swerve (one drive motor per module) legal and an 8-motor tank illegal.

**R503 — "Don't modify motors (mostly)."** [C] Permitted modifications include trimming leads and
adding connectors, modifying the output shaft/mounting to facilitate connection, and — usefully —
*"Any number of #10-32 plug screws may be removed from the Falcon 500 and the Kraken X60."*

### Market data for the motors a 2027 team would actually consider

| Motor | Free speed | Stall torque | Stall current | Peak power | Price (2026-08-22) | Verified? | Pairs with |
|---|---|---|---|---|---|---|---|
| Kraken X60 (WCP-0940) | 6000 / **5800** FOC | 7.09 / **9.37** FOC Nm | 366 / **483** FOC A | 1108 / **1405** FOC W | **$217.99** edu (MSRP $399.99) | ✓ [C] | Integrated Talon FX |
| Kraken X44 (WCP-0941) | 7758 / **7368** FOC | 4.11 / **5.01** FOC Nm | 279 / **329** FOC A | 835 / **966** FOC W | **$217.99** edu (MSRP $399.99) | ✓ [C] | Integrated Talon FX |
| Minion (24-777378) | UNVERIFIED | 3.1 Nm | UNVERIFIED | 610 W | **$79.99** | ✓ [C] | Talon FXS (+$119.99) |
| NEO Vortex (REV-21-1652) | 6784 RPM | 3.6 Nm | 211 A | 640 W | **$90.00** | ✓ [C] | SPARK Flex (+$110.00) |
| NEO v1.1 (REV-21-1650) | 5676 RPM | 2.6 Nm (emp.) | 105 A (emp.) | — | **$50.00** list / $42.50 sale | ✓ [C] | SPARK MAX (+$100) / Flex / Nova (+$90) |
| NEO 550 (REV-21-1651) | **11 000 RPM** | **0.97 Nm** | **100 A** | — | **$30.00** | ✓ [C] | SPARK MAX / Flex / Nova |
| CIM (am-0255 etc.) | UNVERIFIED | UNVERIFIED | UNVERIFIED | — | UNVERIFIED | ✗ | SPARK MAX, Talon SRX, Victor SPX |

**Free-current note [C]:** Kraken X60 draws **2 A** free, X44 **3 A**. Both are supplied at
**$217.99 educational / $399.99 MSRP** — the X44 is *not* the cheap option, it is the *compact,
faster* option. The X44 was on backorder (expected no earlier than mid-fall 2026) when checked.

**Sleeper pick [S]: the NEO 550 at $30.00 is the best value-per-dollar motor in the legal set.**
11 000 RPM free and 0.97 Nm stall makes it the obvious choice for intakes, indexers, feeders,
hood adjusters, and turrets — anywhere you need speed and precision but not raw torque. Buy several.

**Cost-per-axis reality check** [C, arithmetic on verified prices]:

| Package | Motor | Controller | **Total / axis** |
|---|---|---|---|
| NEO + Thrifty Nova | $50.00 | $90.00 | **$140.00** |
| NEO + SPARK MAX | $50.00 | $100.00 | **$150.00** |
| NEO 550 + Thrifty Nova | $30.00 | $90.00 | **$120.00** |
| NEO Vortex + SPARK Flex | $90.00 | $110.00 | **$200.00** |
| Minion + Talon FXS | $79.99 | $119.99 | **$199.98** |
| Kraken X60 or X44 (integrated) | $217.99 (edu) | $0 | **$217.99** |

**Small-team takeaway [S]:** NEO + Nova/SPARK MAX is ~30% cheaper per axis than Vortex/Minion and
~35% cheaper than Kraken. For a 15-student team, the correct move is usually **Kraken or Vortex on
the drivetrain (where power density and closed-loop quality decide matches) and NEO/NEO 550 on
everything else.** Do not buy Krakens for an indexer.

---

## §3 — Motor controllers [C]

> **R504 (REB) — "Power (most) actuators off of approved devices."** With the exception of servos,
> fans, or motors integral to sensors of COTS computing devices, **each actuator must be controlled
> by a power regulating device.** The only permitted devices are the ones listed below.

**Permitted motor controllers (R504-A), verbatim list:**

| Controller | Part number(s) from R504 | Price (2026-08-22) | Verified? |
|---|---|---|---|
| Koors40 | am-5600 | UNVERIFIED | ✗ |
| **SPARK Flex** | REV-11-2159, am-5276 | **$110.00** | ✓ [C] |
| Spark (original, PWM) | REV-11-1200, am-4260 | UNVERIFIED | ✗ |
| **SPARK MAX** | REV-11-2158, am-4261 | **$100.00** | ✓ [C] |
| **Talon FX** (integrated only) | 217-6515, 19-708850, am-6515, am-6515_Short, WCP-0940, WCP-0941 | n/a — sold as part of the motor | — |
| **Talon FXS** | 24-708883, WCP-1692 | **$119.99** | ✓ [C] |
| Talon (legacy) | CTRE_Talon, CTRE_Talon_SR, am-2195 | discontinued | — |
| Talon SRX | 217-8080, am-2854, 14-838288 | UNVERIFIED | ✗ |
| **Thrifty Nova** | TTB-0100 | **$90.00** | ✓ [C] |
| Venom (motor+controller) | BDC-10001 | UNVERIFIED | ✗ |
| Victor SP | 217-9090, am-2855, 14-868380 | UNVERIFIED | ✗ |
| Victor SPX | 217-9191, 17-868388, am-3748 | UNVERIFIED | ✗ |

**Relay modules (R504-B):** Spike H-Bridge (217-0220, SPIKE-RELAY-H); Automation Direct relays
(AD-SSR6M12-DC-200D, AD-SSRM6M25-DC-200D, AD-SSR6M40-DC-200D); **PDH switched channel
(REV-11-1850) for non-actuator CUSTOM CIRCUITS only.**
**Pneumatics controllers (R504-C):** PCM (am-2858, 217-4243), **Pneumatic Hub (REV-11-1852)**.
**Servo controllers (R504-D):** **Servo Hub (REV-11-1855)**.

### R505 — one load per controller, with exceptions [C]

> **R505 — "Don't overload controllers."** *"Unless otherwise noted, each power regulating device
> shall control 1 and only 1 electrical load."* (REB p. 95, Table 8-2)

The motor rows of **Table 8-2**:

| Load class | Motor controller | Relay module | Pneumatics controller |
|---|---|---|---|
| RedLine, BaneBots, CIM, **Minion**, **NEO**, **NEO 550**, **NEO Vortex**, Pulsar 775, Mini-CIM, RS775 Pro | **Yes — 1 per controller** | No | No |
| AndyMark 9015, VEXpro BAG | **Yes, up to 2 per controller** | No | No |
| **Falcon 500, Venom, Kraken X44, Kraken X60** | Yes — **integrated controller only** | No | No |

The rows not shown cover the remaining brushed motors and linear actuators, compressors, solenoid
valves, electric solenoids and CUSTOM CIRCUITS; read them in R505 before wiring anything pneumatic.

**Practical consequence [S]:** two NEOs on one shaft (a classic cheap dual-flywheel) needs **two**
controllers. Two BAGs can share one. Budget accordingly.

### Choosing a controller ecosystem for a 15-student team [S]

| | **CTRE (Phoenix 6)** | **REV (REVLib)** | **TTB (Nova)** |
|---|---|---|---|
| Flagship | Kraken X60/X44 (integrated), Talon FXS | NEO Vortex + SPARK Flex | Nova with NEO |
| Cost/axis | Highest | Middle | **Lowest** |
| Closed loop | Best-in-class (FOC, on-device motion magic) | Very good | Good |
| Config tooling | Phoenix Tuner X | REV Hardware Client | REV Hardware Client-adjacent |
| CAN FD | **Yes** (needs CANivore on roboRIO; **native on Systemcore** — 5× CAN-FD ports) | CAN 2.0 | CAN 2.0 |
| Risk for 2027 | Vendor libraries must be ported to Systemcore | Same | Same, smaller vendor |

**Pick one ecosystem and stay in it.** Mixing CTRE and REV on one robot doubles the vendordep
surface, doubles the firmware-update ritual, and doubles the number of things that break on the
Systemcore migration. Mixed-vendor CAN buses are a classic small-team time sink. [S]

---

## §4 — 2027 control system core: **Systemcore** replaces the roboRIO

**This is the biggest control-system change since the cRIO → roboRIO transition in 2015.** [C]

### What is confirmed [C]

| Item | Status |
|---|---|
| Systemcore is the FRC robot controller **starting in the 2027 season** | **[C]** (FIRST community posts) |
| FTC adopts Systemcore in the **2027-28** season | **[C]** |
| SoC: **Raspberry Pi CM5** — quad-core ARM Cortex-A76, **4 GB RAM**, VideoCore VII GPU, real-time Linux | **[C]** |
| I/O coprocessor: **Raspberry Pi RP2350** provides *reconfigurable* I/O (PWM, DIO, analog in) | **[C]** WPILib docs |
| Onboard **LEDs and a display** in addition to the IMU | **[C]** WPILib docs |
| **2027 FIRST Driver Station** is a new, cross-platform app: Windows / **macOS** / **Linux** (x64 and arm64). It works **only** with Systemcore; the roboRIO keeps the existing DS | **[C]** wpilib.org blog |
| DS details: **16-bit gamepad resolution** (was 8-bit), up to **64 buttons / 8 POVs**, new E-Stop reset (Esc+I), op-mode selection, **WPILib-format logs readable by AdvantageScope**, min 1280 px effective display width | **[C]** |
| **FMS (At Event) support only on Windows** and the hardware appliance | **[C]** |
| Emerson/NI **LabVIEW** support for Systemcore is being *explored*, not committed | **[C]** |
| Physical size: "approximately the size of a large smartphone" | **[C]** |
| **5× CAN-FD ports** (Weidmüller wire-to-board) | **[C]** |
| **6× SmartIO ports** (3-pin Molex-SL, flexible analog/digital in/out) | **[C]** |
| **2× I²C** (4-pin Molex-SL), **4× USB 3.0-A**, **1× USB-C device**, **1× Ethernet** | **[C]** |
| **1× Power input** (Weidmüller), **1× RSL port** (2-pin Molex-SL), **1× MotionCore bridge port** (4-pin Molex Microfit+) | **[C]** |
| **Built-in IMU** for odometry/localization | **[C]** |
| **M.2 A+E slot** compatible with the **Hailo-8 AI accelerator** | **[C]** |
| **Integrated 2.4/5 GHz WiFi radio** on the board | **[C]** |
| Limelight is building the web configuration interface: device config, on-robot hosted coding (Blockly, Java, Python), live sensor values | **[C]** |
| Pricing goal: FIRST states it is *"on target to meet the goal of offering Systemcore at a lower price than the roboRIO"*; **the exact price has not been announced** | **[C]** |
| Alpha testing: FRC from June 2025, FTC from Sept 2025, 50–100 teams per program | **[C]** |

### What this changes about how you build a robot [S]

| Change | Consequence for a small team |
|---|---|
| **5 native CAN-FD ports** | The CANivore (21-678682, ~$100+) becomes unnecessary for most teams. CAN FD bandwidth (~8× CAN 2.0 payload rate) is now free, and you can split the bus by subsystem — a shorted drivetrain wire no longer kills your elevator's CAN. **This is a genuine reliability win.** |
| **Built-in IMU** | The Pigeon 2.0 ($199.99) and navX may become optional for basic odometry. **Do not delete them from your budget until the Systemcore IMU's noise/drift specs are published.** UNVERIFIED. |
| **Integrated WiFi radio** | Unclear whether FRC will use it at events or continue to require an external VH-109. **UNVERIFIED — do not assume the radio line item disappears.** |
| **M.2 Hailo-8 slot** | On-controller neural inference. Could displace a separate coprocessor (Orange Pi / Limelight) for object detection. UNVERIFIED whether WPILib will ship a supported pipeline for 2027. |
| **Real-time Linux + CM5** | Vastly more compute than the roboRIO's dual-core ARM Cortex-A9. Vision on the controller becomes plausible. Also: a completely different deploy/debug story. |
| **SmartIO replaces DIO/AI/PWM headers** | Every sensor pigtail you own is the wrong connector. **Budget for connector adapters and rewiring.** [S] |
| **No MXP** in the confirmed port list | R713's approved-MXP-device list (navX MXP, RIOduino, Digit Board, Spartan Sensor Board, HUSKIE 2.0) is likely obsolete for 2027. UNVERIFIED. |

### What remains UNVERIFIED until the **Pre-Kickoff Virtual Kit Release, 2026-11-12**

- **Exact price.** Only "lower than roboRIO" has been stated. **UNVERIFIED.**
- **KoP distribution:** whether every team gets one free, whether it's a voucher, whether rookie vs
  veteran differ, and whether the roboRIO remains legal as a fallback in 2027. **UNVERIFIED.**
  > A second-hand claim circulates that *"every team will get a Systemcore in their 2027
  > year-specific KoP box, and teams that want an additional Systemcore will be able to purchase
  > one."* **This could not be traced to a primary FIRST source in this pass — treat it as
  > UNVERIFIED and do not budget on it.** The WPILib blog's note that *"the roboRIO … will continue
  > to use their existing Driver Station systems"* is at least consistent with the roboRIO not being
  > hard-banned, but says nothing about competition legality. [C on the quote, S on the inference]
- Whether the **external VH-109 radio is still required** given the integrated WiFi. **UNVERIFIED.**
- Whether **PWM motor controllers** (Spark, Victor SP, Talon SRX in PWM mode) remain usable, and via
  which port. SmartIO is described as analog/digital, not explicitly PWM. **UNVERIFIED.**
- **Servo** support and the R506/R712 servo rules. **UNVERIFIED.**
- Whether **PCM/PH/Servo Hub** CAN control is unchanged (likely yes — they are CAN devices). **[S]**
- Which **rule numbers** carry the Systemcore text. R701 ("Control the ROBOT with a roboRIO") is the
  obvious rename target. **[S]**

### Action plan for the 2026-27 preseason [S]

| Date | Action |
|---|---|
| **Now → Nov 2026** | Track `github.com/wpilibsuite/SystemcoreTesting` and the WPILib 2027 beta docs. Do **not** buy a roboRIO 2.0. Do **not** buy a CANivore. |
| **2026-11-12** | **Pre-Kickoff Virtual Kit Release.** Watch it live. This is when price, KoP contents, and the radio question get answered. Update `parts_electronics.yaml` the same day. |
| **Nov–Dec 2026** | Port your 2026 codebase to the WPILib 2027 beta on a bench Systemcore if you can get one. Budget **2× your normal offseason software time.** |
| **Kickoff 2027-01-09** | Re-read R7xx in the new manual **first**, before any mechanical decision. The control-system rules will have moved. |

> **Budget guidance [S]:** hold **$300–500 unallocated** for control-system surprises in 2027.
> A platform transition year always produces one part you did not know you needed. In 2015
> (cRIO→roboRIO) it was the PDP and VRM; in 2025 it was the VH-109 radio swap.

---

## §5 — Power distribution, breakers, wire, battery [C]

### The main power path — R609, verbatim [C]

> **R609 — "Connect main power safely."** The following devices shall be connected with **6 AWG
> (7 SWG or 16 mm²) copper wire or larger**: (A) 1 ROBOT battery; (B) a single pair of **Anderson
> Power Products (APP) 2-pole SB type connectors**; (C) a single main **120 A surface mount circuit
> breaker** (Cooper Bussman CB185-120, CB185F-120, CB285-120, CB285F-120, CB285120F **or** Optifuse
> 153120, 253120); (D) a single main power distribution device (PD).

**Legal PDs (R609-D)** [C]:

| PD | Part numbers | Price (2026-08-22) | Verified? | Notes |
|---|---|---|---|---|
| CTRE **PDP** (1.0) | am-2856, 217-4244, 14-806880 | **DISCONTINUED** — "no longer available for purchase"; CTRE points to PDP 2.0 | ✓ status [C] | Legacy; screw terminals; has shared VRM/PCM 20 A pairs (see R617) |
| CTRE **PDP 2.0** | 24-806880, WCP-1690 | UNVERIFIED | ✗ | Newer CTRE option |
| REV **PDH** | **REV-11-1850** | **$250.00** | ✓ [C] | 20× 40 A channels + 3× low-current (15 A cont / 20 A peak) + 1 switchable; **toolless WAGO terminals**; CAN + USB-C telemetry; 517 g |
| AndyMark **AMPD** | am-5754 | UNVERIFIED | ✗ | |

**PDH vs PDP for a 15-student team [S]:** the PDH's **toolless WAGO levers** are worth the premium.
A screw-terminal PDP requires a screwdriver and a torque habit; every loose screw terminal is a
brownout waiting to happen, and brownouts are the #1 self-inflicted match loss for small teams.
The PDH's per-channel LEDs and live telemetry also make debugging teachable to a rookie.

### Breakers and fuses — R619/R620/R621 [C]

**Legal PD breakers (R619):** Snap Action **VB3-A** or **AT2-A** (terminal style F57) ≤40 A;
Snap Action **MX5-A / MX5-L** ≤40 A; **REV ATO auto-resetting** ≤40 A; **CTRE ATO auto-resetting**
≤40 A; any **ATM** breaker ≤ the fuse values permitted by R620.

**Legal PD fuses (R620):** PDP → **ATM** matching the printed value; all PDs → **ATC/ATO ≤10 A**;
PDH → **ATM ≤15 A**, *except* a single **20 A** fuse for powering a PCM or PH.

**Branch protection (R621, Table 8-3):**

| Branch circuit | Breaker/fuse | Qty per breaker |
|---|---|---|
| Motor controller | up to 40 A | **1** |
| CUSTOM CIRCUIT | up to 40 A | no limit |
| Automation Direct relay 40 A (*6M40*) | up to 40 A | 1 |
| Fans per R501 (not part of a COTS computer) | up to 20 A | no limit |
| Spike relay module | up to 20 A | 1 |
| Automation Direct relay 25 A (*6M25*) | up to 20 A | 1 |
| **PCM/PH with compressor** | up to 20 A | 1 |
| Servo Power Module / Servo Hub | (see manual) | — |

### Wire sizing — R622, Table 8-4 [C]

| Application | Minimum wire size |
|---|---|
| 31–40 A breaker circuit | **12 AWG** (13 SWG / 4 mm²) |
| 21–30 A breaker circuit | **14 AWG** (16 SWG / 2.5 mm²) |
| 6–20 A breaker circuit; 11–20 A fuse circuit; PDP↔VRM/RPM/PCM/PH dedicated terminals; compressor outputs from PCM/PH | **18 AWG** (19 SWG / 1 mm²) |
| Motor power adapter board circuit; ≤5 A breaker; ≤10 A fuse; VRM 2 A circuits; ≤2 A fuse | **22 AWG** (22 SWG / 0.5 mm²) |
| **VH-109 passthrough per R626** | Cat5e/6/7/8, **2 pairs total** (1 pair V+, 1 pair GND) |
| roboRIO PWM port outputs; ≤1 A fuse | **24 AWG** (24 SWG / 0.25 mm²) |

**Wire colours — R624 [C]:** positive = **red, yellow, white, brown, or black-with-stripe**;
negative/common = **black or blue**. Exceptions: factory leads on legal devices (and same-colour
extensions), and Ethernet used for PoE.

### Battery and charging [C]

> **R601 — "Battery limit — everyone has the same power."** Exactly **1** non-spillable sealed
> lead-acid (SLA) battery: **12 V nominal**; **17.0–18.2 Ah** at the 20-hour rate; **rectangular**;
> nominal **7.1 × 3.0 × 6.6 in ±0.1 in** (18.03 × 7.62 × 16.76 cm ±0.25 cm); **11.0–14.5 lb**
> (4.99–6.57 kg); **nut-and-bolt terminals**; vents unobstructed during charging.

**The standard legal battery: MK Battery ES17-12.** [C]

| Vendor listing | P/N | Price | Per battery | Verified? |
|---|---|---|---|---|
| AndyMark — *MK ES17-12 12V SLA Battery (Set of 2)* | ES17-12 | **$116.00** / 2-pack | **$58.00** | ✓ [C] |
| REV Robotics — *MK Battery ES17-12 · 2 Pack* | REV-19-2487-PK2 | **$120.00** / 2-pack | **$60.00** | ✓ [C] |

Specs (AndyMark listing) [C]: 12 V, **18 Ah**, **7.13 × 2.99 × 6.57 in**, **12.89 lb**, nut-and-bolt
terminals, SLA/AGM. Cycle life 200 (full discharge) / 500 (50%) / 1000 (30%); useful competition
life 1–2 years. **Every R601 clause passes**: 18 Ah is inside 17.0–18.2 Ah; dimensions are inside
7.1 × 3.0 × 6.6 ±0.1 in; 12.89 lb is inside 11.0–14.5 lb; terminals are nut-and-bolt.

**Main power path parts, live-verified [C]:**

| Item | P/N | Price | Verified? | Notes |
|---|---|---|---|---|
| Anderson **SB50** connector + 2× 6 AWG contacts | — (AndyMark) | **$6.60** | ✓ | Buy one per battery *plus* one robot-side; 0.2 lb |
| **120 A surface-mount breaker**, Eaton Bussmann | **CB285-120** (AndyMark alt: am-0282, ¼-28 thread) | **UNVERIFIED — page showed SOLD OUT on 2026-08-22** | status ✓ | 120 A, 48 VDC, 2.9 × 1.9 × 1.5 in, manual reset, M6 thread, 0.24 lb. **Lead-time risk — order early.** |
| **Robot Signal Light** | **am-3583** | **$70.00** | ✓ | 3.23 in tall, 0.109 lb, two spade connectors, no polarity. Larger housing than the Allen-Bradley alternative |
| Charger — NOCO **GEN5X3** (3-bank, 15 A total) | GEN5X3 | UNVERIFIED | ✗ | 3 banks × 5 A keeps each bank under R604's 6 A cap — **verify per-bank current yourself**, and R603 still requires an Anderson SB connector on the charger |

> **R603 — "Charge batteries with safe connectors."** Any charger used on a ROBOT battery must have
> the corresponding **Anderson SB connector** installed. [C]
> **R604 — "Charge batteries at a safe rate."** A charger may not be used such that it exceeds
> **6 A average charge current**. [C]

> **R602 — "Other batteries for cameras or computers only."** COTS USB battery packs **≤100 Wh**
> (27000 mAh at 3.7 V) with **5 V/5 A** or **12 V/5 A** max output per port via USB-PD, or batteries
> integral to a COTS computing device / self-contained camera, may power COTS computing devices and
> their peripherals — provided they are securely fastened, connected only with unmodified COTS
> cables, and charged per manufacturer recommendations. [C]
> **R605 — "Batteries are not ballast."** No other batteries at all, powered or not. [C]

**Battery practice that actually wins matches [S]:**
- **6 batteries minimum** for a 12-match event: 1 in the robot, 1 on the charger, 4 resting. A
  battery needs ~30 min of rest after charge before its resting voltage is meaningful.
- **Log every battery.** Number them, log load-tested internal resistance, retire anything above
  ~18 mΩ. A tired battery is indistinguishable from a code bug from the driver's seat.
- **Never** run a battery two matches in a row. This is the cheapest reliability upgrade in FRC.
- Anderson **SB50** is the standard robot-side connector. Buy the crimp lugs and a real hex crimper;
  a bad SB50 crimp causes intermittent brownouts that will consume a whole regional.

### Other power rules worth memorising [C]

- **R610** — every circuit must be sourced from a **single protected connector pair** of the PD; no
  circuit may connect to the PD's main power input (exceptions: R615, R617).
- **R611** — **the ROBOT frame is not a wire.** All wiring must be electrically isolated from the
  frame. Frame-ground is an instant inspection failure.
- **R612** — the 120 A breaker must be **quickly and safely accessible from the exterior**; it is
  the only 120 A breaker allowed.
- **R613** — the PD, wiring, and all breakers must be **visible for inspection**. Design your
  electronics board to be seen, not buried.
- **R614** — CUSTOM CIRCUITS must not produce measurable voltages **>24 V** (exception: COTS PoE
  injectors used with COTS Ethernet cable and COTS receiving devices).
- **R615** — roboRIO power input connects **directly** to a **non-switched protected output pair**
  with a **10 A** fuse/breaker; **no other load** on that circuit. *(Systemcore analogue UNVERIFIED.)*
- **R618** — **only 1 wire per PD terminal.**
- **R625** — CUSTOM CIRCUITS must not alter the power pathway between battery, PD, controllers,
  relays, motors, or control-system items. High-impedance voltage / low-impedance current monitoring
  is allowed if its effect is inconsequential.
- **R709** — **1–2 Robot Signal Lights** (855PB-B12ME522 and/or **am-3583**), visible from 36 in
  away from at least one side, connected to the RSL terminals. If using the 855PB, jumper "La"–"Lb"
  for solid operation. *(Systemcore has a dedicated 2-pin Molex-SL RSL port.)* [C]

---

## §6 — The radio [C]

> **R702 (REB p. 104): "Communicate with the ROBOT with the specified radio."** One **Vivid Hosting**
> wireless bridge (**P/N: VH-109, WCP-1538**), configured with the team's encryption key at each event,
> *"is the only permitted device for communicating to and from the ROBOT during the MATCH."* **Events
> held in China are the exception** and use an **OpenMesh (P/N: OM5P-AN or OM5P-AC)** radio.

**Verdict: the VH-109 is the required radio; legacy OpenMesh is legal only at China events.** [C]
This resolves the question in the task brief definitively from the 2026 manual text.

| Fact | Detail | Label |
|---|---|---|
| Required radio | **Vivid-Hosting VH-109** (WCP-1538) | [C] R702 |
| Radio tech | Wi-Fi 6E (802.11ax), ruggedised, configurable PoE outputs | [C] frc-radio.vivid-hosting.net |
| Firmware floor | ≥ **1.3.0** was required for 2025 events; 2025 KoP units shipped with 1.1.2 and needed upgrading | [C] |
| **2027 firmware requirement** | **UNVERIFIED** — check the 2027 manual and Vivid-Hosting docs at kickoff | UNVERIFIED |
| Price | **UNVERIFIED** — not published on the Vivid-Hosting docs site; check AndyMark / WCP / FIRST Choice | UNVERIFIED |
| Bandwidth cap | **7.0 Mbit/s** for VH-109 (4.0 Mbit/s for OpenMesh) | [C] R704 |
| Mounting | **R708** — must be mounted so the diagnostic lights are visible to FIELD STAFF | [C] |
| Powering | **R616-A** — inject into the **"RIO" port** with a passive injector or modified Ethernet cable connected directly to a PD, **and/or** wire directly to the radio's **12 V input**. **R617** — that supply must be on a non-switched protected pair with a **10 A** fuse/breaker, no other load | [C] |
| PoE passthrough | **R626** — VH-109 PoE output may power **one COTS device ≤2 A at 12 V**, over standard Cat5e/6/7/8, with the VH-109 itself powered via its **12 V input using ≥18 AWG** | [C] |
| roboRIO connection | **R703** — v1.5 radios: RIO port directly / pigtail / passive PoE adapter. v1.0 radios: RIO port **via** passive PoE injector or an Ethernet cable with the appropriate wires removed, **or** AUX 1 / AUX 2 with the DIP switch off | [C] |

**2027 open question [S]:** Systemcore has an **integrated 2.4/5 GHz WiFi radio**. Whether FRC
retires the external VH-109, keeps it, or uses the internal radio only for tethered configuration is
**UNVERIFIED** and is one of the highest-value things to learn on **2026-11-12**.

**Open FMS ports (R704, Table 8-5)** [C]: UDP/TCP **1180–1190** (camera from RIO to dashboard over
USB), TCP **1735** (SmartDashboard), UDP **1130** (DS→robot), UDP **1140** (robot→DS), HTTP **80**
and **443** (camera via on-robot switch), UDP/TCP **554** (RTSP h.264), UDP/TCP **1250** (CTRE).
Anything else is blocked at the field — a classic "it worked in the pit" failure. [H]

**R707 — "Limited wireless allowed."** Only R702/R706 comms, event-provided location tags, and
**RFID/NFC used exclusively within the ROBOT**. No Bluetooth telemetry, no ESP32 side-channel. [C]

---

## §7 — Sensors

| Sensor | Part number | Price (2026-08-22) | Verified? | Interface | Use |
|---|---|---|---|---|---|
| **REV Through Bore Encoder V1** | REV-11-1271 | **$40.80** (was $48.00) — **listed DISCONTINUED, in stock** | ✓ [C] | Quadrature (2048 CPR / 8192 counts) **+ absolute PWM**; JST-PH 6-pin; ≤10 000 RPM; 3.3–5 V | Arm/hood/turret absolute position. **Discontinued — do not design a 2027 robot around this SKU.** Check REV for a successor. |
| **CTRE CANcoder** | 22-676768 | **$89.99** | ✓ [C] | **CAN FD / CAN 2.0**, 6–16 V, <50 mA | Swerve module absolute azimuth; anything where you want absolute position on the CAN bus with no DIO port |
| **CTRE Pigeon 2.0 IMU** | 21-737785 | **$199.99** | ✓ [C] | CAN | 9-DOF AHRS, Kalman fusion, no boot calibration, ~0.12 °/hr yaw drift. **Systemcore has a built-in IMU — reassess this line item after 2026-11-12.** |
| **Kauai Labs navX2** (MXP or micro) | UNVERIFIED | UNVERIFIED | ✗ | MXP / I²C / USB | Alternative IMU. **R713 lists navX MXP and navX2 MXP as approved active MXP devices** — but **Systemcore has no MXP in its confirmed port list**, so the MXP variant is at risk for 2027. Prefer the USB/I²C variant if you buy one. [S] |
| **CTRE CANrange** (ToF) | 24-827871 | **$64.99** | ✓ [C] | CAN | Time-of-flight proximity, 1 mm resolution, up to 100 cm (short) / 300 cm (long) / 100 cm @100 Hz (high-speed). Game-piece detection, wall standoff, hood range |
| **Beam break** (through-beam IR pair) | UNVERIFIED | ~$10–25/pair UNVERIFIED | ✗ | DIO (Systemcore: SmartIO) | **The highest value-per-dollar sensor in FRC.** Two per indexer station tells you exactly how many game pieces you hold and where |
| **Limit switch** | UNVERIFIED | ~$2–8 | ✗ | DIO / SmartIO or controller data port | Homing and hard-stop protection. Wire **normally-closed** so a broken wire reads "at limit" and fails safe [S] |
| **Analog pressure sensor** | REV-11-1107 | UNVERIFIED | ✗ | Analog in (or PH analog port) | Required-or-alternative pneumatic pressure sensing per **R805-C / R812-B** |

**Sensor strategy for a 15-student team [S]:**
1. **Beam breaks first.** Knowing where your game pieces are eliminates 80% of "why did it do that?"
   debugging, costs almost nothing, and is a great rookie wiring project.
2. **Absolute encoders on every arm/pivot.** A relative encoder means a homing sequence, and a
   homing sequence means a match where you forgot to home. CANcoder or through-bore absolute.
3. **One IMU, on CAN.** Pending Systemcore's built-in IMU spec.
4. **Skip everything else** until a specific failure demands it. Sensors you do not read are weight,
   CAN traffic, and a wire that can come loose.

**CAN bus rules [C]:** **R714** — every CAN motor controller must get enable/disable from the
roboRIO via **either** PWM (per R713) **or** CAN, **never both simultaneously on the same device.**
**R715** — PCM, PH, and Servo Hub must be controlled over CAN from the built-in roboRIO CAN.
**R716** — nothing may interfere with, alter, or block CAN comms. **R717** — a **CTRE CANivore**
(21-678682, WCP-1522) USB-to-CAN adapter may add CAN buses. *(Systemcore's 5 native CAN-FD ports
likely make the CANivore redundant — do not buy one for 2027. [S])*

---

## §8 — Vision

| Option | Cost (2026-08-22) | Verified? | Setup effort | What you get | Small-team fit |
|---|---|---|---|---|---|
| **Limelight 4** | **$449.00** | ✓ [C] | **Lowest** — power + Ethernet + web UI | Integrated camera, compute, LEDs, IMU; AprilTag pose, retroreflective/colour pipelines; optional **Hailo-8 upgrade kit from $95.00** [C] for neural detection | **Best if you can afford exactly one vision device.** The setup time you save is worth more than the price delta to a 15-student team |
| **Limelight 3G** | **$400.00** (sold out at time of check) | ✓ [C] | Lowest | Global shutter — **much** better AprilTag pose at speed | The global shutter is the single biggest accuracy factor for pose estimation while moving [S] |
| **Limelight 3** | **$400.00** | ✓ [C] | Lowest | Rolling shutter predecessor | Buy 3G or 4 instead if available |
| **Limelight 3A** | **$189.00** | ✓ [C] | Low | Compute module without the integrated enclosure/optics of the full LL3 — you supply a USB camera | **The value pick.** LL3A + a good global-shutter USB camera ≈ LL3G capability at roughly half the cost |
| **PhotonVision on Orange Pi 5 / Raspberry Pi 5** | UNVERIFIED (~$80–150 SBC + ~$40–90 camera + PoE/power) | ✗ | **Highest** — flash image, network config, camera calibration, thermal management, and you own every failure | Open-source, excellent AprilTag pipeline, full control, cheap to add a *second* camera | Only if you have a software student who *wants* this. It is a genuine multi-weekend project. |
| **USB camera on the controller** (driver view only) | ~$20–40 UNVERIFIED | ✗ | Trivial | Driver situational awareness, no pose estimation | Always worth having. Note the R704 bandwidth cap: **7.0 Mbit/s total** — a full-rate MJPEG stream will eat it and drop your control packets. Stream at low resolution and low FPS. [C/S] |

**The honest tradeoff [S].** A Limelight is not better *technology* than PhotonVision on an Orange
Pi — it is better *time*. For 15 students, vision cost should be measured in student-hours, not
dollars. A $449 Limelight that works on day 3 beats a $200 Orange Pi setup that works on day 30 and
breaks at the regional because nobody remembers the static IP. Buy the Limelight **if and only if**
the game rewards ranged/aligned scoring; if it does not, spend the $449 on a sixth battery, spare
motors, and practice field material.

**Global shutter matters more than resolution.** A rolling-shutter camera skews the AprilTag while
the robot rotates, injecting pose error exactly when you need pose most. If you are choosing between
"higher resolution" and "global shutter," choose global shutter every time. [S]

**2027 note:** Systemcore's CM5 + optional **Hailo-8 M.2** may make on-controller vision viable
without any coprocessor. Whether WPILib ships a supported pipeline for this in 2027 is
**UNVERIFIED**. Do not plan around it until the Nov 12 kit release. [S]

---

## §9 — Pneumatics

### The rules, with numbers [C]

| Rule | Requirement |
|---|---|
| **R801** | *"no pneumatic parts other than those explicitly permitted in this section shall be used"* |
| **R802** | All pneumatic items must be **COTS** and either (A) rated **≥125.0 psi** (861.8 kPa / 8.618 Bar), or (B) installed **downstream of the primary relieving regulator** and rated **≥70.0 psi** (482.6 kPa / 4.826 Bar) |
| **R803** | No modification. Exceptions: tubing may be **cut**; device wiring may be modified to interface with the control system; assembly using pre-existing threads/brackets/quick-connects; the mounting pin may be removed from a cylinder; labelling |
| **R804** | Permitted items: vent plug valves; relief valves; **solenoid valves with max ⅛ in NPT/BSPP/BSPT port or integrated ¼ in OD quick-connect**; tubing **max ¼ in OD**; pressure transducers, gauges, passive needle valves, manifolds, fittings (incl. COTS U-tubes); check and quick-exhaust valves (subject to R813) |
| **R805** | **If you use pneumatics at all, these are mandatory:** (A) 1 legal compressor; (B) a pressure relief valve calibrated per R811; (C) a **Nason SM-2B-115R/443** pressure switch **and/or** a **REV-11-1107** analog pressure sensor wired per R812; (D) ≥1 pressure vent plug; (E) **stored** and **working** pressure gauges; (F) **1 primary working pressure regulator** |
| **R806** | Compressed air on the ROBOT must come from **its 1 onboard compressor only**; compressor spec must not exceed nominal **1.1 cfm (519.1 cm³/s) @ 12 VDC** at any pressure |
| **R807** | **Stored** pressure ≤ **120.0 psi** (~827 kPa / 8.2 Bar). No off-board stored air |
| **R808** | **Working** pressure ≤ **60.0 psi** (413.7 kPa / 4.137 Bar), through a **single primary adjustable relieving regulator**. Additional regulators may be downstream |
| **R809** | Only compressor, relief valve, pressure switch, vent plug, gauge, storage tanks, tubing, transducers, filters, and fittings upstream of the regulator |
| **R810** | Gauges must be **easily visible**, upstream and downstream of the regulator, in psi/kPa/Bar |
| **R811** | Relief valve attached **directly to the compressor** or by legal hard fittings to its output; teams **must check/adjust it to release at 125.0 psi** — *"The valve may or may not have been calibrated prior to being supplied to teams"* |
| **R812** | Pressure switch on the **high-pressure side**; Nason wired directly to the PCM/PH pressure-switch input (or to the roboRIO if using a relay, with code enforcing the limit); REV-11-1107 analog output to **analog input 0** |
| **R813** | Vent plug must vent to atmosphere when manually operated and be **visible and easily accessible** |
| **R814** | **Output air from multiple solenoid valves must not be combined** |
| **R608-A** | Stored compressed air is a permitted non-electrical energy source at match start, if charged per R806/R807 |

> **These rules apply at all times while at the event, not just on the field.** (Preamble to §8.8.)

### The pneumatics shopping list [C for prices marked ✓]

| Item | Part number | Price (2026-08-22) | Verified? |
|---|---|---|---|
| **REV Pneumatic Hub (PH)** | **REV-11-1852** | **$90.00** | ✓ [C] — 16 solenoid channels (16 single-acting / 8 double-acting), user-selectable **12 V or 24 V** regulated output, 200 mA/channel, **15 A** compressor output, 1 digital pressure-switch input + 2 analog sensor inputs, CAN + USB-C, 74 g |
| CTRE PCM (alternative) | am-2858, 217-4243 | UNVERIFIED | ✗ |
| Compressor (≤1.1 cfm @ 12 VDC) | UNVERIFIED (e.g. VIAIR-class KOP compressor) | UNVERIFIED | ✗ |
| Analog pressure sensor | REV-11-1107 | UNVERIFIED | ✗ |
| Nason pressure switch | SM-2B-115R/443 | UNVERIFIED | ✗ |
| Relief valve, regulator, gauges ×2, vent plug | UNVERIFIED | UNVERIFIED | ✗ |
| Solenoid valves (≤⅛ in port or ¼ in QC) | UNVERIFIED | UNVERIFIED | ✗ |
| Cylinders (bore/stroke to suit) | UNVERIFIED | UNVERIFIED | ✗ |
| Tubing ¼ in OD, fittings | UNVERIFIED | UNVERIFIED | ✗ |
| Storage tanks (optional) | UNVERIFIED | UNVERIFIED | ✗ |

**Realistic all-in cost of a first pneumatic system: $250–450 UNVERIFIED**, plus ~4–7 lb, plus the
compressor's continuous electrical draw during a match.

### Is pneumatics worth it in 2026–27? — verdict [S]

**Default answer: NO for a 15-student team, with three specific exceptions.**

**Why not:**
1. **R805 makes it all-or-nothing.** You cannot buy "one cylinder." The moment you use any pneumatic
   component you owe the inspector a compressor, relief valve, pressure switch/sensor, vent plug,
   **two** gauges, and a primary regulator. That is a fixed ~$250–450 and ~4–7 lb entry fee.
2. **Air is a finite budget.** With ≤120 psi stored (R807) and ≤60 psi working (R808), your shot/
   actuation count per match is bounded by tank volume, and the 1.1 cfm compressor cap (R806) means
   you cannot refill fast under load. Teams routinely run out of air in the last 30 seconds.
3. **The compressor competes with your drivetrain for battery.** It runs a 15 A load at the worst
   possible moments.
4. **Modern brushless motors ate pneumatics' lunch.** A NEO 550 ($UNVERIFIED) or a NEO ($50) with a
   cheap gearbox does most "extend/retract" jobs with *position control*, *current limiting*, and
   *no plumbing*. In 2015 pneumatics was the only cheap fast linear actuator. In 2026 it is not.
5. **Weight.** 4–7 lb of pneumatics is a shooter hood, a climber hook, or a fifth battery's worth of
   ballast you could have spent elsewhere.
6. **Rule surface.** R801–R814 is 14 rules and an inspection checklist. That is real student time.

**The three exceptions where pneumatics still wins [S]:**
- **Very high force, very short stroke, binary state** — e.g. a latching climber hook or a brake.
  A cylinder holds force at zero current; a motor holding force draws current and heats up.
- **You need genuinely instantaneous actuation** — sub-100 ms deploy, e.g. an intake that must drop
  faster than a motor can accelerate it.
- **You already own a complete, inspected, working pneumatic kit** and the marginal cost is one
  cylinder and two fittings.

**If you do use pneumatics:** use the **REV PH** over the PCM (CAN + USB-C bench testing without a
robot controller is a real workflow advantage), fuse it at **20 A** per R620-C/R621, and wire the
compressor outputs with **18 AWG** per R622.

---

## §10 — Baseline electrical BOM for one competitive robot

Assumptions: **4-motor swerve** (R502 caps propulsion at 4 motors) with 4 azimuth motors, **2
mechanism motors**, **REV PDH**, **Limelight 3A** vision, **no pneumatics**, **no turret**.

### 10.1 — The BOM

| # | Item | P/N | Qty | Unit | Ext. | Verified? |
|---|---|---|---|---|---|---|
| **CONTROL CORE** |
| 1 | **Systemcore** robot controller | TBA | 1 | **UNVERIFIED** ("lower than roboRIO") | **UNVERIFIED** | ✗ [C on the pricing *statement*] |
| 2 | Robot Signal Light | am-3583 or 855PB-B12ME522 | 1 | UNVERIFIED | UNVERIFIED | ✗ |
| 3 | **VH-109 radio** | VH-109 / WCP-1538 | 1 | UNVERIFIED | UNVERIFIED | ✗ |
| **POWER** |
| 4 | **REV Power Distribution Hub** | REV-11-1850 | 1 | **$250.00** | **$250.00** | ✓ |
| 5 | 120 A main breaker | CB185-120 (or listed equiv.) | 1 | UNVERIFIED | UNVERIFIED | ✗ |
| 6 | Anderson SB50 connector pair | — | 3 | UNVERIFIED | UNVERIFIED | ✗ |
| 7 | 6 AWG copper wire (main path) | — | 6 ft | UNVERIFIED | UNVERIFIED | ✗ |
| 8 | **SLA battery, 12 V 18 Ah** (R601-legal) | — | **6** | UNVERIFIED | UNVERIFIED | ✗ |
| 9 | Battery charger, ≤6 A, SB connector (R603/R604) | — | 2 | UNVERIFIED | UNVERIFIED | ✗ |
| 10 | Breaker/fuse assortment (40 A ×8, 20 A ×4, 10 A ×4) | R619/R620-legal | 1 set | UNVERIFIED | UNVERIFIED | ✗ |
| 11 | Wire: 12 AWG ×50 ft, 18 AWG ×50 ft, ferrules | — | 1 set | UNVERIFIED | UNVERIFIED | ✗ |
| **MOTORS + CONTROLLERS** |
| 12 | **Kraken X60** — swerve drive | WCP-0940 | 4 | **$217.99** (edu, variant UNVERIFIED) | **$871.96** | PARTIAL |
| 13 | **NEO** — swerve azimuth | REV-21-1650 | 4 | **$50.00** | **$200.00** | ✓ |
| 14 | **Thrifty Nova** — azimuth controllers | TTB-0100 | 4 | **$90.00** | **$360.00** | ✓ |
| 15 | **NEO Vortex** — mechanism | REV-21-1652 | 2 | **$90.00** | **$180.00** | ✓ |
| 16 | **SPARK Flex** — mechanism controllers | REV-11-2159 | 2 | **$110.00** | **$220.00** | ✓ |
| **SENSORS** |
| 17 | **CANcoder** — swerve azimuth absolute | 22-676768 | 4 | **$89.99** | **$359.96** | ✓ |
| 18 | **Pigeon 2.0** IMU (*may be redundant with Systemcore's built-in IMU*) | 21-737785 | 1 | **$199.99** | **$199.99** | ✓ |
| 19 | **CANrange** ToF | 24-827871 | 1 | **$64.99** | **$64.99** | ✓ |
| 20 | Beam-break pairs | — | 3 | UNVERIFIED | UNVERIFIED | ✗ |
| 21 | Limit switches | — | 4 | UNVERIFIED | UNVERIFIED | ✗ |
| **VISION** |
| 22 | **Limelight 3A** + global-shutter USB camera | — | 1 | **$189.00** (LL3A) + camera UNVERIFIED | **$189.00+** | PARTIAL |
| **CABLING** |
| 23 | CAN wire (yellow/green twisted pair), 50 ft | — | 1 | UNVERIFIED | UNVERIFIED | ✗ |
| 24 | Ethernet Cat6 patch, passive PoE injector | — | 2 | UNVERIFIED | UNVERIFIED | ✗ |
| 25 | Zip ties, heat shrink, wire loom, labels | — | 1 set | UNVERIFIED | UNVERIFIED | ✗ |
| 26 | Spares: 1× Kraken, 1× NEO, 1× Nova, 1× CANcoder | — | 1 set | ≈ $217.99+$50+$90+$89.99 | **≈$447.98** | derived |

### 10.2 — Running total

| Bucket | Live-verified subtotal | Status |
|---|---|---|
| Power distribution (PDH) | **$250.00** | ✓ |
| Drive motors (4× Kraken X60) | **$871.96** | edu price, variant UNVERIFIED |
| Azimuth (4× NEO + 4× Nova) | **$560.00** | ✓ |
| Mechanism (2× Vortex + 2× Flex) | **$400.00** | ✓ |
| Sensors (4× CANcoder + Pigeon + CANrange) | **$624.94** | ✓ |
| Vision (Limelight 3A) | **$189.00** | ✓ (camera extra) |
| Spares set | **≈$447.98** | derived |
| **VERIFIED-PRICE SUBTOTAL** | **≈ $3,343.88** | |
| Systemcore, radio, RSL, batteries ×6, chargers ×2, breakers, wire, connectors, beam breaks, limit switches, cabling, consumables | **UNVERIFIED** | **budget an additional $1,200–1,900 [S]** |
| **REALISTIC ALL-IN ELECTRICAL** | **≈ $4,500–5,300** | **[S]** |

**Cost-reduction levers for a tight budget [S]:**

| Swap | Saves | Costs you |
|---|---|---|
| 4× **NEO Vortex + SPARK Flex** instead of 4× Kraken X60 on drive | ≈ **$72** | ~nothing; Vortex is a strong drive motor |
| 4× **NEO + Thrifty Nova** instead of Kraken on drive | ≈ **$312** | Some power density and Phoenix 6's closed loop |
| Drop the **Pigeon 2.0** (pending Systemcore's built-in IMU spec) | **$199.99** | Risk if the built-in IMU underperforms — **hold until 2026-11-12** |
| **Tank/West-Coast drive** instead of swerve | ≈ **$920** (4 azimuth motors + 4 controllers + 4 CANcoders) | Manoeuvrability. See `reference/04_PREDICTIVE_FACTORS.md` before assuming swerve is mandatory |
| Skip vision entirely | **$189–449** | Only viable if the game does not reward ranged/aligned scoring |
| Buy **4 batteries** not 6 | ≈ 2 batteries | Reliability. **Do not do this.** Batteries are the highest ROI line in this BOM |

### 10.3 — "In the KOP" vs "you buy" — **2027 contents are UNKNOWN** [H]

The 2027 Kit of Parts is announced at the **Pre-Kickoff Virtual Kit Release on 2026-11-12** and
distributed via FIRST Choice + kickoff kit. The table below is the **2025/2026 historical pattern
projected forward** — every row is **[H]**, not [C].

| Item | Historical KOP status (2025/26) | 2027 expectation | Label |
|---|---|---|---|
| **Robot controller** (roboRIO → **Systemcore**) | roboRIO historically supplied to rookies / available at cost to veterans | **UNVERIFIED.** A platform transition usually comes with broad distribution, but FIRST has not said | **[H]/UNVERIFIED** |
| Power distribution (PDP/PDH) | Typically in the KOP or FIRST Choice | Likely present | **[H]** |
| **VH-109 radio** | Distributed in the 2025 KoP (shipped with fw 1.1.2) | Likely present **if still required** | **[H]** |
| **Battery** ×1 | Typically 1 battery in the KOP | Likely 1; **you buy the other 5** | **[H]** |
| Battery charger | Sometimes | Assume you buy | **[H]** |
| 120 A main breaker, SB50, 6 AWG | Typically included | Likely | **[H]** |
| Breaker/fuse assortment | Partially | Assume you top up | **[H]** |
| **RSL** | Typically included | Likely | **[H]** |
| **Motors** | A rotating "KOP motor" allotment (historically CIMs, then a brushless voucher) | **UNVERIFIED** — motor allotments have varied every year | **[H]/UNVERIFIED** |
| **Motor controllers** | Occasionally via FIRST Choice / vendor vouchers | Assume you buy | **[H]** |
| Pneumatics starter kit | Historically available via FIRST Choice / vendor | Assume you buy | **[H]** |
| **Sensors, vision, CAN wire, consumables** | Rarely | **You buy** | **[H]** |
| Vendor **discount vouchers** (REV, CTRE, WCP, AndyMark, Limelight) | Consistently offered every season | Very likely | **[H]** |

**Planning rule [S]:** budget as if the KOP contains **the controller, the PD, the radio, one
battery, the main breaker, and the RSL** — and **nothing else you need.** Every year a team that
budgeted for KOP motors gets surprised. Then, on **2026-11-12**, replace this whole table with the
real one and re-run your budget.

---

## §11 — Validation / dry run

Run these before spending money, and again before every inspection.

```bash
# Run from the repository root.

# V1. Every motor P/N in your BOM must appear in the manual's Table 8-1.
for pn in WCP-0940 REV-21-1650 REV-21-1652 24-777378; do
  printf '%-14s ' "$pn"
  grep -qF "$pn" research/rule_inventories/2026_rules_full.txt && echo LEGAL || echo "NOT IN R501"
done

# V2. Every controller P/N must appear in R504.
for pn in TTB-0100 REV-11-2158 REV-11-2159 24-708883 REV-11-1852; do
  printf '%-14s ' "$pn"
  grep -qF "$pn" research/rule_inventories/2026_rules_full.txt && echo LEGAL || echo "NOT IN R504"
done

# V3. YAML parses and every price carries a verification flag.
python -c "
import yaml
d=yaml.safe_load(open('reference/bom/parts_electronics.yaml'))
bad=[p['name'] for p in d['parts'] if 'verified' not in p]
print('parts:',len(d['parts']),'| missing verified flag:',bad or 'none')
print('unverified prices:',sum(1 for p in d['parts'] if not p.get('verified')))
"

# V4. Cycle model still runs (launcher decisions depend on it).
python tools/cycle-model.py --game rebuilt | head -20
```

### Inspection dry-run checklist (paper, before the event) [C, derived from the rules cited above]

| ✔ | Check | Rule |
|---|---|---|
| ☐ | Exactly 1 battery, R601-legal dimensions/capacity, securely mounted in any orientation | R601, R606 |
| ☐ | All battery + main-breaker terminals **fully insulated** | R607 |
| ☐ | 120 A breaker reachable from outside the robot; only one on the robot | R612 |
| ☐ | 6 AWG from battery → SB50 → 120 A breaker → PD, nothing else in that path | R609 |
| ☐ | Every branch circuit on exactly one PD breaker; **one wire per terminal** | R610, R618 |
| ☐ | Motor-controller branches ≤40 A; PCM/PH-with-compressor ≤20 A | R621 |
| ☐ | Wire gauge matches breaker size everywhere | R622 |
| ☐ | Wire colours: +ve red/yellow/white/brown/black-stripe; −ve black/blue | R624 |
| ☐ | **No electrical connection to the frame anywhere** | R611 |
| ☐ | PD, wiring, breakers all **visible** | R613 |
| ☐ | 1–2 RSLs, visible from 36 in, on the RSL terminals, jumpered if 855PB | R709 |
| ☐ | Radio is a VH-109, diagnostic LEDs visible, powered per R616/R617 on a dedicated 10 A circuit | R702, R708, R616, R617 |
| ☐ | Every motor and controller appears in R501 / R504 | R501, R504 |
| ☐ | ≤4 propulsion motors | R502 |
| ☐ | One load per controller (except the R505 exceptions) | R505 |
| ☐ | No device altering the CAN bus; no PWM + CAN on the same controller | R714, R716 |
| ☐ | *If pneumatic:* compressor, relief valve @125 psi, pressure switch/sensor, vent plug, **2** gauges, primary regulator ≤60 psi, all present and visible | R805, R808, R810, R811 |
| ☐ | *If pneumatic:* no combined solenoid outputs; tubing ≤¼ in OD | R814, R804-D |
| ☐ | No CUSTOM CIRCUIT above 24 V | R614 |
| ☐ | No extra batteries anywhere, even unpowered | R605 |

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/bom/03_LAUNCHERS_ELECTRONICS.md` | This document |
| `reference/bom/parts_electronics.yaml` | Machine-readable parts table: name, part number, vendor, price, `verified` flag, verification date, source URL, and the rule that legalises it |

**Referenced, not modified:** `tools/cycle-model.py`, `tools/rule-show.py`, `tools/frc_diff.py`,
`research/rule_inventories/2026_rules_full.txt`, `manuals/archive/frc/2026_REBUILT_GameManual.pdf`,
`reference/04_PREDICTIVE_FACTORS.md`, `reference/RULE-CHURN-WATCHLIST.md`,
`reference/QA-AMBIGUITY-HOTSPOTS.md`.

---

## Known limitations

1. **All rule quotations are from the 2026 REBUILT manual.** BIOCORE's 2027 manual will renumber
   nothing (the 2024 scheme is stable) but **will rewrite every roboRIO reference.** Treat R615,
   R701, R703, R711–R717 as *guaranteed to change*.
2. **Systemcore price, KoP distribution, and the radio question are unanswerable today.** The only
   confirmed pricing statement is the goal of being *"lower than the roboRIO."* The blocking event
   is the **Pre-Kickoff Virtual Kit Release on 2026-11-12**.
3. **Kraken X60/X44 pricing is only partially verified.** The WCP page showed MSRP $399.99 and an
   FRC educational price of $217.99, but the mapping of those figures to the X60 vs X44 vs
   multi-packs was not resolvable from the page text. **Verify before ordering.**
4. **Many prices are UNVERIFIED**: batteries, chargers, the VH-109, the RSL, breakers, wire,
   connectors, PDP/PDP 2.0/AMPD, NEO 550, CIM, Talon SRX, Victor SPX, Koors40, Venom, navX2,
   beam breaks, limit switches, all pneumatic components, and all launcher wheel SKUs. They are
   marked UNVERIFIED rather than estimated, per project accuracy policy.
5. **Motor performance specs are incomplete.** Kraken X60/X44 free speed, stall torque, and stall
   current were not resolvable from the WCP product page; consult `docs.wcproducts.com/kraken-x60/`
   and `docs.wcproducts.com/kraken-x44/`.
6. **The REV Through Bore Encoder V1 (REV-11-1271) is listed DISCONTINUED.** A 2027 design should
   not depend on it. A successor SKU was not identified in this pass.
7. **The entire launcher half is [S].** BIOCORE's scoring element is not public. No claim here is a
   prediction that BIOCORE rewards launching. The base rate (§1.1) is roughly a coin flip.
8. **No launcher part numbers are given.** Wheel SKUs (Colson, compliant, Fairlane, BaneBots) vary
   by bore and vendor, and guessing one would violate the project accuracy policy. Verify on the
   vendor page at purchase time.
9. **The BOM assumes swerve.** If `reference/04_PREDICTIVE_FACTORS.md` argues against swerve for a
   team this size, the BOM drops by roughly $920 and this document does not re-litigate that.
10. **Cycle-time and EV arithmetic is deliberately absent.** It lives in `tools/cycle-model.py`.
    Duplicating it here would create two sources of truth.
