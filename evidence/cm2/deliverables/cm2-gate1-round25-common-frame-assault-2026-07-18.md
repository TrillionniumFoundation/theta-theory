# CM2 Gate 1 round 25: positive big cell and same-representative common-frame join

Date: 2026-07-18 (Asia/Shanghai)  
Frozen root: `cm2-twenty-fourth-direct-assault-manifest-2026-07-18.sha256`  
Strict verdict: **the compact QNL logarithmic gauge that already carries the
selected local canonical holonomies and four nonzero twisting wedges lies
uniformly in one positive Gauss big cell.  It has an exact determinant-one
biprojective half-density frame factor with `q>999/1000`.  This closes the
big-cell/common-frame typing gap for that specific physical candidate.  The
same candidate is nevertheless already proved not to belong to class `H` on
the frozen connector common basic set, so the coupled all-plaque equations,
Gate 1, and CM2 remain fail-closed.**

## 1. One frozen gauge, not a cross-representative splice

The compact section gauge is

```text
G=U_v L_u=(I+v E_12)(I+u E_21)
 =[[1+uv,v],[u,1]],
u=chi k y^2 log|y|,
v=chi k x^2 log|x|.
```

The dependency hashes and the compact gauge internal digest bind the
following results to this same gauge:

1. canonical stable and unstable limits for every pair on the corresponding
   local QNL plaques;
2. the immutable selected QNL homoclinic loop and its direct two-sided tail;
3. all four nonzero QNL eigen-axis twisting wedges; and
4. the connector stable-tail divergence on the previously frozen common
   basic set containing the connector.

This is stronger than merely observing that the twisting and class-`H`
representatives are cohomologous.  The positive local holonomy/twisting
facts and the negative connector fact concern the same compact product
gauge.  The faithful diagonal class-`H` representative remains a different
representative and still has zero same-axis twisting.

## 2. Uniform positive big cell

Choose the standard compact cutoff with

```text
0<=chi<=1,
chi=1 on U_core,
chi=0 on the boundary collar of U_chart.
```

The frozen chart radius is `10^-10`, and the 5000-bit Arb coefficient
enclosure gives `0<k<1`.  For `0<r<=10^-10`, the function
`-r^2 log r` is increasing.  Moreover the entirely rational exponential
witness

```text
exp(3)>1+3+9/2+27/6=13>10
```

implies `log 10<3`.  Hence

```text
|u|,|v| < 10^-19 log(10) < 3*10^-19 < 10^-18,
|uv| < 10^-36.
```

Put `d=1+uv`.  Then `d>0` on the whole supported chart and `d=1` outside
it.  Define

```text
u_bip=u/(1+uv),
v_bip=v,
q=1-u_bip v_bip=1/(1+uv).
```

The strict uniform estimate is

```text
q > 1/(1+10^-36) > 999/1000.
```

Thus the formerly open **uniform big-cell lower bound is now certified for
this compact twisting candidate**.  It is not claimed for every possible
future gauge.

## 3. Exact common-frame factorisation

With `f=sqrt(1+uv)=q^(-1/2)`, direct `2x2` multiplication gives

```text
G
= q^(-1/2) [[1,v_bip],[u_bip,1]]
  diag(sqrt(1+uv),1/sqrt(1+uv)).
```

Both factors have determinant one, and the diagonal factor is everywhere
positive.  The biprojective factor has the determinant-one frame columns

```text
a=q^(-1/2)(1,u_bip)^T,
b=q^(-1/2)(v_bip,1)^T,
det(a,b)=1.
```

The producer and independent verifier replay the identity over the
rationals at

```text
u=7/9, v=1, d=16/9, sqrt(d)=4/3,
u_bip=7/16, q=9/16.
```

No numerical square root or floating comparison is used in that algebraic
replay.

This is an exact factorisation of the already frozen physical gauge `G`.
It does **not** assert that the biprojective factor by itself inherits the
four twisting intervals; that would require a canonical-holonomy transport
argument.  The frozen twisting belongs to the full product gauge `G`.

## 4. Decisive same-representative boundary

The join now has five positive candidate-interface layers:

```text
single determinant-one compact physical gauge:            CERTIFIED
uniform positive big cell and common frame:                CERTIFIED
canonical Hs/Hu on the local QNL plaques:                  CERTIFIED
typed selected immutable homoclinic loop:                  CERTIFIED
four nonzero selected twisting wedges:                     CERTIFIED
```

The sixth and decisive layer fails for this candidate:

```text
uniform all-plaque Butler--Park class H
in this same representative on the connector basic set:   REFUTED
```

At the connector fixed point the compact gauge is the identity on a
neighbourhood, while the frozen mixed jet is nonzero.  The canonical stable
increment obeys

```text
(K_n)_21=-Lambda*(Lambda/nu)^n*b_21(y_n),
b_21(y)=c y+O(y^2),
y_n~d nu^n,

(K_n)_21 ~ -Lambda*c*d*Lambda^n.
```

It is unbounded, so the stable canonical limit cannot converge there.  The
new positive `q` bound does not repair this exponent obstruction.

Accordingly, the candidate-interface maturity is exactly `5/6`, with the
missing global slot refuted for this particular gauge.  This is **not** an
official Gate-1 fraction: Gate 1 remains `0/1`, and the global core-gate
count remains unchanged.

## 5. Strict non-promotion

```text
all-plaque coupled half-density equations:              NOT_CERTIFIED
uniform all-plaque Holder holonomies in twisting gauge: NOT_CERTIFIED
another third gauge with both class H and twisting:     NOT_CERTIFIED
full-mass physical projective PPE:                      NOT_CERTIFIED
Gate 1:                                                 NOT_CERTIFIED
CM2:                                                    NO-GO FOR CLAIM
```

The shortest remaining constructive route is now narrower.  It must change
the critical jet at the connector (or exclude it on a rigorously adequate
same physical basic set), while preserving the selected loop, and then solve
the stable and unstable all-plaque common-frame equations with uniform
Hölder bounds.  Merely shrinking the amplitude or proving `q>0` cannot do
that.

## 6. Replay

Use Python 3.12 with the frozen workspace dependencies:

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python -m py_compile \
  deliverables/cm2_gate1_round25_common_frame_cert.py \
  deliverables/cm2_gate1_round25_common_frame_verifier.py

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round25_common_frame_verifier.py --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round25_common_frame_verifier.py --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round25_common_frame_verifier.py --self-test

# Expected live fail-close: exit 2.
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round25_common_frame_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-round25-common-frame-manifest-2026-07-18.sha256
```
