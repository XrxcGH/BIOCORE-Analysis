# Manipulation & Elevation — verified COTS parts, architectures, and the hours they actually cost

**Purpose:** give a 15-student team a pre-kickoff parts and architecture reference for *touching the
game piece* and *moving it vertically*, so that on 2027-01-09 the only open question is **which class
of game piece BIOCORE uses** — not which wheel, which elevator kit, or how many hours it costs.
Every price below was pulled from a live vendor page on **2026-08-22** or is marked **UNVERIFIED**.
Nothing here assumes a BIOCORE game piece; BIOCORE's scoring element specs are **not public**.

**Companion file:** [`parts_manipulation.yaml`](parts_manipulation.yaml) — machine-readable SKU/price
table with the same evidence labels, consumable by a BOM generator or a kickoff-day cost roll-up.

**Sibling BOM files in this directory:** [`01_DRIVETRAIN.md`](01_DRIVETRAIN.md) +
[`parts_drivetrain.yaml`](parts_drivetrain.yaml) · [`03_LAUNCHERS_ELECTRONICS.md`](03_LAUNCHERS_ELECTRONICS.md)
+ [`parts_electronics.yaml`](parts_electronics.yaml). Motors, gearboxes, motor controllers and the
Systemcore-side electrical budget for every mechanism in *this* file live in those two — this file
deliberately does not re-price them.

> **Schema divergence, flagged for whoever assembles the master BOM.** [`recheck_prices.sh`](recheck_prices.sh)
> parses `url:` / `unit_usd:` keys (the drivetrain file's schema). `parts_manipulation.yaml` uses
> `source:` / `price_usd:`. **The shared script will silently find zero rows in this file.** Use the
> Python validator in §15 for this file, or normalise the two schemas before running a combined check.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Fetched from a live vendor/primary page on 2026-08-22, price quoted verbatim |
| **[H]** HISTORICAL-PATTERN | Observed across prior FRC seasons/manuals in this corpus; not stated for BIOCORE |
| **[S]** SPECULATION | Inference, flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked in this pass. **Check before you spend money.** |

**Source shorthand**

`REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO · `CHRG` = 2023 CHARGED UP ·
`RAPD` = 2022 RAPID REACT · `INFR` = 2020-21 INFINITE RECHARGE · `DEEP` = 2019 DESTINATION: DEEP SPACE ·
`PWUP` = 2018 POWER UP · `STMP` = 2017 STEAMWORKS · `STRO` = 2016 STRONGHOLD.
All manuals in [`manuals/archive/frc/`](../../manuals/archive/frc/). Rule inventories in
[`research/rule_inventories/`](../../research/rule_inventories/). The manuals are not in the
repository, because FIRST's documents are not redistributed; `bash tools/rebuild-corpus.sh --fetch`
downloads them.

**Vendor shorthand:** `AM` = AndyMark · `WCP` = WestCoast Products · `TTB` = The Thrifty Bot ·
`REV` = REV Robotics · `VEX` = VEX Robotics / VEXpro · `CTRE` = CTR Electronics (also resells WCP) ·
`MMC` = McMaster-Carr.

> **Scope guard.** BIOCORE is **FRC**. Nothing here draws on FTC BIOBUZZ. "Pollen", StarterBots and
> Skill Builders are FTC things and appear nowhere in this document. See
> [`research/00_PREMISE_CORRECTION.md`](../../research/00_PREMISE_CORRECTION.md).
>
> **Control-system guard.** 2027 replaces the roboRIO with **Systemcore**. Nothing in *this* file is
> Systemcore-dependent — rollers and elevators are mechanical — but the *motor controller* count and
> the CAN/CAN-FD topology for every mechanism below live in
> [`reference/team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md). Budget the
> controller, not just the motor.

---

## 0. Kickoff-day 60-second workflow

At 12:05 p.m. ET on **2027-01-09**, with the manual PDF on disk, run this. It answers exactly one
question — *which game-piece class am I building for* — and that answer selects the rest of this file.

```bash
# Run from the repository root.
M="manuals/2026-27_BIOCORE/BIOCORE_GameManual.pdf"     # the file you download at 12:00 ET

pdftotext -layout "$M" - | tr -s ' \n' ' ' > /tmp/bio.txt

# ---- 1. GAME PIECE CLASS: what shape and how big? (the only question that matters at 12:05) ----
grep -oiE "([0-9]+(\.[0-9]+)?|[0-9]+ ?[0-9]*/[0-9]+) ?(in|inch|inches|\") ?(diameter|dia\.?|nominal|tall|long|wide)" /tmp/bio.txt | sort | uniq -c | sort -rn | head -20
grep -oiE "\b(sphere|spherical|ball|disc|disk|cube|tote|cylinder|torus|ring|tube|cone|hexagon)[a-z]*\b" /tmp/bio.txt | sort | uniq -c | sort -rn
grep -oiE "weigh[st]? (approximately |about |roughly )?[0-9.]+ ?(oz|ounce|lb|pound|g|gram)" /tmp/bio.txt | sort -u

# ---- 2. ELEVATION: is vertical reach scored at all, and how high? -------------------------------
grep -oiE "[0-9]+ ?(ft|feet|in|inches|\") (above|from) the (floor|carpet|FIELD)" /tmp/bio.txt | sort -u
grep -oiE "(HEIGHT|EXTENSION) (LIMIT|CONSTRAINT)[^.]{0,200}" /tmp/bio.txt | head -5
grep -oiE "may not extend more than [0-9]+ ?(in|inches|\")[^.]{0,120}" /tmp/bio.txt | sort -u   # frame perimeter extension rule

# ---- 3. CAPACITY: does a hopper/indexer pay for itself? ----------------------------------------
grep -oiE "may not (simultaneously )?CONTROL more than [0-9]+ [A-Z]+" /tmp/bio.txt | sort -u
#   output present  -> low cap  -> single-piece gripper, NO indexer.  See Sec 5.1.
#   no output       -> uncapped -> hopper + indexer + roller tower.   See Sec 5.2.

# ---- 4. ENDGAME: is there a climb, and does it need a telescope? --------------------------------
grep -oiE "(CLIMB|HANG|ASCEND|PARK|ONSTAGE|CAGE|CHAIN|RUNG|DEEP CAGE|SHALLOW)[A-Z]*[^.]{0,160}" /tmp/bio.txt | sort -u | head -15

# ---- 5. one-line decision -----------------------------------------------------------------------
echo "class -> Sec 1 table -> pick roller row (Sec 2) + architecture row (Sec 4) + lift row (Sec 7)"
```

**Read the output in this order:** step 1 (class), step 3 (capacity — decides indexer yes/no), step 2
(height — decides elevator vs arm vs neither), step 4 (climber). By 12:15 p.m. you should be able to
name a row in §1, a row in §2, a row in §4 and a row in §7. That is your whole mechanism BOM.

---

## 1. The fork: game-piece class → mechanism family

BIOCORE's element is unnamed and unspecified as of 2026-08-22. The one public hint is the AndyMark
pre-order structure — Kit-of-Parts quantity **$70.00**, 1/5-of-a-field quantity **$169.00**, "custom
item manufactured overseas" — which is a *pricing/packaging* pattern consistent with **many small
elements per field** rather than a few large ones. That is **[S] SPECULATION**, not fact
([`00_PREMISE_CORRECTION.md`](../../research/00_PREMISE_CORRECTION.md)).

| Class | Prior-season instances | Diameter / size | Intake that wins | Lift that wins | Small-team verdict |
|---|---|---|---|---|---|
| **(a) small ball, ~3–7 in.** | RAPD Cargo (9.5 in. — large), INFR Power Cell (7 in.), STMP Fuel (5 in.), 2014 (24 in. — large) | 3–7 in. sphere | Horizontal roller, over-the-bumper, 2 in. compliant wheels on 1/2 hex | Usually **none** — shoot instead | **Best case.** Cheapest, most forgiving, most COTS |
| **(b) large ball, > 8 in.** | RAPD Cargo 9.5 in., 2014 Ball 24 in., 2016 Boulder 10 in. | 8–24 in. sphere | Wide roller + polycord bridge, or scoop | Rare | Moderate. Roller width drives cost |
| **(c) flat / disc** | REB (2026) elements¹, 2013 Frisbee, 2012 Basketball² | thin, planar | Sticky roller pair or side-grip belt; **hardest to singulate** | Elevator or 4-bar | Hard. Ground pickup of flats is a machining problem |
| **(d) cube / tote / box** | PWUP Power Cube (13 in. cube), 2015 Tote/Container, CHRG Cube (9.5 in.) | 9–13 in. | Two opposed vertical roller arms ("claw-take") | Elevator (stack) or arm | Moderate. Very COTS-friendly; classic elevator game |
| **(e) ring / tube / cone** | CRES Note (14 in. torus), CHRG Cone, 2007/2011 tube games, DEEP Hatch Panel | 12–16 in. OD | Over-the-bumper roller that folds the ring; or passive V-funnel | Arm / 4-bar > elevator | Moderate. Rings are forgiving; cones are not |

¹ REB (2026) element geometry: read from the manual in `manuals/archive/frc/` before relying on it —
this pass did not re-derive it. **UNVERIFIED** as stated here.
² 2012 was a 29 in. basketball; listed only to show the historical size spread.

**The load-bearing generalisation [H]:** across 2016–2026, **every** game whose element was a
sub-8-inch sphere or a ring was solvable by a small team with a single-motor over-the-bumper compliant
roller and no custom machining. **Every** game whose element was a flat plate or a cone produced a
long tail of teams that never achieved reliable ground pickup. If §0 step 1 says *disc* or *cone*,
your risk went up and your first design review should be about pickup geometry, not about scoring.

---

## 2. Intake rollers — the wheel catalog

### 2.1 Compliant wheels (the default)

**Rule of thumb [H]:** softer durometer = more grip and more compliance, less RPM capability and less
life. For a hand-off/intake roller you want **30–40A**. For a shooter or a high-speed indexer you want
**50–60A**. Mixing durometers along one shaft (soft outboard, hard inboard) is a cheap way to get
centering for free.

| Vendor | Product | Diameter | Durometer options | Bore | Price each | Evidence |
|---|---|---|---|---|---|---|
| **AM** | Compliant Wheels | 2 in. | 35A / 40A / 50A / 60A | 1/2 hex, 3/8 hex, nub | **$6.20** | **[C]** |
| **AM** | Compliant Wheels | 2 1/4 in. | 35A / 40A / 50A / 60A | 1/2 hex, 3/8 hex, 5 mm hex | **$7.20** | **[C]** |
| **AM** | Compliant Wheels | 3 in. | 35A / 40A / 50A / 60A | 1/2 hex, 3/8 hex, 5 mm hex | **$8.40** | **[C]** |
| **AM** | Compliant Wheels | 4 in. | 35A / 40A / 50A / 60A | 1/2 hex, 3/8 hex, 5 mm hex, nub | **$11.00** | **[C]** |
| **REV** | ION Compliant Wheel | 2 in. | 30A / 40A / 60A | 1/2 hex (PK4), MAXSpline (PK10) | **$6.50** (pack price band) | **[C]** band; per-SKU **UNVERIFIED** |
| **REV** | ION Compliant Wheel | 3 in. | 30A / 40A | MAXSpline | **$18.00** (band top for 3 in.) | **[C]** band; per-SKU **UNVERIFIED** |
| **REV** | ION Compliant Wheel | 4 in. | 30A / 40A | MAXSpline | **$30.00** (band top) | **[C]** band; per-SKU **UNVERIFIED** |
| **WCP** | Straight Stretch-Core Flex Wheel | 1-5/8, 2, 3, 4 in. | 30A / 45A / 60A | 1/2 hex stretch (1-5/8, 2 in.); 1-1/4 round stretch (3, 4 in.) | from **$2.99** (CTRE) / from **$4.99** (wcproducts) | **[C]** entry price both retailers; per-variant **UNVERIFIED** |
| **WCP** | Straight **Solid-Core** Flex Wheel | as above | 30A / 45A / 60A | as above | **UNVERIFIED** | UNVERIFIED |
| **VEX** | Flex Wheel (VEXpro) | 1.625–4 in. | 30A / 40A / 60A | 1/2 hex, 1-1/8 round | **UNVERIFIED** (vexrobotics.com returned HTTP 403 to this pass) | UNVERIFIED |

**Verified WCP Flex Wheel SKUs** (from the CTRE listing, 2026-08-22) — 1/2 in. width, 1/2 in. hex
stretch bore: `WCP-1281` 1.625 in. 30A (**$2.99** **[C]**), `WCP-1282` 1.625 in. 45A, `WCP-1283`
1.625 in. 60A, `WCP-1284` 2 in. 30A, `WCP-1285` 2 in. 45A, `WCP-1286` 2 in. 60A. 1 in. width,
1-1/4 in. round stretch bore: `WCP-1358/1359/1360` = 3 in. 30A/45A/60A, `WCP-1361/1362/1363` = 4 in.
30A/45A/60A. **[C]** SKUs; only WCP-1281's price was published per-variant — the other eleven are
**UNVERIFIED** on price.

> **Note the price spread.** A 1-5/8 in. WCP flex wheel at $2.99 versus a 2 in. AndyMark compliant
> wheel at $6.20 is a >2× difference on a part you buy eight of. For a budget-limited team that is a
> real saving — but flex wheels use a *stretch* bore (the wheel is stretched onto an oversized hub),
> which is a different assembly method from a keyed hex bore. Do not mix the two ecosystems on one
> shaft without checking hub compatibility.
| **AM** | Compliant Stars | — | — | — | **UNVERIFIED** | UNVERIFIED |
| **AM** | SmoothGrip Wheels | — | — | — | **UNVERIFIED** | UNVERIFIED |

**Verified SKUs (REV ION, from the live variant list):** `REV-21-2029-PK4` (2 in. 30A, 1/2 hex),
`REV-21-2030-PK4` (2 in. 40A), `REV-21-2031-PK4` (2 in. 60A), `REV-21-6555-PK10` (2 in. 40A MAXSpline),
`REV-21-2452` (3 in. 30A MAXSpline), `REV-21-2456` (3 in. 40A), `REV-21-2453` (4 in. 30A),
`REV-21-2457` (4 in. 40A). **[C]** SKUs; the price *mapping* to each SKU is **UNVERIFIED** — the page
publishes an MSRP range of $6.50–$30.00 and does not break it out per variant in machine-readable form.

**Bore ecosystem warning — pick one and stay in it.** 1/2 in. hex is the FRC lingua franca and is
cross-compatible between AM, WCP, TTB and VEX. REV's **MAXSpline** and 3/8 hex are *not* 1/2 hex. A
15-student team that buys wheels in three bore standards will spend a Saturday making adapters. **Pick
1/2 in. hex** unless you are already committed to the REV MAXPlanetary/MAXSpline ecosystem for the
whole robot.

### 2.2 Cost model: a typical intake roller

| Line item | Qty | Unit | Extended | Evidence |
|---|---|---|---|---|
| AM 2 in. 35A compliant wheel, 1/2 hex | 8 | $6.20 | **$49.60** | **[C]** |
| 1/2 in. hex shaft, ~24 in. | 1 | UNVERIFIED | — | UNVERIFIED |
| 1/2 in. hex bearings (flanged, 1.125 OD) | 4 | UNVERIFIED | — | UNVERIFIED |
| Hex spacers / shaft collars | ~10 | UNVERIFIED | — | UNVERIFIED |
| Motor + controller (see `03_programming_stack.md`) | 1 | — | — | — |
| **Roller subtotal, wheels only** | | | **≈ $50** | **[C]** |

**Read that number.** A working intake roller's *wheel* cost is **under $60**. Intakes are not where a
small team's money goes. Elevators are (§7, §13).

### 2.3 Non-wheel roller surfaces

| Surface | What it is | Best for | Typical source | Price | Evidence |
|---|---|---|---|---|---|
| **Polycord / round belt** | urethane round belting, 1/8–3/16 in., welded to length | spanning wide gaps, ball transport, "bridge" between two roller shafts | MMC, WCP, AM | **UNVERIFIED** | UNVERIFIED |
| **Surgical tubing** | latex tubing stretched over a shaft or over pulleys | very grippy, very cheap, poor life | MMC, pharmacy supply | **UNVERIFIED** | UNVERIFIED |
| **Silicone tube over hex** | silicone tubing slid over 1/2 hex shaft | sticky roller at near-zero cost | MMC | **UNVERIFIED** | UNVERIFIED |
| **Mecanum / omni rollers** | angled rollers that translate a piece sideways while pulling it in | **singulating** and **centering** small balls, class (a) | AM, VEX | **UNVERIFIED** | UNVERIFIED |
| **Brush roller** | nylon strip brush wound on a core (vacuum-cleaner style) | picking flats and discs off carpet — class (c) — where wheels skid | MMC (strip brush), industrial supply | **UNVERIFIED** | UNVERIFIED |
| **Timing-belt-over-wheel** | HTD belt run around two pulleys, belt face is the grip surface | ring/tube class (e) side-grip; long-throw conveyors | WCP, REV, TTB, VEX | see §3 | — |

**[H] The 2016–2026 pattern:** compliant wheels dominate; polycord shows up on wide (>14 in.) intakes
to avoid buying 16 wheels; surgical tubing shows up on teams with no budget and is a *reliability*
liability (it work-hardens, glazes, and snaps mid-event). **Do not run surgical tubing on a mechanism
you cannot re-tube in under 4 minutes between matches.**

---

## 3. Rotary power transmission for manipulators

This is the boring section that determines whether your intake survives Saturday.

| Element | Standard | Where it wins | Where it fails | Evidence |
|---|---|---|---|---|
| **HTD 5 mm belt + pulley** | 9 mm / 15 mm wide belt, 5 mm pitch | quiet, no lube, tolerant of misalignment, easy CoG-friendly routing; the default for intakes and indexers 2019→2026 | needs correct centre distance (belts don't tension by link removal); skips under shock load if under-tensioned | **[H]** |
| **GT2 3 mm** | 3 mm pitch | tiny, light, low-torque indexer rollers | too weak for a driven intake shaft | **[H]** |
| **#25 chain** | 1/4 in. pitch roller chain | high torque, tensionable by half-links, cheap; the elevator standard | needs lube, sheds under-tension, noisy | **[H]** |
| **#35 chain** | 3/8 in. pitch | climbers and drivetrains | heavy and overkill for manipulators | **[H]** |
| **1/2 in. hex shaft** | 0.500 across flats | universal FRC bore; wheels/pulleys/sprockets all key to it | twists at high torque in long spans | **[H]** |
| **ThunderHex** | slightly oversized hex (WCP) | removes hex-slop; better for precision shafts | not interchangeable with plain hex in tight bores | **[H]** |
| **Flanged hex bearing** | 1.125 in. OD, 1/2 hex ID | the standard support; press into 1.125 in. hole | 1.125 in. hole requires a step drill or hole saw — see tooling floor §13 | **[H]** |

**Verified transmission parts (TTB, live page 2026-08-22):**

| Part | Price | Note | Evidence |
|---|---|---|---|
| QTY 2 — Half Inch Hex 22-Tooth #25 Sprocket | **$19.99** | elevator/roller drive | **[C]** |
| QTY 1 — #25 Chain Tensioner | **$14.99** | | **[C]** |
| QTY 1 — #25 Chain Attachment Part | **$22.99** | chain-to-carriage anchor | **[C]** |
| QTY 2 — Half Inch Hex Coupler | **$22.99** | joins two 1/2 hex shafts | **[C]** |
| QTY 10 — 0.75 in. OD × 0.25 in. ID × 0.280 in. radial ball bearing | **$20.00** | elevator bearing-block rollers | **[C]** |
| QTY 10 — 0.50 in. OD × 0.25 in. ID × 0.188 in. round radial bearing | **$20.00** | | **[C]** |
| Thrifty Dead Axle Tube Roller Kit | **$45.00** | roller that spins on a fixed axle through box tube | **[C]** |
| Thrifty Live Axle Tube Roller Kit | **$15.00** | roller driven by a through-shaft | **[C]** |

The **$15.00 Live Axle Tube Roller Kit** is the single highest-value line in this document for a small
team: it converts a length of 2×1 box tube you already own into a supported, driven roller with no
machining beyond drilling. Two of them plus $50 of compliant wheels is a complete intake.

---

## 4. Intake architectures

### 4.1 The four architectures

| # | Architecture | Description | COTS : fabricated | Tooling floor | Build hours (15-student team) | Top failure modes |
|---|---|---|---|---|---|---|
| **A1** | **Fixed, inside frame perimeter** | rollers live permanently inside the bumper envelope; piece must be driven into a funnel | 80 : 20 | drill press, hand tools | **8–14 h** | can't reach pieces against the wall; driver frustration; funnel jams |
| **A2** | **Over-the-bumper (OTB), fixed** | roller cantilevered above and outside the bumper, always deployed | 70 : 30 | drill press + band saw; 1.125 in. hole saw | **14–24 h** | **bumper-height rule violation**; roller struck in collisions; long unsupported shaft twists |
| **A3** | **Over-the-bumper, deploying / pivoting** | roller stows inside perimeter, pivots out on a pneumatic cylinder or motor | 55 : 45 | + tapping, + 1/4 in. plate work | **28–45 h** | pivot hardstop fatigue; cylinder mount tears out; deploy timing bugs; **the classic small-team hour sink after the elevator** |
| **A4** | **Under-the-bumper (UTB)** | piece passes *beneath* the bumper into the robot | 45 : 55 | + precise floor-clearance machining, often a router or mill | **30–50 h** | ground clearance vs. field seams; piece wedges under bumper; nearly unrecoverable if the class turns out to be big |

**Small-team recommendation [H]:** build **A2** unless the frame-perimeter extension rule (§0 step 2)
makes it illegal, in which case build **A3**. A2 is the highest reliability-per-hour architecture in
the 2016–2026 record. Skip A4 entirely — a UTB intake is a machining-capability bet, and a
15-student team with a drill press loses that bet.

### 4.2 COTS-vs-fabricated split, in plain terms

- **Always COTS:** wheels, bearings, belts/chain, sprockets/pulleys, shaft, gearboxes, motors,
  pneumatic cylinders, springs. Buying these is not "cheating"; it is what the hours are for.
- **Always fabricated (by you):** the two side plates that set your roller centre distances and your
  pivot geometry. There is no COTS part for "my robot's specific geometry".
- **The lever:** if your side plates are **2D profiles cut from 1/4 in. or 1/8 in. aluminum plate**,
  you can have them cut by a sponsor, a local waterjet, or a hobbyist CNC router in a week. If they
  require **3D machining**, you have a project instead of a part. Design every manipulator plate as a
  flat 2D profile. This single constraint is worth more than any part in this file.

### 4.3 Pneumatics vs motors for deployment

| | Pneumatic cylinder deploy | Motor deploy (with hard stops) |
|---|---|---|
| Weight | compressor + tank + regulator ≈ several lb | one small motor |
| Speed | fast, binary | tunable, can be slow |
| Positions | 2 (unless you buy more valves) | continuous |
| Failure mode | leaks; you *will* have a leak at an event | current-limit tuning; back-drive |
| Small-team verdict | **[H]** only worth it if you already run pneumatics for something else. Otherwise the compressor's weight and the leak-hunting hours are pure cost | **Preferred** for a first mechanism |

**2027 caveat:** the legal pneumatic component list and the legal motor list are re-published every
season in the manual. **Do not buy either until you have read the 2027 manual's `R` rules.** Prior-season
lists are **[H]**, not **[C]**, for 2027.

---

## 5. Indexers, conveyors, hoppers, singulators

### 5.1 If §0 step 3 finds a possession cap of 1–2

**Do not build an indexer.** Build a gripper (§6) and spend the hours on the lift. Across 2016–2026,
low-capacity games (CHRG, REEF, DEEP, PWUP) rewarded *positional accuracy*; high-capacity games
(STMP, INFR, RAPD) rewarded *throughput*. Building a throughput mechanism in an accuracy game is the
most expensive single strategic error available to a small team.

### 5.2 If uncapped, the standard stack

| Stage | Function | Typical construction | COTS content | Failure mode |
|---|---|---|---|---|
| **Hopper** | hold N pieces loosely | polycarbonate walls + a floor | high (sheet + rivets) | bridging/arching of pieces; needs an agitator |
| **Singulator** | present exactly one piece at a time | a narrow gate + a counter-rotating roller, or mecanum rollers | medium | **the hardest sub-problem in the whole robot**; jams here kill cycles |
| **Indexer / tower** | queue pieces vertically | stacked 1/2 hex roller shafts belted together, or a polycord tower | high | belt skip; pieces "double up" |
| **Conveyor** | transport horizontally | HTD belt or polycord loop | high | tracking (belt walks off pulleys) — needs a crowned or flanged pulley |
| **Feeder** | hand off to shooter/scorer | one compliant wheel pair at higher speed | high | pre-spinning the piece and losing shot repeatability |

**[H] Rule for small teams:** every additional stage is a new jam location. A **two-stage** path
(intake → single roller tower → score) is achievable in a 6-week build. A **four-stage** path
(intake → hopper → singulator → indexer → shooter) is a 200-hour project and needs a dedicated
sub-team. If you have 15 students total, you do not have a dedicated sub-team.

### 5.3 The single-motor trick

Belting the intake roller, the tower rollers and the feeder to **one** motor with HTD belt costs you
tuning flexibility and gains you: one motor, one controller, one CAN node, one current limit, one
failure mode, and a mechanism that cannot get out of sync. **[H]** This is a recurring pattern in
successful low-resource robots and it is nearly free.

---

## 6. Grippers and end effectors

| Type | How it works | Actuation | Holding under power loss | Fab burden | Best classes |
|---|---|---|---|---|---|
| **Roller "claw-take"** | two opposed powered rollers pinch the piece | 1 motor | none — piece drops | low | (a) (d) (e) |
| **Motorized claw** | two jaws driven by a geared motor, closed under current limit | 1 motor + gearbox | holds while current-limited; drops on disable | medium | (c) (d) |
| **Pneumatic claw** | double-acting cylinder drives jaws | 1 cylinder + solenoid | holds if you use a **single-acting spring-closed** cylinder or a check valve | medium | (c) (d) |
| **Passive over-center grabber** | spring-loaded jaws snap over the piece; released by a small actuator or by driving away | spring; release by 1 small motor/cylinder | **holds with zero power** | medium-high (geometry-sensitive) | (e) (d) |
| **Passive funnel / V-scoop** | pure geometry — drive at the piece and it wedges in | **none** | holds by geometry | **lowest** | (a) (e) |
| **Suction / vacuum** | vacuum cup on a plate | pump | fails on disable | high, and pumps are usually **not legal** | (c) |

**Small-team ranking [H]:** passive funnel > roller claw-take > motorized claw > pneumatic claw >
over-center > vacuum. Every step to the right buys precision with hours you probably don't have.

**Over-center grabbers deserve a note.** A well-designed passive over-center gripper is the only end
effector that holds a game piece through a brownout, a disable, and a match-ending power loss. On
elevation mechanisms this matters more than it sounds: dropping the piece at the top of a 5-foot
elevator during a brownout is a lost cycle *and* a field hazard. Their cost is that the geometry is
sensitive — expect two or three iterations, which is exactly why they belong in an off-season
prototype (now, August 2026), not in week 3 of build season.

---

## 7. Elevators — kits, rigging, and the ratio math

> **This is the section that decides your season.** See §13: elevators are the classic small-team
> schedule killer, and the failure is almost never "we couldn't afford it" — it is "we spent
> weeks 3, 4 and 5 on it and never got to practise driving."

### 7.1 Verified elevator kits (live prices, 2026-08-22)

| Vendor | Product | SKU | Price | Stages | Drive | You must also supply | Evidence |
|---|---|---|---|---|---|---|---|
| **WCP** | GreyT Cascade Elevator | — | **$299.99** | single / 2 / 3 configurable (CAD provided) | **single #25 chain**, spur gearbox, multi-motor support, bearings on all surfaces | motors, tube, mounting | **[C]** price; stage/travel spec **UNVERIFIED** |
| **WCP** | Kit: GreyT Elevator (Cascade, First Stage) | **KIT-0048** | **$324.99** | first stage | as above | motors, tube, mounting | **[C]** price + SKU; contents list **UNVERIFIED** |
| **WCP** | Greyt Universal Elevator v2 | **WCP-0223** | **discontinued / sold out** | 2 | double-chain cascade | — | **[C]** (as discontinued) |
| **TTB** | Thrifty Elevator Stage Kit — **1 stage** | — | **$389.00** | 1 | #25H chain + Dyneema, CAM tensioner | **2×1 in. box tube, hex shaft, fasteners, gearbox** | **[C]** |
| **TTB** | Thrifty Elevator Stage Kit — **2 stage** | — | **$599.99** | 2 | as above | as above | **[C]** |
| **REV** | (MAXTube / ION elevator ecosystem) | — | **UNVERIFIED** | — | — | — | UNVERIFIED |
| **CTRE** | resells WCP GreyT Cascade Elevator | — | **UNVERIFIED** (separate listing exists) | — | — | — | UNVERIFIED |

**TTB kit contents, verified:**

- **1-stage $389.00** = 1× Sliding Elevator Bearing Block Kit + 1× Elevator #25 Chain Drive Kit +
  1× Constant Force Spring Kit + 1× Elevator Gusset Kit. **[C]**
- **2-stage $599.99** = 2× Bearing Block Kit + 1× #25 Chain Drive Kit + **2× Elevator Dyneema Pulley
  Kit** + 1× Constant Force Spring Kit + 1× Gusset Kit. **[C]**
- Compatible with "the various brands of 2 in. × 1 in. aluminum box extrusion", any wall thickness. **[C]**

**TTB à-la-carte (build it up yourself):** Sliding Elevator Bearing Block Kit **$99.99** · Elevator #25H
Chain Drive Kit **$199.99** · Elevator Dyneema Pulley Kit **$59.99** · Constant Force Spring Kit
**$49.99** · Elevator Gusset Kit **$39.99** · Thrifty Top Elevator Bearing Plate **$10.99** · Thrifty
Planetary Mount Plate **$10.99** · V1 Bearing Block Shoulder Bolt ×8 **$12.99** · 1/8 in. Dyneema Rope,
25 ft **$10.99**. All **[C]**.

**Buy-vs-build note:** 1× each of the five à-la-carte kits = $99.99 + $199.99 + $59.99 + $49.99 +
$39.99 = **$449.95**, versus **$389.00** for the assembled 1-stage kit. The bundle is cheaper. **[C]**
(arithmetic on verified prices).

### 7.2 Cascade vs. continuous rigging — definitions and the math

Terminology in the FRC community has drifted, so define by *behaviour*, not by name, and let physics
arbitrate. Let there be **N** moving stages, each with per-stage stroke **s**, and let the drum pay out
rope (or chain) at linear speed **v_d** with tension **T**. Let **W** be the total lifted weight
(carriage + game piece + the mass of every stage above the one being considered).

**Cascade rigging — stages move *simultaneously and proportionally*.**

- Stage 1 rises at `v_d`; stage 2 at `2·v_d`; … carriage (top of stage N) at `N·v_d`.
- Total travel `H = N·s`.
- **Energy conservation** (frictionless): `T·v_d = W·v_carriage = W·N·v_d`  ⟹  **`T = N·W`**.
- Drum torque `τ = T·r = N·W·r`.
- **Consequence:** a 3-stage cascade is **3× faster** and needs **3× the torque** of a single stage.
  It also multiplies rope stretch and backlash by N, so position control gets harder as N grows.

**Continuous ("sequential") rigging — stages extend one after another.**

- Whichever stage is currently moving rises at `v_d`. Carriage top speed is `v_d`.
- Total travel `H = N·s` (same as cascade).
- `T = W`, `τ = W·r`. **1/N the torque, 1/N the speed.**
- **Consequence:** lower torque and simpler rigging, but there is a mechanical hand-off ("clunk") each
  time the next stage picks up, and the centre of gravity rises in steps rather than smoothly.

**[S] Terminology caution:** some vendors and whitepapers use "continuous rigging" to mean a single
continuous rope loop that drives the carriage positively in *both* directions (as opposed to relying on
gravity for retraction). That is a different axis entirely — *bidirectional drive* vs *gravity return* —
and both cascade and sequential elevators can be built either way. When reading a vendor page, ask two
separate questions: **(1) do the stages move together or in sequence?** and **(2) is the down-stroke
driven or gravity-fed?** The physics above depends only on (1).

### 7.3 The gear-ratio worksheet

Given: target carriage travel `H`, target time `t`, lifted weight `W`, drum radius `r`, motor count `n_m`.

```
v_carriage      = H / t                                   [in/s]
v_drum          = v_carriage / N        (cascade)          [in/s]     N = stage count
                = v_carriage            (sequential)
ω_drum          = v_drum / r                               [rad/s]
τ_drum_required = N · W · r             (cascade)           [in·lb]
                = W · r                 (sequential)
τ_motor_avail   = n_m · τ_stall · η_eff / G                 G = gearbox reduction
```

Design so that `τ_drum_required ≤ 0.4 · n_m · τ_stall / G` — i.e. **size the ratio to hold at ≤40 % of
stall torque**, not at stall. **[H]** This is the single most-repeated FRC elevator lesson: elevators
are sized by *holding* and *acceleration*, not by steady-state lift. An elevator that just barely lifts
its load will brown out the robot on every up-stroke and will sag whenever the piece is heavier than
you modelled.

**Then subtract the counterbalance.** A TTB Constant Force Spring Kit provides a **16.5 lb** constant
upward force over **50 in. of travel** (**[C]**). If your carriage assembly weighs 20 lb, one spring
kit removes 82 % of the static load from the motor. Two kits over-balance it. See §10.

**Verify with the repo's model:** `tools/cycle-model.py` exists in this project and should be pointed at
whatever cycle time your elevator produces before you commit to the design. **UNVERIFIED** whether it
currently accepts an elevator parameter set — read the script's `--help` first.

### 7.4 Motor spec table (for the worksheet)

**UNVERIFIED for 2027.** Prior-season nominal figures **[H]**: Kraken X60 ≈ 7.09 N·m stall / 6000 RPM
free · Falcon 500 ≈ 4.69 N·m / 6380 RPM · NEO Vortex ≈ 3.60 N·m / 6784 RPM · NEO 1.1 ≈ 2.6 N·m /
5676 RPM · CIM ≈ 2.41 N·m / 5330 RPM. **The 2027 manual's `R` rules define the legal motor list, and
Systemcore changes the controller side. Re-verify every one of these numbers against the vendor page
and the 2027 manual before using them in a calculation.**

---

## 8. Linear motion hardware

| Option | What it is | Pros | Cons | Price | Evidence |
|---|---|---|---|---|---|
| **Bearing block on box tube** (the FRC standard) | 3 or 4 small radial bearings in an aluminum block riding the flats of 2×1 tube | cheap, serviceable, tolerant of dirt, COTS | needs shimming; wears the tube over a season | TTB Sliding Elevator Bearing Block Kit **$99.99** | **[C]** |
| **Bearings direct on tube edges** | bearings ride the *corners* of the tube | fewest parts | point-loads the tube; galls | — | **[H]** |
| **UHMW / Delrin slide pads** | plastic pads sliding on aluminum | silent, zero backlash, no bearings to fall out | friction rises with load; needs periodic replacement; **not** for high-cycle | MMC sheet, **UNVERIFIED** | UNVERIFIED |
| **igus DryLin rail + carriage** | polymer plain-bearing linear rail | precise, low-profile, self-lubricating | expensive; rail must be well supported; not an FRC-native ecosystem | **UNVERIFIED** | UNVERIFIED |
| **Telescoping tube set** | nested 2 → 1.5 → 1 in. tubes with internal bearings | complete solution incl. constant-force return | fixed geometry | TTB Thrifty Telescoping Tube Kit: base **$140.00**, 2nd stage **$140.00**, base+2nd **$220.00** | **[C]** |

**Bearing-block kit contents, verified** (TTB Sliding Elevator Bearing Block Kit, **$99.99**, covers
"one stage of a sliding 2 in. × 1 in. box extrusion elevator") **[C]**:

| Item | Qty |
|---|---|
| Sliding Bearing Block Plate (2024 update) | 4 |
| 0.50 OD × 0.25 ID × 0.188 W bearing | 8 |
| 0.75 OD × 0.25 ID × 0.280 W bearing | 8 |
| 1/4 in. dia. × 1.75 in. steel dowel | 4 |
| Bearing Block Shoulder Bolt Spacer | 8 |
| 1/4-20 × 1 in. button head bolt | 8 |
| 1/4-20 thin locknut | 8 |
| 10-32 × 5/8 in. button head screw | 16 |
| 10-32 thin locknut | 16 |
| 4 in. zip tie | 4 |

**16 bearings and 60 fasteners per stage.** That parts count is the real reason §13 puts a 1-stage
elevator at 22 build-hours: it is not one hard job, it is sixty small ones done accurately.

**Rigging hardware, verified:** TTB Elevator Dyneema Pulley Kit **$59.99** · 1/8 in. Dyneema rope, 25 ft
**$10.99** · Elevator #25H Chain Drive Kit **$199.99** · #25 Chain Attachment Part **$22.99** ·
#25 Chain Tensioner **$14.99**. All **[C]**.

**Dyneema vs chain for elevator rigging [H]:** Dyneema (UHMWPE) rope is lighter, quieter, and routes
around corners; it also **creeps** under sustained load and needs re-tensioning (hence the TTB "CAM
tensioning system"). #25 chain does not creep and is trivially tensionable by half-link, but is heavier
and must not be run over small-radius idlers. Small teams generally do better with **chain for the
drive and Dyneema only for the cascade tie-backs** — which is precisely the TTB 2-stage kit's
architecture (#25H chain drive + 2× Dyneema pulley kits).

**Telescoping tube kit constant-force detail (verified):** the TTB telescoping base stage includes two
constant-force springs, **39 in. long, 5.94 lb pull each**, plus eight 1/2 in. OD bearings, two
aluminum plates, and 25 ft of 1/8 in. Dyneema. **[C]**

---

## 9. Arms, pivots, and four-bars

### 9.1 Which topology is correct

| Topology | Geometry | Use when | Do **not** use when | Relative build cost |
|---|---|---|---|---|
| **Single-jointed arm** | one pivot, one link | you need two or three discrete heights and the end-effector angle may change with height | the piece must stay level (it won't) | **1.0×** (baseline) |
| **Virtual four-bar** | single-jointed arm **+** a belt/chain from a fixed ground pulley to the wrist, at 1:1 | you want a single-jointed arm *and* a level end effector — the belt keeps the wrist parallel to ground for free | you need the wrist to *also* be independently controlled | **1.2×** |
| **True four-bar** | two parallel links + coupler | you want the end effector to translate along an arc while staying level, and you want the load path split over two links | space is tight — a four-bar sweeps a big envelope | **1.6×** |
| **Double-jointed arm** | two powered pivots | you must reach *over* an obstacle, or reach both a low floor pickup and a high score with one mechanism | you have not written inverse-kinematics code before | **3.0×**, plus significant software risk |
| **Elevator + short wrist** | vertical translation + 1 pivot | the score locations are at very different heights and directly above the robot | horizontal reach matters more than vertical | **2.5×** |

**[H] The small-team ordering:** virtual four-bar > single-jointed arm > elevator + wrist > true
four-bar > double-jointed arm. The **virtual four-bar is the highest value-per-hour articulation in
FRC** for a resource-constrained team: it costs one extra belt and two pulleys over a plain arm and
gives you a level end effector through the whole sweep, which removes an entire class of scoring
failures.

### 9.2 Pivot hardware

| Part | Purpose | Notes | Evidence |
|---|---|---|---|
| **Large-bore ("thin section") bearing** | arm shoulder pivot carrying bending load | lets the arm pivot on a large-diameter bearing instead of a shaft; dramatically stiffer | **UNVERIFIED** pricing/SKUs; WCP, TTB, AM all list options |
| **Turntable bearing / lazy-susan** | full rotation about a vertical axis | heavy; almost never worth it for a small team | **UNVERIFIED** |
| **1/2 in. hex shaft + flanged bearings** | cheapest pivot | fine for light arms; **twists** and adds slop on long/heavy arms | **[H]** |
| **Dead-axle pivot** | fixed shaft, arm rotates on bearings around it | stiffer than live-axle; the correct default for arms | **[H]** |
| **Absolute encoder at the pivot** | position feedback that survives power cycles | **mandatory** for any gravity-loaded arm — a relative encoder means re-zeroing on every enable | **[H]**; see `03_programming_stack.md` |

**Design rule [H]:** put the encoder on the **joint**, not on the motor. Any backlash between motor and
joint becomes position error, and gravity-loaded arms make backlash visible instantly.

---

## 10. Holding position under gravity

This is where naive elevators and arms fail: they lift fine, then sag, oscillate, or fall on disable.

| Method | Part / mechanism | Holds when disabled? | Cost | Notes |
|---|---|---|---|---|
| **Brake mode** | motor controller setting | **No** — brake mode is *dynamic* braking; it resists motion but does not lock, and it does nothing once the robot is disabled and the controller unpowered | free | Necessary but never sufficient |
| **Gravity feedforward** | `kG` term in the controller | No | free (software) | The correct baseline: hold with a constant feedforward, not with integral windup |
| **High reduction / self-locking** | worm gear or very high ratio | Yes (worm), partly (high ratio) | varies | Worm drives are heavy and inefficient; high ratios are slow |
| **Ratchet** | pawl on a gear or drum | **Yes, one direction** | see §11 | The correct answer for a **climber**; wrong for a mechanism that must go back down |
| **Constant-force spring** | TTB Constant Force Spring Kit — **16.5 lb**, **50 in. travel**, 2 aluminum brackets + spool + retainers + hardware, **$49.99**, 0.60 lb kit weight; TTB recommends **1–2 kits per elevator** | Partially — it offsets weight so the elevator doesn't slam down | **$49.99** **[C]** | **Highest-value safety part in this document.** Also the most dangerous to handle — see §14 |
| **Constant-force spring (telescoping)** | in TTB Telescoping Tube Kit — **39 in. long, 5.94 lb pull**, 2 per stage | Partially | included in $140.00 kit **[C]** | |
| **Gas spring / gas strut** | nitrogen-charged strut, sized by force and stroke | Partially, and non-linearly | **UNVERIFIED** (MMC and automotive suppliers) | Force varies over stroke, unlike a constant-force spring — model it |
| **Counterweight** | dead mass on a rope over a pulley | Yes | weight budget | Almost never worth the weight in FRC |
| **Surgical tubing / extension spring** | elastic assist | Partially | cheap | Force grows with extension — exactly backwards for an elevator; use only for short strokes |

**Counterbalance sizing [H]:** target **80–95 % static offset**, not 100 %. A perfectly balanced
elevator drifts unpredictably; a slightly under-balanced one always settles down, which is the
predictable and safe failure direction. With a 20 lb carriage, one 16.5 lb constant-force kit gives
82.5 % — which is why "one kit per elevator" is TTB's own recommendation and why a second kit is a
decision, not a default.

---

## 11. Climbers

**Do not design a climber before §0 step 4 tells you a climb exists.** Endgame mechanics changed
shape every season 2016–2026 (bar hang, rung traverse, cage grab, ramp park, buddy climb).

### 11.1 Verified climber COTS (live, 2026-08-22)

| Part | SKU | Price | Travel | Included | Evidence |
|---|---|---|---|---|---|
| AM Climber in a Box — **with** extrusion, 1 stage | **am-4667** | **$195.00** | 24.5 in. | 1.5×1.5×0.062 + 1.0×1.0×0.062 tube; **no motor/gearbox** | **[C]** |
| AM Climber in a Box — with extrusion, 2 stage | **am-4668** | **$277.00** | 24.5 in./stage, **49 in. total** | 2×2, 1.5×1.5, 1×1 tube; **no motor/gearbox** | **[C]** |
| AM Climber in a Box — **without** extrusion, 1 stage | **am-4677** | **$144.00** | 24.5 in. | no tube, no motor, no gearbox | **[C]** |
| AM Climber in a Box — without extrusion, 2 stage | **am-4678** | **$214.00** | 49 in. total | no tube, no motor, no gearbox | **[C]** |
| AM Climber in a Box Winch Kit (1.5×1.5 extrusion) | **am-4663** | **$66.00** | — | winch for your own planetary gearbox; **no ratchet** | **[C]** |
| AM Climber in a Box Winch Kit (2×2 extrusion) | **am-4664** | **$72.00** | — | as above; **no ratchet** | **[C]** |
| AM Climber in a Box Hook Kit / Swappable Hook Kit | — | **UNVERIFIED** | — | 2026 version ships two hook styles | **[C]** for the two-style claim; price UNVERIFIED |
| AM Climber in a Box Bearing Kits / Brace Upgrade Kits | — | **UNVERIFIED** | — | — | UNVERIFIED |
| TTB Thrifty Telescoping Tube Kit (base) | — | **$140.00** | — | 2 constant-force springs (39 in., 5.94 lb), 8 bearings, 25 ft Dyneema | **[C]** |
| AM **Ratchet Sport** — Ratchet Only | **am-4424** | **$44.00–$110.00** range across the five configs | — | "works with the Sport gearboxes to control back drive" | **[C]** SKUs + range; per-SKU price **UNVERIFIED** |
| AM Ratchet Sport — Pneumatic Actuator Only | **am-4425** | (in range above) | — | — | **[C]** SKU |
| AM Ratchet Sport — Ratchet **with** Pneumatic Actuator | **am-4426** | (in range above) | — | releasable under load via a small air cylinder | **[C]** SKU |
| AM Ratchet Sport — Servo Actuator Only | **am-5408** | (in range above) | — | — | **[C]** SKU |
| AM Ratchet Sport — Ratchet **with** Servo Actuator | **am-5409** | (in range above) | — | releasable under load via servo | **[C]** SKU |
| WCP **Ratchet Plate** (gearbox accessory) | — | **UNVERIFIED** | — | — | UNVERIFIED |

**Why the Ratchet Sport matters:** AndyMark's own description says it "can be added to an already
installed gearbox without changing the motor" and that it "can release under load" when actuated by a
small air cylinder or servo. **[C]** That is exactly the property a climber needs — hold the robot's
full weight with the motor unpowered, then release deliberately. A ratchet you cannot release under
load turns a failed climb into a stuck robot. If you buy a ratchet, buy an **actuated** one
(am-4426 or am-5409), not the bare am-4424.

**AM's own claim, verified:** Climber in a Box is "an unassembled kit of everything you need (excluding
gearmotor)" designed to "require no precision machining". **[C]** That claim is the entire reason a
15-student team should buy it rather than build one: it converts a machining problem into an assembly
problem.

### 11.2 The four climber sub-problems

1. **Extension** — telescoping tubes (COTS above) or a pivoting arm. Constant-force springs *extend*
   the tubes; the winch *retracts* them and thereby lifts the robot.
2. **Latching** — a hook that engages the field element. Passive hooks that self-engage when the tube
   extends are far more reliable than actuated hooks. **[H]**
3. **Winching** — a drum with rope. **Dyneema 1/8 in.** is the standard (TTB sells 25 ft for
   **$10.99** **[C]**). Wind the drum in a single layer if you can; multi-layer winding changes the
   effective radius and therefore your gear ratio mid-climb.
4. **Holding** — a **ratchet**, not brake mode. A climber that must hold the robot's full weight for
   the last 10 seconds of a match with the motor unpowered *requires* a mechanical one-way device.
   Note the verified fact above: **the AM Climber-in-a-Box winch kits do not include a ratchet.** You
   must add one. **AM Ratchet Sport** is the verified option: `am-4426` (ratchet + pneumatic actuator)
   or `am-5409` (ratchet + servo actuator), within a published range of **$44.00–$110.00**. **[C]**
   A WCP ratchet plate and a REV MAXPlanetary ratchet stage also exist but are **UNVERIFIED** here.

**Budget check:** a complete two-stage COTS climber = am-4678 ($214.00) + am-4664 ($72.00) + a
gearbox/motor + a ratchet + Dyneema ($10.99) ≈ **$300 in COTS before the powertrain**. **[C]** on the
quoted lines; total is arithmetic on those.

---

## 12. 3D printing on a 2026-era FRC robot

**What actually survives, and where each material fails.** All **[H]** — from the community's
accumulated practice, not from a BIOCORE source.

| Material | Survives | Fails at | Correct FRC uses | Wrong FRC uses |
|---|---|---|---|---|
| **PLA / PLA+** | dry, room-temperature, low-impact parts | **heat** (a robot in a hot venue or a part near a motor will creep and sag); brittle fracture on impact | prototypes, bumper-number templates, camera mounts, sensor brackets, wire guides, non-structural spacers | anything load-bearing, anything near a motor, any gripper jaw that takes impact |
| **PETG** | moderate heat, moderate impact, outdoors | layer-adhesion in Z under tension; creeps under sustained load | funnels, chutes, hoppers, light covers, ball guides, non-critical brackets | pivots, gears, anything holding a spring load |
| **ABS/ASA** | heat better than PETG | warping during printing; needs an enclosure | motor shrouds | fine-detail parts |
| **Nylon (PA6/PA12)** | impact, abrasion, flexure | **moisture absorption** — it goes soft and dimensionally unstable if not dried; hard to print | living hinges, wear surfaces, gripper pads | dimensional precision parts |
| **Nylon-CF (PA-CF)** | impact + stiffness + heat; the best general-purpose FRC filament | needs hardened nozzle, dry filament, and a capable printer; expensive; still not aluminum | **gears, pulleys, sprockets, roller cores, gripper jaws, structural brackets** | replacing a machined pivot in the main load path |
| **Onyx (Markforged)** | as Nylon-CF, with excellent surface finish; **continuous-fibre reinforcement** available on some machines | proprietary machine + filament; slow; expensive; you probably don't own one | structural brackets if a sponsor prints them | anything you need in 24 hours |
| **TPU** | huge elongation, abrasion | no stiffness at all | intake grip surfaces, bumper corner pads, cable strain relief | structure |

**The three failure modes that actually happen at competition [H]:**

1. **Heat creep near a motor.** A PLA bracket 2 in. from a hard-working motor will deform on Saturday
   and not on Thursday. If a printed part is within a hand's width of a motor, print it in
   Nylon-CF or make it from aluminum.
2. **Layer separation in tension.** Printed parts are strong across layers and weak between them.
   **Orient every printed part so the primary load is in-plane, never peeling layers apart.**
3. **Set screws and threads in plastic.** Threads tapped directly into plastic strip. Use heat-set
   brass inserts (a $20 soldering-iron tip and a $15 bag of inserts) or a through-bolt and nut.

**The small-team rule:** print **fixtures, guides, prototypes and enclosures**; machine or buy
**anything in the load path**. A 3D printer is a prototyping accelerator, not a machine-shop
replacement — and in the 6 weeks between kickoff and bag/ship, its highest-value output is the
*cardboard-aided-design successor*: a same-day physical mock-up of the game piece interface, printed
Friday night and tested Saturday morning.

---

## 13. Build hours and tooling floor, by mechanism class

Hours below are **team-hours for a ~15-student team with an experienced mentor**, from first CAD to a
mechanism that works reliably three matches in a row. They assume the *first* time your team builds
that mechanism class. Halve them for a repeat build. **[H]** — calibrated against the small-team
patterns in [`reference/04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md), not measured here.

| Mechanism | Minimum tooling | Nice-to-have | Design h | Build h | Debug/tune h | **Total h** | Schedule risk |
|---|---|---|---|---|---|---|---|
| Fixed roller intake (A1) | drill press, hacksaw, hand tools, rivet gun | band saw, 1.125 in. hole saw | 4 | 6 | 4 | **14** | Low |
| OTB fixed intake (A2) | + band saw, + step drill | drill press vise, tap set | 6 | 10 | 6 | **22** | Low |
| OTB deploying intake (A3) | + tapping, + 1/4 in. plate cutting | CNC router / waterjet sponsor | 10 | 20 | 12 | **42** | **Medium-high** |
| UTB intake (A4) | + precise plate work | mill or CNC router | 14 | 24 | 14 | **52** | **High — skip** |
| Roller tower / indexer (2 stage) | drill press, band saw | 3D printer for guides | 6 | 12 | 10 | **28** | Medium |
| Hopper + singulator | + sheet bending, polycarb work | — | 12 | 20 | **24** | **56** | **High** |
| Passive funnel gripper | hand tools | 3D printer | 2 | 4 | 3 | **9** | Very low |
| Roller claw-take gripper | drill press | — | 4 | 6 | 5 | **15** | Low |
| Motorized claw | + tapping, plate work | absolute encoder | 8 | 12 | 10 | **30** | Medium |
| Single-jointed arm | drill press, band saw, tapping | plate cutting, absolute encoder | 8 | 14 | 14 | **36** | Medium |
| **Virtual four-bar** | as arm + belt/pulley | as arm | 10 | 16 | 14 | **40** | Medium |
| True four-bar | as arm | — | 12 | 18 | 16 | **46** | Medium-high |
| Double-jointed arm | as arm | strong software team | 20 | 24 | **36** | **80** | **Very high** |
| **Elevator, 1 stage, COTS kit** | drill press, band saw, **tube square-cutting**, tapping | chop saw, plate cutting | 10 | **22** | **20** | **52** | **High** |
| **Elevator, 2 stage, COTS kit** | as above + patience | as above | 14 | **32** | **28** | **74** | **Very high** |
| Elevator, fabricated from scratch | mill or CNC + all above | — | 24 | 60 | 40 | **124** | **Do not** |
| Climber, COTS kit (Climber in a Box) | drill press, hand tools | — | 6 | 14 | 10 | **30** | Medium |
| Climber, custom telescoping | + plate work, + tube machining | mill | 16 | 30 | 24 | **70** | High |

### 13.1 Why elevators are the small-team schedule killer

Read the elevator rows against the intake rows. A 2-stage elevator is **74 hours** — more than three
intakes. And the hours are back-loaded into *debug/tune*, which is exactly the phase that collides
with the last two weeks of build season, driver practice, and the awards submissions
([`reference/awards/01_AWARD_WINNING_PATTERNS.md`](../awards/01_AWARD_WINNING_PATTERNS.md)).

Five specific reasons elevators eat schedule, all **[H]**:

1. **They are unforgiving of squareness.** Two lengths of 2×1 tube cut 1 mm out of square bind. A hand
   hacksaw does not produce square cuts. **The tooling floor for an elevator is a chop saw or a band
   saw with a fence — not a drill press.**
2. **They require iteration on tension.** Chain and Dyneema both need retensioning after the first few
   dozen cycles. That is a second and third build session you did not schedule.
3. **They need position control, which needs an absolute encoder, soft limits, gravity feedforward and
   a homing routine** — four software features that do not exist for a roller intake.
4. **They fail loudly.** A binding elevator jams the whole robot; a bad intake just misses pieces.
5. **They multiply weight high on the robot,** which then requires drivetrain and CG work you also did
   not schedule.

**The decision rule [H]:** if §0 step 2 shows scoring heights reachable by a **virtual four-bar** (~40 h)
or a fixed shooter (~0 h of elevation), take that path. Build an elevator only when the manual
*requires* travel that no arm can cover — typically when the highest and lowest score locations are
more than roughly 4 ft apart in height **and** both must be reached from a compact footprint.

---

## 14. SAFETY — stored energy is the top school-shop injury risk

**Elevators and springs store enough energy to break fingers and put fragments in eyes.** This section
is not boilerplate; it is the section a mentor should read aloud before the first constant-force spring
comes out of its bag.

### 14.1 Constant-force springs

A constant-force spring is a coil of hardened steel strip under permanent tension. The TTB kit's spring
delivers **16.5 lb over 50 in.** — that is roughly 68 ft·lb of stored work if fully extended. It is
also a **sharp-edged steel band that will uncoil violently** if it slips its spool.

**Handling rules — non-negotiable:**

1. **Safety glasses on everyone within reach, always**, including the person just watching.
2. **Never uncoil a constant-force spring by hand and let go.** Retain the free end mechanically at all
   times. Install with the spool captured in its bracket, never free-standing.
3. **Gloves for handling the strip.** The edges of the steel band are sharp and the strip is springy.
4. **One person installs; one person supervises.** No spring installation by a lone student.
5. **Never cut, drill, grind, or heat a constant-force spring.** It is hardened; it will shatter.
6. **A spring that has kinked or taken a set is scrap.** Do not straighten and reuse.
7. Store spare springs **coiled, in their packaging, in a labelled box** — not loose in a drawer.

### 14.2 Elevators

1. **Physically block the elevator before working on it.** A wooden block or a hard-stop pin in the
   frame, not "we'll hold it." Gravity plus a counterbalance spring means the carriage can move *up*
   as well as down when the drive is disengaged.
2. **Disconnect the battery and vent all pneumatic pressure before reaching into the travel path.**
3. **Never put a hand between the carriage and a hard stop** with the robot enabled. Treat the travel
   path as a machine guard zone.
4. **Declare and mark the pinch points.** Sprocket/chain nips and the top pulley are amputation-class
   hazards on a powered elevator. Guard them or tape-mark them.
5. **Test the first power-on with the elevator at the bottom, current-limited low, and everyone behind
   the drive team,** not clustered around the mechanism.
6. **Software must have soft limits and a homing routine before the first full-speed run.** A
   position-controlled elevator that homes wrong drives the carriage into a hard stop at full torque.
7. **Brake mode is not a safety device** and it does nothing when disabled. See §10.

### 14.3 Climbers, gas springs, pneumatics

1. A charged **gas spring** is a pressure vessel. Never cut, puncture, heat, or dispose of one in
   general waste; never disassemble one.
2. A robot hanging from a climber is a **suspended load**. Nobody underneath, ever, including in the
   pit. Support it before touching it.
3. **Vent pneumatics to zero** and confirm at the gauge before disconnecting any line.
4. **Dyneema under tension cuts.** Do not run a hand along a loaded rope; do not use rope as a handle.

### 14.4 Shop practice for the whole manipulation build

Safety glasses in the shop, always · no loose hair/sleeves/lanyards near rollers or sprockets · nobody
operates a power tool alone or without training sign-off · a powered mechanism gets a test that is
announced out loud before it runs · a mechanism that surprised you once gets guarded before it runs
again.

---

## 15. Validation / dry-run — check this file before you spend money

Run this **the week before kickoff (early January 2027)** and again the day you place the order.

```bash
# Run from the repository root.
cd reference/bom

# 1. Does the YAML parse and does every [C] row still carry a source URL?
python - <<'PY'
import yaml, sys
d = yaml.safe_load(open("parts_manipulation.yaml"))
bad = []
for cat, items in d.get("parts", {}).items():
    for p in items:
        if p.get("evidence") == "C" and not p.get("source"):
            bad.append((cat, p.get("name")))
        if p.get("price_usd") in (None, "") and p.get("evidence") == "C":
            bad.append((cat, p.get("name"), "no price"))
print("rows:", sum(len(v) for v in d["parts"].values()))
print("PROBLEMS:", bad if bad else "none")
PY
# EXPECTED OUTPUT as written 2026-08-22:
#   rows: 68
#   PROBLEMS: [('elevator_kits','Greyt Universal Elevator v2'), ('climbers','Ratchet Sport')]
# Those two are intentional: WCP-0223 is verified DISCONTINUED (no price exists), and AM's
# Ratchet Sport publishes only a $44.00-$110.00 range. They are listed under
# meta.expected_validator_exceptions in the YAML. ANY OTHER row appearing here is a real defect.

# 2. Re-check every price. Any diff > 10% means this file is stale.
python - <<'PY'
import yaml
d = yaml.safe_load(open("parts_manipulation.yaml"))
for cat, items in d["parts"].items():
    for p in items:
        if p.get("source"):
            print(f'{p.get("price_usd","?"):>10}  {p["name"][:52]:<54} {p["source"]}')
PY
# ...then open each URL and compare. Prices verified 2026-08-22; vendors re-price in
# Sept-Jan for the new season. EXPECT drift.

# 3. Arithmetic self-check on the two bundle claims in Sec 7.1 and Sec 11.
python -c "print('TTB a-la-carte:', 99.99+199.99+59.99+49.99+39.99, 'vs bundle 389.00')"
python -c "print('AM climber COTS:', 214.00+72.00+10.99)"
```

**Expected output of step 3 as written 2026-08-22:** `TTB a-la-carte: 449.95 vs bundle 389.00` and
`AM climber COTS: 296.99`. If those two lines change, someone edited a price without re-verifying it.

**Kickoff-day validation (2027-01-09, after §0):**

- [ ] §0 step 1 produced a game-piece class. Write it at the top of the whiteboard.
- [ ] §0 step 3 answered the capacity question. If capped → **no indexer** (§5.1).
- [ ] §0 step 2 produced a max scoring height. Compare against a virtual four-bar's reach *before*
      anyone says the word "elevator" (§13.1).
- [ ] §0 step 4 answered whether a climb exists. If no → delete §11 from the budget.
- [ ] Total build hours from §13 for your chosen set ≤ **your actual available hours**, computed as
      (students who show up) × (hours/week) × (weeks before your first event) × **0.6** for the
      inevitable losses. If it doesn't fit, cut the elevator first.
- [ ] Every part you are about to order has been re-priced today, not read from this file.

---

## Files written by this pass

| Path | What it is |
|---|---|
| [`reference/bom/02_MANIPULATION_ELEVATION.md`](02_MANIPULATION_ELEVATION.md) | this document |
| [`reference/bom/parts_manipulation.yaml`](parts_manipulation.yaml) | machine-readable SKU/price/evidence table, same data, consumable by a BOM roll-up |

No other file in the project was modified. Files marked DONE in the project README were read, not
rewritten.

---

## Known limitations

1. **BIOCORE's game piece is unknown.** Everything in §1 is a *decision tree*, not a prediction. The
   AndyMark pre-order pricing hint is **[S]**, and this document does not act on it.
2. **Prices are a snapshot of 2026-08-22 and will drift.** FRC vendors re-price between the off-season
   and kickoff, and several 2027-season products do not exist yet. Re-run §15 step 2 before ordering.
3. **Two vendor pages could not be read at all:** `vexrobotics.com/flex-wheels.html` returned
   **HTTP 403**, and `docs.wcproducts.com/greyt-elevator-cascade` returned **404** at the URL tried
   (so GreyT stage count, travel and motor requirement are **UNVERIFIED**). Both are marked
   UNVERIFIED above rather than filled in from memory.
4. **Three vendors publish price *ranges* rather than per-SKU prices**, and this pass did not resolve
   them: **REV ION compliant wheels** ($6.50–$30.00 across 8 verified SKUs), **AM Ratchet Sport**
   ($44.00–$110.00 across 5 verified SKUs), **WCP Straight Flex Wheels** (only WCP-1281 at $2.99 of 12
   verified SKUs). In all three cases the **SKUs are [C]** and the **per-SKU price is UNVERIFIED**.
   Resolving these means adding items to a cart, which this pass deliberately did not do.
5. **The two WCP flex-wheel retailers quote different entry prices** — $2.99 at CTRE, $4.99 at
   wcproducts.com. Both numbers are **[C]** for the page they came from. Which applies to *you*
   depends on which retailer and which variant; do not assume the lower one.
6. **No part numbers, prices, or URLs were invented.** Where a part is real but the price was not
   fetched (WCP Ratchet Plate, igus DryLin, polycord, surgical tubing, brush roller stock, mecanum
   rollers, large-bore bearings, AM Compliant Stars, AM SmoothGrip, REV elevator ecosystem, Climber-
   in-a-Box hook/bearing/brace kits), the row says **UNVERIFIED** and gives no number.
7. **Build hours in §13 are [H] estimates**, calibrated against the small-team patterns in
   `04_PREDICTIVE_FACTORS.md`. They are not measured against this team's own history — if the team has
   a build log, replace these with real numbers and the whole §13 risk column gets sharper.
8. **Motor torque/speed figures in §7.4 are prior-season [H] values and are not re-verified.** The 2027
   legal motor list is published in the BIOCORE manual on 2027-01-09. Systemcore also changes the
   controller side of every mechanism here; see `reference/team-ops/03_programming_stack.md`.
9. **The cascade/continuous terminology in §7.2 is contested in the community.** The physics given is
   from first principles and is correct; the *names* attached to it vary by vendor. Judge a vendor kit
   by the two behavioural questions in §7.2, not by the word on the product page.
10. **Weight is not budgeted here.** Every mechanism in this file competes for the same robot weight
   allowance, whose 2027 value is unknown. A weight roll-up belongs in a separate pass.
11. **`tools/cycle-model.py` was not run against an elevator parameter set** in this pass; whether it
    accepts one is **UNVERIFIED**.
