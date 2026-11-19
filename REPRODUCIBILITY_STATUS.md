# Current reproducibility status

Updated 19 November 2026; this supersedes the older `OPEN_ISSUES_FOR_AGU.md` that was written before the sensitivity experiments were recovered.

## Recovered and checked

- A 56-case FaIR sensitivity matrix, 841 members per case, bound 2184 representing end-of-emissions-year 2183: **56/56 PASS**.
- All **616** preserved case-output file hashes verified, and **152/152** numerical comparisons in supplementary Tables S3–S6 reproduced from the saved output archives.
- Separate original 12-case V67 three-model archive (FaIR, Hector, OSCAR) retained; original FaIR bound **2183**.
- Original V67 programme-coupled FaIR comparisons verified at bound 2183: **75.74 W m⁻² yr**, **18.61 ppm**, **43.64 °C yr**; paired minima **58.35 W m⁻² yr**, **15.93 ppm**, **22.93 °C yr**.
- Corrected Figure 2 can be plotted from actual member data using the newly provided script, plus the 56-case and original V67 coupled ZIPs. The source remains credited to the archive, not to an invented new FaIR run.

## Do not overclaim

1. The archived-output verifier does **not** itself rerun the 56 full climate-model simulations.
2. No archived original programme-coupled FaIR model run with timebound 2184 was found; the manuscript correctly retains the **2183** values and explicitly distinguishes them.
3. The original complete figure-rendering suite is unavailable; a new Figure 2 rendering script does not recover the original source code.
4. The 56-case matrix was performed with FaIR; Hector/OSCAR were tested in the separate older 12-case experiment and were not rerun in the 56-case matrix.
5. Input CSV source hashes and output CSV hashes differ where files were reserialised; source and preserved output bytes are both documented. The climate values agree to floating-point precision.
6. The source has a **10⁻⁴ W m⁻²** matching threshold in the 56-case matrix, not the older **10⁻⁷ W m⁻²** FaIR convergence criterion. Bounds and numerical gate tolerances must not be conflated.
7. Public GitHub author and citation metadata prevent this link being independently anonymous under a double-blind policy.

The repository demonstrates numerical reproducibility of preserved sensitivity outputs, **not** independently validated physics or a fresh end-to-end 56-run reproduction.
