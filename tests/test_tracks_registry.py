from __future__ import annotations

from pathlib import Path

TRACKS = Path(__file__).resolve().parents[1] / "conductor" / "tracks.md"


def test_tracks_registry_orders_the_focused_tracks():
    text = TRACKS.read_text(encoding="utf-8")
    expected = [
        "Source Archive and Provenance Registry",
        "Cross-Language Golden Test Suite",
        "Python Tooling and CI Modernization",
        "Calculator Core Abstraction and Validation Models",
        "Public Calculator API Contract",
        "Arrow and Polars Data Bundle Migration",
        "GitHub Pages Web App Prototype",
        "C# Calculation Engine and Power Platform Adapter",
        "Release and Supply-Chain Governance",
        "Starlight Documentation Site and Versioning",
        "Ecosystem Standards and Language Readiness",
        "Rust Core Architecture and Calculator Abstraction",
        "Rust Acute 2025 Proof of Concept with Python Bindings",
        "Multi-Surface Binding and Delivery Roadmap",
        "Rust CI, Pre-Commit, and Supply-Chain Hardening",
        "Documentation, Release, and Public Readiness",
        "Power Platform ALM App Setup and Delivery",
        "Power BI and Power Platform CLI Tooling",
        "IHACPA Source Archive Gap Closure and Restore Validation",
        "IHACPA Feature Incorporation and Calculator Coverage Roadmap",
    ]

    positions = [text.index(name) for name in expected]
    assert positions == sorted(positions)


def test_tracks_registry_records_dependency_and_gate_language():
    text = TRACKS.read_text(encoding="utf-8")
    for phrase in [
        "Gate: establish source acquisition, storage policy, and manifest provenance",
        "Depends on: source archive manifesting and known-good reference artifacts.",
        "Depends on: source archive provenance and validation fixture shape.",
        "Depends on: validation evidence and CI coverage",
        "Depends on: calculator core abstractions and golden fixtures.",
        "Depends on: calculator core abstractions and stable validation fixtures.",
        "Depends on: public API contract, validation fixtures, and governance rules",
        (
            "Depends on: public API contract, calculator core abstractions, "
            "and golden fixtures."
        ),
        "Depends on: CI, validation evidence, and contract stability.",
        (
            "Depends on: public calculator contracts, validation vocabulary, "
            "docs governance, and GitHub Pages delivery rules."
        ),
        (
            "Depends on: public calculator contracts, golden fixtures, release "
            "governance, Starlight documentation, and Power Platform boundary "
            "documentation."
        ),
        (
            "Gate: assess scientific software standards, language packaging "
            "maturity, C# and Power Platform implementation readiness"
        ),
        "Depends on: public calculator contracts, Arrow/Parquet bundle guidance",
        "Gate: define Rust as the intended future calculator core",
        "Depends on: Rust core architecture, acute 2025 golden fixtures",
        "Gate: implement the first Rust-backed acute 2025 canary",
        "Depends on: Rust core architecture, Rust/Python proof-of-concept results",
        (
            "Gate: define binding and delivery sequencing for Python, R, Julia, "
            "C#, Rust, Go, TypeScript/WASM, Streamlit, GitHub Pages, and Power Platform"
        ),
        "Depends on: Python tooling and CI modernization, release governance",
        "Gate: align branch triggers, pre-commit hooks, Rust quality gates",
        "Depends on: Rust core architecture, binding delivery roadmap",
        (
            "Gate: publish conservative docs for current versus intended "
            "Rust-backed behavior"
        ),
        "Gate: research current Microsoft Power Platform ALM guidance",
        "Power Platform CLI Tooling",
        "recover or explicitly gap-record the remaining Box-hosted SAS artifacts",
        "map archive families and helpers to executable surfaces",
    ]:
        assert phrase in text


def test_modernization_foundation_is_coordination_only():
    text = TRACKS.read_text(encoding="utf-8")

    assert "**Track: Modernization Foundation**" in text
    assert "*Coordination only.*" in text
    assert "Retained to preserve sequencing and governance context." in text
    assert "Do not duplicate work already owned by the focused tracks above." in text
