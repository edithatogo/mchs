#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GATE="all"

readonly PAC_GATES=(
  "pack|pac solution pack --help"
  "pack|pac solution unpack --help"
  "check|pac solution checker run --help"
  "import|pac solution import --help"
)

usage() {
  cat <<'EOF'
Usage: ./scripts/power-platform-alm-lifecycle-gates.sh [--gate <pack|check|import|all>]

This script performs deterministic ALM gate checks for locally available tooling.
It does not perform authentication or environment writes.

--gate <name>   Run all gates (default) or only pack/check/import.
EOF
}

log() {
  printf '[alm-gates] %s\n' "$1"
}

fail() {
  printf '[alm-gates][ERROR] %s\n' "$1" >&2
  exit 1
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --gate)
        shift
        if [ "$#" -eq 0 ]; then
          fail "--gate requires a value"
        fi
        GATE="$1"
        ;;
      --help)
        usage
        exit 0
        ;;
      *)
        fail "unknown option: $1"
        ;;
    esac
    shift
  done

  case "$GATE" in
    all|pack|check|import)
      ;;
    *)
      fail "invalid gate '$GATE'; expected pack, check, import, or all"
      ;;
  esac
}

run_gate_if_requested() {
  local gate_name="$1"
  local command_to_run="$2"
  local selected_gate="$3"

  if [ "$selected_gate" != "all" ] && [ "$selected_gate" != "$gate_name" ]; then
    return 0
  fi

  if ! command -v pac >/dev/null 2>&1; then
    log "pac not present; skipping ${gate_name} gate. Install pac or run bootstrap to add it."
    return 0
  fi

  log "Running ${gate_name} gate: ${command_to_run}"
  if ! bash -c "$command_to_run" >/tmp/alm-gate-${gate_name}.out 2>&1; then
    cat "/tmp/alm-gate-${gate_name}.out" >&2
    fail "${gate_name} gate command failed: ${command_to_run}"
  fi
  rm -f "/tmp/alm-gate-${gate_name}.out"
}

main() {
  parse_args "$@"
  log "Power Platform ALM lifecycle gate validation started (gate=${GATE})."

  for gate_entry in "${PAC_GATES[@]}"; do
    IFS='|' read -r gate_name command_to_run <<<"$gate_entry"
    run_gate_if_requested "$gate_name" "$command_to_run" "$GATE"
  done

  log "Running contract check validator with deterministic file and workflow checks."
  python3 "$SCRIPT_DIR/validate_power_platform_alm_gates.py"
  log "Power Platform ALM lifecycle gate validation complete."
}

main "$@"
