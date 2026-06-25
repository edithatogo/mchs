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
	case "execute":
		return runExecute(ctx, args[1:], stdin, stdout)
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

func runExecute(ctx context.Context, args []string, stdin io.Reader, stdout io.Writer) error {
	fs := flag.NewFlagSet("execute", flag.ContinueOnError)
	fs.SetOutput(io.Discard)
	requestPath := fs.String("request", "-", "path to a Go binding request json file, or - for stdin")
	outputPath := fs.String("output", "-", "path to write a Go binding response json file, or - for stdout")
	if err := fs.Parse(args); err != nil {
		return err
	}

	request, err := readBindingRequest(ctx, *requestPath, stdin)
	if err != nil {
		return err
	}

	response, err := interop.ServiceAdapter{}.Execute(ctx, request)
	if err != nil {
		return err
	}

	return writeBindingResponse(ctx, *outputPath, stdout, response)
}

func readBindingRequest(ctx context.Context, path string, stdin io.Reader) (*model.GoBindingRequest, error) {
	if path != "-" {
		return interop.BindingFileAdapter{}.LoadRequest(ctx, path)
	}

	var request model.GoBindingRequest
	if err := json.NewDecoder(stdin).Decode(&request); err != nil {
		return nil, fmt.Errorf("decode binding request from stdin: %w", err)
	}
	return &request, nil
}

func writeBindingResponse(ctx context.Context, path string, stdout io.Writer, response *model.GoBindingResponse) error {
	if path != "-" {
		return interop.BindingFileAdapter{}.SaveResponse(ctx, path, response)
	}

	enc := json.NewEncoder(stdout)
	enc.SetIndent("", "  ")
	return enc.Encode(response)
}

func usage(stderr io.Writer) error {
	_, _ = fmt.Fprintln(stderr, "usage:")
	_, _ = fmt.Fprintln(stderr, "  mchsbind execute --request <file|-> --output <file|->")
	_, _ = fmt.Fprintln(stderr, "  mchsbind load --path <file>")
	_, _ = fmt.Fprintln(stderr, "  mchsbind save --path <file> < input.json")
	return errors.New("invalid command")
}
