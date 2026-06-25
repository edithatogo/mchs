# Specification: HTTP API Contract

## Overview

Define a domain-specific HTTP API for calculator execution, validation,
schemas, jobs, and evidence. The API must be OpenAPI 3.1 and generated from or
validated against canonical schemas.

## Requirements

- Define `GET /v1/calculators`.
- Define `GET /v1/calculators/{calculator_id}`.
- Define `GET /v1/schemas/{schema_name}`.
- Define `POST /v1/validate`.
- Define `POST /v1/calculations`.
- Define async job endpoints.
- Define evidence endpoints.
- Reuse canonical diagnostics, errors, and provenance.

## Acceptance Criteria

- OpenAPI 3.1 contract exists and validates.
- API examples include sync, async, pass, and fail cases.
- API docs state that the domain API is canonical for HTTP, not OpenAI-compatible by default.
