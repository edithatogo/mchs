from __future__ import annotations

import argparse
import json
from pathlib import Path

from nwau_py.licensed_asset_registry import audit_restricted_asset_signatures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the repository for restricted licensed-asset signatures."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="repository root or working tree to audit",
    )
    args = parser.parse_args()

    report = audit_restricted_asset_signatures(args.root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

