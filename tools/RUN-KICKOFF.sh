#!/usr/bin/env bash
# RUN-KICKOFF.sh -- the ONE command for kickoff day.
#
#   bash tools/RUN-KICKOFF.sh <manual.pdf>          # phase 1: mechanical extraction
#   bash tools/RUN-KICKOFF.sh --phase2 <review_dir> # phase 2: quantitative pass
#
# You should never need to type phase 2 yourself. CLAUDE.md instructs the assistant to run
# phase 1, read the briefing pack, fill three small schema files, then run phase 2 and write
# the review. Your one step is: put the manual in this folder and say "run kickoff".
#
# WHY TWO PHASES
#   Phase 1 is everything a script can know without understanding the game: rule inventory,
#   evergreen-vs-game-specific split (read from FIRST's headline COLOUR, not any word),
#   baseline diff, glossary delta, undefined ALL-CAPS, every Violation: clause, ambiguity
#   tripwires, section map.
#   Phase 2 needs three things only a reader of the manual can supply -- the scoring actions
#   and their point values, the candidate strategies, and the mechanisms each implies. The
#   assistant fills those into stub files; then the arithmetic is mechanical again.
#
# Nothing here needs the network. Safe to run offline in a competition venue.
#
# Env overrides (the defaults are what kickoff day uses; tools/rebuild-corpus.sh sets both
# to temporary directories when it regenerates a historical briefing pack):
#   REVIEW_ROOT=<dir>  where review/<label>_<stamp>/ and LATEST go   (default: review)
#   INGEST_OUT=<dir>   where tools/ingest-manual.sh writes            (default: manuals/2026-27_BIOCORE)
#   BASELINE=<pdf>     manual to diff against, passed to ingest-manual.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-python}"
export PYTHONIOENCODING=utf-8
REVIEW_ROOT="${REVIEW_ROOT:-$ROOT/review}"
INGEST_OUT="${INGEST_OUT:-$ROOT/manuals/2026-27_BIOCORE}"
export INGEST_OUT
case "${1:-}" in -h|--help) sed -n '2,27p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;; esac

banner() { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
ok()     { printf '   \033[32mOK\033[0m   %s\n' "$*"; }
warn()   { printf '   \033[33mWARN\033[0m %s\n' "$*"; }
die()    { printf '\n!! %s\n' "$*" >&2; exit 1; }

# =============================================================== PHASE 2
if [ "${1:-}" = "--phase2" ]; then
  # <review_dir> may be omitted: review/LATEST names the dir the last phase-1 run created.
  REVIEW="${2:-}"
  if [ -z "$REVIEW" ] || [ "$REVIEW" = "LATEST" ] || [ "$REVIEW" = "review/LATEST" ]; then
    [ -f "$REVIEW_ROOT/LATEST" ] || die "no review dir given and review/LATEST does not exist -- run phase 1 first."
    REVIEW="$(cat "$REVIEW_ROOT/LATEST")"
  fi
  [ -d "$REVIEW" ] || die "no such review dir: $REVIEW"
  GAMEDEF="$REVIEW/game_def.json"
  CANDS="$REVIEW/candidates.yaml"
  BOMCFG="$REVIEW/bom_config.yaml"
  OUT="$REVIEW/results"
  mkdir -p "$OUT"

  banner "Phase 2 preflight"
  for f in "$GAMEDEF" "$CANDS" "$BOMCFG"; do
    [ -f "$f" ] || die "missing $f -- phase 2 needs all three schema files filled in."
    grep -q 'FILL_ME' "$f" && die "$(basename "$f") still contains FILL_ME placeholders. Fill it before phase 2."
  done
  ok "all three schema files present and filled"

  # The 2026 rehearsal costed, gate-checked, scheduled and ordered parts for a robot with no legal
  # path to the scoring aperture (a hopper dump against a HUB opening 72 in off the carpet). The
  # geometric gate in bom-builder.py catches that -- but ONLY when bom_config declares a target.
  # Leaving `target:` out downgraded the fatal error to a warning nobody reads, which is the exact
  # silence that produced the defect. So a missing or unanswered target is a HARD preflight failure.
  if ! grep -qE '^[[:space:]]*target:' "$BOMCFG"; then
    die "bom_config.yaml declares no 'target:' block.
   Phase 2 will not run without one -- a BOM that is never checked for reach is how the 2026
   rehearsal ordered parts for a robot that could not score.
   Add, from the manual (see reference/03_ARCHETYPE_CORPUS.md 2.4 item 4 -- 'find this number first'):
     target:
       name: \"<scoring opening>\"
       aperture_height_in: <how far off the carpet the opening is>
       aperture_range_in:  <how far away you may deliver from>
       source: \"manual s5.x\""
  fi
  # Strip the trailing YAML comment BEFORE the quotes/whitespace, or an inline `# manual s5.4`
  # gets concatenated onto the number (beta test 2026-08-23 produced "72#manuals5.4/...").
  APH="$(grep -E '^[[:space:]]*aperture_height_in:' "$BOMCFG" | head -1 \
         | sed -e 's/.*: *//' -e 's/#.*//' | tr -d '\r\"'"'"' ')"
  case "${APH:-}" in
    ''|0|0.0|null|None) die "bom_config.yaml has 'target:' but aperture_height_in is missing or 0.
   A zero aperture clears every mechanism and reinstates exactly the blindness this gate exists to end.
   Put the real height from the manual in it." ;;
  esac
  ok "geometric target declared: aperture_height_in = $APH"

  banner "1. Cycle / expected-value model"
  "$PY" "$ROOT/tools/cycle-model.py" --game "$GAMEDEF" --cycle "${CYCLE:-8}" \
        --auto-scored "${AUTO_SCORED:-3}" | tee "$OUT/cycle_model.txt"
  "$PY" "$ROOT/tools/cycle-model.py" --game "$GAMEDEF" --sweep \
        --auto-scored "${AUTO_SCORED:-3}" | tee "$OUT/cycle_sweep.txt"

  banner "2. Strategy ranking (achievability x value, gates, tiers)"
  "$PY" "$ROOT/tools/score-strategy.py" --candidates "$CANDS" | tee "$OUT/strategy_ranking.txt"
  "$PY" "$ROOT/tools/score-strategy.py" --candidates "$CANDS" --json > "$OUT/strategy_ranking.json" 2>/dev/null \
    && ok "strategy_ranking.json" || warn "json export failed (non-fatal)"

  banner "3. Bill of materials + gates"
  "$PY" "$ROOT/tools/bom-builder.py" "$BOMCFG" --markdown > "$OUT/bom.md" 2>&1
  "$PY" "$ROOT/tools/bom-builder.py" "$BOMCFG" --csv "$OUT/bom.csv" > "$OUT/bom.txt" 2>&1
  tail -25 "$OUT/bom.txt"

  banner "4. Team Update watch (season-long)"
  "$PY" "$ROOT/tools/teamupdate-diff.py" season 2027 2>&1 | tail -12 | sed 's/^/   /'

  banner "PHASE 2 COMPLETE"
  cat <<EOF
   results -> $OUT
     cycle_model.txt        points/cycle, break-even for each endgame option, RP feasibility
     cycle_sweep.txt        cycle-time sensitivity -- flat columns = small-team strategies
     strategy_ranking.txt   ranked candidates: quadrant, tier, BINDING CONSTRAINT
     strategy_ranking.json  machine-readable
     bom.md / bom.csv       costed BOM with gate warnings and order-by dates

   Next: the assistant writes the review from these + the phase-1 briefing pack.
EOF
  exit 0
fi

# =============================================================== PHASE 1
PDF="${1:?usage: RUN-KICKOFF.sh <manual.pdf>}"
LABEL="${2:-V1}"
[ -f "$PDF" ] || die "no such file: $PDF  (archived manuals: bash tools/rebuild-corpus.sh --fetch)"
head -c4 "$PDF" | grep -q '%PDF' || die "not a PDF: $PDF"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REVIEW="$REVIEW_ROOT/${LABEL}_${STAMP}"
mkdir -p "$REVIEW"
# review/LATEST is the DEFINITION of `review/<dir>` used everywhere in CLAUDE.md.
# It is rewritten by every phase-1 run and read by phase 2 and by any resumed session,
# so <dir> never depends on scrollback or on "newest directory" guesswork.
printf '%s
' "$REVIEW" > "$REVIEW_ROOT/LATEST"

banner "BIOCORE KICKOFF PIPELINE -- phase 1 (mechanical)"
echo "   manual : $PDF"
echo "   review : $REVIEW"

banner "1. Ingest (rules, glossary, diff, tripwires)"
if bash "$ROOT/tools/ingest-manual.sh" "$PDF" "$LABEL" > "$REVIEW/ingest.log" 2>&1; then
  ok "ingest-manual.sh"
else
  warn "ingest-manual.sh returned non-zero -- see $REVIEW/ingest.log"
fi
WORK="$(ls -dt "$INGEST_OUT"/ingest_${LABEL}_* 2>/dev/null | head -1)"
[ -n "${WORK:-}" ] && [ -d "$WORK" ] || die "ingest produced no work dir; read $REVIEW/ingest.log"
ok "ingest output: $WORK"
echo "$WORK" > "$REVIEW/.ingest_dir"

banner "1b. Extraction sanity gate"
# Beta test 2026-08-23: the 2019 DEEP SPACE manual ran clean, reported PHASE 1 COMPLETE, and produced
# a 349-line briefing pack containing ZERO rules, ZERO violations and an EMPTY section map. The
# span parser (tools/frc_spans.py) keys on the modern layout; on a pre-2023 manual it matches nothing
# and returns empty. Silent emptiness is the worst possible failure here, because every downstream
# section still renders and a review can be written on nothing. Fail loudly instead.
#
# Calibration: every FRC season 2016-2026 has 124-228 rules (research/rule_inventories/
# counts_by_prefix.tsv). A floor of 100 clears the smallest real season with margin.
SANE_RULES=$(wc -l < "$WORK/rule_ids.txt" 2>/dev/null || echo 0)
SANE_VIOL=$(( $(wc -l < "$WORK/violations.tsv" 2>/dev/null || echo 1) - 1 ))
SANE_SECT=$(( $(wc -l < "$WORK/SECTION_MAP.tsv" 2>/dev/null || echo 1) - 1 ))
SANE_GLOS=$(wc -l < "$WORK/glossary_terms.txt" 2>/dev/null || echo 0)
printf '   rules=%s  violations=%s  sections=%s  glossary=%s\n' \
       "$SANE_RULES" "$SANE_VIOL" "$SANE_SECT" "$SANE_GLOS"
SANE_FAIL=""
[ "$SANE_RULES" -lt 100 ] && SANE_FAIL="${SANE_FAIL}rules=$SANE_RULES (every season 2016-2026 has 124-228) "
[ "$SANE_VIOL"  -lt 20  ] && SANE_FAIL="${SANE_FAIL}violations=$SANE_VIOL (REBUILT has 80) "
[ "$SANE_SECT"  -lt 20  ] && SANE_FAIL="${SANE_FAIL}sections=$SANE_SECT (REBUILT has 138) "
[ "$SANE_GLOS"  -lt 30  ] && SANE_FAIL="${SANE_FAIL}glossary=$SANE_GLOS (REBUILT has 100) "
if [ -n "$SANE_FAIL" ]; then
  die "EXTRACTION FAILED SANITY CHECK: $SANE_FAIL

   The parser matched almost nothing. A briefing pack built from this would look complete and
   contain no rules -- do not write a review from it.

   Most likely cause: the manual uses a layout tools/frc_spans.py does not handle. It keys on the
   2017+ gutter geometry and the 2023+ colour encoding. Pre-2017 manuals, and any future layout
   change, will land here.

   What to do:
     1. Confirm the PDF has selectable text:  pdftotext -f 1 -l 3 '$PDF' - | head
     2. Cross-check with the era-tolerant extractor, which handles 2016-2026:
          python tools/rule-inventory.py            # writes research/rule_inventories/
        If THAT finds rules and frc_spans.py does not, the layout changed and frc_spans.py needs
        its x-position/colour rules updated for the new era -- see its header comment.
     3. If FIRST changed the 2027 layout, fixing frc_spans.py is the first kickoff-day task.
        Until then the manual is still readable by hand; the pipeline is not."
fi
ok "extraction sane"

banner "2. Assemble briefing pack"
PACK="$REVIEW/BRIEFING_PACK.md"
{
  echo "# BIOCORE Kickoff Briefing Pack"
  echo
  echo "Generated $STAMP from \`$(basename "$PDF")\` (label $LABEL)."
  echo "Mechanical extraction only -- nothing here required understanding the game."
  echo
  echo "## Summary"; echo '```'
  cat "$WORK/SUMMARY.txt" 2>/dev/null || echo "(no SUMMARY.txt)"
  echo '```'
  echo
  echo "## GAME-SPECIFIC rules -- blue headline. THIS IS THE NEW GAME. Read every one."
  # Pass the path as ARGV, never interpolated into the -c source: $WORK is an MSYS path
  # (/c/Users/...) and native Windows python cannot open that form from a string literal.
  # As an argument, MSYS rewrites it to C:/Users/... on the way in. (Beta test 2026-08-23.)
  if [ "$($PY -c "import json,io,sys;print(json.load(io.open(sys.argv[1],encoding='utf-8')).get('colour_encoding'))" "$WORK/spans/stats.json" 2>/dev/null)" = "False" ]; then
    echo
    echo "> **⚠ THIS MANUAL HAS NO EVERGREEN/GAMESPEC COLOUR ENCODING** (a 2023+ convention)."
    echo "> Every rule below is UNKNOWN, so any count here is meaningless -- do **not** report"
    echo "> \"N rules are game-specific\". Derive the new-this-season set from the rule-id diff"
    echo "> (ADDED / CHANGED sections) instead."
    echo
  fi
  echo '```'
  cut -f1,4 "$WORK/rules_GAMESPECIFIC.tsv" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Rules ADDED vs the REBUILT baseline"; echo '```'
  cut -f1,2 "$WORK/rules_ADDED.txt" 2>/dev/null | head -60 || echo "(none)"
  echo '```'
  echo
  echo "## Rules REMOVED -- ask what replaced them"; echo '```'
  cut -f1,2 "$WORK/rules_REMOVED.txt" 2>/dev/null | head -40 || echo "(none)"
  echo '```'
  echo
  echo "## NEW glossary terms -- the game's defined nouns"; echo '```'
  cut -f1 "$WORK/glossary_ADDED.txt" 2>/dev/null | tr '\n' ' ' | fold -w 96 -s || echo "(none)"
  echo '```'
  echo
  echo "## UNDEFINED ALL-CAPS -- used in the body, never defined. LOOPHOLE SIGNAL."
  echo "Manual s1.6 promises ALL CAPS == defined term. Anything here is a typo, an acronym,"
  echo "or a load-bearing undefined term. The third kind is where rule arguments get won."
  echo '```'
  head -40 "$WORK/UNDEFINED_CAPS.tsv" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Every Violation: clause, attached to its rule"; echo '```'
  head -70 "$WORK/violations.tsv" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Scored-when evidence (live vs at-the-buzzer)"; echo '```'
  head -35 "$WORK/SCORED_WHEN.txt" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Scoring mentions"; echo '```'
  head -60 "$WORK/scoring_mentions.txt" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Timing mentions"; echo '```'
  head -35 "$WORK/timing_mentions.txt" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Section map"; echo '```'
  awk -F'\t' 'NR>1 && $1==1 {printf "p%-5s %s\n", $2, $3}' "$WORK/SECTION_MAP.tsv" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Ambiguity tripwires (first 120 lines)"; echo '```'
  head -120 "$WORK/TRIPWIRES.txt" 2>/dev/null || echo "(none)"
  echo '```'
  echo
  echo "## Priors to test against this manual"
  echo "- \`reference/RULE-CHURN-WATCHLIST.md\` -- rules predicted contentious (G413,R106,G403,G420,G427;"
  echo "  evergreen-but-unstable G415,G416,G211,R402,G409,G210,G425)"
  echo "- \`reference/QA-AMBIGUITY-HOTSPOTS.md\` -- bumpers R4xx and contact G41x are the historic core"
  echo "- \`research/04_biocore_community_intel.md\` -- the 10-item betting sheet; score it now"
  echo "- \`reference/SCOUTING-PLAN.md\` -- name the endgame structure and you know the free-data shape"
} > "$PACK"
ok "briefing pack: $(wc -l < "$PACK") lines"

# SELF-DIFF DETECTION. If the manual is byte-identical to the baseline, every diff section is
# empty and the whole "what changed" half of the pack is meaningless. CLAUDE.md told the reader
# to notice this; beta testing (2026-08-23, REBUILT vs default REBUILT baseline) showed the
# pipeline emitted `added=0 removed=0 changed=0` silently and a careless reader would have
# reported "no rules changed" as a finding. Announce it instead of relying on vigilance.
if grep -qE '^rules .*added=0 +removed=0 +changed=0' "$WORK/SUMMARY.txt" 2>/dev/null; then
  BANNER="$(cat <<'EOB'
> ## ⚠ SELF-DIFF — THIS IS A REHEARSAL, NOT KICKOFF
>
> Every rule/glossary diff below is **zero** because the manual you supplied is the **same document
> as the diff baseline**. Nothing changed because nothing could change.
>
> **Do NOT report "no rules were added/removed/changed" as a finding.** The ADDED / REMOVED /
> CHANGED and glossary-delta sections carry no information in this run and must be omitted from
> any review.
>
> Sections that ARE still valid: game-specific rules, undefined ALL-CAPS, Violation clauses,
> scored-when evidence, scoring/timing mentions, section map, tripwires.
>
> To get a real diff, point the baseline at a different season:
> `BASELINE=manuals/archive/frc/2025_REEFSCAPE_GameManual.pdf bash tools/RUN-KICKOFF.sh <manual.pdf> <label>`
EOB
)"
  printf '%s\n\n%s\n' "$BANNER" "$(cat "$PACK")" > "$PACK.tmp" && mv -f "$PACK.tmp" "$PACK"
  printf '   \033[33m*** SELF-DIFF DETECTED ***\033[0m manual == baseline; all diff sections are empty.\n'
  printf '       Banner prepended to the briefing pack. This is a REHEARSAL, not kickoff.\n'
fi

banner "3. Write schema stubs for the assistant to fill"

cat > "$REVIEW/game_def.json" <<'JSON'
{
  "_comment": "Fill from the manual. Feeds tools/cycle-model.py. Remove every FILL_ME. Keys beginning with _ are notes and are ignored by every tool.",
  "_units": "every *_s field is SECONDS (int); every points field is POINTS (int).",
  "_sourcing": "cycle-model.py prints a CONSTANTS table and flags every value with no declared source as [UNSOURCED] -- the 2026 rehearsal shipped 5 unsourced constants and was graded D for it. To source a value, add a SIBLING key named `<key>_source` -- e.g. `auto_s` is sourced by `auto_s_source`, `threshold` by `threshold_source`. NO LEADING UNDERSCORE: keys starting with _ are notes and the tool cannot read them. An object may also carry one `_source`-free blanket key `source` covering all its values. A top-level `_sources` map does NOT work.",
  "auto_s_source": "FILL_ME e.g. 'manual s5.12 Table 5-4 audio cues'",
  "teleop_s_source": "FILL_ME",
  "endgame_s_source": "FILL_ME",
  "name": "FILL_ME BIOCORE (2027) -- game name as printed on the manual cover",

  "auto_s": "FILL_ME int seconds of AUTO, from the match-timing table",

  "_teleop_s_note": "INCLUSIVE of the endgame window. Put the FULL teleop period here (REBUILT: 140, which CONTAINS the 30 s END GAME). The model computes cycling time as teleop_s minus the chosen fixed action time_s, so subtracting the endgame here too makes every number in the review wrong.",
  "teleop_s": "FILL_ME int seconds of TELEOP, endgame INCLUDED",

  "_endgame_s_note": "INFORMATIONAL ONLY. Printed in the banner, used in no arithmetic anywhere. The real cost of an endgame action is fixed_actions[].time_s. Fill it for the reader; changing it changes no output.",
  "endgame_s": "FILL_ME int seconds of the endgame window",

  "_cycle_actions_note": "ONLY cycle_actions[0] is modelled. Entries 1..n are IGNORED (the tool now prints a SCHEMA WARNING if you supply more). If the game has two repeatable scoring actions of different value, put the DOMINANT one here, run the model once per action, and combine by hand in REVIEW.md section 2.",
  "cycle_actions": [
    {
      "name": "FILL_ME primary repeatable scoring action",
      "points_auto": "FILL_ME int points for ONE unit scored during AUTO",
      "points_teleop": "FILL_ME int points for ONE unit scored during TELEOP",
      "_per_cycle_note": "ROBOT DESIGN ASSUMPTION, not a manual fact. How many units one round trip delivers. Largest single lever on every number downstream. Tag it [INFERENCE] in REVIEW.md and name the source below: last season match video, an archetype in reference/03_ARCHETYPE_CORPUS.md, or an explicit guess.",
      "per_cycle": "FILL_ME how many units one robot trip delivers",
      "per_cycle_source": "FILL_ME where this number came from -- NOTE: no leading underscore, or the tool cannot read it"
    }
  ],

  "_fixed_actions_note": "One-off actions: climbs, endgame tasks, AUTO-only bonuses. phase is exactly one of: auto | teleop | endgame. phase=auto is additive and consumes no teleop time; phase=endgame or teleop costs time_s of cycling. If one act pays differently in AUTO than in TELEOP (REBUILT: TOWER L1 = 15 auto / 10 teleop) the schema CANNOT express it -- split into two rows named ACT (AUTO) and ACT (TELEOP). There is likewise no way to say an action is legal in only one phase; encode that in the name and a _note.",
  "fixed_actions": [
    {
      "name": "FILL_ME endgame or one-off action",
      "points": "FILL_ME int points it pays",
      "_time_s_note": "NO FRC MANUAL STATES A TIME COST FOR ANY ACTION. This is always an estimate. Source it below: measured from last season match video, or the entry in reference/bom/06_MECHANISM_CATALOG.md, or an explicit guess. The entire break-even table in REVIEW.md section 2 is a function of these numbers.",
      "time_s": "FILL_ME seconds it consumes",
      "_time_s_source": "FILL_ME where this number came from",
      "phase": "endgame"
    }
  ],

  "_rp_note": "basis tells the model how to count the RP and REPLACES the old hard-coded game-noun match. Set basis to cycle when the RP counts units of cycle_actions[0], or fixed when it counts a fixed/endgame action such as a climb total. If basis is omitted the tool guesses by matching metric against fixed_actions names -- set it explicitly, do not rely on the guess. threshold is a SINGLE scalar: enter the tier your team actually competes at (district/regional) and put any per-tier escalation in note. NOTHING PARSES note, so if the escalation is strategically decisive you must say so yourself in REVIEW.md section 2.",
  "rp": [
    { "name": "FILL_ME bonus RP", "metric": "FILL_ME which action counts",
      "basis": "cycle",
      "threshold": "FILL_ME int, at YOUR event tier",
      "note": "note tier escalation if thresholds differ by event tier" }
  ],

  "_known_gaps": "This schema CANNOT express: a scoring duty cycle (a target that is periodically inactive), a conditional or positional multiplier, or a phase in which points are worth zero. REBUILT HUB active/inactive was unrepresentable and had to be corrected by hand. If BIOCORE has any such mechanic, model it by HAND-DERATING per_cycle (target live 90 s of 140 s -> multiply per_cycle by 0.64) and record the derate and its arithmetic in a _derate key here AND in REVIEW.md section 2."
}
JSON
ok "game_def.json"

cat > "$REVIEW/candidates.yaml" <<'YAML'
# candidates.yaml -- the strategies BIOCORE actually permits.
#
# Enumerate EXHAUSTIVELY before scoring: by scoring action, by field zone, by match phase,
# by alliance role, by RP path, by opponent denial. Include the ones a student never proposes:
# pure defense, pure auto, feeder/support, deliberately-simple-and-flawless.
# See STRATEGY-RANKING-SYSTEM.md section 2 -- its 2.7 checklist is what produces those rows.
#
# Score achievability BY HAND against the anchors in reference/ACHIEVABILITY-RUBRIC.md section 2.
# A1-A13 and V2-V5 are 0-5. V1 is IMPORTED from cycle-model.py -- do not set it. Nothing
# validates that you did not; if you set it, the cycle_model block silently overwrites it.
#
# EVERY ROW MUST CARRY corpus_archetype. reference/03_ARCHETYPE_CORPUS.md scores 30 archetypes
# against five real seasons. A row that contradicts its archetype verdict is not automatically
# wrong, but it must be defended by name in REVIEW.md section 3.

team_overrides:
  outsourced_2d_account: false     # true ONLY once a SendCutSend-class account EXISTS and one
                                   # test order has SHIPPED. Never set it aspirationally.

candidates:
- id: FILL_ME_S1
  name: FILL_ME
  corpus_archetype: FILL_ME        # e.g. "R2 -- highest-value small-team play in REBUILT".
                                   # The closest row in reference/03_ARCHETYPE_CORPUS.md
                                   # section 2, plus its verdict in one clause. "none" is a
                                   # legal answer meaning genuinely novel -- say so out loud.
  achievability: {A1: 0, A2: 0, A3: 0, A4: 0, A5: 0, A6: 0, A7: 0,
                  A8: 0, A9: 0, A10: 0, A11: 0, A12: 0, A13: 0}
  value:         {V2: 0, V3: 0, V4: 0, V5: 0}
  gates_input:
    # mfg_floor -- LEGAL TOKENS, exactly one of:
    #     hand | bandsaw+drill | 3dprint | router | CNC
    # These team_capacity.yaml / bom-builder.py spellings are also accepted and aliased:
    #     hand_tools -> hand       bandsaw_drillpress -> bandsaw+drill
    #     router_cnc -> router     outsourced -> router        mill_lathe -> CNC
    # ANY OTHER STRING IS A HARD SCHEMA ERROR; score-strategy.py refuses to run and says so.
    # It used to fire gate G1 instead, silently deleting the row from the ranking.
    mfg_floor: bandsaw+drill
    # new_workstreams -- streams ON TOP OF the three mandatory ones (drivetrain, electrical,
    # software), per rubric A2 and gate G2. A KOP chassis plus one intake is 1, NOT 4.
    # bom-builder.py prints an "N effective" workstream count on a DIFFERENT convention: it
    # counts the mandatory three as well, and absorbs mechanisms under roughly 12 h / 0 motors.
    # The two numbers are expected to differ by about three. Never copy one into the other.
    new_workstreams: 1
    # novel_mechanisms -- mechanisms this team has never built before. bom-builder.py DERIVES
    # its own count from the mechanism list. If they disagree, the builder count is the one to
    # trust and this field is the one to fix; reconcile them before writing REVIEW.md.
    novel_mechanisms: 1
    marginal_cost_high_usd: 0      # high end of the cost range in USD, above the KOP baseline
    mechanism_hours: 0             # build hours for the mechanisms only, not the whole robot
    mentor_minutes_per_week: 0     # mentor UNBLOCK time this design demands, minutes/week
    # drive_practice_sensitivity -- LEGAL TOKENS, exactly one of: low | med | high | extreme
    # Only "extreme" fires anything (soft gate G6). Rubric A4 maps low:5 med:3 high:2 extreme:0.
    drive_practice_sensitivity: med
  cycle_model:
    # game -- path to game_def.json, resolved RELATIVE TO THE DIRECTORY THE COMMAND RUNS FROM
    # (the repo root, for the autorun). The bare filename "game_def.json" works because phase 2
    # passes the review dir explicitly. When in doubt give the full path.
    game: FILL_ME_path_to_game_def.json
    # cycle -- seconds for one full scoring round trip. For a NON-SCORING candidate (pure
    # defense, feeder, endgame-only) there is no cycle: use 999 as the sentinel and hand-score
    # V1 to 0 or 1. Never use a small number just so it computes.
    cycle: 10
    auto_scored: 0                 # units this design scores during AUTO
    # median_alliance_score -- DO NOT GUESS. Derive it from the TBA CSVs already on disk:
    #   research/predictive_tba/tba_matches_*.csv   (2026 median alliance score = 147)
    # It feeds V1 and therefore moves every value score in the ranking. A guessed 120 against
    # a real 147 was a graded error in the 2026-08 rehearsal.
    median_alliance_score: 0
YAML
ok "candidates.yaml"

cat > "$REVIEW/bom_config.yaml" <<'YAML'
# bom_config.yaml -- the mechanisms the chosen strategy implies.
# Valid ids:  python tools/bom-builder.py --list      (they are deliberately not copied here;
#                                                      run it, the catalog moves)
# Start from reference/bom/examples/simple.yaml and add only what the game forces.
#
# WORKSTREAM ABSORPTION: the builder decides on its own that a mechanism with 0 motors and
# roughly <=12 build hours is not a separate workstream. That heuristic is the difference
# between FAILS 3 GATES and ALL GATES PASS, and it is invisible until you read the output.
# Read the workstream line in results/bom.md and sanity-check it before believing a verdict.
#
# GEOMETRIC FEASIBILITY -- the target: block below is the whole point.
# The builder runs a GEOMETRY (REACH) gate: at least one mechanism's delivery envelope in
# reference/bom/mechanism_catalog.yaml must clear the aperture you declare, or the run FAILS
# and names the shortfall in inches. LEAVE target: OUT AND YOU GET A LOUD WARNING INSTEAD OF A
# CHECK -- that silence is what costed, gated, scheduled and ordered parts for a hopper dump
# (30 in rim) aimed at a 72 in HUB lip in the 2026 rehearsal (review/REHEARSAL_GRADE.md sec 5).
#
# reference/03_ARCHETYPE_CORPUS.md section 2.4 item 4: "the scoring lip is the mechanism gate.
# Any archetype delivering the game piece must clear it. In BIOCORE, FIND THIS NUMBER FIRST."
# Find it in the manual (2026 REBUILT: sec 5.4, 72 in) BEFORE you choose a mechanism, not after.
# Regression pair: reference/bom/examples/geom_fail_2026_hopper.yaml (FAILS by 42 in) and
#                  reference/bom/examples/geom_pass_2026_shooter.yaml (clears by 36 in).
name: "FILL_ME chosen design"
notes: >
  FILL_ME one paragraph: the design thesis, which workstream is the novel one, and
  HOW THIS DESIGN PHYSICALLY REACHES THE SCORING TARGET -- state the aperture height from
  the manual and the delivery height of the mechanism. The GEOMETRY gate checks the numbers;
  this sentence is where you show you understand them.
target:
  # FILL_ME from the manual -- find this number FIRST, before choosing mechanisms.
  name: "FILL_ME scoring opening, e.g. HUB upper opening"
  aperture_height_in: 0        # height of the scoring opening off the carpet, INCHES
  aperture_range_in: 0         # horizontal stand-off required; 0 = may be approached in contact
  source: "FILL_ME manual sec X.Y"
mechanisms:
  - kop_chassis
  - bumpers_frame
  - baseline_electrical_package
YAML
ok "bom_config.yaml"

banner "PHASE 1 COMPLETE"
cat <<EOF
   review dir : $REVIEW
   briefing   : $REVIEW/BRIEFING_PACK.md
   stubs      : game_def.json · candidates.yaml · bom_config.yaml

   NEXT (the assistant does this automatically -- see CLAUDE.md):
     1. Read BRIEFING_PACK.md and the manual.
     2. Fill the three stub files (no FILL_ME may remain).
     3. bash tools/RUN-KICKOFF.sh --phase2 "$REVIEW"
     4. Write the review from the results.
EOF
