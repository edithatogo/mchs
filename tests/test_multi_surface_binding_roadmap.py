from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _track(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor track or archive: {track_id}")


TRACK = _track("multi_surface_binding_delivery_20260510")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_multi_surface_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "binding-matrix.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
    ]:
        assert path.exists(), path


def test_binding_matrix_covers_required_language_surfaces():
    text = _read(TRACK / "binding-matrix.md")

    for phrase in [
        "Python",
        "R",
        "Julia",
        "C#",
        "Rust",
        "Go",
        "TypeScript",
        "implemented",
        "planned",
        "deferred",
        "advisory",
        "thin wrappers over the Rust core",
        "Rust/Python parity",
    ]:
        assert phrase in text


def test_binding_matrix_records_recommended_toolchains_and_boundaries():
    text = _read(TRACK / "binding-matrix.md")

    for phrase in [
        "PyO3 / maturin",
        "wasm-bindgen or wasm-pack",
        "extendr",
        "Julia `ccall`",
        "Stable ABI wrapper or service boundary",
        "C ABI or service boundary",
        "GitHub Pages remains synthetic/demo-only",
        "Power Platform remains orchestration-only",
        "Arrow-compatible table exchange",
    ]:
        assert phrase in text


def test_track_index_links_the_binding_matrix():
    text = _read(TRACK / "index.md")
    assert "[Binding Matrix](./binding-matrix.md)" in text
