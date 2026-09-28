# Referee Report — General Theta Foundations I, Revision 58 (r39)

**Manuscript package:** *General Theta Foundations I*, Revision 58  
**Focused quantitative article:** *Stochastic Width of Compact Orbits and a Rational Exact–Noisy Separation*  
**Focused structural article:** *Clock Removal and Finite Physical Actions in Stochastic Realization*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v58-finite-input-2026-09-27`
- `revision/general-theta-foundations-i-v58-referee-ready-2026-09-27`

**Reviewed publication head:** `27be4b236b9336bbfa2fa855dec3a346d63b8be7`  
**Readable native theorem source:** `3997b7247b75b892be1fd6e313bf81b9e69c11c1`  
**Predecessor publication:** Revision 57, `0e07470b9693a2789af00222f063e715a83ff454`  
**Controlling prior report:** r38, `5b2fb03f87a6b28bddcef51d498a0c78429bfa22`  
**Review branch:** `review/general-theta-foundations-i-v58-external-referee-r39-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 58 is a substantial and technically serious improvement over Revision 57. I did not find a fatal mathematical gap in the new least-orbit-dimension theorem, the explicit rational free experiment, the robust exponentially small error interval, the rational compiler, or the inherited structural chains that I re-audited. The focused quantitative paper in particular now contains a genuine finite-input exponential-exact versus polynomial-noisy separation, rather than an existential algebraic/transcendental endpoint. The author has also separated the quantitative and structural articles and has been unusually explicit about resource conventions, imported theorems, finite checks, and unresolved logarithmic and pipeline gaps.

The top-four disposition nevertheless remains negative. The central realization model is specialized and permits nonuniform, horizon-dependent real transition tables while leaving the clock, table construction, exact arithmetic, and exact sampling outside the primary width invariant. The clock-removal result requires eventual approximate returns at every sufficiently large length. The quantitative converse retains a logarithmic loss and an imported, non-effective spectral-gap constant. The output theory is terminal and convex-valued rather than an online or pathwise classification. Most importantly, the theorem-level priority boundary against compact stochastic semigroups, nonnegative matrix groups, positive realization, advice automata, probabilistic/weighted automata, and controlled hidden-state realization has not been independently settled. The author-side literature audit is careful but expressly not an independent priority clearance.

**Disposition outside the four leading general journals:** the two focused articles are plausible strong specialist contributions after conventional external priority checking and further editorial tightening. I would not recommend another wholesale mathematical reconstruction. I would recommend separate specialist submissions, with the complete 63-page preservation edition treated as repository history rather than as the submitted article.

---

## 1. Scope, genealogy, and material reviewed

The two advertised Revision 58 branches are identical and point to the same publication commit, `27be4b...`. No Revision 59 branch was present at the time of this review. The publication commit is one commit beyond the readable native theorem source `3997b724...`; that final step adds rendered documents, qualification records, page images, archives, and the review-ready entry without changing the native theorem source.

I reviewed the active Revision 58 source graph, with particular attention to:

- `quantitative.tex`, `structural.tex`, and `main.tex`;
- `sections/12-stationarization.tex`;
- `sections/09-purification.tex`;
- the finite-quotient and boundary chain inherited by the structural paper;
- `sections/16-uniform-orbits.tex`;
- `sections/20-minimal-orbits.tex`;
- `editions/extreme-profile.tex`;
- `sections/21-rational-endpoint.tex`;
- `sections/22-rational-compiler.tex`;
- `qubit_compiler.py` and `check_revision.py`;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r38 report and frozen repository-wide pipeline ledger;
- the committed build receipt, isolated-rebuild receipt, source hashes, theorem locations, and regression records; and
- the Revision 58 qualification workflow.

I also checked the exact branch genealogy from the Revision 57 publication, the equivalence of the two Revision 58 branch heads, the separation between the native-source commit and publication commit, and the status of repository-wide A/B/C/D completion claims.

The present report is a mathematical and editorial referee assessment, not a formal proof-assistant certificate and not an exhaustive independent search of every neighboring literature. Where the priority boundary remains uncertain, I say so explicitly rather than converting an author-side bibliography audit into a novelty theorem.

---

## 2. What Revision 58 genuinely adds

### 2.1 Uniform caps from the least orbit dimension

The most conceptual new theorem identifies the optimal exponent in the all-direction small-ball estimate with

```text
p_* = min_{||u||=1} dim G u,
```

for a fixed-point-free finite-dimensional orthogonal representation of a compact connected Lie group. This removes the need to verify a separate cap estimate for every possible conditional-centroid direction. The distinction between the least orbit dimension `p_*` and the chosen target-orbit dimension `q` is important: `p_*` controls the lower-width exponent, whereas `q` controls the inner-hull upper construction.

This is a real advance over Revision 57. It is not merely a repackaging of the special sphere or density-matrix calculations. The proof gives a uniform local-submersion estimate over the whole unit sphere and shows optimality of the exponent by selecting a least-dimensional orbit.

### 2.2 A fixed rational exact endpoint

The manuscript now displays concrete rational `2 x 2` unitaries `U,V` and a rational rank-one seed `P_0`. The generators are squares of explicit norm-five quaternions. A modulo-five rank-one matrix argument proves freeness for all reduced words, rather than extrapolating from finite enumeration. A third quaternion direction rules out a nontrivial projective stabilizer of the seed. The reachable pure states are therefore in bijection with the reduced free-word ball, giving the exact cut profile

```text
|S_t| = 2*3^t - 1.
```

This resolves the most conspicuous weakness of the Revision 57 endpoint: the example is now a fixed rational finite input, not a nonconstructively selected dense free pair with a transcendental seed.

### 2.3 Robustness at exponentially small positive error

The exact exponential profile is shown to persist throughout

```text
0 <= epsilon <= 625^(-N)/16.
```

The proof uses the denominator lattice of the induced Bloch rotations. At cut `t`, distinct reachable unit vectors are separated by at least `25^(-t)`. A fixed suffix preserves that distance. Small expected Frobenius error forces each prefix distribution to place positive mass on a label whose conditional decoder mean lies in a small cap about its target; the stated error scale makes these caps disjoint for all cuts `t <= N`.

This is stronger than a zero-error discontinuity statement and is one of the most attractive results in the revision.

### 2.4 A constructed rational compiler

The new compiler is not merely a finite-precision rounding theorem for a supplied realization. It builds a rational stereographic net, proves an inner-hull inclusion, constructs sparse common stochastic rows by exact rational barycentric identities, and uses legal density-matrix decoders. The positive-error version rounds only row probabilities to dyadic values and gives an explicit fair-bit budget.

The result remains pseudo-polynomial in the numerical horizon and inverse accuracy, as the paper correctly states. It is not a polynomial-time algorithm in the binary length of those parameters and is not a minimum-width solver.

### 2.5 Independent article architecture

Revision 58 finally implements the separation recommended in r38. The 18-page quantitative paper and 33-page structural paper are independently buildable and contain their own definitions and proofs. The 63-page complete edition preserves the historical development but is not used as a hidden proof dependency of the focused papers.

This architectural correction is successful.

---

## 3. Correctness audit of the new quantitative chain

### 3.1 Least-orbit-rank theorem

Let `r=p_*`. For each unit vector `u`, the infinitesimal orbit map has rank at least `r`, so at least one `r x r` minor is nonzero. Taking the maximum over the finitely many minors gives a continuous positive function on the unit sphere; compactness therefore supplies a uniform positive lower bound. Boundedness of all entries turns this into a uniform least-singular-value bound for a selected minor.

The proof then uses finitely many ordered exponential product charts. Uniform derivative control over the compact unit sphere makes the projected orbit map quantitatively injective in the selected `r` coordinates. The change-of-variables estimate gives `O(h^r)` volume for the inverse image of an ambient ball, uniformly in the unit vector and the center. A finite translate cover extends the estimate over the group. Finally, a least-dimensional orbit has locally positive smooth invariant density and supplies the matching lower scaling, proving optimality of the uniform exponent.

I find this argument sound. Two qualifications are correctly retained: the constants are not dimension-uniform, and the quantifier-elimination proposition assumes supplied exact algebraic infinitesimal matrices known to define the representation. It neither recognizes an arbitrary compact group input nor computes a spectral gap.

### 3.2 Executable contraction and the logarithm

The inherited all-direction cap theorem is used in the right place. Conditional centroids need not lie on the target orbit; an orbit-only cap estimate would not justify the maximum over arbitrary normalized conditional directions. The Haar union-bound defect has order `k^(-2/p)`. Spectral-gap smoothing, followed by averaging over a small group ball, produces a pointwise executable block of length `O(log k)`. The moving-centroid argument then yields the narrow-cut occupation bound and

```text
W_{N,epsilon} >= c (N/log(N+2))^(p/2).
```

The upper construction uses a quadratic inner approximation of the target orbit hull and gives exponent `q/2`. The manuscript does not hide the logarithmic mismatch. I found no correctness defect in this chain, but the logarithm is a real unresolved quantitative gap and remains one reason the result is not top-four sharp.

### 3.3 Quaternion freeness and the rational seed

The six norm-five quaternion numerators reduce modulo five to six rank-one matrices whose image lines are the six points of `P^1(F_5)`. The kernel line of each matrix is the image line of its inverse letter. Consequently, a product is zero modulo five exactly when adjacent inverse cancellation occurs; every freely reduced product remains nonzero. An integral scalar numerator of norm `5^n` would reduce to zero modulo five when possible, giving the required contradiction. This proves projective freeness for all reduced words.

The displayed rational matrices are the squares of two of these generators. A reduced word in the squares expands to a nontrivial reduced word in the original free group. If an element of this subgroup fixed the rational seed, it would commute with the third quaternion axis. Conjugating that third generator by a nonempty word in the first two produces a distinct reduced word, so the stabilizer is trivial.

The density argument is also adequate. Each generator has rational nonintegral trace, so its eigenvalues are not roots of unity; its powers are dense in the corresponding one-dimensional torus. The two torus directions and their bracket generate `su(2)`, forcing the closed generated subgroup to be `SU(2)`.

I found no fatal gap in these arguments.

### 3.4 Exact and robust profiles

The extreme-output theorem is correctly formulated pointwise at every cut. One fixed suffix is chosen for the cut; the corresponding affine action is injective. Extremality forces all positive-mass labels for a prefix to decode to the same terminal extreme point, and distinct prefix orbit points therefore have disjoint supports. Deterministic orbit storage attains all cut lower bounds simultaneously.

For the robust extension, the induced rational rotations have entries in `25^(-1) Z`, so cut-`t` reachable vectors lie on the `25^(-t)` lattice. The conditional decoder means lie in the Bloch ball. The displayed mean-square estimate implies the existence of a positive-mass label within radius `sqrt(2 sqrt(2) epsilon)` of each target. Under `epsilon <= 625^(-N)/16`, twice that radius is strictly smaller than `25^(-N)` and hence smaller than `25^(-t)` for every `t <= N`. The caps are disjoint and the exact profile remains necessary.

The constant calculation is conservative and consistent. The argument does not use the spectral-gap theorem.

### 3.5 Fixed-positive-error law

The fixed-positive-error lower bound imports Bourgain–Gamburd only after algebraicity and density of the displayed generators have been proved. Lazification supplies an absolute mean-zero `L^2` contraction. The upper bound is supplied constructively by the rational compiler and does not use the spectral gap.

The result is therefore honest but non-effective on the lower side: no numerical spectral-gap constant is obtained. The theorem should continue to display this limitation prominently.

### 3.6 Rational inner hull and compiler

The stereographic grid supplies a rational net of the sphere with support deficit at most `m^(-2)`, hence

```text
(1-m^(-2)) B_3 subset conv(V_m).
```

A point on a ray can be represented by the origin and at most three vertices of a triangulated supporting facet. Exhaustive triple enumeration and exact rational linear algebra therefore suffice. With `m^2 >= N/(1-beta)`, Bernoulli's inequality gives `r^N >= beta`, and the decoder Bloch vectors have norm at most one, so every decoder is a legal density matrix.

The dyadic rounding budget is also consistent. Each sparse row has at most four nonzero masses; rounding the first three downward and assigning the remainder to the last keeps stochasticity and support, with total-variation error at most `3*2^(-b)`. Stochastic contraction over `N` steps and the Frobenius diameter `sqrt(2)` of the qubit density matrices give the stated final error budget.

The checked command-line implementation is specialized to the displayed qubit alphabet, whereas the theorem is phrased for any fixed finite rational list of Bloch rotations. This is not a mathematical contradiction—the proof gives the general finite enumeration algorithm—but the implementation/documentation boundary should be stated more explicitly.

---

## 4. Correctness audit of the structural companion

### 4.1 Same-width stationarization

The proof first obtains a finite stationary obstruction by compactness and the finite intersection property. It then selects many narrow cuts and colors each pair by cells containing the actual return kernel and the actual command-plus-return kernels. A Ramsey-homogeneous clique supplies one approximate neutral table and one approximate table per command. Prefix, inter-block, and suffix physical returns make each test of the extracted stationary machine correspond to one genuine word of the original horizon.

The proof does not assume that hidden rows on return words are close to the identity. The neutral representative is absorbed into the terminal decoder and is not declared idempotent. The telescoping estimate uses only stochastic `l1` contraction. Arbitrarily wide intervening registers are allowed. This establishes the same label bound and the same closed numerical tolerance.

I continue to regard this argument as correct under the stated eventual-approximate-return hypothesis. That hypothesis is substantial: recurrence along a subsequence is not enough, and a one-letter irrational rotation is an explicit obstruction.

### 4.2 Stochastic purification

The compact joint closure of physical inverses and stochastic word products contains a minimum-rank idempotent over the physical identity. Its compact corner is a group. The stationary rows of the stochastic idempotent form a simplex whose vertices are the recurrent-class stationary distributions. The corner group acts by affine automorphisms and therefore permutes these vertices.

Projecting the initialization into this simplex and evaluating the old legal decoder on its vertices gives a permutation realization with no width or error increase. The empty word and nonempty words are treated through the same closed joint-semigroup inequalities. Randomized initialization remains allowed.

The subsequent kernel averaging over hidden permutations above the physical identity descends the action to a finite continuous physical-group action. This correctly separates physical relations from hidden relations in the original machine.

### 4.3 Finite quotients and boundary statements

A finite continuous physical action has an open normal kernel. Conversely, storing a seed and a coset of an open normal subgroup and decoding by a constrained center gives a finite realization. The legal output set remains part of the radius minimization. Equality at a critical radius is treated as an attainment question, not as an illegitimate limit from larger error.

I found no new structural defect introduced by the split presentation.

---

## 5. Reproducibility and evidentiary status

The committed package is unusually complete. The build receipt records ten rebuilt documents, exact source hashes, page-text and page-raster comparisons, a native-only isolated rebuild, the explicit rational compiler output, inherited regression suites, and more than thirty-seven thousand finite assertions. The finite checker contains named negative controls and explicitly refuses to interpret finite word enumeration as a proof of infinite freeness, a universal cap theorem, or a spectral gap.

These are strong reproducibility practices. They are not mathematical proof and are not independent priority clearance. At the exact reviewed publication SHA, the GitHub API returned no combined commit status and no workflow run whose head SHA is `27be4b...`. The committed receipt is consistent with the branch-producing workflow and the source/publication genealogy, but it is still an in-tree attestation rather than an externally visible final-head status check. A release-quality submission should expose an immutable successful workflow run or signed release/tag for the exact public head.

This evidentiary limitation does not create a mathematical counterexample. It only limits how strongly one may describe the final SHA as independently CI-qualified.

---

## 6. Why the top-four threshold is still not met

### 6.1 Specialized and permissive resource model

The primary invariant counts persistent hidden labels, not a conventional uniform computational resource. The horizon, external clock, construction and lookup of horizon-dependent tables, exact real arithmetic, and exact atomic sampling are outside the width measure. The manuscript is transparent about this, and the lower bounds are nontrivial even in this permissive model. Nevertheless, the model's specialization limits the breadth required for a leading general journal.

### 6.2 Strong recurrence hypothesis in the structural theorem

The clock-removal theorem requires approximate physical returns at every sufficiently large length. It is not a clock-removal theorem for arbitrary finite alphabets, arbitrary compact semigroups, or arbitrary controlled hidden-state systems. The hypothesis is natural in important examples, but it is not a minor technicality.

### 6.3 Quantitative non-sharpness

The lower law remains smaller than the upper law by a logarithmic factor. No matching constants or asymptotic equivalence are established. The lower constant depends on a deep imported spectral-gap theorem and is not computed even for the explicit rational pair.

Revision 58 correctly solves the class-wide cap-exponent problem, but it does not solve the main remaining quantitative sharpness problem.

### 6.4 Terminal-output scope

The theory concerns terminal convex-valued outputs. It does not classify online observations, adaptive queries, path laws, repeated sampled outputs, general operator-valued hidden memories, or irreversible physical semigroups. Those extensions have genuine consistency and causality constraints and cannot be inferred from the present theorems.

### 6.5 Priority remains author-audited, not independently settled

Many ingredients lie close to classical theories: compact stochastic semigroups, groups of nonnegative matrices, recurrent simplices, positive realization, probabilistic and weighted automata, neutral-letter/advice collapse, compact recognition, controlled hidden Markov realization, homogeneous-space entropy, and quantum/classical automata succinctness.

The manuscript is more careful than earlier revisions in identifying imported structure and isolating its new quantifiers. However, its literature file explicitly records a targeted author-side audit, incomplete access to some neighboring theorem texts, and no independent priority clearance. For a top-four recommendation, the exact theorem-level novelty boundary would need to be established much more decisively.

### 6.6 No repository-wide mathematical closure

The finite-dimensional realization results do not supply the raw local-limit, stopped large-deviation, global past-kernel, Mosco/Nisio, filtering, changing-filtration response, or labelled posterior-contraction gates in the repository's separate A/B/C/D analytic program. All aggregate closure flags remain false.

The local paper does not need that larger pipeline for correctness. Conversely, the existence of that larger pipeline cannot be used to raise the local paper's significance. The manuscript must stand on the two focused theorem packages alone.

### 6.7 No external major problem is resolved

The revision resolves several objections internal to its own development program, especially finite-input explicitness and all-direction cap verification. I do not see a consequence settling a recognized open problem of comparable visibility outside that program. Without such a consequence, the specialized model, unresolved logarithm, and unsettled priority boundary remain decisive at the four-journal level.

---

## 7. Required changes before specialist submission

1. **Submit the focused articles separately.** The quantitative and structural papers are now independently coherent. The complete preservation edition should remain archival and should not be presented as a third competing submission object.

2. **Obtain an independent theorem-level priority audit.** For each principal theorem, state the closest classical theorem, all changed hypotheses, and the exact strengthened quantifier or output object. The audit should be performed by someone not responsible for the manuscript's revision history.

3. **Keep the resource model on the first page.** The uncharged clock, horizon, table description, exact arithmetic, and exact sampling must remain visible. The finite compiler is a companion result, not a retroactive reinterpretation of the primary width measure.

4. **Keep the recurrence hypothesis in every structural headline.** “Clock removal” without “under eventual approximate returns” would be misleading.

5. **Do not suppress the logarithmic gap.** The lower and upper laws should be displayed together in the abstract and main theorem, as they are now.

6. **Separate effective from non-effective conclusions.** The explicit rational endpoint and compiler are effective; the spectral-gap lower constant is not. The rank invariant is computable only from supplied exact algebraic infinitesimal matrices.

7. **Clarify theorem versus CLI scope.** The theorem treats a supplied finite rational rotation list; the checked script hardcodes the displayed qubit experiment. Either generalize the interface or say explicitly that the script is the certified implementation of the principal example.

8. **Expose final-head CI evidence.** Publish a successful immutable workflow run for the exact final SHA, or a signed tag/release binding the native source, PDFs, receipt, and compiler output.

9. **Keep the wider Theta pipeline out of the novelty claim.** It may remain in a provenance appendix, but no aggregate progress or closure should be inferred from this paper.

10. **Tighten the specialist positioning.** The strongest sell is not a universal theory of memory. It is the combination of same-width stationarization under cofinal returns, finite physical actions for stationary stochastic realizations, least-orbit-rank width exponents, and one explicit rational exact/noisy separation with a constructive upper machine.

---

## 8. Detailed comments

1. The least-orbit theorem should state immediately that `p_*` is positive only because the group is connected and the representation has no nonzero fixed vector. The proof does this; the theorem's surrounding prose should make it just as prominent.

2. The phrase “optimal uniform exponent” is correct only for a constant uniform in `u,v,h` for the fixed representation. It should never be read as dimension-uniform or representation-uniform.

3. The quantifier-elimination proposition is a decidability statement, not a practical complexity result. Its wording should continue to avoid “efficient.”

4. The dense-generation proof for the rational pair should retain the rational-nonintegral-trace argument and the two torus directions; merely citing finite word growth would not suffice.

5. The exact profile depends on the legal decoder set being the density matrices. Enlarging the decoder set to an ambient vector ball or full categorical simplex changes the problem and may destroy extremality.

6. The robust profile is horizon dependent through `625^(-N)/16`. It does not state exponential width at one fixed positive error. The manuscript distinguishes this correctly and should preserve the distinction in all summaries.

7. The fixed-positive-error lower bound and exact/robust lower bound have different logical inputs. The former uses Bourgain–Gamburd; the latter does not. They should remain separated visually.

8. The compiler's zero vertex is a hidden label whose decoder is `I/2`; it is not a pure-state net point. The exposition handles this correctly.

9. The fair-bit count samples hidden transitions only. It is not a quantum-state preparation or terminal measurement algorithm.

10. The sparse-row search is polynomial in the number of explicitly enumerated net points and hence in the numerical horizon/inverse accuracy parameters. It is not polynomial in their bit lengths.

11. The structural stationarization theorem counts positive cuts; the initialization cut requires separate handling. The current proof does so through the prefix construction.

12. The neutral table in the Ramsey extraction is part of the decoder. It is neither the identity nor an idempotent. This warning remains necessary because it blocks an otherwise tempting but invalid shortcut.

13. The purification theorem preserves error balls, not the original machine's erroneous wordwise outputs. This is the right theorem and should remain explicit.

14. Randomized initialization can strictly reduce width. Therefore a deterministic-quotient index is an upper bound, not a formula for the unrestricted stationary minimum.

15. The finite-quotient boundary uses centers constrained to the legal output set. An unconstrained ambient Chebyshev radius would define a different invariant.

16. The build and regression suite should not be described as certifying infinite freeness or the universal cap theorem. The current files avoid this error.

17. The final publication commit is unsigned. For a package whose evidentiary architecture is unusually elaborate, signing the release would materially improve provenance.

18. The author-side literature table is useful and should be retained, but its disclaimers are substantive, not boilerplate. In particular, the HMM/controlled-realization comparison remains incomplete.

---

## 9. Final assessment

Revision 58 successfully answers the main mathematical criticisms of r38 that were answerable within the current program:

- the all-direction cap condition is derived from a computable rank invariant for fixed representations;
- the exact exponential endpoint is a fixed rational finite input;
- the exact profile persists on a nonzero, explicitly quantified error interval;
- the positive upper realization is constructed by a rational compiler; and
- the article has been split into two independent focused papers without deleting the historical mathematics.

I found no fatal gap in these new theorem chains or in the inherited structural core that I rechecked. The work has therefore reached the level of a serious specialist contribution.

It has **not** reached the Annals / Inventiones / JAMS / Acta threshold. The model remains specialized, the structural theorem retains a strong return hypothesis, the nonabelian law retains a logarithmic and non-effective gap, the output scope is terminal, the independent priority boundary remains unsettled, and the broader repository pipeline is explicitly open and mathematically separate.

**Recommendation: reject at the four leading general mathematics journals; encourage separate, substantially tightened submissions to strong specialist venues after independent priority review.**
