# A2 v67 — post-download visual and mechanical checks

Date: September 16, 2026. Compiled source: `97b0c5bf15d6581c42b0f503bbe902c9d89b42db`. Native artifact: `10437417575`, workflow `35074257415`, attempt 1. The native PDFs are those retained under `deliveries/a2-v67/97b0c5bf15d6581c42b0f503bbe902c9d89b42db/`.

## Mechanical comparison

The downloaded native artifact digest was checked against GitHub's reported SHA-256. The 47 build-report evidence entries and 855 frozen source files were verified by lengths and hashes; source Git blob identities and recorded modes reconstructed the complete manuscript tree `5ba7cc8f87aaadd2e3f734c41bb030668e15cff7`. The frozen file bytes match the intended local manuscript used in a separately completed native build.

All 151 principal, 326 full and seven companion pages were compared with those local PDFs in extracted text and in RGB samples rendered by the same PyMuPDF renderer at 72 dpi. Every comparison agrees. This checks all 484 pages mechanically. It does not assert that the PDFs from different runs have equal bytes, that all pages were individually inspected visually, or that their mathematics has been formally verified.

## Targeted visual inspection of the downloaded native PDFs

Native pages were rendered at 90 dpi (PDF scale 1.25). Individual pages and labelled contact sheets were inspected for line overflow, clipped formulae, overlaps, missing glyphs and the layout of the changed argument.

- Principal article: pages **1, 2, 3, 4, 47, 49, 50, 51, 90 and 151**. This covers the new abstract and synthesis, Theorem 1.1, the residual bound, corrected Proposition 10.4, its explicit recursion and propagation proof, the principal underfull notice location, and the final bibliography.
- Full manuscript: pages **1, 3, 4, 14, 50, 247, 292, 325 and 326**. This covers the full entry's abstract, opening and leading theorem, the displayed finite-iteration correction and recursion, all four full-manuscript underfull-notice locations, and the ending bibliography.

No clipping, overlapping text, black replacement squares or broken glyphs was observed on these inspected pages. The principal p. 51 proof ends normally and is followed by the retained relative-law argument. The bibliographies retain readable identifiers and report attributions; they are not described as journal-commissioned decisions.

The companion is included in the complete mechanical comparison and final-log check; no new manual page-by-page visual certification of that unchanged manuscript is claimed here. These statements distinguish rendered-page inspection from text extraction and all-page parity.

## Final log diagnostics retained

The final native logs contain no overfull-box, undefined-reference/citation, missing-character or LaTeX-error diagnostic. There is **one principal underfull notice** and **four full-manuscript underfull notices**; the companion has none. The affected principal p. 90 and full pp. 14, 247, 292 and 325 were visually inspected. No clipping or unreadable text was found there. These notices are recorded rather than suppressed or relabelled as a warning-free build.

## Reproduction route and limits

The actual source includes `tools/build_revision_v67.py`, `tools/check_revision_v67.py` and `tools/retain_native_v67.py`. The versioned native workflow records the exact activation, build, retention and fetched-object verification steps. The complete delivery retains the source ZIP, final auxiliary files, recorder inputs, logs, tool versions, build report and normal/optimized diagnostic outputs. The final auxiliary files provide the printed page numbers used in the review-ready index.

Compilation, source retention, finite exact-arithmetic controls, render parity and targeted layout inspection have different scopes. None is a substitute for an external mathematical proof review or an editorial assessment of exceptional significance.
