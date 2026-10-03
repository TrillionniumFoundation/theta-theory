# Referee Report — General Theta Foundations I, Revision 67 (r44)

**Quantitative manuscript:** *Intrinsic Instrument Entropy, Adaptive Precision, and Positive Streaming*  
**Structural companion:** retained focused structural manuscript and complete research edition  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:**
- `revision/general-theta-foundations-i-v67-intrinsic-instrument-entropy-2026-10-03`

**Reviewed publication head:** `98a4b12126502ea41c620b58bad4b9aa30f9c72c`  
**Qualified native source:** `429a7cbe79c032386da934eb824d4ba31416ec44`  
**Source predecessor:** Revision 66 publication `58490231d19fd5c5e557e353593251f1202105fa`  
**Controlling external report:** Revision 66 r43, `0a3d74582eeeda315237ee73fdd2ac0021862184`  
**Controlling pipeline audit:** `6c2aee0e242668ff960f3bf4835c87923b8e730f`  
**Source qualification workflow:** `37107995113`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v67-external-referee-r44-2026-10-03`  
**Date:** 3 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 67 contains a coherent and technically competent new theorem package. I did not find a fatal gap in the affine-dimension computation for quantum instruments, the high-resolution diamond-metric covering law, the exact rational intrinsic-coordinate codec, the adaptive programme upper bound on a strictly positive Choi body, the repeated-Choi discrimination lower bound, or the resulting fixed-error reusable description law

```text
log_2 covering number = (s/2) log_2 N + O(1),
    s = d^2(m n^2 - 1).
```

The distinction between ordinary high-resolution description, which has coefficient `s`, and reusable fixed-error description under `N` adaptive uses, which has coefficient `s/2`, is mathematically clean. The manuscript also correctly separates the description of a supplied memoryless instrument from unknown-channel learning, physical classical simulation, mutable streaming workspace, and quantum implementation. The code package gives an exact rational encoder/decoder rather than relying on floating-point feasibility tests.

Revision 67 is nevertheless not at the level of the four leading general mathematics journals. The new leading coefficients arise from fixed-dimensional affine geometry, norm equivalence, volume packing, one classical-programme comparison, Pinsker's inequality, and repeated Choi-state testing. Their combination is useful, but the present theorem remains restricted to fixed input/output/outcome dimensions, fixed error, a strictly positive Choi interior, and a memoryless instrument reused by a common tester. The rank-deficient boundary, a joint dimension--accuracy--reuse asymptotic, the full variable-input mutable-workspace converse, and general higher-order quantum strategies remain open. The independent priority boundary is also not settled: the author-side audit is careful but is not an external novelty determination, and the adaptive-channel-discrimination literature requires a more direct comparison.

**Disposition outside the four leading general journals:** the quantitative manuscript is a plausible strong specialist contribution in quantum information, channel/instrument approximation, metric entropy, or finite-resource simulation. I would encourage a focused submission after an independent priority review, sharper separation of the v67 contribution from the large inherited archive, and completion of the exact-final-head verification chain. I would not request another wholesale reconstruction of the mathematics.

---

## 1. Scope, genealogy, and material reviewed

The highest `General Theta Foundations I` revision located in the branch survey was

```text
revision/general-theta-foundations-i-v67-intrinsic-instrument-entropy-2026-10-03
```

at publication head

```text
98a4b12126502ea41c620b58bad4b9aa30f9c72c.
```

No Revision 68 branch and no separate Revision 67 referee-ready alias were present at the time of this report. The publication commit is a direct successor of the qualified native source `429a7cbe...`. Revision 67 starts from the published Revision 66 head `58490231...` and explicitly identifies the r43 report and audit as its controlling referee documents.

I reviewed, in particular:

- `quantitative.tex` and the complete research edition;
- `sections/38-intrinsic-instrument-entropy.tex`;
- `sections/39-adaptive-description-entropy.tex`;
- the inherited Choi streaming section, including the added exact PSD validation lemma;
- `instrument_codec.py` and the codec regression program;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r43 report and proof/pipeline audit;
- the build receipt, source inventory, theorem-location data, regression records, and preservation records;
- the source-qualification workflow and the present exact-head workflow state; and
- the repository-wide frozen A/B/C/D pipeline ledger and history.

I also made a targeted comparison with metric entropy of finite-dimensional channel bodies, adaptive quantum-channel discrimination, diamond-distance channel learning, finite classical simulation of noisy and perfect channels, and programmable quantum processors. This is not a formal proof-assistant verification and not an exhaustive novelty search. Where priority remains uncertain, I treat that as an editorial limitation rather than as a mathematical counterexample.

---

## 2. Executive assessment of the new mathematics

### 2.1 The intrinsic affine dimension

For an `m`-outcome instrument from `M_d` to `M_n`, the manuscript represents each outcome map by an unnormalized input-first Choi block in the Hermitian space of order `dn`. Complete positivity is blockwise positive semidefiniteness, and joint trace preservation is the affine constraint

```text
sum_y Tr_out J_y = I_d.
```

The ambient real dimension is `m(dn)^2`. The partial-trace constraint has real rank `d^2`, so the affine dimension is

```text
s = m d^2 n^2 - d^2 = d^2(m n^2 - 1).
```

The maximally mixed instrument lies in the relative interior, so positivity does not lower the local dimension. This calculation is correct.

### 2.2 Diamond-metric entropy of the instrument body

On the trace-annihilating translation space, the proof compares the Hilbert--Schmidt tuple norm, the sum of Choi trace norms, and the instrument diamond norm. In fixed dimensions these norms are equivalent. The manuscript gives explicit inequalities sufficient for both covering and packing.

The center

```text
J_y^0 = I_(dn)/(m n)
```

has a positive operator margin. A sufficiently small ball in the affine translation space therefore remains inside the instrument body. Volume comparison in the `s`-dimensional affine space gives the lower covering bound. A rational lattice in independent affine coordinates, followed by reconstruction of the omitted trace-preserving coordinates and addition of a positive buffer, gives a legal rational upper net.

Consequently, for fixed `d,n,m`,

```text
log_2 N_diamond(eta)
       = s log_2(1/eta) + O_(d,n,m)(1).
```

The coefficient `s` is exact. I find this theorem correct in its fixed-dimensional, high-resolution regime.

### 2.3 Exact rational intrinsic-coordinate codec

The codec deletes exactly `d^2` dependent real coordinates, quantizes the remaining `s` coordinates, reconstructs the affine marginal constraint, and adds a fixed positive buffer. Its payload alphabet has cardinality `(2B+1)^s`; hence the fixed-length payload has

```text
s log_2 B + O(s)
```

bits. The encoder-produced word decodes to a completely positive jointly trace-preserving instrument and has diamond error `O(1/B)`.

This is more than an existential rational-density argument. The source implements canonical parsing, bounded payload length, the affine reconstruction, exact rational PSD checking, and explicit error metadata without floating-point decisions.

Two scope points are essential. First, arbitrary in-range digit strings need not be positive; the decoder validates and may reject them. The mathematical codebook is therefore the encoder image, not the full mixed-radix cube. Second, the advertised payload length excludes the separately supplied dimension and parameter header. This is legitimate for fixed dimensions, but it must remain visible in every variable-input discussion.

### 2.4 Adaptive reusable description on a positive Choi body

Fix a strict margin body

```text
C_a = { J : J_y >= a I for every outcome y }.
```

For two instruments in this body, the programme lemma constructs two common instruments `K_+` and `K_-` and writes the two targets as Bernoulli mixtures with nearby mixing probabilities. Reusing the same instrument `N` times therefore reduces distinguishability under any common causal tester to the classical divergence between two Bernoulli product programmes. Pinsker's inequality gives

```text
d_N(J,L) <= min{2, C_a sqrt(N) ||J-L||_2}.
```

The tester may use finite quantum memory, an entangled reference, classical feedback, and a bounded public stopping rule. Contractivity after the common programme is the correct mechanism; no independence of the tester's quantum state is assumed.

The lower bound prepares a maximally entangled state independently at every use, producing repeated normalized Choi states. A pair-dependent Helstrom test then gives exponential separation once `N ||J-L||_2^2` is large. Combined with volume packing in `s` dimensions, this yields, for fixed margin and fixed nontrivial error `delta`,

```text
log_2 N_(C_a,d_N)(delta)
       = (s/2) log_2 N + O_(a,delta,d,n,m)(1).
```

The exponent `s/2` is correct. The upper and lower metrics use the same target family, although the lower tester is much simpler than the tester class allowed in the supremum.

### 2.5 The boundary obstruction

The manuscript correctly refuses to extend the local `sqrt(N)` modulus uniformly to the boundary. A one-parameter unitary phase family with separation of order `1/N` can be amplified coherently across `N` uses to constant or perfect distinguishability. Thus strict positivity is not a technical convenience; it removes coherent boundary directions with different scaling.

This boundary example is important because it prevents a misleading global `N^{s/2}` statement for the entire compact instrument body.

---

## 3. Detailed correctness audit

### 3.1 Rank of the partial-trace constraint

The map from a Hermitian `dn x dn` block to its input marginal is onto the Hermitian `d x d` space: tensoring an arbitrary Hermitian input matrix with a fixed output density matrix supplies a right inverse. Summing over outcomes does not change surjectivity. Therefore the affine constraint has rank exactly `d^2`, not merely at most `d^2`.

The relative interior point makes all blocks positive definite, so a neighborhood in the affine plane lies in the feasible set. The use of the full affine dimension `s` is justified.

### 3.2 Norm comparison and interior radius

For a Hermiticity-preserving map with Choi matrix `X`, the diamond norm controls the Hilbert--Schmidt norm of `X` after applying the map to a maximally entangled input, while a standard Choi trace-norm estimate controls the diamond norm from above. Summing over outcomes gives the instrument inequalities used in the proof.

The exact constants are not claimed optimal and are unnecessary for the leading entropy coefficient. What matters is that the constants depend only on fixed dimensions. The proof uses them consistently.

At the central instrument, subtracting a small Hermitian perturbation whose operator norm is less than `1/(mn)` preserves block positivity. The Hilbert--Schmidt and operator norms are ordered in the needed direction, so the displayed affine ball is legal.

### 3.3 Volumetric lower bound

Let `K` be the instrument body translated to the origin in its `s`-dimensional affine space. Since `K` contains an affine Euclidean ball of radius `r` and is covered by `M` translates of an `eta`-ball in the diamond norm, norm comparison converts the latter to Euclidean balls of radius `C eta`. Volume gives

```text
M >= (r/(C eta))^s.
```

There is no appeal to an ambient dimension larger than `s`, and the affine constraint is already eliminated. This part is sound.

### 3.4 Rational upper net and positivity repair

The independent coordinates are rounded toward zero. The omitted outcome/output coordinates are reconstructed from the trace-preserving equations. This can amplify the coordinate error only by a fixed dimension-dependent factor. Adding a central positive buffer shifts every block away from the boundary while preserving the joint marginal after the denominator is adjusted as specified.

The resulting approximation error is `O(1/B)` in Hilbert--Schmidt norm and therefore in diamond norm. Rational points are explicit. The upper covering exponent is `s`.

The proof should continue to distinguish “all mixed-radix strings” from “legal codec outputs.” The implementation calls validation after reconstruction, which is the right behavior.

### 3.5 Programme upper bound

Write `Delta=J-L`, choose `r=|Delta|_2`, and select a common scale so that

```text
K_+ = J_0 + Delta/(2r),
K_- = J_0 - Delta/(2r)
```

remain in the instrument body because the targets have a uniform Choi eigenvalue margin. Then `J` and `L` are two Bernoulli mixtures of `K_+,K_-` with parameters separated by order `r/a`.

A causal tester interacting with the instrument can be viewed as a common channel applied to the hidden classical programme sequence together with its own memory. Relative entropy between the final stopped outputs is bounded by the relative entropy of the programme distributions. The public bounded stopping time can be padded to `N` programme draws, so it cannot increase the divergence beyond the length-`N` product value.

Pinsker then yields a trace-distance bound of order `sqrt(N) r/a`. This reasoning remains valid with entangled inputs, finite quantum memory, feedback, and adaptive stopping because all of those operations are identical under the two hypotheses once the programme sequence is fixed.

### 3.6 Repeated-Choi testing lower bound

At every use, feed half of a fresh maximally entangled state and retain the reference. The outcome flag plus output/reference system has normalized state equal to the direct-sum normalized Choi representation of the instrument. Repeating this nonadaptive experiment gives tensor powers.

The trace distance of the two one-use states is bounded below by a fixed multiple of the Choi Hilbert--Schmidt separation. The fidelity or affinity tensorizes, and the Fuchs--van de Graaf inequalities give an exponentially small testing error once `N r^2` is large. This establishes the needed pairwise separation in `d_N`.

The tester is allowed to depend on the pair in a covering/packing lower bound. The proof does not claim one universal measurement distinguishes the whole packing simultaneously.

### 3.7 Metric-entropy exponent under reuse

For the upper bound, choose a Hilbert--Schmidt mesh of scale `delta/sqrt(N)` in the `s`-dimensional positive body and apply the programme lemma. This gives at most `C N^{s/2}` codewords at fixed `delta`.

For the lower bound, choose a Euclidean packing at scale `C/sqrt(N)` inside a smaller positive affine ball. The repeated-Choi test separates every pair by at least `delta`. Volume gives at least `c N^{s/2}` points.

Taking logarithms proves `(s/2) log_2 N+O(1)`. The constants deteriorate as the Choi margin tends to zero or the target error tends to zero; the theorem does not claim uniformity in those parameters.

### 3.8 Exact PSD validation

The added bordered-minor/Schur-complement lemma gives an exact rational positivity test with polynomial bit complexity for fixed matrix size and, more generally, polynomial time in the explicit rational matrix input. Zero pivots are handled through the required vanishing of the corresponding row/column before continuing. This is a valid implementation-level lemma, not a substitute for the analytical covering proof.

---

## 4. Implementation and reproducibility assessment

### 4.1 Codec implementation

`instrument_codec.py` implements:

- the exact intrinsic dimension `s`;
- enumeration of independent Hermitian coordinates;
- canonical mixed-radix packing and unpacking;
- reconstruction of the omitted trace-preserving coordinates;
- positive buffering;
- exact CP and TP validation;
- a canonical bounded hexadecimal payload;
- an encoder-side diamond-error upper bound;
- exact certificate verification; and
- an adaptive grid choice scaling as `sqrt(N)` for fixed margin and error.

The source explicitly states that it encodes supplied rational data, not an unknown instrument, and that it is not quantum preparation or random sampling. This is the correct scope.

### 4.2 Regression evidence

The build receipt records more than 170,000 new exact assertions, hundreds of codec and bordered-minor cases, adaptive-grid and product-programme checks, and named negative controls. The inherited v66, v65, v64, and v63 suites also pass. No floating-point oracle is used in the new codec checks.

These are strong regression practices. They verify the reference arithmetic, parser, legality checks, finite identities, and source reproducibility. They do not prove the universal metric-entropy theorem, the adaptive programme lemma for all testers, or independent novelty.

### 4.3 Workflow status

The source qualification workflow completed successfully on the native source and produced the publication commit and recorded PDFs. The publication head contains an exact-head workflow definition, but the GitHub Actions query at the time of review returned no workflow run whose triggering `head_sha` was the reviewed publication `98a4b121...`.

Thus the accurate provenance statement is:

> the native source was successfully qualified and the resulting publication contains an exact-head verifier, but the exact final publication head had not yet received its separate read-only reconstruction run.

This is not a mathematical defect. It should be corrected before journal delivery, particularly because earlier revisions had already established a stronger exact-head attestation pattern.

### 4.4 Branch completeness

The repository contains the v67 work branch and review-ready marker file, but no distinct `revision/...-v67-referee-ready-...` alias was located. The marker should not describe an alias as completed until the branch actually exists and the exact-head run succeeds.

---

## 5. Relation to inherited results and the repository pipeline

Revision 67 inherits a very large theorem graph: compact-group stationarization and purification, finite physical actions, causal strong converses for repeatable probes, spectral-entropy width laws, exponential accuracy crossover, uniform numerical streaming, and Choi/instrument streaming from v66. The new v67 theorems do not re-prove or replace those results; they add intrinsic description entropy and adaptive reuse laws.

The new results do not close the independent repository-wide analytic programme. The frozen dependency chains involving raw local limits, stopped-path large deviations, global past kernels, Mosco/Nisio recovery, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction remain separate. The proof-status file correctly leaves all aggregate flags false:

```text
historical A2 replacement: false
B4 aggregate:              false
C2 aggregate:              false
eleven-paper aggregate:    false
whole Theta programme:     false
```

The local GTF-I paper must be judged on its own instrument/channel approximation theorems. Neither the size of the repository nor preservation of hundreds of earlier files raises the journal significance of the local result.

---

## 6. Novelty and priority

The author-side literature audit makes useful comparisons with recent work on finite classical resources for channel simulation, diamond-distance channel learning, and programme methods in channel metrology. It correctly distinguishes:

- description of a supplied channel from learning an unknown channel;
- a reusable classical description from physical simulation;
- metric entropy from query complexity;
- one pair-dependent Helstrom tester from a universal tomography procedure; and
- strict interior laws from boundary/unitary families.

However, the exact theorem-level priority boundary remains unsettled. The metric-entropy result is closely related to general finite-dimensional convex-body entropy: once the affine dimension and local norm equivalence are identified, the coefficient `s` follows by standard volume arguments. The adaptive coefficient `s/2` combines a local asymptotic programme upper bound with repeated-state discrimination and packing. The strength is the precise quantum-instrument formulation and exact codec, not a wholly new entropy or discrimination principle.

A specialist submission should include a direct comparison with adaptive quantum-channel discrimination, for example Salek--Hayashi--Winter, arXiv:2011.06569, and should explain why the present covering metric over all common causal testers is different from binary error exponents. The manuscript should also retain its comparisons with Mele--Bittel, arXiv:2512.10214, and Oufkir--Girardi, arXiv:2601.04180, which study learning unknown channels in diamond distance, and with Naik--Gisin--Banik, arXiv:2501.15807, which studies finite classical resources for physical channel simulation.

No author-written literature file should be described as independent expert priority clearance.

---

## 7. Why the four-leading-journal threshold is not met

### 7.1 Fixed-dimensional convex geometry dominates the high-resolution theorem

The coefficient `s` is exact and useful, but the mechanism is affine dimension plus norm-equivalent volumetric covering. In a top-four general journal, one would expect either a nontrivial dimension-growing law, a boundary-stratified theorem, or a consequence resolving a broadly recognized problem.

### 7.2 The adaptive law is interior and fixed-error

The coefficient `s/2` is proved on a compact strict-margin body with fixed nonzero error. The constants are not uniform as the margin or error vanishes. The boundary example shows that a single global law is false, but the manuscript does not replace it with a full rank-stratified or tangent-cone theory.

### 7.3 Important joint regimes remain open

The work does not determine the optimal joint dependence on:

- input/output/outcome dimensions;
- Choi rank or boundary stratum;
- adaptive-use horizon `N`;
- target error `delta`;
- Choi margin; and
- mutable workspace of a variable-input codec.

These are not merely leading-constant questions; they determine which geometry controls the problem.

### 7.4 The strongest testers and the simplest lower tester leave structure unused

The metric permits arbitrary finite quantum memory and feedback, but the lower bound uses repeated Choi states and binary testing. That is enough for the exponent in the strict interior, but it does not characterize when adaptivity, entanglement across uses, or higher-order comb strategies change constants or boundary exponents.

### 7.5 The wider structural companion remains specialized

The causal results concern repeatable fresh nondisturbing probes, not general irreversible hidden dynamics or repeated quantum measurement. The terminal stationarization theorem retains its own eventual-return hypothesis. These limitations remain despite the new instrument-description layer.

### 7.6 Priority is not independently closed

The package contains a targeted author-side comparison, not an external priority report. Given the rapid 2025--2026 development of channel learning, adaptive discrimination, programmable processors, and finite simulation costs, independent expert comparison is essential.

### 7.7 No external major problem is resolved

Revision 67 solves a natural internal question raised by v66: the intrinsic description dimension and the cost of reusing a strictly positive memoryless instrument. I do not see a consequence settling a recognized open problem of corresponding breadth outside the manuscript's own programme.

---

## 8. Required revisions before specialist submission

1. **Submit a focused v67 quantitative paper.** The journal-facing article should center the intrinsic entropy theorem, adaptive reuse theorem, boundary obstruction, and rational codec. The 112-page complete edition should remain archival.

2. **State the fixed-dimensional convention in every entropy theorem.** The `O(1)` terms may depend arbitrarily on `d,n,m`, the Choi margin, and the target error.

3. **Separate the full instrument body from the strict interior body.** The first has the `s log(1/eta)` high-resolution law; the second has the `(s/2) log N` adaptive fixed-error law. They are not one theorem with interchangeable parameters.

4. **Add a boundary-stratification discussion.** At minimum, formulate the open problem by Choi rank, tangent cone, and coherent/unitary directions rather than only giving one counterexample.

5. **Clarify the codebook.** Encoder outputs are legal; arbitrary payload strings may be rejected. Do not describe the entire mixed-radix cube as a legal net.

6. **Charge or freeze the header explicitly.** The leading payload theorem is for fixed dimensions and fixed public parameters. A variable-dimension theorem would need to charge headers, indexing, and validation workspace.

7. **Distinguish classical description from physical simulation.** The decoder outputs a rational matrix description. It does not implement the instrument in the laboratory and does not classically reproduce all quantum interactions without quantum hardware.

8. **Distinguish description from learning.** The encoder receives the target instrument. No sample or query complexity for discovering an unknown instrument follows.

9. **Expand the adaptive-discrimination comparison.** Include binary adaptive channel-discrimination literature and explain why `d_N` is a covering metric, not an error-exponent theorem.

10. **Complete exact-head CI.** Run the read-only exact-head workflow on `98a4b121...`, publish the attestation, and create the advertised referee-ready alias if it is part of the release convention.

11. **Keep finite tests in their evidentiary lane.** They certify arithmetic and implementation examples, not the universal analytical theorem or novelty.

12. **Keep the independent A/B/C/D pipeline out of the contribution claim.** Its aggregate flags remain false and its open analytic gates are not consequences of v67.

13. **Obtain an independent priority review.** This is especially important for programmable processors, channel learning, adaptive discrimination, metric entropy, and classical simulation literature.

14. **Reduce historical volume.** The focused submission should not require navigating the entire v1--v66 archive, frozen reports, and unrelated pipeline records.

---

## 9. Detailed comments

1. Define clearly whether an “instrument diamond norm” is the diamond norm of the flagged direct-sum channel or the sum of outcome-map diamond norms. The proof uses an equivalent fixed-dimensional convention; the exact convention should be stated once.

2. Keep the Choi normalization visible. The input-first unnormalized convention changes factors of `d` in the testing and norm inequalities.

3. The affine dimension formula assumes all `m` outcome slots remain part of the model. If zero outcomes are removed by the codec option, the effective dimension changes and should be reported as such.

4. The lower volume bound should explicitly say that volume is Lebesgue measure on the translation space of the affine constraint.

5. The rational upper net does not require every quantized string to be positive. State the net as the image of the encoder or as the set of validated reconstructions.

6. The error guarantee belongs to an encoder/target pair. Decoding a bare certificate can certify legality and syntax, but not proximity to an unspecified target.

7. The programme lemma's margin parameter should be tied to the smallest eigenvalue of every outcome Choi block, not only of their sum.

8. Explain the bounded stopping convention in one sentence: pad the programme sequence to `N` draws and let the tester ignore the unused suffix.

9. The tester class should specify whether fresh ancillas of unbounded finite dimension are allowed. In fixed system dimension this may affect only the formal definition, but it should be unambiguous.

10. The repeated-Choi lower tester is nonadaptive. Emphasize that adaptivity is allowed in the supremum but not needed for the lower packing.

11. A pair-dependent Helstrom measurement is legitimate for metric packing; it would not be a universal decoding measurement for the entire codebook.

12. Fixed `delta` is essential in the `(s/2) log N+O(1)` statement. If `delta=delta_N` vanishes, the hidden constant is no longer a constant.

13. Likewise, the strict margin `a` is fixed. No uniform statement as `a=a_N` tends to zero is proved.

14. The unitary boundary example shows failure of one global modulus, but it does not determine the entropy exponent of every boundary stratum.

15. The exact PSD validator is useful engineering evidence. Do not present polynomial-time validation as polynomial-time construction of an optimal net in variable dimensions.

16. The payload bit formula should state whether leading zero padding is conceptually included in the fixed-length code. The canonical hexadecimal serialization deliberately omits redundant leading zeroes.

17. The `preserve_zeros` option changes the active outcome count. A decoder receiving only the payload still needs the active-outcome mask in the public header.

18. The adaptive codec is a reusable **description** of one memoryless instrument. The tester's own quantum memory is not encoded in that description.

19. The description law does not upper-bound a universal programmable processor's hardware dimension without an additional physical realization theorem.

20. The build receipt is unusually detailed and should be retained in the research package, not placed in the main mathematical narrative.

21. The exact publication commit is unsigned. The package correctly makes no cryptographic authorship claim.

22. Create the referee-ready alias only after its head and exact-head attestation are frozen; otherwise the marker and branch state diverge.

23. The inherited v63 crossover multiplicative gap remains open. The v67 coefficient theorem does not remove it.

24. No syntax, regression, or PDF hash check changes the false status of the repository-wide A/B/C/D aggregate claims.

---

## 10. Final assessment

Revision 67 gives a mathematically sound and well-organized answer to a natural finite-dimensional question:

```text
How many classical description bits are intrinsically required
for a supplied quantum instrument, and how does this change when
the same strictly positive memoryless instrument is reused N times
against arbitrary common adaptive testers?
```

The answers

```text
s log_2(1/eta) + O(1)
```

for high-resolution one-shot description and

```text
(s/2) log_2 N + O(1)
```

for fixed-error reuse on a strict interior body are correct and useful. The exact rational codec makes the upper theory executable in a meaningful sense.

The work has not crossed the threshold for the four leading general mathematics journals. Its new mechanisms remain fixed-dimensional and predominantly volumetric/local; the adaptive theorem is restricted to a strict interior and fixed error; the boundary and joint asymptotic theories are incomplete; and independent priority has not been established. The wider repository programme remains open and mathematically separate.

**Recommendation: reject at the Annals / Inventiones / JAMS / Acta level; encourage a substantially focused specialist submission after the revisions above.**
