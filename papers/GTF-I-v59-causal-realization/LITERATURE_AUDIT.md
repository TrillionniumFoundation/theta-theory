# Theorem-level literature addition — Revision 59

The complete v58 audit and its twelve-area comparison remain in retained-v58/LITERATURE_AUDIT.md. The present addition addresses the controlled-process gap raised in both r39 reports. It is an author-side comparison, not independent priority clearance.

## Directly inspected primary source

Satinder Singh, Michael R. James and Matthew Rudary, *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, UAI 2004, pp. 512–519, arXiv:1207.4167. The full primary paper was read; the displayed HMM/POMDP factorization on printed p. 515 and predictive-state result on p. 516 were also inspected as page images.

Theorem 2 bounds the system-dynamics rank by the hidden POMDP state count. Theorem 6 equates finite linear dimension with finite linear predictive-state dimension. The update coefficients in the latter need not be nonnegative. These are rank/exact-model statements, not a count of distinct future-response functions.

## Comparison with the new statements

| New statement | Closest object | Additional hypotheses and conclusion |
|---|---|---|
| Repeatable-process boundedness | Controlled hidden-state instrument and future-response matrix | Compact reversible physical actions plus repeatable fresh probes; arbitrary horizon-dependent nonnegative instruments; one TV budget for all adaptive transcripts; finite response quotient at every fixed error below one. |
| Eventual minimum below one half | Finite-state behavioral quotient | One common statistical continuation gives disjoint events; large enough success probability requires a distinct cut label per response type. This is not inferred from linear dimension. |
| Adaptive rational compiler | Positive state realization / controlled HMM approximation | Supplied rational rotations and rational unit seed; affine probes uniformly positive on the whole ball; explicit instruments with a joint-trajectory entropy/coupling proof. |
| Explicit process converse | Finite statistical experiment comparison | Uses the v58 rational orbit lattice and repeated coordinate probes; no spectral gap; sufficient continuation length is charged to the horizon. |

The information-theoretic inequalities used in these proofs are elementary classical tools and are proved in place. The finite-register testing inequality is a nonnegative-mixture argument, not a newly named general information-theory principle. The paper does not claim a new general theory of HMMs, a rank characterization for arbitrary irreversible systems, or quantum measurement non-disturbance.

## Access and priority limits

The new full-primary comparison repairs one specific missing theorem-level access point. It does not exhaust Heller/Jaeger/controlled-positive-realization formulations, prove that no equivalent numerical-error theorem exists, or constitute approval by an independent expert. The classical compact-semigroup, neutral-letter, spectral-gap, nonnegative-rank and orbit-geometry attributions from v58 remain. No publication recommendation is derived from archive volume, test count or revision number.
