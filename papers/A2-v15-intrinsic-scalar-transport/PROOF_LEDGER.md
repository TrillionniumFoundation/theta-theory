# A2 v15 proof and dependency ledger

The classical scalar comparison and the physical identification have separate logical roles. The additions below do not replace any inherited proof.

| Result | Hypotheses and proof route | Source label |
| --- | --- | --- |
| Uniform scalar product, coordinate and iterates | Joint smoothness; common fixed point; positive derivative and strict contraction margins. Differentiate the orbit recurrence, sum the logarithmic cocycle, integrate, prove normalized uniqueness, then use the inverse coordinate for the sharp fixed-order rate. | `lem:v15-scalar-product` |
| Physical determinant/product equality | The existing physical half-line construction and exact Schur concatenation identify the density. Its quotient with the scalar density is invariant and equals one at the fixed point. | `cor:v15-determinant-product` |
| Exact finite logarithmic remainder | Telescope the physical scalar cocycle; compose `log B` with the normalized inverse coordinate to obtain the mixed-norm exponential bound. | `eq:v15-physical-product-remainder` |
| Width/profile equivalence | Differentiate the existing energy-pushforward integral for positive energy and extend the weighted derivative to zero. This is one invariant in two coordinates. | `eq:v15-width-equivalence` |
| Independent-contact inverse | Entire prior section is retained under `lambda -> varrho`, `r_b -> mathfrak r_b`; the block, its strict positivity and recursive inverse do not change. | `thm:v12-two-contact` |

## Retained physical chain

`v3/10_geometry_action.tex` and `v3/20_integration.tex` supply the physical stationary action and residual-time normalization. `v4/10_boundary_layers.tex` constructs the half-line action, its trace-class density and the normalized two-boundary factorization. The differentiated operator and Morse-transport arguments remain active. The original physical cocycle theorem uses these results and exact finite concatenation; the classical scalar lemma alone is not its substitute.

`article/20_boundary_compatibility.tex` supplies the energy pushforward and the full smooth Volterra uniqueness argument. The new width sentence does not replace smooth uniqueness with a Taylor-series argument. The independent-contact, physical-image and two-flight proofs retain their distinct information sets. The Abel inverse, regularized acquisition and separately charged calibration retain their stated norms and class certificates.

## Preservation checks

The 52 original top-level input commands are unchanged and in the same order. The three edited mathematical inputs contain 12 pre-existing theorem/lemma/proposition/corollary/proof blocks; all remain exact after reversing the two documented notation substitutions in the contact section. The new scalar lemma/proof and product corollary/proof add four formal blocks. Every other inherited native file is carried by the original Git tree, not reconstructed from a summary.

The local edited-source check and finite identities were executed. The complete-checkout source traversal is supplied separately and was not executed locally. A Git-tree inheritance guarantee, a line-by-line proof audit, and a formal proof certificate are different kinds of evidence; this ledger does not identify them.
