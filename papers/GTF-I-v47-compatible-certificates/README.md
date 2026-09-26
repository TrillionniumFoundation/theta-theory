# General Theta Foundations I — Revision 47

**Robust Compatibility of Numerical Word Realizations**  
Qian Qi · 27 September 2026

Controlling report: r29, `6e8a9504a1a0820e6195317df885d99aed06c878`, reviewing v43. Source predecessor: v46 source-review `d7914880e7df679756c3b6ae86311485ac922f8a`. Published archival predecessor: v44 `d7042cf71485f661e27d87d12ffae35a2edfc15c`. No later report is invented for those later sources.

Work branch: `revision/general-theta-foundations-i-v47-compatible-certificates-2026-09-27`. The referee-ready branch is created only after the current build succeeds.

[Article](paper.pdf) · [Native source](main.tex) · [Response](RESPONSE_TO_REFEREE.md) · [New proofs](two-state-compatibility.tex) · [Build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone sources](evidence/CORE_SOURCES.zip)

## Results

For every antisymmetric finite binary target, the actual optimal two-label numerical error equals uniform approximation by a bounded decomposable seed/epoch/query tensor. The reduction deletes affine offsets without retaining an additional symmetrization coin. A balanced negative sign set gives a finite certificate against every two-label machine. For targets with means in `{0,+rho,-rho}`, sign factorability decides whether strict improvement over error `rho/2` is possible; if possible, the proof constructs error at most `rho/4`. The latter is not always the optimum.

For identity and quarter-turn commands on four planar axis seeds, two separated two-label bottlenecks force the exact error `rho/2` regardless of intervening widths. At one command and `rho<=1/6`, profiles `(2,3)` and `(3,2)` have exact error `rho/4`, `(2,2)` has `rho/2`, and `(3,3)` is exact. A complete arbitrary-horizon frontier is also given for profiles whose widths are one, two or at least four. The witnesses are rational for rational rho. The gap is robust under arbitrary uniform TV perturbations of size less than `rho/8`.

These are low-width and numerical-error results, not a new growth exponent or a general higher-width tensor classification. All previous Gram, Hankel, moment, arithmetic, profile and finite-bit proofs remain in the article. The current verification script checks finite identities and witnesses, not universal proofs or independent priority.

## Rebuild

Python 3.12, SymPy 1.14.0, PyMuPDF 1.26.7 and a standard AMS-compatible TeX installation suffice. No font files are distributed.

```sh
python check_compatibility.py
python -O check_compatibility.py
python build.py --core-only
```

The full archival build additionally reads `../GTF-I-v44-hankel-resonance/` or the directory named by `GTF_V44_INPUT`. It preserves the published v44 article and cumulative volumes. The standalone core does not need those archives. `verify_inherited.py` and `finite_bit.py` are unchanged published v44 code; the new verifier is separate.

The workflow builds the native source commit, performs a clean isolated rebuild, then adds only generated v47 artifacts and its root entry. It does not force-push. Source, build and publication commit identifiers are distinct. A workflow being queued or a successful source write is not a successful build.

## Preservation and resources

The complete original v46 introduction is in `inherited-introduction.tex`. All its other mathematical modules are unchanged except `main.tex`, which adds the new section and updates the title/abstract. Older repository paths and all prior review/work branches are untouched. The v44 article and cumulative PDFs are optional history, not the compact editorial package.

The primary resource counts available persistent labels and the held two-label answer. Epoch, horizon, row tables and arithmetic are free in the atomic model. The finite-bit theorem has its own separate accounting. The sign decision algorithm requires the explicit response table; it need not be polynomial in a succinct horizon. New finite frontiers do not solve all width-three profiles, all finite targets, all nongapped arithmetic or the independent analytic manuscript pipeline. Independent proof and priority assessment remain necessary.
