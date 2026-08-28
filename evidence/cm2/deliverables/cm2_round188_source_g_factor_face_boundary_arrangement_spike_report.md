# CM2 Round188 — source-G factor-face boundary-arrangement spike

Date: 2026-07-26  
Verdict: `PARTIAL`

## Question

Can the `16,132` Round186 outgoing-W factor faces that have one strict
inactive factor and one regular active factor, but no whole-base bracket, be
replaced by a finite, dimension-safe clipped-curve arrangement using full-face
derivatives, strict corner signs, and the four rectangle edges?

## Method

The read-only probe
`cm2_round188_source_g_factor_face_boundary_arrangement_probe.py` was run at
SHA256

`11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de`.

It pins the frozen Round182 package and the hardened Round186 probe, rebuilds
all `18,324` outgoing residual leaves and their `18,412` unresolved t-faces,
and independently reproduces the Round186 factor taxonomy.  For each of the
`16,132` no-complete-bracket faces it:

1. separates the strict inactive factor from the active factor;
2. chooses `p` or `s` only when the corresponding full-face derivative is
   strict;
3. evaluates the active factor at all four exact corners;
4. classifies every boundary edge either by a strict C0 exclusion or by a
   strict tangential derivative and its two endpoint signs; and
5. accepts a face-level curve only when exactly two boundary edges contain a
   unique bracketed zero and the other two edges are certified zero-free.

This gives a regular zero set that is single-valued over the transverse
coordinate and has exactly two unique boundary endpoints.  The probe does not
materialize the evidence rows as an attachment, does not build side-specific
return signatures, and issues no whole-leaf or global credit.

The final run used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=188052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round188_boundary.time \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round188_source_g_factor_face_boundary_arrangement_probe.py \
  > /tmp/cm2_round188_boundary.json \
  2> /tmp/cm2_round188_boundary.stderr
```

An earlier development run stopped on an assumption that both full-face
partial derivatives must be available.  No result from that stopped run is
used here.  The final criterion instead requires one strict graph derivative
and independently classifies every edge by its own C0 or tangential
derivative evidence.

## Evidence

The final run exited zero:

- elapsed: `3:04.13`;
- maximum RSS: `728,316 KiB`;
- probe result SHA256:
  `5ff61905ab33608571222bb0e99cb2c5cadb6e6736555fe2a7e0520c3cf5b76f`;
- output JSON SHA256:
  `284b4874532c3466032c6bc03f9249348a10fd7614ac0ae4711b8ee9fe5242b9`.

The exact input was reconfirmed:

| item | count |
|---|---:|
| outgoing residual leaves | 18,324 |
| outgoing origins | 8,268 |
| retained children | 11,960 |
| single-U leaves | 18,236 |
| U\|U leaves | 88 |
| unresolved t-faces | 18,412 |

The exact coordinate volume remains

`861459/419430400000`.

The reproduced Round186 face taxonomy is:

| class | faces |
|---|---:|
| both factors strict | 4 |
| one active factor absent | 1,172 |
| one active factor full graph | 1,104 |
| one active factor regular, no complete bracket | 16,132 |

All `16,132` active faces have strict corner signs and at least one strict
full-face graph derivative.  The active factor is exactly balanced:
`HPLUS=8,066`, `HMINUS=8,066`.

The boundary arrangement certifies:

- `15,844` unique two-endpoint factor curves;
- `288` residual faces;
- `15,844` faces using `p` as the graph axis;
- `288` endpoint-degenerate faces using `s` as the graph axis.

Thus the new finite boundary atlas resolves `98.214728%` of the previous
no-complete-bracket face class.  Its five endpoint-edge pairs are:

| unique endpoint edges | faces |
|---|---:|
| `E\|N` | 3,959 |
| `E\|S` | 3,959 |
| `N\|W` | 3,959 |
| `S\|W` | 3,959 |
| `N\|S` | 8 |

The `16,132` compact evidence summaries have SHA256

`9e05d19e2c8f58172463ca645957b7fb5a7041421774cd2623b03545c56e439c`.

Canonical re-hashing independently reproduced the probe-result digest, and
the identities

`18,236 + 88 = 18,324`

and

`18,236 + 2*88 = 18,412`

were rechecked.

## What worked

- The exact factorization reduces every input face to at most one active
  scalar factor.
- Four-corner signs and edge-local evidence replace the overly strong
  whole-base bracket requirement on `15,844` faces.
- Every accepted active zero set has a strict regular graph direction and
  exactly two unique boundary endpoints.
- The method is finite and reconstructible in principle; it does not rely on
  arbitrarily deep uniform `p` refinement.
- The active-factor, side, corner-pattern, derivative-sign, and endpoint-pair
  censuses are symmetric and internally conserved.

## What remains

The `288` residual faces touch a `p=+/-1` endpoint.  Their `p` derivative is
unavailable while `s` remains strict.  Typical rows have opposite corner
signs on the two constant-`s` edges, but those complete edges still overwrap
and lack a strict `p` derivative.  A bounded `p` split near the endpoint is
therefore the targeted next probe; it is not necessary to refine the other
`15,844` faces again.

Even complete face-level resolution would not alone close the source-G gate:

- the `88` U|U leaves require the two face curves to be ordered and glued
  across `t`;
- the separate `64` wall-G residual leaves are outside this probe;
- all accepted curves still need full evidence rows, half-open edge
  ownership, split lineage, and side-specific local return signatures; and
- an independent verifier must rebuild the entire arrangement without
  importing or executing its producer.

## Promotion boundary

This spike is diagnostic only:

- evidence attachment emitted: `false`;
- whole-leaf credit: `0`;
- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next formal route is a factorized clipped-face certificate comprising the
`15,844` accepted curves, targeted endpoint refinement for the remaining
`288`, explicit U|U cross-t ordering, the wall-G tail, full dimensional
ledgers, and an independent verifier.
