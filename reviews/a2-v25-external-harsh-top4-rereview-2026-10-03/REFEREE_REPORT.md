# External top-four referee report on A2 v25

**Manuscript:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Reviewed revision:** `revision/a2-v25-effective-local-recognition-2026-10-03`  
**Equivalent referee-copy alias:** `revision/a2-v25-referee-copy-2026-10-03`  
**Reviewed commit:** `7151ddcd8b29516a8a6f8fa5043b97c49206b3ae`  
**Reviewed tree:** `175e6b77020f87ffb5f7d7ceff19e8786b401eb7`  
**Mathematical checkpoint:** `a5293ca684337b184ba4637cba2c223c684a61ea`  
**Controlling preceding report:** `3aeea88879dbba28a7564e3c5787ce293e3a45c8`  
**Manuscript directory:** `papers/A2-v25-effective-local-recognition`  
**Date:** 3 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 25 is another genuine mathematical revision. It answers the two most concrete technical criticisms in the v24 report.

First, it replaces the previously non-effective compactness constant by an explicit, if extremely conservative, calibration. The new argument gives a numerical interval-to-strip continuation modulus, converts local graph closeness into complete-pair Hausdorff closeness, locks the physical copies by the supplied shape, symmetry and separation margins, and then chooses a finite jet order, value-grid size and registry threshold from the numerical priors. The accompanying fixed-presentation compactness lemma also supplies the missing topology across lattice-basis walls and representative changes.

Second, the revision weakens the acquisition primitive. The effective alternative fingerprint uses finitely many boundary values rather than high derivatives. Certified finite differences, interval root certification and quadrature then reconstruct the normal contact and intrinsic endpoint coordinates from local chart heights. The sensor no longer returns derivatives or arclength values directly. The stopping exponent is also stated consistently: the theorem now quantifies over a chosen `a >= 6`, with expected generic probe work requiring `a > 4+s` and value-query work requiring `a > 5+3s_v`.

On the new v25 core audited in detail, I found no fatal counterexample to the fixed-presentation compactness statement, the explicit continuation estimate, the quantitative physical-copy locking argument, the jet or value fingerprint separation, the finite-difference bounds, the local normal/clearance construction, the arclength quadrature, or the corrected cost summability. The retained local inverse, completion defect, rational period recovery and anytime certificate continue to be coherent in their stated scope. Independent diagnostics accompanying this report support the finite algebra and inequalities. I therefore do **not** base the negative recommendation on a known false central theorem.

The remaining objection is editorial and conceptual. The new “effective” result is effectivity only relative to an exceptionally strong numerical prior package and an active local geometric sensor. It assumes certified complex-strip and graph-disk bounds, quantitative global shape separation and asymmetry, physical-copy separation, curvature and chart margins, local boundary-height access to arbitrarily prescribed accuracy, and distance-to-the-entire-solid enclosures near candidate flights. It then combines those inputs with two complete two-dimensional endpoint-density functions per record, absolute whole-cell Liouville normalization, analytic continuation and a compact physical class.

Moreover, the explicit calibration is not remotely an effective acquisition theorem in the practical or complexity-theoretic sense. For the supplied arithmetic example the paper obtains

`P = 27 * 2^519`, `E_* = 76 * 2^(-P)`, and `N = 2^P`.

The value fingerprint therefore has more than `2^P` coordinates. This is a legitimate finite symbolic recipe, and the manuscript is honest about its size, but it demonstrates that the remaining theorem is a quantitative compactness existence result rather than a usable finite sensor design. The hidden constant in the displayed epoch-cost power contains this enormous class-dependent `N`.

The local-value reduction is mathematically careful but does not change the information category enough to reach the requested benchmark. The apparatus still receives local boundary geometry in laboratory coordinates and a distance oracle for all solid near the flight. The probability and stopping layer is standard once genuine records with a uniform hazard have been constructed. Global uniqueness still rests on strong analyticity and genericity assumptions, and the count-only and passive unmarked-trajectory problems remain outside the theorem.

In my judgment this is serious specialist-journal mathematics. A focused submission centered on the effective within-table recognition theorem and the completion defect could be strong after a fresh human proof review and the clarifications below. It does not have the exceptional naturality, breadth or conceptual transformation required by the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

Both v25 branch names listed above resolve to the author head

`7151ddcd8b29516a8a6f8fa5043b97c49206b3ae`

with repository tree

`175e6b77020f87ffb5f7d7ceff19e8786b401eb7`.

Its parent is the mathematical checkpoint

`a5293ca684337b184ba4637cba2c223c684a61ea`,

which is based directly on the v24 external-review head

`3aeea88879dbba28a7564e3c5787ce293e3a45c8`.

That report reviewed v24 author commit

`f5754f7eacc5b2bde9450de154a4e4c0093b3e23`.

The complete reviewed v24 paper is preserved at

`papers/A2-v25-effective-local-recognition/retained/v24`

with tree

`3d729a1fe93e2250cd68494d149fbb6e90b4096e`.

The original complete supplement remains at tree

`14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

No `revision/a2-v26...` branch existed when this review branch was created. The review branch starts directly from the v25 author head and adds files only below

`reviews/a2-v25-external-harsh-top4-rereview-2026-10-03/`.

No manuscript source, revision branch, previous report, retained volume or unrelated paper is modified by this review.

The active primary consists of the eight inputs

- `core/01_setting.tex`;
- `core/02_fingerprints.tex`;
- `core/07_effective_fingerprints.tex`;
- `core/03_local_acquisition.tex`;
- `core/08_value_probe.tex`;
- `core/04_inverse_certificate.tex`;
- `core/05_noisy_stopping.tex`;
- `core/06_comparison.tex`.

The acquisition, inverse/certificate and stopping chapters retain their v24 blob identities. I also inspected the response, proof/history/literature ledgers, source pins, publication binding, calibration code, local receipt, exact-SHA workflow and hosted workflow result.

## 3. The new theorem package

The observation now has four logically separate layers.

1. A laboratory trajectory experiment supplies encountered collision positions up to a bounded time.
2. A certified local value probe supplies Cartesian graph charts, boundary-height enclosures and distance-to-solid enclosures in fixed neighborhoods.
3. A finite bridge fingerprint identifies a translation class and one coherent transverse sign.
4. Two unconditional endpoint histograms at known absolute times recover two complete endpoint-density functions. These functions, not the finite fingerprint, reconstruct the stationary action, reflecting arcs and absolute free area.

For a selected clear normal bridge the retained law is

\[
f_T(s,t)=\frac{-W_{st}(s,t)}{2\pi A}(T-W(s,t))_+.
\]

On a strictly active rectangle two times give

\[
W=\frac{T_1f_2-T_2f_1}{f_2-f_1},\qquad
A=\frac{(T_2-T_1)(-W_{st})}{2\pi(f_2-f_1)}.
\]

The action derivatives reconstruct the two local arcs. Analytic continuation reconstructs complete obstacle images; congruence clustering and a spanning tree assemble visible types; non-tree records give cycle vectors. The completion defect

\[
\mathcal D=\operatorname{covol}\Gamma-A-
                 \sum_{i\in I}\operatorname{area}(C_i)
 =([\Lambda:\Gamma]-1)\operatorname{covol}\Lambda
   +\sum_{i\notin I}\operatorname{area}(C_i)
\]

vanishes exactly when every type is visible and the observed cycle subgroup is the full period lattice.

Version 25 makes the record-recognition stage numerically calibratable from prior bounds and implements it with local values. It does not change the function-valued endpoint-law inverse or the absolute-normalization mechanism.

## 4. Audit of the fixed-presentation compactness statement

The new compactness lemma avoids choosing a discontinuous reduced lattice basis. It keeps all bounded presentations `L`, writes representative Steiner centers as `L t_i` with `t_i in [0,1]^2`, and uses centered support functions with uniform holomorphic bounds. The matrix and inverse-matrix bounds make the lattice presentations compact; Montel compactness on narrower strips controls every fixed real derivative.

A bounded bridge is represented by a finite label `(i,j,k,epsilon)`. The bridge-length, diameter and inverse-presentation bounds uniformly bound `k`. Strict convexity makes the closest pair unique. The positive contact Hessian and implicit-function theorem give continuity of contact charts through each fixed order. The quarter-turn definition of the transverse frame avoids an angle-coordinate branch cut.

Changes of representative copies and unimodular basis changes merely relabel `k`. At cell faces and reduction walls the proof retains both descriptions rather than selecting one. The shape and physical-separation margins prevent two inequivalent fixed labels from becoming equivalent in the limit.

This supplies the topology that was only implicit in v24. I found no counterexample to the stated fixed-presentation compactness route.

## 5. Audit of the explicit continuation modulus

### 5.1 Interpolation on the first disk

For a function bounded by `B` in the strip and by `e` on a real interval, the proof interpolates at `m+1` equispaced nodes. On the disk of radius `a`, the sum of absolute Lagrange coefficients is bounded by

\[
\frac{2^m m^m}{m!}<6^m.
\]

The contour of radius `4a` gives the remainder

\[
\frac43 B(2/3)^{m+1}.
\]

Taking `m=floor(log(1/t)/log 9)`, `t=e/B`, gives a disk bound no larger than `3B t^(1/8)`. The constants are intentionally weak but correct. The restriction `a <= rho/8` keeps every contour strictly inside the strip.

### 5.2 Chain of disks

Hadamard three-circles at radii `a,2a,4a` turns a bound `Bu` on the inner disk into `B u^(1/2)` on the middle disk. Moving the center by at most `a` propagates the inner-disk estimate. With

\[
J=\lceil4/a\rceil,\qquad \vartheta_*=2^{-(J+3)},
\]

at most `J` steps cover a full real period and yield

\[
\sup_{\mathbb R}|f|\le3B(e/B)^{\vartheta_*}.
\]

The independent checks in this review verify the interpolation amplification, the radius and step inequalities, and the exact cancellation

\[
(m_0 2^{J+3})\,2^{-(J+3)}=m_0.
\]

This is a classical chain-of-disks estimate, not a new optimal continuation theorem. Its extreme exponent is accurately reflected by the later calibration.

## 6. Audit of quantitative bridge separation

### 6.1 From local graphs to complete convex bodies

The graph disk bound gives a uniform slope bound on the working interval. The curvature lower bound gives `psi'' >= kappa_*` in the chosen graph orientation, so a fixed normal-angle interval has supporting points inside the observed graph segment. Taking a support maximum is one-Lipschitz in the graph sup norm. Hence a gap error `d` and graph error `v` give support-value errors at most `v` and `d+v` on the two ends.

Centered support functions are bounded on the strip by the supplied `M`. Translating them to the source-contact frame adds only a controlled first harmonic. The manuscript's bound

\[
B=2\{M+(R_++D_0)3^{\lceil\rho\rceil}\}
\]

is conservative enough for the two pair differences. Applying the explicit strip estimate gives complete-pair Hausdorff control.

### 6.2 Locking the physical copies

A Hausdorff error `Delta` changes a Steiner point by at most `2Delta`; recentering gives support error at most `3Delta`. The shape gap excludes a different source type. The reflection margin excludes the wrong component of `O(2)`, and the rotation margin bounds the remaining angle by `9Delta/eta`.

After aligning the physical source copies by their true lattice translation, the target error is bounded by

\[
C_*\Delta,\qquad C_*=3+9(R_++2D_0)/\eta.
\]

Choosing `Delta_* <= d_0/(4C_*)` makes two distinct target bodies impossible because distinct physical bodies have separation at least `d_0`. The unique closest segment then fixes the normal and the transverse sign. This is a valid within-table rigidity argument under the declared pairwise noncongruence, asymmetry and physical-separation margins.

### 6.3 Jet and value fingerprints

For the jet fingerprint, the normalized coefficient error contributes at most `d/2` on `|y| <= r/2`; Cauchy bounds control the two Taylor tails. For the value fingerprint, the slope bound fills the intervals between the `N+1` grid nodes. With `d <= E_*/8`, the resulting local support errors are below the threshold `E_*`, so the continuation and physical-locking lemmas force equivalence.

The reversal action on the value fingerprint is exactly the permutation `j -> N-j`. Therefore the same registry proof applies. I found the stated error budgets consistent.

The theorem is genuinely computable in the classical finite sense. It is not computationally usable. The supplied example has `J=516`, `P=27*2^519` and `N=2^P`. Every complexity or resource summary must continue to state that the constants may dominate all epoch powers by an astronomical amount.

## 7. Audit of the value-only local probe

### 7.1 Certified differentiation

For three height values with deterministic error at most `epsilon`, centered differences satisfy

\[
|D_1-f'|\le M_3t^2/6+\epsilon/t,\qquad
|D_2-f''|\le M_3t/3+4\epsilon/t^2.
\]

These constants follow directly from the cubic remainder and the coefficient absolute sums. Taking `t` proportional to `nu` and value error proportional to `nu^3` gives `C^2` chart error `O(nu)` after local quadratic interpolation and a bounded-overlap partition of unity. No independence assumption is used.

### 7.2 Normal point and clearance

At a normal bridge the distance Hessian is positive. In value coordinates it is conjugated by bounded chart changes. Uniform `C^3` bounds control its modulus of continuity. A standard interval Newton or contraction test can therefore certify a unique normal root on a protected ball, while rejecting inputs without slack.

Facing support half-planes make the certified segment the global shortest segment for the two encountered convex bodies. A finite mesh of the one-Lipschitz distance-to-solid function certifies clearance away from endpoint collars. The endpoint collars are controlled by the local charts, convexity and the physical-separation margin.

The proof is credible but should be made slightly more operational in any final journal version: state one fixed choice of protected ball, interval-Newton residual threshold and mesh accuracy in terms of the displayed margins, rather than leaving all constants in prose. This is an exposition/completeness request, not a counterexample.

### 7.3 Intrinsic offsets

The arclength integrand `sqrt(1+(f')^2)` is one-Lipschitz in `f'`. Uniform derivative approximation and a mesh of size `O(nu)` therefore recover intrinsic offsets to `O(nu)`. Normal-root and endpoint-position uncertainty enter at the same order. The resulting coordinate error is exactly the kind charged by the retained histogram boundary-band argument.

The weaker probe is still strong. A boundary-height chart with certified coordinates and a query returning distance to **all** solid near a flight are active geometric observations. The theorem does not derive them from unmarked billiard collisions or endpoint counts.

## 8. Resource accounting

The correction to the stopping exponent is successful. The schedule now uses a chosen `a >= 6` consistently.

For a generic local probe with cost `P(nu) <= C nu^(-s)`, epoch `k` has cost of order `k^(3+s)`. Multiplication by the polynomial tail requires

\[
a>4+s
\]

for a finite expected total. At `a=6` this proof covers `s<2`, not `s=2`.

For value access,

\[
P_{val}(\nu)\le C(1+N)(1+\nu^{-1})V(c\nu^3).
\]

If `V(epsilon) <= C epsilon^(-s_v)`, then the effective probe exponent is `s=1+3s_v`; cumulative work through epoch `m` is `O(m^(5+3s_v))`, with a class-dependent constant containing `N`. The sufficient expected-work condition

\[
a>5+3s_v
\]

is correct.

The paper properly excludes analytic fitting, apparatus travel, setup and unrestricted bit complexity from the launch count. Those exclusions must remain adjacent to every complexity headline.

## 9. Qualifications and requested corrections

The following changes are needed for a polished specialist submission.

### 9.1 List the exact numerical prior inputs in the theorem statement

The effective calibration uses not only broad “analytic and geometric margins,” but specifically the support-strip bounds, local graph radius and bound `(R,M_g)`, curvature lower bound, bridge-length and diameter bounds, rotation and reflection margin `eta`, shape gap `sigma`, and physical-body separation `d_0`. Theorem 1.2 should list these explicitly or point to one numbered definition containing the full directed upper/lower-bound convention.

### 9.2 Clarify the value-query tolerance wording

The phrase “each requiring accuracy no smaller than `c nu^3`” is ambiguous because `epsilon` is an error tolerance. The proof requires height errors **at most** a constant times `nu^3`. State this as “error tolerance at most `c nu^3`” or define accuracy as the reciprocal tolerance.

### 9.3 Separate symbolic computability from executable fingerprint size

The exact-expression output is useful, but an implementation cannot expand or measure `N=2^P` nodes in the supplied example. The abstract already says the constants need not be practical. The theorem summary should also state that the hidden class constant in the query and epoch costs is proportional to this fixed fingerprint size.

### 9.4 Expand the current travel-time comparison

The literature section should include the 2023 Gurfinkel–Noakes–Stoyanov developments on uniqueness/rigidity of strictly convex obstacles from travelling times in Riemannian manifolds (`arXiv:2309.11141` and `arXiv:2311.07813`). They do not subsume the present periodic selected-record theorem, but they are part of the current nearest information category and should be acknowledged in a 2026 submission.

### 9.5 Keep the sensor contract in every headline

“Boundary values” means a certified Cartesian chart with coordinate coverage and arbitrary prescribed height accuracy, together with a distance-to-the-entire-solid oracle near the candidate flight. It is not a finite list of passive collision coordinates. The title is acceptable, but abstracts, talks and theorem summaries should preserve the phrase “active local value and distance access.”

## 10. Top-four significance assessment

### 10.1 The strongest observation remains richer than natural billiard invariants

Each record ultimately contains two complete two-dimensional endpoint-density functions, known branch times and local coordinate marks, and absolute normalization by the free area of the whole periodic cell. The new local sensor additionally supplies accurate boundary values and distance-to-solid information. This is far more informative than collision counts, an unmarked trajectory, a marked length spectrum, or ordinary scattering lengths.

### 10.2 The effective theorem packages strong global priors

The separation algorithm depends on supplied numerical lower bounds for asymmetry, inter-type shape distance and physical-copy separation, as well as complex analytic bounds. These priors are not inferred from the experiment. They rule out precisely the near-collisions of models that make recognition difficult. Converting them into an explicit finite threshold is useful, but it is not a broad rigidity principle beyond the compact generic class.

### 10.3 The new proof mechanisms are classical once the model is fixed

The main ingredients are equispaced interpolation, Cauchy bounds, three-circles, support functions, finite differences, interval contraction, quadrature, concentration, rational reconstruction and summable error spending. Their combination is nontrivial and carefully executed. It does not constitute a new general theory of inverse dynamics or analytic continuation.

### 10.4 The global unresolved problems remain outside the theorem

The paper does not prove passive unmarked-trajectory discovery, exact analytic count-only rigidity or nonrigidity, conventional marked-length rigidity on the stated class, or a minimax theorem for whole-table reconstruction. The earlier count fibers and testing results remain logically distinct.

### 10.5 Existing travelling-time rigidity emphasizes the information-model issue

Known exterior travelling-time and lens-rigidity theorems recover finite unions of strictly convex obstacles from global boundary scattering data in other settings. They do not contain the present periodic completion defect or local recognition construction. They nevertheless show that the editorial novelty must be located in the particular sensor reduction and certification architecture, not in obstacle recovery from rich travel-time-type data as such.

For a top-four venue, I would expect either a substantially more natural observation theorem, a removal of the decisive analytic/generic priors, a new global rigidity principle, or a sharp information-theoretic result for the physical experiment. Version 25 does not cross that threshold.

## 11. Independent diagnostics and source qualification

The accompanying `verify_review.py` imports no author module. In ordinary and optimized Python it performs 29,326 checks covering:

- Lagrange amplification and the explicit interpolation exponent;
- disk-chain radius, coverage and exponent cancellation;
- support-angle and strip translation bounds;
- shape, reflection and physical-copy locking margins;
- symbolic jet-tail and value-grid budgets;
- registry separation bands;
- deterministic first- and second-difference errors;
- arclength-integrand Lipschitz control;
- generic and value-query expected-cost exponents;
- retained subgroup/covolume and completion-defect algebra;
- translation invariance of relative contacts.

These checks are finite diagnostics, not a proof of compactness, analytic continuation, interval root certification, physical acquisition or the full retained programme.

The author local receipt records 5,490 checks, identical normal/optimized output and a warning-free 22-page primary build. It explicitly identifies that execution as primary-only source-content execution, not an authenticated checkout or physical experiment.

The exact-SHA GitHub Actions run `37111917413`, bound to the reviewed commit, completed successfully. Its job checked out the triggering SHA, validated the current sources and all declared submission volumes, and archived the receipts and delivered PDFs. Source delivery is therefore **not** a basis for the present rejection.

## 12. Final verdict

**Response to the v24 report:** substantively successful. The topology behind compactness is stated, the fingerprint constants are computable from numerical priors, the derivative/arclength sensor is reduced to value access, and the stopping exponent inconsistency is fixed.

**Mathematical audit:** no fatal counterexample found in the new v25 core; several presentation and literature updates remain.

**Editorial assessment:** the result is a rigorous, strongly conditional, active-sensor certification theorem. Its explicit fingerprint is formally finite but astronomically large; its global conclusion still depends on unusually rich function-valued data and decisive analytic/generic priors. This does not meet the exceptional conceptual standard of *Annals*, *Acta*, *Inventiones* or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.**