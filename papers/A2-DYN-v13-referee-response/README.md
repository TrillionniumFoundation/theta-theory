# A2-DYN, revision 13

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The active article is `main.tex`. This revision continues the original raw mixed-density problem and retains every inherited theorem and all 29 inherited core modules. It adds `core/30_unsmoothed_moments.tex`, with a complete collision-gap argument for unsmoothed fourth moments, quantitative actual-return covariance convergence, and first and second moments with an insertion at any one actual return. `core/31_count_nondegeneracy.tex` uses an integer-valued cohomology argument to prove that the collision-count component has uniformly positive Gaussian variance. Theorem D summarizes the addition.

The parent is revision 12 at `13b088e47bfbe8d46313b00bb97bc92a235a2376`. The controlling referee report is the substantive v11 report at `fd84da57359a3ad2fefed532b0b5094ab8c6e436`, not the earlier source-identity notice. Revision 12 already repaired the reviewed packet and passed its exact-source build; this revision advances the mathematics beyond that repair.

## Main addition

Finite-product collision decoupling, proved by gap-dependent smoothing and chronological spectral splitting, yields an unsmoothed fourth-moment and maximal fourth-moment bound of order `m^2`. Fourth-moment visit windows and cumulative-return tails give an `L2` two-sided stopping error `O(n^(-1/6))`. Consequently the covariance of the actual, unmodified return record divided by `n` converges uniformly to `D_R` at that rate. A centered collision-state insertion has a summable three-point correlation; this supplies marked quadratic moments with separate supremum and variation budgets. The induced Green--Kubo formula is thereby established with Cesaro lag weights, without assuming absolute summability of induced correlations.

The new characteristic stopping error is `O(M_a(1+|v|)n^(-2/9))`. It improves only the stopping term; the central band remains `|v| <= 2n^(1/200)`, physically `|omega| <= 2n^(-99/200)`.

## Source and verification

Run `bash papers/A2-DYN-v13-referee-response/build.sh` from a checkout. The build verifies the exact source manifest, all inherited core identities apart from one explicitly listed punctuation repair, retained labels, normal/optimized finite checks, the inherited diagnostics, and native TeX. `.github/workflows/a2-dyn-v13-qualification.yml` archives the event source and emits a dynamic receipt carrying the event SHA, run ID, and PDF hash. Build success is not mathematical proof certification.

`RESPONSE_TO_REFEREE.md` answers the report item by item; `PROOF_LEDGER.md` states the exact dependencies and remaining raw-density obligations. No full raw LLT, positive definiteness of the entire covariance matrix, or independent human review is claimed by the supporting metadata.
