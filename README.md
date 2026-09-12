# BIOCORE Analysis — FRC 2027 Research Workbench

Research workbench for **BIOCORE™ presented by Haas**, the *FIRST* Robotics Competition game of the **FIRST CANOPY** 2026-27 season. Everything here is **input to the deep manual review that runs on kickoff day**.

> **Kickoff / game reveal: Saturday, January 9, 2027, 12:00 p.m. ET.**
> **There is no FRC event on September 12, 2026.** That is the *FTC* BIOBUZZ kickoff: a different program, in the sibling project [`XrxcGH/BIOBUZZ-Analysis`](https://github.com/XrxcGH/BIOBUZZ-Analysis). The nearby FRC date is **September 24, 2026**, when Kit & Kickoff registration and Round 1 event preferencing open. Read [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) before anything else.

`[AUDIT 2026-08-22]` This README did not exist before the audit pass. Created as the entry point; see [`research/00_AUDIT.md`](research/00_AUDIT.md) for what was verified, fixed, and still missing.

`[AUDIT 2026-09-04]` **The workbench is finished for the pre-kickoff period and its next real
milestone is kickoff itself.** Every gap the 2026-08-22 pass left open that could be closed before a
manual exists has been closed: the scouting schema, the cycle and EV model, the Team Update differ,
and the end-to-end playbook dry run against two real manuals. What is left is genuinely blocked on
FIRST publishing something. Three dates own the remaining time, and none of them is a code task:
**2026-11-12** Pre-Kickoff Virtual Kit Release, **2026-11-21** order-by date for anything with a long
lead (re-run `reference/bom/recheck_prices.sh` first), **2027-01-09 12:00 ET** kickoff.

> ### → [`INDEX.md`](INDEX.md) — the full navigation map
>
> Every document in the project, one line each, grouped by track (Manual analysis · Strategy ranking ·
> Awards · BOM · Team ops · AI integration · Tools), with the key season dates, the FRC-vs-FTC firewall
> in brief, and a **"start here on kickoff day"** reading order. Start there if you are looking for a
> file rather than reading straight through.
>
> Correctness of everything it lists: [`reference/00_SYSTEM_AUDIT.md`](reference/00_SYSTEM_AUDIT.md)
> `[AUDIT 2026-08-22]` — all four core tools executed with real output pasted, every award name checked
> against the naming authority, every vendor URL curled, the rubric attacked with a purpose-built
> stress set (**back-test 27/30 = 90%**), and BOM rollups recomputed from the part lists.
>
> Re-run **2026-09-04**, recorded in that file's §10: every tool clean and unchanged, back-test still
> 27/30, **80 vendor URLs re-curled with 0 regressions**, `frc2027` still not staging. The re-run also
> corrected three things the original pass got wrong: its §0 re-run commands matched their own
> evidence, its URL count reported the live set as if it were the whole set, and the archive file
> counts below were stale within eight hours of being written.

---

## Read in this order

| # | File | Why |
|---|---|---|
| 1 | [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) | The FTC/FRC firewall. Pollen, StarterBots, and Skill Builders are **FTC BIOBUZZ**, not BIOCORE. |
| 2 | [`reference/FRC_VS_FTC_ORIENTATION.md`](reference/FRC_VS_FTC_ORIENTATION.md) | FRC structures with no FTC analogue: no bag day, district points, event weeks, double elimination, inspection flow, Q&A timing. |
| 3 | [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md) | **The operating document.** Phases 0–6, ready-to-paste prompts, kickoff-day clock. |
| 4 | [`research/03_biocore_official_intel.md`](research/03_biocore_official_intel.md) | Every published BIOCORE fact + 33 open questions the manual will answer. |
| 5 | [`research/04_biocore_community_intel.md`](research/04_biocore_community_intel.md) | Community intel and a falsifiable 10-item betting sheet to score against the manual. |
| 6 | [`research/02_supplemental_docs_index.md`](research/02_supplemental_docs_index.md) | Document precedence chain, kickoff-day URL fetch list, version-drift trap. |
| 7 | [`reference/QA-AMBIGUITY-HOTSPOTS.md`](reference/QA-AMBIGUITY-HOTSPOTS.md) | Which rules teams provably cannot parse, computed from 3 seasons of Q&A. |
| — | [`research/00_AUDIT.md`](research/00_AUDIT.md) | Audit trail: what is verified, what was wrong, what is still missing. |

---

## What is not in this repository

`[AUDIT 2026-09-12]` FIRST's game manuals, Q&A, Team Updates, award documents and web pages are
copyrighted, so this repository does not redistribute them or the text extracted from them. It keeps
what was derived from them: rule IDs with page and headline, counts, hashes, similarity scores,
crosswalks and churn statistics. The exact exclusion patterns are in [`.gitignore`](.gitignore).

| Artifact group | Why it is absent | What rebuilds it |
|---|---|---|
| FIRST source documents: `manuals/` (game manuals, Q&A exports, Team Updates, field drawings, CAD) and `reference/awards/pdfs/` (award and judging PDFs) | FIRST copyright. The set is also about 2.2 GB, and three files exceed GitHub's 100 MB limit | `bash tools/rebuild-corpus.sh --fetch` downloads the PDFs the analysis is built from |
| Text extracted from those documents: `**/_text/`, `manuals/archive/frc/_txt/`, full rule bodies in `research/rule_inventories/` (`*_rules_full.txt`, `*_bodies_v2.jsonl`, `_changes*_v2.md`, `<year>_violations.tsv`), and the text spans, full text, rule-body diff, glossary definitions, Violation clauses and raw manual lines under `reference/validation/*/` | Each is a full or per-rule verbatim copy of FIRST text | `bash tools/rebuild-corpus.sh` |
| Per-year rule dumps: `research/rule_inventories/<year>.json` | Each record carries the rule's full text | Nothing. No tool in the repository writes them; `tools/rules-full.py` builds `<year>_rules_full.txt` from `<year>_bodies_v2.jsonl` instead |
| Award web page snapshots: `reference/awards/_web/` | Raw text of FIRST web pages | `python reference/awards/fetch_award_pages.py` |
| Kickoff briefing packs: `review/*/BRIEFING_PACK.md` | Mostly verbatim manual text | `tools/RUN-KICKOFF.sh`, which writes a new pack on every run |
| Run state: `review/LATEST`, `review/*/.ingest_dir`, `research/teamupdate_analysis/.watch_state.json` | Records one machine's runs and paths | `tools/RUN-KICKOFF.sh` and `tools/teamupdate-diff.py --watch` write it on first use |
| `reference/awards/awards.yaml` and `reference/awards/01_AWARD_WINNING_PATTERNS.md` | Both quote FIRST's full award descriptions and guidelines, so they are held back until those quotes are cut to a sentence each | Nothing yet. The trimmed copies will be published at the same paths |

From the repository root, once per clone:

```bash
bash tools/rebuild-corpus.sh --fetch   # download the FIRST PDFs into manuals/ and reference/awards/pdfs/
bash tools/rebuild-corpus.sh           # regenerate the excluded text from the PDFs present; names any missing
```

`bash tools/rebuild-corpus.sh --help` lists the steps. The kickoff commands below, and every tool that
reads a FIRST manual or text extracted from one, expect these two commands to have run.

---

## Layout

```
INDEX.md                     navigation map for the whole project -- every doc, one line each
KICKOFF_PLAYBOOK.md          operating document for kickoff day
README.md                    this file
research/                    BIOCORE intel, rule inventories, TBA-derived analysis
  00_AUDIT.md                audit trail
  00_PREMISE_CORRECTION.md   FTC/FRC firewall — read first
  02/03/04_*.md              supplemental doc index, official intel, community intel
  rule_inventories/          2015–2026 structured rule corpus + churn/stability/Q&A-heat
  predictive_tba/            seed→win rates, score inflation, auto share
  awards_tba/                award migration and winner forensics
reference/                   durable, non-BIOCORE-specific reference
  00_SYSTEM_AUDIT.md         correctness audit: tools run, names checked, URLs curled, rubric attacked
  FRC_VS_FTC_ORIENTATION.md  FRC-only structures
  QA-AMBIGUITY-HOTSPOTS.md   empirical rule-ambiguity map
  team-ops/                  programming stack (Systemcore/WPILib 2027), business & awards
  awards/                    2026 award slate, judging guidelines, scoring analysis
  ai-integration/            FIRST AI policy, verified
tools/                       47 scripts (see INDEX.md Track 7)
manuals/                     FIRST source documents. Not tracked: holds only README files until you
                             run tools/rebuild-corpus.sh (see "What is not in this repository")
  archive/frc/               game manual PDFs, plus _txt/ extractions for 2022–2026
  archive/supplemental/      Team Updates, Q&A exports, inspection checklists, field drawings
  2026-27_BIOCORE/           ingest output lands here on kickoff day; see the README in that directory
logs/                        fetch and ingest logs
```

Match, ranking, alliance and award data under `research/predictive_tba/` and `research/awards_tba/`: Powered by [The Blue Alliance](https://www.thebluealliance.com).

---

## Kickoff day, in two commands

```bash
# Run from the repository root. On a fresh clone, run the corpus rebuild first
# (bash tools/rebuild-corpus.sh --fetch, then bash tools/rebuild-corpus.sh; see above).
# 1. Find + download the manual the moment it goes live:
bash tools/probe-2027-manual.sh --download
# 2. Ingest it:
bash tools/ingest-manual.sh "manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf" V1
```

`ingest-manual.sh` takes a **local PDF path**; it does not download anything. It was executed end to end on 2026-08-22 against a prior-season manual and works. Full Step 1 in [`KICKOFF_PLAYBOOK.md`](KICKOFF_PLAYBOOK.md).

`probe-2027-manual.sh` exists because **the FRC CDN has public container listing disabled** —
verified 2026-08-22: `GET /frc2026?restype=container&comp=list` returns 404 even though
`/frc2026/Manual/2026GameManual.pdf` returns 200. You cannot enumerate the container, so the
filename must be guessed, and FIRST has changed its shape (`<YEAR>FRCGameManual.pdf` in 2022–23 →
`<YEAR>GameManual.pdf` in 2024–26). The probe sweeps every known shape plus Team Updates, field
drawings, inspection checklist, and AprilTag layout. **Self-tested against 2026: found the manual
(4,939 KB) and the inspection checklist.** Against `frc2027` it correctly reports nothing live yet —
re-run 2026-09-04, every probe still 404.

`[AUDIT 2026-09-04]` **The shape list was reconciled with a second, independently written probe and
it was missing more than it knew.** The [Trellis suite](https://github.com/XrxcGH/Trellis) ships `tools/manual-probe.mjs` against the same
CDN; the two swept 42 name shapes between them and shared only 7. Merging them, and adding the shapes
recorded in this project's own `logs/fetch_*.log`, closed a real gap: **2026 moved the field drawings
and the AprilTag guide to kebab case** (`2026-field-dimension-dwgs.pdf`,
`2026-apriltag-images-user-guide.pdf`) and this probe was still asking for the 2024 and 2025 names.
Self-tested against 2026 after the merge: **11 live files, up from 2**, now including the field
drawings, the 35 MB field assembly manual, the AprilTag guide and the HTML edition of the manual.
Against `frc2027` it still correctly reports nothing. The reciprocal fix went the other way and is
written up in that suite's `docs/05-COMPANIONS.md` §4.2.

---

## Conventions

Every factual claim in this project carries a tag. Untagged claims are not trustworthy.

| Tag | Meaning |
|---|---|
| `[VERIFIED]` | Stated in a primary FIRST/vendor source, linked inline, or extracted from a local manual PDF with rule + page |
| `[COMPUTED]` | Derived by a script in `tools/` from data in this repo; reproducible |
| `[COMMUNITY]` / `[COMMUNITY-CONSENSUS]` | Stated publicly by a named, credible non-FIRST source; not authoritative |
| `[INFERENCE]` | Reasoning chained off verified facts |
| `[SPECULATION]` | Pattern-matching; flagged so it never contaminates the manual review |
| `[AUDIT 2026-08-22]` | Added or corrected by the audit pass |
| `[AUDIT 2026-09-04]` | Added or corrected by the re-run pass, which also corrects the audit |

**Anything in this project is a prior, not a fact about BIOCORE.** When the BIOCORE manual contradicts a file here, the manual wins and the file gets corrected.
