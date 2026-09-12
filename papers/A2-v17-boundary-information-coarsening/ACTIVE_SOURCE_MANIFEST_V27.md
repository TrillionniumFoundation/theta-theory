# A2 v27 active source and preservation map

Date: September 12, 2026. Branch: `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`.

## Exact source provenance

Review base: `a5b2d4b5a9ed31059e16e5011c8010579d713598`. Reviewed v26 manuscript: `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`.

The complete v27 mathematical source is committed at `416124f13f182f8e2d876f93090865f13269c86b`, repository tree `da8779b9c2a7352486931a64252752f3c6eae0b5`. This snapshot contains every inherited source, not merely the files below. Later verification/navigation commits preserve its native TeX bytes.

The stable paper directory is `papers/A2-v17-boundary-information-coarsening`. Its native entry points are `main.tex` and `two_collision.tex`. The directory name is not a version claim.

## Active replacements and addition

| Historical source, preserved | Active source | Change |
|---|---|---|
| `article/01_introduction_v26.tex` | `article/01_introduction_v27.tex` | Propagate observed-type dichotomy and smooth finite-jet argument; retain main theorem statements |
| `article/23a_signed_endpoint_rigidity_v22.tex` | `article/23a_signed_endpoint_rigidity_v27.tex` | Finite Taylor remainders; arbitrary smooth-remainder factorization; retain the complete signed inverse |
| `article/18f_domination_and_position_comparison_v26.tex` | `article/18f_domination_and_position_comparison_v27.tex` | Exact record definitions; maximal varying-type deficiency; fixed-type equivalence; explicit disk witness |
| No replaced source | `article/23g_density_support_distinction_v27.tex` | Scoped functional support-preserving example after the unchanged single-offset inverse |

The original three source files remain in the tree but are not additionally compiled into the active article. Their old theorem labels are carried by the corrected sections, avoiding competing active versions.

## Verified new native Git blobs

| File | Git blob |
|---|---|
| `main.tex` | `2133039c3a220a923b232db9f1c5a5661938773c` |
| `article/01_introduction_v27.tex` | `14e5fe4a23f833c6caa581bbe055d0efe73650b6` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `article/23g_density_support_distinction_v27.tex` | `94064ab1f9be56218d30db5de736a85cec427694` |

The source bytes tested locally match these Git blobs. The signed-rigidity file omits a final newline; this has no mathematical or TeX effect and is included in the byte-level hash.

## Unchanged central sources

The single-offset law inverse `article/23f_single_offset_law_inverse_v26.tex` remains active with blob `35f538eea4415951d1572cd9db76fdff429afa0a`. The historical full signed inverse remains at blob `facc0674006967debca05ab4196002e8a7f5b886`.

The companion `two_collision.tex` remains at blob `df44402b17031525c087d39dfedf8dac3ada611d`. The preamble remains at `7e0de97c08dd2e12187193aff89f3ca4712f430f`. The full native build utility remains at `233b6f37ff4912b99793460634983ac9b8da379b`.

The relative law, finite geometry and integration, boundary layers, operator comparison, uniform hyperbolic margins, physical experiment transfer, analytic continuation, intrinsic gluing, rank-two lattice recovery, finite-signature stability, short-flight benchmarks, same-experiment direct-position benchmark, Gaussian and Poisson information, count quotient, Abel and deautoconvolution results, observable calibration, global single-offset reconstruction and compatible variation bundles all remain active through the original ordered inputs.

## Complete auxiliary material is retained

`article/99_auxiliary_compendium_v19.tex` is unchanged at blob `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e`. Its 36 literal direct inputs remain active: nonlinear information; contact rigidity; finite-jet stability; profile/Abel acquisition and calibration; critical, adaptive-critical, random-hazard and supercritical experiments; inverse and pairwise inverse calculations; three-amplitude and fixed-offset recovery; joint minimax; smooth remainder and envelope minimax bounds; observable comparisons; self-calibration; coalescence; measurable reconstruction; count-only acquisition and lower bounds; fixed-bracket acquisition; marked and record-response results; circular calculations; flux, geometry, threshold, record and consequence proofs.

`v5/references_v25.tex` remains the active bibliography. No historical mathematical file, companion source, auxiliary module, review report, or bibliography key is deleted in this revision.

## Navigation preservation

The old repository and paper README blobs are copied without modification to `README_PRE_V27.md` at the repository root and in the paper directory, respectively. Their Git blobs are `bfeb2f5c53bb571a0ee778818d42768fb66baaf6` and `f8375a6309564b4203b0ace8c53ad9899603a6b6`. New entry pages identify v27 while retaining direct access to every former index.

## Audit boundary and reproducible full audit

`diagnostics/v27-changed-source-audit.json` records the executed **changed-source** check: 32 old signed-inverse labels and nine old introduction labels are preserved; main has 48 direct inputs rather than 47; exactly three inputs are replaced and one added; all other direct inputs retain order. This is not an executed recursive scan of the entire inherited article.

`tools/audit_native_sources_v27.py` performs the requested complete literal input scan of both native entry points from a full checkout. It records every visited file's bytes, SHA-256 and Git blob, every input edge, labels, citations, bibliography keys and the prefixed companion references. Missing files, input cycles, unresolved literal references/citations and duplicate labels/keys fail the audit. As a literal scanner it does not replace the TeX engine.

`tools/build_submission.py` then builds both complete entry points, including every active appendix and bibliography, with native logs and PDF metadata. `VERIFICATION_V27.md` states whether these commands actually executed. The existence of either script or this source map is not a successful native build certificate.
