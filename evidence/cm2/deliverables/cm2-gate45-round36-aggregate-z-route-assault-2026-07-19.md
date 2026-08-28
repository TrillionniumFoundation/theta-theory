# CM2 Gates 4/5 round 36: aggregate-Z route

Date: 2026-07-19  
Status: **an exact aggregate standard-family recurrence is certified; its physical face forcing is still open**

## Verdict

The primary recovery route is now the unnormalised aggregate boundary ledger,
not the cellwise retained-depth `2^D` ledger.  On one same-ID standard family
for a complete physical return/survivor level, the frozen closed-step
estimate gives

```text
Z_(n+1) <= a Z_n + b m_n + J_n,
a = 360134800/360493663 < 1,
b = 2*10^90.
```

Here `J_n` is the new unnormalised physical face numerator.  This recurrence
uses neither inverse component mass nor cellwise retained depth.

## Exact resolvent

The contraction margin and resolvent are

```text
1-a = 358863/360493663,
1/(1-a) = 360493663/358863.
```

Iteration gives

```text
Z_n <= a^n Z_0
       + sum_(j=0)^(n-1) a^(n-1-j)(b m_j+J_j).
```

If `m_j<=m_*` and `J_j<=J_*`, then

```text
sup_n Z_n <= Z_0+(b m_*+J_*)/(1-a).
```

An explicit growth-compatible weight is

```text
w = (1+a)/(2a) = 720628463/720269600 > 1,
w a = 720628463/720987326 < 1,
1-w a = 358863/720987326.
```

Thus a weighted `l1` bound follows as soon as the weighted physical mass and
face-injection sums are finite.

## Why the D1 tail is insufficient

Round 35 controls the additive charge `sum_i 2^B_i`, but the common-carrier
image recut can contain the product `2^(sum_i B_i)`.  The certificate freezes
an exact logical countermodel:

```text
P(B=14)=1-4^-14,
P(B=b)=3*4^-b, b>=15,
B_i=B for every time i.
```

It has the stronger one-time tail `P(B>b)=4^-b`, a finite
`E[2^(3B/2)]`, and finite D1 `L^(6/5)` moment at every fixed depth.  Yet for
every `beta>0`,

```text
E[N_recut,n^beta]=infinity whenever beta*n>=2.
```

This is a non-implication model, not a claim about the physical billiard rank
process.  It proves only that the current marginal/D1 evidence cannot close
the product route.

## First remaining physical equation

The forcing decomposes as

```text
J_n = J_core,n + J_owner,n + J_occurrence,n + J_cemetery,n.
```

Available on the common arbitrary-`R_n` IDs are F8, all-face F9, the 64
moving-occurrence seed F10 values and the fixed-core delay Green kernel.  A
uniform or weighted bound for `J_n` still needs global all-pullback F10,
return-wide F12, moving-current F13, strong cemetery and F14--F18.

The naive all-key F7 factor `580000/1999` does not contract after the closed
step, so it cannot replace this missing face sum.

## Strict boundary

```text
abstract aggregate recurrence:                  CERTIFIED
physical uniform/weighted J_n bound:            NOT CERTIFIED
physical aggregate Z bound:                     NOT CERTIFIED
complete C_fw,C_rev and final q:                 NOT CERTIFIED
strong cemetery:                                NOT CERTIFIED
Gate 4 / Gate 5:                                NOT CERTIFIED
CM2:                                             NO-GO FOR CLAIM
```

## Evidence

- `deliverables/cm2_gate45_round36_aggregate_z_route_cert.py`
- `deliverables/cm2_gate45_round36_aggregate_z_route_verifier.py`
- `deliverables/cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json`

Validation passes syntax, dependency integrity, replay and live fail-close;
the suite rejects `15/15` hostile mutations.
