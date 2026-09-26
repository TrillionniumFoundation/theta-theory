# Proof dependencies — A2 v167

The complete theorem/page lookup is `THEOREM_INDEX_V167.json`, generated only from compiled auxiliary files.

## Main chain

Gotzmann regularity and classical graph Rees algebra -> explicit evaluation matrix -> `thm:determinantal-v167` -> `prop:jet-v167` and `prop:smith-v167` -> `thm:finite-fan-v167`.

The first arrow is an attributed classical input. Finite residue cancellation is proved by an explicit ordered-support partition, not by assuming generic coefficients.

## Geometric evaluation of the main theorem

`thm:determinantal-v167` + the 13 row ideals of the slice matrix -> `eq:slice-minors-v167` -> `thm:two-wall-v167`.

The inherited division and Hilbert–Burch families verify the displayed universal curves. The exact blow-up identification uses the determinant ideal, not a proper-birational-isomorphism shortcut.

`thm:two-wall-v167` -> `cor:slice-chambers-v167` -> `prop:slice-geometry-v167` and `cor:no-uniform-v167`.

## Parameter-family comparison

Relative Hilbert representability + `lem:density-v167` -> `thm:basechange-v167`; schematic diagonal closure -> `prop:refinement-v167`. The nonflat restriction in `ex:basechange-v167` distinguishes strict and full pullback. No compatibility is inferred across different generic Hilbert polynomials.

## Inherited local algebra

`thm:extension-class-v166` -> explicit presentation and overlap clarification in `sec:local-algebra-v167`.

`thm:ramified-v166` -> `prop:no-saturation-bound-v167`, `prop:toric-classes-v167`, and `lem:normalization-gluing-v167`.

## Paper I dependency boundary

The sharp inverse and effective reconstruction are inputs to `cor:effective-states-v167`, not consequences of any Hilbert-boundary theorem. That corollary also uses `thm:determinantal-v167` and the retained fixed-target comparison. There is no circular use of Paper II to prove Paper I's inverse. No independent proof audit is asserted.
