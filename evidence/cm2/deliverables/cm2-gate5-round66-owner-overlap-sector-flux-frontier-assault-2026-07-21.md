# CM2 Round 66 Gate 5 — owner overlap, sector and flux frontier

Date: 2026-07-21

Strict verdict: **the fixed-`j` owner formula admits a genuine maximal
cross-`j` terminal-record overlap construction, but it does not give a
contracting owner lineage.  On the full immutable terminal/source carrier the
best birth-free live coefficient is `1`; an owner birth or label switch gives a
singular target component.  Gate-5 maturity remains `10/18`, complete blocks
remain zero, and CM2 remains `NO-GO_FOR_CLAIM`.**

## 1. Frozen scope

This append-only leaf pins the Round-65 aggregate, independent audit, Gate-5
and cross-gate leaves; the Round-64 Gate-5 leaf; the Round-50--63
owner/cemetery/Jordan chain; and the Round-27, 39 and 44 physical inputs used
below.  It changes no old artifact.

The decisive fixed-time identity is still

```text
m_(j,a)^own
 =1_(E_(j,a)^owner intersect R_(j,a)^reg) m_occ,   n(a)>j.
```

For one `j` the source-marked owner pieces are disjoint, so their sum is finite
and dominated by `m_occ`.  The formula is now compared for consecutive `j` on
the same raw occurrence law.  No owner-set nesting is assumed.

## 2. The maximal terminal-record crosswalk

Let `a=(n,component,path,parent,seed,...)` denote the immutable finite terminal
record before the insertion-time owner code is read.  On the countable
standard-Borel disjoint union of record copies put

```text
M=sum_a delta_a tensor m_occ.
```

`M` is sigma finite.  The owner-selected fixed-time slice has the indicator
density

```text
S_j={(a,x):n(a)>j,
     x in E_(j,a)^owner intersect R_(j,a)^reg},
sigma_j=1_(S_j) M.
```

The physical state retains the explicit time coordinate.  On terminal records
with `n>j+1` define the injective Borel update

```text
U_j(j,a,x)=(j+1,a,x).
```

This updates `j`; it does not delete it and it is not cross-time owner
deduplication.  Let `bar(ell)_j` be the full owner/root/event/side/word label
with only the explicit insertion coordinate separated out.  Equality of
`bar(ell)_j` and `bar(ell)_(j+1)` is a Borel predicate after the already frozen
standard-Borel coding.

Define the maximal lawful overlap

```text
O_j=S_j intersect S_(j+1)
        intersect {bar(ell)_j=bar(ell)_(j+1)},

D_j^term=S_j intersect {n=j+1},
D_j^switch=S_j minus (O_j union D_j^term),
B_(j+1)=S_(j+1) minus O_j.
```

`D_j^switch` and `B_(j+1)` may refer to the same raw `(a,x)` with different
owner labels; on the labelled carrier that is a death plus a birth, not a
preserved lineage.  The exact decompositions are

```text
sigma_j=1_O M+1_(Dterm)M+1_(Dswitch)M,
sigma_(j+1)=1_O M+1_B M,
```

followed by the explicit `j -> j+1` relabelling.  Thus `n>j+1` being a subset
of `n>j` proves only that there is no **terminal-eligibility birth**.  It does
not prove `B_(j+1)=empty`: the owner and regular predicates depend on `j`.

This is a genuine maximal cross-time map on the common immutable terminal
record.  It is deliberately partial: only `O_j` preserves the complete
non-time owner label.  No frozen theorem gives the actual masses of `O_j`,
`D_j^term`, `D_j^switch` or `B_(j+1)`.

## 3. Exact RN frontier

Pull the next slice back with `U_j`.  On the full terminal/source/owner-label
carrier, both fixed-time laws have zero-one densities with respect to `M`.
Consequently the live-only coefficient is exactly

```text
c_live^* = infinity,  if M(B_(j+1))>0;
           1,         if M(B_(j+1))=0 and M(O_j)>0;
           0,         if sigma_(j+1)=0.
```

The value `infinity` means failure of absolute continuity, not a large finite
estimate.  In the birth-free case the RN density is exactly one on `O_j`.
Therefore even a small **total-mass ratio** does not yield a strong
label-preserving coefficient below one.

If every old record is accounted either as a live overlap or as a one-shot
terminal/switch departure, the combined live-plus-departure density is exactly
one on `S_j`.  Hence

```text
c_account^*=1
```

in the birth-free nonzero case; adding a positive birth makes the full target
singular.  Since `w_Z>1`, neither coefficient can satisfy
`w_Z c^*<1`.  A terminal exit and the pre-regularization singular cemetery are
also different types: the construction above does not materialize or pay the
latter.

The finite replay uses six raw atoms:

| atom | `n` | mass | in `S_j` | in `S_(j+1)` | role |
|---|---:|---:|---:|---:|---|
| a | `j+1` | 2 | yes | no | terminal exit |
| b | `j+2` | 3 | yes | yes | overlap |
| c | `j+3` | 5 | yes | no | owner departure |
| d | `j+3` | 7 | no | yes | owner birth |
| e | `j+4` | 11 | yes | yes | overlap |
| f | `j+4` | 13 | no | no | inactive |

Both live totals happen to equal `21`, but the overlap is `14`, departures
total `7`, and the birth has mass `7`; the RN coefficient is infinite.  If the
birth is deleted, the next total/source total ratio is `14/21=2/3`, while the
full-label essential-supremum coefficient remains exactly `1`.  This separates
average tail loss from the required strong lineage contraction.

## 4. Seven tagged sectors on the overlap

For a positive sector `s`, write on the same ambient carrier

```text
Gamma_j^s=1_(S_j) h_j^s M,
Gamma_(j+1)^s=1_(S_(j+1)) h_(j+1)^s M.
```

On `O_j`, the exact RN density is

```text
h_(j+1)^s/h_j^s.
```

It is infinite if the numerator is positive where the denominator is zero, or
if the target sector assigns positive charge to `B_(j+1)`.  Thus

```text
kappa_s^*
 =ess sup_(O_j) h_(j+1)^s/h_j^s
```

only after both singular pieces have been proved zero.  On the disjoint
sector-tagged carrier, the common exact coefficient is the maximum over

```text
active-clock, raw-Z, power-Orlicz, complement,
variation, common-mode, one-shot cemetery.
```

This strengthens the fixed-fibre criterion by exposing the owner-birth term.
It also shows why summing the marks first is unsafe: a small charge in one
sector may hide an infinite RN ratio in another, while the typed direct sum
retains it.

The actual frozen slice still fails upstream:

```text
base owner law at fixed j:                    finite
complement/orientation variation/common:      finite at fixed j
active clock/raw-Z/power-Orlicz RHS:           not certified finite
pre-regularization one-shot cemetery:          not materialized
```

Hence the seven-sector finite tagged measure does not yet exist.  Even if it
did, no owner-birth nullity or overlap ratio below `w_Z^(-1)` is frozen.

For raw clearance and the power-Orlicz mark, the same-slice comparison remains

```text
H_raw<=H_Orl<C_col H_raw.
```

On a birth-free overlap it only compares the two unknown drift coefficients
within the same finite factor.  It neither proves finiteness nor creates a
coefficient.  Finite truncations `K<=N` are not uniform: on one atom the raw
mark is `2^(N+1)`, so every truncation is finite while the envelope diverges as
`N -> infinity`.

## 5. Arrival and positive path payment

The overlap decomposition distinguishes three ledgers:

1. normal terminal exits `D_j^term`;
2. owner/label-switch departures `D_j^switch`;
3. the separate pre-regularization cemetery outside `sigma_j`.

The first two can be sent to one-shot labelled departure atoms without
repeating occupancy.  Their weighted total is bounded only if the conditional
source potential or a genuine source-slice decay pays

```text
sum_j w_Z^(j+1) sigma_j(D_j^term union D_j^switch).
```

The identity `live+departure=source` gives no contraction; it merely prevents
double counting.  Absorbing occupancy still diverges for every nonzero arrival
when `w_Z>1`.  Nothing in the terminal-record construction reaches the missing
pre-regularization cemetery law.

## 6. Round-54 / Round-61 oriented positive carrier

The terminal crosswalk compares consecutive Round-52 owner restrictions.  It
does not identify Round-54's physical hit/miss source law `|lambda_p|` with
Round-61's orientation-cost owner law `m_j^own`.  The missing typed row remains

```text
|lambda_p| <= m_j^own
```

on one immutable record and with charge preservation.

Let

```text
m_p=mu^+(X)=mu^-(X),
F_j=xi_j^f(X),  R_j=xi_j^r(X).
```

An exact orientation-preserving mass crosswalk necessarily satisfies

```text
F_j=m_p=R_j.
```

Thus `F_j=R_j` is only the first scalar test.  Round 61 supplies the separate
strict upper bounds

```text
F_j <395304765824751/220000,
R_j <162772550633721/176000,
```

whose sum is `2395081816467609/880000`; it supplies neither actual totals nor
their equality.  Unequal upper bounds do not prove unequal totals.  There is
also no positive lower bound for `m_p`, so the RN coefficients cannot be
bounded by dividing those constants.

After the scalar test one still needs the two full RN rows and common-mode
equality.  Separate normalization of forward and reverse laws would change
physical amplitudes and is not an oriented Jordan bridge.  Therefore the
Round-63 cost-Jordan law still cannot be promoted to the Round-54 physical
positive pair.

## 7. The remaining eight fields

| field | exact Round-66 effect | status |
|---|---|---|
| F5 inverse Jacobian | terminal overlap supplies no homogeneous return-word inverse-Jacobian row | open |
| F6 distortion | no same-block all-record distortion sum | open |
| F10 coarea regularity | fixed-time pieces exist; birth/raw/cemetery/all-time positive ledger absent | open |
| F11 dynamic pullback | no branch-uniform physical test embedding | open |
| F14 regular-density cost | depends on complete F10 and one recovered strong block | open |
| F15 standard-family cost | raw/Orlicz, recovery and positive cemetery absent | open |
| F17 dynamic-test cost | no all-input vector-current strong recipient | open |
| F18 operator phase block | preceding rows do not coexist on one physical block | open |

The maximal overlap is a new exact sublayer, not a completed field.  Gate-5
maturity therefore stays `10/18`.

## 8. Technology boundary

The dominated-kernel technology pinned in Round 65 starts after a positive
kernel domination and Lyapunov row have been supplied.  It cannot remove the
singular birth component `B_(j+1)` or turn the density-one overlap into a
strict contraction.  Killing/branching diffusion results use a different
process and recipient.  No external theorem is promoted.

## 9. Strict frontier

```text
terminal-record time update U_j:                    CERTIFIED_EXACT_BOREL
time-j retained / cross-j deduplication:             YES / ILLEGAL
maximal full-label overlap O_j:                      CERTIFIED_EXACT_BOREL
n>j+1 subset n>j implies owner-set nesting:          CERTIFIED_FALSE
actual overlap/departure/birth masses:                NOT_CERTIFIED

birth-free live RN coefficient:                      EXACTLY_1_IF_NONZERO
positive birth/label-switch target:                  SINGULAR_ON_FULL_LABEL
birth-free live+departure accounting coefficient:    EXACTLY_1
positive-overlap nesting route below w_Z^(-1):       CERTIFIED_FALSE
actual coefficient including zero/birth cases:       NOT_EVALUATED

seven-sector overlap RN formula:                     CERTIFIED_EXACT_TYPED
actual finite seven-sector slice:                    NOT_CERTIFIED
actual raw-Z/Orlicz drift:                            NOT_CERTIFIED
pre-regularization cemetery:                         NOT_MATERIALIZED

oriented total-mass necessary row F_j=m_p=R_j:       CERTIFIED_EXACT
actual scalar equality / carrier / two RN rows:      NOT_CERTIFIED
physical common-mode alignment:                      NOT_CERTIFIED

remaining fields:                                    F5/F6/F10/F11/F14/F15/F17/F18
Gate-5 maturity / complete blocks:                   10/18 / 0
complete composite gates:                            0/5
CM2:                                                  NO-GO_FOR_CLAIM
```

## 10. Shortest lawful continuation

1. evaluate the four same-law pieces `O_j,D_j^term,D_j^switch,B_(j+1)` on
   actual terminal records and first prove birth/label-switch nullity;
2. replace total-mass tail decay by a pointwise conditional sector potential,
   because the surviving density is one on the full record label;
3. materialize raw-Z/Orlicz and pre-cemetery slices, then compute every typed
   overlap ratio rather than one summed average;
4. bind `|lambda_p|` and `m_j^own` on one terminal record, test
   `F_j=m_p=R_j`, and only then compute the two orientation RN ratios and
   common mode;
5. close F5/F6/F11/F17 independently and assemble the resulting physical
   rows with F10/F14/F15 into F18.

## 11. Executable evidence

The companion producer and independent verifier pin the complete frozen
scope, replay the six-atom overlap/birth model, the birth-free `2/3` versus
`1` separation, seven typed sector ratios, raw truncation growth, the oriented
mass necessity and all eight open fields; regenerate canonical JSON
byte-for-byte; reject hostile semantic and strict-JSON mutations; validate a
five-row SHA ledger; and fail closed by default with exit `2`.
