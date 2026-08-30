# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone paper**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `c29fb28719e72ad9a079cd4271dcb42fe76cdcc8`

## Executive assessment

D1 has been substantially rewritten. It now records the correct finite-volume normalization

\[
D^2Q_\epsilon=\mu_\epsilon\operatorname{Cov},
\]

introduces an abstract analytic–convex commutation theorem, distinguishes platform-labelled contractions, and states the constrained covariance as a Schur complement. These changes repair the most visible error of the previous version.

The new abstract theorem contains two direct mathematical errors. First, the convex dual of the normalized constrained pressure is the constrained rate **minus its constrained minimum**; the displayed commutation identity omits this normalization. Second, the proposed local likelihood ratio is not an exact mean-one density because the fluctuation field is centered at the limiting mean `DQ`, while the normalizing pressure expansion uses the finite mean `DQ_epsilon`. Local uniform convergence gives no `o(mu^{-1/2})` rate, so the mismatch may diverge. The same problem invalidates the Gaussian limit centered at the limiting mean.

Beyond these errors, hypotheses (H1)–(H4) assume essentially the whole B1–B4 program. D1 does not independently prove the hard-sphere commutations; it restates consequences that would follow if the upstream theorems existed. Since those theorems remain open in the controlling manuscripts, D1 cannot close the series.

## Improvements relative to the preceding circulation

1. The large-deviation-speed factor in the pressure Hessian is correct.
2. The conditioned covariance is stated as the correct Schur complement.
3. Cross-platform contractions are typed and require separate scaling maps.
4. Mechanical calibration is explicitly conditional on equality of likelihood cocycles.
5. The manuscript attempts to state sufficient analytic/LDP hypotheses for derivative and duality commutation.

These are useful corrections for a future summary theorem.

## Major mathematical objections

### 1. The constrained duality identity omits the normalization constant

The paper defines

\[
Q^a(\Theta)
=
\inf_\lambda\{Q(\Theta+C^*\lambda)-\lambda\cdot a\}
-
\inf_\lambda\{Q(C^*\lambda)-\lambda\cdot a\}.
\]

Thus `Q^a(0)=0`. If

\[
I(x)=Q^*(x)+Q(0)
\]

has minimum zero, the dual of `Q^a` is

\[
I^a(x)
=
\begin{cases}
I(x)-I_C(a),&Cx=a,\\
+\infty,&Cx\ne a,
\end{cases}
\]

where

\[
I_C(a)=\inf_{Cx=a}I(x).
\]

Consequently, after contraction by `T`,

\[
(Q^a\circ T^*)^*(y)
=
\inf_{Tx=y,\,Cx=a}I(x)
-
\inf_{Cx=a}I(x).
\]

Part (vi) of the commutation theorem instead writes

\[
\inf_{Tx=y,\,Cx=a}I(x)
=(Q^a\circ T^*)^*(y),
\]

omitting the constrained minimum. This is false unless `I_C(a)=0`, i.e. the constraint is typical under the base law. The entire point of the preparation theory is to allow atypical `a`, so the missing constant is essential.

### 2. The displayed “likelihood ratio” is not mean one

Let

\[
m_\Theta=DQ(\Theta),
\qquad
m_{\epsilon,\Theta}=DQ_\epsilon(\Theta).
\]

The exact Radon–Nikodym derivative from source `Theta` to `Theta+h/sqrt(mu_epsilon)` is

\[
\exp\left\{
\sqrt{\mu_\epsilon}\langle h,\mathcal X_\epsilon\rangle
-
\mu_\epsilon
[Q_\epsilon(\Theta+h/\sqrt{\mu_\epsilon})-Q_\epsilon(\Theta)]
\right\}.
\]

The paper’s `L_epsilon(h)` equals this exact density multiplied by

\[
\exp\left\{
\sqrt{\mu_\epsilon}
\langle h,m_{\epsilon,\Theta}-m_\Theta\rangle
\right\}.
\]

Therefore its expectation is not one unless the finite and limiting means coincide at the stronger rate

\[
\sqrt{\mu_\epsilon}
(m_{\epsilon,\Theta}-m_\Theta)\to0.
\]

Hypothesis (H1) supplies local uniform convergence of the pressures and hence `m_epsilon -> m`; it supplies no `o(mu^{-1/2})` rate. The factor can converge to a nonunit constant or diverge.

Thus the object called a canonical likelihood ratio is not a likelihood ratio under the stated hypotheses.

### 3. The Gaussian field is centered at the wrong mean

The paper sets

\[
Z_\epsilon
=
\sqrt{\mu_\epsilon}
(\mathcal X_\epsilon-DQ(\Theta)).
\]

Analytic convergence of `Q_epsilon` to `Q` does not imply a central limit theorem for this centering. For example, one may have a holomorphic perturbation

\[
Q_\epsilon(\Theta)=Q(\Theta)+\mu_\epsilon^{-1/4}\ell(\Theta),
\]

which converges locally uniformly with all fixed-order derivatives, while

\[
\sqrt{\mu_\epsilon}
(DQ_\epsilon-DQ)
=
\mu_\epsilon^{1/4}D\ell
\]

diverges. The characteristic-function proof then retains a divergent linear term.

The finite field must be centered at `DQ_epsilon(Theta)`, or a quantitative convergence rate must be assumed and proved. The theorem as stated is false.

### 4. Holomorphic convergence alone does not supply process Gaussianity

Even after correcting the center, the analytic Taylor argument proves Gaussian convergence only for each fixed finite family of source directions. It does not yield tightness of an infinite-dimensional path field, convergence of filtrations, or a dynamic Girsanov theorem. D1 alternates between finite-dimensional projections and path-space likelihood language without stating the additional tightness hypotheses.

### 5. The constraint minimizer is not guaranteed for every target named in the theorem

Uniform positivity of

\[
C D^2Q C^*
\]

makes the constraint map locally invertible and the finite-dimensional objective strictly convex on the source ball. It does not show that an arbitrary target `a` lies in the gradient image or that the minimizer remains inside the declared ball. Part (iii) needs an explicit compact target set contained in that image and a boundary coercivity condition.

### 6. The “independent” theorem assumes the complete upstream series

Hypotheses (H1)–(H4) include:

- complex normal convergence on a larger source neighborhood;
- a full good convex LDP;
- rate-dense exposed points;
- strict constraint covariance; and
- continuous or exponentially good contraction maps.

In the hard-sphere application these are exactly the unproved principal theorems of B1–B4. D1 proves formal consequences of those hypotheses; it does not provide an independent route to them.

### 7. The rate–pressure–semigroup triangle is conditional on B2/B4

The additive action and Lax–Oleinik semigroup are imported from B2 and B4. B2 does not prove the full actual-collision LDP, and B4’s containment/comparison framework contains direct velocity-weight errors. The diagram therefore has no established deterministic hard-sphere instance.

### 8. Cross-platform registry entries remain promises

The tagged Brownian, heat-bath, and Lorentz entries are correctly labelled as separate platforms. The manuscript then says that once their convergence maps are supplied they become instances of the theorem. This is a roadmap, not a proved contraction. It contributes no present theorem about those models.

### 9. The calibration result is tautological at the numerical-identification step

The entropic coefficient equals the mechanical field only after the paper assumes that both use the same nonconstant likelihood cocycle. Under that assumption equality is immediate. This is a valid typing statement, not a first-principles derivation of preference.

### 10. The controlling manuscript is not standalone

The active source is a preamble and one closure module. It references the B1–B4 pressure, rate, action, semigroup, and source space without defining them or reproducing exact theorem hypotheses.

## Editorial recommendation

**Reject and remove as a standalone submission.** The corrected normalization and abstract commutation framework could become a useful theorem section in a future principal paper. Before that, the constrained dual must include its normalization constant, the Gaussian field and likelihood ratio must be centered at the finite-volume mean or accompanied by a quantitative convergence rate, and all process-level conclusions must have tightness hypotheses. Most importantly, D1 cannot certify a dependency chain whose upstream theorems remain unproved.