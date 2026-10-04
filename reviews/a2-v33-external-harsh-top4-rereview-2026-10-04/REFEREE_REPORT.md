# External top-four referee report on A2 v33

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v33-finite-precision-sequential-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v33-referee-copy-2026-10-04`  
**Reviewed commit:** `245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`  
**Reviewed repository tree:** `98f56b2e1433701e95f0e01e98d26d6dcada1ed8`  
**Native paper tree:** `213cecf77265c5ebea98791a99126b9def5d25f0`  
**Mathematical checkpoint:** `a3c4b12d2d56d67a7569e3b239f0bcea8f546ee3`  
**Controlling preceding report:** `058d2b7b773038cfa7e43f7f52a3b79fdc4107f6`  
**Manuscript directory:** `papers/A2-v33-finite-precision-sequential`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, formal proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 33 is a genuine and mathematically substantive response to the v32 report. It does not merely add resource-accounting prose. The revision supplies four concrete advances:

1. an explicit finite dyadic realization of the adaptive collision protocol, including command-description and output-description bounds;
2. a parameter-independent laboratory gauge and a proof that the physical packing remains separated after Steiner centering;
3. a genuinely sequential expected-stopping lower bound, rather than an unsupported extension of the deterministic-cap theorem; and
4. a physical common-response construction showing that, in the stipulated worst-case bounded-position-error model, insufficient calibration cannot be compensated by arbitrarily many additional collision bits.

On the new v33 core audited in detail, I found no fatal counterexample. The single-grid dyadic stencil, rounded bisection recurrence, prefix-free stopped-word inequality, centered packing estimate, expected-length information lower bound, swept-set Hausdorff estimate, separated-sweep geometry, and common-response coupling are coherent under the hypotheses stated. The retained v32 upper and deterministic lower bounds remain active, and the exact-source sixteen-document workflow succeeds at the reviewed SHA. The negative recommendation is therefore not based on a known false central theorem or a source-delivery failure.

The remaining objection is conceptual and editorial. The strongest new converse is deliberately tied to a very adversarial calibration class: the actual-start perturbation may depend on the unknown table, the nominal command and the nominal draw, and the actual start is not observed. Two different tables are rendered indistinguishable by two different admissible implementation kernels. This is a valid minimax statement, and it usefully proves that the paper's shrinking tolerance is not merely an omitted sample factor. It is not, however, a universal physical resolution law. It says nothing comparable for a common fixed offset, table-independent jitter, a known mean-zero noise distribution, replicated metrology, observed actual starts, or longer-flight controls.

Likewise, finite dyadic command descriptions do not price the construction of the localized launch distribution, actuator precision, apparatus travel, calibration production, or the full bit complexity of the physical interface. Once the reciprocal collision means have been converted into approximate membership queries, the geometric upper bound is built from classical active boundary search and interpolation, while the sequential lower bound is classical coding/information theory applied to a one-dimensional Hölder packing. The synthesis is careful and meaningful, but the principal abstract mechanisms are not transformative.

The whole-table conclusion also remains conditional on a bounded periodic presentation, known smoothness and curvature bounds, a fixed protective aperture, and a known positive nonperiod-patch margin for uniform finite period decisions. It does not infer crystallinity from an arbitrary configuration and does not establish rigidity from passive trajectories, count germs, marked lengths, or spectra.

In my judgment v33 is a strong specialist-journal candidate after a fresh human proof review and modest clarification of the calibration experiment. It remains below the exceptional naturality, breadth, and conceptual reach expected by the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

Both v33 branch names listed above resolve to author head

`245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`

with repository tree

`98f56b2e1433701e95f0e01e98d26d6dcada1ed8`.

Its parent is the mathematical checkpoint

`a3c4b12d2d56d67a7569e3b239f0bcea8f546ee3`,

which is based directly on the v32 external-review head

`058d2b7b773038cfa7e43f7f52a3b79fdc4107f6`.

That report reviewed v32 author head

`eeb171d4e00242c9813c10e2124556b2cee480d3`.

The exact complete v32 paper is retained under

`papers/A2-v33-finite-precision-sequential/retained/v32`

at tree

`2a7d949f43dcb7b84d4a85ef8a4436349f615493`.

Its six active v32 proof chapters are also retained byte-for-byte in the v33 primary, with original core tree

`b0655672858cd000e2c6d939f681ec47b35eb716`.

No A2 revision later than v33 existed when this review was frozen. The review branch starts directly from the author head and adds files only under

`reviews/a2-v33-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, prior report, author revision branch, retained volume, workflow, or unrelated paper is modified.

The active primary consists of:

- `core/00_setting.tex`;
- `core/00b_resource_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/06_finite_precision.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `core/05_comparison.tex`.

I also inspected the response, proof/history/literature ledgers, source pins, submission map, validation tools, local receipt, exact-SHA workflow and run, retained v32 source, and the complete v32 external report.

## 3. The theorem package and information model

Each attempted preparation returns one bit. For a nominal start `q` and displacement `a`, the bit is one exactly when `q` is free and the unreflected segment `[q,q+a]` first meets a solid. A solid start and a free miss both return zero and both remain in the denominator.

The controller chooses a localized start distribution, the four-direction compass displacement law, and the translated reciprocal reverse law. The pointwise identity

\[
B_a(q)-B_{-a}(q+a)
 =\mathbf 1_{\mathcal O}(q+a)-\mathbf 1_{\mathcal O}(q)
\]

turns two pooled means into the forcing

\[
g_\sigma=(T-I)u_\sigma,
\qquad u_\sigma=\kappa_\sigma*\mathbf 1_{\mathcal O}.
\]

The retained v32 theorem uses finitely many local killed-Bellman evaluations, a coarse acquisition, robust radial bisection, and degree-six boundary interpolation. With `s=6+beta`, it reconstructs at `C^2` accuracy `nu` using

\[
N_\nu\le C\nu^{-1/(s-2)}
       \log(C/\nu)\log(C/(\nu\delta))
\]

attempted collision bits and localization/calibration scale

\[
\sigma\asymp \nu^{s/(s-2)}.
\]

The retained deterministic-cap lower bound has the same power in `nu`, up to logarithms.

Version 33 adds:

- a finite dyadic command and output encoding;
- an expected-stopping lower bound of order `nu^{-1/(s-2)}`;
- a centered-gauge proof for the packing; and
- a worst-case calibration necessity of order `nu^{s/(s-2)}`.

## 4. Audit of finite dyadic controls

The digital construction rounds one target point to a dyadic mesh and then forms the complete compass dependency stencil by exact addition of a dyadic step. This is the correct way to preserve reciprocal translation: rounding every dependency point independently would break the algebraic stencil.

The finite Bellman calculation uses empirical Bernoulli counts and rational arithmetic. The bisection proof allows the rounded midpoint to differ from the exact midpoint by at most the mesh size `d`. If `w_k` is the geometric bracket width, then

\[
w_{k+1}\le \frac12w_k+d,
\]

and hence

\[
w_k\le 2^{-k}w_0+2d.
\]

Thus rounding produces a mesh floor rather than a loss linear in the number of bisection stages. The pre-existing indeterminate boundary layer and the dyadic floor can be absorbed in the radial-value error budget.

On the bounded aperture, a dyadic center, scale, repetition count, and confidence allocation require only logarithmically many bits in `nu^{-1}` and `delta^{-1}`. The stated total digital-control order is consistent with multiplying this per-batch description by the established query count.

The manuscript correctly separates this from physical implementation. Describing a kernel center and scale does not manufacture the launch distribution or certify the actuator. The conditional arithmetic bound also depends on effective numerical representations of the prior constants, kernel, partition of unity, and elementary-function evaluations. These qualifications must remain in every summary of the bit-complexity theorem.

## 5. Audit of the lower-bound gauge and centering

The disclosed lower-bound information is parameter-independent: fixed laboratory axes, the lattice, species names, and the fixed second obstacle. The unknown Steiner point and orientation-dependent bump pattern are not supplied.

For the packing supports `p_omega`, the difference of two raw supports is uniformly `O(h^s)` in `C^0`. The Steiner map

\[
z(p)=\frac1\pi\int_0^{2\pi}p(\theta)n(\theta)\,d\theta
\]

therefore changes by `O(h^s)`. Subtracting the corresponding first harmonic changes the `C^2` norm by the same order. At a differing bump center the second derivatives differ by `c h^{s-2}`. Since `h^s=o(h^{s-2})`, the centered supports remain separated by `c' h^{s-2}`.

This closes the gauge ambiguity identified in the v32 report. “Pose given” no longer hides a parameter-dependent translation or rotation, and the lower bound is proved for a weaker centered-shape loss before being transferred to the stronger physical output.

## 6. Audit of the sequential expected-length lower bound

Condition on all parameter-independent controller randomness. A stopped binary protocol has a prefix-free set of terminal words: once the protocol stops at a word, it cannot also stop at a strict extension. Kraft's inequality and the log-sum inequality give

\[
H(Z\mid U=u)\le \mathbb E(|Z|\mid U=u).
\]

After averaging over the independent seed `U`,

\[
I(V;Z,U)\le \mathbb E\mathsf T.
\]

Disjoint acceptable output sets provide a decoder. The elementary conditional-entropy/Fano estimate then yields

\[
\frac1M\sum_{j=1}^M\mathbb E_j\mathsf T
 \ge (1-\delta)\log_2 M-h_2(\delta).
\]

Applied to the centered physical packing with `log M` of order `nu^{-1/(s-2)}`, this proves the asserted worst-case expected-attempt lower bound. Continuous command values and the stopping time do not create an extra information channel because, after the seed is fixed, both are functions of the observed terminal word.

I found this argument sound. It is important, however, not to overread it. It gives the principal power at fixed confidence. It does not prove sharp confidence dependence, logarithmic optimality, or an expected-cost lower bound for apparatus motion, controller arithmetic, or calibration production.

## 7. Audit of the physical common-response coupling

For one convex body, the hit bit can be represented by the swept body

\[
S_a(C)=C+[-a,0].
\]

Under the closed-solid convention, the bit is the indicator of the sweep minus the indicator of the body. If distinct bodies are separated by `d_0` and `|a|<d_0`, distinct swept bodies are separated by at least `d_0-|a|`. Therefore a nominal start with bit one identifies a unique responsible component.

Matched bodies at Hausdorff distance at most `e` have swept bodies at Hausdorff distance at most `e`. Suppose the nominal bits are `(1,0)`. In the zero table, either the nominal start lies in the matched solid or it lies outside the matched closed sweep.

- In the first case, moving the hit-side start into its own matched solid by at most a constant multiple of `e` forces a zero.
- In the second case, an outward move beyond the hit-side sweep by at most a constant multiple of `e` forces a free miss.

The separation margin prevents the move from entering another swept body. Reversing the roles handles `(0,1)`. Agreeing bits require no perturbation. The construction can be made measurable by metric projection and a measurable normal selection.

Applying the deterministic map independently to every fresh nominal draw preserves conditional independence. Coupling the controller seeds and nominal draws across the two parameter values then gives identical bit histories for every adaptive, bit-measurable protocol. The support-bump pair has Hausdorff distance `O(h^s)` and centered `C^2` distance `c h^{s-2}`, giving the necessary relation

\[
r\lesssim \nu^{s/(s-2)}.
\]

I found no fatal geometric error in this mechanism.

The interpretation must be stated with precision. The two worlds use two different table-dependent admissible perturbation maps. The theorem is consequently a minimax nonidentifiability result over a worst-case uncertainty class, not a claim that a single table-independent noise device produces the same data in both worlds. This distinction is already present in the text, but it is central enough to belong immediately in the theorem headline and abstract.

## 8. Necessary corrections and qualifications

### 8.1 State the uncertainty quantifiers in one formula

The calibration theorem should write the order of quantifiers explicitly, for example:

\[
\forall\mathcal A\ \exists(\mathcal O_0,K_0),(\mathcal O_1,K_1)
\quad\text{such that}\quad
\mathsf{Law}_{\mathcal O_0,K_0}(Z)
 =\mathsf{Law}_{\mathcal O_1,K_1}(Z),
\]

where each `K_j` is an admissible table-dependent bounded-error implementation. This would prevent readers from mistaking the result for a lower bound under one common known or table-independent noise law.

### 8.2 Clarify the boundary convention in the common-response lemma

The proof uses closed solids and closed swept sets. The statement should explicitly say that boundary starts are assigned through the same inward/outward perturbation before evaluating the forced response. The null-set convention is immaterial statistically but matters in a pointwise lemma quantified over every nominal start.

### 8.3 Keep command descriptions separate from physical precision

A finite dyadic word for `(x,sigma)` does not by itself guarantee that the apparatus samples the prescribed localized distribution or realizes the required start tolerance. The paper does distinguish these resources; the abstract phrase “finite dyadic descriptions” should remain adjacent to the separate physical tolerance statement.

### 8.4 Do not advertise a universal calibration threshold

The necessary exponent is proved for short collision commands, unobserved actual starts, and arbitrary table-/command-/draw-dependent bounded perturbations. The manuscript correctly excludes fixed offsets and known mean-zero laws. These exclusions are not technical footnotes; they define the theorem.

### 8.5 Simplify the submission architecture

The 21-page primary is substantially clearer than the historical programme, but the package still nests sixteen declared documents and preserves earlier names such as “Supplement R” inside “Supplement R32.” This is reproducible but editorially cumbersome. A specialist submission should provide one self-contained article plus only the proof appendices actually needed for its active theorem, while retaining the full chronology in the repository rather than the journal package.

## 9. Top-four significance assessment

Version 33 closes the most concrete resource-accounting objections left by v32. It now has a coherent four-part statement: an adaptive attempted-bit upper bound, matching deterministic and expected-bit lower powers, finite digital descriptions, and a matching worst-case position-resolution power.

That is a meaningful result. It remains a theorem about a highly engineered active experiment. The controller chooses a continuum of spatial inputs, implements reciprocal translated preparations, and must realize an accuracy-dependent physical calibration. The global recognition theorem assumes periodicity, a bounded presentation, and a known discrete margin. The calibration lower bound obtains its sharp power by allowing the uncertainty implementation to vary adversarially with the table and command.

The mathematical ingredients—reciprocal cancellation, killed random-walk inversion, line search, Hölder interpolation, metric entropy, prefix coding, Fano's inequality, and convex swept-set geometry—are classical individually. Their assembly in this billiard sensor is careful and appears novel within the focused comparison, but it does not reveal a new general rigidity principle or transform a standard passive invariant.

For the requested four-journal benchmark, the information model is too specialized and the global hypotheses too strong. The principal advance is a sharp resource characterization inside that model, not a broad theorem about dispersing billiards or inverse geometry.

## 10. Literature and novelty boundary

The active upper-bound comparison with Castro--Nowak and Locatelli--Carpentier--Kpotufe remains appropriate. Those papers supply class labels or membership-style responses directly, whereas the present experiment first derives an approximate membership response from pooled reciprocal collision bits. The v33 manuscript does not claim line search or polynomial boundary interpolation as abstract novelties.

Shannon's source-coding framework supports the prefix-free entropy step; the paper writes the stopped-word argument in full rather than citing a black-box sequential theorem. General membership-query and region-based active-learning papers study related adaptive binary transcripts but not this swept-set collision sensor or its table-dependent calibration ambiguity.

Approximate polytope-membership work also uses indeterminate boundary layers, but there the body is preprocessed and the question is query data structure complexity, not learning an unknown physical obstacle through collision commands.

In a focused primary-source search I did not locate a theorem containing the exact combination of reciprocal collision cancellation, adaptive smooth-boundary recovery, expected stopped-bit lower bounds, and the physical common-response calibration converse. This is not an exhaustive priority claim.

## 11. Source qualification and independent diagnostics

The author's local source-content receipt records:

- 117,772 new finite diagnostics;
- 36 new validation-contract checks;
- 11,647 retained v32 diagnostics and 42 retained contract checks;
- identical ordinary and optimized Python output;
- a 21-page primary with no final TeX diagnostics;
- no physical sensor execution and no formal proof certificate.

The exact-source GitHub Actions run `37165176734`, bound to the reviewed SHA, completed successfully. Its job checked out the exact triggering source, qualified all sixteen declared documents, archived the actual source/evidence, and uploaded the bound artifact. Source delivery is therefore not a basis for the recommendation.

The accompanying independent `verify_review.py` imports no author code. Ordinary and optimized Python executions agree byte-for-byte and perform 1,129,071 checks. They cover reciprocal truth tables, exact dyadic stencil arithmetic, rounded-width recurrences, centering and exponent algebra, prefix-free entropy examples, sequential information inequalities, one-dimensional swept-set common responses, adaptive transcript identity, and retained bounded-denominator/Hermite arithmetic.

These checks are diagnostics only. They do not prove the continuum common-response lemma, execute a physical apparatus, rebuild TeX, establish literature priority, or certify the retained multi-volume programme.

## 12. Final verdict

**Response to the v32 report:** substantively successful. The gauge ambiguity, deterministic-versus-sequential distinction, finite-control description, and calibration-resource objection have all received real mathematical answers.

**Mathematical audit:** no fatal counterexample found in the new v33 core under its declared worst-case active sensor model. Several quantifier and presentation clarifications should be made.

**Delivery audit:** exact-source sixteen-document qualification passes at the reviewed SHA.

**Editorial assessment:** strong specialist-journal potential, but insufficient naturality and universal conceptual reach for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

**Recommendation: reject at the requested top-four benchmark.**
