# Specification: Repo Health 9.9 Power Platform Completion

## Overview

Create an enforceable path to a `9.9` Power Platform repo-health score without overclaiming current runtime or business outcomes.

The optimized home screen is published, but each connector operation page must be source-controlled, UX-complete, and runtime-proven before repo health can move beyond `9.5`.

## Functional Requirements

- Track every custom connector operation with a corresponding Power App screen source file.
- Distinguish source-controlled generated pages from UX-complete operation pages.
- Require live NSW `dylan` smoke evidence for health, validation, calculation, evidence, and flow operations.
- Keep calculation logic out of Power Apps; Power Apps remains orchestration-only.
- Add a `9.9` health contract that blocks promotion until page, runtime, flow, governance, ALM, and subrepo gates are evidenced.

## Acceptance Criteria

- All six connector operations have source-controlled page coverage.
- The contract explicitly states operation pages are not complete until optimized UX states and live connector execution are evidenced.
- Repo health remains `9.5` and does not claim `9.9` prematurely.
- Validators fail if operation pages, calculation proof, or 9.9 score are overclaimed.

## Out of Scope

- Claiming production readiness without live connection references and service-boundary execution evidence.
- Embedding calculator formulas in Power Apps.
- Treating a published app launch as proof of calculation correctness.
