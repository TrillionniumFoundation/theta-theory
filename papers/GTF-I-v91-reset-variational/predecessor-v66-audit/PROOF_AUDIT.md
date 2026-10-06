# Written-proof audit — Revision 66

This is an author-side audit of the written arguments, not an independent referee report or formal proof-assistant verification. The latest external assessment is v65/r42; it does not assess the new theorems in this revision.

## Rational instrument repair

`eq:choiconvention66` fixes input-first unnormalized Choi matrices. Summed output partial trace is `I_d`, hence summed Choi trace is `d`. Confusing this with a trace-one channel-state convention loses a dimension factor.

For a coordinate grid approximation `T_y`, the error has operator norm at most `2nd/B`. Partial trace on the `n`-dimensional output has Hermitian operator-norm bound `n`, so the common residual has norm at most `2mn^2d/B`. Correcting only outcome one in one output coordinate therefore gives operator error at most `c/B`, where `c=2nd(1+mn)`. Adding `c I` to the integer numerator gives positivity; partial trace of that addition is `nc I_d` in each outcome. Division by `B+mnc` exactly restores trace preservation.

The difference numerator is `B(Q_y-J_y)+cI-mncJ_y`. The three summed trace-norm terms are bounded respectively by `mndc`, `mndc`, and `mndc`; the last uses positivity and total Choi trace `d`. This gives the explicit `3mndc/(B+mnc)` bound. Each output numerator entry is bounded in modulus by the denominator, because positive matrices and the joint partial trace bound control diagonals and then off-diagonals.

The map from supplied numerical coefficients to a Choi matrix is not asserted to be a quantum operation. The *resulting Choi matrices* define linear completely positive maps. This distinguishes the construction from tensoring the nonlinear state repair with an identity.

## Complete norm and adaptive comparison

The Choi/diamond estimate is proved for arbitrary auxiliary dimension. A unit rank-one input is represented using coefficient maps of Hilbert–Schmidt norm one; their operator norms are at most one. Singular-value decomposition extends the estimate to arbitrary input matrices. Thus no restriction to separable reference inputs or positive test operators is hidden in the induced-norm upper bound.

The common tester may retain quantum memory and perform joint operations. Each neighboring hybrid pair shares its state before the changed slot; a classical command/history block weights the slot error by its trace. Subsequent common channels contract trace norm. An absorbing public halt flag makes bounded stopping a case of the same argument. This is the standard network hybrid principle, explicitly credited, applied to the integer descriptions.

The theorem is not a physical classical state-preparation procedure for an unknown quantum input. A specified numerical joint simulation charges its joint dimension and description.

## Posterior conversion

For `A=p rho` and `B=q sigma`, the inequality `|p-q|<=||A-B||_1` yields `p||rho-sigma||_1<=2||A-B||_1`. It remains valid with arbitrary `sigma` when `q=0`. Summation gives the true-law expectation bound; Markov's inequality gives the tail bound. The pooled-event bound divides by its true probability, not by each individual branch weight. There is no assertion that all rare normalized posteriors are uniformly accurate.

The numerical stopped bound freezes halted blocks. Only live blocks are repaired; their total mass is at most one. Consequently the original `(N+1)6d^2/B` budget remains valid without a union bound over stopping times.

## Variable-description numerical theorem

The exact entry formula is `S[alpha,beta]=sum_ij C[i alpha,j beta]P[i,j]`. Tests compare this expression with the full complex Kraus update to catch a transposition/conjugation error. Positivity is supplied by the Choi criterion, and the exact mass identity is `sum_y tr S_y=D_a tr P`.

No rational Kraus factorization needs to be supplied or computed. No claim of its impossibility is made. Exact mode retains unnormalized numerators whose traces are at most `z0 Dmax^t`. Approximate mode retains the fixed state denominator and reuses the fully written branch-mass recursion. The program processes outcomes sequentially rather than retaining every branch matrix.

The new PSD validator reduces rational Schur complements after every operation. Ratios of minors and Hadamard's bound give polynomial operand lengths. This replaces the fixed-dimensional unreduced scaled Schur routine only in the new variable-input parser; the inherited implementation remains unchanged. Input validation is charged separately as polynomial preprocessing. The streaming formula is not falsely declared to include a sharper linear-space validator.

Worst-case storage applies to every rejection trial; runtime and fair-bit use are expected. Literal interpreter allocation, operating-system entropy and formal bit-machine compilation are not certified by the regression suite.

## Mathematical clarification of r42 detailed comment 1

The exact promised density input has nonnegative diagonal entries. Directed truncation of the first `d-1` entries leaves their sum between zero and one; the trace-completing last coordinate is therefore in `[0,1]`. The report's suggested out-of-range scalar warning does not apply to this definition. `rem:diagonal66` records the calculation. The matrix may nevertheless be indefinite, and the old `(4,6;6,9)/13` counterexample is preserved. Positivity of the whole matrix still requires the buffer.

## Inherited proof and release boundaries

All prior complete-edition labels remain active. The 16 old labels from Sections 32–33 leave only the structural focused proof graph and remain in both quantitative and complete graphs. The relocation is explicit in the manifest and checked at both destinations. All 85 predecessor native files remain at the base repository paths with their hashes checked.

The fixed-program lower theorems retain the full-action gap, all-direction cap, pure-target and legal numerical-output hypotheses. No general noisy transcript-only lower bound or disturbing-process classification is asserted. The v63 multiplicative width gap, independent priority question and independent A/B/C/D analytic obligations are unchanged.
