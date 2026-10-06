# A2-DYN revision 26

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Active source: `main.tex`. This revision responds to the v25 report at `b9d11ff3bc2c08bb7410d93d3128d847e277cc08`, from the qualified v25 author source `4c07267338175932688a20a6021dae1b602074a0` (paper tree `5c5378441102a155ccbf76f4b7f18d426390d3a9`). The original title, table, actual section, four-coordinate record and raw mixed-density endpoint are unchanged.

## New results

Theorem P proves one nonrectangular prescribed-count Fourier region, not just a roof-direction box. A shape-independent fixed-order estimate uses ordinary volume and first radial moment; a dyadic product-times-maximum budget covers new discrete-coordinate and mixed directions. The logarithmic compensation is inside the region definition. The original `n^(-3/280) sqrt(log(2+n))` central error and the old isotropic/roof union are retained. Each of the four axes reaches physical frequency of order `n^(-41/100)`.

Theorem Q proves a quantitative transport bound for the complete signed raw correction when the active kernel is changed among the new dyadic, old roof-box and old isotropic cutoffs. The exact edge/residual cancellation makes this a bound for the original finite-count law, not a bound involving uncontrolled separate changes in extracted jets. For a bounded fixed weight class the normalized transition is `O(n^(-3/280))`. This does not establish smallness of the common correction itself.

## Preservation and qualification

All 54 inherited core files, all inherited Python scripts and the bibliography are byte-identical to v25. Five exact replacements affect `main.tex` only. The new core files are `55_shape_adaptive_fixed_count.tex` and `56_coherent_raw_cutoff_transport.tex`; all inherited theorem labels and Theorems A--O remain included.

Run `bash papers/A2-DYN-v26-referee-response/build.sh` from a full checkout. The verifier checks source identities, exact edit replay, labels, bibliography, finite algebra and kernel/cancellation diagnostics normally and with `-O`; native TeX and the exact-event workflow produce dynamic receipts. Execution evidence is not a continuum proof certificate.

The full isotropic one-tenth region, full complementary integral, genuine long-time derivative sum, absolute local-edge estimate, weighted denominator asymptotics and exact physical-event replacement remain specific mathematical obligations. `RESPONSE_TO_REFEREE.md` gives the itemized response and the precise scope of the new theorems.
