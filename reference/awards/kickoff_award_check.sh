#!/usr/bin/env bash
# kickoff_award_check.sh -- the Section 0 workflow of 00_AWARD_LIST_VERIFIED.md, as a file.
# Run it directly (or paste the body into a shell opened in reference/awards):
#     bash reference/awards/kickoff_award_check.sh [--offline] [path-to-BIOCORE-manual.pdf]
# Default manual path is the 2026 REBUILT manual, so the script is runnable (and testable)
# TODAY, before BIOCORE exists. Swap in the BIOCORE manual on 2027-01-09.
#   --offline   skip the web fetch in step 1 and diff the snapshots already in _web/
# FIRST's manuals, the _web/ snapshots and awards.yaml are not in the public repository.
# From the repository root, bash tools/rebuild-corpus.sh --fetch downloads the first two.

set -uo pipefail
OFFLINE=0
case "${1:-}" in
  -h|--help) sed -n '2,11p' "${BASH_SOURCE[0]:-$0}" | sed 's/^# \{0,1\}//'; exit 0 ;;
  --offline) OFFLINE=1; shift ;;
esac
A="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
R="$(cd "$A/../.." && pwd)"
M="${1:-$R/manuals/archive/frc/2026_REBUILT_GameManual.pdf}"
MISSING_INPUT=0
cd "$A" || exit 1

echo "=============================================================="
echo " 1. DID FIRST CHANGE ANY AWARD NAME?  (live pages vs baseline)"
echo "=============================================================="
if [ "$OFFLINE" = "1" ]; then
  python award_diff.py
elif python fetch_award_pages.py >/dev/null 2>&1; then
  python award_diff.py
else
  echo "   fetch_award_pages.py failed (offline, or FIRST moved a page): award names NOT checked."
  echo "   Rerun online, or rerun with --offline to diff the snapshots already in _web/."
fi
echo

echo "=============================================================="
echo " 2. NEW AWARD NAMES IN THE MANUAL  (empty == no new awards)"
echo "    manual: $(basename "$M")"
echo "=============================================================="
if [ ! -f "$M" ]; then
  echo "   MISSING: ${M#"$R"/} (not in the public repository; run: bash tools/rebuild-corpus.sh --fetch)"
  MISSING_INPUT=1
elif ! command -v pdftotext >/dev/null 2>&1; then
  echo "   MISSING: pdftotext (install poppler-utils or xpdf); steps 2 and 3 skipped"
  MISSING_INPUT=1
else
  pdftotext -layout "$M" - 2>/dev/null \
    | grep -oE "([A-Z][A-Za-z'\&.-]*[ ]){0,5}Award" \
    | sed 's/[[:space:]]\+/ /g; s/ $//; s/^\(The\|A\.\|An\) //' \
    | awk 'NF>1' | sort -u | grep -vxF -f known_awards_2026.txt
  echo "  (nothing above == manual award vocabulary matches the 2026 baseline)"
fi
echo

echo "=============================================================="
echo " 3. THE AWARD SLATE AT YOUR EVENT  (playoff ceremony breaks)"
echo "=============================================================="
if [ -f "$M" ] && command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout "$M" - 2>/dev/null | grep -oE "awards break:.*|^Awards: .*" | sed 's/^/   /'
else
  echo "   (skipped: see step 2)"
fi
echo

echo "=============================================================="
echo " 4. DEADLINES + YOUR RANKED TARGETS  (from awards.yaml)"
echo "=============================================================="
if [ ! -f awards.yaml ]; then
  echo "   MISSING: reference/awards/awards.yaml (not in the public repository, and no tool produces it; see bash tools/rebuild-corpus.sh --help)"
  MISSING_INPUT=1
else
python - <<'PY'
import datetime, yaml
d = yaml.safe_load(open("awards.yaml", encoding="utf-8"))
today = datetime.date.today()
print("  DEADLINES")
for r in d["deadlines_2027"]:
    label = r.get("award") or r.get("milestone")
    when = r.get("closes") or r.get("date")
    print(f"    [{r['evidence']}] {label:42s} {when}")
print()
print("  RANKED TARGETS for a ~15-student team")
for r in d["small_team_ranked_targets"][:6]:
    print(f"    {r['rank']:2d}. {r['award']}")
    print(f"        {r['why']}")
print()
print("  DO NOT CHASE")
for r in d["effectively_out_of_reach"]:
    print(f"    x  {r['award']} -- {r['why'][:88]}")
print()
print(f"  Days from {today} to BIOCORE kickoff 2027-01-09:",
      (datetime.date(2027, 1, 9) - today).days)
PY
fi

echo
echo "=============================================================="
echo " 5. THE ONE RULE THAT DECIDES YOUR STRATEGY"
echo "=============================================================="
echo '   Judge Manual: "Do not award the same team more than 1 judged'
echo '   award at a single event."  -> pick ONE lane per event, plus one backup.'

echo
echo "=============================================================="
echo " 6. AVAILABILITY INTEGRITY GATE  (added 2026-08-22)"
echo "    No published availability figure may exceed the number of"
echo "    DISTINCT EVENTS at which that EXACT award name was given."
echo "=============================================================="
echo "   Why this gate exists: 00_AWARD_LIST_VERIFIED.md once printed the FIRST"
echo "   Leadership Award as '192 events @ 2.08/event, the highest availability on"
echo "   the board'. That was the award (1 event) summed with its Finalist (71) and"
echo "   DCMP Semi-Finalist (120) tiers: 400 rows / 192 events. A 192x overstatement"
echo "   of a Championship-only award. Never sum an award with its Finalist or"
echo "   Semi-Finalist tiers, and never sum Regional+District+DCMP into one figure."
echo
AVAIL_FAIL=0
for f in "$A/00_AWARD_LIST_VERIFIED.md" \
         "$A/00_AWARD_LIST_EMPIRICAL_2026.md" \
         "$A/AWARD-ALIGNMENT.md" \
         "$A/01_AWARD_WINNING_PATTERNS.md"; do
  [ -f "$f" ] || continue
  if ! python "$R/tools/award_availability.py" --check "$f" | sed 's/^/   /'; then
    AVAIL_FAIL=1
  fi
done
echo
if [ "$AVAIL_FAIL" -ne 0 ]; then
  echo "   *** AVAILABILITY GATE FAILED -- fix the figures above before shipping. ***"
  echo "   Recompute the truth with:  python tools/award_availability.py"
else
  echo "   Availability gate PASSED for all award reference files."
fi

echo
echo "=============================================================="
echo " 7. TOP-10 AVAILABILITY, exact names only (no tier sums)"
echo "=============================================================="
python "$R/tools/award_availability.py" 2>/dev/null | sed -n '4,14p' | sed 's/^/   /'

if [ "$MISSING_INPUT" -ne 0 ]; then
  echo
  echo "   Some inputs were missing (MISSING lines above), so this check is incomplete."
fi
exit $(( AVAIL_FAIL | MISSING_INPUT ))
