# Round-Twenty-Three mathematical regression suite

The checks below encode the explicit counterexamples in the Round-Twenty-Two report.  They are not numerical evidence for the main theorems; they prevent a later edit from silently reinstating a formula already disproved by the referee.

## A4-R1: regular-point residue

For a matrix or closed operator resolvent `R(z)` holomorphic at `z0`,

```text
Res_{z=z0} R(z)P = 0.
```

**Required source invariant:** the Round-Twenty-Three source contains no construction that enlarges a resolved space with a residue of the full resolvent at a point explicitly declared regular.  The only memory object is the Feshbach kernel through `QLQ`.

## A4-R2: large-z Feshbach coefficient

For bounded block products,

```text
PLQ (z-QLQ)^{-1} QLP
  = z^{-1} PLQLP + O(|z|^{-2}).
```

**Required source invariant:** the leading `z^{-1}` coefficient is displayed.  Time decay is derived from the orthogonal semigroup, not from a nonexistent generic cancellation.

## B1-R1: canonical normalization

For the normalized reference law `nu_{N,lambda0}`,

```text
q_N(0,0) = N^{-1} log E_nu[1] = 0.
```

For comparison, the forbidden raw object `(1/N!) integral exp(sum lambda C)` has the Stirling drift `-log N+O(1)` and may not be used as a finite limiting pressure without its activity/reference normalization.

## B3-R1: balanced tangent

At equilibrium `Gamma=A_f`, let `u` perturb `f` and set

```text
h = deltaGamma - DA_f[u].
```

The collision quadratic form must be

```text
Q(u,h) = (1/2) integral h^2/A_f,
```

up to the displayed transport/gauge blocks.  In particular `Q(u,0)=0`.  A source formula proportional to `|k+a|^2` fails this test and is forbidden.

## C1-R1: Dirac domination

An uncountable family `{delta_{Phi(x)}}` cannot be dominated by one probability measure with uniformly positive densities.  The hidden transition kernel must therefore remain outside the domination hypothesis.  Only observation measures may be dominated, stratum by stratum.

## A3-R1: order separation

Two legal two-mark words `AB` and `BA` may have the same empirical mark measure and the same total clock while producing distinct paths.  The state must contain an ordered word/path coordinate; empirical flow is only a contraction.

## A3-R2: KL absolute continuity

For a non-atomic reference kernel `K(x,dm)`,

```text
H(delta_m | K(x,.)) = +infinity.
```

Every finite-cell recovery kernel must have density `g_x=dq_x/dK(x,.)` and be supported on the cell.  Selecting one representative atom is forbidden.

## B4-R1: escaping kinetic energy

For `f_n=(1-n^{-2})phi+n^{-2}phi(. - ne_1)`, second moments remain bounded while energy is not uniformly integrable.  Hence second-moment boundedness alone is not compact in a topology testing quadratic growth.

**Required source invariant:** state/action sublevels contain a superquadratic de la Vallée--Poussin bound, for example a uniform `(2+delta)` moment.

## B1-R2: mixed lattice--continuous Gaussian conditioning

For covariance

```text
Sigma = [[Sigma_ZZ, Sigma_ZR], [Sigma_RZ, Sigma_RR]],
```

the continuous conditional law at lattice deviation `z` has mean

```text
Sigma_RZ Sigma_ZZ^{-1} z
```

and covariance

```text
Sigma_RR - Sigma_RZ Sigma_ZZ^{-1} Sigma_ZR.
```

An unshifted marginal Gaussian is forbidden unless the cross block is proved zero.

## C2-R1: stochastic exponential positivity

A Doléans exponential of a finite continuous Brownian integral is strictly positive.  A merely nonnegative uniformly integrable martingale may hit zero.  The likelihood representation therefore requires equivalent laws, strict positivity, and logarithmic integrability.

## D1-R1: LDP versus local asymptotics

An LDP supplies exponential rates, not a polynomial prefactor or local coefficient.  Every formula of the form

```text
P(E_j) = exp(-a alpha_j) a^{-gamma_j}(c_j+o(1))
```

must cite a proved local Laplace/Morse--Bott theorem, not the LDP alone.

## Machine-readable tokens

The source verifier requires the following exact tokens:

```text
A4_NO_REGULAR_RESIDUE
A4_CORRECT_Z_INVERSE
B1_NORMALIZED_PRESSURE
B1_SCHUR_CONDITIONAL_GAUSSIAN
B3_BALANCED_TANGENT_ZERO
C1_OBSERVATION_ONLY_DOMINATION
A3_ORDERED_WORD
A3_AC_RECOVERY
B4_SUPERQUADRATIC_COMPACTNESS
C2_STRICTLY_POSITIVE_LIKELIHOOD
D1_MORSE_BOTT_NOT_LDP
```
