# A2 v47 review: source register, coverage, and reproduction

This document accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). All manuscript references are frozen. A successful finite check, a source hash, and a successful TeX build are different kinds of evidence; none is a formal mathematical certificate.

## 1. Frozen review target

Repository: `TrillionniumFoundation/theta-theory`.

- Reviewed branch: `revision/a2-v47-review-ready-2026-09-14`.
- Reviewed snapshot: `eb384575c6d21d5a5d6b59d06d9a3057935a1844`.
- Actual compiled mathematical source: `219b39e94b14187561dc3b7e5bdbae49dbd92cc2`.
- Source-prefix tree recorded in the build report: `1e06cf3bd9e5b31ca9a0e623f3ecae3ee306c9a6`.
- Workflow preparation: `344905675ef544080e9d7139d31aa50abdd5f111`; this is not represented as the compiled source.
- Native run `34843699559`, attempt 1, artifact `10347280538`.
- Published product head: `ec4d6faa66a96d6242fbb18138071919b267482c`.
- New review branch: `review/a2-v47-independent-harsh-top4-2026-09-14`, created from the reviewed snapshot, not from the older default branch.

The preceding report is frozen at `45b42eee377c7fd3cff81c24c95acb91d6f46ab6`; its reviewed mathematical source was `ab99196fadc20682c1ee44d6bb433a788c7274ab`. The final v47 main has 248 pages, not the preceding 243. Its companion has 7 pages. The historical source-directory name `A2-v17-boundary-information-coarsening` does not denote the revision number.

## 2. Primary repository sources

**S01 — Complete manuscript, introduction, and architecture.**

[Main source at the compiled commit](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/main.tex); [new introductory module](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/01h_calibration_overview_v47.tex).

[Complete 248-page native main](https://github.com/TrillionniumFoundation/theta-theory/blob/eb384575c6d21d5a5d6b59d06d9a3057935a1844/deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/main.pdf); [complete 7-page native companion](https://github.com/TrillionniumFoundation/theta-theory/blob/eb384575c6d21d5a5d6b59d06d9a3057935a1844/deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/two_collision.pdf).

**S02 — Author response and historical audit.**

[RESPONSE_TO_REFEREE_V47.md](https://github.com/TrillionniumFoundation/theta-theory/blob/eb384575c6d21d5a5d6b59d06d9a3057935a1844/papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V47.md); [HISTORICAL_DERIVATION_AUDIT_V47.md](https://github.com/TrillionniumFoundation/theta-theory/blob/eb384575c6d21d5a5d6b59d06d9a3057935a1844/papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V47.md).

These were read as the author's account, not adopted as independent verification.

**S03 — Complete new mathematical module.**

[article/23l_calibrated_histograms_v47.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/23l_calibrated_histograms_v47.tex).

Fresh audit: entire module, Sections 19.7–19.9, native pages 94–97. It contains Lemmas 19.7–19.8, Theorem 19.9, and Corollary 19.10. Equation (19.21) is the normalized density; (19.24) the grid-tube bound; (19.27) amplified offset error; (19.29) calibrated bias; (19.30) the confidence radius; and (19.32)–(19.34) the grid, pilot, and sample choices.

**S04 — Inherited quantitative inverse and its sampling interface.**

[article/23k_quantized_law_stability_v46.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/23k_quantized_law_stability_v46.tex).

Fresh examination: quantified observation class, histogram-to-fixed-jet estimate, finite Bellman recursion, finite-order analytic continuation, finite-witness registration, accuracy prescription, sampling/selection/cap proof, and the calibration clarification adjacent to (19.19), page 92. No fresh independent cubic/quartic Bellman symbolic implementation is claimed in this round.

**S05 — Physical sensor, same-flight pilot, and observable projection.**

[article/25a_common_observables_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/25a_common_observables_v25.tex).

Fresh examination: physical record and calibration contract, onset localization, positive success bound, finite time-grid pilot, same-final-flight gap error, projection error, and the offset/chart transfer argument. This is a position-sensor result, not histogram-only chart discovery.

**S06 — Explicit single-offset density inverse.**

[article/23f_single_offset_law_inverse_v42.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v42.tex).

Fresh examination: source lines 1–250, especially the anchored four-density identity, signed action recovery, geometric quadratic recovery, and the finite-flight normalization interface. This does not independently re-prove the full relative-operator machinery on which that interface relies.

**S07 — Smooth finite-jet factorization.**

[article/23a_signed_endpoint_rigidity_v27.tex, lines 298–410](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex#L298-L410).

Fresh examination is restricted to this functional-remainder proof: graph interpolation, differentiated stationary actions, terminal-term control, summable passage to the limit, and the implication for finite jets. No independent reconstruction of every preceding weighted Banach-space estimate is asserted.

**S08 — Geometric finite-channel skeleton.**

[article/23j_generic_finite_channel_rigidity_v45.tex, lines 1–230](https://github.com/TrillionniumFoundation/theta-theory/blob/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/papers/A2-v17-boundary-information-coarsening/article/23j_generic_finite_channel_rigidity_v45.tex#L1-L230).

Fresh examination: blocked-segment splitting, finite clear-channel paths, finite quotient/gain construction, spanning tree plus two independent cycle gains, and persistence at the indicated interface. The later generic-asymmetry proof is not newly certified in full. The quantitative registration used by v47 was examined in S04.

**S09 — Preceding independent report.**

[REFEREE_REPORT.md for v46](https://github.com/TrillionniumFoundation/theta-theory/blob/45b42eee377c7fd3cff81c24c95acb91d6f46ab6/reviews/a2-v46-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md).

Its favorable findings, minor calibration clarification, and adverse placement judgment were distinguished. Earlier findings were not treated as formal certification or silently reclassified as current defects.

**S10 — Delivery and source evidence.**

[Final review ledger](https://github.com/TrillionniumFoundation/theta-theory/blob/eb384575c6d21d5a5d6b59d06d9a3057935a1844/papers/A2-v17-boundary-information-coarsening/REVIEW_READY_V47.md); [retained delivery directory](https://github.com/TrillionniumFoundation/theta-theory/tree/eb384575c6d21d5a5d6b59d06d9a3057935a1844/deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2); [actual source commit](https://github.com/TrillionniumFoundation/theta-theory/commit/219b39e94b14187561dc3b7e5bdbae49dbd92cc2).

Independent checks cover the downloaded native artifact, its 34 evidence entries, and the 103 unique active source inputs. They do not purport to reconstruct or independently re-fetch the entire repository tree.

## 3. External primary literature

Checked on September 14, 2026. This is a targeted comparison, not an exhaustive priority search.

- **L1:** Finamore–Leguil, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983), v1, October 21, 2025. Rigidity for finite-horizon Sinai billiards uses an enriched marked length spectrum. It must not be identified with the selected endpoint-law observation without a proved reduction.
- **L2:** Florio–Leguil, [arXiv:2010.04120](https://arxiv.org/abs/2010.04120), especially the v5 notice dated June 3, 2021. The notice distinguishes the removed earlier geometric spectral-rigidity assertion from the retained dynamical conjugacy results. The abstract/version notice and the first PDF page were checked.
- **L3:** L. N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT Numerical Mathematics 60 (2020), 901–915, [arXiv:1908.11097](https://arxiv.org/abs/1908.11097), DOI `10.1007/s10543-020-00802-7`. Relevant context for conditional continuation and its ill-conditioning, not a substitute for S04's proof.

## 4. Independent implementation and negative controls

[Independent script](independent_checks.py) imports no author diagnostic. Its finite mathematical checks use explicit failures rather than Python assertions, so optimization cannot remove the checks. The finite part uses the Python standard library; the optional whole-document reproduction comparison uses PyMuPDF.

| Check | Scope and result |
|---|---|
| Positive-offset quadratic-cap TV | 300 exact rational identities; passed. |
| Amplified timing control | Actual TV 1/201 versus 1/20001 if the flight multiplier were wrongly omitted. |
| Grid-tube area | 500 exact rational comparisons of the exact area and printed upper bound; passed. |
| Grid refinement | Explicit column-pairing maps have displacement 1/q tending to zero and categorical L1 equal to one. |
| Outer edges | A shifted unit-square law gives L1 equal to 2r through an outer edge alone. |
| Mass on an edge | A strip collapsed onto a half-open cell edge obeys the coupling bound despite a singular image component. |
| Joint budget | Exact synthetic gap, mesh, finite-flight, offset, chart, and selector budget; passed. |
| Samples and caps | Direct arithmetic checks of the stated sufficient choices; passed. |

These examples are functional controls for the error estimates, not claimed periodic billiard realizations or counterexamples to the manuscript. The displayed cost orders in the report are deductions from sufficient prescriptions, not minimax lower bounds.

The independent ordinary and optimized executions produced byte-identical JSON. Their retained combined result is [CHECK_RESULTS.json](CHECK_RESULTS.json).

The author's `tools/check_revision_v47.py` was separately rerun under ordinary and optimized Python; those outputs were identical. The retained [AUTHOR_DIAGNOSTICS.json](AUTHOR_DIAGNOSTICS.json) is explicitly author-code output. It reports 101 inherited active files, 99 unchanged in place, two exact archived originals with prescribed amendments, two new active modules, and preserved inherited input order. Its environment counts aggregate the active inputs of the main and companion; they should not be silently described as main-only counts.

Other historical diagnostic outputs in the native bundle were verified as evidence bytes. That verification is not a claim that every historical script was newly executed.

## 5. Native rebuild and PDF inspection

The complete source ZIP was extracted into an isolated directory. The companion was built first, followed by the main. Both latexmk invocations completed successfully with shell escape disabled. The main has five underfull-box notices, no overfull-box notice, and no unresolved citation/reference notice. The epstopdf warning about disabled shell escape is expected under this build policy. It is not concealed under a claim of a warning-free build.

All 255 pages were compared between the native and separately rebuilt products in extracted text and in pixels from the same PyMuPDF renderer at 72 dpi. Every comparison matched. PDF bytes did not match and are not asserted to do so.

Individual readable-resolution visual inspection covered main pages **92, 94, 95, 96, and 97**, rendered at approximately 101 dpi. No clipping, overlap, or broken mathematical layout was observed there. Other rendered files and whole-document pixel comparisons are not counted as individual visual inspections.

| Object | SHA-256 |
|---|---|
| Downloaded native artifact ZIP | `90d5894ff1761d3260cc2299ed3f66a3229d763d2a61ecf0ead2ca238ccb7458` |
| Native source ZIP | `ca80bc70d16a81decbb840a1d771ed79be8ac8d28bef0130175c7dab1f56261e` |
| Native main, 248 pages | `622ac0d72dc6c6c460d3aaf4375de424a0aff2279d77a306abc1a9c8e14678e5` |
| Independently rebuilt main | `b5364a9e99e7f3a354a5d4ba64daa93855ddfbfd822d815d5187109e4a7731cc` |
| Native companion, 7 pages | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Independently rebuilt companion | `7dc3284777c6e53fd0a04c19d970db11499d25b244035f8798f80931f35f40f2` |

## 6. Reproduction commands

From a checkout of this review branch, with Python, PyMuPDF, the author's Python dependencies including SymPy, and the manuscript's TeX dependencies installed:

```bash
set -eu
REVIEW="$PWD/reviews/a2-v47-independent-harsh-top4-2026-09-14"
DELIVERY="$PWD/deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2"
WORK="$(mktemp -d)"
mkdir -p "$WORK/source"
unzip -q "$DELIVERY/native-source.zip" -d "$WORK/source"
cp -a "$WORK/source/source" "$WORK/rebuilt"

(
  cd "$WORK/rebuilt"
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
)

python "$REVIEW/independent_checks.py" \
  --native "$DELIVERY" --source "$WORK/source/source" \
  --rebuilt "$WORK/rebuilt" > "$WORK/independent-normal.json"
python -O "$REVIEW/independent_checks.py" \
  --native "$DELIVERY" --source "$WORK/source/source" \
  --rebuilt "$WORK/rebuilt" > "$WORK/independent-optimized.json"
cmp "$WORK/independent-normal.json" "$WORK/independent-optimized.json"

python "$WORK/source/source/tools/check_revision_v47.py" \
  > "$WORK/author-normal.json"
python -O "$WORK/source/source/tools/check_revision_v47.py" \
  > "$WORK/author-optimized.json"
cmp "$WORK/author-normal.json" "$WORK/author-optimized.json"
```

The optional `--archive PATH` argument records the SHA-256 of the downloaded Actions ZIP; the permanent delivery directory is sufficient for the other checks. A fresh build can have different PDF byte hashes while still matching all extracted text and same-renderer pixels. The independent finite checks alone can be run with `python independent_checks.py`, without an archive or PyMuPDF.

## 7. Boundaries of the conclusion

The new v47 module has been subjected to a fresh targeted proof audit. The specified inherited interfaces have also been examined. The full native products have been reproduced, and their source/evidence identities checked as described above.

This is not a line-by-line fresh review of every inherited proof, a proof-assistant certificate, a sensor-noise theorem, a sharp complexity result, or exhaustive literature clearance. The report's adverse journal-placement recommendation is an explicitly identified evaluative judgment. The review branch adds review documents and diagnostics only; it does not amend the manuscript to manufacture agreement with that judgment.
