# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r29-causal-energy-2026-10-10`  
**Reviewed exact branch head:** `09eda58be2297ce885c7f2b4447f24fec3a0c9b4`  
**Reviewed branch root tree:** `1f06829c5f233ade703eff445ac1b046603683d0`  
**Ordinary mathematical-source commit:** `31d06e6f21ccfe072016a7f0c9d39aeee4f6836f`  
**Native directory tree:** `7110d104216f244ab7521716015a21953634d7ef`  
**Ordinary mathematical-text projection:** `8e7a5a5ba3cb01124005a3c7a032197759a88e66`  
**Hosted artifact commit:** `ecdd25b0d87fba16cbc92675a6ba68866d166887`  
**Native PDF SHA-256:** `0c0173f8dcbbe9bf284c5c35c4f28c06ee4e3090969d17802f7b1d0eab60bc83`  
**Native article length:** 20 pages  
**Complete corrected Companion F:** 31 pages  
**Complete deposited packet:** thirteen PDFs, 352 pages  
**Predecessor external report:** R27 review head `00cad841267ee714f20d71ca9734dc5d4014ee4f`, report blob `79c032f1bd1697722d44206dfb28f48b1cdf2311`  
**Intervening research-only intake:** R28 head `37826ed38311e247874c35674e668855402ed6ff`  
**Review branch:** `review/general-theta-restart-r29-causal-energy-external-top4-referee-r29-2026-10-10`  
**Date:** 10 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision R29 is a genuine and substantial mathematical advance over R27 and is, in my assessment, the strongest finite-horizon spatial result in the restart sequence. It introduces a clean causal obstruction that is different from the temporal occupation modulus of R27: even when every raw report has a state-independent law, the full-history predictive update is an isometry, and the acquired marginal law is unchanged from one stage to the next, a finite observer can lose predictive energy at every update because it must both quantize each incoming row and pool incompatible predecessor centroids into one outgoing label.

The central theorem is mathematically coherent. It proves an exact identity

```text
e_t = kappa_t e_(t-1) - D_row - D_pool,
```

where `D_row` is the ordinary within-row conditional quantization loss and `D_pool` is the additional loss caused by merging conditional centroids from different predecessor labels. This identity yields a lower bound against every legal Borel randomized observer, not merely against a selected recursive quantizer. It also gives the correct local equality criterion: every positive-energy incoming row must attain the extremal one-step quantization coefficient, and all incoming centroids assigned to the same outgoing label must agree.

The exact circle theorem is particularly effective. The static circle coefficient

```text
beta_m = (sin(pi/m)/(pi/m))^2
```

is combined with an explicit centroid-compatible recursive encoder to give the exact sequential value

```text
B + 1 - product_t beta_(m_t).
```

When the deadline must be represented internally, all reachable phases are proved disjoint under the common Haar report law. If `M-1=nq+r`, `0<=r<n`, the complete autonomous optimum is therefore

```text
B + 1 - beta_q^(n-r) beta_(q+1)^r,
```

with feasibility exactly when `M>=n+1`. This is a real total-state resource theorem, not a checkpoint quantization statement with an uncharged clock.

The higher-dimensional orbit and quantum arguments are also nontrivial. The lower bound is uniform over every normalized incoming conditional mean, rather than only over the prepared pure-state orbit. In the projective quantum realization, a spectral-gap argument selects a Grassmannian coordinate of dimension at least `2(D-1)`, while the pure-state orbit supplies the matching global cover and one-dimensional stabilizer-fixed subspace. The resulting exponent is the intrinsic orbit dimension `2(D-1)`, not the ambient traceless-matrix dimension `D^2-1`.

In the load-bearing arguments checked, I did not find an elementary gap invalidating:

- the raw finite-test transport identity under state-independent report laws;
- the two-stage conditional-square decomposition into row and pooling losses;
- the all-Borel row-quantization lower bound;
- the local necessary-and-sufficient centroid-compatibility condition for saturation;
- the product lower on retained predictive energy;
- the homogeneous-orbit lower from a mass estimate uniform over all incoming directions;
- the stabilizer-averaging correlation recursion used for the causal upper;
- the spherical small-ball and global-cover estimates;
- the exact static circle quantization formula, including randomized fractional cells;
- the exact recursive circle product;
- the disjoint-phase lower for an internally enforced deadline;
- the balanced integer allocation and exact total-state circle law;
- the surviving-stratum lower and upper with its actual mass and inactive labels;
- the classical word-transport realization;
- the noncommuting qubit realization and its hidden-report rank change;
- the uniform higher-dimensional conjugacy-orbit mass lemma;
- the projective quantum acquired-dimension conclusion;
- the paid fixed-start gated-test transfer of the inherited marked obstruction;
- the corrected physical-crossing convention in Companion F;
- the product-state causal simulator accounting;
- the finite-precision circle construction at the level at which it is stated;
- the protected-audit disclosure-deficiency lower and stateless Haar-fill upper; or
- the source, artifact, and independent-reconstruction claims at the level at which they are stated.

The negative top-four judgment concerns the **breadth, intrinsic reach, relation to the mature sequential-quantization literature, and external mathematical impact of the advance**, rather than an identified fatal proof defect.

The general energy identity assumes a finite-dimensional executable test space, a report law independent of the entering physical state and all prior reports, and a linear pullback of the predictive coordinates. These assumptions are transparent and verified in the raw examples, but they exclude the principal difficulty of nonlinear filtering and partially observed control: state-dependent likelihoods. The exact product and total-state formulas then rely on Haar symmetry, global homogeneous covers, and in the exact case the special centroid structure of regular circle arcs.

The paper has therefore established a sharp theorem for a nontrivial and well-typed class of **relative-report tracking experiments**. It has not yet produced a necessary-and-sufficient theory of recursive causal compression, a broad theorem for noisy state-dependent observations, or a resolution of a recognized difficult natural problem in zero-delay coding, POMDPs, robust filtering, quantum control, or information theory. The examples validate the mechanism convincingly, but are built to realize the symmetry and conditional-centroid structure needed by the theorem.

For a strong specialist journal in information theory, stochastic control, quantization, real-time coding, mathematical statistics, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance, and pipeline inspected

A fresh two-page enumeration immediately before this report identified

```text
referee-ready/general-theta-restart-r29-causal-energy-2026-10-10
```

as the latest completed `General Theta Foundations I` referee-ready branch. The continuation page was empty. A separate two-page review-branch enumeration found external reports only through R27; no R28 or R29 report was present.

The exact object reviewed is the evidence-only terminal head

```text
09eda58be2297ce885c7f2b4447f24fec3a0c9b4.
```

Its sole parent is the artifact commit

```text
ecdd25b0d87fba16cbc92675a6ba68866d166887,
```

which is the direct child of ordinary mathematical source

```text
31d06e6f21ccfe072016a7f0c9d39aeee4f6836f.
```

The native directory tree is

```text
7110d104216f244ab7521716015a21953634d7ef,
```

and the ordinary mathematical-text projection, excluding review inputs and generated evidence, is

```text
8e7a5a5ba3cb01124005a3c7a032197759a88e66.
```

I reviewed the native article and its derivation and delivery pipeline, rather than treating the 352-page packet as one undifferentiated manuscript. The inspection included:

- `main.tex`, all ten native section files, and `references.tex`;
- `README.md`, `SUBMISSION_GUIDE.md`, `REFEREE_RESPONSE.md`, `REFEREE_COMMENT_CONCORDANCE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, `PINNED_INPUTS.md`, and `RETAINED_PATCHES.json`;
- the canonical restart charter, foundational outline, theorem targets, and realization-registry boundary;
- the complete R27 external report and the R29 point-by-point response;
- the R28 intake's stated status as research-only provenance;
- the complete corrected Companion F and its crossing-index repair;
- the ordinary source manifest, verification and regression programs, build programs, source-publication record, independent-rebuild record, read-only verification, final scope record, and referee packet;
- the relation among corrected Companion F and unchanged E/D/C/B/A/X/W/V/U/T/S; and
- a targeted comparison with static and recursive quantization, finite-state vector quantization, optimal sequential vector quantization, zero-delay Markov coding, nonanticipative rate-distortion theory, long-run finite-memory POMDPs, and the earlier marked Poisson/occupation theory.

The native article is 20 pages. Corrected Companion F is 31 pages. The eleven unchanged older companions contain 301 pages. The complete packet therefore contains thirteen PDFs and 352 pages. Editorial assessment should be based primarily on the 20-page native article; the companions serve as mathematical history and provenance, not as hidden premises of the new energy theorem.

The native source audit records 48 ordinary files plus its manifest, 12 active TeX inputs, 68 labels, 55 cross-references, 13 bibliography entries, and 22 formal statements, each with a written proof. Companion F retains all 103 mathematical labels from R27 after the explicit crossing-convention correction.

The independent reconstruction used the actual downloaded remote source export and compared it with the actual hosted artifact. It reports 682 immutable source inputs, 34 isolated PDF builds in each TeX environment, three passes per technical rebuild, 18,875 native finite checks, and successful ordinary/optimized regression parity. All thirteen PDFs have matching page counts, normalized text, and RGB rendering across TeX Live 2023 and 2025 for all 352 pages. Raw PDF bytes differ across engines; repeated builds within each environment are byte-identical.

These controls are useful source-integrity, finite-arithmetic, and reproducibility evidence. They are not proofs of the continuum statements, priority, or journal significance. I did not independently re-referee every theorem in the historical companions, every v1--v96 branch, or every separate realization branch.

---

## 2. Executive assessment of Revision R29

R29 changes the center of the paper from a temporal Markov-renewal obstruction to a spatial and recursive finite-memory obstruction.

The R27 theorem compared a marked Poisson residual--oscillation functional with physical-prefix discrepancies. R29 preserves that result in corrected Companion F, but its native theorem does not use regeneration, group inverses, or physical return tails. It instead considers a finite-dimensional family of executable predictive tests transported by reports whose law is independent of the hidden predictive point.

For a finite-state observer, let

```text
v_(t,s) = E[p_t | S_t=s],
e_t = E ||v_(t,S_t)||^2.
```

Given predecessor label `s`, the raw transported old mean is

```text
W_s = A_t(Y_t) v_(t-1,s).
```

The observer first compresses this row through its report-dependent update and then pools the resulting rowwise centroids whenever several predecessor states use the same outgoing label. The manuscript proves that these are exactly the only two energy losses.

This formulation isolates a genuine causal issue. The actual marginal law of `p_t` can be the same at every stage. A checkpoint with access to the entire report history can quantize that law once. A recursive observer, however, sees the current relative transformation only through its old finite label and must update that label without a real-valued posterior register. Repeated compression therefore accumulates.

The paper then obtains three levels of consequence:

1. an exact all-observer lower and local saturation criterion for general state-independent linear test transport;
2. matching rates for homogeneous compact-group orbits; and
3. an exact circle law, including the entire internal deadline state budget.

The native article is consequently more concentrated than several earlier revisions. Its central mechanism, exact model, and resource comparison are visible within 20 pages.

---

## 3. Response to the R27 external report

R29 is not a cosmetic revision. It addresses several of the strongest R27 objections with new mathematics.

| R27 issue | R29 assessment |
|---|---|
| The paper lacked a broad nonreset obstruction outside marked regeneration | **Resolved for a distinct finite-horizon relative-transport class.** No regeneration or observer reset is used in the energy theorem. |
| The previous signed all-row lower did not automatically apply from one prescribed start | **Resolved only with the correct qualification.** Proposition `prop:access` adds a paid tagged initialization and a gated test; scalar cancellation remains explicitly possible. |
| The crossing index had an off-by-one error | **Resolved.** `lem:crossing-new` distinguishes `C_N<=N` from the older shifted `K_N=C_N+1<=N+1`; Companion F applies the correction. |
| Spatial matching relied on strong supplied cover/stability data | **Improved in a raw homogeneous class.** Haar instruments supply actual mass, isometric updates, report continuity, global covers, and a stabilizer certificate. |
| A finite-memory theorem should charge an internal deadline | **Resolved exactly on the circle and to sharp order on spheres/orbits.** Reachable phases are disjoint and balanced allocation is proved optimal. |
| A natural quantum verification was requested | **Improved substantially.** The projective orbit has intrinsic dimension `2(D-1)` and the lower is uniform over mixed incoming means. |
| The paper needed a substantive non-temporal consequence | **Resolved.** Identical acquired marginals have different checkpoint and causal resource curves. |
| General computational synthesis remained exhaustive | **Improved only in the circle allocation.** One division solves the phase widths, but compiling the full finite machine and obtaining matched bit/time lower bounds remain open. |
| A recognized difficult external problem was still absent | **Not resolved.** The examples establish a designed relative-transport class rather than settling a standard open problem. |
| The breadth implied by “Foundations” remained larger than the proved class | **Still unresolved.** The native abstract is scoped, but the title continues to suggest a more intrinsic general classification. |

The preceding report asked for a theorem whose content was not merely another compactness or finite-enumeration layer. R29 provides one. The remaining question is whether the theorem's highly symmetric information interface has enough intrinsic reach and external consequence for a top-four general journal.

---

## 4. Audit of the raw experiment and information pattern

### 4.1 State-independent reports are a central hypothesis

The report law at stage `t` is a prescribed probability `lambda_t`, independent of the entering physical state and of all earlier reports. On the selected centered test coordinates,

```text
p_t = A_t(Y_t) p_(t-1),
```

and

```text
integral A_t(y)^T A_t(y) lambda_t(dy) = kappa_t I.
```

This is stronger than report continuity or domination. It is the reason the current report is independent of the hidden old predictive vector conditional on the old observer label. A state-dependent likelihood would generally require a normalized Bayesian update and does not fall under this identity.

The manuscript states this boundary honestly in Sections 2 and 10. It should remain prominent in the theorem heading and abstract, because it determines both the proof and the range of applications.

### 4.2 The observer class is correctly typed

At a sequentially scheduled stage, the observer has at most `m_t` labels, an old label, the current report, and fresh update randomness. It has no persistent seed, real posterior register, history tape, or free response wire. In the autonomous model, one reused row and one finite label set must also represent the internal deadline.

The terminal audit occurs only after the answer has been committed. It is not feedback and cannot be used to update the machine. This timing is maintained in the classical, quantum, singular, and simulator constructions.

### 4.3 The finite test space is a task quotient, not the full physical state

The predictive coordinates arise from a finite family of executable future tests closed under the declared report instruments. The quotient lemma requires a standard-Borel image and a Borel section. In the raw orbit examples these conditions are verified.

The result therefore concerns the full quotient of the **declared one-audit future experiment**, or a declared task factor when other physical tests are explicitly excluded. It does not imply that an arbitrary workload, density matrix, or nonlinear physical state has the same finite-dimensional predictive quotient.

This distinction is correctly stated. It should be repeated near every application where a reader might otherwise interpret the sphere or projective coordinate as the full physical state space.

---

## 5. Audit of the causal energy theorem

### 5.1 The exact identity

For an old label `s`, set

```text
W_s = A_t(Y_t) v_(t-1,s).
```

Because the report is independent of the past and the new label depends only on the old label, current report, and fresh update randomness,

```text
E[p_t | S_(t-1),Y_t,S_t]
 = A_t(Y_t) v_(t-1,S_(t-1)).
```

Taking conditional expectations first onto `(S_(t-1),S_t)` and then onto `S_t` gives the row centroids `c_(s,j)` and outgoing centroids `v_(t,j)`. Two applications of the Pythagorean identity for conditional expectation give

```text
kappa_t e_(t-1)
 = D_row + D_pool + e_t.
```

This derivation is correct. It uses neither a hidden independence between duration and exit nor a normalized filtering approximation.

### 5.2 Row loss versus pooling loss

`D_row` measures the distortion of encoding the random transported mean within each predecessor row. `D_pool` measures the variance of the rowwise centroids around their common outgoing-label mean.

The pooling term is not cosmetic. Two predecessor rows can each use an optimal local quantizer and still lose additional energy when they assign different centroids to the same outgoing label. The counterexample ledger correctly records this failure mode.

This is the clearest conceptual contribution of the paper. The manuscript should make it even more prominent that the identity is a finite-state analogue of a compatibility constraint between locally optimal quantizers, not merely a repeated application of static quantization.

### 5.3 Quantization lower and product bound

For every nonzero entering mean, the law of `A_t(Y_t)v` scales quadratically in `||v||`. Static squared quantization bounds the row loss by

```text
kappa_t eta_t(m_t) ||v||^2.
```

Summing over rows and discarding the nonnegative pooling term gives

```text
e_n <= e_0 product_t kappa_t(1-eta_t(m_t)).
```

Zero entering means are handled without division. The manuscript also correctly declines to infer earlier-stage equality from a later zero product factor.

### 5.4 Equality criterion

For a nonzero one-step bound, equality requires:

1. every positive-mass, positive-energy incoming direction to attain the infimum defining `eta_t(m_t)`;
2. each row encoder to attain its corresponding static `q_m`; and
3. the centroids from all predecessor rows using a common outgoing label to agree.

Because all losses are nonnegative, these conditions are necessary and sufficient locally. Successive rows satisfying them attain the full product.

The logical statement is correct. The exposition should distinguish more sharply between:

- this exact **local saturation criterion**; and
- the separate existence of a globally compatible recursive construction.

The circle supplies exact existence. General homogeneous orbits supply a matching-rate construction, but not exact product saturation. The manuscript eventually says this; placing the distinction directly after Theorem `thm:energy` would reduce the risk of overreading.

---

## 6. Homogeneous orbit law

### 6.1 Uniform lower over all incoming means

A lower based only on the prepared orbit would be insufficient: conditional means carried by observer labels can lie inside the convex hull and need not be pure orbit points.

Theorem `thm:homogeneous` therefore assumes a small-ball estimate for `gv` uniformly over every unit vector `v` in the centered test space. This yields

```text
q_m(Law(gv)) >= c m^(-2/d)
```

for every normalized incoming mean direction. The energy theorem then gives the all-observer product lower.

This quantifier is correct and load-bearing.

### 6.2 Stabilizer averaging and causal upper

The upper stores one orbit codepoint. Conditional on `g xhat = u`, Haar disintegration over the stabilizer of `xhat` gives

```text
E[g x | g xhat = u] = <x,xhat> u
```

when the stabilizer-fixed subspace is exactly the line through `xhat`. A global nearest-direction cover therefore multiplies the expected true/estimated correlation by a coefficient `kappa_m` at each stage.

The legal final response scales the last stored direction by the precomputed product of these coefficients. Its excess is `1-product kappa_m^2`, which has the required sum-of-scales upper.

The construction stores only a finite codepoint label. The scalar product is a program constant used by the terminal readout, not an evolving uncharged real register.

### 6.3 Scope of the homogeneous theorem

The theorem is broad within compact homogeneous orbits, but its primitive assumptions are substantial:

- Haar or an equivalent invariant report law;
- no fixed centered vector;
- a stabilizer-fixed line;
- a uniform small-ball exponent for all incoming directions; and
- a matching global cover of the prepared orbit.

The article would benefit from one non-Haar or nontransitive example where these assumptions are verified in a less symmetric way. Without such an example, the theorem's apparent abstraction is driven largely by representation-theoretic symmetry.

---

## 7. Exact circle theorem

### 7.1 Static quantization with randomized cells

The proof of

```text
q_m(sigma_1)=1-beta_m
```

correctly allows fractional memberships. For a cell of mass `p`, rearrangement bounds its first moment by `sin(pi p)/pi`. The manuscript then maximizes the sum of retained energies by reducing any cell larger than one half and applying concavity on `[0,1/2]`. Equal arcs attain the bound.

This is the correct Euclidean chordal squared-loss formula with centroids in the disk. It is not a geodesic formula or a codebook constrained to the circle.

### 7.2 Exact compatible recursion

Regular arcs give every predecessor row the same outgoing-label probabilities and the same conditional centroid for a given outgoing arc. Thus every row is statically optimal and `D_pool=0`.

Induction gives retained conditional-mean radius

```text
product_t sin(pi/m_t)/(pi/m_t),
```

and hence the exact risk product. This establishes equality over the full Borel randomized observer class because the lower came from the energy theorem.

### 7.3 Internal deadline

With a time-homogeneous reused label row and iid Haar reports, the future stopping-time law conditional on a label is the same every time that label is reached. A nonhalt label therefore cannot occur at two different phases of a deterministic exact deadline. Halt labels occur only at the final phase. The positive-probability label sets at phases `0,...,n` are disjoint.

The budget

```text
1 + sum_t m_t <= M
```

is therefore valid. If the initial distribution uses several positive-probability states, the stronger count only helps the lower.

The singular autonomous extension correctly weakens “identical laws” to a common positive-path support condition through mutually equivalent phase report laws. This support-level argument should be stated as a short standalone lemma, because equivalence preserves possible transition paths but not their probabilities.

### 7.4 Balanced allocation

The strict concavity of

```text
2 log(sin(pi/x)/(pi/x))
```

for `x>1` implies that any two positive integer widths differing by at least two can be balanced to increase the product. Width one has coefficient zero, which correctly produces the saturated range.

The quotient/remainder formula and feasibility threshold follow. This is a rare part of the manuscript where the synthesis problem is solved exactly rather than by enumeration.

---

## 8. Singular reports and actual mass

A hidden report leaves the physical transform in place but makes its conditional Haar average zero. Once this occurs, later visible orthogonal transforms preserve the zero mean. The actual full-history predictive law is therefore

```text
w_n mu + (1-w_n) delta_0,
```

not a normalized copy of `mu`.

The full-history baseline rises from `V-1` to `V-w_n`. The sequential lower keeps the factor `w_n`; the upper reserves an inactive label in every phase and uses active orbit codepoints only on the surviving event. The autonomous state count includes those inactive labels.

These calculations are correct and preserve the actual singular mass. The manuscript also correctly warns that a deterministic visible suppression pattern can act as an external phase clock and invalidate the autonomous clock lower.

---

## 9. Raw classical and quantum realizations

### 9.1 Classical word transport

The raw physical state is the entire finite word of rotations. A report appends and reveals only the new Haar rotation. The declared future audit queries one coordinate of the current direction after the answer has been committed.

The finite coordinate tests separate points on the sphere and close under reported rotations. Their conditional predictions are exactly the current direction. Thus the sphere is a realized quotient of the declared future experiment, even though the raw word state is not finite-dimensional.

This is a legitimate raw realization rather than a postulated sphere-valued Markov chain. Its limitation is equally clear: adding richer nonlinear future observations changes the quotient.

### 9.2 Qubit instrument

The reported instrument

```text
rho -> U rho U* h(dU)
```

has a state-independent Haar report law and rotates the Bloch coordinate orthogonally. The Pauli audit queries one effect at a time; it does not assume a joint measurement of incompatible observables. Nonparallel states do not commute.

The hidden-report branch is Haar twirling, which gives the actual maximally mixed conditional state. For pure preparation, the rank therefore changes from one to two with the displayed surviving mass.

The observer remains classical. The physical qubit is the predicted experiment, not free quantum memory.

### 9.3 Higher-dimensional projective orbit

The proof must control the orbit of every possible normalized conditional mean, including mixed spectra and repeated eigenvalues. The manuscript obtains a uniform adjacent eigengap from zero trace and unit Hilbert--Schmidt norm. Closeness of two conjugates controls the corresponding top spectral projections. Haar measure on the relevant Grassmannian has local dimension `2j(D-j)`, which is at least `2(D-1)`.

Since only finitely many ranks can realize the selected gap, the constants can be chosen uniformly. The pure-state orbit itself has dimension `2(D-1)`, provides the matching cover, and has a stabilizer-fixed line in the centered traceless space.

This closes the most important quantifier in the projective lower. The proof does not assume a uniform simple spectrum.

For readability, the eigengap and projector inequalities should be extracted into a separate lemma with all constants and norms displayed before the chart calculation. The present proof is correct but compressed.

### 9.4 Audit effects and normalization

An orthonormal Hilbert--Schmidt basis element has operator norm at most one, so the effects `(I±F_i)/2` are positive. Randomly selecting one basis direction and rescaling its sign yields the centered coordinate expectation. The query index and outcome are generated only at the audit after response commitment.

These details are present, but should be stated in the theorem rather than left partly to the proof, because they are essential to the operational quantum interpretation.

---

## 10. Fixed-start accessibility and inherited correction

### 10.1 Observable gated access

The old marked dual concerns a supremum over entering rows. R29 does not silently turn it into a scalar lower from one initial law.

Instead a paid, parameter-independent initialization emits a visible row tag with every row having probability at least `a`. The test family then includes row-gated raw scores. Disintegration transfers the all-row discrepancy to this accessible test family, paying the initialization calls and the factor `a`.

The unknown gain, model, and dual vector remain analytical. Runtime gates only the observable raw score.

This is the correct fixed-start statement. The periodic two-row example correctly shows that an ungated scalar risk can cancel even when both rows are accessible.

### 10.2 Crossing convention

R29 repairs the concrete R27 indexing error:

```text
T_0=0,
T_j=sum_(ell=1)^j tau_ell,
C_N=min{j>=1:T_j>=N},
C_N<=N.
```

In the old shifted convention

```text
S_k=T_(k-1),
K_N=min{k>=1:S_k>=N},
```

one has

```text
K_N=C_N+1<=N+1,
```

while the number of summands with `k<K_N` is at most `N`.

Companion F consistently uses predictable starts `T_(j-1)<N`. The repaired estimates are unchanged. This fully resolves the issue identified in the R27 report.

---

## 11. Composition, finite precision, and deficiency

### 11.1 Causal simulator accounting

A simulator with `S` labels and an observer with `M` labels uses the product state of size at most `MS`. Reports must be emitted before the target decisions that use them. The physical audit remains environment-owned.

A forward simulator supplies only a forward risk comparison. A reverse inequality requires a reverse task-compatible simulator. Call counts, physical time, program description, workspace, and precision remain distinct from persistent labels.

### 11.2 Finite-bit circle implementation

The finite-precision proof couples exact and rounded programs using the same real reports. Until the first state mismatch, the exact next angle is uniform conditional on the current label, so the probability of crossing a rounded boundary is controlled by total boundary length.

The resulting bound is on decision mismatch probability and readout error. It does not claim total-variation closeness between a continuous report and a discrete approximation.

The stated program, workspace, and schoolbook-arithmetic upper counts are plausible and correctly identified as upper bounds. They are not matched computational lower bounds.

### 11.3 Protected-audit disclosure deficiency

The simulator may replace hidden reports by fresh Haar draws, giving discrepancy at most `1-w_n`. For the lower, the statistic formed from the simulated accumulated direction and the later physical audit has an expectation gap proportional to `1-w_n`. On a hidden-transform history, the physical predictive coordinate is zero conditional on all information available to the simulator before the audit.

This lower applies even with arbitrary classical simulator memory. It relies essentially on the protected physical audit and report deadlines. An unrestricted comparison allowing replacement of the audit would be different.

The final common-task law therefore uses an attained physical deficiency, not an arbitrary permitted error tolerance promoted to an unavoidable loss.

---

## 12. Literature position and novelty

The native bibliography correctly credits static quantization, exact circle quantization, zero-delay coding of Markov sources, long-run finite-memory POMDP theory, strategic measures, and the older marked Poisson/ergodic tools.

The comparison should nevertheless be expanded in four directions.

### 12.1 Optimal sequential vector quantization

Borkar, Mitter, and Tatikonda, *Optimal Sequential Vector Quantization of Markov Sources*, SIAM Journal on Control and Optimization 40 (2001), 135--148, formulates sequential vector quantization of a Markov source as a partially observed stochastic control problem and characterizes optimal schemes.

R29 differs because the machine does **not** observe the current source point. It receives only a relative transformation report and its counted old label. Nevertheless, this paper is a direct methodological neighbor and should be discussed explicitly.

### 12.2 Classical finite-state vector quantization

Foster, Gray, and Dunham, *Finite-state vector quantization for waveform coding*, IEEE Transactions on Information Theory 31 (1985), 348--359, treats a finite-state quantizer whose current state selects a codebook and whose selected codeword determines the next state.

R29's pooling compatibility can be presented as a theorem-level obstruction for a special relative-observation finite-state quantizer. The historical finite-state-vector-quantization literature should not be represented only through modern zero-delay Markov coding.

### 12.3 Recursive quantization

Pagès and Sagna's recursive marginal quantization work, including *Recursive marginal quantization of the Euler scheme of a diffusion process* and the later general weak/strong error analysis, studies accumulation of local quantization errors under recursively quantized Markov dynamics.

Their object and comparison class differ from R29's all-observer converse and pooling defect, but the conceptual proximity is close enough that the distinction should be made theorem by theorem.

### 12.4 Nonanticipative and sequential rate-distortion theory

Nonanticipative rate-distortion and sequential rate-distortion theory provide causal lower bounds, finite-horizon allocations, and filtering realizations for Markov and partially observed Gaussian sources. Relevant work includes Stavrou, Kourtellaris, and Charalambous on nonanticipative RDF; Stavrou, Charalambous, Charalambous, and Loyka on finite-horizon causal filtering; and Tanaka, Kim, Parrilo, and Mitter on Gaussian sequential rate-distortion tradeoffs.

These theories charge information rate rather than a hard finite label alphabet and generally assume a different observation interface. They do not obviously contain R29's exact finite-state relative-Haar law. They nevertheless form an essential adjacent lower-bound tradition.

A very recent 2026 preprint on sequential lossy compression under a causal conditional-perception constraint is also adjacent at the level of stagewise causal reconstruction laws, although it does not appear to study the fixed-label relative-transform problem.

### 12.5 Novelty that can reasonably be claimed

A targeted search did not locate an existing theorem with the exact combination:

- only relative Haar transformations are reported;
- the absolute predictive point is never observed;
- the complete persistent label budget is fixed;
- all Borel randomized update rules are covered;
- pooling of predecessor centroids is isolated exactly; and
- an internally represented deterministic deadline is optimized exactly.

This is not an independent priority certificate. It does support a narrower novelty claim: the recursive pooling obstruction and exact circle deadline law for this observation interface appear materially different from standard current-source zero-delay quantization.

The paper should avoid broader formulations suggesting that conditional variance, recursive quantization, or finite-state coding itself is new.

---

## 13. Why the present paper does not meet the top-four threshold

### 13.1 The general theorem remains tied to a narrow observation channel

State-independent reports are not a minor regularity condition. They remove Bayesian normalization and make the current report independent of the hidden old predictive point. The energy identity then becomes exact and linear.

This class is mathematically nontrivial, but most difficult filtering and partially observed control problems have state-dependent observation laws. An extension that replaces state independence with a quantitative likelihood geometry would substantially change the paper's reach.

### 13.2 Exact sharpness relies on high symmetry

The exact result is on the circle. Higher-dimensional spheres and projective orbits are matched only to constants. Both lower and upper exploit Haar invariance, homogeneous mass, and stabilizer averaging.

A nonhomogeneous example with a genuinely varying report geometry would show that the pooling mechanism is not primarily an artifact of compact-group symmetry.

### 13.3 No recognized difficult natural problem is resolved

The classical and quantum instruments are valid raw experiments, not mere coordinate examples. However, they are constructed to realize the theorem. The paper does not derive a new limit for a standard physical communication protocol, solve a previously open zero-delay coding problem, or change a known POMDP/quantum-control classification.

This is the principal remaining significance obstacle.

### 13.4 The title remains substantially broader than the proved classification

“General Theta Foundations I” suggests an intrinsic framework for causal acquired geometry across broad experiments. The native article proves a precise theorem for finite test transport with state-independent reports, and a sharp homogeneous subclass.

The abstract is reasonably scoped, but the title and framing still create an expectation of a more general classification than the paper supplies.

### 13.5 Computational optimality is only partially addressed

The circle phase allocation is solved by integer division. The finite-bit construction gives explicit upper resources. The paper does not prove lower bounds for program length, workspace, report precision, arithmetic time, or simulator state, and it does not give efficient synthesis for general raw kernels.

The result should be presented as an exact statistical/persistent-state theorem with a certified implementation upper, not a complete computational resource theory.

---

## 14. Major revision requests

### 14.1 Isolate the central theorem and observation interface

The introduction should state, in one compact theorem box, that the new general result requires:

- a finite executable centered test space;
- state-independent current report laws;
- linear test pullbacks;
- finite observer labels; and
- squared terminal loss.

Readers should not need to infer from Section 2 that state independence is the decisive structural condition.

### 14.2 Separate three notions of “compatibility”

The revision should explicitly distinguish:

1. static row optimality;
2. zero pooling defect for a chosen outgoing labeling; and
3. existence of a globally compatible sequence of labelings across all stages.

Theorem `thm:energy` characterizes the first two locally. Circle arcs establish the third exactly. General homogeneous covers establish only a matching-rate construction.

### 14.3 Add theorem-level comparison with sequential and finite-state quantization

The literature section should compare R29 with:

- Borkar--Mitter--Tatikonda sequential vector quantization;
- Foster--Gray--Dunham finite-state vector quantization;
- recursive marginal quantization; and
- nonanticipative/sequential rate-distortion theory.

The comparison should list source observation, memory object, horizon, distortion criterion, and whether the conclusion is existence, dynamic programming, information-rate lower, or exact hard-state formula.

### 14.4 Provide a less symmetric application or an obstruction theorem

A materially stronger article would either:

- verify the energy/pooling mechanism for a non-Haar, nontransitive report family; or
- prove a counterexample showing that no comparable product theorem can hold under general state-dependent likelihoods without an additional term.

Either result would clarify the conceptual boundary of the method.

### 14.5 Strengthen the operational significance

The manuscript should connect the exact circle law to a recognizable real-time estimation/coding protocol in which only relative transformations are physically available. The present classical word and quantum orbit experiments are mathematically valid, but remain largely theorem-realizing constructions.

### 14.6 Clarify the status of the projective quantum theorem

The theorem should state directly that:

- the observer is classical;
- the physical system is not memory available to the observer;
- one audit basis element is selected after commitment;
- the exponent is an orbit-dimension result for the declared linear test family; and
- exact higher-dimensional product saturation is not proved.

### 14.7 Extract the uniform conjugacy-orbit lemma

The eigengap, spectral-projection, and Grassmannian-mass argument should be made more modular. Its uniformity over repeated eigenvalues is one of the stronger technical parts of the article and deserves a standalone presentation.

### 14.8 Make sequential and autonomous results visually distinct

The sequential model has an external phase schedule and phase-dependent rows. The autonomous model must encode the phase in its labels. These are different resource classes.

A one-page table should compare their legal information, label accounting, and exact conclusions.

### 14.9 Keep the inherited temporal theory editorially separate

Corrected Companion F is useful and should remain available. The native R29 paper should not rely on the reader treating the 352-page packet as one submission. The 20-page native article is the appropriate editorial object.

### 14.10 Reframe the title or justify its breadth

If the title is retained for programmatic reasons, the introduction should state explicitly that this article proves one foundational mechanism—recursive compatibility for a finite test transport class—rather than a complete foundation for all causal acquired geometry.

### 14.11 Distinguish exact mathematical implementation from bit execution

The exact Borel machine can compare real reports to exact boundaries. The finite-bit proposition is an approximation theorem with a paid report-precision oracle.

This distinction should be placed next to the first exact circle construction, not only in the resource section.

### 14.12 State a clear route to a materially stronger top-four case

The conclusion should identify one or two concrete targets rather than listing many open directions. The most compelling are:

- a state-dependent-likelihood extension with an intrinsic pooling term; or
- a recognized natural problem whose optimal finite-state curve follows from the theorem.

---

## 15. Technical comments

1. In Theorem `thm:energy`, put the zero-energy and zero-product-factor qualifications directly in the theorem statement, not only in the proof.

2. State whether `eta_t(m)` is attained. The lower needs only an infimum, but the equality criterion should distinguish actual attainment from approximation.

3. The output alphabet has at most `m_t` labels; zero-mass labels can be discarded before applying the static quantization identity. Say this explicitly.

4. Define the response set as the closed unit ball or the convex hull of the predictive orbit before the first use of a scaled terminal readout.

5. In the homogeneous upper, state that the codepoint cover has at most `m` points. Repeated or unused labels do not improve the resource count.

6. Separate the notation `k=d+1` used for sphere coordinates from the `k=D^2-1` audit dimension in the projective theorem.

7. Near the baseline `B=V-1`, state once that the total audit loss may be rescaled to `[0,1]` if required by a comparison theorem, without changing the excess identities.

8. In Lemma `lem:circle`, give a citation or a short justification for the fractional rearrangement principle before differentiating the mass functional.

9. In the deadline lemma, say explicitly that the physical experiment continues to make reports available until the machine halts; otherwise a reader could misread the horizon as an externally terminated process.

10. For mutually equivalent phase report laws in the singular clock lower, formulate the exact positive-path-support lemma and identify the common null sets.

11. In the singular theorem, display separately the total risk and the excess over `B_n=V-w_n`; this will reduce sign errors when readers compare it with the un-erased baseline `B=V-1`.

12. In the projective quantum theorem, verify the audit normalization in one line:

```text
E[S e_I | rho] = (r c_D/k) x.
```

13. Clarify whether the Hilbert--Schmidt basis contains matrices with operator norm exactly one or merely at most one; positivity only needs the latter.

14. In the uniform orbit-mass lemma, name the selected rank `j(V)` and note that constants are uniform after taking the maximum over the finite set `1,...,D-1`.

15. The Borel section for rank-one projectors should be described as a finite-chart section modulo phase; this is asserted but can be made more explicit.

16. In Proposition `prop:access`, the family remainder `B_N(X)` is global. A sharper fixed-`x` statement is available by applying the inherited theorem to the singleton family; mention this if useful.

17. The Boolean gate and prefix clock in the accessibility tester are extra labels. Keep them outside the original observer budget in every derived statement.

18. In Proposition `prop:composition`, specify whether `epsilon` already includes the target observer's fresh randomization. The proof appears to compare the complete joint law, which is the correct version.

19. In the finite-bit proposition, the bound `C(M-1)h` can saturate at one; retain the displayed `min(1,...)` in every summary.

20. State whether compiled sine/cosine constants are shared read-only data or copied into every row when reporting the program-description bound.

21. The disclosure-deficiency lower uses a statistic in `[-1,1]`, hence the expectation gap is at most twice total variation. The manuscript uses the correct factor; note the convention beside the proposition.

22. In the full resource law, distinguish constants depending on dimension from those depending on physical contrast `chi`, especially as `chi` tends to zero.

23. The external report response says “nonregenerative” for the energy theorem. It would be more precise to say “finite-horizon without a regenerative decomposition”; the raw word process still begins from one preparation.

24. The bibliography should cite published versions where available. In particular the Ghomi--Linder--Yuksel article has a 2022 IEEE Transactions on Information Theory publication.

25. The recent literature comparison should record search dates but should not treat absence of an exact match as a priority proof.

26. Keep build and regression counts out of the mathematical abstract and conclusion. Their current placement in evidence files is appropriate.

27. The corrected Companion F should state visibly on its title page that it is a corrected preserved version of R27, not the originally externally reviewed object.

28. The review response and retained-patch manifest should continue to preserve the original R27 report and source objects separately from the corrected companion.

---

## 16. Directions that could materially change the top-four assessment

### 16.1 State-dependent likelihoods

Derive a replacement for the energy identity when the report law depends on the current predictive state. A useful result would identify the extra term caused by Bayesian normalization and still give an all-finite-state lower with an attainable compatibility criterion.

### 16.2 Intrinsic recursive-compressibility classification

Turn the local pooling criterion into a theorem that characterizes when a family of acquired laws admits a compatible sequence of finite quantizers. Such a result should not assume a compact-group action in advance.

### 16.3 Exact higher-dimensional law

Find a homogeneous orbit beyond the circle for which exact static optimal cells and exact pooling compatibility can be proved, yielding a closed total-state formula rather than order bounds.

### 16.4 Recognized natural application

Apply the theory to a standard relative-sensing, synchronization, attitude-estimation, phase-tracking, or quantum-reference-frame problem and derive a previously unknown optimal finite-memory curve.

### 16.5 Matched computational resources

Prove lower bounds that couple persistent labels with program description, report precision, workspace, arithmetic time, or simulator memory. The present implementation counts are upper bounds only.

Any one of the first four, if developed at comparable sharpness, could significantly alter the editorial assessment.

---

## 17. Editorial assessment

R29 is a coherent and technically serious article. Its main theorem is more conceptually concentrated than the earlier restart manuscripts: the row/pooling decomposition identifies a real causal obstruction, the circle realizes it exactly, and the complete-state deadline law is memorable and testable.

The paper is also careful about several recurrent sources of overclaiming:

- it does not identify checkpoint and online risk;
- it does not normalize away singular mass;
- it does not provide the observer with analytical conditional means;
- it charges phase labels and inactive states;
- it does not call finite-precision execution exact real arithmetic;
- it preserves the physical audit in deficiency comparisons; and
- it does not claim exact higher-dimensional saturation.

These strengths make the manuscript a plausible contribution to a strong specialist journal.

At the top-four general-mathematics level, however, the advance remains too tied to a specially symmetric relative-report interface, and its broader conceptual consequence has not yet been demonstrated. The exact circle result is elegant, but elegance and correctness within a designed class do not by themselves supply the breadth or external impact expected at that level.

My recommendation is therefore:

> **Reject at the top-four general-mathematics level in the present form, without prejudice to publication after focused revision in a strong specialist venue.**

The recommendation would warrant reconsideration if the author can either extend the mechanism beyond state-independent homogeneous transport or use it to settle a recognized natural finite-memory problem.
