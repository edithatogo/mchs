# Licensed Asset Loader Framework

## Overview

Users with valid licenses need a supported way to register and validate local restricted assets while the repository remains redistributable.

## Requirements

- Add an ignored local asset manifest for licensed IHACPA, ICD-10-AM, ACHI, ACS, mapping, and grouper assets.
- Provide CLI tooling to register, validate, diagnose, and audit local licensed assets.
- Require explicit user acknowledgement that licensing remains their responsibility.
- Add commit and CI guards that reject restricted source files and common licensed asset signatures.
- Expose local asset availability to validators and grouper/classifier providers without leaking restricted data.

## Acceptance Criteria

- Safe fixture manifests validate and missing/invalid local assets fail closed.
- Restricted dummy files are rejected by guard tests.
- Documentation explains what can be committed, what is local-only, and how runtime loading works.
- Runtime status reports `blocked_licensed` when required local assets are absent.

## Out of Scope

- Supplying licensed assets.
- Circumventing license checks or reverse engineering proprietary logic.
