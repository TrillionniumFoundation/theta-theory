# CM2 Round 65 Gate 5 — cross-time sector, Jordan and cemetery frontier

Date: 2026-07-21

Strict verdict: **Gate-5 maturity remains 10/18, complete 18-field blocks
remain zero, complete composite gates remain 0/5, and CM2 remains
NO-GO_FOR_CLAIM.**

## 1. Frozen actual audit

This append-only leaf pins the Round-64 aggregate, independent audit and Gate-5
leaf; the Round-61--63 Gate-5 chain; and the Round-39, 44, 50, 52, 54, 56 and
60 physical inputs used below.  No frozen artifact is edited.

The fixed-time data support exactly the following positive objects:

```text
owner/root law nu_j:                         finite for every fixed j
orientation-cost forward/reverse laws:      finite for every fixed j
cost variation/common mode/complement:      finite for every fixed j
source exact-grazing charge:                 zero for every fixed j
raw Z_col / power-Orlicz right side:         not certified finite
pre-regularization cemetery arrival law:     not materialized
```

Round 52's formula

```text
m_(j,a)^owner
 =1_(E_(j,a)^owner intersect R_(j,a)^reg) m_occ,   n>j
```

is a constant-one restriction theorem separately for each `j`.  Its owner token
contains `time-j`, its set of terminal records is `n>j`, and the frozen chain
contains no Borel cross-time map carrying the `j` owner fibres to the `j+1`
fibres.  Hence it supplies neither

```text
beta_(j+1) << beta_j
```

nor any numerical essential-supremum ratio.  No actual coefficient below
`w_Z^(-1)` can be extracted from the frozen data.

## 2. Exact live/one-shot-arrival split theorem

Let `Lambda_j` be a finite live law on a standard-Borel carrier `E_j`, with
immutable non-time label map `ell_j:E_j->L`.  Let `Lambda_(j+1)` be the next live
law and let `A_(j+1)` be the **one-shot** cemetery-arrival law, with the same label
space.  Write

```text
beta_j       =(ell_j)_# Lambda_j,
beta_(j+1)   =(ell_(j+1))_# Lambda_(j+1),
alpha_(j+1)  =(ell_dagger)_# A_(j+1).
```

For `0<=c<=1`, there exist label-preserving positive kernels
`K_j^live,K_j^dagger` satisfying

```text
Lambda_j K_j^live   = Lambda_(j+1),
Lambda_j K_j^dagger = A_(j+1),
K_j^live 1 + K_j^dagger 1 <= c
```

if and only if

```text
beta_(j+1)+alpha_(j+1) <= c beta_j.                 (2.1)
```

Necessity is projection.  For sufficiency, disintegrate the live and arrival
targets over `L`, put

```text
r=d(beta_(j+1)+alpha_(j+1))/d beta_j,
```

and split `r(ell_j x)` between the two target conditional laws according to
their labelwise masses.  The sharp coefficient is

```text
c_split^*
 = ||d(beta_(j+1)+alpha_(j+1))/d beta_j||_infinity,
```

with value infinity when absolute continuity fails.  Round 64's live-only
criterion is the special case `alpha=0`.

This theorem adds a decisive cemetery guard: a stationary nonzero live label
law plus any positive arrival on that label has `c_split^*>1`, so it cannot be
the output of a sub-Markov split.  A singular new cemetery label is equally
impossible.  In the finite replay

```text
beta_j=(4,2), beta_(j+1)=(1,1), alpha_(j+1)=(1,0),
```

both label ratios are `1/2`, and `c_split^*=1/2` is attained.

### Arrival payment from a genuine live law

Suppose the split is genuinely generated from the live law and a Lyapunov drift
gives

```text
Lambda_j(V_j) <= kappa^j Lambda_0(V_0),
V_j>=1,                    w_Z kappa<1.
```

Then positivity pays the one-shot arrivals:

```text
sum_(j>=0) w_Z^(j+1) A_(j+1)(1)
 <= w_Z Lambda_0(V_0)/(1-w_Z kappa).
```

This does not pay a cemetery law removed **before** `Lambda_j` is constructed.
That missing pre-regularization law must first be materialized and joined to the
split.

For comparison, if arrivals are turned into a leaky occupancy

```text
O_j=sum_(i<=j)q^(j-i)A_i,
```

then, for `w_Z q<1`, its exact weighted ledger is

```text
sum_j w_Z^j O_j(1)
 = [sum_i w_Z^i A_i(1)]/(1-w_Z q).
```

At the absorbing value `q=1`, every nonzero arrival yields an infinite ledger
because `w_Z>1`.  Thus the requested positive cemetery is necessarily an
arrival/innovation ledger, not repeated absorbing occupancy.

## 3. Exact seven-sector common-kernel criterion

Retain the same label ratio

```text
r_j=d beta_(j+1)/d beta_j.
```

For each positive sector `s` in

```text
active-clock, raw-Z, power-Orlicz, complement,
variation, common-mode, one-shot cemetery,
```

assume first that its Lyapunov mark is fibre-constant:

```text
H_j^s=h_j^s composed ell_j.
```

There exists one label-preserving live kernel transporting `Lambda_j` to
`Lambda_(j+1)` and satisfying every Feynman--Kac row

```text
K_j H_(j+1)^s <= kappa_(j,s) H_j^s
```

if and only if, almost everywhere on `beta_j`,

```text
r_j<=1,
r_j h_(j+1)^s <= kappa_(j,s) h_j^s       for every sector s.    (3.1)
```

The sharp coefficient in sector `s` is

```text
kappa_(j,s)^*
 = ess sup [r_j h_(j+1)^s/h_j^s],
```

using infinity when the denominator vanishes under a positive numerator.  A
single uniform drift exists exactly when the maximum over all seven sectors is
below `w_Z^(-1)`.  Nonuniform coefficients pay a sector precisely through the
sufficient product ledger

```text
sum_j w_Z^j product_(i<j)kappa_(i,s)<infinity.
```

For non-fibre-constant physical charges, define the label marginal

```text
gamma_j^s=(ell_j)_#(H_j^s Lambda_j).
```

Then `gamma_(j+1)^s<=kappa gamma_j^s` is necessary for a common physical
Feynman--Kac kernel and is an exact iff for a **sector-specific charge
transport**.  It is not sufficient to assert that the same physical live kernel
works for all sectors.  This separates the measure-side owner problem from an
`L^infinity` function-side operator theorem.

The actual frozen chain fails before (3.1) can be evaluated:

- no common cross-`j` immutable-label ratio `r_j` is materialized;
- raw `Z_col` and its power-Orlicz law are not certified finite even at one
  fixed `j`;
- the positive pre-regularization cemetery slice is absent;
- the fixed-`j` RN cost marks have not been identified as fibre-constant marks
  on one cross-time label carrier.

Thus no sector coefficient, uniform maximum, or nonuniform product can be
promoted.

## 4. Active Abel, raw `Z_col` and Orlicz drift

On `A_col`, retain the exact marks

```text
H_clock=w_Z^r_K,
H_raw=2^(K+1),
H_Orl=H_clock^q_col,
q_col=log(2)/(beta log(w_Z)).
```

Round 61 gives the same-slice comparison

```text
H_raw <= H_Orl < C_col H_raw,
C_col=w_Z^q_col=2^(1/beta).
```

Consequently, once a common cross-time label ratio exists, the sharp raw and
Orlicz drift coefficients obey

```text
C_col^(-1) kappa_raw^* <= kappa_Orl^* <= C_col kappa_raw^*.
```

This comparison does not turn the owner-law exponent `q_col` into a trace RN
exponent.  It also does not generate either coefficient.

A one-label separator proves why base lineage contraction is insufficient.  Set

```text
w=3/2, beta_j=3^(-j), K_j=j.
```

Then the base coefficient is `1/3<w^(-1)` and

```text
sum_j w^j beta_j=sum_j 2^(-j)=2.
```

But the raw-sector coefficient is `2/3=w^(-1)` and

```text
sum_j w^j beta_j 2^(K_j+1)=sum_j 2=infinity.
```

Thus even a valid base owner kernel needs a separate clearance/Orlicz
Feynman--Kac row.  The active Abel identity and raw/Orlicz exact iff remain
useful diagnostics, not finite estimates.

## 5. Oriented positive bridge and Jordan common mode

Let `mu^+,mu^-` be the Round-54 physical hit/miss positive pair and
`xi^f,xi^r` the Round-61 orientation-cost pair.  After providing a common
immutable label space, an orientation-preserving sub-Markov bridge with bound
`c` exists exactly when

```text
(ell_x)_#xi^f <= c (ell_p)_#mu^+,
(ell_x)_#xi^r <= c (ell_p)_#mu^-.
```

The minimum coefficient is the maximum of the two RN essential suprema.  This
is the positive, orientation-typed analogue of the owner-fibre theorem.

For an exact mass-preserving crosswalk, the two label marginals must be equal
orientation by orientation.  Round 54 has

```text
mu^+(X)=mu^-(X)=m_p,
```

so any exact mass-preserving identification forces the scalar necessary row

```text
xi^f(X)=xi^r(X).
```

Round 61 supplies separate upper bounds, not this equality, and supplies no
common carrier or RN ratios.  Hence the exact physical bridge is still absent.

On a common carrier, either of the following equivalent pairs of data determines
the oriented positive pair:

```text
(signed law J, positive sum S=mu^++mu^-),
(signed law J, common mode lambda=mu^+ wedge mu^-).
```

Indeed `mu^+=(S+J)/2`, `mu^-=(S-J)/2`, and
`S=|J|+2lambda`.  Signed equality alone cannot control the common mode.  The
Round-63 cost-Jordan identity therefore remains a fixed-time cost law, not the
Round-54 physical Jordan law.

## 6. Audit of the remaining eight fields

The exact 18-field schema leaves these eight global rows open:

| field | name | first unpaid Gate-5 interface |
|---|---|---|
| F5 | `inverse_Jacobian_bound` | only candidate-local values; no global homogeneous return-word row |
| F6 | `log_Jacobian_distortion_sum` | only candidate-local template; no global same-block sum |
| F10 | `coarea_density_regular_bound` | all-time positive sector/cut/cemetery ledger absent |
| F11 | `dynamic_Holder_test_pullback_bound` | no branch-uniform physical dynamic test embedding |
| F14 | `regular_density_operator_cost` | F10 and common recovered strong block absent |
| F15 | `standard_family_operator_cost` | raw-Z/Orlicz, recovery and positive cemetery absent |
| F17 | `dynamic_test_operator_cost` | all-input vector-current/strong recipient absent |
| F18 | `operator_phase_block` | the preceding seven open rows do not coexist on one block |

The live/arrival theorem and seven-sector criterion sharpen F10/F14/F15 and the
cemetery part of F18, but they do not fill any actual row.  Gate-5 maturity
therefore remains exactly `10/18`.

## 7. Latest technology boundary

`arXiv:2510.19573v3`, *Quasi-compactness for dominated kernels with application
to quasi-stationary distribution theory*, proves function-side domination and
Lyapunov/local-compactness criteria on weighted supremum spaces, including an
essential-spectral-radius comparison for `0<=P<=Q`.  It assumes the dominated
positive kernels and Lyapunov structure; it does not construct the measure-side
owner marginal domination (2.1), the CM2 cross-time labels, or the missing
positive slice.  It is therefore guidance only.

`arXiv:2605.07824`, *Tamed Feynman-Kac diffusion processes: Killing-branching
intertwine*, concerns one-dimensional drifted diffusions with killing/branching
potentials.  It is the wrong process and does not supply a billiard
owner/coarea trace kernel.

No external theorem is promoted.

## 8. Strict frontier

```text
live + one-shot-arrival split iff:              CERTIFIED_EXACT
sharp split coefficient c_split^*:             CERTIFIED_EXACT
actual pre-cemetery arrival law:                NOT_MATERIALIZED
actual cross-j live/arrival domination:         NOT_CERTIFIED

seven-sector fibre-constant common criterion:   CERTIFIED_EXACT
sector-specific charge marginal criterion:      CERTIFIED_EXACT_TYPED
actual common label ratio / sector coefficients:NOT_CERTIFIED
unified finite positive slice:                  NOT_CERTIFIED

raw/Orlicz drift comparison:                    CERTIFIED_EXACT
base drift pays raw-Z:                          CERTIFIED_FALSE_BY_SEPARATOR
physical active Abel/raw-Z/Orlicz RHS:          NOT_CERTIFIED

oriented positive bridge iff:                   CERTIFIED_EXACT
equal-total scalar necessity:                   CERTIFIED_EXACT
Round54/Round61 carrier/RN/common-mode bridge:  NOT_CERTIFIED

remaining global fields:                       8 open / 18 total
Gate-5 maturity / complete blocks:              10/18 / 0
complete composite gates:                       0/5
CM2:                                            NO-GO_FOR_CLAIM
```

## 9. Shortest continuation

1. materialize `beta_j,beta_(j+1),alpha_(j+1)` on one immutable label carrier
   and compute the sharp split RN ratio;
2. build the finite raw-Z/Orlicz and pre-cemetery sectors before asking for
   their Feynman--Kac coefficients;
3. prove the seven sector ratios below `w_Z^(-1)` or a summable nonuniform
   product, with the same physical kernel where required;
4. construct the Round54/Round61 oriented carrier and first test the necessary
   forward/reverse total-mass equality, then the two RN ratios and common mode;
5. independently close F5/F6/F11/F17 and assemble all open rows into F18.

## 10. Executable evidence

The companion producer and independent verifier pin the complete frozen scope,
replay finite live/arrival splits, seven-sector sharp coefficients, raw-sector
boundary divergence, leaky/absorbing cemetery algebra, oriented RN bridges and
all eight open-field rows; regenerate canonical JSON byte-for-byte; reject
hostile semantic and strict-JSON mutations; validate a five-row SHA ledger; and
fail closed by default with exit `2`.
