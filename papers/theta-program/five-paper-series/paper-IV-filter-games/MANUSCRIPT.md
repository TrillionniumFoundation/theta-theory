# Filtering and Isaacs limits for partially observed deterministic multiscale games

## Abstract

We combine the Doob-selected rough homogenization of Paper III with partial
observation and two-player dynamic programming.  The three relevant branches
are separated permanently.  A sequential game produces lower and upper HJB
equations without requiring Isaacs equality.  A simultaneous game is treated
with relaxed controls; bilinearity gives a mixed Isaacs value but not, by
itself, a pure saddle.  A filtering branch uses prediction contraction,
posterior moment balls, and an explicit Bayes Lipschitz constant.  If the
prediction performed between observations dominates the Bayes expansion, the
filter contracts uniformly along every strategy tree.

Belief collapse in the slow limit also requires the microscopic initial layer
to have vanishing slow duration.  We state this condition explicitly; bounded
geometric sensitivity alone would not make the first reward independent of the
initial belief.  With the initial-layer gate, the fast homogenization error is
uniform over strategies.  We prove bounded-state and weighted versions.  The
weighted theorem includes a separate comparison/uniqueness gate, which cannot
be inferred from Lyapunov coupling alone.

An actual model is supplied by the four-branch deterministic system of Papers
I--III: its branch coding is Bernoulli, so the hidden-symbol prediction forgets
the prior in one step.  Positive finite-alphabet observations and compact
controls then give exact strategy-tree belief collapse and a complete
mixed-Isaacs realization.

---

## 1. State, controls, and observations

Let `X_t^epsilon` be the slow state and `Z_n^epsilon` the fast hidden state.
Players use controls

\[
u\in U,\qquad v\in V,
\]

where `U,V` are compact metric spaces.  The frozen hidden prediction kernel is

\[
P_{x,u,v}.
\]

Observations take values in an alphabet `Y` and have likelihood

\[
g_y(z;x,u,v)>0.
\]

A belief is a probability measure `nu` on the hidden state.  Prediction and
Bayes update are

\[
\mathsf Pred_{x,u,v}(\nu)=\nu P_{x,u,v},
\tag{1.1}
\]

\[
\mathsf B_{y,x,u,v}(\nu)(dz)
=
\frac{g_y(z;x,u,v)\nu(dz)}{\nu(g_y)}.
\tag{1.2}
\]

---

## 2. Bounded filtering and the observation-gap criterion

Use

\[
\|\mu-\nu\|_{TV}
=\sup_{|f|\le1}|\mu(f)-\nu(f)|.
\]

### Assumption 2.1 (uniform prediction contraction)

For all slow states and controls,

\[
\|\mu P_{x,u,v}-\nu P_{x,u,v}\|_{TV}
\le\rho\|\mu-\nu\|_{TV},
\qquad 0\le\rho<1.
\tag{2.1}
\]

### Assumption 2.2 (positive observations)

There are constants

\[
0<g_-\le g_y(z;x,u,v)\le g_+<\infty
\tag{2.2}
\]

uniformly in all variables.

### Lemma 2.3 (Bayes Lipschitz bound)

Under (2.2),

\[
\|\mathsf B_g(\mu)-\mathsf B_g(\nu)\|_{TV}
\le C_B\|\mu-\nu\|_{TV},
\qquad C_B=2g_+/g_-.
\tag{2.3}
\]

#### Proof

For `|f|<=1`, add and subtract `nu(gf)/mu(g)`:

\[
\left|
\frac{\mu(gf)}{\mu(g)}-
\frac{\nu(gf)}{\nu(g)}
\right|
\le
\frac{|(\mu-\nu)(gf)|}{\mu(g)}
+
\frac{|\nu(gf)|\,|(\mu-\nu)(g)|}
     {\mu(g)\nu(g)}.
\]

The first term is at most `(g_+/g_-)||mu-nu||`.  Since
`|nu(gf)|<=nu(g)`, the second has the same bound.

### Theorem 2.4 (filter contraction with an observation gap)

Suppose `r_*` prediction steps occur between observations and

\[
q:=C_B\rho^{r_*}<1.
\tag{2.4}
\]

Then one complete prediction--observation update contracts beliefs by `q`.
For a fixed observation/control path,

\[
\|\nu_n-\nu_n'\|_{TV}
\le q^n\|\nu_0-\nu_0'\|_{TV}.
\tag{2.5}
\]

The estimate is uniform over all admissible strategy trees.

#### Proof

Iterating (2.1) `r_*` times gives `rho^{r_*}`.  Apply Lemma 2.3.  The constants
are uniform in controls, observations, and slow states.

### Assumption 2.5 (vanishing slow initial layer)

Before the first order-one slow reward or terminal comparison is sampled, the
fast filter performs `ell_epsilon` complete updates, where

\[
ell_\varepsilon\to\infty,
\qquad
\delta_\varepsilon^{\rm init}\to0
\tag{2.6}
\]

and `delta_epsilon^init` is the corresponding slow physical duration.  Running
cost accumulated inside this initial layer is bounded by
`C delta_epsilon^init`.

### Corollary 2.6 (initial-belief collapse in slow values)

Under Theorem 2.4 and Assumption 2.5, the difference between slow values
started from `nu` and `nu'` is bounded by

\[
C_Tq^{\ell_\varepsilon}
\|\nu-\nu'\|_{TV}
+C\delta_\varepsilon^{\rm init}
+\operatorname{Err}_\varepsilon,
\tag{2.7}
\]

where `Err_epsilon` contains the later slow-freezing/filter perturbations.  If
that error tends to zero, the limiting value is independent of the initial
belief.

#### Proof

Couple the two filters along the same controls and observations.  At the first
macroscopic sampling time, (2.5) gives the first term in (2.7).  The only reward
that can see the uncontracted prior lies in the initial layer and has size at
most the second term.  Thereafter the strategy-tree contraction and the
slow-variation convolution control all differences.

### Remark 2.7

The bounded geometric series `sum q^k` alone would only give a finite
Lipschitz constant in the initial belief; it would not prove belief
independence.  The vanishing initial-layer condition is essential.

---

## 3. Slow variation and strategy-tree stability

Let `omega_P(delta)` and `omega_g(delta)` be moduli for the prediction kernel
and likelihood when the slow/control path varies by `delta`.

### Proposition 3.1 (convolution stability)

For two paths with the same observation symbols and slow/control discrepancy at
most `delta_k` on the `k`th update,

\[
\|\nu_n-\nu_n'\|
\le q^n\|\nu_0-\nu_0'\|
+C\sum_{k=0}^{n-1}q^{n-1-k}
\bigl(\omega_P(\delta_k)+\omega_g(\delta_k)\bigr).
\tag{3.1}
\]

#### Proof

At each update, insert an intermediate belief using the same parameters on both
sides.  The first difference contracts by `q`; parameter replacement is
bounded by the moduli.  Iterate the affine recursion.

---

## 4. The weighted filtering branch

For noncompact hidden states, let `W>=1` and define

\[
\|\mu-\nu\|_W
=\sup_{|f|\le W}|\mu(f)-\nu(f)|.
\]

### Assumption 4.1 (weighted packet)

1. predictions satisfy a drift/minorization or Harris estimate and contract on
   a common `W`-moment ball;
2. posterior and prediction preserve that ball;
3. the likelihood and reciprocal have the weighted regularity needed for a
   finite Bayes factor `C_B(W,R)`;
4. `C_B(W,R)rho_W^{r_*}<1`;
5. the weighted initial-layer analogue of Assumption 2.5 holds;
6. the limiting weighted HJB/Isaacs equation has comparison in the declared
   growth class.

### Theorem 4.2 (weighted filter and value collapse)

Under Assumption 4.1, Theorems 2.4, 2.6, and 3.1 hold in the weighted norm on
finite slow horizons.  The partially observed values converge to a unique
weighted HJB/Isaacs limit.

#### Proof

The moment ball makes the Bayes denominator and weighted numerator estimates
uniform.  The Harris contraction and Bayes bound yield the strict update
factor.  The initial-layer and strategy-tree arguments are unchanged.
Tightness and local consistency give half-relaxed sub- and supersolutions; the
separately assumed weighted comparison theorem identifies the limit.

### Remark 4.3

Lyapunov coupling alone does not prove the final PDE comparison theorem.

---

## 5. Sequential games

Player `U` maximizes and player `V` minimizes.  In a sequential lower game,
`u` is chosen first and `v` responds:

\[
H^-(x,p,X)
=\sup_{u\in U}\inf_{v\in V}
F(x,p,X;u,v).
\tag{5.1}
\]

For the opposite order,

\[
H^+(x,p,X)
=\inf_{v\in V}\sup_{u\in U}
F(x,p,X;u,v).
\tag{5.2}
\]

### Theorem 5.1 (sequential homogenized values)

Assume the Paper-III K2 limit holds uniformly over frozen controls, the filter
packet and initial-layer gate give strategy-tree belief collapse, and the lower
and upper DPPs are stable and consistent.  Then the prelimit lower and upper
values converge to the unique viscosity solutions of

\[
\partial_tu^-+H^-(x,Du^-,D^2u^-)=0,
\tag{5.3}
\]

\[
\partial_tu^++H^+(x,Du^+,D^2u^+)=0.
\tag{5.4}
\]

#### Proof

On each DPP step, Paper III supplies control-uniform local characteristics and
Corollary 2.6 removes the initial-belief dependence.  The order of the two
optimizations is retained in the consistency limit.  Half-relaxed limits and
comparison give (5.3)--(5.4).

Without an Isaacs condition, these are distinct legitimate limits.

---

## 6. Simultaneous relaxed games and mixed Isaacs equality

Let `P(U)` and `P(V)` be relaxed-control spaces and define

\[
\overline F(x,p,X;\mu,\nu)
=
\int_{U\times V}F(x,p,X;u,v)\,\mu(du)\nu(dv).
\tag{6.1}
\]

### Assumption 6.1

`U,V` are compact and `F` is continuous.  Thus `overline F` is continuous and
affine in each relaxed control.

### Theorem 6.2 (mixed Isaacs equality)

\[
\sup_{\mu\in\mathcal P(U)}
\inf_{\nu\in\mathcal P(V)}\overline F
=
\inf_{\nu\in\mathcal P(V)}
\sup_{\mu\in\mathcal P(U)}\overline F.
\tag{6.2}
\]

#### Proof

The relaxed-control spaces are compact convex, and `overline F` is continuous,
concave in the maximizing variable and convex in the minimizing variable.
The minimax theorem applies.

### Theorem 6.3 (simultaneous homogenized game)

Under the uniform K2/filter/initial-layer/DPP packets, simultaneous relaxed
prelimit values converge to the unique viscosity solution with Hamiltonian
equal to either side of (6.2).

### Proposition 6.4 (pure-saddle criterion)

Mixed Isaacs equality does not imply a pure saddle.  A pure saddle follows if,
for each `(x,p,X)`, there are `u_*,v_*` such that

\[
F(u,v_*)\le F(u_*,v_*)\le F(u_*,v)
\]

for all `u,v`, or from a declared convex--concave pure-control structure.

---

## 7. Belief-state and path-state equations

If contraction is not accelerated enough to eliminate the belief, the Markov
state is `(x,nu)`.  The DPP gives a belief-state HJB on

\[
\mathbb R^m\times\mathcal P(E).
\]

### Theorem 7.1 (belief-state limit)

Under filter tightness, K2 control-uniform characteristics, local consistency,
and comparison on the belief space, the partially observed values converge to
the unique belief-state viscosity solution.

If admissibility or coefficients depend on the entire observation/control
history beyond the current filter, the state is a path and the DPP produces a
path-dependent PDE.

### Scope rule 7.2

A path-dependent problem is not projected to a finite-dimensional equation
unless a sufficient Markov state has actually been proved.

---

## 8. Actual four-branch hidden-symbol game

Use the Paper-III Bernoulli coding.  Let

\[
I_n\in\{1,2,3,4\}
\]

be the hidden branch symbol.  For controls `(u,v)` and slow state `x`, choose
smooth probabilities

\[
p_j(x,u,v)\ge p_*>0,
\qquad \sum_jp_j=1,
\]

obtained from compact tilts of the four branch weights, and set

\[
P_{ij}^{x,u,v}=p_j(x,u,v).
\tag{8.1}
\]

Thus

\[
\nu P^{x,u,v}=p(x,u,v)
\tag{8.2}
\]

for every prior, so `rho=0`.

Let observations satisfy

\[
g_y(j;x,u,v)\in[g_-,g_+].
\]

### Proposition 8.1 (exact strategy-tree filter collapse)

After one prediction, the posterior is independent of the belief before
prediction.  Hence Assumption 2.5 holds with `ell_epsilon=1` and a one-fast-step
slow duration tending to zero.

#### Proof

Equation (8.2) is independent of `nu`; Bayes update therefore starts from the
same predicted vector for every prior.  The diffusive slow time of one fast
step tends to zero.

Let slow increments be bounded functions `c_j(x,u,v)`, centered with respect to
`p(x,u,v)`.  The K2 driver is a control-dependent triangular array of bounded
conditionally independent increments, with covariance

\[
\Sigma(x,u,v)=\sum_jp_jc_j\otimes c_j.
\]

### Theorem 8.2 (actual sequential and simultaneous limits)

The four-branch hidden-symbol model has:

1. exact filter stability and vanishing initial layer;
2. uniform control-dependent rough WIP and nonautonomous homogenization;
3. sequential lower and upper HJB limits;
4. a simultaneous relaxed mixed-Isaacs limit;
5. a pure value whenever Proposition 6.4 is verified.

---

## 9. Exported interface

Paper V may import:

```text
P4-FILTER-B      bounded filter contraction and belief collapse
P4-FILTER-W      weighted filter theorem with comparison gate
P4-SEQ           lower and upper sequential HJBs
P4-MIXED         simultaneous relaxed mixed Isaacs value
P4-PURE-GATE     additional pure-saddle condition
P4-BELIEF        belief-state HJB
P4-PATH          path-state DPP/PPDE interface
P4-ACTUAL-4B     actual hidden-symbol game
```

---

## 10. Conclusion

Partial observation and games do not form one undifferentiated K3 step.  Filter
stability, initial-layer collapse, sequential order, simultaneous minimax, and
pure saddles have different hypotheses and outputs.  Once these branches are
typed, the K2 rough limit combines with them without circularity or hidden
Isaacs assumptions.
