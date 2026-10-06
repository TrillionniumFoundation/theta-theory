# Proof audit — General Theta Foundations I, Revision 93

The controlling external assessment is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. The immediate published base is v92 at `a7081ca8cfb1df8f6369a5820e4f3b5027b66ca2`, native source `33811525dd80dbc3c0c70059114fb779e9ac9c84`. No later referee report is being assumed. The original reports remain frozen verbatim.

## Current theorem dependencies

Primary Sections 15–18 retain the general finite-experiment normal form, attained common-barycenter roofs and duals, the shared-basis exact scores and the two-cut rank hierarchy. The new Primary Section 19 uses their actual unsaturated centered-swap upper, not a numerical fit or an informal memory analogy.

| New result | Dependencies and decisive argument |
|---|---|
| Theorem 19.1: optimal initial Grams | Rank-sensitive centered-swap bound; equality forces each normalized Gram to be a common flat rank-r projection, hence rho<=I/r. Conversely the interval decomposition and support-inverse instrument give attainment. The exceptional (2,1) cap is automatic. |
| Corollary 19.2: three specified cuts | Resolve a mixed initial state classically inside its q-dimensional reference, never add a quantum purification there. A Kraus branch has rank at most min(q,k); the second Gram has rank at most ell. Existing rank bounds give complete-class uppers, fixed-subspace inputs attain them. |
| Lemma 19.3: projection stability | Write eta=1-f^2 and e=tr(ab)-f^2/r. The centered deficit is at least (d-1-1/r)eta+e. The positive polar product has rank at most r. Schatten inequalities and a purification trace estimate give distance to its flat support with no matrix inverse. |
| Corollary 19.4: near-optimal frames | Sum nonnegative branch deficits with weights tr(A)/d, then apply Jensen separately at each first label. These are Gram weights, not hypothesis probabilities. |
| Proposition 19.5: initial spectral loss | Exact unhalved trace distance to {sigma<=I/r} is twice the mass above 1/r; combine with the approximate-frame residual. |
| Proposition 19.6: exceptional qubit | A pure factor reduces the centered product to sqrt(b)(I-2a)sqrt(b). Its trace and determinant give norm sqrt(1-4|z|^2), and the pinching error is 2|z|. |

## Quantifiers and edge cases

The finite basis index is selected once and reused twice. Equal-prior spectral optimality and rigidity assume t>0; the biased three-cut formula uses the existing explicitly stated prior. At t=0 every score is 1/2 and no rigidity follows. The projection construction permits zero eigenvalues and works on the actual Schmidt support. The stability lemma permits unequal supports and only bounds the smaller Gram rank; it does not divide by fidelity and includes f=0. The common projection may vary between recorded branches. In the exceptional qubit rank-one case, the exact equality set is commutation with the pure factor, including mixed diagonal states, not merely a pair of pure projectors.

Public mixtures in the two-cut model are represented by a common purified initial preparation followed by dimension-preserving classical refinement. For the new first-reference cap, mixed states are instead resolved classically without enlarging that reference. The two arguments must not be interchanged. No result caps final-measurement workspaces at every time.

## Proof versus execution

`spectral_frame.py` checks and constructs rational spectra and weights exactly; it assumes a known eigenbasis and does not construct a second-moment design or a physical device. `spectral_rigidity_check.py` checks exact small-dimensional spectra, instrument trace identities, qubit Born probabilities, singular and noncommuting negative controls, and pinching identities. Its complex random sanity cases are expressly floating-point, deterministic and not continuum proofs. All prior suites are retained and executed. Fresh build receipts, not this document, establish which exact source and final SHA were rebuilt.
