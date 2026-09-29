# Referee Report — General Theta Foundations I, Revision 64 (r41)

**Quantitative manuscript:** *Spectral Entropy, Stochastic Widths, and Uniform Streaming Space*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v64-uniform-streaming-2026-09-28`
- `revision/general-theta-foundations-i-v64-referee-ready-2026-09-28`

**Reviewed exact final head:** `abd5600b0085463ff78a1525d9588f42c8a514d5`  
**Candidate publication:** `a42cccbf879f7ec7f71294eccfeba8176ef939ca`  
**Qualified native source:** `4dd6a9a2fa75531490d966c72e05522bc90b29a2`  
**Source predecessor:** Revision 63 publication `f5c1e5d6eacecc1597fba18697a715f8e7844e09`  
**Controlling external report:** Revision 61 r40, `4a99da0aab823418d95631d5dbbd8e9b8178994d`  
**Controlling pipeline audit:** `02c642d3c08774d2dbaee939ffb2eee57b545f92`  
**Source qualification workflow:** `36406379977`, conclusion `success`  
**Exact-head read-only reconstruction:** `36406831322`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v64-external-referee-r41-2026-09-29`  
**Date:** 29 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This remains **not a correctness rejection**. Revision 64 is a substantial advance over the Revision 61 manuscript reviewed in r40. It answers one of the most serious conceptual objections to the earlier work: the principal label-width invariant allowed arbitrary horizon-dependent real stochastic tables and did not by itself give a finite-bit algorithm. The new Section 31 now formulates a separate uniform one-pass computation problem, charges the complete private configuration and all integer workspace, proves a matching lower bound even for randomized algorithms with unlimited internal running time, and supplies one explicit deterministic integer algorithm. For the fixed six rational Lubotzky--Phillips--Sarnak Bloch rotations, the optimal writable bit-space is

```text
Theta(min{N, L + log(N+1)})
```

at Frobenius accuracy `2^(-L)`. The returned output is always a legal density matrix. The proof does not reinterpret arbitrary real advice as computation: it independently constructs the upper algorithm.

Revision 64 also inherits two mathematically significant developments not covered by r40. Revision 62 removes the identity/return requirement from the quantitative occupation theorem by transporting the entropy potential through arbitrary deterministic physical drift; gives an explicit six-command no-idle experiment; and strengthens the causal theorem to a strong converse at every whole-transcript total-variation error below one. Revision 63 analyzes accuracy that may decay exponentially with the horizon. Under a full spherical Ramanujan bound, it proves the uniform crossover law

```text
exp[-O(sqrt(N log N))]
    min{(2r-1)^N, ((N+1)/epsilon)^(p/2)}
 <= W_(N,epsilon)
 <= C min{(2r-1)^N, ((N+1)/epsilon)^(p/2)},
```

and for the explicit six rational rotations obtains the exponential rate

```text
lim (1/N) log W_(N,epsilon_N)
    = min{lim (1/N) log(1/epsilon_N), log 5}
```

whenever the first limit exists. I independently audited the v62 and v63 chains needed for the present decision. I did not find a fatal mathematical gap in the complete-configuration reduction, the finite bit--accuracy obstruction, directed legality-preserving rounding, the return-free entropy occupation argument, the no-idle exact profile, the nonbacktracking block-entropy estimate, the causal tail-capacity lemma, or the resulting strong converses.

The four-leading-journal disposition nevertheless remains negative. The new uniform space theorem is sharp and attractive, but it concerns one fixed low-dimensional numerical task, with a general extension only under strong full-action spectral and all-direction cap assumptions and with unit-ball legal outputs. The exponential crossover theorem determines the exponential rate but retains a subexponential multiplicative gap. The quantitative lower bounds still import deep arithmetic spectral information. The structural process theorem relies on repeatable fresh nondisturbing probes, an oracle-like classical observation model rather than a general partially observed, irreversible, or quantum measurement process. The independent theorem-level priority boundary is still unsettled. In particular, the Revision 64 literature audit does not compare the April and May 2026 Chen--Wu papers on exact probabilistic simulation cost for one-way quantum finite automata, which prove `Theta(n^2)` and `Theta(c q^2)` state-simulation laws under strict-cutpoint semantics. Those models are not equivalent to the present full-vector numerical-output and precision-space problem, but they are directly relevant current work and must be discussed before any priority claim about classical simulation cost for finite quantum automata.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is now a strong and technically mature specialist contribution. The structural manuscript is also a coherent specialist-level contribution, although its oracle-like probing assumptions should remain explicit. I would encourage separate submissions after an independent priority review, a current-literature update, and substantial editorial compression. I would not request another wholesale mathematical reconstruction.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 64 manuscript branches are identical at the exact final head

```text
abd5600b0085463ff78a1525d9588f42c8a514d5.
```

No later `General Theta Foundations I` revision was present in the branch survey used for this report. The final head requests a read-only reconstruction of the already published candidate. The candidate publication is descended from the qualified native source `4dd6a9a...`; the stated source predecessor is the Revision 63 publication `f5c1e5d...`, not the Revision 61 manuscript reviewed in r40.

No v62- or v63-specific external GTF referee report was located. Their theorems are therefore inherited source mathematics, not externally certified results. I reviewed the portions needed to assess Revision 64 rather than treating successful preservation or regression as a substitute for mathematical review.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/31-uniform-streaming.tex`;
- `streaming.py` and `check_streaming.py`;
- `sections/27-drift-occupation.tex`;
- `sections/29-no-idle-sphere.tex`;
- `sections/30-exponential-accuracy.tex`;
- `sections/28-tail-capacity.tex`;
- `sections/23-causal-process.tex`;
- the retained v61 entropy kernel, entropy dissipation, centroid transport, orbit-cap, exact-profile, and rational-compiler chains;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r40 referee report and pipeline audit;
- the build receipt, source hashes, theorem locations, page checks, regression outputs, journal package, and preservation manifest;
- the source-qualification workflow and exact-head read-only workflow; and
- the frozen repository-wide A/B/C/D pipeline ledger and history.

I also made a targeted current-literature check. The classical LPS/Pinochet Lobos--Pittet spectral input is correctly imported. Ambainis--Watrous and Panduranga Rao--Vinay are relevant but do not exhaust the present quantum-automata simulation literature. Chen--Wu, arXiv:2604.07058 and arXiv:2605.10682, are close 2026 antecedents in exact probabilistic simulation cost and should be added to the comparison. This check is targeted, not an exhaustive novelty search.

---

## 2. Executive assessment of the new and inherited mathematics

### 2.1 Charged one-pass numerical space

The new computational model has a fixed finite program. It reads `N`, `L`, and then exactly `N` commands in one pass. Consumed commands are inaccessible. All retained data, temporary integer storage, private randomness, addresses, and control information are included in the complete private configuration. A randomized algorithm must return a legal density matrix on every run; correctness is required only for the mean output, which makes the lower bound stronger.

The lower theorem first forgets bit encodings and counts complete private configurations. A machine with at most `k` configurations at each command boundary induces a clocked stochastic realization of width at most `k`: integrate all internal computation and fresh randomness between two boundaries into one stochastic row, and replace the terminal randomized output by its conditional mean. Convexity of the density-matrix set preserves legality.

The inherited no-idle occupation estimate then gives, for `k=2^B`,

```text
N <= 1 + 6 log(12 k)
       + 648 pi^2 k * [sqrt(2) epsilon/(1-sqrt(2) epsilon)].
```

At `epsilon=2^(-L)`, this forces either exponentially many configurations in `N` or at least order `N/epsilon` configurations. Taking logarithms gives the matching lower order

```text
min{N, L + log N}.
```

The argument allows horizon-dependent stochastic boundary rows, arbitrary randomization, and unlimited time between commands. It therefore does not rest on a conventional time-space tradeoff or on a deterministic-state assumption.

### 2.2 Legality-preserving integer upper algorithm

For the six rational Bloch rotations, write each matrix as `M_a/5` with fixed integer `M_a`. In the approximate mode, maintain a grid vector `n/2^b`, multiply by `M_a`, and divide every signed coordinate by five using truncation toward zero. Coordinatewise absolute values decrease, so the Euclidean unit ball is preserved at every prefix. The one-step vector error is at most `sqrt(3) 2^(-b)`, and orthogonality makes the errors telescope linearly. With

```text
b = L + ceil(log_2 N) + 2,
```

the terminal Frobenius error is below `2^(-L)`.

When this precision is at least the horizon, the algorithm switches to exact integer numerators and denominator `5^t`. Numerators and denominator have `O(t)` bits because orthogonality gives `||n||=5^t`. The smaller of the approximate and exact modes gives the upper order. Parameter `L` is scanned with saturation at `N`, so an excessively long precision request is not stored. A counter charging exactly `N` commands uses `O(log N)` bits. The output is a signed-binary rational density matrix with one common denominator.

This construction is elementary but correctly addresses the implementation objection. Nearest-grid rounding or floor rounding would not preserve the Bloch ball; the signed truncation direction matters.

### 2.3 General rational orthogonal actions

The paper extends the bit-space law to a fixed rational alphabet in `O(Q^m)` under the full action gap and an all-direction cap estimate, with legal outputs in the closed Euclidean unit ball. The lower argument uses only decoder norm at most one. The upper argument uses directed coordinate truncation or exact common-denominator arithmetic.

This is a useful generalization, but it should not be described as a general finite-precision theorem for arbitrary legal orbit hulls or higher-dimensional density-matrix cones. Coordinatewise truncation preserves a Euclidean ball; it need not preserve an arbitrary invariant convex body or positive-semidefinite cone. The manuscript states this limitation correctly.

### 2.4 Return-free occupation and no-idle realization

The v62 theorem replaces the identity filler by arbitrary deterministic physical drift. Covariance of the smoothing kernel and entropy under rotations lets one compare the old directional law, after one random spectral letter and a fixed filler word, with the new directional law. The transport cost is paid by the loss of total conditional-centroid mass. No hidden return row is assumed to be an identity, and intermediate registers remain unrestricted.

For the six nonidentity LPS rotations, the theorem gives an explicit occupation bound and width law without adding an idle command. The exact orbit at cut `t` is a right-coset ball of cardinality `5^t`: the seed stabilizer is the cyclic subgroup generated by the first free generator, and each coset has a unique shortest reduced representative with no terminal first-generator letter. Padding by powers of that generator fixes the seed and reaches every shorter coset at exactly the required length.

The robust exact profile follows from the denominator-five lattice. It persists through `epsilon <= 25^(-N)/16`. At fixed positive error the width is linear, and at positive subexponential accuracy it is `Theta(N/epsilon_N)`.

### 2.5 Exponential accuracy crossover

The v63 proof strengthens the fixed-error entropy defect. For a Markov average `T`, the identity

```text
H(f)-H(Tf) = sum_j a_j D(f_j || Tf)
```

combined with monotonicity from Kullback--Leibler to Rényi order one half gives a logarithmic defect controlled by the squared `L^2` norm of `T sqrt(f)`. Applying this to nonbacktracking word averages of length `b`, and using the radial free-group polynomial estimate, gives an entropy loss of order

```text
b log(2r-1) - O(log b).
```

The directional transport cost retains the small terminal error factor. Choosing `b` on the scale `sqrt(N log N)` balances the radial entropy gain, initial entropy range, and transport term. The resulting lower bound loses only `exp[-O(sqrt(N log N))]` relative to the minimum of the exact-word scale and the polynomial accuracy scale.

The argument is coherent and the exponential rate corollary follows. It does **not** provide a uniform multiplicative equivalent throughout the crossover or determine the exact saturation window. Those remain genuine quantitative limitations.

### 2.6 Strong converse for repeatable observations

The structural companion studies fresh, nondisturbing classical probes. A future-response type records every continuation and probe law. Finite response type is equivalent to an open-normal physical quotient and to an exact stationary causal realization.

The v62 tail-capacity lemma says that if a finite nonhomogeneous hidden process has width at most `k` infinitely often, its observation tail can contain at most `k` disjoint positive-probability events. The product-law strong converse constructs distinct tail events by empirical frequencies. A common diagnostic cycle returns each finite response type to itself and generates distinct i.i.d. block laws. Composite instruments between selected narrow cuts then yield the occupation obstruction and eventual exact quotient cardinality at every transcript error below one.

I find this chain mathematically coherent. Its interpretation must remain narrow: probes are fresh, repeatable, and leave the physical state unchanged. The model is not repeated measurement of one unknown quantum system, not a general hidden Markov identification theorem, and not a classification of irreversible partially observed dynamics.

---

## 3. Detailed correctness audit of the v64 space theorem

### 3.1 Complete configurations really produce stochastic rows

The boundary reduction includes all private retained information. Given a current configuration and next public command, almost-sure termination makes the distribution of the next boundary configuration a row of total mass one. Consumed input and old random bits cannot influence the future unless recorded in the configuration. The boundary index and fixed public parameters may be used by the induced clocked row; this only makes the comparison model more permissive.

At the terminal boundary, the conditional mean of legal random density matrices is again a legal density matrix. Thus the induced decoder realizes exactly the original mean output. The reduction does not make a conditional-correctness assertion after a rare history and does not assume exact sampling.

### 3.2 The finite obstruction is used at the right resource level

The no-idle occupation theorem counts every positive cut. If all positive boundary widths are at most `k`, its explicit formula gives the finite inequality used in the proposition. At zero error, the exact terminal width `5^N` supplies the sharper `B >= N log_2 5` bound.

For positive dyadic error, the inequality

```text
N <= C_0 + C_1 log k + C_2 epsilon k
```

has the required dichotomy. Either `log k` is linear in `N`, or `k` is at least a constant multiple of `N/epsilon`. The two-word witness excludes the one-configuration endpoint in the bounded exceptional range. No hidden assumption that an individual sampled output is accurate is introduced.

### 3.3 Fixed-program space and configuration count

The theorem first states a configuration-count lower bound. It then derives the conventional fixed-program work-space lower bound using at most

```text
C(s+1)^d 2^(c s)
```

complete configurations for `s` writable bits and a fixed number of heads. This distinction is important. A nonuniform program family with arbitrarily much hardwired finite control is not the same resource. The paper should continue to make “fixed finite program” visible wherever the bit-space corollary is advertised.

### 3.4 Directed rounding and legality

For every coordinate, truncation toward zero decreases its absolute value and changes it by less than one grid unit. Hence it preserves the Euclidean unit ball. Orthogonal evolution preserves prior error exactly, so the new error is at most the previous error plus the current grid residual. The Frobenius/Bloch normalization contributes the stated factor `1/sqrt(2)`.

The reference implementation uses signed integer truncation rather than Python floor on negative integers. Its exact and approximate recurrences agree with the theorem. The tests include explicit witnesses showing that floor and nearest rounding may leave the unit ball.

### 3.5 Scratch, parameter, and output accounting

Each fixed integer matrix row has bounded coefficient sum. Temporary products and sums therefore require only `b+O(1)` bits in grid mode. Division by five and multiplication by fixed integers can be performed by digit scans with linear bit operations and storage. Exact-mode integers have `O(t)` bits. The input precision is scanned with saturation, and the command counter is included.

The theorem returns a numerical rational matrix, not a physically prepared qubit. A write-only result is not reused as free private memory. The encoded output itself has the same order of bit length as the maintained state. These conventions are consistent.

### 3.6 Limits of the general extension

The rational-orthogonal corollary should repeat in one place that the alphabet, dimension, rational denominators, gap, cap constants, and seed are fixed independently of `N` and `L`. The present surrounding text makes this clear, but a self-contained theorem statement would reduce the risk of treating varying dimension or varying input matrices as free advice.

---

## 4. Reproducibility and qualification

The source qualification workflow `36406379977` ran successfully on the native source `4dd6a9a...`. The committed receipt records:

- 44 pages for the quantitative article;
- 40 pages for the structural article;
- 92 pages for the complete research edition;
- 71 current source files;
- 478 predecessor native files;
- 303 preserved predecessor labels and 321 complete active labels;
- an isolated rebuild;
- normal and optimized Python agreement;
- 272,113 exact assertions in the new streaming regression;
- 9,486 tested command words;
- 14 named negative controls; and
- exact source, document, and package hashes.

The final head has its own read-only reconstruction run `36406831322`. The job checked out exactly `abd5600...`, rebuilt and compared the source, preserved history, tests, and every PDF page, rebuilt the minimal journal package independently, and uploaded an external read-only attestation. This is a material improvement over a self-publishing workflow whose final commit lacks a post-publication check.

The regression program is appropriately scoped. It verifies exact finite arithmetic, parser behavior, legality, prefix error, scratch-size estimates, mode selection, and the explicit CLI route. It does not claim to prove the universal entropy theorem, the full LPS spectrum, or novelty. The exact-head workflow is reproduction evidence, not a proof assistant or an external priority opinion.

The final reviewed commit is unsigned. A signed release or tag would improve archival provenance, but this is not a mathematical objection.

---

## 5. Novelty and priority

### 5.1 What appears genuinely new in the present package

Subject to independent priority review, the most distinctive combination is:

1. a lower bound for all horizon-dependent stochastic realizations with arbitrary intervening widths, obtained from conditional-centroid entropy transport;
2. an explicit rational no-idle LPS orbit with exact cut profile and full numerical spectral constants;
3. a uniform accuracy crossover from exact exponential width to positive-error polynomial width;
4. a complete-configuration reduction that converts the stochastic-width obstruction into an optimal one-pass bit-space lower bound; and
5. a legality-preserving deterministic integer upper algorithm with the same order.

The sharp bit-space theorem is not merely the statement that a constant-dimensional real linear recurrence exists. Its point is that negative or real linear coordinates do not constitute a nonnegative finite-state implementation, and accuracy must be stored somewhere in a classical one-pass simulator.

### 5.2 Close classical inputs

The following inputs are classical or imported:

- invariant polyhedral cones and positive realization;
- probabilistic and weighted automata;
- exact LPS/Pinochet Lobos--Pittet spectral norms;
- nonbacktracking free-group radial polynomials;
- Rényi/Kullback--Leibler monotonicity;
- entropy continuity under transport;
- tail structure of finite nonhomogeneous Markov chains;
- compact-group orbit geometry; and
- elementary fixed-denominator integer approximation.

The manuscript generally credits these correctly. The contribution lies in their synthesis with the all-word stochastic realization resource, not in a new spectral theorem or a new general entropy inequality.

### 5.3 Missing current quantum-automata comparisons

The new literature section compares Benvenuti--Farina, Ambainis--Watrous, and Panduranga Rao--Vinay. It should also compare at least:

- Z. Chen and J. Wu, *The Quadratic State Cost of Classical Simulation of One-Way Quantum Finite Automata*, arXiv:2604.07058 (v2 dated 27 August 2026); and
- Z. Chen and J. Wu, *On the Simulation Cost of Quantum Finite Automata*, arXiv:2605.10682.

These works concern exact probabilistic simulation under strict-cutpoint language semantics. They prove worst-case `Theta(n^2)` PFA simulation for an `n`-dimensional one-way general QFA and `Theta(c q^2)` for a hybrid one-way model. They do not give the present full density-matrix numerical output, worst-word approximation, accuracy-dependent one-pass bit-space, or legal-decoder theorem. Thus they do not subsume Revision 64. Nevertheless, they directly address quantitative classical simulation cost for finite quantum automata and use prepare--test/state-complexity obstructions. Omitting them makes the 28 September 2026 author-side priority comparison materially incomplete.

A revised paper should explain exactly why strict-cutpoint state simulation and full-vector numerical approximation lead to different invariants, and whether either proof technique transfers.

### 5.4 Four-leading-journal significance

The package contains serious mathematics, but the breadth and external consequence remain below the four-leading-general-journal threshold. The strongest computational theorem is for a fixed qubit/LPS task. The generalization assumes a full-action gap and all-direction caps and uses Euclidean-ball outputs. The crossover theorem has a subexponential multiplicative uncertainty. The structural strong converse uses fresh nondisturbing probes. No major recognized open problem outside this revision program is resolved.

The appropriate significance comparison is therefore with strong specialist work in probability, automata/streaming complexity, positive realization, harmonic analysis, control, and quantum-information theory—not with a general theory already compelling across broad areas of mathematics.

---

## 6. Relation to the repository-wide pipeline

The repository's independent analytic dependency graph remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent.
```

The open obligations include raw unsmoothed local limits, stopped-path entropy/LDP recovery, a global past kernel, canonical shell conditioning, process CLT and Mosco recovery, nonlinear Nisio resolvents and graph cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction.

The spherical entropy potential, LPS spectral input, complete-configuration reduction, and integer streaming algorithm do not establish those gates. The local paper does not require them for correctness. Conversely, the existence of the larger Theta program cannot be used to raise the significance of this local manuscript. All A2-replacement, B4/C2 aggregate, eleven-paper, and whole-program completion flags correctly remain false.

---

## 7. Required revisions before specialist submission

1. **Update the 2026 priority comparison.** Add Chen--Wu arXiv:2604.07058 and arXiv:2605.10682, and distinguish strict-cutpoint PFA state cost from legal full-vector numerical approximation and precision-dependent bit-space.

2. **Keep the two resources separate.** The label-width invariant still permits arbitrary real tables. The charged bit-space theorem is a separate theorem for a fixed implemented task; it does not retroactively price every earlier upper realization.

3. **Keep “fixed program” visible.** The conventional bit-space corollary must not be read as allowing a different uncharged finite-control program for every `N,L`.

4. **State fixed-input dependence in the rational-orthogonal corollary.** Dimension, alphabet, rational denominators, seed, cap constants, and spectral constants must be fixed independently of the stream parameters.

5. **Do not overstate crossover sharpness.** The exponential rate is sharp, but a factor `exp[O(sqrt(N log N))]` remains. The exact saturation window and multiplicative equivalent are open.

6. **Keep the full-action spectral hypothesis explicit.** Contraction on the advertised three-dimensional representation is insufficient. The LPS norm is a deep imported theorem.

7. **Keep the no-idle scope separate from terminal stationarization.** v62 removes identity/returns for the quantitative occupation theorem, not for the general same-width clock-removal theorem.

8. **Preserve the oracle disclaimer in the structural paper.** Fresh nondisturbing probes are not repeated quantum measurements and not a general POMDP/HMM observation model.

9. **Submit the articles separately.** The 44-page quantitative and 40-page structural papers address different problems. The 92-page complete edition should remain archival.

10. **Compress the journal-facing provenance.** The repository evidence is excellent, but the submission should foreground theorem statements and proofs rather than revision genealogy.

11. **Clean the bibliography.** The Benvenuti--Farina tutorial appears under two keys, and the Pinochet Lobos--Pittet theorem references should consistently distinguish the one-step LPS bound from the exact radial-average theorem.

12. **Obtain independent expert priority opinions.** At minimum, one from probabilistic/weighted automata and positive realization, and one from quantum finite automata/streaming complexity.

13. **Retain the exact-head attestation.** The read-only workflow is a genuine strength and should be linked from a stable release.

14. **Consider a signed release tag.** This is archival hardening rather than a mathematical requirement.

---

## 8. Detailed comments

1. In the space theorem, “complete private configuration” is the correct primitive. It should remain defined before any machine-specific work-tape corollary.

2. The boundary reduction is more permissive than the implemented algorithm because its stochastic rows may depend on the public boundary index. This is appropriate for a lower bound and should be said explicitly.

3. Almost-sure termination between commands is necessary. Without it, the boundary row could have subunit mass. The present assumption is correctly included.

4. Mean correctness is weaker than samplewise correctness. The paper should continue to emphasize that the lower bound already holds under this weaker condition.

5. Every randomized output must remain legal samplewise. Otherwise conditional averaging could hide illegal outputs outside the density-matrix set.

6. The one-configuration witness in the lower proof is useful for absorbing additive constants. Retain the explicit pair of command words.

7. Parameter input length and workspace are different resources. The saturating parser handles workspace correctly; avoid language suggesting that the full decimal or binary precision string is stored.

8. The output encoding uses hexadecimal in the reference implementation but binary bit complexity in the theorem. This is harmless because both are constant-radix encodings.

9. The reference Python interpreter is not itself a certified optimal-space machine. Its docstring correctly says that it executes the integer recurrence rather than literally measuring Python allocator space.

10. The scratch-size regression is useful but remains finite testing. The proof, not the tested horizon list, establishes the universal bound.

11. The exact-mode threshold `b>=N` is a convenient constant-level choice. It need not minimize actual memory for every small input; only the asymptotic order is claimed.

12. The no-idle exact profile is a coset profile, not the cardinality of the whole free-group sphere. The stabilizer argument and right-coset convention should remain adjacent.

13. The robust error interval `25^(-N)/16` is horizon dependent. It is not a fixed-positive-error exponential lower bound.

14. The fixed-positive-error linear law and the exponentially small-error exact profile use different proof inputs. Keep them separate.

15. In the v63 crossover, the nonbacktracking operator is an average over formal reduced words. Physical relations do not invalidate the operator polynomial or the exact formal-word upper machine.

16. The full-action projection must be onto all invariant functions, not merely global constants in a possibly nontransitive action.

17. The entropy in the occupation theorem is an auxiliary relative entropy of smoothed direction measures, not hidden-register Shannon entropy.

18. The causal tail-capacity lemma relies on observation tail events. It does not imply that every hidden process with infinitely many predictive rows requires infinite state.

19. The strong causal theorem's threshold one is natural because total variation is at most one. The earlier one-continuation threshold one half is not the final theorem.

20. The journal abstract should not combine every historical result at equal weight. Lead with the space theorem and the accuracy crossover; move preservation statements out of the abstract.

21. The general rational-orthogonal upper bound does not construct orbit-hull stochastic rows. It directly simulates the rational linear orbit in the unit ball. This is an important simplification and should be stated plainly.

22. The fixed qubit result outputs a numerical density matrix. It is not a classical procedure that physically prepares the corresponding quantum state.

23. The proof does not imply a time lower bound. The converse explicitly permits unlimited internal running time.

24. The exact-head workflow is read-only with respect to the attested tree. That trust separation should be preserved in future revisions.

---

## 9. Final assessment

Revision 64 is the strongest version of this manuscript program that I have reviewed. It contains three credible specialist-level advances:

- return-free sharp stochastic-width occupation through entropy transport;
- an exponential accuracy crossover for Ramanujan spherical alphabets; and
- an optimal charged one-pass bit-space law with a concrete legality-preserving integer algorithm.

The structural companion supplies a separate all-error-below-one strong converse for repeatable fresh observations. The source and exact-head reproduction chain is unusually strong.

I did not find a fatal mathematical gap in the inspected arguments. The main remaining concerns are significance, breadth, quantitative residual gaps, oracle-like structural assumptions, and incomplete independent priority positioning—especially the omission of directly relevant 2026 quantum-automata simulation-cost work.

**Recommendation: reject at the four leading general mathematics journals; encourage separate submissions to strong specialist venues after current-literature revision, independent priority review, and editorial compression.**
