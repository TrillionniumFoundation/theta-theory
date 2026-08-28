# Doob-selected rough homogenization and nonlinear theta-expectations from deterministic fast dynamics

## Abstract

We study deterministic fast systems whose frozen transfer operators admit the
pressure, covariance, and common-space response package of Paper II.  An
external cotangent/control signal first selects a normalized Doob kernel; the
selection is made before any limiting HJB solution is introduced.  Under a
uniform martingale--rough packet we prove an enhanced weak invariance principle,
including its area anomaly, and a nonautonomous homogenization theorem for
slowly varying parameters.  A quantitative compatibility condition between the
enhanced-WIP modulus and the block scale is stated explicitly.  Qualitative
uniform WIP alone yields a cofinal diagonal result, not automatically a full
scale limit.

The homogenized coefficients define monotone dynamic-programming operators.
Consistency and comparison give an HJB limit and a time-consistent nonlinear
semigroup, called the theta-expectation.  Gradient-dependent finite-response
ports may produce nonconvex Hamiltonians, so the semigroup need not be
subadditive.  For the four-branch system of Papers I--II, locally constant
observables give an actual Bernoulli/Doob model.  Its slowly varying version is
a bounded martingale triangular array, so a direct predictable-characteristics
argument gives the full-scale rough limit without asserting an unproved rough
Berry--Esseen exponent.

---

## 1. Frozen microscopic data and the no-feedback rule

Let `K` be a compact slow/cotangent window and let

\[
\theta=(x,p,\zeta)\in\Theta_K
\]

collect the slow state, an external cotangent signal, and an optional tilt or
control.  Paper II provides a fixed common operator space and a family of
positive twisted transfer operators

\[
L_\theta.
\]

Let `lambda_theta>0` and `h_theta>0` be the leading eigenvalue and right
eigenfunction.  The normalized Doob operator is

\[
\mathsf P_\theta f
=
\lambda_\theta^{-1}h_\theta^{-1}
L_\theta(h_\theta f).
\tag{1.1}
\]

It preserves constants and has invariant law `mu_theta^D`.

### Principle 1.1 (causal order)

The objects in (1.1) are constructed from frozen microscopic data and the
external signal `theta`.  Only after homogenization and dynamic programming is
`p` identified with a test-function or value-function gradient.  No unknown
HJB solution is used to define `L_theta`, `h_theta`, or `P_theta`.

---

## 2. The uniform martingale--rough packet

Let `v_theta` be a centered `R^d`-valued fast observable.

### Assumption 2.1 (UM packet)

Uniformly for `theta in Theta_K`:

1. **UM1, physical clock.**  The parameter bundle is compact and chambered;
   collision and physical-time normalizations are fixed.
2. **UM2, moments.**  For some `q>4`,
   \[
   \sup_\theta\|v_\theta\|_{L^q(\mu_\theta^D)}<\infty.
   \]
3. **UM3, Gordin decomposition.**  There are `chi_theta` and martingale
   differences `m_theta` such that
   \[
   v_\theta=m_\theta+\chi_\theta\circ T_\theta-\chi_\theta.
   \tag{2.1}
   \]
4. **UM4, bracket.**  Conditional quadratic variations converge uniformly to
   `Sigma_theta`.
5. **UM5, second level.**  The iterated sums converge with deterministic area
   anomaly `Gamma_theta`.
6. **UM6, maximal coboundary control.**  The rescaled maximum of the
   coboundary in (2.1) vanishes in probability uniformly.
7. **UM7, initial laws.**  A quantitative forgetting estimate transfers the
   result from the invariant law to the declared admissible initial laws.
8. **UM8, parameter regularity.**  `Sigma_theta`, `Gamma_theta`, the Poisson
   solution, and the martingale decomposition have a common modulus.
9. **UM9, enhanced-WIP modulus or direct triangular characteristics.**  For
   the block route there is a deterministic `eta(N)->0` controlling the frozen
   enhanced-law approximation.  Alternatively, the actual nonautonomous array
   may satisfy a direct martingale-characteristics theorem.
10. **UM10, switching and uniqueness.**  Frozen generators have a switching
    modulus, and the limiting martingale problem or RDE is unique.

### Proposition 2.2 (spectral sufficient conditions)

Suppose `P_theta` has a uniform spectral gap on a Banach algebra embedded in
`L^q`, the observable and its tensor square belong uniformly to that algebra,
and the Paper-II common-space parameter modulus holds.  Then UM2--UM8 follow.

#### Proof

On the centered space define

\[
\chi_\theta
=\sum_{n\ge1}\mathsf P_\theta^nv_\theta.
\tag{2.2}
\]

The spectral gap gives convergence and a uniform norm bound.  Since
`P_theta(chi_theta circ T_theta)=chi_theta`, the increment

\[
m_\theta=v_\theta+\chi_\theta-\chi_\theta\circ T_\theta
\]

has zero conditional expectation and gives (2.1).  Maximal inequalities for
the martingale and the bounded Poisson term yield UM6.  Apply the same
construction to the centered matrix observable
`m_theta otimes m_theta-Sigma_theta` and to the antisymmetric second-level
observable; this yields UM4 and UM5.  The resolvent identity

\[
R_\theta-R_{\theta'}
=R_\theta(\mathsf P_\theta-
\mathsf P_{\theta'})R_{\theta'}
\]

gives UM8.  Exponential loss of memory gives UM7.

UM9 remains a separate quantitative or direct-characteristics input; a scalar
CLT does not supply it.

---

## 3. Frozen enhanced WIP

For a frozen parameter, define

\[
W_N^\theta(t)
=N^{-1/2}\sum_{j< Nt}v_\theta\circ T_\theta^j,
\tag{3.1}
\]

and

\[
\mathbb W_N^\theta(t)
=N^{-1}\sum_{0\le i<j<Nt}
 v_\theta\circ T_\theta^i\otimes
 v_\theta\circ T_\theta^j.
\tag{3.2}
\]

### Theorem 3.1 (uniform enhanced WIP)

Under UM1--UM9 in the frozen-modulus route, for every admissible `p>2`,

\[
(W_N^\theta,\mathbb W_N^\theta)
\Longrightarrow
(W^\theta,\mathbb W^\theta+t\Gamma_\theta)
\tag{3.3}
\]

uniformly in `theta`, in the `p`-variation rough-path topology.  The Brownian
covariance is `Sigma_theta`.

#### Proof

Replace `v_theta` by the martingale difference in (2.1); UM6 removes the first
level coboundary.  Discrete integration by parts writes the second-level
coboundary terms as endpoint terms plus an ergodic average, whose limit is
`Gamma_theta`.  The martingale functional CLT with `q>4` gives joint first- and
second-level convergence and tightness.  UM4 and UM5 identify the bracket and
area.  UM7 transfers the law, and the UM9 modulus makes the approximation
uniform in the parameter.

### Lemma 3.2 (qualitative versus full-scale use)

Qualitative uniform convergence in (3.3), without a compatible modulus, always
allows a cofinal sequence of microscopic scales along which a diagonal block
argument works.  It does not by itself imply convergence for every
`epsilon->0`.

#### Proof

Choose frozen lengths `N_k` for which the uniform enhanced-law error is below
`2^{-k}` and then choose a decreasing cofinal sequence `epsilon_k` whose block
lengths equal `N_k` and whose physical block durations vanish.  This gives a
diagonal subsequence.  Extending the conclusion to all small `epsilon` requires
control of the gaps between the chosen `N_k`, equivalently a usable modulus or
a direct triangular-array characteristic theorem.

---

## 4. Nonautonomous rough homogenization

Let

\[
\theta_t^\varepsilon
=\Theta(X_t^\varepsilon,p_t^\varepsilon,\zeta_t^\varepsilon).
\]

For the block route, freeze the parameter on blocks of `m_epsilon` fast steps.
Put

\[
h_\varepsilon=\varepsilon^2m_\varepsilon,
\qquad
N_\varepsilon\asymp T/h_\varepsilon.
\]

### Assumption 4.1 (compatible block scale)

\[
m_\varepsilon\to\infty,
\qquad h_\varepsilon\to0,
\tag{4.1}
\]

and

\[
N_\varepsilon\eta(m_\varepsilon)	o0.
\tag{4.2}
\]

The total freezing, switching, initial-law, and remainder errors over all
blocks also tend to zero.  A typical local freezing error is `O(h^{3/2})`, so
its total is `O(h^{1/2})`.

### Theorem 4.2 (Doob-selected nonautonomous homogenization)

Assume either the compatible block route (4.1)--(4.2) or the direct
triangular-characteristics route in UM9.  Then the slow process converges to
the unique solution of

\[
dX_t
=\bar b(X_t,p_t,\zeta_t)\,dt
+\sigma(X_t,p_t,\zeta_t)\,dW_t
+b_\Gamma(X_t,p_t,\zeta_t)\,dt,
\tag{4.3}
\]

where

\[
\sigma\sigma^T=\Sigma
\]

and `b_Gamma` is the deterministic bracket correction obtained by applying the
antisymmetric area anomaly to the commutators of the slow vector fields.

#### Proof

In the block route, Theorem 3.1 replaces the frozen deterministic driver by its
Brownian rough path.  Condition (4.2) makes the accumulated frozen-law error
vanish.  UM8 and the slow-path modulus control parameter freezing.  Rough-path
continuity transports enhanced-driver convergence to the slow path.

In the direct route, the slowly varying martingale array satisfies conditional
Lindeberg, its predictable bracket converges to the time integral of `Sigma`,
and its antisymmetric predictable second level converges to the integral of
`Gamma`.  The martingale rough-path FCLT then gives the same driver.  Tightness,
characteristic identification, and UM10 give the unique global limit.

---

## 5. An actual Bernoulli--Doob realization

For the four-branch family of Paper I, the branch itinerary under its selected
Bernoulli/Gibbs law has probabilities `w_i(a)`.  Let `zeta` be a compact tilt
and let `c_i in R^d` be branch increments.  The locally constant twisted
potential gives Doob probabilities

\[
p_i(a,\zeta)
=
\frac{w_i(a)e^{\zeta\cdot c_i}}
     {\sum_jw_j(a)e^{\zeta\cdot c_j}}.
\tag{5.1}
\]

For frozen parameters, branch symbols are i.i.d. with probabilities (5.1).  Set

\[
v_{a,\zeta}(i)
=c_i-\sum_jp_j(a,\zeta)c_j.
\]

### Proposition 5.1 (actual uniform rough packet)

On compact `(a,zeta)` windows:

1. all moments are uniformly bounded;
2. the martingale-coboundary decomposition is trivial (`chi=0`);
3. the covariance is
   \[
   \Sigma(a,\zeta)=\sum_ip_i v_i\otimes v_i;
   \]
4. the antisymmetric area anomaly is zero;
5. frozen enhanced WIP is uniform over the compact probability simplex;
6. for a slowly varying parameter sequence, the centered branch increments
   form a bounded martingale triangular array whose predictable bracket is the
   Riemann sum of `Sigma` and whose antisymmetric compensator is zero.

#### Proof

Items 1--4 are direct from conditional independence.  Frozen Donsker and
second-level martingale convergence are uniform because the probability
vectors range in a compact subset of the simplex and increments are bounded.
For item 6, conditional Lindeberg is automatic.  Smoothness of (5.1) and slow
variation give convergence of the predictable covariance Riemann sums.  The
martingale rough-path triangular-array theorem yields the full-scale enhanced
limit directly, without accumulating frozen block-law errors.

### Corollary 5.2 (actual full-scale K2)

The slowly selected four-branch Bernoulli model satisfies Theorem 4.2 for the
full microscopic scale `epsilon->0` by the direct-characteristics route.

---

## 6. Dynamic programming and the HJB limit

Let `S_{t,s}^epsilon` be prelimit dynamic-programming operators acting on
bounded uniformly continuous terminal payoffs.  The microscopic port is fixed
before these operators are introduced.

### Assumption 6.1 (DPP package)

1. `S^epsilon` is monotone, constant preserving in the declared cash
   convention, and dynamically consistent;
2. values are locally equicontinuous and stable;
3. Theorem 4.2 gives the frozen local characteristics;
4. for every smooth test `phi`,
   \[
   \frac{S_{t,t+h}^\varepsilon\phi-\phi}{h}
   \longrightarrow
   -\mathcal H(x,D\phi,D^2\phi);
   \tag{6.1}
   \]
5. the limiting equation has comparison in the chosen growth class.

### Theorem 6.2 (HJB convergence)

Under Assumption 6.1, the prelimit values converge locally uniformly to the
unique viscosity solution of

\[
\partial_tu+\mathcal H(x,Du,D^2u)=0,
\qquad u(T,\cdot)=\phi.
\tag{6.2}
\]

#### Proof

Take upper and lower half-relaxed limits.  Monotonicity and consistency at a
strict smooth contact point give the viscosity sub- and supersolution
inequalities.  Stability passes the terminal condition.  Comparison identifies
the two limits, and local equicontinuity upgrades subsequential convergence to
local uniform convergence.

The proof uses K2 characteristics but no filtering, game, BSDE, or Girsanov
representation.

---

## 7. The theta-expectation semigroup

For `s<=t`, define

\[
\mathcal E_{s,t}^{\theta}[\phi](x)
=u(s,x),
\tag{7.1}
\]

where `u` solves (6.2) with terminal value `phi` at time `t`.

### Theorem 7.1 (theta-expectation properties)

The family in (7.1) is monotone, terminally stable, constant preserving under
the declared normalization, and time consistent:

\[
\mathcal E_{r,s}^{\theta}
\left[
\mathcal E_{s,t}^{\theta}[\phi]
\right]
=
\mathcal E_{r,t}^{\theta}[\phi].
\tag{7.2}
\]

#### Proof

Monotonicity and stability follow from comparison.  Constant preservation is
the zero-cost normalization.  Equation (7.2) follows by concatenating the DPP
or by uniqueness on adjacent time intervals.

### 7.2 Explicit nonconvexity and failure of subadditivity

Let the finite-response port contain

\[
H(p)=\gamma(1-\cos p)-\delta(1-\cos2p),
\tag{7.3}
\]

with

\[
\delta>\gamma/4>0.
\tag{7.4}
\]

Then

\[
H''(0)=\gamma-4\delta<0,
\]

so the Hamiltonian is nonconvex.  More explicitly, with

\[
p=q=\pi/2,
\]

one has

\[
H(p+q)-H(p)-H(q)=4\delta>0.
\tag{7.5}
\]

The readout (7.3) is fixed as a deterministic endpoint response before the HJB
is solved.  Add any uniformly elliptic Paper-II diffusion field.

### Proposition 7.2 (non-subadditive theta-expectation)

The theta-expectation associated with (7.3) is not subadditive.

#### Proof

Use affine terminal data localized by a smooth cutoff around one point.  The
short-time viscosity expansion there is

\[
\mathcal E_{t-h,t}^{\theta}[\phi](x)
=
\phi(x)+hH(D\phi(x))+o(h),
\]

because the Hessian vanishes at the contact point.  Apply this to gradients
`p`, `q`, and `p+q`.  Subadditivity would imply
`H(p+q)<=H(p)+H(q)` after division by `h`, contradicting (7.5).

---

## 8. Exported interface

Paper IV may import:

```text
P3-DOOB       frozen normalized selected kernels
P3-RWIP       uniform enhanced WIP with declared modulus or characteristics
P3-NAHOM      nonautonomous homogenized characteristics
P3-HJB        uncontrolled/one-player viscosity limit
P3-THETA      time-consistent theta-expectation semigroup
P3-NONCONVEX  explicit non-subadditive branch
P3-ACTUAL-4B  Bernoulli four-branch full-scale realization
```

Paper V may import `P3-HJB`, `P3-THETA`, and the coefficient regularity window.

---

## 9. Conclusion

The microscopic selection, rough limit, and nonlinear expectation now occur in
the correct causal order.  The enhanced-WIP scale compatibility is explicit;
the actual four-branch model uses direct martingale characteristics rather than
an unsupported quantitative rough rate.  Games and filtering are optional
downstream branches rather than hidden assumptions of the basic theta-HJB
theorem.
