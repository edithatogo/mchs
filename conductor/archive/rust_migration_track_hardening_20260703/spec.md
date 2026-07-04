# Rust Migration Track Hardening Specification

## Overview

Harden the Rust CLI/MCP migration track set before implementation begins. This track does not implement the Rust migration itself; it corrects and sharpens the three active Rust migration tracks so their metadata, specs, plans, runtime decisions, and validation gates are decision-complete and aligned with Conductor governance.

The track covers:

- `rust_cli_core_migration_20260703`
- `rust_mcp_core_migration_20260703`
- `rust_cli_mcp_promotion_evidence_20260703`

## Functional Requirements

- Normalize governance metadata for the three Rust migration tracks:
  - CLI track: `track_class` is `binding`, `current_state` is `roadmap-only`, and `publication_status` is `published-with-gaps`.
  - MCP track: `track_class` is `binding`, `current_state` is `roadmap-only`, and `publication_status` is `published-with-gaps`.
  - Promotion track: `track_class` is `validator`, `current_state` is `roadmap-only`, and `publication_status` is `future-only`.
- Update the CLI and MCP migration specs to pin the first implementation slice to acute 2025, using existing Rust canary/kernel evidence as the starting point.
- Update the CLI migration spec and plan to make runtime selection explicit:
  - expose `--runtime python|rust|auto` for CLI users;
  - keep the default as `python` until the promotion track proves a default change;
  - allow `NWAU_RUNTIME` only as an internal or CI override;
  - give explicit CLI options precedence over environment defaults;
  - fail closed when `rust` is requested for unsupported calculators, years, formats, or output modes.
- Update the MCP migration spec and plan to distinguish the Python stdio transport shim from the formula runtime:
  - Python may remain the stdio transport during transition;
  - promoted calculation behaviour must use the Rust-backed dispatcher;
  - MCP should reuse CLI runtime policy and parity fixtures;
  - MCP should not shell out to the CLI unless a later implementation decision records that boundary explicitly.
- Add a contract-hardening pre-phase to the CLI and MCP migration plans covering:
  - numeric tolerance and rounding policy;
  - schema parity source;
  - unsupported diagnostic codes;
  - acute 2025 fixture scope;
  - support-status wording for Rust canary, Rust opt-in, Python default, and Rust default.
- Add or extend repo-local validation so the Rust migration track set rejects:
  - unknown `track_class` values;
  - unknown `current_state` values;
  - missing `publication_status`;
  - Rust migration tracks that omit the runtime-selection or first-slice decisions.
- Keep the first validator scoped to the Rust migration track set so legacy tracks with older metadata vocabularies do not block this hardening track before the broader governance backfill is complete.
- Update the Conductor status matrix and active-track registry after hardening changes.
- Record additional improvement recommendations for follow-on work:
  - synchronize reusable `conductor-newtrack` skill/template wording with this repo's automated-review workflow;
  - decide whether the metadata-governance validator should later cover every active track after legacy backfill;
  - ensure GitHub Project synchronization includes this new hardening track if the external project boards remain active planning surfaces.

## Non-Functional Requirements

- The hardening work must not change runtime behaviour, package entry points, registry publication status, or released docs claims.
- Documentation and track language must separate current state from intended state.
- The validation added by this track must be non-interactive and suitable for CI.

## Acceptance Criteria

- The three Rust migration tracks use only governance-approved metadata values and include `publication_status`.
- CLI and MCP specs identify acute 2025 as the first Rust-backed implementation slice.
- CLI runtime selection is specified as `--runtime python|rust|auto`, defaulting to Python until promotion evidence changes that decision.
- MCP specs distinguish Python transport from Rust-backed formula execution and avoid making shell-out-to-CLI the implicit architecture.
- A validator or focused test fails if the same governance and runtime-decision gaps return in the Rust migration track set.
- `python3 scripts/validate_conductor_status_matrix.py` passes.

## Out of Scope

- Implementing Rust-backed CLI execution.
- Implementing Rust-backed MCP execution.
- Promoting Rust to the default runtime.
- Publishing package, registry, or MCP releases.
- Changing non-CLI/MCP adapters such as R, Julia, Power Platform, web demos, or C ABI.
