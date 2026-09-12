# Prompt Templates — Documentation, Awards, Business, Media, Knowledge Base

**Purpose:** the runnable half of
[`../04_ai_for_docs_and_business.md`](../04_ai_for_docs_and_business.md). Thirty copy-paste prompts,
numbered **P-01 … P-30**, each keyed to a section of the parent file. Every one is written for
**FRC Team \<NNNN\>: 15 students, 1 experienced technical mentor, $2,500 robot budget,
bandsaw + drill press + FDM printer, 2027 BIOCORE presented by Haas, kickoff 2027-01-09.**

**Parent file:** [`../04_ai_for_docs_and_business.md`](../04_ai_for_docs_and_business.md) — read §1
(rules) and §8 (what AI does badly) before using any template here.

**Evidence labels:** **[C]** CONFIRMED · **[H]** HISTORICAL-PATTERN · **[S]** SPECULATION ·
**UNVERIFIED**. Prompt *design* here is `[S]`; the constraints the prompts carry are `[C]` and cite
their source file.

---

## 0. The 60-second workflow

```bash
# Run from the repository root.

# 1. The standing preamble every prompt needs. Paste it once per conversation, or
#    let team-kb/CLAUDE.md carry it automatically (parent file §6.3).
sed -n '/^### PREAMBLE/,/^### END PREAMBLE/p' reference/ai-integration/templates/docs-business-prompts.md

# 2. Find the template you need
grep -n "^## P-" reference/ai-integration/templates/docs-business-prompts.md

# 3. Character-count check -- USE THIS EVERY TIME on award text (parent §8.2).
#    Models cannot count characters. 500 for exec summaries, 10000 for the essay.
python -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();print(len(t),'chars',
'OK' if len(t)<=500 else 'OVER (500 limit)')" team-kb/07_awards/impact/q03.txt

# 4. Angle-bracket check -- FIRST warns < and > may prevent the submission saving
grep -n '[<>]' team-kb/07_awards/impact/*.txt && echo "!! REMOVE ANGLE BRACKETS"
```

---

## 1. The preamble — paste this first, every time

Every template below assumes this block is in context. If `team-kb/CLAUDE.md` (parent §6.3) is loaded,
skip it.

### PREAMBLE

```
You are assisting FRC Team <NNNN> for the 2027 season.

TEAM REALITY (authority: reference/team_capacity.yaml — do not contradict it):
- 15 students, 1 experienced technical mentor, ~15 scheduled hours/week.
- Tooling: bandsaw, drill press, one FDM 3D printer. NO mill, lathe or CNC router in house.
  Mentor-supervised mill access only. Outsourcing budget ~$400, ~2 week lead time.
- Robot discretionary budget $2,500. Season planning total ~$11,500.
- In-season awards+business hours: 44.9 total, kickoff to Week 1 event.

SEASON:
- BIOCORE presented by Haas is the FRC 2027 game, FIRST CANOPY season. Kickoff 2027-01-09 12:00 ET.
- BIOBUZZ is the FTC game, not ours. Pollen, StarterBots and Skill Builders are FTC. Never mention
  them in connection with BIOCORE.
- BIOCORE's rules are NOT public. Anything you say about the 2027 game specifics is fabrication.
- 2027 replaces the roboRIO with Systemcore. WPILib 2027 is a breaking rewrite (Java edu.wpi.first ->
  org.wpilib; C++ frc:: -> wpi::; NetworkTables v3, Shuffleboard, SmartDashboard, PathWeaver,
  RobotBuilder and LabVIEW all removed; Java 25 / C++23 required). Your training data is mostly
  pre-2027. Treat every control-system claim you make as UNVERIFIED.

HOW TO ANSWER:
- Label every claim [C] confirmed / [H] historical pattern / [S] speculation / UNVERIFIED.
- NEVER invent a URL, price, part number, team number, rule number, award name or deadline.
  If unsure, write UNVERIFIED and name the file or primary source that would settle it.
- Award names come only from reference/awards/00_AWARD_LIST_VERIFIED.md. Dean's List is now the
  FIRST Leadership Award.
- Do not do BOM arithmetic; tell me to run tools/bom-builder.py.
- No student PII. No full names of minors, addresses, birthdates, grades, health or contact data.
- Be concise. We do not have hours for elegance.
```

### END PREAMBLE

---

# Section A — Documentation (parent §2)

## P-01 — Open Alliance build-thread post from meeting notes  `parent §2.1`

```
Draft this week's Open Alliance build thread post for Team <NNNN>.

INPUTS
- This week's raw meeting notes: <paste team-kb/04_meetings/*.md for the week>
- Last week's posted update (for continuity and voice): <paste>
- Photos available this week (filenames + one-line description each): <paste>

WRITE
1. A 400-700 word post, first person plural, plain engineering voice. No marketing language.
2. Structure: what we set out to do this week -> what we actually did (by subsystem) ->
   what broke or surprised us -> data/numbers -> what's next week -> open questions for readers.
3. Suggest where each photo goes.

HARD RULES
- Use ONLY facts present in my notes. Invent nothing: no dimensions, part numbers, cycle times,
  costs or outcomes that are not written down.
- Where the notes imply something happened but do not say what, insert a literal placeholder
  [WHAT WENT WRONG? — <specific question>] rather than guessing. I will fill these in.
- Where a number is missing but would strengthen the post, insert [NUMBER NEEDED: <what>].
- Flag anything you assert about Systemcore/WPILib 2027 as UNVERIFIED.
- End with our standing attribution line placeholder.
- Open Alliance readers reward candor. Do not sand off the failures.

OUTPUT: the post in markdown, then a bullet list of every placeholder I must resolve before posting.
```

## P-02 — Design Decision Record from a 60-second brain dump  `parent §2.2`

```
Turn my rough account into a Design Decision Record using EXACTLY this skeleton:

# DDR-<NNN> — <title>
Date: | Status: DECIDED|PROPOSED|SUPERSEDED | Owner: | Supersedes:
## Context
## Options            (each: cost, build hours, tooling level required, risk)
## Decision           (one sentence, active voice)
## Rationale          (in terms of hours, budget, tooling, motor count — our real constraints)
## Consequences       (what this forecloses; what it obligates)
## Evidence
## Revisit-if

MY ACCOUNT: <paste bullets or voice-to-text>

RULES
- Every fact not present in my account gets [UNVERIFIED] appended. Do not smooth over gaps.
- If an option's cost or hours are unknown, write [UNVERIFIED — check reference/bom/] — do not
  estimate a price.
- Rationale must reference our actual constraints: $2,500 budget, 129.8 fabrication hours,
  74.9 CAD hours, 134.8 programming hours, bandsaw+drill press tooling, max 12 motors,
  max 2 novel mechanisms.
- If my account does not actually contain a decision, say so and ask the three questions that
  would produce one.
- Keep it under 400 words. A DDR nobody reads is worthless.
```

## P-03 — Trade study with scored matrix  `parent §2.2`

```
Build a trade study for: <decision>

OPTIONS I AM CONSIDERING: <list 2-4>
DATA I HAVE: <paste relevant rows from reference/bom/mechanism_catalog.yaml, plus any test data>

SCORE each option 1-5 against these criteria, weighted for OUR team:
  - Cost against $2,500 robot discretionary        (weight 3)
  - Fabrication hours against 129.8 available      (weight 3)
  - Programming hours against 134.8 available      (weight 2)
  - Buildable with bandsaw + drill press + FDM     (weight 3 — a NO here is disqualifying)
  - Failure modes / reliability under match load   (weight 3)
  - Repairability between matches with 15 students (weight 2)
  - Counts against our max-2-novel-mechanisms cap  (weight 2)

RULES
- Show the weighted arithmetic, but state clearly that the BOM totals must be confirmed by running
  tools/bom-builder.py, which enforces the real gates. Do not present your arithmetic as final.
- Any option that requires machining we cannot do in house must show the outsourcing cost against
  our $400 budget AND the 2-week lead time against the calendar.
- Give me the strongest argument AGAINST your top-scored option.
- Mark every number you did not get from my inputs as UNVERIFIED.
```

## P-04 — Subsystem documentation from source code  `parent §2.3`

```
Write a one-page pit-binder summary of the <subsystem> subsystem.

SOURCES (use ONLY these; do not rely on your general knowledge of FRC code):
- Source files: <paste>
- Relevant DDRs: <paste from team-kb/03_decisions/>
- CAD notes / BOM rows: <paste>

SECTIONS
1. Purpose — what it does in the game, one sentence
2. Actuators and controllers — exact hardware from my BOM only
3. Sensors and what they measure
4. Control strategy — in words a judge can follow
5. Key constants and WHAT THEY PHYSICALLY MEAN
6. Known failure modes and what we do about each
7. "The 60-second pit explanation" — the script a student says out loud to a judge

CRITICAL
- Our control system is Systemcore with WPILib 2027, NOT roboRIO. If you find yourself writing
  edu.wpi.first, Shuffleboard, SmartDashboard, PathWeaver or roboRIO, you are drawing on stale
  training data — stop and flag it.
- If you reference a class, method or constant, it must appear in the source I pasted. If it does
  not, you are hallucinating: write [NOT FOUND IN SOURCE] instead.
- One page. Judges will not read two.
```

## P-05 — Meeting notes to action items  `parent §2.4`

```
Process these raw meeting notes.

NOTES: <paste>
CURRENT OPEN ACTIONS (so you can close/dedupe): <paste team-kb/04_meetings/ACTIONS.md>

OUTPUT exactly four blocks:
1. DECISIONS MADE — one line each. Flag any that deserves a full DDR (parent §2.2).
2. ACTION ITEMS — table: what | owner | due date | blocked by.
   If the notes do not name an owner, write "UNASSIGNED — needs owner". NEVER assign one yourself.
   If no date is stated, write "NO DATE — needs date".
3. OPEN QUESTIONS — things nobody resolved.
4. CLOSED — items from the current list the notes show as done.

Use initials or roles only, never full names. Keep it terse; this gets pasted into ACTIONS.md.
```

## P-06 — Onboarding lesson from existing documentation  `parent §2.5`

```
Write onboarding lesson <N>: <topic>, for a student with no prior robotics experience.

SOURCE MATERIAL: <paste the relevant subsystem doc, DDRs, safety plan section>
WHO TEACHES IT: <role> | TIME AVAILABLE: <e.g. 45 minutes> | TOOLS ON HAND: bandsaw, drill press,
FDM printer, hand tools

FORMAT
- Objective: what they can do afterward, stated as a capability
- Why it matters on our robot (use our real subsystem, not a generic example)
- 20-minute demo script for the teacher
- Hands-on exercise the student does themselves
- "You are done when..." — an observable check
- Who to ask when stuck (role, not name)
- Common mistakes

RULES
- Safety content: cite our own safety plan. Do NOT invent an OSHA reference, a chemical procedure,
  or a PPE standard. If a safety point is not in my source, write [MENTOR MUST SUPPLY].
- If this is a software lesson, it must target WPILib 2027 / Systemcore only. Anything roboRIO-era
  is scrap. Flag any statement you are not certain of as UNVERIFIED.
- Assume the teacher is a junior, not the mentor.
```

## P-07 — Team handbook / safety plan / pit checklist skeleton  `parent §2.6`

```
Draft a <team handbook | safety plan | pit checklist | event-day run sheet> for our team.

WHAT I CAN TELL YOU: <paste bullets — school rules, shop rules, travel constraints, roles, schedule>
CONSTRAINTS: 15 students, 1 technical mentor, <school name withheld>, our shop is <describe>.

RULES
- Maximum 8 pages for a handbook, 1 page for a checklist. Longer documents do not get used.
- Every policy sentence must trace to something I told you. Where a policy is needed but I have not
  supplied it, write [MENTOR DECISION NEEDED: <question>] rather than inventing one.
- SAFETY: do not invent regulations, standards, extinguisher classes or chemical procedures.
  Every safety line traces to my input, our school policy, or a named manufacturer document.
- Note for me where school administration review is required before this can be issued.
- There is no longer a Safety Award in FRC — do not frame the safety plan as an award play.
```

---

# Section B — Awards (parent §3)

> **Read parent §3.1 first.** The students supply the experience, claims, numbers and voice. AI
> supplies structure, pressure and a second read. None of these templates writes final award prose.
> **P-09 in particular is designed to refuse.**

## P-08 — Criteria gap analysis  `parent §3.2A`

```
Act as a judge preparing to score us against published criteria.

AWARD: <exact name from reference/awards/00_AWARD_LIST_VERIFIED.md>
PUBLISHED CRITERIA: <paste from reference/awards/01_AWARD_WINNING_PATTERNS.md dossier or the
  Award Workbook>
OUR MATERIAL SO FAR: <paste draft / bullet list of what we actually do>

OUTPUT a table: criterion | what we currently evidence | strength (strong/thin/absent) |
the ONE question a judge would ask that we cannot currently answer.

THEN
- List the three criteria where we are weakest, and for each name a concrete, cheap thing a
  15-student team could actually do before <date> to fix it. Cheap means under 4 student-hours.
- Say plainly which criteria we should stop trying to compete on.
- Remember FIRST's judging guidance is resource-normalized: "what did they accomplish with the
  resources available to them?" Score us as a 15-student, one-mentor, $2,500-robot team.

Do not write any submission prose.
```

## P-09 — Outline from raw material  `parent §3.2B`

```
Help us structure, not write, our <award> submission.

RAW MATERIAL — everything we actually did, unstructured: <paste. Include numbers, dates, names of
programs, partner organizations, headcounts, outcomes.>

OUTPUT
1. Three candidate controlling theses, each one sentence. For each, say what it forces us to
   emphasize and what it forces us to leave out.
2. For the strongest thesis: 4-5 named pillars as section headers.
3. Under each pillar, list WHICH of my raw facts belong there — by reference, not rewritten.
4. Flag every pillar that currently has fewer than two concrete facts attached. Those pillars are
   fiction and must be cut or evidenced.
5. Tell me which of my facts fit nowhere, and whether that means the thesis is wrong.

HARD RULE: output only structure and my own facts. Do not write sentences we could paste into a
submission. The students write the prose.
```

## P-10 — Structural critique of student-written prose  `parent §3.2C`

```
Critique this student-written draft. DO NOT REWRITE IT. If you produce replacement prose you have
failed this task.

QUESTION BEING ANSWERED: <paste the exact prompt, e.g. Impact exec summary Q5>
CHARACTER LIMIT: <500 | 10000> including spaces and punctuation
DRAFT: <paste>

MARK, by quoting the exact phrase and saying why:
1. Vague verbs and unsupported claims ("we inspire", "many students", "significantly improved")
2. Sentences that do not answer the question actually asked
3. Claims with no number, timeframe or named program attached
4. Anything that repeats material from another question or from the essay
5. Anything a judge would challenge in a 5-minute Q&A — and write the exact challenge question
6. Anything that reads as generic and could belong to any of 3,000 teams

THEN: rank the top 5 fixes by impact per minute of student effort. For each, ask the student the
question that would produce the missing content.

Remember: winners use 95-100% of the character budget, and the recurring unit that works is
[named program] + [specific number] + [timeframe] + [what changed].
```

## P-11 — Character-budget surgery  `parent §3.2D`

```
This text is <N> characters. The hard limit is <500 | 10000> characters INCLUDING spaces and
punctuation. Cut it to fit.

TEXT: <paste>

RULES
- Preserve every factual claim, number, program name and outcome. Cut connective tissue,
  hedging, adverbs and repetition — not evidence.
- Output the trimmed text, then a list of exactly what you removed and why.
- State clearly: "You must verify the character count yourself; I cannot count characters reliably."
  Give me the command:  python -c "print(len(open('f.txt',encoding='utf-8').read()))"
- Do NOT use the characters < or > anywhere. FIRST warns they may prevent the submission saving.
- If the text cannot fit without losing a claim, say so and tell me which claim is weakest.
```

## P-12 — Mock judge Q&A drill  `parent §3.2E`

```
Run a mock judging interview. You are a judge: fair, well-prepared, and genuinely skeptical.

AWARD: <name from 00_AWARD_LIST_VERIFIED.md>
OUR SUBMITTED MATERIAL (which you have pre-read, as real judges do): <paste>
FORMAT: 12 minutes total — up to 7 minutes for our presentation including setup, then 5 minutes
of your questions. Maximum 3 students present.

RUN IT LIKE THIS
1. Ask one question at a time. Wait for my answer. Do not supply answers.
2. Follow up on anything vague — real judges do, and they cross-check claims with Match Observers
   who watched our matches.
3. Ask at least two questions that probe whether the students actually did the work described.
4. Ask the uncomfortable one: our published question 12 asks for an area we need to improve.
5. After 5 minutes of questions, stop and give: what was convincing, what was thin, which answer
   would have cost us the award, and the three questions we must prepare before the event.

Draw question style from FIRST's published judge question bank where I have pasted it. Do not
invent an official FIRST question and present it as official — mark invented ones [S].
```

## P-13 — Judge-feedback triage  `parent §3.2F`

```
We received post-event judge feedback (each field is 500 characters or less, delivered within 48
hours via the Dashboard). Turn it into a change list.

FEEDBACK: <paste all three fields: area to improve / what impressed / answer to our own question>
NEXT EVENT DATE: <date>
WHAT WE CAN STILL CHANGE: the presentation and the video. The submitted essay and exec summaries
are LOCKED and cannot be altered.

OUTPUT
1. What the feedback is actually saying, including what it implies but does not state.
2. A ranked change list — only changes to the presentation, video or pit materials. Anything that
   would require editing the locked submission: say so and drop it.
3. For each change: hours needed, who does it, and done-by date working back from <date>.
4. What we should ask as our submitted judge question next time, given what this feedback did and
   did not tell us.
```

---

# Section C — Business and administration (parent §4)

## P-14 — Sponsor prospect research  `parent §4.1`

```
Build a sponsor prospect table.

EMPLOYERS connected to our team's families and mentors (company names only — no student or family
names): <paste list>
OUR LOCATION (city/region, no school name): <paste>
WHAT WE NEED: cash toward a ~$11,500 season, and in-kind machining/materials to compensate for a
shop with only a bandsaw, drill press and FDM printer.

TABLE: company | likely giving vehicle (corporate giving / matching gifts / employee-directed /
local branch discretionary / in-kind) | plausible in-kind offer they could make us |
suggested first ask amount | who on our team has the connection (by role) | confidence [C/H/S]

RULES
- Mark EVERY specific program claim UNVERIFIED unless I gave it to you. You do not know whether a
  given company has a matching-gift program — do not assert it. Give me the URL pattern I should
  check on the company's own site instead.
- Do not invent contact names, email addresses, phone numbers or philanthropy program names.
- Rank by realistic yield per hour of student effort, not by company size.
- Separately: list the in-kind categories FIRST itself recommends asking for, and which of our
  prospects plausibly has each.
```

## P-15 — Sponsor letter, tailored  `parent §4.2`

```
Draft a one-page sponsorship letter.

RECIPIENT: <company, and the specific connection — e.g. "parent works in their machining division">
TIER WE ARE ASKING FOR: <$ amount or in-kind item>
OUR TRUE STORY — use only these facts: <paste. Include team size, budget reality, what students
actually build and learn, outreach we actually do, and any prior relationship.>

RULES
- One page. Open with the connection, not with FIRST's mission statement.
- Name what their money or material specifically buys, in our terms ($2,500 robot budget,
  no CNC in house, 15 students).
- Include exactly what they get back at this tier. Do not promise anything I did not list —
  FIRST's own guidance: "Don't promise to give a 10-foot cardboard cutout of your robot if you
  can't follow through."
- No superlatives, no "passion for STEM", no invented statistics.
- Add a one-line disclosure that AI assisted in drafting; funders increasingly ask.
- End with a specific ask and a specific next step with a date.
```

## P-16 — Gene Haas Foundation application framing  `parent §4.3`

```
Help me frame our Gene Haas Foundation "Student Competition Teams" application. INTERVIEW ME —
ask questions one at a time; do not draft until you have my answers.

WHAT IS ESTABLISHED [C], from reference/team-ops/05_business_awards_sustainability.md §5.5:
- The track is for "approved competitions (FRC, FTC, SAE, etc.) in which students design and build
  a product that utilizes CNC machining."
- Applications for the FIRST 2026/2027 season are accepted after May 1, 2026 — the window is open.
- The Foundation's mission: "To introduce to and educate individuals for the field of manufacturing
  technologies specifically CNC machining."
- Haas presents the 2027 FRC game BIOCORE.

WHAT IS **UNVERIFIED** — you must not treat these as fact and must not let me budget against them:
- The reported $3,000 FRC / $2,000 FTC amounts (secondary sources only; not published by the
  Foundation).
- A reported restriction on buying Haas-manufactured products with grant funds.
- There is NO published deadline for the competition-teams track. December 1 belongs to the
  secondary-school CNC scholarship track and June 30 to the post-secondary track — neither is ours.

ASK ME ABOUT: how our students actually encounter machining (including mentor-supervised mill
access and outsourced work); whether any student is on a Haas certification pathway; whether there
is an HTEC or Haas Factory Outlet near us; what machining skill a grant would let us add.

THEN produce an OUTLINE only, foregrounding machining education over competition results — that is
what this funder actually funds. Flag anything I still need to confirm in the application portal.
```

## P-17 — Grant boilerplate library  `parent §4.3`

```
Build our reusable grant boilerplate.

MY RAW ANSWERS: <paste — team history, mission, student demographics in aggregate only, budget,
outreach, what the money does, how we measure impact, sustainability plan>

For each standard question below, produce a SHORT (~100 word) and LONG (~400 word) version:
1. Describe your organization and its mission
2. Describe the program to be funded
3. Who does it serve, and how many
4. What is the need
5. How will funds be used (specific line items)
6. How do you measure success
7. How will this be sustained after the grant
8. Total budget and other funding sources

RULES
- Use only my facts. Every number must come from me. Where a funder will expect a number I have
  not given you, write [NUMBER NEEDED: <what>].
- No aggregate demographic claim unless I supplied it. No individual student information at all.
- Keep a plain, unadorned voice. Grant reviewers read hundreds of these.
- Output as markdown ready to save to team-kb/06_business/grant-boilerplate.md.
```

## P-18 — Budget scenario narration  `parent §4.4`

```
Do NOT do arithmetic. Interpret and stress-test.

OUR NUMBERS (authority: reference/team_capacity.yaml and our budget.yaml): <paste>
  robot discretionary $2,500 | registration $6,500 | season planning total $11,500 |
  spares/consumables $500 | outsourcing $400 | sales tax 7%
SCENARIO: <e.g. "we add a second district event" | "the Haas grant does not come through" |
  "a sponsor doubles">

OUTPUT
1. What breaks first, and at what dollar figure.
2. The three line items with the most give, and what each cut actually costs us competitively.
3. Which cut damages an award lane (check against reference/awards/AWARD-ALIGNMENT.md).
4. What FIRST's process rules constrain here — including: do not pay registration while a grant
   decision is pending; several grants disqualify teams that already paid.
5. Any line item you think is missing entirely, checked against FIRST's own budget template
   categories.

Do not compute totals. For any BOM question, tell me to run tools/bom-builder.py, which enforces
the real gates ($2,500 cap, 129.8 build h, 74.9 design h, 134.8 programming h, 12 motors,
bandsaw+drill press tooling).
```

## P-19 — Inventory reconciliation and order-by dates  `parent §4.5`

```
Reconcile our inventory against what the season needs.

WHAT WE HAVE: <paste photo-derived list or spreadsheet dump>
WHAT WE NEED: <paste BOM rows from reference/bom/>
KEY DATES: BOM order-by 2026-11-21 | kit selection closes 2026-11-17 | kickoff 2027-01-09
LEAD TIME SAFETY MARGIN: 1 week

OUTPUT
1. Have / need / gap table.
2. Gaps sorted by order-by date, computed backward from when we need the part, plus lead time,
   plus the 1-week margin.
3. Anything whose order-by date has already passed or lands inside two weeks — flagged loudly.
4. What we can substitute from stock, and what that substitution costs us.

RULES
- NEVER invent a part number or a price. Every one must come from my paste or from
  reference/bom/. If a part is unpriced, write [PRICE UNVERIFIED — check vendor].
- Long-lead electrical items are the classic miss. Call them out separately.
```

## P-20 — Travel logistics packet  `parent §4.5`

```
Draft the travel packet for <event, dates, location>.

CONSTRAINTS: <students attending (count only), chaperones available, departure/return times,
budget, school travel rules, dietary needs described in AGGREGATE only — no names>

PRODUCE
1. Hour-by-hour itinerary including load-in, pit setup, match blocks, load-out.
2. Packing list split: robot/pit, tools and spares, team, individual students.
3. Meal plan within budget, noting where a sponsor in-kind ask could cover meals.
4. Chaperone assignments by role and the ratio implied.
5. A parent information letter — plain, one page.
6. An emergency-contact and comms plan (structure only; I fill in the actual contacts).

RULES
- No student names, addresses, phone numbers or medical details anywhere in your output.
- Do not book anything, quote a hotel price, or state an airline/venue policy as fact — mark all
  such items [VERIFY WITH VENDOR].
- Flag every item that needs school administration approval.
```

## P-21 — Season calendar and collision check  `parent §4.5`

```
Build our season calendar and find the collisions.

FIXED DATES [C], from INDEX.md and reference/team-ops/05_business_awards_sustainability.md:
  2026-09-13 BAE grant | 2026-09-24 Kit & Kickoff selection opens | 2026-09-30 Boston Scientific
  2026-10-16 Boeing | 2026-10-29 12:00 ET award submission portal OPENS | 2026-11-06 John Deere
  2026-11-12 Pre-Kickoff Virtual Kit Release | 2026-11-17 kit selection CLOSES
  2026-11-21 BOM order-by | 2027-01-09 12:00 ET KICKOFF
  2027-02-04 15:00 ET FIRST Leadership Award + Woodie Flowers Finalist due
  2027-02-11 15:00 ET FIRST Impact Award due
OUR DATES: <paste school calendar: exam weeks, breaks, holidays, other commitments>

OUTPUT
1. Merged calendar, chronological, with the hard stops marked.
2. Every collision between a FIRST deadline and a school blackout, with a mitigation.
3. Working-back schedules: what must start when, for the Impact submission, the grant
   applications, and the kit selection.
4. Reminder text for each item, ready to paste into a calendar app.

Do not restate a deadline I did not give you. If you think one is missing, ask.
```

---

# Section D — Outreach and media (parent §5)

## P-22 — Social post variants

```
Write 5 caption variants for one post.

PHOTO/VIDEO: <describe> | THE FACT: <one true, specific thing that happened — with a number>
AUDIENCE: <sponsors | prospective students | FRC community | local community>
SPONSORS TO TAG: <list>

RULES
- Every variant must contain the specific fact. A caption with no fact is a caption we do not post.
- Minors are FIRST NAME ONLY. Never a full name.
- No invented statistics, no "changing the world", no exclamation-point stacking.
- Vary the angle across variants: technical / human / sponsor-thanking / recruiting / behind-the-scenes.
- Suggest hashtags actually used in the FRC community; mark any you are unsure of as UNVERIFIED.
- A human posts. You never post.
```

## P-23 — Monthly newsletter from existing build-thread posts

```
Assemble this month's newsletter for sponsors and parents.

SOURCE — build thread posts already written this month: <paste>
OUTREACH EVENTS THIS MONTH: <paste rows from team-kb/05_outreach/events-log.yaml>
SPONSOR NEWS: <paste>

FORMAT: 400-600 words. Sections: where the robot is | what students learned | outreach | thank-you
to sponsors by name | what's next | one clear ask (volunteer, in-kind, referral).

RULES
- Every fact comes from the pasted sources. Add nothing.
- Sponsors named exactly as they appear in team-kb/06_business/sponsors.yaml — a misspelled sponsor
  name is worse than no newsletter.
- First names only for students.
- End with the AI attribution line.
```

## P-24 — Presentation deck outline

```
Outline a <length>-minute presentation for <audience: school board | sponsor | community demo |
Impact judges>.

WHAT WE WANT: <the ask or the message>
MATERIAL AVAILABLE: <paste>

OUTPUT: slide-by-slide — slide title, the ONE point it makes, what is on it visually, and speaker
notes as bullets a student can talk from (not a script to read).

RULES
- If this is the Impact interview: 12 minutes total, up to 7 for presentation INCLUDING setup, 5
  for judge Q&A, maximum 3 students presenting. One mentor may attend as a silent observer.
  Build the deck for 6 minutes so setup fits.
- Students deliver this. If they cannot answer a question about a slide, the slide is wrong —
  flag any slide that depends on a claim the presenting students did not personally live.
- Fewer slides than you think. One point per slide.
```

## P-25 — Press release / local media pitch

```
Draft a press release and a pitch email.

THE NEWS: <what actually happened, with the date and the numbers>
QUOTES AVAILABLE: <paste ACTUAL quotes people actually said, with role — or write "none">
OUTLET: <local paper / school paper / sponsor's internal comms>

RULES
- NEVER invent a quote. If I gave you none, insert [QUOTE NEEDED FROM: <role>] and give me two
  questions that would produce a usable one.
- Minors: first name only, plus grade level at most.
- Standard release structure: headline, dateline, lede answering who/what/when/where/why,
  two body paragraphs, boilerplate about the team, contact (mentor, not student).
- The pitch email is 5 sentences maximum. Editors do not read more.
- Every number traceable to my input.
```

---

# Section E — The knowledge base (parent §6)

## P-26 — Generate the project `CLAUDE.md`

```
Draft team-kb/CLAUDE.md — the standing brief any AI reads before working with our team.

Use the template in reference/ai-integration/04_ai_for_docs_and_business.md §6.3 as the structure,
and fill it with these specifics: <paste team number, actual tooling inventory, actual budget from
budget.yaml, actual roles, actual directory contents>

RULES
- Under 150 lines. A long CLAUDE.md gets skimmed and is worse than a short one.
- Must include, non-negotiably: the FRC-vs-FTC firewall (BIOBUZZ/Pollen/StarterBots/Skill Builders
  are FTC); the Systemcore/WPILib-2027 warning; the no-PII rule; the "you do not write award
  submissions" rule; the evidence-label requirement; the attribution line.
- Written as instructions to a model, not as documentation for a human.
- Point to the authority file for each class of fact rather than restating the facts.
```

## P-27 — Knowledge base freshness audit  `parent §6.5`

```
Audit our knowledge base for staleness.

FILE LIST WITH LAST-MODIFIED DATES: <paste output of:  ls -lR --time-style=+%Y-%m-%d team-kb/  >
CONTENTS OF SUSPECT FILES: <paste>

OUTPUT
1. Files not touched in 60+ days, with a guess at whether that is fine (archived) or a problem
   (should be current).
2. Claims that are probably stale: sponsors listed as current, subsystem docs predating a rebuild,
   roles held by graduated students, roboRIO-era software content.
3. Files missing the status field (DRAFT / CURRENT / SUPERSEDED-BY-<file> / ARCHIVED).
4. Contradictions between files — the highest-value finding. Name both files and both claims.
5. A 15-minute fix list, ranked.

Do not rewrite anything. Report only.
```

## P-28 — Graduating senior exit interview  `parent §6.5`

```
Structure this exit interview transcript into a knowledge artifact.

TRANSCRIPT: <paste — from a 30-minute recorded conversation>
STUDENT'S ROLE(S): <role only, no name>

OUTPUT under these headings:
1. What this person knew that nobody else on the team knows — the irreplaceable list
2. Undocumented processes they were personally carrying
3. What they would tell themselves as a freshman
4. What is about to break when they leave, and who should own each thing now
5. Relationships they held (sponsor contacts, partner orgs, other teams) that need a handoff —
   organizations only, no personal contact details
6. Which of the above should become a DDR, a lesson in 08_onboarding/, or a row in sponsors.yaml

RULES
- Use role labels, never the student's name.
- Quote them where the exact wording carries the knowledge. Do not paraphrase away specifics.
- Flag anything they said that contradicts our written documentation — that is the most valuable
  output of this exercise.
```

## P-29 — Season retrospective  `parent §6.5, written every April`

```
Facilitate our season retrospective, then write it up.

INPUTS: <paste — match record, award results, judge feedback, DDR list, build thread, budget
actuals vs plan, what students say went wrong>

PHASE 1 — ask me 10 questions, one at a time, that a team does not usually ask itself. Include at
least two about decisions that LOOKED right and were not, and one about something we got right
by luck rather than process.

PHASE 2 — write team-kb/01_season/<year>/retrospective.md:
  ## What we set out to do
  ## What actually happened (with numbers)
  ## Decisions that held up      (link the DDRs)
  ## Decisions that did not      (link the DDRs — this section is the most valuable in the file)
  ## What we got right by luck
  ## What we would tell next year's team on kickoff day
  ## Specific changes for next season, with an owner each

RULES
- Blameless. Roles, never names, for anything negative.
- Every claim traceable to my inputs. No consoling generalities.
- The "would tell next year's team" section is written FOR a stranger who was not there.
```

## P-30 — Cross-document question over the knowledge base  `parent §6.6`

```
Answer a question using only our knowledge base.

QUESTION: <e.g. "Why did we choose a roller intake in 2027, and did it work?">
FILES: <paste the 3-6 relevant files, or grant file access to team-kb/>

RULES
- Answer ONLY from the files. If the answer is not there, say "not documented" and name the file
  that should have contained it — that gap is itself a finding worth reporting.
- Cite the file and section for every claim.
- If two files disagree, say so explicitly and name both. Do not silently pick one.
- Check status fields: never answer from a file marked SUPERSEDED or ARCHIVED without saying so.
- Distinguish what was DECIDED from what was OBSERVED from what was SPECULATED at the time.
```

---

## Validation

| # | Check | Result |
|---|---|---|
| 1 | Every template is numbered P-01…P-30 and referenced by the parent file | 30 templates present; `grep -c "^## P-"` = 30 **[C]** |
| 2 | Parent-file section references resolve | Each template header names a `parent §` that exists in `04_ai_for_docs_and_business.md` **[C]** |
| 3 | No award name appears outside `00_AWARD_LIST_VERIFIED.md` | Only FIRST Impact Award, FIRST Leadership Award, Woodie Flowers Finalist appear, all by verified name **[C]** |
| 4 | No FTC contamination | Pollen / StarterBots / Skill Builders appear only in the preamble and P-26, both as explicit exclusions **[C]** |
| 5 | No prompt asks the model to write final award prose | P-08…P-13 each carry an explicit refusal instruction; P-10 refuses to rewrite **[C]** |
| 6 | Character limits stated as 500 / 10,000 incl. spaces, with the `<`/`>` ban | P-11, §0 step 3–4 **[C]** |
| 7 | Every prompt touching money or parts forbids invented prices/part numbers | P-02, P-03, P-14, P-18, P-19 **[C]** |
| 8 | PII rules present in every prompt that touches people | P-05, P-14, P-15, P-17, P-20, P-22, P-23, P-25, P-28, P-29 **[C]** |
| 9 | Systemcore warning present in every software-adjacent prompt | Preamble, P-01, P-04, P-06, P-27 **[C]** |
| 10 | Gene Haas facts carry the same labels as the parent file | P-16 marks amount, restriction and deadline as UNVERIFIED **[C]** |
| 11 | §0 commands are syntactically valid | `sed`, `grep`, `python -c` forms checked; paths relative to project root **[C]** |
| 12 | Prompt effectiveness | **NOT MEASURED.** No A/B test, no output scoring **[S]** |

---

## Files written by this pass

| Path | What it is |
|---|---|
| `reference/ai-integration/templates/docs-business-prompts.md` | This file — the preamble plus 30 prompt templates (P-01…P-30) for documentation, awards, business, media and the knowledge base |
| `reference/ai-integration/04_ai_for_docs_and_business.md` | Parent — the policy layer, the workflows these prompts execute, the hours ledger and the failure-mode list |

---

## Known limitations

1. **No prompt here has been measured.** Wording is `[S]` — designed from the failure modes in parent
   §8, not from tested output comparisons. Edit them in place as you learn what your model actually
   does; the templates are a starting point, not a specification.
2. **No AI vendor or model is named.** Model behaviour differs, and the parent file's attribution
   requirement is vendor-agnostic. Some prompts will need tightening or loosening per model.
3. **Deadlines and character limits are carried from the parent file and are 2026-season values in
   places.** Re-verify against FIRST when the 2027 award pages re-issue. `00_FIRST_AI_POLICY_VERIFIED.md`
   flags the 500 / 10,000 figures as 2026 calibration values explicitly.
4. **P-16's Gene Haas amounts stay UNVERIFIED by design.** Do not remove those flags when you edit;
   they are the only thing preventing a $3,000 line item that may not exist.
5. **The preamble must be kept in sync with `team-kb/CLAUDE.md` and `reference/team_capacity.yaml`.**
   Two copies of the team's numbers will drift. When they disagree, `team_capacity.yaml` wins.
6. **BIOCORE's rules do not exist yet.** Every prompt that touches game strategy will produce
   fabrication until 2027-01-09. The preamble says so, but a model will still try.
