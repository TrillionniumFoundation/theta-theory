# CM2 one hundred thirty-fourth direct assault

Date: 2026-07-24

Strict verdict: **the missing Round28-ID-to-exact-seed-target crosswalk is now
materialized, and the full Round113 parent rectangle is certified to contain
no moving-occurrence tangency root for any of its twelve compatible target
lifts.  This is an exact-seed emptiness theorem, not a global absence theorem.
Gate5 and CM2 are unchanged.**

## Typed incidence crosswalk

Round134 independently types all 64 Round132 occurrence records against the
Round113 exact-seed target geometry:

```text
Round132 occurrence records:          64
source-G compatible records:          44
source-W type mismatches:              20
unique signed target sheets:           16
unique target lifts:                   12
```

Round122 supplied an empty physical-face audit but did not type-join the
Round28 occurrence IDs.  Round134 installs that missing join.  The twelve
resulting target lifts are pinned as a closed set, so a source-`W` record
cannot be silently retyped as a source-`G` target.

## Whole-box discriminant theorem

The main theorem is proved over the complete Round113 product rectangle:

```text
c0 in [3/65536, 1/16384]
b3 in [1/32768, 1/16384]
s  in [-1/400, 1/400].
```

For every target lift, the verifier performs a 2048-bit outward-rounded Arb
evaluation on the whole box together with the certified implicit-`t` root
enclosure.  No finite sampling inference is used.

The twelve closed enclosures split into:

```text
strictly positive discriminants:   2
strictly negative discriminants:  10
zero discriminants:                0
tangency roots:                    0
uniform absolute strict margin:  > 1/100
```

The two positive cases, `W[-1,-1]` and `W[-1,-2]`, each have two transverse
line intersections.  They are not tangencies.  The other ten targets are
whole-line misses.  The closest enclosure to zero is still strictly negative:

```text
W[-1,0]:
[-374189179/25000000000, -101296291/7812500000].
```

Eight corner values per target agree with the corresponding enclosure sign,
but those values are auxiliary diagnostics only.  The rectangle-wide
conclusion comes from outward interval evaluation over the whole product
box.  The exact-seed Round28 moving-occurrence root count is therefore zero.

## Independent carrier checks

Round122 is independently recounted as:

```text
common children:                    24
child-stage audit rows:             72
stage candidate counts:       57/55/57
candidates per child:              169
total candidate checks:           4056
physical faces:                      0
residual physical faces:             0
```

This proves the same exact-seed collar empty and checks all seven physical
boundary kinds.  Its scope cannot be expanded to arbitrary parameter fibres.

Round75's 16 physical `R2` components and 32 curves are stationary
destination-core `t/p` boundary preimage crosscuts.  They cannot be renamed
as the required moving occurrence-pullback family at an active transverse
tangency root.  That proposed substitution is
`REJECTED_TYPE_MISMATCH`.

Likewise, a tailored analytic leaf through a face witness is not by itself a
canonical component, and a parameter-`s` hit/miss germ cannot replace a
fixed-`s` plaque-side and path proof.

## Frozen frontier

The scoped exact-seed result is `CERTIFIED_EMPTY`.  Actual nonempty `n>=2`
occurrence incidence elsewhere remains `UNKNOWN_NOT_CERTIFIED`, not empty.

The first unpaid construction is:

```text
one genuine fixed-s, n>=2, parent-W/path component
crossing a Round28 moving-occurrence graph
→ complete primitive-free active fibre
→ regular transverse rank-zero root
→ owner minimization and recordwise q_j output.
```

Round134 materializes zero new occurrence-pullback return components,
rank-zero components, complete active primitive fibres, owner keys,
recordwise `q_j` outputs, Round67 owned `Omega_j` records and global complete
18-field blocks.

## Independent verification

The verifier does not import or execute the Round134 producer.  It
independently rebuilds the typed crosswalk, performs all twelve whole-box Arb
evaluations, and recounts all 4056 Round122 checks.

The formal result is `PASS`.  It rejects:

- all 69 re-signed semantic mutations, including crosswalk, interval-sign,
  target-root, corner-role, materialization and global-promotion attacks;
- all 18 strict-JSON attacks, including duplicate keys, non-integral numeric
  forms, non-finite constants, encoding attacks, trailing documents,
  surrogate and envelope/digest attacks;
- missing, tampered, aliasing, symlink, hardlink, FIFO and protected-output
  paths.

Dual `PYTHONHASHSEED` replays are byte-identical to the formal verification
artifact.

## Strict global state

```text
exact-seed Round28 occurrence incidence:             CERTIFIED_EMPTY
actual nonempty n>=2 incidence elsewhere:            UNKNOWN_NOT_CERTIFIED
new nonempty occurrence-pullback components:         0
new complete active primitive fibres:                0
new owner keys / recordwise q_j outputs:              0 / 0
new Round67 owned Omega_j records:                    0
global complete 18-field blocks:                     0
Gate5 maturity:                                      10/18
Gate5:                                               NOT_CERTIFIED
CM2:                                                 NO-GO_FOR_CLAIM
```
