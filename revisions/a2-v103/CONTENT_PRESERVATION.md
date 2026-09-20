# A2 v103 — preservation and proof-dependency map

Base: `8054ae5d5c318b7e59f9ad42545ae27b416bec09`, the controlling v102 review. The revision adds new paths only. It does not overwrite the v102 article or any historical derivation.

| Reviewed material | New principal use | Where the complete old text remains |
|---|---|---|
| v102 intrinsic residual envelope, arc order, and metric covariance | Proposition 2.1 retains the foundation; Theorem 2.2 and Corollary 2.3 add a finite-sheet lift, exposed faces, realization and products | `rigidity_v103_supporting.tex`, which inputs the complete v102 article |
| v102 binary coefficient inverse and local quotient | Lemmas 4.1–4.2 and Theorem 4.3 give an expanded self-contained proof and both uniform whole-model Hausdorff inclusions | Same supporting volume, without changes |
| v102 arbitrary-metric ray criterion and adaptive lower bound | Section 5 studies the native Hellinger family, proves dimension bounds and gives a fixed-experiment sharp witness | The entire old arbitrary-metric theorem and its proof remain in the supporting volume |
| v102 endpoint active-set formula and invisible-matrix example | Theorems 6.1–6.2 add equality classes, range, canonical value-function data and full one-endpoint fibres | Same supporting volume |
| v102 scalar polynomial wall, higher cancellation, residue discussion and probability embedding | Corollary 3.5 retains the scalar conclusion; Theorems 3.1–3.2 and 3.6 extend to coupled weighted systems | All old scalar proofs, residue examples and probability proof remain in the supporting volume |
| v102 supplied real monomial-presentation calculation | Appendix A supplies an analytic proper-surjective existence construction using exact primary references | The complete earlier presentation and order calculation remain in the supporting volume |
| v101 principal and its historical archive | Used for the unchanged cubic, boundary, rank-loss, weighted-atlas and equality-shell record | `rigidity_v103_archive.tex` inputs `rigidity_v102_complete.tex`, which includes the v102 article and its complete inherited archive |

The preserved historical record includes the full multiplicity and endpoint atlas; exact rank-deficient cubic fibres and identifying inequalities; the inverse through channel-rank loss; both cubic walls; signed second-order and critical equality-shell calculations; real weighted comparison; finite-jet and Puiseux-residue material; and fixed-format entrance results. No new weighted-system theorem is substituted for those distinct cubic hypotheses.

The new principal has its own complete proof chain for the new conclusions. The supporting and archive entrypoints retain earlier results, rather than serve as unidentified missing steps in a shortened new proof.

The native builder traverses literal TeX input and PDF-source edges. It recompiles available source dependencies, explicitly identifies and hashes any binary-only PDF dependency, records the exact triggering source commit, and checks that the difference from the controlling review is addition-only. These are intended runtime checks; their successful execution is evidenced only by the actual native receipt, not by this preservation map.
