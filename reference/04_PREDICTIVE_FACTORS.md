# Predictive Factors — what actually determines whether a 15-student team can pull a strategy off

**Purpose:** supply the achievability rubric with *measured* factor weights instead of invented ones.
Every weight below is anchored either to 30,986 team-event records scraped from The Blue Alliance
(2023–2026) or to a named, dated primary account. Where a factor could not be measured, it says so and
carries a lower weight for that reason. §12 gives the five weight moves you make after reading the
BIOCORE manual on 2027-01-09; §13 back-tests the whole instrument against five past seasons.

**Companion file:** `reference/04_predictive_factors.yaml`
(machine-readable weights + the game-conditional rules, consumed by `tools/rubric_weights.py`).

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
`RAPD` = 2022 RAPID REACT (136 pp). All in `manuals/archive/frc/`, with plain-text mirrors in
`manuals/archive/frc/_txt/`. Team Updates in `manuals/archive/supplemental/`. None of these is in the
repository, because FIRST's text is not redistributed: from the repository root,
`bash tools/rebuild-corpus.sh --fetch` downloads the PDFs and `bash tools/rebuild-corpus.sh` rebuilds
the text.
`TBA` = the four seasons of scraped Blue Alliance event pages in `research/predictive_tba/`.

> **Scope guard.** BIOCORE is **FRC**. Nothing in this document draws on FTC BIOBUZZ. BIOCORE's
> scoring element, field and rules are **not public as of 2026-08-22**; every game-specific number
> here is from a *prior* FRC season and is labelled `[H]` or `[C]`-for-that-season, never
> `[C]`-for-BIOCORE. See [`research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md).

---

## 0. Kickoff-day 60-second workflow

Paste this at 12:05 p.m. ET on **2027-01-09**, once the manual PDF is on disk. Every command below was
run against `REB` and `REEF` while writing this document; the outputs quoted in §13 are verbatim.

```bash
# Run from the repository root.
M="manuals/2026-27_BIOCORE/BIOCORE_GameManual.pdf"      # <- the file you download at 12:00 ET

# ---- 1. the weights, straight off the manual (~20 s) --------------------------
# On kickoff day you have no match data yet, so omit --typical-score.
python tools/rubric_weights.py "$M"

# After Week 1 of competition, re-run with the real median alliance score to
# finish the defense term (see step 6):
# python tools/rubric_weights.py "$M" --typical-score 143.3

# ---- 2. flatten once for the eyeball checks ----------------------------------
pdftotext -layout "$M" - | tr -s ' \n' ' ' > /tmp/b.txt

# ---- 3. THE SINGLE MOST IMPORTANT LINE: is defense legal where points happen? -
# A protection rule with NO time window kills defense. One that says "during the
# last N seconds" costs a defender almost nothing. See Sec 9.
grep -oE "[A-Z][A-Z/ ]{2,28} protection\.[^.]{0,240}" /tmp/b.txt | sort -u

# ---- 4. is there a possession cap? (the strongest playing-field leveler) ------
grep -oiE "may not (simultaneously )?CONTROL more than [0-9]+ [A-Z]+" /tmp/b.txt | sort -u
# no output  ==  uncapped cycle game  ==  elite teams run away; see Sec 4.4

# ---- 5. is any Ranking Point gated on AUTO? (moves auto weight +25) ----------
grep -oiE "\b(AUTO[A-Z]*|Autonomous)[ -]?(RP|BONUS|Ranking Point)\b" /tmp/b.txt | sort -u
grep -oE "[A-Z][A-Za-z]{3,14} (RP|BONUS)\b" /tmp/b.txt | sort | uniq -c | sort -rn | head -8

# ---- 6. the defense cost terms ----------------------------------------------
grep -oE "There.s a [0-9]+-count on PINS" /tmp/b.txt | sort -u     # 5s permissive / 3s tight
grep -oE "a credit of [0-9]+ points" /tmp/b.txt | head -2          # minor foul, then major foul
grep -oE "1 defender at a time[^.]{0,180}" /tmp/b.txt | head -1    # present only in REEF so far
```

**Read the output in this order:** step 3 first (it decides whether the whole defense-first branch of
the rubric is live), then step 4 (it decides whether the ceiling is reachable at all), then step 5.
Steps 1 and 6 are bookkeeping.

---

## 1. The evidence base — what was measurable, and what was not

| Source | Status | What it gave |
|---|---|---|
| The Blue Alliance public event pages | **[C]** scraped OK | 30,986 team-event rows, 770 events, 2023–2026: rank, Avg Match, Avg Auto, DQ, Played, W-L-T, plus every alliance-selection slot |
| FRC manuals 2022–2026 | **[C]** in corpus | exact G-rule text for every defense, pin and protection rule |
| Chief Delphi | **[C]** fetched via `tools/cd_fetch.py` | 14 topics, named + dated mentor and student accounts |
| Vendor list prices | **[C]** fetched 2026-08-22 | drivetrain cost ladder (§5.1) |
| **Statbotics API** | **UNVERIFIED — hard down** | component (auto/teleop/endgame) EPA. `GET https://api.statbotics.io/v3/team_year/254/2025` → **HTTP 500**, as did `/v3/team_years`, `/v3/events`, `/v3/year/2025`. `/v3/` root returns 200, so the service is up and the data endpoints are broken. Re-probe before trusting §6 |
| **TBA API v3** | **UNVERIFIED — needs a key** | per-match breakdowns, which is the only route to a true breakdown/availability rate. `GET /api/v3/status` → **HTTP 401**. Get a key at [thebluealliance.com/account](https://www.thebluealliance.com/account) and §8 can be redone properly |

Two consequences you should hold onto:

1. **Reliability is measured through DQ, which is a weak proxy.** DQ counts *rule* disqualifications,
   not breakdowns. A robot that sits dead on the field for three matches shows up nowhere in this data.
   The DQ effect in §8 is therefore almost certainly an *under*-statement of what unreliability costs.
2. **"Matches played" carries no signal.** `pct_team_events_short_of_modal_played` is **0.0%** in all
   four seasons — FRC schedules everyone the same number of quals, and TBA reports the schedule, not
   attendance. Do not build an availability metric on it.

---

## 2. The recommended weights, in one table

Weights are 0–100 and are **relative to each other only**. They are not probabilities and do not sum
to anything. Tuned for: ~15 students, experienced mentor, below-median funding, no guaranteed full
practice field, no in-house CNC.

| # | Factor | **Weight** | Evidence | Single number that sets it |
|---|---|---:|:---:|---|
| 1 | **Drive practice / hours on a working robot before event 1** | **90** | [H] | Field output grows 24–38% Week 1→Week 5, and the median team's rank percentile moves **< 2 points**. Everyone improves; nobody gains |
| 2 | **Reliability** | **88** | [C] | One DQ drops pick probability from ~62% to 22–42% |
| 3 | **Scope discipline (mechanisms in the critical chain)** | **85** *(+10 if ≥8 scoring rows)* | [H] | A 10-link chain at 95% each is 60% reliable; 2 links is 90%. `REB`'s minimum viable chain was **5** |
| 4 | **Scoring output (avg match points)** | **80** | [C] | Best single predictor of being picked in all 4 seasons (AUC 0.80–0.87), beating qual rank and Ranking Score |
| 5 | **Event selection (field size)** | **70** *(context multiplier, not a per-strategy score)* | [C] | Same rank band, **3.1% vs 60.8%** pick probability between a 61+-team and a <36-team event |
| 6 | **COTS leverage** | **55** | [C] | A complete competitive robot is buyable for ~$1,500 over the KoP; a custom one cost a district-level team **$13k–$17k** |
| 7 | **Drivetrain choice (swerve vs tank)** | **45** | [H] | 90 of the 100 True-Everybot teams that captained an alliance in 2026 were **not** on swerve |
| 8 | **Auto capability** | **40** *(+25 if an RP is gated on AUTO)* | [C] | Partial correlation of auto points with rank, holding total score fixed: **0.04 / −0.04 / 0.26 / 0.06** — non-zero only in the one season with an AUTO RP |
| 9 | **Defense capability** | **35 base → 1–41 after the manual** | [C] | Winning alliances draw their second pick from the bottom half of the standings **72–85%** of the time |
| 10 | **Vision / localization** | **30** | [S] | Not independently measurable — Statbotics component EPA was down. Force multiplier on mechanisms that must already work |
| 11 | **Custom fabrication capacity** | **25** | [S] | Named as a hard gate on *top-tier* performance, not on the captain or second-pick paths this rubric targets |

### 2.1 What changed from the previous pass, and why

| Factor | Was | Now | Reason |
|---|---:|---:|---|
| Event selection | 60 | **70** | It is the largest measured effect in the entire corpus (up to 20×) and it costs zero build hours. Re-scoped as a context multiplier rather than a per-strategy row |
| Defense (`REB` back-test) | 17 | **26** | The v1 model counted protection *rules*; the v2 model reads their *time scope*. See §9.2 — this was a real modelling error, not a tuning tweak |
| Defense (`REEF` back-test) | 9 | **1** | Same fix, opposite direction |
| Drive practice evidence | growth 49.8–73.5% | **37.0–45.7%** | The old figure mixed District Championships and FIRST Championship into the "late" bucket, which inflates growth *and* guarantees a rank decline for reasons unrelated to the robot. §7 restricts to Weeks 1–6 |

---

## 3. Swerve vs tank for a small team — the 2026 state of the question

### 3.1 The module price barrier is gone. The rest of the barrier is not.

All prices list, per unit, fetched 2026-08-22.

| Item | Price | Note |
|---|---:|---|
| [REV 4in EasySwerve module](https://www.revrobotics.com/rev-21-3006/) | **$223.00** | encoder **not** included; "only four tools" to assemble |
| [REV 3in MAXSwerve module](https://www.revrobotics.com/rev-21-3005/) | **$275.00** | through-bore encoder included |
| [Thrifty Swerve module](https://www.thethriftybot.com/products/thrifty-swerve) | **$299.99** | magnetic encoder included; tread sold separately |
| [SDS MK4i module](https://www.swervedrivespecialties.com/products/mk4i-swerve-module) | **$365–$377** | encoder **not** included |
| [AndyMark AM14U6 KoP tank chassis](https://andymark.com/products/am14u6-6-wheel-drop-center-robot-drive-base-2025-frc-kit-of-parts-drive-base) | **$940.00** | 2 Toughbox Mini S, 6 HiGrip wheels, belts. No motors |
| [REV MAXSwerve motor + controller bundle](https://www.revrobotics.com/FRC/motion/maxswerve-system/) (per corner) | **$280.00** | |
| [CTRE Kraken X60](https://store.ctr-electronics.com/products/kraken-x60) | **$217.99** | educational price; **integrated** Talon FX controller |

**The headline:** 4 × EasySwerve = **$892**, which is *less than the $940 KoP tank chassis*. **[C]**
As of 2026-08-22 the cheapest COTS swerve modules cost less than the standard tank drive base.

**The headline is also misleading.** Swerve needs **8** motors and **8** controller channels where
tank needs 4–6, plus 4 absolute encoders and a competent gyro. Drivetrain BOM, comparable configs:

| Configuration | Modules/chassis | Motors + controllers | **Total** |
|---|---:|---:|---:|
| KoP tank, 6 × NEO + SPARK MAX | 940 | 255 + 600 | **~$1,795** |
| MAXSwerve + REV bundles | 1,100 | 1,120 | **~$2,220** |
| MK4i + Kraken X60 ×8 | ~1,460 | 1,744 | **~$3,204** |

So swerve is **1.2×–1.8× the drivetrain cost**, not the 3× it was five years ago — but the whole-robot
delta reported by an actual district-level mentor is larger than the BOM delta implies:

> "13K this year barely got us a full robot with a custom tank drive. With swerve drive we would have
> cost 17K." — [martinma, #14, 2026-03-11](https://www.chiefdelphi.com/t/516134/14) (+50), lead
> mechanical mentor, ~4 mentors / ~10 students / ~$20k annual budget. **[C]** as a first-hand account.

### 3.2 What the adoption data says

| Season | Swerve share | Source |
|---|---|---|
| 2023 | ~45–55% | thread opener recalling the prior year, [Karthik, 2024-03-04](https://www.chiefdelphi.com/t/457171) **[S]** |
| 2024 | **~71%** | [Percentage of Swerve Drives in 2024](https://www.chiefdelphi.com/t/457171), 166/185 events pit-scouted **[C]** for that dataset |
| 2025 | higher still; multiple **100%-swerve events** (ISR district, Sacramento Regional 34/34) | [Percentage of Swerve Drives in 2025](https://www.chiefdelphi.com/t/493648) **[C]** |
| 2026 | not re-collected; 118 states *"the community's feelings that swerve drive is the new floor is correct"* | [Sidoti, #9](https://www.chiefdelphi.com/t/521036/9) **[S]** |

Composition of the non-swerve remainder, 2025 week 2: **32.3% KitBot variants, 12.0% Everybot variants**
([yapple](https://www.chiefdelphi.com/t/493648/40)). **[C]** for that sample. Tank is not a legacy
population; it is substantially a *deliberate COTS-template* population.

### 3.3 The competitive delta — and the confound that eats it

The honest finding is that **no clean swerve-vs-tank performance study exists.** Statbotics does not
label drivetrain, so every published comparison is confounded: swerve teams are richer, larger and more
experienced teams. What is *not* confounded is this:

> 100 unique True-Everybot teams captained an alliance in 2026 (116 captaincies). **"Of those 100 teams,
> only 10 (10%) have currently been identified to have Swerve."**
> — [Sidoti, #14, 2026-05-20](https://www.chiefdelphi.com/t/521036/14) **[C]** with the author's own
> caveat that drivetrain characterisation was incomplete, so 10% is a floor.

Against that, the one event with a full drivetrain-by-pick-order breakdown:

> FMA Allentown 2024, 27 teams, 8 tank. *"There were no tank captains, and the first tank off the board
> was pick #8."* — [thatnameistaken, #69](https://www.chiefdelphi.com/t/457171/69) **[C]** for n=1 event.

Both are true. Tank still captains, in volume, every season. Tank also gets picked later at a given
event. The rubric should treat drivetrain as a **moderate** factor (45), well below practice and
reliability, because of the two accounts that matter most for a team with ~15 students:

> "A tank on a well practiced driver will always outperform a swerve with an inexperienced driver."
> — [John_Bottenberg, #32, 2024-03-04](https://www.chiefdelphi.com/t/457171/32) **[C]**

> "What struck me most is that a significant percentage of teams that have swerve really weren't
> utilizing it to its full potential… If an event had 50% swerve, I'd say maybe half of them were more
> effective at moving around the field than a tank chassis."
> — [Jarren_Harkema, #61, 2024-03-08](https://www.chiefdelphi.com/t/457171/61) **[C]**

And the cleanest decision rule anyone stated, which the rubric adopts verbatim:

> "You should pick your drivetrain for 3 reasons: It's the one you know how to build the best. It's the
> one you know how to program the best. It's the one you know how to drive the best. **None of those
> reasons have anything to do with the game.**"
> — [UnofficialForth, #22, 2026-01-16](https://www.chiefdelphi.com/t/510353/22) **[C]**

### 3.4 Has swerve become the LOW-risk choice? No — but it is no longer the high-cost one.

**[S]** Verdict for a 15-student team: swerve is now **low-cost and medium-risk**. The residual risk is
not money and not modules; it is *field-oriented control, pose estimation, and driver hours* — and 2027
resets the software stack (§6.3). The rubric should score a first-year swerve adoption in 2027 as a
**scope item competing with a mechanism**, not as a free drivetrain upgrade. `[H]` A team switching to
swerve in the same season it attempts a two-mechanism robot is spending its scope budget twice.

**Weight: 45.** [H] Justification: adoption is near-universal and the price barrier has collapsed, which
argues up; but every measured link from drivetrain to *outcome* is confounded, tank still produced 100
alliance captains in 2026, and both credible mentor accounts subordinate drivetrain to driver hours.
45 keeps it a real term without letting it dominate practice (90) or scope (85).

---

## 4. Scope — one mechanism excellently vs two adequately

### 4.1 The arithmetic nobody escapes

Mechanisms in a scoring chain are in **series**: intake → index → launch. One failure kills the match.

| Links in the chain | 95% each | 90% each |
|---:|---:|---:|
| 1 | 95.0% | 90.0% |
| 2 | 90.3% | 81.0% |
| 3 | 85.7% | 72.9% |
| 5 | 77.4% | 59.0% |
| 10 | **59.9%** | **34.9%** |

**[H]** This is arithmetic, not observation — but the observation matching it is unusually precise:

> "at minimum this year you need a chain of subsystems like intake - indexing - shooter kicker - shooter
> speed - aiming to play meaningfully. That is a minimum chain of **5** subsystems… For a higher level
> team the chain looks more like [10 items]… **we nailed 9 out of 10 subsystems perfectly on the first
> try**… We missed having sufficient ball agitation… One mistake / oversight out of 10 subsystems and
> hundreds of correct design decisions and now without coming up with a solution **we are the lower EPA
> percentile.**" — [martinma, #14](https://www.chiefdelphi.com/t/516134/14) **[C]**

A 90%-execution team landing in the lower EPA percentile is exactly what the 10-link row predicts.

### 4.2 What the community says the trade actually costs

> "the number one rule of frc robot design is build something simple. If only 1 mechanism is required to
> do the primary scoring task, build that mechanism, and make any and every change you can think of to
> that mechanism… **adding a second mechanism doubles the workload to get the same quality.**"
> — [Robogram, #3, 2026-05-07](https://www.chiefdelphi.com/t/520378/3) **[C]**

> "The less degrees of freedom, the less points of possible failure… my team this year opted out of
> having a turret because we weren't familiar with making and programming one, and we were set to go to
> a week 1 regional. Without having to spend the time working on a turret, we were able to make a super
> reliable static shooter with an adjustable hood." — [Indoraptor, #6](https://www.chiefdelphi.com/t/520378/6) **[C]**

### 4.3 What alliance captains actually pick — the measurement

Across 750 events, 2023–2026, ranking each event's teams by four public columns and computing the AUC
for "was this team picked", restricted to the contested middle of the field:

| Season | **Avg Match** | Qual rank | Ranking Score | Avg Auto | n events |
|---|---:|---:|---:|---:|---:|
| 2023 | **0.856** | 0.827 | 0.812 | 0.755 | 176 |
| 2024 | **0.872** | 0.826 | 0.821 | 0.731 | 180 |
| 2025 | **0.840** | 0.782 | 0.777 | 0.692 | 194 |
| 2026 | **0.801** | 0.798 | 0.783 | 0.700 | 200 |

Source: `research/predictive_tba/pf4_pick_auc.csv`. **[C]**

**Captains buy points, not rank and not Ranking Score.** In all four seasons the raw scoring column
separates picked from unpicked better than the qualification rank the field is literally sorted by. This
is the empirical answer to "does EPA reward reliability or ceiling": the *pick* rewards **average
delivered output**, which is a reliability-weighted quantity — a robot that scores 40 in nine matches
and 0 in three averages 30, and the captains see the 30.

One important counterweight, from the canonical alliance-selection guide:

> "if you are on the strong side of the bracket and going for a win, or if you are the 7/8 captain, you
> should **move the high-variance teams up** on your picklist a fair bit. You're probably not going to
> beat the strong alliances if you have 'consistent' partners that are consistently worse."
> — [Gettin' Picky, Part 2, #~30](https://www.chiefdelphi.com/t/361998) **[C]**

**[S]** Read together: consistency is what gets you picked by a *top* alliance; ceiling is what gets you
picked by a *desperate* one. For a 15-student team the first market is much larger.

### 4.4 The population check — does a deliberately-simple robot actually compete?

The Robonauts Everybot programme publishes hard counts. 2026 season, [Sidoti, #1 and
#14](https://www.chiefdelphi.com/t/521036): **[C]** for the published figures, with the author's stated
manual-classification caveat.

| Metric | 2026 value |
|---|---:|
| "True Everybot" builds (only Everybot mechanisms) | **441** |
| Everybot-inspired robots competing | 852 |
| Unique True-Everybot teams that captained an alliance | **100** (116 captaincies) |
| → captaincy rate | **22%** |
| True-Everybot event wins / finalists | **21 / 18** |
| Of the 100 captains, in the top 8 after quals | 44 |
| Of the 100 captains, average qualification rank | **9th** |
| Everybot-inspired teams founded 2018–25 still active in 2026 | **78%** |
| Non-Everybot teams founded 2018–25 still active in 2026 | **32%** |

Now put the 22% next to the population base rate, matched on events attended
(`research/predictive_tba/pf5_captaincy_base.csv`, **[C]**):

| Events attended, 2026 | n teams | % that ever captained |
|---|---:|---:|
| 1 | 852 | 9.2% |
| **2** | **1,639** | **21.8%** |
| 3 | 828 | 59.7% |
| 4+ | 380 | 79.7% |
| ALL | 3,699 | 33.3% |

**[S]** The Everybot event-count distribution is not published, so this is an inference, not a proof —
but a two-event team is the modal FRC team, and a deliberately one-to-two-mechanism robot captained at
**21.8% vs 22%**: *parity*. A robot built by a small team with common tools, a 3D printer and ~$1,500
performed at the population rate for its event count, and won 21 events.

That is the strongest single argument in this document for weighting scope discipline at 85 rather than
treating mechanism count as a ceiling to be maximised.

**Weight: 85, +10 when the manual offers ≥8 distinct scoring rows.** [H] The bonus fires because a wide
scoring table is precisely when the temptation to add mechanism #2 is strongest and the serial-reliability
penalty is worst. Back-tested in §13.

---

## 5. COTS vs custom — how much performance is buyable

### 5.1 The cost ladder

| Robot | All-in cost | Fabrication needed | Source |
|---|---:|---|---|
| **Everybot 2026** | **~$1,500 over the KoP** | *"only common tools, a basic 3D printer, items purchased from your local hardware store"* | [118, #1, 2026-01-10](https://www.chiefdelphi.com/t/510331) **[C]** |
| KitBot | in the Kickoff Kit | assembly only | [FIRST KitBot](https://www.firstinspires.org/resources/library/frc/kitbot) **[C]** |
| Custom tank, district-competitive | **~$13,000** | 2D sheet CNC/laser, tube CNC, 3D printing | [martinma, #14](https://www.chiefdelphi.com/t/516134/14) **[C]** account |
| Custom swerve, district-competitive | **~$17,000** | same | same |

**An order of magnitude separates the COTS path from the custom path, and the COTS path captained 100
alliances in 2026.** That is the quantification the rubric needs.

### 5.2 Where custom fabrication still pays

The same mentor lists the hard gates for *top-tier* performance — note that these are gates on the
elite tier, not on the captain/second-pick tier this rubric targets: **[C]** as a first-hand account,
**[S]** as a general law.

> "2D sheet CNC or laser cutting (in house **or the ability to fund outsourcing such as sendcutsend**)
> is essential… 2D tube CNC is critical to weight reduction… 3D printing is a requirement."

The parenthetical is the operative clause for a 15-student team: **outsourced 2D sheet substitutes for
in-house CNC.** In-house tube CNC does not have a cheap substitute, which is why custom fabrication
sits at 25 rather than lower — it is real, but it gates a tier the rubric is not aiming at.

### 5.3 The widening-gap context

An analysis of Statbotics EPA distributions 2016–2025, posted with graphs and code offered:
[mattd77, #1, 2026-03-11](https://www.chiefdelphi.com/t/516134) (+54). **[H]** — a community analysis
of prior seasons; the author disclosed AI assistance in writing the code and stated he verified the
numbers.

| Metric | 2016/2018 | 2025 |
|---|---:|---:|
| Share of total EPA held by the **bottom 50%** of teams | 41.5% (2018) | **26.5%** |
| Share held by the **top 10%** | 14.7% (2018) | **23.6%** |
| P90 / P50 EPA ratio | 1.38 (2018) | **2.35** |
| P10 / P50 EPA ratio | 0.62 (2016) | ~0.45 |

**[S]** Implication the rubric must encode: the gap to the top is widening, so a small team's realistic
target is **not** "close the gap" — it is the *event-selection* and *second-pick* paths (§9.3, §11),
both of which are measurably stable across the same period.

**Weight: 55 for COTS leverage, 25 for custom fabrication.** [C]/[S]

---

## 6. Auto and vision

### 6.1 Auto buys almost no rank beyond its face value — with one exception

Within each event, the Spearman correlation of a team's Avg Auto with its qualification rank, **holding
total match score constant** (`research/predictive_tba/pf4_auto_within_event.csv`, **[C]**):

| Season | Auto share of score | Spearman rank↔AvgMatch | Spearman rank↔AvgAuto | **Partial (auto \| total)** | AUTO-gated RP? |
|---|---:|---:|---:|---:|:---:|
| 2023 `CHRG` | 27.6% | 0.893 | 0.747 | **0.044** | no |
| 2024 `CRES` | 37.3% | 0.873 | 0.719 | **−0.044** | no |
| 2025 `REEF` | 19.6% | 0.838 | 0.724 | **0.259** | **yes — AUTO RP** |
| 2026 `REB` | 20.6% | 0.882 | 0.719 | **0.061** | no |

**The reading:** auto points are worth exactly their face value in the score, and nothing more —
*unless* a Ranking Point is gated on an autonomous accomplishment, at which point the partial
correlation jumps 4–6×. 2025 is the only season of the four with such an RP, and it is the only season
with a materially non-zero partial. **[C]** for the four seasons measured.

Confirming from the pick side: **Avg Auto is the worst of the four public predictors of being picked in
every single season** (§4.3 table, AUC 0.69–0.76 vs 0.80–0.87 for Avg Match).

### 6.2 What that means for a 15-student team

**[S]** Build the auto that scores the same game piece your teleop scores, from the same starting
position, and stop. Do not build a second auto path until step 5 of §0 shows an AUTO-gated RP. If it
does, auto moves from 40 to 65 and a multi-path auto becomes the highest-leverage software project of
the season.

### 6.3 Vision — and the 2027 control-system reset

Vision could not be measured independently: Statbotics component EPA is the only public source that
separates auto/teleop/endgame contribution, and it was **down** (§1). The one calibration point found:

> 3467 at a 2025 event — Auto EPA 15.4 vs scouted auto 15.7; Teleop EPA 49 vs scouted 47.0.
> — [Kevin_Leonard, #3](https://www.chiefdelphi.com/t/494190/3) **[C]** for n=1 team. Component EPA
> tracks scouted reality closely, which is why its absence is a real gap rather than a nuisance.

**The 2027-specific fact that changes this factor:** **[C]** as of 2026-08-14, per
[Latest controller information for FRC and FTC?](https://www.chiefdelphi.com/t/523342):

> "Will FRC use Systemcore in 2027? All guidance points to yes. That is the stated plan. **WPILib 2027
> is currently Systemcore-only.** However, there are no production units currently available and 2027
> kickoff is approaching." — paulonis, #3
>
> "The 27 WPILIB is **incompatible with the Rio**." — FrankJ, #4

Whether the roboRIO stays legal in 2027 is **UNVERIFIED** — FIRST has not announced it, and
[the 2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027)
does not say. Track it.

**[S]** Two-sided effect the rubric should encode:
- *Levelling:* every team's accumulated vision/odometry stack needs re-porting. The elite software
  advantage that §5.3 documents is partially, temporarily reset.
- *Risk:* a 15-student team has the least slack to absorb a platform migration in the same season it
  learns a new game. **Any 2027 strategy whose scoring depends on vision-based pose estimation should
  carry an explicit schedule-risk penalty in the rubric until SystemCore is in your hands and running.**

**Weight: auto 40 (+25 conditional); vision/localization 30.** [C]/[S]

---

## 7. Drive practice — the evidence that hours dominate sophistication

### 7.1 The whole field improves at the same rate

Mean event Avg Match score by week, indexed to that season's Week 1
(`research/predictive_tba/pf5_week_curve.csv`, **[C]**):

| Season | Wk1 | Wk2 | Wk3 | Wk4 | Wk5 | Wk6 | Champs |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 100 | 101 | 112 | 125 | **127** | 176 | 208 |
| 2024 | 100 | 100 | 113 | 125 | **124** | 170 | 226 |
| 2025 | 100 | 93 | 106 | 122 | **133** | 177 | 251 |
| 2026 | 100 | 104 | 116 | 139 | **138** | 167 | 353 |

Week 6 in 2023–2025 and Week 7 in 2026 contain District Championships, which are qualification-gated —
that is the jump. **Weeks 1→5 is the clean regular-season comparison: +24% to +38%.**

### 7.2 …which is why individual improvement buys no ground

For every team that played two regular-season events (Weeks 1–6 only, `pf5_early_late.csv`, **[C]**):

| Season | n teams | Their own output growth | **Δ rank percentile** | % that improved |
|---|---:|---:|---:|---:|
| 2023 | 2,372 | +37.0% | **+0.2** | 48.8% |
| 2024 | 2,543 | +39.6% | **+0.6** | 48.1% |
| 2025 | 2,702 | +45.7% | **−0.2** | 50.1% |
| 2026 | 2,653 | +40.3% | **−1.9** | 52.6% |

*(Rank percentile: 0 = best at the event, 100 = worst. Negative Δ = improved.)*

**This is the most important table in the document.** The median team gets 37–46% better between its
first and second event — and moves **less than two percentile points**, with the odds of improving at
all indistinguishable from a coin flip. In-season improvement is *universal*, therefore it is *not
competitive*. The only improvement that buys relative position is improvement that happens **before
event 1**, when the rest of the field is still improving on the shop floor.

**[H]** Causal caution: this shows in-season gains do not move relative rank. It does not directly prove
that pre-season driver hours *do*. No dataset of practice hours vs outcome exists — nobody records it.
The mechanism is inferred, and the supporting evidence is testimony:

> "A tank on a well practiced driver will always outperform a swerve with an inexperienced driver."
> — [John_Bottenberg](https://www.chiefdelphi.com/t/457171/32) **[C]**

> "So with this being our first year with swerve, I actually got no practice because we had lots of
> problems when building, so in our first comp I was not actually driving… (we didn't do too great on
> first comp)" — [MiguelV, #8, 2026-05-24](https://www.chiefdelphi.com/t/521233/8) **[C]**, a driver
> describing exactly the failure mode this factor is meant to price

The cheapest substitutes for a practice field, named by drivers in the same thread and costing nothing:
**field-oriented control in the simulator**, controller-in-hand mental rehearsal, and driving along with
recorded matches of a team that does it well. — [AssortedTrivial, #13](https://www.chiefdelphi.com/t/521233/13) **[C]**

**Weight: 90 — the highest in the table.** [H] It is the highest because it is the only factor whose
required input (hours) a 15-student, low-budget team can supply on equal terms with a 60-student,
well-funded one, *and* because the data shows the alternative — improving during the season — is worth
approximately nothing in relative terms.

---

## 8. Reliability

`research/predictive_tba/pf4_reliability.csv`, **[C]**:

| Season | team-events | % with ≥1 DQ | **% picked, no DQ** | **% picked, ≥1 DQ** | median rank %ile, no DQ | median rank %ile, ≥1 DQ |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 7,208 | 2.80% | 62.9% | **41.6%** | 48.9 | 75.7 |
| 2024 | 7,605 | 1.34% | 61.7% | **22.5%** | 50.0 | 86.0 |
| 2025 | 8,013 | 1.70% | 62.1% | **22.8%** | 49.1 | 86.4 |
| 2026 | 8,160 | 2.67% | 64.7% | **39.4%** | 49.2 | 74.6 |

A single DQ in a team's event roughly **halves** its probability of making a playoff alliance and moves
its median finish from the middle of the field to the bottom quartile. Consistent across four seasons
and 30,986 team-events.

**Read this as a lower bound, not the effect size.** DQ is a *rules* event. The mechanical failures this
factor is really about — a dead battery, a snapped intake, a robot that does not move — are invisible in
this dataset (§1). The true cost of unreliability is larger than the table shows.

Practitioner consensus on how reliability is actually bought
([How do you make a reliable robot](https://www.chiefdelphi.com/t/520378), **[C]** as testimony):
drive it into a wall at full speed on purpose; re-check every fastener every 30–60 minutes of driving;
run a written pre-match checklist; **make a spare of every part outside the frame perimeter**; overbuild
anything outside the frame perimeter and ignore its weight; design for repairability (access holes,
nothing that requires full disassembly).

**Weight: 88.** [C] Second only to practice, and above scope, because the effect is large, measured, and
consistent across four seasons — and because the measurement understates it.

---

## 9. Defense — is a defense-first strategy viable for a small team?

### 9.1 The payoff is real and it is growing

Rank percentile of each slot on the alliance that **won** the event
(`research/predictive_tba/pf5_winning_alliance.csv`, **[C]**; 0 = best, 100 = worst):

| Season | captain | 1st pick | **2nd pick** | **2nd pick from bottom half** |
|---|---:|---:|---:|---:|
| 2023 | 2.9 | 9.4 | **63.2** | **72.1%** |
| 2024 | 2.9 | 9.6 | **66.7** | **76.9%** |
| 2025 | 2.8 | 8.4 | **68.8** | **76.3%** |
| 2026 | 2.9 | 7.3 | **71.0** | **84.5%** |

The support/defense slot on the *winning* alliance is filled from the bottom half of the qualification
standings **72–85% of the time, and the trend is up.** For a 15-student team this is the single most
reachable banner path in FRC, and unlike almost everything else in this document it does not require
out-scoring anybody.

### 9.2 Whether the rules permit it is a per-season coin flip — and the old test was wrong

The first version of this model counted "`<THING>` protection" G-rules and charged −8 each. That model
ranked 2026 `REB` **third of five** for defense viability. The post-season community verdict was the
opposite:

> "defense really became a game-changer. especially with tactics like stealing and fuel deprivation"
> · "Defense was amazing this year which I really loved (**a lot better than 2025** lmao)"
> · "**Reminder that Reefscape had complaints of being defenseless.**"
> — [Post-Season reflect: How was Rebuilt?](https://www.chiefdelphi.com/t/519847) **[C]** as sentiment

Reading the actual rule text shows why the count was the wrong statistic. What matters is **whether the
protection covers the place the opponent scores, for most of the match**, or only an endgame structure
in the closing seconds:

| Season | Rule | Text that decides it | **Scope** |
|---|---|---|:---:|
| `RAPD` 2022 | HANGAR ZONE protection | *"protection **engaged 0:30**"* (ARENA timing table); G-rule reads *"during the **final 30 seconds**"* | endgame-only |
| `CHRG` 2023 | — | no protection rule exists | none |
| `CRES` 2024 | G422 PODIUM | *"**Prior to the last 20 seconds** of a MATCH, a ROBOT may not contact… an opponent ROBOT whose BUMPERS are in contact with their PODIUM"* | **teleop-wide** |
| `CRES` 2024 | G423 SOURCE/AMP ZONE | *"may not contact… if any part of either ROBOT'S BUMPERS are in the opponent's SOURCE ZONE or AMP ZONE"* — **no time window at all** | **teleop-wide** |
| `CRES` 2024 | G424 STAGE | *"during the last 20 seconds of the MATCH"* | endgame-only |
| `REEF` 2025 | G427 ZONE protection | *"may not contact… an opponent ROBOT partially or fully inside the opponent's **BARGE ZONE or REEF ZONE** regardless of who initiates contact"* — **no time window** | **teleop-wide** |
| `REEF` 2025 | G428 CAGE protection | *"during the last 20 seconds"* | endgame-only |
| `REB` 2026 | G420 TOWER protection | *"in contact with an opponent TOWER **during the last 30 seconds** of the MATCH"* | endgame-only |

**`REEF` protected the REEF ZONE — the primary CORAL scoring structure — for the entire match, and added
G421 "1 defender at a time" (*"No more than 1 ROBOT may be on the opponent's side of the FIELD"*), which
exists in no other season in this corpus. `REB` protected only the endgame climb, only in the last 30
seconds.** That is the whole story, and the rule count misses it entirely.

Supporting rule text worth knowing: both `REEF` G426 and `REB` G419 forbid *collusion* to shut down game
play but explicitly permit solo defense — `REB` G419 lists *"A single ROBOT blocking access to a
particular area"* as **standard gameplay, not a violation**. **[C]** A one-robot defensive play has been
explicitly legal in every season 2022–2026.

### 9.3 The v2 defense sub-model and its back-test

```
base 35
  + 10   if the PIN count is >= 5 seconds
  - 20   if ANY protection rule covers a scoring/loading area through TELEOP
  -  4   per endgame-only protection rule
  - 15   if a "1 defender at a time" rule exists
  - 10   if the MAJOR foul is >= 12% of a typical alliance score
  -  5      "     "        "     8-12%
  +  5      "     "        "     < 8%
```

| Season | PIN | teleop-wide protections | endgame-only | 1-defender | major foul % | **v2 weight** | v1 weight | Independent verdict |
|---|---:|---|---:|:---:|---:|---:|---:|---|
| `RAPD` 2022 | 5 s | — | 1 | no | n/a | **41** | 37 | defense-heavy season |
| `CHRG` 2023 | 5 s | — | 0 | no | 15.2% | **35** | 35 | defense-heavy season |
| `REB` 2026 | 3 s | — | 1 (TOWER) | no | 10.5% | **26** | 17 | *"defense was amazing this year"* |
| `CRES` 2024 | 5 s | PODIUM, SOURCE/AMP | 1 | no | 11.1% | **16** | 11 | scoring + loading both protected |
| `REEF` 2025 | 3 s | ZONE (REEF/BARGE) | 1 | **yes** | 6.9% | **1** | 9 | *"complaints of being defenseless"* |

v2 orders the five seasons **2022 > 2023 > 2026 > 2024 > 2025**, which matches the independent community
verdict; v1 put 2026 below 2023 by 18 points and had 2024 and 2025 nearly tied. The banded foul term also
removes a cliff: `REB`'s major foul is 10.5% of a typical score, 0.5 pp over v1's single 10% threshold,
which is not a difference the data can support.

**Weight: 35 base, 1–41 after reading the manual.** [C] The wide conditional range is the point — this is
the factor that swings hardest on rules you will not see until 2027-01-09.

---

## 10. Week-1 vs later-week — what it implies about scoping

Combine §7.1 and §7.2: a Week 5 field scores **24–38% more** than a Week 1 field, and a team that plays
both improves by **37–46%** over the same span, netting a rank-percentile change of **under 2 points**.

**[C]** for both measurements; **[S]** for the conclusion, which is that **the two effects cancel**, and
choosing a later first event is therefore approximately free in competitive terms while buying 4–5 extra
weeks of build and practice.

This inverts a common piece of folk wisdom. "Go to a Week 1 event because the field is weak" is half
right — the field *is* 24–38% weaker in absolute output — but you are weaker by the same proportion,
and rank is a within-event measure, so nothing is gained. What a Week 1 event actually does is move your
completion deadline forward by a month.

**Rubric implication:** score any strategy that requires a Week 1 event against a build calendar that is
**4–5 weeks shorter**. And note the compounding risk in 2027 specifically: a Week 1 event plus a
first-year SystemCore port (§6.3) is the highest-schedule-risk combination available.

One caveat, **[S]**: this is measured on teams that played *two* regular-season events. Teams that play
one event and choose Week 1 may differ systematically from those that choose Week 5. The 2023–2025
Week 6 buckets also contain District Championships, which is why §7.1 quotes Weeks 1→5 rather than 1→6.

---

## 11. Event selection — the largest measured effect in the corpus

Probability of being picked for a playoff alliance, by field size and rank band
(`research/predictive_tba/pf5_field_size_pick.csv`, all four seasons, **[C]**):

**Rank band 75–90% (bottom quarter, not last):**

| Field size | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| small (<36 teams) | **54.2%** | **53.2%** | **57.3%** | **60.8%** |
| medium (36–45) | 22.3% | 22.4% | 27.1% | 25.0% |
| large (46–60) | 8.2% | 10.9% | 12.9% | 15.6% |
| huge (61+) | 11.4% | 3.8% | 10.2% | **3.1%** |

**Rank band 50–66% (middle of the field):**

| Field size | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| small (<36 teams) | **84.1%** | **82.5%** | **76.9%** | **81.7%** |
| medium (36–45) | 50.4% | 50.5% | 52.6% | 53.8% |
| large (46–60) | 32.5% | 28.1% | 28.0% | 26.4% |
| huge (61+) | 28.8% | 30.2% | 33.3% | 25.5% |

**The same robot, at the same relative rank, is 3–20× more likely to play in the playoffs at a
sub-36-team event than at a 61+-team event.** The mechanism is trivial — 8 alliances take 24 teams
regardless of field size — but the magnitude dwarfs every robot-design factor in this document, it is
stable across four seasons, and it costs zero build hours.

**Practical consequence with a date on it:** FRC Event Registration Round 1 preferencing opens
**2026-09-24, 12:00 ET**. Missing it costs a Regional team its first-choice event, which per this table
is worth more than any single mechanism decision the team will make in January.
(See [`research/00_PREMISE_CORRECTION.md`](../research/00_PREMISE_CORRECTION.md) for the date table.)

**Weight: 70 — but as a context multiplier, not a rubric row.** [C] Event selection is not a property of
a *strategy*; it is a property of the *season*. Set it once, at the top of the rubric, and let it scale
the achievability of every strategy underneath. Scoring it per-row would double-count it.

---

## 12. Game-conditional adjustments — the five weight moves you make on kickoff day

`tools/rubric_weights.py` reads all five off the manual. Each is keyed on text that is printed in
Section 6 (or its equivalent) of every modern FRC manual.

| # | Reads | Effect | Positive controls in corpus | Negative controls |
|---|---|---|---|---|
| 1 | a Ranking Point or Bonus **named after the autonomous period** | `auto += 25` | `REEF` "AUTO RP" | `RAPD`, `CHRG`, `CRES`, `REB` |
| 2 | any protection rule covering a **scoring/loading** area with **no terminal time window** | `defense −= 20` | `CRES` (PODIUM, SOURCE/AMP), `REEF` (ZONE) | `RAPD`, `CHRG`, `REB` |
| 3 | protection rules that fire only *"during the last N seconds"* | `defense −= 4` each | `RAPD` HANGAR, `CRES` STAGE, `REEF` CAGE, `REB` TOWER | `CHRG` |
| 4 | *"1 defender at a time"* | `defense −= 15` | `REEF` G421 only | all others |
| 5 | PIN count ≥ 5 s | `defense += 10` | `RAPD`, `CHRG`, `CRES` | `REEF`, `REB` (3 s) |
| 6 | MAJOR foul as % of a typical alliance score | `defense −10 / −5 / +5` at ≥12% / 8–12% / <8% | — | — |
| 7 | ≥8 point-value rows in the scoring table | `scope += 10` | `RAPD` 10, `CRES` 16, `REEF` 14, `REB` 9 | `CHRG` (unparsed) |
| 8 | **no** SCORING ELEMENT possession cap | *no weight change — prints a warning* | `REB` (uncapped) | `RAPD` 2, `CHRG` 1, `CRES` 1, `REEF` 1 |

### 12.1 The leveler checklist — read the manual against this list

Adapted from [John_Bottenberg, #15, 2026-03-11](https://www.chiefdelphi.com/t/516134/15) (+45), who
catalogued the game-design features that compress the gap between elite and average teams, with the
seasons each appeared in. **[H]** — a community taxonomy over prior seasons, reproduced here as a
checklist rather than a scored input.

Count how many of these BIOCORE has. **The more boxes checked, the higher a small team's realistic
ceiling.**

- [ ] Game piece **possession limit** (§0 step 4 answers this mechanically)
- [ ] **Diminishing returns** from scoring — scoring locations that fill up
- [ ] **Shutdown defense** is viable (§0 step 3 answers this mechanically)
- [ ] Tasks worth real points achievable **with only a drivebase**
- [ ] An **endgame worth a lot**, achievable once per match
- [ ] **Full-field cycles** — drivetrain speed does not vary much from mid to top tier
- [ ] **Game piece scarcity**
- [ ] Major tasks requiring **cooperation between alliance partners**
- [ ] A **ranking system** that admits variance in the top seeds

His verdict on the season this instrument was tuned against: *"Rebuilt has none of these things… This
allows elite teams to shine more than any other game since I started paying attention."* `REB` also has
no possession cap — the one item on the list that §0 can check automatically — and produced the widest
EPA spread in the corpus (§5.3). **[S]** The two observations are consistent, which is why the
possession-cap check earns a slot in the 60-second workflow.

---

## 13. Validation / dry run

### 13.1 The extractor runs on all five archived manuals

Verbatim output of `python tools/rubric_weights.py <manual> --typical-score <median>`, run
2026-08-22 against the PDFs in `manuals/archive/frc/`. Typical scores are the median `Avg Match` value
over every team-event in that season's TBA scrape — **independently recomputed**, and they match the
values used by the previous pass exactly:

```
2023  n=7208  median Avg Match =  78.9
2024  n=7605  median Avg Match =  45.2
2025  n=8013  median Avg Match =  86.4
2026  n=8160  median Avg Match = 143.3
```

| Season | foul (minor/major) | PIN | protected zones (with scope) | possession cap | AUTO-gated RP | scoring rows | **defense** | **auto** | **scope** |
|---|---|---:|---|---:|---|---:|---:|---:|---:|
| `RAPD` 2022 | 4 / 8 | 5 s | HANGAR ZONE `[endgame-only]` | 2 | none | 10 | **41** | 40 | 95 |
| `CHRG` 2023 | 5 / 12 | 5 s | *(none)* | 1 | none | *unparsed* | **35** | 40 | 85 |
| `CRES` 2024 | 2 / 5 | 5 s | PODIUM `[teleop-wide]`, SOURCE/AMP ZONE `[teleop-wide]`, STAGE `[endgame-only]` | 1 | none | 16 | **16** | 40 | 95 |
| `REEF` 2025 | 2 / 6 | 3 s | CAGE `[endgame-only]`, ZONE `[teleop-wide]` | 1 | **AUTO RP** | 14 | **1** | **65** | 95 |
| `REB` 2026 | 5 / 15 | 3 s | TOWER `[endgame-only]` | **NONE** | none | 9 | **26** | 40 | 95 |

Machine-readable: `research/predictive_tba/pf5_game_conditional_dryrun.csv`.

### 13.2 Every extracted fact was verified against the rule text by hand

| Fact | Verification |
|---|---|
| PIN counts | `REEF` G425 and `REB` G418 both read *"There's a 3-count on PINS"*; `RAPD`/`CHRG` G202 and `CRES` G420 read *"5-count"*. ✅ 5/5 |
| Protection scope | full rule text quoted in §9.2. ✅ 5/5 |
| 1-defender rule | `REEF` G421 *"No more than 1 ROBOT may be on the opponent's side of the FIELD"*; `grep` returns nothing for the other four seasons. ✅ 5/5 |
| Possession cap | `RAPD` G403 *"2 CARGO max"*; `CHRG` *"may not have CONTROL of more than 1 GAME PIECE"*; `CRES` G403 *"1 NOTE at a time"*; `REEF` G409 *"may not simultaneously CONTROL more than 1 CORAL and 1 ALGAE"*; `REB` **no such rule**. ✅ 5/5 |
| AUTO-gated RP | fires on `REEF` only; `REB`'s RP names parse as ENERGIZED / SUPERCHARGED / TRAVERSAL, none autonomous. ✅ 5/5 |
| Foul values | `REB` `grep "a credit of"` → 5, then 15, matching the manual's penalty table order. ✅ 5/5 |

### 13.3 Two bugs the dry run caught and fixed

Both were found by running the model against seasons whose answers are independently known.

1. **Window bleed.** `REEF`'s G427 ZONE protection was scored `endgame-only` because the 700-character
   read-ahead ran past its `Violation:` line into G428 CAGE protection's *"during the last 20 seconds"*.
   Fixed by truncating each rule's segment at its own `Violation:`. This one error inverted the entire
   defense verdict for 2025.
2. **2022's protection is not in a G-rule.** `RAPD` states HANGAR ZONE protection only in the ARENA
   timing table, as *"HANGAR ZONE protection engaged 0:30"* — no G-rule carries the phrase. Fixed by
   also matching `engaged N:NN`. Before the fix, 2022 scored as `teleop-wide` and came out at 25 instead
   of 41.

**[S]** Generalisation for kickoff day: if BIOCORE's protection rules are worded in any way these two
patterns do not cover, §0 step 3 will print the raw rule text and you can classify it by eye in five
seconds. **Do that anyway.** It is the highest-value five seconds of the day.

### 13.4 The population statistics reproduce

`tools/predictive_factor_stats5.py` recomputes the captaincy base rates from the raw scrape using an
independent code path from `predictive_factor_stats4.py`. All twenty cells match to 0.1 pp
(`pf5_captaincy_base.csv` vs `pf4_captaincy_base_rates.csv`). The winning-alliance and reliability
tables likewise reproduce. **[C]**

### 13.5 Where the back-test disagrees with the prior pass, and why

The prior pass reported early→late output growth of 49.8 / 49.8 / 66.8 / 73.5% and rank-percentile
changes of +3.1 / +2.5 / +1.8 / +4.2. Restricting to Weeks 1–6 gives 37.0 / 39.6 / 45.7 / 40.3% and
+0.2 / +0.6 / −0.2 / −1.9. **The prior numbers are not wrong; they answer a different question.**
Including District Championships and the FIRST Championship in the "late" bucket compares a team's
regular-season event against a qualification-gated field, which manufactures both a larger apparent
growth and a guaranteed rank decline. Use the Weeks 1–6 row when reasoning about a team's own
improvement; use the all-events row only when reasoning about advancement.

---

## 14. How to use these weights in the rubric

1. **Set the context multiplier first.** Field size of the events you can actually register for (§11).
   This scales everything.
2. **Run §0.** It returns the four game-conditional weights (`defense`, `auto`, `scope`, plus the
   possession-cap warning).
3. **Score each candidate strategy against the eleven factors in §2** using the adjusted weights.
4. **Apply the two 2027-specific penalties** that no back-test can supply:
   - any strategy depending on vision-based pose estimation → schedule-risk penalty until SystemCore is
     in hand and running (§6.3);
   - a first-year swerve adoption counts as a **mechanism**, not a drivetrain upgrade (§3.4).
5. **Sanity-check the top-ranked strategy against §4.4.** If it needs more mechanisms than an Everybot
   and your team is smaller than the median Everybot team, the ranking is wrong somewhere.

---

## Files written by this pass

| Path | Contents |
|---|---|
| `reference/04_PREDICTIVE_FACTORS.md` | this document |
| `reference/04_predictive_factors.yaml` | machine-readable weights + game-conditional rules (rewritten this pass) |
| `tools/predictive_factor_stats5.py` | new: controlled week-curve, early-vs-late, field-size and captaincy analyses |
| `tools/rubric_weights.py` | **modified**: scope-aware protection classifier, possession-limit test, banded foul term |
| `research/predictive_tba/pf5_week_curve.csv` | mean event score by week, indexed to Week 1, 4 seasons |
| `research/predictive_tba/pf5_early_late.csv` | early→late growth and rank change, with and without the Weeks 1–6 restriction |
| `research/predictive_tba/pf5_field_size_pick.csv` | pick probability by field size × rank band, 4 seasons, 128 cells |
| `research/predictive_tba/pf5_winning_alliance.csv` | winning-alliance slot rank profile, 4 seasons |
| `research/predictive_tba/pf5_captaincy_base.csv` | captaincy rate matched on events attended |
| `research/predictive_tba/pf5_game_conditional_dryrun.csv` | the §13.1 back-test table |
| `research/predictive_tba/pf5_summary.json` | all of the above in one JSON |

---

## Known limitations

- **Reliability is measured through DQ, which is a rules event, not a breakdown.** The real quantity —
  did the robot work for all 12 matches — needs TBA API v3 match breakdowns and a key. Everything in §8
  is a lower bound. This is the largest gap in the document.
- **Statbotics was down** (HTTP 500 on every data endpoint, 2026-08-22). No component EPA, so §6.3
  (vision) has no independent measurement and carries `[S]`. Re-probe with
  `curl -s -o /dev/null -w "%{http_code}" https://api.statbotics.io/v3/team_year/254/2025` before
  trusting that section; if it returns 200, redo §6 properly.
- **No swerve-vs-tank study exists, and this pass did not create one.** Statbotics does not label
  drivetrain and TBA does not either. The 45 weight rests on adoption data, a cost ladder, one
  single-event pick-order observation, and two mentor accounts. If someone publishes a labelled
  comparison, §3 should be rewritten first.
- **No practice-hours dataset exists anywhere.** §7 proves in-season improvement does not move relative
  rank; it *infers* that pre-season hours do. The inference is strong but it is an inference.
- **The Everybot 22%-vs-21.8% parity comparison is not like-for-like.** 118 does not publish the
  event-count distribution of Everybot teams, so the matched base rate is chosen, not computed. If
  Everybot teams skew toward 1-event schedules the true comparison is *favourable* to Everybot; if they
  skew toward 3+, it is unfavourable. Ask 118 — they have the spreadsheet.
- **`scoring_rows` is the weakest extracted fact.** It depends on PDF layout: `REB` parses as 9 rows
  from the PDF and 7 from the `pdftotext` mirror, and the scope bonus threshold is 8 — so the two
  extractions disagree on whether the bonus fires. `CHRG` does not parse at all. **Count the point-value
  table by eye on kickoff day; it takes ten seconds and the parser does not deserve your trust here.**
- **Typical-alliance-score for 2022 is unavailable** (the TBA scrape starts at 2023), so `RAPD`'s
  defense weight of 41 omits the foul-cost term and is not strictly comparable to the other four.
- **2026's auto column is `Avg Auto Fuel`, not `Avg Auto`.** `REB` reported only the fuel component of
  autonomous scoring in the public rankings, so the 2026 auto-share figure (20.6%) and partial
  correlation (0.061) understate total autonomous contribution by an unknown amount.
- **Week 6 contains District Championships in 2023–2025** (2026 moved them to Week 7). §7.1 therefore
  quotes Weeks 1→5 for the clean regular-season comparison, and the Week 6 column should not be read as
  a regular-season data point in those three seasons.
- **All Chief Delphi content in this document is testimony, not measurement**, except where a poster
  published counts from a dataset they describe (118's Everybot statistics, Karthik's swerve census,
  mattd77's EPA analysis). Testimony is labelled `[C]` only as to *what was said*, never as to whether
  it generalises.
- **Nothing about BIOCORE's own rules is known.** Every game-conditional weight in §12 is a *procedure*,
  validated on five past seasons. None of them is a prediction about BIOCORE.

---

## Security note

All Chief Delphi topics, FRC manuals, vendor pages and FIRST community posts read for this pass were
treated as **data**. None contained text addressed to an AI assistant or any attempt to issue
instructions. Scraping used a normal browser user-agent against public endpoints only; no
authentication was used or attempted.
