# Representation calculus for theta-expectations: calibrated diffusions, BSDEs, PPDEs, and path evaluations

## Abstract

This paper begins after the HJB, Isaacs, belief-state, or path-dependent limit
has already been derived.  We prove that a genuinely nonlinear theta-expectation
cannot be represented by one payoff-independent linear Markov law.  For a
sufficiently regular payoff, however, the corresponding decoupling field
canonically calibrates a linear parabolic operator along its own jet.  This
yields a payoff-dependent diffusion/Feynman--Kac formula without reversing the
upstream dependency.

We then separate the available stochastic representations by PDE type.
Semilinear Markov equations yield classical FBSDEs; controlled HJB equations
yield control or randomized-BSDE representations; convex fully nonlinear
second-order equations may yield 2BSDEs; nonconvex Isaacs equations retain a
game or nonlinear martingale-problem representation; genuinely path-dependent
problems yield PPDEs and path-dependent BSDE/2BSDE branches.  Girsanov formulas
are applied only after calibration and only under the corresponding
integrability condition.  The gradient variable `p` and the BSDE integrand `Z`
are related by `Z=sigma^T Du` and are never identified directly.

---

## 1. Upstream input and dependency guardrail

The input is one of the following already established objects:

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
generator contains a nonlinear Hamiltonian or a nonlinear Hessian dependence,
(2.1) is impossible.

#### Proof

The right-hand side of (2.1) preserves arbitrary linear combinations.  Hence
the semigroup is linear.  Its generator, on a common core, is therefore linear.
A nonlinear HJB/Isaacs generator contradicts this conclusion.

### Corollary 2.2

A payoff-calibrated diffusion law, a control-selected law, or a family of laws
may represent a nonlinear theta-expectation.  None of these is a single
payoff-independent classical martingale problem for the whole semigroup.

---

## 3. Jet-calibrated linearization

Consider a terminal-value PDE

\[
\partial_tu
+F(t,x,u,Du,D^2u)=0,
\qquad u(T,x)=\phi(x).
\tag{3.1}
\]

Assume on a representation window that `F` is continuously differentiable in
`(y,p,X)` and that the solution is classical.  Define along the solution

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

and the calibrated residual

\[
r^u
=F(t,x,u,Du,D^2u)
-a^u:D^2u-b^u\cdot Du-c^uu.
\tag{3.5}
\]

### Theorem 3.1 (exact calibrated linear PDE)

The same function `u` solves

\[
\partial_tu
+a^u:D^2u+b^u\cdot Du+c^uu+r^u=0.
\tag{3.6}
\]

#### Proof

Substitute (3.5) into the left-hand side of (3.6).  It becomes exactly the
left-hand side of (3.1).

The theorem is algebraic but decisive: calibration is performed after `u` has
been derived, and all calibrated coefficients are payoff dependent through
`u`.

### Assumption 3.2 (diffusion window)

Assume

\[
a^u(t,x)\ge\lambda I
\]

and choose `sigma^u` such that

\[
\sigma^u(\sigma^u)^T=2a^u.
\tag{3.7}
\]

Assume the calibrated SDE

\[
dX_s=b^u(s,X_s)ds+\sigma^u(s,X_s)dW_s
\tag{3.8}
\]

is well posed and the exponential factors below are integrable.

### Theorem 3.3 (calibrated Feynman--Kac representation)

Under Assumption 3.2,

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

### Remark 3.4

If `a^u` is only semidefinite, one may use a well-posed degenerate martingale
problem or a vanishing elliptic regularization.  The resulting law remains
payoff calibrated.

---

## 4. The Markov semilinear FBSDE branch

Suppose (3.1) has the form

\[
\partial_tu
+\frac12\operatorname{tr}(\sigma\sigma^TD^2u)
+b\cdot Du
+f(t,x,u,\sigma^TDu)=0.
\tag{4.1}
\]

Let the forward diffusion satisfy

\[
dX_s=b(s,X_s)ds+\sigma(s,X_s)dW_s.
\tag{4.2}
\]

The backward equation is

\[
Y_s=\phi(X_T)
+\int_s^Tf(r,X_r,Y_r,Z_r)dr
-\int_s^TZ_r\,dW_r.
\tag{4.3}
\]

### Theorem 4.1 (decoupled FBSDE representation)

Under the standard Lipschitz, growth, and well-posedness conditions,

\[
Y_s=u(s,X_s),
\qquad
Z_s=\sigma(s,X_s)^TDu(s,X_s).
\tag{4.4}
\]

#### Proof

Apply Itô's formula to `u(s,X_s)` and use (4.1).  The martingale coefficient is
`σ^T Du`; uniqueness of the BSDE identifies `(Y,Z)`.

### Convention 4.2

The HJB gradient `p=Du` and the BSDE integrand `Z` have different dimensions
and meanings.  Their relation is (4.4), not `Z=p`.

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
relaxed control, or a randomized/constrained BSDE, not one fixed classical
FBSDE.

#### Proof

The DPP gives the viscosity solution of (5.1).  Conversely, verification for
smooth `u` follows from Itô's formula and the Hamiltonian inequality; equality
holds along an optimizing selector.  Approximation extends the result to the
viscosity setting under the assumed stability theorem.

The same rule applies to the one-player theta-HJB of Paper III.

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
law; the optimizing mixed strategies remain part of the representation.

---

## 7. Fully nonlinear second-order branches

Suppose `F` is nonlinear in `X`.

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
game, a nonlinear martingale problem, or a specifically proved nonconvex
second-order theory.

### Theorem 7.1 (typed second-order rule)

A fully nonlinear theta-equation enters Branch 7A only when its Hessian
Hamiltonian has the declared volatility-uncertainty representation.  Otherwise
it enters Branch 7B.  No generic `fully nonlinear -> 2BSDE` implication is
claimed.

---

## 8. Path-dependent equations and evaluations

Let `Omega` be a path space and let

\[
U(t,\omega_{[0,t]})
\]

be the value from the Paper-IV path-state DPP.  If the path cannot be reduced
to a finite-dimensional sufficient statistic, its equation is a PPDE with
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

A convex second-order path equation may admit a path-dependent 2BSDE
representation.  A nonconvex game PPDE remains a path-dependent game unless a
stronger representation theorem is proved.

### Definition 8.1 (nonlinear path evaluation)

For a terminal path payoff `Phi`, define

\[
\mathcal E_{s,t}[\Phi](\omega_{[0,s]})
=U(s,\omega_{[0,s]}).
\tag{8.2}
\]

The DPP gives time consistency under path concatenation.

---

## 9. Girsanov after calibration

Consider the calibrated diffusion (3.8).  Let `vartheta_s` be progressively
measurable and assume

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

is Brownian and the drift becomes

\[
b^u+\sigma^u\vartheta.
\tag{9.3}
\]

### Theorem 9.1 (calibrated Girsanov formula)

Every Girsanov identity obtained from (9.2)--(9.3) represents the already
calibrated payoff `u`.  It does not supply an upstream proof of the nonlinear
HJB or identify one law for all payoffs.

#### Proof

The measure change is the classical exponential-martingale argument applied to
the SDE whose coefficients were defined in Section 3.  Since those coefficients
depend on `u`, the law is downstream and payoff dependent.

---

## 10. Orientation and sign ledger

The series uses terminal-value orientation

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

If Paper III writes its diffusion coefficient as

\[
A=\frac12\Sigma,
\]

then `sigma sigma^T=Sigma`; no second factor `1/2` is inserted.

---

## 11. Applications to the θ-series

### 11.1 Paper-III nonconvex theta-expectation

The nonlinear Hamiltonian fails the single-law test in Theorem 2.1.  For a
smooth payoff, Theorem 3.3 yields a calibrated diffusion with a source term.
If the equation is semilinear on a local window, Theorem 4.1 yields an FBSDE.

### 11.2 Paper-IV mixed Isaacs value

The value is represented by the mixed relaxed game.  A classical feedback
FBSDE is obtained only when a pure or measurable mixed saddle is fixed.

### 11.3 Paper-IV belief/path branch

A finite-dimensional belief state gives a Markov representation on the
simplex.  Genuine history dependence enters Section 8 and produces the path
evaluation (8.2).

---

## 12. Main representation theorem

### Theorem 12.1 (typed representation hierarchy)

Given the theta/Isaacs/path semigroup derived in Papers III--IV:

1. every sufficiently smooth payoff admits the exact calibrated linearization
   and Feynman--Kac formula of Section 3;
2. a Markov semilinear equation admits the FBSDE representation of Section 4;
3. a control HJB admits the control/randomized representation of Section 5;
4. a game equation retains the sequential or simultaneous game type of Paper
   IV;
5. a convex volatility-uncertainty equation may use the 2BSDE branch, while a
   nonconvex second-order equation remains in the game/nonlinear-MP branch;
6. a genuine path-state problem admits the PPDE/path-evaluation branch;
7. Girsanov transformations are valid only after one of the preceding laws has
   been fixed and the exponential integrability condition holds.

No conclusion in this theorem is used to prove an upstream HJB limit.

---

## 13. Conclusion

A nonlinear expectation has many legitimate stochastic representations but no
universal payoff-independent linear law.  The correct organization is a typed
hierarchy determined by the PDE and DPP structure.  Calibration supplies a
common downstream calculus while preserving the causal separation between
deterministic microscopic derivation and stochastic representation.
