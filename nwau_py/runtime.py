"""Shared adapter helpers for CSV calculator execution.

This module keeps the CLI-facing boundary small:

- read an input CSV using a caller-provided loader;
- call a calculator callable with the loaded table and runtime parameters;
- write the resulting table back to CSV using a caller-provided writer.

The helper stays free of calculator math and does not depend on a specific
tabular backend.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, TextIO, TypeVar, cast

InputTableT = TypeVar("InputTableT", contravariant=True)
ParamsT = TypeVar("ParamsT", contravariant=True)
OutputTableT = TypeVar("OutputTableT", covariant=True)


class CalculatorCallable(Protocol[InputTableT, ParamsT, OutputTableT]):
    """Protocol for runtime calculator callables."""

    def __call__(
        self,
        data: InputTableT,
        params: ParamsT,
        *,
        year: str,
        ref_dir: Path | None = None,
    ) -> OutputTableT: ...


def open_output_stream(output: str | Path) -> TextIO:
    """Open the target output stream for CSV writing."""
    if str(output) == "-":
        return cast(TextIO, sys.stdout)
    return open(Path(output), "w", newline="", encoding="utf-8")


def run_csv_calculation[InputTableT, ParamsT, OutputTableT](
    input_csv: str | Path,
    output: str | Path,
    calculator: CalculatorCallable[InputTableT, ParamsT, OutputTableT],
    params: ParamsT,
    *,
    year: str | None = None,
    ref_dir: str | Path | None = None,
    read_csv: Callable[[str | Path], InputTableT],
    write_csv: Callable[[OutputTableT, TextIO], None],
    default_year: str = "2025",
) -> None:
    """Read CSV input, invoke ``calculator``, and write CSV output.

    ``read_csv`` and ``write_csv`` are supplied by the caller so this helper can
    stay free of any one tabular library dependency.
    """
    input_table = read_csv(input_csv)
    result = calculator(
        input_table,
        params,
        year=year or default_year,
        ref_dir=Path(ref_dir) if ref_dir is not None else None,
    )

    outfh = open_output_stream(output)
    try:
        write_csv(result, outfh)
    finally:
        if outfh is not sys.stdout:
            outfh.close()
