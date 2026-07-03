# IHACPA source scanner contract fixtures

This directory contains synthetic, machine-readable fixtures for the IHACPA
source scanner contract.

## Contents

- `source-scanner.schema.json`: JSON Schema for the scanner contract bundle.
- `source-scanner.contract.json`: Contract document describing the scanner
  surface, source categories, and output formats.
- `examples/dry-run.scan.json`: Synthetic dry-run discovery report.
- `examples/add-year.draft-manifest.json`: Synthetic draft manifest produced by
  an add-year workflow.

## Scope

These files are fixtures only. They are intentionally small and do not contain
live discovery output, downloaded artifacts, or proprietary source material.

Use them to exercise parsing, review workflows, and contract checks without
depending on network access or current IHACPA release availability.

## Rules

- Keep the examples synthetic.
- Do not add patient-level data, private documents, or live archive payloads.
- Do not treat these files as authoritative source data.

The scanner contract also includes a review-only `sources audit` surface that
packages source-scanner results into draft manifest, Conductor track, and
GitHub issue text for offline review.
