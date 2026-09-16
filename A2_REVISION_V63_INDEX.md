# A2 revision 63 — next-review index

September 16, 2026. **Complete source and native products are committed**, not merely staged for a future build.

## Fixed identities and branches

| Item | Identity |
|---|---|
| Review addressed | `review/a2-v62-independent-harsh-top4-2026-09-16` at `a568573d1d4a5d976f6db3c54122d97c769acd38` |
| Reviewed v62 mathematical source | `037c80dc44d8191e6f808591ea0651e813234d06` |
| New mathematical source | `f5517519440b897707ddc60deeafba19e86bb5a5` |
| New manuscript Git tree | `b042811c7ceb2c5fd841b2a03ab0b8c232c39dce` |
| Source branch | `revision/a2-v63-referee-response-2026-09-16` |
| Native-products branch | `revision/a2-v63-native-products-35050788011-1`, verified head `869d9ad65f80b17847db09aac8b499600efcf31d` |
| Next-review branch | `revision/a2-v63-review-ready-2026-09-16` |
| Native workflow | [35050788011](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/35050788011), attempt 1; native and publication jobs both successful |
| Retrieved native artifact | `10428569064`, SHA-256 `2a2c8d78236274484f1fd3ff6ba905a01ee4eab4c0c2d60e363c5b9670af79ba` |

The review-ready branch descends from the verified native-products head. Its final additions are navigation and verification records outside the manuscript subtree; the mathematical source and native PDFs remain exactly those identified above.

## Complete manuscripts

| Entry | Pages | Source and native PDF |
|---|---:|---|
| Principal journal article | 125 | [rigidity.tex](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [rigidity.pdf](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/rigidity.pdf) |
| Complete technical manuscript | 301 | [main.tex](papers/A2-v17-boundary-information-coarsening/main.tex) · [main.pdf](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/main.pdf) |
| Two-collision companion | 7 | [two_collision.tex](papers/A2-v17-boundary-information-coarsening/two_collision.tex) · [two_collision.pdf](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/two_collision.pdf) |

All three PDFs are retained in the same delivery directory, including the full technical PDF used by the principal article's external references. The [native source archive](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/native-source.zip) contains the complete 784-file frozen source and its manifest. Its SHA-256 is `e819269bdbf65d38da8369ae9f8aa180aa6422d7b6bea69db6706336b7c09691`.

PDF SHA-256 identities:

- Principal: `ca9a511514f821ae6bfbbd2b54b45668a5c1ab480c8d802d49e22cf3bb2bc75f`.
- Full: `95778e360fd784650ce8b1c31171e10593c66e6d70d843d0c9b2ff8070ddbb39`.
- Companion: `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1`.

## What changed in the mathematics and presentation

**R62-m1 / D2.** The proof of `cor:v62-total-budget` now retains the pilot-grid ceiling explicitly. With `q=j(g_+-g_-)/epsilon` and `L_grid=ceil(q)+2`, the new identity is

\[
t_{L_{\mathrm{grid}}}-jg_+=(\lceil q\rceil-q+2)\varepsilon\in[2\varepsilon,3\varepsilon).
\]

Thus all programmed pilot times are strictly below `jg_+ + 3 epsilon`. The successful stopping event still has its sharper `2 epsilon` bound; failed histories are not bounded by that event-specific estimate. The deterministic cap already counts every grid point. Both confidence exponents and the evolution-time order remain unchanged. The correction is equation (13.24), on principal p. 69 and full-manuscript p. 70. The notation `L_grid` avoids collision with the preceding logarithmic budget quantity.

**R62-E2.** One shared comparison is included in the existing introductory literature discussion of both manuscripts: [article/00d_orbit_local_comparison_v63.tex](papers/A2-v17-boundary-information-coarsening/article/00d_orbit_local_comparison_v63.tex). It credits orbit-local all-order spectral recovery, states the scope of Zelditch's published Theorem 1.1 and contrasts the observation maps and relative normalization. It distinguishes the proved internal leading-data separation from any unproved information ordering relative to a full spectrum or marked-length datum. Both bibliographies add the published Annals reference; no inherited item is removed. Locations: principal pp. 9–10, full p. 10; final bibliography pages 125 and 301.

**R62-M1--M6 / S1 / E1 / D1--D4.** The [point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V63.md) addresses normalization, realizability, random counts, estimator existence versus computation, both confidence powers, pilot charging, exact scope, significance and verification. The contribution case is centered on the relative-action mechanism and actual-smooth two-contact inverse rather than another framework or an accumulation of statistical corollaries. The existing complete-germ target and all geometric conclusions remain. No new main theorem is claimed for this corrective/comparative revision.

[Cover letter](papers/A2-v17-boundary-information-coarsening/COVER_LETTER_V63.md) · [Historical derivation audit](papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V63.md) · [Primary-literature check](papers/A2-v17-boundary-information-coarsening/LITERATURE_CHECK_V63.md) · [Dependency ledger](papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V63.md).

## Preservation, checks and reproduction

The [v63 checker](papers/A2-v17-boundary-information-coarsening/tools/check_revision_v63.py) passes in ordinary and optimized Python with identical output. It verifies all 767 inherited paths, all original executable modes, 759 byte-identical inherited files and byte-exact archived originals of the eight modified paths. All 126 inherited active inputs remain; one shared comparison brings the total to 127. All five finite-experiment statement bodies are unchanged. The inherited bibliography counts of 19 and 48 are preserved before the single addition in each list. Exact rational controls include 720 grid configurations, 366 fractional-grid counterexamples to the former literal bound and 48 confidence-balance configurations. The referee's `308/101 > 307/101` example is reproduced.

The [frozen baseline manifest and originals](papers/A2-v17-boundary-information-coarsening/history/v62-review-baseline/) identify the comparison bytes. No mathematical source, prior review, A1 file or earlier delivery was deleted.

Native compilation used the retained immutable-Git-source builder, the same three complete entry points and the existing adaptive/v32/v38 controls. The main and principal builds consumed source-matched producer auxiliaries. All native checks passed. No unresolved citation/reference, duplicate label/destination, missing glyph or overfull box was reported. The full manuscript retains three underfull-vbox warnings; they are recorded rather than suppressed. The native principal and companion logs have no reported warnings.

The separately retrieved artifact was independently checked against all 784 local source files and modes. All 433 pages have exact text and 72-dpi rendered-pixel equality with the verified local build. Selected final local pages were visually inspected at 120 dpi: principal 1, 9, 69 and 125, and full 10. The pixel comparison transfers that layout identity to the published PDFs; it is not a claim of visual inspection of every page.

Evidence: [independent retrieval record](A2_V63_INDEPENDENT_DELIVERY_VERIFICATION.json), [build report](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/build-report.json), [post-push Git-object check](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/COMMITTED_OBJECTS_VERIFIED.json), [native preservation controls](deliveries/a2-v63/f5517519440b897707ddc60deeafba19e86bb5a5/check_revision_v63-normal.json), and all raw logs in the delivery directory.

From a fresh checkout of the fixed source commit, run:

```sh
python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v63.py
python3 -O -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v63.py
python3 -B papers/A2-v17-boundary-information-coarsening/tools/build_revision_v56.py --output-dir /tmp/a2-v63-native-rebuild
```

The build directory must be absent or empty; the documented TeX and scientific-Python dependencies are installed by the pinned workflow. The retained builder's historical filename does not identify the manuscript version: its report, source commit and source tree do.

## Scope of the next assessment

The revision maintains the intended general-journal submission. The latest report's significance assessment is answered with a focused mathematical comparison, not declared overturned by arithmetic correction or CI success. Source hashes, finite controls, compilation and selected layout checks are not proofs of every theorem or a guarantee of acceptance. The full manuscripts and the exact response are now available for the next referee to assess on their merits.
