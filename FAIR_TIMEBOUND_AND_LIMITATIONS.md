# Reproducibility audit notes for editors and referees

## Completed checks

- Exactly 56 independent FaIR cases (28 removal size/rate, 14 leakage, 12 official emissions background cases, and 2 400-GtCO2 pathways).
- Each case has FaIR 2.2.4 metadata with 841 constrained configurations, end-of-2183 state at timebound 2184, finite annual median trajectories and 3 endpoint member-level metrics datasets (2100, 2150, 2183).
- Forcing-match residuals stay below the predeclared simulation criterion of 1e-4 W m-2.
- All 152 supplementary Table S3–S6 comparisons agree within published rounding tolerances: S3 70, S4 48, S5 28, S6 6. None were edited to force agreement.

## Critical timebound correction

An initial audit appeared to fail six Table S4 background checks because it compared the published column "OFF CO2 in 2100 (ppm)" with the END OF 2100 (FaIR timebound 2101). The published CO2 levels correspond instead to FaIR timebound 2100: low 442.769 ppm (rounds to 443), medium 594.959 ppm (595), high 722.231 ppm (722). This comparator correction explains all six differences; all other result calculations were unchanged. For the 2183 endpoint, use bound 2184. The manuscript/SI should explicitly identify this mixed reporting convention.

## Hash and provenance limitation

Every original case `validation.json` recorded a SHA-256 of the case's input CSV *before* `src/run_fair_case.py` resaved the input as `external_validation_net_co2_trajectory.csv` in the results directory. Their raw byte hashes therefore differ even where the numbers are identical to numerical precision. None of the original evidence was rewritten. `FAIR_PROVENANCE_AUDIT.csv` documents both hashes and the maximum differences; the exact preserved archive bytes are covered by `FAIR_RESULTS_SHA256.csv`. The V6 code records both source and staged hashes in any new runs.

## Scientific scope and limitations

- This verifies numerical results against the study's published tables, not independent validity of the underlying climate physics or choice of scenarios.
- The archived data contain **annual median** trajectories and member-level **endpoint/integral metrics**, not every full annual time series for all 841 members. A new FaIR run is needed to rebuild arbitrary uncertainty bands by year.
- Original exact manuscript figure-rendering scripts are still missing; this package does not claim bitwise-identical regeneration of all original figures.
- Cross-model Hector and OSCAR results are available elsewhere in the project's archived V67 files, but the 56-case matrix here is FaIR-only. It does not independently re-execute their full multi-model experiments.
- The rerun depends on publicly reachable pinned Git source commits and dependency mirrors; no claim is made that future public upstream services will remain indefinitely available. A Zenodo archive would improve long-term preservation.
- The model-matching tolerance is 1e-4 W/m2, not the original V62 demonstration's stricter 1e-7 W/m2. Further stricter re-execution can be done separately and reported transparently.
- Journals may also require authors to disclose related earlier submissions and independently justify the scientific interpretation.

## How to cite data

Repository: `https://github.com/bcjohnjr/Climate-Reversal`. Refer to the tagged release/commit SHA after upload; a Zenodo DOI must only be cited after an actual published Zenodo deposit. No new DOI is implied by this ZIP.
