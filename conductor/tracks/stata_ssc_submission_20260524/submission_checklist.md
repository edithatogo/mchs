# Stata SSC Submission Checklist

This checklist captures the evidence and follow-up rules for the `mchs@0.1.0`
Stata SSC publication gate.

## Inputs

- Package: `mchs`
- Version: `0.1.0`
- Local surface: `bindings/stata/`
- Prepared artifact: `bindings/stata/mchs-stata-interop-0.1.0.zip`
- Package index file: `bindings/stata/pkg-mchs.pkg`
- Public SSC package file: `http://fmwww.bc.edu/repec/bocode/m/mchs.pkg`
- Public SSC ado file: `http://fmwww.bc.edu/repec/bocode/m/mchs.ado`
- Public SSC help file: `http://fmwww.bc.edu/repec/bocode/m/mchs.sthlp`

## Required verification steps

1. Probe the public SSC/RePEc URLs for `mchs.pkg`, `mchs.ado`, and `mchs.sthlp`.
2. Verify `mchs.pkg` contains the expected package metadata and distribution date.
3. Record the probe status, timestamps, and any maintainer feedback in the track evidence.
4. If SSC requests changes, rebuild the archive, update checksum evidence, and repeat the public probe after publication.
5. Do not send maintainer email or follow-up correspondence without explicit approval of the final recipient, subject, and body immediately before sending.

## Evidence to record

- Archive checksum
- Maintainer feedback or acceptance note
- Installability evidence from SSC
- Public `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` probe results

## Completion rule

Do not mark the track complete until SSC has accepted the submission or the package is otherwise verified as installable from SSC. Any future email follow-up remains explicit-approval gated.
