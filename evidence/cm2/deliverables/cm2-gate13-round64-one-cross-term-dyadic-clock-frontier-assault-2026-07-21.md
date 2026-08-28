# CM2 Round 64 Gate 1/3 — one-cross-term gauge and dyadic clock-trace frontier

Date: 2026-07-21  
Scope: append-only Gate-1/Gate-3 leaf from the frozen Round-63 aggregate and
independent audit  
Strict verdict: **Round 64 does not promote Gate 1 or Gate 3.  It joins the
previous physical clean-SFT one-sided Green gauges to the endpoint-defect
calculus and reduces their combined all-plaque class-`H` check to one scalar
unstable cross term.  A directly checkable strict scalar budget makes that
term vanish, while critical exact models show that equality can either
converge to a nonzero limit or oscillate.  On Gate 3, the safe stopped clock
is put in closed form and its time-labelled jump current is reduced to one
dyadic level-trace ledger whose cost is independent of the numerical jump in
collision time.  The existing weak-TV/F13/cemetery inputs do not control that
trace ledger, and anisotropic bulk Piola remains open.  Gate 1 and Gate 3 stay
`NOT_CERTIFIED`; complete composite gates stay `0/5`; CM2 stays
`NO-GO_FOR_CLAIM`.**

## 1. Frozen roots and physical-data audit

This leaf pins, without modifying, the complete Round-63 aggregate report
and recursive ledger, the Round-63 independent audit report/manifest/ledger,
and the final Round-63 Gate-1/3 report/manifest/ledger.  It also pins the
three older physical roots used for the two joins:

```text
variable-diagonal all-plaque Green frontier,
physical whole-family/Dbar grouping frontier,
same-ID all-five-face F13 Borel trace frontier.
```

The relevant frozen physical facts are exactly:

```text
finite faithful clean SFT for the actual derivative:                 CERTIFIED
faithful invariant-frame diagonal class-H representative:            CERTIFIED
lower and upper variable-diagonal Green gauges separately class H:   CERTIFIED_THEOREMS
combined U_v L_u cross-term convergence on every plaque:              NOT_CERTIFIED
selected twisting in that same combined representative:               NOT_CERTIFIED

integer-valued Borel M and safe Dbar on physical whole families:       CERTIFIED
actual stopped weak graph-TV restriction/assembly:                     NORM_ONE
base regular same-ID five-grammar F13 Borel charge and moment:          CERTIFIED
finite-s dyadic threshold traces and speeds:                            NOT_CERTIFIED
strong cemetery and anisotropic moving-domain Piola:                   NOT_CERTIFIED
```

No file in the frozen stack supplies numerical physical values for the new
strict Gate-1 scalar budget.  No file supplies a common finite-parameter
level-set atlas for the dyadic `M` faces.  Those absences are checked as
field absences, not filled by a literature citation.

## 2. Gate 1 — the combined Green gauge has one remaining scalar term

### 2.1 Exact relative matrix

On the pinned finite clean SFT, retain the two separately constructed
one-sided Green functions and choose the order

```text
D(z)=U_v(z)L_u(z)
    =[[1+v(z)u(z), v(z)],
      [u(z),        1   ]].                              (2.1)
```

For two endpoints write

```text
du=u_y-u_x,   dv=v_y-v_x.
```

Direct `2 x 2` multiplication, with no asymptotic omission, gives

```text
D_y D_x^(-1)
 =[[1+v_y du,  dv-v_y du v_x],
   [du,         1-du v_x      ]].                       (2.2)
```

The lower critical coordinate is the already solved `du`.  In the upper
critical coordinate, `dv` is the already solved one-sided upper Green term.
Therefore the only new noncommutative term is

```text
-v_y du v_x.                                           (2.3)
```

For a local unstable pair, put

```text
x_n=sigma^(-n)x, y_n=sigma^(-n)y,
R_n=the signed diagonal upper critical product,
T_n(x,y)=R_n^(-1) v(y_n)[u(y_n)-u(x_n)]v(x_n).          (2.4)
```

All other matrix coordinates are already covered by the two frozen
one-sided Green theorems and their opposite-direction contractions.
Consequently, on this clean-SFT construction, the combined gauge belongs to
class `H` precisely when `T_n` has the required uniform plaque limit and
uniform Holder modulus.  The limit need not be zero for class-`H`
membership.  It must be zero only for the stronger claim that the upper
canonical family is transported without an extra cross-term contribution.

This distinction corrects a dangerous quantifier collapse:

```text
T_n -> a nonzero Holder limit: compatible with class H;
T_n -> 0:                     sufficient for exact one-sided-family join;
T_n bounded:                  insufficient for either conclusion.
```

### 2.2 One strict scalar sufficient budget

Assume on every actual local unstable plaque of the clean SFT that

```text
|R_n(x)| >= rho_*^n,
|v| <= V,
|u(y_n)-u(x_n)|
  <=H_u lambda_u^(alpha n)d(x,y)^alpha,                (2.5)
```

where `rho_*>0`, `0<lambda_u<1`, and `alpha>0`.  Then (2.4) gives

```text
|T_n(x,y)|
 <=V^2 H_u (lambda_u^alpha/rho_*)^n d(x,y)^alpha.      (2.6)
```

Thus the single inequality

```text
q_cross=lambda_u^alpha/rho_* < 1                       (2.7)
```

forces uniform cross-term decay.  Together with the frozen one-sided
theorems it gives the combined clean-SFT class-`H` family and the exact join
of those one-sided canonical limits.  It is a conditional sufficient
criterion.  The physical constants in (2.5), the inequality (2.7), and the
selected twisting values for this combined representative are not present
in the frozen data.

The executable exact models set `V=H_u=d=1`, `R_n=rho_*^n`, and use the
actual `SL(2)` endpoints

```text
D_x=U_1,
D_y=U_1 L_(du_n),
D_y D_x^(-1)=[[1+du_n,-du_n],[du_n,1-du_n]].           (2.8)
```

They give four sharp regimes:

```text
rho_*=1/2, |du_n|=(1/4)^n: q=1/2, T_n=(1/2)^n ->0;
rho_*=1/4,  du_n=(1/4)^n: q=1,   T_n=1 ->1;
rho_*=1/4,  du_n=(-1/4)^n:q=1,   T_n=(-1)^n, no limit;
rho_*=1/4,  du_n=(1/2)^n: q=2,   T_n=2^n, unbounded.
```

Hence strictness is sharp for **automatic decay from the magnitude rows**.
At equality, convergence may hold or fail; `q<1` is not claimed necessary
for class `H`.

### 2.3 Strict Gate-1 boundary

The new join changes the remaining quantifier from an unspecified matrix
registry to one scalar sequence on the already constructed combined Green
gauge:

```text
exact U_v L_u relative-matrix reduction:                 CERTIFIED
only remaining combined-Green term T_n:                  CERTIFIED_EXACT
q_cross<1 sufficient and sharp for automatic decay:      CERTIFIED_CONDITIONAL
actual physical constants and q_cross<1:                 NOT_CERTIFIED
actual uniform Holder convergence of T_n:                NOT_CERTIFIED
selected nonzero twisting in that combined family:       NOT_CERTIFIED
actual compact-to-third plaque-tempered transport:        NOT_CERTIFIED
Gate 1:                                                   NOT_CERTIFIED
```

The result is subsystem-scoped to the pinned finite clean SFT.  It does not
create a full-mass physical PPE and does not rename arbitrary cylinder
markers as the immutable selected twisting loop.

## 3. Gate 3 — exact safe clock and the single dyadic trace ledger

### 3.1 Closed form of the frozen safe clock

The physical whole-family root defines

```text
C_p=4*10^90*360493663/358863,

Dbar(M)=0, if 2^M<=C_p,
Dbar(M)=min{d>=1:2^(M-d)<C_p/2}, otherwise.             (3.1)
```

Exact integer comparison gives

```text
2^310<C_p<2^311,
2^309<C_p/2<2^310.                                    (3.2)
```

Since `M-d` is an integer, (3.1) is therefore exactly

```text
Dbar(M)=0,       0<=M<=310,
Dbar(M)=M-309,   M>=311.                              (3.3)
```

Thus `R0=696 Dbar` first jumps from `0` to `1392` and every later dyadic
level changes it by `696`.  Formula (3.3) removes a minimisation and an
unbounded per-record search from the interface.  It does not supply a
finite-parameter trace theorem.

### 3.2 Collision-time distance is not a TV multiplier

At the dyadic threshold between two adjacent `M` strata, use the extended
stopped carrier with the immutable output-time tag.  With nonnegative
one-sided trace densities, the jump current is

```text
B_m=v_m[(Y_m^-)_*(rho_m^- trace_m)
       -(Y_m^+)_*(rho_m^+ trace_m)].                   (3.4)
```

The two time tags differ whenever `Dbar` differs.  Hence the two positive
measures in (3.4) are mutually singular on the extended carrier even if
their spatial landing points coincide.  Therefore

```text
||B_m||_TV
 =integral_(Gamma_m)|v_m|(rho_m^-+rho_m^+)dH.          (3.5)
```

There is no factor `|696 Dbar_+-696 Dbar_-|` in (3.5).  Total variation sees
two distinct atoms, not the metric distance between their integer labels.
The entire clock debt is exactly the single dyadic level-trace ledger

```text
E_clock^dyad
 =sum_(m>=310) integral_(Gamma_m)
    |v_m|(rho_m^-+rho_m^+)dH.                          (3.6)
```

Absolute finiteness of (3.6), on one common finite-`s` atlas with the actual
landing maps, pays the complete time-labelled clock current.  This replaces
an ambiguous “sum the clock jumps” obligation by one trace/coarea object.  It
does not pay the regular moving strong term, cemetery term, or bulk Piola.

### 3.3 Exact separator from weak TV, F13 and weak cemetery

The frozen weak restriction norm, the base regular F13 moment, and weak mass
cemetery do not imply (3.6).  For each finite `N`, partition `[0,1]` by

```text
e_k(s)=k/(N+1)+s, k=1,...,N,
```

with unit density and label the `N+1` cells by

```text
M_k=310+k,  k=0,...,N.
```

Use distinct landing/face tags at distinct cuts and the safe times from
(3.3).  Every cut has speed one and two unit traces.  Therefore

```text
weak source restriction TV =1,
base regular F13 charge     =0,
weak cemetery mass          =0,
E_clock^dyad                =2N.                       (3.7)
```

All records are finite and all clock labels are legitimate; the replay uses
`N=1,2,4,8,16,32`.  This is a logical finite stopped-atlas model, not a
billiard realization.  It proves that even arbitrarily strong fixed-record
finiteness or base Borel charge cannot replace a uniform dyadic trace bound.

### 3.4 Strict Gate-3 boundary

After Round 64 the reduced strong ledger is typed as

```text
E_stop^red
 =E_regular,moving-strong + E_clock^dyad + E_cemetery,
plus the anisotropic bulk directional-Piola series.     (3.8)
```

Its state is

```text
safe Dbar closed form:                                  CERTIFIED
clock jump TV independent of collision-time distance:   CERTIFIED_EXACT
single dyadic trace ledger (3.6):                        CERTIFIED_INTERFACE
weak TV/base F13/weak cemetery -> (3.6):                CERTIFIED_FALSE
physical common finite-s level atlas and (3.6):          NOT_CERTIFIED
moving regular strong/cemetery sums:                     NOT_CERTIFIED
anisotropic bulk directional Piola:                      NOT_CERTIFIED
physical strong R_s/Q_s and MT_DQ:                       NOT_CERTIFIED
Gate 3:                                                   NOT_CERTIFIED
```

## 4. Technology boundary

The current literature surface changes none of the physical rows above.
The shrinking-boundary-hole work `arXiv:2604.19671v2` starts from regular
conditional families and does not provide a moving-scatterer finite-`s`
current atlas or anisotropic Piola derivative.  `arXiv:2606.10155v1` is a
transfer-operator/anisotropic-space review, not such a theorem.  The
canonical-holonomy reference `arXiv:1909.11548v2` defines the required
limits but does not solve the combined non-fibre-bunched Green cross term.
No external theorem is promoted.

## 5. Strict continuation

```text
Gate 1:                   NOT_CERTIFIED
Gate 3:                   NOT_CERTIFIED
complete composite gates: 0/5
CM2:                      NO-GO_FOR_CLAIM
```

The shortest remaining routes are now:

1. On Gate 1, compute certified physical values for `rho_*`, `lambda_u`,
   `alpha`, `H_u`, and `V`, or directly prove uniform Holder convergence of
   the single scalar `T_n`; then evaluate the immutable selected twisting
   tokens in that same combined representative.
2. On Gate 3, construct one finite-parameter incidence-reduced atlas whose
   dyadic level traces pay (3.6), pay the strong cemetery and regular moving
   traces, and independently prove the anisotropic bulk directional-Piola
   sum.  Only then install strong `R_s/Q_s` and `MT_DQ`.

## 6. Executable evidence

- `cm2_gate13_round64_one_cross_term_dyadic_clock_frontier_cert.py`;
- `cm2_gate13_round64_one_cross_term_dyadic_clock_frontier_verifier.py`;
- `cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json`;
- `cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256`.

The producer and independent verifier pin the recursive roots, replay the
exact matrix identity, all four scalar regimes, the exact integer clock
formula and the finite dyadic-trace separator, require canonical strict
JSON, reject semantic and parser mutations, re-emit byte-for-byte, expose
compatible `--emit`/`--verify` modes, and fail closed with default exit `2`.
