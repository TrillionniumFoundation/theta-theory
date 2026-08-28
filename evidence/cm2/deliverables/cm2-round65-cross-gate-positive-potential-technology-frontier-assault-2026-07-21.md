# CM2 Round 65 cross-gate assault: positive path potential and technology frontier

Date label: 2026-07-21

Strict verdict: **this leaf closes no composite gate.  It gives one exact
operator criterion joining the Gate-4 tag lift, Gate-5 cross-time drift and
the positive-variation side of Gate-3 current/Piola.  The frozen actual data
do not satisfy its required pointwise envelope.  CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Frozen scope

This append-only leaf pins the Round-64 aggregate and independent audit, the
Round-64 Gate-1/3 scalar-clock leaf, the Gate-2/4 tag-lift leaf and the Gate-5
lineage leaf.  It modifies no old artifact.

The purpose is to prevent three distinct average statements from being
mistaken for a strong all-time operator bound:

1. a finite moment of one actual tagged measure;
2. a geometric loss of total live mass across insertion time; and
3. a signed current identity with possible cancellation.

The correct common object is a positive conditional path potential.

## 2. Exact positive path-potential criterion

Let `(X,mu)` be a finite standard-Borel measure space.  For every `j>=0`, let
`P_(0:j)` be a sub-Markov kernel from `X` to a standard-Borel space `E_j`.
Let `K_j` be a Markov tag kernel from `E_j` to `Z_j`, and let
`g_j:Z_j->[0,infinity]` be a measurable positive charge.  It may be the sum
of finitely or countably many typed sector charges.  Put

```text
W_j(y)=integral g_j(z) K_j(y,dz),
H(x)=sum_(j>=0) w^j P_(0:j)W_j(x),       w>1.
```

For `f in L1(mu)`, define the time-labelled lift

```text
A f = direct_sum_(j>=0) w^j (K_j)_#(P_(0:j))_#(f mu),
```

with target norm equal to the sum of the `g_j`-weighted total variations.
Then

```text
A:L1(mu) -> direct_sum_j X_(g_j) is bounded
iff H belongs to L-infinity(mu),

||A|| = ||H||_infinity.
```

Indeed, positivity gives

```text
||Af|| <= integral |f| H dmu.
```

For nonnegative `f` there is no Jordan cancellation and equality holds.
Indicators of positive-measure superlevel sets of `H` give the reverse
operator-norm inequality.  Thus the criterion is exact, not merely
sufficient.

For several CM2 sectors, replace `g_j` by the sum of the active-clock,
raw-`Z`, Orlicz, complement, variation, common-mode, cemetery-arrival,
tag-depth and positive-current charges.  Every term remains typed and
positive.  A signed difference cannot pay this norm.

## 3. Sharp two-factor separator

The two necessary mechanisms -- time decay and pointwise tag control -- are
independent.

Take `X={1,2,...}` with

```text
mu{n}=3*4^(-n),       w=3/2,
P_(0:j)(n,{n})=3^(-j),
W_j(n)=2^n.
```

The owner marginal contracts at every step by `kappa=1/3`, so

```text
w*kappa=1/2<1.
```

The actual one-vector tag moment is finite:

```text
integral W_0 dmu=3.
```

Even the complete weighted all-time charge of that one vector is finite:

```text
sum_j w^j integral P_(0:j)W_j dmu
 =sum_j 3*(1/2)^j
 =6.
```

But the conditional path potential is

```text
H(n)=sum_j (1/2)^j 2^n=2^(n+1),
```

which is unbounded.  Unit `L1(mu)` densities concentrated at larger `n`
therefore have strong-lift norms tending to infinity.  Consequently

```text
cross-j contraction + finite actual all-time moment
does not imply a bounded strong lift.
```

Conversely, take `W_j=1` and the identity Markov path.  The tag envelope is
uniformly bounded at each time, but

```text
H=sum_j w^j=infinity.
```

Thus pointwise tag control does not replace cross-time decay.

A useful sufficient interface is the genuinely pointwise estimate

```text
P_(0:j)W_j(x) <= C kappa^j       for mu-a.e. x,
w*kappa<1,
```

which yields `H<=C/(1-w*kappa)`.  The Round-64 frozen rows give neither this
joint estimate nor its exact `L-infinity` equivalent.

## 4. Cemetery and current typing

The same potential explains the one-shot cemetery rule.  If a killed record
is counted as absorbing occupancy at every `j>=tau`, its conditional charge
contains

```text
sum_(j>=tau) w^j=infinity
```

whenever `tau<infinity`.  A positive cemetery can therefore enter the
weighted direct sum only as a one-shot arrival charge, whose own conditional
arrival potential must still be essentially bounded.

For Gate 3, the criterion applies to positive total variation or positive
Jordan components of a current.  It does not construct the physical
anisotropic Piola recipient, bounded differentiable `R_s/Q_s`, or `MT_DQ`.
It says exactly what their positive all-time charge must pay once those maps
are typed.

For Gate 4, `W_j` specializes to the conditional tag-depth moment.  The
Round-64 condition `W_D in L-infinity` is the one-time case.  The present
result shows that a uniform one-time bound is still insufficient unless the
entire conditional path potential is in `L-infinity`.

For Gate 5, a same-label owner marginal coefficient `c_*<w^(-1)` controls
only live mass.  It does not control the conditional tag/current/sector
charge without the joint pointwise estimate above.

## 5. Latest technology boundary

Four current sources were checked directly.

- `arXiv:2603.19509v3` builds a sequence-space resolvent for nonautonomous
  linear response under rapid loss of memory and strong differentiability.
  Its verified deterministic example is sequential `C^3` expanding maps;
  its other example uses positive noise.  It does not verify moving-billiard
  discontinuity, boundary current, anisotropic Piola or CM2 `R_s/Q_s`.
- `arXiv:2604.25746v1` proves Bernoulli properties for hyperbolic SRB
  measures of `C^(1+beta)` flows on compact boundaryless manifolds.  Its
  singularities are fixed points of the generating vector field, not
  billiard collision discontinuities or moving boundaries.
- `arXiv:2510.19573v3` proves domination and Lyapunov criteria for positive
  kernels on weighted `L-infinity` function spaces.  It assumes the kernel
  domination/local compactness or Lyapunov rows that CM2 still needs; it does
  not manufacture the measure-side cross-`j` owner domination.
- `arXiv:2605.07824` concerns tamed Feynman--Kac diffusion processes and a
  killing--branching intertwining.  It is the wrong process and recipient.

These sources sharpen the abstract technology map but supply none of the
missing pinned actual hypotheses.  No external theorem is promoted.

## 6. Strict boundary after this leaf

```text
positive path-potential iff:                         CERTIFIED_EXACT
two-factor separator:                               CERTIFIED_EXACT
one-shot cemetery consequence:                      CERTIFIED_EXACT
actual CM2 joint conditional potential in L-infty:  NOT_CERTIFIED
physical anisotropic Piola / strong R_s-Q_s:         NOT_CERTIFIED
actual collision-SRB invariant product tree:         NOT_CERTIFIED
actual cross-j owner contraction:                    NOT_CERTIFIED

Gate 1: NOT_CERTIFIED
Gate 2: NOT_CERTIFIED; official fields 0/17
Gate 3: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED; landing join 1/7
Gate 5: NOT_CERTIFIED; maturity 10/18, blocks 0
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

The shortest lawful strong route is now one joint task: construct the actual
path kernel on immutable owner/time labels and prove an `L-infinity` bound
for the sum of every positive sector, tag, current and one-shot-arrival
charge.  Average fixed-time moments cannot substitute for that bound.
