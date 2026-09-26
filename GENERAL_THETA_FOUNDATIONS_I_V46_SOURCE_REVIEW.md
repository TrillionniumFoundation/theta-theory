# General Theta Foundations I — Revision 46: source review

**Certified Positive Realization of Numerical Word Experiments**  
27 September 2026

This entry publishes the complete readable LaTeX manuscript and author response. It is a **source-review** release, not a successful GitHub Actions publication receipt.

- [Complete article entry point](papers/GTF-I-v46-certified-hankel/main.tex)
- [New finite-horizon certificate proofs](papers/GTF-I-v46-certified-hankel/finite-horizon-certificates.tex)
- [Response to the controlling r29 report](papers/GTF-I-v46-certified-hankel/RESPONSE_TO_REFEREE.md)
- [Publication status](papers/GTF-I-v46-certified-hankel/PUBLICATION_STATUS.md)
- [Resource conventions](papers/GTF-I-v46-certified-hankel/RESOURCE_LEDGER.md)
- [Preservation audit](papers/GTF-I-v46-certified-hankel/HISTORY_AUDIT.md)

Controlling review: `6e8a9504a1a0820e6195317df885d99aed06c878`, reviewing v43. Mathematical predecessor: published v44 `d7042cf71485f661e27d87d12ffae35a2edfc15c`. The separate staged v45 branch remains unchanged and is not represented as mathematically reviewed. The new work descends from frozen base `36f5865f4f3f2e3a28993ffd7e3fb622ca930672`.

The new section gives an exact all-word Gram certificate, a finite-moment characterization of actual optimized terminal error, rational-grid two-sided bounds, and an explicitly solved finite planar frontier. Classical equivalence, real-algebraic elimination and nonnegative-rank ingredients are credited. All inherited v44 mathematical modules remain in this manuscript.

A local build produced a 26-page article and optional preserved archives. The last observed remote workflow `36260243370` was queued and had no executed steps. A later direct write of the new `certify.py` program was blocked by the tool safety check; it was not retried through a different encoding or transport. Consequently this source release does not claim complete native verifier publication, remote compilation, or a successful remote artifact build. Local PDFs, source archives and executed local receipts are delivered with the conversation separately.

Compile the readable manuscript from its directory with a standard AMS-compatible LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Source review does not certify independent mathematical correctness, priority or journal acceptance. No pre-existing manuscript, review, work branch or repository main branch is overwritten.
