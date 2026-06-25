# Track Template: IHACPA Discovery Audit

Use this template to create a recurring audit track that searches IHACPA's public website for new formulae, systems, mappings, groupers, technical specifications, costing data, documentation, or classification changes that should enter the roadmap or source archive.

## Template Variables

- `TRACK_ID`: `ihacpa_discovery_audit_<YYYYMMDD>`
- `TRACK_TITLE`: `IHACPA Discovery Audit`
- `AUDIT_DATE`: `<YYYY-MM-DD>`
- `PRICING_YEARS`: `<years or all current/recent years>`
- `AUDITOR`: `<name or role>`
- `TRACK_STATUS`: `new` for a created track, or another valid lifecycle status

## metadata.json

```json
{
  "track_id": "TRACK_ID",
  "type": "chore",
  "status": "TRACK_STATUS",
  "track_class": "source-discovery",
  "current_state": "roadmap-only",
  "primary_contract": "source discovery audit report",
  "dependencies": [
    "conductor/source-archive.md",
    "conductor/roadmap-governance.md"
  ],
  "completion_evidence": [
    "source discovery table",
    "URLs and retrieval metadata",
    "new or updated roadmap tracks"
  ],
  "publication_status": "not-applicable",
  "created_at": "AUDIT_DATET00:00:00Z",
  "updated_at": "AUDIT_DATET00:00:00Z",
  "description": "Search IHACPA for new formulae, systems, mappings, classifications, cost data, and documentation relevant to PRICING_YEARS."
}
```

## spec.md

```markdown
# Specification: TRACK_TITLE

## Overview
Search IHACPA's public website for new or changed materials relevant to NWAU calculation, activity-based funding, costing studies, and classification systems. The audit should identify source artifacts that require implementation, archival, documentation, validation, or roadmap changes.

## Discovery Scope
- NEP, NEC, NWAU calculators, national pricing model technical specifications, price weights, and user guides.
- Formulae, adjustment parameters, HAC/AHR materials, risk models, grouper logic, and reference tables.
- Classification systems and mappings including AR-DRG, ICD-10-AM, ACHI, ACS, AECC, UDG, Tier 2, AMHCC, SNAP, and future systems.
- Emergency mapping or transition resources such as UDG to AECC changes.
- Admitted acute grouping resources such as ICD-10-AM/ACHI/ACS to AR-DRG relationships and grouper versions.
- Costing materials including AHPCS, NHCDC, cost report appendices, data request specifications, cost buckets, and cost bucket reviews.
- Aged care or adjacent IHACPA pricing/costing systems if relevant to future extension.

## Required Evidence
- Search queries used.
- Source URLs, publication dates, retrieval dates, file names, and checksums where downloadable.
- Classification of each source as new, changed, unchanged, inaccessible, licensed/restricted, or irrelevant.
- Recommended action for each relevant source: archive, manifest, implement, validate, document, create track, or ignore.
- SAS and Excel availability for each pricing year, including whether parity can be checked or must be gap-recorded.

## Acceptance Criteria
- The audit produces a source discovery table with URLs and recommended actions.
- New or changed relevant materials produce Conductor tracks or updates to existing roadmap tracks.
- Restricted/licensed materials are marked without being committed unless redistribution is permitted.
- The source archive matrix and validation roadmap are updated or follow-up tasks are created.
- Pricing-year validation recommendations explicitly state whether SAS parity and Excel formula parity are possible.

## Out of Scope
- Implementing all newly discovered formulae or systems during the audit.
- Circumventing access controls or redistributing restricted classification products.
```

## plan.md

```markdown
# Plan: TRACK_TITLE

## Phase 1: Search Strategy
- [ ] Task: Define IHACPA search queries and source categories.
    - [ ] Include pricing, NWAU, classifications, groupers, mappings, costing, NHCDC, AHPCS, and cost buckets.
    - [ ] Record expected current-year and historical-year coverage.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Search Strategy' (Protocol in workflow.md)

## Phase 2: Source Discovery
- [ ] Task: Search IHACPA's public website and collect candidate sources.
    - [ ] Record URLs, publication dates, filenames, checksums, and source category.
    - [ ] Mark inaccessible, Box-hosted, or restricted materials explicitly.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Source Discovery' (Protocol in workflow.md)

## Phase 3: Relevance and Gap Analysis
- [ ] Task: Compare discovered sources against local manifests, docs, archive matrices, and roadmap tracks.
    - [ ] Identify new formulae, changed parameters, new systems, mappings, groupers, and documentation gaps.
    - [ ] Separate implementation sources from costing-study/reference materials.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Relevance and Gap Analysis' (Protocol in workflow.md)

## Phase 4: Roadmap and Manifest Updates
- [ ] Task: Create or update tracks for each relevant new gap.
    - [ ] Update source archive matrices or create manifest follow-up tasks.
    - [ ] Add documentation/tutorial recommendations where warranted.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Roadmap and Manifest Updates' (Protocol in workflow.md)
```
