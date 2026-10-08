# A2-DYN, revision 49

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The active complete article is `main.tex`. The controlling report is the v48 external report at `3c8a41dd89f8491ac85c1ba40d85c68dc040e6dc`, reviewing author source `418000c216e9efa7c259a9bee9dac4fcf288ee1d`.

## New result

The complete original exact-index mixed density converges in uniformly translated, fixed-length roof-window total variation to the arithmetic transition kernel. The proof includes every incidence and clearance source. It first represents clearance by a thin preceding-flight envelope at the next collision, obtains a width- and mark-uniform local upper bound, and sums physical defects before the collision limit. It then proves a local L1 bound on the full signed reconstruction correction with ordered modulus B^(-1/192). The theorem gives arbitrary measurable roof selectors, central mixed-measure total variation and exact-window conditional roof total variation.

This is an additional density-norm theorem for the original record. The essential-supremum physical correction, the full pointwise raw LLT and the single-roof conditioned path bridge retain their original meanings and are not declared proved. No arithmetic residue is suppressed.

## Reading and reproduction

The new proof is in `core/105_physical_thin_layers.tex`, `core/106_physical_residual_local_variation.tex` and `core/107_raw_local_total_variation.tex`. The introduction states one new leading theorem and a short dependency route. The 11 preceding leading statements and their proofs remain compiled in `appendices/v48_leading_statements.tex`; all 104 prior core modules and all 131 prior Python scripts are byte-identical. The complete former introduction is archived under provenance; the A-X synopsis and bibliography remain unchanged.

Run `bash papers/A2-DYN-v49-referee-response/build.sh`. The read-only workflow checks exact source identity, the actual controlling report, finite diagnostics in normal and optimized Python, native typesetting and theorem-page rendering. The dynamic receipt, not this README, records the actual event SHA and outcome. These checks do not certify continuum proofs or constitute an independent human review.
