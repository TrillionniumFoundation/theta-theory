# A2 v116 proof audit

This records proof dependencies and executed checks, not an independent-referee verdict or a proof-assistant certificate.

## Universal arguments added

| Result | Essential argument | Dependency boundary |
|---|---|---|
| Lemma `lem:triangular-row-filtration` | Monic pivot elimination; row `q` has order at least `q`; explicit nonzero initial minor | Original polynomial multiplication, not generic determinantal dimension counting |
| Lemma `lem:weighted-relation-minors` | Weighted monomial relation columns; induction on `m`; four extremal deficit cases and the exceptional `m=2` step | A proof for every `m`, not extrapolation from Groebner computations |
| Theorem `thm:quartic-primary` | Initial minor spanning, secant-principal ideal containment, Nakayama, faithful flatness | Uses `n=4` critically; does not identify the complete primary ideal for `n>4` |
| Corollary `cor:quartic-infinitesimal-layers` | Cancellation in the regular local ring and the exact product ideal | Determines actual layers, not only their lengths |
| Theorem `thm:conductor-reduction` | `WU=gV_{2n-d}`, then a base-point-free pencil propagation; quotient of a sheaf surjection | Uniform in nonreduced divisors and compatible with base change |
| Lemma `lem:confluent-power-basis` | Monic Newton basis, triangular jet substitution and Cayley--Hamilton | Polynomial identity at collisions and ramification; no division by discriminant |
| Theorem `thm:contact-pencil-primary` | Exact cokernel identification, principal determinant ideal, UFD primary decomposition and frame descent | Specified residue-pencil Grassmannians, not arbitrary ambient subseries |
| Corollary `cor:contact-local-structure` | Completed weighted arrangement and ideal-quotient cancellation | Singularities and nilradical layers on a smooth frame cover, with descent stated up to smooth variables |

The quartic theorem's initial-to-full-ideal step is explicitly proved: the candidate ideal `I=F p^{T-2}` satisfies `J subset I`, and spanning modulo `p I` gives `J+pI=I`; Nakayama yields `J=I`. It is not an identification of schemes from equal tangent spaces. The contact theorem's analogous step uses an actual cokernel isomorphism and Cayley--Hamilton over the coefficient ring, not only set-theoretic corank calculations.

## Expanded v115 arguments

`parts/02j-proof-details.tex` supplies the two explicit diagonal plane-derivative matrices, the split and tangent residual-image calculations, the length-two Hankel radical including a double point, and a precise equivariant associated-point lemma. These supplement rather than replace the archived v115 proof blocks.

## Executed finite diagnostics

`verify_v116.py` reports source preservation, exact quartic residual-minor ideal comparisons for `m=2,3`, six symbolic power-basis determinant identities, 27 rank tests of the **original** multiplication map over the prime field with 1009 elements, and the finite monomial coverage checks through `m=16`. `--extended` adds the full `m=4` Groebner ideal comparison. The original `verify_revision.py` remains active and includes 80 hyperplane rank/polar cases and earlier diagnostics.

All finite tests can expose errors, but none proves a universal theorem by itself. In particular a finite-field rank test is not an assertion about every characteristic or every complex point. The manuscript works over the complex numbers.

## Remaining boundaries

The full Ballico (1993) theorem comparison remains uncompleted because the full theorem pages were not obtained. The full ambient quadratic excess primary decomposition and the full `n>4` hyperplane primary ideal are not claimed. These scope statements are not substitutes for proofs: the new exact quartic and contact-family theorems are the positive content submitted for review.
