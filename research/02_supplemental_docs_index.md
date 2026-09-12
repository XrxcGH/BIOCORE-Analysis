# 02 — Supplemental (Non-Manual) Official FRC Document Index

**Purpose:** map and mirror everything that changes how the BIOCORE game manual is *read*, so the post-kickoff deep review sees the whole rule surface — not just the manual PDF.

**Compiled:** 2026-08-21 · **Last verified & extended:** 2026-08-22
**Local root:** `manuals/archive/supplemental/`
**On disk now:** **433 files, 1.8 GiB**, 33 folders. Zero corrupt/truncated files — every `.pdf` re-checked for a `%PDF` magic header and every `.zip` for `PK` this pass; all pass.
**Fetch logs:** `logs/fetch_supplemental.log`, `logs/fetch_agent.log`, `logs/fetch_archive_gapfill.log`
**Not in the public repository:** FIRST's documents are not redistributed, so none of the files indexed here is included; `bash tools/rebuild-corpus.sh --fetch` downloads the PDFs the text corpus is built from, and the rest come from the links in these tables. `[AUDIT 2026-09-12]`

> Read [`00_PREMISE_CORRECTION.md`](./00_PREMISE_CORRECTION.md) first. FRC **BIOCORE presented by Haas** kicks off **Jan 9, 2027, 12:00 p.m. ET**. **"Pollen", StarterBots and Skill Builders belong to FTC BIOBUZZ presented by RTX** — a different program in the same FIRST CANOPY 2026-27 season. Re-confirmed 2026-08-22: the FIRST post that names Pollen, StarterBots and Skill Builders is an **FTC** post ([Game Preview 2027: StarterBots, Skill Builders, Field Elements and More!](https://community.firstinspires.org/game-preview-field-elements)) describing **BIOBUZZ**, whose scoring element is Pollen and whose kickoff was Sept 12, 2026. **The FRC BIOCORE scoring element has no public name or specification as of today.** Nothing in this index assumes otherwise.

Tags: **[VERIFIED]** = confirmed by fetching the primary source or extracting text from an official file on disk, with the verification date given. **[SPECULATION]** = pattern-based inference, explicitly not confirmed.

---

## 0. The three things to internalize

1. **FRC never publishes an ordered precedence list.** The hierarchy in §1 is assembled from ten scattered statements across the manual plus two webpages. Students read the manual PDF and stop; the exploitable gaps live in the seams between documents.
2. **The manual PDF mutates in place at the same URL all season.** The file you download on kickoff day and the file at that URL in April are different documents with the same name and the same URL. §1.5.
3. **There is a fourth rule channel nobody indexes: the FRC Community Blog.** Legal-device additions and removals, event-rule changes, advancement changes, and control-system mandates are announced there and *never* appear in a Team Update. §9.

---

## 1. Documents that override or amend the manual, in precedence order

### 1.1 The chain

| # | Layer | What it governs | Beats | Loses to |
|---|---|---|---|---|
| 0 | **English game manual PDF on the Season Materials webpage** | Everything textual | Translations, the assistive-device DOCX, the HTML render, any third-party copy | — (base document) |
| 1 | **Specific rule language** (the numbered rule body) | Rule meaning | Colloquial headline; blue boxes; metric conversions | Team Updates |
| 2 | **Team Updates** | Any revision to any official season documentation | The manual text they revise | Nothing — they *become* the manual |
| 3 | **Official FIELD drawings + 3D CAD** | Field geometry, tolerances, construction | Manual illustrations and manual-stated dimensions (explicitly "nominal") | Team Updates that revise the drawings |
| 4 | **Q&A answers** | Interpretation only | Nothing — explicitly non-superseding | Manual text; Team Updates |
| 5 | **Event authorities in the moment** (Head REFEREE, LRI, FTA) | Score, penalty, card, legality *at that event* | Everything above, in practice, on the day | Nothing at the event |

Running parallel to layers 0–4, and easy to miss:
- The **District & Regional Events (Event Experience) webpage** is separately self-declared authoritative for event rules & expectations, and is itself amended by Team Updates.
- The **Awards webpages** and the **official FIELD drawings** are named in manual §1.9 as Q&A-clarifiable — i.e. FIRST treats them as rule text. **There is no awards *manual* for FRC; the award criteria are webpage content.**
- The **FRC Community Blog** sits outside this chain entirely and still changes what is legal (§9).
- **Part-legality rulings by email.** Manual §8 routes metric-equivalent part questions to `frcparts@firstinspires.org` "for an official ruling" — a private, uncited, unarchived ruling channel that binds only the asking team.

### 1.2 Quoted authority — all verbatim

Source for every quote below: the **2026 REBUILT Game Manual, Version TU22, 166 pp.**, text extracted locally via `pdftotext -layout` from `manuals/archive/frc/2026_REBUILT_GameManual.pdf`. Page numbers are the manual's own footer pages. Canonical URL: <https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf>. **All ten quotes re-verified verbatim against the local extraction on 2026-08-22.**

`[AUDIT 2026-09-12]` For the public repository, every quote longer than a sentence or two is cut to its operative sentence, the rest of each passage is paraphrased outside the quotation marks, and every section and page cite is unchanged. The kept text was re-checked verbatim against the same local extraction and the webpage snapshot.

**Literalism — the interpretive rule that governs all others** (§1.6 *This Document & Its Conventions*, **p. 9**):
> "The intent of this manual is that the text means exactly, and only, what it says. … There are no hidden requirements or restrictions."

The omitted sentence tells readers not to interpret the text from assumed intent, past rules, or real-life situations.

**Rule body beats blue box** (§1.6, **p. 10**):
> "While blue boxes are part of the manual, they do not carry the weight of the actual rule (if there is an inadvertent conflict between a rule and its blue box, the rule supersedes the language in the blue box)."

**Rule body beats headline** (§1.6, **p. 10**):
> "Any disagreement between the specific language used in the rules and the colloquial language is an error, and the specific rule language is the ultimate authority."

**Imperial beats metric** (§1.6, **p. 10**):
> "The metric conversions are offered for convenient reference only and do not overrule or take the place of the imperial dimensions presented in this manual and the official drawings (i.e. dimensions and rules will always defer to measurements using imperial units)."

**English PDF is the commanding version** (§1.7 *Translations & Other Versions*, **p. 10**):
> "In the event that a rule or description is modified in an alternate version of this manual, the English pdf version as published on the Season Materials webpage is the commanding version."

**Team Updates amend official documentation** (§1.8 *Team Updates*, **p. 11**):
> "Team Updates are used to notify the FIRST Robotics Competition community of revisions to the official season documentation (e.g. the manual, drawings, etc.) or important season news."

The same section sets the cadence: Tuesdays and Fridays from the first Tuesday after Kickoff through the Tuesday before Week 1 events, then Tuesdays only from Week 1 through the week after the final District Championship events. Updates are posted on the Season Materials webpage, generally before 5 p.m. Eastern, with additions highlighted in yellow and deletions struck through.

**Q&A jurisdiction is wider than the manual** (§1.9 *Question and Answer System*, **p. 11**) — the sentence most teams miss:
> "The Question and Answer System (Q&A) is a resource for clarifying the 2026 REBUILT Game Manual, **Awards webpages**, **official FIELD drawings**, and/or **District and Regional Events webpage** content."
>
> (emphasis added) → the Awards webpages and the District & Regional Events webpage are rule-bearing documents, not marketing pages.

**Q&A does not supersede; refs and inspectors do** (§1.9, **p. 11**):
> "The responses in the Q&A do not supersede the text in the manual, although every effort will be made to eliminate inconsistencies between the two."

The paragraph goes on to name REFEREES and INSPECTORS as the ultimate authority on rules, citing section 9 and §6.7.

**Q&A can *cause* manual revisions** (§1.9, **p. 11**) — the feedback loop:
> "The Q&A may result in revisions to the text in the official manuals (which are communicated using the process described in Team Updates)."

**CAD/drawings govern the field, not the manual's numbers** (§5.1 *Dimensions and Accuracy*, **p. 17**):
> "The 3D CAD model is the official representation of the REBUILT FIELD and how it is constructed."

The same list says the section's illustrations are for general understanding only and that "dimensions included in the manual are nominal and no tolerances are implied." It sends readers to the official drawings for exact dimensions, tolerances, and construction details: the Field Dimension Drawings package gives each FIELD element's critical dimensions, the FIELD Manual covers construction and how construction type affects tolerances, and the FIELD Acceptance Checklists (welded and AndyMark) list the controlled dimensions event staff check several times during the event.

**Timers beat audio cues** (§5.12 FMS, **p. 36**; repeated for the alliance-selection pick timer at §10, p. 124):
> "audio cues are intended as a courtesy to participants and not intended as official MATCH markers. If there is a discrepancy between an audio cue and the FIELD timers, the FIELD timers are the authority."

**Event-day final authority on gameplay** (§6.7 *Head REFEREE and FTA Interaction*, **p. 52**):
> "The Head REFEREE rulings are final. No event staff, including the Head REFEREE, will review video, photos, artistic renderings, etc. of any MATCH, from any source, under any circumstances."

Before these sentences, the section gives the Head REFEREE ultimate authority in the ARENA during the event, with input allowed from Game Designers, FIRST personnel, the FTA, and other event staff.

**Event-day final authority on legality** (§9 *Inspection & Eligibility*, **p. 115**):
> "At each event, the Lead ROBOT INSPECTOR (LRI) has final authority on the legality of any COMPONENT, MECHANISM, or ROBOT."

The LRI may consult the Global LRIs or FIRST personnel before deciding, and INSPECTORS may re-inspect ROBOTS at any time.

**The private ruling channel** (§8 preamble, **p. ~76**):
> "If your team has a question about a metric-equivalent part's legality, please e-mail your question to the FIRST Robotics Competition Kit of Parts team at frcparts@firstinspires.org for an official ruling."

Requests to approve alternate devices for future seasons go to the same address, with item specifications.

**Webpage-level authority** — FRC *District & Regional Events / Event Experience* page. [VERIFIED verbatim 2026-08-22 against local snapshot `webpages/FRC_EventExperience_webpage_snapshot_2026-08-21.html`]:
> "This webpage is considered the authority on Rules & Expectations for FIRST Robotics Competition Events."
> — [firstinspires.org/resource-library/frc/event-experience](https://www.firstinspires.org/resource-library/frc/event-experience)

The same passage says Team Updates announce content changes to any official season documentation, including the Game & Season Manual, award deadlines, and drawings, but not typo fixes, and that the page's Updates dates change to match the Team Update behind each change.

> **Page-citation audit, closed.** Two earlier passes disagreed about the page of the "commanding version" quote. Settled 2026-08-22 by page-by-page `pymupdf` extraction with each page's own `N of 166` footer as the check: it is on **p. 10**. §1.7's *heading* sits near the p. 10/11 break, its *text* does not. Full table: literalism p. 9; blue box p. 10; headline p. 10; imperial p. 10; commanding version p. 10; Q&A jurisdiction p. 11; Q&A non-supersession p. 11; 3D CAD p. 17; FIELD timers p. 36; Head REFEREE p. 52; LRI p. 115. Manual is **166 pp.**

### 1.3 Consequences a high-school student will miss

1. **A "rule" can live in six places.** Manual body, official drawings, Awards webpages, Event Experience webpage — all four explicitly Q&A-clarifiable — plus the Community Blog and the `frcparts@` email channel, neither of which is.
2. **A blue box is not a rule, but it is not nothing.** It is "part of the manual" and loses *only on conflict*. Blue-box permissions that no rule addresses survive, because §1.6 also states there are "no hidden requirements or restrictions." Argue this from §1.6's literalism clause, not from intent.
3. **Metric users lose measurement arguments at inspection.** All dimensional disputes resolve in imperial. A team that designs in millimetres and rounds to the metric figure printed in the manual can be legal in metric and illegal in imperial.
4. **Manual dimensions are nominal and untoleranced.** Any strategy that depends on a field dimension being exact is exposed. The toleranced numbers are in the Field Dimension Drawings; the *actually-checked-at-events* numbers are in the Field Acceptance Checklists. **Anything not on an acceptance checklist is not verified at any event** — and the manual explicitly says "the FIELD is expected to change during MATCH play."
5. **Q&A answers are frequently pointer answers.** In the 2026 export a large share of answers say "see Team Update NN" — the substance is in the Team Update, not the Q&A. Indexing the Q&A without following the pointers gives you a hollow corpus.
6. **Head Referee will never review video.** Any strategy whose legality depends on post-hoc proof is dead on arrival.
7. **The Q&A feedback loop is a lever, not just a lookup.** §1.9 states Q&A *may result in* manual revisions. A well-constructed question filed in the first two weeks is the cheapest way to get an ambiguity resolved in your favour. Questions filed late get answered but rarely produce a Team Update.
8. **Team Update cadence is asymmetric.** Twice weekly (Tue + Fri) only until the Tuesday before Week 1 — i.e. the volatile window is the ~6 weeks of build season. After Week 1 it is Tuesdays only. Design decisions locked before the first Friday update carry the most amendment risk.
9. **Q&A question quality is itself gated.** §1.9 lists what will *not* be answered: vague situations, challenges to past-event decisions, and design reviews for legality. FIRST demonstrated this on the record — 2026 **Q1** is a deliberate nonsense question ("chute door") posted by team `99999` (the key-volunteer account) and answered with a pointer to §1.9. Budget your questions: broad "is this legal?" questions are wasted.

### 1.4 Precedence chain, as one sentence

> Manual English PDF (rule body > headline > blue box; imperial > metric) → amended by Team Updates → field geometry deferred to official drawings/CAD (toleranced), with only acceptance-checklist dimensions actually verified at events → interpreted but never overridden by Q&A → and on event day, overridden in practice by the Head REFEREE (gameplay) and LRI (legality), whose rulings are final and unreviewable. Outside this chain, the Event Experience and Awards webpages carry rule weight, the `frcparts@` mailbox issues unpublished part rulings, and the Community Blog changes device legality without ever entering it.

### 1.5 Version drift — the trap inside the PDF itself

[VERIFIED] The manual PDF is republished at the *same URL* after Team Updates, and the footer version marking changed format in 2026.

| Season | Version marking | Pages by marker (final PDF) |
|---|---|---|
| 2023 CHARGED UP | per-page `V0`…`V12` in footer | V9:47, V11:38, V8:11, V12:11, V2:10, V4:9, V1:8, **V0:3** |
| 2025 REEFSCAPE | per-page `V0`…`V13` in footer | V11:57, V4:22, V13:15, V6:13, V3:12, V2:10, V5:9, V1:8, **V0:5** |
| 2026 REBUILT | uniform `Version: TU22` on every page | no per-page signal |

**Why it matters:** in 2023 and 2025 the footer told you exactly which pages had been amended and at which revision — only **3** (2023) and **5** (2025) pages survived the entire season untouched. In 2026 FIRST replaced that with a single whole-document stamp, destroying the signal. [SPECULATION] BIOCORE will follow 2026. **Archive the kickoff-day manual PDF within minutes of release and diff every republished version yourself** — the PDF will no longer tell you what moved. `tools/frc_diff.py` exists for this.

---

## 2. Category A — Team Updates (the amending instrument)

Base path: `https://firstfrc.blob.core.windows.net/frc<YEAR>/Manual/TeamUpdates/`. **Naming is not stable across seasons** — the single biggest gotcha when scripting downloads, and the thing that will break a naive kickoff-day script.

| Season | Range held | Naming on CDN | Combined PDF | Local folder (files) |
|---|---|---|---|---|
| 2026 REBUILT | 00–22 | **`2026TeamUpdate00.pdf` for #00, then `REBUILT_TeamUpdateNN.pdf`** | `REBUILT_TeamUpdate-Combined.pdf` | `2026_TeamUpdates/` (24) |
| 2025 REEFSCAPE | 00–21 | `TeamUpdateNN.pdf` | `TeamUpdate-Combined.pdf` | `2025_TeamUpdates/` (23) |
| 2024 CRESCENDO | 00–21 | `TeamUpdateNN.pdf` | `TeamUpdates-combined.pdf` | `2024_TeamUpdates/` (23) |
| 2023 CHARGED UP | 00–21 | `TeamUpdateNN.pdf` | `TeamUpdates-combined.pdf` | `2023_TeamUpdates/` (23) |
| 2022 RAPID REACT | 01–21 (**no 00**) | `TeamUpdateNN.pdf` | `TeamUpdates-combined.pdf` | `2022_TeamUpdates/` (22) |
| 2021 IR at Home | 00–19 | `2021TeamUpdateNN.pdf` | `2021TeamUpdates-combined.pdf` | `2021_TeamUpdates/` (21) |
| 2020 INFINITE RECHARGE | 01–17 (COVID cutoff) | `TeamUpdateNN.pdf` | `TeamUpdates-combined.pdf` | `2020_TeamUpdates/` (18) |
| 2019 DEEP SPACE | 01–21 | `TeamUpdateNN.pdf` | `TeamUpdates-combined.pdf` | `2019_TeamUpdates/` (22) |
| 2012–2018 | combined only | `TeamUpdates-combined.pdf` / `<YEAR>TeamUpdatesComplete.pdf` | held | `<YEAR>_TeamUpdates/` (1 each) |

**[VERIFIED 2026-08-22 — ceiling re-probe]** Every season 2019–2026 re-probed at TU22–TU28 (2020 at TU22–28, 2019 at TU22–28). **All 404.** Confirmed maxima: 2019 = 21, 2020 = 17, 2021 = 19, 2022 = 21, 2023 = 21, 2024 = 21, **2025 = 21**, **2026 = 22**. No FRC season 2019–2026 has exceeded Team Update 22. 2022 genuinely has no TU00 (probed, 404).

**[VERIFIED 2026-08-22 — the naming trap, in detail]** `https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/TeamUpdate01.pdf` returns **404**, while `.../REBUILT_TeamUpdate01.pdf` returns 200 and `.../frc2025/Manual/TeamUpdates/TeamUpdate01.pdf` still returns 200. So 2026 was the season FIRST introduced the **game-name prefix**, and it applied it to #01–#22 but *not* to #00, which is `2026TeamUpdate00.pdf` (year prefix, no game name). Local copies were byte-size-matched to the live CDN objects this pass (TU00 = 192,563 B; TU22 = 172,032 B; Combined = 1,440,345 B). **A BIOCORE script that only tries `TeamUpdateNN.pdf` will silently fetch nothing.** See §12 for the fetch order.

**[VERIFIED 2026-08-22]** No "combined" PDF exists at `TeamUpdate-Combined.pdf` for 2022/2023/2024 — those seasons use `TeamUpdates-combined.pdf` (lowercase `c`, plural `Updates`). 2025 uses `TeamUpdate-Combined.pdf` (capital `C`, singular). 2026 uses `REBUILT_TeamUpdate-Combined.pdf`. Three different shapes in three consecutive seasons.

**Why it matters:** TU00–TU02 are where kickoff-day manual errors get fixed, and historically where the largest strategic swings happen — scoring clarifications, bumper geometry, human-player limits. The combined PDF is the fastest way to read the whole amendment history in one pass; the individual PDFs preserve the yellow-highlight / strikethrough diff formatting per release, which the combined file sometimes flattens. **Read both.**

**BIOCORE analytic use:** on kickoff day, diff the manual against TU00 and TU01 immediately. Any rule amended in the first week is a rule the GDC itself found ambiguous — that is a pre-labelled list of the loopholes worth hunting.

---

## 3. Category B — Q&A System

### 3.1 How it works [VERIFIED 2026-08-22]

| Property | Finding |
|---|---|
| URL | <https://frc-qa.firstinspires.org/> |
| Technology | Meteor SPA over **DDP/SockJS long-polling**. No REST/JSON API, no export button, no season selector. |
| Seasons served | **Exactly one at a time.** Wiped at rollover. |
| **Current state (2026-08-22)** | **Still serving the 2026 REBUILT corpus, read-only/closed.** Live DDP pull today returned the same 86 manual sections and the same Q1–Q3 as the archived export. **It has not yet rolled to 2027.** |
| Citation format | Answers are cited by bare Q number — "Q123" / "per Q123". IDs are global sequential within a season and are the same integer in the SPA and in FIRST's PDF export. |
| Past-season archive in-app | **None.** The app holds only the current season. |
| Wayback usefulness | **None** — the SPA renders client-side, so snapshots are empty shells. |
| Official bulk export | **Prose PDF only, published after the season ends** (see §3.2). Nothing machine-readable is ever published. |
| Unofficial bulk export | **Yes — `tools/frc_qa_scrape.py`** (this project). Speaks DDP directly. §3.3. |
| Question gating | §1.9 of the manual: no vague situations, no challenges to past-event decisions, no design reviews, no duplicates, no nonsense. |
| Asker identity | Team number is published with every answer. **Team `99999` = key volunteers** (referees, inspectors) — those questions are the ones FIRST itself wanted on the record, and are the highest-signal entries in the corpus. |

### 3.2 Official season Q&A exports — all downloaded

Pattern: `https://firstfrc.blob.core.windows.net/frc<YEAR>/FRC<YEAR><GAMENAME>-QandAExport.pdf` (2022 onward). Older seasons use ad-hoc paths.

| Season | Local file | URL | Why it matters |
|---|---|---|---|
| 2026 REBUILT | `2026_QA/2026_QAExport_OFFICIAL.pdf` + `qa2026.txt` | [link](https://firstfrc.blob.core.windows.net/frc2026/FRC2026REBUILT-QandAExport.pdf) | The immediately-prior season's full interpretive record; the closest prior for BIOCORE rule-shape |
| 2025 REEFSCAPE | `2025_QAExport_OFFICIAL.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2025/FRC2025REEFSCAPE-QandAExport.pdf) | — |
| 2024 CRESCENDO | `2024_QAExport_OFFICIAL.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2024/FRC2024CRESCENDO-QandAExport.pdf) | Last season with a game piece comparable to a ball/disc handling problem |
| 2023 CHARGED UP | `2023_QAExport_OFFICIAL.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2023/FRC2023CHARGEDUP-QandAExport.pdf) | First AprilTag season — vision/localization Q&A precedent |
| 2022 RAPID REACT | `2022_QAExport_OFFICIAL.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2022/FRC2022RapidReact-QandAExport.pdf) | **Ball game.** Highest-value prior if BIOCORE uses a ball |
| 2021 IR at Home | `2021_QAExport_OFFICIAL.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2021/Manual/FRCQA-2021InfiniteRecharge.pdf) | — |
| 2019 DEEP SPACE | `2019_QAExport_OFFICIAL.pdf` (18 MB) | [link](https://firstfrc.blob.core.windows.net/frc2019/2019_QA_Full_Archive.pdf) | — |
| 2012–2015, 2017–2020 | `QA_Archives/<YEAR>_QA_Full_Archive.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | Long-run precedent |
| 2020 pre-season | `QA_Archives/2020_QA_PreSeason_Archive.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2020/2020_QA_PreSeason_Archive.pdf) | Only surviving example of a **pre-kickoff** Q&A window |
| 2016 | **missing** | — | [VERIFIED 2026-08-22] No 2016 Q&A archive exists at any tried CDN path; not linked from the Archived Games page either |

### 3.3 Structured 2026 Q&A export (produced locally — the reusable asset)

`tools/frc_qa_scrape.py` → `2026_QA/` (and an independent re-pull in `2026_QA_live_recheck/`).

| File | Contents |
|---|---|
| `2026_QA_full_export.json` | Raw documents — question, published answer, asker team, section, tags, asked/answered timestamps |
| `2026_QA_index.csv` | **221 published Q&A rows** (`qa_number, manual_section, tags, title, asked, answered`), IDs running to 232 |
| `2026_QA_full_export.md` | Readable Q/A text |
| `2026_QA_manual_sections.json` | **86** manual sections FIRST exposes as filing targets |
| `2026_QA_tags.json` | **101** controlled tags — effectively FIRST's own list of the season's contested defined terms |
| `2026_QA_rule_index.json` | The rule list the UI links questions to |

**[VERIFIED 2026-08-22]** The `2026_QA_live_recheck/` re-pull is **byte-identical** to `2026_QA/` — the corpus is frozen and the scrape is reproducible.

**Operational consequence for BIOCORE:** the official PDF export lands ~May 2027, far too late to help during build season. **Run `frc_qa_scrape.py --season 2027` daily from Q&A open (~Jan 13, 2027) through Championship.** The 86 sections and 101 tags are published *before* answers accumulate, which means on Q&A-open day you get FIRST's own taxonomy of the BIOCORE manual — a free structural map of which sections FIRST expects to be argued about.

### 3.4 2026 Q&A load by manual section — the prior for BIOCORE

The 2026 index shows where interpretive pressure concentrated: **§8.4 BUMPER Rules**, **§7.4 In-MATCH**, **§6.4 MATCH Periods**, **§6.5 Scoring**, **§5 ARENA** subsections. Bumper geometry and in-match contact/possession rules are perennially the top two. See `reference/QA-AMBIGUITY-HOTSPOTS.md` for the section-level heat map. [SPECULATION] Expect the same two to dominate BIOCORE; pre-write your bumper and possession questions before kickoff so they can be filed in the first 48 hours.

---

## 4. Category C — Field drawings, CAD, AprilTags

FIRST reorganized this area twice: `PlayingField/` → `FieldAssets/`, and in 2026 split the drawing package into complete/evergreen/game-specific plus a separate dimension package.

| Doc type | Season | Local file | URL | Why it matters |
|---|---|---|---|---|
| **Field Dimension Drawings** | 2026 | `2026_FieldDimensionDrawings.pdf` (31 pp) | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dimension-dwgs.pdf) | **The toleranced numbers.** Manual dimensions are nominal; these are not. First stop for any geometry argument |
| **FIELD Manual** | 2026 | `2026_FieldManual.pdf` (37 MB) | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/field-manual.pdf) | Build instructions + how construction type changes tolerances. Tells you how much the field can legally vary between events |
| **Field Acceptance Checklist — welded** | 2026 | `2026_FieldAcceptanceChecklist_Welded.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-acceptance-welded.pdf) | **The only dimensions actually verified at an event.** Anything not here is unchecked |
| **Field Acceptance Checklist — AndyMark** | 2026 | `2026_FieldAcceptanceChecklist_AndyMark.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-acceptance-am.pdf) | Same, for the AndyMark field variant — the two variants have different tolerances |
| **Drawing package — complete** | 2026 | `Drawings/2026_FieldDrawings-Complete.pdf` (321 pp, 288 MB) | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dwg-complete.pdf) | **Downloaded this pass.** Evergreen + game-specific in one file |
| **Drawing package — evergreen** | 2026 | `Drawings/2026_FieldDrawings-Evergreen.pdf` (109 pp, 87 MB) | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dwg-evergreen.pdf) | Carpet, guardrails, perimeter, alliance wall structure — **the parts that carry into BIOCORE unchanged** |
| **Drawing package — game-specific** | 2026 | `Drawings/2026_FieldDrawings-GameSpecific.pdf` (196 pp, 184 MB) | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dwg-game-specific.pdf) | **Downloaded this pass.** The 2026-only elements; the diff against evergreen shows exactly what a season contributes |
| Field drawings | 2019–2025 | `2019_FieldDrawings.pdf`, `2020/2021/2022/2023_FieldDrawings-{Evergreen,GameSpecific}.pdf`, `2024_FieldDrawings.pdf`, `2025_FieldDrawings.pdf`, `Drawings/2023_FieldDrawings.zip`, `Drawings/2024_FieldDrawings-Evergreen.pdf`, `Drawings/2025_FieldDrawings-{Evergreen,GameSpecific}.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | Multi-season evergreen diff = what FIRST considers permanent |
| **Layout & Marking Diagram** | 2020–2025 | `2020–2024_LayoutAndMarkingDiagram.pdf`, `2025_FieldLayoutAndMarkingDiagram.pdf`, `Drawings/2012–2018_LayoutAndMarkingDiagram.pdf` | per season | Tape layout for a practice field. **Folded into the drawing package in 2026** — no standalone file exists for 2026 |
| **AprilTag Images & User Guide** | 2024, 2025, 2026 | `2024/2025/2026_AprilTag_Images_and_User_Guide.pdf` | [2026](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-apriltag-images-user-guide.pdf) · [2025](https://firstfrc.blob.core.windows.net/frc2025/FieldAssets/Apriltag_Images_and_User_Guide.pdf) · [2024](https://firstfrc.blob.core.windows.net/frc2024/FieldAssets/Apriltag_Images_and_User_Guide.pdf) | Tag family, size, ID→location map, print tolerances. **The tag ID map is a rule-bearing document for any vision strategy** |
| **Field CAD (STEP)** | 2022–2026 | `FieldCAD/2022_RAPIDREACT2022Field-STEP.zip` *(downloaded this pass)*, `2023_CHARGEDUP2023Field-STEP.zip`, `2024_CRESCENDO2024Field-STEP.zip`, `2025_2025Field-STEP.zip`, `2026_FE-2026-rev-rebuilt-playing-field.step` | per season | Manual §5.1: "The 3D CAD model is the **official representation** of the FIELD." This outranks the manual's own illustrations |
| **Field CAD (Fusion)** | 2026 | `FieldCAD/2026_AutodeskFusionFiles.zip` (108 MB) *(downloaded this pass)* | [link](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-autodesk-fusion-files.zip) | Same model, Fusion-native |
| **Practice/test element STEP** | 2026 | `FieldCAD/2026_{event-test,team-practice,team-test}-elements.step`, `2026_wood-practice-perimeter.step` | [FieldAssets](https://www.firstinspires.org/resources/library/frc/playing-field) | The **wood practice perimeter** is the low-cost field spec — what your practice field must match to be representative |
| **Low-cost / team-version field elements** | 2012–2026 | `FieldElements_LowCost/` (25 files incl. `2026_TE-26{000,100,200,300,500,600}-build-instructions.pdf`, `2025_TeamElements.zip`, `2024_3DPrintedFieldFiles.zip`) | [Playing Field](https://www.firstinspires.org/resources/library/frc/playing-field) | The TE-drawings define the *sanctioned* practice-element geometry. Building to these means your practice results transfer |
| **Scoring-element assessments** | 2024, 2026 | `ScoringElement/2024_NOTECounterAssessment.pdf`, `2024_NOTEUsabilityGuide.pdf`, `2026_FuelCounterAssessment.pdf` | [2026](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-fuel-counter-assessment.pdf) | **Sleeper category.** FIRST publishes measured accuracy/failure modes of the automated scoring hardware. If BIOCORE auto-counts a scoring element, its assessment doc tells you the counter's error behaviour — directly exploitable in scoring strategy |
| Onshape master models | 2026 | link-only | [Playing Field page](https://www.firstinspires.org/resources/library/frc/playing-field) | Manual §5.1: "All official models for the REBUILT FIELD were created in Onshape" — the Onshape docs are upstream of every exported format |
| WPILib AprilTag field-layout JSON | 2023–2026 | link-only, **not a FIRST document** | [wpilibsuite/allwpilib](https://github.com/wpilibsuite/allwpilib) | The tag pose table every vision stack actually consumes. Community-maintained; **not authoritative** — if it disagrees with the FIRST AprilTag guide, the FIRST guide wins |

---

## 5. Category D — Inspection

| Doc type | Season | Local file | URL | Why it matters |
|---|---|---|---|---|
| **Inspection Checklist** | 2026 | `2026_InspectionChecklist.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026FRCInspectionChecklist.pdf) | The **operationalized** rule set. Every line maps to an R- or I-rule; what is *not* on it is not routinely checked |
| Inspection Checklist | 2013, 2015–2025 | `<YEAR>_InspectionChecklist.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | Year-over-year diff shows which rules FIRST decided needed a physical check — a proxy for which rules got abused |
| Abbreviated checklist | 2022 | `2022_InspectionChecklist_Abbreviated.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | Only season with a short form; shows FIRST's own view of the *critical* subset |
| **Robot Inspection Quick Reference** | — | **does not exist** | — | [VERIFIED 2026-08-22] No such file 2022–2026 under any tried name on the CDN or `hubfs`. Commonly-referenced by teams; it is a community artifact, not a FIRST one |
| Weight/size verification | — | **no standalone doc** | — | [VERIFIED] Weight and size limits and their measurement tolerances live in manual §8.1 and §10.3 (Measurement) only |

**Analytic use:** the checklist is the fastest legal-risk audit available. Diff `2026_InspectionChecklist.pdf` against `2025_InspectionChecklist.pdf` to see which rules FIRST escalated to a checked item — those are the rules with a live enforcement history.

---

## 6. Category E — Kit of Parts

| Doc type | Seasons | Local files | URL | Why it matters |
|---|---|---|---|---|
| KOP Checklists (Black Tote / Gray Tote / Season-Specific Box / Drive Base Kit / Separate Items / Everyone Box) | 2020–2026 | `KOP/` (33 files) | [Kit of Parts](https://www.firstinspires.org/resources/library/frc/kit-of-parts) | Manual §8.3 exempts KOP items from budget rules by reference to these lists. **The checklist *is* the definition of "KOP item"** — a part on the list has different legal status than the identical part bought retail |
| Voucher Catalog | 2023–2026 | `KOP/<YEAR>_VoucherCatalog.pdf`, `KOP/2026_VoucherCatalog.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2026/frc-voucher-catalog-2026.pdf) | Enumerates what is obtainable at zero marginal cost — directly shapes budget-rule strategy |
| FIRST Choice process | cross-season | `KOP/FRC_FIRSTChoiceProcess.pdf` | [link](https://www.firstinspires.org/hubfs/web/program/frc/resources/first-choice-process.pdf) | Manual §8.3 names FIRST Choice as a KOP-equivalent source |
| KitBot (build instructions, drawings, iteration guide, code) | 2024–2026 | `KitBot/` (9 files incl. `2026_KitBot_{BuildInstructions,Drawings,Drawings_Metric,IterationGuide,JavaGuide}.pdf`) | [KitBot](https://www.firstinspires.org/resources/library/frc/kitbot) | **Rule-bearing by reference:** manual §8.4 says "reference the KitBot Instructions for a detailed step-by-step on how to build bumpers for the KitBot." A bumper built to the KitBot instructions is presumptively legal |
| **Approved/Encouraged Devices list** | — | **no standalone doc** | — | [VERIFIED 2026-08-22] Does not exist as a separate file. The motor list, battery spec, and legal-device tables are **in-manual tables only** (§8.5, §8.6). Additions/removals are announced on the **Community Blog** (§9), never in a Team Update |

---

## 7. Category F — Cross-season rule-bearing / rule-adjacent documents

| Doc type | Local file | URL | Why it matters |
|---|---|---|---|
| **FIRST Safety Manual** | `crossseason/FIRST_SafetyManual.pdf`, `2020/2021/2022_SafetyManual.pdf` | [Safety](https://www.firstinspires.org/resources/library/safety) | **Incorporated by reference** — manual §8.6 and §12 both defer to it ("Please see the FIRST Safety Manual for additional information") |
| **Pneumatics Manual** | `crossseason/FRC_PneumaticsManual.pdf` | [Technical Resources](https://www.firstinspires.org/resources/library/frc/technical-resources) | The only expanded treatment of §8.8 pneumatic rules; inspectors use it |
| **Bumper Guide** | `crossseason/FRC_BumperGuide.pdf` | [Technical Resources](https://www.firstinspires.org/resources/library/frc/technical-resources) | §8.4 is the single most Q&A'd section every season. This is FIRST's own illustrated reading of it |
| Judge Manual | `crossseason/FRC_JudgeManual.pdf` | [Awards](https://www.firstinspires.org/resources/library/frc/awards) | The **judging** rule set — invisible to most teams, fully determines award outcomes |
| Award Workbook | `crossseason/FRC_AwardWorkbook.pdf` | [link](https://www.firstinspires.org/hubfs/web/program/frc/awards/award-workbook.pdf) | Submission mechanics + deadlines. Award deadlines are explicitly Team-Update-amendable |
| Impact Award Judging Guidelines | `crossseason/FRC_ImpactAwardJudgingGuidelines.pdf` | [link](https://www.firstinspires.org/hubfs/web/program/frc/awards/fia-judging-guidelines.pdf) | Scoring rubric for the highest award |
| Leadership Award guides | `crossseason/FRC_{FIRSTLeadershipAwardGuide,LeadershipAwardJudgingGuidelines}.pdf` | [dla](https://www.firstinspires.org/hubfs/web/program/frc/awards/dla-judging-guidelines.pdf) · [fla](https://www.firstinspires.org/hubfs/web/program/frc/awards/fla-guide.pdf) | — |
| Awards best practices / Inside look at judging | `crossseason/FRC_AwardsBestPracticesForTeams.pdf`, `FRC_InsideLookAtJudgingProcess.pdf` | [best practices](https://www.firstinspires.org/hubfs/web/program/frc/awards/best-practices-for-teams.pdf) · [inside look](https://www.firstinspires.org/hubfs/web/program/frc/awards/inside-look-at-judging-process.pdf) | — |
| 2021 Award Guidelines | `2021_AwardGuidelines.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2021/Manual/2021-award-guidelines.pdf) | Last season awards had a season-specific PDF |
| Kickoff Instructions | `crossseason/FRC_KickoffInstructions.pdf` | [link](https://www.firstinspires.org/hubfs/web/program/frc/reg/kickoff-instructions.pdf) | **Linked from the live BIOCORE page today.** Kit pickup logistics for Jan 9, 2027 |
| Kickoff Game Breakdown Worksheet | `crossseason/FRC_KickoffGameBreakdownWorksheet.pdf` | [Technical Resources](https://www.firstinspires.org/resources/library/frc/technical-resources) | FIRST's own kickoff-day analysis template — a useful checklist to beat |
| Effective Strategies / Scoring Analysis | `crossseason/FRC_EffectiveStrategies.pdf`, `FRC_ScoringAnalysis.pdf` | [Technical Resources](https://www.firstinspires.org/resources/library/frc/technical-resources) | FIRST's official framing of scoring-strategy analysis |
| Tool Recommendations | `crossseason/FRC_ToolRecommendations.pdf` | [link](https://www.firstinspires.org/hubfs/web/program/frc/resources/frc-tool-recommendations.pdf) | — |
| Game Summaries 1992–2012 | `crossseason/FRC_GameSummaries_1992-2012.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | Long-run game-design pattern library |
| **Playoff Alliance Communication** | `2022–2026_PlayoffAllianceCommunication.pdf` + `_Championship` variants (2024–2026) | [2026](https://firstfrc.blob.core.windows.net/frc2026/Manual/playoff-alliance-communication.pdf) · [2026 CMP](https://firstfrc.blob.core.windows.net/frc2026/Manual/champs-playoff-alliance-communication.pdf) | The **exact script and timing** of alliance selection. Procedural rules not fully in the manual; separate Championship variant |
| **Drivers' Meeting Form** | `EventOps/FRC_DriversMeetingForm.pdf` *(downloaded this pass)* | [link](https://www.firstinspires.org/hubfs/web/program/frc/events/drivers-meeting-form.pdf) | The template the Head Referee uses at the event drivers' meeting — event-day rule emphasis in FIRST's own words |
| Single-day event plan | `EventOps/2022_SingleDayEventPlan.pdf` *(downloaded this pass)* | [link](https://firstfrc.blob.core.windows.net/frc2022/2022-single-day-plan.pdf) | Modified tournament structure precedent |
| Event Preferencing FAQ + User Guide | `Registration/FRC_EventPreferencing{FAQ,UserGuide}.pdf` | [FAQ](https://www.firstinspires.org/hubfs/web/program/frc/reg/event-preferencing-faq.pdf) · [guide](https://www.firstinspires.org/hubfs/web/program/frc/reg/event-preferencing-user-guide.pdf) | **Immediately actionable — BIOCORE Round 1 preferencing opens Sept 24, 2026, 12:00 ET** |
| Usage Reporting Data | `UsageReporting/2025-anonymized-usage-data.zip`, `2026-…zip` | [2026 post](https://community.firstinspires.org/2026-usage-reporting-data) | See §9.2 — FIRST telegraphing R-rule changes with data |
| GDC Finalists 2021 | `2021_GDCFinalists.pdf` | [link](https://firstfrc.blob.core.windows.net/frc2021/GDCFinalists/2021-gdc-finalists.pdf) | Rare published GDC design reasoning |
| 2027 controller RFP | `ControlSystem2027/2023_RFP_FRC-FTC_RobotController_for_2027.pdf` | see §10 | The origin document for the 2027 control-system change |
| Administrative Manual | `AdminManuals/2012–2016_AdministrativeManual.pdf` | [Archived Games](https://www.firstinspires.org/resources/library/frc/archived-games) | **Historical only.** [VERIFIED 2026-08-22] Probed `<YEAR>{FRC,}AdministrativeManual.pdf` for 2017–2026: **all 404.** The Administrative Manual was retired after 2016 and folded into the Game Manual as §§10–14 (Tournaments, District Tournaments, Championship, **Event Rules (E)**). There is no separate event-rules document for a modern season |
| Assistive-device text manual | `Translations/2026_GameManual_AssistiveDevice_TEXT.docx` | [link](https://firstfrc.blob.core.windows.net/frc2026/Manual/Translations/2026GameManual-AD.docx) | **The single best machine-parseable manual source.** DOCX text, no PDF layout artifacts. Loses to the English PDF on conflict (§1.7) but is far easier to diff |

---

## 8. Category G — Rule-bearing *webpages* (no PDF exists)

Named in manual §1.9 as Q&A-clarifiable, or self-declared authoritative. **These change silently; snapshot them.** All snapshots in `webpages/`.

| Webpage | Local snapshot | URL | Why it matters |
|---|---|---|---|
| **District & Regional Events / Event Experience** | `FRC_EventExperience_webpage_snapshot_2026-08-21.html` | [link](https://www.firstinspires.org/resource-library/frc/event-experience) | **Self-declared "the authority on Rules & Expectations for FIRST Robotics Competition Events."** Amended by Team Updates. Its operative sentence is quoted in §1.2 |
| **Awards** | `FRC_Awards.html` | [link](https://www.firstinspires.org/resources/library/frc/awards) | Award criteria and deadlines live here, not in the manual. Q&A-clarifiable per §1.9 |
| **Season Materials** | `FRC_SeasonMaterials.html` | [link](https://www.firstinspires.org/resources/library/frc/season-materials) | The manual's own named home for the "commanding version" and for Team Updates. **This page is where BIOCORE materials will appear on Jan 9, 2027** |
| **Playing Field** | `FRC_PlayingField.html` | [link](https://www.firstinspires.org/resources/library/frc/playing-field) | Named in §5.1 as the home of official drawings, CAD, and low-cost versions |
| **Kit of Parts** | `FRC_KitOfParts.html` | [link](https://www.firstinspires.org/resources/library/frc/kit-of-parts) | Defines KOP membership for §8.3 |
| **BIOCORE Game & Season** | `FRC_BIOCORE_GameAndSeason.html` | [link](https://www.firstinspires.org/programs/frc/game-and-season) | The 2027 landing page. **Note the URL moved from `/robotics/frc/` to `/programs/frc/`** |
| **FIRST CANOPY 2026-27** | `FIRST_CANOPY_2026-27.html` | [link](https://www.firstinspires.org/first-canopy) | Umbrella season page covering both BIOCORE (FRC) and BIOBUZZ (FTC) |
| Archived Games | `FRC_ArchivedGames.html` | [link](https://www.firstinspires.org/resources/library/frc/archived-games) | **The master index of every past-season document** (383 distinct file links). The best single source for gap-filling |

---

## 9. Category H — The FRC Community Blog: the undocumented fourth rule channel

Base: `https://community.firstinspires.org/<slug>`. Server-rendered HTML; body in `div.blog-post__body`; attachments are plain `href`s. **32 posts snapshotted** in `webpages/blog/`.

**Why this category exists:** device-legality changes, event-rule changes, advancement-formula changes, and control-system mandates are announced here and appear in *no* Team Update and *no* Q&A. A team that reads only the manual and Team Updates will miss them.

### 9.1 Posts that changed or telegraphed rules

| Date | Post | Rule consequence |
|---|---|---|
| 2025-05-21 | [Welcome to REBUILT](https://community.firstinspires.org/2025-welcome-to-rebuilt) | Season-name reveal pattern — the analogue for BIOCORE was 2026-05 |
| 2025-05-23 | [REEFSCAPE By The Numbers — New Legal Devices](https://community.firstinspires.org/2025-reefscape-by-the-numbers-part-2) | **Added legal devices mid-offseason.** Never entered a Team Update |
| 2025-08-27 | [Regional Advancement Updates for 2026](https://community.firstinspires.org/2025-regional-advancement-updates-for-2026) | Changed advancement — a §11/§13 matter |
| 2025-09-24 | [2026 Event Updates](https://community.firstinspires.org/2025-2026-event-updates) | The Sept registration-window post; the BIOCORE analogue is due ~Sept 24, 2026 |
| 2025-10-03 | [2026 Season Award Updates](https://community.firstinspires.org/2025-2026-season-award-updates) | Changed the award set before the manual existed |
| 2025-10-07 | [2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027) | §10 |
| 2025-10-24 | [2026 Robot Rules Preview](https://community.firstinspires.org/2025-2026-robot-rules-preview) | **R-rule changes published ~11 weeks before kickoff.** The single highest-value pre-kickoff post. **Watch for the BIOCORE equivalent ~Oct 2026** |
| 2025-11-10 | [Upcoming Important Dates](https://community.firstinspires.org/2025-upcoming-important-dates) | The de-facto season-dates document (§13: no season-dates PDF exists) |
| 2025-12-10 | [2026 Season Event Rule Updates](https://community.firstinspires.org/2025-2026-season-event-rule-updates) | **Event rules changed pre-kickoff, blog-only** |
| 2026-01-05 | [Head Referee Interaction Pilot](https://community.firstinspires.org/2026-head-referee-interaction-pilot) | Changed §6.7 Question Box procedure **by blog post**. Check whether it carried into 2027 before planning any Question Box workflow |
| 2026-01-06 | [Practice Field & Team Element Changes](https://community.firstinspires.org/2026-practice-field-and-team-element-changes) | Changed the sanctioned practice-element set 3 days before kickoff |
| 2026-01-13 | [Post Kickoff Information](https://community.firstinspires.org/2026-post-kickoff-information) | The post-kickoff consolidation post; **expect the BIOCORE analogue ~Jan 12-13, 2027** |
| 2026-03-02 | [FUEL Counter Update](https://community.firstinspires.org/2026-fuel-counter-update) | Mid-season change to automated scoring hardware behaviour |
| 2026-06-08 | [Pre-Orders for 2027 Scoring Elements](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements) | **BIOCORE scoring element exists and is orderable; name and spec withheld** |
| 2026-07-21 | [BIOCORE Event Registration Updates](https://community.firstinspires.org/2026-biocore-event-registration-updates) | 2027 event structure |
| 2026-08-06 | [New Global & Senior Head Referees](https://community.firstinspires.org/2026-new-global-and-senior-head-referees) | Most recent FRC post as of 2026-08-22 |

### 9.2 Usage Reporting Data — FIRST telegraphing 2027 rule changes

[VERIFIED] `UsageReporting/2026-anonymized-usage-data.zip` and `2025-…zip`, from [2026 Usage Reporting Data](https://community.firstinspires.org/2026-usage-reporting-data) (Jul 29, 2026). FIRST publishes anonymized per-robot device usage across all events. **FIRST uses this to decide which devices to keep legal.** A device with near-zero usage is a candidate for removal from the legal list; a heavily-used non-KOP device is a candidate for a new rule. Reading the 2026 dataset now is the cheapest available forecast of BIOCORE §8.5/§8.6 changes.

---

## 10. Category I — The 2027 control-system transition (BIOCORE-specific, R-rule critical)

[VERIFIED] BIOCORE is the season the FRC control system changes. This will rewrite manual §8.7 (Control, Command & Signals) and much of §8.6.

| Doc | Local | URL | Why it matters |
|---|---|---|---|
| 2023 RFP for the 2027 FRC/FTC robot controller | `ControlSystem2027/2023_RFP_FRC-FTC_RobotController_for_2027.pdf` | see below | The originating requirements document. States what FIRST asked for — a preview of what §8.7 must accommodate |
| [Introducing the Future Mobile Robot Controller](https://community.firstinspires.org/introducing-the-future-mobile-robot-controller) | `webpages/blog/FRCblog_introducing-the-future-mobile-robot-controller.html` | link | — |
| [March Updates on the Future Robot Controller](https://community.firstinspires.org/march-updates-on-the-future-robot-controller) | `webpages/blog/FRCblog_march-updates-on-the-future-robot-controller.html` | link | — |
| [Control System Update — FTC Edition](https://community.firstinspires.org/control-system-update-first-tech-challenge-edition) | `webpages/blog/FRCblog_control-system-update-first-tech-challenge-edition.html` | link | FTC moved first; FTC's rules are the leading indicator |
| [SystemCore Alpha Testing — First Wave](https://community.firstinspires.org/systemcore-alpha-testing-first-wave) | `webpages/blog/FRCblog_systemcore-alpha-testing-first-wave.html` | link | Names the hardware and the alpha cohort |
| [Introducing FIRST A301](https://community.firstinspires.org/2025-introducing-first-a301) | `webpages/blog/FRCblog_2025-12-09_IntroducingFIRSTA301.html` | link | — |
| [2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027) | `webpages/blog/FRCblog_2025-10-07_ControlSystemTestingReminder2027.html` | link | — |

**Analytic consequence:** for BIOCORE, §8.7 is the section with the least prior art. The 2026 manual's §8.7 is a *poor* prior. The FTC control-system rules and the SystemCore alpha material are better predictors. **Treat every §8.7 rule in the BIOCORE manual as new text on kickoff day** and Q&A it aggressively — new rule text is where drafting errors concentrate.

---

## 11. Category J — 2027 BIOCORE / FIRST CANOPY materials

[VERIFIED 2026-08-22] **Nothing rule-bearing has been published for BIOCORE.** The `frc2027` CDN container does not resolve for any tried path (manual, team updates including a `BIOCORE_` prefix, field drawings, KOP checklists, inspection checklist, KitBot) — **all 404**.

| Item | Status | Source |
|---|---|---|
| Game name | **BIOCORE™ presented by Haas** | [BIOCORE Game & Season](https://www.firstinspires.org/programs/frc/game-and-season) |
| Umbrella season | **FIRST CANOPY** 2026-27 | [FIRST CANOPY](https://www.firstinspires.org/first-canopy) |
| Kickoff / game reveal / manual release | **January 9, 2027, 12:00 p.m. ET** | BIOCORE Game & Season page (verified today) |
| Theme framing | "teams will use engineering skills and delve into the heart of what sustains life on Earth" | ibid. |
| Scoring element | **Exists, orderable, name and spec withheld.** AndyMark pre-order describes "a custom item manufactured overseas with properties specific to BIOCORE"; KOP quantity $70, 1/5-field quantity $169; all sales final; ships from Jan 11 | [Pre-Orders for 2027 Scoring Elements](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements) · [AndyMark BIOCORE collection](https://andymark.com/collections/2027-first%C2%AE-robotics-competition-season-biocore%E2%84%A2) |
| **NOT BIOCORE** | Pollen, StarterBots, Skill Builders are **FTC BIOBUZZ presented by RTX** (kickoff Sept 12, 2026) | [Game Preview 2027 (FTC)](https://community.firstinspires.org/game-preview-field-elements) · [FTC Skill Builders](https://community.firstinspires.org/introducing-first-tech-challenge-skill-builders) |
| Event preferencing Round 1 | **Opens Sept 24, 2026, 12:00 ET; closes Nov 17, 2026, 12:00 ET** | [BIOCORE Event Registration Updates](https://community.firstinspires.org/2026-biocore-event-registration-updates) |
| Kickoff Instructions PDF | Live now, linked from the BIOCORE page | [link](https://www.firstinspires.org/hubfs/web/program/frc/reg/kickoff-instructions.pdf) |

[SPECULATION] The 1/5-field pricing lot ($169) implies a **numerous, small** scoring element rather than a few large ones. Consistent with a ball. Not confirmed.

---

## 12. Predicted BIOCORE URLs — kickoff-day fetch list

[SPECULATION] Extrapolated from the 2026 pattern; every one re-probed and 404 as of **2026-08-22**. **Try the 2026-style name first, fall back to the 2025-style.** Naming instability is the rule, not the exception (§14).

```
Manual         https://firstfrc.blob.core.windows.net/frc2027/Manual/2027GameManual.pdf
               (fallbacks: 2027FRCGameManual.pdf, 2027GameSeasonManual.pdf)
Manual (HTML)  .../frc2027/Manual/HTML/2027GameManual.htm
Manual (DOCX)  .../frc2027/Manual/Translations/2027GameManual-AD.docx      <- BEST for parsing/diffing
Translations   .../frc2027/Manual/Translations/2027GameManual-{FR,SP,TU,PO,HE,CS}.pdf

TU 00          .../frc2027/Manual/TeamUpdates/2027TeamUpdate00.pdf         <- year prefix, no game name
TU NN          .../frc2027/Manual/TeamUpdates/BIOCORE_TeamUpdateNN.pdf     <- PRIMARY (2026 shape)
               .../frc2027/Manual/TeamUpdates/TeamUpdateNN.pdf             <- fallback (2019-2025 shape)
TU combined    .../frc2027/Manual/TeamUpdates/BIOCORE_TeamUpdate-Combined.pdf
               (fallbacks: TeamUpdate-Combined.pdf, TeamUpdates-combined.pdf)

Inspection     .../frc2027/Manual/2027FRCInspectionChecklist.pdf           (fallback: 2027-inspection-checklist.pdf)
Playoff comms  .../frc2027/Manual/playoff-alliance-communication.pdf
               .../frc2027/Manual/champs-playoff-alliance-communication.pdf

Field dims     .../frc2027/FieldAssets/2027-field-dimension-dwgs.pdf
Field pkg      .../frc2027/FieldAssets/2027-field-dwg-{complete,evergreen,game-specific}.pdf
Field manual   .../frc2027/FieldAssets/field-manual.pdf
Acceptance     .../frc2027/FieldAssets/2027-field-acceptance-{welded,am}.pdf
AprilTags      .../frc2027/FieldAssets/2027-apriltag-images-user-guide.pdf
Element assess .../frc2027/FieldAssets/2027-<element>-counter-assessment.pdf   (cf. fuel-counter / NOTE)
Field STEP     .../frc2027/FieldAssets/FE-2027-rev-biocore-playing-field.step
Fusion         .../frc2027/FieldAssets/2027-autodesk-fusion-files.zip
Low-cost perim .../frc2027/FieldAssets/wood-practice-perimeter.step
Team elements  .../frc2027/FieldAssets/TE-27NNN-build-instructions.pdf  and  TE-27NNN-rev.step

KOP            .../frc2027/KOP/2027-checklist-{black-tote,gray-tote,season-specific-box}.pdf
Voucher cat.   .../frc2027/frc-voucher-catalog-2027.pdf
KitBot         .../frc2027/KitBot/2027-kitbot-{build-instructions,iteration,drawings,java-guide}.pdf

Q&A live       https://frc-qa.firstinspires.org/                    (opens ~Jan 13, 2027; scrape daily)
Q&A export     .../frc2027/FRC2027BIOCORE-QandAExport.pdf           (posted ~May 2027 — too late to help)
```

> **`tools/probe-2027-manual.sh` needs one fix before kickoff.** It currently probes only `TeamUpdateNN.pdf` for team updates. Per the 2026 finding above that shape returns 404 for the newest season. Add `BIOCORE_TeamUpdateNN.pdf` and `2027TeamUpdate00.pdf` to its Team Updates block.

**Timing model for BIOCORE** [from 2026 manual §1.8/§1.9]: Team Updates every **Tuesday and Friday** from the first Tuesday after kickoff (**Jan 12, 2027**) through the Tuesday before Week 1; then **Tuesdays only** through the week after the final District Championship; posted before 5 p.m. ET. Q&A opens ~4 days after kickoff (2026: kickoff Jan 10, Q&A opened **Jan 14**) and closes before Championship.

**Pre-kickoff watch list, in date order:** Sept 24, 2026 (event registration + preferencing Round 1 opens) → ~Oct 2026 (2027 Robot Rules Preview blog post — the R-rule changes) → ~Nov 2026 (Upcoming Important Dates; Pre-Kickoff Virtual Kit Release, Nov 12) → ~Dec 2026 (Season Event Rule Updates) → Jan 9, 2027 (kickoff).

---

## 13. Gaps and deliberate omissions

| Item | Status |
|---|---|
| 2026 field-photo zip (`2026-field-images.zip`), Stratasys 3D-print zip, game-logo zips | Link-only by choice — not rule-bearing |
| Field CAD in SOLIDWORKS / Inventor / Onshape-native | Link-only; STEP + Fusion held, which covers the geometry. STEP is not text-analyzable regardless |
| KitBot code zips (Java/C++/LabVIEW/Python) | Link-only; the build instructions and iteration guide are the rule-bearing parts |
| 2020 Q&A *season* export | Does not exist (season cancelled). Pre-season and full archives held instead |
| **2016 Q&A archive** | [VERIFIED 2026-08-22] Does not exist at any tried CDN path and is not linked from the Archived Games page. Genuine hole in FIRST's own record |
| Q&A archives 2019–2025 in **structured** form | Only the official prose PDFs exist. The live system is single-season with no bulk-export endpoint, and Wayback holds nothing (SPA). **2026 is structured only because we scraped it while it was still live — do the same for 2027** |
| "Robot Inspection Quick Reference" | [VERIFIED 2026-08-22] No such FIRST file 2022–2026 under any tried name (CDN + `hubfs`) |
| Standalone Administrative / Event Rules manual | [VERIFIED 2026-08-22] Retired after 2016; probed 2017–2026, all 404. Folded into manual §§10–14 |
| Standalone Encouraged/Approved Devices list, motor list, battery list | [VERIFIED] Do not exist; in-manual tables only. Changes announced on the blog |
| FRC "Season Dates" PDF | [VERIFIED] Does not exist. FTC publishes one; FRC does not. The functional equivalent is the annual **"Upcoming Important Dates"** blog post |
| 2019 KOP checklists | Link-only; enumerated on the [Archived Games page](https://www.firstinspires.org/resources/library/frc/archived-games) |
| 2014 Inspection Checklist | Not published that season |
| `frc2027` anything | [VERIFIED 2026-08-22] Container does not resolve for any path |
| WPILib AprilTag JSONs | Link-only and **not authoritative** — community-maintained. Path moved since last check; resolve via the repo, not a hardcoded raw URL |
| Chief Delphi / community analysis | Deliberately excluded — this index is official sources only. See [`04_biocore_community_intel.md`](./04_biocore_community_intel.md) |

---

## 14. Method notes (reproducible)

- **Container listing is disabled server-side.** [VERIFIED 2026-08-22] `GET /frc2026?restype=container&comp=list` → 404 `ResourceNotFound`, and `GET /?comp=list` likewise, even though `/frc2026/Manual/2026GameManual.pdf` returns 200. **You cannot enumerate the CDN; you must guess filenames.** This is why the fallback lists in §12 matter.
- **CDN probing:** `curl -sL -o /dev/null -w "%{http_code}|%{size_download}"` over generated URL lists. Three traps:
  (a) a missing blob returns a **215-byte XML** body with HTTP 404, so a size check alone is not a validity test;
  (b) `firstinspires.org` returns an **83,399-byte HTML 404 page** with a 404 status — a naive `-o file` save produces a plausible-looking file that is a 404 page;
  (c) re-probe any `000` (transient TLS/timeout) before recording absence — several "missing" Team Updates in the first pass were `000`s that resolved on retry.
  **Always validate a saved PDF by its `%PDF` magic header and a saved zip by `PK`.** Both checks were re-run across all 433 files this pass; all pass.
- **Byte-size cross-check.** Local copies of the 2026 Team Updates were size-matched against live CDN objects; TU00/TU22/Combined match exactly. Do the same after any bulk fetch.
- **Manual text:** `pdftotext -layout` for grepping; `pymupdf` per-page extraction for page-accurate citations, cross-checked against each page's own `N of 166` footer.
- **Q&A:** Meteor DDP over SockJS long-polling, stdlib `urllib` only. The `qa` publication accepts a raw Mongo selector plus options from the client but **caps returns at 150 documents** — paginate with `skip`, and note that `sort` must use the array-of-pairs form (`[["asked","asc"]]`); the object form is rejected with a bare `nosub`. `rules`, `manualSections`, and `tags` take no arguments and return in full. Open a fresh DDP connection per page — the server intermittently refuses `qa` on a connection already carrying subscriptions. An independent re-pull returned byte-identical output.
- **Blog:** `community.firstinspires.org/<slug>` is server-rendered; body text is in `div.blog-post__body`. Attachment links (`.zip`, `.pdf`, `.xls`) are plain `href`s — the usage-reporting datasets are only reachable this way.
- **Best single gap-filling source:** the [Archived Games page](https://www.firstinspires.org/resources/library/frc/archived-games) carries **383 distinct document links** across all seasons. Scrape its `href`s and diff against local inventory rather than guessing URLs.
- **Naming instability, observed cases:** `TeamUpdateNN` → `GAMENAME_TeamUpdateNN` (2026); `TeamUpdates-combined.pdf` → `TeamUpdate-Combined.pdf` → `GAMENAME_TeamUpdate-Combined.pdf` (three shapes in three seasons); `KitofParts/` → `KOP/`; `PlayingField/` → `FieldAssets/`; `<YEAR>LayoutMarkingDiagram.pdf` → `<YEAR>FieldDrawings-FieldLayoutAndMarking.pdf` → folded into the drawing package (2026); `<YEAR>-inspection-checklist.pdf` → `<YEAR>FRCInspectionChecklist.pdf` (kebab → CamelCase and back); `<YEAR>KOPChecklist-Name.pdf` → `<YEAR>-checklist-name.pdf`; the game-and-season page moved from `/robotics/frc/` to `/programs/frc/`. **Never assume last season's path; always try both cases.**

---

## 15. What changed in the 2026-08-22 pass

**Newly downloaded** (all verified on disk):

| File | Size | Source |
|---|---|---|
| `Drawings/2026_FieldDrawings-Complete.pdf` | 288 MB, 321 pp | [2026-field-dwg-complete.pdf](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dwg-complete.pdf) |
| `Drawings/2026_FieldDrawings-GameSpecific.pdf` | 184 MB, 196 pp | [2026-field-dwg-game-specific.pdf](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-field-dwg-game-specific.pdf) |
| `Drawings/2023_FieldDrawings.zip` | 36 MB | [2023FieldDrawings.zip](https://firstfrc.blob.core.windows.net/frc2023/FieldAssets/2023FieldDrawings.zip) |
| `FieldCAD/2026_AutodeskFusionFiles.zip` | 108 MB | [2026-autodesk-fusion-files.zip](https://firstfrc.blob.core.windows.net/frc2026/FieldAssets/2026-autodesk-fusion-files.zip) |
| `FieldCAD/2022_RAPIDREACT2022Field-STEP.zip` | 15 MB | [RAPIDREACT2022Field-STEP.zip](https://firstfrc.blob.core.windows.net/frc2022/FieldAssets/RAPIDREACT2022Field-STEP.zip) |
| `EventOps/FRC_DriversMeetingForm.pdf` | 60 KB | [drivers-meeting-form.pdf](https://www.firstinspires.org/hubfs/web/program/frc/events/drivers-meeting-form.pdf) |
| `EventOps/2022_SingleDayEventPlan.pdf` | 239 KB | [2022-single-day-plan.pdf](https://firstfrc.blob.core.windows.net/frc2022/2022-single-day-plan.pdf) |

**Newly verified:**
- Team Update ceilings re-probed for all seasons 2019–2026 — no season exceeds TU22.
- The 2026 `REBUILT_TeamUpdateNN.pdf` naming confirmed against the live CDN (bare `TeamUpdate01.pdf` 404s for 2026, 200s for 2025); local copies byte-size-matched.
- Combined-PDF filename differs in all three of 2024 / 2025 / 2026.
- `frc-qa.firstinspires.org` is **still serving the 2026 corpus** and has not rolled to 2027; live DDP pull matches the archive exactly.
- No `frc2027` asset exists at any tried path, including a `BIOCORE_`-prefixed team update.
- No standalone Administrative/Event-Rules manual for 2017–2026 (probed both filename shapes, all seasons).
- No 2016 Q&A archive exists.
- All eleven manual quotes in §1.2 re-verified verbatim; page-citation dispute closed.
- All 433 local files re-validated by magic header.

**Corrected:** the "commanding version" quote is on **p. 10** (an earlier pass had moved it to p. 11 in the wrong direction). The precedence chain gained two layers previously unstated: the `frcparts@firstinspires.org` private ruling channel, and the acceptance-checklist distinction between *toleranced* and *actually-verified* field dimensions.
