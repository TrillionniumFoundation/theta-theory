# CM2 Round125 — exact-seed graph-current recipient and child-local F17

Date: 2026-07-23  
Verdict: **VERIFIED by independent 3072-bit replay; 248/248 re-signed
semantic mutations and 15/15 strict-JSON attacks rejected.**

## Result

Round125 installs a genuinely vector-valued graph-current recipient and the
one-step dynamic-test operator field F17 on the same 24 Round121 exact-seed
children used by Rounds121--124.  It does not rename the existing scalar F11
slots.

The frozen producer and certificate materialize:

```text
actual common children                         24
Eulerian graph-current leg rows                72
recipient components                            4
recipient pullback maps                        72
source-injection contract rows                  3
source-injection derivation rows                3
input artificial trace rows                   144
input internal incidence rows                  69
stage-3 output artificial trace rows          432
stage-3 output internal incidences             215
new within-input incidences cancelled          192
old inter-child incidences retained             23
retained typed output trace sides               48
new F17 full-key slots                         120
inherited Round124 slots                      1920
combined child-local slots                    2040
child-local fields                    F1-F17 = 17/18
remaining child-local field                    F18
global Gate5 maturity                         10/18
complete 18-field blocks                          0
Gate5 blocks                                      0
CM2                                   NO-GO_FOR_CLAIM
```

This remains a finite theorem on one exact analytic `b` seed, its 24
materialized common children, and their three physical collision stages.  It
does not extend the four-component recipient to the global Borel key
universe.

## Eulerian graph-current legs

Every materialized physical leg uses collision-area coordinates

```text
(r,p) = (R theta, sin(phi)),
area form = dr dp.
```

For the horizontal translation of the `W` obstacle, the Eulerian generator is

```text
X_i = (partial_s F_(i,s)) composed with F_(i,0)^(-1).
```

Writing the incoming ray as

```text
u = -c n + p Jn,
c = sqrt(1-p^2),
```

and the relative center velocity as `eta e_x`, the two generator components
are

```text
X_r = eta (n_y - (p/c)n_x),
X_p = (eta/R)(c n_y - p n_x).
```

The exact derivative identities give

```text
partial_r X_r =  (eta/R)(n_x + (p/c)n_y),
partial_p X_p = -(eta/R)(n_x + (p/c)n_y),
div_(dr dp) X = 0.
```

The stagewise relative velocities are `1`, `-1`, and `0`.  The stored guarded
enclosures prove

```text
stage 0: |X_r| + |X_p| < 8,
stage 1: |X_r| + |X_p| < 2,
stage 2: X_r = X_p = 0 exactly.
```

Each of the 72 rows binds its actual Round122 source owner/chart audit row,
its Round124 target family row, the positive guarded target-cosine lower
bound, both generator components, and the same-stage F11/F13/F15
dependencies.

## Source graph-current injection

For an admitted tagged input member,

```text
mu_i = M_i rho_i d ell_*,
K_i  = X_i mu_i,
T_(K_i,B_i) = -div(K_i) + B_i.
```

The density is positive and normalized on an adapted carrier of length
`L_i <= delta < 1`.  Consequently,

```text
1 = integral rho_i d ell_*
  <= L_i ||rho_i||_infinity,

||rho_i||_infinity >= 1/L_i > 1,
M_i <= M_i ||rho_i||_infinity.
```

Round125 does not infer the geometric incidence rank by reversing the F11
formula.  Every leg independently verifies the Round43 inequality

```text
1/c_target <= 2^B
```

from its stored positive guarded cosine lower.  The ranks are

```text
stage 0: B = 15,
stage 1: B = 14,
stage 2: B = 14.
```

The F11 identities `4915200=150*2^15` and
`2457600=150*2^14` are only same-stage consistency crosswalks.

The bulk and two-side artificial-trace estimates give

```text
TV(K_i) <= 25*2^B M_i
        <= 25*2^B M_i ||rho_i||_infinity,

TV(B_i) < 27 M_i ||rho_i||_infinity.
```

Thus the stagewise source injections are

```text
stage 0: 25*2^15 + 27 = 819227,
stage 1: 25*2^14 + 27 = 409627,
stage 2: 25*2^14 + 27 = 409627.
```

The certificate makes this theorem an acyclic hash graph:

```text
3 source-injection contracts
  -> 72 graph-current legs
  -> 3 stage derivations listing all leg ID/hash pairs
  -> 120 F17 slots.
```

The derivation rows contain the exact 24 graph-row IDs and hashes for their
stage, their canonical aggregate digest, the minimum guarded cosine lower,
the maximum reciprocal-cosine upper, the maximum actual generator bound, and
the normalization/Tonelli payment.  They are not isolated narrative
booleans.

## Input artificial traces and the adapted Jacobian

There are

```text
24 children x 3 stages x 2 sides = 144
```

typed input artificial traces.  If a source face is represented by
`x_face(s)`, the exact trace atom is

```text
orientation_sign
  * v_face^(x)
  * J_*^in
  * M_i rho_i,

v_face^(x) = d_s x_face,
J_*^in = |partial_x ell_*|.
```

The adapted-density Jacobian is mandatory and is stored in every trace row.
Each trace also binds the corresponding Round124 family-leg row, input
materialized recut, input-member contract, and immutable source-family tag
domain.

At each of the 69 adjacent input incidences, the two geometric carriers and
their input-family tag domains are distinct.  Opposite orientation alone does
not permit cancellation.  Both traces remain typed unless their
unnormalized densities are explicitly compared inside one identical source
family tag.

## Four-component recipient and Piola intertwining

The finite exact-seed recipient has four components:

```text
G:W   owner G[0,0]    chart W
W:N   owner W[-1,-1] chart N
G:S   owner G[0,0]    chart S
G:N   owner G[-1,-2] chart N
```

The three physical routes are

```text
stage 0: G:W -> W:N,
stage 1: W:N -> G:S,
stage 2: G:S -> G:N.
```

All 72 maps bind the source and target component IDs and row hashes, the
actual Round124 family row, the corresponding graph-current row, every
same-key Round122 F11 slot, and the authoritative stage F11 row.  The
one-step pullback bounds are

```text
stage 0: 4915200,
stage 1: 2457600,
stage 2: 2457600.
```

For scalar tests,

```text
phi -> phi composed S_i.
```

For vector Radon measures and typed boundary traces,

```text
K -> S_i#(DS_i K),
B -> S_i#B.
```

The graph-current identity is

```text
S_i# T_(K,B)
  = T_(S_i#(DS_i K), S_i#B).
```

The determinant is one in collision-area coordinates.  Both Eulerian vector
components are received, physical and artificial traces stay separately
typed, and the transparent roof split does not create an additional physical
map or operator factor.

## Stage-3 trace witnesses

The 216 Round123 output fragments produce 432 oriented output trace rows and
215 internal incidences.

Every trace binds:

- its Round123 fragment row;
- its Round124 stage-2 input-family row and input materialized recut;
- the immutable input-family tag template and tag-domain ID;
- its Round123 merged-cut canonical digest, or the pinned outer-face evidence;
- an endpoint-velocity witness;
- an unnormalized-density witness carrying the input geometry, input-family
  contract, endpoint, and endpoint evidence.

At each of the 192 new Round123 cuts, the two adjacent natural output cells
are distinct but arise from the same input materialized recut and the same
input-family tag domain.  Cancellation occurs before distinct output-member
tags are assigned.  The two orientations oppose, the root velocity is the
same, and

```text
M_fragment rho_fragment
  = M_input rho_input / J_star
```

recovers the same unnormalized density on both sides.  The 192 endpoint,
velocity-witness, and density-witness IDs are each unique.

At the 23 older inter-child cuts, the input family rows and tag domains are
different.  Their unnormalized-density witness IDs do not match, so neither
side is cancelled.  Together with the two outer sides this leaves

```text
23*2 + 2 = 48
```

typed output trace sides.  No physical-empty statement erases these
artificial traces.

## Full-key F17 registry

Round125 creates 120 F17 slots:

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
 dynamic_test_operator_cost).
```

Each slot binds one graph-current leg, its source-injection contract and
stage derivation, one recipient pullback map, the source and target recipient
components, the same-key Round122 F11 slot, and the same-key Round124 F15
slot.

The F17 values equal the stage F11 pullback constants numerically, but F17 is
a distinct vector-current/Piola theorem with distinct field IDs and full-key
slots.  The transparent roof split creates multiple field slots where
required without multiplying one physical operator.

The combined registry contains 2040 distinct immutable keys: 120 for each of
the 17 certified child-local fields F1 through F17.  F18 remains
uninstalled.

## Independent verification

The independent verifier and canonical verification artifact are frozen:

```text
producer SHA256             e360c511c87f10483ee19cf566d9542f123a2fbdf37585d9954a9c33575b940b
certificate SHA256          cecae7d1b864abcb62215c317bb87bbf392848c70b6affca253d350a9f687579
certificate result SHA256   b75c0574aa337c7ea5f9659e04980d0e415c30a2dd1a2b81b3774ed0577053ba
verifier SHA256             15f5313fc9f9593a0e1d41b95a9c09f7cc204f3471e177c17b1355b9a3f13737
verification SHA256         919c50840eee75bcebb7ed8d870f2300d6a47466055bd4d25d95645dbbc6bd62
verification result SHA256  92919d7d41bf159628068d589f6e16e390be2f04017c6094f1aa4cdedd32527c
producer precision          1536 bits
verifier precision          3072 bits
semantic mutations          248/248 rejected
strict-JSON mutations       15/15 rejected
```

Without importing the Round125 producer, the verifier reconstructs:

- all 72 guarded graph-current legs at independent precision, with complete
  enclosure containment and actual upper-bound dominance;
- all four recipient components and all 72 source-target/F11/Piola maps;
- all three source-injection contracts, all three 24-leg derivations, and the
  complete contract-to-slot hash DAG;
- all 144 input traces with the exact adapted Jacobian;
- all 432 output traces and all 215 incidences, including the 192/23
  cancellation split and every tag/witness crosslink;
- all 120 F17 slots and all 2040 combined child-local keys;
- every local/global status boundary and strict nonclaim.

Two complete producer/verifier runs under distinct `PYTHONHASHSEED` values
are byte-identical to the canonical certificate and verification artifact.
A missing certificate and a valid-JSON tamper both exit nonzero without
writing an output.

## Strict nonclaims

Round125 does not claim:

- that scalar F11 slots have merely been renamed as vector-current F17 slots;
- `C_dyn=1` or satisfaction of the old global
  `C_dyn<7961063/7800000` threshold;
- automatic cancellation of unequal inter-child traces;
- erasure of artificial traces by the Round122 physical-empty audit;
- a strong global F13 or arbitrary-return-depth F17 theorem;
- extension of the four-component exact-seed recipient to the global Borel
  key universe;
- global power-Orlicz, owner drift, or strong cemetery control;
- an F18 operator phase block or a complete 18-field block;
- a global Gate5 maturity upgrade;
- an endpoint-inclusive physical collar or cross-trace union reach;
- a CM2 claim.

The authoritative global state therefore remains

```text
Global Gate5 = 10/18
complete 18-field blocks = 0
Gate5 blocks = 0
CM2 = NO-GO_FOR_CLAIM
```
