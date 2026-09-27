# Targeted literature audit — Revision 57

This is an author-side primary-source comparison, not independent or exhaustive priority clearance. The unchanged v56 and earlier audits remain under `retained-v56/`.

## New external inputs and exact scope

**Bourgain–Gamburd, A spectral gap theorem in SU(d), JEMS 14 (2012), 1455–1511, arXiv:1108.6264.** The primary statement assumes a finite algebraic-entry generating family with dense subgroup in SU(d). We use precisely that input with a lazy symmetric law to obtain an absolute L2 contraction on mean-zero functions. The paper does not compute the spectral-gap constant, and no finite word test certifies it. The full matrix orbit has dimension 2(d-1), not d^2-2; the uniform small-ball proof is separate from the imported spectral-gap theorem.

**Breuillard–Gelander, On dense free subgroups of Lie groups, Journal of Algebra 261 (2003), 448–467, arXiv:math/0206236v2.** Theorem 1.1 states that every dense subgroup of a connected semisimple real Lie group contains a dense free subgroup on two generators. Applied to the algebraic-entry subgroup of SU(d), it yields fixed algebraic free generators. The new article proves that a specified transcendental projective line has trivial stabilizer under this group and then derives the exact stochastic width. It does not claim an explicit numerical pair or a free-generator discovery algorithm.

**Breuillard–Gelander, On dense free subgroups of Lie groups—revisited, arXiv:2605.20568 (20 May 2026).** The correction was checked rather than omitted. It repairs an argument in original Proposition 2.7, supplies missing details for Proposition 3.3, and corrects Example 2.2. The authors explicitly state that validity of the original statements is unaffected. We cite the correction alongside the original Theorem 1.1. No inference relies on the erroneous solvable-group commutator argument.

**Szarek, Metric entropy of homogeneous spaces, Banach Center Publications 43 (1998), 395–410, arXiv:math/9701213.** Compact homogeneous-space covering is classical. Our fixed-dimensional Grassmannian cap estimate is proved directly in graph coordinates; the rank-one cap law is computed from normalized complex Gaussian coordinates. No dimension-uniform constant is borrowed without proof. The quadratic support estimate for a smooth orbit hull is also proved directly. We do not claim these geometric ingredients as new entropy theory.

**Ambainis–Freivalds, 1-way quantum finite automata: strengths, weaknesses and generalizations, arXiv:quant-ph/9802062 (1998).** This is a relevant antecedent for state-size advantages in language recognition. The present full-matrix interface differs from an acceptance language: every terminal hidden label must decode to a legal density matrix, the entire output vector is required, and the stochastic competitor can be redesigned at each horizon with a free clock. Our exponential exact endpoint follows from extremality of that legal output set. Enlarging the tomography image to a full unconstrained simplex destroys that argument. These differences delimit claims; they do not certify novelty across all quantum/weighted-automata representations.

## Retained priority boundaries

The compact stochastic-semigroup idempotent and group-corner geometry is classical (Flor/Schwarz); v56's physical kernel averaging and Ramsey clock removal were already present before this continuation. Its neutral-letter/advice comparison, nonnegative-factorization hardness comparison, and group-closure/real-algebraic sources remain in the article and unchanged predecessor audit. No new independent clearance of those full theorem statements is claimed here.

## Remaining scope

The nonabelian rates agree in polynomial exponent but retain a logarithmic lower-bound loss. The exact pure-state formula is not the zero-error scalar planar endpoint. General online/adaptive interfaces and general irreversible radius formulas are not consequences. The finite-precision theorem compiles supplied encoded tables; it does not make arbitrary unencoded reals computable or establish efficient width optimization. Independent human theorem-level comparison remains necessary before any priority assertion.
