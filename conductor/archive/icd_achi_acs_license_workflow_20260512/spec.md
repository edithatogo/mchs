# Specification: ICD-10-AM/ACHI/ACS Licensed Product Workflow

## Overview
Add a formal workflow for handling licensed classification products required for admitted acute grouping and validation, including ICD-10-AM, ACHI, ACS, AR-DRG definitions manuals, mapping tables, and grouper software.

## Contract
- The repository may describe licensed products, local file locations, and validation status, but it must not commit, mirror, or redistribute restricted tables, manuals, or grouper binaries.
- Any manifest or setup flow must accept user-supplied local paths or environment references for licensed assets.
- Public, synthetic, and metadata-only artifacts are the only artifacts that can be used in CI or published documentation.
- The track governs workflow and guardrails only; it does not provide the licensed content itself and does not replace the user's own licensing obligations.

## Local-Only License Boundary
- Licensed products must live outside the repository or in an ignored local path.
- Manifests may point to local paths or environment variables, but those references are placeholders until the user supplies legitimate licensed assets.
- The workflow must fail safely when required licensed assets are absent, and the failure text must name the missing category without exposing restricted contents.
- The repository must stay publishable even when no licensed products are present on disk.

## Functional Requirements
- Document which assets are public metadata versus licensed/restricted products.
- Add local-only paths and manifest references for user-supplied licensed products.
- Add checks that prevent restricted assets from being committed.
- Add setup docs for users who have legitimate access to licensed products.
- Add CI-safe tests using synthetic/minimal fixtures that do not contain restricted content.

## Evidence Surfaces
- `metadata.json` records the track contract, current state, and completion evidence expectations.
- `spec.md` defines the boundary between public metadata and user-supplied licensed assets.
- `plan.md` breaks the workflow into phased deliverables with review checkpoints.
- Repository guards and ignore rules demonstrate that restricted files cannot enter version control.
- Synthetic-only tests demonstrate safe behavior when licensed assets are unavailable.
- Setup documentation demonstrates the supported local-only configuration path.

## Non-Functional Requirements
- Repository must remain publishable without restricted classification products.
- Error messages must tell users what local asset is missing without exposing restricted content.
- Docs must be explicit that users are responsible for obtaining licenses where required.
- No task should imply that the repository provides, caches, or vendors the licensed products.
- CI must remain safe to run without access to any restricted classification table, manual, or grouper bundle.

## Acceptance Criteria
- Restricted asset patterns are ignored or guarded.
- Manifests can reference local licensed files without committing them.
- Documentation gives a safe setup path for licensed grouper/table users.
- The plan includes explicit phase checkpoints and artifact-level evidence for the boundary, guards, and docs.
- The workflow clearly states that licensed products are local-only and user-supplied.

## Caveats
- This track is governance and workflow only; it is not a source of licensed classification data.
- The repository must not encode or infer any proprietary classification content beyond safe metadata references.
- Supported behavior is limited to local, user-controlled environments where the user already has lawful access.
- Any integration with external grouper software remains subject to vendor licensing and distribution terms.

## Source Evidence
- IHACPA admitted acute care product and licence references: https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care
