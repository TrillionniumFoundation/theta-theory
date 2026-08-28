# CM2 Round 67 Gate 5 — direct positive-potential attenuation frontier

Date: 2026-07-21

Strict verdict: **the maximal time-retaining terminal-record carrier supports an
exact direct all-time positive-potential criterion which does not require the
surviving full-label RN density to be below one.  Uniform conditional terminal
moments, a bounded Lyapunov/Doob supersolution, or a genuinely weighted
sub-Markov survival estimate would pay it.  None of those pointwise rows, the
raw-`Z`/Orlicz slice, the pre-regularization cemetery arrival, or the physical
Round-54/Round-61 oriented carrier is present in the frozen actual data.  Gate-5
maturity remains `10/18`, complete blocks remain zero, and CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Frozen scope and the change of route

This append-only leaf pins the Round-66 aggregate and independent audit, the
Round-66 graph-registry and Gate-5 leaves, the Round-65 positive-potential and
sector leaves, and the Round-54/61--64 owner, cemetery and oriented-positive
chain.  It modifies no old artifact.

Round 66 proved that on a nonzero birth-free full-label overlap the one-step RN
density is exactly one.  This leaf does not revisit terminal nesting as a
contraction proof.  Instead it evaluates the direct resolvent on the complete
time-retaining record.  Finite lifetime can pay that resolvent even while every
surviving record has density one.

## 2. The maximal direct potential

Let `(X,mu)` be the physical input root law and let `Q_x` be a graph-supported
terminal-record kernel into the maximal standard-Borel record carrier `R`.  A
record retains terminal word, source/root, owner, event, side, branch and every
immutable insertion label.  No time coordinate is deleted.

For time `j` and typed positive sector `s`, let

```text
g_j^s(r)>=0
```

be its time-`j` charge.  The seven Gate-5 sectors are

```text
active-clock, raw-Z, power-Orlicz, complement,
variation, common-mode, one-shot-cemetery.
```

Normal terminal and owner-switch departures are one-shot arrivals.  The
pre-regularization cemetery is a different arrival sector.  Put

```text
G(r)=sum_(j>=0) w_Z^j sum_s g_j^s(r),
H(x)=integral_R G(r) Q_x(dr).
```

Every summand is positive and typed.  If `A` sends `f in L1(mu)` to the
time/sector direct sum of the corresponding positive lifted measures, with
target norm the sum of sector total variations, then

```text
A is bounded  iff  H belongs to L-infinity(mu),
||A||=||H||_infinity.
```

The proof is Tonelli plus positivity.  The upper estimate is
`||Af||<=integral |f|H dmu`; nonnegative normalized indicators of superlevel
sets of `H` give the reverse inequality.  This is also the exact criterion when
some charges take value infinity.

There are two distinct levels which must not be conflated:

```text
recordwise sufficient condition: G in L-infinity(R),
exact physical condition:        QG=H in L-infinity(mu).
```

Recordwise boundedness can be stronger because `Q_x` may average terminal
depth.  Conversely, a finite actual average `integral H dmu` is weaker than the
required essential supremum.  The criterion therefore cannot be evaluated
without the actual graph-supported root kernel and all positive charge marks.

## 3. Exact finite-lifetime identity

Let `N(r)>=1` be terminal lifetime and first take unit live charge
`g_j(r)=1_{j<N(r)}`.  Then

```text
G_live(r)=sum_(j=0)^(N(r)-1) w_Z^j
         =(w_Z^N(r)-1)/(w_Z-1),

H_live(x)=(E_x[w_Z^N]-1)/(w_Z-1).
```

Thus the direct unit-live lift is bounded exactly when

```text
ess sup_x E_x[w_Z^N] < infinity.
```

This cleanly separates the valid direct route from the invalid nesting route.
For a conditional geometric lifetime

```text
Q_x{N>j}=r^j,
```

the surviving full-label density is one on every record, yet

```text
H_live=1/(1-w_Z r)<infinity  iff  w_Z r<1.
```

The same identity works with nonconstant positive marks after replacing the
survival probability by the conditional charged survivor
`Q_x[g_j 1_{N>j}]`.  Frozen Round-39 clearance-rank tails do not estimate the
terminal insertion depth `N`, and no frozen row gives
`ess sup_x E_x[w_Z^N]` or its charged-sector analogue.

## 4. Lawful attenuation mechanisms

### 4.1 Direct sub-Markov survival

For a time-inhomogeneous sub-Markov path `P_(0:j)` and positive time charge
`W_j`, the exact potential is

```text
H=sum_j w_Z^j P_(0:j)W_j.
```

A pointwise bound

```text
P_(0:j)W_j <= C kappa_j,
sum_j w_Z^j kappa_j < infinity
```

pays the strong lift.  In the geometric case `kappa_j=kappa^j`, the familiar
threshold is `w_Z kappa<1`.  This estimate may arise from conditional killing
even though the labelled survivor density remains one.  Average total-mass
decay is not enough.

### 4.2 Doob/Lyapunov supersolution

Let `V_j>=W_j` and suppose

```text
P_j V_(j+1) <= kappa_j V_j.
```

Then

```text
P_(0:j)W_j <= V_0 product_(i<j) kappa_i.
```

For the unweighted source space `L1(mu)`, the lawful sufficient condition is

```text
V_0 in L-infinity(mu),
sum_j w_Z^j product_(i<j)kappa_i < infinity.
```

The weaker actual-vector condition `integral V_0 dmu<infinity` only pays one
input.  It does not give an `L1 -> strong` operator.  In stationary notation,
the minimal positive solution is the resolvent

```text
H=W+w_Z P H.
```

A bounded Lyapunov supersolution is sufficient, while the bounded minimal
solution itself is the exact condition.

### 4.3 One-shot departure telescoping

Let

```text
x_j(x)=Q_x[V_j 1_(live at j)]
```

be nonincreasing, and let the exact lost charge arriving at time `j+1` be
`d_(j+1)=x_j-x_(j+1)`.  Finite summation gives

```text
sum_(j=0)^N w_Z^(j+1)d_(j+1)
=w_Z x_0+(w_Z-1)sum_(j=1)^N w_Z^j x_j
 -w_Z^(N+1)x_(N+1).
```

Whenever the weighted live potential is finite, the boundary term vanishes and

```text
H_departure=x_0+(w_Z-1)H_live.
```

Therefore exact lost mass, or a uniformly bounded mark times lost mass, is paid
by the same bounded live potential.  This is a lawful use of terminal/switch
departures.  It does not pay an owner birth, and it does not materialize the
separate pre-regularization cemetery.

Bare telescoping is insufficient.  With

```text
x_j=w_Z^(-j)/(j+1)
```

the unweighted departures telescope to `x_0`, but both the weighted live series
and the weighted arrival series diverge harmonically.  Absorbing cemetery
occupancy is worse: one positive arrival repeated at all later times has charge
`sum_(j>=tau)w_Z^j=infinity`.

## 5. Seven-sector and sharp strong separators

On the typed direct sum put

```text
H_s(x)=sum_j w_Z^j P_(0:j)W_j^s(x),
H_total=sum_s H_s.
```

For the finite seven-sector list, `H_total in L-infinity` is equivalent to every
`H_s in L-infinity`; the exact norm uses their positive sum.  A base survival
estimate does not pay raw-`Z`, Orlicz or variation marks unless their charged
conditional survivors obey the corresponding estimate.

The Round-65 separator remains decisive.  On `X={1,2,...}` take

```text
mu{n}=3*4^(-n),  w_Z=3/2,
P_(0:j)(n,{n})=3^(-j),  W_j(n)=2^n.
```

Then `w_Z/3=1/2`, the one-time actual moment is `3`, and the complete weighted
charge of that one actual vector is `6`; nevertheless

```text
H(n)=2^(n+1)
```

is unbounded.  This simultaneously shows that a finite actual all-time moment,
an integrable Lyapunov function, and geometric mass loss do not provide the
strong `L1` operator.

For actual Gate 5 the frozen status is stricter still:

```text
fixed-j base owner law:                         finite
fixed-j complement/variation/common cost law:  finite
active-clock/raw-Z/power-Orlicz positive slice: not certified finite
pre-regularization cemetery arrival:            not materialized
conditional terminal/charged-survivor tails:    not certified
graph-supported common physical root kernel:    not certified
direct H_total in L-infinity:                   not evaluable/certified
```

## 6. Oriented positive pair and common mode

Let `mu^+,mu^-` be the Round-54 physical hit/miss pair with common total `m_p`,
and let `xi_j^f,xi_j^r` be the Round-61 cost pair.  Before either orientation can
enter the physical direct potential, an exact mass-preserving oriented bridge
must pass

```text
xi_j^f(X)=m_p=xi_j^r(X),
```

then the two orientation-specific label-marginal/RN rows, and then common-mode
equality on one immutable carrier.  Separate upper bounds do not prove the
scalar equality and cannot be divided by an absent positive lower bound for
`m_p`.

After that upstream bridge exists, the all-time positive requirement is

```text
H^+, H^-, H^common in L-infinity
```

on the same root.  Equivalently one may use signed law plus common mode, since

```text
mu^+=J^+ + lambda,
mu^-=J^- + lambda,
mu^++mu^-=|J|+2lambda.
```

Signed cancellation never pays `lambda`.  The frozen Round-63 cost-Jordan law
is not the physical Round-54 pair, so none of these physical potentials is
currently materialized.

## 7. Audit of F5/F6/F10/F11/F14/F15/F17/F18

| field | Round-67 exact effect | strict status |
|---|---|---|
| F5 | direct potential supplies no global inverse-Jacobian row | open |
| F6 | supplies no all-record distortion sum | open |
| F10 | exact target is the complement/cut/cemetery part of `H_total`; actual marks/tails absent | open |
| F11 | no branch-uniform physical test pullback is constructed | open |
| F14 | needs completed F10 plus a bounded recovered strong block | open |
| F15 | raw-`Z`/Orlicz/recovery/cemetery sectors remain unpaid | open |
| F17 | physical oriented carrier and all-input strong current remain absent | open |
| F18 | the seven preceding rows still do not coexist on one actual block | open |

The new direct criterion is an exact interface, not a completed field.  Gate-5
maturity therefore remains `10/18`.

## 8. Technology boundary

The dominated-kernel, Lyapunov and Feynman--Kac technology already audited in
Rounds 63--66 begins after a physical positive kernel, potential and drift row
have been supplied.  The direct resolvent above is the maximal conclusion
available without importing a different process or changing the source norm.
No external theorem is promoted by this leaf.

## 9. Strict frontier

```text
direct positive-potential operator iff:            CERTIFIED_EXACT
recordwise G bounded is exact physical iff:         CERTIFIED_FALSE
unit-live terminal exponential-moment identity:     CERTIFIED_EXACT
direct attenuation despite survivor RN density 1:   CERTIFIED_POSSIBLE
bounded Lyapunov/Doob sufficient interface:          CERTIFIED_EXACT
integrable V_0 suffices for L1 strong operator:      CERTIFIED_FALSE
weighted one-shot departure identity:                CERTIFIED_EXACT
bare/unweighted telescoping pays w_Z>1:               CERTIFIED_FALSE
absorbing cemetery occupancy if nonzero:              DIVERGES

actual graph-supported root kernel/all sector marks:  NOT_MATERIALIZED
actual conditional terminal/sector tail:              NOT_CERTIFIED
actual H_total in L-infinity:                         NOT_CERTIFIED
physical oriented total/two-RN/common-mode bridge:    NOT_CERTIFIED

remaining fields:                                    F5/F6/F10/F11/F14/F15/F17/F18
Gate-5 maturity / complete blocks:                    10/18 / 0
complete composite gates:                             0/5
CM2:                                                   NO-GO_FOR_CLAIM
```

## 10. Shortest lawful continuation

1. build one graph-supported actual root kernel carrying terminal, owner,
   insertion, sector and orientation tokens;
2. materialize every positive fixed-time mark, especially raw-`Z`, Orlicz and
   pre-regularization cemetery arrival;
3. prove directly either `H_total in L-infinity`, a uniform conditional charged
   terminal-moment bound, or a bounded sectorwise Lyapunov supersolution;
4. use the weighted telescoping identity only for arrivals dominated by actual
   lost live charge, keeping owner births and pre-cemetery arrivals separate;
5. test `xi_j^f(X)=m_p=xi_j^r(X)`, the two RN rows and common mode before adding
   the physical oriented pair to the potential;
6. close F5/F6/F11/F17 independently and assemble all eight open fields into
   F18.

## 11. Executable evidence

The companion producer and independent verifier pin the frozen dependency
chain; replay exact geometric-lifetime, Lyapunov, weighted-telescoping,
seven-sector and strong no-go models; regenerate canonical JSON byte-for-byte;
reject hostile semantic and strict-JSON mutations; validate a five-row SHA
ledger; and fail closed by default with exit `2`.
