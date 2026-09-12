# Drivetrain BOM — verified COTS options for BIOCORE (FRC 2027)

**Purpose:** give a ~15-student, budget-constrained team a priced, SKU-level drivetrain menu it can
order from **before** the 2027-01-09 BIOCORE kickoff, and one honest swerve-vs-tank decision table.
Every price here was fetched from a live vendor page on **2026-08-22**; anything that would not load
is marked `UNVERIFIED` rather than guessed. Drivetrain is the one subsystem you can commit to in the
fall, because — per the rule this project adopts verbatim — the choice has nothing to do with the game.

**Companion file:** [`parts_drivetrain.yaml`](parts_drivetrain.yaml) — machine-readable, one mapping
per SKU, same evidence labels. Re-verify script: [`recheck_prices.sh`](recheck_prices.sh).

**Upstream files this builds on (do not duplicate them, cite them):**
[`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) §3 (swerve-vs-tank weight = 45), §5.1
(cost ladder) · [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md)
(Systemcore) · [`../../research/00_PREMISE_CORRECTION.md`](../../research/00_PREMISE_CORRECTION.md).

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Fetched from a live vendor page or a primary FRC document, 2026-08-22 |
| **[H]** HISTORICAL-PATTERN | Observed across prior FRC seasons / this corpus; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or planning estimate. Flagged. Do not quote it as fact |
| **UNVERIFIED** | Page 404'd, 403'd, or did not expose the number. Confirm before ordering |

**Source shorthand**

`REB` = 2026 REBUILT manual (166 pp) · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO.
All in `manuals/archive/frc/`; rule text extracted in
`research/rule_inventories/2026_rules_full.txt` and `2026_rules.tsv`. The manuals and
`2026_rules_full.txt` are not in the repository, because FIRST's text is not redistributed: run
`bash tools/rebuild-corpus.sh --fetch`, then `bash tools/rebuild-corpus.sh`, from the repository root
before §0 step 3 or §9 V4.
`PF` = [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) ·
`PS` = [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md).
Vendor shorthand: `REV` = revrobotics.com · `SDS` = swervedrivespecialties.com ·
`TTB` = thethriftybot.com · `WCP` = wcproducts.com · `AM` = andymark.com · `CTRE` = ctr-electronics.com.

> **BIOCORE scope warning.** The BIOCORE game manual does not exist until **2027-01-09**. Frame
> perimeter, weight, and BUMPER geometry in §7 are the **2026 REBUILT** numbers, used as a planning
> baseline **[H]**. `R103`/`R104`/`R402`–`R408` are among the most stable rules in FRC, but the
> BUMPER *zone* height and the perimeter maximum have both moved before. Re-run §0 step 4 on
> kickoff day before you cut a single bumper board.

---

## 0. The 60-second workflow

Runnable **today** against 2026 data, and again on **2027-01-09** against the BIOCORE manual.
Tested 2026-08-22 on Git Bash / Windows 11.

```bash
# Run from the repository root.
cd reference/bom

# 1. HAVE ANY PRICES MOVED? re-fetch every SKU in the yaml and diff against the locked value.
#    exit 0 == this document's numbers still hold.
bash recheck_prices.sh                       # ~40 s, writes price_check_$(date +%F).tsv

# 2. WHAT DOES YOUR CHOSEN CONFIG COST? (edit CONFIG=, see the table in §8)
python - <<'PY'
import yaml, sys
d = yaml.safe_load(open('parts_drivetrain.yaml'))
for name, cfg in d['configurations'].items():
    print(f"{cfg['total_usd']:>9,.2f}  {name:<34} {cfg['drivetrain_type']}")
PY

# 3. BUMPER + FRAME LIMITS FROM THE MANUAL YOU ACTUALLY HAVE  (swap the year on 2027-01-09)
R=../../research/rule_inventories/2026_rules_full.txt
grep -A2 -E '^### R(10[34]|40[2-8])\b' "$R" | grep STATEMENT | cut -c1-260

# 4. ON KICKOFF DAY: did BUMPER geometry change vs the baseline this file assumed?
#    (after ingesting the BIOCORE manual with tools/ingest-manual.sh + tools/rule-inventory.py)
diff <(grep -E '^R40[1-9]' ../../research/rule_inventories/2026_rules.tsv | cut -f1,9) \
     <(grep -E '^R40[1-9]' ../../research/rule_inventories/2027_rules.tsv | cut -f1,9)

# 5. SANITY: is your drivetrain under the weight budget? (see §8.4)
echo "R103 robot weight limit 2026 = 115.0 lb without bumpers; R408 = 135.0 lb with bumpers"
```

If step 1 exits non-zero, **stop and fix this file before ordering.** Vendor prices moved twice
mid-season in 2026 **[H]**.

---

## 1. Swerve modules — the verified menu

All prices **[C]**, fetched from live product pages **2026-08-22**, per single module, USD.
"Motors" column = what you must buy separately unless noted.

| Module | Vendor SKU | Price/module | ×4 | Encoder | Wheel | Azimuth ratio |
|---|---|---:|---:|---|---|---|
| [REV 3in MAXSwerve](https://www.revrobotics.com/rev-21-3005/) | `REV-21-3005` | **$275.00** | $1,100.00 | **Included** — Through Bore Encoder, 10-bit, on the turning axis | 3 in | ~46.42:1 (exactly 9424:203) |
| [REV 4in EasySwerve](https://www.revrobotics.com/rev-21-3006/) | `REV-21-3006` | **$223.00** | **$892.00** | **NOT included** — needs a 1/2 in hex encoder, e.g. Through Bore Encoder V2 | 4 in | 20:1 |
| [SDS MK4i](https://www.swervedrivespecialties.com/products/mk4i-swerve-module) | (variant-coded) | **$365.00–$377.00** | $1,460–$1,508 | **NOT included** | tread pre-installed | (not stated on page) |
| [SDS MK4n](https://www.swervedrivespecialties.com/products/mk4n-swerve-module) | (variant-coded) | **$365.00–$377.00** | $1,460–$1,508 | **NOT included**; encoder guard *is* included | tread pre-installed on Billet option | **18.75:1** |
| [Thrifty Swerve](https://www.thethriftybot.com/products/thrifty-swerve) | `TTB-SWERVE-KRAKENX60-KRAKENX60` | **$299.99** | $1,199.96 | **Included** — Thrifty Absolute Magnetic Encoder | **tread NOT included** (1.5 in wide) | **25:1** |
| [WCP Swerve X2](https://wcproducts.com/collections/robot-drive/products/swerve-x2) | (variant-coded) | **$274.99** | $1,099.96 | **NOT included**; "natively supports CAN and Mag Encoder", on-axis mounting | wider wheel than X | UNVERIFIED |
| [WCP Swerve X (Legacy)](https://wcproducts.com/collections/robot-drive/products/swerve-x) | (variant-coded) | **$299.99** | $1,199.96 | **NOT included**; native CAN/Mag encoder support | — | UNVERIFIED |

> **Read the encoder column before you compare prices.** EasySwerve at $223 and MAXSwerve at $275
> are a $52 gap on paper; MAXSwerve ships the absolute encoder and EasySwerve does not, so the real
> gap is smaller than it looks. Thrifty at $299.99 includes the encoder but **not the tread**, which
> reverses the same trick in the other direction. Compare *delivered corners*, not module stickers.

### 1.1 Motors required, and what a delivered corner actually costs

Swerve needs **8 motors and 8 controller channels**; tank needs 4–6. That is the real cost driver,
not the modules (`PF` §3.1).

| Motor | SKU | Price | Controller |
|---|---|---:|---|
| [REV NEO Brushless V1.1](https://www.revrobotics.com/rev-21-1650/) | `REV-21-1650` | **$42.50** | needs SPARK MAX |
| [REV SPARK MAX](https://www.revrobotics.com/rev-11-2158/) | `REV-11-2158` | **$100.00** | — |
| [CTRE Kraken X60](https://store.ctr-electronics.com/products/kraken-x60) | `WCP-0940` | **$217.99** *(educational; retail = contact sales)* | **integrated Talon FX** — no separate controller |
| REV MAXSwerve motor + controller bundle, per corner | — | **$280.00** | bundle (`PF` §3.1 **[C]**) |
| [REV NEO 550 Brushless Motor](https://www.revrobotics.com/rev-21-1651/) (MAXSwerve azimuth) | `REV-21-1651` | **$30.00** | needs SPARK MAX |
| REV NEO Vortex / SPARK Flex | UNVERIFIED | UNVERIFIED | SPARK Flex |
| [CTRE **CANcoder** — CAN Bus Magnetic Encoder](https://store.ctr-electronics.com/products/cancoder) (MK4i / MK4n / X2) | `22-676768` | **$89.99** | CAN FD and CAN 2.0 |
| [REV Through Bore Encoder **V1**](https://www.revrobotics.com/rev-11-1271/) | `REV-11-1271` | **$40.80** | 1/2 in hex |
| REV Through Bore Encoder **V2** (the part EasySwerve names) | UNVERIFIED | UNVERIFIED — V1 at $40.80 is the best available proxy **[S]** | 1/2 in hex |

**The encoder line is not a rounding error.** Four CANcoders at $89.99 = **$359.96**, which is
**more than the entire motor bill of a 4-NEO tank drive** ($170.00). Any swerve comparison that omits
encoders is understating the swerve path by $160–$360.

**Kraken X60 note [C]:** *"1,108W peak power (413W@40amp), 87% max efficiency (@30A), and 7.09Nm
stall torque."* Its integrated controller is why an 8-Kraken swerve is only ~2× a 6-NEO tank rather
than ~3×: you buy 8 motors, not 8 motors *plus* 8 SPARK MAXes.

### 1.2 Gear ratios and free speed — what is on the record

| Module | Drive ratios offered | Free speed **[C]** where the page stated it |
|---|---|---|
| REV EasySwerve | **6.3:1** (single drive ratio) | **18.79 ft/s** with NEO Vortex; **15.724 ft/s** with NEO 2.0 |
| REV MAXSwerve | 3 base speeds (low/med/high) + optional upgrade kit adding **5** higher ratios | not stated in page text — UNVERIFIED |
| SDS MK4i | **L1 / L2 / L3.** Page: *"the most popular ratios… suitable for standard full weight competition robots. The L3 ratio is more aggressive and is recommended for light weight robots."* | published as a chart image only — UNVERIFIED as text |
| SDS MK4n | **L1+ / L2+ / L3+** | table on page, not extractable as text — UNVERIFIED |
| Thrifty Swerve | **6 swappable ratios**, steel azimuth and drive gears | not stated — UNVERIFIED |
| WCP Swerve X2 | ratio table lives in `docs.wcproducts.com` | UNVERIFIED |

**[S] Planning rule for a 15-student team:** pick the **middle** ratio (L2 / MAXSwerve medium /
EasySwerve's single 6.3:1) and do not revisit it. Every free speed in this table is 14–19 ft/s, and
`PF` §7 finds **drivetrain speed does not vary meaningfully from mid-tier to top-tier teams** — top
speed is not what separates you. Cycle time is driven by acquisition and scoring dwell, not sprint.

### 1.3 Module weight — the number that decides your mechanism budget

**[C]** Thrifty Swerve is the only vendor that published per-config module mass on its page:

| Config | Module mass | ×4 |
|---|---:|---:|
| NEO azimuth + NEO drive | 5.60 lb | **22.4 lb** |
| NEO azimuth + Kraken drive | 6.04 lb | **24.2 lb** |
| Kraken azimuth + Kraken drive | 6.28 lb | **25.1 lb** |

Against `R103`'s **115.0 lb** robot limit (excluding bumpers and battery), four modules alone are
**19–22% of your entire weight budget** before a frame, a belly pan, electronics, or a mechanism.
A 6-wheel AM14U6 with 6 NEOs is in a similar band, but you get the *frame* included in that number.
Other vendors' module masses: UNVERIFIED — get them from CAD before you do a weight study.

### 1.4 What the team must fabricate for a swerve drive

This is the part every module price table omits, and it is where a 15-student team loses February.

| Item | Why | Fab needed | **[S]** hours, first time |
|---|---|---|---|
| **Frame rails** (2×1 tube, 4 pieces) | modules bolt to corners or to tube faces | cut square to ±0.010, drill/tap mounting pattern | 4–8 h without a mill; 2 h with |
| **Belly pan** (1/8 in 6061 or 3/16 in polycarb) | ties the 4 corners together; carries electronics | **2D sheet cut** — outsource (SendCutSend) or hand-drill from a printed template | 3 h if outsourced (CAD only), 10–16 h if hand-made |
| **Standoffs / hex spacers** | belly pan to top rail | cut to length, or buy COTS | 1–2 h |
| **Bumper mounting brackets** | `R402-D` requires a *rigid* fastening system — no zip ties, no hook-and-loop | drill + rivet/bolt | 3–5 h |
| **Electronics board** | Systemcore + PDH + 8 controllers | 2D cut or plywood | 2–4 h |
| **Corner gussets** | squareness under impact | 2D cut | 2 h |

**Tooling floor for COTS swerve [S]:** hex key set through 5 mm, torque-ish driver, **thread locker
(non-negotiable — loose azimuth pinion screws are the #1 swerve failure mode [H])**, a vise or arbor
press for bearings, a chop saw or bandsaw with an aluminum blade, drill press, tap set (#10-32 and
M4/M5), and a rivet gun if you rivet. REV advertises EasySwerve as needing *"only four tools"* to
assemble **[C]** — that claim is about the *module*, not about the chassis it must sit in.

**[S] Assembly-hours estimate, 4 modules, from kit to spinning:** MAXSwerve/EasySwerve **5–8 h**;
Thrifty **6–9 h** (more ratio choices to commit to); MK4i/MK4n **8–14 h** (ships unassembled,
highest part count, tightest tolerances). Add **12–25 h** for the chassis around them. These are
planning estimates, **not measured** — no time-study exists in this corpus.

### 1.5 Reliability notes **[H]**

| Failure | Module family | Mitigation |
|---|---|---|
| Azimuth pinion / drive pinion set screws back out | all | Loctite 242 at build, re-torque before every event day |
| Absolute encoder magnet drifts or the offset is lost | all | write offsets to a file in version control, **not** to controller flash only; re-zero after any azimuth disassembly |
| Bevel/spur wear on plastic gears | polymer-geared modules | Thrifty ships **steel** azimuth and drive gears **[C]** — a durability argument in its favour |
| Tread wears through in 2 events | all | budget **2 tread changes per season**; Thrifty sells tread separately, so it is already a line item |
| Module knocked out of square by a defensive hit | corner-mount styles | prefer tube-mount where the vendor offers both (X2 and MK4i both do) |
| CAN bus saturation with 12 devices | all, pre-2027 | **Solved in 2027** — Systemcore has 5 CAN buses (§6) |

---

## 2. Tank / West Coast Drive

| Item | SKU | Price | Included | Not included |
|---|---|---:|---|---|
| [AndyMark **AM14U6**](https://www.andymark.com/products/am14u6-6-wheel-drop-center-robot-drive-base-2025-frc-kit-of-parts-drive-base) — *"6 Wheel Drop Center Robot Drive Base — 2026 FRC Kit of Parts"* | `AM-14U6` | **$940.00** (all gear-ratio options) **[C]** | 2× Toughbox Mini S gearboxes; HTD belts (160T / 131T / 120T); **6× 6 in HiGrip wheels, 80A**; bearings, shafts, gears, spacers, fasteners | **CIM motors, NEO motors, battery, charger, bumper hardware mount kit, vertical battery mount kit** |
| WCP GreyT chassis kit | — | **UNVERIFIED** — no GreyT *chassis* product page resolved on 2026-08-22; GreyT is a family of **mechanism** kits (Elevator, Telescope, Claw, Shooter) | — | — |
| [WCP 2026 Competitive Concept](https://wcproducts.com/products/2026-wcp-competitive-concept) | — | **$17.99** for the CAD/BOM/documentation package; a full kit version listed at **$278** (sale, from $400) **[C]** but its exact contents are **UNVERIFIED** | design package: CAD, OnShape, BOM | physical parts (in the $17.99 tier) |
| TTB / WCP WCD structural kits, VersaFrame tube stock | — | **UNVERIFIED** — collection pages 404'd on 2026-08-22 | — | — |

**AM14U6 geometry [C]:** three configurations, **24.3 in × 27 in** (smallest) up to
**32.3 in × 31 in** (largest). Center drop **0.140 in** in the long configuration, **0.07 in** in the
wide configuration. That maximum footprint is well inside `R104`'s **110.0 in** perimeter limit
(2026 baseline), which is why the KOP chassis has never needed a manual re-check.

### 2.1 What the team must fabricate for AM14U6

Almost nothing, and that is the entire point.

| Item | Fab needed | **[S]** hours |
|---|---|---|
| Chassis itself | **rivet the pre-cut, pre-drilled rails.** No cutting, no drilling, no CAD | **3–5 h** |
| Belly pan | optional — the KOP rails already tie together | 0–4 h |
| Bumper brackets | drill + rivet | 3–5 h |
| Electronics board | plywood or polycarb, hand-cut | 2–3 h |
| **Total to a driving chassis** | rivet gun, hex keys, drill | **~8–17 h** |

**Tooling floor: a rivet gun, a drill, and hex keys.** There is no lower floor in FRC. **[H]**

### 2.2 Tank reliability **[H]**

Belt-in-tube 6-wheel drop-center with a 0.07–0.14 in drop is the most reliable drivetrain
architecture in the program. Failure modes are a shed belt (fix: correct tension, belt guards) and
a stripped hex bore (fix: use the supplied hardware). It does not have absolute encoders to lose,
does not have 8 devices on a CAN bus, and does not have azimuth set screws.

---

## 3. KOP chassis — what actually ships, and when it is right

**[C]** The [FIRST KitBot](https://www.firstinspires.org/resources/library/frc/kitbot) is *"a
versatile, beginner-friendly robot kit included in the FIRST Robotics Competition Kickoff Kit."*
It is built on the **AM14U6 chassis**, and AndyMark publishes the drivetrain build guide. The FIRST
page also references *"the REV Robotics Control System components provided in the rookie Kickoff
Kit."* **No 2027 / BIOCORE KitBot information exists as of 2026-08-22** — the page's newest
resources are 2026.

> **2027 uncertainty [S]:** the KitBot's electrical bill of materials will change, because the
> roboRIO is gone (§6). Whether the AM14U6 or a successor ships in the BIOCORE Kickoff Kit is
> **UNVERIFIED**. Do not pre-buy a second KOP chassis on the assumption it is the same one.

### 3.1 Capability ceiling

Do not read "beginner" as "non-competitive." From `PF` §5.1 and §4 **[C]**:

- The **Everybot 2026** — a KOP-chassis-class robot costing *"~$1,500 over the KoP"*, built with
  *"only common tools, a basic 3D printer, items purchased from your local hardware store"* —
  produced **100 unique alliance captains in 2026** across 116 captaincies.
- Of those 100 captains, **only 10 were identified as having swerve.**
- Non-swerve robots in 2025 week-2 pit scouting were **32.3% KitBot variants and 12.0% Everybot
  variants** — a *deliberate COTS-template population*, not a legacy population.

**The ceiling is "alliance captain at a regional / district event."** It is not "Einstein." That is
also the ceiling this project's rubric is aimed at.

### 3.2 When the KOP chassis is the right answer for a 15-student team

Take the KOP/tank path if **any two** of these are true **[S]**:

1. Nobody currently on the team has assembled a swerve module before.
2. Nobody has written field-oriented swerve code before **(weigh this at double in 2027 — see §6)**.
3. Your build season has fewer than ~5 reliable mechanical students on any given night.
4. Your intended robot has **two or more** distinct scoring mechanisms.
5. You have less than ~$6,000 of total robot budget.
6. You did not get ≥20 hours of driver practice on a complete robot last season.

---

## 4. Gearboxes

| Product | SKU | Price | Ratios |
|---|---|---:|---|
| [REV **MAXPlanetary System Kit**](https://www.revrobotics.com/rev-21-2100/) | `REV-25-2109` | **$36.00** **[C]** | see cartridges below |
| MAXPlanetary 2:1 cartridge | `REV-21-2140` | UNVERIFIED | 2:1 |
| MAXPlanetary 3:1 cartridge | `REV-21-2101` | UNVERIFIED | 3:1 |
| MAXPlanetary 4:1 cartridge | `REV-21-2102` | UNVERIFIED | 4:1 |
| MAXPlanetary 5:1 cartridge | `REV-21-2103` | UNVERIFIED | 5:1 |
| MAXPlanetary 9:1 cartridge | `REV-21-2129` | UNVERIFIED | 9:1 |
| MAXPlanetary bundles | — | UNVERIFIED | **9:1 through 125:1** (e.g. 125:1 = 5:1 + 5:1 + 5:1) **[C]** |
| AndyMark **Toughbox Mini S** | — | included in `AM-14U6` | multiple ratio options at the same $940 price **[C]** |
| VEX **VersaPlanetary** | `217-xxxx` | **UNVERIFIED** — vexrobotics.com returned **HTTP 403** to automated fetch on 2026-08-22 | UNVERIFIED |
| WCP gearboxes (SS, Flipped, single-stage) | — | **UNVERIFIED** | UNVERIFIED |
| TTB gearboxes | — | **UNVERIFIED** — `thethriftybot.com/collections/drivetrain` returned **404** | UNVERIFIED |

**[S] For a drivetrain specifically, you probably buy zero gearboxes.** Swerve modules *are* the
gearbox. The AM14U6 ships with its gearboxes. MAXPlanetary and VersaPlanetary belong in the
*mechanism* BOM, not here — they appear in this file only so nobody double-orders.

---

## 5. Wheels and tread

| Wheel | SKU | Price | Size | Grip / durability **[H]** |
|---|---|---:|---|---|
| [AndyMark **SDS Colson**, wheel only](https://andymark.com/products/sds-colson-wheel) | `am-5171` | **$19.10** **[C]** | 4 in (100 mm) × 1.5 in | The swerve default. *"co-injection molded… thermoplastic elastomer tread permanently bonded to a polyolefin core."* Very long life; moderate μ; does not shed |
| AndyMark SDS Colson **with hub** | `am-5173` | **$38.00** **[C]** | same | drop-in for MK4/MK4i |
| AndyMark SDS Colson **with bevel gear** | `am-5261` | **$72.00** **[C]** | same | for bevel-drive modules |
| [WCP **Colson Performa**](https://wcproducts.com/products/colson-wheels) | not listed on page | **from $4.99** **[C]** (price varies by size; per-size SKUs **UNVERIFIED**) | many | *"some of the most widely used and recognizable wheels in large-scale competition robotics"*; integrated plastic hex hubs |
| [AndyMark **6 in. HiGrip Wheel Rev2**](https://www.andymark.com/products/higrip-wheels-options) | `am-0940a` | **$12.00** **[C]** — but ⚠️ **DISCONTINUED**: *"This product is no longer for sale at AndyMark and has been replaced by am-0940b."* `am-0940b` price **UNVERIFIED** | 6 in, 0.95 in bore, six holes on 1.875 in BC, **0.5 lb**, 90 lb load | Black polycarbonate + TPU, **80A**. *"aggressive tread pattern providing maximum transfer of gearbox power to the ground."* High μ on carpet, softer, wears faster than Colson. **6 are included in `AM-14U6`** **[C]** |
| **Roughtop tread** (1.5 in / 2 in wide) | — | **UNVERIFIED** — no vendor page loaded | — | Highest μ of the common options; **wears fastest**; budget 2 changes/season |
| **Omni wheels** | — | **UNVERIFIED** | — | Only relevant on a tank corner-omni layout to ease turning; costs you pushing power |
| **Mecanum** | — | **UNVERIFIED** | — | **[H] Do not.** Holonomic without swerve's traction; near-zero pushing force; effectively extinct in modern FRC and a liability against any defender |

**[S] Recommendation:** Colson on swerve (it is what the modules are designed around and it lasts a
season); the supplied HiGrip on AM14U6; roughtop only if you have a specific pushing-match reason
and have budgeted replacement tread.

---

## 6. Systemcore — the 2027 drivetrain electronics reset

**The roboRIO is gone.** Detail lives in `PS`; this section extracts only what changes a
**drivetrain** decision. Source for every row: `PS` §"Systemcore hardware, verified" and
[Removed features for 2027](https://docs.wpilib.org/en/2027/docs/yearly-overview/removed-features.html).

| Change | Drivetrain consequence | Direction |
|---|---|---|
| **5 CAN interfaces, FD-capable, up to 8 Mbps, built-in 120 Ω termination** (roboRIO had 1 bus @ 1 Mbps) **[C]** | An 8-motor + 4-encoder swerve is **12 CAN devices**. On one 1 Mbps bus that was a genuine bandwidth and diagnosis problem, and teams bought a CANivore to split it. **You no longer need to.** | ✅ **Helps swerve, materially** |
| **Onboard IMU** — 400 Hz quaternion, fused robot yaw, 3-axis accel + gyro **[C]** | You do **not** buy a Pigeon 2 or a navX. One less CAN device, one less failure point, one less line item. Field-oriented swerve *requires* a gyro, so this saving lands disproportionately on the swerve path | ✅ **Helps swerve** |
| **SPI removed** **[C]** | *Kills* ADIS16448, ADIS16470, ADXL345, ADXRS450. **Any SPI IMU in your parts bin is e-waste for 2027.** Do not buy one used | ⚠️ Write off existing stock |
| **Analog Gyro removed** **[C]** | Legacy analog gyros gone | ⚠️ |
| **`Counter` removed** **[C]** | Anything counting edges. Quadrature *is* listed among the 6 reconfigurable I/O modes but is flagged *"in progress or subject to change"* in the alpha spec | ⚠️ Verify before relying on a DIO drivetrain encoder |
| **`Servo` removed** — *"Systemcore doesn't have the ability to give servos the power they demand"* **[C]** | Only bites the drivetrain if you planned a **servo-actuated shifter or PTO release**. Use pneumatics or a small motor instead | ⚠️ Design around it |
| **WPILib 2027 is Systemcore-only**; Java packages move `edu.wpi.first` → `org.wpilib`, C++ `frc::` → `wpi::`; Java 25 / C++23 required; NetworkTables v3 removed; **Shuffleboard, SmartDashboard, PathWeaver, RobotBuilder and LabVIEW all removed** **[C]** | **This is the big one for swerve.** Every swerve template you might copy — REV MAXSwerve template, YAGSL, CTRE swerve project generator, Phoenix 6, REVLib — must be **re-released by its vendor for 2027** before you can use it. Path planning tooling is being replaced. Your 2026 swerve code does **not** port by find-and-replace | 🔴 **Hurts swerve, a lot, in year one** |
| **Systemcore price** | FIRST says *"on target to… a lower price than the roboRIO"* but **has published no number** **[C]**. `PS` §6: *"Treat Systemcore price as unknown; do not build a budget on a guess"* | ❓ Unbudgetable |
| **No production units available** as of the `PF` §6.3 quote **[C]** | `PF`: *"carry an explicit schedule-risk penalty in the rubric until SystemCore is in your hands and running"* | 🔴 Schedule risk |

### 6.1 The net Systemcore verdict for drivetrain choice **[S]**

Systemcore makes swerve **cheaper and cleaner in hardware** (free IMU, five CAN buses, no CANivore)
while making it **more expensive in software-schedule risk than any season since swerve became
common**. Those pull in opposite directions and they do **not** cancel: hardware savings are worth a
few hundred dollars once, and a swerve software stack that isn't ready in week 4 costs you the
season. `PF` §3.4 already reached this conclusion independently: score a first-year swerve adoption
in 2027 as **"a scope item competing with a mechanism,"** not as a free upgrade.

**Concrete fall-2026 action:** watch for 2027 releases of REVLib, Phoenix 6, and YAGSL. If a working
2027 swerve template is not public by **early December 2026**, a first-year swerve team should
default to tank. Put that date on the calendar now.

---

## 7. Bumpers

> ⚠️ **BUMPER geometry is manual-governed. Every number below is the 2026 REBUILT baseline [H],
> not a BIOCORE fact.** Re-derive from the BIOCORE manual on 2027-01-09 using §0 step 3.

**2026 REBUILT rule requirements, summarized [C]** (`research/rule_inventories/2026_rules_full.txt`):

| Rule | Requirement (2026) |
|---|---|
| `R402-A` Padding | **≥ 2.25 in (5.72 cm) depth**, **≥ 4.5 in (11.43 cm) tall**, solid blocks/sheets/stacked rods of: **solid pool noodles or backer rod**; **solid polyethylene closed-cell foam (incl. crosslinked), density 1.5–3.0 lb/ft³**; **solid EVA closed-cell foam, density 2.0–6.0 lb/ft³**; **foam floor tiles**. Multiple types/shapes/layers permitted |
| `R402-B` Backing | backer **≥ 4.5 in tall** supporting the padding (no cantilever except in corners), and it must facilitate install/removal per `R410` |
| `R402-C` Cover | **cloth** covering all outward, upward and downward facing surfaces — no exposed padding |
| `R402-D` Fastening | **rigid** fastening to the ROBOT PERIMETER — *"not attached with hook-and-loop tape, tape, or cable ties"* |
| `R403` | must not extend **> 4.0 in (10.16 cm)** from the ROBOT PERIMETER |
| `R404` | hard parts **≤ 1.25 in (3.17 cm)** beyond the perimeter; padding must extend **≥ 2.0 in** beyond any hard part |
| `R405` BUMPER ZONE | padding + backing must entirely fill **2.5 in to 5.75 in (6.35–14.61 cm) from the floor** |
| `R406` | corner joints filled with **uncompressed** padding extending **≥ 2.25 in** from the corner, no gaps. Blue box: *"Separate bumper segments meeting at a miter in the corner are not considered to 'fill' the corner"* |
| `R407` | must not act as wedges |
| `R408` | robot **with** bumpers **≤ 135.0 lb (61.23 kg)** |
| `R103` | robot **without** bumpers, battery, and location tags **≤ 115.0 lb (52.16 kg)** |
| `R104` | STARTING CONFIGURATION perimeter **≤ 110.0 in (2.794 m)**, height **≤ 30 in** |

**That gives you a ~20 lb bumper + battery budget.** A full set of four FRC bumpers has
historically run 12–18 lb **[H]**.

### 7.1 Material list and cost

| Item | Qty for a ~30×30 in robot | Source | Cost |
|---|---|---|---|
| Backing — 3/4 in **plywood** (or 1/8 in aluminum angle) | ~14 linear ft, 5 in wide | hardware store | **UNVERIFIED** — price locally; historically **$25–$50** for the sheet **[S]** |
| Padding — **pool noodles** (solid, not hollow) or backer rod | 2 rods per side, 2 sides deep | hardware / pool supply | **UNVERIFIED**; historically **$2–$5 each**, ~$20–$40/set **[S]** |
| Cover — **cloth**, red and blue, ~1000D Cordura or heavy nylon | ~4 yd per color | fabric store / AndyMark | **UNVERIFIED**; historically **$40–$90 per color set** **[S]** |
| Fasteners — bolts, locking pins, brackets (**rigid**, per `R402-D`) | 8–12 attachment points | hardware store | **UNVERIFIED**; **$20–$40** **[S]** |
| Team numbers — 4 in tall vinyl or sewn (per `R412`) | 4 sets | vinyl cutter or vendor | **UNVERIFIED** |
| **[S] Planning total, two sets (red + blue)** | | | **~$150–$250** |

**All bumper costs above are UNVERIFIED** — no vendor bumper-kit page loaded on 2026-08-22
(`andymark.com/products/frc-bumper-kit` returned 404). Price these locally in the fall. The
*rule text* in §7 is `[C]`; the *dollars* are `[S]`.

**[C] `R402` blue box:** *"For information on a reference design, see the Bumper Guide under the
Mechanical Resources section of the Technical Resources Page."* Use it — do not invent a bumper.

**[S] Small-team bumper rule:** build **one** set of backings with **swappable cloth covers**, not
two complete sets. Halves the wood, the labor, and the weight you must store.

---

## 8. THE DECISION TABLE — swerve vs tank, 15 students, 2027

### 8.1 Priced configurations (drivetrain only — no bumpers, no battery, no Systemcore)

| # | Configuration | Modules / chassis | Motors + controllers | Encoders | Core total | **Delivered total** |
|---|---|---:|---:|---:|---:|---:|
| T1 | **AM14U6 + 4× NEO + 4× SPARK MAX** | $940.00 | $170.00 + $400.00 | $0 — onboard Systemcore IMU | $1,510.00 | **$1,510.00** |
| T2 | **AM14U6 + 6× NEO + 6× SPARK MAX** | $940.00 | $255.00 + $600.00 | $0 | $1,795.00 | **$1,795.00** |
| S1 | **REV EasySwerve + 8× NEO + 8× SPARK MAX** | $892.00 | $340.00 + $800.00 | 4× TBE, **$163.20** (V1 price as proxy for the V2 the vendor names) **[S]** | $2,032.00 | **~$2,195.20** |
| S2 | **REV MAXSwerve + REV corner bundles** | $1,100.00 | $1,120.00 (4 × $280.00) | **included** | $2,220.00 | **$2,220.00** |
| S3 | **WCP Swerve X2 + 8× Kraken X60** | $1,099.96 | $1,743.92 | 4× CANcoder, **$359.96** (WCP Mag Encoder price UNVERIFIED) | $2,843.88 | **$3,203.84** |
| S4 | **Thrifty Swerve + 8× Kraken X60** | $1,199.96 | $1,743.92 | **included** | $2,943.88 | **$2,943.88 + tread** |
| S5 | **SDS MK4i + 8× Kraken X60** | $1,480.00 | $1,743.92 | 4× CANcoder, **$359.96** | $3,223.92 | **$3,583.88** |

Motor arithmetic: NEO `REV-21-1650` $42.50 · NEO 550 `REV-21-1651` $30.00 · SPARK MAX `REV-11-2158`
$100.00 · Kraken X60 `WCP-0940` $217.99 educational (integrated controller) · CANcoder `22-676768`
$89.99 · Through Bore Encoder V1 `REV-11-1271` $40.80. All **[C]** 2026-08-22.

**Fully verified, encoders and all, the cheapest swerve you can actually field is S2 at $2,220.00 and
the cheapest tank is T2 at $1,795.00.** Everything else in the swerve column is more expensive.

### 8.2 The three deltas

| Delta | Cheapest honest comparison | Widest realistic comparison |
|---|---|---|
| **Cost** | S2 − T2 = **+$425.00** (both fully verified, both encoder-complete) | S5 delivered − T1 = **+$2,073.88** (before a spare module or spare tread) |
| **Build hours [S]** | swerve **17–33 h** (modules 5–8 + chassis 12–25) vs tank **8–17 h** → **+9 to +16 h** | MK4i path: **20–39 h** vs **8 h** → **+12 to +31 h** |
| **Programming hours [S]** | tank arcade drive to a driving robot: **2–5 h**. Swerve with a *working, released* 2027 vendor template: **15–30 h**. Swerve with **no 2027 template yet**: **50–100 h+** | — |

The cost delta is the **smallest** of the three and it is the one everyone argues about. The
programming delta is the largest, and in 2027 it is also the **most uncertain**, because WPILib 2027
is a breaking rewrite and no vendor swerve template has shipped for it yet (§6).

### 8.3 Weight delta

| | Drivetrain mass | % of `R103` 115.0 lb |
|---|---:|---:|
| 4× Thrifty Swerve, NEO+Kraken **[C]** | 24.2 lb *(modules only — no frame, no belly pan)* | 21% |
| AM14U6 + 6 NEO **[S]** | ~28–32 lb *(complete rolling chassis)* | 24–28% |

Swerve's 24.2 lb buys you **zero structure**. Add a fabricated frame and belly pan and swerve is
heavier than the KOP chassis, not lighter. Budget accordingly.

### 8.4 What the evidence actually supports

From `PF` §3, all **[C]** as cited accounts:

- Swerve adoption was **~71% in 2024** (166/185 events pit-scouted) and higher in 2025, with
  multiple 100%-swerve events.
- **No clean swerve-vs-tank performance study exists.** Statbotics does not label drivetrain, so
  every published comparison is confounded — swerve teams are richer, larger, and more experienced.
- **100 unique tank/Everybot teams captained an alliance in 2026** (116 captaincies); only **10%**
  of them had swerve.
- Counter-evidence, n=1 event: FMA Allentown 2024, 27 teams, 8 tank — *"There were no tank captains,
  and the first tank off the board was pick #8."*
- *"A tank on a well practiced driver will always outperform a swerve with an inexperienced driver."*
- *"If an event had 50% swerve, I'd say maybe half of them were more effective at moving around the
  field than a tank chassis."*
- And the decision rule this project adopts verbatim: *"You should pick your drivetrain for 3
  reasons: It's the one you know how to build the best. It's the one you know how to program the
  best. It's the one you know how to drive the best. **None of those reasons have anything to do
  with the game.**"*

`PF` weights drivetrain choice at **45 / 100** — a real term, well below drive practice (90) and
scope discipline (85). **This file does not overturn that. It confirms it with SKUs.**

### 8.5 The honest conditional recommendation

**If your team already ran swerve in 2026 →** run swerve in 2027. **Buy the same modules again.**
Your build knowledge transfers completely; only the software resets. Configuration **S2**
(MAXSwerve + REV bundles, $2,220, encoders included) or **S4** (Thrifty, steel gears, encoder
included) are the lowest-friction reorders. Budget the Systemcore port as its own project with its
own owner, starting the day WPILib 2027 beta drops — **not** in January.

**If your team has never run swerve →** **do not adopt it in 2027.** This is the single strongest
recommendation in this file, and 2027 is the specific reason. Every previous "should we switch"
season let you copy a mature, battle-tested swerve template on day one. 2027 does not: WPILib is a
breaking rewrite, Systemcore has no production units as of 2026-08-22, and no vendor swerve template
has been released for it. A first-year swerve adoption in a control-system reset year, on a
15-student team, is spending your scope budget three times — new hardware, new software stack, new
driver skill — against a $425–$2,074 saving you could put into practice time instead. Run **T2**
(AM14U6 + 6 NEO, $1,795), finish the robot in week 4, and spend the delta on driver hours, which
`PF` weights at **90**.

**If you are on the fence and have real money →** the tiebreaker is **not** budget. It is this
question: *can you name the student who will own the swerve software, and are they available
20 h/week in January?* If you cannot name that person, the answer is tank.

**The one thing that beats both:** a complete robot by week 4 with 20+ hours of driver practice.
Neither drivetrain gets you there by itself; the wrong one prevents it.

### 8.6 Buy-in-the-fall list — safe to order before 2027-01-09 **[S]**

Drivetrain is the only major subsystem you can commit to before the game is revealed, because the
choice does not depend on the game (§8.4).

| Order in the fall | Why it is game-independent |
|---|---|
| Chassis or 4 modules + **1 spare module** | Frame perimeter limits have been stable at `R104` ≈ 110 in for years **[H]** |
| All 8 (or 6) drive motors + controllers | Motor choice is independent of game |
| Wheels/tread + **one full spare set** | Wear is certain |
| Bumper **backings** and fasteners | ⚠️ Only if `R403`/`R405` geometry holds — verify on kickoff day before cutting |
| Bumper **cloth** | Colors and `R411`/`R412` numbering have been stable **[H]** |
| **DO NOT pre-order:** Systemcore | Price unpublished; no production units; availability unknown **[C]** |

---

## 9. Validation / dry-run

Run this before you trust any number in this file.

```bash
# Run from the repository root.
cd reference/bom

# V1. Every URL in the yaml resolves (expect 200 for all rows marked evidence: C)
grep -oE 'https?://[^ "]+' parts_drivetrain.yaml | sort -u | while read -r u; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 "$u")
  printf '%s\t%s\n' "$code" "$u"
done | sort

# V2. Config totals in the yaml equal the sum of their line items
python - <<'PY'
import yaml
d = yaml.safe_load(open('parts_drivetrain.yaml'))
bad = 0
for name, c in d['configurations'].items():
    s = round(sum(i['qty'] * i['unit_usd'] for i in c['line_items']), 2)
    flag = '' if abs(s - c['total_usd']) < 0.01 else '  <-- MISMATCH'
    if flag: bad += 1
    print(f"{name:<36} yaml={c['total_usd']:>9,.2f} sum={s:>9,.2f}{flag}")
print('OK' if not bad else f'{bad} MISMATCHES')
PY

# V3. No price in this .md that is absent from the .yaml (catches drift between the pair)
grep -oE '\$[0-9][0-9,]*\.[0-9]{2}' 01_DRIVETRAIN.md | tr -d '$,' | sort -u > /tmp/md.txt
grep -oE '[0-9]+\.[0-9]{2}' parts_drivetrain.yaml | sort -u > /tmp/yml.txt
comm -23 /tmp/md.txt /tmp/yml.txt   # empty == in sync

# V4. Bumper rule numbers in §7 match the manual this repo actually holds
grep -c 'UNVERIFIED' 01_DRIVETRAIN.md   # expect 40; every one is a real gap, not a typo
sed -n "$(grep -n '^### R402' ../../research/rule_inventories/2026_rules_full.txt | cut -d: -f1),+3p" \
  ../../research/rule_inventories/2026_rules_full.txt | grep -o '2\.25in\|4\.5in'

# V5. KICKOFF DAY ONLY: re-derive §7 from the BIOCORE manual and fail loudly if it moved
#     (requires tools/ingest-manual.sh + tools/rule-inventory.py to have run on the 2027 PDF)
for r in R103 R104 R403 R405 R408; do
  echo "== $r"; grep -A2 "^### $r " ../../research/rule_inventories/2027_rules_full.txt | grep STATEMENT | cut -c1-200
done
```

**Actual results, run 2026-08-22 (this is a real run, not an aspiration):**

| Check | Result |
|---|---|
| V1 | The 18 live product URLs carrying a locked price all resolved on fetch. The six URLs in `unverified_registry` did **not** — five returned 404, `vexrobotics.com` returned 403 |
| V2 | **All 7 configurations reconcile to the cent.** `T1 1,510.00 · T2 1,795.00 · S1 2,032.00 · S2 2,220.00 · S3 2,843.88 · S4 2,943.88 · S5 3,223.92` |
| V3 | **empty** — every dollar figure in this .md also appears in the .yaml |
| V4 | `40` UNVERIFIED markers; `2.25in` and `4.5in` both present in the 2026 `R402` text |
| V5 | n/a until 2027-01-09 |

`recheck_prices.sh` extracts **18 URL/price pairs** from the yaml. If that count drops, the yaml's
block structure changed and the awk extractor needs updating before you trust its PASS.

---

## Files written by this pass

| File | What it is |
|---|---|
| `reference/bom/01_DRIVETRAIN.md` | this document |
| `reference/bom/parts_drivetrain.yaml` | machine-readable companion: 30 SKU entries + 7 priced configurations, same evidence labels |
| `reference/bom/recheck_prices.sh` | re-fetches every `evidence: C` URL in the yaml and diffs the price; §0 step 1 |

Nothing marked DONE elsewhere in this project was modified.

## Known limitations

1. **Prices are a single-day snapshot (2026-08-22) and FRC vendor prices move mid-season [H].**
   Run `recheck_prices.sh` before any purchase order. Treat every number as ±10% until re-checked.
2. **Eight categories could not be verified.** VEX VersaPlanetary (**403 Forbidden** to automated
   fetch), TTB drivetrain collection (**404**), WCP WCD kit (**404**), AndyMark bumper kit (**404**),
   REV MAXSwerve system landing page (**404**), roughtop tread, omni, mecanum. **A WCP "GreyT
   chassis" product does not appear to exist** — GreyT is a family of *mechanism* kits (Elevator,
   Telescope, Claw, Shooter). If a GreyT chassis was intended, it is either discontinued or was
   never a product; do not cite one.
   Two prices are **stale-by-succession** rather than unfetchable: HiGrip `am-0940a` ($12.00) is
   marked discontinued in favour of `am-0940b`, and REV Through Bore Encoder **V1** ($40.80) is
   priced while **V2** — the part the EasySwerve docs actually name — is not. Both successors need a
   price before you order.
3. **Gear-ratio tables for MK4i, MK4n, MAXSwerve, Thrifty and Swerve X2 are published as images or
   in separate docs sites and could not be extracted as text.** Only EasySwerve's 6.3:1 / 18.79 ft/s
   and the azimuth ratios (MAXSwerve 9424:203, EasySwerve 20:1, MK4n 18.75:1, Thrifty 25:1) are
   `[C]`. Get the rest from the vendor's docs site before finalizing a speed choice.
4. **All build-hour, assembly-hour and programming-hour figures are `[S]` planning estimates.**
   No time-study exists in this corpus. They are internally consistent and directionally defensible;
   they are not measured. Do not present them to a sponsor as data.
5. **Every bumper dollar figure is `[S]`/UNVERIFIED.** The bumper *rules* in §7 are `[C]` from the
   2026 manual; the *costs* are historical impressions. Price them locally in the fall.
6. **§7 is 2026 REBUILT geometry, not BIOCORE.** BIOCORE's manual does not exist until 2027-01-09.
   `R405`'s BUMPER ZONE and `R403`'s 4.0 in extension are the two most likely to move **[H]** — see
   [`../RULE-CHURN-WATCHLIST.md`](../RULE-CHURN-WATCHLIST.md).
7. **Systemcore's price is unknown and no production units exist** as of 2026-08-22. Any total-robot
   budget built on this file is missing one line item of unknown size.
8. **This file did not create a swerve-vs-tank performance study, and none exists.** §8.4 restates
   `PF` §3's evidence; the 45/100 weight is inherited, not re-derived.
9. **Motor unit prices are REV educational list and CTRE educational list.** Retail Kraken pricing
   requires contacting CTRE sales. Team discounts, FIRST Choice credits, and voucher programs are
   not modeled anywhere in this file and can move real spend by hundreds of dollars.
10. **Module masses come from one vendor.** Only Thrifty publishes per-config mass on its product
    page. §8.3's AM14U6 figure is `[S]`. Do a real weight study from CAD before committing.
