# Equal-prior initial-spectrum evaluator — Revision 95

Input is a JSON object containing `spectrum`, a nonincreasing or arbitrarily ordered list of exact rational strings/integers summing to one, `t`, an exact rational in [0,1], and optionally `fresh_dimension`, an integer between two and d. Every eigenvalue must be nonnegative; d is the list length and is at least two. Floats and booleans are rejected. The old receiver dimension is exactly the theorem's upper allowance two; this is not an all-rank evaluator.

`--bits` between 1 and 4096 chooses the rational square-root enclosure refinement. Output includes dimension, largest eigenvalue, q, v, exact lower/upper score bounds, and flags making clear that neither a physical reset certificate, unknown eigenbasis, actual preparation nor continuum proof is computed. The interval is obtained by monotone rational substitutions into the explicit square-root formula, not by trusting a floating-point rounded value.

The supplied example has d=3, spectrum (3/4,1/8,1/8), t=1 and fresh dimension two. Its two commuting rank-two atoms admit the support-inverse instrument checked exactly in the companion regression suite. A basis family is a separately specified weighted exact second-moment experiment; the evaluator does not synthesize one.
