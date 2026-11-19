# Upload instructions — repository correction V7

Target: https://github.com/bcjohnjr/Climate-Reversal

The ChatGPT GitHub connector **could read** this repo but returned HTTP 403 when asked to update files. **No edits were pushed to GitHub by ChatGPT.** To publish the corrections:

1. Extract this ZIP. Open the GitHub repository (main branch).
2. Replace existing root `README.md` with the supplied `README.md`.
3. Replace existing root `CITATION.cff` with the supplied `CITATION.cff`.
4. Upload the new root files `REPRODUCIBILITY_STATUS.md`, `FAIR_REBUILD_FIG2.py`, `FAIR_FIG2_PAIRED_AUDIT.csv`, `V67_COUPLED_BOUND2183_EARLY.zip`, and `V67_COUPLED_BOUND2183_LATE.zip`.
5. Replace `figures/Fig2.png` with the supplied file in the `figures/` subdirectory. This is a newly reproducible reconstruction, not the identical original historical rendering.
6. Delete the obsolete `OPEN_ISSUES_FOR_AGU.md` once the new status file is committed. Do **not** delete `data.zip`, `FAIR_56_CASE_OUTPUTS.zip`, or any existing provenance archives.
7. Commit as "Update reproducibility status and reconcile programme-coupled FaIR bound".
8. Run `python FAIR_VERIFY.py --verify` and optionally `python FAIR_REBUILD_FIG2.py` from the repository root after installing the requirements in its header. Check the figure is reproduced.

The new README is neutral about journals; `CITATION.cff` keeps legitimate author attribution. Thus the public repository is **still author-identifying** and is NOT an anonymised review mirror. The journal editor must approve its use under double-blind review.
