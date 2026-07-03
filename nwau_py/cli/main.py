"""Command line interface for the NWAU calculators."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import IO, Any, Protocol, cast

import click


class _CsvFrame(Protocol):
    def to_csv(self, outfh: IO[str], *, index: bool) -> None: ...


_CLASSIFICATION_SYSTEMS = {
    "acute": "ar_drg",
    "ed": "aecc",
    "outpatients": "tier_2",
}
_INTEROP_CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "contracts"
    / "interop"
    / "cli-file-interop.contract.json"
)


def _write_output(df: _CsvFrame, outfh: IO[str]) -> None:
    df.to_csv(outfh, index=False)


def _load_interop_contract() -> dict[str, Any]:
    return json.loads(_INTEROP_CONTRACT_PATH.read_text(encoding="utf-8"))


def _run(
    stream: str,
    calculator,
    params,
    input_csv: str,
    output: str,
    year: str | None,
    ref_dir: str | None,
) -> None:
    import pandas as pd

    from nwau_py.classification_validation import get_classification_requirement
    from nwau_py.runtime import run_csv_calculation

    validation_year = year or "2025"
    try:
        input_df = pd.read_csv(input_csv)
        requirement = get_classification_requirement(
            _CLASSIFICATION_SYSTEMS[stream],
            validation_year,
        )
        if requirement.expected_version is None:
            raise click.ClickException(
                f"{requirement.display_name} is not available for pricing year "
                f"{validation_year}"
            )
        missing_fields = requirement.missing_fields(input_df.columns)
        if missing_fields:
            raise click.ClickException(
                f"{requirement.display_name} {validation_year} is missing required "
                f"fields: {', '.join(missing_fields)}"
            )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    run_csv_calculation(
        input_csv=input_csv,
        output=output,
        calculator=calculator,
        params=params,
        year=year,
        ref_dir=ref_dir,
        read_csv=pd.read_csv,
        write_csv=_write_output,
    )


def _common_options(func):
    func = click.argument("input_csv", type=click.Path(exists=True))(func)
    func = click.option(
        "--params",
        default=None,
        type=click.Path(file_okay=False, dir_okay=True),
        help="Directory containing SAS tables",
    )(func)
    func = click.option("--year", default=None, help="NEP/NWAU edition year")(func)
    func = click.option(
        "--output",
        default="-",
        show_default=True,
        help="Output CSV path ('-' for stdout)",
    )(func)
    return func


def common_options(func: Callable[..., Any]) -> Callable[..., Any]:
    options = [
        click.argument("input_csv", type=click.Path(exists=True)),
        click.option(
            "--params",
            default=None,
            type=click.Path(file_okay=False, dir_okay=True),
            help="Directory containing SAS tables",
        ),
        click.option(
            "--year",
            default=None,
            help="NEP/NWAU edition year",
        ),
        click.option(
            "--output",
            default="-",
            show_default=True,
            help="Output CSV path ('-' for stdout)",
        ),
        click.option(
            "--icu/--no-icu",
            default=True,
            show_default=True,
            help="Include ICU adjustments",
        ),
        click.option(
            "--covid/--no-covid",
            default=True,
            show_default=True,
            help="Include COVID adjustments",
        ),
    ]
    for opt in reversed(options):
        func = opt(func)
    return func


@click.group()
def cli() -> None:
    """NWAU calculation commands."""


@cli.group()
def interop() -> None:
    """Inspect the file interop contract bundle."""


@interop.command(name="contract")
def interop_contract() -> None:
    """Print the machine-readable CLI/file interop contract."""
    click.echo(json.dumps(_load_interop_contract(), indent=2, sort_keys=True))


@cli.group()
def sources() -> None:
    """Discover source pages and build draft manifests."""


@cli.group(name="coding-set")
def coding_set() -> None:
    """Inspect coding-set registry metadata."""


@coding_set.group(name="registry")
def coding_set_registry() -> None:
    """Inspect metadata-only coding-set registry entries."""


@coding_set_registry.command(name="list")
@click.option("--year", default=None, help="filter registry versions by pricing year")
@click.option(
    "--metadata-only/--include-restricted",
    default=True,
    show_default=True,
    help="emit public metadata only; restricted payloads are never included",
)
def coding_set_registry_list(year: str | None, metadata_only: bool) -> None:
    """List metadata-only coding-set registry entries."""
    from nwau_py.coding_set_registry import list_coding_set_families

    families = []
    for family in list_coding_set_families():
        payload = family.to_dict()
        if year is not None:
            versions = payload["versions"]
            if not isinstance(versions, list):
                raise click.ClickException("registry versions must be a list")
            filtered_versions = []
            for version in versions:
                if not isinstance(version, dict):
                    continue
                version_record = cast(dict[str, Any], version)
                version_year = version_record.get("year", "")
                if str(version_year) == year:
                    filtered_versions.append(version_record)
            payload["versions"] = filtered_versions
        payload["metadata_only"] = metadata_only
        families.append(payload)
    click.echo(json.dumps({"families": families}, indent=2, sort_keys=True))


@coding_set_registry.command(name="validate-compatibility")
@click.option("--entry", "system", required=True, help="coding-set family or alias")
@click.option("--year", required=True, help="pricing year")
@click.option("--version", default=None, help="declared version")
def coding_set_registry_validate_compatibility(
    system: str,
    year: str,
    version: str | None,
) -> None:
    """Validate a coding-set family/version against the registry."""
    from nwau_py.coding_set_registry import (
        CodingSetRegistryError,
        validate_coding_set_compatibility,
    )

    try:
        result = validate_coding_set_compatibility(system, year, version)
    except CodingSetRegistryError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    if not result.compatible:
        raise SystemExit(1)


def _source_scan_input_options(func):
    func = click.option(
        "--html-file",
        "html_files",
        multiple=True,
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        help="HTML fixture file to scan",
    )(func)
    func = click.option(
        "--text-file",
        "text_files",
        multiple=True,
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        help="text fixture file to scan",
    )(func)
    func = click.option(
        "--url",
        "urls",
        multiple=True,
        help="explicit URL to include in the draft manifest",
    )(func)
    func = click.option(
        "--source-page-url",
        default=None,
        help="base URL used to resolve relative links",
    )(func)
    return func


def _scan_output_options(func=None, *, include_year: bool = True):
    def decorate(inner):
        if include_year:
            inner = click.option(
                "--year",
                default=None,
                help="pricing year to stamp into the draft manifest",
            )(inner)
        inner = click.option(
            "--json/--dry-run",
            "emit_json",
            default=False,
            show_default=True,
            help="emit JSON instead of the human-readable dry-run summary",
        )(inner)
        return inner

    if func is None:
        return decorate
    return decorate(func)


@sources.command(name="scan")
@_source_scan_input_options
@_scan_output_options
def sources_scan(
    html_files: tuple[Path, ...],
    text_files: tuple[Path, ...],
    urls: tuple[str, ...],
    source_page_url: str | None,
    year: str | None,
    emit_json: bool,
) -> None:
    """Scan offline fixtures or URL lists and print a draft manifest."""
    from nwau_py.source_scanner import manifest_to_json, scan_sources_dry_run

    result = scan_sources_dry_run(
        html_documents=html_files,
        text_documents=text_files,
        urls=urls,
        source_page_url=source_page_url,
        pricing_year=year,
    )
    if emit_json:
        click.echo(manifest_to_json(result.manifest))
    else:
        click.echo(result.dry_run_output)


@sources.command(name="add-year")
@click.argument("year")
@_source_scan_input_options
@_scan_output_options(include_year=False)
def sources_add_year(
    year: str,
    html_files: tuple[Path, ...],
    text_files: tuple[Path, ...],
    urls: tuple[str, ...],
    source_page_url: str | None,
    emit_json: bool,
) -> None:
    """Create or update a pricing-year draft manifest from discoveries."""
    from nwau_py.source_scanner import manifest_to_json, scan_sources_dry_run

    result = scan_sources_dry_run(
        html_documents=html_files,
        text_documents=text_files,
        urls=urls,
        source_page_url=source_page_url,
        pricing_year=year,
    )
    if emit_json:
        click.echo(manifest_to_json(result.manifest))
    else:
        click.echo(result.dry_run_output)


@cli.command(name="validate-year")
@click.argument("year")
@click.option(
    "--json/--text",
    "emit_json",
    default=False,
    show_default=True,
    help="emit JSON instead of the human-readable validation report",
)
def validate_year(year: str, emit_json: bool) -> None:
    """Validate repository-local evidence for a pricing year."""
    from nwau_py.pricing_year_validation import (
        format_pricing_year_validation_report,
        validate_pricing_year,
    )

    report = validate_pricing_year(year)
    if emit_json:
        click.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        click.echo(format_pricing_year_validation_report(report))
    if not report.passed:
        raise SystemExit(1)


@cli.command(name="diff-year")
@click.argument("from_year")
@click.argument("to_year")
@click.option(
    "--json",
    "emit_json",
    is_flag=True,
    default=False,
    help="emit JSON instead of the human-readable markdown diff",
)
def diff_year(from_year: str, to_year: str, emit_json: bool) -> None:
    """Compare repository-local reference-data manifests for two pricing years."""
    from nwau_py.pricing_year_diff import (
        compare_pricing_year_manifests,
        format_pricing_year_diff_report,
    )
    from nwau_py.reference_manifest import ReferenceManifestError

    try:
        report = compare_pricing_year_manifests(from_year, to_year)
    except (FileNotFoundError, ReferenceManifestError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    if emit_json:
        click.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        click.echo(format_pricing_year_diff_report(report))


@cli.command()
@_common_options
def acute(input_csv: str, params: str | None, output: str, year: str | None) -> None:
    """Calculate NWAU for acute care."""
    from nwau_py.calculators import AcuteParams, calculate_acute

    _run("acute", calculate_acute, AcuteParams(), input_csv, output, year, params)


@cli.command()
@_common_options
def ed(input_csv: str, params: str | None, output: str, year: str | None) -> None:
    """Calculate NWAU for emergency department care."""
    from nwau_py.calculators import EDParams, calculate_ed

    _run("ed", calculate_ed, EDParams(), input_csv, output, year, params)


@cli.command(name="non-admitted")
@_common_options
def non_admitted(
    input_csv: str, params: str | None, output: str, year: str | None
) -> None:
    """Calculate NWAU for non-admitted care."""
    from nwau_py.calculators import OutpatientParams, calculate_outpatients

    _run(
        "outpatients",
        calculate_outpatients,
        OutpatientParams(),
        input_csv,
        output,
        year,
        params,
    )


if __name__ == "__main__":  # pragma: no cover
    cli()
