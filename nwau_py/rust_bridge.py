"""Helpers for loading the optional Rust-backed acute 2025 extension."""
# no-stub-enforce: abstract contract boundary helpers

from __future__ import annotations

import importlib
from collections.abc import Mapping
from importlib import machinery, util
from pathlib import Path
from types import ModuleType

RustKernelRow = Mapping[str, object]
RustKernelReference = Mapping[str, object]
RustKernelAdjustments = Mapping[str, object]
RustKernelResult = Mapping[str, object]


def _candidate_extension_paths() -> list[Path]:
    root = Path(__file__).resolve().parents[1]
    candidates: list[Path] = []
    for rel in (
        "rust/target/debug/deps",
        "rust/target/release/deps",
        "rust/target/debug",
        "rust/target/release",
    ):
        base = root / rel
        if not base.exists():
            continue
        candidates.extend(sorted(base.glob("libnwau_py_rust.*")))
        candidates.extend(sorted(base.glob("nwau_py_rust.*")))
    return [path for path in candidates if path.suffix in {".so", ".dylib", ".pyd"}]


def _load_from_path(path: Path) -> ModuleType:
    spec = util.spec_from_file_location(
        "nwau_py._rust",
        path,
        loader=machinery.ExtensionFileLoader("nwau_py._rust", str(path)),
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load Rust extension from {path}")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_installed_extension() -> ModuleType:
    """Import the installed Rust extension, if it exists."""
    return importlib.import_module("._rust", __package__)


def _load_module_if_available(path: Path) -> tuple[ModuleType | None, str | None]:
    try:
        return _load_from_path(path), None
    except Exception as exc:
        return None, f"{path}: {exc.__class__.__name__}: {exc}"


def load_rust_extension() -> ModuleType:
    """Load the optional Rust extension.

    The bridge is intentionally opt-in. It first tries the installed
    ``nwau_py._rust`` module. If that module is missing, it falls back to
    known on-disk build artifacts under ``rust/target``. Any other import
    failure from the installed module is surfaced immediately so callers can
    distinguish a missing extension from a broken build.
    """
    try:
        return _load_installed_extension()
    except ModuleNotFoundError as exc:
        if getattr(exc, "name", None) not in {"nwau_py._rust", "_rust"}:
            raise ImportError(
                "installed Rust extension import failed before nwau_py._rust could load"
            ) from exc
        installed_failure = f"installed module missing: {exc}"
    except Exception as exc:
        raise ImportError(
            "installed Rust extension import failed before nwau_py._rust could load"
        ) from exc

    candidate_failures: list[str] = [installed_failure]
    for candidate in _candidate_extension_paths():
        module, failure = _load_module_if_available(candidate)
        if module is not None:
            return module
        if failure is not None:
            candidate_failures.append(failure)

    message = [
        "Rust extension nwau_py._rust is not available.",
        "Fallback order:",
        "- installed module import",
        "- on-disk build artifacts under rust/target/debug and rust/target/release",
    ]
    if candidate_failures:
        message.append("Load diagnostics:")
        message.extend(f"- {failure}" for failure in candidate_failures)
    raise ImportError("\n".join(message))


def kernel_label() -> str:
    return load_rust_extension().kernel_label()


def _calculate_acute_2025_row_contract(
    row: RustKernelRow,
    reference: RustKernelReference,
    adjustments: RustKernelAdjustments,
    /,
) -> RustKernelResult:
    """Static single-row boundary for the Rust acute 2025 bridge."""
    # no-stub-enforce: intentional abstract contract boundary

    raise RuntimeError("contract helper is for static typing only")


def calculate_acute_2025_row(*args, **kwargs):
    """Run one acute 2025 row through the Rust kernel.

    This helper is a single-row boundary: batch wrappers should normalize one
    input row, one reference row, and one adjustment mapping per call. The Rust
    kernel itself stays scalar here so the opt-in bridge remains easy to audit
    and fall back from.
    """
    if kwargs:
        raise TypeError("calculate_acute_2025_row accepts positional arguments only")
    if len(args) != 3:
        raise TypeError(
            "calculate_acute_2025_row expects row, reference, and adjustments"
        )

    row, reference, adjustments = args
    ext = load_rust_extension()
    return ext.calculate_acute_2025_row(
        str(row["DRG"]),
        float(row["LOS"]),
        float(row.get("ICU_HOURS", 0.0)),
        float(row.get("ICU_OTHER", 0.0)),
        bool(int(row.get("PAT_SAMEDAY_FLAG", 0))),
        bool(int(row.get("PAT_PRIVATE_FLAG", 0))),
        bool(int(row.get("PAT_COVID_FLAG", 0))),
        bool(int(row.get("EST_ELIGIBLE_PAED_FLAG", row.get("eligible_paed_flag", 0)))),
        float(reference.get("inlier_lower_bound", 0.0)),
        float(reference.get("inlier_upper_bound", 0.0)),
        float(reference.get("paediatric_multiplier", 1.0)),
        bool(int(reference.get("same_day_list_flag", 0))),
        bool(int(reference.get("bundled_icu_flag", 0))),
        float(reference.get("same_day_base_weight", 0.0)),
        float(reference.get("same_day_per_diem", 0.0)),
        float(reference.get("inlier_weight", 0.0)),
        float(reference.get("long_stay_per_diem", 0.0)),
        float(reference.get("private_service_adjustment", 0.0)),
        float(adjustments.get("icu_rate", 0.0)),
        float(adjustments.get("covid_adjustment", 0.0)),
        float(adjustments.get("indigenous_adjustment", 0.0)),
        float(adjustments.get("remoteness_adjustment", 0.0)),
        float(adjustments.get("treatment_remoteness_adjustment", 0.0)),
        float(adjustments.get("radiotherapy_adjustment", 0.0)),
        float(adjustments.get("dialysis_adjustment", 0.0)),
        float(adjustments.get("private_accommodation_same_day", 0.0)),
        float(adjustments.get("private_accommodation_overnight", 0.0)),
    )
