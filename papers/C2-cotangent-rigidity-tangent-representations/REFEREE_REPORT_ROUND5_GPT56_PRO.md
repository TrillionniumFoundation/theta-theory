# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations Across Deterministic Platforms*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `c77f7ed52e6b5d47a12f23ae29174ef9bef8a9e2`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/C2_HISTORY_LIKELIHOOD_DOOB_INTERTWINING.tex`, blob `416437e77122dbc5b4f328586ab6de5eb5192431`

## Source-control verdict

The active C2 paper is unchanged from round four. It still treats a finite slow coordinate as Markov before homogenization and differentiates a statewise normalized Feynman–Kac ratio as though it were the Doob semigroup.

The round-five packet is not materialized. It correctly defines finite likelihoods as conditional expectations in the full resolved-history filtration and writes an actual eigenfunction Doob transform. However its strict-dual theorem lacks the necessary rate coercivity, its conditional-kernel Markovization imports a theorem not proved in A4, and its memory/likelihood diagrams remain ill typed or conditional.

## Audit of the proposed round-five replacement

### 1. Goodness of the rate does not make pressure finite for weighted unbounded sources

The candidate chooses a weight `W` with compact sublevels and defines sources satisfying `F/W -> 0` at weighted infinity. It then states, for any good platform rate,

\[
Q(F)=\sup_\nu\{\nu(F)-I(\nu)\}
\]

is continuous on bounded source sets and has a compact maximizing phase set.

This is false without a coercive inequality relating the rate to the `W`-moment, such as

\[
I(\nu)\ge a\nu(W)-b.
\]

Goodness in the underlying weak topology does not imply exponential integrability of `W`, finiteness of `Q(F)`, or uniform `W`-moment bounds for maximizing sequences. The round-four version explicitly imposed a source-domain/coercivity condition; the candidate has dropped it.

### 2. The candidate source itself contains another control character

The displayed exponential-approximation condition in the exact candidate blob contains an ASCII control byte between `P_` and `epsilon`. The branch workflow stopped earlier on the A1 control byte, so this second invalid source was never reached by the materializer. The packet has no clean TeX or exact-source certificate.

### 3. The conditional-kernel theorem is not an output of A4

The candidate assumes that A4 supplies kernels `K_t^epsilon(h,.)` satisfying uniform convergence on compact history sets to a diffusion transition kernel depending only on the present slow coordinate. The A4 packet states an enhanced invariance principle and a history coupling estimate; it does not prove this uniform conditional invariance principle.

Ordinary weak convergence of slow paths does not imply convergence of conditional expectations or optional projections. Such convergence generally requires stable convergence, a quenched/conditional limit theorem, or a semigroup convergence theorem uniform over histories. The proof’s truncation of the remote past does not establish the finite-history conditional diffusion limit.

### 4. The optional projection is not necessarily an endpoint transition kernel

The theorem writes

\[
K_{T-t}^\varepsilon F(h)
\]

for a “terminal functional” `F`. If `F` depends on the future path rather than only the endpoint slow state, the diffusion comparison requires a path-kernel on an enlarged state, not the endpoint transition semigroup. The functional class and Markov state are not specified.

### 5. The memory pairing is still not correctly typed

The formula

\[
\int_0^\infty e^{-zt}
D\mathcal E_t(0)[A](B)dt
\]

treats the derivative in direction `A` as though it were a bilinear form evaluated at `B`. The derivative is a function `P-tilde_t A`; one must explicitly pair it with `B` in a declared Hilbert space.

The candidate later inserts an inner product on the right, but does not define the corresponding left pairing, domains, or the relationship between the history Feller space and `L2(nu_D)`. This is not a cosmetic notation issue because the projection and compressed inverse depend on the chosen Hilbert structure.

### 6. Similarity does not automatically preserve the A4 memory construction claimed

The candidate sets

\[
P^D=U^{-1}PU
\]

and calls it a projection in an “equivalent eigenmeasure Hilbert norm.” It must prove that `U` is bounded with bounded inverse on the relevant domains, that `P^D` is the orthogonal projection for the transformed inner product, and that the compressed resolvent is invertible on the entire half-plane used for memory. None of this follows merely from the formal generator similarity.

Moreover A4’s memory theorem is constructed for a prepared Koopman group, while the tilted Feynman–Kac generator is not a unitary Koopman generator. A separate Volterra/domain theorem is required after the Doob transformation.

### 7. Exact finite likelihoods are correct, but their diffusion convergence is unproved

The normalized conditional expectation

\[
M_t^\varepsilon=
\frac{E[e^{\theta\Phi(X_T^\varepsilon)}\mid\mathcal F_t^{hist}]}
{E e^{\theta\Phi(X_T^\varepsilon)}}
\]

is indeed a mean-one martingale. This is a genuine correction. Passing it to a stochastic exponential requires the missing conditional-kernel convergence and uniform integrability on the path filtration. A bounded terminal payoff gives uniform integrability of each martingale, but not convergence of the martingale process under changing filtrations.

### 8. The Girsanov/BSDE theorem lacks analytic hypotheses

The candidate calls `u` a bounded classical solution and applies Ito’s formula. This requires regularity and nondegeneracy assumptions on `b_Gamma`, `sigma`, and the terminal data, together with a well-posed diffusion. They are not stated. If the limiting covariance is degenerate, the claimed gradient representation and bounded derivative need not hold.

### 9. Every model-specific component remains downstream of open papers

The strict path rate comes from A3/B2, the history eigenfunction and conditional limit from A4, and the process Gaussian tangent from B3. Those inputs are not proved. C2 remains a synthesis of desired correspondences rather than an independent theorem.

## Genuine improvement

The candidate correctly keeps physical platforms disjoint, defines finite likelihoods in the full history filtration, and uses the genuine eigenfunction Doob semigroup for pressure tangents. These are important corrections to the active paper. They do not establish the conditional homogenization, strict dual, or memory intertwining.

## Required reconstruction

The authors must restore an explicit rate-coercivity/source-domain hypothesis, prove a quenched or stable conditional homogenization theorem on history states, and type the memory identity in one Hilbert space with a transformed orthogonal projection. The diffusion regularity assumptions and functional class must be stated before Girsanov or BSDE conclusions are drawn.

## Recommendation

**Reject.** The active manuscript retains the round-four category errors. The unmaterialized candidate fixes the formal Doob normalization but assumes an unavailable conditional-kernel theorem, drops the coercivity needed for weighted pressure, and does not construct the Hilbert-space memory intertwining or process likelihood convergence.