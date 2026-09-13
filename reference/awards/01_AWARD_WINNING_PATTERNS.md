# What Actually Wins Each Robot-Adjacent FRC Award

**Purpose:** turn every robot-adjacent FRC award into an aimable target. For each award: the published
criteria (key wording quoted, the rest paraphrased), what real winners measurably had, the artifacts that
win it, the 5-minute pit pitch, the if-then design signal that makes it live, and the student-hours it
costs. Built so that on 2027-01-09 a ~15-student team can pick 2 award lanes in ten minutes and know
exactly who builds what.

**Companion file:** `reference/awards/award_target_matrix.csv`
(13 rows: 10 live robot-adjacent awards + 3 retired, with design signals, artifacts, hours and owners)
and the kickoff-day ranker `reference/awards/award_aim.py`.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

**Source shorthand**
`REB` = 2026 REBUILT manual (TU22, 166 pp) · `REEF` = 2025 REEFSCAPE (164 pp) · `CRES` = 2024 CRESCENDO
(153 pp) · `CHRG` = 2023 CHARGED UP (142 pp) · `RAPD` = 2022 RAPID REACT (136 pp) — all in
`manuals/archive/frc/`.

Award-specific primaries, all in `reference/awards/`:
`JM` = Judge Manual (Rev 2 – 2/18/2026, `_text/judge-manual.txt`, 147 KB) ·
`AW` = Award Workbook (Rev Oct 2025, `_text/award-workbook.txt`) ·
`TJT` = Technical Judges Tip Sheet (Rev Oct 2025, `_text/technical-judging-tips.txt`) ·
`MAW` = [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards) ·
`TAW` = [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards) ·
`TBA` = `research/awards_tba/tba_awards_2022..2026.csv` (23,162 award rows, 5 seasons).

FIRST's award text is quoted here only in short excerpts, each cited to its page or document and its
revision. Longer criteria are paraphrased and labeled as paraphrase; read the source for the exact wording.

> **BIOCORE is FRC.** Its sibling BIOBUZZ is FTC. Nothing in this document is derived from FTC sources;
> FTC has a different award slate (Inspire, Think, Connect, Innovate, Design, Motivate, Control) that does
> **not** apply here. See [`research/00_PREMISE_CORRECTION.md`](../../research/00_PREMISE_CORRECTION.md).

---

## 0. Kickoff-day 60-second workflow

Paste this on 2027-01-09 once you have settled on a robot concept. Every command below was run and
its output verified on 2026-08-22.

```bash
cd reference/awards   # run from the repository root

# 1. DID THE SLATE CHANGE? Re-pull FIRST's two authority pages and diff vs the locked 2026 baseline.
#    Catches renames (Dean's List -> FIRST Leadership, mid-season, TU12 2026) and sponsor churn.
python fetch_award_pages.py && python award_diff.py
#    exit 0 = slate unchanged; exit 1 = drift. If it drifts, re-read Sec.2 before building anything.

# 2. WHAT DOES OUR CONCEPT SIGNAL? List the declarable signals, then declare yours honestly.
python award_aim.py --list-signals

# 3. RANK OUR AWARD LANES. --have takes the signals your robot will ACTUALLY show a judge.
#    --budget is total student-hours you can spend on award materials all season.
python award_aim.py --have novel_mechanism,build_finish,risk_mitigation --budget 90 --lanes 2

# 4. ROOKIE / REBUILT TEAM? Rookie All-Star is worth 8 district points, not 5. Re-run with --rookie.
python award_aim.py --have build_finish,working_robot,outreach_story --rookie --lanes 2

# 5. Did the MANUAL add or drop an award? Diff its award mentions against the 2026 baseline.
#    Reads the flattened text your ingest step produces (ingest_<TAG>/full_layout.txt).
grep -ohE "([A-Z][A-Za-z']{1,20} )+Award" ../../manuals/2026-27_BIOCORE/ingest_*/full_layout.txt \
 | sed 's/  */ /g;s/^ *//;s/ *$//' \
 | sed -E 's/^(The|District Championship|District|Regional|Championship) //' \
 | grep -vE "^(Star|All Star|Winners|At the) Award$" \
 | sort -u | grep -vxF -f known_awards_2026.txt
#    Anything that survives is a genuinely new 2027 award or a rename. Both are news.
#    Empty output = slate unchanged. Verified empty against the REBUILT dry-run ingest (Sec.6.6).
```

Verified output of step 3 (run 2026-08-22):

```
1. Creativity Award   [score 14.56]  PRIMARY
     winners rank   : median 31.8% of quals   |  76.3% of winners won it only once
     cost           : 25-45 student-hours   owner: DESIGN_DOC_OWNER
2. Quality Award   [score 7.76]  SECONDARY
     winners rank   : median 18.2% of quals   |  69.6% of winners won it only once
     cost           : 20-35 student-hours   owner: BUILD_LEAD
TOTAL worst-case cost of these 2 lanes: 80 student-hours
Within your 90 h budget (10 h spare).
```

`award_aim.py` filters retired awards on `status_2026`, so it can never recommend the dead Safety or
Media & Technology awards, and it promotes Rookie All-Star to PRIMARY only when `--rookie` is passed.
Both behaviours are regression-tested in §6.3.

---

## 1. The three structural rules that govern all award strategy

These three facts matter more than any individual award's criteria. Get them wrong and every hour of
award prep is misallocated.

### 1.1 You can win **exactly one** judged award per event [C]

> "Do not award the same team more than 1 judged award at a single event." — `JM`, *Equitable Award
> Distribution (Spread the Wealth)*

The same section explains the reasoning and its one important limit. Paraphrase: FIRST wants awards spread
across as many teams as possible because that motivates more students, so one team collecting several
awards at an event runs against the policy. The limit is that the policy applies "within events, not
between events" (`JM` Rev 2, 2/18/2026, same section). Judges should not exclude a team from an award
because it won the same award at an earlier event, except for the awards that can be won only once per
level of competition (FIRST Impact, Rookie All-Star, Engineering Inspiration).

**Back-tested against `TBA`, 2022–2026:** of **12,993** team-events that won at least one judged award,
**12,992 won exactly one**. The single exception is 2022mxmo team 6832 (Judges' + Team Spirit).
That is a 99.992% hold rate on FIRST's own stated policy.

**Consequence, and it is the whole point of this document:** chasing eight awards does not multiply your
chances — the ceiling is one. A 15-student team maximises P(win *something*) by pointing **two** lanes at
the awards its robot genuinely signals, not by spreading thin across eight. Judged and *field* awards are
explicitly exempt from spread-the-wealth, so winning the event and winning a judged award can co-occur.

### 1.2 Every machine award is worth **identical** district points [C]

> "Team Judged Awards — 10 points for FIRST Impact Award / 8 points each for Engineering Inspiration and
> Rookie All Star Awards / 5 points each for all other team judged awards" — `REB` Table 11-1, p.133

Points earned at District Championships are **multiplied by 3** (`REB` §11.1). So Industrial Design,
Quality, Excellence in Engineering, Creativity, Innovation in Control, Autonomous, Imagery, Judges',
Team Spirit, Gracious Professionalism, Team Sustainability and Rising All-Star are **all worth 5 points**.

**Consequence:** among the machine awards there is no "more valuable" target. Choose purely on
**probability of winning**. The only judged awards worth more are Impact (10), Engineering Inspiration (8)
and Rookie All-Star (8) — and only RAS is realistically robot-adjacent, for rookies only.

Also `REB` §11.1.4 [C]: *"If an award … is not judged at the event (e.g. Safety Animation Award,
sponsored by UL), no points are earned."* The same rule also excludes awards that are not judged or not
given to a team, such as the FIRST Leadership Award (paraphrase).
The Safety Animation Award earns **zero district points**.

### 1.3 Day 1 shortlists you; Day 2 wins it [C]

`JM` describes two judging models (Split Judging / Split Award). Both converge on the same shape:

| Stage | What happens (`JM`, *Judging Process*) | What it means for you |
|---|---|---|
| Day 1 | Every team interviewed **twice** — once machine-focused, once team-focused | Two shots to plant a hook |
| End Day 1 | "Judges can nominate 1-2 teams for each award they judged" → **Short List Matrix** | You are on a list or you are not |
| Day 2 | Shortlisted teams **re-interviewed** by judges who nominated them, for "specific subsets of awards" | The deciding conversation |
| Final | "the JA will help deconflict between awards" | One award assigned to you at most |

**Consequence:** the Day 1 pit pitch's job is *not* to win — it is to be **nominatable in a single named
award lane**. A pitch that spreads across five awards gives a judge nothing to write in the matrix. A
pitch that hammers one lane gets you nominated. If you get a second, longer, more specific interview on
Day 2, you are on the short list — switch from breadth to depth and bring out the data.

**Corroborating rule [C]:** two dedicated **Match Observers** validate pit claims against field
performance — *"Pit judges should validate what teams tell them with the Match Observers"* (`JM`). A claim
you cannot demonstrate on the field is a liability, not an asset. See §5.4.

---

## 2. The 2027-candidate slate: live, dead, and volatile

### 2.1 Live robot-adjacent awards [C]

Confirmed present in `TBA` 2026 at full event volume, in `JM` Ch.4, and on `MAW`/`TAW`.

| Award (exact 2026 name) | Category | Given at % of 2026 events | District pts |
|---|---|---:|---:|
| Industrial Design Award | Machine | 91.3 | 5 |
| Quality Award | Machine | 92.2 | 5 |
| Excellence in Engineering Award sponsored by Littelfuse | Machine | 91.6 | 5 |
| Creativity Award sponsored by Rockwell Automation | Machine | 91.3 | 5 |
| Innovation in Control Award sponsored by nVent | Machine | 91.8 | 5 |
| Autonomous Award sponsored by Google.org | Machine | 91.5 | 5 |
| Imagery Award in honor of Jack Kamen | Team | 91.2 | 5 |
| Judges' Award | Discretionary | 93.5 | 5 |
| Rising All-Star Award | Team (optional) | 75.8 | 5 |
| Rookie All Star Award | Team (rookie only) | 59.3 | 8 |

### 2.2 Dead — do **not** build materials for these [C]

The task brief listed Safety and Media & Technology as candidate targets. Both are gone from FRC.

| Award | Status | Evidence |
|---|---|---|
| **Industrial Safety Award** (was sponsored by UL) | **Removed for the 2022 season** | 0 mentions across `RAPD`/`CHRG`/`CRES`/`REEF`/`REB`; absent from `JM`, `AW`, `MAW`, `TAW`; in `TBA` 2022–2026 only 3 rows, all offseason custom awards (2024nycrr "Safety Award in memory of Ken Vessey", 2025txntx, 2025txsg) |
| **Media and Technology Innovation Award** | **Not on the FRC slate** | **Zero** rows in `TBA` 2022–2026; absent from `JM`, `AW`, `MAW`, `TAW` |
| **Safety Animation Award** sponsored by UL | Live but **submitted, not judged at event** | `REB` §11.1.4 — earns **0 district points**; judged off-event, no pit interaction |

**Safety did not disappear — it changed category.** It is now an award-**eligibility gate**: alongside
Core Values and Gracious Professionalism, `JM` requires teams to *"implement and follow appropriate safety
practices"* to be eligible for any award (`JM` Rev 2, 2/18/2026, *Judged Awards*). And
`AW`'s team question bank still asks *"How do you ensure that your team is following correct safety
practices?"* Safety now costs you awards if absent and earns you none if present. Budget it as
compliance, not as a lane.

### 2.3 Award names are volatile — re-verify at kickoff [C]

Name churn is not hypothetical; it happened **mid-season** in 2026.

| Change | When | Evidence |
|---|---|---|
| Dean's List Award → **FIRST Leadership Award** | Effective **Feb 18, 2026**, mid-season | [REBUILT Team Update 12](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate12.pdf) |
| Chairman's Award → FIRST Impact Award | 2022 | `TBA` diff |
| Industrial Design "sponsored by General Motors" → unsponsored | 2024→2025 | `TBA`: 726 GM-suffixed rows, then 211 bare |
| Autonomous "sponsored by Ford" → "sponsored by Google.org" | 2024→2025 | `TBA`: 341 Ford rows, 208 Google.org rows |
| Autonomous "Google.org" → **"Google DeepMind"** | Listed in `JM` Rev 2 (2/18/2026) while `MAW` and `TBA` still say Google.org | **Live discrepancy** — sponsor name in flux |

`JM` itself warns: *"Note: Most of the Award Descriptions & Guidelines have been updated for the 2026
season."* **[S] Expect at least one rename for 2027.** Step 1 of §0 exists precisely to catch it. Never
print an award name onto a physical artifact before running that diff.

---

## 3. Award dossiers

Each dossier gives the criteria (one key sentence quoted, the rest paraphrased), the measured winner
profile, the artifacts, the pitch, the design signal, and the cost. Winner-profile statistics are computed
over `TBA` 2022–2026 (see §6.1 for method).

**Reading the winner profile.** *median rank* = median qualification-rank percentile of winners; lower
means winners ranked better. *one-time* = share of distinct winning teams that won it only once — high
means the award is open to newcomers. *3+ share* = share of all wins taken by teams winning it 3+ times —
high means a dynasty award. *bottom-half share* = of all machine-award wins by teams finishing in the
**bottom half** of quals, the share that were this award.

---

### 3.1 Creativity Award sponsored by Rockwell Automation — **the small team's best robot award**

**Published criteria** (`MAW`, `AW`, both Rev Oct 2025) [C]:

> "Since creativity may involve risk of failure, the team should be able to describe how they mitigated
> that risk." (Creativity Award guidelines, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** a robot component, concept or attribute that improves strategy of play and was
  designed on purpose, not found by accident.
- The team can describe the creative feature and show how it was conceived and developed.
- The feature's uniqueness has a practical use and serves the objectives of the game.
- When the feature works as designed, it adds to the team's results on the field.

**What winners actually had** [C]:

| Metric | Value | Rank among 6 machine awards |
|---|---:|---|
| Wins 2022–2026 / distinct teams | 938 / **706** | most distinct winners |
| Median winner qual rank | **31.8%** | **worst-ranked winners** = least field-dependent |
| One-time winners | **76.3%** | **most open** machine award |
| Wins by 3+-time winners | **16.1%** | **least dynastic** machine award |
| Share of bottom-half machine-award wins | **35.6%** | **#1 by a factor of 2.3** |

That last row is the headline. Of every machine award won by a team finishing in the **bottom half** of
qualification, **35.6% were Creativity** — versus 15.6% Quality, 15.0% Industrial Design, 6.2% Autonomous.
**Creativity is the one machine award that does not require you to be good at the game.**

Top repeat winners, verified on The Blue Alliance: **4907 Thunderstamps** (10 wins), 2481 (6), 324 (5),
8608 (5). Even the most decorated Creativity team has fewer wins than the top Autonomous team.

What judges are told to look for on the field (`TJT`) [C]. Paraphrase: match observers flag any robot that
handles a game task (collecting or scoring game pieces, the end game) differently from the other robots at
the event. The vetting step sets a low bar for performance:

> The mechanism "**does not need to be the best** at completing the game challenge, but it should complete
> the desired objective." (`TJT`, Technical Judges Tip Sheet, Rev. Oct 2025, Creativity Award)

**Artifacts that win it**

| Artifact | Spec | Why it maps to a criterion |
|---|---|---|
| **Origin-story board** (A3, in pit) | Napkin sketch → CAD iteration → final part, 3–5 dated images left to right | Directly answers "can trace its conception and design" |
| **The failed prototype**, kept and labelled | The v1 that didn't work, on the pit table with a 1-line tag | Evidence for "describe how they mitigated that risk" — the highest-value and most-skipped artifact |
| **30-second bench demo** | The mechanism (or a spare) actuating by hand or on a battery, off-robot | Judges may not touch the robot uninvited (`JM`); a spare you hand them removes that barrier |
| **One-line uniqueness claim** | "We are the only team here that does X by Y" | Gives the judge the sentence to write in the Short List Matrix |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | **Name the lane** | "The thing we'd most like to show you is our \<mechanism\> — we think it's the most unusual solution to \<game task\> here." |
| 0:30–1:30 | **Show it move** | Bench demo. Silent for 5 seconds while it actuates. Then: what it does, in one sentence. |
| 1:30–2:30 | **Trace conception** | Walk the origin board left to right. Name the student who had the idea and the date. |
| 2:30–3:30 | **The risk story** | "This was risky because \<X\>. Here is v1, which failed at \<Y\>. We mitigated by \<Z\>." Hand them the failed prototype. |
| 3:30–4:30 | **Practical payoff** | "It gets us \<N\> more cycles / lets us score from \<place\> nobody else can." Cite a real match number. |
| 4:30–5:00 | **Close the loop** | "Have you seen anyone else doing it this way?" — invites the comparison judges are told to make. |

**DESIGN SIGNAL** — *if your robot solves one game task in a way visibly different from the other 30
robots in the venue, and you kept the failed prototype and can date the idea, Creativity becomes a live
target — and it is the only machine award that stays live if you finish in the bottom half of quals.*

**Cost: 25–45 student-hours.** Owner: `DESIGN_DOC_OWNER` (1 student + mentor review).
Origin board 8–12 h · photographing/labelling iterations 4–8 h (near-zero if photographed as you build) ·
bench-demo spare 8–15 h · pitch rehearsal 5–10 h. **The cheapest robot award to prepare**, because the
artifacts are byproducts of building the mechanism — *if* you photograph as you go. Retro-fitting an
origin board in week 6 costs triple.

---

### 3.2 Quality Award — the reliability award

**Published criteria** (`MAW`, `AW`) [C]:

> "A team must be able to describe their quality plan i.e. how their design ensures robustness throughout
> the entire competition." (Quality Award guidelines, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** a machine that is sound in both its design concept and its fabrication.
- Quality shows across the whole machine: workmanship, welds, fasteners and attachments, wiring, paint.
- The machine survives the wear of competition and keeps working, helped by redundancy and risk
  mitigation designed in from the start.
- Building the machine this way contributes to the team's results on the field.

**What winners actually had** [C]: 946 wins / 649 distinct teams · median winner rank **18.2%** ·
**69.6%** one-time winners · **24.1%** of wins to 3+-time winners · **15.6%** of bottom-half machine wins.
Top repeat winners: 3937 (7), 5895 (7), 1942 (6), 231 (6).

`TJT` is unusually candid that this award is hard to spot from the stands [C]. Paraphrase: observers are
told the award is hard to see in match play and that their best guide is instinct about which machines
look well built. The vetting step is stricter, calling for "**little to no failures on the field**"
(`TJT`, Technical Judges Tip Sheet, Rev. Oct 2025, Quality Award).

**Read that as an instruction.** The award is decided by (a) gut impression of workmanship in the pit and
(b) whether you break during matches. Both are controllable by a small team without money.

**Artifacts that win it**

| Artifact | Spec |
|---|---|
| **The written quality plan** | **One page.** The criterion literally says "describe their quality plan" — most teams have no document called this. Having one titled *Quality Plan* is disproportionately effective. Sections: fastener standard, wire routing standard, pre-match checklist, spares inventory, known-risk list + mitigation. |
| **Match-by-match failure log** | A table: match #, issue, root cause, fix, minutes. Even mostly-empty it proves the practice. Directly evidences "maintaining functionality". |
| **Wiring / labelling photo set** | 4–6 close-ups: labelled harness, strain relief, connector retention, serviceable battery mount. This is the "workmanship … wiring" clause made visible. |
| **Designed-in redundancy callout** | One physical example you can point at — a doubled fastener, a backup sensor, a hard stop. The word *redundancy* is in the criteria and almost nobody addresses it. |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | Name the lane | "We'd like to walk you through our quality plan." Hand them the one-pager. |
| 0:30–1:30 | Standards | "Every fastener is \<standard\>, every wire is \<gauge/colour rule\>, every connector is retained by \<method\>." Point at three examples on the robot. |
| 1:30–2:30 | Redundancy + risk | "We identified \<N\> failure risks. Here's the one we were most worried about and the redundancy we designed in." |
| 2:30–3:30 | **The log** | "We've played \<N\> matches. Here's every issue we've had and how long each took to fix." Hand over the log. |
| 3:30–4:30 | Serviceability | Demonstrate one fast service action — battery swap, module removal — with a stopwatch claim. |
| 4:30–5:00 | Field tie-in | "That's why we haven't missed a match." (Only if true. Match Observers will check.) |

**DESIGN SIGNAL** — *if your robot is visibly finished — consistent fasteners, routed and labelled wiring,
no zip-tie archaeology — and you can produce a written failure log showing near-zero match losses, Quality
becomes a live target. It rewards discipline rather than budget, which makes it the best fit for a small
team that builds carefully.*

**Cost: 20–35 student-hours.** Owner: `BUILD_LEAD`.
Quality plan 4–6 h · photo set 3–5 h · failure log ~10 min/match, so 5–10 h/season · rehearsal 4–8 h.
**Highest ratio of award-probability to hours of any machine award**, because the failure log is an
operational good you should keep regardless.

---

### 3.3 Industrial Design Award — the whole-machine award

**Published criteria** (`MAW`, `AW`) [C]:

> "**The entire machine, and not just a single component**, or the detailed process used to develop the
> design, is worthy of this recognition." (Industrial Design Award guidelines, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** the machine applies industrial design principles and balances form, function and
  appearance.
- The team can explain why the design is elegant, efficient (simple to build and run) and practical.
- The robot stands out from the others on appearance, design and performance.

**What winners actually had** [C]: 937 wins / 604 distinct teams · median winner rank **17.5%** ·
68.0% one-time · 31.8% to 3+-time winners · 15.0% of bottom-half machine wins.
Top repeat winners: 1768 (7), 125 (7), 6417 (7), 6800 (6).

`TJT` [C]: observers look for robots with *"an overall polished/elegant look"* (`TJT` Rev. Oct 2025,
Industrial Design Award). Paraphrase of the rest: the award favors an efficiently designed machine whose
components were designed to work together as one system.

**The distinguishing clause is "the entire machine, and not just a single component."** This is the exact
inverse of Creativity. Pitching one clever mechanism here actively disqualifies your framing.

**Artifacts that win it**

| Artifact | Spec |
|---|---|
| **Full-robot CAD render beside the finished robot** | Printed A3, same camera angle as the real machine. The single most effective Industrial Design artifact: it proves the whole machine was designed, not accreted. |
| **Packaging cutaway / section view** | A CAD section showing how subsystems nest. Evidences "components work together seamlessly". |
| **Design-language one-pager** | The 3–4 rules you applied everywhere: one fastener family, one bracket motif, one colourway, one wire-routing convention. |
| **Before/after packaging pair** | Two renders showing a volume you reclaimed. Evidences "efficient (simple/executable)". |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | Name the lane | "We'd like to talk about the machine as a whole rather than any one mechanism." |
| 0:30–1:30 | The rules | Design-language one-pager: "We applied these four rules to every subsystem." Point at the same motif in three places. |
| 1:30–2:30 | Packaging | Render vs robot, side by side. "Everything sits inside this envelope. Here's the section view." |
| 2:30–3:30 | Elegance = simplicity | "This subsystem started at 14 parts and ships at 6." Name what you deleted. |
| 3:30–4:30 | Practicality | Serviceability and manufacturability: "Every part on this robot can be made on the two machines we own." |
| 4:30–5:00 | Aesthetic intent | "We chose \<finish/colour\> because \<reason\>." Aesthetics is in the criteria — say it out loud. |

**DESIGN SIGNAL** — *if a stranger can look at your whole robot and see one consistent design language —
repeated bracket motifs, one fastener family, deliberate finish, no visible improvisation — and you have a
full-robot CAD model that matches what you built, Industrial Design becomes a live target. If your robot
is one brilliant mechanism bolted to an improvised frame, pitch Creativity instead.*

**Cost: 25–40 student-hours.** Owner: `DESIGN_DOC_OWNER`.
Full-robot CAD kept current 10–20 h (near-zero if you already CAD the whole robot; prohibitive if you
don't) · renders/section views 6–10 h · one-pager 3–5 h · rehearsal 4–6 h.
**Gated on whether you already CAD the entire robot.** If you do not, this is the most expensive lane on
the board and you should pick another.

---

### 3.4 Excellence in Engineering Award sponsored by Littelfuse — the process award

**Published criteria** (`MAW`, `AW`) [C]:

> "The engineering solution is functional, practical, and did not create new problems." (Excellence in
> Engineering Award guidelines, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** the machine includes an engineering solution whose components were designed to work
  together.
- The team can explain which game problems it identified and how the machine solves them. **A robot is not
  required to address every game challenge** (the exact sentence is quoted below).
- The team can walk through its engineering process and follow design elements from first concept to
  finished part.
- The solution contributes to the team's results on the field.

**What winners actually had** [C]: 940 wins / 569 distinct teams · median winner rank **15.4%** ·
65.7% one-time · **38.7%** to 3+-time winners (second most dynastic) · 14.3% of bottom-half machine wins.
Top repeat winners: **341 Miss Daisy** (10), 1073 (7), 1325 (7), 6800 (7), 118 (7).

`TJT` is explicit that this one is invisible from the stands [C]:
> "Identifying Candidates — **N/A. This award is based primarily on process and thus cannot be identified
> well by observing robots.**"

**That is a strategic gift and a trap.** Gift: field performance cannot nominate you, so the pit interview
is the entire channel — a small team competes on equal terms. Trap: winners still have a median qual rank
of 15.4%, because the criteria demand the solution "contributes to the team's success on the field", and
`TJT` tells judges to verify the robot is effective.

The explicit permission — *"Teams do not have to design a robot that solves all game challenges"* — is the
single most small-team-friendly sentence in the entire award corpus. **A deliberately scoped robot that
does one job well is a valid Excellence in Engineering entry, provided the scoping decision is
documented as a decision.**

**Artifacts that win it**

| Artifact | Spec |
|---|---|
| **Design journal with dated decision points** | The core artifact. Not a build log — a *decision* log: date, decision, options considered, criteria, choice, who decided. 10–20 entries beats 200 pages of photos. |
| **Requirements → solution trace matrix** | One table: game requirement \| our design response \| how verified. Literally the "trace elements of the designs from conception through completion" clause. |
| **The scoping-decision page** | "We decided **not** to attempt \<task\>, on \<date\>, because \<analysis\>." Turns a small team's necessary limitation into documented engineering judgement. |
| **Iteration photo series** | One subsystem across 3–4 revisions with the reason for each change. |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | Name the lane | "We'd like to show you our engineering process." Open the journal to a tabbed page. |
| 0:30–1:30 | Problem selection | "We identified \<N\> problems in the game. We chose to solve these two and deliberately not that one — here's the analysis." |
| 1:30–3:00 | **Trace one decision end to end** | Pick ONE decision. Requirement → options → criteria → choice → part → test → match result. Judges want traceability; give one complete thread rather than five partial ones. |
| 3:00–4:00 | No new problems | "This solution didn't create new problems — we checked \<specific interaction\>." Addresses a clause almost nobody addresses. |
| 4:00–5:00 | Field contribution | Cite the match statistic the solution produced. |

**DESIGN SIGNAL** — *if you keep a dated decision log and can trace one requirement from the manual all
the way to a part on the robot and a number in a match, Excellence in Engineering becomes a live target —
and it is the only machine award where a deliberately narrow robot is an asset rather than an excuse,
provided the narrowing is documented as a decision rather than a shortfall.*

**Cost: 35–60 student-hours.** Owner: `DESIGN_DOC_OWNER` + mentor.
Journal ~1 h/week × 12 weeks = 12 h if maintained live, 40+ h if reconstructed · trace matrix 6–10 h ·
scoping page 2–3 h · iteration photos 4–6 h · rehearsal 6–10 h.
**Cost is entirely determined by whether you journal in real time.** Reconstructed journals read as
reconstructed. Start it in week 1 or do not pick this lane.

---

### 3.5 Innovation in Control Award sponsored by nVent — the controls award

**Published criteria** (`MAW`, `AW`) [C]:

> "Celebrates an innovative control system or application of control components - electrical, mechanical
> or software - to provide unique machine functions." (Innovation in Control Award description, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the guidelines:
- The team can describe its controls innovation and show how it was conceived, designed, built or deployed.
- The system itself is new and distinctive.
- It is tied into the machine, the human players and the game strategy, both in concept and in execution.
- It is practical, addresses the game challenge, and keeps working reliably under competition stress.

**What winners actually had** [C]: 941 wins / 612 distinct teams · median winner rank **17.6%** ·
68.6% one-time · 31.8% to 3+-time winners · 13.3% of bottom-half machine wins.
Top repeat winners: 230 (8), 1261 (7), **1690 Orbit** (7), 1701 (7), 686 (7).
Note 1690 Orbit also holds 6 Autonomous wins — controls strength converts across both lanes.

`TJT` draws the distinction from Autonomous explicitly [C]. Paraphrase: Autonomous rewards highly effective
autonomous actions, while this award rewards **inventive control solutions** that still work well on the
field. Observers are told to watch for mechanisms that move fast yet stay precisely controlled, since doing
both usually means sensors or a deliberate control strategy. The tip sheet also names a second route:

> **Innovative controllers:** "any team using an innovative device to control their robot (e.g., a
> custom-made replica of the robot's arm)" can be a candidate (`TJT`, Technical Judges Tip Sheet, Rev. Oct
> 2025, Innovation in Control Award).

**The "innovative controllers" clause is the underexploited path.** A custom operator interface is
cheap, buildable in the off-season, visible in the pit, and explicitly named in judge training. The
criteria also say "electrical, **mechanical** or software" — a purely mechanical control solution
qualifies.

**Artifacts that win it**

| Artifact | Spec |
|---|---|
| **Live bench demo of the loop closing** | The decisive artifact. A subsystem on a bench that visibly seeks and holds a setpoint when you disturb it by hand. Nothing else demonstrates "control" as fast. |
| **Plotted tuning data** | Step response before/after tuning, printed. This is what separates this award from a claim. |
| **Control block diagram** | One page, sensor → estimator → controller → actuator, with the actual part names. |
| **The custom operator console** | If you built one, it *is* the entry. Put it on the pit table with a sign. |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | Name the lane | "Can we show you a control loop closing?" |
| 0:30–1:30 | **Demo first** | Run the bench demo. Disturb it by hand. Let them watch it recover. Say nothing for 5 seconds. |
| 1:30–2:30 | The data | Hand over the step-response plot. "Before tuning, \<X\>. After, \<Y\>. Measured with \<method\>." |
| 2:30–3:30 | Why it's unique | "Most teams do \<standard approach\>. We do \<ours\> because \<reason\>." Uniqueness is an explicit criterion. |
| 3:30–4:30 | Integration | How it ties to driver, human player, strategy — the "integrated with the machine, human players, strategy" clause. |
| 4:30–5:00 | Reliability | "It has worked in \<N\> of \<M\> matches." |

**DESIGN SIGNAL** — *if you can put a subsystem on the pit table, disturb it by hand, and have a judge
watch it recover to setpoint — and you can hand them a plot of that behaviour — Innovation in Control
becomes a live target. If your controls story is "we tuned a PID" with no demo and no plot, it is not.*

**Cost: 30–55 student-hours.** Owner: `CONTROLS_OWNER` (1 student, needs real mentor support).
Bench demo rig 12–20 h · data collection/plotting 8–15 h · block diagram 3–5 h · rehearsal 6–10 h.
**Riskiest lane for a 15-student team**: it depends on one student's availability, and if that student is
also the drive-team programmer they will be unavailable exactly when judges circulate.

---

### 3.6 Autonomous Award sponsored by Google.org — **the one to avoid**

> Sponsor discrepancy [C]: `JM` Rev 2 (2/18/2026) calls this the *"Autonomous Award sponsored by Google
> DeepMind"*, while `MAW` and all 208 `TBA` 2026 rows say *Google.org*. Re-verify at kickoff.

**Published criteria** (`MAW`, `AW`) [C]:

> "**Consistent and reliable operation is weighted more heavily than the ability to score maximum points**
> during any specific autonomously managed actions." (Autonomous Award guidelines, [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards),
> entry updated December 18, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** the machine performs consistently, reliably and at a high level while acting on its own
  during matches. Judges evaluate how well it senses its surroundings, positions itself or its mechanisms,
  and carries out tasks.
- The team can explain how the robot senses the field, navigates or positions its mechanisms, and then
  performs its tasks.
- The team can name the factors it considered that could cause an autonomous action to fail.
- The team can describe the design, development and testing behind those actions.
- Judges may consider autonomous actions both at the start of the match and during teleop. (FIRST's
  guideline still names the first 15 seconds; `REB` 7.4.1 set the 2026 AUTO period at 20 seconds.)

**What winners actually had** [C] — the most extreme profile of any award:

| Metric | Value | Meaning |
|---|---:|---|
| Median winner qual rank | **9.0%** | the median winner is a **top-9%** team |
| Winners in qual top 8 | **80.4%** | four in five winners were a top-8 seed |
| Winners in bottom half | **4.9%** | essentially never |
| Wins by 3+-time winners | **44.6%** | **most dynastic award on the board** |
| One-time winners | 62.7% | lowest of any machine award |
| Share of bottom-half machine wins | **6.2%** | lowest of any machine award |

Top repeat winners: 1771 North Gwinnett Robotics (11), 7457 (9), 111 (7), 2056 (7), 5687 (7).

**Verdict for a ~15-student team: AVOID as a target.** Not because autonomous work is worthless — the
"weighted more heavily" clause genuinely rewards reliability over ambition, and a 2-note reliable auto is
a real strategic asset. But as an *award lane* it is the hardest to break into and the most
field-performance-gated. Build auto because it wins matches; do not spend award-prep hours on it.

**If you pursue it anyway** — artifacts: an auto success-rate table (routine × attempts × successes ×
failure mode), a field-relative path visualisation, a sensing explainer. Pitch: lead with the success
rate, not the point total, because the criteria explicitly weight consistency higher.

**DESIGN SIGNAL** — *if you run 3+ distinct autonomous routines with a measured success rate above ~85%
across a full event, and you can explain your sensing stack, Autonomous becomes a live target. Below that
bar it is not, regardless of preparation — 80.4% of winners were top-8 seeds.*

**Cost: 40–70 student-hours** for award materials alone, on top of the (much larger) cost of the autonomous
capability itself. Owner: `CONTROLS_OWNER`. **The worst hours-to-probability ratio on the board for a
small team.**

---

### 3.7 Imagery Award in honor of Jack Kamen — robot + brand integration

**Published criteria** (`TAW`, `AW`) [C]:

> "**The theme is incorporated into all aspects of the team, i.e. uniforms, pits, machine, mascot, etc.**"
> (Imagery Award guidelines, [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** named for Jack Kamen, Dean Kamen's father, in recognition of his art and illustration
  and his commitment to FIRST. It recognizes attractive engineering and a strong visual match between the
  machine and the team's appearance.
- The team can explain its theme and where the theme came from.
- The theme is original and suits the team's goals, character or history.
- Team and machine together make a striking, attractive visual.
- The theme is consistent with FIRST Core Values.

**What winners actually had** [C]: 936 wins / 577 distinct teams · median winner rank **48.7%** —
essentially **independent of field performance** · 66.6% one-time · 36.5% to 3+-time winners.
Top repeat winners: **6740 G3 – Glue Gun & Glitter** (10), 193 (10), 3182 (9), 5926 (8).

**This is the most field-independent robot-adjacent award on the board.** Median winner rank of 48.7%
means winning Imagery is uncorrelated with being good at the game — unlike every machine award
(15.4%–31.8%). For a small team that expects to finish mid-pack, Imagery and Judges' are the two
robot-adjacent awards where field results do not hold you back.

**The operative word is "integration."** The criteria list uniforms, pits, machine, mascot. A beautiful
robot with mismatched shirts and a bare pit does not win this; a coherent *system* does.

**Artifacts that win it**

| Artifact | Spec |
|---|---|
| **The theme origin one-pager** | "Describe its theme and its origins" is criterion #1 and the most commonly failed. Where the theme came from, why it fits your team's history, dated. |
| **Integration photo grid** | One page, 6 cells: robot, pit, uniform, mascot, buttons, banner — all visibly the same language. This *is* the award. |
| **Source art / livery drawings** | Original artwork proving originality, with the student artist named. |
| **Applied colourway on the robot** | Theme colours actually on the machine — powder coat, anodising, vinyl, printed panels. |

**5-minute pit pitch**

| Time | Beat | Content |
|---|---|---|
| 0:00–0:30 | Name the lane | "Can we tell you about our theme?" |
| 0:30–1:30 | **Origins** | Where it came from and why it fits this team specifically. Name the student. |
| 1:30–2:30 | Integration sweep | Physically point: robot → pit banner → your own shirt → mascot → buttons. Narrate the shared element. |
| 2:30–3:30 | On the machine | Show the theme executed on the robot itself, and how you did it within budget. |
| 3:30–4:30 | Originality | Show the source art. "This was drawn by \<student\>, not clip art." |
| 4:30–5:00 | Core Values tie | Why the theme is consistent with FIRST Core Values — an explicit criterion. |

**DESIGN SIGNAL** — *if your robot carries the same visual language as your pit, your shirts and your
mascot, and a student drew the source art, Imagery becomes a live target — and it is the robot-adjacent
award least affected by how you finish in quals (median winner rank 48.7%).*

**Cost: 20–40 student-hours.** Owner: `MEDIA_BRAND_OWNER` (1 student, ideally an art student — this is the
one lane that does not compete for build-team hours). Theme one-pager 3–5 h · photo grid 4–6 h ·
source art 8–20 h · applying livery 5–10 h.
**Best lane for a 15-student team with one artistically inclined member**, because it consumes no
mechanical or programming capacity.

---

### 3.8 Judges' Award — the one you cannot pitch

**Published criteria** (`TAW`, `AW`) [C]:

> "**Many judges have noticed and commented on** the positive aspects of the team." (Judges' Award
> guidelines, [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** at any point during the event, the judging panel may single out a team whose distinctive
  effort, performance or team dynamic deserves recognition.
- The team has taken FIRST's principles fully to heart.
- The team shows a positive quality that the criteria for the other awards do not cover.

`JM` adds a structural fact [C]: its exemption from Equitable Award Distribution covers only the
non-judged awards (Woodie Flowers Finalist, Volunteer of the Year, and match Finalists and Winners), which it
calls *"NOT a responsibility of the judges"* (`JM` Rev 2, 2/18/2026, *Non-Judged Awards*). The Judges'
Award is not on that list, so the one-award limit in §1.1 applies to it. (Corrected 2026-09-13: an earlier
version of this line misquoted that passage as exempting the Judges' Award.)

**What winners actually had** [C]: 953 wins / **787** distinct teams — the **most distinct winners of any
award** · median winner rank **50.0%** — perfectly field-independent · **83.0%** one-time winners ·
only **9.2%** of wins to 3+-time winners — **the least dynastic award in FRC**.

**This is the most statistically accessible judged award that exists.** It is also the only one with no
buildable artifact: the criterion is *"many judges have noticed"*, which is a breadth-of-exposure
condition, not a document condition.

**How it is actually won:** by being visibly, distinctively yourselves to *multiple* judges across two
days. The mechanism is coverage. `JM` notes judges are *"free to visit teams in the stands, practice
fields, or in queuing lines"*, and Match Observers feed impressions back — so every interaction is a
sampling opportunity.

**No pitch structure. Instead, the three behaviours that produce it:**

1. **Be findable.** `JM`: *"DO NOT skip a team just because they are not in their pit."* Judges will come
   back — but leave a note saying where you are and when you return.
2. **Have one true, unusual, non-award-shaped story** and let every student tell it the same way. The
   criterion is explicitly *"not addressed in the criteria for other awards"*.
3. **Be memorable to many, not impressive to one.** Breadth beats depth here, uniquely.

**DESIGN SIGNAL** — *there isn't one. This award is uncorrelated with robot properties (median winner rank
50.0%) and is the residual category by construction. Do not allocate hours to it; allocate* behaviour *to
it. For a 15-student team it is the highest-probability judged award on the board and costs zero prep
hours — treat it as the free option that rides along with every other lane.*

**Cost: 0 dedicated student-hours.** Owner: `PIT_LEAD` (behaviour, not artifact).

---

### 3.9 Rookie All-Star Award — rookies only, worth 8 points

**Published criteria** (`TAW`, `AW`) [C]:

> "This team seems like a '**FIRST Impact Award team in the making**.'" (Rookie All-Star Award guidelines,
> [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards), entry
> updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** a rookie team with a new but solid partnership that carries out the FIRST mission of
  getting students interested in science and technology.
- The Impact-in-the-making test covers community activity, leadership, vision and spirit.
- The school or organization and the sponsors work as genuine partners.
- The team understands what FIRST is for and sees technical work as fun, demanding and a path to a future.
- **The team has built a robot suited to the game's challenges** (the exact clause is quoted below).

Eligibility [C]: `AW` notes *"Any team with a team number of 10,900 or higher is eligible for this award"*
(the 2026 rookie threshold; the 2027 number will differ). `TAW` adds that a team may win it only **once
per level of competition**, and judges may decline to present it.

**What winners actually had** [C]: 680 wins / 574 distinct teams · median winner rank **66.7%** — winners
are typically in the **bottom third** of quals · **84.0%** one-time winners · only 6.2% to 3+-time winners.
Given at only **59.3%** of events — the least-offered award here, because many events have no rookies.

**Note the robot clause is deliberately weak**: *"a robot appropriate to the game's challenges"* — not
excellent, not competitive. **Appropriate.** Rookie All-Star is 80% a culture/partnership award with a
robot-adequacy gate. Worth **8 district points** (vs 5) and Championship-qualifying, so for an actual
rookie it is the highest-value target on the board — which is why `award_aim.py --rookie` promotes it.

**Artifacts:** a compressed Impact-award-style evidence set — sponsor partnership letter//logos with the
story of how the partnership formed, outreach photo log with dates and headcounts, a "why we started"
one-pager, and a robot that reliably does one scoring task.

**5-minute pit pitch:** 0:00–1:00 why the team exists and who started it · 1:00–2:00 the partnership
(school/organisation + sponsors, named) · 2:00–3:00 community activity with real numbers ·
3:00–4:00 the robot doing its one job, honestly scoped · 4:00–5:00 the 3-year vision.

**DESIGN SIGNAL** — *if this is your rookie year, build a robot that reliably completes one scoring task
and put every remaining hour into partnership and outreach evidence. The robot criterion is "appropriate",
not "competitive" — and the median winner finishes in the bottom third of quals.*

**Cost: 30–60 student-hours.** Owner: `PIT_LEAD`. **Not applicable to a veteran team** — if you are not a
rookie, this lane is closed and `award_aim.py` will reject it.

---

### 3.10 Rising All-Star Award — the young/rebuilt team's lane

**Published criteria** (`TAW`, `AW`) [C]:

> "This could be the result of being a new team, or a team with recent turnover in membership." (Rising
> All-Star Award description, [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards),
> entry updated October 2, 2025; same wording in `AW` Rev. Oct 2025)

Paraphrase of the rest of the description and guidelines:
- **Description:** recognizes a team that has kept going through challenges despite being young. Judges may
  decline to present it if no team at the event qualifies.
- The team understands the FIRST mission and shows Gracious Professionalism and Coopertition in its
  actions, both at home and at events.
- The team is a model for other young teams.
- The team looks sustainable, with a promising future in FIRST.
- **First-year status is not required.** A second- or third-year team that has grown substantially or
  come through setbacks can qualify.

**What winners actually had** [C]: 404 wins / 351 distinct teams · median winner rank **67.5%** ·
**87.2%** one-time winners · only **5.9%** to 3+-time winners — the **most open award measured**.
Offered at 75.8% of events; optional, so judges may skip it.

**Relevant to a ~15-student team with membership turnover** — the criteria explicitly cover *"recent
turnover in membership"*, not just rookies. If you lost a senior class and rebuilt, you qualify.

**Artifacts:** a turnover/growth narrative **with numbers** (members lost, gained, retained; skills
rebuilt), and a written succession plan — `AW` asks *"Do you have a succession plan? Can you describe
it?"* directly.

**DESIGN SIGNAL** — *no robot signal. If your roster turned over substantially in the last 1–2 seasons and
you can show numbers and a succession plan, this becomes live at 10–20 hours' cost. Do not claim youth you
do not have — judges cross-check against team age.*

**Cost: 10–20 student-hours.** Owner: `PIT_LEAD`. Cheapest lane on the board after Judges'.

---

## 4. Accessibility ranking for a ~15-student team

Two independent measures, computed this pass, ranking how open each award is to a team that is **not** a
field powerhouse. They agree.

| Award | Median winner qual rank | One-time winners | Wins by 3+-time winners | Openness rank |
|---|---:|---:|---:|---:|
| **Judges' Award** | 50.0% | **83.0%** | **9.2%** | **1** |
| **Rising All-Star** | 67.5% | **87.2%** | **5.9%** | **1** |
| **Rookie All-Star** (rookies only) | 66.7% | 84.0% | 6.2% | **1** |
| **Creativity** | **31.8%** | 76.3% | 16.1% | **2** |
| Quality | 18.2% | 69.6% | 24.1% | 3 |
| Innovation in Control | 17.6% | 68.6% | 31.8% | 5 |
| Industrial Design | 17.5% | 68.0% | 31.8% | 4 |
| Imagery | **48.7%** | 66.6% | 36.5% | 8 |
| Excellence in Engineering | 15.4% | 65.7% | 38.7% | 6 |
| **Autonomous** | **9.0%** | 62.7% | **44.6%** | **7 (hardest)** |

**Recommended allocation for ~15 students, ~90 student-hours of award prep:**

| Priority | Lane | Hours | Owner | Rationale |
|---|---|---:|---|---|
| 1 | **Creativity** | 25–45 | DESIGN_DOC_OWNER | Only machine award that survives a bottom-half finish (35.6% of such wins) |
| 2 | **Quality** *or* **Imagery** | 20–40 | BUILD_LEAD / MEDIA_BRAND_OWNER | Quality if you build cleanly; Imagery if you have an artist and expect mid-pack |
| 3 | **Judges'** | 0 | PIT_LEAD | Free option; highest raw accessibility |
| — | Autonomous, Excellence in Engineering | 0 | — | Worst hours-to-probability ratio unless you already journal / already run elite auto |

Remember §1.1: you can only win **one**. Two prepared lanes plus the free Judges' option is the
efficient frontier. A third prepared lane mostly buys overlap, not probability.

---

## 5. The shared artifact library — build once, use in three lanes

Most artifacts serve multiple awards. Sequence them by reuse, not by award.

| Artifact | Creativity | Quality | Ind. Design | Exc. Eng. | Innov. Control | Imagery | Hours |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| Dated build/decision photos | ● | ● | ● | ● | ● | ● | ~0 if habitual |
| Failure / match log | | ● | | ● | ● | | 5–10 |
| Full-robot CAD kept current | | | ● | ● | | | 10–20 |
| Origin-story board (1 mechanism) | ● | | | ● | ● | | 8–12 |
| The kept failed prototype | ● | ● | | ● | | | ~1 |
| Bench demo spare / rig | ● | | | | ● | | 8–20 |
| One-page written plan (quality / design language / theme) | | ● | ● | | | ● | 3–6 each |
| Integration photo grid | | | ● | | | ● | 4–6 |

### 5.1 The single highest-leverage habit
**Photograph every subsystem at every revision, with the date, from day one.** Six of eight artifacts
above are free byproducts if you do this and expensive reconstructions if you don't. This is the cheapest
award decision available to a 15-student team and it must be made in week 1, not week 6.

### 5.2 What FIRST says about handing judges paper [C]
> "**judges are not expected to review every piece of material** handed to them during the event" (`JM`
> Rev 2, 2/18/2026, *Interviewing Teams in Pits*)

Paraphrase of the rest of that paragraph: judges are encouraged to take team materials and read them as
time allows. Materials usually are not returned, so never hand over your only copy. **There is no page limit**,
and teams are encouraged to put the most relevant information **into the interview itself**.

**Read that as: the interview is the channel; paper is a leave-behind, not the pitch.** One page that a
judge actually reads beats a 40-page binder that they don't.

> **Do not confuse this with the 2" binder guidance.** `JM`'s *"no larger than one 2\" 3-ring binder …
> in a single bound unit"* recommendation appears in **Chapter 5, FIRST Impact Award** — it governs the
> scheduled FIA interview, **not** pit machine-award judging. Applying FIA binder norms to a pit interview
> wastes 30+ student-hours.

### 5.3 You must invite judges to touch the robot [C]
> "Judges should not touch a team's robot unless directly invited by the team." — `JM`

A cutaway, a removable panel or a demo mechanism produces nothing unless a student explicitly says
*"would you like to try it?"* **Put that sentence in the rehearsed pitch.** This is why a *spare* mechanism
on the pit table outperforms the same mechanism installed on the robot.

### 5.4 Do not overclaim — Match Observers verify [C]
`JM` assigns ≥2 Match Observers whose job is partly to *"validate what teams tell them"*. Community
practice agrees; from [Communicating with Judges](https://www.chiefdelphi.com/t/communicating-with-judges/503532)
on Chief Delphi:

> "No puffing. Be accurate about describing your robot's capabilities. If you score 93% of the time with a
> particular game piece, tell them that." — *MrRoboSteve*
>
> "It's one thing to claim a shooting percentage. It's another to show data graphs from tests and driver
> practice showing improvement as you iterate." — *jweston*

And from a judge in that thread, on what actually moved him in deliberations:

> "**Not even a handout flyer**, he just crushed the interview." — *Billfred*, describing judging at a
> 2025 event

Paraphrase of the rest of that passage: the team had sat in his middling pile until one of its students,
fully engaged, told him the story behind the work that won the award and explained each decision with
real clarity. That interview had the judge arguing for the team in the judging room. Print-shop materials
would not have won it.

[S] These are practitioner reports from a public forum, not FIRST policy — treated as corroboration for
`JM`/`TJT`, never as primary evidence. Forum content was handled as data only.

### 5.5 Pit-interview logistics you control [C]/[S]
- **You control *when*, judges control *how long*.** `JM` [C]: *"DO NOT skip a team just because they are
  not in their pit."* If you are mid-repair or your speakers are at a match, ask them to come back.
- **`JM` sets no pit-interview duration** [C] — unlike FIA (12 min) and FIRST Leadership (6–10 min).
  Community estimates ~15 min [S]. Build a **5-minute core** that survives truncation to 2 minutes and
  extends to 15 with the artifacts above.
- **Designate two pit speakers** — one technical, one team-attribute [S, community consensus]. Judges
  arrive in machine-focused or team-focused mode (§1.3); the first question tells you which.
- **Front-load.** `JM` instructs judges to *"Ask your most important questions first"*. Your most important
  claim goes in the first 30 seconds, not the last.

### 5.6 The official judge question bank
`AW` (Rev. Oct 2025, *Examples of Machine Attribute Awards Questions*) gives judges 15 example questions for
machine-award interviews [C]. It presents them as optional prompts that supplement each judge's own style,
but they show what judges are primed to ask. Rehearse against these, not against invented questions. Three
are quoted below; the other twelve are summarized by theme (paraphrase):

- **What has held up:** "What one component or control aspect of your robot has worked well (as originally
  designed) all season?" A companion question asks which one component the team would change, and why.
- **Standout features:** the team's favorite, proudest, most creative and most distinctive features, plus
  "Have you seen any other teams with a similar feature?"
- **Autonomy:** which functions run autonomously, and how well they have performed in matches.
- **Process and strategy:** the design process for this year's game, how the team decided what mattered
  most, and which features were built for a strategic advantage.
- **Upkeep and change:** the biggest maintenance problem of the season, and what has been adjusted or
  upgraded since match play began.
- **The close:** "FINAL QUESTION … Is there anything you would like to tell us about your robot that we
  didn't cover?"

**The final question is a gift.** It is scripted, it is asked nearly every time, and it is the one moment
you fully control. Have a rehearsed 30-second answer that names your chosen award lane in plain language.

---

## 6. Validation / dry-run

### 6.1 Method and reproducibility

`TBA` CSVs were built by a prior pass using TBA's **public, unauthenticated event pages**, not APIv3.
Verified this pass: `https://www.thebluealliance.com/api/v3/status` returns **HTTP 401** both with no key
and with a dummy key — APIv3 requires an `X-TBA-Auth-Key` mintable only from a TBA account, which this
harness does not have.

| Endpoint | Auth | Used |
|---|---|---|
| `https://www.thebluealliance.com/events/<YEAR>` | none | event keys per season |
| `https://www.thebluealliance.com/event/<EVENTKEY>` | none | awards + rankings + alliances |
| `https://www.thebluealliance.com/team/<TEAM>` | none | winner identity verification (§6.2) |
| `https://www.thebluealliance.com/api/v3/event/<KEY>/awards` | **X-TBA-Auth-Key required** | **not used — 401** |

To rebuild with the authenticated API once a key exists:
`curl -H "X-TBA-Auth-Key: $TBA_KEY" https://www.thebluealliance.com/api/v3/event/2026necmp/awards`

**Name normalisation** was the main correctness risk and it bit twice during this pass. Award strings
carry sponsor suffixes and level prefixes that must be stripped before aggregation:
`District|Regional|District Championship|Championship` prefixes, and the suffixes
`sponsored by Google.org|Ford|Rockwell Automation|Littelfuse|nVent|Dow|SpaceX|General Motors` and
`in honor of Jack Kamen`.

Two bugs were caught and fixed by cross-checking against the prior pass's independently-computed totals:

| Bug | Symptom | Fix |
|---|---|---|
| `sponsored by General Motors` unstripped (726 rows) | Industrial Design totalled 187 instead of 937 | added to suffix list |
| `sponsored by Ford` unstripped (341 rows) | Autonomous totalled 598 instead of 939 | added to suffix list |

**Post-fix cross-validation** — all 15 normalised totals reproduce the prior pass's independently derived
figures exactly:

```
Industrial Design 937 · Quality 946 · Excellence in Engineering 940 · Creativity 938
Innovation in Control 941 · Autonomous 939 · Imagery 936 · Judges' 953 · Rookie All-Star 680
Team Spirit 943 · Gracious Professionalism 949 · Team Sustainability 773
Engineering Inspiration 946 · FIRST Impact 769
```

### 6.2 Back-test 1 — the one-award-per-event rule holds at 99.992%

FIRST's stated policy (`JM`): *"Do not award the same team more than 1 judged award at a single event."*
Tested against 5 seasons of independent event results:

| Judged awards won by one team at one event | Team-events | Share |
|---|---:|---:|
| Exactly 1 | **12,992** | 99.992% |
| 2 | **1** | 0.008% |
| 3+ | 0 | 0% |

The lone exception is 2022mxmo team 6832 (Judges' + Team Spirit). Pairwise co-occurrence across all six
machine awards is **0.00%** in every cell. **A published policy reproduced by an independent data source
at four nines — this is the most reliable fact in this document, and §1.1 rests on it.**

### 6.3 Back-test 2 — does the targeting advice match what low-ranked teams actually win?

The recommendation in §4 (Creativity first, Autonomous never) was derived from concentration and median-rank
statistics. This is an **independent** test using a different cut: take only teams finishing in the
**bottom half of quals**, and ask which machine awards they actually won.

| Machine award | Share of bottom-half machine-award wins | §4 recommendation |
|---|---:|---|
| **Creativity** | **35.6%** | **Priority 1** ✓ |
| Quality | 15.6% | Priority 2 ✓ |
| Industrial Design | 15.0% | Secondary ✓ |
| Excellence in Engineering | 14.3% | Deprioritised ✓ |
| Innovation in Control | 13.3% | Opportunistic ✓ |
| **Autonomous** | **6.2%** | **Avoid** ✓ |

Creativity outperforms the next award by 2.3×, and Autonomous is last. **The ranking derived from
openness metrics is reproduced by the raw win distribution of exactly the population this document is
written for.** The instrument agrees with itself across two independent derivations.

Full judged-award distribution by qualification band, confirming the culture/rookie lanes dominate at the
bottom and machine awards dominate at the top:

| Qual band | n | Top 3 judged awards won |
|---|---:|---|
| Top 25% | 5,487 | Autonomous 14.3% · Excellence in Eng. 11.6% · Innovation in Control 11.0% |
| 25–50% | 3,310 | Gracious Prof. 9.1% · Team Spirit 8.8% · Imagery 8.7% |
| 50–75% | 2,282 | Team Spirit 11.6% · Imagery 11.4% · Judges' 10.9% |
| Bottom 25% | 1,763 | Rookie All-Star 13.8% · Team Spirit 12.8% · Judges' 12.7% |

### 6.4 Back-test 3 — tool regression tests

`award_aim.py` was run against five scenarios on 2026-08-22. Two genuine defects were found and fixed:

| Test | Expected | Result |
|---|---|---|
| Novel mechanism + clean build, 80 h budget | Creativity #1, Quality #2, flags over-budget | **pass** |
| Controls-heavy, 120 h | Innovation in Control #1, Excellence in Eng. #2, within budget | **pass** |
| `--rookie` | Rookie All-Star promoted to #1, labelled PRIMARY (rookie) | **fail → fixed** (was down-weighted to AVOID and out-ranked) |
| No signals declared | Only signal-free awards (Judges', Rising All-Star) offered | **pass** |
| Retired-award leakage | Safety / Media & Technology never recommended | **fail → fixed** (retired rows were being scored; now filtered on `status_2026 == active`) |

The retired-award leak was the more serious: without the fix the tool could have recommended building
materials for an award that has not existed since 2021.

### 6.5 Back-test 4 — the retired-award claim

The task brief named Safety and Media & Technology as candidate targets. Four independent sources agree
they are dead in FRC:

| Check | Safety Award | Media & Technology Innovation |
|---|---|---|
| Mentions in `RAPD`/`CHRG`/`CRES`/`REEF`/`REB` | **0** | **0** |
| Rows in `TBA` 2022–2026 | 3, all offseason custom names | **0** |
| Present in `JM` Ch.4 judged-award list | no | no |
| Present on `MAW` / `TAW` | no | no |

Corroborated by [FIRST Robotics Wiki — Industrial Safety Award](https://first-robotics.fandom.com/wiki/Industrial_Safety_Award):
the Industrial Safety Award sponsored by UL was **removed for the 2022 season** [S — community wiki, not a
FIRST primary source; the four checks above are the primary evidence].

### 6.6 Back-test 5 — §0 step 5 against the dry-run manual

Step 5 (manual award-slate diff) was dry-run against
`manuals/2026-27_BIOCORE/ingest_DRYRUN_.../full_layout.txt`, which is a **REBUILT** manual ingested under
the BIOCORE path. The correct answer is therefore **empty output** — REBUILT introduces no award unknown
to the 2026 baseline. Getting there required tightening the extractor twice:

| Regex | False positives on the dry-run | Cause |
|---|---:|---|
| `[A-Z][A-Za-z' ]{3,40} Award` (first attempt) | **14** | allows lowercase words, so it swallows sentence fragments ("Any team who wins the FIRST Impact Award", "At the Award") |
| `([A-Z][A-Za-z']{1,20} )+Award` (each word Title Case) | **3** | `District FIRST Impact Award`, `The Woodie Flowers Award`, `Star Award` (a line-break split of "Rookie All Star Award") |
| + strip level prefixes/articles, drop known line-break fragments | **0** ✓ | shipped in §0 |

**Result: 0 false positives, correct empty output.** On kickoff day a non-empty result is therefore
signal, not noise — which is the property that makes the check worth running.

---

## 7. Files written by this pass

| Path | Contents |
|---|---|
| `reference/awards/01_AWARD_WINNING_PATTERNS.md` | this document |
| `reference/awards/award_target_matrix.csv` | machine-readable companion: 13 award rows (10 live + 3 retired) with design signals, artifacts, pitch anchors, hours, owners, and the accessibility statistics |
| `reference/awards/award_aim.py` | kickoff-day award-target ranker; reads the matrix, filters retired awards, ranks lanes against declared robot signals and an hours budget |

Unmodified but depended on: `awards_baseline.txt`, `known_awards_2026.txt`, `award_diff.py`,
`fetch_award_pages.py`, `award_accessibility.csv`, `research/awards_tba/tba_awards_*.csv`.

---

## 8. Known limitations

- **Individual winners' robot features were not verified.** Winner *identities* and *win counts* are exact
  (verified against TBA team pages — 4907 Thunderstamps, 1771 North Gwinnett Robotics, 341 Miss Daisy,
  1690 Orbit, 6740 G3 – Glue Gun & Glitter). What those specific robots contained was **not** individually
  checked. The "what winners actually had" sections therefore characterise winners statistically and via
  `TJT`'s explicit judge-facing instructions, **not** by inspecting each winning machine. Do not cite this
  document as evidence that any named team's robot had any particular feature.
- **Student-hour estimates are [S].** They are calibrated to the artifact lists, not measured against real
  teams. Treat them as relative magnitudes (Creativity cheap, Autonomous expensive) rather than budgets.
  Track actuals in your first event and recalibrate the CSV.
- **`TBA` award names are event-reported.** Offseason events invent names (the count-1 entries in §2), and
  a handful of unindexed events may be missing entirely.
- **Rising All-Star counts cover fewer seasons.** The award appears in `TBA` only from 2025 (404 rows over
  two seasons), so its concentration statistics rest on a smaller base than the machine awards' five
  seasons. A prior-pass file reports 778 wins for this award; that figure could not be reproduced from the
  raw CSVs, which contain 404 — **prefer the figures in this document** and see §6.1 for the normalisation
  actually used.
- **Chief Delphi threads are [S] corroboration only.** Two threads were read as data. The Discourse JSON
  endpoint is slow from this harness; one thread was truncated to 25 posts. No forum claim is load-bearing.
- **The 2027 slate is not knowable yet.** Everything here is the **2026 baseline**. Award names churned in
  every season 2022→2026 and once *mid-season* (TU12, Feb 2026). §0 step 1 exists to detect that; run it
  before printing any award name onto a physical artifact.
- **Criteria are quoted only in short excerpts and otherwise paraphrased**, from the Rev Oct 2025 award
  pages and workbook (the `MAW` Autonomous entry is dated December 18, 2025) and the Rev 2 (2/18/2026)
  Judge Manual. Read the source pages for exact wording. `JM`
  already disagrees with `MAW` on the Autonomous sponsor (Google DeepMind vs Google.org). Re-pull both at
  kickoff rather than trusting the quotes here for exact naming.
- **Cosmetic bug in a depended-on tool.** On success `award_diff.py` prints *"no change — 00_AWARD_LIST_VERIFIED.md
  is still accurate"*, but no file of that name exists; the award list it refers to is
  `00_AWARD_LIST_EMPIRICAL_2026.md`. The exit code (0 = unchanged, 1 = drift) is correct and is what §0
  step 1 relies on — trust the exit code, ignore the filename in the message.
- **District points assume a district.** All point values are `REB` Table 11-1 district points. At
  Regionals, judged awards carry no equivalent points, so the §4 ranking is driven purely by win
  probability there — which does not change the recommended order.

---

## 9. Security note

Nothing in the Judge Manual, Award Workbook, Technical Judges Tip Sheet, FIRST award webpages, REBUILT
Team Update 12, TBA records, or the two Chief Delphi threads inspected for this pass contained text
addressed to an AI assistant or any attempt to issue instructions. All content was treated as data.
