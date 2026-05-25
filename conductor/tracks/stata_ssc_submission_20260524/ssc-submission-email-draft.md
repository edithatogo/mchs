# SSC submission email draft for `mchs`

This is a draft only. Do not send it without author approval from the account that should be listed as the SSC package submitter.

To: `baum@bc.edu`

Subject: New SSC submission: mchs

Body:

```text
Dear Professor Baum,

I would like to submit a new Stata package to the SSC archive.

Suggested package name: mchs

Title line:
MCHS Stata file/CLI interop adapter

Description:
mchs provides a thin Stata adapter for MCHS/NWAU health-economics workflows. It supports importing shared-core CSV outputs into Stata, invoking the external shared-core CLI through Stata's shell boundary, and validating required provenance columns on imported outputs. It does not implement calculator formula logic in Stata; all calculations are delegated to the external shared-core CLI/file boundary.

Version: 0.1.0

Files included in the attached zip:
- mchs.ado
- mchs.sthlp

Repository:
https://github.com/edithatogo/mchs

Prepared bundle:
bindings/stata/mchs-stata-interop-0.1.0-ssc.zip

SHA-256:
ae0b0adf12aba71dc4e844282bbfcd88bd09b2fd2c2237f565cbc1cfe9d8f225

Runtime note:
The package has been prepared from the repository ado/help/pkg sources, but the repository environment used for packaging did not include a Stata executable, so no Stata runtime validation is claimed in the repository evidence.

Best regards,
Dylan Mordaunt
```

Attachment:

- `bindings/stata/mchs-stata-interop-0.1.0-ssc.zip`
