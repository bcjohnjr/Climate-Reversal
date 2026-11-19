# Rebuilt Fig. 2 — source and provenance

The figure in the revised manuscript is **not** the exact original historical rendering script. It is a newly written reproduction from archived 841-member outputs. Run `python FAIR_REBUILD_FIG2.py` in the repository root (requires numpy, pandas, matplotlib and pillow) after uploading the two V67 coupled source ZIPs in this patch. The existing `FAIR_56_CASE_OUTPUTS.zip` is also needed.

| Protocol | Data files | FaIR evaluation bound |
|---|---|---:|
| Fixed source | `FAIR_56_CASE_OUTPUTS.zip`: `size_2013.88_rate_20_early/late` | 2184 |
| Ideal permanence | `FAIR_56_CASE_OUTPUTS.zip`: `leak_0.00_tau_0_early/late` | 2184 |
| Programme-coupled | Original GitHub Actions ZIPs in this patch, member metrics | 2183 |

The source GitHub Actions run is https://github.com/bcjohnjr/Planetary-Restoration-Model-V67/actions/runs/34724619356.

- `V67_COUPLED_BOUND2183_EARLY.zip` — artifact ID **10309224861**, SHA-256 `690cb9cae89461cad2c120329de2e6caa37d787ac2b289b3c17a0bb2cdaf4c7c`.
- `V67_COUPLED_BOUND2183_LATE.zip` — artifact ID **10310590536**, SHA-256 `0904097d0c1d2ce1306885c7a09ea5f3b816278cf3a77d9c55ff777a8b8d7384`.

The figure's FaIR dots show differences of median early/late trajectories (published Table 1), and the violin and 5–95% interval are computed from 841 differences of matched ensemble members. The median of member-by-member differences need not coincide exactly with the difference of median trajectories. Hector/OSCAR point markers are based on original archived central results. The original V67 OSCAR least-favourable member margins and support proportions are shown for forcing and endpoint concentration. The script regenerates a TIFF image and `FAIR_FIG2_PAIRED_AUDIT.csv`.

A true end-of-2183 **programme-coupled FaIR bound-2184** simulation remains unavailable and has not been fabricated. Its absence does not invalidate the 56-case FaIR sensitivity matrix, which is a different experiment.
