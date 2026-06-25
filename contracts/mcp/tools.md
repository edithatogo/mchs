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
    "id": "acute",
    "displayName": "Acute admitted care",
    "description": "Boundary adapter for acute admitted-care calculator requests",
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
  "calculatorId": "acute",
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
  "calculatorId": "acute",
  "year": "2025-26",
  "inputs": {
    "DRG": "A01A"
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

Validate a calculation request at the MCP boundary and delegate formula execution to the canonical runtime. The MCP adapter must not duplicate calculator formula logic; current stdio responses therefore return `result: null` with an explicit delegation diagnostic unless a downstream runtime execution result is added by a later contract.

**Input:**

```json
{
  "calculatorId": "acute",
  "year": "2025-26",
  "inputs": {
    "DRG": "A01A"
  },
  "options": {
    "includeEvidence": true,
    "includeExplanation": true
  }
}
```

**Output:** A `CalculationResponse` with result, diagnostics, optional evidence/explanation.

```json
{
  "calculatorId": "acute",
  "year": "2025-26",
  "result": null,
  "diagnostics": {
    "diagnostics": [
      {
        "severity": "warning",
        "code": "MCHS-WARN-MCP-001",
        "message": "MCP server validated the request boundary. Formula execution is delegated to the canonical runtime and is not duplicated in the MCP adapter."
      }
    ],
    "summary": { "errorCount": 0, "warningCount": 1, "infoCount": 0 }
  },
  "provenance": { "server": "mchs", "transport": "stdio" }
}
```

---

## `mchs.explain_result`

Return the MCP boundary explanation for a validated request.

**Input:**

```json
{
  "calculatorId": "acute",
  "year": "2025-26",
  "inputs": {
    "DRG": "A01A"
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
