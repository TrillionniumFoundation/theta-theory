# External top-four referee report on A2 v32

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v32-adaptive-scalar-boundary-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v32-referee-copy-2026-10-04`  
**Reviewed commit:** `eeb171d4e00242c9813c10e2124556b2cee480d3`  
**Reviewed repository tree:** `1c36f869ff4e875a0c6c8ecabbd8a38169e47c66`  
**Native paper tree:** `2a7d949f43dcb7b84d4a85ef8a4436349f615493`  
**Mathematical checkpoint:** `7044eb0a7e4bfe9c33f67c8d93e006f02d09cedc`  
**Controlling preceding report:** `f2e2a13a9a742c412a4b1a59b43388a2ba385bda`  
**Manuscript directory:** `papers/A2-v32-adaptive-scalar-boundary`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 32 is a genuine and substantial mathematical advance over the reviewed v31 manuscript. It answers the most concrete open criticism in the previous report. The old finite construction measured a uniformly accurate occupation field on a fine two-dimensional grid and had no matching statistical lower bound. The present revision replaces that design by a fixed coarse acquisition, finitely supported local Bellman queries, robust radial bisection, and one-dimensional polynomial boundary reconstruction. It then constructs a physical `C^{6,\beta}` packing and proves a binary-transcript lower bound with the same power
\[
        \nu^{-1/(4+\beta)}
\]
as the attempted-bit upper bound, up to logarithmic factors.

On the new v32 core audited in detail, I found no fatal counterexample. In particular, the reciprocal endpoint identity, calibration tube estimate, fixed-depth killed-compass inverse, coarse component acquisition, bisection with arbitrary labels in a boundary layer, radial regularity without derivative loss, seven-point interpolation, protected-patch period locking, physical bump packing, and binary decision-tree argument are coherent under the hypotheses stated. The exact-source fifteen-document workflow also passes at the reviewed SHA. The negative recommendation is therefore not based on a known false central theorem or on a source-delivery defect.

The remaining objection is editorial and conceptual. The theorem is an active, precisely calibrated input-output result. Although each attempted preparation returns one bit, the controller chooses localized launch distributions at adaptively selected real-valued positions, prescribes the four-atom displacement law and its translated reciprocal reverse law, and maintains position/time/angle errors of order
\[
        \nu^{(6+\beta)/(4+\beta)}.
\]
Input precision, apparatus motion, calibration production, and arithmetic bit complexity are not included in the attempted-bit count. Once the reciprocal measurements have been converted to a constant-accuracy approximate membership query, the upper-bound geometry is a refined instance of active smooth-boundary estimation. The lower bound is the corresponding one-dimensional Hölder metric-entropy packing combined with binary-tree counting. Their synthesis in this collision model is meaningful and technically careful, but the main abstract engines are classical.

The global conclusion also remains conditional on a bounded periodic presentation, strong curvature/separation/smoothness bounds, a fixed protective aperture, and a **known positive nonperiod-patch margin** for uniform finite period decisions. The result neither infers crystallinity from an arbitrary configuration nor proves rigidity from passive trajectories, count germs, marked lengths, or spectra.

In my judgment v32 is a serious and potentially strong specialist-journal paper, and it is materially stronger than v31. It does not, however, reach the exceptional naturality, breadth, or conceptual transformation expected at the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

The two v32 branch names listed above resolve to the same author head
`eeb171d4e00242c9813c10e2124556b2cee480d3`
with repository tree
`1c36f869ff4e875a0c6c8ecabbd8a38169e47c66`.

Its parent is the mathematical checkpoint
`7044eb0a7e4bfe9c33f67c8d93e006f02d09cedc`.
That checkpoint is based directly on the latest v31 external-review head
`f2e2a13a9a742c412a4b1a59b43388a2ba385bda`,
which reviewed v31 author commit
`27d109b0eba6a03d453834ef9da9418446ac637d`.

The exact complete v31 manuscript is preserved under
`papers/A2-v32-adaptive-scalar-boundary/retained/v31`
at tree
`ff74e5124141dc46b0f08f7e38a5cf258b87e642`.
Its active v31 core is preserved at tree
`aa9026847310ecd9205fe631b5ed85aa141b70ed`.

No A2 revision branch later than v32 existed when this review was frozen. The present review branch starts directly from the v32 author head and adds files only under
`reviews/a2-v32-external-harsh-top4-rereview-2026-10-04/`.
No author source, prior report, revision branch, retained volume, workflow, or unrelated paper is modified.

The active v32 primary consists of:

- `core/00_setting.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/05_comparison.tex`.

I also inspected the response to referees, proof/history/literature ledgers, source pins, submission map, current validation tools and receipts, exact-SHA workflow, hosted run, retained v31 source, and the complete v31 external report.

## 3. Information model and theorem package

For a nominal displacement `a`, one attempted command returns one exactly when a **free** start at `q` has a first collision on the unreflected segment `[q,q+a]`. A solid start and a free miss both return zero, and both remain in the denominator.

For a localized start density `f_{x,\sigma}` and the compass law
\[
 \rho=\tfrac14(\delta_{te_1}+\delta_{-te_1}
                    +\delta_{te_2}+\delta_{-te_2}),
\]
the forward experiment attempts `(q,a)`. The reciprocal experiment uses the same nominal joint law and attempts `(q+a,-a)`. Only the two pooled means are used. The pointwise identity
\[
 B_a(q)-B_{-a}(q+a)
       =\mathbf 1_{\mathcal O}(q+a)-\mathbf 1_{\mathcal O}(q)
\]
therefore gives
\[
        g_\sigma=(T-I)u_\sigma,
        \qquad u_\sigma=\kappa_\sigma*\mathbf1_{\mathcal O}.
\]

The first principal theorem computes isolated approximate-membership queries from these pooled means, obtains coarse component hulls and interior centers, performs adaptive radial searches, and reconstructs every required boundary. With `s=6+\beta`, it takes
\[
 h\asymp \nu^{1/(s-2)},\qquad \sigma\asymp h^s,
\]
and proves
\[
 J_\nu\le C\nu^{-1/(s-2)}\log(C/\nu),
\]
\[
 N_\nu\le C\nu^{-1/(s-2)}
            \log(C/\nu)\log(C/(\nu\delta)).
\]
The geometric loss is `C^2` boundary error together with matched primitive-period and free-area errors. Exact rational period relations and the primitive orbit count are discrete outputs; Euclidean period coordinates remain estimates.

The second principal theorem constructs a fixed physical subclass with
\[
        \log M_\nu\asymp \nu^{-1/(s-2)}
\]
pairwise disjoint accuracy balls. Since at most `N` binary table-dependent outputs generate at most `2^N` transcripts after controller randomness is fixed, uniform success probability at least `3/4` forces
\[
        N\ge c\nu^{-1/(s-2)}.
\]

## 4. Audit of the reciprocal local query

### 4.1 Reciprocal balance

The endpoint case distinction is exact. If both endpoints are free, a segment and its reverse either both meet a solid or both miss. If exactly one endpoint is solid, the command started in the solid is zero and the command started at the free endpoint hits. If both endpoints are solid, both commands are zero. This proves the displayed difference identity without conditioning on a free start or a successful collision.

The use of the same nominal **joint** forward law and translated reverse law is essential. Independently selecting only the reverse direction distribution would not give the same cancellation.

### 4.2 Calibration

The swept set for one convex component is `C+[-a,0]`. Bounded position and displacement errors can change the solid-start or swept-set indicators only in boundary tubes whose local area is `O(\sigma r)`, where
\[
        r=\ell+\tau+t\alpha.
\]
Packing from the component-separation prior bounds the number of contributing components. Multiplication by the localized density bound `O(\sigma^{-2})` gives bias `O(r/\sigma)`. The argument permits conditionally chosen, non-mean-zero bounded errors and includes tangencies.

I found no missing rare-event factor. Each pooled mean is estimated to a fixed absolute accuracy, so the number of Bernoulli attempts per dependency center is logarithmic in the allocated confidence and independent of `\sigma`. The price paid for localization appears instead in the required controller calibration.

### 4.3 Killed compass inverse

The four-atom walk is centered and has second moment `t^2`. Before it reaches the zero set of `u_\sigma`, it remains in one enlarged component, because distinct enlarged components are separated by more than one step. Bounded stopping of
\[
        |X_n-x|^2-nt^2
\]
gives the uniform mean-exit bound. Markov's inequality in blocks gives a geometric survival tail.

The killed Bellman recursion
\[
        V_{n+1}=\max(0,T^WV_n-g_\sigma)
\]
is monotone and bounded above by `u_\sigma`. Along the stopped path, killing at the outer aperture creates no discrepancy, because the complete positive component and its first exit location are contained in the fixed aperture. The error is dominated by the killed semigroup applied to the occupation and hence by the survival tail.

A target value at depth `n_*` depends only on the finite diamond
\[
        x+t(i,j),\qquad |i|+|j|\le n_*.
\]
Thus a constant number of spatial centers, depending on the prior but not on `\sigma` or `\nu`, suffices for each approximate-membership query. This is the central mechanism behind the improved exponent, and I found it sound.

## 5. Audit of adaptive boundary reconstruction

### 5.1 Coarse acquisition

The curvature upper bound supplies a uniform interior rolling radius. At one fixed scale, grid points well inside a body are labelled inside, points outside its enlarged body are labelled outside, and only a fixed boundary tube is indeterminate. Separation prevents clusters from different components from joining.

The convex hulls approximate the complete protected components to fixed Hausdorff error. Computing an inscribed disk in each polygon gives a center with a uniform inball. Because both the true component and the hull contain this inball, Hausdorff error controls their radial functions uniformly. The resulting radial brackets can be made shorter than the inter-component separation and hence cannot encounter another obstacle at the later fine scales.

### 5.2 Bisection with arbitrary boundary-layer labels

The bisection proof does not assume monotone noisy labels. A positive label at radial coordinate `a` implies only
`a\le R_C+A\sigma`; a zero label implies only
`a\ge R_C-A\sigma`.
The relaxed interval invariant is preserved under either permitted label. After `k` queries the midpoint error is
\[
        A\sigma+2^{-k-1}w_0.
\]
This correctly handles adversarial or history-dependent outputs inside the indeterminate layer.

### 5.3 Radial regularity and interpolation

A superficial conversion from a `C^{6,\beta}` support function to a radial function appears to lose one derivative. The manuscript supplies the needed cancellation:
\[
        R'=R(p'/p)\circ\theta.
\]
Since the inverse angle map is uniformly regular, the radial function remains `C^{6,\beta}`.

Degree-six interpolation on seven angular samples, patched by a fixed smooth partition of unity, gives
\[
 \|\widehat R-R\|_{C^j}
       \le C(h^{s-j}+eh^{-j}),\qquad j\le3.
\]
With radial-value error `e=O(\sigma)=O(h^s)`, the reconstructed support has `C^2` error `O(h^{s-2})`. The polar convexity expression
\[
        R^2+2(R')^2-RR''
\]
retains a positive margin, so the output is an actual smooth strictly convex body rather than only a point cloud.

### 5.4 Complexity

There are `O(h^{-1})` angular directions and `O(\log(1/h))` bisection queries per direction. Each query uses a prior-bounded dependency stencil and logarithmically many attempted bits for its confidence allocation. Choosing
\[
        h\asymp\nu^{1/(s-2)}
\]
gives the stated upper bound. The calculation is consistent.

This is an attempted-bit and command-center bound. It is not an end-to-end bit-complexity theorem: representing command locations, achieving calibration `O(\sigma)`, apparatus movement, and certified evaluation of elementary functions are separate resources. The manuscript states this, and the qualification must remain prominent.

## 6. Audit of period recognition

The patch defect tests whether a bounded candidate translation reproduces every protected component in both signs. Exact zero is equivalent to membership in the full period group. A root component and all bounded matching copies generate the full period lattice, including possible periods smaller than the supplied presentation lattice.

For the finite theorem, the known nonperiod margin `\eta` separates true periods from all bounded false candidates. Once the reconstructed Hausdorff error is small, the threshold test recovers exactly the accepted period list and the primitive component-orbit relation.

An independent pair has determinant separated from zero by the primitive covolume lower bound. All other accepted vectors have rational coordinates with a uniformly bounded denominator in that pair. Rational separation and Hermite reduction therefore recover the exact discrete relations and a matched primitive basis. This part is a correct conditional finite arithmetic argument.

The conclusion is not an inference of periodicity. Periodicity and a bounded presentation are members of the prior class, and `\eta` is supplied for a uniform finite stopping rule. Without known `\eta`, the manuscript correctly retreats to a pointwise eventual statement.

## 7. Audit of the information lower bound

### 7.1 Physical packing

The variable obstacle has support
\[
 p_\omega(\theta)
 =1+ah^s\sum_{j=1}^m\omega_j
          \psi((\theta-\theta_j)/h),
 \qquad m\asymp h^{-1}.
\]
The angular supports are disjoint. The derivative of order `k\le6` is
`O(h^{s-k})`, and the sixth derivative has a uniform `\beta`-Hölder seminorm. The curvature-radius perturbation is `O(h^{s-2})`, so a sufficiently small fixed amplitude preserves strict convexity and all geometric margins.

Two different bit vectors differ in the second derivative by
`c h^{s-2}` at one bump center. The fixed second obstacle has a different size, forcing the primitive period group to remain the prescribed lattice and providing a uniform patch margin. Thus the lower bound is not caused by period uncertainty.

One clarification should be inserted in the theorem proof: the paper defines the class using centered supports but displays the packing in an uncentered laboratory support. Subtracting the Steiner first harmonic changes the bump family by `O(h^s)`, which is negligible relative to the `C^2` separation `h^{s-2}`. Hence the separation survives centering. This is a short argument, but it should be written explicitly so that “laboratory pose supplied” cannot be read as table-dependent shape side information.

### 7.2 Binary transcripts

After all parameter-independent random seeds are fixed, every adaptive controller command and final output is a function of the preceding binary transcript. A depth-`N` experiment has at most `2^N` leaves. Pairwise disjoint acceptable output sets allow at most one packed parameter to succeed at each leaf. Averaging over the uniform parameter and then over the seeds gives success probability at most `2^N/M`.

Taking `h\asymp\nu^{1/(s-2)}` produces
\[
        \log_2M\asymp\nu^{-1/(s-2)},
\]
and yields the stated lower bound. This proof permits more precise adaptive inputs than the upper-bound construction and therefore legitimately applies to it.

The result concerns a deterministic cap on table-dependent binary outputs. It is not, as written, an expected-stopping-time lower bound, a lower bound for continuous-valued sensors, or a theorem about input precision. The manuscript states these boundaries.

## 8. Corrections and qualifications required in any resubmission

### 8.1 Make the lower-bound gauge explicit

Give one formula for the lower-bound accuracy sets in the laboratory frame and state explicitly:

- which component correspondence and global pose are supplied;
- whether supports are centered or uncentered in the loss;
- why Steiner centering changes the packing by only `O(h^s)`;
- why the `h^{s-2}` separation therefore remains.

The present argument contains all ingredients, but the gauge should not be left to inference.

### 8.2 Keep the deterministic-cap scope adjacent to “matching power”

The phrase “matching power” is correct for the least uniform deterministic cap on binary outputs at fixed confidence. It does not cover expected random stopping times or confidence/logarithmic factors. This distinction belongs in every abstract-level summary.

### 8.3 Display all resource axes together

Any complexity table should separately list:

- table-dependent output bits;
- distinct or repeated command centers;
- finest spatial localization;
- position/time/angle calibration;
- aperture size;
- controller movement/setup;
- numerical and bit-operation cost.

Only the first two are bounded by the displayed statistical rate. The lower bound deliberately gives the controller arbitrary input precision.

### 8.4 Preserve the exact sensor contract

“Scalar collision law” must remain accompanied by localized start densities, a prescribed compass law, translated reciprocal nominal reverse starts, fresh preparations, and all-attempt normalization. A free-start label or impact location is not observed.

### 8.5 Keep the known-margin and periodic-class assumptions visible

Uniform finite primitive-period recovery depends on the known positive patch margin and a bounded periodic presentation. These are not consequences of the collision bits.

## 9. Top-four significance assessment

Version 32 materially improves the paper. It supplies the missing lower bound, identifies the correct boundary-smoothness power, and reduces the finite design from a two-dimensional uniform grid to adaptive one-dimensional boundary searches. This is a publishable conceptual organization of the active experiment.

Nevertheless, the strongest theorem remains a conditional active sensing result whose controller carries substantial continuous input information and increasingly precise calibration. Its local-query reduction uses classical reciprocal cancellation, stopped random-walk potential theory, and value iteration. Its boundary algorithm uses established active line search and polynomial approximation. Its lower bound is the natural Hölder bump entropy coupled with binary leaf counting. The genuinely new contribution is the rigorous integration of these mechanisms for this collision sensor and the subsequent periodic arithmetic.

That integration is nontrivial, but its reach remains tied to the engineered observation protocol and strong prior class. It does not establish a new general rigidity principle for billiards or a natural invariant used elsewhere in dynamics and inverse geometry. In my judgment this does not meet the exceptional conceptual threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 10. Literature and novelty boundary

The revised comparison with active boundary estimation is necessary and substantially better than in v31. Castro–Nowak study adaptive feature queries with binary class labels and classification-risk losses. Locatelli–Carpentier–Kpotufe study active recovery of smooth decision boundaries using line searches and interpolation, including adaptation to unknown regularity/noise parameters. The present experiment differs because its collision bit is not a membership label; the reciprocal Bellman reduction first constructs an approximate label, and the final loss is physical `C^2` geometry plus periodic recognition.

The paper does not claim that bisection, polynomial interpolation, killed Green estimates, or binary-tree counting are new abstract principles. I did not find in this focused review a cited theorem containing the exact combination proved here. This was not an exhaustive priority search.

## 11. Verification and source delivery

The author's local source-content receipt records:

- 11,647 finite mathematical/source diagnostics;
- 42 validation-contract checks;
- identical ordinary and optimized outputs;
- a warning-free 13-page primary;
- no physical apparatus execution and no formal proof certificate.

The exact-source hosted run `37153403982` checked out the reviewed SHA, qualified all fifteen declared documents, archived the native sources and evidence, and completed successfully. Source delivery is therefore not a basis for the recommendation.

The accompanying independent `verify_review.py` imports no author code. Ordinary and optimized executions agree and perform 142,820 checks, principally in exact integer or rational arithmetic. They cover:

- the reciprocal endpoint truth table and pooled translation identity;
- normal-contact Hessian positivity;
- exact finite mean exits and Bellman domination;
- different-zero-set resolvent inequalities on finite models;
- dependency-diamond versus full killed updates;
- interval propagation;
- adversarial boundary-layer bisection;
- seven-node polynomial reproduction and noise norms;
- exponent balances;
- bounded-denominator period arithmetic and unimodular invariance;
- binary-tree counting and packing scales;
- finite query/attempt bookkeeping.

These diagnostics do not certify the continuum compactness, tube, rolling-ball, interpolation, physical packing, or period-recognition proofs. They do not execute the sensor, build TeX, establish novelty, or make an editorial decision.

## 12. Final verdict

**Response to the v31 report:** substantively successful. The missing lower bound and closest active-boundary comparison have been supplied, and the finite upper construction is genuinely improved.

**Mathematical audit:** no fatal counterexample found in the new v32 core; one lower-bound gauge/centering clarification and several scope qualifications should be added.

**Reproducibility:** exact-SHA fifteen-document qualification passed.

**Editorial assessment:** strong specialist-journal potential, but the active calibrated information model, decisive priors, and classical nature of the principal statistical mechanisms leave the contribution below the requested top-four threshold.

**Recommendation: reject at the Annals/Acta/Inventiones/JAMS benchmark.**
