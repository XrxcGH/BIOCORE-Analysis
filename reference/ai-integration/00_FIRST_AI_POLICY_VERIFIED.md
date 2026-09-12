# FIRST's official stance on AI use — VERIFIED

Verified 2026-08-21 by the top-level session. **This file is authoritative for this project.**
If any other document here contradicts it, this file wins.

## The headline: AI is explicitly permitted

> Teams are permitted to use Artificial Intelligence (AI) to assist in the creation of award
> submissions, handouts, writing robot code, etc.

Source: the [Submitted Awards page](https://www.firstinspires.org/resources/library/frc/submitted-awards)
and the [2026 Judge Manual](https://www.firstinspires.org/hubfs/web/program/frc/awards/judge-manual.pdf),
Ch. 4, "Use of Artificial Intelligence (AI)", p. 14.
`[AUDIT 2026-09-12]` The quotes in this file are cut to the permission and attribution sentences, and
the rest of the passage is paraphrased. The full text is in `../awards/_text/judge-manual.txt`, which
`bash tools/rebuild-corpus.sh` rebuilds locally because FIRST's text is not redistributed.

FIRST frames AI as **a tool in the same category as CAD and 3D printers** — not as a compromise or a
gray area. This is a permissive, unambiguous policy.

## The one binding obligation: attribution

> Teams using AI to assist with code or content generation must provide proper credit and
> attribution, and respect intellectual property rights and licenses.

FIRST's example of proper credit: **"Essay created by Team XXXX and ChatGPT."**

**Action item:** adopt a standing attribution line on every AI-assisted award submission, handout, and
code repository. Put it in the team AI policy and the repo README. Cost of compliance ≈ zero; cost of
non-compliance is an integrity finding.

## Judges may not penalize AI use

Judges are told not to discredit a team, or rank it lower, simply because it used AI. Teams are
compared on what they accomplished against the award judging guidelines.

FIRST also warns against AI-detection tools: it tells judges that sites claiming to detect AI use are
unreliable and must not be used to check a submission.

## Award submission hard limits (2026 season, for calibration)

| Item | Limit |
|---|---|
| Executive summary | **500 characters** incl. spaces and punctuation |
| Essay | **10,000 characters** incl. spaces and punctuation |
| 2026 submission deadline | Thursday, **February 12, 2026, 3:00 p.m. ET** |

⚠️ These are **2026** figures. Re-verify the 2027 equivalents when FIRST publishes them —
expect the BIOCORE-season deadline in **mid-February 2027**.

## What this policy does NOT do

FIRST's permission is about **eligibility and judging**. It does not address:

1. **Your school district's** academic-integrity and AI policy — usually stricter. Check it.
2. **Student learning.** Permission to use a tool is not a reason to skip the thinking. The whole
   point of the AI plan in this project is to move student hours *toward* hands-on work, not to
   remove students from the intellectual work.
3. **Safety-critical robot code.** No policy makes unverified generated code safe on a robot that is
   legal up to **115.0 lb** bare (2026 R103, excluding BUMPERS, battery, and event location tags) and
   **135.0 lb** with BUMPERS (2026 R408). Human review before anything actuates remains non-negotiable.
   `[AUDIT 2026-08-22]` Corrected from "125 lb", which matches neither limit.
4. **Minors' data and account terms** — `[AUDIT 2026-08-22, revised by team-ops audit]`
   [`05_ai_infrastructure_and_policy.md`](05_ai_infrastructure_and_policy.md) **now exists** and its
   §2 covers this in detail: Anthropic requires all Claude account holders to be **18+** with no
   parental-consent flow and no supervised-minor account type **[C]**, so the mentor holds every
   account and students work at the keyboard beside them. It also covers COPPA, FERPA and state
   minor-privacy law. That file is the operational authority on accounts; **this file remains the
   authority on FIRST's competition stance only.** Your district's own AI and data policy still
   binds independently — check it directly.

## Sources

- [FIRST Impact Award Resources](https://www.firstinspires.org/resources/library/frc/fia-resources)
- [Submitted Awards — FIRST Robotics Competition](https://www.firstinspires.org/resources/library/frc/submitted-awards)
- [2026 Season Award Updates — FIRST Community Blog](https://community.firstinspires.org/2025-season-award-updates-for-2026)
- [2026 FIRST Leadership Award Guide (PDF)](https://info.firstinspires.org/hubfs/web/program/frc/awards/first-leadership-award-guide.pdf)
