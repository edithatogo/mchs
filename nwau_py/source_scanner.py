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
            self._current_heading = _normalize_whitespace("".join(self._heading_chunks))
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


def manifest_to_json(manifest: SourceDraftManifest) -> str:
    """Serialize a draft manifest to pretty JSON."""
    return json.dumps(manifest.to_dict(), indent=2, sort_keys=True)


__all__ = [
    "SUPPORTED_GAP_KINDS",
    "SUPPORTED_SOURCE_SCAN_SCHEMA_VERSION",
    "SUPPORTED_SOURCE_SCAN_STATUSES",
    "SourceDiscovery",
    "SourceDocument",
    "SourceDraftManifest",
    "SourceGapRecord",
    "SourceScanError",
    "SourceScanResult",
    "SourceScannerError",
    "manifest_to_json",
    "render_dry_run",
    "scan_sources",
    "scan_sources_dry_run",
]
