# Author response to Referee Round Twenty-Two — B4

The compactness and topology layer has been replaced rather than defended.

## B4.1 — compactness

The kinetic shell now carries a uniform `(2+delta)` velocity moment and the `W_2` topology.  This makes quadratic energy uniformly integrable.  The referee's sequence with mass `n^{-2}` at velocity `n` has `(2+delta)` moment of order `n^delta` and is not contained in a fixed shell.  Action compactness combines this moment bound with a negative-Sobolev time modulus from the balance equation.

## B4.2 — transfer metric

Control transfer is proved directly by synchronous coupling in `W_2`, the metric assumed by the theorem.  No weak countable-test metric is upgraded to weighted `L^1`.  Finite-action controls are reached by truncating their relative multipliers and then using entropy convergence.

## B4.3 — product collision measures

`W_2` convergence plus the uniform superquadratic moment implies convergence of product measures and uniform integrability of the linear-growth collision kernel.  A velocity truncation proves `A_{f_n} -> A_f`; the entropy topology then passes controlled currents `q_n A_{f_n}`.

## B4.4 — semigroup limit

The Nisio semigroup is constructed on bounded uniformly `W_2`-continuous functions.  The discounted resolvent satisfies the implicit identity

`R_lambda h = R_mu(h + (mu-lambda) R_lambda h)`,

derived from dynamic programming; no linear pseudo-resolvent product is used.  The limiting Hamiltonian has an explicit cylindrical core, the `(2+delta)` moment is a containment function, and a Wasserstein doubling proof gives comparison.  B2's retained collision histories produce exact specular BBGKY correctors on a diagonal history cutoff.  Half-relaxed limits plus comparison prove the nonlinear semigroup convergence.

The positive compactness, Nisio, generator, and finite-volume convergence results are retained on the corrected state topology.
