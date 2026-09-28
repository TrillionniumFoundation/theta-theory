# A2 v72 — independent harsh referee review

September 17, 2026. Author-requested, AI-assisted assessment at the requested Annals / Inventiones / Acta / JAMS standard; not a commissioned journal report.

**Start with [REFEREE_REPORT.md](REFEREE_REPORT.md).** The review concerns reading head `161ee773c42bc39db4bdb0e18aaf8d516848140b`, compiled source `020c8b08176617e7bfb5dc37110c5b58fef99c1c`, and the complete new Section 8 with the operative dependencies enumerated in the report.

**Recommendation:** no acceptance recommendation at the requested top-four level on exceptional significance. No new fatal mathematical error or mandatory repair of the examined core is established. The unknown-offset single-law result is recognized as substantive. Prior closed comparison requests remain closed.

## Files

- `REFEREE_REPORT.md`: full English report, six detailed findings on the new section, inherited proof-interface audit, literature comparison and separate placement judgment.
- `AUDIT_EVIDENCE.json`: immutable source identities, read coverage, independent-check hashes and explicit delivery limitations.
- `independent_checks.py`: independently written exact algebra checks; no manuscript diagnostics imported.
- `MATHEMATICAL_CHECKS.json`: actual output from the independent script.

## Reproduce finite checks

Requires Python 3 and SymPy. Executed here with Python 3.13.5 and SymPy 1.14.0.

```sh
python independent_checks.py --output checks-normal.json
python -O independent_checks.py --output checks-optimized.json
cmp checks-normal.json checks-optimized.json
```

All checks use explicit exceptions, not removable assertions. The two actual runs were byte-identical. The JSON includes the script hash and interpreter/library versions, so different environment versions may change those metadata fields.

The checks cover 16 unequal-action/signed-anchor examples, 16 absolute-anchor negative controls, 12 signed cyclic blocks, nine cofactor/transfer cases, and additional exact identities. They do not certify infinite-dimensional estimates or physical realizability of arbitrary algebraic examples.

The report independently derives the finite-flight correction
`partial_uv log f_N(0,0) = p^2/d^2 + D_N/d + partial_uv log beta_N(0,0)`.
This supports the manuscript's distinction between exact limiting identification and finite-flight bias; it is not presented as a counterexample.

## Review boundary and repository isolation

This is a source-based mathematical review. Native manuscript PDFs and the source ZIP were not independently downloaded, rebuilt, hash-verified or rendered in this session. Author-side and previous-review delivery verification is not claimed as this review's work. Later analytic/global/catalogue and companion proofs outside the stated read scope remain uncertified here.

Only this new review directory is added, with the reviewed reading head as parent. No manuscript, prior report, delivery file, existing branch, default branch or repository permission is altered. No pull request or administrative change is required by this review.
