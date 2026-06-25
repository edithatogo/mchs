# Specification: NSW Funding Model

## Overview

Create a NSW-specific funding model registry. NSW must be explicit because NSW
service agreement material publishes a State Price per NWAU and uses district
and network return costing bases.

## Requirements

- Source NSW State Price by financial year.
- Capture source terminology such as NWAU25 and State Price.
- Capture Local Health District and Specialty Health Network applicability where
  public sources identify it.
- Capture adjustments, excluded activity, block-funded services, and local
  notes where available.
- Map NSW NWAU source terminology to the generic HWAU abstraction.
- Record source URL/path, retrieved date, checksum, licence, and support status.

## Acceptance Criteria

- NSW model schema exists.
- At least one public-safe NSW source fixture exists.
- Missing years are marked blocked or unknown rather than inferred.
- NSW price application can run in parallel with national, local, and
  discounted valuations.
