# Active Workstreams

> Parallel-agent notice: update this file before taking ownership of files in
> an active track. Cline/deepseek and Codex may be working in this repository at
> the same time.

## Ownership protocol

- Add or update a row before editing shared files.
- Keep owned paths narrow.
- Do not stage files owned by another active agent without coordination.
- Always stage only owned files.
- Record validation and handoff status before leaving a track.

| Agent | Track | Owned paths | Started | Validation | Handoff status |
| --- | --- | --- | --- | --- | --- |
| Codex | coordination/governance guardrails | `conductor/active-workstreams.md`, `conductor/templates/review-template.md`, `contracts/support/`, `contracts/release/`, `contracts/surfaces/`, governance tests | 2026-05-13 | `uv run pytest tests/test_governance_contracts.py -q` | In progress |
| Cline/deepseek | Rust implementation and generated contracts | `rust/crates/`, `contracts/canonical/`, `contracts/cli-file/`, `contracts/http-api/`, `contracts/mcp/`, `contracts/openai-adapter/`, `.github/workflows/` | 2026-05-13 | Owner to record | Active external agent |

## Handoff requirements

- Track `review.md` exists or an equivalent review note is linked.
- Changed files are listed.
- Validation commands and results are recorded.
- Remaining blockers are explicit.
- Next owner is named or set to `unassigned`.

## 2026-10-31 isolated qualification lane

Current GHA chat owns `/Users/doughnut/Documents/mchs-qualified`, branch
`codex/python315-qualification`, runtime/dependency qualification and subsequent
NEP26 and mapping PR branches under parent #396. This is a fresh verified remote
clone, not the unrelated dirty local checkout. Earlier assignments above remain
history; no changes to their local files or native operations. No deployment,
registry submission or patient-data publication is part of this lane.
