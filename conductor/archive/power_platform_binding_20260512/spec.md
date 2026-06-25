# Specification: Power Platform Binding

## Overview
Finalize Power Platform as an orchestration-only binding surface. Canvas apps, model-driven apps, flows, and custom connectors must call a shared service, managed connector, or file/API boundary and must not contain formula logic.

## Functional Requirements
- Define supported Power Platform integration modes: custom connector, Power Automate flow, service API, and managed solution packaging.
- Define request/response schemas aligned with the shared calculator contract.
- Define a calculator/pricing-year capability matrix that covers every Power
  Apps selector option and marks source-available, unsupported, blocked,
  shadow, planned, helper, and implemented combinations without overclaiming
  runtime support.
- Define environment variables, connection references, ALM, and publish requirements.
- Reuse shared fixtures through service-level tests.

## Acceptance Criteria
- Power Platform roadmap separates app orchestration from calculator execution.
- Power Apps surfaces discover calculator/year availability from the shared
  service boundary instead of hardcoding one default calculator/year.
- The source-controlled app surface model must wire selector loading,
  request validation, guarded calculation submission, and diagnostics display
  to the custom connector operations without adding formula logic.
- Managed solution publication path is documented.
- No formula logic is stored in apps or flows.
