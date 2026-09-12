#!/usr/bin/env bash
# recheck_prices.sh -- re-fetch every evidence:C vendor URL in parts_drivetrain.yaml
# and report whether the locked price still appears on the live page.
#
# Usage:   bash recheck_prices.sh [path/to/parts_drivetrain.yaml]
# Output:  price_check_YYYY-MM-DD.tsv  (status, locked_price, found?, url)
# Exit:    0 = every locked price still found on its page
#          1 = at least one price changed or a page failed to load  -> FIX 01_DRIVETRAIN.md
#
# Written 2026-08-22. Companion to reference/bom/01_DRIVETRAIN.md sec 0 step 1.

set -uo pipefail
YAML="${1:-$(dirname "$0")/parts_drivetrain.yaml}"
OUT="price_check_$(date +%F).tsv"
UA='Mozilla/5.0 (compatible; BIOCORE-BOM-recheck/1)'
fail=0

[ -f "$YAML" ] || { echo "no such file: $YAML" >&2; exit 2; }

# Pull (url, unit_usd) pairs. The yaml is hand-written with url: on a line and the
# matching unit_usd: within the next 6 lines of the same block.
pairs=$(awk '
  /^[[:space:]]*url:[[:space:]]*http/ { u=$2; n=0; next }
  u && n<6 {
    n++
    if ($1=="unit_usd:" && $2 != "null") { printf "%s\t%s\n", u, $2; u=""; }
    if ($1=="unit_usd_min:")             { printf "%s\t%s\n", u, $2; u=""; }
  }
' "$YAML" | sort -u)

printf 'status\tlocked\tfound\turl\n' > "$OUT"

while IFS=$'\t' read -r url price; do
  [ -z "${url:-}" ] && continue
  body=$(curl -sL --max-time 25 -A "$UA" "$url" 2>/dev/null)
  code=$?
  if [ $code -ne 0 ] || [ -z "$body" ]; then
    printf 'FETCH_FAIL\t%s\t-\t%s\n' "$price" "$url" | tee -a "$OUT"
    fail=1; continue
  fi
  # match the number with or without a thousands separator
  bare="${price%.00}"
  if printf '%s' "$body" | grep -qF "$price" || printf '%s' "$body" | grep -qF "$bare"; then
    printf 'OK\t%s\tyes\t%s\n' "$price" "$url" >> "$OUT"
  else
    printf 'PRICE_MOVED\t%s\tno\t%s\n' "$price" "$url" | tee -a "$OUT"
    fail=1
  fi
done <<< "$pairs"

echo
echo "wrote $OUT"
awk -F'\t' 'NR>1{c[$1]++} END{for(k in c) printf "  %-12s %d\n", k, c[k]}' "$OUT"

if [ $fail -ne 0 ]; then
  echo
  echo "FAIL: at least one price moved or a page did not load."
  echo "      Update 01_DRIVETRAIN.md and parts_drivetrain.yaml before ordering."
  exit 1
fi
echo "PASS: every locked price still present on its live page."
exit 0
