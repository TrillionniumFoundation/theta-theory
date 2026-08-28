# Topology-optimal enhanced WIP rate

## 0. Why “optimal” must name a topology

There is no topology-free optimal functional central-limit rate.  Endpoint
metrics, uniform path metrics, Hölder metrics, fractional Sobolev metrics, and
rough-path metrics resolve different Brownian scales.  This note fixes a
separable step-two fractional Sobolev rough-path topology and proves matching
upper and lower exponents for the actual four-branch Bernoulli realization.

The main export is

```text
P3-RWIP-OPTIMAL-WETA-P.
```

---

## 1. Rough Sobolev state space

Let `p>4` and

\[
\frac1p<\eta<\frac12.
\tag{1.1}
\]

For a continuous path `x:[0,1]->R^d`, define the Slobodetsky norm

\[
\|x\|_{W^{\eta,p}}^p
=
\int_0^1|x_t|^pdt
+
\int_0^1\int_0^1
\frac{|x_t-x_s|^p}{|t-s|^{1+\eta p}}\,dsdt.
\tag{1.2}
\]

For a step-two geometric rough path

\[
\mathbf x=(x,\mathbb x),
\]

use

\[
d_{\eta,p}(\mathbf x,\mathbf y)
=
\|x-y\|_{W^{\eta,p}}
+
\|\mathbb x-\mathbb y\|_{W^{2\eta,p/2}}^{1/2}.
\tag{1.3}
\]

Let `d_KR^(eta,p)` be the Kantorovich--Rubinstein distance over real
functionals that are one-Lipschitz for (1.3) and bounded by one.

---

## 2. Enriched random walk

Let `xi_1,xi_2,...` be iid `R^d`-valued random variables satisfying

\[
\mathbb E\xi_1=0,
\qquad
\mathbb E(\xi_1\xi_1^T)=\Sigma,
\qquad
\mathbb E|\xi_1|^{p+3}<\infty.
\tag{2.1}
\]

Let `W_N` be the affine interpolation of

\[
N^{-1/2}\sum_{j=1}^k\xi_j
\]

at times `k/N`, and let `mathbb W_N` be its canonical iterated integral.  Write

\[
\mathbf W_N=(W_N,\mathbb W_N).
\]

Let `mathbf B_Sigma` be enhanced Brownian motion with covariance `Sigma`.

---

## 3. Upper bound

### Theorem 3.1 (rough Sobolev Berry--Esseen rate)

Under (1.1)--(2.1),

\[
\boxed{
 d_{KR}^{\eta,p}
 (\mathcal L(\mathbf W_N),\mathcal L(\mathbf B_\Sigma))
 \le C_{p,\eta,d,\xi}
 N^{-(1/2-\eta)}.
}
\tag{3.1}
\]

#### Proof

Split the comparison into

\[
\mathbf W_N
\longleftrightarrow
\mathbf B_\Sigma^{(N)}
\longleftrightarrow
\mathbf B_\Sigma,
\tag{3.2}
\]

where `B_Sigma^(N)` is the affine interpolation of Brownian motion on the same
mesh, with its canonical lift.

**Step 1: increment replacement.**  Apply the finite-dimensional
Stein--Lindeberg replacement one increment at a time to smooth cylindrical
approximations of a `d_(eta,p)`-Lipschitz functional.  Discrete
Burkholder inequalities control both the first level and the antisymmetric
second level.  The sum of the third-order replacement remainders is

\[
O(N^{-1/2}).
\tag{3.3}
\]

The smoothing error is absorbed by the fractional Sobolev moment bound.  This
is the enriched Donsker estimate in the Stein--Dirichlet rough-path method.

**Step 2: Brownian bridge interpolation.**  On one mesh interval of length
`h=1/N`, a Brownian bridge increment has size `h^(1/2)`.  Scaling (1.2) gives

\[
\mathbb E
\|B_\Sigma^{(N)}-B_\Sigma\|_{W^{\eta,p}}
\le C h^{1/2-\eta}.
\tag{3.4}
\]

The missing Lévy-area on the interval has size `h`; after the square root in
(1.3), the same exponent appears:

\[
\mathbb E
\|\mathbb B_\Sigma^{(N)}-\mathbb B_\Sigma\|_{W^{2\eta,p/2}}^{1/2}
\le C h^{1/2-\eta}.
\tag{3.5}
\]

Combining (3.3)--(3.5), and observing that
`N^{-1/2} <= N^{-(1/2-eta)}`, proves (3.1).

### Remark 3.2

The proof uses the same scale as the quantitative rough Donsker theorem of
Coutin--Decreusefond.  The exponent loss is not a mixing loss; it is the cost
of resolving Brownian bridges in `W^(eta,p)`.

---

## 4. Matching lower bound

For a continuous path `x`, define the midpoint bridge defect

\[
D_{k,N}(x)
=
x_{(k+1/2)/N}
-
\frac{x_{k/N}+x_{(k+1)/N}}2,
\tag{4.1}
\]

and

\[
F_N(x)
=
N^{\eta-1/p}
\left(
\sum_{k=0}^{N-1}|D_{k,N}(x)|^p
\right)^{1/p}.
\tag{4.2}
\]

### Lemma 4.1 (uniform discrete trace bound)

There is `C=C(eta,p)` such that

\[
|F_N(x)-F_N(y)|
\le C\|x-y\|_{W^{\eta,p}}
\tag{4.3}
\]

for every `N`.

#### Proof

On each mesh interval, write the midpoint defect as an average of two
increments from the left and right half-intervals.  Jensen's inequality and
the local part of the double integral in (1.2) give

\[
N^{\eta p-1}
\sum_k|D_{k,N}(x-y)|^p
\le C\|x-y\|_{W^{\eta,p}}^p.
\]

Taking the `p`th root gives (4.3).

Every affine mesh path satisfies

\[
F_N(W_N)=0.
\tag{4.4}
\]

For Brownian motion, the defects are independent centered Gaussians with
variance comparable to `1/N`; therefore

\[
\mathbb EF_N(B_\Sigma)
\ge c_{p,\eta,\Sigma}N^{-(1/2-\eta)}
\tag{4.5}
\]

when `Sigma` has a nonzero direction.

### Theorem 4.2 (optimality)

For every law supported on affine paths on the `N`-mesh,

\[
\boxed{
 d_{KR}^{\eta,p}
 (\mathcal L(\mathbf X_N),\mathcal L(\mathbf B_\Sigma))
 \ge cN^{-(1/2-\eta)}.
}
\tag{4.6}
\]

#### Proof

Normalize a truncation of `F_N/C` to be a bounded one-Lipschitz test for the
rough metric.  Use (4.4)--(4.5).  The rough metric dominates its first-level
component, so no second-level coupling can remove the lower bound.

Combining Theorems 3.1 and 4.2 proves that `1/2-eta` is the optimal exponent in
the declared topology.

---

## 5. Endpoint rate and a second optimality statement

If a scalar projection `e dot xi_1` has nonzero third cumulant, the usual
one-dimensional Edgeworth/Berry--Esseen obstruction gives

\[
\sup_{\|f\|_{C_b^3}\le1}
\left|
\mathbb Ef(e\cdot W_N(1))
-
\mathbb Ef(e\cdot B_\Sigma(1))
\right|
\asymp N^{-1/2}.
\tag{5.1}
\]

Thus the endpoint smooth-test exponent is exactly `1/2`, while the full rough
Sobolev path exponent is exactly `1/2-eta`.  These are compatible because the
path topology sees unresolved Brownian bridges.

---

## 6. Actual four-branch realization

For the Paper-I four-branch full-branch map, branch labels are iid under
Lebesgue measure with probabilities `w_i(a)`.  Let

\[
\xi_a(i)\in\mathbb R^d,
\qquad
\sum_iw_i(a)\xi_a(i)=0,
\tag{6.1}
\]

and assume the covariance is uniformly nondegenerate.  The increments are
bounded and depend smoothly on `a`; hence all constants in Theorem 3.1 are
uniform on the compact parameter interval.  Therefore

\[
\sup_a d_{KR}^{\eta,p}
(\mathcal L(\mathbf W_{N,a}),
 \mathcal L(\mathbf B_{\Sigma(a)}))
\le CN^{-(1/2-\eta)}.
\tag{6.2}
\]

The lower bound is uniform on any subinterval on which one covariance
direction remains bounded away from zero.

This closes the actual optimal-rate blocker without asserting an unavailable
rate for every hyperbolic system.

---

## 7. Transfer to martingale--coboundary systems

Suppose a stationary dynamical observable has

\[
v=m+\chi-\chi\circ T,
\tag{7.1}
\]

where `m` is a martingale difference.  Let `r_m(N)` be a quantitative enriched
martingale approximation rate in (1.3).  Maximal inequalities give the
coboundary contribution `O(N^{-1/2})` when `chi in L^p`.  Hence

\[
 d_{KR}^{\eta,p}(\mathbf W_N,\mathbf B)
\le C\left[
N^{-(1/2-\eta)}+r_m(N)+N^{-1/2}\|\chi\|_p
\right].
\tag{7.2}
\]

There is no universal optimal exponent unless `r_m` and the topology are
specified.  Formula (7.2) is the maximal correctly typed general theorem.

---

## 8. Nonautonomous block choice

Put

\[
\delta=\frac12-\eta>0.
\]

If a slow-fast proof uses block length `m_epsilon` and approximately
`epsilon^{-2}/m_epsilon` blocks, the total frozen-WIP error is controlled when

\[
\frac{\epsilon^{-2}}{m_\epsilon}
 m_\epsilon^{-\delta}\to0.
\tag{8.1}
\]

For `m_epsilon=epsilon^{-kappa}`, this is

\[
\boxed{
\frac{2}{1+\delta}<\kappa<2.
}
\tag{8.2}
\]

The interval is nonempty for every `delta>0`.  Thus the optimal rate supplies
an explicit full-scale K2 block window.

---

## 9. Export

```yaml
id: P3-RWIP-OPTIMAL-WETA-P
topology:
  first_level: W_eta_p
  second_level: W_2eta_p_over_2_square_root
range: 1/p < eta < 1/2
actual_upper_exponent: 1/2-eta
piecewise_linear_lower_exponent: 1/2-eta
endpoint_smooth_exponent: 1/2
actual_system: four_branch_Bernoulli_symbol_process
nonautonomous_block_window: 2/(1+1/2-eta) < kappa < 2
forbidden_upgrade:
  - topology_free_optimal_rate
  - qualitative_WIP_to_quantitative_rate
```

## Primary reference for the upper-rate method

L. Coutin and L. Decreusefond, *Stein's method for rough paths*,
arXiv:1707.01269.
