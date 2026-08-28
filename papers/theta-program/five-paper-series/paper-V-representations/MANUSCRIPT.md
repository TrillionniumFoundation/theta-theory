# Representation calculus for theta-expectations: calibrated diffusions, BSDEs, PPDEs, and path evaluations

## Abstract

This paper begins after the HJB, Isaacs, belief-state, or path-dependent limit
has already been derived.  We prove that a genuinely nonlinear theta-expectation
cannot be represented by one payoff-independent linear Markov law.  For a
sufficiently regular payoff, however, the corresponding decoupling field
canonically calibrates a linear parabolic operator along its own jet.  This
yields a payoff-dependent diffusion/Feynman--Kac formula without reversing the
upstream dependency.

We separate the available stochastic representations by PDE type.  Semilinear
Markov equations yield classical FBSDEs; controlled HJB equations yield control
or randomized-BSDE representations; convex fully nonlinear second-order
equations may yield 2BSDEs; nonconvex Isaacs equations retain a game or
nonlinear martingale-problem representation; genuinely path-dependent problems
yield PPDEs and path-dependent BSDE/2BSDE branches.  Girsanov formulas are
applied only after calibration and only under the corresponding integrability
condition.  The gradient variable `p` and the BSDE integrand `Z` are related by
`Z=sigma^T Du` and are never identified directly.

---

## 1. Upstream input and dependency guardrail

The input is one of:

1. a Markov HJB/theta semigroup from Paper III;
2. a sequential or simultaneous Isaacs semigroup from Paper IV;
3. a belief-state HJB semigroup from Paper IV;
4. a path-dependent value functional with a DPP from Paper IV.

This paper does not prove CM2, U3, pressure response, rough WIP,
homogenization, filtering, the DPP, or viscosity comparison.

Let

\[
\mathcal E_{s,t}[\phi]
\]

denote the resulting nonlinear evaluation.

---

## 2. The single-law obstruction

### Theorem 2.1 (no payoff-independent linear law)

Suppose that for every bounded continuous payoff `phi` there is one and the
same Markov transition law `P_{s,t}(x,dy)`, independent of `phi`, such that

\[
\mathcal E_{s,t}[\phi](x)
=
\int\phi(y)P_{s,t}(x,dy).
\tag{2.1}
\]

Then `mathcal E_{s,t}` is linear in `phi`.  In particular, if the infinitesimal
generator contains a nonlinear Hamiltonian or nonlinear Hessian dependence,
(2.1) is impossible.

#### Proof

The right-hand side preserves arbitrary linear combinations.  Hence the
semigroup and its generator on a common core are linear, contradicting a
genuinely nonlinear HJB/Isaacs generator.

### Corollary 2.2

A payoff-calibrated law, a control-selected law, or a family of laws may
represent a nonlinear theta-expectation.  None is a single payoff-independent
classical martingale problem for the whole semigroup.

---

## 3. Jet-calibrated linearization

### Convention 3.1 (generator orientation)

We write the terminal PDE as

\[
\partial_tu+F(t,x,u,Du,D^2u)=0,
\qquad u(T,x)=\phi(x),
\tag{3.1}
\]

in **generator orientation**: where differentiable, `F_X` is positive
semidefinite.  If an upstream paper uses a convention with a negative diffusion
term, it is first rewritten in generator orientation before the formulas below
are applied.

Assume on a representation window that `F` is continuously differentiable in
`(y,p,X)` and the solution is classical.  Define along the solution

\[
a^u=F_X(t,x,u,Du,D^2u),
\tag{3.2}
\]

\[
b^u=F_p(t,x,u,Du,D^2u),
\tag{3.3}
\]

\[
c^u=F_y(t,x,u,Du,D^2u),
\tag{3.4}
\]

and

\[
r^u
=F(t,x,u,Du,D^2u)
-a^u:D^2u-b^u\cdot Du-c^uu.
\tag{3.5}
\]

### Theorem 3.2 (exact calibrated linear PDE)

The same `u` solves

\[
\partial_tu
+a^u:D^2u+b^u\cdot Du+c^uu+r^u=0.
\tag{3.6}
\]

#### Proof

Substitute (3.5) into (3.6); its left-hand side becomes that of (3.1).
Calibration is exact and occurs after `u` has been derived.

### Assumption 3.3 (diffusion window)

Assume

\[
a^u(t,x)\ge\lambda I
\]

and choose `sigma^u` such that

\[
\sigma^u(\sigma^u)^T=2a^u.
\tag{3.7}
\]

Assume

\[
dX_s=b^u(s,X_s)ds+\sigma^u(s,X_s)dW_s
\tag{3.8}
\]

is well posed and the exponential factors below are integrable.

### Theorem 3.4 (calibrated Feynman--Kac representation)

Under Assumption 3.3,

\[
\boxed{
\begin{aligned}
u(t,x)=\mathbb E_{t,x}\Big[&
 e^{\int_t^T c^u(r,X_r)dr}\phi(X_T)\\
&+\int_t^T
 e^{\int_t^s c^u(r,X_r)dr}
 r^u(s,X_s)ds
\Big].
\end{aligned}
}
\tag{3.9}
\]

#### Proof

Apply Itô's formula to

\[
e^{\int_t^s c^u(r,X_r)dr}u(s,X_s).
\]

Equation (3.6) leaves drift `-e^{int c}r^u ds`.  Integrate to `T`, take
expectations, and rearrange.

### Remark 3.5

If `a^u` is only semidefinite, use a well-posed degenerate martingale problem or
a vanishing elliptic regularization.  The law remains payoff calibrated.

---

## 4. The Markov semilinear FBSDE branch

Suppose

\[
\partial_tu
+\frac12\operatorname{tr}(\sigma\sigma^TD^2u)
+b\cdot Du
+f(t,x,u,\sigma^TDu)=0.
\tag{4.1}
\]

Let

\[
dX_s=b(s,X_s)ds+\sigma(s,X_s)dW_s
\tag{4.2}
\]

and

\[
Y_s=\phi(X_T)
+\int_s^Tf(r,X_r,Y_r,Z_r)dr
-\int_s^TZ_r\,dW_r.
\tag{4.3}
\]

### Theorem 4.1 (decoupled FBSDE representation)

Under the declared Lipschitz, growth, and well-posedness conditions,

\[
Y_s=u(s,X_s),
\qquad
Z_s=\sigma(s,X_s)^TDu(s,X_s).
\tag{4.4}
\]

#### Proof

Apply Itô's formula to `u(s,X_s)` and use (4.1).  The martingale coefficient is
`σ^T Du`; uniqueness identifies `(Y,Z)`.

### Convention 4.2

The HJB gradient `p=Du` and BSDE integrand `Z` have different dimensions and
meanings.  Their relation is (4.4), not `Z=p`.

---

## 5. Controlled HJB and randomized/control BSDEs

Consider

\[
\partial_tu+\sup_{\alpha\in A}
\left\{
\frac12\operatorname{tr}(a^\alpha D^2u)
+b^\alpha\cdot Du+f^\alpha(t,x,u)
\right\}=0.
\tag{5.1}
\]

### Theorem 5.1 (control representation)

Under compactness, measurable selection, tightness, and comparison, `u` equals
the value over admissible controlled diffusions.  If an optimal feedback
`alpha^u(t,x)` exists, substituting it gives a payoff-dependent classical BSDE.
Without such a feedback, the correct representation is a control family,
relaxed control, or randomized/constrained BSDE, not one fixed FBSDE.

#### Proof

The DPP gives the viscosity solution.  For smooth `u`, Itô's formula and the
Hamiltonian inequality yield verification; equality holds along an optimizer.
Approximation extends the result under the assumed stability theorem.

---

## 6. Isaacs equations

For a sequential or simultaneous game, the generator contains

\[
\sup_u\inf_vF^{u,v}
\quad\text{or}\quad
\inf_v\sup_uF^{u,v}.
\]

### Theorem 6.1 (game representation)

The Paper-IV sequential equations are represented by their corresponding
nonanticipative lower and upper games.  The simultaneous relaxed equation is
represented by the mixed game.  A pure feedback FBSDE representation is
available only after the Paper-IV pure-saddle gate has been verified.

A mixed Isaacs equality does not turn the game into a payoff-independent single
law; optimizing mixed strategies remain part of the representation.

---

## 7. Fully nonlinear second-order branches

### Branch 7A (convex volatility uncertainty)

If

\[
F(t,x,y,p,X)
=
\sup_{a\in\mathcal A(t,x)}
\left\{
\frac12a:X+f(t,x,y,p,a)
\right\}
\tag{7.1}
\]

with a stable nondominated volatility class and the required aggregation,
comparison, and minimality conditions, the equation admits a 2BSDE or
nonlinear-expectation representation.

### Branch 7B (nonconvex second-order Isaacs)

If the Hessian dependence is a nonconvex sup--inf game, a standard convex
2BSDE theorem does not apply.  The correct representation remains a stochastic
game, nonlinear martingale problem, or a specifically proved nonconvex
second-order theory.

### Theorem 7.1 (typed second-order rule)

A fully nonlinear theta-equation enters Branch 7A only when its Hessian
Hamiltonian has the declared volatility-uncertainty representation.  Otherwise
it enters Branch 7B.  No generic `fully nonlinear -> 2BSDE` implication is
claimed.

---

## 8. Path-dependent equations and evaluations

Let

\[
U(t,\omega_{[0,t]})
\]

be the Paper-IV path-state value.  If the path cannot be reduced to a
finite-dimensional sufficient statistic, its equation is a PPDE with
horizontal and vertical derivatives.

### Branch 8A (semilinear PPDE)

For

\[
\partial_t^{H}U
+\frac12\operatorname{tr}(\sigma\sigma^T
\partial_{\omega\omega}^2U)
+b\cdot\partial_\omega U
+f(t,\omega,U,\sigma^T\partial_\omega U)=0,
\tag{8.1}
\]

a functional Itô formula gives a path-dependent BSDE representation under the
corresponding regularity or viscosity framework.

### Branch 8B (fully nonlinear PPDE)

A convex second-order path equation may admit a path-dependent 2BSDE.  A
nonconvex game PPDE remains a path-dependent game unless a stronger theorem is
proved.

### Definition 8.1 (nonlinear path evaluation)

For terminal path payoff `Phi`, define

\[
\mathcal E_{s,t}[\Phi](\omega_{[0,s]})
=U(s,\omega_{[0,s]}).
\tag{8.2}
\]

The DPP gives time consistency under concatenation.

---

## 9. Girsanov after calibration

Let `vartheta_s` be progressively measurable and assume

\[
\mathbb E\exp\left(
\frac12\int_t^T|\vartheta_s|^2ds
\right)<\infty.
\tag{9.1}
\]

Define

\[
\mathcal Z_T
=
\exp\left(
\int_t^T\vartheta_s\,dW_s
-
\frac12\int_t^T|\vartheta_s|^2ds
\right).
\tag{9.2}
\]

Under `dQ=Z_T dP`,

\[
W_s^Q=W_s-\int_t^s\vartheta_rdr
\]

is Brownian and the drift in (3.8) becomes

\[
b^u+\sigma^u\vartheta.
\tag{9.3}
\]

### Theorem 9.1 (calibrated Girsanov formula)

Every identity obtained from (9.2)--(9.3) represents the already calibrated
payoff `u`.  It does not prove the nonlinear HJB or identify one law for all
payoffs.

---

## 10. Orientation and factor ledger

The terminal-value orientation is

\[
\partial_tu+F=0,
\qquad u(T)=\phi.
\]

The associated BSDE is

\[
Y_s=\phi(X_T)+\int_s^Tf_rdr-\int_s^TZ_rdW_r.
\]

The diffusion convention is

\[
\frac12\sigma\sigma^T:D^2u.
\]

Paper III writes `A=Sigma/2`, so

\[
\sigma\sigma^T=\Sigma.
\]

No additional factor `1/2` is inserted.

---

## 11. Applications to the θ-series

1. The Paper-III nonconvex theta-expectation fails the single-law test.  A
   smooth payoff admits the calibrated formula of Section 3, and a semilinear
   local window admits Section 4.
2. The Paper-IV mixed Isaacs value is represented by its mixed game.  A
   classical feedback BSDE requires a verified saddle.
3. A finite-dimensional belief gives a Markov representation on the simplex;
   genuine history dependence enters the PPDE branch.

---

## 12. Main representation theorem

### Theorem 12.1 (typed representation hierarchy)

Given the theta/Isaacs/path semigroup derived in Papers III--IV:

1. every sufficiently smooth payoff admits the exact calibrated linearization
   and Feynman--Kac formula of Section 3;
2. a Markov semilinear equation admits the FBSDE representation of Section 4;
3. a control HJB admits the control/randomized representation of Section 5;
4. a game equation retains the sequential or simultaneous type of Paper IV;
5. a convex volatility-uncertainty equation may use the 2BSDE branch, while a
   nonconvex second-order equation remains in the game/nonlinear-MP branch;
6. a genuine path-state problem admits the PPDE/path-evaluation branch;
7. Girsanov transformations are valid only after one preceding law has been
   fixed and exponential integrability holds.

No conclusion here is used to prove an upstream HJB limit.

---

## 13. Conclusion

A nonlinear expectation has many legitimate stochastic representations but no
universal payoff-independent linear law.  The correct organization is a typed
hierarchy determined by the PDE and DPP structure.  Calibration supplies a
common downstream calculus while preserving the causal separation between
deterministic microscopic derivation and stochastic representation.
