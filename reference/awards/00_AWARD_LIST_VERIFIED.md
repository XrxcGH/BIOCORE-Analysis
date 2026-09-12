# FRC Award List — VERIFIED for the 2026-27 BIOCORE season

**Purpose:** settle, with citations, exactly which awards FRC offers for **BIOCORE presented by Haas**,
under exactly which names, with which deadlines, which eligibility gates, and which of them a
~15-student team can actually win. Award names churned in **every** season 2022→2026 and the
individual-student award was **renamed mid-season in 2026**. Every downstream document in this project
cites this file for an award name; if this file is wrong, the whole ranking system is wrong.

**Companion file:** [`awards.yaml`](awards.yaml) — 25 award entries, machine-readable, one mapping per
award with all fields below. Re-verify script: [`kickoff_award_check.sh`](kickoff_award_check.sh).

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Verified in a primary source in this corpus |
| **[H]** HISTORICAL-PATTERN | Observed in prior-season FRC manuals/results; not stated for BIOCORE |
| **[S]** SPECULATION | Inference. Flagged as such. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked |

**Source shorthand**

`REB` = 2026 REBUILT manual (TU22, 166 pp) · `REEF` = 2025 REEFSCAPE (164 pp) ·
`CRES` = 2024 CRESCENDO (153 pp) · `CHRG` = 2023 CHARGED UP (142 pp) ·
`RAPD` = 2022 RAPID REACT (136 pp). All in `manuals/archive/frc/`; flat text in `manuals/archive/frc/_txt/`.
`TU12` = [2026 REBUILT Team Update 12, 2026-02-20](https://firstfrc.blob.core.windows.net/frc2026/Manual/TeamUpdates/REBUILT_TeamUpdate12.pdf), local copy `manuals/archive/supplemental/2026_TeamUpdates/TeamUpdate12.pdf`.
`JM` = [Judge Manual](https://www.firstinspires.org/hubfs/web/program/frc/awards/judge-manual.pdf) (Rev 2 · 2/18/2026) ·
`WB` = [Award Workbook](https://www.firstinspires.org/hubfs/web/program/frc/awards/award-workbook.pdf) (Rev. Oct 2025).
`WEB-M` = [Awards Based on Machine Attributes](https://www.firstinspires.org/resources/library/frc/machine-awards) ·
`WEB-T` = [Awards Based on Team Attributes](https://www.firstinspires.org/resources/library/frc/team-awards) ·
`WEB-S` = [Submitted Awards](https://www.firstinspires.org/resources/library/frc/submitted-awards) ·
`WEB-A` = [Awards (main)](https://www.firstinspires.org/robotics/frc/awards) ·
`WEB-E` = [FIRST Championship Eligibility](https://www.firstinspires.org/resources/library/frc/championship-eligibility).
Each of WEB-M / WEB-T / WEB-S states on its own face: *"This webpage is considered the authority."*
Local snapshots in `_web/`, PDFs in `pdfs/` with SHA-256 in `pdfs/MANIFEST.csv` (§8 says how to rebuild
the first two).
`TBA` = `research/awards_tba/tba_awards_{2022..2026}.csv` — 23,167 award rows over 1,057 year-event pairs.

---

## 0. Kickoff-day 60-second workflow

Runnable **today** (it defaults to the REBUILT manual so it is testable before BIOCORE exists) and on
**2027-01-09**. Swap in the BIOCORE manual path as `$1`. Tested end-to-end 2026-08-22 on Git Bash /
Windows; all five steps produced the output shown in §9.

```bash
# Run from the repository root.
cd reference/awards
M="../../manuals/archive/frc/2027_BIOCORE_GameManual.pdf"   # <- the file you download 2027-01-09

# 1. DID FIRST RENAME ANYTHING? live authority pages vs the locked baseline
python fetch_award_pages.py && python award_diff.py          # exit 0 == this document still valid

# 2. NEW AWARD NAMES IN THE MANUAL  <-- the money shot. empty output == no new awards.
pdftotext -layout "$M" - \
  | grep -oE "([A-Z][A-Za-z'\&.-]*[ ]){0,5}Award" \
  | sed 's/[[:space:]]\+/ /g; s/ $//; s/^\(The\|A\.\|An\) //' \
  | awk 'NF>1' | sort -u | grep -vxF -f known_awards_2026.txt

# 3. THE SLATE AT YOUR EVENT -- the playoff ceremony breaks list every award, in order
pdftotext -layout "$M" - | grep -oE "awards break:.*|^Awards: .*"

# 4. DEADLINES + YOUR RANKED TARGETS, straight out of awards.yaml
python - <<'PY'
import datetime, yaml
d = yaml.safe_load(open("awards.yaml", encoding="utf-8"))
for r in d["deadlines_2027"]:
    print(f"  [{r['evidence']}] {(r.get('award') or r.get('milestone')):42s} {r.get('closes') or r.get('date')}")
for r in d["small_team_ranked_targets"][:6]:
    print(f"  {r['rank']:2d}. {r['award']}\n      {r['why']}")
print("  days to kickoff:", (datetime.date(2027,1,9) - datetime.date.today()).days)
PY

# 5. THE RULE THAT DECIDES YOUR STRATEGY
#    JM: "Do not award the same team more than 1 judged award at a single event."
#    -> pick ONE lane per event, plus one backup. Do not spread yourself across five.
```

Or just: `bash reference/awards/kickoff_award_check.sh "$M"`.

**Step 2 is validated against five real seasons in §9.** Run against the 2025 manual it flags
`Dean's List Finalist Award`; against 2022 it flags `District Chairman's Award` — i.e. it catches
both of the real award renames of the last five years, with zero false positives on the other three.

---

## 1. What actually changed — the 2026 restructure, precisely

### 1.1 The headline: Dean's List → **FIRST Leadership Award** [C]

`TU12`, dated **2026-02-20**, verbatim:

> "Effective at FIRST events beginning February 18, the Dean's List Award will be known as the
> FIRST Leadership Award for the 2025-2026 season. The award's purpose, criteria, and significance
> remain unchanged. ... Historical records of recipients from previous seasons will not be updated
> at this time."

This is a **rename mid-season**, not a new award. It propagated to every tier of the award:

*Column split 2026-08-22: the old single "2026 count" column mixed event counts and row counts,
which is exactly the confusion that produced the retracted 192/2.08 figure in §2.1.*

| Retired 2026 name | Current name | rows in `TBA` | distinct events |
|---|---|---:|---:|
| `FIRST Dean's List Award` | `FIRST Leadership Award` | 10 | **1** (Championship, `2026cmptx`) |
| `FIRST Dean's List Finalist Award` | `FIRST Leadership Award Finalist` | 172 | **71** |
| `District Championship Dean's List Semi-Finalist` | `District Championship FIRST Leadership Award Semi-Finalist` | 218 | **120** |

**Any document in this project that says "Dean's List" is out of date.** The award is also now
cross-program: 10 FRC students **and** 10 FTC students are named Winners each year (`WEB-S`).

### 1.2 The full 5-season name-churn ledger [C]

Computed from `TBA` by set-differencing the standard slate (awards appearing at ≥15 events) year over year.

| Transition | Gone | New |
|---|---|---|
| 2022→2023 | Chairman's Award (Regional + District), Entrepreneurship Award | **FIRST Impact Award** (Regional + District), **Team Sustainability Award**, District Championship Dean's List Semi-Finalist |
| 2023→2024 | Autonomous Award **sponsored by Ford**, Highest Rookie Seed | Autonomous Award (unsponsored), Team Sustainability Award **sponsored by Dow** |
| 2024→2025 | Rookie Inspiration Award, Wildcard | **Rising All-Star Award**, Innovation in Control **sponsored by nVent**, Volunteer of the Year |
| 2025→2026 | All `Dean's List` names, Industrial Design **sponsored by General Motors** | All `FIRST Leadership Award` names, Industrial Design (unsponsored), Autonomous **sponsored by Google.org**, Excellence in Engineering **sponsored by Littelfuse**, Engineering Inspiration **sponsored by SpaceX** |

**A sponsor suffix moved on at least one award in every single season.** Never print a sponsor suffix
on a handout before the 2027 award pages are re-issued (§10).

### 1.3 What did **not** change, and what stayed retired [C]

- **No award was retired or added in the 2026 restructure.** The 2026 slate is the 2025 slate with
  one rename and four sponsor changes. The [2025 Season Award Updates for 2026](https://community.firstinspires.org/2025-season-award-updates-for-2026)
  community post describes guideline rewording and the Littelfuse sponsorship — **not** a structural change.
- **There is no Safety Award / Industrial Safety Award.** It appears **zero** times in the standard
  slate across all five seasons of `TBA`. The only surviving safety-linked award is the
  **Safety Animation Award sponsored by UL Solutions**, and `REB` §11.1.4 names it explicitly as an
  award "not judged at the event" that therefore earns **no District points**.
- Also still retired: Entrepreneurship, Rookie Inspiration, Highest Rookie Seed, Wildcard, Media and
  Technology Innovation. If any of these appears in the BIOCORE manual, that is news — §0 step 2 catches it.

---

## 2. The complete 2026-27 award list

25 entries. Counts are `TBA` 2026: **56 Regionals, 122 District events, 218 total indexed events,
median 18 award rows per event.**

> ### !! AVAILABILITY CORRECTION — 2026-08-22
>
> **This file is AUTHORITATIVE for availability** (events offered / per event). The companion
> [`00_AWARD_LIST_EMPIRICAL_2026.md`](00_AWARD_LIST_EMPIRICAL_2026.md) is authoritative for nothing
> but the raw TBA row counts it prints; where the two disagree, this file wins — **but only as of
> this correction**, because before it this file was the *wrong* one.
>
> **The defect.** The "Events offered 2026 / Per event" columns below were built by **summing an
> award with its Finalist and Semi-Finalist tiers**, then dividing total rows by the union of
> events. That is not availability. It is a blend of three different ballots.
>
> **Worst case — FIRST Leadership Award, row 16.** Published here as *"192 events, 2.08 per event —
> the highest availability on the board."* Recomputed from
> `research/awards_tba/tba_awards_2026.csv`, counting distinct events for the **exact** name:
>
> | exact award name | events | rows | per event |
> |---|---:|---:|---:|
> | `FIRST Leadership Award` (the award itself) | **1** (`2026cmptx`, Championship) | 10 | 10.00 |
> | `FIRST Leadership Award Finalist` | 71 | 172 | 2.42 |
> | `District Championship FIRST Leadership Award Semi-Finalist` | 120 | 218 | 1.82 |
> | *the discredited rollup* | *192* | *400* | *2.08* |
>
> The FIRST Leadership Award proper was given at **one event in the entire 2026 season**, not 192.
> A team that staffed a submission against "2.08 awards/event at 192 events" was reading a hit rate
> overstated by **192x on availability**. The winnable tier is the **Finalist** (71 events) — a
> different, correctly-named row. §2.1a is the corrected table; every `†` in §2.1 points into it.
>
> Reproduce with `python tools/award_availability.py`; assert with
> `python tools/award_availability.py --check reference/awards/00_AWARD_LIST_VERIFIED.md`.

### 2.1 Master table — names, sponsors, mechanism, advancement

| # | Award (exact current name) | Sponsor | Decided by | Pre-submission? | Advances to Champ? | Events offered 2026 | Per event |
|---:|---|---|---|---|---|---:|---:|
| 1 | Autonomous Award sponsored by Google.org | Google.org | Pit interview | No | No | 208 | 1.00 |
| 2 | Creativity Award sponsored by Rockwell Automation | Rockwell Automation | Pit interview | No | No | 208 | 1.00 |
| 3 | Excellence in Engineering Award sponsored by Littelfuse | Littelfuse | Pit interview | No | No | 208 | 1.00 |
| 4 | Industrial Design Award | — | Pit interview | No | No | 210 | 1.00 |
| 5 | Innovation in Control Award sponsored by nVent | nVent | Pit interview | No | No | 208 | 1.00 |
| 6 | Quality Award | — | Pit interview | No | No | 209 | 1.00 |
| 7 | Engineering Inspiration Award sponsored by SpaceX | SpaceX | Pit interview | **No** | **YES** | **56 Reg · 123 Dist · 15 DCMP · 8 Champ** `†2` | 1.00 · 1.00 · 1.47 · 1.00 |
| 8 | Gracious Professionalism Award | — | Pit interview | No | No | 211 | 1.00 |
| 9 | Imagery Award in honor of Jack Kamen | — (honoree) | Pit interview | No | No | 208 | 1.00 |
| 10 | Judges Award *(also printed "Judges' Award")* | — | Pit interview | No | No | 209 | 1.00 |
| 11 | Rising All-Star Award | — | Pit interview | No | No | 204 | 1.00 |
| 12 | Rookie All-Star Award *(TBA prints "Rookie All Star Award")* | — | Pit interview | No | **YES** | 133 `†6` | 1.00 |
| 13 | Team Spirit Award | — | Pit interview | No | No | 210 | 1.00 |
| 14 | Team Sustainability Award sponsored by Dow | Dow | Pit interview | No | No | 208 | 1.00 |
| 15 | **FIRST Impact Award** | — | Submission + 12-min interview | **YES — 2027-02-11** | **YES (strongest)** | **56 Reg · 122 Dist · 15 DCMP** `†3` | 1.00 · 1.00 · 2.00 |
| 16 | **FIRST Leadership Award** | — | Submission + interview | **YES — 2027-02-04** | Student only | **1 (Champ only)** · Finalist 71 · DCMP Semi 120 `†1` | 10.00 · 2.42 · 1.82 |
| 17 | **Woodie Flowers Finalist Award** | — | External panel, pre-event | **YES — 2027-02-04** | Mentor only | **71** `†4` | 1.11 |
| 18 | Woodie Flowers Award (Championship) | — | External panel | YES — 2027-02-04 | Championship only | 1 | 1.00 |
| 19 | Digital Animation Award sponsored by WPI | WPI | External panel (WPI faculty) | **YES — "Coming Soon"** | No | 0 (not event-judged) | — |
| 20 | Safety Animation Award sponsored by UL Solutions | UL Solutions | External panel | **YES — ~Oct/Nov 2026** | No | 0 (not event-judged) | — |
| 21 | Winner | — | Match play | No | YES at DCMP | **56 Reg · 123 Dist · 25 DCMP · 8 Champ** `†5` | 3.16 · 3.16 · 3.24 · 4.00 |
| 22 | Finalist | — | Match play | No | No | **56 Reg · 123 Dist · 25 DCMP · 8 Champ** `†5` | 3.30 · 3.15 · 3.28 · 4.00 |
| 23 | Volunteer of the Year Award *(TBA prints "Volunteer of the Year")* | — | Event planning committee | No | n/a | 12 | **1.08** `†7` |
| 24 | Founder's Award | — | FIRST HQ | No | n/a | **0 in TBA** `†8` | — |
| 25 | The Allaire Medal | — | Championship FIA team itself | No | n/a | **0 in TBA** `†8` | — |

`WEB-A` groups these into four categories plus two standalones, verbatim: *"Machine, Creativity, and
Innovation Awards, Team Attribute Awards, Submitted Awards, and Robot Performance Awards. The Founder's
Award and Volunteer of the Year Award stand alone."*

### 2.1a Availability, recomputed — **THE AUTHORITATIVE AVAILABILITY TABLE** [C]

*Added 2026-08-22 by the availability correction. Generated by `tools/award_availability.py` from
`research/awards_tba/tba_awards_2026.csv` (4,993 rows, 218 distinct events, 65 distinct award names).*

**Definition.** `availability(A)` = the number of **distinct events** at which a row whose award name
is **exactly** `A` appears. `per event` = rows ÷ those distinct events, i.e. how many recipients are
named where the award is given at all. **An award is never summed with its Finalist or Semi-Finalist
tier, and never with its Regional / District / District Championship siblings.** Those are separate
ballots decided by separate panels; adding them answers no question a team actually has.

Names below are TBA's exact strings, which differ in punctuation from FIRST's printed names
(`Judges' Award` vs FIRST's `Judges Award`; `Rookie All Star Award` vs `Rookie All-Star Award`).
Names appearing at 1–2 events are offseason events inventing their own vocabulary — noise, not slate.

| exact award name (TBA) | events | rows | per event |
|---|---:|---:|---:|
| `Gracious Professionalism Award` | 211 | 211 | 1.00 |
| `Industrial Design Award` | 210 | 210 | 1.00 |
| `Team Spirit Award` | 210 | 210 | 1.00 |
| `Judges' Award` | 209 | 209 | 1.00 |
| `Quality Award` | 209 | 209 | 1.00 |
| `Autonomous Award sponsored by Google.org` | 208 | 208 | 1.00 |
| `Creativity Award sponsored by Rockwell Automation` | 208 | 208 | 1.00 |
| `Excellence in Engineering Award sponsored by Littelfuse` | 208 | 208 | 1.00 |
| `Imagery Award in honor of Jack Kamen` | 208 | 208 | 1.00 |
| `Innovation in Control Award sponsored by nVent` | 208 | 208 | 1.00 |
| `Team Sustainability Award sponsored by Dow` | 208 | 208 | 1.00 |
| `Rising All-Star Award` | 204 | 204 | 1.00 |
| `Rookie All Star Award` | 133 | 133 | 1.00 |
| `District Engineering Inspiration Award sponsored by SpaceX` | 123 | 123 | 1.00 |
| `District Event Finalist` | 123 | 388 | 3.15 |
| `District Event Winner` | 123 | 389 | 3.16 |
| `District FIRST Impact Award` | 122 | 122 | 1.00 |
| `District Championship FIRST Leadership Award Semi-Finalist` | 120 | 218 | 1.82 |
| `FIRST Leadership Award Finalist` | 71 | 172 | 2.42 |
| `Woodie Flowers Finalist Award` | 71 | 79 | 1.11 |
| `Regional Engineering Inspiration Award sponsored by SpaceX` | 56 | 56 | 1.00 |
| `Regional FIRST Impact Award` | 56 | 56 | 1.00 |
| `Regional Finalists` | 56 | 185 | 3.30 |
| `Regional Winners` | 56 | 177 | 3.16 |
| `District Championship Finalist` | 25 | 82 | 3.28 |
| `District Championship Winner` | 25 | 81 | 3.24 |
| `District Championship Engineering Inspiration Award sponsored by SpaceX` | 15 | 22 | 1.47 |
| `District Championship FIRST Impact Award` | 15 | 30 | 2.00 |
| `District Championship Rookie All Star Award` | 14 | 17 | 1.21 |
| `Volunteer of the Year` | 12 | 13 | 1.08 |
| `Championship Division Finalist` | 8 | 32 | 4.00 |
| `Championship Division Winner` | 8 | 32 | 4.00 |
| `Engineering Inspiration Award sponsored by SpaceX` | 8 | 8 | 1.00 |
| `Finalist` | 4 | 13 | 3.25 |
| `Winner` | 4 | 12 | 3.00 |

*(31 further names appear at 1–2 events each — offseason custom awards plus the three Championship-only
rows `FIRST Leadership Award` (1 ev / 10 rows), `Woodie Flowers Award` (1 / 1) and `FIRST Impact Award`
(1 / 1). Run the script with no `--min-events` to see all 65.)*

#### The do-not-sum families, and the footnotes from §2.1

| `†` | Award family | Correct, per exact name | The rollup that was published, and why it is wrong |
|---|---|---|---|
| `†1` | FIRST Leadership Award | `FIRST Leadership Award` **1 ev / 10 rows**; `FIRST Leadership Award Finalist` **71 / 172**; `District Championship … Semi-Finalist` **120 / 218** | **192 ev @ 2.08** — summed the award with *both* subordinate tiers. Overstates the award's own availability **192x**. Target the **Finalist** tier (71 events); the award proper is Championship-only. |
| `†2` | Engineering Inspiration Award sponsored by SpaceX | Regional **56 / 56**; District **123 / 123**; DCMP **15 / 22**; Champ-division (unsponsored string) **8 / 8** | **204 ev @ 1.03** — summed four tiers. A Regional team's real availability is **56 events**, and it is one award per event, not 1.03. |
| `†3` | FIRST Impact Award | Regional **56 / 56**; District **122 / 122**; DCMP **15 / 30** | **194 ev @ 1.11** — summed three tiers (nearest the 193 / 1.08 the data actually rolls up to). No single team is eligible at 194 events. |
| `†4` | Woodie Flowers Finalist Award | `Woodie Flowers Finalist Award` **71 ev / 79 rows** = 1.11 | **72 ev** — off by one: the Championship `Woodie Flowers Award` (1 event) was folded in. Small error, same mechanism. |
| `†5` | Winner / Finalist | Winner: Reg **56 / 177**, Dist **123 / 389**, DCMP **25 / 81**, Champ-div **8 / 32**. Finalist: Reg **56 / 185**, Dist **123 / 388**, DCMP **25 / 82**, Champ-div **8 / 32** | **204 ev @ 3.17 / 3.21** — a tier sum. Defensible as "some form of this award exists at 204 events," but it was not labelled as one, and the bare names `Winner`/`Finalist` are offseason strings appearing at 4 events each. |
| `†6` | Rookie All Star Award | **133 / 133**. `District Championship Rookie All Star Award` is a *separate* **14 / 17** | **No error** — 133 was already the exact-name count. Audited and confirmed clean. |
| `†7` | Volunteer of the Year | **12 ev / 13 rows** = **1.08** | Per-event was printed as 1.00; one event named two. Cosmetic. |
| `†8` | Founder's Award · The Allaire Medal | **Absent from TBA 2026 entirely** — 0 rows under any name | Printed as `1` and `Champ`. Both are HQ-conferred and not event-indexed; the `1` was an assumption, not a count. Availability for a competing team is **not applicable**, not 1. |

#### What survived the audit unchanged

Rows **1–6, 8–11, 13, 14** (Autonomous, Creativity, Excellence in Engineering, Industrial Design,
Innovation in Control, Quality, Gracious Professionalism, Imagery, Judges, Rising All-Star, Team
Spirit, Team Sustainability) are all **1 row = 1 event, exactly one exact name, per event 1.00**.
They have no Finalist tier and no Regional/District split, so the summing defect could not reach them.
Rows **19, 20** (Digital Animation, Safety Animation) are correctly `0` — verified absent from the CSV.
**These twelve availability figures are the only ones in §2.1 that were right the first time.**


### 2.2 What the published criteria actually say — machine awards [C] `WEB-M`

| Award | Description (verbatim) | The guideline sentence that decides it (verbatim) |
|---|---|---|
| **Autonomous** | "Celebrates the team whose machine has demonstrated consistent, reliable, high-performance robot operation during autonomous (i.e. non-operated guided) actions during match play." | "**Consistent and reliable operation is weighted more heavily than the ability to score maximum points** during any specific autonomously managed actions." |
| **Creativity** | "Celebrates a creative robotic component, concept, or attribute that enhances strategy of play that was **intentionally designed and not discovered**." | "Since creativity may involve risk of failure, the team should be able to **describe how they mitigated that risk**." |
| **Excellence in Engineering** | "Celebrates the team whose machine incorporates an engineering solution designed to have components work together seamlessly." | "**Teams do not have to design a robot that solves all game challenges.**" |
| **Industrial Design** | "Celebrates the team whose machine demonstrates industrial design principles, striking a balance between form, function, and aesthetics." | "**The entire machine**, and not just a single component, or the detailed process used to develop the design, is worthy of this recognition." |
| **Innovation in Control** | "Celebrates an innovative control system or application of control components – electrical, mechanical or software – to provide unique machine functions." | "The innovation is practical; it addresses the game's challenge and is **reliable under the stress of competition**." |
| **Quality** | "Celebrates machine robustness in concept and fabrication" | "A team must be able to describe **their quality plan** i.e. how their design ensures robustness throughout the entire competition." |

### 2.3 What the published criteria actually say — team attribute awards [C] `WEB-T`

| Award | Description (verbatim) | The guideline sentence that decides it (verbatim) |
|---|---|---|
| **Engineering Inspiration** | "Celebrates a team who demonstrates outstanding success in advancing respect and appreciation for engineering within a team's school or organization and community." | "...with **performance indicators that provide measurable success** of their efforts ... Efforts are ongoing, not strictly concentrated on the build and competition season." |
| **Gracious Professionalism** | "Celebrates outstanding demonstration of FIRST Core Values such as continuous Gracious Professionalism, sportsmanship, and working together both on and off the playing field." | "**If the team worked with another FIRST Robotics Competition team pre-season** - they can describe the following: How the collaboration was conducted ... The financial impacts of working together vs working independently." |
| **Imagery** | "Celebrates attractiveness in engineering and outstanding visual aesthetic integration of machine and team appearance." | "The team must be able to **describe its theme and its origins**. The theme is incorporated into all aspects of the team, i.e. uniforms, pits, machine, mascot, etc." |
| **Judges** | "During the course of the competition, the judging panel may decide a team's unique efforts, performance, or dynamics merit recognition." | "The team exemplifies a positive attribute or feature that is **not addressed in the criteria for other awards**." |
| **Rising All-Star** | "Celebrates the team that has persisted through challenges, despite the difficulties of being young. This could be the result of being a new team, or a team with **recent turnover in membership**." | "**Teams do not have to be in their first year.** ... the award could recognize a team in their second or third year who has undergone significant growth or succeeded despite challenges." |
| **Rookie All-Star** | "Celebrates the rookie team exemplifying a young but strong partnership effort..." | `JM`: "Building a robot that is appropriate to the game's challenges means '**did they build a robot or not**'. ... How good the robot is compared to other rookie teams at the event is irrelevant." |
| **Team Spirit** | "Celebrates extraordinary enthusiasm and spirit through exceptional partnership and teamwork furthering the objectives of FIRST." | "They demonstrate spirit **as a unified team**." |
| **Team Sustainability** | "Celebrates a team which has developed sustainable practices that focus on a 'triple bottom line' (i.e. People, Prosperity, and Planet)..." | "The team must be able to explain their plans and actions associated with **one or more** of the following sustainability initiatives" |

Full guideline text for all 14 is on the `WEB-M` and `WEB-T` pages linked above.

---

## 3. The four classes, separated

### 3.1 (a) Awards requiring a WRITTEN SUBMISSION with a deadline — 6

| Award | Submitter | Portal | Artifacts required | Closes |
|---|---|---|---|---|
| **FIRST Impact Award** | Student Award Submitter **or** Lead Coach 1/2 | FIRST Dashboard | 14 executive summaries @500 char (last optional @250) · essay @10,000 char · **optional** video URL (16:9, 1–3 min, Dropbox/Box/Google Drive, public) · **optional** Documentation Form · **required** Video Consent & Release agreement | **2027-02-11 15:00 ET** [C] |
| **FIRST Leadership Award** | **Adult** Award Submitter or Lead Coach 1/2, **not related** to either nominee | FIRST Dashboard | up to 2 student nominations + essay each · signed FIRST Consent & Release per nominee (or mentor checks the paper-copy box) | **2027-02-04 15:00 ET** [C] |
| **Woodie Flowers Award** (→ WFFA) | **Student** Award Submitter — "this must be a student-led effort" | FIRST Dashboard | essay @3,000 char in English · 1 required mentor headshot + up to 3 photos, ≤1.0 MB total · 2 adult references | **2027-02-04 15:00 ET** [C] |
| Woodie Flowers Award (Championship re-nomination) | Student Award Submitter | FIRST Dashboard | a **new** stand-alone 3,000-char essay — "previous essay are not considered" | 2027-02-04 15:00 ET [C] |
| **Digital Animation Award** | Any Adult Mentor | **WPI web form**, not the Dashboard | ≤30 s animation on YouTube/similar, public · 2 s title + 1 s slate before, 1 s slate + ≤5 s credits after (39 s total max) · title screen naming program, team #, team name, org, title, duration | **"Coming Soon"** [C] — 2026 season was 2026-01-12 23:59 ET [H] |
| **Safety Animation Award** | Student Award Submitter or Lead Coach 1/2 | FIRST Dashboard | ≤40 s animation **including** opening and credits, as .AVI/.MPEG/.MP4/.WMV | **not yet published** — 2026 season was 2025-10-13 12:00 → 2025-11-20 15:00 ET [H] |

All three Dashboard awards **open Thursday 2026-10-29 at 12:00 ET** [C] `WEB-S`.

### 3.2 (b) Awards judged from pit/robot interviews with NO pre-submission — 14

Awards **1–14** in §2.1. There is nothing to file, no portal, no deadline. Judges walk to your pit.
`WB`: *"Judges should make a concerted effort to conduct the interview while the robot and
spokespersons are in the team's pit."*

Two of these carry advancement consequences despite requiring no paperwork:
**Engineering Inspiration** and **Rookie All-Star** are Cultural Awards (§5). Engineering Inspiration
is the single highest-value award in FRC that costs a team **zero** pre-season writing.

### 3.3 (c) Awards for individuals — 4

| Award | Who it is for | Selected by | Note |
|---|---|---|---|
| **FIRST Leadership Award** | Students in their **10th or 11th school year only** | Judges, from submission + interview | 4 tiers: Semi-finalist (2 per team) → DCMP Semi-finalist → Finalist (2 per Regional; per-District ratio 1 per 9 to 1 per 6 Championship District teams) → **Winner (10 FRC + 10 FTC)** |
| **Woodie Flowers Finalist Award** | A registered, actively-mentoring **mentor** | External panel of past Championship WFA winners, **before the event**. `JM` lists it under "Non-Judged Awards" | "A mentor may only receive the WFFA **one time** regardless of the number of teams the mentor has served" |
| **Woodie Flowers Award** | A mentor who already holds a WFFA | Same panel, at Championship | Requires re-nomination by the mentor's present team |
| **The Allaire Medal** | One student on the **Championship FIRST Impact Award team** | Chosen by that team itself | Up to $10,000 undergraduate scholarship. Must be a junior/senior accepted to a 4-year program |

**"Dean's List" no longer exists as a name.** See §1.1.

### 3.4 (d) Objective / performance awards — 2 (+3 non-team)

- **Winner** — "celebrates the Alliance that wins the competition." 3.17 recipients per event.
- **Finalist** — "celebrates the Alliance that makes it to the final match." 3.21 per event.
- `JM` lists both under **Non-Judged Awards**: "Finalists and Winners (determined via matches)",
  alongside the WFFA (external panel) and Volunteer of the Year (planning committee, pre-event).
- Not team-competable at all: **Volunteer of the Year Award**, **Founder's Award**, **Allaire Medal**.

---

## 4. 2027 deadline calendar

FIRST has **already published** the 2027-season dates for the three Dashboard awards [C] `WEB-S`
(confirmed against the live page 2026-08-22; all four dates fall on a Thursday, consistent with
FIRST's pattern).

| Date | Award / milestone | Evidence |
|---|---|---|
| **~2026-10-13** (est.) | Safety Animation Award submission **opens** | **[H]** — 2026 season opened 2025-10-13 12:00 ET |
| **2026-10-29 12:00 ET** | FIRST Impact / FIRST Leadership / Woodie Flowers submissions **open** | **[C]** |
| **~2026-11-20** (est.) | Safety Animation Award submission **closes** | **[H]** — 2026 season closed 2025-11-20 15:00 ET |
| **2027-01-09 12:00 ET** | **BIOCORE kickoff** | **[C]** |
| **~2027-01-11** (est.) | Digital Animation Award closes | **[H]** — 2026 season closed 2026-01-12 23:59 ET; page currently reads "Coming Soon" |
| **2027-02-04 15:00 ET** | **FIRST Leadership Award closes** | **[C]** |
| **2027-02-04 15:00 ET** | **Woodie Flowers Award closes** | **[C]** |
| **~2027-02-08** (est.) | FIRST Leadership judge portal opens | **[H]** — was 2026-02-09 |
| **2027-02-11 15:00 ET** | **FIRST Impact Award closes** | **[C]** |
| **~2027-02-15** (est.) | FIRST Impact judge portal opens | **[H]** — was 2026-02-16 |

> **The single most time-critical fact in this document.** The **Safety Animation Award** window for the
> 2027 season most likely opens **mid-October 2026** — roughly **8 weeks from today** and **11 weeks
> before kickoff**. It requires 40 seconds of animation, no robot, and pays **$500 to the winner and
> $250 to each of two Finalists** against next season's registration. For a small, under-funded team
> that is the highest return-per-hour item on the entire award calendar, and it is gone before the
> game is even revealed. **Watch [the safety page](https://www.firstinspires.org/resources/library/safety)
> weekly from 2026-09-01.**

Two deadlines land **before or barely after kickoff**: Safety Animation (~Nov 2026) and Digital
Animation (~Jan 2027). Everything you can win on those is decided in the autumn, not in build season.

---

## 5. Which awards advance you [C] `WEB-E`, `REB` §11

### 5.1 The Cultural Awards — the only judged awards with advancement power

`JM`: *"Cultural Awards are the awards that have the most impact on the community and may qualify the
team to move on to the District Championship or FIRST Championship. The three Cultural Awards are the
FIRST Impact Award (FIA), Engineering Inspiration (EI), and Rookie All Star (RAS)."*

| Award | District event win → | District Championship win → | Regional win → |
|---|---|---|---|
| **FIRST Impact** | qualifies for DCMP | **Championship slot** + Hall of Fame path | Championship consideration; **remote interview offered** if not otherwise qualified |
| **Engineering Inspiration** | qualifies for DCMP *(award only)* | **Championship slot** | competes for the award at Championship |
| **Rookie All-Star** | qualifies for DCMP *(award only)* | **Championship slot** | competes for the award at Championship |

`JM`: *"Once a team has won a cultural award, they may not win that award again at the same level of
competition."* District teams are **not eligible** for any Cultural Award at Regional or inter-district
events.

### 5.2 District points [C] `REB` §11.1.4 / Table 11-2

| Award class | Points |
|---|---:|
| FIRST Impact Award | **10** |
| Engineering Inspiration, Rookie All Star | **8** each |
| All other **team-judged** awards | **5** each |
| FIRST Leadership Award, Safety Animation Award, WFFA, Volunteer of the Year | **0** |

`REB` verbatim: *"If an award is not judged, is not for a team (e.g. the FIRST Leadership Award) or is
not judged at the event (e.g. Safety Animation Award, sponsored by UL), no points are earned."*
DCMP points are ×3. Regional-model teams earn Championship slots via the points-based **Regional Pool**
(top-ranked teams from their first two Regionals), not by any single award; each US Regional advances 3
teams, each international Regional 4.

---

## 6. Four judging mechanics that decide your strategy [C] `JM`

1. **One judged award per team per event.** Verbatim: *"Do not award the same team more than 1 judged
   award at a single event."* Chasing five lanes does not multiply your odds — it splits one pitch five
   ways. **Pick one primary lane per event and one backup.** This is the single most consequential line
   in the entire award corpus for a small team.
2. **"Spread the wealth" applies within an event, not between events.** *"judges should not use the
   fact that a team won award X at an earlier event to exclude them from award X at the current event."*
   Winning Team Spirit at event 1 does **not** block Team Spirit at event 2. Repeat the same lane.
3. **Judged awards and field awards are independent.** *"Do not allow the possibility of a team winning
   the event to affect a decision on a judged award."* Making finals costs you nothing in the judge room.
4. **AI use is explicitly permitted, with attribution.** `WEB-S`: *"Teams are permitted to use
   Artificial Intelligence (AI) to assist in the creation of award submissions... Proper Credit can
   look like this: Essay created by Team XXXX and ChatGPT."* And: *"Judges should not discredit a team
   who uses AI or rank them lower simply for using the tool."* Cross-reference
   [`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md).

**The ceremony order tells you the slate** [C] `REB` §10.6.2 Table 10-2 — five breaks in the playoff
schedule, each naming its awards:

```
break 1: Imagery, Gracious Professionalism, Team Spirit, and Rising All Star
break 2: Autonomous, Creativity, Quality, and Industrial Design
break 3: Innovation in Control, Excellence in Engineering, Team Sustainability, Judges
break 4: Rookie All Star, FIRST Leadership Award, Engineering Inspiration**
final  : Remaining awards, Finalists, Winners, and FIRST Impact Award
   ** Program Delivery Partners may choose to hold these awards until after all MATCHES are complete.
```

---

## 7. What a ~15-student team can actually win

All percentages recomputed 2026-08-22 directly from `TBA` (23,167 rows, 1,057 year-event pairs).
Names canonicalised across seasons before aggregation: Chairman's → FIRST Impact; Rookie Inspiration →
Rising All-Star; Entrepreneurship → Team Sustainability; sponsor suffixes stripped. **"top-8"** = TBA
`qual_rank` ≤ 8. **"bottom half"** = `rank_pct` > 50. Sorted by bottom-half winner share — i.e. by how
often a team that is *not* good on the field wins it anyway.

| Award | Wins 22-26 | % events offered | **% winners from bottom half** | Median winner rank pct | Distinct winners | % wins by repeat winners | Median winning team # |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Rising All-Star** | 778 | 73.6 | **69.1** | 67.5 | 613 | 37.9 | 9158 |
| Rookie All-Star | 680 | 62.8 | 68.4 | 66.7 | 574 | 29.1 | 9691 |
| **Team Spirit** | 944 | 89.3 | **51.9** | 53.5 | 677 | 46.5 | 4855 |
| **Judges** | 953 | 90.2 | **49.6** | 50.0 | **787** | **31.5** | 5012 |
| **Imagery** | 936 | 88.6 | **47.7** | 48.7 | 577 | 59.0 | 4957 |
| **Team Sustainability** | 939 | 88.8 | **43.7** | 44.0 | 621 | 56.0 | 3880 |
| **Gracious Professionalism** | 951 | 90.0 | **41.2** | 43.6 | 661 | 49.8 | 4061 |
| Engineering Inspiration | 948 | 86.6 | 31.1 | 33.3 | 556 | 66.1 | 3558 |
| **Creativity** | 938 | 88.7 | **28.1** | 31.8 | **706** | **42.5** | 4146 |
| FIRST Impact | 970 | 83.0 | 27.0 | 27.8 | 446 | **77.7** | 3347 |
| Quality | 946 | 89.5 | 12.2 | 18.2 | 649 | 52.2 | 3494 |
| Industrial Design | 937 | 88.6 | 11.9 | 17.5 | 604 | 56.1 | 3602 |
| Excellence in Engineering | 944 | 89.3 | 11.4 | 15.5 | 572 | 60.1 | 3419 |
| Innovation in Control | 943 | 89.2 | 10.4 | 17.6 | 612 | 55.5 | 3472 |
| Autonomous | 939 | 88.8 | **4.9** | 9.0 | 536 | 64.2 | 3255 |

### 7.1 Realistically winnable — chase these

| Rank | Award | Why, in one line |
|---:|---|---|
| 1 | **Rising All-Star Award** | 69.1% of winners come from the bottom half; the only award whose *median* winner sits in the bottom third. Offered at 204/211 events. Eligibility explicitly covers "recent turnover in membership", **not just year one**. |
| 2 | **FIRST Leadership Award — Finalist tier** | Judged on **one student**, not on a robot, a budget or a 3-year record. **[AVAILABILITY 2026-08-22]** The reachable prize is the **Finalist**: 172 named at **71 events** (2.42 where offered). `District Championship … Semi-Finalist`: 218 at **120 events**. The **award itself** was given at **1 event** (Championship, 10 FRC students) — do not plan against it. See §2.1a. Costs one mentor essay. |
| 3 | **Judges Award** | 787 distinct winners — more than any FRC award — and the lowest repeat concentration (31.5%). Criteria literally reward "a positive attribute ... not addressed in the criteria for other awards". |
| 4 | **Team Spirit Award** | 51.9% bottom-half. Criteria demand spirit "as a unified team", which is *easier* at 15 students than at 60. |
| 5 | **Woodie Flowers Finalist Award** | A 3,000-char student essay about your mentor, judged off-site before the event. Robot, budget and headcount are irrelevant. You have an experienced mentor — this is the highest-dignity cheap win available. |
| 6 | **Imagery Award** | 47.7% bottom-half. A theme with a written origin story costs intent, not money. |
| 7 | **Safety Animation Award** | 40 s of animation, cash prize, no robot — but the window closes ~Nov 2026, before kickoff. |
| 8 | **Team Sustainability Award** | "**one or more** of the following" lets you answer on People alone. For a 15-student team, succession *is* the sustainability story. |
| 9 | **Gracious Professionalism Award** | 41.2% bottom-half, and the pre-season-collaboration bullet is a checklist you can deliberately satisfy by partnering with one team before January. |
| 10 | **Creativity Award** | The only machine award a low-seed wins 28.1% of the time, with the lowest repeat concentration (42.5%) of any machine award. **This is the one robot-design award worth aiming a mechanism at.** |
| 11 | **Winner / Finalist** | Reachable via **alliance selection**, not seeding. Be the best 8th-to-24th pick in the room: reliable, fast to repair, useful on defense. |

### 7.2 Effectively requires a large sustained program — do not spend the season on these

| Award | The disqualifying number or clause |
|---|---|
| **FIRST Impact Award** | **77.7% of wins go to repeat winners**; only 446 distinct teams in five seasons — the most concentrated award in FRC. Criteria require "special emphasis on recent accomplishments within the last 3 years" and "activities over a sustained period". A program without a 3-year outreach record is structurally excluded. *(The FIA Judging Guidelines do instruct judges to "Consider utilization of team resources, especially when comparing large teams vs small teams" — real, but not enough to close a 3-year gap.)* |
| **Autonomous Award** | **80.4% of winners were qual top-8; only 4.9% from the bottom half.** The most performance-coupled judged award in FRC. |
| Excellence in Engineering / Industrial Design / Innovation in Control / Quality | 10–12% bottom-half winners each. Winnable in principle, dominated in practice by build resources. Excellence in Engineering says "Teams do not have to design a robot that solves all game challenges" — but 62.5% of its winners were still top-8 seeds. |
| **Engineering Inspiration** | 66.1% repeat winners. Better odds than FIA (31.1% bottom-half) and needs **no written submission** — the best "reach" target if outreach is already real. Otherwise a multi-year build. |
| **Rookie All-Star** | Hard gate: rookie teams only, `JM` "team number 10,900 or higher". Not a lane unless you are a rookie. **Rising All-Star is the substitute and has no rookie gate.** |
| Woodie Flowers Award (Championship) / Founder's / Volunteer of the Year / Allaire Medal | Gated on a prior WFFA, or not team-competable at all. |

### 7.3 The strategic consequence

Because **only one judged award per team per event** is allowed (§6.1), the ranking system downstream of
this file should output **one primary and one backup lane per event**, not a wishlist. On the evidence
above the default pairing for this team is **Rising All-Star (primary) + Judges Award (backup)** at
event 1, with **Team Spirit** or **Imagery** substituted at event 2 — and **FIRST Leadership Award +
Woodie Flowers Finalist Award** running in parallel all season, because neither is a "judged award at the
event" and neither is blocked by the one-award rule.

---

## 8. Rubrics and guides downloaded

All in [`pdfs/`](pdfs/), SHA-256 and fetch date in [`pdfs/MANIFEST.csv`](pdfs/MANIFEST.csv); plain-text
extractions in [`_text/`](_text/). Fetched/verified 2026-08-22. The PDFs and extractions are not in the
repository, because FIRST's text is not redistributed: from the repository root,
`bash tools/rebuild-corpus.sh --fetch` downloads the PDFs and `bash tools/rebuild-corpus.sh` rebuilds
`_text/`, while §0 step 1 (`python fetch_award_pages.py`) recreates the `_web/` snapshots.

| File | Source URL | Bytes | Internal revision |
|---|---|---:|---|
| `judge-manual.pdf` | `firstinspires.org/hubfs/web/program/frc/awards/judge-manual.pdf` | 1,079,671 | **Rev 2 · 2/18/2026** |
| `award-workbook.pdf` | `.../awards/award-workbook.pdf` | 293,066 | **Rev. Oct 2025** |
| `first-leadership-award-guide.pdf` | `.../awards/fla-guide.pdf` | 878,748 | 17 pp |
| `first-leadership-award-judging-guidelines.pdf` | `.../awards/dla-judging-guidelines.pdf` | 275,155 | **Rev. Feb 2026** |
| `fia-judging-guidelines.pdf` | `.../awards/fia-judging-guidelines.pdf` | 284,654 | **Rev. Jan 2026** |
| `fia-definitions.pdf` | `.../awards/fia-definitions.pdf` | 197,026 | "updated for 2026 season" |
| `fia-documentation-form.pdf` | `.../awards/fia-documentation-form.pdf` | 236,265 | — |
| `fia-video-consent.pdf` | `.../awards/fia-video-consent.pdf` | 103,752 | — |
| `best-practices-for-teams.pdf` | `.../awards/best-practices-for-teams.pdf` | 252,417 | — |
| `technical-judging-tips.pdf` | `.../awards/technical-judging-tips.pdf` | 220,455 | — |
| `inside-look-at-judging-process.pdf` | `.../awards/inside-look-at-judging-process.pdf` | 241,669 | — |
| `sibling-teams-guidelines.pdf` | `.../reg/sibling-teams-guidelines.pdf` | 194,051 | — |

**URL-equivalence check performed.** The task-supplied
`info.firstinspires.org/hubfs/web/program/frc/awards/first-leadership-award-guide.pdf` and
`www.firstinspires.org/hubfs/web/program/frc/awards/fla-guide.pdf` return the **byte-identical** file —
SHA-256 `d57a6b9b035b52febd2c6443425ef2e857bf8e804d4f75688ce6b5e5ff6daedb`, 878,748 bytes. Note that
FIRST still serves the FIRST Leadership Award judging guidelines from the **legacy path
`dla-judging-guidelines.pdf`** ("dla" = Dean's List Award) — the URL was never renamed. Do not read that
filename as evidence the Dean's List still exists.

**Not obtained.** The FIRST Safety Manual: three candidate hubfs paths all returned HTTP 404 on
2026-08-22 and no working direct PDF URL was found. **UNVERIFIED.** It is not an award-criteria document
— there is no Safety Award (§1.3) — so nothing in this file depends on it.

**No judging *rubric* with numeric weights exists for the 14 pit-judged awards.** `JM` is explicit:
*"The guidelines for all awards should not be viewed as strict criteria that should be met to win any
award. Rather, FIRST asks that judges use these guidelines as a framework in deliberations."* The only
scored rubric FIRST publishes is the Digital Animation Award's (WPI, 4 categories, 30 points for
"Connection to the Theme"). Any system that claims to score a team against a numeric FRC judging rubric
is inventing it.

---

## 9. Validation — dry run against five past seasons

The instrument in §0 was back-tested against the 2022–2026 manuals in this corpus. **The test is
honest because the stoplist `known_awards_2026.txt` was built from the 2026 slate only — running it
against an older manual simulates kickoff day with a season's worth of drift.**

### 9.1 §0 step 2 — new-award detection

| Manual | Output | Correct? |
|---|---|---|
| `RAPD` 2022 RAPID REACT | `District Chairman's Award` | **TRUE POSITIVE** — Chairman's was renamed to FIRST Impact for 2023 |
| `CHRG` 2023 CHARGED UP | *(clean)* | correct — 2023 names match the 2026 baseline |
| `CRES` 2024 CRESCENDO | *(clean)* | correct |
| `REEF` 2025 REEFSCAPE | `Dean's List Finalist Award` | **TRUE POSITIVE** — renamed to FIRST Leadership Award for 2026 |
| `REB` 2026 REBUILT | *(clean)* | correct — this is the baseline |

**2 true positives, 0 false positives, 0 false negatives across five seasons.** The instrument catches
both real award renames of the last five years — including the exact 2026 restructure this document
is about — and stays silent otherwise.

Getting there required two rounds of tightening, both recorded in `known_awards_2026.txt`:
the naive regex `[A-Z][A-Za-z'&-]*( [A-Za-z'&-]+){0,5} Award` emitted 11 sentence-fragment false
positives on `REB` ("At the Award", "For the FIRST Impact Award", "District teams to one FIRST Impact
Award"). Requiring **every** word to be capitalised, stripping leading `The`/`A.`/`An`, and dropping
1-word matches cut that to 4; adding a Tier-6 block of level-prefixed forms
(`District FIRST Impact Award`, `FIRST Leadership Award Finalist`, …) and the line-wrap fragment
`Inspiration Award` cut it to 0.

### 9.2 §0 step 3 — ceremony-slate extraction

| Manual | break 1 tail | break 4 middle |
|---|---|---|
| `CRES` 2024 | "...and **Rookie**" *(Rookie Inspiration)* | "Rookie All Star, **Dean's List**, Engineering Inspiration" |
| `REEF` 2025 | "...and **Rising All**" *(Rising All-Star)* | "Rookie All Star, **Dean's List**, Engineering Inspiration" |
| `REB` 2026 | "...and **Rising All Star**" | "Rookie All Star, **FIRST Leadership Award**, Engineering Inspiration" |

The ceremony lines independently reproduce **both** transitions — Rookie Inspiration → Rising All-Star
(2024→2025) and Dean's List → FIRST Leadership Award (2025→2026) — from a completely different part of
the manual than step 2 reads. Two independent channels agreeing is why this document trusts them.
`RAPD` 2022 and `CHRG` 2023 produce **no** output: the "awards break:" line only entered the playoff
schedule table in 2024. **Step 3 is therefore only valid for 2024-and-later manual formats** — if it
returns nothing on 2027-01-09, the table format changed, not the awards.

### 9.3 §0 step 1 — live-page drift detection

`python award_diff.py` run 2026-08-22 against freshly fetched pages: `baseline=23 live=23 — no change`.
The extractor pairs each award name with the literal "Updated"/"Updates" line that follows it in FIRST's
accordion markup, cross-checked against the flat "All Awards" list. Exit 0 = this document is still
accurate; exit 1 = something moved and §2 must be re-verified before use.

### 9.4 Full-workflow run, 2026-08-22

All five steps executed end-to-end against `REB` as the stand-in manual. Steps 1–3 produced the results
above; step 4 printed the six deadlines, the top-6 ranked targets and "days to kickoff: 140"; step 5
printed the one-award-per-event rule. **The workflow runs.**

---

## 10. Discrepancies and the 2027 watch list

### 10.1 Live contradictions inside FIRST's own documents [C]

| # | Conflict | Resolution |
|---|---|---|
| 1 | **Autonomous Award sponsor.** `JM` p.12 prints "sponsored by **Google DeepMind**". `WEB-M`, `WEB-A` and all 208 `TBA` 2026 event records say "sponsored by **Google.org**". | Use **Google.org**. The webpage self-declares as the authority and the event records agree with it. Re-check at kickoff. |
| 2 | **Judges Award apostrophe.** `WEB-T` and `JM` write "**Judges Award**". `WEB-A`'s All Awards list and every `TBA` 2026 record write "**Judges' Award**". | Both are FIRST's. Use "Judges Award"; match either when parsing. |
| 3 | **Rookie All-Star hyphen.** `WEB-T` writes "Rookie All-**S**tar Award"; `TBA` and `REB`'s ceremony line write "Rookie All Star Award". | Cosmetic. Both are in the stoplist. |
| 4 | **Digital Animation Award sponsor string** renders as "Digital Animation Award **s ponsored by** Worcester Polytechnic Institute" — a stray space in FIRST's own HTML. | Preserved verbatim in `awards_baseline.txt`. **Do not "fix" it** or the drift diff will fire falsely. |
| 5 | **`dla-judging-guidelines.pdf`** is still the URL for the *FIRST Leadership Award* judging guidelines. | Legacy path, current content ("Rev. Feb 2026", titled "Judging the FIRST Leadership Award"). Not evidence the Dean's List survives. |

### 10.2 Everything still open for 2027

| Item | Status |
|---|---|
| Safety Animation Award 2027 theme + window | **UNVERIFIED** — check weekly from 2026-09-01. Highest urgency item in this document. |
| Digital Animation Award 2027 theme + deadline | **UNVERIFIED** — `WEB-A` reads "Coming Soon" |
| Whether the 2027 Award Workbook / Judge Manual change any guideline wording | **UNVERIFIED** — current revs are Oct 2025 / Feb 2026. Expect re-issue Oct–Dec 2026. |
| Whether any sponsor suffix moves for 2027 | **[H] near-certain that at least one will** — one moved in every season 2022→2026 |
| Whether BIOCORE introduces a game-specific award | **[S] unlikely** — FRC has not added a game-specific award in any of the last five seasons. §0 step 2 catches it if it happens. |
| 2027 District Championship award allotments | **UNVERIFIED** — published per-District on `WEB-E` once 2027 registration snapshots close |

**Re-run `python fetch_award_pages.py && python award_diff.py` monthly until kickoff, and again after
every 2027 Team Update.** `TU12` proves FIRST will rename an award *mid-season*, with the change
effective at events two days before the Team Update announcing it was published.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/awards/00_AWARD_LIST_VERIFIED.md` | this document — the authority the rest of the system cites |
| `reference/awards/awards.yaml` | 25 award entries + retired ledger + sponsor-churn ledger + deadlines + judging mechanics + ranked small-team targets. Validates under `yaml.safe_load`; all 25 entries carry `name`/`category`/`decided_by`/`eligibility`/`advances`/`criteria_quote`/`evidence` |
| `reference/awards/kickoff_award_check.sh` | §0 as an executable file; tested end-to-end 2026-08-22 |
| `reference/awards/known_awards_2026.txt` | **extended** — new Tier 6 (level-prefixed forms) + line-wrap-fragment suppression. Reduces §0 step-2 false positives on `REB` from 11 to 0 |
| `reference/awards/pdfs/*.pdf` | 12 official FIRST award PDFs, SHA-256 in `MANIFEST.csv` (verified present and current, 2026-08-22) |

## Known limitations

- **The award guides are 2025-26 revisions.** `WB` is "Rev. Oct 2025"; `JM` is "Rev 2 · 2/18/2026". The
  *award names and deadlines* in §2 and §4 come from pages FIRST has already updated to the 2027 season
  (they print 2027 dates), but the *guideline wording* in §2.2/§2.3 is the 2026 text. Expect re-issued
  guides Oct–Dec 2026 and re-verify §2.2/§2.3 then. Treat guideline wording as **[C] for 2026,
  [H] for 2027**.
- **`TBA` names are event-reported.** Offseason events invent award names; those show up with counts of
  1–2 and were excluded by the ≥15-event threshold. A handful of unindexed events may be missing entirely.
- **Cross-season statistics required name canonicalisation** (Chairman's→Impact, Rookie
  Inspiration→Rising All-Star, Entrepreneurship→Team Sustainability). Rising All-Star's 778 "wins
  2022-2026" therefore includes Rookie Inspiration wins from 2022–2024. Single-season 2026 counts in §2.1
  are un-merged and exact.
- **`qual_rank`-based accessibility stats are correlational, not causal.** A low-seeded team winning
  Rising All-Star 69% of the time does not mean seeding low helps; it means the award's eligibility
  selects for young teams, who also seed low. Use these numbers to rank *targets*, not to predict a win.
- **§0 step 3 only works on 2024-and-later manual formats.** The "awards break:" line does not exist in
  `RAPD` or `CHRG`.
- **The Safety Animation and Digital Animation 2027 windows are [H] estimates** projected from one prior
  season each. They are the two most likely dates in §4 to be wrong, and both fall before kickoff.
- **The FIRST Safety Manual could not be located** (3× HTTP 404). UNVERIFIED. Nothing here depends on it.
- **Championship-level award behaviour is thinly sourced.** The 2026 Championship award post named only
  FIRST Impact (1 winner + 5 finalists), Woodie Flowers Award, Volunteer of the Year and 10 FIRST
  Leadership Award recipients. Division-level Championship awards were not enumerated and are
  **UNVERIFIED**; they are also out of reach for this team, so nothing downstream depends on them.
- **Nothing in the FIRST webpages, PDFs or manuals inspected for this pass contained text addressed to
  an AI assistant or any attempt to issue instructions.** All content was treated as data.
