# A2 — uniform collision-threshold laws and marked response

**Author:** Qian Qi. **Revision date:** September 9, 2026.

**New branch:** `revision/a2-uniform-collision-thresholds-2026-09-09`.

**Controlling review:** `50e2bd898e3168d43f1519729a0d88ccbc03946a`,
`reviews/a2-two-collision-harsh-independent-2026-09-08/REFEREE_REPORT.md`.

**Reviewed manuscript:** `e8d3b658ead4996dabfc9f31a07b812e070f5446`,
`workstreams/2026-09-08-next-step/research/A2_Two_Collision_Response.tex`.

## Publication object

`main.tex` is a complete new 14-page English article, **Uniform collision-threshold laws and marked response in a periodic Lorentz gas**. `two_collision.tex` is the complete, unchanged 7-page reviewed article, supplied as a separately compilable companion. Its 20,663 bytes have Git blob `df44402b17031525c087d39dfedf8dac3ada611d`. No inherited theorem, derivation, source range or radius interval is deleted or weakened.

The new main result treats every collision order j on any fixed compact radius interval inside (0, 1/2). It gives a common threshold collar, explicit exponentially decaying coefficients, a relative error uniform in j, source-dependent derivative bounds summable in j, and the joint onset record including physical sampling-time cuts. The coefficient hierarchy distinguishes actual specular correlations from independent roofs with the identical marginal and determines the normal period-two multiplier.

The exact original two-collision result remains valid in its original R and T ranges. It is not relabelled as a proof of the new theorem. The new uniform extremal theorem is also not relabelled as the historical unrestricted long-time mixed Edgeworth theorem. `SUBMISSION_INDEX.md` fixes the separate publication objects and their logical statuses.

Read `RESPONSE_TO_REFEREE.md` for TC-R1--TC-R4 and the minor points. `PROOF_LEDGER.md` identifies the new analytical steps, inherited inputs and scope boundaries. The complete controlling report and historical Round 33 chapter are preserved as exact Git objects in the repository's new directory; their immutable identities are also in `history/SOURCE_PINS.json`.

## Reproduction

From this directory, with Python 3.10+, NumPy, SciPy and TeX Live:

```sh
python tools/build_native.py
python tools/verify_thresholds.py > /tmp/a2-threshold-checks.json
python -O tools/verify_thresholds.py > /tmp/a2-threshold-checks-O.json
cmp /tmp/a2-threshold-checks.json /tmp/a2-threshold-checks-O.json
```

The native builder compiles both full documents without shell escape. It checks actual auxiliary-file convergence, final references and citations, overfull boxes, and agreement of the TeX recorder with the declared source closure. The current build has 14 main pages and 7 companion pages, with no final unresolved-reference or overfull-box warnings. Source hashes, execution facts and PDF hashes are in `verification/NATIVE_BUILD.json`; the full stdout logs accompany the downloadable native package.

The new diagnostic program passes 411 explicit checks in ordinary and optimized Python with identical output. It separates 141 exact rational checks from 270 non-interval floating checks. Physical reflection and relative-flux stress tests reach j=128; numerical quadrature tests the onset coefficient for j=1,2,3,8. These are finite diagnostics, not a proof of the continuum uniformity. The full analytical arguments are in the main article. No formal proof assistant, exhaustive priority search, unrestricted long-time operator estimate, or journal acceptance is claimed.

Historical reports, previous branches, the statistical A1 line and the B2 workstream are unchanged. This branch is submitted for a new independent assessment of the new mechanical theorem.
