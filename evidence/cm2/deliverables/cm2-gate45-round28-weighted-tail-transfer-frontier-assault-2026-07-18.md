# CM2 Gate 4/5 round-28 weighted-tail transfer frontier assault

Date: 2026-07-18 (Asia/Shanghai)

## Verdict

This append-only leaf joins the frozen C24 arbitrary-`n` first-return mass
ledger, the uniform unweighted exponential return tail, the finite Q2
once-charged schema, and the numerical recovery stack.  It closes the exact
mathematical interface needed to turn an unweighted return tail into a
strong-`q` weighted tail, while keeping the current missing physical payload
fail-closed.

```text
C24 FIRST-RETURN MASS/UNWEIGHTED-TAIL JOIN:             CERTIFIED
SURVIVOR-CONDITIONED L^p WEIGHTED-TAIL TRANSFER:       CERTIFIED (conditional)
GLOBAL L^p WEIGHTED-TAIL TRANSFER:                     CERTIFIED (conditional)
POINTWISE EXPONENTIAL SERIES COMPATIBILITY THRESHOLD:  CERTIFIED (exact)
CURRENT PHYSICAL FIRST-RETURN TRANSFER HYPOTHESIS:     NOT CERTIFIED
CURRENT STRONG-q EXCURSION/CEMETERY TAIL:              NOT CERTIFIED
INDUCED STRONG LASOTA--YORKE:                          NOT CERTIFIED
GATE 4 / GATE 5:                                      NOT CERTIFIED
CM2:                                                   NO-GO FOR CLAIM
```

Evidence:

- `deliverables/cm2_gate45_round28_weighted_tail_transfer_frontier_cert.py`;
- `deliverables/cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py`;
- `deliverables/cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json`;
- `deliverables/cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.sha256`.

## 1. Exact first-return mass ledger

For each fixed `|s|<=1/400`, write

```text
S_n = mu_s(Q_n)/mu_s(C_s),
mbar_s,n,k = m_s,n,k/mu_s(C_s),
a_n = sum_k mbar_s,n,k = S_(n-1)-S_n.
```

The frozen round-27 ledger gives the first-return telescope modulo the
collision-null singular/core-boundary set and

```text
S_n < A r^floor(n/N_open),
A = 550000/147,
r = 111718729/111718750,
1-r = 21/111718750.
```

`N_open>=1` is one uniform theorem-supplied integer, but it is not numerical.
This leaf does not change that fact.

Normalize the once-charged branch mass in the same way,

```text
qbar_j,k = q_j,k/mu_s(C_s).
```

For a positive-mass first-return component define the strong density

```text
c_j,k = qbar_j,k/mbar_j,k = q_j,k/m_j,k >= 0,
q_j,k = max(C_fw,C_rev,2) m_j,k.
```

The two views share one physical restriction and are charged once.  A
zero-mass component must have zero `qbar` for an absolutely continuous charge.
The strong singular-cemetery charge is typed separately; collision-null mass
alone is not relabelled as a strong-space bound.

All transfer statements below are first proved for the normalized weighted
tail.  The physical tail satisfies

```text
Wphys_n = mu_s(C_s) Wbar_n <= Wbar_n
```

because `0<mu_s(C_s)<1`, so every displayed normalized upper bound also
bounds the physical charge.

## 2. Survivor-conditioned `L^p` transfer

Let

```text
Wbar_n = sum_(j>n,k) qbar_j,k.
```

If some `p>1` and `0<K_p<infinity` satisfy, on the same physical first-return
registry,

```text
sum_(j>n,k) mbar_j,k c_j,k^p <= K_p^p S_n
```

for every `n`, then Hölder gives

```text
Wbar_n
 <= (sum_tail mbar c^p)^(1/p) S_n^(1-1/p)
 <= K_p S_n
 < K_p A r^floor(n/N_open).
```

Thus a uniform survivor-conditioned `L^p` envelope preserves the full
unweighted block factor `r`.  This is the highest-leverage target for the
next physical registry because it does not require a tiny pointwise loss at
every collision.

## 3. Global `L^p` transfer

The weaker global hypothesis

```text
sum_(j>=1,k) mbar_j,k c_j,k^p <= M_p,
0 < M_p < infinity
```

still yields

```text
Wbar_n
 <= M_p^(1/p) S_n^(1-1/p)
 < M_p^(1/p) A^(1-1/p)
   r^((1-1/p) floor(n/N_open)).
```

For `p=2`, this is

```text
Wbar_n < sqrt(M_2 A) r^(floor(n/N_open)/2).
```

The exponent degrades by `1-1/p`, but remains exponential.  The frozen
product same-occurrence moment is not an instance of this hypothesis: its
depth mark is an auxiliary product variable, and its restart theorem is only
for each separately predeclared finite `H`, not the unbounded physical
first-return registry.

## 4. Exact pointwise exponential compatibility window

Suppose instead that some `C>0`, `G>=1` bound every positive-mass return
component:

```text
c_j,k <= C G^j,   G>=1.
```

Group return times into blocks
`b N_open < j <= (b+1) N_open`.  Their mass is at most
`S_(b N_open)<A r^b`, so the geometric upper-series route gives

```text
Wbar_n
 < C A G^N_open
   (G^N_open r)^floor(n/N_open)
   /(1-G^N_open r),
```

provided

```text
G^N_open r < 1
iff G < r^(-1/N_open).
```

For a blockwise density `c_j,k<=C H^ceil(j/N_open)`, the condition is simply
`H r<1`, and

```text
Wbar_n < C A H (H r)^floor(n/N_open)/(1-H r).
```

The exact one-block window is extremely narrow:

```text
1/r = 111718750/111718729
    = 1 + 21/111718729,

21/111718750 < -log(r) < 21/111718729.
```

Consequently any `G>=1/r` fails this particular series condition for every
integer `N_open>=1`; every integer `G>=2` therefore fails it.  Because
`N_open` is not numerical, `r^(-1/N_open)` cannot yet be turned into a
numerical per-collision threshold.

This is a compatibility statement for the displayed geometric upper-series
argument.  It is **not** a theorem that the physical CM2 weighted tail is
impossible outside that window.  The `L^p` routes above can succeed without a
pointwise multiplicative cost of this form.

## 5. Current physical instantiation

The current stack has substantial but differently typed inputs:

- all-iterate `D_std<30000000`;
- `vartheta_p=360134800/360493663<1`;
- recovery constants `A0=301500`, `A1=1005`, `gamma=1/12060`;
- a native levelwise unnormalised recovery moment;
- a same-occurrence product joint moment and every fixed finite registered
  restart history;
- 114,006 finite Q2 exact masses and common fw/rev restriction IDs;
- 114,006 symbolic once-charged Q2 formulas.

But the exact join required by the transfer theorem is still absent:

```text
Q2 numerical C_fw rows:                         0
Q2 numerical C_rev rows:                        0
Q2 numerical q rows:                            0
Q2 common strong recovery-carrier rows:          0
uniform survivor-conditioned L^p envelopes:      0
global physical first-return L^p envelopes:      0
compatible pointwise exponential envelopes:      0
numerical strong cemetery-charge rows:            0
```

The fixed product mark is not a physical first-return component moment, and
the open-operator coefficient is not an induced first-return coefficient.
Neither may be used to fill these zeros.

## 6. Exact shortest remaining interface

The certificate freezes six ordered missing records:

1. nonempty physical first-return component rows with positive masses;
2. one common fw/rev restriction and strong recovery carrier;
3. numerical once-charged `C_fw`, `C_rev`, and `c=q/m`;
4. a survivor-conditioned/global `L^p` or compatible pointwise envelope;
5. the strong singular-cemetery charge;
6. the induced common-space Lasota--Yorke assembly with complete F14--F18.

The shortest next tail target is therefore not a larger unweighted replay.
It is a same-ID physical first-return `c=q/m` registry followed by a uniform
survivor-conditioned `L^p` estimate.

## 7. Replay and fail-close contract

Use `.venv-neurips/bin/python`:

```text
cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py --integrity-only
  AUDIT_MODE: PASS

cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py --replay
  AUDIT_MODE: PASS

cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py --self-test
  HOSTILE_TESTS: 83/83 PASS

cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py
  exits 2 (physical strong-q tail and induced coefficient remain open)
```

No frozen artifact was modified.
