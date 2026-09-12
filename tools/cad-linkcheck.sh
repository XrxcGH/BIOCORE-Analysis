#!/usr/bin/env bash
# cad-linkcheck.sh -- verify every CAD/manufacturing/sourcing URL cited in
# reference/team-ops/02_design_cad_manufacturing.md still resolves.
#
# Usage:  bash tools/cad-linkcheck.sh            # check the built-in list
#         bash tools/cad-linkcheck.sh --md       # markdown table output
#
# Exit code 0 always (a 403 from a bot-blocking vendor is not a broken link).
# READ THE OUTPUT. 404 or 000 on a link means the doc must be corrected, not the link retried.
# Last run: 2026-08-22.

set -u
MD=0; [ "${1:-}" = "--md" ] && MD=1

URLS=(
  # --- CAD platform + FIRST licensing (doc sec 1.3) ---
  "https://www.onshape.com/en/education/"
  "https://www.onshape.com/en/education/sign-up"
  "https://www.onshape.com/en/education/first-robotics"
  "https://www.onshape.com/en/education/cam-for-first"
  "https://www.onshape.com/en/blog/how-to-onboard-your-first-robotics-team"
  "https://www.ptc.com/en/education/first"
  "https://cad.onshape.com/"
  "https://cad.onshape.com/appstore"
  # --- part libraries (doc sec 2.2) ---
  "https://appstore.onshape.com/"
  "https://frcdesign.org/"
  "https://www.chiefdelphi.com/t/pic-introducing-mkcad-the-onshape-frc-parts-library/161295"
  "https://www.firstinspires.org/resources/library/frc/kit-of-parts"
  "https://www.revrobotics.com/"
  "https://www.wcproducts.com/"
  "https://docs.wcproducts.com/"
  "https://andymark.com/"
  "https://www.thethriftybot.com/"
  "https://www.swervedrivespecialties.com/"
  "https://store.ctr-electronics.com/"
  "https://sendcutsend.com/"
  "https://www.xometry.com/"
  "https://www.mcmaster.com/"
  "https://www.grainger.com/"
  "https://www.chiefdelphi.com/"
)

[ $MD -eq 1 ] && printf '| Status | URL |\n|---|---|\n'
for u in "${URLS[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 -A "Mozilla/5.0" "$u")
  case "$code" in
    200|30*) note="OK" ;;
    403|406) note="BOT-BLOCKED (not proof of absence; open in a browser)" ;;
    000)     note="NO RESPONSE (DNS/TLS/timeout)" ;;
    *)       note="** FIX THE DOC **" ;;
  esac
  if [ $MD -eq 1 ]; then printf '| %s %s | %s |\n' "$code" "$note" "$u"
  else printf '%3s  %-52s %s\n' "$code" "$note" "$u"; fi
done
exit 0
