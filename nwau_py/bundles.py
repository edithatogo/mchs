"""Data bundle contracts for Arrow/Parquet-backed calculator inputs.

The bundle layer stays dataframe-neutral:

- manifests describe bundle identity, provenance, and payload layout;
- payloads are stored as Arrow/Parquet files;
- readers may return pandas or Polars dataframes, but the manifest itself does
  not depend on either library.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any

try:  # pragma: no cover - optional dependency
    import polars as pl
except Exception:  # pragma: no cover - polars is optional in some environments
    pl: ModuleType | None = None

BUNDLE_SCHEMA_VERSION = "1.0"
_HEX_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")


class BundleContractError(ValueError):
    """Raised when a bundle manifest or payload violates the contract."""


@dataclass(frozen=True, slots=True)
class BundlePayload:
    """Contract metadata for a single tabular payload."""

    role: str
    path: Path
    format: str
    row_count: int
    columns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DataBundleManifest:
    """Validated manifest for a dataframe-neutral runtime bundle."""

    schema_version: str
    bundle_id: str
    calculator: str
    pricing_year: str
    source_artifact_id: str
    source_page_url: str
    checksum: str
    backend_neutral: bool
    payloads: dict[str, BundlePayload]
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DataBundle:
    """Validated bundle manifest plus its root directory."""

    manifest_path: Path
    bundle_dir: Path
    manifest: DataBundleManifest

    def payload_path(self, role: str) -> Path:
        return self.bundle_dir / self.manifest.payloads[role].path


def _require_str(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BundleContractError(f"{field} must be a non-empty string")
    if value.strip() != value:
        raise BundleContractError(f"{field} must not contain surrounding whitespace")
    return value


def _require_bool(value: Any, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise BundleContractError(f"{field} must be a boolean")
    return value


def _require_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise BundleContractError(f"{field} must be an integer")
    return value


def _require_columns(value: Any, *, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise BundleContractError(f"{field} must be a non-empty list of strings")
    columns: list[str] = []
    seen: set[str] = set()
    for column in value:
        if not isinstance(column, str) or not column.strip():
            raise BundleContractError(f"{field} must be a non-empty list of strings")
        if column in seen:
            raise BundleContractError(f"{field} must not contain duplicate names")
        seen.add(column)
        columns.append(column)
    return tuple(columns)


def _validate_year(value: str) -> str:
    if not _YEAR_RE.fullmatch(value):
        raise BundleContractError("pricing_year must be a supported four-digit label")
    return value


def _validate_checksum(value: str) -> str:
    if not _HEX_SHA256_RE.fullmatch(value):
        raise BundleContractError("checksum must be a lowercase sha256 hex digest")
    return value


def _parse_payload(role: str, payload: dict[str, Any]) -> BundlePayload:
    return BundlePayload(
        role=role,
        path=Path(_require_str(payload.get("path"), field=f"payloads.{role}.path")),
        format=_require_str(payload.get("format"), field=f"payloads.{role}.format"),
        row_count=_require_int(
            payload.get("row_count"), field=f"payloads.{role}.row_count"
        ),
        columns=_require_columns(
            payload.get("columns"), field=f"payloads.{role}.columns"
        ),
    )


def load_bundle_manifest(manifest_path: str | Path) -> DataBundleManifest:
    """Load and validate a bundle manifest."""
    path = Path(manifest_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise BundleContractError("bundle manifest must be a JSON object")

    schema_version = _require_str(payload.get("schema_version"), field="schema_version")
    if schema_version != BUNDLE_SCHEMA_VERSION:
        raise BundleContractError(
            f"unsupported schema_version {schema_version!r}; "
            f"expected {BUNDLE_SCHEMA_VERSION!r}"
        )

    bundle_id = _require_str(payload.get("bundle_id"), field="bundle_id")
    calculator = _require_str(payload.get("calculator"), field="calculator")
    pricing_year = _validate_year(
        _require_str(payload.get("pricing_year"), field="pricing_year")
    )
    source_artifact_id = _require_str(
        payload.get("source_artifact_id"), field="source_artifact_id"
    )
    source_page_url = _require_str(
        payload.get("source_page_url"), field="source_page_url"
    )
    checksum = _validate_checksum(
        _require_str(payload.get("checksum"), field="checksum")
    )
    backend_neutral = _require_bool(
        payload.get("backend_neutral"), field="backend_neutral"
    )
    if not backend_neutral:
        raise BundleContractError("backend_neutral must be true")

    payloads_raw = payload.get("payloads")
    if not isinstance(payloads_raw, dict) or not payloads_raw:
        raise BundleContractError("payloads must be a non-empty mapping")
    payloads = {
        role: _parse_payload(role, payload_value)
        for role, payload_value in payloads_raw.items()
    }

    provenance = payload.get("provenance", {})
    if not isinstance(provenance, dict):
        raise BundleContractError("provenance must be a mapping")

    return DataBundleManifest(
        schema_version=schema_version,
        bundle_id=bundle_id,
        calculator=calculator,
        pricing_year=pricing_year,
        source_artifact_id=source_artifact_id,
        source_page_url=source_page_url,
        checksum=checksum,
        backend_neutral=backend_neutral,
        payloads=payloads,
        provenance=provenance,
    )


def load_bundle(manifest_path: str | Path) -> DataBundle:
    """Load a validated bundle manifest from disk."""
    path = Path(manifest_path)
    manifest = load_bundle_manifest(path)
    return DataBundle(
        manifest_path=path,
        bundle_dir=path.parent,
        manifest=manifest,
    )


def _ensure_payload_path(bundle: DataBundle, role: str) -> Path:
    try:
        payload = bundle.manifest.payloads[role]
    except KeyError as exc:
        raise BundleContractError(f"unknown payload role {role!r}") from exc

    path = bundle.payload_path(role)
    if not path.is_file():
        raise BundleContractError(f"payloads.{role}.path does not exist: {path}")
    if payload.format != "parquet":
        raise BundleContractError(f"payloads.{role}.format must be parquet")
    return path


def read_bundle_frame(bundle: DataBundle, role: str):
    """Read a bundle payload as a dataframe."""
    path = _ensure_payload_path(bundle, role)
    if pl is not None:
        return pl.read_parquet(path)
    try:
        import pyarrow.parquet as pq

        return pq.read_table(path)
    except Exception:
        from nwau_py import compat as pd

        return pd.read_parquet(path)


def read_bundle_frame_polars(bundle: DataBundle, role: str):
    """Read a bundle payload as a Polars dataframe."""
    if pl is None:  # pragma: no cover - optional dependency guard
        raise ImportError("polars is not installed")
    path = _ensure_payload_path(bundle, role)
    return pl.read_parquet(path)
