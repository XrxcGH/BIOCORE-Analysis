# BIOCORE KICKOFF PLAYBOOK

**The operating document for the deep AI review that runs the moment the BIOCORE manual drops.**

| | |
|---|---|
| **Target event** | FRC **BIOCORE presented by Haas** kickoff & game reveal — **Saturday, January 9, 2027, 12:00 p.m. ET** `[VERIFIED]` ([FRC Game & Season](https://www.firstinspires.org/programs/frc/game-and-season)) |
| **Written** | 2026-08-22 (T−140 days) |
| **Audience** | The mentor running the review, and the model doing it |
| **Scope** | Everything from "the PDF exists" to "the team has a one-page strategy brief" — target **4 hours** on kickoff day, **72 hours** to full output |
| **Not in scope** | Pre-kickoff intel gathering (that is [`research/03_biocore_official_intel.md`](research/03_biocore_official_intel.md) and [`research/04_biocore_community_intel.md`](research/04_biocore_community_intel.md)) |

**Tag convention used throughout, and required of every output this playbook produces:**

| Tag | Means |
|---|---|
| `[VERIFIED]` | Quoted or computed from a primary source, with the source named |
| `[COMPUTED]` | Derived by a script in `tools/` from data in this project |
| `[INFERENCE]` | Follows logically from a `[VERIFIED]` fact; the chain is stated |
| `[SPECULATION]` | A guess. Confidence stated as a percentage or it does not ship |

> **The single most important instruction in this document:** the BIOCORE manual will contain rules that no prior manual contained. Everything in this project is a *prior*, not an answer. The moment the real text contradicts a prior here, **the real text wins and the prior gets deleted, not reconciled.**

---

## Document map — what exists and when you use it

| File | Phase | What it gives you |
|---|---|---|
| [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) | Read first, once | The FTC-vs-FRC firewall. "Pollen", StarterBots, Skill Builders are **FTC BIOBUZZ**, not BIOCORE. Do not let them into the review. |
| [`research/03_biocore_official_intel.md`](research/03_biocore_official_intel.md) | 0, 1 | Every published BIOCORE fact + the 33 "open questions the manual will answer" — Phase 1's questionnaire is the answer sheet for that list |
| [`research/04_biocore_community_intel.md`](research/04_biocore_community_intel.md) | 2, 5 | The 10-item betting sheet (P1–P10). Score it against the manual in Phase 2 — a wrong prior is diagnostic |
| [`research/02_supplemental_docs_index.md`](research/02_supplemental_docs_index.md) | 0, 4 | Document precedence chain, the kickoff-day URL fetch list (§12), version-drift trap (§1.5) |
| [`reference/QA-AMBIGUITY-HOTSPOTS.md`](reference/QA-AMBIGUITY-HOTSPOTS.md) | 0, 4 | Empirical map of which rules teams cannot parse. Read the hot blocks first. |
| [`reference/FRC_VS_FTC_ORIENTATION.md`](reference/FRC_VS_FTC_ORIENTATION.md) | Read first, once · 2, 3, 6 | `[NEW 2026-08-22]` The FRC structures with no FTC analogue: **no bag day**, district points (awards and being picked are literally scoring), event weeks, 8-alliance double elimination, Ranking Score as a *mean*, the I101–I107 inspection flow, Q&A timing. Everything in it changes what "a good BIOCORE robot" means. |
| ~~`reference/robot_construction_rules.md`~~ | 3 | **DOES NOT EXIST** `[AUDIT 2026-08-22]` — never written. Use §3.2's own extraction table, seeded from `research/rule_inventories/2026_rules.tsv` (R-prefix rows carry headline + page). |
| ~~`reference/loopholes_and_exploits.md`~~ | 4 | **DOES NOT EXIST** `[AUDIT 2026-08-22]` — never written. §4.1's pass is self-contained; the empirical substitute is `reference/QA-AMBIGUITY-HOTSPOTS.md` plus `research/rule_inventories/churn_semantic.tsv`. |
| [`reference/team-ops/03_programming_stack.md`](reference/team-ops/03_programming_stack.md) | 3, 5 | SystemCore / WPILib 2027 reality — the transition tax |
| [`reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`](reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md) | 6 | Real 2026 award slate (Dean's List is gone; it is the **FIRST Leadership Award**) |
| [`reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md) | 6 | AI is explicitly permitted; **attribution is mandatory** on anything submitted |
| `research/rule_inventories/` | 0 | 2016–2026 structured rule corpus — the diff baseline |
| `research/predictive_tba/` | 2 | Seed→win rates, week-by-week score inflation, auto share of score |
| `tools/` | 0 | Extraction and analysis scripts |

> `[AUDIT 2026-08-22]` Verified by exhaustive filesystem walk: **`robot_construction_rules.md` and `loopholes_and_exploits.md` do not exist anywhere in this project.** An earlier note here said they "may land in `reference/` or `research/`" — they did not. Do not spend kickoff-day minutes hunting for them. Every other file in this table was confirmed present.

---

## How to use this

### The 60-second orientation

1. **Do not watch the reveal and then read the manual.** Download the PDF first, start Phase 0 while the animation plays. The kickoff video is marketing; the manual is the game.
2. **Run Phase 0 mechanically.** It is scripts, not thinking. 15 minutes, zero judgment calls. It produces the artifacts every later phase reads.
3. **Do Phase 1 before you have any opinion.** Comprehension before strategy. The single biggest failure mode on kickoff day is strategizing against a misread rule.
4. **Phases 2–4 are the AI review proper.** Paste the prompts from [§Ready-to-paste prompts](#ready-to-paste-prompts) in order. Each one is written to produce mentor-grade analysis, not a summary.
5. **Phase 4 has a deadline.** Q&A opens ~4 days after kickoff and answers are binding. Questions filed in week 1 get answered before the queue floods and are the ones that can still cause a Team Update. `[VERIFIED — 2026 manual §1.9]`
6. **Phase 6 is what the students actually get.** Four artifacts, one page each. Everything upstream is scaffolding.

### Step 1 — Ingest the manual

**`tools/ingest-manual.sh` does not download anything.** It contains no network code. It takes a **local PDF path** as its first positional argument. Step 1 is therefore two commands, in this order: fetch, then ingest.

> `[AUDIT 2026-08-22]` A previous version of this section documented `bash tools/ingest-manual.sh` with no arguments, and `--url` / `--file` flags. **None of those work** — no-args aborts on `${1:?usage}`, and the flags are parsed as filenames and die with `!! no such file: --url`. The syntax below was executed end to end against the 2025 REEFSCAPE manual on 2026-08-22 and completed successfully (164 pp, 229 rules, 9 added / 7 removed / 153 changed vs. the REBUILT baseline).

#### 1a. Fetch and freeze

```bash
# Run from the repository root. On a fresh clone, run the corpus rebuild first
# (bash tools/rebuild-corpus.sh --fetch, then bash tools/rebuild-corpus.sh; see README.md).
B=https://firstfrc.blob.core.windows.net/frc2027
mkdir -p manuals/archive/frc manuals/2026-27_BIOCORE/sections manuals/archive/supplemental logs
TMP=$(mktemp -d)

# The manual. 2026 used /Manual/2026GameManual.pdf (verified live); try that shape first.
GOT=
for u in "$B/Manual/2027GameManual.pdf" "$B/Manual/2027FRCGameManual.pdf" \
         "$B/Manual/2027BIOCOREGameManual.pdf"; do
  code=$(curl -sL --max-time 180 -o "$TMP/m.pdf" -w "%{http_code}" "$u")
  if [ "$code" = 200 ] && head -c4 "$TMP/m.pdf" | grep -q '%PDF'; then
    cp "$TMP/m.pdf" "manuals/archive/frc/2027_BIOCORE_GameManual.pdf"; GOT=$u; echo "GOT $u"; break; fi
done
[ -n "$GOT" ] || echo "!! nothing downloaded — check the Season Materials webpage for the real filename"

# FREEZE IT. The PDF mutates in place at the same URL all season.
cp "manuals/archive/frc/2027_BIOCORE_GameManual.pdf" \
   "manuals/2026-27_BIOCORE/2027_BIOCORE_GameManual_KICKOFF_$(date +%Y%m%dT%H%M).pdf"
sha256sum manuals/archive/frc/2027_BIOCORE_GameManual.pdf | tee -a logs/manual_hashes.txt

# Supplementals worth having in hour one. Names change most years — expect some 404s.
curl -sLO --output-dir manuals/archive/supplemental "$B/Manual/2027FRCInspectionChecklist.pdf"
curl -sLO --output-dir manuals/archive/supplemental "$B/FieldAssets/2027-field-dimension-dwgs.pdf"
```

If FIRST renamed something (they do, most years — see [`02_supplemental_docs_index.md` §12 and §14](research/02_supplemental_docs_index.md)), download the manual by hand from the Season Materials webpage and save it to that exact path.

The **filename `2027_BIOCORE_GameManual.pdf` under `manuals/archive/frc/` is load-bearing** — `tools/rule-inventory.py` matches `^(\d{4})_([A-Z0-9]+)_GameManual\.pdf$` and will silently skip anything else.

#### 1b. Ingest

```bash
# usage: ingest-manual.sh <manual.pdf> [label]        label defaults to V1
bash tools/ingest-manual.sh "manuals/archive/frc/2027_BIOCORE_GameManual.pdf" V1
```

Re-run it after every republish, with the Team Update number as the label, to diff BIOCORE against **itself**:

```bash
BASELINE="manuals/2026-27_BIOCORE/BIOCORE_GameManual_V1.pdf" \
  bash tools/ingest-manual.sh "manuals/archive/frc/2027_BIOCORE_GameManual.pdf" TU03
```

Outputs land in `manuals/2026-27_BIOCORE/ingest_<LABEL>_<UTC-STAMP>/`; the run log goes to `logs/`. Default `BASELINE` is the 2026 REBUILT manual, which is what you want for the V1 run and wrong for every run after it.

### Step 2 — The exact prompt to start the review

Paste this, verbatim, as the first message of the review session:

```text
You are running the BIOCORE kickoff review. Project root: the repository root (the directory holding KICKOFF_PLAYBOOK.md)

Operating document: KICKOFF_PLAYBOOK.md — read it in full before doing anything else, then read
research/00_PREMISE_CORRECTION.md, reference/QA-AMBIGUITY-HOTSPOTS.md, and
research/02_supplemental_docs_index.md sections 1 and 12.

The BIOCORE manual is at manuals/archive/frc/2027_BIOCORE_GameManual.pdf.

Execute Phase 0 of the playbook now, end to end, using the tools in tools/. Do not summarize the
game. Do not offer strategy. Produce only the Phase 0 artifacts and the filled-in Manual Fingerprint
Card, and then stop and report the Phase 0 exit-criteria checklist with each item marked PASS or FAIL.

Rules for this entire session:
- Every factual claim about the game cites a rule ID and the manual page it came from. No exceptions.
- Tag every statement [VERIFIED] / [COMPUTED] / [INFERENCE] / [SPECULATION]. Untagged = rejected.
- Where the manual is ambiguous, say "ambiguous" and quote the exact sentence. Do not resolve it by
  guessing intent — the manual states it means exactly and only what it says.
- Prior-season expectations in this project are priors, not facts. When the BIOCORE text contradicts
  one, say so explicitly and flag the file that needs correcting.
- I am an experienced FRC/FTC mentor. Write for me, not for a student. No recaps of things I can read
  myself; spend the words on things I would miss.
```

### Kickoff-day clock

| Clock | Phase | Output |
|---|---|---|
| **T−0:30** | Pre-position | Terminal open at project root, `tools/` verified runnable, this file read |
| **T+0:00** | Reveal begins | Start probing the CDN. Assets frequently stage before the video ends |
| **T+0:15** | Manual in hand | **Phase 0** — mechanical ingest |
| **T+0:30** | | **Phase 1** — comprehension questionnaire |
| **T+1:30** | | **Phase 2** — scoring strategy |
| **T+2:30** | | **Phase 3** — design strategy, archetype shortlist |
| **T+3:30** | | **Phase 4** — loophole pass + Q&A draft list |
| **T+4:30** | | **Phase 5/6** — pitfalls, deliverables |
| **T+1 day** | | Re-run Phase 0 on any republished PDF; re-read after sleep |
| **T+3 days** (Jan 12) | First Team Update | `[VERIFIED pattern]` Tue+Fri cadence begins |
| **T+4 days** (~Jan 13) | **Q&A opens** | Submit the Phase 4 question list **this week** |

---

## Phase 0 — Mechanical ingest (0–15 min)

No judgment. Run it, check the artifacts exist, move on.

`[AUDIT 2026-09-12]` On a fresh clone, run `bash tools/rebuild-corpus.sh --fetch` and then `bash tools/rebuild-corpus.sh` before anything in this phase, so the prior-season comparisons have their inputs: earlier manuals and the text extracted from them are not tracked in the repository ([README.md](README.md#what-is-not-in-this-repository)).

### 0.1 Freeze the artifact — do this before anything else

`[VERIFIED]` The manual PDF is **republished at the same URL** all season, and in 2026 FIRST replaced the per-page version footer (`V0`…`V13`) with a single whole-document `Version: TU22` stamp — destroying the signal that told you which pages moved. In 2023 only **3 pages** and in 2025 only **5 pages** survived the season untouched. ([`02_supplemental_docs_index.md` §1.5](research/02_supplemental_docs_index.md))

**Therefore:** timestamped copy + SHA-256 of every version you ever download, from minute one. You are building your own diff history because FIRST no longer gives you one.

```bash
cp manuals/archive/frc/2027_BIOCORE_GameManual.pdf \
   "manuals/2026-27_BIOCORE/2027_BIOCORE_GameManual_$(date +%Y%m%dT%H%M).pdf"
sha256sum manuals/2026-27_BIOCORE/*.pdf >> logs/manual_hashes.txt
```

### 0.2 The seven extractions

| # | Extraction | Command | Artifact |
|---|---|---|---|
| A | Layout text | `pdftotext -layout manuals/archive/frc/2027_BIOCORE_GameManual.pdf research/rule_inventories/_text/2027.txt` | `_text/2027.txt` |
| B | Rule inventory | `python tools/rule-inventory.py --min-year 2024 --max-year 2027` | `research/rule_inventories/2027.json`, `2027.txt`, `_counts.csv`, `_matrix.csv` |
| C | Full rule bodies | see 0.2C below | `2027_rules_full.txt`, `2027_rules.tsv` |
| D | Semantic diff vs 2026 | `python tools/rule-taxonomy-analyze.py` | `churn_pairs_2026_2027.tsv`, `evergreen_semantic.tsv` |
| E | Number harvest | see 0.2E | `research/rule_inventories/2027_numbers.tsv` |
| F | Undefined ALL-CAPS terms | see 0.2F | `research/rule_inventories/2027_newterms.tsv` |
| G | Violation ladder | see 0.2G | `research/rule_inventories/2027_violations.tsv` |

**0.2C — full rule bodies.** `rule-inventory.py` writes `2027.json` with `{id, prefix, num, page, title, body, changed_by_update}` per rule. The downstream tools (`rule-show.py`, `rule-taxonomy-analyze.py`) read the flat `<year>_rules_full.txt` / `<year>_rules.tsv` format instead, and **the script that produced those for 2016–2026 was not saved to `tools/`.** Regenerate from the JSON:

```bash
python - <<'PY'
import json,re,os
R="research/rule_inventories"  # relative path: run from the repository root
d=json.load(open(f"{R}/2027.json",encoding="utf-8"))
full=open(f"{R}/2027_rules_full.txt","w",encoding="utf-8")
tsv=open(f"{R}/2027_rules.tsv","w",encoding="utf-8")
full.write(f"# FRC 2027 game manual -- reconstructed rule text\n# source: {d['source']}   rules: {d['count']}\n")
tsv.write("rule_id\tprefix\tnum\tpage\tstmt_chars\tviol_chars\theadline\n")
for r in d["rules"]:
    b=r["body"]; m=re.search(r"(Violation:.*?)(?=$)",b,re.S)
    viol=m.group(1).strip() if m else ""
    stmt=b[:m.start()].strip() if m else b.strip()
    full.write("\n"+"="*78+f"\n### {r['id']}  (p.{r['page']}, 2027)\n"+"="*78+"\n")
    full.write(f"STATEMENT: {stmt}\n")
    if viol: full.write(f"\nVIOLATION: {viol}\n")
    tsv.write(f"{r['id']}\t{r['prefix']}\t{r['num']}\t{r['page']}\t{len(stmt)}\t{len(viol)}\t{r['title']}\n")
full.close(); tsv.close(); print("wrote 2027_rules_full.txt +.tsv")
PY
```

**0.2E — number harvest.** Every point value, duration, dimension, count and limit in the manual, with its rule/page. This is the raw material for Phase 2, and it catches the numbers buried in prose that no one notices until week 3.

```bash
python - <<'PY'
import re,io,sys
R="research/rule_inventories"  # relative path: run from the repository root
txt=open(f"{R}/_text/2027.txt",encoding="utf-8",errors="replace").read()
PAT=[("POINTS",  r"\b\d+(?:\.\d+)?\s*(?:points?|pts?|POINTS?)\b"),
     ("RP",      r"\b\d+\s*(?:RANKING POINTS?|RPs?)\b"),
     ("TIME",    r"\b\d+(?:\.\d+)?\s*(?:seconds?|sec\b|s\b|minutes?|min\b)\b"),
     ("LENGTH",  r"\b\d+(?:\.\d+)?\s*(?:in\.?|inch(?:es)?|ft\.?|feet|foot|mm|cm|m\b)\b"),
     ("MASS",    r"\b\d+(?:\.\d+)?\s*(?:lbs?\.?|pounds?|kg|g)\b"),
     ("COUNT",   r"\b(?:no more than|at most|up to|maximum of|minimum of|at least|exactly)\s+\w+\b"),
     ("PERCENT", r"\b\d+(?:\.\d+)?\s*%")]
lines=txt.splitlines(); page=1; out=[]
for i,l in enumerate(lines):
    if re.search(r"\b\d+\s+of\s+\d+\b",l):
        mm=re.search(r"\b(\d+)\s+of\s+\d+\b",l); page=int(mm.group(1))
    rid=re.findall(r"\b([GRITHSECA]\d{3})\b",l)
    for k,p in PAT:
        for m in re.finditer(p,l,re.I):
            out.append((k,m.group(0).strip(),page,rid[0] if rid else "",l.strip()[:150]))
seen=set(); f=open(f"{R}/2027_numbers.tsv","w",encoding="utf-8")
f.write("kind\tvalue\tpage\trule\tcontext\n")
for r in out:
    key=(r[0],r[1],r[2],r[4])
    if key in seen: continue
    seen.add(key); f.write("\t".join(str(x) for x in r)+"\n")
print("numbers:",len(seen))
PY
```

Then eyeball it in one pass: `sort -k1,1 research/rule_inventories/2027_numbers.tsv | awk -F'\t' '$1=="POINTS"'`

**0.2F — undefined ALL-CAPS terms.** FRC capitalizes defined terms. A capitalized term that appears in a rule but is *never defined* is either a drafting error or a genuine ambiguity — and either way it is a Q&A question. Terms new since 2026 are the game-specific vocabulary, and that is where the whole game lives.

```bash
python - <<'PY'
import re,collections
R="research/rule_inventories"  # relative path: run from the repository root
new=open(f"{R}/_text/2027.txt",encoding="utf-8",errors="replace").read()
old=open(f"{R}/_text/2026.txt",encoding="utf-8",errors="replace").read()
STOP={"FIRST","ROBOT","ROBOTS","FRC","THE","AND","FIELD","MATCH","ALLIANCE","AUTO","TELEOP",
      "NOT","MAY","ALL","PDF","LED","USB","CAN","PWM","AWG","NOTE","RP","VIOLATION"}
def caps(t): return collections.Counter(w for w in re.findall(r"\b[A-Z][A-Z]{2,}(?:S)?\b",t) if w not in STOP)
n,o=caps(new),caps(old)
f=open(f"{R}/2027_newterms.tsv","w",encoding="utf-8")
f.write("term\tcount_2027\tcount_2026\tstatus\tdefined_in_manual\n")
for w,c in n.most_common():
    # "defined" = appears adjacent to a definition cue somewhere in the manual
    dfn = bool(re.search(r"\b%s\b[^.\n]{0,40}\b(is|are|means|refers to|defined as)\b" % re.escape(w),new)
               or re.search(r"\b(is|are|means|called)\b[^.\n]{0,40}\b%s\b" % re.escape(w),new))
    st = "NEW-IN-2027" if o.get(w,0)==0 else ("GREW" if c>2*o[w] else "carryover")
    if st!="carryover" or not dfn:
        f.write(f"{w}\t{c}\t{o.get(w,0)}\t{st}\t{'yes' if dfn else 'NO-DEFINITION-FOUND'}\n")
print("wrote 2027_newterms.tsv")
PY
```

**Read every `NEW-IN-2027` + `NO-DEFINITION-FOUND` row out loud.** Each one is a candidate Q&A question and a candidate loophole. `[COMPUTED]` For calibration: 2026 REBUILT introduced `FUEL`, `TOWER`, `OUTPOST`, `HUB` — and the rules governing them (G408, G420, G427) were all new, and all drew Q&A traffic.

**0.2G — the violation ladder.** Every `Violation:` line in the manual, with its rule. `[COMPUTED]` The 2026 manual has **78** of them across 225 rules; 25 rules mention YELLOW CARD, 19 mention RED CARD.

```bash
python - <<'PY'
import re
R="research/rule_inventories"  # relative path: run from the repository root
t=open(f"{R}/2027_rules_full.txt",encoding="utf-8").read()
f=open(f"{R}/2027_violations.tsv","w",encoding="utf-8")
f.write("rule\tpage\tminor\tmajor\tyellow\tred\tdq\tverbal\tescalating\tviolation_text\n")
for m in re.finditer(r"### ([GRITHSECA]\d{3})\s+\(p\.(\d+), 2027\)\n=+\n(.*?)(?=\n=+\n### |\Z)",t,re.S):
    rid,pg,body=m.group(1),m.group(2),m.group(3)
    v=re.search(r"VIOLATION:(.*?)(?=\n\n|\Z)",body,re.S)
    if not v: continue
    s=" ".join(v.group(1).split())
    flag=lambda p: "1" if re.search(p,s,re.I) else ""
    f.write("\t".join([rid,pg,flag(r"MINOR FOUL|\bFOUL\b(?! )"),flag(r"MAJOR FOUL|TECH(NICAL)? FOUL"),
        flag(r"YELLOW CARD"),flag(r"RED CARD"),flag(r"DISQUALIF"),flag(r"VERBAL WARNING"),
        flag(r"subsequent|each additional|per .*occurrence|repeated"),s[:400]])+"\n")
print("wrote 2027_violations.tsv")
PY
```

### 0.3 The diff that matters most

`[COMPUTED]` Rule-ID counts by prefix, 2016–2026, from [`counts_by_prefix.tsv`](research/rule_inventories/counts_by_prefix.tsv):

| Year | G | R | I | T | E | Total |
|---|--:|--:|--:|--:|--:|--:|
| 2024 CRESCENDO | 50 | 95 | 7 | 12 | 47 | 212 |
| 2025 REEFSCAPE | 55 | 97 | 7 | 16 | 52 | 228 |
| 2026 REBUILT | 47 | 99 | 7 | 16 | 55 | 225 |
| **2027 BIOCORE** | ___ | ___ | ___ | ___ | ___ | ___ |

`[INFERENCE]` Expect **~210–240 rules**, of which **~45–55 are G-rules** and **~95–100 are R-rules**. A total materially outside that band is itself news.

Three diffs, in priority order:

1. **G4xx (gameplay) — expect near-total replacement.** These encode the game. `[COMPUTED]` 2025→2026 churn shows the game-specific G-rules re-numbered *and* rewritten: `G415→R106` (sim 0.353), `G415→G413` (0.393), `G409→G408` (0.413), `G433→G425` (0.548). **Do not track by rule ID across seasons — track semantically.** That is what `rule-taxonomy-analyze.py` is for.
2. **R4xx (bumpers) — expect near-total *retention*, and read it anyway.** `[CONFIRMED]` The bumper block drew **116 Q&A questions across 2024–2026**, the largest cluster in the manual, and R402 is *accelerating* (3 → 9 → 16). ([`QA-AMBIGUITY-HOTSPOTS.md` §2.1](reference/QA-AMBIGUITY-HOTSPOTS.md)) Bumpers are also the most common inspection failure. **Read R4xx before any CAD happens.**
3. **Everything with `min_sim < 0.6` in the 2026→2027 churn pairs.** `[COMPUTED]` Those are the rewritten rules. A rewritten rule in a historically hot block (R408, R504, R303, R205, G202 — see [`stability.tsv`](research/rule_inventories/stability.tsv)) is the highest-value text in the manual.

`[VERIFIED]` **The evergreen set is real and large.** Rules like R623 (connectors, mean similarity 0.951 across ten years), R902 (visible display, 0.946), R607 (insulate battery, 0.937), R103 (weight limit, 0.905) have survived four renumberings essentially unchanged. `[INFERENCE]` **You do not need to re-read the evergreen set.** Spend the reading budget on the diff. Full list: [`evergreen.tsv`](research/rule_inventories/evergreen.tsv), [`evergreen_5yr.tsv`](research/rule_inventories/evergreen_5yr.tsv).

### 0.4 Manual Fingerprint Card — fill this in before Phase 1

```
MANUAL FINGERPRINT — BIOCORE
  Filename / URL actually used ........ ____________________
  SHA-256 (first 12) .................. ____________________
  Page count .......................... ____
  Version stamp (footer) .............. ____________________
  Total rules ......................... ____   (G __ / R __ / I __ / T __ / E __ / other __)
  Rules with a Violation: line ........ ____   (2026 = 78)
  Rules mentioning RED CARD ........... ____   (2026 = 19)
  NEW-IN-2027 capitalized terms ....... ____   list: _______________________________
  ...of which UNDEFINED ............... ____   list: _______________________________
  Distinct point values in manual ..... ____   list: _______________________________
  MINOR FOUL value .................... ____ pts   (2024=2, 2025=2, 2026=5)
  MAJOR/TECH FOUL value ............... ____ pts   (2024=5, 2025=6, 2026=15)
  AUTO length ......... ____ s   TELEOP ____ s   ENDGAME trigger @ ____ s
  Alliance size ....... ____ (3 assumed, unconfirmed for 2027)
  Holding limit ....... ____   (VERIFIED pre-kickoff: >1)
  Scoring element name  ____________________
  Ranking points: ____ objective RPs + Win/Tie.  Names: _______________________________
  Field footprint ..... ____ x ____ ft  (carpet continuity implies 30 x 74 — VERIFIED carpet)
  Pneumatics legal? ... YES / NO   (FIRST said removal was under review — see below)
  roboRIO legal? ...... YES / NO
  A301 legal? ......... YES / NO, count limit ____
  Weight limit ........ ____ lb w/ bumpers   (2026 = 115 lb + bumpers)
```

### 0.5 Phase 0 exit criteria

- [ ] Kickoff PDF frozen with timestamp + SHA-256 in `logs/manual_hashes.txt`
- [ ] `2027.json` exists and rule count is within 10% of 225
- [ ] `2027_rules_full.txt` and `2027_rules.tsv` regenerate cleanly
- [ ] `churn_pairs_2026_2027.tsv` exists; the 30 lowest-similarity rows are printed
- [ ] `2027_numbers.tsv` exists; every distinct POINTS value is listed
- [ ] `2027_newterms.tsv` exists; every NEW-IN-2027 term is listed with defined/undefined
- [ ] `2027_violations.tsv` exists; the count of MAJOR-FOUL and RED-CARD rules is recorded
- [ ] Fingerprint Card fully populated — **no blanks**. A blank means you have not read that part of the manual.
- [ ] Field Dimension Drawings downloaded (manual dimensions are *nominal and untoleranced*; the drawings govern — `[VERIFIED]` 2026 manual §5.1)

---

## Phase 1 — Game comprehension (15–60 min)

**Fill every table. No strategy allowed in this phase.** Anything you cannot fill in is either a Q&A question or a re-read, and both outcomes are wins.

This questionnaire is deliberately the answer sheet to the 33 open questions in [`03_biocore_official_intel.md`](research/03_biocore_official_intel.md). Cross off each as you answer it.

### 1.1 Match phases

| Phase | Start trigger | Duration | Ends how | Robot control | Human control | Notes |
|---|---|---|---|---|---|---|
| Pre-match / setup | | | | n/a | | Staging rules, element pre-load allowance |
| AUTO | | ____ s | | autonomous only | | Opponent interaction rule? (2026: G403) |
| Transition | | ____ s | | | | Is there one? |
| TELEOP | | ____ s | | | | |
| ENDGAME | @ T−____ s | ____ s | | | | Trigger: clock, event, or both? |
| Post-match | | | | | | Scoring finalization, element retrieval |

**Ask explicitly:** does *anything* change value between phases? (2026 pattern: AUTO-scored elements worth more.) Does the holding limit change by phase? Do zone restrictions change at ENDGAME?

### 1.2 Scoring action ledger — the core table

One row per **distinct scoring action**. If two actions differ in points, location, or phase, they are two rows.

| # | Action (verb + object + location) | Rule / page | AUTO pts | TELEOP pts | ENDGAME pts | Who can do it (robot / HP / either) | Repeatable? | Cap per match | Descorable by opponent? | Counts toward which RP |
|---|---|---|--:|--:|--:|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| … | | | | | | | | | | |

**Completeness test:** sum the theoretical maximum of every row. If your max is not roughly 2–4× the projected winning score, you have missed a scoring action or misread a cap.

### 1.3 Zone register

| Zone name | Defined at (rule/page) | Physical bounds | Who may enter (own robots / opponents / humans) | What is legal only inside | What is illegal inside | Protected? Penalty for violation |
|---|---|---|---|---|---|---|
| | | | | | | |

**The high-value questions here:** Is there a zone where opponent contact is penalized (a *protected* zone)? Is there a zone where scoring is only legal from inside (2026: G407 "Only score while in your ALLIANCE ZONE")? Is any zone *shared* between alliances? `[SPECULATION]` Shared/contested field elements are the single most loophole-rich category in FRC design ([`03_biocore_official_intel.md`](research/03_biocore_official_intel.md) open question 15).

### 1.4 Field element register

| Element | Qty on field | Owned by (red/blue/shared) | Nominal dims (manual) | **Toleranced dims (drawings)** | Height off carpet | Robot may contact? | Robot may climb/hang on? | Does it move? | AprilTag on it? |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

> `[VERIFIED]` "dimensions included in the manual are nominal and no tolerances are implied… The 3D CAD model is the official representation of the FIELD" — 2026 manual §5.1, p. 17. **Any mechanism whose function depends on a dimension being exact must be sized from the drawings, not the manual.** And a dimension that appears on *neither* the drawings nor the Field Acceptance Checklist is not verified at any event — do not depend on it at all.

### 1.5 Scoring element — the spec sheet

`[VERIFIED]` pre-kickoff facts to check against the manual immediately ([FRC blog, Jun 8 2026](https://community.firstinspires.org/2026-pre-orders-for-2027-scoring-elements)):
- BIOCORE has **exactly one type** of scoring element
- Robots have a **holding limit > 1** during the match
- The Kickoff Kit Season Specific Box contains **more than the holding limit**
- No additional elements through FIRST Choice; only source is the Kickoff Kit or AndyMark

| Property | Value | Source (manual page / drawing) |
|---|---|---|
| Official name | | |
| Shape & dimensions | | |
| Mass | | |
| Material / compressibility | | |
| Alliance-colored variants? | | |
| Quantity on full field | | |
| Quantity pre-loaded per robot | | |
| Quantity available in AUTO vs TELEOP | | |
| Holding limit (number) | | |
| Does the limit differ by phase / zone / role? | | |
| Definition of CONTROL / POSSESSION | | |
| Penalty for exceeding | | |
| Is a damaged element still legal & scorable? | | |
| May a robot deliberately damage one? (2026: R206, G406) | | |

### 1.6 Ranking formula

| RP | Name | Condition (exact text) | Value | Achievable solo? | Achievable by an alliance that loses? | Coopertition-linked? |
|---|---|---|---|---|---|---|
| Win/Tie | | | ___ / ___ | n/a | n/a | |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

**Then write out the full ranking sort:** `Rank = f(RP/match, tiebreak 1, tiebreak 2, …)` — copy the tiebreaker chain verbatim from the manual, in order. Teams lose seeds to tiebreakers they never read.

`[SPECULATION, 78%]` Expect **2–3 objective RPs plus Win/Tie**, with at least one being a cumulative volume threshold ("Energized"-style) — FRC has used a threshold-count RP every year since 2018. ([`04_biocore_community_intel.md` P7](research/04_biocore_community_intel.md))

### 1.7 Endgame

| Question | Answer |
|---|---|
| Trigger (clock time / event) | |
| Duration | |
| Task(s) | |
| Tiered? How many tiers, what values | |
| Multi-robot interaction permitted (buddy climb / ramp)? | |
| Does it lock out any teleop scoring? | |
| Endgame points as % of projected winning score | ____ % |
| Is there an endgame RP? Threshold? | |
| Does the robot have to *stay* in position at T=0? What is the settle rule? | |

`[SPECULATION, 62%]` Community consensus expects a **climb/ascent scored in ≥2 tiers, worth ≥15% of a winning score**, overcorrecting REBUILT's undervalued climb. Three consecutive climb endgames is the base rate; the counter-argument is that platform/balance is "due" (last used 2019, 2023). Score this prediction. ([`04_biocore_community_intel.md` P6](research/04_biocore_community_intel.md))

### 1.8 Human player roles

| Role | How many | Where they stand | What they may touch | What they may do with elements | Timing restrictions | Rules governing (2026 analogues: G424, G425, G426, G427) |
|---|---|---|---|---|---|---|
| DRIVER(s) | | | | | | |
| HUMAN PLAYER(s) | | | | | | |
| DRIVE COACH | | | | | | |
| TECHNICIAN | | | | | | |

**The question everyone forgets:** what is the *rate limit* on human element delivery, and is there a storage/staging limit on the human side? (2026: G427 "The OUTPOST has a storage limit.") Human-player throughput caps are a hidden ceiling on cycle-based strategies.

### 1.9 Penalty structure

| Category | Name in BIOCORE | Point value | Escalation |
|---|---|---|---|
| Minor | | ____ | |
| Major | | ____ | |
| Yellow card | | n/a | |
| Red card | | n/a | |
| DQ | | n/a | |

`[VERIFIED]` Historical values, extracted from the manuals: **2024** FOUL 2 / TECH FOUL 5 · **2025** FOUL 2 / TECH FOUL 6 · **2026** MINOR FOUL 5 / MAJOR FOUL 15. Note the terminology change in 2026 and the 3× jump in penalty severity. If BIOCORE keeps 2026's scale, penalty arbitrage is expensive; if it reverts, it is cheap. **This single number drives all of §4.2.**

### 1.10 Comprehension self-test — answer without looking

If you cannot answer all ten from memory, you have not read the manual, you have skimmed it.

1. What is the single highest-value scoring action, and what does it require?
2. What is the highest **points-per-second** scoring action?
3. Name every action a human player can take that scores points.
4. What is the exact wording of the holding-limit rule, and what is the violation?
5. Which zones are protected, and what happens if you enter one?
6. What is the ranking sort, including all tiebreakers, in order?
7. Which RP is hardest for a mid-tier alliance to earn, and why?
8. Name three actions that draw a MAJOR FOUL.
9. What must be true at T=0 for the endgame to score?
10. Name three things the manual says are *illegal* that a naive reading of the game would suggest are fine.

---

## Phase 2 — Scoring strategy analysis

### 2.1 The cycle model

The one model that matters. Everything else is decoration.

```
CYCLE TIME (s)  =  t_acquire + t_travel_out + t_align + t_score + t_travel_back
POINTS/CYCLE    =  (points per element) x (elements carried per cycle)   [capped by holding limit]
POINTS/SECOND   =  POINTS_PER_CYCLE / CYCLE_TIME
MATCH POINTS    =  POINTS/SECOND x (usable teleop seconds)  +  AUTO points  +  ENDGAME points
                   where usable teleop seconds = TELEOP_LENGTH − t_endgame_reserved − t_defense_lost
```

Fill for **every** viable scoring action, not just the obvious one:

| Action | pts/element | elems/cycle | t_acq | t_travel | t_align | t_score | **cycle s** | **pts/s** | cycles in a match | match pts |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | | | | | | | | | | |

**The decision rule:** the highest-`pts/s` action that your robot can execute **reliably** is your primary scoring mode. The highest-`pts` action is usually *not* it. Two failure modes this exposes:

- A high-value action with a long alignment time loses to a low-value action with a 4-second cycle. Compute it; do not eyeball it.
- **Holding limit is a multiplier on `t_travel`, not on `t_score`.** `[VERIFIED]` BIOCORE's holding limit is >1. If the limit is 4 and travel is 6 s each way, carrying 4 cuts effective travel per element from 12 s to 3 s. **A holding limit >1 is the strongest argument in the game for an intake that can hold the full limit**, and the first thing to check is whether the *scoring* mechanism can dispense them faster than one per cycle.

### 2.2 Points per complexity — what the strategy is actually worth to *this* team

| Scoring capability | Match pts (from 2.1) | Mechanisms required | Est. build-weeks | Est. weight (lb) | Novel risk (1–5) | **pts per build-week** | **pts per lb** |
|---|--:|---|--:|--:|--:|--:|--:|
| Drive + push only (defense) | | drivetrain | 0 | 0 | 1 | — | — |
| Ground intake + lowest goal | | | | | | | |
| + mid tier | | | | | | | |
| + highest tier | | | | | | | |
| + endgame tier 1 | | | | | | | |
| + endgame tier 2 | | | | | | | |
| + AUTO (n-element) | | | | | | | |

**Read the `pts per build-week` column bottom-up.** The last capability added is almost always the worst deal, and it is the one teams add anyway. `[INFERENCE]` For a small team, the correct output of this table is a *deletion list*, not an addition list.

### 2.3 Auto is worth more than teams think, and less than they fear

`[COMPUTED, TBA 2023–2026]` Auto's share of match score and its rank correlation:

| Season | Median auto as % of match score | Spearman(rank, avg auto) | Spearman(rank, avg score) |
|---|--:|--:|--:|
| 2025 REEFSCAPE | 20.0% | 0.221 | 0.229 |
| 2026 REBUILT | 20.6% | 0.219 | 0.291 |

`[INFERENCE]` Auto is a **stable ~20% of the scoreboard** and its rank correlation is *nearly identical* to total-score correlation — meaning auto performance is mostly a proxy for overall robot quality, not an independent lever. The strategic implication: a reliable, simple auto that always scores beats an ambitious auto that works 60% of the time, because the variance costs you RP thresholds and the upside is capped at ~20% of the match.

### 2.4 RP vs. win — settle this with data, not vibes

The recurring kickoff argument is "play for RPs" vs "play to win matches." Here is the empirical answer.

`[COMPUTED, TBA, `research/predictive_tba/winner_seed_validation.json`]` **Which alliance seed actually wins the event:**

| Season | Events | Seed 1 wins | Seed 1 or 2 | Seeds 5–8 |
|---|--:|--:|--:|--:|
| 2023 | 179 | **65.4%** | 84.4% | 6.1% |
| 2024 | 184 | **66.3%** | 82.6% | 5.4% |
| 2025 | 198 | **82.8%** | 92.9% | 1.0% |
| 2026 | 208 | **81.7%** | 95.7% | 0.5% |

`[INFERENCE]` **Seeding is the game.** In the two most recent seasons the top-seeded alliance won **>80%** of events and seeds 5–8 won **under 1%**. The "we'll get picked and win from the 6 seed" plan has a sub-1% historical base rate. Whatever the RP formula is, **maximize RP** — that is what determines the captaincy, which determines the alliance, which determines the event.

`[COMPUTED]` **And ranking mostly determines whether you get picked at all** (2023 data, % of teams picked by within-event rank percentile):

| Rank band | Small event (<36) | Medium (36–45) | Large (46–60) | Huge (61+) |
|---|--:|--:|--:|--:|
| Top 10% | 100% | 100% | 100% | 100% |
| 25–33% | 100% | 94.9% | 87.4% | 56.6% |
| 50–66% | 84.6% | 51.4% | 33.6% | 29.2% |
| 75–90% | 54.2% | 22.3% | 8.2% | 11.4% |

`[COMPUTED]` The winning alliance's composition is lopsided: captain median qual rank **2.9th percentile**, first pick **9.4th**, second pick **63.2nd**. Second picks come from the bottom half **69%** of the time. `[INFERENCE]` The realistic small-team target is *first-pick quality* — top ~10% — not captaincy. Second-pick status is nearly rank-independent and is won on scouting reputation and one visible specialty.

**Fill in for BIOCORE:**

| Question | Answer |
|---|---|
| Max RP per match | ____ |
| RP available to a *losing* alliance | ____ |
| Is any RP achievable solo by an elite robot? | (this is the "meta lock-in" risk — see §5) |
| Is any RP achievable only with partner cooperation? | |
| Which RP is the marginal one for us — what is the exact threshold, and what is our per-match probability of hitting it? | ____ % |
| Expected RP/match for our realistic robot | ____ |
| RP/match historically needed for a top-8 seed at our event size | ____ |

### 2.5 Score projection — week 1 vs. championship

Teams design to the week-1 score and get run over in week 5. `[COMPUTED, TBA]` Mean event average match score by week:

| Season | W1 | W2 | W3 | W4 | W5 | W6 | Champs | **W1→W6** | **W1→Champs** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2023 CHARGED UP | 65.2 | 65.7 | 72.9 | 81.5 | 82.8 | 114.8 | 135.6 | 1.76× | 2.08× |
| 2024 CRESCENDO | 37.4 | 37.4 | 42.2 | 46.7 | 46.4 | 63.4 | 84.4 | 1.70× | 2.26× |
| 2025 REEFSCAPE | 72.5 | 67.3 | 77.1 | 88.3 | 96.2 | 128.3 | 182.0 | 1.77× | 2.51× |
| 2026 REBUILT | 115.4 | 119.7 | 133.7 | 159.9 | 159.4 | 192.6 | 407.8 | 1.67× | 3.53× |

Top-team averages inflate similarly (W1→Champs: 1.69× / 1.98× / 2.04× / 2.54×).

**The projection template:**

```
S_w1_avg      = (best estimate of week-1 average match score)      = ______
S_w1_top      = (best estimate of week-1 top-team average)         = ______
S_w6          = S_w1 x 1.72       [mean of 4 seasons, sd 0.05]     = ______
S_champs      = S_w1 x 2.6        [mean of 4 seasons, range 2.1-3.5] = ______
OUR TARGET    = the score we must produce to be a top-8 seed at OUR event, in OUR week = ______
```

**Design to `S_w6`, not `S_w1`.** `[INFERENCE]` A robot built to be competitive at the week-1 average is a bottom-half robot by week 5, because the field converges on the optimal strategy while your robot does not change. The correct design target is the **week-6 top-team average of the *previous* comparable game**, scaled.

**Kickoff-day estimate of `S_w1`:** take the Phase 2.1 model, assume a *median* robot executes the second-best `pts/s` action at 70% efficiency for 60% of teleop, add a 50%-reliable endgame, ×3 robots. Sanity-check against: is your number within 2× of the previous season's W1? If not, re-derive.

### 2.6 "What actually wins" — the hypothesis, stated falsifiably

Write it as one paragraph, then commit to numbers:

```
HYPOTHESIS (write in plain English, one sentence):
  "In BIOCORE, matches are won by ______________________________, because ______________________."

NUMERIC COMMITMENTS
  Winning alliance score, week 1 ........................ ______
  Share of that score from AUTO ......................... ____ %
  Share from the primary teleop action .................. ____ %
  Share from ENDGAME .................................... ____ %
  Share from opponent penalties ......................... ____ %
  Cycles the winning alliance completes .................. ______
  Number of robots on the winning alliance that must be
     capable of the primary scoring action ............... ___ of 3
  The single capability whose absence most reduces win
     probability ........................................  ______________

FALSIFIERS — I am wrong if:
  1. ______________________________________________
  2. ______________________________________________
  3. ______________________________________________

RE-TEST DATE: end of Week 1 (against real match data on TBA / Statbotics)
```

**Then score the pre-kickoff betting sheet.** [`04_biocore_community_intel.md`](research/04_biocore_community_intel.md) contains ten falsifiable predictions (P1–P10) with confidences. Mark each TRUE/FALSE against the manual. Predictions that were *wrong* tell you which parts of the analytical model were broken and therefore which downstream conclusions in this project need re-deriving — the author flags **P2 (element count <150)** as load-bearing for P4/P5/P9.

---

## Phase 3 — Design strategy

### 3.1 Archetype shortlist — derived, not brainstormed

**Do not brainstorm archetypes.** Derive them from the Phase 2 tables by this procedure:

1. Rank every scoring action by `pts/s` (§2.1).
2. Rank every capability by `pts per build-week` (§2.2).
3. An **archetype** = the minimal set of mechanisms covering a contiguous top slice of both lists.
4. Kill any archetype whose top capability requires a mechanism your team has never built *and* that sits below the median on `pts per build-week`.

| # | Archetype | Scoring actions covered | Mechanisms | Est. match pts (W1 / W6) | Build weeks | Weight | Novel-mechanism count | Alliance-selection value | Verdict |
|---|---|---|---|---|--:|--:|--:|---|---|
| A | Minimum viable scorer | | drivetrain + intake + single scoring output | | | | | | |
| B | Primary-action specialist | | | | | | | | |
| C | Full-tier scorer | | | | | | | | |
| D | Endgame specialist + light scoring | | | | | | | | |
| E | Feeder / support / cycle-assist | | | | | | | | |
| F | Dedicated defense | | drivetrain + bumper strategy only | | | | | | |

**Two archetype questions specific to BIOCORE:**

- `[VERIFIED]` **Holding limit > 1.** Does the winning archetype carry the full limit, or is the limit a red herring because the scoring mechanism is the bottleneck? Compute both; they give different intakes.
- `[SPECULATION, 72%]` **≥3 scoring locations or height tiers of differing value.** If true, the fork is *reach* vs *rate*: a tall/precise scorer that hits the high tier slowly, versus a fast scorer that floods the low tier. Resolve it with §2.1's `pts/s`, not with aesthetics. If the low tier's `pts/s` is within 20% of the high tier's, **build the low-tier robot** — it is lighter, faster to build, more reliable, and can be defended less easily.

**Archetype F (dedicated defense) is a real answer and should be evaluated honestly**, not dismissed. Evaluate it as: `(points denied to opponent per match) − (penalty points conceded)` and compare to Archetype A's match points. `[COMPUTED]` In 2026 the mean DQ rate was 2.7% of team-events and the MAJOR FOUL was worth 15 points — a defense strategy that draws two major fouls per match has to deny 30+ points to break even.

### 3.2 Constraint extraction table

Pull each row from the BIOCORE R-rules; the "2026 value" column is the prior. Detail and rule-by-rule commentary live in `reference/robot_construction_rules.md`.

| Constraint | 2026 rule | 2026 value | **BIOCORE rule** | **BIOCORE value** | Changed? | Design consequence for us |
|---|---|---|---|---|---|---|
| Frame perimeter must be fixed | R101 | fixed, non-articulated | | | | |
| Starting config — no overhang | R102 | | | | | |
| Robot weight limit | R103 | 115 lb (excl. bumpers/battery) | | | | |
| Starting config — max size | R104 | | | | | |
| Horizontal extension limit | R105 | | | | | |
| Horizontal extension — one direction at a time | R106 | one at a time | | | | **New in 2026; 12 Q&A questions in year one** |
| Vertical extension limit | R107 | | | | | |
| Extension / floor interaction | R108 | | | | | |
| Bumper zone height | R401/R410 | | | | | |
| Bumper construction spec | R402 | | | | | **Hottest rule in the manual — 28 Q&A '24–'26** |
| Bumper extension limit | R403 | | | | | |
| Bumper softness / material | R404 | | | | | |
| Bumper-to-bumper interaction | R405 | | | | | |
| Weight limit incl. bumpers | R408 | 135 lb | | | | 2026 R103 excludes BUMPERS, battery + its Anderson half, and event location tags |
| Bumpers must be removable | R410 | | | | | |
| Allowable motors (list + counts) | R501 | | | | | Is **A301** on the list? At what count? |
| Propulsion motor cap | R502 | 4 | | | | |
| Approved motor controllers | R504 | | | | | Talon / Venom / Victor SP under review for removal |
| Battery / power | R601–R625 | | | | | Does the PDH survive? |
| Control system | R615 | roboRIO | | | | **SystemCore. roboRIO explicitly illegal?** |
| Radio | R616/R617 | VH-109 | | | | SystemCore's onboard radio is FTC-competition-only |
| **Pneumatics legal at all?** | R801–R807 | legal | | | | `[VERIFIED]` FIRST said the section may be **removed entirely** |
| Individual item cost limit | R301 | | | | | |
| Major mechanism, this year only | R302 | | | | | |
| Custom vs COTS definitions | §9 / R3xx | | | | | |

> `[VERIFIED]` The pneumatics question is not speculation. From [2026 Usage Reporting Data](https://community.firstinspires.org/2026-usage-reporting-data) (Jul 29, 2026): pneumatics usage was **~3.5%**, and FIRST wrote that this "will drive a review of whether we should make changes to re-incentivize pneumatics use or **remove it entirely**." **Resolve this before any prototyping.** The answer may arrive before kickoff in the ~late-October "2027 Robot Rules Preview" blog post — historically the single most valuable pre-kickoff document.

### 3.3 Build vs. buy

| Subsystem | Build | Buy (vendor/part) | Cost delta | Weeks saved | Risk delta | Decision |
|---|---|---|--:|--:|---|---|
| Drivetrain | | COTS swerve module / KitBot chassis | | | | |
| Intake | | | | | | |
| Elevator / arm | | COTS elevator kit | | | | |
| Endgame mechanism | | | | | | |
| Electronics board | | | | | | |

**Decision rule for a small team:** buy anything that is (a) on the critical path to a working robot, (b) a solved problem with a mature COTS option, and (c) not the mechanism your competitive advantage rests on. Build exactly one thing well. `[INFERENCE]` The `R301` individual-item cost limit and total-cost rules constrain this — extract the actual 2027 numbers before committing to a swerve budget.

**2027 has a mandatory build-vs-buy shock:** SystemCore. `[VERIFIED]` It replaces the roboRIO, and WPILib 2027 removes Shuffleboard, SmartDashboard, PathWeaver, RobotBuilder, NetworkTables v3, and servo/relay/SPI/analog-gyro support, renames `edu.wpi.first`→`org.wpilib`, and requires Java 25 / C++23. **Code cannot target both 2026 and 2027 libraries.** See [`reference/team-ops/03_programming_stack.md`](reference/team-ops/03_programming_stack.md). Budget this as a *subsystem*, not as "we'll port it."

### 3.4 Reliability vs. ceiling

The expected-value framing that ends the argument:

```
E[match points]  =  P(mechanism works) x (points when it works)
E[season]        =  sum over matches, but ALSO:
                    a mechanism that fails mid-event costs the REST of the event,
                    because you cannot fix it between back-to-back matches.

BREAK-EVEN:  a 60%-reliable high scorer beats a 100%-reliable low scorer only if
             high_points > low_points / 0.6  (i.e. 1.67x the points)
```

| Option | pts when working | P(works) per match | E[pts] | P(works) at 60 matches | Fails-catastrophically? | Verdict |
|---|--:|--:|--:|--:|---|---|
| | | | | | | |

**The asymmetry teams miss:** ranking is a *sum over matches*, and a single mechanism failure in a qual match costs the win plus the RPs — often 4 RP swing. `[COMPUTED]` Given that seed 1 wins >80% of 2025–26 events, a reliability failure that costs two seeds is worth more than the ceiling that caused it. **Default to reliability. Add ceiling in week 4, not week 1.**

### 3.5 The 2027 transition tax — subtract it from every estimate

`[VERIFIED]` 2027 is the largest control-system change since the cRIO. Add to every build-week estimate:

| Item | Tax |
|---|---|
| SystemCore bring-up, first time | +1–2 weeks of software, front-loaded |
| WPILib 2027 API migration (package rename, removed classes) | +0.5–1 week |
| Loss of Shuffleboard/SmartDashboard/PathWeaver/RobotBuilder | dashboard + pathing workflow rebuilt from scratch |
| New Driver Station (multi-platform, replaces NI DS) | +driver-practice friction at the first event |
| Vendor library maturity (CTRE/REV/PathPlanner 2027 alphas) | expect bugs in weeks 1–3 |
| Possible pneumatics removal | if removed, every pneumatic prototype design is dead |

`[INFERENCE]` **The teams that win week 1 in 2027 will be the ones whose software was working in December**, not the ones with the cleverest mechanism. Recommend a pre-kickoff SystemCore drivetrain-only robot as the off-season deliverable.

---

## Phase 4 — Loophole and edge-case hunt

Full case book and historical precedents: `reference/loopholes_and_exploits.md`. This section is the *pass* — run it against the BIOCORE text, in order.

### 4.1 The pass

Work the checklist top to bottom. For every hit, record: rule ID, exact quoted sentence, what the ambiguity is, what you would do with it, and what the referee risk is.

**Where to look first, statistically.** `[CONFIRMED]` From [`QA-AMBIGUITY-HOTSPOTS.md`](reference/QA-AMBIGUITY-HOTSPOTS.md) — questions asked per rule, 2024–2026: bumpers (R401/402/404/405/408/409) **116 combined**; contact & defense (G416/G415/G418/G210/G403) **75**; extension (G413/R106/R101) **49**; and G211 "egregious or exceptional violations" **26** on its own. **Read the BIOCORE analogues of these blocks first.**

- [ ] **§1 Definitions.** Every capitalized term from `2027_newterms.tsv` marked `NO-DEFINITION-FOUND`. An undefined term in an operative rule is an ambiguity by construction.
- [ ] **CONTROL / POSSESSION.** `[SPECULATION, 82%]` BIOCORE ships an explicit numeric holding limit. Historically these produce definitional loopholes. Ask, specifically: does the limit apply in AUTO? Does it apply while touching a scoring structure? Does an element *resting on* the robot count as controlled? Is plowing/herding an exception? Is an element in a chute you are also touching yours?
- [ ] **Scoring definitions.** What exactly makes an element "scored"? Is it position, contact, sensor state, or referee judgment? Can it become un-scored? Can *you* un-score your own? Can the opponent?
- [ ] **Scoring at the buzzer.** What is the settle rule? Is an element in flight at T=0 scored? Is a robot mid-climb at T=0 credited?
- [ ] **Zone boundary geometry.** Is the boundary the tape's inner edge, outer edge, or centerline? Is "in the zone" bumpers, frame perimeter, or any part of the robot? Vertical projection or physical contact?
- [ ] **Protected zones.** Where does protection begin and end, and does it lapse (e.g. only during ENDGAME, only if the defender initiated)?
- [ ] **Extension limits.** Measured from what datum, in what configuration, at what moment? Is a momentary overshoot a violation? Is extension *through* a field element counted?
- [ ] **Bumpers.** Height window in every robot configuration including tilted/climbing. Are bumper-mounted deflectors/ramps legal, and are they weighed with the bumpers? `[COMMUNITY-CONSENSUS]` This exact loophole was flagged pre-kickoff.
- [ ] **The blue boxes.** `[VERIFIED]` Blue boxes are "part of the manual" and lose *only on conflict* with a rule. A **blue-box permission that no rule addresses survives**, because §1.6 states there are "no hidden requirements or restrictions." Harvest every permissive blue box.
- [ ] **Literalism.** `[VERIFIED]` "the text means exactly, and only, what it says… Please avoid interpreting the text based on assumptions about intent." Every rule that says *less* than it obviously intends is an opportunity. Look for missing quantifiers: "a ROBOT" vs "ROBOTS", "may not" vs "must not", absent time bounds, absent zone bounds.
- [ ] **Imperial vs metric.** `[VERIFIED]` Imperial governs; metric conversions "do not overrule." Any dimension where the metric conversion is looser than the imperial is a trap, not an opportunity — inspection uses imperial.
- [ ] **Nominal vs toleranced dimensions.** `[VERIFIED]` Manual dimensions are nominal and untoleranced; the drawings govern; only the Field Acceptance Checklist numbers are actually verified at events. Any mechanism sized to a manual dimension with <0.5 in margin is a field-variance failure waiting to happen.
- [ ] **The seams between documents.** A rule can live in the manual, the official drawings, the Awards webpages, or the Event Experience webpage — `[VERIFIED]` all four are explicitly Q&A-clarifiable — plus the Community Blog, which changes device legality and never enters the chain.
- [ ] **Human-player rate limits.** Storage caps, delivery timing, what a HP may do that a robot may not (and vice versa).
- [ ] **Multi-robot interactions.** Buddy climbs, ramps, lifting a partner, deliberate contact with a partner. Is a robot a legal surface to climb on? (2026: G414 "Don't climb on each other.")
- [ ] **AUTO-period asymmetries.** Reduced opponent-interaction rules in AUTO (2026: G403) are perennially exploitable. What is legal in AUTO that is illegal in TELEOP?
- [ ] **Field damage / element abuse.** (2026: R206, G406, G411.) Bounds on force, launch velocity, and what counts as "abuse."
- [ ] **Rules with no stated violation.** Cross-reference `2027_violations.tsv` against the full rule list. **A rule with no violation clause is unenforceable as written** — and is a Q&A question.
- [ ] **Escalating vs per-occurrence penalties.** Which violations escalate on repetition and which do not. A non-escalating minor foul is the raw material for §4.2.
- [ ] **G211-equivalent.** Find BIOCORE's "egregious or exceptional violations" rule. `[CONFIRMED]` 26 Q&A questions across three seasons because it is deliberately unbounded. **Any strategy whose viability depends on not being judged egregious carries real referee risk — mark it and price it.**

### 4.2 "Is the penalty cheaper than the points?" audit

The honest version of this question, run as a table. **This is an analysis to inform legal play and to anticipate what opponents will do — not a plan to break rules.** Anything that lands in the "cheaper" column and is not clearly legal goes to the Q&A list (§4.3), not to the drive team.

```
NET(action) = points_gained + points_denied_to_opponent − penalty_points_conceded
              − P(yellow/red card) x (cost of losing a match)
              − P(escalation to G211-equivalent) x (cost of a red card)
```

| Candidate action | Rule broken | Penalty | Penalty pts | Pts gained/denied | **NET** | Card risk | Escalates? | Verdict |
|---|---|---|--:|--:|--:|---|---|---|
| Enter protected zone to disrupt a high-value cycle | | | | | | | | |
| Exceed holding limit deliberately during a rush | | | | | | | | |
| Contact opponent during AUTO | | | | | | | | |
| Descore / disturb opponent's scored elements | | | | | | | | |
| Block a scoring aperture with the robot body | | | | | | | | |
| Extension violation for one high-value cycle | | | | | | | | |
| Pin beyond the count | | | | | | | | |

`[VERIFIED]` **Calibration from history:** MINOR/MAJOR foul values were 2/5 (2024), 2/6 (2025), **5/15 (2026)**. The 2026 tripling made most penalty arbitrage unprofitable. Record BIOCORE's numbers in §1.9 first — **the entire table's verdict column flips depending on whether BIOCORE is on the 2024 scale or the 2026 scale.**

`[VERIFIED]` **Two structural facts that kill most arbitrage plans:**
1. "No event staff, including the Head REFEREE, will review video, photos, artistic renderings, etc. of any MATCH, from any source, under any circumstances." — 2026 manual §6.7. **Any strategy whose legality depends on post-hoc proof is dead on arrival.**
2. The Head Referee has ultimate authority in the arena and rulings are final. Referee *inconsistency* is highest exactly in the contact/defense cluster, which is where arbitrage lives. Price that variance.

### 4.3 Q&A question generator — the highest-leverage 48 hours of the season

`[VERIFIED]` Why this matters: the Q&A is a resource for clarifying the manual **and** the Awards webpages, official field drawings, and District & Regional Events webpage. Answers do not supersede the manual, but **"the Q&A may result in revisions to the text in the official manuals"** — a well-built question in week 1 is the cheapest way to get an ambiguity resolved, because it can still produce a Team Update. Q&A opens ~4 days after kickoff (~Jan 13, 2027) and Team Updates run **Tuesday + Friday** through build season. `[VERIFIED — 2026 manual §§1.8, 1.9]`

**Selection rule — file a question only if all four hold:**
1. The answer changes a **design decision**, not merely a curiosity.
2. The manual text genuinely does not resolve it (you can quote the exact ambiguous sentence).
3. Your preferred reading is *defensible from the text*, not from intent.
4. You would rather have the answer than have the ambiguity — **ask this last one seriously.** A question that closes a loophole you were planning to use is a self-inflicted wound. If the ambiguity favors you and the risk is only referee inconsistency, the right move may be to prepare a one-page rule citation for the Question Box instead of filing publicly.

**Question template — use verbatim:**

```
Rule: [ID]
Manual page: [n]
Quoted text: "[exact sentence, unedited]"

Situation: [one concrete, unambiguous physical scenario. No hypotheticals stacked on hypotheticals.]

Question: [a single question with a yes/no or one-of-N answer. Never two questions in one.]

Our reading: [state the reading the text supports, and why, citing only the text.]
```

**Anti-patterns that get you a non-answer:** multi-part questions; questions that ask "is this legal?" about a whole mechanism; questions that argue intent; questions answerable by reading the rule; questions about something a Team Update already changed (always check the latest TU first — `[VERIFIED]` a large share of 2026 Q&A answers were pointers to Team Updates).

**Prioritized generator — produce candidates in this order:**

| Priority | Source | Target count |
|---|---|--:|
| 1 | Every `NO-DEFINITION-FOUND` term that appears in an operative rule (`2027_newterms.tsv`) | all |
| 2 | The CONTROL/holding-limit rule — phase, zone, and "resting on" edge cases | 3–5 |
| 3 | Scoring definition + the T=0 settle rule | 2–3 |
| 4 | Zone boundary geometry (which part of the robot, which edge of the tape) | 2–3 |
| 5 | Any BIOCORE rule whose 2026 ancestor is in the Q&A hot list *and* whose text changed (`churn_pairs_2026_2027.tsv`, sim < 0.7) | 3–6 |
| 6 | Bumper rules interacting with a *new* field element or climbing geometry | 2–4 |
| 7 | Rules with no violation clause | all |
| 8 | Extension limits measured against a new field element | 1–3 |

**Target: 8–15 filed questions in week 1.** More than that and you are asking things you could have read. Fewer and you are leaving free interpretation on the table.

**Also do this:** `[VERIFIED]` re-run `tools/frc_qa_scrape.py` daily through the season. The live Q&A is a real-time map of what every other team is confused about, and questions cluster on the rules that will be amended.

---

## Phase 5 — Pitfalls and red flags

Warn the team about these explicitly, in this order, on kickoff day.

**Strategy pitfalls**

1. **Designing to the week-1 scoreboard.** `[COMPUTED]` Scores inflate ~1.7× from W1 to W6 and ~2.6× to Championship. Your week-5 competitiveness is set by your week-6-equivalent design target.
2. **Chasing the highest-point action instead of the highest points-per-second action.** Run §2.1 before anyone says "we should do the high goal."
3. **Believing the 6-seed plan.** `[COMPUTED]` Seeds 5–8 won **0.5–1.0%** of events in 2025–26. If the plan is "get picked," the plan is to be a *first pick* — top ~10% of rank.
4. **Ignoring the RP formula until week 3.** RPs decide the seed, the seed decides the alliance, the alliance decides the event. Design for the marginal RP from day one.
5. **Adding the last capability.** `[INFERENCE]` The final capability on the §2.2 list is almost always the worst points-per-build-week deal and is the one that eats weeks 5–6 and destroys reliability.
6. **Building the game the community predicted instead of the game in the manual.** The pre-kickoff betting sheet exists to be *scored*, not followed.

**Rules pitfalls**

7. **Reading the manual once, on kickoff day.** `[VERIFIED]` In 2023 only 3 pages, and in 2025 only 5 pages, survived the season unamended. And in 2026 the per-page version marker was removed, so **the PDF no longer tells you what changed.** Diff every republished version yourself.
8. **Missing Team Updates.** Tuesday **and** Friday until the Tuesday before Week 1; Tuesdays after. They *become* the manual.
9. **Not knowing the Community Blog is a rule channel.** `[VERIFIED]` Legal-device additions and removals, event rule changes, and control-system mandates are announced there and **never appear in a Team Update.**
10. **Trusting manual dimensions.** Nominal, untoleranced. The drawings govern; the acceptance checklist is what's actually verified.
11. **Arguing metric at inspection.** Imperial governs, explicitly.
12. **Quoting a blue box as a rule.** It is part of the manual but loses on conflict.
13. **Planning any strategy that requires video review.** It does not exist, under any circumstances.
14. **Assuming a rule ID means the same thing as last year.** FRC renumbered in 2017, 2019, 2022, 2024, and moved rules again in 2025–26 (`G415→R106`, sim 0.35). Track semantically.

**2027-specific red flags**

15. **SystemCore.** `[VERIFIED]` Biggest control-system change since the cRIO; roboRIO not supported by WPILib 2027; code cannot target both. If your software team's first SystemCore boot is in January, you will lose week 1 to it.
16. **Pneumatics may not exist.** `[VERIFIED]` FIRST publicly floated removing the section entirely. Do not prototype a pneumatic mechanism until the R-rules are read.
17. **Vendor library maturity.** 2027 alphas across CTRE/REV/PathPlanner/AdvantageKit. Expect breakage weeks 1–3 and do not schedule a hard software milestone in week 2.
18. **Legacy motor controllers.** Talon, Venom, Victor SP were flagged for possible removal. If they are in your parts bin, verify legality before wiring.
19. **New officiating leadership.** `[VERIFIED]` Two new Global Head Referees and two new Senior Head Referees for 2027. `[SPECULATION]` Expect interpretation drift in the first weeks relative to 2026 precedent — do not treat 2026 referee behavior as a guide.
20. **The FTC firewall.** "Pollen", StarterBots, and Skill Builders are **FTC BIOBUZZ**. `[VERIFIED]` If any BIOCORE analysis mentions them as FRC concepts, that analysis is contaminated — stop and re-check its premises.

**Team pitfalls**

21. **Strategy by loudest voice.** The Phase 2 tables exist so the argument is about numbers.
22. **Skipping the reliability conversation.** Break-even for a 60%-reliable mechanism is 1.67× the points. Say the number out loud.
23. **No practice time budgeted.** Driver skill is a scoring multiplier that costs zero build-weeks and is the first thing cut.
24. **AI-assisted award submissions without attribution.** `[VERIFIED]` FIRST permits AI explicitly and judges may not penalize it — **but attribution is required.** "Essay created by Team XXXX and [tool]." Cost of compliance ≈ zero; cost of non-compliance is an integrity finding. ([`reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md`](reference/ai-integration/00_FIRST_AI_POLICY_VERIFIED.md))
25. **Referring to the "Dean's List."** `[CONFIRMED]` It no longer exists; it is the **FIRST Leadership Award**. Any document saying otherwise is stale. ([`reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md`](reference/awards/00_AWARD_LIST_EMPIRICAL_2026.md))

---

## Phase 6 — Deliverables

Four artifacts. **One page each.** If it does not fit on a page, it will not be read, and an unread strategy document has no effect on the robot.

### 6.1 One-page strategy brief (for the whole team, day 1)

```
BIOCORE — WHAT WINS
  The game in three sentences: ______________________________________________
  Winning score, our week: ____   Our target score: ____
  What wins: ____________________________________________________________
  Our archetype: ________________________________________________________
  Our three must-haves:  1. __________  2. __________  3. __________
  Our explicit non-goals (things we are choosing NOT to do): _______________
  The RP we are optimizing for: __________  our per-match probability: ____%
  How we get picked / pick: _____________________________________________
  Kill criteria — we abandon this plan if: _______________________________
```

### 6.2 Constraint sheet (for the build team, taped to the wall)

The filled §3.2 table, reduced to hard numbers only: weight limit, starting envelope, extension limits, bumper spec with a dimensioned sketch, motor list and counts, legal control system and controllers, cost limits. **Every number cites its rule ID.** `[INFERENCE]` This one page prevents the two most expensive failures in FRC: an inspection failure at the first event, and a mechanism redesigned in week 5 because it violated an extension rule nobody read.

### 6.3 Scouting spec (for the strategy team, before week 1)

Derived directly from §2.1 and §2.6 — **scout the variables the model needs, nothing else.**

| Field to collect | Why (which model input it feeds) | Type |
|---|---|---|
| Cycles completed | `pts/s` validation | count |
| Primary scoring action + tier | archetype identification | enum |
| Cycle time (sampled) | §2.1 | seconds |
| Endgame achieved + tier | §2.5 share-of-score | enum |
| AUTO elements scored | §2.3 | count |
| Fouls drawn / conceded | §4.2 | count |
| Mechanism failure observed | §3.4 reliability | bool + note |
| Defense played against them / by them | archetype F evaluation | enum |

Plus the pick-list rule: `[COMPUTED]` winning-alliance first picks sit at the **9.4th** rank percentile, second picks at the **63rd** and come from the bottom half **69%** of the time — so scout the bottom half for *one visible specialty*, not for general competence.

### 6.4 Q&A submission list (filed in week 1)

The §4.3 output: 8–15 questions in the template format, ranked, with the design decision each one unblocks named explicitly. Track answers; **an answer that contradicts your design assumption is a week-1 redesign, not a week-5 one.**

### 6.5 Living artifacts (maintained all season)

- `logs/manual_hashes.txt` — every manual version you have seen
- A Team Update log: date, TU number, rules touched, whether it affects our design
- The scored betting sheet (§2.6) with the re-test after Week 1

---

## Ready-to-paste prompts

Each block is written to produce mentor-grade analysis. They assume the session was started with the Step 2 prompt above, so the tag discipline and citation requirement are already in force.

### P1 — Phase 0 verification (after the scripts run)

```text
Phase 0 artifacts are generated. Do not summarize the game.

1. Print the Manual Fingerprint Card from KICKOFF_PLAYBOOK.md §0.4, fully filled, with the rule ID
   and page for every value. Mark any value you could not find as UNRESOLVED and say why.
2. Print the 30 rules with the lowest 2026->2027 semantic similarity, with both texts side by side,
   sorted ascending. For each, state in one line what materially changed.
3. Print every NEW-IN-2027 capitalized term, whether the manual defines it, and the rule IDs it
   appears in. Rank by (appears in an operative rule) x (undefined).
4. Print every rule that has no Violation: clause.
5. Print the distinct point values in the manual, each with the action it attaches to.

Then answer one question: which single page of this manual contains the most information I do not
already have from the 2026 baseline? Justify it from the diff, not from impression.
```

### P2 — Phase 1 comprehension interrogation

```text
Fill in every table in KICKOFF_PLAYBOOK.md Phase 1 (sections 1.1 through 1.9) from the BIOCORE
manual. Rules for this task:

- Every cell cites a rule ID and page. A cell you cannot source is written UNSOURCED, not guessed.
- Where the manual's wording is ambiguous, put the exact quoted sentence in the cell and append
  [AMBIGUOUS]. Do not resolve it.
- For the scoring action ledger (1.2), be exhaustive. Include actions worth 0 points that gate other
  actions, and include anything a human player can do. Then sum the theoretical maximum and tell me
  whether it is 2-4x a plausible winning score; if not, say what you have probably missed.
- Cross off, by number, each of the 33 open questions in research/03_biocore_official_intel.md that
  the manual answers, and list the ones it does not.

Finish by giving me the 10-question self-test from section 1.10 with your own answers, and flag any
question you could not answer confidently — that is where my reading is thin too.
```

### P3 — Phase 2 scoring model

```text
Build the scoring model from KICKOFF_PLAYBOOK.md Phase 2.

1. Section 2.1 cycle table: one row per scoring action. State every time estimate as a range with the
   assumption behind it (e.g. "t_align 1.5-4s, assumes vision-assisted alignment on a 3in aperture").
   Do not produce a single-point estimate without a range.
2. Section 2.2 points-per-complexity table. Estimate build-weeks against a team that has previously
   built: [MENTOR: fill in - e.g. swerve, single-stage elevator, ground intake, no shooter].
3. Section 2.3: compute what share of a projected winning score comes from AUTO in BIOCORE and
   compare to the 20% historical median.
4. Section 2.4: given the actual BIOCORE RP formula, tell me the RP-maximizing strategy and whether
   it differs from the score-maximizing strategy. If it differs, quantify the divergence in RP/match.
5. Section 2.5: project week-1 average, week-6 average, and championship average scores using the
   multipliers in the playbook. Show the arithmetic.
6. Section 2.6: state the "what actually wins" hypothesis with all numeric commitments filled in and
   three falsifiers.
7. Score the P1-P10 betting sheet in research/04_biocore_community_intel.md TRUE/FALSE against the
   manual. For every FALSE, say which downstream conclusions in this project are now invalid.

Where you are uncertain, give me the uncertainty as a range and tell me which single observation
would collapse it.
```

### P4 — Phase 3 archetype derivation

```text
Derive the archetype shortlist per KICKOFF_PLAYBOOK.md 3.1. Derive it from the Phase 2 tables using
the stated procedure — do not brainstorm, and do not include an archetype you cannot trace to a row
in the points-per-second or points-per-build-week ranking.

For each archetype give: mechanisms, projected match points at week 1 and week 6, build-weeks,
weight, novel-mechanism count, and its value at alliance selection (would a top seed pick this?).

Then do three things a typical student would not:
1. Argue the strongest case FOR the archetype you ranked last, and tell me what would have to be true
   for it to be correct.
2. Identify the archetype that is most likely to be OVER-built by the field this season, and
   therefore the one where the marginal robot is worth least at alliance selection.
3. Evaluate dedicated defense honestly: points denied minus penalty points conceded, using the actual
   BIOCORE foul values, versus the minimum-viable-scorer's match points.

Then fill the constraint extraction table in 3.2 completely from the BIOCORE R-rules, flagging every
row that CHANGED from 2026 and stating the design consequence of each change.
```

### P5 — Phase 4 loophole pass

```text
Run the full Phase 4.1 checklist against the BIOCORE manual. Work it in order and do not skip items
that seem unlikely — the point of the checklist is to defeat my intuition about where to look.

For each finding, give exactly:
  RULE: [id, page]
  TEXT: "[exact quoted sentence]"
  AMBIGUITY: [what two or more readings the text supports]
  EXPLOIT: [what a team could do with it]
  RISK: [referee variance; does it touch the egregious-violations rule?]
  CONFIDENCE: [% that a referee would allow it]

Prioritize by (impact on match outcome) x (confidence it survives a referee), and give me the top 10
first. Include findings that are DEFENSIVE — things an opponent could do to us that we should be
prepared for — and label them DEFENSIVE.

Start with the blocks that are statistically hottest per reference/QA-AMBIGUITY-HOTSPOTS.md: the
bumper rules, the contact/defense cluster, and the extension limits. Then do the game-specific
G-rules, which are all new and therefore all untested.
```

### P6 — Penalty arbitrage audit

```text
Run KICKOFF_PLAYBOOK.md 4.2. First state BIOCORE's actual minor and major foul point values and the
card ladder, with rule citations. Then fill the table.

Be rigorous and be honest in both directions:
- Do not tell me a penalty is "not in the spirit of FIRST" and stop. Compute the number, then tell me
  the number AND the ethical read, separately.
- Do not tell me an action is profitable without accounting for the card risk and the escalation
  path, including the egregious-violations rule.
- Flag anything where the arbitrage is profitable but the legality is genuinely ambiguous — that goes
  to the Q&A list, not to the drive team.
- Tell me which of these OPPONENTS are most likely to do to US, and what our counter is.

End with a one-line verdict: on the 2024 foul scale, the 2025 scale, or the 2026 scale, is BIOCORE a
game where fouling is a viable strategy? Justify from the numbers.
```

### P7 — Q&A question generation

```text
Generate the week-1 Q&A submission list per KICKOFF_PLAYBOOK.md 4.3.

Use the prioritized generator order. Produce 15 candidates in the exact template format, then rank
them and recommend which 8-12 to actually file.

For each candidate, add two lines the template does not have:
  UNBLOCKS: [the specific design decision that this answer changes]
  RISK OF ASKING: [does a bad answer close something that currently favors us? if yes, say so
                   plainly and recommend NOT filing, with the alternative of preparing a rule
                   citation for the Question Box instead]

Reject any candidate that is answerable by reading the rule, that asks two things at once, that
argues intent, or that asks "is our mechanism legal." Show me the rejected ones and why — I want to
see the filter working.

Then check the most recent Team Update and tell me if any candidate is already resolved.
```

### P8 — Red-team the whole plan

```text
You have produced a strategy. Now attack it.

Assume everything in the analysis so far is wrong in at least one important way. Find it.

1. What is the single assumption in this plan that, if false, invalidates the most downstream work?
   How would we detect that it is false, and by what date?
2. Which number in the Phase 2 model am I most likely to have estimated optimistically? Re-run the
   conclusion with a pessimistic value and tell me if the archetype choice changes.
3. What is the strongest argument that a completely different archetype wins this game? Make it
   properly, as if you believed it.
4. What does the manual permit that we have not considered at all? Look specifically for scoring
   actions with no obvious mechanism, permissions in blue boxes, and things the human player may do.
5. Name the three most likely ways this plan fails at the first event, ranked, with the mitigation
   for each and the week it must be done by.
6. What would a top-10-in-the-world team do differently, and which parts of that are actually
   available to a team of our size?

Be blunt. I would rather find this now than in week 5.
```

### P9 — Produce the deliverables

```text
Produce the four Phase 6 deliverables as separate markdown files in the project root:

  BRIEF_strategy.md      — one page, section 6.1 template, written for 15-year-olds who have not
                           read the manual. Plain language, no jargon, no hedging.
  SHEET_constraints.md   — one page, hard numbers only, every number citing its rule ID. This gets
                           printed and taped to the wall.
  SPEC_scouting.md       — one page, the fields to collect and why, plus the pick-list rule.
  LIST_qa.md             — the ranked Q&A submissions in template format, ready to paste into
                           frc-qa.firstinspires.org.

Constraints: one page means one page. Cut analysis, keep conclusions. Every claim that a student
could challenge carries its rule citation inline. No file may contain the words "it depends" without
immediately stating what it depends on and what the answer is in each case.
```

### P10 — Weekly re-run (every Tuesday and Friday of build season)

```text
A new Team Update / manual version is out.

1. Diff the new manual PDF against the last archived version. List every changed rule with old text,
   new text, and a one-line materiality judgment.
2. For each change, state whether it affects: our archetype, our constraint sheet, our Q&A list, or
   our scouting spec. Name the specific line of the specific deliverable that must change.
3. Check the FRC Community Blog since the last run — it changes device legality and never appears in
   a Team Update.
4. Re-run tools/frc_qa_scrape.py and tell me which rules the field is asking about most this week,
   and whether any cluster suggests an upcoming manual revision.
5. Update logs/manual_hashes.txt.

If nothing material changed, say "no material change" in one line. Do not pad.
```

---

## Appendix A — Kickoff-day fetch list

Full predicted-URL list with fallbacks: [`research/02_supplemental_docs_index.md` §12](research/02_supplemental_docs_index.md). `[SPECULATION]` All extrapolated from the 2026 pattern; **all 404 as of 2026-08-21**, and `[VERIFIED]` naming instability is the norm — try the 2026-style name first, then the 2025-style.

Priority order on kickoff day: **manual** → **field dimension drawings** → inspection checklist → KoP checklists → field manual → AprilTag guide → team-element drawings.

Two CDN traps `[VERIFIED]`: a missing blob returns a **215-byte XML body with HTTP 404** (so a size check alone is not a validity test), and firstinspires.org returns an **83 KB HTML 404 page** with a 404 status. Always check the status code and the `%PDF` magic bytes. Re-probe any `000` before recording it as absent.

**Watch for the `frc2027` container going live** — `firstfrc.blob.core.windows.net/frc2027/` 404s today. The moment it returns 200, assets are staging.

## Appendix B — Season calendar

| Date | Event | Status |
|---|---|---|
| 2026-09-24 12:00 ET | FRC event preferencing Round 1 opens | `[VERIFIED]` |
| ~2026-10-03 | 2027 Season Award Updates (blog) | `[INFERENCE]` from 2026 precedent |
| **~2026-10-24** | **"2027 Robot Rules Preview" (blog)** — highest-value pre-kickoff document; expect it to be unusually large in a control-system transition year | `[INFERENCE]` |
| 2026-11-12 | Pre-Kickoff Virtual Kit Release | `[VERIFIED]` |
| 2026-11-17 12:00 ET | Preferencing closes / season registration due | `[VERIFIED]` |
| ~2026-12-01 | 2027 KitBot shopping list | `[INFERENCE]` |
| ~2026-12-10 | 2027 Season Event Rule Updates | `[INFERENCE]` |
| **2027-01-09 12:00 ET** | **BIOCORE KICKOFF + GAME REVEAL** | `[VERIFIED]` |
| 2027-01-11 | AndyMark scoring elements begin shipping | `[VERIFIED]` |
| 2027-01-12 | First Team Update (Tue) | `[VERIFIED]` cadence |
| ~2027-01-13 | **Q&A opens** — file the Phase 4 list this week | `[INFERENCE]` from pattern |
| ~2027-02 mid | Award submission deadline (2026 analogue: Feb 12, 3:00 p.m. ET) | `[INFERENCE]` — re-verify |
| 2027-04-28 → 05-01 | FIRST Championship, Houston | `[VERIFIED]` |

---

*Companion to [`research/00_PREMISE_CORRECTION.md`](research/00_PREMISE_CORRECTION.md) — read that first, once, and never let FTC BIOBUZZ concepts into an FRC BIOCORE analysis.*
