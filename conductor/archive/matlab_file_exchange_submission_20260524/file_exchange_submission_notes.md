# MATLAB File Exchange submission notes

Submission URL: https://www.mathworks.com/matlabcentral/fileexchange/

## Package details

- Name: MCHS MATLAB Interop
- Version: 0.1.0
- License: MIT
- Repository: https://github.com/edithatogo/mchs
- Upload archive: bindings/matlab/mchs-matlab-interop-0.1.0.zip
- Original uploaded archive SHA-256: 1156f506cda8ab797b5d07adebc35ecccb36bd9758cffaf011029c71c9d2515a
- Corrected local archive SHA-256: d78cc11a9ab23080b38604e21c5d21ba9c8801ae0cf6219888f1797834cf2336

## Summary

MATLAB file and CLI boundary helpers for MCHS shared-core outputs.

## Description

MCHS MATLAB Interop provides lightweight MATLAB helper functions and examples for working with MCHS/NWAU shared-core outputs through file and command-line boundaries. The package includes CSV/table import helpers, CLI invocation helpers, input validation scaffolding, examples, README, and MIT license metadata.

This package intentionally does not reimplement pricing or clinical formula logic in MATLAB. It is an interop layer for workflows that exchange files or invoke the external CLI/shared-core tooling.

## Suggested tags

- health economics
- microcosting
- matlab
- csv
- parquet
- cli

## Included files

- README.md
- LICENSE
- file-exchange-submission.json
- matlab-interop-notes.md
- mchs/README.md
- mchs/importResultTable.m
- mchs/invokeCli.m
- mchs/validateInput.m
- examples/cli_invocation_demo.m
- examples/file_import_demo.m

## Runtime note

MATLAB and Octave are not installed on the current validation machine, so no MATLAB runtime validation is claimed in the project evidence. The submission should be reviewed in a MATLAB session before or during File Exchange upload if the publisher account requires runtime screenshots or examples.
