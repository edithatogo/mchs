from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"
TRACK_ROOT = ROOT / "conductor" / "tracks"
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
    return json.loads(_read(TRACK_ROOT / track_id / "metadata.json"))


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
    return HTTPError(
        url,
        code,
        "test error",
        headers or {},
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
        "python_pypi",
        "rust_crates_io",
        "typescript_npm",
    }
    assert all(item["blocker"] is None for item in published)
    assert all(item["submission_url"] for item in published)


def test_remaining_prepared_registry_tracks_are_blocked_without_publication_claims():
    tracks = _read(TRACKS)
    expected = {
        "vscode_openvsx": (
            "vscode_openvsx_registry_submission_20260524",
            "prepared_eclipse_github_linked_pending_eclipse_agreement_login_tokens_and_vsix_publish",
            "Publisher Agreement",
            "VS Code/Open VSX Extension Submission",
        ),
        "matlab_file_exchange": (
            "matlab_file_exchange_submission_20260524",
            "prepared_pending_file_exchange_upload_review",
            "MathWorks account/session",
            "MATLAB File Exchange Submission",
        ),
    }

    for registry_id, (
        track_id,
        current_status,
        blocker_text,
        title,
    ) in expected.items():
        metadata = _metadata(track_id)
        registry = _registry(registry_id)
        assert metadata["status"] == "blocked"
        assert metadata["current_status"] == current_status
        assert metadata["local_readiness_resolved"] is True
        assert metadata["publication_claimed"] is False
        assert metadata["publication_status"] == "not_published"
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
        registry["submissionEvidence"]["uuid"]
        == "58dad789-f56a-4ab3-a66f-c15139bf9cbe"
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
            metadata["local_readiness_resolved"]
            == registry["localReadinessResolved"]
        )
        if registry["current_status"] == "published_verified":
            assert metadata["status"] == "completed"
            assert registry["blocker"] is None
            assert metadata["publication_claimed"] is True
            assert f"- [x] **Track: {registry['title']}**" in tracks_md
        else:
            assert registry["blocker"]
            assert (
                metadata["status"] in {"blocked", "submitted"}
                or metadata["status"].startswith("submitted_")
            )
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
        }

    monkeypatch.setattr(module, "fetch_json", fake_fetch_json)
    live = module.live_submission_state(
        "https://github.com/conda-forge/staged-recipes/pull/33452"
    )
    assert live["live_state"] == "submitted_open"
    assert "merged=False" in live["live_detail"]

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
    assert (
        module.public_probe_url(by_id["jvm_maven_central"])
        == "https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml"
    )
    assert (
        module.public_probe_url(go_registry)
        == "https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go"
    )
    assert (
        module.public_probe_url(homebrew_registry)
        == "https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb"
    )
    assert (
        module.public_probe_url(by_id["vscode_openvsx"])
        == "https://open-vsx.org/api/edithatogo/mchs-tools"
    )
    assert module.public_probe_url(by_id["matlab_file_exchange"]) is None

    assert module.request_headers_for_url(
        "https://open-vsx.org/api/edithatogo/mchs-tools"
    )["Accept"] == "application/json"
    assert module.request_headers_for_url(
        "https://api.github.com/repos/conda-forge/staged-recipes/pulls/33452"
    )["Accept"] == "application/vnd.github+json"

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
            raise module.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
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
                'sha256 "6f987bc4a81f3ac78cbc893d6a502fc572a534905f9f1f89cfc05600ff4ddff3"\n'
            )
        raise AssertionError(f"unexpected text fetch: {url}")

    def fake_json_post(url: str, payload: dict, timeout: int = 20) -> dict:
        if "marketplace.visualstudio.com" in url:
            criteria = payload["filters"][0]["criteria"][0]
            assert criteria["filterType"] == 7
            assert criteria["value"] == "edithatogo.mchs-tools"
            return {"results": [{"extensions": []}]}
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
        module.live_public_package_state(by_id["swift_package_index"])["public_state"]
        == "public_listing_missing"
    )
    assert (
        module.live_public_package_state(by_id["vscode_openvsx"])["public_state"]
        == "public_listing_missing"
    )
    assert (
        module.live_public_package_state(by_id["matlab_file_exchange"])["public_state"]
        == "manual_check_required"
    )


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

    monkeypatch.setattr(
        module,
        "fetch_text",
        lambda url, timeout=20: "pkg page includes v0.1.0 release",
    )

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
    deferred_conda_row = conda_row | {"live_state": "check_deferred_rate_limited"}
    assert (
        module.promotion_state(deferred_conda_row)["promotion_state"]
        == "submitted_waiting_review"
    )

    julia_row = {
        "id": "julia_general",
        "status": "published_verified",
        "public_state": "public_listing_available",
        "live_state": "submitted_open",
        "blocker": None,
    }
    assert (
        module.promotion_state(julia_row)["promotion_state"]
        == "completion_candidate"
    )

    merged_conda_row = conda_row | {"public_state": "public_listing_available"}
    assert (
        module.promotion_state(merged_conda_row)["promotion_state"]
        == "completion_candidate"
    )

    closed_issue_row = {
        "id": "swift_package_index",
        "status": "submitted_accepted_pending_spi_public_probe",
        "public_state": "public_listing_missing",
        "live_state": "submitted_issue_completed",
        "blocker": "Swift Package Index issue closed without public listing.",
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
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["promotion_state"]] = counts.get(row["promotion_state"], 0) + 1

    assert counts == {
        "external_gate_blocked": 3,
        "publication_needs_follow_up": 1,
        "submitted_waiting_review": 4,
    }


def test_language_registry_external_gate_docs_explain_live_monitor_contract():
    text = _read(LANGUAGE_REGISTRY_GATES_DOC)

    assert "--promotion --live" in text
    assert "target-version evidence" in text
    assert "public_listing_version_unverified" in text
    assert ".github/workflows/language-registry-live.yml" in text
    assert "language-registry-live" in text
    assert "PR CI workflow writes non-live JSON artifacts only" in text
    assert "https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go" in text


def test_external_submission_runbook_matches_current_go_and_swift_states():
    text = _read(EXTERNAL_SUBMISSION_RUNBOOK)

    assert (
        "PyPI, npm, crates.io, NuGet, the Homebrew personal tap, and the Go "
        "module are externally published and verified"
    ) in text
    assert "Go module proxy/pkg.go.dev" in text
    assert "Remaining step: none. Version `0.1.0` was verified" in text
    assert (
        "PackageList issue: "
        "`https://github.com/SwiftPackageIndex/PackageList/issues/13717`, "
        "closed as completed" in text
    )
    assert "verify public SPI listing/version evidence" in text
    assert "wait for or retrigger `pkg.go.dev` page indexing" not in text
    assert "Swift Package Index review/indexing" not in text


def test_external_only_runbook_has_exact_next_action_checklists():
    runbook = _read(EXTERNAL_SUBMISSION_RUNBOOK)
    gates = _read(LANGUAGE_REGISTRY_GATES_DOC)

    required_runbook_fragments = [
        "Wait for CRAN incoming/pretest or reviewer email",
        "Verify `https://cran.r-project.org/package=nwauR` and record version `0.1.0`",
        "Namespace verification: on 2026-06-12, Sonatype Central Portal shows `io.github.edithatogo` as Verified",
        "Wait for Central to discover public key `BB03C82343A653EE44BD5CDA9DF6B142F065199E`",
        "Verify `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml` contains version `0.1.0`",
        "Complete the Eclipse Foundation password login/agreement-recognition flow for account `edithatogo`",
        "Run `npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat \"$OVSX_PAT\"`",
        "Run `npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat \"$VSCE_PAT\"`",
        "Upload `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`",
        "Copy the description, license, tags, and version from `bindings/matlab/file-exchange-submission.json`",
        "Email the SSC package submission contact with package name `mchs-stata-interop`, version `0.1.0`",
        "Include `bindings/stata/pkg-mchs.pkg` as the package index file",
        "Treat vcpkg as upstream-policy deferred",
        "Complete the ConanCenter CLA/recheck gate",
        "Wait for ConanCenter job scheduler and maintainer review",
        "Verify the merged ConanCenter package page before changing the Conan side of the gate to complete",
    ]
    for fragment in required_runbook_fragments:
        assert fragment in runbook

    required_gate_fragments = [
        "Next actions: record incoming/pretest evidence",
        "Next actions: wait for supported keyserver propagation or publish the key through another supported path",
        "Next actions: complete the Eclipse password login/agreement-recognition flow",
        "Next actions: sign in to MathWorks File Exchange",
        "Next actions: wait for SSC maintainer response",
        "vcpkg is upstream-policy deferred",
        "ConanCenter remains active: complete CLA/recheck",
    ]
    for fragment in required_gate_fragments:
        assert fragment in gates

    vague_runbook_phrases = [
        "Submit through CRAN maintainer upload/review workflow.",
        "Create a track-local upstream PR checklist with the vcpkg version update and ConanCenter `conandata.yml` requirements.",
        "Required step: MathWorks account upload and File Exchange review.",
        "Required step: SSC maintainer submission/review.",
        "Required submission steps:",
        "Current blocker: no vcpkg/Conan PR opened",
    ]
    for phrase in vague_runbook_phrases:
        assert phrase not in runbook
