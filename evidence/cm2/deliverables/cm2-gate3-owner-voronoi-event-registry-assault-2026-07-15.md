# CM2 Gate 3 owner/Voronoi endpoint-registry assault

Date: 2026-07-15  
Verdict: **analytic owner partition and target-target endpoint typing certified; immutable physical event rows, global DQ, and scalar matching remain NOT CERTIFIED**

## Scope and predecessor

This continuation works on the rational two-disk torus pilot, the standard
solid-boundary section

\[
N=G\sqcup W,
\qquad |s|\leq 1/400,
\qquad \tau_{\max}<3.
\]

It consumes the frozen eight-chart atlas with 95,596 `multi_candidate` leaf
boxes.  The earlier pair/triple normal-form certificate already proved that
two distinct disjoint target disks cannot be simultaneous *first* events.
The present problem is different: a later-target double tangency can change
the miss trace along one connected first-tangency sheet, so those transition
points must be found before an immutable event-row registry can be emitted.

The executable certificate is
`cm2_gate3_owner_voronoi_event_registry_cert.py`.  It uses exact rational
algebra for all defining polynomials and 256-bit Arb boxes for strict
inequalities.

## 1. Exact owner reduction

For a ray `q+tau*u` and a target disk `T`, put

\[
\ell_T=u\cdot(a_T-q),\qquad
\Delta_T=R_T^2-w_T^2.
\]

Because every pair of candidate disks is strictly disjoint, their ray
intersection intervals are disjoint whenever both are nonempty.  Their
centres are exactly the projections `ell_T`.  Thus the incoming-root order is
the centre-projection order; no radical comparison is needed.

Consequently every one of the 95,596 multi-candidate leaf boxes has the exact
finite Boolean owner partition

```text
Delta_T>0 and ell_T>0 and, for every B != T,
(Delta_B<0 or ell_B<=0 or ell_T<ell_B).
```

After merging chart duplicates this gives:

- 144 global owner predicates;
- 288 global signed tangency sheets;
- 42 owner orbits and 72 signed-sheet orbits under `Jx,Jy`.

## 2. Exhaustive raw endpoint universe

The certificate enumerates every signed common-tangent descriptor between a
distinguished tangent target `T` and another target `B`:

- 82,048 target-target common-tangent descriptors;
- 576 source-grazing equations, with at most 1,152 roots before identity
  reduction;
- 576 parameter-boundary sheet rows;
- 288 constant-polarity split equations `u_y=0`.

The corrected target-target first pass classifies 81,760 descriptors strictly
on the whole parameter window and leaves 288 descriptors whose Arb boxes
contain a transition.  Its exact classification counts are:

| class | count |
|---|---:|
| no source intersection | 71,088 |
| target tangency behind source | 4,976 |
| nonphysical earlier tangent behind source | 3,556 |
| source-grazing identity boundary | 832 |
| target tangency after `tau=3` | 348 |
| physical target but other is not next | 312 |
| earlier tangent physical but target still occluded | 248 |
| nonphysical target strictly occluded | 176 |
| source-grazing transition unresolved | 176 |
| nonphysical earlier tangent strictly blocked | 128 |
| target-time endpoint unresolved | 76 |
| physical earlier occlusion boundary | 48 |
| physical later miss-switch boundary | 48 |
| earlier-tangent visibility unresolved | 16 |
| target visibility unresolved | 8 |
| target-after-earlier unresolved | 8 |
| later-miss order unresolved | 4 |

The rows sum to 82,048.

## 3. Closing the 288 corrected first-pass descriptors

Adaptive exact-dyadic subdivision to depth 24 produces 3,328 regular
subinterval leaves and resolves 284 of the 288 descriptors without any
endpoint collar.  The remaining leaves merge to four disjoint transition
collars.  Their maximum width is

\[
\frac{11}{1677721600},
\]

or 22 depth-24 grid widths.  They form one four-element `Jx,Jy` orbit.

### 3.1 Forward-time audit and explicit retraction

An earlier common-tangent partner can occlude `T` only when its own contact
is forward:

```text
ell_B > 0.
```

The initial classifier required that `B` be first in its comment and typing,
but omitted this explicit test.  That omission produced a now-retracted set
of 16 purported physical third-target vertices.  Replaying those descriptors
with the missing condition proves, over the full parameter window, that

```text
ell_B < 0.
```

Their partner contacts lie behind the source, so they are not forward
physical boundaries.  The corrected physical-transition vertex count from
this registry is zero.  For auditability the manifest preserves the old
320-row set digest

```text
c04fc55676bcb0341c24f8ae5f50116913bb9b70b18ca901873c7e1ff15238a2
```

and marks the 16-vertex claim as retracted rather than silently deleting its
history.

### 3.2 Four residual collars are uniformly nonphysical

The four corrected collars surround a crossing of the distinguished target time
through `tau=3`.  On the entire collar the common-tangent partner satisfies

\[
0<\ell_B<\ell_T.
\]

Thus `T` is uniformly not the first event on either side or at the crossing.
These four collars, one `Jx,Jy` orbit, are discarded from the physical
first-event endpoint registry.  No numerical isolation of the irrelevant
`tau=3` root is used to claim a physical row.

Therefore the post-audit count of numerically unresolved target-target
transition collars is **zero**:

```text
82,048 descriptors
= 81,760 whole-window strict
+ 284 resolved by adaptive strict subdivision
+ 4 uniformly nonphysical tau=3 crossings.
```

## 4. Why the miss trace really must be cut

The certificate also rules out a tempting shortcut: the miss owner is not
constant on a connected physical target-tangency sheet.  On the full window
`|s|<=1/400`, it covers the connected path

```text
source=G, chart=G:E, target=W[0,0], epsilon=+1,
0<=t<=3221/5000
```

by 10 Arb boxes of maximum depth 4 and proves that `W[0,0]` remains the
physical first tangency throughout.  Nevertheless the strict next target is
`G[1,1]` near `t=0` and `G[2,1]` near `t=3221/5000`.  Thus a later-target
double tangency can change the miss trace without producing equal first
roots.  The target-target curves above are genuine row-cutting boundaries,
not optional bookkeeping.

## 5. What this does not certify

The preceding equality is an endpoint-*typing* result, not yet a global
event inventory.  The following finite but essential work remains open:

1. quotient duplicate algebraic endpoints produced by distinct raw
   descriptors;
2. cut each of the 288 signed sheets into all connected visible components;
3. prove a constant miss trace and a constant parameter-coarea polarity on
   every component;
4. emit immutable physical event rows with exact hit/miss trace maps and
   coarea/current data;
5. assemble the global distributional derivative quotient (`DQ`) and prove
   row-by-row and scalar matching.

The certificate therefore prints

```text
GATE3_ANALYTIC_SINGLE_OWNER_PARTITION: CERTIFIED
GATE3_CONNECTED_IMMUTABLE_EVENT_ROWS: NOT_CERTIFIED
GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED
```

No statement in this report upgrades Gate 3 or unconditional CM2.

## 6. Reproduction

Run with python-flint available:

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_owner_voronoi_event_registry_cert.py
```

Then run the manifest self-test and replay verifier.  The replay/integrity
path must pass, while the live global verdict must return exit code 2 until
the five open items above are supplied.
