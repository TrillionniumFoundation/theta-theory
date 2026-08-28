# CM2 eighty-eighth direct assault

Date: 2026-07-22 (Asia/Shanghai)

## Outcome

Round88 closes four finite frontiers without changing the global strict gate
vector.

1. The 6,952 C24 landing residual boxes are reduced to a finite transverse
   event-surface exceptional set.  Positive-volume target-leaf ambiguity is
   zero, and the current frozen atlas has no one-step `RETURN -> RETURN` edge.
2. The finite `s=0` Gate3 two-sided material registry is enlarged from
   `152/176` to `176/176` with whole-collar physical certification.
3. The rank-three registered physical continuation frontier is reduced from
   2,108 elementary arcs to 496 live arcs, and all 496 registered-side endpoint
   pairs are now exact and unambiguous.
4. The fixed collision-density profiles on 152 Gate5 packets have a bounded
   `Reg_alpha` strong synthesis.  The official arbitrary-input F14 operator is
   still absent, so no F14 slot or `14/18` credit is installed.

The strict state remains

```text
Gate 1:             NOT_CERTIFIED
Gate 2:             0/17
Gate 3:             NOT_CERTIFIED
Gate 4:             1/7
Gate 5:             10/18, complete blocks 0
composite gates:    0/5
CM2:                NO-GO_FOR_CLAIM
```

## 1. C24 pullback event-surface closure

Round87 left 6,952 positive-volume residual boxes from 1,952 parents.  The
Round88 interval-AD certificate enumerates every frozen target-boundary event
over those boxes:

```text
box-local event occurrences:  95,436
  landing_t boundary:          73,396
  landing_p boundary:           2,776
  parameter-s boundary:        19,264
```

All `landing_t` and `landing_p` event surfaces are transverse with a certified
absolute partial derivative greater than `7/5`; the `s` derivative is exactly
one.  Hence the exceptional set is a finite union of transverse C1
hypersurfaces and has zero three-dimensional Lebesgue measure.  Off that set,
every residual point lies in exactly one of the frozen 33,960 target leaves.

Therefore

```text
positive-volume target-leaf ambiguity after quotient: 0.
```

Shared target faces are not artificially assigned to a unique closed leaf.

Every residual landing is also separated from the destination core's frozen
RETURN-source hull in the `p` coordinate by more than `1/200`:

```text
landing below RETURN hull: 3,476
landing above RETURN hull: 3,476
```

Together with the pinned 4,216-atom incidence registry, this proves

```text
one-step RETURN -> RETURN edges:                         0
nonempty one-step recurrent same-key subroot:            false
```

This says nothing about a later return reached through a SURVIVE leaf, and it
does not construct stable plaques or holonomy.  Gate2 stays `0/17` and Gate4
stays `1/7`.

## 2. Gate3 finite-root collar completion

The Round87 seam audit showed that exact recutting of the old registry could
not repair 48 zero-area contacts.  Round88 replaces those contacts with 40
deduplicated positive physical collars:

```text
edge-contact incidences:           40
corner-only incidences:             8
unique physical collars:           40
uniform t,p radius:             1/4096
uniform s radius:               1/6400
minimum source-core margin:     7/102400
```

All 16 parent cores replay strict first owner.  On every whole collar, Arb
certifies the branch key, positive collision radicand, strict flight order,
outgoing chart, and the immutable destination core.  Both contacting rows
receive positive area.

The finite-root conclusion is now

```text
s=0 two-sided material coverage on enlarged collar registry: 176/176.
```

This is not global Gate3.  The all-cell/all-depth common material radius,
uniform Piola remainder, global two-sided trace/current atlas, stopped
`MT_DQ`, and common strong recipient remain open.

## 3. Rank-three registered-side quotient

The 2,108 registered elementary arcs split by local outward physicality as

```text
physical-open:      352 components,   496 arcs,   945 physical ports, 47 source ports
nonphysical-open:   920 components, 1,212 arcs, 2,267 nonphysical ports, 157 source ports
source-only:        400 components,   400 arcs,   800 source ports
mixed physicality:    0 components,     0 arcs
```

Thus local physical and nonphysical outward ports never occur in the same
frozen box component.

The first quotient layer pairs the registered endpoints of 320 single-arc
live components.  The remaining 32 multi-arc components contain 1,020 boxes.
An exact centered-Taylor overlap graph performs 1,524 pair tests:

```text
zero-connecting overlaps:       844
strict-zero-excluding overlaps: 680
equality/critical unresolved:     0
```

The graph has exactly 176 zero-set pieces.  Each piece has endpoint degree
two, and the port-to-piece ambiguity count is zero.  Combining both layers
gives

```text
live registered arcs paired:       496/496
distinct registered endpoints:     992
physical-port <-> physical-port:    449
source-boundary <-> physical-port:   47
```

This is the pairing of endpoints on the registered arc pieces.  It is not a
pairing of the 945 physical ports through the unregistered outward region.
Consequently no complete physical-face count, RN row, or Gate5 field follows.

## 4. Gate5 fixed-profile `Reg_alpha` frontier

For each of the 152 finite-root packets, Round87 supplied

```text
dLambda(v)=m(v)dv/M,
rho_v=cos(4r+v)/(sqrt(17)*m(v)).
```

Along the slope-four curves,

```text
|d_(ell_*) log rho_v|<1/80,
dell_*=(kappa+4)|dr|.
```

Equal adapted-length chopping at `delta_*=10^-90` preserves the fixed
`Reg_alpha` mark and obeys

```text
Z_after <= Z_before + 2/delta_*.
```

The resulting synthesis from `ell^1(152)` coefficients on the 152 fixed
collision-density profiles into the frozen strong source completion has cost

```text
< 2*10^90 + 4302.
```

This sublayer survived a conflicting independent audit only after the claim
was narrowed.  The frozen norm ledger still has

```text
regular_density_prefix_suffix_intertwiner = false,
immutable_complete_return_word_operator_registry = false.
```

The finite fixed-profile span is not the arbitrary regular-density input
space required by official F14.  Therefore all proposed keys retain

```text
immutable_F14_slot_id = NOT_MATERIALIZED,
official F14 slots = 0,
finite-root candidate-local maturity = 13/18 unchanged.
```

## 5. Verification

All Round88 producers and verifiers use `.venv-neurips/bin/python`; system
Python is not used for Arb work.

- Pullback closure: 512-bit producer, 1,024-bit independent interval-AD
  replay, semantic `8/8`, pins `11/11`, strict JSON `4/4`.
- Gate3 collars: 512-bit producer, 768-bit independent physical replay,
  semantic `7/7`, pins `15/15`, strict JSON `4/4`.
- Registered component quotient: independent complete incidence replay,
  semantic `6/6`, strict JSON `4/4`.
- Multi-arc resolver: 512-bit producer, 768-bit independent centered-Taylor
  replay, semantic `6/6`, pins `10/10`, strict JSON `4/4`.
- Fixed-profile F14 frontier: 512-bit producer, 1,024-bit independent replay,
  semantic `13/13`, pins `19/19`, strict JSON `4/4`.

All five producer/verifier pairs cold replay byte-for-byte.  The three child
SHA ledgers verify completely, all ten Python sources parse and compile, and
no frozen artifact is zero length.

## 6. Next exact frontiers

1. Continue the 945 physical outward ports through the unregistered tangent
   intervals and type every owner/chart/translation/rank-transition event.
   The registered-side quotient is now exact and no longer the blocker.
2. Search later returns through the SURVIVE target leaves or choose a new C24
   root; the current atlas has no one-step recurrent RETURN subroot.
3. Feed the 40 Gate3 collars into an arbitrary-cell/all-depth Piola and
   two-sided trace/current construction, then build stopped `MT_DQ`.
4. Extend the 152 fixed-profile `Reg_alpha` calculation to arbitrary inputs in
   the frozen regular-density space and prove the same-key prefix/suffix
   intertwiner.  Only then can F14 be installed.
5. Gate1 and the all-depth Gate2/Gate4 stable-material root remain independent
   core fronts and receive no credit from the finite closures above.
