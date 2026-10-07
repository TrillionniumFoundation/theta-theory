# External top-four referee report on A2-DYN revision 33

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v33-referee-response-2026-10-07`, `revision/a2-dyn-v33-referee-copy-2026-10-07`  
**Reviewed commit:** `13af9a5795503671a18b5c261e79d61e87ae8bd6`  
**Reviewed repository tree:** `60f153775ba1e562d681d58524600d701346939b`  
**Frozen ordinary paper tree:** `42ba62ef825d1e555f6c6bf83e647792bba67de8`  
**Active manuscript directory:** `papers/A2-DYN-v33-referee-response`  
**Active mathematical source:** sixty-eight numbered core modules; revision 33 adds modules 67--68  
**Qualified revision-32 baseline:** `f63fb5101c8bcf6202abf4468d703be6242923a1`  
**Baseline ordinary paper tree:** `d6462c94e0cb7a702bf4e46e60da0440fb94a5ac`  
**Controlling report:** `reviews/a2-dyn-v32-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `c41e23ea3494aaa40502aed990c6d46b9bce1153` / `9b25d7264504a0cf214d0e473281010505713310`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 33 is a genuine mathematical revision. It responds directly to the most important distinction in the revision-32 report: the preceding-section return event and the original stationary physical observation are different microscopic events. The new source treats

\[
\{W_R(t)=k,\ C_R(t)=m\}
\]

directly at a deterministic physical observation time and prescribed physical collision count. It retains the initial and terminal within-flight cell corrections, integrates the true stationary flight age, obtains an exact three-frequency inverse, proves a uniform all-label second-distributional-derivative bound for the physical-time profiles, and converts that bound into a pointwise `O(B^{-1})` far-time-frequency error with a polynomial bandwidth. It also derives a positive likelihood on the original trajectory space with unnormalized source-total-variation error `O(B^{-1})`, uniformly against bounded measurable selectors.

The second new module evaluates the actual three-dimensional Gaussian central contribution. The two endpoint roof weights, the smoothing and unsmoothing costs, the covariance replacement, the rescaled integration volume, and the physical covariance Jacobian are all paid explicitly. On the parts audited below, I found no decisive counterexample, missing normalization factor, or sign inconsistency in these new calculations. In particular, the five polynomial exponents printed in the two-roof estimate and the identity

\[
\det \mathcal V_R=\frac{\det\Sigma_R}{\bar\tau_R^5}
\]

are consistent with the stated scales.

These are meaningful advances. They should not be described as a relabeling of revision 32 or as merely formal bookkeeping.

The negative recommendation is instead forced by the exact conclusion of the new theorem. Revision 33 proves a pointwise identity of the form

\[
t^{3/2}p_{m,R}(k,t)
 =g_{\mathcal V_R}(\xi)
  +t^{3/2}\mathfrak M_{m,R,B_m}(k,t)+o(1),
\]

where `\mathfrak M` is the signed inverse over every frequency outside the shrinking central ball and inside the polynomial time-frequency cutoff. No estimate proving

\[
 t^{3/2}\mathfrak M_{m,R,B_m}(k,t)\longrightarrow0
\]

is supplied. The manuscript explicitly states that the microscopic Gaussian denominator is equivalent to this vanishing on central compact sets. Thus the outstanding term is not a secondary remainder after the main local theorem; it is precisely the unresolved noncentral and middle-frequency part of that theorem.

Moreover, this direct physical calculation does not prove the advertised four-coordinate raw local limit theorem for the actual return record. The common pointwise correction and finite complement for that return law remain open, as do the evaluated weighted middle transform and a positive denominator for selected path events.

At the requested benchmark, a reduction of the central theorem to one explicit signed integral is valuable infrastructure but not a completed top-four result. The paper still lacks either

1. the unconditional raw mixed-density local theorem that organizes the article, or
2. a new general principle of comparable independent scope that controls the remaining signed complements for singular hyperbolic systems.

## 2. Frozen source, chronology, and qualification

Both named revision-33 author branches resolve to

`13af9a5795503671a18b5c261e79d61e87ae8bd6`.

The source manifest identifies revision 32 as the frozen mathematical baseline. All sixty-six inherited core modules, all seventy-one inherited Python files, all inherited mathematical labels, and the bibliography are retained byte-for-byte. Revision 33 adds

- `core/67_exact_stationary_endpoint_inversion.tex`;
- `core/68_stationary_gaussian_complement.tex`.

Five replayable edits to `main.tex` update the revision identity, extend the abstract, insert introductory Theorem X, include the two new modules, and add a short comparison paragraph. The previous abstract is retained separately. The source ledger correctly distinguishes the new physical endpoint theorem from Theorem W for the preceding-section return record.

The exact-source qualification runs completed successfully on both reviewed branches:

- response branch run `37616590047`;
- referee-copy branch run `37616637895`.

The validation protocol checks the complete source identity, the frozen revision-32 tree, inherited labels, edit replay, normal and optimized finite diagnostics, native TeX compilation, and rendering of the new proof interval. The manuscript reports a 213-page article. These are meaningful provenance and reproducibility checks. They do not certify the continuum billiard arguments, the spectral estimates, or the missing middle-frequency bound.

The present review branch starts from the reviewed author commit and adds this report only under

`reviews/a2-dyn-v33-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, prior review, or unrelated path is intentionally modified.

## 3. Scope of this review

I have not attempted to re-prove every inherited statement in a 213-page article with sixty-eight core modules. The substantive audit concerns

1. the exact stationary overlap and cell-correction formula in module 67;
2. the all-label time-regularity and pointwise far-frequency estimates;
3. the positive source likelihood and arbitrary-selector statement;
4. the endpoint-weighted three-dimensional central estimate in module 68;
5. the Gaussian normalization and the conversion from collision count to physical time;
6. the logical status of the signed middle complement;
7. the response to the six principal obligations in the revision-32 report;
8. source identity and successful exact-SHA qualification.

The inherited covariance, collision-space spectral splitting, smoothing estimates, phase arithmetic, return reconstructions, geometric extraction, and positive finite-band theorem are treated as the qualified revision-32 baseline. This does not turn earlier AI-assisted reviews or successful diagnostics into formal proof certification.

## 4. Exact stationary source and cell corrections

The stationary current-collision coordinates are written as

\[
 d\mathbb P_R(x,a)=\bar\tau_R^{-1}d\nu(x)\,da,
 \qquad 0\le a<\tau_R(x).
\]

This is the correct suspension probability over the collision map. The new proof does not replace it by the normalized section law or by an unbiased entrance distribution.

For a fixed bounded convex polygonal fundamental cell, uniform finite horizon implies that a lifted physical flight meets only a fixed finite set of cell translates. The intersection with each translate is an interval, apart from endpoint conventions and the null family of flights running along a cell edge. This justifies the finite family `I_{R,d}(x)` without differentiating cell-crossing times.

If `C_R(t)=m`, the terminal state and age are

\[
 y=T_R^m x,
 \qquad v=t+a-S_{m,R}(x),
 \qquad 0\le v<\tau_R(y),
\]

and the manuscript keeps the exact identity

\[
 W_R(t)=K^{\rm c}_{m,R}(x)+d_R(y,v)-d_R(x,a).
\]

Both within-flight terms are indispensable at singleton lattice resolution. Their presence is one of the strongest features of the revision. The formula does not use an `O(1)` replacement that would be harmless only on a macroscopic scale.

For initial and terminal intervals `I,J`, integrating the initial age produces

\[
 H_{I,J}(s)=\int \mathbf 1_I(a)\mathbf 1_J(s+a)\,da
           =\mathbf 1_{-I}*\mathbf 1_J(s).
\]

Substitution gives the displayed exact probability formula for `p_{m,R}(k,t)`. I found the age signs and lattice signs consistent with the Fourier amplitudes used later.

## 5. Uniform time-profile regularity

The overlap kernel is continuous and piecewise affine. In distributional form,

\[
 \|H_{I,J}\|_1=|I||J|,
 \qquad \|H'_{I,J}\|_1\le2|I|,
 \qquad \|D^2H_{I,J}\|_{\rm TV}\le4.
\]

After summing over the output lattice label, every initial-terminal cell pair is counted once. The interval partitions then give the claimed uniform bounds

\[
 \sum_k\|p_{m,R}(k,\cdot)\|_1\le A_0,
 \quad
 \sum_k\|\partial_t p_{m,R}(k,\cdot)\|_1\le A_1,
 \quad
 \sum_k\|D_t^2p_{m,R}(k,\cdot)\|_{\rm TV}\le A_2.
\]

The constants are independent of the prescribed collision count. No count of long collision words appears. This is an important simplification relative to the return-density extraction.

The source-level translation argument also gives

\[
 \sum_k|p_{m,R}(k,t)-p_{m,R}(k,s)|\le L_0|t-s|.
\]

The proof correctly includes changes of the fixed count event: outside the terminal flight-age interval the indicator is zero. The zero extension to negative observation times is compatible with the same translation estimate.

The manuscript is careful to call `D_t^2p` a finite signed measure, not an `L^1` function. This distinction must remain explicit. The finite diagnostics cannot replace the distributional argument, but their negative control for this distinction is appropriately scoped.

## 6. Absolute inversion and the polynomial far tail

The initial and terminal flight amplitudes are finite sums of interval integrals. Therefore

\[
 |A_R^\pm(x;u,b)|
 \le \min\{\tau_+,2J_*/|b|\}.
\]

Their product decays as `|b|^{-2}`, uniformly in the intervening collision count and in the spatial torus frequency. Since the spatial torus has finite volume, the exact three-frequency inverse is absolutely convergent.

The stronger summed estimate uses the distributional second derivative:

\[
 \sum_k|\widehat p_{m,R}(k,b)|
 \le \frac{A_2}{b^2}.
\]

Integrating `|b|>B` with the one-dimensional inverse factor gives

\[
 \sum_k\|p_{m,R}(k,\cdot)-p^{\rm sharp}_{m,R,B}(k,\cdot)\|_\infty
 \le \frac{A_2}{\pi B}.
\]

The normalization is correct. There is no additional factor equal to the number of attainable lattice labels, because the sum is taken before the tail integral.

Consequently `B_m=m^{P+3/2}` makes the normalized far-time-frequency error `O(m^{-P})`. This is a genuine pointwise estimate and a substantial improvement over the preceding-section reconstruction, whose sufficient bandwidth may be `exp(O(n log n))`.

The scope is nevertheless narrow and exact: the estimate controls only the large `|b|` tail for the original stationary endpoint at fixed physical collision count. It supplies no decay for the complete region

\[
 u\in\mathbb T^2,
 \qquad |b|\le B_m,
 \qquad |(u,b)|>r_m.
\]

All noncentral spatial frequencies remain in that region.

## 7. Positive likelihood and bounded selectors

Convolution in the observation-time variable with the positive compact-Fourier-support kernel produces a likelihood between zero and one on the original stationary trajectory space. The source translation estimate yields

\[
 \|\mathbf 1_A-\lambda_{A,B}\|_{L^1(\mathbb P_R)}
 \le C/B.
\]

This is stronger than a scalar probability comparison. Multiplication by any bounded measurable trajectory statistic contracts the unnormalized source error, so the arbitrary-selector statement is valid without differentiating the selector.

The manuscript correctly refrains from claiming that the initial weighted amplitude has `1/|b|` decay for an arbitrary selector. It also correctly divides by an actual denominator before making any posterior statement.

This result is therefore an **absolute reconstruction theorem**, not a weighted local limit theorem. For a selected event, the following remain separate obligations:

- evaluate the weighted finite Fourier integral;
- control its weighted middle-frequency part;
- prove a positive denominator for the selected event;
- only then normalize to obtain a relative conditional law.

The unselected Gaussian central term cannot provide these conclusions for every selector.

## 8. The two-roof central comparison

The centered three-coordinate collision record is

\[
 f_R^{\rm c}=(\kappa_{R,1},\kappa_{R,2},\tau_R-\bar\tau_R)
            =P_Rh_R,
\]

and

\[
 \Sigma_R=P_R\Gamma_RP_R^{\mathsf T}.
\]

Because the inherited joint covariance is uniformly positive definite and `P_R` has full row rank, the stated uniform ellipticity of `\Sigma_R` follows.

After smoothing the collision record and both endpoint roof weights, the endpoint-weighted transform is represented by the collision transfer operator for `m` steps. The proof pays two endpoint norm costs and one projector difference. The printed pointwise error has the form

\[
 C\left[
 \delta+|v|\sqrt{\delta\ell_\delta}
 +|v|^2\delta\ell_\delta
 +m^{-1/2}\delta^{-6}(|v|+|v|^3)
 +\delta^{-4}\rho^m
 \right].
\]

With `\delta=m^{-1/14}/4` and a three-dimensional rescaled ball of radius `2m^{1/200}`, direct integration gives the five polynomial margins

\[
 \frac{79}{1400},\quad
 \frac{11}{700},\quad
 \frac{13}{280},\quad
 \frac9{175},\quad
 \frac{29}{700}.
\]

The slowest is `11/700`, exactly as stated. The two analytic smallness inequalities also have strict positive margins. I found the exponent arithmetic coherent.

Replacing the exact single-flight amplitudes by the endpoint roofs costs

\[
 O\!\left(m^{-1/2}
   \int_{|v|\le2m^{1/200}}|v|\,dv\right)
 =O(m^{-12/25})
\]

on the normalized scale. This is smaller than the retained central error.

For a future revision, I recommend displaying one explicit transfer-operator identity with the adopted convention before the spectral splitting. The present sentence that the pairing is “exactly” the displayed operator expression is plausible and consistent with the inherited convention, but it is load-bearing and should not require the reader to reconstruct the direction of composition across several earlier modules.

## 9. Gaussian normalization and physical covariance

The two endpoint roofs have mean `\bar\tau_R`. Their product contributes `\bar\tau_R^2`, and division by the stationary suspension mean leaves the factor `\bar\tau_R` in

\[
 m^{3/2}G^{\rm cen}_{m,R}(k,t)
 =\bar\tau_R g_{\Sigma_R}
   \left(\frac{k}{\sqrt m},
         \frac{t-m\bar\tau_R}{\sqrt m}\right)
 +o(1).
\]

This normalization is correct.

For physical scaling, the manuscript sets

\[
 D_R^{\rm clk}=\operatorname{diag}(1,1,-1/\bar\tau_R),
 \qquad
 \mathcal V_R=\bar\tau_R^{-1}
 D_R^{\rm clk}\Sigma_R(D_R^{\rm clk})^{\mathsf T}.
\]

The determinant identity

\[
 \det\mathcal V_R=\det\Sigma_R/\bar\tau_R^5
\]

follows. The matrix

\[
 A_R=\sqrt{\bar\tau_R}
       \operatorname{diag}(1,1,-\bar\tau_R)
\]

satisfies `A_R\mathcal V_RA_R^{\mathsf T}=\Sigma_R` and has absolute determinant `\bar\tau_R^{5/2}`. This gives the physical Gaussian `g_{\mathcal V_R}` with no omitted covolume in the integer cell coordinates.

Possible parity, arithmetic, or peripheral resonances are not erased by this calculation. They remain in the signed middle complement. That is the correct logical allocation.

## 10. The unresolved signed middle integral

The new complement is

\[
 \mathfrak M_{m,R,B}(k,t)
 =\frac1{(2\pi)^3\bar\tau_R}
  \int_{\substack{u\in[-\pi,\pi]^2,\ |b|\le B\\ |(u,b)|>r_m}}
  e^{-i(u\cdot k+bt)}\mathcal F_{m,R}(u,b)\,db\,du.
\]

It contains

- every nonzero and noncentral spatial torus frequency;
- the annular region adjacent to the shrinking central ball;
- all intermediate time frequencies up to the polynomial cutoff;
- all arithmetic or peripheral resonances not already excluded by a proved operator estimate;
- any cancellation needed between these regions.

The manuscript proves neither an absolute integral bound nor a direct oscillatory cancellation theorem for this complete domain. Calling the term “signed” does not make it small. A signed inverse may indeed exhibit cancellation, but that cancellation must be proved uniformly in the radius and the central target.

The exact identity

\[
 t^{3/2}p_{m,R}(k,t)
 =g_{\mathcal V_R}(\xi)
  +t^{3/2}\mathfrak M_{m,R,B_m}(k,t)+o(1)
\]

is useful because it eliminates discarded-density and event-replacement errors. It also shows with unusual clarity that the remaining task is the local theorem itself.

The statement that the microscopic Gaussian denominator is equivalent to vanishing of the normalized complement is correct for the specified bandwidth and central compact sets. It is not an unconditional denominator theorem, and it gives no mechanism proving either side.

Neither the positive kernel approximation nor global source total variation can fill this gap. Small global mass or small unnormalized source error does not control the value of a density at a microscopic singleton after multiplication by `t^{3/2}`.

## 11. Status of the revision-32 obligations

The revision-32 report identified six principal obligations. Revision 33 changes their status as follows.

### 11.1 Evaluate or eliminate the finite complement

**Partially advanced, not closed.** The physical far-time-frequency tail is eliminated at polynomial bandwidth and the central contribution is evaluated. The finite signed middle integral is not estimated. The corresponding complement for the four-coordinate return record also remains open.

### 11.2 Obtain a pointwise local correction rather than only global `L^1`

**Closed only for the direct physical far tail.** The `C/B` bound is genuinely pointwise in observation time. It is not the common pointwise correction required for the original four-coordinate return density.

### 11.3 Prove a microscopic Gaussian denominator

**Not closed.** The Gaussian central term and correct normalization are proved. The denominator asymptotic remains equivalent to the unproved vanishing of the middle complement.

### 11.4 Treat the original microscopic physical-time event

**The representation problem is closed; the local theorem is not.** Revision 33 directly represents the original event, so no preceding-section replacement is used in this route. The route still needs the middle estimate. If the article continues to use the return route elsewhere, the relative return-to-physical comparison at microscopic denominator scale also remains a separate issue.

### 11.5 Close the downstream selector class

**Closed in absolute source total variation, not in normalized local form.** Every bounded selector is allowed in the reconstruction estimate. The weighted middle transform and selected denominator remain unproved.

### 11.6 Independent specialist audit

**Not closed.** No independent human billiards, transfer-operator, or harmonic-analysis review is supplied. The finite diagnostics are appropriately disclaimed.

Thus revision 33 materially advances obligations 1--5 but does not complete the mathematical endpoint attached to any of them.

## 12. Relation to the original return-density theorem

The paper’s title, abstract, and historical architecture concern the four-coordinate record of actual returns

\[
 J_{n,R}=(K_{n,R},N_{n,R},T_{n,R}).
\]

Theorem X instead concerns a prescribed physical collision count at deterministic physical time. This is not a defect; it is a natural and useful observable. But it is a different local problem.

The flight-age overlap succeeds because two bounded endpoint intervals supply inverse-square decay in the time frequency. The four-coordinate return density does not automatically inherit this mechanism. In particular, revision 33 does not prove

- the common pointwise return correction;
- the complete return-frequency complement estimate;
- the full parameter-uniform raw mixed-density return LLT;
- its arbitrary weighted inserted versions.

A future paper must make the logical endpoint unambiguous. If the four-coordinate return LLT remains the principal theorem, it must actually be proved. If the direct physical fixed-count theorem is intended as a second route to the conditioned physical-time conclusions, the missing middle estimate and the passage from fixed count to the intended observation/conditioning statement must be completed without treating the return theorem as already available.

## 13. Top-four significance and editorial assessment

The exact age-overlap mechanism is elegant. It removes a genuine obstruction that survived the previous reconstruction: the original stationary endpoint now has a direct pointwise far-frequency theorem with no geometric removal and no super-exponential cutoff. The endpoint-weighted central comparison is also a nontrivial use of the inherited collision spectral machinery.

Nevertheless, the mathematical claim available after 213 pages is still a system of Gaussian, reconstruction, and reduction theorems surrounding an open raw local theorem. The new middle complement contains the difficult noncentral dynamics. No new argument in revision 33 controls it.

At the level of *Annals*, *Acta*, *Inventiones*, or *JAMS*, one normally expects the manuscript’s central probabilistic theorem to be complete, or else a general method whose standalone impact clearly exceeds the target application. The present revision does not yet meet either standard.

The exposition also reflects cumulative revision history rather than a final top-four article. There are sixty-eight numbered modules, introductory theorems running through Theorem X, numerous status maps and proof ledgers, and repeated distinctions among return, stationary, positive, weighted, source-TV, global-`L^1`, and pointwise statements. These distinctions are mathematically necessary, but the present organization makes the principal theorem and the remaining gap harder to see than they should be. Successful closure should be followed by a substantial conceptual rewrite rather than another additive layer.

## 14. Required mathematical changes before a further top-four submission

1. **Control the physical signed middle complement.** Prove, for one explicit polynomial bandwidth and uniformly on compact physical central sets,
   \[
   \sup t^{3/2}|\mathfrak M_{m,R,B_m}(k,t)|\to0.
   \]
   The proof must cover the entire noncentral spatial torus and every intermediate time-frequency regime, including possible arithmetic resonances.

2. **Supply an actual mechanism, not only an equivalence.** A useful proof may combine compact-frequency spectral gaps, quantitative peripheral estimates, anisotropic high-frequency bounds, and an explicit splice. The constants and overlap of the regions must be checked on the same operator family and in the pointwise norm required by the theorem.

3. **Close the weighted physical theorem.** For the selectors used downstream, evaluate the weighted middle transform and prove the selected denominator. Absolute source-TV contraction alone is insufficient for conditional laws on microscopic events.

4. **Complete the original four-coordinate return LLT.** The direct physical theorem does not establish the advertised raw mixed-density theorem for `J_{n,R}`. Its common pointwise correction and full finite complement remain to be controlled, including the weighted insertion class.

5. **Clarify the route to physical conditioning.** State exactly whether the final conditional path theorem is obtained from the return LLT plus a microscopic bridge, or from the direct fixed-count physical LLT plus a summation/localization in `m`. Every event replacement must be controlled relative to the actual denominator.

6. **Obtain independent specialist verification.** The collision geometry, the long inherited transfer-operator chain, and the new endpoint-weighted central estimate should be checked by specialists independent of the author-side construction.

7. **Rewrite the completed argument as one paper rather than a revision archive.** Once the central estimates are proved, compress duplicated interfaces, move provenance ledgers outside the article, reduce the number of headline theorems, and present one transparent dependency chain from collision dynamics to the final local theorem.

## 15. Technical and presentation comments

1. In the two-roof comparison, display the exact transfer identity with the paper’s composition convention before invoking the spectral decomposition.
2. State the dependence of `J_*` on the chosen fundamental cell and the uniform horizon once, then keep it fixed throughout the physical endpoint section.
3. Keep emphasizing that `D_t^2p` is a measure. Avoid shorthand elsewhere that could be read as a `W^{2,1}` statement.
4. Qualify every “equivalence to the denominator theorem” by the chosen bandwidth, the unweighted event, and the fixed compact central set.
5. Distinguish uniformity in all `k,t` for the central inverse estimate from the central scaling assumption used to convert it to the physical Gaussian.
6. The title “Exact microscopic stationary observations” for Theorem X may be read as announcing the microscopic LLT. A phrase such as “exact inversion and Gaussian-plus-complement reduction” would communicate its proved scope more precisely.
7. The abstract is accurate but too long and too ledger-like for a final journal submission. It should state the main unconditional theorem first and list no more than the principal remaining caveat.
8. The article should not use successful finite diagnostics as evidence for the missing middle-frequency dynamics. The current validation files do not make that overclaim and should remain so limited.

## 16. Final assessment

Revision 33 makes real progress and resolves an important representational error risk: the original stationary physical endpoint is now analyzed with the true initial age and both cell offsets. The pointwise `B^{-1}` far tail and the evaluated three-dimensional central term are worthwhile results. I found the new calculations internally coherent on the passages audited.

The manuscript nevertheless stops at an exact Gaussian-plus-signed-complement identity. The signed complement contains the whole unresolved noncentral local-limit problem, and the four-coordinate return LLT remains open as well. The microscopic denominator and the normalized weighted conditional theorems therefore do not follow.

For these reasons I recommend rejection at the requested top-four benchmark in the present form. A substantially different assessment would be warranted only after the physical and return middle-frequency complements, the selected denominators, and the final local conditioning chain are proved rather than isolated as criteria.