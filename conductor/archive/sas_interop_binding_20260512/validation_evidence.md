# SAS Interop Validation Evidence

This track resolves scaffold ambiguity by classifying SAS interoperability as
private/no-new-development.

## Evidence checked

- No public `bindings/sas` or `contracts/sas-interop-binding` surface is part
  of this track.
- Archived SAS material is treated as reference input only and is not edited by
  this track.
- Public SAS-adjacent exchange must use the shared CLI/file contract.
- Any SAS comparison report must be produced locally from licensed reference
  outputs or from synthetic fixtures.

## Claims this track does not make

- No public SAS adapter is adapter-ready.
- No SAS package, registry, or publication surface exists.
- No SAS source code, macro code, or formula logic is copied into this track.
- No pricing year has SAS parity unless a separate, provenance-backed
  comparison report exists for that year.

## Focused validation

The focused guard test is `tests/test_sas_interop_binding_track.py`. It checks
the metadata reclassification, documentation guardrails, private publication
status, and absence of public adapter claims.
