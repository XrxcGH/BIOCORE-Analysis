#!/usr/bin/env bash
# probe-2027-manual.sh -- find the BIOCORE manual the moment it goes live.
#
# WHY THIS EXISTS
#   The FRC CDN (firstfrc.blob.core.windows.net) has PUBLIC CONTAINER LISTING DISABLED.
#   Verified 2026-08-22:
#       GET /frc2027?restype=container&comp=list -> 404 ResourceNotFound
#       GET /frc2026?restype=container&comp=list -> 404   (yet /frc2026/Manual/2026GameManual.pdf = 200)
#   So you cannot enumerate the container. You must guess the filename. FIRST has changed
#   the manual filename shape several times (2022/2023 used "<YEAR>FRCGameManual.pdf",
#   2024-2026 used "<YEAR>GameManual.pdf"), so guess ALL known shapes, not just last year's.
#
# USAGE
#   bash tools/probe-2027-manual.sh              # probe once, print what is live
#   bash tools/probe-2027-manual.sh --download   # also download anything that resolves
#   YEAR=2027 bash tools/probe-2027-manual.sh    # override season
#
# On kickoff morning (2027-01-09, 12:00 ET) run with --download.
# Downloads land in manuals/2026-27_BIOCORE/, except Team Updates, which go to
# manuals/archive/supplemental/<YEAR>_TeamUpdates/ where tools/teamupdate-diff.py reads them.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "${1:-}" in -h|--help) sed -n '2,21p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
YEAR="${YEAR:-2027}"
B="https://firstfrc.blob.core.windows.net/frc${YEAR}"
DL=0; [ "${1:-}" = "--download" ] && DL=1
OUT="$ROOT/manuals/2026-27_BIOCORE"
TU_OUT="$ROOT/manuals/archive/supplemental/${YEAR}_TeamUpdates"
mkdir -p "$OUT"

hit=0
probe() { # probe <url> <savename> [outdir]
  local u="$1" n="$2" d="${3:-$OUT}" code
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 20 "$u" 2>/dev/null)
  if [ "$code" = "200" ]; then
    hit=$((hit+1))
    local size; size=$(curl -sI -L --max-time 20 "$u" 2>/dev/null | tr -d '\r' \
                       | awk 'tolower($1)=="content-length:"{print $2}' | tail -1)
    printf '  \033[32mLIVE\033[0m  %-10s  %s\n' "$([ -n "${size:-}" ] && echo "$((size/1024))KB" || echo "?")" "$u"
    if [ "$DL" = "1" ]; then
      mkdir -p "$d"
      curl -sL --max-time 300 -o "$d/$n" "$u" && echo "        -> saved $d/$n"
    fi
  else
    printf '  ----  %-10s  %s\n' "$code" "$u"
  fi
}

echo "Probing FRC ${YEAR} CDN  ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
echo
echo "== Game manual (all known filename shapes) =="
probe "$B/Manual/${YEAR}GameManual.pdf"            "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/${YEAR}FRCGameManual.pdf"         "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/${YEAR}GameSeasonManual.pdf"      "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/${YEAR}FRCGameSeasonManual.pdf"   "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/GameManual.pdf"                   "BIOCORE_GameManual_V1.pdf"
# [AUDIT 2026-09-04] reconciled with the Trellis suite's tools/manual-probe.mjs, which sweeps the
# same CDN and shared only 7 of the 42 shapes the two tried between them. These four came from
# there or from this project's own fetch logs, which recorded the URL every archived file came from.
probe "$B/Manual/${YEAR}_GameManual.pdf"           "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/${YEAR}GameManual_Rev1.pdf"       "BIOCORE_GameManual_V1.pdf"
probe "$B/Manual/HTML/${YEAR}GameManual.htm"       "BIOCORE_GameManual_V1.htm"   # observed 2026
probe "$B/manuals/${YEAR}GameManual.pdf"           "BIOCORE_GameManual_V1.pdf"

echo
echo "== Team Updates =="
# NAMING TRAP (verified 2026-08-22 against the live CDN):
#   2026 moved to a GAME-NAME prefix. .../frc2026/Manual/TeamUpdates/TeamUpdate01.pdf -> 404,
#   .../REBUILT_TeamUpdate01.pdf -> 200, while frc2025/.../TeamUpdate01.pdf still -> 200.
#   TU00 did NOT get the game prefix: it is .../frc2026/Manual/TeamUpdates/2026TeamUpdate00.pdf.
#   So probe all three shapes. Combined PDF has had 3 different names in 3 seasons.
GAME="${GAME:-BIOCORE}"
probe "$B/Manual/TeamUpdates/${YEAR}TeamUpdate00.pdf"       "TeamUpdate00.pdf" "$TU_OUT"  # 2026 shape for #00
probe "$B/Manual/TeamUpdates/TeamUpdate00.pdf"              "TeamUpdate00.pdf" "$TU_OUT"  # 2019-2025 shape
for n in 01 02 03; do
  probe "$B/Manual/TeamUpdates/${GAME}_TeamUpdate${n}.pdf"  "TeamUpdate${n}.pdf" "$TU_OUT" # 2026 shape (primary)
  probe "$B/Manual/TeamUpdates/TeamUpdate${n}.pdf"          "TeamUpdate${n}.pdf" "$TU_OUT" # 2019-2025 fallback
done
probe "$B/Manual/TeamUpdates/${GAME}_TeamUpdate-Combined.pdf" "TeamUpdate-Combined.pdf" "$TU_OUT"
probe "$B/Manual/TeamUpdates/TeamUpdate-Combined.pdf"         "TeamUpdate-Combined.pdf" "$TU_OUT"
probe "$B/Manual/TeamUpdates/TeamUpdates-combined.pdf"        "TeamUpdate-Combined.pdf" "$TU_OUT"

echo
echo "== Field / inspection / kit =="
# [AUDIT 2026-09-04] 2026 moved these to kebab case and this script was still probing the 2024/2025
# shapes only. The three marked "observed 2026" are the ones that actually served files that season,
# read off this project's own logs/fetch_*.log. Ordered most likely first.
probe "$B/FieldAssets/${YEAR}-field-dimension-dwgs.pdf" "FieldDrawings.pdf"        # observed 2026
probe "$B/FieldAssets/field-manual.pdf"                 "FieldManual.pdf"          # observed 2026
probe "$B/FieldAssets/${YEAR}FieldDrawings.pdf"        "FieldDrawings.pdf"
probe "$B/FieldAssets/${YEAR}LayoutMarkingDiagram.pdf" "LayoutAndMarking.pdf"
probe "$B/FieldAssets/${YEAR}FieldDrawings-Evergreen.pdf"     "FieldDrawings_Evergreen.pdf"
probe "$B/FieldAssets/${YEAR}FieldDrawings-${GAME}Specific.pdf" "FieldDrawings_GameSpecific.pdf"
probe "$B/FieldAssets/${YEAR}FieldDrawings-FieldLayoutAndMarking.pdf" "LayoutAndMarking.pdf"
probe "$B/FieldAssets/LayoutandMarking.pdf"            "LayoutAndMarking.pdf"
probe "$B/FieldAssets/TeamVersionLayoutMarking.pdf"    "TeamLayoutMarking.pdf"
probe "$B/Manual/${YEAR}FRCInspectionChecklist.pdf"    "InspectionChecklist.pdf"
probe "$B/Manual/${YEAR}-inspection-checklist.pdf"     "InspectionChecklist.pdf"
probe "$B/Manual/${YEAR}InspectionChecklist.pdf"       "InspectionChecklist.pdf"
probe "$B/Manual/TeamResources/${YEAR}InspectionChecklist.pdf" "InspectionChecklist.pdf"
probe "$B/Manual/${YEAR}InspectionChecklist.xlsx"      "InspectionChecklist.xlsx"
probe "$B/FieldAssets/${YEAR}-apriltag-images-user-guide.pdf" "AprilTagGuide.pdf"  # observed 2026
probe "$B/FieldAssets/Apriltag_Images_and_User_Guide.pdf"     "AprilTagGuide.pdf"
probe "$B/FieldAssets/${YEAR}FieldAprilTagLayout.json"       "AprilTagLayout.json"
probe "$B/AprilTags/${YEAR}AprilTagLayout.pdf"         "AprilTagLayout.pdf"

echo
if [ "$hit" -eq 0 ]; then
  echo "Nothing live yet for frc${YEAR}. (Kickoff: 2027-01-09 12:00 ET.)"
  echo "Container listing is disabled server-side, so absence here is not proof of absence —"
  echo "if kickoff has passed, check https://www.firstinspires.org/robotics/frc/game-and-season"
  echo "for the real filename and add its shape to this script."
else
  echo "$hit live URL(s). Re-run with --download to fetch."
  echo "Then: bash tools/ingest-manual.sh \"$OUT/BIOCORE_GameManual_V1.pdf\" V1"
fi
