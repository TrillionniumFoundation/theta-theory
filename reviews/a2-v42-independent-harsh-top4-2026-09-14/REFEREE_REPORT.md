# Independent referee-style report on A2 revision 42

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 14, 2026  
**Requested standard:** a leading general mathematics journal at the level of the four journals specified by the author. This is an author-requested, AI-assisted independent assessment, not a commissioned journal report or an editorial decision.

| Reviewed object | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Author branch | `revision/a2-v42-native-source-referee-response-2026-09-14` |
| Submission commit | `6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad` |
| Submission tree | `fb689bc8487a1d6b9522dc5270282edd7bee8691` |
| Previous submission | A2 v41, `c730a60bbc8af2a4c6e432813c31dccc897828e7` |
| Addressed previous report | `e162532115071265cf73b97a5069f33628347cfe` |
| Native entry | `papers/A2-v17-boundary-information-coarsening/main.tex` |

Source identifiers S01–S21 and literature identifiers L1–L4 refer to the immutable links and explicit coverage in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). The historical directory name `A2-v17` does not identify the current version. This report reviews the actual v42 manuscript commit, not the other v42-named branch that still points to the v41 report.

## Recommendation

**MAJOR REVISION. I do not recommend acceptance of this snapshot. The complete-native-delivery hold C2 remains open.** The current source makes real repairs: it corrects the stale current-version navigation and supplies a detailed common-frame uniqueness argument in the single-offset global theorem. These repairs should be credited, not reopened by repeating the previous report mechanically. [S01–S04]

Within the fresh examination described below, **I have not established a new fatal mathematical counterexample**. In particular, the relative determinant argument, smooth finite-jet factorization, fixed-anchor density inverse, rerooting mechanism, finite-signature matching, compact-local Gaussian upgrade, and two-sided Poisson kernels withstand the checks reported here. That is a bounded finding, not certification of the complete recursive manuscript, all auxiliary applications, or the entire physical-transfer chain.

The latest mathematical source has its own failed hosted run, distinct from the earlier infrastructure run described by the author. That latest-head run executed no job steps and supplied no artifacts. There is therefore no basis for closing C2 by treating the new source as a delivered, compiled and visually inspected article. Equally, those metadata do not show a TeX error and do not justify inventing one. [S05]

| Issue | Disposition in this review |
|---|---|
| C2: complete source-matched main and companion delivery | **Open; major delivery hold.** Fresh exact-head evidence is recorded below. |
| R39-I1: stale current navigation and missing current response/evidence entry | **Resolved.** Both current entries identify v42 and link the response and ledger. |
| Common anchoring frame, tree root and global uniqueness | **Resolved at the inspected composition step.** The detailed v42 proof now implements the existing rerooting argument. |
| Florio–Leguil version-sensitive comparison | **Corrected statement retained and independently checked.** |
| Newly examined mathematical arguments | No new fatal defect established; positive findings are limited to the stated coverage. |
| Exceptional significance for the requested journal level | **Not established by this assessment.** This is an editorial reservation, not a mathematical impossibility claim. |

## 1. Revision identity and response to the previous report

The v41-to-v42 comparison contains three commits and sixteen changed paths. Five paths belong to the inherited v41 review package. The author-side changes comprise a workflow, updated navigation, a new response and verification ledger, preservation records, the native entry, and the new single-offset chapter. The underlying statistical chapters and the principal half-line analysis are not replaced in this delta. [S01–S04]

The new chapter retains the density inverse and extends the detailed proof of `thm:v26-single-offset-global`. The author reports a byte-identical comparison of theorem, proposition and corollary statements with its predecessor. I have inspected the current statements and proof; I do not present that author-side programmatic comparison as an independently rerun test. The mathematical change is principally integration of an existing argument, not a newly claimed stronger observation theorem. That is an appropriate response to a composition or exposition issue.

Both the root README and the manuscript README now identify v42, the actual author branch, the immediately preceding v41 report, and one current response/evidence entry. The earlier README bytes are preserved in a historical directory. Thus the specific stale-v38 navigation objection is closed. The fact that the evidence ledger honestly records an open delivery item is not another navigation failure. [S01–S03]

## 2. Relative nonlinear bridge asymptotics

The forward statement concerns a normalized mixed endpoint derivative. Its denominator is exponentially small in the flight number. Consequently an absolute error estimate for the stationary action would not establish the claimed law. The inspected proof uses the necessary relative mechanism. [S06]

At quadratic order the half-line interior Hessian has diagonal entries $2c_{(b+i)\bmod2}/g$ and adjacent entries $-1/g$. With the manuscript's parity factors, its inverse is

$$
G^{(b)}_{ik}=\frac{g\sigma_i^{(b)}\sigma_k^{(b)}}{2c\sinh\gamma}
\left(e^{-\gamma|i-k|}-e^{-\gamma(i+k)}\right).
$$

Splitting the weighted sum at $k=i$ gives the two convergent geometric ratios $e^{-\gamma_-}/\rho$ and $\rho e^{-\gamma_-}$, where $e^{-\gamma_-}<\rho<1$. This supplies the local nonlinear contraction. At each prescribed finite differentiated order, the same invertible linearized operator multiplies the highest orbit derivative. The claim requires the corresponding boundary norms; it is not a uniform theorem over all derivative orders with fixed constants.

Locality and exponential endpoint decay make the sum of the absolute Hessian-perturbation entries finite, independently of bridge length. This is what permits trace-norm control. For the finite bridge, the sum of the two half-lines has an interior residual of order $j\rho^j$ in the sum norm. Symmetry of the uniformly diagonally dominant Hessian transfers the maximum-norm inverse estimate to the sum norm. The resulting orbit correction remains exponentially small after every fixed number of differentiations.

For the determinant comparison the proof retains the first and last $\lfloor j/3\rfloor$ sites. It estimates the discarded perturbation in trace norm, the remote Green reflections, and the off-diagonal interaction between the retained blocks. The inequality

$$
|\operatorname{tr}(T^m-(T')^m)|\le m q^{m-1}\|T-T'\|_1,
\qquad \|T\|,\|T'\|\le q<1,
$$

then controls the logarithmic determinant before exponentiation. This is not an uncontrolled division by the reference twist. I found no dimension-dependent error disguised as a uniform relative estimate in this inspected argument.

The subsequent moving-sublevel calculation uses constructive Morse maps to a common disk. The inverse maps and transformed amplitudes are compared in fixed smooth norms; odd Taylor terms integrate to zero, and finite additional endpoint derivatives control offset derivatives at zero. This supplies an actual mechanism for the asserted smooth right extension, rather than formal differentiation of a moving indicator. The preceding global itinerary localization and full-phase normalization remain dependencies: their complete proofs were not reconstructed anew in this review. [S06, S18]

## 3. Single-offset inversion and the smooth contact-jet recursion

### 3.1 The density inverse has the correct datum and topology

On an interior square the law has density

$$f(u,v)=Z^{-1}B(u)B(v)\{d-S(u)-S(v)\}.$$

The four-density ratio satisfies

$$
R(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},\qquad
1-R(u,v)=t(u)t(v),\qquad t(u)=\frac{S(u)}{d-S(u)}.
$$

At a fixed nonzero anchor $a$, strict convexity gives $t(a)>0$. Therefore

$$t(u)=\frac{1-R(u,a)}{\sqrt{1-R(a,a)}},\qquad S(u)=\frac{dt(u)}{1+t(u)}.$$

The amplitude also follows up to its normalization. The algebra is valid for a non-even action and an unknown nonconstant amplitude. The square root is taken at one nondegenerate scalar anchor; the proof does not differentiate a degenerate pointwise square root at $u=0$. [S07]

A law in the declared smooth class determines its continuous density on the interior. This justifies the slice identities at the level of exact laws. It does not turn a density value into an individual sample observation. The stability theorem correctly uses an interior $C^M$ norm, positive density denominators and a positive anchor bound. It does not assert that small total variation controls arbitrarily high derivatives.

The finite-flight corollary controls the normalizing integral on the whole common box with $|x_+-y_+|\le |x-y|$, then differentiates only on an interior square where the cutoff is positive. Its subtraction of estimated constant and linear action terms before applying the anchored jet inverse is appropriate. These are genuine safeguards, not dispensable notation. Our rational tests below directly retain odd terms and unknown amplitudes.

### 3.2 The envelope limit, rather than the determinant, proves the filtration

The critical issue is whether the order-$n$ action jet can depend on higher graph derivatives exposed by differentiating the stationarity equation. The inspected proof does not infer the answer from a formal Taylor expansion. It first differentiates finite action truncations: interior orbit variations cancel, while the remaining terminal variation tends to zero with a summable exponentially decaying bound. [S08]

For two actual smooth graph pairs with identical jets through order $M$, interpolate the graphs on a common contact interval. This is a local interpolation, not an assertion that an arbitrary path of local graphs is realized by global periodic tables. At fixed flight endpoints,

$$
\partial_t\ell_{r,t}(y,z)=\frac{h_{r,t}(y,z)}{\ell_{r,t}(y,z)}
\{\Delta\psi_r(y)+\Delta\psi_{1-r}(z)\}.
$$

Equal finite jets give $\Delta\psi_r(y)=O(|y|^{M+1})$. Weighted orbit decay supplies a summable majorant $C|u|^{M+1}\rho^{(M+1)i}$. Integrating the exact finite envelope identity in $t$ and then taking the truncation limit yields

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

Thus finite action jets factor through finite graph jets, even for smooth remainders and flat variations. The functional smoothness bounds are explicitly required. A bounded finite coefficient list is not substituted for them.

At the first occurrence of an order-$n$ graph jet, only the linear half-line orbit contributes. The initial endpoint appears once and each interior site twice. The two sums are

$$
1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),\qquad
2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
$$

Together with $\mathfrak r_0\mathfrak r_1=1$, these produce the stated determinant-one block. The leading curvature inverse and the proved block-lower-triangular dependence then justify the fixed-order tangent isomorphism. Determinant one alone would not justify a bound on an unrestricted infinite-jet inverse, and the current text does not make that stronger assertion. Exact boundary-image determination uses analyticity only after this smooth finite-jet argument.

## 4. Common-frame periodic uniqueness and finite-signature stability

### 4.1 The v42 composition addresses the actual root issue

Coincident complete oriented curvature signatures on a connected analytic boundary are exactly the orbits of its orientation-preserving Euclidean symmetry group. The proof uses analytic continuation of the arclength curvature function followed by uniqueness of the planar Frenet system. A unique signature at one framed point therefore forces the proper symmetry group to be trivial, and consequently makes the signatures unique at every framed point. [S09]

The rerooting lemma then has a simple but valid combinatorial content. Only edges on the path from the old root to the new root reverse. Every intermediate new parent was already an old parent and has unique signatures everywhere. The terminal new parent has that property by hypothesis. Off-path edges retain their orientation. The anchoring cycle supplies the hypothesis at the desired new root. This does not permit arbitrary rerooting at a symmetric leaf. [S10]

The detailed v42 global proof now uses this fact in one gauge. It fixes the common anchoring frame, roots the supplied tree at an incident obstacle with the required unique signature, recovers both translation holonomies, sets

$$L=VM^{-1},\qquad L^TL=M^{-T}V^TVM^{-1},$$

and places the remaining obstacle orbits by induction along the rerooted tree. To prove uniqueness, it aligns the starting frames of two admissible realizations, identifies their holonomies and lattice, and then identifies each successive child placement. The deck corrections are interpreted through that same lattice matrix. [S07, S11]

This is the missing detailed composition, not merely the matrix identity. The realizability hypothesis supplies existence, geometric admissibility and consistency with unused edges. The argument neither solves an unmarked inverse problem nor places obstacles outside the stipulated spanning structure. No additional inter-channel registration hypothesis is required by the inspected repair. I regard this composition issue as resolved. An explicit cross-reference to the rerooting lemma in the older abbreviated v24 proof would improve local readability, but the complete manuscript now supplies the needed argument; this is not a new fatal gap.

### 4.2 Noisy finite matching is not inferred from an outside-arc gap

The finite-signature chapter contains a separate proof of local embedding. A transition obstacle cannot have constant analytic curvature or a nontrivial proper symmetry. At each point some positive-order curvature derivative is nonzero. Compactness selects a finite signature order with uniformly nonvanishing derivative. A uniform second-derivative bound gives a local secant lower bound. A second compactness argument over pairs outside that arc selects finitely many additional coordinates and a positive global separation. [S12]

For a recovered signature curve close in $C^2$ and a nearby target, the squared-distance objective has

$$f''(x)=|\widetilde J'(x)|^2+(\widetilde J(x)-y)\cdot\widetilde J''(x).$$

The local derivative bound makes this uniformly positive on a sufficiently small arc, while the outside separation excludes other minimizers. The resulting unique nearest point is locally Lipschitz under the stated perturbations. This properly excludes the false inference that mere $C^0$ proximity or an outside-arc gap alone guarantees a unique local match.

The later compact inverse modulus is a distinct non-effective continuity result. It does not assert well-conditioned analytic continuation from arbitrary noisy Taylor coefficients. Similarly, the lattice perturbation estimate multiplies by the fixed marked matrix $M^{-1}$ rather than inverting a noisy holonomy matrix. These distinctions are mathematically important and are respected in the examined source.

## 5. Fresh scrutiny of the local statistical experiments

### 5.1 Moving support and compact Gaussian comparison

The original family $f_\theta=a_\theta(w_\theta)_+$ can have support-exclusive observations, so its likelihood relative to the reference member need not exist everywhere. The source explicitly separates that mass and constructs a common-collar representative before using reference likelihoods. At

$$np_n\delta_n^2\log(1/\delta_n)\to1,\qquad
q_n=\delta_n[\log(1/\delta_n)]^{1/4},$$

the removed product mass is $O(np_nq_n^2)=o(1)$. Both censoring and reverse reconstruction use reference quantities, not the unknown local parameter. The singular second, third and fourth score-moment estimates have the respective orders $\log(1/q_n)$, $q_n^{-1}$ and $q_n^{-2}$. These give the displayed LAN remainder and triangular-array central limit estimates on the representative. [S13]

Compact-parameter Le Cam convergence is then treated as a separate question. The finite-net lemma uses one kernel for a fixed finite net and bounds its error elsewhere by the prelimit and limit total-variation moduli. It does not supply the unknown parameter to a nearest-net-point kernel. The moving-boundary estimate yields a product modulus bounded by a constant times

$$s\sqrt{1+\log(1/s)},\qquad s=\|h-h'\|,$$

which tends to zero. Gaussian continuity on the identifiable subspace supplies the other modulus, including singular information. This is a legitimate finite-to-compact upgrade, conditional on the cited finite-experiment convergence. [S14]

My fresh check here covers the common-collar and LAN argument and the complete compact-net argument. It does not reprove every likelihood-disintegration, contiguity, alternative moment, quadratic-loss, count–endpoint or anchored physical-realization result elsewhere in the article. The previous report's favorable examination of some of those dependencies remains historical evidence, not a newly executed certification by this report. [S04]

### 5.2 The Poisson comparison includes the reverse direction and the corner

The moving-ceiling chapter imposes not only convergence of the ceiling and trace but also a separate $O(k^{-1})$ relative-density perturbation on the common bulk. This additional hypothesis is used in the proof and is explicitly connected there to the anchored application. Trace convergence alone would not control the bulk product experiment. [S15]

The reference layer $|k(w-r)|\le R$ is parameter independent. Its probability is $O(k^{-1})$. Near the intersection with the fixed face $r=0$, the endpoint strip has volume $O(k^{-1})$ and the relevant residual interval has length $O(k^{-1})$. Hence its one-record mass is $O(k^{-2})$ and its scaled intensity error is $O(k^{-1})$. Outside that strip, fiber integration controls the shifted ceiling. The conditional bulk normalizers preserve a relative error of order $k^{-1}$, giving squared Hellinger error $O(k^{-2})$ per bulk record.

The forward kernel extracts the layer point process. The reverse kernel maps its points back to physical residual time, fills the remaining records with the reference bulk law and randomly interleaves the sample. The source defines the kernel also on negative-residual corner exceptions and Poisson counts larger than $k$. The accumulated bulk replacement costs $O(k^{-1/2})$ in total variation. This establishes the claimed two-sided comparison under the stated hypotheses, not merely weak convergence of an extracted point process. The independent diagnostics below test this geometry and the necessity of the bulk assumption; they do not prove the full physical application.

## 6. Independently executed diagnostics

The accompanying [script](independent_checks.py), [full results](RESULTS.json) and [execution output](EXECUTION.txt) belong to this review. They are not the v41 tests copied under a new version. The script has no network access and does not invoke the manuscript's implementation. All assertions passed in the recorded environment. [S20]

| Diagnostic | Actual result | Scope |
|---|---|---|
| Exact rational four-density cancellation | 625 pair identities; 75 action/amplitude recoveries at three anchors | A non-even polynomial action and unknown nonconstant amplitude |
| Exhaustive finite-tree rerooting | 1,442 labelled trees on one through six vertices; 229,133 admissible reroot cases | Combinatorial consequence after analytic signature uniqueness |
| Quadratic half-line Green recurrence | Six configurations, 80 sites; maximum tested residual $4.45\times10^{-16}$ | Interior recurrence; the last finite row's omitted infinite tail is explicitly excluded |
| Nonlinear finite smooth-remainder test | 48 stationary solves, 80 edges; maximum stationarity residual $1.12\times10^{-16}$ | Fifth-degree perturbation preserving graph jets through degree four |
| Fifth-order coefficient isolation | Maximum finest-endpoint coefficient error $6.82\times10^{-7}$ | Asymmetric curvatures, both starting and varied contact types |
| Poisson layer and bulk budgets | Nine $(z,k)$ cases satisfy the asserted diagnostic bounds | Exactly normalized parabolic ceiling and a separate normalized bulk-tilt test |

Two negative controls are important. Rerooting at a symmetric leaf, outside the lemma's hypothesis, is detected as invalid. A bulk perturbation tending to zero only at order $k^{-1/4}$ has product squared Hellinger distance tending towards its maximal value, despite vanishing one-record perturbation. The latter deliberately violates the manuscript's stated $O(k^{-1})$ bulk assumption. Neither is a counterexample to the actual theorem; both guard against stronger, incorrect readings.

The nonlinear calculation solves finite Euclidean flight-length stationarity equations, not merely the displayed two-by-two block. Nevertheless, finite truncations at finitely many endpoints cannot establish infinite-dimensional differentiability, arbitrary smooth-remainder estimates, or uniformity over a geometric class. Diagnostic counts must not be used as a substitute for those proofs.

## 7. Literature and the general-journal significance threshold

The version-sensitive comparison is correct in the inspected current introduction. Florio–Leguil v5 explicitly removes the earlier open-billiard spectral-rigidity assertion after an error in Proposition 3.1, while retaining the smooth-conjugacy conclusion. The manuscript uses the latter, not the removed geometric rigidity assertion. I independently checked the primary version notice and abstract. [S16; L1]

De Simoi–Kaloshin–Leguil treat marked-length determination for analytic open billiards under symmetry and genericity hypotheses. Finamore–Leguil's stated finite-horizon Sinai result uses an enriched marked length spectrum. These are not the same observation map as two signed channel laws with onsets and marked incidence data. The current article correctly refrains from asserting an unproved reduction between those data. This bounded literature check establishes neither a priority refutation nor an automatic superiority claim. [S16; L2–L3]

Meister–Reiß already prove a nonregular-regression equivalence to Poisson experiments whose intensity supports encode the target boundary. Thus a Gaussian/Poisson contrast, by itself, is not a new general principle. The billiard-specific nonlinear laws and the kernels between the declared retained records must carry the additional contribution. The work is cited in the manuscript; no concealed-precedence allegation is made. [S16; L4]

My evaluation remains severe. The most credible contribution is the composition of the relative nonlinear bridge law with the all-order inverse from genuinely coarsened transverse laws. The amplitude cancellation, compact-injection argument and final lattice matrix equation are not individually persuasive reasons for placement in a highest-level general mathematics journal. The richer physical position experiment also admits the direct geometric-sampling benchmark acknowledged in the introduction; merely restricting its flights to be long does not make that consistency theorem a uniquely difficult inverse result. [S16]

The revised exposition recognizes these distinctions, which is an improvement. It does not settle the separate editorial question of whether the central mechanism and its consequences have exceptional breadth and depth. I do not recommend inventing a stronger theorem, changing the observation space, or deleting essential proofs to manufacture that impression. The next submission should make the existing contribution assessable as a complete article, with its precise hypotheses, classical inputs and substantive advances visible independently of the author-requested review history. Successful compilation would be necessary delivery evidence here, not a sufficient reason for acceptance.

## 8. Outstanding requirements and final disposition

### R42-D1 / inherited C2 — complete native delivery remains open

For the exact mathematical commit reviewed here, the authenticated Actions query returns run **34799807519**, whose head is **6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad**. Job **103840001543** has `steps: []`, runner identifier zero, no runner name and conclusion `failure`. The artifacts endpoint returns zero artifacts. This is fresh evidence about the actual new manuscript, not the infrastructure-parent attempt recorded in the author's initial checkpoint. [S05]

No TeX command, raw compiler log, complete-main PDF, companion product or visual-inspection result is established by this run. The cause of the pre-step failure is not established by those metadata. This report also does not claim a successful local native build: the attempted repository clone in the review environment failed at DNS resolution, and no complete local checkout was obtained. Connector source reads and independent mathematical diagnostics did succeed. These are different operations with different evidentiary scope. [S19–S20]

Closure requires a durable, retrievable package for the complete native main and companion, pinned to the source actually built. It should identify the recursive inputs, the actual commands and tool versions, exit status, raw logs and recorders, generated companion-auxiliary producer/consumer provenance where used, resulting PDF identities, and rendered-page inspection coverage. Correct unresolved references, missing material or obstructive typesetting defects if the actual build reveals them. None of those defects is alleged without an inspected product. A release or artifact archive is acceptable; binaries need not all be committed to Git. A miniature integration fixture, a companion alone, an earlier mathematical source, or a configured workflow does not close this requirement.

### R42-E1 — append the latest-head evidence without relabelling the checkpoint

The current author ledger is explicitly a source-revision checkpoint and honestly leaves C2 open. It records the earlier run at `4d78f5d...`, whose mathematical source was still inherited v41. Preserve that record and append the exact-head run and any subsequent actual products with their own source identities. This is a traceability update, not an allegation that the current ledger falsely claims success. The repaired current navigation should remain closed rather than being needlessly reworked. [S03, S05]

### Conditions for further consideration

Retain the now-explicit common-frame proof, the finite smooth-remainder argument, the actual observation-space distinctions, and the compact-experiment and reverse-kernel proofs. Supply the complete source-matched article and make every invoked dependency accessible within the declared submission. Further examination must still address any newly observed proof or presentation defects in that complete product; this report makes no promise of acceptance after delivery. The whole-paper significance judgment remains separate from the bounded positive mathematical findings.

**Final recommendation: major revision, with no acceptance recommendation and C2 explicitly open.** The revision is a genuine improvement, not a failure of its entire mathematical programme. Conversely, a valid repaired composition and passed finite checks do not amount to a complete correctness certificate or a top-four-journal acceptance case. No manuscript deletion, programme abandonment, additional registration hypothesis, or arbitrary contraction of the stated scope is requested.
