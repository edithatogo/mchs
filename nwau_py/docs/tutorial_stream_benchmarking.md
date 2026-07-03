# Tutorial: Stream-Level Benchmarking with NHCDC Context

**Objective:** Load synthetic multi-stream activity data, calculate NWAU for each stream, compute notional funding, and produce a comparison table alongside synthetic cost benchmarks — mirroring the structure of an NHCDC-informed costing study.

## Outline

### 1. Load synthetic multi-stream activity data

Create separate DataFrames for acute, ED, mental health, subacute, and outpatient activity. Each stream requires different input columns as specified by its calculator.

### 2. Calculate NWAU for each stream

Apply the appropriate calculator (`calculate_acute`, `calculate_ed`, `calculate_mh`, `calculate_subacute`, `calculate_outpatients`) with its respective params dataclass.

### 3. Calculate notional funding = NWAU × NEP

Multiply each stream's total NWAU by the NEP from `pricing_constants`. For simplicity, the same NEP is used across streams (in practice, NEC pricing applies to non-admitted and subacute streams).

### 4. Load synthetic cost benchmarks

Create a synthetic benchmark table that mimics what would come from NHCDC (observed average cost per episode by stream).

### 5. Create a comparison table

Stream | Episodes | Total NWAU | Notional Funding | Observed Cost | Cost Ratio

### 6. Explain NHCDC and AHPCS context

- NHCDC provides the national cost benchmarks used to derive NWAU price weights and the NEP/NEC
- AHPCS ensures consistent cost allocation methodology across hospitals
- Without AHPCS compliance, cost comparisons between hospitals are unreliable

## Code Example

```python
import pandas as pd
import numpy as np
from nwau_py.calculators import (
    calculate_acute, AcuteParams,
    calculate_ed,     EDParams,
    calculate_mh,     MHParams,
    calculate_subacute, SubacuteParams,
    calculate_outpatients, OutpatientParams,
)
from nwau_py.pricing_constants import get_nep

# ── 1. Synthetic activity data for each stream ───────────────────────
np.random.seed(2025)

# Acute
acute_df = pd.DataFrame({
    "DRG": np.random.choice(["E62A", "E62B", "F62A", "F62B", "G02A"], size=50),
    "LOS": np.random.randint(1, 10, size=50),
    "ICU_HOURS": 0, "ICU_OTHER": 0,
    "PAT_SAMEDAY_FLAG": 0, "PAT_PRIVATE_FLAG": 0,
})

# ED
ed_df = pd.DataFrame({
    "AECC": np.random.choice(["AECC01", "AECC02", "AECC03", "AECC04"], size=80),
    "COMPENSABLE_STATUS": 2, "DVA_STATUS": 2,
})

# Mental health
mh_df = pd.DataFrame({
    "AMHCC": np.random.choice(["1A01", "1A02", "1B01", "2A01"], size=30),
    "LOS": np.random.randint(1, 20, size=30),
    "STATE": 1, "PAT_PRIVATE_FLAG": 0, "PAT_SAMEDAY_FLAG": 0,
    "PAT_PUBLIC_FLAG": 1,
    "priceCat": 1,
})

# Subacute
sa_df = pd.DataFrame({
    "ANSNAP": np.random.choice(["4A01", "4A02", "4B01", "4B02"], size=25),
    "ADM_DATE": pd.Timestamp("2025-03-01"),
    "SEP_DATE": pd.Timestamp("2025-03-10"),
    "LEAVE_DAYS": 0, "BIRTH_DATE": pd.Timestamp("1970-06-15"),
    "STATE": 1, "PAT_PRIVATE_FLAG": 0, "PAT_PUBLIC_FLAG": 1,
    "CARE_TYPE": 1,
})

# Outpatients
op_df = pd.DataFrame({
    "TIER2_CLINIC": np.random.choice([20.01, 20.02, 30.01, 40.01], size=60),
    "SERVICE_DATE": pd.Timestamp("2025-06-01"),
    "BIRTH_DATE": pd.Timestamp("1980-01-01"),
})

# ── 2. Calculate NWAU per stream ─────────────────────────────────────
result_acute  = calculate_acute(acute_df, AcuteParams())
result_ed     = calculate_ed(ed_df, EDParams())
result_mh     = calculate_mh(mh_df, MHParams())
result_sa     = calculate_subacute(sa_df, SubacuteParams())
result_op     = calculate_outpatients(op_df, OutpatientParams())

nwau_col = "NWAU25"
streams = {
    "Acute":       result_acute,
    "ED":          result_ed,
    "MentalHealth": result_mh,
    "Subacute":    result_sa,
    "Outpatient":  result_op,
}

# ── 3. Notional funding ──────────────────────────────────────────────
nep = get_nep("2025")  # 7258

# ── 4. Synthetic cost benchmarks (imitating NHCDC stream averages) ───
# In a real study these would come from NHCDC data extracts.
cost_benchmarks = {
    "Acute":       5_800,
    "ED":            620,
    "MentalHealth": 9_200,
    "Subacute":     7_400,
    "Outpatient":     520,
}

# ── 5. Comparison table ──────────────────────────────────────────────
rows = []
for stream_name, df_result in streams.items():
    total_nwau = df_result[nwau_col].sum()
    notional_funding = total_nwau * nep
    n_episodes = len(df_result)
    synthetic_obs_cost = n_episodes * cost_benchmarks[stream_name]
    cost_ratio = (synthetic_obs_cost / notional_funding) if notional_funding > 0 else float("inf")
    rows.append({
        "Stream":    stream_name,
        "Episodes":  n_episodes,
        "Total NWAU":  round(total_nwau, 4),
        "Notional Funding": round(notional_funding, 2),
        "Observed Cost":    round(synthetic_obs_cost, 2),
        "Cost Ratio":       round(cost_ratio, 4),
    })

benchmark_table = pd.DataFrame(rows)
print("── Stream-Level Benchmarking Comparison ──")
print(benchmark_table.to_string(index=False))

# ── 6. NHCDC & AHPCS context ─────────────────────────────────────────
print("\n── Context ──")
print("• NHCDC provides the national cost benchmarks that inform NWAU "
      "price weights and the NEP.")
print("• AHPCS ensures methodological consistency in cost allocation "
      "across hospitals and jurisdictions.")
print("• Without AHPCS compliance, inter-hospital cost comparisons "
      "may be misleading.")
print("• In practice, non-admitted and subacute streams use NEC "
      "(not NEP) pricing, which has a fixed+variable cost structure.")
print("• Synthetic data used here — all cost ratios are illustrative "
      "and do not reflect real hospital performance.")
```

## Expected output

| Stream | Episodes | Total NWAU | Notional Funding | Observed Cost | Cost Ratio |
|--------|----------|-----------|-----------------|---------------|-----------|
| Acute | 50 | *varies* | *varies* | 290 000 | *varies* |
| ED | 80 | *varies* | *varies* | 49 600 | *varies* |
| MentalHealth | 30 | *varies* | *varies* | 276 000 | *varies* |
| Subacute | 25 | *varies* | *varies* | 185 000 | *varies* |
| Outpatient | 60 | *varies* | *varies* | 31 200 | *varies* |

Some streams may show `NWAU25 = 0` for all records if the synthetic classification codes do not match the reference data — this is a realistic reflection of what happens when classification codes are not present in the published price-weight tables.

## Caveats for real-world use

1. **Not all streams use NEP** — subacute and non-admitted activity are more commonly priced via NEC (National Efficient Cost), which has a fixed-plus-variable structure.
2. **NHCDC cost data is lagged** — NHCDC data typically reflects costs from 1-2 years prior.
3. **Risk adjustment** — real benchmarking should adjust for case mix, remoteness, and indigenous status.
4. **Jurisdiction variation** — states and territories may apply different price multipliers, loadings, and activity funding policies.
