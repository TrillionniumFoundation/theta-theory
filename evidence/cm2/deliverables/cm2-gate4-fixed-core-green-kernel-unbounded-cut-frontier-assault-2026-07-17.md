# CM2 Gate 4: fixed-core Green kernel and unbounded-cut threshold

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the fixed 24-core contraction, native levelwise moment, native
prefix antichain, and the new finite two-cut carrier outer  
Strict verdict: **the fixed core now has a summable unbounded-delay Green
kernel with a rational exponential moment.  A precise geometric-tail
criterion for unbounded new cuts is also closed, but no physical cut-count
tail or occurrence-to-core incidence is available, so native repeated
recovery and Gate 4 remain open.**

## 1. Exact Green kernel

For the fixed open operator `O=T_* o M_core`, the inherited adapted boundary
kernel is

```text
g_k=b_core^k,
b_core=720269600000/720626832337<1,
1-b_core=357232337/720626832337.
```

The arbitrary-time recurrence therefore has the exact delay moments

```text
sum g_k     = 720626832337/357232337,
sum k*g_k   = 519045600276638055200000
              ---------------------------------- .
                 127614942598481569
```

The tail is exactly `b_core^(L+1)/(1-b_core)`.  In particular every
polynomial transport-delay moment is finite.

## 2. Rational exponential moment

The frozen half-life gives `b_core^2018<1/2`.  Choose `gamma=1/4036`.  The
elementary series estimate

```text
e < 1+1+1/2+1/6+(1/24)sum_{j>=0}4^-j
  =49/18<25/9
```

implies `exp(1/2)<5/3`.  Hence one 2018-step weighted block is below `5/6`.
Grouping the series in those blocks gives the rational bounds

```text
sum exp(gamma*k) g_k       <= 20180,
sum k exp(gamma*k) g_k     <= 244339440,
weighted tail from block q <= 20180*(5/6)^q.
```

This is a genuine unbounded propagation-delay ledger, not only a bound for
each fixed `n`.

## 3. Summable transported injections

For any nonnegative injections `J_j` with `sum J_j<infinity`, put

```text
G_n=sum_{j<=n} b_core^(n-j)J_j.
```

Tonelli gives the exact zeroth and first delay bounds and the exponential
bound `sum exp((n-j)/4036)b_core^(n-j)J_j<=20180 sum J_j`.  Thus arbitrarily
many injection times are allowed whenever their total positive injection is
summable.

Conditionally, if the new common two-cut current with TV outer
`2590777728/5` were transported into the core with norm enlargement at most
one, its complete delay ledger would be bounded by

```text
total TV:       24246544771660906368/23196905,
first moment:   3492809820813258473063362560000
                ----------------------------------,
                    1657336916863397
exponential TV: 10456378910208.
```

That installation is not made: the transported physical incidence remains
missing.

## 4. New-cut count criterion

Propagation delay and the number of newly selected cuts are different axes.
For integer `H>=0`, if

```text
P(H>=h)<=C*rho^h,
```

then

```text
E[a^H]
 <=1+C*(a-1)*rho/(1-a*rho), provided a*rho<1.
```

The one-cut mass-weighted shell has `a=15/8`, so its unbounded repetition
requires `rho<8/15`.  Repeating the raw all-component field-7 bound would
require the far stronger `rho<1999/580000`.  Neither physical tail has been
certified.  This turns the old generic “missing unbounded-cut tail” into two
exact numerical thresholds.

```text
FIXED-CORE UNBOUNDED DELAY GREEN KERNEL:  CERTIFIED
SUMMABLE-INJECTION CONVOLUTION LEDGER:    CERTIFIED
UNBOUNDED NEW-CUT TAIL CRITERION:         CERTIFIED
OCCURRENCE-TO-CORE INCIDENCE:             NOT CERTIFIED
NATIVE UNBOUNDED REPEATED-CUT RECOVERY:   NOT CERTIFIED
COMPLETE C_fw,C_rev,q / GATE 4:           NOT CERTIFIED
```

## 5. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_cert.py \
  deliverables/cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_verifier.py \
  --self-test

# Expected exit 2: the native physical tail/incidence remains open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_verifier.py
```
