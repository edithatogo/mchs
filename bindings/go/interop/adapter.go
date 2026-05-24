package interop

import (
	"context"

	"github.com/edithatogo/mchs/bindings/go/model"
)

// Adapter defines the file interop boundary used by the CLI and any future
// host integration.
type Adapter interface {
	Load(ctx context.Context, path string) (*model.Workbook, error)
	Save(ctx context.Context, path string, workbook *model.Workbook) error
}
