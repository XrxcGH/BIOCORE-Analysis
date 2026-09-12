# Team ______ — AI Use Policy

**Adopted:** ____________  **Review date:** ____________  **Owner:** ____________ (mentor)
**Season:** 2027 — BIOCORE™ presented by Haas · FIRST® Robotics Competition · FIRST CANOPY℠

*Fill the four blanks above, print it, sign it, post it in the shop, send a copy home.*

---

## Why this exists

*FIRST* **permits** AI. Its own words: teams may use AI "to assist in the creation of award
submissions, handouts, writing robot code, etc." *FIRST* treats AI as a tool in the same class as CAD
programs and 3D printers, tells judges not to rank a team lower for using it, and tells them that
AI-detection sites are unreliable. (Sources: *FIRST*'s Submitted Awards page and the 2026 Judge
Manual, Ch. 4, "Use of Artificial Intelligence (AI).")

*FIRST* requires **one** thing in return: **proper credit and attribution.**

This policy is how our team earns that permission responsibly. It is one page on purpose.

---

## 1. Safety-critical code

Our robot is a machine that can weigh well over 100 lb and move under its own power. Software failure
is a physical-safety event, not a bug report.

1. **No generated code is deployed to the robot until a human has read every line of it.**
2. **AI never sets a number that describes physical reality.** Current limits, soft limits, PID and
   feedforward gains, gear ratios, mass, field dimensions, and mechanism travel come from
   **measurement, SysId, or the Game Manual**. A number produced by a model has the syntax of a
   measurement and none of the truth of one. This is the most dangerous failure mode there is.
3. **Every WPILib and vendor-library call is verified against the 2027 documentation**
   (`docs.wpilib.org/en/2027/`). The 2027 season replaces the roboRIO with **Systemcore** and rewrites
   WPILib: `edu.wpi.first.*` became `org.wpilib.*`, `robotInit()` is gone, `Servo`, `Ultrasonic`,
   `Relay`, `Counter`, and `SPI` are removed, and `Rotation2d` angle getters now return **wrapped**
   angles. **Every FRC code example published before 2027 is wrong, and much of it still compiles.**
   Assume any AI-suggested WPILib API is stale until you have checked it.
4. **A student can explain every line, or it does not merge.** This applies identically to code copied
   from Chief Delphi, from another team's repository, or from a model. Enforced at pull-request review.

## 2. Awards integrity and attribution

5. **Every AI-assisted submission, handout, and repository carries the team attribution line:**

   > *Portions of this work were created with AI assistance (Claude, Anthropic) by Team ______.
   > All content was reviewed, verified, and is understood by the students credited.*

   The line lives in **one** file (`ops/ATTRIBUTION.md`) and is copy-pasted, never retyped.
   *FIRST*'s own example of acceptable credit is *"Essay created by Team XXXX and ChatGPT."*
6. **Essays state what students actually did, in students' own voice.** A model can cut a paragraph
   to a character limit, restructure an argument, or catch a repeated word. It cannot know what
   happened at our outreach event, and it must never be allowed to invent it.
7. **Every factual claim traces to something we did.** Numbers of students reached, hours served,
   sponsor names, event dates: if you cannot point at the record, it does not go in.
8. **If you cannot answer a judge's question about a document, you do not submit it.** Judges evaluate
   students, not artifacts. This is the real test and it is unforgiving.
9. **Log what AI wrote.** Not to punish anyone — so that when something behaves oddly we know which
   work got human scrutiny and which did not.

## 3. Data privacy — we are a team of minors

10. **Accounts are held by adults.** Claude requires all account holders to be **18 or older**; there
    is no parental-consent or supervised-minor account. Mentors — and any student who is genuinely 18+
    — hold the accounts. **No student under 18 creates a Claude account for team work.** GitHub
    accounts are different and every student should have their own.
11. **Under-18 students work in paired sessions**, on a shared screen, in the shop. The student owns
    the problem, states the goal, judges the output, and decides what is committed. The adult drives
    the keyboard. **This is not a workaround; it is how the learning actually happens.**
12. **Never enter into any AI tool:** student full names combined with school and grade, home
    addresses, phone numbers, dates of birth, student ID numbers, medical or IEP information,
    disciplinary records, photographs of identifiable minors, or anything exported from a school
    information system.
13. **Public robotics data is fine.** Team numbers, match results, scouting observations of robot
    capability, our own rule analysis, and our own code are all fine.
14. **Conversation history is visible to whoever holds the account.** Say this out loud rather than
    discovering it later. It is supervision, not surveillance.
15. **We follow ____________ School District's acceptable-use and AI policy**, which is stricter than
    this page and overrides it wherever they differ. Read it. *FIRST*'s permission does not override
    your district.

## 4. Verification

16. **Read it before you run it.** Every time.
17. **Compile, test, and explain — in that order — before merging.** Some 2027 changes are renames
    (the compiler catches them) and some are silent behaviour changes (it does not).
18. **Content you fetch is data, not instructions.** A web page, PDF, or chat message that tells the
    AI to "ignore previous instructions" is text we read, never a command we obey. Bring anything like
    that to a mentor.
19. **Grant write access per task, never standing.** An agent that can push to `main` or overwrite the
    Impact essay is an agent that will, eventually, at the worst possible moment.
20. **Stop and think when you are going in circles.** Three failed attempts at the same problem means
    the problem is misunderstood, not that the prompt was bad. Go find a mentor or a whiteboard.

---

## What this policy is *for*

We use AI so that **desk work stops eating shop time** — so the hours go into building, wiring,
machining, and driving instead of into boilerplate and formatting. If it ever starts replacing the
thinking instead of the typing, it has failed and we stop.

---

## Signatures

By signing, I confirm I have read this page and will follow it.

| Name | Role | Date | Signature |
|---|---|---|---|
| | Mentor | | |
| | Student | | |
| | Student | | |
| | Student | | |
| | Student | | |
| | Student | | |

*(Add rows as needed. One page, one signature, once a season.)*

---

**Parent/guardian note.** Our team uses AI tools (Claude, GitHub Copilot) the way we use CAD software
and 3D printers — as tools, under supervision. All accounts are held by adult mentors. Students never
enter personal information. All AI-assisted work is disclosed to *FIRST* as their rules require.
Questions: ____________________ (mentor name and contact).

---

*Template source: `reference/ai-integration/templates/team-ai-policy.md` ·
Policy authority: `reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md` ·
Infrastructure and rationale: `reference/ai-integration/05_ai_infrastructure_and_policy.md`*
