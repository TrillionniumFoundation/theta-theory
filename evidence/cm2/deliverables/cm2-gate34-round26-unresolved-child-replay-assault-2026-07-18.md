# CM2 Gates 3/4 — Round-26 unresolved-child fresh replay leaf

Date: 2026-07-18  
Status: append-only strict leaf; no aggregate or recursive root modified

## Frozen conclusion

The frozen round-25 split plan contains 26,876 `UNRESOLVED_OUTER`
parents and schedules exactly two children per parent.  This leaf reconstructs
all 53,752 scheduled boxes and freshly runs the 384-bit Arb whole-box
trichotomy on every child.

```text
RETURN_AT_1_INNER          4,088 children
SURVIVE_THROUGH_1_INNER    2,048 children
UNRESOLVED_OUTER          47,616 children
                           ------
TOTAL                     53,752 children
```

The corresponding parameter-averaged unnormalised base masses are

```text
RETURN_AT_1_INNER        5953/1024000000
SURVIVE_THROUGH_1_INNER 17319/1024000000
UNRESOLVED_OUTER          38701/256000000
                         ----------------
TOTAL                       44519/256000000.
```

Thus the one-generation residual outer-base-mass ratio is exactly

```text
(38701/256000000)/(44519/256000000)
  = 38701/44519
  < 7/8,
```

and the newly resolved base-mass ratio is

```text
1 - 38701/44519 = 5818/44519 > 1/8.
```

This is a strict numerical statement for this single frozen refinement
generation.  It is not promoted to a uniform multigeneration boundary-tube
rate, a collision-SRB weighted tail, or a complete R1/Q1 partition.

## 1. Frozen plan consumption

The input plan is bound to

```text
cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json
SHA-256 6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86
```

and its complete reconstructed split-record digest is

```text
7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b.
```

The producer does not trust only the three representative records retained
in the compact F7--F9 manifest.  It regenerates all 26,876 split records from
the 33,960 frozen adaptive rows, sorts them by parent atom ID, and requires
the complete digest and the three representative records to match.

All current unresolved parents are at depths 12 or 15.  Under the frozen
largest-parent-normalised-side rule with tie order `t,p,s`, all scheduled
splits are along `t`; the child depths are therefore 13 or 16:

```text
depth 13: RETURN 0,    SURVIVE 1,728, UNRESOLVED 11,904
depth 16: RETURN 4,088, SURVIVE   320, UNRESOLVED 35,712.
```

No midpoint value assigns a class.  Every terminal assignment in this leaf
comes from the strict closed whole-box Arb test.

## 2. Child-parent ownership and exact mass conservation

For every frozen parent `P` with path `w`, the leaf independently checks:

1. the two child paths are exactly `w0` and `w1`;
2. the scheduled split coordinate has the exact rational midpoint;
3. all nonsplit coordinate intervals are unchanged;
4. sibling interiors are disjoint and their union is `P` modulo the shared
   midpoint face;
5. each child has exactly half the parent's rational base mass;
6. the two child masses sum exactly to the parent mass;
7. child paths are unique and prefix-free inside each source core;
8. the frozen complete next-collision first-owner witness passes to each
   child by source-domain inclusion.

The global parent and child mass sums both equal
`44519/256000000`.  There are 53,752 unique child atom IDs and 26,876 exact
two-child parent packets.  Their full canonical digests are

```text
parent-group rows
1ff91e8ec667380cc4215c35e6b6c8f8a7f047a395111d16daeadef4a95791dc

sorted child atom IDs
0cb99b470605e15b4072782a6005189e99b6601b78f4b9304d275ec6354336fc
```

## 3. Fresh 384-bit whole-box trichotomy

Each child is reconstructed as an exact rational `(t,p,s)` box inside its
source physical core.  The frozen round-25 collision map is then evaluated
at `ctx.prec=384`.  Admission is fail-closed:

- `RETURN_AT_1_INNER` requires the full image enclosure to lie strictly
  inside exactly one of the complete 24-core destination registry;
- `SURVIVE_THROUGH_1_INNER` requires a strict separator from every eligible
  destination core;
- any chart-boundary, core-boundary, or collision-geometry ambiguity remains
  `UNRESOLVED_OUTER`.

The 4,088 return children hit 16 destination cores.  Every child row carries
the source and parent IDs, exact source box, split record, child side,
first-owner witness binding, output enclosure, classification-witness digest,
rational mass bracket, and the exact invariant-area Jacobian seed.

The canonical full-row and class-frontier digests are

```text
all 53,752 child rows
8b4231dd12755ad51bfcb177ed573a26d0e4144eebf2f0282b5b7949abb58be9

RETURN_AT_1_INNER rows
754c57bd537cff1575ded4e524cab1c26739636fc2b7bf2f82d1023a3d3c7a76

SURVIVE_THROUGH_1_INNER rows
95c96a656f164bfa5696a12265baeac42cecc9e1eca11dde532ef9f2e84fea69

UNRESOLVED_OUTER rows
9c2c63341e3bedcb329fdebc9b901a87b36cbf5c12ed70f44f5ed512cdc905ed
```

The manifest is deliberately compact: the deterministic full rows are
materialized on replay, while the JSON retains the full digests, 24 per-core
count/mass summaries, seven representative children, and the exact global
counts and masses.  The independent verifier reconstructs and reclassifies
all 53,752 children rather than trusting producer summaries.

## 4. Independent fail-closed audit

The verifier does not import the round-26 producer.  After hash-checking the
producer and frozen dependencies, it separately:

- parses JSON with duplicate-key and nonfinite-value rejection;
- rebuilds the complete split plan with its own axis/box/record functions;
- reconstructs every child and calls the frozen audited 384-bit classifier;
- independently builds child IDs, row payloads, parent packets, per-core
  summaries, depth histograms, mass sums, and class-frontier digests;
- compares every result to the compact frozen manifest;
- checks the complete prefix-free and per-parent mass-conservation contracts.

The replay passed, as did integrity and all 66 hostile mutations.  Hostile
tests include forged counts, masses, split axes, ownership flags, raw-row and
frontier digests, promoted strict conclusions, duplicate JSON keys, and
nonfinite JSON values.  Half the result mutations recompute the internal
digest before presentation, so the separately frozen result digest remains
necessary and active.

Default live mode exits `2` and reports that the complete one-step R1/Q1
partition and Gate 5 are not certified.

## 5. Exact nonpromotion boundary

```text
FROZEN 26,876-PARENT SPLIT PLAN REPLAY:          CERTIFIED
53,752 FRESH 384-BIT CHILD TRICHOTOMIES:         CERTIFIED
CHILD-PARENT PREFIX OWNERSHIP:                   CERTIFIED
EXACT PARENT/CHILD BASE-MASS CONSERVATION:       CERTIFIED
ONE-GENERATION UNRESOLVED BASE RATIO < 7/8:      CERTIFIED

RESIDUAL UNRESOLVED CHILDREN:                    47,616 NONEMPTY
RESIDUAL UNRESOLVED BASE MASS:                   38701/256000000
RESIDUAL CHILDREN PROMOTED TO R1 OR Q1:          0
FINITE-DEPTH OUTER-COVER EXHAUSTION:             NOT CERTIFIED
UNIFORM MULTIGENERATION BOUNDARY-TUBE DECAY:     NOT CERTIFIED
COMPLETE STEP-1 R1/Q1 PARTITION:                 NOT CERTIFIED
ARBITRARY-n PHYSICAL R_n/Q_n PARTITION:          NOT CERTIFIED
q-WEIGHTED RETURN TAIL:                          NOT CERTIFIED
INDUCED STRONG LASOTA--YORKE COEFFICIENT:        NOT CERTIFIED
GATE 3:                                          NOT CERTIFIED
GATE 4:                                          NOT CERTIFIED
GATE 5:                                          NOT CERTIFIED
CM2:                                             NO-GO FOR CLAIM
```

## 6. Next strict executable leaf

The residual 47,616 child boxes are the only admissible next frontier from
this leaf.  The next refinement must:

1. consume their frozen class-frontier digest and reconstruct their exact
   parent links;
2. apply the same fair largest-normalised-side policy (the scheduled next
   axis is determined per current box, not assumed from this report);
3. freshly classify every grandchild by a whole-box enclosure;
4. prove a second independent residual-mass ratio before proposing any
   summable boundary-tube law;
5. keep all remaining outer boxes out of R1 and Q1.

In parallel, the already strict Q1-inner survivor boxes may seed later
physical `R_n/Q_n` iterations, but each new branch must be created with its
numeric mass, unstable Jacobian/distortion, common forward/reverse
restriction IDs, and strong `q_n` load.  None of those arbitrary-n or strong
operator fields is supplied by this one-step refinement leaf.

## 7. Frozen artifacts and replay commands

- `cm2_gate34_round26_unresolved_child_replay_cert.py`
- `cm2_gate34_round26_unresolved_child_replay_verifier.py`
- `cm2-gate34-round26-unresolved-child-replay-manifest-2026-07-18.json`
- `cm2-gate34-round26-unresolved-child-replay-manifest-2026-07-18.sha256`

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round26_unresolved_child_replay_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round26_unresolved_child_replay_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round26_unresolved_child_replay_verifier.py \
  --self-test
```

Frozen leaf hashes before the leaf-chain file itself:

```text
producer  237440eb97921c9c79aec04fbc0d664f0dc7d34accf5d98d27db0323675b04d6
verifier  ec5f2ded54513fa949e698ec8d7c6a096aa9222ddedc3a0827b1279247cd65f6
manifest  64bc7a9a17e62483a8b8249056ffd007426abd1b825bc875d5e736641d8bc9dd
```
