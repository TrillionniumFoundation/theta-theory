# Referee Report — General Theta Foundations I, Revision 71 (r46)

**Quantitative manuscript:** *Input-Dependent Boundary Coding and the Full Error Range*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v71-input-dependent-boundary-2026-10-03`
- `revision/general-theta-foundations-i-v71-referee-ready-2026-10-03`

**Reviewed exact final head:** `8c053f4820da3abcbb04daab628aa94379fd01e3`  
**Candidate publication:** `ab89696e486afd60c34e7407c8195bac1ad535e2`  
**Qualified native source:** `78314ce960b523adfebbfcb02c0a966d8e12380a`  
**Source predecessor:** Revision 70 final head `a5cd3bb0ea9c29f680381230c603e54354866376`  
**Controlling external report:** Revision 68 r45, `e862e5c963ef36b9caa3b1b814b495ae4428a088`  
**Controlling pipeline audit:** `a3fd5b80549a855c46151fd7183b3fc7139abac7`  
**Source qualification workflow:** `37123790238`, conclusion `success`  
**Exact-head read-only reconstruction:** `37124181836`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v71-external-referee-r46-2026-10-03`  
**Date:** 3 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 71 is a coherent and technically competent extension of the instrument-description programme. I did not find a fatal mathematical gap in the new full-error covering argument, the fixed-readout input-dependent boundary theorem, the centre retraction, the adaptive metric comparison, the rowwise rational codec, or the matching rank-stratum converse. Because Revision 70 had no separate external referee report, I also independently audited the inherited coherent/preparation tensor law, its mixed `N^{-1}` and `N^{-1/2}` scales, the rational projective-unitary atlas, and the preparation-centre retraction needed for the present manuscript. I did not find a fatal gap in those chains either.

The principal Revision 71 theorem concerns the fixed-readout measure-and-prepare family

```text
Phi_(sigma,y)(X) = sum_x <e_x,Xe_x> sigma_(x,y),
```

with public conditional output-rank bounds `r_(x,y)`. Writing

```text
V = sum_x [sum_y r_(x,y)(2n-r_(x,y)) - 1],
```

it proves the joint reusable-description law

```text
log_2 M_N(delta)
  = (V/2) log_2 N + V log_2(1/delta) + O(1)
```

uniformly for every `N >= 1` and every `0 < delta <= delta_* < 2`, at fixed dimensions, rank data, and error cap. The decoded centre may initially be any legal memoryless instrument: composition with the fixed-basis dephasing retraction cannot increase its distance to a target in this family, so arbitrary centres give no covering advantage. The rational upper code is assembled row by row from the singular preparation codec, preserves every conditional zero block, and never increases the declared conditional ranks.

A second new ingredient extends the inherited interior and preparation-family half-dimensional laws from the small-error interval to every fixed submaximal unhalved trace-distance cap. A common normalized-Choi estimator gives mean-square error `O(1/N)` for every member of a finite-dimensional patch. Disjoint estimator events and a covering-multiplicity lemma replace the invalid large-error argument based on pairwise separation by more than `2 delta`. This yields `c N^(a/2)` covering lower bounds for any fixed `a`-dimensional bi-Lipschitz patch and every fixed `delta_* < 2`.

These are meaningful improvements. They remove two local restrictions identified in r45: the absence of input dependence in the preparation boundary theorem and the small-error limitation in the half-dimensional coding laws. The manuscript also preserves the Revision 70 coherent tensor family

```text
F_(U,sigma,y)(X) = U X U* tensor sigma_y,
```

whose description length has coefficient `u+v/2` in `log N`, where `u=d^2-1` is the projective-unitary dimension and `v` is the preparation rank-stratum dimension.

The four-leading-journal disposition nevertheless remains negative. The new theorems classify reusable **descriptions of supplied fixed-dimensional matrix data** in two explicit boundary families. They do not classify the boundary of all disturbing instruments; they do not treat a varying readout basis in the cq theorem; they are not unknown-channel learning results; they do not give mutable-workspace lower bounds; and they do not provide finite-classical-resource physical simulations accepting an unknown quantum input. The full-error argument is a useful but elementary combination of standard finite-dimensional tomography, volume packing, and event multiplicity. The mixed coherent/preparation exponent is attractive, but it remains a theorem for a product family with decoupled reversible and preparation coordinates rather than a tangent-cone classification of general coherent/noisy couplings.

The priority boundary also remains incomplete. The present comparison cites Salek--Hayashi--Winter and Cooney--Mosonyi--Wilde, but it should additionally discuss the environment-parametrized and environment-seizable channel framework of Das--Wilde, Wilde--Berta--Hirche--Kaur, and Wang--Wilde. Those papers already reduce adaptive processing of suitable channel families to processing associated programme/environment states and treat classical--quantum channel discrimination. They do not contain the present finite-use family-covering exponents, rank-aware rational code, or arbitrary-centre retraction, so they do not subsume Revision 71; they are nevertheless direct antecedents for the common-processor mechanism used in the upper metric comparison.

**Disposition outside the four leading general journals:** the 29-page focused quantitative manuscript is a plausible strong specialist contribution in quantum information, finite-dimensional metric entropy, and exact rational coding. I would encourage a specialist submission after an independent priority review, an explicit comparison with environment-parametrized/cq channel-box results, and further compression of the historical framing. The structural paper remains a coherent specialist contribution, but it is inherited here and retains its fresh nondisturbing-probe and terminal-realization scope.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 71 manuscript branches are identical at

```text
8c053f4820da3abcbb04daab628aa94379fd01e3.
```

No Revision 72 branch was present in the final branch survey. The exact final head is a direct successor of candidate publication `ab89696e...` and adds the read-only exact-head reconstruction request. The candidate publication descends from native theorem source `78314ce9...`. The stated source predecessor is the completed Revision 70 final head `a5cd3bb0...`.

No Revision 69 proof-complete publication and no Revision 70-specific external referee report were located. Revision 69 is historical unfinished work; Revision 70 is a completed mathematical predecessor but had not received a separate external GTF report. I therefore reviewed the v70 coherent/preparation additions needed for the v71 decision rather than treating their author audit or successful tests as external certification.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/42-preparation-centres.tex`;
- `sections/43-coherent-boundary-codes.tex`;
- `sections/45-full-error-coverings.tex`;
- `sections/46-input-dependent-boundary.tex`;
- `coherent_codec.py` and its finite regression;
- `conditional_codec.py` and `check_conditional.py`;
- the inherited preparation, intrinsic-instrument, Choi, and streaming codecs;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r45 report and audit;
- the resource ledger, source inventory, build receipt, theorem locations, page checks, and preservation manifest;
- the source-qualification workflow and exact-head read-only workflow; and
- the frozen repository-wide A/B/C/D proof-dependency ledger.

I also performed a targeted external comparison with primary work on quantum population coding, classical--quantum and environment-parametrized channel discrimination, channel-box distinguishability, quantum reading with programme/environment states, adaptive channel discrimination, and replacer channels. This is not a formal proof-assistant verification and not an exhaustive novelty search across all quantum statistics, metric entropy, and quantization literature.

---

## 2. Executive assessment of the v71 mathematics

### 2.1 Covering multiplicity beyond the half-diameter threshold

For a common tester producing disjoint events `A_i`, suppose target `i` assigns probability at least `1-eta` to `A_i`. If one centre is within unhalved trace distance `delta` of several targets under this tester, then it assigns at least

```text
1 - eta - delta/2
```

to each corresponding event. Since the events are disjoint, one centre covers at most the reciprocal of this quantity. Hence a cover of `K` targets needs at least

```text
(1 - eta - delta/2) K
```

centres.

This is the correct replacement for the usual pairwise-packing argument when `delta > 1`: in a metric of diameter two, no pair can be separated by more than `2 delta` in that regime. The factor `delta/2` is consistent with the manuscript's unhalved trace-norm convention.

### 2.2 A common finite-dimensional estimator

The normalized flagged Choi state is expanded in a Hilbert--Schmidt orthonormal Hermitian basis of the ambient block space. The proof divides the `N` samples among the basis coordinates and estimates each expectation using the binary observable `(I+H_j)/2`. Since Hilbert--Schmidt norm one implies operator norm at most one, this is a valid effect.

For `N` at least the number of basis elements, the variance sum is bounded by a constant times `1/N`. For smaller `N`, the zero estimator has uniformly bounded error and the displayed larger constant still covers it. Markov's inequality then gives a common estimator ball with probability at least `1-eta` for every target in the patch.

The proof does not claim sample optimality. Its role is only to supply one common family-independent witness for multiplicity control.

### 2.3 The full submaximal-error patch theorem

Let a compact target family contain an `a`-dimensional Euclidean parameter ball on which the normalized Choi map is bi-Lipschitz. Pack it at radius proportional to `N^{-1/2}`. The common estimator balls around the packing points are disjoint. Choosing

```text
eta = (2-delta_*)/4
```

gives

```text
1 - eta - delta_*/2 = eta > 0.
```

The multiplicity lemma therefore converts the Euclidean packing cardinality into a covering lower bound `c N^(a/2)` uniformly for every `delta <= delta_* < 2`.

This is correct. The constant necessarily degenerates as `delta_*` approaches two, and no uniform statement at the maximal error is obtained.

### 2.4 Fixed-readout input-dependent instruments

The family is specified by a public orthonormal input basis. For each basis symbol `x`, the conditional output blocks form a classical--quantum state

```text
Omega_x = direct_sum_y sigma_(x,y),
```

of trace one. A channel use first measures the input in the fixed basis and then emits the corresponding row state.

The rank-stratum dimension of one row is

```text
v_x = sum_y r_(x,y)(2n-r_(x,y)) - 1,
```

so the product family has dimension `V=sum_x v_x`. The normalization removes one real coordinate per row, not one globally. This is the correct dimension count because each input row is independently trace normalized.

### 2.5 Arbitrary-centre retraction

Let `Pi` be the fixed-basis dephasing channel. Every target satisfies `Phi Pi = Phi`. Given any legal memoryless centre `K`, define the retracted centre `K Pi`. For every tester against `Phi` and `K Pi`, insert `Pi` immediately before each unknown device call. This produces an admissible tester against `Phi` and `K` with exactly the same two output states, because the target is fixed by `Pi`.

Therefore

```text
d_N(Phi, K Pi) <= d_N(Phi,K).
```

This establishes that arbitrary legal memoryless centres offer no covering advantage. It does **not** say that the retraction preserves centre ranks; the manuscript and regression suite correctly give counterexamples to such a claim.

### 2.6 The adaptive metric sandwich

For each input row, repeatedly feed the basis state `|x><x|` and retain all output flags and states. This proves the lower bound

```text
max_x ||Omega_x^tensor N - Lambda_x^tensor N||_1
  <= d_N(Phi_sigma,Phi_tau).
```

For the upper bound, provide one copy of every conditional row state at every slot to a fixed processor. The processor measures the incoming system in the fixed basis, selects the corresponding programme row, discards unused row states, and executes the common tester's interleaving operation. The same processor works for both hypotheses. Trace-norm contraction gives

```text
d_N(Phi_sigma,Phi_tau)
 <= || tensor_x Omega_x^tensor N
       - tensor_x Lambda_x^tensor N ||_1.
```

This common-processor construction remains valid with an initially entangled reference, finite quantum memory, adaptive feedback, and bounded public stopping. It is an instance of the established environment/programme-state methodology and should be positioned as such.

For one use the exact distance is the maximum row trace distance. The upper proof writes the output difference as a sum of positive reference weights tensored with row differences; triangle inequality gives the maximum, and a basis-state input attains it.

### 2.7 Rowwise rational code

Each conditional row is encoded by the inherited singular preparation codec. The row factor coordinates have dimension at most `v_x+1`. Choosing a common grid

```text
B >= 4 sqrt(N V)/delta
```

and using the product-purification estimate gives total squared adaptive error at most

```text
16 N V / B^2.
```

The Cartesian product of the row codebooks has cardinality at most a fixed constant times `(sqrt(N)/delta)^V`. Every decoded block is positive semidefinite, each row remains trace normalized, zero conditional blocks remain zero, and no conditional rank increases.

For rational targets the implementation computes squared Cholesky-factor coordinates through exact rational Schur residuals and uses integer square roots; it does not store algebraic factors. For arbitrary real targets the theorem is an existence statement producing rational integer-factor centres.

### 2.8 Matching lower bound

In every nontrivial row choose a small smooth maximal-rank factor patch of dimension `v_x`. The product of these patches has dimension `V` and is locally bi-Lipschitz in tuple Hilbert--Schmidt norm. At small error, the normalized-Choi binary test gives separation at scale `delta/sqrt(N)`. At larger fixed error, the common-estimator patch theorem gives the `N^(V/2)` factor, while the additional `delta^{-V}` term is bounded above and below by constants on the fixed interval away from zero.

The lower centres may be arbitrary legal instruments because the packing argument uses only metric balls, and the retraction theorem separately shows that restricting centres to the fixed-readout family does not change the covering cardinality.

I find this chain correct in its stated fixed-dimensional scope.

---

## 3. Independent audit of the unreviewed v70 additions

### 3.1 Preparation-centre retraction

For any instrument centre `C`, feed the maximally mixed state into its input and use the resulting output blocks as a preparation instrument `R(C)`. If the target is input-erasing, a tester against the target and `R(C)` can be converted into a tester against the target and `C` by replacing each device input with the maximally mixed state. This proves that arbitrary centres give no advantage for covering a preparation family.

The map is legal, rationality preserving, and idempotent. It need not preserve ranks. The proof is sound.

### 3.2 Coherent/preparation tensor family

The Revision 70 family combines a projective unitary coordinate with a preparation coordinate. Let

```text
u = d^2-1,
V_prep = sum_y r_y(2n-r_y)-1.
```

The theorem gives

```text
log covering number
 = (u+V_prep/2) log_2 N
   + (u+V_prep) log_2(1/delta) + O(1)
```

for the stated small-error range.

Discarding the preparation output leaves the unitary channel and yields a coherent lower modulus of order `min{N chi(U,V),1}`. Discarding the data output leaves the preparation experiment and yields the `sqrt(N)` modulus. Conversely, a hybrid argument bounds the unitary change by `O(N chi)` and a common-programme processor bounds the preparation change. Product packings give the mixed exponent.

The unitary lower argument is valid: choose two eigenphases of `U*V` whose sine separation controls the projective chordal metric and reuse the evolving data output through a suitable number of calls. The rational unitary atlas uses finitely many stereographic charts for Givens rotations and diagonal phases. It is a terminating finite search, not an efficient variable-dimensional encoder.

The qubit reference implementation uses rational quaternion charts and exact target replay. I found no fatal gap in this predecessor chain.

### 3.3 Remaining limitation

The coherent theorem is not extended to the whole error interval by Revision 71. Its `N^{-1}` local scale is qualitatively different from the common-tomography `N^{-1/2}` scale, and the manuscript correctly refuses to infer a full-range coherent theorem from the new multiplicity lemma alone.

---

## 4. Implementation and reproducibility assessment

### 4.1 Conditional codec

`conditional_codec.py`:

- rejects targets with off-diagonal input-basis Choi blocks instead of silently dephasing them;
- extracts and validates every conditional preparation row;
- computes the declared product-family dimension;
- chooses the least sufficient common integer grid;
- calls the exact rank-aware row codec;
- joins rows with an exact common denominator;
- verifies the total squared error certificate;
- validates payload lengths and public headers;
- supports exact target-bound canonical replay; and
- exposes dephasing retraction as a separate operation.

The implementation correctly distinguishes bare decoding, which certifies syntax and legality, from target-bound verification, which re-runs the canonical encoder. Public dimensions, ranks, horizon, and tolerance are not counted in the displayed payload; pivot masks and integer bodies are counted. Expanded matrices and encoder workspace remain separate resources.

### 4.2 Conditional regression

`check_conditional.py` exercises:

- random fixed-readout families across small dimensions;
- exact row extraction and reassembly;
- rank nonincrease and zero-block preservation;
- very small rational eigenvalues and nonleading pivots;
- pure programme-state tensor bounds;
- adaptive classical policies whose chosen input depends on past outputs;
- centre retraction and a rank-increase counterexample;
- the common-estimator variance identities;
- the large-error multiplicity coefficient;
- target replay, malformed headers, altered certificates, and rank violations; and
- the actual command-line interface.

These checks use exact arithmetic and contain named negative controls. They are strong implementation evidence, not a proof of the continuum covering theorem.

### 4.3 Coherent implementation

`coherent_codec.py` implements the qubit quaternion code, a general finite rational unitary atlas, exact projective-distance checks, the preparation-centre retraction, tensor-instrument assembly, and target-bound certificate replay. The general atlas search has no practical efficiency claim. The finite regression explicitly treats a finite search cap as inconclusive rather than as evidence that no codeword exists.

### 4.4 Build and workflow evidence

The build receipt records:

- a 29-page quantitative paper;
- a 40-page structural paper;
- a 130-page complete edition;
- isolated rebuilding;
- no recorded LaTeX diagnostics;
- ordinary/optimized test agreement;
- 155 predecessor native files;
- 438 preserved predecessor labels and 460 active complete-edition labels;
- 5,868 new exact conditional assertions;
- 4,712 inherited v70 coherent assertions; and
- successful execution of all earlier regression suites.

Source qualification run `37123790238` completed successfully on native source `78314ce9...`. Exact-head run `37124181836` checked out `8c053f48...` without retained credentials, verified sources, pages, tests, and immutable predecessor files, independently reconstructed the minimal journal package, and uploaded a read-only attestation.

This is a strong source/reproduction chain. The final commit is unsigned, and the package correctly makes no cryptographic authorship claim. Neither CI nor finite regression is a mathematical proof or a priority certificate.

---

## 5. Why the four-leading-journal threshold is not met

### 5.1 The main object is a supplied-description problem

The encoder receives the target matrices. It does not infer them from channel queries or physical copies. The theorem counts a reusable classical description, not learning samples, tomography queries, online workspace, implementation hardware, or a physical classical simulator.

### 5.2 The boundary classification is partial

Revision 71 handles a fixed-readout cq family. Revision 70 handles a tensor product of a unitary channel and an input-erasing preparation. These are valuable model families, but they do not classify arbitrary Choi support changes, varying measurement bases, coherent/noisy couplings, or general higher-order processes.

### 5.3 Fixed-dimensional constants are essential

All dimensions, labelled outcomes, rank bounds, and the full-error cap are fixed public parameters. The proofs do not provide dimension-uniform constants or a simultaneous growing-dimension theorem. Header, index, and schema costs are outside the leading fixed-dimensional payload formula.

### 5.4 The full-error extension is conceptually modest

The multiplicity lemma is useful and correctly fixes the large-error packing issue, but the ingredients are standard finite-dimensional tomography, Markov's inequality, disjoint events, and Euclidean volume. This is not by itself a breakthrough of the breadth expected at a leading general mathematics journal.

### 5.5 The half-parameter scale has strong antecedents

The coefficient `dimension/2` under repeated use or repeated copies is consistent with classical parametric coding, local asymptotic statistics, and quantum population compression. The manuscript's exact legal rank-aware rational code and finite-use adaptive covering interface are the distinctive contributions; the scale itself is not a new universal principle.

### 5.6 Direct programme/environment antecedents need fuller treatment

Das--Wilde introduce environment-parametrized memory cells and analyze adaptive protocols through associated environment states. Wilde--Berta--Hirche--Kaur establish asymptotic cq-channel discrimination results and treat environment-parametrized/environment-seizable classes. Wang--Wilde develop channel-box distinguishability and note significant simplifications for classical--quantum and environment-seizable channel boxes. These are not finite-use covering theorems, but they are direct conceptual antecedents for the common-processor upper bound and should appear in the focused comparison.

### 5.7 The structural companion is inherited and specialized

The structural article remains based on terminal convex outputs, eventual approximate returns for stationarization, and fresh repeatable nondisturbing classical probes for its causal strong converse. It is not a general irreversible hidden-process or repeated-quantum-measurement classification.

### 5.8 The wider Theta pipeline is open

The frozen A/B/C/D graph still requires raw unsmoothed local limits, stopped-path entropy/LDP recovery, one global past kernel, canonical shell conditioning, process CLT and Mosco recovery, nonlinear Nisio resolvents and graph cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction. None of the finite-dimensional coding theorems supplies those objects. All aggregate completion flags remain false.

### 5.9 No external major problem is settled

Revision 71 closes internal gaps in an evolving programme. It does not presently resolve a recognized external open problem of comparable breadth, nor does it establish a general boundary theory for quantum instruments.

---

## 6. Required revisions before specialist submission

1. **Submit the focused quantitative paper as the primary object.** Keep the 130-page complete edition as repository history, not as the journal manuscript.

2. **Separate v70 and v71 novelty explicitly.** The coherent/preparation mixed exponent and unitary atlas are inherited Revision 70 results; the full-error and fixed-readout results are Revision 71.

3. **Add Das--Wilde, Wilde--Berta--Hirche--Kaur, and Wang--Wilde to the theorem-level comparison.** Explain environment-parametrization, cq discrimination, and channel-box simplifications, then state exactly what the finite-use covering and rational codec add.

4. **Retain the fixed-readout hypothesis in every headline.** “Input-dependent boundary” without the public dephasing basis would be too broad.

5. **Keep the fixed-dimensional convention on page one.** Dimensions, outcome labels, rank bounds, horizon, tolerance, and error cap are public; only the reusable payload is counted.

6. **Keep unhalved trace norm visible.** Event probabilities differ by at most half the displayed metric radius.

7. **Separate centre retraction from rank preservation.** The retracted centre may have larger ranks. Rank preservation belongs to the explicit upper codec, not the no-advantage theorem for arbitrary centres.

8. **Distinguish the metric sandwich from an equality theorem.** Equality is proved at one use and for the preparation subfamily, not for general `N` in the fixed-readout family.

9. **State the error ranges separately.** The half-dimensional interior, preparation, and fixed-readout laws extend to each fixed `delta_*<2`; the coherent mixed-scale theorem retains its small-error range.

10. **Do not identify descriptions with programme hardware.** A rational codeword specifies a mathematical quantum operation; it is not a bound on the Hilbert-space dimension of a universal processor.

11. **Do not identify descriptions with learning.** The target is supplied. Query/sample complexity remains a separate problem.

12. **Document real-target versus rational-target implementation.** The rational CLI is exact for rational inputs. The general real-target upper theorem is an existence/construction statement in exact real arithmetic.

13. **Preserve the legal-codebook convention.** Covering centres are decoded legal instruments. Arbitrary raw integer bodies, altered headers, and unverified certificates are not codewords.

14. **Expose the exact final-head workflow in the release record.** The present evidence is good; a signed release would improve provenance but is not a substitute for proof.

15. **Obtain independent priority review from quantum-information/statistical-experiment experts.** The author-side audit is careful but cannot certify absence of equivalent formulations.

16. **Keep the A/B/C/D graph out of the local significance claim.** No aggregate closure follows from the coding results.

---

## 7. Detailed comments

1. The definition of `d_N` should remain in the focused article immediately before its first use, including references, feedback, and bounded public stopping.

2. The normalized flagged Choi convention should retain the factor `1/d`; otherwise the constants in the local binary test change.

3. In the multiplicity lemma, explicitly state that the `A_i` are events in one common output sigma-algebra produced by one common tester.

4. The full-error lower constant depends on the fixed cap `delta_*`; no uniformity as `delta_* -> 2` should be suggested.

5. The common estimator is not an optimal tomography protocol. Calling it merely an informationally complete estimator is preferable.

6. The patch theorem needs a quantitative inverse Lipschitz constant on a compact subpatch. The current proof supplies the right compactness argument; retain it.

7. Every conditional row has its own trace-one constraint, explaining the subtraction of one in each `v_x`.

8. The fixed-readout family includes noncommuting output rows and zero blocks, but the input measurement basis is fixed and classical.

9. The input retraction is composition on the input side. State the composition convention next to the formula.

10. The centre-retraction proposition applies to memoryless centres. Do not silently extend it to arbitrary memoryful processes without an explicit process-level composition definition.

11. The upper programme uses one copy of every row state per slot. Unused rows are discarded; this overhead is not counted as a physical implementation resource.

12. The one-use metric equality is a useful exact statement and should be displayed separately from the `N`-use sandwich.

13. The rowwise factor code counts each pivot mask. Public rank bounds do not identify the actual pivot set.

14. Zero conditional blocks are preserved by the encoder because they have no factor columns; centre retraction alone does not provide that property.

15. The common denominator assembled by an lcm is part of the expanded decoded representation, not the fixed-length compressed payload.

16. Target-bound verification should continue to compare the complete canonical JSON object, so extra or altered fields cannot be silently accepted as the same certificate.

17. The coherent family uses projective unitaries. Global phase is correctly removed from the dimension `d^2-1`.

18. The general rational unitary atlas is a finite exhaustive construction, not a polynomial-time encoder in variable dimension or precision.

19. The coherent lower bound uses a pair-dependent eigenvector superposition and a number of calls depending on the pair; this is legitimate for pairwise packing.

20. The full-error theorem must not be advertised as closing the coherent transition for large error.

21. The structural article's repeatable probes are oracle-like fresh classical observations, not nondestructive repeated measurements on one unknown quantum system.

22. The exact-head run verifies source identity and reproduction, not independent authorship; the reviewed commit remains unsigned.

23. Finite tests validate formulas and implementations but do not certify all adaptive testers, continuum packing, or novelty.

24. Preserve the explicit false aggregate pipeline flags in all release summaries.

25. The focused introduction should lead with the two new v71 theorems and move the long revision genealogy to a repository note.

26. The conclusion should formulate the next mathematical boundary precisely: varying readout bases and general coupled coherent/support-changing tangent directions.

---

## 8. Final assessment

Revision 71 makes two legitimate advances over the last externally reviewed object:

- it extends the half-dimensional reusable-description laws to every fixed submaximal error cap by a correct common-estimator/multiplicity argument; and
- it proves a matching joint horizon--accuracy law, arbitrary-centre retraction, and exact rank-aware rational upper code for a genuinely input-dependent fixed-readout cq boundary family.

The unreviewed Revision 70 predecessor also contains a coherent mixed-scale theorem that appears mathematically sound in its declared tensor-product family. The implementation and reproducibility package is unusually strong, and the exact final head has a successful read-only reconstruction.

The package nevertheless remains below the Annals / Inventiones / JAMS / Acta threshold. Its strongest new conclusions are fixed-dimensional coding laws for supplied descriptions in explicit channel families; the general instrument boundary, growing-dimension regime, mutable-space converse, learning problem, physical simulation problem, and independent priority boundary remain open. The repository-wide analytic programme is separate and incomplete.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused specialist submission after direct environment-parametrized/cq-channel comparison and independent priority review.**
