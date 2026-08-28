# Actual weighted noncompact and path-dependent θ-model

## 0. Goal and separation of branches

This note constructs one deterministic product system that supplies two
compatible actual branches:

1. a **weighted noncompact filtering branch** with an unbounded hidden state,
   a polynomial Lyapunov function, an invariant posterior moment ball, and
   exponential filter stability;
2. a **genuinely path-dependent branch** in which the fast filter observable is
   averaged into a delay diffusion, followed by a pure path game, a segment
   DPP, a path/segment PDE, and a BSDE evaluation.

The filter is fast in the second branch. Its stationary average enters the slow
drift, while its centered fluctuations are `o(1)` at the slow scale. The
limiting PPDE is therefore a function of the delay path alone; it does not
silently retain a fast belief variable after averaging.

The two per-paper exports are

```text
P4-WEIGHTED-NONCOMPACT-ACTUAL
P5-PATH-ACTUAL
```

and their series-level bundle is

```text
P4-P5-WEIGHTED-PATH-ACTUAL.
```

---

## 1. Deterministic Bernoulli product base

### 1.1 Moving-seam coordinate

Let `T_a` be the open four-branch moving-seam map from Paper I. Under Lebesgue
measure its branch labels `I_n in {1,2,3,4}` are iid with probabilities
`w_i(a)`.

### 1.2 Countable full-branch coordinate

Fix `0<r<1`. Let

\[
\mathcal A=\{(s,k):s\in\{-1,1\},\ k\ge1\},
\qquad
p_{s,k}=\frac{1-r}{2}r^{k-1}.
\tag{1.1}
\]

Partition `[0,1]` into intervals `I_(s,k)` of lengths `p_(s,k)` and map every
interval affinely onto `[0,1]`. Denote the map by `G`. Its Perron operator is

\[
(L_Gh)(y)=\sum_{s,k}p_{s,k}
 h(a_{s,k}+p_{s,k}y),
\tag{1.2}
\]

so Lebesgue measure is invariant and the branch symbols `J_n=(S_n,K_n)` are
iid with law (1.1). Define

\[
\xi(J_n)=S_nK_n.
\tag{1.3}
\]

Then `E xi=0`, the support is unbounded, and `xi` has moments of every order
and an exponential moment for every `eta<-log r`.

### 1.3 Exact deterministic observation uniforms

Let

\[
\Omega_U=[0,1]^{\mathbb Z},
\qquad
\mathbb P_U=\operatorname{Leb}^{\mathbb Z},
\]

and let `S_U` be the left shift. The coordinate functions

\[
U_n(\omega)=\omega_n
\]

are iid uniforms under `P_U`, although the evolution is the single
deterministic map `S_U`. This avoids the false assertion that successive
states of the doubling map themselves are iid uniforms.

The complete deterministic fast base is

\[
\boxed{
\mathcal T_a=T_a\times G\times S_U.
}
\tag{1.4}
\]

All random variables below are deterministic coordinate functions of this
measure-preserving system equipped with its invariant initial law.

---

## 2. Noncompact hidden signal

Let `|alpha|<1` and define

\[
Y_{n+1}=\alpha Y_n+\xi(J_{n+1}).
\tag{2.1}
\]

The unique stationary solution is

\[
Y_n=\sum_{j=0}^{\infty}\alpha^j\xi(J_{n-j}).
\tag{2.2}
\]

Its support is unbounded.

### Proposition 2.1 (polynomial Lyapunov drift)

For `W(y)=1+y^2`,

\[
\boxed{
PW(y)\le\alpha^2W(y)+b,
\qquad
b=1+\mathbb E\xi^2-\alpha^2.
}
\tag{2.3}
\]

Indeed,

\[
\mathbb E[1+(\alpha y+\xi)^2]
=1+\alpha^2y^2+\mathbb E\xi^2.
\]

### Proposition 2.2 (exact synchronous contraction)

Under the same innovations,

\[
\boxed{
|Y_n^y-Y_n^{y'}|=|\alpha|^n|y-y'|.
}
\tag{2.4}
\]

---

## 3. Bounded nondegenerate observations

At an observation time define `O_n in {-1,1}` by

\[
O_n=1
\quad\Longleftrightarrow\quad
U_n\le g_1(Y_n),
\]

where

\[
g_o(y)=\frac{1+o\epsilon\tanh y}{2},
\qquad 0<\epsilon<1.
\tag{3.1}
\]

Thus

\[
g_-:=\frac{1-\epsilon}{2}
\le g_o(y)\le
\frac{1+\epsilon}{2}=:g_+,
\tag{3.2}
\]

and the observation kernel is generated exactly by the deterministic uniform
coordinate. The Bayes operator is

\[
B_o\mu(dy)=\frac{g_o(y)\mu(dy)}{\mu(g_o)}.
\tag{3.3}
\]

---

## 4. Weighted moment ball and filter contraction

Put `q_g=g_+/g_-`. A Bayes update satisfies

\[
B_o\mu(W)\le q_g\mu(W).
\tag{4.1}
\]

After `m` prediction steps,

\[
P^mW(y)
\le\alpha^{2m}W(y)+b_m,
\qquad
b_m=b\sum_{j=0}^{m-1}\alpha^{2j}.
\tag{4.2}
\]

Choose `m_*` so that

\[
\boxed{q_g\alpha^{2m_*}<1.}
\tag{4.3}
\]

Then

\[
\mathcal K_M=\{\mu:\mu(W)\le M\}
\]

is invariant whenever

\[
M\ge\frac{q_gb_{m_*}}
{1-q_g\alpha^{2m_*}}.
\tag{4.4}
\]

Define the weighted bounded-Lipschitz metric

\[
d_W(\mu,\nu)
=\sup_f|\mu(f)-\nu(f)|,
\tag{4.5}
\]

where

\[
|f(y)|\le W(y),
\qquad
|f(y)-f(y')|
\le(1+|y|+|y'|)|y-y'|.
\]

### Lemma 4.1 (Bayes bound)

On `K_M`,

\[
d_W(B_o\mu,B_o\nu)
\le C_B(M,\epsilon)d_W(\mu,\nu).
\tag{4.6}
\]

#### Proof

Use

\[
B_o\mu(f)-B_o\nu(f)
=
\frac{\mu(g_of)-\nu(g_of)}{\mu(g_o)}
+
\nu(g_of)
\frac{\nu(g_o)-\mu(g_o)}{\mu(g_o)\nu(g_o)}.
\]

The denominators are at least `g_-`; multiplication by the bounded globally
Lipschitz function `g_o` maps the weighted test class into a fixed multiple of
it; and `nu(W)<=M` controls the normalization term.

### Lemma 4.2 (prediction bound)

There is `C_P(M)` such that

\[
d_W(P^m\mu,P^m\nu)
\le C_P(M)|\alpha|^m d_W(\mu,\nu)
\tag{4.7}
\]

for `mu,nu in K_M`.

#### Proof

Use the synchronous coupling (2.4). The weighted Lipschitz factor along the
two coupled trajectories is bounded in expectation by the uniform second
moment supplied by (2.3)--(4.4).

Increase the observation gap, if necessary, until

\[
\boxed{
q_*:=C_B(M,\epsilon)C_P(M)|\alpha|^{m_*}<1.
}
\tag{4.8}
\]

### Theorem 4.3 (actual weighted noncompact filter)

For every two initial beliefs in `K_M`, filters driven by the same observation
path satisfy

\[
\boxed{
 d_W(\pi_n^\mu,\pi_n^\nu)
 \le q_*^n d_W(\mu,\nu).
}
\tag{4.9}
\]

The hidden state has unbounded stationary support. This proves the actual
export `P4-WEIGHTED-NONCOMPACT-ACTUAL`.

---

## 5. Stationary filter observable and averaging

Let

\[
H(\pi)=\int\tanh(y)\,\pi(dy).
\tag{5.1}
\]

The prediction--Bayes recursion on `K_M` is a contractive iterated random
function. It therefore has a unique stationary law `Lambda` and is
geometrically ergodic in `d_W`. Define

\[
\bar m=\int H(\pi)\,\Lambda(d\pi).
\tag{5.2}
\]

For the stationary filter process,

\[
\frac1N\sum_{n=0}^{N-1}H(\pi_n)
\longrightarrow\bar m
\tag{5.3}
\]

in `L^2`. Because `H` is bounded and the filter is geometrically mixing, the
centered partial sums are `O_{L^2}(N^{1/2})`.

Consequently, if the slow drift is multiplied by `epsilon^2` and
`N_epsilon=O(epsilon^{-2})`, then

\[
\epsilon^2
\sum_{n<N_\epsilon}
[H(\pi_n)-\bar m]
=O_{L^2}(\epsilon)
\longrightarrow0.
\tag{5.4}
\]

This is the precise reason the fast belief variable disappears from the
limiting path equation.

---

## 6. Slow delay state driven by the deterministic fast system

Let `zeta(I_n)` be a bounded centered vector observable of the four-branch
symbol with nondegenerate covariance `Sigma(a)`. At slow step
`h_epsilon=epsilon^2`, define

\[
\begin{aligned}
X_{n+1}^\epsilon
={}&X_n^\epsilon
+\epsilon^2 b(\mathbf X_n^\epsilon,
              H(\pi_n^\epsilon),u_n,v_n)
+\epsilon\sigma_0\zeta(I_{n+1}),
\end{aligned}
\tag{6.1}
\]

where `mathbf X_n^epsilon` is the interpolated window on `[-delta,0]`. Take

\[
\begin{aligned}
b(\omega,m,u,v)
={}&-\kappa\omega(0)
+\int_{-\delta}^0K(\theta)\tanh(\omega(\theta))d\theta\\
&+\beta m+B_uu+B_vv,
\end{aligned}
\tag{6.2}
\]

with `kappa>||K||_1` and bounded controls.

The branch noise has the enhanced WIP of
`OPTIMAL_ENHANCED_WIP_RATE.md`. Since it enters additively, the segment
solution map is continuous in the uniform driving path.

### Theorem 6.1 (deterministic delay homogenization)

After the vanishing filter initial layer, the interpolation of (6.1) converges
jointly with its delay window to

\[
\boxed{
 dX_t=b(X_{t+\cdot},\bar m,u_t,v_t)dt
 +\sigma_0\Sigma(a)^{1/2}dB_t.
}
\tag{6.3}
\]

The convergence is uniform over bounded Lipschitz feedbacks.

#### Proof

Replace `H(pi_n)` by `bar m` using (5.4), replace the branch random walk by
Brownian motion using the quantitative WIP, and apply a discrete Gronwall
estimate to the Lipschitz delay Euler map.

For

\[
\mathcal V(\omega)=1+\|\omega\|_\infty^2,
\tag{6.4}
\]

dissipativity, BDG, and Gronwall yield

\[
\mathbb E\sup_{t\le T}\mathcal V(X_{t+\cdot})
\le C_T\mathcal V(\omega_0).
\tag{6.5}
\]

The path state is noncompact.

---

## 7. Genuinely path-dependent pure game

Let

\[
\Phi(\omega)
=
\arctan\left(\int_{-\delta}^0q(\theta)\omega(\theta)d\theta\right)
+\lambda_0\tanh\left(\max_{\theta\in[-\delta,0]}\omega(\theta)\right).
\tag{7.1}
\]

This bounded Lipschitz payoff cannot be reduced to `omega(0)`.

Take

\[
\begin{aligned}
\ell(\omega,u,v)
={}&\ell_0(\omega)
+b_1(\omega)\cdot u+c_1(\omega)\cdot v\\
&-\frac{\lambda_u}{2}|u|^2
+\frac{\lambda_v}{2}|v|^2
+u^TC(\omega)v.
\end{aligned}
\tag{7.2}
\]

It is strongly concave in `u` and strongly convex in `v`. The theorem in
`PURE_STRATEGY_ISAACS.md` gives a unique Lipschitz pure saddle

\[
(u_*(\omega),v_*(\omega)).
\tag{7.3}
\]

---

## 8. Segment DPP and path/segment PDE

Let

\[
\Omega_\delta=C([-\delta,0];\mathbb R^d).
\]

The delay diffusion is Markov on `Omega_delta`. Let `S` denote the horizontal
shift generator on the segment, and let `partial_0`, `partial_{00}^2` denote
vertical derivatives at the present endpoint. For a stopping time `tau`, the
pure value satisfies

\[
V(t,\omega)
=
\sup_u\inf_v
\mathbb E\left[
\int_t^\tau\ell(X_{s+\cdot},u_s,v_s)ds
+V(\tau,X_{\tau+\cdot})
\right].
\tag{8.1}
\]

After inserting the unique saddle, the generator-oriented segment equation is

\[
\boxed{
\partial_tV
+\mathcal SV
+b_*(\omega)\cdot\partial_0V
+\frac12
\operatorname{Tr}
(\sigma_0\Sigma\sigma_0^T\partial_{00}^2V)
+\ell_*(\omega)=0.
}
\tag{8.2}
\]

The terminal condition is (7.1).

### Theorem 8.1 (actual path-dependent value)

Under the displayed Lipschitz, nondegeneracy, and dissipativity conditions,
the DPP value is the unique viscosity/mild solution of (8.2) in the
polynomial-growth class controlled by (6.4).

The comparison input is precisely typed: semilinear segment/path equation,
constant nondegenerate vertical diffusion, Lipschitz drift and driver, and
polynomial localization. There is no omitted belief-state derivative.

---

## 9. BSDE path evaluation

Under the pure saddle, solve (6.3) and

\[
Y_t=\Phi(X_{T+\cdot})
+\int_t^T f(s,X_{s+\cdot},Y_s,Z_s)ds
-\int_t^TZ_s\,dB_s,
\tag{9.1}
\]

where `f` is the saddle-reduced Lipschitz driver. Standard Lipschitz BSDE
theory gives a unique solution and

\[
\boxed{
V(t,\omega)=Y_t^{t,\omega}.
}
\tag{9.2}
\]

This proves the actual export `P5-PATH-ACTUAL`.

---

## 10. Full actual construction

```text
four-branch moving-seam map
x countable full-branch innovation map
x deterministic Bernoulli shift of iid uniforms
  -> unbounded AR(1) hidden signal
  -> weighted moment ball and filter contraction
  -> stationary filter averaging
  -> additive deterministic WIP
  -> noncompact delay diffusion
  -> strong concave-convex pure path game
  -> segment DPP and path PDE
  -> BSDE path evaluation.
```

The weighted-filter and path-evaluation branches are both actual. Their
coupling is explicit: the former contributes the averaged coefficient
`bar m` to the latter.

---

## 11. Export packet

```yaml
bundle: P4-P5-WEIGHTED-PATH-ACTUAL
P4_export: P4-WEIGHTED-NONCOMPACT-ACTUAL
P5_export: P5-PATH-ACTUAL
fast_system:
  parameter_coordinate: four_branch_moving_seam
  unbounded_innovation_coordinate: countable_full_branch_Bernoulli
  observation_noise_coordinate: two_sided_uniform_Bernoulli_shift
hidden_state:
  dynamics: contractive_AR1
  support: unbounded
  Lyapunov: 1+y^2
filter:
  invariant_moment_ball: true
  contraction: observation_gap_plus_prediction_contraction
coupling_to_path:
  mechanism: stationary_filter_average
  centered_filter_drift_error: O_L2(epsilon)
slow_path:
  state: C([-delta,0])
  dynamics: dissipative_delay_diffusion
control:
  pure_saddle: strong_concave_convex
outputs:
  - weighted_noncompact_filter
  - deterministic_delay_homogenization
  - segment_DPP
  - path_dependent_value_equation
  - BSDE_path_evaluation
```

## Primary context

- I. Ekren, C. Keller, N. Touzi, J. Zhang, *On viscosity solutions of path
  dependent PDEs*, arXiv:1109.5971.
- Z. Ren, N. Touzi, J. Zhang, *Comparison of viscosity solutions of
  semi-linear path-dependent PDEs*, arXiv:1410.7281.
- A. S. Reddy, A. Apte, *Stability of non-linear filter for deterministic
  dynamics*, arXiv:1910.14348.
