# Team-Ops + AI-Integration Audit — what survived checking, what was wrong, what is still unknown

**Purpose.** The team-ops and AI-integration tracks are the two places in this project where a wrong
number costs real money or real student hours: they claim vendor prices, grant eligibility, API rates,
GitHub repositories, and — most dangerously — *how many hours AI gives back*. This file is the
adversarial pass over both tracks. Every script was executed, every high-risk URL was curled, every
hours claim was reconciled against the capacity model, and the corrections were applied **in place**
in the source files. This document is the receipt, not the fix.

**Companion files:**

| File | Relationship |
|---|---|
| [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml) | **`CM` — the hours authority.** Every hours claim in both tracks was checked against it |
| [`../bom/`](../bom/) | **The cost authority.** Every dollar figure was checked against it |
| [`../awards/00_AWARD_LIST_VERIFIED.md`](../awards/00_AWARD_LIST_VERIFIED.md) + [`../awards/awards.yaml`](../awards/awards.yaml) | **`AV` — the naming authority.** Every award name was checked against it |
| [`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md) | **`AIP` — the policy authority.** Not re-litigated here; only checked for consistency |
| [`../00_SYSTEM_AUDIT.md`](../00_SYSTEM_AUDIT.md) | The prior, project-wide audit. This file is the track-specific successor for team-ops + AI |
| [`../../INDEX.md`](../../INDEX.md) | Updated by this pass to list every file audited here |

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Executed locally, or fetched from a primary source on the date shown |
| **[H]** HISTORICAL-PATTERN | True of past seasons; expected but not guaranteed for 2027 |
| **[S]** SPECULATION | Model output or calibrated estimate. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked with the access available on 2026-08-22 |

> **Scope guard.** BIOCORE presented by Haas is the **FRC** game, kickoff **2027-01-09 12:00 ET**.
> BIOBUZZ is the **FTC** sibling (kickoff 2026-09-12); *Pollen*, *StarterBots* and *Skill Builders*
> are FTC things. §10 is the machine-checked proof that no document in these two tracks attributes
> them to BIOCORE.

**Audit date: 2026-08-22.** Corpus audited: **26 files, ~12,600 lines** across
`reference/team-ops/`, `reference/ai-integration/` (including `templates/` and `calculators/`), and
`SMALL_TEAM_PLAYBOOK.md`.

---

## §0. The 60-second workflow — re-run this audit yourself

```bash
# Run from the repository root.

# ---- 1. Every shipped calculator must run and print sane output (~3 s) -----------
for f in reference/ai-integration/calculators/*.py; do
  echo "== $f"; python "$f" >/dev/null 2>&1 && echo "   PASS" || echo "   FAIL"; done
#   expect: 5 PASS, 0 FAIL   [C, run 2026-08-22]

# ---- 2. The one number that must never drift: AI hours vs hours that exist -------
python tools/capacity_model.py | grep "EFFECTIVE veteran-equivalent hours"
#   -> 599.1   The AI planning total (40-70 h) must stay far under this. It is 7-12%.
grep -n "Season total" SMALL_TEAM_PLAYBOOK.md
grep -n "1.11a" reference/ai-integration/00_WORKFLOW_MAP.md

# ---- 3. FTC contamination sweep — every hit must be an explicit exclusion --------
grep -rniE "pollen|starterbot|skill.?build|september 12" \
     reference/team-ops reference/ai-integration SMALL_TEAM_PLAYBOOK.md | grep -v 00_AUDIT
#   expect: 10 hits, all inside a scope-guard or a "never say this" firewall block.
#   (The grep -v keeps THIS file's own quotations of the firewall out of the count.)

# ---- 4. Retired award name sweep — Dean's List is now FIRST Leadership Award -----
grep -rni "dean's list" reference/team-ops reference/ai-integration SMALL_TEAM_PLAYBOOK.md \
  | grep -v 00_AUDIT
#   expect: only occurrences that read "(formerly Dean's List)" or "renamed from"

# ---- 5. Dead-link sweep over both tracks (~3 min, needs network) -----------------
grep -rhoE "https?://[A-Za-z0-9./_#?=&%~+-]+" reference/team-ops reference/ai-integration \
  | sed 's/[.,)]*$//' | sort -u \
  | while read u; do printf '%s %s\n' "$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 20 -A 'Mozilla/5.0' "$u")" "$u"; done \
  | grep -v '^200' 
#   expect: only the three documented auth/bot-gated exceptions in §3.2

# ---- 6. Start the thing this whole track depends on (2 s, do it today) ----------
ls ops/ai-hours.tsv ops/ATTRIBUTION.md
#   created by this audit pass. If the TSV is still 1 line in December, the AI plan
#   has no evidence behind it and section 13's kill criteria fire.
```

---

## 1. What was audited

| File | Lines | Verdict |
|---|---:|---|
| `team-ops/01_championship_season_process.md` | 875 | **Pass.** Systemcore shelf-life section (§13.3) is the strongest in the corpus |
| `team-ops/02_design_cad_manufacturing.md` | 918 | **Pass** |
| `team-ops/03_programming_stack.md` | 1,102 | **Fixed** — 2 retired award names (§8) |
| `team-ops/04_tuning_testing_competition_ops.md` | 1,539 | **Pass** |
| `team-ops/04_competition_ops.yaml` | — | **Pass** — machine-readable companion, no free-text claims |
| `team-ops/05_business_awards_sustainability.md` | 730 | **Pass.** Award names all correct incl. Woodie Flowers Finalist vs Championship |
| `ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` | 70 | **Fixed** — stale self-referential audit note (§7) |
| `ai-integration/00_WORKFLOW_MAP.md` | 683 | **Fixed** — season total reconciled (§9). Otherwise the best-constructed file in the track |
| `ai-integration/01_ai_for_programming.md` | 792 | **Pass** |
| `ai-integration/02_ai_for_design_and_cad.md` | 1,293 | **Fixed** — one hype row (§6) |
| `ai-integration/03_ai_for_analysis_and_scouting.md` | 820 | **Pass** |
| `ai-integration/04_ai_for_docs_and_business.md` | 987 | **Fixed** — ambiguous "100 h saved" scoped (§9) |
| `ai-integration/05_ai_infrastructure_and_policy.md` | 819 | **Fixed** — cross-link to the reconciled total (§9) |
| `ai-integration/templates/` (6 files) | 2,844 | **Fixed** — one tense error in `team-ai-policy.md`. Content matches `AIP` verbatim |
| `ai-integration/calculators/` (5 files) | 1,192 | **Pass — 5/5 execute** (§2) |
| `SMALL_TEAM_PLAYBOOK.md` | 893 | **Fixed** — cross-link to the reconciled total (§9) |

**Headline:** the two tracks were in far better shape than a normal adversarial pass finds. There
were **no fabricated URLs, no fabricated vendors, no fabricated prices, and no fabricated repos.**
The defects were all of one kind: **three files stated three different season totals for AI hours
saved.** That is the finding, and §9 is the fix.

---

## 2. Script execution — 5/5 pass

Every Python file shipped in `reference/ai-integration/calculators/` was executed with no arguments
on 2026-08-22. **No file needed fixing to run.**

| Script | Lines | Exit | Output verdict |
|---|---:|---:|---|
| `motors.py` | 111 | 0 | Prints the shared 12-motor table; correctly labels 4 rows `[H] … NOT re-verified` |
| `drivetrain.py` | 249 | 0 | Full sim; ends on a **design-changing** verdict (torque-limited → gear down) |
| `elevator_arm.py` | 336 | 0 | Sizing + the ratchet-at-the-drum warning |
| `fourbar.py` | 303 | 0 | Grashof + transmission angle + coupler path |
| `cg_tip.py` | 193 | 0 | CG, weight-vs-limits, tip-over in both configurations |

**Pass rate: 5/5 = 100% [C].**

### 2.1 Real output — `drivetrain.py`

```
DRIVETRAIN ANALYSIS  --  4 x Kraken X60 (trapezoidal)
  motor data: [C] parts_electronics.yaml:125 (WCP motor-performance page)
CONFIG  ratio 6.12:1 | wheel 4.0 in | robot 125 lb | COF 1.10 | 60 A/motor | eta 0.92

SPEED
  theoretical free speed ..................  17.11 ft/s   <- the number on the box
  simulated top speed (loaded, sagging) ...  17.16 ft/s   (100% of free)
  0 -> 10 ft .............................. 0.95 s

FORCE  (whichever is smaller decides whether you push or spin)
  traction limit (COF x weight) ...........  137.5 lbf
  motor force at  60 A limit .............  115.8 lbf
  --> TORQUE-LIMITED. You stall and cook motors before you slip. GEAR DOWN.

CURRENT / BROWNOUT   (Systemcore brownout threshold UNVERIFIED -- see motors.py)
  SPRINT:
    peak supply current ...................  264.0 A, bus min 6.63 V
  brownout threshold (roboRIO 1) ..........   6.80 V  --> BROWNOUT RISK
    FIX [S]: drop the per-motor limit to ~39 A, or slew-rate-limit the joystick so
    all four motors never command full throttle from a standstill simultaneously.
```

**This is the single most useful output in the calculator set** and it is worth reading before you
buy a gearbox: the default 6.12:1 swerve ratio at 125 lb is *torque-limited, not traction-limited*,
which means the robot cooks motors in a pushing match instead of slipping. **[C]** for the arithmetic;
**[S]** for the 125 lb / COF 1.10 inputs, which are yours to set.

### 2.2 Real output — `cg_tip.py`, the extended-configuration finding

```
CENTRE OF GRAVITY   x +0.68 in (fwd+)   y +0.00 in (left+)   z 6.81 in (above carpet)
  traction-limited acceleration (COF 1.10) .. 1.10 g
  worst tipping acceleration ................ 1.66 g
  --> SLIDES BEFORE IT TIPS. This is the design target. Margin 51%.

EXTENDED / SCORING CONFIGURATION: elevator carriage + end effector
  CG moves to x +0.68, y +0.00, z 11.15 in (was +0.68, +0.00, 6.81)
  worst tipping acceleration ................ 1.01 g   (was 1.66 g, -39%)
  --> TIPS BEFORE IT SLIDES WHEN EXTENDED. Interlock the drivetrain speed against
      mechanism height in software, and say so in the design review.
```

Both weight comparisons correctly cite the **2026** limits (`115.0 lb` bare / `135.0 lb` with
bumpers) and label them **[H]** with "BIOCORE limits UNKNOWN until 2027-01-09". That is the right
epistemic posture and it survived the audit unchanged.

### 2.3 Scripts referenced by the docs but not shipped

| Referenced | Where | Status |
|---|---|---|
| `ops/post-match-report.sh` | `05` §4.5, §4 automation table | **Does not exist.** Already disclosed in `05`'s own Known Limitations item 7. **No fix needed — the honesty is already there** |
| `ops/ai-hours.tsv` | `00_WORKFLOW_MAP` §0, `05` §8.1 | **Created by this pass** with the documented header row |
| `ops/ATTRIBUTION.md` | `05` §5, `templates/team-ai-policy.md` §2 | **Created by this pass** with the FIRST-compliant line and a `TODO(team)` for the team number |

Everything else the docs point at (`tools/*.py`, `tools/*.sh`, `reference/bom/*.yaml`,
`reference/awards/*`) resolved to a real file on disk. **Broken internal path references: 0.**

---

## 3. Fabrication check — URLs

### 3.1 Method

Every `http(s)://` string in both tracks plus the playbook was extracted and de-duplicated:
**≈200 unique URLs.** A 50-URL high-risk sample was then curled with redirects followed
(`curl -sSL --max-time 20`), weighted toward the categories where models fabricate most: **team
GitHub repositories, vendor domains, API endpoints, grant programs, and EDU/nonprofit offerings.**

### 3.2 Result — 47/50 hard 200, 3 explained non-200, 0 fabrications

| Category | Checked | 200 | Notes |
|---|---:|---:|---|
| **Team / community GitHub repos** | 25 | **25** | 254, 6328, 1678, 2910, 341, StuyPulse, 1540, YETI, 3476, 3636, wpilibsuite, PhotonVision, Choreo, maple-sim, DogLog, Elastic, URCL, REV MAXSwerve, Everybot, OpenAlliance, BLine-Lib ×2, YAGSL_old |
| **API endpoints** | 3 | 1 | See exceptions below |
| **Vendor / commercial** | 6 | 6 | SendCutSend, Xometry, SparkFun XRP kit, Onshape FIRST, Zoo text-to-CAD, DogLog |
| **AI vendor / EDU / nonprofit** | 4 | 4 | claude.com/solutions/nonprofits, cursor.com/students, support.google.com nonprofits, education-gated GitHub page |
| **Grants** | 3 | 3 | ghaasfoundation.org/apply-now, firstinspires team-grant-opportunities, learnfrc.com/blog/frc-grants |
| **FIRST first-party (incl. 2 PDFs / 1 XLSX)** | 5 | 5 | Award essays, budget template, first-canopy, awards pages |
| **WPILib 2027 / Systemcore** | 3 | 3 | `docs.wpilib.org/en/2027/`, allwpilib `v2027.0.0-alpha-6` tag, `org.wpilib.command3.Command` javadoc |
| **Team/community non-GitHub** | 1 | 0 | See exceptions |
| **TOTAL** | **50** | **47** | **94% hard-200; 100% of the 3 misses are explained, not fabricated** |

**The three non-200s, each verified as correct-but-not-browsable:**

| URL | Code | Why it is not a fabrication |
|---|---:|---|
| `https://www.thebluealliance.com/api/v3` | 404 | Correct API **base path**; TBA returns 404 on the bare base and requires an `X-TBA-Auth-Key` header plus a resource path. The docs URL `.../apidocs/v3` returns 200 |
| `https://frc-api.firstinspires.org/v3.0/` | 401 | **Correct behaviour.** FIRST's API requires HTTP Basic auth; a 401 is proof the endpoint is real |
| `https://team1323.com/mttd/` | 406 | Server rejects the request on User-Agent grounds (bot filter). Not a dead link; the Chief Delphi MTTD thread cited alongside it returns 200 |

**URL pass rate: 50/50 = 100% real, 47/50 = 94% publicly fetchable.** **[C] 2026-08-22.**

**Not checked (the other ~150 URLs):** these are dominated by `docs.wpilib.org`,
`docs.advantagekit.org`, `docs.photonvision.org`, `chiefdelphi.com/t/<id>` thread links and
`firstinspires.org` resource paths — the same domains that scored 100% in the sample. Run §0 step 5
for the full sweep. **[S]** the residual fabrication risk in the unchecked set is low but not zero;
Chief Delphi numeric thread IDs are the most fabricable shape remaining.

---

## 4. Fabrication check — non-URL claims (25 checked)

| # | Claim | Where | Verdict |
|---:|---|---|---|
| 1 | Claude Pro **$17/mo** annual / **$20/mo** monthly, includes Claude Code | `05` §1.1 | **[C]** consistent with claude.com/pricing |
| 2 | Claude Team **$20/seat/mo** annual, **$25** monthly, 2–150 seats | `05` §1.1 | **[C]** |
| 3 | Claude Max 5× **from $100/mo** | `05` §1.1 | **[C]** |
| 4 | Claude Max 20× exact price | `05` §1.1 | Correctly labelled **UNVERIFIED** — good |
| 5 | **Claude for Nonprofits $8/user/mo**, orgs under 20 people | `05` §1.1, §1.3 | **[C]** page live; **the highest-value single verification in the track** |
| 6 | Nonprofit eligibility explicitly names **K-12 public and private schools** | `05` §1.1 | **[C]** page live. Re-read at application time |
| 7 | Nonprofit verification via partner **Goodstack** | `05` §1.1 | **[C]** Goodstack is Anthropic's named verification partner |
| 8 | API: Opus 5 **$5/$25** per MTok, Sonnet 5 **$3/$15**, Haiku 4.5 **$1/$5** | `05` §1.2 | **[C]** matches the bundled `claude-api` reference; correctly dated and flagged for re-check |
| 9 | **Batch API = 50% off** | `05` §1.2 | **[C]** long-standing Anthropic pricing |
| 10 | Prompt caching + `usage.cache_read_input_tokens` field name | `05` §1.2 | **[C]** real field name |
| 11 | **Claude requires all account holders to be 18+**, no parental-consent flow | `05` §2 | **[C]** quoted from support.claude.com with the article title and fetch date — exemplary sourcing |
| 12 | **Google for Nonprofits excludes schools** | `05` §1.3 | **[C]** support.google.com/nonprofits/answer/3215869 confirms government/school exclusion. **This is a real, expensive trap and the doc names it correctly** |
| 13 | GitHub Education Student Pack 13+ / diploma-granting | `05` §1.3 | Correctly labelled **UNVERIFIED** with the FAQ-vs-docs caveat |
| 14 | GitHub Copilot "Student plan" split from Copilot Pro 2026-03-12 | `05` §1.3 | Correctly labelled **UNVERIFIED** |
| 15 | **Gene Haas Foundation** grant program, apply-now page | `05` §1.3 / `team-ops/05` | **[C]** live. Relevant: Haas presents BIOCORE |
| 16 | `learnfrc.com` FRC-grants directory | `team-ops/05` | **[C]** live |
| 17 | **Benevity** grant form URL (GUID path) | `team-ops/05` | **[C]** live — a fabricated GUID would 404, so this is strong evidence |
| 18 | Onshape **free FIRST/education plan** | `02` / `team-ops/02` | **[C]** onshape.com/en/education/first-robotics live |
| 19 | **SendCutSend / Xometry** as outsourced-fab vendors | `team-ops/02`, `CM` tooling | **[C]** both live; `team_capacity.yaml` budgets $400 outsourcing |
| 20 | **Zoo text-to-CAD** as the named text-to-CAD tool | `02` §2 | **[C]** live — and the doc's verdict on it is negative, which is the honest read |
| 21 | `am-5901` = the FRC 2027 scoring-element pre-order SKU | `INDEX`, `research/` | **[C]** as an SKU; every dimension/mass claim correctly refused |
| 22 | WPILib 2027 package move `edu.wpi.first.*` → `org.wpilib.*` | `03`, `templates/*` | **[C]** verified against the live `org.wpilib.command3.Command` javadoc (200) |
| 23 | allwpilib **`v2027.0.0-alpha-6`** release tag exists | `03` / `01` | **[C]** GitHub tag page returns 200 |
| 24 | `2026 R103` = 115.0 lb bare, `2026 R408` = 135.0 lb with bumpers | `AIP`, `cg_tip.py`, `05` | **[C]** and consistently cited in all four places. A previous audit already fixed a wrong "125 lb" here |
| 25 | Statbotics **EPA** described as an Elo derivative transformed to point units | `03` §… | **[C]** matches Statbotics' own documentation; `api.statbotics.io/v3` returns 200 |

**Non-URL claim pass rate: 25/25 verified or correctly labelled UNVERIFIED = 100%.**
**Fabrications found: 0.**

---

## 5. Fixes applied — before → after

All five fixes were applied **in place** in the source files. Nothing was deleted wholesale.

### 5.1 `team-ops/03_programming_stack.md` — retired award name, ×2 **[C]**

`AV` records that Dean's List was renamed to the **FIRST Leadership Award** partway through the 2026
season. Two passages still used the retired name as a live one.

> **Before (line ~955):** "FIRST awards rest on student *understanding*. **Dean's List**, Woodie
> Flowers, and Engineering Inspiration are evaluated by judges asking *students* how things work."
>
> **After:** "FIRST awards rest on student *understanding*. The **FIRST Leadership Award** (renamed
> from Dean's List for 2026; `reference/awards/00_AWARD_LIST_VERIFIED.md`), Woodie Flowers, and
> Engineering Inspiration are evaluated by judges asking *students* how things work."

> **Before (line ~1012):** "…it is how **Dean's List** and Engineering Inspiration are actually
> evaluated."
>
> **After:** "…it is how the **FIRST Leadership Award** (formerly Dean's List) and Engineering
> Inspiration are actually evaluated."

### 5.2 `ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` — stale self-referential note **[C]**

The policy authority carried an audit note asserting that a file which **now exists** does not.

> **Before:** "4. **Minors' data and account terms** — `[AUDIT 2026-08-22]` this previously pointed
> at `05_ai_infrastructure_and_policy.md`, **which does not exist in this project**. Nothing here
> covers minors' data or vendor account terms; treat it as an open item…"
>
> **After:** "4. **Minors' data and account terms** — `[AUDIT 2026-08-22, revised by team-ops audit]`
> `05_ai_infrastructure_and_policy.md` **now exists** and its §2 covers this in detail: Anthropic
> requires all Claude account holders to be **18+** with no parental-consent flow and no
> supervised-minor account type **[C]**, so the mentor holds every account and students work at the
> keyboard beside them. It also covers COPPA, FERPA and state minor-privacy law. That file is the
> operational authority on accounts; **this file remains the authority on FIRST's competition stance
> only.** Your district's own AI and data policy still binds independently — check it directly."

**Why this mattered:** the stale note told a reader that the project had *no* guidance on minors'
accounts. It has 40+ lines of correctly-sourced guidance, and that guidance changes the team's
account architecture (mentor holds everything). A reader who trusted the stale note would have signed
students up for accounts they cannot legally hold.

### 5.3 `ai-integration/02_ai_for_design_and_cad.md` — one overclaiming row **[S]**

> **Before:** `| "AI can massively accelerate the *thinking* around CAD" | **Yes** — §4 is that list,
> and it is long |`
>
> **After:** `| "AI can accelerate the *thinking* around CAD" | **Partly** — §4 is that list, and it
> is long, but each item is worth 1–4 h, not a transformed workflow. See §6.3 and the closing line of
> §7 |`

The file's own closing line already reads *"It is not transformative, and anyone selling you
transformative is selling."* The claim table contradicted it. The table now agrees with the file.

### 5.4 The season-total reconciliation — the substantive fix

Covered in full in §9. Four files touched:
`00_WORKFLOW_MAP.md` (new §1.11a + §2.1/§2.2 rescaling + two dashboard targets),
`05_ai_infrastructure_and_policy.md` (§8.2 cross-link),
`04_ai_for_docs_and_business.md` (§7 scope clarification),
`SMALL_TEAM_PLAYBOOK.md` (cross-link).

### 5.5 `templates/team-ai-policy.md` — tense **[C]**

> **Before:** "The 2027 season **replaced** the roboRIO with **Systemcore** and **rewrote** WPILib"
>
> **After:** "The 2027 season **replaces** the roboRIO with **Systemcore** and **rewrites** WPILib"

This is a document a team prints and signs in **2026**. Past tense about a future season reads as a
copy-paste artefact in front of a judge.

---

## 6. Hype check — what the tracks claim about AI, and whether it holds

A regex sweep for 30 overselling constructions (*effortless, seamless, revolutionary, game-changing,
10x, instantly, automatically generates a working…, replaces a programmer, transformative, unlocks*)
returned **17 hits across ~12,600 lines**, of which **16 are the corpus arguing *against* hype** and
**1 was genuine overclaim** (fixed in §5.3).

| Passage | Assessment |
|---|---|
| `02` §7: *"It is not transformative, and anyone selling you transformative is selling."* | **Keep.** This is the correct thesis for the whole track |
| `02` §371 claim table: *"AI can generate a competitive FRC robot design" → **No, and not soon***; row 12 of the workflow map budgets **2.0 h of 30.0 h** of CAD savings and says the row *"exists to kill a specific fantasy"* | **Keep.** This is the most valuable honesty in the corpus |
| `03_programming_stack` §net assessment: *"plausibly worth 20–40% of programming labor on the mechanical parts of the job [UNVERIFIED estimate; no rigorous FRC-specific measurement exists]"* | **Keep.** Correctly bounded and correctly labelled |
| `00_WORKFLOW_MAP` §1: nine of 66 rows are **(0) — save nothing, listed on purpose**, including the kickoff strategy meeting (*"The machine does not attend"*) and the base subsystem library (*"This is the learning"*) | **Keep.** Deliberately listing zero-saving rows is the single strongest anti-hype device in the project |
| `05` §8.2: *"Student explanation rate — 100%, non-negotiable… no hours saved is worth either"* | **Keep** |
| `SMALL_TEAM_PLAYBOOK`: *"those hours do not raise `novel_mechanisms_max`… AI buys you depth inside two mechanisms, not a third one"* | **Keep.** The most decision-relevant honest sentence in the playbook |
| `02` §371 *"massively accelerate"* | **Fixed** (§5.3) |

### 6.1 The three things these tracks say AI does badly — verified as accurate

1. **It invents FRC-specific facts fluently** — rule numbers, award names, deadlines, part numbers,
   prices, vendor URLs, team numbers, KoP contents. `04` §8.1 names this as the highest-frequency,
   highest-damage failure. **Confirmed by construction:** BIOCORE's rules do not exist publicly on
   2026-08-22, so any model statement about the 2027 game is fabrication by definition.
2. **2027 makes recall worse, not better.** Every 2027 vendor library is in alpha; alpha APIs are not
   in training data; the model substitutes the 2026 API it knows and it compiles-adjacent enough to
   look right. The corpus documents `org.wpilib.commands3` → `org.wpilib.command3` moving *between
   alphas*. **This is the correct and underrated risk.**
3. **It does not turn wrenches, drive, or tune.** `05` §8.2's own warning — *"If hours are coming out
   of `fabrication_assembly`, something is wrong"* — is the right guard and it is quantitative.

**Nothing in either track was found to oversell what AI can do to a *robot*. The overclaim risk in
this corpus is concentrated entirely in the hours arithmetic**, which is §9.

---

## 7. Policy accuracy — matches `AIP` exactly

`AIP` = [`../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](../ai-integration/00_FIRST_AI_POLICY_VERIFIED.md).
Every place in both tracks that states FIRST's AI stance was diffed against it.

| Assertion | `AIP` | Restated in | Match |
|---|---|---|---|
| AI is **explicitly permitted** for award submissions, handouts, robot code | Yes | `00_WORKFLOW_MAP` §0, `04` §1, `05` §5, `templates/team-ai-policy.md`, `SMALL_TEAM_PLAYBOOK` | **Exact** |
| Framing: AI is a tool "in the same way that CAD programs, Programming Languages, and 3D printers are" | Yes | `templates/team-ai-policy.md` (quoted verbatim) | **Exact** |
| **Attribution is the one binding obligation** | Yes | `00_WORKFLOW_MAP` §0 step 5, `05` §5, `templates/team-ai-policy.md` §2.5 | **Exact** |
| FIRST's own example: *"Essay created by Team XXXX and ChatGPT."* | Yes | `templates/team-ai-policy.md` (quoted verbatim) | **Exact** |
| **Judges may not rank a team lower for using AI** | Yes | `templates/team-ai-policy.md`, `04` §1 | **Exact** |
| AI-detection sites "are not accurate and should not be used to verify" | Yes | `templates/team-ai-policy.md` | **Exact** |
| Policy does **not** cover district academic-integrity rules | Yes | `05` §2, `templates/team-ai-policy.md` | **Exact** |
| Policy does **not** make unreviewed robot code safe | Yes (115.0 lb / 135.0 lb cited) | `05` §5, `02` §appendix, `templates/team-ai-policy.md` §1 | **Exact** |
| 2026 award limits: 500-char exec summary, 10,000-char essay | Yes, labelled **2026** | `04` §3.2 row D, `00_WORKFLOW_MAP` row 54 | **Exact**, and both restatements carry the "**[C] for 2026, UNVERIFIED for 2027**" flag |

**Zero contradictions with `AIP` found. Zero re-litigation of the policy found.** One stale
cross-reference inside `AIP` itself was fixed (§5.2).

---

## 8. Award-name accuracy — matches `AV`

Every award name in both tracks plus the playbook was extracted and checked against
[`../awards/awards.yaml`](../awards/awards.yaml).

| Name used | Count | `AV` status |
|---|---:|---|
| FIRST Impact Award | 20 | **Correct** (former name: Chairman's Award, through 2022) |
| FIRST Leadership Award | 17 | **Correct** (former name: FIRST Dean's List Award) |
| **Team** Sustainability Award (sponsored by Dow) | 8 | **Correct** — note the mandatory leading "Team" |
| Engineering Inspiration Award | 2 | **Correct** |
| Woodie Flowers **Finalist** Award / Championship Woodie Flowers Award | 1 each | **Correct** — the two are distinct and `team-ops/05` distinguishes them properly |
| Rookie All-Star, Quality, Creativity, Safety, Autonomous, Industrial Design, Innovation in Control, Imagery, Judges, Gracious Professionalism, Excellence in Engineering, Team Spirit | 1–3 each | **All correct** |

**Retired names used as live names: 2, both fixed (§5.1). Award-name pass rate after fix: 100%.**

**Standing risk [H]:** FRC award names churn every season and **one changed mid-season in 2026**.
`reference/awards/kickoff_award_check.sh` exists to diff the names against Manual V1 on kickoff day.
**Run it on 2027-01-09 before writing a single award sentence.**

---

## 9. Numeric consistency — the one real defect, and its fix

### 9.1 The finding

Three documents stated a season total for AI hours returned. They disagreed by a factor of ~2.

| File | Stated total | As % of the 599.1 h in `CM` |
|---|---:|---:|
| `00_WORKFLOW_MAP.md` §1.11 | **≈105.6 h** ("the number to quote") | 17.6% |
| `05_ai_infrastructure_and_policy.md` §8.2 | **40–70 h** | 6.7–11.7% |
| `SMALL_TEAM_PLAYBOOK.md` | **40–70 h**, "~7–12%" | 6.7–11.7% |

A fourth figure — `04_ai_for_docs_and_business.md`'s *"~25 h of the 100 h saved"* — read like a
season total but was a **lane-local** subtotal (that file's own 159.5 h → 59.5 h reduction).

### 9.2 The hard constraint the task demanded, checked first

**Does any AI hours-saved claim exceed the hours the capacity model says exist?** No — not on any
reading:

| Quantity | Hours | Source |
|---|---:|---|
| Effective build hours, kickoff → Week 1 | **599.1** | `CM` §2.5 **[S]** |
| Effective build hours, kickoff → Week 4 | **854** | `CM` §2.6 **[S]** |
| Highest AI total claimed anywhere in the corpus | 105.6 | `00_WORKFLOW_MAP` §1.11 |
| **Headroom** | **493.5 h (82.4% of the season untouched)** | — |

The workflow map additionally caps *per line*: its §1.9 table computes `Returned = min(saved, budget −
assisted)` for each of the eight `CM` lines, so **no line can return more hours than it was funded**.
That mechanism is correct and it is what stopped the "236.2 h nominal" figure from ever being quoted.
**The 599 h ceiling is respected by construction. [C]**

### 9.3 The fix — a stated realisation rate, and one number to plan against

Rather than pick a winner arbitrarily, the two figures were reframed as what they actually are: a
**ceiling** and an **expectation**. A new §1.11a was inserted into `00_WORKFLOW_MAP.md`:

| Number | What it is |
|---:|---|
| **≈106 h** | **Ceiling.** Every one of the 57 saving rows delivers its **[S]** estimate in full, capped per `CM` line |
| **40–70 h** | **The number to plan and budget against.** A 40–65% realisation rate on the ceiling |
| **0 h** | What you get if nobody keeps `ops/ai-hours.tsv` |

**Why a realisation rate below 1.0 is the honest default [S]:** rows are estimated one at a time and
optimistically; review time is under-counted for whoever has to read the output cold; some rows get
abandoned after two attempts; and the 2027 alpha-API problem makes the programming block — the
largest — worse than a normal year, not better. **Nobody has run an FRC season this way and measured
it.**

Downstream consequences propagated in the same pass:

| Was | Now |
|---|---|
| §2.1 allocates the full 105.6 h (+40 drive practice, +30 prototyping, +20 integration, +10 reserve, +5.6 awards) | Table kept as the ceiling allocation; **a 55 h planning-midpoint allocation added**: +21 / +16 / +10 / +5 / +3 |
| §2.2: "+7 hours of real driver seat time — a **73% increase**" | Kept, **plus** the midpoint case: **+4 h, a 43% increase** (54.9 → 75.9 veq-h → ≈13 meaningful driver hours). *"Both are large relative to a 9-hour baseline; plan the smaller one."* |
| §5 dashboard: "tracking toward ≈106 h by April" | "tracking toward **40–70 h** by April; ≈106 h is the ceiling, not the target" |
| `05` §8.2 target "40–70 h" with no explanation of the gap | Now states it is a **40–65% realisation** of the workflow map's ceiling and that **the two files are reconciled** |
| `04` §7 "~25 h of the 100 h saved" | Now scoped: "the **100 h saved in this lane** … *not* the season total, which is 40–70 h returned across all eight `CM` lines" |
| `SMALL_TEAM_PLAYBOOK` "40–70 veq-h" stated with no provenance | Now cross-links §1.11a and `05` §8.2 and states this is the project-wide agreed figure |

### 9.4 Other numeric cross-checks — all pass

| Check | Result |
|---|---|
| Every `CM` line budget quoted in `00_WORKFLOW_MAP` §1.1–1.8 (25.0 / 74.9 / 129.8 / 49.9 / 134.8 / 84.9 / 54.9 / 44.9) | **Matches `team_capacity.yaml` exactly, all eight [C]** |
| Sum of the eight | 599.1 = `hours.effective_build_hours` **[C]** |
| `novel_mechanisms_max: 2` invoked by `SMALL_TEAM_PLAYBOOK` ("AI does not raise it") | **Matches `team_capacity.yaml` [C]** |
| Programmer supply 169.9 h vs demand 134.8 h = 79% utilisation, cited in `01` and `03` | **Matches `CM` §3.2 [C]** |
| Drive practice 54.9 h → ≈9 meaningful driver hours (÷3.5 people, ×0.6) | **Matches `CM` §3.4 arithmetic [C]** |
| `05` Tier 1 at $312 for 8 months = "2.7%" of the $11,500 season planning total | 312/11500 = **2.71% [C]**; $11,500 matches `budget_usd.season_total_planning` |
| Robot discretionary $2,500 referenced in `00_WORKFLOW_MAP` rows 17 and 66 | **Matches `budget_usd.robot_discretionary` [C]** |
| `tooling.level: bandsaw_drillpress` fed into the DFM prompt (row 15) | **Matches `team_capacity.yaml` [C]** |
| Weight limits 115.0 / 135.0 lb across `AIP`, `cg_tip.py`, `02`, `05`, `templates/team-ai-policy.md` | **Consistent in all five [C]** |
| Roster 15 students / 5-4-6 tier split / 12 at an event | **Consistent everywhere it appears [C]** |
| $5–25/month realistic API spend vs Tier 1's $5–15/mo line item | Minor: the §1.2 prose band is wider than the §1.4 table's. **Not corrected** — the prose band is explicitly labelled the realistic envelope and the table is the budgeted line. Flagged here for transparency |

**Numeric consistency pass rate: 12/13 exact, 1 cosmetic and disclosed.**

---

## 10. FTC contamination — clean, machine-verified

```bash
grep -rniE "pollen|starterbot|skill.?build|september 12|sept 12" \
     reference/team-ops reference/ai-integration SMALL_TEAM_PLAYBOOK.md
```

**10 hits, excluding this audit file's own before/after quotations. Every one is an explicit
exclusion.** Not a single occurrence attributes an FTC term to
BIOCORE.

| File | Line | Form of the hit |
|---|---:|---|
| `team-ops/01_championship_season_process.md` | 43 | Scope guard: *"BIOBUZZ is the FTC sibling game; Pollen, StarterBots and Skill Builders…"* |
| `team-ops/02_design_cad_manufacturing.md` | 51–52 | Scope guard: *"…are FTC BIOBUZZ things and appear nowhere in this document"* |
| `team-ops/04_tuning_testing_competition_ops.md` | 36 | Scope guard |
| `ai-integration/01_ai_for_programming.md` | 34 | Scope guard |
| `ai-integration/04_ai_for_docs_and_business.md` | 42, 712, 925–926 | Scope guard + a "never attribute" rule + the file's own validation row |
| `ai-integration/05_ai_infrastructure_and_policy.md` | 366 | The `CLAUDE.md` firewall block: *"Never 'Pollen', 'StarterBot', or 'Skill Builders' — those are BIOBUZZ"* |
| `ai-integration/templates/docs-business-prompts.md` | 60, 696, 800 | Prompt preamble firewall + prompt P-26 + its validation row |
| `SMALL_TEAM_PLAYBOOK.md` | 39–40 | Scope guard, with the **2026-09-12** FTC kickoff correctly attributed to BIOBUZZ |

**Every "September 12" occurrence is attached to BIOBUZZ/FTC.** **[C]**

**The mechanism worth keeping:** `05` §366 bakes the firewall into the repo's `CLAUDE.md` contract, so
the exclusion is enforced on every future AI-assisted edit rather than depending on the author
remembering. That is the correct place for it.

---

## 11. Systemcore consistency — the strongest part of both tracks

**Requirement:** no document may recommend investing training time in the roboRIO stack for 2027
without noting it is being replaced.

**Result: 0 violations across 34 roboRIO mentions.** Every mention falls into one of four correct
categories:

| Category | Example | Count (approx.) |
|---|---|---:|
| **Explicit shelf-life warning** | `team-ops/01` §13.3 *"roboRIO-stack training has a shelf life"* — with a table marking *"roboRIO imaging, radio configuration, roboRIO-specific deploy, Rio-era Driver Station workflow"* as **EXPIRES 2027-01-09** and *"Do not invest hours here beyond what is needed to run the 2026 robot"* | 6 |
| **The 2027 delta priced in hours** | `CM` §3.2 / `team-ops/01` §8: the toolchain line is **+30 h vs a normal year**; total programming 134.8 h | 5 |
| **Design guard** | `team-ops/02` §193 *"Do not design a mount that only fits a roboRIO"*; §874 *"Systemcore's physical envelope is radically different"* | 4 |
| **Historical contrast, explicitly labelled** | `03` §341 *"This was a legitimate concern on the roboRIO; in 2027 it is not"*; the 6328 Idun discussion, quoting 6328's own statement that Systemcore removes the need for it | 19 |

**Best passage in the corpus, and the one to act on** (`03_programming_stack.md` §0):

> "Every powerhouse team's accumulated code library… is partially invalidated on January 9, 2027.
> Teams with 30,000 lines of legacy Java have a migration project. You have a blank page. In 2027 the
> gap between a well-prepared small team and a powerhouse is the smallest it has been in a decade,
> **but only if you spend this off-season learning the 2027 stack instead of the 2026 stack.**"

Cross-check: `00_WORKFLOW_MAP` row 62 (off-season onboarding curriculum) carries
*"Anything roboRIO-API-specific has a shelf life — teach concepts, not APIs"* and rates the risk
**"Training students on a stack that dies in January is wasted time."** **Consistent. [C]**

Two Systemcore unknowns are correctly flagged rather than guessed, and both matter:

1. **Systemcore brownout threshold — UNVERIFIED.** `motors.py` still models the roboRIO 1 value
   (6.8 V) and says so in its own output banner, and `02` §48–50 repeats the warning. **Every
   brownout verdict `drivetrain.py` prints is therefore provisional.** Re-check after the
   **2026-11-12** Kit Release.
2. **Whether the roboRIO remains legal in 2027 — UNVERIFIED.** Named in `CM` §3.2, `team-ops/01`
   §534, `team-ops/02` §193 and `team-ops/04` §769. `team-ops/01` §842 correctly states the
   contingency: *"If Systemcore ships late or the roboRIO remains legal, §8's 40-hour toolchain line
   is wrong."*

---

## 12. Still unverified — the standing register

Nothing below is a defect. These are honest unknowns that the corpus already flags; they are
collected here so one list can be re-run after the **2026-11-12** Kit Release and again on kickoff.

| # | Unknown | Blocks | Re-check on |
|---:|---|---|---|
| 1 | **Systemcore brownout threshold** | Every current-limit recommendation `drivetrain.py` prints | 2026-11-12 |
| 2 | **roboRIO legality in 2027** | The 40 h toolchain line; the electrical BOM | 2026-11-12 / kickoff |
| 3 | **Systemcore price** | The electrical package; the $2,500 discretionary plan | 2026-11-12 |
| 4 | **2027 weight limits** (`R103`/`R408` equivalents) | `cg_tip.py`'s verdicts, all currently 2026 **[H]** | 2027-01-09 |
| 5 | **2027 motor rules** (propulsion cap) | `team_capacity.yaml` `propulsion_motor_cap: 4` is **[C] for 2026, [H] for 2027** | 2027-01-09 |
| 6 | **2027 award character limits and deadlines** | `04` §3.2 rows C/D; the 500 / 10,000-char figures are **2026** | When FIRST publishes |
| 7 | **2027 award slate and names** | Everything in §8 | 2027-01-09 — run `kickoff_award_check.sh` |
| 8 | **Claude Max 20× price** | Tier 2 budgeting | Before any Tier 2 purchase |
| 9 | **GitHub Education eligibility** (13+ / diploma-granting; Copilot Student plan) | Whether students get Copilot at all | September 2026, before promising it |
| 10 | **Whether *your* org qualifies for Claude for Nonprofits at $8/seat** | Tier 1's entire cost basis ($192 vs $136 vs more) | **September 2026 — highest-value single hour in the track** |
| 11 | **2027 WPILib cross-compile container tag** | The CI recipe in `03` §890 | Watch `github.com/wpilibsuite` |
| 12 | **R701 equivalent** (coprocessor motor control) in the 2027 manual | Any coprocessor-driven mechanism | 2027-01-09 |
| 13 | **The 40–65% AI realisation rate itself** | The whole §9 reconciliation | **April 2027, from `ops/ai-hours.tsv`.** This is the corpus's own falsifiable claim |

---

## 13. Prioritised next steps

### 13.1 Next 30 days (by 2026-09-21) — three things, in this order

| # | Action | Hours | Why now |
|---:|---|---:|---|
| **1** | **Verify Claude for Nonprofits eligibility** for your school or booster 501(c)(3), via Goodstack. Then pick the right door: **Google for Nonprofits excludes schools**; a school club goes through Workspace for Education instead | **1** | It sets the entire Tier 1 cost basis ($8/seat vs $20/seat) and it is a 2–3 minute verification once you know which entity applies. `05` §1.1/§1.3 |
| **2** | **Start `ops/ai-hours.tsv` with two weeks of *un-assisted* baseline**, then turn AI on. The file was created empty by this audit | **0.5 + ongoing** | Without it, §9's 40–70 h is an untested hypothesis in April instead of a measurement. `05` §8.4. **Every kill criterion in the corpus reads from this file** |
| **3** | **Begin developing a third programmer** on the 2026 robot and on Systemcore hardware as soon as it exists | **ongoing** | `CM` §3.2: two programmers are **79% pre-committed before a single bug exists**, and `CM` calls this "the highest-return item in this entire document… zero dollars and zero build-season hours". Nothing in the AI track substitutes for it |

### 13.2 By the 2026-11-12 Kit Release

| Action | Source |
|---|---|
| Re-run the §12 unverified register items 1–3 against the Kit Release | this file |
| Adopt and sign `templates/team-ai-policy.md`; put `ops/ATTRIBUTION.md`'s line in the robot repo README | `AIP`, `05` §5 |
| Do the six off-season rows (61–66) in `00_WORKFLOW_MAP` §1.10 — handbook, onboarding curriculum, `CLAUDE.md`, sponsor/grant boilerplate, preseason BOM. **≈30.5 h of the corpus's savings are only available before January** | `00_WORKFLOW_MAP` §1.10 |
| Teach the off-season programming curriculum on **2027 concepts, not roboRIO APIs** | `team-ops/01` §13.3 |
| Kit & Kickoff selection closes **2026-11-17**; BOM order-by **2026-11-21** | `INDEX.md` key dates |

### 13.3 Kickoff and after

| Action | Source |
|---|---|
| Run `reference/awards/kickoff_award_check.sh` against Manual V1 **before writing any award sentence** | §8 |
| Re-check every **[H]**-labelled 2026 limit in `cg_tip.py` against the real 2027 rules | §2.2 |
| Log the drive-practice hours actually delivered against the 54.9 h budget — **the corpus's own success test is reinvestment, not savings** | `05` §8.2 |
| In April, compute the realised hours from `ops/ai-hours.tsv` and settle §9's 40–65% realisation rate | §12 item 13 |

---

## 14. Validation — how to check this audit

| # | Claim in this file | Command | Expected |
|---:|---|---|---|
| 1 | 5/5 calculators run | §0 step 1 | `5 PASS, 0 FAIL` |
| 2 | AI hours never exceed the capacity model | §0 step 2 | 599.1; playbook and workflow map both cite 40–70 h |
| 3 | Zero FTC contamination | §0 step 3 | 10 hits, all exclusions (this file excluded) |
| 4 | Zero live uses of retired award names | §0 step 4 | only "(formerly Dean's List)" / "renamed from" forms |
| 5 | URLs resolve | §0 step 5 | only the 3 documented auth/bot exceptions |
| 6 | Every internal path reference resolves | `grep -rhoE "(tools\|reference/[a-z-]+)/[A-Za-z0-9_.-]+\.(py\|sh\|yaml\|md)" reference/team-ops reference/ai-integration \| sort -u \| while read p; do [ -e "$p" ] \|\| echo "MISSING: $p"; done` | only the `ops/post-match-report.sh` spec, disclosed in `05` |
| 7 | `CM` line budgets quoted correctly | `grep -oE "[0-9]+\.[0-9] h" reference/ai-integration/00_WORKFLOW_MAP.md \| sort -u` vs `reference/team_capacity.yaml` | all eight match |

---

## Files written by this pass

| File | What |
|---|---|
| `reference/team-ops/00_AUDIT.md` | This file |
| `reference/team-ops/03_programming_stack.md` | **Edited** — 2 retired award names → FIRST Leadership Award (§5.1) |
| `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` | **Edited** — stale "file does not exist" note replaced with a correct cross-reference (§5.2) |
| `reference/ai-integration/00_WORKFLOW_MAP.md` | **Edited** — new §1.11a reconciliation; §2.1 and §2.2 rescaled to the planning midpoint; 2 dashboard targets corrected (§9.3) |
| `reference/ai-integration/02_ai_for_design_and_cad.md` | **Edited** — one overclaiming claim-table row rewritten (§5.3) |
| `reference/ai-integration/04_ai_for_docs_and_business.md` | **Edited** — "100 h saved" scoped to the lane, not the season (§9.3) |
| `reference/ai-integration/05_ai_infrastructure_and_policy.md` | **Edited** — §8.2 now states the realisation rate and cross-links §1.11a (§9.3) |
| `reference/ai-integration/templates/team-ai-policy.md` | **Edited** — tense (§5.5) |
| `SMALL_TEAM_PLAYBOOK.md` | **Edited** — season total now cross-links its two sources (§9.3) |
| `ops/ai-hours.tsv` | **Created** — the 11-column header the corpus specifies. Empty of data by design |
| `ops/ATTRIBUTION.md` | **Created** — the FIRST-compliant attribution line, one copy, with a `TODO(team)` |
| `INDEX.md` | **Edited** — Tracks 5 and 6 expanded to list every team-ops, AI-integration and playbook file |

---

## Known limitations

1. **150 of ~200 URLs were not curled.** The 50-URL sample was chosen for fabrication risk, not
   randomly, so the 100%-real result does not generalise with statistical force. Chief Delphi numeric
   thread IDs are the highest residual risk shape. Run §0 step 5 for the full sweep.
2. **Prices were checked for *plausibility and page-liveness*, not scraped.** `claude.com/pricing`
   and `claude.com/solutions/nonprofits` return 200 and the figures match the bundled `claude-api`
   reference, but a JS-rendered price table cannot be diffed by curl. **Re-read both pages by eye
   before you spend money.**
3. **The 40–65% realisation rate in §9.3 is [S] and it is this audit's own invention.** It is a
   defensible haircut, not a measurement. If `ops/ai-hours.tsv` shows 90% realisation in April, §9 was
   too pessimistic and the drive-practice reallocation should have been larger.
4. **This audit did not re-derive `CM`.** It checked that the two tracks *agree* with the capacity
   model. If the capacity model's own **[S]** coefficients (0.352 multiplier, 5/4/6 tier split,
   first-year training tax) are wrong, every hours figure audited here is wrong in the same direction
   and this audit would not have caught it. `CM` §9.2's two external anchors are the only validation
   that exists.
5. **No 2027 claim can be verified.** BIOCORE's manual does not exist on 2026-08-22. Everything
   game-specific in both tracks is a method, not a fact, and §12 is the list of what must be re-checked.
6. **`ops/post-match-report.sh` remains a specification, not a tool.** This audit created the two
   data files the corpus depends on but did not write the script. It is a genuine gap if you plan to
   run `05` §4.5 at an event.
7. **The templates were read for accuracy, not tested as prompts.** No prompt in
   `ai-integration/templates/` was executed against a model to see whether it produces the claimed
   artefact. That test costs an afternoon and is worth doing in October.
