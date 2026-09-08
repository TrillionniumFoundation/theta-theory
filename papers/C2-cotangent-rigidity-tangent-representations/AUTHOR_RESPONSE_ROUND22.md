# Author response to Referee Round Twenty-Two — C2

The topology, rigidity, optional-projection, and likelihood layers have each been replaced by a typed theorem with its own hypotheses.

## C2.1 — weighted strict topology

`C_W(E)` is mapped isomorphically to `C_b(E)` by division by `W`.  The weighted strict topology is the pullback of the standard strict topology.  Its continuous dual is therefore exactly the Radon measures with finite `W` moment, and its Mackey property follows under that homeomorphism.  The invalid normalized-tail sequence criterion has been removed.

## C2.2 — hard-sphere adjoint

The adjoint of the linearized balance operator is written explicitly as

`(-partial_t r - v.grad_x r - L_f^* r, Delta r)`

plus the finite collision-invariant source.  The nonzero collision operator is not absorbed into the contact component.  Closed range from B3 identifies the annihilator.

## C2.3 — pressure and periodic data

Pressure equality first gives equilibrium expectation identities.  A separate equilibrium-localisation lemma constructs potentials whose equilibrium states converge to each regular periodic orbit.  Only then are periodic sums obtained, followed by a constructive Livsic theorem.  Periodic data are no longer claimed to follow directly from a local pressure derivative.

## C2.4 — optional projections and brackets

The theorem assumes joint convergence of the prediction processes, convergence of their filter martingale problems, uniform tightness of semimartingale characteristics, and predictable bracket convergence.  Under these hypotheses optional projections, innovations, stochastic integrals, and brackets converge jointly.  Ordinary weak convergence alone is never used for this conclusion.

## C2.5 — likelihood exponential

The likelihood is assumed strictly positive with reciprocal moments, so the two measures are equivalent on finite horizons.  Brownian innovation representation then gives the Doléans exponential and Novikov control.  A merely nonnegative uniformly integrable martingale that can hit zero is not represented by a finite Brownian exponential.

The A3 and C1 examples now use the corrected ordered state and integrated belief kernel, respectively.  The positive rigidity and tangent-representation results are retained.
