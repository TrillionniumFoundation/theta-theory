# A2-DYN revision 52

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Active manuscript: `main.tex`. The complete v51 manuscript is retained. This revision adds two proved modules on the original exact n,k,m source: a path-valued raw numerator and conditional bridge kernels at their own roof values. It does not change the topic or replace the pointwise density endpoint by an averaged index.

## New proof route

`110_path_valued_raw_inversion.tex` proves an endpoint Lipschitz bound for the entire pinned collision path, upgrades fixed-band cylindrical factorization to the full unit bounded-Lipschitz path class, and establishes an essential-norm positive-remainder representation for path-density measures. Local physical variation gives convergence in the integral, over each translated fixed roof window, of the path dual norm. A measurable path test can be chosen after the roof value, provided its path Lipschitz and supremum norms are bounded by one.

`111_same_roof_conditional_bridges.tex` proves the corresponding actual-return path-valued local law by an exact pinned time change, then a same-roof conditional bridge in mean under the unchanged conditional roof law. It also proves that the existing scalar positive-height condition suffices for the uniform pointwise bridge on positive-reference central targets: no additional uncontrolled bounded-Lipschitz path numerator is left.

The complete two-sided scalar pointwise density theorem remains a target, with its actual arithmetic transition kernel. Incidence/clearance essential-height smallness has not been proved by this revision. Path total variation, arbitrary measurable-selector Gaussian amplitudes, a polynomial collision-count rate, and independent human verification are not claimed.

## Source and verification

The baseline is v51 at `39ee9d88831a574a519785407732b3872ccbca3b`; the frozen controlling review is `f3c14d327837289fd44d3824d0447c010565aba2`. All 109 old core modules, all 139 old Python scripts, the bibliography and all old compiled appendices are byte-identical. The previous front matter and source records are copied under provenance.

Run `bash papers/A2-DYN-v52-referee-response/build.sh` in the repository. The read-only two-branch workflow verifies the exact source and report blobs, normal/optimized diagnostics, native typesetting and label-selected page rendering. Successful execution is recorded only in the actual dynamic receipt. Source qualification is not a continuum proof certificate.
