# Response to the controlling v68/r45 reports — Revision 70

Quantitative manuscript: **Coherent and Preparation Directions in Rational Instrument Coding**.
Structural companion: **Finite Physical Actions and a Strong Converse for Repeatable Observations**.

External report `e862e5c963ef36b9caa3b1b814b495ae4428a088` and proof/pipeline audit `a3fd5b80549a855c46151fd7183b3fc7139abac7` review completed v68 head `d9d8c464282157485813041d181e909e648b1f4f`. This revision does not mistake the older v64 report for the latest one. The v69 continuation at `02ed97a71c1a8c8f3b247126b52d294c1e2752fb` is preserved as an anchor only. The mathematical base is v68.

## Mathematical response

The report identifies a substantive boundary question: a preparation family alone has no reversible coherent direction. We retain every v68 theorem and add an explicit non-input-erasing tensor family

    F_(U,sigma),y(X) = U X U* tensor sigma_y.

Here U is a d-dimensional unitary modulo global phase and the positive preparation blocks have fixed public rank bounds r_y. Put u=d^2-1 and v=sum r_y(2n-r_y)-1. The new joint law is

    log2 C_N(delta;r) = (u+v/2) log2 N + (u+v) log2(1/delta) + O(1)

for all N>=1 and 0<delta<=1/32, uniformly in both N and delta at fixed dimensions/ranks. Centres in the converse may be arbitrary legal memoryless instruments. This is a positive theorem for a coherent and support-changing boundary family, not a claim that all disturbing-instrument tangent cones have the same law.

The lower proof routes a data system through a common correcting unitary and uses a two-eigenvector probe. It obtains an N-scale coherent separation. Discarding that system instead retains the preparation product experiment and its sqrt(N)-scale separation. A Cartesian product of two locally bi-Lipschitz packings gives the mixed coefficient. The correcting controls and binary projections remain pair-dependent. A single simultaneous identification measurement is not required or claimed.

The upper proof constructs a finite rational unitary atlas with exactly d^2-1 grid coordinates, by signed stereographic Givens factors and diagonal phases. It composes this atlas with the inherited rank-nonincreasing preparation code. For supplied rational U the atlas may be searched using a rational squared-Choi-distance test; this is finite but not advertised as efficient. The qubit specialization has a direct three-digit rational quaternion encoder, implemented in coherent_codec.py. The combined error certificate uses the triangle inequality, including its cross term, rather than adding squared errors incorrectly.

A separate exact theorem retracts arbitrary memoryless covering centres for preparation targets to preparation centres by C_y(I_d/d). A fixed fresh-input tester proves nonincrease of the distance to every preparation target. This settles the centre restriction for all positive radii; it does not prove the full-error coding-law proposal in the v69 anchor, and it does not preserve centre ranks.

The journal objective is unchanged. The new theorem package addresses the report by adding a different operational geometry, while retaining the original supplied-description interface and its resource conventions.

## Fourteen required revisions

### R45 required 01 — Direct replacer-channel antecedent

Sections 42 and the focused comparison now cite Cooney–Mosonyi–Wilde, arXiv:1408.3373v3, p. 5 and Sections 4.1–4.2. The two-replacer mechanism, asymptotic binary exponents, exact finite-use identity, and family covering-centre retraction are distinguished.

### R45 required 02 — Supplied data

Page one states that the encoder receives matrix data. The new family is supplied as U and preparation blocks; general rational U can be encoded by a finite rational atlas search. No unknown-channel learning or tomography theorem is asserted.

### R45 required 03 — Physical interface

Both new codec statements explicitly return mathematical instruments. They do not implement an unknown reference-entangled input using a classical message processor.

### R45 required 04 — Fixed dimensions and ranks

The main theorem fixes d,n,m and public rank bounds. The O(1) term is uniform in N and delta, not in those fixed parameters.

### R45 required 05 — Interior and boundary separation

All v68 interior and preparation theorems remain. Section 43 adds a distinct non-input-erasing boundary family U X U* tensor sigma_y; it does not drop the margin in the general interior theorem.

### R45 required 06 — Qualified boundary language

The new title and theorem identify coherent and preparation directions. The general disturbing-instrument body is not said to have been classified.

### R45 required 07 — Metric convention

The new theorem explicitly uses unhalved final-state trace distance over common adaptive testers with references, quantum memory, feedback and bounded public stopping. The same memoryless instrument is reused at each call.

### R45 required 08 — Pair-specific tests

The unitary correcting operation, eigenvector probe, and preparation binary test can depend on the pair. They do not yield one universal identification measurement.

### R45 required 09 — Rank variables

For preparation instruments the Choi ranks are d times the output ranks. In the new tensor family the Choi ranks equal the preparation output ranks, since the unitary Choi factor has rank one. Both facts are stated explicitly.

### R45 required 10 — Payload accounting

The rational atlas headers and digits and preparation pivot masks are charged. Public parameters, encoder search state, rational operand lengths, and expanded Choi storage are recorded separately. No polynomial-time claim is made for the exhaustive general atlas encoder.

### R45 required 11 — Accuracy range

The coding laws keep 0<delta<=1/32; no unproved full-error extension is used. Only the exact centre retraction holds for every positive radius.

### R45 required 12 — Earlier width crossover

The v63 multiplicative width gap remains a different question. A supplied-description coding theorem does not close it.

### R45 required 13 — Independent priority review

The author-side primary-source comparison is strengthened and INDEPENDENT_REVIEW_BRIEF.md supplies a precise review specification. No independent human opinion has been obtained or fabricated.

### R45 required 14 — Focused journal object

The standalone quantitative paper contains the current complete coding proof graph. The full research edition retains every predecessor mathematical label, outside the minimal journal-facing bundle.

## Twenty-four detailed comments

### R45 detailed 01 — TV constants

The retained binary lemma uses half-l1 total variation and constant 3/32. Its Choi corollary uses unhalved trace distance and 3/16.

### R45 detailed 02 — Choi projection

The positive spectral projection remains pair-dependent; the product packing does not turn it into universal tomography.

### R45 detailed 03 — Covering centres

The new lower bound permits all legal memoryless centres, including outside the tensor family. The exact preparation retraction permits full preparation centres, not necessarily rank-restricted ones.

### R45 detailed 04 — Packing space

The interior lower ball remains in the joint-marginal affine translation space. The new product packing uses local projective-unitary and maximal-rank preparation charts.

### R45 detailed 05 — Saturation

The delta<=1/32 hypothesis remains in every uniform coding headline and in the saturated lower-bound comparison.

### R45 detailed 06 — Input erasure

Section 42 explicitly separates input erasure from entanglement breaking. The new family is not erased: its data system remains coherent.

### R45 detailed 07 — Quantum processor

The preparation-programme processor is quantum. It is not a classical operational simulation.

### R45 detailed 08 — Zero PSD pivot

The existing zero-row proof is retained in full. The new code delegates the singular preparation factor construction unchanged.

### R45 detailed 09 — Pivot positions

Pivot masks remain charged in the preparation part of the payload; not only their cardinalities.

### R45 detailed 10 — Rank nonincrease

Rounding may lower rank. The new codec promises only nonincrease and preserves a zero outcome exactly.

### R45 detailed 11 — Lost rounded pivot

A rounded nonanchor pivot can vanish harmlessly. No lower-rank output is rejected for that reason.

### R45 detailed 12 — Rational factors

The preparation code still uses rational squared coordinates, not a rational Cholesky factor of the target. The new unitary decoder is exactly rational by stereographic identities.

### R45 detailed 13 — Normalization denominator

The Gram denominator and rational unitary denominators are included in expanded output accounting, not hidden in a claim that expanded matrices have payload size.

### R45 detailed 14 — Local rank chart

The inherited leading-principal-block rank chart remains local. The projective-unitary lower chart is also local; only the upper rational atlas is global.

### R45 detailed 15 — Singleton

v=0 is treated separately for the preparation factor. For d>=2, a coherent unitary family remains nontrivial even when v=0.

### R45 detailed 16 — Classical subfamily

The m-1 classical preparation example stays in the active paper. It becomes the v=m-1 factor of the tensor-family law.

### R45 detailed 17 — Standard dimensions

The dimensions n^2-1,2n-2 and d^2-1 are credited as standard geometry. The new conclusion combines their distinct adaptive scales.

### R45 detailed 18 — Legal codebook

Every unitary-atlas word decodes unitarily. Only valid preparation factor images are used; invalid syntax is not counted as a legal centre.

### R45 detailed 19 — Verification interfaces

Bare decoding checks syntax, legality and the construction budget. Target-bound verification replays both deterministic encoders. It rejects a different target quaternion.

### R45 detailed 20 — Binary tests

Finite exact Bernoulli tests remain implementation regression. The continuum derivative proof is retained.

### R45 detailed 21 — Rank tests

Independent rational elimination checks finite Choi-rank examples, not the global stratum theorem.

### R45 detailed 22 — Authorship

Hashes and read-only reconstruction are not a cryptographic author signature. No signature or acceptance is claimed.

### R45 detailed 23 — v69 status

The v69 anchor is a Git ancestor and no theorem premise. Its proposed full-accuracy extension is not declared complete. Section 42 proves the centre question anew.

### R45 detailed 24 — Analytic pipeline

The frozen dependency ledgers and all five aggregate false flags are preserved. No coding, rendering or finite arithmetic check discharges a separate analytic gate.

## Proof and review boundary

All new statements have proofs in Sections 42–43. The common tester, repeated memoryless operation, tensor order, ranks, and fixed dimensions are explicit. Finite tests separately check rational identities, unitary and instrument legality, rank nonincrease, exact zeros, centre retraction, and target-bound replay. They do not prove the continuum lower bounds or determine priority. A successful independent source reconstruction likewise does not establish journal acceptance. The primary antecedents and the specific remaining novelty comparison are recorded in LITERATURE_AUDIT.md and INDEPENDENT_REVIEW_BRIEF.md.
