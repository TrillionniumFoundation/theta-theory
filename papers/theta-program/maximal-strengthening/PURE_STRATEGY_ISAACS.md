# Pure-strategy Isaacs: exact criterion, no-go, and actual saddle class

## 0. Resolution

A general pure-strategy saddle theorem is false.  The correct closure consists
of:

1. an exact compact-action equivalence between pure Isaacs equality and a pure
   saddle;
2. a measurable-selector theorem;
3. a robust strong concave--convex class with a unique smooth saddle;
4. an actual four-branch control/game realization;
5. a matching-pennies counterexample excluding any stronger unconditional
   theorem.

The main export is

```text
P4-PURE-ISAACS-MAXIMAL.
```

---

## 1. Pure lower and upper Hamiltonians

Let `Z` be the state/jet space and let `U,V` be compact metric action spaces.
For a continuous payoff

\[
F:Z\times U\times V\to\mathbb R,
\]

the maximizing player chooses `u` and the minimizing player chooses `v`.
Define

\[
H^-(z)=\max_{u\in U}\min_{v\in V}F(z,u,v),
\tag{1.1}
\]

\[
H^+(z)=\min_{v\in V}\max_{u\in U}F(z,u,v).
\tag{1.2}
\]

Always `H^-<=H^+`.

A pair `(u_*,v_*)` is a pure saddle at `z` when

\[
F(z,u,v_*)
\le F(z,u_*,v_*)
\le F(z,u_*,v)
\tag{1.3}
\]

for every `u,v`.

---

## 2. Exact equivalence

### Theorem 2.1 (pure Isaacs iff pure saddle)

For compact `U,V` and continuous `F(z,.,.)`, the following are equivalent for
each fixed `z`:

1. `H^-(z)=H^+(z)`;
2. a pure saddle exists.

#### Proof

A saddle immediately gives equality.  Conversely choose

\[
u_\star\in\arg\max_u\min_vF(z,u,v),
\]

\[
v_\star\in\arg\min_v\max_uF(z,u,v).
\]

Compactness gives existence.  If the common value is `c`, then

\[
F(z,u_\star,v)\ge c\quad\forall v,
\]

and

\[
F(z,u,v_\star)\le c\quad\forall u.
\]

At `(u_star,v_star)` the first inequality gives `F>=c` and the second gives
`F<=c`, so equality holds and (1.3) follows.

### Corollary 2.2

Mixed relaxed Isaacs equality does not imply a pure saddle.  It only proves
equality after convexifying the actions.  A pure theorem must prove the pure
equality (1.1)--(1.2) or provide a saddle directly.

---

## 3. General no-go

Take `U=V={-1,1}` and

\[
F(u,v)=uv.
\tag{3.1}
\]

Then

\[
H^-=-1,
\qquad
H^+=1,
\]

while the relaxed mixed value is zero.  No pure saddle exists.

### Theorem 3.1 (unrestricted pure-saddle no-go)

Compactness, continuity, ellipticity of the state equation, DPP, and mixed
minimax do not imply a pure saddle.  Any general theorem omitting a pure
Isaacs or equivalent structural condition is false.

---

## 4. Measurable saddle selectors

Let `Z` be Polish.  Assume `F` is Borel in `z` and continuous in `(u,v)`.
Define the saddle correspondence

\[
\mathcal S(z)=\left\{(u,v):
F(z,u',v)\le F(z,u,v)\le F(z,u,v')
\ \forall u',v'\right\}.
\tag{4.1}
\]

### Theorem 4.1 (measurable pure selector)

If `S(z)` is nonempty for every `z`, then it has a Borel measurable selector

\[
z\mapsto(u_*(z),v_*(z)).
\tag{4.2}
\]

#### Proof

Continuity in actions makes each `S(z)` compact.  The inequalities in (4.1),
checked on countable dense subsets of `U,V`, show that the graph of `S` is
Borel.  The Kuratowski--Ryll-Nardzewski selection theorem gives (4.2).

Thus pure Isaacs equality pointwise, plus compact Caratheodory data, is enough
to construct admissible Markov selectors.

---

## 5. Strong concave--convex theorem

Assume now `U subset R^m` and `V subset R^n` are compact convex.  Suppose
`F(z,.,.)` is `C^2` and, uniformly in `z`,

\[
D_{uu}^2F(z,u,v)\le-\lambda_uI,
\qquad
D_{vv}^2F(z,u,v)\ge\lambda_vI
\tag{5.1}
\]

for positive `lambda_u,lambda_v`.

### Theorem 5.1 (unique pure saddle)

Under (5.1), each `z` has a unique pure saddle.  Hence `H^-=H^+` in pure
strategies.  If the saddle is interior and `F` is `C^k` in all variables, the
selector is `C^{k-1}` in `z`.

#### Proof

Strong concavity and convexity imply the convex--concave minimax equality and
uniqueness of the maximizing/minimizing components.  Equivalently define

\[
\mathcal G_z(u,v)=(-D_uF(z,u,v),D_vF(z,u,v)).
\tag{5.2}
\]

For two points `w=(u,v)`, `w'=(u',v')`, symmetry of mixed derivatives makes
the mixed terms cancel in the symmetric part of `D G`.  Hence

\[
\langle\mathcal G_z(w)-\mathcal G_z(w'),w-w'\rangle
\ge
\min(\lambda_u,\lambda_v)|w-w'|^2.
\tag{5.3}
\]

The associated variational inequality has a unique solution, which is the
saddle.  At an interior solution the Jacobian of `G` is invertible by strong
monotonicity, so the implicit function theorem gives the parameter regularity.

### Remark 5.2

No small cross-Hessian assumption is needed.  Cross derivatives cancel in the
monotonicity calculation; they affect the location of the saddle, not its
existence.

---

## 6. Robust finite-action alternative

For finite `U,V`, assume there is `(u_*,v_*)` and `delta>0` such that

\[
F(z,u,v_*)
\le F(z,u_*,v_*)-\delta
\quad(u\ne u_*),
\tag{6.1}
\]

\[
F(z,u_*,v)
\ge F(z,u_*,v_*)+\delta
\quad(v\ne v_*).
\tag{6.2}
\]

Then `(u_*,v_*)` is the unique pure saddle and remains so under any uniform
perturbation smaller than `delta/3`.  This is the correct packet for a robust
finite pure game.

---

## 7. Actual four-branch pure game

Let `z=(t,x,nu,p,X)` denote the slow state, belief, gradient, and Hessian data
produced by Papers III--IV.  Take compact Euclidean controls large enough to
contain the functions below and define

\[
\begin{aligned}
F(z,u,v)={}&h(z)+b(z)\cdot u+c(z)\cdot v
-\frac{\lambda}{2}|u|^2
+\frac{\mu}{2}|v|^2
+u^TC(z)v,
\end{aligned}
\tag{7.1}
\]

where `lambda,mu>0` and all coefficients are bounded Lipschitz functions of
`z`.  The control enters the finite-response port before the K2 limit, so
`F` is the actual local Hamiltonian of the four-branch game, not a post-hoc
PDE choice.

Equation (7.1) is strongly concave in `u` and strongly convex in `v`.  In the
scalar case the unique interior saddle is

\[
\boxed{
 u_*(z)=\frac{\mu b(z)-\gamma(z)c(z)}
 {\gamma(z)^2+\lambda\mu},
\qquad
 v_*(z)=\frac{-\gamma(z)b(z)-\lambda c(z)}
 {\gamma(z)^2+\lambda\mu}.
}
\tag{7.2}
\]

The vector case is the unique solution of the strongly monotone block system

\[
\lambda u-Cv=b,
\qquad
C^Tu+\mu v=-c.
\tag{7.3}
\]

Choose the action sets to contain this solution uniformly.  The selectors are
Lipschitz in `z`, so the actual monotone game schemes of Paper IV converge to
one pure Isaacs equation, not merely to a mixed relaxed value.

### Theorem 7.1 (actual pure-Isaacs chain)

The four-branch deterministic fast model, equipped with the control port
(7.1), has a unique pure feedback saddle, a pure Isaacs Hamiltonian, a
well-posed pure-strategy DPP, and the corresponding viscosity limit.

---

## 8. Export

```yaml
id: P4-PURE-ISAACS-MAXIMAL
general_theory:
  pure_saddle_equivalent_to: pure_H_minus_equals_H_plus
  measurable_selector: Caratheodory_plus_nonempty_saddle_correspondence
positive_classes:
  - uniformly_strong_concave_convex
  - finite_action_strict_margin
actual_system:
  fast_model: four_branch_moving_seam
  Hamiltonian: quadratic_bilinear_control_port
  selector: unique_Lipschitz_pure_feedback
negative_result:
  counterexample: matching_pennies
  mixed_to_pure_without_certificate: false
```
