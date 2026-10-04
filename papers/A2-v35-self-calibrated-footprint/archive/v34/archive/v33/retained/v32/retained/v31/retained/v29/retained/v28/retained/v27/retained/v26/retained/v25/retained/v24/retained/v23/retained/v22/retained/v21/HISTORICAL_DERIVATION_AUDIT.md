# Historical derivations used in A2 v21

## Controlling sources

The latest review is `40e9f1beaf49bf7f870f2f6f73ac027feab1a84e`; its report blob is `d5adb7728eff4dbc8d69cf07937de73b5ecb445f`. It reviews v20 author commit `c376e802e6e86735888dcd685f987c7a8f475903`, not the older v18/v19 sources discussed earlier. The new revision branch starts from that review head.

The complete v20 paper tree is `3b34e4156b3ff621df9c1a3fb8aece4c66f1f07b`. Its exact copy at `history/v20-reviewed` retains the old proofs, responses, source bindings, local evidence and all nested history. The current primary also reuses all six v20 core files byte-for-byte, tree `2bfb749b8dd15464e96fdf252cb09b4ad5794165`, with two additional active chapters.

## Mathematical dependencies actually consulted

`01_setting.tex` fixes the raw phase normalization, local arclength record, global shape assumptions, unlabelled collection, covolume calibration and distinction between partial and complete catalogues. The new acquisition protocol expressly inherits this normalization rather than replacing it by conditioning on a finite scan disk.

`02_local.tex` gives the residual-time affine density, action/normalization equivalence, stationary Schur-complement curvature formulas and the physical C3 Lipschitz comparison. These arguments supply each pair image used in the new deduplication and witness selection. The earlier full-law development is preserved in Supplement R, especially its two-window chapter.

`03_descent.tex` gives analytic-image equality, unique matching of asymmetric complete images, tree placement, geometric cycle vectors, calibrated volume and finite-index physical ambiguity. The new key lemma specializes its matching argument to translations within one table. The ambiguity examples remain relevant when witness retention or sufficient acquisition fails.

`04_stability.tex` gives the physical compact prior, cell-average reconstruction, variance-aware Bernstein bound, continuation exponent, shape matching and integer locking. The new witness theorem changes which channels must persist; it retains this density-to-geometry proof and its rate rather than claiming an independent minimax theorem.

`06_canonical.tex` gives obstruction descent, the covering-radius connectedness theorem, all-cycle determinantal index, the 2/3/5 example and stable saturation. The aperture bound uses its connected quotient; sparse extraction uses its all-cycle index; persistence uses fixed integer cycle generators in a deformation chart. The new gap-relative proposition credits the classical proximity mechanism and reuses the direct periodic descent/lifting proof.

`05_comparison.tex` retains the boundary-distance/lens/travelling-time comparisons and separates moment compression, full histograms, counts and smooth relative laws. The new proximity and visibility discussion supplements rather than replaces those comparisons.

## Preservation of the earlier program

Supplement R is the whole v18 source tree `3c558d7799e9e49812e7bab98320d3a98e7f7418` at `retained/v18`. Supplement S remains tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda` at `complete`, also included within R. The earlier historical derivation ledgers are preserved, not silently recast as a new exhaustive audit. No claim is made that every inherited proof has been independently re-proved in this revision.
