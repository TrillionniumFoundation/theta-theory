# External top-four referee report on A2 v29

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v29-scalar-collision-tomography-2026-10-03`  
**Equivalent referee-copy alias:** `revision/a2-v29-referee-copy-2026-10-03`  
**Reviewed commit:** `b81664d3961cdbad58563f37dcaed03288de199e`  
**Reviewed tree:** `7957f3778b73ff4948090bce5338df8de0b2de0c`  
**Mathematical checkpoint:** `44c2b6bd6caf8946384ade3576a079c4e237bbd9`  
**Controlling preceding external report:** `a067c123c5702decb4b7146cf57961a65afe5c88`  
**Manuscript directory:** `papers/A2-v29-scalar-collision-tomography`  
**Date:** 3 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 29 is a genuine mathematical revision and gives a materially different answer to the main information-content objection in the v28 report. The previous exact route recorded a first-impact position whose support directly exposed a physical boundary patch. The present primary records only one binary outcome per attempted launch: collision before one fixed horizon, or zero for both a miss and an attempted start in the solid. With two opposed directions and translated spatial input laws, the paper proves the exact identity

\[
 B_a(q)-B_{-a}(q+a)=\mathbf 1_{\mathcal O}(q+a)-\mathbf 1_{\mathcal O}(q).
\]

A finite-chain minimum formula then reconstructs the obstacle occupation from this finite difference, using the diameter and separation priors to guarantee a zero on every chain. This scalar-output reduction is real; it is not a relabelling of the position-output theorem.

On the new v29 core audited in detail, I found no fatal counterexample. The reversal identity, finite-chain inverse, indicator and mollified zero witnesses, scale-independent propagation of scalar-mean error through the chain inverse, finite-grid occupation comparison, rolling-ball component matching, compensated support smoothing, retained two-sided period test, rational lattice locking, and the finite-confidence rate calculation are coherent under the stated hypotheses. The current exact-SHA twelve-document workflow also succeeds. I therefore do **not** base the negative recommendation on a known false central theorem or on an unresolved source-delivery failure.

The remaining objection is editorial and conceptual. The output is one bit, but the total information contract is not low-information in the usual rigidity sense. The experiment may command a two-dimensional grid of increasingly localized spatial launch densities, knows every command center and direction, uses exactly opposed collimated velocities and a fixed calibrated horizon, and keeps attempted starts in the unknown solid in the denominator as zero outcomes. Exact data consist of two functionals on a large class of spatial test densities, not two scalar probabilities. The finite theorem transfers output localization to input localization of order `nu^(3/2)` and uses `O(nu^-3 log(C/(nu delta)))` attempts.

Mathematically, the new core is an elegant physical realization of an elementary finite-difference identity plus a telescoping minimum inverse. The global period theorem is the retained v28 finite-patch theorem, under an assumed bounded periodic presentation and, for uniform noisy decisions, a known nonperiod patch margin. The remaining statistical and approximation ingredients are standard once those inputs are granted. This is serious and potentially strong specialist-journal mathematics, but in my judgment it does not produce the exceptional naturality, breadth, or conceptual transformation expected by the four journals named above.

A focused specialist submission centered on the scalar reversal/chain inverse and repeated-motif period reconstruction, after a fresh human proof review and the literature and framing corrections below, could be compelling. I would not recommend another open-ended revision cycle at the requested top-four benchmark.

## 2. Frozen source and chronology

Both v29 branch names listed above resolve to the same author head

`b81664d3961cdbad58563f37dcaed03288de199e`

with tree

`7957f3778b73ff4948090bce5338df8de0b2de0c`.

The head is the response/source-binding commit. Its parent is the mathematical checkpoint

`44c2b6bd6caf8946384ade3576a079c4e237bbd9`,

which is based directly on the v28 external-review head

`a067c123c5702decb4b7146cf57961a65afe5c88`.

That report reviewed v28 author commit

`3ac2df58d175010f338dd6ae8af84158c1590d20`.

The complete reviewed v28 paper is preserved under `retained/v28` with native tree

`b17c9c051f3e279d6f7610e3d1c5e56d0733216a`.

No `revision/a2-v30...` branch existed when this report was frozen. The present review branch starts directly from the v29 author head and adds files only under

`reviews/a2-v29-external-harsh-top4-rereview-2026-10-03/`.

No author source, author workflow, previous report, retained volume, or unrelated paper is modified.

The active primary consists of:

- `core/01_reversal.tex`;
- `core/02_local_acquisition.tex`;
- `core/03_periods.tex`;
- `core/04_finite_experiment.tex`;
- `core/05_comparison.tex`.

I also inspected the response, proof ledger, literature audit, source pins, README, references, validation receipt, workflow definition, hosted workflow result, and the controlling v28 report.

## 3. The exact observation and what v29 changes

Let `chi` be the indicator of the obstacle union. For a displacement `a=tv`, define `B_a(q)` to equal one when the attempted start is free and the unreflected segment from `q` to `q+a` meets the obstacle; it equals zero for a solid start or a free miss. Before a first collision, a billiard flight follows precisely that segment.

For a nonnegative commanded density `f`, the observable mean is

\[
P_a(f)=\int f(q)B_a(q)\,dq.
\]

The reverse experiment uses velocity `-v` and the translated density `f_a(q)=f(q-a)`. Thus it begins from the opposite segment endpoint with the corresponding translated distribution.

The key identity is exact at positive time. It is not a time derivative, a small-horizon asymptotic, a reconstruction from reflected post-collision dynamics, or a collision-position observation. Interior-only intersections cancel because both endpoint starts are free and both orientations hit. If exactly one endpoint is solid, the difference of the two bit outputs records the signed endpoint occupation difference.

Testing all smooth nonnegative spatial densities determines the signed measure with density

\[
\delta_a\chi(q)=\chi(q+a)-\chi(q).
\]

This is the right exact interpretation. “Two opposed collision laws” means two input-output functionals over spatial commands, not two real numbers.

Version 29 then supplies an explicit finite experiment. Localized kernel commands on a deterministic grid estimate mollified occupation differences. The finite-chain inverse recovers the occupation averages, and a physical candidate consistent with all scalar means supplies the finite patch used by the retained period argument.

## 4. Correctness audit of the scalar inverse

### 4.1 Reversal balance

Let `I(q)` indicate whether the unoriented segment `[q,q+a]` meets the obstacle. Both directions see the same segment image. Therefore

\[
B_a(q)=(1-\chi(q))I(q),\qquad
B_{-a}(q+a)=(1-\chi(q+a))I(q).
\]

Their difference is

\[
\{\chi(q+a)-\chi(q)\}I(q).
\]

If either endpoint is solid, `I(q)=1`; if both endpoints are free, the prefactor is zero. The pointwise formula follows in all cases, including multiple component intersections. Changing variables in the reverse integral gives the weighted identity.

This proof is correct. It also reveals the elementary nature of the mechanism: the mathematical novelty cannot be attributed to an abstract new finite-difference theorem. It lies, if anywhere, in recognizing that this attempted-launch convention physically realizes the signed occupation difference and in combining it with the later geometric inverse.

### 4.2 Finite-chain inversion

If a nonnegative function `u` has a zero among

\[
u(x),u(x+a),\ldots,u(x+ma),
\]

then the partial sums of `delta_a u` are exactly `u(x+ka)-u(x)`. Their minimum is `-u(x)`, proving

\[
u(x)=-\min_{0\le k\le m}
       \sum_{j=0}^{k-1}\delta_a u(x+ja).
\]

The pointwise perturbation bound follows because the minimum is one-Lipschitz in the sup norm of the finite partial-sum list. The stated `L^p` estimate follows from Minkowski after translating the finitely many domains. I found no defect in this argument.

The zero condition is indispensable: constants have the same zero finite difference. The paper states this and supplies an appropriate geometric witness rather than inserting an unobserved free reference point.

### 4.3 Geometric zero witnesses

Suppose components have diameter at most `D_0`, mutual separation at least `d_0`, `t<d_0`, and `mt>D_0`. If every chain point were occupied, consecutive points could not switch components, so the two endpoints would lie in one component at distance `mt>D_0`, a contradiction.

For mollified occupation, positivity implies membership in the `sigma`-parallel enlargement of some component. The enlarged diameters are at most `D_0+2sigma`, their separation is at least `d_0-2sigma`, and the same argument applies when the displayed strict inequalities hold. This part is sound.

The hypotheses are substantive. The inversion is not valid for unbounded slabs parallel to the displacement, for components without a diameter bound, or when the chosen step permits the chain to move between enlarged components.

## 5. Correctness audit of finite patch reconstruction

### 5.1 Scalar-mean stability

Each balance difference is formed from two Bernoulli means. If each mean has error at most `epsilon`, the difference error is at most `2epsilon`, and the finite-chain inverse amplifies it by at most `m`. Thus the occupation-average error is at most `2m epsilon`, uniformly in the kernel scale. Clipping to `[0,1]` is nonexpansive. This calculation is correct.

The phrase “uniformly in the scale” concerns propagation of already controlled mean error. It does **not** mean that the physical commands are scale-free: a translation error in a localized density costs `O(ell/sigma)` in total variation, and the finite theorem requires spatial localization to sharpen as `sigma` decreases.

### 5.2 Finite grid and component matching

The occupation average has Lipschitz constant at most `K/sigma`. The chosen grid radius, together with the finite-chain comparison, converts grid closeness to a uniform occupation difference below `1/8` on the protected square.

If a point lies in the `sigma`-erosion of one obstacle union, its occupation average is one. Uniform closeness prevents it from lying more than `sigma` from the other union. This yields the two erosion inclusions. The curvature upper bound gives a uniform interior rolling radius: in support coordinates, `p+p''` is bounded below by `1/kappa_+`, so erosion followed by dilation recovers each component for smaller `sigma`.

Connected erosions cannot be split between distinct expanded target components. Applying the inclusion in both directions and using physical separation makes the component matching bijective and gives Hausdorff error at most `2sigma`. The protective collar prevents an incomplete outer fragment from being treated as a full body. I found this argument coherent.

### 5.3 Smooth support interpolation

Hausdorff distance equals the sup norm of support-function difference. A compensated kernel with vanishing moments through degree three gives

\[
\|J_h*(p-p')\|_{C^2}\le C e h^{-2},
\qquad
\|J_h*p-p\|_{C^2}+\|J_h*p'-p'\|_{C^2}\le C h^4
\]

under the stated `C^6` bound. Balancing with `h=e^{1/6}` yields `C e^{2/3}`. Steiner-center error is `O(e)`. The exponent calculation is correct; it is a standard interpolation/smoothing mechanism rather than a new approximation-theoretic result.

## 6. Period recognition and whole-table reconstruction

The finite patch theorem is retained from v28, but the primary includes the proof needed by the scalar route.

A bounded, possibly nonprimitive periodic presentation is assumed. Repeated congruent bodies and arbitrary individual symmetries are allowed. For a candidate translation `w`, the defect tests every central component in both the `+w` and `-w` directions. Because the central square contains a representative of every presentation orbit, zero two-sided defect implies both

\[
\mathcal O+w\subseteq\mathcal O,
\qquad
\mathcal O-w\subseteq\mathcal O,
\]

and hence equality. The converse is immediate.

The full period group contains the supplied-but-unknown presentation lattice. Its quotient injects into the finite set of component orbits, so the index is at most `r_0` and its covolume has a positive lower bound. The protected finite list contains presentation generators and representatives of every quotient coset; accepted differences therefore generate the full intrinsic period lattice.

For noisy geometry, the paper first classifies finite candidate translations using the known patch-defect margin. Only geometrically accepted vectors enter the arithmetic stage. Determinant separation detects an independent pair; bounded subgroup index gives bounded-denominator rational coordinates; finite rational search and a column Hermite basis then recover the exact discrete relations. This order avoids taking an integer span of noisy real vectors. I found no fatal flaw in this chain.

The exact theorem does not require a numerical patch margin. The uniform finite-confidence theorem does. When the margin is unknown, the paper correctly proves only pointwise eventual correctness, not an observable uniform finite stopping certificate. The repeated-disk symmetry-jump example correctly explains the necessity of this distinction.

## 7. Audit of the finite-confidence theorem

The deterministic grid contains `O(sigma^{-2})` commands. Every command mean is estimated to a fixed absolute accuracy by Hoeffding and a union bound, giving

\[
O\!\left(\sigma^{-2}\log\frac{C}{\sigma\delta}\right)
\]

attempts. On the simultaneous event, an approximate minimizer over the compact physical class has ideal scalar means close enough to the true means for the grid lemma to apply. This is an existence-based measurable regularization, not a polynomial-time search over an infinite-dimensional class.

Hausdorff error is `O(sigma)` and `C^2` support error is `O(sigma^{2/3})`. Taking

\[
\sigma=c\nu^{3/2}
\]

gives `C^2` error `O(nu)` and transforms the command count into

\[
O\!\left(\nu^{-3}\log\frac{C}{\nu\delta}\right).
\]

The exponent algebra is correct. The period basis and area errors are smaller, `O(sigma)`, after the discrete relations have locked.

This is a sufficient upper bound under known `eta`, `C^6` and physical bounds. It is not minimax, not an end-to-end computational bound, and not robust to unspecified angular or timing error. A total-variation command bias may be charged only when independently certified.

## 8. Information contract and physical interpretation

The manuscript now describes its observation more honestly than earlier revisions. Still, the following qualifications must remain inseparable from every headline claim.

### 8.1 Solid-start attempts are essential

The denominator counts all commanded attempts, including commands whose realized start lies in the unknown solid. Such attempts are assigned the same zero bit as a free miss. This convention is what makes the endpoint occupation terms appear in the reversal difference. A standard billiard experiment defined only on free phase space, or one conditioning on successful preparation, does not automatically provide the same identity.

The theorem is valid under its protocol. The protocol should not be described as ordinary collision-count observation without this attempted-preparation convention.

### 8.2 One-bit output is not one-bit total information

Each trial returns one bit, but the command identity, command center, spatial mask, direction and horizon are known. Exact data are functionals on spatial densities; finite data use a two-dimensional grid whose resolution grows as the desired geometric error shrinks. The output channel is scalar while the controlled input family carries location information.

This trade is mathematically legitimate and interesting. It prevents a direct conclusion that v29 solves the earlier uniformly prepared count-only inverse problem or dominates the position-output experiment in a Blackwell or minimax sense.

### 8.3 Periodicity is assumed, not inferred

The scalar inverse recovers a physical patch without periodicity. Extending that patch to the whole plane and recovering a lattice use the bounded periodic-presentation prior. The result is not a crystallinity theorem for an arbitrary Delone configuration, nor a discovery of periodicity from one unstructured scalar experiment.

## 9. Literature and novelty framing

The manuscript's comparisons with covariograms and recent local-periodicity/Delone theory are useful. They do not yet cover the nearest observation tradition adequately.

Long before the present work, random-set theory and mathematical morphology organized geometric information through hit probabilities and capacity functionals: translated compact “structuring elements” are tested for intersection with a set. The v29 bit is not exactly a standard capacity functional because it contains an endpoint-exclusion convention and uses a signed opposed-direction cancellation. Nevertheless, a randomly translated segment hitting a deterministic obstacle is extremely close in observation language and should be compared explicitly. Matheron's stereological/random-set framework and modern treatments of capacity functionals are the natural starting points.

There is also a substantial active geometric-probing and binary-projection literature in computational geometry and discrete tomography. Those works use different probes and targets and do not obviously contain the exact reversal/minimum formula here. They are nevertheless closer to the preparation/output trade of v29 than passive spectral or marked-length rigidity.

I do not assert that these sources subsume the new theorem, and this review is not an exhaustive priority search. The correction is one of novelty placement: the paper's plausible increment is the endpoint-exclusion reversal identity, the bounded-zero-witness inverse, and their integration with periodic-motif recovery—not the general idea that hit/no-hit probabilities of translated probes encode a set.

## 10. Top-four significance assessment

Version 29 is stronger, cleaner and more focused than v28. It eliminates impact-position output and proves a nontrivial reconstruction from controlled scalar means. It also permits repeated motifs and arbitrary body symmetries through the retained patch-period theorem. These are real accomplishments.

At the requested benchmark, however, several limitations remain decisive.

1. **The central identity and chain inverse are elementary once the protocol is written down.** The proof is essentially a four-case endpoint calculation followed by telescoping and a minimum.
2. **The input control is exceptionally rich.** Location information removed from the output reappears in arbitrary localized spatial commands, exact opposed directions and attempted solid-start normalization.
3. **The global conclusion is prior-driven.** A bounded periodic presentation, diameter/separation/curvature bounds and, for uniform noisy decisions, a numerical patch-defect margin are assumed.
4. **The finite inverse is existence-based.** Candidate selection over a compact infinite-dimensional class has no effective complexity theorem.
5. **The statistical theorem is an upper bound for a designed experiment.** No lower bound, minimax theory, or comparison of total experimental resources is provided.
6. **The result does not solve a standard major rigidity datum.** Uniform count laws, passive trajectories, marked lengths and spectra remain outside the theorem.

The combination is original enough to merit serious specialist consideration, but I do not see an exceptional structural principle of the breadth expected for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 11. Corrections required for a specialist resubmission

1. Add a theorem-level comparison with random-set capacity/hit functionals, mathematical morphology, and active geometric probing. State exactly which endpoint convention and signed cancellation are new.
2. Keep the attempted-solid-start denominator in the abstract, first theorem and any press-style summary. “Collision probability” without this convention is ambiguous.
3. Keep “one bit per attempt” adjacent to the spatial-command complexity. Avoid language that could be read as one-bit total data or as a comparison with uniformly prepared count laws.
4. Qualify the scale-independent mean-error sentence: the chain inverse has no `sigma^{-1}` amplification, but command localization and center calibration become more stringent as `sigma` decreases.
5. Keep the known patch margin `eta` adjacent to every uniform discrete-recovery or finite-confidence statement.
6. Distinguish exact rational relations in a recovered generator basis from exact real-valued Euclidean coordinates.
7. Preserve the present honest statement that candidate selection is an existence regularization, not an efficient reconstruction algorithm.

## 12. Independent diagnostics and source qualification

The accompanying `verify_review.py` imports no author module. Ordinary and optimized Python produced identical output with **306,117** successful finite checks. The checks cover:

- all endpoint configurations and many finite segment-hit patterns for the reversal identity;
- weighted finite analogues of the probability balance;
- binary and nonnegative chain inversion and deterministic noise bounds;
- indicator and enlarged-component zero-witness examples;
- the finite-grid constants and smoothing/rate exponents;
- two-sided finite-motif period tests;
- determinant gaps, patch-margin classification, bounded-denominator coordinates and subgroup-index arithmetic.

These diagnostics are exact integer/rational computations. They do not certify the compactness arguments, continuum erosion theorem, measurable candidate selection, physical apparatus, literature priority or the full retained programme.

The author-side local receipt records 18,945 finite mathematical/source checks, 19 validation-contract checks, identical normal/optimized output and a warning-free twelve-page primary. That local receipt is source-content execution only.

The exact-triggering-SHA workflow run `37133211373`, bound to the reviewed commit, completed successfully. Exact checkout, current and retained entry-point checks, all twelve declared document qualifications, evidence archival and artifact upload all concluded successfully. Consequently source delivery is not a basis for the present negative recommendation.

## 13. Final verdict

**Response to the v28 report:** substantively successful. Version 29 removes impact-position output and gives a genuine scalar-output inverse under an explicitly richer active-input protocol.

**Mathematical audit:** no fatal counterexample found in the new core; the retained period theorem remains coherent in the scope used here.

**Reproducibility:** exact-SHA twelve-document qualification succeeds; finite diagnostics are evidence, not proof certification.

**Editorial assessment:** the paper is technically serious and potentially strong for a specialist journal, but its elementary central mechanism, highly controlled spatial inputs, decisive priors and limited relation to standard rigidity data leave it below the exceptional conceptual threshold of the requested four journals.

**Recommendation: reject at the Annals/Acta/Inventiones/JAMS benchmark.**