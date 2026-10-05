# Revision 8 proof ledger

All nineteen earlier mathematical core files are retained exactly. New mathematical proofs are restricted to the following four statements, together with explanatory remarks. The source audit counts environments and resolves labels; those syntactic checks do not establish mathematical correctness.

| New statement | Main conclusion | Inputs used | Distinction from stronger unproved claims |
|---|---|---|---|
| `thm:cumulative-return-tail` | `Pr(N_n>L) <= A exp(an-cL)`; fixed-strip moments of the complete record | Actual visit count; `0 <= chi <= 1_Y`; invariant collision probability; `prop:soft-killing`; bounded one-flight record | No independence; coarse linear upper envelope is not the Kac mean; no centered large-deviation rate function claimed |
| `prop:linear-count-budget` | Polynomially weighted TV and Fourier-derivative truncation; linear cutoff on exponential bands | Tail integration; domination by physical collision count; contraction under pushforward | Finite-band transform error, not pointwise raw density or all-branch Jacobian variation |
| `thm:common-renewal` | Actual first-return operators, damped renewal and Schur identities, exact record pairings | Invertibility/recurrence; hard projections on genuine `L^1`; disjoint first-return domains; chronological composition | Boundary convergence is strong, not operator-norm; no anisotropic multiplier claim or spectral gap |
| `thm:common-scale-holomorphy` | Fixed complex tube of holomorphic `L^p -> L^q` operators and strong radius continuity | New cumulative exponential moments; Holder inequality; Taylor remainder domination; backward finite-itinerary stability; uniform integrability | Different Lebesgue exponents, not one-space analytic perturbation; no operator-norm radius continuity or spectral theorem |

## Dependency chain

Collision spectral input -> smooth killing -> actual visit-count comparison -> cumulative record exponential moments -> fixed complex Lebesgue-scale realization. Independently, actual first-return domain decomposition -> exact renewal identity -> identification with the physical record. The new finite-band budget also follows directly from the cumulative count tail.

The independent raw-density chain still requires the exact critical/singular decomposition and its global variation sums. The low-frequency covariance and high-frequency anisotropic reconstruction criteria retained in the manuscript are not discharged by the existence of the Lebesgue realization.

## Diagnostic scope

The added finite model checks use rational matrix identities on invertible periodic systems with unequal return times. They check the chronological order, first-return projection formula, Schur/renewal inverse, exact n-return pairing, deterministic soft-count comparison, and cutoff algebra. They are not simulations of the continuum billiard theorem. The tests use explicit exception-raising checks, also run under optimized Python, and never report full LLT or independent-review completion.
