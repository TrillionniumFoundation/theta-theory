# General Theta Foundations I — sixteenth revision

**Constructive Causal Deficiency and Physical Testing**  
Qian Qi, 23 September 2026.

`main.tex` is the full canonical English article; `development.tex` adds the entire preserved predecessor development. `paper.pdf` and `complete-development.pdf` are produced by `build.py`. The root `GENERAL_THETA_FOUNDATIONS_I_V16_REVIEW_READY.md` records the eventual frozen source, publication and referee-ready identities.

The main new source files are `nonlinear-testing.tex`, `collective-hard-spheres.tex`, and `physical-testing.tex`. They prove an endogenous polynomial testing dual at the original private/selector budget, a nonconserved collision-compatible hard-sphere realization with exact marked deficiency and nonzero Gram residual, and a joint physical-certificate theorem with sharp bounded exponential transfer.

Read `RESPONSE_TO_REFEREE.md` for E15.1–E15.8, including the distinction between the actual complete v15 mathematical base and the different unmaterialized branch reviewed by the deposited report. The latest-named v15-r2 review had no new report at the recorded checks. No unavailable report is presented as read.

`PROOF_LEDGER.md`, `LITERATURE_COMPARISON.md`, `HISTORY_AUDIT.md`, `PIPELINE_GRAPH.json`, and `PRESERVATION_DIFF.md` separate proof locations, original-source comparison, historical targets, scoped dependencies and content preservation. Original Norberg/Paull–Unger proof-level priority and the full historical B4 nonlinear kinetic closure are not claimed complete.

## Reproduce

From a checkout with all pinned inherited directories:

```sh
python -m pip install -r papers/GTF-I-v16-constructive-causal-certification/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v16-constructive-causal-certification/build.py
```

The new exact finite checker is `verify.py`; `certified_examples.py` contains all rational polynomial and interval arithmetic. The remote build emits the full coefficient array and physical interval data. This is not a generic collision-chart implementation, a formal proof verifier, or independent referee approval. The inherited diagnostic suites and source hashes are reproducibility evidence, not certificates for analytic proofs.
