# Literature and theorem-role audit — Revision 61

## New primary-source comparisons, 28 September 2026

This is an author-side audit, not independent priority clearance. The predecessor's targeted comparisons are retained below, including their access and scope qualifications. No claim of exhaustive novelty follows from a search or from repository ancestry.

| Source and exact role | Comparison with this revision |
|---|---|
| Polyanskiy–Wu, *Wasserstein continuity of entropy and outer bounds for interference channels*, IEEE TIT 62 (2016), 3992–4002; arXiv:1504.04419v2, Proposition 1 | Proves entropy continuity for regular Euclidean densities using a logarithmic-gradient condition. The entropy/transport principle is classical. Our compact-support spherical mixture lemma is proved independently, including zeros, and is combined with a centroid-mass flow coupling and a narrow-cut occupation argument. No novelty is assigned to entropy continuity itself. |
| Lubotzky–Phillips–Sarnak, *Hecke operators and distributing points on the sphere I*, CPAM 39 (1986), S149–S186 | The norm-five rotation construction and its arithmetic spectral theorem are classical deep inputs. This revision uses them to make a stochastic-width constant numerical; it does not prove the Hecke spectral theorem. |
| Pinochet Lobos–Pittet, arXiv:1805.05261v2, Theorem 1.1, p. 2; published expanded article in Enseign. Math. 67 (2021), 63–94 | The exact statement inspected gives norm 2 sqrt(p)/(p+1) for the adjoint norm-p quaternion set. At p=5 this is exactly the displayed six-rotation set and sqrt(5)/3. The primary PDF page was visually inspected. Its discussion attributes the original spectral inclusion to LPS and Deligne. The original Wiley paper's full proof was not newly inspected. |
| Full Koopman/regular-representation spectral gap versus finite-dimensional matrix contraction | The new theorem requires the full L2 action bound off all invariant functions. Circle examples with contracting first harmonics and invariant or nearly invariant high harmonics explain why the weaker matrix condition is insufficient. No finite harmonic test certifies the required gap. |
| Classical KL/Hellinger inequality, Fisher-information convexity and continuity-equation calculus | These are elementary/classical ingredients, proved in the form used. The specific additional invariant is the law weighted by p_s times the norm of the conditional centroid, with transport cost paid by its lost total mass. |

Sources inspected: https://arxiv.org/html/1504.04419v2 ; https://arxiv.org/pdf/1805.05261 ; https://ems.press/journals/lem/articles/3007703 . The bibliography gives conventional publication data and DOI identifiers. The v61 fixed-error lower argument does not rely on the polynomial mixing rate as a pointwise executable block; the entropy loss is incurred in one step and only the initial potential has a logarithmic range.

## Quantifiers that must be compared in a future independent review

The theorem quantifies over a new clocked stochastic realization at every horizon, every advertised positive cut of a given width, arbitrarily large intervening registers, zero or arbitrarily small hidden masses, and a closed wordwise numerical error with all decoder values legal. It does not assume that the hidden state is a deterministic geometric quantizer, that centroids remain on the target orbit, or that identity-product words leave hidden labels unchanged. These are the precise additional realization conditions for comparison with entropy-transport, positive realization, quantization and controlled hidden-state literatures.

The new explicit example is an action on a Bloch sphere with rational rotation matrices and a rational seed; its unitary lifts are algebraic. It is not the old five-letter rational-unitary example with a silently substituted spectral constant. Its exact count is a coset-ball count because the seed has a nontrivial cyclic stabilizer.

## Preserved v59 comparison and its qualifications

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
