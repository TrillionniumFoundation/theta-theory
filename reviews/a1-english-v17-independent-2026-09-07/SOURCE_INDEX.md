# Source index, provenance, and coverage for the A1 v17 review

## Submission identity

Repository: `TrillionniumFoundation/theta-theory`.

Reviewed branch: `revision/a1-english-v17-referee-response-2026-09-07`.

Reviewed commit: `1f3838d89a5820b853d1e4b78194293b23e70bd2`, whose GitHub commit timestamp is `2026-09-06T20:37:20Z` (7 September in Singapore). The branch was identified by enumerating matching revision branches and inspecting its commit history, not by assuming that the default branch contained the latest paper.

Immutable manuscript directory: [A1 English v17 at the reviewed commit](https://github.com/TrillionniumFoundation/theta-theory/tree/1f3838d89a5820b853d1e4b78194293b23e70bd2/papers/A1-english-v17).

Directory tree object: `b583f5c8fca86b57451eaf1ca58dec912ff7c938`.

The v16 directory tree returned in the pinned repository tree is `19d6e8a58c53826f3b9b1e7ec5e328284e8d7a5a`. Both this tree and the v17 directory tree point to the identical `core/` tree `ec90bdd89964db07fb2cab26e973ee93fd4c610c`. This identity was read directly through GitHub's Git-tree API. It verifies byte preservation of that subtree only; it is not a proof-preservation run over the compiled manuscript.

## Primary manuscript sources inspected

All paths below are relative to `papers/A1-english-v17/` at the reviewed commit. “Complete” means the relevant file content was obtained through the connector, using overlapping range reads where needed. A partial range is deliberately not described as a complete audit of that file. Mathematical attention was concentrated on the claims identified in the report, not every typographical detail of every returned paragraph.

| ID | Path and coverage | Git blob identifier | Use in the review |
| --- | --- | --- | --- |
| S1 | `main.tex`, complete | `2e076299956c8eb6d8e5c8162bd8dd8c62d1309d` | Title, abstract, and assembly of principal sections and appendices. |
| S2 | `sections/operational_reconstruction.tex`, complete | `584859638569dca920444f0c1444555d6868167b` | All four new results: integer-envelope duality, operational reconstruction, monomial recovery, circular recovery; their hypotheses, proofs, and exclusions. |
| S3 | `sections/positive_history.tex`, complete | `64f45c36bb0108d983dbaace55b35c502d812149` | Normalized product criterion, quantitative minorization, and the two-Chebyshev-system sufficient condition. |
| S4 | `core/03_transversality.tex`, complete | `6395724ba2c4bed3ead19178a1cfe8206f9a3824` | Mixed-moment positivity, actual binomial tangent, normalized rank, and continuous causal state representation. |
| S5 | `core/06b_collision_geometry.tex`, complete across overlapping reads | `e0b9ba68173fc2b50f9e9fc30038959484f2ce96` | Leja pivots, complete Newton attainment, intrinsic checkpoint and streaming proofs, collision-tree and intersecting-locus example. |
| S6 | `sections/circular.tex`, complete | `98072475fe13197d25f41f7c45f614786602c4b6` | Continuous command model, acquisition submersion, Fourier query metric, paired scales, and weighted causal update. Its nested context file was not separately audited. |
| S7 | `sections/structural_comparison.tex`, complete | `c9c477ed7b1234be2e87b5e17a7c2e3f41e97f7a` | Corrected finite-versus-continuous command language, contribution comparison, and scope of the inverse. |
| S8 | `sections/introduction.tex`, lines 1--200 | `b28361a59a6b465888f450aa78e4a76654ed6492` | Main problem setup, forward and inverse framing, command continuity, and fixed-horizon circular scope. |
| S9 | `sections/classical.tex`, complete | `86f1ca39bfa6a502e4a22e2a08c65aa5f3155a6f` | Arbitrary-prefix Hermite principle and exterior spectral comparison. |
| S10 | `core/06a_attainable_filtration.tex`, lines 1--190 | `fedb4c3421227a6c8060d32d2091a5d65ff9a9a6` | The complete thin-rectangle lemma and proof, including integer budgets and reachable centers; surrounding attainable statements. Not a complete reread of this appendix. |
| S11 | `core/06_streaming.tex`, lines 1--155 | `e662f435a3a485542606b759b7a3129f298cd865` | Resource definition, loss, Lipschitz transition proof, streaming upper proof, and beginning of lower statement. |
| S12 | `sections/directional_geometry.tex`, lines 1--190 | `59ed97f03742f7263645cd4cf56f93f898a0c693` | Full inspected covariance and prior-ambiguity sandwich arguments, including normalized pullback; beginning of lower-moment advice subsection. Nested bounded-dual file and later parts not separately reverified. |
| S13 | `sections/uncertainty_geometry.tex`, complete across overlapping reads | `89600893e2d8ac7641352d8003fefee230ccfd5f` | Interior consistency class, overlap and tilt calculation, physical ambiguity, joint-law dependency, and saturation deductions. Compiler dependencies were not fully reaudited. |
| S14 | `sections/request_conformance.tex`, complete | `858675572b5c84ef0eb666983b9d9ff0f6c26084` | Scope of the request-bound numerical implication; not execution or certification of the underlying compiler. |
| S15 | `build.py`, lines 1--170 | `0dceca2b90132610c51554886da34de8d47074a4` | Location of relocated analytic inputs, definition of operational model, and author-side preservation assertions. Read, not executed. |
| S16a | `references.tex`, complete | `6fd90741f233a2caf6c4275b5de326b0db204b92` | Bibliographic assembly and source attribution. |
| S16b | `references-v16.tex`, complete | `cacb72d8c9e56c0045bb453afd9518511a7f736b` | The two precise Fourier references. |
| S16c | `references-v9.tex`, complete | `8bab36ef02df6af551c3a000213ce17114108c86` | Classical interpolation, quantization, and tame-geometry references. |
| S17a | `README.md`, complete | `fbd8b687ed6e0ac060f782dfd927d68e85436638` | Author's description of the revision and its artifacts. |
| S17b | `RESPONSE_TO_REFEREE.md`, complete | `a1e103ec1dd3f2c641855a3741cc4505116daedd` | E16.1 and E16.2 responses, novelty qualifications, and claimed validation scope. |

A file's Git identifier is supplied to make this coverage reproducible. It does not mean its contents were copied into the local runtime or that its proofs were mechanically checked.

## Controlling earlier report

The prior report was retrieved from commit `0ef7e8bd90c0767b7fdc0f2bd175548242e39cec`, path

`reviews/a1-english-v16-independent-2026-09-07/REFEREE_REPORT.md`.

[Immutable prior report](https://github.com/TrillionniumFoundation/theta-theory/blob/0ef7e8bd90c0767b7fdc0f2bd175548242e39cec/reviews/a1-english-v16-independent-2026-09-07/REFEREE_REPORT.md).

Its recommendation, stated correctness disposition, and E16.1/E16.2 findings were read. Its companion numerical counts were not adopted as present execution, and its recommendation was not treated as a mathematical premise. The present report explicitly closes the corrected wording item rather than repeating it.

## Public primary-source checks

These checks were made on 7 September 2026. Descriptions below state the portions actually consulted, not an exhaustive literature audit.

**P1.** E. van den Berg, *Efficient Bayesian phase estimation using mixed priors*, Quantum 5 (2021), 469. [Published article](https://quantum-journal.org/papers/q-2021-06-07-469/), [publisher PDF](https://quantum-journal.org/papers/q-2021-06-07-469/pdf/). Section 2.2, equations (12)--(15), was checked in parsed text and on a rendered screenshot of printed page 4. This supports the attribution of Fourier representations and updates. It is not treated as a source for A1's finite-label minimax law.

**P2.** B. de Neeve, A. V. Lebedev, V. Negnevitsky, J. P. Home, *Time-adaptive phase estimation*, [arXiv:2405.08930v1, HTML](https://arxiv.org/html/2405.08930v1). Section II, equations (1)--(3), was inspected for the reduced-contrast likelihood and Fourier Bayesian update. The report's comparison is confined to that representation/update content and the difference of resource and loss; it does not claim a new exhaustive assessment of every numerical method in this source.

**P3.** G. Comte, I. Halupczok, *Motivic Vitushkin invariants*, [arXiv:2206.15412v2](https://arxiv.org/pdf/2206.15412v2). The parsed introduction on printed pages 3--4 explicitly gives the classical real definitions and entropy inequality (4)--(5) and attributes the underlying real theorem. The nonarchimedean results are not being substituted for a real inequality.

**P4.** Y. Zhang, J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116v4](https://arxiv.org/pdf/2311.05116v4). The parsed definition of regularity and Lemma 2.18 on printed page 11 were checked for the bounded semialgebraic section-complexity input. No sharp constant from that lemma is claimed or needed in the present review.

PDF screenshot requests for P3 and P4 failed in the retrieval tool; their mathematical text was available. No visual inspection of those two PDFs is claimed. Retrieval of some alternative HTML/PDF URLs also failed before the accessible primary versions above were obtained. No allegation about priority, a missing citation, or an incorrect bibliographic entry is based on a failed retrieval. The other references in the manuscript were not all independently verified in this round.

## New execution and deliberate limits

`verify_review.py` is a new standalone diagnostic program. It uses no network, imports no author code, and does not call earlier review programs. `EXECUTION_REPORT.json` is the receipt for its actual successful execution. The local script's SHA-256 and Python version are in that receipt.

The review did **not** rebuild the submission PDF, inspect its published page layout, verify all author-side artifact hashes, rerun the complete compiled proof-preservation validator, or test every inherited synthesis/precision contract. It does **not** claim a formal proof of all statements in the manuscript. Git-tree equality of `core/` is a separately established and much narrower fact.

The source review, mathematical calculations, and finite diagnostics support the dispositions stated in the report. They do not constitute journal endorsement, a guarantee of completeness, or an exhaustive negative claim about the literature.
