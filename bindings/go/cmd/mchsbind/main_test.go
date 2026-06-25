package main

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/edithatogo/mchs/bindings/go/model"
)

func TestRunExecuteUsesServiceBoundary(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var request model.GoBindingRequest
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			t.Fatalf("decode request: %v", err)
		}
		response := model.GoBindingResponse{
			SchemaVersion: request.SchemaVersion,
			CalculatorID:  request.CalculatorID,
			PricingYear:   request.PricingYear,
			Mode:          model.BindingModeService,
			Success:       true,
			Status:        "pass",
			Message:       "Service boundary returned a contract response.",
			Diagnostics: model.Diagnostics{
				Status:  "pass",
				Checks:  []model.DiagnosticCheck{{ID: "service_boundary", Status: "pass", Message: "ok"}},
				Summary: model.DiagnosticSummary{Passed: 1},
			},
			Provenance: model.Provenance{
				Command:            "mchsbind execute",
				BindingBundleID:    "go_binding_contract_20260513",
				SourceManifestPath: "contracts/go-binding/examples/service.pass.json",
				SourceURL:          "https://example.invalid/contracts/go-binding",
				RetrievedOn:        "2026-05-13",
				SHA256:             "synthetic-sha256-go-binding-cli-test",
				Bytes:              1,
				ChecksumAlgorithm:  "sha256",
			},
			ServiceURL:           request.ServiceURL,
			FixtureGateState:     "pass",
			ModuleReadinessState: "ready",
		}
		if err := json.NewEncoder(w).Encode(response); err != nil {
			t.Fatalf("encode response: %v", err)
		}
	}))
	defer server.Close()

	stdin := bytes.NewBufferString(`{
  "schema_version": "1.0",
  "calculator_id": "acute",
  "pricing_year": "2025",
  "input_schema_version": "1.0",
  "output_schema_version": "1.0",
  "mode": "service",
  "service_url": "` + server.URL + `",
  "fixture_gate": "synthetic_only_examples"
}`)
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	err := run(context.Background(), []string{"execute", "--request", "-", "--output", "-"}, stdin, &stdout, &stderr)
	if err != nil {
		t.Fatalf("run execute error = %v; stderr = %s", err, stderr.String())
	}

	var response model.GoBindingResponse
	if err := json.Unmarshal(stdout.Bytes(), &response); err != nil {
		t.Fatalf("decode stdout: %v", err)
	}
	if response.Status != "pass" {
		t.Fatalf("response.Status = %q, want pass", response.Status)
	}
}
