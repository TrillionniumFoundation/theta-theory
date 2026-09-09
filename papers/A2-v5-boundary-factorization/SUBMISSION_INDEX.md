# A2 v5 referee entry points

The complete article is `main.tex`; `python build.py` builds it and the exact original `two_collision.tex` companion. The local validated outputs are 55 and 7 pages. `RESPONSE_TO_REFEREE_V5.md` is the controlling response, and `PROOF_LEDGER_V5.md` gives the dependencies.

| Question | Article locator |
|---|---|
| What is the reusable analytical mechanism? | Theorem 5.1, Section 5, `v5/10_twist_chains.tex` |
| How is the exponentially small flux controlled relatively? | Cofactor and trace-log comparisons in Sections 5.2 and 6.2 |
| Where does the physical preparation enter? | Section 4 and Theorem 6.3 |
| Does the nonlinear geometric fiber require long records to be visible? | Proposition 7.3: it is already visible at one complete flight |
| What happens to the old programmed-offset estimator under timing error? | Proposition 10.1 |
| What extra observation removes the inverse-offset factor? | First residual time; Lemma 10.2 and Theorem 10.3 |
| Is the new inverse pairwise and finite-data? | Theorem 13.1: first four limiting threshold amplitudes, including collisions |
| Why is the exponent one third attainable? | Lemmas 13.2 and 13.3: collision Jacobian and multiplicity-preserving root matching |
| Why is it sharp? | Actual two-sided geometric path in the proof of Theorem 13.1, with a weighted whole-sequence estimate |
| Is the radial one-half theorem retained? | Theorems 12.1 and 12.2 |
| Where is the DKL Inventiones comparison? | Section 15 and the bibliography |

## Frozen inputs

Review commit: `ec861ecfcdd83a81880c1a9082becc19b0c76977`. Reviewed manuscript commit: `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`. The review is preserved in the repository and under `review-basis-v4/REFEREE_REPORT.md` in this revision.

The whole frozen native v4 manuscript tree is the base of this new directory. Previous source directories, diagnostics, reports, and historical derivations remain available. Every one of the 176 formerly active v4 article labels remains active in v5. Historical entry-point metadata are retained under `history/v4-publication`; old response and proof-ledger aliases are preserved under `history/v1-entrypoints`.

## Validation

Read `verification-v5/NATIVE_BUILD.json`, `verification-v5/VALIDATION_SUMMARY.json`, and `verification-v5/REVISION_CHECKS.json`. The native build has no stubbed references or substituted statements. The verification scope is finite symbolic/numerical diagnostics and native-document validation, not a formal or editorial certificate.
