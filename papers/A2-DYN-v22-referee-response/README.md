# A2-DYN revision 22

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision responds to the latest v20 external report at `a77d1b0af695877bcd43ddb494c637d8353d9b10`, from the reviewed author source `b5b209000bbef852076f413ef4f718137aeb4dd3`. At branch discovery, the pre-existing v21 response branch still pointed to the review commit and contained no distinct v21 manuscript. The new v22 branch avoids overwriting that reserved branch.

## New fixed-count result

Theorem L and the two new core modules prove a fixed-return inner-annulus bound at the raw four-dimensional scale. For a single controlled BV insertion at any actual return, the full physical transform satisfies

`n^2 integral_{2 n^(-99/200) <= |z| <= 2 n^(-12/25)} |Phi_n(z)| dz <= C[M_a n^(-1/200) sqrt(log(2+n)) + V_a n^(-13/100)]`.

There is no average over return counts and no normalization by annular volume. A degree-19 spectral Taylor polynomial, whose finite coefficients are bounded through summable collision cumulants, provides the damping needed for this bound. The analytic radius remains smoothing-dependent. The proof removes smoothing and uses the genuine two-sided stopping comparison; it never infers a fixed-time estimate from v20's Gram averages.

The complete integrated comparison extends to rescaled radius `2 n^(1/50)` (physical radius `2 n^(-12/25)`). The old, sharper comparison at radius `2 n^(1/200)` is retained unchanged. The new cutoff is inserted into the exact count-localized raw inversion identity, with the new local edge correction explicitly retained. A general finite-order construction permits every rescaled exponent strictly between `1/200` and `1/42` with a corresponding finite degree and positive error margins.

## Source and validation

All 45 inherited core modules and every inherited Python script remain byte-identical. The introduction and bibliography have eight exact changes listed in `INHERITED_EDITS.json`; all old labels and bibliography entries remain. New proofs are in `core/46_finite_order_damping.tex` and `core/47_fixed_return_annulus.tex`.

Run `bash papers/A2-DYN-v22-referee-response/build.sh`. The source verifier checks the full frozen v20 paper tree, exact edits, file hashes and references. The build runs normal and optimized finite diagnostics and all inherited checks, compiles natively, and emits a dynamic SHA/run/PDF receipt. The workflow is read-only and checks the exact event SHA.

The full complementary region beyond the enlarged band, the long-time raw second-derivative budget, the local extracted-edge estimates, and exact physical-event replacement are not claimed complete. The original raw mixed-density topic and all its requirements are retained. Execution evidence is not an independent mathematical proof certificate.
