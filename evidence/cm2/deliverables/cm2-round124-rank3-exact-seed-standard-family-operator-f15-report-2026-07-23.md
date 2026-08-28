# CM2 Round124 — exact-seed standard-family operator and child-local F15

Date: 2026-07-23  
Verdict: **VERIFIED child-local Gate5 `16/18` on all 24 Round121 exact-seed children.**

## Result

Round124 lifts the final Round123 arbitrary-density memberwise estimate to a
typed standard-family operator on the same exact-seed carriers.  It installs
the one-step standard-family operator value

```text
F15 = 34
```

on the existing 120 source full keys.  The resulting strict ledger is:

```text
actual common children                         24
physical family-leg operator rows              72
relative zero-cemetery rows                    72
tagged third-stage payload members             216
new F15 full-key slots                         120
inherited Round123 slots                      1800
combined child-local slots                    1920
child-local fields                    F1-F16 = 16/18
remaining child-local fields              F17, F18
global Gate5 maturity                         10/18
complete 18-field blocks                          0
Gate5 blocks                                      0
CM2                                   NO-GO_FOR_CLAIM
```

The result remains limited to one exact analytic `b` seed, its 24
materialized common children, and their three materialized physical collision
stages.

## Typed standard-family domain

The positive finite input domain consists of tagged members

```text
G = {(M_a, rho_a, C_a)}_a
```

with

```text
M_a > 0,
rho_a > 0,
integral_(C_a) rho_a d ell_* = 1,
Reg_(1/3)(rho_a) <= 500000000000000000000000000,
```

where each carrier `C_a` is one of the materialized Round123 stage carriers.
Its strong norm is

```text
||G||_SF = sum_a M_a (1 + Reg_(1/3)(rho_a) + 1/L_a).
```

Input tags are part of the state.  Two members with identical geometry but
different tags remain distinct; no geometric or cross-child deduplication is
allowed.

The finite positive operator extends to countable tagged positive families
with finite strong norm by monotone convergence and Tonelli.  It extends to
signed inputs by applying the positive operator separately to positive and
negative Jordan standard families and taking the infimum over positive
decompositions.  This adds no factor two and uses no cancellation.

## Family-level Tonelli lift

For each input member and output piece, Round124 uses

```text
alpha_aj = integral_(preimage of output j) rho_a d ell_*,
M_aj     = M_a alpha_aj,
rho_aj^+ = rho_a/(alpha_aj J_*) transported to output j.
```

Zero-`alpha_aj` members are omitted.  Every positive retained density is
normalized, and the half-open output partition gives

```text
sum_j M_aj = M_a,
sum_(a,j) M_aj = sum_a M_a.
```

The final Round123 memberwise F14 estimate and these mass identities yield
the typed family theorem

```text
sum_(a,j) M_aj (1 + Reg_aj^+ + 1/ell_aj)
  < 34 sum_a M_a (1 + Reg_a + 1/L_a).
```

There is no multiplier by 193 natural cells, 216 output fragments, or the
number of members in a family.  The value `34` agrees numerically with F14
but is a distinct F15 theorem and a distinct full-key field.

The exact positive coefficient gap independently recomputed by the verifier
is

```text
34 - 100/3 - delta*(1 + 15000000000000000000000000)
  = 1999999999999999999999999999999999999999999999999999999999999999954999999999999999999999997
    / 3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
  > 0.
```

## Stagewise adapted properness

Round124 keeps the local adapted boundary projection

```text
Z_*(G) = sum_a M_a/L_a
```

strictly separate from the complete standard-family strong norm.  The frozen
adapted growth data are

```text
vartheta_p = 360134800/360493663 < 1,
C_p^* delta = 1441974652/358863,
Z_*(T G) <= vartheta_p Z_*(G) + 2*10^90 M(G).
```

The source inverse-length coefficients are `200`, `100/3`, and `200/17`;
the output coefficients are `100/3`, `200/17`, and `125/4`.  All lie
strictly inside the frozen adapted `C_p^*` threshold.  Every stage input and
output is already proper, so the local recovery clock is exactly zero and no
recovery iterate is applied.

This `Z_*` is not the Round61 owner-collar `Z_col`.  Round124 does not install
or promote the Round61 power-Orlicz law, Round62 outer series, Round65
all-time sector drift, or an ambient positive cemetery.

## Relative zero-cemetery ledger

Round124 reconstructs 72 rows:

```text
24 exact-seed children x 3 physical stages.
```

At each row the actual output partition is disjoint, half-open, and exhaustive.
An internal cut belongs to the right output member, the source parent right
endpoint stays open, and endpoints have `ell_*` measure zero.  Accepted
densities are `ell_*`-absolutely continuous, hence endpoint mass is zero.
The discarded relative-domain complement is empty and the restricted
cemetery arrival kernel is exactly zero.

This is only a zero-cemetery theorem on the restricted materialized
exact-seed regular domain.  It is not an ambient pre-regularization or
all-time owner-cemetery theorem.

## Full-key F15 registry

Round124 creates 120 F15 slots:

```text
stage 0 / roofs 0,1       48
stage 1 / roof 0          24
stage 2 / roofs 0,1       48
total                    120
```

Every immutable key is

```text
(official-word-key-id,
 refined-homogeneous-subbranch-id,
 roof-level-j,
 standard_family_operator_cost).
```

Each slot binds the actual physical stage, the input materialized recut, its
family-leg operator row, tagged output members, its relative zero-cemetery
row, and same-key Round122 F7 and Round123 F14 dependencies.  The transparent
wall roof split creates two field slots for one physical operator where
required; it neither duplicates family mass nor multiplies the value `34`.
The 216 third-stage output members remain payload and do not become F15 source
keys.

The combined registry contains 1920 distinct immutable keys: 120 for each of
the 16 certified child-local fields F1 through F16.  F17 and F18 remain
uninstalled.

## Independent verification

The independent verifier imports neither the Round124 producer nor a
Round124 proof helper.  It byte-pins the producer and 32 frozen upstream
artifacts, strict-parses Round122 and Round123 as data, and independently
reconstructs:

- all 72 tagged standard-family leg operators;
- all 72 relative zero-cemetery rows;
- all 120 stage-aware F15 slots and all 1920 combined keys;
- the finite-positive, countable-projective, and signed-Jordan lifts;
- the exact `F15=34` arithmetic and adapted raw-`Z_*` properness;
- every status boundary and strict nonclaim.

The verifier rejects `154/154` re-signed semantic mutations and `15/15`
strict-JSON mutations.  Two producer runs and two full verifier runs with
distinct hash seeds, fixed locale, and fixed timezone are byte-identical to
the canonical artifacts.

## Strict nonclaims

Round124 does not claim:

- a full Borel-`b` materialization or uniform ranking theorem;
- that F15 is merely a renamed F14 slot;
- that local adapted `Z_*` is the global owner-collar `Z_col`;
- global power-Orlicz, raw-collar, outer-series, or all-time cemetery control;
- owner minimization or cross-child/tag deduplication;
- 216 output-payload source slots;
- F17 dynamic-test operator cost or the F18 operator phase block;
- a complete 18-field block or any global Gate5 upgrade;
- an endpoint-inclusive physical collar or cross-trace union reach;
- a CM2 claim.

The authoritative global state therefore remains

```text
Global Gate5 = 10/18
complete 18-field blocks = 0
Gate5 blocks = 0
CM2 = NO-GO_FOR_CLAIM
```
