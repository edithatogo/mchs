"""Phase 2-4 Rust promotion gate evidence.

These tests keep the Rust continuation baseline conservative. They do not
assert missing stream parity as a failing test because Phase 2 is documenting
the next red gate before production Rust/Python implementation changes. The
Phase 3/4 checks below also record Python-side exposure: a blocked Rust stream
or extension listing is not treated as default Rust calculator support until
the Python bridge has an explicit entrypoint and source-backed parity fixture.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = PROJECT_ROOT / "tests" / "fixtures" / "golden"


@dataclass(frozen=True)
class RustPromotionGate:
    stream: str
    python_calculator: str
    rust_entrypoint: str | None
    fixture_id: str | None
    status: str
    python_exposure: str
    next_gate: str


PHASE2_PROMOTION_GATES: tuple[RustPromotionGate, ...] = (
    RustPromotionGate(
        stream="acute",
        python_calculator="nwau_py.calculators.acute.calculate_acute",
        rust_entrypoint="nwau_py.calculators.acute.calculate_acute_rust_2025",
        fixture_id="acute_2025",
        status="canary",
        python_exposure="explicit-opt-in",
        next_gate="broaden fixtures beyond the synthetic acute 2025 three-row pack",
    ),
    RustPromotionGate(
        stream="emergency",
        python_calculator="nwau_py.calculators.ed.calculate_ed",
        rust_entrypoint=None,
        fixture_id=None,
        status="blocked",
        python_exposure="none",
        next_gate="add source-backed AECC or UDG fixture before writing Rust ED parity",
    ),
    RustPromotionGate(
        stream="sub-acute",
        python_calculator="nwau_py.calculators.subacute.calculate_subacute",
        rust_entrypoint=None,
        fixture_id=None,
        status="opt-in-blocked",
        python_exposure="blocked-no-rust-entrypoint",
        next_gate=(
            "do not expose Python Rust subacute parity until the blocked stream "
            "has a source-backed fixture and non-placeholder output"
        ),
    ),
    RustPromotionGate(
        stream="community-mental-health",
        python_calculator="nwau_py.calculators.community_mh_calculator.calculate_community_mh",
        rust_entrypoint=None,
        fixture_id=None,
        status="blocked",
        python_exposure="none",
        next_gate="add a trusted Python/source fixture before Rust promotion",
    ),
)


def _resolve_dotted_name(dotted_name: str) -> object:
    module_name, attr_name = dotted_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def test_phase2_matrix_names_exactly_one_rust_canary_stream():
    canary_streams = [
        gate.stream for gate in PHASE2_PROMOTION_GATES if gate.status == "canary"
    ]

    assert canary_streams == ["acute"]


def test_phase2_canary_stream_has_fixture_and_rust_entrypoint():
    gate = next(g for g in PHASE2_PROMOTION_GATES if g.stream == "acute")

    assert gate.fixture_id is not None
    assert (GOLDEN_DIR / gate.fixture_id / "manifest.json").is_file()
    assert callable(_resolve_dotted_name(gate.python_calculator))
    assert gate.rust_entrypoint is not None
    assert callable(_resolve_dotted_name(gate.rust_entrypoint))


def test_phase2_blocked_streams_are_documented_without_false_rust_entrypoints():
    blocked = [
        gate
        for gate in PHASE2_PROMOTION_GATES
        if gate.status in {"blocked", "opt-in-blocked"}
    ]

    assert {gate.stream for gate in blocked} == {
        "community-mental-health",
        "emergency",
        "sub-acute",
    }
    for gate in blocked:
        assert callable(_resolve_dotted_name(gate.python_calculator))
        assert gate.rust_entrypoint is None
        assert gate.fixture_id is None
        assert gate.python_exposure in {"none", "blocked-no-rust-entrypoint"}
        assert gate.next_gate


def test_phase2_does_not_claim_unbacked_golden_fixtures():
    fixture_ids = {path.parent.name for path in GOLDEN_DIR.glob("*/manifest.json")}
    claimed_fixture_ids = {
        gate.fixture_id
        for gate in PHASE2_PROMOTION_GATES
        if gate.fixture_id is not None
    }

    assert claimed_fixture_ids <= fixture_ids
    assert claimed_fixture_ids == {"acute_2025"}


def test_phase3_subacute_placeholder_is_not_python_rust_support():
    gate = next(g for g in PHASE2_PROMOTION_GATES if g.stream == "sub-acute")

    assert gate.status == "opt-in-blocked"
    assert gate.python_exposure == "blocked-no-rust-entrypoint"
    assert callable(_resolve_dotted_name(gate.python_calculator))
    assert gate.rust_entrypoint is None

    calculators_module = importlib.import_module("nwau_py.calculators")
    subacute_module = importlib.import_module("nwau_py.calculators.subacute")

    assert "calculate_subacute" in calculators_module.__all__
    assert "calculate_subacute_rust" not in calculators_module.__all__
    assert not hasattr(subacute_module, "calculate_subacute_rust")
    assert not hasattr(subacute_module, "calculate_subacute_rust_2025")


def test_phase4_default_python_rust_surface_remains_acute_only():
    exposed_rust_entrypoints = {
        gate.stream: gate.rust_entrypoint
        for gate in PHASE2_PROMOTION_GATES
        if gate.rust_entrypoint is not None
    }

    assert exposed_rust_entrypoints == {
        "acute": "nwau_py.calculators.acute.calculate_acute_rust_2025",
    }
    assert {
        gate.stream
        for gate in PHASE2_PROMOTION_GATES
        if gate.python_exposure == "explicit-opt-in"
    } == {"acute"}
