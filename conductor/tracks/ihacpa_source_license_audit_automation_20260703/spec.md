# IHACPA Source License Audit Automation

## Overview

Future IHACPA releases should be discovered, classified, and queued for review through repeatable automation that does not commit restricted assets or overclaim support.

## Requirements

- Extend source scanning to audit source availability, license status, manifest drift, capability drift, and validation gaps.
- Produce dry-run outputs that can draft manifest changes, Conductor tracks, and GitHub issues for review.
- Keep live scans separate from required CI unless configured as scheduled/non-blocking checks.
- Detect restricted assets and route them to local-only workflows.
- Include clear evidence links and gap records in generated drafts.

## Acceptance Criteria

- Audit fixtures cover new public source, restricted source, removed source, changed metadata, and validation drift.
- Dry-run issue and track drafts are deterministic and reviewable.
- Automation never commits or uploads restricted content.
- Documentation explains scheduled use, manual review gates, and publication caveats.

## Out of Scope

- Automatically merging source updates.
- Automatically accepting licensing decisions without maintainer review.
