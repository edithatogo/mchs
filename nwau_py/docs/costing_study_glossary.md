# IHACPA Costing Study Glossary

## NWAU (National Weighted Activity Unit)

A measure of hospital activity cost-weight. Each episode of care is assigned an NWAU value based on its clinical complexity, length of stay, and patient characteristics. NWAUs are calculated using stream-specific calculators (acute, ED, mental health, subacute, outpatient) that apply IHACPA's published price weights and adjustment factors.

## NEP (National Efficient Price)

The price per NWAU set annually by IHACPA for admitted acute and related activity. For NEP26 (2026-27) the price is **$7,418 per NWAU(26)**. For NEP25 it was **$7,258 per NWAU(25)**. The NEP is published in IHACPA's *National Efficient Price Determination* each year.

```python
from nwau_py.pricing_constants import get_nep, NEP_BY_YEAR

nep_2025 = get_nep("2025")  # 7258
nep_2026 = get_nep("2026")  # 7418
```

## NEC (National Efficient Cost)

The cost per unit for non-admitted, rehabilitation, and other activity types that are not well-suited to the NEP model. The NEC uses a fixed-plus-variable cost structure. For NEC26, IHACPA published a fixed cost of **$3.127m per hospital** and a variable cost of **$8,003 per NWAU**.

```python
from nwau_py.pricing_constants import get_nec, NEC26

nec = get_nec("2026")
# NecPricing(fixed_cost_dollars=3_127_000, variable_cost_per_nwau=8_003, in_scope_hospitals=364)
```

## Notional Funding

The funding that would be received if every NWAU were reimbursed at the full NEP rate. Calculated as:

**Notional Funding = NWAU × NEP**

This is a benchmark figure, not actual hospital funding (which depends on jurisdiction-specific pricing policies, activity-based funding arrangements, block grants, and other adjustments).

## Efficient Price

The benchmark cost per unit that IHACPA considers efficient for delivering care. For acute admitted activity, this is the NEP. For non-admitted and subacute streams, the efficient cost is modelled through the NEC. "Efficient" means the cost that a reasonably efficient hospital should incur — not the average cost, but a target derived from the cost distribution of peer hospitals.

## Observed Cost

The actual cost incurred by a hospital or health service to deliver care, typically drawn from:
- **NHCDC** (National Hospital Cost Data Collection) — IHACPA's national collection of hospital cost data
- Local general ledger or patient-level costing systems (e.g. PowerPerformance, Logibec)

In a costing study, observed costs at the episode or patient level are compared against the efficient price to identify underpricing or overpricing.

## NHCDC (National Hospital Cost Data Collection)

IHACPA's national data collection that captures hospital activity, cost, and revenue data from public and private hospitals across Australia. The NHCDC underpins the derivation of NWAU price weights and the NEP/NEC determinations. It is the primary source for cost benchmarks used in Australian hospital costing.

## AHPCS (Australian Hospital Patient Costing Standards)

The methodological standards published by IHACPA that govern how hospitals should assign costs to patient episodes. AHPCS ensures consistency in:
- Cost allocation (direct vs indirect costs)
- Overhead attribution
- Patient-level costing methodology
This consistency is essential for benchmarking across hospitals and jurisdictions.

## Costing Study

An analytical exercise that compares hospital activity, cost, and funding, typically with the goal of identifying services that are over- or under-funded relative to efficient benchmarks. A typical costing study workflow:
1. Calculate NWAU per episode using the stream-appropriate calculator
2. Multiply NWAU by NEP to get notional funding
3. Compare observed cost (from NHCDC or local systems) against notional funding
4. Summarise at stream, DRG, or hospital level

## Benchmarking

The process of comparing local costs against a reference standard. In the IHACPA context, benchmarking typically means comparing observed costs against national efficient prices (NEP or NEC). A cost ratio > 1 indicates the local cost exceeds the efficient price; a ratio < 1 indicates the local cost is below the efficient price. Benchmarks are most meaningful at aggregate (stream or hospital) rather than individual episode level due to case-mix variation.
