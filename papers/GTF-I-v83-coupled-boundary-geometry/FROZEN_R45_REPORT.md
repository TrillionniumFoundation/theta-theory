# Referee Report — General Theta Foundations I, Revision 68 (r45)

**Quantitative manuscript:** *Joint Instrument Coding Laws and Boundary-Uniform Rational Realization*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v68-boundary-uniform-coding-2026-10-03`
- `revision/general-theta-foundations-i-v68-referee-ready-2026-10-03`

**Reviewed exact final head:** `d9d8c464282157485813041d181e909e648b1f4f`  
**Candidate publication:** `fdac5733790f2acd10923d7ef686fe8ea347bb96`  
**Qualified native source:** `9e52ce69cd1270f49249889c85a446f9cdde44ac`  
**Source predecessor:** Revision 67 publication `98a4b12126502ea41c620b58bad4b9aa30f9c72c`  
**Controlling external report:** Revision 67 r44, `68c69a4a2e8b4e3b11c43a181806ab578584b719`  
**Controlling pipeline audit:** `7a9586cd8cf7995152fbbf501f3e47da4aa89900`  
**Source qualification workflow:** `37111159523`, conclusion `success`  
**Exact-head read-only reconstruction:** `37111465009`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v68-external-referee-r45-2026-10-03`  
**Date:** 3 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 68 is a substantial and mathematically coherent response to r44. It closes two of the most important local gaps left by Revision 67.

First, on a fixed blockwise-positive instrument body of real affine dimension

```text
s = d^2(m n^2 - 1),
```

it upgrades the earlier fixed-error reusable-description law to the genuinely joint horizon--precision statement

```text
log_2 M_N(delta;a)
  = (s/2) log_2 N + s log_2(1/delta) + O_{d,n,m,a}(1)
```

uniformly for every `N >= 1` and `0 < delta <= 1/32`. The new point is not the finite-dimensional volume calculation by itself, but a uniform local binary testing lemma that preserves the precision term all the way to Bernoulli endpoints, followed by a pair-dependent normalized-Choi test. I found no fatal defect in this chain.

Second, the paper proves an actual boundary theorem, though for a deliberately restricted family: input-erasing preparation instruments. If outcome `y` has output-rank bound `r_y`, it identifies the rank-stratum dimension

```text
v = sum_y r_y(2n-r_y) - 1
```

and proves

```text
log_2 P_N(delta;r)
  = (v/2) log_2 N + v log_2(1/delta) + O_{n,m,r}(1)
```

without a positive eigenvalue margin. The exact adaptive metric reduces to the trace distance of `N` copies of the associated classical--quantum preparation state. The upper construction uses a rational triangular-factor code that does not store irrational Cholesky entries, never increases the declared block ranks, and preserves zero outcomes exactly. The converse uses a quantitatively bi-Lipschitz patch in the maximal rank stratum and the same local binary test. I did not find a fatal gap here either.

The four-leading-journal disposition nevertheless remains negative. The new results are sharp and useful finite-dimensional coding theorems, but they concern reusable **descriptions of supplied matrix data**, not the learning of an unknown instrument, not mutable online workspace, and not a finite-classical-resource physical simulation of an unknown quantum input. The boundary theorem is exact for input-erasing preparation instruments; it does not classify support-changing and coherent directions of a general disturbing instrument. Constants are fixed-dimensional and margin-dependent in the interior theorem. The half-parameter logarithmic scale has strong antecedents in quantum population compression and finite-dimensional parametric coding. Most importantly, the exact theorem-level priority boundary remains author-audited rather than independently settled.

A further literature correction is required. The focused comparison cites Salek--Hayashi--Winter for adaptive channel discrimination, but it omits Cooney--Mosonyi--Wilde, *Strong converse exponents for a quantum channel discrimination problem and quantum-feedback-assisted communication* (arXiv:1408.3373). That paper treats discrimination against replacer channels and explicitly discusses the reduction of two replacer channels to state discrimination. It does not contain the present finite-use covering theorem or rational rank-preserving codec, but it is a direct antecedent for the “adaptive processing gives no advantage for input-erasing channels” mechanism and should be discussed.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is now a strong specialist-level contribution in quantum information theory, finite-dimensional metric entropy, and exact rational coding. I would encourage submission to a strong specialist venue after an independent priority review, a direct comparison with replacer-channel discrimination, and editorial compression. The retained structural manuscript is also a coherent specialist contribution, but it is mostly inherited in this revision and retains its fresh nondisturbing-probe scope.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 68 manuscript branches are identical at

```text
d9d8c464282157485813041d181e909e648b1f4f.
```

The final head is a direct successor of the candidate publication and adds the exact-head reconstruction request. The candidate publication descends from qualified native source `9e52ce69...`. Revision 68 itself descends from the exact Revision 67 publication reviewed in r44.

A higher-numbered work branch, `revision/general-theta-foundations-i-v69-full-accuracy-centres-2026-10-03`, exists, but at the time of this report it contains only an explicit continuation anchor. That anchor states that it is not a proof completion. No v69 referee-ready publication and no v70 branch were present. Revision 68 is therefore the latest completed referee-ready object.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/38-intrinsic-instrument-entropy.tex`;
- `sections/39-adaptive-description-entropy.tex`;
- `sections/40-joint-description-precision.tex`;
- `sections/41-boundary-preparation-codes.tex`;
- `preparation_codec.py` and `check_preparation.py`;
- the inherited exact Choi and instrument codecs and their regression suites;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r44 external report and companion audit;
- the resource ledger, schemas, build receipt, source hashes, theorem locations, and preservation manifest;
- the source-qualification workflow; and
- the exact-head read-only workflow, including its separate reconstruction of the immutable v67 publication reviewed in r44.

I also made a targeted current and classical literature comparison. This remains a referee assessment, not a formal proof-assistant verification and not an exhaustive search across all quantization, quantum statistics, and channel-coding literature.

---

## 2. Executive assessment of the new mathematics

### 2.1 A uniform local binary lower bound

The new elementary lemma proves

```text
TV(Bern(p)^N, Bern(q)^N)
  >= (3/32) min{sqrt(N)|p-q|, 1}
```

for every `N >= 1` and all `p,q` in `[0,1]`, including arbitrarily small gaps and endpoint probabilities.

The proof uses a clipped affine ramp centered at the midpoint of the two binomial means. Differentiating its binomial expectation gives `N` times the expected one-step increment under a `Bin(N-1,t)` law. Chebyshev keeps at least three quarters of that law in the affine portion of the ramp, uniformly even when `p=0` or `q=1`. Larger parameter gaps follow by monotone coupling.

This lemma is elementary, but it is exactly the missing uniform ingredient in the previous fixed-error argument. It avoids a hidden variance floor, a normal approximation, or an error term depending on `p,q,N`.

### 2.2 Transfer to instrument geometry

For two legal instruments, the normalized flagged Choi difference is a trace-zero Hermitian operator. Measuring its positive spectral projection gives a Bernoulli probability gap equal to half its trace norm, and therefore at least half its Hilbert--Schmidt norm. Repeating the normalized Choi input `N` times and applying the binary lemma yields

```text
d_N(J,L)
  >= (3/16) min{sqrt(N)||J-L||_2/(2d), 1}.
```

The test may depend on the pair of packing points. This is legitimate for a metric supremum. It is not a universal tomography measurement and does not identify every codeword simultaneously.

### 2.3 Joint horizon--precision entropy in the strict interior

The positive-margin instrument body contains a fixed `s`-dimensional Euclidean ball in the affine marginal-constraint space. Packing that ball at scale `delta/sqrt(N)` and using the preceding pairwise test gives the lower bound

```text
M_N(delta;a) >= c (sqrt(N)/delta)^s.
```

The inherited intrinsic rational grid, combined with the classical-programme estimate on the same fixed positive-margin body, gives the matching upper bound. Crucially, both estimates are finite and uniform throughout the declared range, so the additive remainder no longer hides dependence on `delta`.

I regard this theorem as correct in its fixed-dimensional, fixed-margin, supplied-description scope.

### 2.4 Exact adaptive reduction for preparation instruments

For a preparation instrument

```text
R_sigma,y(X) = tr(X) sigma_y,
```

each use discards its input and emits one classical--quantum preparation state. Any `N`-use adaptive tester, including arbitrary finite references, quantum memory, feedback, and public stopping, is therefore one common quantum processor applied to `N` independent copies of the preparation state. Trace contraction gives the upper comparison. A tester that uses all calls and retains every classical--quantum output gives equality.

Thus

```text
d_N(R_sigma,R_tau)
 = ||sigma_block^⊗N - tau_block^⊗N||_1.
```

This is a clean exact finite-use identity. It relies on input erasure, not merely on entanglement breaking. It should be compared explicitly with the earlier replacer-channel discrimination literature.

### 2.5 Singular triangular factors and rational encoding

A positive semidefinite block admits the standard no-pivot Cholesky recursion. At a zero residual pivot, positivity forces the remaining residual row and column to vanish, so that pivot contributes no factor column. A nonzero pivot contributes one real diagonal coordinate and two real coordinates for each lower complex entry.

For an `n x n` block of rank at most `r`, the number of real factor coordinates is at most

```text
r(2n-r).
```

Across outcome blocks, trace normalization removes one real degree of freedom and gives the dimension `v` above.

The encoder takes the largest-magnitude factor coordinate as an anchor, rounds all coordinate ratios on an integer grid, forms integer lower-triangular factors, and normalizes their Gram matrices by their total trace. Every decoded block is positive semidefinite. No new factor columns are introduced, so ranks cannot increase. A zero input block produces no pivots and remains exactly zero.

For rational target matrices, all squared factor coordinates and their signs are rational even when the factor coordinates themselves are irrational. The encoder obtains the required integer floors using exact rational comparisons and integer square roots. It does not store algebraic square roots.

The pure-factor comparison and tensor-product estimate give

```text
d_N(R_sigma,R_tilde_sigma)
 <= 4 sqrt(N(h-1))/B.
```

The finite code counts the pivot mask, anchor/sign data, and mixed-radix payload. Expanded matrices and encoder workspace are explicitly separate resources.

### 2.6 Rank-stratified converse

A maximal rank stratum contains a local gauge-fixed Cholesky patch of real dimension `v`. Positive leading diagonal entries make the factorization unique. After trace normalization, the factor-to-state map and its inverse are smooth on a sufficiently small closed patch. The patch is therefore quantitatively bi-Lipschitz in Euclidean factor coordinates and tuple Hilbert--Schmidt distance.

Volumetric packing of this patch at scale `delta/sqrt(N)`, followed by the same binary test, gives the matching lower exponent. Smaller-rank strata cannot increase the upper exponent, while the maximal stratum already supplies the lower one.

The special cases are consistent:

- one full-rank density matrix: `v=n^2-1`;
- one pure state: `v=2n-2`;
- a classical distribution on `m` outcomes: `v=m-1`;
- `v=0`: a singleton family.

---

## 3. Correctness audit

### 3.1 Binary derivative identity

For `S ~ Bin(N,t)` and a bounded statistic `f`, differentiation gives

```text
d/dt E_t f(S)
 = N E_t[f(T+1)-f(T)],
```

with `T ~ Bin(N-1,t)`. In the proof, the center of the clipped ramp is fixed at `N(p+q)/2`. When `q-p <= N^(-1/2)`, the mean of `T` remains within `sqrt(N)/2+1` of this center. On the event `|T-E T| <= sqrt(N)`, both `T` and `T+1` remain inside the affine interval. Chebyshev gives probability at least `3/4`. The constant `3/32` follows.

For a larger gap, the intermediate parameter `p+N^(-1/2)` lies below `q`; monotonicity of the statistic under the standard binomial coupling supplies the saturated constant. I find this proof correct.

### 3.2 Choi normalization and constants

The manuscript consistently uses input-first, unnormalized Choi blocks whose total trace is `d`. The repeated test uses the normalized direct-sum Choi state. The positive spectral projection of a trace-zero difference gives half the trace norm. The Hilbert--Schmidt lower estimate and the final factor of two from unhalved trace distance are consistent.

### 3.3 Interior packing

The central instrument has every block eigenvalue `1/(mn)`. A tuple Hilbert--Schmidt perturbation of radius `1/(mn)-a` has every block operator norm below that radius and remains in the blockwise `a`-positive body. A maximal separated set in this affine ball gives the stated volume lower bound.

At the chosen separation `32d delta/sqrt(N)`, the local Choi test separates packing points by more than `2delta`, including the saturated branch because `delta <= 1/32`. Therefore no decoded center can cover two packing points. The centers themselves need only be legal; they need not retain margin `a`.

### 3.4 Preparation processor identity

The adaptive tester can be represented as a sequence of common CPTP maps that consume one fresh preparation state at each use. Its output in either hypothesis is the image of the corresponding tensor-power preparation state under the same processor. This gives the upper trace-norm contraction. The lower tester realizes the tensor-power states themselves. Public stopping is handled by supplying `N` copies and ignoring unused suffix copies.

The proof neither assumes a classical processor nor infers physical classical simulation.

### 3.5 Zero pivots

At a zero diagonal entry of a positive semidefinite residual matrix, every entry in the corresponding row and column must vanish. The no-pivot recursion therefore remains valid on singular blocks. Positive pivots are precisely the nonzero factor columns; their number equals the rank.

The coordinate order in the implementation matches the written factor order. Independent Gaussian-rational elimination in the regression suite checks that the number of pivots agrees with matrix rank on finite cases.

### 3.6 Exact ratio encoding

Each residual pivot and each residual matrix entry is rational. A diagonal factor square is the pivot; an off-diagonal real or imaginary coordinate square is the square of a rational residual component divided by that pivot. Its sign is also rationally decidable. Hence

```text
floor(B sqrt(q))
```

can be computed as the integer square root of `floor(B^2 q)` without representing `sqrt(q)`.

The mixed-radix body parser checks canonical hexadecimal form, payload range, pivot ordering, rank promises, public dimensions, coordinate count, family dimension, and the advertised error certificate. Target verification replays the encoder; bare decoding certifies syntax and legality only.

### 3.7 Product error estimate

The normalized factor coordinates purify the classical--quantum preparation state. If two unit factor vectors are at Euclidean distance `eta`, their `N`-fold pure-state trace distance is at most `2 sqrt(N) eta`. Partial trace cannot increase trace norm. Combining this with directed ratio rounding gives the displayed adaptive error bound.

### 3.8 Stratum chart

On the selected patch, every nonzero-rank block uses a lower-trapezoidal factor with positive leading diagonal. This fixes the unitary gauge. The factor-to-state map is injective and has the standard Cholesky inverse on the leading principal block, followed by linear recovery of the lower rows. Restriction to a sufficiently small compact coordinate ball gives uniform upper and lower Lipschitz constants. The packing argument is therefore legitimate.

I found no fatal correctness defect in these new arguments.

---

## 4. Reproducibility and implementation evidence

The exact source qualification run `37111159523` completed successfully on native source `9e52ce69...`. The final publication head `d9d8c464...` subsequently triggered read-only workflow `37111465009`, which completed successfully. That job:

1. checked out the exact v68 head;
2. rebuilt source, all manuscript pages, and finite tests;
3. rebuilt the minimal journal package;
4. independently checked the immutable v67 publication reviewed in r44; and
5. uploaded separate read-only attestations.

The build receipt records:

- an 18-page focused quantitative paper;
- a 40-page structural paper;
- a 118-page complete edition;
- an isolated rebuild;
- no recorded LaTeX diagnostics;
- normal/optimized test agreement;
- preservation of 115 predecessor native files;
- preservation of 394 prior active labels and 419 current active labels; and
- the inherited and new exact regression suites.

`check_preparation.py` checks the binary inequality on rational grids and very small endpoint gaps; singular factors; nonleading pivots; extreme eigenvalue ratios; exact zero outcomes; independent rank elimination; exact product trace bounds; canonical parsing; tampered metadata; wrong-target replay; and the actual command-line interface. Its scope statement correctly denies universal proof or priority certification.

These are strong reproducibility practices. They are not a proof assistant, an independent novelty determination, a cryptographic authorship certificate, or a journal decision. The exact final commit is unsigned, and the package does not claim otherwise.

---

## 5. Novelty, priority, and significance

### 5.1 What is genuinely added

The strongest local increment is the combination of:

- a finite, endpoint-uniform binary lower bound;
- a pairwise Choi test preserving the `delta/sqrt(N)` scale;
- a joint horizon--precision description law with a uniform remainder;
- an exact finite-use reduction for preparation instruments;
- a rank-stratified boundary exponent;
- an exact rational factor codec that preserves ranks and zero outcomes; and
- target-bound, executable certificates.

This is more than a new test suite or a reformulation of Revision 67.

### 5.2 Classical and neighboring ingredients

The following ingredients are classical or close to classical:

- finite-dimensional volume packing;
- Bernoulli product testing and monotone coupling;
- Choi-state binary discrimination;
- dimension of rank-`r` positive semidefinite strata;
- Cholesky/Gram parameterization;
- tensor-power pure-state trace bounds;
- the half-parameter logarithmic scale in quantum population coding; and
- the absence of an adaptive advantage for pairs of replacer channels in channel-discrimination theory.

The paper generally does not claim these ingredients individually as new. Its claim rests on their exact combination with the supplied-description interface, adaptive covering metric, rank promises, legal rational decoding, and finite certificate format.

### 5.3 Missing direct antecedent

Cooney, Mosonyi, and Wilde, arXiv:1408.3373, should be added. Their setting is asymptotic binary channel discrimination, not finite-family covering and not rational encoding. Nevertheless, the paper explicitly treats an arbitrary channel versus a replacer and notes that two replacer channels reduce to state discrimination. This is a closer antecedent for Lemma `productreplacer68` than the current comparison alone suggests.

The manuscript should distinguish clearly:

- exact finite-use trace-norm equality for two preparation instruments;
- asymptotic binary error exponents for replacer-channel discrimination; and
- covering numbers of an entire supplied family.

### 5.4 Why the four-journal bar is not met

The present results remain bounded by several independent limitations:

1. **Fixed-dimensional metric entropy.** The dimensions and rank bounds are fixed. Constants are not uniform in dimension.
2. **Strict-interior dependence.** The general instrument theorem retains a fixed blockwise eigenvalue margin. No uniform limit as that margin vanishes is proved.
3. **Restricted boundary family.** The boundary theorem concerns input-erasing preparation instruments. General disturbing instruments may have support-changing, coherent, and reversible directions with different reuse scales.
4. **Description, not computation in general.** The code length is a reusable description length for supplied matrices. Expanded decoder storage, encoder workspace, and variable-data mutable simulation are separate.
5. **Description, not learning.** No unknown-instrument query or sample complexity is proved.
6. **Description, not physical classical simulation.** The decoded object remains a quantum instrument or state. It does not implement unknown entangled inputs with finite classical messages.
7. **Priority remains open.** The author-side audit is careful but not independent and still needs the direct replacer-channel comparison.
8. **No repository-wide closure.** The independent A/B/C/D analytic programme remains open in every aggregate status.
9. **No broad external consequence.** The revision closes important internal theorem gaps but does not resolve a recognized external problem of comparable general visibility.

These points do not diminish the specialist value of the work. They do prevent a recommendation to one of the four leading general mathematics journals.

---

## 6. Required revisions before specialist submission

1. **Add Cooney--Mosonyi--Wilde to the focused comparison.** State precisely what their replacer-channel discrimination results do and do not imply for the exact finite-use product identity and family covering law.

2. **Keep the supplied-description interface on page one.** The encoder is given matrix data. No unknown-channel learning or tomography claim should be inferred.

3. **Keep the physical-simulation disclaimer adjacent to every codec theorem.** A rational Choi or factor description is not a finite-classical-message processor for unknown entangled inputs.

4. **State fixed dimensions and public rank bounds in every main theorem.** The `O(1)` remainder depends on them; no dimension-uniform claim is proved.

5. **Keep interior and boundary theorems visibly separate.** The general instrument theorem has a positive block margin. The boundary theorem is for preparation instruments only.

6. **Do not use “boundary-uniform” without the family qualifier.** A reader could otherwise misread it as a theorem on the entire instrument body.

7. **Expose the metric convention in the theorem statement.** `d_N` is an unhalved final-state trace norm over common bounded adaptive testers.

8. **Retain pair-dependence of lower tests.** The packing converse does not give a universal measurement or identification decoder.

9. **Clarify the rank variables.** The `r_y` are output-state ranks in the preparation family; the corresponding Choi ranks are multiplied by the input dimension.

10. **Separate payload length from encoder and expanded-decoder workspace.** The present resource ledger does this; the abstract should be equally explicit.

11. **Retain the `delta <= 1/32` range or prove a clean extension.** The current saturation constants use this bound.

12. **Keep the v63 multiplicative width gap separate.** The new description law does not close the earlier label-width crossover.

13. **Commission independent priority review.** The author-side literature file cannot satisfy this request by declaration.

14. **Submit the 18-page focused quantitative article, not the 118-page research edition.** The complete edition is valuable archival material but should not be the principal journal object.

---

## 7. Detailed comments

1. The phrase “uniform binary lower bound” should always include the constants and the unhalved/halved total-variation convention.

2. In the Choi corollary, remind the reader that the positive spectral projection is a pair-specific two-outcome measurement.

3. In the interior theorem, specify whether the covering centers may lie outside the positive-margin body. The proof allows arbitrary legal centers, which strengthens the converse.

4. The lower volume estimate is in the real affine translation space satisfying the joint marginal constraint, not in the full ambient Hermitian space.

5. The fixed error range is not merely cosmetic: it ensures the saturated binary lower bound exceeds `2delta`.

6. The preparation metric identity is exact because both hypotheses are input erasing. “Entanglement breaking” alone is insufficient.

7. The common processor in the product identity is quantum. It is not a classical simulation protocol.

8. The no-pivot Cholesky argument should retain the one-line proof that a zero PSD diagonal forces the residual row and column to vanish.

9. Pivot positions, not only the number of pivots, are part of the finite code header.

10. Rounding may decrease rank. The theorem correctly claims nonincrease, not exact rank preservation.

11. When a diagonal factor coordinate is not the anchor, directed ratio rounding may eliminate that column. This is harmless and should not be described as a defect.

12. The exact encoder uses rational squared coordinates. It does not output a rational Cholesky factor of the target.

13. The factor code's normalization denominator is data dependent but explicitly bounded. Its bit length is part of expanded output, not the compressed body alone.

14. The rank-stratum inverse uses a leading full-rank block. This is a local chart, not a global parameterization of every support pattern.

15. The `v=0` case should remain a separate sentence; the asymptotic logarithmic expression otherwise obscures the singleton.

16. The classical `m-1` case is an important sanity check and should remain in the main text.

17. The full-state `n^2-1` coefficient and pure-state `2n-2` coefficient align with standard manifold dimensions; this should be credited as geometry, not presented as an unexpected dimensional discovery.

18. The codebook consists of valid decoder images, not all abstract mixed-radix words. Invalid words do not count as legal centers.

19. Bare decode and target-bound verification are different interfaces. The schema files correctly distinguish them.

20. Finite tests of the binary inequality do not prove the continuum lemma; the written derivative proof does.

21. Finite rank tests do not prove the global stratum theorem; they qualify the implementation.

22. The final head is unsigned. Exact hashes and read-only CI establish reconstruction, not authorship.

23. The v69 anchor should not be cited as a completed successor until a proof-complete referee-ready publication exists.

24. No successful build, page comparison, or arithmetic regression changes the independent A/B/C/D pipeline flags.

---

## 8. Pipeline assessment

The local coding genealogy is now:

```text
v66 exact rational Choi legality and trajectory coding
  -> v67 intrinsic affine instrument entropy
       + classical-programme upper comparison
       + repeated normalized-Choi lower testing
  -> v68 endpoint-uniform local binary test
       -> joint N,delta interior description law
       + input-erasing preparation reduction
       -> singular triangular-factor code
       -> rank-stratified boundary law.
```

This is a coherent local programme. It does not establish any of the repository's independent raw local-limit, stopped large-deviation, global-kernel, shell-conditioning, Mosco/Nisio, filtering/LAN, changing-filtration response, or posterior-contraction gates. The status file correctly leaves

```text
historical_A2_replacement = false
B4_aggregate             = false
C2_aggregate             = false
eleven_paper_aggregate   = false
whole_Theta_program      = false.
```

The wider repository cannot be used as a significance multiplier for this paper, and this paper cannot be used as evidence that the wider analytic pipeline is closed.

---

## 9. Final assessment

Revision 68 successfully addresses the central mathematical objections of r44 that were tractable within the current programme:

- it proves the missing joint precision term rather than hiding it in a fixed-error remainder;
- it supplies an actual rank-stratified boundary theorem for a nontrivial family;
- it handles zero outcomes and singular states exactly;
- it gives a legal rational code with rank nonincrease and target-bound verification;
- it preserves all inherited hypotheses and open boundaries honestly; and
- it now has exact-head read-only reconstruction evidence.

I found no fatal mathematical gap in the new proof package. The manuscript has reached the level of a strong specialist contribution.

It has **not** reached the Annals / Inventiones / JAMS / Acta threshold. The decisive limitations are the fixed-dimensional supplied-description setting, the preparation-only boundary theorem, the separation from learning and physical simulation, the still-open general disturbing-instrument geometry, and unresolved independent priority.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused specialist submission after the literature and scope revisions above.**
