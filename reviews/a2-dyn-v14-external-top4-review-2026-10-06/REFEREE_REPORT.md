# External top-four referee report on A2-DYN revision 14

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v14-referee-response-2026-10-06`, `revision/a2-dyn-v14-referee-copy-2026-10-06`  
**Reviewed commit:** `cac1a5f9ece9a8a63e69fcfb2156768337790034`  
**Reviewed repository tree:** `c5013ff28abb35900c18d290bd7ea3e8d24d148a`  
**Active manuscript directory:** `papers/A2-DYN-v14-referee-response`  
**Reviewed v13 author baseline:** `47d2430dc14c4d98a9e80db6fd573b049be8808c`  
**Controlling v13 report:** `reviews/a2-dyn-v13-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `014dbfa28501551a30388b44c0509fb7fbfbc444` / `0b505155503326568196c422034107cbfa8fc5ed`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 14 is a genuine and important mathematical revision. It closes the first major blocker in the preceding report: the manuscript now proves uniform positive definiteness of the full four-dimensional covariance of the actual return record, rather than positivity of only the collision-count coordinate.

The new proof is not a restatement of the earlier periodic-rank criterion. It introduces a different route designed specifically for the fact that the zero-variance transfer function is only an `L^2` class and cannot be evaluated at prescribed periodic points. The argument derives an exact collision action one-form, obtains stable and unstable holonomy identities for a merely measurable circle phase on positive-measure hyperbolic product sets, uses symplectic area to eliminate a nonzero roof coefficient, uses two- and three-rotation products to eliminate a nonintegral constant phase, and uses ergodicity of a finite physical cover to rule out a real spatial collision coboundary. The integer-valued section contribution is removed algebraically before the physical symmetries are applied.

I found no decisive counterexample in this proof chain. The action-form signs are coherent, the conditional-pair approximation does not require pointwise regularity of the measurable phase, the four-corner cancellation uses the correct product-measure logic, the triangular rotation identities give the advertised constant-phase cancellation, and the finite-cover invariant contradicts ergodicity exactly as claimed. The final passage from pointwise positive definiteness to a uniform lower eigenvalue uses only the already proved continuity of the covariance and compactness of the radius interval.

This is a substantial advance. It removes covariance nondegeneracy from the hypotheses of the central inversion interfaces and gives a genuinely nondegenerate limiting Gaussian for the original four-coordinate record.

The negative recommendation is therefore not based on source failure, version ambiguity, mathematical vacuity, or a detected fatal flaw in Theorem E. It is based on the fact that the organizing endpoint of the paper remains the parameter-uniform raw mixed-density local limit theorem, while two central analytical mechanisms and the exact-conditioning extension remain unproved:

1. an integrated estimate on the complete complementary-frequency region outside the proved growing central ball;
2. a complete critical/singular branch extraction with quantitative residual derivative sums and local-edge estimates;
3. weighted complementary tails, weighted edge estimates, and relative event replacement for the exact physical conditioning application.

The new measurable phase rigidity is qualitative. It excludes exact unit-modulus phases, but it does not reconstruct a regular phase from an approximate spectral vector, prove a quantitative induced resolvent estimate, or control the integrated transform on the annulus and high-frequency regions needed for raw inversion. Likewise, uniform ellipticity controls the tail of the limiting Gaussian, not the complementary transform of the physical record or its edge-subtracted residual.

At the requested benchmark, proving the nondegenerate Gaussian, moments, growing central integrals, and marked insertions while leaving the full complementary-frequency and global raw-branch mechanisms conditional is not sufficient for acceptance of a paper organized around a raw LLT. The unconditional package is nevertheless mathematically substantial and could support a strong specialist publication after independent expert verification and a reorganization around the theorems that are actually complete.

## 2. Frozen source, chronology, and qualification

The two named revision-14 author branches resolve to the same commit:

`cac1a5f9ece9a8a63e69fcfb2156768337790034`.

The revision descends from the v13 review commit in two steps. The intermediate staging commit is

`34639ee5f62de16e0e9b71e4a73f65f71c105898`,

and the reviewed child is the complete ordinary-source revision. The one-time assembly workflow is removed at the reviewed SHA; the exact qualification workflow is read-only.

Revision 14 adds two mathematical modules:

- `core/32_measurable_phase_rigidity.tex`;
- `core/33_joint_nondegeneracy.tex`.

It retains all thirty-one inherited core modules and all inherited mathematical labels. Twenty-three inherited core files, all inherited diagnostic scripts, and the bibliography are byte-identical. The remaining inherited edits are listed as exact, replayable replacements in `INHERITED_EDITS.json`; they update revision identity, theorem dependencies, cross-references, and the status of covariance nondegeneracy without deleting inherited theorems.

The source manifest identifies the v13 author baseline, the controlling v13 report commit and blob, the baseline and revised hashes, the new core hashes, and the fact that the full raw LLT is not claimed proved.

The exact-source workflow completed successfully on both reviewed author branches at the reviewed SHA:

- response branch run `37416098651`;
- referee-copy branch run `37416112991`.

For the response branch, exact checkout, source archive, verification/build, and artifact upload all completed successfully. The qualification artifact is

`11390879549`,

named

`a2-dyn-v14-cac1a5f9ece9a8a63e69fcfb2156768337790034`,

with digest

`sha256:27e82ce59d2004a20ca8829ecbbbc5ddb1fe8f3f91208dc59a820129c9dee3cb`.

These facts establish source identity and successful execution of the declared build and finite checks. They do not certify the continuum local-product, disintegration, finite-cover, or raw-density arguments.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v14-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier review, or unrelated repository path is modified.

## 3. What revision 14 actually proves

Let

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

be the bounded collision compensation and let `D_R` be the covariance already obtained from the collision Green--Kubo formula and the exact stopping identity.

The inherited kernel theorem states that a real direction has zero Gaussian variance if and only if the corresponding collision observable is an `L^2` coboundary. For a joint direction

\[
 v=(w,a,b),\qquad w\in\mathbb R^2,
\]

this gives

\[
 w\cdot\kappa_R+a+b\tau_R-\zeta\eta_R
   =B-B\circ T_R,
\qquad
 \zeta=\frac{a+b\bar\tau_R}{c_*}.
\]

Revision 14 proves that this identity forces `v=0`.

Its new unconditional conclusions are:

- an exact action identity
  \[
  d\tau_R=T_R^*(Rp\,d\alpha)-Rp\,d\alpha
  \]
  on every regular collision branch;
- stable and unstable holonomy formulas for merely measurable circle phases on a positive-measure product set;
- exclusion of every nonzero roof coefficient by a symplectic-area obstruction;
- exclusion of every nonintegral constant collision phase by two- and three-rotation products;
- absence of a nonzero real spatial collision coboundary by a finite-cover ergodicity argument;
- positive definiteness of `D_R` for each radius and uniform ellipticity on the compact radius interval;
- eventual ellipticity of the actual normalized finite-return covariance;
- uniform positive definiteness of the projected physical-time covariance;
- a uniformly defined four-dimensional Gaussian density and an exponentially small tail for the limiting Gaussian outside the growing central ball.

The theorem does not estimate the physical characteristic function outside the central ball and does not supply the all-branch raw residual bounds.

## 4. Audit of the qualitative billiard input

The load-bearing geometric import is the local product structure for finite-horizon dispersing billiards. I checked the cited primary source, Young's 1998 *Annals* paper, at Sections 8.1--8.3 rather than relying only on the manuscript's source map.

Section 8.1 treats billiards on a two-torus with pairwise disjoint `C^3` strictly positively curved scatterers and finite horizon. It records ergodicity of every positive power of the collision map and states the exponential-mixing theorem for this class. Sections 8.2B--8.2D give transverse invariant cones, adapted expansion/contraction, homogeneity strips, and homogeneous local stable and unstable curves. Section 8.3 constructs a positive-measure hyperbolic product set and verifies the absolute-continuity properties used in the tower construction.

The triangular Lorentz family and the finite physical covers used in revision 14 fit this qualitative class: the scatterers are disjoint circles with positive curvature, the Euclidean reflection law is unchanged, and finite horizon is inherited by the cover. The manuscript does not introduce an affine distortion of reflection.

The article uses more than the bare existence of stable and unstable manifolds. It needs a compact positive-measure product set on which:

- stable and unstable arcs remain on regular homogeneous branches in the relevant time direction;
- their ordinary lengths tend to zero;
- the restricted collision measure is in the same measure class as a product of nonatomic transversal measures;
- almost every four-corner product quadrilateral is simple and nondegenerate.

The manuscript explains how these properties are obtained by restricting the Young product set away from grazing and using both forward and reverse holonomy absolute continuity. I found that explanation plausible and consistent with the cited source. It remains a proper target for independent billiards-specialist review, especially the passage from the two holonomy formulas to the stated product measure class on the restricted compact set.

No uniformity in the radius is imported at this stage. This is appropriate: the final uniform lower eigenvalue is obtained only after pointwise kernel exclusion, using continuity and compactness.

## 5. Audit of the exact action identity

The physical one-form is

\[
 \vartheta_R=Rp\,d\alpha.
\]

On a fixed regular flight branch, lift the flight to its actual initial and terminal disks. Differentiation of the Euclidean flight length gives the terminal tangential contribution minus the initial tangential contribution. Specular reflection preserves the tangential component at arrival. Since the lattice label is constant on the branch, it contributes no differential. Thus

\[
 d\tau_R=T_R^*\vartheta_R-\vartheta_R.
\]

Summing this identity along a regular arc gives the forward telescoping formula. Applying it to the backward image of an unstable arc gives the backward formula. I checked the signs in both identities; they lead to the same sign in the stable and unstable holonomy formulas later in the proof.

The one-form is bounded on the collision cylinder. Contraction of homogeneous stable arcs forward and unstable arcs backward therefore makes the terminal action integrals vanish. The use of a small regular coordinate box avoids the angular seam and collision singularities.

I found no sign or normalization error in this part of the argument.

## 6. Audit of measurable stable and unstable holonomy

The phase equation is

\[
 q\circ T_R=\exp\{i(u\cdot\kappa_R+s+t\tau_R)\}\,q,
 \qquad |q|=1,
\]

with `q` merely measurable.

The delicate point is that contraction of two endpoints does not imply pointwise convergence of their values under a merely measurable `q`. The manuscript handles this correctly. It disintegrates the normalized restriction of collision measure over one family of local curves and draws two conditionally independent points on the same curve. Both marginals are the restricted collision probability and are bounded by a fixed multiple of the ambient invariant measure.

A smooth approximation `q_\varepsilon` with supremum at most one then gives, uniformly in the iterate,

\[
 \int |q(T^ny)-q(T^nx)|
 \le C\|q-q_\varepsilon\|_{L^1(\nu)}
   +\int|q_\varepsilon(T^ny)-q_\varepsilon(T^nx)|.
\]

The second term tends to zero by contraction and bounded convergence; the first is then removed by `L^1` approximation. This proves endpoint agreement in the required averaged sense without assigning values to `q` on selected leaves or periodic points.

Iteration of the phase identity along a stable pair cancels the constant term and all lattice labels. Combining it with the forward action formula yields

\[
 \frac{q(y)}{q(x)}
 =\exp\!\left(it\int_{\gamma_s(x,y)}\vartheta_R\right)
\]

for almost every stable pair. The backward argument gives the same sign for almost every unstable pair.

The proof's use of Fatou's lemma is legitimate: the exact ratio has a pointwise limit determined by the shrinking action integral, while its distance from one tends to zero in `L^1`.

I found this measurable-phase step coherent. It is one of the strongest aspects of the revision.

## 7. Audit of the four-corner area obstruction

The stable-pair identity holds on a full-measure subset of the appropriate three-coordinate product space; the unstable identity has the analogous property. Product measure-class equivalence and Fubini allow all four edge identities to hold simultaneously for almost every quadruple of two stable and two unstable transversal coordinates.

Multiplication around the four corners telescopes the phase values and gives

\[
 \exp\!\left(it\oint_{\partial Q}\vartheta_R\right)=1.
\]

The product set can be restricted to arbitrarily small positive-measure transversal pieces. Nonatomicity excludes repeated coordinates almost everywhere, while transversality makes almost every four-corner quadrilateral a nondegenerate Jordan domain. Stokes' formula gives

\[
 \left|\oint_{\partial Q}\vartheta_R\right|
   =R\,\operatorname{area}_{\alpha,p}(Q)>0.
\]

For a fixed nonzero `t`, choose the product box so small that the absolute phase lies strictly between zero and `2\pi`. This contradicts the preceding circle identity. Hence `t=0`.

This is a qualitative exact-phase argument. It does not give a lower bound for the defect of an approximate phase, and the article correctly does not claim such a bound.

A future version would benefit from writing one explicit corner ordering and boundary orientation beside this multiplication. The current signs are recoverable from the text, but a diagram would reduce the burden on the reader.

## 8. Audit of constant-phase rigidity

After the roof coefficient is zero, the manuscript uses the actual sixty-degree physical rotation. In triangular lattice coordinates the rotation matrix satisfies

\[
 A^3=-I_2,
 \qquad
 I_2+A^2+A^4=0.
\]

For

\[
 Q_2=q(q\circ S_3),
 \qquad
 Q_3=q(q\circ S_2)(q\circ S_4),
\]

the spatial phases cancel exactly, while the constant phases become `2s` and `3s`. Since the collision map is mixing, it has no nontrivial unit-circle eigenvalue. Therefore

\[
 e^{2is}=e^{3is}=1,
\]

and hence `e^{is}=1`.

The use of both products is essential; a two-factor product alone would only determine the constant phase modulo `\pi`. The manuscript and its negative diagnostic correctly preserve this distinction.

The rotations are used only for the physical collision quantities. No rotational invariance of the enlarged return section is assumed.

## 9. Audit of the real spatial obstruction

Suppose a nonzero real vector `w` made `w\cdot\kappa_R` an `L^2` coboundary. Composing with the sixty-degree rotation gives a second coboundary in direction `wA`. The determinant of the two row directions is

\[
 -(w_1^2-w_1w_2+w_2^2),
\]

which is nonzero for `w\ne0`. Solving the two equations would therefore make both components of the lattice displacement a vector-valued real coboundary:

\[
 \kappa_R=H-H\circ T_R.
\]

The manuscript then passes to the actual billiard on the torus modulo `2\Lambda`. Its collision map is the finite skew product

\[
 \widetilde T_R(x,\ell)
  =(T_Rx,\ell+\kappa_R(x)\bmod2).
\]

This is a physical finite-horizon dispersing billiard with four scatterers. Young's billiard theorem applies to this finite cover; equivalently one may use the stated rectangular eight-scatterer Euclidean cover and then quotient by its deck group.

The function

\[
 F(x,\ell)=\exp\{i\pi(H_1(x)+\ell_1)\}
\]

is invariant under the skew product. It has modulus one and zero integral after averaging over `\ell_1`, so it cannot be almost everywhere constant. This contradicts ergodicity of the cover.

The cancellation in the exponent is exact, including reduction of the sheet coordinate modulo two. I found no algebraic defect here.

The specialist point is the applicability of the standard finite-horizon ergodicity theorem to the stated cover. The geometric hypotheses appear satisfied; the manuscript should retain the explicit cover description and not replace it by an abstract sheet-extension assertion.

## 10. Audit of the joint kernel argument

For a zero-variance direction, the collision coboundary is

\[
 w\cdot\kappa_R+a+b\tau_R-\zeta\eta_R
  =B-B\circ T_R,
 \qquad
 \zeta=\frac{a+b\bar\tau_R}{c_*}.
\]

If `\zeta\ne0`, exponentiation by `2\pi i/\zeta` removes the integer-valued section term exactly. Physical phase rigidity then gives `b=0` and requires `a/\zeta` to be an integer. But `\zeta=a/c_*`, so `a/\zeta=c_*`, which lies strictly between zero and one. This is impossible.

If `\zeta=0`, exponentiating the physical identity first gives `b=0`. The definition of `\zeta` then gives `a=0`, and the remaining spatial coboundary is excluded by the finite-cover lemma.

This exhausts every joint direction. The section discontinuity is never restricted to stable or unstable arcs; it disappears before the geometric phase argument. This is the correct way to avoid the regularity obstruction identified in earlier reports.

Since `D_R` is continuous and symmetric on the compact radius interval, pointwise positive definiteness gives a uniform positive lower eigenvalue. The established actual-covariance rate then gives eventual finite-`n` ellipticity. The physical-time projection has full rank, so its covariance is uniformly positive definite as well.

I found the algebra and the uniformity argument correct.

## 11. What the new theorem closes

Revision 14 closes the covariance blocker from the v13 report.

In particular:

- the four-dimensional Gaussian density is unconditionally defined for every radius;
- `\det D_R` stays uniformly away from zero;
- the Gaussian tail outside the rescaled central ball is exponentially small uniformly in the parameter;
- positive definiteness is no longer an assumption in the initial or marked raw-inversion interfaces;
- the physical-time fluctuation covariance is uniformly elliptic.

The theorem is stronger than the prior scalar count argument and avoids the unresolved periodic-representative issue rather than assuming it away.

## 12. Remaining mathematical blockers for the raw LLT

### 12.1 Complete complementary-frequency estimate

The proved central radius is

\[
 |\omega|\le 2n^{-1/2+1/200}
 =2n^{-99/200}.
\]

The remaining transform must be controlled from this boundary through:

- the intermediate annulus before any previously contemplated `n^{-2/5}` regime;
- compact nonzero lattice frequencies;
- growing roof frequencies;
- the far roof-frequency tail.

The exact-phase theorem in revision 14 is qualitative. It proves that an exact measurable phase with nonzero roof coefficient or nonintegral constant coefficient cannot exist. It does not prove a quantitative lower bound for approximate eigenvectors, a Fredholm estimate for the unbounded induced twist, or an integrated decay estimate on the complement.

A contradiction argument based only on absence of exact eigenfunctions is insufficient unless compactness and regularity of approximate phases are established with constants compatible with the growing frequency ranges. The manuscript explicitly recognizes this boundary.

Uniform ellipticity gives

\[
 \int_{|v|>n^{1/200}}e^{-v^{\mathsf T}D_Rv/2}\,dv
 \le Ce^{-cn^{1/100}},
\]

but this is a tail of the limiting Gaussian. It is not the Fourier tail of the physical record or of the residual transform.

### 12.2 Complete critical and singular branch extraction

The inherited single-word critical-edge calculations remain useful. They do not constitute a decomposition of the full actual measure.

The raw theorem still requires:

- every regular critical word;
- central critical branches;
- grazing and competing-root boundaries;
- dynamically generated image boundaries;
- extraction of every nonintegrable jump;
- summation of the remaining second distributional derivative norms with their actual return-count dependence;
- local control of the extracted density and its low-frequency convolution on central windows.

Collision moments, finite-return covariance, initial-coordinate BV, and phase rigidity do not provide these inverse-coarea density estimates.

### 12.3 Weighted tails and exact physical conditioning

The marked central and marked moment theorems treat one controlled function of one actual return state. They do not automatically cover multiple-time path insertions, exact terminal lattice/time indicators, or the relative comparison of two shrinking rare events.

The exact physical conditioning theorem still needs:

- weighted complementary-frequency estimates for the actual indicator class;
- weighted critical/singular edge bounds;
- lower bounds for the exact denominator on the correct local scale;
- a relative event-replacement estimate between the completed-return and physical observation events.

The same-event conditional results do not perform this replacement.

## 13. Top-four significance assessment

The sequence of revisions now contains a substantial unconditional package:

- actual Gaussian and functional laws;
- a growing integrated central band;
- initial and single-marked insertions;
- unsmoothed fourth moments;
- actual covariance convergence;
- same-event conditional moments;
- full joint covariance nondegeneracy.

The compensation-and-stopping architecture, especially the measurable phase argument of revision 14, is mathematically interesting. A paper centered on this completed package could be valuable in a strong specialist journal after independent expert review.

For a top-four journal, however, the present article continues to promise its raw mixed-density endpoint while retaining the full complementary transform and full raw branch sum as assumptions or criteria. Alternatively, the method could support a top-four claim if developed as a broad abstract theorem and demonstrated in several substantially different hyperbolic systems. The current manuscript remains tied to one carefully engineered Lorentz family.

I therefore do not regard revision 14 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 14. Required work before another top-four review

### A. Close the complete complementary-frequency region

Produce an integrated estimate beginning at the actual central cutoff and extending through all intermediate, compact nonzero, growing-roof, and far-tail regimes. If an induced anisotropic operator is used, construct it for the actual unbounded record and prove the phase-reconstruction and Fredholm estimates quantitatively. If a different method is used, it must still give explicit constants and a strictly feasible splice.

The new measurable exact-phase theorem should be used only as one qualitative obstruction unless it is strengthened to a quantitative approximate-phase theorem.

### B. Complete the raw branch decomposition

Construct the full extracted edge measure for the actual return record, including all regular, critical, singular, and image-boundary contributions. Prove residual `L^1` integrability and second-derivative summation with the true `n`-dependent constants, then verify the local edge conditions in the exact central windows.

### C. Complete the weighted exact-conditioning chain

For the actual physical indicators, prove weighted complementary tails and weighted edge bounds, and establish the relative comparison of the exact physical event with the completed-return event. State precisely which initial, terminal, and path insertion classes are stable under the required operations.

### D. Obtain independent specialist review

At minimum, independent experts should check:

- the Young product-set import and product measure class;
- the measurable conditional-pair and four-corner Fubini argument;
- the action-form signs and Stokes obstruction;
- the finite-cover ergodicity step;
- the inherited Demers--Zhang collision-space construction;
- the future complementary-frequency operator or alternative;
- the complete raw critical/singular decomposition.

### E. Consider a specialist-paper reorganization

If the full raw LLT is not completed, reorganize the article around the unconditional Gaussian, marked, moment, and nondegeneracy theorems. In that form the raw LLT should be presented as a future application or a sharply separated criterion, not as the apparent main theorem of the current article.

## 15. Presentation and technical comments

1. The introduction's Theorem A still calls `D_R` positive semidefinite before Theorem E later proves it uniformly positive definite. This is logically correct because Theorem A is inherited, but a sentence immediately after Theorem E should state that all later uses may take the stronger conclusion.
2. In the product-set lemma, identify explicitly which transversal coordinate is fixed on stable leaves and which on unstable leaves. This would make the four-coordinate Fubini step easier to verify.
3. State the exact conditional pair measures in product coordinates, including the measure-class densities used to pass from stable and unstable triple products to the four-corner product.
4. Add a diagram or an ordered list of the four corners and oriented edges in the Stokes argument.
5. Retain the explanation that stable and unstable holonomy have the same sign; this is easy to lose when rewriting the backward action identity.
6. In the finite-cover lemma, state in one place why the enlarged physical table remains finite horizon and why the free domain is in the class covered by the cited ergodicity theorem.
7. Keep the two- and three-rotation products separate. Their coprime multiplicities are what force the full constant phase.
8. Continue to distinguish qualitative exact-phase rigidity from quantitative approximate-spectrum control.
9. Beside every inversion statement, display both the rescaled cutoff `n^{1/200}` and the physical cutoff `n^{-99/200}`.
10. Do not refer to the Gaussian tail as a complementary transform estimate.
11. Continue to call the induced Green--Kubo conclusion Cesaro convergence rather than absolute convergence.
12. Keep the finite-cover obstruction as a real physical billiard argument; do not rephrase it as a formal independent-sheet model.
13. The exact inherited-edit ledger is useful and should remain part of future source qualification.
14. Supporting publication metadata should continue to distinguish author revision, successful build, external review, and formal proof certification.

## 16. Verification boundary

I reviewed the frozen source, the new phase-rigidity and joint-nondegeneracy modules, the inherited dependency updates, the source manifest and exact edit ledger, the branch and commit identities, and the actual GitHub Actions results at the reviewed SHA. I also checked the cited Young billiard source at the sections used for cones, homogeneous local manifolds, the positive-measure product construction, absolute continuity, and ergodicity.

I did not independently reconstruct every singularity estimate in the inherited paper, formally verify the continuum disintegration argument, or certify the complete manuscript proof-by-proof.

Finite algebra and high-precision collision diagnostics can test the rotation matrices, action derivatives, selected regular roots, source hashes, and exponent arithmetic. They cannot prove the continuum product structure, almost-everywhere four-corner argument, finite-cover ergodicity, complementary-frequency estimates, or global coarea branch sum.

The recommendation is therefore a mathematical and editorial referee assessment at the requested standard, not a formal proof certificate.

## 17. Final conclusion

Revision 14 closes the full covariance-nondegeneracy blocker by a credible and conceptually interesting argument. It removes the discontinuous section term before applying physical phase rigidity, avoids evaluating an `L^2` transfer function on periodic orbits, and obtains uniform ellipticity through covariance continuity. I found no decisive counterexample in the new proof.

The exact source is properly qualified, and the new theorem materially strengthens the unconditional probabilistic package.

Nevertheless, the parameter-uniform raw mixed-density LLT remains conditional on the complete complementary-frequency estimate and the full critical/singular residual decomposition; the exact physical conditioning application additionally requires weighted tails and relative event replacement. These are central mechanisms, not peripheral clean-up.

For those reasons I recommend rejection at the requested top-four benchmark in the present form, while recognizing revision 14 as a substantial mathematical advance and a potentially strong specialist contribution.