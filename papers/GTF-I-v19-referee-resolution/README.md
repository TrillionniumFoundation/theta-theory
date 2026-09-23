# General Theta Foundations I — v19

**Continuation Complexity and Stable Causal Certification**  
Qian Qi · Full English theorem–proof manuscript · 23 September 2026

`paper.pdf` is the canonical article, compiled from `main.tex` and its local inputs. `complete-development.pdf` appends the unchanged 294-page v18 development. No predecessor manuscript or pipeline source is overwritten. Historical assertions in the companion retain their historical status; they are not new endorsements.

The main theorem combines an exact streaming-test width classification, a 400-training-reset physical certificate with a nineteen-bit auditor, and global transport of the bounded entropic backward representation along changing collision trajectories. Candidate and auditor registers are separate. Including validation, the concrete audit uses 402 trials. Its score bound is an expectation, not confidence from one realized pair. The state bound is an implementation upper bound, not a minimality or program-description bound.

## Reading entry points

- `paper.pdf` / `main.tex`: complete canonical proofs and dependency diagram.
- `RESPONSE_TO_REFEREE.md`: all E17-R3.1–12 and E17-P1–8, distinguishing inherited v18 answers from new v19 results.
- `PROOF_LEDGER.md` and `PROOF_STATUS.json`: novelty subtraction, exact statement identities and review status.
- `HISTORY_AUDIT.md` and `PIPELINE_STATUS.json`: all eleven components preserved with scoped proof credit and supersession.
- `LITERATURE_AUDIT.md`: original-source access and the still-unverified Norberg comparison.
- `evidence/BUILD_RECEIPT.json`: actual source-bound build and diagnostics, not analytic certification.
- `evidence/SUBMISSION_SOURCES.zip`: portable canonical TeX source tree, with no font files.

## Reproduction

For the portable canonical source archive, run `pdflatex main.tex` three times. For the full release from the repository:

```sh
python -m pip install -r papers/GTF-I-v19-referee-resolution/requirements.txt
python papers/GTF-I-v19-referee-resolution/build.py
```

The system needs pdfLaTeX with AMS packages, lmodern, TikZ and the packages in `preamble.tex`. The complete build requires the pinned v18 `complete-development.pdf` in its original repository location. `verify.py` contains explicit error checks that remain active under `python -O`.

The scoped theorem assumptions are fixed positive Gaussian noise, a common preparation, bounded signals, and a bounded scalar entropic terminal transform. The physical realization has two particles and one nongrazing collision. These results do not by themselves certify all eleven papers, a particle-number-uniform kinetic limit, or the independent A2 geometric chain. New analytic proofs await independent review, and the original Norberg proof-level crosswalk remains unverified.
