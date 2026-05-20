#!/usr/bin/env bash
set -euo pipefail

readonly WORKFLOW_NAME="Power Platform Official Actions"
readonly WORKFLOW_FILE=".github/workflows/power-platform-official-actions.yml"
readonly REQUIRED_SECRETS=(
  "POWER_PLATFORM_ENVIRONMENT_URL"
  "POWER_PLATFORM_APPLICATION_ID"
  "POWER_PLATFORM_CLIENT_SECRET"
  "POWER_PLATFORM_TENANT_ID"
)

DISPATCH=0
PRESENT_SECRETS=()

log() {
  printf '[github-live-gate-bootstrap] %s\n' "$1"
}

warn() {
  printf '[github-live-gate-bootstrap][WARN] %s\n' "$1" >&2
}

fail() {
  printf '[github-live-gate-bootstrap][ERROR] %s\n' "$1" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage: ./scripts/bootstrap-power-platform-github-live-gate.sh [--dispatch]

Checks the GitHub repository secrets required by the official Power Platform
live gate, prints exact `gh secret set` commands for any missing secrets, and
dispatches the workflow only after all secrets are present.

Options:
  --dispatch   Run the workflow dispatch after all required secrets exist.
  --help       Show this help text.

This script never sets secrets for you.
EOF
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

parse_repo_metadata() {
  local repo_json

  repo_json="$(gh repo view --json nameWithOwner,defaultBranchRef)"
  REPO_NAME_WITH_OWNER="$(
    printf '%s' "$repo_json" | python3 -c 'import json, sys; print(json.load(sys.stdin)["nameWithOwner"])'
  )"
  DEFAULT_BRANCH="$(
    printf '%s' "$repo_json" | python3 -c '
import json
import sys
data = json.load(sys.stdin)
ref = data.get("defaultBranchRef") or {}
print(ref.get("name") or "master")
'
  )"
}

print_secret_commands() {
  local secret_name="$1"
  local placeholder

  placeholder="$(placeholder_for_secret "$secret_name")"

  printf '  gh secret set %s --repo %s --body %q\n' \
    "$secret_name" \
    "$REPO_NAME_WITH_OWNER" \
    "$placeholder"
}

placeholder_for_secret() {
  case "$1" in
    POWER_PLATFORM_ENVIRONMENT_URL)
      printf '%s' '<dataverse-environment-url>'
      ;;
    POWER_PLATFORM_APPLICATION_ID)
      printf '%s' '<application-client-id>'
      ;;
    POWER_PLATFORM_CLIENT_SECRET)
      printf '%s' '<application-client-secret>'
      ;;
    POWER_PLATFORM_TENANT_ID)
      printf '%s' '<azure-tenant-id>'
      ;;
    *)
      fail "No placeholder defined for secret: $1"
      ;;
  esac
}

collect_present_secrets() {
  local secret_json

  secret_json="$(gh secret list --repo "$REPO_NAME_WITH_OWNER" --json name)"
  while IFS= read -r secret_name; do
    [ -n "$secret_name" ] || continue
    PRESENT_SECRETS+=("$secret_name")
  done < <(
    printf '%s' "$secret_json" | python3 -c '
import json
import sys
for item in json.load(sys.stdin):
    print(item["name"])
'
  )
}

secret_is_present() {
  local needle="$1"
  local candidate

  if [ "${#PRESENT_SECRETS[@]}" -eq 0 ]; then
    return 1
  fi

  for candidate in "${PRESENT_SECRETS[@]}"; do
    [ "$candidate" = "$needle" ] && return 0
  done

  return 1
}

main() {
  local missing=()

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --dispatch)
        DISPATCH=1
        ;;
      --help|-h)
        usage
        return 0
        ;;
      *)
        fail "Unknown argument: $1"
        ;;
    esac
    shift
  done

  command_exists gh || fail "gh is required. Install GitHub CLI and authenticate before running this script."
  command_exists python3 || fail "python3 is required to parse gh JSON output."
  [[ -f "$WORKFLOW_FILE" ]] || fail "Missing workflow file: $WORKFLOW_FILE"

  parse_repo_metadata
  collect_present_secrets

  log "Repository: $REPO_NAME_WITH_OWNER"
  log "Default branch: $DEFAULT_BRANCH"
  log "Workflow: $WORKFLOW_NAME ($WORKFLOW_FILE)"

  for secret_name in "${REQUIRED_SECRETS[@]}"; do
    if ! secret_is_present "$secret_name"; then
      missing+=("$secret_name")
    fi
  done

  if [ "${#missing[@]}" -gt 0 ]; then
    warn "Missing required repository secrets:"
    for secret_name in "${missing[@]}"; do
      print_secret_commands "$secret_name"
    done
    warn "Set the secrets above, then re-run this script with --dispatch."
    return 1
  fi

  log "All required repository secrets are present."

  if [ "$DISPATCH" -ne 1 ]; then
    log "Re-run with --dispatch to trigger the live gate."
    return 0
  fi

  log "Dispatching workflow only after secret checks passed."
  gh workflow run "$WORKFLOW_NAME" --repo "$REPO_NAME_WITH_OWNER" --ref "$DEFAULT_BRANCH" -f run_live_checks=true
  log "Workflow dispatch requested."
}

main "$@"
