# AI Infrastructure and Policy — the systems layer

**Purpose.** Everything underneath the other AI documents: which tools to buy, what they cost in
2026 dollars, who is legally allowed to hold an account, where the files live, what runs on a timer,
what to wire into MCP, what the team's written policy says, how students learn to use it, and how you
tell — with numbers — whether any of it returned hours.

**Written** 2026-08-22 (off-season). **Season:** 2027 BIOCORE™ presented by Haas (FRC, FIRST CANOPY),
kickoff **2027-01-09, 12:00 p.m. ET**. ~4.5 months of runway from today.

**Companion files**
- [`00_FIRST_AI_POLICY_VERIFIED.md`](00_FIRST_AI_POLICY_VERIFIED.md) — **authoritative** on what FIRST
  permits. This file does not re-litigate it; it operationalises it.
- [`templates/team-ai-policy.md`](templates/team-ai-policy.md) — the one-page policy this file tells
  you to adopt. Print it, fill the blanks, sign it.
- [`../02_TEAM_CAPACITY_MODEL.md`](../02_TEAM_CAPACITY_MODEL.md) + [`../team_capacity.yaml`](../team_capacity.yaml)
  — **every hour and dollar figure below is checked against these.** They are the authority.
- [`../team-ops/03_programming_stack.md`](../team-ops/03_programming_stack.md) §11 — the honest
  assessment of where AI helps and hurts in FRC software. Read it before §7 here.
- [`../team-ops/05_business_awards_sustainability.md`](../team-ops/05_business_awards_sustainability.md)
  — where the awards/business hours in §8 come from.
- [`../../INDEX.md`](../../INDEX.md) · [`../../KICKOFF_PLAYBOOK.md`](../../KICKOFF_PLAYBOOK.md)

| Label | Meaning |
|---|---|
| **[C]** CONFIRMED | Fetched from the vendor's own page on the date shown, or executed locally |
| **[H]** HISTORICAL-PATTERN | Prior-season behaviour; not stated for 2027 |
| **[S]** SPECULATION | Model output or inference. Flagged. Do not act on it as fact |
| **UNVERIFIED** | Could not be checked from a primary source; go check before you spend |

> **Prices move.** Every dollar figure carries a verification date. **Re-verify anything you are about
> to put on a purchase order.** A price quoted here in August 2026 is evidence, not a quote.

---

## §0 — Runnable 60-second workflow

Paste into **Git Bash** on Windows 11. Nothing here costs money or needs an account.

```bash
# Run from the root of this repository. Step 3 changes directory, so keep this path in WB.
WB="$(pwd)"

# 1. Is the BIOCORE manual live yet? (safe to run any day; it just probes the CDN)
bash tools/probe-2027-manual.sh

# 2. Any Team Updates you have not seen? (--watch prints only what is NEW since last run)
python tools/teamupdate-diff.py season 2027 --watch

# 3. Stand up the AI scaffolding in your ROBOT repo (not this analysis repo)
mkdir -p ~/biocore-2027/{robot,cad,strategy,scouting,business,ops/cron,docs}
cd ~/biocore-2027 && git init -q
printf '%s\n' '# CLAUDE.md — repo root' '' \
  'Team ####, FRC 2027 BIOCORE. Control system: **Systemcore**, WPILib **2027** (`org.wpilib.*`).' \
  'NEVER assume 2026 APIs. Verify every WPILib call against https://docs.wpilib.org/en/2027/ .' \
  'AI-assisted work carries the attribution line in ops/ATTRIBUTION.md (FIRST requires credit).' \
  'No AI-authored number may describe physical reality (gains, limits, ratios, dimensions).' > CLAUDE.md
git add -A && git commit -qm "scaffold: repo + root CLAUDE.md" && echo "OK: $(pwd)"

# 4. Adopt the policy (edit the blanks, then have mentor + students sign it)
cp "$WB/reference/ai-integration/templates/team-ai-policy.md" \
   ~/biocore-2027/docs/TEAM-AI-POLICY.md
```

Four commands. The rest of this file explains what to do next and what it costs.

---

## 1. The stack, at three price tiers

### 1.1 What was verified, and when

| Item | Figure | Label | Verified |
|---|---|---|---|
| Claude Free | **$0** | **[C]** | claude.com/pricing, 2026-08-22 |
| Claude Pro | **$17/mo** billed annually · **$20/mo** billed monthly; *includes Claude Code* | **[C]** | same |
| Claude Max 5× | **from $100/mo** | **[C]** | same |
| Claude Max 20× | higher tier of Max; **exact figure not shown on the page fetched** | **UNVERIFIED** | check before buying |
| Claude Team | **$20/seat/mo** annual · **$25/seat/mo** monthly; **2–150 seats**; *includes Claude Code and Claude Cowork* | **[C]** | same |
| Claude Team premium seat | **$100/seat/mo** annual · **$125** monthly | **[C]** | same |
| Claude Enterprise | seat price + usage at API rates; custom | **[C]** | same |
| **Claude for Nonprofits** | **$8/user/mo** Team plan for orgs **under 20 people** | **[C]** | claude.com/solutions/nonprofits, 2026-08-22 |
| Nonprofit eligibility | "registered 501(c)(3) organizations and their international equivalents, **as well as K-12 public and private schools**" | **[C]** | same |
| Nonprofit verification | ~2–3 minutes through partner **Goodstack** | **[C]** | same |

**Read that eligibility line twice.** K-12 public and private schools are named as eligible. If your
team sits under a school, or under a booster 501(c)(3), the **$8/seat/month** Team rate is very likely
available to you — a 60% cut off the $20 annual rate, and it includes Claude Code. **Verifying this
is the single highest-value hour in this document.** Do it in September, not in January.

### 1.2 API prices (for the automation in §4, not for chat)

Anthropic first-party API rates, per million tokens. **[C]** cached 2026-06-24 via the bundled
`claude-api` reference; re-check at the pricing page before budgeting.

| Model | Model ID | Context | Input $/MTok | Output $/MTok |
|---|---|---|---|---|
| Claude Opus 5 | `claude-opus-5` | 1M | $5.00 | $25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

Two cost levers that matter for a small team:

- **Batch API — 50% off** for anything not latency-sensitive. Every scheduled job in §4 qualifies:
  overnight Team Update summaries, Q&A triage, post-match log reports. **[C]**
- **Prompt caching** — a cached prefix is billed at a fraction of input rate. Your rule corpus, your
  `CLAUDE.md`, and the manual text are stable prefixes. Put stable content first, volatile content
  (today's date, this match's data) last, and verify with `usage.cache_read_input_tokens`. If that
  field reads zero across repeated runs, something in your prefix is changing — usually a timestamp. **[C]**

**[S] Realistic API spend for this team: $5–25/month.** The scheduled jobs in §4 process kilobytes,
not gigabytes. The only thing that would blow this up is looping a 500-page manual through Opus daily,
which you should not do — ingest it once, cache it, diff it.

### 1.3 Free and discounted programs worth an application

| Program | What you get | Eligibility | Label |
|---|---|---|---|
| **Claude for Nonprofits** | Team seats at **$8/user/mo** (<20 people) | 501(c)(3) + intl. equivalents + **K-12 public and private schools**; Goodstack verification | **[C]** 2026-08-22 |
| **Claude Free** | Claude + a usage-capped slice of Claude Code, $0 | Any account holder **18+** | **[C]** |
| **GitHub Education — Student Developer Pack** | GitHub Pro + Copilot for verified students | **13+** and enrolled in a degree- or **diploma-granting** program (a US high school qualifies) | **UNVERIFIED** — from GitHub community FAQ, not the official docs page. Confirm at education.github.com |
| GitHub Copilot **Student plan** | Changed from Copilot Pro to a distinct "Copilot Student" plan for verified students **as of 2026-03-12**; fewer features than Pro | verified students | **UNVERIFIED** — check before promising it to students |
| **GitHub Education — Teacher** | Copilot Pro + teacher toolkit | verified faculty at accredited schools | **UNVERIFIED** — same caveat |
| **GitHub Free** | Unlimited private repos, **GitHub Actions free on public repos** | anyone 13+ | **[C]** long-standing |
| **Google for Nonprofits / Workspace for Nonprofits** | Workspace Business Starter at $0; Gemini reported free for up to 2,000 users for enrolled nonprofits; up to ~75% off higher editions | 501(c)(3), TechSoup verification — **schools and government entities are explicitly excluded** | **[C]** on the school exclusion; **UNVERIFIED** on the 2,000-user Gemini figure |
| **Google Workspace for Education Fundamentals** | Free tier for qualifying schools — the route a school-based team actually takes | accredited institutions | **UNVERIFIED** — your district almost certainly already has it; ask IT, don't apply |
| **Microsoft 365 Education A1** | Free web-apps tier for schools | accredited institutions | **UNVERIFIED** |
| **Azure for Students** | Credit grant, no card | student verification; **age floor differs from GitHub's — check** | **UNVERIFIED** |
| Anthropic **API credits for researchers/nonprofits** | free API credits for high-priority scientific work | applications reviewed monthly | **UNVERIFIED** — an FRC team is a weak fit; do not plan on it |

**The trap worth naming:** Google for Nonprofits **excludes schools**. If your team is a school club,
that door is closed and you go through Workspace for Education instead. If your team is an independent
booster 501(c)(3), that door is open and the school one is not. **Pick the right door once.** Teams
lose an evening every year discovering this at the wrong end of an application form.

### 1.4 The three tiers

Costs assume the season runs **Sept 2026 → Apr 2027 (8 months)**.

#### Tier 0 — $0/month

| Component | Cost | Notes |
|---|---|---|
| Claude Free (mentor account) | $0 | Usage caps make sustained Claude Code work impractical |
| GitHub Free, public robot repo | $0 | Actions minutes free on public repos |
| VS Code + WPILib 2027 toolchain | $0 | Required regardless |
| AdvantageScope, Elastic, PathPlanner | $0 | Already the recommendation in `03_programming_stack.md` |
| Local scripts in `tools/` | $0 | 38 of them already exist and run offline |

**Season total: $0.** **[S] Honest assessment:** this tier is real and it is not a joke — the analysis
repo you already have was built with it. What it cannot do is sustained agentic work: the Free plan's
usage caps will stop you mid-task during build season, repeatedly, at the worst times. Use Tier 0 to
*prove the workflow* in September and October. Do not plan to run January on it.

#### Tier 1 — ~$25–60/month (**recommended default**)

| Component | Monthly | 8-month | Notes |
|---|---|---|---|
| Claude Team, nonprofit rate, 3 seats @ $8 | $24 | $192 | **If §1.3 verification succeeds.** Includes Claude Code |
| *…or* Claude Pro, 1 mentor seat, annual billing | $17 | $136 | Fallback if the nonprofit rate does not apply |
| Anthropic API for scheduled jobs (Haiku/Sonnet + batch) | $5–15 | $40–120 | §4 |
| GitHub Free | $0 | $0 | |
| **Tier 1 total** | **$24–39** | **$192–312** | |

**[S] Against the season budget:** `team_capacity.yaml` puts season planning total at **$11,500**
(registration $6,500 + robot discretionary $2,500 + the rest). Tier 1 at $312 is **2.7%** of that.
It buys the seats named in §2 and every automation in §4.

#### Tier 2 — ~$150+/month, **and only in burst**

| Component | Monthly | When | Cost |
|---|---|---|---|
| Claude Max 5× — one mentor / lead programmer | $100 | **Jan 9 – Apr 30 only** (4 mo) | $400 |
| Claude Team nonprofit seats × 3 @ $8 | $24 | Sept – Apr (8 mo) | $192 |
| API for automation, heavier during comp | $15–30 | Sept – Apr | $120–240 |
| **Tier 2 total** | — | — | **$712–832** |

**[S] The burst pattern is the actual recommendation.** Claude Max is a monthly subscription; there is
no reason to hold it in October when the shop is doing off-season drivetrain work. Buy Tier 1 from
September, add **one** Max seat on **January 9** for the person doing the most Systemcore/WPILib-2027
migration work, drop it after your last event. Season cost lands near **$700**, or **6.1%** of the
$11,500 planning total.

**Where the money comes from — say it out loud.** `team_capacity.yaml` sets
`robot_discretionary: 2500`, and the BOM gate in `tools/bom-builder.py` fails a BOM that exceeds it.
**Do not fund AI out of that line.** Software subscriptions are an operating expense; fund them from
the business/sponsorship line (see `../team-ops/05_business_awards_sustainability.md`) or as an
in-kind sponsor ask. A $700 subscription that quietly eats 28% of the robot budget is a bad trade —
that is a swerve module.

### 1.5 What to buy, in order

1. **September:** apply for the nonprofit/school rate. Free, ~3 minutes, potentially saves $200/season.
2. **September:** GitHub Education verification for every student who wants it, and for the mentor.
   Do this before the pack's annual re-verification lands mid-season.
3. **October:** Tier 1. Prove the §4 automations run unattended for a month before you depend on them.
4. **November 12** (Virtual Kit Release): confirm Tier 1 is still enough. It will be.
5. **January 9, kickoff morning:** add the Max seat. Not before.
6. **After your last event:** cancel the Max seat the same week. Put a calendar reminder in now.

---

## 2. Accounts and access for minors

This is the section most teams get wrong, in both directions — some by ignoring it, some by banning
AI outright out of vague fear. Neither is correct.

### 2.1 The hard constraint

> **"We require all users to be at least 18 years old to create and use a Claude account."**
> — Claude Support, *Minimum age requirement access restriction*, fetched **2026-08-22** **[C]**

There is **no parental-consent flow** and **no supervised-minor account type** for consumer Claude.
Enforcement is real: app stores share age signals with Anthropic, rollout is staged by US state, and
accounts showing minor-activity indicators can be disabled. **[C]**

**Consequence for a team of ~15 high-school students:** most of your students **cannot hold their own
Claude account.** That is not a policy preference you can weigh against convenience. It is the
provider's terms. A team that has 14-year-olds sign up "because the mentor said it was fine" is
one enforcement sweep away from losing accounts mid-build-season, and has quietly asked minors to
misrepresent their age — which is a worse look in front of a judge than not using AI at all.

### 2.2 Where the law actually sits

Practical, not alarmist:

| Regime | What it does | What it means for you |
|---|---|---|
| **COPPA** (US) | Verifiable parental consent to collect personal information from **under-13s** | Your students are mostly 14–18, so COPPA is usually *not* the binding constraint. It is the reason vendors set 13+ or 18+ floors in the first place |
| **FERPA** (US) | Governs **education records** held by a school | Binds if the team is a school program and you put graded work, IEP-adjacent info, discipline records, or student IDs into a third-party tool. **Robot code and scouting data are not education records.** A judging essay draft that names a student's disability *is* sensitive |
| **State minor-privacy / age-appropriate-design laws** | Varying | Why Anthropic's 18+ enforcement is rolling out state by state **[C]** |
| **District AI/acceptable-use policy** | Almost always stricter than any vendor's | **Read it before anything else in this file.** `00_FIRST_AI_POLICY_VERIFIED.md` already flags this: FIRST's permission does not override your district |

**[S]** The realistic risk to this team is not a regulator. It is (a) a district IT policy violation
that gets the tool banned mid-season, and (b) a parent who first learns about AI use from their child
rather than from you. Both are solved by the same thing: a one-page written policy sent home in
September. That is §6.

### 2.3 The workable model: mentor-held accounts, student-driven work

This model is compliant, and — importantly — it is *pedagogically better than students working alone*.

```
                MENTOR (18+, holds every account)
                        │
        ┌───────────────┼────────────────┐
        │               │                │
   Claude Team     GitHub org       Google/School
   seat(s)         (owner)          Workspace
        │               │                │
        │               │                │
   ┌────┴────────────────────────────────┴──────────┐
   │  THE PAIRED SESSION                            │
   │  Screen on the shop TV. Mentor at the keyboard │
   │  OR an 18+ student "driver". Under-18 students │
   │  own the problem: they state the goal, judge   │
   │  the output, and decide what gets committed.   │
   └────────────────────────────────────────────────┘
                        │
                 git commit --author=<student>
                 Co-Authored-By trailer + attribution line
```

**Rules that make it work:**

1. **Accounts are held by adults.** Mentor(s) plus any student who is genuinely 18+ (seniors, often
   2–4 of 15). Seats: **2–3 is enough** at Tier 1. **[S]**
2. **Under-18 students never log in to Claude.** They sit at the session, drive the thinking, and type
   into the editor. This is the substantive difference between "AI did the work" and "a student used a
   tool" — and it is the difference a judge will hear in the pit.
3. **Sessions are public by default.** In the shop, on the big screen, not on someone's laptop at home
   at 1 a.m. Reduces the temptation, and doubles as teaching.
4. **The commit records the human.** `git commit --author` names the student who owns the change;
   the AI attribution trailer records the tool. Both, always. §6.
5. **GitHub is the exception, and it is fine.** GitHub accounts are available at **13+**
   (**UNVERIFIED** as a current figure — confirm on GitHub's ToS page), so students *can and should*
   hold their own GitHub accounts under the team org. Code review, PRs, and issue threads are where
   students demonstrate ownership. Put them there.
6. **Never paste into a chat:** student full names + school + grade together, home addresses, phone
   numbers, medical/IEP information, photos of identifiable minors, or anything from a school SIS.
   Scouting data (team numbers, match results, robot capabilities) is public information and is fine.
7. **Mentor reviews history.** Whoever holds the account can see the conversation history. Say so up
   front in the policy; it is a supervision feature, not surveillance.

### 2.4 Consent, in one paragraph you can actually send

Put the template in §6 in front of parents in September with the season paperwork. It should say:
what tools the team uses, that accounts are held by adults, that students never enter personal
information, that all AI-assisted work is disclosed per FIRST's rules, and who to contact with
questions. **[S]** One page, one signature line. It takes an evening and it removes essentially every
version of this problem.

---

## 3. Repository and knowledge architecture

Two repos. Keep them separate — one is a durable analysis workbench, the other is a season artifact.

```
BIOCORE-Analysis/                              <- THIS repo: analysis workbench, already built
  INDEX.md  README.md  KICKOFF_PLAYBOOK.md  STRATEGY-RANKING-SYSTEM.md
  reference/  research/  manuals/  tools/  logs/
  CLAUDE.md                                    <- ADD THIS (see 3.2); it does not exist yet

~/biocore-2027/                                <- NEW: the season repo the students live in
  CLAUDE.md                    root context: team, season, control system, the hard rules
  README.md                    what this robot is, how to build it, AI attribution line
  .gitignore                   build/, .gradle/, *.wpilog, secrets
  .github/
    workflows/
      build.yml                gradlew build + test + spotlessCheck  (free on public repos)
      attribution-check.yml    fails a PR that touches src/ with no AI-disclosure trailer
    pull_request_template.md   "Which parts were AI-assisted?" + "Can you explain every line?"
  robot/                       the WPILib 2027 gradle project
    CLAUDE.md                  <- the most important CLAUDE.md in the tree
    build.gradle  vendordeps/
    src/main/java/frc/robot/
      Robot.java  RobotContainer.java  Constants.java
      subsystems/  commands/  util/
    src/test/java/frc/robot/
  cad/
    CLAUDE.md                  units, stock list, tooling limits, what the shop can actually make
    notes/                     design decisions in markdown, one file per mechanism
    exports/                   STEP/DXF handed to the vendor; never edited by hand
    onshape-links.md           links only — CAD lives in Onshape, not in git
  strategy/
    CLAUDE.md                  scoring model, archetype vocabulary, ranking rubric pointers
    game-analysis.md           filled on kickoff day from the manual ingest
    rules/                     rule extracts + open questions -> Q&A submissions
    decisions/ADR-0001-*.md    one file per irreversible decision, dated, with the alternative
  scouting/
    CLAUDE.md                  schema, what is public data, what never leaves the team
    schema.md                  generated by tools/scouting-plan.py schema
    data/                      CSV per event
    picklists/
  business/
    CLAUDE.md                  award vocabulary, character limits, attribution requirement
    impact/                    Impact Award essay + exec summary drafts
    leadership/                FIRST Leadership Award (due 2027-02-04)
    sponsors/                  contact log — NO personal contact details in git
    outreach-log.md
  ops/
    CLAUDE.md                  how the automation works and how to turn it off
    ATTRIBUTION.md             the exact attribution string, copy-pasted everywhere
    cron/
      probe.sh  teamupdate.sh  qa.sh  tba.sh  run-all.sh
      register-tasks.ps1       Windows Task Scheduler registration
    post-match-report.sh       WPILOG -> one-page match report  (see §4.5 — you must write this)
  docs/
    TEAM-AI-POLICY.md          <- copied from templates/team-ai-policy.md, signed
    onboarding.md              day-one guide for a new student
    curriculum/                the four sessions from §7
```

### 3.1 Why `CLAUDE.md` per directory

Claude Code reads `CLAUDE.md` from the repo root **and** from directories it works in. A single
root file becomes a 400-line wall that is stale by week 3. Per-directory files stay short, get read
by the person who owns that directory, and fail loudly when wrong.

**Rule of thumb: if a `CLAUDE.md` is over ~40 lines, it is doing two jobs. Split it.** **[S]**

### 3.2 What each `CLAUDE.md` contains

| File | Must contain | Must NOT contain |
|---|---|---|
| **root** | Team number; season = 2027 BIOCORE (FRC); control system = **Systemcore**; WPILib **2027**, `org.wpilib.*` not `edu.wpi.first.*`; "verify every API against docs.wpilib.org/en/2027/"; the attribution requirement; "no AI-authored physical numbers"; where the policy lives | Anything FTC. Never "Pollen", "StarterBot", or "Skill Builders" — those are BIOBUZZ |
| **robot/** | Language + framework; **the 2027 breaking-change list** (`robotInit()` gone, `set()`→`setThrottle()`, `Servo`/`Ultrasonic`/`Relay`/`Counter`/`SPI`/analog-gyro removed, one `Gamepad` class, `Rotation2d` getters now **wrapped**); vendordep versions actually installed; the subsystem pattern you chose; "current limits and soft limits are human-set, never generated"; how to run tests | Gains, gear ratios, or field dimensions. Those live in `Constants.java` and come from measurement |
| **cad/** | Units (mm vs in — pick one, write it down); stock the shop actually has; tooling ceiling (`tooling.level: bandsaw_drillpress` per `team_capacity.yaml` — **no mill, no CNC router, no lathe in-house**); outsourcing lead time (2 weeks) and budget ($400); "CAD lives in Onshape; git holds notes and exports only" | Any claim that the team can machine something it cannot |
| **strategy/** | Pointers to `STRATEGY-RANKING-SYSTEM.md` and `reference/03_ARCHETYPE_CORPUS.md`; the rule-citation format (`G###`/`R###`); "the manual is the authority, this repo is commentary"; that rules = manual + Team Updates + Q&A | Rule text pasted from a prior season |
| **scouting/** | The schema; what is public (match results, team numbers, robot capability) vs. private (your own picklist reasoning); "no personal names of other teams' students" | Any picklist you do not want leaked |
| **business/** | Award character limits (2026 calibration: **500-char** exec summary, **10,000-char** essay — **re-verify for 2027**); deadlines (Leadership + WFF **2027-02-04**, Impact **2027-02-11**); the FIRST attribution requirement, quoted; "essays state what students did, in students' voice" | Sponsor contacts, dollar amounts of pending asks |
| **ops/** | What each scheduled job does, when it runs, where output lands, and **how to disable it**; that jobs are read-only against FIRST's servers | API keys. Ever. Use environment variables |

### 3.3 Secrets

`.env` in `.gitignore`, never a key in a `CLAUDE.md`, never a key in a commit. On Windows, set the
key for your user account once:

```bash
# Git Bash — sets a persistent user-level environment variable, then re-open the shell
setx ANTHROPIC_API_KEY "sk-ant-..." >/dev/null && echo "set; reopen Git Bash"
```

TBA needs its own key (`TBA_AUTH_KEY`) for the `tba_*.py` scrapers in `tools/`.

---

## 4. Automation — what runs on a timer

**Principle:** automate *monitoring*, not *judgement*. A scheduled job should tell you something
changed. A human decides what it means. **[S]** Every job below is read-only against FIRST's servers
and polite about it.

### 4.1 The schedule

| Job | Command | Cadence | Why |
|---|---|---|---|
| Manual/CDN probe | `bash tools/probe-2027-manual.sh` | Daily 07:00 → **hourly from Jan 5**, then a 2-min loop on kickoff morning | The CDN has container listing disabled; you must guess filenames. First to know = first to plan |
| Team Update diff | `python tools/teamupdate-diff.py season 2027 --watch` | Daily 07:05, Jan–Apr | 23 Team Updates shipped in 2026. Each can silently redefine a rule you designed around |
| Q&A scrape | `python tools/frc_qa_scrape.py --out manuals/archive/supplemental/2027_QA --season 2027` | Daily 07:10, Jan–Apr | The Q&A is part of the rules. Feeds `tools/qa-rule-heat.py` |
| TBA pull | `python tools/tba_predictive_scrape.py 2027 --out research/predictive_tba/` | Weekly Sun 08:00, then **daily during competition weeks** | Event results, OPR/COPR, scouting inputs |
| TBA COPR | `python tools/tba_copr_scrape.py 2027 --out research/predictive_tba/` | Weekly, competition season | Component OPRs for picklist work |
| Post-match log report | `bash ops/post-match-report.sh <match.wpilog>` | Manually, after every match | §4.5. Named student, 5 minutes, every match |
| Attribution check | GitHub Actions on every PR | per PR | §6 compliance, free |

**Cost:** the probe/diff/scrape jobs are pure Python + curl — **$0**. Only the optional "summarise
what changed in plain English" step calls the API, and at batch rates on Haiku that is cents.

### 4.2 Wrapper scripts (Git Bash)

`ops/cron/probe.sh`:

```bash
#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # repository root: this file is in ops/cron/
LOG="$ROOT/logs/probe-$(date +%Y%m%d).log"
cd "$ROOT" || exit 1
{ echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="; bash tools/probe-2027-manual.sh; } >> "$LOG" 2>&1
```

`ops/cron/teamupdate.sh`:

```bash
#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # repository root: this file is in ops/cron/
cd "$ROOT" || exit 1
OUT="$(python tools/teamupdate-diff.py season 2027 --watch 2>&1)"
# --watch prints ONLY what is new since the last run, so a short output means nothing changed.
if [ "$(printf '%s' "$OUT" | wc -l)" -gt 2 ]; then
  printf '%s\n' "$OUT" | tee -a "$ROOT/logs/teamupdate-$(date +%Y%m%d).log"
  # optional: notify. Replace with your Discord/Slack webhook, or leave it printing to the log.
  # curl -s -X POST -H 'Content-Type: application/json' \
  #   -d "$(printf '{"content": %s}' "$(printf '%s' "$OUT" | head -c 1800 | python -c 'import json,sys;print(json.dumps(sys.stdin.read()))')")" \
  #   "$DISCORD_WEBHOOK_URL" >/dev/null
fi
```

`ops/cron/run-all.sh`:

```bash
#!/usr/bin/env bash
set -uo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$D/probe.sh"
bash "$D/teamupdate.sh"
bash "$D/qa.sh"
[ "$(date +%u)" = "7" ] && bash "$D/tba.sh"   # Sundays only
exit 0
```

### 4.3 Registering with Windows Task Scheduler

**Git Bash mangles `/TN`-style arguments** — MSYS path conversion rewrites anything starting with `/`
into a Windows path. Two working options:

**Option A — PowerShell registration (recommended; the payload is still bash).** Save as
`ops/cron/register-tasks.ps1`, run once from PowerShell:

```powershell
$bash = "C:\Program Files\Git\bin\bash.exe"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path   # repository root, two levels above ops/cron
$fwd  = $repo -replace '\\', '/'                                # same path with forward slashes, which Git Bash accepts
$act  = New-ScheduledTaskAction -Execute $bash `
        -Argument "-lc `"cd '$fwd' && bash ops/cron/run-all.sh`"" `
        -WorkingDirectory $repo
$trg  = New-ScheduledTaskTrigger -Daily -At 7:00am
$set  = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 20)
Register-ScheduledTask -TaskName "BIOCORE\daily-watch" -Action $act -Trigger $trg `
        -Settings $set -Description "FRC 2027 manual/TU/Q&A watch" -Force
```

Verify and run it once by hand:

```powershell
Get-ScheduledTask -TaskName "daily-watch" -TaskPath "\BIOCORE\" | Get-ScheduledTaskInfo
Start-ScheduledTask -TaskName "daily-watch" -TaskPath "\BIOCORE\"
```

**Option B — `schtasks` from Git Bash**, with path conversion disabled:

```bash
MSYS_NO_PATHCONV=1 schtasks /Query /TN "BIOCORE\daily-watch" /V /FO LIST | head -20
MSYS_NO_PATHCONV=1 schtasks /Run   /TN "BIOCORE\daily-watch"
MSYS_NO_PATHCONV=1 schtasks /Delete /TN "BIOCORE\daily-watch" /F     # to remove
```

Without `MSYS_NO_PATHCONV=1` (or doubling the slash as `//TN`), Git Bash turns `/TN` into
`C:/Program Files/Git/TN` and the command fails with a confusing error. **[C]** — this is standard
MSYS2 argument-conversion behaviour; test it on your machine before the season depends on it.

### 4.4 Kickoff morning — 2027-01-09

The manual drops at 12:00 p.m. ET. Do not sit refreshing a browser:

```bash
# Run from the repository root.
until [ -s manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf ]; do
  bash tools/probe-2027-manual.sh --download
  sleep 120
done
bash tools/ingest-manual.sh "manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf" V1
python tools/rule-inventory.py --years 2027
```

Loop on **file existence**, not on the script's exit code — `probe-2027-manual.sh` reports per-URL
status and you should not assume its exit semantics. Full sequence: `KICKOFF_PLAYBOOK.md`.

### 4.5 Post-match log reports — **you have to write this one**

No tool in `tools/` does this today. **Do not pretend otherwise.** The spec, so a student can build it
in the off-season as a genuinely good first project:

```
INPUT   a .wpilog from the match (AdvantageKit or DataLogManager output)
OUTPUT  ops/reports/<event>-<match>.md, one page:
          - match number, alliance, final score
          - per-mechanism: commanded vs. achieved, count of setpoint misses
          - brownout events (bus voltage < threshold) with timestamps
          - CAN error counts / device dropouts
          - cycle count and mean cycle time  (feeds tools/cycle-model.py)
          - top 3 anomalies, ranked, with timestamps to scrub to in AdvantageScope
WHO     one named student, 5 minutes, every match. Not the whole team.
AI ROLE writing the parser is a good AI task (mechanical, verifiable).
        Interpreting the anomalies is NOT — that is the student's job and it is
        the part a judge will ask about.
```

**[S] Value:** `03_programming_stack.md` already calls this out as "how a small team looks like a big
one." Six matches a day × 5 minutes beats one person watching video for two hours.

---

## 5. MCP and integrations

**MCP (Model Context Protocol)** lets Claude read from and act on external systems. Wire up the ones
that remove typing; skip the ones that just look impressive.

| Integration | What it unlocks | Verdict | Risk |
|---|---|---|---|
| **Filesystem + Bash** | Reading the repo, running `tools/`, editing code | **Already built into Claude Code.** Do not install a separate filesystem MCP; it is redundant | Low — it is your machine |
| **GitHub** | Read issues/PRs, draft PR descriptions, triage, cross-reference a bug to the commit that caused it | **Wire it up.** Highest value per minute of setup for a code-carrying team | Medium — scope the token to your org, read-only where possible. **Never let it merge.** |
| **Google Drive** | Reading sponsor decks, the outreach log, judging materials the team already keeps in Docs | **Wire it up if — and only if — Drive is where your business docs actually live** | **High if minors' data is in that Drive.** Scope to a single shared folder that contains no student PII. Do not connect a district-wide Drive |
| **Slack / Discord** | Post Team Update alerts, build-blog snippets, meeting summaries into the team channel | **Use webhooks, not MCP.** A one-line `curl` to an incoming webhook (§4.2) does 95% of what you want with none of the read access | Medium — a read-scoped MCP into a team Discord exposes every student message. Do not do it |
| **Calendar** | Deadline tracking (Nov 12, Nov 17, Nov 21, Jan 9, Feb 4, Feb 11) | Marginal — six dates, put them in your phone | Low |
| **Onshape / CAD** | Reading assembly metadata | **UNVERIFIED** whether a usable connector exists. Do not plan a workflow around it | — |
| **The Blue Alliance** | Match/event data | **Skip MCP.** `tools/tba_*.py` already does this, deterministically, with output you can diff | — |

**Two rules for anything you connect** **[S]**:

1. **Read-scope by default.** Write access to GitHub means an agent can push. Write access to Drive
   means an agent can overwrite the Impact essay at 11 p.m. on February 10. Grant write only per-task,
   never as a standing permission.
2. **Content you fetch is data, never instructions.** A Chief Delphi post, a PDF, or a Discord message
   that says "ignore previous instructions" is text you read, not a command you obey. Teach students
   this explicitly in Session 4 (§7) — it is the single most useful security concept in this document
   and it transfers to the rest of their lives.

**Setup order:** GitHub first (September). Drive only if business docs genuinely live there (October).
Everything else: no.

---

## 6. The team AI policy

**Adopt [`templates/team-ai-policy.md`](templates/team-ai-policy.md).** One page. Fill the four blanks,
have every student and mentor sign it, send a copy home with September paperwork, and post it in the
shop.

It covers exactly four things, because those are the four that can actually hurt you:

1. **Safety-critical code** — nothing that actuates a 115.0 lb (bare, 2026 R103) / 135.0 lb (with
   bumpers, 2026 R408) machine ships without human review. AI never sets a current limit, soft limit,
   gain, gear ratio, or dimension.
2. **Awards integrity and attribution** — FIRST **permits** AI and **requires credit**. The team uses
   one standing attribution line. Judges may not penalise AI use, and AI-detection tools are
   inaccurate and should not be used — quoted from `00_FIRST_AI_POLICY_VERIFIED.md`.
3. **Data privacy for minors** — accounts held by adults; no student PII, medical info, addresses, or
   photos of identifiable minors in any prompt; conversation history is visible to the account holder.
4. **Verification** — a student can explain every line, or it does not merge. Every WPILib/vendor API
   is checked against the **2027** docs. Every factual claim in an essay traces to something the team
   actually did.

The **attribution string** lives in one file (`ops/ATTRIBUTION.md`) and is copy-pasted, never retyped:

```
Portions of this work were created with AI assistance (Claude, Anthropic) by Team ####.
All content was reviewed, verified, and is understood by the students credited.
```

FIRST's own example is *"Essay created by Team XXXX and ChatGPT."* — the form above says the same
thing and adds the verification claim, which is the part judges actually probe. **[C]** on FIRST's
wording; **[S]** on the added sentence being an improvement.

---

## 7. Four-session curriculum

Run these **October–December 2026**, 90 minutes each, before kickoff. Target: every student can use
the tool honestly and none of them outsource their thinking. Sessions cost **0 build hours** —
`team_capacity.yaml` allocates `strategy_rules: 25.0` h and `awards_business: 44.9` h across the
season; this training runs in the off-season, *before* that clock starts.

### Session 1 — "It is a very fast intern with no hands and no memory of your robot" (90 min)

| Segment | Min | Content |
|---|---|---|
| Live demo: good task | 15 | Generate a `SubsystemIO` interface + a sim implementation from a description. It works. Students see the win |
| Live demo: bad task | 15 | Ask it for the kV of your actual flywheel. It answers with a confident number. **The number is fabricated.** Then run SysId and show the real one. *This is the most important 15 minutes of the four sessions* |
| The 2027 trap | 20 | Ask for a WPILib subsystem. Watch it emit `edu.wpi.first.*`, `robotInit()`, `XboxController`. Show it failing to compile. Explain: every FRC example ever written is now wrong |
| Policy read-through | 20 | Read `docs/TEAM-AI-POLICY.md` aloud. Everyone signs |
| Hands-on | 20 | Each student writes one prompt, runs it, and writes one sentence on what was wrong with the output |

**Exit check:** every student can name one task AI does well and one it does badly, from having seen it.

### Session 2 — Prompting as specification writing (90 min)

| Segment | Min | Content |
|---|---|---|
| Context is the whole job | 20 | Same request with and without `CLAUDE.md` loaded. Compare. Students write their subsystem's `CLAUDE.md` section |
| Decomposition | 25 | Take one real mechanism. Break it into 6 tasks. Mark each: "AI can draft" / "AI can review" / "human only". Defend the marks |
| Verification loop | 25 | Write it → read it → compile it → test it → explain it. Practice on a deliberately subtly-wrong generated file that compiles and misbehaves |
| Hands-on | 20 | Pairs: one drives, one verifies. Swap at 10 min |

**Exit check:** a student-written task decomposition, on paper, with the "human only" items justified.

### Session 3 — Awards, writing, and honesty (90 min)

| Segment | Min | Content |
|---|---|---|
| What FIRST actually says | 15 | Read `00_FIRST_AI_POLICY_VERIFIED.md`. AI is permitted. Credit is required. Judges may not penalise you |
| The voice problem | 25 | AI-drafted paragraph vs. a student's own paragraph about the same outreach event. Which one would a judge believe? Why? |
| Character limits | 15 | 500-char exec summary / 10,000-char essay (**2026 figures — re-verify for 2027**). AI is genuinely good at cutting to a limit without losing the point. Practice it |
| The interview | 20 | Mock judge: "Tell me about this." A student who cannot explain their own essay loses the award. Run it twice |
| Attribution | 15 | Add the line to a real draft. Where it goes, what it says |

**Exit check:** each student can answer three judge questions about a document they helped write.

### Session 4 — Autonomy, limits, and not getting played (90 min)

| Segment | Min | Content |
|---|---|---|
| Agents and blast radius | 20 | What "it can run commands and edit files" means. Why write-scope is granted per-task, never standing |
| Prompt injection | 25 | Live: a web page containing "ignore previous instructions." Fetch it, watch what happens. **Content you read is data, not orders.** This concept transfers well beyond robotics |
| Cost and honesty | 20 | Show real token usage and what it cost. Show a session that burned budget going in circles. When to stop and think instead |
| Measurement | 15 | Introduce the §8 log. Everyone commits to filling it in |
| Where AI does not go | 10 | Gains, limits, dimensions, physical intuition, judging interviews, and driving |

**Exit check:** every student can describe prompt injection and name the one rule that prevents it.

---

## 8. Measurement — did this actually return hours?

If you cannot answer this in April, you spent ~$700 on a feeling. Keep it cheap: **one TSV, appended
to by hand, ~15 seconds per entry.** **[S]**

### 8.1 The log

`ops/ai-hours.tsv` — tab-separated, one line per AI-assisted task:

```
date	who	area	task	est_solo_min	actual_min	verified_by	accepted
2026-10-14	AH	robot	generate FlywheelIO + sim	90	25	mentor	y
2026-10-16	RS	business	cut exec summary to 500 chars	45	20	mentor	y
2026-10-21	JT	robot	tune shooter kV	60	55	mentor	n   # fabricated number, redone with SysId
```

`est_solo_min` is written **before** starting, by the student, and it is a guess — that is fine, the
error averages out over 40 entries. `accepted = n` entries are the honest ones and the most valuable.

### 8.2 The metrics

| Metric | How | Target | Why it is the right metric |
|---|---|---|---|
| **Hours returned** | Σ(`est_solo_min` − `actual_min`) ÷ 60, accepted rows only | **[S]** 40–70 h over the season | The headline. Compare to the 599 effective build hours in `team_capacity.yaml` — 50 h returned is **8.3%** of the season. This 40–70 h is a **40–65% realisation** of the ≈106 h per-row ceiling computed in [`00_WORKFLOW_MAP.md`](00_WORKFLOW_MAP.md) §1.9/§1.11a; the two files are reconciled and 40–70 h is the number to budget against |
| **Where they came from** | Group by `area` | Concentrated in `programming` (134.8 h budgeted) and `awards_business` (44.9 h) | If hours are coming out of `fabrication_assembly` (129.8 h), something is wrong — AI does not turn wrenches |
| **Rejection rate** | `accepted = n` ÷ total | **[S]** 15–30% is healthy | **Under 10% means nobody is checking.** Over 50% means you are using it for the wrong tasks |
| **Hours *reinvested*** | Drive-practice hours logged vs. the 54.9 h budgeted | ≥ budget | **This is the whole point.** Hours saved at a desk are only a win if they show up on the practice field |
| **Mentor unblock load** | Times the mentor was the blocker, per week | ↓ from baseline | `team_capacity.yaml` sets `mentor_unblock_hours_per_week: 3.4` — that is the scarcest resource on the team |
| **Cost per hour returned** | Total AI spend ÷ hours returned | **[S]** < $20/h | At $700 and 50 h that is $14/h. Compare honestly to $700 of aluminium |
| **Student explanation rate** | Spot-check at PR review: can they explain it? | **100%, non-negotiable** | Below 100% you have an awards problem and a safety problem, and no hours saved is worth either |

### 8.3 Kill criteria — decide these now, in August

**[S]** Write these down before you are emotionally invested:

- **Rejection rate > 50% for three consecutive weeks** → you are applying AI to tasks it cannot do.
  Cut back to boilerplate + documentation only.
- **Any student cannot explain merged code at a PR review** → the paired-session rule broke. Stop
  solo AI work entirely until Session 2 is re-run.
- **Fewer than 15 hours returned by 2026-12-15** → cancel the Tier 2 Max upgrade planned for
  January 9. The evidence is not there.
- **Drive practice below the 54.9 h budget in `team_capacity.yaml`** → the hours went somewhere other
  than the field. The investment failed on its own terms even if the log looks good.

### 8.4 Baseline — do this in September

Before turning anything on, log **two weeks of un-assisted work** in the same format
(`est_solo_min` = `actual_min`). Without a baseline the April number is unfalsifiable, and an
unfalsifiable number is exactly the kind of thing this project exists to avoid.

---

## 9. Season calendar

| Date | Action | Cost |
|---|---|---|
| **Sept 2026** | Read the district AI policy. Apply for the nonprofit/school Claude rate (Goodstack, ~3 min). GitHub Education verification. Send the signed policy home | $0 |
| Sept 2026 | Log the two-week un-assisted baseline (§8.4) | $0 |
| **2026-09-24** | Kit & Kickoff registration opens — unrelated to AI, but it is the hard gate. Do not let AI setup displace it | — |
| Oct 2026 | Buy Tier 1. Scaffold the season repo (§0). Wire GitHub MCP. Sessions 1 & 2 | ~$24–39/mo |
| Nov 2026 | Sessions 3 & 4. Prove §4 automations run unattended for 30 days | same |
| **2026-11-12** | Pre-Kickoff Virtual Kit Release — confirm Tier 1 still sufficient | — |
| **2026-11-17 / 11-21** | Kit selection closes / BOM order-by | — |
| Dec 2026 | Mid-point review against §8 metrics. **Decide the January Max seat on evidence** | same |
| **2027-01-09** | Kickoff. Run §4.4. Add the Max seat *today*, not before | +$100/mo |
| Jan–Apr 2027 | Daily watch jobs on. Post-match reports every match. Log every entry | Tier 2 |
| **2027-02-04 / 02-11** | Leadership + WFF / Impact submissions — attribution line on every one | — |
| Week after last event | **Cancel the Max seat.** Write the April retrospective from `ops/ai-hours.tsv` | back to Tier 1 |

---

## Validation

Everything here that can be checked, and how:

```bash
# Run from the repository root.

# 1. Every hours/dollar figure in this file traces to team_capacity.yaml
grep -nE "effective_build_hours|programming:|drive_practice|awards_business|fabrication_assembly|robot_discretionary|season_total_planning|mentor_unblock" reference/team_capacity.yaml

# 2. The tools cited in §4 exist and are runnable
for t in probe-2027-manual.sh teamupdate-diff.py frc_qa_scrape.py tba_predictive_scrape.py \
         tba_copr_scrape.py ingest-manual.sh rule-inventory.py cycle-model.py scouting-plan.py; do
  [ -f "tools/$t" ] && echo "OK   tools/$t" || echo "MISS tools/$t"
done

# 3. §4.3's Git Bash path-conversion claim, on YOUR machine
MSYS_NO_PATHCONV=1 schtasks /Query /FO LIST | head -5   # should list tasks
schtasks /Query /FO LIST | head -5                       # expected to fail or misbehave

# 4. Python and git are where §0 assumes
python --version && git --version
```

Executed 2026-08-22 on this machine: Python **3.14.6**, git **2.55.0.windows.2**, all nine tools
present. **[C]**

**Price re-verification, before any purchase:**

| Claim | Check at |
|---|---|
| Claude subscription tiers | `https://claude.com/pricing` |
| Claude for Nonprofits, $8/seat, school eligibility | `https://claude.com/solutions/nonprofits` |
| Claude API rates | `https://claude.com/pricing` (API tab) |
| Minimum age 18 | `https://support.claude.com/en/articles/13117299-minimum-age-requirement-access-restriction` |
| FIRST AI policy | `https://www.firstinspires.org/resources/library/frc/submitted-awards` |
| GitHub Education | `https://education.github.com` |
| Google for Nonprofits eligibility (schools excluded) | `https://support.google.com/nonprofits/answer/3215869` |

---

## Files written by this pass

| Path | Lines | What it is |
|---|---|---|
| `reference/ai-integration/05_ai_infrastructure_and_policy.md` | this file | The systems layer: cost, accounts, repo, automation, MCP, curriculum, measurement |
| `reference/ai-integration/templates/team-ai-policy.md` | ~90 | One-page team AI-use policy, ready to fill in and sign |

**Cross-links to add elsewhere** (not done by this pass, to avoid rewriting finished files):

- `INDEX.md` Track: add both files.
- `README.md` directory map: `ai-integration/` line currently reads "FIRST AI policy, verified" —
  extend to mention infrastructure/policy and the template.
- `00_FIRST_AI_POLICY_VERIFIED.md` §"What this policy does NOT do", item 4 currently says
  `05_ai_infrastructure_and_policy.md` **does not exist**. **It now does.** That sentence should be
  updated to point here — §2 of this file is the minors'-data and vendor-terms coverage it was
  looking for.

---

## Known limitations

1. **Prices are dated, not quoted.** Every figure carries a fetch date of 2026-08-22 or the
   2026-06-24 API cache. Vendors change pricing without notice. Re-verify before a PO. The
   Max 20× figure is **UNVERIFIED** — the pricing page fetch did not separate it from Max 5×.
2. **GitHub Education details are second-hand.** The 13+ / diploma-granting eligibility and the
   2026-03-12 "Copilot Student plan" change came from GitHub community discussion and secondary
   coverage, **not** from GitHub's official docs. Marked UNVERIFIED throughout. Confirm at
   `education.github.com` before telling a student they qualify.
3. **Microsoft and Azure programs are unverified.** Named for completeness with UNVERIFIED labels.
   Azure for Students' age floor in particular differs from GitHub's and was not checked.
4. **The Google-for-Nonprofits Gemini figure (2,000 users) is second-hand.** The *school exclusion*
   is confirmed and is the load-bearing fact; the user-count is not.
5. **Age enforcement is a moving target.** Anthropic's 18+ rollout is staged by US state as of
   2026-08-22. It may tighten. It is very unlikely to loosen. Plan on 18+.
6. **No FERPA/COPPA legal advice.** §2.2 is an orientation, not counsel. A district's own policy is
   what will actually be enforced against you, and it is stricter than anything here.
7. **`ops/post-match-report.sh` does not exist.** §4.5 is a specification, not a delivered tool.
   Nothing in `tools/` reads WPILOG files today. Do not schedule it until someone writes it.
8. **Hours-returned targets are [S].** The 40–70 h figure is an inference from
   `03_programming_stack.md` §11's *"plausibly worth 20–40% of programming labor on the mechanical
   parts of the job"* — itself explicitly flagged UNVERIFIED there — applied to the 134.8 programming
   hours in `team_capacity.yaml`. **No rigorous FRC-specific measurement of AI productivity exists.**
   That is precisely why §8 asks you to measure it yourself rather than trust this paragraph.
9. **The 2027 AI-reliability degradation is real and not modelled here.** Every FRC code example ever
   published uses the removed 2026 API surface. Expect AI help with WPILib to be *worse* in
   January 2027 than it was in 2026, and to stay worse until 2027 code exists publicly. If you are
   budgeting on the assumption that AI accelerates Systemcore migration, **do not.** Budget mentor
   hours for it instead, and treat any AI speedup as upside.
10. **MCP connector availability was not tested.** The GitHub/Drive/Slack rows describe what those
    integrations do in general. Whether a given connector is available and authorised on this machine
    was not verified — several MCP servers in this environment are unauthenticated.
11. **This file assumes one experienced technical mentor**, per `team_capacity.yaml`
    (`technical_mentors: 1`, `mentor_unblock_hours_per_week: 3.4`). A team with three mentors should
    buy more seats and re-run §8's cost-per-hour maths; a team with zero should not attempt Tier 2.
