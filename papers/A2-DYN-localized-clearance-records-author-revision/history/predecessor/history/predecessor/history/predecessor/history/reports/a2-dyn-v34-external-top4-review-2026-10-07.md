# External top-four referee report on A2-DYN revision 34

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v34-referee-response-2026-10-07`, `revision/a2-dyn-v34-referee-copy-2026-10-07`  
**Reviewed commit:** `882035928dbf3a0c7fe079ec2a7813ab9b921d65`  
**Reviewed repository tree:** `8f534c28ab9522ad609c0965cfbda6b344d722b0`  
**Ordinary source payload tree:** `4d846ba657c6d5b44aa9ac22b17eb570fd1c378e`  
**Active manuscript directory:** `papers/A2-DYN-v34-referee-response`  
**Active mathematical source:** seventy-one numbered core modules; revision 34 adds modules 69--71  
**Frozen revision-33 author baseline:** `13af9a5795503671a18b5c261e79d61e87ae8bd6`  
**Frozen revision-33 paper tree:** `42ba62ef825d1e555f6c6bf83e647792bba67de8`  
**Controlling report:** `reviews/a2-dyn-v33-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `9fc2f553168a589e043be73e0354900d5559f433` / `5159113603f557e654792626bf88c2aa5396e3c9`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This recommendation requires a substantially different explanation from the recommendation in the revision-33 report.

Revision 34 is a genuine and important mathematical revision. Revision 33 had reduced the original stationary singleton probability to a Gaussian central contribution plus one explicit signed middle-frequency inverse, but it did not prove that the latter vanished. Revision 34 supplies a new three-module argument which, if the load-bearing anisotropic estimates are correct, closes that physical problem. It proves a parameter-uniform microscopic local limit for

\[
  \{W_R(t)=k,\ C_R(t)=m\}
\]

under the stationary Lorentz-flow law, with the actual initial flight age and both within-flight cell corrections retained. It also obtains a positive microscopic denominator, evaluates a regular endpoint-selected class, proves normalized total-variation comparison with the positive finite-band likelihood, and deduces the vanishing of the complete signed middle inverse at an explicit polynomial bandwidth.

I audited the new modules

- `core/69_compact_collision_spectrum.tex`;
- `core/70_collision_mixing_local_limit.tex`;
- `core/71_stationary_microscopic_local_limit.tex`;

and their use in the new leading theorem. I found no decisive counterexample, normalization error, Fourier-sign inconsistency, omitted cell correction, or invalid exchange of a growing frequency cutoff with a fixed-band spectral estimate. The proof deliberately takes the collision count to infinity for each fixed band and only then enlarges the band through positive upper and lower envelopes. That order is mathematically appropriate and is one of the principal improvements over the unresolved revision-33 reduction.

The negative top-four recommendation is therefore **not** based on the absence of an unconditional physical local theorem. At the level of the stated stationary event, revision 34 crosses that threshold.

The recommendation is instead based on four broader considerations.

First, the article's title, historical architecture, and much of its mathematical mass are still organized around the raw four-coordinate law of the actual induced return record

\[
 J_{n,R}=(K_{n,R},N_{n,R},T_{n,R}).
\]

The manuscript explicitly records that the pointwise common return correction and the full return-frequency complement remain unproved. The new bounded collision twist contains the displacement--roof triple at a prescribed physical collision count; it contains neither the discontinuous section occupation nor the unbounded induced record. Thus the original raw-return local limit theorem remains open inside the submitted article.

Second, while the stationary theorem is substantial, the manuscript has not yet made a convincing four-journal significance case relative to the existing Lorentz-process local-limit theorem, mixing local-limit theorems with endpoint observables, and abstract suspension-flow local central limit theory. The genuinely new features appear to be the uniform moving-radius family, the joint displacement/collision-count singleton at deterministic physical time, exact treatment of the stationary age and two cell offsets, and the source-level posterior comparison. These are valuable. In the current presentation, however, they form a highly specialized theorem for one compact one-parameter triangular billiard family rather than a new general mechanism stated and proved at a level likely to transform the subject.

Third, the decisive new operator argument is compressed relative to its difficulty. The preceding-flight multiplier, its partition by backward singularity curves, the matched-connector action estimate, the bounded-band Lasota--Yorke inequalities, the passage from peripheral distributions to bounded physical phases, and the parameter-varying endpoint test all require specialist verification. I did not find a fatal flaw in the written chain, but source qualification and finite diagnostics do not substitute for an independent expert reading of those continuum arguments.

Fourth, the present article is extremely large and carries two distinct local problems: the now-completed stationary physical singleton theorem and the still-incomplete four-coordinate raw-return theorem. The new front matter is much better than the cumulative revision-33 synopsis, but the body still asks the reader to navigate seventy-one modules and a long historical pipeline before the principal new contribution can be judged against the literature.

My mathematical assessment is consequently more positive than a bare rejection label suggests. Subject to a genuine billiards/anisotropic-spaces proof audit, revision 34 contains a credible major theorem and could support a strong specialist or high-level dynamics/probability submission. At the requested four-journal benchmark, however, the incomplete organizing return theorem, the specialized scope of the completed theorem, the unresolved novelty comparison, and the verification burden prevent a positive recommendation.

## 2. Frozen source and revision chronology

The two named revision-34 author branches resolve to the same commit,

`882035928dbf3a0c7fe079ec2a7813ab9b921d65`.

That commit has repository tree

`8f534c28ab9522ad609c0965cfbda6b344d722b0`.

The source manifest identifies revision 33 as the frozen author baseline and the revision-33 external report as the controlling report. The ordinary revision-34 payload is identified by tree

`4d846ba657c6d5b44aa9ac22b17eb570fd1c378e`.

Revision 34 retains the sixty-eight revision-33 core modules and adds exactly the three new modules listed above. It also rewrites the front matter around one leading theorem, while preserving the former A--X synopsis in a compiled appendix and retaining the prior main source under provenance. The source metadata records that the inherited core modules, inherited Python files, bibliography, and inherited mathematical labels are preserved.

The present review branch starts directly from the reviewed author commit and adds this report only under

`reviews/a2-dyn-v34-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, previous report, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and verification boundary

The exact-source workflow on the response branch completed successfully:

- workflow: `A2-DYN v34 exact-source qualification`;
- run: `37629733461`;
- reviewed SHA: `882035928dbf3a0c7fe079ec2a7813ab9b921d65`;
- conclusion: `success`.

The referee-copy branch points to the identical SHA. I did not find a separate workflow run indexed under that branch name. This creates no source ambiguity, since the two refs identify the same commit, but the provenance record should distinguish one successful exact-SHA execution from two independently executed branches.

The validation protocol checks, among other things,

- the frozen revision-33 source tree;
- preservation of inherited source and labels;
- inclusion of all seventy-one core modules;
- exact source hashes and the workflow hash;
- chronological operator pairings in finite models;
- the order of choices in a finite Lasota--Yorke norm model;
- square-root inequalities used in the multiplier estimates;
- Beurling--Selberg envelope arithmetic;
- weighted overlap factorizations;
- the physical covariance Jacobian;
- native TeX compilation and rendering of the new proof interval.

Those checks are useful for provenance and for detecting algebraic regressions. They do not prove the continuum multiplier theorem, the matched-curve estimates, quasi-compactness, physical peripheral exclusion, the local endpoint-measure convergence, or the resulting local limit theorem. The author-side validation states this limitation correctly.

## 4. Scope of this review

A complete line-by-line verification of a seventy-one-module article is not represented here. The substantive review concentrates on

1. the exact image-side collision twist and its multiplier regularity;
2. the accumulated action estimate on homogeneous and matched curves;
3. the bounded-band Lasota--Yorke argument and compact-frequency spectral gap;
4. the near-origin perturbation and covariance normalization;
5. the fixed-band endpoint local limit and the positive interval-envelope passage;
6. the local endpoint measures and parameter-varying overlap tests;
7. the stationary microscopic local law and its physical covariance change of variables;
8. the deduction of signed-complement smallness and normalized posterior comparison;
9. the distinction between this physical theorem and the still-open four-coordinate return theorem;
10. source identity and qualification evidence.

The many inherited Gaussian, phase-rigidity, covariance, raw-edge, mesoscopic-window, and bridge results are treated as the qualified baseline claimed by the revision. This report does not convert prior author-side or AI-assisted checking into formal proof certification.

## 5. The exact image-side collision twist

Revision 34 uses the bounded collision observable

\[
 f_R^{\mathrm c}=(\kappa_{R,1},\kappa_{R,2},\tau_R-\bar\tau_R)
\]

and places its preceding-flight version on the image side of the collision transfer operator:

\[
 Q_{R,z}=M_{\exp(i z\cdot(f_R^{\mathrm c}\circ T_R^{-1}))}\mathcal L_R.
\]

This placement is important. For the adopted convention, iteration gives the exact endpoint pairing

\[
 \ell\!\left(M_dQ_{R,z}^m(a\nu)\right)
 =\int a(x)e^{iz\cdot\sum_{j<m}f_R^{\mathrm c}(T_R^jx)}
        d(T_R^mx)\,d\nu(x).
\]

I checked the chronological orientation. The initial density is on the right, the terminal multiplier is on the left, and the phase is the forward collision sum. The sign and operator order are consistent with the later Fourier inversion.

The manuscript analyzes the preceding-flight root directly in collision coordinates. Finite horizon leaves a fixed finite candidate set. On a regular candidate region, the entry root is one-half Hölder up to the tangency boundary; the displacement label is constant there. The discontinuity boundaries are backward collision singularities, hence unstable curves transverse to stable test curves. This is the correct geometry for applying a piecewise multiplier theorem on the chosen anisotropic spaces, and is preferable to placing the forward flight discontinuity on the wrong side of the operator.

The proof nevertheless uses a nontrivial imported multiplier criterion in a new parameter-uniform setting. A publication version should make the following checks completely explicit in one place:

1. the uniform number of monotone backward-singularity pieces in each homogeneity strip;
2. the uniform stable-curve intersection count;
3. the boundary-neighborhood length estimate required by the multiplier lemma;
4. the exact relation between the selected exponents `p,q,gamma,zeta` and every exponent restriction in the collision spaces;
5. preservation of these conditions under the radius-dependent boundary reparametrization;
6. the multiplier-norm estimate for the complex exponential and all required derivatives.

The written argument gives the intended mechanism and compatible inequalities. I found no contradiction in the exponent choices. The point remains sufficiently delicate that it should not be left to analogy with a cited lemma alone.

## 6. The collision action and accumulated weights

The strongest conceptual step in module 69 is the use of the exact action identity

\[
 d\tau_R=T_R^*\vartheta_R-\vartheta_R,
 \qquad \vartheta_R=R\sin\varphi\,d\alpha.
\]

On a regular connector `gamma` this telescopes to

\[
 S_{m,R}(y)-S_{m,R}(x)
 =\int_{T_R^m\gamma}\vartheta_R-\int_\gamma\vartheta_R.
\]

Since the lattice sum is constant on a regular branch, the long collision phase has a Lipschitz seminorm bounded independently of `m` on each homogeneous inverse stable component. This is precisely the estimate needed to avoid the exponentially growing variation one would obtain by differentiating every flight separately.

The manuscript also treats the matched pieces in the unstable norm. The corresponding initial connector has length of order `Lambda^{-m} epsilon`, while its terminal image has length of order `epsilon`. The telescoping action identity therefore bounds the roof-sum difference by `C epsilon`. Trimming the two inverse graphs to a common interval introduces another `C epsilon` change. Interpolation then gives

\[
 \|w_{m,\omega}^{(1)}-w_{m,\omega}^{(2)}\|_{C^q}
 \le C_B\epsilon^{1-q}.
\]

This is the right form for the unstable comparison.

I found the logic coherent, but it is a principal load-bearing point. In particular, an independent specialist should verify that

- every connector declared matched is regular through all intermediate iterates;
- any connector meeting an intermediate singularity is indeed assigned to the unmatched family without changing the old combinatorial estimates;
- the paired endpoints have identical lattice itineraries;
- the trimming operation used in the actual collision-space proof has exactly the displacement estimate asserted here;
- homogeneity boundaries and grazing endpoints do not create an unrecorded phase partition.

No finite diagnostic can establish these continuum assertions.

## 7. Bounded-band Lasota--Yorke estimates

The proof distinguishes weak, strong stable, and unstable norms. This is necessary; a single multiplier bound is not enough.

For the weak norm, the accumulated phase is a uniformly bounded Hölder test on each inverse piece. For the strong stable norm, the proof subtracts the average of the pulled-back terminal test rather than the average of the entire weighted test. The contracting test difference retains the stable factor, while the nondecaying phase variation is charged to the weak norm. This avoids a common but serious error in which a noncontracting phase derivative is placed in the leading strong coefficient.

For the unstable norm, the old matched/unmatched decomposition is retained. The matched weight difference is paid through the preceding action estimate. The cross term is explicitly allowed to grow like `C_3^m` in the stable norm; the manuscript does not falsely declare it uniformly bounded.

The equivalent-norm argument is ordered correctly. For a fixed frequency band, one first chooses a block length `N` so that the stable and unstable leading coefficients are small, and only afterwards chooses the coefficient of the unstable norm so that the finite cross term at that block length is absorbed. This yields an `N`-step Doeblin--Fortet inequality and hence power boundedness and quasi-compactness.

The dependence of the equivalent norm and constants on the fixed band `B` is harmless for the later proof because no estimate is claimed uniformly in a growing `B`. The local limit argument freezes `B`, takes `m` to infinity, and enlarges `B` only through positive approximation.

For a fully convincing publication proof, I recommend expanding the weighted versions of the precise Jacobian and length sums from the cited unweighted Lasota--Yorke proposition. The present text says which terms change and gives the intended estimates, but a reader should not have to reconstruct the complete norm calculation across two papers and several conventions.

## 8. Peripheral spectrum and the near-origin expansion

After quasi-compactness and power boundedness, the manuscript excludes unit-modulus eigenvalues at nonzero frequency.

The argument takes a peripheral spectral projection and applies it to smooth densities. Cesaro averages of their twisted images remain bounded when paired against `L^1` test functions, so the resulting peripheral distribution is represented by a bounded measurable density `q`. The eigenvector equation becomes a genuine measurable phase equation. Ergodicity makes `|q|` constant, and the inherited complete physical phase theorem forces

\[
 u=0,\qquad b=0,\qquad \lambda=1.
\]

This is a good way to avoid evaluating an arbitrary anisotropic distribution on periodic points. It converts the spectral obstruction to a physical measurable phase before invoking the arithmetic theorem.

The finite-dimensional range and density argument is plausible. A polished proof should state explicitly the density class used in the strong anisotropic space and why the Cesaro projection estimate extends from smooth tests to the claimed `L^1` domination. I found no algebraic defect in the resulting eigen-equation.

Strong-to-weak parameter continuity, the uniform bounded-band Lasota--Yorke estimate, and pointwise peripheral exclusion are then used with compactness to obtain a uniform spectral radius below one on

\[
 |b|\le B,\qquad |(u,b)|\ge\epsilon.
\]

Near zero, strong analyticity gives a simple eigenvalue and spectral projection. Differentiation identifies the Hessian of `log lambda_R` with minus the collision covariance `Sigma_R`. The inherited uniform positive definiteness gives the Gaussian bound. The centering and covariance normalization are consistent with the later three-dimensional inverse.

I found no reason to reject the compact-frequency theorem on internal grounds. Its validity depends chiefly on the multiplier and Lasota--Yorke details discussed above.

## 9. The fixed-band collision local limit

Module 70 first treats a time test `q` whose Fourier transform has compact support. Torus orthogonality and time Fourier inversion give an exact integral containing

\[
 \widehat q(-b).
\]

The minus sign is correct for the convention `q(S_m-t)`. Outside a fixed neighborhood of zero, the compact-frequency spectral gap gives exponential decay. Inside, the perturbative expansion and the rescaling

\[
 v=\sqrt m\,(u,b)
\]

produce the three-dimensional Gaussian. The endpoint amplitude tends to the product of endpoint means.

The manuscript then uses Beurling--Selberg upper and lower envelopes for a fixed interval. Their Fourier transforms are supported in a fixed band, they preserve pointwise order, and their masses differ from the interval length by `2 pi/B` on each side. For nonnegative endpoint insertions, multiplying the envelope inequalities by the source weight preserves order. The proof takes

1. `m -> infinity` for fixed `B`;
2. `B -> infinity` afterwards.

This is the decisive logical point. No unknown growth of `C_B` is used. The squeeze yields the unsmoothed interval local limit and, from one fixed majorant, a uniform local mass upper bound.

The extension from nonnegative smooth endpoint functions to continuous complex functions is handled by positive approximation and decomposition into real and imaginary parts. The local upper bound pays the approximation error.

I found this section internally coherent. It also clarifies the exact advance over revision 33: rather than estimating every intermediate frequency at a polynomially growing cutoff, the proof evaluates positive local probabilities using a two-stage limit.

## 10. Local endpoint measures

The source measure

\[
 \rho_{m,R}^{k,t}
 =m^{3/2}(x,S_{m,R}(x)-t,T_R^mx)_*
   (\mathbf 1_{\{K_{m,R}^{\rm c}=k\}}\nu)
\]

is shown to converge vaguely to

\[
 g_{\Sigma_{R_0}}(\zeta_0)\,\nu(dx)\,ds\,\nu(dy)
\]

along convergent parameter and central-target sequences.

Products of continuous endpoint functions and interval indicators form the initial convergence class. The local upper bound supplies uniform masses on compact time slabs. Continuous compactly supported tests follow by approximation. Tests continuous outside a limiting null set follow by upper/lower approximation or Portmanteau.

The parameter-varying test statement is important. Pointwise convergence alone would not justify substituting the radius-dependent age-overlap function. The manuscript instead assumes uniform convergence outside open exceptional neighborhoods of arbitrarily small limiting measure and uses the local mass bound to control those neighborhoods. This is the correct architecture.

The remaining burden is geometric: the actual overlap tests must satisfy that hypothesis uniformly. Module 71 addresses it by removing grazing, one-flight singularities, cell-edge tangencies, and vertex crossings. On compact sets separated from these exceptions, the flight interval endpoints vary uniformly. The exceptional sets are finitely many curves and boundary pieces, so their neighborhoods have small product measure.

I found this plausible. A specialist should nevertheless verify the treatment of flights coincident with a cell edge, changes in the number of nonempty cell intervals, and the parameter-uniform choice of exceptional neighborhoods. These issues are localized and do not indicate a discovered counterexample.

## 11. The stationary microscopic local law

The exact age-overlap formula expresses the physical singleton probability as a finite sum over initial and terminal cell labels. In the `(d,e)` term the collision displacement label is

\[
 k+d-e,
\]

so both cell corrections remain present. Because the label offsets belong to a fixed finite set, their effect on the normalized central coordinate is `O(m^{-1/2})`.

The overlap test is

\[
 F_R^{d,e}(x,s,y)=H_{I_{R,d}(x),I_{R,e}(y)}(-s).
\]

It is bounded and compactly supported in `s`. Its total limiting amplitude satisfies

\[
 \sum_{d,e}\int F_R^{d,e}(x,s,y)
 \,d\nu(x)\,ds\,d\nu(y)=\bar\tau_R^2.
\]

The stationary source contributes the factor `1/bar_tau_R`, so the collision-scale local law has main term

\[
 \bar\tau_R g_{\Sigma_R}(\zeta_{m,R}).
\]

This normalization is correct.

The sequential compactness argument establishes uniformity over the radius interval and central compact sets. The physical-scale variables are related by the displayed clock map. With

\[
 \mathcal V_R=\bar\tau_R^{-1}D_R^{\rm clk}\Sigma_R(D_R^{\rm clk})^{\mathsf T},
 \qquad D_R^{\rm clk}=\operatorname{diag}(1,1,-1/\bar\tau_R),
\]

one has

\[
 \det\mathcal V_R=\frac{\det\Sigma_R}{\bar\tau_R^5}.
\]

The factor `bar_tau_R^{5/2}` arising from the scale change converts the collision-scale Gaussian exactly to `g_{mathcal V_R}`. Uniform ellipticity then gives a denominator bounded below by `c_M t^{-3/2}` on each fixed central compact set.

I found no missing lattice covolume or clock determinant in this conversion.

## 12. Vanishing of the signed middle complement

Revision 33 proved an exact pointwise decomposition

\[
 t^{3/2}p_{m,R}(k,t)
 =g_{\mathcal V_R}(\xi)
 +t^{3/2}\mathfrak M_{m,R,B_m}(k,t)
 +o(1),
\]

with an explicit central error and a polynomial far-frequency error, but did not estimate the signed middle term.

Revision 34 first evaluates the complete positive probability independently, using fixed-band spectral decay, positive interval envelopes, local endpoint measures, and the exact age overlap. It then subtracts the revision-33 identity. The result is

\[
 \sup t^{3/2}|\mathfrak M_{m,R,B_m}(k,t)|\longrightarrow0
\]

on central compact sets for `B_m=m^{P+3/2}`.

This deduction is logically valid. It proves cancellation in the entire signed inverse. It does not prove that the integral of the modulus of the middle transform is small, and the manuscript does not claim such an absolute estimate. No intermediate frequency region is omitted from the definition of the complement.

The result should be described as a consequence of the independently proved positive local theorem, not as a direct quantitative spectral bound at the growing bandwidth. The present text makes that distinction.

## 13. Endpoint selectors and posterior comparison

For bounded regular initial and terminal flight-state selectors, the overlap is weighted before the age integration. Integrating in the centered roof variable factors the limiting amplitude into the product of the two stationary selector means. This gives a selected local law and a positive selected denominator when that product is uniformly positive.

The class includes jointly continuous bounded families and specified indicator classes with null boundaries and uniform exceptional-neighborhood control. It does not include every arbitrary path-dependent rare event. This limitation is stated correctly.

Separately, the inherited positive finite-band likelihood approximates the original event indicator in unnormalized source total variation with error `C/B`. Choosing

\[
 B_m=m^{P+3/2}
\]

and dividing by the newly established `m^{-3/2}` denominator gives normalized total-variation error `O(m^{-P})`. Total variation then controls every bounded measurable test on the unchanged trajectory space. This arbitrary-test conclusion is a comparison of posterior measures; it is not a Gaussian-amplitude theorem for an arbitrary selector.

The distinction between these two weighted statements is important and is maintained in revision 34.

## 14. Relation to prior local-limit theory

The manuscript cites three bodies of work directly relevant to the new leading theorem:

- the local central limit theorem for the planar Lorentz process;
- anisotropic-space local limits for cell indices with endpoint observables;
- abstract local central limit theorems for hyperbolic suspension flows, including finite-horizon Sinai billiards.

Revision 34 does more than quote those results: it constructs an exact bounded collision twist containing the roof, verifies action estimates in the collision norms, obtains radius-uniform compact-frequency control, retains the stationary age and both cell offsets, and evaluates a joint displacement/collision-count singleton. These are genuine technical additions.

For a top-four submission, however, the novelty comparison must be considerably sharper. The current paragraph says that a spatial local theorem is not simply cited as a theorem for the three-coordinate record. That is true but not enough. The manuscript should give a theorem-by-theorem comparison explaining

1. whether the fixed-`R` stationary conclusion follows from an existing abstract suspension local limit theorem after checking its hypotheses;
2. which part of the new proof is required specifically for uniformity in `R`;
3. whether the endpoint-selected statement is already implicit in a known mixing local limit theorem;
4. whether the collision-count coordinate introduces a new arithmetic group or is a standard suspension coordinate;
5. which exact raw or singleton topology is stronger than prior formulations;
6. why the resulting theorem has significance beyond the particular triangular family.

Without this comparison, it is difficult to separate a technically demanding parameter-uniform verification from a genuinely new general principle. That distinction is central to a four-journal significance judgment.

## 15. The unresolved four-coordinate return problem

The source metadata correctly leaves the following claims false:

- `full_raw_return_LLT_proved`;
- `common_pointwise_return_correction_proved`;
- `full_return_complement_proved`;
- `microscopic_conditional_path_bridge_proved`;
- `arbitrary_selected_path_Gaussian_amplitude_proved`.

The new collision observable is bounded because it records one physical collision. The actual induced return record includes a discontinuous section count and unbounded return blocks. The age-overlap positivity regularizes the physical fixed-count event but does not automatically regularize the four-coordinate return density. Therefore the stationary theorem cannot be cited as completion of Theorem `thm:LLT` for `J_{n,R}`.

This is not a minor presentational issue. The title still emphasizes collision records and raw local inversion, and a large part of the article develops periodic arithmetic, critical-edge extraction, coherent return corrections, and return-frequency splicing for precisely that unresolved theorem.

A future submission should make an explicit editorial choice:

1. **Complete the four-coordinate return LLT.** Then the physical local theorem becomes an additional route and application inside a genuinely unified paper; or
2. **Rebuild the paper around the stationary microscopic theorem.** In that case the return programme should be presented as a clearly delimited secondary theory or companion, and the title, abstract, theorem hierarchy, and significance discussion should reflect the theorem actually completed.

This is not a recommendation to delete mathematical work. It is a recommendation to align the submitted theorem, narrative, and venue claim.

## 16. Exposition and architecture

The revision-34 front matter is substantially improved. It names the two records immediately, states one leading theorem, explains the fixed-band mechanism, and explicitly separates the physical theorem from the return problem. Retaining the A--X synopsis in an appendix is preferable to placing it before the proof.

The body remains unusually long and historically layered. Many modules were created to close successive interfaces that the new stationary proof now bypasses. A publication version needs a dependency graph distinguishing

- essential inputs for the stationary theorem;
- independent results about the return record;
- conditional interfaces for the still-open raw return theorem;
- historical or superseded proof routes.

The present `PROOF_LEDGER.md` is helpful, but the article itself should permit a reader to verify the leading theorem without navigating the full historical pipeline. One possible solution is a self-contained main part for the stationary theorem and a companion or clearly separated part for the return programme. The mathematical content need not be weakened or discarded.

## 17. Required changes before a future top-four resubmission

### R1. Obtain an independent specialist proof audit

At minimum, a billiards/anisotropic-spaces expert should audit:

- the backward-flight partition and piecewise multiplier conditions;
- the action estimate on matched connectors;
- the weighted weak, stable, and unstable Lasota--Yorke inequalities;
- the equivalent-norm/quasi-compactness argument;
- the bounded-density representation of peripheral eigendistributions;
- the parameter-uniform compact-frequency gap;
- the varying endpoint-overlap test.

The paper should record the scope of that audit accurately. A successful source build is not such an audit.

### R2. Expand module 69 into a fully checkable operator proof

State the exact anisotropic norms and every parameter restriction used. Reproduce the weighted Jacobian/length sums needed for the three Lasota--Yorke estimates. Verify the multiplier partition conditions and matched-connector regularity without relying on prose analogy. Make the dependence on the fixed frequency band explicit at each step.

### R3. Give a precise prior-art comparison

Compare the leading theorem statement, not only the method, with the Lorentz-process local CLT, endpoint mixing local limits, and suspension-flow local central limit theorems. Identify which fixed-parameter conclusions are known, which uniform-in-radius conclusions are new, and which exact singleton or selector topology is stronger.

### R4. Align the article with its proved endpoint

Either complete the four-coordinate return LLT or reorganize the submission so that the stationary microscopic local law is unmistakably the main theorem and the incomplete return LLT is a separate programme. The title and abstract should not leave a general reader uncertain about which raw local theorem has actually been proved.

### R5. Separate regular endpoint amplitudes from arbitrary posterior tests

Retain the current distinction. State every regularity, null-boundary, and positive-mean condition for the selected local law. Do not infer a Gaussian amplitude or positive denominator for an arbitrary bounded path selector merely from total-variation comparison.

### R6. Preserve the order of limits visibly

Every use of the compact-frequency theorem should continue to fix the band first. The positive-envelope squeeze should state the quantifier order explicitly. No future quantitative claim at `B=B_m` should be made without a proved growth estimate for the spectral constants.

### R7. Streamline the proof dependency structure

Provide a short, article-level route from the collision spectrum to the leading theorem, with exact references to the inherited inputs. Move historical derivation material away from the main logical path while preserving it in the repository or a companion source.

### R8. Report reproducibility evidence exactly

Record the successful response-branch exact-SHA run and its artifact. If a separate referee-copy execution is desired, trigger and record it; otherwise state simply that the copy ref points to the already qualified SHA. Continue to distinguish finite diagnostics, native typesetting, and mathematical proof verification.

## 18. Top-four significance assessment

Revision 34 materially changes the status of the project. The original stationary singleton is no longer represented only by an unevaluated Fourier ledger. The article now contains an unconditional local limit theorem with a positive denominator and a source-level conditioning consequence.

That theorem combines several attractive ingredients:

- an exact image-side unsmoothed collision twist;
- an action-based control of long roof phases;
- a compact-frequency spectral gap uniform in a moving billiard family;
- positive Fourier envelopes rather than an unjustified growing-band substitution;
- endpoint local measures;
- exact stationary age integration with cell corrections;
- normalized posterior approximation on the original trajectory space.

These constitute a strong specialist contribution if the continuum operator proof survives independent verification.

At the requested four-journal benchmark, however, one normally expects either a completed theorem of broad significance or a general principle whose influence clearly extends beyond the model. The manuscript currently proves a specialized physical local theorem for one triangular Lorentz family while retaining an incomplete, more ambitious four-coordinate return theorem as its organizing programme. It does not yet establish that the uniform stationary result lies beyond existing abstract flow local-limit frameworks in a way commensurate with *Annals*, *Acta*, *Inventiones*, or *JAMS*.

A verified and sharply focused version could merit serious consideration by a strong journal in dynamics, probability, or mathematical physics. Completion of the raw return theorem, or abstraction of the image-side action method into a general local-limit principle for parameter families of singular hyperbolic flows, would materially change the top-four assessment.

## 19. Final recommendation

**Reject in the present form at the requested top-four benchmark.**

The recommendation should be read together with the following positive mathematical conclusion:

- revision 34 is not a cosmetic revision;
- it appears to close the stationary physical middle-frequency obstruction identified in the revision-33 report;
- it proves a credible microscopic stationary local law rather than merely a reconstruction or conditional criterion;
- no decisive error was found in the audited new chain;
- the remaining objections concern specialist verification, paper architecture, novelty/significance, and the still-open four-coordinate return theorem.

I would welcome a substantially reorganized and independently audited resubmission, especially one that either completes the return-density theorem or presents the stationary local law as a focused theorem with a precise general and literature-level significance claim.
