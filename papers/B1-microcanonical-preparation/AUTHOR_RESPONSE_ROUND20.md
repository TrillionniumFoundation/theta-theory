# B1 Author Response — Round Twenty

The active B1 source fixes the Boltzmann--Grad scaling and places the conserved
and cell constraints on the quotient by all affine relations.  Strict
convexity and properness are proved on that quotient, giving a global
source-dependent saddle on compact interior target sets rather than a local
inverse-function assertion.

The former high-frequency proof has been replaced by a fixed-size smoothing
block construction.  Each selected block contains enough separated position
and velocity variables for the complete constraint map to have full rank.
Position coordinates enter the coarea minor whenever the Fourier direction is
position dominated, so velocity integration is not asked to detect a
position-only phase.  The conditional density of one fixed block has a fixed
`W^{s,1}` bound from the normalized B2 connected expansion.  Many blocks are
integrated successively, but no amplitude is differentiated to order growing
with `N`; this removes the `C^4` versus `O(N)` contradiction.

The local coefficient theorem now separates lattice and continuous
coordinates, distinguishes absolute and relative shell errors, and excludes
exact point events in continuous variables.  Finally, exact-number and
microcanonical pressures are derived by a joint activity/constraint contour
through the reoptimized saddle, with bounded path/contact insertions and source
derivatives.  The Schur-complement covariance follows by differentiating the
saddle equations.

The positive exact-number theorem is retained at its advertised strength.  No
signed-polymer probability, no no-go substitute, and no silent restriction to
velocity-only constraints remains.
