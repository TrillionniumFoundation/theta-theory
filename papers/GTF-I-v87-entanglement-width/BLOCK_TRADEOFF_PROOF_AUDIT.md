# Proof audit: independent-block learning tradeoff (v78)

## Statement and scope

`sections/58-block-resource-learning.tex`, Theorem `thm:blocklearning78`, proves

\[
M_b^\star(d,N,\delta,\eta)
=\Theta_d\!\left(\frac{N^2}{b\delta^2}\log\frac1\eta\right)
\]

for fixed `d >= 2`, `1 <= b <= N`, sufficiently small absolute `delta > 0`, and `0 < eta <= 1/8`. The upper bound is explicitly `C d^4 N^2/(b delta^2) log(d/eta)`; no sharp growing-dimension claim is made. The scalar exception is `Theta(N delta^-2 log(1/eta))` independently of `b`.

This is a mathematical proof audit, not a formal proof-assistant certificate or an independent human priority assessment. The proof introduces a resource restriction within the retained ordered, binary, input-consuming, classical-output interface. It does not extend the interface to general POVMs, disturbing instruments, or channels with residual quantum output.

## Exact access boundary

Definition `def:freshblocks78` permits arbitrary classical feedback, retained quantum outputs, arbitrary collective instruments at block boundaries, and a final collective estimate. Conditioned on the complete classical history, each newly selected block is prepared from common parameter-independent resources, tensor-separated from old quantum registers. The *entire* current tester, including references and unused inputs, stays isolated from old registers until its final declared call. The next boundary may process old and new outputs jointly.

Initial tensor separation alone is insufficient: a later interaction with the current reference can transfer old quantum information into unused queried inputs. Similarly, a retained register may not be relabelled as a fresh one. The source explicitly excludes these operations during an active block. The cap is a cap on independent query-block length, not a bound on all entanglement in the stored output or on arbitrary protocols with unrestricted coherent memory across calls.

The length `t` is chosen from the classical history *before* each block and charged in full. Internal early exit is padded within that declared length. The every-record budget bounds the sum of declared lengths. Boundary stopping is unrestricted subject to that deterministic cap. A cap only on actual calls combined with uncharged larger declared maxima is not the model proved here.

## Upper bound

Lemma `lem:blockhybrid78` proves `d_N <= ceil(N/b) d_b` by replacement of consecutive groups of calls in an arbitrary future tester. The common prefix, including its retained quantum memory, is a legal reference-assisted input to the changed group. The common suffix contracts trace distance. Padding covers public stopping.

The retained common learner, Theorem `thm:matrixlearning77`, is run at future horizon `b` and accuracy `delta/ceil(N/b)`. Its construction already uses fresh independent blocks with no quantum memory carried into future probes. Its call count is

\[
C d^4 b\lceil N/b\rceil^2\delta^{-2}\log(d/\eta)
\le 4C d^4 N^2(b\delta^2)^{-1}\log(d/\eta).
\]

The output is legal and Gaussian rational as required by the retained codec. Every-record budgets and the uniform conditional guarantees are inherited unchanged from the retained learner at the new public parameters.

## Lower bound: the finite pair

Lemma `lem:blockfidelity78` embeds

\[
E_\phi=\tfrac12(I+\cos\phi\,\sigma_1+\sin\phi\,\sigma_2)
\oplus\tfrac12 I_{d-2}.
\]

The common unitary representation is `M_theta = M_0 o Ad_(U_theta*)`, where `U_theta = exp(-i theta sigma_3/2) oplus I`. Its numerical range has real part at least `cos(|theta|/2)` for `|theta| <= pi`. Hence one reference-assisted call contributes Bures angle at most `|theta|/2`. The Bures-angle triangle inequality and contraction under common controls give root fidelity at least `cos(t |theta|/2)` for any internally adaptive common `t`-call tester when `t |theta| <= pi`.

For `b |theta| <= 1` and `t <= b`, this is at least `exp(-t^2 theta^2/4) >= exp(-bt theta^2/4)`. The restriction on angle is essential: a sufficiently long block can distinguish this pair perfectly, so the exponential inequality is not asserted for arbitrary angle and length.

The explicit parallel GHZ state with relative phase `alpha = N theta/2 + pi/2` has output parity means `-sin(N theta/2)` and `+sin(N theta/2)`. Its unhalved distance is `2 |sin(N theta/2)|`. The same Bures-angle estimate gives the opposite adaptive upper bound, proving the exact identity `d_N^na = d_N = 2 sin(N |theta|/2)` for `N |theta| <= pi`. Its two-dimensional case is contained in known multiple-shot projective-discrimination formulas and is cited to `PPKKO72`, Corollary 1 and Theorem 2; it is not claimed as new. This is a finite-pair calculation; the probe may depend on both hypotheses and is not used as a common learner.

## Lower bound: adaptive histories and stopping

Use subnormalized retained states `A_h` and `B_h`, with history probabilities included in their traces. Root fidelity is additive on classical direct sums, multiplicative on tensor products, and nondecreasing under common instruments after summing their branches. These identities require no common support assumption.

For `a = b theta^2/4`, the proof tracks

\[
\Psi=\sum_h e^{-a(M-m(h))}\mathfrak f(A_h,B_h),
\]

where `m(h)` is the charged call count stored in the history. Initially `Psi = exp(-a M)`. A fresh length-`t` tester multiplies that branch's fidelity by at least `exp(-a t)`; reducing the remaining charge by `t` multiplies its potential weight by `exp(a t)`. The branch contribution cannot decrease. A common boundary instrument cannot decrease the sum of its child fidelities, and all its children inherit the same charge before selecting their next tester. Stopped branches are carried unchanged.

Positive block lengths give at most `M` block generations. At termination all potential weights are at most one, so full transcript/output root fidelity is at least `exp(-a M)`. Final collective processing can only increase it. Histories with different call counts are not merged during the calculation. This is a finite induction, with no optional-stopping theorem and no unjustified factorization of unconditional record laws.

The source includes measurable classical outcomes by replacing sums with integrals against a common dominating history measure. The direct-integral fidelity identity and instrument inequality follow by finite coarse-graining and refinement; each coarse-graining keeps the integer charge field. Thus continuous-valued boundary instruments are not silently excluded.

## Testing, confidence, and scalar exception

Choose `theta = 4 delta/N` and reduce the inherited absolute accuracy cap to at most `1/4`. Since `b <= N`, the local fidelity condition holds. The exact future distance is `2 sin(2 delta) > 2 delta`, so radius-`delta` success balls are disjoint. An estimate with failure at most `eta` gives a binary test with both errors at most `eta`. Its root fidelity is at most `2 sqrt(eta)`. Data processing and the preceding bound yield

\[
M\ge \frac{N^2}{8b\delta^2}\log\frac1{4\eta}
\ge \frac{N^2}{24b\delta^2}\log\frac1\eta.
\]

The full confidence logarithm follows directly from fidelity. No relative entropy or likelihood support bound is used on the projective pair. For `d = 1`, Bernoulli endpoint learning and the retained scalar converse give the separate block-independent order.

## Consequences and prior ingredients

Corollary `cor:onecallseparation78` applies to any acquisition interface consisting of independent one-call probes/references, even with collective final reconstruction. This includes independently prepared Choi copies and the separate known-input measurements discussed in `MB67` and `ZRK76`, respectively. It proves a worst-case future-loss limitation of the interface, rather than inferring one from a sufficient operator-norm accuracy substitution.

The source credits `SHW68` for the distinction between classical input control and quantum output memory, `Hyllus78`/`Toth78` for established block-limited metrological scaling, and `Watrous65`/`YF76` for the fidelity ingredients. The finite high-confidence learner theorem combines these ingredients with the retained complete-body learner; it makes no claim of independent human priority clearance.

Corollary `cor:blocklearnedcode78` runs the new learner at `delta/2`, then the retained exact codec at `delta/2`. The decoded error is at most `27 delta/32`, without new device calls. Payload order remains

\[
\frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
+d^2\log_2(1/\delta)+O_d(1).
\]

The training and payload converses are separate. Decoder time, storage, trusted preparation, and exact arithmetic are not charged as device calls, and the exhaustive codec is not asserted efficient.
