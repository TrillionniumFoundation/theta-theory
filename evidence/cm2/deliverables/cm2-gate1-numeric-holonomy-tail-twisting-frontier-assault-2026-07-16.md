# CM2 Gate 1: numerical QNL holonomy-tail and selected twisting assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: the immutable homoclinic, compact logarithmic-gauge, exact
resonance, physical replay, graph, connector and shadow stacks were read only  
Strict verdict: **the selected immutable QNL homoclinic loop now has a direct
two-sided numerical enclosure and four nonzero QNL eigen-axis twisting
wedges; global class `H`, Gate 1 and unconditional CM2 remain
`NOT_CERTIFIED`**

## 1. Result

The preceding immutable-orbit certificate selected the unique physical point
`z_h` on the actual local unstable graph for which

```text
T^96 z_h = I z_h,       F=T^2,       F^48 z_h=I z_h.
```

It proved that the compact-gauge homoclinic holonomy `psi_z:E_p->E_p` exists,
but it stopped before a numerical matrix because its QNL-tail estimates were
only qualitative.  This assault supplies the missing constants.

At depth `N=260`, a 5000-bit correlation-preserving Arb replay certifies the
unique pre-tail point

```text
w_N=F^(-260) z_h,
x(w_N) = -1.439318702793738701001244647611699402587...e-286,
root radius = 1e-400.
```

The half excursion contains 568 physical collisions and the full reversible
excursion contains `2N+48=568` returns of `F`.  Its two shooting faces have
momenta

```text
left  = -1.279209815618811637247950618413386262603...e-101,
right = +1.279209815618811637247950618413386262603...e-101,
```

while the derivative along every admissible graph has a strict positive
Arb lower bound.  All frozen flight, discriminant, incidence and clearance
margins remain strict.  Replaying the first 260 returns gives

```text
x_prefix-x(z_h center)
 = -1.1732640510476685192599251782769920...e-67
   +/- 4.98e-117,
```

so the entire Arb interval lies strictly inside the previously frozen
`z_h` radius `1e-50`, not merely inside a looser display tolerance.  Its
graph ordinate also lies in the frozen graph tube.

The displayed decimal is only the centre of an enclosing rectangle; the
proof never substitutes it for the unknown analytic graph ordinate.  On the
whole rectangle the frozen theorem gives `|h_u(x)|<=x^2` and
`|h_u'(x)|<=1e-4`.  The opposite face signs hold uniformly over that entire
ordinate tube, and the lower bound

```text
partial_x shooting - |partial_y shooting|*1e-4 > 0
```

holds on the whole rectangle.  The intermediate-value theorem on the actual
graph gives existence, and this strict derivative gives uniqueness.  The
prefix replay then identifies that unique deep root with the unique frozen
`z_h` occurrence.  No point-valued approximation to `h_u` is assumed.

The directly enclosed finite loop, in the canonical QNL eigenfiber `E_p`, is

```text
psi_260 =
[  7.229574772903447875081430851836658...e2    -1.734476789206717359495827495109825...e-28 ]
[ -4.909881822280033567276963020729284...e77    +1.177949786260054584434662602082016...e47 ].
```

The two infinite tail products change each matrix entry by at most

```text
8.567025181664067265507817354450332e-49.
```

Consequently all four eigen-axis wedges are strictly nonzero.  The smallest
one has magnitude greater than `1.7344767892067172e-28`, leaving more than
sixteen decimal orders beyond the deliberately enlarged tail error.

## 2. The coordinate conversion that must not be skipped

The physical invariant-graph replay uses coordinates `(x_g,y_g)` defined by

```text
s=x_g+y_g,       p=kappa(x_g-y_g).
```

The frozen exact `325/144` resonance proof uses a differently scaled canonical
eigenbasis.  Direct comparison of the two exact linear changes gives

```text
(x,y)=(x_g,-2*kappa*y_g).
```

Thus the billiard involution is a swap in graph coordinates but is

```text
R = [ 0             -1/(2*kappa) ]
    [ -2*kappa       0             ]
```

in the canonical resonance coordinates.  The certificate checks `R^2=I`
entry by entry.  It also converts every Taylor coefficient before applying
the logarithmic gauge.  In particular it recovers, in the same fiber used by
the frozen resonance proof,

```text
g_u/lambda =  325/144,
g_s/mu     = -325/144.
```

Using the graph-coordinate swap together with the canonical gauge would give
the wrong cubic coefficient and wrong wedge signs.  This conversion is part
of the certified computation, not a display convention.

## 3. Finite reversible excursion

Let `H` be the derivative of the 568-collision half excursion from `w_N` to
`Fix(I)`.  Exact preservation of `ds wedge dp` gives `det(H)=1`; the fourth
entry is reconstructed as

```text
H_22=(1+H_12 H_21)/H_11
```

and is checked against the independently propagated interval.  Reversibility
then gives the full derivative without a second long replay:

```text
D F^(2N+48)(w_N) = R H^(-1) R H.
```

On the `chi=1` core the compact gauge is

```text
B(x,y)=B_u(x)B_s(y),
t(r)=k r^2 log|r|,
k=-325/(144 log(mu)),
det(B)=1.
```

Finite-word gauge factors telescope, so the correctly typed truncation is

```text
psi_N = A^(-(N+48))
        B(Iw_N)^(-1) D F^(2N+48)(w_N) B(w_N)
        A^(-N),
A=diag(lambda,mu).
```

Here the exponents are forced by the orbit typing.  Starting at
`w_N=F^-N z_h`, the orbit uses `N` returns to reach `z_h`, `48` returns to
reach `I z_h`, and another `N` returns to reach `I w_N`; hence the middle
cocycle has exactly `2N+48` returns of `F`.  The two finite holonomy
approximants are

```text
H^u_N(p,z_h)=A_hat^N(w_N) A^(-N): E_p -> E_z,
H^s_N(z_h,p)=A^(-(N+48)) A_hat^(N+48)(z_h): E_z -> E_p.
```

Their typed composition and the cocycle identity give

```text
H^s_N H^u_N
 =A^(-(N+48)) A_hat^(2N+48)(w_N) A^(-N),
```

after which the finite gauge telescope produces the displayed `B(Iw_N)^-1`
and `B(w_N)` factors.  Thus neither `N+48` nor `2N+48` is a collision/return
conversion convention: both are checked `F`-return counts in the immutable
phase.

This formula maps `E_p` to `E_p`; it is not the raw physical excursion matrix
and it is not identified with the older periodic-shadow matrix.

## 4. Numerical infinite-tail lemma

The certificate differentiates the exact non-grazing `G-W-G` branch with a
two-variable interval Taylor algebra through total degree four on

```text
|x|,|y| <= 1e-10.
```

After conversion to canonical coordinates it obtains

```text
max |D^3 F| < 806443,
max |D^4 F| < 620,
|subordinate graph coordinate| <= 14 r^2,
lambda < 12,
|k| < 1.
```

All quadratic Taylor terms vanish.  Put `G=2*kappa<14`,
`S=1+G*1e-10`, and let `M_3,M_4` be the displayed derivative bounds.  The
certificate first computes the following separate positive ledgers:

```text
C_F  = M_3 S^3/6,
C_D  = M_3 S^2/2,
C_cr = M_3(G+G^2*1e-10/2)+M_4 S^3/6.
```

They certify, respectively,

```text
|F(z)-Az| <= C_F r^3,
||DF(z)-A||_max <= C_D r^2,
|D_crit(z)-g r^2| <= C_cr r^3
```

after the subordinate graph coordinate is inserted.  If
`X=lambda*x+R_X`, then `|R_X|<=C_F r^3`.  The scalar inequalities

```text
|t(u)|  <= |k| |u|^2(1+|log|u||),
|t(X)-t(lambda*x)|
 <= |k| sup_(|u|<=A r)|u|(3+2|log(A r)|) |R_X|,
A=lambda+C_F(1e-10)^2,
```

produce independent gauge-composition and gauge-difference ledgers.

For the unstable critical entry the certificate expands the matrix product
exactly as

```text
(B(Fz)^-1 DF(z) B(z))_12
 = b+a t(x)-t(X)(c t(x)+d).
```

It subtracts

```text
g_u x^2+lambda t(x)-mu t(lambda*x)=0
```

before applying any absolute values.  The five surviving classes are:

1. the `C_cr r^3` cubic derivative remainder;
2. `mu[t(lambda*x)-t(X)]`;
3. `(a-lambda)t(x)`;
4. `-t(X)(d-mu)`;
5. `-t(X)c t(x)`.

The stable `21` entry is the reversible counterpart using
`g_s y^2+mu t(y)-lambda t(mu*y)=0`.  Every other entry is bounded directly
from

```text
B(Fz)^-1(DF-A)B(z)+(B(Fz)^-1 A B(z)-A)
```

with the matrix infinity norm.  These are separately recorded in the JSON
as `unstable_critical_explicit_ledger` and
`noncritical_explicit_ledger`.

Taylor's theorem, the graph substitution, the two triangular shears and
their exact inverses then give, on either local graph,

```text
critical entry:    |delta_crit| <= C r^3(1+|log r|),
other entries:     |delta_ij|   <= C r^2(1+|log r|).
```

After the two exact cancellations, fully expanding `B_u B_s`, its exact
inverse, `DF`, and the reversible stable formula gives fewer than `2^12`
scalar monomials.  The largest factor degree is five: the stable `21`
expansion contains the explicit term

```text
t(X)t(Y)c t(x)t(y).
```

All other expanded monomials have degree at most five as well.  The
certificate therefore bounds the expansion by

```text
2^12 (1+sum of the explicit positive category ledgers)^5.
```

This is a finite algebraic domination tied to the displayed matrix formulas,
not an unspecified asymptotic constant.  Its numerical value is checked
against the JSON `derived_product_ledger`; the certificate deliberately
rounds it upward to

```text
C=1e80.
```

The replayed graph transform supplies the inverse contraction
`q=0.091`.  Hence the critical conjugated ratio satisfies

```text
rho=lambda^2 q^3 < 0.09281 < 1/10.
```

Writing `r_0=2*kappa*|x(w_N)|` and `L_0=1+|log r_0|`, the two scalar sums used
by the verifier are

```text
S_crit,R <= C lambda^(2N+1) r_0^3
          [ L_0/(1-rho) + |log q| rho/(1-rho)^2 ],

S_crit,L <= lambda^96 S_crit,R,

S_diag <= C lambda r_0^2
          [ L_0/(1-q^2) + |log q| q^2/(1-q^2)^2 ].
```

The fixed `lambda^96` in the left tail is essential.  Four times the
appropriate critical sum plus `S_diag` bounds each matrix infinity-norm
exponent separately.  At `N=260`,

```text
E_R < 7.933e-227,
E_L < 1.745e-126,
||P_R-I||_infinity <= exp(E_R)-1,
||P_L-I||_infinity <= exp(E_L)-1.
```

More explicitly, adding one pre-tail return gives the exact recursion

```text
psi_(n+1)=S_n psi_n U_n,
U_n=A^n A_hat(w_(n+1)) A^(-(n+1)),
S_n=A^(-(n+49)) A_hat(Iw_n) A^(n+48).
```

The critical `12` entry of `U_n` acquires `lambda^(2n+1)`.  In contrast, the
critical `21` entry of `S_n` acquires

```text
mu^(-(n+49)) lambda^(n+48)=lambda^(2n+97).
```

Thus the left series is exactly the displayed `lambda^96` enlargement of
the common critical majorant.  Diagonal entries acquire no exponential
factor, and the opposite off-diagonal entries decay.  For a sequence with
`sum ||K_n-I||<=E`, repeated submultiplicativity gives

```text
||product K_n|| <= exp(E),
||product K_n-I|| <= exp(E)-1.
```

If `eta_R=exp(E_R)-1` and `eta_L=exp(E_L)-1`, the two-sided loop error is
bounded by

```text
||psi-psi_N||_infinity
 <= ||psi_N||_infinity ((1+eta_L)(1+eta_R)-1)
 < 8.568e-49.
```

The complete tail lies inside radius `1e-12`, where the compact cutoff is
identically one.  Thus no unrecorded cutoff derivative enters these bounds.

## 5. Four selected twisting wedges

For the canonical eigenvectors `e_1,e_2`, the four intervals are

```text
wedge(e_1,psi e_1) < -4.9098e77,
wedge(e_2,psi e_1) < -7.2295e2,
wedge(e_1,psi e_2) >  1.1779e47,
wedge(e_2,psi e_2) >  1.7344e-28.
```

Each excludes zero after the full two-sided tail inflation.  This certifies
twisting for the selected immutable QNL homoclinic occurrence in the exact
QNL fiber.  Nonvanishing, rather than a coordinate-dependent sign pattern,
is the invariant conclusion.

## 6. Exact remaining boundary

This closes the numerical `H^u`, `H^s`, `psi_z` and four-wedge blockers for
one selected local loop.  It does **not** close Gate 1.  Still missing are:

1. a faithful global physical coding;
2. compatible holonomies for every relevant stable and unstable plaque pair,
   with uniform Holder constants;
3. a global Butler--Park class-`H` cocycle on that coding;
4. the physical projective spectral-gap/PPE interface required downstream.

No equality with the older periodic-shadow matrix is claimed or needed for
the direct selected-loop computation.  Gate 1 and unconditional CM2 remain
fail-closed.

## 7. Replay

Use `python-flint==0.9.0`:

```bash
python deliverables/cm2_gate1_numeric_holonomy_tail_twisting_frontier_cert.py
python deliverables/cm2_gate1_numeric_holonomy_tail_twisting_frontier_verifier.py --replay
python deliverables/cm2_gate1_numeric_holonomy_tail_twisting_frontier_verifier.py --self-test
python deliverables/cm2_gate1_numeric_holonomy_tail_twisting_frontier_verifier.py
sha256sum -c deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256
```

The default verifier intentionally exits `2`: the selected loop and its four
wedges are certified, while global class `H`, Gate 1 and CM2 are not.
