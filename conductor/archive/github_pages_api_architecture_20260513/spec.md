# Specification: GitHub Pages API Architecture

## Overview

Clarify how GitHub Pages, TypeScript/WASM, and the HTTP API fit together.
GitHub Pages can host docs and static demos; it cannot run the API backend.

## Requirements

- Document docs-only, static WASM, external API, and local API modes.
- Prevent claims that GitHub Pages hosts a production API backend.
- Keep API examples honest about hosted or local execution.
- Keep optional TypeScript/WASM as a static web surface.

## Acceptance Criteria

- Architecture note exists.
- Docs distinguish static GitHub Pages from API hosting.
- API-backed demos require explicit backend mode.
