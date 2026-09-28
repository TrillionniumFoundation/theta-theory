# A2 v43 — audit scope, sources and reproduction

This file accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It separates author-produced evidence from checks actually executed for this review. It does not certify every mathematical statement in the complete article.

## Frozen objects

Repository: `TrillionniumFoundation/theta-theory`.

| Identity | Value |
|---|---|
| Mathematical source commit | `22d9b930a426cdb2c62984a5a3e5875e95e05e79` |
| Source repository tree | `104656f83d15c5bf4ca86a55b1084b7e02a04054` |
| Products commit, direct child of source | `edd95683ee57965ff8cd82cee1462a478d06ae39` |
| Products repository tree | `b874e40955fa154626960b4d598452a4a916047b` |
| Addressed report | `19935273acf323a3f8971d7f5029b8670ec1bd58` |
| Native Actions run / attempt | `34813913830` / `1` |
| Source artifact | `10335751435` |
| Native artifact | `10336196390` |

The source branch is `revision/a2-v43-complete-native-delivery-2026-09-14`; the products branch is `revision/a2-v43-native-products-34813913830-1`. The latter adds only the delivery directory. The new review is based on that products commit and adds review files only. No manuscript, historical report, default branch or existing revision branch is changed by this review.

## S01 — retrieval and native build

The authenticated connector downloaded both exact-head Actions artifacts. A direct repository clone in the local environment had failed at DNS resolution; the complete source was instead obtained from the authenticated source archive. The successful local build therefore does not depend on claiming that the clone succeeded.

[Run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34813913830) · [Artifact metadata](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34813913830/artifacts) · [Source commit](https://github.com/TrillionniumFoundation/theta-theory/commit/22d9b930a426cdb2c62984a5a3e5875e95e05e79) · [Products commit](https://github.com/TrillionniumFoundation/theta-theory/commit/edd95683ee57965ff8cd82cee1462a478d06ae39).

| Downloaded artifact or native product | Bytes | SHA-256 |
|---|---:|---|
| Source Actions ZIP | 1424721 | `71aea703a6b3cd30ac37dd31697a9d74c46f326e82f1054c595f318e6bb0edb4` |
| Native Actions ZIP | 3659647 | `a15b7a0b7f4ca43ab2d9521f0109f2eab3db33be4b9ce8e340592d3f1f32c627` |
| Native main PDF | 1742379 | `00ff6d0a15884dadf9b509dd87a55289f72c758dea1bef66a6374b7d8743a947` |
| Native companion PDF | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Native package's source ZIP | 1515858 | `6d7017e6c99a0e2188e384aac12a703e85b55a3a93bc2402572f26c54e5fcda0` |

The two source packaging layouts differ; the Actions source ZIP is not asserted to equal the native package's inner source ZIP. The review checked all 95 active-manifest entries (94 main, 1 companion) against the extracted source using both SHA-256 and Git blob SHA-1. There were no mismatches. This is an independently executed manifest-to-source check, not a theorem proof or an independently established provenance attestation for every historical file.

Both native PDFs matched the products recorded in `build-report.json`. The downloaded companion auxiliary has SHA-256 `99cebb7753b5ca752e144c0a6d85d546bc2d812a1532e725f23796bab1420ec6`; the imported-generated-input and recorder records identify the same companion-produced file and source commit. The author's source-integrity/recorder machinery and its existing preservation diagnostics are supporting delivery evidence; their mathematical certification remains false.

The review copied the complete extracted manuscript into a separate build directory, without changing its TeX source, and independently ran the following commands, in this order:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands returned zero. The local pdfTeX was version 1.40.26. The companion produced 7 pages and the main 222 pages. After whitespace normalization of extracted text, every one of the 229 local pages matched the corresponding downloaded native page. This is **text parity, not PDF byte identity or raster identity**. Compilation alone does not establish the correctness of any theorem.

Final native logs contain three underfull vertical-box notices in the main; no unresolved references, missing-character messages or overfull-box warnings were found there. The local run also emitted the shell-escape-disabled epstopdf warning. Early compilation passes required ordinary reference reruns. No claim of a literally warning-free build is made.

Raw local stdout was retained as `local-companion-build.txt` and `local-main-build.txt` in the review workspace. The committed author delivery contains the raw stdout captures `two_collision-build.txt` and `main-build.txt`; its missing `.log`/`.fls` Git objects are treated separately in R43-D1. A configured workflow, an early failed run and an actual successful native build are not interchangeable evidence.

### Rendered-page coverage

The following native main pages were rendered and inspected in contact-sheet overview: **1, 3, 10, 17, 18, 20, 24, 45, 47, 49, 52, 54, 58, 60, 67, 68, 70, 72, 82, 93, 96, 100, 107, 112, 114, 120, 136, 138, 141, 143, 186, 221, 222**. All 7 companion pages were also rendered and inspected. Main pages 49, 68 and 141 were additionally opened individually at readable resolution, covering the smooth-remainder proof, common-frame theorem and physical budget theorem.

No conspicuous clipping, overlap or missing formula material was identified in that sample. This is not a claim that all 222 main pages were visually inspected at full resolution. Reading extracted text, checking a recorder list and visually inspecting a page are different operations.

## Source map and fresh mathematical coverage

All paths below are relative to `papers/A2-v17-boundary-information-coarsening/` at the frozen source commit. Links identify the full exact files. Coverage describes this review, not the cumulative coverage of preceding reports.

### S02

[article/01_introduction_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v41.tex) · [article/01d_proof_architecture_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/01d_proof_architecture_v41.tex)

Complete fresh reading of the introduction and proof architecture, including benchmarks and observation distinctions.

### S03

[article/01c_geometric_setup_v43.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/01c_geometric_setup_v43.tex) · [v3/10_geometry_action.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/v3/10_geometry_action.tex)

Geometric setup, localization, finite Green/Hessian, weighted stationary solutions and relative determinant argument.

### S04

[v3/20_integration.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/v3/20_integration.tex)

Flux normalization, Morse-map integration, right-offset extension and restrictions on the count-law interpretation.

### S05

[v4/10_boundary_layers.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex)

Targeted scrutiny of weighted half-lines, endpoint gluing, trace-norm relative factorization and differentiated exponential bounds; not a claim of a new independent proof of every auxiliary application.

### S06

[article/23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex)

Complete fresh reading: weighted implicit function argument, finite envelope, smooth remainders, homogeneous coefficient isolation and finite-order inverse.

### S07

[article/23f_single_offset_law_inverse_v42.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v42.tex)

Complete fresh reading: density inverse, interior stability, finite-flight transfer and detailed global common-frame proof.

### S08

[article/23b_intrinsic_multichannel_rigidity_v28.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23b_intrinsic_multichannel_rigidity_v28.tex) · [article/23c_analytic_continuation_v23.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23c_analytic_continuation_v23.tex)

Signature/symmetry and gluing arguments; full analytic continuation argument. The earlier fixed-Gram classification is distinguished from the later uncalibrated theorem.

### S09

[article/23b1_signature_rigid_rerooting_v40.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23b1_signature_rigid_rerooting_v40.tex)

Complete rerooting proof and its non-symmetric-root hypothesis.

### S10

[article/23d_rank_two_lattice_recovery_v43.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v43.tex)

Rank-two holonomy, marked matrix recovery and the newly explicit Theorem 15.4 composition.

### S11

[article/23e_signature_stability_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/23e_signature_stability_v25.tex)

Finite signature embedding, perturbed nearest matching, fixed-marked-matrix lattice stability and compact inverse modulus.

### S12

[article/18a1_compact_experiments_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex)

Complete compact-net upgrade and moving-support modulus. Full preceding LAN and all Poisson/loss dependencies were not rederived.

### S13

[article/25a_common_observables_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex)

Common physical sample space, onset pilot, normal/tangent estimation, final-flight choice and bounded-test bias.

### S14

[article/25b_augmented_global_reconstruction_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/25b_augmented_global_reconstruction_v26.tex)

Complete fixed-order template/concentration construction, charged caps and fresh-stage budget implementation in Theorem 39.3.

### S15

[article/25c_analytic_variation_bundles_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/article/25c_analytic_variation_bundles_v25.tex)

Finite-rank support-function/Hermite construction and the role of compactness and contact-separation margins.

### S16 — current navigation and retention defect

[Root README](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/README.md) · [Paper README](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/README.md) · [Ignore file](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/.gitignore) · [Workflow, retention job](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/.github/workflows/a2-v43-native-submission.yml#L67-L105) · [Retention implementation](https://github.com/TrillionniumFoundation/theta-theory/blob/22d9b930a426cdb2c62984a5a3e5875e95e05e79/papers/A2-v17-boundary-information-coarsening/tools/retain_native_v43.py) · [Receipt](https://github.com/TrillionniumFoundation/theta-theory/blob/edd95683ee57965ff8cd82cee1462a478d06ae39/deliveries/a2-v43/22d9b930a426cdb2c62984a5a3e5875e95e05e79/REPOSITORY_RETENTION.json) · [Source/products comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/22d9b930a426cdb2c62984a5a3e5875e95e05e79...edd95683ee57965ff8cd82cee1462a478d06ae39).

Both current README files identify v42. The products commit adds 26 paths, none modifying the manuscript. The receipt describes the filesystem copy as Git retention, but 13 listed files are absent from that commit:

```text
main.aux
main.fdb_latexmk
main.fls
main.log
main.out
main.pdf
main.toc
two_collision.aux
two_collision.fdb_latexmk
two_collision.fls
two_collision.log
two_collision.out
two_collision.pdf
```

These names are in the downloaded artifact. A connector fetch of the exact advertised `main.pdf` path at `edd95683ee57965ff8cd82cee1462a478d06ae39` returned 404. Commit comparison independently shows the absent paths. The workflow uses ordinary directory-level `git add --` after generating its receipt; the repository ignores all these suffixes. The local negative control reproduces the omission. No credentials, tokens or sensitive configuration were accessed or changed.

This distinction can be rechecked in any authenticated checkout without downloading binary content through a text-only API:

```sh
SOURCE=22d9b930a426cdb2c62984a5a3e5875e95e05e79
PRODUCTS=edd95683ee57965ff8cd82cee1462a478d06ae39
git diff --name-only "$SOURCE" "$PRODUCTS"
git ls-tree -r --name-only "$PRODUCTS" -- "deliveries/a2-v43/$SOURCE"
git cat-file -e "$PRODUCTS:deliveries/a2-v43/$SOURCE/main.pdf"
```

The last command should fail for the reviewed products commit. This does not test whether the PDF exists in Actions: the successful download already establishes that. The artifact metadata records expiry on `2026-12-13T06:32:42Z`. A lasting archive or correct Git retention is requested, not an assertion that present access failed.

### S17 — preceding review, historical rather than newly executed evidence

[The v42 report](https://github.com/TrillionniumFoundation/theta-theory/blob/19935273acf323a3f8971d7f5029b8670ec1bd58/reviews/a2-v42-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md) reviewed v42 source `6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad`. Its full native-delivery hold concerned failed pre-runner Actions evidence. It expressly allowed a release or artifact package rather than requiring all binaries in Git. Its earlier favorable LAN, Poisson and diagnostic findings are not represented as new executions here.

### S18 — this review's diagnostics

[Source](independent_checks.py) · [Recorded final results](RESULTS.json).

Environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0; Git was available. Commands actually executed:

```sh
OPENBLAS_NUM_THREADS=1 python3 -B independent_checks.py > RESULTS.json
OPENBLAS_NUM_THREADS=1 python3 -O -B independent_checks.py > RESULTS_OPTIMIZED.json
cmp RESULTS.json RESULTS_OPTIMIZED.json
```

Both final executions returned zero and the comparison found identical bytes. An earlier draft of the diagnostic needed a Python integer-to-Fraction conversion corrected; it was an implementation issue, not a failure of a manuscript identity. The committed version and recorded results are the corrected, executed pair.

The rational test concerns interior cancellation and uses an arbitrary positive normalization constant: it is not advertised as a normalized global billiard law. The nonlinear test solves actual finite stationary flight equations; the sixth-order test uses the finite stationary envelope with 60 flights and decreasing endpoints, not an infinite-domain theorem. The Git test operates in a temporary directory and never stages author files. All diagnostic tolerances and configurations are visible in the source. Exact last-bit floating-point equality across different BLAS/platform environments is not promised.

## Primary literature checked on September 14, 2026

**L1.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5). The version notice explicitly removes the earlier geometric spectral-rigidity assertion following the Proposition 3.1 error; the abstract retains the smooth-conjugacy application. The current manuscript is not accused of citing the removed assertion as valid.

**L2.** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4). The primary abstract states symmetry and genericity assumptions for analytic open billiards.

**L3.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1). The primary abstract uses an enriched marked length spectrum and finite horizon. No claim about ordinary un-enriched data is inferred.

**L4.** Alexander Meister and Markus Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1). The primary abstract states equivalence with two independent Poisson point processes whose intensity boundaries contain the target curve.

These checks establish the specific comparison statements in the report. They do not constitute an exhaustive priority search or an independent proof of these external papers. Different observation maps are not ordered without a proved reduction.
