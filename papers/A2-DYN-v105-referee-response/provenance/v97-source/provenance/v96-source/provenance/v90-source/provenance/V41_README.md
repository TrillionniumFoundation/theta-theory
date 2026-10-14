# A2-DYN revision 41

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision continues the latest v39 referee response from the already landed v40 author commit `d07c73f9db6a27c216fcfb2f32f844d63858c90b`. It is not an empty branch or a return to the older v35/v36 state.

## New results

Theorem 6 and modules 87--89 evaluate the exact-index interval inverse uniformly through changes of arithmetic type; prove a continuous conditional bridge for the actual return path tied to its actual endpoint; and give a radius-uniform local law on a fixed finite packet of return indices. The bridge conditions on exactly `{K_n=k,N_n=m,T_n-t in J}`. Its uniform statement requires the explicit natural-scale lower mass bound; at each fixed radius every positive arithmetic class satisfies it by the inherited local law.

The finite Gaussian transition kernel retains damping, drift, phase, curvature and endpoint amplitude of every nearby spectral branch. Strictly subunit eigenvalues are not discarded in an inverse-time parameter transition. A zero-residue criterion characterizes the uniform unmodulated single-index interval law. A common slowly shrinking roof interval is obtained without claiming pointwise density control or a prescribed shrinking rate.

## Preservation and proof scope

All 86 inherited core modules and 99 inherited Python scripts are byte-identical. The original title, family, section, return record, bibliography, A--X synopsis and raw-density target are retained. The new theorems do not prove that all section residues vanish, the common pointwise coarea correction, or the full roof-frequency tail. Independent human audit and formal proof certification are not claimed.

## Build and review

Run `bash papers/A2-DYN-v41-referee-response/build.sh` from a checkout, then `python3 papers/A2-DYN-v41-referee-response/tools/render_v41.py`. The read-only workflow records the exact event SHA and generated PDF in a dynamic receipt. `RESPONSE_TO_REFEREE.md` maps the latest report to the new proofs; `PROOF_LEDGER.md` and `SPECIALIST_AUDIT_MAP.md` record dependencies and precise verification boundaries.
