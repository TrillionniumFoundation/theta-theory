# Author-team AI mathematical challenge: unrestricted approximation

Reviewed source: `research/realization/51-unrestricted-approximation.tex`.
Reviewed SHA-256: `4763767ab0ac35e6380a7bba2bf30039ef17ba03f25635d104fe8ca03650e421`.
This is an internal author-team AI challenge, not an external referee
report, proof-assistant verification, human endorsement, or editorial
decision. The file was read against the actual R76 instrument, return
approximation and physical-dictionary source definitions.

## Checks and findings

1. **Robust antichain.** From `lambda_n d_m >= b`, one summand is at least
   `b/M`; both factors are at most one, so both factors are at least `b/M`.
   The diagonal bound forces that coordinate of `lambda_m` strictly below
   `b/(2M)` when `epsilon < b^2/(2M^2)`. Thus each ordered pair of threshold
   supports has a witness outside the other support. This proves an
   antichain, not merely a family of different supports. The displayed
   random-permutation argument gives the central-binomial count exactly.
2. **Conditioning is justified.** Joint stopped-record TV bounds both
   herald mass and herald-and-rejection mass. With `delta <= p_* s^2/(32M^2)`,
   the simulator herald mass is positive. The bounds
   `lambda_n d_n <= s^2/(16M^2)` and `lambda_n d_m >= s/2` follow. The former
   is strictly below `(s/2)^2/(2M^2) = s^2/(8M^2)`, leaving slack for the
   strict antichain hypothesis. No assumption that conditioning preserves
   TV error was made.
3. **Causal quantifier.** A common `lambda_n` exists because the binary test
   is requested only after the herald and a fixed causal controller cannot
   inspect a future request or an uncounted copy of the policy's full plan.
   Decoder entries may otherwise be completely arbitrary. This is the
   material operational condition; it must stay explicit in abbreviated
   statements.
4. **Finite-cost qubit tests.** In the actual undamped instrument, report
   `1` initially has probability `1/8` and prepares the pure reset state;
   every later zero report has probability `1/8`. Prefix `1 0^n` has
   probability `8^{-(n+1)}` and leaves the displayed rotated pure state.
   Initial randomization with `zeta=min(1,7B/8)` gives expected call cost
   `zeta sum_{j=0}^n 8^{-j} <= B`, for every positive B and every n. The
   terminal test is cost-free under the inherited definition. The cost is
   measured under the target law, not the simulator's law.
5. **Algebraic phase.** `(3+4i)/5` is not a root of unity because its sum
   with its inverse is the nonintegral rational `6/5`. For every q, its
   real numerator has integral denominator `5^q`; positive separation from
   one is therefore at least `1/(2*5^q)` in the rejection probability.
   Substitution gives exactly `25 zeta/(128*200^J*J^2)`. The phase is a
   Bloch angle, and the inherited unitary uses the half-angle; there is no
   unaccounted squaring of the phase.
6. **General algebraic phase.** The field norm of
   `A^q(z^q-1)` is a nonzero integer. Bounding all conjugates except z by
   `2 max(1,|z_j|)^q` yields
   `|1-z^q| >= 2^{1-D} H^{-q}`, and hence rejection margin
   `>=4^{-D} H^{-2q}`. The displayed `8 H^4` exponential condition follows.
7. **Asymptotics and scope.** Exponential-in-J error thresholds give
   `J = constant * log(1/delta) - O(log log(1/delta))`. The antichain lower
   `a(J)>=log_2 J` therefore gives the stated liminf coefficient one for
   `log_2 log_8(1/delta)`. This does not give the Born-dictionary logarithmic
   lower in the unrestricted class; the manuscript correctly retains that
   gap and does not infer an extra pure initializer.

No mathematical correction was found in these arguments. The inherited
physical upper bounds and their seed geometry remain inherited proof
dependencies, not independently reproved in this focused challenge. The
new finite calculations do not establish a matching unrestricted rate,
the full general-M risk frontier, or journal suitability.
