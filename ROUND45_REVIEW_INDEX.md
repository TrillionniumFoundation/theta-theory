# Round 45 review entry

Canonical article: `ROUND45_REVISION.tex` and every `round45/*.tex` input.
Response: `AUTHOR_RESPONSE_ROUND44.md`.
Traceability: `round45/PROOF_LEDGER.json`, `round45/HISTORICAL_REUSE.md`.
Integrity: `round45/SOURCE_MANIFEST.json`.
The distribution receipt is `ROUND45_VERIFICATION.json` when present; its
`source_commit` is the immutable source object actually checked. A PDF is
part of the distribution only when `ROUND45_REVISION.pdf` is present and its
hash matches that receipt. Source-only and PDF publication are not conflated.

## Mathematical reading order

`uniform_statistics.tex` contains the finite-n bounds and Laplace tracking.
`inverse_stability.tex` contains the replacement condition calculation.
`infinite_jacobi.tex` and `linear_time_protocol.tex` verify the two experiments.
`growing_depth_uncertainty.tex` supplies contraction and frequentist confidence
sets. The homogeneous likelihood, lattice and filter sections preserve the
finite-dimensional results.

## Reproduction

```sh
python3 tools/verify_round45.py --build --source-sha "$(git rev-parse HEAD)"
```

This runs six regression tests and three LaTeX passes, checks every source
hash before and after, rejects undefined references and overfull boxes, and
reports the PDF hash. Tests do not constitute proof-assistant verification.
