# General Theta Foundations I — v17 referee entry

**Full English revision, 23 September 2026.**

**Article:** General Theta Foundations I: Adaptive Testing and Collision-Sensitive Comparison.

## Exact review scope

The controlling report is the second independent v16 report at `b59d8527c8edc0361be3085604bcf3a920dbfbda`, report blob `e5da7aad09a5a5df84b16d6e8daa76e5dc7054c0`. The earlier pipeline-aware v16 report at `f52d4afe6a688a2c440d4f9f351e3664e1f08a2a`, blob `59dc90d92c5dfc0b0448114c4d27907790359e3d`, is also addressed. Both reviewed the complete v16 submission `5941223e297f6c54583d729cc292831c183277e9`. The revision branch starts from the controlling review, not from an older GTF submission.

## Read the revision

| Entry | Purpose |
|---|---|
| [Full article — 59 pages](papers/GTF-I-v17-intrinsic-adaptive-testing/paper.pdf) | Canonical theorem–proof manuscript; [LaTeX entry](papers/GTF-I-v17-intrinsic-adaptive-testing/main.tex) |
| [Complete development — 256 pages](papers/GTF-I-v17-intrinsic-adaptive-testing/complete-development.pdf) | Preserves the predecessor mathematical bodies and historical introductions |
| [Standalone submission sources](papers/GTF-I-v17-intrinsic-adaptive-testing/evidence/SUBMISSION_SOURCES.zip) | 26 local canonical TeX inputs plus README; compiles without historical revision directories |
| [Point-by-point referee response](papers/GTF-I-v17-intrinsic-adaptive-testing/RESPONSE_TO_REFEREE.md) | E16-R2.1–E16-R2.10, the earlier E16.1–E16.8, and technical comments |
| [Proof ledger](papers/GTF-I-v17-intrinsic-adaptive-testing/PROOF_LEDGER.md) | Hypotheses, proof locations and mathematical boundaries |
| [Literature comparison](papers/GTF-I-v17-intrinsic-adaptive-testing/LITERATURE_COMPARISON.md) | Theorem-level classical subtraction and remaining priority questions |
| [History audit](papers/GTF-I-v17-intrinsic-adaptive-testing/HISTORY_AUDIT.md) | GTF ancestry, historical B4/C2 requirements and the eleven-component program |
| [Typed pipeline graph](papers/GTF-I-v17-intrinsic-adaptive-testing/PIPELINE_GRAPH.json) | Preserved prior declarations and new scoped microscopic dependencies |
| [Preservation map](papers/GTF-I-v17-intrinsic-adaptive-testing/PRESERVATION_DIFF.md) | All original files unchanged; exact annotations to three local copies |
| [Small exact adaptive certificate](papers/GTF-I-v17-intrinsic-adaptive-testing/evidence/ADAPTIVE_CERTIFICATE.json) | Three weights, nine-term nonnegative identity and seventeen rational coefficients |
| [Collision certificate](papers/GTF-I-v17-intrinsic-adaptive-testing/evidence/COLLISION_CERTIFICATE.json) | Rational nongrazing and detector margins |
| [Build receipt](papers/GTF-I-v17-intrinsic-adaptive-testing/evidence/BUILD_RECEIPT.json) | Actual source commit, hashes, theorem pages and executed checks |
| [Complete source closure](papers/GTF-I-v17-intrinsic-adaptive-testing/evidence/COMPILED_SOURCES.zip) | 446 pinned inputs needed to rebuild the entire development |

## Source and publication identities

- Initial remote scope commit: `9801f3cecadc03140e6e2c4fe827b49276315c73`.
- Complete source transport and isolated workflow: `cdb943a856aa398c69c3b6970b81c63045516ff4`.
- First complete plaintext source: `1d24d88d01e59695d0c92e7f8a061664ef381d49`.
- Organization-only refinement: `0283c422c50ef4ac58d8ef8d0d457a8cf34e5680`.
- **Final mathematical source and exact successful build checkout:** `f93ab1a6c8c5255a3398f1884c5af05d65ced73a`.
- **Final PDF/evidence publication:** `978800e2f1d8678291d7a4b1f0dcc4396235f8b5`.
- Final successful GitHub Actions run: `35836335685`; job `107100581547`; artifact `10739552465`.
- Working branch: `revision/general-theta-foundations-i-v17-intrinsic-adaptive-testing-2026-09-23`.
- Frozen referee branch: `revision/general-theta-foundations-i-v17-intrinsic-adaptive-testing-referee-ready-2026-09-23`.

The first build also succeeded. Final layout review moved two inherited certificate subsections back into the intrinsic-comparison section; all theorem files stayed byte-identical. The final build reran the complete verification rather than reusing the first receipt. The final source differs from the original transport by exactly the hash-guarded core relocation and its manifest entry, recorded in the dedicated workflow.

This root entry is documentation only. It changes no mathematical source, PDF or source-bound receipt. Relative to the controlling review, all changes are additions under the new v17 directory, its dedicated workflow, and this entry. No original file is modified or deleted. This delivery updates no earlier review/revision, default or A2 branch reference.

## Main proof locations in the final canonical PDF

| Result | Location |
|---|---|
| Independent adaptive testing on the original nonconvex behavior image | Theorem 3.1, p. 15 |
| Behavior-dimension degree/support bound and attained finite-level moment dual | Theorem 3.3, p. 16 |
| Three-weight certificate with seventeen positive rational coefficients | Proposition 3.5, p. 17 |
| Exact marked private/visible versus hidden-two-selector values | Theorem 4.1, p. 19 |
| Uniform collision geometry creating a transverse informative signal | Lemma 4.2, p. 20 |
| Same-budget collision-sensitive physical resource separation | Theorem 4.3, p. 21 |
| Whole-process posterior stability under marked variation | Theorem 5.1, p. 23 |
| Microscopic Gaussian-observation optional-projection limit | Theorem 5.3, p. 24 |

The independent-test approximation error is at most `4 R a/sqrt(n)` in observable affine dimension `a` and diameter `R`. At most `(n+1)^a` occupied test coefficients and `(n+2)^a` moment-dual atoms suffice. These are test degree/support bounds, not a polynomial-time claim for nonconvex verification or an intrinsic coefficient-bit bound.

In the physical example, the same width-one retained register has private/visible error greater than `9/20`, while an independent hidden two-valued selector gives error less than `13/100`. The underlying exact marked values are `sqrt(5/2)-9/8` and `1/8`. The physical discrepancy is below `1/300`. A nontrivial diameter interval creates a unique nongrazing collision; removing that collision with the same preparation and detector makes every deficiency zero. Feedback is a sensor gate chosen after the first report, not a mechanical forcing or freely retained emitted history.

## Verification actually performed

The final successful remote build checked 402 inherited files and 43 new manifest-listed inputs. The manifest itself gives the 446th source-archive entry. All 812 v16 complete-development labels are preserved, 666 retained labels resolve, and the 179 shared canonical labels have identical numbering in both views. Both manuscripts stabilized in three native LaTeX passes. The build rejected unresolved references/citations, duplicate labels and overfull boxes.

The new exact suite executed 120 checks with matching ordinary and optimized Python results. Eight designated incorrect variants were rejected in each mode, for sixteen negative-control executions. All sixteen predecessor diagnostic suites were rerun successfully. Both referee report blobs were checked from Git. The pipeline checker verifies source identity and declared contracts, not analytic truth.

The small certificate stores seventeen rational coefficients with maximum stored-integer bit length nineteen. Its JSON is 1,654 bytes. Its proof also uses three explicit cubic weights and a nine-term nonnegative identity. For comparison, the retained v16 example has 9,409 coefficients with maximum stored-integer bit length 148; the recomputed compact numeric array is 431,449 bytes. This is an exact example comparison, not a universal complexity theorem.

The final remote artifact was downloaded and checked against GitHub's SHA-256 digest. All 44 plaintext revision files were compared with the final prepared sources. Both PDF hashes and page counts, and both source-archive hashes, were checked against the receipt. Extracted text bounds were checked on all 315 PDF pages. Twenty selected pages across the two views were rendered and inspected, including the new theorem statements and physical bounds. The standalone source archive was additionally extracted into a clean directory and compiled in isolation for three passes to 59 pages, with no unresolved references or overfull boxes. Neither source archive contains font files.

- `paper.pdf`: SHA-256 `6f25b42250e22f96df6b8715d11623a63be116f0457662e0f551274bdc2bd588`.
- `complete-development.pdf`: SHA-256 `a17207665449f820f41d55fbc0d5bd979d56a1ebb3c5348e93fe06f4c3b95d0d`.
- `COMPILED_SOURCES.zip`: SHA-256 `30b615e4c7c8eb6b8d6021511c8ac61436010e56c623cd32d8d5bfcb16936b1f`.
- `SUBMISSION_SOURCES.zip`: SHA-256 `49eb157fbcb408a5ac7d8f356fb76e95264ba68e8e0b3d098f6b90eed810147d`.
- Downloaded final artifact: SHA-256 `afb67b427556058b5200aa28986827669d9a5a21c8d7058a80fe3f9839c1f966`.

## Matters reserved for independent review

The adaptive game receives a proposed behavior law, not an unknown physical mark; it is not an ordinary one-sample randomization theorem. Its moment dual does not convexify the executable private simulator image. The scattering theorem is fixed-particle and single-collision, not particle-number-uniform kinetic scaling. The new C2 result supplies a proved whole-process optional-projection criterion in a stated microscopic observation class; it does not establish every historical C2 conclusion. The full historical B4 action, uniform hierarchy corrector and nonlinear kinetic limit remain separate requirements. All full-historical-target closure flags are retained as false. The primary A2 geometric chain remains independent.

Original-text proof-level comparison with Norberg remains unverified. The revised literature analysis records that limitation without inferring absent theorems from an abstract. The accessible Bernstein/hypercube and filtered-comparison originals are compared at named theorem locations. No independent analytic certification, journal acceptance or official journal referee approval is asserted.

## Reproduce

For the canonical article alone, extract `SUBMISSION_SOURCES.zip` and run `pdflatex main.tex` three times. For the full source-bound verification, use a checkout containing the inherited source directories:

```sh
python -m pip install -r papers/GTF-I-v17-intrinsic-adaptive-testing/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v17-intrinsic-adaptive-testing/build.py
```

A later rebuild records its actual checkout. The published PDFs and receipt remain bound to `f93ab1a6c8c5255a3398f1884c5af05d65ced73a`, not to this subsequent documentation commit.
