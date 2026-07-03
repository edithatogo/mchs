"""Tests for the canonical scoring package layout."""

from __future__ import annotations

import inspect
from pathlib import Path

import nwau_py.scoring as scoring

ROOT = Path(__file__).resolve().parents[1]


def test_scoring_implementation_lives_in_the_root_package_tree() -> None:
    """The readmission scorer should be hosted in the canonical root package."""
    source_file = inspect.getsourcefile(scoring.score_readmission)
    assert source_file is not None
    source = Path(source_file).resolve()

    assert source == ROOT / "nwau_py" / "scoring" / "scorer.py"
    assert all("src" not in Path(path).parts for path in scoring.__path__)


def test_readme_points_to_the_root_scoring_module() -> None:
    """The repo README should not advertise the compatibility source tree."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "`nwau_py/scoring/scorer.py`" in readme
    assert "`src/nwau_py/scoring/scorer.py`" not in readme
