# A2 revision 142 — native mathematical revision

**Intrinsic reconstruction from nonreduced failure schemes** — Qian Qi — 24 September 2026.

Read `geometry.tex` / `geometry.pdf` for the principal article, `supplement.tex` / `supplement.pdf` for the full technical supplement, and `complete.tex` / `complete.pdf` for both proof networks. Native sources require no transport decoding or unpublished manuscript.

## Exact baselines

The controlling v141 review is commit `a10f8f1ea938e0ef8ce5a4aca4ee8e4a662ee84c`, assessing restoration-only head `bf0d9be9e2624058d24a57c48b19ec4c38105c1f`. After that review, the v141 branch advanced to substantive native manuscript `8cd389f4048a1047be9aa8e8e4f642595175a555`. This revision retains that later manuscript in full, including its universal spectral family and totally real likelihood theorem. It does not revert to the older reviewed state.

The predecessor artifact came from run 35872058050, artifact 10755263912. ZIP SHA-256: `4da8b77eb6a79f5d65ad5e84c7c8581b3e8d9f0138321d81605ac609157a6a92`; its publication-commit receipt equals the pinned native head. Original review and revision branches remain unchanged.

## New mathematical content

`parts/24-jacobian-casimir.tex`: mixed Jacobian–contraction identity at every rank, direct singular-kernel proof, exact Casimir Gram identity, complete normalized singular-value spectrum and Moore–Penrose inverse.

`parts/25-fixed-spectral-strata.tex`: fixed-discriminant/fixed-reduced-rank classification, necessary and sufficient dominance criterion for fixed-form curve specializations, all allowed transitions realized by flat actual finite-neighbourhood families, and sharp detection at the same order. The first relation is the degree-d first graded Betti space on a marked Hilbert locus. Classical orbit classification is explicitly credited.

`parts/01d-operator-strata-overview.tex` and `parts/01e-dependency-map.tex`: theorem overview and dependency map. Every inherited mathematical part and check is retained byte-for-byte; changed wrappers are archived in `history/v141/`. The inherited bibliography is preserved and extended by `references-v142.tex`.

## Referee and build objects

Read `RESPONSE_TO_REFEREES_V140_V141.md`, `ISSUE_MATRIX.json`, and `LITERATURE_AUDIT_V142.md` for the issue-by-issue response and source comparisons.

Run `bash build.sh` with Python 3, SymPy, NumPy, PyMuPDF and TeX Live (AMS, Latin Modern, microtype, xr-hyper, hyperref). All seventeen inherited scripts plus the new regression suite run before three PDF builds and the source/layout audit. In an isolated local copy, set `A2_PREDECESSOR_DIR` to the pinned v141 directory for nondeletion checks; in the repository it is found automatically.

Actual results and the exact mathematical source commit appear in `evidence/BUILD_RECEIPT_V142.json`; the same audit creates `PROVENANCE_MANIFEST_V142.json` and `NONDELETION_V142.json`. A receipt labelled `local-preflight` is not a remote green run. Inherited receipts describe their own earlier versions only.

The full Ballico 1993 article has not been obtained and exhaustive historical priority has not been certified. These documentary items are not marked closed. No theorem is weakened on that account; no passing script constitutes formal proof or editorial acceptance.
