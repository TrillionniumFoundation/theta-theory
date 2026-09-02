# Author response to Referee Round Twenty-Two — B2

B2 has been rebuilt as the hard-sphere root paper.  The revision does not use moment bounds as a substitute for trace regularity and does not concatenate a reduced one-particle state.

## B2.1 — grazing trace

The regular tilted class assumes an `L^p(A_f)` density of the contact current.  Direct spherical integration gives `A_f(grazing_eta)=O(eta^2)`, and Hölder then gives a quantitative vanishing bound for the tilted trace.  General finite-entropy controls are approximated by bounded-density, nongrazing controls.  No `C eta^2` estimate is inferred from moments alone.

## B2.2 — singular geometry

The proof no longer claims that analytic stratification classifies every rank-deficient point as grazing, simultaneous, collinear, or multiple contact.  It forms the determinant ideal of the loop-closure map and uses a Łojasiewicz sublevel estimate on each compact chronology chart.  Named boundary mechanisms are handled separately.

## B2.3 — surplus-contact gain

After a spanning-tree coarea reduction, every surplus edge requires an already determined pair of trajectories to satisfy an additional loop-closure tube constraint.  On a regular minor this yields a factor `epsilon eta^{-m}` beyond the standard collision cross-section.  The small-minor region has size `eta^kappa`.  Optimizing `eta` produces a positive `epsilon^alpha` for each independent loop.

## B2.4 — finite-time propagation

The interface state is a factorial hierarchy of complete, time-ordered collision histories with open ancestral half-edges.  Slice composition glues those half-edges exactly.  A cutting argument controls large histories and loop opening controls recollisions created by the cut.  The proof therefore retains the correlation information emphasized in the existing cluster and long-time hard-sphere literature.

## B2.5 — LDP identification

The source pressure is proved from normalized connected coefficients.  For the lower bound, smooth positive controlled Boltzmann paths are implemented by exact tilts of the deterministic initial law; the history expansion proves concentration under those tilts.  Positive recovery makes such paths rate-dense.  Exponential tightness, exposed-point lower bounds, and extension to all finite-action controls are stated separately.

The grand-canonical theorem precedes B1.  Only the microcanonical theorem imports B1's exact-number local coefficient, preserving the noncircular dependency order.
