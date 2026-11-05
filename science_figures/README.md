# Reconstructed sensitivity inputs and analytical reference values

The code in `generate_sensitivity_inputs.py` uses the **original** 2026–2183 emissions columns from the recovered V67 GitHub Actions `fixed__early` case trajectory and the scenario definitions in the submitted `GBC_Supporting_Information.docx`.

Regenerate all inputs locally:

```sh
python science_figures/generate_sensitivity_inputs.py
python science_figures/check_against_supplement.py
```

Inputs are organized as:

* `inputs/size_rate/` — 14 feasible total/rate pairs, early and late (28 CSV files).
* `inputs/leakage/` — the 0% leakage control and 6 nonzero leakage cases, early and late (14 CSV files). Each year's leakage is calculated from the **existing** reservoir before the current year's deposit is added. The OFF branch should exclude programme-contingent leakage (`off_stored_reversal_zero=true`).
* `inputs/pathways_2100/` — two 400-GtCO2 timing pathways; because endpoint rates in the paper are rounded, the annual shapes are proportionally normalized to precisely 400 GtCO2. These are **reconstructed schedules** and not independently verified original schedule files.
* `inputs/joos_linear_kernel_table_S3.csv` — independently calculated linear-kernel endpoint prediction under the exact equation in the Supporting Information; all 14 values agree with the reported Table S3 after rounding to 0.01 ppm.
* `inputs/leakage_accounting_table_S5.csv` — independently calculated mass balance; all reported Table S5 total leaked values agree after rounding to integer GtCO2.

**Not reconstructed / not independently verified:** FaIR member-level output for these sensitivity cases, three non-canonical fair-calibrate 1.4.1 background trajectories, bound-2184 forcing matches, the original PNG rendering scripts, and any figure data beyond these reconstructed inputs and analytical values. In particular these inputs **do not constitute a replacement** for the missing FaIR outputs behind Figures 3 and 4.

The original model runner scripts can be fetched at pinned commits via `scripts/fetch_pinned_sources.py`, but the full FaIR sensitivity simulations are computationally expensive and must be rerun and checked separately against Tables S3–S6 before a complete reproducibility claim can be made.
