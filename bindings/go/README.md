# Go bindings

This directory contains a synthetic, non-published Go module used as a
prototype binding surface.

Scope:

- Typed spreadsheet-shaped structs
- A file interop adapter boundary
- Typed Go binding request and response envelopes
- A service adapter that posts contract envelopes to a shared calculator
  endpoint
- A small CLI that round-trips model data and can execute service-bound
  binding requests

Out of scope:

- Formula parsing
- Formula evaluation
- Spreadsheet calculation semantics
- Repo-wide build or release wiring

## Layout

- `model/`: typed data structures
- `interop/`: file adapter abstraction, JSON-backed implementation, and
  service adapter
- `cmd/mchsbind/`: CLI entrypoint

## Usage

```bash
cd bindings/go
go run ./cmd/mchsbind load --path ./sample.json
go run ./cmd/mchsbind save --path ./sample.json < ./input.json
go run ./cmd/mchsbind execute --request ./service-request.json --output ./response.json
```

The `execute` command currently supports the service transport mode. It
validates the binding envelope, posts it to the configured `service_url`, and
writes the contract response without computing or mutating calculator results in
Go.
