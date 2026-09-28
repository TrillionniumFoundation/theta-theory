# A2 revision 93: constrained determinant geometry and scalar gauges

New revision branch: `revision/a2-v93-constrained-newton-gauge-2026-09-19`.

This revision addresses the exact v92 referee report at commit
`37e03652f639930f5489dfee09150a7cba3964d7`, reviewing manuscript commit
`d55c480f8cdf9f1327b4142bf1bb31a315f71b2b`. It is a new revision, not an
edit of the review branch or of main.

## Read and build

The complete manuscript entrypoint is
`papers/A2-v17-boundary-information-coarsening/rigidity_v93.tex`.
The new main source is `article/v93/paper.tex`, relative to that paper directory.
All twenty previously active proof/bibliography modules remain active and
unchanged. New proofs are in `article/v93/constrained_newton.tex` and
`article/v93/fibres_and_admissibility.tex`.

```sh
python3 revisions/a2-v93/verify_a2_v93.py --receipt /tmp/a2-v93-verification.json
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v93.tex
```

The build needs Python with NumPy and SymPy, and a standard TeX installation
with amsart, Latin Modern, microtype, mathtools, hyperref and latexmk.
The branch-scoped workflow `.github/workflows/a2-v93-native.yml` installs
these dependencies and audits every push, including manifest-only changes.
Its artifact is named `a2-v93-exact-head-<actual SHA>` and contains the PDF,
log, extracted text, exact-HEAD receipt and source-response archive when the
corresponding steps complete successfully. A queued run is not a successful
build; inspect the run conclusion and the receipt for the delivered SHA.

## Principal result

Theorem `thm:constrained-newton` computes the exact constrained root exponent
from all homogeneous determinant coefficients and gives its leading
Hellinger-ball diameter on the finite quotient. Proposition
`prop:quadratic-exposure` shows why first-order Laurent exposure is insufficient:
strictly positive examples have no visible first variation but fixed-normalizer
exponent 2/m. With a free monic normalizer their exponent is 1/m.

Corollary `cor:free-normalizer-v93` gives the reciprocal actual resolvent pole
as the exact fixed-datum exponent, including cancellation-reduced poles and
nontriangularizable algebras. The scalar interpolation shear transports the
complete determinant invariant, and a bidegree refinement tracks separate
scalar and zero-sum coefficient errors. These pointwise results do not silently
change the constants in the retained boundary-uniform additive flag theorem.

The revision also provides the explicit binary stochastic-refactorization
lemma, distinguishes intrinsic from pointed singularities, and proves
fixed-margin compact equivalence of the Fisher condition and eta_d inverse.
It executes Option B of the v92 report; it does not misrepresent the binary
full-collapse fibre as the still-unproved Option A normal form.

## Review record and provenance

The detailed point-by-point response is
`revisions/a2-v93/RESPONSE_TO_REFEREE.md`. The original report is retained at
`reviews/a2-v92-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`.
`revisions/a2-v93/SOURCE_MANIFEST.json` separates the preceding report,
preceding revision, current source-snapshot commit, content identities and
runtime-HEAD policy. The verifier records actual `revision_head` and tree,
checks GITHUB_SHA in Actions, and verifies all imported and new source hashes.

Seven local finite diagnostic groups passed. The new proof modules passed a
local TeX smoke test without overfull horizontal boxes. These are not a full
inherited-manuscript compilation and are not formal theorem verification.
The exact-head native workflow is the full-source build check.
