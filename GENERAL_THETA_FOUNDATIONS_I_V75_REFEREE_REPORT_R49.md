# Referee Report — General Theta Foundations I, Revision 75 (r49)

**Quantitative manuscript:** *Geometry and Adaptive Coding of Binary Quantum Measurements*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v75-full-measurement-body-2026-10-04`
- `revision/general-theta-foundations-i-v75-referee-ready-2026-10-04`

**Reviewed exact final head:** `16b78c8edef566300ea21300908854ad83455879`  
**Native theorem-source parent:** `efa7b14e2a42c6276f6748f98e3a15f2da018db3`  
**Source predecessor:** Revision 74 exact head `8477a4c44cbed327068ab895c244f2ddfa86e27a`  
**Controlling external report:** Revision 74 r48, `0fd7db3c634b85ad93a4d205b95bf04b6cb7e476`  
**Controlling pipeline audit:** `53371065e8684e33bd3f04748dbea652011c5a7e`  
**Exact-head read-only reconstruction:** Actions run `37181064054`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v75-external-referee-r49-2026-10-04`  
**Date:** 4 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 75 is a substantial and mathematically coherent advance over the Revision 74 object reviewed in r48. It replaces the earlier unbiased Bloch-ball theorem by a treatment of the complete closed four-dimensional body of ordered binary qubit effects

```text
E = (a I + x·sigma)/2 = q I + (p-q) P_u,
0 <= q <= p <= 1,
```

where bias, both spectral endpoints, contrast, and direction are all target data. The manuscript proves an all-pair, all-horizon comparison for the full reference-assisted adaptive distance. It then derives the small-error covering law

```text
C_N(delta) = Theta(N^2 log(N+2) delta^(-4))
```

and supplies an exact rational code whose single payload index jointly charges both eigenvalues and the eigendirection. The logarithmic enhancement is traced to the accumulation of geometric scales near the projective corner, rather than inserted through a redundant coordinate system.

I did not find a fatal mathematical gap in the two-endpoint Bernoulli estimate, the scalar-cross-overlap dilation, the adaptive upper bound, the bias-removing lower witness, the spectral noncancellation argument, the coupling of spectral and angular changes, the projective-corner packing, the matching lattice count, or the exact rational encoder. The theorem statements also handle scalar effects, deterministic effects, one-sided singular faces, and projective measurements without assigning fictitious directions to repeated eigenvalues.

The four-leading-journal disposition nevertheless remains negative. The new theorem is strong within its interface, but the interface is still one fixed input dimension, two ordered outcomes, no residual quantum output, and memoryless reuse. The covering conclusion is restricted to sufficiently small error. The paper does not give an exact finite-use distance formula for arbitrary biased pairs, a common estimator for its packings, a higher-dimensional or multi-outcome theorem, or a result for general disturbing instruments. The ingredients—finite Bernoulli testing, pairwise dilation comparison, binary measurement discrimination, finite-dimensional packing, and rational charts—are combined effectively, but the resulting breadth remains below the standard of the four leading general mathematics journals.

The priority boundary is also not fully settled. The active literature comparison correctly discusses Fiurášek–Mičuda, Sedlák–Ziman, and the Puchała–Pawela–Krawiec–Kukulski projective results. It should additionally compare Krawiec–Pawela–Puchała, *Discrimination of POVMs with rank-one effects*, arXiv:2002.05452, which studies multiple-shot parallel and adaptive discrimination and constructs a two-shot adaptive perfect-discrimination example for rank-one POVMs. That paper does not contain the present all-pair binary biased metric, global covering law, or rational codec, but it is a direct neighboring antecedent for repeated adaptive POVM discrimination. Datta–Biswas–Saha–Augusiak, arXiv:2012.07069, is also relevant to the nonprojective single-shot boundary.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is now a strong specialist-level contribution in quantum information theory, adaptive measurement discrimination, and finite-dimensional metric entropy. I would encourage a separate specialist submission after an independent priority review, an updated neighboring-literature comparison, and editorial compression. I would not request another wholesale reconstruction of the mathematics.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 75 manuscript branches listed above point to the same exact final head

```text
16b78c8edef566300ea21300908854ad83455879.
```

That commit is the publication/evidence successor of the native theorem-source parent `efa7b14e...`. Revision 75 is three commits ahead of the completed Revision 74 head. No higher proof-complete `General Theta Foundations I` revision was present in the branch survey used for this report.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/51-biased-measurement-metric.tex`;
- `sections/52-biased-measurement-entropy.tex`;
- the inherited Revision 73 angular theorem and Revision 74 coupled-boundary theorem on which the new lower witnesses depend;
- `biased_codec.py` and `check_biased_geometry.py`;
- the active codec schema and resource ledger;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r48 external report and proof/pipeline audit;
- the build receipt, source hashes, theorem locations, page checks, package manifests, and regression outputs;
- the exact-head read-only Actions run; and
- the frozen repository-wide A/B/C/D pipeline ledger and history.

This report is not a proof-assistant certificate and is not an exhaustive search of every work on quantum statistical geometry or measurement discrimination. Where the priority boundary remains uncertain, I treat that as an editorial limitation rather than as a mathematical counterexample.

---

## 2. Executive assessment of the new mathematics

### 2.1 The correct global parameter body

An ordered binary qubit measurement with no residual quantum output is determined by one effect

```text
E_(a,x) = (a I + x·sigma)/2,
0 <= a-|x| <= a+|x| <= 2.
```

Equivalently,

```text
E = p P_u + q(I-P_u),
0 <= q <= p <= 1.
```

The manuscript correctly regards the effect matrix—not a redundant eigenvalue/eigenvector tuple—as the target. At `p=q`, the direction disappears. At `p=1,q=0`, the target is projective. Outcome exchange is not quotiented out. This is the right identifiable four-dimensional body.

The exact one-use normalization

```text
d_1(E,F) = 2 ||E-F||_op = |a-a'| + |x-x'|
```

is correct. For a reference-assisted input, the two classical output blocks are `B` and `-B`, with `||B||_1 <= ||E-F||_op`; an extremal eigenstate attains equality.

### 2.2 Spectral endpoint geometry

The two eigenvalues are controlled separately through

```text
T_N(s,t)
 = |s-t| sqrt(N/(max{s(1-s),t(1-t)}+1/N)).
```

The finite Bernoulli lemma is uniform at both support endpoints. The upper bound combines direct coupling with product fidelity. The lower bound uses a no-success block statistic at the appropriate support scale, a common stochastic recentering to symmetric Bernoulli biases, and the inherited finite majority lemma. The `1/N` cutoff is not cosmetic; it is the finite-use regularization at a zero probability.

For a general pair of noncommuting effects, inputting an extremal eigenstate of one target gives a Bernoulli parameter lying beyond the corresponding endpoint of the other target. Monotone likelihood ratio then proves that both the maximal-eigenvalue and minimal-eigenvalue product distances are separately bounded by the operational distance of the actual pair. This prevents cancellation between the two spectral coordinates.

### 2.3 Angular geometry for fixed spectrum

For fixed `p,q`, the manuscript identifies the angular scale

```text
K_N(p,q)
 = (p-q) sqrt(N/(p(1-p)+q(1-q)+1/N)).
```

The upper argument is the most conceptually interesting new step. The author chooses two measurement dilations and an environment gauge for which the cross overlap is a scalar multiple `c I` of the input identity. With

```text
A = sqrt(p(1-p)) + sqrt(q(1-q)),
z = (p-q) sin(h/2),
```

one obtains

```text
c^2 = A^2/(A^2+z^2).
```

Because the overlap is scalar on the entire input, it multiplies under arbitrary common adaptive use. Purifying the tester and padding a public stopping rule by ignored calls gives

```text
d_N <= 2 sqrt(1-(A^2/(A^2+z^2))^N),
```

in addition to the hybrid bound `2Nz`. This proves the stated square-root/projective crossover without assuming parallel optimality for every noisy measurement.

### 2.4 Matching angular lower witnesses

The lower comparison uses two legal pair-dependent experiments.

First, a tangent pure input turns the pair into Bernoulli laws with gap `(p-q) sin(h/2)`. This captures rare outcome behavior associated with the bias coordinate.

Second, a common random half-turn and outcome swap removes the bias and reduces the pair to the inherited unbiased measurement family. This imports the finite entangled-block witness, not an unproved exact formula.

The legal-body inequality relating `1-b^2`, `1-r^2`, and

```text
V = p(1-p)+q(1-q)
```

shows that one of these two witnesses has the desired `K_N` order. The distinction among a scalar effect, a one-sided singular effect, and a projective effect is correctly preserved: `q=0<p<1` has a square-root horizon angular scale at fixed `p`, whereas the projective corner has linear scale.

### 2.5 The all-pair metric

For two arbitrary effects, the manuscript first controls both endpoint changes, then aligns the spectra through a common two-row Bernoulli programme, and finally compares a fixed-spectrum angular leg. This gives

```text
(1/8192) min{1,H_N(E,F)}
 <= d_N(E,F)
 <= min{2,3 H_N(E,F)},
```

where `H_N` is the sum of two endpoint scales and the smaller angular scale.

The proof does not subtract lower bounds. The lower comparison takes the maximum of separate spectral and angular witnesses. The claim that nonadaptive pair-dependent witnesses already give the lower order is supported by repeating the triangle argument at the level of the nonadaptive supremum.

I find the quantifiers coherent: the known pair may determine the input or block test, but the chosen test is common to the two hypotheses.

### 2.6 The full-body covering law

The lower bound uses boxes near the projective corner

```text
p=1-alpha, q=beta,
alpha,beta comparable to t,
t=8^j/N.
```

Inside a box, both spectral coordinates and two angular coordinates have operational mesh scale `delta sqrt(t/N)`. The spectral intervals contribute order `Nt delta^(-2)` points; the angular patch contributes order `N t^(-1) delta^(-2)` points. Their product is order

```text
N^2 delta^(-4)
```

at every scale. Spectral separation keeps different scales apart, and there are order `log(N+2)` admissible scales. Thus the logarithm is a genuine accumulation of projective-corner layers.

The packing is strictly separated and therefore excludes two targets from any radius-`delta` ball regardless of the legal memoryless centre. No retraction to a selected subfamily and no common estimator is used.

### 2.7 The exact rational upper code

The upper construction uses two rational square-root-probability charts for each eigenvalue. The spectral grid contains zero and one exactly and controls product Bernoulli error through Hellinger distance. Each ordered non-scalar spectral pair receives a rational stereographic direction grid at its proved angular scale. A scalar spectral pair has one word and no direction field.

The lattice sum retains the finite-use cutoff and gives

```text
L_(N,delta) <= C N^2 log(N+2) delta^(-4).
```

The count does not pick up a spurious `log(1/delta)` factor. One payload index includes both spectral digits and the full angular address.

For rational Cartesian input data, the norm and eigenvalues may be irrational. The encoder nevertheless uses exact sign-before-squaring comparisons against rational thresholds and decodes to rational spectral values and a rational unit direction. The implementation makes no claim of optimal workspace or polynomial running time in all binary input lengths; this is the correct boundary.

---

## 3. Detailed correctness comments

### 3.1 Bernoulli endpoint estimate

The complement reduction, large-gap branch, block length choice, no-success probability estimate, and common stochastic recentering are mutually consistent. The proof explicitly keeps a block length of at least one. No Gaussian approximation or positive variance floor is hidden.

The likelihood-ratio monotonicity statement should remain accompanied by its finite count-interval argument. It is used in a direction-sensitive way in the spectral projection lemma.

### 3.2 Reference-assisted spectral programme

For aligned eigendirections, the qc measurement can be implemented by first measuring the common projective basis and then drawing a row-dependent Bernoulli bit. This remains exact on inputs entangled with a reference because the reference output blocks are the corresponding partial matrix elements weighted by the row probabilities. Pre-supplying independent row-bit arrays therefore gives a legitimate common programme upper bound for adaptive testers.

### 3.3 Scalar-overlap dilation

The key algebraic identity is sufficiently explicit. The environment gauge changes the dilation without changing the observed measurement channel. The resulting cross overlap is scalar on the full input space, which is precisely what permits iteration through arbitrary common tester operations.

At `A=0`, the proof correctly separates the projective/deterministic cases instead of using a zero-over-zero expression. At `p=q`, the angular term is absent.

### 3.4 Stopping rules

A publicly stopped tester can be embedded into an `N`-slot tester by making fixed dummy calls after the stop and discarding those outputs. The extra calls may only lower the overlap of a chosen purification; tracing them out recovers the original operational output. This is sufficient for the upper bound.

### 3.5 Projective-corner packing

The local chart is uniformly bi-Lipschitz on the selected angular square. The spectral gap is bounded below, while both endpoint variances are of order `t`. Consequently all four local coordinates have the stated operational scale. The count and cross-scale separation are correct up to absolute constants.

The theorem should continue to call the error range “sufficiently small” and not suggest a full submaximal-error covering theorem.

### 3.6 Lattice count

The spectral-grid endpoint multiplicities and redundant signed charts are included in the capacity, which is safer than quotienting them informally. The dyadic ring estimate produces `log(N+2)` because `B/sqrt(U)=sqrt(N)`; it does not depend on accuracy. This is the correct source of the logarithm in the constructed code.

### 3.7 Code legality and replay

The decoder recomputes the public layout before accepting the payload. Validation occurs before memoized lookup, avoiding Boolean/integer cache-key collisions. It checks canonical rationals, exact legality, the derived codeword count, fixed bit length, error metadata, and payload range. Target-bound replay is correctly distinguished from bare legal decoding.

The finite regression is appropriately described as implementation evidence rather than as a proof of the adaptive supremum or the continuum packing theorem.

---

## 4. The inherited structural companion and the wider GTF pipeline

The structural paper is inherited in Revision 75. Its principal results remain same-width stationarization under eventual approximate returns, stochastic purification, finite physical actions, finite-quotient boundary criteria, and the causal strong converse for fresh nondisturbing classical probes. None of those results is newly proved by the biased-measurement geometry, and the fresh-probe model must not be reinterpreted as repeated measurement of one unknown quantum system.

The active historical chain also retains spectral-entropy width laws, return-free/no-idle estimates, the exponential-accuracy crossover, uniform numerical streaming, exact Choi/instrument streaming, intrinsic instrument coding, preparation-boundary codes, coherent boundary codes, and the Revision 74 unbiased measurement geometry. These provide context and lemmas, but they remain separate resource statements with separate hypotheses.

Most importantly, the independent analytic programme remains

```text
A1 independent
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The present finite-dimensional covering theorem proves none of the raw local-limit, stopped LDP, global past-kernel, shell-conditioning, Mosco/Nisio, filtering/LAN, changing-filtration response, or posterior-contraction obligations in that programme. All aggregate completion flags correctly remain false.

The 156-page complete edition and extensive repository history are useful provenance. They do not add editorial significance to the 55-page focused theorem beyond the mathematics actually used there.

---

## 5. Reproducibility and evidentiary status

The committed build receipt records:

- a 55-page quantitative paper;
- a 41-page structural companion;
- a 156-page complete edition;
- isolated reconstruction;
- no recorded LaTeX diagnostics;
- 522 preserved predecessor labels and 557 active complete-edition labels;
- twelve exact regression suites in ordinary and optimized Python modes; and
- 3,441 new exact assertions in the biased-geometry suite, with named malformed-input and uncharged-parameter controls.

The exact reviewed SHA `16b78c8...` triggered Actions run `37181064054`. Its read-only job checked out that exact object, rebuilt the submitted sources and every PDF page, independently rebuilt the focused journal package, and preserved source-bound reconstruction evidence. This is a strong and correctly separated reproducibility chain.

The final and native-source commits are unsigned. The package does not claim a cryptographic human-author signature. Hashes, exact-head reconstruction, finite tests, and page comparison establish source identity and reproducibility; they do not establish mathematical correctness, novelty, or editorial acceptance.

---

## 6. Why the top-four threshold is not met

### 6.1 Fixed low-dimensional interface

The new full-body theorem is full only for ordered binary qubit effects. It does not treat general POVMs, higher-dimensional effects, measurement instruments with residual quantum outputs, or arbitrary memoryless channels. This is a substantial theorem, but not yet a general structure theory.

### 6.2 Comparison rather than exact optimization

The all-pair metric is determined up to large absolute constants. No exact adaptive distance formula is given away from the projective endpoint, and no optimal common strategy is characterized. The cover is asymptotically sharp only in a small-error range.

### 6.3 Supplied-description resource

The code receives exact matrix data. It is not a learning theorem for an unknown measurement, a sample/query complexity theorem, a mutable-workspace lower bound, or a finite-classical-message physical simulator. These distinctions are stated correctly, but they limit general significance.

### 6.4 Classical and specialized mechanisms

The logarithmic enhancement is interesting, yet the proof remains a finite-dimensional combination of Bernoulli endpoint regularization, scalar-overlap dilation, elementary packing, and rational charts. The manuscript does not derive a general theorem explaining boundary entropy for broad quantum statistical models.

### 6.5 Priority remains unsettled

The author-side audit is careful but is not independent priority clearance. The multi-shot adaptive rank-one-POVM literature and nonprojective entanglement-assisted discrimination literature require a direct theorem-level comparison. A top-four recommendation would require a much firmer account of exactly what remains new after those antecedents.

### 6.6 The broader repository does not close the gap

The paper cannot borrow significance from unresolved A/B/C/D projects or from the volume of retained historical material. No externally recognized broad open problem is resolved by the present binary-qubit result.

---

## 7. Required revisions before specialist submission

1. **Submit the focused quantitative article independently.** The complete research edition should remain archival, not a journal-facing submission object.

2. **Keep “ordered binary qubit measurements” in every headline.** “Full measurement body” without those qualifiers is too broad.

3. **Add Krawiec–Pawela–Puchała (arXiv:2002.05452).** Compare its multi-shot adaptive rank-one-POVM setting directly with the present all-pair binary metric and covering problem.

4. **Add the nonprojective entanglement-assisted single-shot boundary.** Datta–Biswas–Saha–Augusiak (arXiv:2012.07069) is relevant to the role of nonprojective measurements and entanglement.

5. **Obtain an independent specialist priority review.** The author-side comparison and automated searches cannot substitute for this.

6. **Separate the metric theorem from the covering theorem in the abstract.** The metric is all-pair/all-horizon; the covering law is a small-error result.

7. **Retain the “comparison up to constants” language.** Do not describe `H_N` as an exact formula for the adaptive distance.

8. **State the small-error cap wherever the payload formula appears.** The bit law is not proved uniformly for every error below two.

9. **Preserve the arbitrary-centre convention in the lower bound.** This is one of the strongest aspects of the covering theorem.

10. **Preserve the pair-dependent-witness quantifier.** The proof does not produce one estimator identifying an entire packing.

11. **Keep both endpoint probabilities visible.** A distance-to-one-face proxy gives the wrong angular scale on `q=0`, `p<1`.

12. **Explain the scalar-overlap mechanism before the asymptotic estimate.** This is the conceptual core of the adaptive upper proof.

13. **Keep the exact one-use normalization near the definition of `d_N`.** It fixes the unhalved trace convention.

14. **Do not identify the rational codec with efficient learning or physical implementation.** Input length, workspace, output expansion, and hardware remain separate.

15. **Report actual code complexity conservatively.** The reference layout uses quadratic arithmetic in the spectral grid and does not claim polynomial complexity in all encoded numerical lengths.

16. **Retain final-head read-only verification.** Bind the journal package, native source, PDFs, and theorem locations to the exact submitted SHA.

17. **Use a signed release if authorship provenance is important.** The present commits are unsigned.

18. **Keep the structural companion separate.** It is inherited and concerns a different fresh-probe interface.

19. **Keep all A/B/C/D aggregate flags unchanged.** No coding or reconstruction test discharges those analytic gates.

20. **Compress the introduction and comparison.** The focused contribution is the full biased binary effect-body metric, its projective-corner entropy, and the exact joint code; the full historical route should not dominate the journal article.

---

## 8. Detailed comments

1. The target effect body is four-dimensional, but the spectral tuple is singular at `p=q`. Dimension counts must always be made on the effect body, not on a redundant `(p,q,u)` parameterization.

2. The output labels are ordered. The common outcome swap in a lower witness is a tester operation, not a quotient of the target family.

3. The one-use formula uses the unhalved trace norm. Classical total variation is half the trace norm of a classical block.

4. The endpoint regularizer is `1/N`, not an arbitrary smoothing parameter.

5. The no-success block statistic is a lower-bound device, not an optimal decision rule.

6. The two spectral endpoint lower bounds are separate witnesses; no single eigenstate is claimed to recover both simultaneously.

7. The aligned two-row Bernoulli representation is an upper programme bound, not an exact tensor-product distance formula for every commuting biased pair.

8. The scalar cross overlap is pairwise. It is not a global environment seizer for the full effect body.

9. The dilation gauge must continue to be described as acting only on inaccessible environments and leaving the observed channel unchanged.

10. Early stopping is public. Private stopping information would have to be retained in the tester state and would change the interface.

11. On `q=0`, `0<p<1`, the fixed-spectrum angular scale is order `sqrt(N)`; it is not automatically projective.

12. At `p=q`, direction is absent and the remaining exact problem is Bernoulli product discrimination along the scalar interval.

13. At `(p,q)=(1,0)`, the inherited exact projective endpoint remains relevant. The new theorem gives a constant-comparison law, not a replacement exact formula.

14. The lower metric constant is deliberately weak. It should not be used for numerical optimality claims.

15. The nonadaptive lower statement is a supremum statement over pair-specific tests, not a simultaneous measurement theorem.

16. In the projective-corner packing, both `alpha` and `beta` must be discretized. Charging only one depth parameter would lose the four-dimensional count.

17. Cross-scale separation should continue to be proved through a spectral endpoint test, rather than inferred from parameter distance.

18. The logarithm is in `N`, not in `1/delta`. The cutoff retained in the lattice sum is essential to this distinction.

19. The scalar grid layers correctly carry one codeword. Assigning them sphere charts would overcount a non-identifiable direction.

20. The signed stereographic charts overlap; the exact capacity counts that redundancy, so no quotient argument is needed.

21. Exact radical comparisons require sign checks before squaring. The implementation correctly treats this as a validation invariant.

22. The payload is one integer index. The JSON envelope and derived tables are not part of the leading payload count.

23. Public dimension, horizon, and requested error are separate parameters. Bias, contrast, and direction are not public calibration in the new theorem.

24. Bare decoding proves legality. Approximation to a supplied target is certified only by deterministic encoder replay.

25. The cached layout validation must remain outside the cache lookup because Python booleans collide with integer keys.

26. Finite capacity samples are useful regressions but do not prove the asymptotic lattice bound.

27. The build receipt should remain explicit that finite tests do not prove the adaptive supremum or continuum covering theorem.

28. The structural fresh-probe theorem is not a theorem about repeatedly measuring one quantum system.

29. The v63 width crossover still has its recorded multiplicative gap; the present description entropy does not remove it.

30. The final publication commit is unsigned. Exact reconstruction should not be called a human signature.

31. The current proof does not cover three or more outcomes. Extending the angular/spectral noncancellation to general POVMs is not formal.

32. Higher-dimensional effects have flag and eigenspace strata of substantially different geometry. The qubit proof should not be advertised as dimension-free.

33. The codec does not learn eigenvalues from device calls. It starts from supplied exact Cartesian data.

34. The lower packing permits arbitrary legal memoryless centres but not time-varying simulators. Those are different covering objects.

35. The full historical volume should not appear to establish priority. Only theorem-level comparisons do so.

36. The paper would benefit from one schematic figure of the double-cone effect body, scalar axis, one-sided singular faces, and projective sphere, but such a figure is expository rather than mathematical evidence.

---

## 9. Final assessment

Revision 75 successfully answers the principal mathematical breadth request in r48 within the binary-qubit measurement interface. It charges bias, contrast, and direction together; proves a uniform all-pair adaptive metric comparison over the entire closed effect body; identifies the different scalar, one-sided singular, and projective regimes; derives the sharp full-body small-error entropy with its logarithmic enhancement; and constructs an exact rational legal code attaining that order.

I found no fatal gap in the new theorem chain. The paper has therefore reached the level of a strong specialist contribution.

It has **not** reached the Annals / Inventiones / JAMS / Acta threshold. The result remains confined to a fixed binary qubit qc interface, determines the adaptive metric only up to constants, proves the covering law only at small error, and leaves multi-outcome, higher-dimensional, residual-output, learning, and physical-simulation problems open. The priority boundary is not independently settled, and the wider repository pipeline remains mathematically separate and incomplete.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused submission to a strong specialist venue after independent priority review and current-literature revision.**
