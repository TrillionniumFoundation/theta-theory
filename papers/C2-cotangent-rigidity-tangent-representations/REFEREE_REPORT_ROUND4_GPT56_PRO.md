# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `c77f7ed52e6b5d47a12f23ae29174ef9bef8a9e2`

## Overall assessment

The revision correctly replaces the former “one universal parent rate” rhetoric by a platform-labelled coproduct and adds an explicit coercive source domain for the weighted-strict pressure. These changes fix a major category error.

The central stochastic representation theorem is nevertheless based on a false finite-volume Markov identity for the resolved slow coordinate. The memory section also reintroduces the old state-dependent Feynman--Kac normalization and identifies its derivative with a Doob semigroup, which is algebraically incorrect unless the Doob eigenfunction is constant. Consequently the claimed likelihood, Girsanov, BSDE, and memory-pressure commutation diagrams are not proved.

## Major objections

### 1. The prelimit resolved coordinate is not Markov

The manuscript defines

\[
\mathcal G_t^\varepsilon
=\sigma(X_s^\varepsilon:0\le s\le t)
\]

and asserts

\[
\mathbb E[F(X_T^\varepsilon)\mid\mathcal G_t^\varepsilon]
=P_{t,T}^\varepsilon F(X_t^\varepsilon).
\]

But A4's own premise is that the exact sufficient state is the complete resolved history, not the present value `X_t^epsilon`. A slow coordinate of a deterministic chaotic system is generally non-Markov at finite `epsilon`; its conditional future depends on unresolved variables and on its past.

The paper neither defines a state-valued Markov process whose current state is `X_t^epsilon` nor proves an exact sufficient-statistic theorem. Therefore the displayed equality is false in general.

At most one could write

\[
\mathbb E[F(X_T^\varepsilon)\mid\mathcal G_t^\varepsilon]
=K_{t,T}^\varepsilon(H_t^\varepsilon,F)
\]

for a history kernel, and then prove asymptotic Markovization. That theorem is missing.

### 2. The finite likelihood process need not be a martingale

The manuscript defines

\[
M_t^\varepsilon
=\frac{P_{t,T}^\varepsilon(e^{\theta\Phi})(X_t^\varepsilon)}
{P_{0,T}^\varepsilon(e^{\theta\Phi})(X_0^\varepsilon)}.
\]

Without the Markov/conditional-expectation identity above, the numerator is not the optional projection of the terminal exponential and `M_t^epsilon` need not be a martingale or have expectation one.

Thus uniform integrability and convergence to a stochastic exponential cannot be inferred from kernel convergence. The object being called a likelihood ratio is not shown to define a probability change of measure.

### 3. Semigroup convergence does not imply filtration convergence

Even if one had convergence of transition semigroups for deterministic initial states, it would not automatically imply convergence of conditional expectations with respect to the natural filtrations. Filtration convergence requires stable convergence, convergence of optional projections, or a martingale-problem theorem with uniqueness and compatible initial laws.

The proof's invocation of “uniform kernel convergence and process convergence” is circular because the prelimit kernels on the present state have not been constructed. Aldous' criterion for the purported conditional martingales also presupposes they are martingales.

### 4. The memory section uses the wrong nonlinear normalization

The paper defines

\[
\mathcal E_t^\Psi F
=\log P_t^\Psi(e^F)-\log P_t^\Psi\mathbf1
\]

and asserts

\[
D\mathcal E_t^\Psi(0)A=P_t^{\Psi,\mathrm D}A,
\]

where `P^{Psi,D}` is the normalized Doob semigroup.

Direct differentiation gives

\[
D\mathcal E_t^\Psi(0)A
=\frac{P_t^\Psi A}{P_t^\Psi\mathbf1}.
\]

The genuine Doob semigroup from A4 is

\[
\widetilde P_t^\Psi A
=e^{-\lambda_\Psi t}h_\Psi^{-1}P_t^\Psi(h_\Psi A).
\]

These are not equal unless `h_Psi` is constant and `P_t^Psi 1=e^{lambda t}` statewise. No such condition is assumed. The statement that division by `P_t^Psi 1` is “exactly the Doob normalization” is false.

Therefore the pressure-tangent/memory theorem is algebraically invalid.

### 5. The memory operator is changed without justification

A4's compressed-memory construction begins with the prepared Koopman group on `L^2(nu)` and an orthogonal projection. C2 instead uses a normalized Doob history Markov generator `L_Psi^D`. These are different operators on different state spaces and inner products.

A similarity/Doob transformation may relate selected transfer operators, but the manuscript does not construct a unitary or bounded intertwining map identifying the two compressed resolvents. Hence saying the two memory constructions “give the same operator” is unsupported even after correcting the derivative formula.

### 6. The weighted-strict dual theorem needs a more precise state space

The coercive restriction is a welcome improvement. However, the proof assumes that the path space is Polish, the weight has compact sublevels, and rate sublevels are compact in the weighted topology for every platform. These facts are not proved for the hard-sphere density/collision path space or for the A1 cut-port completion.

The claim that the dual is exactly all finite-`W` Radon measures depends on the precise mixed topology; the manuscript gives a verbal definition but not a complete locally convex construction. This is repairable, but it cannot be treated as a universal theorem without checking each platform.

### 7. The pressure-response theorem remains conditional on A2/B2

The Green--Kubo formula for the Sinai platform requires the unproved A2 spectral/LLT packet, and the hard-sphere derivative theorem requires B2/B3. The paper is a synthesis, not an independent source of these derivatives.

### 8. Entropic rigidity is standard and the calibration remains an added axiom

The CARA classification is a known consequence of strong assumptions on one utility-generated certainty equivalent. Matching the coefficient to the mechanical field follows only after requiring equality of likelihood cocycles. This is an operational convention/theorem under an extra axiom, not an unconditional mechanical selection principle.

### 9. The platform functor is mathematically correct but largely definitional

Once each platform has a proved LDP and a continuous map, the contraction principle applies componentwise. The coproduct construction prevents category mistakes but does not itself provide a top-four-level theorem. The hard work remains in A1--A4 and B1--B4, where the gates are open.

## Status of previous objections

The platform-label error and the unbounded source-domain issue are materially improved. The current fatal defects arise in the new likelihood and memory interfaces, where the paper reverts from exact history states to an unproved present-state Markov kernel and from a true Doob transform to statewise normalization.

## Minimum viable reconstruction

A valid representation theorem must:

1. retain the complete prelimit history state and its transition kernel;
2. prove asymptotic Markovization of the slow coordinate, including convergence of optional projections;
3. define finite likelihoods as exact conditional-expectation martingales;
4. use the actual Doob transform with eigenfunction `h_Psi` throughout;
5. identify precisely which generator and Hilbert space enter the compressed memory; and
6. prove an intertwining theorem before claiming memory-pressure commutation.

## Recommendation

**Reject.** The revision fixes the cross-platform typing but its two headline representation diagrams rest on false Markov and Doob-normalization identities.