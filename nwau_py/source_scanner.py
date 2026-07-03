"""Offline-testable discovery helpers for IHACPA source scanning.

The scanner works from supplied HTML/text fixtures or explicit URL lists. It
does not fetch remote content, so tests can exercise discovery and manifest
drafting without network access or licensed downloads.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urljoin, urlsplit

from nwau_py.provenance import ArtifactKind

SUPPORTED_SOURCE_SCAN_SCHEMA_VERSION = "1"
SUPPORTED_SOURCE_SCAN_STATUSES = ("source-discovered", "source-only", "gap-explicit")
SUPPORTED_GAP_KINDS = (
    "source_missing",
    "parse_failure",
    "scope_unknown",
    "license_unclear",
    "review_required",
)
DEFAULT_AUDIT_TRACK_TITLE = "IHACPA Source/License Audit Automation"
DEFAULT_AUDIT_ISSUE_TITLE = (
    "chore: automate IHACPA source and license audit with track and issue drafting"
)
DEFAULT_AUDIT_ISSUE_LABELS = ("enhancement", "ci", "docs", "codex")

_URL_RE = re.compile(r"https?://[^\s<>'\"()]+", re.IGNORECASE)
_YEAR_RE = re.compile(r"\b(20\d{2})(?:[-/](\d{2,4}))?\b")
_WHITESPACE_RE = re.compile(r"\s+")


class SourceScannerError(ValueError):
    """Raised when supplied source inputs cannot be parsed."""


SourceScanError = SourceScannerError


@dataclass(frozen=True, slots=True)
class SourceDocument:
    """Input document supplied to the scanner."""

    kind: Literal["html", "text", "urls"]
    name: str
    content: str
    source_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.name,
            "content": self.content,
            "source_url": self.source_url,
        }


@dataclass(frozen=True, slots=True)
class SourceDiscovery:
    """A discovered source candidate from HTML/text/URL input."""

    source_url: str
    label: str
    source_kind: Literal["html-link", "text-url", "explicit-url"]
    source_document: str
    host: str
    filename: str
    artifact_kind: str
    source_category: str
    year_label: str | None = None
    year_start: int | None = None
    review_required: bool = False
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "label": self.label,
            "source_kind": self.source_kind,
            "source_document": self.source_document,
            "host": self.host,
            "filename": self.filename,
            "artifact_kind": self.artifact_kind,
            "source_category": self.source_category,
            "year_label": self.year_label,
            "year_start": self.year_start,
            "review_required": self.review_required,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class SourceGapRecord:
    """Explicit record for a missing, ambiguous, or blocked source."""

    gap_id: str
    kind: Literal[
        "source_missing",
        "parse_failure",
        "scope_unknown",
        "license_unclear",
        "review_required",
    ]
    scope: str
    reason: str
    expected_resolution: str
    status: Literal["open", "tracked", "resolved"] = "open"
    related_url: str | None = None
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "kind": self.kind,
            "scope": self.scope,
            "reason": self.reason,
            "expected_resolution": self.expected_resolution,
            "status": self.status,
            "related_url": self.related_url,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class SourceDraftManifest:
    """Draft manifest produced from discovery-only scanning."""

    schema_version: str
    generated_at: str
    scan_id: str
    source_page_url: str | None
    pricing_year: str | None
    validation_status: str
    dry_run: bool
    documents: tuple[SourceDocument, ...]
    discoveries: tuple[SourceDiscovery, ...]
    gaps: tuple[SourceGapRecord, ...]
    notes: tuple[str, ...] = ()

    def unresolved_gaps(self) -> tuple[SourceGapRecord, ...]:
        return tuple(gap for gap in self.gaps if gap.status != "resolved")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "scan_id": self.scan_id,
            "source_page_url": self.source_page_url,
            "pricing_year": self.pricing_year,
            "validation_status": self.validation_status,
            "dry_run": self.dry_run,
            "documents": [document.to_dict() for document in self.documents],
            "discoveries": [discovery.to_dict() for discovery in self.discoveries],
            "gaps": [gap.to_dict() for gap in self.gaps],
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class SourceScanResult:
    """Convenience wrapper with the draft manifest and rendered dry-run text."""

    manifest: SourceDraftManifest
    dry_run_output: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest.to_dict(),
            "dry_run_output": self.dry_run_output,
        }


@dataclass(frozen=True, slots=True)
class SourceAuditPackage:
    """Review-only package for drafting source audit outputs."""

    scan_manifest: SourceDraftManifest
    track_id: str
    track_title: str
    github_issue_number: int | None
    github_issue_url: str | None
    draft_manifest_json: str
    track_metadata: dict[str, Any]
    track_spec: str
    track_plan: str
    track_index: str
    tracks_registry_entry: str
    github_issue_title: str
    github_issue_body: str
    github_issue_labels: tuple[str, ...]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "scan_manifest": self.scan_manifest.to_dict(),
            "track_id": self.track_id,
            "track_title": self.track_title,
            "github_issue_number": self.github_issue_number,
            "github_issue_url": self.github_issue_url,
            "draft_manifest_json": self.draft_manifest_json,
            "track": {
                "metadata": self.track_metadata,
                "spec": self.track_spec,
                "plan": self.track_plan,
                "index": self.track_index,
                "tracks_registry_entry": self.tracks_registry_entry,
            },
            "github_issue": {
                "title": self.github_issue_title,
                "body": self.github_issue_body,
                "labels": list(self.github_issue_labels),
            },
            "summary": self.summary,
        }


class _HTMLLinkParser(HTMLParser):
    """Collect anchor tags from supplied HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str, str]] = []
        self._href: str | None = None
        self._heading_tag: str | None = None
        self._chunks: list[str] = []
        self._heading_chunks: list[str] = []
        self._current_heading: str = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized_tag = tag.lower()
        if normalized_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = normalized_tag
            self._heading_chunks = []
            return
        if normalized_tag != "a":
            return
        attr_map = {key.lower(): value for key, value in attrs}
        self._href = attr_map.get("href")
        self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._chunks.append(data)
        elif self._heading_tag is not None:
            self._heading_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()
        if normalized_tag == self._heading_tag:
            self._current_heading = _normalize_whitespace(
                "".join(self._heading_chunks)
            )
            self._heading_tag = None
            self._heading_chunks = []
            return
        if normalized_tag != "a" or self._href is None:
            return
        text = _normalize_whitespace("".join(self._chunks))
        self.links.append((self._href, text, self._current_heading))
        self._href = None
        self._chunks = []


def _normalize_whitespace(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value).strip()


def _load_text_input(source: str | Path) -> tuple[str, str]:
    """Load a fixture path or inline text value."""
    if isinstance(source, Path):
        return source.read_text(encoding="utf-8"), source.as_posix()
    candidate = Path(source)
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(encoding="utf-8"), candidate.as_posix()
    return source, "inline"


def _coerce_documents(
    *,
    html_documents: tuple[str | Path, ...] = (),
    text_documents: tuple[str | Path, ...] = (),
) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for index, source in enumerate(html_documents, start=1):
        content, name = _load_text_input(source)
        documents.append(
            SourceDocument(kind="html", name=name or f"html-{index}", content=content)
        )
    for index, source in enumerate(text_documents, start=1):
        content, name = _load_text_input(source)
        documents.append(
            SourceDocument(kind="text", name=name or f"text-{index}", content=content)
        )
    return documents


def _normalize_url(url: str, *, base_url: str | None = None) -> str:
    url = url.strip().rstrip(".,;)")
    if base_url is not None:
        url = urljoin(base_url, url)
    return url


def _extract_urls_from_text(text: str, *, base_url: str | None = None) -> list[str]:
    return [
        _normalize_url(match.group(0), base_url=base_url)
        for match in _URL_RE.finditer(text)
    ]


def _extract_year(url: str, label: str) -> tuple[str | None, int | None]:
    for value in (label, url):
        match = _YEAR_RE.search(value)
        if match is None:
            continue
        start = int(match.group(1))
        end = match.group(2)
        if end is None:
            return str(start), start
        end_year = int(end)
        if len(end) == 2:
            century = start // 100 * 100
            end_year = century + end_year
            if end_year < start:
                end_year += 100
        return f"{start}-{str(end_year)[-2:]}", start
    return None, None


def _infer_host(url: str) -> str:
    parsed = urlsplit(url)
    return parsed.netloc.lower()


def _infer_filename(url: str) -> str:
    parsed = urlsplit(url)
    return Path(parsed.path).name


def _infer_artifact_kind(url: str, label: str) -> str:
    candidate = f"{url} {label}".lower()
    if any(token in candidate for token in (".xlsb", ".xlsx", ".xls")):
        return ArtifactKind.EXCEL.value
    if any(token in candidate for token in (".zip", ".rar", ".7z")):
        return ArtifactKind.SUPPORT.value
    if ".pdf" in candidate:
        return ArtifactKind.DOCUMENTATION.value
    if any(token in candidate for token in (".htm", ".html")):
        return ArtifactKind.DOCUMENTATION.value
    if "sas" in candidate:
        return ArtifactKind.SAS.value
    return ArtifactKind.UNKNOWN.value


def _infer_source_category(label: str, url: str) -> str:
    candidate = f"{label} {url}".lower()
    if "technical specification" in candidate or "specification" in candidate:
        return "technical-specification"
    if any(token in candidate for token in ("price weight", "price-weight", "weights")):
        return "price-weights"
    if "calculator" in candidate or "calculation" in candidate:
        return "calculator"
    if any(
        token in candidate for token in ("classification", "classification resource")
    ):
        return "classification-resource"
    if any(token in candidate for token in ("report", "reports")):
        return "report"
    return "discovery"


def _make_discovery(
    *,
    source_url: str,
    label: str,
    source_kind: Literal["html-link", "text-url", "explicit-url"],
    source_document: str,
    base_url: str | None = None,
    pricing_year: str | None = None,
) -> SourceDiscovery:
    url = _normalize_url(source_url, base_url=base_url)
    host = _infer_host(url)
    filename = _infer_filename(url)
    resolved_label = _normalize_whitespace(label) or filename or url
    year_label, year_start = _extract_year(url, resolved_label)
    if year_label is None and pricing_year is not None:
        year_label = pricing_year
        try:
            year_start = int(pricing_year)
        except ValueError:
            year_start = None
    review_required = host.endswith("box.com") or ".box.com" in host
    notes = []
    if review_required:
        notes.append("external-hosted content discovered without download")
    if not filename:
        notes.append("URL does not include a filename")
    return SourceDiscovery(
        source_url=url,
        label=resolved_label,
        source_kind=source_kind,
        source_document=source_document,
        host=host,
        filename=filename,
        artifact_kind=_infer_artifact_kind(url, resolved_label),
        source_category=_infer_source_category(resolved_label, url),
        year_label=year_label,
        year_start=year_start,
        review_required=review_required,
        notes=tuple(notes),
    )


def _discover_html(
    document: SourceDocument, *, base_url: str | None, pricing_year: str | None
) -> list[SourceDiscovery]:
    parser = _HTMLLinkParser()
    try:
        parser.feed(document.content)
    except Exception as exc:  # pragma: no cover - HTMLParser is rarely fatal
        raise SourceScannerError(
            f"failed to parse HTML document {document.name}: {exc}"
        ) from exc
    discoveries: list[SourceDiscovery] = []
    for href, text, heading in parser.links:
        if not href:
            continue
        label = text or _infer_filename(href)
        if _extract_year(href, label)[0] is None:
            if not heading:
                continue
            label = f"{heading} {label}"
        discoveries.append(
            _make_discovery(
                source_url=href,
                label=label,
                source_kind="html-link",
                source_document=document.name,
                base_url=base_url,
                pricing_year=pricing_year,
            )
        )
    return discoveries


def _discover_text(
    document: SourceDocument, *, base_url: str | None, pricing_year: str | None
) -> list[SourceDiscovery]:
    discoveries: list[SourceDiscovery] = []
    for line in document.content.splitlines():
        urls = _extract_urls_from_text(line, base_url=base_url)
        if not urls:
            continue
        label = _normalize_whitespace(_URL_RE.split(line, maxsplit=1)[0])
        discoveries.extend(
            _make_discovery(
                source_url=url,
                label=label or _infer_filename(url),
                source_kind="text-url",
                source_document=document.name,
                base_url=base_url,
                pricing_year=pricing_year,
            )
            for url in urls
        )
    return discoveries


def _discover_explicit_urls(
    urls: tuple[str, ...], *, pricing_year: str | None
) -> list[SourceDiscovery]:
    return [
            _make_discovery(
                source_url=url,
                label=_infer_filename(url),
                source_kind="explicit-url",
                source_document="url-list",
                base_url=None,
                pricing_year=pricing_year,
            )
        for url in urls
    ]


def _build_gap_records(
    discoveries: tuple[SourceDiscovery, ...],
    *,
    source_page_url: str | None,
) -> tuple[SourceGapRecord, ...]:
    gaps: list[SourceGapRecord] = []
    for index, discovery in enumerate(discoveries, start=1):
        if discovery.review_required:
            gaps.append(
                SourceGapRecord(
                    gap_id=f"gap-{index:03d}",
                    kind="license_unclear",
                    scope=discovery.source_url,
                    reason=(
                        "external-hosted content was discovered, but no download "
                        "was attempted"
                    ),
                    expected_resolution=(
                        "review licensing and access terms before downloading"
                    ),
                    related_url=discovery.source_url,
                    notes=discovery.notes,
                )
            )
        if not discovery.filename:
            gaps.append(
                SourceGapRecord(
                    gap_id=f"gap-{index:03d}-filename",
                    kind="scope_unknown",
                    scope=discovery.source_url,
                    reason="the discovered URL did not expose a filename",
                    expected_resolution=(
                        "add a descriptive link label or explicit file name"
                    ),
                    related_url=discovery.source_url,
                )
            )
    if not discoveries:
        gaps.append(
            SourceGapRecord(
                gap_id="gap-001",
                kind="source_missing",
                scope=source_page_url or "unspecified source inputs",
                reason="no source links were discovered from the supplied inputs",
                expected_resolution="supply a fixture with source links or a URL list",
                related_url=source_page_url,
            )
        )
    return tuple(gaps)


def scan_sources(
    *,
    html_documents: tuple[str | Path, ...] = (),
    text_documents: tuple[str | Path, ...] = (),
    urls: tuple[str, ...] = (),
    source_page_url: str | None = None,
    pricing_year: str | None = None,
    scan_id: str = "ihacpa-source-scan",
    dry_run: bool = True,
) -> SourceDraftManifest:
    """Discover source candidates from offline fixtures and explicit URL lists."""
    documents = tuple(
        _coerce_documents(html_documents=html_documents, text_documents=text_documents)
    )
    discoveries: list[SourceDiscovery] = []
    for document in documents:
        if document.kind == "html":
            discoveries.extend(
                _discover_html(
                    document,
                    base_url=source_page_url,
                    pricing_year=pricing_year,
                )
            )
        elif document.kind == "text":
            discoveries.extend(
                _discover_text(
                    document,
                    base_url=source_page_url,
                    pricing_year=pricing_year,
                )
            )
    discoveries.extend(_discover_explicit_urls(urls, pricing_year=pricing_year))

    unique: dict[tuple[str, str], SourceDiscovery] = {}
    for discovery in discoveries:
        key = (discovery.source_url, discovery.source_kind)
        current = unique.get(key)
        if current is None:
            unique[key] = discovery
            continue
        if len(discovery.label) > len(current.label):
            unique[key] = discovery
    merged_discoveries = tuple(unique[key] for key in sorted(unique))
    gaps = _build_gap_records(merged_discoveries, source_page_url=source_page_url)
    validation_status = (
        "gap-explicit"
        if gaps and any(g.kind != "source_missing" for g in gaps)
        else "source-discovered"
    )
    generated_at = datetime.now(timezone.utc).isoformat()
    return SourceDraftManifest(
        schema_version=SUPPORTED_SOURCE_SCAN_SCHEMA_VERSION,
        generated_at=generated_at,
        scan_id=scan_id,
        source_page_url=source_page_url,
        pricing_year=pricing_year,
        validation_status=validation_status,
        dry_run=dry_run,
        documents=documents,
        discoveries=merged_discoveries,
        gaps=gaps,
        notes=(
            "discovery-only output; no remote content was fetched",
            "licensed material was not downloaded",
        ),
    )


def render_dry_run(manifest: SourceDraftManifest) -> str:
    """Render a review-friendly dry-run summary."""
    lines = [
        "IHACPA source scanner dry-run",
        f"scan_id: {manifest.scan_id}",
        f"generated_at: {manifest.generated_at}",
        f"source_page_url: {manifest.source_page_url or '-'}",
        f"pricing_year: {manifest.pricing_year or '-'}",
        f"validation_status: {manifest.validation_status}",
        f"documents: {len(manifest.documents)}",
        f"discoveries: {len(manifest.discoveries)}",
        f"gaps: {len(manifest.gaps)}",
        "",
        "discoveries:",
    ]
    if manifest.discoveries:
        for item in manifest.discoveries:
            line = (
                f"- {item.label} | {item.source_url} | {item.artifact_kind} | "
                f"{item.source_kind}"
            )
            if item.year_label:
                line += f" | year={item.year_label}"
            if item.review_required:
                line += " | review-required"
            lines.append(line)
    else:
        lines.append("- none")
    lines.extend(["", "gaps:"])
    if manifest.gaps:
        for gap in manifest.gaps:
            line = f"- {gap.gap_id} | {gap.kind} | {gap.scope} | {gap.reason}"
            lines.append(line)
    else:
        lines.append("- none")
    return "\n".join(lines)


def scan_sources_dry_run(
    *,
    html_documents: tuple[str | Path, ...] = (),
    text_documents: tuple[str | Path, ...] = (),
    urls: tuple[str, ...] = (),
    source_page_url: str | None = None,
    pricing_year: str | None = None,
    scan_id: str = "ihacpa-source-scan",
) -> SourceScanResult:
    """Return the manifest and rendered dry-run output together."""
    manifest = scan_sources(
        html_documents=html_documents,
        text_documents=text_documents,
        urls=urls,
        source_page_url=source_page_url,
        pricing_year=pricing_year,
        scan_id=scan_id,
        dry_run=True,
    )
    return SourceScanResult(manifest=manifest, dry_run_output=render_dry_run(manifest))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _render_source_audit_track_metadata(
    manifest: SourceDraftManifest,
    *,
    track_id: str,
    github_issue_number: int | None,
    github_issue_url: str | None,
) -> dict[str, Any]:
    now = _utc_now_iso()
    return {
        "track_id": track_id,
        "type": "chore",
        "status": "in_progress",
        "track_class": "audit",
        "current_state": "in_progress",
        "primary_contract": (
            "nwau_py.source_scanner review-only source audit package generation for "
            "manifest drafts, Conductor track scaffolds, and GitHub issue updates"
        ),
        "dependencies": [
            "conductor/archive/ihacpa_source_scanner_20260512",
            "conductor/roadmap-governance.md",
            "conductor/track-archive-policy.md",
        ],
        "completion_evidence": [
            "tests",
            "cli",
            "docs",
            "draft-package-rendering",
        ],
        "publication_status": "not-ready",
        "created_at": now,
        "updated_at": now,
        "description": (
            "Automate IHACPA source and license audits that draft manifests, "
            "Conductor tracks, and GitHub issue updates without committing "
            "restricted assets."
        ),
        "no_stub_enforce": True,
        "support_scope": (
            "Review-only audit package generation, draft Conductor track "
            "scaffolding, and GitHub issue update text for public or licensed "
            "IHACPA source discovery."
        ),
        "github_issue_number": github_issue_number,
        "github_issue_url": github_issue_url,
        "scan_manifest_generated_at": manifest.generated_at,
        "scan_manifest_id": manifest.scan_id,
    }


def _render_source_audit_spec(
    manifest: SourceDraftManifest,
    *,
    github_issue_url: str | None,
) -> str:
    issue_line = github_issue_url or "(GitHub issue link not supplied)"
    pricing_year = manifest.pricing_year or "unspecified"
    return "\n".join(
        [
            f"# Specification: {DEFAULT_AUDIT_TRACK_TITLE}",
            "",
            "## Overview",
            "Add review-only automation that turns IHACPA source-scanner output into",
            "draft artifacts for source manifests, Conductor tracks, and GitHub",
            "issue updates. The automation must preserve the existing",
            "non-redistribution boundary: public metadata and review summaries may",
            "be drafted, but restricted assets must never be copied into the",
            "repository.",
            "",
            "## Contract",
            "- Scanner output remains the source of truth for discovered URLs, gaps,",
            "  and review status.",
            "- Draft artifacts may include manifest text, Conductor track scaffolds,",
            "  and GitHub issue bodies.",
            "- Restricted or licensed source content must remain referenced, not",
            "  copied.",
            "- The audit package must be deterministic for the same scanner input.",
            "- Draft outputs must not overstate validation, parity, or publication",
            "  readiness.",
            "",
            "## Functional Requirements",
            "- Build a review-only audit package from source scanner results.",
            "- Render draft Conductor track metadata, spec, plan, and registry text",
            "  from the scanner package.",
            "- Render a GitHub issue body that summarizes the audit boundary and",
            "  validation expectations.",
            "- Preserve gap records, review notes, and licensing caveats in the",
            "  generated drafts.",
            "- Expose the package through the installed CLI so maintainers can",
            "  generate drafts from offline fixtures or URL lists.",
            "",
            "## Non-Functional Requirements",
            "- The automation must not require live IHACPA access in CI.",
            "- The generated drafts must remain conservative and human-reviewable.",
            "- The implementation must keep restricted content out of version",
            "  control.",
            "- The package should be easy to reuse for future audit or discovery",
            "  tracks.",
            "",
            "## Acceptance Criteria",
            "- A source scan can produce an audit package with manifest, track, and",
            "  issue draft text.",
            "- The draft issue body links to the local Conductor track path and",
            "  states the licensing boundary.",
            "- The draft Conductor track includes metadata, spec, plan, and registry",
            "  entry text.",
            "- The CLI can emit the audit package without mutating restricted source",
            "  material.",
            "- Tests prove the outputs are deterministic and do not embed restricted",
            "  content.",
            "",
            "## Out of Scope",
            "- Fetching or downloading restricted source assets.",
            "- Auto-merging GitHub issues or committing draft outputs without",
            "  review.",
            "- Replacing the existing source scanner contract.",
            "- Adding new licensing interpretations beyond explicit manifest and gap",
            "  records.",
            "",
            "## Source Evidence",
            f"- GitHub issue: {issue_line}",
            "- Source scanner: `nwau_py.source_scanner`",
            "- Licensed asset workflow: `nwau_py.licensed_product_workflow`",
            "- Source scanner contract fixtures: `contracts/source-scanner/`",
            "",
            "## Scope Notes",
            f"- Pricing-year coverage is draft-only for {pricing_year}; the package",
            "  records gaps without claiming parity or publication readiness.",
            "- The generated artifacts are intended for review and follow-up, not",
            "  for direct publication.",
        ]
    )


def _render_source_audit_plan() -> str:
    return "\n".join(
        [
            f"# Plan: {DEFAULT_AUDIT_TRACK_TITLE}",
            "",
            "## Phase 1: Draft Package Contract",
            "- [ ] Task: Define the review-only audit package shape and renderers.",
            "    - [ ] Add failing tests for the audit package, track scaffold text,",
            "      and GitHub issue draft.",
            "    - [ ] Verify the outputs do not embed restricted assets or overclaim",
            "      validation.",
            "    - [ ] Keep the scanner manifest as the source of truth for draft",
            "      generation.",
            "- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Draft",
            "  Package Contract' (Protocol in workflow.md)",
            "",
            "## Phase 2: CLI Integration and Docs",
            "- [ ] Task: Add the audit package CLI surface and reusable writers.",
            "    - [ ] Expose the audit package through the installed",
            "      `funding-calculator` entrypoint.",
            "    - [ ] Update source-scanner contract fixtures or docs to mention",
            "      the audit package workflow.",
            "    - [ ] Preserve review-only behavior for licensed or restricted",
            "      source material.",
            "- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: CLI",
            "  Integration and Docs' (Protocol in workflow.md)",
        ]
    )


def _render_source_audit_index(track_id: str, github_issue_url: str | None) -> str:
    issue_link = (
        f"- [GitHub Issue #209]({github_issue_url})"
        if github_issue_url
        else "- GitHub issue link pending"
    )
    return "\n".join(
        [
            f"# Track {track_id} Context",
            "",
            "- [Specification](./spec.md)",
            "- [Implementation Plan](./plan.md)",
            "- [Metadata](./metadata.json)",
            issue_link,
        ]
    )


def _render_source_audit_registry_entry(track_id: str) -> str:
    return "\n".join(
        [
            f"- [~] **Track: {DEFAULT_AUDIT_TRACK_TITLE}**",
            f"*Link: [./tracks/{track_id}/](./tracks/{track_id}/)*",
            "*Gate: turn IHACPA source-scanner output into review-only draft",
            "manifests, Conductor tracks, and GitHub issue updates without copying",
            "restricted assets into version control.*",
        ]
    )


def _render_source_audit_issue_body(
    manifest: SourceDraftManifest,
    *,
    track_id: str,
    github_issue_url: str | None,
) -> str:
    track_path = f"`conductor/tracks/{track_id}/`"
    issue_link = github_issue_url or "(issue URL pending)"
    pricing_year = manifest.pricing_year or "unspecified"
    return "\n".join(
        [
            "## Summary",
            "Automate IHACPA source/license audits that draft manifest, Conductor",
            "track, and GitHub issue updates without committing restricted assets.",
            "",
            "## Conductor track",
            track_path,
            "",
            f"GitHub issue: {issue_link}",
            "",
            "## Acceptance criteria",
            "Audit fixtures cover public source, restricted source, removed source,",
            "changed metadata, and validation drift; dry-run drafts are",
            "deterministic; automation never uploads restricted content.",
            "",
            "## Licensing and support boundary",
            "No automatic merging or automatic licensing decisions.",
            "Restricted assets must never be copied into the repository.",
            "They remain references or gap records only.",
            "",
            "## Validation expectations",
            "Run the focused tests for this track plus the applicable repository",
            "gates: `python conductor/scripts/stub_detector.py --root . --json`,",
            "`uv run ruff check .`, `uv run ty check`, and focused `uv run pytest`.",
            "",
            "## Draft scope",
            f"- Pricing year: {pricing_year}",
            f"- Scanner discoveries: {len(manifest.discoveries)}",
            f"- Gap records: {len(manifest.gaps)}",
            "- Review posture: review-only draft outputs",
        ]
    )


def build_source_audit_package(
    manifest: SourceDraftManifest,
    *,
    track_id: str,
    github_issue_number: int | None = None,
    github_issue_url: str | None = None,
    track_title: str = DEFAULT_AUDIT_TRACK_TITLE,
    issue_labels: tuple[str, ...] = DEFAULT_AUDIT_ISSUE_LABELS,
) -> SourceAuditPackage:
    """Build a review-only package for source-scanner driven audit outputs."""
    if not track_id:
        raise SourceScannerError("track_id must not be blank")
    manifest_dict = manifest.to_dict()
    draft_manifest_json = json.dumps(manifest_dict, indent=2, sort_keys=True)
    track_metadata = _render_source_audit_track_metadata(
        manifest,
        track_id=track_id,
        github_issue_number=github_issue_number,
        github_issue_url=github_issue_url,
    )
    track_spec = _render_source_audit_spec(
        manifest,
        github_issue_url=github_issue_url,
    )
    track_plan = _render_source_audit_plan()
    track_index = _render_source_audit_index(track_id, github_issue_url)
    tracks_registry_entry = _render_source_audit_registry_entry(track_id)
    github_issue_body = _render_source_audit_issue_body(
        manifest,
        track_id=track_id,
        github_issue_url=github_issue_url,
    )
    summary = (
        f"{len(manifest.discoveries)} discoveries, {len(manifest.gaps)} gaps, "
        f"pricing year {manifest.pricing_year or 'unspecified'}"
    )
    return SourceAuditPackage(
        scan_manifest=manifest,
        track_id=track_id,
        track_title=track_title,
        github_issue_number=github_issue_number,
        github_issue_url=github_issue_url,
        draft_manifest_json=draft_manifest_json,
        track_metadata=track_metadata,
        track_spec=track_spec,
        track_plan=track_plan,
        track_index=track_index,
        tracks_registry_entry=tracks_registry_entry,
        github_issue_title=DEFAULT_AUDIT_ISSUE_TITLE,
        github_issue_body=github_issue_body,
        github_issue_labels=issue_labels,
        summary=summary,
    )


def source_audit_package_to_json(package: SourceAuditPackage) -> str:
    """Serialize a source audit package for CLI and review usage."""
    return json.dumps(package.to_dict(), indent=2, sort_keys=True)


def write_source_audit_package(
    package: SourceAuditPackage,
    *,
    root: Path,
) -> dict[str, Path]:
    """Write the draft package to review-only files under ``root``."""
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / "draft-manifest.json"
    issue_path = root / "github-issue.md"
    track_root = root / "conductor" / "tracks" / package.track_id
    track_root.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": manifest_path,
        "issue": issue_path,
        "metadata": track_root / "metadata.json",
        "spec": track_root / "spec.md",
        "plan": track_root / "plan.md",
        "index": track_root / "index.md",
    }
    paths["manifest"].write_text(package.draft_manifest_json, encoding="utf-8")
    paths["issue"].write_text(package.github_issue_body, encoding="utf-8")
    paths["metadata"].write_text(
        json.dumps(package.track_metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths["spec"].write_text(package.track_spec, encoding="utf-8")
    paths["plan"].write_text(package.track_plan, encoding="utf-8")
    paths["index"].write_text(package.track_index, encoding="utf-8")
    return paths


def manifest_to_json(manifest: SourceDraftManifest) -> str:
    """Serialize a draft manifest to pretty JSON."""
    return json.dumps(manifest.to_dict(), indent=2, sort_keys=True)


__all__ = [
    "SUPPORTED_GAP_KINDS",
    "SUPPORTED_SOURCE_SCAN_SCHEMA_VERSION",
    "SUPPORTED_SOURCE_SCAN_STATUSES",
    "SourceAuditPackage",
    "SourceDiscovery",
    "SourceDocument",
    "SourceDraftManifest",
    "SourceGapRecord",
    "SourceScanError",
    "SourceScanResult",
    "SourceScannerError",
    "build_source_audit_package",
    "manifest_to_json",
    "render_dry_run",
    "scan_sources",
    "scan_sources_dry_run",
    "source_audit_package_to_json",
    "write_source_audit_package",
]
