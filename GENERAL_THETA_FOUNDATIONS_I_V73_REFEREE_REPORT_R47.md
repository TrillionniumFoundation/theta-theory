# Referee Report — General Theta Foundations I, Revision 73 (r47)

**Quantitative manuscript:** *Noise-Uniform Readout Geometry and Reusable Instrument Descriptions*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v73-noisy-readout-crossover-2026-10-04`
- `revision/general-theta-foundations-i-v73-referee-ready-2026-10-04`

**Reviewed exact final head:** `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`  
**Candidate publication:** `f4a4412cd656239e0a49cd6945cbe7a467c7d9cf`  
**Qualified native source:** `28ab8c51143df999b444273b954f63a5160c83f7`  
**Source predecessor:** Revision 72 final head `12296ed387dbc197ff7cb854d3a78d0bf964960e`  
**Controlling external report:** Revision 71 r46, `b78c1dddd41de645edf207bc415406b3fc1b5e83`  
**Controlling pipeline audit:** `43e6713de2aa65f65e649df7cd90e2a95fc83a06`  
**Source qualification workflow:** `37152200748`, conclusion `success`  
**Exact-head read-only reconstruction:** `37152470375`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v73-external-referee-r47-2026-10-04`  
**Date:** 4 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 73 contains a coherent and technically competent new theorem package. I did not find a fatal gap in the noise-uniform adaptive modulus, the finite GHZ-block converse, the circle covering argument, the exact rational readout codec, or the conditional-state extension. Because Revision 72 did not receive a separate external report, I also independently audited the inherited observable-readout theorem, its phase-free rational flag atlas, and the uniformly seizable covering transfer needed to assess the current paper. I did not find a fatal gap in those chains either.

The central new result concerns the ordered binary qubit measurements

```text
E_(theta,lambda)^±
  = 1/2 [ I ± lambda(cos(theta) sigma_1 + sin(theta) sigma_2) ],
```

where the visibility `lambda in [0,1]` is public. Writing

```text
K_(N,lambda)
  = lambda sqrt( N min{N, 1/(1-lambda^2)} ),
K_(N,1)=N,  K_(N,0)=0,
```

the manuscript proves, with absolute constants,

```text
(1/64) min{1, K_(N,lambda) h(theta,phi)}
 <= d_N(M_(theta,lambda),M_(phi,lambda))
 <= min{2, K_(N,lambda) h(theta,phi)}.
```

It follows that for `0 < delta <= 2^(-10)` the arbitrary-centre covering number and the rational-circle covering number are both of order

```text
1 + K_(N,lambda)/delta,
```

uniformly in the horizon, public visibility, and accuracy. The fixed-length reusable payload is therefore

```text
log_2(1 + K_(N,lambda)/delta) + O(1).
```

At fixed interior noise this is the square-root scale; at projective visibility it is the linear coherent scale; and at complete erasure the family collapses to one point. The proof is finite-distance and finite-horizon. It does not infer the result from local Fisher information.

A companion corollary appends two rank-bounded conditional output states. If

```text
V = sum_(y=±) [r_y(2n-r_y)-1],
```

then the description length becomes

```text
log_2(1+K_(N,lambda)/delta)
  + (V/2) log_2 N + V log_2(1/delta) + O(1)
```

on a fixed small-error range. The decoded conditional states remain rational when the supplied data are rational, preserve zero/rank promises in the inherited sense, and do not increase the declared ranks.

These are meaningful results. Revision 73 answers a concrete objection left after r46: the constants of the strict-interior programme argument are now controlled along one explicit path to the projective boundary. It also supplies an exact legal code rather than only a metric-entropy existence proof.

The four-leading-journal disposition nevertheless remains negative. The new theorem is an exact analysis of one fixed one-dimensional noisy POVM family. Its principal mechanisms—classical simulation by common extremal channels, the noisy Heisenberg-to-standard transition, entangled block amplification, and finite-dimensional metric packing—have substantial antecedents. The manuscript's contribution is their finite-use, noise-uniform covering consequence and rational realization, not a new general principle of comparable breadth. The visibility is public rather than learned or encoded. The covering law is proved only at small error. The conditional-state extension is a product construction with separately identifiable angular and preparation coordinates. General nonobservable readout, arbitrary noisy POVMs, coupled support-changing/coherent tangent directions, growing dimensions, mutable workspace, unknown-instrument learning, and physical classical simulation remain outside the theorem.

The priority comparison also remains incomplete. The bibliography correctly cites the Demkowicz-Dobrzański--Kołodyński--Guţă classical-simulation mechanism and the Puchała--Pawela--Krawiec--Kukulski--Oszmaniec multiple-shot theorem for projective measurements. It does not cite the more directly relevant paper by M. Sedlák and M. Ziman, *Optimal single-shot strategies for discrimination of quantum measurements*, **Phys. Rev. A 90** (2014), 052312, arXiv:1408.0934, which explicitly treats projective qubit measurements and their mixtures with white noise by reduction to state discrimination. Nor does the focused comparison cite the later single-shot measurement-distance formulation of Puchała--Pawela--Krawiec--Kukulski, **Phys. Rev. A 98** (2018), 042103. These papers do not contain the present finite-use uniform crossover, arbitrary-centre covering law, or rational codec, but they are direct theorem-level antecedents and must be discussed before making a priority claim.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is a strong specialist-level contribution in quantum information, finite-dimensional metric entropy, and exact rational coding. I would encourage a substantially focused submission to a strong specialist venue after an independent priority review, a direct comparison with the noisy-measurement discrimination literature, and further compression of the inherited history. The structural companion remains a coherent specialist contribution, but it is inherited here and retains its fresh nondisturbing-probe and terminal-realization scope.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 73 manuscript branches are identical at

```text
ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f.
```

No Revision 74 branch was present in the branch survey used for this report. The exact final head is a direct successor of candidate publication `f4a4412c...` and adds the read-only reconstruction request. The candidate publication descends from native theorem source `28ab8c51...`. The declared predecessor is the completed Revision 72 final head `12296ed3...`.

Revision 72 was source-qualified and exactly reconstructed but had no separate external GTF referee report. Its theorems are therefore inherited source mathematics, not externally certified conclusions. I reviewed the v72 material needed for the present decision instead of treating successful CI or author-side audit files as a mathematical endorsement.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/47-varying-readout.tex`;
- `sections/48-seizable-covering-transfer.tex`;
- `sections/49-noisy-readout-crossover.tex`;
- `noisy_readout_codec.py` and `check_noisy_readout.py`;
- the inherited conditional, preparation, coherent, intrinsic-instrument, Choi, and streaming codecs;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r46 report and proof/pipeline audit;
- the schemas, resource ledgers, preservation manifest, build receipt, source hashes, theorem locations, page checks, and regression results;
- source-qualification run `37152200748`; and
- exact-head read-only run `37152470375`.

I also made a targeted comparison with primary work on noisy measurement discrimination, multiple-shot projective-measurement discrimination, noisy quantum metrology, environment-parametrized and environment-seizable channels, quantum population coding, and adaptive channel discrimination. This is not a formal proof-assistant verification and not an exhaustive novelty search.

---

## 2. Executive assessment of the v73 mathematics

### 2.1 Exact one-use distance and the hybrid branch

For two angles at circular distance `h`, put

```text
a = lambda sin(h/2).
```

The positive-outcome effect difference is a traceless qubit operator of operator norm `a`. For a reference-assisted input, the two classical output blocks differ by `B` and `-B`, with `||B||_1 <= a`; an eigenstate of the effect difference attains equality. Hence the exact one-use unhalved distance is

```text
d_1 = 2a.
```

Replacing device calls one at a time gives

```text
d_N <= 2Na.
```

This argument is sound for arbitrary common adaptive testers, finite references, feedback, and bounded public stopping.

### 2.2 Pair-dependent two-point programme

Let `u` be the midpoint direction of the two equatorial Bloch vectors and `v` its perpendicular. The target Bloch vectors have the form

```text
m ± a v,
m = lambda cos(h/2) u.
```

With

```text
b = sqrt(1-||m||^2) = sqrt(1-lambda^2+a^2),
```

the endpoints `m ± b v` are pure and define two legal projective measurements. Each target is an exact mixture of these same endpoints, with Bernoulli programme bias

```text
t = a/b.
```

For every fixed adaptive tester, its final state is a common channel of `N` independent programme bits. Classical fidelity and trace-norm contraction therefore give

```text
d_N <= 2 sqrt(1-[ (1-lambda^2)/(1-lambda^2+a^2) ]^N).
```

Combining this with the hybrid branch yields

```text
d_N <= min{2, K_(N,lambda) h}.
```

The processor depends on the pair of alternatives. That is legitimate for a two-point metric bound, but it is not a global environment seizer for the circle and should never be advertised as one.

### 2.3 The Bernoulli majority lemma

For symmetric Bernoulli laws with biases `±a`, the manuscript proves

```text
||P_+^m-P_-^m||_1 >= (1/2) min{1,a sqrt(m)}.
```

The proof retains the largest odd number of coordinates and differentiates the majority probability exactly. The central binomial coefficient estimate and Bernoulli inequality give a uniform derivative bound for `a <= m^(-1/2)`; monotonicity supplies the saturated regime. The argument includes `m=1`, `a=0`, and `a=1` and uses neither a variance lower bound nor an asymptotic normal approximation.

I find the constants conservative but correct.

### 2.4 GHZ-block lower bound

A `k`-qubit GHZ input with one pair-dependent phase turns the product of the `k` measurement signs into a Bernoulli variable with opposite biases

```text
a_k = lambda^k |sin(kh/2)|
```

under the two hypotheses. Repeating `m=floor(N/k)` independent blocks and applying the preceding lemma gives

```text
(1/2) min{1,sqrt(m) a_k}
```

as an admissible lower bound.

Put

```text
eta = 1-lambda^2,
T = min{N,1/eta},
k_0=floor(T).
```

For `1 <= k <= k_0`, the manuscript proves

```text
lambda^k >= lambda/2.
```

This follows from the exact logarithmic estimate and is not an assertion about arbitrary large blocks. Small angular differences use `k=k_0`, the case `k_0=1` uses single-copy blocks, and larger angular differences use `k=max{1,floor(1/h)}`. These cases yield

```text
d_N >= (1/64) min{1,K_(N,lambda)h}.
```

I checked the floor estimates and the endpoint cases `lambda=0` and `lambda=1`; I did not find a missing regime.

### 2.5 Arbitrary-centre covering lower bound

At small error, circle points separated by

```text
256 delta/K_(N,lambda)
```

have pairwise adaptive distance at least `4 delta`. Therefore a radius-`delta` ball about any legal memoryless instrument—not merely a member of the equatorial family—contains at most one packing point. If the required angular separation exceeds the circle diameter, the trivial cardinality-one lower bound supplies the `1+K/delta` form after adjusting the absolute constant.

The arbitrary-centre quantifier is handled correctly. No noisy-circle retraction is assumed.

### 2.6 Rational circle upper code

Two rational stereographic semicircle charts cover the unit circle:

```text
z_s(t)=s((1-t^2)/(1+t^2), 2t/(1+t^2)),
s in {±1},  -1 <= t <= 1.
```

Their angular speed is at most two. Rounding `t` to `j/B` gives angular error at most `1/B`; choosing `B` of order `K/delta` gives the desired adaptive error. The chart sign and integer digit produce at most `4B+2` codewords.

For rational visibility and target direction, the grid is selected by integer squaring and exact rational comparison. Every accepted codeword decodes to effects with eigenvalues `(1±lambda)/2`; there is no approximate positivity test or irrational normalization. At `lambda=0`, one canonical zero-bit codeword suffices.

The implementation agrees with this construction and distinguishes the compressed payload from the JSON envelope and expanded Choi matrices.

### 2.7 Conditional-state extension

Discarding the conditional quantum output recovers the noisy readout, so the angular lower bound is independent of the states. Feeding `I/2` makes both retained outcomes equiprobable and produces the programme state

```text
(1/2)rho_+ direct_sum (1/2)rho_-.
```

This is independent of the angle and visibility. Rank-stratum patches for the two trace-one states have total dimension

```text
V = sum_y [r_y(2n-r_y)-1].
```

Crossing the angular and state packings is legitimate: different angles are separated by the readout witness regardless of states, while equal angles with different states are separated by the mixed-input product-state witness.

For the upper bound, the angle receives half the error budget and the two state programmes receive a quarter each. A common processor consumes one copy of each row state at every call and selects the outcome-indexed state. The resulting description count is the product of the circle code and the two inherited singular factor codes. The Choi blocks are

```text
(E_y)^T tensor rho_y,
```

with the input-first transpose. Rationality, complete positivity, trace preservation, and rank nonincrease are preserved in the declared scope.

I find the argument correct as a product-family theorem. It is not a result for arbitrary correlated variation of effects and conditional states.

---

## 3. Independent audit of the inherited v72 additions

### 3.1 Observable varying projective readout

Revision 72 considers ordered rank-one projective flags

```text
P=(P_1,...,P_d) in U(d)/T^d,
```

of real dimension

```text
b=d^2-d,
```

combined with rowwise rank-bounded conditional output states of total dimension `V`. It proves the small-error covering law

```text
C_1 (N/delta)^b (sqrt(N)/delta)^V
 <= R_N(delta)
 <= C_2 (N/delta)^b (sqrt(N)/delta)^V.
```

The projective readout scale is linear in `N`; the conditional preparation scale is square-root in `N`.

The exact multiple-use projective-measurement formula is imported from Puchała--Pawela--Krawiec--Kukulski--Oszmaniec. The manuscript correctly treats that theorem as an external premise. The product packing and arbitrary-centre argument are then elementary and coherent.

### 3.2 Phase-free rational flag atlas

The direct codec chooses rational nonzero columns from supplied rational projectors, performs partial-pivot LU, and records a permutation plus the strictly lower-triangular entries of a unit lower-triangular matrix. Right multiplication by the upper-triangular factor preserves the nested column spans. Successive differences of rational projections onto those spans recover the ordered flag without storing normalized algebraic eigenvectors or column phases.

The finite family of charts has exactly `d^2-d` real coordinates. The uniform inverse-singular-value bound on the bounded triangular cube gives a dimension-dependent projection perturbation estimate. Rounding at grid `B` yields a legal rational flag and an `O_d(N/B)` adaptive error.

I did not find a fatal issue in this construction. Its constants are extremely dimension dependent, and no growing-dimensional result follows.

### 3.3 Uniformly seizable covering transfer

The v72 theorem assumes one fixed processor `A` on the full ambient programme-state space and one fixed one-use seizer `B` satisfying

```text
B(A(omega))=omega
```

for every programme state. Under this strong hypothesis, the adaptive metric equals the `N`-copy state trace distance. The map `R=A B` is an idempotent superchannel on arbitrary legal memoryless centres and cannot increase their distance to a target family member. Therefore family covering numbers transfer exactly, including arbitrary centres.

The proof is sound under the stated ambient-domain assumption. A pairwise programme representation is not enough; v73 correctly distinguishes its pair-dependent noisy upper proof from this global seizing theorem.

---

## 4. Implementation and reproducibility assessment

### 4.1 Exact codec

`noisy_readout_codec.py` implements:

- canonical rational parsing for visibility and unit-circle coordinates;
- exact computation of `K^2` through rational arithmetic;
- an integer ceiling square root for the grid;
- two legal rational circle charts;
- fixed-alphabet payload accounting;
- exact effect and Choi assembly;
- the `lambda=0` zero-payload branch;
- nested preparation-state codes with explicit error budgets and rank headers;
- strict schema validation;
- duplicate-field rejection; and
- complete target-bound canonical replay.

The decoder checks mathematical legality. The verifier proves only equality with the canonical encoder output for the supplied target. This is the correct certificate boundary.

### 4.2 Finite regression

`check_noisy_readout.py` records 6,461 exact assertions, 189 readout cases, 72 GHZ-block cases, eight conditional-state cases, and 30 named negative controls. It checks, among other things:

- exact circle identities;
- the erased endpoint;
- effect determinants and ranks;
- majority-polynomial derivatives;
- GHZ tensor probabilities and parity means;
- finite programme expressions;
- conditional Choi assembly;
- rank nonincrease;
- malformed/canonical payload handling; and
- target-bound replay.

No floating-point oracle is used. These tests are strong regression evidence. They do not prove the continuum covering theorem, the supremum over all adaptive testers, the imported projective-measurement theorem, or novelty.

### 4.3 Build and exact-head evidence

The build receipt records:

- a 40-page quantitative article;
- a 40-page structural article;
- a 140-page complete edition;
- an isolated rebuild;
- no unresolved references or LaTeX box diagnostics;
- 197 preserved predecessor source files;
- 482 preserved predecessor labels and 502 current complete-edition labels;
- agreement between normal and optimized regression modes; and
- successful execution of all inherited suites.

Source qualification run `37152200748` completed successfully. Exact-head run `37152470375` checked out `ab67d30...` without retained credentials, reconstructed exact source and every PDF page, executed all tests, verified the immutable predecessor, rebuilt the minimal journal package, and uploaded a read-only attestation.

This is strong source and reproducibility evidence. It is not a proof-assistant certificate, an independent priority determination, a cryptographic author signature, or journal acceptance. The exact final commit is unsigned.

---

## 5. Why the top-four threshold is not met

### 5.1 The new theorem is deliberately one-dimensional

The noise-uniform transition is proved for one equatorial circle of ordered binary qubit measurements with one public visibility. The proof does not produce a general local normal form for noisy POVM manifolds, a rank/tangent classification of instrument boundaries, or a multidimensional anisotropic crossover theorem.

### 5.2 The main scaling mechanisms are established

Classical simulation of noisy channels, the transition from coherent to standard scaling under noise, GHZ amplification, environment/programme processing, and finite-dimensional covering are established ideas. The finite-use two-sided modulus and exact rational family cover are useful new syntheses, but their breadth is not comparable to that normally expected at the four leading general journals.

### 5.3 Public visibility removes an important parameter

The visibility may depend on `N` and `delta`, but it is public. The theorem does not encode an unknown visibility jointly with the angle, learn it from queries, or analyze a two-dimensional target family. Adding that coordinate could change both identifiability and local anisotropy.

### 5.4 The error range is small

The angular covering law is proved for `delta <= 2^(-10)`. The manuscript expressly does not obtain a full submaximal-error coherent covering law. Pair-dependent tests do not automatically yield a common large-error estimator or multiplicity theorem.

### 5.5 The conditional extension is separable

The readout and two conditional state coordinates are isolated by different public experiments and combined through a product code. This is mathematically clean, but it does not address coupled effect/state perturbations or general disturbing instruments.

### 5.6 The v72 theorem remains highly structured

Observable ordered flags, orthogonally recoverable labels, and global ambient seizing are strong identifiability structures. Equal conditional rows can erase the readout exactly. The paper does not classify partially observable or overlapping-output readout families.

### 5.7 Priority is not independently closed

The author-side audit is careful and unusually candid, but the closest noisy-measurement discrimination antecedents are not all in the focused comparison. The omission of Sedlák--Ziman is especially material because their paper explicitly treats white-noise mixtures of projective qubit measurements.

### 5.8 The wider Theta programme remains independent

The finite-dimensional description theorems do not prove the repository's raw local-limit, stopped LDP, global-kernel, canonical conditioning, Mosco/Nisio, filtering/LAN, changing-filtration response, or posterior-contraction gates. Every aggregate A/B/C/D completion flag remains false.

### 5.9 The structural article is inherited

The structural companion is not materially advanced in Revision 73. Its stationarization and repeatable-probe theorems remain specialist-level results with their original recurrence and fresh-probe hypotheses. Their presence cannot be added to the significance of the new noisy-circle theorem as though all parts were one new contribution.

---

## 6. Required revisions before specialist submission

1. **Submit a genuinely focused quantitative article.** Keep the v73 noisy-readout theorem, the minimum v72 machinery needed to state it, the exact codec, and direct comparisons. Treat the 140-page complete edition as repository history.

2. **Add Sedlák--Ziman explicitly.** Explain precisely what their single-shot white-noise-mixture reduction proves and what the present finite-use covering theorem adds.

3. **Add the 2018 single-shot measurement-distance paper.** Distinguish its diamond-norm optimization from the v72 multiple-shot formula and from the v73 noise-uniform family cover.

4. **Keep established mechanisms out of the novelty claim.** The novelty statement should be the finite-use uniform modulus, arbitrary-centre covering order, endpoint-uniform constants, and exact legal rational code.

5. **Put the public-visibility convention in every headline theorem.** Do not let “noise-uniform” suggest that visibility is an unknown encoded or learned coordinate.

6. **Keep the small-error cap visible.** The result is not a full-error coherent covering law.

7. **Preserve the ordered-outcome convention.** `theta` and `theta+pi` are distinct because outcome labels are not quotiented by relabelling.

8. **Separate pairwise programmes from global seizing.** The v73 upper processor depends on the pair; the v72 transfer theorem requires one processor and one seizer over the full ambient family.

9. **Separate pairwise packing tests from common estimators.** The GHZ phase and block length may depend on the two packing points. No one global decoding measurement is constructed.

10. **State the centre classes every time.** Lower covers allow arbitrary legal memoryless centres; rational upper centres lie in the displayed family. No noisy-circle centre retraction is proved.

11. **Clarify rationality.** Rational circle coordinates and rational visibility give rational effects. For irrational public visibility, the geometric theorem remains real-valued but the decoded Choi matrices need not be rational.

12. **Separate payload from all other resources.** JSON length, public headers, encoder workspace, expanded matrices, programme copies used in a proof, and physical processor dimension are not the fixed-length payload.

13. **Keep learning and physical simulation separate.** The encoder receives the target. It does not identify an unknown measurement and does not implement a finite-classical-resource device acting on unknown quantum input.

14. **Retain the exact hypotheses of the v72 imported theorem.** State clearly where projectivity, ordered outcomes, and the external multiple-shot theorem enter.

15. **Obtain independent priority review.** At least one expert in quantum measurement discrimination/metrology should compare the exact finite-use statement with the noisy-measurement and channel-simulation literature.

16. **Publish a signed release or tag.** The exact-head CI is strong, but the reviewed commit remains unsigned.

17. **Keep the A/B/C/D programme out of the local novelty claim.** The current paper neither depends on nor closes those gates.

---

## 7. Detailed comments

1. The abstract should write the definition of `K_(N,lambda)` exactly once and retain the endpoint conventions. The alternative expression `lambda min{N,sqrt(N/(1-lambda^2))}` is equivalent but can conceal the `lambda=1` convention.

2. “Noise-uniform” means uniform constants over public `lambda`; it does not mean robustness to uncertainty or misspecification of `lambda`.

3. The exact one-use equality `d_1=2lambda sin(h/2)` is an important normalization check and should precede the asymptotic interpretation.

4. The programme endpoints are pair dependent. This dependence is harmless for a metric upper bound but prevents interpreting them as one global finite programme alphabet for the whole circle.

5. The finite fidelity expression is stronger than the final scale inequality and should remain in the paper.

6. The lower tester is nonadaptive after choosing its GHZ block design. The defining supremum allows adaptivity, but the proof does not need it.

7. The GHZ phase depends on the unordered pair of alternatives, not on the unknown hypothesis. This should remain explicit.

8. The proof of `lambda^k >= lambda/2` is valid only for `k` below the noise correlation scale; the manuscript states this correctly.

9. In the large-angle case, the choice `max{1,floor(1/h)}` handles `h>1`; retaining this `max` avoids a zero block length.

10. At `lambda=0`, every direction represents the same instrument. The canonical zero-payload branch is preferable to carrying redundant chart words.

11. The packing proof should continue to say that arbitrary off-family centres are excluded by triangle inequality, not by an unproved retraction.

12. The two semicircle charts overlap at endpoints. This affects only an absolute factor in codebook size.

13. The `C^{rat}` notation is potentially misleading for irrational public visibility. “Rational-circle centres” would be clearer.

14. The fixed-length payload is the index capacity, not the canonical hexadecimal string length. The code documentation makes this distinction; the paper should do the same.

15. In the conditional theorem, the state dimension subtracts one trace constraint for each normalized conditional state, hence the sum of `r_y(2n-r_y)-1`. This differs from the jointly subnormalized preparation family of v68.

16. The maximally mixed input is decisive because both binary effects have trace one. This is not a general fact for arbitrary multi-outcome noisy POVMs.

17. The conditional upper processor consumes two row programmes per slot in the proof. Those programme systems are proof devices, not charged payload or hardware.

18. Rank nonincrease applies to the encoded conditional states. It is not a statement about arbitrary covering centres or about a noisy-circle retraction.

19. The v72 ordered flag dimension is `d^2-d`; it must not be confused with the projective-unitary dimension `d^2-1` from v70.

20. The v72 exact multiple-use formula is imported. The journal-facing paper should quote its hypotheses accurately and avoid making it appear as a corollary of the present codec.

21. The v72 LU chart stores nested subspaces, not normalized basis vectors. This is a useful construction and deserves a concise self-contained explanation.

22. Uniform seizing requires a left inverse on the full ambient programme space because covering centres are unrestricted. A left inverse only on the target rank stratum would not suffice.

23. The Pauli/Bell corollary is an application of a standard seizing mechanism. Its coding consequence is local to this paper; the mechanism is not.

24. The source-transfer workflow is provenance infrastructure, not part of the mathematical proof.

25. The 6,461 new assertions should not be summarized as verifying the adaptive metric theorem. Their correct scope is finite exact regression.

26. The final-head run is attached to the exact reviewed SHA and is materially stronger than a workflow that self-publishes an unverified successor.

27. The commit is unsigned. Exact hashes establish identity of bytes, not authorship.

28. The structural paper's “repeatable observation” model still uses fresh nondisturbing classical probes. It is not repeated measurement of one quantum system.

29. The complete edition is valuable as an archive but far too broad to serve as the journal submission object for the present theorem.

30. The strongest next mathematical problem is not another special family. It is a structural criterion that derives the operational exponent from coupled local geometry while accounting for identifiability, coherent accumulation, support change, and arbitrary legal centres.

---

## 8. Final assessment

Revision 73 gives a correct-looking and useful finite-use description theorem for one explicit noisy measurement family. The argument is more than a local metrological calculation: it supplies a finite-distance upper programme, a matching GHZ-block lower witness, arbitrary-centre covering estimates, endpoint-uniform constants, and an exact rational code. Revision 72 also contains a coherent observable-readout and uniformly seizable covering package that I find mathematically plausible after independent inspection.

I did not find a fatal mathematical error in the inspected chains. The work is therefore suitable for serious specialist consideration.

It does not meet the Annals / Inventiones / JAMS / Acta threshold. The principal theorem is one-dimensional and highly structured; its central scaling mechanisms are established; visibility is public; the error range is small; the conditional extension is product-separable; the general boundary problem remains open; and independent priority is not closed.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused specialist submission after direct noisy-measurement literature comparison and independent priority review.**
