# A2-DYN, revision 15

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The revision responds to the v14 report at `43d797ce65ad5e4cf92f874a6656c9cd0af9d572` (report blob `197a42fbe2c815860423fa405f10e96cbe82e3d4`) and preserves the original model, actual return section, four-coordinate record and raw mixed-density endpoint. Its author-source baseline is v14 at `cac1a5f9ece9a8a63e69fcfb2156768337790034`.

## New mathematics

`core/34_complete_phase_arithmetic.tex` proves complete measurable physical phase rigidity, including arbitrary irrational spatial frequencies. A phase is constant on a positive-measure product set, has countable range on its ergodic saturation, and yields an excluded invariant on a finite physical cover unless every lattice phase is trivial. Positive-measure returns to an auxiliary product set then provide a finite generating family in the displacement/count lattice.

`core/35_quantitative_phase_defects.tex` converts the conditional-pair proof into finite-time defect bounds. Density truncation is explicit: measure-class equivalence is not silently replaced by bounded density. On a fixed compact nonzero physical collision-frequency set and at a fixed radius, circle phases of BV norm at most H have L1 defect at least c/(1+log H). Normalized complex functions with supremum plus BV norm at most H have L2 defect at least c/(1+log H)^2. Modulus control and a finite-perimeter radial truncation reconstruct the phase without assuming a pointwise lower modulus. For fixed H and a fixed compact band, a separate compactness proof gives separation uniformly in the radius. Theorem F is the introductory synopsis.

## Scope of the estimate

These are actual collision-function estimates. The logarithmic constants have not been made uniform in radius or in bands approaching zero or extending to unbounded roof frequency. The radius-uniform conclusion fixes H. No conversion from anisotropic distribution vectors to the stated function class has been proved. Thus neither a complete induced complementary integral nor the global critical/singular residual sum is declared closed. The weighted exact-event requirements remain on the same physical record.

## Source and build

All 33 inherited core modules remain, and two are added. Exact changes in five inherited core files, the introduction and one appended bibliography item are replayed by `INHERITED_EDITS.json`. All inherited Python diagnostics remain byte-identical. The build checks the source manifest, retained labels and citations, normal/optimized finite diagnostics and native typesetting. Run:

```sh
bash papers/A2-DYN-v15-referee-response/build.sh
```

The read-only qualification workflow checks the exact event SHA, archives its source and emits the actual run ID, attempt, PDF hash and source hashes. Its receipt is execution evidence, not a mathematical certificate or journal acceptance. The response and proof ledger identify both the new results and the remaining requirements for further substantive review.
