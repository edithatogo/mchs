from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "csharp_dotnet_binding_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
PACKAGING_MATRIX = ROOT / "docs" / "roadmaps" / "polyglot-packaging-release-matrix.md"
ARCHITECTURE_DOC = ROOT / "conductor" / "csharp-architecture.md"
PACKAGING_PLANS = ROOT / "conductor" / "downstream-packaging-plans.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "csharp_dotnet_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
PASS_EXAMPLE = FIXTURE_ROOT / "validation.pass.json"
FAIL_EXAMPLE = FIXTURE_ROOT / "validation.fail.json"
CONTRACT_ROOT = ROOT / "contracts" / "csharp-dotnet-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "csharp-dotnet-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "csharp-dotnet-binding.schema.json"
LIVE_PASS_EXAMPLE = CONTRACT_ROOT / "examples" / "validation.pass.json"
LIVE_FAIL_EXAMPLE = CONTRACT_ROOT / "examples" / "validation.fail.json"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _squash(text: str) -> str:
    return " ".join(text.split())


def test_csharp_dotnet_binding_track_metadata_docs_and_contract_bundle_are_safe():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS,
        PACKAGING_MATRIX,
        ARCHITECTURE_DOC,
        PACKAGING_PLANS,
        CONTRACT_BUNDLE,
        PASS_EXAMPLE,
        FAIL_EXAMPLE,
        LIVE_CONTRACT,
        LIVE_SCHEMA,
        LIVE_PASS_EXAMPLE,
        LIVE_FAIL_EXAMPLE,
        ROOT / "bindings" / "dotnet" / "DotNetBinding.csproj",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS)
    packaging_matrix = _read_text(PACKAGING_MATRIX)
    architecture_doc = _read_text(ARCHITECTURE_DOC)
    contract_bundle = _load_json(CONTRACT_BUNDLE)
    live_contract = _load_json(LIVE_CONTRACT)
    live_pass = _load_json(LIVE_PASS_EXAMPLE)
    live_fail = _load_json(LIVE_FAIL_EXAMPLE)

    assert metadata["track_id"] == "csharp_dotnet_binding_20260512"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "in-progress"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "dotnet-binding-roadmap-complete"
    assert metadata["primary_contract"] == (
        "contracts/csharp-dotnet-binding/csharp-dotnet-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert "C#/.NET binding" in str(metadata["description"])

    assert "Specification: C#/.NET Binding" in spec
    assert "Initial strategy: service boundary." in spec
    assert "Fallback: CLI / Arrow-file interop" in spec
    assert "C ABI / PInvoke remains a later option" in spec
    assert "No formula logic is implemented in C#." in spec
    assert "typed C# request/response models" in spec
    assert "shared golden fixtures and provenance diagnostics" in spec

    assert (
        "Compare C ABI/PInvoke, service boundary, and CLI/Arrow-file interop." in plan
    )
    assert "Preserve diagnostics and provenance metadata." in plan
    assert "shared-fixture tests" in plan
    assert "- [x] Task: Choose the .NET integration strategy" in plan
    assert "- [x] Task: Build a C# prototype and shared-fixture tests." in plan

    assert "Track csharp_dotnet_binding_20260512 Context" in index
    assert "C#/.NET Binding" in tracks
    assert "Gate: expose institutional .NET integration" in tracks

    assert "NuGet / C#" in packaging_matrix
    assert "`preview`" in packaging_matrix
    assert "Release when the .NET wrapper remains thin" in packaging_matrix
    assert "signed package publishing is repeatable" in packaging_matrix
    assert "downstream adapter or service integration target" in architecture_doc
    assert "formula logic" in architecture_doc
    assert "shared golden fixtures" in architecture_doc

    bundle = _as_mapping(contract_bundle)
    assert bundle["schema_version"] == "1.0"
    assert bundle["binding_id"] == "csharp_dotnet_binding_20260512"
    assert bundle["surface"] == "csharp-dotnet"
    assert bundle["initial_strategy"] == "service boundary"
    assert bundle["fallback_strategy"] == "cli-arrow-file interop"
    assert bundle["formula_logic_location"] == "rust core"
    assert bundle["nuget_status"] == "future-only"

    diagnostics = _as_mapping(bundle["diagnostics"])
    provenance = _as_mapping(bundle["provenance"])
    package = _as_mapping(bundle["package"])

    assert diagnostics["format"] == "json"
    assert diagnostics["includes"] == [
        "contract_id",
        "pricing_year",
        "fixture_id",
        "validation_status",
    ]
    assert provenance["checksum_algorithm"] == "sha256"
    assert provenance["preserve_fields"] == [
        "source_basis",
        "fixture_id",
        "notes",
    ]
    assert package["nuget"]["status"] == "future-only"
    assert package["nuget"]["release_gate"] == "contract and parity stable"
    assert live_contract["schema_version"] == "1.0"
    assert live_contract["bundle_type"] == "synthetic"
    assert live_contract["binding"]["language"] == "C#"
    assert live_contract["public_calculator_contract"]["alignment_mode"] == (
        "shape-aligned"
    )
    assert live_contract["nuget_readiness"]["status"] == "preview"
    assert {check["status"] for check in live_pass["checks"]} == {"pass"}
    assert "fail" in {check["status"] for check in live_fail["checks"]}

    pass_example = _load_json(PASS_EXAMPLE)
    fail_example = _load_json(FAIL_EXAMPLE)

    assert pass_example["result"] == "pass"
    assert pass_example["strategy"] == "service boundary"
    assert pass_example["fallback"] == "cli-arrow-file interop"
    assert _as_mapping(pass_example["diagnostics"])["format"] == "json"
    assert _as_mapping(pass_example["provenance"])["checksum_algorithm"] == "sha256"

    assert fail_example["result"] == "fail"
    assert "formula logic" in str(fail_example["reason"]).lower()
    assert "nuget" in str(fail_example["reason"]).lower()
    assert "overclaim" in str(fail_example["reason"]).lower()


def test_csharp_dotnet_binding_preserves_provenance_without_formula_logic():
    bundle = _load_json(CONTRACT_BUNDLE)
    pass_example = _load_json(PASS_EXAMPLE)
    fail_example = _load_json(FAIL_EXAMPLE)

    bundle_diagnostics = _as_mapping(bundle["diagnostics"])
    bundle_provenance = _as_mapping(bundle["provenance"])
    pass_diagnostics = _as_mapping(pass_example["diagnostics"])
    pass_provenance = _as_mapping(pass_example["provenance"])

    assert bundle_diagnostics["format"] == pass_diagnostics["format"] == "json"
    assert (
        bundle_provenance["checksum_algorithm"]
        == pass_provenance["checksum_algorithm"]
        == "sha256"
    )
    assert bundle_provenance["preserve_fields"] == pass_provenance["preserve_fields"]
    assert bundle["formula_logic_location"] == "rust core"
    assert pass_example["formula_logic_location"] == "rust core"
    assert "c#" not in str(bundle["formula_logic_location"]).lower()
    assert "c#" not in str(pass_example["formula_logic_location"]).lower()
    assert "overclaim" in str(fail_example["reason"]).lower()


def test_csharp_dotnet_binding_if_a_scaffold_exists_it_stays_thin_and_non_formula():
    candidate_roots = [
        ROOT / "csharp-dotnet-binding",
        ROOT / "dotnet-binding",
        ROOT / "csharp_binding",
        ROOT / "bindings" / "dotnet",
        ROOT / "src" / "CSharp",
        ROOT / "src" / "csharp",
    ]
    scaffold_root = next((path for path in candidate_roots if path.exists()), None)

    if scaffold_root is None:
        return

    observed = _squash(_read_text(ARCHITECTURE_DOC)).lower()
    assert "downstream adapter or service integration target" in observed
    assert "formula logic should live in the rust core rather than in c#" in observed
    assert "shared golden fixtures" in observed

    scaffold_text = _squash(
        " ".join(
            _read_text(path)
            for path in scaffold_root.rglob("*")
            if path.is_file()
            and "bin" not in path.parts
            and "obj" not in path.parts
            and path.suffix in {".md", ".txt", ".json", ".cs", ".csproj", ".sln"}
        )
    ).lower()

    assert "nuwau" not in scaffold_text
    assert "formula logic" not in scaffold_text or "not implemented" in scaffold_text
    assert "nuget" not in scaffold_text or "preview" in scaffold_text
