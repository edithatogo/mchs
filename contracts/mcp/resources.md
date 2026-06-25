# MCHS MCP Resources

MCP Resources provide read-only access to schemas, support status, and evidence data.

## URI Scheme

All MCHS resources use the `mchs://` URI scheme.

| URI Template | Description |
|---|---|
| `mchs://schemas` | List all available canonical schemas |
| `mchs://schemas/{schemaId}` | Fetch a specific canonical schema by ID |
| `mchs://schemas/inputs/{calculatorId}` | Fetch the input schema for a calculator |
| `mchs://schemas/outputs` | Fetch the base output schema |
| `mchs://support/streams` | List all streams with support status |
| `mchs://support/streams/{stream}` | Get support status for a specific stream |
| `mchs://support/years` | List all supported years |
| `mchs://support/years/{year}` | Get support status for a specific year |
| `mchs://evidence/{bundleId}` | Fetch a specific evidence bundle |
| `mchs://calculators` | List all calculators |
| `mchs://calculators/{calculatorId}` | Get a specific calculator definition |

## Resource Definitions

### Schema Resources

`mchs://schemas/{schemaId}`

Returns a JSON Schema document. Valid schema IDs:

| ID | Schema |
|---|---|
| `calculator` | `calculator.schema.json` |
| `diagnostics` | `diagnostics.schema.json` |
| `provenance` | `provenance.schema.json` |
| `support-status` | `support-status.schema.json` |
| `evidence` | `evidence.schema.json` |

**Example response:**

```
Content-Type: application/json
mchs-resource-uri: mchs://schemas/calculator

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://mchs.example.org/schemas/calculator.json",
  "title": "Calculator",
  ...
}
```

### Support Status Resources

`mchs://support/streams`

Returns an array of `SupportStatus` objects for all stream/year combinations.

`mchs://support/years`

Returns an array of supported year strings.

### Evidence Resources

`mchs://evidence/{bundleId}`

Returns an `EvidenceBundle` object. For the current stdio MCP boundary, evidence bundles describe contract, release, support-scope, and publication evidence; calculation responses do not imply that formula execution occurred inside the MCP adapter.

## Resource Discovery

MCP clients can discover all available resources by querying the standard MCP `resources/list` endpoint. The server responds with the full list of resource templates and their descriptions.

## Caching

Resources are cached according to standard HTTP caching semantics. The `mchs-resource-version` header can be used for cache invalidation. Schema resources are immutable within a schema version.
