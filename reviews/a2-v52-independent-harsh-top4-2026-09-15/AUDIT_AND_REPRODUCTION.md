# Audit, source map, and reproduction record — A2 v52

This accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It records what was actually read or executed, distinguishes author diagnostics from independent calculations, and pins the assessed source. No statement here is an institutional journal endorsement or a complete mathematical certification.

## 1. Frozen identities and authentic artifact

| Object | Identifier |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v52-review-ready-2026-09-15` |
| Reviewed delivery head | `95046e3b4fce025e5763b555c38180339d4869a0` |
| Actual compiled mathematical source | `9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6` |
| Workflow preparation head, not compiled source | `6a1ed217b022c84b2327feddf5b940e4ab4bcd9e` |
| Source repository tree | `094034dce88597a3955a98c9ea597370a11eb240` |
| Source `papers` tree | `cf9ab97be8ecf764ea99b2ac0f9047aadd4936a5` |
| Source manuscript subtree | `ba34d61e1eda687d1257be33d1cbae9758127d94` |
| Native workflow run / attempt | `34919713194` / `1` |
| Downloaded artifact | `10376789760` |
| Artifact name | `a2-v52-native-9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6-1` |
| Native product commit | `1785b8047369572a81eb8ac032322c1c42070e7b` |
| Product-attestation commit | `6cd41275d6b0be1091959a3a27bcb6298a7594ad` |

The GitHub connector was used to discover the revision branches, read the submission and preceding report, obtain the workflow artifact metadata, and download the authorized artifact. The actual Git commit object and the two successive Git tree objects were fetched separately. They link source commit `9fd0c14...` to manuscript subtree `ba34d61...`. The independent reconstruction of that subtree from all downloaded source entries agrees exactly.

The artifact ZIP has 4,477,869 bytes and SHA-256:

```
cfb7b4c2b5cf1cb4f32f06111a6ff3a9ea597c0621f1a95a189f0809bc9735e9
```

This agrees with the digest in GitHub's workflow-artifact record. The nested complete source ZIP has SHA-256:

```
9aee1723a9fd08c62015b0bf7d5cb6dd218049beb4b01bf5be9ab6605239346c
```

The preceding v51 report is frozen at `d0fd9a9b0d5cdd8004f42a7f109e39de50adda75`. It assessed source `b9201bc272bc7ecbab1ad6a91fc844216685fadd` and delivery `ffd53f26383874dc798af9a54ae877ffdd0f81eb`. These identities are retained to avoid treating the preceding report as a review of the present source.

## 2. Source map and limits of reading

Except where specified otherwise, every manuscript source below is under `papers/A2-v17-boundary-information-coarsening/` at compiled commit `9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6`. Line numbers refer to these frozen UTF-8 files. Page numbers in the report refer to the complete native main PDF, not a condensed version.

**[S1] Introduction and principal formulations.** `main.tex`; `article/00_structural_introduction_v48.tex`, lines 1–334; and `article/00b_interaction_overview_v51.tex`, lines 1–81. Theorems A/B, supplied observations, significance claims, and equation (1.6) were examined. The common-measure discussion is on main page 8. Full introductory sources were read.

**[S2] Complete new v52 module.** `article/23q_support_and_interior_windows_v52.tex`, lines 1–271. Full statements and proofs were read: support centering, lines 1–54; window model and extraction, lines 56–165; geometric fiber and kernel, lines 167–236; physical recording, fixed-observation convergence, and acquisition qualifications, lines 238–271. Lemma 14.5 and Theorem/Corollary 14.6–14.7 occur on pages 61–64.

**[S3] Inherited unknown-origin interaction.** `article/23p_uncentered_interaction_v51.tex`, lines 1–390. The interaction formula, anchored inverse, finite-smooth local extension, geometric fiber, projected derivative kernel, and observation restrictions were examined. Particular derivative checks concern lines 182–276 and 278–365.

**[S4] Relative forward core.** `v4/10_boundary_layers.tex`, lines 1–386. The half-line construction, relative factorization at lines 118–250, and fixed-offset law at lines 252–327 were read in detail. The review examines the gluing, localized Hessian, trace-class comparison, and fixed-offset interfaces; it does not claim a new formal verification of every upstream operator lemma in the repository.

**[S5] Actual-smooth signed inverse.** `article/23a_signed_endpoint_rigidity_v27.tex`, lines 1–598. The weighted inverse and envelope framework, actual-smooth factorization at lines 292–381, homogeneous isolation, degree block at lines 471–530, and tangent/analytic completion at lines 531–598 were examined. This is the basis for the report's distinction between actual smooth jets and formal power series.

**[S6] Registered analytic continuation.** `article/23c_analytic_continuation_v23.tex`, lines 1–44. The complete lemma and proof were read. The exact identity-theorem conclusion is not treated as a quantitative continuation estimate.

**[S7] Finite-symmetry interfaces.** `article/23n_finite_symmetry_v49.tex`, lines 1–243. The finite-congruence lemma, actual local angular branch, finite compatible-fiber enumeration, and circular comparison were read. The review follows the inherited cochain formula through the current proof interfaces; it does not freshly re-prove every historical realization example.

**[S8] Differential and finite-coordinate interfaces.** `article/23m_differential_rigidity_v48.tex`, lines 1–505. The common-strip family, moving reference derivatives, action inverse, analytic variation, registration, lattice, and finite-coordinate argument were examined. The finite-coordinate proof at lines 423–505 was checked directly, including its convex-ball lower Lipschitz argument.

**[S9] Charged histogram interface.** `article/23l_calibrated_histograms_v47.tex`, especially lines 139–203 and 285–305. The category-bias decomposition, pilot conditioning, and cap accounting were checked as interfaces. This is not an independent proof audit of the full pilot, the quantitative analytic inverse in the preceding section, or all statistical claims in Parts II and III.

**[S10] Current response and historical audit.** `RESPONSE_TO_REFEREE_V52.md` and `HISTORICAL_DERIVATION_AUDIT_V52.md`, at the reviewed delivery/source. These were used to identify the revision's asserted changes and historical dependencies, not as mathematical certificates. The author preservation checker was inspected and rerun separately as described below.

**[S11] Prior report.** `reviews/a2-v51-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at `d0fd9a9b0d5cdd8004f42a7f109e39de50adda75`. The full report was read across paginated reads. Its bounded requests and previously resolved points were distinguished from its editorial judgment. Its conclusions were not substituted for current source checks.

The new module and the core interfaces listed above received substantive mathematical review. The remaining statistical experiments, global estimators, auxiliary appendices, and two-collision companion did **not** all receive independent theorem-by-theorem proof certification. The complete companion was nevertheless included in source verification and rebuilding.

## 3. Primary-literature check

The following primary records were checked on September 15, 2026. The search was targeted rather than exhaustive. No priority theorem or information reduction between different observation models is inferred from it.

**[L1]** P. W. Holland and Y. J. Wang, *Dependence function for continuous bivariate densities*, Communications in Statistics—Theory and Methods **16** (1987), 863–876. DOI: `10.1080/03610928708829408`. The primary publisher abstract was checked for the continuous dependence-function framework; the complete article's proofs were not audited.

**[L2]** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics **37** (2009), 459–489. DOI: `10.1214/07-AOS572`; arXiv `0903.0702v1`. The primary arXiv record and PDF introductory definition were checked. PDF page 2 explicitly displays the four-density cross-product ratio and distinguishes association from marginal laws. The present review does not import that paper's sampling-invariance conclusions into the billiard experiment.

**[L3]** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv `2510.18983v1`. The current primary record lists the October 21, 2025 version and states the finite-horizon, enriched marked-length-spectrum problem. Its data are not the conditional endpoint laws of this submission.

**[L4]** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv `1905.00890v4`; DOI: `10.1007/s00222-023-01191-8`. The primary version history and abstract were checked for the analytic open-billiard, non-eclipse, symmetry/genericity comparison. The full external proof was not re-audited.

**[L5]** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv `2010.04120v5`. The June 3, 2021 version's explicit notice about the erroneous earlier Proposition 3.1 and removal of the geometric spectral-rigidity assertion was checked. No removed assertion is used as support for the present manuscript.

Primary record addresses:

```
https://www.tandfonline.com/doi/abs/10.1080/03610928708829408
https://arxiv.org/abs/0903.0702
https://arxiv.org/pdf/0903.0702
https://arxiv.org/abs/2510.18983
https://arxiv.org/abs/1905.00890
https://arxiv.org/abs/2010.04120
```

## 4. [D1] Independent source and build verification

[VERIFICATION.json](VERIFICATION.json) records the executed verification. [verify_snapshot.py](verify_snapshot.py) is the independent read-only verifier. It imports no author code, checks manifest entries and Git objects, reconstructs the manuscript tree, verifies native evidence, compares the complete PDFs, and scans the final logs.

All **598** source files passed size, SHA-256, and Git blob checks. The reconstructed tree equals `ba34d61e1eda687d1257be33d1cbae9758127d94`. All **110** active inputs passed both native-manifest and rebuilt-input checks, and all **34** native evidence entries passed size/digest checks.

Both full entries were compiled from a copy of the downloaded frozen source, with the companion first and shell escape disabled:

```bash
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands exited successfully and produced the complete **273-page** and **7-page** documents. Every page had identical extracted text and identical 72-dpi RGB arrays under the same PyMuPDF 1.26.7 renderer. This is not a claim of PDF byte identity or of identical rendering at every resolution and renderer. The file digests differ and are retained in `VERIFICATION.json`.

Direct visual inspection of the native main PDF covered pages **8, 61, 62, 63, and 64**, rendered at 90 dpi. No clipping was observed on those inspected pages. Other rendered pages and the complete automated pixel comparison are not counted as additional direct visual coverage. The final main log has four underfull-vbox notices; its warning scan found no overfull box, undefined reference/citation, or rerun-to-resolve notice. The companion final warning scan was empty.

## 5. Author diagnostics versus independent calculations

The read-only author diagnostic `tools/check_revision_v52.py` was inspected before execution and run under ordinary and optimized Python. Both outputs are byte-identical and match the native retained output. [AUTHOR_CHECKS_RERUN.json](AUTHOR_CHECKS_RERUN.json) retains the result. Its preservation checks find all **109** inherited active inputs, **104** byte-identical in place, **five** exact archived originals, and **532** inherited statement/proof blocks, including **250** proofs, preserved verbatim. The new module contributes one lemma, one theorem, one corollary, and three proofs. These are author-implemented preservation/control checks rerun by the reviewer, not an independent theorem prover.

The separate [independent_checks.py](independent_checks.py) imports no author code. It exercises non-even actions, unequal separate endpoint weights, mixed logarithmic derivatives, signed scalar-anchor inversion, moving origins and anchor derivatives, the fixed-window normalizer, and the small-window Hellinger expansion in the report. Explicit exception-based checks remain active under `python -O`. The deliberate omission controls are essential: they show the tests distinguish the checked formulas from several plausible wrong ones.

[INDEPENDENT_CHECKS.json](INDEPENDENT_CHECKS.json) and its optimized counterpart are identical. Selected results are an action-derivative maximum error of approximately `1.04e-9`, a fixed-window normalizer error of approximately `6.17e-11`, and nonzero errors of approximately `0.106`, `0.00336`, and `0.00966` in the frozen-origin, omitted-anchor-derivative, and omitted-normalizer controls respectively. The exact Hellinger leading coefficient in the chosen quadratic example is `7/145800`; the decreasing-window quadrature approaches that value.

The analytic expansion and product-affinity argument in the main report prove the stated functional two-point benchmark. Quadrature is corroboration, not a proof of the exponent. None of these finite checks constructs a global billiard realizing the exact quadratic actions, proves infinite-flight bounds, gives a sufficient estimator, or certifies a global billiard minimax rate.

For a fresh reproduction, extract the workflow ZIP into `ROOT/native`, its `native-source.zip` into `ROOT/source`, and copy `ROOT/source/source` to `ROOT/rebuild`. Put this review directory at `ROOT/report`. Build the two entries from `ROOT/rebuild` as above, then run:

```bash
# From ROOT/source/source:
python tools/check_revision_v52.py > ../../report/AUTHOR_CHECKS_RERUN.json
python -O tools/check_revision_v52.py > ../../report/AUTHOR_CHECKS_OPTIMIZED.json

# From ROOT/report:
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS_OPTIMIZED.json
python verify_snapshot.py .. /path/to/a2-v52-native-review-input.zip \
  > VERIFICATION.json
```

The finite checks require NumPy; the author checker also requires SymPy. The snapshot verifier requires PyMuPDF. A working TeX installation with the manuscript's packages and `latexmk` is required for the full rebuild. The verifier does not itself compile or execute manuscript sources.

## 6. Interpretation and repository scope

The rejection recommendation concerns the requested journal level, not a newly disproved theorem. The preceding concrete editorial requests are recorded as addressed. The new small-window result is a functional observation-model benchmark with explicit scope, not a reason to demand a uniform theorem excluded by the manuscript.

This review is additive. Its commit is based on the frozen v52 delivery and introduces only files in the new review directory. It does not revise mathematical source, overwrite prior reports, alter the default branch, change permissions, or certify unreviewed workstreams. The exact commit and branch are to be taken from the repository record, not from a mutable version label.
