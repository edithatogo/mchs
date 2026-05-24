package main

import (
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"

	"github.com/edithatogo/mchs/bindings/go/interop"
	"github.com/edithatogo/mchs/bindings/go/model"
)

func main() {
	if err := run(context.Background(), os.Args[1:], os.Stdin, os.Stdout, os.Stderr); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run(ctx context.Context, args []string, stdin io.Reader, stdout, stderr io.Writer) error {
	if len(args) == 0 {
		return usage(stderr)
	}

	switch args[0] {
	case "load":
		return runLoad(ctx, args[1:], stdout)
	case "save":
		return runSave(ctx, args[1:], stdin)
	default:
		return usage(stderr)
	}
}

func runLoad(ctx context.Context, args []string, stdout io.Writer) error {
	fs := flag.NewFlagSet("load", flag.ContinueOnError)
	fs.SetOutput(io.Discard)
	path := fs.String("path", "", "path to a workbook json file")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *path == "" {
		return errors.New("load requires --path")
	}

	workbook, err := interop.JSONFileAdapter{}.Load(ctx, *path)
	if err != nil {
		return err
	}

	enc := json.NewEncoder(stdout)
	enc.SetIndent("", "  ")
	return enc.Encode(workbook)
}

func runSave(ctx context.Context, args []string, stdin io.Reader) error {
	fs := flag.NewFlagSet("save", flag.ContinueOnError)
	fs.SetOutput(io.Discard)
	path := fs.String("path", "", "path to write a workbook json file")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *path == "" {
		return errors.New("save requires --path")
	}

	var workbook model.Workbook
	if err := json.NewDecoder(stdin).Decode(&workbook); err != nil {
		return fmt.Errorf("decode workbook from stdin: %w", err)
	}

	return interop.JSONFileAdapter{}.Save(ctx, *path, &workbook)
}

func usage(stderr io.Writer) error {
	_, _ = fmt.Fprintln(stderr, "usage:")
	_, _ = fmt.Fprintln(stderr, "  mchsbind load --path <file>")
	_, _ = fmt.Fprintln(stderr, "  mchsbind save --path <file> < input.json")
	return errors.New("invalid command")
}
