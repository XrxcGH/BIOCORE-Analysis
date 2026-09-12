#!/usr/bin/env bash
# fetch-frc-manuals.sh — sweep candidate URLs for every FRC game manual + supplements.
# Writes into manuals/archive/frc and manuals/archive/supplemental; logs to logs/fetch.log
#
#   bash tools/fetch-frc-manuals.sh            download whatever is not already on disk
#   FETCH_LOG=<file> bash tools/fetch-frc-manuals.sh
#                                              log somewhere else (the default log is
#                                              truncated on every run; tools/rebuild-corpus.sh
#                                              sends it to manuals/fetch.log instead)
#
# A file already on disk is skipped. Delete it to download it again.
# Every URL below was either swept by this script or recorded in logs/fetch*.log as the
# source of the archived copy. The 2008-2016 Q&A archives and the 2016 manual are no longer
# on FIRST's servers, so those URLs are Internet Archive captures of firstinspires.org.
case "${1:-}" in -h|--help) sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="${FETCH_LOG:-$ROOT/logs/fetch.log}"; mkdir -p "$(dirname "$LOG")"; : > "$LOG"
B="https://firstfrc.blob.core.windows.net"

try() { # try <outdir> <outname> <url>
  local d="$1" n="$2" u="$3"
  [ -s "$d/$n" ] && { echo "SKIP  $n"; return 0; }
  local code
  code=$(curl -sL --max-time 300 -o "$d/$n.part" -w "%{http_code}" "$u" 2>/dev/null)
  local sz; sz=$(stat -c%s "$d/$n.part" 2>/dev/null || echo 0)
  if [ "$code" = "200" ] && [ "$sz" -gt 40000 ] && head -c4 "$d/$n.part" | grep -q '%PDF'; then
    mv -f "$d/$n.part" "$d/$n"; echo "OK    $n  ($((sz/1024)) KB)  $u" | tee -a "$LOG"
  else
    rm -f "$d/$n.part"; echo "miss  [$code ${sz}b] $u" >> "$LOG"; return 1
  fi
}

FRC="$ROOT/manuals/archive/frc"; SUP="$ROOT/manuals/archive/supplemental"
mkdir -p "$FRC" "$SUP"

echo "=== Core game manuals ==="
try "$FRC" "2026_REBUILT_GameManual.pdf"        "$B/frc2026/Manual/2026GameManual.pdf"
try "$FRC" "2025_REEFSCAPE_GameManual.pdf"      "$B/frc2025/Manual/2025GameManual.pdf"
try "$FRC" "2024_CRESCENDO_GameManual.pdf"      "$B/frc2024/Manual/2024GameManual.pdf"
try "$FRC" "2023_CHARGEDUP_GameManual.pdf"      "$B/frc2023/Manual/2023FRCGameManual.pdf"
try "$FRC" "2022_RAPIDREACT_GameManual.pdf"     "$B/frc2022/Manual/2022FRCGameManual.pdf"
for u in "$B/frc2021/Manual/2021GameManual.pdf" "$B/frc2021/Manual/2021FRCGameManual.pdf"; do
  try "$FRC" "2021_INFINITERECHARGE_GameManual.pdf" "$u" && break
done
try "$FRC" "2021_INFINITERECHARGE_AtHomeChallengesManual.pdf" "$B/frc2021/Manual/2021AtHomeChallengesManual.pdf" || true
for u in "$B/frc2020/Manual/2020FRCGameSeasonManual.pdf" "$B/frc2020/Manual/2020GameManual.pdf"; do
  try "$FRC" "2020_INFINITERECHARGE_GameManual.pdf" "$u" && break; done
for u in "$B/frc2019/Manual/2019FRCGameSeasonManual.pdf" "$B/frc2019/Manual/2019GameManual.pdf"; do
  try "$FRC" "2019_DESTINATIONDEEPSPACE_GameManual.pdf" "$u" && break; done
for u in "$B/frc2018/Manual/2018FRCGameSeasonManual.pdf" "$B/frc2018/Manual/2018GameManual.pdf"; do
  try "$FRC" "2018_POWERUP_GameManual.pdf" "$u" && break; done
for u in "$B/frc2017/Manual/2017FRCGameSeasonManual.pdf" "$B/frc2017/Manual/2017GameManual.pdf" \
         "$B/frc2017/Manual/2017FRCGameManual.pdf"; do
  try "$FRC" "2017_STEAMWORKS_GameManual.pdf" "$u" && break; done
FI="https://www.firstinspires.org/sites/default/files/uploads/resource_library/frc/game-and-season-info"
WB="https://web.archive.org/web"
try "$FRC" "2016_STRONGHOLD_GameManual.pdf" \
    "$WB/20160109215209id_/http://www.firstinspires.org/sites/default/files/uploads/resource_library/frc/game-and-season-info/competition-manual/2016/frc-2016-gamemanual-enc.pdf" || true
try "$FRC" "2015_RECYCLERUSH_GameManual.pdf" "$FI/archive/2015/GameManual20150407.pdf" || \
try "$FRC" "2015_RECYCLERUSH_GameManual.pdf" "$B/frcarchive/2015/2015-game-manual.pdf" || true

echo "=== Q&A archives (research/rule_inventories/_text/qa_<year>.txt is built from these) ==="
try "$FRC" "2026_REBUILT_QandA.pdf"          "$B/frc2026/FRC2026REBUILT-QandAExport.pdf" || true
try "$FRC" "2025_REEFSCAPE_QandA.pdf"        "$B/frc2025/FRC2025REEFSCAPE-QandAExport.pdf" || true
try "$FRC" "2024_CRESCENDO_QandA.pdf"        "$B/frc2024/FRC2024CRESCENDO-QandAExport.pdf" || true
try "$FRC" "2023_CHARGEDUP_QandA.pdf"        "$B/frc2023/FRC2023CHARGEDUP-QandAExport.pdf" || true
try "$FRC" "2022_RAPIDREACT_QandA.pdf"       "$B/frc2022/FRC2022RapidReact-QandAExport.pdf" || true
try "$FRC" "2021_INFINITERECHARGE_QandA.pdf" "$B/frc2021/Manual/FRCQA-2021InfiniteRecharge.pdf" || true
try "$FRC" "2020_INFINITERECHARGE_QandA.pdf" "$B/frc2020/2020_QA_Full_Archive.pdf" || true
try "$FRC" "2019_DESTINATIONDEEPSPACE_QandA.pdf" "$B/frc2019/2019_QA_Full_Archive.pdf" || true
try "$FRC" "2018_POWERUP_QandA.pdf"          "$B/frc2018/2018_QA_Full_Archive.pdf" || true
try "$FRC" "2017_STEAMWORKS_QandA.pdf"       "$B/frc2017/2017_QA_Full_Archive.pdf" || true
try "$FRC" "2016_STRONGHOLD_QandA.pdf"       "$WB/20171128192729id_/$FI/archive/2016/frcqnada-2016-04-18.pdf" || true
try "$FRC" "2015_RECYCLERUSH_QandA.pdf"      "$WB/20151227171221id_/$FI/archive/2015/FRCQandA_2015-04-20_09_24_41.pdf" || true
try "$FRC" "2014_AERIALASSIST_QandA.pdf"     "$WB/20151227171202id_/$FI/archive/2014/2014-frc-qanda.pdf" || true
try "$FRC" "2013_ULTIMATEASCENT_QandA.pdf"   "$WB/20151227171148id_/$FI/archive/2013/2013-q-and-a.pdf" || true
try "$FRC" "2012_REBOUNDRUMBLE_QandA.pdf"    "$WB/20151227170716id_/$FI/archive/2012/2012-frc-qanda.pdf" || true
try "$FRC" "2010_BREAKAWAY_QandA.pdf"        "$WB/20171128192743id_/$FI/archive/2010/2010-breakaway-q-and-a.pdf" || true
try "$FRC" "2008_FIRSTOVERDRIVE_QandA.pdf"   "$WB/20171128192714id_/$FI/archive/2008/2008-overdrive-q-and-a.pdf" || true

echo "=== Team Updates (2022-2026) ==="
game_of() { case "$1" in 2022) echo RAPIDREACT;; 2023) echo CHARGEDUP;; 2024) echo CRESCENDO;;
                         2025) echo REEFSCAPE;; 2026) echo REBUILT;; esac; }
for y in 2022 2023 2024 2025 2026; do
  mkdir -p "$SUP/${y}_TeamUpdates"
  g="$(game_of "$y")"
  for n in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25; do
    # 2026 moved to <GAME>_TeamUpdateNN.pdf, except TU00, which is <YEAR>TeamUpdate00.pdf.
    try "$SUP/${y}_TeamUpdates" "TeamUpdate${n}.pdf" "$B/frc${y}/Manual/TeamUpdates/TeamUpdate${n}.pdf" && continue
    try "$SUP/${y}_TeamUpdates" "TeamUpdate${n}.pdf" "$B/frc${y}/Manual/TeamUpdates/${g}_TeamUpdate${n}.pdf" && continue
    [ "$n" = "00" ] && try "$SUP/${y}_TeamUpdates" "TeamUpdate${n}.pdf" "$B/frc${y}/Manual/TeamUpdates/${y}TeamUpdate${n}.pdf"
    true
  done
done

echo "=== Supplemental (inspection, field, kit) ==="
for y in 2024 2025 2026; do
  try "$SUP" "${y}_InspectionChecklist.pdf" "$B/frc${y}/Manual/${y}FRCInspectionChecklist.pdf" || \
  try "$SUP" "${y}_InspectionChecklist.pdf" "$B/frc${y}/Manual/${y}InspectionChecklist.pdf" || true
  try "$SUP" "${y}_FieldDrawings.pdf" "$B/frc${y}/FieldAssets/${y}FieldDrawings.pdf" || true
  try "$SUP" "${y}_ArenaLayoutAndMarking.pdf" "$B/frc${y}/FieldAssets/LayoutandMarking.pdf" || true
done
echo "=== DONE ==="; grep -c '^OK' "$LOG" 2>/dev/null || true
