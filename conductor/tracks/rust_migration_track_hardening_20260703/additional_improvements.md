# Additional Track-Quality Improvements

This track intentionally scopes hardening validation to the Rust migration
track set first. The repository still contains legacy tracks with older
metadata vocabularies, so broad enforcement should wait until legacy backfill
is complete.

Recommended follow-on improvements:

- Update the reusable `conductor-newtrack` skill or repo-local track template
  wording so newly generated plans use the repo's automated-review workflow
  language rather than older manual-verification checkpoint wording.
- Add a broader metadata-governance validator after legacy backfill normalizes
  older track metadata values. The first broad validator should distinguish
  active-track requirements from archived historical records.
- Include this hardening track in GitHub Project synchronization if GitHub
  Project synchronization remains an active planning surface for MCHS and
  RI-HERO coordination.
