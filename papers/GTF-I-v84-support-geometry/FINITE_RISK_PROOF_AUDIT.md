# Finite rational risk certificates — mathematical audit

## Claims and direct dependencies

| Claim | Proof input | Checkable conclusion |
| --- | --- | --- |
| `thm:finitecertificate81` | Explicit inward matrix grid; product telescoping; trace-norm contraction; fixed output subsets; interior metric | Complete finite rational inequalities imply risk for every real target, with radius and probability buffers |
| `prop:rationalreadout81` | Uniform POVM mixing; coordinate rounding; residual normalization; operator-norm row bound | A prescribed denominator contains a legal rational readout within the stated TV allowance |
| `thm:rationallearner81` | Previous all-confidence binary estimator and interior dictionary; two lemmas above; dyadic finite search; finite controls | Same optimal joint call and payload orders, with rational readout and finite risk certificate computed before access |

These are written analytic proofs. They require neither the unresolved A/B/C/D analytic gates nor a numerical hypothesis about a finite sample. Mele–Bittel supplies the existing statistical upper primitive; the local construction uses it only to establish a feasible count.

## Soundness, including boundaries

Set `K=ceil(4d/r)`. Moving `E` to `(1-8d/K)E+(4d/K)I` puts its spectrum in `[1/4+2d/K,3/4-2d/K]`. Gaussian-rational rounding changes operator norm by at most `d/K`; the rounded matrix is still legal and within `3d/K<=r`. For the theorem's `r`, the inward multiplier is positive. The actual grid is completely enumerated and filtered by full exact PSD tests.

The one-copy record difference has unhalved norm `2||E-G||_1/d`, and product telescoping bounds the `m`-copy norm by `2m||E-G||op`. The output TV is therefore at most `mr`. A nearby grid point defines one fixed subset of good indices. Those indices are all within `a+r` of the true effect, and their probability changes by at most `mr`. This step avoids an incorrect appeal to continuity of target-dependent indicator functions. Equality belongs to the good set.

## Rationalization, including zero-probability strings

Mix each `L`-outcome POVM with `s I/L`, `s=eta/16`. Every component now has a positive lower spectral margin `s/L`. Rounding the first `L-1` matrices at `Q=ceil(64L^2D/eta)` incurs norm at most `D/Q` per matrix; the exact final residual incurs at most `(L-1)D/Q<s/L`. Thus all effects are positive and their sum is exactly identity. This also bounds every effect above by identity. Both real and imaginary coordinates lie in `Q^{-1} Z`; reduced denominators may divide `Q`.

The index-law change is at most `eta/16+eta/32=3eta/32` for arbitrary subnormalized classical conditioning blocks. There is no division by their unknown probabilities. All `2^m` conditional POVMs must be present and legal, even when some branches have zero probability for a target. The one-outcome case uses the identity exactly.

## Termination and resource order

A finite prescribed-denominator class is exhausted at each `m=1,2,4,...`. Its tests use only public rational data. Every failed stage therefore terminates. The existing estimator at error `delta/(128 ceil(sqrt(N)))` and failure `eta/8`, followed by clipping and the unchanged dictionary, has operator error below `a=delta/(8 ceil(sqrt(N)))`. It defines a feasible ideal POVM by a finite Borel partition. Padding with ignored extra Choi records gives such a POVM for all `m>=m0`.

Rational approximation raises failure from `eta/8` to at most `7eta/32<eta/4`, so the prescribed finite class has a passing member at the first dyadic count above `m0`. Hence `M<=2m0`, rather than just eventual termination of a general dovetail. Its implicit statistical constant need not be supplied to the algorithm.

## Operational implementation

The exact certificate gives ideal future loss at most `5delta/8`, failure at most `5eta/16`. Rational positive effects have computable algebraic positive square roots and a finite readout dilation. Allocate total unhalved error `eta/(M+1)` to each of `M` fresh-pair preparations and one complete final readout, splitting target-approximation and actual trusted-realization errors. The complete output-law TV cost is at most `eta/2`; actual failure for `d_N>delta` is at most `13eta/16`. Input-reference pairs remain separated from earlier retained outputs throughout acquisition.

## Executed versus mathematical scope

`finite_risk_certificate.py` verifies supplied exact tuples and regenerates the complete public target grid. A size cutoff yields incomplete verification. `finite_risk_check.py` records the completed scalar certificate and local complex-matrix identities, as well as rejection controls. The general high-dimensional exhaustive search, theorem-scale tomography acquisition, and physical readout are not claimed executed. No polynomial-time verification or synthesis bound follows from the finite theorem.

The main proof includes explicit candidate counts and raw array-storage bounds. Those bounds do not alter the charged decoder payload or replace the unresolved growing-dimensional full-body minimax problem. The old semialgebraic construction, full-body rates and all inherited proofs remain active unchanged.
