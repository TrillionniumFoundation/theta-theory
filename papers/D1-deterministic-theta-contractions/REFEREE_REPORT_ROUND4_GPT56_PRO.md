# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `5f107627fd9b99bdc9b2e33c619ee8f2130cf49c`

## Overall assessment

The revision correctly repairs the two elementary errors identified in the preceding report: the exact Hessian is now `mu_epsilon` times covariance, and the local likelihood ratio is centered at the finite-volume mean `DQ_epsilon`, making it an exact mean-one density. The constrained dual also now includes the necessary subtraction of the constrained minimum.

The new “analytic--convex commutation theorem” is nevertheless false or underdetermined under its stated hypotheses. It assumes pressure convergence only on a local source ball but identifies a global convex dual over the entire Banach space. It also assumes a full LDP plus rate-dense exposed points—essentially the most difficult conclusion—and then presents standard consequences as an independent theorem. Its process-level likelihood statements remain conditional on the invalid B3 and C2 interfaces. The paper adds no standalone top-four contribution.

## Major objections

### 1. A local pressure does not determine the global rate by a supremum over all sources

Hypothesis H1 gives holomorphic convergence of `Q_epsilon` only on a complex neighborhood of a real ball

\[
B\Subset X.
\]

The theorem then states

\[
I(x)=\sup_{\Theta\in X}
\{\langle\Theta,x\rangle-Q(\Theta)+Q(0)\}.
\]

But `Q(Theta)` has not been defined or proved finite outside `B`. A local analytic cumulant determines only a local support function/exposed branch. It cannot recover the full good rate on `X^*`.

A full LDP does not automatically imply the Laplace principle for unbounded linear sources in all of `X`; exponential integrability is required. The theorem must either assume a globally defined proper lower-semicontinuous pressure on a separating dual space or restrict every dual formula to the proven pressure domain and accept only the corresponding convex envelope.

As written, part (ii) is not a consequence of H1--H4.

### 2. H2 assumes the central hard theorem

H2 assumes:

- a full LDP with a good convex rate; and
- rate-preserving approximation of every finite-rate point by exposed points of the pressure.

This is essentially the global lower-bound and dual-identification theorem which A3/B2 struggle to prove. Once H2 and a global Laplace principle are assumed, much of D1 is standard convex analysis.

Thus D1 does not close the microscopic programme; it repackages its desired output as an abstract hypothesis.

### 3. The proof of rate duality still has a gap

The text says the full LDP gives the Laplace upper bound and lower bound at exposed points, after which the exposed approximation proves the global dual. For an unbounded linear functional `Theta`, Varadhan's lemma requires exponential-tail control. H2 supplies rate approximation, not uniform integrability of `exp(mu<Theta,X_epsilon>)`.

Therefore even with exposed density, the equality between the good LDP rate and the conjugate of `Q` does not follow on the full source space.

### 4. The constrained saddle theorem needs finite-volume control for conditioning

The limiting constrained pressure formula is a standard analytic consequence of a positive limiting Hessian. To claim it represents the microscopic conditional law, one additionally needs the finite-volume coefficient/local-limit theorem proved in B1. H1--H4 do not contain such a condition.

D1's abstract theorem therefore conflates analytic minimization of the limiting pressure with actual conditioning of the prelimit measures. Source-dependent conditioning is not a consequence of the listed commutation hypotheses alone.

### 5. The contracted constrained dual requires a no-gap theorem on the full domain

The identity

\[
((Q^a\circ T^*)^*)(y)
=
\inf_{Tx=y,Cx=a}I(x)-\inf_{Cx=a}I(x)
\]

is valid under appropriate closed convex duality and domain qualifications. With only a local pressure ball and an l.s.c. extension, the conjugate of the restricted pressure may be strictly smaller/larger than the intended constrained rate envelope. The proof invokes “joint affine duality” without verifying closedness, coercivity, or absence of a duality gap.

### 6. The exact local likelihood theorem is correct only in finite-dimensional projections

The finite-dimensional expansion at

\[
\Theta+h/\sqrt{\mu_\varepsilon}
\]

is now correctly centered and normalized. Local holomorphic convergence yields Gaussian convergence for each fixed finite family of sources.

It does not by itself produce an `X^*`-valued Gaussian random element. Tightness in an infinite-dimensional dual space requires nuclearity, compact embeddings, or uniform covariance-tail estimates. The theorem appropriately adds B3 tightness as an extra condition for process convergence, but that condition is not established by B3.

The standalone conclusion must therefore remain finite-dimensional and conditional.

### 7. Uniform integrability needs a quantitatively larger source domain

The proof obtains an `L^{1+eta}` bound from a “slightly larger real source ball.” This requires

\[
\Theta+(1+\eta)h/\sqrt{\mu_\varepsilon}
\]

to stay in a domain on which the finite pressures are uniformly bounded, and it must be uniform in `epsilon`. This is plausible for fixed `h` on a compact interior ball, but it should be stated quantitatively. It does not give uniform integrability for an infinite collection of directions or a process likelihood without further bounds.

### 8. The rate--pressure--semigroup triangle imports every unresolved theorem

The first row is B2/B3, the variational semigroup is B4, and the Girsanov conclusion is C2. Those papers remain unproved. The diagram is therefore a conditional summary, not a new result.

The assertion that “dynamic additivity of `I` is equivalent to the nonlinear tower of `S`” also needs qualifications: additive action gives the tower for the variational semigroup, but a semigroup can have many representations and tower alone does not identify a unique additive rate.

### 9. The contraction registry is a scope statement, not a theorem

The platform labels correctly prevent false deletion/freezing arguments. Entries such as tagged Brownian motion and heat-bath rays are explicitly conditional on separate scaling theorems. This is honest bookkeeping, but it contributes no new mathematics.

### 10. The calibration theorem remains conditional on equality of cocycles

Entropic rigidity plus equality of the valuation and mechanical likelihood cocycles forces equality of coefficients. This is correct under the assumptions and has already appeared in A1/C2/B4. Repetition in D1 does not create an independent theorem.

### 11. The hard-sphere application does not satisfy the abstract hypotheses

The manuscript says H1--H4 are supplied by B1--B4. In fact:

- B2 has not proved its full LDP or global source pressure;
- B1 has not proved the finite shell coefficient;
- B3 has not proved its covariance-nullspace or process tightness theorem; and
- B4 has not constructed the claimed HJ semigroup/comparison on compatible spaces.

Thus the final “Round-four D1 closure” cannot be applied to the series.

## Status of previous objections

The normalization and finite-centering errors have been genuinely fixed. The current rejection is not based on those old formulas. It is based on the local/global duality gap, assumption of the full microscopic theorem in H2, and lack of independent mathematical content.

## Appropriate disposition

D1 should not be maintained as a standalone manuscript. A corrected finite-dimensional analytic lemma could be included in a future principal hard-sphere paper:

- Cauchy convergence of derivatives on a complex chart;
- finite-volume `mu Cov` normalization;
- local constrained Schur complement; and
- exact local likelihood expansion.

Global LDP duality, conditioning, semigroup convergence, and process likelihoods should appear only after their model-specific proofs and with their precise domains.

## Recommendation

**Reject; remove as a standalone submission.** The revision corrects its elementary formulas, but the new theorem assumes the central LDP/exposed-density result, uses a local pressure as though it were global, and adds no independent top-four-level contribution.