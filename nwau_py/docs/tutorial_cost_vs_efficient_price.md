# Tutorial: Comparing Observed Costs to Efficient Prices

**Objective:** Take synthetic activity data that includes an `ObservedCost` column, compute notional funding via NWAU × NEP, and compare the two to identify over- and under-priced episodes.

## Outline

### 1. Start with synthetic activity + cost data

Create a DataFrame with both the standard calculator columns and an `ObservedCost` column representing the recorded hospital cost per episode.

### 2. Calculate NWAU and notional funding

Use `calculate_acute()` to get `NWAU25`, then multiply by `get_nep("2025")` to produce `NotionalFunding`.

### 3. Compare column-wise: ObservedCost vs NWAU × NEP

Add a `FundingDiff` column (`ObservedCost - NotionalFunding`) and a `CostRatio` column.

### 4. Calculate cost ratio

**Cost Ratio = ObservedCost / (NWAU × NEP)**:
- **Ratio > 1** — observed cost exceeds the efficient price (service may be overpriced or inefficient)
- **Ratio < 1** — observed cost is below the efficient price (service may be efficient or under-coded)

### 5. Interpret results

Show a per-episode sample and an aggregate summary. Discuss what the cost ratio means at different levels (episode vs stream vs hospital).

### 6. Limitations

- Synthetic data does not reflect real cost distributions
- No risk adjustment is applied; real studies should adjust for case mix
- Jurisdictional variation in pricing and costing methodology is not captured
- AHPCS compliance is assumed but not verified in this toy example

## Code Example

```python
import pandas as pd
import numpy as np
from nwau_py.calculators import calculate_acute, AcuteParams
from nwau_py.pricing_constants import get_nep

# ── 1. Synthetic activity + cost data ────────────────────────────────
np.random.seed(1)
n = 30
synthetic = pd.DataFrame({
    "DRG": np.random.choice(["E62A", "E62B", "F62A", "F62B", "G02A"], size=n),
    "LOS": np.random.randint(1, 12, size=n),
    "ICU_HOURS": np.random.choice([0, 0, 0, 0, 2, 6], size=n),
    "ICU_OTHER": 0,
    "PAT_SAMEDAY_FLAG": 0,
    "PAT_PRIVATE_FLAG": 0,
})
# Create synthetic observed costs with some noise around a plausible rate
synthetic["ObservedCost"] = (
    synthetic["LOS"] * np.random.uniform(1200, 2200, size=n)
    + np.random.normal(0, 500, size=n)
).clip(500)

# ── 2. Calculate NWAU and notional funding ──────────────────────────
result = calculate_acute(synthetic, AcuteParams())
nep = get_nep("2025")  # 7258
nwau_col = "NWAU25"
result["NotionalFunding"] = (result[nwau_col] * nep).round(2)

# ── 3-4. Compare costs and compute ratio ────────────────────────────
result["FundingDiff"] = (result["ObservedCost"] - result["NotionalFunding"]).round(2)
result["CostRatio"] = (
    result["ObservedCost"] / result["NotionalFunding"].replace(0, np.nan)
).round(4)

# ── 5. Interpret ────────────────────────────────────────────────────
print("── Per-episode sample (first 8 rows) ──")
cols = ["DRG", "LOS", nwau_col, "ObservedCost", "NotionalFunding", "CostRatio"]
print(result[cols].head(8).to_string(index=False))

summary = pd.DataFrame({
    "Episodes": len(result),
    "Total Observed Cost": result["ObservedCost"].sum().round(2),
    "Total Notional Funding": result["NotionalFunding"].sum().round(2),
    "Aggregate Cost Ratio": (
        result["ObservedCost"].sum() / result["NotionalFunding"].sum()
    ).round(4),
    "Episodes Over-Priced (ratio>1)": (result["CostRatio"] > 1).sum(),
    "Episodes Under-Priced (ratio<1)": (result["CostRatio"] < 1).sum(),
}, index=["Acute"])

print("\n── Aggregate Summary ──")
print(summary.to_string(index=True))

# ── 6. Limitations ──────────────────────────────────────────────────
print("\n⚠  This is a synthetic example. Real costing studies must:")
print("   - Use validated, AHPCS-compliant observed costs")
print("   - Apply appropriate risk / case-mix adjustment")
print("   - Account for jurisdictional variation in pricing")
print("   - Consider that a single-episode cost ratio is noisy; "
      "aggregate ratios are more reliable")
```

## Interpreting the cost ratio

| Cost Ratio | Interpretation |
|-----------|---------------|
| **< 0.8** | Cost well below efficient price — may indicate high efficiency, or under-counting of costs |
| **0.8 – 1.2** | Cost near the efficient benchmark — typical range for well-priced services |
| **> 1.2** | Cost exceeds efficient price — may indicate inefficiency, complex case mix, or inadequate funding |

At the **episode level**, the cost ratio is noisy. Real analyses should aggregate to DRG, stream, or hospital level for reliable benchmarking.
