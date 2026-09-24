# General Theta Foundations I — revision 29

**Intrinsic Continuation Geometry and Causal Memory**  
Qian Qi · 24 September 2026

Controlling r13 report: `9c8161e9df1b017fa2dfb46218a4fa42f42e9bdd`. Reviewed v28 head: `cdc749027c5f7a6f66c572ea498cd15e1b1a3391`. This additive package is on `revision/general-theta-foundations-i-v29-intrinsic-continuation-2026-09-24`, with a separate referee-ready branch after successful publication. It does not write to the pre-existing v29-intrinsic-memory branch or to any older paper/review path.

[Canonical article](paper.pdf) · [LaTeX source](main.tex) · [Response to r13](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Complete mathematical manuscript](complete-manuscript.pdf) · [Complete preserved development](complete-development.pdf) · [Source archive](evidence/SUBMISSION_SOURCES.zip)

## Theorem spine

For a complete finite causal response array, enumerate all normalized residual continuations. Their minimal-face intersection graph and component affine ranks define an intrinsic quantity `s_t`, independent of any analyst-selected certificate family. Every stochastic realization has at least `s_t` states. If each component hull is a simplex, its extreme residuals realize that profile simultaneously through normalized stochastic shifts. The condition and construction are finite and effective for explicit rational or algebraic data.

This complete terminal-channel class is closed under independent products, with multiplicative exact capacity. A full-support product channel at a preparation barrier consequently has an exact q^n peak even under adaptive acquisition and output order.

The binary-query experiment has a more pronounced distinction between dimension and positivity. Its ordinary predictive rank is n+1 for every signal eta>0. Nevertheless its exact whole-schedule peak is

```
n+1 for 0 < eta <= 1/n^2,
2^n for 1-1/n < eta <= 1.
```

Both converses permit adaptive acquisition. The weak regime has an explicit fixed-order online encoder with exactly t+1 labels after t bits; no real-valued accumulator or persistent shared seed is free. The exact law is required at every input/query, not only in average score. Intermediate signals are not classified here.

Minimax contact links the invariant to the marked saddle's five forced response rows. The known-target Brownian five-state decision count, all-fixed-clock peak twelve, and reverse support-boundary jump remain proved in the supporting development. Acquired calibration gives separately priced approximate-score guarantees, not exact reconstruction of an unknown algebraic row.

## Layout and preservation

The current theorem spine precedes supporting appendices containing the entire substantive v28 mathematical body. Its eighteen mathematical input modules are byte-identical copies. The pinned predecessor main Git blob is `f4a82fe0ec5b294bfa9a8d8a299e8bb97fb6f442`. `assemble.py` checks that the old body can be recovered exactly from the new source. No predecessor repository file is altered.

## Reproduction

Use Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7, and a LaTeX installation with AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools and hyperref. From the repository root:

```sh
python papers/GTF-I-v29-intrinsic-continuation/verify.py
python -O papers/GTF-I-v29-intrinsic-continuation/verify.py
python papers/GTF-I-v29-intrinsic-continuation/build.py
```

The source ZIP uses sibling package directories. Extract it into an empty directory and run `python GTF-I-v29-intrinsic-continuation/build.py`. It includes exact prior sources and PDFs needed for reproducibility, and no standalone font files.

The build verifies native assembly, runs new and inherited regression programs in normal and optimized Python, runs deliberately invalid controls, compiles three times, rejects undefined references or overfull boxes, appends the unchanged predecessor volumes, and records hashes and theorem pages. Inspect the actual receipt rather than inferring successful execution from this description.

## Exact boundaries

The geometric theorem is complete on its decidable componentwise-simplicial class, not on all positive realizations or autonomous shared-row machines. Full specified arrays and supported partial laws are distinguished. The new adaptive results concern the declared barrier/query families; they do not change the collision theorem's fixed-clock quantifier. Product laws, additive scores, exact stochastic rows, finite fair-bit devices and acquired calibration are distinct resources. The historical A2/B4/C2 gates are not declared closed by finite-state synthesis. Mathematical and originality claims remain subject to independent review.
