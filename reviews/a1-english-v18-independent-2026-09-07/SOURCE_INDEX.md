# Sources, coverage, and execution limits — A1 v18 review

## Immutable source selection

Repository: `TrillionniumFoundation/theta-theory`. The reviewed branch was `revision/a1-english-v18-structural-classification-2026-09-07`, pinned to `be8effe038608bef255fa97318a9ee3b4434af2d`. The commit is dated 7 September 2026, 00:42:42 UTC. Its parent is the v18 preparation commit `311bed64562a4774dc78c586e365d22c89438453`, whose parent is the controlling v17 report `a2adb648c08b3c9e803e916f533605203963ee35`. The preceding submission is `1f3838d89a5820b853d1e4b78194293b23e70bd2`.

The GitHub branch list and commit ancestry, not conversational memory or a guessed branch name, determined the source. Reads used the connected GitHub API with explicit commit references. A later branch change would not change the object reviewed here.

A source URL can be formed by appending a path below to:

`https://github.com/TrillionniumFoundation/theta-theory/blob/be8effe038608bef255fa97318a9ee3b4434af2d/`

All mathematical labels below refer to `papers/A1-english-v18/`. Stable labels are used instead of inventing PDF page numbers or compilation-dependent theorem numbers.

## Coverage of the eleven new named results

| File / label | Scope of inspection | Disposition |
| --- | --- | --- |
| `sections/structural_classification.tex`, `lem:v18-normalized-rank` | Full statement and proof; actual versus adjoined evidence direction | No mathematical objection found |
| Same file, `thm:v18-rank-classification` | Full statement and proof; global cover, mass, randomization, zero rank, causal update, uniformity | No essential missing step found under the printed hypotheses |
| Same file, `lem:v18-image-mass` | Full statement and proof; boundary dimension, graph format, full kernel integration and report evidence | No mathematical objection found |
| Same file, `thm:v18-moment-strata` | Full statement and proof; finite coefficient minors, interior moment body, density perturbation | No mathematical objection found |
| `sections/affine_geometry.tex`, `thm:v18-affine-classification` | Full statement and proof, including weights, all budgets, rank-zero endpoint | No mathematical objection found |
| Same file, `lem:v18-projective-law` | Exact posterior, both report branches, inverse, determinant, density bounds | No mathematical objection found; independent symbolic checks |
| Same file, `lem:v18-thick-linear` | Whole-support cover and projected ellipsoid lower bound, including short axes | No mathematical objection found |
| Same file, `cor:v18-affine-invariant` | Dependence on integer-envelope lemma, zero padding and eventual slope | No mathematical objection found |
| Same file, `prop:v18-interior-example` | Actual prior integrals, positive likelihoods, posterior derivative and zero endpoint | Exact independent identities agree |
| `sections/universal_attainment.tex`, `thm:v18-universal-pairing` | Both implications, normalization and compact-family minorization | No mathematical objection found; E18.1 requires a prior-work comparison |
| Same file, `cor:v18-matched-spaces` | Evaluation-rank argument and squared determinant | No mathematical objection found |

This table records proof inspection, not formal verification. The eleven diagnostic groups in `INDEPENDENT_CHECKS.json` are not eleven proof certificates and do not correspond one-to-one to these results.

## Source object identifiers

| Path within the manuscript directory | Git blob SHA |
| --- | --- |
| `main.tex` | `453da995df4a6f0542e085a2f5e80546e176c65f` |
| `sections/structural_classification.tex` | `a196172c7eab3ee45e97d3e6383d8af330473c40` |
| `sections/affine_geometry.tex` | `f72755147e01c7cdbf07288631bb2c4af5d37c8c` |
| `sections/universal_attainment.tex` | `8811f08808aaa1274a6022191eaa067dd594701a` |
| `sections/positive_history.tex` | `64f45c36bb0108d983dbaace55b35c502d812149` |
| `core/03_transversality.tex` | `6395724ba2c4bed3ead19178a1cfe8206f9a3824` |
| `core/06a_attainable_filtration.tex` | `fedb4c3421227a6c8060d32d2091a5d65ff9a9a6` |
| `core/06b_collision_geometry.tex` | `e0b9ba68173fc2b50f9e9fc30038959484f2ce96` |
| `sections/circular.tex` | `98072475fe13197d25f41f7c45f614786602c4b6` |
| `sections/operational_reconstruction.tex` | `584859638569dca920444f0c1444555d6868167b` |
| `build.py` | `0b19fc32d5f0b241d012db8652a715e08c17682a` |
| `history/build_v17.py` | `0dceca2b90132610c51554886da34de8d47074a4` |
| `validate.py` | `3d5149043c72a426c012d193ece652cbbe9529d7` |
| `history/V17_SOURCE_MANIFEST.json` | `e8870117088145c9db0f71fc38e9be0ff0d27de2` |
| `validation/EXECUTION_REPORT.json` | `a36fb5d5cf193b6e5bd477eba9ab232649e9a041` |

The inverse-source blob was independently compared with `papers/A1-english-v17/sections/operational_reconstruction.tex` at the preceding submission; they match. The archived v17 source-manifest blob was independently compared with `papers/A1-english-v17/SOURCE_MANIFEST.json` at the preceding submission; they match. These are two specific source-identity checks, not a full independent preservation audit.

## Additional inspected material

The current `README.md`, introduction, response to the v17 referee, the v17 referee's principal recommendation and analysis, `LITERATURE_VERIFICATION_V18.md`, and the complete bibliography chain (`references-v18.tex`, `references.tex`, `references-v9.tex`, `references-v16.tex`) were consulted. The inspected bibliography contains no Banaji–Pantea entry.

The principal inherited coverage was the mixed-moment and binomial-tangent arguments; the exact normalized rank and causal representation; the positive-history criterion; the thin-rectangle geometric input; the Leja/Newton collision attainment, checkpoint and causal laws; the full circular section; and the full operational-reconstruction section. The review did not exhaustively reread the numerical/compiler appendices, every uncertainty theorem, or the repository's historical derivation archive. Inherited results not re-audited here are not silently certified by this report.

## Public literature and inspection boundary

The references and precise relevance are recorded in the report. The primary Banaji–Pantea PDF was read at Definition 2.24 and Lemmas 2.32 and 2.36; rendered PDF pages 7 and 11–13 were inspected. The Zhang–Kileel and Forrester primary HTML texts were consulted for their relevant geometric and determinant identities. Only the primary abstract/record of the Saldi–Yüksel–Linder POMDP preprint was inspected. No exhaustive literature-priority search or theorem-level duplication claim about the complete memory laws is made.

## Execution

`independent_checks.py` was written for this review and run locally. It does not import or invoke any repository validator, compiler, proof counter, or prior referee program. The final recorded execution uses exact SymPy algebra, rational integration, and exact minor/product comparisons. The receipt contains the script's SHA-256 digest and the execution environment. Reproduce with:

```sh
python independent_checks.py INDEPENDENT_CHECKS.json
```

The tested environment had Python 3.13.5 and SymPy 1.14.0. The output timestamp naturally changes on rerun. Use ordinary Python execution, not `python -O`, which disables Python assertions. A preliminary development run stopped because nested rational expressions needed `together` before `cancel`; this was a diagnostic-normalization issue, not a manuscript counterexample. The final complete run passed all eleven named groups.

No author validator was independently rerun, no TeX compilation or manuscript-PDF visual audit was performed, and no end-to-end source mutation experiment was executed. The report explicitly distinguishes the static observation about standalone `build.py` from the additional historical-manifest protection in `validate.py`.

The computational receipt is evidence about those finite calculations only. Uniform mass, whole-image covering, arbitrary-prior claims, asymptotic zero products, and minimax optimality are assessed by the mathematical arguments in the report, not inferred from a finite diagnostic count.
