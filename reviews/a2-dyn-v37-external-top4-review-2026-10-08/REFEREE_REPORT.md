# External top-four referee report on A2-DYN revision 37

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v37-referee-response-2026-10-08`, `revision/a2-dyn-v37-referee-copy-2026-10-08`  
**Reviewed commit:** `d039c92d9f957ee180b74c0f3cf4c8bf52b9547c`  
**Reviewed repository tree:** `3f642ca58b50434c65ecb2028e579991faa396a8`  
**Ordinary source payload tree:** `5c37877f730b6e4743f10f2a9c9c266882e237cb`  
**Active manuscript directory:** `papers/A2-DYN-v37-referee-response`  
**Active mathematical source:** seventy-nine numbered core modules; revision 37 adds modules 76--79 and makes six declared replacements in modules 72 and 74  
**Actual mathematical baseline:** revision 35, commit `fda52bb72045204b50159e8263c05afaa6a9dc58`  
**Controlling report:** `reviews/a2-dyn-v36-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `ef921b94134118b9b41a4ca8237c3f87a34a02bd` / `a3b919fec33408b58505649125f4f74c3a9af5ef`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 37 is an actual theorem-bearing author revision. It is not a branch-name alias for a previous review commit. This resolves the source-identity defect emphasized in the preceding report.

It also contains a substantive advance on the original four-coordinate return problem. The manuscript now realizes the true section occupation

```text
A_{m,R}=sum_{j=0}^{m-1} 1_{Y_R^*}(T_R^j x)
```

as an exact bounded multiplier on the collision anisotropic spaces, proves a mixed local--central limit for displacement, roof and occupation, and then uses an exact orbit disintegration to obtain a local theorem for the original actual-return measure. In that theorem displacement and physical collision count are fixed exactly, roof time lies in a fixed unscaled interval, and the genuine return index is resolved on a diffusive window.

The source also repairs the previously circular endpoint of the strong-space faithfulness proof, states finite-cover mixing as an independent input with a pinned theorem, separates the hypotheses of the compact-family principle, and supplies a genuinely nonelliptic support-function application.

I audited the new modules

- `core/76_finite_cover_inputs.tex`;
- `core/77_section_occupation_local_limit.tex`;
- `core/78_actual_return_local_windows.tex`;
- `core/79_support_function_family.tex`;

as well as the declared changes to modules 72 and 74. I found no decisive counterexample, endpoint-indexing error, Fourier-sign inconsistency, covariance-Jacobian error, or hidden replacement of the actual return event in the new chain.

In particular, the following points are internally coherent:

1. the occupation multiplier is placed on the source side of each collision step, while the preceding displacement--roof multiplier remains on the image side;
2. the resulting chronological pairing counts section visits in `[0,m)` and excludes collision `m`;
3. on an orbit beginning and ending in the section, `A_{m,R}=n` is equivalent to `N_{n,R}=m`;
4. the matrix identity `Omega_R=c L_R D_R L_R^T` gives `det Omega_R=c^6 det D_R`; and
5. the limit amplitude agrees with the result of summing a hypothetical four-coordinate singleton local law over `sqrt(m)` return indices.

These are meaningful achievements. Revision 37 is materially stronger than revision 35 and substantially stronger than the v36 alias state.

The negative recommendation is nevertheless unavoidable at the requested benchmark. The new result is a **diffusive-window local theorem**, not the full raw mixed-density local limit theorem advertised by the article's title and inherited endpoint. The manuscript itself correctly records that the following remain unproved:

- inversion to one exact return index;
- the common pointwise raw correction for the actual-return law;
- the complete return-frequency complement;
- pointwise roof-density inversion for the four-coordinate return record;
- the unconditional singleton raw-return LLT;
- general selected-path Gaussian amplitudes and the microscopic conditional path bridge.

Resolving the return index in a window of width `sqrt(m)` integrates out precisely the occupation frequencies that remain uncontrolled away from a shrinking neighborhood of zero. Keeping the roof in a fixed interval likewise avoids the pointwise continuous-coordinate inversion and the critical-edge complement which organize the raw theorem. Thus the new theorem is not a reformulation of the missing endpoint; it is a rigorous and useful marginal/window consequence that remains strictly weaker.

At a four-journal level, the paper would need either the completed raw-return theorem or a general theorem of independent breadth whose significance does not depend on that unfinished endpoint. Revision 37 supplies neither yet. Its strongest completed package remains technically impressive but closely tied to finite-horizon periodic dispersing billiards, one lattice, one exact section geometry, and the existing anisotropic collision framework.

My mathematical assessment is therefore positive about the direction and cautious about correctness, but negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source and chronology

The two author branches named above both resolve to

`d039c92d9f957ee180b74c0f3cf4c8bf52b9547c`.

The repository tree is

`3f642ca58b50434c65ecb2028e579991faa396a8`.

The active paper is

`papers/A2-DYN-v37-referee-response`.

This is the first theorem-bearing manuscript after the v36 branch-alias episode. The actual mathematical baseline is revision 35 at

`fda52bb72045204b50159e8263c05afaa6a9dc58`.

Revision 37 preserves all seventy-five inherited core modules in the compiled article. Seventy-three are byte-identical. Six exact replacements are made in modules 72 and 74, and their old versions are retained under `provenance/`. The four new mathematical modules are 76--79. All eighty-three inherited Python files, the bibliography, the inherited theorem labels, and the compiled A--X synopsis are retained.

The controlling report is the v36 submission-state and supplementary report at

`ef921b94134118b9b41a4ca8237c3f87a34a02bd`.

That report identified the revision-36 aliases as review commits rather than new author mathematics, audited revision 35, and requested an actual new source, a noncircular faithfulness proof, a theorem-level finite-cover mixing input, a clearer separation of compact-family assumptions, progress on the true section occupation, preservation of the corrected Portmanteau condition, and an independent specialist audit.

Revision 37 responds directly to all but the last of those requests and to the full singleton raw-return endpoint.

The present review branch starts from the reviewed author SHA and adds this report only under

`reviews/a2-dyn-v37-external-top4-review-2026-10-08/`.

No manuscript source, author branch, previous report, workflow, historical paper, or unrelated repository path is intentionally modified.

## 3. Qualification and verification boundary

The exact-source qualification workflows completed successfully on both author branches:

- response branch run `37658530003`;
- referee-copy branch run `37658545478`.

The source manifest records the active directory and payload tree, the two exact branch names, the revision-35 baseline, the controlling report blob, seventy-nine included core modules, all inherited labels, and the declared replacement ledger.

The validation protocol checks, among other things,

- reconstruction from the frozen baseline;
- the complete ordinary-source Merkle identity;
- exact replay of the six replacements;
- native TeX compilation with warnings and undefined references treated as failures;
- equality of normal and optimized diagnostic output;
- exact rational covariance and Schur-complement identities;
- endpoint/count conventions in finite orbit models;
- negative controls for the wrong endpoint, wrong sign, or missing occupation term; and
- rendering of the pages found from the actual theorem labels.

These checks are valuable provenance evidence. They do not certify:

- the continuum multiplier theorem for the moving five-rectangle section;
- regularity of every matched connector through every intermediate iterate;
- the action-weighted Lasota--Yorke estimates;
- strong-space faithfulness;
- finite-cover mixing for every stated family;
- the compact-family peripheral exclusion;
- the mixed local--central theorem;
- the parameter-varying endpoint-measure passage; or
- the support-function tangency and transversality assertions.

The manuscript and its metadata correctly disclaim formal proof certification and independent human review.

## 4. Scope of this review

I have not attempted to reproduce every argument in a seventy-nine-module article. My substantive audit concentrated on:

1. the repaired strong-space faithfulness endpoint;
2. the pinned finite-cover mixing input;
3. the true-section multiplier;
4. the joint displacement--roof--occupation covariance;
5. the compact displacement--roof gap perturbed by a small occupation frequency;
6. the mixed local--central inversion;
7. the exact return/occupation disintegration;
8. the normalization against the inherited return covariance;
9. the support-function application;
10. source identity and exact-SHA qualification; and
11. the distinction between a diffusive return window and the full singleton raw theorem.

The inherited stationary physical local theorem, collision Gaussian theory, periodic arithmetic, edge extraction, coherent cutoff transport, path statements, and raw inversion criteria are treated as the source-pinned baseline asserted by the packet. This report does not convert previous AI-assisted review into proof certification.

## 5. Repair of strong-space faithfulness

The previous report identified a circular last sentence in the proof that the strong anisotropic completion is faithfully represented by physical distributions. Revision 37 repairs that endpoint.

The proof first uses transverse averaging to show that a vector annihilating every smooth global test also annihilates smooth tests on stable curves. It then passes to the little `C^q` stable tests by norm density, including endpoint trimming and approximation of boundary curves by curves with strict cone and curvature margins.

The conclusion is now made directly in the defining seminorms:

- every normalized stable-curve pairing vanishes, hence the strong stable seminorm is zero;
- every matched-pair difference is a difference of two zero pairings, hence the unstable seminorm is zero.

The completed-space step is expressed through uniform convergence of the two scalar pairing families for a strong Cauchy sequence. It no longer concludes by assuming injectivity of the strong-to-weak inclusion which the argument was meant to establish.

This fixes the specific logical objection in the preceding report. The transverse-averaging construction and the passage from global tests to all admissible stable tests remain specialist-level functional analysis, but I found no remaining formal circularity in the printed endpoint.

## 6. Finite-cover mixing

Revision 37 separates finite-cover dynamics from connectedness and other geometric assumptions. For each fixed finite lattice cover it invokes a collision-map exponential correlation theorem in the transverse finite-horizon configuration class, checks the obstacle regularity, curvature bounds, positive minimal flight length and transverse horizon, and then extends mixing from the stated Hölder class to `L^2` by approximation.

The arithmetic argument fixes one prime cover at a time. It requires no rate uniform in the prime and does not sum estimates over cover size. This is the correct logical scope.

The distinction between the two arithmetic cases is also correct:

- a nonzero constant-step character would produce a nontrivial unit-modulus eigenvalue and is excluded by mixing;
- a zero constant-step character would produce a nonconstant invariant function and is excluded by ergodicity.

This is an improvement over treating connectedness as a proxy for mixing.

The applicability of the pinned theorem to each fixed flat Euclidean cover remains an important human-audit item, especially the asserted transverse-horizon verification and the passage from the triangular cover to a rectangular Euclidean realization. I found no concrete contradiction in the written check.

## 7. The actual section as an anisotropic multiplier

The new section occupation is

```text
eta_R = 1_{Y_R^*},
A_{m,R} = sum_{j=0}^{m-1} eta_R(T_R^j x).
```

The proof uses the actual five-rectangle section. Its boundaries lie in a compact region away from grazing. After the stated coordinate changes, the horizontal and vertical sides remain transverse to the stable cone. A stable curve meets each side at most once, its intersection with each cell is an interval, and the stable length within distance `epsilon` of the fixed finite boundary is `O(epsilon)`.

These are the appropriate fixed-complexity conditions for a piecewise multiplier. The idempotence of the indicator gives the exact entire formula

```text
exp(iv(eta_R-c))
 = exp(-ivc) [I + (exp(iv)-1) M_{eta_R}].
```

No smoothing limit is used.

This is exactly the new ingredient needed to distinguish true section occupation from the constant collision step used in the earlier physical arithmetic.

The most important specialist check is whether the same local collision spaces and exponent conventions used for the preceding-flight multiplier apply without modification to every moving rectangle corner and coordinate cut. The manuscript supplies a plausible finite partition argument; finite diagnostics cannot validate this continuum multiplier statement.

## 8. Chronological operator convention

Let `Q_{R,z}` be the image-side displacement--roof collision operator. Revision 37 defines

```text
mathcal Q_{R,z,v}=Q_{R,z} M_{exp(iv(eta_R-c))}.
```

With the transfer convention used in the paper, this order inserts the occupation at the source point of each collision and the preceding-flight record on the image side. Iterating gives the physical pairing

```text
exp{i z·(K_m^c,S_m-m bar_tau_R) + i v(A_m-mc)}.
```

The sum therefore includes collision times `0,...,m-1` and excludes collision `m`.

I checked this endpoint convention against the later return disintegration. It is consistent. Reversing the two multiplier sides would shift the occupation and break the exact identity; the manuscript does not make that error.

## 9. Joint covariance and Schur data

The bounded compensated collision observable inherited from the paper is transformed by the matrix

```text
L_R = [[1,0,0,0],
       [0,1,0,0],
       [0,0,-bar_tau_R,1],
       [0,0,-c,0]].
```

Applied to the compensation, this gives exactly

```text
(kappa_1,kappa_2,tau_R-bar_tau_R,eta_R-c).
```

Thus

```text
Omega_R = L_R Gamma_R L_R^T = c L_R D_R L_R^T.
```

Since `det L_R=c`, in four dimensions

```text
det Omega_R = c^6 det D_R.
```

The manuscript's Schur complement

```text
beta_R=b_R^T Sigma_R^{-1},
sigma_{A,R}^2=d_R-b_R^T Sigma_R^{-1}b_R
```

is consequently positive and uniformly bounded away from zero when the inherited return covariance is uniformly positive definite.

I found the covariance transformation, determinant, conditional mean sign and scale normalization internally consistent.

## 10. Fixed displacement--roof band and small occupation frequency

For each fixed displacement--roof band and fixed exclusion radius, the inherited compact collision spectrum gives a spectral radius strictly below one away from zero. The exact occupation multiplier differs from the identity by `O(v)` in strong operator norm. A uniform resolvent perturbation therefore preserves the compact-band gap for sufficiently small occupation frequency.

The order of quantifiers is important:

1. fix the displacement--roof band `B` and the exclusion radius;
2. choose the occupation neighborhood depending on them;
3. let the collision count tend to infinity.

The mixed theorem uses occupation frequency `theta/sqrt(m)`, which eventually lies in this neighborhood for every fixed `theta`. It does not require a spectral estimate on the full occupation torus.

This is sufficient for a central-limit variable in occupation. It is not sufficient to invert occupation to one exact integer. The manuscript states this limitation accurately.

## 11. The mixed local--central theorem

Theorem `thm:v37-occupation-local-central` fixes displacement at one lattice point and the roof sum in a fixed interval, while testing the centered occupation on its `sqrt(m)` scale.

For a fixed band-limited roof test and a characteristic occupation test, the exact Fourier expression uses

```text
mathcal Q_{R,(u,b),theta/sqrt(m)}^m.
```

The compact complement is exponentially small by the preceding fixed-band argument. Near zero, the joint analytic expansion yields the four-dimensional Gaussian. Partial inversion in the three displacement--roof variables gives

```text
g_{Sigma_R}(z)
 exp{i theta beta_R z - theta^2 sigma_{A,R}^2/2}.
```

The sign of the conditional mean is consistent with the inverse factor `exp(-iw·z)`.

To replace the band-limited roof test by a sharp interval, the proof uses positive upper and lower Fourier envelopes. Although the occupation characteristic factor is complex, the replacement error is dominated in modulus by the nonnegative upper-minus-lower endpoint integral at occupation frequency zero. The proof then takes `m` to infinity for each fixed band before enlarging the band.

This is a sound order-preserving mechanism. It avoids comparing complex integrands by order and avoids inserting a growing band into a fixed-band spectral estimate.

The passage from characteristic functions to bounded continuous occupation tests uses finite positive measures, convergence of their masses, and continuity of the limiting Gaussian transform. Fixed intervals and half-lines are continuity sets. The statement is appropriately central, not local, in occupation.

I found no decisive defect in this argument. Its continuum spectral premises remain part of the specialist-audit burden.

## 12. Exact return/occupation disintegration

On a nonsingular orbit beginning at a section point and ending at a section point at collision time `m`, write the section visits as

```text
0=j_0<j_1<...<j_n=m.
```

There are exactly `n` visits in `[0,m)`. Therefore

```text
A_{m,R}=n,
N_{n,R}=m.
```

Conversely, `N_{n,R}=m` gives precisely this list. On the same event, additivity gives

```text
K_{n,R}=K_{m,R}^c,
T_{n,R}=S_{m,R}.
```

After inserting the normalized section measure, this proves the exact measure identity in Proposition `prop:v37-exact-return-disintegration`.

The endpoint convention is correct: the terminal visit at `m` is excluded from `A_m`, so the number of visits counted equals the number of completed returns.

No random-clock approximation, event replacement, independence assumption, or asymptotic comparison is used in this step.

## 13. The actual-return window theorem

The theorem defines a positive measure in

```text
y=(n-mc)/sqrt(m)
```

by summing the original return probabilities over genuine return indices. Applying the mixed occupation theorem with both endpoint multipliers equal to `eta_R` gives endpoint amplitude `c^2`; the normalized section source contributes `c^{-1}`. The limiting amplitude is therefore `c`.

For a fixed interval `[a,b]` in the rescaled return coordinate, the theorem obtains

```text
m^(3/2) sum_n P{K_n=k, N_n=m, T_n-t in J}
 -> c |J| g_{Sigma_R}(z)
    integral_a^b g_{sigma_A,R^2}(y-beta_R z) dy.
```

The lower bound of order `m^(-3/2)` follows from positivity, continuity and compactness.

The agreement formula

```text
c g_{Omega_R}(z,y)
 = c^(-2) g_{D_R}(c^(-1/2)L_R^(-1)(z,y))
```

is consistent with `Omega_R=c L_R D_R L_R^T`. It is exactly the normalization obtained by summing a putative `n^(-2)` four-coordinate local law over `sqrt(m)` adjacent return counts.

This last observation is a normalization check, not a proof of the missing singleton law. The manuscript is explicit on that point.

## 14. What the return-window theorem does and does not prove

Theorem 3 is genuinely a theorem about the original return measure. It is not merely a stationary-flow consequence. It fixes:

- both displacement coordinates exactly;
- physical collision count exactly;
- roof time in a fixed unscaled interval;
- return index in a diffusive window.

It therefore gives a nontrivial local constraint and a positive denominator for that window event.

It does **not** fix one exact return index. Such an inversion requires control of occupation frequencies outside the shrinking `m^{-1/2}` neighborhood used by the proof.

It also does **not** give a pointwise density in the roof coordinate. That requires the raw edge correction, pointwise common correction, and complete roof-frequency complement.

These missing inversions are exactly the portions of the original raw theorem which remain analytically difficult. Weak convergence of the occupation window measures cannot supply them.

Accordingly, the source manifest is correct to leave

```text
full_raw_return_LLT_proved = false,
common_pointwise_return_correction_proved = false,
full_return_complement_proved = false.
```

## 15. The nonelliptic support-function family

The support function

```text
h(psi)=R+e cos(3(psi-theta))+f cos(4(psi-phi))
```

with the printed compact parameter constraints has positive curvature radius. The support bounds place each obstacle between two fixed disks, giving a positive lattice gap and transferring finite horizon from the smaller circular table.

The perimeter and area formulas follow from orthogonality of the third and fourth harmonics. A nonzero third harmonic prevents central symmetry even after translation, so the family is genuinely nonelliptic.

The manuscript further checks:

- finite candidate obstacles under the uniform horizon;
- semialgebraic rational-trigonometric charts before normalized arclength;
- a square-root normal form at nondegenerate tangency;
- stable transversality of the backward singularity arcs;
- finite-cover mixing;
- regular matched connectors inherited from the unweighted construction; and
- closed exceptional neighborhoods with small measure and null boundary for the one-flight observation intervals.

This is a useful second application of the action mechanism and materially strengthens the generality case beyond circles and ellipses.

The semialgebraic partition, uniform tangency normal form and transversality assertions remain significant continuum claims. I found no direct contradiction, but they should be audited by a specialist rather than inferred from the finite arithmetic scripts.

## 16. Relation to prior local-limit theory

The conceptual ingredients of the new return-window result are recognizable within existing hyperbolic local-limit methodology:

- analytic perturbation near zero;
- compact-frequency spectral exclusion;
- partial Fourier inversion;
- positive envelopes for sharp roof intervals;
- a bounded additional observable tested on its central scale; and
- disintegration through an exact return identity.

The manuscript's genuine contributions are the physical verification of these ingredients for the unsmoothed billiard observables, the moving compact family, the exact section multiplier, the source/image ordering, the finite-cover arithmetic, and the exact passage from occupation to the actual return record.

This is substantial specialized mathematics. The return-window theorem also aligns the completed physical part with the original return problem more effectively than earlier revisions.

It still does not, in my judgment, establish a four-journal significance case. The theorem is a partial inversion deliberately designed to avoid the two unresolved noncentral frequency directions. The general action-family principle remains built around the established anisotropic collision framework for finite-horizon periodic dispersing billiards, and the applications share one lattice and closely related obstacle geometry.

A stronger significance case would require one of the following:

1. completion of the singleton raw-return LLT;
2. full occupation-frequency control yielding exact return-index inversion;
3. a general theorem for a substantially wider class of singular hyperbolic systems, with independent applications; or
4. a new sharp phenomenon not already organized by spectral perturbation and suspension/inducing local-limit methods.

## 17. Architecture and presentation

The three leading theorems now make the completed stationary theorem, the compact-family action principle, and the return-window theorem visible at the front of the paper. The division into an action/physical part and an actual-return/raw-inversion part is clearer than the architecture of earlier revisions.

The paper nevertheless remains extremely large. It combines:

- a completed stationary microscopic theorem;
- a compact-family and nonelliptic extension;
- a new actual-return window theorem;
- a long inherited Gaussian and functional pipeline;
- periodic arithmetic;
- critical-edge extraction;
- finite-band reconstruction; and
- an unfinished singleton raw-return programme.

For an editorial submission, the authors should decide whether the principal theorem is the compact-family physical local law plus return-window theorem, or the full raw-return theorem. At present the title and historical architecture continue to promise more than the strongest completed return statement.

This is not a recommendation to delete the inherited mathematics. It is a recommendation to separate completed theorem, supporting technology, and open endpoint so that the reader can evaluate the submission without treating an unfinished programme as part of the claimed main result.

## 18. Independent verification burden

No independent human specialist audit is claimed. Such an audit is particularly important here because the main novelty is not a short abstract deduction but a chain of technical continuum assertions.

The highest-priority checks are:

1. the five-rectangle section against the exact piecewise-multiplier hypotheses in the same local spaces used for the roof twist;
2. the source/image operator convention and `[0,m)` occupation identity;
3. transverse averaging and the little-`C^q` passage in strong-space faithfulness;
4. every matched connector's intermediate regularity;
5. the weighted weak, stable and unstable norm sums;
6. the physical representation of peripheral eigendistributions;
7. applicability of the finite-cover mixing theorem to every fixed cover and family;
8. the small-occupation resolvent perturbation on a fixed displacement--roof band;
9. the positive-envelope replacement with a complex occupation phase;
10. the conditional Gaussian sign and covariance normalization;
11. the support-family singularity partition and tangency normal form; and
12. the parameter-varying endpoint tests with closed exceptional neighborhoods.

Successful exact-SHA builds and finite model checks do not discharge these obligations.

## 19. Required changes before another top-four review

A further top-four submission should address the following points.

1. **Complete the exact return-index inversion.** Establish spectral or cancellation control for occupation frequencies outside the shrinking central neighborhood, sufficient to pass from a diffusive window to one return index.
2. **Complete the pointwise roof inversion.** Prove the common raw correction and full return-frequency complement for the four-coordinate return law, including the critical/singular branch contribution in the local norm required by the theorem.
3. **State one completed principal endpoint.** If the singleton raw theorem is not yet complete, the submitted article should present the physical and return-window theorems as its finished claims and move the remaining raw programme to an explicitly separate sequel or companion.
4. **Obtain an independent specialist audit.** At minimum, the section multiplier, action-weighted norms, faithfulness, peripheral-density argument, finite-cover input, mixed local--central theorem and support-family verification require review by experts in dispersing billiards and anisotropic transfer operators.
5. **Make the novelty comparison theorem-by-theorem.** Distinguish the exact new uniform-family, occupation, endpoint and posterior statements from existing fixed-table Lorentz and suspension local-limit results.
6. **Strengthen the generality case.** Explain which hypotheses and conclusions survive outside one-obstacle periodic Lorentz gases and demonstrate the mechanism on genuinely independent systems if a four-journal breadth claim is maintained.
7. **Preserve all scope distinctions.** A window theorem must not be described as a singleton theorem; source-total-variation approximation must not be described as a universal selected Gaussian amplitude; and a physical fixed-count theorem must not be substituted for the raw return-density theorem.
8. **Retain exact version identity.** The two author branches, active directory, source manifest, workflow and referee copy should continue to identify one mathematical SHA, as revision 37 now does.

## 20. Final assessment

Revision 37 is a serious mathematical advance. It is a genuine author revision, repairs two load-bearing proof interfaces, broadens the compact-family application beyond quadrics, and proves a local theorem on the original actual-return measure rather than only on the stationary physical process.

The exact section multiplier and return disintegration are particularly valuable. The covariance normalization is coherent, the order of Fourier limits is appropriate, and I found no decisive mathematical error in the new chain during this audit.

Subject to specialist verification, the completed stationary theorem, compact-family action principle, nonelliptic application and actual-return window theorem form a credible and potentially strong contribution to dispersing billiards and dynamical limit theory.

At the requested *Annals* / *Acta* / *Inventiones* / *JAMS* benchmark, however, the submission remains premature. The original singleton raw-return theorem is still unproved, the new return theorem deliberately averages over the unresolved return-index frequency, the pointwise roof complement remains open, the breadth/significance case remains specialized, and no independent expert proof audit has occurred.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
