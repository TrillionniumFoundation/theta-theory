# Response to the v28 referee — A2 v29

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 12, 2026

The addressed report is [the v28 external report](../../reviews/a2-v28-external-harsh-top4-2026-09-12/REFEREE_REPORT.md), at review commit `5f10927a6399ebec0492b7f87b622ec80a4df631`. It reviews author head `f5fcd5e319cb4a37bdcbf8d9f9d190786ec7fc7d`. This revision descends from that review commit. Its mathematical source is pinned at `78852f2ccf828385fd45063c1b58c0d474ddf6c5`; the first substantive source commit is `e468c075b0e57e015e774829f5886ce2322e6c02`.

We thank the referee for separating the now-proved common-orientation classification from the remaining off-model stability issue and the independent native-build requirement. The response below does not equate those three questions. The exact geometric classification is preserved. The off-model extension is repaired on an open neighborhood of general positive densities. Native companion verification has now been executed, but complete native-main verification has not, so C2 is not marked closed.

## C1. Common-orientation classification: preserve the closed result

The referee closes C1. The definition of the complete-law orientation orbit, the reflection-equivariance lemma, the gluing identities, and both directions of the periodic classification proof remain unchanged. The orientation character of the marked lattice and every transverse convention are transported together. No independent channel reversal, pointwise absolute-value map, or reflected mixture is substituted for this datum.

The active orientation source is now `article/23h_global_orientation_quotient_v29.tex`. Everything before its holonomy/stability corollary is byte-identical to the preceding source, as is the entire final folded-record remark. All inherited labels are retained in their original order. The corollary and its proof now distinguish the exact-law inverse from an extension to arbitrary nearby densities and refer explicitly to the new extension below. The intrinsic multichannel source, the holonomy reconstruction, and the recovered Gram-form and scale statements are untouched.

## T1. An equivariant extension on perturbed densities

### The defect and its exact scope

We agree with the referee's calculation. If the same signed anchor is held fixed in both sectors, reflection gives

\[
 S_{d,a}(f^r)=S_{d,-a}(f)\circ\varsigma,
 \qquad \varsigma(u)=-u,
\]

not, in general, `S_{d,a}(f) composed with varsigma`. On the exact factorized law family the inverse is anchor-independent, so this defect does not change the exact classification. It does affect an assertion about arbitrary nonfactorized density perturbations. The revised argument addresses that latter assertion directly rather than removing its perturbation neighborhood.

### Transport the anchor with the common orientation

The new subsection [Equivariant reconstruction of perturbed densities](article/23f1_equivariant_density_extension_v29.tex), labelled `subsec:v29-equivariant-density`, fixes one positive magnitude `a`. In sector `epsilon` the formula uses anchor `epsilon*a`. This is a coordinate convention, not a supplied geometric parameter or an additional observation. All contacts and edges use the same orientation tag; their fixed positive anchor magnitudes may differ.

The formula domain is specified before the statement. It consists of positive `C^M` functions for which the anchor radical and `1+T` are positive. It does not require factorization or probability normalization. Reflection exchanges the domains for `alpha` and `-alpha`. Proposition `prop:v29-transported-anchor` proves, on this entire domain,

\[
 T_{-\alpha}(f^r)=T_\alpha(f)\circ\varsigma,
 \quad S_{d,-\alpha}(f^r)=S_{d,\alpha}(f)\circ\varsigma,
 \quad B_{-\alpha}(f^r)=B_\alpha(f)\circ\varsigma.
\]

The proof starts with the four-density ratio and transports its scalar radical and numerator exactly. The amplitude ratio on the coordinate axis is included; it is not left as an implicit consequence about the action alone.

### Uniform stability without a hidden convex-domain assumption

The same proposition gives pairwise `C^M` Lipschitz bounds on sets with a positive lower density bound, a bounded `C^M` norm, a positive anchor-radical bound, and a positive lower bound for `1+T`. The constants are identical in the two reflected sectors. Compact exact-model families and their reflected copies have common neighborhoods of this form.

The proof controls differences directly by product and reciprocal identities and by the sum-of-square-roots denominator. Thus it does not assume that the segment between two arbitrary perturbed densities remains in the nonlinear formula domain. It also does not differentiate a square root at the action minimum. The statement holds for every pair satisfying the bounds, rather than only a model point and one perturbation.

### Quotient stability and finite contact jets

Corollary `cor:v29-density-orbit-stability` defines the tagged orbit distance by aligning the orientation tags. Equivariance then descends the estimate with the same constant. For a collection of contact laws the alignment is common to the whole collection.

For finite jets, the anchored projection `Ph=h-h(0)-u*h'(0)` commutes with reflection. The gap and quadratic geometry are invariant; odd graph and action coefficients change sign. The inherited finite smooth-jet factorization makes the lower-jet remainder independent of representatives and cutoffs, and reflection gives its degree-by-degree parity. Since the determinant-one last-jet block depends only on quadratic geometry, the finite inverse recursion is equivariant. The error remains

\[
 C_M(\tau^j+\varepsilon+\varepsilon_g)
\]

through any fixed order `M`, with the original density and gap error meanings. No order-uniform analytic-continuation stability is asserted. An arbitrary perturbed density is not declared to be the exact law of a globally glued analytic periodic table; global reconstruction remains a statement on the exact law image. This separates two domains of one argument without weakening the exact inverse or deleting the stable finite-jet extension.

### The referee's witness is retained and checked

Remark `rem:v29-fixed-anchor-witness` includes the positive density

\[
 f_\zeta(u,v)=\frac2\pi(1-u^2-v^2)_+
                   \{1+\zeta uv(u+v)\}.
\]

Its perturbation integrates to zero by simultaneous reversal. At `a=1/4` and `zeta=1/100`, the two incorrectly identified squared quantities are `107/22500` and `4/837`, whose difference is `-49/2092500`. The exact rational diagnostic independently recomputes these values. It also checks transported radicals, numerators, axis amplitudes, asymmetric exact-model recovery, and finite polynomial-jet parity. The witness is identified as an off-model formula obstruction, not as physical-table nonidentifiability. These finite checks support implementation accuracy; the proposition's proof supplies the continuum statement.

## Minor comment. Put the observation hierarchy on one stopped sample space

The new [observation hierarchy](article/01b_observation_hierarchy_v29.tex) starts with one full stopped acquisition history for a fixed parameter-independent policy with preparation cap `N`. It includes designs, within-preparation collision histories, failures, stopping time, and any recorded policy randomness. Countable unions of finite marked-array spaces and the finite products/unions under the cap give a common standard Borel space.

The one-preparation endpoint--time map is explicitly a building block, not a separate rung in an asserted inclusion of stopped sigma-fields. Deterministic maps now take the full stopped history to the endpoint--time transcript, the count--endpoint transcript, and the output record. Equation `eq:v29-stopped-hierarchy` states the actual pullback inclusions on that common space. Waiting-count encoding retains the terminal censored failure run and stopping information.

The retained designs are those generated by the original policy. Deleting a recorded time does not retrospectively change that policy, and an adaptive design can itself encode information about a deleted record. Consequently the information-scale descriptions retain the cited theorems' protocol hypotheses. The distinctions among physical cost, statistical coarsening, laboratory registration, and a law-valued common-orientation quotient remain in the text. No failed preparation is silently discarded.

## C2. Executed progress and the remaining full-main requirement

The complete unchanged native `two_collision.tex` has now been materialized with its Git-blob identity checked and compiled successfully with `latexmk` and `pdflatex -no-shell-escape`. The native PDF has seven pages. Its full reference/citation scan and final engine log have no unresolved references or citations, duplicate labels, missing glyphs, or overfull/underfull boxes. All seven pages were rendered and inspected. The retained `epstopdf` warning states that shell escape is disabled; no EPS conversion is used. The PDF SHA-256 is

`98dfd9a5a9792edce676d61e7f872c7f29a2e9d401bb37fa0cf6b06bac8b4748`.

The native companion source, engine versions, complete logs and checksums are identified in [VERIFICATION_V29.md](VERIFICATION_V29.md). This is genuine native-companion verification, not a reduced replacement for that entry.

For the main article, a ten-page selected-module fixture was executed. It includes the exact new sources and the inherited single-offset inverse. All new labels resolve; there are no overfull/underfull boxes or missing glyphs. Eighteen reference occurrences involving seventeen inherited labels outside that fixture remain explicitly unresolved. The fixture is not the full native main and is never used as a C2 certificate.

Both automatically triggered complete-native workflows ended before any step executed. Run `34679614994` at source `e468c075b0e57e015e774829f5886ce2322e6c02` and run `34680067058` at final mathematical source `78852f2ccf828385fd45063c1b58c0d474ddf6c5` each report `steps=[]`, `runner_id=0`, and an empty runner name. These observations do not establish a TeX failure or its infrastructure cause. No runner protection, membership, or repository permission was changed to bypass this condition.

**C2 is not closed.** A successful complete recursive audit and native build of `main.tex`, including the companion links, bibliography and every active appendix, with a pinned full PDF and layout review, remain outstanding. The repository contains a bounded full-checkout workflow and the existing complete-native audit/build utilities for that exact task. Their configuration is not represented as their successful execution. The locally materialized subset is likewise not represented as a full repository checkout.

## Earlier closed points, scope and significance

The observed-contact dichotomy and the finite-smooth-remainder proof accepted in the preceding review are preserved by Git object identity. V29 does not return to a claim of position singularity at a fixed observed contact, does not identify arbitrary smooth functions with convergent Taylor series, and does not infer a finite observation directly from a point evaluation of a continuous density.

The principal derivation remains the weighted half-line construction, signed single-offset action recovery, determinant-one finite contact-jet inverse, analytic intrinsic matching and lattice holonomy, followed by the separately specified statistical experiments and charged physical acquisition theorem. The direct physical-position benchmark remains active. The transported-anchor result is a necessary technical completion of stability, not a new priority or journal-significance claim.

The native main retains the complete inherited article and auxiliary material. Its input list changes only by two versioned substitutions and one added subsection. The earlier native entry and navigation are archived byte-for-byte. The mathematical text remains separate from this response and its execution record. This is an author revision for renewed independent assessment, not an editorial decision or a statement of acceptance by a journal.
