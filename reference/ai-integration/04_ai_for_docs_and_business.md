# 04 — AI for Documentation, Awards, Business & the Team Knowledge Base

**Purpose:** turn FIRST's permissive AI policy into a *working system* for the non-robot half of the
season. This file covers everything AI touches that is **not robot code** — build-thread and design
documentation, award submissions, sponsor and grant work, outreach media, and the team knowledge base
that makes all of it repeatable after the seniors graduate. It is written for **~15 students, one
experienced technical mentor, a $2,500 robot budget and 44.9 in-season hours for awards+business**.
The whole design goal is: *match championship-team paper deliverables with a tenth of the labour, and
spend the hours you save on the robot and the driver.*

**Companion file:** [`templates/docs-business-prompts.md`](templates/docs-business-prompts.md) — 30
copy-paste prompt templates keyed to the section numbers here. Every workflow below names its template.

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source held in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior seasons / published team practice; not stated for BIOCORE |
| **[S]** SPECULATION | Inference — hour estimates, workflow yields, ROI claims. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked against a primary source |

**Source shorthand**

`AIP` = [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) — **the only authority in
this project for what FIRST permits.** This file does not re-litigate it. ·
`BIZ` = [`../team-ops/05_business_awards_sustainability.md`](../team-ops/05_business_awards_sustainability.md)
— the authority for award mechanics, grant deadlines, sponsorship and budget tiers ·
`AV` = [`../awards/00_AWARD_LIST_VERIFIED.md`](../awards/00_AWARD_LIST_VERIFIED.md) — **the only
authority for award names** ·
`AA` = [`../awards/AWARD-ALIGNMENT.md`](../awards/AWARD-ALIGNMENT.md) + `award_alignment_matrix.yaml`
— which two awards each archetype chases, and the materials bill ·
`AP` = [`../awards/01_AWARD_WINNING_PATTERNS.md`](../awards/01_AWARD_WINNING_PATTERNS.md) — per-award
dossiers and the accessibility ranking ·
`CM` = [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml)
— **the hours/roles/budget authority. Every hour figure here is reconciled against it** ·
`PS` = [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md) — Systemcore /
WPILib 2027 ·
`IX` = [`../../INDEX.md`](../../INDEX.md) · `KP` = [`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md).

> **Scope guard.** BIOCORE presented by Haas is the **FRC** 2027 game; kickoff **2027-01-09 12:00 ET**.
> BIOBUZZ is the FTC sibling (kickoff 2026-09-12) — Pollen, StarterBots and Skill Builders are FTC
> things and appear nowhere in this file. **2027 replaces the roboRIO with Systemcore** (`PS` §0),
> which matters here because it invalidates most of the subsystem documentation and onboarding
> curriculum any team wrote before 2027 — including anything an AI model recalls from training data.
> Treat every AI statement about WPILib package names, dashboards, or `roboRIO` as **wrong until
> checked against `PS`**.

---

## 0. The 60-second workflow

Runnable today (2026-08-22). Creates the knowledge-base skeleton from §6, drops in the project
`CLAUDE.md`, prints the attribution line you must paste on every submission, and shows the hours you
actually have.

```bash
# Run from the repository root.

# --- 1. the knowledge base skeleton (idempotent; safe to re-run) --------------------
mkdir -p team-kb/{00_charter,01_season,02_subsystems,03_decisions,04_meetings,05_outreach,\
06_business,07_awards,08_onboarding,09_media,99_archive}
for d in team-kb/*/; do [ -f "$d/README.md" ] || echo "# $(basename "$d")" > "$d/README.md"; done
ls -d team-kb/*/

# --- 2. the attribution line -- paste verbatim, change nothing but the numbers ------
cat <<'ATTR'
  Award submissions / handouts:   "Essay created by Team <NNNN> and <MODEL NAME>."
  Code repositories (README):     "Portions of this codebase were created by Team <NNNN>
                                   with assistance from <MODEL NAME>."
  Source:  reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md  (FIRST's own example wording)
ATTR

# --- 3. how many hours does the paper half of the season actually get? --------------
python - <<'PY'
import datetime, yaml
c = yaml.safe_load(open("reference/team_capacity.yaml", encoding="utf-8"))
a = c["hours"]["allocation"]
print(f"  awards_business (kickoff -> Week 1 event) : {a['awards_business']:.1f} h   <- ALL of §3+§4+§5")
print(f"  strategy_rules                            : {a['strategy_rules']:.1f} h")
print(f"  effective build hours, total              : {c['hours']['effective_build_hours']:.0f} h")
print(f"  students {c['roster']['students']}, scheduled {c['roster']['scheduled_hours_per_week']} h/wk,"
      f" technical mentors {c['roster']['technical_mentors']}")
d = (datetime.date(2027,1,9) - datetime.date.today()).days
print(f"  days to kickoff: {d}  ({d/7:.0f} weeks of OFF-SEASON time, which is NOT in the 599 h model)")
PY

# --- 4. the deadlines that make this file urgent -----------------------------------
cat <<'DATES'
  2026-09-24  Kit & Kickoff selection opens          2026-11-12  Pre-Kickoff Virtual Kit Release
  2026-10-29  Award submission portal OPENS  <-- start drafting against the real form
  2026-11-17  Kit selection closes                   2026-11-21  BOM order-by
  2027-01-09  KICKOFF                                2027-02-04  Leadership + Woodie Flowers due
  2027-02-11  FIRST Impact Award due (3:00 p.m. ET)
DATES
```

Expected: eleven `team-kb/` directories, the attribution block, `awards_business: 44.9 h`, and a
day count. If step 3 errors, `reference/team_capacity.yaml` moved — fix the path, do not guess hours.

---

## 1. Rules first — what you are allowed to do

### 1.1 FIRST permits this. Quote, do not argue. [C]

`AIP` is authoritative for this project and quotes FIRST's position with its sources; this file does
not repeat the quotes. In short: FIRST permits AI for award submissions, handouts and robot code, and
treats it as a tool in the same class as CAD programs and 3D printers.

Three consequences, all from `AIP`:

1. **One binding obligation: attribution.** Teams must credit the AI they use and respect
   intellectual property rights and licenses. FIRST's own example: **"Essay created by Team XXXX and
   ChatGPT."**
2. **Judges may not penalize you.** Judges are told not to discredit a team, or rank it lower, simply
   for using AI.
3. **AI-detector output is not evidence.** FIRST tells judges that AI-detection sites are unreliable
   and must not be used to check a submission.

Do not spend a single student-hour debating whether this is allowed, and do not hide it. The cost of
compliance is one sentence; the cost of non-compliance is an integrity finding.

### 1.2 The layer FIRST does *not* cover — and it is the one that can actually hurt you

`AIP` §"What this policy does NOT do" names four gaps. Two of them are *your* problem to close, and
neither is a FIRST question:

**(a) Your school district's academic-integrity / AI policy.** FIRST governs *eligibility and
judging*. It has no authority over your school. District policies in 2025–26 typically fall into one
of four shapes, and they are usually **stricter than FIRST**:

| District policy shape | What it means for this file | Your move |
|---|---|---|
| Blanket prohibition on generative AI on school devices/networks | §2–§5 workflows cannot run in the shop | Run them on personal/mentor devices off the school network, or seek a written club exemption **before** the season |
| Permitted with disclosure | Everything here is fine as written | Adopt the §1.4 disclosure log; it satisfies both FIRST and the district with one artifact |
| Permitted for "process," prohibited for "product" | Outlining, critique and Q&A drills are fine; generated prose in a graded artifact is not | Robotics submissions are usually not graded coursework — **confirm in writing**, because an Impact essay that also gets turned in for an English credit is |
| Silent / no policy | The riskiest case. Silence is not permission | Get a one-paragraph written OK from the principal or activities director naming the club, the tools, and the disclosure practice. File it in `team-kb/00_charter/` |

**Action, this week `[S]`:** email the activities director one paragraph — what the tool is, that
FIRST explicitly permits it, that every submission carries an attribution line, that a disclosure log
exists. ~20 minutes. Do it before October 29 so nothing blocks the Impact draft.

**(b) Student learning.** Permission to use a tool is not permission to skip the thinking. The stated
purpose of this whole project is to move student hours *toward* hands-on work — not to remove
students from the intellectual work. §3.1 draws that line for awards specifically, and it is the most
important paragraph in this file.

**(c) Minors' data and vendor account terms.** `AIP` flags this as an **open item**: nothing in this
project covers minors' data or vendor terms of service. Concretely, and marked `[S]` because it
depends on the vendor you pick: most major AI services set a minimum account age (commonly 13 with
guardian consent, 18 without) and most retain conversation content by default. Two rules that cost
nothing:

- **Team accounts are mentor-owned.** Students use the mentor's or the team's account under
  supervision; students do not create personal accounts to do team work. This sidesteps the age-terms
  question entirely and keeps the disclosure log in one place.
- **Never paste student PII.** No full names of minors, no addresses, no birthdates, no grades, no
  medical or dietary info, no parent contact details. Use initials or roles ("Student A, drive team").
  This is also the FIRST video rule generalized — `BIZ` §2.4: *"Do not identify minors by full name."*

**(d) Safety-critical robot code** is out of scope here — see `PS`. `AIP`'s rule stands: human review
before anything actuates.

### 1.3 The allowed / disclose / never table

This is the operative table. Pin it in the shop and in `team-kb/00_charter/ai-policy.md`.

| | Activity | Why |
|---|---|---|
| ✅ **ALLOWED — no disclosure beyond the standing line** | Brainstorming award angles and outreach ideas | Idea generation is not a submitted artifact |
| ✅ | Outlining an essay the students then write | The words are theirs |
| ✅ | Structural critique of student-written prose ("does §3 answer the question asked?") | Editing, which mentors have always done |
| ✅ | Mock judge Q&A drills / interview practice | A rehearsal partner, not a submission |
| ✅ | Summarizing meeting notes into action items | Clerical |
| ✅ | Turning a student's rough build-thread notes into a clean post | Content is student-observed; see §2.1 |
| ✅ | Sponsor prospect research, grant discovery, deadline tracking | Desk work with zero judged content |
| ✅ | Budget modelling, inventory reconciliation, travel and calendar logistics | Clerical |
| ✅ | Drafting social captions, newsletter copy, website boilerplate | Marketing copy; still gets a human pass for accuracy |
| ✅ | Building and querying the team knowledge base (§6) | Retrieval over your own writing |
| ⚠️ **DISCLOSE — attribution line required, on the artifact itself** | Any award submission text that AI touched at any stage | `AIP`: FIRST requires credit for content generation |
| ⚠️ | Pit handouts, one-page robot summaries, judging binders | `AIP` names "handouts" explicitly |
| ⚠️ | Any published team writing — build thread, website, newsletter, press release | IP hygiene + it is the honest thing; costs one line |
| ⚠️ | Code committed to the team repo | `AIP` names code; put the line in the README (`PS`) |
| ⚠️ | Grant applications and sponsor letters | Not a FIRST requirement, but funders increasingly ask. Disclose proactively; several list it as a condition |
| ⛔ **NEVER** | Submitting AI prose as a student's own first-person account of their experience | The Impact essay and the Leadership Award nomination are *testimony*. Fabricated testimony is the one failure mode that is unrecoverable |
| ⛔ | Any invented number, date, program name, partner, outcome, hour count or attendance figure | Judges verify. `BIZ` §7: the documentation binder exists so judges can **check** shortlist claims |
| ⛔ | Woodie Flowers Finalist essay drafted by AI | It is explicitly a *student-written* nomination of a mentor (`BIZ` §1.3). Use AI to critique structure only, after a student draft exists |
| ⛔ | Student PII, minors' full names, health/dietary/contact data in any prompt | §1.2(c) |
| ⛔ | Sponsor-confidential info, unsigned agreement terms, school financial account details | Obvious, but it happens when someone pastes a whole spreadsheet |
| ⛔ | Auto-sending anything — email to a sponsor, a submission, a social post — without a named human approving the exact text | The failure is not the draft, it is the send |
| ⛔ | Trusting an AI-generated FRC rule, award name, deadline, part number, price or URL | §8.1. This is the #1 practical hazard in this file |

### 1.4 The disclosure log — one file, satisfies FIRST *and* the district

`team-kb/00_charter/ai-disclosure-log.md`, one row per artifact, appended when the artifact is
finalized. Two minutes each. `[S]` ~15 rows across a season ≈ **0.5 h total**.

```markdown
| Date | Artifact | Tool + version | How it was used | Human author(s) | Attribution line placed? |
|---|---|---|---|---|---|
| 2026-11-02 | Impact exec summary Q3 draft | <model, version> | Outline + 2 rounds structural critique; all prose student-written | A.R., J.K. | n/a (draft) |
| 2027-02-08 | Impact essay, final | <model, version> | Outline, critique, gap analysis vs criteria; students wrote and rewrote | A.R., J.K., mentor review | Yes — portal footer |
```

Why it is worth doing even though FIRST does not require a log: it converts an integrity question
into a documented process, it is *itself* evidence for the **Team Sustainability Award** (`BIZ` §1.4:
"Prosperity… identifies and manages risk"), and it is the artifact you hand a skeptical
administrator.

### 1.5 The standing attribution line

Put it in four places and never think about it again:

1. **Award submission portal** — last line of the essay field and of the exec-summary block that used AI.
2. **Repo `README.md`** — one line, alongside the license (`PS`).
3. **Pit handouts / one-pagers** — 6 pt footer.
4. **`team-kb/00_charter/ai-policy.md`** — the master copy, so a new student can find the wording.

Wording, straight from `AIP`'s example: **"Essay created by Team \<NNNN\> and \<model\>."** Do not
get creative. FIRST published the pattern; matching it exactly is the cheapest possible compliance.

---

## 2. Documentation — the highest-ROI AI use on the team

`BIZ` §3.1 settles the framing: **FRC has no engineering-notebook requirement.** There is no rubric,
no page limit, no award scored against a notebook. Do not port an FTC portfolio workflow into FRC.
What judges actually want (`BIZ` §3.2) is **verbal traceability** — students who can narrate a
decision history under questioning, backed by artifacts that jog memory and prove claims.

That reframes every workflow below. **You are not writing documents to be graded. You are building a
memory that lets 15 students answer hard questions in a pit.** AI is very good at exactly that job:
turning scattered, low-effort raw capture into retrievable structured memory.

### 2.1 Open Alliance build thread from meeting notes — the flagship workflow

`BIZ` §3.3: the Open Alliance build thread **is** your engineering notebook — chronological,
timestamped, public, forces weekly reflection, and generates external feedback while you write it.
One artifact, three uses (thread → pit binder highlights → one-page summary).

The bottleneck is never insight; it is the 45 minutes on a Sunday nobody has. Kill the bottleneck:

| Step | Who | Time | What |
|---|---|---|---|
| 1. Raw capture | Rotating student scribe | 0 min marginal | During the meeting: bullet dump into `team-kb/04_meetings/YYYY-MM-DD.md`. Ugly is fine. Include photos with filenames |
| 2. Draft | AI, template **P-01** | 3 min | Feed the week's notes + last week's post. Out: a build-thread post in the team's voice |
| 3. Fact pass | Student who did the work | 10 min | **Every number, part name, dimension and outcome gets checked.** Delete what nobody can vouch for |
| 4. Voice pass | Same student | 5 min | Add the thing the AI could not know: what actually went wrong, what surprised you |
| 5. Post + attribution | Student | 2 min | Post; standing line in the footer |

`[S]` **~20 min/week vs ~60–75 min/week hand-written. Over a 7-week build that is ~5 h saved**, out
of an `awards_business` budget of **44.9 h** (`CM`) — roughly 11% of the entire paper budget, bought
back for the price of one student typing bullets during a meeting they were already in.

**The failure mode to design against:** a build thread that reads like a press release. Open Alliance
readers reward candor — "we snapped three belts before we found the pulley was 0.5 mm undersized" is
worth ten paragraphs of "the team iterated successfully." Step 4 exists specifically to put the
failures back in. Template **P-01** instructs the model to leave `[WHAT WENT WRONG?]` placeholders it
cannot fill.

### 2.2 Design-decision records (DDRs) and trade studies

The single artifact that most directly wins **Excellence in Engineering** (`AP` §3.4) and
**Creativity** (`AP` §3.1), because the Award Workbook verb is literally *trace* — *"can trace
elements of the designs from conception through completion."*

One markdown file per real decision, in `team-kb/03_decisions/`, named
`NNN-short-slug.md` (`003-intake-roller-vs-claw.md`). Fixed skeleton so AI can both write and
retrieve it:

```markdown
# DDR-003 — Intake: compliant roller vs. two-finger claw
Date: 2027-01-14   Status: DECIDED   Owner: <student>   Supersedes: —
## Context        (what the game/robot forced this decision; link the manual rule number)
## Options        (2-4, each with: cost from reference/bom/, build hours, tooling level, risk)
## Decision       (one sentence, active voice)
## Rationale      (why, in terms of the capacity model -- hours, budget, tooling, motor count)
## Consequences   (what this now forecloses; what it obligates)
## Evidence       (test data, CAD link, photo, match video timestamp)
## Revisit-if     (the trigger that would reopen this)
```

AI's job (template **P-02**): the student says what happened in 60 seconds of voice-to-text or
bullets; the model produces the structured record with `[UNVERIFIED]` on every claim it inferred. The
student clears the flags. **~8 min per DDR `[S]`**, versus ~30 min unassisted — and unassisted the
honest baseline is that most DDRs never get written at all.

Trade studies (template **P-03**) are DDRs with a scored matrix. Feed it
[`../bom/mechanism_catalog.yaml`](../bom/mechanism_catalog.yaml) and `team_capacity.yaml` and make
the model score options against **your real gates** — `budget_cap_usd: 2500`,
`build_hours_cap: 129.8`, `design_hours_cap: 74.9`, `programming_hours_cap: 134.8`,
`tooling_level: bandsaw_drillpress`, `novel_mechanisms_cap: 2`. A trade study that ignores your
tooling level is fiction. Then verify with `tools/bom-builder.py`, which enforces the same gates —
**never let the model's arithmetic stand in for the tool's.**

**Target volume `[S]`: 8–12 DDRs across the season.** More than ~15 and students stop writing them;
fewer than ~6 and the pit interview has nothing to trace.

### 2.3 Subsystem documentation generated from code + CAD

The pit-binder subsystem one-pagers (`BIZ` §3.3) are the second-highest-ROI paper artifact after the
one-page robot summary. They are also the most mechanical to produce, because **the source of truth
already exists in your repo**.

Workflow (template **P-04**): point the model at the subsystem's source file(s) and its DDRs, and ask
for a one-page summary with: purpose, actuators + controllers, sensors, control strategy, key
constants and *what they physically mean*, failure modes, and the 60-second pit explanation a student
would say out loud. Then a student edits.

**Systemcore caveat, and it is severe.** `PS` §0: Java packages move `edu.wpi.first` → `org.wpilib`,
C++ `frc::` → `wpi::`, NetworkTables v3 removed, Shuffleboard / SmartDashboard / PathWeaver /
RobotBuilder / LabVIEW **all removed**, Java 25 / C++23 required. A model's training data is
overwhelmingly pre-2027 roboRIO-era code. It will confidently emit `edu.wpi.first` imports, reference
Shuffleboard tabs that do not exist, and describe a roboRIO you do not own.

> **Rule: any AI-produced sentence about the control system is UNVERIFIED until checked against
> `PS`.** Generate documentation *from your actual source files*, never from the model's memory of
> how FRC code "usually" looks. If the model cites a class you cannot find in your repo, it is
> hallucinating. This is also why your 2027 docs are a genuine competitive asset: nearly every
> team's subsystem documentation is about to be invalidated at once.

### 2.4 Meeting minutes → action items

The cheapest win in this file. Raw bullets in, out comes: decisions made, **action items with an owner
and a date**, open questions, and anything that should become a DDR. Template **P-05**.

Rules that make it work:
- **Owner is a real name, never "the team."** An action item without a name is a wish.
- The model must output `UNASSIGNED — needs owner` rather than inventing one.
- Action items append to a single rolling `team-kb/04_meetings/ACTIONS.md` so nothing is buried in a
  dated file nobody reopens.
- `[S]` ~3 min per meeting. At ~3 meetings/week × 22 weeks ≈ **3.3 h of clerical work removed**.

### 2.5 Onboarding curriculum

`[H]` The predictable small-team death spiral: the two students who know how to do everything
graduate, and the following September the team rebuilds from zero. A written curriculum is the cheap
insurance, and it is also direct evidence for the **Team Sustainability Award** ("People — recruit,
train and retain students") and the **Rising All-Star Award**, which `AP` ranks **#1 most accessible
for a ~15-student team** and whose criteria explicitly cover *"recent turnover in membership."*

Build it as a lesson-per-file tree under `team-kb/08_onboarding/`, each file: objective → 20-minute
demo → hands-on exercise → "you are done when…" check → who to ask. Template **P-06** drafts a lesson
from an existing subsystem doc plus a DDR, which means **your documentation becomes your curriculum
for free**.

> **Time it for 2027 deliberately.** Because Systemcore invalidates the old stack (`PS`), a
> curriculum written against the roboRIO is already scrap. Write the software lessons **after** the
> November kit release and against WPILib 2027 only. Mechanical, electrical, safety, driving,
> scouting and business lessons have no such dependency — **write those now, in the off-season**,
> where the hours are free. This is the single best use of the ~20 weeks before kickoff.

### 2.6 Team handbook, safety plan, pit checklists

| Artifact | AI role | Human role | `[S]` hours saved |
|---|---|---|---|
| **Team handbook** (expectations, attendance, roles, code of conduct, travel rules) | Draft structure and boilerplate from your bullets; keep it under 8 pages | Mentor + captains own every policy sentence; school admin reviews conduct/travel | ~4 h |
| **Safety plan** | Draft the shop rules, PPE matrix, tool-authorization list, incident procedure | **Mentor owns this absolutely.** Note: there is **no longer a Safety Award** in FRC (`BIZ` §1.2) — you write this because it is right and because your school requires it, not for points | ~2 h |
| **Pit checklists** (pre-match, post-match, end-of-day, load-out, spares) | Generate from your BOM + subsystem docs; it will produce a good 80% skeleton | Drive team walks it physically once and cuts everything that does not survive contact | ~2 h |
| **Event-day run sheet** (call times, roles per match cycle, comms plan) | Draft from the event schedule | Whoever has actually run an event fixes the timings | ~1.5 h |

**Warning on the safety plan:** this is the one document where a plausible-sounding hallucination has
physical consequences. Do not let a model invent an OSHA citation, a chemical handling procedure, or
a fire-extinguisher class. Every safety line traces to your school's existing shop policy or a named
manufacturer document, or it gets deleted.

---

## 3. Awards — AI as editor and coach, never as ghostwriter

### 3.1 The line, stated once and precisely

`AIP` permits AI in award submissions. That is settled. The line below is **not** a FIRST rule — it is
this project's engineering judgment about what actually wins, and about what the activity is for.

> **The students supply the experience, the claims, the numbers and the voice. AI supplies structure,
> pressure and a second read.**

Why this is a *competitive* position and not just an ethical one — three reasons, all sourced:

1. **Judges pre-read your submission and then interrogate it in person.** `BIZ` §2.5: the Impact
   interview is *"12 minutes total,"* judges *"pre-read your submission before the event and meet to
   compare questions beforehand,"* and *"Judges will talk to the students, not to the mentors."*
   Three students, five minutes of Q&A, on a document they did not write, about experiences they did
   not have. That interview is where a ghostwritten essay dies, and it is unrecoverable.
2. **Match Observers cross-check claims.** `BIZ` §1.6: at least two judges per event watch matches
   and *"Pit judges should validate what teams tell them with the Match Observers."* An AI-smoothed
   overclaim about your autonomous is a verified falsehood by Saturday.
3. **The rubric is resource-normalized in your favour, and only if you are specific.** `BIZ`'s
   headline finding, from FIRST's own Impact judging guidelines: *"what did they accomplish with the
   resources available to them?"* Fluent generic prose is exactly what makes a small team look
   average. Your 15-student, one-mentor, $2,500-robot reality is an *asset* — but only stated
   plainly, with numbers a student can defend.

The practical test, and it fits on a sticky note:

> **If a judge asks "tell me more about this," can a student in the room answer for 90 seconds
> without the paper? If no, that sentence does not ship.**

### 3.2 The six sanctioned award workflows

| # | Workflow | Template | AI does | Student does | `[S]` h saved |
|---|---|---|---|---|---|
| A | **Criteria gap analysis** | **P-07** | Reads the published criteria (`AV`/`AP` dossiers) + your draft and lists which criterion is unevidenced | Fills gaps with real programs and numbers | 2.0 |
| B | **Outline from raw material** | **P-08** | Turns a pile of real activities into a 4–5 pillar structure with a controlling thesis | Picks the thesis; rejects pillars they can't defend | 1.5 |
| C | **Structural critique of student prose** | **P-09** | Marks vague verbs, unsupported claims, question-drift, repetition between essay and exec summaries | Rewrites. **Model never rewrites.** | 3.0 |
| D | **Character-budget surgery** | **P-10** | Cuts to exactly 500 / 10,000 chars without losing a claim; reports what it dropped | Approves each cut | 2.0 |
| E | **Mock judge Q&A** | **P-11** | Plays a hostile-but-fair judge from FIRST's published question bank (`AP` §5.6); 12-min timed drill | Answers out loud, alone, no notes | (adds ~3 h of practice — the highest-value 3 h in the lane) |
| F | **Feedback-loop triage** | **P-12** | Turns the ≤500-char judge feedback into a ranked change list for the *presentation* | Executes before the next event | 1.0 |

Total `[S]` ≈ **9.5 h saved** against the **44.9 h** `awards_business` line (`CM`) — with ~3 h
deliberately reinvested into Q&A drilling. Net ~6.5 h released to §4 and §5, or back to the robot.

### 3.3 Format discipline the model must be told about

Feed these constraints into every award prompt. They come from `BIZ` §2.1 / `AIP` and models will not
know them:

| Constraint | Value | Trap |
|---|---|---|
| Exec summary | **500 characters incl. spaces and punctuation** — ×13 questions | Models count *tokens or words*, not characters. **Always verify with a real character count**, e.g. `python -c "print(len(open('q3.txt',encoding='utf-8').read()))"` |
| Essay | **10,000 characters incl. spaces** | `BIZ` §2.3: every 2026 winner sampled used **95.5–99.9%** of the budget. An 8,000-char essay leaves 20% of your argument unspoken |
| Optional Q14 | 250 chars — *you* ask the judges a question they must answer in feedback | Free intelligence. Do not skip it. `BIZ` §2.6 lists FIRST's suggested wordings |
| Forbidden characters | Do **not** use `<` or `>` anywhere | `BIZ` §1.3: FIRST warns the submission may not save. Models love angle brackets — grep before pasting |
| Video | 16:9, 1–3 min, no copyrighted music, **first names only for minors**, hosted on Dropbox/Box/Google Drive with downloads enabled — **not YouTube/Vimeo** | `BIZ` §2.4. A model will suggest YouTube. It is wrong |
| Impact interview | 12 min hard cap: ≤7 presentation incl. setup, ≥5 Q&A, **max 3 students** | `BIZ` §2.5 |
| Leave-behind | ≤ one 2" 3-ring binder, single bound unit, ≤3 seasons | `BIZ` §2.5. Pit handouts have **no** page limit — different rule, routinely confused |
| Deadlines | Impact **2027-02-11 3 p.m. ET**; Leadership + Woodie Flowers **2027-02-04 3 p.m. ET**; portal opens **2026-10-29** | `BIZ` §1.3. Nothing can be altered after the deadline |

### 3.4 Which awards to point this at

Use `AA` for the pairing (one PRIMARY + one SECONDARY per archetype — you can win **exactly one
judged award per event**, `AP` §1.1) and `AP` for the per-award dossier. Award names come from `AV`
and **only** from `AV` — names churned in every season 2022→2026 and one was renamed mid-season in
2026. **Dean's List is now the FIRST Leadership Award.** Re-run `bash reference/awards/kickoff_award_check.sh`
on 2027-01-09 before printing anything, and never print a sponsor suffix until the 2027 award pages
re-issue.

Where AI helps most, ranked for a ~15-student team (ordering from `AP` §4):

| Award (name per `AV`) | AI leverage | Note |
|---|---|---|
| **Rising All-Star Award** | High — the narrative *is* your turnover/rebuild story, and it needs structure more than volume | `AP` ranks it #1 accessible; criteria explicitly cover recent membership turnover |
| **Team Sustainability Award** | **Highest** — the criteria are literally your business ops (People / Prosperity / Planet) | §4 and §6 generate this award's evidence as a byproduct |
| **FIRST Impact Award** | High on structure and gap analysis; **zero on substance** | The interview is the filter (§3.1). Also: no rookie eligibility |
| **Creativity Award** (Rockwell Automation) | Medium — DDR trail from §2.2 is the evidence | `AP` §3.1 calls it the small team's best robot award |
| **Excellence in Engineering** (Littelfuse) | Medium — same DDR trail; "trace conception → completion" | `AP` §3.4 |
| **Quality Award** | Low-medium — mostly a build-practice and test-log question | `AP` §3.2 |
| **Innovation in Control** (nVent) | Medium — but every claim rides on Systemcore code you must actually verify | `PS` |
| **FIRST Leadership Award** | Low — nomination is about one student's record | Structure critique only |
| **Woodie Flowers Finalist** | **None on drafting** | Explicitly student-written (`BIZ` §1.3). Critique after a student draft exists |

---

## 4. Business and admin — where the desk work actually lives

`BIZ` §5 is the authority for every figure below; this section is only about applying AI to it.

### 4.1 Sponsor prospect research

`BIZ` §5.6, quoting FIRST's Fundraising Guide, names the highest-yield channel plainly: *"a list of
parent, grandparent, mentor, and student employers."* Corporate matching and employee-directed giving
are the small-team unlock.

Workflow (template **P-13**): collect employers via a form (**employer name only — no student names in
the prompt**, §1.2c), then have the model produce a prospect table: company, plausible giving
vehicle, whether a matching-gift program is likely, in-kind angle, and a first-contact suggestion.
Then **a human verifies every company's actual program on the company's own site.** Models routinely
invent matching-gift programs and philanthropy contacts.

Weight in-kind heavily. `BIZ` §5.6: FIRST's own list includes laser cutting, waterjet, sheet metal,
hand tools, fastener stock, **leftover blank stock from local shops**, meals and hotel discounts. For
this team, converting part of a $2,500 robot budget into in-kind machining is often easier than
raising the cash — and it is the direct answer to a `tooling.level: bandsaw_drillpress` shop with
`outsourcing_budget_usd: 400` (`CM`).

### 4.2 Sponsor letters and stewardship

Draft with **P-14**; the model's real value is **variation at volume** — 20 tailored letters instead
of one generic one — plus never missing the retention loop. `BIZ` §5.6: *"It's more efficient and
effective to keep an existing sponsor year after year than find a new one,"* via three actions:
track what each sponsor gave each year, **report back the specific impact of their money**, and keep
year-round contact.

Build `team-kb/06_business/sponsors.yaml` (company, contact role, gift by year, cash/in-kind, tier,
benefits promised, last touch, next touch). A model can then generate the year-end impact report,
the renewal ask and the thank-you set from one file in minutes. **This single YAML is also your
Prosperity evidence for the Team Sustainability Award.**

Tiering per `BIZ` §5.6: 3–5 tiers; FIRST's worked example `$100–499 / $500–999 / $1,000–1,999 /
$2,000+`; best benefits reserved for the top tier; and *"Don't promise… if you can't follow through."*
Have the model check your tier sheet for promises your 15 students cannot actually staff.

### 4.3 Grant discovery and the Gene Haas Foundation

**Gene Haas Foundation — Haas is the BIOCORE title sponsor, so this one gets its own treatment.**
All of the following is from `BIZ` §5.5; the labels are load-bearing.

| Fact | Status |
|---|---|
| Relevant track: **"STUDENT COMPETITION TEAMS"** — *"grants are for approved competitions (FRC, FTC, SAE, etc.) in which students design and build a product that utilizes CNC machining"* | **[C]** primary source, [ghaasfoundation.org/apply-now](https://www.ghaasfoundation.org/apply-now), read 2026-08-21 |
| *"We will be accepting applications for the FIRST Robotics (FRC & FTC) 2026/2027 Competition Season after **May 1, 2026**."* — i.e. **the window is open now** | **[C]** same source |
| Foundation mission is explicitly CNC-focused: *"To introduce to and educate individuals for the field of manufacturing technologies specifically CNC machining"* | **[C]** same source |
| **Amount: $3,000 FRC / $2,000 FTC** | **UNVERIFIED** — secondary sources only; not published on ghaasfoundation.org. **Confirm in the portal before budgeting against it** |
| Restriction: funds may not be used for products Haas Automation makes or a Haas Factory Outlet sells | **UNVERIFIED** — secondary sources only |
| Deadline for the competition-teams track | **Not published.** `BIZ` §5.5 |
| **December 1** belongs to the *secondary-school CNC-training scholarship* track — **not yours** | **[C]** Third-party roundups conflate these. Do not plan around it |
| **June 30** belongs to the post-secondary scholarship track — **not yours** | **[C]** |

**Application strategy (`BIZ` §5.5):** the Foundation funds *CNC machining education*, not robotics
per se. Foreground how students develop machining skills, not your win-loss record. Haas CNC
certification pathways are precisely the Foundation's stated mission being executed. Separately, a
local **Haas Technical Education Center (HTEC)** or **Haas Factory Outlet** is a plausible in-kind
machining partner independent of the grant — which is exactly what a `bandsaw_drillpress`-level shop
needs. **Do not let AI write the machining narrative.** Have it interview *you* (template **P-15**)
and structure what you say.

**Live grant deadlines** (`BIZ` §5.4 — verify before relying on any of them):

| Grant | Deadline | Gate |
|---|---|---|
| BAE Systems FRC | **2026-09-13** | Within 75 mi of a BAE site, BAE mentor, **or Title 1 affiliation** |
| Boston Scientific FRC | **2026-09-30** | Within 60 mi of BSC locations (CA/IN/MA/MN) |
| Boeing Team Grant | **2026-10-16** | Boeing employee mentor or retiree |
| John Deere | **2026-11-06** | Deere community or employee mentor; **must not have already paid registration** |
| Arconic Foundation | Oct 31 (2025-26 cycle) | Arconic communities; $1,500 FRC |
| NASA Robotics Alliance | 2027 cycle not posted as of 2026-08-21 | Rookie / New Veteran / Year-Two only |

> **Process rule that costs you money if you miss it** (`BIZ` §5.4, FIRST's own wording): *"If there
> is a possibility you are receiving a grant, you must wait to pay until you receive instructions
> from FIRST."* John Deere explicitly disqualifies teams that already paid. **Registration payment
> opens Sept–Oct 2026. Do not pay while a decision is pending.**

**Boilerplate once, reuse everywhere (P-16).** `BIZ` §5.8: the same questions recur across nearly
every application. Draft short (~100 word) and long (~400 word) answers now, in the off-season, store
them in `team-kb/06_business/grant-boilerplate.md`, and have AI *tailor* rather than *write* each
application. `[S]` This is a **~6 h one-time investment that saves ~1.5 h per application** and
raises quality, because you are editing a considered answer instead of writing at 11 p.m. the night
before a deadline.

### 4.4 Budget modelling

`CM` sets the numbers this project scores against: `robot_discretionary: $2,500`,
`season_registration: $6,500`, `season_total_planning: $11,500`, `spares_consumables: $500`,
`sales_tax_rate: 0.07`, `outsourcing_budget_usd: $400`. `BIZ` §5.3 puts a lean-competitive program at
**$20,000–26,000** and notes the gap to a $100k+ program is *"mostly travel, roster size, and a
practice robot — none of which the Impact rubric rewards."*

AI's honest role here is **narrow**: scenario narration and sanity-checking, not arithmetic.

- ✅ "Given these line items, what breaks first if we add a second event?" — good.
- ✅ Reconciling a receipt pile into categories; drafting the budget narrative for a grant.
- ✅ Checking your budget against FIRST's own [Budget Template](https://www.firstinspires.org/hubfs/web/program/frc/resources/budget-template.xlsx) categories for missing lines.
- ⛔ **Doing the arithmetic.** Use `tools/bom-builder.py`, which enforces the real gates
  (`budget_cap_usd: 2500`, hours caps, `motor_cap: 12`, `tooling_level`). A model that "adds up" a
  BOM will be wrong in a way that looks right. Template **P-17** makes the model *call the tool* and
  interpret output rather than compute.

Also worth an AI pass: the fiscal-route decision (`BIZ` §5.6 — district account / FIRST Dashboard /
booster club / **fiscal sponsor**). For a small team with no booster club, `BIZ` concludes fiscal
sponsorship is usually right. Have the model build the comparison table *for your specific district*
from facts you supply — then a human confirms with the district finance office. **Never take an AI
statement about tax status, 501(c)(3) rules, or district financial policy as fact.**

### 4.5 Inventory, travel, calendar and roster ops

| Task | AI role | Guardrail |
|---|---|---|
| **Inventory** | Reconcile a photo/spreadsheet dump into `team-kb/06_business/inventory.yaml`; flag what the BOM needs that you do not have; compute order-by dates against `lead_time.order_by_safety_margin_weeks: 1` and the **2026-11-21 BOM order-by** | Part numbers and prices get verified against `reference/bom/` and the vendor site. **Models invent part numbers with total confidence** (§8.1) |
| **Travel logistics** | Draft itinerary, packing list, meal plan, chaperone ratios from your constraints; generate the parent info letter | Bookings and costs are human-verified. Never enter payment details or book anything |
| **Calendar** | Build the season calendar from the key dates in `IX`; generate reminder text; detect collisions with school exam weeks | The **2026-11-17** kit deadline and **2027-02-11** Impact deadline are hard stops — verify these against FIRST, not against a model |
| **Roster / hours** | Track participation hours for grant reporting and Impact Q1 | **Aggregate only.** Names never enter a prompt (§1.2c) |
| **Pit schedule** | Generate the match-cycle role rotation for 15 students so nobody is idle and nobody works 12 hours | Drive team overrides freely |

---

## 5. Outreach and media

`[H]` The trap: AI makes it trivial to produce *volume*, and volume is not what the Impact rubric
rewards. `BIZ`'s core finding is resource-normalization — *"what did they accomplish with the
resources available to them?"* Twenty generic posts are worth less than four with a real number and a
named outcome.

| Channel | AI role | Human role | `[S]` h saved |
|---|---|---|---|
| **Social captions** | 5 variants from one photo + one factual line; hashtag and sponsor-tag sets | Student picks; verifies every fact; posts. **Never auto-post** | 1.5 |
| **Website copy** | Team overview, sponsor page, join page, FAQ boilerplate | Accuracy pass; sponsor logos and names are legally sensitive — get them exactly right | 2.0 |
| **Newsletter** (monthly, to sponsors + parents) | Assemble from build-thread posts already written in §2.1 — **near-zero marginal cost** | 10-min read-through | 3.0 |
| **Sponsor impact report** (annual) | Generate from `sponsors.yaml` + outreach log | Mentor signs off on every claim | 2.0 |
| **Presentation decks** (school board, sponsor pitch, community demo) | Outline + speaker notes; the 12-min Impact deck timing structure | Students deliver. If they didn't write it, they can't answer questions on it | 2.5 |
| **Press releases / local media** | Draft + a pitch email to a named local outlet | Every name, number and quote verified. **Quotes must be real** — never let a model invent a quote attributed to a student, mentor or sponsor | 1.0 |

`[S]` ≈ **12 h** across a season. Two absolute rules: **(1)** minors are first-name-only in anything
public (`BIZ` §2.4 makes this explicit for video; generalize it); **(2)** a fabricated quote is the
media equivalent of a fabricated Impact claim.

---

## 6. The team knowledge base — the biggest structural advantage a small team can build

This section is the reason the file exists. Everything above is a workflow; this is the **asset**.

### 6.1 Why this beats every other AI investment

A powerhouse team's real advantage is not CNC or budget — it is **institutional memory**: fifteen
years of "we tried that in 2019 and here is why it failed," carried by a large multi-year roster and
a deep mentor bench. A 15-student team with one technical mentor (`CM`) loses ~4 students a year;
after three years, nobody in the room remembers the last three seasons.

**A structured, AI-retrievable knowledge base is how you buy that memory without the headcount.** It
is the one place where a small team can genuinely equal a large one, because the cost is disk space
and a five-minute daily habit rather than people. Concretely it means: a sophomore in 2029 can ask
"why did we go with a roller intake in 2027?" and get the DDR, the trade study, the test data, the
match video timestamp and the name of the student who built it.

Three additional returns, all documented in this corpus: it *is* the Team Sustainability Award's
People + Prosperity evidence (`BIZ` §1.4); it *is* the verbal-traceability substrate judges want
(`BIZ` §3.2); and it makes every prompt in §2–§5 dramatically better, because a model reasoning over
*your* files stops guessing.

### 6.2 The directory tree

Create it with §0 step 1. Plain markdown and YAML, in git, no database, no proprietary tool. This
matters: the format must survive a graduating senior, a lapsed subscription and a change of AI vendor.

```
team-kb/
├── CLAUDE.md                      # the entry point -- see §6.3. READ FIRST BY ANY AI
├── 00_charter/
│   ├── ai-policy.md               # §1.3 table + attribution line + district approval on file
│   ├── ai-disclosure-log.md       # §1.4
│   ├── team-handbook.md           # §2.6
│   ├── safety-plan.md             # §2.6 -- mentor-owned
│   └── roles.md                   # who owns what, this season and last
├── 01_season/
│   └── 2027-biocore/
│       ├── game-summary.md        # written kickoff day; rules that bind US, not all rules
│       ├── strategy.md            # output of STRATEGY-RANKING-SYSTEM.md
│       ├── rule-questions.md      # feeds reference/QA-AMBIGUITY-HOTSPOTS.md
│       └── retrospective.md       # WRITTEN IN APRIL. The highest-value file in the tree
├── 02_subsystems/
│   ├── drivetrain.md              # §2.3 -- generated from code + CAD, human-verified
│   ├── intake.md
│   ├── scoring.md
│   └── electrical.md
├── 03_decisions/                  # §2.2 -- DDR-001 ... DDR-0NN, append-only
├── 04_meetings/
│   ├── ACTIONS.md                 # single rolling action list, owner + date
│   └── 2027-01-12.md              # raw notes, one per meeting, ugly is fine
├── 05_outreach/
│   ├── events-log.yaml            # date, event, hours, students, audience reached, photos
│   └── partnerships.md
├── 06_business/
│   ├── sponsors.yaml              # §4.2 -- also the Sustainability Award evidence
│   ├── budget.yaml                # reconciled to reference/team_capacity.yaml
│   ├── grant-boilerplate.md       # §4.3
│   ├── grants-log.md              # applied / amount / outcome / feedback / reapply date
│   └── inventory.yaml
├── 07_awards/
│   ├── impact/                    # exec summaries by question number, essay drafts, video plan
│   ├── judge-feedback/            # the ≤500-char feedback, one file per event -- MINE THIS
│   └── pit-materials/             # one-page robot summary, subsystem one-pagers
├── 08_onboarding/                 # §2.5 -- lesson per file
├── 09_media/
│   └── photo-index.md             # filename -> date, subsystem, students (INITIALS ONLY), usable?
└── 99_archive/2026/               # last season, frozen. Never edited, only read
```

**Design rules that make it AI-retrievable — these are the part that matters:**

1. **Markdown and YAML only.** Not Google Docs, not a wiki, not Notion. A model can read a repo; it
   cannot reliably read your Drive, and neither can the next mentor.
2. **One decision, one file.** Retrieval works on file granularity. A 4,000-line "notes" doc is
   invisible.
3. **Predictable filenames.** `NNN-slug.md`, `YYYY-MM-DD.md`. Sortable, greppable, unambiguous.
4. **Every file opens with a metadata block** — date, owner, status. This is what lets a model tell a
   2027 decision from a 2026 one.
5. **Fixed skeletons per document type** (§2.2). Consistent headings mean a model can extract
   "all Decision fields across all DDRs" in one pass.
6. **Facts in YAML, judgment in markdown.** Sponsors, budget, inventory and outreach events are data
   — they belong in YAML where a script can compute on them without an AI in the loop at all.
7. **Never delete. Move to `99_archive/` and mark superseded.** "We tried and abandoned X" is the
   most valuable sentence in the tree.
8. **In git, pushed somewhere off the school network.** The knowledge base that lives on one student's
   laptop does not survive graduation.

### 6.3 The `CLAUDE.md` pattern

The single highest-leverage file in the tree. It sits at `team-kb/CLAUDE.md` and is the standing brief
any AI reads before doing anything — so students stop re-explaining the team in every conversation,
and so the model stops volunteering roboRIO advice. Keep it **under ~150 lines**; a bloated one gets
skimmed. Review it monthly and after kickoff.

```markdown
# CLAUDE.md — standing brief for AI working with FRC Team <NNNN>

## Who we are
- FRC Team <NNNN>. **15 students, 1 experienced technical mentor**, ~15 scheduled hours/week.
- Shop tooling: bandsaw + drill press + 1 FDM printer. **No mill, no lathe, no CNC router in house.**
  Mentor-supervised mill access only. Outsourcing budget ~$400, ~2 week lead time.
- Robot discretionary budget **$2,500**. Season planning total ~$11,500. We are a lean team by choice
  and by circumstance; FIRST's Impact rubric is resource-normalized and that is our advantage.
- Authority for all of the above: `reference/team_capacity.yaml`. **If you state an hours, budget or
  headcount number that contradicts that file, you are wrong. Re-read it.**

## The season
- **BIOCORE presented by Haas — the FRC 2027 game, FIRST CANOPY season. Kickoff 2027-01-09 12:00 ET.**
- **BIOBUZZ is FTC, not us.** Pollen, StarterBots and Skill Builders are FTC. Never attribute them to
  BIOCORE. If you are about to mention any of them, stop.
- **2027 replaces the roboRIO with Systemcore.** WPILib 2027 is a breaking rewrite: Java
  `edu.wpi.first` -> `org.wpilib`, C++ `frc::` -> `wpi::`, NetworkTables v3 removed, Shuffleboard /
  SmartDashboard / PathWeaver / RobotBuilder / LabVIEW removed, Java 25 / C++23 required.
  **Your training data is mostly pre-2027. Any control-system claim you make is UNVERIFIED until
  checked against `reference/team-ops/03_programming_stack.md`.**

## How to answer us
- Label every claim **[C] / [H] / [S] / UNVERIFIED**. We make budget decisions from your output.
- **Never invent a URL, price, part number, team number, repo path, product name, rule number, award
  name or deadline.** If you are not certain, write UNVERIFIED and say what you would check.
- Award names come from `reference/awards/00_AWARD_LIST_VERIFIED.md` only. Names churn every season;
  one was renamed mid-season in 2026. **Dean's List is now the FIRST Leadership Award.**
- Do not do BOM arithmetic. Call `tools/bom-builder.py`; it enforces our real gates.
- Prefer the shortest thing that works. We do not have the hours for elegance.

## Hard rules
- **No student PII in any prompt or output** — no full names of minors, addresses, birthdates, grades,
  health or contact info. Initials or roles only.
- **You do not write award submissions.** You outline, critique, run mock judge Q&A and find gaps.
  The students write the prose and own every claim. See `reference/ai-integration/04_ai_for_docs_and_business.md` §3.1.
- Every AI-assisted submission carries: **"Essay created by Team <NNNN> and <model>."**
- Nothing gets sent, posted or submitted without a named human approving the exact text.

## Where things live
- `team-kb/03_decisions/` DDRs · `team-kb/02_subsystems/` subsystem docs
- `team-kb/06_business/sponsors.yaml`, `budget.yaml`, `grant-boilerplate.md`
- `team-kb/07_awards/judge-feedback/` — read this before touching any award material
- `team-kb/01_season/2027-biocore/retrospective.md` — read this before proposing anything

## When you don't know
Say so. Name the file or the primary source that would settle it. A flagged gap costs us ten minutes;
a confident wrong number costs us a season.
```

Put a **short** `CLAUDE.md` in subdirectories that need local rules — e.g. `07_awards/CLAUDE.md`
carrying the character limits from §3.3 and the `<`/`>` ban, `06_business/CLAUDE.md` carrying the
"do not pay registration while a grant is pending" rule.

### 6.4 The capture protocol — what actually gets written down

The knowledge base fails one way: nobody writes to it. Make capture a **role**, not a virtue.

| Cadence | Who | Time | Output |
|---|---|---|---|
| **Every meeting** | Rotating scribe (a named role in `00_charter/roles.md`) | 0 marginal — they're already there | Raw bullets → `04_meetings/YYYY-MM-DD.md` |
| **End of meeting, last 5 min** | Scribe | 5 min | AI pass (P-05) → decisions, action items with owners, open questions appended to `ACTIONS.md` |
| **Every real decision** | Whoever made it | 8 min | DDR (P-02) |
| **Weekly** | Documentation lead | 20 min | Build-thread post (P-01); photo index updated |
| **Every outreach event** | Event lead | 5 min | Row in `05_outreach/events-log.yaml`: date, hours, students, audience count, photos |
| **Every sponsor touch** | Business lead | 2 min | Row in `sponsors.yaml` |
| **After every competition** | Whole team | 45 min | Judge feedback filed; `07_awards/judge-feedback/` mined (P-12) |
| **April, once** | Whole team | 2 h | `retrospective.md` — **the single highest-value file in the tree** |

`[S]` **Total ≈ 1.5–2 h/week of capture**, most of it inside meetings already happening. That is
inside the `awards_business` 44.9 h line *only because* the AI passes are minutes rather than hours —
the same protocol done by hand is ~4 h/week and would consume the entire budget by Week 6. **This is
the actual arbitrage of this document.**

**What to capture, in priority order when time is short:**
1. Decisions and *why* (irreplaceable — nobody remembers rationale after 6 months)
2. Failures and dead ends (nobody else records these; they are your unique asset)
3. Numbers: test data, cycle times, current draws, costs, hours, attendance
4. Photos with dated, indexed filenames (worthless unindexed; every award lane needs them)
5. Names of people outside the team: judges' feedback, sponsor contacts, partner orgs
6. Narrative prose ← **last.** It is the easiest thing to regenerate from 1–5.

### 6.5 Keeping it current, and surviving graduation

- **Monthly freshness pass `[S]` 15 min.** Ask the model to list every file not modified in 60 days
  and flag stale claims (a "current sponsor" who lapsed, a subsystem doc that predates a rebuild).
- **Status field on every doc:** `DRAFT / CURRENT / SUPERSEDED-BY-<file> / ARCHIVED`. A model can then
  refuse to answer from a superseded file. This one field prevents most stale-answer failures.
- **Season rollover, every April:** freeze `01_season/<year>/` into `99_archive/`, write the
  retrospective *before* seniors leave, refresh `CLAUDE.md`.
- **The exit interview.** Every graduating senior spends **30 minutes** answering: what do you know
  that nobody else on this team knows? What would you tell yourself as a freshman? What is about to
  break when you leave? Record it, AI-transcribe and structure it (**P-18**), file in
  `00_charter/exit-interviews/`. `[S]` 4 seniors × 30 min = **2 h/year to prevent the single most
  common cause of small-team collapse.**
- **Two named owners, always.** The knowledge base has a student owner and a mentor owner. One
  graduates; one does not.
- **Vendor-independence check, annually:** if your AI vendor vanished tomorrow, is the KB still a
  useful set of documents to a human? If the answer is no, you have built a dependency, not an asset.

### 6.6 Retrieval — making the KB actually answerable

Three tiers, cheapest first:

1. **grep.** `grep -ril "intake" team-kb/` answers most questions in one second with zero tokens.
   Teach the students this before anything else.
2. **Paste-in context.** For a focused question, paste the 3–6 relevant files. Highest accuracy,
   fully auditable, no infrastructure. **This is the right default for a 15-student team.**
3. **Agentic file search** (an AI with tool access reading the repo directly). Best for
   cross-document questions ("every DDR that mentions a belt failure"). Requires the tree discipline
   of §6.2 — this is *why* the naming rules exist.

**Do not build a vector database / RAG pipeline.** `[S]` For a corpus this size (a few hundred small
files), it is engineering effort with no accuracy gain over tiers 1–3, it needs maintenance nobody
will do in February, and it fails silently when it goes stale. The tree *is* the index.

---

## 7. Hours ledger — what this actually buys, reconciled to `CM`

Every figure below is `[S]` model output, reconciled against `reference/team_capacity.yaml`.
**In-season budget is `awards_business: 44.9 h`** (kickoff → Week 1 event), out of 599 effective build
hours. Off-season hours (2026-08 → 2027-01-09) are **outside** the 599 h model and are separately
scarce.

| Workstream | Baseline hours, unassisted | With AI | Saved | Where the saving goes |
|---|---|---|---|---|
| §2.1 Build thread (7 wk) | 8.0 | 2.3 | **5.7** | Reinvested: pit-interview prep |
| §2.2 DDRs + trade studies (10) | 5.0 | 1.5 | **3.5** | Reinvested: more DDRs actually written |
| §2.3 Subsystem docs (4) | 4.0 | 1.5 | **2.5** | Drive practice |
| §2.4 Meeting minutes (22 wk) | 4.5 | 1.2 | **3.3** | Fabrication |
| §2.6 Handbook / safety / checklists | 10.0 | 2.5 | **7.5** | Off-season; frees Jan–Feb |
| §3 Awards A–D, F | 16.0 | 6.5 | **9.5** | ~3 h back into §3E mock Q&A |
| §4 Business + grants (in-season share) | 8.0 | 3.0 | **5.0** | Sponsor stewardship |
| §5 Outreach media | 16.0 | 4.0 | **12.0** | Split: outreach delivery + robot |
| §6 KB capture (22 wk @ ~1.7 h) | 88.0 | 37.0 | **51.0** | The KB exists at all |
| **Totals** | **159.5** | **59.5** | **100.0** | |

**Read this honestly.** The unassisted baseline of 159.5 h is **3.5× the 44.9 h you have** — which is
the real reason small teams simply do not produce these artifacts. Even at 59.5 h, the assisted total
still **exceeds** the in-season line. The plan only closes if:

- **~25 h moves to the off-season** (handbook, safety plan, most onboarding lessons, grant
  boilerplate, sponsor list, KB skeleton, `CLAUDE.md`). Off-season hours are outside the 599 h model.
  **Do this work now — it is the whole point of the 20 weeks before kickoff.**
- **~10 h of KB capture is charged to the meetings it happens inside**, not to `awards_business`.
- The residual **~25 h in-season fits inside 44.9 h with ~20 h of headroom** for the things this file
  cannot predict.

**If you do nothing else in the off-season, do §6.2 + §6.3 + §4.3 boilerplate + §2.6.** That is ~25 h
of the **100 h saved in this lane** (§7's own 159.5 → 59.5 subtotal — *not* the season total, which is
40–70 h returned across all eight `CM` lines; see [`00_WORKFLOW_MAP.md`](00_WORKFLOW_MAP.md) §1.11a),
and it is the portion that is *only* available before January.

---

## 8. What AI does badly — read before you trust anything above

This section exists because the user makes budget decisions from this project. `[H]`/`[S]` throughout.

### 8.1 It invents FRC-specific facts with total confidence

The highest-frequency, highest-damage failure. Models will fabricate, fluently: **rule numbers**
("R502 says…"), **award names** (2022→2026 names churned every season; one changed mid-2026),
**deadlines**, **part numbers and prices**, **vendor URLs**, **team numbers**, and **KoP contents**.
BIOCORE's rules do not exist publicly as of 2026-08-22, so *anything* a model says about the 2027
game is fabrication by definition.

**Mitigation, non-negotiable:** award names ← `AV` only. Rules ← the manual PDF via
`tools/ingest-manual.sh` / `rule-inventory.py`. Parts and prices ← `reference/bom/` and the vendor
page. Deadlines ← `BIZ` / `IX`. If a model produces one of these without a citation you can open, it
is UNVERIFIED.

### 8.2 It cannot count characters

Directly relevant to §3.3: the 500-char exec summary and 10,000-char essay are **hard** limits.
Models estimate; they do not count. Always verify with a real counter before pasting. This has cost
real teams real submissions.

### 8.3 Its FRC control-system knowledge is a season behind, and 2027 breaks everything

Covered in §2.3 and `PS` §0. Training data is overwhelmingly roboRIO-era. Expect `edu.wpi.first`
imports, Shuffleboard references, and PathWeaver workflows — all removed in 2027. Also: vendor library
readiness is genuinely in flux (`PS` lists ChoreoLib and maple-sim with **no current 2027 story** as
of 2026-08). Re-check in November and again at kickoff. A model cannot know this.

### 8.4 It smooths away the specifics that win awards

Generic fluency is the default output mode, and generic fluency is precisely what loses a
resource-normalized rubric (§3.1). The model will happily write "our team is passionate about
inspiring the next generation of engineers," which is worth zero. Force **[named program] + [number] +
[timeframe] + [what changed]** — the recurring unit `BIZ` §2.3 measured in actual winning essays.

### 8.5 It agrees with you

Ask "is this a good design?" and you get validation. Ask "give me the three strongest arguments this
design fails, and the failure mode that would embarrass us in the pit" and you get analysis. Every
critique template in the companion file is phrased adversarially for this reason.

### 8.6 It has no idea what your shop can build

It does not know you have a bandsaw and a drill press. It will suggest waterjet gussets and CNC
plates. Every design-adjacent prompt must carry `team_capacity.yaml`'s tooling level, budget and
motor caps, or the output is fantasy.

### 8.7 It cannot do the things that actually win

It cannot drive, wire, machine, weld, practice, or stand in a pit and answer a judge. `CM` gives 54.9 h
to drive practice and 84.9 h to integration/debug — **AI touches neither.** The entire value
proposition of this file is moving hours *toward* those lines, which only works if you actually spend
them there.

### 8.8 It will help you produce more than you can sustain

The easiest failure of a small team with good AI tooling: a 40-page handbook, a weekly newsletter and
three social accounts in October — all abandoned by February, in front of judges who can see the
timestamps. **Ship the smallest version you can maintain in Week 6 when the robot is broken.**

---

## 9. Validation / dry-run

Every check below was run or specified on 2026-08-22.

| # | Check | Method | Result |
|---|---|---|---|
| 1 | §0 step 1 creates the tree idempotently | Ran the `mkdir -p` + README loop twice | 11 directories, no errors on re-run **[C]** |
| 2 | §0 step 3 reads real capacity data | `reference/team_capacity.yaml` parsed; `awards_business` = **44.9** | Matches `CM` **[C]** |
| 3 | Every hours claim reconciles to `CM` | §7 totals vs `hours.allocation`; 25.0 + 74.9 + 129.8 + 49.9 + 134.8 + 84.9 + 54.9 + 44.9 = **599.1** ≈ `effective_build_hours: 599` | Consistent **[C]** |
| 4 | No award name outside `AV` | All names cross-checked against `00_AWARD_LIST_VERIFIED.md`; Dean's List → **FIRST Leadership Award** | Pass **[C]** |
| 5 | No FTC contamination | `grep -i "pollen\|starterbot\|skill builder"` over this file  returns only the §Scope-guard disclaimer and the CLAUDE.md firewall block (both explicit exclusions) | Pass **[C]** |
| 6 | Policy claims trace to `AIP` | Every quote in §1.1 is verbatim from `00_FIRST_AI_POLICY_VERIFIED.md` | Pass **[C]** |
| 7 | Grant facts trace to `BIZ` §5.4/§5.5 with labels preserved | Gene Haas amount + restriction carried through as **UNVERIFIED**; Dec 1 / Jun 30 disambiguation preserved | Pass **[C]** |
| 8 | Character-limit advice matches `AIP`/`BIZ` | 500 / 10,000 chars incl. spaces; `<`/`>` ban; 2027-02-11 and 2027-02-04 deadlines | Pass **[C]** |
| 9 | No invented URL | Every link is copied from `BIZ`, `AIP`, `AV`, `PS` or `IX`; no new external URL is introduced by this file | Pass **[C]** |
| 10 | Systemcore warnings consistent with `PS` | Package renames, removed tools, Java 25 / C++23, alpha library status | Pass **[C]** |
| 11 | Companion prompt file exists and cross-references resolve | `templates/docs-business-prompts.md`, P-01…P-30 | Pass **[C]** |
| 12 | Dry-run of §2.1 on synthetic notes | Fed 12 bullets from a hypothetical meeting through the P-01 structure | Produced a post with 3 `[WHAT WENT WRONG?]` placeholders unfilled, as designed **[S]** |

**Dry-run limitation:** checks 1–11 are structural/consistency checks that can be run today. Check 12
is a workflow illustration, not a measurement. **No hour-saving figure in §7 has been measured on
this team** — they are model estimates. Log actual times for four weeks in
`team-kb/00_charter/` and correct §7 in place.

---

## Files written by this pass

| Path | What it is |
|---|---|
| `reference/ai-integration/04_ai_for_docs_and_business.md` | This file — policy layer, documentation/awards/business/media workflows, knowledge-base architecture, hours ledger, failure modes |
| `reference/ai-integration/templates/docs-business-prompts.md` | Companion — 30 numbered, copy-paste prompt templates (P-01…P-30) keyed to sections here |
| `team-kb/` *(created by §0 step 1, not by this pass)* | The knowledge-base skeleton: 11 directories + `CLAUDE.md` from §6.3 |

**Cross-links added:** `AIP` (policy authority) · `BIZ` (award/grant/sponsor authority) · `AV` (award
names) · `AA` + `AP` (award targeting) · `CM` (hours + budget) · `PS` (Systemcore) ·
`reference/bom/` (parts + prices) · `tools/bom-builder.py` (gate enforcement) · `IX` / `KP` /
`README.md` (navigation) · `reference/SCOUTING-PLAN.md` and `reference/QA-AMBIGUITY-HOTSPOTS.md`
(feed `team-kb/01_season/`).

---

## Known limitations

1. **Every hour figure in §7 is `[S]` — a model estimate, never measured on this team.** The 100 h
   saving is the load-bearing claim of this document and it is unvalidated. Treat it as a hypothesis
   with a four-week measurement plan attached, not as a budget input.
2. **The Gene Haas competition-team grant amount ($3,000) and the Haas-product spending restriction
   remain UNVERIFIED** against the primary source, exactly as `BIZ` §5.5 found them. Do not budget
   against $3,000. The competition-track **deadline is not published at all**.
3. **No BIOCORE game content exists.** All award/documentation advice is cross-season invariant by
   construction. Re-run `reference/awards/kickoff_award_check.sh` on 2027-01-09 before printing
   anything, and expect at least one award name to move.
4. **The 2026 award character limits and deadlines are carried forward.** `AIP` explicitly warns these
   are 2026 figures for calibration; §3.3's 500 / 10,000 are 2026 values and `BIZ` §1.3's 2027 dates
   come from the Submitted Awards page as read 2026-08-21. **Re-verify when FIRST re-issues.**
5. **School-district AI policy is unknown.** §1.2's four-shape table is a framework, not a finding.
   The actual answer requires an email nobody has sent yet, and it can invalidate §2–§5 entirely.
6. **Vendor terms and minors' data remain an open item**, carried forward from `AIP` §"What this
   policy does NOT do" item 4. The mentor-owned-account and no-PII rules in §1.2(c) are risk
   *reduction*, not a legal review. Check your vendor's terms directly.
7. **No AI vendor, model or product is named anywhere in this file.** That is deliberate — the
   landscape moves faster than this document can, and `AIP`'s attribution requirement is
   vendor-agnostic. Fill in `<model>` in the attribution line with whatever you actually used.
8. **The knowledge-base tree is untested at scale on this team.** It is derived from published team
   practice and general documentation-systems reasoning `[H]/[S]`, not from a controlled comparison.
   The most likely failure is §6.4 capture discipline lapsing in Weeks 4–6, which is exactly when the
   records are most valuable.
9. **§8 is not exhaustive.** It lists the failure modes observed in building this corpus. New ones
   will appear; append them to `team-kb/00_charter/ai-policy.md` as you hit them.
10. **This file does not cover robot code.** See `PS`. `AIP`'s rule stands: human review before
    anything actuates.
