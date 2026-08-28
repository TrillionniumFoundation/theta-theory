# Topology- and test-class-optimal enhanced WIP rate

## 0. Why “optimal” must name both topology and tests

There is no topology-free or test-class-free optimal functional central-limit
rate.  Endpoint metrics, bounded-Lipschitz path metrics, Hölder metrics,
fractional-Sobolev metrics, and smooth Stein test distances are different
objects.  Moreover, the quantitative Stein theorem for enriched walks does
not estimate every Lipschitz functional: it uses a regular Stein--Dirichlet
subclass whose pulled-back second derivative has a controlled Lipschitz
modulus.

This note fixes exactly that quantitative distance and proves matching upper
and lower exponents for the actual four-branch Bernoulli realization.  No
full Lipschitz--Kantorovich rate is claimed.

The main export remains

```text
P3-RWIP-OPTIMAL-WETA-P
```

and now means **optimal in the declared fractional-Sobolev Stein--Dirichlet
test distance**.

---

## 1. Rough Sobolev state space

Choose

\[
p>6,
\qquad
\frac13<\eta-\frac1p,
\qquad
\eta<\frac12.
\tag{1.1}
\]

The Sobolev embedding exponent `eta-1/p` is therefore above the step-two rough
threshold `1/3`, while Brownian paths still belong to `W^(eta,p)`.

For a step-two logarithmic rough path

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
\tag{1.2}
\]

Let `S_2` denote the step-two signature map and let

\[
\widetilde F=F\circ S_2.
\]

---

## 2. Stein--Dirichlet test class

Let `Sigma_(eta,p)` be the class of functions `F` on the rough Sobolev space
such that:

1. `F` is one-Lipschitz for (1.2) and bounded by one;
2. the pulled-back functional `F tilde` is twice differentiable in the
   Cameron--Martin directions;
3. its second derivative satisfies the normalized Hilbert--Schmidt Lipschitz
   condition used in the Stein--Dirichlet theorem;
4. smooth cylindrical approximants obey the same bounds.

Write

\[
\|F\|_{\Sigma_{\eta,p}}
\]

for the maximum of these normalized constants and define

\[
\boxed{
 d_{SD}^{\eta,p}(\mu,\nu)
 =
 \sup_{\|F\|_{\Sigma_{\eta,p}}\le1}
 \left|\mu(F)-\nu(F)\right|.
}
\tag{2.1}
\]

This is the exact test distance used below.  It is weaker than the full
bounded-Lipschitz Kantorovich distance; the distinction is permanent.

---

## 3. Enriched random walk

Let `xi_1,xi_2,...` be iid `R^d`-valued random variables satisfying

\[
\mathbb E\xi_1=0,
\qquad
\mathbb E(\xi_1\xi_1^T)=\Sigma,
\qquad
\mathbb E|\xi_1|^{p+3}<\infty.
\tag{3.1}
\]

Let `W_N` be the affine interpolation of

\[
N^{-1/2}\sum_{j=1}^k\xi_j
\]

at times `k/N`, and let `mathbb W_N` be its canonical iterated integral.  Put

\[
\mathbf W_N=(W_N,\mathbb W_N).
\]

Let `mathbf B_Sigma` be enhanced Brownian motion with covariance `Sigma`.

---

## 4. Quantitative upper bound

### Theorem 4.1 (Stein--Dirichlet rough rate)

Under (1.1) and (3.1),

\[
\boxed{
 d_{SD}^{\eta,p}
 (\mathcal L(\mathbf W_N),\mathcal L(\mathbf B_\Sigma))
 \le C_{p,\eta,d,\xi}
 N^{-(1/2-\eta)}.
}
\tag{4.1}
\]

#### Proof

Let `B_Sigma^(N)` be the affine interpolation of Brownian motion on the same
mesh, with its canonical lift.  Decompose

\[
\mathbf W_N
\longleftrightarrow
\mathbf B_\Sigma^{(N)}
\longleftrightarrow
\mathbf B_\Sigma.
\tag{4.2}
\]

For the first comparison, pull `F` back by the signature map and apply the
finite-dimensional Stein--Dirichlet replacement.  The normalized second-
derivative Lipschitz condition defining `Sigma_(eta,p)` controls the
non-Gaussian remainder, giving

\[
\sup_{\|F\|_{\Sigma_{\eta,p}}\le1}
\left|
\mathbb EF(\mathbf W_N)
-
\mathbb EF(\mathbf B_\Sigma^{(N)})
\right|
\le CN^{-1/2}.
\tag{4.3}
\]

For the second comparison, the Brownian bridge on a mesh interval of length
`h=1/N` has first-level Sobolev size `h^(1/2-eta)`.  Its missing Lévy-area has
size `h`; after the square root in (1.2), the same exponent appears.  Hence

\[
\mathbb E
d_{\eta,p}
(\mathbf B_\Sigma^{(N)},\mathbf B_\Sigma)
\le CN^{-(1/2-\eta)}.
\tag{4.4}
\]

Lipschitz continuity of `F`, (4.3), and (4.4) prove (4.1).

### Remark 4.2

The restriction to `Sigma_(eta,p)` is essential in the present proof.  The
finite-dimensional reduction requires regularity of the pulled-back second
derivative.  The manuscript does not replace this with an unsupported full
Lipschitz--KR estimate.

---

## 5. A matching smooth lower test

Let

\[
D_{k,N}(x)
=
x_{(k+1/2)/N}
-
\frac{x_{k/N}+x_{(k+1)/N}}2.
\tag{5.1}
\]

Choose an even nonnegative function

\[
\phi\in C_b^3(\mathbb R),
\qquad
\phi(0)=0,
\]

such that `E phi(Z)>0` for a nondegenerate centered Gaussian `Z`.  For a fixed
nonzero covariance direction `e`, define

\[
F_N(\mathbf x)
=
c_0N^{-3/2+\eta}
\sum_{k=0}^{N-1}
\phi\left(
\sqrt N\,e\cdot D_{k,N}(\pi_1\mathbf x)
\right),
\tag{5.2}
\]

followed, if necessary, by a fixed smooth truncation outside `[-1,1]`.

### Lemma 5.1 (uniform Stein-test norm)

The constant `c_0>0` can be chosen independently of `N` so that

\[
\boxed{
\|F_N\|_{\Sigma_{\eta,p}}\le1
\quad\text{for every }N.
}
\tag{5.3}
\]

#### Proof

Each midpoint defect is a Cameron--Martin linear functional supported on one
mesh interval.  After multiplication by `sqrt N`, its Cameron--Martin norm is
a constant independent of `N`, and the `N` supports are orthogonal.  The
first, second, and third derivatives of (5.2) are diagonal sums of these
orthogonal directions, multiplied respectively by the bounded derivatives of
`phi`.  Their operator and Hilbert--Schmidt bounds are controlled by

\[
N^{-3/2+\eta}\sqrt N
=N^{-1+\eta}\le1.
\]

The same disjoint-interval calculation, or the fractional discrete trace
inequality, gives a uniform Lipschitz bound in (1.2).  A fixed `c_0` normalizes
all constants simultaneously.

Every affine path on the `N`-mesh satisfies

\[
F_N(\mathbf W_N)=0.
\tag{5.4}
\]

For Brownian motion, the `N` midpoint bridge defects are independent and

\[
\sqrt N\,D_{k,N}(B_\Sigma)
\]

has one fixed nondegenerate Gaussian law in the direction `e`.  Therefore

\[
\boxed{
\mathbb EF_N(\mathbf B_\Sigma)
=c_1N^{-(1/2-\eta)}
}
\tag{5.5}
\]

for some `c_1>0`.

### Theorem 5.2 (optimality in the declared distance)

For the affine enriched walk,

\[
\boxed{
 cN^{-(1/2-\eta)}
\le
 d_{SD}^{\eta,p}
 (\mathcal L(\mathbf W_N),\mathcal L(\mathbf B_\Sigma))
\le
 CN^{-(1/2-\eta)}.
}
\tag{5.6}
\]

#### Proof

The upper bound is Theorem 4.1.  The lower bound uses the admissible test
`F_N` from Lemma 5.1 and (5.4)--(5.5).

Thus `1/2-eta` is the exact optimal exponent and rate order in the declared
Stein--Dirichlet rough test distance.

---

## 6. Endpoint rate and the full-Lipschitz boundary

If a scalar projection `e dot xi_1` has nonzero third cumulant, the ordinary
smooth endpoint-test distance has the separate order

\[
N^{-1/2}.
\tag{6.1}
\]

The slower rough path order in (5.6) comes from unresolved Brownian bridges.

No exact rate is claimed here for the full bounded-Lipschitz
Kantorovich--Rubinstein distance on the entire rough Sobolev space.  That is a
strictly stronger metric problem.  The absence of such a theorem is not hidden
inside the export `P3-RWIP-OPTIMAL-WETA-P`.

---

## 7. Actual four-branch realization

For the Paper-I four-branch full-branch map, branch labels are iid under
Lebesgue measure with probabilities `w_i(a)`.  Let

\[
\xi_a(i)\in\mathbb R^d,
\qquad
\sum_iw_i(a)\xi_a(i)=0,
\tag{7.1}
\]

and assume the covariance is uniformly nondegenerate.  The increments are
bounded and depend smoothly on `a`; all constants in Theorems 4.1 and 5.2 are
therefore uniform on the compact parameter interval.  Hence

\[
\boxed{
\sup_a
d_{SD}^{\eta,p}
(\mathcal L(\mathbf W_{N,a}),
 \mathcal L(\mathbf B_{\Sigma(a)}))
\asymp N^{-(1/2-\eta)}.
}
\tag{7.2}
\]

The lower constant is uniform on any subinterval on which one covariance
direction remains bounded away from zero.

---

## 8. Transfer to martingale--coboundary systems

Suppose a stationary dynamical observable has

\[
v=m+\chi-\chi\circ T,
\tag{8.1}
\]

where `m` is a martingale difference.  Let `r_m(N)` be a quantitative enriched
martingale approximation rate in the same test distance.  Maximal inequalities
give the coboundary contribution `O(N^{-1/2})` when `chi in L^p`.  Thus

\[
 d_{SD}^{\eta,p}(\mathbf W_N,\mathbf B)
\le C\left[
N^{-(1/2-\eta)}+r_m(N)+N^{-1/2}\|\chi\|_p
\right].
\tag{8.2}
\]

There is no universal optimal exponent unless the martingale rate, topology,
and test class are all specified.

---

## 9. Nonautonomous block choice

Put

\[
\delta=\frac12-\eta>0.
\]

If a slow-fast proof uses block length `m_epsilon` and approximately
`epsilon^{-2}/m_epsilon` blocks, the accumulated frozen-WIP error is controlled
when

\[
\frac{\epsilon^{-2}}{m_\epsilon}
 m_\epsilon^{-\delta}\to0.
\tag{9.1}
\]

For `m_epsilon=epsilon^{-kappa}`, this is

\[
\boxed{
\frac{2}{1+\delta}<\kappa<2.
}
\tag{9.2}
\]

The interval is nonempty for every `delta>0`.

---

## 10. Export

```yaml
id: P3-RWIP-OPTIMAL-WETA-P
topology:
  first_level: W_eta_p
  second_level: W_2eta_p_over_2_square_root
  rough_embedding: eta_minus_one_over_p_greater_than_one_third
test_distance: Stein_Dirichlet_Sigma_eta_p
range:
  - p_greater_than_6
  - one_third_less_than_eta_minus_one_over_p
  - eta_less_than_one_half
actual_upper_exponent: one_half_minus_eta
actual_lower_exponent: one_half_minus_eta
actual_system: four_branch_Bernoulli_symbol_process
nonautonomous_block_window: 2/(1+1/2-eta) < kappa < 2
forbidden_upgrade:
  - full_Lipschitz_KR_exact_rate
  - topology_or_test_class_free_optimal_rate
  - qualitative_WIP_to_quantitative_rate
```

## Primary quantitative input

L. Coutin and L. Decreusefond, *Stein's method for rough paths*,
arXiv:1707.01269.  Its finite-dimensional rate is stated for the regular
Stein--Dirichlet class `Sigma_(eta,p)`, not for every Lipschitz test.
