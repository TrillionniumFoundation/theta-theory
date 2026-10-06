# A2-DYN, revision 16

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete active article is `main.tex`. The baseline is the already landed revision 15 at `656104408b8f9d62ccab0b1d7bc847e3be950a08`; the controlling report remains the latest substantive v14 report at `43d797ce65ad5e4cf92f874a6656c9cd0af9d572`. This revision continues the same physical model and raw mixed-density problem. It does not overwrite revision 15 or describe that manuscript as externally reviewed.

## New proof

Theorem G proves parameter-uniform near-origin defect bounds for the **actual unbounded return record**, not only the collision record. Its proof is in `core/36_near_origin_defects.tex` and `core/37_actual_return_defects.tex`.

The first section combines the established elliptic covariance with a diffusive twisted middle block and short untwisted endpoint blocks. It gives a quadratic lower bound for collision phase defects while the BV budget grows. A modulus argument gives the corresponding normalized complex-function bound, without a lower-modulus assumption.

The second section constructs the exact tower lift, proves that its defect occurs only at actual tower tops, and regularizes it with explicit first-variation and approximation costs. A lifted semialgebraic graph, a finite connected-component bound and slice coarea control the variation of finite collision records without bounding inverse derivatives at grazing. The resulting actual-return bounds hold with `r=|z|`, `Lambda=1+log(H/r)`, and `K=Lambda*log(2+Lambda)` whenever `r*K` is sufficiently small: the circle defect is at least `c*r^2` and the normalized complex-function defect at least `c*r^2/K`.

For polynomial regularity budgets these estimates apply throughout `2 n^(-99/200) <= |z| <= n^(-2/5)`, uniformly in the radius. They are defect estimates, not a claim of a completed complementary Fourier integral.

## Preserved source and build

All 35 inherited core files and all inherited Python files are byte-identical to v15. All old theorem and equation labels and all bibliography items remain. `INHERITED_EDITS.json` records the introduction and bibliography additions exactly. The two new core modules are ordinary committed source; qualification does not generate manuscript text.

Run `bash papers/A2-DYN-v16-referee-response/build.sh`. The read-only exact-SHA workflow verifies source hashes and inheritance, executes normal and optimized finite diagnostics, runs the six inherited diagnostic programs, compiles the complete article, and emits a SHA/run/PDF-bound receipt. The workflow does not certify continuum mathematics or journal acceptance. See `RESPONSE_TO_REFEREE.md` and `PROOF_LEDGER.md` for the mathematical scope.
