# Round 51 — referee entry point

Active article: [ROUND51_REVISION.tex](ROUND51_REVISION.tex), *Single-Atom Boundary Identification with Retained State and Logarithmic Physical Depth*.

Read the [point-by-point response](AUTHOR_RESPONSE_ROUND50.md), then the article in input order. The controlling report is [Round 50](REFEREE_REPORT_ROUND50_GPT6_PRO_HARSH.md), frozen at `a7b9ffcfd79d2f8cd5179238db9124486c1d9f0a`. The earlier reviewed manuscript was frozen at `abae39b7efeec5f6995f85fcbe1cc1d10e27fba6`. This branch descends from the controlling report, preserving the earlier sources and review history.

## Theorem map

| File | Main responsibility |
|---|---|
| `round51/introduction.tex` | General single-atom logarithmic-depth theorem; scoped literature comparison |
| `round51/model_inverse.tex` | Common stability and exponential all-depth jet inverse; exact inherited source |
| `round51/sampled_generator.tex` | Integrated-pulse correction, `16^-N` remainder, exact weighted transform, explicit region |
| `round51/likelihood.tex` | Entropy, nuisance integral, chronological full-posterior transfer |
| `round51/blocks.tex` | Enlarged event, all-sign energy, complete-posterior proof |
| `round51/response_transfer.tex` | FIR-to-physical reduction, bounded-input estimator, finite-section uniformity |
| `round51/enclosures.tex` | Certified rational outer sets and all five error budgets |
| `round51/optimality.tex` | All-policy two-way propagation and logarithmic depth-order lower bound |

## Reproduce from an ordinary checkout

Python 3.10 or newer suffices for the standard-library implementation and tests. A TeX Live installation providing `pdflatex`, `amsart`, `lmodern`, `mathtools`, `booktabs`, `geometry`, `microtype` and `hyperref` is needed for the PDF. From the repository root:

```sh
python tools/verify_round51.py
python tools/verify_round51.py --build
```

The first command checks frozen source identity and runs the new tests; it does not claim a PDF build. The second additionally requires three successful LaTeX passes. Actual receipts and logs are written under `artifacts/round51/`. The PDF is generated as `artifacts/round51/ROUND51_REVISION.pdf`. No separately delivered program archive is required for this revision.

The source manifest covers the active TeX closure, implementation, tests, verifier and review documentation; it excludes itself and generated receipts to avoid circular hashing. Its own SHA256 appears in the verification receipt. A receipt is evidence of a particular execution, not a formal proof. PDF byte identity across different TeX installations is not promised; source identity and successful dependency resolution are checked separately.

## Scope of verification and historical preservation

The finite suite checks exact algebra, coefficient reconstruction, complete sign enumeration, certificate inequalities, input validation and resource failure behavior. It does not prove an infinite-dimensional theorem by enumeration, simulate posterior contraction, or certify practical complexity. The analytic proofs are in the manuscript.

The old 43-test Round 49 implementation was not recovered. The present programs and test receipt are explicitly Round 51. The independent Round 50 referee suite is unchanged and is not relabeled as ours. The older roots, `round49/` and `round45/` remain available on the branch; they are not part of this round's active-root build.

See [proof/source ledger](round51/PROOF_LEDGER.json), [literature audit](round51/LITERATURE_AUDIT.md) and [source manifest](round51/SOURCE_MANIFEST.json). The publication record binds the committed sources to the recorded local checks after upload. No merge into `main` or editorial approval is implied.
