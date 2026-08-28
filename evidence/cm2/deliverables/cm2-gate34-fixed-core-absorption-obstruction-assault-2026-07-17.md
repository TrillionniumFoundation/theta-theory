# CM2 Gates 3/4: fixed-core absorption obstruction

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the 24 positive collision cores, the exact QNL period-two
branch, and the actual-parameter all-scale recovery germs  
Strict verdict: **the frozen 24-core union has positive collision-SRB mass
but is not a global absorbing trap.  The exact QNL period-two orbit avoids it
forever.  Therefore “propagate every regular state to a first 24-core” is a
false global lemma; the physical bridge must use branchwise core/cemetery
stopping or positive-fraction unnormalised recovery.**

## 1. The frozen core envelope

The fixed registry consists of 24 collision rectangles:

```text
8 axis cores:      1/100 <= t <= 1/50,
16 diagonal cores: 69/100 <= |t| <= 7/10.
```

All are positive compact subcores of distinct return-word keys.  Their union
has certified positive normalized collision-SRB mass greater than
`147/550000`.  Positive mass, however, is not the same as global absorption.

## 2. Exact avoiding orbit

At `s=0`, the centered normal branch is the exact period-two physical word

```text
G(0,0) -> W(0,0) -> G(0,0).
```

Its collision phases are

```text
G: n=( 1/sqrt(2),  1/sqrt(2)), p=0,
W: n=(-1/sqrt(2), -1/sqrt(2)), p=0.
```

Both points lie on dominant-chart seams.  Regardless of half-open seam
ownership, their collision coordinate satisfies

```text
|t|=1/sqrt(2)>7/10,
```

because `1/2>(7/10)^2=49/100`.  Hence neither phase belongs to an axis or
diagonal core rectangle.  Periodicity then gives

```text
tau_core(QNL)=infinity.
```

The finite QNL orbit itself has collision-SRB mass zero, so this does not
quantify the total non-returning cemetery.  It does rigorously refute an
all-state deterministic absorption claim.

## 3. Required recovery interface

The valid stopping object is

```text
tau_C(x)=inf{n>=0:T^n x in C},
cemetery={tau_C=infinity}.
```

For the 128 selected actual-parameter germs, one must now construct a
branchwise measurable stopping ledger and prove either:

- a charged tail for the core/cemetery decomposition; or
- a positive-fraction, record-preserving unnormalised recovery theorem that
  does not demand whole-tube absorption.

The QNL counterexample is not asserted to lie inside one of the selected
germs, so selected-germ reachability is neither proved nor refuted here.

## 4. Strict frontier

```text
EXACT QNL PERIOD-TWO ORBIT AVOIDS 24-CORE:       CERTIFIED
GLOBAL ALL-STATE FIRST-CORE ABSORPTION:          REFUTED
SELECTED 128-GERM CORE/CEMETERY LEDGER:          NOT CERTIFIED
QUANTITATIVE CEMETERY PAYLOAD:                   NOT CERTIFIED
NATIVE 2018/12108 NO-RECUT DWELL:                NOT CERTIFIED
GATE 3:                                          NOT CERTIFIED
GATE 4:                                          NOT CERTIFIED
```
