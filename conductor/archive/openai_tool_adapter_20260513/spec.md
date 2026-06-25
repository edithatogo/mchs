# Specification: OpenAI Tool Adapter

## Overview

Create an OpenAI-compatible tool adapter over the canonical API/MCP contracts.
The calculator should not pretend to be an OpenAI model endpoint. OpenAI
compatibility means generated tool definitions and examples that route through
the canonical calculator API or MCP server.

## Requirements

- Generate tool definitions from canonical schemas.
- Provide examples for Responses-style tool use.
- Keep prompts and model orchestration outside the calculator core.
- Avoid `/v1/chat/completions` or `/v1/responses` compatibility claims for the
  calculator service itself.
- Preserve diagnostics, errors, provenance, and support status in tool outputs.

## Acceptance Criteria

- Tool definitions are contract-tested against canonical schemas.
- Documentation explains the difference between domain API, MCP, and OpenAI
  adapter.
- The adapter contains no formula logic and no model-specific business rules.
