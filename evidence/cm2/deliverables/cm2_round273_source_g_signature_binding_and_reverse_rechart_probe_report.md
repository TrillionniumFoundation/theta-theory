# CM2 Round273 pre-freeze probe — signature binding and reverse rechart

Date: 2026-07-29

## Decision

This probe is fail-closed and awards no occurrence, component, maximality,
fibre, disposition, Gate5, D02, or CM2 credit.  It fixes two dependencies that
the formal Round273 producer must respect.

## Frozen signature/frontier census

- Rounds208/269/270/271/272 contain exactly `332,020` frozen local signature
  rows.
- Exactly `36,040` Round208 rows are already named members of the frozen
  `126,468` expanded-occurrence frontier.
- Signature equality is not a physical binding rule: only `560` rows have a
  signature hash occurring in one existing occurrence-supported component;
  `331,460` rows have the same hash in multiple existing components.
- The frozen `63,224`-component frontier has `5,816` components with explicit
  expanded-occurrence members; the remainder are currently virtual-only.
- Round182 has `202,840` collar leaves.  The five signature rounds cover
  `202,776` parent leaves with multiplicity histogram
  `1:73,536`, `2:129,236`, `3:4`.
- The remaining `64` leaves are not orphans: each is the unique RESIDUAL_3D
  leaf in one of Round204's `64` locally completed origins, and they carry
  `96` already-expanded Round204 region rows.

Therefore the formal binding must use frozen origin/leaf/region provenance
and exact positive-dimensional adjacency.  Neither exact-key equality nor
complete-signature equality may union components by itself.

## True-seam dependency correction

The `152` Round268 patch origins are disjoint from the Round182 collar-
occurrence origins.  A direct `patch -> closed-collar signature` join returns
`0|0` incident rows on every patch.  This is not missing data: the incident
physical regions live behind the deferred adjacent-chart guard channel.

Consequently the safe dependency order is:

1. bind the closed-collar signatures to their local expanded region graph;
2. reverse-rechart the positive-volume guards;
3. attach the `152` true-seam patches to the recharted incident regions;
4. only then recompute the DSU quotient.

## Reverse-rechart probe

All `728 + 152 = 880` guard boxes were transformed to the unique adjacent
Source-G chart using the exact identity

```text
(t')^2 = 1-t^2,  p'=p,  s'=s.
```

Every algebraic image was enclosed by an outward dyadic interval and required
to lie strictly inside the adjacent true chart before the pinned Round174
dynamic evaluator was called on the whole enclosure.

- `736` guards resolve directly at a 32-bit dyadic enclosure;
- adaptive full-cover subdivision raises the fully resolved guard count to
  `824/880`;
- these resolved covers contain `5,288` strict signature cells and `44`
  observed adjacent-chart exact keys;
- the eight cyclic directed chart transitions are symmetric, with `661`
  accepted cells per transition;
- `56` guards remain fail-closed:
  - `40` outgoing-chart-seam arrangements;
  - `8` `X=0` wall endpoint/count-transition arrangements;
  - `8` `Y=0` wall endpoint/count-transition arrangements.

The residual families persist under refinement because they cross genuine
event graphs.  More depth is not accepted as closure; they require explicit
half-open graph/wall arrangement rows.

## Current credit and next action

All counters remain frozen at:

```text
quotient                    63,224
expanded occurrences       126,468
exact keys                     116
maximality                0/63,224
fibres                       0/116
dispositions            0/224,580
Gate5                        10/18
D02                        BLOCKED
CM2              NO-GO_FOR_CLAIM
```

Next: build the independently verified Round273 producer for provenance-based
signature/region binding and the 824 complete reverse-rechart guards, while
retaining the 56 graph/wall tails in an explicit residual ledger.  Then close
those 56 by exact arrangements and attach the 152 seam patches before issuing
any DSU union credit.
