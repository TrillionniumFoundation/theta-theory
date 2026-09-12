# Independent referee-style report on A2 v29

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Author branch:** `revision/a2-v29-equivariant-density-stability-top4-2026-09-12`  
**Reviewed head:** `b137f2a92943d5491e0239eee193599eaa3728b8`  
**Reviewed tree:** `e3715007ef37041f85739f573904607b376cc304`  
**Mathematical-source commit:** `78852f2ccf828385fd45063c1b58c0d474ddf6c5`  
**Preceding review parent:** `5f10927a6399ebec0492b7f87b622ec80a4df631`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v29-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the standards sought for Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a representation of affiliation with those journals. The object is the pinned A2 revision, not A1 or the entire research programme. Stable source labels are used rather than unverified PDF page numbers. The accompanying [source audit](SOURCE_AUDIT.md) distinguishes complete module readings, sampled dependencies, executed diagnostics, and verification not performed.

## Recommendation and principal findings

**The v29 mathematical repair resolves T1. The stopped-history clarification is also resolved. C1 remains closed for the exact marked common-orientation datum. C2 remains open for the complete native main submission. I do not recommend unconditional acceptance of the assembled article at a top-four mathematics journal on the present evidence, but I find no new fatal counterexample and no basis in this audit for demanding another major mathematical reconstruction.**

These conclusions are deliberately separate. Correcting an off-model extension does not verify every inherited theorem. Conversely, an unexecuted full build does not show that a theorem is false. The appropriate next disposition is completion and inspection of the existing submission package, followed by assessment of the already stated contribution, not an automatic escalation to an unrelated new theorem.

| Item carried into this review | Finding at the pinned v29 head | Disposition |
|---|---|---|
| C1: exact common-orientation classification | The common action, lattice orientation character, and exact classification are retained; the revised corollary distinguishes its domains | Remains closed |
| T1: fixed-anchor reconstruction on arbitrary perturbed densities | The anchor is transported with the common orientation; equivariance and pairwise fixed-order stability are proved on an explicit open formula domain | Closed |
| Stopped-history hierarchy | All deterministic coarsenings are placed on one stopped-history space for one fixed policy; terminal censoring and adaptive-design information are retained | Closed for the stated forgetting maps |
| C2: complete native submission verification | Native-companion success and a selected-module fixture are reported, but neither observed hosted job executed any step and no complete native-main package was independently verified here | Open |
| Earlier observed-type and smooth-remainder repairs | Their principal arguments were re-examined; no ground to reopen them was found | No reopened objection |

The reviewed head is three commits ahead of the preceding review parent, with no divergence. A separate comparison from the mathematical-source commit to the reviewed head lists only navigation, response, diagnostic, and evidence changes, not mathematical TeX changes. The revision comparison lists no deleted files. These are repository comparisons, not deductions from version numbers. [S1, S2]

## 1. T1: the transported-anchor extension is correct

### 1.1 Exact-model inversion and off-model extension are no longer conflated

For the exact interior density

\[
f(u,v)=Z^{-1}B(u)B(v)\{d-S(u)-S(v)\},
\qquad t(u)=\frac{S(u)}{d-S(u)},
\]

the four-density ratio satisfies

\[
R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=1-t(u)t(v).
\]

Strict convexity, anchoring at zero, and an admissible nonzero anchor imply \(t(a)>0\). Consequently the positive scalar root at the anchor recovers \(t(a)\), and every admissible anchor gives the same action. This explains why the old error was invisible on the exact factorized family. [S4, `thm:v26-density-inverse`]

On an arbitrary nearby density, anchor independence need not hold. V29 correctly does not assert it. Instead it defines

\[
q_\alpha(f)=\sqrt{1-R_f(\alpha,\alpha)},\qquad
T_\alpha(f)(u)=\frac{1-R_f(u,\alpha)}{q_\alpha(f)},
\]

\[
S_{d,\alpha}(f)=\frac{dT_\alpha(f)}{1+T_\alpha(f)},\qquad
B_\alpha(f)(u)=\frac{f(u,0)}{f(0,0)}\{1+T_\alpha(f)(u)\}.
\]

The domain requires positive density, positive anchor radical, and positive \(1+T_\alpha\), on the specified compact square and interval. It does not require factorization, normalization to mass one, or physical realizability. All denominators and the scalar square root are therefore defined before the proposition is stated. [S3, `eq:v29-formula-domain`]

### 1.2 The reflection calculation includes the amplitude

Let \(f^r(u,v)=f(-u,-v)\). Direct substitution gives

\[
R_{f^r}(u,v)=R_f(-u,-v),\qquad
q_{-\alpha}(f^r)=q_\alpha(f).
\]

It follows on the entire formula domain, not merely on the exact model, that

\[
T_{-\alpha}(f^r)(u)=T_\alpha(f)(-u),
\]

and hence

\[
S_{d,-\alpha}(f^r)=S_{d,\alpha}(f)\circ\varsigma,
\qquad B_{-\alpha}(f^r)=B_\alpha(f)\circ\varsigma,
\quad\varsigma(u)=-u.
\]

The amplitude identity uses the reflected axis ratio as well as the action identity. It is explicitly included in the source. The three positivity conditions are transported to the domain with the opposite anchor, and reflection is an isometry for the fixed-order maximum-derivative norms. Using \(\alpha=\epsilon a\) in orientation sector \(\epsilon\) is therefore a valid equivariant extension. No hidden geometric parameter has been added: the sign of an already fixed coordinate anchor is transported with the coordinate convention. [S3, `prop:v29-transported-anchor`]

### 1.3 The pairwise stability proof does not assume a convex formula domain

A potentially serious point would have been an unjustified mean-value argument along a segment of densities that crosses a zero radical. The revised proof avoids this. It estimates differences by products and reciprocal identities between the two endpoints.

For example, at order zero suppose \(m\le f,g\le K\), both anchor roots are at least \(q_*\), and both \(1+T\) denominators are at least \(\nu\). Set \(e=\|f-g\|_\infty\). One explicit, nonoptimal bound is

\[
\|R_f-R_g\|_\infty\le C_R e,
\qquad C_R=\frac{2K}{m^2}+\frac{2K^2}{m^3}.
\]

The identity for the difference of positive square roots then yields

\[
|q_\alpha(f)-q_\alpha(g)|\le\frac{C_R}{2q_*}e.
\]

Writing \(A=1+K^2/m^2\), one obtains

\[
\|T_\alpha(f)-T_\alpha(g)\|_\infty
\le C_Te,
\qquad C_T=\frac{C_R}{q_*}+\frac{AC_R}{2q_*^3}.
\]

Finally,

\[
\|S_{d,\alpha}(f)-S_{d,\alpha}(g)\|_\infty
\le \frac{dC_T}{\nu^2}e.
\]

The amplitude follows from the same product bounds. These independent estimates confirm the structure of the source argument. At finite order, Leibniz's rule and repeated differentiation of \(h h^{-1}=1\) give the corresponding bounds in \(C^M\). The square root is a scalar evaluated at the nonzero anchor, not a differentiated square root at the action minimum. None of these steps requires a segment to remain in the nonlinear domain. Reflection preserves all the bounds, so the sector constants agree. [S3]

The dependence on positive density, anchor, and denominator margins is essential. This is not stability as \(a\to0\), \(d\downarrow0\), or \(M\to\infty\). V29 retains those qualifications.

### 1.4 The quotient and finite-jet conclusions follow on their stated domains

The datum is tagged: \((\epsilon,f)\sim(-\epsilon,f^r)\). There is one tag-aligning reflection for each pair of representatives. After alignment, the source's orbit distance is just the within-sector norm; changing representatives reflects both sides isometrically. The Lipschitz estimate therefore descends. For several channels, the same tag alignment is used throughout; independent channel reversals are not substituted. [S3, `cor:v29-density-orbit-stability`]

For contact reconstruction, the projection

\[
Ph=h-h(0)-uh'(0)
\]

commutes with reflection and removes spurious unanchored terms without changing coefficients of order at least two. The gap and quadratic action coefficients are invariant. At order \(n\), graph and action coefficients acquire the factor \((-1)^n\). The finite smooth-jet factorization ensures that the lower-jet remainder is well defined independently of smooth representatives. Reflection of those representatives gives its required parity. Since the last-jet block depends only on the quadratic geometry, the recursion commutes with reflection by induction. Smoothness of finitely many recursion steps on a sufficiently small positive neighborhood yields the stated error

\[
C_M(\tau^j+\varepsilon+\varepsilon_g).
\]

This remains a fixed-order statement in an interior density norm, with the inherited gap-error interpretation. It does not reconstruct a globally realizable analytic table from every arbitrary density perturbation. The explicit separation of local extension and exact global image is correct, rather than a reduction of the exact rigidity theorem. [S3, S4, S6]

### 1.5 The old witness is a regression check, not a new unresolved objection

For the previous positive-density example at \(a=1/4\) and \(\zeta=1/100\), the two incorrectly identified fixed-anchor squared outputs remain

\[
\frac{107}{22500},\qquad \frac4{837},
\qquad \text{difference}=-\frac{49}{2092500}.
\]

V29 retains this witness, explains its off-model scope, and repairs precisely the failed identity. The exact calculations were reproduced in this review. It would be incorrect to report the retained counterexample as evidence that the new transported-anchor proposition is false, or to promote it into physical-table nonidentifiability. **T1 is closed.** [S3; accompanying diagnostics]

## 2. The inherited contact inverse survives the specific re-examination

The substantive inverse is not the four-density cancellation alone. It needs the half-line action construction and the filtration through finite graph jets. I re-examined the weighted inverse, the finite-truncation envelope calculation, smooth-remainder interpolation, homogeneous isolation, and finite inverse recursion in the active signed-rigidity source. [S6]

The weighted Green estimate uses both summable ratios \(e^{-\gamma_-}/\rho<1\) and \(\rho e^{-\gamma_-}<1\). The local Hessian perturbation is then small in the same weighted operator norm, allowing the Neumann inverse and fixed-order derivative induction. This is an actual operator argument, not an appeal to a finite determinant alone.

For two graph pairs with equal jets through order \(M\), interpolate the graphs on a common small contact interval. The gap and quadratic operator remain fixed. The direct variation of each flight is

\[
\partial_t\ell_t(y,z)
=\frac{h_t(y,z)}{\ell_t(y,z)}
  \{\Delta\psi_0(y)+\Delta\psi_1(z)\},
\]

with contact labels adjusted to that flight. Since \(\Delta\psi_b(y)=O(|y|^{M+1})\), and the stationary orbit obeys \(|x_i(u)|\le C|u|\rho^i\), the direct variations have a summable \(|u|^{M+1}\rho^{(M+1)i}\) majorant. Finite differentiation cancels the interior orbit variations; the remaining terminal product tends to zero. Integrating the finite identity before taking the limit gives equality of the finite action jets. The proof requires the stated functional smooth bounds; bounded Taylor coefficients alone would not justify it. [S6, `lem:v27-smooth-jet-factorization`]

The new-jet block then follows from the pure degree contribution on the linear orbit. Counting the initial site once and the interior sites twice gives

\[
1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),
\qquad
2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

Thus \(\det M_n=1\) because \(\mathfrak r_0\mathfrak r_1=1\). The separate leading-curvature inverse and the lower-triangular recursion give the fixed-order inverse. This justifies the parity step used by v29. It is not an infinite-dimensional condition-number theorem.

I found no reason to reopen the smooth-remainder objection. Equal smooth jets do not imply equal smooth boundary images; the manuscript uses analyticity only for that later conclusion. Nevertheless, this module-level re-examination is not a new line-by-line certification of every earlier differentiated relative-law estimate on which finite-flight convergence depends.

## 3. C1 remains closed; intrinsic geometry is not a folded experiment

The active orientation subsection preserves the correct reflection of representatives,

\[
(\iota,(A_e),(C_{e,\sigma}))
\longmapsto (J\iota,(JA_eJ),(JC_{e,\sigma})),
\qquad J(x,y)=(x,-y).
\]

The two conjugations keep channel placements proper. The identity

\[
\tau_{-J\iota(\nu)}(JA_eJ)(JC_{e,\sigma})
=J\bigl(\tau_{-\iota(\nu)}A_eC_{e,\sigma}\bigr)
\]

transports the deck correction, not just the obstacle shape. Every improper Euclidean motion is a proper motion followed by this reflection, which supplies both directions of the quotient classification. The lattice orientation character changes with the common transverse convention. There is no unhandled fixed-point problem: even a reflection-invariant law has two different tagged representatives. [S5]

In the rank-two refinement, the marked cycle columns need only be independent over the reals, not a primitive integer basis. The identity \(L=VM^{-1}\) and its reflected form \(L^r=JL\) preserve the Gram matrix. The underlying uniqueness requires the declared signature-rigid transitions and rooted spanning tree. Writing an orientation quotient does not remove those hypotheses or select a phase in a nonsingleton gluing space. [S5, S7]

The datum remains an orbit of complete probability laws with retained relative signs and marked labels. It is not the distribution of absolute endpoint values, independently unoriented channels, or a mixture with reflection. The earlier density examples distinguish those maps but do not establish physical realizability of an unsigned counterexample. The revised stability corollary now invokes either the equivariant exact inverse on its image or the explicit transported-anchor local extension. **C1 remains closed for this precise datum.**

## 4. The stopped-history correction is adequate

The new hierarchy begins with one fixed, parameter-independent policy and a deterministic preparation cap. A countable disjoint union of finite marked collision arrays, followed by the finite products and disjoint unions allowed by that cap, provides a common standard Borel record space. Changing the table changes the law, rather than requiring a different underlying measurable space. The one-preparation map is correctly treated as a building block. [S8]

The endpoint-time transcript, count-endpoint transcript, and endpoint output are successive specified forgetting maps from this history. Their sigma-fields are therefore compared after pullback to the same space. Waiting-count encoding is equivalent to the full binary success history only when the terminal censored failure run and stopping information are retained. The independent diagnostic checked every binary history of lengths zero through eight, including histories with no successes; the mathematical point is the explicit encoding, not the number of checks.

The source also makes an important qualification that should remain: a retained adaptive design can encode information about an earlier residual time that is subsequently deleted. Hence a coarsened transcript is not the transcript of a retrospectively changed acquisition policy. The displayed hierarchy does not, by itself, imply that every adaptive coarsening has the same local limit as a particular fixed-design protocol. The asymptotic identifications are explicitly restricted to the protocols and hypotheses of the cited theorems.

The correction closes the preceding sample-space presentation issue for the stated forgetting maps. It does not assert a total-variation replacement theorem for every full growing collision array, and this review does not infer one.

## 5. Additional checks beyond the new subsection

### 5.1 Finite signature matching and compact global continuity are distinct

The active signature-stability argument does not infer unique matching from a scalar curvature value or an outside-arc gap. Analytic nonconstancy implies that at every point some positive-order curvature derivative is nonzero. Compactness selects a finite signature order with a uniform immersion bound. Trivial oriented symmetry on transition obstacles separates distinct complete signatures; a second compactness argument selects finitely many coordinates separating distant pairs. Enlarging the vector preserves the local lower bound furnished by its original block. [S9, `thm:v25-finite-signature-embedding`]

For a noisy curve, the source requires \(C^2\) control and proves positivity of

\[
\frac{d^2}{dx^2}\frac12|\widetilde J(x)-y|^2
=|\widetilde J'(x)|^2+(\widetilde J(x)-y)\cdot\widetilde J''(x)
\]

on a sufficiently small arc, while global separation excludes other arcs. That supplies a unique minimizer and a local Lipschitz estimate. It is not a false nearest-point uniqueness claim under arbitrary \(C^0\) perturbations.

The subsequent global inverse modulus uses a different argument: exact injectivity and compactness in the declared labelled topologies. The summable tail \(C2^{-M}\) belongs to a product metric; it is not an exponential analytic-continuation rate. The text states this distinction. I found no new gap in these specific arguments. Their applicability still requires the specified compact analytic class and rigid transition structure; those assumptions cannot be omitted in a summary of the theorem.

### 5.2 The physical pilot and finite-template estimator avoid the earlier oracle traps

The calibration model supplies marked channel labels and one sensor frame shared by the two contact types of a channel, but not relative placements between different channels. It records planar positions and failures. Its finite scan chooses a time grid before observation. The lower success bound is needed only at a grid point with excess in \([h,2h]\), not at arbitrary late times; earlier success only improves the upper onset bound. All unsuccessful trials are counted. [S10]

The pilot is run at the final chosen even flight number \(J\), so it controls \(J|\widehat g-g|\), rather than an error at a smaller flight number followed by an uncontrolled change of design. The estimated projection is observable. The ideal contact projection occurs only in the proof of its error bound. Likewise the total-variation continuity estimate applies to centered scalar laws, not to ambient position laws supported on different unknown curves.

The global estimator first selects finitely many bounded Lipschitz separators and a finite template library on the compact class, then chooses the sample size, flight number, and pilot resolution in the required order. Concentration is applied to an uncapped iid sequence of successful marks, and the batch-cap probability is added separately. The proof does not assert iid sampling by conditioning on cap completion. [S11]

The prescribed-budget construction runs a selected stage afresh; it is not a cumulative transcript containing all previous short flights. Consequently the claimed diverging minimum flight number is compatible with that implementation. The library and inverse moduli may be non-effective, as explicitly admitted. This is a consistency theorem, not a sharp analytic minimax rate or an efficient design-generation algorithm.

These are substantive qualifications, not defects to be reopened after they have been supplied. The experiment nevertheless remains richer than intrinsic transverse-law data: it uses exact planar positions in the charged pilot. The direct graph-sampling benchmark is therefore a necessary comparison, and the introduction acknowledges it. The global consistency conclusion must not be used to claim that half-line inversion is necessary in the richer position experiment. [S10, S11, S14]

### 5.3 The two-sided Poisson comparison has a genuine reverse kernel

The inspected deficiency source includes an explicit relative-density bound on the common bulk, \(\rho_{n,z}/\rho_{n,0}=1+O_K(k^{-1})\). Mere trace convergence would not suffice for the product Hellinger estimate; the manuscript now states this additional hypothesis and explains its fixed-window application. [S12]

The reference layer has one-record mass \(O(k^{-1})\). Its rescaled intensity approaches the target with error \(O_K(\varepsilon_{n,K}+k^{-1})\). At the intersection with the fixed face \(r=0\), an endpoint strip of area \(O(k^{-1})\) and residual thickness \(O(k^{-1})\) gives the required \(O(k^{-2})\) one-record corner mass. These orders are compatible after multiplication by \(k\).

The forward kernel extracts a reference-defined layer. The reverse kernel maps Poisson points back, fills the remaining records with the reference conditional bulk law, and randomly interleaves them. Corner exceptions and excess point counts are defined explicitly. Since the conditional bulk Hellinger square is \(O(k^{-2})\), replacing at most \(k\) bulk records costs \(O(k^{-1/2})\) in total variation. This supports the conditional bound

\[
\Delta\le C_K(\varepsilon_{n,K}+k^{-1/2}),
\]

rather than only convergence of an extracted point process. The kernels may use fixed local reference quantities, not the unknown local parameter. This local experiment statement is not automatically a globally calibrated kernel for unknown tables. I checked the layer/bulk proof as stated, not every inherited expansion or every LAN assertion in Part II.

### 5.4 The observed-type distinction remains necessary and correct

The active homothety argument concerns matched successful records. When the observed obstacle varies, distinct anchored strictly convex homothetic boundaries meet only at the fixed anchor; deleting that zero-probability point produces pairwise disjoint full-probability output events. A kernel applied to a commonly dominated scalar family has all its output laws dominated by one probability measure, which can charge only countably many such disjoint events. This gives worst-case deficiency one. [S13]

When the observed obstacle is fixed, its graph embedding and transverse projection are parameter-independent inverse maps on the supported patch, giving equivalence. The result compares records with the same residual-time retention. It neither makes a wrong assertion of common non-domination for finite-strip Poisson families nor discards failed preparations from the distinct unconditional acquisition protocol. No reason to reopen the observed-type correction was found.

## 6. C2: progress is real, but a complete native main remains unverified

The author's execution record now reports a successful build of the unchanged native `two_collision.tex`: seven pages, with source and product hashes and an encoded bundle of complete logs. That is stronger evidence than a replacement fixture. I read the execution record, but did not independently rebuild the companion, decode and audit all those logs, or inspect its PDF. Accordingly this review records the advance as author-supplied companion evidence, not as a new reviewer-issued native-companion certificate. [S15]

The same record labels the ten-page selected-module output as a fixture. Its eighteen unresolved-reference occurrences involve seventeen inherited labels outside that selected input set. They do not establish unresolved references in the full article. Equally, the fixture cannot certify the full native main, its appendix closure, bibliography, or companion links.

The following job observations were independently obtained from the live authenticated GitHub endpoints:

| Run | Job | Mathematical source | Completion on September 12, 2026, UTC | Executed steps |
|---|---|---|---|---|
| `34679614994` | `103515663273` | `e468c075b0e57e015e774829f5886ce2322e6c02` | `07:00:56`, failure | `[]` |
| `34680067058` | `103516970408` | `78852f2ccf828385fd45063c1b58c0d474ddf6c5` | `07:11:21`, failure | `[]` |

Both jobs report runner ID zero and an empty runner name. No checkout, source audit, diagnostic, or TeX step is recorded. These facts show that the inspected hosted attempts did not execute the required verification. They do not establish a TeX error, a billing explanation, a permission explanation, or any other infrastructure cause. This review did not rerun workflows or alter repository settings. [S16; `ci_observations.json`]

**C2 remains the existing bounded request:** provide a source-pinned complete native package for the actual main and companion entries, with the full recursive mathematical input closure, executed reference/citation checks including external companion references, successful native logs and tool versions, complete PDFs with hashes, and inspection of remaining layout warnings. If the submission head differs from the build source only in evidence files, demonstrate the identity of the mathematical input closure.

A functioning local environment is sufficient; a particular hosted runner is not a mathematical requirement. Another manifest or selected-module fixture is not execution of the full task. No deletion of auxiliary mathematics, shortening of the article, or substitution of a reduced entry is requested. Compilation does not prove mathematics, but an assembled inspectable submission is a necessary condition for an assembled-submission recommendation.

## 7. Significance, literature, and top-four presentation

My strongest positive assessment concerns the geometry-specific chain from the uniform nonlinear relative law through the unsymmetrized contact inverse to intrinsic periodic recovery under explicit incidence hypotheses. The new equivariant extension correctly completes a stability convention in that chain. It is not, by itself, a new flagship result. Neither the elementary four-density cancellation, the identity \(L=VM^{-1}\), the finite-group quotient, nor compact inverse continuity independently establishes exceptional significance. The difficult forward estimates and the contact-action mechanism must carry the principal mathematical weight. [S3–S7, S9, S14]

The limited primary-source comparison confirms that observation maps matter. De Simoi–Kaloshin–Leguil study marked-length determination of analytic chaotic billiards with axial symmetry and genericity conditions. Finamore–Leguil study an enriched marked length spectrum for finite-horizon Sinai billiards. Meister–Reiß give a regression-to-Poisson equivalence precedent for nonregular errors. These works concern different observations and hypotheses. Their abstracts neither prove that A2 follows from them nor establish that every A2 mechanism is unprecedented. Only their abstracts and version metadata were checked in this review; an exhaustive priority assessment was not performed. [L1–L3]

The inspected introduction now distinguishes noiseless position sampling from intrinsic transverse-law inversion and separates standard structural steps from the more difficult inverse mechanism. That is preferable to inflating the global physical consistency statement or treating an arbitrary number of revisions as evidence of significance. The private referee memoranda in the bibliography must remain provenance, not external scientific validation; the manuscript's explicit disclaimers should be preserved. [S14, S17]

I would not issue an unconditional top-four acceptance recommendation on the basis of this audit. This is not an adverse theorem about the research programme, nor a demand for a different article. It is a judgment about the currently validated submission and the limits of the evidence inspected. Passing T1 must not be advertised as certification of every inherited forward estimate, every asymptotic experiment, or the entire auxiliary compendium.

## 8. Executed checks, limitations, and final requests

The author's v29 diagnostic was reproduced byte-for-byte, checked against Git blob `bd27b08638c9ca2d92f77eb848ac69d24f18fd1f`, and run using Python 3.13.5 in ordinary and optimized modes. Both outputs were byte-identical and passed **12,443** checks. The source SHA-256 is `efa21131f44d3af8a5740f96f78b0c0ae3d3bb4c16819dc3dabaff9446e3a458`. The reproduced output is retained as [author_checks_reproduced.json](author_checks_reproduced.json).

The separately written [independent diagnostic](independent_checks.py) was also run in both modes with byte-identical outputs. Its **5,033** exact rational checks include nonsymmetric nonfactorized perturbations, anchor transport, nonunit-offset exact recovery, normalized amplitudes, last-jet blocks, all binary stopped histories through length eight, retained adaptive-design information, and normalized layer/bulk arithmetic in a moving-ceiling toy model. The [result](independent_checks.json) identifies its script hash and precise scope. These finite computations do not certify continuum norm bounds, infinite half-line convergence, physical realizability of arbitrary densities, or whole-paper correctness.

No complete native-main build, full recursive source audit, proof-assistant verification, or complete-PDF inspection was executed in this review. The original relative-law construction, all local asymptotic experiments, the companion mathematics, and every auxiliary chapter were not independently rechecked line by line. These limitations are recorded to prevent a module-level review from being promoted into an unsupported acceptance certificate.

**Final requests are bounded.** Preserve the now-correct transported-anchor convention and its off-model domain; preserve the common tagged orientation datum and the fixed-policy stopped-history formulation; complete C2 on the unchanged full submission; and retain the stated distinctions between exact laws, finite samples, physical position acquisition, and fixed-order versus global stability. No new theorem is required solely because the earlier objections have been answered.

**Final disposition:** T1 closed; hierarchy clarification closed; C1 remains closed; C2 open. No new fatal mathematical counterexample was established. Further native-submission validation and assembled-manuscript assessment are required before an acceptance recommendation.

## Source key

Except for the explicitly identified repository metadata and prior review, paths below are relative to `papers/A2-v17-boundary-information-coarsening` at the reviewed head. They refer to immutable source contents, not the moving revision branch. Reading scope and selected blob identities appear in [SOURCE_AUDIT.md](SOURCE_AUDIT.md).

- **S1:** Repository root `README.md`, `main.tex`, revision commit metadata, and comparisons `5f10927a...b137f2a9` and `78852f2c...b137f2a9`.
- **S2:** `RESPONSE_TO_REFEREE_V29.md`; repository-relative `reviews/a2-v28-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`.
- **S3:** `article/23f1_equivariant_density_extension_v29.tex`.
- **S4:** `article/23f_single_offset_law_inverse_v26.tex`.
- **S5:** `article/23h_global_orientation_quotient_v29.tex`.
- **S6:** `article/23a_signed_endpoint_rigidity_v27.tex`.
- **S7:** `article/23d_rank_two_lattice_recovery_v24.tex`.
- **S8:** `article/01b_observation_hierarchy_v29.tex`.
- **S9:** `article/23e_signature_stability_v25.tex`.
- **S10:** `article/25a_common_observables_v25.tex`.
- **S11:** `article/25b_augmented_global_reconstruction_v26.tex`.
- **S12:** `article/18c1_endpoint_time_deficiency_v25.tex`.
- **S13:** `article/18f_domination_and_position_comparison_v27.tex`, through the principal domination, observed-type, and matched-time proofs; later examples not fully reread.
- **S14:** `article/01_introduction_v27.tex`, first 220 source lines.
- **S15:** `VERIFICATION_V29.md`; its reported build executions are distinguished from reviewer executions above.
- **S16:** Live Actions run collection for the author branch and job collections for runs `34679614994` and `34680067058`.
- **S17:** `v5/references_v25.tex`, bibliography content inspected.

### Primary literature: limited abstract and metadata comparison

**L1.** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, revised August 17, 2022. Related journal DOI: `10.1007/s00222-023-01191-8`.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. No later version or publication status is asserted here.

**L3.** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248v1, submitted January 27, 2011.

The three arXiv abstract pages and their version metadata were consulted on September 12, 2026. This bibliography does not imply that their complete proofs were independently verified for this report.
