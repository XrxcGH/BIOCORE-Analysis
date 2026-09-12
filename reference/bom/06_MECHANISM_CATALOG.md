# Mechanism Catalog — 27 archetypes, priced, hour-costed, and gated

**Purpose.** Phase 1 of this BOM effort produced three deep vendor files (drivetrain, manipulation,
launchers+electronics) holding ~900 verified part rows. Nobody builds a *part*; they build a
*mechanism*. This file consolidates those rows into 27 buildable mechanism archetypes, each with a
delivered cost, a tooling floor, an hours cost, its failure modes, and a buy-vs-make verdict written
specifically for ~15 students with one experienced mentor and $2,500 of discretionary robot budget.
Then it hands the whole thing to a tool that will tell you, in numbers, that your kickoff whiteboard
robot is impossible.

**Companion files:** [`mechanism_catalog.yaml`](mechanism_catalog.yaml) (machine-readable, consumed
by [`../../tools/bom-builder.py`](../../tools/bom-builder.py)) ·
[`../team_capacity.yaml`](../team_capacity.yaml) (gate thresholds) ·
[`examples/`](examples/) (three runnable input files).

## Evidence labels

| Label | Meaning | Where it appears in this catalog |
|---|---|---|
| **[C]** CONFIRMED | Read off a live vendor product page on 2026-08-22 by phase 1, or quoted from a manual this repo holds | 119 of 146 COTS lines; every `unit_price` |
| **[H]** HISTORICAL-PATTERN | Recurs across seasons in the 1992–2026 manual corpus; not stated for BIOCORE | Mechanism *relevance* claims, bumper rules, launcher-game frequency |
| **[S]** SPECULATION | Engineering inference or planning estimate | All `build_hours` / `design_hours` / `programming_hours`; all `est_unit_price`; every game-piece-class mapping |
| **UNVERIFIED** | Not confirmed against a live source | 27 of 146 COTS lines — these carry `unit_price: null` and a separate `est_unit_price`; **do not raise a PO against them** |

**The rule this catalog never breaks:** an estimate is never written into a `unit_price` field. If a
price was not read from a live page it is `null`, and the planning figure lives in `est_unit_price`
where the tool renders it with a `~` and a `U` flag. Estimated dollars are reported separately in
every rollup.

## Source shorthand

`REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO ·
`PF` = [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) ·
`CAP` = [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) ·
`ARCH` = [`../03_ARCHETYPE_CORPUS.md`](../03_ARCHETYPE_CORPUS.md) ·
`DT/MAN/ELE` = [`01_DRIVETRAIN.md`](01_DRIVETRAIN.md) / [`02_MANIPULATION_ELEVATION.md`](02_MANIPULATION_ELEVATION.md) / [`03_LAUNCHERS_ELECTRONICS.md`](03_LAUNCHERS_ELECTRONICS.md).

## Two warnings that govern everything below

1. **BIOCORE's scoring element is not public.** Name, geometry, and mass are unknown as of
   2026-08-22. Every `game_piece_classes` field is a *hypothesis set* — "this archetype historically
   handles this shape class" — not a claim about BIOCORE. Pollen, StarterBots, and Skill Builders are
   **FTC BIOBUZZ** concepts and appear nowhere in this catalog.
2. **2027 replaces the roboRIO with Systemcore.** WPILib 2027 is Systemcore-only, so no 2026 code
   carries over untouched. That is why `baseline_electrical_package` carries **40 programming hours**
   and why every programming-hours figure in this file should be read as competing against a budget
   that `CAP` §3.2 already flagged as the tightest role on the team.

---

## §0 — The 60-second workflow (runnable)

```bash
# Run from the repository root.

# 1. WHAT EXISTS? every archetype, its cost, its hours, its motor count (2 s)
python tools/bom-builder.py --list

# 2. PRICE THE ROBOT YOU ACTUALLY WANT.
#    Copy an example, edit the mechanism list, run it.
cp reference/bom/examples/simple.yaml /tmp/my_robot.yaml
python tools/bom-builder.py /tmp/my_robot.yaml

# 3. THE SINGLE LINE THAT MATTERS IS "VERDICT:".
#    ALL GATES PASS  -> exit 0, the plan fits the team.
#    FAILS n GATE(S) -> exit 1, and the gate names tell you exactly what to cut.

# 4. SHOW THE TEAM WHY THE WHITEBOARD ROBOT IS IMPOSSIBLE. Run these side by side.
python tools/bom-builder.py reference/bom/examples/simple.yaml     | tail -25
python tools/bom-builder.py reference/bom/examples/ambitious.yaml  | tail -25

# 5. TURN IT INTO A PURCHASE ORDER (CSV opens in any spreadsheet)
python tools/bom-builder.py /tmp/my_robot.yaml --csv /tmp/po.csv

# 6. PASTE IT INTO THE BUILD BINDER
python tools/bom-builder.py /tmp/my_robot.yaml --markdown > /tmp/bom.md

# 7. BEFORE ANY MONEY MOVES: re-verify every price against the live vendor pages.
bash reference/bom/recheck_prices.sh
```

**Kickoff-day usage, in one line:** at 12:05 on 2027-01-09, read the possession limit and the
scoring geometry, pick mechanism ids from §2, run the tool, and cut whatever the gates reject —
*before* anyone opens CAD.

---

## §1 — The schema, and how to read an entry

Each catalog entry answers eleven questions. This is exactly the shape
[`../../tools/bom-builder.py`](../../tools/bom-builder.py) consumes.

| Field | What it holds | Label |
|---|---|---|
| `id` · `name` · `function` | Stable key, human name, one-line job | — |
| `game_piece_classes` | Shape classes this archetype historically handles | **[S]** |
| `cots_parts[]` | `{vendor, item, sku, qty, unit_price, est_unit_price, url, verified}` | **[C]** where `verified: true` |
| `fabricated_parts[]` | `{part, material, process, machine_required, qty, est_hours}` | **[S]** |
| `cots_cost_usd` · `material_cost_usd` · `total_cost_usd` | Computed, not hand-entered — see §13 validation | derived |
| `kop_credit_usd` | Portion the Kit of Parts is expected to supply (2 entries only) | **[H]** / **[S]** |
| `tooling_floor` | `hand_tools` < `bandsaw_drillpress` < `router_cnc` < `mill_lathe` < `outsourced` | **[S]** |
| `build_hours` · `design_hours` · `programming_hours` | Calibrated against `CAP` §3.1 and `MAN` §13 | **[S]** |
| `motors_required` · `controllers_required` · `sensors_required` · `pneumatics_required` | Load on the electrical and CAN budget | **[S]** |
| `lead_time_weeks` · `stockout_risk` | Drives the order-by date | **[H]** |
| `common_failure_modes` | What actually breaks, from the corpus and from `PF` reliability weighting | **[H]** |
| `buy_vs_make_recommendation` | For **15 students**, with the reasoning stated | **[S]** |
| `cheapest_credible_usd` · `best_version_usd` | The floor and ceiling of the same archetype | **[S]** |
| `category` · `workstream` · `counts_as_novel` | Feeds the parallel-workstream and novel-mechanism gates | derived |

**`counts_as_novel`** is the load-bearing flag. `CAP` §5.2 gives this team **`novel_mechanisms_max: 2`**
— two mechanisms beyond the drivetrain. Drivetrain, bumpers, electrical, and vision are marked
`counts_as_novel: false` because they are mandatory infrastructure, not scope choices. Everything
else counts, **including climbers**: `CAP` §5.3 is explicit that an endgame mechanism is
workstream #4.

---

## §2 — The index: all 27 archetypes at a glance

Sorted by category. `total $` = COTS + raw material for the *catalog configuration*; `cheapest
credible` and `best version` bracket it in §3–§10.

| id | category | tooling floor | COTS $ | mat $ | **total $** | build h | design h | prog h | motors | lead wk | stockout | novel |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|:---:|
| `bumpers_frame` | drivetrain | bandsaw_drillpress | 197 | 60 | **257** | 19 | 4 | 0 | 0 | 2 | low | no |
| `kop_chassis` | drivetrain | hand_tools | 1510 | 90 | **1600** | 12 | 4 | 10 | 4 | 0 | low | no |
| `swerve_drivetrain` | drivetrain | bandsaw_drillpress | 2345 | 260 | **2605** | 40 | 22 | 45 | 8 | 4 | high | no |
| `tank_wcd` | drivetrain | mill_lathe | 1080 | 220 | **1300** | 34 | 18 | 12 | 4 | 3 | med | no |
| `deploying_intake` | intake | mill_lathe | 490 | 110 | **600** | 28 | 16 | 12 | 2 | 3 | med | Y |
| `over_bumper_intake` | intake | bandsaw_drillpress | 310 | 70 | **380** | 16 | 8 | 4 | 1 | 2 | low | Y |
| `under_bumper_intake` | intake | bandsaw_drillpress | 230 | 75 | **305** | 18 | 10 | 4 | 1 | 2 | low | Y |
| `gripper_end_effector` | handling | bandsaw_drillpress | 240 | 55 | **295** | 14 | 12 | 6 | 1 | 2 | low | Y |
| `hopper` | handling | hand_tools | 255 | 70 | **325** | 15 | 8 | 2 | 1 | 1 | low | Y |
| `indexer_conveyor` | handling | bandsaw_drillpress | 331 | 80 | **411** | 20 | 10 | 14 | 1 | 2 | low | Y |
| `catapult` | launcher | mill_lathe | 394 | 100 | **494** | 24 | 16 | 10 | 1 | 3 | med | Y |
| `dual_flywheel` | launcher | mill_lathe | 568 | 120 | **688** | 26 | 18 | 22 | 2 | 3 | med | Y |
| `single_flywheel` | launcher | mill_lathe | 284 | 95 | **379** | 20 | 14 | 18 | 1 | 3 | med | Y |
| `turret` | launcher | router_cnc | 480 | 180 | **660** | 38 | 28 | 26 | 1 | 5 | high | Y |
| `variable_hood_shooter` | launcher | router_cnc | 443 | 140 | **583** | 34 | 24 | 30 | 2 | 4 | med | Y |
| `cascade_elevator` | elevation | bandsaw_drillpress | 768 | 150 | **918** | 30 | 20 | 20 | 2 | 4 | med | Y |
| `continuous_elevator` | elevation | bandsaw_drillpress | 903 | 110 | **1013** | 22 | 14 | 14 | 1 | 3 | med | Y |
| `telescoping_arm` | elevation | bandsaw_drillpress | 494 | 90 | **584** | 20 | 12 | 12 | 1 | 3 | med | Y |
| `double_jointed_arm` | arm | mill_lathe | 723 | 160 | **883** | 40 | 30 | 40 | 2 | 4 | med | Y |
| `single_jointed_arm` | arm | mill_lathe | 361 | 95 | **456** | 22 | 16 | 18 | 1 | 3 | low | Y |
| `virtual_four_bar` | arm | mill_lathe | 381 | 110 | **491** | 26 | 18 | 14 | 1 | 3 | low | Y |
| `passive_latch_climber` | climber | bandsaw_drillpress | 185 | 60 | **245** | 12 | 10 | 2 | 0 | 1 | low | Y |
| `telescoping_climber` | climber | mill_lathe | 653 | 100 | **753** | 26 | 18 | 12 | 1 | 3 | med | Y |
| `winch_climber` | climber | bandsaw_drillpress | 454 | 85 | **539** | 18 | 12 | 6 | 1 | 2 | low | Y |
| `baseline_electrical_package` | support | bandsaw_drillpress | 1914 | 65 | **1979** | 30 | 8 | 40 | 0 | 6 | high | no |
| `pneumatics_package` | support | bandsaw_drillpress | 510 | 45 | **555** | 14 | 6 | 5 | 0 | 2 | low | no |
| `vision_package` | support | hand_tools | 293 | 25 | **318** | 6 | 4 | 30 | 0 | 3 | med | no |
| **catalog totals** | 27 entries | | 16797 | 2820 | **19617** | 624 | 380 | 428 | 40 | | | |

**Read the totals row as a sanity check, not a plan.** Building the whole catalog would cost
~$22.4k, ~608 build hours, and 40 motors. The team has **$2,500**, **129.8 build hours**, and a
practical ceiling of **12 motors**. The entire job of this document is to make that gap arithmetic
instead of an argument.

---

## §3–§10 — The catalog by family

Each family gets three tables: costs and shape classes, the actuation/sensor load and the
buy-vs-make verdict, and the failure modes. The verdicts are written for **~15 students, one
experienced mentor, bandsaw + drill press, $2,500** — they are not general FRC advice.

### Drivetrains and frame

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Swerve drivetrain (4 COTS modules)**<br>`swerve_drivetrain` | none | $2032 | $2605 | $2844 | bandsaw_drillpress | C |
| **Tank / West Coast Drive (custom or kit-based 6WD)**<br>`tank_wcd` | none | $1116 | $1300 | $1510 | mill_lathe | C |
| **KOP chassis (AndyMark AM14U-series)**<br>`kop_chassis` | none | $90 | $1600 | $1600 | hand_tools | C |
| **Bumpers + frame perimeter package**<br>`bumpers_frame` | none | $197 | $257 | $300 | bandsaw_drillpress | H |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `swerve_drivetrain` | 8 / 8 | 4x azimuth absolute encoder; 1x IMU; 8x integrated motor encoder | no | BUY the modules outright, always. A 15-student team that machines its own swerve spends its entire fabrication budget on a solved problem. Even buying, swerve consumes ~45 programming hours out of 134.8 available -- and 2027 is a Systemcore port year, so that 45 is on top of a platform rewrite. This is the single largest scope decision on the robot. If programming depth is thin, do not do it. |
| `tank_wcd` | 4 / 4 | 1x IMU; 4x integrated motor encoder | no | MAKE only if you have reliable mill access. The dropped-center bearing bores are the one feature that genuinely needs a mill; a drill press will produce a drivetrain that binds. If you do not have a mill, buy the KOP chassis (see kop_chassis) instead -- it is the same architecture, pre-bored. |
| `kop_chassis` | 4 / 4 | 1x IMU; 4x integrated motor encoder | no | BUY -- it is already bought; it ships with registration. For a 15-student team this is 12 build hours to a competition-legal drivetrain versus 34-40 for anything else, and it frees the entire fabrication budget for the scoring mechanism. 02_TEAM_CAPACITY_MODEL sec 5 says you get TWO novel mechanisms; spending one of them on a drivetrain you were given is the classic rookie error. |
| `bumpers_frame` | 0 / 0 | none | no | MAKE -- there is no credible COTS bumper. Budget 19 hours and start the backing boards the first weekend. CRITICAL: bumper rules are in the top churn tier (see reference/RULE-CHURN-WATCHLIST.md); re-derive every dimension from the BIOCORE manual on 2027-01-09 before a single cut. |

| Mechanism | Common failure modes |
|---|---|
| `swerve_drivetrain` | - Azimuth zero offsets lost after a module is disassembled; robot drives sideways.<br>- Belt/gear backlash in azimuth causes hunting under closed-loop control.<br>- CAN bus ID collisions across 8 controllers + 4 encoders; intermittent brownouts on the bus.<br>- Set screws on drive shafts back out; one corner freewheels mid-match.<br>- Odometry drift when a wheel slips; auto paths walk off target by Week 2. |
| `tank_wcd` | - Bearing bores drilled instead of bored; wheels bind and the drivetrain eats current.<br>- Chain tension lost as rails flex; chain skips a tooth under defense.<br>- Dropped center too shallow -> the robot will not turn on carpet.<br>- Gearbox output shaft shears where a set screw crushed the hex. |
| `kop_chassis` | - Assembled with the gearbox on the wrong side; belly pan no longer fits.<br>- Chain tension not set at assembly; skips in Week 1.<br>- Team treats "it came in a box" as "it is done" and never drive-practices it. |
| `bumpers_frame` | - Bumper geometry rules changed at kickoff and the team built to last year's numbers -- FAILS INSPECTION.<br>- Corner gaps exceed the allowance; inspector rejects.<br>- Fabric not tight; noodle rotates and the bumper sags below the legal zone.<br>- Only one colour set built. Both are required. |

**The drivetrain decision, compressed.** `PF` §3 weights swerve-vs-tank at 45 — real, but not
decisive. What *is* decisive for this team is that swerve costs **45 programming hours** in a
Systemcore port year against a 134.8-hour budget that `CAP` §3.2 already calls the tightest role on
the team. `kop_chassis` gets you a legal, drivable robot in **12 build hours and 10 programming
hours**, leaving both of your novel-mechanism slots for scoring. `tank_wcd` is the only drivetrain
in the catalog whose tooling floor exceeds this shop's — the dropped-center bearing bores genuinely
need a mill, and a drill press will produce a drivetrain that binds.

### Intakes

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Over-bumper roller intake (fixed)**<br>`over_bumper_intake` | sphere_small, sphere_large, cube_soft, torus, irregular | $180 | $380 | $400 | bandsaw_drillpress | C |
| **Under-bumper intake**<br>`under_bumper_intake` | disc_flat, cylinder, torus, cube_soft | $175 | $305 | $320 | bandsaw_drillpress | H |
| **Deploying (articulated) intake**<br>`deploying_intake` | sphere_small, sphere_large, cube_soft, torus, cylinder, irregular | $330 | $600 | $620 | mill_lathe | H |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `over_bumper_intake` | 1 / 1 | 1x beam break or current-spike detection | no | HYBRID: buy the roller kit and wheels, make the plates. This is the single best hours-to-capability ratio on the robot at ~16 hours. For a 15-student team the over-bumper fixed intake is the default answer whenever the game piece is floor-accessible and the bumper height allows it. |
| `under_bumper_intake` | 1 / 1 | 1x beam break | no | MAKE, but verify the bumper cutout rule FIRST, verbatim, from the BIOCORE manual. Under-bumper is cheaper and lower than over-bumper but it is rule-coupled in a way over-bumper is not. For a 15-student team, only choose this if the game piece is genuinely too flat to go over the bumper. |
| `deploying_intake` | 2 / 2 | 1x absolute encoder on pivot; 1x beam break; 2x limit switch | no | This is a NOVEL MECHANISM in the 02_TEAM_CAPACITY_MODEL sense -- it costs you one of your two. For a 15-student team, prefer a fixed over-bumper intake unless the game explicitly forces stowing. If you must deploy, use pneumatics for the pivot (see pneumatics_package) -- it removes the encoder, the closed loop, and roughly 8 programming hours. |

| Mechanism | Common failure modes |
|---|---|
| `over_bumper_intake` | - Roller sits too high; the game piece is pushed rather than pulled in.<br>- Compliant wheel durometer too hard; no grip on a smooth piece.<br>- Intake extends outside the frame perimeter at rest -> inspection failure.<br>- Sheet-metal or polycarb side plates flex and the roller axis walks. |
| `under_bumper_intake` | - Bumper cutout exceeds the legal gap allowance -> inspection failure. THE dominant failure.<br>- Ground clearance too low; the robot high-centres on a field seam.<br>- Only works on thin pieces; a spherical piece jams at the bumper line.<br>- Cutout weakens the bumper backing and it cracks on first contact. |
| `deploying_intake` | - Deployed intake gets hit by a defender; the pivot gearbox strips.<br>- No absolute encoder -> pivot loses zero after a brownout and slams into a hard stop.<br>- Deploy speed unlimited in software; the intake self-destructs on the first stow.<br>- Stowed position does not actually clear the frame perimeter -> inspection failure. |

**The intake decision, compressed.** `over_bumper_intake` is the best hours-to-capability ratio in
the entire catalog: 16 build hours, 4 programming hours, one motor, $380 delivered. Take it as the
default. `under_bumper_intake` is cheaper and lower but rule-coupled — the bumper cutout allowance
is the dominant failure mode and it is in the top churn tier
(see [`../RULE-CHURN-WATCHLIST.md`](../RULE-CHURN-WATCHLIST.md)). `deploying_intake` costs a
mill, a second motor, an absolute encoder, and 12 more build hours; take it only when the game
forces stowing, and use pneumatics for the pivot if you do.

### Handling: grippers, indexers, hoppers

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Gripper / claw end effector**<br>`gripper_end_effector` | cylinder, torus, cube_soft, irregular | $155 | $295 | $320 | bandsaw_drillpress | S |
| **Indexer / conveyor**<br>`indexer_conveyor` | sphere_small, cube_soft, cylinder, disc_flat | $240 | $411 | $420 | bandsaw_drillpress | H |
| **Hopper / storage magazine**<br>`hopper` | sphere_small, cube_soft, disc_flat | $195 | $325 | $330 | hand_tools | H |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `gripper_end_effector` | 1 / 1 | 1x time-of-flight or beam break; 1x current sensing for grip detection | no | MAKE. There is no general-purpose COTS FRC gripper because the geometry is game-specific -- and BIOCORE's scoring element is not public, so this entry cannot be more specific than the class. Print jaws in PETG/PC-CF, keep the carrier plates in polycarbonate so they bend instead of break. Roller-style (intake-wheels-in-a-jaw) beats pinch-style for a small team: it self-centres. |
| `indexer_conveyor` | 1 / 1 | 3x beam break for position tracking | no | MAKE, and only if the game genuinely lets you hold more than one piece. 02_MANIPULATION sec 5.1 is explicit: if possession is capped at 1-2, an indexer is 20 build + 14 programming hours you spent for nothing. Check the possession rule at 12:05 on kickoff day before drawing anything. |
| `hopper` | 1 / 1 | none | no | MAKE, cheaply, and only when the game rewards bulk possession. Never build a hopper before you have measured the possession limit. Design the funnel throat at >= 1.6x the piece's largest dimension or it WILL bridge; that ratio is the single highest-value number in this entry. |

| Mechanism | Common failure modes |
|---|---|
| `gripper_end_effector` | - Grip force tuned by stall current; the motor cooks over a 2.5-minute match.<br>- 3D printed jaws crack at the layer line on the first hard contact.<br>- Piece pose entering the gripper is uncontrolled; grip succeeds 70% of the time.<br>- No detection of "have piece"; the driver scores air. |
| `indexer_conveyor` | - Two pieces arrive at once and jam at the singulation point.<br>- Beam breaks blinded by arena lighting; state machine desynchronises.<br>- Indexer state machine has no recovery path; a jam requires a match-ending reboot.<br>- Compression too high; the piece deforms and will not launch consistently. |
| `hopper` | - Pieces bridge across the funnel throat and stop feeding -- the classic hopper failure.<br>- Hopper volume exceeds any legal possession limit; the robot is penalised for holding.<br>- Walls flex outward under load and pieces escape over the top.<br>- Hopper blocks access to the battery / main breaker; pit crew cannot work. |

**The possession-limit question decides this whole family.** `MAN` §5.1 is blunt: if the game caps
possession at 1–2 pieces, an indexer is 20 build hours and 14 programming hours spent for nothing.
Read the possession rule at 12:05 on kickoff day, before anything else in this family is drawn. The
hopper's one non-obvious number: size the funnel throat at **≥ 1.6×** the piece's largest dimension
or it will bridge.

### Launchers

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Single flywheel launcher**<br>`single_flywheel` | sphere_small, disc_flat, torus | $270 | $379 | $400 | mill_lathe | S |
| **Dual flywheel launcher (opposed wheels)**<br>`dual_flywheel` | sphere_small, disc_flat, torus | $512 | $688 | $720 | mill_lathe | S |
| **Variable-hood shooter**<br>`variable_hood_shooter` | sphere_small, disc_flat | $443 | $583 | $700 | router_cnc | S |
| **Turret (rotating launcher/effector platform)**<br>`turret` | sphere_small, disc_flat, torus | $480 | $660 | $780 | router_cnc | S |
| **Catapult / kicker (stored-energy launcher)**<br>`catapult` | sphere_small, sphere_large, cube_soft | $360 | $494 | $520 | mill_lathe | S |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `single_flywheel` | 1 / 1 | 1x integrated motor encoder for closed-loop velocity | no | Only build a launcher if the arithmetic in 03_LAUNCHERS sec 1.8 / tools/cycle-model.py says it beats a placement mechanism on points-per-second. If it does: single flywheel, high-inertia, ONE motor, closed-loop velocity, fixed hood. Recovery time beats peak RPM -- size for inertia, not speed. If BIOCORE's element is not a projectile class, this entry is dead scope. |
| `dual_flywheel` | 2 / 2 | 2x integrated motor encoder | no | For a 15-student team, dual flywheel is a WORSE trade than single flywheel: +6 build hours, +4 programming hours, +$218 in motor, and the only thing you buy is spin control. Choose it ONLY if the game demands a flat trajectory with controlled spin over a long range. Otherwise: single. |
| `variable_hood_shooter` | 2 / 2 | 1x hood absolute encoder; 1x flywheel encoder; vision for range | no | DO NOT BUILD THIS on a 15-student team. It needs router/CNC access, a working vision pose stack, a calibrated lookup table, and 30 programming hours -- it is workstream #4 and #5 at once. The correct small-team answer to "we need two ranges" is TWO FIXED HOODS or a two-position pneumatic hood stop, not a continuously variable one. |
| `turret` | 1 / 1 | 1x absolute encoder; 2x limit switch for travel stops; vision for aiming | no | DO NOT BUILD. A turret is the archetypal scope trap: it requires CNC, vision, a large-diameter bearing with a 5-week lead time, and 26 programming hours -- and its entire benefit (aim while moving) is largely delivered by swerve for free. 02_TEAM_CAPACITY sec 5 gives this team THREE workstreams. A turret is #4. Listed here so it can be explicitly, deliberately rejected. |
| `catapult` | 1 / 1 | 1x limit switch at cocked position; 1x limit switch at release | no | MAKE only for a heavy or soft piece a flywheel cannot grip, and only if the game has ONE launch range. The catapult's honest advantage over a flywheel is that it needs almost no programming (10 h vs 18-30 h) and no closed-loop velocity control -- for a programming-starved 15-student team in a Systemcore year, that is a real argument. Its honest disadvantage is cycle time. |

| Mechanism | Common failure modes |
|---|---|
| `single_flywheel` | - Recovery time between shots dominates cycle time and nobody measured it.<br>- Wheel surface polishes after 200 shots; range drifts short by match 8.<br>- Compression set by feel; shot-to-shot variance is the whole error budget.<br>- Battery sag between shots changes exit velocity; no voltage compensation in the controller.<br>- Open-loop percent-output control instead of closed-loop velocity. Range is then unrepeatable. |
| `dual_flywheel` | - Two velocity loops fight each other; the piece squirts sideways.<br>- Wheel gap not adjustable; one durometer change means new plates.<br>- Doubles the recovery-time problem and doubles the current draw spike.<br>- Backspin tuned once, on one battery, and never re-checked. |
| `variable_hood_shooter` | - Range-to-hood-angle lookup table has 4 points and interpolates badly between them.<br>- Hood backdrives under launch impulse; angle changes shot to shot.<br>- Requires vision to be useful, so it inherits every vision failure mode too.<br>- Arc plates cut on a router with the wrong radius; the hood binds at one end of travel. |
| `turret` | - Wire routing through the rotation axis; cables twist and pull out mid-match.<br>- Travel limits enforced only in software; a code bug shears the ring gear.<br>- Backlash in the ring gear makes closed-loop aiming oscillate.<br>- Turret ring is the heaviest single part on the robot and it is all at the top. |
| `catapult` | - The hard stop takes the full impulse every shot; the frame cracks by Week 2 practice.<br>- Re-cock time is 1.5-3 s and destroys cycle time versus a flywheel.<br>- Single fixed energy -> exactly one range. Any range change means physical re-tuning.<br>- Stored energy at rest is a safety and inspection concern; needs a positive lock. |

**Launchers are conditional scope, and the condition is arithmetic.** ~40% of FRC seasons have had a
projectile scoring element **[H]** — a real prior, but not a prediction about BIOCORE. Before
building any of these, run [`../../tools/cycle-model.py`](../../tools/cycle-model.py) and confirm the
launcher beats a placement mechanism on points-per-second. If it does, the small-team answer is
`single_flywheel`: high inertia, **one** motor, closed-loop velocity, fixed hood. Recovery time
beats peak RPM. `turret` and `variable_hood_shooter` are in this catalog explicitly so a team can
point at them on kickoff day and say no — both need CNC access, a working vision pose stack, and 26–30
programming hours, and `turret` additionally carries a 5-week lead time on a large-diameter bearing.
`catapult`'s honest advantage is that it needs almost no programming (10 h); its honest disadvantage
is a 1.5–3 s re-cock that destroys cycle time.

### Elevation

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Cascade elevator (multi-stage, stages move together)**<br>`cascade_elevator` | cylinder, torus, cube_soft, irregular | $611 | $918 | $950 | bandsaw_drillpress | C |
| **Continuous elevator (single-stage or chained, constant ratio)**<br>`continuous_elevator` | cylinder, torus, cube_soft, irregular | $599 | $1013 | $1100 | bandsaw_drillpress | C |
| **Telescoping arm (linear extension on a pivot or fixed angle)**<br>`telescoping_arm` | cylinder, torus, irregular | $494 | $584 | $620 | bandsaw_drillpress | C |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `cascade_elevator` | 2 / 2 | 1x bottom limit switch; 2x integrated encoder; optional absolute encoder | no | BUY the elevator kit. Fabricating extrusion, bearing blocks, and rigging from scratch is 60+ hours and it is the single most common place a small team's season dies. WCP GreyT at $299.99 or the Thrifty single-stage at $389.00 both remove that risk. Cascade gives you speed; continuous gives you simplicity. See continuous_elevator for the trade. |
| `continuous_elevator` | 1 / 1 | 1x bottom limit switch; 1x integrated encoder | no | BUY. This is the SMALL-TEAM DEFAULT for elevation: one motor, one ratio, one limit switch, no rigging puzzle, ~14 programming hours versus 20 for cascade. You lose top speed and total extension per unit of chassis height. For a 15-student team that trade is nearly always correct. |
| `telescoping_arm` | 1 / 1 | 1x retracted limit switch; 1x integrated encoder | no | BUY the tube kit. Making nested telescoping tubes with correct clearance requires a mill and a lot of fitting. At $220.00 for two stages this is the cheapest reach-extension in the catalog. |

| Mechanism | Common failure modes |
|---|---|
| `cascade_elevator` | - Rigging routed wrong; stages bind or one stage lifts before the other.<br>- Dyneema rope wraps over itself on the drum and the effective radius jumps.<br>- No bottom limit switch; the carriage drives into the base and strips the gearbox.<br>- Gravity holding: elevator falls on disable and shears the carriage. Needs a brake or a ratchet.<br>- Motor sized for speed, not torque; it stalls at the top of travel with a piece. |
| `continuous_elevator` | - Chain stretch changes the zero over the season; positions drift.<br>- Single motor stalls under load at full extension.<br>- No hold mechanism; the carriage sags when disabled.<br>- Chain attachment point is the failure point -- it fatigues and snaps. |
| `telescoping_arm` | - Slide pads wear; the arm develops play at full extension and the tip wanders inches.<br>- Extended arm is a lever; a side hit bends the base tube permanently.<br>- Retraction relies on gravity or a spring and jams when the tubes are loaded off-axis.<br>- Extension limit not enforced; the robot exceeds the extension rule -> penalty. |

**Buy the elevator. This is not a close call.** Fabricating extrusion, bearing blocks, and rigging
from scratch is 60+ hours and it is the single most common place a small team's season dies. Between
the two: `cascade_elevator` gives you speed and extension per unit of chassis height for a rigging
puzzle and a second motor; `continuous_elevator` gives you one motor, one ratio, one limit switch,
and 6 fewer programming hours. **For 15 students, continuous is nearly always the right trade.**
Both need a mechanical hold — brake or ratchet — or the carriage falls when the robot is disabled.

### Arms

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Single-jointed arm**<br>`single_jointed_arm` | cylinder, torus, cube_soft, irregular | $371 | $456 | $520 | mill_lathe | C |
| **Double-jointed arm (shoulder + elbow)**<br>`double_jointed_arm` | cylinder, torus, cube_soft, irregular | $741 | $883 | $1000 | mill_lathe | S |
| **Virtual four-bar (belt/chain-coupled wrist)**<br>`virtual_four_bar` | cylinder, torus, cube_soft | $380 | $491 | $540 | mill_lathe | H |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `single_jointed_arm` | 1 / 1 | 1x absolute encoder on the pivot axis; 2x limit switch | no | MAKE the arm, BUY the gearbox stack. A single-jointed arm is the cheapest and most reliable manipulator topology available to a 15-student team -- one motor, one absolute encoder, one gravity feedforward term. Prefer it over any elevator when the required reach fits an arc. NON-NEGOTIABLE: absolute encoder ON THE JOINT, not on the motor shaft. |
| `double_jointed_arm` | 2 / 2 | 2x absolute encoder on joints; 4x limit switch | no | REJECT for a 15-student team. Forty build hours out of 129.8 and FORTY programming hours out of 134.8 -- in a Systemcore port year that is not a mechanism, it is the entire season. A single- jointed arm on an elevator reaches the same workspace with half the control complexity. Listed so the team can point at this entry and say no on kickoff day. |
| `virtual_four_bar` | 1 / 1 | 1x absolute encoder on shoulder; 2x limit switch | no | MAKE, and strongly prefer this over a double-jointed arm. A virtual four-bar delivers most of the double-jointed benefit -- constant effector attitude across the arc -- for ONE motor and 14 programming hours instead of 40. For a 15-student team this is the correct sophisticated-arm answer. The mechanism does the math so the programmers do not have to. |

| Mechanism | Common failure modes |
|---|---|
| `single_jointed_arm` | - Absolute encoder on the motor instead of the joint -> zero lost through gearbox backlash.<br>- Gravity feedforward not implemented; the arm sags on hold and overshoots on the way up.<br>- Reduction sized for speed; the arm cannot hold a loaded end effector horizontal.<br>- Arm swings outside the frame perimeter at a legal-extension boundary nobody checked. |
| `double_jointed_arm` | - Inverse kinematics written from scratch under time pressure; singularities crash the arm.<br>- Coupled gravity torque -- elbow angle changes the shoulder load -- and the feedforward ignores it.<br>- Joint travel envelope allows self-collision; the arm folds into itself.<br>- Wire routing across two moving joints fails first, not the mechanism.<br>- The two joints together draw more current than budgeted; brownout on simultaneous motion. |
| `virtual_four_bar` | - Chain tension lost -> the wrist angle drifts and the "virtual" constraint stops holding.<br>- Idler placement wrong; the chain rubs the arm tube and saws through it.<br>- The coupling ratio is not 1:1 and nobody noticed until the effector tilts at full extension. |

**The arm hierarchy, in order of preference for this team.** `single_jointed_arm` first: one motor,
one absolute encoder **on the joint** (not on the motor shaft — that is the #1 failure), one gravity
feedforward term. `virtual_four_bar` second: it buys constant end-effector attitude across the arc
for one motor and 14 programming hours, because the mechanism does the math the programmers would
otherwise have to. `double_jointed_arm` is a **reject** — 40 build hours out of 129.8 and 40
programming hours out of 134.8 is not a mechanism, it is the entire season.

### Climbers

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Winch climber (rope/strap pull-up)**<br>`winch_climber` | none | $385 | $539 | $560 | bandsaw_drillpress | C |
| **Telescoping climber (extend-hook-retract)**<br>`telescoping_climber` | none | $545 | $753 | $800 | mill_lathe | C |
| **Passive latch / hook climber (no dedicated actuator)**<br>`passive_latch_climber` | none | $185 | $245 | $260 | bandsaw_drillpress | H |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `winch_climber` | 1 / 1 | 1x limit switch at full retract; 1x integrated encoder | no | BUY the winch kit, MAKE the hook and the structural tie. This is the cheapest points-per-hour endgame in the catalog at 18 build hours and 6 programming hours. Mandatory: a mechanical hold (ratchet or worm) so the climb survives the disable at T=0. That single part is the difference between scoring the climb and not. |
| `telescoping_climber` | 1 / 1 | 2x limit switch; 1x integrated encoder | no | BUY the kit if the game's bar geometry needs the reach. Otherwise prefer winch_climber -- it is $130 cheaper, 8 build hours shorter, and has one fewer failure mode. Telescoping only wins when the climb point is genuinely above the robot's static height. |
| `passive_latch_climber` | 0 / 0 | none | no | MAKE. If the game has a low climb tier reachable by driving into it, this is the highest points-per-hour mechanism in the entire catalog: ZERO motors, ZERO controllers, 2 programming hours. For a 15-student team, check for this option FIRST on kickoff day before pricing a winch. |

| Mechanism | Common failure modes |
|---|---|
| `winch_climber` | - No ratchet or brake; the robot descends when the motor is disabled at match end -> no points.<br>- Rope wraps over itself; effective drum radius jumps and the pull stalls.<br>- Frame not reinforced at the winch mount; the mount tears out under full robot weight.<br>- Hook geometry does not capture the bar reliably at any approach angle but one. |
| `telescoping_climber` | - Extension height rule changed at kickoff; the climber is illegal as designed.<br>- Extended tube is hit by a robot in the last 10 seconds and bends; it will not retract.<br>- Hook misses the bar because the drivers cannot see the alignment. Needs a camera or a guide.<br>- Deployment eats 3-5 s of a 30 s endgame; the cycle math was never done. |
| `passive_latch_climber` | - Latch requires a precise drive approach; it works in the shop and fails at the venue.<br>- Latch engages accidentally during the match and drags on the carpet.<br>- Only reaches the lowest-value climb tier; the points may not justify even 12 hours. |

**Check for the passive option first.** `passive_latch_climber` is the highest points-per-hour
mechanism in the catalog: zero motors, zero controllers, 2 programming hours, 12 build hours. If the
game has a low tier reachable by driving into it, price that before you price a winch. If it does
not, `winch_climber` at 18 build hours and 6 programming hours is the answer — and the ratchet or
worm that holds the climb through the disable at T=0 is not optional, it is the difference between
scoring and not. `telescoping_climber` only wins when the climb point is genuinely above the robot's
static height.

### Support packages

| Mechanism | Game-piece classes | Cheapest credible | Catalog total | Best version | Tooling floor | Ev |
|---|---|---:|---:|---:|---|:--:|
| **Vision package (AprilTag pose + piece detection)**<br>`vision_package` | none | $189 | $318 | $544 | hand_tools | C |
| **Pneumatics package**<br>`pneumatics_package` | none | $425 | $555 | $620 | bandsaw_drillpress | C |
| **Baseline electrical package (Systemcore era)**<br>`baseline_electrical_package` | none | $1400 | $1979 | $2200 | bandsaw_drillpress | C |

| Mechanism | Motors / ctrl | Sensors required | Pneum. | Buy-vs-make verdict for 15 students |
|---|---|---|:---:|---|
| `vision_package` | 0 / 0 | 1x vision coprocessor camera | no | BUY the Limelight. Do NOT roll your own coprocessor stack on a 15-student team in a Systemcore transition year. Even bought, this is ~30 programming hours out of 134.8, and 02_TEAM_CAPACITY sec 5.3 explicitly calls a vision-based pose stack "workstream #4" -- over the line. Treat vision as an OPTION you enable in week 4 if programming is ahead of schedule, not a week-1 commitment. |
| `pneumatics_package` | 0 / 0 | 2x pressure sensor (system + working); limit switches per cylinder | yes | BUY the whole package or skip it entirely -- there is no partial pneumatics. The real trade for a 15-student team: pneumatics buys you a binary actuator with ZERO closed-loop programming, which in a Systemcore port year is worth real hours. It costs ~$450, ~9 lb, and a permanent leak-hunting task. Rule of thumb: worth it at 2+ binary actuations, never worth it for exactly one. |
| `baseline_electrical_package` | 0 / 0 | 1x IMU (Systemcore onboard; may make Pigeon 2.0 redundant) | no | BUY everything; make only the board and the loom. This package is NOT optional and NOT a workstream you can defer -- it is inside mandatory workstream #1. Budget 40 programming hours because 2027 is a Systemcore port: WPILib 2027 is Systemcore-only, so NO 2026 code carries over untouched. Order long-lead items in the fall. Watch for the Pre-Kickoff Virtual Kit Release (2026-11-12) for the first hard Systemcore price and availability data. |

| Mechanism | Common failure modes |
|---|---|
| `vision_package` | - Camera pose in robot frame measured by eye; every tag estimate is off by inches.<br>- Pose estimate fused without a rejection gate; one bad frame teleports the robot's odometry.<br>- Venue lighting differs from the shop; exposure tuned wrong on Thursday.<br>- Latency compensation not implemented; the robot aims where the target used to be. |
| `pneumatics_package` | - Leaks. Every pneumatic robot leaks; the compressor runs all match and browns out the bus.<br>- Vent valve missing or not accessible -> inspection failure.<br>- Cylinder force computed at 60 psi working but the design assumed 120 psi.<br>- Compressor duty cycle exceeds recharge; the last cylinder actuation of the match does not happen.<br>- Adds ~8-10 lb to a weight budget that had no slack. |
| `baseline_electrical_package` | - 2027 SPECIFIC: Systemcore price, availability, and ship date are UNVERIFIED as of 2026-08-22.<br>- Battery count too low; you cannot rotate charged batteries through a qualification schedule.<br>- Crimps done with pliers instead of a proper crimper; intermittent faults nobody can find.<br>- CAN bus daisy chain broken by one bad connector; half the robot disappears from the bus.<br>- Main breaker not accessible per rule; inspection failure.<br>- Wiring not labelled; every pit debug takes 3x longer than it should. |

**`baseline_electrical_package` is not optional and cannot be deferred** — it lives inside mandatory
workstream #1. Its 40 programming hours are the Systemcore port. Its 6-week lead time and `high`
stockout risk make it the earliest order-by date in every example below. Watch the **Pre-Kickoff
Virtual Kit Release on 2026-11-12** for the first hard Systemcore price and availability data; until
then the Systemcore line is `unit_price: null` with a $450 planning estimate, and it is the single
largest unverified number in this catalog.

**Pneumatics rule of thumb:** worth it at **2+ binary actuations**, never worth it for exactly one.
It costs ~$555, ~9 lb of a weight budget with no slack, and a permanent leak-hunting task — but it
buys binary actuators with *zero* closed-loop programming, which in a Systemcore year is a real
argument.

**Vision is an option, not a commitment.** `CAP` §5.3 calls a vision-based pose stack "workstream
#4." Buy the Limelight; enable it in Week 4 if programming is ahead of schedule.

---

## §11 — The gate model

[`../../tools/bom-builder.py`](../../tools/bom-builder.py) checks eight gates against
[`../team_capacity.yaml`](../team_capacity.yaml). Every threshold traces to `CAP`.

| Gate | Threshold | Source | Fails when |
|---|---:|---|---|
| **BUDGET** | $2,500 discretionary | `CAP` §8.1 `robot_discretionary` | gross total − KOP credit exceeds it |
| **TOOLING FLOOR** | `bandsaw_drillpress` | shop inventory | any mechanism needs `router_cnc`, `mill_lathe`, or `outsourced` |
| **BUILD HOURS** | 129.8 h | `CAP` §3.1 fabrication line | Σ `build_hours` exceeds it |
| **DESIGN HOURS** | 74.9 h | `CAP` §3.1 CAD line | Σ `design_hours` exceeds it |
| **PROGRAMMING HOURS** | 134.8 h | `CAP` §3.1 programming line | Σ `programming_hours` exceeds it |
| **PARALLEL WORKSTREAMS** | 3 | `CAP` §5.2, triple-derived | more than 3 *effective* workstreams |
| **NOVEL MECHANISMS** | 2 | `CAP` §5.2 `BINDING` | more than 2 mechanisms with `counts_as_novel: true` |
| **MOTOR COUNT** | 12 | practical CAN/current ceiling | Σ `motors_required` exceeds it |

Two modelling decisions are worth stating explicitly because they change the verdicts:

**KOP credit.** The $2,500 in `CAP` §8.1 is "robot BOM *over the KOP*." So the tool subtracts a
`kop_credit_usd` for the two entries the Kit of Parts is expected to supply: `kop_chassis` ($1,510,
**[H]** — the AM14U-series chassis plus a recent-KOP-typical motor/controller allotment) and
`baseline_electrical_package` ($721, **[S]** — Systemcore + radio + RSL, on the pattern of the
2024–2026 roboRIO-era kits). **Both credits are assumptions. Verify them against the 2027 Kit of
Parts list on kickoff day**; if they are wrong, the simple configuration below moves from PASS to
FAIL on budget, and that is a real risk, not a rounding error.

**Workstream absorption.** A mechanism with **zero motors and ≤ 12 build hours** is treated as
absorbed into an adjacent workstream rather than opening a new one. That is what lets
`passive_latch_climber` ride along in the simple configuration without tripping the 3-workstream
gate. It is a modelling choice, and the tool prints which mechanisms it absorbed so you can argue
with it.

---

## §12 — Three worked examples, with real tool output

All three example inputs live in [`examples/`](examples/) and the output below is pasted verbatim
from actual runs on 2026-08-22. Exit code 0 = all gates pass, 1 = at least one gate fails.

### 12.1 `simple.yaml` — KOP chassis + one intake + passive climb → **exit 0**

```
$ python tools/bom-builder.py reference/bom/examples/simple.yaml
==============================================================================
BOM BUILDER -- SIMPLE -- KOP chassis + one intake + passive climb
catalog: reference/bom/mechanism_catalog.yaml   capacity: reference/team_capacity.yaml
notes: One novel mechanism (over-bumper intake) plus a passive latch endgame that costs zero motors and 2 programming hours. Everything else is mandatory infrastructure. Target: a reliable, driver-practiced robot by Week 1. See 02_TEAM_CAPACITY_MODEL sec 5.3.

==============================================================================

### KOP chassis (AndyMark AM14U-series)  [drivetrain / drivetrain]
    id=kop_chassis  tooling=hand_tools  motors=4  lead=0wk  stockout=low  evidence=C
------------------------------------------------------------------------------
  COTS
    VENDOR                     ITEM                               SKU              QTY       UNIT        EXT V
    AndyMark                   AM14U6 6-Wheel Drop Center Robot D AM-14U6            1     940.00     940.00 v
        https://www.andymark.com/products/am14u6-6-wheel-drop-center-robot-drive-base-2025-frc-kit-of-parts-drive-base
    REV Robotics               NEO Brushless Motor V1.1           REV-21-1650        4      42.50     170.00 v
        https://www.revrobotics.com/rev-21-1650/
    REV Robotics               SPARK MAX Motor Controller         REV-11-2158        4     100.00     400.00 v
        https://www.revrobotics.com/rev-11-2158/
  FABRICATED
    PART                             MATERIAL                       PROCESS            MACHINE              QTY  HOURS
    Belly pan / electronics board    1/8 in polycarbonate           cut + drill        hand_tools             1    3.0
    Superstructure mounting rails    1x1 6061 tube                  cut + drill        bandsaw_drillpress     4    4.0
  SUBTOTAL  cots $  1510.00  material $    90.00  total $  1600.00
  HOURS     build  12.0  design   4.0  programming  10.0  (fab-detail  7.0)
  ORDER BY  2027-01-02   (kickoff 2027-01-09 minus 0 wk lead + 1 wk margin)

### Bumpers + frame perimeter package  [drivetrain / drivetrain]
    id=bumpers_frame  tooling=bandsaw_drillpress  motors=0  lead=2wk  stockout=low  evidence=H
------------------------------------------------------------------------------
  COTS
    VENDOR                     ITEM                               SKU              QTY       UNIT        EXT V
    UNVERIFIED                 Pool noodle, 2-1/2 in nominal, per -                  8      ~4.00      32.00 U
    UNVERIFIED                 1000 denier Cordura, red and blue  -                  2     ~60.00     120.00 U
    UNVERIFIED                 Bumper mounting hardware / bracket -                  1     ~45.00      45.00 U
  FABRICATED
    PART                             MATERIAL                       PROCESS            MACHINE              QTY  HOURS
    Bumper backing                   3/4 in plywood                 cut + drill        bandsaw_drillpress     8    8.0
    Bumper fabric sewing / stapling  Cordura                        sew + staple       hand_tools             2    8.0
    Team number panels               vinyl or sewn numerals         cut + apply        hand_tools             2    3.0
  SUBTOTAL  cots $   197.00  material $    60.00  total $   257.00
  HOURS     build  19.0  design   4.0  programming   0.0  (fab-detail 19.0)
  ORDER BY  2026-12-19   (kickoff 2027-01-09 minus 2 wk lead + 1 wk margin)

### Baseline electrical package (Systemcore era)  [support / software]
    id=baseline_electrical_package  tooling=bandsaw_drillpress  motors=0  lead=6wk  stockout=high  evidence=C
------------------------------------------------------------------------------
  COTS
    VENDOR                     ITEM                               SKU              QTY       UNIT        EXT V
    FIRST / TBD                Systemcore control system          -                  1    ~450.00     450.00 U
    REV Robotics               Power Distribution Hub (PDH)       REV-11-1850        1     250.00     250.00 v
        https://www.revrobotics.com/rev-11-1850/
    AndyMark                   Robot Signal Light (RSL)           am-3583            1      70.00      70.00 v
        https://andymark.com/products/robot-signal-light
    AndyMark                   Vivid-Hosting VH-109 FRC Radio V1. am-5583a           1     201.00     201.00 v
        https://andymark.com/products/vivid-hosting-vh-109-frc-radio-v1-5
    REV Robotics               Radio Power Module (RPM)           REV-11-1856        1      34.00      34.00 v
        https://www.revrobotics.com/rev-11-1856/
    AndyMark                   MK ES17-12 12V SLA Battery (Set of -                  3     116.00     348.00 v
        https://andymark.com/products/mk-es17-12-12v-sla-battery-set-of-2
    AndyMark                   Anderson SB50 Connector with Conta -                  4       6.60      26.40 v
        https://andymark.com/products/sb50-anderson-powerpole-connector-with-contacts
    UNVERIFIED                 120A main breaker (CB285-120)      -                  2     ~25.00      50.00 U
    UNVERIFIED                 Battery charger, <=6A, SB connecto -                  2     ~90.00     180.00 U
    UNVERIFIED                 6 AWG / 12 AWG / 18 AWG wire + fer -                  1    ~160.00     160.00 U
    UNVERIFIED                 Snap-action breaker assortment     -                  1     ~60.00      60.00 U
    UNVERIFIED                 CAN wire 50 ft + Cat6 + consumable -                  1     ~85.00      85.00 U
  FABRICATED
    PART                             MATERIAL                       PROCESS            MACHINE              QTY  HOURS
    Electronics board                1/4 in polycarbonate or 1/8 in cut + drill        bandsaw_drillpress     1    4.0
    Battery retention mount          1/8 in 6061 + strap            cut + drill        bandsaw_drillpress     1    3.0
    Wire loom routing + labelling    split loom + labels            assemble           hand_tools             1    8.0
  SUBTOTAL  cots $  1914.40  material $    65.00  total $  1979.40
  HOURS     build  30.0  design   8.0  programming  40.0  (fab-detail 15.0)
  ORDER BY  2026-11-21   (kickoff 2027-01-09 minus 6 wk lead + 1 wk margin)

### Over-bumper roller intake (fixed)  [intake / scoring]
    id=over_bumper_intake  tooling=bandsaw_drillpress  motors=1  lead=2wk  stockout=low  evidence=C
    note: primary scoring mechanism -- workstream #2
------------------------------------------------------------------------------
  COTS
    VENDOR                     ITEM                               SKU              QTY       UNIT        EXT V
    AndyMark                   Compliant Wheels, 3 in.            -                  6       8.40      50.40 v
        https://andymark.com/products/compliant-wheels
    The Thrifty Bot            Thrifty Dead Axle Tube Roller Kit  -                  2      45.00      90.00 v
        https://www.thethriftybot.com/collections/elevator-kits
    REV Robotics               NEO 550 Brushless Motor            REV-21-1651        1      30.00      30.00 v
        https://www.revrobotics.com/rev-21-1651/
    REV Robotics               SPARK MAX Motor Controller         REV-11-2158        1     100.00     100.00 v
        https://www.revrobotics.com/rev-11-2158/
    The Thrifty Bot            QTY 2 - Half Inch Hex 22 Tooth #25 -                  1      19.99      19.99 v
        https://www.thethriftybot.com/collections/elevator-kits
    The Thrifty Bot            QTY 10 - .50in OD x .25in ID Radia -                  1      20.00      20.00 v
        https://www.thethriftybot.com/collections/elevator-kits
  FABRICATED
    PART                             MATERIAL                       PROCESS            MACHINE              QTY  HOURS
    Intake side plates               1/8 in polycarbonate           cut + drill        bandsaw_drillpress     2    5.0
    Roller standoff tube             1x1 6061 tube                  cut + drill        bandsaw_drillpress     2    2.0
    Polycarbonate funnel / guide     0.060 in polycarbonate         cut + heat bend    hand_tools             1    3.0
  SUBTOTAL  cots $   310.39  material $    70.00  total $   380.39
  HOURS     build  16.0  design   8.0  programming   4.0  (fab-detail 10.0)
  ORDER BY  2026-12-19   (kickoff 2027-01-09 minus 2 wk lead + 1 wk margin)

### Passive latch / hook climber (no dedicated actuator)  [climber / endgame]
    id=passive_latch_climber  tooling=bandsaw_drillpress  motors=0  lead=1wk  stockout=low  evidence=H
    note: endgame with zero actuators; drive into it
------------------------------------------------------------------------------
  COTS
    VENDOR                     ITEM                               SKU              QTY       UNIT        EXT V
    UNVERIFIED                 Spring-loaded latch hardware / gas -                  2     ~40.00      80.00 U
    The Thrifty Bot            Constant Force Spring Kit          -                  1      49.99      49.99 v
        https://www.thethriftybot.com/products/constant-force-spring-kit
    UNVERIFIED                 1/4 in aluminum plate stock for ho -                  1     ~55.00      55.00 U
  FABRICATED
    PART                             MATERIAL                       PROCESS            MACHINE              QTY  HOURS
    Passive hooks                    1/4 in 6061 plate              profile + deburr   bandsaw_drillpress     2    5.0
    Latch pivot + spring mount       1/8 in 6061 sheet              cut + drill        bandsaw_drillpress     2    4.0
    Frame reinforcement              2x1 6061 tube                  cut + drill        bandsaw_drillpress     2    3.0
  SUBTOTAL  cots $   184.99  material $    60.00  total $   244.99
  HOURS     build  12.0  design  10.0  programming   2.0  (fab-detail 12.0)
  ORDER BY  2026-12-26   (kickoff 2027-01-09 minus 1 wk lead + 1 wk margin)

==============================================================================
ROLLUP
==============================================================================
  COTS subtotal                 $  4116.78
  Material / raw stock          $   345.00
  GRAND TOTAL (gross)           $  4461.78
  less KOP-supplied credit      $ -2231.00
  DISCRETIONARY SPEND           $  2230.78   <-- the number the budget gate uses
      of which price-verified   $  2799.78   (16 COTS lines)
      of which ESTIMATED        $  1317.00   (11 COTS lines, marked ~ and U)

  Build hours         89.0      Design hours     34.0      Programming hours   56.0
  Motors                 5      Controllers         5      Pneumatics            no
  Mechanisms             5      Novel               2      Workstreams            4 (eff 3)
  Highest tooling floor required: bandsaw_drillpress

==============================================================================
GATE CHECKS  (vs reference/team_capacity.yaml)
==============================================================================
  [PASS] BUDGET               $2230.78 discretionary (gross $4461.78 - KOP credit $2231.00) limit $2500.00        
         robot_discretionary is the number design trades score against (02_TEAM_CAPACITY_MODEL sec 8.1)
  [PASS] TOOLING FLOOR        bandsaw_drillpress           limit bandsaw_drillpress
         every mechanism is within shop capability
  [PASS] BUILD HOURS          89.0 h                       limit 129.8 h         
         fabrication_assembly line, kickoff -> Week 1 (02_TEAM_CAPACITY_MODEL sec 3.1)
  [PASS] DESIGN HOURS         34.0 h                       limit 74.9 h          
         cad_design line
  [PASS] PROGRAMMING HOURS    56.0 h                       limit 134.8 h         
         2027 is a Systemcore port year -- this line is already inflated ~40 h
  [PASS] PARALLEL WORKSTREAMS 3 effective (5 mechanisms)   limit 3               
         effective: drivetrain, scoring, software; absorbed (0 motors, <=12 build h): passive_latch_climber
  [PASS] NOVEL MECHANISMS     2                            limit 2               
         novel = over_bumper_intake, passive_latch_climber
  [PASS] MOTOR COUNT          5 motors / 5 controllers     limit 12              
         propulsion cap is separately 4 (2026 R502; 2027 UNVERIFIED)

  VERDICT: ALL GATES PASS

==============================================================================
ORDER SCHEDULE  (counted back from kickoff 2027-01-09)
==============================================================================
  2026-11-21   baseline_electrical_package     6 wk lead   stockout=high
  2026-12-19   bumpers_frame                   2 wk lead   stockout=low
  2026-12-19   over_bumper_intake              2 wk lead   stockout=low
  2026-12-26   passive_latch_climber           1 wk lead   stockout=low
  2027-01-02   kop_chassis                     0 wk lead   stockout=low

  EARLIEST ORDER-BY: 2026-11-21  -- anything high-stockout must be on a PO by this date.
  Note: no bag day since 2020, so build continues to the event; these dates protect
  the kickoff-to-Week-1 window, not a bag deadline.
```

This is the configuration a 15-student team should default to on kickoff day. One novel scoring
mechanism, one free endgame, $2,231 discretionary against a $2,500 cap, 89 of 129.8 build hours, 56
of 134.8 programming hours. The **40 hours of slack in every budget is not waste** — `PF` weights
drive practice at 90, the highest factor in the corpus, and `CAP` §3.3 shows the baseline plan closes
with *zero* slack. This configuration is the only one of the three that leaves room to practise.

### 12.2 `moderate.yaml` — swerve + intake + elevator + gripper + winch → **exit 1, fails 5 gates**

```
$ python tools/bom-builder.py reference/bom/examples/moderate.yaml
==============================================================================
BOM BUILDER -- MODERATE -- swerve + intake + continuous elevator + winch climb
catalog: reference/bom/mechanism_catalog.yaml   capacity: reference/team_capacity.yaml
notes: Two novel scoring mechanisms (intake, elevator) plus a motorised endgame. This is at or slightly past the capacity model's binding limit -- run it to see WHICH gate trips first.

  [... per-mechanism COTS / FABRICATED detail elided for length;
      run the command above to see all lines ...]

==============================================================================
ROLLUP
==============================================================================
  COTS subtotal                 $  6364.23
  Material / raw stock          $   705.00
  GRAND TOTAL (gross)           $  7069.23
  less KOP-supplied credit      $  -721.00
  DISCRETIONARY SPEND           $  6348.23   <-- the number the budget gate uses
      of which price-verified   $  5137.23   (33 COTS lines)
      of which ESTIMATED        $  1227.00   (10 COTS lines, marked ~ and U)

  Build hours        159.0      Design hours     80.0      Programming hours  115.0
  Motors                12      Controllers        12      Pneumatics            no
  Mechanisms             7      Novel               4      Workstreams            4 (eff 4)
  Highest tooling floor required: bandsaw_drillpress

==============================================================================
GATE CHECKS  (vs reference/team_capacity.yaml)
==============================================================================
  [FAIL] BUDGET               $6348.23 discretionary (gross $7069.23 - KOP credit $721.00) limit $2500.00        
         robot_discretionary is the number design trades score against (02_TEAM_CAPACITY_MODEL sec 8.1)
  [PASS] TOOLING FLOOR        bandsaw_drillpress           limit bandsaw_drillpress
         every mechanism is within shop capability
  [FAIL] BUILD HOURS          159.0 h                      limit 129.8 h         
         fabrication_assembly line, kickoff -> Week 1 (02_TEAM_CAPACITY_MODEL sec 3.1)
  [FAIL] DESIGN HOURS         80.0 h                       limit 74.9 h          
         cad_design line
  [PASS] PROGRAMMING HOURS    115.0 h                      limit 134.8 h         
         2027 is a Systemcore port year -- this line is already inflated ~40 h
  [FAIL] PARALLEL WORKSTREAMS 4 effective (7 mechanisms)   limit 3               
         effective: drivetrain, endgame, scoring, software
  [FAIL] NOVEL MECHANISMS     4                            limit 2               
         novel = over_bumper_intake, continuous_elevator, gripper_end_effector, winch_climber
  [PASS] MOTOR COUNT          12 motors / 12 controllers   limit 12              
         propulsion cap is separately 4 (2026 R502; 2027 UNVERIFIED)

  VERDICT: FAILS 5 GATE(S): BUDGET, BUILD HOURS, DESIGN HOURS, PARALLEL WORKSTREAMS, NOVEL MECHANISMS

==============================================================================
ORDER SCHEDULE  (counted back from kickoff 2027-01-09)
==============================================================================
  2026-11-21   baseline_electrical_package     6 wk lead   stockout=high
  2026-12-05   swerve_drivetrain               4 wk lead   stockout=high
  2026-12-12   continuous_elevator             3 wk lead   stockout=med
  2026-12-19   bumpers_frame                   2 wk lead   stockout=low
  2026-12-19   over_bumper_intake              2 wk lead   stockout=low
  2026-12-19   gripper_end_effector            2 wk lead   stockout=low
  2026-12-19   winch_climber                   2 wk lead   stockout=low

  EARLIEST ORDER-BY: 2026-11-21  -- anything high-stockout must be on a PO by this date.
  Note: no bag day since 2020, so build continues to the event; these dates protect
  the kickoff-to-Week-1 window, not a bag deadline.
```

This is the configuration most teams actually put on the whiteboard, and it fails five gates. Note
*which* five: budget by 2.5×, build hours by 29, design hours by 5, and both scope gates. It passes
programming and motors — meaning the problem is not that the robot is technically hard, it is that
there is not enough of everything else. The fix is not "work harder"; the fix is to delete
`gripper_end_effector` and `winch_climber` and re-run.

### 12.3 `ambitious.yaml` — the whiteboard robot → **exit 1, fails all 8 gates**

```
$ python tools/bom-builder.py reference/bom/examples/ambitious.yaml
==============================================================================
BOM BUILDER -- AMBITIOUS -- swerve + turret shooter + double-jointed arm + vision + pneumatics
catalog: reference/bom/mechanism_catalog.yaml   capacity: reference/team_capacity.yaml
notes: The whiteboard robot. Every gate that can trip, trips. Run this next to simple.yaml and put both outputs on the wall before anyone starts CAD.

  [... per-mechanism COTS / FABRICATED detail elided for length;
      run the command above to see all lines ...]

==============================================================================
ROLLUP
==============================================================================
  COTS subtotal                 $  8378.70
  Material / raw stock          $  1225.00
  GRAND TOTAL (gross)           $  9603.70
  less KOP-supplied credit      $  -721.00
  DISCRETIONARY SPEND           $  8882.70   <-- the number the budget gate uses
      of which price-verified   $  6590.70   (48 COTS lines)
      of which ESTIMATED        $  1788.00   (17 COTS lines, marked ~ and U)

  Build hours        295.0      Design hours    170.0      Programming hours  254.0
  Motors                17      Controllers        17      Pneumatics           YES
  Mechanisms            11      Novel               6      Workstreams            5 (eff 5)
  Highest tooling floor required: mill_lathe

==============================================================================
GATE CHECKS  (vs reference/team_capacity.yaml)
==============================================================================
  [FAIL] BUDGET               $8882.70 discretionary (gross $9603.70 - KOP credit $721.00) limit $2500.00        
         robot_discretionary is the number design trades score against (02_TEAM_CAPACITY_MODEL sec 8.1)
  [FAIL] TOOLING FLOOR        mill_lathe                   limit bandsaw_drillpress
         needs outsourcing or shop upgrade: deploying_intake (mill_lathe), variable_hood_shooter (router_cnc), turret (router_cnc), double_jointed_arm (mill_lathe), telescoping_climber (mill_lathe) | outsourcing_available: true (budget $400, +2 wk lead)
  [FAIL] BUILD HOURS          295.0 h                      limit 129.8 h         
         fabrication_assembly line, kickoff -> Week 1 (02_TEAM_CAPACITY_MODEL sec 3.1)
  [FAIL] DESIGN HOURS         170.0 h                      limit 74.9 h          
         cad_design line
  [FAIL] PROGRAMMING HOURS    254.0 h                      limit 134.8 h         
         2027 is a Systemcore port year -- this line is already inflated ~40 h
  [FAIL] PARALLEL WORKSTREAMS 5 effective (11 mechanisms)  limit 3               
         effective: drivetrain, endgame, scoring, software, support; absorbed (0 motors, <=12 build h): vision_package
  [FAIL] NOVEL MECHANISMS     6                            limit 2               
         novel = deploying_intake, indexer_conveyor, variable_hood_shooter, turret, double_jointed_arm, telescoping_climber
  [FAIL] MOTOR COUNT          17 motors / 17 controllers   limit 12              
         propulsion cap is separately 4 (2026 R502; 2027 UNVERIFIED)

  VERDICT: FAILS 8 GATE(S): BUDGET, TOOLING FLOOR, BUILD HOURS, DESIGN HOURS, PROGRAMMING HOURS, PARALLEL WORKSTREAMS, NOVEL MECHANISMS, MOTOR COUNT

==============================================================================
ORDER SCHEDULE  (counted back from kickoff 2027-01-09)
==============================================================================
  2026-11-21   baseline_electrical_package     6 wk lead   stockout=high
  2026-11-28   turret                          5 wk lead   stockout=high
  2026-12-05   swerve_drivetrain               4 wk lead   stockout=high
  2026-12-05   variable_hood_shooter           4 wk lead   stockout=med
  2026-12-05   double_jointed_arm              4 wk lead   stockout=med
  2026-12-12   vision_package                  3 wk lead   stockout=med
  2026-12-12   deploying_intake                3 wk lead   stockout=med
  2026-12-12   telescoping_climber             3 wk lead   stockout=med
  2026-12-19   bumpers_frame                   2 wk lead   stockout=low
  2026-12-19   indexer_conveyor                2 wk lead   stockout=low
  2026-12-19   pneumatics_package              2 wk lead   stockout=low

  EARLIEST ORDER-BY: 2026-11-21  -- anything high-stockout must be on a PO by this date.
  Note: no bag day since 2020, so build continues to the event; these dates protect
  the kickoff-to-Week-1 window, not a bag deadline.
```

Every gate trips. 295 build hours against 129.8. 254 programming hours against 134.8 — in a
Systemcore port year. Five mechanisms need tooling this shop does not have. **Print this next to
§12.1 and put both on the shop wall before anyone opens CAD on 2027-01-09.**

### 12.4 Machine-readable output

```bash
python tools/bom-builder.py reference/bom/examples/simple.yaml --csv /tmp/po.csv     # spreadsheet
python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown > bom.md   # build binder
python tools/bom-builder.py /tmp/x.yaml --catalog other.yaml --capacity other.yaml   # what-if
```

CSV columns: `mechanism_id, mechanism_name, line_type, vendor_or_material, item_or_part,
sku_or_process, machine, qty, unit_price, ext_price, hours, verified, url, order_by`. `line_type` is
`COTS`, `FABRICATED`, or `MATERIAL_STOCK`.

---

## §13 — Validation / dry run

Every check below is runnable and was run on 2026-08-22.

### 13.1 Verified-vs-unverified part count

| Category | Verified COTS lines **[C]** | UNVERIFIED lines | Total | % verified |
|---|---:|---:|---:|---:|
| drivetrain | 13 | 5 | 18 | 72% |
| intake | 18 | 0 | 18 | 100% |
| handling | 12 | 3 | 15 | 80% |
| launcher | 20 | 5 | 25 | 80% |
| elevation | 18 | 0 | 18 | 100% |
| arm | 19 | 0 | 19 | 100% |
| climber | 9 | 3 | 12 | 75% |
| support | 10 | 11 | 21 | 48% |
| **TOTAL** | **119** | **27** | **146** | **81.5%** |

Fabricated-part lines: **84** (all **[S]** by nature -- hours are estimates, materials are named stock).

**27 of 146 COTS lines (18.5%) are UNVERIFIED**, and they concentrate in exactly the places you would
expect: raw consumables (wire, fasteners, tubing, pool noodle, Cordura) and the one part nobody can
price yet — **Systemcore**, at $450 estimated, which is the single largest unverified line in the
catalog. Every unverified line renders with a `~` on the price and a `U` in the verified column, and
every rollup reports estimated dollars separately from verified dollars.

### 13.2 The runnable checks

```bash
# Run from the repository root.

# V1. The catalog is valid YAML and every mechanism has every required field.
python - <<'EOF'
import yaml
REQ=["id","name","function","game_piece_classes","cots_parts","fabricated_parts",
     "cots_cost_usd","material_cost_usd","total_cost_usd","tooling_floor","build_hours",
     "design_hours","programming_hours","motors_required","controllers_required",
     "sensors_required","pneumatics_required","lead_time_weeks","stockout_risk",
     "common_failure_modes","buy_vs_make_recommendation","cheapest_credible_usd",
     "best_version_usd","category","workstream","counts_as_novel"]
d=yaml.safe_load(open("reference/bom/mechanism_catalog.yaml",encoding="utf-8"))
bad=[(m["id"],k) for m in d["mechanisms"] for k in REQ if k not in m]
print("mechanisms:",len(d["mechanisms"]),"| missing fields:",bad or "none")
EOF

# V2. Every cost rollup equals the sum of its line items (catches hand-edit drift).
python - <<'EOF'
import yaml
d=yaml.safe_load(open("reference/bom/mechanism_catalog.yaml",encoding="utf-8"))
bad=[]
for m in d["mechanisms"]:
    c=sum((p["unit_price"] if p["unit_price"] is not None else (p.get("est_unit_price") or 0))*p["qty"]
          for p in m["cots_parts"])
    if abs(c-m["cots_cost_usd"])>0.01 or abs(c+m["material_cost_usd"]-m["total_cost_usd"])>0.01:
        bad.append(m["id"])
print("cost-arithmetic mismatches:", bad or "none")
EOF

# V3. cheapest_credible <= total <= best_version for every entry.
python - <<'EOF'
import yaml
d=yaml.safe_load(open("reference/bom/mechanism_catalog.yaml",encoding="utf-8"))
bad=[m["id"] for m in d["mechanisms"]
     if not (m["cheapest_credible_usd"]<=m["total_cost_usd"]<=m["best_version_usd"])]
print("price bands out of order:", bad or "none")
EOF

# V4. No estimate was ever promoted into a unit_price field.
python - <<'EOF'
import yaml
d=yaml.safe_load(open("reference/bom/mechanism_catalog.yaml",encoding="utf-8"))
bad=[(m["id"],p["item"]) for m in d["mechanisms"] for p in m["cots_parts"]
     if (p["unit_price"] is not None) != bool(p["verified"])]
print("verified/price-presence mismatches:", bad or "none")
EOF

# V5. The tool runs clean on all three examples and returns the expected exit codes.
for f in simple moderate ambitious; do
  python tools/bom-builder.py reference/bom/examples/$f.yaml >/dev/null 2>&1
  echo "$f -> exit $?"      # expect: simple 0, moderate 1, ambitious 1
done

# V6. Bad input is rejected, not silently ignored.
printf 'name: x\nmechanisms: [flux_capacitor]\n' > /tmp/bad.yaml
python tools/bom-builder.py /tmp/bad.yaml; echo "expect exit 2, got $?"

# V7. KICKOFF DAY ONLY: prices move. Re-verify before any money moves.
bash reference/bom/recheck_prices.sh
```

### 13.3 Results of the dry run, 2026-08-22

```
V1  mechanisms: 27 | missing fields: none
V2  cost-arithmetic mismatches: none
V3  price bands out of order: none
V4  verified/price-presence mismatches: none
V5  simple     -> exit 0
V5  moderate   -> exit 1
V5  ambitious  -> exit 1
V6  unknown id rejected -> exit 2 : ERROR: unknown mechanism id(s): flux_capacitor
V7  recheck_prices.sh -- NOT run in this pass; run it before any purchase order.
```

---

## Files written by this pass

| File | Size | What it is |
|---|---:|---|
| [`06_MECHANISM_CATALOG.md`](06_MECHANISM_CATALOG.md) | this file | The catalog, the gate model, three worked examples |
| [`mechanism_catalog.yaml`](mechanism_catalog.yaml) | ~1,280 lines | 27 archetypes, 146 COTS lines, 84 fabricated-part lines, machine-readable |
| [`../team_capacity.yaml`](../team_capacity.yaml) | ~110 lines | Gate thresholds — the machine-readable form of `CAP` §8, which that file referenced but had never emitted |
| [`../../tools/bom-builder.py`](../../tools/bom-builder.py) | ~440 lines | BOM composer + 8 gate checks + order-by scheduler; `--markdown`, `--csv`, `--list` |
| [`examples/simple.yaml`](examples/simple.yaml) | 16 lines | Passing configuration — the kickoff-day default |
| [`examples/moderate.yaml`](examples/moderate.yaml) | 20 lines | Fails 5 gates — the whiteboard robot most teams draw |
| [`examples/ambitious.yaml`](examples/ambitious.yaml) | 19 lines | Fails all 8 gates — the teaching artefact |

**Consolidated, not duplicated.** Phase-1 files [`01_DRIVETRAIN.md`](01_DRIVETRAIN.md),
[`02_MANIPULATION_ELEVATION.md`](02_MANIPULATION_ELEVATION.md),
[`03_LAUNCHERS_ELECTRONICS.md`](03_LAUNCHERS_ELECTRONICS.md) and their three `parts_*.yaml`
companions remain the authority on individual parts, specs, and price provenance. This file adds
*composition* and *gating* on top; it re-verified nothing and re-priced nothing.

---

## Known limitations

1. **BIOCORE's scoring element is unknown.** Every `game_piece_classes` mapping is **[S]**. The
   catalog cannot tell you which archetype BIOCORE rewards — only what each archetype costs once you
   know. Re-read §2 with the real element in hand on 2027-01-09.
2. **The Systemcore line is the largest unverified number here** ($450 estimated, `unit_price: null`).
   The Pre-Kickoff Virtual Kit Release on **2026-11-12** is the first date this can be fixed, and it
   falls *before* the earliest order-by date the tool computes (2026-11-21) — which is fortunate, and
   also means that date is the real deadline for this whole plan.
3. **Both KOP credits are assumptions** (§11). If the 2027 Kit of Parts does not include the chassis
   allotment or the control system, the simple configuration fails the budget gate. This is the
   single most consequential assumption in the file.
4. **All hours are [S].** They are calibrated against `CAP` §3.1 and `MAN` §13, not measured on this
   team. A team that has built an elevator before will beat these numbers; a team that has not will
   miss them. Log actuals this season and recalibrate.
5. **The catalog prices one configuration per archetype.** `cheapest_credible_usd` and
   `best_version_usd` bracket the range, but the tool only computes the middle configuration. It will
   not automatically find you the cheap version.
6. **Prices are a 2026-08-22 snapshot.** FRC vendor prices moved mid-season in 2026. Treat everything
   as ±10% and run [`recheck_prices.sh`](recheck_prices.sh) before any purchase order.
7. **No weight model.** The catalog tracks dollars, hours, motors, and tooling — not pounds. Weight
   is a hard rule limit and this file will not catch you exceeding it. That is a gap worth closing.
8. **Rule-coupled entries are dated.** `bumpers_frame`, `under_bumper_intake`, and
   `telescoping_climber` depend on rules in the top churn tier
   ([`../RULE-CHURN-WATCHLIST.md`](../RULE-CHURN-WATCHLIST.md)). Re-derive their geometry from the
   BIOCORE manual before cutting anything.
9. **The 12-motor cap is [S].** The 2026 propulsion cap of 4 is **[C]** for 2026; the 2027 motor
   rules are UNVERIFIED. If BIOCORE changes the motor rules, edit `team_capacity.yaml`, not this file.
