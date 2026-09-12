# AI for design and CAD — what actually works, what is marketing, and four calculators that run

**Purpose:** you are going to be pitched AI-for-CAD constantly between now and kickoff. Almost all
of it is useless for a 15-student FRC team, and a small, specific slice of it is genuinely
transformative. This file separates the two, states plainly what text-to-CAD *cannot* do for a
competitive robot, and then builds the thing that is actually worth having — **four working
engineering calculators**, written and run by this pass, that replace the half-remembered
spreadsheet every small team re-derives every January.

The framing that matters: **[C]** *FIRST* views AI "as tools available to students in the same way
that CAD programs, Programming Languages, and 3D printers are tools available for their use"
([`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md)). That is exactly the right
altitude. A 3D printer does not design your robot either.

**Companion files written by this pass:**
[`calculators/motors.py`](calculators/motors.py) ·
[`calculators/drivetrain.py`](calculators/drivetrain.py) ·
[`calculators/elevator_arm.py`](calculators/elevator_arm.py) ·
[`calculators/fourbar.py`](calculators/fourbar.py) ·
[`calculators/cg_tip.py`](calculators/cg_tip.py) ·
[`templates/design-prompts.md`](templates/design-prompts.md)

**Upstream files this builds on — cited, not duplicated:**
[`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) (the AI policy authority) ·
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) (**the hours/budget authority — every
hours claim here is denominated in it**) · [`../bom/`](../bom/) (the cost/parts authority) ·
[`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md) (Systemcore/WPILib 2027) ·
[`../../tools/cycle-model.py`](../../tools/cycle-model.py) (**cycle time and shooter/EV maths already
exist — this file does not duplicate them**) ·
[`../ACHIEVABILITY-RUBRIC.md`](../ACHIEVABILITY-RUBRIC.md) ·
[`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md).

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Executed, produced, or verified by this pass; or quoted from a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed practice across FRC seasons or standard engineering practice; not a rule and not measured here |
| **[S]** SPECULATION | Inference or planning judgement. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Not checked by this pass. **Check it before you spend money on it** |

> **BIOCORE scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game; kickoff
> **2027-01-09 12:00 ET**. Nothing here draws on FTC BIOBUZZ. This file contains **no
> game-specific claim** — it cannot, because the manual does not exist. Frame/weight figures used
> in the calculators are **2026 REBUILT** baselines **[H]** and are labelled as such at every
> appearance.
>
> **Control-system guard.** 2027 replaces the roboRIO with **Systemcore**. The one place this
> touches *design* is the brownout threshold in `motors.py`: the roboRIO 1 value is 6.8 V, the
> roboRIO 2 value is 6.3 V, and the **Systemcore threshold is UNVERIFIED** as of 2026-08-22.
> Re-check after the **2026-11-12 Pre-Kickoff Virtual Kit Release**.

> **Vendor-claim guard, stated once and meant throughout §1.** The licensing and pricing facts in
> §1 were **fetched and verified on 2026-08-22** — the verification log with URLs is **§1.0**. Facts
> carried from those sources are labelled **[C]**; anything still unfetched keeps **UNVERIFIED** and
> a re-check instruction. The distinction matters because the whole point of this file is that you
> should not make a budget decision on a confident-sounding description of a tool nobody opened.
> The §1 *verdicts* are judgements about a **category** and hold even if a specific product moves;
> the *prices* must be re-checked before a purchase order, because pricing in this space moved
> materially in the twelve months before this pass.

---

## 0. The 60-second workflow

Every number in §3 is this script output. Run it before you argue with any of it.

```bash
# Run from the repository root.
cd reference/ai-integration/calculators

# ---- 0. the shared motor table + the battery/bus model everything else uses (instant) --------
python motors.py

# ---- 1. DRIVETRAIN: the only table you actually need on kickoff day -------------------------
#         Read the "verdict" column. Take the FASTEST ratio still marked traction-limited,
#         then step one slower. Everything else in the drivetrain argument is noise.
python drivetrain.py --sweep
python drivetrain.py --motor kraken_x60 --ratio 6.12 --weight 125 --limit 60

# ---- 2. GRAVITY LOADS: elevator and arm, including the two lines teams forget ---------------
#         "HOLDING CURRENT" decides whether you need a ratchet. "RATCHET must hold" is the
#         number you give the person picking the pawl.
python elevator_arm.py elevator --mass 18 --travel 48 --stages 2 --ratio 12 --pulley 1.75
python elevator_arm.py arm --mass 12 --length 22 --ratio 100 --motor neo
python elevator_arm.py arm --gas-spring          # how much ratio a counterbalance buys back

# ---- 3. LINKAGES: does it bind, and does it leave the frame perimeter? ----------------------
python fourbar.py analyze                        # transmission angle + coupler path + torque
python fourbar.py parallel --dx 14 --dy 20 --link 24
python fourbar.py synth2 --p1 4,6 --p2 22,26 --pivot 0,2

# ---- 4. CG + TIP-OVER, stowed AND extended. The extended case is the one that surprises. ----
python cg_tip.py

# ---- 5. CYCLE TIME AND EXPECTED VALUE ARE ALREADY SOLVED. Do not re-derive them, do not ask
#         a chatbot. Run the model that exists in this project. ------------------------------
cd ../../..                                      # back to the repository root
python tools/cycle-model.py --game rebuilt --sweep
```

**Read it in this order:** `drivetrain.py --sweep` first (it is the decision), then `cg_tip.py`
(it is the constraint nobody checks), then the mechanism-specific tool. If `cg_tip.py` says the
robot tips before it slides when extended, stop designing and fix that first — no driver and no
control loop recovers a tipped robot.

---

## 1. The CAD-adjacent AI landscape, August 2026 — capability vs marketing

### 1.1 The summary table

Read the **Verdict** column. Read the **Verified?** column before you read anything else.

| Tool / category | What it claims | What it actually does **[S]** unless noted | Cost | Verified? | **Verdict for a 15-student team** |
|---|---|---|---|---|---|
| **CADQuery / build123d + LLM** | Python-scripted parametric CAD | **Genuinely works.** LLM writes Python; you *run* it; it either produces a solid or throws. Exports STEP/DXF into Onshape or Fusion | **$0.** Both open source, on the OpenCASCADE kernel | **[C]** fetched 2026-08-22 | **USE IT.** The one place LLMs materially help CAD. §1.2 |
| **Onshape** (the CAD itself) | Cloud parametric CAD, free education tier | The FRC standard. Real-time multi-user, versioning, part libraries, FeatureScript, browser-only (works on school Chromebooks) | **$0.** Educator Plan is free for FRC/FTC teams, incl. Simulation and **CAM Studio** | **[C]** fetched 2026-08-22 | **USE IT** — for the CAD, not for the AI. §1.3 |
| **Onshape AI Advisor** | AI assistance inside Onshape | Real product, shipped. In-canvas conversational guidance: step-by-step recommendations, troubleshooting, best-practice tips. Powered by Amazon Bedrock. It advises *you*; it does not model *for* you | Bundled into the plan you already have — no separate line item | **[C]** fetched 2026-08-22 | **Use it free, budget $0.** A help system, not a design capability. §1.3 |
| **FeatureScript generation via LLM** | Custom Onshape features from a prompt | Partially works. FeatureScript is a small, weakly-documented language, so hallucinated std-library calls are common. Compile-fail rate is materially worse than Python | Free (FeatureScript is free) | **[H]** | **Marginal.** Only if a student already knows Onshape well. §1.4 |
| **Fusion generative design** | AI generates optimal geometry from loads | Real technology, real maths (topology optimisation). Produces organic shapes that need 5-axis machining or metal additive | **$0 for you.** Education plan = free licence + **unlimited cloud credits**. (Commercial: 33 credits ≈ $33/study, or a $1,600/yr extension) | **[C]** fetched 2026-08-22 | **NO — but not because of cost.** §1.5. The outputs are unmanufacturable in your shop. Reject it on manufacturability, never on price |
| **Text-to-CAD** (Zoo, formerly KittyCAD) | "Describe a part, get CAD" | Produces simple, single, self-contained parts. Does not produce assemblies, mates, constraint-driven design intent, or anything that fits an existing robot | Freemium: **40 free min/month**, then **$0.50/min**. App is open source | **[C]** fetched 2026-08-22 | **NO for the robot.** Toy value only — and the free tier is ample for proving that to yourself. §2 |
| **Image-to-CAD / scan-to-CAD** | Photo or scan → solid model | Mesh reconstruction, not parametric solids. Meshes are not editable design intent | Varies — **UNVERIFIED** | UNVERIFIED | **NO.** You cannot dimension a mesh |
| **LLM as an engineering calculator** | "Compute the gear ratio" | **Actively dangerous.** Confident arithmetic with silent unit errors. §3.0 documents one caught in this pass | Free | **[C]** | **NO — use §3's scripts.** But LLMs are *excellent at writing* the scripts |
| **LLM for manual constraint extraction** | Read the manual, pull the numbers | **Works well, with a rule-ID discipline.** §4.1 | Free–low | **[H]** | **USE IT.** Highest-value non-CAD design use |
| **LLM for DFM / design review** | Critique a design | Works when you state your tooling *and its absence*. §4.3 | Free–low | **[H]** | **USE IT** |
| **Multimodal photo / sketch review** | Look at a prototype and comment | Real capability, bounded by no-depth and no-scale. §5 | Free–low | **[H]** | **USE IT, bounded** |

### 1.0 Verification log — what was actually opened, and when

Verified **2026-08-22** by this pass. Anything not in this table is **UNVERIFIED** wherever it
appears, regardless of how confident the surrounding prose sounds.

| Claim | Status | Source |
|---|---|---|
| Onshape is free for FIRST teams (Educator Plan, FRC **and** FTC) | **[C]** | [onshape.com/en/education/programs-and-partners/first](https://www.onshape.com/en/education/programs-and-partners/first) — "Onshape is proud to provide free access to our CAD platform and resources for FRC and FTC Teams" |
| Educator Plan includes Simulation, Release Management, Classes & Assignments | **[C]** | [onshape.com/en/education/first-robotics](https://www.onshape.com/en/education/first-robotics) |
| CAM Studio is included free with the Educator Plan, for mentors **and** students | **[C]** | [CAM Studio for FRC Teams announcement](https://community.firstinspires.org/2025-cam-studio-for-first-robotics-competition-teams-announcement) |
| No school affiliation required for the Educator Plan | **[C]** | [onshape.com/en/blog/educator-plan-first-robotics-teams](https://www.onshape.com/en/blog/educator-plan-first-robotics-teams) |
| Onshape **AI Advisor** is shipped, in-canvas, on Amazon Bedrock | **[C]** | [PTC press release](https://www.ptc.com/en/news/2025/ptc-announces-latest-onshape-ai-advisor-release) · [Introducing AI Advisor](https://www.onshape.com/en/blog/ai-advisor-guide-cad-pdm) |
| FeatureScript **generation** by AI agents is announced roadmap, not shipped | **[C]** | Same PTC release — listed under planned enhancements. **Do not plan around it** |
| Autodesk Education plan → free Fusion + **unlimited cloud credits** | **[C]** | [Cloud credits for the Education Community](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Cloud-credits-for-the-Education-Community.html) |
| Commercial generative design ≈ 33 credits/study; extension $1,600/yr | **[C]** | [Digital Engineering 24/7](https://www.digitalengineering247.com/article/autodesk-modifies-generative-design-extension-pricing/Generative-Design) |
| Zoo Text-to-CAD: 40 free min/month, then $0.50/min | **[C]** | [text-to-cad.zoo.dev](https://text-to-cad.zoo.dev/) · [3D Printing Industry](https://3dprintingindustry.com/news/open-source-ai-text-to-cad-software-by-zoo-unlocks-accessible-3d-design-236964/) |
| build123d / CADQuery are free, OpenCASCADE-kernel Python CAD | **[C]** | [build123d.readthedocs.io](https://build123d.readthedocs.io/) |
| PTC grants for teams with PTC mentors, opening July 2026 | **UNVERIFIED** — secondary source only | [firstinspireswi.org](https://www.firstinspireswi.org/post/grant-for-first-teams-that-use-onshape). Check before counting on money |
| Onshape AI Advisor's *usefulness* to a novice FRC student | **UNVERIFIED** | Nobody on this team has used it. §1.3 tells you how to test it in one hour |

**The headline finding, stated plainly: every CAD tool discussed in this file costs you $0.**
There is no CAD line item in the budget. The scarce resource in
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) is **hours**, not dollars — 74.9
`cad_design` hours, total. Evaluate these tools on whether they *save hours*, and ignore price
entirely. Any vendor conversation that starts with pricing is aimed at someone who is not you.

**Re-check discipline before any purchase order:**

```bash
# Prices in this space moved materially in the year before this pass. Re-open the page.
# Log the answer into reference/bom/ with a date, the way the BOM files already do:
grep -n "verified" reference/bom/parts_drivetrain.yaml | head    # run from the repository root
```

### 1.2 CADQuery / build123d + LLM — go deep, this is the real one

**What they are.** Both are Python libraries that build B-rep solids on the OpenCASCADE kernel and
export STEP, DXF, STL. CADQuery uses a fluent selector chain (`.faces(">Z").workplane().hole(0.196)`);
build123d is a newer, more Pythonic API over the same kernel with a builder/algebra syntax. Both are
free and open source. **UNVERIFIED** in the sense that this pass did not fetch their repositories;
the description is **[H]**.

**Why LLMs are genuinely good at this and bad at everything else in CAD.** Four properties, and it
is the *conjunction* that matters:

| Property | Consequence |
|---|---|
| The output is **text** | It is the modality LLMs are actually built for. Geometry kernels are not |
| The output is **executable** | You run it. It either produces a solid or raises. There is no "looks right" |
| Failure is **loud** | A hallucinated method is an `AttributeError` in one second, not a part that is wrong in metal in three weeks |
| The result is **parametric by construction** | Change `plate_thickness_in` and re-run. This is what CAD is *for*, and text-to-CAD does not give it to you |

Compare: a text-to-CAD tool hands you a shape. If the shape is wrong you have no handle on it. A
CADQuery script hands you a *program* that produced the shape, and a program is editable by a
15-year-old who can read Python — which, per
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §2.3, you have two to five of.

**Where it earns its keep on an FRC robot.** Not the robot. *Parts.*

| Good fit **[H]** | Bad fit |
|---|---|
| Gussets and plates with a bolt pattern derived from tube size | The whole chassis assembly |
| Spacers, standoffs, shaft collars, bearing blocks | Anything whose shape is decided by fitting around other parts |
| Bumper corner brackets, mounting adapters | Mechanism layout and packaging |
| Anything with a **pattern** — hole grids, sprocket-clearance slots, lightening | Anything a human would draw by looking at it |
| **Parts you need 40 slightly-different copies of** | One-off shapes with no parameter |
| Flat DXF for outsourced 2D cutting (constraint #4 in the capacity model's hierarchy) | 3D machined parts |

**The workflow that works [S]:**

```
1. Describe the part with EVERY dimension named as a parameter (templates/design-prompts.md §4)
2. LLM writes the script; you paste your library version and forbid invented methods
3. RUN IT. Not optional. Reading generated CAD code proves nothing.
4. Assert-check it in-script: bounding box, mass at material density, min edge distance
5. Export STEP -> import into Onshape as a derived part -> mate it in the real assembly
6. Print/cut ONE. Test fit. Change the parameter. Re-run.
```

Step 4 is the one people skip. An assertion block turns "the code ran" into "the code produced a
part that is 4.00 in long and weighs 0.31 lb", which is a different and much stronger claim.

**The honest limitation.** Code-CAD is *worse* than direct modelling for anything shaped by
context — i.e. most of a robot. You cannot usefully write a script for "the plate that connects the
elevator to the frame in the space left over after the battery moved". A human in Onshape does that
in ten minutes; a script does it in an hour and is wrong when the battery moves again.

### 1.3 Onshape — use it, for the CAD

Onshape is the de-facto FRC CAD standard **[H]**: browser-based (so it runs on school Chromebooks,
which matters), real-time multi-user (so two students can be in the same assembly, which matters
more when you have five core-technical students), versioned, with mature FRC part libraries.

**Licensing, now confirmed [C].** The **Educator Plan is free for FRC and FTC teams**, and your team
does **not** need a school affiliation to qualify — educational use is the only test. It includes
Simulation, Release Management, and Classes & Assignments. Sign-up is at `onshape.com/edu`. Sources
in §1.0.

**The genuinely useful thing nobody budgets for: CAM Studio is free on that plan**, for students as
well as mentors **[C]**. That is toolpath generation bundled at $0. It is not AI and it is not what
this file is about, but it is the highest-value line in §1.0 for a team whose tooling ladder tops out
at a bandsaw and a drill press — because it is the software half of the outsourcing and
sponsor-machine-shop path that
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §5.2 already assumes. **[S]** If a
sponsor has a CNC router and you have never handed them a toolpath, this is the off-season project
with the best ratio of payoff to hours in this entire file.

**On AI Advisor specifically [C].** It is shipped, it lives in the design canvas, it runs on Amazon
Bedrock, and it gives step-by-step guidance, troubleshooting and best-practice tips. Read what that
is: **a help system that knows where your cursor is.** For a novice FRC student who does not yet know
what a feature is called, that is a real reduction in mentor-interrupt load — and mentor unblock time
is capped at **3.4 h/wk** in the capacity model, making it one of the tightest constraints you have.
It does not model anything for you.

> **Test it in one hour, in November, before you form an opinion [S].** Sit a *second-year* student
> down with a task they have done before, with AI Advisor on. Measure one thing: how many times they
> had to ask the mentor. Compare against your memory of last year. That is the whole evaluation. Do
> not run this in January, and do not run it on a first-year student — you will be measuring their
> learning curve, not the tool.

Its last relevance to this file is a warning: **Onshape's built-in interference detection is exact,
free, and one click.** Any AI-based "check my CAD for collisions" workflow (§5.2) is strictly worse
than the button already in the software. Use the button. Use AI for what the button cannot do.

### 1.4 FeatureScript via LLM — marginal, and here is the honest reason

FeatureScript is Onshape's domain-specific language for custom features. It is real, it is
powerful, and it is exactly the wrong shape for an LLM: a **small** language with a **moving**
standard library and **thin** public documentation compared to Python. LLM output quality tracks
training-corpus volume, and the FeatureScript corpus is orders of magnitude smaller than Python's.
The observable result is a much higher rate of confidently-invented `std` functions **[H]**.

**PTC has announced AI agents that generate FeatureScript — treat it as roadmap, not as a plan [C].**
The same press release that shipped AI Advisor lists FeatureScript generation under *planned*
enhancements, alongside automated geometry generation and AI-assisted rendering. Announced is not
shipped, and shipped is not good. **[S]** The correct posture: check once at the **2026-11-12**
Pre-Kickoff Virtual Kit Release, and if it has shipped by then, evaluate it against §1.4's actual
objection — which is corpus size, and which a first-party tool with access to the real std library
*could* legitimately fix. That would be a genuine change in the verdict, and it is the one item in
this file most likely to move before kickoff.

**Verdict:** worth an hour of a student's time in November if that student already knows Onshape
well. Not worth a build-season hour in January. The prompt in
[`templates/design-prompts.md`](templates/design-prompts.md) §5 includes the mitigation that
matters — forcing the model to list every std function it called so a human can check the list
against the docs before pasting anything.

### 1.5 Fusion generative design — a real technology that is wrong for you

Generative design is topology optimisation: you specify load cases, keep-out volumes and preserved
faces, and the solver removes material to hit a stiffness-to-mass target. The maths is real. The
results are real. It is not marketing.

> **Correction, and it matters for how you argue this [C].** An earlier draft of this file rejected
> generative design partly on cost — "historically consumes cloud credits". **That is wrong for
> you.** Verified 2026-08-22: an active Autodesk **Education** plan carries **unlimited cloud
> credits**, so generative design costs an education user **$0**. The $1,600/yr extension and the
> ~33-credits-per-study figure are *commercial* pricing and do not apply.
>
> This is worth flagging as a method point, not just a fact: the cost objection was the *easy* one,
> and it was the *false* one. Reject generative design on manufacturability — reason 1 below — which
> is true, checkable against your own tooling list, and does not evaporate the moment a vendor runs a
> promotion. **If you argue against a tool on price and the price goes to zero, you have no argument
> left.** Make sure the reason you reject something is the reason that is actually load-bearing.

It is still wrong for this team, for four independent reasons — any one of which is disqualifying,
and **none of which is cost**:

1. **Manufacturability.** Outputs are organic, doubly-curved shapes. Your shop is a bandsaw, a
   drill press, and one FDM printer ([`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md)
   §5.2, route C). You cannot make them, and the outsourced path you *do* have is **2D flat sheet**,
   which is the one thing generative design does not produce.
2. **Setup cost exceeds the benefit.** Defining load cases correctly is a day of work. FRC parts are
   overwhelmingly *not* mass-critical — they are **stiffness**- and **hours**-critical.
3. **The weight is not where you think.** Run `cg_tip.py` on the worked example: the drivetrain,
   bumpers and battery are ~50% of the mass and none of them is a candidate. Optimising a bracket
   from 0.31 lb to 0.22 lb saves 0.09 lb against a 6.1 lb margin.
4. **It optimises the wrong variable.** `PF` weights reliability at **88** and drive practice at
   **90**. Mass is not in the top factors. A lighter, weaker bracket that fails in match 40 is a
   strictly worse outcome than a heavy one that does not.

**When it would be right:** a team with a CNC mill or metal additive, a mass budget genuinely at
the limit, and slack engineering hours. That is not a 15-student team with 599 effective hours and
zero slack (`02_TEAM_CAPACITY_MODEL` §3.3).

---

## 2. The honest answer on text-to-CAD for a competitive robot

**Short version: text-to-CAD cannot design a competitive FRC robot, and the gap is not one of
model quality. It is a gap of kind, not degree, and more training will not close it.**

Here is why, stated as five things it cannot do. Each is a *requirement* of a competitive robot,
not a nice-to-have.

### 2.1 It cannot hold design intent

CAD's value is not the shape. It is the **constraint graph**: this hole is concentric with that
bearing; this face is coincident with the frame rail; this dimension is driven by that one. When
the game piece turns out to be 2 in wider than the prototype assumed, a constrained model updates
and a shape does not. Text-to-CAD emits shapes. **The most valuable property of CAD is precisely
the property text-to-CAD does not produce.**

### 2.2 It cannot do assemblies, and a robot is nothing but an assembly

Ask for "an intake" and the interesting problem is not the roller. It is: where does it mount,
what does it collide with through its full sweep, does the chain have a tensioning path, can a
human reach the bolts after the elevator is installed, does it stay inside the frame perimeter in
every position. Those are all *relational*. Every current text-to-CAD tool produces a single,
context-free part. **UNVERIFIED** as of 2026-08-22 that any produces a constrained multi-body
assembly with mates; treat any claim that one does as marketing until you watch it happen.

### 2.3 It has never seen your robot, and it has never seen BIOCORE

An LLM's knowledge of FRC ends at its training cutoff. **BIOCORE's rules are not in any model's
training data and will not be until well after kickoff.** A model asked to "design a robot for
BIOCORE" will produce a competent-sounding blend of previous seasons. This is the single most
expensive failure available to you on kickoff day, because it *looks* like progress and it consumes
the strategy hours (25 veq-h, `02_TEAM_CAPACITY_MODEL` §3.1) that are your entire game-analysis
budget.

### 2.4 It cannot be inspected

Your robot passes through a human inspector against a rule set. Frame perimeter, BUMPER geometry,
weight, extension limits, motor legality. A generated shape has no traceability from any dimension
back to a rule ID. The extraction workflow in §4.1 exists precisely to build that traceability, and
it is text, not geometry.

### 2.5 It removes the learning that is the point

`02_TEAM_CAPACITY_MODEL` §5.5 shows adding five students buys **zero** additional mechanisms,
while §9.4 shows losing **one** unsupervised lead costs **half** your mechanism capacity. The
binding resource is *students who can own a design decision*. A student who has watched a tool
extrude a shape has not become one. A student who prototyped in cardboard, measured it, argued
about the transmission angle, and then drew it, has.

### 2.6 What this leaves — the accurate claim

| Claim | True? |
|---|---|
| "AI can generate a CAD model of a part" | **Yes**, via code-CAD, for simple parametric parts (§1.2) |
| "AI can generate a CAD model of an FRC mechanism" | **No** |
| "AI can generate a competitive FRC robot design" | **No, and not soon** |
| "AI can accelerate the *thinking* around CAD" | **Partly** — §4 is that list, and it is long, but each item is worth 1–4 h, not a transformed workflow. See §6.3 and the closing line of §7 |
| "AI can do the desk work so students spend hours on the robot" | **Yes**, and this is the real win |

The last row is the one to plan against. The value is not in the CAD. It is in everything that
surrounds the CAD.

**Do not take this section on faith — the disproof is free [C].** Zoo's Text-to-CAD gives **40
minutes per month at no cost** (§1.0). That is more than enough to settle the argument empirically,
and a student who has seen it fail will argue the point far better than one who was told.

> **The 20-minute November exercise [S].** Give a student three prompts, in this order:
> 1. *"A 2 in × 2 in aluminium plate, 0.125 in thick, with a 0.196 in hole in the centre."* — this
>    will probably work. It is a single part with no context.
> 2. *"A gusset that joins two pieces of 2×1 in tube at 37 degrees, with the standard FRC hole
>    pattern."* — watch what happens to the hole pattern, and ask what "standard" it used.
> 3. *"An intake for a 2027 FRC robot."* — this is the one that matters.
>
> Then have them try prompt 2 again with CADQuery via an LLM (§1.2), and **run** the result. The
> difference they will notice is not output quality. It is that the failing script *said* it failed,
> in one second, on a specific line — and the shape just sat there looking plausible.
>
> Log the outputs in your engineering notebook with the date and the exact prompts. That is
> evidence for the Engineering Design / Innovation in Control judging conversation
> ([`../awards/AWARD-ALIGNMENT.md`](../awards/AWARD-ALIGNMENT.md)): a team that *tested* a tool and
> rejected it with a reason is demonstrably stronger than one that either dismissed it or
> credulously adopted it. Attribution per
> [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) applies to anything you keep.

---

## 3. Where AI *is* strong — the calculators, built and run

### 3.0 Why these exist at all, and the error that proves the point

Do not ask a language model for engineering numbers. Ask it to **write the script** that produces
them, then run the script, then check the script against a second implementation.

**[C] A concrete, caught-in-this-pass example.** The first version of `drivetrain.py` modelled a
current-limited drivetrain by putting the **stator** current limit straight onto the battery. It
reported that four Kraken X60s at a 60 A limit draw **265 A** through the 120 A main breaker while
pushing a wall — which would mean every current-limited swerve robot in FRC trips its main breaker
on first contact. They do not. A motor controller is a buck converter: the battery sees
**supply** current = duty × stator current, and at zero shaft speed the duty is small. The
corrected model reports **240 A of stator current at 18% duty → 67 A at the breaker**, which is
consistent with reality. **The error was a factor of ~3.5, it was confidently formatted, and it was
only caught by running the model and disbelieving the output.**

That is the whole methodology of this section. Every number below is script output you can
reproduce, and every script says out loud where its model is thin.

**Already solved — do not duplicate:**
[`../../tools/cycle-model.py`](../../tools/cycle-model.py) does cycle time, per-strategy expected
value in a 150-second match, fixed-action opportunity cost (is a 30-point climb worth the cycles it
costs?), and RP-threshold analysis, with a validated 2026 REBUILT worked example. Shooter and
scoring-EV maths lives there. `python tools/cycle-model.py --game rebuilt --sweep`.

### 3.1 `drivetrain.py` — speed, torque, current, brownout

**The question it settles:** which gear ratio do we order, and will the bus brown out.

```
$ python drivetrain.py
===============================================================================
DRIVETRAIN ANALYSIS  --  4 x Kraken X60 (trapezoidal)
  motor data: [C] parts_electronics.yaml:125 (WCP motor-performance page)
===============================================================================
CONFIG  ratio 6.12:1 | wheel 4.0 in | robot 125 lb | COF 1.10 | 60 A/motor | eta 0.92

SPEED
  theoretical free speed ..................  17.11 ft/s   <- the number on the box
  simulated top speed (loaded, sagging) ...  17.16 ft/s   (100% of free)
  0 -> 10 ft .............................. 0.95 s

FORCE  (whichever is smaller decides whether you push or spin)
  traction limit (COF x weight) ...........  137.5 lbf
  motor force at  60 A limit .............  115.8 lbf
  motor force at true stall (no limit) ....  706.6 lbf
  --> TORQUE-LIMITED. You stall and cook motors before you slip. GEAR DOWN.

CURRENT / BROWNOUT   (Systemcore brownout threshold UNVERIFIED -- see motors.py)
  PUSH INTO A WALL, limit ON:
    stator current (what heats the motor) .  240.0 A total, duty 18%
    SUPPLY current (what the breaker sees)    67.3 A total, bus 11.15 V
    sustained push force ..................  115.8 lbf
    main breaker .......................... under 120 A main breaker
  PUSH INTO A WALL, limit OFF (do not do this):
    SUPPLY current ........................   87.2 A, bus 10.69 V --> under 120 A
  SPRINT:
    peak supply current ...................  264.0 A, bus min 6.63 V
    peak stator current ...................  240.0 A
  brownout threshold (roboRIO 1) ..........   6.80 V  --> BROWNOUT RISK
    FIX [S]: drop the per-motor limit to ~39 A, or slew-rate-limit the joystick so
    all four motors never command full throttle from a standstill simultaneously.

SPRINT TRACE    t(s)   v(ft/s)   I_total(A)   V_bus
               0.00      0.06         67.3   11.15
               0.25      7.37        250.7    6.94
               0.50     12.31        139.2    9.50
               0.75     14.77         83.8   10.78
               1.00     16.00         56.2   11.41
               1.25     16.61         42.5   11.72
               1.50     16.91         35.6   11.88
               1.75     17.06         32.2   11.96
               2.00     17.14         30.5   12.00
```

**Three findings a small team can act on immediately:**

1. **Pushing into a wall is not what browns you out — accelerating is.** The wall push draws 67 A
   at the breaker because duty is 18%. The *sprint*, at ~0.25 s in when duty has climbed but the
   motors still want limit current, hits 264 A and drags the bus to 6.63 V. This inverts the
   intuition almost every team has.
2. **A 60 A limit on 6.12:1 with 4 in wheels is torque-limited, not traction-limited** — you are
   leaving 22 lbf of available push on the table and heating motors to get it.
3. The fix is free: **lower the current limit and slew-rate the joystick.** No parts, no hours.

**And the ratio table, which is the actual kickoff-day artefact:**

```
$ python drivetrain.py --sweep
GEAR-RATIO SWEEP  --  4 x Kraken X60 (trapezoidal), 4.0 in wheel, 125 lb, COF 1.10, 60 A limit
  ratio  free ft/s   top ft/s  0-10ft s   traction   F@limit   push A  verdict
   4.00      26.18      25.93      1.05      137.5      75.7       67  TORQUE-LIMITED
   4.50      23.27      23.23      1.01      137.5      85.2       67  TORQUE-LIMITED
   5.00      20.94      20.94      0.98      137.5      94.6       67  TORQUE-LIMITED
   5.50      19.04      19.07      0.96      137.5     104.1       67  TORQUE-LIMITED
   6.00      17.45      17.50      0.96      137.5     113.6       67  TORQUE-LIMITED
   6.12      17.11      17.16      0.95      137.5     115.8       67  TORQUE-LIMITED
   6.75      15.51      15.58      0.96      137.5     127.8       67  TORQUE-LIMITED
   7.50      13.96      14.04      0.98      137.5     142.0       64  traction-limited OK
   8.50      12.32      12.41      1.03      137.5     160.9       55  traction-limited OK
  10.00      10.47      10.56        --      137.5     189.3       46  traction-limited OK

PICK RULE [S]: take the FASTEST ratio still traction-limited at your current limit,
then step one slower for margin. Speed you cannot put on the carpet is not speed.
```

Note the column nobody expects: **0-to-10-ft time barely moves across the whole table** (0.95 s to
1.05 s). Over a 2.4× range of gear ratio, sprint time varies by 10%, because the sprint is
traction- and voltage-limited, not gearing-limited. **[S]** The practical consequence: gear for
push force and for the top speed you can actually control, and stop arguing about acceleration.

A second worked configuration, a 6-NEO tank drive, which lands on the other side of the verdict:

```
$ python drivetrain.py --motor neo --motors 6 --ratio 8.45 --wheel 6 --weight 120 --limit 40
  traction limit (COF x weight) ...........  132.0 lbf
  motor force at  40 A limit .............  136.3 lbf
  --> TRACTION-LIMITED. Wheels slip before motors stall. Correct design point.
  PUSH INTO A WALL, limit ON:
    stator current (what heats the motor) .  232.4 A total, duty 46%
    SUPPLY current (what the breaker sees)   131.3 A total, bus 9.68 V
    main breaker .......................... OVER 120 A MAIN BREAKER
```

Same robot mass, *lower* per-motor limit, and it **does** exceed the main breaker — because six
motors at 46% duty is a different animal from four at 18%. This is exactly the kind of result no
one gets right by intuition.

### 3.2 `elevator_arm.py` — gravity loads, holding torque, ratchets and gas springs

**The question it settles:** will it lift, will it *hold*, and do we need a ratchet.

```
$ python elevator_arm.py elevator
===============================================================================
ELEVATOR SIZING  --  2 x Kraken X60 (trapezoidal) @ 12.0:1, 1.75 in drum, 2-stage continuous rig
===============================================================================
LOAD    carriage+game piece 18.0 lb, travel 48 in, friction allowance x1.25
  force at carriage .......................    22.5 lbf
  force at drum (x 2 stages) ..............    45.0 lbf

TORQUE
  to HOLD position ........................   0.436 Nm  (3.9 in-lb)
  to ACCELERATE to 1.00 s full travel .....   0.631 Nm
  available at 40 A limit .................   1.550 Nm
  available at true stall (no limit) ......  14.180 Nm
  --> dynamic margin ......................    2.45 x  OK

SPEED
  kinematic max carriage speed ............    91.6 in/s
  fastest possible full travel ............    0.52 s  (target 1.00 s)

HOLDING CURRENT -- the line that decides whether you need a ratchet
  current per motor to hold ...............    11.3 A  (3% of stall current)
  thermal verdict [S] ..................... safe indefinitely

COUNTERBALANCE / RATCHET SIZING
  constant-force spring to fully null gravity ... 22.5 lbf at the carriage
  gas springs (a PAIR, one per side), by counterbalance fraction:
       50% counterbalance -> 2 x    5.6 lbf gas springs
       75% counterbalance -> 2 x    8.4 lbf gas springs
      100% counterbalance -> 2 x   11.2 lbf gas springs
  holding current at 80% counterbalance ......... 2.3 A/motor (safe indefinitely)
  RATCHET/pawl must hold ........................ 4.45 Nm (39 in-lb) at the DRUM shaft
  NOTE: spec the ratchet at the DRUM, not at the motor. At the motor it is 12x smaller
        and a slipping gearbox between ratchet and load makes the ratchet decorative.
```

**The two lines that earn this tool's existence:**

- **"force at drum (x 2 stages)"** — a continuously-rigged cascade elevator multiplies force at
  the drum by the stage count. Getting this backwards is the most common elevator sizing error
  **[H]**, and it under-sizes the gearbox by exactly the stage count.
- **"RATCHET must hold ... at the DRUM shaft"** — spec the ratchet at the load, not at the motor.
  A pawl on the motor shaft is 12× understressed on paper and completely defeated by any
  compliance between it and the load.

Now the arm, at 100:1 on a single NEO:

```
$ python elevator_arm.py arm
ARM SIZING  --  1 x REV NEO v1.1 (empirical) @ 100:1, 12.0 lb at 22.0 in CG radius
  worst-case gravity torque (arm horizontal) ..   29.83 Nm  (264 in-lb)
  available at 40 A limit .....................   74.29 Nm
  torque to also ACCELERATE (1.2 s sweep) ......   42.34 Nm
  STATIC margin ................................    2.49 x  OK
  DYNAMIC margin ...............................    1.75 x  OK
  free-speed sweep time (no load) ..............    0.40 s  (target 1.20 s)
  holding current ..............................    16.1 A/motor (15% of stall)
  thermal verdict [S] .......................... OK for a match; motor gets warm
  back-drive ................................... marginal. Brake mode may hold it cold
                                                  and fail warm. Ratchet recommended [S]

  angle  gravity Nm                            net Nm   hold A
    -30        25.83           0.00      25.83     13.9
      0        29.83           0.00      29.83     16.1
     45        21.09           0.00      21.09     11.4
     90         0.00           0.00       0.00      0.0
```

And what a counterbalance buys back:

```
$ python elevator_arm.py arm --gas-spring
GAS-SPRING OPTIMISATION  (minimise peak |net torque| over the sweep)
  uncounterbalanced peak gravity torque .. 29.83 Nm
  best: 30 lbf gas spring at 6.0 in arm radius -> peak net 11.32 Nm
  reduction .............................. 62%

  arm r (in)   spring (lbf)   peak net Nm
        3.0             40         16.72
        3.0             80         13.92
        4.0             40         11.75
        4.0             80         15.26
        5.0             40         12.05
        5.0             80         16.38
```

**Read the sweep table, not just the headline.** Note the non-monotonicity — at a 4 in arm radius,
40 lbf is *better* than 80 lbf, because an over-strong spring simply reverses the sign of the peak
torque and you are back where you started with the arm trying to fly up. Counterbalancing is a
matching problem, not a "more is better" problem, and it is the kind of thing a table finds and
intuition does not.

**What the 62% reduction is worth in the currency that matters:** it lets you drop from 100:1 to
roughly 38:1, which is ~2.6× faster arm motion for the price of two springs, or it lets you delete
a motor. Either outcome is bought with an afternoon of geometry rather than with build hours.

### 3.3 `fourbar.py` — linkage synthesis, transmission angle, frame-perimeter check

**The question it settles:** does the linkage bind, and does it leave the frame perimeter.

```
$ python fourbar.py analyze
FOUR-BAR ANALYSIS   crank a=6.00  coupler b=18.00  rocker c=12.00  ground d=20.00 (in)
  coupler point P at (10.00, 3.00) in the coupler frame; payload 15.0 lbf vertical
  Grashof: Grashof (crank-rocker or double-crank): at least one link fully rotates
           s+l = 26.00  vs  p+q = 30.00

  crank deg      Px      Py   trans.angle   crank torque(in-lb)   coupler deg
       -20    9.81    7.52       53.4                62.8         49.7
         0   11.46    8.90       51.0                54.8         41.8
        20   12.32   10.07       53.4                46.2         33.5
        40   12.17   11.05       60.0                36.9         26.8
        60   11.13   11.75       69.4                22.0         22.2
        80    9.50   12.04       80.2                 1.1         19.2
       100    7.58   11.79       91.3                22.6         17.6

  minimum transmission angle .............. 51.0 deg  --> OK (>=40)
  peak crank torque under 15 lbf ......... 62.8 in-lb (7.09 Nm)
  coupler-point bounding box .............. x [6.61, 12.37]  y [7.52, 12.04]
  horizontal reach 5.76 in, vertical rise 4.52 in
```

The **transmission angle** column is the reason to run this. Below ~40° the linkage approaches a
toggle and the required torque climbs toward infinity; below ~30° it binds. The tool flags every
row. As a demonstration, the change-point geometry `a=6 b=20 c=6 d=20` (equal-length crank and
rocker with equal coupler and ground — a very natural thing to draw on a whiteboard) reports:

```
  Grashof: Change point (special-case Grashof): links can align, motion is ambiguous. AVOID
  minimum transmission angle .............. 0.0 deg  --> TOGGLE / WILL BIND. Redesign.
```

That is a mechanism that looks fine in a sketch, works when you push it by hand in cardboard, and
locks up under load in aluminium.

The **bounding box** is your frame-perimeter check. Compare `max x` against your frame half-width
plus BUMPER thickness — using 2026 R102/R104 as a **[H] baseline only**, because BIOCORE's
extension rules do not exist until 2027-01-09.

Sizing a parallelogram lift from the travel you want:

```
$ python fourbar.py parallel --dx 14 --dy 20 --link 24
  target travel ......... dx 14.0 in, dy 20.0 in   link length 24.0 in
  start link angle ......   -65.6 deg
  end link angle ........    -4.4 deg
  swept angle ...........    61.1 deg   <- this is what your gearbox must deliver
  ground clearance at the low position .. -15.9 in (pivot at 6.0 in)
      --> BELOW 1 in. This drags on carpet or on the field border. Raise the pivot.
  peak torque at the pivot under 15 lbf .. 359 in-lb (40.6 Nm)
  max horizontal extension past the pivot .. 23.9 in
  closure check: achieved dx 14.000, dy 20.000 in (must match the target)
```

The tool solves the geometry exactly (the closure check confirms it) **and then tells you the
design is bad**: a 24 in link that delivers 20 in of rise has to start pointing steeply downward,
so the end effector is 15.9 in below the carpet at the start of travel. This is a real result, not
a bug — it is the tool refusing to let a feasible-on-paper linkage through. The fixes are all
visible in the same output: shorter links with more sweep, a raised pivot, or an elevator instead.

And two-position synthesis, for when you know where the end effector must start and finish:

```
$ python fourbar.py synth2 --p1 4,6 --p2 22,26 --pivot 0,2
  moving pivot at position 1 .... (4.00, 8.00)
  moving pivot at position 2 .... (22.00, 28.00)
  chord length .................. 26.91 in
   offset(in)     ground pivot          link length     swept angle
      -12.0     (  21.92,    9.97)         18.03          -96.5 deg
       -8.0     (  18.95,   12.65)         15.65         -118.5 deg
       +8.0     (   7.05,   23.35)         15.65         +118.5 deg
      +12.0     (   4.08,   26.03)         18.03          +96.5 deg
```

Every row is a *valid* solution — the ground pivot may sit anywhere on the perpendicular bisector.
You pick by packaging. That is the correct division of labour: the tool enumerates the solution
family, and the human chooses using knowledge (what is already in that corner of the robot) that
the tool does not have.

### 3.4 `cg_tip.py` — centre of gravity and tip-over

**The question it settles:** does it slide before it tips — *with the mechanism up*.

```
$ python cg_tip.py
CG + TIP-OVER  --  stowed / driving configuration
  component                                   mass lb    x in    y in    z in
  swerve modules + drive motors (4)              34.0     0.0     0.0     3.0
  frame + belly pan + tube                       16.0     0.0     0.0     3.5
  bumpers (4 sides)                              18.0     0.0     0.0     5.5
  battery                                        12.9    -8.0     0.0     4.0
  electrical board + PD + Systemcore              8.0    -4.0     0.0     6.0
  elevator frame (static)                        11.0     2.0     0.0    22.0
  elevator carriage + end effector               14.0     6.0     0.0    12.0
  intake                                          9.0    13.0     0.0     7.0
  pneumatics / misc / fasteners                   6.0     0.0     0.0     8.0
  TOTAL                                         128.9

CENTRE OF GRAVITY   x +0.68 in (fwd+)   y +0.00 in (left+)   z 6.81 in (above carpet)
  CG height as a fraction of half-track ... 0.57  (lower is better; < 1.0 is healthy [S])

WEIGHT vs the 2026 BASELINE limits [H] -- BIOCORE limits UNKNOWN until 2027-01-09
  with bumpers .........  128.9 lb  vs 135.0 lb (2026 R408)  --> under 2026 R408 by 6.1 lb
  bare estimate ........   98.0 lb  vs 115.0 lb (2026 R103)  --> under 2026 R103 by 17.0 lb

TIP-OVER   wheelbase 24.0 in, track 24.0 in
  direction                   tips at (g) static ramp (deg)
  forward (braking)                  1.86           61.8
  backward (accelerating)            1.66           59.0
  left                               1.76           60.4
  right                              1.76           60.4

  traction-limited acceleration (COF 1.10) .. 1.10 g
  worst tipping acceleration ................ 1.66 g
  --> SLIDES BEFORE IT TIPS. This is the design target. Margin 51%.

-------------------------------------------------------------------------------
EXTENDED / SCORING CONFIGURATION: elevator carriage + end effector
  CG moves to x +0.68, y +0.00, z 11.15 in (was +0.68, +0.00, 6.81)
  worst tipping acceleration ................ 1.01 g   (was 1.66 g, -39%)
  worst static ramp angle ................... 45.4 deg
  --> TIPS BEFORE IT SLIDES WHEN EXTENDED. Interlock the drivetrain speed against
      mechanism height in software, and say so in the design review.
```

**This is the single most valuable output in the file.** The robot is comfortably stable stowed
(1.66 g tipping vs 1.10 g traction, a 51% margin) and **tips before it slides when the elevator is
up** (1.01 g vs 1.10 g). Moving 14 lb from z=12 in to z=52 in destroys a 51% margin.

The consequences are concrete and cheap:

1. **A software interlock** that scales maximum drive acceleration with mechanism height. This is
   a ten-line change in the drive subsystem and it belongs in the design review document, not in a
   bug report in week 6.
2. **Two calculators talk to each other:** the tool prints the follow-on command
   `python drivetrain.py --cof 1.10 --weight 129`, so the traction number you assumed in the
   tip analysis is the same one used for the sprint model. Consistency between models is not
   automatic and is worth engineering.
3. **The weight column doubles as a rule check** against the 2026 R103/R408 baseline — flagged
   **[H]**, because the BIOCORE limits are unknown until kickoff.

**Feed it your own numbers** with `--parts myrobot.json` (a JSON list of
`{"name","mass_lb","x","y","z"}` in inches, origin at the centre of the frame footprint at carpet
level). Ten minutes with a kitchen scale and a tape measure produces a better CG model than any
CAD mass-properties estimate that has not been reconciled with reality.

### 3.5 What the calculators do NOT do — stated plainly

| Not modelled | Why it matters | What to do instead |
|---|---|---|
| Transient inductive spikes on direction reversal | This is what actually browns out real robots | Log bus voltage on the real robot; the calculator is necessary, not sufficient |
| Motor thermal behaviour over a match | Stall current limits are time-dependent; `THERMAL` in `elevator_arm.py` is **[S]** heuristics | Touch the motor after a practice match. Seriously |
| Battery ageing | Internal resistance rises with cycles; the model uses one healthy value **[S]** | Load-test batteries; retire the bad ones |
| Structural deflection and stiffness | Every mechanism here is treated as rigid | Push on it hard in cardboard, then in metal |
| Chain/belt stretch, backlash, compliance | Affects repeatability, which affects auto | Design the sensor at the load, not at the motor |
| Anything about BIOCORE | The manual does not exist | Re-run everything on 2027-01-09 |

---

## 4. Trade studies, DFM, BOM, and manual constraint extraction

These are the four highest-value uses of AI in design, and none of them produces geometry. All four
prompt templates live in [`templates/design-prompts.md`](templates/design-prompts.md).

### 4.1 Extracting every dimensional constraint from the game manual

**The single highest-value AI task on kickoff day. [H]** A game manual is ~160 pages; the numbers
that constrain a mechanism are scattered across the field section, the game section, the robot
rules and the inspection checklist. A human doing this well takes most of a day. The structured
extraction in [`templates/design-prompts.md`](templates/design-prompts.md) §1 takes an hour and —
critically — **produces a rule ID on every row**, which is what makes it checkable.

**The discipline that makes it safe:**

- Every row must carry a rule ID that appears literally in the pasted text. No ID, no row.
- Verbatim quotes only, ≤25 words. Paraphrase is where numbers drift.
- The model is forbidden from using outside knowledge. It has none about BIOCORE anyway.
- **The most valuable output is the model's list of dimensions the manual does *not* specify.**
  That list is your Q&A submission list on **2027-01-13** and feeds
  [`../QA-AMBIGUITY-HOTSPOTS.md`](../QA-AMBIGUITY-HOTSPOTS.md).

Reconcile against the machine-readable inventory, which is deterministic and does not hallucinate:

```bash
# Run from the repository root.
bash tools/ingest-manual.sh        # on kickoff day, against the BIOCORE PDF
python tools/rule-inventory.py     # -> research/rule_inventories/2027_rules.tsv
python tools/rule-show.py R103     # then spot-check the AI table row by row
```

**AI extracts; the inventory verifies; a human signs off.** Never the AI alone — an inspection
failure costs a match, and `PF` weights reliability at 88.

### 4.2 Trade studies and decision matrices

AI is good at *populating* a matrix and bad at *weighting* one. Fix the weights yourself. The
template ([`templates/design-prompts.md`](templates/design-prompts.md) §3) forces:

- weights supplied by you and explicitly locked;
- an **evidence tag** on every cell ([C]/[H]/[S]), so unsupported cells are visibly discountable;
- a **sensitivity question** — which criterion drives the ranking, and what happens if you halve
  its weight;
- an explicit strongest-argument-against the winner;
- **a physical test, under two hours, that would resolve the biggest uncertainty.**

The last item is the one that converts the exercise into progress. Then run the project's own
scorer, which is calibrated to this team rather than to the internet:

```bash
python tools/score-strategy.py        # the achievability rubric, backtested in reference/05_RUBRIC_BACKTEST.md
python tools/cycle-model.py --game rebuilt --sweep
```

Where the AI matrix and `score-strategy.py` disagree, the rubric wins, because the rubric is
denominated in **your** 599 effective hours and **your** `novel_mechanisms_max = 2`.

### 4.3 DFM review of a design description

The prompt that works states the shop **and its absence** — no mill, no lathe, no CNC router, no
welding — because a model given only positive capabilities defaults to advice for a machine shop.
Full template at [`templates/design-prompts.md`](templates/design-prompts.md) §6. The five outputs
worth asking for:

1. features that cannot be made with your tools, and the nearest that can;
2. features that need a fixture or jig students will get wrong first time;
3. tolerance stack-up — which two features must actually be concentric or square;
4. **fastener access after assembly** — can a hand tool physically reach every bolt;
5. the one change that most reduces fabrication hours without changing function.

**Item 4 finds more real problems than the rest combined [H]**, and it is exactly the kind of
review a small team never gets because it has one experienced mentor with
**3.4 h/week of unblock capacity** (`02_TEAM_CAPACITY_MODEL` §6.2). This is AI substituting for
*absent* review capacity, not for the mentor.

Item 5 matters because fabrication is the largest line in the budget — **129.8 veq-h, 21.7%** of
the season (`02_TEAM_CAPACITY_MODEL` §3.1).

### 4.4 BOM generation and cost-rule compliance

**This is where AI is most dangerous to a budget-constrained team.** Models invent part numbers and
prices with complete confidence, and a wrong price in a BOM is a wrong order.

The rules that make it safe ([`templates/design-prompts.md`](templates/design-prompts.md) §10):

- paste the verified catalogue from [`../bom/`](../bom/) into the prompt;
- an `IN_CATALOGUE?` column that is YES **only** if the part number appears literally in what you
  pasted;
- anything not in the catalogue gets a **blank** price and goes on a "must be researched" list.
  **A guessed price in a budget is worse than a blank**, because a blank gets investigated.

Then reconcile against the tools that hold the real numbers:

```bash
# Run from the repository root.
python tools/bom-builder.py
bash reference/bom/recheck_prices.sh    # re-fetches every SKU and diffs against the locked value
```

The cost authority is [`../bom/`](../bom/) — `parts_drivetrain.yaml`, `parts_manipulation.yaml`,
`parts_electronics.yaml`, `mechanism_catalog.yaml` — every price fetched live on **2026-08-22**,
with `UNVERIFIED` where a page did not load. The AI output is a **draft to be reconciled**, and the
reconciliation is where the errors surface. Budget against
**`robot_discretionary = $2,500`** (`02_TEAM_CAPACITY_MODEL` §8.1), not against the season total.

**Cost-rule compliance** — per-item cost caps and total-cost accounting exist in the FRC rules and
are inspected. The BIOCORE values are **UNVERIFIED** until 2027-01-09. AI can *format* a cost
accounting sheet from your BOM; it cannot tell you the rule. Get the rule from the manual.

---

## 5. Multimodal uses — real, and bounded

### 5.1 Photographing a prototype or whiteboard sketch

**Works. [H]** The highest-value version is not "what do you think of this" but a structured load-
path and failure-mode read: what is in tension, what is in compression, what fails first when this
is aluminium at 3× the speed, and what two measurements to take before CAD.

**The bounds, which must be stated to the students using it:**

- **Scale is guessed unless you give it one.** Always put a ruler, a 12 in speed square, or a known
  game piece in the frame and *say what it is*.
- **It cannot see behind anything.** Ask what it cannot determine, first, before anything else.
- **It will not volunteer that it is uncertain.** The prompt has to demand it.
- The template's final question — *what second photo, from what angle, would most reduce your
  uncertainty* — converts one photo into a deliberate sequence and is the highest-yield line in
  the whole template **[S]**.

Whiteboard sketches specifically: transcribing a kickoff-weekend whiteboard into a structured
mechanism list with open questions is a genuine 20-minute-to-2-minute saving, and it happens at the
exact moment (kickoff Saturday afternoon) when nobody wants to be the scribe.

### 5.2 Reviewing a CAD screenshot for packaging problems

**Works, weakly, and is the most over-sold multimodal use.** State the limitation clearly:

> A CAD screenshot has no depth. The model cannot rotate the assembly, cannot measure, and cannot
> see occluded geometry. It finds *obvious* packaging errors — the kind a fresh pair of human eyes
> finds.

**Onshape's and Fusion's own interference detection is exact, free, and one click.** Run that
first. Use AI for the things geometry checks structurally cannot catch:

| Geometry check catches | AI screenshot review can catch **[S]** |
|---|---|
| Solid-body interference | Assembly *order* problems ("you cannot install this after that") |
| Clearance below a threshold | Hand and tool access to fasteners |
| Mass properties | Wire and pneumatic routing across moving parts |
| — | Battery swap access in under 30 s |
| — | "That looks like it extends past the frame perimeter in this position" |

Send 3–4 views including **one with the mechanism extended**, because the extended position is
where both packaging and tip-over (§3.4) go wrong.

### 5.3 Competitor robot photos and match video

**Works for qualitative description. Fails, badly and confidently, at identification. [C]**

- **Never let a model assign a team number.** Team-number hallucination is reliable and severe.
  The prompt must say: quote a number only if it is literally legible; otherwise "not legible".
- Mechanism-class description from photos (drivetrain type, intake style, scoring architecture) is
  genuinely useful and reasonably reliable.
- Cycle timing from video frames is possible but coarse; "cannot determine" must be an allowed and
  encouraged answer.
- **Quantitative scouting comes from The Blue Alliance and from your own scouts, never from a
  model.** `tools/tba_*.py` and [`../SCOUTING-PLAN.md`](../SCOUTING-PLAN.md) own that.

This matters more for this team than for most: `02_TEAM_CAPACITY_MODEL` §4.4 shows you have
**3 to 5 scouts against the 6 a full manual scheme needs**. AI-assisted qualitative notes on match
video are a partial substitute for scouts you do not have — but they are notes, not data, and the
rubric consequence in §4.4 stands: any strategy that depends on out-scouting the field is out of
reach.

---

## 6. Where AI slots into kickoff → prototype → CAD, without replacing hands-on learning

### 6.1 The rule

> **AI absorbs desk work. Students keep the decisions, the prototyping, the fabrication and the
> driving.**

The test for any proposed AI use, applied honestly:

| Question | If yes |
|---|---|
| Would a student have learned something durable by doing this? | **Do not automate it** |
| Is this transcription, reformatting, cross-referencing, or search? | **Automate it** |
| Does the output need to be *right*, and can it be *checked* cheaply? | Automate the draft, keep the check |
| Does it require judgement about *our* team, *our* shop, *our* budget? | **Human.** The model does not know your shop |

### 6.2 The kickoff-weekend timeline

Times are wall-clock from kickoff, **2027-01-09 12:00 ET**. Hour figures are **[S]** and are
denominated in the 25 veq-h strategy line + 74.9 veq-h CAD line of
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §3.1.

| When | Activity | AI role | Human-only, non-negotiable |
|---|---|---|---|
| **Sat 12:00–14:00** | Watch the reveal, read the manual | **None.** Everyone reads. No summaries | Reading the manual yourselves |
| **Sat 14:00–16:00** | Constraint extraction (§4.1) | **Heavy.** Structured table + the missing-dimensions list | Verifying every row against the text |
| **Sat 14:00–18:00** | *In parallel*: cardboard prototyping of game-piece handling | **None** | **All of it.** This is where the design is actually decided |
| **Sat 18:00–20:00** | Strategy: what scores, what the RPs reward | `tools/cycle-model.py` with a BIOCORE game file; AI helps *write the game file* | Choosing the strategy |
| **Sun 09:00–12:00** | Architecture trade study (§4.2) | **Moderate.** Populate the matrix; you fix the weights | Weights, and the two-hour physical test |
| **Sun 12:00–15:00** | Prototype the top-2 architectures | **None** | **All of it** |
| **Sun 15:00–17:00** | Motor/ratio/CG sizing | **The calculators (§3).** This is where they pay | Reading the verdict lines and deciding |
| **Sun 17:00–18:00** | Scope check against capacity | `python tools/capacity_model.py \| grep BINDING` | Saying no to workstream #4 |
| **Mon+** | CAD | **Light.** Code-CAD for repetitive parts (§1.2); DFM review of the layout (§4.3) | The layout, the packaging, the mates |

Two things to notice. **The Saturday-afternoon parallelism is the whole trick**: AI does the
manual extraction *while* students are cutting cardboard, so the desk work stops competing with
the hands-on work for the same students. And **there is no AI in the prototyping rows.** That is
deliberate and it is the point of §2.5.

### 6.3 The honest accounting of what this saves

Denominated against the 599 effective veteran-equivalent hours to a Week 1 event
(`02_TEAM_CAPACITY_MODEL` §2.5, §3.1). All savings **[S]**.

| Budget line | veq-h | Realistic AI saving | Notes |
|---|---:|---:|---|
| Strategy / rules / game analysis | 25.0 | **−6 to −10** | Constraint extraction is the big win; the decision is not automatable |
| **CAD + design** | **74.9** | **−8 to −15** | Code-CAD on repetitive parts + DFM review. Layout is not automatable |
| Fabrication + assembly | 129.8 | **0** | **The largest line, and AI does not touch it.** Chips are cut by humans |
| Electrical + pneumatics | 49.9 | −2 | Wiring diagrams, labels |
| Programming (incl. Systemcore port) | 134.8 | See [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md) | Out of scope here |
| Integration / debug / reliability | 84.9 | **0 to −3** | Debugging needs the robot in front of you |
| **Drive practice** | 54.9 | **0** | The highest-weighted factor in `PF` (90) is untouched by AI |
| Awards / business / media / scouting | 44.9 | See [`../team-ops/05_business_awards_sustainability.md`](../team-ops/05_business_awards_sustainability.md) | Out of scope here |

**The design-side saving is roughly 15–30 veq-h — about 3–5% of the season.** That is real and
worth having. It is not transformative, and anyone selling you transformative is selling.

**And here is the result that matters most, because it is counter-intuitive:** those recovered
hours **do not raise `novel_mechanisms_max`**. `02_TEAM_CAPACITY_MODEL` §5.2 derives that number
three independent ways; route B (hours) gives 2.27, but routes A (unsupervised student leads) and
C (the single-machine shop queue) both give exactly 2, and the binding value is the minimum. §5.5
shows the same thing for adding five students, and §9.4 shows that even +37% hours leaves the
number at 2.

> **AI buys you hours inside the two mechanisms you were always going to build. It does not buy
> you a third mechanism. Spend the recovered hours on reliability (`PF` weight 88) and drive
> practice (`PF` weight 90), which is where they convert into rank.**

### 6.4 What AI must never be allowed to do on this team

**[S]** except where noted, and every line has a reason with a cost attached.

| Prohibition | Reason |
|---|---|
| Make the architecture decision | §2.5 — the binding resource is students who can own a decision |
| Be cited as a rules authority | The manual and the Q&A are the authorities. Inspection is human |
| Produce a part number or price that goes on a purchase order unchecked | §4.4 — fabricated SKUs |
| Write code that actuates a mechanism without human review | **[C]** `00_FIRST_AI_POLICY_VERIFIED.md` item 3 — a 115.0 lb machine (2026 R103) |
| Replace cardboard prototyping | §6.2 — this is where designs are actually decided |
| Appear in an award submission without attribution | **[C]** *FIRST* requires credit: `"Essay created by Team XXXX and ChatGPT."` |
| Name a team number from a photo | §5.3 — **[C]** reliable hallucination |
| Estimate cycle time | Already solved deterministically by `tools/cycle-model.py` |

### 6.5 The fall programme — what to do before kickoff

`02_TEAM_CAPACITY_MODEL` §7.5 makes the case that every top-ranked constraint is relaxable only
before kickoff. The design-side additions, all costing zero build-season hours:

| Action | Deadline | Why |
|---|---|---|
| Run all four calculators on the **2026** robot and check them against reality | 2026-10 | The calculators are only trustworthy once they have been falsified against a real robot |
| Weigh every subsystem of the 2026 robot; build the `cg_tip.py` parts JSON | 2026-10 | Real masses beat CAD estimates; the file is then reusable |
| Have two students do one CADQuery part end-to-end: script → STEP → print → fit | 2026-11 | Builds the only genuinely new CAD skill on the list |
| Rehearse §4.1 constraint extraction on the **2026 REBUILT** manual and score it against `research/rule_inventories/2026_rules.tsv` | 2026-12 | You want the kickoff-day workflow debugged in December, not on 2027-01-09 |
| ~~Verify Onshape / Fusion education licensing~~ — **DONE 2026-08-22, see §1.0.** Answer: both free, $0 CAD line item | — | Closed. Re-check prices only, not the education terms |
| Claim the **Onshape Educator Plan** at `onshape.com/edu` (no school affiliation needed) and confirm **CAM Studio** appears for students | 2026-09 | **[C]** free, and it is the software half of your outsourcing path (§1.3). Do this first — it is the highest payoff-per-hour item here |
| Run the §1.3 one-hour **AI Advisor** test on a second-year student; record mentor-interrupt count | 2026-11 | Mentor unblock time is capped at 3.4 h/wk. This is the only §1 row still UNVERIFIED that you can settle yourself |
| Run the §2.6 20-minute **text-to-CAD disproof** on Zoo's free tier; log prompts + outputs in the notebook | 2026-11 | Free. Converts a claim in this file into team-owned evidence, and it is judge-ready |
| Re-check whether PTC shipped **AI-generated FeatureScript** (announced roadmap only, §1.4) | after **2026-11-12** | The one verdict in this file most likely to flip before kickoff |
| Write the team AI attribution line into the repo README and the awards template | 2026-12 | **[C]** policy obligation, ~zero cost |
| Re-check the Systemcore brownout threshold and update `motors.py` | after **2026-11-12** | The one place the control-system change touches design |

---

## 7. Prompt templates

All templates live in [`templates/design-prompts.md`](templates/design-prompts.md), each with a
stated failure mode:

| § | Template | Evidence |
|---|---|---|
| 1 | Extract every dimensional constraint from the manual | **[C]** structure tested |
| 2 | Turn constraints into an architecture-neutral design spec | **[H]** |
| 3 | Trade study / decision matrix with locked weights | **[S]** |
| 4 | CADQuery / build123d parametric part generation | **[C]** |
| 5 | FeatureScript with a function-audit trailer | **[S]** |
| 6 | DFM review stating the shop *and its absence* | **[C]** |
| 7 | Photograph a prototype or whiteboard sketch | **[S]** |
| 8 | Review CAD screenshots for packaging | **[S]** |
| 9 | Competitor photos and match video (never team numbers) | **[C]** on the failure mode |
| 10 | BOM generation with an `IN_CATALOGUE?` column | **[C]** on the failure mode |
| 11 | Re-deriving an AI's engineering claim as a runnable script | **[C]** — caught the §3.0 error |
| 12 | The anti-prompt: seven things not to ask, and what to run instead | **[C]** |

---

## 8. Validation / dry run

### 8.1 Everything in §3 is reproducible

```bash
# Run from the repository root.
cd reference/ai-integration/calculators
python motors.py
python drivetrain.py
python drivetrain.py --sweep
python drivetrain.py --motor neo --motors 6 --ratio 8.45 --wheel 6 --weight 120 --limit 40
python elevator_arm.py elevator
python elevator_arm.py arm
python elevator_arm.py arm --gas-spring
python fourbar.py analyze
python fourbar.py parallel --dx 14 --dy 20 --link 24
python fourbar.py synth2 --p1 4,6 --p2 22,26 --pivot 0,2
python cg_tip.py
```

Pure Python 3 standard library. No network, no dependencies, no randomness. Tested on
**Python 3.14.6, Windows 11**, 2026-08-22. Every block quoted in §3 is verbatim script output from
that run.

### 8.2 Internal cross-checks the tools perform on themselves

| Check | Where | Result |
|---|---|---|
| Parallelogram four-bar closure — does the solved geometry actually achieve the requested travel? | `fourbar.py parallel`, `closure check` line | **dx 14.000, dy 20.000 in** against a 14/20 target ✅ |
| Grashof classification vs the transmission-angle sweep — a change-point linkage must show μ→0 | `fourbar.py analyze` on `a=6 b=20 c=6 d=20` | classified "Change point ... AVOID"; min μ = **0.0°** ✅ consistent |
| Traction consistency between `cg_tip.py` and `drivetrain.py` | `cg_tip.py` final line | prints the exact follow-on command with the same COF and mass ✅ |
| Stator vs supply current | `drivetrain.py` | 240 A stator at 18% duty → 67 A supply. Ratio 3.6× ≈ 1/duty ✅ |
| Motor constants | `motors.py` peak power | Kraken X60 computed **1114 W** vs `parts_electronics.yaml:125` published **1108 W** — 0.5% ✅ |

That last row is a genuine external validation: `peak_w = τ_stall·ω_free/4` is derived from the
linear model, and it lands within 0.5% of the manufacturer's independently published peak-power
figure transcribed in the BOM. It confirms the linear approximation is not wildly wrong.

### 8.3 The sanity checks a human must still do

| Claim | How to falsify it cheaply |
|---|---|
| COF = 1.10 for blue nitrile | Fish scale on carpet with the real robot. **[H]** value, not measured here |
| Battery R = 23 mΩ | Measure sag under a known load. Ages badly |
| Efficiency 0.92 drivetrain / 0.85 elevator / 0.75 arm | All **[S]**. Compare predicted vs measured free speed on the 2026 robot |
| Thermal verdicts | Touch the motor after a match |
| 2026 R103/R408 weight limits | **[H] baseline only.** Re-read the BIOCORE manual 2027-01-09 |
| Systemcore brownout threshold | **UNVERIFIED.** Re-check after 2026-11-12 |

### 8.4 Consistency with the capacity model

Every hours figure in §6.3 is quoted from
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §3.1 (599.1 total; CAD 74.9;
fabrication 129.8; drive practice 54.9; strategy 25.0). Every budget figure is quoted from §8.1
(`robot_discretionary = $2,500`). The §6.3 conclusion — that recovered hours do **not** raise
mechanism count — is derived from §5.2's route A/B/C minimum and §5.5's headcount result, not
asserted here.

### 8.5 What the 2026-08-22 verification pass actually checked

Four checks were run. Two passed clean, one found a factual error, one found a broken link.

| Check | Method | Result |
|---|---|---|
| Every calculator still executes | Ran all five scripts plus **every** subcommand quoted in §0 — `drivetrain.py --sweep`, `elevator_arm.py arm` and `--gas-spring`, `fourbar.py analyze/parallel/synth2`, `cg_tip.py` | **PASS.** All exit 0. §3's pasted output is real output, not illustrative |
| §1 vendor claims | Fetched the vendor/press pages listed in §1.0 | **5 rows corrected**, all moved UNVERIFIED → **[C]** |
| §1.5's cost premise | Autodesk education cloud-credit terms | **FAILED — the claim was wrong.** Corrected in §1.5; the verdict stands on other grounds |
| Internal links resolve | Path-existence check on every relative link in this file and `templates/design-prompts.md` | **1 broken link found and fixed** (`../bom/` → `../../bom/` in the prompts file). All others resolve |

**Reproduce the link check yourself:**

```bash
# Run from the repository root.
cd reference/ai-integration
for f in 02_ai_for_design_and_cad.md templates/design-prompts.md; do
  base=$(dirname "$f")
  grep -o '](\([^)#][^)]*\))' "$f" | sed 's/^](//;s/)$//' | grep -v '^http' | sort -u |
    while read p; do [ -e "$base/$p" ] || echo "MISSING in $f -> $p"; done
done
```

**The honest reading of this table.** A document that has never been re-checked is not a document
that was right the first time — it is a document nobody has tested. One pass over §1 found a wrong
cost claim and a dead link in a file that read as authoritative and internally consistent before the
check. Assume the same is true of the sections not yet re-checked, and of this one after the next
vendor price change. The **[S]** judgements in §1 and §6.3 remain the softest material in the file
and no amount of URL-fetching hardens them.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/ai-integration/02_ai_for_design_and_cad.md` | this document |
| `reference/ai-integration/calculators/motors.py` | **new** — shared FRC motor table (12 motors, evidence-labelled per row) + battery/bus model |
| `reference/ai-integration/calculators/drivetrain.py` | **new** — speed/torque/current/brownout, stator-vs-supply current, gear-ratio sweep |
| `reference/ai-integration/calculators/elevator_arm.py` | **new** — gravity-load motor sizing, holding current, ratchet + gas-spring/constant-force sizing |
| `reference/ai-integration/calculators/fourbar.py` | **new** — four-bar analysis (transmission angle, coupler path, torque), parallelogram sizing, two-position synthesis |
| `reference/ai-integration/calculators/cg_tip.py` | **new** — CG roll-up, weight-limit check, tip-over stowed **and** extended |
| `reference/ai-integration/templates/design-prompts.md` | **new** — 12 prompt templates, each with its failure mode |

**Revision, 2026-08-22 (vendor-verification pass).** All five calculators were re-executed end to
end — including every subcommand in §0 — and all exit 0 with the output shown in §3. The document
changes were confined to §1 and its consequences: **§1.0** (new verification log with URLs), the
§1.1 table (five rows moved UNVERIFIED → **[C]** with real prices), **§1.3** (Onshape licensing
confirmed; CAM Studio and AI Advisor added), **§1.4** (FeatureScript roadmap noted), **§1.5** (a
false cost claim corrected), **§2.6** (free disproof exercise), **§6.5**, Known limitations, and the
Security note. No calculator source and no §3 output was edited.

Nothing marked DONE was modified. [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md),
[`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md), [`../bom/`](../bom/) and
[`../../tools/cycle-model.py`](../../tools/cycle-model.py) were read and cited, not edited.

---

## Known limitations

- **§1's licensing facts are now verified; its *judgements* are still judgements.** The §1.0 table
  lists exactly what was fetched on 2026-08-22 and from where. What that verification establishes
  is narrow: **what these tools cost** (uniformly $0 on education tiers) and **what the vendors say
  they do**. It does not establish that any of them works well for a 15-year-old, because that was
  not measured and cannot be measured from a vendor page. Every "USE IT" / "NO" verdict remains an
  **[S]** engineering judgement about a category.
- **Two §1 rows remain UNVERIFIED and are flagged in place:** the PTC grant programme (secondary
  source only — do not count on that money) and AI Advisor's real usefulness to a novice
  (untested by anyone on this team; §1.3 gives the one-hour November protocol to settle it).
- **Prices were verified once, on one day, and will drift.** Zoo's $0.50/min and Autodesk's
  commercial figures are the most volatile numbers here. The *education* terms are the stable ones
  and are also the only ones you should ever be paying against — which is to say, nothing. §6.5
  puts a dated re-check before the **2026-11-21** BOM order-by date.
- **A cost claim in the previous draft was wrong and is corrected in §1.5.** Generative design was
  rejected partly on cloud-credit cost; education plans carry unlimited credits, so that reason was
  false. The verdict did not change, because the load-bearing reason (manufacturability) was never
  the cost. This is left visible on purpose as a worked example of the failure mode this whole file
  is about: a confident, plausible, unchecked vendor claim surviving into a document because nobody
  opened the page.
- **Four of the twelve motors in `motors.py` are [H], not [C].** CIM, MiniCIM, Falcon 500 and
  775pro carry widely-published motor-curve values that were **not** re-verified in this corpus,
  and Falcon 500 legality for 2027 is **UNVERIFIED**. The eight Kraken/NEO rows come from
  `parts_electronics.yaml` with line numbers.
- **The linear motor model is wrong near stall and wrong when hot.** It is a straight line through
  two endpoints. It is good to roughly ±10% in the 20–70%-of-free-speed band, which is where teams
  operate, and it degrades exactly where the consequences are worst (sustained stall). Every
  thermal verdict in `elevator_arm.py` is **[S]** heuristic, not a manufacturer duty-cycle curve —
  no such curve exists in this corpus.
- **The brownout verdict is necessary, not sufficient.** The bus model is a damped fixed-point
  solve of `V = Voc − I·R`. It does not model transients, and the transient on a direction
  reversal is what actually browns out real robots. A "pass" here does not mean your robot will
  not brown out; a "BROWNOUT RISK" is a much stronger signal than a pass.
- **`R_battery` = 23 mΩ is a single [S] point estimate** and it drives every brownout verdict
  directly. A tired battery can be double that, which would turn several "pass" results into
  failures. Load-test your batteries; the model cannot.
- **`cg_tip.py`'s bare-weight estimate is crude** — it subtracts anything whose name contains
  "bumper" or "battery". It is a smell test, not a weigh-in. Weigh the robot.
- **All weight and geometry limits are 2026 REBUILT [H] baselines.** 2026 R103 (115.0 lb bare) and
  R408 (135.0 lb with BUMPERS) are used because they are the most recent published values. The
  BIOCORE limits are **UNKNOWN** until **2027-01-09** and both the perimeter maximum and BUMPER
  zone height have moved in past seasons.
- **`fourbar.py` is planar, rigid and quasi-static.** No out-of-plane loads, no deflection, no
  friction at the joints, no dynamics. The torque figures are virtual-work results for a vertical
  payload only. A real linkage under a side load behaves worse than this predicts.
- **The gas-spring model treats force as constant over the stroke.** Real gas springs vary
  ~20–40% end to end and are temperature-sensitive; a spring that balances an arm in a warm pit
  will not balance it identically on a cold field. Constant-force springs are closer to the model.
  Neither was priced by this pass.
- **§6.3's savings estimates are [S] and unmeasured.** No dataset of AI-assisted FRC design hours
  exists — the same gap `02_TEAM_CAPACITY_MODEL` §9 hits everywhere. The figures are deliberately
  conservative; the *structural* conclusion (savings land on CAD and strategy, not on fabrication
  or drive practice, and therefore do not raise mechanism count) does not depend on their
  magnitude and is the part to trust.
- **Only some of the prompt templates were end-to-end tested.** See the Known-limitations section
  of [`templates/design-prompts.md`](templates/design-prompts.md). Prompt behaviour is model- and
  version-dependent and will drift; the structure is durable, the wording is not.
- **This file contains no BIOCORE claim, by design.** Every calculator takes the game-dependent
  quantities — game-piece mass, required reach, scoring height, cycle target — as *inputs*. On
  2027-01-09 you supply them and re-run. Nothing here needs rewriting on kickoff day, which is the
  only useful property a pre-kickoff design document can have.

---

## Security note

Sources for this pass were local project files plus, on **2026-08-22**, a small set of **public,
unauthenticated vendor and press pages** fetched read-only to verify §1.0 — Onshape/PTC, Autodesk,
Zoo, build123d, and the FIRST community blog. Every URL is listed in §1.0.

No authentication was used or attempted, nothing was submitted, downloaded, or purchased, and no
account was created. Fetched page content was treated strictly as **data**: claims from it were
recorded with their source and evidence label, and no fetched page was allowed to direct the
content of this file. No page read contained text addressed to an AI assistant or any attempt to
issue instructions; had one, it would have been quoted here rather than acted on.

**A standing caution for anyone extending this file: vendor pages are marketing.** They are the
least reliable class of source in this corpus — they describe roadmap as capability and omit
limits. That is precisely why §1.0 separates *what a vendor states* (**[C]**, with a URL) from
*whether it is any good for you* (**[S]**, this file's judgement). Never collapse those two columns.

The calculator scripts are pure-stdlib Python with no network access, no file writes outside an
explicit `--parts` read, and no subprocess execution.
