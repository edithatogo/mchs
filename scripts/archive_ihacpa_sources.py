"""Archive IHACPA NWAU calculator source artifacts.

The script reads the public IHACPA NWAU calculators page, downloads listed
calculator artifacts, and writes provenance metadata to a tracked location.
Raw binaries are intentionally written under ``archive/ihacpa/raw/``, which is
ignored by Git until the project chooses Git LFS, release assets, or external
object storage. The durable manifest is written outside that raw storage.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess  # nosec B404
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Protocol
from urllib.error import HTTPError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from nwau_py.provenance import (
    AcquisitionStatus,
    ArtifactKind,
    RunContext,
    SourceArchiveManifest,
    SourceArtifact,
    SourceHost,
    SourcePageSnapshot,
    normalize_acquisition_status,
    normalize_artifact_kind,
    normalize_service_stream,
    sha256_file,
    stable_artifact_id,
    tracked_manifest_paths,
    write_manifest_csv,
    write_manifest_json,
    write_source_page_snapshot,
)

PAGE_URL = "https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators"
USER_AGENT = (
    "Mozilla/5.0 microcosting-healthservices-source-archiver/0.1 "
    "(+https://github.com/edithatogo/microcosting_healthservices)"
)
SCRIPT_VERSION = "0.2"
DEFAULT_OUTPUT_DIR = Path("archive/ihacpa/raw")
DEFAULT_PROVENANCE_DIR = Path("data/provenance/ihacpa")


@dataclass
class FetchMetadata:
    requested_url: str
    final_url: str
    status_code: int
    content_type: str
    headers: dict[str, str]
    redirect_chain: list[dict[str, str]]
    fetched_at: str


class ResponseProtocol(Protocol):
    """Minimal urllib response surface used by the archiver."""

    headers: dict[str, str]

    def geturl(self) -> str: ...

    def getcode(self) -> int | None: ...

    def read(self, size: int = -1) -> bytes: ...

    def close(self) -> None: ...


class RedirectTrackingHandler(HTTPRedirectHandler):
    """Capture redirect metadata while preserving urllib redirect behavior."""

    def __init__(self, redirect_chain: list[dict[str, str]]) -> None:
        super().__init__()
        self.redirect_chain = redirect_chain

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        self.redirect_chain.append(
            {
                "from_url": req.full_url,
                "to_url": newurl,
                "status_code": str(code),
                "location": headers.get("Location", ""),
                "content_type": headers.get("Content-Type", ""),
            }
        )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def git_commit(root: Path) -> str:
    try:
        result = subprocess.run(  # nosec B404 B603 B607 - intentional git metadata read
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:  # pragma: no cover - git availability varies by environment
        return ""
    return result.stdout.strip()


class NwauCalculatorPageParser(HTMLParser):
    """Extract calculator artifact links grouped by year heading."""

    def __init__(self, page_url: str) -> None:
        super().__init__()
        self.page_url = page_url
        self.items: list[SourceArtifact] = []
        self.current_year_label = ""
        self.current_year_start = 0
        self._in_h2 = False
        self._h2_text = ""
        self._anchor: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "h2":
            self._in_h2 = True
            self._h2_text = ""
        if tag == "a" and attr_map.get("href"):
            self._anchor = [urljoin(self.page_url, attr_map["href"] or ""), ""]

    def handle_data(self, data: str) -> None:
        if self._in_h2:
            self._h2_text += data
        if self._anchor is not None:
            self._anchor[1] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            text = " ".join(self._h2_text.split())
            match = re.search(r"(20\d{2})-(\d{2})", text)
            if match:
                self.current_year_start = int(match.group(1))
                self.current_year_label = f"{match.group(1)}-{match.group(2)}"
            self._in_h2 = False

        if tag == "a" and self._anchor is not None:
            href, text = self._anchor
            self._anchor = None
            self._append_artifact(href, " ".join(text.split()))

    def _append_artifact(self, href: str, label: str) -> None:
        lower = href.lower()
        downloadable = lower.endswith((".xls", ".xlsm", ".xlsb", ".zip", ".7z"))
        box_share = "box.com/s/" in lower
        if not self.current_year_label or not (downloadable or box_share):
            return

        artifact_kind = normalize_artifact_kind(label, href)
        if artifact_kind is ArtifactKind.UNKNOWN:
            artifact_kind = (
                ArtifactKind.SAS
                if "sas" in label.lower() or lower.endswith((".zip", ".7z"))
                else ArtifactKind.EXCEL
            )
        artifact_type = artifact_kind.value
        self.items.append(
            SourceArtifact(
                artifact_id=stable_artifact_id(
                    self.current_year_label,
                    label,
                    href,
                    artifact_kind=artifact_kind,
                ),
                year_label=self.current_year_label,
                year_start=self.current_year_start,
                artifact_type=artifact_type,
                artifact_kind=artifact_kind,
                service_stream=(normalize_service_stream(artifact_kind, label)),
                label=label,
                source_page_url=self.page_url,
                artifact_url=href,
                source_host=SourceHost.BOX if box_share else SourceHost.IHACPA,
            )
        )


def fetch(url: str, timeout: int) -> tuple[ResponseProtocol, FetchMetadata]:
    """Open ``url`` with retry support and return response metadata."""

    last_error: Exception | None = None
    for attempt in range(1, 4):
        attempt_result = _fetch_once(url, timeout)
        if isinstance(attempt_result, tuple):
            return attempt_result
        last_error = attempt_result
        if not isinstance(attempt_result, HTTPError):
            time.sleep(attempt)
            continue
        if attempt_result.code < 500:
            raise attempt_result
        time.sleep(attempt)
    if last_error is None:  # pragma: no cover
        raise RuntimeError("request failed without an exception")
    raise last_error


def _fetch_once(
    url: str, timeout: int
) -> tuple[ResponseProtocol, FetchMetadata] | Exception:
    try:
        redirects: list[dict[str, str]] = []
        request = Request(url, headers={"User-Agent": USER_AGENT})
        opener = build_opener(RedirectTrackingHandler(redirects))
        response = opener.open(request, timeout=timeout)
        headers = {key: value for key, value in response.headers.items()}
        metadata = FetchMetadata(
            requested_url=url,
            final_url=response.geturl(),
            status_code=int(response.getcode() or 0),
            content_type=response.headers.get("content-type", ""),
            headers=headers,
            redirect_chain=redirects,
            fetched_at=now_iso(),
        )
        return response, metadata
    except HTTPError as exc:
        return exc
    except Exception as exc:  # pragma: no cover - network variability
        return exc


def safe_filename(item: SourceArtifact, final_url: str, content_type: str) -> str:
    name = Path(unquote(urlparse(final_url).path)).name
    if not name or "." not in name:
        suffix = ".html" if "html" in content_type else ".download"
        stem = re.sub(r"[^a-z0-9]+", "_", item.label.lower()).strip("_")
        name = f"{stem or item.artifact_type}{suffix}"
    return re.sub(r"[^A-Za-z0-9._%()+ -]+", "_", name)


def snapshot_source_page(
    page_url: str,
    provenance_dir: Path,
    timeout: int,
) -> tuple[str, SourcePageSnapshot, dict[str, object]]:
    response, metadata = fetch(page_url, timeout)
    try:
        body = response.read()
    finally:
        response.close()

    snapshot_path = provenance_dir / "snapshots" / "source-page.html"
    snapshot = write_source_page_snapshot(
        body.decode("utf-8", errors="replace"), snapshot_path
    )

    snapshot_metadata: dict[str, object] = {
        "requested_url": metadata.requested_url,
        "final_url": metadata.final_url,
        "status_code": metadata.status_code,
        "content_type": metadata.content_type,
        "headers": metadata.headers,
        "redirect_chain": metadata.redirect_chain,
        "fetched_at": metadata.fetched_at,
        "path": snapshot.path,
        "bytes": snapshot.byte_count,
        "sha256": snapshot.sha256,
    }
    return body.decode("utf-8", errors="replace"), snapshot, snapshot_metadata


def download_artifact(item: SourceArtifact, root: Path, timeout: int) -> None:
    target_dir = root / str(item.year_start) / item.artifact_type
    target_dir.mkdir(parents=True, exist_ok=True)

    response, metadata = fetch(item.artifact_url, timeout)
    try:
        path = target_dir / safe_filename(
            item, metadata.final_url, metadata.content_type
        )

        item.final_url = metadata.final_url
        item.content_type = metadata.content_type
        item.path = str(path)
        item.local_path = str(path)
        item.redirect_chain = metadata.redirect_chain

        if path.exists() and path.stat().st_size > 0:
            item.status = normalize_acquisition_status(
                item.artifact_url,
                final_url=metadata.final_url,
                content_type=metadata.content_type,
                downloaded=True,
            ).value
            item.lifecycle.acquisition_status = AcquisitionStatus(item.status)
            item.bytes = path.stat().st_size
            item.checksum_algorithm = "sha256"
            item.checksum = sha256_file(path)
            item.checksum_checked_at = now_iso()
            return

        tmp_path = path.with_suffix(path.suffix + ".part")
        with tmp_path.open("wb") as file:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                file.write(chunk)
        tmp_path.replace(path)

        item.status = normalize_acquisition_status(
            item.artifact_url,
            final_url=metadata.final_url,
            content_type=metadata.content_type,
            downloaded=True,
        ).value
        item.lifecycle.acquisition_status = AcquisitionStatus(item.status)
        item.bytes = path.stat().st_size
        item.checksum_algorithm = "sha256"
        item.checksum = sha256_file(path)
        item.downloaded_at = now_iso()
        item.checksum_checked_at = now_iso()

        if item.status == AcquisitionStatus.EXTERNAL_HTML_ONLY.value:
            item.lifecycle.acquisition_status = AcquisitionStatus.EXTERNAL_HTML_ONLY
            item.bytes = 0
            item.downloaded_at = ""
    finally:
        response.close()


def parse_artifacts(
    page_url: str,
    provenance_dir: Path,
    timeout: int,
) -> tuple[list[SourceArtifact], SourcePageSnapshot, dict[str, object]]:
    html, snapshot, snapshot_metadata = snapshot_source_page(
        page_url, provenance_dir, timeout
    )
    parser = NwauCalculatorPageParser(page_url)
    parser.feed(html)
    return parser.items, snapshot, snapshot_metadata


def write_manifests(
    items: list[SourceArtifact],
    provenance_dir: Path,
    *,
    page_url: str,
    source_snapshot: SourcePageSnapshot,
    invocation_args: tuple[str, ...],
    run_started_at: str,
) -> None:
    provenance_dir.mkdir(parents=True, exist_ok=True)
    manifest_paths = tracked_manifest_paths(provenance_dir)
    run_context = RunContext(
        script_name=Path(__file__).name,
        script_version=SCRIPT_VERSION,
        git_commit=git_commit(repo_root()),
        invocation_args=invocation_args,
        source_page_url=page_url,
        source_page_snapshot=source_snapshot,
        started_at=run_started_at,
        completed_at=now_iso(),
    )
    manifest = SourceArchiveManifest(
        schema_version="1",
        generated_at=now_iso(),
        run_context=run_context,
        artifacts=tuple(items),
    )

    write_manifest_json(manifest, manifest_paths.json_path)
    write_manifest_csv(manifest, manifest_paths.csv_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-url", default=PAGE_URL)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--provenance-dir", default=str(DEFAULT_PROVENANCE_DIR))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    provenance_dir = Path(args.provenance_dir)
    run_started_at = now_iso()
    items, source_snapshot, _snapshot_metadata = parse_artifacts(
        args.page_url,
        provenance_dir,
        args.timeout,
    )

    if not args.list_only:
        for item in items:
            error = _download_item(item, output_dir, args.timeout)
            if error is not None:
                item.status = "failed"
                item.error = f"{type(error).__name__}: {error}"

    write_manifests(
        items,
        provenance_dir,
        page_url=args.page_url,
        source_snapshot=source_snapshot,
        invocation_args=tuple(sys.argv[1:]),
        run_started_at=run_started_at,
    )

    counts: dict[str, int] = {}
    for item in items:
        counts[item.status] = counts.get(item.status, 0) + 1
    print(json.dumps({"items": len(items), "statuses": counts}, sort_keys=True))


def _download_item(item: SourceArtifact, root: Path, timeout: int) -> Exception | None:
    try:
        download_artifact(item, root, timeout)
    except Exception as exc:  # pragma: no cover - network variability
        return exc
    return None


if __name__ == "__main__":
    main()
