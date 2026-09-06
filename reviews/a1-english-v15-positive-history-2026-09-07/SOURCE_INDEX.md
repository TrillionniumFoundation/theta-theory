# Source index and verification boundary — A1 v15 review

**Review date:** 7 September 2026  
**Reviewed revision:** `revision/a1-english-v15-positive-history-2026-09-06`  
**Reviewed commit:** `e1d0ff2ef04a8641ac77923b664c4d3e8386f212`  
**Reviewed tree:** `4f72df4514e84231086245d6a613a09c2bb80264`  
**Review destination:** `review/a1-english-v15-harsh-referee-2026-09-07`

All submission links below are pinned to the reviewed commit, not to a moving branch. Blob identifiers were returned by the authorized GitHub connection. “Read in full” means the named source body, not all files transitively included by that body. Statements about mathematical checking are limited by the coverage column and the referee report. Source-line ranges below are ranges requested from the repository source, not the line numbers of an escaped JSON tool response.

## Submission sources

### S0 — Revision identity, response, and author-reported verification

[README](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/README.md), blob `aad36cfc242e2685a000f373fcdd739228a3b9d6`.

[Response to referee](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/RESPONSE_TO_REFEREE.md), blob `afd35a52647e5c9ae836e0235766c2c328bcdc37`.

[Proof ledger](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/PROOF_LEDGER.md), blob `df98378a6cfec07c5f05735a037c05b7783411b7`.

Coverage: read in full. Used to identify the response to the preceding review, the intended hierarchy, and the author's claims about retained proofs, build length, and test execution. The author-reported 80-page build, preservation counts, and 68,481 suite assertions were not independently reproduced in this review. They are not substitutes for proof checking.

### S1 — Physical experiment and operational future equivalence

[core/02_experiments.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/core/02_experiments.tex), blob `1bd4f6273d62c860f8a348dcc4f72734dbc388db`.

Coverage: read in full. Stable labels: `eq:channel`, `lem:interior`, `def:future`, `prop:tests`. Checked the finite command interface, positive report likelihoods, posterior normalization, prohibition on uncharged prefix access, and the product future-test space.

### S2 — Manuscript hierarchy and the stated contribution

[main.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/main.tex), blob `3d579eed4335ec18531b073d21c0223328ce34fb`.

[sections/introduction.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/introduction.tex), blob `c4e78e2caa450a0990a3381fc8b6927540e3fe74`.

Coverage: main source body read in full; introduction source lines 1–200 inspected. This includes the principal profile, attainable/global/causal distinctions, standalone attainment statement, circular application, and theorem-level comparison with spectral and real-geometric inputs. Generated includes and the compiled PDF were not treated as read merely because the main source names them.

### S3 — New positive-history criterion

[sections/positive_history.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/positive_history.tex), blob `64f45c36bb0108d983dbaace55b35c502d812149`.

Coverage: read in full and mathematically reconstructed. Stable labels: `prop:product-criterion`, `eq:abstract-minorization`, `thm:positive-attainment`. Audit A1–A2 addresses the exact rank loss, complementary kernel coordinates, evidence-weighted minorization, two-system determinant argument, and dominated-prior compactness.

### S4 — New circular experiment and resolution theorem

[sections/circular.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/circular.tex), blob `5f00ca33fccf0a6bfdc974560b73db86c86aaec3`.

Coverage: read in full using complementary source ranges when a long response was truncated. Stable labels: `eq:circle-cells`, `eq:circle-right-inverse`, `thm:circle-resolution`, `lem:circle-attainment`, `lem:circle-query-metric`, `eq:circle-update`, `cor:circle-phases`. Audit A3–A6 reconstructs the full physical acquisition/observation/covering/converse/causal chain, including zero contrast and the integer label budget. Independent diagnostics are in S12.

### S5 — General bounded dual and retained directional ambiguity

[sections/bounded_dual.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/bounded_dual.tex), blob `87fcf663998ed7ea8e531c260ec9b25f7477f46d`.

[sections/directional_geometry.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/directional_geometry.tex), blob `59ed97f03742f7263645cd4cf56f93f898a0c693`.

Coverage: both source bodies read in full. Stable labels: `prop:general-bounded-dual`, `lem:flag-covariance`, `prop:ambiguity-ellipsoid`, `cor:prefix-ambiguity`. Checked the whole-cube right inverse, prior normalization, full-flag covariance, width orders, exact prefix constraints, and the event-weighted constant-failure interpretation. Attribution to the preceding audit was read as attribution, not independently recertified provenance for every historical derivation.

### S6 — Retained exact rank and exact causal state

[core/03_transversality.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/core/03_transversality.tex), blob `6395724ba2c4bed3ead19178a1cfe8206f9a3824`.

Coverage: read in full. Stable labels: `lem:mixed-moment`, `lem:binomial-tangent`, `thm:rank`, `thm:causal`, `eq:sparse-update`. Checked the separated product tangent, full-support mixed pairing, normalized rank, invariance-of-domain lower bound, and factor-to-moment changeover.

### S7 — Retained intrinsic collision geometry

[core/06b_collision_geometry.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/core/06b_collision_geometry.tex), blob `e0b9ba68173fc2b50f9e9fc30038959484f2ce96`.

Coverage: source lines 1–395 inspected. This covers the complete Leja scale lemma, normalized Newton attainment lemma, intrinsic checkpoint theorem, intrinsic causal theorem, and intrinsic bit-law proof. The later collision-tree developments and examples were not freshly audited in full. Stable labels: `lem:leja-scales`, `lem:newton-attainment`, `thm:intrinsic-checkpoint`, `thm:intrinsic-streaming`, `eq:formal-multiindex-update`.

### S8 — Retained thin-rectangle covering input

[core/06a_attainable_filtration.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/core/06a_attainable_filtration.tex), blob `fedb4c3421227a6c8060d32d2091a5d65ff9a9a6`.

Coverage: source lines 1–165 inspected, including the dimension-truncated real variation and zonotope argument in `lem:tame-rectangle`. The tail of this source and its other retained results were not read in full. The primary real-geometric inputs were checked at L1–L2. The all-integer-budget argument in the new circular proof was separately checked in S4.

### S9 — Retained common-name law

[sections/uncertainty_geometry.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/sections/uncertainty_geometry.tex), blob `89600893e2d8ac7641352d8003fefee230ccfd5f`.

Coverage: source body read in full. Stable labels: `thm:sharp-common-moments`, `lem:overlap-tilt`, `lem:uniform-collision-ambiguity`, `cor:advice-saturation`. Checked the interior-name information convention, prior-tilt separation, overlapping history laws, combination of lower bounds, and the upper proof's invocation of common construction and profile stability. The invoked numerical appendices and the separate collision-intersection example supplying its geometric profile were not independently re-proved here. Reading a corollary's deduction does not certify an uninspected dependency.

### S10 — Persistent resource and causal input access

[core/06_streaming.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/core/06_streaming.tex), blob `e662f435a3a485542606b759b7a3129f298cd865`.

Coverage: source lines 1–145 inspected. Stable labels: `def:finite-state`, `eq:brier`, `lem:lipschitz`, `thm:stream-upper`. Checked that only the previous label and current command/report are available to a transition, that the clock and program are read-only, that a future query is revealed only after the index, and that only one checkpoint/query experiment is executed in a run.

### S11 — Bibliography inputs

[references.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/references.tex), blob `2c655f3185d6301a327cc494d390f6a39538aee2`.

[references-v9.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/e1d0ff2ef04a8641ac77923b664c4d3e8386f212/papers/A1-english-v15/references-v9.tex), blob `8bab36ef02df6af551c3a000213ce17114108c86`.

Coverage: both read in full. Neither L3 nor L4 appears in these bibliography inputs. This finding supports a positioning request, not an allegation of plagiarism, an assertion of exhaustive prior-art search, or a conclusion that the principal theorem is already known.

### S12 — Newly executed independent review diagnostics

`reproduce_review.py` and `EXECUTION.json` in this review directory.

Script SHA-256: `7b406a8a4bd16e61a0c5017232b20d0a9126d9d63150c343e84b7da8e3f4f22d`.

Execution: Python 3.13.5; 1,800 exact arithmetic assertions; five deliberate negative-control families detected. No author helpers or suites imported. No PDF rebuilt. The program is a finite algebraic diagnostic, not a transducer implementation, a continuum-uniform proof, or a formal verification system.

Run from this directory:

```sh
python3 reproduce_review.py --output EXECUTION.local.json
```

The output records the running interpreter and script digest. On a different Python version that version field may differ; the mathematical assertions and fixture counts should agree. Failure raises an exception rather than emitting a new successful receipt.

## R — Controlling previous review

[Referee report on revision 14](https://github.com/TrillionniumFoundation/theta-theory/blob/3d58bb33ae122ebb2430874e2a57a5863e6a876a/reviews/a1-english-v14-geometric-2026-09-06/REFEREE_REPORT.md).

Review commit: `3d58bb33ae122ebb2430874e2a57a5863e6a876a`. Report blob: `db5559a523edaf92df0e40593ab5c1d15e8c38c7`. Its reviewed submission was `ffb9214b0fc7e218d6183c1f81bccb3e47587421` on `revision/a1-english-v14-geometric-response-2026-09-06`.

Coverage: the recommendation, principal mathematical findings, E14.1–E14.2, editorial refinements and closing boundary were inspected. The prior execution material was not rerun. Used to track addressed requests and avoid reopening closed issues without new evidence. The prior report is not used as an independent proof certificate for v15.

## Primary literature checked during this review

### L1 — Rational and semialgebraic regularity

Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4 (2025). [Versioned primary text](https://arxiv.org/html/2311.05116v4).

Inspected Lemmas 2.17–2.18: regularity bounds for rational images and bounded-format semialgebraic sets. Relevant to the upper covering input, not a measure on attainable histories. This was a focused check of the invoked results, not a review of every application in that paper.

### L2 — The real variation inequality

G. Comte and I. Halupczok, *Motivic Vitushkin invariants*. [Versioned primary text](https://arxiv.org/html/2206.15412v2).

Inspected the introduction, equations (4)–(5), which recall the real affine-section variations and real metric-entropy inequality. The current manuscript uses those real statements, not the article's later nonarchimedean theorem.

### L3 — Exact Bayesian Fourier representation and update

E. van den Berg, *Efficient Bayesian phase estimation using mixed priors*, Quantum **5** (2021), 469. [Publisher PDF](https://quantum-journal.org/papers/q-2021-06-07-469/pdf/); [author preprint PDF](https://arxiv.org/pdf/2007.11629).

Inspected Section 2.2, particularly equations (12)–(15), and the subsequent coefficient-growth discussion. Page 4 of the preprint was also visually checked. This supports the representation/update comparison, not a claim that the paper proves the present finite-label minimax formula. A publisher-PDF screenshot failed; the corresponding preprint page was successfully rendered. This visual check concerns literature, not the A1 PDF.

### L4 — Reduced-contrast likelihood and Bayesian coefficient recursion

B. de Neeve, A. V. Lebedev, V. Negnevitsky and J. P. Home, *Time-adaptive phase estimation*, Physical Review Research **7** (2025), 023070. [Publisher record](https://doi.org/10.1103/PhysRevResearch.7.023070); [inspected preprint](https://arxiv.org/html/2405.08930v1).

Inspected Section II, equations (1)–(3), and Section IV of the preprint; publication metadata checked at the publisher. The reduced-contrast likelihood and Fourier recursion are pertinent prior representation machinery. The objective is phase estimation, not the present independent future-query squared loss. Coefficient storage and fixed persistent labels are different resources.

## What these sources do not establish

No exhaustive novelty search or priority adjudication was performed. No existing work containing the identical positive-history or circular fixed-label theorem was identified in the sources checked. The journal-level recommendation is the referee's stated significance judgment, not a theorem about publication standards. The author's program, historical reviews and derivations remain intact; this review introduces only its own new files.
