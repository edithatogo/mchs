package interop

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"

	"github.com/edithatogo/mchs/bindings/go/model"
)

// ServiceAdapter posts a Go binding request to a shared calculator service and
// decodes the contract response. It owns transport concerns only.
type ServiceAdapter struct {
	Client *http.Client
}

func (adapter ServiceAdapter) Execute(ctx context.Context, request *model.GoBindingRequest) (*model.GoBindingResponse, error) {
	if err := ValidateServiceRequest(request); err != nil {
		return nil, err
	}

	payload, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("encode service request: %w", err)
	}

	httpRequest, err := http.NewRequestWithContext(ctx, http.MethodPost, request.ServiceURL, bytes.NewReader(payload))
	if err != nil {
		return nil, fmt.Errorf("create service request: %w", err)
	}
	httpRequest.Header.Set("Content-Type", "application/json")
	httpRequest.Header.Set("Accept", "application/json")
	if request.CorrelationID != "" {
		httpRequest.Header.Set("X-Correlation-ID", request.CorrelationID)
	}

	client := adapter.Client
	if client == nil {
		client = &http.Client{Timeout: 30 * time.Second}
	}

	httpResponse, err := client.Do(httpRequest)
	if err != nil {
		return nil, fmt.Errorf("execute service request: %w", err)
	}
	defer httpResponse.Body.Close()

	if httpResponse.StatusCode < 200 || httpResponse.StatusCode > 299 {
		return nil, fmt.Errorf("execute service request: status %d", httpResponse.StatusCode)
	}

	var response model.GoBindingResponse
	if err := json.NewDecoder(httpResponse.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("decode service response json: %w", err)
	}
	if err := ValidateServiceResponse(request, &response); err != nil {
		return nil, err
	}

	return &response, nil
}

func ValidateServiceRequest(request *model.GoBindingRequest) error {
	if request == nil {
		return errors.New("service request is nil")
	}
	if request.Mode != model.BindingModeService {
		return fmt.Errorf("service adapter requires mode %q", model.BindingModeService)
	}
	required := map[string]string{
		"schema_version":        request.SchemaVersion,
		"calculator_id":         request.CalculatorID,
		"pricing_year":          request.PricingYear,
		"input_schema_version":  request.InputSchemaVersion,
		"output_schema_version": request.OutputSchemaVersion,
		"service_url":           request.ServiceURL,
		"fixture_gate":          request.FixtureGate,
	}
	for field, value := range required {
		if value == "" {
			return fmt.Errorf("service request missing %s", field)
		}
	}
	return nil
}

func ValidateServiceResponse(request *model.GoBindingRequest, response *model.GoBindingResponse) error {
	if response == nil {
		return errors.New("service response is nil")
	}
	if response.SchemaVersion != request.SchemaVersion {
		return fmt.Errorf("service response schema_version %q does not match request %q", response.SchemaVersion, request.SchemaVersion)
	}
	if response.CalculatorID != request.CalculatorID {
		return fmt.Errorf("service response calculator_id %q does not match request %q", response.CalculatorID, request.CalculatorID)
	}
	if response.PricingYear != request.PricingYear {
		return fmt.Errorf("service response pricing_year %q does not match request %q", response.PricingYear, request.PricingYear)
	}
	if response.Mode != model.BindingModeService {
		return fmt.Errorf("service response mode %q does not match %q", response.Mode, model.BindingModeService)
	}
	if response.Status == "" {
		return errors.New("service response missing status")
	}
	if response.Message == "" {
		return errors.New("service response missing message")
	}
	if response.Diagnostics.Status == "" {
		return errors.New("service response missing diagnostics.status")
	}
	if response.FixtureGateState == "" {
		return errors.New("service response missing fixture_gate_state")
	}
	if response.ModuleReadinessState == "" {
		return errors.New("service response missing module_readiness_state")
	}
	return nil
}
