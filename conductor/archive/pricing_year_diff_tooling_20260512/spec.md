# Specification: Pricing-Year Diff Tooling

## Overview
Add diff tooling to compare formulae, parameters, coding-set versions, source artifacts, and validation status between pricing years.

## Functional Requirements
- Add `funding-calculator diff-year <from-year> <to-year>`.
- Compare NEP/NEC constants, price weights, adjustment parameters, classification versions, source files, and validation statuses.
- Emit human-readable markdown and machine-readable JSON outputs.
- Highlight breaking changes and areas requiring new fixtures.

## Non-Functional Requirements
- Diffs must be stable for review and release notes.
- Large data diffs should summarize by stream and changed keys rather than dumping full tables by default.
- Diffs must distinguish source-data changes from implementation changes.

## Acceptance Criteria
- Diff command works for two manifest-backed years.
- Tests cover changed, unchanged, missing, and newly introduced parameter cases.
- Release docs can consume diff output for change summaries.
