# A2 v25 — effective local recognition

Qian Qi · 3 October 2026

**Primary article:** *Reference-free certification from intrinsic boundary laws*, `main.tex`. The actual local primary build has **22 pages**. The controlling referee report is the v24 report at `3aeea88879dbba28a7564e3c5787ce293e3a45c8`, reviewing author commit `f5754f7eacc5b2bde9450de154a4e4c0093b3e23`. The mathematical checkpoint was published first at `a5293ca684337b184ba4637cba2c223c684a61ea`.

## Reading route

Theorem 1.1 retains local acquisition and whole-table certification, with a consistently chosen stopping-tail exponent `a >= 6`. Theorem 1.2 summarizes the additional effective-recognition and value-access results.

Lemma 2.1 supplies the topology behind the finite-fingerprint compactness argument, including changing lattice representatives and basis walls. Theorem 3.4 computes a finite jet order, separation threshold and a value-only fingerprint from numerical analytic and geometric priors. Its continuation exponent, error budget and physical-copy separation are proved explicitly. The constants can be very conservative; a compact symbolic representation of a huge fingerprint is not its physical acquisition.

Theorem 5.2 constructs the same periodic local records from certified boundary-height values and distance-to-solid enclosures. Derivatives and intrinsic arclength are computed with bounded errors rather than supplied by the sensor. Chart coverage, numerical regularity and distance access remain assumptions: this is not passive unmarked-trajectory reconstruction. The proof counts local measurements separately from launches and explains the sufficient expected-cost condition `a > 5 + 3*s_v` when a value query of accuracy epsilon costs at most `C*epsilon^(-s_v)`.

`RESPONSE_TO_REFEREES.md` maps the referee's concrete comments and information-category objections to these changes. `PROOF_LEDGER.md` separates mathematical claims from finite diagnostics. The title, billiard-boundary-law subject and requested leading-mathematics-journal target are unchanged; no editorial outcome is asserted.

## Preservation

The complete reviewed v24 native tree is supplied unchanged at `retained/v24`, tree `3d729a1fe93e2250cd68494d149fbb6e90b4096e`. Its nested v23, v22, v21 and v18 companions remain intact. The original smooth Supplement S and its auxiliary document remain at `complete`, tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

All six v24 core chapters remain active in this primary. Three of them—local acquisition, inverse/certificate, and noisy stopping—are byte-identical. Changes to the other three are additions and the explicitly identified tail correction. The full original versions also remain in the exact snapshot. Existing papers, review files and other repository paths are not rewritten.

## Reproduction

Use Python 3.10+, LaTeX with amsart/Latin Modern/microtype/needspace, latexmk and Poppler pdfinfo. Full inherited qualification additionally needs NumPy and SciPy.

```sh
python3 tools/calibrate_fingerprint.py examples/numerical_bounds.json
python3 tools/validate_v25.py
# In an actual clean checkout of this revision, with retained volumes:
python3 tools/validate_v25.py --all-volumes --require-checkout
```

The example contains exact rational prior bounds for illustrating arithmetic. Its physical realizability is not asserted. The calibrator retains enormous integers and tiny thresholds as exact symbolic expressions, not floating-point zero.

## Actual evidence and its scope

The actual local run passed **5,490 finite checks**, with identical ordinary and optimized Python output. The 22-page primary compiled with no final TeX warnings, undefined references, or overfull/underfull boxes. All rendered pages were inspected, including the final literature-page update. The mathematical/tool manifest remained unchanged.

This was **source-content execution, not an authenticated Git checkout**. It did not execute a physical sensor or rebuild the retained volumes. `verification/local/receipt.json` records null checkout/run fields and actual commands, exits and digests. `verification/local/logs.zip` contains the seven raw command logs named in that receipt; their individual SHA-256 values are retained there. `SOURCE_PINS.json` and `PUBLICATION_BINDING.json` bind the checked sources to their native Git objects and the actual local PDF.

The read-only v25 workflow checks out its exact triggering commit and requalifies the primary and all declared inherited volumes. It preserves the old raw-layout diagnostics and disclosed staging-only wrappers. A workflow definition or queued run is not a successful hosted build. Consult the actual run associated with the final branch SHA; this document does not assert a hosted v25 success. The successful v24 run remains historical evidence for v24 only.

Finite checks, compilation and layout inspection are not independent proof certification, exhaustive priority verification or journal acceptance.
