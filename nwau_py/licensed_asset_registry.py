"""Local-only registry helpers for licensed IHACPA assets.

The registry is intentionally metadata-only. It records where licensed assets
live on a user's machine, whether the user has acknowledged the licensing
boundary, and whether the repository can safely treat the assets as absent or
present at runtime.

The helpers here do not read or expose restricted asset contents.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import Any, Final, Literal, cast

from .licensed_product_workflow import (
    LicensedProductWorkflowError,
    is_commit_safe_excluded_path,
    is_local_only_licensed_path,
)

__all__ = [
    "LICENSED_ASSET_MANIFEST_RELATIVE_PATH",
    "LICENSED_ASSET_MANIFEST_SCHEMA_VERSION",
    "LicensedAssetManifest",
    "LicensedAssetReference",
    "LicensedAssetRegistryError",
    "audit_restricted_asset_signatures",
    "build_licensed_asset_manifest",
    "build_licensed_asset_reference",
    "doctor_licensed_assets",
    "ensure_licensed_asset_manifest",
    "is_commit_safe_licensed_asset_path",
    "is_local_only_licensed_asset_path",
    "licensed_asset_manifest_path",
    "load_licensed_asset_manifest",
    "register_licensed_asset_manifest",
    "save_licensed_asset_manifest",
    "validate_licensed_asset_manifest",
]

LICENSED_ASSET_MANIFEST_SCHEMA_VERSION: Final[str] = "1.0"
LICENSED_ASSET_MANIFEST_RELATIVE_PATH: Final[Path] = Path(
    "archive/ihacpa/raw/licensed-assets.manifest.json"
)
_LICENSE_ACKNOWLEDGEMENT = (
    "I acknowledge that licensed IHACPA, ICD-10-AM, ACHI, ACS, mapping, and "
    "grouper assets remain my responsibility to license and use properly."
)
_FORBIDDEN_SIGNATURES: Final[dict[str, tuple[str, ...]]] = {
    "licensed-office-workbook": (".xls", ".xlsx", ".xlsm", ".xlsb"),
    "licensed-office-document": (".doc", ".docx", ".pdf"),
    "licensed-archive": (".7z", ".zip", ".rar", ".tar", ".gz"),
    "licensed-statistical-dataset": (".sas7bdat", ".sav", ".dta"),
}
_ALLOWED_LOCAL_MANIFEST_NAMES: Final[frozenset[str]] = frozenset(
    {
        "licensed-assets.manifest.json",
        "manifest.json",
    }
)
_ALLOWED_REPOSITORY_PREFIXES: Final[tuple[str, ...]] = (
    "archive/sas/",
    "archive/ihacpa/raw/",
    "bindings/",
    "excel_calculator/archive/",
)


class LicensedAssetRegistryError(LicensedProductWorkflowError):
    """Raised when a licensed-asset manifest or guard check is invalid."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise LicensedAssetRegistryError(f"{field} must be a string")
    if not value:
        raise LicensedAssetRegistryError(f"{field} must not be blank")
    if value.strip() != value:
        raise LicensedAssetRegistryError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_relative_path(path: str | Path, *, field: str) -> str:
    candidate = Path(path)
    if candidate == Path(""):
        raise LicensedAssetRegistryError(f"{field} must not be blank")
    if candidate.is_absolute():
        raise LicensedAssetRegistryError(f"{field} must be a relative path")
    if any(part == ".." for part in candidate.parts):
        raise LicensedAssetRegistryError(f"{field} must not contain parent traversal")
    normalized = candidate.as_posix()
    if normalized == ".":
        raise LicensedAssetRegistryError(f"{field} must not be blank")
    return normalized


def _normalize_string_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise LicensedAssetRegistryError(f"{field} must be a tuple or list of strings")
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise LicensedAssetRegistryError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    return tuple(normalized)


def licensed_asset_manifest_path(
    repo_root: str | Path | None = None,
) -> Path:
    """Return the ignored local manifest path for licensed assets."""
    if repo_root is None:
        return LICENSED_ASSET_MANIFEST_RELATIVE_PATH
    return Path(repo_root) / LICENSED_ASSET_MANIFEST_RELATIVE_PATH


def is_local_only_licensed_asset_path(path: str | Path) -> bool:
    """Return ``True`` when the path lives in local-only licensed storage."""
    return is_local_only_licensed_path(path)


def is_commit_safe_licensed_asset_path(path: str | Path) -> bool:
    """Return ``True`` when the path is under commit-safe ignored storage."""
    return is_commit_safe_excluded_path(path)


@dataclass(frozen=True, slots=True)
class LicensedAssetReference:
    """Metadata-only reference for a local licensed asset."""

    asset_id: str
    system: str
    pricing_year: str
    kind: Literal[
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    ]
    source_refs: tuple[str, ...]
    local_path_hint: str
    restricted: bool
    license_boundary: Literal["local-only", "public-metadata"]
    license_acknowledgement: str
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "asset_id", _normalize_non_blank(self.asset_id, field="asset_id")
        )
        object.__setattr__(
            self,
            "system",
            _normalize_non_blank(self.system, field="system"),
        )
        object.__setattr__(
            self,
            "pricing_year",
            _normalize_non_blank(self.pricing_year, field="pricing_year"),
        )
        if self.kind not in {
            "public-metadata",
            "user-supplied-licensed-file",
            "derived-validation-fixture",
        }:
            raise LicensedAssetRegistryError(f"unsupported asset kind {self.kind!r}")
        object.__setattr__(
            self,
            "source_refs",
            _normalize_string_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self,
            "local_path_hint",
            _normalize_relative_path(self.local_path_hint, field="local_path_hint"),
        )
        if self.kind == "public-metadata":
            if self.restricted:
                raise LicensedAssetRegistryError(
                    "public-metadata assets must not be restricted"
                )
            if self.license_boundary != "public-metadata":
                raise LicensedAssetRegistryError(
                    "public-metadata assets must use the public-metadata boundary"
                )
        else:
            if not self.restricted:
                raise LicensedAssetRegistryError(
                    "licensed asset records must be restricted"
                )
            if self.license_boundary != "local-only":
                raise LicensedAssetRegistryError(
                    "licensed asset records must use the local-only boundary"
                )
            if not is_commit_safe_licensed_asset_path(self.local_path_hint):
                raise LicensedAssetRegistryError(
                    "licensed asset paths must be stored in commit-safe ignored storage"
                )
        object.__setattr__(
            self,
            "license_acknowledgement",
            _normalize_non_blank(
                self.license_acknowledgement, field="license_acknowledgement"
            ),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_string_tuple(self.notes, field="notes"),
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable asset record."""
        return {
            "asset_id": self.asset_id,
            "system": self.system,
            "pricing_year": self.pricing_year,
            "kind": self.kind,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "restricted": self.restricted,
            "license_boundary": self.license_boundary,
            "license_acknowledgement": self.license_acknowledgement,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class LicensedAssetManifest:
    """Local-only manifest for user-supplied licensed assets."""

    schema_version: str
    storage_root: str
    license_acknowledgement: dict[str, Any]
    assets: tuple[LicensedAssetReference, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "schema_version",
            _normalize_non_blank(self.schema_version, field="schema_version"),
        )
        if self.schema_version != LICENSED_ASSET_MANIFEST_SCHEMA_VERSION:
            raise LicensedAssetRegistryError(
                "unsupported schema_version for licensed asset manifest"
            )
        object.__setattr__(
            self,
            "storage_root",
            _normalize_relative_path(self.storage_root, field="storage_root"),
        )
        if self.storage_root != "archive/ihacpa/raw":
            raise LicensedAssetRegistryError(
                "storage_root must be archive/ihacpa/raw"
            )
        acknowledgement = self.license_acknowledgement
        if not isinstance(acknowledgement, Mapping):
            raise LicensedAssetRegistryError(
                "license_acknowledgement must be a mapping"
            )
        acknowledged = acknowledgement.get("acknowledged")
        statement = acknowledgement.get("statement")
        if acknowledged is not True:
            raise LicensedAssetRegistryError(
                "license_acknowledgement.acknowledged must be true"
            )
        _normalize_non_blank(statement, field="license_acknowledgement.statement")
        object.__setattr__(self, "assets", tuple(self.assets))
        if not self.assets:
            raise LicensedAssetRegistryError("assets must not be empty")
        asset_ids = [asset.asset_id for asset in self.assets]
        if len(set(asset_ids)) != len(asset_ids):
            raise LicensedAssetRegistryError(
                "assets must not contain duplicate asset_id values"
            )
        object.__setattr__(
            self, "notes", _normalize_string_tuple(self.notes, field="notes")
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable manifest payload."""
        return {
            "schema_version": self.schema_version,
            "storage_root": self.storage_root,
            "license_acknowledgement": dict(self.license_acknowledgement),
            "assets": [asset.to_dict() for asset in self.assets],
            "notes": list(self.notes),
        }


def build_licensed_asset_reference(
    *,
    asset_id: str,
    system: str,
    pricing_year: str,
    source_refs: Iterable[str],
    local_path_hint: str | Path,
    notes: Iterable[str] = (),
    license_acknowledgement: str = _LICENSE_ACKNOWLEDGEMENT,
) -> LicensedAssetReference:
    """Build a local-only licensed asset reference."""
    return LicensedAssetReference(
        asset_id=asset_id,
        system=system,
        pricing_year=pricing_year,
        kind="user-supplied-licensed-file",
        source_refs=tuple(source_refs),
        local_path_hint=str(local_path_hint),
        restricted=True,
        license_boundary="local-only",
        license_acknowledgement=license_acknowledgement,
        notes=tuple(notes),
    )


def build_licensed_asset_manifest(
    *,
    storage_root: str = "archive/ihacpa/raw",
    assets: Iterable[LicensedAssetReference],
    notes: Iterable[str] = (),
) -> LicensedAssetManifest:
    """Build a local-only licensed asset manifest."""
    return LicensedAssetManifest(
        schema_version=LICENSED_ASSET_MANIFEST_SCHEMA_VERSION,
        storage_root=storage_root,
        license_acknowledgement={
            "acknowledged": True,
            "statement": _LICENSE_ACKNOWLEDGEMENT,
        },
        assets=tuple(assets),
        notes=tuple(notes),
    )


def save_licensed_asset_manifest(
    manifest: LicensedAssetManifest,
    path: str | Path,
) -> None:
    """Write a licensed asset manifest to disk."""
    manifest_path = Path(path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_licensed_asset_manifest(path: str | Path) -> LicensedAssetManifest:
    """Load a licensed asset manifest from disk."""
    manifest_path = Path(path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise LicensedAssetRegistryError("licensed asset manifest must be a mapping")
    assets = []
    for raw_asset in payload.get("assets", []):
        if not isinstance(raw_asset, dict):
            raise LicensedAssetRegistryError("assets must be mappings")
        assets.append(
            LicensedAssetReference(
                asset_id=str(raw_asset["asset_id"]),
                system=str(raw_asset["system"]),
                pricing_year=str(raw_asset["pricing_year"]),
                kind=cast(
                    Literal[
                        "public-metadata",
                        "user-supplied-licensed-file",
                        "derived-validation-fixture",
                    ],
                    raw_asset["kind"],
                ),
                source_refs=tuple(raw_asset.get("source_refs", ())),
                local_path_hint=str(raw_asset["local_path_hint"]),
                restricted=bool(raw_asset["restricted"]),
                license_boundary=cast(
                    Literal["local-only", "public-metadata"],
                    raw_asset.get("license_boundary", "local-only"),
                ),
                license_acknowledgement=str(raw_asset["license_acknowledgement"]),
                notes=tuple(raw_asset.get("notes", ())),
            )
        )
    return LicensedAssetManifest(
        schema_version=str(payload["schema_version"]),
        storage_root=str(payload["storage_root"]),
        license_acknowledgement=dict(payload["license_acknowledgement"]),
        assets=tuple(assets),
        notes=tuple(payload.get("notes", ())),
    )


def ensure_licensed_asset_manifest(
    path: str | Path,
) -> LicensedAssetManifest:
    """Load a manifest or raise a registry error."""
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise LicensedAssetRegistryError(
            f"licensed asset manifest does not exist: {manifest_path}"
        )
    return load_licensed_asset_manifest(manifest_path)


def _existing_paths(existing_paths: Iterable[str | Path]) -> set[str]:
    return {
        _normalize_relative_path(path, field="existing_paths")
        for path in existing_paths
    }


def _asset_present(asset: LicensedAssetReference, existing_paths: set[str]) -> bool:
    return asset.local_path_hint in existing_paths


def validate_licensed_asset_manifest(
    manifest: LicensedAssetManifest | str | Path,
    *,
    existing_paths: Iterable[str | Path] = (),
) -> dict[str, Any]:
    """Validate a manifest and report whether local assets are present."""
    loaded = (
        ensure_licensed_asset_manifest(manifest)
        if isinstance(manifest, (str, Path))
        else manifest
    )
    existing = _existing_paths(existing_paths)
    missing_assets = [
        {
            "asset_id": asset.asset_id,
            "system": asset.system,
            "pricing_year": asset.pricing_year,
            "local_path_hint": asset.local_path_hint,
            "missing_category": (
                "licensed-local-asset"
                if asset.restricted
                else "public-metadata"
            ),
            "safe_message": (
                f"{asset.system} {asset.pricing_year} is missing local licensed asset "
                f"category {asset.asset_id!r}"
            ),
        }
        for asset in loaded.assets
        if asset.restricted and not _asset_present(asset, existing)
    ]
    status = "validated" if not missing_assets else "blocked"
    support_status = "executable" if not missing_assets else "blocked_licensed"
    return {
        "status": status,
        "support_status": support_status,
        "manifest": loaded.to_dict(),
        "missing_assets": missing_assets,
    }


def doctor_licensed_assets(
    manifest: LicensedAssetManifest | str | Path,
    *,
    existing_paths: Iterable[str | Path] = (),
) -> dict[str, Any]:
    """Return a fail-closed status report for a licensed asset manifest."""
    report = validate_licensed_asset_manifest(
        manifest,
        existing_paths=existing_paths,
    )
    report["status"] = (
        "blocked_licensed" if report["missing_assets"] else "ready"
    )
    return report


def register_licensed_asset_manifest(
    *,
    manifest_path: str | Path,
    system: str,
    pricing_year: str,
    source_refs: Iterable[str],
    local_path_hint: str | Path,
    acknowledge_license: bool,
    notes: Iterable[str] = (),
) -> LicensedAssetManifest:
    """Create and persist a local licensed asset manifest."""
    if not acknowledge_license:
        raise LicensedAssetRegistryError(
            "license acknowledgement is required before registering assets"
        )
    notes_tuple = tuple(notes)
    asset = build_licensed_asset_reference(
        asset_id=f"{system.lower()}-{pricing_year}",
        system=system,
        pricing_year=pricing_year,
        source_refs=tuple(source_refs),
        local_path_hint=local_path_hint,
        notes=notes_tuple,
    )
    manifest = build_licensed_asset_manifest(assets=(asset,), notes=notes_tuple)
    save_licensed_asset_manifest(manifest, manifest_path)
    return manifest


def _tracked_paths(root: Path) -> tuple[Path, ...]:
    git_dir = root / ".git"
    if git_dir.exists():
        git_executable = which("git") or "git"
        completed = subprocess.run(  # noqa: S603
            [
                git_executable,
                "-C",
                str(root),
                "ls-files",
                "-co",
                "--exclude-standard",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return tuple(
            root / line
            for line in completed.stdout.splitlines()
            if line.strip()
        )
    return tuple(path for path in root.rglob("*") if path.is_file())


def audit_restricted_asset_signatures(root: str | Path) -> dict[str, Any]:
    """Scan for tracked restricted-asset signatures and report findings."""
    root_path = Path(root)
    findings: list[dict[str, Any]] = []
    for path in _tracked_paths(root_path):
        try:
            relative = path.relative_to(root_path).as_posix()
        except ValueError:
            continue
        if relative in _ALLOWED_LOCAL_MANIFEST_NAMES:
            continue
        if relative == LICENSED_ASSET_MANIFEST_RELATIVE_PATH.as_posix():
            continue
        if relative.startswith(_ALLOWED_REPOSITORY_PREFIXES):
            continue
        if relative.startswith("archive/ihacpa/raw/"):
            findings.append(
                {
                    "path": relative,
                    "signature": "restricted-raw-asset",
                    "safe_message": (
                        "restricted raw assets must stay out of version control"
                    ),
                }
            )
            continue
        suffix = path.suffix.lower()
        for signature, suffixes in _FORBIDDEN_SIGNATURES.items():
            if suffix in suffixes:
                findings.append(
                    {
                        "path": relative,
                        "signature": signature,
                        "safe_message": (
                            f"file {relative!r} matches the licensed asset signature "
                            f"{signature!r}"
                        ),
                    }
                )
                break
    return {
        "status": "blocked" if findings else "pass",
        "support_status": "blocked_licensed" if findings else "executable",
        "findings": findings,
        "root": root_path.as_posix(),
    }
