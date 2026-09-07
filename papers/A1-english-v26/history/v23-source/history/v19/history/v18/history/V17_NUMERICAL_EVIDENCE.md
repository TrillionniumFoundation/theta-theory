# Numerical and source evidence — A1 v17

The new analytic results are proved in `sections/operational_reconstruction.tex`. Numerical tests are finite regression checks, not substitutes for those proofs.

`tests/test_v17.py` uses only exact rational arithmetic and integer powers. It checks the supporting real budget, all competing branches, upward integer rounding, bounded recovery with integer budgets, repeated scales, positive-to-zero rank changes, vanishing-product tails, paired circular exponents and their repeated ratios. It checks branch maxima without computing floating-point roots. It also verifies that the published command-language correction remains in place and that no inherited test source was altered.

The six inherited suites `test_v10.py` through `test_v15.py` are copied unchanged. Their original assertion counts are verified by the new execution driver. The optional original v16 referee script is pinned by SHA-256 and rerun without its old-v16-artifact option. That rerun checks its mathematical fixtures only and does not create an independent review of v17.

The full build performs three no-shell-escape TeX passes and rejects undefined references and overfull boxes. `build.py` additionally compares every v16 complete proof and named statement with a preservation manifest generated from the verified v16 source expansion. Source hashes, proof preservation, typesetting, exact rational diagnostics and floating-point diagnostics are reported as different forms of evidence.

The new curve transform takes an infimum over all positive integer budgets. Neither the finite test suite nor a finite observed budget range is claimed to reconstruct the continuum family of true minimax risks. The zero-product assertion is an analytic limit, proved separately in the text.

See the actual `validation/EXECUTION_REPORT.json` for successful runs, counts, source hashes, PDF digest and explicit scope. Results from predecessor executions are kept only under `history/`.
