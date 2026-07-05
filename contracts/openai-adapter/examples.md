# OpenAI Adapter Usage Examples

These examples show how to use the MCHS tools with the OpenAI Responses API and Chat Completions API.

## Example 1: List Calculators (Responses API)

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    tools=[...],  # MCHS tool definitions
    input="What micro-costing calculators are available for admitted_acute in 2025-26?"
)

# The model will call:
# list_calculators({ "stream": "admitted_acute", "year": "2025-26" })
```

**Tool call arguments sent:**

```json
{
  "stream": "admitted_acute",
  "year": "2025-26"
}
```

**Tool response:**

```json
[
  {
    "id": "icu-bed-day",
    "displayName": "ICU Bed-Day",
    "description": "Calculates the micro-cost of a single ICU bed-day",
    "version": "1.2.0",
    "supportedStreams": ["admitted_acute"],
    "supportedYears": ["2025-26", "2026-27"],
    "inputSchema": { "$ref": "https://mchs.example.org/schemas/inputs/icu-bed-day.json", "format": "json-schema" },
    "outputSchema": { "$ref": "https://mchs.example.org/schemas/outputs/cost-result.json", "format": "json-schema" }
  },
  {
    "id": "chemotherapy-cycle",
    "displayName": "Chemotherapy Cycle",
    "description": "Calculates the micro-cost of a chemotherapy cycle",
    "version": "1.0.0",
    "supportedStreams": ["admitted_acute", "outpatient_clinic"],
    "supportedYears": ["2025-26"],
    "inputSchema": { "$ref": "https://mchs.example.org/schemas/inputs/chemotherapy-cycle.json", "format": "json-schema" },
    "outputSchema": { "$ref": "https://mchs.example.org/schemas/outputs/cost-result.json", "format": "json-schema" }
  }
]
```

---

## Example 2: Validate Input (Chat Completions API)

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Validate these ICU inputs: age 65, DRG A01A, 4 days LOS"}],
    tools=[...],  # MCHS tool definitions
    tool_choice="auto"
)
```

**Tool call arguments sent:**

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "inputs": {
    "age": 65,
    "drgCode": "A01A",
    "losDays": 4,
    "ventilatorHours": 0,
    "admissionType": "elective"
  }
}
```

**Tool response (pass):**

```json
{
  "valid": true,
  "diagnostics": {
    "diagnostics": [
      { "severity": "info", "code": "MCHS-INF-001", "message": "Input validated successfully" }
    ],
    "summary": { "errorCount": 0, "warningCount": 0, "infoCount": 1 }
  }
}
```

---

## Example 3: Run Calculation with Explanation

```python
response = client.responses.create(
    model="gpt-4o",
    tools=[...],
    input="What's the micro-cost of a 4-day ICU stay for a 65yo with DRG A01A?",
    tool_choice={"type": "function", "name": "calculate"}
)
```

**Tool call arguments sent:**

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
  "includeExplanation": true
}
```

**Tool response (abbreviated):**

```json
{
  "calculatorId": "icu-bed-day",
  "year": "2025-26",
  "result": {
    "totalCost": 4520.75,
    "costBreakdown": { "nursing": 2100.00, "medical": 875.50, "consumables": 345.25, "overhead": 1200.00 },
    "hwau": 4.85,
    "nwau": 4.85,
    "currency": "AUD"
  },
  "diagnostics": { "diagnostics": [{ "severity": "info", "code": "MCHS-INF-001", "message": "Calculation completed successfully" }], "summary": { "errorCount": 0, "warningCount": 0, "infoCount": 1 } },
  "explanation": {
    "calculatorId": "icu-bed-day",
    "year": "2025-26",
    "steps": [
      { "step": 1, "label": "Identify AR-DRG weight", "description": "Lookup NWAU weight for AR-DRG A01A in 2025-26 schedule", "value": "4.85" },
      { "step": 2, "label": "Adjust for length of stay", "description": "Apply LOS adjustment factor of 1.15 for 4-day stay", "value": "5.58" },
      { "step": 3, "label": "Apply ventilator modifier", "description": "Add ventilator hourly surcharge of $45.50 for 12 hours", "value": "$546.00" },
      { "step": 6, "label": "Compute final total", "description": "Sum base cost, ventilator surcharge, and overhead", "value": "$4,520.75" }
    ]
  }
}
```

The calculation result exposes generic HWAU as `hwau` and preserves Australian
NWAU source terminology as the compatible `nwau` alias.

---

## Example 4: Error Handling — Calculator Not Found

```python
# Tool call to non-existent calculator
response = client.responses.create(
    model="gpt-4o",
    tools=[...],
    input="Run calculation for 'non-existent' calculator"
)
```

**Tool response (error):**

```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "Error MCHS-ERR-NOTFOUND-001: Calculator 'non-existent' not found. Use list_calculators to see available calculators."
    }
  ]
}
```

---

## Example 5: Evidence Retrieval

```python
response = client.responses.create(
    model="gpt-4o",
    tools=[...],
    input="Get the evidence bundle for evb-icu-2025-q2"
)
```

**Tool call arguments:**

```json
{
  "bundleId": "evb-icu-2025-q2"
}
```

**Tool response (abbreviated):**

```json
{
  "bundleId": "evb-icu-2025-q2",
  "calculatorId": "icu-bed-day",
  "references": [
    { "id": "ref-nwa-2025-table-4.2", "type": "cost_weight", "title": "NWAU Schedule 2025-26, Table 4.2" }
  ],
  "costWeightVersion": "CW-2025-v2",
  "dataSources": [{ "name": "IHACPA NWAU Schedule", "version": "2025-26" }],
  "assumptions": [{ "key": "nurse-patient-ratio", "description": "Nurse-to-patient ratio", "value": "1:1" }]
}
```
