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
- pkg-mchs.pkg

Repository:
https://github.com/edithatogo/mchs

Prepared bundle:
bindings/stata/mchs-stata-interop-0.1.0.zip

SHA-256:
ba2bb2b43b92c8eda0b20ee7f7de888e69be8e2a0abd3480100db6a216ec6bb2

Runtime note:
The package has been prepared from the repository ado/help/pkg sources, but the repository environment used for packaging did not include a Stata executable, so no Stata runtime validation is claimed in the repository evidence.

Best regards,
[submitter name]
```

Attachment:

- `bindings/stata/mchs-stata-interop-0.1.0.zip`
