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
CLI=${KICAD_CLI:-kicad-cli}
# FreeRouting is not deterministic: a cell is re-routed (up to 3 tries) until KiCad's DRC
# reports no unconnected item.  check_iso_cells.py is the gate; this loop only saves reruns.
unconnected() {
  $CLI pcb drc --format json -o "$WORK/u.json" "$HERE/../cells/$1/$1.kicad_pcb" >/dev/null 2>&1
  python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))['unconnected_items']))" "$WORK/u.json"
}
for cell in ${*:-can rs485 eth_rmii2 eth_usb1 m1553}; do
 for try in 1 2 3; do
  $PY "$HERE/gen_iso_cells.py" place "$cell" 2>&1 | grep -v 'SetWidth' || true
  D="$HERE/../cells/$cell"
  cp "$D/route.dsn" "$WORK/$cell.dsn"
  timeout 600 java -jar "$JAR" --gui.enabled=false --usage_and_diagnostic_data.disable_analytics=true -de "$WORK/$cell.dsn" -do "$WORK/$cell.ses" -mp 100 \
    > "$WORK/$cell.log" 2>&1 || true
  grep -E 'unrouted' "$WORK/$cell.log" | tail -1 || true
  test -s "$WORK/$cell.ses" || { echo "$cell: no session"; exit 1; }
  $PY "$HERE/gen_iso_cells.py" finish "$cell" "$WORK/$cell.ses" 2>&1 | grep -v 'SetWidth' || true
  u=$(unconnected "$cell"); echo "$cell try $try: unconnected $u"
  [ "$u" = 0 ] && break
 done
done
