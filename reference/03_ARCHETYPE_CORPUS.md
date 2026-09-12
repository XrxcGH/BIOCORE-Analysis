# Archetype Corpus — the calibration set the achievability rubric is back-tested against

**Purpose:** give the rubric a labelled test set. 30 strategy/design archetypes drawn from five
real FRC seasons (2022–2026), each carrying the same 13 fields, each with a *known* competitive
outcome and a *known* small-team verdict. When the rubric scores BIOCORE strategies on
2027-01-09, these are the records it must reproduce first. Effort is weighted toward **2026
REBUILT** — freshest data, largest scraped sample, and the manual whose structure BIOCORE most
plausibly resembles.

**Companion file:** [`reference/archetype_corpus.yaml`](archetype_corpus.yaml) — one machine-readable
entry per archetype, all fields below, consumed by the rubric back-test harness.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified against a primary source in this corpus (manual text or scraped TBA data) |
| **[H]** HISTORICAL-PATTERN | Observed across prior FRC seasons; not stated for BIOCORE |
| **[S]** SPECULATION | Inference — cost bands, cycle estimates, difficulty ratings. Flagged as such |
| **UNVERIFIED** | Could not be checked from local data |

**Source shorthand**

`REB` = 2026 REBUILT (TU22, 166 pp) · `REEF` = 2025 REEFSCAPE (V3, 164 pp) ·
`CRES` = 2024 CRESCENDO (V5, 153 pp) · `CHRG` = 2023 CHARGED UP (V4, 142 pp) ·
`RAPD` = 2022 RAPID REACT (V7, 136 pp). PDFs in
[`manuals/archive/frc/`](../manuals/archive/frc/), text mirrors in
[`manuals/archive/frc/_txt/`](../manuals/archive/frc/_txt/). Neither is in the repository, because
FIRST's text is not redistributed: from the repository root, `bash tools/rebuild-corpus.sh --fetch`
downloads the PDFs and `bash tools/rebuild-corpus.sh` rebuilds the text mirrors.
`TBA` = scraped Blue Alliance data in [`research/predictive_tba/`](../research/predictive_tba/)
(30,986 team-event COPR rows, 115,390 alliance-scores, 2023–2026).
`PF` = [`reference/04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md) (DONE — factor weights).
`AW` = [`reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`](awards/00_AWARD_LIST_EMPIRICAL_2026.md) (DONE — exact 2026 award names).

> **Scope guard.** BIOCORE is **FRC**, kickoff **2027-01-09 12:00 ET**. Nothing here draws on FTC
> BIOBUZZ — no Pollen, no StarterBots, no Skill Builders. BIOCORE's scoring element name and specs
> are not public as of 2026-08-22. Every point value below belongs to a *prior* FRC season and is
> `[C]`-for-that-season, never `[C]`-for-BIOCORE. See
> [`research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md).
> **2027 also replaces the roboRIO with Systemcore** — every programming-difficulty rating in this
> file carries a +0.5 to +1.0 first-season penalty until the new control system's library maturity
> is known. See §9.4.

---

## 0. Kickoff-day 60-second workflow

Run this at 12:05 p.m. ET on **2027-01-09**, once the BIOCORE manual PDF is on disk. Everything
below was run against `REB` while writing this file; quoted outputs in §10 are verbatim.

```bash
# Run from the repository root.
M="manuals/2026-27_BIOCORE/BIOCORE_GameManual.pdf"    # the file you download at 12:00 ET
mkdir -p manuals/archive/frc/_txt
pdftotext -layout "$M" manuals/archive/frc/_txt/2027_BIOCORE.txt
T=manuals/archive/frc/_txt/2027_BIOCORE.txt

# --- 1. the point table: the only input the archetype slots actually need (~10 s) ---
grep -n -A45 -iE "point values" "$T" | head -60

# --- 2. how many scoring LOCATIONS / TIERS are there? -> caps the archetype count -----
grep -oiE "(LEVEL|L)[ ]?[1-4]\b" "$T" | sort | uniq -c | sort -rn | head
grep -oiE "\b[A-Z]{3,10} (RP|BONUS RP)\b" "$T" | sort | uniq -c | sort -rn | head

# --- 3. is there a possession cap? uncapped == volume game == archetype I1 dominates --
grep -oiE "may (not )?(simultaneously )?[Cc]ontrol (any amount|more than [0-9]+)" "$T" | sort -u
# REB output: "may control any amount"  -> uncapped

# --- 4. how high must a scoring element go? sets the mechanism floor ------------------
grep -oiE "(opening|goal|target|rim).{0,60}[0-9]{2,3}(\.[0-9])?in.{0,30}(off the (carpet|floor|ground))" "$T" | sort -u
# REB output: HUB opening front edge "72in (~1.83m) off the carpet" -> launcher effectively required

# --- 5. is defense legal where the points are? (only PROTECTION zones restrict it) -----
grep -oiE "[A-Z][A-Z/ ]{2,28} protection\.[^.]{0,200}" "$T" | sort -u
# REB output: TOWER protection ONLY -> neutral-zone defense unrestricted

# --- 6. instantiate the seven invariants against this game -----------------------------
python - <<'PY'
import sys
try: import yaml
except ImportError: sys.exit("pip install pyyaml, or read reference/archetype_corpus.yaml by hand")
d = yaml.safe_load(open("reference/archetype_corpus.yaml"))
for inv in d["invariants"]:
    print("%-38s %-7s  %s" % (inv["name"], inv["seasons_present"], inv["biocore_slot_prompt"]))
PY
# verbatim output (2026-08-22):
# Reliable high-volume single-task scorer 5/5   What is the single highest-frequency scoring action, and can it be done from one fixed position?
# Do-everything robot                    5/5   Do NOT fill this slot. Record it only so there is something explicit to reject.
# Defense specialist                     5/5   Is there any period, zone or state in which our own scoring is impossible or worthless?
# Endgame specialist                     5/5   What is the largest single-action point value in the last 30 seconds, and what is its RP threshold?
# AUTO specialist                        5/5   What does the AUTO period pay EXTRA for, versus TELEOP? Express it as a ratio.
# Feeder / support robot                 5/5   Can a robot with NO scoring mechanism materially raise a partner's rate? Name the field feature it exploits.
# Deliberately-minimal flawless robot    5/5   What is the cheapest action that scores something at all, every single match?
# --- 7. score each slot with the rubric, using this corpus as the calibration set ------
# python tools/rubric_weights.py "$M"        # see reference/04_PREDICTIVE_FACTORS.md §0
```

Expected total: **under 60 seconds**. Step 6 prints seven blank slots. Filling them is the
kickoff-day strategy deliverable; §9 says what a good answer looks like for each.

---

## 1. Field schema — how to read every record

Each archetype record carries these 13 fields. The YAML uses the same key names.

| Field | Values / units | Notes |
|---|---|---|
| `scoring_actions` | free text | The specific manual-named actions this robot targets, nothing else |
| `points_per_cycle` | points | A "cycle" = acquire → travel → score → return. `[S]` unless taken straight from the point table |
| `est_cycles_per_match` | integer or `null` | How many such loops fit in the scoring window. `null` for continuous/support roles `[S]` |
| `mechanism_count` | integer | Powered subsystems **beyond** the drivetrain. Intake=1, indexer=1, shooter=1, climber=1 |
| `drivetrain` | `tank` / `swerve` / `either` | `either` means the archetype has been executed well on both |
| `sensing` | `none` → `full-pose` | 5 tiers: none · encoders · gyro+encoders · vision-assist (AprilTag range/yaw) · full-pose (odometry fusion) |
| `marginal_cost_usd` | band, USD | **Beyond** a base drivetrain + control system. Excludes the drivetrain itself `[S]` |
| `mfg_floor` | `hand` / `bandsaw+drill` / `router` / `CNC` | Minimum shop needed to hit the tolerances the archetype requires |
| `programming_difficulty` | 1–5 | 1 = teleop mapping only. 5 = closed-loop + vision + multi-step autonomous |
| `drive_practice_sensitivity` | `low` / `med` / `high` / `extreme` | How much output collapses without practice hours |
| `reliability_profile` | free text | The specific failure mode and whether it is graceful or total |
| `outcome` | see below | What actually happened to this archetype competitively |
| `small_team_verdict` | `YES` / `CONDITIONAL` / `MARGINAL` / `NO` | Did a ~15-student, low-budget team execute it *well*? |

**`outcome` vocabulary** — `event-winning` (routinely on winning alliances) ·
`captain-tier` (routinely an alliance captain) · `first-pick` · `second-pick` ·
`third-pick/backup` · `unpicked` (built, rarely rewarded).

**`small_team_verdict` vocabulary** —
`YES` = repeatedly executed well by low-resource teams ·
`CONDITIONAL` = works only if a named precondition holds (stated per record) ·
`MARGINAL` = possible but the cost/benefit is poor for 15 students ·
`NO` = requires resources this team does not have.

**Base-rate anchor for every verdict below** `[C]` TBA — computed over 765 event-winning alliances,
2023–2026:

| Season | Winning alliances containing a **below-median-OPR** member | #1 seeds containing one |
|---|---:|---:|
| 2023 CHARGED UP | 115/179 = **64%** | 71% |
| 2024 CRESCENDO | 125/182 = **69%** | 68% |
| 2025 REEFSCAPE | 135/198 = **68%** | 71% |
| 2026 REBUILT | 160/206 = **78%** | 81% |

> **The single most important number in this file.** Two-thirds to four-fifths of *winning*
> alliances carry a below-median-scoring robot. The support, defense, endgame and minimal
> archetypes are not consolation prizes — they are the statistically normal path onto a winning
> alliance. In REBUILT that path was *wider* than in any prior season in the set.

Second anchor `[C]` TBA — the **deepest-picked** team at a median event sits at the following OPR
percentile (0% = best robot at the event):

| Season | median deepest pick | 90th-pct event |
|---|---:|---:|
| 2023 | 85th pctile | 95th |
| 2024 | 82nd | 96th |
| 2025 | 88th | 96th |
| 2026 | **90th** | **97th** |

At half of 2026 events, a robot in the *bottom decile* of OPR was still selected. Being picked is
not gated on scoring. It is gated on being **legible, reliable, and useful** — which is what the
archetype fields measure.

---

## 2. 2026 REBUILT — the primary calibration season

### 2.1 Game facts this section rests on `[C]` REB

| Fact | Value | Manual location |
|---|---|---|
| SCORING ELEMENT | FUEL — 5.91 in (15.0 cm) high-density foam ball, 0.448–0.500 lb | §5.10.1 |
| FUEL staged per match | **504** (600 at DCMP/Champs); 24 per DEPOT, 24 per OUTPOST CHUTE, up to 8 preloaded per ROBOT | §6.3.4 |
| Possession cap | **NONE** — "may control any amount of fuel at a time" | §3 overview |
| HUB | 47 × 47 in prism, 158.6 in from ALLIANCE WALL; **41.7 in hexagonal top opening, front edge 72 in off carpet** | §5.4 |
| TOWER | 78.25 in tall, integrated into ALLIANCE WALL; LEVEL 1/2/3 | §5.8 |
| AUTO | **20 s** | Table 6-2 |
| TELEOP | 2:20 — TRANSITION SHIFT 10 s, SHIFT 1–4 @ 25 s each, END GAME 30 s | Table 6-2 |
| **HUB active/inactive** | Both active in AUTO, TRANSITION, END GAME. During SHIFT 1–4 **only one alliance's HUB is active**, alternating. The alliance that scored **more** FUEL in AUTO is **inactive first** | §6.4.1, Table 6-3 |
| Point values | FUEL in active HUB **1** (AUTO and TELEOP). FUEL in inactive HUB **0**. TOWER L1 **15 AUTO / 10 TELEOP** (max 2 robots in AUTO), L2 **20**, L3 **30** | Table 6-4 |
| BONUS RP (Regional/District) | ENERGIZED **100** FUEL · SUPERCHARGED **360** FUEL · TRAVERSAL **50** TOWER points | Table 6-5 |
| Defense restriction | **TOWER protection only.** Neutral-zone defense unrestricted; 5-count on PINS | §7 (G-rules) |

**Derived, and load-bearing** `[S]`: your HUB is active for **110 s of 160 s** (AUTO 20 + TRANSITION
10 + two 25 s SHIFTS + END GAME 30). For 50 s you *cannot score at all*. That is the defining
structural fact of REBUILT and the reason its defense archetype is the strongest in this corpus.

**Scoring distribution** `[C]` TBA, n = 30,352 alliance-scores:

| Season | median | p25 | p75 | p90 | p99 | p99/median |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 87 | 62 | 114 | 139 | 178 | 2.0× |
| 2024 | 50 | 35 | 68 | 87 | 121 | 2.4× |
| 2025 | 93 | 63 | 128 | 169 | 236 | 2.5× |
| **2026** | **147** | 78 | 253 | 374 | 608 | **4.1×** |

Individual COPR, 2026, n = 8,160 team-events: median **38.5**, p90 **153.4**, p99 **270.6**,
max **470.7**. The p99/median ratio of 7.0× (vs 3.1× in 2024) is the signature of an **uncapped
volume game**: elite teams run away, and a median team's absolute contribution stops mattering.
This directly justifies REBUILT's high defense and support verdicts.

### 2.2 REBUILT archetype records — identity and scoring

| ID | Archetype | Scoring actions targeted | Points per cycle | Cycles/match | Mech | Drivetrain | Sensing |
|---|---|---|---|---|---:|---|---|
| **R1** | Cycle Cannon (turreted high-rate shooter) | FUEL → active HUB from mid-field, continuous | 25–40 FUEL per trip `[S]` | 5–7 in 110 s | 3–4 | swerve (strongly) | vision-assist → full-pose |
| **R2** | Fixed-Zone Bulk Shooter | FUEL → active HUB from **one surveyed spot**; no turret, one hood angle | 8–15 FUEL `[S]` | 5–6 | 2–3 | either | encoders (shooter RPM) |
| **R3** | Neutral-Zone Herder / Feeder | 0 direct. Sweeps NEUTRAL ZONE FUEL to partners / into DEPOT / to OUTPOST | 0 pts; +20–40% partner throughput `[S]` | continuous | 1 | either | none |
| **R4** | TOWER Climber Specialist (L3) | TOWER L3 = **30** in END GAME; contributes 30 of TRAVERSAL's 50 | 30 | 1 | 1–2 | either | encoders + limits |
| **R5** | AUTO Specialist | 8 preloads + DEPOT FUEL in the 20 s AUTO; optional L1 = **15** | 12–30 pts of AUTO `[S]` | 1 | 0 extra | either | full-pose |
| **R6** | Shift Defender / HUB Denier | 0 direct. Denies opponent's two 25 s active SHIFTS | 0 pts; −30–60 opp. pts `[S]` | 2 windows | 0–1 | swerve or 6WD traction | none |
| **R7** | Depot Cycler / Lift Dumper | FUEL → HUB by **lifting over the 72 in lip**, short DEPOT loop | 15–25 FUEL `[S]` | 4–5 | 2–3 | either | encoders |
| **R8** | Minimal Flawless (plow + L1) | Herd FUEL; TOWER L1 = 10 TELEOP / 15 AUTO | 10–15 | 1 + herding | 1 | either | encoders |

### 2.3 REBUILT archetype records — build cost and verdict

| ID | Marginal $ USD | Mfg floor | Prog 1–5 | Practice sens. | Reliability profile | Outcome | Small-team verdict |
|---|---:|---|---:|---|---|---|---|
| **R1** | $1,200–2,400 | router → CNC | 5 | high | Indexer jams under 30-ball loads; flywheel wear shifts range mid-event. Failure is **partial** (rate drops) | **event-winning** — top-COPR robots in 2026 are all FUEL-volume | **NO** at full spec. The turret + full-pose stack is where 15-student teams lose the season |
| **R2** | $600–1,100 | bandsaw+drill | 2 | med | One RPM setpoint, one distance. Failure = you miss the whole burst until re-aligned. **Graceful** | **first/second-pick** | **YES** — the highest-value small-team play in REBUILT. Same points as R1 at ⅓ the cost, 40% of the rate |
| **R3** | $150–450 | hand tools | 1 | med | Nothing to break. Plow bends, keeps working | **second/third-pick** | **YES** — but pick equity is weak *alone*; pair with R4 |
| **R4** | $250–700 | bandsaw+drill (winch) · router (telescope) | 2 | high | Single-shot. Miss the hook = **0**. No partial credit | **second-pick**, TRAVERSAL-RP gating | **YES** — 30 pts is 20% of the 147-pt median match from one 15 s action |
| **R5** | $0–350 (odometry only) | none (software) | 4 | low | Fails to a stationary robot; costs nothing else | **captain-tier multiplier** | **YES** — best pts-per-dollar in the corpus. See §9.4 Systemcore caveat |
| **R6** | $0–350 | hand tools | 1 | **extreme** | No mechanism to fail; risk is **fouls**, not breakage | **second/third-pick**; 78% of 2026 winners carried a below-median robot | **YES** — REBUILT is the strongest defense season in this corpus, purely because of the SHIFT structure |
| **R7** | $700–1,500 | router | 3 | med | Elevator/conveyor is the most jam-prone path; a stuck FUEL kills the run. **Total** failure | **third-pick/backup** | **MARGINAL** — the 72 in front lip makes lifting cost more per point than shooting |
| **R8** | $250–550 | hand tools → bandsaw | 2 | med | Two independent simple systems; degrades gracefully | **third-pick** | **YES** — the safe floor, but 10–15 pts is a thin share of a 147-pt median match |

### 2.4 REBUILT reading — what the calibration set must learn

1. **Uncapped + 1 pt/element + 504 elements = a rate game.** With no possession cap and a 4.1×
   p99/median spread, marginal points come from *throughput*, not from unlocking a higher-value
   location. A rubric that scores "can we reach the top tier?" would mis-rank REBUILT entirely.
   `[C]` REB §5.10 + TBA.
2. **The SHIFT mechanic makes defense free.** For 50 s your HUB is dead. The manual itself says
   robots "may perform defensive strategies or collect more fuel while their hub is inactive"
   (§3 overview). A defense specialist gives up *nothing*. This is why R6 rates `YES` here and
   only `CONDITIONAL` in most seasons. `[C]` REB §6.4.1.
3. **Winning AUTO is a mixed blessing.** The alliance that scores more FUEL in AUTO has its HUB
   set **inactive** for SHIFT 1. AUTO points are real and permanent; the ordering penalty is
   nominal, but it means R5's value is in *points banked*, not in tempo. `[C]` REB Table 6-3.
4. **72 in scoring lip is the mechanism gate.** Any archetype delivering FUEL must clear 72 in.
   That is why R7 (lift) rates below R2 (shoot) despite a shorter travel loop. In BIOCORE, find
   this number first — §0 step 4. `[C]` REB §5.4.
5. **TRAVERSAL RP = 50 TOWER points** is reachable with **one L3 + one L2** (30 + 20), i.e. two of
   three robots. An alliance shopping for its third pick will pay for a reliable L2/L3 climber.
   `[C]` REB Table 6-5.
6. **SUPERCHARGED RP = 360 FUEL** over a 110 s active window = ~3.3 FUEL/s alliance-wide, ~1.1
   FUEL/s per robot sustained. Only R1-class robots hit it. Small teams should plan around
   **ENERGIZED (100)**, which is ~0.3 FUEL/s per robot and well inside R2's envelope. `[C] + [S]`.

---

## 3. 2025 REEFSCAPE

**Point values `[C]` REEF Table 6-2:** LEAVE 3 (AUTO). CORAL L1 **3/2**, L2 **4/3**, L3 **6/4**,
L4 **7/5** (AUTO/TELEOP). ALGAE in PROCESSOR **6/6**, in NET **4/4**. BARGE: PARK 2, shallow CAGE
**6**, deep CAGE **12**. AUTO RP = all robots LEAVE + ≥1 CORAL. CORAL RP = ≥7 CORAL on each level
(3 levels if Coopertition). BARGE RP = ≥16 BARGE points. Median alliance score **93**, p90 **169**.

| ID | Archetype | Scoring actions | Pts/cycle | Cycles | Mech | DT | Sensing | $ USD | Mfg floor | Prog | Practice | Reliability | Outcome | Small-team verdict |
|---|---|---|---|---|---:|---|---|---:|---|---:|---|---|---|---|
| **F1** | L4 Branch Specialist | CORAL → L4 (7 AUTO / 5 TELEOP) | 5–7 | 8–12 | 3 (elevator, arm, intake) | swerve | vision-assist | $1,400–2,600 | CNC | 4 | high | Elevator tuning drifts; a dropped CORAL on the reef blocks a branch. Partial failure | **event-winning / captain-tier** | **NO** — elevator + articulated wrist to a 6 ft branch is the single most over-attempted mechanism of 2025 |
| **F2** | L1 Trough Filler | CORAL → trough L1 (3/2) | 2–3 | 12–18 | 1–2 | either | encoders | $350–800 | bandsaw+drill | 2 | med | Ground-level delivery; nearly nothing to jam | **second-pick**; gates CORAL RP's L1 row | **YES** — the archetype that quietly earned CORAL RP for hundreds of alliances |
| **F3** | Processor Cycler | ALGAE → PROCESSOR (**6** — highest single action in REEF) | 6 | 5–8 | 2 | either | encoders | $500–1,100 | bandsaw+drill | 2 | med | Compliant-wheel ALGAE grip degrades; failure is graceful | **first/second-pick** | **YES** — 6 pts/element beat L4's 5 in TELEOP for less than half the mechanism |
| **F4** | Deep CAGE Climber | BARGE deep CAGE **12** | 12 | 1 | 1–2 | either | encoders + limits | $400–900 | router | 3 | high | Single-shot; deep cage tolerance is unforgiving. Total failure | **second-pick**; alone nearly satisfies BARGE RP (16) | **CONDITIONAL** — `YES` only if you build the cage-interface fixture and practice ≥50 climbs |
| **F5** | AUTO Specialist | LEAVE 3 + 3–4 CORAL at L4 (7 ea) | 24–31 in AUTO | 1 | 0 extra | swerve | full-pose | $0–400 | software | 5 | low | Path drift compounds; fails to a parked robot | **captain-tier multiplier**; AUTO RP is all-robot-gated | **CONDITIONAL** — `YES` for LEAVE + 1 CORAL (satisfies AUTO RP). `NO` for 4-piece |
| **F6** | ALGAE Defender / Reef Clearer | Remove opponent ALGAE, block PROCESSOR loop | 0 direct | continuous | 0–1 | swerve | none | $0–300 | hand tools | 1 | extreme | No mechanism; foul risk only | **second/third-pick**; 68% of 2025 winners carried a below-median robot | **YES** |

**Reading:** REEFSCAPE is the corpus's clearest case of a **cheaper action out-scoring the
prestige action** — PROCESSOR at 6 pts beat L4 at 5 pts in TELEOP with one-third the mechanism.
The rubric must test for this inversion in BIOCORE (§0 step 1: read *every* row of the point table
before choosing).

---

## 4. 2024 CRESCENDO

**Point values `[C]` CRES Table 6-2** (PDF column extraction is misaligned; values reconciled
against the published table layout — flagged `[C]*`): LEAVE 2 (AUTO). AMP NOTE **2/1**. SPEAKER
NOTE **5/2**. SPEAKER NOTE **AMPLIFIED 5** (TELEOP). PARK 1, ONSTAGE 3, ONSTAGE SPOTLIT 4,
HARMONY 2, NOTE in TRAP 5. MELODY RP = 18 NOTES (15 w/ Coopertition) at Regional/District.
ENSEMBLE RP = ≥10 STAGE points and ≥2 ONSTAGE robots. Median alliance score **50** — the
**lowest** in the set, and the reason defense was decisive.

| ID | Archetype | Scoring actions | Pts/cycle | Cycles | Mech | DT | Sensing | $ USD | Mfg floor | Prog | Practice | Reliability | Outcome | Small-team verdict |
|---|---|---|---|---|---:|---|---|---:|---|---:|---|---|---|---|
| **C1** | SPEAKER Cycler | NOTE → SPEAKER, 2 (5 amplified) | 2–5 | 10–15 | 2–3 | swerve | vision-assist | $900–1,800 | router | 4 | high | Shooter RPM + variable-distance aim; partial failure | **event-winning / captain-tier** | **CONDITIONAL** — `YES` only in the fixed-distance subwoofer variant (see C3) |
| **C2** | AMP Feeder + Amplification Manager | NOTE → AMP (1), then trigger AMPLIFIED window for partners | 1 direct; +3/NOTE to partners | 8–12 | 2 | either | encoders | $500–1,000 | bandsaw+drill | 2 | med | Simple low delivery; graceful | **second-pick**; drives MELODY RP | **YES** — the season's best support archetype |
| **C3** | Subwoofer Camper (fixed-distance shooter) | NOTE → SPEAKER from the fixed subwoofer position only | 2 | 8–12 | 2 | either | encoders | $600–1,100 | bandsaw+drill | 2 | med | One setpoint; contested position is the real risk | **second-pick** | **YES** — the definitive small-team CRESCENDO robot |
| **C4** | STAGE Climber + TRAP | ONSTAGE 3 (SPOTLIT 4) + HARMONY 2 + TRAP 5 | 5–11 | 1 | 2 | either | encoders | $600–1,300 | router | 3 | high | Chain alignment + TRAP delivery at height; single-shot | **second-pick**; ENSEMBLE RP gating | **CONDITIONAL** — `YES` for ONSTAGE only, `NO` with TRAP |
| **C5** | AUTO Specialist | LEAVE 2 + 3–4 SPEAKER at **5** each | 17–22 in AUTO | 1 | 0 extra | swerve | full-pose | $0–400 | software | 5 | low | Fails to parked | **captain-tier multiplier** | **CONDITIONAL** — 2-NOTE auto `YES`, 4-NOTE `NO` |
| **C6** | Defense Specialist | Deny SPEAKER lane, box out AMP | 0 direct | continuous | 0 | swerve | none | $0–250 | hand tools | 1 | extreme | Foul risk only | **second-pick**; 69% of 2024 winners carried a below-median robot | **YES** — the lowest-scoring season (median 50) makes each denied cycle worth the most |

**Reading:** CRESCENDO is the corpus's **defense maximum by score-share** — at a median of 50
points, denying three cycles is ~12% of a match. REBUILT is the defense maximum by *opportunity
cost* (free during your inactive SHIFTS). Both mechanisms must be tested separately in BIOCORE.

---

## 5. 2023 CHARGED UP

**Point values `[C]` CHRG Table 6-2:** MOBILITY 3 (AUTO). GAME PIECE bottom row **3/2**, middle
**4/3**, top **6/5**. LINK (3 adjacent NODES) **5**. SUPERCHARGED NODE 3. DOCKED not ENGAGED
**8/6**, DOCKED and ENGAGED **12/10** (max 1 robot in AUTO). PARK 2. Median alliance score **87**.

| ID | Archetype | Scoring actions | Pts/cycle | Cycles | Mech | DT | Sensing | $ USD | Mfg floor | Prog | Practice | Reliability | Outcome | Small-team verdict |
|---|---|---|---|---|---:|---|---|---:|---|---:|---|---|---|---|
| **G1** | Cube-Only Top-Row Cycler | CUBE → top row (6/5); LINK contribution 5 | 5–6 (+5 LINK) | 6–9 | 2 (intake + arm) | swerve | vision-assist | $800–1,600 | router | 3 | high | CUBE is forgiving geometry; arm setpoints drift. Partial | **first-pick** | **YES** — dropping CONES halved the mechanism problem for a ~15% point loss |
| **G2** | Full-Grid CONE + CUBE Scorer | Both GAME PIECES, all 3 rows, double-substation intake | 5–6 | 8–12 | 3–4 | swerve | full-pose | $1,600–3,000 | CNC | 5 | high | Cone-tip alignment is the season's hardest tolerance. Total failure on a tipped cone | **event-winning / captain-tier** | **NO** |
| **G3** | CHARGE STATION Specialist | AUTO ENGAGED **12** + TELEOP ENGAGED **10** = 22 | 22 | 2 (auto + endgame) | 0–1 | either | gyro (pitch) + encoders | $0–300 | hand tools | 3 | high | Balance loop; a mis-timed partner tips the station. Partial | **second-pick**; ACTIVATION RP gating | **YES** — 22 pts on a 87-pt median from a gyro and a PID loop. Best pts-per-dollar in the corpus |
| **G4** | HYBRID-Row Filler / LINK Facilitator | GAME PIECES → bottom/HYBRID row (3/2), completing LINKs (5) | 2–3 (+5 LINK) | 10–14 | 1 | either | none | $250–600 | hand tools | 1 | low | Push-in delivery; essentially unbreakable | **second/third-pick**; SUSTAINABILITY RP gating | **YES** |
| **G5** | Defense / Floor-Intake Support | Deny COMMUNITY entry; feed partners | 0 direct | continuous | 0–1 | swerve | none | $0–300 | hand tools | 1 | extreme | Foul risk only | **third-pick**; 64% of 2023 winners carried a below-median robot | **CONDITIONAL** — CHARGED UP's protected LOADING ZONE narrowed the useful defense window |

---

## 6. 2022 RAPID REACT

**Point values `[C]` RAPD Table 6-1:** TAXI 2 (AUTO). CARGO in LOWER HUB **2/1**, UPPER HUB
**4/2**. HANGAR per robot: LOW **4**, MID **6**, HIGH **10**, TRAVERSAL **15**. CARGO BONUS RP =
20 CARGO (18 with a QUINTET — ≥5 CARGO in AUTO). HANGAR BONUS RP = ≥16 HANGAR points.

| ID | Archetype | Scoring actions | Pts/cycle | Cycles | Mech | DT | Sensing | $ USD | Mfg floor | Prog | Practice | Reliability | Outcome | Small-team verdict |
|---|---|---|---|---|---:|---|---|---:|---|---:|---|---|---|---|
| **P1** | UPPER HUB Cycler | CARGO → UPPER HUB (4/2) | 2–4 | 10–16 | 3 (intake, indexer, shooter) | swerve | vision-assist | $900–1,800 | router | 4 | high | Two-ball indexer jams; partial | **event-winning / captain-tier** | **CONDITIONAL** — `YES` in the fixed-range variant only |
| **P2** | LOWER HUB Dumper | CARGO → LOWER HUB (2/1) by driving up and dumping | 1–2 | 12–18 | 1–2 | either | none | $200–500 | hand tools | 1 | low | Nearly unbreakable | **third-pick**; contributes to CARGO BONUS RP | **YES** — the canonical minimal-viable RAPID REACT robot |
| **P3** | TRAVERSAL Climber | HANGAR TRAVERSAL **15** | 15 | 1 | 2–3 (static + dynamic hooks) | either | full-pose (arm) | $900–2,000 | CNC | 5 | extreme | Multi-stage, sequenced, timed. Total failure and it eats the last 25 s | **first-pick** | **NO** — the most seductive over-reach in the corpus |
| **P4** | MID-RUNG Climber + Low CARGO | HANGAR MID **6** + LOWER HUB CARGO | 6 + 1–2/cycle | 1 + 10 | 2 | either | encoders + limits | $350–800 | bandsaw+drill | 2 | med | Single winch, one motion. Graceful | **second/third-pick**; 2 MID + 1 HIGH = 22 → HANGAR RP | **YES** — the small-team RAPID REACT answer |
| **P5** | QUINTET AUTO Specialist | ≥5 CARGO in AUTO (drops CARGO RP threshold 20 → 18) + TAXI 2 | 12–22 in AUTO | 1 | 0 extra | swerve | full-pose | $0–400 | software | 5 | low | Fails to a taxi | **captain-tier multiplier** | **CONDITIONAL** — 2-ball `YES`, 5-ball `NO` |

---

## 7. Cross-season invariant archetypes

These seven recur in **every** season in the corpus. BIOCORE will have its own instance of each.
The rubric and the award pairing key on these, not on the season-specific records.

| # | Invariant | Instances | Seasons present | Median mech | Median marginal $ | Mfg floor | Prog | Small-team success |
|---|---|---|---|---:|---:|---|---:|---:|
| **I1** | Reliable high-volume single-task scorer | R1, R2, R7, F1, F3, C1, C3, G1, P1 | 5/5 | 2 | $900 | router | 3 | **4/9** outright; **6/9** restricted to the fixed-range / single-tier variant; **0/4** at full spec |
| **I2** | Do-everything robot | G2, plus the full-spec forms of R1 / F1+F3 / C1+C2+C4 / P1+P3 | 5/5 | 4 | $2,200 | CNC | 5 | **0/5 = 0%** |
| **I3** | Defense specialist | R6, F6, C6, G5 | 5/5 | 1 | $150 | hand tools | 1 | **3/4** YES (G5 CONDITIONAL on the protection rules) |
| **I4** | Endgame specialist | R4, F4, C4, G3, P3, P4 | 5/5 | 2 | $500 | bandsaw+drill | 3 | **3/6** outright; **3/3** at the low/mid tier (R4, G3, P4); **0/3** at the top tier (F4, C4, P3) |
| **I5** | AUTO specialist | R5, F5, C5, P5, (G3 auto-dock) | 5/5 | 0 | $200 | software only | 5 | **2/5** outright; **5/5** scoped to 1–2 elements; **0/3** at full scope |
| **I6** | Feeder / support robot | R3, F2, C2, G4, P2 | 5/5 | 1 | $400 | hand tools | 2 | **5/5 = 100%** |
| **I7** | Deliberately-minimal flawless robot | R8, F2, C3, G4, P2 | 5/5 | 1 | $350 | hand tools | 2 | **5/5 = 100%** |

### 7.1 The four rules the corpus actually teaches

**Rule 1 — the simplified variant of the volume scorer beats the full one, for this team.**
I1 succeeds in **6 of 9** instances when stripped to a fixed range or a single tier (R2, F3, C3, G1,
plus the fixed-range variants of C1 and P1) and in **0 of 4** at full spec (turret + vision +
variable distance: R1, F1, C1-full, P1-full). The delta is entirely mechanism count
and programming difficulty, not concept. **The rubric must score the *variant*, never the family.**

**Rule 2 — I2 (do-everything) has never once been a small-team success in this corpus.**
Five seasons, five failures. Its cost is not additive, it is multiplicative: each extra mechanism
multiplies integration debt, and integration debt is paid in the weeks that would have been drive
practice — the single highest-weighted factor in `PF`. A rubric that lets a strategy score well by
summing capability points is broken; §10.3 is the regression test for this.

**Rule 3 — I3/I6/I7 are how 15-student teams get on winning alliances.**
64–78% of event-winning alliances carried a below-median-OPR robot `[C]` TBA. The support/defense/
minimal cluster has a 80–100% small-team success rate. This is not the fallback plan; it is the
modal winning plan for this team profile.

**Rule 4 — I5 (AUTO) is free money and the only invariant with a 100% success rate at low scope.**
Zero mechanisms, $0–400, software only, and in every season the highest per-second point density
of the match (REBUILT: TOWER L1 pays 15 in AUTO vs 10 in TELEOP; CRESCENDO: SPEAKER pays 5 vs 2;
REEFSCAPE: L4 pays 7 vs 5). The failure mode is **scope**, not capability — 1–2 elements succeeds
5/5, full-field auto succeeds 1/5. **Caveat: see §9.4 on Systemcore.**

### 7.2 Award pairing key `[C]` AW (2026 exact names)

Each invariant has a natural award. Judges reward *legibility*, and these archetypes are the most
legible things a small team builds. Awards named exactly as given at 2026 events.

| Invariant | Best-fit award | Why it pairs |
|---|---|---|
| I1 simplified volume scorer | **Quality Award** · **Industrial Design Award** | A robot that does one thing to a visibly high standard is exactly the Quality pitch |
| I2 do-everything | **Creativity Award sponsored by Rockwell Automation** — *if it works* | The only award that pays for ambition; do not build for it |
| I3 defense specialist | **Judges' Award** · **Gracious Professionalism Award** | Hardest archetype to win a *robot* award with; the culture awards are the realistic route |
| I4 endgame specialist | **Excellence in Engineering Award sponsored by Littelfuse** | A single mechanism with a documented design process is the cleanest Excellence story |
| I5 AUTO specialist | **Autonomous Award sponsored by Google.org** · **Innovation in Control Award sponsored by nVent** | Direct match. The cheapest robot award to target |
| I6 feeder / support | **Industrial Design Award** · **Team Spirit Award** | Design-for-purpose framing; strategic-role storytelling |
| I7 minimal flawless | **Quality Award** · **Excellence in Engineering Award sponsored by Littelfuse** | "It never failed" *is* the Quality Award thesis |

Cross-reference [`reference/awards/01_AWARD_WINNING_PATTERNS.md`](awards/01_AWARD_WINNING_PATTERNS.md)
before writing any pit pitch.

---

## 8. Small-team verdict scoreboard

All 30 records, sorted by verdict. This is the label column the rubric back-test predicts.

| Verdict | Count | Records | Common signature |
|---|---:|---|---|
| **YES** | 17 | R2, R3, R4, R5, R6, R8 · F2, F3, F6 · C2, C3, C6 · G1, G3, G4 · P2, P4 | ≤2 mechanisms · ≤ $1,100 · prog ≤ 3 · mfg floor at or below bandsaw+drill |
| **CONDITIONAL** | 8 | F4, F5 · C1, C4, C5 · G5 · P1, P5 | One named precondition — usually "fixed-range variant only" or "scope to 1–2 elements" |
| **MARGINAL** | 1 | R7 | The mechanism is possible but a cheaper action pays more per dollar |
| **NO** | 4 | R1, F1, G2, P3 | ≥3 mechanisms **and** prog ≥ 4 **and** mfg floor = CNC |

**The verdict predicate, stated as a testable rule** `[H]` — this is the rubric's first regression
test, and it is *deliberately naive*. It reads only cost and complexity.

```
risk = (mechanism_count >= 3)
     + (programming_difficulty >= 4)
     + (mfg_floor in {router, CNC})
     + (marginal_cost_usd_high > 1200)

NO           if risk >= 3
CONDITIONAL  if risk == 2
YES          if risk <= 1
```

It reproduces **21 of 30** hand-assigned verdicts (70%). The nine misses are the interesting part
and are dissected in §10.3 — they are not noise, they are five named blind spots in any
cost-and-complexity-only rubric.

---

## 9. Instantiating the invariants for BIOCORE — the slots to fill on 2027-01-09

Seven blank records. `§0` step 6 prints them. Fill each within 90 minutes of kickoff.

| Slot | Question to answer from the BIOCORE manual | What a good 2027 answer looks like `[S]` |
|---|---|---|
| **I1** | What is the *single* highest-frequency scoring action, and can it be done from one fixed position? | Names one manual action, one distance, one mechanism chain of ≤3 |
| **I2** | *Do not fill this slot.* Record it only to have something to reject | An explicit written "we are not doing this," with the mechanism count that killed it |
| **I3** | Is there any period, zone, or state in which our own scoring is impossible or worthless? | REBUILT's answer was "yes — 50 s of inactive SHIFTS." If BIOCORE has an equivalent, defense is free |
| **I4** | What is the largest single-action point value available in the last 30 s, and what is its RP threshold? | A number and a threshold, e.g. "L3 = 30, TRAVERSAL = 50" |
| **I5** | What does the AUTO period pay *extra* for, versus TELEOP? | A ratio, e.g. "TOWER L1 pays 15 vs 10 = 1.5×" |
| **I6** | Can a robot with **no** scoring mechanism materially raise a partner's rate? | A named field feature (DEPOT, CHUTE, CORRAL analogue) that a plow can exploit |
| **I7** | What is the cheapest action that scores *anything at all* every single match? | One action, ≤1 mechanism, ≤ $500 |

### 9.4 Systemcore adjustment — apply to every programming-difficulty rating `[H]`/`[S]`

2027 replaces the roboRIO with **Systemcore**. Every `programming_difficulty` value in this corpus
was measured under a mature WPILib/roboRIO stack with a decade of community examples. For the 2027
season, before the ecosystem catches up:

| Archetype class | Adjustment | Reason |
|---|---|---|
| Teleop-only, open-loop (I3, I6, I7) | **+0.0** | Motor-controller mapping is the first thing any new control system ships working |
| Single closed-loop mechanism (I4, simplified I1) | **+0.5** | PID/velocity control ports easily; tuning constants do not transfer |
| Odometry / path-following (I5) | **+1.0** | Highest-risk category. Vendor swerve/odometry libraries historically lag a new control system by weeks |
| Vision + pose fusion (full I1, I2) | **+1.0 and treat as unavailable in weeks 1–3** | Coprocessor integration, AprilTag pipelines, and network tables are the last things to stabilise |

**Consequence for the rubric:** I5 (AUTO specialist) is normally this corpus's best pts-per-dollar
play at 100% small-team success. In 2027 it carries a real first-season execution risk. Budget for
**LEAVE-equivalent + one scoring element**, not a multi-element path, until the Systemcore odometry
story is proven at a Week 1 event. Do not delete the AUTO plan — de-scope it.

---

## 10. Validation and dry-run

### 10.1 Corpus integrity check

```bash
# Run from the repository root.
python - <<'PY'
import yaml, collections
d = yaml.safe_load(open("reference/archetype_corpus.yaml"))
a = d["archetypes"]
REQ = ["id","name","season","scoring_actions","points_per_cycle","mechanism_count",
       "drivetrain","sensing","marginal_cost_usd","mfg_floor","programming_difficulty",
       "drive_practice_sensitivity","reliability_profile","outcome","small_team_verdict",
       "evidence"]
bad = [(r["id"], k) for r in a for k in REQ if k not in r]
print("records:", len(a), "| missing fields:", bad or "none")
print("per season:", dict(collections.Counter(r["season"] for r in a)))
print("verdicts  :", dict(collections.Counter(r["small_team_verdict"] for r in a)))
print("invariants:", len(d["invariants"]), "| every archetype mapped:",
      all(r.get("invariant") for r in a))
PY
```

Expected output (verbatim, as of this pass):

```
records: 30 | missing fields: none
per season: {2026: 8, 2025: 6, 2024: 6, 2023: 5, 2022: 5}
verdicts  : {'NO': 4, 'YES': 17, 'MARGINAL': 1, 'CONDITIONAL': 8}
invariants: 7 | every archetype mapped: True
```

> **Gotcha for anyone editing the YAML:** `YES` and `NO` are YAML 1.1 booleans. Every
> `small_team_verdict` value is quoted for that reason. Unquote one and the back-test silently
> collapses to 1/30 agreement — that is the failure this check was written to catch.

### 10.2 Re-derive the two base-rate anchors from raw TBA data

```bash
python - <<'PY'
import csv
from collections import defaultdict
for y in (2023, 2024, 2025, 2026):
    opr = defaultdict(dict)
    for r in csv.DictReader(open(f"research/predictive_tba/tba_copr_{y}.csv")):
        try: opr[r["event"]][r["team"]] = float(r["opr"])
        except ValueError: pass
    al = defaultdict(list)
    for r in csv.DictReader(open(f"research/predictive_tba/tba_alliances_{y}.csv")):
        al[(r["event"], r["alliance"])].append(r)
    hit = tot = 0
    for (e, _), mem in al.items():
        tm = opr.get(e)
        if not tm or len(tm) < 20 or mem[0]["won_event"] != "1": continue
        rank = sorted(tm, key=lambda t: -tm[t])
        pos = {t: i / len(rank) for i, t in enumerate(rank)}
        tot += 1
        hit += any(pos.get(m["team"], 0) > 0.5 for m in mem)
    print(y, f"{hit}/{tot} = {100*hit/tot:.0f}% of winning alliances had a below-median-OPR member")
PY
```

Verbatim output from this pass:

```
2023 115/179 = 64% of winning alliances had a below-median-OPR member
2024 125/182 = 69% of winning alliances had a below-median-OPR member
2025 135/198 = 68% of winning alliances had a below-median-OPR member
2026 160/206 = 78% of winning alliances had a below-median-OPR member
```

### 10.3 Back-test: the §8 predicate against the hand-assigned verdicts

```bash
python - <<'PY'
import yaml
a = yaml.safe_load(open("reference/archetype_corpus.yaml"))["archetypes"]
ok, miss = 0, []
for r in a:
    risk = ((r["mechanism_count"] >= 3) + (r["programming_difficulty"] >= 4)
            + (r["mfg_floor"] in ("router", "CNC")) + (r["marginal_cost_usd"][1] > 1200))
    p = "NO" if risk >= 3 else ("CONDITIONAL" if risk == 2 else "YES")
    ok += p == r["small_team_verdict"]
    if p != r["small_team_verdict"]:
        miss.append(f'{r["id"]}:{p}!={r["small_team_verdict"]}')
print(f"predicate agreement: {ok}/{len(a)} = {100*ok//len(a)}%")
print(f"misses({len(miss)}):", " ".join(miss))
PY
```

Verbatim output from this pass:

```
predicate agreement: 21/30 = 70%
misses(9): R7:NO!=MARGINAL F4:YES!=CONDITIONAL F5:YES!=CONDITIONAL C1:NO!=CONDITIONAL
           C5:YES!=CONDITIONAL G1:CONDITIONAL!=YES G5:YES!=CONDITIONAL P1:NO!=CONDITIONAL
           P5:YES!=CONDITIONAL
```

**The nine misses are the finding, not a bug.** They fall into five named families, and each one
names a dimension the rubric must add.

| # | Family | Records | Predicate → hand | Root cause | Fix the rubric needs |
|---|---|---|---|---|---|
| **A** | Scope-conditional AUTO | F5, C5, P5 | YES → CONDITIONAL | The predicate cannot see **scope**. A 1-element auto and a 4-element auto have *identical* cost, mechanism count and mfg floor, and opposite verdicts | Add a `scope` dimension. Score the scoped variant, not the family |
| **B** | Fixed-range variant of a volume scorer | C1, P1 | NO → CONDITIONAL | The predicate scores the full-spec family; the hand label scores the best available **variant**. Same root cause as A | Enumerate variants as separate rubric candidates *before* scoring |
| **C** | Rule-dependent defense window | G5 | YES → CONDITIONAL | CHARGED UP's protected LOADING ZONE narrowed where defense was legal. Invisible to a cost predicate | Read the protection rules first (§0 step 5) and gate I3 on the result |
| **D** | Borderline cost / mfg floor | G1, F4 | CONDITIONAL → YES, YES → CONDITIONAL | Adjacent-class error. The band straddles the $1,200 cut, and `mfg_floor: router` is over-weighted when only *one* part needs that floor | Make `mfg_floor` a graded term weighted by how many parts need it |
| **E** | Economic, not feasibility | R7 | NO → MARGINAL | `MARGINAL` is outside the predicate's output range by construction — it means "feasible, but a cheaper action pays more per dollar" | Add a dominance check: flag MARGINAL when another archetype beats it on every field |

Families **A** and **B** are the same defect seen twice, and it is exactly §7.1 Rule 1 showing up
as a measurable prediction error: *the rubric must score variants, never families*. That single fix
recovers 5 of the 9 misses.

**One further term the predicate needs, which no miss reveals** — because all four defense records
happen to land on the correct side by luck:

```
downgrade YES -> CONDITIONAL if drive_practice_sensitivity == "extreme"
                              and available_drive_hours_before_event_1 < 20
```

R6, F6 and C6 are trivially cheap and trivially simple, so the predicate rates them `YES` and the
hand label agrees — but their *entire* cost is driver hours, an input the predicate cannot see. It
is right for the wrong reason. This term is consistent with `PF`'s highest-weighted factor (drive
practice, weight 90), reached from independent evidence.

### 10.4 Falsification checks — what would break this corpus

| Check | If it fails, the corpus is wrong about… |
|---|---|
| Is BIOCORE's element **capped** in possession? | Rule 1. A cap compresses the score spread and I1's simplified variant loses its edge |
| Does BIOCORE have a **period or state where scoring is impossible**? | I3's REBUILT-strength verdict. Without it, defense drops back to `CONDITIONAL` |
| Is the top scoring tier worth **>2× the bottom tier**? | I7. In REBUILT (1 pt flat) minimal robots contribute little; in a 2×+ game they contribute less still |
| Does an RP threshold exist that **one cheap robot** can nearly satisfy alone? | I4's `YES`. REBUILT TRAVERSAL (50 from L3+L2) and REEFSCAPE BARGE (16 from one deep cage) both did |
| Is AUTO **longer than 15 s** and paid at a premium? | I5. A 20 s AUTO paying 1.5× (REBUILT) is worth software effort; a 10 s AUTO paying 1× is not |

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/03_ARCHETYPE_CORPUS.md` | This document — 30 archetype records across 2022–2026, 7 cross-season invariants, award pairing key, BIOCORE instantiation slots, validation harness |
| `reference/archetype_corpus.yaml` | Machine-readable companion — one entry per archetype with all 13 fields plus `evidence` and `invariant`; the 7 invariants with success rates and BIOCORE slot prompts; the `NO` predicate as data |

Nothing else was written. Files marked DONE in the project brief were read and cited, not modified.

## Known limitations

1. **Archetype membership is expert-assigned, not measured.** TBA publishes scores, not designs.
   No public dataset labels a robot as "fixed-zone shooter" vs "turreted shooter." Every record's
   `mechanism_count`, `mfg_floor`, `sensing` and `marginal_cost_usd` is `[S]` — a reconstruction
   from the manual's requirements plus the mentor's knowledge of the season, not a survey.
   Only the point values, RP thresholds, field dimensions and the TBA-derived base rates are `[C]`.
2. **`outcome` is a season-level generalisation.** "event-winning" means the archetype was
   routinely present on winning alliances, not that every instance won. Per-archetype win rates
   cannot be computed without robot-design labels (see 1).
3. **COPR ≠ contribution.** The below-median-OPR base rate in §1 uses OPR percentile as a proxy
   for "did not score much." A defense robot and a broken robot look identical in that column.
   The rate is therefore an **upper bound** on how often a *deliberate* support archetype was on a
   winning alliance.
4. **2022 has no scraped TBA data** in this repo (`research/predictive_tba/` starts at 2023), so
   RAPID REACT records rest on the manual and on pattern, with no local outcome statistics.
5. **CRESCENDO point values were reconciled, not read cleanly.** The `pdftotext` extraction of
   `CRES` Table 6-2 misaligns its columns; values were reconciled against the published table
   layout and are labelled `[C]*`. Re-verify against the PDF before quoting them externally.
6. **Cost bands are 2026 USD and exclude the drivetrain, control system, and the Systemcore
   changeover.** 2027 control-system pricing is unknown as of 2026-08-22 and is deliberately
   absent rather than guessed. Treat every `marginal_cost_usd` as ±40%.
7. **No BIOCORE content.** Zero archetypes in this file describe BIOCORE. The game is not public.
   §9's slots are empty by design and are the kickoff-day deliverable.
8. **Programming difficulty is pre-Systemcore.** §9.4 gives the adjustment, but the adjustment
   itself is `[S]` — no 2027 control-system software has shipped for evaluation.
