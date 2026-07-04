# MCHS MCP Tools

All tools follow the Model Context Protocol (MCP) specification. Tool inputs and outputs conform to the canonical JSON Schemas.

---

## `mchs.list_calculators`

List available micro-costing calculators.

**Input:**

```json
{
  "stream": "admitted_acute",
  "year": "2025-26",
  "includeDeprecated": false
}
```

All parameters are optional. If omitted, returns all calculators.

**Output:** Array of `Calculator` objects conforming to `calculator.schema.json`.

```json
[
  {
    "id": "icu-bed-day",
    "displayName": "ICU Bed-Day",
    "description": "Calculates the micro-cost of a single ICU bed-day",
    "version": "1.2.0",
    "supportedStreams": ["admitted_acute"],
    "supportedYears": ["2025-26", "2026-27"],
    "inputSchema": { "$ref": "...", "format": "json-schema" },
    "outputSchema": { "$ref": "...", "format": "json-schema" }
  }
]
```

---

## `mchs.get_schema`

Retrieve the JSON Schema for a calculator's inputs or outputs.

**Input:**

```json
{
  "calculatorId": "icu-bed-day",
  "direction": "input"
}
```

| Parameter | Required | Default | Description |
|---|---|---|---|
| `calculatorId` | Yes | — | Calculator identifier |
| `direction` | No | `input` | `input` or `output` |

**Output:** A JSON Schema document (object).

---

## `mchs.validate_input`

Validate input data against a calculator's input schema without executing a calculation.

**Input:**

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "inputs": {
    "age": 65,
    "drgCode": "A01A",
    "losDays": 4,
    "ventilatorHours": 12,
    "admissionType": "emergency"
  }
}
```

**Output:** A `ValidationResponse` with `valid` boolean and `diagnostics`.

```json
{
  "valid": true,
  "diagnostics": {
    "diagnostics": [
      {
        "severity": "info",
        "code": "MCHS-INF-001",
        "message": "Input validated successfully"
      }
    ],
    "summary": { "errorCount": 0, "warningCount": 0, "infoCount": 1 }
  }
}
```

---

## `mchs.calculate`

Run a micro-costing calculation.

**Input:**

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "inputs": {
    "age": 65,
    "drgCode": "A01A",
    "losDays": 4,
    "ventilatorHours": 12,
    "admissionType": "emergency"
  },
  "options": {
    "runtime": "rust",
    "refDir": "tests/data/2025",
    "includeEvidence": true,
    "includeExplanation": true
  }
}
```

**Output:** A `CalculationResponse` with result, diagnostics, optional evidence/explanation.

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "result": {
    "totalCost": 4520.75,
    "costBreakdown": { "nursing": 2100.00, "medical": 875.50 },
    "nwau": 4.85,
    "currency": "AUD"
  },
  "diagnostics": { "diagnostics": [], "summary": { "errorCount": 0, "warningCount": 0, "infoCount": 1 } },
  "evidence": { "bundleId": "evb-...", "calculatorId": "icu-bed-day", "references": [], "costWeightVersion": "CW-2025-v2" },
  "explanation": {
    "calculatorId": "icu-bed-day",
    "year": "2025-26",
    "steps": [
      { "step": 1, "label": "Identify AR-DRG weight", "description": "...", "value": "4.85" }
    ]
  }
}
```

Runtime selection is bounded during the Rust migration:

- missing `options.runtime`, `python`, and `auto` preserve Python/default MCP
  compatibility behaviour;
- `rust` is supported only for `calculatorId = "acute"` and `year = "2025"`;
- unsupported Rust requests fail closed with `MCHS-MCP-RUST-UNSUPPORTED`;
- unavailable local Rust extensions fail closed with `MCHS-MCP-RUST-UNAVAILABLE`.

The `mchs-mcp` stdio process may still be launched by Python during this
transition. That is a transport shim, not a claim that Python owns formula
runtime for promoted Rust-backed requests.

---

## `mchs.explain_result`

Return a step-by-step explanation of how a result would be computed for given inputs.

**Input:**

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "inputs": {
    "age": 65,
    "drgCode": "A01A",
    "losDays": 4,
    "ventilatorHours": 12,
    "admissionType": "emergency"
  }
}
```

**Output:** An `ExplainResponse` with ordered explanation steps.

---

## `mchs.get_evidence`

Retrieve an evidence bundle by its bundle ID.

**Input:**

```json
{
  "bundleId": "evb-icu-2025-q2"
}
```

**Output:** An `EvidenceBundle` object conforming to `evidence.schema.json`.

---

## Error Handling

All tools return errors in the following format on failure:

```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "Error MCHS-ERR-VAL-001: Field 'age' value 999 exceeds maximum allowed value of 130"
    }
  ]
}
```

Standard MCP error codes are used for transport-level issues. Domain errors use MCHS diagnostic codes.
