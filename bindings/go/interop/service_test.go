package interop

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/edithatogo/mchs/bindings/go/model"
)

func TestServiceAdapterExecutePostsContractEnvelope(t *testing.T) {
	var seenCorrelationID string
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Fatalf("method = %s, want POST", r.Method)
		}
		seenCorrelationID = r.Header.Get("X-Correlation-ID")

		var request model.GoBindingRequest
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			t.Fatalf("decode request: %v", err)
		}
		if request.CalculatorID != "acute" {
			t.Fatalf("CalculatorID = %q, want acute", request.CalculatorID)
		}

		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(serviceResponse(request.CalculatorID, request.PricingYear, request.ServiceURL)); err != nil {
			t.Fatalf("encode response: %v", err)
		}
	}))
	defer server.Close()

	request := validServiceRequest(server.URL)
	response, err := (ServiceAdapter{Client: server.Client()}).Execute(context.Background(), request)
	if err != nil {
		t.Fatalf("Execute() error = %v", err)
	}
	if !response.Success {
		t.Fatal("response.Success = false, want true")
	}
	if response.Mode != model.BindingModeService {
		t.Fatalf("response.Mode = %q, want service", response.Mode)
	}
	if seenCorrelationID != request.CorrelationID {
		t.Fatalf("correlation header = %q, want %q", seenCorrelationID, request.CorrelationID)
	}
}

func TestServiceAdapterRejectsNonServiceMode(t *testing.T) {
	request := validServiceRequest("https://calculator.local/v1/execute")
	request.Mode = model.BindingModeArrowFile

	_, err := (ServiceAdapter{}).Execute(context.Background(), request)
	if err == nil {
		t.Fatal("Execute() error = nil, want validation error")
	}
}

func TestValidateServiceResponseChecksEchoFields(t *testing.T) {
	request := validServiceRequest("https://calculator.local/v1/execute")
	response := serviceResponse("ed", request.PricingYear, request.ServiceURL)

	if err := ValidateServiceResponse(request, response); err == nil {
		t.Fatal("ValidateServiceResponse() error = nil, want mismatch error")
	}
}

func validServiceRequest(serviceURL string) *model.GoBindingRequest {
	return &model.GoBindingRequest{
		SchemaVersion:       "1.0",
		CalculatorID:        "acute",
		PricingYear:         "2025",
		InputSchemaVersion:  "1.0",
		OutputSchemaVersion: "1.0",
		Mode:                model.BindingModeService,
		ServiceURL:          serviceURL,
		CorrelationID:       "go-binding-service-test",
		Metadata:            map[string]string{"source": "synthetic"},
		FixtureGate:         "synthetic_only_examples",
	}
}

func serviceResponse(calculatorID, pricingYear, serviceURL string) *model.GoBindingResponse {
	return &model.GoBindingResponse{
		SchemaVersion: "1.0",
		CalculatorID:  calculatorID,
		PricingYear:   pricingYear,
		Mode:          model.BindingModeService,
		Success:       true,
		Status:        "pass",
		Message:       "Service-bound request completed by shared core boundary.",
		Diagnostics: model.Diagnostics{
			Status: "pass",
			Checks: []model.DiagnosticCheck{
				{ID: "service_boundary", Status: "pass", Message: "Service boundary returned a contract response."},
			},
			Summary: model.DiagnosticSummary{Passed: 1},
		},
		Provenance: model.Provenance{
			Command:            "mchsbind execute",
			BindingBundleID:    "go_binding_contract_20260513",
			SourceManifestPath: "contracts/go-binding/examples/service.pass.json",
			SourceURL:          "https://example.invalid/contracts/go-binding",
			RetrievedOn:        "2026-05-13",
			SHA256:             "synthetic-sha256-go-binding-service-test",
			Bytes:              1,
			ChecksumAlgorithm:  "sha256",
		},
		ServiceURL:           serviceURL,
		FixtureGateState:     "pass",
		ModuleReadinessState: "ready",
	}
}

func writeTestFile(path string, data []byte) error {
	return os.WriteFile(path, data, 0o644)
}
