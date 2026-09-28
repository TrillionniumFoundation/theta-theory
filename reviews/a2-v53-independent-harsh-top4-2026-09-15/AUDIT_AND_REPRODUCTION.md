# Audit ledger and reproduction record — A2 v53

This file defines the source keys used by `REFEREE_REPORT.md`. All manuscript paths below are relative to `papers/A2-v17-boundary-information-coarsening` at compiled-source commit `42cc62f230473c34d78af1d06b9ca5c2651ae86d`. Historical version numbers in filenames do not identify the current revision. The enclosing review-ready commit is `da8d788ee1ba5a34c7430ccca805ae9524bcca88`; its root tree is `9a6fc7ee7b3d53c6784fccf98f6b0ab2b703c87d`.

## Source and coverage keys

**S1 — Architecture and observation scope.** `main.tex` (161 lines), `article/00_structural_introduction_v48.tex` (353 lines), and `article/00b_interaction_overview_v51.tex` (81 lines). Read the entry, structural theorem statements, observation qualifications and synthesis. This does not claim independent proof review of every input in the entry graph.

**S2 — Complete new mathematical module.** `article/18g_realized_window_information_v53.tex` (366 lines); Section 23, native main pages 103–107. Lemma `lem:v53-window-expansion` / Theorem `thm:v53-realized-experiment` / Corollary `cor:v53-finite-flight` are the new statements. The full source, constants, geometry, normalization, three testing regimes and finite-flight passage were examined. The exact labels can also be found directly in the frozen source; the module blob is `0f378e92f29c9f82d5dcbc9e3b89339e4f1870fc`.

**S3 — Relative forward construction.** `v4/10_boundary_layers.tex` (386 lines). Fresh reading of its half-line construction, finite/half-line gluing, normalized Hessian determinant, relative law and fixed-offset normalization. This is not a newly complete audit of all earlier phase-space preparation definitions imported elsewhere.

**S4 — Signed action-to-contact mechanism.** `article/23a_signed_endpoint_rigidity_v27.tex` (599 lines). Focus on the weighted inverse, finite envelope identity, actual-smooth jet factorization, last-jet matrix, odd-order retention and finite-order tangent bound, especially the actual-smooth argument and ensuing recursion in lines 292–599. Its complete dependency library has not been independently formalized.

**S5 — Density extraction and analytic propagation.** `article/23f_single_offset_law_inverse_v42.tex` (270 lines) and `article/23c_analytic_continuation_v23.tex` (44 lines). Checked positive square/scalar anchor inversion, finite-order density stability, and the separate analytic image recovery step.

**S6 — Unknown centers and interior windows.** `article/23q_support_and_interior_windows_v52.tex` (271 lines). Read the support-centering distinction, window extraction, smoothness, both geometric fiber inclusions and projected differential kernel. No claim that total variation controls derivatives or that arbitrary crops retain the needed critical lines.

**S7 — Clear skeleton.** `article/23j_generic_finite_channel_rigidity_v45.tex` (525 lines), with fresh close coverage of lines 1–247: separation, obstruction descent, persistent clear collars, selected-channel locality and the two-cycle graph count. The subsequent entire genericity discussion is not included in this round's close proof-coverage claim.

**S8 — Finite alternatives and lattice.** `article/23n_finite_symmetry_v49.tex` (243 lines), especially the congruence/local-alignment and finite-fiber proofs through line 195; and `article/23d_rank_two_lattice_recovery_v43.tex` (164 lines). Checked actual local branches, finite candidate enumeration, both realization directions, and the genuine gain-matrix inverse. The circular comparison is not needed by the new statistical result.

**S9 — Differential mechanism.** `article/23m_differential_rigidity_v48.tex` (505 lines). Read the moving-reference derivative, moving normalizer, smooth inverse linearization, analytic variation, local harmonic registration, lattice derivative, kernel theorem and finite-coordinate argument. Scope is the explicitly stipulated common-strip families and model-local exact observables.

**R1 — Previous report.** Repository-relative `reviews/a2-v52-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md` at the review-ready commit. Blob `373519334427c754e25ed57125a67a4acc76f27c`. Read for the actual requests, closed items, functional benchmark and prior recommendation. It is evidence of review history, not a proof certificate.

**R2 — Response and history.** `RESPONSE_TO_REFEREE_V53.md` (95 lines) and `HISTORICAL_DERIVATION_AUDIT_V53.md` (39 lines), read in full. The response does not say a newly appended theorem was mandatory and does not equate resolving technical issues with editorial acceptance.

The precise byte counts, SHA-256 hashes and Git blob identities of S1–S9/R2 are in `reproduction.json`. To inspect a pinned source through GitHub, use the compiled commit and the full manuscript path, not a moving branch head.

## D1 — Independent delivery verification and rebuild

GitHub Actions run **34924398658**, attempt **1**, artifact **10380075042**, named `a2-v53-native-42cc62f230473c34d78af1d06b9ca5c2651ae86d-1`, was downloaded through the authorized connected GitHub action. Its archive digest matches the digest returned by GitHub:

```text
288117d5b31d61ad65e8ab2b62ad3de805a059a3d5629c144a4bc38978391638
```

The workflow preparation head `d64bebebac6c8e20dcbe38763dbd51b2ab0c75ce` is distinct from the compiled-source commit. Extracting `native-source.zip` provides the source directory used below. Verification rehashes every one of 612 frozen files, reconstructs its Git tree from blob contents and recorded modes, and obtains:

```text
6153e28c29bd54c2d45f6466d3c3c3bf6dd09942
```

The connected GitHub contents response for `papers` at the compiled-source commit independently identifies that exact tree for `A2-v17-boundary-information-coarsening`. Thus the reconstructed tree is not only compared to an unverified self-declared local value. All 111 unique active inputs agree with the frozen manifest; all 34 declared native evidence files match their hashes.

A separate copy of the complete source was rebuilt, companion first, with these commands:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both commands succeeded. The native PDFs and the independently rebuilt PDFs have different byte hashes, which are all retained in the JSON. Their extracted page texts and same-renderer 72-dpi RGB page arrays agree on **278/278 main pages and 7/7 companion pages**. The final main log has four underfull vertical-box notices and no scanned overfull, undefined-reference/citation or missing-character warning. The companion final log has none of those notices. Earlier-pass output may contain warnings resolved by later passes; the summary refers to final logs.

Direct visual inspection was of **main pages 103–107 only**. Programmatic comparison of all pages is not a claim to have read every displayed proof visually. No font files, native PDFs or redundant manuscript copies are added by this review.

The included portable verifier reproduces the hash/tree/evidence and PDF comparisons after artifact extraction and a separate rebuild:

```sh
python verify_delivery.py \
  --artifact a2-v53-native-artifact.zip \
  --native native --source source/source --rebuild rebuild \
  --output delivery-result.json
```

It requires PyMuPDF and Python supporting `Path.is_relative_to`; it performs no download, build or manuscript-code execution. It was itself run against the reviewed files and returned the same core result as the original session verifier. A different TeX installation may legitimately alter pagination or rendering, so the current agreement is recorded as a concrete result, not promised as universal byte reproducibility.

## D2 — Finite mathematical diagnostics and preservation rerun

The author checker was read and run from the frozen manuscript directory:

```sh
python tools/check_revision_v53.py > author-normal.json
python -O tools/check_revision_v53.py > author-optimized.json
cmp author-normal.json author-optimized.json
cmp author-normal.json native/check_revision_v53-normal.json
```

Here the last `native` path is relative to the chosen extraction layout. Both comparisons succeeded in this review's layout. Its output hash and complete preservation summary are in `reproduction.json`. This validates reproducibility of the checker and its stated preservation checks; it does not make an author diagnostic an independent theorem prover.

The separate `independent_checks.py` imports **no author code**. It uses exact rational arithmetic for curvature/Hessian coefficients and information constants, a direct quadratic half-line energy sum, Gauss–Legendre quadrature for two synthetic actions with nonzero quartic terms, exact product-affinity identities, and exact geometric-distribution tail formulas. Its guards use explicit exceptions, not optimized-away assertions.

```sh
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

Both runs succeeded and their outputs were identical. `independent_checks.json` is the retained ordinary-run result. Its exact Hellinger coefficient, after multiplication by $d^4$, is `2622050/2250423`; the likelihood coefficient is four times this. For synthetic quartic actions, the Hellinger distance divided by its leading term decreases from about 1.23516 at $h=0.08$ to 1.00321 at $h=0.01$. These synthetic actions are **not** asserted to be exact actions of the realized bodies. The geometry and asymptotic proofs are given in the report; finite quadrature cannot certify them.

No Monte Carlo estimate, numerical fit, build status, or preservation count is treated as a proof of the full manuscript.

## Primary literature keys

Records were checked on September 15, 2026. This is a targeted scope/attribution check, not an exhaustive priority search or a fresh verification of the external proofs.

**L1.** Gerhard Osius, *Asymptotic inference for semiparametric association models*, arXiv:0903.0702. Primary record: <https://arxiv.org/abs/0903.0702>. Used only for the established odds-ratio association framework with unrestricted marginals.

**L2.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983. Primary record: <https://arxiv.org/abs/2510.18983>. Used for its enriched marked-length datum and finite-horizon setting, not to assert equivalence with the present boundary-law inverse.

**L3.** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890. Primary record: <https://arxiv.org/abs/1905.00890>. Used for the different analytic open-billiard observation setting and scope.

**L4.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5. Primary record: <https://arxiv.org/abs/2010.04120v5>. The version-specific record expressly explains removal of a geometric spectral-rigidity assertion affected by an error. The report does not claim that this removed assertion remains valid.

## Review disposition and write scope

The only intended repository additions are this new review directory and its report, audit record, two scripts and two JSON records. The manuscript, author responses, prior reviews, default branch and branch-protection settings are not modified by the review. The report does not approve a pull request or merge any author revision. Its mathematical nonfatal findings and its negative highest-journal placement recommendation are separate judgments.
