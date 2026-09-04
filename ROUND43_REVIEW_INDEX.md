# Round 43 v2 review index

## Immutable publication unit

- `ROUND43_REVISION.tex` — canonical manuscript entry point.
- `round43/*.tex` — every input source, including the effective-inversion and
  no-washout linear-time chapters.
- `round43/SOURCE_MANIFEST.json` — exact SHA-256 and byte-size inventory.
- `ROUND43_LOCAL_VERIFICATION.json` — tests and two-pass build record.
- `ROUND43_REVISION.pdf` — PDF built from the exact final source tree.

## Referee response packet

- `AUTHOR_RESPONSE_ROUND42.md` — item-by-item response and v2 audit additions.
- `round43/PROOF_LEDGER.json` — obligation/evidence/check separation.
- `round43/HISTORICAL_REUSE.md` — prior derivations reused and strengthened.
- `ROUND43_READY_FOR_REVIEW.md` — immutable-head review instructions.

## Main theorem map

- `thm:abstract-bvm` — nonlinear adaptive random-information quasi-BvM.
- `prop:balanced-contrast` — finite-prefix global empirical contrast.
- `thm:filter-jets` — strong filter derivatives in deterministic separable spaces.
- `thm:jacobi-reconstruction` — complete Weyl--Schur coefficient recovery.
- `thm:jacobi-rate` / `eq:jacobi-posterior-ldp` — full posterior LDP for the
  logarithmic-washout protocol.
- `thm:effective-jacobi-stability` — explicit depth/separation modulus.
- `lem:response-moment-triangularity` — exact response-derivative to moment
  recursion.
- `prop:effective-gram-reconstruction` — finite Gram/Hankel coefficient
  reconstruction and condition bound.
- `thm:effective-response-jet-audit` — line-addressable proof of the effective
  response-jet inverse.
- `thm:growing-depth-recovery` — increasing finite-block recovery.
- `thm:explicit-shrinking-block-rate` — concrete shrinking coefficient and
  weighted-operator radii.
- `cor:weighted-operator-recovery` — weighted operator-norm contraction.
- `thm:adaptive-exploration-floor` — adaptive exploration floor for the full
  response experiment.
- `thm:honest-jacobi-cylinders` — honest growing-block confidence cylinders
  with logarithmic washout.
- `lem:l1-impulse-geometry` — policy-uniform `L^1` impulse-response compactness.
- `lem:predictable-intercept-information` — fresh-sign orthogonality against
  the complete adaptive history.
- `thm:linear-time-adaptive-jacobi` — no-washout posterior upper exponent in
  linear physical time.
- `thm:linear-time-honest-cylinders` — no-washout finite-sample honest
  coefficient cylinders.

## Reproduction

```text
python3 -m unittest -v tests/test_round43.py
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
python3 tools/verify_round43.py --check-manifest --check-build
```

The final review request identifies one immutable commit SHA.  The retained
workflow is read-only and reproduces precisely the commands above.
