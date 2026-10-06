# Proof audit — Revision 64

This is an author-side derivation audit. It is not an independent referee report.

## New dependency chain

    full LPS action gap + spherical caps
        -> inherited v62 return-free entropy occupation, including logarithmic term
    finite one-pass complete configurations
        -> common stochastic boundary rows + legal conditional-mean decoder
        -> finite bit–accuracy obstruction
        -> logarithmic-or-linear lower-space dichotomy
    exact rational orthogonality + truncation toward zero
        -> every approximate state remains in the closed unit ball
        -> prefix error <= t sqrt(3) 2^(-b)
        -> legal rational density decoder and endpoint Frobenius bound
    exact denominator-five fallback + capped parameter scan
        -> O(min(N, L+log(N+1))) writable bits, including temporary storage

The new lower theorem depends on v62, not on the stronger v63 rate theorem. The latter remains in the paper because bit-space order is a coarser question and does not replace its exponential-rate result.

## Checks of hypotheses and quantifiers

1. The input word is read once. Input-dependent information cannot be hidden in a revisitable input or readable output tape, a private address or an uncharged clock.
2. The stochastic reduction includes all private state. Almost-sure between-command termination makes every boundary row sum to one. A fresh random tape's old bits cannot be reused unless retained and counted.
3. The terminal conditional mean is legal by convexity of the density-matrix set. Therefore lower bounds for mean correctness apply to randomized algorithms; samplewise lower correctness is not assumed.
4. The six-letter LPS Koopman gap is the full spherical bound. A fixed-dimensional matrix norm does not suffice.
5. The lower bound retains `1+6 log(12k)` before inversion. For epsilon<=1/4 the remaining coefficient is bounded by an absolute multiple of epsilon. Splitting those two positive terms gives the two alternatives uniformly over all L.
6. Absorption of additive constants is justified by a two-word witness: all x versus x^(N-1)y give density matrices at distance sqrt(8/5), hence a single decoder is impossible at error <=1/4.
7. A fixed work-tape program has at most exponentially many complete configurations in its bit-space, including its polynomial number of possible work-head positions. Arbitrarily large hardwired finite control cannot be smuggled into a universal minimum by calling it free storage.
8. Coordinatewise truncation toward zero contracts each absolute coordinate. It therefore preserves Euclidean norm, unlike floor or nearest rounding. No approximate spectral decomposition or projection is used.
9. Orthogonality propagates one-step deterministic errors additively, not exponentially. Frobenius error is Euclidean Bloch error divided by sqrt(2). The chosen two extra precision bits safely cover the factor sqrt(3/2).
10. Exact-mode numerators have norm 5^t; their bit length, the denominator and temporary small-integer products cost O(t+1), not a free exact-arithmetic operation.
11. The choice between exact and approximate modes depends only on the supplied numerical parameters. Capping L at N avoids retaining an arbitrarily huge requested precision; the physical command stream is not reused.
12. Binary output consists of a constant number of signed integer numerators and one denominator. Decimal conversion is not asserted to have linear bit time. The Python reference uses hexadecimal output and is not described as a literal optimal-space Python allocator.

13. The rational-orthogonal extension uses legal unit-ball decoders. The lower proof uses only the decoder norm bound; the upper starts from a truncated rational seed and budgets N+1 rounding errors. Fixed common denominators cost O(N) bits in exact mode. No preservation of a general orbit hull or PSD cone by coordinate truncation is assumed.

## Claim boundaries

The result is a uniform two-parameter order theorem for a fixed rational numerical experiment. It is not a theorem on physical quantum preparation, repeated quantum measurement, arbitrary irreversible dynamics, language recognition, optimal leading bit constants, or a removal of the remaining multiplicative crossover loss in label width. General compact actions still require their stated geometric and spectral hypotheses.

The structural companion, including its repeatable-probe model and the stronger v62 causal minimum, is retained. The new section has no logical dependency on the independent A/B/C/D analytic gates. None of their aggregate flags is changed.
