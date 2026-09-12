# Response to the A2 v26 referee report

**Manuscript:** Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards  
**Author:** Qian Qi  
**Revision:** v27, September 12, 2026  
**Branch:** `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`

The report addressed is `reviews/a2-v26-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`, committed at `a5b2d4b5a9ed31059e16e5011c8010579d713598`. It reviews manuscript commit `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`. The complete revised mathematical source was committed at `416124f13f182f8e2d876f93090865f13269c86b`. The stable native directory remains `papers/A2-v17-boundary-information-coarsening`; its historical directory name is not the article version.

We thank the referee for separating the valid single-offset inverse from the incorrect unrestricted auxiliary comparison. The revision preserves the two-type intrinsic inverse, all-order contact recursion, analytic gluing, rank-two metric recovery, global physical reconstruction, and the complete auxiliary compendium. It replaces the false unrestricted comparison by a sharp observed-type dichotomy and supplies a functional smooth-remainder proof for finite-jet factorization. These are changes to the active mathematical article, not qualifications confined to this response.

## R1. The observed contact type and matched records

### The defect in the previous statement

We agree that the previous proposition was false for an arbitrary even-flight design. An even bridge starting on the fixed facing obstacle has both retained endpoints on that fixed obstacle. A visit to the varying obstacle at an intermediate collision is not an observed endpoint. It cannot justify singularity of the endpoint-position experiment.

The opening of the revised comparison section now defines the records exactly. A successful scalar record is `(u,v)` and the matched position record is `(X_b,lambda(u),X_b,lambda(v))`. Residual time is integrated out in both. Intermediate positions and waiting counts are in neither. The fixed transverse projection is one parameter-independent kernel. A separate remark treats residual time retained in both records; no comparison silently changes that coordinate.

### A sharper positive theorem

In `article/18f_domination_and_position_comparison_v27.tex`, Proposition `prop:v27-observed-type-dichotomy` also retains the legacy label `prop:v26-position-deficiency`, so references in the article resolve to the corrected result.

For a compact nondegenerate interval of positive homotheties anchored at a fixed contact point, the proposition now states both cases. With the total-variation convention `sup_A |P(A)-Q(A)|`, for every finite `k >= 1`:

* When the even design starts on the varying obstacle, the scalar-to-position deficiency is exactly **one**, and the reverse deficiency is zero. The position family has pairwise disjoint full-probability first-endpoint events and no common sigma-finite dominating measure.
* When the even design starts on the fixed obstacle, the two matched experiments have Le Cam distance **zero**. Both maps are explicitly given: the fixed graph embedding and the transverse projection. The position family has a common dominating measure and a common positive-density region, and distinct members are not mutually singular.

Thus the correction does not merely insert a hypothesis in the old lower bound. It determines the exact deficiency in the intended case and proves the opposite behavior for the case the referee identified.

### Proof of the maximal deficiency

Lemma `lem:v27-dominated-disjoint` gives the measure-theoretic argument independently of the billiard example. If all input laws are dominated by a probability measure `nu`, then the output of any parameter-independent kernel is dominated by `K nu`. A probability measure charges at most countably many pairwise disjoint measurable sets. An uncountable family of disjoint full-probability output events therefore contains an event to which the proposed simulated output assigns probability zero. Its error is one. Taking the infimum over kernels leaves one.

The scalar laws are dominated by normalized Lebesgue measure on their common bounded endpoint box, also for every finite product. For the varying obstacle, strict convexity shows that two distinct positive homothetic boundaries meet only at the anchor. An arclength-density endpoint has no atom there. Removing the anchor produces the disjoint events required by the lemma. The reverse deficiency is zero by the fixed transverse projection. The argument uses no parameter-dependent reconstruction kernel and no integration over an uncountable parameter index.

### The fixed-obstacle witness remains in the article

The explicit two-disk family from the report is included in the revised section: a fixed unit disk centered at `(-1,0)` and a disk of radius `lambda` centered at `(1+lambda,0)`, homothetic about `(1,0)`. The gap is one. A two-flight word starting and ending on the first disk observes the fixed graph `X_0(u)=(-1+sqrt(1-u^2),u)`.

The proof is not based on a plot. Smooth dependence of the finite stationary action and positive flux gives the scalar density `Z_lambda^-1 A_lambda (d-E_2,lambda)_+`. Since the excess is zero at the origin, compactness gives a common square with `E_2,lambda < d/4`. The known fixed graph embedding pushes this positive-density core to a common position-support core. For matched residual-time records the same argument uses `d/4 < r < d/2` and the graph embedding times the identity.

The earlier nonsymmetric analytic oval is retained. It now illustrates both observed-type cases rather than claiming a conclusion for an unspecified design. No global cycle or spanning-tree structure is inferred from that local example.

### Propagation and unchanged inverse scope

The abstract and introduction state the observed-type distinction. The text emphasizes that the intrinsic global inverse still uses both contact types and the separately retained onset gap. Distribution-level injectivity, maximal finite-sample deficiency on an uncountable homothetic family, and uniform reconstruction of a compact analytic class are distinct assertions. The revised result makes no universal claim that every position record is support-singular or that one exact position determines an arbitrary analytic boundary.

## R2. Smooth Taylor remainders and finite-jet factorization

### Finite expansions replace a smooth power-series equality

The active signed-rigidity section is now `article/23a_signed_endpoint_rigidity_v27.tex`. The original v22 file is preserved unchanged. Equation `eq:v22-general-contact-jets` is a finite Taylor expansion for every prescribed `M`, with a remainder satisfying derivative bounds through `M+1` under a common `C^(M+1)` bound. It no longer identifies a general smooth graph with its infinite Taylor series.

The argument does not stop with polynomial jet-coordinate variations. New Lemma `lem:v27-smooth-jet-factorization` treats two arbitrary smooth anchored graph pairs with the same gap and equal jets through degree `M`.

### Functional envelope argument

Interpolate the two graph pairs linearly. On a common small contact interval, convexity, anchors, the quadratic half-line operator, and a weighted inverse bound persist. The stationary orbit satisfies `|x_i(u,t)| <= C |u| rho^i`, uniformly in the interpolation parameter. The graph difference is `O(|y|^(M+1))`.

At fixed endpoints the direct variation of a flight is

`partial_t ell = (h/ell) (Delta psi_r(y) + Delta psi_(1-r)(z))`,

with `0 < h/ell <= 1`. The proof differentiates a finite action truncation. Every interior orbit-variation term vanishes by stationarity; the fixed initial endpoint contributes none. The sole remaining terminal term tends to zero uniformly, as a product of two weighted decaying factors.

We integrate this exact finite identity in the interpolation parameter before taking the truncation limit. The direct variations have a summable majorant of the form `C_M |u|^(M+1) rho^((M+1)i)`. The resulting bound is

`|S_b^[1](u)-S_b^[0](u)| <= C_M |u|^(M+1)/(1-rho^(M+1))`.

Since the actions are `C^M`, their jets through order `M` agree. This establishes factorization through the finite graph jet for arbitrary smooth remainders, not just independence from formal coordinates above degree `M`.

### Uniformity and analyticity

The lemma explicitly requires uniform functional derivative bounds; it does not derive a uniform smooth remainder estimate from a bounded list of jet coefficients. For the stated undifferentiated remainder comparison, bounded `C^(M+2)` graph norms and positive geometric margins suffice. Additional differentiated estimates require the corresponding higher bounds.

After representative independence is established, polynomial graph representatives with smooth cutoffs define the finite-dimensional jet map. On compact positive finite-jet sets these representatives admit uniform finite smooth bounds. The existing determinant-one block calculation and quantitative tangent isomorphism therefore retain their conclusions, now with the missing representative-independence argument supplied.

A flat `epsilon exp(-1/y^2)` variation is included to mark the distinction precisely. Equal smooth graph jets imply equal finite action jets, not equality of the smooth graph functions or boundary images. Analyticity enters only at the later boundary-image continuation step. The smooth contact-jet theorem has not been restricted to analytic contacts.

All existing weighted Green estimates, nonlinear inverse bounds, truncation-envelope proof, homogeneous isolation, odd/even jet blocks, leading curvature inversion, and finite-flight error argument remain in the active section. Its 32 legacy labels are preserved; five labels are added.

## R3. Native integration, navigation, provenance, and build evidence

Both repository and paper entry pages now identify v27 and link this response, the active-source map, and executed verification records. Exact pre-v27 README blobs are copied to historical snapshots, so no historical navigation is discarded.

The full `main.tex` remains the native article entry point; `two_collision.tex` remains the companion. Only three active inputs are replaced: the introduction, the signed-rigidity section, and the position-comparison section. One additional subsection is inserted after the single-offset law inverse. All other 44 direct inputs retain their order. The auxiliary compendium and all its 36 direct inputs remain active. Neither a shortened article nor a typesetting fixture replaces a native entry point.

The complete revised mathematical source is pinned by commit `416124f13f182f8e2d876f93090865f13269c86b` and tree `da8779b9c2a7352486931a64252752f3c6eae0b5`. New verification tools and records do not alter those mathematical source bytes. `ACTIVE_SOURCE_MANIFEST_V27.md` distinguishes this source map from an executed recursive graph audit.

The native workflow requests a complete source archive, ordinary and optimized diagnostics, a recursive label/reference/citation audit of both native closures, both full native builds through the retained `tools/build_submission.py`, engine versions, logs, page metadata and hashes. Missing inputs are fatal in the recursive scanner. It does not replace the manuscript by selected sections.

**The requested successful whole-native-build evidence is not yet available.** The first v27 run, `34674173652`, at the mathematical source commit failed with job `103500916466` reporting `steps=[]` and `runner_id=0`. Thus neither checkout nor a TeX command executed. This is not a successful build and is not evidence of a manuscript compilation error. Subsequent observed run evidence, when present, is recorded in `VERIFICATION_V27.md`; a workflow file or queued run is never counted as execution.

The local checks comprise 884 finite mathematical diagnostic cases, with byte-identical ordinary/optimized output and a verified Git blob for the executed script. The changed-source audit checks only the fetched old/new modules and the direct main input list. A separate 16-page revised-module typesetting fixture ran three passes with zero overfull boxes, missing-glyph messages, or duplicate-label messages. It deliberately leaves inherited references and citations unresolved and is **not** a successful native manuscript build or full reference verification. The fixture uses no invented placeholder theorem labels.

Accordingly, R3's navigation, source pinning and reproducibility machinery are delivered, but its full native execution requirement is not represented as closed. The mathematical revisions are submitted for re-review with that evidence boundary visible.

## Additional clarification: one density versus one support

The optional functional support comparison is now proved in `article/23g_density_support_distinction_v27.tex`. At `d=1`, the strictly convex actions `S(u)=u^2` and `phi_epsilon(S(u))`, with `phi_epsilon(s)=s+epsilon s(1-s)(s-1/2)`, have the same endpoint support for `0 < epsilon <= 1/10`, but different four-density invariants. Monotonicity, the reflection identity `phi(1-s)=1-phi(s)`, and a strictly positive second-derivative bound are shown explicitly.

This is labeled a comparison in the functional action-density class, not an assertion that both toy actions arise from physical tables satisfying the global hypotheses. The physical single-offset inverse remains based on the established relative law. No new flagship theorem is demanded from the support example, and no existing global conclusion is replaced by it.

## Historical derivations and scope of verification

The revision relies on the historical weighted inverse, envelope and last-jet block in v22; the v26 amplitude-free inverse and its finite-flight stability; the v23-v25 analytic continuation, intrinsic gluing and observable acquisition chain retained in the active entry point; and the original build utility and auxiliary compendium. The earlier smooth count-envelope section concerns a different observation model and is not used as a substitute for the new graph-remainder proof. The bibliography and existing comparisons with marked/enriched length rigidity remain intact; no unsupported inclusion of those data maps is added.

The report and this response are author-requested referee-style research records, not journal editorial decisions. Finite diagnostics, source consistency, typesetting, and mathematical validity are reported separately. No journal acceptance or proof-assistant certification is asserted.
