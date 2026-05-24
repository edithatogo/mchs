#!/usr/bin/env bash
set -euo pipefail

readonly WORKFLOW_NAME="Power Platform Official Actions"
readonly WORKFLOW_FILE=".github/workflows/power-platform-official-actions.yml"
readonly DEFAULT_OPERATOR_INPUTS_FILE="docs/runbooks/github-live-gate.env"
readonly REQUIRED_SECRETS=(
  "POWER_PLATFORM_ENVIRONMENT_URL"
  "POWER_PLATFORM_APPLICATION_ID"
  "POWER_PLATFORM_CLIENT_SECRET"
  "POWER_PLATFORM_TENANT_ID"
)

DISPATCH=0
OPERATOR_INPUTS_FILE="$DEFAULT_OPERATOR_INPUTS_FILE"
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
Usage: ./scripts/bootstrap-power-platform-github-live-gate.sh [--inputs-file PATH] [--dispatch]

Checks the GitHub repository secrets required by the official Power Platform
live gate, validates a sanitized operator-inputs env file for placeholder
values, prints exact `gh secret set` commands for any missing secrets, and
dispatches the workflow only after the inputs and secrets are ready.

Options:
  --inputs-file PATH  Read sanitized operator inputs from PATH.
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

is_placeholder_angle_value() {
  case "$1" in
    '<'*'>')
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

validate_operator_input_value() {
  local key="$1"
  local value="$2"
  local placeholder="$3"
  local message="$4"

  if [ -z "$value" ]; then
    fail "$key is missing from $OPERATOR_INPUTS_FILE."
  fi

  if [ "$value" = "$placeholder" ] || is_placeholder_angle_value "$value"; then
    fail "$key still contains a placeholder value in $OPERATOR_INPUTS_FILE: $message"
  fi
}

validate_runtime_token_value() {
  local key="$1"
  local value="$2"

  if [ -z "$value" ]; then
    return 0
  fi

  if [ "$value" != "provided_by_github_actions" ]; then
    fail "$key must not store a real token in $OPERATOR_INPUTS_FILE; omit it or keep the built-in GitHub runtime sentinel only."
  fi
}

validate_operator_inputs_file() {
  local line
  local key
  local value
  local known_keys=""
  local live_gate_workflow=""
  local live_gate_tag=""
  local nsw_operator_name=""
  local nsw_operator_email=""
  local nsw_approver_name=""
  local nsw_approver_email=""
  local nsw_release_reason=""
  local nsw_release_notes=""
  local github_token=""
  local gh_token=""

  [ -f "$OPERATOR_INPUTS_FILE" ] || fail "Missing sanitized operator inputs file: $OPERATOR_INPUTS_FILE"

  log "Preflight operator inputs: $OPERATOR_INPUTS_FILE"

  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%$'\r'}"
    case "$line" in
      ''|\#*)
        continue
        ;;
    esac

    case "$line" in
      *=*)
        key="${line%%=*}"
        value="${line#*=}"
        ;;
      *)
        fail "Invalid operator input line in $OPERATOR_INPUTS_FILE: $line"
        ;;
    esac

    case "$key" in
      LIVE_GATE_WORKFLOW)
        live_gate_workflow="$value"
        ;;
      LIVE_GATE_TAG)
        live_gate_tag="$value"
        ;;
      NSW_OPERATOR_NAME)
        nsw_operator_name="$value"
        ;;
      NSW_OPERATOR_EMAIL)
        nsw_operator_email="$value"
        ;;
      NSW_APPROVER_NAME)
        nsw_approver_name="$value"
        ;;
      NSW_APPROVER_EMAIL)
        nsw_approver_email="$value"
        ;;
      NSW_RELEASE_REASON)
        nsw_release_reason="$value"
        ;;
      NSW_RELEASE_NOTES)
        nsw_release_notes="$value"
        ;;
      GITHUB_TOKEN)
        github_token="$value"
        ;;
      GH_TOKEN)
        gh_token="$value"
        ;;
      *)
        fail "Unknown operator input key in $OPERATOR_INPUTS_FILE: $key"
        ;;
    esac
  done < "$OPERATOR_INPUTS_FILE"

  validate_operator_input_value \
    "LIVE_GATE_WORKFLOW" \
    "$live_gate_workflow" \
    "" \
    "replace the example workflow with the actual workflow name you intend to reference"
  validate_operator_input_value \
    "LIVE_GATE_TAG" \
    "$live_gate_tag" \
    "v0.0.0" \
    "replace the example release tag with the real tag you intend to use"
  validate_operator_input_value \
    "NSW_OPERATOR_NAME" \
    "$nsw_operator_name" \
    "NSW operator name" \
    "replace the example operator name with the real approver/dispatcher name"
  validate_operator_input_value \
    "NSW_OPERATOR_EMAIL" \
    "$nsw_operator_email" \
    "operator@example.nsw.gov.au" \
    "replace the example operator email with the real approver/dispatcher email"
  validate_operator_input_value \
    "NSW_APPROVER_NAME" \
    "$nsw_approver_name" \
    "NSW approver name" \
    "replace the example approver name with the real approval name"
  validate_operator_input_value \
    "NSW_APPROVER_EMAIL" \
    "$nsw_approver_email" \
    "approver@example.nsw.gov.au" \
    "replace the example approver email with the real approval email"
  validate_operator_input_value \
    "NSW_RELEASE_REASON" \
    "$nsw_release_reason" \
    "Manual live-gate dispatch for GitHub release or registry publication" \
    "replace the example release reason with a real dispatch reason"
  validate_operator_input_value \
    "NSW_RELEASE_NOTES" \
    "$nsw_release_notes" \
    "Document the evidence bundle, dispatch time, and approval reference here" \
    "replace the example release notes with the real evidence reference"
  validate_runtime_token_value "GITHUB_TOKEN" "$github_token"
  validate_runtime_token_value "GH_TOKEN" "$gh_token"

  log "Operator inputs preflight passed."
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
      --inputs-file)
        shift
        [ "$#" -gt 0 ] || fail "--inputs-file requires a path argument."
        OPERATOR_INPUTS_FILE="$1"
        ;;
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

  validate_operator_inputs_file
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
