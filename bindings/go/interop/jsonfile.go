package interop

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/edithatogo/mchs/bindings/go/model"
)

// JSONFileAdapter stores the workbook model as plain JSON on disk.
type JSONFileAdapter struct{}

func (JSONFileAdapter) Load(_ context.Context, path string) (*model.Workbook, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read workbook file: %w", err)
	}

	var workbook model.Workbook
	if err := json.Unmarshal(data, &workbook); err != nil {
		return nil, fmt.Errorf("decode workbook json: %w", err)
	}

	return &workbook, nil
}

func (JSONFileAdapter) Save(_ context.Context, path string, workbook *model.Workbook) error {
	data, err := json.MarshalIndent(workbook, "", "  ")
	if err != nil {
		return fmt.Errorf("encode workbook json: %w", err)
	}

	if err := os.WriteFile(path, data, 0o644); err != nil {
		return fmt.Errorf("write workbook file: %w", err)
	}

	return nil
}
