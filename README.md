# Climate Reversal — consolidated data and research code

**Manuscript:** *Carbon-cycle compensation can reverse endpoint and cumulative rankings of equal CO₂ removals*  
**Journal:** Global Biogeochemical Cycles (2026GB009769)  
**Authors:** Jonathan Karl Bily; Christoph Pahl

This repository is intended to become the **permanent, DOI-backed reproducibility archive** for the above study. GitHub itself is not the permanent archival DOI; once scientifically complete, publish a tagged release to Zenodo.

## What is archived

- `data/v67/cases/`: **12 original successful multi-model case outputs**, each containing input trajectory CSV, FaIR/Hector/OSCAR time series, model/ensemble member metrics, numerical summaries and console logs. These files were directly extracted from the verified GitHub Actions archives; they were **not regenerated**.
- `data/v67/synthesis/`: original synthesis tables (`V67_CASE_METRICS.csv`, `V67_MEMBER_RANKING.csv`) and validation JSON/Markdown.
- `data/v67/original_artifacts/`: **13 original ZIP archives** for bit-for-bit provenance, with GitHub-recorded SHA-256 digests in `provenance/archive_manifest.json`.
- `figures/Fig1.png` through `Fig4.png`: figure image files from the submitted manuscript ZIP.
- `data/published_tables/Table_S1.csv` through `Table_S6.csv`: cell text faithfully exported from the accompanying Word Supporting Information, labeled as **published tables**, not raw simulation data.
- `science_figures/inputs/`: **44 independently reconstructed scenario input trajectories** for removal size/rate, storage leakage and the 400-GtCO₂ pathways; also validated analytical linear-kernel and leakage mass-balance reference tables. These are NOT archived FaIR ensemble simulation outputs.
- `code/`: pinned copies of V62.2, V65 and V67 source repositories **after the included source-fetching script has been run**.
- `scripts/`, `provenance/`: import utility, checksum and validation instructions.

## Model source — required one-time step

Before creating the GitHub release or uploading the complete source archive, run:

```bash
python scripts/fetch_pinned_sources.py
python scripts/verify_archive.py
```

This fetches the actual original source code from three existing public repositories at **specific Git commit hashes**, checks those hashes, removes nested `.git` directories and stages the complete source snapshots under `code/`. The script is intentionally not a speculative rewrite.

On Windows, open PowerShell in the unpacked directory and run `python scripts/fetch_pinned_sources.py` (requires Git and Python). You can then run `scripts/PUBLISH_TO_GITHUB_WINDOWS.ps1` to push all files to the named empty repository using your own authorized Git credentials.

## Evidence and caveats

The 13 downloaded V67 output archives passed comparisons to the SHA-256 values recorded by GitHub. The upstream Actions workflow run 34724619356 reports successful completion of 12 cases plus synthesis. See `provenance/archive_manifest.json` for source commits, run ID, original file digests and provenance.

**This repository is not yet proof of full reproduction of the four-figure manuscript.** The original sensitivity-input schedules have been reconstructed with explicit formulas, but **the climate-model outputs and original rendering scripts have not been recovered**. The manuscript additionally describes FaIR experiments at end-of-2183 / FaIR bound **2184** for removal size/rate, background scenario, leakage and 2100 pathways. The formerly cited `science_figures` folder, raw outputs for those additional sensitivity runs and their figure-generation scripts were **not available** in the V67 repository. The published table CSVs document the reported values but do not substitute for missing raw data or code. See `OPEN_ISSUES_FOR_AGU.md`.

Do not claim that the present FaIR-bound-2183 workflow outputs reproduce the manuscript's FaIR-bound-2184 figures until verified. Do not invent missing data, and do not assign a DOI without a published Zenodo record.

## Data reuse

These files are research materials with different upstream ownership/licensing conditions. Original source files retain their upstream notices (when imported); consult the original model repositories and package licenses before redistribution or adaptation. No new blanket license is claimed for third-party model code or outputs.
