package interop

import (
	"context"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/edithatogo/mchs/bindings/go/model"
)

func TestBindingFileAdapterRoundTripsRequestAndResponse(t *testing.T) {
	ctx := context.Background()
	dir := t.TempDir()
	adapter := BindingFileAdapter{Root: dir}
	requestPath := "request.json"
	responsePath := "response.json"

	response := serviceResponse("acute", "2025", "https://calculator.local/v1/execute")
	if err := adapter.SaveResponse(ctx, responsePath, response); err != nil {
		t.Fatalf("SaveResponse() error = %v", err)
	}

	requestJSON := []byte(`{
  "schema_version": "1.0",
  "calculator_id": "acute",
  "pricing_year": "2025",
  "input_schema_version": "1.0",
  "output_schema_version": "1.0",
  "mode": "service",
  "service_url": "https://calculator.local/v1/execute",
  "fixture_gate": "synthetic_only_examples"
}`)
	if err := writeTestFile(filepath.Join(dir, requestPath), requestJSON); err != nil {
		t.Fatalf("write request fixture: %v", err)
	}

	request, err := adapter.LoadRequest(ctx, requestPath)
	if err != nil {
		t.Fatalf("LoadRequest() error = %v", err)
	}
	if request.Mode != model.BindingModeService {
		t.Fatalf("Mode = %q, want %q", request.Mode, model.BindingModeService)
	}
	if request.CalculatorID != "acute" {
		t.Fatalf("CalculatorID = %q, want acute", request.CalculatorID)
	}
}

func TestBindingFileAdapterRejectsPathEscapes(t *testing.T) {
	ctx := context.Background()
	root := t.TempDir()
	outside := t.TempDir()
	adapter := BindingFileAdapter{Root: root}
	response := serviceResponse("acute", "2025", "https://calculator.local/v1/execute")

	cases := []string{
		filepath.Join(outside, "response.json"),
		filepath.Join("..", filepath.Base(outside), "response.json"),
	}
	for _, path := range cases {
		err := adapter.SaveResponse(ctx, path, response)
		if err == nil || !strings.Contains(err.Error(), "escapes configured root") {
			t.Fatalf("SaveResponse(%q) error = %v, want root escape error", path, err)
		}
	}
}

func TestBindingFileAdapterRejectsSymlinkEscapes(t *testing.T) {
	ctx := context.Background()
	root := t.TempDir()
	outside := t.TempDir()
	adapter := BindingFileAdapter{Root: root}
	response := serviceResponse("acute", "2025", "https://calculator.local/v1/execute")

	requestOutside := filepath.Join(outside, "request.json")
	if err := writeTestFile(requestOutside, []byte(`{"schema_version":"1.0"}`)); err != nil {
		t.Fatalf("write outside request fixture: %v", err)
	}
	requestLink := filepath.Join(root, "request-link.json")
	if err := os.Symlink(requestOutside, requestLink); err != nil {
		t.Fatalf("create request symlink: %v", err)
	}
	if _, err := adapter.LoadRequest(ctx, "request-link.json"); err == nil || !strings.Contains(err.Error(), "escapes configured root") {
		t.Fatalf("LoadRequest() error = %v, want root escape error", err)
	}

	responseOutside := filepath.Join(outside, "response.json")
	if err := writeTestFile(responseOutside, []byte(`{}`)); err != nil {
		t.Fatalf("write outside response fixture: %v", err)
	}
	responseLink := filepath.Join(root, "response-link.json")
	if err := os.Symlink(responseOutside, responseLink); err != nil {
		t.Fatalf("create response symlink: %v", err)
	}
	if err := adapter.SaveResponse(ctx, "response-link.json", response); err == nil || !strings.Contains(err.Error(), "escapes configured root") {
		t.Fatalf("SaveResponse() error = %v, want root escape error", err)
	}
}
