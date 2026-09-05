# Round 53 review entry point

Active manuscript: **`ROUND53_REVISION.tex`** (14 pages in the recorded build).

Revision branch: `revision/round53-bound-certificates-energy-robust-posterior-2026-09-05`.
Controlling review HEAD: `8e3e6f663fde9942384298eb9c60cf217a926bac`.

Read `AUTHOR_RESPONSE_ROUND52.md` for the complete item-by-item response. The active root contains the broadened theorem, the clock-aware pulse inverse, the new squared-energy posterior principle, the physical corollary, finite-response reduction, corrected primary-source comparison, bound outer-enclosure contract and readout/time lower-bound distinction. It directly inputs the complete unchanged `round51/model_inverse.tex` and `round51/likelihood.tex`; these are included in the source manifest and are present on this branch.

## Reproduce

From a checkout of this branch, with Python 3.10+ and a TeX installation containing the packages named in the root:

```sh
python tools/verify_round53.py --pdf
```

The executed environment used Python 3.13.5. This command verifies source hashes without modifying the manifest; runs 66 historical and 44 new tests; and builds the article with three actual `pdflatex` passes. Output is written to `artifacts/round53/`. Inspect `VERIFICATION.json`, `ROUND51_REGRESSION.json` and `ROUND53_REGRESSION.json`. Run without `--pdf` for source and test verification only; that receipt explicitly reports that a PDF build was not executed.

The committed manuscript is TeX, with all dependencies. A binary PDF is not required for a GitHub checkout to build it. The source/build receipt records the generated PDF digest, and a compiled PDF accompanies the conversation deliverable.

## Review targets

R52-C1: Section 8 and `certify_outer`; negative witnesses and a real nonempty positive complete-grid fixture in `tests/test_round53.py`.

R52-Q1/Q2: Theorem 1.1, Section 3, and the exact certificate constructor. The example certificate changes from N=60 to N=41 without changing its model, target or clock.

R52-M1: Section 7.1 and `round53/LITERATURE_AUDIT.md` explicitly distinguish Gaussian pseudocode from sub-Gaussian proof hypotheses.

R52-M2: Theorems 1.2 and 5.1, the polynomial-discrepancy corollary, and their physical information budget. Mathematical and editorial judgments are not conflated.

Elapsed time: the final corollary requires a positive sampling gap for comparison policies.

The old unbound predicate exists only as preserved historical code. Use `tools/round53_certificates.py` for the active certifying endpoint. Finite tests are not formal verification of the universal analytic theorems. The positive end-to-end fixture uses a deliberately narrow box and does not establish practical wide-box enumeration costs. Historical reports and older manuscript roots remain unchanged.
