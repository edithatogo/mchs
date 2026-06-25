# Specification: Source Archive and Provenance Registry

## Goal

Create a durable registry for IHACPA source artifacts across all available years, file types, and service streams.

## Requirements

- Commit durable provenance manifests outside ignored raw storage.
- Preserve the source page URL, artifact URL, final redirected URL, content type, size, SHA-256, acquisition time, and status.
- Preserve acquisition run context, including script version or Git commit and source page snapshot details.
- Distinguish lifecycle axes for acquisition, extraction, implementation, and validation.
- Keep raw binaries out of normal Git history until a storage backend is chosen.
- Handle IHACPA-hosted files and Box-hosted share pages.
- Document how to reproduce a source acquisition pass.

## Acceptance Criteria

- `scripts/archive_ihacpa_sources.py` can list and download artifacts.
- Manifest fields are documented in `conductor/source-archive.md`.
- Manifests are written to a tracked provenance location, not ignored raw storage.
- Lifecycle state is represented as structured fields rather than a single status string.
- Large raw archives are ignored by Git.
- Known Box-hosted gaps are represented explicitly.
