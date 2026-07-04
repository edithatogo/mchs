#!/usr/bin/env python
"""Run the conservative MIMIC-IV Demo worked example."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from nwau_py.public_clinical_datasets import run_mimic_demo_worked_example


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_output_dir() -> Path:
    return _repo_root() / ".cache" / "mchs" / "mimic-demo-worked-example"


def build_parser() -> argparse.ArgumentParser:
    """Build the example runner argument parser."""
    root = _repo_root()
    fixture_dir = Path(__file__).resolve().parent / "fixtures"
    parser = argparse.ArgumentParser(
        description=(
            "Stage MIMIC-IV Demo-shaped data, apply an explicitly synthetic "
            "Australian AR-DRG overlay, and run the acute calculator with "
            "fixture weights."
        )
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=fixture_dir,
        help=(
            "Directory containing MIMIC-IV Demo-shaped CSV files. Defaults to "
            "the committed synthetic fixtures."
        ),
    )
    parser.add_argument(
        "--synthetic-overlay",
        type=Path,
        default=fixture_dir / "synthetic_overlay.csv",
        help="Synthetic Australian AR-DRG overlay for documentation runs.",
    )
    parser.add_argument(
        "--local-ar-drg-overlay",
        type=Path,
        default=None,
        help=(
            "Optional local-only precomputed Australian AR-DRG overlay with "
            "episode_id, australian_ar_drg, and classification_provenance."
        ),
    )
    parser.add_argument(
        "--reference-weights",
        type=Path,
        default=root / "tests" / "data" / "nep25_aa_price_weights.csv",
        help="Fixture acute price weights used by the runnable tutorial.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_default_output_dir(),
        help="Directory for generated local outputs.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the example and print a JSON summary."""
    parser = build_parser()
    args = parser.parse_args(argv)
    bundle = run_mimic_demo_worked_example(
        args.input_dir,
        synthetic_overlay_path=args.synthetic_overlay,
        local_ar_drg_path=args.local_ar_drg_overlay,
        reference_weights_path=args.reference_weights,
        output_dir=args.output_dir,
    )
    summary = {
        "row_count": len(bundle.calculated),
        "outputs": dict(bundle.written_files),
        "support_status": dict(bundle.support_status_summary),
        "scenario_sensitivity_report": list(bundle.scenario_sensitivity_report),
        "classification_boundary": (
            "synthetic overlay output is runnable documentation only; "
            "authoritative Australian NWAU claims require local Australian "
            "AR-DRG provenance"
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
