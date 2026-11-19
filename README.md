# Climate Reversal — research code and reproducibility archive

**Study:** *Carbon-cycle compensation can reverse endpoint and cumulative rankings of equal CO₂ removals*

This public research repository preserves the original carbon-cycle experiments and subsequent reproducibility work. It is **not associated with an active journal submission**. Authorship is retained in `CITATION.cff` and historical Git records. See `REPRODUCIBILITY_STATUS.md` for the precise distinction between recovered and newly generated outputs.

## Verified FaIR sensitivity matrix — bound 2184

`FAIR_56_CASE_OUTPUTS.zip` contains **56 FaIR 2.2.4 cases**: 28 removal total/rate cases, 14 stored-carbon leakage cases, 12 low/medium/high background cases, and two 400-GtCO₂ timing cases. Each case was run with **841 calibrated configurations**. These simulations evaluate the **end of the emissions year 2183**, FaIR timebound **2184**. The maximum archived non-CO₂ forcing residual was **2.43 × 10⁻⁵ W m⁻²**, beneath the declared **10⁻⁴ W m⁻²** matching threshold.

Independent clean-extraction verification of the archived outputs passed **56/56 case validations**, **616/616 original file hashes**, and **152/152 numerical comparisons** with Tables S3–S6 (70/70, 48/48, 28/28 and 6/6). The Table S4 background CO₂ column for *2100* uses FaIR timebound **2100**, while the end-of-2183 terminal comparisons use **2184**. The verifier confirms archived results and table calculations, not a fresh 56-case climate-model run.

Run in the repository root (Python with NumPy and pandas required):

```bash
python FAIR_VERIFY.py --verify
```

The deposited rerun code is in `FAIR_REPRODUCTION_CODE_V6.zip`; use `python FAIR_VERIFY.py --extract-code` or `python FAIR_VERIFY.py --rerun` if all pinned dependencies, Git and computational resources are available. Windows launchers are provided. A GitHub Actions workflow is present at `.github/workflows/fair-sensitivity-reproduction.yml`, but its presence alone does not establish that a new complete run has executed successfully.

## Original V67 three-model protocol archive — FaIR bound 2183

`data.zip` preserves original GitHub Actions archives for **12** FaIR/Hector/OSCAR protocol cases, including fixed-source, ideal-permanence, programme-coupled and permafrost settings. These were originally executed at FaIR timebound **2183**, *before* applying all emissions in 2183. They are not interchangeable with the newer bound-2184 sensitivity outputs.

In particular, the original **programme-coupled FaIR** early/late cases, independently recalculated from the 841 member-level files at **bound 2183**, give:

| Metric | Verified bound-2183 value |
|---|---:|
| Early minus late integrated CO₂-forcing advantage | **75.74 W m⁻² yr** |
| Late minus early terminal atmospheric CO₂ benefit | **18.61 ppm** |
| Early minus late integrated avoided warming | **43.64 °C yr** |
| Minimum paired-member integrated forcing margin | **58.35 W m⁻² yr** |
| Minimum paired-member terminal concentration margin | **15.93 ppm** |
| Minimum paired-member integrated warming margin | **22.93 °C yr** |

An earlier manuscript draft listed **75.41 / 19.50 / 43.62** and corresponding member minima at bound 2184 for this programme-coupled case; those exact values were not supported by an archived bound-2184 programme-coupled simulation. The manuscript was corrected to use the genuine archived **bound-2183** results, explicitly labelled. The separately archived Table S2 canonical FaIR row (75.74 / 18.61) agrees.

Two copies of the original V67 coupled-case Actions ZIPs, `V67_COUPLED_BOUND2183_EARLY.zip` and `V67_COUPLED_BOUND2183_LATE.zip`, and `FAIR_REBUILD_FIG2.py` provide direct reproducibility of the corrected Figure 2 distributions when added from the accompanying documentation patch. The rebuilt plot is not claimed to be the exact original historical plotting script.

## Provenance, model references and limitations

- FaIR 2.2.4 source commit: `ec46fefc8f8c6b560a8b78ab1f4a9a5e04537f79`; fair-calibrate 1.4.1, **841** configurations.
- V62.2 matched-forcing source runner commit: `89a0f4ab18df25db3a05d4e39c6db06405456505`.
- OSCAR v3.3 source tag commit: `3ce008400e06363564e5981a35cbc32377d41d86`; tagged software reference DOI: `10.5281/zenodo.10548477`.
- Source-input hashes in some original case `validation.json` files were recorded before CSV reserialisation. The maximum difference in numerical values is approximately `1.24 × 10⁻¹⁴ GtCO₂ yr⁻¹`; `FAIR_RESULTS_SHA256.csv` and `FAIR_PROVENANCE_AUDIT.csv` preserve exact output-byte checksums and this distinction.
- The FaIR 56-case archive stores annual *median* time series and member-level endpoint/integral metrics, not every member's full annual time series.
- The 56-case sensitivity matrix is FaIR-only. Older Hector/OSCAR cases have not been newly executed as part of that matrix, and the original figure-rendering scripts were not recovered in full.
- The public repository exposes the author identity through account and citation metadata. **It is not anonymous for double-blind peer review.** The journal editor should authorise the identifying link or request an anonymised view.
- A repository commit SHA identifies specific deposited files. No new Zenodo DOI is implied before a real published deposition. Original model sources and third-party data retain their own licence and citation requirements.

**For source-by-source details:** `FAIR_README_GITHUB_UPLOAD.md`, `FAIR_TIMEBOUND_AND_LIMITATIONS.md`, `REPRODUCIBILITY_STATUS.md`, `science_figures/README.md`, `provenance/archive_manifest.json`.

The older `science_figures/inputs/` directory preserves reconstructed input trajectories, **not** the full sensitivity output. The authoritative recovered sensitivity outputs are now archived in `FAIR_56_CASE_OUTPUTS.zip`.
