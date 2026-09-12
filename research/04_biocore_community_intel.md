# BIOCORE (FRC 2027) — Community Intel & Informed Speculation

**Compiled:** 2026-08-21 · **Last revised:** 2026-08-22 · **Kickoff:** 2027-01-09 12:00 ET · **Days to manual:** 140

> **2026-08-22 revision.** Re-pulled every live source. **No new community activity** — the main prediction thread is unchanged at 357 posts (last post 2026-08-12) and the pre-order thread at 98 (last 2026-06-28); the corpus below is complete as of today. Two substantive additions from a full re-read of the pre-order thread: a **shipping-rate ladder** that constrains element *geometry* and is the strongest physical evidence available (**new §2.3**), and the discovery that AndyMark's listed weight for `am-5901` is a **placeholder**, which both creates the project's best leak tripwire and weakens every shipping-derived inference — including one this file previously relied on. Betting sheet revised accordingly: **P9 downgraded, new P11 added.**
**Purpose:** Input to a post-kickoff deep manual review. Everything here is pre-manual. Tags are load-bearing — do not promote a `[SPECULATION]` line to fact when scoring this against the real manual.

**Tag key**
- `[VERIFIED]` — primary source (firstinspires.org, FIRST community blog, AndyMark product data, WPILib). Link + date given.
- `[COMMUNITY-CONSENSUS]` — repeated independently by multiple credible posters; still not fact.
- `[SPECULATION]` — single-source theory, meme, or my own inference. Sub-labeled `(quantitative)` where the reasoning chains off verified numbers.

---

## 0. STOP — three premises in the task brief are wrong

This matters more than anything else in this document, because a wrong premise here poisons every downstream design decision.

### 0.1 "Pollen" is the **FTC** scoring element, not FRC's

`[VERIFIED]` The 2026-27 **FIRST Tech Challenge** game is **BIOBUZZ™ presented by RTX**, kickoff **September 12, 2026**. Its scoring element is **POLLEN**. Source: [Game Preview 2027: StarterBots, Skill Builders, Field Elements and More! — FIRST community blog](https://community.firstinspires.org/game-preview-field-elements).

`[VERIFIED]` POLLEN hard specs, from the AndyMark product record (`am-5851_preview`, [BIOBUZZ™ POLLEN Game Preview Pack](https://andymark.com/products/ftc-2026-27-game-preview-pack), retrieved 2026-08-21):
- Color: **Yellow**
- Diameter: **2.8 in ± 0.1 in**
- Weight: **0.055 lb**
- Price: $5.50 for 3 → **$1.83 each**

`[VERIFIED]` For comparison, the FTC DECODE **ARTIFACT** (`am-3376a`, [DECODE™ Game Pieces](https://andymark.com/products/ftc-25-26-am-3376a)): **5.00 in diameter, 0.165 lb, $1.35 each**. So POLLEN is *not* the same part as an Artifact — it is roughly **half the diameter and one third the mass**. FIRST's phrasing was "similar characteristics," not "identical." The brief's "~3in plastic balls, similar to DECODE Artifacts" is right about POLLEN and wrong about the lineage being a reuse.

`[VERIFIED]` The **FRC** BIOCORE scoring element is a *different, unrelated, still-secret part*: SKU **`am-5901`**, described as "**a custom item manufactured overseas with properties specific to BIOCORE**," with **no published dimensions, mass, material, color, or shape**. Sources: [Pre-Orders for 2027 Scoring Elements — FRC Blog, 2026-06-08](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements) and [BIOCORE™ FRC Scoring Element Pre-Orders — AndyMark](https://andymark.com/products/biocore-frc-scoring-element-pre-order).

`[VERIFIED]` The [FRC BIOCORE Game & Season page](https://www.firstinspires.org/programs/frc/game-and-season) (retrieved 2026-08-21) contains **no mention of Pollen, StarterBots, or Skill Builders**. As of today FIRST has published *nothing* about the FRC element's physical form.

**The community knows this and has said so explicitly.** The first mention of Pollen anywhere in the 357-post FRC prediction thread is post #331, [TheKwabe, 2026-07-30](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/331), who correctly frames it as *"the FTC game for next year."* Two posts later, asked whether there's an FRC equivalent, [TheKwabe, #346, 2026-07-31](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/346) replies: **"nothing published yet, but i'll keep a lookout."**

### 0.2 "StarterBots" and "Skill Builders" are **FTC** programs

`[VERIFIED]` Both terms come from the same FTC BIOBUZZ preview blog. **StarterBot Bases** were released by four vendors (AndyMark, goBILDA, REV Robotics, Studica — the last on 2026-05-04); full StarterBot designs land at FTC kickoff 2026-09-12. **Skill Builders** are described as *"activities hosted on FIRST Training, including learning content, challenges, and fun robot mini-games."* ([source](https://community.firstinspires.org/game-preview-field-elements))

`[VERIFIED]` FRC's analogue already exists and is *older*: the **FRC KitBot**, e.g. the [2026 KitBot Instruction Guide](https://firstfrc.blob.core.windows.net/frc2026/KitBot/2026-kitbot-build-instructions.pdf) and [2026 KitBot Iteration Guide](https://firstfrc.blob.core.windows.net/frc2026/KitBot/2026-kitbot-iteration.pdf), plus vendor equivalents such as the [2026 REV ION **FRC Starter Bot**](https://docs.revrobotics.com/frc-kickoff-concepts). So the *word* "Starter Bot" does appear in FRC — as REV vendor branding, not a FIRST program. Nothing has been announced for FRC 2027.

**Net:** there is no evidence FIRST is scaffolding *FRC* more than it already does. See §4.

### 0.3 The Sept 24, 2026 date is real but is registration, not game content

`[VERIFIED]` [BIOCORE Event Registration Updates — FRC Blog, 2026-07-21](https://community.firstinspires.org/2026-biocore-event-registration-updates): **Round 1 event preferencing starts 2026-09-24**; inter-district registration opens **2026-11-05**. Substantive rule changes: teams **must** select a home-country event in Round 1 where one exists; Regional teams may now buy into a District event for **$1000** but earn **no District/Regional points, no direct qualification, and no eligibility for Cultural Awards** (Impact, EI, RAS, Leadership, WFF). New Regional in the **Netherlands**. This is season logistics; it says nothing about the game.

---

## 1. Verified baseline — the complete set of hard FRC facts as of 2026-08-21

Everything below is `[VERIFIED]`.

| Fact | Source |
|---|---|
| Season brand: **FIRST® CANOPY™**, biodiversity theme | [firstinspires.org/first-canopy](https://www.firstinspires.org/first-canopy) |
| FRC game: **BIOCORE™ presented by Haas** (Gene Haas Foundation) | [FRC Game & Season](https://www.firstinspires.org/programs/frc/game-and-season) |
| Kickoff / reveal: **2027-01-09, 12:00 p.m. ET**, FRC YouTube | same |
| Theme line: teams *"delve into the heart of what sustains life on Earth"* | same |
| **BIOCORE has exactly ONE type of scoring element** | [Pre-Orders blog, 2026-06-08](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements) |
| **Robots have a holding limit during the match, and it is more than one** | same |
| **KoP Season Specific Box quantity > the holding limit** | same |
| **No additional scoring elements via FIRST Choice** | same |
| Element is **custom, manufactured overseas**, properties specific to BIOCORE | same |
| Pre-order SKUs: `am-5901_kop` = **$70.00**; `am-5901_partial` (1/5 field) = **$169.00** | [AndyMark](https://andymark.com/products/biocore-frc-scoring-element-pre-order), product JSON retrieved 2026-08-21 |
| FIRST **intentionally will not state** how many elements are in each quantity | [Pre-Orders blog](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements) |
| Pre-orders open 2026-06-08 → 2027-01-09; ship from **2027-01-11**; **all sales final**, cannot combine shipments | same + AndyMark |
| **SystemCore replaces roboRIO for 2027**; roboRIO will *not* run alongside it; every team gets a SystemCore in the 2027 year-specific KoP box | [WPILib Systemcore docs](https://docs.wpilib.org/en/latest/docs/software/systemcore-info/systemcore-introduction.html), [2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027) |
| Round 1 preferencing 2026-09-24; in-country requirement; $1000 Regional→District buy-in | [Event Registration Updates, 2026-07-21](https://community.firstinspires.org/2026-biocore-event-registration-updates) |

**The 2026 baseline you're comparing against** `[VERIFIED]` — REBUILT presented by Haas: 5.91 in / 0.448–0.5 lb high-density polyurethane foam **FUEL** balls; AndyMark SKUs `am-5801` ($2.00 ea), `am-5801_kop` = **10 pieces**, `am-5801_42` = **42 pieces = 1/12 of a full field → full field = 504 FUEL** ([Official REBUILT™ FUEL](https://andymark.com/products/official-rebuilt-fuel)). Holding limit **8** (G-rule wording: *"it fully and solely supports not more than 8 FUEL"*). Hub shooter with alternating Hub activation; three-rung Tower climb.

`[AUDIT 2026-08-22 — CORRECTED against the local 2026 manual PDF, Table 6-4/6-5]` The earlier one-line summary here ("climb 10/20/30; Energized ≥100, Supercharged ≥360, Traversal ≥50") was the **Regional-tier teleop** slice only. The full picture, which matters because both features are exactly the kind of structure to look for in BIOCORE:

- **TOWER points are period-dependent.** LEVEL 1 = **15 in AUTO, 10 in TELEOP** (max 2 ROBOTS); LEVEL 2 = **20**; LEVEL 3 = **30**. LEVEL 1 is only earnable in AUTO; the higher levels only later. A flat "10/20/30" hides the AUTO premium.
- **BONUS RP thresholds escalate by event tier** (Table 6-5), and the manual states they *"may increase"* for DCMP/CMP with the values announced in Team Updates:

  | BONUS RP | Regional / District | District Championship | *FIRST* Championship |
  |---|---|---|---|
  | ENERGIZED RP | **100** | **240** | **360** |
  | SUPERCHARGED RP | **360** | **360** | **500** |
  | TRAVERSAL RP | 50 | 50 | 50 |

  **Carry this into the BIOCORE review as an explicit question:** does BIOCORE tier its BONUS RP thresholds? If it does, a robot tuned to clear the Regional threshold is *not* tuned to clear the Championship one, and the gap (100 → 360 for ENERGIZED, a 3.6× jump) is far larger than teams expect.

Win 3 / Tie 1. ([Rebuilt (FIRST) — Wikipedia](https://en.wikipedia.org/wiki/Rebuilt_(FIRST)), [2026 Game Manual](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf), `manuals/archive/frc/_txt/2026_REBUILT.txt`). `[AUDIT 2026-09-12]` That extraction is not in the public repository, because FIRST's manual text is not redistributed; rebuild it locally with `bash tools/rebuild-corpus.sh --fetch` and then `bash tools/rebuild-corpus.sh`.

---

## 2. The strongest available signal: pre-order price arithmetic

This is the one place where FIRST leaked real information, and it is worth more than the entire 357-post speculation thread.

### 2.1 The community's version

`[COMMUNITY-CONSENSUS]` Within hours of the 2026-06-08 blog, CD ran the numbers:

- [pigrammer, #5, 2026-06-08](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/5) (21 likes): *"1/5 of a field is around 2.5-3 times what is in the KOP… a whole field is around 12.5x what is in the KOP. Since the holding limit is at least 2, therefore what is in the KOP is at least 3 elements, and we have at least 37-38 game pieces on the field."*
- [Christopher149, #63](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/63) formalizes the floor: holding limit ≥2 → KoP ≥3.
- [dan, #10](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/10) (19 likes): *"In Rebuilt, we had a quantity of ⅙ of a full field. I assume that now we have ⅕ because the number of field elements isn't divisible by 6… the closest to your calculation will be 40. Could also be 50, 70, 80, or 100."*
- [Garrison, #14](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/14) (19 likes) — **the shipping tell**: *"2/5 of a field delivered to San Diego via Fedex Ground was $26. Shipping for 2/6 of a field last year was ~$230. I'm guessing an inflatable or something easily compressible."*
- [Michael_Corsetto, #16](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/16) (36 likes): *"our all-in cost was about $1400 for 7/5 of a field. About 35% of what we paid last year."*
- [Zack_Osowski, #35](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/35) (39 likes) — highest-liked concrete guess: *"Rubber Inflatable Footballs. Carry limit three, four in the KOP, fifty on the field. Works out to about $17 per football and ships cheap. Game pieces are called 'seeds'."*

### 2.2 My tightened version `[SPECULATION] (quantitative — chains off VERIFIED prices)`

The community stopped one step short. Calibrating against REBUILT, where we now know the ground truth, sharpens the estimate considerably.

**Calibration (REBUILT 2026, all verified):** pre-order was KoP **$58** and 1/6 field **$438** ([bobbysq #7](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2026-game-pieces/504079/7), [pigrammer #6](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2026-game-pieces/504079/6); later raised to $61/$470 on 2025-09-16 for tariffs, [bobbysq #126](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2026-game-pieces/504079/126)). Ground truth: KoP = **10**, field = **504**.
- Price ratio 438/58 = **7.552** → naive field/KoP = 6 × 7.552 = **45.3**
- True field/KoP = 504/10 = **50.4**
- ⇒ AndyMark applies a ~**10% bulk discount** on the partial-field SKU. Naive ratio *understates* the true count by ~11%.

**Apply to BIOCORE:** 169/70 = **2.4143** → naive field/KoP = 5 × 2.4143 = **12.07** → discount-corrected **field ≈ 13.4 × KoP**.

Combined with KoP ≥ 3 (holding limit ≥2, KoP > holding limit), and cross-checking implied unit price against the historical FRC game-piece price band:

| KoP qty | Implied $/element | Implied full field | Plausible? |
|---|---|---|---|
| 3 | $23.33 | **~40** | Yes — priciest FRC piece ever, but in band |
| **4** | **$17.50** | **~54** | **Yes — dead centre of historical band** |
| **5** | **$14.00** | **~67** | **Yes** |
| 6 | $11.67 | ~80 | Yes |
| 8 | $8.75 | ~107 | Marginal |
| 10 | $7.00 | ~134 | Marginal |
| 12 | $5.83 | ~161 | Unlikely (see shipping) |

Historical per-piece KoP prices for reference, compiled by [TNorris, #39](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2026-game-pieces/504079/39) (10 likes) plus AndyMark: 2017 FUEL $1.10 · 2017 Gear $14.90 · 2019 Cargo $10.60 · 2020 Power Cell $18.69 · 2023 Cone $12.29 · 2024 Note $19.00 · 2025 Coral $5.00 · 2025 Algae $16.50 · 2026 FUEL $2.00 retail / ~$5.80 pre-order.

**Conclusions I'd stake money on:**
1. **The field holds roughly 40–80 scoring elements — call it 36–90 as the honest interval.** That is **~6–13× fewer than REBUILT's 504**, and the full-field cost dropped from ~$2,630 (6 × $438) to **$845** (5 × $169), a **68% cut**.
2. **The element costs $12–23 each.** That is the price class of a Note, an Algae, a Power Cell, a Gear — a substantial moulded object — **not** a foam or plastic ball. A 2.8 in Pollen-alike would cost $1–2 and would need ~400–600 units to reach $845, which the KoP ratio forbids.
3. **The holding limit is 2, 3, or 4.** It must be ≥2 and < KoP, and KoP is almost certainly 3–6.
4. **Garrison's shipping datum kills the high-count branch.** 2/5 of a field for **$26** FedEx Ground vs 2/6 (=168 FUEL) for **$230** implies roughly an order of magnitude less dimensional volume. If the field held 400+ pieces, 2/5 would be 160+ pieces and could not ship for $26 regardless of what they are. Either the count is low (16–36 pieces in that box), or the pieces are collapsible/nestable, or both.
   `[REVISED 2026-08-22]` This datum is now superseded by the **full rate ladder in §2.3**, which is both stronger and more specific — and which comes with a material caveat about AndyMark's placeholder weight that applies to this line too. **Read §2.3 before relying on any shipping-based argument.**

**Why this is the headline finding:** a 40–80-piece field with a 2–4 holding limit is a **cycling / placement economy**, not a volume-shooting economy. REBUILT's 504-ball firehose is not coming back in 2027.

### 2.3 The shipping-rate ladder — a harder constraint than the price ratio `[ADDED 2026-08-22]`

The prior version of this file used only Garrison's single $26 datum. A full re-read of all 98 posts in the pre-order thread surfaced a **rate ladder** that constrains element *geometry*, not just count. This is the best physical evidence in the corpus and it was previously missed.

`[VERIFIED]` (direct quotes, live rate lookups run by teams against AndyMark's checkout on 2026-06-08):

| Order quantity | Shipping quote | Source |
|---|---|---|
| KoP qty → Houston | **same as 1/5 field** | [Weldingrod1, #61](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/61) — *"Oddly enough, shipping to Houston is the SAME for both a KOP and 1/5 field. Sounds like a minimum volume box is involved in this. IE, its driven by at least one characteristic dimension."* |
| 1/5 and 2/5 field → Houston | **$27** | [Weldingrod1, #65](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/65) |
| 3/5 field → Houston | **$35** (first jump) | same |
| 5/5 full field → Houston | **$61** | same — *"it looks like KOP, 1/5, and 2/5 go in the same box."* |
| 2/5 field → San Diego | **$26** FedEx Ground | [Garrison, #14](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/14) |
| 2/5 field → Hawaii (96761) | FedEx Ground $211.18 · **USPS Ground Advantage $83.13** · USPS Priority $100.82 | [ddg258, #44](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/44) |
| REBUILT 2026 2/6 field (=168 FUEL) | **~$230** | [Garrison, #14](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/14) |

`[VERIFIED]` AndyMark's own policy: *"AndyMark, Inc. ships almost exclusively parcel packages via FedEx and USPS small flat rate."* ([shipping policy](https://andymark.com/policies/shipping-policy), retrieved 2026-08-22). So a **full BIOCORE field moves as ordinary parcels, not freight.**

**Three inferences, in descending confidence:**

1. `[SPECULATION] (quantitative)` **A full field is ~2–3 parcel boxes.** $61 / $27 ≈ 2.26 box-units, with the step at 3/5. REBUILT needed ~$230 for *two-sixths* of a field. Whatever BIOCORE's element is, a **whole field of them ships for roughly a quarter of what a third of a REBUILT field cost.** This independently corroborates P2 without using the price ratio at all.

2. `[SPECULATION] (quantitative)` **The elements almost certainly nest, stack, or collapse.** This is the real payload of Weldingrod1's observation. KoP and 2/5-field ship in the *same box*, yet 2/5 field is ≈ 4.8–5.4 × the KoP quantity (2 × the 2.41 price ratio, or 2 × the 2.68 discount-corrected ratio from §2.2). A box justified by a *single* KoP's worth that still swallows five KoP's worth means the box is sized by **one large characteristic dimension of a single element**, and that many elements then fit inside that same envelope.
   **Spheres cannot do this.** Spheres pack at ~64% and do not nest at all; a box holding 20 balls is necessarily ~5× the volume of a box holding 4. The same-box observation is therefore **direct geometric evidence against a ball**, and it is much stronger than the price argument in §2.2 conclusion 2.
   Shapes that satisfy *"one large dimension + high packing efficiency"*: **cones** (2023 CONE, $12.29 — nests perfectly), **rings/tori/tubes** (stack on a rod), **discs** (2013 FRISBEE — stack flat), **shallow bowls / seed-pod half-shells** (nest like cups). All are in the $12–23 price class from §2.2. All are consistent with a CANOPY/botanical theme.

3. `[SPECULATION]` **Hard dimensional ceiling.** USPS Ground Advantage *and* Priority were both offered for a 2/5-field order. Both cap at **70 lb** and Priority at **108 in length + girth**. So 2/5 of a full field — on the §2.2 central estimate, ~21 elements — fits inside one ≤70 lb parcel of ≤108 in length+girth. At 21 elements that is **≤3.3 lb per element**, and realistically far less.

**⚠ Caveat that undercuts all shipping-derived reasoning — flagged because the prior version leaned on it.**
`[VERIFIED]` Both `am-5901` variants carry a **placeholder weight of 999.0 lb / 453,139 g** in AndyMark's product record, identical on both SKUs, and unchanged since the listing was created (confirmed against the [2026-07-01 Wayback snapshot](http://web.archive.org/web/20260701202933/https://andymark.com/products/biocore-frc-scoring-element-pre-order.json) and re-pulled live 2026-08-22). Every *other* AndyMark game-piece SKU carries a true weight — REBUILT FUEL `am-5801` 0.474 lb, FTC POLLEN pack `am-5851_preview` 0.35 lb, DECODE ARTIFACT `am-3376a` 0.165 lb.
A 999 lb variant weight **cannot** produce the quotes above — USPS refuses anything over 70 lb, yet USPS rates were returned. So AndyMark's rate engine is *not* using the listed weight, and we do not know what it *is* using (a manual override, a packing profile, or dimensional-only rating). **The ladder's internal consistency — flat through 2/5, stepping at 3/5, ~2.26× at 5/5 — is strong evidence it reflects something real about volume.** But until that placeholder resolves, treat every number in this subsection as *suggestive, not load-bearing*, and do not upgrade inference 2 above ~60% on shipping evidence alone.

**This makes the 999.0 lb field the single highest-value tripwire in the project.** The moment AndyMark enters a real weight on `am-5901`, mass-per-element is public and §2.2's entire table collapses to one row. It is trivially pollable — see §9.

`[COMMUNITY-CONSENSUS]` The thread reached the nesting conclusion only obliquely. [Footie, #22](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/22) correctly argued the shipping delta is explained by *count* rather than compressibility (*"a shipment is something like 12 balls instead of 90 per unit"*) and is *"continually bearish on inflatables."* [HeroBrayden, #39](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/39) read it as *"collapsible and can be compacted."* [mperino, #100](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/100) noted Gopher's ball shipping is close to AndyMark's pre-order rate, which cuts *against* the inflatable read. **Nobody connected the same-box observation to nesting geometry** — that step is mine, and it is the most useful thing in this document after §2.2.

`[VERIFIED]` Worth carrying into any international-team conversation: [AlexBurchard, #82](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/82) (17 likes) on Türkiye — shipping plus customs often doubles cost and shipments are seized outright. The single-source overseas-manufactured element is a real equity problem, and it is the kind of thing that generates Team Updates.

---

## 3. What the community inferred from the ball/Pollen angle — and why it mostly doesn't transfer

### 3.1 Almost nobody in FRC made the Pollen→BIOCORE leap

`[VERIFIED]` I read all 357 posts of the FRC prediction thread. **Pollen appears exactly once** ([#331](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/331), 2026-07-30), correctly attributed to FTC. The FRC community did *not* adopt "3in ball" as a BIOCORE prior. If your later review assumes a shooter because of Pollen, you are assuming something the informed community explicitly declined to assume.

The one poster who tried to build the cross-program bridge concluded it doesn't work: [Electro, #332, 2026-07-31](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/332) — *"Since there was correlation last year with there being a mini hub for ftc and with them also having spherical objects, I looked for any correlation this year but couldn't think of any since we just had a ball game."*

### 3.2 The pre-Pollen ball-game arguments that do exist

`[SPECULATION]` [Josh_does_cad_a_lot, #65, 2026-05-03](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/65): *"we have seen the ftc starter base, which is pickelballs, and because ftc and frc were somewhat similar this season, i expect it to be similar next year, so i am speculating another shooter game, but much lower volume."* — This is the closest thing to the brief's thesis and it carried **0 likes**.

`[SPECULATION]` [SM7160, #227, 2026-06-09](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/227) (4 likes) built the best pro-shooter case from the holding-limit disclosure: *"2012 Rebound Rumble had one game piece and a holding limit of 3 basketballs; 2020 Infinite Recharge had one game piece and a holding limit of 5 power cells; 2022 Rapid React had one game piece and a holding limit of 2 cargo. Based on historical trends, I think we'll get a shooting game, but it is entirely possible that we get a pick-and-place with a higher holding limit."* **This is the single strongest argument against my §2 conclusion and you should weight it.** A stated holding limit >1 is historically correlated with balls.

`[COMMUNITY-CONSENSUS]` The counter, from [FRCAlum, #278](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/278) and [crummyh, #279](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/279): a >1 holding limit in a *pick-and-place* game hasn't really happened since **2015 Recycle Rush** — 2025 Reefscape allowed one of each type, 2023 Charged Up allowed multiples only in strategically irrelevant zones. So a multi-hold PnP would itself be a break from precedent. Both branches require breaking *some* precedent.

### 3.3 Ball-handling geometry constraints the community flagged

`[SPECULATION]` If it *is* a ball or ball-like solid, the recurring design points raised:
- [cottagechez, #80](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/80) (6 likes): *"We're not going to see another ball shooter for a while, everyone knows how to build a turret now, and they don't want to do things for which there's a semblance of a meta."*
- [maxwaldman, #240](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/240) (3 likes): an asymmetric piece plus a low possession limit *"would allow catapults to be competitive"* rather than flywheels — i.e. FIRST can kill the flywheel meta by changing the piece's inertia tensor rather than the field.
- [Ethan_Reed](https://www.chiefdelphi.com/t/speculation-could-an-american-football-shaped-game-piece-be-used-in-a-future-frc-game/509619/10) on prolate spheroids: *"Footballs are a real 'looks hard, is hard' challenge."* The detailed engineering rebuttal in that thread ([MARS_James, #13](https://www.chiefdelphi.com/t/speculation-could-an-american-football-shaped-game-piece-be-used-in-a-future-frc-game/509619/13), 19 likes, from someone who maintained real football throwing machines) argues the opposite — two wheels offset 30–45°, or three wheels for rifling, is well-trodden and scales down fine. **Caveat:** that thread's OP was widely called out as AI-generated ([Sam948, #24](https://www.chiefdelphi.com/t/speculation-could-an-american-football-shaped-game-piece-be-used-in-a-future-frc-game/509619/24), 38 likes) — treat the framing as low-quality, the replies as high-quality.

### 3.4 What historically wins ball games — the community's own read

`[COMMUNITY-CONSENSUS]` Not a BIOCORE-specific finding, but the repeated pattern in the "hopes" thread ([519917](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917), 248 posts, 8.2k views) is that ball/volume games converge to a single archetype fast and then reward reliability over cleverness: [AvaDoesStuff, #13](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/13) — *"there was so many clones by the end of the season matches got kinda boring to watch."* [kay, #349](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/349) on REBUILT Einstein: the differentiator was not shooter accuracy but **full-robot uptime** — *"Einsteins teams were dealing with bot shutdowns and connection issues this year."* Top-requested change overall, at 94 likes and the highest-voted post in the thread: [JAAMES, #4](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/4) — **"build diversity."**

---

## 4. StarterBot / Skill Builder — is FIRST scaffolding the games?

`[VERIFIED]` The scaffolding push is real but is currently **FTC-side**. Four vendor StarterBot Bases (AndyMark, goBILDA, REV, Studica) shipped pre-kickoff for BIOBUZZ, and FTC "Skill Builders" are hosted learning modules on FIRST Training. FTC also published *foundational challenges* teams should practice before kickoff: acquiring pollen off the foam field surface, **collecting multiple pollen simultaneously (in lines and piles)**, retrieving from borders and corners, and **autonomous navigation between known locations while intaking** ([source](https://community.firstinspires.org/game-preview-field-elements)).

`[SPECULATION]` **The one genuinely transferable inference:** FIRST is now willing to publish *pre-kickoff robot-task guidance* — "practice ground pickup, multi-piece intake, corner extraction, and auto-while-intaking" — months before the manual. If FIRST does the same for FRC 2027 between now and January, **that blog post is the highest-value leak of the cycle** and should be monitored. Nothing equivalent has appeared for FRC yet.

`[SPECULATION]` Is FRC moving toward a tiered/scaffolded game? Weak evidence for, and the community reads it as continuity rather than change:
- FRC already has the **KitBot** (with an explicit "Enhancement/Iteration Guide" — the tiering is in the *robot*, not the *game*), and REV markets an **FRC Starter Bot** whose stated philosophy is *"intentional incompleteness… we want this design to spark fresh ideas rather than limit them."*
- The 2026 game already had a de-facto tiered structure — RP thresholds at 100 / 360 FUEL and a 3-level Tower — which is the standard FRC scaffolding idiom and long predates FTC's StarterBot branding.
- `[COMMUNITY-CONSENSUS]` The loudest *design* ask in the hopes thread is for **more accessibility with a higher ceiling**, not tiers: [Bmongar, #90](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/90) — *"a game that is accessible to the floor where everyone can meaningfully contribute but not limiting to top tier teams… a game with more than 2 design archetypes"*; [gerthworm, #40](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/40) — *"Stacking several, unrelated objectives only hurts 90% of teams, and is barely a speed bump for the top 10%"*; [AdamHeard, #10](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/10) — *"A single game task like this year and 2014."*

**Bottom line:** treat "FIRST is building a scaffolded/tiered FRC game" as `[SPECULATION]` with **weak** support. The FTC StarterBot/Skill Builder program is an FTC onboarding initiative, not a signal about FRC game structure.

---

## 5. Leaks, teaser analysis, trademark filings, sightings

### 5.1 Credible leaks: **none**

`[VERIFIED]` I found no credible leak of BIOCORE game content. FIRST's own blog states they are *"intentionally not specifying the number of scoring elements"* and are *"keeping many details a surprise for Kickoff."* The relevant CD thread on the general question ([Are the seasons leaked to teams before they are announced?, 513933](https://www.chiefdelphi.com/t/are-the-seasons-leaked-to-teams-before-they-are-announced/513933)) exists but produced nothing about 2027.

`[SPECULATION]` One near-leak of *process*, not content — [pigrammer, #317, 2026-07-12](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/317): *"My understanding — these are internal details of course, based on other posts here — is that the in-progress 2021 game was reskinned into Rapid React which is why the theming wasn't awesome with it… Crescendo came from the Game Design Challenge in 2021."* Self-flagged as hearsay. Useful only as a prior on how GDC sources concepts (§6.3).

### 5.2 Teaser / logo image analysis `[COMMUNITY-CONSENSUS]` on the reading, `[SPECULATION]` on every conclusion

The BIOCORE logo is the entire evidentiary basis for most public speculation. Community readings of the central yellow shape, from [thread 519808](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808) (opened 2026-05-02, 357 posts, 23.7k views):
- **Football / prolate spheroid** — the single most common reading. [Psych714, #4](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/4) (11 likes), [#9](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/9) (35 likes) *"Foam football game pieces called seeds and you have to plant them"*; echoed by #197, #240, #241, #286, #288.
- **Seed** — [mountain2me, #87](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/87): *"'Safeguarding seeds for future generations' is probably the biggest clue we have."* Paired with [roproop, #145](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/145), who claims the CANOPY reveal video enumerated three tasks that map to the three programs — pollination → FTC BIOBUZZ, seed-vault → FRC BIOCORE.
- **Corn kernel** — [Christopher149, #7](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/7) (5 likes). **Cell** — [idk123_3296, #34](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/34) (14 likes), who offered to eat Loctite if wrong.

`[SPECULATION]` **The important methodological warning**, from [cottagechez, #287](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/287): *"judging from the previous logos, what a shape in the logo means is what a scoring location looks like"* — i.e. the logo's central object may depict the **goal**, not the piece. Corroborated by [Corbin, #149](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/149), who notes REEFSCAPE's logo showed the reef and REBUILT's showed the Hub. `[COMMUNITY-CONSENSUS]` counter from [CommonII, #242](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/242): *"based on historical trend the logo has almost nothing to do with the game."*

`[SPECULATION]` **Logo-shape rotation theory** — [HeroBrayden, #263](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/263) (3 likes): since 2025 each season's three program logos carry a circle, triangle, and square. 2025-26: UNEARTHED triangle / DECODE circular sundial / REBUILT square. 2026-27: BIOGLOW pulsing triangles / BIOBUZZ pulsing circles / **BIOCORE pulsing squares**. Falsifiable and cheap to check on kickoff day.

### 5.3 Season teaser (Feb–Mar 2026) — [thread 513367](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367), 175 posts, 16.2k views

`[COMMUNITY-CONSENSUS]` The teaser was a topographic map with a river and a green light. [Theadam, #35](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367/35) (52 likes) and [Liammm, #78](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367/78) (14 likes) independently geolocated it to **FIRST HQ in Manchester, NH** — with Liammm noting the gold star marker is *not* at HQ's actual coordinates. Consensus outcome: **the map is set dressing, not a clue.** "Water game confirmed" is the thread's running joke, not a prediction.

`[SPECULATION]` The most structured teaser read, [TurtleM, #32](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367/32) (14 likes): contour lines → field elevation/terrain; river → a central obstacle or field divider; green light → a signal element or a climb.

### 5.4 "Coffee with Collin" — the origin of the stacking theory

`[VERIFIED]` A pre-2026-kickoff FIRST video showed a stack of **2015 Recycle Rush totes falling over** ([thread 509687](https://www.chiefdelphi.com/t/new-coffee-with-collin-game-hint/509687), 2026-01-02, 84 posts, 5.9k views). `[COMMUNITY-CONSENSUS]` It was a **troll**, not a hint — [vdesai, #6](https://www.chiefdelphi.com/t/new-coffee-with-collin-game-hint/509687/6) (33 likes), [Mike_Marandola, #5](https://www.chiefdelphi.com/t/new-coffee-with-collin-game-hint/509687/5) *"red herring"*. `[SPECULATION]` But [scimn27, #83](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/83) (13 likes) argues these videos hint at **the year after next**, citing a 2024 scuba-diver clip that preceded 2025 REEFSCAPE — under which reading the falling totes point at **2027**. This, plus a 12-year "stacking cycle" meme (2003 Stack Attack → 2015 Recycle Rush → 2027; [fennquadnine, #335](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/335), 17 likes), is the entire basis of the stacking-game theory. **I rate it low.** A stacking game with 40–80 elements and a $14–23 unit cost is possible; a stacking game with a *stated holding limit* is awkward.

### 5.5 Trademarks, venue sightings, field-element sightings

`[VERIFIED]` **No results.** I could not locate a USPTO filing for "BIOCORE" attributable to FIRST via web search, and found **zero** reports of BIOCORE field-element sightings, venue leaks, or vendor tooling photos. Given the element is manufactured overseas with a January ship date, no sighting is expected before December 2026 at the earliest. `[SPECULATION]` The first genuine physical leak, if one comes, will most likely be a **shipping-manifest / customs or AndyMark packaging photo in Dec 2026**, not a field element.

---

## 6. Historical pattern analysis the community runs pre-kickoff

### 6.1 The shooter ↔ pick-and-place alternation

`[COMMUNITY-CONSENSUS]` The dominant frame in the thread. Recent FRC: 2022 shooter · 2023 PnP · 2024 shooter · 2025 PnP · 2026 shooter → **2027 PnP**. Asserted by [Bismuth, #157](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/157), [cottagechez, #80](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/80), [Electro, #329](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/329), [roproop, #145](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/145), and others.

`[COMMUNITY-CONSENSUS]` The rebuttal is equally well-organised: [Isaac-The-Pro, #277](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/277) and [NateJay, #311](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/311) — **2020 and 2022 were back-to-back shooters**; [Electro, #309](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/309) — *"It's never a guarantee… they are custom making pieces overseas."* And [pigrammer's #317 hearsay](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/317), if true, means the 2021→2022 "alternation" was a COVID artifact of a reskinned game, which weakens the pattern's foundation.

`[SPECULATION]` My read: the alternation is a real *tendency* with n≈5, and it points PnP — but the §2 price arithmetic points the same way independently, which is why I weight PnP-ish highly. Two weak-but-independent signals agreeing beats one strong signal.

### 6.2 The FTC-element→FRC-element theory — how well does it actually predict?

This is the pattern the brief leans on. Here is the honest track record `[SPECULATION]` on every mapping (these are community-style pattern matches, not FIRST statements):

| FTC season (piece) | Following FRC season (piece) | Match quality |
|---|---|---|
| 2017-18 Relic Recovery — cube glyphs | 2018 Power Up — 13 in fabric **Power Cubes** | **Strong** (both cubes) |
| 2018-19 Rover Ruckus — gold cubes + **silver balls** | 2019 Deep Space — 13 in **Cargo balls** + hatch panels | Moderate |
| 2019-20 Skystone — cube stones | 2020 Infinite Recharge — 7 in **Power Cells** (balls) | **Fails** |
| 2020-21 Ultimate Goal — **rings** | 2022 Rapid React — 9.5 in **Cargo balls** | **Fails** |
| 2021-22 Freight Frenzy — cubes, balls, ducks | 2022 Rapid React — balls | Vacuous (FTC had everything) |
| 2022-23 POWERPLAY — **cones** on junctions | 2023 Charged Up — **Cones** + Cubes | **Strong** |
| 2023-24 CENTERSTAGE — hex foam pixels | 2024 Crescendo — foam **Notes** (rings) | Weak (both foam, different geometry) |
| 2024-25 Into the Deep — blocks + specimens | 2025 Reefscape — PVC **Coral** + **Algae** balls | **Fails** |
| 2025-26 DECODE — 5 in **Artifact balls**, shoot into goal | 2026 Rebuilt — 5.91 in **FUEL balls**, shoot into Hub | **Strong** |

**Score: roughly 3 strong, 2 moderate/weak, 3 clear failures, 1 vacuous.** That is barely better than chance for a domain where "ball" is the base-rate answer anyway. `[SPECULATION]` **The theory is not reliable enough to anchor a design decision on.** Its apparent strength right now is recency bias from the DECODE→REBUILT hit, which is the most recent and most vivid case.

**And the specific 2027 instance breaks the theory's own mechanism.** The reuse story requires FIRST to amortise one part across programs. But BIOBUZZ's POLLEN is a *new* 2.8 in part (`am-5851`) that replaces DECODE's 5 in Artifact (`am-3376a`) — an FTC→FTC redesign — while FRC's BIOCORE element is a *third*, separately tooled, custom overseas part (`am-5901`). **All three parts are distinct.** There is no shared-part economy in play for 2027.

### 6.3 Game Design Challenge → real game

`[VERIFIED]` This pattern is real and better-evidenced than the FTC one. [Here is the Game Design Challenge that inspired ReefScape](https://www.chiefdelphi.com/t/here-is-the-game-design-challenge-that-inspired-reefscape/478600) (2025-01-04) identifies **2021 GDC Finalist Team 1318 — "Operation Outpost"** as the source of 2025 REEFSCAPE. [MooreteP, #2](https://www.chiefdelphi.com/t/here-is-the-game-design-challenge-that-inspired-reefscape/478600/2) notes the carried-over elements: the forest obstacle, and *"During the last 30 seconds, transport vehicles must navigate the Jungle and climb a Vine."* [four, #5](https://www.chiefdelphi.com/t/here-is-the-game-design-challenge-that-inspired-reefscape/478600/5): *"the GDC took more liberties… the field layout is clearly inspired and possibly the algae."*

`[SPECULATION]` The 2027 candidate the community has surfaced is **"BioDome Blitz"** by Cougars Gone Wired (FRC 2996), [YouTube animation](https://www.youtube.com/watch?v=MNGt2M1MeSE), raised by [Hmm_Persons, #272, 2026-06-26](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/272) (9 likes) and [#281](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/281), and again by [Reanobo, #354, 2026-08-07](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/354): *"the game elements are boxes and yellow football shaped things."* **This theory is already partly falsified** — [muffinofsteel, #355](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/355) correctly notes BioDome Blitz has two element types and FIRST has confirmed BIOCORE has one. A second candidate, a "**Ranger Danger**" GDC submission, is floated by [HeroBrayden, #39](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/39) specifically because its piece is *"collapsible and can be compacted into a significantly smaller space,"* which would explain the $26 shipping. I could not independently source either submission's documentation.

### 6.4 Alliance-coloured pieces

`[SPECULATION]` [JerJerBinks, #91](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/91) (13 likes) and [HeroBrayden, #188](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/188): alliance-coloured elements are *"long overdue,"* last used 2022. Excellent supporting research from [FRCAlum, #97](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/97): 1992–2026 breaks down as **22 "Alliance Goal" games, 9 "Alliance Piece" games** (six consecutive 1994–1999), 2 hybrid, 2 unclassifiable; before 2022 Rapid React the last neutral-goal/alliance-piece game was **2007 Rack 'n' Roll**. `[SPECULATION]` I read the "**one type of scoring element**" blog language and the single `am-5901` SKU with no colour variant as **evidence against** alliance-coloured pieces — AndyMark sells DECODE artifacts as separate purple/green SKUs when colours differ.

---

## 7. Sentiment and predictions on scoring, RP, and endgame

### 7.1 Scoring structure `[COMMUNITY-CONSENSUS]` leaning

- **Multiple scoring locations / height tiers** is the most repeated structural guess. [Electro, #329](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/329): *"i'm very sure there will be multiple scoring areas since it has been confirmed there's only one game piece"* — the logic being that a single element type needs positional variety to create a scoring gradient. Same idea in [Sahil, #84](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/84) (12 likes, tiered "tree"), [Arel, #205](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/205), [crummyh, #247](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/247), [Electro, #313](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/313).
- **A minority "shoot smarter, not more" thesis** — [HEFZZJM, #327, 2026-07-25](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/327) (5 likes): multiple targets at different heights/distances, *linked* so completing them together or in order yields bonuses, making interpolation tables and multi-shooter designs meaningful. `[SPECULATION]` **This is the most sophisticated single prediction in the thread and it is compatible with a low element count.** Flag it for the post-kickoff review.
- **Sorting / matching** — the very first reply, [Alex_Y, #2](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/2) (38 likes): *"Sorting game. To get the maximum number of gamepieces, you must score the correct gamepiece in the correct goal."* Now weakened by the single-element-type confirmation, unless the sorting key is *location* rather than piece identity.
- **Race for a shared central structure** — [idk123_3296, #339](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/339): a finite shared goal both alliances fill, explicitly to force interaction. `[SPECULATION]` **A finite 40–80-element field makes a zero-sum race mechanically possible in a way REBUILT's 504 balls did not.** [FRCAlum, #343](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/343) notes the precedent is 2007 Rack 'n' Roll.

### 7.2 Ranking points `[SPECULATION]`

Very little direct discussion — the community treats RP structure as unpredictable. What exists: [Corey_Applegate, #198](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/198) proposes threshold-count RPs plus a **co-op RP that lowers both alliances' thresholds** (the 2024 Coopertition idiom). [MARS_James, #22](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/22) (26 likes) wants a **buddy-climb RP** — *"Preventing the RP most likely attached to it from being a 'can do solo' but still only requiring 1 robot to have the mechanism."* Recurring complaint across both threads: RPs that a single elite robot can solo destroy the value of alliance partners ([CakeDeer6, #34](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/34), 12 likes, on 2-offense/1-defense meta lock-in).

### 7.3 Endgame `[COMMUNITY-CONSENSUS]` — this is the clearest sentiment in the corpus

The community is near-unanimous that **REBUILT's endgame was undervalued and 2027 will overcorrect**:
- [Pointygrnskies, #321, 2026-07-18](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/321): *"climbing in rebuilt was not a necessity, Biocore will likely emphasize climbing tenfold."*
- [cct, #351, 2026-08-01](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/351): *"in order to score or pick up a gamepiece, we will have to climb."*
- [Acdelli, #2](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/2) (52 likes): *"2022 felt like the last time the reward was really worth the risk… 2025's challenge being solved in the first 48 hours kinda killed the 'challenge' aspect."*
- **Split on the form.** Climb/vine/rope: [Bismuth, #157](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/157), [Liam_Gessman, #316](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/316), [ascension, #75](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/75) (*"First CANOPY… I'm seeing very sketchy climb is coming yet again"*), [beril, #18](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/18) (21 likes, a *swinging* branch). Platform/balance: [Mo-tion, #324](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/324) — *"the last major platform ideas were used in 2019 and 2023, while the last three seasons have been climbing"*; [HeroBrayden, #87](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367/87), [Minecraftwtr, #322](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/322) (multi-robot balance), [Weldingrod1, #326](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/326) (a platform that tilts under load).
- **Buddy climb / ramp bots** requested repeatedly: [MARS_James, #22](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/22), [Zihou, #187](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/187), [cottagechez, #7](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/7) (minibots).
- **Non-climb endgame** is the significant minority ask: [Tricks1228, #16](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/16), [AgentSmith451, #118](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/118) — *"Please no more 'climbing a horizontal bar' endgames for a while."*

### 7.4 Non-game season context worth carrying into the review `[VERIFIED]`

- **SystemCore is mandatory in 2027; roboRIO will not run alongside it.** Every team receives one in the year-specific KoP. ([WPILib](https://docs.wpilib.org/en/latest/docs/software/systemcore-info/systemcore-introduction.html), [2027 Control System Testing Reminder](https://community.firstinspires.org/2025-control-system-testing-reminder-for-2027)) `[COMMUNITY-CONSENSUS]` This is a top-3 season anxiety — [rktut-frc2881, #174](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/174) (24 likes): *"BIOCORE? How about a timely and functional SYSTEMCORE before kickoff?"* `[SPECULATION]` [martinma, #56](https://www.chiefdelphi.com/t/26-27-first-robotics-season-teaser-revealed/513367/56) argues the GDC will *not* nerf swerve, partly because *"GDC is pushing more robot autonomy and swerve is the ideal platform for that vision."*
- **Field reset time** is a live complaint — [cottagechez, #12](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/12) (32 likes) asks for *"a sub-7.5 minute field reset."* `[SPECULATION]` A 40–80-element field resets far faster than 504 balls; this may be a *design driver* for the low count, not just a cost decision.
- **Field elements through a standard door** — [BillDunlap, #118](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/118) (12 likes); simple field elements is the #2 ask overall ([Zook, #11](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/11), 53 likes).
- `[COMMUNITY-CONSENSUS]` A rules issue teams want fixed and that will matter for loophole review: **G415/G416** (robot damage/disabling → automatic red card) is argued to be over-punitive and non-intent-based, with a worked Einstein-adjacent example in [AI_orange, #37](https://www.chiefdelphi.com/t/things-youre-hoping-for-in-biocore/519917/37). Also flagged: bumper-mounted "ramps"/deflectors weighed with bumpers as a weight-rule loophole.

---

## 8. Sourcing gaps — what I could not get

- **Reddit** (`r/FRC`, `r/FIRSTRobotics`) is blocked to this toolchain (robots.txt / 403 on both search and JSON APIs). Not covered. `[SPECULATION]` Based on cross-references in the CD threads, reddit's 2027 discussion appears to be downstream of CD rather than a distinct source. `[RECHECKED 2026-08-22]` A targeted web search for BIOCORE reddit discussion returned **zero reddit results** and only Chief Delphi pages — consistent with the read that CD is the primary venue and reddit is derivative.
- **Discord** is not web-indexed; no summaries found.
- **Ri3D**: no 2027 team roster or announcement exists yet. Ri3D groups announce Nov–Dec; the [AndyMark Ri3D page](https://andymark.com/pages/meet-the-ri3d-teams) has no 2027 content. Re-check December 2026.
- **The Blue Alliance blog**: no BIOCORE preview content found.
- **Podcast/YouTube**: no substantive BIOCORE-specific episode surfaced. Off-season FRC media has been dominated by SystemCore, VEX/RECF, and FIRST in Texas ceasing operations.
- **Images**: several CD posts contain image-only evidence I could not visually inspect — notably [Zack_Osowski #35's screenshot](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/35) and [HeroBrayden #39's "Ranger Danger" screenshot](https://www.chiefdelphi.com/t/frc-blog-pre-orders-for-2027-scoring-elements/521731/39). Worth a human look.
- **USPTO**: no BIOCORE filing located by web search. `[RETRIED 2026-08-22 — still blocked]` The TSDR bulk API now requires a registered API key (*"Beginning October 2, you'll need to register for an API key to download bulk data from our TSDR APIs"*), and the `tmsearch.uspto.gov` search endpoint rejects unauthenticated queries. **This needs a human with a free [USPTO API account](https://account.uspto.gov/api-manager/)** — roughly a 5-minute signup. Worth doing: the goods-and-services description occasionally hints at element form, and FIRST files these well before kickoff.
- **AndyMark rate engine**: the contradiction in §2.3 (999 lb placeholder vs. returned USPS rates) could be resolved by a live checkout rate query, which requires an active cart session. **Not attempted** — that is a state change against a vendor's live commerce system for a marginal gain. A human can settle it in 60 seconds by adding a KoP to a cart and reading the quoted rates.

---

## 9. What to monitor between now and 2027-01-09

| Date | Event | Intel value |
|---|---|---|
| 2026-09-12 | FTC BIOBUZZ kickoff | Reveals how FIRST is theming CANOPY; weak FRC signal |
| 2026-09-24 | FRC Round 1 preferencing opens | Logistics only |
| Oct–Dec 2026 | FRC blog "Counting Down to 2027 Kickoff" | **High** — historically carries KoP contents, and 2026's FTC analogue leaked robot-task guidance |
| Nov–Dec 2026 | Ri3D team announcements | Medium |
| Dec 2026 | AndyMark packing / customs photos; KoP box manifests | **Highest realistic leak vector** for element form factor |
| **Weekly, starting now** | **`am-5901` variant weight flips off the 999.0 lb placeholder** | **HIGHEST — and it is a one-line poll.** See §2.3. A real weight settles mass-per-element and collapses §2.2's whole table. Poll: `curl -s https://andymark.com/products/biocore-frc-scoring-element-pre-order.json \| python -c "import json,sys;[print(v['sku'],v['weight'],v['weight_unit']) for v in json.load(sys.stdin)['product']['variants']]"` — alert on anything ≠ 999.0 |
| Dec 2026 – Jan 2027 | Any AndyMark spec-tab update on `am-5901` | **Highest** — dimensions/weight would settle most of §2 |
| Early Jan 2027 | "Coffee with Collin" pre-kickoff video | Historically a troll; log it anyway |

---

## Predicted game shape — a betting sheet

Eleven falsifiable calls to score against the real manual on 2027-01-09. Confidence is my own, not the community's; where I disagree with community consensus I say so. `[2026-08-22: P1 raised, P9 lowered, P11 added — all three driven by §2.3.]`

**P1 — The BIOCORE scoring element is NOT a sphere ≤3.5 in diameter, and is not the FTC POLLEN part. — 90%** `[raised from 88% on 2026-08-22]`
Reasoning: `am-5901` is separately tooled from `am-5851` (POLLEN) and `am-3376a` (Artifact); FIRST calls it "custom… with properties specific to BIOCORE." Implied unit price of $12–23 is 7–13× POLLEN's $1.83. **New:** §2.3's same-box observation is independent geometric evidence — KoP and 2/5-field ship in one box despite a ~5× quantity difference, which spheres cannot do at 64% packing and zero nesting. Two unrelated evidence chains (price, packing) now agree. *Falsified if:* the element is a small ball. *Note:* this directly contradicts the task brief's premise.

**P2 — Fewer than 150 scoring elements on the official full field; most likely 36–90. — 80%**
Reasoning: §2. Discount-corrected field/KoP ratio ≈ 13.4 vs REBUILT's 50.4; full-field pre-order cost fell 68% ($2,630 → $845); Garrison's $26 vs $230 shipping datum. *Falsified if:* the manual's field element count exceeds 150. **This is the highest-information prediction here — everything downstream depends on it.**

**P3 — The robot holding limit (the manual's stated max) is 2, 3, or 4. — 78%**
Reasoning: FIRST states it is >1; KoP > holding limit; KoP is 3–6 across the whole plausible price band. *Falsified if:* the limit is 1, or ≥5.

**P4 — Scoring is dominated by controlled placement/insertion into structures, not by high-rate flywheel launching. A team that builds only a REBUILT-style shooter is non-competitive. — 68%**
Reasoning: 40–90 elements with a 2–4 hold gives ~10–25 cycles/robot/match — a placement economy. Plus the shooter→PnP alternation (§6.1) and cottagechez's "the turret meta is solved" argument. *Against:* SM7160's genuinely good point that a stated multi-piece holding limit historically correlates with balls (2012/2020/2022), and back-to-back shooters are precedented. *Falsified if:* the primary scoring action is launching.

**P5 — There are ≥3 scoring locations or height tiers of differing point value for the single element type. — 72%**
Reasoning: one element type + a low element count forces the scoring gradient into *geometry*. Community's most repeated structural guess; also the mechanism behind HEFZZJM's multi-target thesis. *Falsified if:* there is one goal, or all locations are worth the same.

**P6 — The endgame is a climb/ascent (not a floor platform or balance), scored in ≥2 tiers, and worth ≥15% of a typical winning alliance's match score. — 62%**
Reasoning: CANOPY/canopy/vine theming; three consecutive climb endgames as base rate; near-unanimous community expectation of an overcorrection after REBUILT's weak climb. *Against:* Mo-tion's platform-is-due argument (2019, 2023) and a real chorus asking for non-climb. *Falsified if:* it's a platform/balance, a non-elevation task, or a single-tier climb worth <15%.

**P7 — Ranking points: 2 or 3 objective RPs plus Win/Tie, and at least one is a cumulative scoring-volume threshold (an "Energized"-style count). — 78%**
Reasoning: FRC has used threshold-count RPs every year since 2018; REBUILT used two of them plus an endgame RP. *Falsified if:* zero volume-threshold RPs, or ≥4 objective RPs.

**P8 — The scoring element is neutral (not alliance-coloured). — 72%**
Reasoning: FIRST says "one *type*"; AndyMark lists a single `am-5901` with no colour variants, whereas it split DECODE artifacts into purple/green SKUs. *Against:* [JerJerBinks](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/91) and [HeroBrayden](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/188) — 5 years since alliance-coloured pieces, and FRCAlum's data shows they're historically not rare. *Falsified if:* red/blue variants exist.

**P9 — The element is rigid or semi-rigid moulded plastic/rubber, not inflatable, and not high-density foam. — 50%** `[lowered from 55% on 2026-08-22]`
Reasoning: $12–23/unit and "custom manufactured overseas" fit injection/rotational moulding; foam balls cost ~$2 (REBUILT) and would need 400+ units. *Against:* Garrison and AgentSmith451 read the cheap shipping as inflatable/compressible; HeroBrayden reads it as collapsible. **Downgraded because §2.3 showed the shipping evidence this rests on is contaminated** — AndyMark's 999.0 lb placeholder cannot generate the observed USPS quotes, so the rate engine's inputs are unknown. A rigid *nesting* shape (P11) and a collapsible shape explain the ladder equally well, and I can no longer separate them. **This remains the call most likely to be wrong — treat it as a coin flip.** *Falsified if:* inflatable, foam, or fabric.

**P10 — The manual contains an explicit numeric possession/CONTROL rule (a G-rule capping simultaneous control at the holding limit), with a violation ladder, and it becomes a top-5 source of match-affecting fouls. — 82%**
Reasoning: FIRST has pre-announced a holding limit, which always ships with a control rule; historically these generate definitional loopholes around "control" vs "contact" vs "herding" (2019 Cargo, 2022 Rapid React, 2026 FUEL). **This is the first place to look for exploitable ambiguity on kickoff day** — specifically: does the limit apply during AUTO, does it apply while touching a scoring structure, what counts as CONTROL of an element resting on the robot, and is there a plow/herding exception.

**P11 — The element's geometry is nesting/stackable — a cone, ring/torus, disc, or open bowl/shell — rather than a solid convex blob. — 60%** `[NEW 2026-08-22]`
Reasoning: §2.3. KoP, 1/5-field, and 2/5-field all ship in the same box while differing ~5× in quantity, and the first rate step is at 3/5. That pattern means the carton is sized by one element's largest dimension and additional elements consume little marginal volume — the signature of nesting. Every historical FRC piece in the implied $12–23 band that also nests is one of these four shapes (2023 CONE $12.29; 2013 FRISBEE; Logomotion tubes). Botanical/CANOPY theming fits a pod, shell, or seed-ring. **Design consequence if true:** intakes must handle a *specific orientation*, not just a rolling ball; a nesting shape means field-reset piles are ordered, floor pickup involves de-nesting two stuck-together elements, and "two elements jammed as one" becomes a real failure mode and a likely Q&A topic. *Against:* the shipping evidence is caveated (see §2.3); a small dense blob shipped in a minimum-size carton produces the same flat rate. *Falsified if:* the element is a sphere, a solid convex shape, or does not nest.

---

### Two cross-cutting warnings for the post-kickoff review

1. **P2 is load-bearing.** If the manual shows a high element count, then §2's arithmetic is wrong somewhere (most likely the bulk-discount assumption or a non-linear SKU margin), and P4/P5/P9/P11 should all be re-derived rather than salvaged. `[2026-08-22]` P2 is now supported by **two independent chains** — the price ratio (§2.2) and the shipping ladder (§2.3) — which agree. That is reassuring but not independent *proof*: both ultimately derive from AndyMark's pricing/logistics rather than from FIRST, so a single AndyMark packaging decision could skew both at once.
2. **The whole corpus is one forum.** Chief Delphi's ~1,200 relevant posts across 8 threads are ~90% of the recorded pre-season thinking, and the highest-liked posts in the main thread are jokes ([Aaron_Li, #15](https://www.chiefdelphi.com/t/2027-game-predictions-biocore-presented-by-haas/519808/15), 41 likes: *"Mitochondria is the powerhouse of the cell"*). Signal density is low. The pre-order arithmetic in §2 and the FIRST blog facts in §1 are worth more than every prediction in §5–§7 combined — including mine.
