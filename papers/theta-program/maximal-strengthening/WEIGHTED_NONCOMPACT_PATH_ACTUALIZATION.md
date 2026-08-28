# Actual weighted noncompact and path-dependent θ-model

## 0. Goal

This note constructs one deterministic fast system that simultaneously
actualizes:

- an unbounded hidden state with a polynomial Lyapunov function;
- a weighted nonlinear filter with an invariant moment ball and contraction;
- a noncompact slow/path state;
- a genuinely delay-dependent control game;
- a unique pure feedback saddle;
- a path-space DPP, PPDE, and BSDE/path evaluation;
- a deterministic-fast-to-diffusion limit.

The main export is

```text
P4-P5-WEIGHTED-PATH-ACTUAL.
```

---

## 1. Deterministic Bernoulli product base

### 1.1 Moving-seam coordinate

Let `T_a` be the open four-branch moving-seam map from Paper I.  Under Lebesgue
measure its branch labels `I_n in {1,2,3,4}` are iid with probabilities
`w_i(a)`.

### 1.2 Countable full-branch coordinate

Fix `0<r<1`.  Let

\[
\mathcal A=\{(s,k):s\in\{-1,1\},\ k\ge1\},
\]

and

\[
p_{s,k}=\frac{1-r}{2}r^{k-1}.
\tag{1.1}
\]

Partition `[0,1]` into intervals `I_(s,k)` of these lengths and map every
interval affinely and orientation-preservingly onto `[0,1]`.  Denote the map by
`G`.  Its Perron operator is

\[
(L_Gh)(y)=\sum_{s,k}p_{s,k}
 h(a_{s,k}+p_{s,k}y),
\tag{1.2}
\]

so Lebesgue measure is invariant and the branch symbols `J_n=(S_n,K_n)` are
iid with law (1.1).

Define the unbounded centered innovation

\[
\xi(J_n)=S_nK_n.
\tag{1.3}
\]

It has zero mean, finite moments of every order, and an exponential moment for
all `eta< -log r`.

### 1.3 Observation-noise coordinate

Add an independent two-full-branch map `U(u)=2u mod 1`.  Its branch digits
supply iid uniforms after the usual binary coding.  The complete deterministic
fast base is

\[
\mathcal T_a=T_a\times G\times U.
\tag{1.4}
\]

All stochastic variables below are deterministic functions of this measure-
preserving system and its invariant initial distribution.

---

## 2. Noncompact hidden signal

Let `|alpha|<1` and define

\[
Y_{n+1}=\alpha Y_n+\xi(J_{n+1}).
\tag{2.1}
\]

This skew product has the unique stationary solution

\[
Y_n=\sum_{j=0}^{\infty}\alpha^j\xi(J_{n-j}).
\tag{2.2}
\]

Its support is unbounded.

### Proposition 2.1 (polynomial Lyapunov drift)

For

\[
W(y)=1+y^2,
\]

\[
\boxed{
PW(y)
\le \alpha^2W(y)+b,
\qquad
b=1+\mathbb E\xi^2-\alpha^2.
}
\tag{2.3}
\]

#### Proof

Use `E xi=0` in

\[
\mathbb E[1+(\alpha y+\xi)^2]
=1+\alpha^2y^2+\mathbb E\xi^2.
\]

### Proposition 2.2 (exact synchronous contraction)

If two copies use the same innovation sequence, then

\[
\boxed{
|Y_n^y-Y_n^{y'}|=|\alpha|^n|y-y'|.
}
\tag{2.4}
\]

Thus the prediction kernel contracts every ordinary Wasserstein distance
compatible with the first moment.

---

## 3. Bounded nondegenerate observations

At observation times define `O_n in {-1,1}` by inverse transform using the
independent `U` coordinate and

\[
g_o(y)=\frac{1+o\epsilon\tanh y}{2},
\qquad 0<\epsilon<1.
\tag{3.1}
\]

Then

\[
g_-:=\frac{1-\epsilon}{2}
\le g_o(y)\le
\frac{1+\epsilon}{2}=:g_+,
\tag{3.2}
\]

and `g_o` is globally Lipschitz.

Let `B_o` be the Bayes operator

\[
B_o\mu(dy)=\frac{g_o(y)\mu(dy)}{\mu(g_o)}.
\tag{3.3}
\]

---

## 4. Weighted filter moment ball

For `q_g=g_+/g_-`, an observation update satisfies

\[
B_o\mu(W)\le q_g\mu(W).
\tag{4.1}
\]

After `m` prediction steps,

\[
P^mW(y)
\le\alpha^{2m}W(y)
+b_m,
\qquad
b_m=b\sum_{j=0}^{m-1}\alpha^{2j}.
\tag{4.2}
\]

Choose `m_*` so that

\[
\boxed{q_g\alpha^{2m_*}<1.}
\tag{4.3}
\]

Then every ball

\[
\mathcal K_M=\{\mu:\mu(W)\le M\}
\]

with

\[
M\ge\frac{q_gb_{m_*}}
{1-q_g\alpha^{2m_*}}
\tag{4.4}
\]

is invariant under one prediction--observation cycle.

### Lemma 4.1 (weighted Bayes Lipschitz bound)

On `K_M`, multiplication by `g_o` and normalization in (3.3) are Lipschitz for
the weighted bounded-Lipschitz metric

\[
d_W(\mu,\nu)
=
\sup_f|\mu(f)-\nu(f)|,
\tag{4.5}
\]

where the test class satisfies

\[
|f(y)|\le W(y),
\quad
|f(y)-f(y')|
\le(1+|y|+|y'|)|y-y'|.
\]

More precisely,

\[
d_W(B_o\mu,B_o\nu)
\le C_B(M,\epsilon)d_W(\mu,\nu).
\tag{4.6}
\]

#### Proof

Write

\[
B_o\mu(f)-B_o\nu(f)
=
\frac{\mu(g_of)-\nu(g_of)}{\mu(g_o)}
+
\nu(g_of)
\frac{\nu(g_o)-\mu(g_o)}{\mu(g_o)\nu(g_o)}.
\]

Use `mu(g_o),nu(g_o)>=g_-`, the global Lipschitz bound for `g_o`, and the
uniform `W`-moment bound `M`.  Both `g_of` and `g_o` lie in a fixed multiple of
the test class.

Prediction over `m` steps has a weighted synchronous coupling bound

\[
d_W(P^m\mu,P^m\nu)
\le C_P(M)|\alpha|^m d_W(\mu,\nu).
\tag{4.7}
\]

Increase the observation gap, if necessary, so that

\[
\boxed{
q_*:=C_B(M,\epsilon)C_P(M)|\alpha|^{m_*}<1.
}
\tag{4.8}
\]

### Theorem 4.2 (actual weighted noncompact filter)

For every two initial beliefs in `K_M`, the filters driven by the same
observation path satisfy

\[
\boxed{
 d_W(\pi_n^\mu,\pi_n^\nu)
 \le q_*^n d_W(\mu,\nu).
}
\tag{4.9}
\]

The signal state is noncompact and has unbounded stationary support.

---

## 5. Slow delay state driven by the deterministic fast system

Let `zeta(I_n)` be a bounded centered vector observable of the four-branch
symbol with nondegenerate covariance `Sigma(a)`.  At slow step
`h_epsilon=epsilon^2`, define

\[
\begin{aligned}
X_{n+1}^\epsilon
={}&X_n^\epsilon
+\epsilon^2 b(\mathbf X_n^\epsilon,
              \widehat m_n^\epsilon,u_n,v_n)
+\epsilon\sigma_0\zeta(I_{n+1}),
\end{aligned}
\tag{5.1}
\]

where

- `mathbf X_n^epsilon` is the interpolated delay window on `[-delta,0]`;
- `widehat m_n^epsilon=int tanh(y) pi_n^epsilon(dy)`;
- `u_n,v_n` are feedback controls.

Take

\[
\begin{aligned}
b(\omega,m,u,v)
={}&-\kappa\omega(0)
+\int_{-\delta}^0K(\theta)\tanh(\omega(\theta))d\theta\\
&+\beta m+B_uu+B_vv,
\end{aligned}
\tag{5.2}
\]

with `kappa>||K||_1` and bounded controls.

The branch noise has the topology-optimal enhanced WIP of
`OPTIMAL_ENHANCED_WIP_RATE.md`.  Since it enters additively, the delay solution
map is Lipschitz in the uniform driving path on bounded intervals.

### Theorem 5.1 (deterministic delay homogenization)

After the vanishing filter initial layer, the interpolation of (5.1) converges
to the stochastic delay equation

\[
\boxed{
 dX_t=b(X_{t+\cdot},\bar m,u_t,v_t)dt
 +\sigma_0\Sigma(a)^{1/2}dB_t,
}
\tag{5.3}
\]

where `bar m` is the stationary filtered mean.  The convergence holds jointly
with the filter collapse and uniformly over bounded Lipschitz feedbacks.

#### Proof

Use the WIP for the additive noise, (4.9) for the filtered mean, and the
Lipschitz continuity of the delay Euler map.  A discrete Gronwall estimate
shows that replacing the filter by its stationary version and the random walk
by Brownian motion changes the solution by a quantity tending to zero.

### Proposition 5.2 (noncompact path weight)

For

\[
\mathcal V(\omega,\mu)
=1+\|\omega\|_\infty^2+\mu(W),
\tag{5.4}
\]

solutions of (5.3) and the filter satisfy, on every finite horizon,

\[
\mathbb E\sup_{t\le T}\mathcal V(X_{t+\cdot},\pi_t)
\le C_T\mathcal V(\omega_0,\mu_0).
\tag{5.5}
\]

Dissipativity of (5.2), BDG, and (2.3) prove the estimate.

---

## 6. Genuinely path-dependent payoff and pure game

Let

\[
\Phi(\omega)
=
\arctan\left(\int_{-\delta}^0q(\theta)\omega(\theta)d\theta\right)
+\lambda_0\tanh\left(\max_{\theta\in[-\delta,0]}\omega(\theta)\right).
\tag{6.1}
\]

This bounded Lipschitz payoff depends on the entire terminal window.  It is not
a function of the current value `omega(0)`.

Take the running payoff

\[
\begin{aligned}
\ell(\omega,\mu,u,v)
={}&\ell_0(\omega,\mu)
+b_1(\omega,\mu)\cdot u
+c_1(\omega,\mu)\cdot v\\
&-\frac{\lambda_u}{2}|u|^2
+\frac{\lambda_v}{2}|v|^2
+u^TC(\omega,\mu)v.
\end{aligned}
\tag{6.2}
\]

It is strongly concave in `u` and strongly convex in `v`.  By
`PURE_STRATEGY_ISAACS.md`, it has a unique Lipschitz pure saddle

\[
(u_*(\omega,\mu),v_*(\omega,\mu)).
\tag{6.3}
\]

---

## 7. Path DPP and PPDE

Let `Omega_delta=C([-delta,0];R^d)`.  Concatenation of a delay path with a future
control and Brownian increment defines the canonical path-state transition.
For a stopping time `tau`, the pure value satisfies

\[
V(t,\omega,\mu)
=
\sup_u\inf_v
\mathbb E\left[
\int_t^\tau\ell_sds
+V(\tau,X_{\tau+\cdot},\pi_\tau)
\right].
\tag{7.1}
\]

The proof is the usual two-sided concatenation argument; the filter state is
included in the state variable, so no hidden history is discarded.

After substituting the unique saddle, the equation is a semilinear
path-dependent PDE in generator orientation:

\[
\partial_tV
+\frac12\operatorname{Tr}
(\sigma_0\Sigma\sigma_0^T\partial_{\omega\omega}^2V)
+\langle b_*,\partial_\omega V\rangle
+\ell_*=0,
\tag{7.2}
\]

with terminal value (6.1).  Here the derivatives are Dupire/path derivatives
on the canonical delay state.

### Theorem 7.1 (actual weighted path PPDE)

Under the displayed Lipschitz, moment, nondegeneracy, and dissipativity
conditions, (7.2) has a unique viscosity solution in the class with growth
controlled by `V` in (5.4), and the DPP value is that solution.

The theorem uses the standard semilinear PPDE comparison packet: functional
Ito calculus, bounded/Lipschitz driver, nondegenerate constant diffusion, and
polynomial-growth localization.

---

## 8. BSDE/path evaluation

Under the pure feedback saddle, solve (5.3) and

\[
Y_t=\Phi(X_{T+\cdot})
+\int_t^T f(s,X_{s+\cdot},\pi_s,Y_s,Z_s)ds
-\int_t^TZ_sdB_s,
\tag{8.1}
\]

where `f` is the saddle-reduced running driver.  Standard Lipschitz BSDE theory
gives a unique solution and

\[
\boxed{
V(t,\omega,\mu)=Y_t^{t,\omega,\mu}.
}
\tag{8.2}
\]

This is an actual path evaluation, not a Markov payoff with path notation.

---

## 9. Full actual chain

```text
four-branch moving-seam map
x countable full-branch innovation map
x deterministic observation-noise map
  -> unbounded AR(1) hidden state
  -> polynomial Lyapunov and weighted filter contraction
  -> deterministic additive WIP
  -> delay-state diffusion homogenization
  -> strong concave-convex pure game
  -> path DPP and semilinear PPDE
  -> BSDE path evaluation.
```

Every arrow is actual for the model above.

---

## 10. Export

```yaml
id: P4-P5-WEIGHTED-PATH-ACTUAL
fast_system:
  parameter_coordinate: four_branch_moving_seam
  unbounded_innovation_coordinate: countable_full_branch_Bernoulli
  observation_noise_coordinate: deterministic_Bernoulli
hidden_state:
  dynamics: contractive_AR1
  support: unbounded
  Lyapunov: 1+y^2
filter:
  likelihood: bounded_positive_tanh
  invariant_moment_ball: true
  contraction: observation_gap_plus_prediction_contraction
slow_path:
  state: C([-delta,0])
  dynamics: dissipative_delay_SDE
  deterministic_homogenization: additive_driver
control:
  pure_saddle: strong_concave_convex
outputs:
  - weighted_filter
  - weighted_path_DPP
  - viscosity_PPDE
  - BSDE_path_evaluation
```

## Primary PPDE/filter context

- I. Ekren, C. Keller, N. Touzi, J. Zhang, *On viscosity solutions of path
  dependent PDEs*, arXiv:1109.5971.
- Z. Ren, N. Touzi, J. Zhang, *Comparison of viscosity solutions of
  semi-linear path-dependent PDEs*, arXiv:1410.7281.
- A. S. Reddy, A. Apte, *Stability of non-linear filter for deterministic
  dynamics*, arXiv:1910.14348.
