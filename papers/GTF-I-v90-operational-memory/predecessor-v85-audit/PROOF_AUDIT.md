# Proof and resource audit — Revision 85

This is an author-side verification of a written mathematical argument, not an independent human priority opinion or a proof-assistant certificate. The immutable R54 reports and all earlier mathematical sections remain unchanged. The new proof graph is in Sections 72–74.

## 1. Finite Bernoulli premise in the primary

For `h=|p-q|`, the new lemma proves an absolute unhalved product-law lower `(1/128)min(1,sqrt(N)h)` for every `p,q in [0,1]`. On `m` copies use the bounded complex statistic `exp(i m^(-1/2) sum X_r)`. For `z(a)=1-a+a exp(iu)`, `u=m^(-1/2)`, its expectation is `z(a)^m`. The lower modulus is at least `sqrt(3/4)>3/4`, and the argument derivative is between `u/2` and `4u/3`. When `sqrt(m)h<=1/4`, angular separation bounds the expectation difference below by `sqrt(m)h/16`. If `h<=1/4` but the full record is longer, `m=floor(1/(16h²))` is positive and no larger than `N`, and gives a uniform constant lower. For `h>1/4` the first observation suffices. Discarding unused observations is common postprocessing. The proof covers endpoints, not just an interior asymptotic expansion.

The local probability curve used for a moving two-sided measurement tangent has a nonzero derivative at zero. Such a probability cannot equal zero or one there. This explanation is stated even though the new finite estimate itself is uniform through the endpoints. The primary's support and discrimination results no longer need to reconstruct a historical binary lemma to justify this step.

## 2. Every two-sided first-order direction

Let `P_j=supp(E_j)`, `Q_j=I-P_j`. For each vector in `Q_j`, positivity along both signs of the curve gives a scalar local minimum at zero. Polarization yields `Q_j H_j Q_j=0`. Normalization gives `sum H_j=0`. These are necessary first-order constraints even if ranks change at second order.

They are sufficient: set `A_j=sqrt(E_j)` and `B_j=(sqrt(E_j))^+ H_j(I-P_j/2)`, using only the inverse on the fixed support. Then `A_j*B_j+B_j*A_j=H_j` and the stacked `A*B` is anti-Hermitian. Consequently `(A+tB)(I+t²B*B)^(-1/2)` is real analytic and normalized near zero, with derivative `B`. The induced effects have the requested value and first derivative. This constructs *a* curve, not a differentiable exact factorization of the given curve. The existence proof uses real/algebraic square roots; the rational certificate itself does not need them.

The forward reference from the first-order lemma to this construction is not circular: the construction uses only the displayed missing-block condition, support inverse, and normalization. It does not use the classification or its lower bound.

## 3. Support generator and covariance range

All spaces are real Hermitian Hilbert spaces, and `Gamma=(i/2)sum[P_j,H_j]` is Hermitian. Pairing `H` with the complete v84 kernel parameterization removes the tuple mean and all missing-support `Z_j` blocks. Cyclic trace gives exactly `-2tr(A Gamma)` for the remaining parameter `A in W_E^perp`. Self-adjoint finite-dimensional covariance then yields `H in Ran(C_E)` if and only if `Gamma in W_E`.

For a unitary tangent, `Gamma=G-(1/2)sum(E_j G P_j+P_j G E_j)`. The second term is in the real support span, so the new criterion specializes exactly to the v84 criterion. A stationary unitary generator belongs to `W_E`. This conclusion is not extended to a zero first derivative of an arbitrary curve.

## 4. Horizontal surrogate, not a rank-regularity assumption

For `H in Ran(C_E)`, the retained factorization `C_E=T_A(I-AA*)T_A*/4` gives `B=(I-AA*)T_A*C_E^dagger H/4`. Then `A*B=0`, `T_AB=H` and `4||B||HS²=<H,C_E^dagger H>`. For `S=B*B`, direct ordered multiplication gives

```
A(t)=(A+tB)(I+t²S)^(-1/2),
A(t)*A'(t)=0,
A'(t)=(B-tAS)(I+t²S)^(-3/2),
A'(t)*A'(t)=S(I+t²S)^(-2).
```

No noncommuting factors are exchanged. With `b=||B||op` and `|t|b<=1`, the second derivative is bounded by `7b²`. Duplication of the classical label into a discarded environment preserves those isometry derivative norms. A common purified adaptive tester has orthogonal differentiated-slot summands because `W*W'=0`, giving the unhalved path bound `2b sqrt(N)|t|`.

For a Hermitian tuple `R`, the measurement derivative has diamond norm at most `sum ||R_j||op`, by duality on each subnormalized reference block. The actual curve has second derivative bounded by `L=sum sup ||E_j''||op` in the form specified in the theorem. The surrogate channel has second derivative at most `2||W''||+2||W'||²<=16b²`. Taylor with common value and first derivative gives a channel error at most `(L+16b²)t²/2`. Hybrid telescoping over `N` calls therefore gives a *finite* `2b sqrt(N)|t|+(L+16b²)Nt²/2` bound.

For `x=sqrt(N)|t|<=1`, `x²<=x`; for `x>=1` cap by two. This proves the square-root upper uniformly in `N` on a fixed interval despite support changes. The product Bernoulli lemma and one nonzero component expectation prove the matching lower. Public stopping is padded with discarded dummy outputs; the original stopped record is a common postprocessing.

## 5. Corrected derivative of a general curve

For a tangent outside the covariance range, use the v84 support-complement code for `Gamma`. Write `Z=Gamma-Pi_W Gamma`, `s=tr Z_+`, and `Delta=||Z||HS²/s`. Since `I in W`, `Z` is traceless, `s>0` and `Delta>0`. The reference dimension and complete CPTP recovery are inherited from the actual-label support-code proof; no discarded input or inaccessible environment is supplied to the recovery.

The normalized first-order factors from Section 2 satisfy `sum A_j* B_j=-i Gamma`. If `R_l L_mu J=c_lmu I` are the exact correction identities, then recovery completeness gives

```
sum_l,mu conjugate(c_lmu) R_l dot L_mu J
 = J* sum_mu L_mu* dot L_mu J
 = -i Gamma_L.
```

The adjoint term proves `Phi'_0=-i[Gamma_L,.]`. This differentiation uses only a surrogate sharing the same first jet: the actual effect curve may have nondifferentiable canonical square roots. The actual corrected channel's second derivative is at most `L`; the ideal logical unitary's at most `4||Gamma||op²`. Thus `||Phi_t-U_t||diamond<=kappa t²` with `kappa=L/2+2||Gamma||op²`.

Telescoping `m` channels costs at most `m kappa t²`, without any independence assumption. Starting from equal logical amplitudes gives the actual finite lower `(2|sin(mtDelta/2)|-m kappa t²)_+`. On `|t|<=min(a0,1/(2Delta),Delta/(2pi kappa))`, set `m=min(N,floor(1/(|t|Delta)))`. The floor is at least two before taking the minimum with `N`; `x=m|t|Delta` lies between half the truncated scale and one. The sine lower is `2x/pi`, and the Taylor loss no more than `x/(2pi)`. The ordinary hybrid upper uses the finite first-derivative bound of the given curve. These prove the linear branch. All constants are curve dependent.

## 6. Rank changes and exclusions

The explicit curve `(1-t²)U_t P U_t*+t² I/2`, with its complement and a noncommuting Pauli generator, has eigenvalues `t²/2` and `1-t²/2`. It is projective at zero and full rank elsewhere, but has a nonzero outside-range first jet and the linear finite-use rate. This example is not a fixed unitary orbit.

The scalar curve `(t²,1-t²)` has zero first derivative and exact distance `2[1-(1-t²)^N]`. It is deliberately excluded from the nonzero-first-jet theorem and prevents an incorrect stationarity inference. One-sided curves may have nonzero missing-support first-order blocks and are also outside that theorem. Neither example supplies arbitrary-pair midpoint equivalence, full-boundary entropy, or a uniform stratum theorem.

## 7. Certified control stability

Choose the ideal Helstrom readout for the logical unrotated and ideal rotated states. The curvature loss is paid once, on the rotated hypothesis. Under each hypothesis the implemented output differs from the ideal corrected output by at most `e0+ef+sum nu_r`; triangle comparison pays this twice. This gives the exact ledger in Theorem `thm:controlstability85`.

Encoding and recovery errors can be added to bound a cycle's uniform diamond error by contraction through the unknown measurement. Preparation and final measurement are separate. With `x=m|t|Delta`, `z=min(1,N|t|Delta)`, the sufficient budgets give initial/final error at most `x/(8pi)` and accumulated cycle error at most `x/(8pi)`. Twice their sum costs `x/(2pi)`, leaving at least `x/pi>=z/(2pi)`. These are deterministic worst-case channel errors valid with references, not average calibration errors. Fixed errors independent of angle generally do not satisfy the required scale as `t` tends to zero. There is no claim that a circuit meeting them was synthesized or executed.

## 8. Exact decision and finite regressions

`curve_geometry.py` validates legal Gaussian-rational effects, a Hermitian zero-sum tangent, and every missing-support block. It computes `Gamma`, exact real support-span rank, and the Hilbert–Schmidt Gram projection using the inherited rational support implementation. It reports a zero tangent as `higher_order_undetermined`. Rational rank and elimination have the previously proved polynomial represented-input bit bounds. No curvature constant, optimal tester, recovery circuit or adaptive distance is computed.

The suite has 313 positive checks and 17 rejection controls, including 150 exact finite Bernoulli comparisons and 20 unitary specializations. It verifies nonunitary normalized first jets, every complete-kernel pairing, rank-opening rational curves, horizontal factor derivative identities, a flagged logical derivative, control-budget arithmetic, zero-tangent semantics, malformed inputs and replay mutations. Both ordinary and optimized Python execute the same checks. These are regression tests, not a proof of the continuum statements. All 22 prior suites remain active and execute anew.

## 9. Dependency and preservation boundaries

The new curve proof uses the retained covariance factorization (Section 67), the complete kernel (69), and the support-complement code/recovery proof (70), plus the new main-text Bernoulli lemma (72). It does not use the orbit theorem as a black box, the noisy-projector corollary, a common unknown-device learner, or the structural article. Balanced learning retains its precise linked supplement dependencies.

All old mathematical sections are byte-identical and active in the corresponding edition. The full prior native corpus is included; altered entry/audit/build files are preserved verbatim under `predecessor-v84-audit/`. The current bibliography and introduction supersede historical availability statements without rewriting their archived originals. New native/publication/final receipts must be produced for this source. Neither source hashes nor regression evidence establish priority or a human signature. The independent A/B/C/D aggregate flags stay false.
