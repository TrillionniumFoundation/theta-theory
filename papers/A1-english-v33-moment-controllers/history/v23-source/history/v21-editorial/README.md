# A1 English v21 — attainable geometry and causal memory

**Full manuscript:** `main.pdf` (114 pages in the recorded local build).  
**Readable LaTeX entry point:** `main.tex`.  
**Point-by-point reply:** `RESPONSE_TO_REFEREE.md`.  
**Proof hierarchy and preservation:** `PROOF_LEDGER_V21.md` and `PRESERVATION_REPORT.json`.

This revision responds to the independent v20 report at
`078f34222b00797203cdf6dd421eab9f9f428c59`, based on the published v20
manuscript at `6f103ad252d7c65f140720f4095585026f7bb1b9`. The controlling
report is `reviews/a1-english-v20-independent-2026-09-07/REFEREE_REPORT.md`.
The new branch is
`revision/a1-english-v21-causal-transfer-and-proof-hierarchy-2026-09-07`.

## Reading order

The principal statement is Theorem 1.1. Its proof uses the interpolation
and covering inputs, the geometry-to-causal transfer theorem (Theorem 5.1),
the positive remaining-test update (Lemma 5.2), the acquired Newton flags,
and the explicit verification in Section 6.3. The main argument and its
collision-tree consequences precede Appendix A, which starts on page 22
in the recorded build. The old direct checkpoint and streaming proofs
remain complete in Appendix D; the main proof does not use them as premises.

Appendix A contains structural rank and affine resolution. Appendix B
contains full-support pairings, dimension-free feasibility, exact kernels,
the finite matroid-intersection specialization, the square moving-kernel
example, and the general acquired-history arguments. Appendix C preserves
the circular, inverse-profile and ambiguity developments. Appendices D–G
contain all specialized proofs, decision consequences, effective resource
bounds and contribution comparisons. Nothing is reduced to a proof sketch.

## Substantive changes

The exact-kernel result keeps its original dimension-free conclusion. A
self-contained feasibility lemma replaces the out-of-scope citation in its
statement and proof, including the zero-dimensional case. The finite
unconstrained maximum-rank corner is explicitly identified as classical
linear matroid intersection. The referee's square moving-kernel example is
proved in physical prediction units. The general transfer theorem makes
the joint geometry, acquired mass and causal update assumptions explicit,
permits unequal stage budgets, and retains the whole error recurrence.
Its monomial application constructs a bounded invertible ambient coordinate
change even at exact collisions, without dividing by a zero pivot.

## Build and validation

Run from a checkout containing both this directory and its **unchanged
sibling** `papers/A1-english-v20`:

```sh
cd papers/A1-english-v21
python -m pip install sympy==1.14.0
python manifest.py
python build.py --prepare-only
python validate.py
```

Python 3.13 and a TeX installation providing `pdflatex`, `amsart`, Latin
Modern, `microtype`, `booktabs`, `mathtools`, `mathrsfs` and `hyperref` are
sufficient; validation also uses `pdfinfo`. The CI installs the needed TeX
packages and the pinned SymPy version. Preparation generates readable
`build/*.tex` files and `build/expanded.tex`; they are not absent proofs.
The complete package contains these generated readable files as well.

`validate.py` reruns the ten inherited author suites and the independent-
implementation v21 diagnostics, reruns v21 under `python -O`, executes an
actual standalone inverse-mutation rejection, then performs three TeX
passes. It records actual results in `validation/EXECUTION_REPORT.json`.
The v21 tests are independent of author theorem implementations, not an
independent referee assessment. Test predicates and source identity checks
are not mathematical proof verification or a journal-acceptance claim.

The builder anchors the published v20 source manifest to Git blob
`db8414e9ec13e862a7af091c89417fdd2aa6207d`, verifies all 729 listed sources,
retains 113 of its 114 proof blocks and 116 of its 117 statement blocks
byte-for-byte, and checks the one explicitly registered E20.1 correction.
All 347 earlier labels remain in the full compilation. Five additional
statements and six complete proofs, including the main theorem's direct
transfer proof, produce 122 statement and 120 proof blocks. Counts establish
preservation and navigation, not significance. The original v17 operational
inverse is independently pinned as well.

Older source versions and all review reports are left unchanged. The revised
front matter is archived under `history/v20-editorial/`. The latest source
manifest excludes generated artifacts and execution receipts, so recorded
results can be regenerated without rewriting source hashes.
