"""Offline diffing for repository-local IHACPA pricing-year manifests."""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from nwau_py.reference_manifest import ReferenceDataManifest, load_reference_manifest

__all__ = [
    "FieldChange",
    "ItemChange",
    "PricingYearDiffReport",
    "compare_pricing_year_manifests",
    "format_pricing_year_diff_report",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_REFERENCE_DATA_ROOT = "reference-data"


@dataclass(frozen=True, slots=True)
class FieldChange:
    """A single changed field path and its before/after values."""

    path: str
    before: Any
    after: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "before": _jsonable(self.before),
            "after": _jsonable(self.after),
        }


@dataclass(frozen=True, slots=True)
class ItemChange:
    """A named record change within a manifest section."""

    key: str
    change_type: str
    changes: tuple[FieldChange, ...] = ()
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "change_type": self.change_type,
            "changes": [change.to_dict() for change in self.changes],
            "before": _jsonable(self.before),
            "after": _jsonable(self.after),
        }


@dataclass(frozen=True, slots=True)
class PricingYearDiffReport:
    """Conservative offline comparison between two pricing-year manifests."""

    from_year: str
    to_year: str
    from_manifest_path: Path
    to_manifest_path: Path
    constants: tuple[ItemChange, ...]
    coding_sets: tuple[ItemChange, ...]
    source_artifacts: tuple[ItemChange, ...]
    validation: tuple[FieldChange, ...]
    gaps: tuple[ItemChange, ...]

    @property
    def summary(self) -> dict[str, int]:
        """Return a compact count summary for the diff report."""
        return {
            "constants_changed": len(self.constants),
            "coding_sets_changed": len(self.coding_sets),
            "source_artifacts_changed": len(self.source_artifacts),
            "validation_changed": int(bool(self.validation)),
            "gaps_added": sum(1 for item in self.gaps if item.change_type == "added"),
            "gaps_removed": sum(
                1 for item in self.gaps if item.change_type == "removed"
            ),
            "gaps_changed": sum(
                1 for item in self.gaps if item.change_type == "changed"
            ),
        }

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable comparison report."""
        return {
            "from_year": self.from_year,
            "to_year": self.to_year,
            "from_manifest_path": self.from_manifest_path.as_posix(),
            "to_manifest_path": self.to_manifest_path.as_posix(),
            "summary": self.summary,
            "constants": [item.to_dict() for item in self.constants],
            "coding_sets": [item.to_dict() for item in self.coding_sets],
            "source_artifacts": [item.to_dict() for item in self.source_artifacts],
            "validation": [change.to_dict() for change in self.validation],
            "gaps": [item.to_dict() for item in self.gaps],
        }


def _validate_year_label(year: str) -> str:
    if year.strip() != year:
        raise ValueError("year must not contain leading or trailing whitespace")
    if not _YEAR_RE.fullmatch(year):
        raise ValueError("year must be a supported four-digit IHACPA label")
    return year


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _reference_manifest_path(repo_root: Path, year: str) -> Path:
    return repo_root / _REFERENCE_DATA_ROOT / year / "manifest.yaml"


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _to_plain_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError(f"unsupported record type: {type(value)!r}")


def _diff_mappings(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    prefix: str,
) -> tuple[FieldChange, ...]:
    changes: list[FieldChange] = []
    for key in sorted(str(item) for item in (set(before) | set(after))):
        path = f"{prefix}.{key}" if prefix else str(key)
        if key not in before:
            changes.append(FieldChange(path=path, before=None, after=after[key]))
            continue
        if key not in after:
            changes.append(FieldChange(path=path, before=before[key], after=None))
            continue

        left = before[key]
        right = after[key]
        if isinstance(left, Mapping) and isinstance(right, Mapping):
            changes.extend(
                _diff_mappings(left, right, prefix=path),
            )
        elif left != right:
            changes.append(FieldChange(path=path, before=left, after=right))
    return tuple(changes)


def _compare_record_sections(
    before_items: Sequence[Any],
    after_items: Sequence[Any],
    *,
    key_fn: Callable[[dict[str, Any]], str],
) -> tuple[ItemChange, ...]:
    before_map = {
        key_fn(plain): plain
        for plain in (_to_plain_dict(item) for item in before_items)
    }
    after_map = {
        key_fn(plain): plain for plain in (_to_plain_dict(item) for item in after_items)
    }

    changes: list[ItemChange] = []
    for key in sorted(str(item) for item in (set(before_map) | set(after_map))):
        before_item = before_map.get(key)
        after_item = after_map.get(key)
        if before_item is None:
            changes.append(
                ItemChange(
                    key=key,
                    change_type="added",
                    after=after_item,
                )
            )
            continue
        if after_item is None:
            changes.append(
                ItemChange(
                    key=key,
                    change_type="removed",
                    before=before_item,
                )
            )
            continue

        field_changes = _diff_mappings(before_item, after_item, prefix="")
        if field_changes:
            changes.append(
                ItemChange(
                    key=key,
                    change_type="changed",
                    changes=field_changes,
                    before=before_item,
                    after=after_item,
                )
            )
    return tuple(changes)


def _compare_validation(
    before_manifest: ReferenceDataManifest,
    after_manifest: ReferenceDataManifest,
) -> tuple[FieldChange, ...]:
    before = {
        "current_pricing_year": before_manifest.current_pricing_year,
        "validation_status": before_manifest.validation_status,
        "validation": before_manifest.validation.model_dump(mode="json"),
    }
    after = {
        "current_pricing_year": after_manifest.current_pricing_year,
        "validation_status": after_manifest.validation_status,
        "validation": after_manifest.validation.model_dump(mode="json"),
    }
    return _diff_mappings(before, after, prefix="")


def compare_pricing_year_manifests(
    from_year: str,
    to_year: str,
    *,
    repo_root: Path | str | None = None,
) -> PricingYearDiffReport:
    """Compare two local reference-data manifests without using the network."""
    normalized_from_year = _validate_year_label(from_year)
    normalized_to_year = _validate_year_label(to_year)
    root = Path(repo_root) if repo_root is not None else _default_repo_root()

    from_manifest_path = _reference_manifest_path(root, normalized_from_year)
    to_manifest_path = _reference_manifest_path(root, normalized_to_year)
    from_manifest = load_reference_manifest(from_manifest_path)
    to_manifest = load_reference_manifest(to_manifest_path)

    constants = _compare_record_sections(
        [from_manifest.constants],
        [to_manifest.constants],
        key_fn=lambda _: "constants",
    )
    coding_sets = _compare_record_sections(
        from_manifest.coding_sets,
        to_manifest.coding_sets,
        key_fn=lambda item: item["name"],
    )
    source_artifacts = _compare_record_sections(
        from_manifest.source_artifacts,
        to_manifest.source_artifacts,
        key_fn=lambda item: f"{item['kind']} :: {item['service_stream']}",
    )
    validation = _compare_validation(from_manifest, to_manifest)
    gaps = _compare_record_sections(
        from_manifest.gaps,
        to_manifest.gaps,
        key_fn=lambda item: f"{item['scope']} :: {item['kind']}",
    )

    return PricingYearDiffReport(
        from_year=normalized_from_year,
        to_year=normalized_to_year,
        from_manifest_path=from_manifest_path,
        to_manifest_path=to_manifest_path,
        constants=constants,
        coding_sets=coding_sets,
        source_artifacts=source_artifacts,
        validation=validation,
        gaps=gaps,
    )


def _format_value(value: Any) -> str:
    normalized = _jsonable(value)
    if isinstance(normalized, str):
        return f"`{normalized}`"
    return f"`{json.dumps(normalized, sort_keys=True)}`"


def _format_changes(changes: Sequence[FieldChange]) -> str:
    return "; ".join(
        f"`{change.path}`: "
        f"{_format_value(change.before)} -> {_format_value(change.after)}"
        for change in changes
    )


def _format_item_change(
    item: ItemChange,
    *,
    include_payload: bool = False,
) -> list[str]:
    if item.change_type == "changed":
        return [f"- `{item.key}`: {_format_changes(item.changes)}"]

    payload = item.after if item.change_type == "added" else item.before
    if payload is None:
        return [f"- `{item.key}`: {item.change_type}"]

    if include_payload:
        rendered = json.dumps(_jsonable(payload), sort_keys=True)
        return [f"- `{item.key}`: {item.change_type} {rendered}"]

    return [f"- `{item.key}`: {item.change_type}"]


def format_pricing_year_diff_report(report: PricingYearDiffReport) -> str:
    """Render a markdown diff summary for two pricing-year manifests."""
    lines = [
        f"# Pricing-year diff: {report.from_year} -> {report.to_year}",
        "",
        "## Summary",
        f"- constants changed: {report.summary['constants_changed']}",
        f"- coding sets changed: {report.summary['coding_sets_changed']}",
        f"- source artifacts changed: {report.summary['source_artifacts_changed']}",
        f"- validation changed: {bool(report.summary['validation_changed'])}",
        f"- gaps added: {report.summary['gaps_added']}",
        f"- gaps removed: {report.summary['gaps_removed']}",
        f"- gaps changed: {report.summary['gaps_changed']}",
        "",
        "## Constants",
    ]

    if report.constants:
        for item in report.constants:
            lines.extend(_format_item_change(item, include_payload=True))
    else:
        lines.append("- no changes")

    lines.extend(["", "## Coding sets"])
    if report.coding_sets:
        for item in report.coding_sets:
            lines.extend(_format_item_change(item, include_payload=True))
    else:
        lines.append("- no changes")

    lines.extend(["", "## Source artifacts"])
    if report.source_artifacts:
        for item in report.source_artifacts:
            lines.extend(_format_item_change(item, include_payload=True))
    else:
        lines.append("- no changes")

    lines.extend(["", "## Validation"])
    if report.validation:
        lines.extend(
            (
                f"- `{change.path}`: "
                f"{_format_value(change.before)} -> {_format_value(change.after)}"
            )
            for change in report.validation
        )
    else:
        lines.append("- no changes")

    lines.extend(["", "## Gaps"])
    if report.gaps:
        for item in report.gaps:
            lines.extend(_format_item_change(item, include_payload=True))
    else:
        lines.append("- no changes")

    return "\n".join(lines)
