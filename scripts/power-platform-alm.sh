#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOLUTION_SRC="$ROOT/power-platform/solution/src"
OUT_DIR="$ROOT/dist/power-platform"
SOLUTION_NAME="mchs_alm_orchestration"

usage() {
  cat <<USAGE
Usage: $0 <validate|pack-unmanaged|pack-managed|checker|import-managed>

validate        Run deterministic local static validation.
pack-unmanaged  Pack unmanaged solution zip with pac; requires pac.
pack-managed    Pack managed solution zip with pac; requires pac.
checker         Run solution checker; requires pac auth and target environment.
import-managed  Import managed zip; requires pac auth and target environment.
USAGE
}

require_pac() { command -v pac >/dev/null 2>&1 || { echo "pac is required" >&2; exit 1; }; }

case "${1:-}" in
  validate)
    python3 "$ROOT/scripts/validate_power_platform_static.py"
    ;;
  pack-unmanaged)
    require_pac
    mkdir -p "$OUT_DIR"
    pac solution pack --folder "$SOLUTION_SRC" --zipfile "$OUT_DIR/${SOLUTION_NAME}_unmanaged.zip" --packagetype Unmanaged
    test -s "$OUT_DIR/${SOLUTION_NAME}_unmanaged.zip"
    ;;
  pack-managed)
    require_pac
    mkdir -p "$OUT_DIR"
    managed_src="$(mktemp -d)"
    cp -R "$SOLUTION_SRC"/. "$managed_src"/
    python3 -c 'from pathlib import Path; import sys; p=Path(sys.argv[1]); s=p.read_text(); p.write_text(s.replace("<Managed>0</Managed>", "<Managed>1</Managed>"))' "$managed_src/Other/Solution.xml"
    pac solution pack --folder "$managed_src" --zipfile "$OUT_DIR/${SOLUTION_NAME}_managed.zip" --packagetype Managed
    test -s "$OUT_DIR/${SOLUTION_NAME}_managed.zip"
    ;;
  checker)
    require_pac
    pac solution check --path "$OUT_DIR/${SOLUTION_NAME}_managed.zip" --outputDirectory "$OUT_DIR/checker" --geo Australia
    ;;
  import-managed)
    require_pac
    pac solution import --path "$OUT_DIR/${SOLUTION_NAME}_managed.zip" --publish-changes
    ;;
  *) usage; exit 2 ;;
esac
