# MCHS Orchestration Visual Iteration

## Problem

The first published app was generated from the custom connector. It proved that
the app can be uploaded, saved, published, and launched, but it is not an
acceptable operating experience.

## Iteration

The optimized home screen turns the app into a governed operations console:

- Header communicates NSW environment, ALM scope, and synthetic-data-only use.
- Status cards separate connector, runtime, and evidence posture.
- Primary actions are ordered by operational readiness sequence.
- Governance panel makes production-readiness blockers visible.
- Loading spinner is enabled and no connector calls run on the home screen.

## Remaining

Publish `dist/power-platform/apps/mchs-orchestration-optimized.msapp` over the
existing app, then repeat visual smoke and screenshots.
