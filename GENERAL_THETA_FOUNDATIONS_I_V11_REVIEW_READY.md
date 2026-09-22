# General Theta Foundations I — v11 referee entry

**Full English resource-comparison revision, 23 September 2026.**

The controlling independent referee report is commit `8e44610a9826b799f190639cec80c0435f14487c`, on `review/general-theta-foundations-i-v10-marked-duality-independent-harsh-top4-2026-09-23`. It reviews the v10 referee-ready head `4507bd5b6e61206d0d82c9f52fcbe279585ce1c7`. This revision responds with new proofs and a unified resource-comparison structure while preserving the predecessor mathematics. It is submitted for renewed independent review, not represented as accepted or independently certified.

## Read the revision

| Entry | Purpose |
|---|---|
| [Full article — 78 pages](papers/GTF-I-v11-resource-comparison/paper.pdf) | Canonical theorem–proof manuscript; [LaTeX entry](papers/GTF-I-v11-resource-comparison/main.tex) |
| [Complete development — 175 pages](papers/GTF-I-v11-resource-comparison/complete-development.pdf) | Preserves all earlier mathematical bodies and historical introductions; [LaTeX entry](papers/GTF-I-v11-resource-comparison/development.tex) |
| [Point-by-point referee response](papers/GTF-I-v11-resource-comparison/RESPONSE_TO_REFEREE.md) | E10.1–E10.7 and technical comments 11.1–11.8 |
| [Proof ledger](papers/GTF-I-v11-resource-comparison/PROOF_LEDGER.md) | Proof locations, hypotheses and precise scope |
| [Literature comparison](papers/GTF-I-v11-resource-comparison/LITERATURE_COMPARISON.md) | Original-source comparison and explicitly unresolved priority audit |
| [History audit](papers/GTF-I-v11-resource-comparison/HISTORY_AUDIT.md) | GTF ancestry, historical microscopic B4 and independent primary A2 |
| [Typed pipeline graph](papers/GTF-I-v11-resource-comparison/PIPELINE_GRAPH.json) | All eleven historical components and the two new microscopic dependencies |
| [Preservation diff](papers/GTF-I-v11-resource-comparison/PRESERVATION_DIFF.md) | Original files unchanged; local median-wording correction identified |
| [Build receipt](papers/GTF-I-v11-resource-comparison/evidence/BUILD_RECEIPT.json) | Exact source identity, PDF hashes, theorem pages and executed diagnostics |
| [Complete source closure](papers/GTF-I-v11-resource-comparison/evidence/COMPILED_SOURCES.zip) | 265 pinned inputs needed to reproduce the development |

## Source and publication identities

- Source transport and dedicated workflow commit: `fee7d81b7da9f27f287956692e1a39da99a78536`.
- Complete plaintext mathematical source and exact successful build checkout: `0cee9e4ac7d3eb0f1c47c339b271b04b66c4f848`.
- PDF/evidence publication commit: `abefc31cd051591721422db1e9ff1c837e2f93d6`.
- Successful GitHub Actions run: `35795294760`; job `106973081411`; artifact `10723088730`.
- Working branch: `revision/general-theta-foundations-i-v11-resource-comparison-2026-09-23`.
- Frozen referee branch: `revision/general-theta-foundations-i-v11-resource-comparison-referee-ready-2026-09-23`.

This entry is a documentation-only addition above the publication commit. It changes no mathematical source, PDF or build receipt. All changes since the controlling review are additions under the new v11 directory, its dedicated workflow, and this entry; no existing file was modified or deleted. The earlier review, v10, default and A2 branch references were not updated by this delivery.

## Principal proof locations in the canonical PDF

| Result | Location |
|---|---|
| Executable resource-costed marked comparison, risk-body inclusion and composition | Theorem 3.2, p. 9 |
| Complete-state fusion: quotient comparison at unchanged retained widths | Theorem 3.7, p. 11 |
| Conditional common-encoder duality for a concrete singular report class | Theorem 5.3, p. 18 |
| Exact task-specific restart width as a compatible-cover number | Theorem 7.1, p. 22 |
| Causal task completion and minimal positive-report width profile | Theorem 7.4, p. 24 |
| Exponential positive-state width at linear rank two | Proposition 9.2, p. 26 |
| Collision-compatible graph core for microscopic hard-sphere transport | Theorem 20.2, p. 49 |
| Width-uniform noisy physical-acquisition comparison | Theorem 20.3, p. 50 |

## Verification actually performed

The successful remote build checked 238 inherited files and 26 manifest-listed new source files; the source manifest itself is the additional entry in the 265-input source closure. All 565 v10 companion labels are preserved; 563 retained historical labels resolve, and the 263 shared canonical labels have identical numbering in both views. Both manuscripts stabilized in three LaTeX passes. The build rejected unresolved references, duplicate labels and overfull boxes.

The new finite diagnostic suite executed 825 conditions with matching ordinary and optimized Python results. Eight designated incorrect variants were rejected in each mode, for 16 negative-control executions. All ten predecessor diagnostic suites were rerun successfully. The pipeline check verified the exact controlling review blob from Git and the eleven-component source/label contract; it is not a semantic proof checker.

The successful remote artifact was downloaded and its SHA-256 compared with GitHub's artifact digest. All 27 plaintext revision files were independently compared with the prepared source-bundle hashes. Both PDF hashes and page counts were checked against the remote receipt. Selected pages of both downloaded PDFs, including the new comparison, conditional duality, task and microscopic results, were rendered and visually inspected.

- `paper.pdf`: SHA-256 `2c263f75e00c4704405c05bcd1aadce6f117c8363e88b354ae347f0e65daf8da`.
- `complete-development.pdf`: SHA-256 `47baccc0df6259c64457d9a6901dc1662d66f8f22a02c776c2c863aff27ce462`.
- `COMPILED_SOURCES.zip`: SHA-256 `6bc25da32768ef206ebba5af7556ccc6adefc7268ff8437b986f110ccbca6c40`.
- Downloaded workflow artifact: SHA-256 `caa0d94ee6d268cfef809f9e8b1f0f75eb78bdd3d52109b8b125ba6bb4a00bfe`.

## Mathematical and priority boundaries

The source proves statements in their stated categories. The conditional extension does not claim compactness for every filtered experiment. Complete-state fusion is not resource neutrality for arbitrary consumers. The microscopic graph core and its acquisition corollary do not establish the stronger historical B4 action-sublevel BBGKY corrector or nonlinear kinetic limit; the response specifies the remaining analytic inputs rather than replacing them by the new Lp result. Proof-level priority against the unretrieved Norberg original remains unverified. No independent referee or journal approval is asserted.

## Reproduce

From a checkout containing the inherited source directories:

```sh
python -m pip install -r papers/GTF-I-v11-resource-comparison/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v11-resource-comparison/build.py
```

A later rebuild identifies the checkout actually used. The published PDFs and their receipt remain bound to `0cee9e4ac7d3eb0f1c47c339b271b04b66c4f848`, not to this later documentation commit.
