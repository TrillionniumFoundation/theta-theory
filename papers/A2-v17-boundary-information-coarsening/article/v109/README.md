# A2 revision 109: single-contact multiplication tomography

## Review entry points

`paper.tex` is the self-contained principal manuscript, **Single-contact recovery of information metrics through polynomial multiplication**. The complete retained companion is `../v108/paper.tex`, with all four `../v108/prepared/*.tex` inputs now included in the source tree. Neither the companion nor any earlier mathematical source is deleted or silently rewritten.

Read `RESPONSE_TO_R108.md` for the point-by-point response and `DEPENDENCIES.md` for the theorem dependency and preservation map. The controlling report is `reviews/a2-v108-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md` at commit `5a8a8190e6a5979719591b286fca92aae3cc15cc`; its reviewed mathematical source is `4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191`.

The new result uses one normal space, not the entire conormal bundle. For all d >= 2 a constructive family with k = 3d+2 makes the native inverse metric identifiable at a single positive contact point, while unrestricted metrics retain 5d(d+1)/2 invisible directions. The exact fibre is the annihilator of the normal-polynomial product space. Stability and a finite noisy contact-value experiment are proved separately from the exact-real scalar oracle statement. Standard discriminant geometry, Hankel duality, Gaussian LAN, and real quantifier elimination are explicitly attributed.

## Reproduce

From the repository root, with Python 3, SymPy, a TeX Live installation including amsart/lmodern, latexmk, and Poppler installed:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v109/verify.py
```

The verifier checks every source byte against the exact Git HEAD, verifies the four preparation input/output hashes, verifies unchanged inherited TeX against the review commit, runs the v109/v108/v107 diagnostics and the unchanged independent referee script, and builds both volumes. It rejects missing inputs, undefined or multiply defined references, remaining label rerun warnings, and overfull horizontal boxes. A successful receipt records source commit, manifest hashes, PDF/log hashes, compiler, check counts, and the workflow URL when run in Actions. Evidence is committed separately from source.

To build just the principal source:

```sh
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error article/v109/paper.tex
```

A downloaded source bundle without Git history may use `verify.py --allow-partial`. This mode still builds and checks both volumes, but writes `local-verification.json` with `source_bound: false`. It is never represented as a GitHub Actions success or a source-bound Git checkout.

## Evidence interpretation

`evidence/verification.json`, when present, is the authoritative source-bound build receipt. `evidence/local-verification.json` is an explicitly unbound local replay. Do not infer a successful build from a workflow definition or a queued run. Finite diagnostics are not universal proof certification and do not establish journal-level novelty.

The earlier v108 native run `35553783129` succeeded with 58 pages at its materialized source commit `9affc52cc4eb62e5c14cffb564b380b86503aec2`, not at the unmaterialized reviewed commit. The difference between those two commits consists only of the four prepared TeX inputs and their preservation manifest. Revision 109 includes those existing blobs directly; it does not rewrite the old history to conceal the defect.
