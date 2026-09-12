#!/usr/bin/env bash
# rebuild-corpus.sh -- download FIRST's source documents, then regenerate every text
# artifact the public repository leaves out.
#
# FIRST's game manuals, Q&A archives, Team Updates and award documents are copyrighted, so
# the repository carries neither the PDFs nor the text extracted from them in bulk. This
# script rebuilds each excluded artifact that the tools and documents read, from the PDFs,
# with the command that made the original.
#
# USAGE (paths resolve from this script's location, so any working directory works)
#   bash tools/rebuild-corpus.sh --help    this text
#   bash tools/rebuild-corpus.sh --fetch   download the source PDFs into manuals/ and
#                                          reference/awards/pdfs/, and the award web pages
#                                          into reference/awards/_web/
#   bash tools/rebuild-corpus.sh           regenerate the text artifacts from the PDFs on
#                                          disk, and name any that cannot be built
#   add --force to either                  redo work that already exists (for --fetch this
#                                          applies to the award PDFs and pages only; delete a
#                                          manual to download it again)
#
# Without --force, anything already on disk is skipped, so a second run changes nothing.
# The closing summary counts what was built, skipped and missing, and names each missing
# artifact with the PDF or program it needs. Exit status: 0 when nothing is missing.
#
# WHAT THE DEFAULT RUN BUILDS
#   1 research/rule_inventories/_text/<year>.txt     pdftotext -layout of each game manual
#   2 research/rule_inventories/_text/qa_<year>.txt  pdftotext -layout of each Q&A archive
#   3 manuals/archive/frc/_txt/<YEAR>_<GAME>.txt     the same manual text, 2022 on
#   4 research/rule_inventories/<year>_bodies_v2.jsonl, _changes_v2.md, _changes_linked_v2.md
#                                                    tools/rule-inventory.py, run with --out in
#                                                    a temporary directory so the published
#                                                    cross-year tables stay as they are
#   5 research/rule_inventories/<year>_rules_full.txt  tools/rules-full.py (and, from 2027 on,
#                                                    <year>_violations.tsv)
#   6 reference/validation/ingest_dryrun_REBUILT_vs_REEFSCAPE/  the excluded files of that
#                                                    run: tools/ingest-manual.sh, 2026 manual
#                                                    against the 2025 baseline
#   7 review/<run>/BRIEFING_PACK.md                  tools/RUN-KICKOFF.sh phase 1 in a
#                                                    temporary directory, for the three
#                                                    rehearsal runs kept under review/
#   8 reference/awards/_text/*.txt                   tools/award-text.py
#   9 reference/awards/_web/*.txt                    checked only; --fetch writes them
# Which seasons count as expected comes from the published companion tables: <year>_rules_v2.tsv
# for the JSONL, <year>_rules.tsv for the manual text and _rules_full.txt, qa_heat_<year>.tsv
# for the Q&A text. A newer manual on disk (the 2027 one, after kickoff) is built as well.
#
# HOW CLOSE A REBUILD COMES TO THE ORIGINAL
#   Steps 1-4 and 8 reproduce the originals byte for byte with the xpdf pdftotext 4.06 that
#   ships with Git for Windows and PyMuPDF 1.28.2. Other pdftotext builds can differ in
#   whitespace. Step 5 matches the original format only: the script that wrote the 2016-2026
#   files was never saved, and tools/rules-full.py reads the v2 extraction instead. Step 6
#   differs in spans/rules.json ("source") and spans/stats.json (one added key). Step 7
#   differs in the run stamp and path lines, and the V1 pack gains the SELF-DIFF banner that
#   RUN-KICKOFF.sh added after that run.
#
# NOT REBUILDABLE (no tool in the repository produces these)
#   research/rule_inventories/<year>.json   no writer exists; tools/rules-full.py reads
#                                           <year>_bodies_v2.jsonl instead
#   reference/awards/awards.yaml, reference/awards/01_AWARD_WINNING_PATTERNS.md
#                                           hand-written analysis, withheld until their
#                                           quotations of FIRST's award text are cut down
#   review/LATEST, review/*/.ingest_dir, research/teamupdate_analysis/.watch_state.json
#                                           per-machine run state; the tools recreate it
#
# REQUIREMENTS
#   bash, curl (--fetch), python 3 with PyMuPDF (python -m pip install pymupdf), pdftotext
#   (poppler-utils, or xpdf). PYTHON=<exe> picks the interpreter; TMPDIR is honored.
#   --fetch rewrites reference/awards/pdfs/MANIFEST.csv; a changed sha256 there means FIRST
#   revised that document. The manual fetcher logs to manuals/fetch.log, not logs/.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-python}"
export PYTHONIOENCODING=utf-8

MODE=build
FORCE=0
for arg in "$@"; do
  case "$arg" in
    -h|--help) awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "${BASH_SOURCE[0]}"; exit 0 ;;
    --fetch) MODE=fetch ;;
    --force) FORCE=1 ;;
    *) echo "unknown option: $arg  (see: bash tools/rebuild-corpus.sh --help)" >&2; exit 2 ;;
  esac
done

FRC="$ROOT/manuals/archive/frc"
INV="$ROOT/research/rule_inventories"
TEXT="$INV/_text"
TXT="$FRC/_txt"
AWARDS="$ROOT/reference/awards"
VAL="$ROOT/reference/validation/ingest_dryrun_REBUILT_vs_REEFSCAPE"

BUILT=0; SKIPPED=0; MISSING=0; FAILED=0
MISSING_LINES=()

rel()          { case "$1" in "$ROOT"/*) printf '%s' "${1#"$ROOT"/}" ;; *) printf '%s' "$1" ;; esac; }
banner()       { printf '\n== %s ==\n' "$*"; }
note_built()   { BUILT=$((BUILT + 1)); printf '  built    %s\n' "$(rel "$1")"; }
note_skip()    { SKIPPED=$((SKIPPED + 1)); STEP_SKIPS=$((STEP_SKIPS + 1)); }
note_missing() { MISSING=$((MISSING + 1)); MISSING_LINES+=("$(rel "$1")  ($2)")
                 printf '  MISSING  %s  (%s)\n' "$(rel "$1")" "$2"; }
note_failed()  { FAILED=$((FAILED + 1)); MISSING_LINES+=("$(rel "$1")  (FAILED: $2)")
                 printf '  FAILED   %s  (%s)\n' "$(rel "$1")" "$2"; }
step()         { banner "$*"; STEP_SKIPS=0; }
step_end()     { [ "$STEP_SKIPS" -gt 0 ] && printf '  skip     %d already present\n' "$STEP_SKIPS"; return 0; }
needs_build()  { [ "$FORCE" = 1 ] || [ ! -e "$1" ]; }

# years_from DIR REGEX: the 4-digit years captured by REGEX's one group, sorted, unique
years_from()   { ls "$1" 2>/dev/null | grep -v Section | sed -nE "s/$2/\1/p" | sort -u; }
union()        { printf '%s\n' "$@" | grep -E '^[0-9]{4}$' | sort -u; }
ge()           { local min="$1" y; shift; for y in "$@"; do [ "$y" -ge "$min" ] && echo "$y"; done; return 0; }

manual_for() { # manual_for YEAR: path of that season's game manual PDF
  local f
  for f in "$FRC/$1"_*_GameManual.pdf "$FRC/$1"_*GameManual*.pdf; do
    case "$f" in *'*'*|*Section*) continue ;; esac
    [ -f "$f" ] && { printf '%s\n' "$f"; return 0; }
  done
  return 1
}
qanda_for() { # qanda_for YEAR: path of that season's Q&A archive PDF
  local f
  for f in "$FRC/$1"_*_QandA.pdf; do
    [ -f "$f" ] && { printf '%s\n' "$f"; return 0; }
  done
  return 1
}

HAVE_PY=0; command -v "$PY" >/dev/null 2>&1 && HAVE_PY=1
HAVE_MUPDF=0; [ "$HAVE_PY" = 1 ] && "$PY" -c "import pymupdf" >/dev/null 2>&1 && HAVE_MUPDF=1
HAVE_PDFTOTEXT=0; command -v pdftotext >/dev/null 2>&1 && HAVE_PDFTOTEXT=1
[ "$HAVE_PY" = 1 ] || { echo "python not found (set PYTHON=<exe>)" >&2; exit 1; }

# Expected seasons, read off the published companion tables.
RULES_V2_YEARS="$(years_from "$INV" '^([0-9]{4})_rules_v2\.tsv$')"
RULES_TSV_YEARS="$(years_from "$INV" '^([0-9]{4})_rules\.tsv$')"
QA_YEARS="$(years_from "$INV" '^qa_heat_([0-9]{4})\.tsv$')"
LAST="$(printf '%s\n' $RULES_V2_YEARS | tail -1)"
LOCAL_MANUAL_YEARS="$(years_from "$FRC" '^([0-9]{4})_.*GameManual.*\.pdf$')"
LOCAL_QA_YEARS="$(years_from "$FRC" '^([0-9]{4})_[A-Z]+_QandA\.pdf$')"
VIOLATIONS_FROM=2027   # KICKOFF_PLAYBOOK.md 0.2G writes <year>_violations.tsv for the new season only
AWARD_PDFS="$("$PY" "$AWARDS/fetch_award_pdfs.py" --list </dev/null | tr -d '\r')"
AWARD_PAGES="$("$PY" "$AWARDS/fetch_award_pages.py" --list </dev/null | tr -d '\r')"

summary() { # summary NEXT-HINT
  banner "Summary"
  printf '  built    %d\n' "$BUILT"
  printf '  skipped  %d  (already present; --force redoes them)\n' "$SKIPPED"
  printf '  missing  %d\n' "$((MISSING + FAILED))"
  local i=0 l
  for l in ${MISSING_LINES[@]+"${MISSING_LINES[@]}"}; do
    i=$((i + 1))
    if [ "$i" -le 40 ]; then printf '    %s\n' "$l"; fi
  done
  [ "$i" -gt 40 ] && printf '    ... and %d more (see the MISSING lines above)\n' "$((i - 40))"
  [ -n "$1" ] && printf '\n  %s\n' "$1"
  [ "$MISSING" -eq 0 ] && [ "$FAILED" -eq 0 ]
}

# ================================================================= --fetch
if [ "$MODE" = fetch ]; then
  command -v curl >/dev/null 2>&1 || { echo "curl not found; --fetch needs it" >&2; exit 1; }
  mkdir -p "$ROOT/manuals"

  step "1. Game manuals, Q&A archives, Team Updates (tools/fetch-frc-manuals.sh; log: manuals/fetch.log)"
  FETCH_LOG="$ROOT/manuals/fetch.log" bash "$ROOT/tools/fetch-frc-manuals.sh" </dev/null \
    | awk '/^SKIP/ { s++; next } /^=== DONE/ { next } /^[0-9]+$/ { next } { print "  " $0 }
           END { if (s) printf "  skip     %d already on disk\n", s }'

  step "2. Award PDFs (reference/awards/fetch_award_pdfs.py)"
  all=1; for n in $AWARD_PDFS; do [ -f "$AWARDS/pdfs/$n" ] || all=0; done
  if [ "$all" = 1 ] && [ "$FORCE" = 0 ]; then
    echo "  skip     all $(echo $AWARD_PDFS | wc -w) already on disk"
  else
    "$PY" "$AWARDS/fetch_award_pdfs.py" </dev/null | tr -d '\r' | sed 's/^/  /'
  fi

  step "3. Award web pages (reference/awards/fetch_award_pages.py)"
  all=1; for n in $AWARD_PAGES; do [ -f "$AWARDS/_web/$n" ] || all=0; done
  if [ "$all" = 1 ] && [ "$FORCE" = 0 ]; then
    echo "  skip     all $(echo $AWARD_PAGES | wc -w) already on disk"
  else
    "$PY" "$AWARDS/fetch_award_pages.py" </dev/null | tr -d '\r' | sed 's/^/  /'
  fi

  step "4. Check: every source the default run needs"
  for y in $RULES_V2_YEARS; do
    if manual_for "$y" >/dev/null; then note_skip
    else note_missing "$FRC/${y}_<GAME>_GameManual.pdf" "not downloaded; see manuals/fetch.log"; fi
  done
  for y in $QA_YEARS; do
    if qanda_for "$y" >/dev/null; then note_skip
    else note_missing "$FRC/${y}_<GAME>_QandA.pdf" "not downloaded; see manuals/fetch.log"; fi
  done
  for n in $AWARD_PDFS; do
    if [ -f "$AWARDS/pdfs/$n" ]; then note_skip; else note_missing "$AWARDS/pdfs/$n" "not downloaded"; fi
  done
  for n in $AWARD_PAGES; do
    if [ -f "$AWARDS/_web/$n" ]; then note_skip; else note_missing "$AWARDS/_web/$n" "not downloaded"; fi
  done
  printf '  present  %d\n' "$STEP_SKIPS"
  SKIPPED=0
  summary "Next: bash tools/rebuild-corpus.sh"
  exit $?
fi

# ================================================================= default: build
TMP="$(mktemp -d "${TMPDIR:-/tmp}/rebuild-corpus.XXXXXX")" || { echo "mktemp failed" >&2; exit 1; }
trap 'rm -rf "$TMP"' EXIT
echo "rebuild-corpus: $(rel "$ROOT")  (force=$FORCE, pymupdf=$HAVE_MUPDF, pdftotext=$HAVE_PDFTOTEXT)"

# ---------------------------------------------------------------- 1. manual text
step "1. Game manual text: research/rule_inventories/_text/<year>.txt"
mkdir -p "$TEXT"
for y in $(union $RULES_TSV_YEARS $(ge 2016 $LOCAL_MANUAL_YEARS)); do
  out="$TEXT/$y.txt"
  needs_build "$out" || { note_skip; continue; }
  pdf="$(manual_for "$y")" || { note_missing "$out" "needs the $y game manual PDF; run --fetch"; continue; }
  [ "$HAVE_PDFTOTEXT" = 1 ] || { note_missing "$out" "needs pdftotext"; continue; }
  if pdftotext -layout "$pdf" "$out" 2>/dev/null; then note_built "$out"
  else rm -f "$out"; note_failed "$out" "pdftotext failed on $(rel "$pdf")"; fi
done
step_end

# ---------------------------------------------------------------- 2. Q&A text
step "2. Q&A text: research/rule_inventories/_text/qa_<year>.txt"
for y in $(union $QA_YEARS $LOCAL_QA_YEARS); do
  out="$TEXT/qa_$y.txt"
  needs_build "$out" || { note_skip; continue; }
  pdf="$(qanda_for "$y")" || { note_missing "$out" "needs the $y Q&A archive PDF; run --fetch"; continue; }
  [ "$HAVE_PDFTOTEXT" = 1 ] || { note_missing "$out" "needs pdftotext"; continue; }
  if pdftotext -layout "$pdf" "$out" 2>/dev/null; then note_built "$out"
  else rm -f "$out"; note_failed "$out" "pdftotext failed on $(rel "$pdf")"; fi
done
step_end

# ---------------------------------------------------------------- 3. _txt copies
step "3. Manual text for defense_rule_trend.py and manual_award_order.py: manuals/archive/frc/_txt/"
mkdir -p "$TXT"
for y in $(union $(ge 2022 $RULES_TSV_YEARS) $(ge 2022 $LOCAL_MANUAL_YEARS)); do
  if pdf="$(manual_for "$y")"; then
    name="$(basename "$pdf" .pdf)"; out="$TXT/${name%_GameManual}.txt"
  else
    out="$(ls "$TXT/${y}"_*.txt 2>/dev/null | head -1)"
    [ -n "$out" ] || out="$TXT/${y}_<GAME>.txt"
  fi
  needs_build "$out" || { note_skip; continue; }
  [ -n "$pdf" ] || { note_missing "$out" "needs the $y game manual PDF; run --fetch"; continue; }
  if [ -s "$TEXT/$y.txt" ]; then
    cp -f "$TEXT/$y.txt" "$out" && note_built "$out"
  elif [ "$HAVE_PDFTOTEXT" = 1 ] && pdftotext -layout "$pdf" "$out" 2>/dev/null; then
    note_built "$out"
  else
    rm -f "$out"; note_missing "$out" "needs pdftotext"
  fi
done
step_end

# ---------------------------------------------------------------- 4. rule inventory
step "4. Rule bodies and change reports: tools/rule-inventory.py"
need=""
for y in $(union $RULES_V2_YEARS $(ge 2015 $LOCAL_MANUAL_YEARS)); do
  out="$INV/${y}_bodies_v2.jsonl"
  needs_build "$out" || { note_skip; continue; }
  if manual_for "$y" >/dev/null; then need="$need $y"
  else note_missing "$out" "needs the $y game manual PDF; run --fetch"; fi
done
reports=""
for r in _changes_v2.md _changes_linked_v2.md; do
  needs_build "$INV/$r" && reports="$reports $r" || note_skip
done
window=""
if [ -n "$reports" ]; then
  gap=""
  if [ -n "$LAST" ] && [ "$LAST" -ge 2023 ]; then
    for y in $(seq 2022 "$LAST"); do
      manual_for "$y" >/dev/null || [ -e "$INV/${y}_bodies_v2.jsonl" ] || gap="$gap $y"
    done
  else
    gap=" (no published <year>_rules_v2.tsv from 2023 on)"
  fi
  if [ -n "$gap" ]; then
    for r in $reports; do note_missing "$INV/$r" "needs the game manuals for 2022-$LAST; absent:$gap"; done
    reports=""
  else
    window="$(seq 2022 "$LAST")"
  fi
fi
if [ -n "$need$reports" ] && [ "$HAVE_MUPDF" = 0 ]; then
  for y in $need; do note_missing "$INV/${y}_bodies_v2.jsonl" "needs PyMuPDF"; done
  for r in $reports; do note_missing "$INV/$r" "needs PyMuPDF"; done
elif [ -n "$need$reports" ]; then
  run="$(union $need $window)"
  lo="$(printf '%s\n' $run | head -1)"; hi="$(printf '%s\n' $run | tail -1)"
  ri="$TMP/ri"; mkdir -p "$ri"
  # Seed the cache with every JSONL already built, except the ones --force redoes.
  for y in $(seq "$lo" "$hi"); do
    [ -e "$INV/${y}_bodies_v2.jsonl" ] || continue
    [ "$FORCE" = 1 ] && manual_for "$y" >/dev/null && continue
    cp -f "$INV/${y}_bodies_v2.jsonl" "$ri/"
  done
  echo "  running  tools/rule-inventory.py --years $lo-$hi --no-extract --out <tmp>  (seconds per manual it extracts)"
  if "$PY" "$ROOT/tools/rule-inventory.py" --years "$lo-$hi" --no-extract --out "$ri" \
       > "$TMP/rule-inventory.log" 2>&1 </dev/null; then
    for y in $need; do
      if [ -s "$ri/${y}_bodies_v2.jsonl" ]; then cp -f "$ri/${y}_bodies_v2.jsonl" "$INV/" && note_built "$INV/${y}_bodies_v2.jsonl"
      else note_failed "$INV/${y}_bodies_v2.jsonl" "rule-inventory.py wrote no JSONL for $y"; fi
    done
    for r in $reports; do
      if [ -s "$ri/$r" ]; then cp -f "$ri/$r" "$INV/" && note_built "$INV/$r"
      else note_failed "$INV/$r" "rule-inventory.py did not write it"; fi
    done
  else
    tr -d '\r' < "$TMP/rule-inventory.log" | tail -5 | sed 's/^/    /'
    for y in $need; do note_failed "$INV/${y}_bodies_v2.jsonl" "rule-inventory.py exited non-zero"; done
    for r in $reports; do note_failed "$INV/$r" "rule-inventory.py exited non-zero"; done
  fi
fi
step_end

# ---------------------------------------------------------------- 5. rules_full
step "5. Flat rule text: research/rule_inventories/<year>_rules_full.txt (tools/rules-full.py)"
for y in $(union $RULES_TSV_YEARS $(ge 2016 $(years_from "$INV" '^([0-9]{4})_bodies_v2\.jsonl$'))); do
  out="$INV/${y}_rules_full.txt"
  viol="$INV/${y}_violations.tsv"
  wantviol=0; [ "$y" -ge "$VIOLATIONS_FROM" ] && wantviol=1
  if needs_build "$out"; then
    if [ ! -s "$INV/${y}_bodies_v2.jsonl" ]; then
      note_missing "$out" "needs ${y}_bodies_v2.jsonl (step 4)"
      [ "$wantviol" = 1 ] && needs_build "$viol" && note_missing "$viol" "needs ${y}_rules_full.txt"
      continue
    fi
    flag=""; [ "$wantviol" = 1 ] && needs_build "$viol" && flag="--violations"
    if "$PY" "$ROOT/tools/rules-full.py" "$y" $flag >/dev/null 2>&1 </dev/null; then
      note_built "$out"; [ -n "$flag" ] && note_built "$viol"
    else
      note_failed "$out" "tools/rules-full.py $y exited non-zero"
    fi
  else
    note_skip
    if [ "$wantviol" = 1 ]; then
      if ! needs_build "$viol"; then note_skip
      elif "$PY" "$ROOT/tools/rules-full.py" "$y" --violations-only >/dev/null 2>&1 </dev/null; then note_built "$viol"
      else note_failed "$viol" "tools/rules-full.py $y --violations-only exited non-zero"; fi
    fi
  fi
done
step_end

# ---------------------------------------------------------------- 6. validation run
step "6. Validation dry run: reference/validation/ingest_dryrun_REBUILT_vs_REEFSCAPE/ (tools/ingest-manual.sh)"
VAL_FILES="spans full_raw.txt full_layout.txt full_lines.txt rules_CHANGED_DETAIL.txt glossary.tsv
  glossary_ADDED.txt glossary_REMOVED.txt glossary_CHANGED.tsv violations.tsv violation_lines_raw.txt
  scoring_mentions.txt timing_mentions.txt dimension_mentions.txt penalty_mentions.txt SCORED_WHEN.txt
  TRIPWIRES.txt UNDEFINED_CAPS.tsv"
if [ -d "$VAL" ]; then
  todo=""
  for f in $VAL_FILES; do needs_build "$VAL/$f" && todo="$todo $f" || note_skip; done
  if [ -n "$todo" ]; then
    new="$(manual_for 2026)"; base="$(manual_for 2025)"
    why=""
    [ -n "$new" ] && [ -n "$base" ] || why="needs the 2025 and 2026 game manual PDFs; run --fetch"
    [ -z "$why" ] && [ "$HAVE_MUPDF" = 0 ] && why="needs PyMuPDF"
    if [ -n "$why" ]; then
      for f in $todo; do note_missing "$VAL/$f" "$why"; done
    else
      w="$TMP/val"; mkdir -p "$w"
      echo "  running  tools/ingest-manual.sh on the 2026 manual, baseline 2025  (about 30 s)"
      if INGEST_OUT="$w" BASELINE="$base" bash "$ROOT/tools/ingest-manual.sh" "$new" DRYRUN \
           > "$TMP/ingest.log" 2>&1 </dev/null; then
        d="$(ls -d "$w"/ingest_DRYRUN_* 2>/dev/null | head -1)"
        for f in $todo; do
          if [ -d "$d/$f" ]; then mkdir -p "$VAL/$f" && cp -rf "$d/$f/." "$VAL/$f/" && note_built "$VAL/$f"
          elif [ -s "$d/$f" ]; then cp -f "$d/$f" "$VAL/$f" && note_built "$VAL/$f"
          elif [ "$HAVE_PDFTOTEXT" = 0 ]; then note_missing "$VAL/$f" "needs pdftotext"
          else note_failed "$VAL/$f" "ingest-manual.sh did not write it"; fi
        done
      else
        tr -d '\r' < "$TMP/ingest.log" | tail -5 | sed 's/^/    /'
        for f in $todo; do note_failed "$VAL/$f" "ingest-manual.sh exited non-zero"; done
      fi
    fi
  fi
fi
step_end

# ---------------------------------------------------------------- 7. briefing packs
step "7. Briefing packs: review/<run>/BRIEFING_PACK.md (tools/RUN-KICKOFF.sh phase 1)"
# review dir | manual season | label | baseline season | file name the manual was run under
PACKS=(
  "V1_20260823T014011Z 2026 V1 2026 -"
  "NOT-BIOCORE-REEFSCAPE_20260823T021245Z 2025 NOT-BIOCORE-REEFSCAPE 2026 -"
  "DEEPSPACE_20260824T032851Z 2019 DEEPSPACE 2018 DEEPSPACE.pdf"
)
known=" "
n=0
for p in "${PACKS[@]}"; do
  read -r dir my label by as <<< "$p"
  known="$known$dir "
  rd="$ROOT/review/$dir"; out="$rd/BRIEFING_PACK.md"
  [ -d "$rd" ] || continue
  needs_build "$out" || { note_skip; continue; }
  pdf="$(manual_for "$my")"; bpdf="$(manual_for "$by")"
  if [ -z "$pdf" ] || [ -z "$bpdf" ]; then
    note_missing "$out" "needs the $my and $by game manual PDFs; run --fetch"; continue
  fi
  [ "$HAVE_MUPDF" = 1 ] || { note_missing "$out" "needs PyMuPDF"; continue; }
  n=$((n + 1)); w="$TMP/pack$n"; mkdir -p "$w"
  src="$pdf"
  if [ "$as" != "-" ]; then cp -f "$pdf" "$w/$as"; src="$w/$as"; fi
  echo "  running  tools/RUN-KICKOFF.sh $(basename "$src") $label  (baseline $by, about 30 s)"
  if REVIEW_ROOT="$w/review" INGEST_OUT="$w/ingest" BASELINE="$bpdf" \
       bash "$ROOT/tools/RUN-KICKOFF.sh" "$src" "$label" > "$w/run.log" 2>&1 </dev/null \
     && pack="$(ls "$w/review/${label}_"*/BRIEFING_PACK.md 2>/dev/null | head -1)" && [ -s "$pack" ]; then
    body="$(cat "$pack")"
    body="${body//"$w"/<tmp>}"
    body="${body//"$ROOT"\//}"
    printf '%s\n' "$body" > "$out" && note_built "$out"
  else
    tr -d '\r' < "$w/run.log" | tail -5 | sed 's/^/    /'
    note_failed "$out" "RUN-KICKOFF.sh phase 1 did not produce a pack"
  fi
done
for rd in "$ROOT"/review/*/; do
  dir="$(basename "$rd")"
  case "$known" in *" $dir "*) continue ;; esac
  [ -f "$rd/ingest.log" ] && [ ! -f "$rd/BRIEFING_PACK.md" ] || continue
  note_missing "$rd/BRIEFING_PACK.md" "no recipe for this run; rerun tools/RUN-KICKOFF.sh phase 1 on its manual by hand"
done
step_end

# ---------------------------------------------------------------- 8. award text
step "8. Award document text: reference/awards/_text/ (tools/award-text.py)"
flag=""; [ "$FORCE" = 1 ] && flag="--force"
"$PY" "$ROOT/tools/award-text.py" $flag > "$TMP/award-text.log" 2>&1 </dev/null
while IFS= read -r line; do
  line="${line%$'\r'}"
  case "$line" in
    "  built    "*) note_built "$ROOT/${line#  built    }" ;;
    "  skip     "*) note_skip ;;
    "  MISSING  "*|"  FAILED   "*)
      rest="${line:11}"; why="${rest#*  (}"; why="${why%)}"
      case "$line" in "  MISSING"*) note_missing "$ROOT/${rest%%  (*}" "$why" ;;
                      *)            note_failed  "$ROOT/${rest%%  (*}" "$why" ;; esac ;;
  esac
done < "$TMP/award-text.log"
step_end

# ---------------------------------------------------------------- 9. award web pages
step "9. Award web page snapshots: reference/awards/_web/ (downloaded, not derived)"
for f in $AWARD_PAGES; do
  if [ -f "$AWARDS/_web/$f" ]; then note_skip
  else note_missing "$AWARDS/_web/$f" "a web page snapshot; run --fetch"; fi
done
step_end

# ---------------------------------------------------------------- not rebuildable
banner "Not rebuildable (no tool produces these; see --help)"
absent_json=""
for y in $(years_from "$INV" '^([0-9]{4})\.txt$'); do
  [ -e "$INV/$y.json" ] || absent_json="$absent_json $y"
done
[ -n "$absent_json" ] && echo "  research/rule_inventories/<year>.json for$absent_json: tools/rules-full.py reads <year>_bodies_v2.jsonl instead"
for f in awards.yaml 01_AWARD_WINNING_PATTERNS.md; do
  [ -e "$AWARDS/$f" ] || echo "  reference/awards/$f: hand-written, withheld until its FIRST quotations are cut down"
done

summary ""
exit $?
