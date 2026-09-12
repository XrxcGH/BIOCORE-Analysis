#!/usr/bin/env bash
# ingest-manual.sh -- Kickoff-day manual ingest + diff harness (FRC BIOCORE, 2027 game)
#
# Usage:   bash tools/ingest-manual.sh <path-to-manual.pdf> [label]
# Example: bash tools/ingest-manual.sh ~/Downloads/2027GameManual.pdf V1
#          bash tools/ingest-manual.sh manuals/2026-27_BIOCORE/2027GameManual.pdf TU03
#
# Env overrides:
#   BASELINE=<pdf>   manual to diff against  (default: 2026 REBUILT Game Manual)
#   PYTHON=<exe>     python interpreter      (default: python)
#   KEEP_LAYOUT=0    skip the pdftotext passes
#   INGEST_OUT=<dir> where the manual copy and ingest_<label>_<stamp>/ go
#                    (default: manuals/2026-27_BIOCORE; tools/rebuild-corpus.sh points it
#                    at a temporary directory so a rebuild never touches that slot)
#
# FIRST's archived manuals are not in the public repository. From the repository root,
# bash tools/rebuild-corpus.sh --fetch downloads them into manuals/archive/frc/.
#
# WHY THE BASELINE IS 2026 REBUILT: BIOCORE V1 has no predecessor version of itself, so
# there is nothing to diff a "what changed since last release" against. What CAN be
# diffed is the evergreen spine -- FRC republishes the same numbered evergreen rules
# (G1xx personal safety, G2xx conduct, R1xx-R9xx construction, I1xx, T1xx, E1xx) season
# after season, with only game nouns swapped. Diffing BIOCORE against REBUILT therefore
# answers the question that actually matters on kickoff day: which evergreen rules did
# FIRST quietly edit, which did they delete, and which rule numbers are brand new?
# Point BASELINE at the previous BIOCORE release once V2/TU01 exists.
#
# HOW TEXT IS EXTRACTED, AND WHY:
#   * tools/frc_spans.py (pymupdf) is AUTHORITATIVE. It reads font, colour and x-position,
#     so it (a) attaches each rule body to the right rule, (b) recovers FIRST's
#     evergreen-vs-game-specific encoding, which lives in the headline COLOUR (manual
#     s1.6: green+asterisk = evergreen, blue = game-specific) and in no word anywhere,
#     and (c) reads the two-column glossary as a table instead of interleaving it.
#   * pdftotext -layout is kept for TABLES ONLY (scoring tables, ARENA dimension tables).
#     Never parse rules out of it: -layout emits a rule's wrapped text under the PREVIOUS
#     rule id.
#   * pdftotext raw is kept because its word order is the reflowed reading order, which
#     is the better input for phrase greps that must not be broken by column geometry.
#
# Requires: python3 + pymupdf (verified Python 3.14 / PyMuPDF 1.28.2).
#           pdftotext (poppler) optional; pdfinfo NOT required (page count comes from pymupdf).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "${1:-}" in -h|--help) sed -n '2,40p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
PDF_IN="${1:?usage: ingest-manual.sh <manual.pdf> [label]}"
LABEL="${2:-V1}"
PY="${PYTHON:-python}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${INGEST_OUT:-$ROOT/manuals/2026-27_BIOCORE}"
WORK="$OUT/ingest_${LABEL}_${STAMP}"
SPANS="$WORK/spans"
BASELINE="${BASELINE:-$ROOT/manuals/archive/frc/2026_REBUILT_GameManual.pdf}"
BASE_SPANS="$ROOT/manuals/archive/frc/_spans/$(basename "${BASELINE%.pdf}")"
STOPLIST="$ROOT/tools/caps_stoplist_frc.txt"
LOG="$ROOT/logs/ingest_${LABEL}_${STAMP}.log"

banner() { printf '\n== %s ==\n' "$*"; }
die() { echo "!! $*" >&2; exit 1; }

# --------------------------------------------------------------------------- preflight
[ -f "$PDF_IN" ]   || die "no such file: $PDF_IN  (archived manuals: bash tools/rebuild-corpus.sh --fetch)"
[ -f "$BASELINE" ] || die "baseline missing: $BASELINE  (set BASELINE=<pdf>, or download it with: bash tools/rebuild-corpus.sh --fetch)"
command -v "$PY" >/dev/null 2>&1 || die "python not on PATH (set PYTHON=...)"
"$PY" -c "import pymupdf" >/dev/null 2>&1 || die "pymupdf missing: $PY -m pip install pymupdf"
head -c4 "$PDF_IN" | grep -q '%PDF' || die "not a PDF: $PDF_IN"

mkdir -p "$WORK" "$SPANS" "$ROOT/logs" "$OUT/sections"
# --- BIOCORE slot guard (rehearsal finding 2.3) ------------------------------------
# manuals/2026-27_BIOCORE/ is the ONE directory this project treats as canonical, and
# CLAUDE.md watches it for *BIOCORE*.pdf as an autorun TRIGGER. Copying a non-BIOCORE
# manual in under a BIOCORE name poisons that slot and creates a self-triggering file.
# A manual counts as BIOCORE if its filename says so, or its first pages do.
IS_BIOCORE=0
case "$(basename "$PDF_IN" | tr '[:upper:]' '[:lower:]')" in *biocore*) IS_BIOCORE=1 ;; esac
if [ "$IS_BIOCORE" = "0" ]; then
  if "$PY" -c "import pymupdf,sys; d=pymupdf.open(sys.argv[1]); t=''.join(d[i].get_text() for i in range(min(5,d.page_count))); sys.exit(0 if 'BIOCORE' in t.upper() else 1)" "$PDF_IN" 2>/dev/null; then
    IS_BIOCORE=1
  fi
fi
if [ "$IS_BIOCORE" = "1" ]; then
  DEST="$OUT/BIOCORE_GameManual_${LABEL}.pdf"
else
  # Not BIOCORE (a rehearsal against REBUILT/REEFSCAPE, or a wrong path). Keep the source
  # name so the file can never be mistaken for the real manual or re-trigger the autorun.
  DEST="$OUT/NOT-BIOCORE_$(basename "$PDF_IN")"
  echo "!! WARNING: '$(basename "$PDF_IN")' does not look like a BIOCORE manual." >&2
  echo "   Copying as $(basename "$DEST") instead of BIOCORE_GameManual_${LABEL}.pdf." >&2
  echo "   The BIOCORE_GameManual_*.pdf slot is reserved for the real 2027 manual." >&2
fi
cp -f "$PDF_IN" "$DEST"
PDF="$DEST"

echo "BIOCORE ingest  label=$LABEL  stamp=$STAMP"
echo "  manual   : $PDF"
echo "  baseline : $BASELINE"
echo "  workdir  : $WORK"

# --------------------------------------------------------------- 1. text extraction
banner "1. Extract text (pymupdf authoritative; pdftotext for tables)"
"$PY" "$ROOT/tools/frc_spans.py" "$PDF" --outdir "$SPANS"
if [ "${KEEP_LAYOUT:-1}" = "1" ] && command -v pdftotext >/dev/null 2>&1; then
  pdftotext -enc UTF-8 -layout "$PDF" "$WORK/full_layout.txt" 2>/dev/null \
    && echo "   full_layout.txt  (TABLES ONLY -- never parse rules from this)"
  pdftotext -enc UTF-8          "$PDF" "$WORK/full_raw.txt"    2>/dev/null \
    && echo "   full_raw.txt     (reflowed reading order, for phrase greps)"
else
  echo "   (pdftotext skipped)"
fi
grep -v '^<<<PAGE ' "$SPANS/lines.txt" > "$WORK/full_lines.txt"
echo "   full_lines.txt   $(wc -l < "$WORK/full_lines.txt") lines  <- authoritative body text"

# ------------------------------------------------------------- 2. baseline extraction
banner "2. Baseline extraction (cached)"
if [ -f "$BASE_SPANS/rules.json" ] && [ "$BASE_SPANS/rules.json" -nt "$BASELINE" ]; then
  echo "   cache hit: $BASE_SPANS"
else
  mkdir -p "$BASE_SPANS"
  "$PY" "$ROOT/tools/frc_spans.py" "$BASELINE" --outdir "$BASE_SPANS"
fi

# ------------------------------------------------ 3. rule inventory + diff + glossary
banner "3. Rule inventory, baseline diff, glossary diff, undefined ALL-CAPS"
"$PY" "$ROOT/tools/frc_diff.py" --new "$SPANS" --base "$BASE_SPANS" \
      --outdir "$WORK" --stoplist "$STOPLIST"
cp -f "$SPANS/rule_ids.txt" "$WORK/rule_ids.txt"

echo "   --- rule ids by prefix (G game, R robot, I inspection, T tournament, C champs, E event, Q question box) ---"
cut -c1 "$WORK/rule_ids.txt" | sort | uniq -c | awk '{printf "   %s=%s  ", $2, $1} END {print ""}'
echo "   --- ADDED rule ids (did not exist in the baseline) ---"
if [ -s "$WORK/rules_ADDED.txt" ]; then
  cut -f1 "$WORK/rules_ADDED.txt" | tr '\n' ' ' | fold -w 100 -s | sed 's/^/   /'
else
  echo "   (none)"
fi
echo "   --- REMOVED rule ids (existed in the baseline, gone now) ---"
if [ -s "$WORK/rules_REMOVED.txt" ]; then
  cut -f1 "$WORK/rules_REMOVED.txt" | tr '\n' ' ' | fold -w 100 -s | sed 's/^/   /'
else
  echo "   (none)"
fi
echo "   --- GAME-SPECIFIC rules (blue headline) = THIS IS THE NEW GAME, read every one ---"
tail -n +2 "$WORK/rules_GAMESPECIFIC.tsv" | cut -f1,4 | sed 's/^/   /' | head -60

# ----------------------------------------------------------------- 4. harvests
banner "4. Scoring / timing / dimension / penalty harvest"
L="$WORK/full_lines.txt"
grep -inE '[0-9]+[[:space:]]*(point|pt)s?\b|Ranking Point|BONUS RP|MATCH point' "$L" \
    > "$WORK/scoring_mentions.txt" || true
grep -inE '[0-9]+(\.[0-9]+)?[[:space:]]*(second|sec|minute|min)s?\b|countdown|expire' "$L" \
    > "$WORK/timing_mentions.txt" || true
grep -inE '[0-9]+(\.[0-9]+)?[[:space:]]*(in|inch|inches|ft|feet|cm|mm|m|lbs?|pounds?|kg|oz|deg|degrees)\b|\bdiameter\b|\bheight\b|\bwidth\b|\bperimeter\b' "$L" \
    > "$WORK/dimension_mentions.txt" || true
grep -inE 'MINOR FOUL|MAJOR FOUL|TECH FOUL|\bFOUL\b|YELLOW CARD|RED CARD|DISABLED|DISQUALIF|VERBAL WARNING' "$L" \
    > "$WORK/penalty_mentions.txt" || true
# every enforcement clause, rule-attributed, from the span parser (not a blind grep)
cp -f "$SPANS/violations.tsv" "$WORK/violations.tsv"
grep -inE 'Violation[s]?[[:space:]]*:' "$L" > "$WORK/violation_lines_raw.txt" || true
# when is a thing scored? live vs at-the-buzzer is the highest-leverage distinction there is
grep -inE 'at the (end|conclusion) of|scored (at|when|if)|is awarded|comes to rest|fully supported|remain(s|ing)? (in|on|at)|no longer|counted (once|again)|credited' "$L" \
    > "$WORK/SCORED_WHEN.txt" || true
printf '   scoring=%s  timing=%s  dimension=%s  penalty=%s\n' \
  "$(wc -l < "$WORK/scoring_mentions.txt")" "$(wc -l < "$WORK/timing_mentions.txt")" \
  "$(wc -l < "$WORK/dimension_mentions.txt")" "$(wc -l < "$WORK/penalty_mentions.txt")"
printf '   Violation: clauses=%s (rule-attributed)   raw grep hits=%s   scored-when candidates=%s\n' \
  "$(($(wc -l < "$WORK/violations.tsv") - 1))" "$(wc -l < "$WORK/violation_lines_raw.txt")" \
  "$(wc -l < "$WORK/SCORED_WHEN.txt")"
echo "   --- penalty vocabulary census ---"
for term in "MINOR FOUL" "MAJOR FOUL" "TECH FOUL" "YELLOW CARD" "RED CARD" "VERBAL WARNING" "DISABLED" "DISQUALIFIED"; do
  printf '   %-16s %s\n' "$term" "$(grep -oiE "$term" "$L" | wc -l)"
done

# ----------------------------------------------------------------- 5. glossary report
banner "5. Glossary + undefined ALL-CAPS terms"
cp -f "$SPANS/glossary.tsv" "$WORK/glossary.tsv"
cp -f "$SPANS/glossary.txt" "$WORK/glossary_terms.txt"
echo "   defined terms: $(wc -l < "$WORK/glossary_terms.txt")   new vs baseline: $(wc -l < "$WORK/glossary_ADDED.txt")"
echo "   --- NEW defined terms (these nouns ARE the game) ---"
cut -f1 "$WORK/glossary_ADDED.txt" | tr '\n' ' ' | fold -w 100 -s | sed 's/^/   /'
echo "   --- ALL-CAPS used in the body but NOT defined in the glossary (loophole signal) ---"
echo "       s1.6 promises ALL CAPS == defined term. Anything here is a typo, an acronym,"
echo "       or a load-bearing undefined term. The third kind is where arguments get won."
tail -n +2 "$WORK/UNDEFINED_CAPS.tsv" | head -40 | awk -F'\t' '{printf "   %-22s x%-4s p%s\n", $1, $2, $3}'
echo "   --- undefined ALL-CAPS phrases ---"
tail -n +2 "$WORK/UNDEFINED_CAPS_PHRASES.tsv" | head -20 | awk -F'\t' '{printf "   %-42s x%-4s p%s\n", $1, $2, $3}'

# ----------------------------------------------------------------- 6. section map
banner "6. Section map"
cp -f "$SPANS/sections.tsv" "$WORK/SECTION_MAP.tsv"
echo "   $(($(wc -l < "$WORK/SECTION_MAP.tsv") - 1)) headings -> SECTION_MAP.tsv"
awk -F'\t' 'NR>1 && $1==1 {printf "   p%-4s %s\n", $2, $3}' "$WORK/SECTION_MAP.tsv"

# ----------------------------------------------------------------- 7. tripwires
banner "7. Loophole tripwires"
{
  echo "### Unresolved FIRST editing placeholders (each is a free day-one Q&A)"
  grep -nE '\b[QGRITHSEC]XXX\b|\bTBD\b|\[TBD\]|XXX' "$L" || echo "(none)"
  echo
  echo "### Hedge / vagueness words (ambiguity = loophole surface)"
  grep -inE '\b(generally|typically|usually|intended|attempt|reasonabl|egregious|excessive|repeated|momentar|inadvertent|deliberate|strateg|sole purpose|at the discretion|in the opinion|judgment|likely|approximately)\w*' "$L" || true
  echo
  echo "### Counting words (per-MATCH vs per-instance ambiguity)"
  grep -inE '\b(per MATCH|each MATCH|at a time|simultaneous|at any (given )?time|more than|no more than|at most|up to|maximum of|limit of|only one|a single)\b' "$L" || true
  echo
  echo "### Timers / thresholds"
  grep -inE '\b(within|after|before|for more than|continuous|cumulative|during)\b.*[0-9]+[[:space:]]*(second|minute)' "$L" || true
  echo
  echo "### Exceptions and carve-outs"
  grep -inE '\b(unless|except|other than|does not apply|is exempt|notwithstanding|provided that|is not considered|shall not count)\b' "$L" || true
  echo
  echo "### Referee-discretion hooks (unappealable calls -- design around them, not into them)"
  grep -inE 'Head REFEREE|REFEREE (may|will|determines|judgment)|at their discretion|final and unappealable' "$L" || true
} > "$WORK/TRIPWIRES.txt"
echo "   tripwire hits: $(wc -l < "$WORK/TRIPWIRES.txt")"
echo "   unresolved placeholders: $(grep -cE '\b[QGRITHSEC]XXX\b|\bTBD\b' "$L" || true)"

# ----------------------------------------------------------------- 8. summary
banner "8. Summary"
{
  echo "BIOCORE ingest  label=$LABEL  stamp=$STAMP"
  echo "manual   : $PDF"
  echo "baseline : $BASELINE"
  echo "pages    : $("$PY" -c "import json,io,sys; print(json.load(io.open(sys.argv[1],encoding='utf-8'))['pages'])" "$SPANS/stats.json")"
  echo "rules    : $(wc -l < "$WORK/rule_ids.txt")   added=$(wc -l < "$WORK/rules_ADDED.txt")  removed=$(wc -l < "$WORK/rules_REMOVED.txt")  changed=$(($(wc -l < "$WORK/rules_CHANGED.tsv") - 1))"
  echo "gamespec : $(($(wc -l < "$WORK/rules_GAMESPECIFIC.tsv") - 1))   evergreen=$(($(wc -l < "$WORK/rules_EVERGREEN.tsv") - 1))"
  echo "glossary : $(wc -l < "$WORK/glossary_terms.txt")   added=$(wc -l < "$WORK/glossary_ADDED.txt")  removed=$(wc -l < "$WORK/glossary_REMOVED.txt")"
  echo "undefined: $(($(wc -l < "$WORK/UNDEFINED_CAPS.tsv") - 1)) caps tokens, $(($(wc -l < "$WORK/UNDEFINED_CAPS_PHRASES.tsv") - 1)) phrases"
  echo "violations: $(($(wc -l < "$WORK/violations.tsv") - 1))"
} | tee "$WORK/SUMMARY.txt"

cat <<EOF

==========================================================
 INGEST COMPLETE -> $WORK
==========================================================
 Hand these to the review, in this order:

   1. rules_GAMESPECIFIC.tsv     blue-headline rules -- this IS the new game
   2. rules_ADDED.txt            rule ids that did not exist in the baseline
   3. rules_CHANGED.tsv          evergreen rules FIRST quietly edited (+ _DETAIL for diffs)
   4. rules_REMOVED.txt          rules that vanished -- ask what replaced them
   5. glossary_ADDED.txt         the new game's defined nouns
   6. UNDEFINED_CAPS.tsv         ALL-CAPS used but never defined  <- loophole signal
   7. violations.tsv             every enforcement clause, attached to its rule
   8. SCORED_WHEN.txt            scored-live vs scored-at-the-buzzer evidence
   9. scoring/timing/dimension/penalty_mentions.txt
  10. TRIPWIRES.txt              ambiguity, discretion hooks, carve-outs
  11. SECTION_MAP.tsv            where everything lives
  12. spans/rules.json           every rule with body text, class, colour, page

 full_lines.txt is the authoritative body text. full_layout.txt is TABLES ONLY.
 Log: $LOG
EOF
