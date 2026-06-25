# Parallelization Plan

## Purpose

This track is designed for six subagents working in parallel while preserving
the repository-evidence boundary and the distinction between current package
management, docs-site readiness, and deferred language surfaces.

## Dependencies

The following completed work is treated as prerequisite context:

- Public calculator API contract.
- Cross-language golden fixture runner.
- Release and supply-chain governance.
- Docs-site architecture and deployment surface.
- Validation vocabulary.

## Subagent Workstreams

1. Repository inventory and matrix schema.
   Owns current-state inspection, standards matrix structure, and artifact
   inventory.

2. Python package readiness.
   Owns the current Python packaging and version-management assessment,
   including pyproject/lockfile evidence, transitional artifacts, CI, tests,
   governance files, and publication readiness criteria.

3. Docs-site package maturity.
   Owns the current docs-site npm/package-lock evidence, Node/version policy,
   build/deploy workflow, and GitHub Pages readiness criteria.

4. Deferred surfaces.
   Owns the missing C#, Power Platform, R, and Julia artifact inventory and
   the wrapper/prototype/defer decision criteria for those surfaces.

5. Standards matrix integration.
   Owns the dependency graph, recommendation matrix, and distinction between
   current evidence, transitional artifacts, and intended-state guidance.

6. Final governance alignment.
   Owns consistency checks across the spec, plan, metadata, and index files.

## Write Ownership

- Standards matrix: Worker 1 owns the schema; workers 2 through 4 add their
  domain rows.
- Python readiness: Worker 2 owns the section.
- Docs-site readiness: Worker 3 owns the section.
- Deferred-surface guidance: Worker 4 owns the section.
- Decision matrix and recommendation ordering: Worker 5 owns the integration.
- Final Conductor alignment: parent agent owns the merge.

## Merge Order

1. Repository inventory and schema.
2. Python readiness assessment.
3. Docs-site maturity recommendations.
4. Deferred surface guidance.
5. Final dependency, validation, and Conductor consistency pass.

## Coordination Rules

- Workers must not broaden implementation or validation claims.
- Workers must distinguish current evidence from future recommendations.
- Workers must cite official or authoritative sources for external standards.
- Workers must preserve the shared public contract and golden fixtures as the
  parity gate for any later implementation claim.
