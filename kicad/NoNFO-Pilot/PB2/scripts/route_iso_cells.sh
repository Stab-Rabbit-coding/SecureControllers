#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build, route and pour the NoNFO-Pilot-PB2 isolation cells (S37).
# Needs: a KiCad 9.0.2 Python runner (KICAD_PY, default kicad-python3), Java and
# FreeRouting 2.1.0 (FREEROUTING_JAR), and a Serenity-UAV checkout beside this repo for
# the Serenity-Custom footprints.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${KICAD_PY:-kicad-python3}
JAR=${FREEROUTING_JAR:-/opt/freerouting/fr.jar}
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
for cell in ${*:-can rs485 eth_rmii2 eth_usb1 m1553}; do
  $PY "$HERE/gen_iso_cells.py" place "$cell" 2>&1 | grep -v 'SetWidth' || true
  D="$HERE/../cells/$cell"
  cp "$D/route.dsn" "$WORK/$cell.dsn"
  timeout 600 java -jar "$JAR" --gui.enabled=false --usage_and_diagnostic_data.disable_analytics=true -de "$WORK/$cell.dsn" -do "$WORK/$cell.ses" -mp 100 \
    > "$WORK/$cell.log" 2>&1 || true
  grep -E 'unrouted' "$WORK/$cell.log" | tail -1 || true
  test -s "$WORK/$cell.ses" || { echo "$cell: no session"; exit 1; }
  $PY "$HERE/gen_iso_cells.py" finish "$cell" "$WORK/$cell.ses" 2>&1 | grep -v 'SetWidth' || true
done
