"""Generate packaged price values from canonical reference manifests."""

import json
from pathlib import Path

import yaml


def generated_prices(root: Path) -> str:
    """Serialize published NEP values and their source locators deterministically."""
    prices = {}
    for year in ("2025", "2026"):
        path = root / "reference-data" / year / "manifest.yaml"
        manifest = yaml.safe_load(path.read_text())
        nep = manifest["constants"]["nep"]
        if not isinstance(nep["value"], int) or nep["value"] <= 0:
            raise ValueError(f"Invalid NEP in {path}")
        prices[year] = {"value": nep["value"], "source_url": nep["source_url"]}
    return json.dumps(prices, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root / "nwau_py/data/pricing_constants.json").write_text(generated_prices(root))
