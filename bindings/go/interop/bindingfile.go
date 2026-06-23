package interop

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/edithatogo/mchs/bindings/go/model"
)

// BindingFileAdapter loads and stores Go binding contract envelopes as JSON.
type BindingFileAdapter struct {
	// Root constrains request/response file access. The zero value uses the
	// current working directory.
	Root string
}

func (adapter BindingFileAdapter) LoadRequest(_ context.Context, path string) (*model.GoBindingRequest, error) {
	resolved, err := adapter.resolveExistingPath(path)
	if err != nil {
		return nil, err
	}

	data, err := os.ReadFile(resolved)
	if err != nil {
		return nil, fmt.Errorf("read binding request file: %w", err)
	}

	var request model.GoBindingRequest
	if err := json.Unmarshal(data, &request); err != nil {
		return nil, fmt.Errorf("decode binding request json: %w", err)
	}

	return &request, nil
}

func (adapter BindingFileAdapter) SaveResponse(_ context.Context, path string, response *model.GoBindingResponse) error {
	resolved, err := adapter.resolveWritablePath(path)
	if err != nil {
		return err
	}

	data, err := json.MarshalIndent(response, "", "  ")
	if err != nil {
		return fmt.Errorf("encode binding response json: %w", err)
	}
	data = append(data, '\n')

	if err := os.WriteFile(resolved, data, 0o644); err != nil {
		return fmt.Errorf("write binding response file: %w", err)
	}

	return nil
}

func (adapter BindingFileAdapter) resolveExistingPath(path string) (string, error) {
	resolved, err := adapter.resolvePath(path, false)
	if err != nil {
		return "", err
	}
	return filepath.EvalSymlinks(resolved)
}

func (adapter BindingFileAdapter) resolveWritablePath(path string) (string, error) {
	return adapter.resolvePath(path, true)
}

func (adapter BindingFileAdapter) resolvePath(path string, writable bool) (string, error) {
	if strings.TrimSpace(path) == "" {
		return "", fmt.Errorf("binding file path is required")
	}

	root := adapter.Root
	if root == "" {
		root = "."
	}
	rootAbs, err := filepath.Abs(root)
	if err != nil {
		return "", fmt.Errorf("resolve binding file root: %w", err)
	}
	rootReal, err := filepath.EvalSymlinks(rootAbs)
	if err != nil {
		return "", fmt.Errorf("resolve binding file root symlinks: %w", err)
	}

	target := path
	if !filepath.IsAbs(target) {
		target = filepath.Join(rootReal, target)
	}
	targetAbs, err := filepath.Abs(target)
	if err != nil {
		return "", fmt.Errorf("resolve binding file path: %w", err)
	}
	targetClean := filepath.Clean(targetAbs)

	var targetReal string
	if writable {
		targetReal, err = writableRealPath(targetClean)
	} else {
		targetReal, err = filepath.EvalSymlinks(targetClean)
	}
	if err != nil {
		return "", fmt.Errorf("resolve binding file symlinks: %w", err)
	}
	if !pathWithinRoot(rootReal, targetReal) {
		return "", fmt.Errorf("binding file path escapes configured root")
	}
	return targetReal, nil
}

func writableRealPath(path string) (string, error) {
	if existing, err := filepath.EvalSymlinks(path); err == nil {
		return existing, nil
	} else if !os.IsNotExist(err) {
		return "", err
	}

	parent, err := filepath.EvalSymlinks(filepath.Dir(path))
	if err != nil {
		return "", err
	}
	return filepath.Join(parent, filepath.Base(path)), nil
}

func pathWithinRoot(root string, target string) bool {
	rel, err := filepath.Rel(root, target)
	if err != nil {
		return false
	}
	return rel == "." || (rel != ".." && !strings.HasPrefix(rel, ".."+string(os.PathSeparator)))
}
