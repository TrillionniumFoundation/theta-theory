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
filter contracts uniformly along every strategy tree.  This yields belief
collapse and permits the fast homogenization error to be estimated uniformly
over strategies.

We prove bounded-state and weighted versions.  The weighted theorem includes a
separate comparison/uniqueness gate, which cannot be inferred from Lyapunov
coupling alone.  An actual model is supplied by the four-branch deterministic
system of Papers I--III: its branch coding is Bernoulli, so the hidden-symbol
prediction forgets the prior in one step.  Positive finite-alphabet
observations and compact controls then give exact strategy-tree belief collapse
and a complete mixed-Isaacs realization.

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

Observations take values in a finite or compact alphabet `Y` and have likelihood

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

The filtered state is obtained by composing (1.1) for the prescribed number of
fast steps and then (1.2).

---

## 2. Bounded filtering and the observation-gap criterion

Use the total-variation norm

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
\qquad
C_B=2g_+/g_-.
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
`|nu(gf)|<=nu(g)`, the second has the same bound.  Taking the supremum proves
(2.3).

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
are uniform in controls, observations, and slow states, so the same estimate
holds pathwise on every node of a strategy tree.

### Corollary 2.5 (belief-insensitive values)

If terminal and running rewards are uniformly Lipschitz in belief, then finite-
horizon values starting from `nu,nu'` differ by at most

\[
C\sum_{k=0}^{N}q^k\|\nu-\nu'\|_{TV}
\le\frac{C}{1-q}\|\nu-\nu'\|_{TV}.
\tag{2.6}
\]

When the fast number of filter updates on every positive slow interval tends to
infinity, the limiting value is independent of the initial belief.

---

## 3. Slow variation and strategy-tree stability

The slow state and controls vary during the prediction interval.  Let
`omega_P(delta)` and `omega_g(delta)` be moduli for the prediction kernel and
likelihood when the slow/control path varies by `delta`.

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
sides.  The first difference contracts by `q`; the parameter replacement is
bounded by the two moduli.  Iterate the resulting affine recursion.

If `delta_k` tends to zero on the K2 freezing scale, the convolution term
vanishes uniformly over strategies.

---

## 4. The weighted filtering branch

For noncompact hidden states, let `W>=1` be a Lyapunov function and define the
weighted dual norm

\[
\|\mu-\nu\|_W
=
\sup_{|f|\le W}|\mu(f)-\nu(f)|.
\]

### Assumption 4.1 (weighted packet)

1. predictions satisfy a drift/minorization or Harris estimate and contract on
   a common `W`-moment ball;
2. the posterior and next prediction preserve that moment ball;
3. the likelihood and its reciprocal have the weighted regularity needed for
   a finite Bayes Lipschitz constant `C_B(W,R)` on the ball;
4. the observation gap makes
   \[
   C_B(W,R)\rho_W^{r_*}<1;
   \]
5. the limiting weighted HJB/Isaacs equation has comparison in the declared
   growth class.

### Theorem 4.2 (weighted filter and value collapse)

Under Assumption 4.1, Theorems 2.4 and 3.1 hold in the weighted norm on finite
slow horizons.  The partially observed values converge to a unique weighted
HJB/Isaacs limit.

#### Proof

The moment ball makes the Bayes denominator and weighted numerator estimates
uniform.  The Harris contraction and Bayes bound yield the strict update
factor.  The strategy-tree recursion is unchanged.  Tightness and local
consistency give half-relaxed sub- and supersolutions; the separately assumed
weighted comparison theorem identifies the limit.

### Remark 4.3

Lyapunov coupling alone does not prove the final PDE comparison theorem.  The
comparison gate is an independent typed input and is never omitted.

---

## 5. Sequential games

Fix the payoff convention that player `U` maximizes and player `V` minimizes.
In a sequential lower game, `u` is chosen first and `v` responds.  The local
Hamiltonian is

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

Assume the Paper-III K2 limit holds uniformly over admissible frozen controls,
the filter packet gives strategy-tree belief collapse, and the lower and upper
DPPs are stable and consistent.  Then the lower and upper prelimit values
converge to the unique viscosity solutions of

\[
\partial_tu^-+H^-(x,Du^-,D^2u^-)=0,
\tag{5.3}
\]

\[
\partial_tu^++H^+(x,Du^+,D^2u^+)=0.
\tag{5.4}
\]

#### Proof

On each DPP step, Paper III supplies the control-uniform local characteristics
and Theorem 2.4 removes the initial-belief dependence.  The order of the two
optimizations is retained in the consistency limit.  Half-relaxed limits and
the corresponding comparison theorems give (5.3) and (5.4).

### Corollary 5.2

Without an Isaacs condition, `u^-` and `u^+` are distinct legitimate limits.
Neither is replaced by a simultaneous value.

---

## 6. Simultaneous relaxed games and mixed Isaacs equality

Let `P(U)` and `P(V)` be relaxed-control spaces.  Extend the local payoff by

\[
\overline F(x,p,X;\mu,\nu)
=
\int_{U\times V}F(x,p,X;u,v)\,\mu(du)\nu(dv).
\tag{6.1}
\]

### Assumption 6.1

`U,V` are compact and `F` is continuous.  Hence `overline F` is continuous and
affine in each relaxed control.

### Theorem 6.2 (mixed Isaacs equality)

Under Assumption 6.1,

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

Under the uniform K2/filter/DPP packets, simultaneous relaxed prelimit values
converge to the unique viscosity solution with Hamiltonian equal to either side
of (6.2).

### Proposition 6.4 (pure-saddle criterion)

Mixed Isaacs equality does not imply a pure saddle.  A pure saddle follows if,
for each `(x,p,X)`, there are `u_*,v_*` such that

\[
F(u,v_*)\le F(u_*,v_*)\le F(u_*,v)
\]

for all `u,v`, or from a declared convex--concave pure-control structure.

This extra certificate is the exact pure-strategy gate.

---

## 7. Belief-state and path-state equations

If contraction is not accelerated enough to eliminate the belief, the Markov
state is `(x,nu)`.  The DPP then gives a belief-state HJB on

\[
\mathbb R^m\times\mathcal P(E).
\]

For a smooth cylindrical test `Phi(x,nu)`, the generator includes the K2 slow
characteristics and the filter generator in the measure variable.

### Theorem 7.1 (belief-state limit)

Under filter tightness, K2 control-uniform characteristics, local consistency,
and comparison on the belief space, the partially observed values converge to
the unique belief-state viscosity solution.

If admissibility or coefficients depend on the entire observation/control
history beyond the current filter, the state is a path.  The same DPP produces
a path-dependent PDE rather than a finite-dimensional HJB.

### Scope rule 7.2

A path-dependent problem is not projected to a finite-dimensional equation
unless a sufficient Markov state, such as the current belief, has actually been
proved.

---

## 8. Actual four-branch hidden-symbol game

Use the Paper-III Bernoulli coding.  Let the hidden state be the branch symbol

\[
I_n\in\{1,2,3,4\}.
\]

For controls `(u,v)` and slow state `x`, choose smooth probabilities

\[
p_j(x,u,v)\ge p_*>0,
\qquad \sum_jp_j=1,
\]

obtained from compact tilts of the four branch weights.  Set

\[
P_{ij}^{x,u,v}=p_j(x,u,v).
\tag{8.1}
\]

Thus every prediction sends every prior belief to the same probability vector:

\[
\nu P^{x,u,v}=p(x,u,v).
\tag{8.2}
\]

The prediction contraction coefficient is `rho=0`.

Let observations have likelihoods

\[
g_y(j;x,u,v)\in[g_-,g_+].
\]

### Proposition 8.1 (exact strategy-tree filter collapse)

For the model (8.1), after each prediction the posterior is independent of the
belief before prediction.  Hence the initial belief is forgotten in one fast
step, uniformly over controls and observation paths.

#### Proof

Equation (8.2) is independent of `nu`.  Bayes update therefore starts from the
same predicted vector for every prior.

Let slow increments be bounded functions `c_j(x,u,v)`, centered with respect to
`p(x,u,v)`.  The K2 driver is a control-dependent triangular array of bounded
conditionally independent increments.  Its covariance is

\[
\Sigma(x,u,v)
=
\sum_jp_jc_j\otimes c_j.
\]

Paper III applies uniformly.

### Theorem 8.2 (actual sequential and simultaneous limits)

The four-branch hidden-symbol model has:

1. exact filter stability;
2. uniform control-dependent rough WIP and nonautonomous homogenization;
3. sequential lower and upper HJB limits;
4. a simultaneous relaxed mixed-Isaacs limit;
5. a pure value whenever the additional saddle certificate in Proposition 6.4
   is satisfied.

This is an actual scoped deterministic-symbolic realization of Paper IV.

---

## 9. Exported interface

Paper V may import:

```text
P4-FILTER-B      bounded filter contraction and belief collapse
P4-FILTER-W      weighted filter theorem with separate comparison gate
P4-SEQ           lower and upper sequential HJBs
P4-MIXED         simultaneous relaxed mixed Isaacs value
P4-PURE-GATE     exact additional pure-saddle condition
P4-BELIEF        belief-state HJB
P4-PATH          path-state DPP/PPDE interface
P4-ACTUAL-4B     actual hidden-symbol game
```

---

## 10. Conclusion

Partial observation and games do not form one undifferentiated K3 step.  Filter
stability, sequential order, simultaneous minimax, and pure saddles have
different hypotheses and different outputs.  Once these branches are typed,
the K2 rough limit can be combined with them without circularity or hidden
Isaacs assumptions.
