from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"
TRACK_ROOT = ROOT / "conductor" / "tracks"
ARCHIVE_ROOT = ROOT / "conductor" / "archive"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
LANGUAGE_REGISTRY_GATES_DOC = (
    ROOT / "docs" / "roadmaps" / "language-registry-external-gates.md"
)
EXTERNAL_SUBMISSION_RUNBOOK = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "external-submission-runbook.md"
)
REPORT_SCRIPT = ROOT / "scripts" / "language_registry_external_gate_report.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry(registry_id: str) -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == registry_id
    )


def _metadata(track_id: str) -> dict:
    live_path = TRACK_ROOT / track_id / "metadata.json"
    archive_path = ARCHIVE_ROOT / track_id / "metadata.json"
    path = live_path if live_path.exists() else archive_path
    return json.loads(_read(path))


def _report_module():
    spec = importlib.util.spec_from_file_location(
        "language_registry_external_gate_report", REPORT_SCRIPT
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _http_error(
    url: str,
    code: int,
    body: str = "",
    headers: dict[str, str] | None = None,
) -> HTTPError:
    message = Message()
    for key, value in (headers or {}).items():
        message[key] = value
    return HTTPError(
        url,
        code,
        "test error",
        message,
        io.BytesIO(body.encode("utf-8")),
    )


def test_published_language_registry_entries_do_not_carry_blockers():
    data = json.loads(_read(CONTRACT))
    published = [
        item
        for item in data["registries"]
        if item["current_status"] == "published_verified"
    ]

    assert {item["id"] for item in published} == {
        "dotnet_nuget",
        "go_module_proxy",
        "homebrew",
        "julia_general",
        "jvm_maven_central",
        "matlab_file_exchange",
        "python_pypi",
        "rust_crates_io",
        "stata_ssc",
        "typescript_npm",
    }
    assert all(item["blocker"] is None for item in published)
    assert all(item["submission_url"] for item in published)

    cancelled = [
        item
        for item in data["registries"]
        if "cancelled" in item["current_status"]
    ]
    assert {item["id"] for item in cancelled} == {
        "c_cpp_vcpkg_conan",
        "swift_package_index",
        "vscode_openvsx",
    }
    assert all("Deprecated and cancelled" in item["blocker"] for item in cancelled)


def test_remaining_prepared_registry_tracks_are_blocked_without_publication_claims():
    tracks = _read(TRACKS)
    expected = {}

    for registry_id, (
        track_id,
        current_status,
        blocker_text,
        title,
        publication_status,
    ) in expected.items():
        metadata = _metadata(track_id)
        registry = _registry(registry_id)
        assert metadata["status"] == "blocked"
        assert metadata["current_status"] == current_status
        assert metadata["local_readiness_resolved"] is True
        assert metadata["publication_claimed"] is False
        assert metadata["publication_status"] == publication_status
        assert registry["current_status"] == current_status
        assert registry["localReadinessResolved"] is True
        assert blocker_text in registry["blocker"]
        assert f"- [~] **Track: {title}**" in tracks


def test_conda_forge_is_submitted_but_not_published():
    metadata = _metadata("conda_forge_feedstock_submission_20260524")
    registry = _registry("conda_forge")

    assert metadata["status"] == "submitted"
    assert (
        metadata["current_status"]
        == "submitted_checks_passed_pending_staged_recipes_review"
    )
    assert metadata["publication_claimed"] is False
    assert (
        metadata["submission_url"]
        == "https://github.com/conda-forge/staged-recipes/pull/33452"
    )
    assert (
        registry["submissionEvidence"]["state"]
        == "open_checks_passed_pending_staged_recipes_review"
    )
    latest_probe = registry["preparationEvidence"]["latestLivePrProbe"]
    assert "2026-06-25" in latest_probe
    assert "authenticated live monitor" in latest_probe
    assert "mergeable=MERGEABLE" in latest_probe
    assert "mergeStateStatus=BLOCKED" in latest_probe
    assert "bffc5bf1a85389dc695adfd96c87bf2413f4db25" in latest_probe
    assert "checks remain successful" in latest_probe
    assert "no actionable comments" in latest_probe
    assert "nwau-py-feedstock repository still return HTTP 404" in latest_probe
    assert (
        "no actionable comments" in metadata["package_evidence"]["latest_live_pr_probe"]
    )
    assert "maintainer review/merge/feedstock publication" in registry["blocker"]


def test_julia_general_is_published_verified():
    metadata = _metadata("julia_general_registry_submission_20260524")
    registry = _registry("julia_general")

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert registry["current_status"] == "published_verified"
    assert metadata["publication_claimed"] is True
    assert (
        metadata["submission_url"]
        == "https://github.com/JuliaRegistries/General/pull/156254"
    )
    assert (
        registry["submission_url"]
        == "https://github.com/JuliaRegistries/General/pull/156254"
    )
    assert (
        registry["submissionEvidence"]["repository"]
        == "https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl"
    )
    assert (
        registry["submissionEvidence"]["triggerIssue"]
        == "https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1"
    )
    assert (
        registry["submissionEvidence"]["commit"]
        == "56ddec5ae29513e80717d4625f82c024a211c949"
    )
    assert (
        registry["submissionEvidence"]["prHead"]
        == "bb63b2a81ec2ded2c5675f09fb6cd63128f10a07"
    )
    assert (
        registry["submissionEvidence"]["uuid"] == "58dad789-f56a-4ab3-a66f-c15139bf9cbe"
    )
    assert registry["submissionEvidence"]["checks"] == "successful"
    assert registry["submissionEvidence"]["automergeWait"] == "3-day new-package wait"
    assert registry["submissionEvidence"]["mergedAt"] == "2026-05-28T15:34:44Z"
    assert registry["blocker"] is None


def test_go_module_proxy_and_pkg_go_dev_are_published():
    metadata = _metadata("go_module_registry_submission_20260524")
    registry = _registry("go_module_proxy")

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["publication_status"] == "published_verified"
    assert metadata["publication_claimed"] is True
    assert registry["publicationEvidence"]["version"] == "v0.1.0"
    assert "indexed version 0.1.0" in registry["publicationEvidence"]["pkgGoDevStatus"]


def test_external_gate_report_matches_blocked_registry_contract():
    result = subprocess.run(
        [sys.executable, "scripts/language_registry_external_gate_report.py", "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    data = json.loads(_read(CONTRACT))
    blocked_ids = {
        item["id"]
        for item in data["registries"]
        if item["current_status"] != "published_verified"
    }

    assert payload["report"] == {"live": False}
    assert {item["id"] for item in payload["external_gates"]} == blocked_ids
    assert all(item["blocker"] for item in payload["external_gates"])
    assert all(
        set(item)
        == {
            "blocker",
            "id",
            "package",
            "registry",
            "status",
            "submission_url",
            "track",
            "version",
        }
        for item in payload["external_gates"]
    )


def test_language_registry_submission_validator_enforces_track_consistency():
    data = json.loads(_read(CONTRACT))
    tracks_md = _read(TRACKS)

    for registry in data["registries"]:
        metadata = _metadata(registry["track"])
        assert metadata["track_id"] == registry["track"]
        assert metadata["registry_id"] == registry["id"]
        assert metadata["current_status"] == registry["current_status"]
        assert (
            metadata["local_readiness_resolved"] == registry["localReadinessResolved"]
        )
        if registry["current_status"] == "published_verified":
            assert metadata["status"] == "completed"
            assert registry["blocker"] is None
            assert metadata["publication_claimed"] is True
            assert f"- [x] **Track: {registry['title']}**" in tracks_md
        elif "cancelled" in registry["current_status"]:
            assert metadata["status"] in {"completed", "cancelled"}
            assert metadata["blocker"]
            assert "cancelled" in metadata["current_status"]
        else:
            assert registry["blocker"]
            assert metadata["status"] in {"blocked", "submitted"} or metadata[
                "status"
            ].startswith("submitted_")
            assert metadata["publication_claimed"] is False
            assert f"- [~] **Track: {registry['title']}**" in tracks_md


def test_external_gate_report_can_write_output_file(tmp_path):
    output = tmp_path / "external-gates.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/language_registry_external_gate_report.py",
            "--json",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == ""
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["report"] == {"live": False}
    assert "external_gates" in payload
    assert {item["id"] for item in payload["external_gates"]}


def test_promotion_report_is_non_live_by_default(tmp_path):
    output = tmp_path / "promotion.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/language_registry_external_gate_report.py",
            "--promotion",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == ""
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["report"] == {"live": False}
    assert "generated_at_utc" not in payload["report"]
    assert payload["promotion_counts"] == {
        "deprecated_cancelled": 3,
        "submitted_waiting_review": 2,
    }
    assert "stata_ssc" not in payload["next_actions"]
    assert (
        payload["next_actions"]["conda_forge"]["next_action"]
        == "wait for conda-forge staged-recipes maintainer review, merge, "
        "and feedstock publication"
    )
    assert "promotion_groups" in payload
    flattened = [row for rows in payload["promotion_groups"].values() for row in rows]
    assert all("live_state" not in row for row in flattened)
    assert all(
        set(row)
        == {
            "blocker",
            "id",
            "next_action",
            "package",
            "promotion_state",
            "registry",
            "status",
            "submission_url",
            "track",
            "version",
        }
        for row in flattened
    )
    assert "partial_publication_verified" not in payload["promotion_groups"]


def test_external_gate_report_metadata_is_timestamped_only_for_live_reports():
    module = _report_module()

    assert module.report_metadata(False) == {"live": False}
    assert module.report_metadata(True, "2026-06-14T00:00:00Z") == {
        "live": True,
        "generated_at_utc": "2026-06-14T00:00:00Z",
    }
    assert module.generated_at_utc().endswith("Z")


def test_external_gate_report_live_helpers_classify_submission_urls(monkeypatch):
    module = _report_module()

    assert (
        module.github_pull_api_url(
            "https://github.com/conda-forge/staged-recipes/pull/33452"
        )
        == "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
    )
    assert module.github_pull_api_url("https://example.com/not/a/pr") is None
    assert (
        module.github_issue_api_url(
            "https://github.com/SwiftPackageIndex/PackageList/issues/13717"
        )
        == "https://api.github.com/repos/SwiftPackageIndex/PackageList/issues/13717"
    )
    assert (
        module.github_repo_api_url("https://github.com/edithatogo/homebrew-mchs")
        == "https://api.github.com/repos/edithatogo/homebrew-mchs"
    )
    assert module.live_submission_state(None)["live_state"] == "blocked_no_submission"

    def fake_fetch_json(url: str, timeout: int = 20) -> dict:
        assert (
            url == "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
        )
        return {
            "html_url": "https://github.com/conda-forge/staged-recipes/pull/33452",
            "state": "open",
            "merged": False,
            "draft": False,
            "mergeable": True,
            "mergeable_state": "clean",
        }

    monkeypatch.setattr(module, "fetch_json", fake_fetch_json)
    live = module.live_submission_state(
        "https://github.com/conda-forge/staged-recipes/pull/33452"
    )
    assert live["live_state"] == "submitted_open"
    assert "merged=False" in live["live_detail"]
    assert "mergeable=True" in live["live_detail"]
    assert "mergeable_state=clean" in live["live_detail"]

    def fake_fetch_repo_json(url: str, timeout: int = 20) -> dict:
        assert url == "https://api.github.com/repos/edithatogo/homebrew-mchs"
        return {
            "html_url": "https://github.com/edithatogo/homebrew-mchs",
            "default_branch": "main",
            "archived": False,
        }

    monkeypatch.setattr(module, "fetch_json", fake_fetch_repo_json)
    repo_live = module.live_submission_state(
        "https://github.com/edithatogo/homebrew-mchs"
    )
    assert repo_live["live_state"] == "submission_repo_available"
    assert "default_branch=main" in repo_live["live_detail"]

    def fake_fetch_status(url: str, timeout: int = 20) -> int:
        assert (
            url
            == "https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/list"
        )
        return 200

    monkeypatch.setattr(module, "fetch_status", fake_fetch_status)
    go_live = module.live_submission_state(
        "https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/list"
    )
    assert go_live["live_state"] == "go_proxy_available"

    def fake_fetch_issue_json(url: str, timeout: int = 20) -> dict:
        assert (
            url
            == "https://api.github.com/repos/SwiftPackageIndex/PackageList/issues/13717"
        )
        return {
            "html_url": "https://github.com/SwiftPackageIndex/PackageList/issues/13717",
            "state": "open",
        }

    monkeypatch.setattr(module, "fetch_json", fake_fetch_issue_json)
    issue_live = module.live_submission_state(
        "https://github.com/SwiftPackageIndex/PackageList/issues/13717"
    )
    assert issue_live["live_state"] == "submitted_issue_open"

    def fake_fetch_closed_issue_json(url: str, timeout: int = 20) -> dict:
        assert (
            url
            == "https://api.github.com/repos/SwiftPackageIndex/PackageList/issues/13717"
        )
        return {
            "html_url": "https://github.com/SwiftPackageIndex/PackageList/issues/13717",
            "state": "closed",
            "state_reason": "completed",
        }

    monkeypatch.setattr(module, "fetch_json", fake_fetch_closed_issue_json)
    completed_issue_live = module.live_submission_state(
        "https://github.com/SwiftPackageIndex/PackageList/issues/13717"
    )
    assert completed_issue_live["live_state"] == "submitted_issue_completed"
    assert "state_reason=completed" in completed_issue_live["live_detail"]

    def fake_rate_limited_json(url: str, timeout: int = 20) -> dict:
        raise _http_error(
            url,
            403,
            body='{"message":"API rate limit exceeded"}',
            headers={
                "x-ratelimit-remaining": "0",
                "x-ratelimit-reset": "1770000000",
            },
        )

    monkeypatch.setattr(module, "fetch_json", fake_rate_limited_json)
    rate_limited_live = module.live_submission_state(
        "https://github.com/conda-forge/staged-recipes/pull/33452"
    )
    assert rate_limited_live["live_state"] == "check_deferred_rate_limited"
    assert "x-ratelimit-reset=1770000000" in rate_limited_live["live_detail"]

    def fake_forbidden_json(url: str, timeout: int = 20) -> dict:
        raise _http_error(url, 403, body='{"message":"Resource protected"}')

    monkeypatch.setattr(module, "fetch_json", fake_forbidden_json)
    forbidden_live = module.live_submission_state(
        "https://github.com/edithatogo/homebrew-mchs"
    )
    assert forbidden_live["live_state"] == "check_deferred_forbidden"
    assert "GitHub API forbidden" in forbidden_live["live_detail"]


def test_external_gate_report_live_helpers_classify_public_registry_probes(monkeypatch):
    module = _report_module()
    contract = json.loads(_read(CONTRACT))
    rows = module.external_gate_rows(contract)
    by_id = {row["id"]: row for row in rows}
    dotnet_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "dotnet_nuget"
    )
    go_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "go_module_proxy"
    )
    homebrew_registry = next(
        registry for registry in contract["registries"] if registry["id"] == "homebrew"
    )
    swift_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "swift_package_index"
    )

    rust_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "rust_crates_io"
    )
    assert (
        module.public_probe_url(rust_registry)
        == "https://crates.io/api/v1/crates/nwau-core"
    )
    assert (
        module.public_probe_url(dotnet_registry)
        == "https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json"
    )
    maven_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "jvm_maven_central"
    )
    matlab_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "matlab_file_exchange"
    )
    vscode_registry = next(
        registry
        for registry in contract["registries"]
        if registry["id"] == "vscode_openvsx"
    )
    assert (
        module.public_probe_url(maven_registry)
        == "https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml"
    )
    assert "jvm_maven_central" not in by_id
    assert module.promotion_state(by_id["swift_package_index"])[
        "promotion_state"
    ] == "deprecated_cancelled"
    assert "matlab_file_exchange" not in by_id
    assert module.promotion_state(by_id["vscode_openvsx"])[
        "promotion_state"
    ] == "deprecated_cancelled"
    assert (
        module.public_probe_url(go_registry)
        == "https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go"
    )
    assert (
        module.public_probe_url(homebrew_registry)
        == "https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb"
    )
    assert (
        module.public_probe_url(vscode_registry)
        == "https://open-vsx.org/api/edithatogo/mchs-tools"
    )
    assert module.public_probe_url(matlab_registry) == (
        "https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop"
    )

    assert (
        module.request_headers_for_url(
            "https://open-vsx.org/api/edithatogo/mchs-tools"
        )["Accept"]
        == "application/json"
    )
    assert (
        module.request_headers_for_url(
            "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
        )["Accept"]
        == "application/vnd.github+json"
    )
    assert "Authorization" not in module.request_headers_for_url(
        "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
    )
    monkeypatch.setenv("GH_TOKEN", "gh-test-token")
    assert (
        module.request_headers_for_url(
            "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
        )["Authorization"]
        == "Bearer gh-test-token"
    )
    monkeypatch.setenv("GITHUB_TOKEN", "github-test-token")
    assert (
        module.request_headers_for_url(
            "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
        )["Authorization"]
        == "Bearer github-test-token"
    )
    assert "Authorization" not in module.request_headers_for_url(
        "https://open-vsx.org/api/edithatogo/mchs-tools"
    )

    def fake_status(url: str, timeout: int = 20) -> int:
        if "swiftpackageindex.com" in url:
            return 403
        if "pkg.go.dev" in url:
            return 404
        if "crates.io" in url:
            return 404
        return 500

    def fake_json(url: str, timeout: int = 20) -> dict:
        if "crates.io" in url:
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if "open-vsx.org" in url:
            return {
                "namespace": "edithatogo",
                "name": "mchs-tools",
                "version": "0.1.1",
                "allVersions": {"0.1.1": {}, "0.1.0": {}, "latest": {}},
            }
        raise AssertionError(f"unexpected JSON fetch: {url}")

    def fake_text(url: str, timeout: int = 20) -> str:
        if "pkg.go.dev" in url:
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if "swiftpackageindex.com" in url:
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if "raw.githubusercontent.com/edithatogo/homebrew-mchs" in url:
            return (
                'url "https://files.pythonhosted.org/packages/source/n/nwau-py/'
                'nwau_py-0.2.2.tar.gz"\n'
                'sha256 "6f987bc4a81f3ac78cbc893d6a502fc572a534905f9f1f89'
                'cfc05600ff4ddff3"\n'
            )
        if "mathworks.com/matlabcentral/fileexchange" in url:
            return (
                "<h1>MCHS MATLAB Interop</h1>"
                "<a>Version 0.1.0</a>"
                "<strong>Your submission has been published in File Exchange.</strong>"
            )
        raise AssertionError(f"unexpected text fetch: {url}")

    def fake_json_post(url: str, payload: dict, timeout: int = 20) -> dict:
        if "marketplace.visualstudio.com" in url:
            criteria = payload["filters"][0]["criteria"][0]
            assert criteria["filterType"] == 7
            assert criteria["value"] == "edithatogo.mchs-tools"
            return {
                "results": [
                    {
                        "extensions": [
                            {
                                "publisher": {"publisherName": "edithatogo"},
                                "extensionName": "mchs-tools",
                                "versions": [{"version": "0.1.1"}],
                            }
                        ]
                    }
                ]
            }
        raise AssertionError(f"unexpected JSON POST fetch: {url}")

    monkeypatch.setattr(module, "fetch_status", fake_status)
    monkeypatch.setattr(module, "fetch_json", fake_json)
    monkeypatch.setattr(module, "fetch_json_post", fake_json_post)
    monkeypatch.setattr(module, "fetch_text", fake_text)
    assert (
        module.live_public_package_state(rust_registry)["public_state"]
        == "public_listing_missing"
    )
    assert (
        module.live_public_package_state(go_registry)["public_state"]
        == "public_listing_missing"
    )
    assert (
        module.live_public_package_state(homebrew_registry)["public_state"]
        == "public_listing_available"
    )
    assert (
        module.live_public_package_state(swift_registry)["public_state"]
        == "public_listing_missing"
    )
    vscode_public_state = module.live_public_package_state(vscode_registry)
    assert vscode_public_state["public_state"] == "public_listing_available"
    assert "Open VSX" in vscode_public_state["public_detail"]
    assert "Visual Studio Marketplace" in vscode_public_state["public_detail"]
    assert (
        module.live_public_package_state(matlab_registry)["public_state"]
        == "public_listing_available"
    )


def test_external_gate_report_cran_probe_checks_package_page_crandb_and_index(
    monkeypatch,
):
    module = _report_module()
    cran = {"id": "r_cran", "package": "nwauR", "version": "0.1.0"}
    calls: list[str] = []

    def fake_text(url: str, timeout: int = 20) -> str:
        calls.append(url)
        if url.endswith("/web/packages/nwauR/index.html"):
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/src/contrib/PACKAGES"):
            return "Package: otherpkg\nVersion: 1.0.0\n"
        raise AssertionError(f"unexpected text fetch: {url}")

    def fake_json(url: str, timeout: int = 20) -> dict:
        calls.append(url)
        raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(module, "fetch_text", fake_text)
    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(cran)

    assert state["public_state"] == "public_listing_missing"
    assert (
        "package page https://cran.r-project.org/web/packages/nwauR/index.html HTTP 404"
        in state["public_detail"]
    )
    assert "CRANDB https://crandb.r-pkg.org/nwauR HTTP 404" in state["public_detail"]
    assert (
        "PACKAGES index https://cran.r-project.org/src/contrib/PACKAGES has "
        "no Package: nwauR" in state["public_detail"]
    )
    assert calls == [
        "https://cran.r-project.org/web/packages/nwauR/index.html",
        "https://crandb.r-pkg.org/nwauR",
        "https://cran.r-project.org/src/contrib/PACKAGES",
    ]


def test_external_gate_report_cran_probe_requires_target_version_evidence(
    monkeypatch,
):
    module = _report_module()
    cran = {"id": "r_cran", "package": "nwauR", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if url.endswith("/web/packages/nwauR/index.html"):
            return "<html><h1>nwauR</h1><p>Version 0.0.9</p></html>"
        if url.endswith("/src/contrib/PACKAGES"):
            return "Package: nwauR\nVersion: 0.0.9\n"
        raise AssertionError(f"unexpected text fetch: {url}")

    def fake_json(url: str, timeout: int = 20) -> dict:
        assert url == "https://crandb.r-pkg.org/nwauR"
        return {"Package": "nwauR", "Version": "0.0.9"}

    monkeypatch.setattr(module, "fetch_text", fake_text)
    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(cran)

    assert state["public_state"] == "public_listing_version_unverified"
    assert "version 0.1.0 was not found" in state["public_detail"]
    assert "contains nwauR but version 0.1.0 was not found" in state["public_detail"]


def test_external_gate_report_cran_probe_accepts_public_index_version(monkeypatch):
    module = _report_module()
    cran = {"id": "r_cran", "package": "nwauR", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if url.endswith("/web/packages/nwauR/index.html"):
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/src/contrib/PACKAGES"):
            return (
                "Package: otherpkg\nVersion: 1.0.0\n\nPackage: nwauR\nVersion: 0.1.0\n"
            )
        raise AssertionError(f"unexpected text fetch: {url}")

    def fake_json(url: str, timeout: int = 20) -> dict:
        raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(module, "fetch_text", fake_text)
    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(cran)

    assert state["public_state"] == "public_listing_available"
    assert (
        "PACKAGES index https://cran.r-project.org/src/contrib/PACKAGES "
        "contains nwauR 0.1.0" in state["public_detail"]
    )
    assert module.cran_packages_index_has_version(
        "Package: nwauR\nVersion: 0.1.0\n", "nwauR", "0.1.0"
    )


def test_external_gate_report_conda_probe_checks_anaconda_and_feedstock(monkeypatch):
    module = _report_module()
    row = {"id": "conda_forge", "package": "nwau-py", "version": "0.2.2"}
    calls: list[str] = []

    def fake_json(url: str, timeout: int = 20) -> dict:
        calls.append(url)
        raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_missing"
    assert (
        "Anaconda https://api.anaconda.org/package/conda-forge/nwau-py HTTP 404"
        in state["public_detail"]
    )
    assert (
        "feedstock https://api.github.com/repos/conda-forge/nwau-py-feedstock HTTP 404"
        in state["public_detail"]
    )
    assert calls == [
        "https://api.anaconda.org/package/conda-forge/nwau-py",
        "https://api.github.com/repos/conda-forge/nwau-py-feedstock",
    ]


def test_external_gate_report_conda_feedstock_without_package_is_unverified(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "conda_forge", "package": "nwau-py", "version": "0.2.2"}

    def fake_json(url: str, timeout: int = 20) -> dict:
        if "api.anaconda.org" in url:
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/conda-forge/nwau-py-feedstock"):
            return {
                "html_url": "https://github.com/conda-forge/nwau-py-feedstock",
                "default_branch": "main",
                "archived": False,
            }
        raise AssertionError(f"unexpected JSON fetch: {url}")

    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_version_unverified"
    assert (
        "feedstock https://github.com/conda-forge/nwau-py-feedstock"
        in state["public_detail"]
    )
    assert "Anaconda package version evidence is missing" in state["public_detail"]
    assert (
        module.promotion_state(
            row
            | {
                "status": "submitted_checks_passed_pending_staged_recipes_review",
                "blocker": "feedstock publication pending",
                "public_state": state["public_state"],
            }
        )["promotion_state"]
        == "submitted_waiting_review"
    )


def test_external_gate_report_conda_package_version_completes_public_probe(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "conda_forge", "package": "nwau-py", "version": "0.2.2"}

    def fake_json(url: str, timeout: int = 20) -> dict:
        if "api.anaconda.org" in url:
            return {"files": [{"version": "0.2.2"}]}
        if url.endswith("/conda-forge/nwau-py-feedstock"):
            return {
                "html_url": "https://github.com/conda-forge/nwau-py-feedstock",
                "default_branch": "main",
                "archived": False,
            }
        raise AssertionError(f"unexpected JSON fetch: {url}")

    monkeypatch.setattr(module, "fetch_json", fake_json)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_available"
    assert (
        "Anaconda https://api.anaconda.org/package/conda-forge/nwau-py "
        "version 0.2.2 found" in state["public_detail"]
    )
    assert (
        "feedstock https://github.com/conda-forge/nwau-py-feedstock"
        in state["public_detail"]
    )


def test_external_gate_report_c_cpp_probe_checks_conancenter_before_vcpkg(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "c_cpp_vcpkg_conan", "package": "nwau-c-abi", "version": "0.1.0"}
    calls: list[str] = []

    def fake_text(url: str, timeout: int = 20) -> str:
        calls.append(url)
        raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_missing"
    assert "ConanCenter conanfile" in state["public_detail"]
    assert "ConanCenter conandata" in state["public_detail"]
    assert "vcpkg" in state["public_detail"]
    assert calls == [
        (
            "https://raw.githubusercontent.com/conan-io/conan-center-index/"
            "master/recipes/nwau-c-abi/all/conanfile.py"
        ),
        (
            "https://raw.githubusercontent.com/conan-io/conan-center-index/"
            "master/recipes/nwau-c-abi/all/conandata.yml"
        ),
        (
            "https://raw.githubusercontent.com/microsoft/vcpkg/master/"
            "ports/nwau-c-abi/vcpkg.json"
        ),
    ]


def test_external_gate_report_c_cpp_probe_accepts_conancenter_version(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "c_cpp_vcpkg_conan", "package": "nwau-c-abi", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if url.endswith("/conanfile.py"):
            return 'class NwauCAbiConan(ConanFile):\n    name = "nwau-c-abi"\n'
        if url.endswith("/conandata.yml"):
            return (
                'sources:\n  "0.1.0":\n    url: "https://example.invalid/src.tar.gz"\n'
            )
        if url.endswith("/vcpkg.json"):
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        raise AssertionError(f"unexpected text fetch: {url}")

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_available"
    assert "ConanCenter conanfile" in state["public_detail"]
    assert "ConanCenter conandata" in state["public_detail"]
    assert "version 0.1.0 found" in state["public_detail"]
    assert "vcpkg" in state["public_detail"]


def test_external_gate_report_c_cpp_vcpkg_only_does_not_complete(monkeypatch):
    module = _report_module()
    row = {"id": "c_cpp_vcpkg_conan", "package": "nwau-c-abi", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if "conan-center-index" in url:
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/vcpkg.json"):
            return '{"name": "nwau-c-abi", "version-string": "0.1.0"}'
        raise AssertionError(f"unexpected text fetch: {url}")

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_version_unverified"
    assert (
        "vcpkg listing exists but ConanCenter publication still needs evidence"
        in state["public_detail"]
    )
    assert (
        module.promotion_state(
            row
            | {
                "status": (
                    "submitted_conancenter_cla_resolved_pending_scheduler_review_"
                    "vcpkg_deferred"
                ),
                "blocker": "ConanCenter pending",
                "public_state": state["public_state"],
            }
        )["promotion_state"]
        == "submitted_waiting_review"
    )


def test_external_gate_report_stata_ssc_probe_checks_pkg_ado_and_help(monkeypatch):
    module = _report_module()
    row = {"id": "stata_ssc", "package": "mchs-stata-interop", "version": "0.1.0"}
    calls: list[str] = []

    def fake_text(url: str, timeout: int = 20) -> str:
        calls.append(url)
        raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_missing"
    assert "SSC package manifest" in state["public_detail"]
    assert "SSC ado" in state["public_detail"]
    assert "SSC help" in state["public_detail"]
    assert calls == [
        "http://fmwww.bc.edu/repec/bocode/m/mchs.pkg",
        "http://fmwww.bc.edu/repec/bocode/m/mchs.ado",
        "http://fmwww.bc.edu/repec/bocode/m/mchs.sthlp",
    ]


def test_external_gate_report_stata_ssc_probe_accepts_installable_package(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "stata_ssc", "package": "mchs-stata-interop", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if url.endswith("/mchs.pkg"):
            return (
                "d 'MCHS': module to provide Stata file/CLI boundary adapter\n"
                "d Author: Dylan Mordaunt\n"
                "d Support: email dylan.mordaunt@@vuw.ac.nz\n"
                "f mchs.ado\n"
                "f mchs.sthlp\n"
            )
        if url.endswith("/mchs.ado"):
            return "program define mchs, rclass\nend\n"
        if url.endswith("/mchs.sthlp"):
            return "{title:MCHS Stata file/CLI boundary adapter}\n{cmd:mchs import}"
        raise AssertionError(f"unexpected text fetch: {url}")

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_available"
    assert "SSC package manifest" in state["public_detail"]
    assert "semantic version 0.1.0 is local archive evidence" in state["public_detail"]
    assert "SSC ado" in state["public_detail"]
    assert "SSC help" in state["public_detail"]


def test_external_gate_report_stata_ssc_probe_requires_manifest_identity(
    monkeypatch,
):
    module = _report_module()
    row = {"id": "stata_ssc", "package": "mchs-stata-interop", "version": "0.1.0"}

    def fake_text(url: str, timeout: int = 20) -> str:
        if url.endswith("/mchs.pkg"):
            return "d Unrelated package\nf mchs.ado\nf mchs.sthlp\n"
        if url.endswith("/mchs.ado"):
            return "program define mchs, rclass\nend\n"
        if url.endswith("/mchs.sthlp"):
            return "{title:MCHS Stata file/CLI boundary adapter}\n"
        raise AssertionError(f"unexpected text fetch: {url}")

    monkeypatch.setattr(module, "fetch_text", fake_text)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_version_unverified"
    assert "available but package identity was not verified" in state["public_detail"]


def test_external_gate_report_requires_vscode_version_on_both_marketplaces(monkeypatch):
    module = _report_module()
    vscode = {
        "id": "vscode_openvsx",
        "package": "mchs-tools",
        "version": "0.1.1",
    }

    def fake_json(url: str, timeout: int = 20) -> dict:
        assert "open-vsx.org" in url
        return {
            "namespace": "edithatogo",
            "name": "mchs-tools",
            "version": "0.1.1",
            "allVersions": {"0.1.1": {}, "0.1.0": {}, "latest": {}},
        }

    def fake_json_post(url: str, payload: dict, timeout: int = 20) -> dict:
        assert "marketplace.visualstudio.com" in url
        return {
            "results": [
                {
                    "extensions": [
                        {
                            "publisher": {"publisherName": "edithatogo"},
                            "extensionName": "mchs-tools",
                            "versions": [{"version": "0.1.0"}],
                        }
                    ]
                }
            ]
        }

    monkeypatch.setattr(module, "fetch_json", fake_json)
    monkeypatch.setattr(module, "fetch_json_post", fake_json_post)

    state = module.live_public_package_state(vscode)

    assert state["public_state"] == "public_listing_version_unverified"
    assert "Open VSX" in state["public_detail"]
    assert "Visual Studio Marketplace" in state["public_detail"]
    assert "version 0.1.1 was not found" in state["public_detail"]


def test_external_gate_report_public_probes_require_version_evidence(monkeypatch):
    module = _report_module()
    dotnet = {
        "id": "dotnet_nuget",
        "package": "Mchs.Bindings.DotNet",
        "version": "0.1.0",
    }

    monkeypatch.setattr(
        module, "fetch_json", lambda url, timeout=20: {"versions": ["0.0.1"]}
    )

    state = module.live_public_package_state(dotnet)

    assert state["public_state"] == "public_listing_version_unverified"
    assert "version 0.1.0 was not found" in state["public_detail"]


def test_external_gate_report_status_only_public_probes_do_not_complete(monkeypatch):
    module = _report_module()
    row = {
        "id": "swift_package_index",
        "package": "MCHSBind",
        "version": "0.1.0",
    }

    monkeypatch.setattr(module, "fetch_text", lambda url, timeout=20: "package page")
    monkeypatch.setattr(module, "fetch_status", lambda url, timeout=20: 200)

    state = module.live_public_package_state(row)

    assert state["public_state"] == "public_listing_version_unverified"
    assert (
        module.promotion_state(
            {
                "id": "swift_package_index",
                "status": "submitted_pending_swift_package_index_review",
                "public_state": state["public_state"],
                "live_state": "submitted_issue_open",
                "blocker": "review pending",
            }
        )["promotion_state"]
        == "submitted_waiting_review"
    )


def test_external_gate_report_go_and_swift_text_probes_require_target_version(
    monkeypatch,
):
    module = _report_module()

    def fake_text(url, timeout=20):
        if "swiftpackageindex.com" in url:
            return "MCHSBind mchs-swift package page includes v0.1.0 release"
        return "pkg page includes v0.1.0 release"

    monkeypatch.setattr(module, "fetch_text", fake_text)

    go_state = module.live_public_package_state(
        {
            "id": "go_module_proxy",
            "package": "github.com/edithatogo/mchs/bindings/go",
            "version": "0.1.0",
        }
    )
    swift_state = module.live_public_package_state(
        {
            "id": "swift_package_index",
            "package": "MCHSBind",
            "version": "0.1.0",
        }
    )

    assert go_state["public_state"] == "public_listing_available"
    assert swift_state["public_state"] == "public_listing_available"


def test_external_gate_report_swift_probe_rejects_cloudflare_token_false_positive(
    monkeypatch,
):
    module = _report_module()

    monkeypatch.setattr(
        module,
        "fetch_text",
        lambda url, timeout=20: (
            "<html><head><title>Just a moment...</title></head>"
            "<body>Enable JavaScript and cookies to continue "
            "https://challenges.cloudflare.com token 0.1.0</body></html>"
        ),
    )

    state = module.live_public_package_state(
        {
            "id": "swift_package_index",
            "package": "MCHSBind",
            "version": "0.1.0",
        }
    )

    assert state["public_state"] == "public_listing_blocked"
    assert "Cloudflare challenge" in state["public_detail"]


def test_external_gate_report_classifies_promotion_state():
    module = _report_module()

    go_row = {
        "id": "go_module_proxy",
        "status": "submitted_pending_pkg_go_dev_indexing_proxy_verified",
        "public_state": "public_listing_missing",
        "live_state": "go_proxy_available",
        "blocker": "pkg.go.dev pending",
    }
    assert (
        module.promotion_state(go_row)["promotion_state"]
        == "partial_publication_verified"
    )

    indexed_go_row = go_row | {"public_state": "public_listing_available"}
    assert (
        module.promotion_state(indexed_go_row)["promotion_state"]
        == "completion_candidate"
    )

    partial_vscode_row = {
        "id": "vscode_openvsx",
        "status": (
            "published_marketplace_pending_openvsx_eclipse_agreement_token_publish"
        ),
        "public_state": "public_listing_available",
        "live_state": "manual_check_required",
        "blocker": "Open VSX agreement/token/publish still pending",
    }
    partial_vscode_state = module.promotion_state(partial_vscode_row)
    assert partial_vscode_state["promotion_state"] == "partial_publication_verified"
    assert partial_vscode_state["next_action"] == partial_vscode_row["blocker"]

    conda_row = {
        "id": "conda_forge",
        "status": "submitted_pending_staged_recipes_review",
        "public_state": "public_listing_missing",
        "live_state": "submitted_open",
        "blocker": "review pending",
    }
    assert (
        module.promotion_state(conda_row)["promotion_state"]
        == "submitted_waiting_review"
    )
    assert "feedstock publication" in module.promotion_state(conda_row)["next_action"]
    deferred_conda_row = conda_row | {"live_state": "check_deferred_rate_limited"}
    assert (
        module.promotion_state(deferred_conda_row)["promotion_state"]
        == "submitted_waiting_review"
    )

    stata_row = {
        "id": "stata_ssc",
        "status": "published_verified",
        "public_state": "public_listing_available",
        "live_state": "manual_check_required",
        "blocker": None,
    }
    stata_state = module.promotion_state(stata_row)
    assert stata_state["promotion_state"] == "completion_candidate"
    assert "capture immutable publication evidence" in stata_state["next_action"]

    cran_row = {
        "id": "r_cran",
        "status": "submitted_confirmed_pending_cran_pretest_review_publication",
        "public_state": "public_listing_missing",
        "live_state": "manual_check_required",
        "blocker": "CRAN pretest pending",
    }
    assert "CRAN incoming/pretest" in module.promotion_state(cran_row)["next_action"]

    conan_row = {
        "id": "c_cpp_vcpkg_conan",
        "status": "deprecated_cancelled_not_published",
        "public_state": "public_listing_missing",
        "live_state": "submitted_open",
        "blocker": "Conan scheduler pending",
    }
    assert module.promotion_state(conan_row)["promotion_state"] == (
        "deprecated_cancelled"
    )
    assert (
        "historical evidence only" in module.promotion_state(conan_row)["next_action"]
    )
    conan_published_row = conan_row | {"public_state": "public_listing_available"}
    conan_published_state = module.promotion_state(conan_published_row)
    assert conan_published_state["promotion_state"] == "deprecated_cancelled"

    julia_row = {
        "id": "julia_general",
        "status": "published_verified",
        "public_state": "public_listing_available",
        "live_state": "submitted_open",
        "blocker": None,
    }
    assert (
        module.promotion_state(julia_row)["promotion_state"] == "completion_candidate"
    )

    merged_conda_row = conda_row | {"public_state": "public_listing_available"}
    assert (
        module.promotion_state(merged_conda_row)["promotion_state"]
        == "completion_candidate"
    )

    closed_issue_row = {
        "id": "swift_package_index",
        "status": "submitted_packagelist_merged_pending_spi_page_probe",
        "public_state": "public_listing_missing",
        "live_state": "submitted_issue_completed",
        "blocker": (
            "Swift Package Index PackageList PR merged without public page evidence."
        ),
    }
    assert (
        module.promotion_state(closed_issue_row)["promotion_state"]
        == "publication_needs_follow_up"
    )

    indexed_closed_issue_row = closed_issue_row | {
        "public_state": "public_listing_available"
    }
    assert (
        module.promotion_state(indexed_closed_issue_row)["promotion_state"]
        == "completion_candidate"
    )

    published_swift_row = {
        "id": "swift_package_index",
        "status": "published_verified",
        "public_state": "public_listing_available",
        "live_state": "submitted_issue_completed",
        "blocker": None,
    }
    assert (
        module.promotion_state(published_swift_row)["promotion_state"]
        == "completion_candidate"
    )

    rejected_issue_row = closed_issue_row | {
        "status": "submitted_pending_swift_package_index_review",
        "live_state": "submitted_issue_closed",
    }
    assert (
        module.promotion_state(rejected_issue_row)["promotion_state"]
        == "submission_closed_needs_follow_up"
    )

    ready_row = {
        "id": "dotnet_nuget",
        "status": "prepared_pending_nuget_api_key_and_push",
        "public_state": "public_listing_available",
        "live_state": "blocked_no_submission",
        "blocker": "old blocker",
    }
    assert (
        module.promotion_state(ready_row)["promotion_state"] == "completion_candidate"
    )

    blocked_row = {
        "id": "rust_crates_io",
        "status": "prepared_pending_crates_token_and_cargo_publish",
        "public_state": "public_listing_missing",
        "live_state": "blocked_no_submission",
        "blocker": "token missing",
    }
    assert (
        module.promotion_state(blocked_row)["promotion_state"]
        == "external_gate_blocked"
    )


def test_non_live_promotion_group_counts_are_stable_from_contract():
    module = _report_module()
    rows = module.enrich_promotion_from_contract(
        module.external_gate_rows(json.loads(_read(CONTRACT)))
    )
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["promotion_state"], []).append(row)

    assert module.promotion_counts(grouped) == {
        "deprecated_cancelled": 3,
        "submitted_waiting_review": 2,
    }
    assert "stata_ssc" not in module.next_actions_by_registry(grouped)


def test_language_registry_external_gate_docs_explain_live_monitor_contract():
    text = _read(LANGUAGE_REGISTRY_GATES_DOC)

    assert "--promotion --live" in text
    assert "target-version evidence" in text
    assert "public_listing_version_unverified" in text
    assert "next_actions" in text
    assert "promotion_counts" in text
    assert "promotion_groups" in text
    assert "report.live" in text
    assert "report.generated_at_utc" in text
    assert ".github/workflows/language-registry-live.yml" in text
    assert "language-registry-live" in text
    assert "GitHub Actions job summary" in text
    assert "GITHUB_TOKEN" in text
    assert "promotion group counts" in text
    assert "submission detail" in text
    assert "public detail" in text
    assert "mergeability fields" in text
    assert "generated timestamp" in text
    assert "CRAN package page, CRANDB" in text
    assert "src/contrib/PACKAGES" in text
    assert "Anaconda `conda-forge/nwau-py` package API" in text
    assert "feedstock-only result" in text
    assert "vcpkg / ConanCenter live public probe" in text
    assert "deprecated and cancelled" in text
    assert "Boston College SSC/RePEc" in text
    assert "mchs.pkg" in text
    assert "mchs.ado" in text
    assert "mchs.sthlp" in text
    assert "promotion state" in text
    assert "next actions" in text
    assert "PR CI workflow writes non-live JSON artifacts only" in text
    assert "https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go" in text


def test_markdown_report_includes_promotion_next_actions():
    module = _report_module()
    rows = module.enrich_promotion_from_contract(
        module.external_gate_rows(json.loads(_read(CONTRACT)))
    )

    markdown = module.render_markdown(rows)

    assert "Promotion group counts:" in markdown
    assert "`deprecated_cancelled`: 3" in markdown
    assert "`submitted_waiting_review`: 2" in markdown
    assert "`approval_required_before_follow_up`" not in markdown
    assert "Next action" in markdown
    assert "wait for CRAN incoming/pretest or reviewer email" in markdown
    assert "feedstock publication" in markdown
    assert "explicit user approval" not in markdown
    assert "historical evidence only" in markdown


def test_live_markdown_report_includes_pr_mergeability_details():
    module = _report_module()
    rows = [
        {
            "id": "conda_forge",
            "registry": "conda-forge",
            "package": "nwau-py",
            "status": "submitted_checks_passed_pending_staged_recipes_review",
            "blocker": "review pending",
            "submission_url": "https://github.com/conda-forge/staged-recipes/pull/33452",
            "version": "0.2.2",
            "live_state": "submitted_open",
            "live_detail": (
                "https://github.com/conda-forge/staged-recipes/pull/33452 "
                "state=open merged=False draft=False mergeable=True "
                "mergeable_state=clean"
            ),
            "public_state": "public_listing_missing",
            "public_detail": (
                "https://api.anaconda.org/package/conda-forge/nwau-py HTTP 404"
            ),
            "promotion_state": "submitted_waiting_review",
            "next_action": "wait for feedstock publication",
            "track": "conda_forge_feedstock_submission_20260524",
        }
    ]

    markdown = module.render_markdown(rows, generated_at="2026-06-14T00:00:00Z")

    assert "Generated at (UTC): `2026-06-14T00:00:00Z`." in markdown
    assert "Submission detail" in markdown
    assert "Public detail" in markdown
    assert "mergeable=True" in markdown
    assert "mergeable_state=clean" in markdown
    assert "https://api.anaconda.org/package/conda-forge/nwau-py HTTP 404" in markdown


def test_external_submission_runbook_matches_current_go_and_swift_states():
    text = _read(EXTERNAL_SUBMISSION_RUNBOOK)

    assert (
        "Swift Package Index, Open VSX, Visual Studio Marketplace, and "
        "vcpkg/ConanCenter are deprecated and cancelled"
    ) in text
    assert "Maven Central" in text
    assert "io.github.edithatogo:mchs-jvm-bindings:0.1.0" in text
    assert (
        "Visual Studio Marketplace: `edithatogo.mchs-tools@0.1.1` "
        "historical evidence retained"
    ) in text
    assert (
        "Open VSX: `edithatogo.mchs-tools@0.1.0` remains available; "
        "latest is `0.1.1`; surface deprecated and cancelled"
        in text
    )
    assert "Swift Package Index: `MCHSBind@0.1.0` historical evidence retained" in text
    assert "GitHub Actions job summary" in text
    assert (
        "including the generated timestamp, promotion group counts, submission "
        "detail, public detail, promotion state, and next action"
    ) in text
    assert "submission detail includes live mergeability fields" in text
    assert "GitHub PR and feedstock probes avoid anonymous rate limits" in text
    assert "CRAN public-proof note" in text
    assert "CRAN package page, CRANDB" in text
    assert "src/contrib/PACKAGES" in text
    assert "conda-forge public-proof note" in text
    assert "feedstock creation alone is not treated as publication" in text
    assert "vcpkg / ConanCenter public-proof note" in text
    assert (
        "historical local packaging, vcpkg pr, and conancenter pr evidence"
        in text.lower()
    )
    assert "Stata SSC public-proof note" in text
    assert "mchs.pkg" in text
    assert "Go module proxy/pkg.go.dev" in text
    assert "Remaining step: none. Version `0.1.0` was verified" in text
    assert (
        "PackageList issue: "
        "`https://github.com/SwiftPackageIndex/PackageList/issues/13717`, "
        "closed as completed" in text
    )
    assert "Publication evidence: on 2026-06-12" in text
    assert "stable `v0.1.0`" in text
    assert "Cancellation state: deprecated and cancelled on 2026-07-03" in text
    assert "wait for or retrigger `pkg.go.dev` page indexing" not in text
    assert "Swift Package Index review/indexing" not in text


def test_external_only_runbook_has_exact_next_action_checklists():
    runbook = _read(EXTERNAL_SUBMISSION_RUNBOOK)
    gates = _read(LANGUAGE_REGISTRY_GATES_DOC)

    required_runbook_fragments = [
        "Wait for CRAN incoming/pretest or reviewer email",
        "Verify `https://cran.r-project.org/package=nwauR` and record version `0.1.0`",
        (
            "Namespace verification: on 2026-06-12, Sonatype Central Portal "
            "shows `io.github.edithatogo` as Verified"
        ),
        "Central validation passed after propagation",
        (
            "`https://repo1.maven.org/maven2/io/github/edithatogo/"
            "mchs-jvm-bindings/maven-metadata.xml` returns HTTP 200 and "
            "exposes latest/release/version `0.1.0`"
        ),
        (
            "Feedback addressed: pushed commit "
            "`e6ff7985c94b78471457e446e8fe3abfbe61fa41`"
        ),
        (
            "the PR was later refreshed to head "
            "`bffc5bf1a85389dc695adfd96c87bf2413f4db25`"
        ),
        (
            "Open VSX publish check: `npx --yes ovsx publish "
            "integrations/vscode/mchs-tools-0.1.0.vsix --pat [REDACTED]` "
            "returned that version `0.1.0` is already published."
        ),
        "`MCHS Tools` version `0.1.1` as Public",
        (
            "Visual Studio Marketplace Gallery `extensionquery` returns public "
            "`edithatogo.mchs-tools` version `0.1.1`"
        ),
        "1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad",
        "bfbeca13497f21489c532e58af3b1e10df9fe60ae5eab4c721e632baee9b5dd6",
        (
            "corrected local SHA-256 is "
            "`d78cc11a9ab23080b38604e21c5d21ba9c8801ae0cf6219888f1797834cf2336`"
        ),
        "No corrected replacement publication is claimed.",
        "Public evidence: on 2026-06-14",
        "mchs.pkg` was live and listed the MCHS module",
        "Remaining step: none for SSC publication",
        "Treat vcpkg / ConanCenter as deprecated and cancelled",
        "Retain PRs and local packaging evidence as historical evidence only",
        "Do not wait for ConanCenter review",
    ]
    for fragment in required_runbook_fragments:
        assert fragment in runbook

    required_gate_fragments = [
        "Next actions: record incoming/pretest evidence",
        (
            "Maven Central | `io.github.edithatogo:mchs-jvm-bindings` | "
            "Published and verified on repo1.maven.org"
        ),
        (
            "Open VSX API `https://open-vsx.org/api/edithatogo/mchs-tools` "
            "returns namespace `edithatogo`"
        ),
        "Marketplace-sync artifact `integrations/vscode/mchs-tools-0.1.1.vsix`",
        (
            "Visual Studio Marketplace is published and public as "
            "`edithatogo.mchs-tools` version `0.1.1`"
        ),
        "deprecated and cancelled on 2026-07-03",
        (
            "Published and verified at `https://www.mathworks.com/"
            "matlabcentral/fileexchange/184067-mchs-matlab-interop`"
        ),
        (
            "SSC / Stata package distribution | `mchs-stata-interop` | "
            "Published and verified"
        ),
        "no further upstream review, publication, or monitoring work is planned",
    ]
    for fragment in required_gate_fragments:
        assert fragment in gates

    vague_runbook_phrases = [
        "Submit through CRAN maintainer upload/review workflow.",
        (
            "Create a track-local upstream PR checklist with the vcpkg "
            "version update and ConanCenter `conandata.yml` requirements."
        ),
        "Required step: MathWorks account upload and File Exchange review.",
        "Required step: SSC maintainer submission/review.",
        "Required submission steps:",
        "Current blocker: no vcpkg/Conan PR opened",
    ]
    for phrase in vague_runbook_phrases:
        assert phrase not in runbook
