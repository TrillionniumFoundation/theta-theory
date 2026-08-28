# CM2 Gate 1: resonant logarithmic-gauge frontier assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: v52 and the canonical QNL resonance manifest were read only  
Strict verdict: **the QNL natural-gauge obstruction has an explicit local
two-axis `C^{1,alpha}` logarithmic-gauge repair, but a global faithful class-`H`
coding, all-pairs holonomies, Gate 1 and CM2 remain `NOT_CERTIFIED`**

## 1. Result

The exact `325/144` increment is a genuine resonance, but it is not an
absolute Hölder-cohomology obstruction.  The exact cubic jet also has the
reversible unstable coefficient

```text
F_1,xxy/lambda=325/72,   F_2,xyy/mu=-325/72.
```

On the local stable coordinate the critical homological solution is

```text
t(y)=k y^2 log|y|,
k=g/(mu log(mu))=-325/(144 log(mu)).
```

The triangular fiber gauge

```text
B(y)=I+t(y)E_21
```

removes the complete stable resonant quadratic term exactly.  The symmetric
unstable gauge

```text
B_u(x)=I+k x^2 log|x| E_12,
k=325/(144 log(lambda))=-325/(144 log(mu))
```

removes the unstable term.  Their product `B(x,y)=B_u(x)B_s(y)` has
determinant one.  It extends `C^1` at
the QNL point and is `C^{1,alpha}` for every `alpha<1`, but is not `C^2`.
For the actual analytic non-grazing circular-billiard branch, the critically
amplified entry gains one power on each axis.  The transformed local canonical
increments are absolutely summable forward on the stable axis and backward
on the unstable axis, so both local QNL tails converge in this gauge.

This repairs only the two selected local QNL tails.  No global finite Markov
coding, common gauge on every stable/unstable pair, Hölder holonomy family,
typed QNL homoclinic loop or Butler--Park class-`H` object is constructed.
Park--Piraino fiber bunching on the two natural codings remains impossible,
because a same-coding cohomology cannot change the periodic eigenvalue ratio.

## 2. Exact resonant homological identity

Write

```text
A=diag(lambda,mu),  lambda*mu=1,  0<mu<1,
M_2(y)=A+g y^2 E_21,  g/mu=-325/144.
```

Since `E_21^2=0`,

```text
B(y)^-1=I-t(y)E_21
```

exactly.  The lower-left coefficient of
`B(mu y)^-1 M_2(y) B(y)` is

```text
g y^2+mu t(y)-lambda t(mu y).
```

For `t(y)=k y^2 log|y|`,

```text
lambda t(mu y)-mu t(y)
 = mu k y^2(log|y|+log(mu))-mu k y^2 log|y|
 = mu k log(mu) y^2
 = g y^2.
```

Therefore

```text
B(mu y)^-1 M_2(y) B(y)=A
```

exactly.  By contrast, for every smooth quadratic trial `t(y)=c y^2`,

```text
lambda t(mu y)-mu t(y)=0.
```

Thus no `C^2` quadratic jet can change the resonant coefficient; the
logarithmic regularity loss is the precise escape from that resonance.

On the unstable axis write

```text
M_u,2(x)=A+g_u x^2 E_12,  g_u/lambda=325/144.
```

The lower-left calculation has the exact upper-right counterpart

```text
mu t(lambda x)-lambda t(x)=g_u x^2.
```

Since `lambda=1/mu`, its coefficient is the same

```text
k=g_u/(lambda log(lambda))
 =325/(144 log(lambda))
 =-325/(144 log(mu)).
```

Thus `B_u(lambda x)^-1 M_u,2(x)B_u(x)=A` exactly, and the backward unstable
truncation is constant.  A smooth quadratic upper-triangular gauge is again
annihilated by the resonance and cannot change `g_u`.

## 3. Gauge regularity

Set `t(0)=0`.  For `y!=0`,

```text
t'(y)=k(2y log|y|+y),
t''(y)=k(2log|y|+3).
```

Hence `t'(y)->0`, so `t` is `C^1` with `t'(0)=0`.  The elementary bound

```text
r|log r|=O(r^alpha),  0<alpha<1,
```

shows that `t'` is locally `alpha`-Hölder for every `alpha<1`.  Since
`t''` is unbounded, the gauge is not `C^2`.  Its determinant is one, so it
is invertible without shrinking for algebraic reasons; a local neighborhood
is used only to stay on the selected analytic billiard branch.

## 4. Actual analytic QNL tail

The circular-scatterer collision map is real analytic on every fixed
non-grazing branch.  The QNL orbit is strictly non-grazing, and its analytic
local stable graph gives

```text
S(y)=mu y+O(y^3).
```

The frozen exact jet and vanishing quadratic derivatives give, along that
graph,

```text
DF(y)=A+
  [ O(y^2)       O(y^2)     ]
  [ g y^2+O(y^3) O(y^2)     ].
```

Conjugating by `B` cancels `g y^2` exactly.  The substitution
`S(y)=mu y+O(y^3)` changes `t(mu y)` only by `O(y^4|log|y||)`.  Thus the
transformed entries have the conservative orders

```text
21: O(y^3|log|y||),
diagonal: O(y^2|log|y||),
12: O(y^2).
```

The frozen stable-orbit lemma gives the stronger two-sided asymptotic
`y_n/mu^n -> c(z)!=0` for every local nontrivial stable point.  In particular
`y_n=O(mu^n)` and `|log|y_n||=O(n)`.  The canonical conjugation amplifies only
the `21` entry by `(lambda/mu)^n=mu^-2n`.  The three envelopes become

```text
21:       O(n mu^n),
diagonal: O(n mu^(2n)),
12:       O(mu^(4n)).
```

They are absolutely summable, with exact scalar majorants

```text
sum_(n>=1) n mu^n    = mu/(1-mu)^2,
sum_(n>=1) n mu^(2n) = mu^2/(1-mu^2)^2,
sum_(n>=1) mu^(4n)   = mu^4/(1-mu^4).
```

The infinite product of transformed stable increments therefore converges.
Applying the symmetric calculation to the inverse branch gives the same
`O(n mu^n)` critical envelope and convergence for the local unstable tail.
This is the first explicit local gauge in the certificate stack that restores
both QNL canonical tails.  It does not alter the already certified fact that
the stable tail diverges in the frozen natural gauge.

## 5. Why Gate 1 is still open

Butler--Park class `H` requires common stable and unstable canonical
holonomies for every relevant pair, with Hölder dependence and a faithful
symbolic cocycle.  The present gauge is constructed only in one local QNL
stable chart.  Completion still requires:

1. a finite faithful coding of the physical billiard derivative;
2. one compatible gauge across all chart overlaps and periodic fibers;
3. all-pairs stable and unstable Hölder holonomies;
4. a genuine QNL homoclinic occurrence carrying the already certified
   pinching/twisting data in that same gauge;
5. the projective spectral-gap/PPE conclusion on the physical full-mass
   quotient.

The periodic fiber-bunching inequality on the two frozen natural codings
remains false under every same-coding cohomology.  The new route is therefore
specifically a non-fiber-bunched class-`H` route, not a Park--Piraino repair.

## 6. Latest technology audit

The arXiv API was re-audited on 2026-07-16.  No new theorem supplies the
global extension above.

- `arXiv:2605.11848v2` constructs positive-entropy bounded-orbit measures for
  continuous cocycles, not canonical holonomies or projective spectral gaps.
- `arXiv:2606.15718v2` proves persistence of exponential separation under
  perturbation, assuming an existing separated cocycle; it does not solve the
  resonant holonomy equation.
- `arXiv:2607.06242v2` concerns coupling and large deviations for Markov
  cocycles in random environments, aimed at SPDEs, not singular billiard
  derivatives or prescribed periodic fibers.
- The closest Gate-1 theorem remains Butler--Park `arXiv:1909.11548v2`; the
  local logarithmic repair addresses one of its canonical tails but not its
  global class-`H` hypotheses.

## 7. Exact boundary

```text
NATURAL-GAUGE QNL STABLE CANONICAL LIMIT:            DOES NOT CONVERGE
EXACT STABLE/UNSTABLE CUBIC RESONANCES:              CERTIFIED
EXACT TWO-AXIS LOG-GAUGE HOMOLOGICAL IDENTITIES:     CERTIFIED
LOCAL C^{1,alpha} GAUGE, EVERY alpha<1:              CERTIFIED
TRANSFORMED ANALYTIC QNL STABLE TAIL:                CONVERGENT
TRANSFORMED ANALYTIC QNL UNSTABLE TAIL:              CONVERGENT
GLOBAL FAITHFUL SYMBOLIC CODING:                     NOT CERTIFIED
ALL-PAIRS STABLE/UNSTABLE HOLDER HOLONOMIES:         NOT CERTIFIED
GLOBAL BUTLER--PARK CLASS H:                         NOT CERTIFIED
PARK--PIRAINO FIBER BUNCHING ON NATURAL CODINGS:    NO-GO
GATE 1:                                             NOT CERTIFIED
UNCONDITIONAL CM2:                                  NO-GO FOR CLAIM
```

## 8. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_resonant_log_gauge_frontier_cert.py \
  deliverables/cm2_gate1_resonant_log_gauge_frontier_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_resonant_log_gauge_frontier_verifier.py \
  --replay --integrity-only

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_resonant_log_gauge_frontier_verifier.py \
  --self-test

# Expected exit 2: global Gate 1 remains fail-closed.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_resonant_log_gauge_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-resonant-log-gauge-frontier-manifest-2026-07-16.sha256
```
