# Strategy: IHACPA Source Scanner

## Contract

The track implements a conservative source-discovery surface under the installed
CLI entrypoint:

- `funding-calculator sources scan`
- `funding-calculator sources add-year <year>`

The scanner accepts checked-in HTML/text fixtures and explicit URLs. It does not
perform live downloads, does not commit source artifacts, and does not claim
calculator parity.

## Implementation posture

- Keep CI offline and deterministic.
- Treat external-hosted or filename-less links as explicit gaps.
- Emit discovery manifests that are review material, not release evidence.
- Preserve the distinction between source discovery, parameter extraction, and
validated calculator support.

## Review outcome

The initial parallel implementation created the scanner, docs, contract
fixtures, and parser tests. Review identified one contract drift issue: docs and
fixtures used an undocumented `nwau` command name while the package exposes
`funding-calculator`. The integration phase resolved the drift by making the
installed entrypoint explicit everywhere.
