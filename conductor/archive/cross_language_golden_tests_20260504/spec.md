# Specification: Cross-Language Golden Test Suite

## Goal

Create self-describing fixture packs that enforce parity across Python, future C#, and web calculation surfaces without relying on Python-specific assumptions.

## Current State

- The repository already contains one concrete pilot pack at `tests/fixtures/golden/acute_2025/`.
- That pack is synthetic and small, and it uses a JSON manifest plus CSV payloads.
- The shared runner/validator API exists in `nwau_py.fixtures` and exposes manifest loading, pack loading, payload reading, runner parameter generation, and runner execution through `load_fixture_manifest`, `load_fixture_pack`, `read_payload_frame`, `iter_fixture_cases`, `fixture_case_params`, `run_fixture_case`, `run_fixture_suite`, `run_fixture_suite_from_root`, and `assert_fixture_case_output`.
- The manifest vocabulary is runner-neutral. It uses fields such as `fixture_id`, `calculator`, `pricing_year`, `service_stream`, `cross_language_ready`, `privacy_classification`, `source_basis`, `payloads`, `precision`, and `provenance`.
- The current pack is intentionally shaped so shared readers can consume the same manifest and payload files across runners without Python-specific objects or harness details.
- Arrow/Parquet remain the preferred payload format for future packs where practical, but the current acute pilot pack remains CSV-backed.

## Requirements

- Fixture packs must be synthetic, small, and explicitly source traceable.
- Each fixture pack must include a committed manifest that describes calculator, pricing year, service stream, inputs, expected outputs, tolerance, rounding policy, source basis, and privacy classification.
- The current pilot pack uses CSV payloads; Arrow/Parquet remain preferred where practical for future packs that need stronger cross-language interoperability.
- The manifest must declare cross-language readiness, schema version, fixture identifiers, and any required compatibility notes.
- Fixtures must be self-describing enough that failures can report provenance, tolerance, and privacy classification without inspecting implementation code.
- The fixture format must remain stable across runners and must not encode Python-specific objects or test harness details.
- Python tests already consume the acute pilot pack through the shared runner helper and report provenance in failures.

## Acceptance Criteria

- The acute_2025 synthetic pilot pack exists with a manifest and payloads.
- The fixture manifest is parseable by C#-oriented tooling without translation of the core fields.
- Privacy classification, source basis, tolerance, and rounding policy are enforced by schema validation.
- Python tests can read the pilot pack through the shared manifest contract and surface provenance in failures.
- The fixture format is suitable for web and future cross-language parity checks.

## Parity Workflow

1. Python, C#, and web runners all resolve the same committed manifest and payload paths.
2. Each runner validates the shared metadata before execution, including privacy classification, source basis, tolerance, rounding policy, and cross-language readiness.
3. The runner then loads the payloads using its own native reader while preserving the field names and value semantics declared in the manifest.
4. Any fixture marked `cross_language_ready: true` becomes release-blocking for downstream surfaces until all supported runners can consume the same pack without translation of the core contract.
5. Any pack that fails validation remains a regression fixture only and must not be used as a cross-language release gate.
