# AR-DRG Version Parity Fixture Workflow Notes

This track documents fixture workflows for version-specific AR-DRG grouping and admitted acute NWAU behavior.

## Fixture classes

- Synthetic fixtures are the default for committed examples.
- Local licensed fixtures are allowed only when the source license permits local use and the outputs stay out of the repository.

## Safe synthetic workflow

Use synthetic fixtures when you need stable, reviewable examples that prove version-specific behavior without exposing licensed content.

- Write coded admitted episode inputs with illustrative, non-restricted values.
- Record the expected AR-DRG version, grouper version, coding-set version, and pricing year.
- Capture the expected admitted acute path and the NWAU-relevant output fields the test needs.
- Keep the fixture small enough that the intent is obvious from the record itself.

## Local licensed workflow

Use local licensed fixtures only when you need parity against a licensed grouper or reference dataset.

- Keep the licensed source files and raw outputs on the local machine or in another approved private location.
- Do not commit proprietary grouper outputs, restricted code tables, or redistributable source extracts unless the license explicitly allows it.
- Commit only redacted metadata, schema examples, or synthetic stand-ins that let other maintainers understand the test shape.
- If a fixture depends on a licensed reference result, document the provenance and the exact version tuple it came from, but not the proprietary payload.

## Admitted acute NWAU checks

The fixture should prove more than a grouping label.

- Assert the episode is treated as admitted acute before checking downstream NWAU behavior.
- Verify the expected AR-DRG changes when the version tuple changes.
- Verify the NWAU-relevant outputs for the matching pricing year and reject reuse when the pricing year or grouping version is incompatible.
- Keep the expected outputs scoped to the behavior under test, not to a complete exported grouper report.

## Review rule

If a fixture cannot be shared safely, keep it local and document the reason in the track notes rather than committing the proprietary output.
