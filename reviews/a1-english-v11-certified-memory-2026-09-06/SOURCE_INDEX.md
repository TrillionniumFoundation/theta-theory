# Source and execution index

## Submission identity

All S-keys below refer to the immutable submission commit
`f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0` in
`TrillionniumFoundation/theta-theory`, with tree
`e4281eaee6beb548f8bb29126693a272fa7b595b`.

The paper root is
[papers/A1-english-v11](https://github.com/TrillionniumFoundation/theta-theory/tree/f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0/papers/A1-english-v11).
Paths below are relative to that root. Line ranges describe source text actually retrieved, not PDF pages. “Complete” means the file's complete text was read. A range ending inside an argument is not a claim to have audited the rest of that argument.

## Manuscript and implementation evidence

| Key | Source and read extent | Role in this report |
|---|---|---|
| S0 | `main.tex`, `sections/introduction.tex`, `sections/comparison.tex`, complete | Principal claim, input order, theorem-specific literature comparison |
| S1 | `README.md`, `RESPONSE_TO_REFEREE.md`, complete | Author's stated changes, numerical claims, scope and preservation claims |
| S2 | `core/02_experiments.tex`, complete | Positive reports, charged failures, future-only continuation, probe span |
| S3 | `core/03_transversality.tex`, lines 1–180 | Mixed-moment positivity, binomial tangent, normalized rank, beginning of exact causal state argument |
| S4 | `sections/classical.tex`, complete | Arbitrary-prefix Hermite lemma and exterior spectral comparison |
| S5 | `core/05_confluence.tex`, lines 1–170; `core/06a_attainable_filtration.tex`, lines 1–205 | Complete confluent-positive lemma; complete thin-rectangle covering proof including integer budgets; surrounding inherited statements |
| S6 | `core/06b_collision_geometry.tex`, lines 1–350 | Profile definition, Leja scales, uniform attainable flags, checkpoint theorem and principal causal proof; not the entire later example catalogue |
| S7 | `sections/effective.tex`, lines 1–320 | Compact compiler, finite moment evaluation, main digital theorem and most of its proof; not all later calibration details |
| S8 | `sections/certified_resources.tex`, lines 1–340 | Separated floor, uniform resources, radius certificate, adaptive stopping, tolerance version, residual and moment certificates |
| S9 | `sections/certified_resources.tex`, lines 341 through end | Cover/profile comparison, profile-adaptive theorem, arithmetic wording, resource-phase corollary |
| S10 | `finite_compiler.py`, `certified_compiler.py`, complete | Actual offline construction, runtime machine, numerical data and residual/adaptive interfaces |
| S11 | `tests/test_v11.py`, complete | Physical fixtures, negative controls, off-grid domain, separate adaptive fixtures |
| S12 | `SOURCE_MANIFEST.json`, `references.tex`, complete; `.github/workflows/a1-v11-revision.yml` | Three source hash comparisons, literature version pin, publication metadata; no independent verification of the entire manifest/preservation inventory |

R1 is the controlling v10 report at commit
`1aa4599eedca650d34c3778a00f3ad854c2bc9d7`,
[REFEREE_REPORT.md](https://github.com/TrillionniumFoundation/theta-theory/blob/1aa4599eedca650d34c3778a00f3ad854c2bc9d7/reviews/a1-english-v10-effective-finite-memory-2026-09-06/REFEREE_REPORT.md),
source lines 1–130. Its recommendation, principal audit, earlier closures and new defects were read; v11's complete response supplies the point-by-point response being assessed. Earlier opinions are not treated as proof of current correctness.

## Primary public literature consulted

The comparison was targeted, not an exhaustive priority search. Sources were accessed on 6 September 2026.

**L1.** T. F. Gonzalez, *Clustering to minimize the maximum intercluster distance*, Theoretical Computer Science 38 (1985), 293–306.
[Publisher source](https://www.sciencedirect.com/science/article/pii/0304397585902245), DOI 10.1016/0304-3975(85)90224-5. Publisher metadata/abstract were consulted; no assertion is made that the full publisher proof was independently reread. The elementary farthest-first argument was checked directly in the manuscript.

**L2.** N. Saldi, S. Yüksel and T. Linder, *On the Asymptotic Optimality of Finite Approximations to Markov Decision Processes with Borel Spaces*, Mathematics of Operations Research 42 (2017), 945–978, DOI 10.1287/moor.2016.0832.
The bibliography explicitly links [arXiv:1503.02244v3](https://arxiv.org/pdf/1503.02244v3). The retrieved text identifies v3 dated 22 September 2016. Its PDF-index page 31 / printed page 32 labels the discounted bound Theorem 5.2; PDF-index page 34 / printed page 35 labels the average-cost result Theorem 5.3. Section 6 addresses order optimality. This is the version-specific basis of P11.4. Screenshot attempts for those pages failed with cache errors; the claim is grounded in the explicit retrieved theorem text, not a falsely claimed visual inspection. The publisher landing page confirmed the bibliographic identity but did not supply a usable full-text version. No assertion about different numbering in an unexamined final typesetting is made.

**L3.** A. Kara and S. Yüksel, *Near Optimality of Finite Memory Feedback Policies in Partially Observed Markov Decision Processes*, JMLR 23(11) (2022), 1–46.
[Journal article and PDF](https://jmlr.org/papers/v23/20-1152.html). Theorem 12 was read in the journal PDF and visually checked on PDF-index page 14 / printed page 15. It is a finite-window discounted-control conclusion with stability and discount assumptions; it is not an M-label posterior-covering theorem. Relevant assumption text was retrieved; the requested preceding-page screenshot failed.

**L4.** J. Subramanian, A. Sinha, R. Seraj and A. Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12) (2022), 1–83.
[Journal article and PDF](https://jmlr.org/papers/v23/20-1165.html). Definition 7 and Theorem 9 were read and visually checked on PDF-index pages 14–15 / printed pages 15–16. Theorem 17's action-compression statement was retrieved in text at PDF-index page 23; its screenshot failed. These results support the manuscript's distinction between an error-propagation framework and its budgeted finite synthesis, not a claim that either theory contains the other.

The original books/articles behind total positivity, Hermite interpolation and the real entropy inequality were not exhaustively reread in this round. The relevant supplied proofs and the way those analytic inputs are used were inspected. This report makes no independent full bibliography or all-journal priority certification.

## Executed evidence

**X1:** [EXECUTION.json](EXECUTION.json), generated by
[reproduce_review.py](reproduce_review.py).
**T1:** [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md), containing the independent exact arguments.

| Exact imported author source | SHA-256 |
|---|---|
| `finite_compiler.py` | `5e6335160cec538c13f7b0fbfb3d6ad89ec55946734ee7d527dae564ac654fda` |
| `certified_compiler.py` | `6965862f93bd2ef8f107eca30fd53fb3c8ce52e696f99c893a343aad980a226c` |
| `tests/test_v11.py` | `4cfe2c0a6a492cdff3ca87053ce2de541c6ce90fe97f51fa3238122a6019b2b6` |

These exact source copies matched the submission manifest before execution and remained unchanged afterward. The local run used Python 3.13.5. The unmodified suite and the transition mutation each passed 8,207 checks; 775 transition entries changed in the latter. The independent interval and rational-product diagnostics were separately executed by the same review script.

The full baseline/mutation JSON and stdout are reproduced by the script into its selected output directory. The committed compact receipt includes every assertion-category count, mutation counts, exact rational witness values, source hashes, platform information and explicit non-execution list. It does not require storing duplicate author code in the review directory.

## Negative scope statement

No TeX build, manuscript PDF visual inspection, GitHub Actions run, legacy author/referee test rerun, full historical derivation audit, all-eleven-paper review, exhaustive proof-preservation verification, or formal theorem proving was performed in this round. The review does not modify manuscript sources, historical reports, repository administration, or the revision branch. Publication verification is performed separately after the review files are committed.
