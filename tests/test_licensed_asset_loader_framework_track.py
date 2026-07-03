from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from click.testing import CliRunner

from nwau_py import licensed_asset_registry as lar
from nwau_py.cli.main import cli

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "nwau_py" / "docs" / "licensed_assets.md"
README = ROOT / "nwau_py" / "README.md"
GUARD_SCRIPT = ROOT / "scripts" / "validate_licensed_assets.py"


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_licensed_asset_manifest_path_is_local_only_and_ignored() -> None:
    path = lar.licensed_asset_manifest_path()

    assert path.as_posix() == "archive/ihacpa/raw/licensed-assets.manifest.json"
    assert lar.is_local_only_licensed_asset_path(path)
    assert lar.is_commit_safe_licensed_asset_path(path)


def test_register_validate_doctor_and_audit_commands_work(tmp_path: Path) -> None:
    manifest_path = (
        tmp_path / "archive" / "ihacpa" / "raw" / "licensed-assets.manifest.json"
    )
    runner = CliRunner()

    register = runner.invoke(
        cast(Any, cli),
        [
            "licensed-assets",
            "register",
            "--manifest",
            str(manifest_path),
            "--system",
            "ICD-10-AM",
            "--year",
            "2026",
            "--local-path-hint",
            "archive/ihacpa/raw/2026/licensed/icd_10_am",
            "--source-ref",
            "https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27",
            "--acknowledge-license",
        ],
    )
    assert register.exit_code == 0, register.output

    manifest = _read_json(manifest_path)
    assert manifest["schema_version"] == "1.0"
    assert manifest["license_acknowledgement"]["acknowledged"] is True
    assert manifest["assets"][0]["restricted"] is True
    assert manifest["assets"][0]["local_path_hint"] == (
        "archive/ihacpa/raw/2026/licensed/icd_10_am"
    )

    validate = runner.invoke(
        cast(Any, cli),
        [
            "licensed-assets",
            "validate",
            "--manifest",
            str(manifest_path),
            "--existing-path",
            "archive/ihacpa/raw/2026/licensed/icd_10_am",
        ],
    )
    assert validate.exit_code == 0, validate.output
    validated = json.loads(validate.output)
    assert validated["status"] == "validated"
    assert validated["support_status"] == "executable"

    doctor = runner.invoke(
        cast(Any, cli),
        [
            "licensed-assets",
            "doctor",
            "--manifest",
            str(manifest_path),
        ],
    )
    assert doctor.exit_code == 0, doctor.output
    report = json.loads(doctor.output)
    assert report["support_status"] == "blocked_licensed"
    assert report["missing_assets"]


def test_licensed_asset_audit_rejects_restricted_signatures(tmp_path: Path) -> None:
    restricted = tmp_path / "licensed-price-weights.xlsx"
    restricted.write_bytes(b"PK\x03\x04 synthetic restricted workbook")

    report = lar.audit_restricted_asset_signatures(tmp_path)

    assert report["status"] == "blocked"
    assert report["findings"]
    assert report["findings"][0]["signature"] == "licensed-office-workbook"

    runner = CliRunner()
    result = runner.invoke(
        cast(Any, cli),
        [
            "licensed-assets",
            "audit",
            "--root",
            str(tmp_path),
        ],
    )
    assert result.exit_code != 0
    assert "licensed-office-workbook" in result.output


def test_licensed_asset_docs_and_guard_script_are_present() -> None:
    assert DOC.exists(), DOC
    assert README.exists(), README
    assert GUARD_SCRIPT.exists(), GUARD_SCRIPT

    doc = DOC.read_text(encoding="utf-8").lower()
    readme = README.read_text(encoding="utf-8").lower()

    for phrase in [
        "local-only",
        "register",
        "validate",
        "doctor",
        "audit",
        "blocked_licensed",
    ]:
        assert phrase in doc

    assert "licensed-assets" in readme
