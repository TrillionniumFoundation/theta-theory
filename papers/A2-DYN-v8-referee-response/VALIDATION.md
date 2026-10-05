# Author-side validation of revision 8

The complete local article builds to **49 pages** with native `pdflatex`, using the included `build.sh`. The final TeX log has no undefined references/citations, warnings, overfull or underfull boxes. The title page and pages containing the new results were rendered and visually inspected. The article has **21 included core source files, 62 explicit proof environments, and 194 unique labels**. These counts are syntactic, not assertions that an automated system certified the proofs.

All **19** preceding core files and **8** historical diagnostic scripts pass exact SHA-256 preservation checks. The new source audit and finite model checks pass in both normal and optimized Python with identical output. The new diagnostics perform **13,217** checks of rational finite renewal models, deterministic counting comparisons and finite-band cutoff algebra. The six retained diagnostics `certify_winding`, `certify_excursion`, `verify`, `verify_v2`, `check_v5` and `check_v6` also run successfully.

The GitHub workflow repeats these checks on its exact event commit and generates its own receipt, including the clean scoped source state, TeX hashes and PDF hash. Local qualification is not reported as a remote CI result; consult the workflow run and its exact-SHA artifact for the remote outcome.

Neither the native build nor these finite diagnostics prove the full continuum raw LLT. Independent human specialist review has not occurred as part of this revision. The remaining analytical hypotheses and the four new proved statements are identified in the manuscript and `PROOF_LEDGER.md`.
