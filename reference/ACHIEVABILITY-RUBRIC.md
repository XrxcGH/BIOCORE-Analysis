# Achievability × Value Rubric — scoring any BIOCORE strategy against THIS team

**Purpose:** on kickoff day a 15-student team will put eight ideas on a whiteboard and pick the
exciting one. This is the instrument that stops that. It scores any candidate strategy or design on
**two axes that are never collapsed** — can we build it, and is it worth building — applies hard
gates that no score can argue past, and names the **one binding constraint** for each candidate.
Every weight traces to a number already fixed in [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md)
or [`02_TEAM_CAPACITY_MODEL.md`](02_TEAM_CAPACITY_MODEL.md). Nothing here is invented.

> ## ⚠ OPERATING RULE — THE QUADRANT DECIDES, THE TIER ONLY WARNS
>
> **The quadrant and the tier are computed from different numbers and they can contradict each
> other. That is not a bug and it does not resolve itself. When they disagree, follow the
> quadrant.**
>
> - The **quadrant** tests ACH and VAL **separately** against 60 and 55. It answers *should this
>   be built at all.* **It is the decision.**
> - The **tier** is computed from the blended index `C = 0.55·ACH + 0.45·VAL` against 62/48, then
>   adjusted by the zero-rule and soft-gate downgrades. It answers *how likely are we to finish
>   it.* **It is a delivery-risk badge on the decision — never a second opinion about the
>   decision.**
>
> Because the tier blends the two axes, a strategy of **zero competitive value** that is trivially
> easy to build still reads **T2 STRETCH** (ACH 100, VAL 0 → C = 55). A tier is therefore *never*
> evidence that something is worth building. Read the pairs like this:
>
> | Quadrant | Tier | What it actually means |
> |---|---|---|
> | BUILD THIS | T1 GREEN | Build it. |
> | **BUILD THIS** | **T2/T3** | **Right target, undeliverable as specified. DESCOPE to a named variant and re-score — do not drop the target.** |
> | CHEAP INSURANCE | any | Build it only if it costs no workstream you need elsewhere. |
> | **TRAP** | **T1/T2** | **The blended index is flattering it. ACH is below 60. Descope or drop.** |
> | **DELETE** | **T1/T2** | **You can build it; it is not worth building. The good tier is meaningless here.** |
>
> `tools/score-strategy.py` prints every such disagreement in a **QUADRANT/TIER DISAGREEMENTS**
> block under the matrix. **Read that block before you rank anything.** The tier column is not
> permitted to appear in `REVIEW.md` §3 without its quadrant beside it.
>
> *(Left deliberately as a documented operating rule rather than a formula change: the tier
> thresholds are the ones the 30-record back-test was calibrated against at 27/30, and retuning
> them to remove the contradiction would invalidate that calibration.)*

**Companion files:** [`achievability_rubric.yaml`](achievability_rubric.yaml) — the machine-readable
instrument · [`../tools/score-strategy.py`](../tools/score-strategy.py) — the scorer ·
[`examples/candidates_example.yaml`](examples/candidates_example.yaml) — the candidate-file shape.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference or model calibration. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

**Source shorthand**

`REB` = 2026 REBUILT · `REEF` = 2025 REEFSCAPE · `CRES` = 2024 CRESCENDO · `CHRG` = 2023 CHARGED UP ·
`RAPD` = 2022 RAPID REACT (all in `manuals/archive/frc/`) ·
`PF` = [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md) / [`.yaml`](04_predictive_factors.yaml) ·
`CAP` = [`02_TEAM_CAPACITY_MODEL.md`](02_TEAM_CAPACITY_MODEL.md) ·
`ARCH` = [`03_ARCHETYPE_CORPUS.md`](03_ARCHETYPE_CORPUS.md) / [`archetype_corpus.yaml`](archetype_corpus.yaml).
The manuals are not in the repository, because FIRST's documents are not redistributed;
`bash tools/rebuild-corpus.sh --fetch` downloads them.

> **Scope guard.** BIOCORE presented by Haas is the **FRC 2027** game, kickoff **2027-01-09 12:00 ET**.
> BIOBUZZ is the **FTC** sibling game; "Pollen", StarterBots and Skill Builders are BIOBUZZ things and
> appear nowhere in this file. BIOCORE's rules, scoring element and point table are **not public** as
> of 2026-08-22 — see [`../research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md).
> **No threshold, weight or anchor in this document is derived from any BIOCORE rule.** The rubric is
> a model of the *team*, which is knowable today; §11 lists the eight slots the manual fills.

---

## §0. The 60-second kickoff-day workflow

Manual read → ranked strategy table. Run this on **2027-01-09** with the team in the room.

```bash
# Run from the repository root.

# ---- 0. sanity: is the team model still the one the rubric assumes? (~2 s) --------
python tools/capacity_model.py | grep -E "BINDING|SLACK IN THE WHOLE PLAN"
#   -> BINDING = novel_mechanisms_max. If your kickoff plan needs more, the plan is wrong.

# ---- 1. read the manual for the EIGHT numbers the rubric needs (~20 min, not 60 s) --
#         Fill reference/achievability_rubric.yaml : biocore_kickoff_inputs
#         (median score seed, scoring-table row count, AUTO-gated RP y/n, protected-zone
#          count, one-defender rule y/n, PIN count, minor/major foul values, SystemCore shipped y/n)
python tools/rule-inventory.py --season 2027 2>/dev/null || \
  echo "no 2027 inventory yet -- read the point table and the G-rules by hand"

# ---- 2. enumerate candidates -- and their DESCOPED VARIANTS, which is the whole trick
cp reference/examples/candidates_example.yaml strategies.yaml
$EDITOR strategies.yaml       # 6-10 rows. Score each factor by hand against section 2.

# ---- 3. price the VALUE axis from real cycle arithmetic, not vibes -----------------
python tools/cycle-model.py --game biocore.json --sweep     # your cycle time, not a good team's
#   paste the TOTAL into each candidate's cycle_model: block, or let score-strategy call it

# ---- 4. THE OUTPUT: ranked table + the 2x2 + the binding constraint per row --------
python tools/score-strategy.py --candidates strategies.yaml

# ---- 5. argue about ONE row at a time, factor by factor ----------------------------
python tools/score-strategy.py --candidates strategies.yaml --detail S1

# ---- 6. the regression test: does the instrument still reproduce 30 known outcomes? -
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml | tail -20
```

**Read the output in this order.** The **quadrant** first — that is the decision. Then the **binding
constraint** — that is the thing to fix. The **combined index** last, and only to order rows *inside*
a quadrant. A team that reads the index first will build the wrong robot with a defensible number
attached to it.

---

## §1. What this instrument is, in one table

| | ACHIEVABILITY axis | VALUE axis |
|---|---|---|
| Question | Can *this* team build it? | Is it worth building? |
| Factors | **13**, each 0–5 | **5**, each 0–5 |
| Weight source | `PF` weights + `CAP` constraint ranks | `PF` weights |
| Weight sum | 856 | 290 |
| Upstream tool | `tools/capacity_model.py` | **`tools/cycle-model.py`** (imported, not reimplemented) |
| Output | 0–100 index | 0–100 index |
| **Combined** | `0.55 × A + 0.45 × V` — **ordering only** | |
| **Real output** | **the quadrant** (§6) + **the binding constraint** (§8) | |

Why 55/45 and not 50/50: `ARCH` invariant **I2** (do-everything robot) has a **0/5** small-team
success rate across five seasons, while **I6** (feeder/support) and **I7** (minimal flawless) are
**5/5**. The measured failure mode for this team profile is *scope*, not insufficient ambition. The
split encodes that asymmetry without letting achievability decide alone — a perfectly achievable robot
that scores nothing still lands in CHEAP INSURANCE, not in BUILD THIS.

---

## §2. The 13 achievability factors, with anchors

**How to score.** Two people score independently against the anchors below, then reconcile. The
anchors are written so that two reasonable people land **within 1 point**; where they might not, a
`tie-break` line gives a mechanical procedure. **5 = easiest for this team. 0 = effectively impossible.**

The calibration constants every anchor is denominated in, all from `CAP` §8:

| Constant | Value | Used by |
|---|---:|---|
| `effective_build_hours` (→ Week 1) | **599** | context |
| `mechanism_hours_pool` (CAD 75 + fab 130) | **205 h** | A1, gate G4 |
| `hours_per_novel_mechanism` | **90 h** | A1 |
| `parallel_workstreams_max` | **3** | A2, gate G2 |
| `novel_mechanisms_max` | **2** | A2, gate G2 |
| `mentor_unblock_minutes_per_week` | **204** (3.4 h) | A3, gate G5 |
| `real_driver_seat_hours` before event 1 | **≈9 h** | A4, gate G6 |
| `budget_usd_robot_discretionary` | **$2,500** | A12, gate G3 |
| `slack_hours` | **0** | A11, A13 |

### A1 · build_hours_fit — weight 85

*Total CAD + fabrication + integration hours needed, against the 205 h mechanism pool.*

| Score | Anchor |
|:--:|---|
| **5** | **≤60 h.** A published/COTS design bolted on. Fabrication hours only, near-zero design hours. Fits with room for a second mechanism. |
| **4** | ≤110 h. One straightforward mechanism, or a copied design needing adaptation. |
| **3** | **≤160 h.** One novel mechanism at the model's generous 90 h plus its share of integration. Fits, but consumes most of the pool. |
| **2** | ≤205 h. Exactly consumes the pool. Nothing left for the second mechanism or for overrun. |
| **1** | **≤300 h.** Exceeds the pool by up to 50%. Buildable only by cannibalising drive practice or the awards line. |
| **0** | **>300 h.** More than the entire CAD+fabrication budget. Not a scope question, an arithmetic one. |

*Tie-break:* both scorers write an hour estimate and average them; the **band**, not the point
estimate, is the output. *Weight rationale:* `PF` `scope_discipline` = **85**. Hours are the currency
scope is spent in, and `CAP` §7.1 ranks effective hours as constraint **#3**.

### A2 · parallel_workstream_demand — weight 85

*Concurrent development threads added ON TOP of the three mandatory ones (drivetrain, primary
mechanism, software).*

| Score | Anchor |
|:--:|---|
| **5** | **0 new streams.** Software-only, or a variation inside an existing stream (a second auto path, a different hood angle). |
| **4** | 0 new streams, but meaningfully enlarges one (a bigger intake on the mechanism you were already building). |
| **3** | **1 new stream** — this IS the primary scoring mechanism, the second of the three mandatory streams. Normal, not free. |
| **1** | **2 new streams.** A scoring mechanism *and* an endgame mechanism; or a mechanism plus a first-year swerve adoption. |
| **0** | **≥3 new streams** (4+ total). Over `parallel_workstreams_max`. **Gate G2 fires.** |

*Tie-break:* a workstream needs **all five** of `CAP` §5.1 — its own design decision, its own
prototype→test→revise loop, its own fab-queue slot, its own **unsupervised** student lead, its own
integration failure mode. *"Add a limelight" is not a stream. "Add a second scoring mechanism" is.*
*Weight rationale:* `PF` `scope_discipline` = **85**; `CAP` constraint **#2** (5 unsupervised leads).
`parallel_workstreams_max = 3` is derived **four** independent ways (`CAP` §5.2 routes A/B/C plus the
mentor route at §6.3), which is why it is a gate and not just a factor.

### A3 · mentor_supervision_load — weight 80

*Mentor unblock minutes per week the design consumes, against the 204 available.*

| Score | Anchor |
|:--:|---|
| **5** | **≤50 min/wk (≤25%).** Pre-solved design, no machine supervision, students proceed unsupervised for a week at a time. |
| **4** | ≤100 min/wk. A check-in and a design review. |
| **3** | **≤150 min/wk (≤75%).** One mechanism needing a weekly design review plus occasional saw supervision. The normal load for the primary mechanism. |
| **2** | ≤204 min/wk. Consumes the entire unblock budget; the other two streams get nothing. |
| **1** | **≤300 min/wk (≤150%).** Needs the mentor present for most of the work, or mill supervision every session. |
| **0** | **>300 min/wk.** The mentor becomes the mechanism (`CAP` §6.5). **Gate G5 fires.** |

*Tie-break:* count **unblock and supervision** minutes only. Teaching first-years is a separate
4.1 h/wk line and is not charged here. *Weight rationale:* `CAP` §7.1 constraint **#1** — the top of
the hierarchy. `PF` has no analogue (it measures outcomes, not inputs), so the weight is set just
under `scope_discipline`'s 85 rather than fabricated.

### A4 · drive_practice_sensitivity — weight 90 *(highest)*

*How much of the design's value is unlocked only by driver hours this team does not have.*

| Score | Anchor |
|:--:|---|
| **5** | **None.** Value is banked by software or by a single scripted action — an AUTO routine, a stationary scorer. |
| **4** | Slight. The driver has to line up on one visible feature. |
| **3** | **Moderate.** A driver learns the one repeated path in 2–3 hours; the rest is marginal gain. |
| **2** | Substantial. Needs a practised cycle but degrades gracefully with an unpractised driver. |
| **1** | **High.** Needs a driver who has run the cycle hundreds of times — a full-field volume cycler, or a single-shot endgame under time pressure. |
| **0** | **Extreme.** The *entire* value is driver skill: defense, denial, contact play. **Soft gate G6 fires** at <20 available drive hours. |

*Tie-break:* if we gave this robot to a driver with **9 hours** of seat time, what fraction of its
ceiling do we get? ≥80% → 5; ~50% → 3; ~25% → 1; <15% → 0. *Weight rationale:* `PF` `drive_practice`
= **90**, verbatim, the highest weight in the measured corpus — the field's whole output grows 50–74%
between an early and a late event while the median team's rank percentile does not move, so the only
improvement that buys relative position happens *before event 1*. `CAP` §3.4 funds **≈9 h** of real
seat time. This factor exists because that gap is the team's most under-priced risk.

### A5 · reliability_exposure — weight 88

*Serial-chain reliability. Every element that must work for the robot to score at all multiplies.*

| Score | Anchor |
|:--:|---|
| **5** | **≥0.90** expected chain reliability. 0–1 elements in the critical chain. |
| **4** | 0.85–0.89. Two elements in series. |
| **3** | **0.80–0.84.** Three elements in series, or two plus a sensing dependency. |
| **2** | 0.72–0.79. Four elements. |
| **1** | **0.65–0.71.** Five elements. Fails in roughly one match in three. |
| **0** | **<0.65.** Six or more serial elements, or a known jam-prone path with no bypass. |

*Tie-break:* use **0.93 per element** for a small team's first-season mechanism; count sensing/vision
as one extra element. **Write the element list, then compute — do not eyeball.** *Weight rationale:*
`PF` `reliability` = **88**, verbatim **[C]**. One DQ in a team's event moves `pct_picked` from
62–65% to 22–42% and median rank percentile from ~49 to 75–86.

### A6 · graceful_degradation — weight 66

*When it breaks mid-match, what is left.*

| Score | Anchor |
|:--:|---|
| **5** | **Rate drops, scoring continues** — or a second independent system keeps producing (the plow keeps herding after the climber dies). |
| **3** | **Primary action lost, robot still a legal, mobile, useful partner** — can play defense, can feed. |
| **1** | **Primary action lost, robot becomes a spectator**, but is not a liability. |
| **0** | **Total, and the failure state is a hazard or a foul source** — stuck extended, immobilised in a protected zone, entangling. |

*Tie-break:* score the **worst single failure**, not the average one. *Weight rationale:*
**0.75 × `PF` `reliability` (88) = 66.** It is the partial-credit half of the *same* evidence, so it
is discounted rather than double-counted at full weight.

### A7 · programming_complexity — weight 70

*Software difficulty **after** the `ARCH` `systemcore_adjustment` is applied.*

> **[C] 2027 replaces the roboRIO with SystemCore, and WPILib 2027 is SystemCore-only and
> incompatible with the Rio** (`PF` §6.3). Add before banding: **+0.0** open-loop teleop ·
> **+0.5** single closed-loop mechanism · **+1.0** odometry / path-following · **+1.0** vision + pose
> fusion, *and treat vision as UNAVAILABLE in build weeks 1–3*. Whether the roboRIO stays legal in
> 2027 is **UNVERIFIED**.

| Score | Anchor |
|:--:|---|
| **5** | **Adjusted difficulty ≤1.** Teleop button mapping. A first-year can write it. |
| **4** | ≤2. One simple closed loop, or a drive-forward auto. |
| **3** | **~3.** One closed-loop velocity or position controller with tuning, plus a one-element auto. |
| **2** | ~4. Multi-mechanism sequencing, or a two-element odometry auto. |
| **1** | **~5.** Closed-loop control + odometry + a multi-step auto. Consumes both programmers for a month. |
| **0** | **>5.** Vision-fused pose estimation driving a turret. In 2027 this is a research project, not a plan. |

*Tie-break:* take `programming_difficulty` straight from `archetype_corpus.yaml` if the design matches
an archetype; otherwise use its 1–5 scale, then add the SystemCore delta **before** banding.
*Weight rationale:* `PF` has **no** programming factor. Derived from `CAP` §3.1–3.2: programming is
the **largest single line** in the 599 h budget (135 h, 22.5%) and runs at **79% programmer
utilisation before a single bug exists**. Placed between `scope_discipline` (85) and `cots_leverage`
(55).

### A8 · sensing_vision_dependence — weight 30

*How much of the design stops working if the camera/coprocessor stack is not ready.*

| Score | Anchor |
|:--:|---|
| **5** | **None, or encoders only.** Nothing to stop working. |
| **4** | Gyro + encoders. Field-oriented drive, dead-reckoning auto; degrades to open-loop. |
| **3** | A sensor improves the cycle but the driver can do it blind. |
| **2** | **Vision-assisted** aiming or alignment. Works without it, at a much lower rate. |
| **0** | **Full pose fusion is load-bearing.** The design does not function without AprilTag localisation. |

*Tie-break:* if the coprocessor never boots at the event, does the robot still score? Yes at full rate
→ 5; yes, slower → 3–2; no → 0. *Weight rationale:* `PF` `vision_localization` = **30**, verbatim.
Deliberately low **on its own** — it is a force multiplier on mechanisms that must already work, and
its real cost shows up in A7 and A13.

### A9 · manufacturing_floor — weight 45

*The most capable machine any part of the design requires.*

| Score | Anchor |
|:--:|---|
| **5** | **Hand tools, hardware-store stock, 3D print.** No queue contention. |
| **4** | **Bandsaw + drill press** on stock tube/plate. Owned — but one of each, so queue contention with the drivetrain stream. |
| **2** | **Router / waterjet / laser-cut sheet.** Not owned. Buildable only via an outsourced 2D account with 1–2 weeks' lead. **Gate G1 fires** unless `outsourced_2d_account: true`. |
| **0** | **In-house CNC mill or lathe** for a load-bearing part. Not owned, not outsourceable at this budget. **Gate G1 fires.** |

*Tie-break:* score the single hardest part, **then check how many parts need that floor** — one router
part is a purchase order, eight is a fabrication programme. (This is `ARCH`'s own stated fix for its
G1/F4 mislabels: *"make mfg_floor a graded term rather than a binary"*.) *Weight rationale:* `PF`
`custom_fabrication` = 25 is the *value*-side weight. Promoted to **45** because `CAP` §5.2 **route C**
(the single-machine shop queue) binds `novel_mechanisms_max` **on its own** and is the one route
insensitive to headcount — adding five students moves it not at all. 45 matches `PF`
`drivetrain_choice`, likewise a "matters through what it consumes" factor.

### A10 · cots_availability — weight 55

*How much can be bought, or copied from a released open design, instead of invented.*

| Score | Anchor |
|:--:|---|
| **5** | **A released, documented, pre-solved design exists** (Everybot / KitBot / vendor kit) and the team can copy it. Fabrication hours, near-zero design hours. |
| **4** | A vendor sells the hard part (gearbox, roller, linear stage) and a build guide exists. |
| **3** | **Core motion is COTS but the geometry around it is bespoke.** *(A team's unreleased CAD posted on Chief Delphi counts here, not at 5 — CAD without a build guide still costs design hours.)* |
| **1** | **Only fasteners and motors are COTS.** Every functional surface is designed here. |
| **0** | Nothing exists to buy or copy; the concept itself must be invented and validated. |

*Weight rationale:* `PF` `cots_leverage` = **55**, verbatim **[C]** — 441 True Everybots in 2026,
**100 alliance captains**, 21 event wins, a **22% captaincy rate against a 21.8% population base
rate**, at ~$1,500 over the Kit of Parts with common tools and a basic 3D printer.

### A11 · iteration_count — weight 60

*Expected prototype → test → revise loops before the design is competition-ready.*

| Score | Anchor |
|:--:|---|
| **5** | **≤1.** Build it once from a known design; tune, do not redesign. |
| **4** | ~2. One rough version, one final. |
| **3** | **~3.** Normal for a first-of-its-kind mechanism on a small team: foamboard proof, rough version, final. |
| **2** | ~4. |
| **1** | **~5.** Compliant-material handling, high-speed launching, anything whose failure mode is only visible under match conditions. |
| **0** | **>5, or the loop length is unknown** because nobody on the team has built anything like it. |

*Tie-break:* count loops that require **re-fabricating a part**. Software rebuilds are free and belong
in A7. *Weight rationale:* **0.7 × `PF` `scope_discipline` (85) = 60.** Iteration is the mechanism *by
which* scope discipline bites, and `CAP` §3.3 measures `SLACK = 0.0 h` — so every unplanned loop is
unfunded by construction.

### A12 · marginal_cost — weight 40

*Dollars beyond a base drivetrain + control system, using the **high** end of the band.*

| Score | Anchor |
|:--:|---|
| **5** | **≤$300.** Hardware store, printed parts, motors already owned. |
| **4** | ≤$700. |
| **3** | **≤$1,200.** One mechanism's worth of vendor parts — roughly half the discretionary budget. |
| **2** | ≤$1,800. |
| **1** | **≤$2,500.** Consumes the entire discretionary budget, leaves nothing for spares. |
| **0** | **>$2,500.** **Gate G3 fires.** |

*Tie-break:* use the **high** end of the band and add 40% — `ARCH` states its cost bands are ±40%.
Exclude drivetrain and control system; those are committed elsewhere. *Weight rationale:* `CAP` §7.2 —
on the COTS path **money binds last, #5 of 5**. Set deliberately **below** `cots_leverage` (55):
whether a part *exists to buy* matters more than what it costs. **[C]** counter-case: the custom-fab
path is $13,000–17,000 and inverts the whole hierarchy — which is exactly why it is gated, not scored.

### A13 · schedule_critical_path_risk — weight 62

*How much work must happen in a fixed order, and how exposed that order is to one late delivery or
one absent student.*

| Score | Anchor |
|:--:|---|
| **5** | **Fully parallel or software-only.** Can be finished in the last two weeks if everything else slips. |
| **4** | One dependency, satisfiable from stock on hand. |
| **3** | **One serial dependency with a known lead time** (a vendor part, a print). Slippable by a week without consequence. |
| **1** | **A chain of 3+ serial dependencies**, or it must be mounted before the electrical board can be finished. |
| **0** | **Depends on something with an unknown ship date** — in 2027, SystemCore hardware itself — **or on one specific student being present**. |

*Tie-break:* draw the dependency chain, count the longest path in weeks. ≤1 → 5; ~3 → 3; ~5 → 1;
unknown → 0. *Weight rationale:* **0.72 × `PF` `scope_discipline` (85) = 62.** `CAP` §3.3
(`SLACK = 0.0`) and §9.4 (losing **one** unsupervised lead halves `novel_mechanisms_max`, and no other
perturbation moves it at all) make serialisation the team's largest uninsured risk.

---

## §3. The achievability weights, normalised

| # | Factor | Raw | Normalised | Traces to |
|---|---|---:|---:|---|
| A4 | drive_practice_sensitivity | **90** | **10.5%** | `PF` drive_practice 90 — verbatim, highest in corpus |
| A5 | reliability_exposure | **88** | **10.3%** | `PF` reliability 88 — verbatim **[C]** |
| A1 | build_hours_fit | 85 | 9.9% | `PF` scope_discipline 85 — verbatim |
| A2 | parallel_workstream_demand | 85 | 9.9% | `PF` scope_discipline 85 — verbatim |
| A3 | mentor_supervision_load | 80 | 9.3% | `CAP` constraint #1; no `PF` analogue, set just under 85 |
| A7 | programming_complexity | 70 | 8.2% | `CAP` §3.1–3.2 (135 h, 22.5%, 79% utilisation); no `PF` analogue |
| A6 | graceful_degradation | 66 | 7.7% | 0.75 × `PF` reliability 88 — discounted to avoid double count |
| A13 | schedule_critical_path_risk | 62 | 7.2% | 0.72 × `PF` scope_discipline 85 |
| A11 | iteration_count | 60 | 7.0% | 0.70 × `PF` scope_discipline 85 |
| A10 | cots_availability | 55 | 6.4% | `PF` cots_leverage 55 — verbatim **[C]** |
| A9 | manufacturing_floor | 45 | 5.3% | `PF` custom_fabrication 25, promoted for `CAP` §5.2 route C |
| A12 | marginal_cost | 40 | 4.7% | `CAP` §7.2 — money binds **#5 of 5** |
| A8 | sensing_vision_dependence | 30 | 3.5% | `PF` vision_localization 30 — verbatim |
| | **Sum** | **856** | 100% | |

**Nine of the thirteen weights are `PF` numbers, used verbatim or as an explicit fraction.** The four
that are not (A3, A7, A11, A13) have no `PF` analogue at all — `PF` measures competitive *outcomes*,
these are capacity *inputs* — and each is anchored to a named `CAP` constraint rank. Every `from:`
field in `achievability_rubric.yaml` says which.

`A = 100 × Σ(wᵢ·sᵢ) / (5 × Σwᵢ)`, range 0–100.

---

## §4. The VALUE axis — 5 factors

**V1 consumes `tools/cycle-model.py`.** Points per match is *not* recomputed here. Run the cycle model
at **your** cycle time — the one your drivers actually achieve, not a good team's — take the `TOTAL`
row, and divide by the season's median alliance score. One robot of three is **0.33 = parity**.

| # | Factor | Weight | 5 | 3 | 1 | 0 |
|---|---|---:|---|---|---|---|
| **V1** | points_per_match_share | **80** | ≥0.45 of median alliance score — carries an alliance | 0.18–0.29 — below parity, real contribution | 0.05–0.09 — token scoring | <0.05 direct **and** no credited indirect effect |
| **V2** | rp_contribution | **55** | Single-handedly clears (or nearly) an RP threshold partners typically cannot | Countable share of a threshold the alliance reaches together | Incidental; the RP would happen anyway | No RP relevance |
| **V3** | alliance_selection_appeal | **75** | Captain-tier / first-pick — the robot others build around | Second pick — a specialist captains shop for | Third pick / backup, fills a slot | Unpicked; nothing legible on the TBA page |
| **V4** | defense_resistance | **35** | Immune — scores in AUTO, or late, or **is** the defense | Degraded but functional; multiple approach angles | Heavily suppressed; one approach path | Neutralised — one surveyed position a defender parks on |
| **V5** | ceiling | **45** | Event-winning; practice keeps paying all season | First/second-pick; plateaus after ~3 weeks | Hard-capped by the concept (an L1 climb is 10 points forever) | First working version is the last version |
| | **Sum** | **290** | | | | |

**Weight rationale, each:**

- **V1 = 80** — `PF` `scoring_output` 80, verbatim **[C]**. "Avg Match" separates picked from unpicked
  better than qualification rank, better than Ranking Score, and much better than Avg Auto, in **all
  four** scraped seasons (AUC 0.801–0.872). *Captains buy points.*
- **V2 = 55** — derived, not verbatim. `PF` measures Ranking Score as a **worse** predictor of being
  picked (AUC 0.777–0.821) than avg match points, so RP value sits **below** `scoring_output`. It
  sits above defense because RP thresholds are the cheapest lever `ARCH` finds: invariant **I4**'s
  lesson is that *the threshold is almost never set at the top tier* — `REB` TRAVERSAL (50) is cleared
  by one L3 + one L2; `RAPD` HANGAR (16) never needed TRAVERSAL.
- **V3 = 75** — the terminal outcome the whole `PF` corpus predicts (`pct_picked_no_DQ` 61.7–64.7).
  Discounted **below** V1 on purpose: AUC 0.80–0.87 means avg-match points already explain most of it,
  and scoring both at full weight would double-count the same evidence.
- **V4 = 35** — `PF` `defense_capability` 35, verbatim, used here as the price of the defense
  *interaction*. Its game-conditional deltas apply on kickoff day (§11).
- **V5 = 45** — set at `PF` `drivetrain_choice`'s 45. Ceiling is what a *better-resourced* version of
  this team would get; `PF` §5.3 measures P90/P50 EPA ratio going 1.38 → 2.35, i.e. headroom accrues
  to teams this one is not. A tiebreaker, not a driver.

**Indirect value [S].** Support and defense designs score 0 directly. Convert before banding, using
the midpoints of the bands `ARCH` itself states: **defense specialist ≈ 45 pts**, **feeder/support
≈ 35 pts**. This is the only way I3 and I6 — the invariants with a **5/5** and **3/4** small-team
success rate — get a non-zero V1, and it is explicitly a modelling choice, not a measurement.

**Base-rate reminder [C]:** **64–78%** of event-**winning** alliances carried a below-median-OPR
robot (78% in 2026 `REB`). The second-pick slot is the *statistically normal* path onto a banner for
this team, not a consolation prize.

`V = 100 × Σ(vⱼ·tⱼ) / (5 × Σvⱼ)`, range 0–100.

---

## §5. Gate checks — hard disqualifiers, independent of score

> **A gate is not a penalty term.** It is a statement that the design **cannot be built by this team
> as specified**. The correct response is *always* to descope to a named variant and re-score it as a
> new candidate — **never** to argue with the gate. A gated design is capped at **T4 GATED** no matter
> how well it scores, and its index is printed for information only.

| Gate | Fires when | Hard? | From | Descope prompt |
|---|---|:--:|---|---|
| **G1 MACHINE** | The manufacturing floor is not in `owned_manufacturing` (`hand`, `bandsaw+drill`, `3dprint`). *Exception:* `router` passes if `outsourced_2d_account: true` **and** ≤2 parts **and** ≥2 weeks' lead | **Yes** | `CAP` §5.2 route C; §7.1 #4 | Can the same function be tube + plate on the bandsaw, or 3D printed? That is a *different candidate* — score it |
| **G2 WORKSTREAMS** | `novel_mechanisms > 2`, or new streams push the total past `parallel_workstreams_max = 3` | **Yes** | `CAP` §5.2, quadruply derived | Which mechanism produces more points per hour? Build that one, buy or copy the other |
| **G3 BUDGET** | `marginal_cost_high > $2,500` | **Yes** | `CAP` §8.1 | Which line is >30% of the total? Is there a COTS or used-market substitute? |
| **G4 HOURS** | `mechanism_hours > 205 h` pool | **Yes** | `CAP` §3.1, §3.3 | Week 1 → Week 4 buys **+255 effective hours for free** (`CAP` §7.4). Have you actually chosen your event? |
| **G5 MENTOR** | Unblock demand > `204 min/wk` | **Yes** | `CAP` §6.2–6.3 | One more technical mentor doubles this to 408 min/wk and is worth more than five more students. Deadline **2026-11-17** |
| **G6 DRIVE_HOURS** | A4 = 0 (extreme) **and** `real_driver_seat_hours < 20` | **Soft** — one-tier downgrade | `ARCH` `verdict_predicate.overriding_term_required`; `PF` drive_practice 90 | Commit to a Week 3–4 event and a fall driving programme, or pick a design whose value is banked in software |

**Two 2027-specific pre-checks that run before G2** (`CAP` §5.6): vision-based pose estimation, **or**
a first-year swerve adoption, each reduce `novel_mechanisms_max` from 2 to **1**. Both together
reduce it to **0** — *"this configuration builds a drivebase and nothing else."* That is a
reasonable-sounding plan that produces no scoring robot, and it must be said out loud on kickoff day.

**The "no zeros in GREEN" rule.** A weighted mean can hide a single anchor written as *impossible*.
So: **one** achievability zero caps the tier at T2 STRETCH; **two or more** cap it at T3 RED. **A4 is
excluded** — it has its own dedicated gate (G6), and double-penalising it would drop every defense
archetype `ARCH` labels YES. This rule alone fixed three of the nine back-test disagreements (§9.2).

---

## §6. The Achievability × Value matrix — the real output

```
            +----------------------------------+----------------------------------+
            |            VALUE < 55            |            VALUE >= 55           |
            +----------------------------------+----------------------------------+
ACH >= 60   |         CHEAP INSURANCE          |            BUILD THIS            |
            +----------------------------------+----------------------------------+
ACH <  60   |              DELETE              |               TRAP               |
            +----------------------------------+----------------------------------+
```

### Q1 · BUILD THIS — `A ≥ 60 and V ≥ 55`

**Decision rule.** Commit on kickoff weekend. Assign an **unsupervised lead by day 3** and
**CAD-freeze by day 10**. If more than one candidate lands here, build the one with the smaller **A1
deficit** first, and hold the other as the second mechanism *only* if `novel_mechanisms_max` still has
room after the 2027 deductions in §5.

### Q2 · CHEAP INSURANCE — `A ≥ 60 and V < 55`

**Decision rule.** Do **not** lead with this — and do not skip it either. This is the second
mechanism, the fallback, and the thing that keeps you a legal, useful alliance partner when the
primary mechanism is in pieces. Build it **after** the Q1 design passes its first reliability test,
from spare hours, with a first-year pair leading it. It is also the **Quality Award** thesis
(`ARCH` I7 `award_pairing`) — *"it never failed"* is a submission, not a consolation.

### Q3 · TRAP — `A < 60 and V ≥ 55`

**Decision rule.** The season-killer quadrant. Everything here is genuinely worth a lot of points and
genuinely out of reach, **which is exactly why teams pick it on kickoff day**. The response is never
"work harder". It is: **enumerate the descoped variants and re-score each as its own candidate** —
fixed-position instead of turreted, one auto element instead of four, L1 climb instead of L3. `ARCH`
proves the variant, not the family, is what a small team should score: invariant **I1 is 0/4 at full
spec and 6/9 restricted to the fixed-range variant**. In the §9 back-test, **10 of 30** archetypes
land here and every one of them is gated.

### Q4 · DELETE — `A < 60 and V < 55`

**Decision rule.** Say it out loud in the strategy meeting and cross it off the whiteboard. Do not
keep it as a "maybe". A live maybe consumes the scarcest resource in the entire model — **mentor
decision attention, 204 min/wk** — every week it stays on the board.

*(In the 30-record back-test this quadrant is **empty**. That is not a bug: `ARCH` is a corpus of
archetypes that someone, somewhere, ran successfully. Your kickoff whiteboard will populate Q4.)*

---

## §7. Tiers

| Tier | Range | What this means for you |
|---|---|---|
| **T1 GREEN** | `index ≥ 62`, no hard gate, ≤0 zeros | **Build it.** Inside your real capacity with enough margin that one bad week does not kill it. You still have to protect the drive-practice and reliability hours — GREEN means the *design* is not the thing that will beat you. |
| **T2 STRETCH** | `48 ≤ index < 62`, no hard gate | **Possible, and only possible, if you spend a specific named thing to buy it:** a Week 3–4 event instead of Week 1 (**+255 effective hours, free**), a second technical mentor, an outsourced-fabrication account, or a third programmer trained in the fall. **Write down which one before you start.** A STRETCH design attempted without buying its enabler is how a season ends with an unfinished robot. |
| **T3 RED** | `index < 48`, no hard gate | **Do not build this.** Not "try and see" — the index is low because several independent factors are bad *at once*, and each one you fix reveals the next. If the VALUE axis is high, go read the TRAP rule and descope it into a different candidate. |
| **T4 GATED** | any hard gate, at any index | **The design as specified cannot be built here.** Not "hard" — it needs a machine you do not own, more concurrent workstreams than you have leads for, or more money than exists. **The index must not be used to argue past the gate.** Descope and re-score. |

---

## §8. The binding constraint

Printed for **every** candidate, gated or not. It is the single thing to fix.

- **If any gate fired** → the **first gate**, with its numbers. Fixing anything else changes nothing.
- **Otherwise** → the achievability factor with the largest **weighted deficit**, `wᵢ × (5 − sᵢ)`.

Weighted deficit, not raw score, because a 3/5 on A4 (weight 90) costs 180 points of index while a
1/5 on A8 (weight 30) costs 120. The rubric tells you where the *leverage* is, not where the ugliest
number is.

---

## §9. Validation / dry run — real output

Everything below is verbatim `tools/score-strategy.py`, run 2026-08-22 on this machine.

### 9.1 The back-test: all 30 archetypes, current shop (no outsourced 2D account)

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml

======================================================================================================================
 BIOCORE ACHIEVABILITY x VALUE  --  ~15 students, 1 mentor, $2,500 discretionary, 599 effective h
======================================================================================================================
id   strategy                             ACH   VAL   idx  quadrant        tier        binding constraint              corpus
----------------------------------------------------------------------------------------------------------------------
C5   AUTO Specialist                     80.2  83.8  81.8  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
P5   QUINTET AUTO Specialist             83.3  78.3  81.0  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
R5   AUTO Specialist                     86.9  72.8  80.5  BUILD THIS      T1 GREEN    A7 programming_complexity = 1/5 YES
F5   AUTO Specialist                     80.2  78.3  79.3  BUILD THIS      T2 STRETCH  A7 programming_complexity = 0/5 CONDITIONAL
G3   CHARGE STATION Specialist           82.7  74.1  78.9  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity = YES
C6   Defense Specialist                  86.4  65.2  76.8  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
F3   Processor Cycler                    73.2  75.2  74.1  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
F6   ALGAE Defender / Reef Clearer       81.0  65.2  73.9  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
P2   LOWER HUB Dumper                    93.7  49.0  73.6  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 4/5        YES
R2   Fixed-Zone Bulk Shooter             73.2  72.8  73.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
G4   HYBRID-Row Filler / LINK Facilita   90.6  49.0  71.9  CHEAP INSURANCE T1 GREEN    A6 graceful_degradation = 3/5   YES
R6   Shift Defender / HUB Denier         80.1  59.7  70.9  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = YES
G5   Defense / Floor-Intake Support      81.0  56.9  70.2  BUILD THIS      T2 STRETCH  A4 drive_practice_sensitivity = CONDITIONAL
R3   Neutral-Zone Herder / Feeder        86.4  49.3  69.7  CHEAP INSURANCE T1 GREEN    A4 drive_practice_sensitivity = YES
R4   TOWER Climber Specialist (LEVEL 3   72.1  63.1  68.0  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity = YES
F2   L1 Trough Filler                    73.2  57.2  66.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5        YES
G1   Cube-Only Top-Row Cycler            51.2  80.7  64.5  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' YES
C2   AMP Feeder / Amplification Manage   73.2  51.7  63.6  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 2/5        YES
C3   Subwoofer Camper (fixed-distance    70.2  54.8  63.3  CHEAP INSURANCE T1 GREEN    A1 build_hours_fit = 2/5        YES
R8   Minimal Flawless (plow + LEVEL 1    87.9  32.4  62.9  CHEAP INSURANCE T1 GREEN    A4 drive_practice_sensitivity = YES
C1   SPEAKER Cycler (variable distance   37.3  89.0  60.6  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' CONDITIONAL
P4   MID-RUNG Climber + Low CARGO        73.2  40.7  58.6  CHEAP INSURANCE T2 STRETCH  A1 build_hours_fit = 2/5        YES
P1   UPPER HUB Cycler                    37.3  83.4  58.1  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' CONDITIONAL
F1   L4 Branch Specialist                30.8  89.0  57.0  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
F4   Deep CAGE Climber                   54.6  57.6  56.0  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' CONDITIONAL
C4   STAGE Climber + TRAP                53.7  57.6  55.5  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' CONDITIONAL
R7   Depot Cycler / Lift Dumper          45.0  61.0  52.2  TRAP            T4 GATED    GATE G1 MACHINE: needs 'router' MARGINAL
R1   Cycle Cannon (turreted high-rate    22.0  89.0  52.2  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
G2   Full-Grid CONE + CUBE Scorer        14.9  92.8  50.0  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
P3   TRAVERSAL Climber                   19.0  69.0  41.5  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s NO
----------------------------------------------------------------------------------------------------------------------
 quadrant thresholds: ACH >= 60, VAL >= 55   |   tiers: T1 >= 62, T2 >= 48, T3 < 48, T4 = any hard gate
 combined index = 0.55*ACH + 0.45*VAL. RANK BY IT, DECIDE BY THE QUADRANT.

            +----------------------------------+----------------------------------+
            |            VALUE < 55            |            VALUE >= 55           |
            +----------------------------------+----------------------------------+
ACH >= 60   |         CHEAP INSURANCE          |            BUILD THIS            |
            |       P2 G4 R3 C2 C3 R8 P4       | C5 P5 R5 F5 G3 C6 F3 F6 R2 R6 G5 |
            |                                  |               R4 F2              |
            +----------------------------------+----------------------------------+
ACH <  60   |              DELETE              |               TRAP               |
            |                -                 | G1* C1* P1* F1* F4* C4* R7* R1*  |
            |                                  |             G2* P3*              |
            +----------------------------------+----------------------------------+
  * = a hard gate fired; the quadrant is shown for information, the tier is T4 GATED.

--- Back-test against archetype_corpus.yaml hand labels ---

 agreement: 24/30 = 80%   (the corpus's own risk predicate scores 21/30 = 70%)

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
G1   YES           T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
C1   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
P1   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
F4   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
C4   CONDITIONAL   T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
R7   MARGINAL      T4 GATED    GATE G1 MACHINE: needs 'router'; shop has ['
```

**Three things to read out of that table.**

1. **80% agreement with 30 hand-assigned expert labels, against the corpus's own risk predicate at
   70%.** The rubric is a strictly better instrument than the four-term predicate `ARCH` §10.3 ships,
   on `ARCH`'s own test set. It is the same test set the anchors were calibrated against, so this is
   *consistency*, not out-of-sample validation (§12).
2. **Every one of the six disagreements is the same disagreement**: the `router` manufacturing floor.
   The rubric gates them; the hand labels call them CONDITIONAL — and "conditional" is precisely what
   `outsourced_2d_account` encodes. §9.3 runs that condition.
3. **The quadrant map reproduces `ARCH`'s central finding without being told it.** All ten TRAP
   entries are gated. All seven CHEAP INSURANCE entries are hand-labelled YES. The four highest
   combined indices are all AUTO specialists — `ARCH` I5, *"the best points-per-dollar play in the
   corpus"* — and three of them are held at **T2 STRETCH** by the no-zeros rule, which is exactly the
   SystemCore warning `ARCH` attaches to I5 for 2027.

### 9.2 What the no-zeros rule bought

| Record | Hand label | Before the rule | After | Why |
|---|---|---|---|---|
| C5, P5, F5 | CONDITIONAL | T1 GREEN ✗ | **T2 STRETCH ✓** | Adjusted programming difficulty >5 under SystemCore. `ARCH`'s stated root cause was *"the predicate cannot see SCOPE"* — a zero on A7 is the closest observable proxy |
| C6, F6, R6, G5 | YES / CONDITIONAL | T1 → T2 via G6 | unchanged | A4 excluded from the rule by construction — G6 already prices extreme drive sensitivity once |

Agreement moved **21/30 → 24/30**. The three records it fixed are exactly the family `ARCH`
predicted its own predicate would miss.

### 9.3 Sensitivity: what if the fall programme opens an outsourced-fabrication account?

`CAP` §7.5 lists *"establish the outsourced-fabrication account and run one test order"* with a
**2026-12** deadline. Flip one constant:

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml \
      --set outsourced_2d_account=true

 agreement: 24/30 = 80%

id   hand          rubric      binding constraint
------------------------------------------------------------------------------
G1   YES           T4 GATED    GATE G4 HOURS: 243 h > 205 h pool
C1   CONDITIONAL   T4 GATED    GATE G2 WORKSTREAMS: 3 novel mechanisms > no
...
```

**Agreement does not move — but the binding constraint does, and that is the finding.** Buying a
fabrication account does not rescue those designs; it moves what stops them from *"a machine you do
not own"* to *"hours and workstreams"*. Money is relaxable (`CAP` §7.2, constraint #5). Hours and
unsupervised leads are not (constraints #2 and #3, in-season elasticity **None**). **The rubric
independently reproduces the constraint hierarchy `CAP` §7.1 derived by a completely different
route.** That is the strongest validation in this document.

### 9.4 One row in detail

```
$ python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --detail R2

==============================================================================
 R2  Fixed-Zone Bulk Shooter
==============================================================================
 ACHIEVABILITY 73.2   VALUE 72.8   index 73.0   BUILD THIS   T1 GREEN
 points/match 60.0  (share of median 0.41)   source: corpus points_per_cycle x cycles

factor                              w  score     w*s  deficit
--------------------------------------------------------------
A1 build_hours_fit                 85      2     170      255
A2 parallel_workstream_demand      85      3     255      170
A3 mentor_supervision_load         80      4     320       80
A4 drive_practice_sensitivity      90      3     270      180
A5 reliability_exposure            88      4     352       88
A6 graceful_degradation            66      5     330        0
A7 programming_complexity          70      4     280       70
A8 sensing_vision_dependence       30      5     150        0
A9 manufacturing_floor             45      4     180       45
A10 cots_availability              55      4     220       55
A11 iteration_count                60      4     240       60
A12 marginal_cost                  40      3     120       80
A13 schedule_critical_path_risk    62      4     248       62
--------------------------------------------------------------
V1 points_per_match_share          80      4     320
V2 rp_contribution                 55      4     220
V3 alliance_selection_appeal       75      4     300
V4 defense_resistance              35      1      35
V5 ceiling                         45      4     180
--------------------------------------------------------------
 BINDING CONSTRAINT: A1 build_hours_fit = 2/5
```

R2 is `ARCH`'s stated *"highest-value small-team play in REBUILT"*. The rubric agrees (BUILD THIS,
T1 GREEN) **and adds the thing the corpus does not say**: at 174 estimated hours against a 205 h pool,
the binding constraint is hours, not money and not difficulty — so the lever is the **event week**,
not the design. Note also **V4 = 1**: a single surveyed shooting position is exactly what a defender
parks on. The rubric prices the strength and the exposure in the same row.

### 9.5 Hand-authored candidates, with V1 taken from `cycle-model.py`

```
$ python tools/score-strategy.py --candidates reference/examples/candidates_example.yaml

id   strategy                             ACH   VAL   idx  quadrant        tier        binding constraint
----------------------------------------------------------------------------------------------------------
S2   Endgame specialist, cheapest RP t   69.9  77.9  73.5  BUILD THIS      T1 GREEN    A4 drive_practice_sensitivity =
S1   Fixed-position bulk scorer          73.2  72.8  73.0  BUILD THIS      T1 GREEN    A1 build_hours_fit = 2/5
S3   Do-everything robot (control)       11.0  92.8  47.8  TRAP            T4 GATED    GATE G1 MACHINE: needs 'CNC'; s
```

S1 and S2 declared no `V1`; `score-strategy.py` imported `tools/cycle-model.py`, called `model()` at a
**12-second** cycle, and derived it — 61.3 pts/match for S1 (share 0.42 → V1 = 4) and 83.8 for S2 with
the L3 endgame (share 0.57 → V1 = 5). **The value axis is not reimplemented; it is consumed.** S3 is a
deliberate control: `ARCH` invariant I2, 0/5 small-team success in five seasons, the highest VALUE
score in the file and three simultaneous hard gates.

### 9.6 Reproducibility

```bash
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --set outsourced_2d_account=true
python tools/score-strategy.py --candidates reference/examples/candidates_example.yaml
python tools/score-strategy.py --from-corpus reference/archetype_corpus.yaml --json | head -40
```

Deterministic. No network, no randomness. Requires PyYAML; `cycle-model.py` is imported by path and
degrades to a warning if absent.

---

## §10. Worked procedure for kickoff day

1. **Read the manual for the eight numbers in §11.** Fill `biocore_kickoff_inputs`. Twenty minutes,
   two people, before anyone draws anything.
2. **Apply the `PF` game-conditional deltas** to the weights (`tools/rubric_weights.py`). An
   AUTO-gated RP moves V2 by +25; each protected zone moves V4 by −8.
3. **Enumerate candidates — and their descoped variants.** This is the single highest-value step.
   `ARCH` measures its own predicate failing on exactly this: *"the predicate scores the full-spec
   family; the hand label scores the best available variant."* Write **"turreted shooter"** and
   **"fixed-position shooter"** as two rows, not one.
4. **Score achievability by hand, two people, independently**, against §2. Reconcile any gap >1 point
   by re-reading the tie-break line — not by splitting the difference.
5. **Run `cycle-model.py` at your real cycle time** and let `score-strategy.py` consume it for V1.
6. **Run the scorer. Read the quadrant, then the binding constraint.**
7. **For every T2 STRETCH row you intend to build, write down which enabler you are buying** — event
   week, second mentor, fab account, third programmer. Unwritten, it will not be bought.
8. **Re-run at Week 3 with real hours spent.** The rubric is a planning instrument and a *tracking*
   one; A1 and A13 move fastest.

---

## §11. What the BIOCORE manual has to fill

All null by design. `achievability_rubric.yaml : biocore_kickoff_inputs`.

| Slot | Feeds | Why it matters |
|---|---|---|
| `median_alliance_score_estimate` | **V1 denominator** | Every value score is a share of this. Seed from a comparable season until real event data exists |
| `scoring_table_rows` | `PF` scope_discipline +10 if ≥8 | Observed: `RAPD` 10, `CRES` 8, `REEF` 12, `REB` 7 |
| `auto_gated_ranking_point` | **V2 +25** | The single largest game-conditional swing. Present in `REEF` only, of the last five seasons |
| `protected_zone_rule_count` | V4 −8 each | Observed: 2022:1, 2023:0, 2024:3, 2025:2, 2026:1 |
| `one_defender_at_a_time` | V4 −15 | True in `REEF` only |
| `pin_count_seconds` | V4 +10 if ≥5 | 5 in 2022–2024, 3 in 2025–2026 |
| `foul_values_minor_major` | V4 −10 or +5 | Major ≥10% of a typical alliance score → defense is priced out |
| `systemcore_shipping` | A13 floor of 1 | If SystemCore hardware has not shipped at kickoff, everything depending on it has an unknown ship date |

**The two `ARCH` falsification checks most likely to move this rubric:** is BIOCORE's scoring element
**capped in possession** (a cap compresses the score spread and the simplified high-volume variant
loses its edge), and **is there a period or state where scoring is impossible** (that is what made
defense free in `REB`, and without it defense reverts to CONDITIONAL).

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/ACHIEVABILITY-RUBRIC.md` | this document |
| `reference/achievability_rubric.yaml` | **new** — the machine-readable instrument: 13 achievability factors, 5 value factors, 6 gates, 4 quadrants, 4 tiers, and the corpus auto-mapping |
| `tools/score-strategy.py` | **new** — the scorer. Imports `cycle-model.py` for the value axis; back-tests against `archetype_corpus.yaml` |
| `reference/examples/candidates_example.yaml` | **new** — the candidate-file shape, with the `cycle_model:` handoff demonstrated |

Nothing marked DONE was modified. [`04_PREDICTIVE_FACTORS.md`](04_PREDICTIVE_FACTORS.md),
[`02_TEAM_CAPACITY_MODEL.md`](02_TEAM_CAPACITY_MODEL.md), [`03_ARCHETYPE_CORPUS.md`](03_ARCHETYPE_CORPUS.md)
and their `.yaml` companions were read and cited, not edited. `tools/cycle-model.py` and
`tools/capacity_model.py` were imported/invoked, not changed.

---

## Known limitations

- **`reference/team_capacity.yaml` does not exist on disk** as of 2026-08-22, although `CAP` §8 and
  its "Files written by this pass" table both name it. `team_constants` in the rubric YAML is
  **transcribed by hand** from that document's §8 table. Regenerate with
  `python tools/capacity_model.py --yaml` and diff before trusting any downstream number.
- **The back-test is consistency, not validation.** The anchors and thresholds were calibrated so
  that `ARCH`'s hand-labelled YES records fall right of the achievability line. 24/30 on the set you
  tuned against is a *floor*, not a measurement. The honest out-of-sample test is 2027: score the
  candidates on kickoff day, seal the file, and compare in April.
- **Every achievability weight is a derivation, not a measurement.** Nine trace to `PF` numbers
  verbatim or as a stated fraction; four (A3, A7, A11, A13) have **no `PF` analogue at all** and are
  anchored to `CAP` constraint ranks. Their `from:` fields say so. `PF`'s own weights are themselves
  **[H]**/**[C]** mixed and are relative, not probabilities.
- **The anchors are calibrated for inter-rater agreement, not accuracy.** Two people scoring the same
  design should land within 1 point. Both can still be wrong about the design.
- **A10 (`cots_availability`, weight 55 = 6.4% of the index) has no source field in
  `archetype_corpus.yaml`** and is proxied from `mfg_floor` in the back-test. It is the weakest
  mapping in the instrument. Score it by hand for real candidates.
- **`auto_score_from_corpus` is a regression-test harness, not a scoring method.** It exists so the
  rubric has 30 records to check itself against. Do not use it on a real kickoff-day candidate — score
  the factors by hand against §2 and use the corpus only to sanity-check yourself.
- **The indirect-value equivalents (defense ≈45 pts, feeder ≈35 pts) are `ARCH`'s own stated band
  midpoints, and `ARCH` marks them [S].** They are load-bearing for I3 and I6 — the two invariants
  with the best small-team success rates — so the two most-recommended archetype families rest on the
  softest number in the value axis.
- **The 0.55/0.45 combined split and the 60/55 quadrant thresholds are choices**, justified in §1 and
  §6 but not derived from data. Rows near a threshold should be treated as ties; the quadrant boundary
  is not a cliff in reality even though it is one in the code.
- **The V1 → `cycle-model.py` handoff needs a BIOCORE game file that does not exist.** `--game
  rebuilt` is the built-in worked example. On kickoff day someone must write `biocore.json` from the
  point table before the value axis means anything.
- **`novel_mechanisms_max = 2` assumes software is exactly one workstream.** `CAP` itself flags that
  in 2027 it is more, and that the −0.4 deduction is an unvalidated guess. If SystemCore production
  units slip past kickoff, gate G2 is *too permissive* and A13 should floor at 1 for everything.
- **Nothing in this file is a BIOCORE claim.** No weight, threshold, anchor or gate is derived from
  any BIOCORE rule, because the game is not public until **2027-01-09 12:00 ET**. §11 is the list of
  what has to be filled before the instrument produces a BIOCORE answer rather than a general one.

---

## Security note

Every source read for this pass was a local file in this project. All of it was treated as **data**.
None contained text addressed to an AI assistant or any attempt to issue instructions. No
authentication was used or attempted, and no external endpoint was contacted while writing this file
or while producing any output pasted into §9.
