# General Theta Foundations I — Revision 41

**Intrinsic Action Gaps and Numerical Memory**  
Qian Qi · 26 September 2026

Controlling r25: `9707844addcd9eb478eb863514f288923f9d40fd`. Reviewed v39: `28890c62dd69f217bf2f1c205ff9542eb537c2ef`. This is an additive revision on `revision/general-theta-foundations-i-v41-intrinsic-action-2026-09-26`. Two existing v40 work branches are untouched. The referee-ready branch is published only after the source-bound build and independent core rebuild succeed.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r25](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## Mathematical result

The effective command action, not a redundant presenting group, defines the expansion hypothesis. Its sphere Koopman gap equals the Lebesgue gap used by the entropy argument. The seed set is arbitrary and finite; its invariant span and canonical isotypic types determine the active experiment. An exact commutant covariance formula computes canonical activation magnitude, and an optimized query norm gives an intrinsic numerical error threshold.

At the stated fixed signal/error, only one expanding active type with maximal minimum-orbit dimension is required:

```
W_(N,epsilon) = Theta(N^(sigma_X/2)).
```

The other active types may fail to expand. A faithful ten-command rational SO(3) x SO(2) example consequently has width Theta(N) even though its full effective group has no norm gap. Its SO(3) gap is a qualitative external Benoist–de Saxcé input, not a computed numerical certificate.

All compact simple adjoint minima are computed by root deletion, including every exceptional type. Classical defining representations, low-rank spin modules and all second exterior powers of SU(n) are also evaluated with stabilizers. In the SU(6) second exterior power the minimizing orbit is SU(6)/Sp(3), dimension 14, not the dimension-17 decomposable orbit. The conditional width exponent is therefore 7.

The current primary arXiv record and v2 PDF verify the Chen–Wu v2 constants. Both versions now have separate references and an explicit dated source audit; differing v1 and v2 theorem numbers are not conflated.

## Reproduction

Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7, mpmath, and a LaTeX installation with AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools, needspace and hyperref suffice for the standalone core. The full archival build also requires NumPy 2.3.5 and SciPy 1.17.0 for the inherited v37/v38 verification programs. These are installed explicitly in the publication workflow.

```sh
python papers/GTF-I-v41-intrinsic-action/verify.py
python -O papers/GTF-I-v41-intrinsic-action/verify.py
python papers/GTF-I-v41-intrinsic-action/build.py --core-only
python papers/GTF-I-v41-intrinsic-action/build.py
```

The core source ZIP extracts to one package. From its parent, run `python GTF-I-v41-intrinsic-action/build.py --core-only`. The full source archive contains pinned predecessors needed for the archival build. No font files are distributed. The build runs v41 and inherited v24–v39 checks in ordinary and optimized Python; there is no claim to have verified the separate v40 work.

## Preservation and boundaries

[Unchanged v39 supporting article](supporting-results.pdf) · [Complete mathematical archive](complete-manuscript.pdf) · [Complete development archive](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

Original paths, reviews and branches remain unchanged. The current article retains the prior analytic proofs and sufficient theorems; the supporting v39 PDF and cumulative volumes are unaltered. Large archives are optional provenance, not the compact referee package.

The primary resource is nonuniform clocked atomic-row label width, with arbitrary hidden states and free tables/arithmetic. The theorem is not a uniform-space statement or an all-alphabet finite-optimum classification. Higher general spin/highest-weight minima, exact leading constants, vanishing-signal limits and the original-page LPS audit are not claimed settled. The optional LPS5-dependent numerical result is separate from the new main theorem. Historical A2/B4/C2 gates and independent review are not declared closed. Executed tests and compilation establish reproducible delivery, not universal proof or journal acceptance.
