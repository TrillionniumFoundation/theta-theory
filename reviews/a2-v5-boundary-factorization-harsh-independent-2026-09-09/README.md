# Independent A2 v5 review

The controlling report is **[REFEREE_REPORT.md](REFEREE_REPORT.md)**.

Reviewed manuscript: `ee879236d0fae1f84c685bef4ff27326403d4b2d`, in `papers/A2-v5-boundary-factorization/`. The review adds no manuscript changes.

**Recommendation:** reject at the requested top-four level on importance and positioning, not an identified fatal mathematical counterexample. The previous NBL requests are substantively addressed. The report includes an independently derived three-amplitude refinement near the physical member with R = 1/4.

This is an independent AI-assisted assessment requested by the repository owner, not a journal-commissioned review.

## Reproduce the finite diagnostics

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python independent_diagnostics.py > DIAGNOSTICS.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O independent_diagnostics.py > DIAGNOSTICS.optimized.json
cmp DIAGNOSTICS.json DIAGNOSTICS.optimized.json
```

Dependencies: NumPy, SciPy, SymPy, and mpmath. Recorded versions and file hashes are in `VERIFICATION.json`. The final suite passes 48 named checks: 29 exact symbolic, 14 ordinary floating non-interval, and 5 high-precision non-interval. These are finite diagnostics, not theorem, interval, formal-proof, or editorial certificates.

The full output is retained in `DIAGNOSTICS.json`; the optimized output is identical in the recorded environment. No manuscript PDF build, remote CI, or replay of author validation suites is claimed.
