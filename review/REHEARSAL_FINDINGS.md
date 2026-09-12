# REHEARSAL FINDINGS — kickoff-day autorun, dry run 2026-08-22

**What was tested:** the five-step autorun in `CLAUDE.md`, executed literally, against
`manuals/archive/frc/2026_REBUILT_GameManual.pdf` standing in for BIOCORE.
**Run directory:** `review/V1_20260823T014011Z/`
**Outcome:** the pipeline ran end-to-end and produced a complete nine-section `REVIEW.md`. It also
**produced a silently wrong answer** on the first attempt and would have shipped it.

---

## 0. Verdict first

**Would this work on 2027-01-09 with no human intervention? — Yes mechanically, no substantively.**

Every script ran. Nothing crashed. Phase 1 took ~30 seconds, phase 2 ~10 seconds. The pipeline is
in far better shape than most kickoff-day plans.

**But the first complete pass produced a strategy ranking in which the three highest-achievability
candidates — the exact three archetypes the project's own corpus says small teams win with — were
all marked `T4 GATED` and effectively deleted, because of an undocumented vocabulary mismatch that
printed no error.** An agent with only `CLAUDE.md` and the briefing pack would have had no reason to
question that output. It looks exactly like a correct answer. That is the worst failure mode a
decision-support pipeline can have, and it is live in the repo today.

Fix Finding 1 and Finding 2 and the answer is yes.

---

## 1. Commands that failed

| # | Command | Error | Severity |
|---|---|---|---|
| 1.1 | `bash tools/RUN-KICKOFF.sh <manual> V1` | — none. Exit 0, 458-line briefing pack, 3 stubs. | OK |
| 1.2 | `bash tools/RUN-KICKOFF.sh --phase2 review/<dir>` | — none. Exit 0 both times. | OK |
| 1.3 | `python tools/bom-builder.py --list` | — none. 27 mechanism ids. | OK |
| 1.4 | **Writing `candidates.yaml` via a Bash heredoc** | `/usr/bin/bash: -c: line 53: unexpected EOF while looking for matching '` — an apostrophe inside the YAML (`a partner's rate`) broke the quoted heredoc despite `<<'EOF'`. **Two files were silently lost** and had to be rewritten with the `Write` tool. | **MEDIUM** — costs 2–3 wasted tool calls on kickoff day and can truncate a file mid-write |
| 1.5 | FILL_ME preflight (deliberately re-broken to test) | Correctly refused: `!! game_def.json still contains FILL_ME placeholders.` `CLAUDE.md`'s claim that "phase 2 refuses to run otherwise" is **true and verified.** | OK |

**Not tested, and untestable before the season opens:** `bash tools/probe-2027-manual.sh --download`
(Step 1's fallback), and `reference/awards/kickoff_award_check.sh` (referenced by
`STRATEGY-RANKING-SYSTEM.md` §0 but **not** by `CLAUDE.md`). The probe is the only network-dependent
step in the whole autorun and it is the one step that has never been exercised against a real 2027
URL. **If it fails at 12:00 ET, the pipeline does not start.** Rehearse it against the 2026 CDN
before January.

---

## 2. `CLAUDE.md` instructions that were ambiguous, wrong, or impossible

### 2.1 **CRITICAL — `mfg_floor` has three mutually incompatible vocabularies and the wrong one is blessed**

`CLAUDE.md` line 100 says: *"`reference/team_capacity.yaml` is the authority for hours, headcount,
and budget. Never make a claim that contradicts it."* Following that instruction produces wrong
answers.

| Source | Accepted `mfg_floor` tokens |
|---|---|
| `reference/team_capacity.yaml` (**blessed by CLAUDE.md**) | `hand_tools`, `bandsaw_drillpress`, `router_cnc`, `mill_lathe`, `outsourced` |
| `reference/achievability_rubric.yaml` (**what `tools/score-strategy.py` actually reads**) | `hand`, `bandsaw+drill`, `3dprint`; soft `router`; hard `CNC` |
| `tools/bom-builder.py` / mechanism catalog | `hand_tools`, `bandsaw_drillpress`, `router_cnc`, `mill_lathe` |
| `candidates.yaml` stub | exactly one example: `bandsaw+drill` |
| `ACHIEVABILITY-RUBRIC.md` §2 A9 | prose only: "Hand tools", "Bandsaw + drill press", "Router / waterjet", "In-house CNC mill" |

`score-strategy.py:186` does `owned = set(tc["owned_manufacturing"]); if mfg not in owned: … fire G1`.
Any unrecognised string fires a **hard gate** and prints `needs '<your string>'; shop has [...]`.

**Observed damage:** using the `team_capacity.yaml` vocabulary, `hand_tools` — the *easiest*
manufacturing floor in the game — fired the machine-capability gate. Five of fourteen candidates
were falsely marked `T4 GATED`:

| id | Strategy | Before fix | After fix |
|---|---|---|---|
| S5 | Feeder/support (`ARCH` I6, **5/5** small-team record) | T4 GATED | **T1 GREEN, rank 1** |
| S4 | Pure defense | T4 GATED | T2 STRETCH |
| S12 | Choke-point denial | T4 GATED | T2 STRETCH |
| S3 | AUTO-only specialist | T4 GATED | T2 STRETCH |
| S1 | Full-field volume cycler | T4 GATED (wrong reason) | T4 GATED (**right** reason: G2 workstreams) |

**The #1-ranked strategy in the entire analysis was deleted by a typo-class error that produced no
error message.** The gate string is the only tell, and it reads like a legitimate finding.

**Fixes, in order of value:**
1. Make `score-strategy.py` **hard-fail on an unrecognised `mfg_floor`** instead of firing G1.
   An unknown token is a schema error, not a capability finding. One line.
2. Add an alias map (`hand_tools`→`hand`, `bandsaw_drillpress`→`bandsaw+drill`, `router_cnc`→`router`,
   `mill_lathe`→`CNC`) so both vocabularies work.
3. Put the legal token list **in the `candidates.yaml` stub as a comment**, next to the field.
4. Correct `CLAUDE.md` line 100 — `team_capacity.yaml` is *not* the authority for gate vocabulary.

### 2.2 **The REBUILT-baseline diff is self-referential when the manual is REBUILT**

Step 2 says the briefing pack contains *"added/removed rules vs. the REBUILT baseline"* and
*"new glossary nouns"*. In this rehearsal the manual **is** the baseline, so:

```
rules: 227  added=0  removed=0  changed=0
glossary: 100  added=0  removed=0
```

Three of the briefing pack's advertised sections were empty. `STRATEGY-RANKING-SYSTEM.md` §0
calls this diff *"the highest-value 60 seconds of the day."* **On kickoff day it will be populated
and it is the section I could not rehearse at all.** Nothing verified that the diff logic works on a
genuinely different manual. That is an unrehearsed critical path.

**Fix:** run the same pipeline with 2025 REEFSCAPE as the manual before January. It is on disk. That
exercises the diff for real and takes five minutes.

### 2.3 **`ingest-manual.sh` overwrites the BIOCORE slot with whatever you hand it**

The pipeline silently copied the 2026 REBUILT manual to
`manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf`. There is now a file named "BIOCORE game manual"
that is the 2026 game. On kickoff day a re-run with a wrong path, or a second rehearsal, poisons the
one directory the project treats as canonical — and `CLAUDE.md`'s trigger clause watches that exact
folder for `*BIOCORE*.pdf`, so **the rehearsal artifact is itself a valid autorun trigger.** A
future session could re-trigger the whole pipeline on REBUILT and never notice.

**Fix:** refuse to write into `manuals/2026-27_BIOCORE/` unless the source filename or the PDF's own
text contains "BIOCORE"; or name the copy after the source file. **Delete
`manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf` now.**

### 2.4 `review/<dir>` is never defined

Steps 3, 4 and 5 all say `review/<dir>`. Step 1 creates `review/V1_<stamp>/` where `<stamp>` is a
UTC timestamp printed only in phase 1's stdout. If the autorun is resumed in a fresh session, or
phase 1's output has scrolled, there is no stated rule for finding `<dir>`. Today `review/` is empty
so "newest directory" works by luck; after one real run plus this rehearsal it is ambiguous.

**Fix:** have phase 1 write `review/LATEST` (a file containing the path, or a junction) and say so
in `CLAUDE.md`.

### 2.5 Section 9 of the review is impossible in a rehearsal, and `CLAUDE.md` does not say so

Step 5 §9 mandates *"grade the 10 predictions in `research/04_biocore_community_intel.md` against the
real manual."* Two problems: **(a)** there are **eleven** predictions, not ten — P11 was added
2026-08-22 and `CLAUDE.md` was not updated; **(b)** grading BIOCORE predictions against REBUILT is
category-incoherent. I wrote §9 as a calibration exercise instead and labelled it as such. On the
real day the instruction is fine — but the count is wrong today and will drift again.

**Fix:** say "every prediction in the betting sheet", not "the 10 predictions".

### 2.6 Step 5 §2 asks for a number the model cannot produce correctly (see 3.2)

*"what one second of cycle time is worth per match and per 12-match schedule"* — the model prints
15.6 pts/match. The true REBUILT figure is ~10, because the model cannot represent the HUB duty
cycle. The instruction is right; the tool feeding it is wrong. **A team following the instruction
literally, without reading Table 6-3, would design to a 54%-inflated score all season.**

### 2.7 Minor

- `CLAUDE.md` never mentions `reference/awards/kickoff_award_check.sh`, which
  `STRATEGY-RANKING-SYSTEM.md` §0 step 5 calls a required kickoff step ("exit 0 == yes"). An agent
  with only `CLAUDE.md` skips it and may use retired award names.
- Step 5 §5 says *"Two awards per strategy."* There are 14 strategies. 28 award pairings is not a
  useful artifact. I produced pairings for the top-5 plus a team-level row. **State a scope: "for
  each strategy in the top tier."**
- Step 5's ordering puts the review last, after phase 2. Sections 1, 6, 7 and 8 depend only on the
  manual and could be drafted **while phase 2 runs**. On kickoff day that parallelism is free.

---

## 3. Schema fields that were unclear or under-specified

### 3.1 `game_def.json`

| Field | Problem |
|---|---|
| `teleop_s` | **Inclusive or exclusive of `endgame_s`?** No comment says. REBUILT's TELEOP is 140 s *including* the 30 s END GAME. `cycle-model.py:85` does `cycling_s = teleop_s − fixed["time_s"]` — it subtracts the *chosen action's* duration, not `endgame_s`, so `endgame_s` is **decorative**: it is printed in the header and never used in arithmetic. Guessing wrong here changes every number in §2 of the review. |
| `endgame_s` | Read by nothing except the banner. Either wire it up or mark it informational. |
| `cycle_actions` | **Only `cycle_actions[0]` is ever used** (`cycle-model.py:76,110`). Additional entries are silently ignored. A game with two repeatable scoring actions of different value — most FRC games — cannot be modelled, and the schema gives no hint. |
| `per_cycle` | *"how many units one robot trip delivers"* — this is a **robot design assumption**, not a manual fact, but it sits in the file labelled "fill from the manual." I set 8 as `[INFERENCE]`. It is the single largest lever on every output and it is unsourced. |
| `fixed_actions[].time_s` | *"seconds it consumes"* — **no FRC manual states a time cost for any action.** Every value here is invented, and the break-even table in §2.3 of the review is entirely a function of these invented numbers. This field needs its own sourcing convention (measured from last season's match video? estimated?). |
| `points_auto` / `points_teleop` | Assume one value per phase. REBUILT's TOWER L1 pays 15 in AUTO and 10 in TELEOP for the *same act*, and L2/L3 are TELEOP-only. I had to split TOWER across four `fixed_actions` rows and encode the AUTO/TELEOP asymmetry in names and a `_note`. The schema has no way to say "this action is legal only in this phase." |
| `rp[].metric` | Matched by the **substring `"TOWER"`** (`cycle-model.py:158`) to decide whether an RP is climb-based. Undocumented magic string. Name your metric anything else and TRAVERSAL gets modelled as a FUEL count. |
| `rp[].threshold` | Single scalar, but REBUILT thresholds are **per event tier** (100/240/360). I encoded the district value and put the escalation in `note`, which nothing parses. The 3.6× escalation is strategically decisive and is invisible to the model. |
| **missing** | **No way to express a scoring duty cycle, a conditional multiplier, or a phase in which points are worth zero.** REBUILT's defining mechanic — HUB active/inactive, Table 6-3 — is unrepresentable. I flagged it in two `_schema_gap` keys and corrected by hand. **This will bite on BIOCORE**, which the community intel predicts has ≥3 scoring locations of differing value (P5). |

### 3.2 `candidates.yaml`

| Field | Problem |
|---|---|
| `gates_input.mfg_floor` | See Finding 2.1. **The single worst-specified field in the project.** |
| `gates_input.new_workstreams` | *On top of the three mandatory streams*, per rubric A2 — but the stub does not say so and the field name implies "total". The BOM gate reports "**4 effective** (drivetrain, endgame, scoring, software)" using a *different* counting convention than A2's. Two counters, two conventions, same word. |
| `gates_input.novel_mechanisms` | Hand-entered here, but `bom-builder.py` **derives** its own count from the mechanism list and they disagreed: my BOM said "1 novel" in prose while the builder counted 3. Nothing reconciles them. |
| `gates_input.drive_practice_sensitivity` | Free string. `low`/`med`/`high` were accepted; nothing documents the legal set, and A4's anchors are a 0–5 scale, not a three-way enum. |
| `cycle_model.game` | *"FILL_ME_path_to_game_def.json"* — **relative to what?** The run dir, the repo root, or the YAML file? `game_def.json` worked; nothing said it would. |
| `cycle_model.median_alliance_score` | No source, no default, no guidance. It feeds V1 (imported, not hand-set) and therefore moves every value score. I used 120 as a pure guess. **There is a repo full of TBA CSVs 2022–2026 that could supply this and the stub does not mention them.** |
| `cycle_model.cycle` | For non-scoring candidates (defense, feeder, endgame-only) there is no cycle. I used the sentinel `99`. The stub gives no convention and no way to say "not applicable." |
| `V1` | Comment says *"imported from cycle-model.py — do not set it."* Nothing validates that you did not set it. |

### 3.3 `bom_config.yaml`

Cleanest of the three. Two gaps: the mechanism id list is only discoverable by running
`bom-builder.py --list` (not in the stub), and **there is no way to declare a mechanism as
"absorbed"** — the builder decided on its own that `passive_latch_climber` (0 motors, ≤12 build h)
did not count as a workstream, which is what flipped the gate verdict. That rule is invisible until
you read the output, and it means the difference between `FAILS 3 GATES` and `ALL GATES PASS` is a
heuristic the author of the config cannot see.

---

## 4. Things requiring knowledge NOT available from CLAUDE.md + briefing pack + manual

Ranked by how badly the analysis degrades without them.

1. **The `mfg_floor` token vocabulary.** Not in `CLAUDE.md`, not in the stub, not in the briefing
   pack, not in the manual, and not in the rubric markdown. Only in `reference/achievability_rubric.yaml`
   line 57 — a file no step tells you to open. **This is the finding.**
2. **That the HUB duty cycle exists and that the cycle model ignores it.** The manual has it
   (Table 6-3) but the briefing pack does not surface it — its "Scoring mentions" grep caught line
   1014 mentioning inactive HUBs but nothing flagged it as a *model-breaking* mechanic. Catching it
   required reading §6.4.1 in full and then reasoning about what `cycle-model.py` does not do.
3. **`per_cycle` and every `fixed_actions.time_s`.** Robot-design assumptions with no manual source.
   They drive the entire break-even and sensitivity analysis.
4. **`median_alliance_score`.** Needs TBA data. The repo has it; no instruction points there.
5. **That `cycle_actions[1..n]` are ignored.** Only discoverable by reading `cycle-model.py`.
6. **The `"TOWER"` substring magic in `rp[].metric`.** Same.
7. **The workstream-absorption heuristic in `bom-builder.py`.** Same.
8. **How to write YAML/JSON safely on this platform.** The Bash-heredoc failure (1.4) is a Windows +
   Git Bash + apostrophe interaction. `CLAUDE.md` says *"Windows 11 + Git Bash. Prefix python with
   `PYTHONIOENCODING=utf-8`"* — the right instinct, wrong hazard. **Add: write schema files with the
   file-write tool, never with a shell heredoc.**
9. **`STRATEGY-RANKING-SYSTEM.md` §2 in full.** `CLAUDE.md` §Step 3 cites it, so this is fair — but
   §2 is 120 lines of generators and its §2.7 checklist is the only thing that produces the
   defense / feeder / minimal rows. **Without reading it you get six variations of "pick up the
   thing and put it in the high place," which is exactly the failure the file warns about.**
10. **The awards deadline dates** (Impact 2027-02-11, Leadership 2027-02-04). In
    `00_AWARD_LIST_VERIFIED.md`, reachable from Step 5 §5.

---

## 5. What dominates kickoff-day wall-clock time

Measured and estimated:

| Step | Wall clock | Notes |
|---|---:|---|
| 1 — `RUN-KICKOFF.sh` phase 1 | **~30 s** | measured |
| 2 — Read briefing pack (458 lines) + manual §§4–7 | **20–35 min** | The manual is 166 pages. Reading "sections on game overview, scoring, and the game rules (G)" is pp. 15–75 — **60 pages.** |
| **3 — Fill the three schemas** | **60–120 min** | **DOMINATES.** |
| 4 — `RUN-KICKOFF.sh --phase2` | **~10 s** | measured |
| 5 — Write `REVIEW.md` (nine sections) | **45–75 min** | |

**Step 3 is the bottleneck, and inside Step 3 it is `candidates.yaml`.** Reasons:

- **14 candidates × 17 hand-scored factors = 238 individual judgements**, each nominally requiring a
  look at a rubric anchor table. `ACHIEVABILITY-RUBRIC.md` §2 is ~250 lines. It also specifies
  *"two people score independently, then reconcile"* — **that procedure is impossible for a single
  autonomous agent and `CLAUDE.md` does not acknowledge it.** Every score in this rehearsal is
  single-scored, which the rubric explicitly says is not how it works.
- Enumeration (31 raw → 14) requires reading `STRATEGY-RANKING-SYSTEM.md` §2's six generators plus
  the §2.7 checklist.
- The `mfg_floor` debugging cost a full extra phase-2 cycle. On a day with a real deadline, that is
  the difference between finishing and not.

**Total realistic: 2.5–4 hours** of which **~70% is Step 3**. `CLAUDE.md` implies a mechanical
sequence; it is actually one short mechanical step, one long judgement step, and one long writing
step.

**Highest-leverage speedups:**
1. Pre-write the ~10 game-agnostic candidate rows (pure defense, feeder, AUTO-only, minimal-flawless,
   do-everything, one endgame row per tier). Their achievability scores barely move between games —
   they depend on the *team*, not the manual. Ship them as `reference/examples/candidates_seed.yaml`
   and let kickoff day edit rather than author. **Saves 45–60 minutes.**
2. Have phase 1 pre-populate `game_def.json` from the manual's scoring-table extraction. The
   briefing pack already greps the scoring lines; parsing Table 6-4 into the schema is a small step
   further and removes the highest-risk transcription in the day.
3. Draft `REVIEW.md` §§1, 6, 7, 8 during Step 2 — they need only the manual.

---

## 6. Blunt verdict

**The pipeline works. The judgement layer around it does not yet defend itself.**

What went right, and should not be understated: five steps, two scripts, zero crashes, forty seconds
of compute, and a complete nine-section review at the end. The `FILL_ME` preflight fired exactly as
documented. The gate model correctly refused a six-mechanism BOM and correctly passed the descoped
five-mechanism one, and the descoping decision it forced — *you may have a scoring mechanism or an
active climber, not both* — is a genuinely good answer that a room of fifteen students would not have
reached on their own. `RULE-CHURN-WATCHLIST.md` predicted 5 of the 12 game-specific rules as
contentious and hit **5 for 5**; `QA-AMBIGUITY-HOTSPOTS.md` hit **4 for 4** on the never-stable
slots. The priors in this repo are good.

What went wrong is worse than a crash. **A crash is a message. This pipeline's failure mode is a
plausible, well-formatted, confidently wrong ranking table with no error attached.** Three of the
four highest-achievability strategies were deleted by an undocumented string vocabulary, and the
only reason they were recovered is that the result looked odd enough — *"pure defense needs a
machine we don't own"* — to be worth chasing into `score-strategy.py`. An agent under time pressure,
or a slightly less suspicious one, ships that table. On 2027-01-09 that table becomes the season.

**Three fixes before January, in priority order:**

1. **Hard-fail on an unknown `mfg_floor`** and add the alias map (Finding 2.1). One afternoon.
   Without this, the answer is unreliable in a way that is invisible.
2. **Rehearse against 2025 REEFSCAPE.** It exercises the rule/glossary diff — the step
   `STRATEGY-RANKING-SYSTEM.md` calls the highest-value sixty seconds of the day and the step this
   rehearsal could not test at all (Finding 2.2). Five minutes to run.
3. **Give `game_def.json` a way to express conditional scoring** — a duty cycle, a phase multiplier,
   a value-by-location gradient (Finding 3.1). REBUILT needed it. The community intel's P5 predicts
   BIOCORE will need it too, at 72% confidence. Right now the model would silently produce numbers
   about 50% too high and nothing in the pipeline would notice.

Also, quickly: delete `manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf` (Finding 2.3) — a 2026
manual is currently sitting in the 2027 folder under a 2027 name, and it satisfies `CLAUDE.md`'s own
autorun trigger.

**With those four done: yes, this runs unattended on 2027-01-09 and produces something a team can
act on by mid-afternoon. Without fix 1, it produces something that looks like that and isn't.**
