# Proof and dependency ledger — GTF I v2

The numbers below refer to the compiled second revision; stable labels are the primary references. Page numbers are navigational, not evidence of correctness.

| Statement | Stable label | Initial page | Proof obligation and dependency |
|---|---|---:|---|
| Theorem 2.1: acquired-law resolution | `thm:v2-resolution` | 5 | Actual-law submeasure lower bound; same-word exact-suffix hybrid telescope; L2 sum; randomized-label converse. Proved in `revision.tex`. |
| Corollary 2.2: A1 anisotropic transfer | `cor:v2-a1` | 6 | Imports the bounded-format thin-rectangle covering lemma from fixed A1 v37; gives integer-budget reduction, rectangular-marginal converse, and finite-horizon recurrence. |
| Theorem 2.3: conditional block criterion | `thm:v2-blocks` | 7 | Adapted conditional second-moment product bound and geometric sum. No block independence or bounded waiting time is assumed. |
| Lemma 3.1: projective contraction | `lem:v2-projective` | 8 | Classical estimate, attributed to Bushell; finite-dimensional derivative/total-variation proof included. |
| Theorem 3.2: every positive refresh rate | `thm:v2-refresh` | 8 | Explicit transition cross-ratio, invariant projective ball, fixed admissible cover, physical posterior Jacobian with floor gamma/(d+1), actual-law lower bound. |
| Corollary 3.3: intermittent refresh | `cor:v2-intermittent` | 9 | Theorem 2.3 plus invariant permutation modes and a good-acquisition submeasure with its probability retained. Expected checkpoints, not a pathwise supremum. |
| Proposition 3.4: singular acquired dimension | `prop:v2-cantor` | 10 | Cantor cylinder concentration and covers; sign-weighted bi-Lipschitz posterior images; exact resetting causal update. |
| Theorem 4.1: contact/calibration/label law | `thm:v2-singular` | 11 | Clipped-root estimator; all-integer anisotropic cover; paired-data least-favourable nuisance; hypercube testing; arbitrary-decoder label floor. |
| Theorem 5.1: unrestricted control comparison | `thm:v2-control` | 13 | Bellman regularity, finite-reference residual, policy lifting, discounted actual-path telescope. Exact value used in proof only. |
| Proposition 6.1: implicit codebook | `prop:v2-program` | 14 | Integer log-odds enumeration and inward rounding; finite description; certified perturbation allowance. |

## Preservation

`legacy/` is the complete original `papers/GTF-I-v1` tree, including its PDF and original introduction. `main.tex` directly includes, without changing their contents, original sections 02--12 and appendices A/B. Their 32 proof blocks, 12 boundary examples, and 103 labels remain in the compiled revision. The original introduction is not duplicated in the new main article; it remains in the preserved original edition. No original repository file is overwritten by the revision.

The compiled second revision has 16 theorem environments, 7 lemmas, 15 propositions, 4 corollaries, 42 proof blocks, and 12 examples. The change is ten additional proof blocks, not an assertion that every retained or additional statement is novel. The original classical information and experiment identities retain their original attribution.

## Dependency kinds

**New principal proofs within this edition:** Theorems 2.1, 2.3, 3.2, 4.1, 5.1 and their applications, all in `revision.tex`. Their classical ingredients are identified in the text.

**Classical inputs with an included proof:** Positive-matrix projective contraction, elementary quantization concentration, Gaussian two-point/hypercube testing steps, and the Bellman comparison calculations. Their inclusion does not establish priority.

**Imported geometric result used only in a corollary:** A1 v37 `text/analytic_inputs.tex`, label `lem:tame-rectangle`, together with the explicitly stated G/A/C hypotheses in `sections/causal_transfer.tex`. The complete source edition is copied into `source-editions/A1-v37`. The new principal theorems do not depend on this result.

**Comparison, not an imported proof premise:** A2 v112 contact-ray, Poisson-to-Gaussian, and score-compression experiments. These are available in `source-editions/A2-v112/parts/04-statistical-experiments.tex`. Theorem 4.1 proves its own paired noisy experiment, not an unproved equivalence to A2's data.

**Historical model interfaces:** The original LDP, spectral, kinetic, unbounded-operator and phase dependencies remain distinct. See `HISTORY_AUDIT.md`; none is used circularly to prove a result here.

## Verification boundaries

The builder verifies source hashes, retained labels, bibliography resolution, absence of overfull boxes, and the stated finite regressions. It does not turn those checks into theorem verification. `evidence/BUILD_RECEIPT.json` binds the executed checkout and PDF to the source. The author-side rendered-page inspection is separately recorded in `RENDER_REVIEW.json`.
