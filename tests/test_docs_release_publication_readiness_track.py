from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "docs_release_publication_readiness_20260510"
TRACKS = ROOT / "conductor" / "tracks.md"
DOCS_SITE = ROOT / "docs-site" / "src" / "content" / "docs"
GOVERNANCE = DOCS_SITE / "governance"
MIGRATION = DOCS_SITE / "migration"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase1_rust_core_architecture_and_migration_status_are_published():
    assert (TRACK / "metadata.json").exists()
    assert (TRACK / "review.md").exists()
    tracks = _read(TRACKS)
    assert "./archive/docs_release_publication_readiness_20260510/" in tracks
    assert "./tracks/docs_release_publication_readiness_20260510/" not in tracks

    architecture = GOVERNANCE / "rust-core-architecture.md"
    reference_generation = GOVERNANCE / "reference-generation.md"
    public_readiness = GOVERNANCE / "public-readiness.md"
    legacy_docs = MIGRATION / "legacy-docs.md"
    governance_index = GOVERNANCE / "index.mdx"

    assert architecture.exists()
    assert reference_generation.exists()
    assert public_readiness.exists()
    assert legacy_docs.exists()
    assert governance_index.exists()

    architecture_text = _read(architecture)
    reference_text = _read(reference_generation)
    public_readiness_text = _read(public_readiness)
    legacy_text = _read(legacy_docs)
    governance_index_text = _read(governance_index)

    assert "Rust is the intended future calculator core" in architecture_text
    assert "Python remains the current validated runtime path" in architecture_text
    assert "Arrow-compatible batch input and output" in architecture_text
    assert "public calculator contracts" in reference_text
    assert "Rust API docs" in reference_text
    assert "WASM or browser docs" in reference_text
    assert "Contributor Path" in public_readiness_text
    assert "Security Guidance" in public_readiness_text
    assert "Citation Guidance" in public_readiness_text
    assert "Rust migration status" in legacy_text
    assert "opt-in" in legacy_text
    assert "not the default runtime" in legacy_text
    assert "Rust core architecture" in governance_index_text
    assert "Reference generation" in governance_index_text
    assert "Public readiness" in governance_index_text


def test_phase2_generated_reference_and_contract_surfaces_are_documented():
    architecture = _read(GOVERNANCE / "rust-core-architecture.md")
    reference_generation = _read(GOVERNANCE / "reference-generation.md")
    public_readiness = _read(GOVERNANCE / "public-readiness.md")
    governance_index = _read(GOVERNANCE / "index.mdx")
    docs_index = _read(DOCS_SITE / "index.mdx")

    assert "generated reference strategy" in architecture
    assert "public contract surfaces" in architecture
    assert "Starlight" in architecture
    assert "public calculator contract" in architecture
    assert "Rust API docs" in architecture
    assert "Python docs" in architecture
    assert "WASM docs" in architecture
    assert "runtime-neutral schema surfaces" in reference_generation
    assert "validation record or fixture pack" in reference_generation
    assert "contributor" in public_readiness.lower()
    assert "de-identified" in public_readiness
    assert "fixture pack" in public_readiness
    assert "Rust core architecture" in governance_index
    assert "Reference generation" in governance_index
    assert "Public readiness" in governance_index
    assert "migration notes" in docs_index
