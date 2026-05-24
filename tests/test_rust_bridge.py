from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any, cast, get_type_hints

import pytest

from nwau_py import rust_bridge


def _raise_missing_rust_extension() -> None:
    exc = ModuleNotFoundError("No module named 'nwau_py._rust'")
    exc.name = "nwau_py._rust"
    raise exc


def test_load_rust_extension_uses_filesystem_fallback_when_installed_module_is_missing(
    monkeypatch,
):
    loaded_paths: list[Path] = []
    candidate_paths = [
        Path("/fake/rust/target/debug/deps/libnwau_py_rust.so"),
        Path("/fake/rust/target/release/deps/libnwau_py_rust.so"),
    ]
    expected_module = ModuleType("nwau_py._rust")
    cast(Any, expected_module).kernel_label = lambda: "acute 2025"

    monkeypatch.setattr(
        rust_bridge,
        "_load_installed_extension",
        _raise_missing_rust_extension,
    )
    monkeypatch.setattr(
        rust_bridge,
        "_candidate_extension_paths",
        lambda: candidate_paths,
    )

    def fake_loader(path: Path) -> tuple[ModuleType | None, str | None]:
        loaded_paths.append(path)
        if path == candidate_paths[0]:
            return None, f"{path}: OSError: bad ABI"
        return expected_module, None

    monkeypatch.setattr(rust_bridge, "_load_module_if_available", fake_loader)

    assert rust_bridge.load_rust_extension() is expected_module
    assert loaded_paths == candidate_paths


def test_load_rust_extension_surfaces_installed_import_failures(monkeypatch):
    def boom() -> ModuleType:
        raise RuntimeError("broken initializer")

    monkeypatch.setattr(rust_bridge, "_load_installed_extension", boom)
    monkeypatch.setattr(
        rust_bridge,
        "_candidate_extension_paths",
        lambda: pytest.fail(
            "filesystem fallback should not run for non-module import errors"
        ),
    )

    with pytest.raises(ImportError, match="installed Rust extension import failed"):
        rust_bridge.load_rust_extension()


def test_load_rust_extension_reports_candidate_diagnostics(monkeypatch):
    candidate_paths = [
        Path("/fake/rust/target/debug/deps/libnwau_py_rust.so"),
        Path("/fake/rust/target/release/deps/libnwau_py_rust.so"),
    ]

    monkeypatch.setattr(
        rust_bridge,
        "_load_installed_extension",
        _raise_missing_rust_extension,
    )
    monkeypatch.setattr(
        rust_bridge,
        "_candidate_extension_paths",
        lambda: candidate_paths,
    )
    monkeypatch.setattr(
        rust_bridge,
        "_load_module_if_available",
        lambda path: (None, f"{path}: ImportError: missing dependency"),
    )

    with pytest.raises(ImportError) as excinfo:
        rust_bridge.load_rust_extension()

    message = str(excinfo.value)
    assert "Rust extension nwau_py._rust is not available." in message
    assert "Fallback order:" in message
    assert str(candidate_paths[0]) in message
    assert str(candidate_paths[1]) in message


def test_rust_bridge_kernel_row_contract_is_scalar_and_positional_only():
    hints = get_type_hints(rust_bridge._calculate_acute_2025_row_contract)
    assert "single-row boundary" in (rust_bridge.calculate_acute_2025_row.__doc__ or "")
    assert hints["row"] == rust_bridge.RustKernelRow
    assert hints["reference"] == rust_bridge.RustKernelReference
    assert hints["adjustments"] == rust_bridge.RustKernelAdjustments
    assert hints["return"] == rust_bridge.RustKernelResult

    kwargs: dict[str, Any] = {"row": {}, "reference": {}, "adjustments": {}}
    with pytest.raises(TypeError, match="positional arguments"):
        rust_bridge.calculate_acute_2025_row(**kwargs)
