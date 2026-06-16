from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
VSCODE_MARKETPLACE_QUERY_URL = (
    "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    "?api-version=7.2-preview.1"
)
VSCODE_MARKETPLACE_EXTENSION_ID = "edithatogo.mchs-tools"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def generated_at_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def report_metadata(live: bool, generated_at: str | None = None) -> dict[str, Any]:
    metadata: dict[str, Any] = {"live": live}
    if generated_at:
        metadata["generated_at_utc"] = generated_at
    return metadata


def external_gate_rows(contract: dict) -> list[dict]:
    rows: list[dict] = []
    for registry in contract["registries"]:
        if registry["current_status"] == "published_verified":
            continue
        blocker = registry.get("blocker")
        if not blocker:
            raise AssertionError(f"{registry['id']} is unpublished but has no blocker")
        submission_url = registry.get("submission_url")
        if submission_url and not (
            registry["current_status"].startswith("submitted_")
            or (
                registry["current_status"].startswith("published_")
                and "_pending_" in registry["current_status"]
            )
        ):
            raise AssertionError(
                f"{registry['id']} is unpublished with a submission URL but is not "
                "review-pending or partial-published"
            )
        if registry.get("localReadinessResolved") is not True:
            raise AssertionError(f"{registry['id']} has unresolved local readiness")
        rows.append(
            {
                "id": registry["id"],
                "registry": registry["registry"],
                "package": registry["package"],
                "status": registry["current_status"],
                "blocker": blocker,
                "track": registry["track"],
                "submission_url": submission_url,
                "version": registry["version"],
            }
        )
    return rows


def github_pull_api_url(url: str) -> str | None:
    prefix = "https://github.com/"
    if not url.startswith(prefix):
        return None
    parts = url[len(prefix) :].strip("/").split("/")
    if len(parts) != 4 or parts[2] != "pull":
        return None
    owner, repo, number = parts[0], parts[1], parts[3]
    if not number.isdigit():
        return None
    return f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"


def github_issue_api_url(url: str) -> str | None:
    prefix = "https://github.com/"
    if not url.startswith(prefix):
        return None
    parts = url[len(prefix) :].strip("/").split("/")
    if len(parts) != 4 or parts[2] != "issues":
        return None
    owner, repo, number = parts[0], parts[1], parts[3]
    if not number.isdigit():
        return None
    return f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"


def github_repo_api_url(url: str) -> str | None:
    prefix = "https://github.com/"
    if not url.startswith(prefix):
        return None
    parts = url[len(prefix) :].strip("/").split("/")
    if len(parts) != 2:
        return None
    owner, repo = parts
    if not owner or not repo:
        return None
    return f"https://api.github.com/repos/{owner}/{repo}"


def request_headers_for_url(url: str) -> dict[str, str]:
    headers = {"Accept": "application/json", "User-Agent": "mchs-registry-gate-report"}
    if url.startswith("https://api.github.com/"):
        headers["Accept"] = "application/vnd.github+json"
        github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if github_token:
            headers["Authorization"] = "Bearer " + github_token
    return headers


def fetch_json(url: str, timeout: int = 20) -> dict:
    request = Request(
        url,
        headers=request_headers_for_url(url),
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_json_post(url: str, payload: dict[str, Any], timeout: int = 20) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers=request_headers_for_url(url) | {"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 20) -> str:
    request = Request(url, headers={"User-Agent": "mchs-registry-gate-report"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def fetch_status(url: str, timeout: int = 20) -> int:
    request = Request(url, headers={"User-Agent": "mchs-registry-gate-report"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return int(response.status)
    except HTTPError as exc:
        return int(exc.code)


def github_deferred_state_from_http_error(
    github_api_url: str, exc: HTTPError
) -> dict | None:
    headers = exc.headers or {}
    rate_remaining = headers.get("x-ratelimit-remaining")
    rate_reset = headers.get("x-ratelimit-reset")
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    body_lower = body.lower()
    rate_limited = exc.code == 429 or (
        exc.code == 403
        and (
            rate_remaining == "0"
            or "rate limit" in body_lower
            or "abuse detection" in body_lower
        )
    )
    if rate_limited:
        detail = (
            f"GitHub API rate-limited while querying {github_api_url}: HTTP {exc.code}"
        )
        if rate_reset:
            detail += f", x-ratelimit-reset={rate_reset}"
        return {
            "live_state": "check_deferred_rate_limited",
            "live_detail": detail,
        }
    if exc.code == 403:
        return {
            "live_state": "check_deferred_forbidden",
            "live_detail": (
                f"GitHub API forbidden while querying {github_api_url}: HTTP {exc.code}"
            ),
        }
    if exc.code == 401:
        return {
            "live_state": "check_deferred_auth_required",
            "live_detail": (
                f"GitHub API authentication required while querying {github_api_url}: "
                f"HTTP {exc.code}"
            ),
        }
    return None


def public_probe_url(row: dict) -> str | None:
    registry_id = row["id"]
    package = row["package"]
    if registry_id == "rust_crates_io":
        return f"https://crates.io/api/v1/crates/{package}"
    if registry_id == "dotnet_nuget":
        return f"https://api.nuget.org/v3-flatcontainer/{package.lower()}/index.json"
    if registry_id == "r_cran":
        return f"https://crandb.r-pkg.org/{package}"
    if registry_id == "julia_general":
        return f"https://juliahub.com/api/packages/{package}"
    if registry_id == "go_module_proxy":
        return f"https://pkg.go.dev/{package}"
    if registry_id == "swift_package_index":
        return "https://swiftpackageindex.com/edithatogo/mchs-swift"
    if registry_id == "jvm_maven_central":
        group, artifact = package.split(":", 1)
        group_path = group.replace(".", "/")
        return (
            f"https://repo1.maven.org/maven2/{group_path}/{artifact}/maven-metadata.xml"
        )
    if registry_id == "conda_forge":
        return f"https://api.anaconda.org/package/conda-forge/{package}"
    if registry_id == "homebrew":
        publication_evidence = row.get("publicationEvidence", {})
        if publication_evidence.get("scope") == "personal_tap":
            submission_evidence = row.get("submissionEvidence", {})
            return submission_evidence.get("formulaUrl") or publication_evidence.get(
                "url"
            )
        return f"https://formulae.brew.sh/api/formula/{package}.json"
    if registry_id == "vscode_openvsx":
        return "https://open-vsx.org/api/edithatogo/mchs-tools"
    if registry_id == "matlab_file_exchange":
        publication_evidence = row.get("publicationEvidence", {})
        if publication_evidence.get("url"):
            return publication_evidence["url"]
        return (
            "https://www.mathworks.com/matlabcentral/fileexchange/"
            "?term=%22MCHS%20MATLAB%20Interop%22"
        )
    return None


def normalize_version(version: str) -> str:
    return version.removeprefix("v").lower()


def public_available(detail: str) -> dict:
    return {"public_state": "public_listing_available", "public_detail": detail}


def public_missing(detail: str) -> dict:
    return {"public_state": "public_listing_missing", "public_detail": detail}


def public_unverified(detail: str) -> dict:
    return {
        "public_state": "public_listing_version_unverified",
        "public_detail": detail,
    }


def public_state_from_http_error(url: str, exc: HTTPError) -> dict:
    if exc.code == 404:
        return public_missing(f"{url} HTTP {exc.code}")
    if exc.code in {401, 403}:
        return {
            "public_state": "public_listing_blocked",
            "public_detail": f"{url} HTTP {exc.code}",
        }
    return {
        "public_state": "public_listing_unknown",
        "public_detail": f"{url} HTTP {exc.code}",
    }


def contains_version(value: object, version: str) -> bool:
    expected = normalize_version(version)
    if isinstance(value, str):
        return normalize_version(value) == expected
    if isinstance(value, dict):
        return any(contains_version(item, version) for item in value.values())
    if isinstance(value, list):
        return any(contains_version(item, version) for item in value)
    return False


def text_contains_version(text: str, version: str) -> bool:
    normalized_text = text.lower()
    bare_version = normalize_version(version)
    return version.lower() in normalized_text or f"v{bare_version}" in normalized_text


def text_contains_cloudflare_challenge(text: str) -> bool:
    normalized_text = text.lower()
    return (
        "cf-mitigated" in normalized_text
        or "just a moment" in normalized_text
        or "enable javascript and cookies to continue" in normalized_text
        or "challenges.cloudflare.com" in normalized_text
    )


def cran_packages_index_has_version(text: str, package: str, version: str) -> bool:
    expected_package = package.lower()
    expected_version = normalize_version(version)
    for stanza in text.split("\n\n"):
        fields: dict[str, str] = {}
        for line in stanza.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[key.strip().lower()] = value.strip()
        if fields.get("package", "").lower() != expected_package:
            continue
        if normalize_version(fields.get("version", "")) == expected_version:
            return True
    return False


def live_cran_public_package_state(row: dict) -> dict:
    package = row["package"]
    version = row["version"]
    package_url = f"https://cran.r-project.org/web/packages/{package}/index.html"
    crandb_url = f"https://crandb.r-pkg.org/{package}"
    packages_url = "https://cran.r-project.org/src/contrib/PACKAGES"
    details: list[str] = []
    version_evidence: list[str] = []
    unavailable_count = 0
    failed_count = 0

    try:
        package_page = fetch_text(package_url)
    except HTTPError as exc:
        unavailable_count += 1
        details.append(f"package page {package_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        failed_count += 1
        details.append(f"package page {type(exc).__name__}: {exc}")
    else:
        if package.lower() in package_page.lower() and text_contains_version(
            package_page, version
        ):
            version_evidence.append(
                f"package page {package_url} version {version} found"
            )
        else:
            details.append(
                f"package page {package_url} available but version {version} "
                "was not found"
            )

    try:
        crandb = fetch_json(crandb_url)
    except HTTPError as exc:
        unavailable_count += 1
        details.append(f"CRANDB {crandb_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        failed_count += 1
        details.append(f"CRANDB {type(exc).__name__}: {exc}")
    else:
        if normalize_version(str(crandb.get("Version", ""))) == normalize_version(
            version
        ):
            version_evidence.append(f"CRANDB {crandb_url} version {version} found")
        else:
            details.append(
                f"CRANDB {crandb_url} available but version {version} was not found"
            )

    try:
        packages_index = fetch_text(packages_url)
    except HTTPError as exc:
        unavailable_count += 1
        details.append(f"PACKAGES index {packages_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        failed_count += 1
        details.append(f"PACKAGES index {type(exc).__name__}: {exc}")
    else:
        if cran_packages_index_has_version(packages_index, package, version):
            version_evidence.append(
                f"PACKAGES index {packages_url} contains {package} {version}"
            )
        elif f"Package: {package}" in packages_index:
            details.append(
                f"PACKAGES index {packages_url} contains {package} but version "
                f"{version} was not found"
            )
        else:
            unavailable_count += 1
            details.append(f"PACKAGES index {packages_url} has no Package: {package}")

    if version_evidence:
        return public_available("; ".join(version_evidence + details))
    if failed_count and unavailable_count == 0:
        return {
            "public_state": "check_failed",
            "public_detail": "; ".join(details),
        }
    if any("available but" in detail or "contains" in detail for detail in details):
        return public_unverified("; ".join(details))
    return public_missing("; ".join(details))


def live_conda_public_package_state(row: dict) -> dict:
    package = row["package"]
    version = row["version"]
    anaconda_url = f"https://api.anaconda.org/package/conda-forge/{package}"
    feedstock_url = f"https://api.github.com/repos/conda-forge/{package}-feedstock"
    details: list[str] = []
    package_version_found = False
    feedstock_found = False

    try:
        payload = fetch_json(anaconda_url)
    except HTTPError as exc:
        details.append(f"Anaconda {anaconda_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"Anaconda {type(exc).__name__}: {exc}")
    else:
        files = payload.get("files", [])
        if any(
            item.get("version") == version for item in files if isinstance(item, dict)
        ):
            package_version_found = True
            details.append(f"Anaconda {anaconda_url} version {version} found")
        else:
            details.append(
                f"Anaconda {anaconda_url} available but version {version} was not found"
            )

    try:
        repo = fetch_json(feedstock_url)
    except HTTPError as exc:
        deferred = github_deferred_state_from_http_error(feedstock_url, exc)
        if deferred:
            details.append(deferred["live_detail"])
        else:
            details.append(f"feedstock {feedstock_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"feedstock {type(exc).__name__}: {exc}")
    else:
        feedstock_found = True
        details.append(
            f"feedstock {repo.get('html_url', feedstock_url)} "
            f"default_branch={repo.get('default_branch')} "
            f"archived={repo.get('archived')}"
        )

    if package_version_found:
        return public_available("; ".join(details))
    if feedstock_found:
        return public_unverified(
            "; ".join(details)
            + "; feedstock exists but Anaconda package version evidence is missing"
        )
    if any("available but" in detail for detail in details):
        return public_unverified("; ".join(details))
    if any("rate-limited" in detail or "forbidden" in detail for detail in details):
        return {
            "public_state": "check_deferred",
            "public_detail": "; ".join(details),
        }
    return public_missing("; ".join(details))


def live_c_cpp_public_package_state(row: dict) -> dict:
    package = row["package"]
    version = row["version"]
    conanfile_url = (
        "https://raw.githubusercontent.com/conan-io/conan-center-index/master/"
        f"recipes/{package}/all/conanfile.py"
    )
    conandata_url = (
        "https://raw.githubusercontent.com/conan-io/conan-center-index/master/"
        f"recipes/{package}/all/conandata.yml"
    )
    vcpkg_url = (
        "https://raw.githubusercontent.com/microsoft/vcpkg/master/"
        f"ports/{package}/vcpkg.json"
    )
    details: list[str] = []
    conan_version_found = False
    conan_identity_found = False
    vcpkg_version_found = False

    try:
        conanfile = fetch_text(conanfile_url)
    except HTTPError as exc:
        details.append(f"ConanCenter conanfile {conanfile_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"ConanCenter conanfile {type(exc).__name__}: {exc}")
    else:
        if package in conanfile or "nwau_c_abi" in conanfile:
            conan_identity_found = True
            details.append(f"ConanCenter conanfile {conanfile_url} found")
        else:
            details.append(
                f"ConanCenter conanfile {conanfile_url} lacks {package} identity"
            )

    try:
        conandata = fetch_text(conandata_url)
    except HTTPError as exc:
        details.append(f"ConanCenter conandata {conandata_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"ConanCenter conandata {type(exc).__name__}: {exc}")
    else:
        if text_contains_version(conandata, version):
            conan_version_found = True
            details.append(
                f"ConanCenter conandata {conandata_url} version {version} found"
            )
        else:
            details.append(
                f"ConanCenter conandata {conandata_url} available but version "
                f"{version} was not found"
            )

    try:
        vcpkg = json.loads(fetch_text(vcpkg_url))
    except HTTPError as exc:
        details.append(f"vcpkg {vcpkg_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"vcpkg {type(exc).__name__}: {exc}")
    except json.JSONDecodeError as exc:
        details.append(f"vcpkg {vcpkg_url} JSONDecodeError: {exc}")
    else:
        if normalize_version(str(vcpkg.get("version-string", ""))) == normalize_version(
            version
        ):
            vcpkg_version_found = True
            details.append(f"vcpkg {vcpkg_url} version {version} found")
        else:
            details.append(
                f"vcpkg {vcpkg_url} available but version {version} was not found"
            )

    if conan_identity_found and conan_version_found:
        return public_available("; ".join(details))
    if vcpkg_version_found:
        return public_unverified(
            "; ".join(details)
            + "; vcpkg listing exists but ConanCenter publication still needs evidence"
        )
    if conan_identity_found or any("available but" in detail for detail in details):
        return public_unverified("; ".join(details))
    return public_missing("; ".join(details))


def live_stata_ssc_public_package_state(row: dict) -> dict:
    version = row["version"]
    package_name = "mchs"
    base_url = "http://fmwww.bc.edu/repec/bocode/m"
    pkg_url = f"{base_url}/{package_name}.pkg"
    ado_url = f"{base_url}/{package_name}.ado"
    help_url = f"{base_url}/{package_name}.sthlp"
    details: list[str] = []
    pkg_identity_found = False
    ado_found = False
    help_found = False

    try:
        package_manifest = fetch_text(pkg_url)
    except HTTPError as exc:
        details.append(f"SSC package manifest {pkg_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"SSC package manifest {type(exc).__name__}: {exc}")
    else:
        normalized_manifest = package_manifest.lower()
        has_name = "'mchs':" in normalized_manifest or f"n {package_name}" in (
            normalized_manifest
        )
        has_files = "f mchs.ado" in normalized_manifest and "f mchs.sthlp" in (
            normalized_manifest
        )
        has_author = "dylan.mordaunt" in normalized_manifest
        if has_name and has_files and has_author:
            pkg_identity_found = True
            details.append(
                f"SSC package manifest {pkg_url} found "
                f"(semantic version {version} is local archive evidence)"
            )
        else:
            details.append(
                f"SSC package manifest {pkg_url} available but package identity "
                "was not verified"
            )

    try:
        ado = fetch_text(ado_url)
    except HTTPError as exc:
        details.append(f"SSC ado {ado_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"SSC ado {type(exc).__name__}: {exc}")
    else:
        if "program define mchs" in ado.lower():
            ado_found = True
            details.append(f"SSC ado {ado_url} found")
        else:
            details.append(f"SSC ado {ado_url} available but command was not verified")

    try:
        help_file = fetch_text(help_url)
    except HTTPError as exc:
        details.append(f"SSC help {help_url} HTTP {exc.code}")
    except (TimeoutError, URLError) as exc:
        details.append(f"SSC help {type(exc).__name__}: {exc}")
    else:
        normalized_help = help_file.lower()
        if "mchs stata" in normalized_help or "{cmd:mchs" in normalized_help:
            help_found = True
            details.append(f"SSC help {help_url} found")
        else:
            details.append(
                f"SSC help {help_url} available but identity was not verified"
            )

    if pkg_identity_found and ado_found and help_found:
        return public_available("; ".join(details))
    if any("available but" in detail for detail in details):
        return public_unverified("; ".join(details))
    return public_missing("; ".join(details))


def live_json_public_package_state(row: dict, url: str) -> dict | None:
    registry_id = row["id"]
    version = row["version"]

    if registry_id == "rust_crates_io":
        payload = fetch_json(url)
        versions = payload.get("versions", [])
        if any(
            item.get("num") == version for item in versions if isinstance(item, dict)
        ):
            return public_available(f"{url} version {version} found")
        return public_unverified(f"{url} available but version {version} was not found")

    if registry_id == "dotnet_nuget":
        payload = fetch_json(url)
        versions = payload.get("versions", [])
        if any(
            normalize_version(item) == normalize_version(version)
            for item in versions
            if isinstance(item, str)
        ):
            return public_available(f"{url} version {version} found")
        return public_unverified(f"{url} available but version {version} was not found")

    if registry_id == "julia_general":
        payload = fetch_json(url)
        if contains_version(payload, version):
            return public_available(f"{url} version {version} found")
        return public_unverified(f"{url} available but version {version} was not found")

    if registry_id == "homebrew":
        publication_evidence = row.get("publicationEvidence", {})
        if publication_evidence.get("scope") == "personal_tap":
            return None
        payload = fetch_json(url)
        stable = payload.get("versions", {}).get("stable")
        if normalize_version(str(stable or "")) == normalize_version(version):
            return public_available(f"{url} version {version} found")
        return public_unverified(
            f"{url} available but stable version {version} was not found"
        )

    if registry_id == "vscode_openvsx":
        return live_vscode_public_package_state(url, version)

    return None


def live_vscode_public_package_state(openvsx_url: str, version: str) -> dict:
    expected = normalize_version(version)
    openvsx_detail: str
    openvsx_has_version = False
    openvsx_latest: str | None = None
    try:
        payload = fetch_json(openvsx_url)
    except HTTPError as exc:
        if exc.code != 404:
            raise
        openvsx_detail = f"Open VSX {openvsx_url} HTTP {exc.code}"
    else:
        openvsx_latest = str(payload.get("version", "") or "")
        all_versions = payload.get("allVersions", {})
        openvsx_versions = {openvsx_latest}
        if isinstance(all_versions, dict | list):
            openvsx_versions.update(str(item) for item in all_versions)
        openvsx_has_version = any(
            normalize_version(item) == expected for item in openvsx_versions
        )
        if openvsx_has_version:
            openvsx_detail = f"Open VSX {openvsx_url} version {version} found"
            if normalize_version(openvsx_latest) != expected:
                openvsx_detail += f" (latest is {openvsx_latest})"
        else:
            openvsx_detail = (
                f"Open VSX {openvsx_url} available but version {version} was not found"
            )

    marketplace_payload = {
        "filters": [
            {
                "criteria": [
                    {
                        "filterType": 7,
                        "value": VSCODE_MARKETPLACE_EXTENSION_ID,
                    }
                ]
            }
        ],
        "flags": 914,
    }
    marketplace = fetch_json_post(VSCODE_MARKETPLACE_QUERY_URL, marketplace_payload)
    extensions = [
        extension
        for result in marketplace.get("results", [])
        if isinstance(result, dict)
        for extension in result.get("extensions", [])
        if isinstance(extension, dict)
    ]
    for extension in extensions:
        publisher = extension.get("publisher", {})
        extension_id = (
            f"{publisher.get('publisherName')}.{extension.get('extensionName')}"
        )
        if extension_id != VSCODE_MARKETPLACE_EXTENSION_ID:
            continue
        versions = extension.get("versions", [])
        marketplace_has_version = any(
            normalize_version(str(item.get("version", ""))) == expected
            for item in versions
            if isinstance(item, dict)
        )
        marketplace_detail = f"Visual Studio Marketplace {extension_id}"
        if marketplace_has_version and openvsx_has_version:
            return public_available(
                f"{openvsx_detail}; {marketplace_detail} version {version} found"
            )
        if marketplace_has_version:
            return public_unverified(
                f"{openvsx_detail}; {marketplace_detail} version {version} found"
            )
        return public_unverified(
            f"{openvsx_detail}; {marketplace_detail} available but version "
            f"{version} was not found"
        )

    return public_missing(
        f"{openvsx_detail}; Visual Studio Marketplace "
        f"{VSCODE_MARKETPLACE_EXTENSION_ID} query returned 0 extensions"
    )


def live_text_public_package_state(row: dict, url: str) -> dict | None:
    registry_id = row["id"]
    version = row["version"]

    if registry_id == "jvm_maven_central":
        text = fetch_text(url)
        root = ElementTree.fromstring(text)
        versions = [element.text or "" for element in root.findall(".//version")]
        if any(
            normalize_version(item) == normalize_version(version) for item in versions
        ):
            return public_available(f"{url} version {version} found")
        return public_unverified(f"{url} available but version {version} was not found")

    if registry_id == "go_module_proxy":
        text = fetch_text(url)
        if text_contains_version(text, version):
            return public_available(f"{url} version {version} found")
        return public_unverified(f"{url} available but version {version} was not found")

    if registry_id == "swift_package_index":
        text = fetch_text(url)
        if text_contains_cloudflare_challenge(text):
            return {
                "public_state": "public_listing_blocked",
                "public_detail": f"{url} Cloudflare challenge",
            }
        normalized_text = text.lower()
        has_identity = (
            "mchsbind" in normalized_text
            or "mchs-swift" in normalized_text
            or "github.com/edithatogo/mchs-swift" in normalized_text
        )
        if has_identity and text_contains_version(text, version):
            return public_available(f"{url} version {version} found")
        if has_identity:
            return public_unverified(
                f"{url} available but version {version} was not found"
            )
        return public_unverified(
            f"{url} available but package identity evidence was not found"
        )

    if registry_id == "matlab_file_exchange":
        text = fetch_text(url)
        if "did not match any of the add-ons" in text:
            return public_missing(f"{url} exact-title search returned no add-ons")
        if "MCHS MATLAB Interop" in text or "mchs-matlab-interop" in text:
            if text_contains_version(text, version):
                return public_available(
                    f"{url} exact-title result version {version} found"
                )
            return public_unverified(
                f"{url} exact-title result found but version {version} was not found"
            )
        return public_unverified(
            f"{url} available but exact-title listing evidence was not found"
        )

    if registry_id == "homebrew":
        publication_evidence = row.get("publicationEvidence", {})
        if publication_evidence.get("scope") != "personal_tap":
            return None
        text = fetch_text(url)
        sha256 = str(publication_evidence.get("formulaSha256") or "")
        has_version = text_contains_version(text, version)
        has_sha256 = not sha256 or sha256 in text
        if has_version and has_sha256:
            return public_available(
                f"{url} personal tap formula version {version} found"
            )
        missing = []
        if not has_version:
            missing.append(f"version {version}")
        if not has_sha256:
            missing.append(f"sha256 {sha256}")
        return public_unverified(
            f"{url} available but {' and '.join(missing)} was not found"
        )

    return None


def live_public_package_state(row: dict) -> dict:
    if row["id"] == "r_cran":
        return live_cran_public_package_state(row)
    if row["id"] == "conda_forge":
        return live_conda_public_package_state(row)
    if row["id"] == "c_cpp_vcpkg_conan":
        return live_c_cpp_public_package_state(row)
    if row["id"] == "stata_ssc":
        return live_stata_ssc_public_package_state(row)

    url = public_probe_url(row)
    if not url:
        return {
            "public_state": "manual_check_required",
            "public_detail": "No deterministic public package probe configured.",
        }
    try:
        json_state = live_json_public_package_state(row, url)
        if json_state is not None:
            return json_state
        text_state = live_text_public_package_state(row, url)
        if text_state is not None:
            return text_state
    except HTTPError as exc:
        return public_state_from_http_error(url, exc)
    except (TimeoutError, URLError) as exc:
        return {
            "public_state": "check_failed",
            "public_detail": f"{type(exc).__name__}: {exc}",
        }
    except (ElementTree.ParseError, json.JSONDecodeError) as exc:
        return public_unverified(
            f"{url} available but response could not be parsed: {type(exc).__name__}"
        )

    try:
        status = fetch_status(url)
    except (TimeoutError, URLError) as exc:
        return {
            "public_state": "check_failed",
            "public_detail": f"{type(exc).__name__}: {exc}",
        }

    if 200 <= status < 300:
        return public_unverified(f"{url} HTTP {status} without target-version evidence")
    if status == 404:
        state = "public_listing_missing"
    elif status in {401, 403}:
        state = "public_listing_blocked"
    else:
        state = "public_listing_unknown"
    return {"public_state": state, "public_detail": f"{url} HTTP {status}"}


def live_submission_state(submission_url: str | None) -> dict:
    if not submission_url:
        return {
            "live_state": "blocked_no_submission",
            "live_detail": "No submission URL recorded.",
        }

    if submission_url.startswith("https://proxy.golang.org/"):
        try:
            status = fetch_status(submission_url)
        except (TimeoutError, URLError) as exc:
            return {
                "live_state": "check_failed",
                "live_detail": f"{type(exc).__name__}: {exc}",
            }
        if 200 <= status < 300:
            return {
                "live_state": "go_proxy_available",
                "live_detail": f"{submission_url} HTTP {status}",
            }
        return {
            "live_state": "go_proxy_unavailable",
            "live_detail": f"{submission_url} HTTP {status}",
        }

    github_api_url = github_pull_api_url(submission_url)
    if github_api_url:
        try:
            pull = fetch_json(github_api_url)
        except HTTPError as exc:
            deferred = github_deferred_state_from_http_error(github_api_url, exc)
            if deferred:
                return deferred
            return {
                "live_state": "check_failed",
                "live_detail": f"HTTP {exc.code} while querying {github_api_url}",
            }
        except (TimeoutError, URLError) as exc:
            return {
                "live_state": "check_failed",
                "live_detail": f"{type(exc).__name__}: {exc}",
            }

        if pull.get("merged") is True:
            state = "submitted_merged"
        elif pull.get("state") == "open":
            state = "submitted_open"
        else:
            state = "submitted_closed_unmerged"
        detail_parts = [
            f"{pull.get('html_url', submission_url)}",
            f"state={pull.get('state')}",
            f"merged={pull.get('merged')}",
            f"draft={pull.get('draft')}",
        ]
        if "mergeable" in pull:
            detail_parts.append(f"mergeable={pull.get('mergeable')}")
        if pull.get("mergeable_state") is not None:
            detail_parts.append(f"mergeable_state={pull.get('mergeable_state')}")
        return {
            "live_state": state,
            "live_detail": " ".join(detail_parts),
        }

    github_api_url = github_issue_api_url(submission_url)
    if github_api_url:
        try:
            issue = fetch_json(github_api_url)
        except HTTPError as exc:
            deferred = github_deferred_state_from_http_error(github_api_url, exc)
            if deferred:
                return deferred
            return {
                "live_state": "check_failed",
                "live_detail": f"HTTP {exc.code} while querying {github_api_url}",
            }
        except (TimeoutError, URLError) as exc:
            return {
                "live_state": "check_failed",
                "live_detail": f"{type(exc).__name__}: {exc}",
            }
        if issue.get("state") == "open":
            state = "submitted_issue_open"
        elif issue.get("state_reason") == "completed":
            state = "submitted_issue_completed"
        else:
            state = "submitted_issue_closed"
        return {
            "live_state": state,
            "live_detail": (
                f"{issue.get('html_url', submission_url)} state={issue.get('state')}"
                f" state_reason={issue.get('state_reason')}"
            ),
        }

    github_api_url = github_repo_api_url(submission_url)
    if github_api_url:
        try:
            repo = fetch_json(github_api_url)
        except HTTPError as exc:
            deferred = github_deferred_state_from_http_error(github_api_url, exc)
            if deferred:
                return deferred
            return {
                "live_state": "check_failed",
                "live_detail": f"HTTP {exc.code} while querying {github_api_url}",
            }
        except (TimeoutError, URLError) as exc:
            return {
                "live_state": "check_failed",
                "live_detail": f"{type(exc).__name__}: {exc}",
            }
        return {
            "live_state": "submission_repo_available",
            "live_detail": (
                f"{repo.get('html_url', submission_url)} "
                f"default_branch={repo.get('default_branch')} "
                f"archived={repo.get('archived')}"
            ),
        }

    return {
        "live_state": "manual_check_required",
        "live_detail": f"Unsupported submission URL: {submission_url}",
    }


def enrich_live(rows: list[dict]) -> list[dict]:
    enriched = [
        row
        | live_submission_state(row.get("submission_url"))
        | live_public_package_state(row)
        for row in rows
    ]
    return [row | promotion_state(row) for row in enriched]


def enrich_promotion_from_contract(rows: list[dict]) -> list[dict]:
    return [row | promotion_state(row) for row in rows]


def promotion_state(row: dict) -> dict:
    registry_id = row["id"]
    status = row["status"]
    public_state = row.get("public_state")
    live_state = row.get("live_state")

    if status.startswith("published_") and "_pending_" in status:
        return {
            "promotion_state": "partial_publication_verified",
            "next_action": row["blocker"],
        }
    if (
        registry_id == "c_cpp_vcpkg_conan"
        and public_state == "public_listing_available"
    ):
        return {
            "promotion_state": "partial_publication_verified",
            "next_action": (
                "capture ConanCenter publication evidence, then keep vcpkg "
                "deferred under the upstream Rust-library port policy"
            ),
        }
    if public_state == "public_listing_available":
        return {
            "promotion_state": "completion_candidate",
            "next_action": (
                "capture immutable publication evidence and complete the track"
            ),
        }
    if status == "submitted_pending_pkg_go_dev_indexing_proxy_verified":
        return {
            "promotion_state": "partial_publication_verified",
            "next_action": (
                "wait for pkg.go.dev indexing before marking the track complete"
            ),
        }
    if status == "submitted_pending_homebrew_core_review_tap_verified":
        return {
            "promotion_state": "partial_publication_verified",
            "next_action": (
                "open or merge Homebrew/core PR before marking the track complete"
            ),
        }
    if registry_id == "homebrew" and live_state == "submission_repo_available":
        return {
            "promotion_state": "partial_publication_verified",
            "next_action": (
                "open or merge Homebrew/core PR before marking the track complete"
            ),
        }
    if status in {
        "submitted_accepted_pending_spi_index_visibility",
        "submitted_accepted_pending_spi_public_probe",
        "submitted_packagelist_merged_pending_spi_page_probe",
    }:
        return {
            "promotion_state": "publication_needs_follow_up",
            "next_action": (
                "accepted PackageList submission still lacks public SPI "
                "page/version evidence"
            ),
        }
    if live_state == "submitted_issue_completed":
        return {
            "promotion_state": "publication_needs_follow_up",
            "next_action": (
                "closed completed submission issue has no public listing; verify "
                "indexing or capture publication evidence"
            ),
        }
    if live_state == "submitted_issue_closed":
        return {
            "promotion_state": "submission_closed_needs_follow_up",
            "next_action": (
                "closed submission issue has no public listing; reopen, resubmit, "
                "or verify publication evidence"
            ),
        }
    if status == "submitted_feedback_addressed_pending_user_approved_reply":
        return {
            "promotion_state": "approval_required_before_follow_up",
            "next_action": (
                "obtain explicit user approval for the exact outbound corrected "
                "archive reply before sending anything"
            ),
        }
    if registry_id == "r_cran":
        return {
            "promotion_state": "submitted_waiting_review",
            "next_action": (
                "wait for CRAN incoming/pretest or reviewer email, then verify "
                "the public CRAN package page exposes the target version"
            ),
        }
    if registry_id == "conda_forge":
        return {
            "promotion_state": "submitted_waiting_review",
            "next_action": (
                "wait for conda-forge staged-recipes maintainer review, merge, "
                "and feedstock publication"
            ),
        }
    if registry_id == "c_cpp_vcpkg_conan":
        return {
            "promotion_state": "submitted_waiting_review",
            "next_action": (
                "wait for ConanCenter job scheduler and maintainer review; keep "
                "vcpkg deferred under the upstream Rust-library port policy"
            ),
        }
    if status.startswith("submitted_"):
        return {
            "promotion_state": "submitted_waiting_review",
            "next_action": "monitor submitted review or merge state",
        }
    return {
        "promotion_state": "external_gate_blocked",
        "next_action": row["blocker"],
    }


def render_markdown(rows: list[dict], generated_at: str | None = None) -> str:
    has_live = any("live_state" in row for row in rows)
    has_promotion = any("promotion_state" in row for row in rows)
    lines = [
        "# Language Registry External Gates",
        "",
        (
            "These registries are locally prepared but not published. Do not mark "
            "the track complete until the listed external gate has publication, "
            "accepted review, or immutable registry evidence."
        ),
        "",
    ]
    if has_promotion:
        counts: dict[str, int] = {}
        for row in rows:
            state = row.get("promotion_state")
            if isinstance(state, str) and state:
                counts[state] = counts.get(state, 0) + 1
        if counts:
            summary = ", ".join(
                f"`{state}`: {count}" for state, count in counts.items()
            )
            lines.extend([f"Promotion group counts: {summary}.", ""])
    if generated_at:
        lines.extend([f"Generated at (UTC): `{generated_at}`.", ""])
    if has_live:
        header = (
            "| Registry | Package | Status | External gate | Submission | "
            "Submission state | Submission detail | Public package state | "
            "Public detail | Promotion |"
        )
        separator = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
        if has_promotion:
            header += " Next action |"
            separator += " --- |"
        header += " Track |"
        separator += " --- |"
        lines.extend([header, separator])
    else:
        header = "| Registry | Package | Status | External gate | Submission |"
        separator = "| --- | --- | --- | --- | --- |"
        if has_promotion:
            header += " Promotion | Next action |"
            separator += " --- | --- |"
        header += " Track |"
        separator += " --- |"
        lines.extend([header, separator])
    for row in rows:
        if has_live:
            line = (
                f"| {row['registry']} | `{row['package']}` | "
                f"`{row['status']}` | {row['blocker']} | "
                f"{row['submission_url'] or ''} | "
                f"`{row.get('live_state', '')}` | "
                f"{row.get('live_detail', '')} | "
                f"`{row.get('public_state', '')}` | "
                f"{row.get('public_detail', '')} | "
                f"`{row.get('promotion_state', '')}` | "
            )
            if has_promotion:
                line += f"{row.get('next_action', '')} | "
            line += f"`{row['track']}` |"
            lines.append(line)
        else:
            line = (
                f"| {row['registry']} | `{row['package']}` | "
                f"`{row['status']}` | {row['blocker']} | "
                f"{row['submission_url'] or ''} | "
            )
            if has_promotion:
                line += (
                    f"`{row.get('promotion_state', '')}` | "
                    f"{row.get('next_action', '')} | "
                )
            line += f"`{row['track']}` |"
            lines.append(line)
    return "\n".join(lines) + "\n"


def write_or_print(content: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    else:
        print(content, end="")


def promotion_counts(grouped: dict[str, list[dict]]) -> dict[str, int]:
    return {state: len(rows) for state, rows in grouped.items()}


def next_actions_by_registry(
    grouped: dict[str, list[dict]],
) -> dict[str, dict[str, str]]:
    actions: dict[str, dict[str, str]] = {}
    for rows in grouped.values():
        for row in rows:
            actions[row["id"]] = {
                "promotion_state": row["promotion_state"],
                "next_action": row["next_action"],
            }
    return actions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable external gate rows"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="query recorded submission URLs and include live review state",
    )
    parser.add_argument(
        "--promotion",
        action="store_true",
        help=(
            "emit rows grouped by promotion state; combine with --live to query "
            "remote registries"
        ),
    )
    parser.add_argument(
        "--output", help="write the report to this path instead of stdout"
    )
    args = parser.parse_args()

    generated_at = generated_at_utc() if args.live else None
    rows = external_gate_rows(load_contract())
    if args.live:
        rows = enrich_live(rows)
    elif args.promotion:
        rows = enrich_promotion_from_contract(rows)
    if args.promotion:
        grouped: dict[str, list[dict]] = {}
        for row in rows:
            grouped.setdefault(row["promotion_state"], []).append(row)
        write_or_print(
            json.dumps(
                {
                    "report": report_metadata(args.live, generated_at),
                    "next_actions": next_actions_by_registry(grouped),
                    "promotion_counts": promotion_counts(grouped),
                    "promotion_groups": grouped,
                },
                indent=2,
            )
            + "\n",
            args.output,
        )
        return
    if args.json:
        write_or_print(
            json.dumps(
                {
                    "report": report_metadata(args.live, generated_at),
                    "external_gates": rows,
                },
                indent=2,
            )
            + "\n",
            args.output,
        )
    else:
        write_or_print(render_markdown(rows, generated_at), args.output)


if __name__ == "__main__":
    main()
