# CM2 Gate 4 product same-occurrence/joint-moment frontier assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault closes the joint endpoint-rank/stopped-depth estimate that was
still missing after the numerical Growth and recovery constants were frozen.
It uses the already certified, query-independent **product depth kernel**.
The product mark is fixed before orientation, time mode, linked query and
final test, and its same `(K,j)` record is transported through both
nonadditive views of one physical occurrence.

The strict result is:

```text
QUERY-INDEPENDENT PRODUCT SAME-OCCURRENCE RECORD:       CERTIFIED
NUMERIC JOINT (B,K) RECOVERY MOMENT:                   CERTIFIED
ONE REGISTERED CUT LEVELWISE BOUNDARY NUMERATOR:       CERTIFIED
FIXED FINITE-H REGISTERED RESTART MOMENT:              CERTIFIED
CONTROLLED PRODUCT GEOMETRIC/Z/CLOCK SUBCOSTS:         CERTIFIED
NATIVE FULL REWEIGHTED RECOVERY:                       NOT CERTIFIED
ARBITRARY OR UNBOUNDED REPEATED-INDICATOR RECOVERY:    NOT CERTIFIED
COMPLETE NUMERIC C_fw,C_rev AND FINAL q:               NOT CERTIFIED
GATE 4:                                                NOT CERTIFIED
```

The central new numerical estimates, before the fixed collision-flux
normalization, are

```text
gamma = 1/12060,

sum_K w_K 2^K exp(gamma(R_fw+R_rev))
  < 2*3^50,

integral 2^(B_s+K) exp(gamma(R_fw+R_rev)) d(m_s tensor w)
  < 31080151660381513756308599682583861157637/12800000,

one-cut levelwise boundary-numerator coefficient
  <= (3/2) C_mesh
   = 104979995960750899200
```

The last coefficient is **per unit incoming occurrence mass**.  It is not a
global mass with a silently omitted factor.

Evidence:

- `deliverables/cm2_gate4_product_same_occurrence_joint_moment_frontier_cert.py`;
- `deliverables/cm2_gate4_product_same_occurrence_joint_moment_frontier_verifier.py`;
- `deliverables/cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json`;
- `deliverables/cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.sha256`.

## 1. Frozen inputs and exact scope

The certificate pins six frozen dependencies.  The numerical inputs are:

```text
64 maximal physical occurrences,
one corrected positive m_e,s per occurrence,
same-occurrence forward/reverse nonadditive views,
w_K=(3/4)4^-K,
E[2^K]=3/2,
K independent of the physical row point,
same (K,j) mark in both orientations,
integral 2^B_s dm_s <= 43293270343755613/25600000,
C_fw^(geom),C_rev^(geom) <=204*2^B_s,
C_mesh=69986663973833932800,
A0=301500,
A1=1005.
```

The parameter-uniform rank and mesh estimates hold for `|s|<=1/400`.
The corrected 64-row current ledger supplies the occurrence identity and
single positive law.  This assault does not alter any frozen input.

## 2. One immutable product same-occurrence record

Extend each occurrence law by

\[
 d\widehat m_{e,s}(a,K)=dm_{e,s}(a)\,w_K,
 \qquad w_K={3\over4}4^{-K}.
\]

After sampling `K`, use the physical cumulative-mass coordinate and put

\[
 j=\lfloor2^K u_{e,s}(a)\rfloor,
 \qquad 0\le j<2^K.
\]

The immutable record is

```text
(occurrence e,s,K,j,owner,polarity,restriction).
```

It is fixed before orientation, time mode, linked product-time query and
final test.  The forward and reverse formulas transport the same restricted
measure and the same `(K,j)` record.  They are alternative representations
of one occurrence, never two additive copies.  Summing over `K,j` returns
exactly `m_e,s`.

This is a valid datum-independent product extension.  It is not relabelled
as a native orbit stopping antichain: `K` remains the already declared
product mark.

## 3. Explicit joint endpoint-rank/depth moment

For a depth-`K` atom, the numerical recovery clock gives

\[
 R_{\rm fw}+R_{\rm rev}
 \le2A_0+2A_1K
 =603000+2010K.                                      \tag{3.1}
\]

Take

\[
 \gamma={1\over12060}.
\]

Then

\[
 \gamma(603000)=50,
 \qquad \gamma(2010K)=K/6.                           \tag{3.2}
\]

No floating-point exponential estimate is used.  The elementary series
comparison gives `e<3`, while

\[
 3<(5/4)^6.
\]

Consequently

\[
 e^{50}<3^{50},\qquad e^{K/6}<(5/4)^K.               \tag{3.3}
\]

The product-depth series is therefore bounded by

\[
 \sum_{K\ge0}{3\over4}4^{-K}2^K
 e^{\gamma(603000+2010K)}
 <3^{50}{3\over4}\sum_{K\ge0}(5/8)^K
 =2\,3^{50}.                                         \tag{3.4}
\]

The crucial point is now exact: in the frozen product kernel `K` is
independent of the physical row point and hence of `B_s`.  Multiplying (3.4)
by the uniform endpoint-rank moment yields

\[
\begin{aligned}
 &\int 2^{B_s+K}e^{\gamma(R_{\rm fw}+R_{\rm rev})}
       \,d(m_s\otimes w)\\
 &\quad< {43293270343755613\over25600000}\,2\,3^{50}\\
 &\quad={31080151660381513756308599682583861157637
          \over12800000}.                            \tag{3.5}
\end{aligned}
\]

This closes the product-kernel joint `(B,K)` moment.  It does not infer a
joint moment for the native physical shell, where `B` and `K` need not be
independent.

## 4. Query-independent levelwise boundary numerator

For either orientation, each depth-`K` equal-mass atom obeys

\[
 Z_{\mathfrak o}(K,j)\le C_{\rm mesh}2^K.             \tag{4.1}
\]

At fixed `K`, the `2^K` atoms each have incoming mass fraction `2^-K`.
Thus their unnormalised boundary numerator is at most

\[
 C_{\rm mesh}2^K
\]

times the incoming occurrence mass.  Averaging over the product mark gives

\[
 C_{\rm mesh}\sum_Kw_K2^K
 ={3\over2}C_{\rm mesh}
 =104979995960750899200.                              \tag{4.2}
\]

Forward and reverse are controlled by one maximum on the common law, so
(4.2) is not doubled.

This is the first fully numerical, query-independent levelwise boundary
numerator for the registered product cut.  It does not say that an
arbitrary characteristic restriction has finite boundary numerator.

## 5. Fixed finite registered histories

Fix the finite history length `H` before the later query and presample the
finite vector `(K_1,j_1),...,(K_H,j_H)`.  Enforce the order

```text
registered cut
 -> retain immutable occurrence/restriction record
 -> recover both available orientations
 -> only then admit the next registered cut.
```

For every fixed finite `H`, independence gives

\[
 E\,2^{\sum_{i=1}^H K_i}=(3/2)^H,                    \tag{5.1}
\]

and (3.4) gives the explicit clocked bound

\[
 E\!\left[2^{\sum_iK_i}
 e^{\gamma\sum_i(R_{{\rm fw},i}+R_{{\rm rev},i})}\right]
 <(2\,3^{50})^H.                                     \tag{5.2}
\]

This certifies every separately predeclared fixed finite registered restart
history.  It does not construct one universal countable-fibre kernel from
which a later query may select `H`.  There is no tail on `H` in the current
physical record, so (5.2) is not uniform over an unbounded number of cuts.

## 6. A numerical controlled product subcost

The common conservative product envelope

\[
 C_{\rm prod}(s,a,K)
 :=2^K e^{\gamma(R_{\rm fw}+R_{\rm rev})}
 \max\{204\,2^{B_s(a)},C_{\rm mesh},2\}              \tag{6.1}
\]

dominates the already certified geometric, one-cut boundary and recovery
clock sublayers of either orientation.  Since `B_s>=20`, the total coarea
mass is at most

\[
 {43293270343755613\over26843545600000}.
\]

Using the maximum bounded by the sum and (3.4), one obtains

\[
 \int C_{\rm prod}\,d(m_s\otimes w)
 <{1087598065258783059015245434544676138185728521412801591795461
    \over6710886400000}.                              \tag{6.2}
\]

Thus the forward and reverse **controlled product geometric/Z/clock
subcosts** are numerical and one common maximum can be charged once.

Equation (6.1) is not named `C_fw` or `C_rev`.  The final CM2 costs must also
contain the complete recordwise strong-operator/source norm, every physical
test lift and exact propagated-current matching.  Those fields remain absent.

## 7. Exact remaining boundary

The product result does not remove the following strict blockers:

1. Materialising the countably infinite native initial partition as one
   family still gives time-zero `Z=infinity`.
2. One arbitrary open indicator can already give normalized `Z=infinity`;
   the repeated quarter-cut counterexample remains `Z_h=4^h`.
3. The fixed-`H` estimate has no summable physical tail on unbounded `H`.
4. The Gate-3 common branch-record `MT_DQ`/physical-current match is still
   missing.
5. The complete recordwise strong-operator and physical-test payloads have
   not been bounded by (6.1).

Therefore the honest status is

```text
C_fw:                                  NOT CERTIFIED
C_rev:                                 NOT CERTIFIED
q=max(C_fw,C_rev,2)m:                  NOT CERTIFIED
native full reweighted recovery:       NOT CERTIFIED
arbitrary/unbounded repeated recovery: NOT CERTIFIED
Gate 4:                                NOT CERTIFIED
```

## 8. Replay and fail-close contract

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_product_same_occurrence_joint_moment_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_product_same_occurrence_joint_moment_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_product_same_occurrence_joint_moment_frontier_verifier.py
```

Replay/integrity and mutation testing exit `0`.  Default live execution exits
`2`, because native/arbitrary repeated recovery, complete `C_fw,C_rev`, final
`q`, and Gate 4 remain open.
