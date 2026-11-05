# Audit of completeness before an AGU/Zenodo claim

**Recovered and verified:** All 13 ZIP archives belonging to V67 GitHub Actions run 34724619356; extracted 12 case datasets and synthesis; four figure PNGs; published supplementary Tables S1–S6; exact pinned upstream repositories and input-data locations.

**Important distinction:** The archived V67 workflow produced FaIR time-bound-2183 results. The submitted manuscript largely reports FaIR end-of-2183 metrics evaluated at bound **2184**, after the final year's emissions have been applied. Matching the manuscript requires an explicit one-year extension and independent numerical comparison, not relabeling of the previous outputs.

**Partially reconstructed:** 44 sensitivity **inputs** from the archived baseline and formulas; all 14 Table S3 linear-kernel reference results match to 0.01 ppm, all Table S5 leaked masses match to integer GtCO₂. These tests do not establish the corresponding FaIR model output values.

**Unrecovered source/data:** The original `science_figures/` experiment source and member-level sensitivity outputs were not in upstream V67 or the supplied Science/ Nature Climate Change submission ZIPs. They include (i) 14 removal total/rate combinations, (ii) three alternative background pathways plus canonical cases, (iii) six storage leakage parameter combinations, and (iv) the pair of 400-GtCO₂ programmes ending 2100. Table S3–S6 CSVs contain published table entries, not the raw 841-member outputs.

**Before claiming fully FAIR-compliant results:** (1) fetch and retain pinned source, (2) reproduce additional FaIR sensitivity results using the pinned calibration and methods, (3) compare regenerated values *including member-level minima and time-bound conventions* against Tables S1–S6 and figures, (4) archive generated raw outputs and exact rendering scripts, (5) create a Zenodo release and cite the real DOI in manuscript and references.

No incomplete component should be described as independently reproduced. The present archive is an honest, substantial preservation of existing evidence, not a claim of completed replication.
