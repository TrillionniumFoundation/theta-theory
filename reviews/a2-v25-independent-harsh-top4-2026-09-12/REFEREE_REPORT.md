# Independent external referee-style report on A2 v25

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Version examined:** `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`  
**Immutable reviewed commit:** `3143762fc98373f93dbb8884c5ece005229ca50b`  
**Active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Entry-point blob:** `43f0acac5e8858df81e6c5c389f0c5adde05ac96`  
**Review branch:** `review/a2-v25-independent-harsh-top4-2026-09-12`  
**Date:** September 12, 2026  
**Requested standard:** Annals of Mathematics, Inventiones Mathematicae, Journal of the American Mathematical Society, or Acta Mathematica.

This is an author-requested, AI-assisted independent referee-style assessment. It is neither a commissioned journal report nor an editorial decision. Author responses, previous referee opinions, diagnostic counts, and branch names are evidence to inspect, not certificates of mathematical correctness.

## Recommendation

**Reject in the present form at the requested top-four level. A materially reworked submission could warrant a fresh assessment.**

The reason is **not** that the three principal v24 proof objections have survived unchanged. The author has now supplied a meaningful common-observation model, included gaps in the statistical separating coordinates, and replaced the invalid finite-signature matching argument by a substantially better one. In the newly inspected proofs, I found no counterexample to the stated global consistency theorem under its explicit full-position acquisition assumptions. It would be misleading to call those repairs cosmetic or to repeat the old objections as if the new sections did not exist.

The central remaining scientific issue is different. The global experiment now records exact two-dimensional collision positions. Those are samples of the unknown boundary itself. This permits a direct local graph-interpolation route to contact jets, using the same long even bridges and the same charged calibration mechanism. The restriction that the minimum flight number diverges does not prevent this route. Consequently, the global consistency theorem does not yet demonstrate why the difficult inverse of the two half-line actions is essential to the newly advertised physical reconstruction problem. This is a serious significance and theorem-selection objection, not a counterexample to consistency.

There is also a definite mathematical classification error in the statistical exposition: failure of absolute continuity with respect to the reference distribution is repeatedly called non-domination of the family. Both the displayed scalar-density family and the finite-strip Poisson family have explicit common dominating measures. The correction does not destroy the collar or reverse-kernel arguments, but it must be made throughout the active statements.

Finally, an exact-head complete native build remains unverified. This is a submission gate, not evidence of a false theorem or even of a LaTeX error. The recommendation above does not rest on an unexecuted workflow alone.

## 1. Scope and provenance of this review

The v25 branch is twenty commits ahead of the v24 review tip `8129defd970bbc1e011bb480b70603d39a31324d`, with no divergence in the comparison returned by GitHub. The earlier reviewed manuscript was `c35b31b1924a1621374eab72ee60e4cb5ab37df5`. The v25 delta contains eighteen changed files. Its eight new mathematical TeX modules were inspected, including the complete observable-calibration, augmented-estimator, finite-signature, analytic-variation, and two-sided-deficiency arguments. The entry point, preservation manifest, author response, verification record, and substantive preceding objections were also inspected. Selected inherited inverse, gluing, finite-threshold, and local-information dependencies were checked separately.

This is a revision-focused source audit. It is **not** a claim to have independently recertified every theorem in the complete historical auxiliary compendium. No complete native checkout, recursive whole-tree reference audit, compiled-page inspection, or full-paper LaTeX build was executed in this review. Source paths and stable theorem labels, rather than invented PDF page numbers, identify the assertions below. Precise coverage is recorded in `SOURCE_AUDIT.md`.

The report includes a separately written, executed diagnostic program. Its 126 finite cases support the specific algebra and examples described below; they are not a formal proof certificate.

## 2. Disposition of the previous objections

| Previous issue | Assessment of v25 | Reason and qualification |
|---|---|---|
| Common observable coordinates and within-channel calibration | Substantially closed in the new, explicitly richer model | [S1] defines actual position records and a charged pilot for points, tangent, and gap. This is not a proof of an unregistered scalar-only experiment. |
| Gap missing from the finite-separator criterion | Closed | [S2] includes estimated gaps in the moment vector and in the finite-template rule. |
| Outside-arc signature separation mistaken for local uniqueness | Closed under the printed hypotheses | [S3] proves a finite immersion, local chord bound, global separation, and strict convexity of a noisy matching criterion. |
| Unspecified finite-dimensional tangent bundle over an analytic class | Substantially closed | [S4] constructs compatible ambient analytic variations on a separately specified contact stratum; the global theorem does not depend on that bundle. |
| Final flight number chosen after pilot precision | Closed | [S2] chooses the final even number before the pilot and uses that same number in both stages. |
| Wrong conditioning on successful completion of a cap | Closed in the inspected argument | Concentration is applied to the uncapped success sequence; the cap-exhaustion event is added separately. |
| Continuity insufficient for selected measurable tests | Closed | [S1–S2] supply centered-law total-variation continuity and select bounded Lipschitz tests. |
| Bulk relative-density hypothesis and Poisson corner conventions | Closed in the inspected local model | [S5] states the needed relative bound and defines the reverse kernel on exceptional configurations. |
| Short-flight benchmark and navigation | Addressed, but a new same-experiment benchmark is needed | [S8] includes the one-flight inverse; root navigation now identifies v25. Exact position samples create the stronger issue in Section 4 below. |
| Exact-head native build | Still unverified | The inspected exact-head workflow is queued with null conclusion. |

These dispositions are not unconditional endorsements of every inherited dependency. They identify which concrete v24 criticisms the new proofs actually answer.

## 3. Mathematical material that deserves positive credit

### 3.1 The signed contact inverse remains the strongest identifiable mechanism

The proof in [S9] does more than formally invert Taylor coefficients. The weighted half-line inverse controls the stationary sequence. Finite-truncation differentiation cancels the internal orbit variations by stationarity, and the remaining boundary term tends to zero with the required fixed-order derivatives. Homogeneous isolation then distinguishes the order of a graph jet in the action from the higher derivative order that may occur in the stationarity equations.

Writing \(x=e^{-\gamma}\), the own-contact and opposite-contact multiplicities give

\[
1+2\sum_{k\geq1}x^{2nk}=\coth(n\gamma),\qquad
2\mathfrak r_b^n\sum_{k\geq0}x^{n(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

Since \(\mathfrak r_0\mathfrak r_1=1\), the last-jet block has determinant one. The independent diagnostic verifies forty-five exact rational instances of the block and its inverse. I found no specific contradiction in the envelope and degree-isolation mechanism inspected here. This credit is limited to the inspected argument, not a new blanket certification of the entire relative-law construction.

The manuscript correctly distinguishes fixed-order conditioning from a uniform condition number for the infinite jet map. Determinant one alone would not establish the latter, and that stronger claim should not be attributed to v25.

### 3.2 The finite-signature repair is real

In [S3], the designated signature-rigid transition obstacles have no nonidentity orientation-preserving symmetry. Analytic nonconstancy ensures that some positive derivative of curvature is nonzero at each point. Compactness selects finitely many derivative coordinates with a uniform immersion bound. A separate compactness argument on pairs outside a short arc selects enough coordinates for global separation.

The noisy matching proof then uses the actual Hessian

\[
f''(x)=|\widetilde J'(x)|^2+
 (\widetilde J(x)-y)\cdot\widetilde J''(x).
\]

On a sufficiently short arc, under the stated \(C^2\) perturbation bound, it is uniformly positive. The global separation first places every minimizer in that arc. This is precisely the missing combination of local uniqueness and outside-arc exclusion. The proof does not claim uniqueness under arbitrary \(C^0\) perturbations.

The compact inverse modulus is also proved independently by exact injectivity and compactness. The tail \(C2^{-M}\) is expressly a weighted-product-metric tail, not an analytic-continuation rate. Repeating the earlier criticism on that point would be unjustified.

### 3.3 The observable pilot and estimator are coherent in their declared model

The grid scan in [S1] has a point with true excess in \([h,2h]\). A success earlier in the scan is still after onset and no later than that point. The probability of missing the useful grid point is controlled by a positive success lower bound and a finite repetition cap. This does not infer zero probability from a finite run of failures.

The displayed estimators give

\[
j|\widehat g-g|\leq h,\qquad
|\widehat p-p|+|\widehat t-t|\leq C\sqrt h
\]

on the simultaneous good event. The estimated coordinates are measurable. The unknown exact chart appears only in the proof of the test-bias bound. The finite-template rule in [S2] uses both gap estimates and successful-law moments; its \(3c<8c\) separation argument and its ordering of design choices are sound in the inspected proof.

### 3.4 The other new repairs should be retained

The trigonometric Hermite construction in [S4] imposes all contact incidences simultaneously, and the triangular support-jet to graph-jet differential supplies actual compatible analytic perturbations. An ambient finite-rank bundle through a compact base is not falsely identified with the tangent bundle of an arbitrary closed analytic class. The independent diagnostic checks twelve exact finite jet-evaluation rank examples; the general proof is the interpolation argument, not those examples.

The layer/bulk estimates in [S5] now explicitly use the relative density bound needed for the \(O(k^{-2})\) one-record bulk Hellinger estimate. The reconstructed bulk, random permutation, invalid residual-coordinate convention, and excessive Poisson-count convention are specified. Under the displayed hypotheses, the \(O(\varepsilon_{n,K}+k^{-1/2})\) deficiency proof has the appropriate structure.

The rank-two formula in [S10], \(L=VM^{-1}\), legitimately recovers the lattice metric from independent marked deck displacements and recovered translation holonomies. It does not require the marked pair to be unimodular. The substantive geometric input remains the preceding recovery and unique matching of curve copies; the last matrix multiplication should not be advertised as the difficult inverse by itself.

## 4. Major scientific objection M1: the exact-position experiment admits a direct geometric route within the same long-even restriction

**Locations:** [S1], `eq:v25-design-record-spaces`; [S2], `thm:v25-global-physical-reconstruction`; [S6], `thm:v25-intro-physical`; [S8], the final comparison paragraphs.

**Classification:** significance and necessity-of-machinery objection, supported by a same-observation benchmark. It is not a counterexample to the stated consistency theorem.

### 4.1 The newly supplied information is more than a coordinate convention

The full physical record includes \(X\in\mathbb R^2\), not just the transverse coordinate of \(X\). After the contact frame has been estimated, its two components provide a point on the graph of the unknown obstacle. In the exact contact chart one has, with the known facing-side sign convention,

\[
y=t\cdot(X-p),\qquad \psi_b(y)=\pm n\cdot(X-p).
\]

The longitudinal coordinate is therefore a noiseless graph-value observation. It is not merely a device for assigning an origin to a scalar statistic. The author explicitly distinguishes the richer position model from the anchored scalar information model in [S6–S7]; that honesty is important. But the implications for the scientific role of the global theorem have not been worked out.

The old one-flight objection is not being repeated. The benchmark below uses **only the long, even, same-type designs allowed in v25**. Nor does it presume a known contact center, tangent, gap, or inter-channel registration: it can use the newly proved pilot.

### 4.2 Direct finite-jet acquisition from the permitted records

Here is the comparison argument at the fixed-order level. Fix an order \(M\), a target error probability, and any prescribed lower bound on the flight number. Choose an even \(J\) above that bound. On the compact class, the boundary graphs have uniform fixed-order derivative bounds in a common contact patch.

Choose a small geometric scale \(a>0\), and \(M+1\) disjoint transverse bins centered at \(a\xi_i\), where the fixed \(\xi_i\) are distinct and lie in a sufficiently small interval. Their widths can be a fixed small multiple of \(a\), so all selected nodes remain separated by \(c_Ma\). Run the observable pilot at this same \(J\), with contact-frame error at most \(\varepsilon\) and with \(J|\widehat g-g|\) much smaller than \(a^2\). The pilot resolution can be made arbitrarily small at finite charged cost, exactly as in [S1].

Program a post-pilot excess proportional to \(a^2\), with a sufficiently large fixed proportionality constant. The finite bridge action has a quadratic upper bound on a sufficiently small endpoint box. The finite physical flux is positive on its interior. Restrict the other endpoint to a small interval of length proportional to \(a\), and the residual time to an interior interval of length proportional to \(a^2\). Then every chosen first-endpoint bin has positive one-preparation probability.

For the benchmark it is enough to fix \(J\) first: compactness and strict positivity give a lower bound for these finitely many bin events, allowed to depend on \(J,M,a\). No asymptotic factorization of the relative density is required for that existential bound. With the manuscript's stronger uniform flux bounds one can also obtain bounds of the schematic form \(c_Ma^4e^{-J\gamma_+}\). Either route is compatible with the absence of any effective-budget requirement in the global theorem.

Take capped independent preparations until each bin has supplied a point. If the uniform lower probability is \(p_{\min}>0\), a cap of order

\[
p_{\min}^{-1}\log\!\frac{(M+1)2|E|}{\beta}
\]

per bin suffices by a union bound. Every failure is charged. The bins are selected using the estimated frame, so the rule is measurable in the same physical transcript. On a sufficiently accurate pilot event, smaller true-coordinate sub-bins lie inside the selected bins, which gives the required uniform positive lower bounds.

Let \(\widehat y_i,\widehat z_i\) be the measured transverse and signed longitudinal coordinates in the estimated frame. On that event,

\[
|\widehat z_i-\psi_b(\widehat y_i)|\leq C\varepsilon.
\]

Interpolate a degree-\(M\) polynomial through these \(M+1\) points. A scaled Vandermonde matrix with separated normalized nodes has a bounded inverse, with a constant depending on \(M\) and the bin configuration. Taylor's formula therefore gives, for \(0\leq m\leq M\),

\[
|\widehat\psi_b^{(m)}(0)-\psi_b^{(m)}(0)|
\leq C_M\bigl(a^{M+1-m}+\varepsilon a^{-m}\bigr).
\tag{4.1}
\]

For \(a\leq1\), the maximum error through order \(M\) is bounded by \(C_M(a+\varepsilon a^{-M})\). Taking the pilot sufficiently fine that \(\varepsilon\leq a^{M+1}\) gives an \(O_M(a)\) error. The pilot's gap accuracy can simultaneously ensure a valid \(a^2\)-offset window. The constants and caps may be extremely unfavorable; v25's consistency statement expressly permits that.

This acquires the labelled graph jets **without recovering or inverting the half-line actions**. The diagnostic program verifies twenty-one exact interpolation examples and the predicted scaling of each derivative error. The argument (4.1), not the number of examples, establishes the comparison mechanism.

### 4.3 Why the restriction to diverging even flight numbers does not remove this comparison

At stage \(s\), choose the already prescribed even \(J_s\geq s\), then perform the pilot and graph sampling just described with that same number. Both endpoint types are available through separate same-type batches. There is no hidden odd flight or short-flight scan.

Complete contact graph jets, gaps, analytic continuation, and the same signature-rigid gluing recover the marked table. On the assumed compact class, exact injectivity of these direct geometric data yields a compact inverse modulus, just as in [S3]. Finite-template selection and a diagonal choice of \(M,a,\varepsilon\), and error probabilities then give a consistency route of the same existential kind as [S2]. This route still uses the geometric gluing and an acquisition argument. It bypasses the new action inverse as the means of obtaining the contact germs, and it does not need a relative long-bridge limit merely to establish finite bin positivity for each selected \(J_s\).

This is a referee-derived reduction using the printed observation model and elementary interpolation, not a claim that the entire paper is already a theorem in the literature. It explains why “every flight number is even and tends to infinity” is not, by itself, a satisfactory answer to the significance question once exact ambient positions are admitted.

### 4.4 A sharp local illustration of the information supplied by positions

In a registered contact chart, consider circles tangent at the origin with centers \((-R,0)\). Their equations are

\[
x^2+y^2+2Rx=0.
\]

One exact non-contact point on the circle determines

\[
R=-\frac{x^2+y^2}{2x}.
\tag{4.2}
\]

Distinct such circles meet only at the origin. A successful endpoint with a continuous arclength density hits that point with probability zero. Thus the conditional raw-position laws for distinct radii are mutually singular, even for arbitrarily small differences of radius.

This is a **local registered observation example**, not a counterexample satisfying the global signature-rigid hypotheses: circles are excluded as transition obstacles there. The phenomenon is not caused by circular symmetry. Distinct compact analytic curve images have isolated, hence finitely many, intersections unless they share an analytic arc and therefore the same connected image. Positive arclength-density observations on distinct images are consequently mutually singular. One can also start from a nonsymmetric strictly convex analytic oval, for example the support function

\[
h(\theta)=1+\frac1{50}\cos(2\theta)+\frac1{100}\sin(3\theta),
\qquad h+h''\geq\frac{43}{50}>0,
\]

anchor a boundary point, and consider small distinct homothetic copies about it. Strict convexity makes these nested copies touch only at the anchor. The harmonic orders two and three exclude a nontrivial rotational symmetry. This supplies the same local support-separation phenomenon without a circular transition.

The point is not that a single point determines an arbitrary analytic obstacle. It does not. It is that exact ambient observations have support information radically different from the scalar-density model. For any two-parameter comparison and any proposed kernel from the coarser to the raw experiment, contraction of total variation gives the lower bound

\[
\delta(\mathsf E_{\rm coarse},\mathsf E_{\rm raw})
\geq\tfrac12\left[
\|P^{\rm raw}_0-P^{\rm raw}_1\|_{\rm TV}
-\|P^{\rm coarse}_0-P^{\rm coarse}_1\|_{\rm TV}
\right]_+.
\]

For the conditional raw laws just discussed, the first distance is one. This is a useful benchmark for any assertion of equivalence or information exhaustion. V25 does **not** assert such an equivalence; [S7] explicitly warns against it. I am therefore not identifying a false theorem at that location. I am requiring the introduction to take the consequences of its correctly stated distinction seriously.

### Required response to M1

Add a same-experiment direct-position benchmark and identify precisely what mathematical result goes beyond it. The important result may be the inverse from genuinely coarsened signed law data, a sharp quantitative physical-information comparison, or another substantive theorem. The choice must be justified by an actual statement and proof, not by the length of the proof architecture or the existence of a long-flight restriction.

This does not request deletion of the all-order inverse, abandonment of global reconstruction, or an arbitrary narrowing of the research program. It requests a defensible account of the central theorem's mathematical difficulty and significance under the observations actually supplied.

## 5. Mathematical correction M2: common domination is confused with domination by the reference model

**Locations:** [S11], opening paragraphs and `eq:v22-vector-density`, `eq:v22-thinned-family`; [S5], the finite-strip Poisson experiment; [S6] and the main abstract's “generally non-dominated” descriptions.

**Classification:** a definite error in the stated classification of the statistical families. The main collar and deficiency calculations can survive the correction.

### 5.1 The scalar family is dominated as a statistical family

The manuscript writes

\[
f_\theta(x)=a_\theta(x)(w_\theta(x))_+,\qquad
P_{n,h}=(1-p_n)\delta_\dagger+p_nf_{\delta_nh}(x)\,dx
\]

on one fixed bounded set \(U\) with a cemetery atom. Consequently

\[
\mu=\operatorname{Leb}|_U+\delta_\dagger
\]

is a common finite dominating measure for **every** displayed \(P_{n,h}\). Its product dominates the corresponding finite product experiment. Adding a second cemetery atom gives a common dominating measure for the censored family as well.

What may fail is \(P_{n,h}\ll P_{n,0}\). That is exactly why a likelihood ratio relative to the reference law is not globally available without treatment of the support-exclusive part. It is not the definition of a non-dominated statistical family.

For a concrete example, on the fixed box \([0,2]\), let

\[
f_\theta(x)=\frac{2(1+\theta-x)_+}{(1+\theta)^2},
\qquad 0\leq\theta<1.
\]

All these laws have Lebesgue densities, yet for \(\theta>0\)

\[
P_\theta((1,1+\theta))=\frac{\theta^2}{(1+\theta)^2}>0,
\qquad P_0((1,1+\theta))=0.
\]

The distinction is exact, not terminological preference. The manuscript should say “not necessarily absolutely continuous with respect to the reference law” or “not necessarily mutually absolutely continuous.” The common-collar construction then produces a representative dominated by its reference member, which is the stronger property its likelihood calculation actually needs.

### 5.2 The finite-strip Poisson family also has a common dominating law

Fix the compact parameter set and the finite strip used in [S5]. On \(B=D\times[-R,R]\), write

\[
d\Lambda_z=\rho(u,v)\mathbf1_{\{y>U(u,v)z\}}\,du\,dv\,dy,
\qquad
d\Lambda_*=\rho(u,v)\,du\,dv\,dy.
\]

Both measures are finite, and \(\Lambda_z\leq\Lambda_*\). If \(\mathsf P_*\) is the Poisson law with intensity \(\Lambda_*\), then

\[
\frac{d\mathsf P_z}{d\mathsf P_*}(N)
=\exp\bigl(\Lambda_*(B)-\Lambda_z(B)\bigr)
 \prod_{q\in N}\mathbf1_{\{y(q)>U(q)z\}}.
\tag{5.1}
\]

The empty product is one. Its expectation is one because the probability of no points in the forbidden part is the exponential of minus that part's intensity. Thus \(\mathsf P_*\) dominates every member of the finite-strip experiment. A reference zero-shift member need not do so. Adjoining the parameter-independent tail described in [S5] does not alter this conclusion on the compact local parameter set.

There is no reason to withdraw the explicit kernels because of this correction. The layer comparison, reference-bulk reconstruction, and Hellinger estimates concern valid probability laws. But repeated use of “non-dominated” in the title of a section, theorem narrative, introduction, and abstract materially obscures what has actually been proved. Repair the classification consistently rather than adding one footnote while leaving the main assertions unchanged.

## 6. What this review does not reject, and what remains necessary for the requested tier

Non-effective constants are not a logical flaw in an explicitly existential consistency theorem. The manuscript openly allows the finite library, separation constants, and compact inverse moduli to depend non-effectively on the compact analytic class. I do not demand a minimax rate as a condition for the truth of that theorem. Nor does the direct-position benchmark show that the relative law or the all-order signed inverse is elementary.

Nevertheless, at the requested publication level, the article must establish why its principal conclusion and its hardest mechanism belong together. A correct implementation of a very informative, noiseless experiment is not automatically a breakthrough inverse theorem. Appending another existential compactness layer does not resolve this issue. In my assessment, the current combination of the two flagships and the separately scoped information hierarchy does not yet make that case convincingly enough.

The related-work comparison in [S6] is improved and should not be falsely reported as absent. De Simoi, Kaloshin, and Leguil [L1] study marked-length determination for analytic open billiards under stated symmetry and genericity assumptions. Finamore and Leguil [L2] use an enriched marked length spectrum for finite-horizon Sinai billiards. These are different data maps from signed channel laws or ambient collision positions. Neither subsumption of A2 nor a direct generalization of those results follows without a proved relation between observations.

Meister and Reiss [L3] establish Poisson-experiment equivalence for nonregular regression with endpoint discontinuities. That comparison does not settle the billiard geometry or the exact local kernels here. It does show why a generic Gaussian/Poisson contrast is not itself a new organizing statistical principle. V25 now acknowledges this; the remaining task is to demonstrate the specific geometric and observational advance, rather than to add more general citations.

A minor implementation clarification is also warranted. The stagewise policies in [S2] satisfy the requirement that all flight numbers used by stage \(s\) are at least \(s\). The final budget-indexing paragraph should specify whether a prescribed-budget procedure restarts the selected stage or accumulates earlier stages. A cumulative full transcript contains earlier, smaller flight numbers, even when the estimator ignores them. This does not refute the printed stagewise theorem; it is a clarification needed if the same restriction is claimed for a cumulative-budget implementation.

## 7. Native verification and independent diagnostics

At inspection, GitHub Actions run `34662232834`, named `A2 v25 complete native build`, had head `3143762fc98373f93dbb8884c5ece005229ca50b`, status `queued`, and null conclusion. The author verification record [S13] also carefully distinguishes finite `--math-only` checks from full source-graph and native-build execution. This disclosure is appropriate. A queued run proves neither a successful build nor a typesetting failure.

Before a submission-ready status is asserted, obtain an executed complete build of both declared native entry points at a frozen source commit, retain the logs and source/PDF hashes, and report unresolved references, duplicate labels, and missing glyphs. The full auxiliary compendium should remain auditable; it need not be deleted to make the build easier. This review did not execute the author's 337-case suite or certify its full-tree modes.

The accompanying independent standard-library program was executed under Python 3.13.5 in ordinary and optimized mode. The outputs agree byte for byte. It counts 126 finite cases: 45 last-jet blocks, 24 pilot brackets, 12 Hermite ranks, 21 graph-interpolation scalings, 3 common-density/reference-non-absolute-continuity examples, 5 Poisson-envelope normalizations, 9 exact raw-position circle inversions, 3 lattice examples, 3 enriched-signature convexity examples, and 1 analytic-oval positivity bound. Multiple assertions inside a case are not separately counted.

Its SHA-256 is `a9ae0911fa17c7547c6ffd656eb755f8cc2953232d158fb27cecdce3a9e8cdd9`. The program uses explicit exceptions rather than Python `assert`; optimization does not disable its checks. These finite algebraic checks and local witnesses do not certify infinite-dimensional estimates, a global billiard counterexample, or a native manuscript build.

## 8. Conditions for a meaningful next revision

The next response should not simply label all previous issues closed and add another claimed flagship. It should address the actual remaining questions.

1. **Compare within the same observation model.** Include or refute, by a specific failed hypothesis, the direct graph-acquisition route in Section 4. Account for exact longitudinal positions, both even endpoint types, the charged pilot, and arbitrary finite preparation caps. Merely forbidding one-flight observations is not an answer.
2. **State the genuinely stronger contribution precisely.** Explain which principal result goes beyond direct geometric sampling and compact analytic continuation, with an actual theorem-level comparison. Retain the signed-action inverse and the substantive relative-law analysis; do not hide them behind a global consistency statement whose acquisition is much richer.
3. **Correct the domination claims globally.** Separate common domination, absolute continuity relative to the reference member, and the support-singular ambient position experiment. Preserve the valid collar and Poisson-kernel estimates while stating their role accurately.
4. **Deliver a source-pinned complete submission artifact.** Supply an executed native build and a coherent dependency map covering the actual retained source graph. Clarify the minor stagewise-versus-cumulative budget statement.

These are not demands to abandon the program or arbitrarily reduce its mathematical scope. They are demands for correct experiment classification, credible significance under the stated data, and a verifiable submission. My recommendation remains negative for the current requested tier, while recognizing that v25 is a substantive mathematical repair of v24 rather than a failed repetition of it.

## Source index

All manuscript references below are to commit `3143762fc98373f93dbb8884c5ece005229ca50b`. Let `P` denote `papers/A2-v17-boundary-information-coarsening`. A reproducible immutable source URL has the form `https://github.com/TrillionniumFoundation/theta-theory/blob/3143762fc98373f93dbb8884c5ece005229ca50b/PATH`.

- **[S1]** `P/article/25a_common_observables_v25.tex`: `eq:v25-design-record-spaces`, `lem:v25-physical-localization`, `thm:v25-observable-calibration`, `prop:v25-test-implementation`.
- **[S2]** `P/article/25b_augmented_global_reconstruction_v25.tex`: `lem:v25-augmented-separators`, `thm:v25-fixed-order-physical`, `thm:v25-global-physical-reconstruction`.
- **[S3]** `P/article/23e_signature_stability_v25.tex`: `thm:v25-finite-signature-embedding`, `lem:v25-noisy-signature-match`, `lem:v24-gluing-persistence`, `thm:v24-global-modulus`.
- **[S4]** `P/article/25c_analytic_variation_bundles_v25.tex`: `lem:v25-hermite-right-inverse`, `prop:v25-analytic-jet-bundle`, `lem:v24-uniform-positive-design`.
- **[S5]** `P/article/18c1_endpoint_time_deficiency_v25.tex`: `eq:v25-bulk-relative-hypothesis`, `lem:v24-layer-bulk-bounds`, `thm:v24-two-sided-deficiency`, `rem:v24-projective-poisson`.
- **[S6]** `P/article/01_introduction_v25.tex`: the two introductory theorems, information hierarchy, and literature comparison; also `P/main.tex`, abstract.
- **[S7]** `P/article/01a_protocol_scope_v25.tex`: explicit separation of scalar local and full-position global experiments.
- **[S8]** `P/article/29a_signed_one_flight_benchmark_v25.tex`: `prop:v25-one-flight-inverse` and the long-even observation comparison.
- **[S9]** `P/article/23a_signed_endpoint_rigidity_v22.tex`: `thm:v22-signed-rigidity`, weighted inverse, envelope, homogeneous isolation, determinant-one blocks, and finite-jet tangent inverse. Source lines 1–450 were inspected; no claim of a complete audit of every inherited continuation dependency is made.
- **[S10]** `P/article/23d_rank_two_lattice_recovery_v24.tex`: metric-free holonomy and lattice reconstruction. Also `P/article/23b_intrinsic_multichannel_rigidity_v23.tex`, lines 1–190, for analytic signatures and gluing definitions.
- **[S11]** `P/article/18a_vector_boundary_information_v22.tex`, lines 1–220: common density, support-exclusive mass, common-collar representative, and the stated LAN setup. The remainder of that inherited section was not independently recertified here.
- **[S12]** `P/article/02_finite_results.tex`: inherited finite threshold and conditional metric statements; the complete historical proofs behind those statements were not all reread.
- **[S13]** `P/RESPONSE_TO_REFEREE_V25.md`, `P/ACTIVE_SOURCE_MANIFEST_V25.md`, `P/VERIFICATION_V25.md`, root `README.md`; preceding report at `reviews/a2-v24-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`.

### Primary literature checked for the comparisons

The following primary-source records were checked online on September 12, 2026. These checks verify the limited observation/hypothesis comparisons made above; they are not claimed to be exhaustive novelty searches or complete rereadings of all cited proofs.

**[L1]** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890, version 4; related publication DOI `10.1007/s00222-023-01191-8`. Primary record: `https://arxiv.org/abs/1905.00890`.

**[L2]** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983, submitted October 21, 2025; the accessed record displays version 1. Primary record: `https://arxiv.org/abs/2510.18983`.

**[L3]** A. Meister, M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248. Primary record: `https://arxiv.org/abs/1101.5248`.
