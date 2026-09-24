# General Theta Foundations I — v22
## Causal Continuation and Statistical Resource Frontiers

The full English revision is `paper.pdf`; its source entry is `main.tex`. The complete historical development is `complete-development.pdf`. The point-by-point response is `RESPONSE_TO_REFEREE.md`. This package starts from the actual v21 publication rather than repeating its results as new.

### Mathematical entry points

Theorem `thm:v22-tournament` gives a fixed-preparation, all-cut rational realization of a response cover. Theorem `thm:v22-revelation` gives an exact Bayesian optimum over all stochastic machines under arbitrary revelation schedules, priors and cut profiles, with sharp sample–peak inversion. Theorem `thm:v22-active` transports retained laws through occupation-weighted transition defects. Theorem `thm:v22-physical` realizes the original physical threshold with 320,000 training trials and peak 1,604, preserving both earlier regimes. Theorem `thm:v22-confidence` gives two fully priced finite-state confidence amplifiers.

Compiled theorem numbers/pages, actual diagnostic counts and source/PDF hashes are recorded by the executed build in `evidence/`. The exact physical fixed-N frontier and exact integer peak are not asserted. The original Norberg proof-level crosswalk remains incomplete; priority is not inferred from unavailable text.

### Reproducibility and preservation

Run `python build.py` with Python 3, PyMuPDF and a LaTeX installation providing the packages in `preamble.tex`. The original sibling directory `../GTF-I-v21-multicut-resources/` is required for preservation checks. The portable archive `evidence/SUBMISSION_SOURCES.zip` contains the needed predecessor sources/PDF in the expected relative location.

The build runs v22 and both inherited finite diagnostic suites normally and with Python optimization, checks that all listed negative controls fail, compiles three LaTeX passes, forbids undefined references and overfull boxes, and compares every appended predecessor page in text and 72-dpi raster rendering. It binds the published files to the actual source commit. Successful diagnostics are not independent verification of the analytic proofs or journal acceptance.

`RESOURCE_LEDGER.md`, `PROOF_STATUS.json`, `PIPELINE_STATUS.json`, `HISTORY_AUDIT.md`, `INHERITANCE.json` and `LITERATURE_CROSSWALK.md` specify resources, proof scopes, actual dependencies and unchanged historical targets. No old manuscript, referee report or repository path is modified by this revision. Font files are not distributed.
