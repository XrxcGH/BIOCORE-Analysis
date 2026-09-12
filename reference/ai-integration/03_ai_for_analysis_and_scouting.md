# AI for Analysis and Scouting — BIOCORE (FRC 2027)

**Purpose:** turn a 150-page game manual and a public match database into decisions, using AI for the
desk work and students for the judgment. This file covers the *data* half of the AI plan: reading the
manual at machine speed, pulling the right numbers from the right API, running the smallest scouting
operation that still wins picks, simulating matches, and knowing exactly where the machine stops
being trustworthy.

**Companion files — read these first, this file extends and does not repeat them:**

| File | What it already settles |
|---|---|
| `reference/SCOUTING-PLAN.md` | FMS publishes Avg Match / Avg Auto / Avg &lt;endgame&gt; / Record / DQ **for free**. Scout only the 22 gap fields. Ships `tools/scouting-plan.py` (`free` · `schema` · `picklist`). |
| `KICKOFF_PLAYBOOK.md` | The kickoff-day clock, Phases 0–6, and prompts P1–P10. The *strategy* pipeline. |
| `STRATEGY-RANKING-SYSTEM.md` | Manual in → ranked strategy + BOM + award plan out. Stages 1–12, checkpoints C1–C7. |
| `reference/02_TEAM_CAPACITY_MODEL.md` + `team_capacity.yaml` | **The hours authority.** 599 effective build hours; 25.0 h strategy/rules; 54.9 h drive practice; zero slack. §4.4: **3–5 scouts available**, not 6. |
| `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` | FIRST **permits** AI, as a tool "in the same way that CAD programs, Programming Languages, and 3D printers are". One binding obligation: **attribution**. |
| `reference/team-ops/03_programming_stack.md` | Systemcore / WPILib 2027. The robot-code half of the AI plan. |
| `reference/ai-integration/templates/analysis-prompts.md` | Every prompt referenced here, with its verifier. |

**Siblings in `reference/ai-integration/`** (verified present 2026-08-22): `01_ai_for_programming.md` ·
`02_ai_for_design_and_cad.md` · `04_ai_for_docs_and_business.md` · `05_ai_infrastructure_and_policy.md`.
This file owns **manual analysis, APIs, scouting, simulation and alliance selection** and defers to those
for robot code, CAD, award writing, and account/tooling policy.

**New tools written by this pass:** `tools/match-sim.py` (Monte Carlo, calibrated) and
`tools/cite-check.py` (citation verifier). Both pure-stdlib, both run offline against data already
in this repo.

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Executed or fetched live during this pass (2026-08-22) and reproducible here |
| **[H]** HISTORICAL-PATTERN | Holds across 2023–2026 seasons; not a FIRST commitment for BIOCORE |
| **[S]** SPECULATION | Inference or forecast. Flagged inline |
| **UNVERIFIED** | Stated but not checked by this pass. Treat as a to-do, not a fact |

---

## §0 — 60-second workflow (runnable today, no API key, no network)

```bash
# Run from the repository root.

# ---- 1. WHAT YOU GET FOR FREE. Do not scout any column this prints. (~1 s)
python tools/scouting-plan.py free
python tools/scouting-plan.py schema --json > scouting_schema.json

# ---- 2. CALIBRATE THE MATCH SIMULATOR against real 2026 results. (~20 s)
#         Read the fitted SIGMA SCALE off this output. The raw model is wrong without it.
python tools/match-sim.py calibrate 2026

# ---- 3. PROVE IT PREDICTS. Brier score vs the always-0.5 baseline. (~15 s)
python tools/match-sim.py backtest 2026 --event 2026mndu --n 400 --sigma-scale 0.592

# ---- 4. SIMULATE A MATCH. Probabilities, not point estimates. (~3 s)
python tools/match-sim.py sim 2026 --event 2026mndu \
    --red 3100,2823,11223 --blue 5348,2503,7797 --n 20000 --sigma-scale 0.592

# ---- 5. THE PICK QUESTION: which candidate actually moves P(win)? (~20 s)
python tools/match-sim.py marginal 2026 --event 2026mndu --us 3267 --partner 2823 \
    --candidates 2847,7797,3297,4009,3130,2861 --n 2000 --opponents 40 --sigma-scale 0.592

# ---- 6. THE ANTI-HALLUCINATION GATE. Run on EVERY AI answer about the rules. (~2 s)
#         exit 1 == a cited rule does not exist, or a "quote" is not in the rule. Do not ship it.
python tools/cite-check.py 2026 some-ai-answer.md --baseline 2025

# ---- 7. ON KICKOFF DAY, in this order:
bash tools/probe-2027-manual.sh                       # find the PDF
bash tools/ingest-manual.sh <manual.pdf> V1           # freeze + extract + diff the evergreen spine
python tools/rule-inventory.py --years 2027           # build the chunk store cite-check.py reads
```

**The three lines you read out loud:**
1. `calibrate` → the **fitted sigma scale**. Every later command needs it.
2. `backtest` → the **Brier score vs 0.500**. If it is not clearly better, do not use the model.
3. `cite-check` → **VERDICT**. Anything other than ALL CITATIONS VERIFIED does not go on a whiteboard.

---

## §1 — Manual analysis automation

`KICKOFF_PLAYBOOK.md` defines *what* to extract from the manual and in what order (Phases 0–6).
This section defines *how to make a machine do it reliably*, which is a different problem with
exactly one failure mode that matters: the model inventing a rule.

### 1.1 Fixed-window chunking is the wrong tool for this corpus [C]

The default RAG recipe — split into 800-token windows with 100-token overlap, embed, retrieve top-k
— is built for prose with no internal addressing. The FRC Game Manual is the opposite kind of
document:

| Property of the manual | Consequence |
|---|---|
| Every normative statement carries a **unique ID** (`G410`, `R802`, `H301`) | The document ships its own primary key. Chunk on it. |
| Rule bodies are **self-contained**; cross-references are explicit ("see R502") | A rule is already the right retrieval unit. Windows split them mid-sentence. |
| Defined terms are **ALL CAPS**, always | A free, exact entity index. No embedding needed to find every mention of a defined term. |
| Evergreen vs game-specific is encoded in **headline colour**, not in any word (manual §1.6) | Text-only extraction silently destroys this. `tools/frc_spans.py` reads font and colour and keeps it. |
| It is **~150 pages**, not 150,000 | The whole corpus fits in a long-context window. Retrieval is an optimisation, not a necessity. |

**The rule:** chunk on rule boundaries. `tools/rule-inventory.py` already does this, emitting
`research/rule_inventories/<year>_rules_full.txt` and `<year>_bodies_v2.jsonl` — one record per rule,
with page number, headline and full body. That is the chunk store. Do not build a second one. Neither
file is in the repository, because both reproduce FIRST's rule text; `bash tools/rebuild-corpus.sh`
rebuilds them locally from the downloaded manuals.

> **The one place windows still win:** the non-numbered prose — game overview, scoring tables, field
> drawings, the glossary. `tools/ingest-manual.sh` keeps a `pdftotext -layout` pass **for tables only**
> and a raw pass for phrase greps, precisely because rule-aware extraction is wrong for those.

### 1.2 Three indexes, none of them embeddings [C]

For a 150-page corpus with a primary key, exact lookup beats semantic search on every axis that
matters — cost, latency, reproducibility, and the ability to prove an answer wrong.

| Index | Built by | Answers | Cost |
|---|---|---|---|
| **Rule ID → body** | `rule-inventory.py` → `<year>_rules_full.txt` | "What does G410 say?" — the majority of real questions | Free, instant, exact |
| **Defined term → mentions** | ALL-CAPS regex + `tools/caps_stoplist_frc.txt` | "Everywhere the manual constrains a SCORING ELEMENT" | Free, exact |
| **Phrase → page** | `pdftotext` raw pass, plain `grep` | "Where does it say anything about height?" | Free, exact |

Add embeddings only when you have a question none of the three can express. In four seasons of this
project's corpus, that has not come up. **Spending the strategy budget (25.0 h — `CAP` §3.1) on a
vector database is spending the scarcest resource on the least binding constraint.**

### 1.3 The multi-pass review structure

One prompt does not read a manual. Five passes do, and each pass has a different failure mode, which
is the whole reason to separate them.

| Pass | Question | Prompt | Verifier | Failure if skipped |
|---|---|---|---|---|
| **P-EXTRACT** | What does it literally say? | `analysis-prompts.md` A1 | `cite-check.py` | Everything downstream inherits a misquote |
| **P-STRUCTURE** | What are the entities and their limits? | A4 + `KICKOFF_PLAYBOOK.md` §0.2 | grep each definition | Undefined terms become silent assumptions |
| **P-ADVERSARIAL** | Where do two rules collide? | A2 | `cite-check.py` + `QA-AMBIGUITY-HOTSPOTS.md` | You file no Q&A and lose the 48-hour window |
| **P-CONSISTENCY** | Does our own analysis contradict itself? | F1 | re-run P-EXTRACT on disputed IDs | A brief that is confidently wrong in two places |
| **P-REGRESSION** | What did this Team Update break? | A3 | `teamupdate-diff.py` + `cite-check.py --baseline` | You build to a rule that changed in week 2 |

**Ordering is load-bearing.** P-ADVERSARIAL run before P-EXTRACT produces imaginative nonsense,
because the model has nothing anchoring it. Run in order, and each pass gets the previous pass's
*verified* output as its only source.

**Pass budget [S]:** a full P-EXTRACT + P-STRUCTURE + P-ADVERSARIAL sweep of a ~150-page manual is on
the order of a few hundred thousand input tokens once you count re-reads and per-section scoping.
That is minutes of wall-clock and a small, real, non-zero bill. Check your provider's current pricing
before you promise the team unlimited passes; the number of passes, not the number of pages, is what
drives it. P-REGRESSION is far cheaper — it reads a diff, not a manual.

### 1.4 The citation-check loop — the highest-value 30 lines in this file [C]

A model asked "which rule governs X" will sometimes return an ID that is plausible, correctly
formatted, numerically adjacent to real rules, and **does not exist**. It does this most often on
edge cases and rule interactions — which is exactly the output of P-ADVERSARIAL, the pass you most
want to trust. Reading the answer will not catch it. A regex will.

`tools/cite-check.py` (written by this pass) checks three things against the extracted manual:

1. **EXISTS** — every `[A-Z]###` token in the document is a real rule ID that season.
2. **QUOTED** — any double-quoted span immediately following a rule ID actually appears in that
   rule's extracted body (whitespace- and smart-quote-normalised).
3. **DRIFT** — with `--baseline`, whether a cited rule existed last season and whether its text
   changed. This catches the specific, common failure of a model answering from the **previous**
   manual.

Executed against a deliberately poisoned test document [C]:

```
CITE-CHECK  doc=citetest.md  season=2026  rule IDs cited=4
  VERIFIED (2): G410 R802
  !! DOES NOT EXIST IN 2026 (2): G999 H301
  !! QUOTE NOT FOUND IN RULE BODY (1):
     G410 <- 'this exact string is not in the rule'
  ~~ TEXT CHANGED vs 2025 (2): G410 R802
     Re-read these before relying on any 2025-era reasoning about them.
  VERDICT: 3 CITATION FAILURE(S)
```

Exit code 1. Wire it into the habit, not the hope:

```bash
python tools/cite-check.py 2027 strategies/BRIEF.md --baseline 2026 || echo "DO NOT SHIP"
```

> **Why this matters more than a better prompt.** You cannot prompt hallucination to zero, and you
> cannot detect it by reading — a fake rule ID reads exactly like a real one. You can make it
> *impossible to ship silently*. That converts an unbounded risk into a caught error, for one command.

### 1.5 What this does not replace

- **Reading the manual.** Every student on strategy reads it. The machine makes the second and third
  readings cheap; it does not make the first one unnecessary.
- **The comprehension self-test** (`KICKOFF_PLAYBOOK.md` §1.10). Answer it without looking, humans only.
- **Judgment about what is worth asking.** The model generates Q&A candidates; a human decides which
  of them are worth spending the team's credibility on.

---

## §2 — The API layer, exactly right

Three data sources matter. They are not interchangeable, and the most common mistake is using the
wrong one for the question.

### 2.1 The Blue Alliance API v3 [C — swagger fetched live 2026-08-22]

| Item | Value |
|---|---|
| Base URL | `https://www.thebluealliance.com/api/v3` |
| Auth | HTTP header **`X-TBA-Auth-Key: <your key>`** on every request |
| Where the key comes from | **You mint it yourself**, signed in to your own TBA account. This project has no key and never will — see §2.2. Never commit it; read it from an environment variable. |
| Machine-readable spec | `https://www.thebluealliance.com/swagger/api_v3.json` — **verified 200** |
| Human docs | `https://www.thebluealliance.com/apidocs/v3` — **verified 200** |
| Unauthenticated `/status` | returns **200** — useful only for reachability, not for data |
| Write/"trusted" API (event organisers) | `https://www.thebluealliance.com/apidocs/trusted/v1` — verified 200. **Not what you want.** |

Endpoints that earn their place, all verified present in the live swagger:

| Endpoint | Gives you | Use it for |
|---|---|---|
| `/event/{event_key}/teams` | Full team objects at an event | Building the pit-scouting list before you travel |
| `/event/{event_key}/matches` | Every match, schedule + full score breakdown | Everything. This is the workhorse. |
| `/event/{event_key}/matches/simple` | Same, minus the breakdown | Fast schedule pulls on venue wifi |
| `/event/{event_key}/rankings` | The FMS ranking table — the free columns in `SCOUTING-PLAN.md` §1 | The 22-field gap argument, live |
| `/event/{event_key}/oprs` | OPR, DPR, CCWM | Baseline point estimate per team |
| `/event/{event_key}/coprs` | **Component** OPRs, per score-breakdown column | Auto vs teleop vs endgame contribution — the input `match-sim.py` uses |
| `/event/{event_key}/alliances` | Playoff alliance composition | Post-hoc: who actually got picked, and from what rank |
| `/event/{event_key}/awards` | Award winners | `AWARD-ALIGNMENT.md` evidence base |
| `/event/{event_key}/insights` | Event-wide aggregates | Sanity-checking your own scouting against reality |
| `/event/{event_key}/predictions` | TBA's own match predictions | A free second opinion to check `match-sim.py` against |
| `/event/{event_key}/teams/statuses` | Per-team rank + playoff status | Live during quals |
| `/team/{team_key}/events/{year}` | A team's season | Pre-event scouting on a known opponent |
| `/team/{team_key}/event/{event_key}/matches` | One team's matches at one event | Pre-match briefs (§5) |
| `/match/{match_key}/zebra_motionworks` | **Robot XY position, ~10 Hz, whole match** | The only real positional data in FRC. Coverage is partial — see §4.3. |
| `/events/{year}` | Every event that season | Bulk collection |

Two operational notes that save real pain:

- **Conditional requests.** TBA supports `Last-Modified` / `If-Modified-Since`; a `304` costs you
  nothing. Cache aggressively — you will re-pull the same event dozens of times across a weekend.
  `UNVERIFIED` in this pass's testing (no key available); confirm against the live docs before relying on it.
- **Venue wifi is hostile.** Pull the full event before you leave the hotel, cache to disk, and make
  every downstream tool read the cache. A tool that needs the network in the pits is a tool that
  fails in the pits.

### 2.2 The no-key path already in this repo [C]

This project reads TBA **without an API key**, by parsing the public event page, which embeds the
rankings table, the alliances table, the playoff bracket, the `coprs` JSON blob and the qualification
match table in one document. Three working scrapers exist:

| Tool | Writes | Contains |
|---|---|---|
| `tools/tba_predictive_scrape.py` | `tba_rankings_<y>.csv`, `tba_alliances_<y>.csv`, `tba_events_<y>.csv` | Rank, RS, season sort columns, record, DQ, played; alliance slots |
| `tools/tba_copr_scrape.py` | `tba_copr_<y>.csv`, `tba_resid_<y>.csv`, `tba_matches_<y>.csv` | Component OPR per team; per-team score **residuals**; every qual match with both scores |
| `tools/tba_award_scrape.py` | `research/awards_tba/` | Award winners with their qualification rank |

2023–2026 data is already scraped and sitting in `research/predictive_tba/`. **`tools/match-sim.py`
reads exactly these files and needs no network at all.**

**Extend, do not rewrite.** When you get a key, the honest upgrade is a thin fetch layer that writes
the *same CSV schema* these scrapers already emit, so every downstream tool keeps working unchanged.
Refresh for BIOCORE with:

```bash
python tools/tba_copr_scrape.py 2027 --out research/predictive_tba/
python tools/tba_predictive_scrape.py 2027 --out research/predictive_tba/
```

### 2.3 Statbotics — what EPA actually measures [C — model doc fetched live 2026-08-22]

| Item | Value |
|---|---|
| REST base | `https://api.statbotics.io/v3` — root **verified 200** (`{"name":"Year V3 Router"}`) |
| Auth | **None.** No key, no header |
| Spec | `https://api.statbotics.io/openapi.json` — **verified 200** |
| v3 paths (verbatim from that spec) | `/v3/`, `/v3/year/{year}`, `/v3/years`, `/v3/team/{team}`, `/v3/teams`, `/v3/team_year/{team}/{year}`, `/v3/team_years`, `/v3/event/{event}`, `/v3/events`, `/v3/team_event/{team}/{event}`, `/v3/team_events`, `/v3/match/{match}`, `/v3/matches` |
| Python client | `pip install statbotics` (source: `github.com/avgupta456/statbotics`, verified 200) |
| **Status on 2026-08-22** | **Data endpoints returned HTTP 500.** `/v3/team_year/254/2026` → 500. The OpenAPI spec serves fine; the data does not. This has been the case since at least 2026-08-21 (see the header comment in `tools/tba_copr_scrape.py`). **Plan for Statbotics to be unavailable.** |

**What EPA is, precisely** — from Statbotics' own model documentation:

- EPA "builds upon the Elo rating system, but transforms ratings to point units". It is a rating in
  **points**, interpretable much like OPR, not an arbitrary scale.
- Teams **start** at one third of the average Week 1 score.
- Update rule: `ΔEPA = K × (actual score margin − predicted score margin)`, with **K = 0.5** early
  (≤6 matches) declining to **0.3** after 12+ matches, and a margin parameter **M** rising from 0 to 1
  across the season.
- **Components.** Auto EPA is fitted independently: `K × (auto score − auto EPA)`. Endgame EPA
  likewise, with margin parameter 0. **Teleop EPA is then derived as `EPA − auto EPA − endgame EPA`.**
- **Ranking points** use a separate model — the Iterative Logistic Strength (ILS) model by Caleb Sykes
  — not EPA itself.
- **Unitless EPA** = `1500 + 250 × (EPA − week-1 mean score / 3) / week-1 SD`, where **a 250-point
  gap corresponds to about a 75% chance of winning**. **Year-normalised EPA** maps end-of-season
  ratings onto a common distribution for cross-year comparison, and is **only available at end of season**.
- **Accuracy:** 72.04% match-prediction accuracy across 2016–2022, versus Elo 70.85% and OPR 70.13%.

**Three caveats that change how you should use it:**

1. **Teleop EPA is a residual, not a measurement.** It is whatever is left after auto and endgame.
   Every error elsewhere in the model lands in the teleop column. Do not present it to students as
   "how good they are at teleop".
2. **~72% accuracy is the ceiling of the whole genre, not a Statbotics weakness.** Roughly one match
   in four goes the other way. Any plan that requires being right more often than that is not a plan.
3. **K is high early.** At the start of an event, EPA is dominated by very few matches. This is the
   same small-sample problem as §6.5 and `analysis-prompts.md` F2.

### 2.4 FIRST FRC Events API [C — probed live 2026-08-22]

| Item | Value |
|---|---|
| Base URL | `https://frc-api.firstinspires.org/v3.0/` — **verified**, returns **401** unauthenticated |
| Auth | HTTP **Basic**: your FIRST username + an API token, base64-encoded in the `Authorization` header. **You register for it yourself.** |
| Registration / docs | `https://frc-events.firstinspires.org/services/API` — **verified 200** |
| Why bother | It is the **source of record**. TBA mirrors it. During an event, FIRST's data is authoritative and slightly ahead. |
| Why not to bother | For everything this team does, TBA is easier, better documented, and richer (Zebra, insights, predictions). |

**Recommendation [S]:** use TBA as the default, FRC Events as the tiebreaker when a number looks
wrong. Do not build two pipelines.

### 2.5 Which source answers which question

| Question | Source | Why not the others |
|---|---|---|
| "What did team X average at this event?" | TBA `/rankings` (free FMS column) | EPA is a model; the ranking table is the actual reported number |
| "How much of that is auto?" | TBA `/coprs` | Rankings give one auto column; coprs decomposes every breakdown field |
| "How good are they, adjusted for schedule?" | Statbotics EPA | OPR does not adjust for opponent strength; EPA does |
| "How consistent are they?" | `tba_resid_<y>.csv` → `match-sim.py` | **Neither TBA nor Statbotics publishes a per-team variance.** This is the gap the simulator fills |
| "Are they a good pick *for us*?" | `match-sim.py marginal` + gap scouting | No public source models complementarity |
| "Will they break?" | **Your scouts.** `breakdown`, `spare_parts_depth` | Not published anywhere, in any form |
| "Where were they on the field?" | TBA `/zebra_motionworks`, where available | Nothing else has positional data |

---

## §3 — Scouting apps, and where AI actually helps

### 3.1 Verified open-source options [C — GitHub API queried 2026-08-22]

| App | Repo | Stack | Licence | Last push | Sync model | Fit for ~15 students |
|---|---|---|---|---|---|---|
| **Scouting PASS** | `github.com/PWNAGERobotics/ScoutingPASS` | JavaScript | *none declared* | 2026-01-25 | Swipe-through form → **QR** → scanner → spreadsheet | **Best default.** Five swipeable pages (pre-match / auto / teleop / endgame / post). Loads once, then needs no connection. Ships a REBUILT (2026) config as a worked example. |
| **QRScout** | `github.com/FRC2713/QRScout` | TypeScript | **MIT** | 2026-07-05 | Form → **QR** → scan into Sheets/Excel | Most actively maintained of the set. Cleanest config format. Smallest thing that works. |
| **Black Hawks Scouting** | `github.com/FRC2834/blackhawks-scouting` | Vue | **MIT** | 2026-03-12 | Offline-capable web app; caches match data in local storage | Good if you want a real PWA rather than QR shuttling |
| **open-scouting** | `github.com/FRC-Team3484/open-scouting` | Svelte | **GPL-3.0** | 2026-08-20 | Server-backed | Most recent commits of the set; a server is a liability at an event with bad wifi |
| **Q-FRC Scouter** | `github.com/Q-FRC/Scouter` | QML | **GPL-3.0** | 2025-03-28 | QR, cross-platform native | Native app, configurable; **not updated in the 2026 season** |
| Team 3176 `scout` | `github.com/Team3176/scout` | Jupyter | *none declared* | 2023-04-17 | — | **Stale.** Listed only so nobody rediscovers it and wastes a week |

> **Licence warning:** two of these declare **no licence**. "Public on GitHub" is not permission to
> reuse. If you intend to fork and modify, prefer **QRScout (MIT)** or **Black Hawks (MIT)**, or open
> an issue and ask. This is also an `AWARD-ALIGNMENT.md` issue — judges notice attribution.

### 3.2 Why QR beats every network sync at an event [C on mechanism]

The QR pattern is: scout fills a form on a phone or tablet with **no connection at all** → the app
renders the record as a QR code → one laptop at the stands scans it with a webcam → a row lands in a
spreadsheet. It wins because it removes every failure mode that actually happens at events:

| Failure | Networked app | QR app |
|---|---|---|
| Venue wifi saturated / blocked | Dead | Unaffected |
| No cell signal in a metal shed | Dead | Unaffected |
| Server laptop sleeps | Dead | Unaffected |
| Scout device battery dies mid-match | Data lost | Data lost (same) |
| Data arrives corrupted | Silent | Scan fails visibly, rescan |

Its real cost is **one person scanning**, continuously. Budget that body — it is not free, and at
3–5 available scouts (`CAP` §4.4) it is a meaningful fraction of your capacity.

**Payload discipline:** QR capacity is finite. Encode enums as single characters and booleans as
`0`/`1`, and keep the field order fixed so the payload is positional rather than keyed. The 22-field
gap schema fits comfortably; a 60-field schema does not. This is another reason the schema is small.

### 3.3 How few scouts you can actually run — and a contradiction to resolve [C]

Two files in this project give different numbers, and the difference is real:

- `SCOUTING-PLAN.md` §4: "a **6-scout rotation** covers the match set".
- `02_TEAM_CAPACITY_MODEL.md` §4.4: of 12 realistic attendees, **5 are available** for scouting, and
  **3** during the Impact judging window. "Full manual scouting requires 6 — one per robot on the
  field. You have 3 to 5."

**Resolution:** a 6-person *rotation across a day* is not 6 people *simultaneously*. Design the
system for **3 concurrent scouts** and let it degrade gracefully upward, never downward:

| Concurrent scouts | Scheme | What you get | What you lose |
|---|---|---|---|
| **3** | One scout per robot, **your alliance colour only** (`CAP` §4.4 scheme 2) | Complete data on partners; complete data on ~half the field over a full event | Opponent-side detail in any single match |
| **4** | 3 alliance-colour + 1 free-roaming qualitative scout | Adds defence quality and breakdown-recovery notes — the highest-value unpublished fields | — |
| **5** | 2 robots per scout on one metric + binary breakdown (`CAP` scheme 1) | Broad, crude coverage of the whole field | Depth on any one robot |
| **0 extra** | **Join a scouting alliance** (`CAP` scheme 3) | Whole-field data for the cost of a conversation in the pits on Thursday | A data-sharing agreement, and a dependency on someone else's schema |

> **The single highest-return move on this list costs zero students:** a scouting alliance. Ask on
> Thursday. Bring your schema in a form other teams can actually merge — which is one more reason to
> use a common app rather than a bespoke one.

### 3.4 Where AI genuinely helps — four jobs, ranked by payoff

| # | Job | When | Payoff | Honest limit |
|---|---|---|---|---|
| **1** | **Generate the BIOCORE gap schema from the manual** (`analysis-prompts.md` B1) | Kickoff day, hours 3–5 | Highest. Compresses a task that historically eats a week into an afternoon, and the constraint prompt keeps it small | The model will over-produce fields unless the "FMS cannot publish this because ___" test is enforced literally. Enforce it. |
| **2** | **Data-quality anomaly detection** (C1) | After every ~12 matches | High. Catches stuck scouts, impossible values and untouched default fields before they poison the pick list | Flags only. **Never let it edit data.** A confidently "corrected" row is worse than a missing one |
| **3** | **Natural-language query** (C3) | Anytime | Moderate. Removes the spreadsheet bottleneck for students who cannot write formulas | Only if it **writes a query you run**, never if it reads the CSV and does arithmetic. Models miscount rows |
| **4** | **Auto-generated reports** (D2) | Thursday night, post-event | Moderate. Turns raw data into something readable at 11 p.m. when nobody wants to write | Prose is easy and cheap to generate, which makes it easy to over-trust. The "what we got wrong" section is the only part worth reading |

**What AI does *not* help with here:** the actual observing. There is no substitute for a student
watching a robot. Everything above is about what happens to the data *after* a human records it, or
about designing the form *before*.
---

## §4 — Match video analysis: what is actually realistic in 2026

### 4.1 The honest assessment

Every season someone proposes "AI that watches the match video and scouts it for us". Here is where
that stands, stated plainly because the user makes budget decisions from this file.

| Capability | Realistic in 2026? | Why |
|---|---|---|
| Read the FMS scoreboard overlay from a stream | **Yes** | Fixed position, fixed font, high contrast. This is ordinary OCR. But it only recovers data TBA already publishes for free. |
| Track which alliance a robot belongs to | **Mostly** | Bumper colour is a strong, deliberate signal |
| Identify a specific team number from broadcast video | **Unreliable** | Bumper numbers are small, motion-blurred, occluded, and often facing away. This is the step everything else depends on, and it is the step that fails |
| Count scoring actions per robot | **No, not reliably** | Requires the identification above *plus* game-specific event detection *plus* occlusion handling, on a new game each January |
| Measure cycle time from video | **Semi**, with human anchors | Achievable if a human marks cycle starts; not achievable end-to-end |
| Judge defence quality | **No** | This is a judgement about intent and effect. It is the single most valuable unpublished field (`SCOUTING-PLAN.md` §3) and it stays human |
| Robot position over time | **Yes — but not from video** | TBA's `/match/{key}/zebra_motionworks` gives real XY tracking where the event captured it. Better than anything computer vision would give you |

**The verdict [S]:** building a video-scouting pipeline is a **negative-value project for this team**.
It would consume the programming line (134.8 h, already the tightest role in 2027 — `CAP` §3.2) that
must instead go to Systemcore migration, to produce data that is partly free from FMS and partly
better obtained from three students with clipboards.

> **The 2027 amplifier:** every hour of programming this season is contested by the roboRIO →
> **Systemcore** transition. A speculative vision pipeline is exactly the kind of project that looks
> impressive in October and is abandoned in February. See `reference/team-ops/03_programming_stack.md`.

### 4.2 The workflow that *is* worth doing

Semi-automated, human-anchored, roughly 20 minutes per match reviewed — and you review perhaps six
matches a season, not sixty.

1. **Record with a fixed camera on your own robot.** One phone on a tripod, framing your robot's
   working area, running the whole match. Not the broadcast feed.
2. **Anchor by hand.** One student scrubs and records timestamps for a handful of events per match:
   cycle starts, intake failures, the moment something breaks. This is the human step and it is
   ~5 minutes per match. It is also the step that makes everything after it possible.
3. **Let the model structure it** (`analysis-prompts.md` E2). Feed it the timestamp log, get back a
   cycle table with durations, the mean, the slowest cycle, and **the single largest recoverable loss
   with the timestamp to review**.
4. **Go watch those 20 seconds.** That is the entire point: the pipeline exists to aim a human at the
   right fragment of video, not to replace watching it.
5. **Feed the result into `tools/cycle-model.py`.** One second of cycle time was worth **9.7
   points/match and 117 points across a 12-match schedule** at an 8-second cycle
   (`SCOUTING-PLAN.md` §4). That is where video review pays — on **your own** robot, not on scouting
   opponents.

**The reframe that makes this worth doing at all:** stop thinking of video as a scouting input.
It is a **driver-practice instrument**. `04_PREDICTIVE_FACTORS.md` weights drive practice at 90, the
highest in the corpus, and `CAP` §3.4 flags the drive-practice line (54.9 h) as the model's most
alarming output. Video review that shortens your own cycle is the cheapest way to buy back some of
that gap.

---

## §5 — Pre-match AI briefs

### 5.1 The constraint that defines the format

Between matches, a drive team has roughly **90 seconds** of usable attention while they are also
carrying a robot, swapping a battery and listening for a queue call. Anything longer than one index
card is not a brief; it is homework.

**`tools/prematch-brief.py`** (written by this pass) produces exactly that card. It computes the
numbers deterministically from local CSVs — no network, no model, no chance of a hallucinated
statistic — and leaves two slots explicitly marked for a human.

```bash
# every match your team is in, at one event
python tools/prematch-brief.py 2026 --event 2026mndu --us 3267 --sigma-scale 0.592

# one specific match, with your own gap-scouting merged in
python tools/prematch-brief.py 2026 --event 2026mndu --us 3267 --match 12 \
       --scouting scouting.csv --sigma-scale 0.592
```

Real output [C]:

```
====================================================================
MATCH #11           us 3267 on BLUE        P(win) = 0.08
====================================================================
ONE-LINE PLAN: ____________________________________  <- HUMAN WRITES THIS
PARTNER 3294   mu   15.1  sigma  25.0  | NO GAP-SCOUTING DATA -- public numbers only
PARTNER 11223  mu   50.0  sigma  22.6  | NO GAP-SCOUTING DATA -- public numbers only
THREAT  5348   mu   85.3  sigma  25.7  | NO GAP-SCOUTING DATA -- public numbers only
OUR RISK 3294  highest sigma on our alliance (25.0) -- the match swings on this robot
SCORE   us p10/p50/p90  102.7 / 132.3 / 163.0    them  147.9 / 188.8 / 228.4
IF IT GOES WRONG: _________________________________  <- HUMAN WRITES THIS
CONFIDENCE: model knows scoring rate and volatility only. It does NOT know
            reliability, defense or driver skill. Trust your scouts over this line.
```

### 5.2 Three design decisions worth copying

| Decision | Why |
|---|---|
| **The numbers are computed, not generated.** The LLM never touches `mu`, `sigma` or `P(win)` | A model asked to "write a brief from this data" will paraphrase a number wrong roughly as often as it paraphrases prose wrong, and you will not notice |
| **`ONE-LINE PLAN` and `IF IT GOES WRONG` are blank** | These are the two lines that require knowing what your robot did in the last match. A model cannot know that. A blank line is honest; a generated one is a guess in a confident voice |
| **The confidence line names what the model does not know** | Every brief ends by telling the drivers to trust their scouts over the number. Repeat it every match until it is boring |

**Where the LLM belongs:** polishing the wording *after* the numbers are fixed
(`analysis-prompts.md` D1), and only when someone has 60 spare seconds. The card works without it.

**Field note:** `NO GAP-SCOUTING DATA` printed on every partner line is not a bug — it is the tool
telling you your scouting has not reached this team yet. When those lines are still blank on Saturday
morning, your scouting plan failed, and you will know before the draft instead of during it.

---

## §6 — Monte Carlo match simulation

### 6.1 Why a distribution and not a point estimate

Summed OPR tells you an alliance is "11 points better". It does not tell you whether that is a
comfortable lead or a coin flip. The difference is variance, and variance is the thing no public
source publishes.

`tools/match-sim.py` models:

```
alliance_score = sum over 3 members ( mu_i + Normal(0, sigma_i x scale) ) + Normal(0, sigma_shared)
```

- **`mu_i`** — component OPR from `tba_copr_<year>.csv` (or Statbotics EPA; same units)
- **`sigma_i`** — that team's match-to-match volatility, from `tba_resid_<year>.csv`
- **`scale`** — a single global multiplier **fitted from real results**, not assumed

### 6.2 Calibration found a real bug in the data, not just a parameter [C]

```
CALIBRATION  year=2026  event=ALL  matches used=15176
  observed  margin-error SD    :    60.16 pts
  model     margin SD (raw)    :   104.47 pts   (sqrt of summed per-team resid_sd^2)
  mean |margin error|          :    44.88 pts
  fitted SIGMA SCALE           :    0.576       --> pass  --sigma-scale 0.576
```

**0.576 is not an arbitrary fudge factor — it is 1/√3 = 0.577.** The reason is a data-shape trap:
`resid_sd` in `tba_resid_*.csv` is an **alliance-level** residual (`actual_score − sum of the 3
members' OPR`) that is then written onto each of the three members. Summing six of them in quadrature
therefore over-disperses by exactly √3. The calibration recovered that constant from 15,176 real
matches without being told it. **Any model that consumed those residuals naively would have been
silently 73% too uncertain.**

Per-event calibration lands in the same place: `2026mndu`, 77 matches → **0.592**.

> **The transferable lesson:** always fit the noise term against outcomes you can check. A variance
> parameter that was reasoned about rather than fitted is a guess wearing a lab coat.

### 6.3 It predicts — and here is the proof [C]

```
BACKTEST  year=2026  event=2026mndu  decided=77  sims/match=400  sigma_scale=0.592
  point-estimate accuracy (higher COPR sum wins) : 0.8442
  Monte-Carlo  accuracy (p_red > 0.5)            : 0.8312
  Brier score  Monte Carlo                       : 0.1073   (lower is better)
  Brier score  always-0.5 baseline               : 0.2500
  CALIBRATION CURVE  (predicted -> observed red win rate)
    p~0.0   n=   11   observed 0.000   OK
    p~0.9   n=   10   observed 1.000   OK
    p~1.0   n=   14   observed 0.929   OK
```

Read this carefully, because the honest reading is the useful one:

- **Accuracy is not the win.** The Monte Carlo (0.8312) is very slightly *worse* than just comparing
  summed OPR (0.8442). Sign flips near p=0.5 cost it a match or two.
- **Calibration is the win.** Brier **0.1073** against a 0.2500 baseline, and the calibration curve
  lands within tolerance in every populated bin. When it says 90%, it means 90%.
- **The uncalibrated model is measurably worse:** the same backtest at `--sigma-scale 1.0` gives
  Brier **0.1192**. Fitting the scale bought ~10% of the Brier score for one command.
- **n is small.** 77 decided matches at one event; most bins hold 10–14 matches. Treat single-bin
  results as indicative, not proven, and re-run on more events before quoting a headline number.

### 6.4 A worked match [C]

```
MONTE CARLO  2026mndu   n=20000   sigma_scale=0.592
        teams                      sum mu       sd
  RED   3100,2823,11223             247.4     33.4
  BLUE  5348,2503,7797              236.4     25.6
  RED  score  p10/p50/p90 :   204.3   247.5   289.9
  BLUE score  p10/p50/p90 :   203.7   236.5   269.7
  margin  mean +10.8   SD 42.2
  P(RED win) = 0.600    P(BLUE win) = 0.400    P(tie) = 0.000
```

An 11-point edge is **a 60/40 match**, not a win. The margin SD (42.2) is four times the edge. That
one line is the whole argument for the tool: it stops the strategy table from treating an OPR
advantage as a result, and it tells the drive team truthfully how much room they have.

### 6.5 On BIOCORE, before any 2027 data exists

You cannot simulate BIOCORE on kickoff day — there are no matches. What you *can* do:

| When | What the simulator is for |
|---|---|
| Kickoff → Week 1 | Nothing. Do not pretend. Use `tools/cycle-model.py` for scoring arithmetic instead |
| After your Week 1 quals | `calibrate 2027 --event <yours>` on ~70 matches. Thin, but real |
| Week 2+ | Re-calibrate on all published 2027 events. This is when it becomes trustworthy |
| Alliance selection | `marginal` — §7 |

Encode the BIOCORE scoring rules with `analysis-prompts.md` E1, and **hand-check every point value
against the manual's scoring table.** A wrong point value corrupts every simulation downstream and
still produces plausible-looking output.

---

## §7 — Alliance selection: what AI assists, what stays human

### 7.1 The marginal-value question, answered on real data [C]

The pick-list question is not "who is best" — it is "**who most raises our probability of winning**".
Those differ, and the difference is computable:

```
MARGINAL PICK VALUE  2026mndu   us=3267 partner=2823   vs 40 random top-20 opponent alliances
  cand     mean P(win)        mu     sigma   endgame
  2847           0.669      80.0      43.1      0.00
  7797           0.623      71.6      20.1      0.00
  3297           0.615      72.3      41.9      0.00
  4009           0.593      67.9      20.5      0.00
  3130           0.555      63.6      30.7      0.00
  2861           0.551      63.1      31.4      0.00
  spread, best vs worst candidate: +0.118 win probability
```

Two findings from this run that a spreadsheet would not have surfaced:

1. **7797 (mu 71.6) outranks 3297 (mu 72.3).** Nearly identical scoring average; 7797's sigma is
   **20.1** against 3297's **41.9**. At equal mean, the consistent robot is the better partner —
   because you win by clearing a threshold repeatedly, not by having a good day once.
2. **The spread is +0.118.** Choosing well here is worth about **12 percentage points** of win
   probability. That is a real, quantified return on running the analysis.

### 7.2 The finding that matters most for a small team [C]

Run the same command for a **dominant** captain pairing (3100, mu 146.6, with 5348) and the entire
candidate spread collapses to **+0.004**.

> **The value of pick analytics is inversely proportional to how strong your top two already are.**
> If your alliance is already dominant, every third pick wins about equally often, and the model is
> telling you to **stop optimising the number and pick on the things it cannot see** — reliability,
> defence, driver skill, spare-parts depth. If your alliance is mid-table, the model is worth 12
> points of win probability and you should run it.

For a ~15-student team whose realistic path is being *picked* rather than picking
(`CAP` §4.4 scheme 2), this is doubly useful: it tells you when to stop spending scarce hours on
analysis you cannot cash in.

### 7.3 The division of labour

| Task | Who | Why |
|---|---|---|
| Aggregate free FMS columns into a starting order | **Machine** — `scouting-plan.py picklist` | Pure arithmetic, zero judgement |
| Compute marginal win probability per candidate | **Machine** — `match-sim.py marginal` | Requires 100k+ simulations. Humans cannot |
| Flag where public data and our scouting disagree | **Machine** — `analysis-prompts.md` C2 | Mechanical comparison; humans miss it under time pressure |
| Write two sentences per candidate | **Machine, then edited** — D3 | Drafting is cheap; the edit is where the value is |
| **Decide whether a robot will still be working on Saturday** | **Human** | `breakdown_cause` and `spare_parts_depth` are qualitative, sparse, and the highest-variance factor in playoffs |
| **Judge defence quality** | **Human** | Not in any public dataset, not inferable from score |
| **Judge driver skill** | **Human** | `SCOUTING-PLAN.md` §3: the best predictor of playoff performance, entirely unpublished |
| **Judge whether we can work with them** | **Human** | Alliance partnership is social. No model has this input |
| **Read the room during the draft** | **Human** | Picks come off the board in real time; the list is stale within 90 seconds |
| **Say the team number out loud** | **Human — a student** | It is their competition |

### 7.4 Three failure modes to name out loud before the draft

1. **Authority laundering.** A number printed by a script acquires more credibility than the same
   number guessed by a student, even when it rests on 8 matches. Print `n` next to every aggregate.
2. **Optimising the measurable.** The model ranks on `mu` and `sigma` because those are what it has.
   The most decisive factor — whether the robot survives Saturday — is in none of them.
3. **The list going stale.** By the third round, half your list is gone. Build the list so it can be
   re-sorted by "still available", and rehearse that in December, not in the stands.

**Rehearsal beats tooling.** Run a mock draft in the fall against 2026 data — `picklist`, then
`marginal`, then a student with a whiteboard reading names. The failure you find in November is free.

---

## §8 — What AI does badly here. Read this before budgeting.

| Failure | How it shows up | Mitigation | Residual risk |
|---|---|---|---|
| **Inventing rule IDs** | A plausible, well-formatted rule that does not exist — most often on the edge cases you most want | `tools/cite-check.py` on **every** rules answer | Low, once wired in. **High if you skip it** |
| **Answering from last season's manual** | Confident statements matching 2026 rules, not BIOCORE | `cite-check.py --baseline 2026` flags drift; always paste extracted text | Moderate in January, when 2027 text is thin in any model's training |
| **Arithmetic over pasted tables** | Wrong totals, miscounted rows, plausible-looking averages | Never let it compute. Make it **write a query you run** (C3) | Low if enforced; the enforcement is the hard part |
| **Confident prose from thin data** | A paragraph about a team built on 6 observations | Print `n` everywhere; run F2 | Moderate — this is the one that survives review |
| **Over-producing schema fields** | A 60-field scouting form nobody can fill in a live match | The "FMS cannot publish this because ___" test in B1; hard cap at 24 | Low |
| **Silent "correction" of data** | An anomaly pass that fixes rows instead of flagging them | Anomaly prompts are read-only by construction (C1) | Low |
| **Fabricated citations to sources** | Non-existent CD threads, papers, product URLs | Verify every URL before it lands in a file. This pass checked every URL below with an HTTP request | Moderate |
| **Video understanding** | Overpromising an end-to-end scouting pipeline | §4. Do not build it | Low if you simply do not start |
| **Displacing the learning** | Students who can operate the pipeline but cannot read a rule | `00_FIRST_AI_POLICY_VERIFIED.md`: "Permission to use a tool is not a reason to skip the thinking" | **The one that actually matters.** Not a technical risk |

**One more, specific to 2027:** models are weakest on the newest thing. Systemcore, WPILib 2027 and
the BIOCORE manual are all brand new in January. Expect model output about them to be **worse** than
about the roboRIO era, and expect it to be wrong in the same confident tone. See
`reference/team-ops/03_programming_stack.md`.

---

## §9 — Hours and money, reconciled against the capacity model

`02_TEAM_CAPACITY_MODEL.md` §3.3 is unambiguous: at 15 h/week into a Week 1 event **the plan closes
with exactly zero slack**. Nothing in this file adds hours. Everything here has to *displace*
something, and the displacement has to be named.

| Activity | Line it draws from (`CAP` §3.1) | Effect [S] |
|---|---|---|
| Manual ingest + multi-pass review, kickoff weekend | `strategy_rules` (25.0 h) | Neutral to positive. Replaces a slower manual read; the pass structure is the same work, faster |
| Schema generation on kickoff day | `strategy_rules` | Saves the multi-session "what should we scout" debate. This is where AI most clearly wins |
| Standing up a scouting app | `programming` (134.8 h) — **the tightest line in 2027** | **Use an off-the-shelf app (§3.1). Do not write one.** Every hour here is an hour not spent on Systemcore |
| Simulator + briefs | `strategy_rules` | Already written and tested. Marginal cost is running two commands |
| Video pipeline (§4) | `programming` | **Do not start.** Negative value against a Systemcore-constrained programming budget |
| Event-day scouting | Bodies, not build hours (`CAP` §4.4: 3–5 available) | Fewer fields → fewer scouts → the 3-concurrent scheme becomes viable |

**Where reclaimed hours should go:** drive practice. `CAP` §3.4 flags the 54.9 h drive-practice line
as the model's most alarming output, and `04_PREDICTIVE_FACTORS.md` weights drive practice at 90 —
the highest in the corpus. Hours saved on scouting admin have exactly one correct destination.

**Money [C on the free items]:**

| Item | Cost |
|---|---|
| The Blue Alliance API v3 | Free. Key from your own account |
| Statbotics | Free. No key |
| FIRST FRC Events API | Free. Registration required |
| All six scouting apps in §3.1 | Free, open source (**check the two with no declared licence**) |
| `match-sim.py`, `cite-check.py`, `prematch-brief.py`, all `tba_*.py` | Free, pure stdlib, offline |
| Scout devices | **Use phones the students already own.** Do not buy tablets |
| LLM usage | Non-zero and driven by **number of passes**, not pages. Check your provider's current pricing before promising unlimited passes; nothing in this file requires a large-volume plan |

**Nothing in this section touches the `robot_discretionary` line ($2,500).** That is the point: this
is the half of the season that gets better without spending the BOM.

---

## §10 — Validation / dry run

Everything below was executed on **2026-08-22** and can be re-run today.

```bash
# Run from the repository root.

# V1 · the free-data argument still holds and the schema still emits 22 fields
python tools/scouting-plan.py free
python tools/scouting-plan.py schema --json | python -c "import sys,json; d=json.load(sys.stdin); print(sum(len(v) for v in d.values()), 'fields')"

# V2 · the simulator calibrates, and the fitted scale is ~1/sqrt(3) = 0.577
python tools/match-sim.py calibrate 2026            # expect  fitted SIGMA SCALE ~0.576

# V3 · calibration beats no calibration, on Brier score
python tools/match-sim.py backtest 2026 --event 2026mndu --n 400 --sigma-scale 1.000   # ~0.119
python tools/match-sim.py backtest 2026 --event 2026mndu --n 400 --sigma-scale 0.592   # ~0.107

# V4 · a small OPR edge is a coin flip, and the tool says so
python tools/match-sim.py sim 2026 --event 2026mndu --red 3100,2823,11223 \
    --blue 5348,2503,7797 --n 20000 --sigma-scale 0.592                # expect P(RED) ~0.60

# V5 · the pick spread collapses for a dominant captain and opens for a mid-table one
python tools/match-sim.py marginal 2026 --event 2026mndu --us 3100 --partner 5348 \
    --candidates 2847,2503,3297,7797,4009,3267 --n 1500 --sigma-scale 0.592   # spread ~+0.004
python tools/match-sim.py marginal 2026 --event 2026mndu --us 3267 --partner 2823 \
    --candidates 2847,7797,3297,4009,3130,2861 --n 2000 --sigma-scale 0.592   # spread ~+0.118

# V6 · the citation gate catches a fake rule, a fake quote, and cross-season drift
printf 'Per G410 the ROBOT may not. See R802 and G999. H301 covers it.\n' > /tmp/ct.md
python tools/cite-check.py 2026 /tmp/ct.md --baseline 2025            # expect exit 1

# V7 · briefs generate offline from local CSVs only
python tools/prematch-brief.py 2026 --event 2026mndu --us 3267 --sigma-scale 0.592 | head -12

# V8 · the APIs are where this file says they are
curl -s -o /dev/null -w "%{http_code}\n" https://www.thebluealliance.com/swagger/api_v3.json  # 200
curl -s -o /dev/null -w "%{http_code}\n" https://api.statbotics.io/openapi.json               # 200
curl -s -o /dev/null -w "%{http_code}\n" https://frc-api.firstinspires.org/v3.0/              # 401 = alive, needs auth
```

**Expected failures, so they do not alarm anyone:**
- `api.statbotics.io/v3/team_year/...` returns **HTTP 500** as of 2026-08-22. Not your fault. §2.3.
- `match-sim.py` on year 2027 exits with `MISSING:` until `tba_copr_scrape.py 2027` has run.
- `cite-check.py 2027` exits with `MISSING:` until `rule-inventory.py --years 2027` has run.

---

## Files written by this pass

- `reference/ai-integration/03_ai_for_analysis_and_scouting.md` (this file)
- `reference/ai-integration/templates/analysis-prompts.md` — prompt library, every prompt with its verifier
- `tools/match-sim.py` — Monte Carlo match simulator: `calibrate` · `sim` · `backtest` · `marginal`
- `tools/cite-check.py` — rule-citation verifier: EXISTS · QUOTED · DRIFT; exit 1 on failure
- `tools/prematch-brief.py` — one index card per match from local CSVs, no network

## Known limitations

- **Everything BIOCORE-specific is [S] until 2027-01-09.** The free-data shape is **[H] from four
  seasons**, not a FIRST commitment (`SCOUTING-PLAN.md`). Re-verify at Week 1.
- **The simulator is calibrated on 2026 only.** The 0.576 scale is a property of how
  `tba_copr_scrape.py` computes residuals, not a law of FRC. **Re-run `calibrate` on 2027 data before
  trusting a single 2027 probability.**
- **The backtest is thin.** 77 decided matches at one event; most calibration bins hold 10–14 matches.
  Re-run across more events before quoting an accuracy figure to anyone.
- **The model contains no defence, reliability or driver-skill term.** By design — those are the
  22 gap fields, and they are the reason scouts exist. Never present `P(win)` as complete.
- **TBA conditional-request behaviour (`If-Modified-Since`) is UNVERIFIED** by this pass; no API key
  was available. Confirm against the live docs before building a caching layer on it.
- **Statbotics data endpoints were returning HTTP 500** throughout this pass. The endpoint list and
  the EPA model description come from its live OpenAPI spec and its published model documentation,
  both of which were reachable; the **response field names were not verifiable**. Treat any specific
  JSON key as UNVERIFIED until you get a 200.
- **Two of the six scouting apps declare no licence.** Verified via the GitHub API on 2026-08-22.
  Do not fork those without asking.
- **`prematch-brief.py` prints every match you are in** unless `--match` is given; `--all` is
  therefore redundant today. Harmless, but do not read it as filtering.
- **No LLM prices are quoted anywhere in this file**, deliberately. They change, and a stale price in
  a budget document is worse than no price. Token *volumes* are given instead.
- **This file cannot make anyone read the manual.** The tooling assumes at least one human who has.
