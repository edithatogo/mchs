# Specification: Abstraction Doctrine Enforcement

## Overview
Make the project abstraction doctrine explicit and enforceable. The codebase
must preserve clear boundaries between formula kernels, reference data bundles,
classification registries, mapping and grouping adapters, validation models,
language bindings, apps, and documentation examples.

This track is a governance scaffold. It defines the canonical abstraction
doctrine, records where boundary ownership belongs, and adds review and check
surfaces that future tracks must follow.

## Primary Contract
The primary contract is a shared ports-and-adapters doctrine plus reviewable
boundary guardrails that tell maintainers where to put formulas, parameters,
mappings, groupers, bindings, app orchestration, and docs examples without
duplicating kernel logic.

## Doctrine Principles
- Formula kernels own the domain math and should not depend on app orchestration
  or binding-specific concerns.
- Reference bundles and registries own versioned data, parameters, coding sets,
  and classifier metadata.
- Mapping and grouping adapters translate external inputs into canonical
  internal forms without duplicating kernel logic.
- Validation models describe and check inputs and outputs, but do not become a
  second implementation of the kernels.
- Language bindings and apps orchestrate, call kernels, and render outputs;
  they must stay thin and delegate logic downward.
- Documentation examples may demonstrate usage, but they must not become an
  alternate source of formula truth.
- No proprietary assumptions: the architecture must not assume hidden fee
  schedules, private crosswalks, or unpublished mappings as part of the core
  design.

## Boundary Taxonomy
- Kernel boundary: canonical formulas, calculators, and rule evaluation.
- Bundle boundary: versioned reference data, lookup tables, and parameter sets.
- Registry boundary: classifier catalogs, coding-set definitions, and
  provenance-bearing metadata.
- Adapter boundary: mapping, grouping, and transformation code that converts
  external records into canonical inputs.
- Validation boundary: schema checks, business-rule guards, and invariant
  enforcement around kernel inputs and outputs.
- Binding boundary: language-specific wrappers and SDKs that call into kernels
  or adapters without re-implementing them.
- App boundary: workflow, UI, or automation orchestration that composes the
  lower layers.
- Docs boundary: examples, walkthroughs, and contributor notes that describe
  the architecture but do not define new behavior.

## Dependencies and Scope
- This track depends on the completed emergency and classification governance
  tracks that already establish versioned registries, mapping bundles, grouped
  output boundaries, fixture parity, pricing-year validation gates, and coding
  set provenance.
- The track must stay upstream of future formula, binding, app, and docs work;
  it is not a substitute for the implementation tracks it governs.
- Compatibility exceptions are allowed only as transitional-state shims and
  must be labeled as such.

## Functional Requirements
- Define a doctrine document that states allowed dependencies and forbidden
  shortcuts across the boundary taxonomy.
- Add tests or static checks that prevent apps, bindings, and docs examples from
  introducing duplicate formula logic.
- Add review checklist items for new pricing years, coding sets, classifiers,
  groupers, and language bindings.
- Add developer documentation showing where formulae, parameters, mappings,
  groupers, bindings, and app orchestration belong.
- Document how transitional compatibility layers may exist without becoming the
  intended architecture.
- Link all future roadmap tracks to the shared abstraction doctrine before
  implementation starts.
- Record the canonical evidence surfaces for the doctrine in track metadata and
  track index summaries.

## Non-Functional Requirements
- Abstraction rules must be concrete enough to review in pull requests.
- Enforcement should prioritize high-signal checks over brittle text matching.
- Exceptions must be documented as transitional-state compatibility, not
  intended architecture.
- No proprietary or undisclosed crosswalk, fee schedule, or source table may be
  treated as part of the canonical architecture unless the source license
  explicitly permits it.

## Validation Surfaces
- Pull request review checklist for boundary placement, duplication, and
  provenance.
- Static or test-based checks for obvious duplicate-formula paths in apps,
  bindings, and examples.
- Documentation review for explicit references to the doctrine and to the
  canonical place to add new formulas, parameters, mappings, and groupers.
- Metadata and roadmap checks ensuring new tracks point back to the doctrine
  instead of inventing their own abstraction rules.

## Acceptance Criteria
- Architecture docs define allowed dependencies and forbidden shortcuts.
- CI or tests catch at least the highest-risk duplicate-formula paths.
- Roadmap and contributor docs tell maintainers where to add formulae,
  parameters, mappings, groupers, bindings, and app orchestration.
- Existing roadmap tracks remain consistent with the abstraction doctrine.
- Track metadata and index pages expose status, validation status, caveats, and
  evidence surfaces clearly enough to audit without reading implementation.
