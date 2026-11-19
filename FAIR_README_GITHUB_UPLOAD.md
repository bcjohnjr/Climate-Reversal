# Climate-Reversal — flat FaIR reproducibility upload, V6

**Destination:** https://github.com/bcjohnjr/Climate-Reversal

## GitHub web upload (flat repository root)

1. Extract `Climate_Reversal_GitHub_Flat_Upload_V6.zip` locally.
2. Open the repository URL above and choose **Add file → Upload files**.
3. Drag **all files from the extracted folder** into the GitHub uploader and commit to `main`. Do **not** upload the outer ZIP alone; it is only the transfer container. Do not delete or overwrite the repository's existing README, data.zip, figures or science_figures folders.
4. For automated GitHub Actions reruns, create the file **`.github/workflows/fair-sensitivity-reproduction.yml`** in the repository and paste the contents of `FAIR_GITHUB_WORKFLOW_UPLOAD_ME.yml`. GitHub only discovers workflows stored under `.github/workflows`; the flat root YAML is a staging file.

All files in the outer ZIP are at its root; no nested upload directories are required. The two archival ZIPs deliberately keep the scientifically meaningful internal per-case directory structure.

## Contents

- `FAIR_56_CASE_OUTPUTS.zip`: original Windows-run outputs for all 56 cases; 11 original files per case, including 841-member metrics at three endpoints, annual median time series, input trajectory, source runner, forcing setup and validation.
- `FAIR_REPRODUCTION_CODE_V6.zip`: reproducibility source, 56 input trajectories, reference tables and pinned source checks, original V67 audit archives, Windows/Linux launchers, corrected numerical comparison code and S4 timebound regression test.
- `FAIR_VERIFY.py`: independent archive-integrity, completeness and numerical reproduction entry point.
- `FAIR_VERIFY_WINDOWS.bat`: one-click Windows offline verification (requires Python 3.12).
- `FAIR_RERUN_WINDOWS.bat`: rerun the original model after extracting source (Git and network required).
- `FAIR_EXPECTED_56.json`: exact IDs of all required cases.
- `FAIR_152_COMPARISONS.csv`, `FAIR_56_CASE_STATUS.json`: published numerical audits.
- `FAIR_PROVENANCE_AUDIT.csv`, `FAIR_RESULTS_SHA256.csv`, `FAIR_UPLOAD_SHA256SUMS.txt`: byte-level source and output evidence.
- `FAIR_AUDIT_SUMMARY.json`: machine-readable reproduction outcome and caveats.
- `FAIR_GITHUB_WORKFLOW_UPLOAD_ME.yml`: optional workflow to paste into `.github/workflows`.

## Commands

**Verify archived results (no climate-model re-run, NumPy + pandas required):**

```shell
python FAIR_VERIFY.py --verify
```

**Extract verified source only:**

```shell
python FAIR_VERIFY.py --extract-code
```

**Rerun using pinned upstream model sources (may require substantial computing resources):**

```shell
python FAIR_VERIFY.py --rerun
```

The rerun uses FaIR 2.2.4, exactly 841 calibrated configurations, the verified V62.2 source, official low/medium/high background inputs, and the 2184 state evaluation bound. On Windows use `FAIR_RERUN_WINDOWS.bat`, which automatically installs the pinned runtime in a dedicated environment.

## Scientific outcome

**56 / 56** cases validated, **152 / 152** reported comparisons passed with the correct convention: Table S4's `OFF CO2 in 2100` refers to FaIR timebound **2100**, not end-of-year 2100 at bound 2101. See `FAIR_TIMEBOUND_AND_LIMITATIONS.md` for detailed limitations. The maximum non-CO2 forcing-matching residual across the archive is **2.42956239e-05 W/m2**, below the documented **1e-4 W/m2** tolerance.

The archived case-input hashes in validation files refer to the pre-staged source CSVs; archived copies were reserialised. The numerical differences from the reconstructed inputs are at most **1.24e-14 GtCO2/yr**, and exact preserved bytes have a separate SHA-256 manifest. This is disclosed rather than disguised.
