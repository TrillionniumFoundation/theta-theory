# A2-DYN, revision 47

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision starts from the v46 external-review commit `ae02860fe7182078ed738d1b23213b3ce8f8afe3`, whose reviewed author source is `fb16f06fb2bd205322d4a15979aef5a9a83d4970`. It adds a pointwise estimate for a genuine part of the collapsing-margin source, not another estimate of its total mass.

## New mathematical result

`core/100_endpoint_decision_deconcentration.tex` proves that a source with collapsing section decisions in the first and last `J+1` collision states, but protected incidence, clearance and middle decisions, has exact-index roof density bounded by `C M (J+1) epsilon m^(-2)` in collision limsup. The bound holds for every bounded measurable source insertion. Its entire signed correction is bounded uniformly over all roof bandwidths.

The proof uses a small-endpoint version of the full arithmetic collision local upper bound, a physical roof flow which crosses only finitely many section cuts, and low-gradient completion to physical critical collars with the same free decisions. A finite occupation enlargement occurs only on the upper side of a positive comparison. The original exact `(n,k,m)` density is never replaced by a packet average. The continued source is `nu/c`, not a newly normalized section probability.

`core/101_first_bad_margin_resolution.tex` gives an exact positive source split and a disjoint first-defect partition of what remains. At `epsilon(B)=A B^(-1/12)`, `J(B)=floor(B^(1/24))`, the protected and endpoint-decision corrections together are `O(B^(-1/24))` after the collision limit. Incidence, clearance and interior-decision corrections remain explicit. Their smaller mass bounds are not described as pointwise bounds.

## Retention and qualification

All 99 inherited core modules, all 123 inherited Python scripts, the bibliography and the compiled A--X synopsis remain byte-identical. Prior front matter, source manifest, response and proof ledger are archived under `provenance/v46-*`. The active article compiles all 101 core modules and retains every inherited mathematical label.

Run `bash papers/A2-DYN-v47-referee-response/build.sh` from the repository checkout. The read-only workflow `.github/workflows/a2-dyn-v47-qualification.yml` checks the exact event source, controlling report, ordinary-source Merkle identity, finite diagnostics, native typesetting and theorem-page rendering. Only an actual successful run and its dynamic receipt qualify that SHA. A local-only missing-review recovery option is explicitly reported and is forbidden in CI.

The original raw arithmetic density target and title are unchanged. This revision does not assert the full residual correction, grazing or clearance boundary smallness, an effective count-dependent protection rate, a pointwise roof-conditioned bridge, or independent human verification.
