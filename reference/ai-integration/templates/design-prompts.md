# Design prompt templates — copy, fill the brackets, paste

**Purpose:** the prompts in this file are the ones that survived testing. Each has a stated
*failure mode* — the way it goes wrong — because a prompt template without a failure mode is a
sales pitch. Companion to [`../02_ai_for_design_and_cad.md`](../02_ai_for_design_and_cad.md).

**Attribution is mandatory.** *FIRST* permits AI use and requires credit
([`../00_FIRST_AI_POLICY_VERIFIED.md`](../00_FIRST_AI_POLICY_VERIFIED.md)); the sample form is
`"Essay created by Team XXXX and ChatGPT."` Put an equivalent line in the repo README, on every
CAD file description that came out of a generated script, and on every award submission.

**Evidence labels**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Tested by this pass, or quoted from a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Practice observed across FRC seasons; not a rule |
| **[S]** SPECULATION | Judgement call. Flagged |
| **UNVERIFIED** | Not checked. Check it |

> **BIOCORE guard.** BIOCORE's manual does not exist until **2027-01-09 12:00 ET**. Every prompt
> below that refers to "the manual" means *the manual you have in hand at the time you run it* —
> in the fall that is the 2026 REBUILT manual as a rehearsal, and from kickoff it is BIOCORE.
> Never let a model answer a BIOCORE rules question from memory. Its training data cannot contain
> BIOCORE. If it answers confidently, it is fabricating.

---

## 0. The 60-second workflow

```bash
# Run from the repository root.

# 1. Rehearse the constraint extraction on a manual you already have (2026 REBUILT).
#    Paste template §1 with the rules text this produces. 2026_rules_full.txt is not in the
#    repository, because FIRST's text is not redistributed; bash tools/rebuild-corpus.sh rebuilds it.
grep -A3 -E '^### R(10[2-9]|1[12][0-9]|40[1-9])\b' \
    research/rule_inventories/2026_rules_full.txt | cut -c1-300 | head -80

# 2. Check any AI dimensional claim against the machine-readable inventory, not against the chat.
python tools/rule-show.py R103 2>/dev/null || grep -n "R103" research/rule_inventories/2026_rules.tsv

# 3. Every number an AI gives you about a mechanism gets re-derived here before it is believed.
python reference/ai-integration/calculators/drivetrain.py --sweep
python reference/ai-integration/calculators/elevator_arm.py elevator
python reference/ai-integration/calculators/cg_tip.py

# 4. Cycle time / expected value: DO NOT ask a model. Run the model that exists.
python tools/cycle-model.py --game rebuilt --sweep
```

---

## 1. Extract every dimensional constraint from the game manual

**Use at:** kickoff +2 hours, and again after every Team Update.
**Failure mode:** the model *summarises* instead of *extracting*, silently dropping the one rule
that kills your design. Mitigate by demanding a rule ID on every row and rejecting any row without
one. Also: models paraphrase numbers. Verify each row against the text yourself. **[C]** tested.

```text
You are a rules analyst for an FRC team. I am pasting the raw text of sections [X] of the
[SEASON] game manual below.

TASK: extract EVERY numeric or geometric constraint that could affect a robot's physical design.
Output a markdown table with EXACTLY these columns:

  rule_id | verbatim_quote | quantity | value | unit | tolerance | applies_to | design_consequence

RULES FOR YOUR OUTPUT:
1. Every row MUST have a rule_id that appears literally in the text I pasted. If you cannot find
   the rule ID, do not emit the row.
2. verbatim_quote must be copied character-for-character from the text, max 25 words.
3. If a value has a tolerance or a "nominal" qualifier, put it in the tolerance column. Never
   silently round.
4. Do NOT use any knowledge about this game from outside the text I pasted. If something is
   ambiguous, add a row with rule_id and the word AMBIGUOUS in the value column.
5. After the table, list separately: (a) constraints stated in the text that you could NOT
   assign a rule ID; (b) dimensions a robot designer needs that this text does NOT specify.

Section (b) is the most valuable part of your answer. Be thorough about it.

TEXT:
[paste]
```

Then: cross-check the output against `research/rule_inventories/` with `tools/rule-inventory.py`.
List (b) — the missing dimensions — feeds directly into
[`../../QA-AMBIGUITY-HOTSPOTS.md`](../../QA-AMBIGUITY-HOTSPOTS.md) and becomes your Q&A questions
on 2027-01-13.

---

## 2. Turn the extracted constraints into a design spec

**Use at:** kickoff +6 hours, before anyone opens CAD.
**Failure mode:** the model invents a "typical" value for anything you left out. Force it to write
UNKNOWN. **[C]** tested — models will happily fill a blank with a plausible number.

```text
Here is a table of extracted game constraints [paste the §1 output] and here is our team's
capacity model summary:

  - 15 students, 1 experienced mentor, ~599 effective build-hours to a Week 1 event
  - MAXIMUM 2 novel mechanisms beyond the drivetrain. This is a hard constraint, not a target.
  - $2,500 discretionary robot budget over the Kit of Parts
  - tooling: bandsaw, drill press, 3D printer. No mill, no CNC router, no lathe.

Write a DESIGN SPEC for a single scoring mechanism with these sections:

  1. Functional requirement (one sentence: what it must do to the game piece)
  2. Interface envelope: every dimension the mechanism must fit within or reach, each traced to
     a rule_id from my table. Write UNKNOWN, in capitals, for any dimension the table does not
     supply. Do not estimate. Do not use a "typical FRC" value.
  3. Load cases: mass, force, and the worst-case orientation
  4. Cycle-time budget: seconds per scoring action, and what that implies for actuator speed
  5. The three things that would make this mechanism fail in match 40 of an event
  6. What must be prototyped in cardboard/wood before any CAD is drawn

Do not propose a specific mechanism architecture. That is the next step and I want the spec to
be architecture-neutral so it can judge more than one.
```

---

## 3. Trade study / decision matrix

**Use at:** kickoff day 2, after prototyping, before CAD.
**Failure mode:** the model assigns weights that flatter whichever option you mentioned first, and
scores are anchored to its own prose. Mitigate by **supplying the weights yourself** and forcing an
evidence column. Then run [`../../../tools/score-strategy.py`](../../../tools/score-strategy.py)
and treat the AI matrix as a second opinion, not the answer. **[S]**

```text
Build a weighted decision matrix comparing these mechanism architectures for [FUNCTION]:
  A) [option]   B) [option]   C) [option]

Criteria and weights are FIXED by me. Do not change them, do not add criteria:
  build hours (weight 25) | cost (20) | reliability under repeated cycles (20) |
  programming difficulty (15) | tooling required vs bandsaw+drill press+3D printer (10) |
  weight added to the robot (10)

For each cell output: score 1-5, then a one-clause justification, then an EVIDENCE tag:
  [C] you can cite a specific FRC team, year, or published design
  [H] a pattern you have seen repeatedly but cannot pin to a source
  [S] your own inference
Any cell you cannot tag [C] or [H] must be tagged [S], and I will discount it.

Then, separately and in plain prose:
 - which criterion is doing the most work in the final ranking, and what happens to the ranking
   if I halve its weight
 - the strongest argument AGAINST the option that scored highest
 - what physical test, doable in under 2 hours with cardboard and a drill, would resolve the
   biggest uncertainty in this matrix
```

The last bullet is the whole point. A trade study that does not end in a prototype test is a
document, and documents do not score points.

---

## 4. CADQuery / build123d parametric part generation

**Use at:** any time. This is the strongest genuine CAD capability the tools have. **[C]**
**Failure mode:** the model hallucinates API methods that do not exist in the installed version,
and confuses CADQuery with build123d syntax. Mitigate by pasting the version and demanding it
compile. Always run the script; never trust the code by reading it.

```text
Write a [CADQuery 2.x | build123d] script that generates the following part parametrically.

CONSTRAINTS ON YOUR OUTPUT:
 - Put EVERY dimension in a single parameters block at the top, with units in the variable name
   (e.g. plate_thickness_in). No magic numbers below that block.
 - Use only API calls that exist in [library + version]. If you are unsure a method exists, use a
   more primitive construction instead. Do not invent methods.
 - The script must run headless and export STEP and DXF.
 - Add an assert block at the end that checks: overall bounding box, mass at [material density],
   and that every hole centre is at least [edge_distance] from an edge.

THE PART:
 - [describe: a gusset / a plate / a spacer / a bearing block]
 - fits [tube size] tube, [hole pattern] on [spacing] centres
 - must clear [interference]
 - material [6061-T6 aluminium / 3D printed PETG], thickness [X]

After the script, list the three parameter values most likely to need changing after the first
test fit, and why.
```

**Then, without exception:** run it, open the STEP, and check it against the physical part.
A script that runs is not a script that is right.

---

## 5. FeatureScript / Onshape

**Use at:** only if someone on the team already knows Onshape well. **[S]**
**Failure mode:** FeatureScript is a small, fast-moving, weakly-documented language; generated
FeatureScript fails to compile far more often than generated Python. Budget debugging time.

```text
Write an Onshape FeatureScript custom feature that [does X].

 - Target the current FeatureScript standard library version; state which version you assumed.
 - Use only documented std functions. If you use anything you are less than certain about, mark
   the line with // UNCERTAIN and say what to check in the FeatureScript docs.
 - Include the precondition block with proper UI parameter definitions and sensible bounds.
 - Explain, in comments, what each query is selecting and why.

After the code: list every std function you called, and for each, one line on what it does. I am
going to check that list against the documentation before I paste anything into Onshape.
```

The "list every function you called" trailer is the useful half. It converts a black box into a
checklist a student can verify in ten minutes.

---

## 6. DFM review of a design description

**Use at:** before every fabrication order or 3D print queue.
**Failure mode:** generic manufacturing advice aimed at a machine shop you do not have. Fix by
stating your tooling *and its absence* explicitly. **[C]** — stating the negative constraints is
what makes this prompt work.

```text
Design-for-manufacturability review. Our shop is EXACTLY this and nothing more:
  - horizontal bandsaw, drill press, hand tools, taps, a rivet gun
  - one 0.25 mm-nozzle FDM printer, 250 x 210 x 210 mm build volume, PETG and PLA only
  - NO mill, NO lathe, NO CNC router, NO welding
  - we can outsource 2D flat sheet cutting (aluminium up to 0.25 in) with a 7-day turnaround
  - the students doing the work are 15-18 and mostly first- or second-year

Here is the design: [describe, or paste dimensions, or attach a CAD screenshot]

Review it and produce:
 1. Every feature that CANNOT be made with the tools above, and the nearest equivalent that can.
 2. Every feature that CAN be made but requires a fixture, jig, or setup the students will get
    wrong on the first attempt. Say what the jig is.
 3. Tolerance stack-up: which dimensions are actually critical, and which we can be sloppy on.
    Be specific about which two features must be concentric or square to each other.
 4. Fastener and access review: can a hand tool physically reach every fastener AFTER assembly?
    Name any fastener that becomes inaccessible.
 5. The single change that most reduces fabrication hours without changing function.

Do not suggest anything requiring a machine we do not have. If the honest answer is "outsource
this", say so and estimate the flat-pattern area in square inches.
```

Item 4 catches more real problems than the rest combined. **[H]**

---

## 7. Photograph a prototype or whiteboard sketch (multimodal)

**Use at:** kickoff weekend prototyping, and after every whiteboard session.
**Failure mode:** the model is confident about what it sees and wrong about scale, and it cannot
see behind anything. Always include a known-length object in the frame and say what it is.

```text
[attach photo]

This is a cardboard-and-wood prototype of [FUNCTION] for our FRC robot. The [ruler / 12 in
speed square / standard game piece] in the frame is [LENGTH] for scale.

Tell me:
 1. What you can actually see, and what is hidden or ambiguous. Do this FIRST and be blunt about
    what you cannot determine from this angle.
 2. Estimated dimensions of the major elements, WITH an error bar, using the scale reference.
 3. The load path: for each member, whether it is in tension, compression, or bending, and which
    member you expect to fail first when this is made in aluminium at 3x this speed.
 4. Three specific things to measure or test before we commit this to CAD.
 5. What second photo, from what angle, would most reduce your uncertainty?

Do not tell me it looks good. Tell me what is going to break.
```

Question 5 turns one photo into a deliberate photo sequence. **[S]** but consistently useful.

---

## 8. Review a CAD screenshot for packaging problems

**Use at:** every design review. **[S]** — this works but is the weakest of the multimodal uses,
because a screenshot has no depth and the model cannot rotate the model.

```text
[attach 3-4 CAD screenshots: iso, top, side, and one with the mechanism in its extended position]

FRC robot assembly. Frame perimeter is [W] x [L] in, bumpers add [T] in per side. Height limit
[H] in. Check for:
 1. Anything that appears to extend past the frame perimeter, in ANY of these views. Call it out
    even if you are unsure — I would rather check a false positive.
 2. Collisions or near-misses between the mechanism sweep and: bumpers, the electrical board,
    the battery, the drivetrain.
 3. Wire and pneumatic routing: is there a path from [component] to [component] that does not
    cross a moving part? Say where you would run it.
 4. Battery access: can a human swap the battery in under 30 seconds without removing anything?
 5. Anything that looks like it will be impossible to assemble in the order the geometry implies.

State explicitly what you CANNOT judge from a screenshot. I know you cannot see the back.
```

**The honest limitation, stated so nobody over-trusts this:** a CAD screenshot review finds
*obvious* packaging errors — the kind a fresh pair of human eyes finds. It does not replace
Onshape's or Fusion's own interference detection, which is exact, free, and takes one click.
**Run the interference check first, then use this for the things geometry checks do not catch**
(assembly order, hand access, wire routing).

---

## 9. Competitor robot photos and match video

**Use at:** week 1 events broadcast before your own event; and between your quals and elims.
**Failure mode:** the model will confidently identify mechanisms it cannot see and invent team
numbers. Never let it name a team. **[C]** — team-number hallucination is reliable and severe.

```text
[attach photos or video frames]

These are frames from an FRC match. Describe ONLY what is visible.

 1. For each robot, describe its drivetrain type, its intake style, and its scoring mechanism —
    from what you can SEE. Where you are inferring rather than seeing, say "inferring".
 2. Do NOT guess team numbers. If a number is legible, quote it; otherwise write "not legible".
 3. Cycle observations: for the robot [in the LEFT frame / with the RED bumpers], time from
    [pickup] to [score] if the frames allow it; say "cannot determine" if they do not.
 4. What mechanism choices are common across these robots? What is unique to one?
 5. What would you scout about these robots that a photo cannot tell you?

Frames may be blurry or partial. "Cannot determine" is a correct and useful answer.
```

Feed the output into [`../../SCOUTING-PLAN.md`](../../SCOUTING-PLAN.md) as qualitative notes only.
Quantitative scouting comes from TBA and from your own scouts, never from a model.

---

## 10. BOM generation and cost-rule compliance

**Use at:** before every order. **[C]** for the checking half; **[S]** for the generation half.
**Failure mode:** models invent part numbers and prices with total confidence. This is the single
most dangerous AI failure for a budget-constrained team.

```text
Here is a mechanism description: [paste]
Here is our verified parts catalogue (prices fetched 2026-08-22): [paste the relevant YAML from
reference/bom/parts_*.yaml]

Produce a bill of materials as a table:
  part | source | part_number | qty | unit_price | ext_price | IN_CATALOGUE?

RULES:
 - The IN_CATALOGUE column is YES only if the part number appears literally in the YAML I pasted.
 - For anything not in the catalogue, put NO, leave part_number and unit_price BLANK, and add it
   to a separate "must be researched" list. Do not guess a part number. Do not guess a price.
   A guessed price in a budget is worse than a blank.
 - Add a raw-stock line for tube, sheet, and fasteners with quantities, not prices.
 - Total the ext_price column for catalogue items only, and state the count of unpriced items.

Then answer: what fraction of this mechanism's cost is in the [most expensive category], and what
is the cheapest single substitution that keeps the function?
```

**Then run the real tool.** [`../../../tools/bom-builder.py`](../../../tools/bom-builder.py) and
[`../../bom/`](../../bom/) are the cost authority; the AI output is a draft to be reconciled against
them, and the reconciliation is where the errors surface.

---

## 11. Re-deriving an AI's engineering claim (the discipline prompt)

**Use at:** every time a model states a number about motors, speeds, forces, or currents.

```text
You just told me [CLAIM]. Do not defend it.

Instead: write the derivation as a short Python script using ONLY these inputs, which I am
giving you: [list the inputs]. The script must print each intermediate quantity with its units.
Do not import anything except math. Do not use any constant I did not supply — if you need one,
stop and ask me for it.
```

Then run it, and run
[`../calculators/`](../calculators/) on the same inputs. If the two disagree, the calculator wins,
because the calculator has been run before. **[C]** — this pattern caught a factor-of-seven error
in a supply-vs-stator current calculation while `drivetrain.py` was being written for this pass.

---

## 12. The anti-prompt — things not to ask

**[C]** These fail in ways that cost money or points. Named so nobody wastes an afternoon.

| Do not ask | Why | Do this instead |
|---|---|---|
| "Design our robot for BIOCORE" | The model has no BIOCORE data. It will produce last-year's robot with new words | Extract constraints (§1), then spec (§2), then trade study (§3) |
| "What's the best gear ratio for our drivetrain?" | It will produce a plausible community-consensus number with no derivation | `python calculators/drivetrain.py --sweep` |
| "Generate a CAD model of our elevator" | Text-to-CAD cannot produce a manufacturable FRC assembly. §2 of the parent file explains at length | CADQuery for individual parts (§4); a human in Onshape for assemblies |
| "Is this design legal?" | Legality is a rules question. Model answers are ungrounded and the stakes are inspection | `tools/rule-inventory.py`, then the Q&A system |
| "What did team [N] build in [year]?" | Team-number and design hallucination is reliable | TBA, `tools/tba_*.py`, and your own eyes |
| "Estimate our cycle time" | Already solved, deterministically | `python tools/cycle-model.py` |
| "Write the whole subsystem's code" | Untested generated code on a 115 lb machine. See the policy file, item 3 | Generate scaffolding; humans review before anything actuates |

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/ai-integration/templates/design-prompts.md` | this file |

## Known limitations

- **Every prompt here was designed and reasoned about; only some were end-to-end tested.**
  §4 and §11 were exercised while building the calculators in this pass **[C]**. §1, §3, §6 are
  refinements of patterns with a strong track record **[H]**. §5, §7, §8, §9 are **[S]** — the
  reasoning is sound, the specific wording is untested against a real BIOCORE artefact, because
  no BIOCORE artefact exists.
- **Prompt behaviour is model- and version-dependent.** These were written against the models
  available in August 2026 and will drift. The *structure* (demand citations, demand UNKNOWN,
  demand a re-derivation) is durable; the exact phrasing is not.
- **No prompt here makes a model's output trustworthy.** They make it *checkable*, which is a
  different and smaller claim. The checking step is not optional and is not automatable.
