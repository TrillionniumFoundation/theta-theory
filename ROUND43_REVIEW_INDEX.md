# Round 43 review index

## Immutable publication unit

- `ROUND43_REVISION.tex` — canonical manuscript entry point.
- `round43/*.tex` — every input source, including the new quantitative chapter.
- `round43/SOURCE_MANIFEST.json` — exact SHA-256 and byte-size inventory.
- `ROUND43_LOCAL_VERIFICATION.json` — tests and two-pass build record.

## Referee response packet

- `AUTHOR_RESPONSE_ROUND42.md` — item-by-item response.
- `round43/PROOF_LEDGER.json` — obligation/evidence/check separation.
- `round43/HISTORICAL_REUSE.md` — prior derivations reused and strengthened.
- `ROUND43_READY_FOR_REVIEW.md` — freeze and review instructions.

## Main theorem map

- `thm:abstract-bvm` — nonlinear adaptive random-information quasi-BvM.
- `prop:balanced-contrast` — finite-prefix global empirical contrast.
- `thm:filter-jets` — strong filter derivatives in deterministic separable spaces.
- `thm:jacobi-reconstruction` — complete Weyl--Schur coefficient recovery.
- `thm:jacobi-rate` / `eq:jacobi-posterior-ldp` — full posterior LDP.
- `thm:effective-jacobi-stability` — explicit depth/separation modulus.
- `thm:growing-depth-recovery` — increasing finite-block recovery.
- `cor:weighted-operator-recovery` — weighted operator-norm contraction.
- `thm:adaptive-exploration-floor` — genuinely adaptive exploration floor.
- `thm:honest-jacobi-cylinders` — honest growing-block confidence cylinders.

## Reproduction

```text
python3 -m unittest -v tests/test_round43.py
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
python3 tools/verify_round43.py --check-manifest --check-build
```
