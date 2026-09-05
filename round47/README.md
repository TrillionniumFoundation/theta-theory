# Round 47 review entry

The active main manuscript is [`../ROUND47_REVISION.tex`](../ROUND47_REVISION.tex):
**Sharp Depth Scales for Adaptive Boundary Identification of Infinite Damped Jacobi Lattices**.
The point-by-point response is [`../AUTHOR_RESPONSE_ROUND46.md`](../AUTHOR_RESPONSE_ROUND46.md).
The controlling report is the Round 46 report at commit `0c2f4c9f10bcf7c9f5a37538d869061e6e0fbfb8`.

## What to review

The main article is self-contained. Its twelve local section inputs contain the proofs of the linear-depth jet inverse, oversampled fixed-window separation, a finite-mean long-probe construction, exact policy-uniform posterior bounds, two-way information comparisons, and constructive confidence enclosures. The logarithmic depth result changes the exploration duration law; it does not assert a bounded maximum duration per long probe. Its total clock has an explicit exponential tail around a linear budget.

`ROUND47_RETAINED_RESULTS.tex` separately retains the earlier homogeneous nonlinear quasi-BvM, filter, memory, and preparation results. Its five `round45/` input blobs are unchanged. The new depth proof does not depend on this supplement. No historical manuscript or report is removed.

`PROOF_LEDGER.json` is an index of claims and proof dependencies, not an independent proof certificate or a journal recommendation. In particular, the actual adaptive information is not replaced by its exploration floor; the fixed-window testing comparison is not asserted for arbitrary no-washout histories; and optimal depth constants are not claimed.

## Reproduce source binding, finite tests, and both builds

Use a Git checkout with the source commit and its ancestry available, Python 3.10 or later, and `pdflatex` with the standard AMS, Latin Modern, geometry, microtype, mathtools, and hyperref packages. On the publication commit or a later artifact-only descendant:

```sh
SOURCE_SHA=$(python3 -c 'import json; print(json.load(open("ROUND47_PUBLICATION.json"))["source_commit"])')
python3 tools/verify_round47.py --source-sha "$SOURCE_SHA" --build
```

At the source-freeze commit itself, before an artifact receipt exists, use `--source-sha "$(git rev-parse HEAD)"`. The verifier requires literal covered source inputs, compares the manifest and every source blob with the named existing commit, runs the tests, and builds both roots in a clean isolated directory. It rejects missing commits, changed sources, missing inputs, undefined references, and overfull boxes. A successful full run writes `ROUND47_VERIFICATION.json`, both PDFs, logs, and `ROUND47_REVIEW_BUNDLE.tar.gz`. Only an actual run of that verifier can establish that status.

The tests alone can be run with:

```sh
python3 -m unittest discover -s tests -p test_round47.py -v
```

The 34 tests include finite algebraic regressions and adversarial Git fixture checks. They do not establish the infinite-dimensional or all-depth theorems. Consult `ROUND47_PUBLICATION.json` for which checks were actually executed at publication; do not infer successful remote CI or a supplement build from a locally built main PDF.

## Exact computational certificates

The certificate module accepts exact rational inputs; no floating-point input is silently interpreted as a rigorous interval.

```python
import sys
from fractions import Fraction as F
sys.path.insert(0, "tools")
from round47_certificates import Box, grid_certificate

box = Box(F(1), F(2), F(1, 2), F(1), F(3), F(4), F(1))
certificate = grid_certificate(box, depth=2, delta=F(1, 16), mode="long")
certificate.validate()
print(certificate.order)
# certificate.separation is an exact positive Fraction.
```

`mode="compact"` uses the unchanged fixed-window diagnostic law. Its rational search may choose a different order from the paper's closed-form sufficient choice; the returned direct remainder and separation certificate is checked exactly. `outer_confidence` implements the finite rational outer construction from rational outward response bands. Resource caps raise an exception rather than returning a partial result. The module does not assert that externally supplied bands have statistical coverage.

## Source and artifact separation

`SOURCE_MANIFEST.json` binds both roots, all active local TeX inputs, code, tests, response, ledger, this entry, and the read-only workflow. Its own bytes are checked against the named source commit, avoiding a circular self-hash. Publication receipts and generated build/test artifacts are outside that source manifest and may be added in an artifact-only descendant without changing the mathematical source.
