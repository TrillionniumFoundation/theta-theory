# Referee Report — General Theta Foundations I, Revision 66 (r43)

**Quantitative manuscript:** *Reference-Stable Rational Instruments, Positive Streaming, and Spectral Space Bounds*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v66-reference-stable-instruments-2026-09-29`
- `revision/general-theta-foundations-i-v66-referee-ready-2026-09-29`

**Reviewed exact final head:** `58490231d19fd5c5e557e353593251f1202105fa`  
**Candidate publication:** `84950347e006fec07ac6766bced3f07d82a5ee6d`  
**Qualified native source:** `3050a45908c5de2858fe578b9383e17ca43b7d74`  
**Source predecessor:** Revision 65 final head `34e5719ce5c7109c8c31f98079716b8ce6dcfffe`  
**Controlling external report:** Revision 65 r42, `5c0796bc1f0ea24d379dfd28888f16d88315a525`  
**Controlling proof/pipeline audit:** `b5d71e67b879f9ada861993caedf8151734f85ba`  
**Source qualification workflow:** `36546520706`, conclusion `success`  
**Exact-head read-only reconstruction:** `36547235610`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v66-external-referee-r43-2026-09-29`  
**Date:** 29 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 66 gives a substantial and mathematically coherent answer to the principal interface objections in r42. Revision 65 supplied a positivity-preserving numerical repair of known density matrices and a fixed-input rational instrument streamer, but that nonlinear state repair could not be tensored with an identity on an unknown reference system. Revision 66 does not make that invalid move. It instead rounds an instrument description once, at the Choi level, and proves that the repaired blocks are exactly completely positive and jointly trace preserving. The resulting rational instrument has an explicit denominator and a certified diamond-error bound. The comparison is stable under arbitrary common adaptive quantum testers, initially entangled references, tester memory, feedback, and bounded public stopping.

The second new theorem removes the fixed-dimension and fixed-Kraus-description restriction on the constructive side. One program accepts variable rational Choi data, validates positivity and partial-trace constraints with exact reduced-rational arithmetic, samples branch outcomes from exact integer weights, and alternates between a positive fixed-denominator state grid and an exact unnormalized fallback. The entire input description, dimension, denominator lengths, validation workspace, temporary arithmetic, expected random-bit use, and worst-case trial storage are explicitly separated. I did not find a fatal gap in the Choi repair, the Choi-to-diamond estimate, the adaptive hybrid, the stopped posterior inequalities, the integral trajectory identity, the mode selection, or the stated space accounting.

Revision 66 therefore resolves two genuine deficiencies of Revision 65:

1. it provides an external-reference-stable **mathematical instrument approximation**, rather than only a nonlinear numerical state repair; and
2. it gives a variable-description **numerical upper algorithm**, rather than only a fixed-input asymptotic implementation.

The four-leading-journal disposition nevertheless remains negative. The new arguments are clean and useful, but their conceptual core is a finite-dimensional arithmetic regularization of classical Choi constraints, followed by a standard diamond/hybrid comparison and a rational trajectory implementation. The variable-data result is an upper theorem; no matching lower theorem is proved for general disturbing instruments, general transcript-only interfaces, variable dimension, or arbitrary rational Choi descriptions. The inherited sharp lower bounds still require a fixed expanding unitary subsystem, a full action spectral gap, all-direction cap bounds, and a legal numerical matrix output. The dimension dependence of the new repair is safe rather than sharp, and no optimal metric entropy, encoding length, validation complexity, or leading constant is established.

The paper also remains highly specialized. The structural strong converse concerns fresh repeatable nondisturbing classical probes, not general quantum measurement, a POMDP, or arbitrary irreversible hidden dynamics. The exponential-accuracy width theorem still has a subexponential multiplicative gap. The exact theorem-level priority boundary is not independently settled. In particular, the present literature audit omits Naik--Zartab--Gisin--Banik, *No-Go Theorem for Generic Simulation of Qubit Channels with Finite Classical Resources*, arXiv:2501.15807v2. That work proves that a perfect qubit channel cannot be simulated by any finite-round purely classical messaging protocol in a reference-sensitive joint-measurement model, whereas noisy depolarizing channels admit finite-resource simulation. Its operational task is not the same as the present rational Choi-description approximation, so it does not invalidate the new theorems. It is, however, a directly relevant neighboring boundary and must be discussed whenever the manuscript distinguishes a mathematical instrument description from a physical classical simulator acting on unknown or entangled input.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is now a strong specialist contribution in quantum information, positive numerical realization, or finite-memory simulation. The structural manuscript is also a coherent specialist-level contribution if its repeatable-probe scope remains explicit. I would encourage separate submissions after an independent priority review, a current-literature revision, and further compression. I would not request another wholesale reconstruction of the mathematics.

---

## 1. Scope, genealogy, and material reviewed

The two advertised Revision 66 manuscript branches are identical at

```text
58490231d19fd5c5e557e353593251f1202105fa.
```

No later `General Theta Foundations I` revision was present in the branch survey used for this report. Revision 66 is four commits ahead of the exact Revision 65 final head. The final commit requests a read-only reconstruction of the already published candidate; it identifies the candidate, qualified source, controlling r42 reports, and source qualification run.

No existing r43 review branch was present. The present review branch was created directly from the exact final head. It modifies no manuscript source, PDF, evidence file, workflow, predecessor directory, review branch, or default branch.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/36-reference-instruments.tex`;
- `sections/37-uniform-choi-streaming.tex`;
- `CHOI_INPUT_SCHEMA.md`;
- `choi_streaming.py` and the inherited `instrument_streaming.py`;
- `check_choi.py` and the retained v65/v64/v63 exact suites;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the complete r42 external report and companion proof/pipeline audit;
- the inherited positive-state repair, fixed-input instrument simulation, matrix-space, spectral entropy, accuracy-crossover, and causal strong-converse chains;
- the build receipt, theorem locations, source hashes, page checks, package manifests, and preservation manifest;
- source qualification run `36546520706`;
- exact-head read-only run `36547235610`; and
- the frozen repository-wide A/B/C/D pipeline history and ledger.

I also made a targeted current-literature check concerning reference-sensitive classical simulation, Choi correction, quantum strategies, process tomography, filtering, and diamond-distance channel learning. This is not an exhaustive priority search and should not be represented as one.

---

## 2. Executive assessment of the new mathematics

### 2.1 Rational Choi repair

For an instrument from `M_d` to `M_n` with `m` outcomes, the paper fixes the input-first unnormalized Choi convention

```text
J_y >= 0,
Sum_y Tr_n J_y = I_d.
```

Starting from Hermitian coordinate approximations `T_y` on a grid of scale `1/B`, the construction first repairs the summed output partial trace by adding the residual to one fixed outcome and output coordinate. It then adds a uniform positive identity buffer to every block and normalizes by one common integer denominator.

With

```text
c = 2 n d (1 + m n),
D = B + m n c,
```

the repaired blocks are

```text
Jtilde_y = (B Q_y + c I_(dn))/D.
```

They are positive semidefinite, have Gaussian-integer numerators, and satisfy the instrument partial-trace identity exactly. The stated bound is

```text
||F-Ftilde||_diamond
 <= Sum_y ||J_y-Jtilde_y||_1
 <= 3 m n d c/(B+m n c)
 <= 6 m n^2 d^2 (1+m n)/B.
```

This is an effective finite-description statement. It does not rely on a spectral decomposition, a nearest positive projection, or a rational Kraus factorization.

### 2.2 Reference-stable adaptive comparison

The repaired instrument is compared to the original with the outcome retained. A one-slot diamond bound is therefore stable against an arbitrary auxiliary quantum reference. Replacing uses one at a time gives an additive hybrid estimate. The common tester may retain quantum memory, begin with an entangled state, perform arbitrary channels and finite-outcome measurements between uses, and select a classical command from the public history and measured tester memory.

A bounded public stopping rule is handled by an absorbing halt flag and identity evolution after stopping. Thus all experiments can be completed at the common horizon without conditioning on a rare stopping event. The final joint trace-norm error is at most the sum of the one-use diamond errors.

This theorem correctly excludes coherent superpositions of commands, which are not part of the declared interface. It also correctly says that a rational instrument description is not a classical physical device capable of accepting an unknown entangled input and preparing the output.

### 2.3 Stopped posterior bounds

For stopped subnormalized blocks

```text
A_h = p_h rho_h,
Ahat_h = q_h rhohat_h,
```

an aggregate block trace error `delta` gives

```text
Sum_h p_h ||rho_h-rhohat_h||_1 <= 2 delta,
P_p{||rho_h-rhohat_h||_1 > eta} <= min{1,2 delta/eta}.
```

Pooling an event of true probability `alpha` gives normalized conditional error at most `min{2,2 delta/alpha}`. The manuscript does not infer simultaneous accuracy for every rare history. This is the correct distinction.

### 2.4 Variable-description Choi streaming

The new numerical program accepts:

- a variable dimension `d`;
- a positive Gaussian-integer initial matrix;
- a finite command dictionary;
- for each command, positive Gaussian-integer Choi blocks and a positive denominator satisfying the exact partial-trace identity; and
- horizon and accuracy parameters.

The integral branch action is

```text
(S_(a,y))_(alpha,beta)
   = Sum_(i,j) (C_(a,y))_(i alpha,j beta) P_(i,j).
```

For the input-first convention, no transpose or conjugation of `P_(i,j)` belongs in this formula. Positivity follows from complete positivity; the summed branch traces equal `D_a tr P`.

The theorem charges the complete encoded input length `S`, the matrix dimension, denominator bit lengths, parameter storage, temporary arithmetic, and validation. With

```text
H = ceil(log_2(D_*+1)),
ell_0 = ceil(log_2(z_0+1)),
Q = ell_0 + N H,
b = L + ceil(log_2(6 d^2 (N+1))),
u = min{Q,b},
```

the post-validation streaming space is

```text
O(S + d^2[H + log(d+1) + u] + log(N+1)).
```

The total peak is explicitly the maximum of this bound and the separately charged polynomial validation workspace.

### 2.5 Exact and grid modes

In exact mode, the simulator stores a selected unnormalized positive numerator. The trace is at most `z_0 D_*^t`, so each entry has `O(ell_0+tH)` bits. Accumulated scalar denominators cancel from outcome probabilities and normalized states.

In grid mode, the simulator applies each rational Choi instrument to the current approximate positive state, samples from the resulting exact integer branch weights, and repairs only the selected normalized branch to the common state denominator. The branch probabilities are computed from the stored approximate state, not from an unavailable exact state. The inherited mass-weighted recursion accounts for this difference.

The program chooses exact mode when the exact numerator bound is cheaper and grid mode otherwise. This is an order-level switch, not a claim of optimal memory for every small instance.

### 2.6 Validation and resource accounting

Variable dimension requires a different validator from the inherited fixed-dimensional fraction-free routine. The new validator uses exact reduced-rational Schur complements. A zero pivot is accepted only when the corresponding row and column vanish. Positive pivots are eliminated by block congruence. The remaining entries are ratios of minors, and Hadamard bounds keep their binary lengths polynomial in the explicit input size.

Outcome sampling uses rejection from a binary interval. The expected number of trials is below two. Rejected words and trial counters are not retained. Thus expected time and expected fresh-bit use are separated from worst-case storage per trial. The CPython allocator and operating-system entropy source are not claimed to be a formal bit-machine implementation or an ideal fair-bit certificate.

---

## 3. Detailed correctness audit

### 3.1 Choi normalization and dimension factors

The manuscript consistently uses unnormalized Choi matrices. Consequently

```text
Sum_y tr J_y = d,
```

not one. This factor is used correctly in the trace-norm estimate. The output partial trace, rather than the input partial trace, appears because the input factor is first in the tensor convention.

### 3.2 Choi-to-diamond inequality

The lower estimate follows by applying the amplified map to the normalized maximally entangled state, whose image is `J/d`.

For the upper estimate, rank-one trace-class inputs are represented as

```text
u = (A tensor I) Omega,
v = (B tensor I) Omega,
```

with Hilbert--Schmidt norms one and hence operator norms at most one. The amplified image is a left/right compression of the Choi matrix and has trace norm at most `||J||_1`. Singular-value decomposition extends the estimate to every trace-class input and arbitrary auxiliary dimension.

The direct-sum outcome register makes the instrument Choi matrix block diagonal, so the block trace norms add. I find this argument sound.

### 3.3 Coordinate error and the positive buffer

For a Hermitian `dn` by `dn` coordinate error, counting independent real coordinates gives the safe bound

```text
||T_y-J_y||_op <= ||T_y-J_y||_F <= 2 n d/B.
```

For Hermitian `E`, the output partial trace satisfies

```text
||Tr_n E||_op <= n ||E||_op.
```

Thus the common residual is at most `2 m n^2 d/B` in operator norm, and every corrected block differs from its target by at most `c/B`. Adding `c I` to the integer numerator makes it positive semidefinite.

Summing the partial traces gives

```text
B I_d + m n c I_d = D I_d,
```

so trace preservation is exact after division by `D`.

### 3.4 Diamond-error constant

Writing `F_y=Q_y-J_y`,

```text
D(Jtilde_y-J_y) = B F_y + c I_(dn) - m n c J_y.
```

The three sums of trace norms are bounded respectively by

```text
m n d c,
m n d c,
m n d c.
```

The last uses positivity and total Choi trace `d`. This yields the displayed `3mndc/D` bound. Substituting `c` gives the stated safe `K/B` estimate. The constants are not optimized, and the paper does not claim otherwise.

### 3.5 Bit length of repaired blocks

The exact partial-trace identity bounds every diagonal entry of every positive numerator by `D`. Positivity then gives

```text
|a_ij|^2 <= a_ii a_jj <= D^2.
```

Hence every Gaussian-integer entry and the common denominator have logarithmic length in `D`. The total explicit description length has the stated matrix-entry factor.

The term “positive Gaussian-integer matrix” should always be read as “positive semidefinite matrix with Gaussian-integer entries,” not as entrywise positivity. I recommend changing the phrase throughout to prevent ambiguity.

### 3.6 Adaptive hybrid and stopping

At the changed slot of two adjacent hybrids, the incoming joint state is the same. Conditioning on the classical command/history register gives positive quantum blocks whose traces sum to one. The diamond bound applies to each block, including arbitrary quantum memory and reference. All later common operations contract trace norm.

The halt-flag construction makes a bounded public stopping rule part of the same common tester. No assertion is made after conditioning on a rare stop history. The resulting estimate is the standard network hybrid in the declared classical-command interface.

### 3.7 Posterior conversion

Trace contraction gives `|p_h-q_h|<=||A_h-Ahat_h||_1`. Therefore

```text
p_h ||rho_h-rhohat_h||_1
 <= ||A_h-Ahat_h||_1 + |p_h-q_h|
 <= 2 ||A_h-Ahat_h||_1.
```

The inequality remains valid when the simulated mass is zero and its normalized state is assigned arbitrarily. Summation and Markov's inequality prove the claimed average and tail bounds. Pooling first and then applying the same inequality proves the event-conditioned result.

### 3.8 Integral Choi action

With the stated input-first convention,

```text
Phi(P)_(alpha,beta)
 = Sum_(i,j) J_(i alpha,j beta) P_(i,j).
```

The code and tests use this formula and compare it to full Kraus updates. The mass identity follows from the exact partial-trace constraint. A positive branch with zero trace is zero and is never sampled.

### 3.9 Exact mode

The selected branch numerator remains positive. Its trace is bounded by the total branch trace, so one step multiplies the trace by at most `D_*`. This gives the exact `Q=ell_0+NH` bit bound. The instrument denominators and all previous common scalar factors cancel from the conditional probabilities and normalized state.

### 3.10 Grid mode and history error

The initial positive repair has trace-norm error at most `6d^2/B`. At every subsequent call, positivity and joint trace preservation make the direct-sum instrument trace-norm contractive on Hermitian differences. Repairing the selected branch produces error proportional to its branch mass. Summing over histories therefore adds at most one `6d^2/B` term per use, not one term per branch.

Choosing `B=2^b` with the displayed precision gives `(N+1)6d^2/B<=2^{-L}`. Freezing stopped branches leaves total live mass at most one and preserves the same bound.

### 3.11 Polynomial validation

The reduced-rational Schur complement test is a valid exact PSD criterion. Fraction reduction prevents the specific exponential blow-up of the unreduced fixed-dimensional scaled recursion. Every intermediate entry is a ratio of minors of the original rational matrix; standard determinant bounds make its bit length polynomial in the explicit matrix dimension and entry lengths.

This supports a polynomial bit-time and polynomial-space validation claim. It does not establish an optimized exponent, a practical large-dimensional algorithm, or a streaming-space validator matching the post-validation bound. The manuscript correctly charges preprocessing separately.

### 3.12 Implementation audit

The implementation:

- rejects an unsupported tensor convention;
- validates Hermitian PSD Choi blocks and exact partial traces;
- preserves explicit zero Choi outcomes;
- recomputes compilation certificates exactly;
- uses signed truncation for rational coordinates;
- streams branch weights without retaining all branch matrices;
- samples from exact integer weights;
- distinguishes ideal fair bits in the theorem from OS randomness in the CLI;
- limits token storage by the longest declared command identifier; and
- emits a legal rational numerical state.

The new exact suite checks rectangular input/output dimensions, Choi-versus-Kraus contraction, entangled references, common adaptive tester interventions, stopped histories, rare-posterior counterexamples, positive-TP-but-not-CP transposition, malformed certificates, and variable-dimensional Schur validation. These are strong regressions. They are not universal proof, formal space verification, spectral certification, or independent novelty review.

---

## 4. Reproducibility and release evidence

The committed build receipt records:

- a 58-page quantitative manuscript;
- a 40-page structural manuscript;
- a 105-page complete research edition;
- 368 active complete-edition labels;
- preservation of 347 prior labels and 85 predecessor native files;
- isolated native reconstruction;
- ordinary/optimized agreement;
- 4,853 new exact assertions and 36 named negative controls;
- retained v65, v64, and v63 regression suites; and
- explicit separation of proof, regression, source identity, and priority.

Source qualification run `36546520706` completed successfully on native source `3050a459...`. Exact-head run `36547235610` checked out `58490231...` read-only, reconstructed exact sources and PDF pages, reran exact tests, rebuilt the minimal journal package, and uploaded an external attestation.

This is strong source and reproduction evidence. It is not a formal proof certificate. The exact final commit is unsigned; the package does not claim a cryptographic author signature.

---

## 5. Priority and significance

### 5.1 Classical ingredients

The following are classical or close to classical:

- Choi positivity and partial-trace criteria;
- trace/diamond norm comparison through a Choi matrix;
- mixing with an identity buffer to restore positivity while retaining trace constraints;
- rational matrix arithmetic and Schur complement PSD validation;
- rejection sampling from integer weights;
- trace-norm contraction of positive trace-preserving instruments;
- additive channel/network hybrid bounds;
- operational strategy norms;
- posterior normalization from subnormalized block bounds; and
- positivity-preserving quantum filtering and trajectory updates.

The manuscript generally credits these ingredients correctly. The contribution is their explicit integer combination with a denominator, deterministic coordinate-error budget, reference-stable diamond control, variable-description trajectory simulator, and the inherited stochastic-width theory.

### 5.2 Directly relevant omitted work

Naik, Zartab, Gisin, and Banik, arXiv:2501.15807v2, study classical simulation of a qubit channel when joint measurements may involve an unknown or externally entangled system. They prove that a perfect qubit channel cannot be simulated by finite classical messaging in that generic physical model, while noisy depolarizing channels admit finite-resource protocols.

Their model is not the present one:

- they study a physical classical communication protocol;
- Revision 66 computes and compares mathematical instrument descriptions and numerical trajectories;
- Revision 66 explicitly does not accept an unknown physical quantum state and prepare its output; and
- its arbitrary-reference guarantee comes from diamond closeness of two genuine quantum instruments, not from a classical realization of either instrument.

Precisely because the distinction is central, this source is a mandatory comparison. Its omission weakens the current priority and interface discussion.

A revised literature section should also distinguish deterministic finite descriptions/nets from statistical learning of unknown channels in diamond distance, including current dimension- and accuracy-dependent channel-learning lower bounds. These are different problems, but the distinction should be made rather than left implicit.

### 5.3 Why the top-four threshold is not reached

The principal new v66 theorem is an upper approximation theorem with safe polynomial dimension dependence. It does not produce:

- a matching lower bound for variable rational Choi descriptions;
- an optimal finite-description entropy for instruments;
- an optimal dependence on input dimension, output dimension, outcomes, or diamond error;
- a classification of which disturbing instruments admit bounded classical numerical memory;
- a physical classical realization of arbitrary unknown quantum input;
- a sharp theorem for general noisy transcript-only interfaces;
- a multiplicatively sharp exponential accuracy crossover; or
- a consequence resolving a recognized open problem outside this revision program.

The paper is mathematically serious, but the new level of generality and conceptual reach is not sufficient for one of the four leading general mathematics journals.

---

## 6. Relationship to the wider repository pipeline

The independent analytic dependency graph remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent.
```

Revision 66 does not prove the raw unsmoothed local limit, predictable stopped-path entropy/LDP recovery, global past kernel, canonical shell conditioning, process CLT/Mosco recovery, nonlinear Nisio cores, exact-experiment filtering/QMD/LAN, changing-filtration response, or labelled posterior-contraction gates.

The bounded stopping theorem here is a finite-dimensional hybrid comparison. It is not the A3 stopped-path large-deviation theorem. The posterior proposition is a normalization inequality for finite stopped blocks. It is not the C1/C2 filtering/LAN or response theorem. The rational Choi validator and trajectory program do not close any analytic aggregate.

Accordingly, all of the following remain false:

```text
historical A2 replacement
B4 aggregate
C2 aggregate
eleven-paper aggregate
whole Theta program closure.
```

The manuscript correctly records this separation. It must remain outside any significance claim for the present paper.

---

## 7. Required revisions before specialist submission

1. **Keep the focused manuscripts separate.** Submit the quantitative and structural papers independently. Treat the 105-page complete edition as archival research history, not as a journal article.

2. **Add the reference-sensitive classical-simulation boundary.** Compare explicitly with Naik--Zartab--Gisin--Banik, arXiv:2501.15807v2, and explain why diamond-close mathematical instruments are not finite-classical-message physical simulators.

3. **Obtain an independent priority review.** The present literature file is author-side and targeted. It cannot itself discharge r42's independent-priority request.

4. **Keep the operational interface on page one.** Distinguish at least: instrument-description compilation, numerical trajectory simulation of specified data, physical action on unknown quantum input, and transcript-only classical simulation.

5. **State the upper/lower asymmetry prominently.** The variable-description Choi theorem is a general upper construction. The inherited lower theorem remains conditional on a fixed program, an expanding unitary subsystem, a full action gap, cap bounds, and legal numerical matrix output.

6. **Do not advertise optimal dimension dependence.** The constant `6mn^2d^2(1+mn)` and the explicit description bound are safe. No optimal dependence or matching lower bound is known here.

7. **Separate preprocessing from streaming.** Preserve the distinction between polynomial validation workspace and the post-validation streaming bound in every theorem summary and abstract-level statement.

8. **Separate expected time from worst-case storage.** Rejection sampling gives almost-sure termination and expected runtime/fair bits, while storage is bounded on every trial. Do not compress these into an unqualified “efficient.”

9. **Retain the rare-posterior limitation.** State only true-law weighted, high-probability, and pooled-event bounds. Do not infer simultaneous accuracy of every normalized rare branch.

10. **Use unambiguous positivity language.** Replace “positive Gaussian-integer matrix” by “positive semidefinite matrix with Gaussian-integer entries.”

11. **Retain the imported spectral hypotheses.** The new upper constructions do not need a gap; the inherited lower conclusions do. Finite regression does not certify a full Koopman gap.

12. **Retain the v63 multiplicative gap.** Revision 66 does not close the `exp(O(sqrt(N log N)))` uncertainty in the width crossover.

13. **Keep the repeatable-probe scope explicit.** The structural theorem remains an oracle-like fresh nondisturbing classical observation model, not a general disturbing quantum measurement or POMDP theorem.

14. **Keep release evidence separate from mathematical evidence.** Exact-head reconstruction establishes source/PDF/test identity, not theorem correctness, priority, authorship, or journal acceptance.

15. **Keep the wider pipeline separate.** The local stopped comparison and posterior inequality do not advance the A/B/C/D aggregate flags.

---

## 8. Detailed comments

1. State the input-first unnormalized Choi convention at every standalone theorem that uses the integer contraction formula.

2. In the Choi/diamond lemma, say explicitly that the trace-norm unit ball is the convex hull of rank-one partial isometries; this makes the SVD reduction fully transparent.

3. The lower Choi bound is not used in the compiler theorem. Explain whether it is retained solely to calibrate convention and potential converse applications.

4. Clarify that the coordinate promise concerns independent Hermitian real coordinates, not every complex matrix coordinate counted twice.

5. The selected outcome/output coordinate in the residual repair is arbitrary. State that changing it affects neither legality nor the uniform bound.

6. Known zero outcomes can be preserved only by removing them before applying the generic repair and restoring them afterwards. This should appear in the theorem discussion, not only after the proof.

7. The finite instrument net is an existence/description result. It is not a statistically learned net and does not provide an efficient enumeration of all members.

8. The adaptive theorem compares the same tester in both experiments. It does not control an adversary whose future strategy depends on which hidden experiment was used.

9. Coherent command superpositions are excluded. This should remain visible in the theorem statement, not just the prose preceding it.

10. The stopping rule is public and bounded. Private stopping based on inaccessible internal simulator state is a different interface.

11. Transcript TV is half the classical block trace norm. Preserve the factor throughout examples and code documentation.

12. The pooled-event posterior bound uses true event probability `alpha`; simulated event probability may be zero. The arbitrary fallback state should be stated wherever the bound is quoted.

13. In exact mode, the retained numerator represents a subnormalized path block only up to omitted common scalar denominators. Explain this once in the algorithm box.

14. The variable-data theorem stores the entire description. A future read-only external-memory variant would be a different space model.

15. The longest command identifier is part of `S`; the token parser correctly caps temporary token storage by that declared maximum. Include this in the resource table.

16. The validator's bit-complexity proof uses ratios of minors. A concise lemma stating the exact minor representation and Hadamard length bound would improve self-containment.

17. The code's `rational_psd` routine does not explicitly permute pivots, but a zero diagonal in a PSD matrix forces its row and column to vanish. The manuscript's reference to permutation is unnecessary and can be simplified.

18. The code uses OS randomness only as a convenient execution source. Preserve the statement that this is not a proof of ideal independent fair bits.

19. The regression suite's entangled-reference tests are finite examples. They support tensor-index correctness; they do not prove the arbitrary-reference theorem.

20. The transposition negative control usefully distinguishes positivity/TP from complete positivity. Retain it.

21. The build receipt reports underfull boxes. These are not correctness defects but should be cleaned before submission.

22. The bibliography entry for Watrous should identify all cited theorem/equation locations, not only one corollary.

23. Add Naik--Zartab--Gisin--Banik to both the quantitative comparison and the main bibliography.

24. The exact final commit is unsigned. A signed release would strengthen provenance, although it would not affect the mathematical verdict.

---

## 9. Final assessment

Revision 66 successfully closes the main local mathematical objections left by r42:

- the instrument approximation is now completely positive and jointly trace preserving;
- it is stable under arbitrary external references in diamond norm;
- adaptive common testers and bounded public stopping are covered;
- posterior consequences are stated in the correct mass-weighted form;
- variable dimension and rational Choi descriptions are accepted by one program;
- no rational Kraus factorization is assumed;
- validation, description length, temporary arithmetic, expected sampling cost, and worst-case storage are separately charged; and
- the structural focused article no longer depends on duplicated computational sections.

I found no fatal correctness defect in these new chains. The paper is now a strong specialist-level contribution.

It still does not meet the Annals / Inventiones / JAMS / Acta threshold. The new theorem is principally a constructive finite-dimensional upper approximation result built from classical Choi, positivity, arithmetic, and hybrid ingredients. There is no matching general lower theory, no optimal dimension/precision law, no physical classical simulation of unknown quantum input, no general disturbing-process classification, no closure of the v63 multiplicative crossover, no independent priority clearance, and no connection closing the separate A/B/C/D analytic program.

**Recommendation: reject at the four leading general mathematics journals; encourage separate specialist submissions after independent priority review, current-literature correction, and editorial compression.**
