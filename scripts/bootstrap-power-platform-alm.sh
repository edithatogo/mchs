#!/usr/bin/env bash
set -euo pipefail

readonly MIN_PAC_VERSION="1.35.0"
readonly MIN_AZ_VERSION="2.70.0"
readonly PAC_DOTNET_TOOL="microsoft.powerapps.cli.tool"
readonly DOTNET_TOOLS_PATH="${HOME}/.dotnet/tools"

INSTALL_MISSING=0
UPGRADE_TO_MINIMUM=0
CHECK_AUTH=0

PAC_HELP_CHECKS=(
  "pac --help"
  "pac auth --help"
  "pac org --help"
  "pac solution --help"
  "pac solution pack --help"
  "pac solution unpack --help"
  "pac solution import --help"
  "pac solution checker --help"
  "pac solution checker run --help"
  "pac pipeline --help"
)

AZ_HELP_CHECKS=(
  "az version"
  "az account --help"
)

log() {
  printf '[bootstrap] %s\n' "$1"
}

warn() {
  printf '[bootstrap][WARN] %s\n' "$1" >&2
}

fail() {
  printf '[bootstrap][ERROR] %s\n' "$1" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage: ./scripts/bootstrap-power-platform-alm.sh [options]

Verification-only by default. No installs or upgrades occur unless explicitly requested.

Options:
  --install-missing   Install missing supported tools when safe.
  --upgrade           Upgrade supported tools that are below the minimum version.
  --check-auth        Report current az/pac auth state without creating credentials.
  --help              Show this help text.

Minimum versions:
  pac >= 1.35.0
  az  >= 2.70.0

This track explicitly rejects pacx. If pacx is on PATH, the script prints guidance
but does not use it.
EOF
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

version_lt() {
  local lhs="$1"
  local rhs="$2"
  local ordered

  ordered="$(printf '%s\n%s\n' "$lhs" "$rhs" | sort -V | head -n 1)"
  [ "$ordered" = "$lhs" ] && [ "$lhs" != "$rhs" ]
}

extract_version() {
  local output="$1"
  printf '%s\n' "$output" | grep -Eo '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -n 1
}

ensure_dotnet_tools_path() {
  if [[ ":$PATH:" == *":$DOTNET_TOOLS_PATH:"* ]]; then
    return
  fi

  export PATH="$PATH:$DOTNET_TOOLS_PATH"
  log "Added dotnet tools path for this shell: $DOTNET_TOOLS_PATH"
  log "If pac remains undiscoverable in future shells, persist it with:"
  log "  echo 'export PATH=\"\$PATH:$DOTNET_TOOLS_PATH\"' >> ~/.zshrc"
  log "  source ~/.zshrc"
}

discover_command() {
  local name="$1"
  local path_value

  if path_value="$(command -v "$name" 2>/dev/null)"; then
    log "command -v $name => $path_value"
    return 0
  fi

  log "command -v $name => not found"
  return 1
}

read_version() {
  local name="$1"
  local version_command="$2"
  local output
  local version

  if ! output="$(bash -c "$version_command" 2>&1)"; then
    fail "Unable to read $name version with '$version_command'."
  fi

  version="$(extract_version "$output")"
  if [ -z "$version" ]; then
    fail "Could not parse $name version from: $output"
  fi

  printf '%s\n' "$version"
}

require_homebrew() {
  if ! command_exists brew; then
    fail "Homebrew is required for automated Azure CLI install/upgrade on this track. Install Azure CLI manually from Microsoft guidance or install Homebrew first."
  fi
}

install_pac_if_requested() {
  if discover_command pac; then
    return
  fi

  ensure_dotnet_tools_path
  if discover_command pac; then
    return
  fi

  if [ "$INSTALL_MISSING" -ne 1 ]; then
    fail "pac is required. Re-run with --install-missing after ensuring dotnet is installed."
  fi

  if ! command_exists dotnet; then
    fail "dotnet is required to install pac. Install the .NET SDK before re-running with --install-missing."
  fi

  log "Installing pac via dotnet tool install --global $PAC_DOTNET_TOOL"
  dotnet tool install --global "$PAC_DOTNET_TOOL"
  ensure_dotnet_tools_path
  discover_command pac || fail "pac command still unavailable after install."
}

install_az_if_requested() {
  if discover_command az; then
    return
  fi

  if [ "$INSTALL_MISSING" -ne 1 ]; then
    fail "az is required. Install Azure CLI manually or re-run with --install-missing in a Homebrew-enabled environment."
  fi

  require_homebrew
  log "Installing Azure CLI via brew install azure-cli"
  brew install azure-cli
  discover_command az || fail "az command still unavailable after install."
}

upgrade_pac_if_requested() {
  local version

  version="$(read_version pac "pac --version")"
  log "pac version detected: $version"

  if ! version_lt "$version" "$MIN_PAC_VERSION"; then
    return
  fi

  if [ "$UPGRADE_TO_MINIMUM" -ne 1 ]; then
    fail "pac version $version is below minimum $MIN_PAC_VERSION. Re-run with --upgrade after confirming dotnet access."
  fi

  if ! command_exists dotnet; then
    fail "dotnet is required to upgrade pac."
  fi

  log "Upgrading pac via dotnet tool update --global $PAC_DOTNET_TOOL"
  dotnet tool update --global "$PAC_DOTNET_TOOL"
  version="$(read_version pac "pac --version")"
  log "pac version after upgrade: $version"
  version_lt "$version" "$MIN_PAC_VERSION" && fail "pac remains below minimum version $MIN_PAC_VERSION after upgrade."
}

upgrade_az_if_requested() {
  local version

  version="$(read_version az "az version")"
  log "az version detected: $version"

  if ! version_lt "$version" "$MIN_AZ_VERSION"; then
    return
  fi

  if [ "$UPGRADE_TO_MINIMUM" -ne 1 ]; then
    fail "az version $version is below minimum $MIN_AZ_VERSION. Re-run with --upgrade in a Homebrew-enabled environment or upgrade Azure CLI manually."
  fi

  require_homebrew
  log "Upgrading Azure CLI via brew upgrade azure-cli"
  brew upgrade azure-cli
  version="$(read_version az "az version")"
  log "az version after upgrade: $version"
  version_lt "$version" "$MIN_AZ_VERSION" && fail "az remains below minimum version $MIN_AZ_VERSION after upgrade."
}

run_help_smoke_check() {
  local command_to_test="$1"
  local output

  if ! output="$(bash -c "$command_to_test" 2>&1)"; then
    fail "Smoke check failed for '$command_to_test'."
  fi

  if [ -n "$output" ]; then
    log "Smoke check ok: $command_to_test => $(printf '%s\n' "$output" | head -n 1)"
  else
    log "Smoke check ok: $command_to_test"
  fi
}

report_pacx_status() {
  if discover_command pacx; then
    warn "pacx is present on PATH but rejected for this track."
    warn "Use pac for supported ALM commands. Do not substitute pacx in CI, docs, or local recipes."
    return
  fi

  log "pacx is not on PATH. This is expected for the supported toolchain."
}

report_auth_state() {
  if [ "$CHECK_AUTH" -ne 1 ]; then
    return
  fi

  log "Auth state report requested."

  if az account show >/dev/null 2>&1; then
    log "Azure CLI auth: ready (az account show succeeded)."
  else
    warn "Azure CLI auth not ready. Run 'az login' outside this repo and select the correct subscription before solution import/export operations."
  fi

  if pac auth list >/dev/null 2>&1; then
    log "Power Platform CLI auth: ready (pac auth list succeeded)."
  else
    warn "Power Platform CLI auth not ready. Run 'pac auth create' outside this repo and target the required Dataverse environment before solution operations."
  fi
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --install-missing)
        INSTALL_MISSING=1
        ;;
      --upgrade)
        UPGRADE_TO_MINIMUM=1
        ;;
      --check-auth)
        CHECK_AUTH=1
        ;;
      --help)
        usage
        exit 0
        ;;
      *)
        fail "Unknown option: $1"
        ;;
    esac
    shift
  done
}

main() {
  parse_args "$@"

  log "Power Platform ALM bootstrap started."
  log "Mode: install_missing=$INSTALL_MISSING upgrade=$UPGRADE_TO_MINIMUM check_auth=$CHECK_AUTH"
  log "Minimum versions: pac>=$MIN_PAC_VERSION az>=$MIN_AZ_VERSION"
  log "This script never creates or stores credentials."

  ensure_dotnet_tools_path
  report_pacx_status

  install_pac_if_requested
  install_az_if_requested

  upgrade_pac_if_requested
  upgrade_az_if_requested

  discover_command pac || fail "pac remains unavailable after bootstrap."
  discover_command az || fail "az remains unavailable after bootstrap."

  log "Running explicit command matrix smoke checks."
  for command_to_test in "${PAC_HELP_CHECKS[@]}"; do
    run_help_smoke_check "$command_to_test"
  done
  for command_to_test in "${AZ_HELP_CHECKS[@]}"; do
    run_help_smoke_check "$command_to_test"
  done

  report_auth_state

  log "Bootstrap verification complete."
  log "Canonical command: ./scripts/bootstrap-power-platform-alm.sh --check-auth"
}

main "$@"
