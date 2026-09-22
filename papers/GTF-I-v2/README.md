# General Theta Foundations I — second revision

**Qian Qi · 22 September 2026**

[Read the new manuscript PDF](paper.pdf) · [Native TeX entry](main.tex) · [New mathematical development](revision.tex) · [Response to the referee](RESPONSE_TO_REFEREE.md) · [Proof ledger](PROOF_LEDGER.md)

This edition responds to the 22 September GTF I v1 report on the review branch. It retains the title, develops a new general quantitative center, and preserves the entire first edition. The manuscript is written in English in the `amsart` format, with complete statements, hypotheses, and proofs. The local build is 44 pages; the runner receipt records the actual published PDF's page count and source identity.

## Results to review first

Theorem 2.1: actual acquired concentration and exact-suffix stability, with matching causal resolution under the stated cover/mass/stability assumptions.

Theorem 2.3 and Corollary 3.3: conditional intermittent contraction and infinite-horizon expected checkpoint resolution without bounded waiting times.

Theorem 3.2: the commanded HMM law for every positive refresh rate, with explicit dimension/mixing constants. Proposition 3.4 gives a singular acquired-dimension law.

Theorem 4.1: matched finite-sample contact, unknown measured-calibration, and finite-label minimax risk.

Theorem 5.1: a finite reference policy compared with the unrestricted optimal controller. Proposition 6.1 supplies an implicit finite-description codebook and numerical error allowance.

## Complete review materials

- [Point-by-point E1--E5 and M1--M7 response](RESPONSE_TO_REFEREE.md)
- [Historical mathematical dependencies](HISTORY_AUDIT.md)
- [Source and edition manifest](SOURCE_MANIFEST.json)
- [Original report, unchanged](review-input/REFEREE_REPORT.md)
- [Preserved complete first edition](legacy/README.md) and [its original PDF](legacy/paper.pdf)
- [Complete fixed A1 v37 source edition](source-editions/A1-v37/README.md)
- [Complete fixed A2 v112 source edition](source-editions/A2-v112/README.md)
- [Executed source-bound build record](evidence/BUILD_RECEIPT.json)
- [Author-side local rendered-page inspection](RENDER_REVIEW.json)

The new PDF incorporates all original mathematical sections and their proofs as appendices. The original introduction remains in the complete original edition instead of being duplicated ahead of the new introduction. All original repository paths remain untouched.

## Build

Install Python 3, `pdflatex`, and `pdfinfo`; on Ubuntu the TeX packages are `texlive-latex-base`, `texlive-latex-recommended`, `texlive-fonts-recommended`, `lmodern`, and `poppler-utils`. From the repository root run:

```sh
python3 papers/GTF-I-v2/build.py
```

The script first verifies the revision manifest and the preserved v1 source hashes, executes the old and new diagnostics, checks that negative controls fail, and compiles until references stabilize. It rejects undefined references/citations, duplicate labels, missing retained labels, and overfull boxes. In GitHub Actions it also verifies the exact preserved Git trees on the source commit. Generated products are `paper.pdf` and `evidence/`; `COMPILED_SOURCES.zip` contains the full build input closure.

The branch-specific workflow publishes only those generated products and only if the source branch still points at the executed commit. Its receipt identifies that source commit separately from the later generated-PDF publication commit. No merge into main is part of this revision.

Build and finite diagnostic results are reproducibility evidence. The manuscript is a new candidate for independent referee assessment, not an assertion of journal acceptance or formal proof verification.
