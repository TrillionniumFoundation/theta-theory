# Author response to Referee Round Twenty-Two — A1

We thank the referee for isolating the domain error in the former response theorem.  The active Round-Twenty-Three source does not infer a geometric projection rate from membership in a Hilbert completion.

## A1.1 — response domain and meaning of the integral

The geometric current fibre `J^m`, the symbolic probability space, and a random current observable are now separate objects.  An observable is a strongly measurable Bochner-square-integrable map `Sigma -> J^m`.  Its response domain carries the explicit norm

`sup_N exp(eta N) ||J - E[J | F_{-N}^N]||_2`.

The mean is a Bochner integral with target `J^m`.  Thus the approximation rate is a hypothesis encoded in the Banach norm, not an alleged consequence of Hilbert membership.

## A1.2 — FCLT

The source defines the filtration, projections `P_n`, centered increment, projective series, martingale difference, and polygonal process.  It proves summability of `sum_j ||P_0 Y_j||_2` from the explicit cylinder norm.  Trace class is obtained from the exact identity

`tr Q = E ||D_0||^2`,

followed by finite-rank tightness and the Hilbert martingale FCLT.

## A1.3 — current calculus

All restrictions and normal derivatives act on positive Sobolev test jets.  Currents receive only transposed extension maps.  The fixed-fibre connection has a stated source and target, and the material derivative is its closed transpose.  The measurable coefficient map is then differentiated in the corresponding Bochner graph space.

## A1.4 — significance and literature

The paper now states explicitly that the suspension benchmark is standard.  Its contribution is the typed incidence fibre, the measurable response domain, and the current-valued martingale theorem.  Kato, Gordin, and Hall--Heyde are cited at the exact points where their frameworks are used, after their hypotheses are verified.

No theorem has been replaced by a no-go statement.  The advertised positive response and FCLT conclusions are retained on the correctly defined observable domain.
