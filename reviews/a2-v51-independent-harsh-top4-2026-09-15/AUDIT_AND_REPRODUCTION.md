# A2 v51: audit, source map, and reproduction

This file supports [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes source integrity, finite diagnostics, mathematical reading, and editorial judgment. None is a substitute for the others. All dates below are September 15, 2026 unless explicitly specified.

## Frozen objects

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Reviewed delivery | `revision/a2-v51-review-ready-2026-09-15` |
| Reviewed delivery head / review-branch base | `ffd53f26383874dc798af9a54ae877ffdd0f81eb` |
| Actual compiled source | `b9201bc272bc7ecbab1ad6a91fc844216685fadd` |
| Source repository root tree | `0605929fe0e40525f49505159e364d73a5d56b01` |
| Source `papers` tree | `10cf44ca1f34097374281d54861a27bea71b61d9` |
| Manuscript subtree | `91989fa41b2714d28a8f93738c992f0c7d89ad2e` |
| Manuscript path | `papers/A2-v17-boundary-information-coarsening` |
| Workflow preparation commit, not compiled source | `f31b5626f1d744e316674d5a09834a8f88329aee` |
| Native workflow run / attempt | `34913487658` / `1` |
| Native artifact ID | `10375761503` |
| Artifact name | `a2-v51-native-b9201bc272bc7ecbab1ad6a91fc844216685fadd-1` |
| Native artifact archive size | `4382838` bytes |
| Artifact SHA-256 | `e8dfb22f5f23d2d617e61dd97cf8e9a38bfec6b81c100cfee488d48bc0779f92` |
| Previous report head | `4b22b793cc2c05d3f48efb9a98dfd46cab003e5c` |
| Previous actual v50 source | `49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4` |

The source commit and both containing Git trees were read through the authorized GitHub connection, independently of the archive manifest. The reconstructed manuscript tree matches the child entry in the connected `papers` tree. The archive was downloaded through the authorized artifact action. Its digest matches the GitHub workflow artifact metadata. The workflow preparation SHA in that metadata is not silently substituted for the materialized source SHA.

The branch inventory identified v51 as the latest materialized A2 revision; the `revision/a2-v5` prefix was checked again before depositing this review, with v50 and v51 but no v52 entry returned. The review is pinned to the objects above, not to a promise that the repository cannot change later.

[Reviewed delivery](https://github.com/TrillionniumFoundation/theta-theory/tree/ffd53f26383874dc798af9a54ae877ffdd0f81eb) · [Actual source](https://github.com/TrillionniumFoundation/theta-theory/tree/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening) · [Native workflow](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34913487658)

## Source map and actual coverage

Paths in this table are relative to the manuscript directory at the compiled source SHA above. Line numbers refer to that frozen text; printed page numbers refer to the native v51 main PDF. The report's source labels refer to this table, not to an unpublished private assessment.

| ID | Source and locations | Coverage in this round |
|---|---|---|
| S01 | `article/00_structural_introduction_v48.tex`; `article/00b_interaction_overview_v51.tex` (53 lines). Theorems A/B, pp. 4–5. | Structural statements, observation conventions, proof route, and scope distinctions read. |
| S02 | [`article/23p_uncentered_interaction_v51.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23p_uncentered_interaction_v51.tex), lines 1–381, pp. 55–60. | Entire new module read. Origins: 13–101; action invariant: 103–171; local regularity: 173–267; geometric/differential interface: 269–356; other observation models: 358–381. |
| S03 | [`v4/10_boundary_layers.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex), lines 1–386. Theorem 7.2, p. 18; Theorem 7.3, p. 20. | Half-line construction, relative normalization, gluing, trace-norm comparison, and fixed-offset integration examined. Not a new audit of every upstream geometric lemma. |
| S04 | [`article/23a_signed_endpoint_rigidity_v27.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex), lines 1–598. In particular 132–470 and 471–598; Lemma 12.4, p. 45. | Weighted inverse, finite envelope, actual smooth remainder, homogeneous degree isolation, last-jet block and finite recursion examined. |
| S05 | [`article/23f_single_offset_law_inverse_v42.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v42.tex), 270 lines. Theorem 13.1 and Proposition 13.2, p. 49. | Scalar-anchor identity, interior stability and finite-flight/finite-jet interface examined; used as the precise old-algebra comparison. |
| S06 | `article/23c_analytic_continuation_v23.tex`, lines 1–44. | Registered analytic-germ globalization read: curvature identity, equal total turning, and Frenet uniqueness. No stable inverse of unrestricted analytic continuation inferred. |
| S07 | [`article/23n_finite_symmetry_v49.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23n_finite_symmetry_v49.tex), 243 lines. Lemmas 20.1–20.2, p. 85; Theorem 20.3, p. 86. | Finite symmetry, actual local angular lift, two directions of finite-fiber reconstruction, lattice checks, and stated circular comparison read. |
| S08 | [`article/23m_differential_rigidity_v48.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23m_differential_rigidity_v48.tex), 505 lines. Lemma 21.1, p. 90; Lemma 21.3, p. 93; Theorems 21.5–21.6, pp. 94–95. | Moving-reference derivative, cap normalizer, scalar-anchor and recursion derivatives, analytic variation, registration/cochain, and finite-dimensional coordinate selection interfaces examined. |
| S09 | `article/23g_density_support_distinction_v27.tex`, lines 1–54. | The explicitly functional support-preserving action example read. It is not silently promoted to a realized billiard example. |
| S10 | [`article/23l_calibrated_histograms_v47.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/b9201bc272bc7ecbab1ad6a91fc844216685fadd/papers/A2-v17-boundary-information-coarsening/article/23l_calibrated_histograms_v47.tex), 305 lines. Lemmas 39.7–39.8, p. 157; Theorem 39.9, p. 158; Corollary 39.10, p. 159. | Offset and hard-cell bounds, pilot-aware confidence proof and the stated acquisition premises inspected. Upstream pilot construction, full quantized inverse, and all statistical experiments not independently re-proved. |
| S11 | `RESPONSE_TO_REFEREE_V51.md`, `HISTORICAL_DERIVATION_AUDIT_V51.md`, `LITERATURE_CHECK_V51.md`, delivery `REVIEW_READY_V51.md`; the previous report linked below. | Response and preservation claims checked against the new source and diagnostic output. Branch inventory is not an independent rereading of every historical report. |
| S12 | `article/23o_two_branch_example_v50.tex`; prior report's C4/C5. | Source preservation checked; the complete infinite-lattice geometry of these unchanged examples was not independently repeated in this round. |

[Previous v50 report](https://github.com/TrillionniumFoundation/theta-theory/blob/4b22b793cc2c05d3f48efb9a98dfd46cab003e5c/reviews/a2-v50-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md).

The complete companion was included in source verification, compilation, text comparison and pixel comparison. Its mathematical assertions were not independently re-proved in this round. Unexamined statements are neither certified nor alleged false.

## D1. Independent delivery reproduction

### Source and preservation verification

The extracted archive contains 582 frozen source files. Each was checked against `frozen-source-manifest.json` for byte length, SHA-256, and the Git blob hash `SHA1("blob " + decimal_length + NUL + bytes)`. Directory trees were then reconstructed using recorded file modes, recursive tree hashes and Git's directory-aware byte ordering. The resulting tree is the independently connected manuscript subtree above.

The active manifest has 108 main inputs and one companion input: all 109 match. All 34 native evidence files listed in the build report match their lengths and SHA-256 hashes.

The archived v50 active manifest has 106 main inputs and one companion input. Of the main inputs, 103 remain byte-identical in place. The original versions of the three amended main inputs (`main.tex`, `article/00_structural_introduction_v48.tex`, `v5/references_v43.tex`) match the exact archive. The companion input is unchanged. Thus 104 of the total old 107 inputs are unchanged in place; the remaining three have verified exact originals. These counts must not be confused with 582 total frozen files or 109 current active inputs.

The rerun author diagnostic separately checks all 522 inherited theorem-style/proof blocks, 245 proof environments, relative input order, labels and references. It finds five new proofs, one new lemma, one new proposition, two new numbered theorems and Theorem B. These are operational preservation checks, not theorem verification.

### Complete clean builds and product comparison

The frozen sources were copied to a fresh build directory. Both complete entries were built successfully with the following commands, companion first:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

No stubs or omitted-input manuscript was used. Both exit codes were zero. The native main has 269 pages and the native companion seven. Every rebuilt page matches the corresponding native page in extracted text and in 72-dpi RGB pixel arrays under the same PyMuPDF renderer. There are no mismatching page numbers in either comparison. Byte-identical PDFs are **not** claimed.

| Product | Native SHA-256 | Rebuilt SHA-256 |
|---|---|---|
| `main.pdf`, 2,003,720 native bytes | `87cc42d87aa35cdcde4542d7df02d106b7b5aaad61bffb75a9f35db69e778196` | `0de97a8f4a4352dabaf89b96263d01a2a6ffa4e3cba8b70bf90bf5a2d7ea79bf` |
| `two_collision.pdf`, 333,367 native bytes | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` | `b2325314c251a342edc55116756fd8e488902b8ff55e23fb6234f1036fd9e7df` |
| `native-source.zip` | `338b2008b7bd0bc3622e200ab8b44f9b99a35c85f9fa746f8d09f766894437e6` | Not a regenerated archive |

The local main final log has three underfull vboxes. The scan found no overfull box or undefined reference/citation. Disabled shell escape also gives the expected package warning; the machine field named `warnings` in the evidence is a specified line-pattern scan, not a claim to enumerate every wrapped package warning. The log and build-output hashes are retained in `EVIDENCE.json`.

Direct visual inspection covered native main pages **4, 5, 56, 57, 58 and 59**, and companion pages **1 and 7**. Page 57 was opened individually; the other listed pages were inspected on labelled sheets of native 90-dpi renders. This bounded visual coverage is different from the automatic all-page pixel comparison. No claim of individual visual inspection or proof review of all 276 pages is made.

Environment: Python 3.13.5, SymPy 1.14.0, PyMuPDF 1.26.7, with the installed `latexmk`/pdfTeX toolchain. Reproduction on another toolchain need not preserve PDF bytes or pixels; the recorded comparison used one renderer and the available local build environment.

### Author suite and separate referee controls

From the extracted source root:

```sh
python tools/check_revision_v51.py > author-normal.json
python -O tools/check_revision_v51.py > author-optimized.json
cmp author-normal.json author-optimized.json
```

Both executions passed. The identical output SHA-256 is `42b785b030495a51244f9e4f026ffbddb82e741bd62c1bdfc2d30af398f1d2ab`; it also matches the retained native v51 output. Older controls imported by this suite were run through that suite. Other native JSON files were integrity-checked, not all separately rerun as standalone programs.

The separate [independent_checks.py](independent_checks.py) imports no repository code:

```sh
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

Both executions passed. The identical output is deposited as [INDEPENDENT_CHECKS.json](INDEPENDENT_CHECKS.json), SHA-256 `4eac8510ea3695a8923b3f15a4ffe3ec72189c51522a39438293923350e3e1aa`. Script SHA-256: `2ded99beeec4b7ffc117586b3cd7944598e053912d244f0bfe06e79e33c85a97`. Explicit exceptions, not optimization-disabled assertions, enforce its checks.

The independent controls use a different non-even strictly convex polynomial action and unequal positive profiles; verify cancellation, scalar-anchor extraction, effective-factor ratios, origin transport and the moving-anchor derivative; test an excluded joint recording factor; check a quadratic support-width maximum; and verify asymmetric determinant-one contact blocks for orders 3 through 12. Negative controls detect the deliberately incorrect shortcuts. The general support-width argument is proved in the report, not inferred from that one quadratic example.

For the joint-factor control, with `epsilon=1/20` and `phi(s)=s+epsilon*s*(1-s)*(s-1/2)`, exact division gives

$$1-\phi(x)-\phi(y)=(1-x-y)\left[1+\epsilon\left(\frac{x+y}{2}-x^2+xy-y^2\right)\right].$$

The bracket is at least $19/20$ on $x,y\ge0$, $x+y\le1$, and remains positive on $0\le x,y\le121/100$ since it is at least $1-2\epsilon(121/100)^2>0$. Its reciprocal at $x=u^2,y=v^2$ is a regular positive joint multiplier, not a separate multiplier. This is a functional control on the explicitly excluded nuisance class; no billiard realization is claimed. These tests do not prove uniform infinite-flight estimates, Banach-space differentiability, analytic continuation stability, statistical equivalence, or a sampling guarantee.

## Primary literature

The following primary bibliographic/abstract records were checked online. Their use is deliberately narrower than an exhaustive priority search or a fresh proof audit of the external papers.

**L1.** P. W. Holland and Y. J. Wang, *Dependence function for continuous bivariate densities*, Communications in Statistics—Theory and Methods 16(3) (1987), 863–876. [Publisher DOI record](https://www.tandfonline.com/doi/abs/10.1080/03610928708829408). The publisher-indexed bibliographic/abstract result was available; a direct full publisher-page request returned HTTP 403. No claim of reading the full article is made. It is used only to identify the established local dependence functional, which the manuscript itself attributes.

**L2.** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37(1) (2009), 459–489, DOI 10.1214/07-AOS572. [Author paper record, arXiv:0903.0702v1](https://arxiv.org/abs/0903.0702v1). The odds-ratio/marginal distinction supplies context, not an imported theorem about the present billiard sampling experiment.

**L3.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025; v1 remained the current public record at this check. The stated setting is finite-horizon Sinai billiards and an enriched marked length spectrum, with an isometry conclusion.

**L4.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), August 17, 2022; DOI 10.1007/s00222-023-01191-8. The stated setting is analytic open billiards with non-eclipse and suitable symmetry/genericity assumptions.

**L5.** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*. [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), June 3, 2021. Its version comment expressly records removal of an earlier geometric spectral-rigidity assertion affected by a mistake. This is why the dynamical result must not be described as that removed geometric result.

No theorem asserting equivalence of these spectral records to the manuscript's conditional laws was found or proved in this review. The report neither alleges prior duplication on that basis nor credits an unproved removal of the cited hypotheses.

## Review-write scope

The new review branch starts from the exact reviewed delivery. Only this new review directory is written. The manuscript, companion, previous reports, unrelated workstreams, default branch and repository permissions are not edited. The principal recommendation is a contribution/synthesis judgment, not a theorem counterexample and not a commissioned journal decision. The paired machine evidence records both completed checks and their limits.
