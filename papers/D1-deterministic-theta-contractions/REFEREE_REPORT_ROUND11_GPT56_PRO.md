# Independent Referee Report — Round Eleven

**Manuscript:** D1 — Deterministic Theta Contractions  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/D1_SOFT_PHASE_DISINTEGRATION_MIXTURE.tex` (Git blob `de58d065f8deac083c468ad02d66824b84e55390`)

## Executive assessment

Round eleven finally constructs a positive finite-volume label on the original sample space and normalizes conditional phase pressures correctly. The elementary exact mixture identity is valid. The claimed phase-local LDP, zero-free charts, boundary recovery, shell theorem, and commutation theorem do not follow from that identity. They are assumed from the platform papers, which do not construct the required order parameter, soft localization estimates, or component laws.

The manuscript also contains internal inconsistencies: the overlap region is later treated as an additional component although no such label was created, and it says early contraction “convexifies” the rate even though its own contraction formula gives the nonconvex minimum. What remains is a generic finite-mixture lemma rather than a standalone top-journal theorem.

## Major mathematical objections

### 1. The soft labels are arbitrary and the platform phase structure is assumed

The paper begins by assuming an order parameter \(M_n\) whose limiting rate has finitely many isolated compact minimizer components. None of A3 or B1/B2 proves such an order parameter theorem, finiteness, isolation, or the required uniform rate gap. Constructing a partition of unity after assuming these objects does not construct the physical phases.

### 2. Positive localization does not preserve a complex zero-free chart

The component partition function is multiplied by an \(n\)-dependent global weight \(\chi_{n,j}(M_n)\). Although this weight is positive on the real sample space, complex source partition functions can acquire cancellations and zeros arbitrarily close to the real domain. Boundedness \(0\le\chi\le1\) and equality to one near \(K_j\) do not imply a subexponential *relative* error uniformly for complex sources.

Thus the claimed phase-local Riesz/zero-free chart cannot be inherited from the unlocalized platform operator without a new localized spectral theorem.

### 3. Component LDPs do not follow from the exact decomposition

An exact identity

\[
\mathbb P_n=\sum_jw_{n,j}\mathbb P_{n,j}
\]

places no regularity on the conditional laws. The \(n\)-dependent soft weights may be exponentially small on parts of state space or oscillate with \(n\). Full upper/lower bounds, exponential tightness, and boundary-face recovery for every component require independent proofs.

The manuscript instead cites “platform source theorem and soft localization,” which is precisely the missing result.

### 4. The overlap is not a separately constructed component

The label is drawn from \(j=1,\ldots,J\) with probabilities \(\chi_{n,j}\). Points in an overlap are randomized among those existing labels. Later the shell proof says that “the overlap is another positive labelled component with its own cost.” No overlap label or conditional measure was defined. This statement is inconsistent with the exact disintegration.

### 5. Early label contraction does not convexify an LDP rate

The contraction principle applied to a finite labelled rate

\[
\mathcal J(j,x)=\alpha_j+I_j(x)
\]

gives

\[
I(x)=\min_j\{\alpha_j+I_j(x)\},
\]

which may be nonconvex. The manuscript itself states this correctly. It later claims that contracting the label before the LDP “generally convexifies” the rate. That is false; convexification can arise from reconstructing a rate only through a pressure Legendre transform, not from probabilistic label contraction.

### 6. The phase weights of minimizer components are not analyzed

If all \(K_j\) are global minimizer components of one normalized rate, their exponential costs are normally zero. Nonzero \(\alpha_j\) would correspond to exponentially suppressed components that are not global minimizers. The manuscript does not reconcile these definitions or state whether the order-parameter rate is normalized separately on each phase.

### 7. The shell theorem imports unproved uniform coefficients

Uniform A2/B1 local coefficients on every active phase chart, including soft-window and overlap regions, are assumed. The previous papers do not prove them. At coexistence, subexponential component weights and coefficients may fail to converge; the statement about “precisely” selected mixtures needs a tightness and subsequence theorem.

### 8. The commutation theorem is mostly finite-volume bookkeeping

Projection and conditioning commute on one exact joint law under standard measurability conditions. The nontrivial content would be uniform passage of the component LDPs, shell coefficients, Gaussian tangents, and dynamic semigroups. All of those are assumed from upstream papers.

### 9. Standalone novelty is insufficient

Once the unproved platform claims are removed, the paper contains the elementary fact that a positive partition of unity gives an exact finite mixture and that a finite mixture of LDPs has a minimum rate. This belongs as a lemma in a platform paper, not as an independent top-four submission.

## Status of earlier objections

The arbitrary mixture of external tilted laws and the double subtraction of phase cost are repaired. The new positive soft label is legitimate. It does not create the phase-local analytic/LDP interfaces claimed downstream.

## Minimum reconstruction

Each platform must first construct a concrete order parameter, prove a finite-component LDP and localized complex/shell estimates, and establish the component recovery laws. D1 should then be reduced to a short common lemma or removed.

## Recommendation

**Reject; remove as a standalone submission.** The exact soft disintegration is valid but elementary, while every substantial phase theorem is assumed rather than proved.