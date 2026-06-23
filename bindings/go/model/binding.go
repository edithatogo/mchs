package model

// BindingMode identifies the transport boundary used by a binding request.
type BindingMode string

const (
	BindingModeService   BindingMode = "service"
	BindingModeCLI       BindingMode = "cli"
	BindingModeArrowFile BindingMode = "arrow-file"
)

// GoBindingRequest is the versioned request envelope described by the Go
// binding contract. It carries transport metadata only; calculation remains in
// the shared core or service reached through the selected boundary.
type GoBindingRequest struct {
	SchemaVersion       string            `json:"schema_version"`
	CalculatorID        string            `json:"calculator_id"`
	PricingYear         string            `json:"pricing_year"`
	InputSchemaVersion  string            `json:"input_schema_version"`
	OutputSchemaVersion string            `json:"output_schema_version"`
	Mode                BindingMode       `json:"mode"`
	InputPath           string            `json:"input_path,omitempty"`
	OutputPath          string            `json:"output_path,omitempty"`
	ServiceURL          string            `json:"service_url,omitempty"`
	ArrowInputPath      string            `json:"arrow_input_path,omitempty"`
	ArrowOutputPath     string            `json:"arrow_output_path,omitempty"`
	CorrelationID       string            `json:"correlation_id,omitempty"`
	Metadata            map[string]string `json:"metadata,omitempty"`
	FixtureGate         string            `json:"fixture_gate"`
}

// GoBindingResponse is the versioned response envelope emitted by a concrete
// transport adapter.
type GoBindingResponse struct {
	SchemaVersion        string         `json:"schema_version"`
	CalculatorID         string         `json:"calculator_id"`
	PricingYear          string         `json:"pricing_year"`
	Mode                 BindingMode    `json:"mode"`
	Success              bool           `json:"success"`
	Status               string         `json:"status"`
	Message              string         `json:"message"`
	Warnings             []string       `json:"warnings,omitempty"`
	Errors               []BindingError `json:"errors,omitempty"`
	Diagnostics          Diagnostics    `json:"diagnostics"`
	Provenance           Provenance     `json:"provenance"`
	ServiceURL           string         `json:"service_url,omitempty"`
	OutputPath           string         `json:"output_path,omitempty"`
	ArrowOutputPath      string         `json:"arrow_output_path,omitempty"`
	FixtureGateState     string         `json:"fixture_gate_state"`
	ModuleReadinessState string         `json:"module_readiness_state"`
}

// BindingError is a machine-readable failure record.
type BindingError struct {
	Code      string `json:"code"`
	Severity  string `json:"severity"`
	Retryable bool   `json:"retryable"`
	Condition string `json:"condition"`
	Message   string `json:"message"`
}

// Diagnostics captures adapter-level pass, fail, and blocked checks.
type Diagnostics struct {
	Status  string            `json:"status"`
	Checks  []DiagnosticCheck `json:"checks"`
	Summary DiagnosticSummary `json:"summary"`
	Notes   string            `json:"notes,omitempty"`
}

// DiagnosticCheck is one named boundary check.
type DiagnosticCheck struct {
	ID      string `json:"id"`
	Status  string `json:"status"`
	Message string `json:"message"`
}

// DiagnosticSummary aggregates diagnostic outcomes.
type DiagnosticSummary struct {
	Passed  int `json:"passed"`
	Failed  int `json:"failed"`
	Blocked int `json:"blocked"`
}

// Provenance records where an adapter result came from.
type Provenance struct {
	Command            string `json:"command"`
	BindingBundleID    string `json:"binding_bundle_id"`
	SourceManifestPath string `json:"source_manifest_path"`
	SourceURL          string `json:"source_url"`
	RetrievedOn        string `json:"retrieved_on"`
	SHA256             string `json:"sha256"`
	Bytes              int64  `json:"bytes"`
	ChecksumAlgorithm  string `json:"checksum_algorithm"`
}
