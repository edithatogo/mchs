# Specification: FFI Safety Review

## Overview

Harden Rust FFI/C ABI boundaries after Cline finishes implementation.

## Requirements

- Replace unchecked UTF-8 conversion with checked conversion.
- Validate pointer, length, and nullability assumptions.
- Define explicit ABI error statuses for invalid UTF-8 and invalid lengths.
- Document ownership and lifetime rules.
- Add tests for invalid pointers where safe to simulate, invalid UTF-8, null
  inputs, and valid calls.

## Acceptance Criteria

- No unchecked conversion of caller-provided string data remains.
- ABI status codes are documented and tested.
- C ABI remains a thin implementation boundary, not standalone C product
  support.
