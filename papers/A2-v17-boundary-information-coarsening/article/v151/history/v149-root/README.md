# A2 revision 149: reading guide

**Principal manuscript:** [geometry.pdf](geometry.pdf), *Finite failure schemes and the reconstruction of quadratic pencils*, Qian Qi.

**Controlling report:** v148 independent report at commit `dc3a951e26de17e0e69403b1d8cfdfb5e28bc306`. Its exact copy is in `review_inputs/v148_REFEREE_REPORT.md` after source assembly in the repository.

**Start with** the abstract, Introduction subsection “Intrinsic strata, infinitesimal parameters, and pencil moduli”, and the three new sections listed below. The full inherited local, global, all-pencil, singular, automorphism, and spectral arguments remain in the principal article.

| New section | Principal results | Source |
|---|---|---|
| Common-divisor strata and intrinsic families | Universal gcd; determinant-divisor quotient; relative first-relation algebras | `parts/37-common-divisor-strata-v149.tex` |
| The effective moduli stack of pencil failure algebras | Exact common multiplicity; all-base effective pencil stack; specialization strata | `parts/38-pencil-deformation-equivalence-v149.tex` |
| Transverse deformations with unchanged determinant support | Three normal modes; complete fixed-radical Grassmannians and symmetry-breaking lines | `parts/39-transverse-relations-v149.tex` |

Stable labels and proof dependencies appear in [the response](RESPONSE_TO_V148_REPORT.md) and [the scope audit](PROOF_SCOPE_AUDIT_V149.md). Numbered theorem/page concordance is generated in `evidence/THEOREM_LOCATOR_V149.json` by the build.

## Scope

The all-base theorem is an equivalence of **effective** stacks on explicitly defined scheme-theoretic strata. The original algebra stack still has nonlinear substitution inertia and an ineffective right matrix group. Fibrewise conditions are not substituted for equations over nonreduced bases. The proper-reduction moving inverse still recovers the actual source bundle and one constant left transformation.

## Review documents

- [Response to the v148 report](RESPONSE_TO_V148_REPORT.md)
- [Issue-by-issue matrix](ISSUE_MATRIX_V149.json)
- [Proof-scope audit](PROOF_SCOPE_AUDIT_V149.md)
- [Literature audit](LITERATURE_AUDIT_V149.md)
- [Source lock](SOURCE_LOCK_V149.json), [nondeletion audit](NONDELETION_V149.json), and [build receipt](evidence/BUILD_RECEIPT_V149.json)

The full Ballico 1993 theorem/proof comparison remains unresolved. Neither historical priority nor a journal decision is certified.

## Other publication objects

[applications.pdf](applications.pdf) remains a separate manuscript, with corrected revision-149 PDF metadata. [archive-v144.pdf](archive-v144.pdf) remains the complete non-submitted historical archive. Neither is an unstated source of proofs needed in the principal article.

## Reproduction

From a checkout of this revision branch, with Python, SymPy 1.14.0, NumPy 2.3.5, a TeX Live installation including amsart and lmodern, and poppler-utils:

```sh
P=papers/A2-v17-boundary-information-coarsening/article/v149
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python "$P/revision_v149.py" assemble
A2_SOURCE_COMMIT=$(git rev-parse HEAD) python "$P/revision_v149.py" build
```

Assembly preserves all v148 source files and checks the controlling review blob when present. The isolated GitHub workflow additionally enforces the predecessor source lock and allowed write paths. Twenty-six scripts, including the inherited twenty-five and the new exact regression, are executed. Three-pass native builds resolve cross-references for all three manuscripts. Computational checks are finite witnesses, not universal proof certificates.
