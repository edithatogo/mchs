"""Compatibility shim for the readmission scorer implementation.

The canonical implementation now lives in ``nwau_py/scoring/scorer.py`` at the
repository root. This shim keeps the historical ``src`` tree importable for any
local tooling that still points there.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_score_readmission():
    source = (
        Path(__file__).resolve().parents[3]
        / "nwau_py"
        / "scoring"
        / "scorer.py"
    )
    if not source.exists():
        raise ImportError(f"Unable to locate scorer implementation at {source}")
    spec = importlib.util.spec_from_file_location(
        "nwau_py.scoring._root_scorer", source
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load scorer implementation from {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.score_readmission


score_readmission = _load_score_readmission()

__all__ = ["score_readmission"]
