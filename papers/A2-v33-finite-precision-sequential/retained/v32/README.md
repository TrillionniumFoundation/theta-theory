# A2 v32 — adaptive scalar boundary reconstruction

Qian Qi · 4 October 2026

**Primary:** *Scalar collision laws and recognition of periodic dispersing billiards*, `main.tex`. The controlling referee report is v31 at `f2e2a13a9a742c412a4b1a59b43388a2ba385bda`, reviewing author `27d109b0eba6a03d453834ef9da9418446ac637d`. The billiard topic, original scalar sensor contract and Annals/Acta/Inventiones/JAMS target are retained.

## Main results

Theorem 1.1 replaces the whole-aperture fine grid by a fixed coarse acquisition followed by adaptive radial searches. Proposition 2.3 evaluates each occupation query on a finite dependency diamond using only the two pooled reciprocal bit means. No free-start label or membership response is supplied by the apparatus. Lemma 3.2 permits adversarial, nonmonotone labels inside the boundary layer; Lemma 3.3 preserves the full C(6,beta) radial regularity and reconstructs a smooth convex body.

For s=6+beta and C2 geometric accuracy nu, the number of attempted preparations is at most

`C nu^(-1/(s-2)) log(C/nu) log(C/(nu delta))`.

The finest localization and sufficient coupled position/time/angle error are of order `nu^(s/(s-2))`. Constants depend on the complete geometric prior and known patch margin. Theorem 1.2 gives a physical packing with a necessary `c nu^(-1/(s-2))` binary outputs at fixed confidence, even with period and pose supplied. Thus the power matches, with a logarithmic gap; no exact logarithmic minimax or unknown-smoothness adaptation is asserted. The lower bound is for a fixed nondegenerate subclass, not every possible restricted prior.

Section 4 recovers the primitive orbit count and exact bounded-denominator relations once the known patch margin is resolved. Period-basis coordinates remain estimates. Repeated shapes and symmetries are allowed. The complete sensor contract includes localized starts, prescribed compass displacements, exactly reciprocal nominal reverse distributions, all-attempt normalization and scale-dependent calibration. Solid starts and free misses both give zero. No physical apparatus execution, passive invariant, or exact analytic count-germ conclusion is claimed.

## Preservation

`retained/v31` is the exact complete reviewed v31 paper tree `ff74e5124141dc46b0f08f7e38a5cf258b87e642`, including all twelve active core files, tools, receipts and nested preceding volumes. It is supplied as Supplement R, not deleted history or an external publication. Its complete fourteen-document package is retained; the new primary makes **fifteen declared documents**. No old paper, referee report or workflow is overwritten. `SUBMISSION_MAP.md` gives the reading map.

## Reproduction and actual local evidence

The local source-content run passed **11,647 finite mathematical/source checks** and **42 validation-contract checks**, with identical ordinary/optimized Python output. The **13-page** primary compiled with no final TeX warnings, undefined references or overfull/underfull boxes. All thirteen pages were rendered and inspected. Numerical radial examples test geometric reconstruction, not a physical collision apparatus. The local receipt has null checkout and hosted-run fields and does not claim full-package qualification.

```sh
python3 tools/validate_v32.py
# In a checkout containing the exact retained sources and all historical workflows:
python3 tools/validate_v32.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
python3 tools/adaptive_scalar.py examples/two-site-conditional.json
```

Requirements: Python 3.10+, latexmk, TeX Live LaTeX extras/recommended fonts, Poppler; NumPy/SciPy for the delegated historical suites. The CLI provides exact finite interval primitives conditional on supplied forcing and survival bounds. Its floating-point radial helper is not a certified interval evaluator. The full physical experiment is specified and proved in the manuscript, not reported as apparatus-tested software.

The read-only v32 workflow checks out its exact triggering SHA, verifies the retained native tree, runs current diagnostics and delegates the entire v31 qualification at that same SHA. It builds all fifteen declared documents and uploads actual receipts, logs, source archives and PDFs, including failures. A workflow definition, queue state or artifact's existence is not a successful qualification. Its actual run supplies that conclusion. The old v31 hosted pass is historical evidence only.

Finite diagnostics and compilation do not certify continuum proofs, literature priority or journal acceptance.
