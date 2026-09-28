# External top-four referee report on A2 v18

**Manuscript:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v18-stable-intrinsic-reconstruction-2026-09-28`  
**Reviewed commit:** `0708f67908355e9881d1993b42bcc698b0c350c6`  
**Reviewed tree:** `2e63e7f7cb8c73cda6ce8436bf1f716da3358f78`  
**Manuscript directory:** `papers/A2-v18-stable-intrinsic-reconstruction`  
**Date:** 28 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

This is a materially stronger manuscript than the version covered by the frozen v16 report. Version 18 does not merely repackage the earlier jet recursion. Its principal new observation is that two strictly active endpoint-density functions at two absolute times eliminate the unknown flux factor and recover the entire stationary two-flight action on a fixed endpoint rectangle. The diagonal first and second derivatives of that action then give explicit formulas for both boundary curvatures. This yields smooth local rigidity without analyticity, reflection symmetry, a supplied area, a supplied gap, or an increasing contact-jet recursion. The finite-bin theorem also replaces the previous order-dependent regularization by a fixed conditional exponent on a quantitatively analytic and asymmetric prior class.

On the new v18 core that I audited, I found no fatal counterexample. The two-window quotient, stationary Schur complement, source and opposite curvature formulas, foot-point speed, local conditional Lipschitz estimate, quadratic cell-average reconstruction, histogram rate balance, image synchronization, and rank-two lattice inversion are internally coherent in their stated scope. Independent exact and nonlinear numerical diagnostics accompanying this report support those finite identities.

The negative recommendation is therefore not a claim that v18 is mathematically empty or obviously false. It is a top-four editorial judgment. The central data are an unusually rich, selected, endpoint-arclength marked subprobability law. Once two full endpoint densities are supplied, the action is recovered by an elementary affine elimination. The subsequent geometric inverse is elegant, but it belongs conceptually to travel-time/lens/scattering inverse geometry rather than establishing rigidity from a standard billiard spectral invariant. The whole-table result additionally retains a designed channel network, obstacle and contact-occurrence labels, integer copy labels, two lattice-cycle labels, onset brackets, uniform analytic strip bounds, quantitative asymmetry margins, and a compact physical prior. These hypotheses make a serious conditional inverse theorem, but not, in my judgment, the exceptional conceptual advance required by the four journals named above.

I would regard the two-window local inverse, after a full proof and literature review and after repairing the source-delivery defects, as potentially suitable for a strong specialist journal. At the requested benchmark, another incremental revision is not the appropriate recommendation.

## 2. Frozen source and relation to the previous report

I reviewed the head of `revision/a2-v18-stable-intrinsic-reconstruction-2026-09-28`, namely commit

`0708f67908355e9881d1993b42bcc698b0c350c6`

with tree

`2e63e7f7cb8c73cda6ce8436bf1f716da3358f78`.

Its parent is the v17 author commit

`2e01331b1c9e20cf9d11d330fab0a163555aec6b`.

The latest frozen external report cited by the author is the v16 review at

`62c98e9178c5571a19afaccf8b5e67fc892c6c1e`.

No `revision/a2-v19...` branch existed when this review branch was created. The present review branch starts directly from the v18 author commit. It adds files only under

`reviews/a2-v18-external-harsh-top4-rereview-2026-09-28/`.

No manuscript source, author revision branch, previous report, or unrelated paper is changed by this review.

The main new mathematical source is `core/13_two_window_inverse.tex`, together with the new overview in `core/01_full_law_overview.tex` and the revised v18 front matter. The v17 moment-compressed inverse, registered and unregistered assembly theorems, older finite-window regularization, count-fiber statements, and relative-law supplement remain active.

## 3. Summary of the new v18 theorem

For one selected isolated normal channel and one itinerary orientation `b,o,b`, let `s,t` be intrinsic arclength at the first and last impacts and let `u(s,t)` be the stationary intermediate impact. The two-flight action is

\[
\mathcal W(s,t)=D(s,u(s,t))+D(t,u(s,t)).
\]

On a strictly active endpoint rectangle, the endpoint density at absolute time `T` is

\[
f_T(s,t)=\frac{-\mathcal W_{st}(s,t)}{2\pi A}
                 (T-\mathcal W(s,t)).
\]

Consequently two times `T_2>T_1` give

\[
\mathcal W=
 \frac{T_1 f_{T_2}-T_2 f_{T_1}}{f_{T_2}-f_{T_1}},
\qquad
A=\frac{(T_2-T_1)(-\mathcal W_{st})}
        {2\pi(f_{T_2}-f_{T_1})}.
\]

On the diagonal put

\[
\ell(s)=\frac12\mathcal W(s,s),\qquad
 a(s)=\mathcal W_s(s,s),\qquad
 v(s)=\sqrt{1-a(s)^2}.
\]

The source and opposite curvatures are then

\[
k(s)=\frac{\mathcal W_{ss}(s,s)-\mathcal W_{st}(s,s)
                  -v(s)^2/\ell(s)}{v(s)},
\]

and

\[
k_o(u(s))=\frac1{\ell(s)}
 \left(\frac{v(s)^2}{-2\ell(s)\mathcal W_{st}(s,s)}-1\right).
\]

A Frenet reconstruction recovers the source arc, and the nearest-point identity recovers the opposite arc and its relative placement. The gap is `\mathcal W(0,0)/2`.

For finite acquisition, square-cell probabilities on two active endpoint histograms reconstruct each density in `C^2` with error

\[
C\{h^\beta+\epsilon h^{-4}\}.
\]

Uniform analyticity propagates the local arc error to the complete obstacle images with a two-constants loss `e^\theta`; quantitative asymmetry synchronizes independently reversed edge reconstructions; and two independent marked lattice cycles recover the lattice. Balancing `h` yields the fixed class-dependent exponent `\beta\theta/(\beta+4)`.

This is a genuine conceptual change from the previous all-order coefficient route.

## 4. Correctness audit of the local inverse

### 4.1 Density and two-window elimination

The density formula is consistent with the intrinsic collision-section symplectic measure. In arclength and conjugate momentum coordinates the section factor is `-\mathcal W_{st}\,ds\,dt`; the free residual time before the first impact contributes `(T-\mathcal W)_+`; normalization contributes `1/(2\pi A)`. On a rectangle strictly inside the active support, the positive-part operation is inactive and the dependence on `T` is affine.

Writing

\[
w=-\mathcal W_{st}/(2\pi A),
\qquad f_{T_j}=w(T_j-\mathcal W),
\]

immediately gives

\[
f_{T_2}-f_{T_1}=(T_2-T_1)w>0
\]

and the displayed quotient for `\mathcal W`. The formula does not insert an unobserved onset. It uses the absolute times and two complete density functions on a rectangle known to be active. The area formula then follows from the recovered mixed derivative.

Equality of the subprobability measures determines the continuous density representative uniquely on the smooth physical class, so there is no hidden representative ambiguity.

### 4.2 Stationary Schur complement and curvature identities

At the diagonal nearest point let `e=(x-y)/\ell`, let `T,N` be the source Frenet frame, and write

\[
e=aT+vN.
\]

With the opposite tangent oriented continuously so that `T\cdot T_o=v`, direct differentiation gives

\[
D_{ss}=v^2/\ell+kv,\qquad
D_{su}=-v/\ell,\qquad
D_{uu}=1/\ell+k_o.
\]

Eliminating the stationary intermediate variable gives

\[
\mathcal W_{ss}=D_{ss}-\frac{D_{su}^2}{2D_{uu}},
\qquad
\mathcal W_{st}=-\frac{D_{su}^2}{2D_{uu}}.
\]

Subtracting the two equations recovers the source curvature; solving the second recovers the opposite curvature. The signs are correct for the external dispersing geometry. At the normal origin these formulas reduce to the retained quadratic Hessian identities.

Differentiating the nearest-point equation gives

\[
u'(s)=\frac{v(s)}{1+\ell(s)k_o(u(s))}>0,
\]

so the recovered opposite image is an actual regularly parametrized arc rather than only a set. I found no defect in this reconstruction.

### 4.3 Reflection ambiguity

A simultaneous replacement `(s,t)\mapsto(-s,-t)` reflects the reconstructed pair. Because both density functions use one coherent edgewise reversal, the quotient is equivariant under this operation. There is no independent reflection of the two members of a pair. The stated local ambiguity is therefore the natural common Euclidean isometry ambiguity.

## 5. Correctness audit of stability and finite acquisition

### 5.1 Conditional local Lipschitz estimate

With a positive lower bound for `f_{T_2}-f_{T_1}`, multiplication, division, and differentiation are locally Lipschitz in `C^2`; hence the action error is controlled in `C^2`. The curvature formulas use only first and second derivatives of the action and positive geometric margins.

The source arc follows from continuous dependence of the Frenet system. For the opposite arc, the proof correctly avoids differentiating the foot-point formula twice and thereby demanding a third action derivative. It instead integrates the positive speed `u'(s)` and then invokes the uniform physical `C^3` boundary prior to compare opposite curvature in common intrinsic arclength coordinates. Under those explicit class assumptions the `C^2` arc estimate is plausible and internally consistent.

The dependence on the physical `C^3` prior, active-margin lower bounds, twist margin, and time-separation margin is essential. The abstract phrase “Lipschitz in a two-derivative density norm” should not be read as an unconditional mapping theorem on all `C^2` densities.

### 5.2 Cell-average reconstruction

The one-dimensional averages of `1,z,z^2` on three adjacent normalized cells form an invertible matrix. Its tensor square recovers every coordinatewise quadratic polynomial on a `3\times3` cell block. For a `C^{2,\beta}` density, the Taylor remainder gives a second-derivative bias `O(h^\beta)`. An absolute cell-probability error `\epsilon` becomes an average-density error `\epsilon h^{-2}` and two derivatives cost another `h^{-2}`, yielding `O(\epsilon h^{-4})`.

A smooth partition of unity does not change this order: derivatives falling on the partition are offset by the corresponding lower-order local approximation bounds. The resulting estimate

\[
\|\widehat f-f\|_{C^2}
 \le C(h^\beta+\epsilon h^{-4})
\]

is therefore credible.

### 5.3 Preparation count

One endpoint observation at a fixed time is a single multinomial outcome, so the same sample simultaneously supplies all cell indicators. Hoeffding bounds and a union bound over `O(h^{-2})` cells introduce only `\log(h^{-2})`, not an additional multiplicative `h^{-2}` in the number of phase preparations. The stated preparation upper bound is consistent with this observation model.

The reported data dimension nevertheless grows like `h^{-2}` per histogram. “Two windows” means two increasingly fine two-dimensional histograms, not two scalar observations.

### 5.4 Pilot

The pilot uses a fixed positive threshold and a prior onset bracket to find a time a controlled positive distance after onset. It is not an `\epsilon`-accurate onset estimator and need not be: the quotient uses absolute times, and the pilot only has to place both histograms on a common strictly active rectangle. The proof does not rely on global monotonicity of the three-impact probability.

## 6. Global assembly audit

The full-law theorem removes continuous cross-channel registration and relative edge signs for quantitatively asymmetric obstacles. It does not remove all marks. The input still includes:

- a selected connected channel graph visiting every labelled obstacle;
- obstacle labels and contact-occurrence labels;
- integer lattice-copy labels on edges;
- two independent fundamental-cycle labels;
- known onset brackets;
- common analytic-strip and geometry bounds;
- a quantitative rotation and reflection margin `\eta`;
- a compact physical prior class.

Given those marks, the assembly mechanism is coherent. Each edge reconstructs a complete pair image up to its own simultaneous reflection. Matching the complete source image to an already placed asymmetric obstacle determines the Euclidean placement uniquely; changing the edge representative by reflection cancels through this unique matching and does not change the placed partner. Induction along a spanning tree places all representative obstacles.

For a non-tree edge, the translated target image determines a displacement vector. Two independent integer labels give

\[
L=[d_{e_1}\ d_{e_2}]\mathsf K^{-1}.
\]

The quantitative support-function margins exclude the incorrect reflection component and control the rotation angle under noise. I found no internal contradiction in this synchronization argument.

The result should nevertheless be described as rigidity of a heavily marked local-scattering network, not as rigidity from an ordinary unmarked billiard invariant.

## 7. The closest missing comparison

The manuscript compares the new observation chiefly with marked-length rigidity for dispersing billiards. Those comparisons are useful but not sufficient for v18.

The central v18 step recovers a local generating/travel-time action as a function of two boundary coordinates. This places the new theorem conceptually close to the boundary-distance, lens, scattering-relation, and obstacle travelling-time rigidity literature. In those subjects, endpoint travel times and their tangential derivatives are the natural data, and local convexity is a standard rigidity mechanism.

At minimum the paper should compare its information set and local inverse with:

- P. Stefanov, G. Uhlmann, and A. Vasy, *Local and global boundary rigidity and the geodesic X-ray transform in the normal gauge*, arXiv:1702.03638;
- T. Gurfinkel, L. Noakes, and L. Stoyanov, *Travelling Times in Scattering by Obstacles in Curved Space*, arXiv:2003.12261, J. Differential Equations 2020.

These works do not obviously subsume the present two-reflection billiard calculation. Conversely, citing only marked-length papers makes the quotient recovery of `\mathcal W` appear more conceptually isolated than it is. A top-four novelty claim requires a precise theorem-level explanation of what the two-window Liouville-density observation adds beyond established travel-time/lens/scattering data and why the explicit curvature reconstruction is not an instance of a known local inverse-geometry principle.

I did not perform an exhaustive priority search. The omission is serious because it concerns the nearest information category introduced by v18.

## 8. Remaining top-four objections

### 8.1 The observation almost explicitly contains the action

Once two full endpoint densities at two times are supplied, the main action is recovered by an elementary affine quotient. The hard geometric part is the curvature reconstruction and global assembly, but the information content is already close to local travel-time data. This is much richer than counts, ordinary marked lengths, or a finite collection of scalar statistics.

A result may be important with rich data, but the manuscript cannot simultaneously emphasize “two windows” and rely on readers to overlook that each window is a full two-dimensional density function, or an increasingly fine histogram in the finite experiment.

### 8.2 The fixed exponent is highly conditional

The exponent `\beta\theta/(\beta+4)` is independent of a contact-jet order, which is a real improvement. It is not universal. The harmonic-measure exponent `\theta`, all constants, active rectangles, histogram regularity, and synchronization stability depend on the uniform analytic strip, global bounds, channel margins, onset brackets, and quantitative separation from every Euclidean symmetry.

This should be advertised as a conditional compact-class regularization theorem. It is not a stable inverse on the natural unconstrained class of analytic dispersing tables.

### 8.3 Count-only rigidity remains open

The manuscript correctly distinguishes full endpoint laws from count data and retains finite and formal count fibers. It does not prove exact analytic nonrigidity for complete count germs, nor asymmetric whole-table rigidity from counts. The strongest theorem therefore changes the sensor rather than resolving the previously isolated count-only inverse problem.

### 8.4 Discrete registration has been reduced, not eliminated

Continuous contact registration and relative signs are no longer supplied for asymmetric obstacles. However, the graph, obstacle labels, occurrence labels, integer copy labels, and two independent lattice-cycle labels remain external marks. These are substantial global combinatorial inputs.

### 8.5 No sharp statistical theory

The finite-bin result is a constructive upper bound. No matching lower bound, minimax exponent, optimal histogram design, or comparison with alternative full-trajectory sensors is given. The statistical result supports operationality; it is not an independent top-four contribution.

### 8.6 The paper remains an accumulated programme

The primary article retains the moment-compressed inverse, two different global assembly theorems, two different finite-data regularizations, count-fiber results, physical finite-jet experiments, and a large supplementary relative-law programme. Version 18 has a much clearer central theorem than v16, but the submission still reads as a repository-wide research programme rather than a final paper organized around one decisive result.

## 9. Source and reproducibility defects

The v18 commit honestly calls itself a mathematical checkpoint and does not claim a hosted build. The current source nevertheless contains a purported exact-checkout validator, `tools/validate_v18.py`, whose execution cannot close on the reviewed commit as stored:

1. it reads `SOURCE_PINS.json`, but that file is absent from the v18 manuscript root;
2. there is no `.github/workflows/a2-v18-verify.yml` on the reviewed branch;
3. GitHub reports no workflow run whose head SHA is `0708f67908355e9881d1993b42bcc698b0c350c6`;
4. the retained driver still carries v17 schema and labels, although the v18 wrapper is intended to nest it.

The mathematical source can still be read and reviewed. What cannot currently be claimed is an authenticated, exact-commit, full-package qualification of v18. Before submission the authors should add the missing pins, add a read-only v18 workflow, execute it on the exact author SHA, and publish the resulting primary and supplementary build receipts. Historical v17 receipts must not be relabelled as v18 evidence.

## 10. Required corrections before any resubmission

1. Add a theorem-level comparison with boundary-distance, lens, scattering-relation, and obstacle travelling-time rigidity, not only marked-length billiard papers.
2. Make “two endpoint density functions / two growing histograms” prominent every time the phrase “two windows” appears in a headline statement.
3. State the `C^3` physical prior and all active/twist/time margins directly in the local Lipschitz proposition, not only in preceding prose.
4. Keep the class dependence of `\theta`, the asymmetry margin, analytic strip, onset brackets, selected channel network, and lattice-copy labels visible in the abstract and main theorem summary.
5. Do not describe the unregistered theorem as removing all registration; it removes continuous cross-edge registration while retaining substantial discrete marking.
6. Preserve the explicit disclaimer that no exact analytic count-only rigidity or nonrigidity theorem follows.
7. Separate or substantially compress the older moment, count, statistical, and relative-law projects so the new full-law inverse is the unmistakable main result.
8. Repair the v18 source pins and exact-SHA build workflow, then archive the actual logs and PDFs.
9. Give a precise comparison between the old order-dependent regularization theorem and the new histogram theorem, and decide which belongs in the main article.
10. Avoid claiming top-four significance from the fixed statistical exponent unless a sharp lower bound or a substantially more natural observation model is established.

## 11. Independent diagnostics

The accompanying `verify_review.py` imports no author verification module. The exact standard-library suite performs 11,525 rational checks:

- 900 source-curvature identities;
- 900 opposite-curvature identities;
- 900 foot-speed identities;
- 900 positivity/twist margin checks;
- 3,000 bivariate two-window quotient coefficient identities through total degree three;
- 300 flux-factor recoveries;
- 300 coherent-reversal checks;
- 9 cell-average matrix inverse checks;
- 81 tensor polynomial-reproduction checks;
- 6 histogram rate-balance identities;
- 4,224 rank-two lattice recovery identities;
- 5 Fourier asymmetry obstruction checks.

A separate nonlinear stationary-ray diagnostic used five asymmetric quartic graph pairs and nine diagonal points per pair. The 90 independently differentiated curvature comparisons had maximum absolute error approximately `1.29e-8`.

These computations test finite formulas only. They do not certify the density derivation, uniform physical branch, analytic continuation, compact-class estimator, retained supplement, literature priority, or journal significance.

## 12. Final verdict

**Response to the frozen v16 report:** substantial. Version 18 supplies a genuinely new full-law route, removes the increasing-order instability from the main local inverse, gives a finite histogram realization, and combines it with the unregistered image-matching mechanism.

**Mathematical audit:** no fatal counterexample found in the new v18 core; the main displayed formulas and finite reconstruction mechanism appear sound under their stated physical and prior margins.

**Information content:** the theorem uses a selected intrinsic endpoint-density law that is far richer than counts or ordinary marked lengths and that almost explicitly encodes the local generating action.

**Global scope:** whole-table stability remains conditional on a strongly marked network and stringent analytic/asymmetry priors.

**Editorial assessment:** technically serious and potentially publishable in a strong specialist venue after restructuring, literature repair, and exact-source validation, but not at the exceptional conceptual threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.**
