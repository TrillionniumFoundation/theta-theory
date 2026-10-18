# External top-four referee report on A2-DYN v4 (latest v5 branch alias)

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Latest revision branch:** `revision/a2-dyn-v5-raw-llt-referee-response-2026-10-05`  
**Equivalent author branch:** `revision/a2-dyn-v4-referee-response-2026-10-05`  
**Reviewed commit:** `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`  
**Reviewed repository tree:** `73ded33d0d53feb57d526bf55d3797012535f6dd`  
**Mathematical checkpoint:** `12a7c04eaf9754de356a69dfc1ec4ae09ba605b8`  
**Active core tree:** `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`  
**Manuscript directory:** `papers/A2-DYN-v4-quantitative-periods-and-clock`  
**Date:** 5 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, formal proof certificate, physical experiment, or independent human specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

The manuscript contains serious and, in several places, elegant dynamics. It constructs a true physical periodic-orbit family in a finite-horizon triangular Lorentz gas, proves an exact joint periodic-annihilator theorem, derives an explicit polynomial lower bound for selected roof phases, identifies and subtracts a genuine jump singularity in a raw return-time density, proves fixed-return continuity as the disk radius varies, and establishes a parameter-uniform first-order physical clock including unfinished returns. On the portions audited in detail, I found no fatal counterexample.

The negative recommendation is not based on the manuscript having falsely claimed a complete local limit theorem. The authors repeatedly and correctly state that the full parameter-uniform raw mixed-density LLT remains unproved. They isolate the missing common operator realization, measurable-cohomology regularity, covariance control, returned temporal high-frequency bounds, and summation of all critical and singular branches. That honesty is a strength.

The editorial difficulty is that these missing items are not peripheral. They are precisely the bridge from the current collection of arithmetic, edge, and clock modules to the paper's motivating probabilistic theorem. The quantitative periodic-phase estimate is not yet a Dolgopyat or resolvent estimate on a specified Banach space. The raw-edge calculation treats an isolated critical contribution and explicitly leaves the all-word residual sum open. The clock theorem is first order on the scale of time and does not provide the square-root residual control needed for the conditioned Gaussian transfer. Thus the manuscript, as it stands, is a rigorous programme of enabling theorems around a still-open central target rather than a completed top-four theorem.

I would regard a focused version as a credible candidate for a strong specialist journal in hyperbolic dynamics or billiards, subject to a fresh human proof review and some expansion of the parameter-continuity arguments. A future manuscript that closes the common-operator, cohomology, covariance, and all-branch residual steps and proves the advertised uniform raw-density LLT would merit a substantially different editorial assessment.

## 2. Frozen source and chronology

The latest branch name contains `v5`, but it resolves to the same commit as the v4 author branch:

`f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`.

That commit adds response, audit, validation, and exact-source qualification material. Its parent

`12a7c04eaf9754de356a69dfc1ec4ae09ba605b8`

contains the v4 mathematical additions. The active core tree is unchanged between the two. I therefore identify the reviewed mathematical object by Git SHA and call it A2-DYN v4, with the latest v5 branch treated as an alias rather than a new mathematical revision.

No prior branch or repository path containing an external A2-DYN referee report was found. The repository instead contains an author-side specialist handoff that explicitly disclaims independent review. I have not substituted the A2-GEOM v43 acceptance report for a dynamics report; the data, theorem, and paper are different.

The present review branch starts directly from the reviewed author head and adds files only under

`reviews/a2-dyn-v4-external-top4-review-2026-10-05/`.

No manuscript source, author branch, workflow, earlier paper, or unrelated path is modified.

## 3. Mathematical package and actual scope

The parameter is a disk radius

\[
R\in I=[0.45,0.47]
\]

for the triangular periodic Lorentz gas. The manuscript distinguishes three clocks and three kinds of data:

1. the physical collision map and its displacement, collision count, and flight time;
2. an induced first-return map to a four-square section, with return displacement, physical collision count, and induced roof;
3. finite experimental or geometric diagnostics, which are never substituted for the continuum dynamics.

The principal unconditional conclusions are:

- explicit physical periodic cycles and a genuine induced section;
- a full augmented lattice at zero roof frequency;
- an infinite zero-winding periodic family with positive, strictly increasing, bounded excess lengths;
- triviality of the joint periodic annihilator;
- quantitative high-roof phase separation using logarithmic-length periods;
- a physical critical-edge coefficient and exact subtraction of one jump term;
- a local inversion criterion allowing nonvanishing extracted edge mass away from the central window;
- fixed-return raw-density and first-moment continuity in the radius;
- exact Kac normalizations;
- a parameter-uniform first-order physical clock and negligible unfinished return on the linear time scale.

The paper does **not** prove:

- a common anisotropic operator family for the induced observables;
- a quantitative resolvent estimate from the periodic phase bounds;
- a measurable-cohomology theorem permitting periodic evaluation of spectral transfer functions;
- uniform nondegeneracy and continuity of the full covariance;
- an integrable all-branch raw characteristic remainder;
- the complete parameter-uniform raw mixed-density LLT;
- the square-root residual estimate needed to transfer a conditioned Gaussian theorem from returns to physical time.

These boundaries are accurately stated in the manuscript and must remain part of any future presentation.

## 4. Audit of the physical periodic geometry

The elementary two- and three-cycles have the displayed lengths and collision records. The winding four-cycle is defined by a scalar reflection equation in an angle interval, and the source includes a rational interval certificate covering all radii in `I`. The certificate controls uniqueness of the root, incidence, and clearance from every third disk, rather than checking only a finite set of floating samples.

The four selected cycles produce the record matrix

\[
V=\begin{pmatrix}
0&0&2&1\\
0&0&3&1\\
1&0&4&1\\
0&1&4&1
\end{pmatrix},
\qquad |\det V|=1.
\]

This correctly gives the complete zero-roof lattice obstruction for circle-valued coboundaries whose transfer function can be evaluated at the selected fixed points. The manuscript also correctly warns that this qualification is essential: a merely measurable transfer function need not have meaningful periodic values.

The added excursion family is the strongest geometric part of the paper. The optical action is strictly convex, the minimizer lies in the physical box, the reflection and clearance checks are explicit, and the orbit has record

\[
K=0,\qquad N=2m+1,\qquad h=m,
\]

with length `L_m`. The Bellman argument yields

\[
0<E_m<E_{m+1}\le 2d^2/g<10^{-2},
\]

so the positive increments tend to zero. This avoids a common logical error: nonarithmeticity is not inferred from a finite list of decimal period lengths.

I found the convexity, physical realization, and strict-increment chain coherent. The proof is nevertheless specialized to this explicit family; it should not be advertised as a general periodic-orbit theorem for dispersing billiards.

## 5. Audit of joint arithmetic and quantitative phase separation

The long normal two-cycle and the excursion family give

\[
\exp i(s+\beta E_m)=1.
\]

Consecutive quotients imply

\[
\beta(E_{m+1}-E_m)\in2\pi\mathbb Z.
\]

Because the increments are positive and converge to zero, this forces `beta=0`; the unimodular four-cycle matrix then forces all remaining torus phases to vanish. The argument proves the stated trivial joint periodic annihilator.

The quantitative section strengthens the optical analysis. The averaged Hessian has the printed uniform spectral bounds and an inverse with explicit lower and upper decay estimates. These give two-sided bounds

\[
10^{-4}400^{-m}
 \le E_{m+1}(R)-E_m(R)
 \le 300^{-1}(49/100)^{m-1}.
\]

Choosing

\[
m(b)=1+\left\lceil\frac{\log b}{\log(100/49)}\right\rceil
\]

produces a phase discrepancy bounded from below by a negative power of `b`. The constants and exponent bookkeeping are internally consistent, and the independent finite diagnostics accompanying this report reproduce the displayed algebra.

This result is useful, but its exact scope is decisive. It is a lower bound for selected periodic phase products, and in its approximate form it applies to a continuous unit-modulus phase near the selected periodic states. It is **not** a transfer-operator norm estimate, a spectral gap at large roof frequency, or a measurable Livšic theorem. A top-four claim based on this arithmetic would require a theorem that transports the phase discrepancy into contraction or resolvent control on the actual operator family used for the raw observables. That bridge is currently listed as future work.

## 6. Audit of raw critical edges and inversion

Near the normal alternating orbit, the reduced action Hessian is computed explicitly. The determinant identity

\[
\sqrt{\det H_N}=\sinh(N\zeta_R)
\]

and the section density give the right-edge jump

\[
J_{N,R}=\frac{1}{2R\sinh(N\zeta_R)}.
\]

The normalization is correct. The more general regular-word proposition identifies a unique normal-to-normal critical point, a positive Schur determinant, and the jump coefficient

\[
J=\frac{|C|}{2R\sqrt{AD-C^2}}.
\]

Its Neumann-series argument yields an individual-word exponential upper bound. The manuscript correctly refuses to multiply this by an uncontrolled word count.

The consequence for Fourier inversion is also correctly drawn. A positive jump at the left endpoint of a raw lattice component prevents the associated raw characteristic coefficient from being integrable in roof frequency. The exact subtraction

\[
f(Ng+s)=Je^{-s}\mathbf1_{s\ge0}+q(s)
\]

retains the physical density and leaves an isolated remainder with quadratic Fourier decay.

The local inversion theorem is conceptually sound: an extracted boundary mass may remain nonzero in total variation if its density or convolution is negligible in the diffusive central window. This is an important clarification of what a raw LLT actually requires.

The unresolved issue is global. The paper has not classified and summed all regular critical words, singular itinerary boundaries, and central branches with an integrable uniform remainder. That missing all-branch estimate is one of the main theorems still needed for the motivating LLT, not a routine appendix.

## 7. Audit of parameter continuity and the physical clock

The exact Kac formulas give the mean return collision count and mean return roof, and hence the physical collision rate

\[
\bar\tau_R^{-1}
 =\frac{2R}{\sqrt3/2-\pi R^2}.
\]

The fixed-return continuity theorem compares actual first-return domains on a common collision space, removes a small singular set, applies branchwise coarea on regular patches, and uses exact Kac means for uniform integrability. The stated conclusions—`L^1` continuity of the fixed-return density and first-moment continuity—are plausible and consistent with the finite-record geometry. This is, however, a load-bearing continuum theorem, and the written proof is compressed relative to the complexity of moving singularity domains. A specialist journal version should make the common-domain construction, patch matching, and treatment of critical-value neighborhoods more explicit.

The uniform-clock theorem uses a compact subadditive upgrade of the `L^1` ergodic theorem, uniform integrability of return blocks, and renewal inversion. It correctly includes the stationary length-biased law and the largest unfinished return. The conclusion is a uniform functional law of large numbers on the linear scale:

\[
\frac1t(V_R(tu),C_R(tu),W_R(tu))
 \longrightarrow
 \left(\frac{uc_*}{\bar\tau_R},
       \frac{u}{\bar\tau_R},0\right).
\]

I found the first-order chain coherent. Its limitation is equally clear. An `o_P(t)` unfinished return is not the `o_P(\sqrt t)` control required for a central or local limit transfer, especially after conditioning on rare lattice events. The paper's downstream proposition assumes the stronger functional CLT and square-root residual conditions rather than proving them.

## 8. Relation to existing Lorentz-gas limit theory

The classical Lorentz-process local limit theorem treats the displacement of the finite-horizon collision process. Abstract local central limit theorems for hyperbolic suspension flows give mixing-LCLT conclusions under spectral, arithmetic, and regularity hypotheses. Functional-analytic frameworks for Lorentz maps and flows provide anisotropic spaces, spectral gaps, perturbation stability, and exponential mixing.

The present manuscript does not supersede those theories. Its contribution is more specific: it works directly with a mixed physical record, exhibits exact periodic arithmetic for a concrete triangular family, detects a raw density edge that a smoothed/test-function theorem can hide, and proves a first-order parameter-uniform mechanical clock. Those are worthwhile modules.

What is still missing is exactly the integration of these modules with the existing operator theories: a common space for the unbounded induced observables, regularity sufficient to pass from spectral coboundaries to periodic obstructions, quantitative large-frequency estimates, covariance control, and a global residual decomposition. The manuscript's own realization section accurately identifies this boundary.

## 9. Top-four significance assessment

At the requested benchmark, a collection of preparatory modules normally requires one of two forms of closure:

1. a completed theorem of correspondingly broad importance, here the parameter-uniform raw mixed-density LLT and its conditioned physical-time consequences; or
2. a new general principle whose independent significance transcends the target theorem, for example a theorem converting explicit periodic phase separation into a robust spectral estimate for singular billiard families.

The current manuscript supplies neither form of closure. Its strongest new arithmetic theorem remains disconnected from the operator norm needed for inversion. Its edge theorem exposes a genuine obstruction but does not complete the global branch sum. Its clock theorem is first order and built from compactness, finite-record continuity, Kac normalization, and renewal inversion. These are valuable, but not in my judgment field-transforming at the level expected by *Annals*, *Acta*, *Inventiones*, or *JAMS*.

This assessment should not be read as a recommendation to weaken or delete the results. A strong specialist paper could be organized around the explicit periodic family, quantitative phase separation, raw edge obstruction, and first-order clock, with the unfinished LLT clearly presented as motivation rather than as the implicit measure of completion. A future top-four resubmission should close the operator/cohomology/covariance/residual chain.

## 10. Required changes for a specialist submission or future resubmission

1. **Choose the paper's endpoint explicitly.** Either complete the uniform raw LLT, or present this as a self-contained module paper whose main theorem is the combined quantitative arithmetic/edge/clock package.
2. **Expand the moving-domain continuity proof.** The branchwise `L^1` density continuity under parameter variation deserves a standalone lemma with precise common charts, excluded singular neighborhoods, and quantitative domination.
3. **State the phase-to-operator gap in theorem form.** The current prose is accurate, but a boxed dependency statement would prevent readers from mistaking periodic separation for a Dolgopyat estimate.
4. **Keep individual-edge and all-edge statements separate.** The exponential coefficient bound is per word; no uncontrolled symbolic multiplicity should enter a global conclusion.
5. **Separate first-order and square-root clocks.** The downstream CLT/LLT transfer should continue to display the additional `o_P(\sqrt t)` residual and conditional estimates.
6. **Repair version identity.** The latest public branch says v5 while all manuscript metadata, directory names, and workflow contracts say v4. Since both branches point to the same SHA this does not corrupt the reviewed source, but it should be normalized before journal submission.
7. **Add a dynamics-specific external proof check.** The periodic action, moving-return-domain coarea argument, and uniform stationary clock should be read by an independent billiards specialist.

## 11. Source qualification and reproducibility

The exact-source workflow attached to the reviewed SHA ran on the equivalent v4 branch:

- run ID: `37253620285`;
- workflow: `A2-DYN v4 exact-source qualification`;
- head SHA: `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`;
- status: `completed`;
- conclusion: `success`.

Exact checkout, TeX dependency installation, source and finite checks, native build, and artifact upload all succeeded. The artifact is:

- artifact ID: `11321513463`;
- digest: `sha256:a7948de353a64a1221acfae8ef7da81d05e9496856fc8d7c24b19d5d3393819f`.

The downloaded receipt records:

- core tree `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`;
- native build passed;
- PDF SHA-256 `e331e99dc9ee15afe415642497edf4a9d8fd3ab6bd7bd4d0d889a15125a0c1da`;
- source and finite checks passed;
- full raw LLT verified: false;
- independent human review: false.

The source audit records 29 pages, 37 proof bodies, 107 labels, preservation of all 28 v3 proofs and 78 labels, 437 current finite checks, and the retained finite winding, excursion, v1, and v2 diagnostics. This is strong source evidence, not continuum proof certification.

## 12. Independent diagnostics and limits of this review

The accompanying `verify_review.py` imports no author code and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256

`e67223c611df7ed74a1383b803b92fdd3ee5033f01a31bcbd205dc096a51efd8`.

It records 471,556 successful checks covering:

- the unimodular four-record matrix;
- the exact five-dimensional determinant `2(sqrt(3)-1)`;
- the logarithmic period selection and printed polynomial phase exponent;
- the alternating-orbit Hessian determinant and edge coefficient;
- the one-sided `1/|b|` Fourier tail and individual-word edge bound;
- mean-free-flight, collision-rate, and derivative formulas;
- exact finite length-bias truncation inequalities;
- finite renewal-inversion models;
- the frequency-splice feasibility inequalities;
- the compact-subadditive block bookkeeping.

These checks support finite algebra and models only. They do not prove the optical-action estimates in the continuum, the moving-domain coarea theorem, a measurable Livšic result, a common anisotropic operator family, covariance nondegeneracy, all-branch residual summability, or the full raw LLT. I did not perform an exhaustive priority search or a physical experiment.

## 13. Final verdict

**Source identity:** unambiguous by SHA; the latest v5 branch is an alias of the v4 manuscript.

**Mathematical audit:** no fatal counterexample found in the audited arithmetic, edge, fixed-return, or first-order clock modules; several continuum steps merit independent specialist review.

**Source delivery:** successful exact-SHA build and archived evidence.

**Editorial assessment:** rigorous and potentially publishable specialist-level progress, but the manuscript stops before the operator, covariance, all-branch residual, and conditioned-clock theorems that would close its central raw-LLT objective. The existing modules do not independently meet the exceptional conceptual threshold of the requested four journals.

**Recommendation: reject at the Annals / Acta / Inventiones / JAMS benchmark.**
