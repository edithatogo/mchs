# Track Archive Policy

Agent coordination note: use this policy before moving any track between `conductor/tracks/` and `conductor/archive/`. Do not archive roadmap-only, scaffold-only, or unreviewed tracks.

## Purpose

The archive is for tracks whose implementation and evidence are complete enough,
within a declared support scope, that they no longer need active execution. It is
not a place to hide incomplete, scaffold-only, or overclaimed work.

## Archive Eligibility

A track may move to `conductor/archive/<track_id>/` only when all of the
following are true:

- `metadata.json` has `status: completed` and `current_state` is `complete` or
  explicitly `complete-with-gaps`.
- `metadata.json` scope statement and gap register are explicit for the track.
- `spec.md` acceptance criteria are satisfied for that scope or explicitly gap-recorded.
- `plan.md` has implementation tasks complete and phase checkpoints recorded.
- Required tests, validation reports, docs, contracts, release evidence, and
  publication evidence exist for the declared scope.
- `conductor-review` has run at the final phase or track boundary and any unresolved
  blockers are non-blocking gaps.
- `conductor/tracks.md` links to the archive path and states the evidence gate.
- Public docs and support-status matrices reflect the same scope and do not
  overclaim the archived track.

## Do Not Archive

Do not archive a track if:

- it contains only roadmap, templates, scaffolds, stubs, examples without executable
  validation, or overbroad future-state claims;
- its public contracts are not explicit and versioned, or its support scope is missing;
- its tests do not exercise the claimed scope of behavior;
- its package, docs, GitHub, or release claims have not been verified for scope;
- it changes user-visible support status but lacks release evidence or a gap log.

## Archive Audit Procedure

1. Inventory `[x]` tracks under `conductor/tracks/` and archived tracks under `conductor/archive/`.
2. For each `[x]` live track, classify it as `complete`, `complete-with-gaps`,
   `scaffold-only`, or `overclaimed`, and record bounded support/gaps.
3. Move only `complete` and accepted `complete-with-gaps` tracks to
   `conductor/archive/`.
4. Create remediation tracks for `scaffold-only` and `overclaimed` work.
5. Update `conductor/tracks.md`, metadata, docs references, and support-status
   pages.
6. Run `conductor-review` and attach archive-audit evidence for claims in scope.

## Required Archive Record

Each archived track should include or retain:

- `index.md`;
- `metadata.json`;
- `spec.md`;
- `plan.md`;
- final review or verification report, if available;
- links to tests, docs, contracts, workflows, release evidence, or explicit gaps.
