# General Theta Foundations I — v10 referee entry

**Full English marked-duality revision, 23 September 2026.**

The controlling referee report is `e5373d129545b269ee4f5477a94542517dbfd0d1`, on `review/general-theta-foundations-i-v9-causal-minimax-harsh-referee-2026-09-23`. This revision adds stronger results while preserving the predecessor development. It is submitted for renewed independent mathematical review, not represented as accepted or independently certified.

## Read the revision

| Entry | Purpose |
|---|---|
| [Full article — 64 pages](papers/GTF-I-v10-marked-duality/paper.pdf) | Canonical theorem–proof manuscript; [LaTeX entry](papers/GTF-I-v10-marked-duality/main.tex) |
| [Complete development — 159 pages](papers/GTF-I-v10-marked-duality/complete-development.pdf) | Includes the preserved earlier mathematical bodies and historical introductions; [LaTeX entry](papers/GTF-I-v10-marked-duality/development.tex) |
| [Point-by-point referee response](papers/GTF-I-v10-marked-duality/RESPONSE_TO_REFEREE.md) | E9.1–E9.7 and the additional technical comments |
| [Proof ledger](papers/GTF-I-v10-marked-duality/PROOF_LEDGER.md) | Proof locations, hypotheses and comparison categories |
| [Literature comparison](papers/GTF-I-v10-marked-duality/LITERATURE_COMPARISON.md) | Classical ingredients, claimed contribution and limits of the priority audit |
| [History audit](papers/GTF-I-v10-marked-duality/HISTORY_AUDIT.md) | Source ancestry, eleven-paper pipeline and current A2 identity |
| [Preservation diff](papers/GTF-I-v10-marked-duality/PRESERVATION_DIFF.md) | Exact changes to the two local predecessor copies; original files unchanged |
| [Build receipt](papers/GTF-I-v10-marked-duality/evidence/BUILD_RECEIPT.json) | Actual source identity, PDF hashes, stable labels and diagnostic results |
| [Complete source closure](papers/GTF-I-v10-marked-duality/evidence/COMPILED_SOURCES.zip) | 238 pinned inputs, including the inherited sources required to rebuild |

## Source and publication identities

- First complete mathematical source commit: `272cb9061f0407c0df1a4a6bb35d20eb60dac4c8`.
- Exact successful build checkout: `c2653682d73571ad01f7c159bb10784f800982b4`. Its only change from the preceding mathematical commit is the dedicated workflow: the missing Latin Modern TeX package was added. All 28 plaintext revision files remained byte-identical.
- PDF/evidence publication commit: `87a877b24ac31110ce1556fb58bde48db7bf6f14`.
- Successful GitHub Actions run: `35789308666`, job `106953703354`; artifact `10720749408`.
- Working branch: `revision/general-theta-foundations-i-v10-marked-duality-2026-09-23`.
- Referee branch: `revision/general-theta-foundations-i-v10-marked-duality-referee-ready-2026-09-23`.

This entry is a documentation-only addition above the publication commit. It does not alter the mathematical sources, published PDFs or their receipt. The earlier review, v9, pre-existing marked-compact v10, default and A2 branches are not modified by this delivery.

## Principal proof locations in the canonical PDF

Theorem 3.3 (p. 10): dominated nonfinite common-encoder duality, with executable public randomization and compact risk functions. Theorem 3.7 (p. 12): width-uniform finite-report approximation of actual marked laws. Theorems 4.3 and 4.5 (pp. 13, 15): operational marked-state minimality and parameter-free reconstruction preserving the actual target. Theorem 5.2 (p. 16): rational output-sensitive exact-state synthesis. Theorem 6.1 (p. 17): three-task private/shared separation, with errors 1/2 and 2/9. Sections 11–12 retain the delayed Gaussian exponent and add a finite-acquisition/table implementation. Sections 13–15 prove the stated positive hidden-Markov, nonlinear finite-state semigroup and one-policy latent-phase consumers.

## Verification performed

The successful remote build checked 210 inherited inputs and 27 new manifest inputs; the manifest itself is the additional source-archive entry. It ran 3,296 finite diagnostic conditions in ordinary and optimized Python with matching results, rejected nine designated incorrect variants in both modes (18 executions), and reran all nine predecessor diagnostic suites. Both manuscript views reached stable references in three native LaTeX passes. The build preserves all 514 v9 companion labels, resolves 501 retained historical labels, and gives the same numbering to 223 shared canonical labels. The logs were checked for unresolved references, duplicate labels and overfull boxes.

The downloaded successful remote artifact was SHA-256 checked against GitHub's artifact digest, all 28 plaintext revision file hashes were compared with the prepared source bundle, and both PDF hashes were checked against the published receipt. Selected pages of both remote PDFs were also rendered for visual inspection.

- `paper.pdf`: SHA-256 `8cb033adb114fbcb2b84df96209e6b64413ca870c8e5e24b8860c6003403b6ac`.
- `complete-development.pdf`: SHA-256 `3c3c77aa82ce7c71ddb59ad6d007c148fb0385bcb4bf8545c3a4bb6fedad238f`.
- Remote artifact ZIP: SHA-256 `6cb1b4fbae7d6753d0d49ccb68048dd8d579f27b3bbd4d127065f8d92dc583f0`.

Finite tests and successful typesetting are not certificates for the analytic proofs. The proof ledger states the hypotheses precisely. Four proved model-scoped pipeline consumers are not a claim that all unrestricted historical microscopic targets are complete; the current primary A2 algebraic-geometric line remains independent.

## Reproduce

From a checkout containing the inherited source directories:

```sh
python -m pip install -r papers/GTF-I-v10-marked-duality/requirements.txt
# Debian/Ubuntu: install texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils.
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v10-marked-duality/build.py
```

A rebuild at this documentation commit will honestly identify that checkout as its source, rather than claim to have run at the earlier build commit. The shipped PDFs and receipt remain bound to `c2653682d73571ad01f7c159bb10784f800982b4`.
