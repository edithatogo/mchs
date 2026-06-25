# Specification: SAS Interoperability

## Overview
SAS interoperability is classified as a private/local reference-comparison
surface. The repository may document how licensed users compare shared-core
outputs with IHACPA SAS calculator outputs, but it does not publish a SAS
adapter, SAS package, SAS macro layer, or SAS formula port.

This track is complete as a governance reclassification, not as a new
implementation surface. Existing SAS-read workflows for local archive and table
inspection remain available where already present; new development must happen
through the shared CLI/file contract or another approved public adapter.

## Functional Requirements
- Classify SAS interoperability as private/no-new-development by default.
- Preserve local SAS reference-output comparison guidance without committing
  licensed SAS source code or derived formula logic.
- Require shared-core outputs to cross the boundary through CSV, Parquet, or
  another approved CLI/file contract format.
- Define comparison-report evidence that a licensed user can produce locally.
- Keep source provenance and validation status explicit.
- Document how SAS calculators are used as references without duplicating code.

## Acceptance Criteria
- Track metadata says `private-no-new-development` and
  `private-not-published`.
- SAS interop strategy is documented as private reference comparison, not a
  public adapter or formula port.
- Comparison evidence is described as local/licensed unless based on synthetic
  fixtures.
- Restricted IHACPA artifacts are handled according to source policy.
- Tests assert that this track does not claim adapter readiness, public package
  publication, or copied SAS formula logic.
