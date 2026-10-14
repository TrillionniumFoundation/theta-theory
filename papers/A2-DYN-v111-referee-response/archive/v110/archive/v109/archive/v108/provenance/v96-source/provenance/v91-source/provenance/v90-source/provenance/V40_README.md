# A2-DYN, revision 40

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. Revision 40 starts from the substantive v39 review at `a76fcf9d6ef7288ea324fed327c4f2f0ce088461`, whose report blob is `34fd05b1740816104f38ca84c75826b11eec1694`. The exact v39 author baseline is `75eda04842b69319ae81c97ce1502129d55ee5fc`, paper tree `549a0879a747bf0a2506a0fb7d1fdd847d2d7577`.

## New theorem-bearing source

`core/84_occupation_cut_power_bounds.tex` proves polynomial occupation-cut bounds in all three collision norms, quasi-compactness on the full occupation torus at fixed roof band, physical peripheral representation, uniform power bounds, and exponential decay on compact joint nonresonant sets.

`core/85_occupation_holonomy_and_residues.tex` uses integer-valued stable/unstable occupation holonomies and nonatomic contact area to exclude nonzero roof resonances. The group is consequently finite cyclic. It computes every actual endpoint residue, including nonzero displacement and nontrivial scalar eigenvalue, and identifies the same Gaussian curvature at each resonance without assuming the measurable phase is a strong multiplier.

`core/86_fixed_count_arithmetic_local_law.tex` proves a radius-uniform finite spectral reduction of the fixed collision-count inverse. At each fixed radius it obtains the exact-return-index, fixed-roof-interval local law with an explicit nonnegative arithmetic factor. This is a long-power argument, not a deduction of coefficients from an Abel average. The factor averages to one over its finite period; a zero factor corresponds to an exactly null event. Theorem 5 states the new interval law in the original return covariance normalization.

The original topic and full raw four-coordinate target remain unchanged. The unmodulated radius-uniform singleton law, the pointwise raw correction and full roof-density inversion are not declared proved. The finite spectral reduction remains uniform even near changes of resonance type; its explicit arithmetic asymptotic is stated at fixed radius.

## Preservation and build

All 83 inherited core files, all 95 inherited Python files, the bibliography and the compiled A--X synopsis are byte-identical to v39. Old front matter and source records are preserved under `provenance/`. All inherited mathematical labels remain in the compiled article.

Run `bash papers/A2-DYN-v40-referee-response/build.sh`. The read-only exact-SHA workflow verifies the frozen baseline, ordinary-source Merkle identity, exact report blob, inherited source, finite arithmetic checks, and normal/optimized agreement; it builds the complete article and renders theorem-bearing pages. Its dynamic receipt identifies the actual commit, run, PDF and source hashes. It is not a continuum proof certificate or independent human audit.
