# A2-DYN, revision 54

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The controlling substantive report is the v52 report at `b487df93e48dbf455b3ed04680c1f7ae3613f45e`. Revision 54 continues the already qualified v53 manuscript at `9d3891615c3e09d8e40b7ba8e24d410ee6e9c76d`, rather than overwriting it or republishing the old v48 packet.

## New scalar results

Modules 115 and 116 establish a finite-count protected height bound with loss epsilon^(-9), a density-superlevel mass bound with power 1/144 and an exponential finite-count error, and a nonempty range of uniform local L^(1+s) bounds for the complete original density. The exact exponent range is specified in the article in terms of one fixed-band spectral decay constant and the already proved exponential finite-count height cap; no numerical universal lower bound for that range is asserted.

The complete arithmetic raw local law and its path-valued version now converge in local roof L^q for 1<q<q_*. Both positive physical remainders are small in these stronger norms. On fixed roof windows with a pointwise positive arithmetic reference floor, the original forward likelihood converges in L^q of the reference law, and forward relative entropy and the corresponding finite-order Renyi divergences tend to zero. Reverse entropy was already controlled by the inherited minorization.

Finite L^q and forward entropy do not give essential-supremum height. The two positive incidence/clearance height conditions, the full two-sided pointwise raw theorem, forward essential likelihood, and the unconditional uniform same-roof bridge remain distinct obligations. The arithmetic transition kernel and exact original indices are unchanged.

## Reproducibility and preservation

Run `bash papers/A2-DYN-v54-referee-response/build.sh`. The strict verifier rechecks the qualified v53 baseline, all frozen reports, all 114 inherited core files and 147 inherited Python files byte-for-byte, bibliography and appendices, retained labels, source Merkle identity and workflow hash. The normal and optimized finite checks must agree. The native TeX build and theorem-based renders are included in the read-only exact-SHA workflow.

The source tree, author response, proof ledger, historical audit, specialist map and dynamic build receipts separate source/build evidence from mathematical proof verification. No independent human specialist review is claimed.
