# Numerical evidence — v12

These are executed finite diagnostics, not a continuum proof or journal assessment.
The full exact-rational receipts are produced by `validate.py` in `validation/`.

## Integrated adaptive physical programs

The shared detector has exponents `(0,1,2+gap)` and cell coefficients
`((1/3,-1/16,-1/16),(1/3,1/16,0),(1/3,0,1/16))`. Total trial budget is
three, with two prefix stages and remaining physical product queries.
Each refinement receives newly perturbed finite coefficient and moment data.
The exact-collision numerical names deliberately break equality of coincident
formal moments. The reference truth uses independent exponent-keyed algebra.

The finite domain is the entire two-command alphabet
`{(1/4,3/4,1/4),(3/4,1/4,3/4)}`. The line domain is the entire continuous
common-command line `g=(u,u,u)`, `1/4<=u<=3/4`, with an analytically exact
posterior quotient. Neither domain is called the full command cube.
A finite command alphabet eventually has an exact finite-state representation;
these tests are not used as evidence for a contrary asymptotic lower law.

| gap | domain | M | selected b | table payload bits | maximum query error |
|---|---|---:|---:|---:|---:|
| 0 | finite_two_command | 1 | 7 | 406 | 0.003598284 |
| 0 | finite_two_command | 2 | 8 | 609 | 0.001858977 |
| 0 | finite_two_command | 4 | 9 | 1020 | 0.000807709 |
| 0 | common_command_line | 2 | 8 | 585 | 0.001858977 |
| 1/1000000000000 | finite_two_command | 1 | 7 | 406 | 0.003598284 |
| 1/1000000000000 | finite_two_command | 2 | 8 | 609 | 0.001858977 |
| 1/1000000000000 | finite_two_command | 4 | 9 | 1020 | 0.000807709 |
| 1/1000000000000 | common_command_line | 2 | 8 | 585 | 0.001858977 |
| 1/7 | finite_two_command | 1 | 7 | 406 | 0.003352947 |
| 1/7 | finite_two_command | 2 | 8 | 609 | 0.001736915 |
| 1/7 | finite_two_command | 4 | 9 | 1020 | 0.000503575 |
| 1/7 | common_command_line | 2 | 8 | 585 | 0.001666969 |

Payload uses one `ceil(log2(M+1))` field per transition and `output_bits+1`
per dyadic output. It excludes the fixed interface, framing, clock, offline
histories and workspace; it is not Python object memory usage.

The exact true finite covering radii are computed independently: a set of
points lies in an unrestricted radius-e maximum-norm ball iff its diameter
is at most 2e. Covering by M such balls is therefore graph M-colouring for
the graph connecting incompatible pairs. Exhaustive search at all critical
pair distances determines the radius. The heuristic order only accelerates
search; it does not replace the exact decision. There are at most 15 distinct
points in these physical fixtures. Every numerical stopping bracket and final
scale is compared to that oracle, rather than to a compiler-supplied radius.

## Mutations and frozen allowances

The old v11 mutation is reproduced exactly: 8,207 assertions pass despite
775/1,389 changed targets over 52 calls. The same two-call-site mutation applied
to v12 cannot complete: the independent adaptive gate rejects it after 17 calls,
with 572 changed entries among 1,002 seen. The legacy physical residual checks
still pass before this rejection, because that residual theorem remains valid.

In the integrated physical fixtures, these nonvacuous changed-entry totals are
independently rejected (totals count distinct mutation attempts, not unique
program entries):

- collapse: 168.
- last: 136.
- erase_state: 99.
- erase_report: 138.
- erase_command: 6.

The data-fixed radius allowances are asserted unchanged under mutation. Wrong
nearest-centre ties are tested separately. A control that changes no entry is
reported as not a mutation, not counted as a successful rejection.
The original zero-decoder and nonconstant-decoder controls remain in v11.

## Independent covering-order witness

For the exact interval system, the optimal radius is `1/(8M)` by its continuum
length argument, not by a finite empirical fit. At M=1,2,4,8,16,32 the correct
program's grid error is at most twice that radius. Collapsed transitions have
error exactly 1/4 for every M, hence error/radius = 2M. Every actual collapse
for M>1 is rejected by the independent nearest-centre contract.

## Additional stability and arithmetic diagnostics

One common-advice program is executed for two different compact interval
systems at four data floors/budgets and on 65 off-grid commands each. Both
models' true radii are checked against every adaptive bracket. The explicit
positive-detector lower witness checks common moment-name compatibility and
the exact physical prediction gap. Paired physical histories at different
calibrations check the finite-moment stability estimate. Exact rational powers
verify the reduced denominator `2^(Nb)`, not a purported b-plus-constant
exact workspace bound.

## Execution scope

The new suite executes 26,158 named assertions. The inherited v10 and v11
suites execute 7,904 and 8,207 respectively. These counts are diagnostics,
not independent theorem counts. The separate legacy v10 referee/mutation
scripts are not rerun by this validator. The four-cell five-trial phases,
a fine off-grid net of the whole cube, and arbitrary prior/input-oracle
certification remain outside the finite experimental coverage. The manuscript
retains the analytic full-cube proof and all historical specializations.
