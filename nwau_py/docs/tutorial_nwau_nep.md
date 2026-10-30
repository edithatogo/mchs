# Tutorial: Calculating Notional Funding from Activity Data

**Objective:** Load synthetic activity data, compute NWAU per record using the `nwau_py` calculator API, then multiply by the NEP to derive notional funding.

## Outline

### 1. Load synthetic activity data

Create a synthetic DataFrame with the columns required by the acute calculator.

### 2. Call `calculate_acute` to get NWAU per record

Pass the DataFrame and an `AcuteParams` instance to the calculator. The result gains an `NWAU25` column.

### 3. Multiply NWAU by NEP to get notional funding

Look up the NEP via `get_nep()` and compute a new `NotionalFunding` column.

### 4. Show stream-level summaries

Aggregate total episodes, NWAU, and notional funding across the synthetic dataset.

### 5. Important caveat

Notional funding (= NWAU × NEP) is **not actual hospital funding**. Real funding depends on jurisdiction activity-based pricing policies, block grants, cross-border arrangements, and other adjustments.

## Code Example

```python
import pandas as pd
import numpy as np
from nwau_py.calculators import calculate_acute, AcuteParams
from nwau_py.pricing_constants import get_nep

# ── 1. Synthetic acute activity data ──────────────────────────────────
np.random.seed(42)
n = 20
synthetic_acute = pd.DataFrame(
    {
        "DRG": np.random.choice(["E62A", "E62B", "F62A", "F62B", "G02A"], size=n),
        "LOS": np.random.randint(1, 15, size=n),
        "ICU_HOURS": np.random.choice([0, 0, 0, 0, 2, 4, 8], size=n),
        "ICU_OTHER": 0,
        "PAT_SAMEDAY_FLAG": np.random.choice([0, 1], size=n, p=[0.8, 0.2]),
        "PAT_PRIVATE_FLAG": np.random.choice([0, 1], size=n, p=[0.85, 0.15]),
    }
)

# ── 2. Calculate NWAU ────────────────────────────────────────────────
result = calculate_acute(synthetic_acute, AcuteParams())
nwau_col = "NWAU25"
print(f"NWAU column: {nwau_col}")
print(result[[nwau_col]].describe())

# ── 3. Calculate notional funding ────────────────────────────────────
nep = get_nep("2025")  # 7 434
result["NotionalFunding"] = result[nwau_col] * nep
result["NotionalFunding"] = result["NotionalFunding"].round(2)

# ── 4. Stream-level summary ──────────────────────────────────────────
summary = pd.DataFrame(
    {
        "Episodes": len(result),
        "Total NWAU": result[nwau_col].sum().round(4),
        "Mean NWAU": result[nwau_col].mean().round(4),
        "Total Notional Funding": result["NotionalFunding"].sum().round(2),
        "Mean Notional Funding": result["NotionalFunding"].mean().round(2),
    },
    index=["Acute"],
)

print("\n── Stream Summary ──")
print(summary.to_string(index=True))

# ── 5. Caveat ────────────────────────────────────────────────────────
print("\n⚠  Notional funding (NWAU × NEP) is a benchmark, not actual hospital funding.")
print(
    "   Real hospital funding depends on jurisdiction activity-based pricing policies,"
)
print(
    "   block grants, cross-border adjustments, and other "
    "jurisdiction-specific factors."
)
```

## Expected output outline

The summary table will show aggregate NWAU and notional funding for the synthetic cohort. Because `DRG` codes in the synthetic data may not match real price-weight tables, some rows may have `NWAU25 = 0` (unrecognised DRG) — this is expected and realistic for incomplete reference data.