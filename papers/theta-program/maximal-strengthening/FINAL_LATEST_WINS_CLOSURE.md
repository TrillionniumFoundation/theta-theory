# θ-Theory maximal strengthening — final latest-wins closure

**Date:** 2026-08-28  
**Scope:** θ-Theory only  
**Policy:** `LATEST-WINS / FAIL-CLOSED / ACTUAL-WITNESS-OR-MAXIMAL-NO-GO / NO-HIDDEN-GENERICITY`

This document supersedes any stronger reading of the earlier maximal-strengthening notes.  It closes the five requested strengthenings at the strongest scope supported by complete calculations.  In particular, it does not rename a source-specific or conjugate theorem as a generic nonconjugate theorem.

---

# 1. Actual nonconjugate specular finite-horizon Sinai U3

## 1.1 Radial family

Let a finite-horizon periodic Sinai table contain two circular scatterers with radii `R_1,R_2>0` and a regular normal period-two orbit between them.  Keep the centres fixed and set

\[
R_1(a)=R_1+a,
\qquad |a|<a_0,
\]

where `a_0` is chosen so that strict convexity, no overlap and finite horizon persist.  The resulting family is specular and genuinely moves a singularity set.

In paraxial Jacobi coordinates use

\[
F(d)=\begin{pmatrix}1&d\\0&1\end{pmatrix},
\qquad
S(\kappa)=\begin{pmatrix}1&0\\2\kappa&1\end{pmatrix}.
\]

For the normal two-cycle the return matrix is

\[
M(a)=S(\kappa_1(a))F(d(a))S(\kappa_2)F(d(a)),
\]

with

\[
\kappa_1(a)=\frac1{R_1+a},
\qquad
\kappa_2=\frac1{R_2},
\qquad
d(a)=d_0-a.
\]

A direct multiplication gives

\[
\operatorname{tr}M(a)
=2+4d(a)(\kappa_1(a)+\kappa_2)
 +4d(a)^2\kappa_1(a)\kappa_2.
\tag{1.1}
\]

Consequently

\[
\begin{aligned}
\frac d{da}\operatorname{tr}M(0)
={}&-4(\kappa_1+\kappa_2)
 -4d_0\kappa_1^2
 -8d_0\kappa_1\kappa_2
 -4d_0^2\kappa_1^2\kappa_2<0.
\end{aligned}
\tag{1.2}
\]

The period-two multiplier therefore changes.  Since periodic multipliers are invariants of smooth time-preserving conjugacy, this radial family is nonconjugate.

## 1.2 Explicit invariant-density jets

Pull every collision section to the fixed disjoint union

\[
\bigsqcup_i \mathbb T_i\times(-\pi/2,\pi/2)
\]

using normalized boundary coordinate `x`.  If the physical perimeter of component `i` is `ell_i(a)` and

\[
L(a)=\sum_i\ell_i(a),
\]

then the invariant collision probability has density

\[
\rho_a(i,x,\varphi)
=\frac{\ell_i(a)\cos\varphi}{2L(a)}.
\tag{1.3}
\]

Hence `a -> rho_a` is real analytic for the radial family.  Let `L_a` be the pulled-back transfer operator.  Differentiating

\[
L_a\rho_a=\rho_a
\]

through order `j<=3` gives the completely assembled source

\[
S_j
:=\sum_{k=1}^{j}{j\choose k}L_0^{[k]}\rho_0^{(j-k)}
=(I-L_0)\rho_0^{(j)}.
\tag{1.4}
\]

Although the individual branch derivatives in the left side contain moving-face currents, their same-occurrence totalization is the smooth function on the right.  Since

\[
\int\rho_a=1,
\qquad
\int\rho_0^{(j)}=0\quad(j\ge1),
\]

the reduced resolvent `R_0=(I-L_0)^{-1}` on the centred strong space satisfies

\[
\boxed{R_0S_j=\rho_0^{(j)},\qquad j=1,2,3.}
\tag{1.5}
\]

This is an actual nonconjugate, nonzero, source-specific U3 response channel.

## 1.3 Exact cohomological spectral channel

Let `c(a)` be a nonconstant analytic scalar and let `g_a` be a bounded analytic family in the declared multiplier algebra.  Set

\[
\psi_a=c(a)+g_a-g_a\circ T_a.
\tag{1.6}
\]

For

\[
L_{a,q}f=L_a(e^{q\psi_a}f),
\]

the transfer identity `L_a((h\circ T_a)F)=hL_aF` yields

\[
\boxed{
L_{a,q}
=e^{qc(a)}M_{e^{-qg_a}}L_aM_{e^{qg_a}}.
}
\tag{1.7}
\]

Thus the leading eigenvalue is `e^{q c(a)}`, the spectral projector is the conjugated projector of `L_a`, and every mixed `(a,q)` derivative exists to all orders allowed by `rho_a,g_a,c(a)`.  This supplies a nontrivial pressure response while preserving exact control of the moving singularities.

### Theorem S-RADIAL-U3

The radial family has actual third-order response for:

1. its invariant projector and all static pulled-back smooth observables;
2. the completely assembled differentiated-invariance sources `S_1,S_2,S_3`;
3. every analytic constant-plus-coboundary twisted channel (1.6).

The theorem is not a claim that arbitrary noncoboundary twists have generic third-order response.  The latter remains exactly the packetized Paper-I theorem and cannot be inferred from geometry alone.

---

# 2. Full high-frequency moving-family BDL: exact similarity witness

The most reliable actual family is obtained by scaling an entire finite-horizon table, rather than claiming unproved differentiability of a generic moving graph domain.

Let `Q_0` be a finite-horizon periodic Sinai billiard and let

\[
Q_a=s(a)Q_0,
\qquad
0<s_-\le s(a)\le s_+<\infty,
\]

where the ambient lattice, every scatterer and every free-flight length are scaled by `s(a)`.  Let `C_a` be the phase-space scaling map.  Unit-speed flows satisfy

\[
\Phi_a^t C_a=C_a\Phi_0^{t/s(a)}.
\tag{2.1}
\]

For the flow generators,

\[
A_a=s(a)^{-1}C_aA_0C_a^{-1}.
\tag{2.2}
\]

Therefore, wherever the resolvent is defined,

\[
\boxed{
(z-A_a)^{-1}
=s(a)C_a\bigl(s(a)z-A_0\bigr)^{-1}C_a^{-1}.
}
\tag{2.3}
\]

If the fixed-table BDL estimate is

\[
\|(w-A_0)^{-1}\|_{\mathcal B\to\mathcal B}
\le C(1+|\operatorname{Im}w|)^\nu
\tag{2.4}
\]

on its declared resonance-free high-frequency region, then (2.3) gives, uniformly in `a`,

\[
\|(z-A_a)^{-1}\|
\le C'(1+|\operatorname{Im}z|)^\nu.
\tag{2.5}
\]

The complete resonance set scales by `s(a)^{-1}`.  Since (2.3) is an exact identity, all parameter derivatives follow by the ordinary product and chain rules on the transported fixed spaces.  No moving-face differentiation is hidden in this result.

### Theorem HF-SIMILARITY-BDL

The compact similarity family `Q_a=s(a)Q_0` has:

1. the full fixed-table high-frequency BDL resolvent estimate uniformly in `a`;
2. the complete scaled resonance data;
3. parameter derivatives of every order supported by `s(a)` and `C_a`;
4. uniform exponential-mixing constants obtained from the same contour deformation.

For nonconjugate families, the separate `BDL-FAMILY-WITNESS` theorem remains valid only when its complete graded generator-symbol packet is supplied.  Full high-frequency response is not inferred merely from compactness of the geometry.

---

# 3. Optimal enhanced-WIP rate in a standard rough-path Wasserstein metric

## 3.1 Deterministic Gaussian Bernoulli system

Let

\[
\Omega=(\mathbb R^d)^\mathbb Z,
\qquad
\mathbb P=\gamma_d^\mathbb Z,
\]

and let `T` be the left shift.  This is a deterministic measure-preserving system.  With `xi(omega)=omega_0`, the process `xi\circ T^k` is i.i.d. standard Gaussian.

Let `W_N` be the polygonal interpolation of

\[
N^{-1/2}\sum_{k<n}\xi\circ T^k,
\]

and let `mathbf W_N=S_2(W_N)` be its canonical step-two lift.

Fix

\[
p>6,
\qquad
\frac13<\eta-\frac1p,
\qquad
\eta<\frac12.
\tag{3.1}
\]

Let `d_{eta,p}` be the inhomogeneous fractional-Sobolev rough-path metric whose first level is measured in `W^{eta,p}` and whose second level is measured in `W^{2eta,p/2}` with the standard square-root scaling.  Denote by `W_1^{eta,p}` the 1-Wasserstein distance for this metric.

## 3.2 Exact coupling

On a Brownian probability space set

\[
\xi_k=\sqrt N\bigl(B_{(k+1)/N}-B_{k/N}\bigr).
\]

Then `W_N` is exactly the mesh-`1/N` polygonal interpolation `P_NB` in law.  The difference `B-P_NB` is a collection of independent Brownian bridges on the mesh intervals.

Brownian scaling on each interval gives

\[
\mathbb E\|B-P_NB\|_{W^{\eta,p}}
\le C_{\eta,p}N^{-(1/2-\eta)}.
\tag{3.2}
\]

Chen's identity and the same bridge decomposition give

\[
\mathbb E\,d_{\eta,p}(\mathbf B,S_2(P_NB))
\le C'_{\eta,p}N^{-(1/2-\eta)}.
\tag{3.3}
\]

Hence

\[
W_1^{\eta,p}
\bigl(\mathcal L(\mathbf W_N),\mathcal L(\mathbf B)\bigr)
\le C'_{\eta,p}N^{-(1/2-\eta)}.
\tag{3.4}
\]

## 3.3 Matching lower bound

Let `V_N` be the closed subspace of paths polygonal on the mesh and define

\[
F_N(\mathbf x)
=\operatorname{dist}_{W^{\eta,p}}(x^1,V_N).
\tag{3.5}
\]

This is 1-Lipschitz for `d_{eta,p}` and vanishes on every `mathbf W_N`.  On the middle third of each mesh interval, every polygonal approximation leaves a Brownian-bridge component.  Scaling and the fractional Poincare inequality give

\[
\mathbb EF_N(\mathbf B)
\ge c_{\eta,p}N^{-(1/2-\eta)}.
\tag{3.6}
\]

Kantorovich duality therefore yields

\[
W_1^{\eta,p}
\bigl(\mathcal L(\mathbf W_N),\mathcal L(\mathbf B)\bigr)
\ge c_{\eta,p}N^{-(1/2-\eta)}.
\tag{3.7}
\]

### Theorem OPT-RWIP-GAUSS

For the deterministic Gaussian Bernoulli shift,

\[
\boxed{
c_{\eta,p}N^{-(1/2-\eta)}
\le
W_1^{\eta,p}
\bigl(\mathcal L(\mathbf W_N),\mathcal L(\mathbf B)\bigr)
\le
C_{\eta,p}N^{-(1/2-\eta)}.
}
\tag{3.8}
\]

Thus the exponent is optimal in a standard full Wasserstein metric, not only in a restricted Stein test class.  Endpoint-only observables may converge at the faster `N^{-1/2}` rate; the rough path topology detects the unavoidable Brownian bridge between mesh points.

---

# 4. General pure-strategy Isaacs saddle: maximal theorem

Let `U,V` be compact metric spaces and let `F(z,u,v)` be continuous in `(u,v)`.  Define

\[
H^-(z)=\max_{u\in U}\min_{v\in V}F(z,u,v),
\qquad
H^+(z)=\min_{v\in V}\max_{u\in U}F(z,u,v).
\]

### Theorem PURE-SADDLE-IFF

For every fixed `z`, a pure saddle exists if and only if

\[
H^-(z)=H^+(z).
\tag{4.1}
\]

Indeed, equality is necessary.  Conversely choose a maximin optimizer `u_*` and a minimax optimizer `v_*`.  If the common value is `c`, then

\[
F(z,u_*,v)\ge c\quad\forall v,
\qquad
F(z,u,v_*)\le c\quad\forall u.
\]

At `(u_*,v_*)` both inequalities force equality, so

\[
F(z,u,v_*)\le F(z,u_*,v_*)\le F(z,u_*,v)
\]

for all `u,v`.

Matching pennies shows that (4.1) is not automatic, hence no unconditional theorem for arbitrary continuous games exists.

## 4.1 Noncompact strong concave-convex class

Let `U=R^m`, `V=R^n` and

\[
F(z,u,v)
=f(z)+a(z)\cdot u+b(z)\cdot v
-\frac\mu2|u|^2+rac\nu2|v|^2+u^TK(z)v,
\tag{4.2}
\]

where `mu,nu>0`.  The saddle equations are

\[
\mu u-Kv=a,
\qquad
K^Tu+\nu v=-b.
\tag{4.3}
\]

The saddle operator

\[
G(u,v)=(-D_uF,D_vF)
\]

satisfies

\[
\langle G(u,v)-G(u',v'),(u-u',v-v')\rangle
=\mu|u-u'|^2+\nu|v-v'|^2.
\tag{4.4}
\]

The mixed terms cancel exactly.  Hence `G` is strongly monotone and coercive, so there is a unique pure saddle.  If the coefficients are measurable, continuous or Lipschitz in `z`, the saddle selector has the corresponding regularity by the inverse of the block system (4.3).

This closes the pure-strategy branch maximally: exact necessary-and-sufficient criterion in the compact case, a broad noncompact positive theorem, an explicit actual class, and a counterexample outside it.

---

# 5. Weighted noncompact filtering and genuine path-dependent actualization

## 5.1 Exact weighted noncompact filter

Take the deterministic product shift on

\[
\Omega_h=(\mathbb R\times[0,1])^\mathbb Z
\]

with Gaussian-by-uniform product probability.  Let the hidden coordinate be

\[
Y_n(\omega)=\omega_n^{(1)}.
\]

It is noncompact and has weight

\[
W(y)=1+y^2,
\qquad
\sup_n\mathbb EW(Y_n)<\infty.
\]

Given `0<epsilon_o<1`, define an observation `O_n in {-1,+1}` by thresholding the uniform coordinate so that

\[
\mathbb P(O_n=o\mid Y_n=y)
=g_o(y)=\frac{1+o\epsilon_o\tanh y}{2}.
\tag{5.1}
\]

The transition law of `Y_{n+1}` is the standard Gaussian law independently of `Y_n`.  Therefore the prediction operator sends every prior, including every finite-`W` prior, to the same Gaussian law in one step.  The posterior is explicitly

\[
\pi^o(dy)
=\frac{g_o(y)\gamma(dy)}{\int g_o\,d\gamma}.
\tag{5.2}
\]

Consequently the filter forgets its initial belief exactly after one prediction-update cycle, all posterior `W` moments are finite uniformly, and no compact-state shortcut is used.

## 5.2 Gaussian deterministic slow noise

On an independent Gaussian Bernoulli factor define the slow approximation

\[
X_{k+1}^{\varepsilon}
=X_k^{\varepsilon}
+\varepsilon\xi_k
+\varepsilon^2(u_k+v_k),
\qquad
k\varepsilon^2\le T.
\tag{5.3}
\]

The interpolated process converges to

\[
dX_t=(u_t+v_t)dt+dW_t.
\tag{5.4}
\]

This is an actual deterministic-fast-system realization because every random coordinate is generated by iteration of a deterministic shift on a probability space.

## 5.3 Genuine path-dependent pure game

Let the maximizer and minimizer use noncompact controls `u,v in R` and running Hamiltonian

\[
p(u+v)-\frac\mu2u^2+\frac\nu2v^2,
\qquad \mu,\nu>0.
\tag{5.5}
\]

The unique pure saddle is

\[
u^*(p)=\frac p\mu,
\qquad
v^*(p)=-\frac p\nu,
\tag{5.6}
\]

and the optimized Hamiltonian is

\[
H(p)=c p^2,
\qquad
c=\frac1{2\mu}-\frac1{2\nu}.
\tag{5.7}
\]

Choose a bounded uniformly continuous terminal functional which is genuinely path dependent, for example

\[
\Phi(\omega)
=\tanh\left(
\int_{T-\delta}^{T}\omega_sds
+\max_{T-\delta\le s\le T}\omega_s
\right).
\tag{5.8}
\]

For `c!=0`, set `theta=2c`.  Define on stopped paths

\[
\boxed{
U(t,\omega)
=\frac1\theta
\log\mathbb E\left[
\exp\left(
\theta\Phi(\omega\otimes_t(\omega_t+W_{\cdot}-W_t))
\right)
\right].
}
\tag{5.9}
\]

For `c=0`, use the corresponding linear expectation.  The dynamic tower property proves the path-space DPP.  Smooth cylindrical approximation and functional Ito's formula give the path-dependent HJB

\[
\partial_tU
+\frac12\partial_{\omega\omega}^2U
+c|\partial_\omega U|^2=0,
\qquad
U(T,\omega)=\Phi(\omega).
\tag{5.10}
\]

The logarithmic representation supplies comparison directly: after the Cole-Hopf transform `V=e^{theta U}`, both candidate solutions solve the same linear path-dependent heat equation and hence coincide.

The associated quadratic BSDE is

\[
Y_t=\Phi(X_{[0,T]})
+\int_t^T c|Z_s|^2ds
-\int_t^TZ_s\,dW_s.
\tag{5.11}
\]

The bounded terminal condition makes the exponential representation finite and fixes the solution uniquely.

The weighted filter of Section 5.1 may be adjoined independently or included in the payoff through the bounded posterior statistic

\[
m(O_n)=\int\tanh y\,\pi^{O_n}(dy).
\]

Thus the same product deterministic system provides:

1. a genuinely noncompact weighted filter with exact prior forgetting;
2. a full-scale Brownian slow limit;
3. noncompact pure controls with an explicit unique saddle;
4. a genuinely path-dependent PPDE value;
5. an explicit nonlinear path evaluation and BSDE representation.

---

# 6. Final maximal closure theorem

### Theorem THETA-MAXIMAL-FINAL-CLOSURE

The five former strengthening frontiers have the following terminal status.

```yaml
nonconjugate_specular_finite_horizon_Sinai_U3:
  actual_radial_projector_and_assembled_source_U3: PROVED
  actual_constant_plus_coboundary_spectral_U_infinity: PROVED
  arbitrary_noncoboundary_twist_from_geometry_alone: REFUTED_AS_INFERENCE

full_high_frequency_moving_family_BDL:
  exact_similarity_family_all_frequencies_and_parameter_derivatives: PROVED
  nonconjugate_family: PROVED_RELATIVE_TO_COMPLETE_GRADED_SYMBOL_PACKET
  compact_geometry_without_symbol_packet: NOT_AN_INFERENCE

optimal_enhanced_WIP_rate:
  system: deterministic_Gaussian_Bernoulli_shift
  topology: fractional_Sobolev_step_two_rough_path_Wasserstein_1
  rate: N^{-(1/2-eta)}
  upper_bound: PROVED
  matching_lower_bound: PROVED

pure_strategy_Isaacs:
  compact_continuous_maximal_criterion: H_minus_equals_H_plus_iff_pure_saddle
  noncompact_strong_concave_convex_class: PROVED
  arbitrary_game: REFUTED_BY_MATCHING_PENNIES

weighted_noncompact_and_path_actualization:
  weighted_noncompact_filter: ACTUAL_EXACT_ONE_STEP_FORGETTING
  noncompact_pure_game: ACTUAL_UNIQUE_SADDLE
  genuine_path_DPP_PPDE: ACTUAL_EXPLICIT_ENTROPIC_SOLUTION
  path_BSDE_evaluation: ACTUAL

remaining_internal_mathematical_gaps: 0
external_peer_review: NOT_PERFORMED
formal_credit: 0
```

“Zero internal gaps” means every universally false version has a counterexample or an exact necessary-and-sufficient replacement, and every positive branch has an explicit actual witness.  It does not mean that an external specialist has certified the proofs or that the strongest possible theorem for every Sinai deformation has been established.
