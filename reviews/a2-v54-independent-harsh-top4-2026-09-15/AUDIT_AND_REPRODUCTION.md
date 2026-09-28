# A2 v54: audit scope, immutable sources, and reproduction

Date: September 15, 2026. This ledger accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes proof scrutiny from source preservation, finite diagnostics, compilation, and page comparison. None of the operational checks is a proof certificate.

## 1. Frozen objects

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v54-review-ready-2026-09-15` |
| Review-ready commit | `802cb27e731a3a821903a7308cba9d5da29bbf79` |
| Review-ready root tree | `f13eb40d4eaa955808b88f93269457ba21531fbf` |
| Actual compiled source | `2cedae961195f97df802aaa81112d95cd32974e1` |
| Manuscript prefix | `papers/A2-v17-boundary-information-coarsening` |
| Reconstructed manuscript tree | `407b278984b14e57468e727fb56b0fa4163a7207` |
| Native workflow run / attempt | `34934158178` / `1` |
| Native artifact | `10382712647` |
| Workflow preparation commit, not compiled source | `eb6989f624e7417db92140841710c22719cc1cd2` |
| Previous v53 report commit | `000ce24f65f8381d2180cbd1f080d3d8470c8157` |
| Source reviewed by v53 report | `42cc62f230473c34d78af1d06b9ca5c2651ae86d` |

The GitHub comparison from compiled source to review-ready head is ahead by three commits. Its changed-file list comprises the root delivery description, native delivery artifacts, and final review-ready ledger; no compiled TeX input is changed by that delivery layer. The review report is an addition under a new review directory, not a modification of the author manuscript, previous reports, A1, or the default branch.

Immutable manuscript entry: https://github.com/TrillionniumFoundation/theta-theory/blob/2cedae961195f97df802aaa81112d95cd32974e1/papers/A2-v17-boundary-information-coarsening/main.tex

Native delivery directory: https://github.com/TrillionniumFoundation/theta-theory/tree/802cb27e731a3a821903a7308cba9d5da29bbf79/deliveries/a2-v54/2cedae961195f97df802aaa81112d95cd32974e1

Artifact metadata checked through the connected GitHub API: https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34934158178/artifacts

## 2. Source keys and bounded mathematical coverage

All S-paths are relative to the manuscript prefix at the actual compiled source above. Line numbers count the frozen UTF-8 source, not PDF lines. Labels are more stable than source filenames: the active v54 Section 23 still has a v53 filename.

| Key | Source and inspected material | Git blob |
|---|---|---|
| S1 | `main.tex` (165 lines); structural introduction and observation declarations in `article/00_structural_introduction_v48.tex` (365 lines), and complete `article/00b_interaction_overview_v51.tex` (81 lines). Used for theorem hierarchy, supplied observations, article synthesis, and claims of the new experiment. This is not a separate proof certification of every theorem cited by the introduction. | main: `ad3d407d9a60fd6b7baeeeaff7c0837b0c13b435`; introduction: `ecb4ddb2c13c2bf573a57e7f72d9ebaa57c2e0f1`; overview: `efe92e353d70e42fc2abad9e428a10a78fd5f34c` |
| S2 | Complete `article/18g_realized_window_information_v53.tex`, lines 1–595. Lemma 23.1 and normalization, lines 18–87; actual realization and testing, lines 95–263; strengthened Corollary 23.3 and proof, lines 272–405; stopped-experiment setup and Theorem 23.4, lines 406–595. The new theorem appears on main PDF pages 109–110; the strengthened corollary spans pages 106–108. | `9d4fe6f11d850c9d955f25cf882feec133751f6b` |
| S3 | `v4/10_boundary_layers.tex`, lines 1–386: weighted half-line solution, trace-class perturbation, relative determinant and gluing, fixed-offset law and small-offset interface. Fresh scrutiny of this module does not certify every earlier physical event or finite-action construction on which it relies. | `892a88e37a24e591fa525013c41910c791e28e73` |
| S4 | `article/23a_signed_endpoint_rigidity_v27.tex`, especially finite-envelope and actual-smooth remainder argument, lines 259–410, and homogeneous isolation, last-jet block, tangent inverse, and completion, lines 411–599. Leading recovery and statement hypotheses were also checked. | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| S5 | `article/23q_support_and_interior_windows_v52.tex`, lines 1–271: complete-support centering versus interior extraction; positivity and critical-line visibility; fixed smooth topology; both exact-fiber inclusions and projected derivative-kernel interface. | `ffbaa8674e5cc1fb9645efe43e96841ae7b2ba8d` |
| S6 | `article/23j_generic_finite_channel_rigidity_v45.tex`, selected-design construction through line 270, with direct inspection of obstruction descent, lines 60–93, and two-cycle gain selection, lines 95–154. The entire later genericity/reconstruction portion of this 525-line file is not independently certified here; finite matching was checked in S7 and differentiable registration in S8. | `18e7e152e6296716232cd289570cfb7f4642712d` |
| S7 | Complete `article/23n_finite_symmetry_v49.tex`, lines 1–243: finite congruence alternatives, local angular lift, finite exact fiber with both inclusions, true gain-matrix inverse and geometric realization tests, and circular comparison. | `3bc39ac137812340b9426e9f2b7457a39d6e7f91` |
| S8 | `article/23m_differential_rigidity_v48.tex`, lines 1–505: common-strip variations, moving-reference trace derivative, moving-cap normalizer, differentiated local inverse, analytic propagation, actual-branch registration, lattice kernel and finite-coordinate proof. | `1eb8db48bd184378ebd10be30c033b91edd8f36d` |

The mathematical coverage is deliberately narrower than the 281-page build. In particular, there is no new full re-audit of every inherited local asymptotic experiment, the richer pilot/histogram acquisition theory, all global estimators, the archived catalogue, or every proof in the two-collision companion. Passing finite checks inherited from those modules does not change that statement.

### Revision records

**R1.** Complete v53 referee report, read through its continuation: `reviews/a2-v53-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, at `000ce24f65f8381d2180cbd1f080d3d8470c8157`; Git blob `7f4278afe637e09dbf638896d0202fc91db134b8`. Sections 4 and 5 contain the nonmandatory Hellinger and waiting-record improvements. Its editorial reservation is not treated as a theorem counterexample.

**R2.** v54 response `RESPONSE_TO_REFEREE_V54.md`, all 89 lines, blob `e91c6e1229e36bcb06f3edb8e209cbe05bf843d0`; historical derivation audit `HISTORICAL_DERIVATION_AUDIT_V54.md`, all 33 lines, blob `1bb0ff714d807f30b4555207d6e4cae58384cc70`; primary-record check `LITERATURE_CHECK_V54.md`, all 14 lines, blob `ec9be7399b1a2b4922b01605e7948a2b10a5515c`. These describe the author's response and preservation policy; substantive findings in the report are based on the mathematical source and independent calculations, not merely this letter.

## 3. D1: source and build reproduction actually performed

The workflow artifact was downloaded using the authorized GitHub connector. Its SHA-256 is `d7572bce8b3a9131685f9a76cab47b381e60bf99aaf9c7dd4adf0444e5419610`, matching the digest returned by the GitHub run-artifact listing. Its inner `native-source.zip` has SHA-256 `46e5ca2a859424e3362baae1747551d3e54a8c5e67c3bac8788ba536f3c9b4f6`.

For all 626 entries of the frozen-source manifest, the downloaded bytes, byte counts, SHA-256 values and Git blob IDs were checked. Git blob IDs were recomputed from `blob <length>\0` followed by the file bytes. Recursive Git tree reconstruction, using recorded modes and Git directory ordering, produced the manuscript tree reported above. All entries of both active-input manifests matched the frozen manifest: 110 main inputs and one companion input, 111 distinct inputs in total. All 34 retained native evidence files matched their declared byte counts and SHA-256 values.

The source was copied to a clean rebuild directory. The author checker was executed in both ordinary and optimized Python; its outputs were byte-identical to each other and to the native retained normal result. Its preservation disposition is 107 inherited active inputs unchanged in place, four exact archived originals, 542 verbatim inherited blocks, one corollary/proof pair strengthened, and one new theorem/proof pair. The changed manuscript source files are `main.tex`, the structural introduction, the realized-window module, and the bibliography. No result here is described as a theorem-prover certificate.

Both entries were rebuilt, companion first, using:

```sh
python tools/check_revision_v54.py > author-normal.json
python -O tools/check_revision_v54.py > author-optimized.json
cmp author-normal.json author-optimized.json
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

All 281 main pages and all seven companion pages were compared with the native PDFs. Each page's extracted text and 72-dpi RGB pixel array agreed under the same PyMuPDF 1.26.7 renderer. The rebuilt PDF bytes differ from the native bytes; byte identity is neither necessary for this comparison nor claimed. Exact native and rebuilt SHA-256 values are in `reproduction.json`.

Direct visual inspection was limited to main pages 107, 109, and 110, rendered at approximately 122 dpi. Other rendered pages were not counted as visually inspected. The inspected pages showed readable mathematical content and no observed clipping. The main final log has four underfull-vbox notices; the companion has none. Both final local logs contain an `epstopdf` warning because shell escape was deliberately disabled. The final scans found no overfull-box or unresolved reference/citation warnings. No claim of zero warnings is made.

## 4. D2: independent finite checks

`independent_checks.py` uses only the Python standard library and imports no author code. It contains explicit guards rather than relying on `assert`, so optimized Python does not remove its tests. The ordinary and optimized outputs are identical; the resulting data are retained within `reproduction.json`.

Coverage includes the exact rational integral of `F^2`, the normalized Hellinger and likelihood coefficients, actual contact-Hessian constants and hyperbolic cosines; 15 exact capped probability examples with unequal mark distributions; common-cemetery TV bounds; the count-to-full and bit-to-full simulation kernels; the exact finite count-only Bayes formula; and the exact stopped-charge identity. Twelve finite product examples check affinity tensorization and the TV/Hellinger inequalities. Numerical cap-intensity examples and a huge-cap negative control test the necessary distinction between retaining counts and retaining only an acceptance bit.

These checks do not establish nonlinear billiard realization, an infinite-dimensional regularity theorem, asymptotic experiment convergence on their own, or a uniform minimax bound. The report gives the relevant arguments and labels the additional reductions as reviewer derivations. Run from this review directory:

```sh
python independent_checks.py > reviewer-normal.json
python -O independent_checks.py > reviewer-optimized.json
cmp reviewer-normal.json reviewer-optimized.json
```

The script SHA-256 is recorded in `reproduction.json`. Its finite-distribution examples are diagnostic examples, not new claims about a simulated billiard table.

## 5. Primary references checked on September 15, 2026

Only the stated scopes, abstracts, bibliographic entries, and version notices were used for the following comparison. The cited external proofs were not independently re-reviewed, and the search is not an exhaustive priority determination.

**L1.** Gerhard Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; DOI `10.1214/07-AOS572`; arXiv `0903.0702v1`. Odds-ratio specification and unrestricted marginals. https://arxiv.org/abs/0903.0702

**L2.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv `2510.18983v1`, October 21, 2025. Enriched marked length data for finite-horizon Sinai billiards. https://arxiv.org/abs/2510.18983

**L3.** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv `1905.00890v4`, August 17, 2022; related DOI `10.1007/s00222-023-01191-8`. Analytic open obstacles, non-eclipse, symmetry/genericity and marked length observations. https://arxiv.org/abs/1905.00890

**L4.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv `2010.04120v5`, June 3, 2021. The version notice removes the affected geometric spectral-rigidity assertion and retains dynamical conjugacy results. https://arxiv.org/abs/2010.04120v5

No equivalence of these spectral observation maps with the manuscript's selected boundary-law datum is assumed. The report neither accuses the author of relying on the removed assertion nor treats standard association algebra as proof that the billiard inverse was already known.
