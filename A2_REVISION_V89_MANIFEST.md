# A2 revision 89 — referee reading entry point

**Manuscript:** *Projective polynomial observations: observable conditioning and singular inference*  
**Author:** Qian Qi  
**Date:** 19 September 2026  
**Revision branch:** `revision/a2-v89-observable-polynomial-quotient-2026-09-19`  
**Review pull request:** https://github.com/TrillionniumFoundation/theta-theory/pull/52

## Pinned provenance

The controlling report is `reviews/a2-v88-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md` at review commit `47fd795b7e4d80f9fe81e9798e73a05efc7fa8f7`. It reviews v88 source commit `777a9c951d5ca94a5261a6585ab6548d267e21e4`. The complete v89 manuscript was committed as `3de72a935ce643ea22e522ba7a6c233331d76247`, an additive child of that review. The subsequent documentation commit does not change the manuscript sources.

The revision is for independent re-review. It neither merges into main nor assigns a journal acceptance verdict. Every inherited source, report, companion and workflow remains unchanged.

## Principal article and response

Compile `papers/A2-v17-boundary-information-coarsening/rigidity_v89.tex`. It inputs `article/v89/paper.tex` and eleven further TeX modules in the same v89 directory. All principal proofs are in that article. The historical companion is retained, not made a prerequisite for the new theorems.

The response package is `reviews/a2-v89-response-to-v88-2026-09-19/`:

- `RESPONSE_TO_REFEREE.md`: point-by-point response, using stable theorem labels.
- `PRESERVATION_AND_SUBMISSION_BOUNDARY.md`: inherited-source hashes and mathematical correspondence.
- `LITERATURE_AUDIT.md`: the added rational-realization references and the scope of source verification.
- `BUILD_AND_VALIDATION.md`: native build, source identity, diagnostic scope and actual CI status.
- `LOCAL_VERIFICATION_RESULTS.json`: recorded finite local diagnostic results; not formal proof certification.

## Main additions and locations

| Statement | Number | First page in the native 25-page build |
| --- | --- | --- |
| Full polynomial span: sharp d+2 clock count | Proposition 2.6 | 6 |
| Observable polynomial inverse and additive normalization gauge | Theorem 3.1 | 7 |
| Explicit degree and clock dependence | Proposition 3.2 | 9 |
| Exact two-sided local metric condition | Theorem 4.1 | 10 |
| General rational interpolation module | Theorem 5.1 | 11 |
| Nondiagonalizable general quotient resolvent bound | Proposition 5.2 | 12 |
| Observable polynomial honest inference | Theorem 9.1 | 21 |
| Sharp degree-d semisimple signal classes | Theorem 9.2 | 22 |
| Real-rooted multiplicity neighbourhood minimax exponents | Theorem 9.3 | 23 |

The affine residue theorem, direct estimator, confidence construction, both positive affine lower-bound families and observation-law correspondence remain in Sections 6–8 and 10. Their four modules are exact copies of the corresponding v88 blobs.

## Build

From the repository root:

```sh
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v89.tex
```

A native local build of all thirteen TeX source files succeeded: 25 pages, no unresolved references/citations, duplicate labels, overfull boxes or underfull boxes in the final log. Source Git blobs match the committed manuscript. The local PDF SHA-256 is `6de1df65d37e6f5e8690202be613a051836a48305582af3bd836d0f50cacdcbb`. A byte-identical PDF is not expected from another TeX distribution or build timestamp; compare source hashes for source identity.

The branch also adds `.github/workflows/a2-v89-manuscript.yml`, with read-only repository permissions. At the validation readback, the initial PR workflow was queued, without a conclusion. No successful Actions build is claimed. The local diagnostic script upload was blocked; its results are recorded with that limitation, and the workflow uses the inherited v88 verifier rather than pretending to run the unavailable new script.
