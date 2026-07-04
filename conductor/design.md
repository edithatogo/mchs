# System Design

Agent coordination note: this file is the design authority for architecture and orchestration. Update it before changing core boundaries, contracts, release gates, or multi-agent execution rules.

## Design Goals

- Make Rust the shared calculator core for GA.
- Keep public behavior contract-first, versioned, and machine-verifiable.
- Preserve researcher workflows through Python, R, Julia, Stata interop, CLI/file contracts, and tutorials.
- Preserve enterprise workflows through C#, API, MCP, OpenAI tool adapter, Power Platform, release automation, and GitHub governance.
- Enable safe real-public-data tutorials only through explicit access/licensing
  assessment, local-only raw data handling, provenance reports, and fail-closed
  classification boundaries.
- Prevent scaffold-only completion by requiring executable evidence and review loops.
- Enable safe parallel work by splitting tracks into bounded contracts, implementations, validation, docs, and release work packages.

## Architecture Overview

```mermaid
flowchart LR
    Sources[Official sources\nIHACPA, jurisdictions, public reports] --> Archive[Source archive\nmanifest + hashes + gap records]
    PublicData[Public clinical datasets\nMIMIC, FHIR, MEDS, synthetic EHR] --> DatasetManifest[Dataset suitability\naccess + license + local cache policy]
    DatasetManifest --> Staging[Worked-example staging\nlineage + data quality + provenance]
    Staging --> Contracts
    Archive --> Bundles[Formula, parameter, coding-set, price bundles]
    Bundles --> Contracts[Canonical versioned contracts\nJSON Schema + OpenAPI + CLI/file + MCP]
    Contracts --> Rust[Rust calculator core]
    Rust --> Py[Python binding]
    Rust --> R[R binding]
    Rust --> Julia[Julia binding]
    Rust --> CSharp[C#/.NET binding]
    Rust --> Wasm[TypeScript/WASM docs demos]
    Rust --> CLI[CLI and file interface]
    CLI --> Stata[Stata interop]
    Contracts --> API[HTTP API]
    Contracts --> MCP[MCP tools/resources]
    Contracts --> OpenAI[OpenAI tool adapter]
    Rust --> Evidence[Validation and release evidence]
    Evidence --> Docs[Starlight documentation]
    Evidence --> Releases[Tagged releases and registries]
```

## Contract Enforcement Flow

```mermaid
flowchart TD
    Req[MoSCoW requirements] --> Design[System design]
    Design --> Track[Granular track spec and plan]
    Track --> Schema[Versioned schemas and fixtures]
    Schema --> Impl[Implementation]
    Impl --> Tests[Unit, property, parity, conformance tests]
    Tests --> CI[Strict CI/CD gates]
    CI --> Review[conductor-review auto-fix loop]
    Review --> Evidence[Evidence bundle]
    Evidence --> Publish[Docs, release, registry, GitHub status]
    Publish --> Audit[Recursive SOTA audit]
    Audit --> Req
```

## Multi-Level Agent Execution Model

```mermaid
flowchart TB
    Lead[Lead orchestrator] --> A1[Track architect]
    Lead --> A2[Implementation coordinator]
    Lead --> A3[Validation coordinator]
    Lead --> A4[Docs/release coordinator]
    A1 --> B1[Schema subagent]
    A1 --> B2[Dependency and scope subagent]
    A2 --> B3[Rust core worker]
    A2 --> B4[Binding worker]
    A3 --> B5[Parity validator]
    A3 --> B6[Security/CI validator]
    A4 --> B7[Starlight docs worker]
    A4 --> B8[GitHub/release worker]
    B1 --> H1[Handoff with files, evidence, risks]
    B3 --> H1
    B5 --> H1
    B7 --> H1
    H1 --> Review[conductor-review]
    Review --> Next[Next phase or track]
```

## Release and Quality Gates

```mermaid
stateDiagram-v2
    [*] --> RoadmapOnly
    RoadmapOnly --> ScaffoldOnly: scaffold exists
    ScaffoldOnly --> InProgress: real implementation starts
    InProgress --> ReviewCandidate: tests + docs + evidence drafted
    ReviewCandidate --> InProgress: conductor-review finds blockers
    ReviewCandidate --> ReleaseCandidate: strict CI + >=90% coverage + evidence
    ReleaseCandidate --> GA: tag + release + docs + registry + support status
    GA --> Maintenance: recursive audits and dependency updates
```

## Core Design Decisions

| Decision | Current position | Enforcement |
| --- | --- | --- |
| Calculator core | Rust core is the GA target; Python remains a stable consumer during migration. | Rust Core GA and parity tracks. |
| Contract source | Canonical schemas and typed models define behavior; adapters consume them. | Contract enforcement harness and drift tests. |
| Data representation | Arrow/Parquet-friendly file contracts for batch work; JSON for API/tool control planes. | CLI/file and canonical contract tracks. |
| API shape | Domain OpenAPI contract first; OpenAI compatibility only as an adapter/tool surface. | HTTP API and OpenAI adapter tracks. |
| Agent work | Multi-agent work must be granular, owned, reviewed, and evidence-backed. | Subagent orchestration and no-stub enforcement. |
| Docs | Starlight/Astro is the documentation platform. | Docs SOTA Starlight track. |
| GitHub setup | Repository metadata, security, branch protection, releases, package publishing, and Pages are part of Done. | GitHub repo SOTA setup track. |
| Public dataset examples | Public clinical datasets are tutorial inputs only after dataset suitability, licensing, local-only cache policy, provenance, data-quality, and classification fail-closed behavior are explicit. | Public clinical dataset worked example track and follow-up GitHub issues. |

## Public Dataset Worked Example Design

Public dataset examples are deliberately separate from official IHACPA source
validation. They demonstrate how the calculator contracts can be used with
real deidentified public data while preserving licensing, privacy, and
Australian classification boundaries.

```mermaid
flowchart LR
    Candidate[Candidate public datasets] --> Assess[Suitability assessment\naccess + license + fields + risks]
    Assess --> Manifest[Committed manifest\nsource + citation + local-cache policy]
    Manifest --> LocalData[Local raw files\nignored, never committed]
    LocalData --> Stage[Episode staging\nlineage + quality checks]
    Stage --> Classify{Australian classification provenance?}
    Classify -->|Precomputed or local licensed| Input[Calculator-ready input]
    Classify -->|Missing| Block[Fail-closed diagnostic]
    Classify -->|Synthetic overlay for docs| DemoInput[Demo-only calculator input]
    Input --> Output[Calculated output + provenance report]
    DemoInput --> Output
    Block --> Docs[Docs caveats + support status]
    Output --> Docs
```

Design rules:

- Candidate datasets must be assessed before implementation, including access,
  license, citation, credentialing, redistribution, field coverage, file size,
  and update cadence.
- Raw public patient-level files stay local-only and must be guarded against
  accidental commits.
- MIMIC US DRG, ICD-9-CM, ICD-10-CM, and ICD-10-PCS fields must not be treated
  as validated Australian AR-DRG, ICD-10-AM, ACHI, or ACS equivalents.
- Worked examples should expose provenance, data-quality, support-status,
  Python API, CLI/file interop, MCP boundary validation, and API/OpenAI
  contract documentation where existing tooling supports them. MCP, API, or
  OpenAI surfaces must not claim formula execution when their current contracts
  only validate or document the boundary.
- New reusable capabilities discovered by examples must become separate
  GitHub issues or Conductor tracks rather than expanding a single tutorial
  track without bounds.

## Stub Detector Integration

The stub detector (`conductor/scripts/stub_detector.py`) enforces MUST-010 (no stub
completion) and MUST-011 (auto-review loop). It is invoked automatically as part of
the `conductor-review` protocol at every phase and track boundary:

```mermaid
flowchart LR
    Phase[Phase or track boundary] --> StubCheck[Stub detector run]
    StubCheck -->|No stubs| Continue[Continue to checkpoint]
    StubCheck -->|Stubs found| Fix[Auto-fix high-confidence stubs]
    Fix --> Recheck[Re-run stub detector]
    Recheck -->|Resolved| Continue
    Recheck -->|Unresolved| Block[Report blockers]
```

### Invocation Contract

```bash
# Full scan with JSON report for automated consumption
python conductor/scripts/stub_detector.py --root . --json

# Auto-fix high-confidence stubs (downgrade overclaimed track states)
python conductor/scripts/stub_detector.py --root . --fix

# Dry-run to preview fixes
python conductor/scripts/stub_detector.py --root . --fix --dry-run
```

Exit code `0` = no stubs; exit code `1` = stubs detected (blocks advancement).

### Exclusion Mechanisms

Tracks may opt out of stub enforcement by adding one of:

- `"no_stub_enforce": true` in `metadata.json` — for tracks where governance,
  audit, or documentation-only work is the legitimate completion evidence.
- `# no-stub-enforce` (Python) or `// no-stub-enforce` (Rust) at the top of a
  source file — for files that intentionally contain abstract stubs or
  forward declarations.

## Track Cross-Reference Rule

Every new or updated track must reference:

- `conductor/requirements.md` requirement IDs it satisfies.
- `conductor/design.md` design sections or diagrams it changes.
- Explicit contracts it creates or consumes.
- Validation evidence required before completion.
- Whether the track can be parallelised and its subagent ownership boundaries.
