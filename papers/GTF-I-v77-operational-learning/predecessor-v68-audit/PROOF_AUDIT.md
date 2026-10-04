# Proof audit — Revision 68

This is an author-side proof audit, not a new external referee report. The controlling report is v67/r44 at `68c69a4a2e8b4e3b11c43a181806ab578584b719`, with audit `7a9586cd8cf7995152fbbf501f3e47da4aa89900`. The native mathematical predecessor is the already qualified v67 publication; its ten additions are inherited and remain available with complete proofs.

## 1. Local binary estimate

For a probability gap at most N^(-1/2), use a clipped ramp centred at N(p+q)/2 with half-width 4 sqrt(N) and slope 1/(8 sqrt(N)). The exact derivative of its binomial expectation is N times the mean one-step increment under Bin(N-1,t). Chebyshev keeps at least 3/4 of this law inside the affine interval, even at p=0 or q=1, yielding derivative at least 3 sqrt(N)/32. Larger gaps follow by monotone coupling. No normal approximation, hidden variance floor, lattice limit or asymptotic remainder enters the proof.

The normalized Choi-state Helstrom projection has probability gap at least tuple-Frobenius distance/(2d). The unhalved convention supplies the factor two. Pair-dependent testers are admissible in a metric supremum; each tester is the same in the two worlds. They never depend on an observed secret experiment label.

## 2. Joint interior code length

An intrinsic s-dimensional ball of radius R=1/(mn)-a lies inside the positive-margin body. A packing at scale 32d delta/sqrt(N) has cardinality at least (R sqrt(N)/(32d delta))^s. The local test separates its points by more than 2delta for delta<=1/32. Arbitrary legal decoded centres therefore need at least that many words, without a margin requirement on the centres.

The inherited intrinsic rational grid has B=O_dims,a(sqrt(N)/delta) and an s-digit payload. Combining these finite estimates, rather than allowing the remainder to depend on delta, gives (s/2)log2N+s log2(1/delta)+O_dims,a(1) for the entire declared parameter range. This theorem charges reusable description length only.

## 3. Preparation metric and references

Input erasure makes the repeated experiment a fixed quantum processor applied to N independent copies of the cq preparation state. The processor includes all tester memory, feedback and public stopping. Trace contraction gives the upper metric identity; a tester retaining every output gives equality. The processor is quantum and is not a classical physical realization claim.

## 4. Singular factor code

No-pivot Cholesky works at zero pivots because a PSD zero diagonal forces the residual row/column to vanish. Each nonzero factor column is counted by one positive pivot, so at most r_y(2n-r_y) real coordinates occur in a rank-bounded block. Together the factor coordinates lie on a unit sphere of dimension at most v=sum r_y(2n-r_y)-1.

One largest-magnitude anchor removes the redundant radial coordinate. Directed rounding of ratios incurs Euclidean error sqrt(h-1)/B before normalization and at most twice that afterwards. Integer factor products are PSD with total trace exactly T. No new columns are introduced, proving rank nonincrease and exact zero-outcome preservation. Product purification gives d_N<=4 sqrt(N(h-1))/B with no small-eigenvalue assumption.

For rational matrices each signed squared factor coordinate is rational. Computing ratio digits by integer square roots is exact even when the factors themselves are irrational. Reduced-rational Schur/minor bounds control operand growth. These preprocessing resources are explicitly not the optimal compressed payload length.

## 5. Rank-boundary converse

A local full-rank-within-the-bound stratum has dimension v. Positive leading principal minors supply unique lower-trapezoidal factors, and the normalization removes one real coordinate. The factor-to-state map has a smooth inverse on a small fixed patch, obtained by leading-block Cholesky and bottom-left multiplication. Shrinking to a closed coordinate ball makes this chart quantitatively bi-Lipschitz. Volumetric packing plus the same local binary test supplies the v-dimensional converse for N-copy trace distance. Lower ranks cannot enlarge the upper exponent; the maximal rank patch already supplies the lower one.

The v=0 singleton, pure-state coefficient 2n-2, full-state coefficient n^2-1, and classical coefficient m-1 are handled explicitly. The converse is not asserted for arbitrary disturbing instruments at the boundary. The inherited unitary phase example is retained as the contrasting phenomenon.

## 6. Checks and unchanged dependencies

`check_preparation.py` validates exact finite binary gaps, independent Gaussian-rational rank calculations, zero-outcome inputs, nonleading pivots, small eigenvalues, all code metadata, exact product trace bounds for pure states and classical distributions, and malformed/altered certificates. A failed first test attempt used a helper that incorrectly required every diagonal entry of a product of Hermitian matrices to be real; the test was corrected to check that their sum is real. No mathematical or implementation claim was weakened. All five inherited exact suites remain enabled in normal and optimized modes.

The old full Koopman/cap, legal-output, fixed-program, positive-probe and repeatable classical-probe hypotheses remain. These coding arguments use none of the independent raw local-limit, stopped LDP, global-kernel, filtering/LAN, Mosco/Nisio or response gates. No aggregate status is changed. Independent priority, signatures and journal acceptance remain separate from source qualification.
