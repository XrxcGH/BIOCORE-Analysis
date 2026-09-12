# Elite Design, CAD and Manufacturing — the Method, Sized for 15 Students

**Purpose.** Championship teams do not win because they own better machines; they win because their
**method** converts a game strategy into cut parts with very few wasted iterations. This file is that
method, stripped of the 40-student, 6-mentor assumptions it is usually written under, and re-derived
against the one thing that actually binds here: **75 CAD hours, 130 fabrication hours, one bandsaw,
one drill press, one 3D printer and 3.4 mentor unblock-hours a week**
([`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) §3.1, §5.2 route C, §6.2).

**This file is about METHOD, not parts.** Every SKU, price, URL and mechanism cost lives in
[`../bom/`](../bom/) and is not repeated here:
[`01_DRIVETRAIN.md`](../bom/01_DRIVETRAIN.md) ·
[`02_MANIPULATION_ELEVATION.md`](../bom/02_MANIPULATION_ELEVATION.md) ·
[`03_LAUNCHERS_ELECTRONICS.md`](../bom/03_LAUNCHERS_ELECTRONICS.md) ·
[`06_MECHANISM_CATALOG.md`](../bom/06_MECHANISM_CATALOG.md) ·
[`mechanism_catalog.yaml`](../bom/mechanism_catalog.yaml).
When this document needs a number for a part, it links there. When it needs a number for the *team*,
it links to the capacity model. It invents neither.

**Companion files:**
[`../bom/mechanism_catalog.yaml`](../bom/mechanism_catalog.yaml) — the `tooling_ranks` / `tooling_floor`
vocabulary §5 is built on, and the lead-time and stockout fields §6 is built on ·
[`../ACHIEVABILITY-RUBRIC.md`](../ACHIEVABILITY-RUBRIC.md) §A9 + **gate G1**, which is the scoring
consequence of everything in §5 ·
[`../../tools/cad-linkcheck.sh`](../../tools/cad-linkcheck.sh) — **new this pass**, re-verifies every
URL below.

**Sibling team-ops files (read, not duplicated):**
[`03_programming_stack.md`](03_programming_stack.md) — Systemcore/WPILib 2027, the software half of the
same off-season ·
[`05_business_awards_sustainability.md`](05_business_awards_sustainability.md) — the CAD artefacts that
also serve judging live there.

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus, or a live URL fetched 2026-08-22 |
| **[H]** HISTORICAL-PATTERN | Standard FRC practice observed across prior seasons; not a BIOCORE claim |
| **[S]** SPECULATION | Model assumption or judgement call. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked from here |

**Source shorthand:** `CAP` = [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) ·
`RUB` = [`../ACHIEVABILITY-RUBRIC.md`](../ACHIEVABILITY-RUBRIC.md) ·
`CAT` = [`../bom/06_MECHANISM_CATALOG.md`](../bom/06_MECHANISM_CATALOG.md) + its YAML ·
`PF` = [`../04_PREDICTIVE_FACTORS.md`](../04_PREDICTIVE_FACTORS.md) ·
`PROG` = [`03_programming_stack.md`](03_programming_stack.md) ·
`CAL` = the 2027 season calendar as transcribed in `research/03_biocore_official_intel.md` §2.

> **Scope guard.** BIOCORE presented by Haas is the **FRC** game; kickoff **2027-01-09 12:00 ET**.
> Its scoring element, field and rules are not public as of **2026-08-22**, so **this file contains no
> game-specific design claim**. Everything here is either game-independent (drivetrain, electrical,
> stack-ups, shop capability, sourcing) or a method that survives any game. **Pollen, StarterBots and
> Skill Builders are FTC BIOBUZZ things** and appear nowhere in this document.
> **2027 replaces the roboRIO with Systemcore** — every packaging study in §3.4 that assumes a roboRIO
> footprint is wrong; see `PROG` §0 and re-measure after the **2026-11-12 Pre-Kickoff Virtual Kit
> Release**.

---

## §0. The 60-second workflow

Runnable today, and again on kickoff day. Nothing here needs the game manual.

```bash
# Run from the repository root.

# ---- 1. Are the CAD / vendor / sourcing links in this file still alive? (~15 s) ----
bash tools/cad-linkcheck.sh
#     403/406 = the vendor blocks bots; open it in a browser. 404/000 = fix this document.

# ---- 2. What can this shop actually build? Group the catalog by tooling floor ----
grep -o 'tooling_floor: [a-z_]*' reference/bom/mechanism_catalog.yaml | sort | uniq -c
#     Expect: 3 hand_tools | 13 bandsaw_drillpress | 2 router_cnc | 9 mill_lathe
#     You OWN ranks 1-2. Ranks 3-4 fire RUB gate G1 unless outsourced. That is 11 of 27 mechanisms
#     off the table before the game is even revealed. Read Sec 5 before you argue with it.

# ---- 3. The order-by dates that make Sec 6 real ----
python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown | grep -i "order"
#     The earliest date the tool computes is 2026-11-21 (6-week electrical lead + 1 week margin).
#     That is BEFORE kickoff. See Sec 6.4.

# ---- 4. Re-check that Sec 5's gate is still what the rubric says ----
grep -n "G1 MACHINE" reference/ACHIEVABILITY-RUBRIC.md

# ---- 5. The hours this document is denominated in ----
python tools/capacity_model.py | grep -E "CAD|Fabrication|BINDING"
```

**Read the output in this order:** step 2 first (it tells you which half of the mechanism catalog you
may not design), then step 3 (it tells you that your first purchasing deadline is in **November**,
not January), then step 5 (it tells you that CAD is 75 hours, so the design method must be cheap).

---

## §1. CAD platform, decided

### 1.1 The four candidates, scored on what matters to a 15-student team

| Criterion (weight) | **Onshape** | SolidWorks | Fusion | Inventor |
|---|---|---|---|---|
| Cost to this team | **$0** — the **Educator Plan**, with a FIRST-specific programme page and documented onboarding **[C]** (§1.3, four pages verified live 2026-08-22) | $0 *if* the FIRST sponsorship offer is granted — **UNVERIFIED**, see 1.3 | $0 education licence — **UNVERIFIED** (Autodesk pages returned 403 to an automated check) | same as Fusion — **UNVERIFIED** |
| Runs on | any browser, incl. Chromebooks and school-locked laptops | **Windows only**, heavy install, admin rights | Windows/Mac install + cloud account | **Windows only**, heaviest install |
| Two students editing the same assembly | **Yes, natively, live** | No (needs PDM) | Partial | No |
| Built-in versioning / branching | **Yes — versions, branches, merges, full history [H]** | File copies, or paid PDM | Cloud version history | Vault (separate product) |
| Recovering "who broke the arm mount on Tuesday" | one click, always | archaeology | possible | archaeology |
| FRC part libraries | **Deepest** — Onshape App Store add-ins + vendor-published Onshape documents [H] | STEP imports only | STEP imports only | STEP imports only |
| CAM for a router (if you ever buy one) | **CAM Studio — free to FIRST teams on the Educator Plan [C]**, requested through the FIRST Mentor Dashboard (§1.3) | HSMWorks/CAMWorks | **Best-in-class integrated CAM** | via Fusion |
| Simulation / FEA | weakest of the four | strongest | good | good |
| Y1 student to first useful part | **fastest [S]** — no install, no file management, no crash-loss | slow | medium | slow |
| Works when the school Wi-Fi dies | **No — hard dependency on the network** | Yes | partly | Yes |

### 1.2 The recommendation, without hedging

**Use Onshape for the whole robot. Run exactly one CAD system.** [S] — but the reasoning is not
close:

1. **The binding constraint is mentor attention, not modelling power** (`CAP` §7.1 ranks mentor
   unblock time #1 at 3.4 h/wk). Every hour a mentor spends on "my file won't open", "I lost my work",
   "which version is current" is taken directly out of the 204 minutes a week that unblock actual
   design decisions. Onshape's cloud model deletes that entire category of question.
2. **Simultaneous editing is worth more than FEA at this scale.** With 2 CAD-capable core students
   (`CAP` §4.2 slots 1 and 3) and 205 h in the whole mechanism pool, serialising CAD behind one
   licence-holder is a throughput loss you cannot afford. Nobody on a 15-student team runs a
   meaningful FEA study; everybody needs two people in the drivetrain assembly on a Tuesday.
3. **Branch/merge is the only realistic design-review enforcement mechanism** you have (§4.4).
4. **Chromebook and locked-laptop compatibility** is the difference between 4 students who can CAD at
   home and 1.
5. **The FRC part-library ecosystem is Onshape-first** [H]. Copying a library part costs minutes;
   modelling a MAXPlanetary from a drawing costs an evening you budgeted for the mechanism.

**The one legitimate exception, now much narrower.** Onshape provides **CAM Studio to FIRST teams on
the Educator Plan** (**[C]** — https://www.onshape.com/en/education/cam-for-first, HTTP 200 on
2026-08-22; requested through the FIRST Mentor Dashboard). So if the team ever acquires a hobby CNC
router (§5.6), **try CAM Studio first** — it keeps design and toolpath in one system and costs nothing.
Reach for Fusion **as a CAM front-end only** if CAM Studio has no post-processor for your specific
controller (**UNVERIFIED** — the page names no machines or post-processors, so confirm against your
actual machine before planning around it). Even then: design in Onshape, export STEP/DXF, toolpath in
Fusion. Do not let the CAM tail wag the design dog — a second *design* environment doubles your library
maintenance and halves your review discipline.

**The anti-recommendation:** do not run SolidWorks and Onshape simultaneously "so students learn
industry tools." That is a real argument in a 40-student programme with a dedicated CAD mentor. Here it
costs you a full workstream's worth of coordination (`CAP` §5.1 criteria 1 and 4) to buy a line on a
résumé. Teach the *concepts* — they transfer; the button locations do not matter.

### 1.3 Getting the licences — do this in September, not January

**This is the FIRST-specific path, and it is confirmed.** Onshape runs a dedicated FIRST Robotics
programme page and a documented team-onboarding procedure; the plan a FIRST team wants is called the
**Onshape Educator Plan**, and it is free.

| Page | URL | Status 2026-08-22 |
|---|---|---|
| **Onshape for FIRST Robotics** — the programme landing page, start here | https://www.onshape.com/en/education/first-robotics | **[C]** 200 |
| **Education sign-up** — where accounts are actually created | https://www.onshape.com/en/education/sign-up | **[C]** 200 |
| **Team-onboarding how-to** — the step list below is taken from this page | https://www.onshape.com/en/blog/how-to-onboard-your-first-robotics-team | **[C]** 200 |
| **CAM Studio for FIRST** — requested via the FIRST Mentor Dashboard | https://www.onshape.com/en/education/cam-for-first | **[C]** 200 |
| **PTC Education for FIRST** — the wider PTC offer (Creo, Mathcad, Onshape; grants for some teams) | https://www.ptc.com/en/education/first | **[C]** 200 (page live; **its specific terms were not read** — open it before quoting them) |

**The procedure, in order** (**[C]** from the onboarding page above, except where marked):

| Step | Action | Why it matters here |
|---:|---|---|
| 1 | **Create a shared team email first** (e.g. `cad@yourteam.org`). Recommended, not required | The classroom is owned by whoever signs up. A shared address is how you stop the account belonging to a senior who graduates |
| 2 | **A mentor signs up for the Educator Plan** using that shared email | Mentors sign up as *educators*; this is the account that gets admin rights |
| 3 | **Name the classroom after the team** | The classroom is the team's shared workspace |
| 4 | **Every student creates their own individual account** via the education sign-up page and joins the classroom as a member | Individual accounts are the point — simultaneous editing (§1.2) needs one identity per student |
| 5 | **Give mentors admin, students member permissions** | Admin is who can recover a deleted document at 11 p.m. |
| 6 | **Have the CLASSROOM own every document, not an individual** | **[C]** the onboarding page recommends exactly this. It is also the single most common CAD-continuity failure on small teams **[S]** — a graduating senior's personal account taking the robot with them |
| 7 | Request **CAM Studio** through the FIRST Mentor Dashboard **if** you own or plan to own a router (§5.6) | Free with the Educator Plan **[C]**; skip it otherwise |
| 8 | Put a licence-review date in the team calendar | **[S]** — renewal/expiry terms are **not stated** on any page read here. Check yearly rather than assume perpetuity |

> **Do this in September (§7.3), not in January.** Fifteen account creations, a classroom, permissions
> and a first lesson is one evening in the fall and is a lost meeting in build season.

**Still UNVERIFIED — do not state these as fact to a student or a sponsor:**

| Claim | Status |
|---|---|
| `FIRST@ptc.com` as the contact address for bulk team access | **UNVERIFIED** — it appears in web search summaries of PTC/Onshape material but was **not** read off a page during this pass. Confirm on the PTC page before emailing a list of student addresses |
| Whether Educator-Plan documents default to **private** | **UNVERIFIED** — none of the four pages fetched addressed document privacy. The free *public/hobbyist* tier historically makes documents world-readable **[H]**. **Check the visibility of your first document by hand**, then make it a §4.3 checklist line |
| Onshape grants for FIRST teams (financial, not licences) | **UNVERIFIED** — referenced in search results; terms not read |
| A **SolidWorks**-for-FIRST sponsorship offer | **UNVERIFIED** — a guessed sponsorship URL returned 404 on 2026-08-22 |
| **Autodesk** (Fusion / Inventor) education terms | **UNVERIFIED** — Autodesk pages returned 403 to an automated check, which is a bot block and **not** evidence the offer does not exist. Open it in a browser |

### 1.4 The 2027 wrinkle: Systemcore has no CAD in your library yet

`PROG` §0 documents the control-system reset. Its CAD consequence is concrete and dated:

| Item | Status 2026-08-22 | What to do |
|---|---|---|
| Systemcore physical envelope, hole pattern, connector faces | **UNVERIFIED** — no dimensioned model in this corpus | Reserve a **generous placeholder volume** in the packaging study (§3.4) and mark it `PLACEHOLDER-SYSTEMCORE` in CAD |
| Vendor-published Systemcore CAD | **UNVERIFIED** | Re-check after **2026-11-12** (Pre-Kickoff Virtual Kit Release, `CAL`) |
| roboRIO legality in 2027 | **UNVERIFIED** (`CAP` §3.2) | Do **not** design a mount that only fits a roboRIO |

**[S]** The cheapest insurance is an electronics board designed as a **flat plate with a 0.5 in hole
grid** (§3.6) rather than a plate with bespoke pockets: any controller footprint bolts to a grid.

---

## §2. Part libraries, reuse and workspace organisation

### 2.1 The rule that saves the most hours

> **Never model a part you can buy, and never model a bought part twice.**

`CAP` gives you **75 CAD hours** for the whole season. A 15-student team that models its own gearbox
internals has spent an entire mechanism's design budget drawing something that arrives in a box.

| Reuse tier | What it is | Design-hour cost | Use it for |
|---|---|---:|---|
| **T-A** Vendor-published CAD | The vendor's own Onshape document or STEP | ~0 | Every COTS part on the robot |
| **T-B** Community library part | Onshape App Store FRC add-in content | ~0 | Hardware, bearings, belts, gears, tube stock |
| **T-C** Your own released library | Parts your team standardised in a prior season | ~0 | Bumper brackets, battery mount, electronics board |
| **T-D** Simplified envelope model | A box/cylinder with the right mounting holes and mass | 0.2–0.5 h | A COTS part with no published CAD, or a 400 MB import that makes the assembly unusable |
| **T-E** Full custom model | You draw every feature | 1–8 h | Only parts you will actually fabricate |

**[S]** A disciplined team spends ≥70% of its CAD hours in T-E on **fabricated parts only**, and the
rest at T-A/T-B. Any hour spent at T-E on a purchasable part is a direct transfer out of the mechanism
budget.

### 2.2 Where the libraries actually are

| Source | What you get | Status 2026-08-22 |
|---|---|---|
| **Onshape App Store** — https://appstore.onshape.com/ (also reachable at https://cad.onshape.com/appstore) | The add-in marketplace. **Both FRC part libraries below are installed from here** — subscribe, "Get for Free", and the app appears in your account | **[C]** both live (200) |
| **MKCad** — the long-standing FRC COTS library | Bearings, fasteners, gears, pulleys, sprockets, hubs, shaft collars, spacers, wheels, motors, sensors, COTS gearboxes, simplified + full electronics. Ships **FeatureScripts** as well as parts — chain-path, shaft, hole-patterned-tube and planetary generators, which are the real time-saver | **[H]** — install via the **Onshape App Store**, not via a web domain. Introduction thread: https://www.chiefdelphi.com/t/pic-introducing-mkcad-the-onshape-frc-parts-library/161295 (**[C]** 200). Originally released by **FRC 1836** per community sources — attribution **UNVERIFIED** from a primary page. **`mkcad.com` is a parked domain-sale page as of 2026-08-22 — do not use it, and confirm the publisher before installing** |
| **FRCDesignLib / FRCDesignApp** — the library `frcdesign.org`'s course now standardises on | An alternative COTS component collection with its own inserter app. Worth knowing about because the widely-used **FRCDesign.org** training course teaches against it, so a student who learns CAD there arrives expecting it | **[C]** — https://frcdesign.org/ live (200); its setup page instructs: find **FRCDesignApp** in the Onshape App Store → *Subscribe* → *Get for Free* → it is added to the account automatically |
| **REV Robotics** — https://www.revrobotics.com/ | Per-product CAD downloads on each product page | **[C]** site live; a guessed `/cad/` index 404'd — go via the product page |
| **WCP** — https://www.wcproducts.com/ and **https://docs.wcproducts.com/** | Product CAD + the documentation site that carries ratio tables and drawings | **[C]** both live |
| **AndyMark** — https://andymark.com/ | Per-product CAD; a guessed `/pages/cad` index 404'd | **[C]** site live |
| **The Thrifty Bot** — https://www.thethriftybot.com/ | Per-product CAD | **[C]** site live |
| **Swerve Drive Specialties** — https://www.swervedrivespecialties.com/ | Module CAD — the one import you absolutely must not redraw | **[C]** site live |
| **CTR Electronics** — https://store.ctr-electronics.com/ | Motor/controller/sensor CAD | **[C]** site live |
| **VEXpro** | Gears, shafts, VersaFrame-family structure [H] | **UNVERIFIED** — `vexrobotics.com/vexpro` returned 403 to the automated checker (bot block, not proof of absence). Open in a browser |
| **Chief Delphi** — https://www.chiefdelphi.com/ | Open-sourced full-robot CAD threads; the highest-value free design education available | **[C]** live |

**Pick ONE library and make it a team standard [S].** Either is fine; running both is not. Two
libraries means two versions of "a 1/2 in hex bearing" in the same assembly, two sets of FeatureScripts
students half-know, and a mass-properties study that silently double-counts. Decide in September (§7.3),
write the choice in `90_TEAM_LIBRARY`, and teach only that one. If any of your students learn CAD from
the FRCDesign.org course, that is a real argument for standardising on the library it teaches.

Per-SKU prices and availability for all of the above are in [`../bom/`](../bom/) — **do not re-derive
them here**, and run [`../bom/recheck_prices.sh`](../bom/recheck_prices.sh) before any purchase order.

### 2.3 Import hygiene (the thing that kills small-team assemblies)

| Problem | Symptom | Fix |
|---|---|---|
| Full-detail vendor STEP of a swerve module ×4 | Assembly takes 40 s to open; students stop opening it | Import once, **derive a simplified envelope** (T-D), keep the detailed one in a reference document |
| Imported parts have no material | Weight study reads 0 lb; you discover the robot is overweight in week 5 | **Assign material to every imported part on import.** Make it a review-checklist line (§4.3) |
| Fastener explosion | 400 screws in the tree, nobody can find the arm | Model fasteners **only where clearance matters**; otherwise leave holes and put the count in the BOM |
| Vendor updates CAD mid-season | Two students' parts don't match | Pin the version. Onshape linked documents reference a **specific version**, not "latest" — use that deliberately |

### 2.4 Workspace organisation — one structure, copied verbatim

**[S]** This layout is a recommendation, not a standard. Its virtue is that it maps 1:1 onto the three
workstreams `CAP` §5.3 says you get, so a document owner and a workstream lead are always the same
person.

```
FRC-2027-BIOCORE  (Onshape team)
├── 00_MASTER_LAYOUT        <- master sketch, field/rule envelopes, game-piece stand-in.  Owner: CAD lead
├── 10_DRIVETRAIN           <- frame, bumpers, modules, belly pan.                        Owner: Core tech B
├── 20_MECHANISM_A          <- the primary scoring mechanism.                             Owner: Core tech A
├── 30_ELECTRONICS_BOARD    <- board, Systemcore placeholder, PDH, battery, air.          Owner: Veteran F
├── 40_ROBOT_ASSEMBLY       <- links the above; nobody models parts here.                 Owner: CAD lead
├── 90_TEAM_LIBRARY         <- your released standard parts (brackets, mounts, grid plate)
└── 99_SANDBOX              <- prototypes, dead ends, student practice. Never referenced by 40_
```

Owner names are the roster slots in `CAP` §4.2. **Every document has exactly one owner**; that person
is who a mentor talks to in the 45–60 minute unblock window (`CAP` §6.3).

### 2.5 Versioning and release branches — the minimum viable discipline

| Concept | Onshape mechanism | Team rule |
|---|---|---|
| "Today's work" | the **main workspace** | Main is always assemble-able. If it is broken at the end of a meeting, it gets fixed or reverted before anyone leaves |
| "I'm trying something risky" | a **branch** | Any change that could break the robot assembly starts on a branch named `initials-what` (e.g. `jd-intake-v2`) |
| "This is good, merge it" | **merge to main**, at a design review | Merges happen **at reviews**, not at 11 p.m. (§4) |
| "This is what we are cutting" | a named **Version**: `REL-<subsystem>-<n>` | **Nothing is fabricated from a workspace. Ever. Only from a named Version** |
| "This is what we ordered" | the Version referenced in the BOM row | The BOM (`bom-builder.py` input) cites the Version name |
| "What changed since we cut v1?" | Onshape compare between Versions | Run it before re-cutting anything |

**The one rule that matters:** *the cut list and the CAD Version have the same name, and that name is
written on the part in Sharpie.* [S] It costs nothing and it ends the single most expensive shop
argument — "is this the new bracket or the old one?" — which on a one-bandsaw team (`CAP` §5.2 route C)
costs queue time you cannot recover.

---

## §3. Design methodology — layout first, and what standardisation actually buys

### 3.1 The order elite teams work in, and why each step exists

| # | Step | Output | Skipping it costs |
|---:|---|---|---|
| 1 | **Strategy → required actions** | A list of physical actions with a cycle-time target | You design a mechanism for a scoring path that isn't worth points ([`../../STRATEGY-RANKING-SYSTEM.md`](../../STRATEGY-RANKING-SYSTEM.md)) |
| 2 | **Prototype the uncertain physics, in cardboard and scrap** | A working rough intake/launcher geometry, measured | Weeks. The #1 small-team failure is CADing a mechanism whose physics was never tested |
| 3 | **Master layout sketch** | One sketch: frame perimeter, height limit, game-piece path, mechanism envelopes | Every downstream part is dimensioned against nothing |
| 4 | **Packaging study** | Reserved volumes for battery, control system, air, wiring, bumper zone | The classic: the mechanism fits, the battery does not |
| 5 | **Top-down subassembly design** | Each subsystem derives its interface from the layout | Two students design to two different frame widths |
| 6 | **Detail + DFM pass** | Every fabricated part reduced to your shop's capability (§5) | Gate G1 fires in the shop instead of on paper |
| 7 | **Release + cut list + BOM** | Named Version, cut list, order | Parts get cut twice |

**Step 2 is not optional and it is not CAD.** `PF` and `CAT` both price the failure mode: a mechanism
whose *geometry* is wrong is discovered in fabrication, at 3–5× the cost of discovering it in cardboard.
Budget prototype hours out of the fabrication line, not the CAD line.

### 3.2 The master sketch — what actually goes in it

A single Part Studio, one sketch, driven by named variables. **[H]** The pattern is universal among
teams that publish their CAD.

| Layer | Contents | Source of truth |
|---|---|---|
| **Rule envelope** | Frame perimeter, max height, max extension, bumper zone | **The 2027 manual, on kickoff day.** Every one of these numbers is **UNVERIFIED for BIOCORE** until 2027-01-09. Put them in as *variables* so they can be changed in one place |
| **Field geometry** | Only the features you interact with: goal height, feed station height, ramp angle | Manual + field drawings |
| **Game piece** | A stand-in solid with the published dimensions | **BIOCORE's element geometry is not public**; use a parameter block and fill it in on kickoff day |
| **Robot skeleton** | Frame rectangle, wheel centres, CG target, mechanism pivot points | You |
| **Cycle path** | The line the game piece travels from intake to scored | You. This is the sketch that catches "the indexer and the elevator want the same 4 inches" |

**Variables, not numbers.** `#frameWidth`, `#bumperZoneBottom`, `#pieceDia`. On the Saturday of Week 3
when a Team Update changes a dimension ([`../RULE-CHURN-WATCHLIST.md`](../RULE-CHURN-WATCHLIST.md)),
you change one variable instead of re-drawing a robot.

### 3.3 Top-down and design-in-context, with the trap named

**Top-down:** subassemblies derive their mounting interfaces *from* the master layout, so a change
propagates. **In-context:** you model a part while seeing the assembly around it.

**The trap [H]:** in-context references go **stale**. Onshape freezes a context at the moment you
create it; the part keeps referencing the old positions until you deliberately update the context.
Students discover this when a bracket that "fits in CAD" doesn't fit the robot.

| Rule | Why |
|---|---|
| Create contexts **deliberately and rarely**; name them | An unnamed context nobody remembers is a landmine |
| Never in-context off a part that is still being designed | Chained staleness |
| Prefer **mate connectors + variables** over in-context geometry for interfaces | Explicit, inspectable, survives change |
| Before release, **update every context and re-check** | Add to the §4.3 checklist |

### 3.4 The packaging study — reserve volumes before you design mechanisms

**[H]** Every one of these must exist somewhere on the robot, and none of them shrink to fit later:

| Volume to reserve | Note for 2027 |
|---|---|
| Battery + retention | Heavy, low, accessible **without removing a mechanism** |
| **Control system board** | **Systemcore footprint UNVERIFIED** — reserve generously; see §1.4 and `PROG` §0 |
| Power distribution + main breaker + bus | Breaker must be reachable by a field-fault official |
| Radio / comms | Placement affects field connectivity |
| Pneumatics (if used) | Compressor + tanks are bulky and heavy; see `CAT` `pneumatics_package` |
| Wire runs and service access | The volume nobody reserves and everybody needs |
| Bumper zone | Non-negotiable, rule-defined, **2027 dimensions UNVERIFIED** |
| Mechanism swept volumes | Where an arm/elevator goes *while moving*, not just at rest |

**The 20-minute exercise that prevents a rebuild [S]:** before any mechanism is detailed, place these
as coloured boxes in the assembly. If the boxes already collide, the mechanism concept is wrong and you
have learned it for 20 minutes instead of 20 hours.

### 3.5 Standard stack-ups — the small-team superpower

**[H]** These are the de-facto FRC standards. Adopting them means a shaft, a bearing, a spacer and a
pulley from three different vendors fit together without a design decision.

| Interface | Standard | Consequence if you standardise |
|---|---|---|
| Rotating shaft | **1/2 in hex** (thin-wall 3/8 in hex for light duty) | One shaft stock, one broach size, one bearing |
| Bearings | **1/2 in hex bore, 1.125 in OD flanged** | Every plate uses the **same 1.125 in hole** — one hole saw / one bore |
| Structure | **1×1 and 2×1, 0.100 in wall 6061 tube** | One saw setup, one drill size family |
| Plate | **1/8 in and 1/4 in 6061; 1/8 in and 1/4 in polycarbonate** | Two stock thicknesses cover the robot |
| Fasteners | **#10-32** primary, **1/4-20** for structure/gearbox, 8-32 for light brackets | Two hex drivers live in the pit, not nine |
| Hole for #10-32 clearance | **#10 clearance (~0.196 in) / 13/64 in** | One drill bit for 80% of holes |
| Belts | **HTD 5 mm pitch**, 9 mm and 15 mm widths | Two belt widths; pulleys interchange |
| Chain | **#25** (light) / **#35** (drivetrain, high load) | Two chain breakers, two master-link stocks |
| Gears | **20 DP** spur (or vendor planetary systems) | Centre distances are arithmetic, not lookup |
| Retention | Shaft collars + retaining rings on hex | No custom shoulders → no lathe (§5) |

**The payoff is not elegance; it is queue time.** `CAP` §5.2 **route C** proves the single-machine
fabrication queue caps the robot at 2 novel mechanisms *regardless of headcount*. Standardisation is
the only lever that attacks route C without money: fewer distinct drill sizes, fewer saw setups,
fewer "wait, what bearing does this take" trips to the parts bin.

| Standardisation act | What it saves **[S]** |
|---|---:|
| One bearing size across the robot | ~4–6 fab h + one stockout risk removed |
| One tube size for all structure | ~3–5 fab h (single saw setup, batch cutting) |
| One primary fastener size | ~2 h + the pit-day version of it |
| A released, reused electronics board design | ~6–10 h and a whole category of wiring rework |
| **Total, plausibly** | **~15–25 fab h of 130** — 12–19% of the fabrication budget, for zero dollars |

### 3.6 The 0.5 in hole grid — what it is and what it actually buys

**[H]** A repeating pattern of holes on a **0.500 in pitch** along tube faces and across plates. The
COTS tube ecosystem is built around it (product names such as **VersaFrame**, **MAXTube**,
**ThriftyTube** — **product pages UNVERIFIED on 2026-08-22** per [`../bom/01_DRIVETRAIN.md`](../bom/01_DRIVETRAIN.md)
§ and [`../bom/02_MANIPULATION_ELEVATION.md`](../bom/02_MANIPULATION_ELEVATION.md) §; the *pattern* is
standard practice regardless of which vendor's stock you buy).

| Buys you | Detail |
|---|---|
| **Adjustability without re-fabrication** | Move a bracket 0.5 in without drilling. On a team that will get the mechanism geometry wrong once, this is the cheapest iteration mechanism in existence |
| **Cross-vendor mounting** | Gearboxes, bearing blocks and brackets are designed to it |
| **A CAD pattern instead of a dimensioning exercise** | One linear pattern replaces 30 dimensions |
| **Layout arithmetic in whole numbers** | Centre distances become "7 holes", not 3.4375 in |
| **A drill-press jig, not a mill** | Grid holes can be produced accurately with a fence, a stop block and a printed template (§5.3) |

| Costs you | Detail |
|---|---|
| Strength | A gridded tube is weaker than a solid one. Do not grid a highly loaded member's tension face without thought |
| Weight-optimisation ceiling | You are not building the lightest possible robot. **You are not trying to** |
| Drill time if self-made | ~40–80 holes per tube by hand. Buy pre-gridded stock where budget allows, or grid only where brackets actually land **[S]** |

**Small-team verdict [S]:** grid the **structure you expect to adjust** (mechanism mounts, electronics
board, bumper brackets); do not grid the drivetrain rails you will never move. The 0.5 in grid is
adjustability insurance, and adjustability is worth more than mass to a team whose first geometry
guess will be wrong.

### 3.7 Tube-and-plate vs plate-and-standoff

| | **Tube and plate** | **Plate and standoff** |
|---|---|---|
| What it is | 1×1/2×1 tube skeleton, gussets and plates at joints | Two parallel plates held apart by standoffs; mechanism lives between |
| Tooling floor | **`bandsaw_drillpress`** (rank 2 — you own it) | **`router_cnc`** (rank 3) in practice: the plates carry all the geometry |
| Where the accuracy lives | In hole positions on a few faces | In the **profile** of the plate — needs a router/waterjet to be accurate |
| Iteration cost | Cut a new tube: ~20 min | Re-cut a plate: an outsourced order + 1–2 weeks |
| Stiffness per pound | Good in bending along the tube | Excellent for a compact mechanism, poor as a long member |
| Best for | Frames, arms, elevators, anything long | Gearbox-adjacent clusters, intakes, compact wrists |
| **This team** | **Default.** It matches the shop you own and the rubric's A9=4 anchor | Use **only** where a single plate pair does the whole job and you can outsource it (≤2 parts — the exact G1 exception, `RUB` §5) |

**[S]** The honest version: plate-and-standoff is how the top 5% build, because they own waterjets. The
same design at rank 2 becomes tube-and-plate with drilled brackets — heavier, uglier, and it plays the
same match.

---

## §4. Design reviews — the highest-leverage 60 minutes of the week

### 4.1 Why a small team needs *more* review discipline than a big one, not less

`CAP` §5.4: a 3-link mechanism at 90% reliability each is **72.9%** reliable, and `PF` weights
reliability at **88**. A big team recovers from a bad design decision by throwing 20 students at a
re-build. You cannot: `CAP` §3.3 shows the plan closes with **exactly zero slack**. Review is not
bureaucracy; it is the only error-detection stage you can afford, because the next one is fabrication.

### 4.2 Three gates, three different meetings

| Gate | When | Duration | Who **must** be there | Decision |
|---|---|---:|---|---|
| **G0 — Concept** | Before CAD starts on a mechanism | 30 min | Mentor, mechanism lead, CAD lead, drive coach, one programmer | Is this the right mechanism *at all*? Prototype evidence required |
| **G1 — Detail / pre-fab** | Before any part is cut | 45 min | Mentor, mechanism lead, whoever will cut it, electrical lead | Is it manufacturable **here** (§5), does it fit (§3.4), can it be assembled? |
| **G2 — Release / pre-order** | Before the PO | 20 min | Mentor, mechanism lead, whoever holds the budget | Named Version, cut list, BOM, lead times (§6) |

**Total: ~1.6 mentor-hours per mechanism per pass.** Against 3.4 unblock h/wk (`CAP` §6.2) that is
affordable for **2 mechanisms plus drivetrain** — the same number `CAP` derives four different ways —
and it is *not* affordable for four. **The review budget is itself a proof of the workstream cap.**

### 4.3 The checklist — copy this into a pinned document

```
G1 DETAIL REVIEW CHECKLIST  (mechanism: ______   Version: REL-____-__   date: ____)

FIT & PACKAGE
[ ] Fits the rule envelope with margin, in every position, including while moving
[ ] Does not collide with reserved volumes (battery / control system / air / wiring)
[ ] Bumper zone respected; bumpers still removable
[ ] Every in-context reference updated; no stale contexts
[ ] Weight study run: every part has a MATERIAL assigned; total is on the whiteboard

MANUFACTURABILITY  (Sec 5 -- the gate)
[ ] Every fabricated part named its machine: hand / bandsaw+drill / 3D print / OUTSOURCED
[ ] ZERO parts require a mill, lathe or in-house CNC   <-- if not, redesign, do not "find a way"
[ ] Router/waterjet parts: count <= 2 AND ordered >= 2 weeks before needed  (RUB gate G1 exception)
[ ] Every hole is a size we own a drill/reamer for
[ ] Every part can be held safely while being cut  (no tiny parts on the bandsaw)
[ ] Tolerances: nothing tighter than +/-0.010 in on a drill-press feature

ASSEMBLY & SERVICE
[ ] Every fastener can be reached with a tool we own, with the robot assembled
[ ] Bearings/shafts can be removed without disassembling an unrelated subsystem
[ ] The failure part we expect to break is replaceable in < 6 min in a pit
[ ] Wire/pneumatic routing exists in CAD, not "we'll figure it out"

INTERFACES
[ ] Motor, gearbox, sensor and controller are the SPECIFIC parts in the BOM (SKU, not "a NEO")
[ ] Sensor mounting exists for every sensor the software plan needs  (PROG)
[ ] Hard stops exist mechanically; software limits are not the only limit
[ ] Standard stack-up used (Sec 3.5); any deviation is written down with a reason

PROCESS
[ ] Cut list generated from the named Version; quantities include 1 spare of anything fragile
[ ] Lead times checked against the build calendar (Sec 6); long-lead items already ordered
[ ] Someone other than the designer has read this drawing and can explain it back
```

### 4.4 How elite teams actually run the meeting — and the small-team adaptation

| Elite practice [H] | Why it works | **This team's version** |
|---|---|---|
| Design presented by the *student*, not the mentor | The reviewer must be able to attack the design without attacking the person | Same. Non-negotiable |
| Screen shows CAD; someone drives, nobody crowds | Keeps it to 45 min | Same |
| Written checklist read aloud | Prevents the loudest concern crowding out the boring fatal one | §4.3 |
| Reviewers assigned roles: manufacturability / integration / serviceability | Each reviewer owns a lens | With 5 core students: **mentor = manufacturability**, CAD lead = integration, whoever will cut it = serviceability |
| Decisions written down, with owner and date | "We discussed that" is not a decision | One line per decision in the meeting doc |
| **Merge to main happens at the review** | The review has teeth | The single enforcement mechanism you have (§2.5) |
| Separate "red team" review before comp | Adversarial pass | Fold into G1; you do not have the bodies for a second panel |

### 4.5 What gets rejected — the list, stated in advance so it isn't personal

**[S]/[H]** A design is sent back, not negotiated, when:

1. It needs a machine the team does not own and cannot outsource in time (**`RUB` gate G1**).
2. It is workstream #4 (**gate G2**) — `CAP` §5.3.
3. It costs more than the remaining discretionary budget (**gate G3**, $2,500 total).
4. Its hours push the mechanism pool past 205 h (**gate G4**).
5. **No prototype evidence exists** that the physics works.
6. A single failure disables scoring entirely and there is no manual/driver fallback.
7. It cannot be serviced in a pit between matches.
8. It requires a tolerance the shop cannot hold (**±0.010 in on a drill press is optimistic**).
9. It adds a mechanism whose function overlaps an existing one (two things that both move the piece
   vertically).
10. The designer cannot state the cycle-time benefit in seconds.

**The healthy norm to establish in the off-season, before it costs anything:** *rejection at G0 is a
success — it is the cheapest possible place to be wrong.*

---

## §5. DFM by shop capability — design choice → required capability

> **This section is the design-side twin of `RUB` §A9 + gate G1 and of the `tooling_floor` field in
> [`../bom/mechanism_catalog.yaml`](../bom/mechanism_catalog.yaml). The category names below are
> exactly the catalog's `tooling_ranks` — do not invent new ones, because `bom-builder.py` and
> `score-strategy.py` both read them.**

### 5.1 The capability ladder (verbatim vocabulary from `mechanism_catalog.yaml`)

| Rank | `tooling_floor` | Machines | Owned by this team? | `RUB` A9 score | Gate |
|---:|---|---|:---:|:---:|---|
| 1 | `hand_tools` | Hand tools, hardware-store stock, **3D printer** | **Yes** | **5** | — |
| 2 | `bandsaw_drillpress` | Bandsaw + drill press on tube/plate | **Yes (one of each)** | **4** | — (queue contention only) |
| 3 | `router_cnc` | Hobby CNC router / waterjet / laser — 2D profiles | **No** | **2** | **G1 fires** unless `outsourced_2d_account: true` **and** ≤2 parts **and** ≥2 weeks' lead |
| 4 | `mill_lathe` | Manual or CNC mill, lathe — 3D features, bores, turned shoulders | **No** | **0** | **G1 fires**. Not outsourceable at $2,500 |
| 5 | `outsourced` | Sponsor waterjet/laser, SendCutSend, Xometry | **Account, not a machine** | treated as 2 | see rank 3 |

**The arithmetic that should govern January.** Of the 27 mechanisms in `CAT`:

| `tooling_floor` | Count | Status for this team |
|---|---:|---|
| `hand_tools` | **3** | Build freely |
| `bandsaw_drillpress` | **13** | Build freely (queue-limited to ~2 concurrent) |
| `router_cnc` | **2** | Only via an outsourced account, ≤2 parts, ≥2 weeks |
| `mill_lathe` | **9** | **Gated. Off the table as specified.** |

**11 of 27 catalogued mechanisms are gated before the game is revealed.** That is not pessimism; it is
the thing that makes kickoff-day triage fast (`KICKOFF_PLAYBOOK.md` Phase 3).

### 5.2 The mapping table — design choice → required capability

**[H]** for the machine mappings (standard shop practice); **[S]** for the small-team workaround column.

| Design choice | Required capability | Rank | Workaround that drops it a rank |
|---|---|:--:|---|
| Cut tube to length, square | Bandsaw (or hacksaw + jig) | 2 | Vendor pre-cut stock, or a chop saw with a non-ferrous blade |
| Holes in tube faces, ±0.010 in | Drill press + fence/stop | 2 | Printed template taped to the tube + centre punch |
| **0.5 in grid on tube** | Drill press + indexing stop | 2 | **Buy pre-gridded tube stock** — the single best money-for-hours trade you can make |
| Plate with a complex outline | Router / waterjet / laser | **3** | Redraw as a **rectangle with drilled holes**; let the tube skeleton carry the geometry |
| Pocketed / lightened plate | Router or mill | **3–4** | **Do not lighten.** You are not weight-limited at this scale; you are hour-limited |
| Precise bore for a bearing (1.125 in) | Mill, or hole saw + reamer, or router | **3–4** | **Bearing blocks** — a COTS bolt-on block turns a bore into 4 drilled holes. Rank 4 → rank 2 |
| Turned shaft with shoulders | Lathe | **4** | **Hex shaft + shaft collars + retaining rings.** Rank 4 → rank 1 |
| Custom gear or sprocket | Mill/CNC + hobbing | **4** | Buy it. Always. There is no exception |
| Gearbox plates | Router/mill | **3–4** | Buy a COTS planetary/gearbox system |
| Custom swerve module | Full CNC shop | **4** | **Buy modules.** `CAT` `swerve_drivetrain` is rank 2 *because* the modules are bought |
| Welded frame | Welder + fixture table | 3-equivalent | **Bolted gussets.** Serviceable, repairable at an event, no fixture |
| Structural 3D-printed bracket | 3D printer | **1** | — (this is already the floor) |
| Compliant intake wheel/roller | COTS compliant wheels on hex | 1–2 | — |
| Sheet-metal bent bracket | Brake / outsourced bend | 3 | Two flat parts bolted at 90°, or a printed part |
| Polycarbonate cover/guard | Bandsaw + drill (score-and-snap for thin) | 2 | — |
| Elevator rails, precise parallel | Drill press + careful layout, or router | 2–3 | **COTS elevator kit** — `CAT` lists cascade/continuous at rank 2 for this reason |
| Long slot | Router, or drill-two-holes-and-file | 3 → 2 | Drill both ends, saw/file between. Ugly, works |
| Anything requiring ±0.002 in | Mill | **4** | Redesign the tolerance out: slots, oversized holes, adjustment screws |
| Chain/belt tension | Slotted mounts or COTS tensioner | 2 | Tensioner pulley on a grid hole |
| Hard stop under load | Bolted stop block | 1–2 | Never rely on software-only limits (`PROG`) |

**The general rule to teach [S]:** *accuracy belongs in one place per assembly.* If the tube skeleton
holds the geometry, every plate can be a rectangle. If the plates hold the geometry, you need a router.
**Choose the first one.**

### 5.3 3D printing — where it genuinely replaces machining, and where it lies to you

| Use | Verdict | Note |
|---|---|---|
| Intake rollers, spacers, pulleys (light) | **Yes** | Highest-value use on a small team |
| Sensor and camera mounts | **Yes** | Iterate freely |
| Wire management, guards, funnels | **Yes** | |
| Game-piece guides / hoppers | **Yes** | Geometry-heavy, load-light — exactly printing's strength |
| Structural brackets in compression | **Conditional** | High wall count, ≥50% infill, PETG or nylon-CF; **never** a load path with impact |
| Gears | **Prototype only** | Print to validate ratios; buy the real one |
| Anything taking a bolt in tension | **No** — unless a metal insert/washer spreads the load | The classic pull-through failure |
| Anything in the drivetrain load path | **No** | |
| Parts >8 h print time | **Treat as a queue resource** | One printer = `CAP` §5.2 route C, again |

**[S]** Print-farm math: one printer, ~10 usable h/day, ~40% of prints on a school printer either fail
or need re-slicing. A 6-hour bracket is really an overnight commitment. **Print the next iteration
before you need it**, and keep a printed-spares box for the pit.

### 5.4 Outsourced 2D — the one capability worth buying, and its exact conditions

`CAP` §7.1 ranks machine access as constraint **#4**, "**High elasticity — via money**", and it is the
only constraint on that list that a few hundred dollars actually relaxes.

| Item | Detail |
|---|---|
| Vendors verified live 2026-08-22 | **https://sendcutsend.com/** (200) · **https://www.xometry.com/** (200). A **sponsor** with a waterjet or laser is better than both, and free |
| What to send | **2D DXF** of a flat profile, plus material and thickness. Nothing 3D, nothing tolerance-critical |
| Design rules to follow **[H]** | Min hole diameter ≥ material thickness; keep features ≥1× thickness from edges; add your own alignment holes; no internal sharp corners (add relief); check the vendor's own current rules before ordering — **specific tolerances and minimums UNVERIFIED here** |
| Lead time | **[S]** plan **1–2 weeks** door to door, more in January when every FRC team orders at once |
| Cost control | Nest multiple parts in one order; order **the whole season's flat parts once**, not three times |
| Gate condition (`RUB` G1) | Passes **only** if ≤2 parts **and** ≥2 weeks' lead **and** the account exists already |
| **Off-season action** | **Open the account and run one real test order before December** (`CAP` §7.5 names this explicitly). An untested account in February is not a capability |

### 5.5 A sponsor machine shop is not the same as owning a mill

**[S]** Teams routinely score their capability as "we have a sponsor with a CNC." Score it honestly:

| Question | If the answer is no, it is **not** a capability |
|---|---|
| Can you get a part made in **≤5 days**, twice, in February? | |
| Do they accept your file format without a paid engineer reformatting it? | |
| Have you actually run one job through them this calendar year? | |
| Is there a named human who answers, not "the company"? | |
| Can they do it **again** when v2 is needed 6 days later? | |

Iteration count, not part quality, is what a small team needs. A sponsor who makes one beautiful part
in three weeks does not relax the constraint — **and the rubric should be told so**: set
`outsourced_2d_account: false` unless all five answers are yes.

### 5.6 If the team ever buys one machine

**[S]** Ordered by hours-returned per dollar for *this* team:

| Priority | Purchase | Why |
|---:|---|---|
| 1 | **A second 3D printer** | Cheapest relief of route C; two mechanisms stop contending; failed prints stop being critical-path |
| 2 | **Pre-gridded tube stock** (a consumable, not a machine) | Converts the single biggest drill-press time sink into money |
| 3 | **A good bandsaw blade supply + a decent vise/fence** | Accuracy at rank 2 is mostly fixturing, not machine |
| 4 | **Outsourced-2D budget line (~$300–500/season)** | Buys rank-3 capability without owning it |
| 5 | Hobby CNC router | Real capability, and **CAM Studio (§1.2) now removes the software half of the cost** — but the machine still needs a *person* to own fixturing, feeds and toolpaths, and that person is a workstream (`CAP` §5.1). You have three |

**Do not buy a mill.** Not because mills are bad — because a mill without a qualified supervisor is
`CAP` §6.2's non-delegable 25% of mentor time, and that time is already spent.

---

## §6. Sourcing and lead times — and why your first deadline is in November

### 6.1 Vendors, verified

All links checked live **2026-08-22** by [`../../tools/cad-linkcheck.sh`](../../tools/cad-linkcheck.sh).
**Prices and SKUs are in [`../bom/`](../bom/), not here.**

| Vendor | URL | Use it for | Status |
|---|---|---|---|
| REV Robotics | https://www.revrobotics.com/ | Motors, controllers, MAXPlanetary, swerve, structure | **[C]** 200 |
| WCP | https://www.wcproducts.com/ · docs at https://docs.wcproducts.com/ | Swerve, gearboxes, structure, mechanism kits | **[C]** 200 |
| AndyMark | https://andymark.com/ | Wheels, KoP-adjacent, chassis, hardware | **[C]** 200 |
| The Thrifty Bot | https://www.thethriftybot.com/ | Swerve, encoders, low-cost mechanism parts | **[C]** 200 |
| Swerve Drive Specialties | https://www.swervedrivespecialties.com/ | MK4/MK4i/MK4n modules | **[C]** 200 |
| CTR Electronics | https://store.ctr-electronics.com/ | Kraken/Falcon, Pigeon, CANivore | **[C]** 200 |
| McMaster-Carr | https://www.mcmaster.com/ | Fasteners, raw stock, bearings — **fastest shipping in the industry [H]** | **[C]** 200 |
| Grainger | https://www.grainger.com/ | Industrial consumables, blades, abrasives | **[C]** 200 |
| SendCutSend | https://sendcutsend.com/ | Outsourced 2D flat parts | **[C]** 200 |
| Xometry | https://www.xometry.com/ | Outsourced 2D/3D, broader processes | **[C]** 200 |
| VEXpro | vexrobotics.com/vexpro | Gears, shafts, structure | **UNVERIFIED** — 403 to the automated checker; open in a browser |
| FIRST Kit of Parts | https://www.firstinspires.org/resources/library/frc/kit-of-parts | KoP contents, virtual kit, vouchers | **[C]** 200 (redirected from `/robotics/frc/kit-of-parts`) |

### 6.2 Lead times, from the catalog's own fields

Verbatim `lead_time_weeks` / `stockout_risk` from
[`../bom/mechanism_catalog.yaml`](../bom/mechanism_catalog.yaml) — **[H]/[S]** planning figures, not
vendor promises:

| Weeks | Stockout | Mechanisms |
|---:|---|---|
| **6** | **high** | `baseline_electrical_package` ← **the earliest order-by on the whole robot** |
| **5** | high | `turret` (large-diameter bearing) — and it is gated anyway (§5.1) |
| **4** | high/med | `swerve_drivetrain`, `variable_hood_shooter`, `cascade_elevator`, `double_jointed_arm` |
| **3** | med/low | `tank_wcd`, `deploying_intake`, `vision_package`, flywheels, `catapult`, `continuous_elevator`, `telescoping_arm/climber`, `single_jointed_arm`, `virtual_four_bar` |
| **2** | low | intakes, `gripper_end_effector`, `indexer_conveyor`, `bumpers_frame`, `winch_climber`, `pneumatics_package` |
| **0–1** | low | `kop_chassis`, `hopper`, `passive_latch_climber` |

**The structural insight:** the long-lead items are **electrical and drivetrain** — precisely the
**game-independent** half of the robot. You can order them before you know the game. The
game-*dependent* mechanisms are almost all 2–3 weeks, which fits inside the season.

### 6.3 What to pre-order in the off-season (game-independent — safe to buy blind)

**[S]** on quantities; the parts themselves are game-independent by inspection.

| Buy now | Why it is safe | Order by |
|---|---|---|
| **Electrical package** — PDH/PDP, breakers, main breaker, wire, lugs, connectors, battery(s), charger | Every FRC robot needs it in the same quantity | **2026-11-21** (§6.4) |
| **Drivetrain**: modules **or** KoP chassis + wheels + gearboxes + motors | Drivetrain is game-independent (§7) | 2026-11-21 → 2026-12-05 |
| **Bumper materials**: plywood/ply-substitute, pool noodle, fabric, brackets | Every year, same construction **[H]**. *Dimensions* change with the frame — buy stock, not cut parts | Dec |
| **Standard stock**: 1×1 and 2×1 tube, 1/8 in and 1/4 in plate/polycarb, hex shaft, bearings, spacers | §3.5 standardisation — you will use all of it | Nov–Dec |
| **Fastener library**: #10-32, 1/4-20, 8-32 in a labelled bin | The most common shop stoppage is a missing screw **[S]** | Nov |
| **Consumables**: bandsaw blades, drill bits, taps, filament, cutting fluid, Loctite | Cheap; running out costs a meeting | Nov–Dec |
| **Spare motor + spare controller** | `PF` weights reliability at 88; a dead motor on Thursday of an event is a season | Dec |
| **Outsourced-2D test order** | Validates the account before it is critical (§5.4) | **Dec** |

**Do NOT pre-order:** anything whose size depends on the game piece (rollers, compliant wheels, belt
lengths, gripper parts), any mechanism-specific gearbox ratio, or anything you are "pretty sure"
you'll want. That is `CAP` §8.1's $2,500 discretionary line, and it is the budget that buys the actual
scoring mechanism in January.

### 6.4 The November sequence — the calendar nobody expects

| Date | Event | Why it binds design/manufacturing |
|---|---|---|
| **2026-09-24 12:00 ET** | Kit & Kickoff selection **opens**; event preferencing Round 1 opens | **[C]** `CAL`. `CAP` §7.4: choose **field size first, then the latest week** — a Week 3–4 event is +255 effective hours, free, and those hours land *after* the robot exists |
| **2026-11-12** | **Pre-Kickoff Virtual Kit Release** | **[C]** First look at KoP contents. **This is when you learn what the 2027 control system physically is** and can stop designing around a placeholder (§1.4) |
| **2026-11-17 12:00 ET** | Kit & Kickoff selection **closes**; registration closes | **[C]** Hard. After this the KoP order is fixed. Also `CAP` §6.4's deadline for recruiting a second technical mentor |
| **2026-11-21** | **Earliest order-by**, computed by `tools/bom-builder.py` | **[S]** 6-week lead + 1-week margin on `baseline_electrical_package`, back-solved from 2027-01-09. **Miss it and your electrical system arrives after you needed it — no design decision can recover that** |
| **2026-12-05 / 12-19 / 12-26** | Order-by dates for 4 / 2 / 1-week-lead items | **[S]** `CAT` §, same back-solve |
| **2027-01-09 12:00 ET** | **Kickoff** | Only *now* do you order game-dependent parts |

**Read that table again.** The first purchasing deadline that can cost you a robot is **seven weeks
before the game exists**. Nothing else in this file is as time-critical.

### 6.5 The standard kickoff order (game-dependent half)

**[S]** Sequence, not a shopping list — the list comes from `bom-builder.py` on your chosen strategy.

| Day | Action |
|---|---|
| **Day 0 (Sat)** | Read manual, strategy. **Order nothing.** |
| **Day 1 (Sun)** | Strategy converges; `score-strategy.py` run; mechanism archetypes chosen from `CAT` |
| **Day 2 (Mon)** | G0 concept review. Prototype the uncertain physics |
| **Day 3 (Tue)** | **First game-dependent order goes out** — compliant wheels, belts, the mechanism's gearbox, anything with a 2–3 week lead. Order **spares of the fragile parts in the same order**; a second shipment costs a week |
| **Day 5–7** | Raw stock top-up from McMaster (fast **[H]**), based on the actual cut list |
| **Week 2** | The *only* re-order window that is comfortably safe for a Week 4 event; after this, every order is a risk |
| **Standing rule** | One person places all orders (`CAP` §4.2 mentor row). Two people ordering = double-ordered motors and a missing $80 of the $2,500 |

---

## §7. The off-season build calendar, 2026-08-22 → 2027-01-09

### 7.1 What the fall is actually worth

**[S]** `capacity_model.py` has no fall mode; this is a hand derivation in the same units, and it
should be treated as an estimate, not as model output.

| Step | Value |
|---|---:|
| Calendar weeks 2026-08-24 → 2027-01-08 | ~19.5 |
| Fall calendar factor (school start, sports, exams, holidays — heavier losses than build season) | ×0.75 |
| Effective weeks | **~14.6** |
| Scheduled hours/week in the off-season (1 weeknight + partial Saturday) | 6 |
| Nominal person-hours | 15 × 6 × 14.6 ≈ **1,314** |
| Effective multiplier (lower than 0.352 — attendance is worse and the training tax is being paid deliberately) | ×0.30 |
| **Effective fall hours** | **≈ 395 veq-h** |

**The fall is worth about two-thirds of a build season, at zero deadline pressure, and it is spent on
the two constraints that cannot be relaxed after kickoff** (`CAP` §7.1: mentor attention and
unsupervised student leads). It is also where the first-year training tax — **−73.5 veq-h** if paid in
January (`CAP` §2.4) — gets paid against hours that have no competing use.

### 7.2 The allocation

| Line | veq-h | Owner (`CAP` §4.2 slots) | Rationale |
|---|---:|---|---|
| CAD skills → 4 students who can model unsupervised | **110** | CAD lead (C), mentor | Constraint #2. This is the *only* time it can be relaxed |
| **Build a complete drivetrain** (game-independent) | **90** | Core tech B, Veteran G, first-years | Fabrication reps + a driveable robot in December |
| **Control-system / Systemcore work** | **60** | Core tech D + E | `PROG` §0; `CAP` §3.2's third programmer |
| Manufacturing skills + tool certification | **45** | Mentor, Veteran G | Route C relief: more people cleared on the bandsaw = less queue |
| **Drive practice** on the 2026 robot | **50** | Veteran H (driver), C (operator) | `PF` weights drive practice **90**, the highest factor measured |
| Sourcing, inventory, account setup, orders | **25** | Mentor + Veteran I | §6.3, §6.4 |
| Design-review habit-building on a fake project | **15** | Everyone | §4 rehearsal, when being wrong is free |
| **Total** | **≈395** | | matches §7.1 |

### 7.3 Month by month

| Window | Design | Build | Learn | Deliverable at the end |
|---|---|---|---|---|
| **Aug 22 – Sep 20** | **Claim the Onshape Educator Plan and build the classroom (§1.3)** — shared team email, classroom owns documents, 15 student accounts, one part library chosen (§2.2). Then folder structure (§2.4). Model the 2026 robot's drivetrain from scratch as a training exercise | Shop clean-out; inventory; label the fastener library; fix the bandsaw fence | Onshape fundamentals: sketch → part → assembly → mate. Every student, including first-years | Every student has an Onshape account; the folder tree exists; **inventory list exists** |
| **Sep 21 – Oct 18** | **Master-sketch practice**: re-do a past game's robot layout as a layout sketch (§3.2). Standard stack-up library modelled (§3.5) | **Start the off-season drivetrain**: cut tube, drill grid, assemble frame | Drill-press accuracy, bandsaw safety, tapping, riveting. Tool certification checklist | **Event choice submitted** (opens 09-24 — field size first, then latest week, `CAP` §7.4) · frame assembled |
| **Oct 19 – Nov 15** | Electronics-board design as a **gridded flat plate** with a Systemcore placeholder (§1.4). Bumper design from stock | Drivetrain rolling. Wire the board. **Run the outsourced-2D test order** (§5.4) | Wiring, crimping, CAN, breaker sizing. First-years cut real parts | **Rolling, wired chassis.** Outsourced account proven |
| **Nov 12** | — | — | — | **Pre-Kickoff Virtual Kit Release** — read it the day it drops; update the control-system placeholder |
| **Nov 16 – Nov 21** | Freeze the game-independent BOM | — | — | **2026-11-17 registration closes** · **2026-11-21 long-lead order placed** (§6.4). *If nothing else in this file happens, this must* |
| **Nov 22 – Dec 20** | Run three **full G0→G1→G2 reviews** on a fake mechanism so the process is muscle memory by January | Build a **practice mechanism** — an intake or elevator from `CAT` at rank 1–2 — purely as a fabrication rep. Throw it away in January without regret | Systemcore/WPILib 2027 as it becomes available (`PROG`). **Third programmer trained** | 2 more students who can model unsupervised · review habit exists |
| **Dec 21 – Jan 8** | Light. Prepare kickoff templates: empty master sketch with variable placeholders, empty BOM, empty cut list | **Drive practice**, weekly, on the off-season drivetrain | Kickoff-day roles rehearsed ([`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md)) | **A driveable robot exists on 2027-01-09** |

### 7.4 The game-independent / game-dependent line, drawn explicitly

| Game-**independent** — build it now | Game-**dependent** — do not touch it until 2027-01-09 |
|---|---|
| Drivetrain (frame, modules/gearboxes, wheels, bumper mounts) | Intake geometry (depends on the game piece) |
| Electrical system, board layout, wiring standards | Launcher/hood geometry, roller compliance, exit angle |
| Control system port and code architecture (`PROG`) | Elevator height and stage count |
| Bumper construction technique (not dimensions) | Arm lengths, joint count, end effector |
| Standard stack-ups, hole grid, tooling, fixtures | Endgame/climb mechanism |
| CAD library, review process, ordering process | Auto routines, scoring paths |
| Driver skill | Cycle strategy |

**[S]** but with one hard caveat: *frame dimensions and bumper rules are set by the 2027 manual and are
**UNVERIFIED** until kickoff.* Build the off-season drivetrain to the **2026** rules as a **training
and practice** article, and expect to re-cut the frame rails in January. That is a deliberate ~8 h
cost buying ~90 h of fabrication reps and a December driving platform. If the 2027 frame rules turn
out unchanged, you keep the chassis and the trade was free.

### 7.5 The five off-season actions ranked by return

Consistent with `CAP` §7.5, restricted to this file's domain:

| # | Action | Relaxes | Deadline |
|---:|---|---|---|
| 1 | **Place the long-lead electrical/drivetrain order** | The only deadline here that can lose a season | **2026-11-21** |
| 2 | **Get 2 more students to unsupervised-CAD standard** | `CAP` constraint #2, the one perturbation that halves `novel_mechanisms_max` | 2027-01-09 |
| 3 | **Open and test the outsourced-2D account** | Constraint #4 / `RUB` gate G1 | 2026-12 |
| 4 | **Certify 3 more students on bandsaw + drill press** | Route C queue contention | 2026-11 |
| 5 | **Build and drive a complete drivetrain** | `PF` drive practice (90) + fabrication reps + December driving | 2026-12-20 |

---

## §8. Where AI helps in this workflow, and where it does not

**Policy first.** FIRST **permits** AI use with attribution — the authority is
[`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md).
Read it before using any of this in a judged context; **attribute**, and be prepared to explain the
work as your own understanding.

| Task | AI usefulness | Honest note |
|---|---|---|
| Generating a design-review checklist, cut list template, order tracker | **High** | Pure desk work. This is the labour AI should absorb (the project's whole premise) |
| Summarising a Team Update's design impact | **High** | With [`../../tools/teamupdate-diff.py`](../../tools/teamupdate-diff.py) |
| Explaining a manufacturing process to a first-year | **High** | Faster than a mentor and does not consume the 3.4 h/wk |
| Sanity-checking gear ratios, belt lengths, centre distances | **Medium** | **Always verify the arithmetic yourself.** Plausible-looking wrong numbers are the failure mode |
| Suggesting a mechanism archetype for a described task | **Medium** | Use `CAT` for the shortlist; AI for the argument against each |
| **Producing CAD geometry** | **Low / none** | It cannot model your robot. Treat any claim otherwise with suspicion |
| **Predicting whether a mechanism will work physically** | **Low** | It has never touched your game piece. **Prototype (§3.1 step 2). There is no substitute** |
| Estimating hours or costs | **Low** | Use `CAP` and `../bom/`, which are calibrated to *this* team |
| Citing part numbers, prices, URLs | **Dangerous** | This corpus exists because those are exactly what get fabricated. Verify every one against a live vendor page |

---

## §9. Validation

### 9.1 Internal consistency checks (run them; they should all pass)

| Check | Command | Expected |
|---|---|---|
| Tooling vocabulary matches the catalog | `grep -o 'tooling_floor: [a-z_]*' reference/bom/mechanism_catalog.yaml \| sort \| uniq -c` | 3 / 13 / 2 / 9 across `hand_tools` / `bandsaw_drillpress` / `router_cnc` / `mill_lathe` — the same four names used in §5.1 |
| Gate G1 wording unchanged | `grep -n "G1 MACHINE" reference/ACHIEVABILITY-RUBRIC.md` | The ≤2 parts / ≥2 weeks exception quoted in §5.1 and §5.4 |
| Hours claims match the capacity model | `python tools/capacity_model.py \| grep -E "CAD|Fabrication"` | CAD 74.9, fabrication 129.8 — §3.5's savings estimate is quoted against 130 |
| Order-by date | `python tools/bom-builder.py reference/bom/examples/simple.yaml --markdown \| grep -i order` | **2026-11-21** for the 6-week electrical package |
| Every URL in this file resolves | `bash tools/cad-linkcheck.sh` | No 404, no 000. 403/406 = bot-blocked, open in a browser |

### 9.2 Cross-file consistency (asserted, checked by reading)

| Claim here | Must agree with | Status |
|---|---|---|
| 2 novel mechanisms; review budget supports 3 workstreams (§4.2) | `CAP` §5.3, §6.3 | ✅ 1.6 mentor-h/mechanism × 3 ≈ 4.8 h; the 3.4 h/wk unblock budget covers **staggered** reviews, not three in one week — §4.2 says so explicitly |
| Rank 3–4 designs are gated (§5.1) | `RUB` §A9 anchors 2 and 0, gate G1 | ✅ same thresholds, same exception |
| Off-season fall hours ≈395 veq-h (§7.1) | `CAP` — **has no fall mode** | ⚠️ **Derived here, not model output.** Labelled [S]. Listed in Known Limitations |
| No BIOCORE game claim anywhere | `research/00_PREMISE_CORRECTION.md` | ✅ every game-dependent dimension marked UNVERIFIED-until-kickoff |
| Prices/SKUs not duplicated | `../bom/` is the price authority | ✅ this file contains **no** price or SKU |

### 9.3 What would falsify this file

- **The 2027 KoP changes the drivetrain baseline** (Nov 12 release). §7.3's off-season drivetrain plan
  would need re-scoping — the *method* survives, the *article* may not.
- **Systemcore's physical envelope is radically different** from a roboRIO-class board (e.g. requires
  active cooling or a specific orientation). §3.4's placeholder approach is designed for exactly this,
  but a large surprise would force an electronics-board redesign in January.
- **The Onshape Educator Plan terms change.** §1 is a recommendation contingent on a $0 licence (and,
  secondarily, on free CAM Studio); if either became paid, the answer for a limited-budget team changes
  and §1.1 must be re-scored. Re-run `tools/cad-linkcheck.sh` and re-read §1.3's four pages each
  September — licence offers are the fastest-moving fact in this file.
- **The team acquires a second technical mentor and a router.** Then rank 3 stops being gated,
  plate-and-standoff becomes available, and §5.2's workaround column is no longer the default.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/team-ops/02_design_cad_manufacturing.md` | this document |
| `tools/cad-linkcheck.sh` | re-verifies every CAD/vendor/sourcing URL cited above; `--md` for a markdown table. **Extended this pass** with the six FIRST-licensing URLs (§1.3) and the three part-library URLs (§2.2) — **24 URLs, all HTTP 200 on 2026-08-22** |

Nothing marked DONE was modified. [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md),
[`../ACHIEVABILITY-RUBRIC.md`](../ACHIEVABILITY-RUBRIC.md), everything under
[`../bom/`](../bom/), [`03_programming_stack.md`](03_programming_stack.md) and
[`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md)
were read and cited, not edited.

---

## Known limitations

- **The fall-hours figure (~395 veq-h, §7.1) is not model output.** `capacity_model.py` models the
  build season only. The 0.75 calendar factor and 0.30 multiplier are hand-chosen **[S]**. If the team
  meets more than 6 h/wk in the fall — many do in September — the figure is low; if the fall is one
  meeting a week, it is high by half. **The month-by-month plan in §7.3 is ordered correctly regardless;
  only the total is soft.**
- **Licensing is now verified for Onshape and only for Onshape.** §1.3's procedure was read off
  Onshape's own FIRST programme, sign-up, onboarding and CAM-for-FIRST pages (all HTTP 200,
  2026-08-22), so the **Educator Plan** path, the classroom model and free CAM Studio are **[C]**.
  Four things around it remain **UNVERIFIED** and are flagged in place: whether Educator-Plan documents
  default to **private** (no page read here says), **renewal/expiry** terms, the `FIRST@ptc.com` contact
  address (search-summary only), and PTC's **grant** programme terms. **SolidWorks** sponsorship
  (guessed URL 404'd) and **Autodesk** education terms (403 to the checker — a bot block, *not* proof of
  absence) are unverified. Confirm any of it in a browser before quoting it to a student or a sponsor.
- **Part libraries: install path verified, provenance not.** Both MKCad and FRCDesignLib are installed
  from the **Onshape App Store** (https://appstore.onshape.com/, 200), which is the only install
  instruction this file gives. `mkcad.com` is a **parked domain-sale page** as of 2026-08-22 — it is not
  the library's home and must not be linked. MKCad's authorship (FRC 1836) and its exact current
  contents come from community sources and **were not read off a primary page**; confirm the publisher
  in the App Store listing before installing. §2.2's "pick one library" rule is **[S]** — a judgement
  about small-team coherence, not a measured result.
- **Vendor design rules for outsourced 2D (§5.4) are generic [H], not quoted.** Minimum hole sizes,
  bend reliefs and tolerances differ by vendor, material and thickness and change over time. Read the
  vendor's own current rules before the order.
- **Every 2027 rule dimension is UNVERIFIED.** Frame perimeter, height limit, extension limit, bumper
  rules and game-piece geometry are not public until 2027-01-09. §3.2 is written so those numbers are
  *variables*; it is not written so that any particular value is right.
- **The DFM mapping table (§5.2) is judgement, not measurement.** The machine each operation requires
  is standard practice **[H]**; which workaround is *worth it* for this team is **[S]** and depends on
  the specific part. Use it as the vocabulary for a G1 review argument, not as a verdict.
- **§3.5's 15–25 saved fabrication hours is an estimate with no measurement behind it.** It is
  directionally defensible (fewer setups, fewer tool changes, fewer stockouts) and it is not a
  measured result. Do not build a schedule that *needs* those hours to close.
- **This file assumes the shop stated in `CAP`**: one bandsaw, one drill press, one 3D printer, one
  qualified supervising mentor. A team with a different shop should re-read §5.1 first and re-derive;
  every downstream conclusion in §5–§7 hangs off that row.
- **Nothing here has been tested against BIOCORE**, because BIOCORE does not exist yet. The method is
  what is being asserted, not its outcome.

---

## Security note

Every source consulted for this pass was either a local file in this project or a vendor/education URL
fetched **HEAD/status-only** by `curl` on 2026-08-22 — no page content was executed, and no page's text
was treated as instruction. The URL check writes nothing outside this project, uses no authentication,
and sends no user data. Nothing read during this pass contained text addressed to an AI assistant or
any attempt to issue instructions.
