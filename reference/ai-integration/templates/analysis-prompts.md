# Analysis & Scouting Prompt Library — BIOCORE (FRC 2027)

**Purpose:** ready-to-paste prompts for the analysis and scouting half of the AI plan. Every prompt
here carries a **verification line** — the command that proves the model did not make it up. A prompt
without a verification line does not belong in this file.

**Companion file:** `reference/ai-integration/03_ai_for_analysis_and_scouting.md` (why each of these
exists, what it costs, and where it fails).

**Not duplicated here:** kickoff manual-comprehension prompts (`KICKOFF_PLAYBOOK.md` §P1–P10) and
strategy-scoring prompts (`STRATEGY-RANKING-SYSTEM.md` §8.1–8.8). Those are the *strategy* pipeline.
This file is the *data* pipeline. Use both.

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Prompt shape executed and its verifier run in this project |
| **[H]** HISTORICAL-PATTERN | Shape holds across 2023–2026; BIOCORE nouns will differ |
| **[S]** SPECULATION | Untested against a live BIOCORE manual — flagged inline |

**Standing attribution** (required by FIRST — see `../00_FIRST_AI_POLICY_VERIFIED.md`). Paste into
every artifact any of these prompts touches:

> Analysis assisted by Team #### and [model name]. All rule citations verified against the
> official Game Manual by `tools/cite-check.py`. Conclusions and decisions are the team's.

---

## §0 — The two rules that govern every prompt below

1. **Never let the model recall a rule. Paste extracted text.** All prompts assume you feed the model
   text produced by `tools/ingest-manual.sh` / `tools/rule-inventory.py`, not the model's memory of a
   manual it saw in training. A model's memory of FRC manuals is a memory of *previous* seasons, and
   it will be confidently, specifically wrong.
2. **Every rule claim carries a rule ID, and every rule ID must survive `cite-check.py`.**

```bash
python tools/cite-check.py 2027 the-answer.md --baseline 2026   # exit 1 == do not ship
```

---

# A. Manual analysis

## A1 — Scoped rule extraction (the workhorse) [C on 2026]

**When:** any question of the form "what do the rules say about X".
**Inputs:** output of `python tools/rule-show.py 2027:/regex/`, pasted whole.

```text
You are reading extracted text from the official FRC 2027 BIOCORE Game Manual. The text below is
the ONLY source you may use. You have prior-season FRC knowledge; it is WRONG for this manual and
you must not use it.

<<<RULES
{paste tools/rule-show.py output}
RULES>>>

Question: {question}

Answer in this format and nothing else:
1. ANSWER - two sentences maximum.
2. CITATIONS - every rule ID you relied on, each followed by a verbatim quote of no more than 20
   words from the text above, in double quotes.
3. NOT ANSWERED BY THIS TEXT - every part of the question the pasted text does not settle.
   If the text does not settle the question at all, section 1 must say exactly:
   "NOT DETERMINABLE FROM THE PROVIDED TEXT."
4. Q&A CANDIDATE - if section 3 is non-empty, write the question as you would submit it to the
   official Q&A: one sentence, one rule ID, no preamble.
```

**Verify:** `python tools/cite-check.py 2027 answer.md`. Section 3 coming back empty on a hard
question is itself a red flag — re-run with a narrower paste.

## A2 — Contradiction and interaction hunt

**When:** Phase 4 of `KICKOFF_PLAYBOOK.md`, and after every Team Update.

```text
Below are {n} extracted rules from the FRC 2027 BIOCORE manual, complete with rule IDs.

<<<RULES ... RULES>>>

Find PAIRS of rules that interact in a way a reasonable team could read two different ways.
For each pair output one row:

| Rule A | Rule B | Scenario where they collide | Reading 1 | Reading 2 | Which reading favours us | Q&A question, one sentence |

Rules:
- Both rule IDs must appear verbatim in the text above. If you cannot find a second rule, do not
  invent one - output the single rule with Rule B blank.
- A pair is only interesting if the two readings imply DIFFERENT ROBOT DESIGNS or DIFFERENT DRIVER
  BEHAVIOUR. Discard anything that is merely wordy.
- Rank by (how much the design changes) x (how cheap the Q&A question is to ask).
- Maximum 12 rows. Fewer good rows beats more bad rows.
```

**Verify:** `cite-check.py`, then cross-check survivors against `reference/QA-AMBIGUITY-HOTSPOTS.md`
— rules with historically high Q&A volume are where this pass pays. Survivors feed the Q&A list
(`KICKOFF_PLAYBOOK.md` §4.3, §6.4).

## A3 — Team Update regression check

**When:** the morning after every Team Update, alongside `tools/teamupdate-diff.py`.

```text
DIFF of the BIOCORE Game Manual between {label_old} and {label_new}:

<<<DIFF ... DIFF>>>

Our current design commitments and the rule each depends on:
<<<COMMITMENTS
{paste strategies/CONSTRAINTS.md}
COMMITMENTS>>>

For each changed rule ID in the diff, answer only:
- BREAKS: which commitment (by name) is now illegal or impossible. Quote the changed words.
- NARROWS: which commitment still works but with less margin. Give the new number.
- OPENS: which strategy we previously discarded is now viable again.
- NO EFFECT: rule IDs only, no commentary.

Do not summarise the diff. Do not restate unchanged rules.
```

**Verify:** `cite-check.py 2027 out.md --baseline 2027` against the previous ingest label, then
`tools/rule-show.py` every BREAKS rule by hand before you cut anything from the robot.

## A4 — Defined-term extraction (the free entity index) [H]

FRC writes defined game terms in ALL CAPS. That is a free, exact, no-embedding index.

```text
From the text below, extract every ALL-CAPS defined term. For each: the term, the manual's own
definition (verbatim), and the section it is defined in. Ignore acronyms in the stop list.
Output as TSV, one term per line, no commentary. If a term is USED but never DEFINED in this
text, put it in a second block headed UNDEFINED - those are the ambiguity hotspots.

STOP LIST: {paste tools/caps_stoplist_frc.txt}
<<<TEXT ... TEXT>>>
```

**Verify:** every extracted definition must be `grep`-able in the extracted manual text. The
UNDEFINED block feeds A2 and the Q&A list.

---

# B. Scouting schema generation — kickoff day

## B1 — Derive the gap fields for BIOCORE [S until the manual exists]

**When:** kickoff day, after Phase 1 of `KICKOFF_PLAYBOOK.md`. Do **not** ask a model for "a scouting
schema" — it will hand you 60 fields, most of which FMS already publishes for free.

```text
Context you must accept as given:
- FIRST's FMS publishes, free, for every team at every event: Ranking Score, Avg Match, Avg Auto,
  Avg <endgame structure>, Record (W-L-T), DQ, Played, Total RP. We will never scout these.
- We have 3 to 5 scouts available during a match cycle. Not 6. This is fixed and not negotiable.
- Our existing 22-field gap schema is below. It was derived for prior seasons.

<<<CURRENT SCHEMA
{paste: python tools/scouting-plan.py schema}
CURRENT SCHEMA>>>

<<<BIOCORE SCORING RULES
{paste the scoring action ledger from KICKOFF_PLAYBOOK.md 1.2 and the ranking formula from 1.6}
BIOCORE SCORING RULES>>>

Produce exactly three lists:
1. KEEP - fields that still capture something FMS will not publish in BIOCORE. One clause on why.
2. RETIRE - fields BIOCORE's scoring makes redundant BECAUSE FMS will now publish it. Name the
   FMS column that replaces each.
3. ADD - new gap fields BIOCORE specifically requires. For each: field name, type, and the
   sentence "FMS cannot publish this because ___". If you cannot complete that sentence, the field
   does not go in the schema.

Hard cap: KEEP + ADD must total 24 fields or fewer, and no more than 14 of them may be recorded
DURING a match. A scout watching two robots has about 8 seconds of attention per robot per cycle.
```

**Verify:** count the fields. Then time one student filling the form while watching a 2026 match
video. If a full match cannot be recorded in real time, the schema is too big — cut from ADD first.

## B2 — Schema to app config

```text
Convert this schema to a {ScoutingPASS | QRScout} config file. Field types must map to the app's
own supported input types only - list any field whose type has no clean equivalent instead of
approximating it. Preserve field order: pre-match, auto, teleop, endgame, post-match. Keep the
QR payload under {n} characters; if it will not fit, tell me which fields to shorten to codes
rather than silently truncating.

<<<SCHEMA
{paste: python tools/scouting-plan.py schema --json}
SCHEMA>>>
```

**Verify:** load the config in the real app, fill one match, scan the QR with a phone, confirm the
decoded row parses. **Do this in December, not at the event.**

---

# C. Scouting data quality

## C1 — Anomaly detection (run after every 12 matches)

```text
Below is our scouting data as CSV, one row per (match, team, scout).

<<<CSV ... CSV>>>

Find data-quality problems only. Do NOT analyse robot performance. Report:
1. SCOUT DISAGREEMENT - same team+match recorded by two scouts with materially different values.
   Give the field and both values.
2. IMPOSSIBLE - values violating the game's own limits (cycle_count above what the match length
   allows, endgame_time_s longer than the endgame period, totals above the theoretical max).
3. STUCK SCOUT - a scout whose values for a field have zero variance across 6+ matches.
4. DEFAULT DRIFT - a field where >60% of rows equal the form's default. That field is probably not
   being filled in; it should be cut or made mandatory.
5. MISSING - (match, team) pairs present in the TBA schedule but absent from this data.

Output columns: type, scout, match, team, field, observed, why_suspicious.
Rank by how much the error would move a pick-list position. Do not fix anything. Do not speculate
about causes beyond the five categories.
```

**Verify:** every flagged row is eyeballed by a human against the match video or the TBA score
breakdown before anything is changed. **Never let the model edit the data** — it flags, you fix.

## C2 — Cross-check scouting against free FMS data

```text
Two tables. Table 1 is our scouting data aggregated per team. Table 2 is the official TBA event
rankings (Avg Match, Avg Auto, Avg <endgame>, DQ, Played).

<<<OURS ... OURS>>>
<<<TBA ... TBA>>>

For each team compute the disagreement between what we recorded and what FIRST published. Report
only teams disagreeing by more than 25%. For each, state which explanation is likelier and what
single observation would distinguish them:
  (a) our scouts mis-recorded,
  (b) the team's performance genuinely changed across the event,
  (c) the team plays defense, so its low published score is not a low capability.

(c) is the interesting one. Flag it explicitly - it is the case where our data is RIGHT and the
public number is misleading.
```

**Why this is the highest-value scouting prompt here:** case (c) is exactly the information free data
cannot give you (`SCOUTING-PLAN.md` §3, `defense_quality`). It is also the case that most often
changes a draft position.

## C3 — Natural-language query over scouting data

Do **not** let a model answer questions by reading a pasted CSV. It does arithmetic wrong past a
handful of rows and reports the wrong answer in a confident tone. Make it write the query instead.

```text
Our scouting data lives in {scouting.csv | a SQLite table `scouting`}. Schema:

<<<SCHEMA ... SCHEMA>>>

Write a single {SQL query | pandas expression} answering: "{question}".
Rules:
- Output ONLY the query, then one sentence naming which rows it excludes and why.
- No column may appear that is not in the schema above.
- If the question cannot be answered from these columns, name the missing column and write no query.
- Ties, nulls, and teams with fewer than 4 recorded matches must be handled explicitly, not ignored.
```

**Verify:** run the query. Spot-check the top and bottom row by hand against the raw data. A query
you have not spot-checked is a rumour.

---

# D. Reports and briefs

## D1 — Pre-match brief (the 90-second one) [S — shape only until BIOCORE]

Normally produced by `tools/prematch-brief.py` (companion file §5); this prompt is the manual
fallback when you are doing it in the stands.

```text
Write a pre-match brief for the drive team. Data:

MATCH: {key} - us {team} on {alliance}
PARTNERS: {rows: team, Avg Match, Avg Auto, Avg <endgame>, DQ, our sigma, our notes}
OPPONENTS: {same}
MONTE CARLO: {paste tools/match-sim.py sim output}

Format - exactly this, nothing else, fits on one index card:

ONE-LINE PLAN: {what we do differently this match, imperative voice, max 15 words}
PARTNER {n}: {what they are good at, and the ONE thing not to collide with them on}
PARTNER {n}: {same}
THREAT: {the single opposing robot that decides this match, and what it does}
IF IT GOES WRONG: {the fallback, one line}
CONFIDENCE: {P(win) from the simulation, plus the words "the model does not know about
reliability, defense or driver skill"}

Do not include statistics the drivers cannot act on. If a number does not change a decision, cut it.
```

**Verify:** hand it to a driver. If they read past 20 seconds, it is too long. Cut, do not reformat.

## D2 — Post-event report (Thursday night, and after the event)

```text
Inputs: our scouting data, the TBA rankings, our match record.

Write the report the strategy lead would write, in this order:
1. WHAT WE GOT WRONG - every team whose pre-event ranking was off by 8+ places, and the specific
   field in our data that would have predicted it if we had weighted it correctly.
2. OUR OWN NUMBERS - our Avg Match, Avg Auto, Avg <endgame>, DQ, and the trend across the day.
3. THE THREE ROBOTS TO REMEMBER - for next event or next year.
4. ONE PROCESS CHANGE - a single change to how we scout, stated as a diff to the schema.

Section 1 is the point of this document. Do not soften it. Do not open with a summary of what
happened; we were there.
```

## D3 — Pick-list narrative (assist, not decision)

```text
Here is our fused pick list: free FMS columns, our gap-scouting aggregates, and the simulated
marginal win probability for each candidate (tools/match-sim.py marginal).

<<<DATA ... DATA>>>

For each of the top 12 candidates write exactly two sentences: what they add to an alliance built
around us, and the specific risk of picking them. Then answer one question in one paragraph:
"Which candidate does the data most disagree about?" - the team where the public numbers and our
scouted numbers point in opposite directions.

You are NOT ranking them. You are NOT recommending. The ranking is the students'.
```

**Verify:** the human rule (companion file §7) — the model may describe, may order by an explicit
stated metric, and may flag disagreement. It may not choose.

---

# E. Simulation and video

## E1 — Encode the BIOCORE scoring rules for the simulator [S]

```text
From the scoring section below, produce a JSON object with exactly these keys:
  actions: [{name, phase(auto|teleop|endgame), points, quoted_rule_id, quote}]
  rp:      [{name, condition_in_plain_english, threshold_if_numeric, quoted_rule_id}]
  match_seconds: {auto, teleop, endgame}
Every entry MUST carry the rule ID and a verbatim quote under 20 words. If a point value is
conditional, emit one entry per condition rather than an average. If you cannot find a value in
the text, use null - never estimate.

<<<SCORING TEXT ... TEXT>>>
```

**Verify:** `python tools/cite-check.py 2027 rules.json`, then hand-check every `points` value
against the manual's scoring table. A wrong point value silently corrupts every downstream
simulation and still looks plausible.

## E2 — Match video: timestamped event log (semi-automated) [S]

Feed the model a **timestamped log plus your own sparse annotations**, never raw video.

```text
Below is a timestamped log from one match: {source - our tablet taps, or a manual scrub log}.
Our robot is {team}, {alliance} station {n}.

<<<LOG ... LOG>>>

Produce a cycle table: cycle number, start ts, end ts, duration, outcome (scored|missed|dropped|
defended), one short note. Then: mean cycle time, the slowest cycle, and the single largest
recoverable loss in seconds with the timestamp to review.

Only report events present in the log. Do not infer events between timestamps. If the log is too
sparse to segment cycles, say so and name the minimum extra annotation that would fix it.
```

**Verify:** scrub to the two timestamps it names. This prompt exists to point a human at the right
20 seconds of a 2.5-minute video — not to replace watching it.

---

# F. Red-team prompts

## F1 — Attack our own analysis

```text
Below is our analysis and the decision it recommends.

<<<ANALYSIS ... ANALYSIS>>>

You are a rival team's strategy lead who wants us to be wrong. Produce:
1. The three assumptions that, if false, break the conclusion - ranked by how likely they are false.
2. For each, the cheapest observation that would test it, and when we could make it.
3. The strongest version of the opposite conclusion, argued in good faith, one paragraph.
4. Any place we treated a model output as a measurement.

Do not hedge. Do not be balanced. Do not compliment the analysis.
```

## F2 — Sample-size and overfitting check

```text
{paste a claim derived from scouting or TBA data, with the n it rests on}

Answer only:
- How many observations does this claim actually rest on, per team?
- What is the plausible range of the underlying quantity given that n?
- Would the conclusion flip if the two most extreme observations were removed?
- Is this a real effect, or the model fitting noise in a 12-match sample?
If n is under 6 per team, say so first and loudly.
```

> **Why F2 matters:** a qualification schedule gives 8–12 matches per team. Almost every confident
> claim a model makes about one team at one event rests on fewer than a dozen observations.
> `tools/match-sim.py` exists partly to make that uncertainty visible instead of letting a point
> estimate hide it.

---

## Files written by this pass
- `reference/ai-integration/templates/analysis-prompts.md` (this file)

## Known limitations
- Every prompt whose inputs come from the BIOCORE manual is **[S]** until 2027-01-09. Shapes derive
  from 2023–2026 manuals; BIOCORE nouns, phases and the endgame structure will differ.
- Prompt wording is model-dependent. These assume a long-context model that will accept a full
  pasted rule set; a small-context model needs the chunking strategy in the companion file §1.
- The verification lines are the load-bearing part of this file. A prompt run without its verifier
  is not covered by anything written here.