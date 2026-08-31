# Independent Referee Report — Round 12

**Manuscript:** A3 — *Full Empirical-Path LDP*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `d5431238029e984337529e2f216c2cf12c419d9a54333f869d8b3d0fd7da87de`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 fixes several important typing errors: collision and physical horizons are deterministic, the terminal incomplete excursion is retained, the original countable renewal kernel is not replaced by a non-lumpable cemetery chain, and one-big-excursion profiles are included in the state.

The new proof nevertheless contains a direct false statement at its singularity-shield interface. A relative-entropy budget of order \(n\) does not preserve exponential rarity uniformly over all controlled laws of cost at most order \(n\). A control can spend part of its entropy budget to raise an exponentially rare event to constant probability. This invalidates Lemma 4.2 and the claimed exponentially good approximation on which the full path-space upper and lower bounds rely. The controlled-rate definition and physical-clock formula also remain insufficiently specified.

## Decisive objections

### 1. The controlled singularity shield contradicts the entropy inequality

Lemma 4.2 claims that, for every cost bound \(M\), one can choose a shield so that uniformly over all controls with entropy cost at most \(Mn\),

\[
Q_n(A_n)\le e^{-Mn},
\]

where \(A_n\) is the event that the shielded and actual profiles differ appreciably.

This is impossible for an event whose reference probability is merely exponential. Suppose

\[
P_n(A_n)=e^{-Ln+o(n)}
\]

with finite \(L>0\). For any fixed

\[
0<q<\min\{1,M/L\},
\]

define

\[
Q_n=qP_n(\cdot\mid A_n)+(1-q)P_n(\cdot\mid A_n^c).
\]

Then

\[
D(Q_n\Vert P_n)=qLn+O(1)\le Mn
\]

for large \(n\), but

\[
Q_n(A_n)=q,
\]

a positive constant. In the extreme case \(L\le M\), conditioning entirely on \(A_n\) already has cost at most \(Mn\).

Thus an order-\(n\) entropy-control class can promote any finite-rate event to macroscopic probability. The sentence “entropy inequality transfers this estimate uniformly to every bounded-cost control” is false. To obtain uniform exponential approximation, one would need a superexponential reference error or a control class with sublinear entropy budget; neither is present.

### 2. This false lemma is load bearing for the path-space LDP

The actual factor map through billiard singularities is discontinuous. The proof uses Lemma 4.2 to replace it by continuous shielded profile maps uniformly on rate sublevels. Since the lemma fails, the extended contraction principle cannot be applied as stated, and neither the projective upper bound nor the recovery construction has been transferred to the physical path topology.

Retaining a singularity-exposure coordinate is a useful idea, but the paper must incorporate its finite cost into the rate. It cannot declare all remaining shield errors exponentially negligible under every finite-cost control.

### 3. The exact control representation is not fully defined at the stopped residual

Theorem 2.1 introduces both predictable transition kernels \(Q_j\) and a separate terminal residual kernel \(Q_{\rm term}\). At a deterministic collision horizon, however, the terminal excursion and its age are determined jointly by the next controlled branch and its length. They are not an independent terminal draw unless a precise disintegration of the stopped path law is given.

The manuscript does not specify:

- the reference residual kernel \(P_{\rm term}\);
- the sigma-field on which it is conditioned;
- how it is coupled to the transition that selected \(A_{N(n)}\); or
- why adding its relative entropy does not double-count the last branch likelihood.

Without this construction, the displayed equality is not an exact variational identity.

### 4. The proposed rate is not shown to be a fixed good rate function

The rate is defined by

\[
I^c(\lambda)
=
\inf_{\mathbf Q:\mathcal L(\mathbf Q)=\lambda}
\liminf_{n\to\infty}
\frac1nE_{\mathbf Q}[\text{entropy cost}].
\]

Here the admissible control may depend on \(n\), and the notation \(\mathcal L(\mathbf Q)=\lambda\) is not defined for a sequence of stopped controlled laws. No proof establishes lower semicontinuity, compact sublevels, or equality with the convex dual of the Laplace functional.

The statement “the entropy representation gives the Laplace upper bound” omits the weak-convergence/control compactness theorem that is the main content of such an approach. A variational formula for each \(n\) is not itself an LDP.

### 5. Uniform Harris input is assumed rather than inherited from a tower tail

The manuscript assumes

\[
\sup_a\sum_bP(a,b)e^{\eta(r(b)+\mathfrak t(b))}<\infty.
\]

An exponential return tail under the stationary Gibbs measure does not automatically imply a uniform exponential moment over every current branch \(a\). The drift proof and all source-uniform controls depend on this stronger estimate. It must be proved from the actual transition kernel and distortion constants.

### 6. The one-excursion epigraph is not justified by exponential moments

“Exponential clock moments give epigraph compactness” is not a valid compactness argument for normalized path profiles. Long excursions can exhibit increasingly complicated singularity patterns while their normalized clocks remain bounded. A topology on the normalized profile space, tightness of all path-window coordinates, and closure of admissible first-return profiles are required.

Moreover, the scalar cost

\[
-r(a)^{-1}\log P(a\mid\text{entrance})
\]

is not defined for a general Markov-renewal kernel without specifying the entrance state. Transition and exit costs are negligible only after a proved uniform comparison.

### 7. The physical-clock rate is not simply “divided by the controlled mean” for nonstationary controls

The admissible controls are predictable and may vary with time and history. Such a control need not have a single controlled mean roof. The physical-time rate requires a joint occupation/clock control theorem and a deterministic stopping analysis, not a formal division by one mean. The final proof says “repeat the entropy representation,” but none of the residual and tightness details are supplied.

### 8. A2 remains an open upstream gate

The paper uses A2 for inserted spectral coefficients and singularity shielding. A2's small- and high-frequency theorems remain invalid in Round 12, so even a corrected control argument could not presently invoke them as established inputs.

## Genuine improvements recognized

The following changes should be retained:

- deterministic collision and physical speeds;
- explicit retention of the terminal excursion and flight age;
- use of the original countable renewal kernel rather than a cemetery Markovization;
- inclusion of normalized long-excursion profiles; and
- separation of positive recurrence from strong positive recurrence.

## Required reconstruction

A viable paper must prove a weak-convergence LDP theorem for the stopped Markov-renewal process on a precisely defined Polish state. Singularity exposure must remain an explicit rate coordinate under controlled laws; it cannot be removed by the false uniform shield. The terminal residual must be part of one exact stopped-path disintegration, and the physical-clock theorem must be proved as a second deterministic stopping problem.

## Recommendation

**Reject.** The new deterministic-clock architecture is better typed, but the singularity approximation is contradicted by an elementary relative-entropy construction. The full good path LDP and its physical-time version therefore remain unproved.