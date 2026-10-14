# A2-DYN revision 89

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Canonical identity: `a2-dyn-v89-critical-distribution-2026-10-12`. Read `main.tex`, `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, and `SOURCE_MANIFEST.json`. The complete preceding weak-Lp article is retained in `supplement.tex`; all 207 earlier core files and their source histories are preserved.

The weak-Lp and main v88 variants are distinct. This new revision descends from the weak-Lp report and records the parallel report as an additional parent. `papers/A2-DYN-v88-main-preserved` holds the complete other source at its exact original tree; no existing revision branch is overwritten.

Modules 208–210 prove a finite-count critical surface distribution bound, original-density critical weak bounds, convergence with every positive logarithmic loss, a logarithmic estimate directly on the original exceptional union, and full diffusive-window limits with measure dt/sqrt(m). The original pointwise objective remains unchanged and its essential-height charge is not asserted zero.

Build with `bash build.sh` in the exact checkout, or `bash build.sh --local` for local archive validation outside CI. Both compile the entire active article and supplement. The workflow is `.github/workflows/a2-dyn-v89-qualification.yml`; prior runs are not new-source qualification. Source hashes and finite fixtures are not continuum proof certificates.
