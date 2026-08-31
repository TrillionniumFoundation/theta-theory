# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `e4fb6c3c1489cb08ef81c4eab3924a8204324006`

## Executive assessment

Round eight correctly abandons a common zero-free complex neighborhood at coexistence and correctly notes that the conjugate of a maximum of pressures is not generally the minimum of the phase conjugates. It tries to recover the minimum-rate formula from an explicit microscopic phase mixture instead.

The central mixture hypothesis is not proved for either platform, and even as an abstract theorem it is insufficient. A remainder of total variation `e^{-c mu}` is only exponentially small, not superexponentially small. It can change every rate value above `c`, and under exponential source weights it can change the pressure. The theorem therefore cannot conclude a full LDP with rate `min_j I_j`. The phase-restricted positive laws and boundary-face lower bounds are themselves assumed rather than constructed. What remains is a standard conditional mixture lemma, not an independent top-four paper.

## Genuine repairs recognized

The paper should retain:

- phase-specific finite-volume laws rather than logarithm branches of one partition function at coexistence;
- explicit permission for Lee–Yang zeros to pinch the real axis;
- exact finite-volume centering of local likelihoods;
- phase-wise contraction before minimization;
- the warning that `(max Q_j)^*` need not equal `min Q_j^*`.

## Major mathematical objections

### 1. An `e^{-c mu}` remainder is not negligible for a full LDP

The assumed decomposition is

\[
P_\varepsilon
=\sum_jw_{\varepsilon,j}P_{\varepsilon,j}
+R_\varepsilon,
\qquad
\|R_\varepsilon\|\le e^{-c\mu_\varepsilon}.
\]

Suppose a closed set `F` has phase rates

\[
\inf_F I_j>2c
\]

for every `j`, while the remainder places mass `e^{-c mu}` on `F`. Then the physical probability of `F` has rate at most `c`, not `min_j inf_F I_j`.

A fixed exponential remainder is negligible only below its own rate threshold. To preserve an unrestricted full LDP it must be superexponentially small, or its own support/rate must be included as an additional phase.

The proof's phrase “the signed remainder is exponentially negligible” is therefore false in the large-deviation sense needed here.

### 2. Total-variation control does not preserve the pressure on arbitrary source charts

For a bounded projection `X` and source `theta`, the remainder contribution to the moment generating function is bounded by

\[
e^{-c\mu}e^{\mu\sup\theta\cdot X}.
\]

It can dominate if the source reward exceeds `c`. Total-variation smallness alone does not imply

\[
Q=\max_jQ_j
\]

on all finite source charts. One needs a source-weighted superexponential bound or a radius restriction tied to `c`.

For unbounded weighted observables the problem is worse.

### 3. Positive phase-restricted laws are not constructed

The paper allows phases to be defined by “metastable boundary conditions or spectral phase projectors.” A Riesz projector of a non-self-adjoint transfer operator is not generally positivity preserving and does not automatically define a probability law. Metastable boundary conditions may define positive laws, but their relation to the physical finite-volume law and their subexponential weights must be proved.

No such construction is supplied for the Sinai or hard-sphere platforms. The microscopic mixture is the principal theorem being assumed.

### 4. The phase-wise face LDP does not follow from local analytic charts

Inside a phase, the paper has local analytic pressure only on compact subsets of `U_j`. To reach an exposed support face it sends a normal source to infinity. That sequence generally leaves every compact subset of `U_j`, can approach a phase boundary, and can destroy the isolated eigenvalue.

The assertion that the tangential restricted operator “remains inside phase `j`” is exactly what must be proved. Compact support gives exponential tightness, but it does not supply the local lower bound at boundary faces.

### 5. The rate `I_{m,j}=Q_{m,j}^*` is not justified on the whole phase support

A local phase pressure determines a local exposed branch. Taking its global Legendre conjugate silently extends it beyond the proved source domain. Boundary points, nonexposed points, and phase-edge points require separate recovery theorems. The manuscript names those recoveries but does not construct them.

### 6. Projective minimization and phase selection need a full-space mixture theorem

For finite projections the rate is claimed to be

\[
\min_j I_{m,j}.
\]

The projective rate obtained from these projections is

\[
\sup_m\min_j I_{m,j}(\pi_mx),
\]

which need not equal

\[
\min_j\sup_m I_{m,j}(\pi_mx).
\]

The phase index minimizing a finite projection can change with `m`. Equality follows only if the full path law is already a genuine finite mixture of phase families satisfying full LDPs on the target topology. That is the unproved hypothesis, not a consequence of projective passage.

### 7. The topology-upgrade theorem assumes the desired recovery concentration

The theorem requires every finite-rate point to possess a phase-wise recovery sequence exponentially concentrated in one compact target-topology sublevel. This is the hard lower-bound/topology theorem. Assuming it makes the projective upgrade tautological.

Neither A3 nor B2 proves the required phase-wise compact recovery.

### 8. Thin-shell conditioning inherits invalid A2/B1 coefficients

The phase-stratified conditioning theorem is algebraically reasonable if each phase has a source-uniform sharp shell theorem. The current A2 local-window theorem and B1 mixed coefficient theorem are not valid. D1 cannot treat them as completed interfaces.

### 9. The standalone contribution is a standard conditional lemma

If one assumes positive phase laws, subexponential weights, superexponentially negligible remainder, and full phase-wise LDPs, the minimum-rate mixture theorem is elementary. Contraction and exact local likelihoods are also standard. The paper adds no independent model theorem capable of closing the series.

## Dependency assessment

D1 is the terminal consumer of every unresolved A- and B-series interface. It cannot establish their closure by assuming phase-specific LDPs and mixture recovery. Its valid local identities should be incorporated into the principal platform papers after those platform theorems are proved.

## Required reconstruction

If retained at all, the abstract theorem must require either:

- an exact positive finite mixture; or
- a superexponentially small remainder uniformly under the relevant source tilts.

It must also distinguish finite-projection phase minima from a full-space phase mixture and state explicit conditions under which the infimum and projective supremum commute. Platform-specific papers must construct the phase laws and face recoveries.

## Recommendation

**Reject; remove as a standalone submission.** The coexistence philosophy is improved, but the fixed-rate exponential remainder directly invalidates the claimed full LDP, and every model-specific phase theorem is assumed rather than proved.