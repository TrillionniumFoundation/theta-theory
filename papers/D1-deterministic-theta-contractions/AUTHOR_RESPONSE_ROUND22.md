# Author response to Referee Round Twenty-Two — D1

D1 now derives phase weights from a local theorem rather than assigning them to an LDP.

## D1.1 — polynomial phase weights

Each phase has a source-inserted local density/coefficient expansion with a positive `C^2` amplitude and a Morse--Bott normal form.  Tubular Laplace integration gives

`exp(-N gamma_j) N^{-kappa_j} c_j`,

where `kappa_j` includes the local Gaussian codimension and all upstream lattice, saddle, exact-number, and conditioning powers.  The determinant integral over the minimizer manifold gives `c_j`.  This information is explicitly stronger than the LDP.

## D1.2 — microscopic cells and conditioning

Phase events are inverse images of disjoint tubular order-parameter cells in the original microscopic space.  Their boundaries are regular level sets with rate strictly above the phase minimum, so they are `I`-continuity sets.  Goodness and exponential tightness first confine all minimizers to a compact sublevel; only then is the complement of the cells separated.  No compactness of the ambient state is assumed.

## D1.3 — shared policy

The controlled state carries the phase posterior and a phase-specific hidden-state belief for every component.  One common action updates all components and their weights.  Optimization is outside the phase log-sum.  Separate phasewise optimizers, which would reveal the latent phase, are not used.

## D1.4 — complex charts

Component partition functions inherit analytic local expansions from the upstream source-inserted theorem.  A phase chart is zero-free only under a proved real-part dominance gap, by Rouché's theorem.  At coexistence, the finite analytic phase sum is retained and zeros are not excluded by declaration.

## D1.5 — Gaussian mixture

Fluctuations are centered by the labelled phase mean.  Mixture weights use the complete `exp(-N gamma_j) N^{-kappa_j} c_j` factors.  At an exponential tie, smaller polynomial exponent dominates; equal exponents are weighted by the local constants.  Means are not reintroduced after global centering.

The positive labelled contraction, phase-posterior control, complex response, and coexistence Gaussian results are retained with these local inputs.
