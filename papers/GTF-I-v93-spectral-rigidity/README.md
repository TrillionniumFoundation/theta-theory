# General Theta Foundations I — Revision 93

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

The controlling external assessment is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. The immediate published base is v92 at `a7081ca8cfb1df8f6369a5820e4f3b5027b66ca2`, native source `33811525dd80dbc3c0c70059114fb779e9ac9c84`. No later referee report is being assumed. The original reports remain frozen verbatim.

### Primary reading route

Start with `paper.pdf` / `quantitative.tex`. The current linked supplement is `BINARY_SUPPLEMENT.pdf` / `supplement.tex`. The standalone journal archive contains exactly these two manuscript objects, their active source dependencies and a reproducibility note. The independent structural article and the complete research edition are archival companions, not additional premises or additional novelty claims for the principal theorem.

The topic and four-leading-general-mathematics-journal objective remain unchanged. The complete support-covariance, fixed-tube profile and hard quadratic-budget laws remain active, as do the v90 exact operational experiment, v91 arbitrary-experiment variational and dual principles and v92 rank-resolved hierarchy. Their quantifiers are not conflated.

### What is new

**Primary Section 19** (source module `86-initial-spectra-and-rank-rigidity.tex`) identifies the complete optimal initial spectral set, gives a finite attaining instrument and derives quantitative common-support rigidity. For the shared-basis family and rank level `r=min(k,ell)`, an initial Gram matrix achieves the equal-prior optimum exactly when `rho<=I/r`. Such a matrix admits a decomposition into at most `d` commuting rank-r projections divided by r. The proof gives an explicit interval construction.

If the initial reference is also bounded by q, the exact equal-prior and biased values replace r by `min(q,k,ell)`; two fixed-subspace preparations attain them without feedback. This counts the first reference, old retained output and fresh reference at their stated cuts. It does not assert an all-times workspace bound or remove the reset cut.

Away from the qubit rank-one exception, a centered-swap deficit bounds squared trace distance of both Grams to a common normalized rank-r projection. The score deficit controls an approximate projection decomposition of the initial Gram and gives a quadratic loss bound in `tr(rho-I/r)_+`. The qubit exception is solved by an exact pinching identity, including commuting mixed factors. Constants are explicit, not claimed optimal.

### Reproduction and preservation

```sh
python build_revision.py --check-source
python spectral_rigidity_check.py
python -O spectral_rigidity_check.py
python spectral_frame.py examples/spectral-frame.json
python build_revision.py --isolated
python build_revision.py --verify-published
```

The last two commands have distinct roles: production runs at an actual native-source Git commit and creates source-bound publication evidence; published-head verification is read-only and reconstructs the submitted archives. Local `--preflight` is not publication qualification. All 815 immediate-predecessor native files are retained in active paths or exact `predecessor-v92-audit` copies; every inherited mathematical section remains byte-identical and active. The full build has 35 suites run normally and under `python -O`. The new suite labels exact fixtures and deterministic floating-point sanity checks separately. Neither is a proof of a continuum theorem.

`RESPONSE_TO_REFEREE.md` addresses all 15 required and 30 detailed R60 comments. `PROOF_AUDIT.md`, `INTERNAL_MATHEMATICAL_REVIEW.md` and `HISTORY_AND_PIPELINE_AUDIT.md` are current Revision 93 documents. Printed primary numbering is used first; `evidence/THEOREM_LOCATIONS.json` records actual numbers and pages. Independent human priority clearance and physical reset calibration are not claimed. The five independent analytic aggregate closure flags remain false.

The complete edition now uses a short abstract and retains the full preceding abstract text as its opening synopsis; no mathematical material is discarded. Its PDF metadata identifies Revision 93.
