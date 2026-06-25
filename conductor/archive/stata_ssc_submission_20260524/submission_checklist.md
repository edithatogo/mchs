# Stata SSC Submission Checklist

This checklist captures the external steps required to finish `mchs-stata-interop@0.1.0`.

## Inputs

- Package: `mchs-stata-interop`
- Version: `0.1.0`
- Local surface: `bindings/stata/`
- Prepared artifact: `bindings/stata/mchs-stata-interop-0.1.0.zip`
- Package index file: `bindings/stata/pkg-mchs.pkg`
- Current archive SHA-256: `7cd12328f7b9e061fb2fe42c72ee6812f055f64ccabb2338ef45c26cdf98ce1a`

## Required steps

1. Identify the SSC submission contact or maintainer channel for Stata package distribution. Completed: Boston College SSC archive maintainer contact `baum@bc.edu` was used.
2. Send the initial package submission with the package name, version, maintainer contact, and short description. Completed on 2026-06-12.
3. Attach or link `bindings/stata/mchs-stata-interop-0.1.0.zip`. Completed for the initial submission.
4. Include `bindings/stata/pkg-mchs.pkg` and the included ado/help/example files in the submission notes. Completed for the initial submission.
5. Record the sent date, recipient, and message identifier in the track evidence. Completed for the initial submission and maintainer-identity clarification.
6. Apply maintainer-requested changes, rebuild the archive if needed, and update the checksum evidence. Completed for the 2026-06-12 feedback requesting author contact information in `mchs.sthlp`.
7. Do not send the corrected-archive follow-up: public SSC/RePEc installability evidence was captured before any approved corrected-archive reply was needed.
8. Verify the package is installable from SSC before closing the track. Completed on 2026-06-14 via `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` on the Boston College SSC/RePEc archive.

## Evidence to record

- Submission email or message identifier
- SSC contact used for the submission
- Archive checksum
- Maintainer feedback or acceptance note
- Installability evidence from SSC/RePEc public package manifest, ado file, and help file

## Completion rule

Do not send any SSC follow-up email or corrected archive without explicit user approval of the exact outbound action. The corrected-archive follow-up is no longer needed for this track because SSC/RePEc public installability evidence has been captured. The public SSC `.pkg` metadata does not expose semantic package versions, so version `0.1.0` remains local archive evidence.
