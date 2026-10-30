"""Typed provenance helpers for IHACPA source archive artifacts.

The helpers in this module keep durable manifest output outside ignored raw
storage, normalize hosted-asset status across IHACPA and Box sources, and
serialize acquisition runs into JSON and CSV formats that remain easy to audit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess  # nosec B404
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

MANIFEST_SCHEMA_VERSION = "1"
DEFAULT_TRACKED_MANIFEST_DIR = Path("data/provenance/ihacpa")
DEFAULT_TRACKED_MANIFEST_JSON = DEFAULT_TRACKED_MANIFEST_DIR / "sources.json"
DEFAULT_TRACKED_MANIFEST_CSV = DEFAULT_TRACKED_MANIFEST_DIR / "sources.csv"
DEFAULT_SOURCE_PAGE_SNAPSHOT = (
    DEFAULT_TRACKED_MANIFEST_DIR / "snapshots" / "source-page.html"
)
DEFAULT_RAW_ARCHIVE_DIR = Path("archive/ihacpa/raw")

MANIFEST_CSV_FIELDNAMES = [
    "schema_version",
    "generated_at",
    "run_script_name",
    "run_script_version",
    "run_git_commit",
    "run_invocation_args",
    "run_source_page_url",
    "run_source_page_snapshot_path",
    "run_source_page_snapshot_sha256",
    "run_source_page_snapshot_bytes",
    "run_source_page_snapshot_captured_at",
    "run_started_at",
    "run_completed_at",
    "artifact_id",
    "year_label",
    "year_start",
    "artifact_type",
    "artifact_kind",
    "service_stream",
    "label",
    "source_page_url",
    "artifact_url",
    "source_host",
    "final_url",
    "content_type",
    "status",
    "path",
    "local_path",
    "checksum_algorithm",
    "checksum",
    "bytes",
    "downloaded_at",
    "checksum_checked_at",
    "redirect_chain",
    "notes",
    "error",
    "acquisition_status",
    "extraction_status",
    "implementation_status",
    "validation_status",
]


class SourceHost(str, Enum):
    """Where the source artifact is hosted."""

    IHACPA = "ihacpa"
    BOX = "box"
    OTHER = "other"


class ArtifactKind(str, Enum):
    """High-level kind of source artifact."""

    EXCEL = "excel"
    SAS = "sas"
    SUPPORT = "support"
    COMPILED = "compiled"
    DOCUMENTATION = "documentation"
    UNKNOWN = "unknown"


class AcquisitionStatus(str, Enum):
    """Lifecycle state for source acquisition."""

    LISTED = "listed"
    DOWNLOADED = "downloaded"
    EXTERNAL_HTML_ONLY = "external-html-only"
    FAILED = "failed"


class ExtractionStatus(str, Enum):
    """Lifecycle state for extraction."""

    NOT_STARTED = "not-started"
    EXTRACTED = "extracted"
    FAILED = "failed"


class ImplementationStatus(str, Enum):
    """Lifecycle state for implementation mapping."""

    NOT_STARTED = "not-started"
    IMPLEMENTED = "implemented"


class ValidationStatus(str, Enum):
    """Lifecycle state for validation."""

    NOT_STARTED = "not-started"
    VALIDATED = "validated"
    FAILED = "failed"


@dataclass(slots=True)
class LifecycleAxes:
    """Lifecycle status values tracked independently for each artifact."""

    acquisition_status: AcquisitionStatus = AcquisitionStatus.LISTED
    extraction_status: ExtractionStatus = ExtractionStatus.NOT_STARTED
    implementation_status: ImplementationStatus = ImplementationStatus.NOT_STARTED
    validation_status: ValidationStatus = ValidationStatus.NOT_STARTED

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-friendly representation of the lifecycle axes."""
        return {
            "acquisition": self.acquisition_status.value,
            "extraction": self.extraction_status.value,
            "implementation": self.implementation_status.value,
            "validation": self.validation_status.value,
        }


@dataclass(slots=True)
class SourcePageSnapshot:
    """Snapshot metadata for the source page HTML captured during a run."""

    path: str
    sha256: str
    byte_count: int
    captured_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "byte_count": self.byte_count,
            "captured_at": self.captured_at,
        }


@dataclass(slots=True)
class RunContext:
    """Metadata describing a single provenance acquisition run."""

    script_name: str
    script_version: str
    git_commit: str
    invocation_args: tuple[str, ...] = ()
    source_page_url: str = ""
    source_page_snapshot: SourcePageSnapshot | None = None
    started_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the run context."""
        return {
            "script_name": self.script_name,
            "script_version": self.script_version,
            "git_commit": self.git_commit,
            "invocation_args": list(self.invocation_args),
            "source_page_url": self.source_page_url,
            "source_page_snapshot": (
                self.source_page_snapshot.to_dict()
                if self.source_page_snapshot is not None
                else None
            ),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(slots=True)
class SourceArtifact:
    """A single source artifact listed by the IHACPA calculators page."""

    artifact_id: str
    year_label: str
    year_start: int
    artifact_type: str
    artifact_kind: ArtifactKind
    service_stream: str
    label: str
    source_page_url: str
    artifact_url: str
    source_host: SourceHost = SourceHost.OTHER
    final_url: str = ""
    content_type: str = ""
    status: str = "listed"
    path: str = ""
    local_path: str = ""
    checksum_algorithm: str = "sha256"
    bytes: int = 0
    checksum: str = ""
    downloaded_at: str = ""
    checksum_checked_at: str = ""
    redirect_chain: list[dict[str, str]] = field(default_factory=list)
    notes: str = ""
    error: str = ""
    lifecycle: LifecycleAxes = field(default_factory=LifecycleAxes)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the artifact."""
        return {
            "artifact_id": self.artifact_id,
            "year_label": self.year_label,
            "year_start": self.year_start,
            "artifact_type": self.artifact_type,
            "artifact_kind": self.artifact_kind.value,
            "service_stream": self.service_stream,
            "label": self.label,
            "source_page_url": self.source_page_url,
            "artifact_url": self.artifact_url,
            "source_host": self.source_host.value,
            "final_url": self.final_url,
            "content_type": self.content_type,
            "status": self.status,
            "path": self.path,
            "local_path": self.local_path,
            "checksum_algorithm": self.checksum_algorithm,
            "bytes": self.bytes,
            "checksum": self.checksum,
            "downloaded_at": self.downloaded_at,
            "checksum_checked_at": self.checksum_checked_at,
            "redirect_chain": self.redirect_chain,
            "notes": self.notes,
            "error": self.error,
            "lifecycle": self.lifecycle.to_dict(),
        }

    def to_csv_row(
        self,
        *,
        manifest: SourceArchiveManifest,
    ) -> dict[str, Any]:
        """Return a flattened row for CSV serialization."""
        return {
            "schema_version": manifest.schema_version,
            "generated_at": manifest.generated_at,
            "run_script_name": manifest.run_context.script_name,
            "run_script_version": manifest.run_context.script_version,
            "run_git_commit": manifest.run_context.git_commit,
            "run_invocation_args": json.dumps(
                list(manifest.run_context.invocation_args),
                ensure_ascii=True,
            ),
            "run_source_page_url": manifest.run_context.source_page_url,
            "run_source_page_snapshot_path": (
                manifest.run_context.source_page_snapshot.path
                if manifest.run_context.source_page_snapshot is not None
                else ""
            ),
            "run_source_page_snapshot_sha256": (
                manifest.run_context.source_page_snapshot.sha256
                if manifest.run_context.source_page_snapshot is not None
                else ""
            ),
            "run_source_page_snapshot_bytes": (
                manifest.run_context.source_page_snapshot.byte_count
                if manifest.run_context.source_page_snapshot is not None
                else 0
            ),
            "run_source_page_snapshot_captured_at": (
                manifest.run_context.source_page_snapshot.captured_at
                if manifest.run_context.source_page_snapshot is not None
                else ""
            ),
            "run_started_at": manifest.run_context.started_at,
            "run_completed_at": manifest.run_context.completed_at,
            "artifact_id": self.artifact_id,
            "year_label": self.year_label,
            "year_start": self.year_start,
            "artifact_type": self.artifact_type,
            "artifact_kind": self.artifact_kind.value,
            "service_stream": self.service_stream,
            "label": self.label,
            "source_page_url": self.source_page_url,
            "artifact_url": self.artifact_url,
            "source_host": self.source_host.value,
            "final_url": self.final_url,
            "content_type": self.content_type,
            "status": self.status,
            "path": self.path,
            "local_path": self.local_path,
            "checksum_algorithm": self.checksum_algorithm,
            "bytes": self.bytes,
            "checksum": self.checksum,
            "downloaded_at": self.downloaded_at,
            "checksum_checked_at": self.checksum_checked_at,
            "notes": self.notes,
            "error": self.error,
            "redirect_chain": json.dumps(self.redirect_chain, sort_keys=True),
            "acquisition_status": self.lifecycle.acquisition_status.value,
            "extraction_status": self.lifecycle.extraction_status.value,
            "implementation_status": self.lifecycle.implementation_status.value,
            "validation_status": self.lifecycle.validation_status.value,
        }


@dataclass(slots=True)
class ManifestPaths:
    """Filesystem locations used for tracked provenance manifests."""

    manifest_dir: Path
    json_path: Path
    csv_path: Path
    source_page_snapshot_path: Path


@dataclass(slots=True)
class SourceArchiveManifest:
    """Serialized provenance for a single archive acquisition run."""

    schema_version: str
    generated_at: str
    run_context: RunContext
    artifacts: tuple[SourceArtifact, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the full manifest."""
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "run_context": self.run_context.to_dict(),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
        }


def tracked_manifest_paths(base_dir: Path | str | None = None) -> ManifestPaths:
    """Return the tracked manifest locations used outside raw storage."""
    manifest_dir = (
        Path(base_dir) if base_dir is not None else DEFAULT_TRACKED_MANIFEST_DIR
    )
    return ManifestPaths(
        manifest_dir=manifest_dir,
        json_path=manifest_dir / "sources.json",
        csv_path=manifest_dir / "sources.csv",
        source_page_snapshot_path=manifest_dir / "snapshots" / "source-page.html",
    )


def raw_archive_dir(base_dir: Path | str | None = None) -> Path:
    """Return the raw archive storage directory."""
    return Path(base_dir) if base_dir is not None else DEFAULT_RAW_ARCHIVE_DIR


def sha256_file(path: Path) -> str:
    """Return the SHA-256 checksum for ``path``."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_source_page_snapshot(html: str, path: Path) -> SourcePageSnapshot:
    """Persist the source page HTML and return its metadata."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return SourcePageSnapshot(
        path=str(path),
        sha256=sha256_file(path),
        byte_count=path.stat().st_size,
        captured_at=datetime.now(UTC).isoformat(),
    )


def git_commit() -> str:
    """Return the current Git commit hash if available."""
    try:
        import shutil

        git_path = shutil.which("git")
        if git_path is None:
            return ""
        result = subprocess.run(  # noqa: S603  # nosec B603 B607
            [git_path, "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:  # pragma: no cover - best-effort metadata
        return ""
    return result.stdout.strip()


def source_host_from_url(url: str) -> SourceHost:
    """Infer the source host from a URL."""
    lowered = url.lower()
    netloc = urlparse(url).netloc.lower()
    if "box.com" in lowered or "box.com" in netloc:
        return SourceHost.BOX
    if "ihacpa.gov.au" in lowered or "ihacpa.gov.au" in netloc:
        return SourceHost.IHACPA
    return SourceHost.OTHER


def normalize_artifact_kind(label: str, url: str) -> ArtifactKind:
    """Infer the artifact kind from the label and URL."""
    lowered_label = label.lower()
    lowered_url = url.lower()
    if lowered_url.endswith((".xls", ".xlsx", ".xlsm", ".xlsb")):
        return ArtifactKind.EXCEL
    if lowered_url.endswith((".zip", ".7z")) or "sas" in lowered_label:
        return ArtifactKind.SAS
    if "guide" in lowered_label or "documentation" in lowered_label:
        return ArtifactKind.DOCUMENTATION
    if "support" in lowered_label or "support" in lowered_url:
        return ArtifactKind.SUPPORT
    if "compiled" in lowered_label or "binary" in lowered_label:
        return ArtifactKind.COMPILED
    return ArtifactKind.UNKNOWN


def normalize_service_stream(artifact_kind: ArtifactKind, label: str) -> str:
    """Return a stable service-stream label for the artifact."""
    if artifact_kind is ArtifactKind.SAS:
        return "SAS-based calculators"
    if label.strip():
        return " ".join(label.split())
    return artifact_kind.value


def normalize_acquisition_status(
    artifact_url: str,
    *,
    final_url: str = "",
    content_type: str = "",
    downloaded: bool = False,
    failed: bool = False,
) -> AcquisitionStatus:
    """Normalize acquisition status across IHACPA-hosted and Box-hosted assets."""
    if failed:
        return AcquisitionStatus.FAILED

    host = source_host_from_url(final_url or artifact_url)
    if host is SourceHost.BOX and "html" in content_type.lower():
        return AcquisitionStatus.EXTERNAL_HTML_ONLY
    if downloaded:
        return AcquisitionStatus.DOWNLOADED
    return AcquisitionStatus.LISTED


def stable_artifact_id(
    year_label: str,
    label: str,
    artifact_url: str,
    *,
    artifact_kind: ArtifactKind | None = None,
) -> str:
    """Return a stable identifier derived from the artifact metadata."""
    prefix = f"{year_label}-{(artifact_kind or ArtifactKind.UNKNOWN).value}-{label}"
    slug = [char.lower() if char.isalnum() else "-" for char in prefix]
    compact = "".join(slug)
    compact = "-".join(part for part in compact.split("-") if part)
    digest = hashlib.sha256(artifact_url.encode("utf-8")).hexdigest()[:10]
    if compact:
        return f"{compact[:80]}-{digest}"
    return digest


def manifest_rows(manifest: SourceArchiveManifest) -> list[dict[str, Any]]:
    """Return flattened rows suitable for CSV output."""
    return [artifact.to_csv_row(manifest=manifest) for artifact in manifest.artifacts]


def write_manifest_json(manifest: SourceArchiveManifest, path: Path) -> None:
    """Write the manifest JSON payload to ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest.to_dict(), indent=2) + "\n", encoding="utf-8")


def write_manifest_csv(manifest: SourceArchiveManifest, path: Path) -> None:
    """Write the manifest CSV payload to ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=MANIFEST_CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(manifest_rows(manifest))
