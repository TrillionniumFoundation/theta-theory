# A1 English v24 — source revision for referee reassessment

**Main article:** *Attainable information at exponent collisions*, Qian Qi.  
**Complete companion:** *Attainable information in positive experiments: complete companion developments*.  
**Controlling review:** `78e948fe03a3969fde4c96411ae1fee5915cb908`.  
**Reviewed submission:** `e7c1111d0ab8fb39e4b213902186db2cdf6d0dea`.

Start with [`main.tex`](main.tex), [`companions.tex`](companions.tex), and the
complete [`RESPONSE_TO_REFEREE.md`](RESPONSE_TO_REFEREE.md). These are the same
mathematical sources as the delivered v24 revision, not a new mathematical
revision. The main article contains the complete direct collision proof;
the companion contains all the separate developments and alternative proofs.

All 130 inherited formal statements and all 129 complete inherited proofs
remain active across the two volumes. Of the proofs, 128 remain byte-identical;
one has the exact navigation-only change recorded in
`EDITORIAL_PROOF_EDITS.json`. The original 772 manifest-covered source files
are retained under `history/v23-source/`, by reusing the immutable v23 Git tree.
The controlling report and its independent diagnostic script are in
`review-basis/`. These source-preservation claims do not certify mathematical
correctness or journal acceptance.

## Reproduce the build offline

From this directory, using Python 3.10 or newer:

```sh
python materialize.py
python build.py --prepare-only
python build.py
python validate.py
```

The first command recreates the redundant historical expansion, inactive audit
concatenations, and the companion bibliography from ordinary source files
already present in the checkout. It verifies the historical expanded baseline
against the original v24 delivery's SHA-256 before proceeding. The resulting
17 expanded/bibliographic files have been compared byte-for-byte with the
original delivery. No manuscript statement or proof is generated from a model,
remote service, or placeholder. No sibling revision directories are required.

The original `build.py` and `validate.py` are unchanged. Building requires
LaTeX with `amsart`, AMS packages, Latin Modern, `mathtools`, `mathrsfs`,
`geometry`, `microtype`, `booktabs`, `xr-hyper` and `hyperref`, plus Poppler's
`pdfinfo`. Focused v22 diagnostics also require SymPy. The build disables shell
escape and uses five alternating passes to resolve cross-volume links. Keep
the resulting `main.pdf` and `companions.pdf` together. The delivered build
has 20 and 108 pages, respectively.

`python validate.py --full` retains the optional older test suites; the prior
incomplete full-suite attempt is explicitly recorded separately. Normal
validation runs the directly relevant v22/v23 author suites, the published
referee diagnostic, exact finite phase checks, proof-preservation mutation
controls, and both builds. These are executable checks, not formal proofs.

## Publication and evidence scope

This branch publishes the complete mathematical **source** revision, historical
source, response, original validation receipts and reproducible build programs.
The precompiled PDF binaries and the enclosing chat-delivery ZIP are not Git
blobs in this source publication. They remain in the previously delivered
package; their exact SHA-256 values are recorded in
`validation/EXECUTION_REPORT.json`. Running the build recreates the PDFs;
byte identity of PDF metadata across later builds is not asserted.

The prior local execution receipt is preserved unchanged in
`validation/EXECUTION_REPORT.json`: 45,393 focused author assertions, 3,878
referee-script checks and 201 v24 finite checks. It is not a GitHub Actions
success receipt or a new independent referee report.

The branch-specific Actions probe (run `34108512754`) failed. Publication uses
GitHub's Git-data API directly and does not depend on that job. The probe
workflow is not retained in the final source tree. The net change against the
controlling review is the new `papers/A1-english-v24/` directory only; earlier
manuscripts, reviews and other branches are not modified.
