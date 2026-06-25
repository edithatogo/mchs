# Specification: Swift Binding

## Overview
Define a Swift integration roadmap for Apple-platform and native client
consumers. Swift should consume the shared core through C ABI, service, or
file/Arrow boundaries and must not duplicate formula logic.

## Functional Requirements
- Compare Swift C ABI, service, and file/Arrow interop.
- Define Swift request/response models, diagnostics, provenance, and fixture gates.
- Document Swift Package Manager publication only after parity and platform gates pass.

## Acceptance Criteria
- Swift strategy is selected and documented.
- Swift examples validate against shared fixtures.
- Formula logic remains single-sourced outside Swift adapters.
