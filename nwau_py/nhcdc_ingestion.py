"""NHCDC public appendix ingestion helpers.

The helpers in this module keep public NHCDC appendix handling manifest-backed
and local-safe. They normalize small committed fixtures for tests and tutorials
without claiming patient-level ingestion or compliance certification.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, cast

import pandas as pd
import yaml

__all__ = [
    "NHCDCAppendixManifest",
    "NHCDCAppendixManifestError",
    "diagnose_nhcdc_appendix_source",
    "load_nhcdc_appendix_manifest",
    "normalize_nhcdc_appendix_table",
]


class NHCDCAppendixManifestError(ValueError):
    """Raised when an NHCDC appendix manifest or source is invalid."""


@dataclass(frozen=True, slots=True)
class NHCDCAppendixManifest:
    """Manifest-backed metadata for one public NHCDC appendix fixture."""

    appendix_id: str
    title: str
    source_url: str
    file_type: str
    publication_date: str
    retrieval_date: str
    source_path: str
    normalized_path: str
    table_categories: tuple[str, ...]
    required_columns: tuple[str, ...]
    provenance_columns: tuple[str, ...]
    status: str
    source_sha256: str | None = None
    normalized_sha256: str | None = None
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable manifest payload."""
        return asdict(self)


def _require_mapping(value: object, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise NHCDCAppendixManifestError(f"{field} must be a mapping")
    return cast(Mapping[str, Any], value)


def _require_sequence(value: object, *, field: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise NHCDCAppendixManifestError(f"{field} must be a sequence")
    return tuple(value)


def _require_str(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NHCDCAppendixManifestError(f"{field} must be a non-empty string")
    return value


def _optional_str(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _require_str(value, field=field)


def _scalar_to_str(value: object, *, field: str) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return _require_str(value, field=field)


def _tuple_of_str(value: object, *, field: str) -> tuple[str, ...]:
    return tuple(
        _require_str(item, field=field)
        for item in _require_sequence(value, field=field)
    )


def _manifest_from_mapping(payload: Mapping[str, Any]) -> NHCDCAppendixManifest:
    return NHCDCAppendixManifest(
        appendix_id=_require_str(payload.get("appendix_id"), field="appendix_id"),
        title=_require_str(payload.get("title"), field="title"),
        source_url=_require_str(payload.get("source_url"), field="source_url"),
        file_type=_require_str(payload.get("file_type"), field="file_type"),
        publication_date=_scalar_to_str(
            payload.get("publication_date"),
            field="publication_date",
        ),
        retrieval_date=_scalar_to_str(
            payload.get("retrieval_date"),
            field="retrieval_date",
        ),
        source_path=_require_str(payload.get("source_path"), field="source_path"),
        normalized_path=_require_str(
            payload.get("normalized_path"),
            field="normalized_path",
        ),
        table_categories=_tuple_of_str(
            payload.get("table_categories"),
            field="table_categories",
        ),
        required_columns=_tuple_of_str(
            payload.get("required_columns"),
            field="required_columns",
        ),
        provenance_columns=_tuple_of_str(
            payload.get("provenance_columns"),
            field="provenance_columns",
        ),
        status=_require_str(payload.get("status"), field="status"),
        source_sha256=_optional_str(
            payload.get("source_sha256"),
            field="source_sha256",
        ),
        normalized_sha256=_optional_str(
            payload.get("normalized_sha256"),
            field="normalized_sha256",
        ),
        notes=tuple(str(note) for note in payload.get("notes", ()) or ()),
    )


def load_nhcdc_appendix_manifest(path: str | Path) -> NHCDCAppendixManifest:
    """Load a committed NHCDC appendix manifest."""
    manifest_path = Path(path)
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise NHCDCAppendixManifestError("manifest must be a mapping")
    return _manifest_from_mapping(cast(Mapping[str, Any], payload))


def _resolve_source_path(
    manifest: NHCDCAppendixManifest,
    manifest_path: Path,
    base_dir: str | Path | None,
) -> Path:
    root = Path(base_dir) if base_dir is not None else manifest_path.parent
    return root / manifest.source_path


def _load_source_frame(source_path: Path) -> pd.DataFrame:
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    return pd.read_csv(source_path)


def diagnose_nhcdc_appendix_source(
    manifest_path: str | Path,
    *,
    base_dir: str | Path | None = None,
) -> dict[str, object]:
    """Diagnose whether a public NHCDC appendix fixture can be normalized."""
    manifest_path = Path(manifest_path)
    manifest = load_nhcdc_appendix_manifest(manifest_path)
    source_path = _resolve_source_path(manifest, manifest_path, base_dir)

    if not source_path.exists():
        return {
            "appendix_id": manifest.appendix_id,
            "status": "missing",
            "gap_id": "missing-source-file",
            "reason": "source file is absent from the local cache or fixture path",
            "scope": manifest.source_path,
            "expected_resolution": (
                "place the appendix source file at the manifest path"
            ),
        }

    frame = _load_source_frame(source_path)
    missing_columns = [
        column for column in manifest.required_columns if column not in frame.columns
    ]
    if missing_columns:
        return {
            "appendix_id": manifest.appendix_id,
            "status": "format-changed",
            "gap_id": "format-changed-source-schema",
            "reason": "source file is missing required appendix columns",
            "scope": manifest.source_path,
            "missing_columns": missing_columns,
            "expected_resolution": (
                "update the manifest or parser to match the appendix schema"
            ),
        }
    return {
        "appendix_id": manifest.appendix_id,
        "status": "available",
        "gap_id": None,
        "row_count": len(frame),
        "source_path": source_path.as_posix(),
        "normalized_path": (source_path.parent / manifest.normalized_path).as_posix(),
    }


def normalize_nhcdc_appendix_table(
    manifest_path: str | Path,
    *,
    base_dir: str | Path | None = None,
) -> pd.DataFrame:
    """Normalize a public NHCDC appendix fixture into a provenance-rich table."""
    manifest_path = Path(manifest_path)
    manifest = load_nhcdc_appendix_manifest(manifest_path)
    source_path = _resolve_source_path(manifest, manifest_path, base_dir)
    frame = _load_source_frame(source_path)

    missing_columns = [
        column for column in manifest.required_columns if column not in frame.columns
    ]
    if missing_columns:
        raise NHCDCAppendixManifestError(
            "source file is missing required appendix columns: "
            + ", ".join(missing_columns)
        )

    normalized = frame.loc[:, manifest.required_columns].copy()
    for column in ("average_cost_per_episode", "average_nwau", "cost_per_nwau"):
        normalized[column] = pd.to_numeric(normalized[column], errors="raise")

    normalized.insert(0, "appendix_id", manifest.appendix_id)
    normalized.insert(1, "appendix_title", manifest.title)
    normalized.insert(2, "source_url", manifest.source_url)
    normalized.insert(3, "publication_date", manifest.publication_date)
    normalized.insert(4, "retrieval_date", manifest.retrieval_date)
    normalized.insert(5, "table_category", "; ".join(manifest.table_categories))
    normalized.insert(6, "source_row_number", range(1, len(normalized) + 1))
    normalized.insert(7, "source_path", manifest.source_path)

    for column in manifest.provenance_columns:
        if column not in normalized.columns:
            raise NHCDCAppendixManifestError(
                f"normalized output is missing provenance column {column!r}"
            )

    ordered_columns = [
        "appendix_id",
        "appendix_title",
        "source_url",
        "publication_date",
        "retrieval_date",
        "table_category",
        "source_row_number",
        "source_path",
        *manifest.required_columns,
        *[column for column in manifest.provenance_columns if column not in {
            "appendix_id",
            "appendix_title",
            "source_url",
            "publication_date",
            "retrieval_date",
            "table_category",
            "source_row_number",
            "source_path",
        }],
    ]
    normalized = normalized.loc[:, ordered_columns]
    return normalized.reset_index(drop=True)
