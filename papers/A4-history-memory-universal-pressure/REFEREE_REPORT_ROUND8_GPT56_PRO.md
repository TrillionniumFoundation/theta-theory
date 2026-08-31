# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — *History, Memory, and Universal Pressure for Prepared Sinai Paths*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `ef17c3d1c25cca30aa27c548e7eefddf18fa6eb9`

## Executive assessment

Round eight makes two correct conceptual changes. It conditions on the genuine symbolic past rather than on the complete deterministic state or a stable-leaf quotient, and it restores the correct causal sign

\[
\widehat K(z)=zI-A-\widehat C(z)^{-1}.
\]

Those repairs remove direct contradictions from the previous versions.

The new memory theorem is nonetheless false as stated. Analyticity plus polynomial growth of a Laplace transform in a left strip does not imply that its inverse is an exponentially decaying function; even the constant transform has a Dirac mass at time zero. The Riesz–Potapov “exact unresolved-space dilation” is also asserted under positivity/passivity and realization hypotheses not established for the compressed billiard generator, and it confuses a multiplicative transmission-zero factorization with an additive unitary decomposition of the microscopic unresolved space. The conditional rough invariance principle remains a one-paragraph claim far beyond the available A2/A3 input.

## Genuine repairs recognized

The manuscript should preserve:

- the use of the two-sided natural extension and the past sigma-field;
- the explicit statement that complete microscopic history gives a Dirac future;
- construction of the continuous-time kernel before Ray compactification;
- the genuine Doob normalization;
- retention of the antisymmetric rough-area correction;
- the corrected causal memory sign.

## Major mathematical objections

### 1. The residual-memory decay theorem is directly false

The theorem assumes that

\[
\widehat K_{\rm res}(z)
\]

is analytic and polynomially bounded in a half-strip and concludes that the time kernel decays exponentially as an ordinary function.

This implication is false. For example,

\[
\widehat K(z)=1
\]

is entire and polynomially bounded, but its inverse Laplace transform is the distribution \(\delta_0\), not an exponentially decaying function on positive time. Likewise \(\widehat K(z)=z^2\) gives a derivative of a Dirac mass. More generally, polynomial growth on a vertical line gives a distribution of finite order; it does not give an integrable Bromwich integral.

One integration by parts does not repair arbitrary polynomial growth. A valid decay theorem needs quantified vertical decay or sufficiently many integrable derivatives after subtracting all instantaneous distributional terms.

### 2. The Riesz–Potapov extraction is not justified for the declared transfer function

The proof begins by treating

\[
M(z)=PLQ(z-QLQ)^{-1}QLP
\]

as a positive-real/passive transfer with a minimal conservative Hilbert realization. No passivity or positive-real property is proved for the non-self-adjoint Doob/Koopman generator and an arbitrary resolved projection.

The final sentence makes passivity conditional, but the proof has already used it to invoke conservative factorization and unitary realization uniqueness. The theorem therefore relies on a hypothesis absent from its statement and absent from the billiard construction.

### 3. Transmission-zero factorization does not automatically produce the claimed additive microscopic decomposition

A Blaschke–Potapov factorization is generally multiplicative at the transfer level. The manuscript asserts the additive identity

\[
M(z)=M_{\rm res}(z)+C_Z(z-A_Z)^{-1}B_Z
\]

and a unitary state-space decomposition of the actual cyclic unresolved subspace. Such an identity requires a realization theorem with controllability, observability, pole/zero separation, and domain compatibility. It does not follow merely by selecting Riesz projections of zeros of a compressed matrix.

In particular, a transmission zero is not automatically an eigenvalue of a finite invariant subspace of the original unresolved generator. The paper supplies no construction of the unitary map `U` or proof that the unbounded generator domains are preserved.

### 4. The all-real-time Feller statement is underspecified on the countable inducing state

The natural-extension alphabet is countable and the roof is unbounded at the inducing level. Normal convergence of a renewal sum and continuity of each finite term do not by themselves give a Feller semigroup on `C_b` of the weighted past space. The topology, vanishing-at-infinity condition, and uniform tail modulus must be stated.

On a noncompact state space, a Markov semigroup need not be strongly continuous on `C_b`. The Ray theorem also requires a precisely defined resolvent cone and normality/tightness properties, not only formal separation.

### 5. Uniform quenched rough convergence is not obtained from an annealed spectral gap

The proof claims that “the past-kernel transfer operators have the same spectral gap on every compact past chart.” No family of conditional transfer operators, common Banach space, or uniform resolvent is constructed. An annealed Ruelle spectral gap does not automatically imply a quenched rough invariance principle uniformly over initial pasts.

The theorem additionally claims an exceptional set of conditional probability `O(e^{-cL})` without defining `L`, the conditioning law, or how this bound interacts with the compact set. Moment bounds for the iterated integral and stable convergence of conditional kernels require a separate martingale-array theorem.

### 6. The martingale decomposition is only asserted

The displayed increments

\[
D_{n+1}=A\circ\sigma^n+
\chi\circ\sigma^{n+1}-\chi\circ\sigma^n
\]

are martingale differences only if `chi` solves the correctly oriented conditional Poisson equation. The manuscript neither states that equation nor verifies the conditional-mean-zero property under the `g`-kernel. This is essential for the quenched argument.

### 7. Memory is not invariant under a generic bounded Doob conjugacy

The final proof says that the memory Schur complement is invariant under bounded conjugacy. A compressed resolvent depends not only on the generator but also on the Hilbert pairing and projection. Under a Doob transform the invariant measure, orthogonal projection, and resolved subspace generally change. Unless all of them are transported, the compressed memory kernel is not conjugacy invariant.

C2 attempts such a covariant transport, but A4 does not construct it here.

### 8. The paper remains dependent on unresolved A2/A3 inputs

The meromorphic strip, high-frequency resolvent bounds, recurrent Gibbs phase, and conditional path compactness are imported from A2/A3, whose current theorems remain unproved. A4 cannot promote those labels into an exact operator dilation or quenched process theorem.

## Required reconstruction

A viable paper should be divided into two parts:

1. a precise past-kernel Markov/Feller and quenched invariance theorem for a specified Gibbs suspension, with a complete conditional martingale argument; and
2. an abstract compressed-resolvent theorem whose assumptions include the exact high-frequency decay, domain properties, and realization hypotheses needed for an exponential memory kernel.

Instantaneous Dirac terms must be separated before claiming decay, and any finite zero-mode extraction must be proved as an operator realization rather than asserted from transfer-function vocabulary.

## Recommendation

**Reject.** The past-filtration repair is correct, but the central memory-decay theorem has an elementary inverse-Laplace counterexample, and the exact unitary transmission-zero dilation is not constructed for the billiard generator.