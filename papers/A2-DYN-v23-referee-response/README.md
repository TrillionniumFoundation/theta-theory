# A2-DYN, revision 23

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision responds to the latest substantive v22 report at `d21f74a59eed269c4b215c53b85434a3a449c779`, reviewing `a656998fee8176316850ef87ac447970d712aae2`. The physical family, actual return section, four-coordinate record, title and raw mixed-density endpoint are unchanged.

## Mathematical addition

Theorem M and the new full proof sections `48_damped_unsmoothing.tex` and `49_wider_fixed_count_band.tex` replace the first-order observable-unsmoothing loss by a damped cubic correction with a fourth-order residual. A coarse scale controls the twisted collision operator, while a separate fine scale regularizes only finitely many insertions. The lower-degree terms retain damping over the entire deterministic collision interval. Small-mass connected correlations bound the undamped fourth moment.

A fixed twentieth collision moment gives actual marked stopping rate `n^(-10/41)`. Combining these mechanisms gives, at every specified return count, the raw `n^2` annular integral through physical radius `2n^(-19/42)`, equivalently rescaled radius `2n^(1/21)`. The separated bound is `C[M_a n^(-5/861)+V_a n^(-59/21)]`. The full marked central comparison on the wider ball has variation loss `V_a n^(-9/175)`. The sufficient general exponent range improves from `epsilon<1/42` to `epsilon<1/20` using fixed orders, not orders growing with `n`.

The exact weighted raw identity recomputes the local edge correction at the new kernel. It requires the explicit intersection of the marked BV class with finite-record subanalytic admissibility. The complete outer complement, long-time residual derivative budget, local edge smallness and exact physical-event comparison are still separate requirements of the original theorem.

## Source and execution

All 47 inherited core files, all inherited Python files and the bibliography are byte-identical. Five exact edits occur only in the introduction, and every old label and theorem remains. The complete revised article is ordinary committed source, not generated during qualification.

Run `bash papers/A2-DYN-v23-referee-response/build.sh` from a checkout. The verifier checks the frozen baseline tree, complete file hashes, the exact edit ledger, old labels and all core inclusions; it runs new and inherited finite checks normally and with `-O`. The native build and read-only exact-SHA workflow record the actual PDF hash, commit, run and attempt in `evidence/build-receipt.json`. Neither finite tests nor a successful build certify continuum mathematics or journal acceptance.
