# Referee Report — General Theta Foundations I, Revision 65 (r42)

**Quantitative manuscript:** *Positive Streaming Simulation and Spectral Space Bounds*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v65-positive-instrument-streaming-2026-09-29`
- `revision/general-theta-foundations-i-v65-referee-ready-2026-09-29`

**Reviewed exact final head:** `34e5719ce5c7109c8c31f98079716b8ce6dcfffe`  
**Candidate publication:** `8c5ff3b261b9e385d87f41aca1a13e38a7bf257d`  
**Qualified native source:** `6134419d53a8cfe3d8966fa4bf8a99c33bd716e0`  
**Source predecessor:** Revision 64 final head `abd5600b0085463ff78a1525d9588f42c8a514d5`  
**Controlling external report:** Revision 64 r41, `bee28d9c8af25880c548b4650f2fdc7eacbdf8af`  
**Controlling proof/pipeline audit:** `7284bc1e406665a8f89edf2741abdd5e71e8555d`  
**Source qualification workflow:** `36538213682`, conclusion `success`  
**Exact-head read-only reconstruction:** `36538707993`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v65-external-referee-r42-2026-09-29`  
**Date:** 29 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 65 is a substantial and technically successful response to the principal scope objections in r41. Revision 64 established a sharp charged-space theorem for one qubit-valued numerical task, but its legality-preserving upper construction used the special geometry of the Bloch ball and did not itself simulate disturbing instruments. Revision 65 replaces that special mechanism by an explicit positive fixed-denominator rounding map on the full density-matrix set, constructs an adaptive finite-bit simulator for fixed rational quantum instruments with genuine disturbance, zero outcomes, and arbitrarily rare nonzero outcomes, and combines the positive construction with the inherited entropy converse to obtain sharp matrix-output space in every fixed dimension under stated spectral and cap hypotheses.

I did not find a fatal mathematical gap in the new positive rounding lemma, the direct-sum instrument trace-norm contraction, the subnormalized-history hybrid argument, the exact integer branch sampler, the exact unnormalized fallback, the fixed-program space accounting, the higher-dimensional matrix-output lower bound, or the strict-cutpoint comparison. The central constructive theorem uses the right error object: the sum of trace norms of subnormalized history blocks. Because the repair error is weighted by branch mass before summation, no inverse outcome probability appears. This is the correct way to avoid a false rare-posterior claim.

The four-leading-journal disposition nevertheless remains negative. The positive instrument theorem is a strong **upper** result for fixed finite Gaussian-rational Kraus data and fixed dimension; it is not a classification of disturbing processes, a diamond-norm simulation with arbitrary external entanglement, or a sharp lower theorem for general noisy instruments. The matching lower order applies only when the interface contains an expanding unitary subsystem and requires a legal numerical matrix output. The lower proof continues to depend on strong full-action spectral and all-direction cap assumptions, with non-effective dimension-dependent constants in the general `SU(d)` examples. The exponential accuracy crossover inherited from Revision 63 still has a subexponential multiplicative uncertainty. The structural classification still concerns fresh, repeatable, nondisturbing classical probes. Finally, the exact theorem-level priority boundary across finite-precision quantum trajectories, positive realization, classical simulation of quantum automata, numerical filtering, streaming complexity, and rational channel simulation has not been independently settled.

**Disposition outside the four leading general journals:** the quantitative manuscript is now a strong specialist contribution, particularly if positioned as a theorem on positive finite-precision simulation and spectral space lower bounds rather than as a universal memory theory. The structural manuscript also contains a coherent specialist theorem package, although the newly duplicated instrument-construction sections weaken its focus. I would encourage separate submissions after independent priority review, sharper interface statements, and substantial editorial compression. I would not request another wholesale mathematical reconstruction.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 65 manuscript branches are identical at

```text
34e5719ce5c7109c8c31f98079716b8ce6dcfffe.
```

No Revision 66 branch was present in the branch survey used for this report. The exact final head adds a read-only reconstruction request to the candidate publication. The candidate is descended from the qualified native source `6134419d...`; Revision 65 is four commits beyond the Revision 64 final head and is isolated under `papers/GTF-I-v65-positive-instrument-streaming/`.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/32-positive-density.tex`;
- `sections/33-adaptive-instruments.tex`;
- `sections/34-matrix-space.tex`;
- `sections/35-cutpoint-comparison.tex`;
- `instrument_streaming.py` and `check_instruments.py`;
- the qubit, qutrit, and ququart fixed instrument descriptions;
- the inherited Revision 64 complete-configuration and integer-streaming theorem;
- the inherited Revision 62 return-free occupation and causal strong-converse chains;
- the inherited Revision 63 exponential-accuracy crossover;
- the matrix-orbit, least-orbit cap, explicit rational alphabet, and full-action gap chains;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r41 report and proof/pipeline audit;
- the build receipt, package manifest, preservation manifest, theorem locations, page checks, and regression outputs;
- the source-qualification workflow and exact-final-head read-only workflow; and
- the frozen repository-wide A/B/C/D pipeline ledger and history.

The present report is a mathematical and editorial referee assessment. It is not a formal proof-assistant verification and not an exhaustive novelty search. Successful source reconstruction and exact finite regression are treated as reproducibility evidence, not as proof of the universal theorems or their priority.

---

## 2. Executive assessment of the new mathematics

### 2.1 Positive fixed-denominator matrix rounding

For a density matrix `rho`, the manuscript first forms a trace-preserving Hermitian grid approximation `Q_B(rho)`. It then defines

```text
R_B(rho) = (B Q_B(rho) + 2 d I)/(B + 2 d^2).
```

The output is positive semidefinite of trace one, has a fixed integer denominator independent of the previous history, and satisfies

```text
||R_B(rho)-rho||_1 <= 6 d^2/B.
```

The proof does not invoke an eigenvalue decomposition, a projection oracle, or a polytope table. It bounds the truncation error in Frobenius and operator norm, shifts the matrix by an explicit scalar multiple of the identity, and normalizes. The supplied rank-one rational example correctly demonstrates that trace-preserving coordinate truncation without the diagonal buffer can be indefinite.

This is an elementary construction, but it is exactly the missing legality mechanism needed to move from the qubit Bloch ball to arbitrary fixed dimension.

### 2.2 Adaptive simulation of rational instruments

The physical data consist of a fixed finite Gaussian-rational Kraus description

```text
Phi_(a,y)(X) = q^(-2) sum_r M_(a,y,r) X M_(a,y,r)^*,
```

with exact completeness and a fixed rational initial density matrix. An external classical controller may choose commands adaptively from the public control-output history. The simulator emits each outcome immediately and retains a legal numerical density matrix.

The error at time `t` is

```text
D_t = sum_h ||A_h - Ahat_h||_1,
```

where `A_h` and `Ahat_h` are true and simulated subnormalized state blocks for complete public histories. This is the trace norm of a block-diagonal classical-quantum state difference. It dominates twice the transcript total variation and contracts under any common terminal measurement.

The direct-sum instrument contraction and homogeneous positive repair give

```text
D_(t+1) <= D_t + 6 d^2/B.
```

Initial rounding contributes one more term, so choosing `B` proportional to `(N+1)2^L` gives error at most `2^(-L)` at every prefix. The argument works uniformly over common adaptive controllers and does not divide by a branch probability.

This is the strongest new result in the revision. It is a genuine process-level construction with disturbance, rather than a list of separately accurate terminal means.

### 2.3 Exact rational sampling and exact fallback

For a stored integer numerator `P`, every branch numerator

```text
S_y = sum_r M_(a,y,r) P M_(a,y,r)^*
```

is positive integral, and its trace is an exact nonnegative integer. The branch traces sum to `q^2 tr(P)`. Rejection from a binary interval of length `2^ell` therefore samples the exact rational outcome law using fresh fair bits. Acceptance probability is greater than one half unless the total is a power of two, and rejected words and trial counts need not be stored.

Approximate mode repairs the chosen normalized branch back to the same fixed denominator. Exact mode keeps the unnormalized branch numerator and never divides it; positivity bounds every entry by the trace, whose bit length grows linearly in the horizon. Selecting the smaller mode gives

```text
O_input(min{N, L + log(N+1)})
```

writable bits. The expected running time is polynomial in the precision, while space is bounded on every rejection trial.

The code implements the same recurrence with exact Gaussian integers. The use of operating-system randomness in the reference program is correctly separated from the ideal fair-bit theorem.

### 2.4 Sharp matrix-output space in fixed dimension

For the converse, a density matrix is centered at `I/d` and divided by

```text
r_d = sqrt((d-1)/d).
```

Every legal density decoder then lies in the Euclidean unit ball, while a pure target lies on the unit sphere. The inherited complete-configuration reduction and return-free entropy occupation theorem apply with mean Frobenius error. Under a full Koopman action gap and an all-direction cap exponent `p`, one obtains

```text
N <= C_0 + C_1 log k + C_2 epsilon k^(2/p).
```

The logarithmic-or-linear alternative yields a configuration-space lower bound of order

```text
min{N, L + log N}.
```

A fixed-program configuration-count argument translates this to writable space. The positive channel simulator gives the matching deterministic upper order with pointwise trace-norm error.

This synthesis is mathematically coherent. Its scope is important: the lower constant and starting horizon may depend on the fixed finite program and physical data; the theorem is not uniform over a nonuniform family of uncharged programs, varying dimension, or arbitrary input descriptions.

### 2.5 Explicit examples in every fixed dimension

The adjacent-coordinate rational unitaries and their inverses generate a dense subgroup of `SU(d)`. Algebraic spectral-gap results, followed by symmetrization, laziness, and Peter-Weyl transfer, supply the full-action gap. The least-orbit theorem gives cap exponent `2(d-1)` for conjugation on traceless Hermitian matrices.

Thus every fixed dimension has an explicit rational alphabet for which the matrix-output space order is sharp. The alphabet is explicit; the spectral constant is qualitative and not computed uniformly in `d`. The upper algorithm does not need this constant.

### 2.6 Strict cutpoints versus numerical calibration

The added comparison with Chen--Wu correctly distinguishes strict-cutpoint language equivalence from calibrated numerical simulation. The attenuation construction

```text
f_beta(w) = lambda + beta^|w| (f(w)-lambda)
```

preserves the strict-cutpoint language while allowing order-one numerical distortion at long lengths. Conversely, trace-norm approximation preserves a threshold decision only with a margin larger than the numerical error.

This comparison is useful and necessary. It does not turn either line of work into the other, and the manuscript correctly avoids claiming a lower bound for unrestricted cutpoint-language simulation.

---

## 3. Correctness audit: positive rounding

### 3.1 Entrywise truncation estimates

For the first `d-1` diagonal entries the error is below `1/B`; the final diagonal error is at most `(d-1)/B`. Every real and imaginary off-diagonal coordinate changes by less than `1/B`. Counting both Hermitian off-diagonal entries gives

```text
||Q_B(rho)-rho||_F^2 <= 3d(d-1)/B^2.
```

The manuscript weakens this to the convenient operator bound `2d/B`. This is valid for all `d>=2`.

### 3.2 Positivity and trace

Since `rho` is positive and the perturbation has operator norm at most `2d/B`, the matrix

```text
Q_B(rho) + (2d/B) I
```

is positive. Its trace is `1+2d^2/B`. Normalization therefore produces a density matrix with integer numerator trace `B+2d^2`.

No claim that `R_B` is affine or completely positive is used. It is a numerical map on a stored matrix.

### 3.3 Trace-norm error

Writing `E=Q_B(rho)-rho` and `eta=2d/B`,

```text
R_B(rho)-rho = [E + eta(I-d rho)]/(1+d eta).
```

The safe bounds `||E||_1<=2d^2/B` and `||I-d rho||_1<=2d` imply the displayed `6d^2/B` estimate. The constants are deliberately nonoptimal but adequate for the space theorem.

### 3.4 Integer implementation

If `rho=P/z` with positive Gaussian-integer `P`, positivity gives `|P_ij|<=z`. The independent rounded entries are signed integer quotients of numbers with the stated bit length. The last diagonal entry enforces exact trace. A fixed number of buffers suffices in fixed dimension.

I found no hidden floating-point, eigenvalue, or cone-membership premise in this construction.

---

## 4. Correctness audit: instrument contraction and adaptive histories

### 4.1 Direct-sum contraction

For Hermitian `X=X_+-X_-`, positivity of each branch and trace preservation after summing outcomes give

```text
sum_y ||Phi_y(X)||_1
 <= sum_y tr Phi_y(X_+ + X_-)
 = ||X||_1.
```

This is exactly the contraction needed for differences of subnormalized blocks, whose traces need not agree history by history.

### 4.2 Homogeneous repair

For a positive branch `X`, homogeneous repair multiplies the rounded normalized state by `tr X`. Its trace is preserved, and its error is at most `delta_B tr X`. A zero-trace positive branch is the zero matrix, so no normalization of a zero-probability outcome occurs.

This branch-mass factor is the key point: after summing all histories and outcomes, the repair budget is `delta_B`, not `delta_B/p_h` for a rare history.

### 4.3 Agreement with the executable sampler

The actual simulator samples outcome `y` using the branch trace computed from the approximate stored state and then stores the repaired normalized branch. Therefore the subnormalized approximate update in the proof is exactly the law generated by the executable procedure. The proof is not analyzing an auxiliary algorithm different from the code.

### 4.4 Adaptive controllers

For each public history `h`, the same controller law `pi(a|h)` is applied to the true and simulated experiments. A private randomized controller may be conditioned on its random seed and then averaged. Because the error estimate is uniform in the conditioned seed, convexity preserves it.

The theorem does not grant the simulator access to an unrecorded controller history or private controller memory. It emits each public outcome immediately.

### 4.5 Error recursion

For each old history, triangle inequality, direct-sum contraction, and branch repair give

```text
sum_(a,y) ||A_(hay)-Ahat_(hay)||_1
 <= ||A_h-Ahat_h||_1 + delta_B tr(Ahat_h).
```

The approximate history blocks have total trace one, so summing gives

```text
D_(t+1) <= D_t + delta_B.
```

With the initial repair, `D_t<=(t+1)delta_B`. The selected `B` yields the promised prefix-uniform bound.

### 4.6 Operational meaning and limits

Taking traces gives the transcript total-variation bound. Appending the same terminal measurement to both experiments gives the corresponding measurement-output bound. The theorem does not simulate an arbitrary external entangled reference and does not establish diamond-norm closeness of channels or instruments. It does not guarantee normalized conditional-state error on every rare observed history.

These exclusions are mathematically substantive and should remain prominent in all summaries.

---

## 5. Correctness audit: finite-bit implementation

### 5.1 Exact outcome weights

Kraus completeness implies that branch traces sum exactly to `q^2` times the stored denominator. Zero branch weights are never selected. If exactly one outcome has positive weight, no fair bit is consumed.

### 5.2 Rejection sampling

Drawing `ell=ceil(log_2 T)` bits and rejecting values at least `T` produces the uniform law on `[0,T)`. Acceptance probability is greater than one half except at powers of two, where it is one. The number of failed trials is not retained, so worst-case storage remains bounded although running time is random.

### 5.3 Approximate mode

The denominator `B+2d^2` is restored after every update. Consequently denominators do not multiply along a sampled path. Fixed Kraus coefficients, branch numerators, traces, interval endpoints, division scratch, and output numerators all use `O_input(L+log N)` bits.

### 5.4 Exact mode

The unnormalized numerator is propagated without division. Its positive integral trace is at most `z_0 q^(2t)`. Positivity bounds every matrix entry by the trace, so all data and temporary products use `O_input(t+1)` bits. Exact branch probabilities and normalized numerical states are reproduced.

### 5.5 Mode selection and parameters

The program scans `L` with saturation at `N` and chooses exact mode before allocating a huge grid. It stores `N`, a command counter, fixed-radix output integers, and a constant number of matrix buffers. The claimed order is therefore consistent in the stated fixed-input bit model.

The reference Python implementation does not certify CPython allocator usage or physical entropy quality. The manuscript states this correctly.

---

## 6. Correctness audit: higher-dimensional lower bound

### 6.1 Centering and legal decoder norm

For every density matrix `D`,

```text
||D-I/d||_F^2 = tr(D^2)-1/d <= (d-1)/d.
```

Pure states attain equality. After scaling by `r_d`, every legal decoder has norm at most one and the target orbit is unit. This supplies precisely the geometric hypothesis used in the centroid argument.

### 6.2 Error conversion

Mean Frobenius error `epsilon` becomes normalized Euclidean error `epsilon/r_d`. With `L>=2` and fixed `d>=2`, the residual amplitude remains uniformly positive. The constants in the finite occupation budget may therefore be fixed independently of `N,L`.

### 6.3 Complete configurations

Almost-sure termination gives boundary stochastic rows, and the conditional mean of samplewise legal matrix outputs remains in the compact convex density-matrix set. Boundary rows may depend on the public time index, which only enlarges the lower-bound comparison class.

### 6.4 Fixed-program quantifier

The theorem first obtains a lower bound on the number of complete configurations. To obtain a conventional work-space lower bound, it fixes the program and machine convention so that `s` work bits have at most a polynomial factor times `2^(O(s))` configurations.

This is correct, but editorially delicate. The theorem is not uniform over arbitrary program descriptions whose finite control changes with `N,L`. The phrase “optimal writable bit-space” must always be accompanied by the fixed-program convention and program-dependent constants or starting horizon.

### 6.5 Explicit `SU(d)` examples

The dense-generation argument for the adjacent rational unitary alphabet is inherited and coherent. The full-action gap is imported from a deep algebraic spectral-gap theorem; the least-orbit cap exponent is inherited from the manuscript's geometric theorem. No numerical or dimension-uniform gap is obtained by finite tests.

The upper algorithm is effective without knowledge of the gap. The lower theorem is qualitative in its general constants.

### 6.6 Instrument sharpness

If the instrument family contains the expanding unitary subsystem, restricting the controller to deterministic unitary words reduces the process error interface to the numerical matrix-output task. The matrix lower bound therefore applies.

This is not a lower bound for transcript-only simulation of arbitrary noisy channels. The manuscript states this boundary correctly.

---

## 7. Reproducibility and evidence

The source-bound qualification run `36538213682` completed successfully on the native source. The exact-final-head workflow `36538707993` checked out `34e5719...` read-only, rebuilt the exact sources and all PDF pages, reran the exact arithmetic suites, reconstructed the minimal journal package, and uploaded an external attestation.

The committed build receipt records:

- a 51-page quantitative paper;
- a 44-page structural paper;
- a 99-page complete edition;
- 347 active complete-edition labels, with 321 predecessor labels preserved;
- isolated rebuild success;
- ordinary/optimized agreement;
- 35,028 new instrument assertions;
- 1,260 positive-rounding cases;
- 768 adaptive-tree branches;
- 2,250 sampled prefixes;
- 23 new negative controls;
- retained Revision 64 and Revision 63 regression suites; and
- no floating-point decision oracle in the new exact checks.

The regression program tests positivity, trace, rigorous rational norm enclosures, exact sampling intervals, rare and zero outcomes, adaptive history trees, exact and grid modes, parser failures, bit-size envelopes, and the actual command-line interface. It explicitly disclaims universal proof, formal space verification, ideality of operating-system randomness, and priority clearance.

These are strong reproducibility practices. The exact final commit remains unsigned; the package does not claim cryptographic authorship.

---

## 8. Relation to the paper pipeline

The local quantitative chain is now

```text
common nonnegative rows
 -> conditional-centroid mass loss
 -> entropy transport and sharp occupation
 -> return-free drift covariance
 -> exponential-accuracy crossover
 -> complete configurations and charged qubit space
 -> positive matrix rounding
 -> adaptive rational-instrument simulation
 -> higher-dimensional sharp matrix-output space.
```

The causal classification chain remains separate:

```text
future-response types
 + repeatable fresh nondisturbing probes
 -> common diagnostic itinerary
 -> observation-tail capacity
 -> all-error-below-one strong converse.
```

Revision 65 gives an upper simulation theorem for disturbing instruments, but it does not extend the finite-response quotient classification to that class.

The repository's independent analytic program remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent.
```

Raw local limits, stopped-path LDP recovery, global past kernels, shell conditioning, process CLT/Mosco recovery, nonlinear Nisio cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction remain separate obligations. Revision 65 closes none of those aggregate gates. Every aggregate completion flag remains false.

The paper should therefore be judged on its local realization, simulation, and space theorems alone. The size of the historical repository is neither a novelty argument nor evidence of whole-program closure.

---

## 9. Why the four-leading-journal threshold is still not met

### 9.1 Fixed-input and fixed-dimension scope

The constructive instrument theorem fixes the dimension, command and outcome sets, Kraus matrices, denominator, and initial state before `N,L` vary. The hidden `O_input` constants may depend on all of these data. This is a legitimate theorem, but it is not a uniform complexity result for variable quantum systems.

### 9.2 The general instrument theorem is upper-only

The positive simulator works for arbitrary fixed rational instruments in the stated class. The sharp lower order does not. It requires an expanding unitary subsystem, a pure seed, a legal matrix interface, a full-action spectral gap, and an all-direction cap estimate. Thus Revision 65 does not determine the optimal space of general noisy or measurement-driven simulation.

### 9.3 Operational metric is restricted

The classical-quantum block trace norm is appropriate for the claimed classical transcript plus numerical matrix interface. It does not include arbitrary external quantum reference systems and is weaker than diamond-norm simulation of instruments. The returned matrices are numerical descriptions, not physical state preparation.

### 9.4 Deep and non-effective lower inputs

The most general sharp lower examples import algebraic spectral-gap theorems. Constants are not numerical or uniform in dimension. The geometric cap constants are also dimension dependent.

### 9.5 Quantitative crossover remains non-sharp multiplicatively

Revision 63 determines the exponential rate, but the lower and upper bounds differ by an `exp[O(sqrt(N log N))]` factor. Neither the exact saturation window nor optimal leading constants are known.

### 9.6 Structural classification remains oracle-like

The finite-response theorem assumes fresh nondisturbing probes that may be repeated without changing the physical state. Revision 65's disturbing-instrument simulator does not supply a corresponding finite-state classification or strong converse.

### 9.7 Priority remains unresolved

The new comparison with Chen--Wu is useful and correct in spirit: strict-cutpoint sign preservation and calibrated numerical approximation are different tasks. However, the author-side audit remains targeted. The paper still needs independent comparison with finite-precision quantum trajectory simulation, numerical filtering, rational channel approximation, hidden quantum Markov models, positive realization, and streaming simulation literature.

### 9.8 Article architecture remains accretive

The 51-page quantitative article retains several generations of structural and quantitative results in addition to the new instrument and matrix-space theorems. The 44-page structural article now repeats the positive rounding and instrument simulator, although those results are computational constructions rather than part of the finite-response classification proof. The submission objects are more focused than the complete edition, but they remain broader than necessary.

### 9.9 No comparably broad external consequence

The revision resolves important objections internal to this program and produces a strong specialist theorem. I do not see a consequence settling a recognized external problem of sufficient breadth to overcome the specialized interfaces, strong spectral hypotheses, and unresolved priority boundary at the four-leading-journal level.

---

## 10. Required revisions before specialist submission

1. **Separate the mathematical products more sharply.** The positive instrument simulator and matrix-space theorem belong naturally with the quantitative/computational paper. The structural finite-action and repeatable-probe classification should not duplicate the full constructive sections unless they are logically necessary there.

2. **State the operational interface in every headline.** Distinguish classical transcript plus numerical matrix blocks from physical state preparation, diamond-norm channel simulation, transcript-only simulation, and normalized rare-posterior accuracy.

3. **Keep the fixed-input convention visible.** Dimension, alphabet, Kraus data, denominator, seed, and—where used—spectral/cap constants are fixed before `N,L` vary.

4. **State the fixed-program lower quantifier precisely.** Program-dependent constants and starting horizons should not be hidden behind an unqualified phrase such as “the optimal classical space.”

5. **Separate upper generality from lower sharpness.** The upper theorem covers fixed rational instruments. The matching lower bound requires a unitary expanding subsystem and a legal numerical matrix interface.

6. **Clarify expected versus worst-case resources.** Space is worst-case over rejection trials; time and fair-bit consumption are expected. No time lower bound is proved.

7. **Preserve the rare-outcome distinction.** The theorem controls mass-weighted subnormalized blocks, not normalized conditional states on every low-probability history.

8. **Add a theorem-level comparison with quantum trajectory and filtering algorithms.** The present priority audit is strongest on automata and positive realization, but the new constructive result also belongs near numerical simulation of quantum instruments.

9. **Retain exact versioning for current literature.** Pin the Chen--Wu versions and theorem numbers used, because the title and exact statement of the April preprint changed between versions.

10. **Do not market the full-action gap as algorithmically certified.** It is an imported premise of the lower theorem, not an output of finite regression or the implementation.

11. **Keep the Revision 63 crossover gap explicit.** The new bit-space theorem does not remove the subexponential multiplicative uncertainty in label width.

12. **Obtain an independent priority review.** The author-side literature audit is candid and useful, but it cannot by itself establish novelty across several mature neighboring fields.

13. **Use the exact-head attestation as provenance only.** Do not merge source identity, finite regression, mathematical proof, novelty, and editorial acceptance into one “verified” claim.

14. **Keep the wider Theta pipeline outside the contribution claim.** No A/B/C/D aggregate gate is changed by this paper.

---

## 11. Detailed comments

1. In the positive rounding lemma, state explicitly that the final diagonal coordinate of `Q_B` need not itself lie in `[0,1]`; positivity is supplied only after the scalar buffer is added.

2. The bound `||I-d rho||_1<=2d` is intentionally loose. A short sentence noting that constants are not optimized would prevent readers from searching for a hidden sharpness claim.

3. The contraction proof needs positivity and total trace preservation after summing outcomes; complete positivity is used for the physical interpretation. The text already says this and should retain it.

4. An explicit zero outcome is represented in the input format by a nonempty Kraus list containing a zero matrix. This convention should be documented next to the JSON schema.

5. The error `D_t` uses the unhalved trace norm. Consequently transcript total variation is bounded by `D_t/2`, not `D_t`. This normalization should be kept consistent in abstracts and examples.

6. The theorem compares the same adaptive controller in the true and simulated experiments. It does not compare arbitrary controllers chosen separately after seeing the simulator's private state.

7. The simulator samples from the approximate branch weights, not the true weights. The subnormalized recursion correctly accounts for this; a sentence emphasizing that point would help readers.

8. Initial rounding contributes one full repair term, which is why the bound is `(t+1)delta_B`. This should remain visible.

9. Rejection sampling has unbounded worst-case running time but bounded worst-case storage. “Almost sure termination” and “expected time” should not be shortened to “efficient sampling” without qualification.

10. Exact mode stores unnormalized positive matrices. The normalized state is `P/tr P`; the omitted global powers of `q^2` cancel from branch probabilities and states. This can be stated once explicitly.

11. The approximate denominator `B+2d^2` is fixed across time. This is one of the construction's main advantages and deserves emphasis.

12. The exact/grid switch is an order-level choice, not a claim of pointwise optimality for every small `N,L`.

13. The reference implementation uses operating-system randomness. It is correctly presented as a recurrence implementation, not a physical fair-bit certification.

14. The matrix lower bound is for mean Frobenius correctness and samplewise legal outputs. The upper bound is stronger, giving deterministic pointwise trace-norm error.

15. The residual amplitude estimate in the matrix theorem depends on `L>=2` and fixed `d`; record that dependence when quoting the finite budget.

16. The work-space lower theorem is asymptotic for each fixed program. It is not a minimization over a different arbitrary finite-control program for every input pair.

17. The all-dimensional alphabet is explicit, but its lower constant is non-effective. “Explicit sharp family” should not be read as “numerically certified spectral constant.”

18. The instrument sharpness corollary requires the numerical matrix interface. It does not give a lower bound when only the emitted classical transcript is requested.

19. The strict-cutpoint attenuation proposition is elementary and useful. It should be presented as a semantic separator, not as a new general automata simulation technique.

20. Trace-norm approximation preserves an effect threshold only with margin. Strict-cutpoint equality without margin is a different invariant.

21. The structural article's abstract now mentions the instrument simulator, but the classification theorem still concerns nondisturbing probes. Readers should not be led to infer a classification of disturbing instruments.

22. The complete 99-page edition is archival and should not be sent as the main journal manuscript unless specifically requested.

23. The exact-head commit is unsigned. A signed tag would improve release provenance, but lack of one is not a mathematical defect and no signature should be fabricated.

24. Finite tests cannot certify the full Koopman gap, universal entropy inequalities, asymptotic lower theorem, or novelty. The current scope statements are correct.

---

## 12. Final assessment

Revision 65 answers the most important mathematical scope criticism of Revision 64. It provides a legal positive matrix update in all fixed dimensions, treats genuine instrument disturbance, handles zero and arbitrarily rare outcomes without a probability floor, controls the whole adaptive classical-quantum history in a natural mass-weighted norm, and gives an explicit finite-bit implementation. It also supplies a coherent conditional matching lower theorem for higher-dimensional numerical matrix output.

I found no fatal gap in these new chains. The source and exact-head reconstruction evidence is strong. The work has reached a technically mature specialist level.

It has **not** reached the Annals / Inventiones / JAMS / Acta threshold. The strongest general instrument result is upper-only and fixed-input; sharp lower bounds require a special expanding unitary subsystem and strong imported hypotheses; the operational metric excludes arbitrary entangled references and rare normalized posteriors; the structural classification remains restricted to nondisturbing probes; the width crossover remains multiplicatively nonsharp; and independent priority clearance is still open.

**Recommendation: reject at the four leading general mathematics journals; encourage separate, compressed submissions to strong specialist venues after independent priority review and sharper interface positioning.**
