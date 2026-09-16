# Validation scope for A2 revision 67

## Completed source and finite algebraic checks

The downloaded v66 native ZIP has SHA-256 `81998d447b67fba243b860d639b68e31876a1d8f048f0941c8c2bd41cf628876`. Its 837 frozen manuscript files reproduce subtree `c693d717577dc5f501f2a86ec937cfa36bf6ce4e` with recorded Git modes. This is the actual source identified by the latest report.

Run:

```sh
python tools/check_revision_v67.py
python -O tools/check_revision_v67.py
```

Both executions have passed and produced byte-identical JSON. The program uses `require` checks rather than optimization-removable assertions. It imports no earlier diagnostic and uses exact rational arithmetic, with exact squaring for the irrational stopping-error control. It verifies preservation of all inherited paths and active inputs, the original labels in the corrected module, 64 positive periodic quadratic configurations (periods 2--9), 832 first-increment bounds, 832 residual bounds, 832 inexact-evaluation bounds, 768 positive-image stopping certificates, 64 two-point data bounds and 256 signed block norm/Lipschitz controls. Nonimage and nonmonotone cases are included. The R66-m1 counterexample and a sufficient cubic propagation constant are reproduced.

These are finite diagnostics, not proofs of arbitrary-order factorization, infinite-dimensional inversion, global billiard realization or statistical risk. The new fixed-order propagation estimate is proved directly in `article/10c_global_curvature_inverse_v66.tex`. No claim is made to have freshly certified all inherited mathematics.

## Native build and publication protocol

`tools/build_revision_v67.py` reuses the retained source-pinned three-entry engine and adds the new diagnostic. It freezes the actual Git source, checks source graphs and imported companion/full auxiliaries, runs diagnostics in normal and optimized Python, and rebuilds every PDF with shell escape disabled and fresh auxiliaries. It records source commit/tree, all file hashes, raw logs and native products.

`tools/retain_native_v67.py` verifies and retains these products in `deliveries/a2-v67/<actual-source-commit>/`. Publication is established only by reading the pushed Git blobs and recording `COMMITTED_OBJECTS_VERIFIED.json`, not by a filesystem copy alone. The final review-ready index records the completed native run, product commit, PDF page counts and actual visual coverage. This source document does not anticipate a successful future build or claim inspection not yet performed.

All 837 inherited paths are retained; 829 are unchanged in place, eight edited originals are archived byte-exactly. The active graph is unchanged at 134 files. Retention counts concern files, not independent theorems. The full manuscript and companion are retained alongside the principal article.
