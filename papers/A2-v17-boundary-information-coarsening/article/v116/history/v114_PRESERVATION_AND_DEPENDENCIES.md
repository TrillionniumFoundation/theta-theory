# Preservation and proof-dependency record

Frozen baseline: independent v113 review `63daaeee1da5a1ee3ac569584e06f55081073da0`.
All earlier manuscripts, reports, mathematical derivations, PDFs and receipts stay unchanged on this branch. Relative to that base, changes are additions under `article/v114/`, the v114 root index, and the v114 branch-scoped workflow only.

## Preservation

All 134 labels and 25 bibliography keys in the v113 manuscript survive in the compiled v114 manuscript. There are 169 labels after the additions. The following six substantive parts are byte-identical to v113:

- `parts/02-global-geometry.tex`
- `parts/02b-component-structure.tex`
- `parts/03-realization-stability.tex`
- `parts/04-statistical-experiments.tex`
- `parts/04b-uniform-constants.tex`
- `parts/05-complements.tex`

`01-contact-native.tex` changes its initial heading and relocates the unchanged codimension theorem to `00-introduction.tex`; its contact, native and threshold arguments remain. `01b-structural-overview.tex` retains its mathematical content and updates cross-references and the primary-source status. `02c` changes the exact reducedness citation. `02d` adds explicit references to the new descent proofs. `02e` retains the old node proof and adds the primary decomposition and relative proof package. `02f` keeps every stated phase/residual theorem and replaces the loop-based descent paragraph with its algebraic proof. `references.tex` retains all keys and corrects the Stacks entry.

The original six-file preservation diagnostic code is retained as `verify_v113_diagnostics.py`, invoked for its finite mathematical diagnostics only. The new verifier performs preservation against the **whole** v113 manuscript, not only those six older files.

## Dependencies without circularity

1. Theorem 2.1 (general polar tangent sequence) is proved by differentiating the incidence and linear duality. Its quadratic identification is an explicit dual-frame calculation.
2. Theorem 2.2 (global singular support/Fitting ideals) follows from the cotangent presentation, the stated pure expected-codimension hypothesis, and Schur elimination. It does not use the binary component classification or the node theorem.
3. The inherited full-range codimension theorem and expected-grade proposition establish that hypothesis for binary subseries when `a <= b`; they do not use the new global singularity theorem.
4. The orientation propositions prove descent independently, using the exact-rank parameterization and its determinant square class. Their reference to the exceptional table names the cases; it does not assume their irreducibility.
5. The all-dimensional component theorem keeps its rank optimization, incidence projection, explicit excess example and generic-reducedness proofs, with the formal descent propositions supplying that step.
6. The relative residual divisor uses the **already established** all-dimensional theorem at smaller dimensions. The normal-bundle factorization is a separate linearized bundle calculation. The nonempty wall open uses the residual incidence and an affine lift, not the conclusion that a node exists.
7. The node theorem follows from these three ingredients by analytic implicit elimination. Analytic and completed local rings remain separately identified.
8. The algebraic phase descent is independent of the global component theorem. It enumerates two-point sectors; the general polar theorem supplies the wider higher-product result.
9. Statistical and native arguments are applications and appendices. They supply no hypotheses or premises for the algebraic classification.

## What the global statement does and does not identify

Residual Fitting identities are pullbacks to constant-rank locally closed strata. Full open-chart Schur–Jacobian equations, also for original corank one, retain transverse infinitesimal structure. The manuscript never tries to recover a global scheme solely from its restrictions to reduced strata.

The full expected-codimension singular scheme is specified, but all analytic normal forms, global normalization/conductor data, and every associated prime or smaller component in excess codimension are not claimed. This distinction prevents the new theorem from being mistaken for several different stronger classification problems.
