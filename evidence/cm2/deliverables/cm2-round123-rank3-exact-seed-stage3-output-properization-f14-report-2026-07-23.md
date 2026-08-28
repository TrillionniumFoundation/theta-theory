# CM2 Round123 — exact-seed third-output properization and child-local F14

Date: 2026-07-23  
Verdict: **VERIFIED child-local Gate5 `15/18` on all 24 Round121 exact-seed children.**

## Result

Round123 extends the frozen Round121 exact seed and final Round122 face-field
bridge through the actual third collision output.  It constructs the complete
third-output properization and installs the arbitrary-regular-density F14
one-step value

```text
34
```

on the existing source full keys.

The resulting strict ledger is:

```text
actual common children          24
third-output fragments          216
new F14 full-key slots          120
inherited Round122 slots       1680
combined child-local slots     1800
child-local fields             F1-F14 and F16 = 15/18
remaining child-local fields   F15, F17, F18
global Gate5 maturity          10/18
complete 18-field blocks       0
Gate5 blocks                   0
CM2                            NO-GO_FOR_CLAIM
```

The result is limited to one exact analytic `b` seed, its 24 materialized
common children, and its three actual physical collision legs.

## Actual third-output properization

The third collision is the north-chart collision with owner `G[-1,-2]`.  Its
adapted coordinate is

```text
a3 = pi/2 - asin(n3_x) + asin(p3)
U3(x) = a3(0) - a3(x).
```

The independent interval replay proves that `U3` is strictly increasing,
that its normalized derivative is strictly larger than `192`, and that

```text
192 < U3(1)/delta < 193,
delta = 10^-90.
```

The equations

```text
U3(x) = j delta,  1 <= j <= 192,
```

therefore give exactly 192 strictly ordered internal roots and 193 natural
third-output cells.  Their identities depend on the exact equation and
combinatorial ownership, not on a numerical bracket.

Round123 merges those 192 cuts with the 23 frozen Round121 input cuts.  The
215 combined internal cuts have pairwise disjoint, strictly ordered dyadic
brackets, including every cross-origin pair.  They produce exactly 216
half-open output fragments.

The fragments are partitioned child-locally.  Each of the 24 input children
owns between 2 and 12 fragments, with histogram

```text
2:1, 3:1, 4:2, 5:1, 6:2, 7:1, 8:1, 9:2, 10:1, 11:1, 12:11.
```

No fragment is deleted, duplicated, reordered, or assigned an equal-mass
ansatz.

## Stagewise output-length theorem

There are 72 accepted-norm leg-output rows:

```text
24 children x 3 physical collision legs.
```

Every input carrier and every output member has adapted length at most
`delta`.  The strict output lower bounds are:

| Physical output | Strict lower bound |
|---|---:|
| first collision | `(3/100) delta` |
| second collision | `(17/200) delta` |
| third collision properized fragments | `(4/125) delta` |
| uniform over all three | `(3/100) delta` |

Consequently, for every child-local output family,

```text
sum_j M_j/ell_j < (100/(3 delta)) M.
```

There is no factor of 193, 216, or the number of fragments belonging to a
child.  The estimate is mass-weighted.

## Arbitrary positive regular densities

Round123 certifies the operator on the closed positive input domain

```text
M > 0,
rho > 0,
integral rho d ell_* = 1,
Reg_(1/3)(rho) <= 500000000000000000000000000.
```

The accepted strong norm is

```text
N(W,M,rho) = M (1 + Reg_(1/3)(rho) + 1/L).
```

For an output member `C_j`, it defines

```text
alpha_j = integral_(C_j) rho d ell_*,
M_j = M alpha_j,
J_*(x) = d ell_*^+(T x) / d ell_*(x),
rho_j^+(T x) = rho(x) / (alpha_j J_*(x)).
```

Thus every retained conditional density is normalized and

```text
sum_j M_j = M.
```

Restriction and conditional normalization only add a constant to `log rho`;
they do not increase `Reg_(1/3)`.  Zero-probability output members are
omitted.  No equality of the member masses is used.

This is an arbitrary-density pushforward theorem on the accepted cone.  It
does not promote the earlier finite fixed-profile synthesis into a theorem
for arbitrary inputs.

## Exact one-step F14 cost

The authoritative one-step recurrence is

```text
Reg_out < (93/100) Reg_in + C_J,
C_J = 15000000000000000000000000.
```

In particular, the parentheses are not
`(93/100)(Reg_in+C_J)`.  Combining the recurrence, mass conservation, and the
uniform output-length bound gives

```text
N_out
  < M (1 + (93/100) Reg_in + C_J + 100/(3 delta)).
```

The exact positive margin for the installed value is

```text
34 - 100/3 - delta (1 + C_J)
  = 2/3 - 15000000000000000000000001/10^90
  > 0.
```

Hence every actual one-step collision operator satisfies

```text
N_out < 34 N_in.
```

The positive-density estimate extends to signed inputs by applying it to the
positive and negative Jordan parts and then taking the positive-decomposition
infimum.  This adds no factor two and uses no cancellation.

Round122 F10 has value zero because the physical face family is empty.  That
same-key F10 slot is a dependency and crosswalk only; it does not pay the
nonzero F14 norm cost.

## One-step slots versus path bounds

Round123 creates the F14 slots on the 120 pre-existing source full keys:

```text
stage 0 / roofs 0,1       48
stage 1 / roof 0          24
stage 2 / roofs 0,1       48
total                    120
```

Each immutable key is

```text
(official-word-key-id,
 refined-homogeneous-subbranch-id,
 roof-level-j,
 regular_density_operator_cost).
```

Every slot binds its physical stage, input materialized recut, accepted-norm
leg-output row, actual output member IDs, and same-key Round122 F10/F13/F16
slots.  The 216 third-output fragments are payload members, not new source
F14 slot keys.

The two-roof cases are symbolic prefix/suffix decompositions of one physical
collision.  They do not apply the density operator twice and do not multiply
the value 34.

There are two distinct three-leg statements:

```text
generic composition of three one-step slots   34^3 = 39304
direct exact-seed three-leg derived bound      34
```

The direct bound uses the exact three-step recurrence with distortion

```text
C_J (1 + 93/100 + (93/100)^2)
  = 41923500000000000000000000
```

and the terminal output-length bound.  It is recorded only as a derived
exact-seed path theorem.  It does not replace the one-step value carried by
an F14 slot.

## Full-key registry

Round122 supplies 1680 slots for F1-F13 and F16.  Round123 adds

```text
24 children x 5 official roof levels = 120 F14 slots.
```

The combined registry has 1800 distinct immutable keys, 120 for each of the
15 certified child-local fields:

```text
F1-F14 and F16.
```

F15, F17, and F18 remain uninstalled.

## Independent verification

The independent verifier runs at 3072-bit Arb precision.  It imports neither
the Round123 producer, the Round123 common helper, the diagnostic spike, nor
the provisional frontier.  The common helper remains byte-pinned internally
by the producer and verifier but is not a top-level freeze-manifest entry.

The verifier independently rebuilds:

- all 27 upstream/helper byte pins;
- the exact Round121 seed and the final Round122 full-key bridge;
- the actual third-collision coordinate and all 192 root brackets;
- all 193 natural cells, 215 merged cuts, and 216 output fragments;
- all 24 child-local partitions and 72 physical-leg output rows;
- the arbitrary-density pushforward, mass, recurrence, length, Jordan, and
  exact-margin contracts;
- all 120 stage-aware F14 slots and the combined 1800-slot registry;
- every strict status and nonclaim.

It rejects `110/110` re-signed semantic mutations and `15/15` strict-JSON
mutations.  Two producer runs and two complete verifier runs with distinct
hash seeds, fixed locale, and fixed timezone are byte-identical to the
canonical artifacts.

## Strict nonclaims

Round123 does not claim:

- a uniform materialization or ranking theorem over the full Borel-`b`
  family;
- 216 output-fragment source F14 slots;
- a fragment-count, natural-cell-count, or symbolic-roof multiplier;
- F15 standard-family operator cost;
- F17 dynamic-test operator cost;
- F18 operator phase block;
- a complete 18-field block or a global Gate5 maturity upgrade;
- endpoint-inclusive physical collar or cross-trace union reach;
- CM2.

The frozen state is exact-seed child-local `15/18`, global `10/18`, complete
blocks `0`, Gate5 blocks `0`, and `NO-GO_FOR_CLAIM`.
