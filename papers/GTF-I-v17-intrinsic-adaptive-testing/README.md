# General Theta Foundations I — seventeenth revision

**Adaptive Testing and Collision-Sensitive Comparison** · Qian Qi · 23 September 2026

The controlling v16 second report is `b59d8527c8edc0361be3085604bcf3a920dbfbda`; the earlier v16 pipeline report is `f52d4afe6a688a2c440d4f9f351e3664e1f08a2a`. Both are answered in [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md). This is an additive mathematical revision, not a claim of independent certification or journal approval.

## Manuscripts

[paper.pdf](paper.pdf) is the canonical English article. Its entry is [main.tex](main.tex); every canonical TeX input is in this directory. No Git history or other revision directory is needed to compile the submission source ZIP. The dependency appendix is part of the article.

[complete-development.pdf](complete-development.pdf) is the preservation archive, not an additional document a journal referee must read to understand the canonical article. It retains the earlier bodies and all 812 predecessor development labels. Its entry is [development.tex](development.tex) and its inherited inputs are fixed by [INHERITED_INPUTS.json](INHERITED_INPUTS.json).

[evidence/SUBMISSION_SOURCES.zip](evidence/SUBMISSION_SOURCES.zip) contains the clean standalone canonical source tree. [evidence/COMPILED_SOURCES.zip](evidence/COMPILED_SOURCES.zip) contains the complete reproducible source closure, including historical bodies. Neither archive includes font files.

## Mathematical additions

The independent adaptive testing game retains the original nonconvex behavior image. Its degree hierarchy has error at most `4 R a / sqrt(n)`, an occupied-test bound `(n+1)^a`, and a dual support bound `(n+2)^a` in observable affine dimension. These are test-size bounds, not verification-time or chart-bit-complexity bounds. A three-weight cubic witness has a 17-coefficient exact strict certificate above `2/5`, invisible to constant tests.

A full-dimensional two-sphere preparation gives a collision-sensitive marked feedback acquisition. Its ideal private/visible value is `sqrt(5/2)-9/8`, whereas a hidden two-selector value is `1/8`. Explicit physical errors are below `1/300` on the stated diameter/noise range. The same preparation and detector give zero deficiency when no collision occurs. Feedback controls a later sensor gate, not mechanical forces; geometric similarity is not a kinetic scaling limit.

A whole-posterior-process stability theorem gives squared uniform coupling error at most `84` times joint marked variation. Gaussian observation of graph-core approximants supplies a real microscopic sufficient condition for changing-filtration convergence. The convergence coupling is not claimed to be causal or free finite-state memory.

## Audit and reproducibility

[PROOF_LEDGER.md](PROOF_LEDGER.md) records hypotheses and proof locations. [PRESERVATION_DIFF.md](PRESERVATION_DIFF.md) identifies all local copy edits. [HISTORY_AUDIT.md](HISTORY_AUDIT.md) and [PIPELINE_GRAPH.json](PIPELINE_GRAPH.json) separate theorem dependencies from adapters and independent historical targets. [LITERATURE_COMPARISON.md](LITERATURE_COMPARISON.md) records primary-source subtraction and the unresolved Norberg original-text priority audit.

Run `python -m pip install -r requirements.txt`, then `python build.py` from this directory in a checkout containing the inherited inputs. The local canonical-only command is `pdflatex main.tex` (repeat to stabilize references). TeX dependencies are `texlive-latex-extra texlive-fonts-recommended lmodern`; PDF metadata requires `poppler-utils`.

The actual build receipt, certificate arrays, negative controls and predecessor diagnostic logs are in `evidence/`. They identify the checkout actually built. Compilation and finite diagnostics are reproducibility checks, not proofs of the analytic statements. The full historical B4 and C2 programs and the primary A2 geometry are not relabeled as consequences of this revision.
