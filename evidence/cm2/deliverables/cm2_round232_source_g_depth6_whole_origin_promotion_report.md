# CM2 Round231–232 — outgoing-seam depth-6 assault

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND232`

Round231 applies six exact t-bisection levels to all `5,368` deferred
outgoing-chart-seam roots. The t direction is fixed by the upstream strict
t-derivative certificate. It materializes `22,348` strict positive-volume
resolved descendants across `44` exact keys, with zero guard descendants.

The depth-6 residual frontier contains `67,924` boxes. This is an interval
dependency effect, not evidence for that many geometric seam components.
Despite the box growth, the retained coordinate volume falls to
`8923/51968` of the starting outgoing-seam volume: exact released fraction
`43045/51968` (`≈82.83%`).

## Whole-origin promotion

Exactly `2,220 / 5,368` roots have no residual box after depth six. Each of
these origins has the exact upstream partition `1 resolved + 1 retained + 0
guard`. The retained child is covered by `6,804` Round231 resolved
descendants in total. On every promoted origin:

- every descendant has one identical ten-field return signature;
- that signature equals the original Round179 resolved sibling signature;
- descendant volume equals the retained-child volume exactly;
- resolved-sibling plus retained-child volume equals the original origin;
- the finite boxes therefore cover the whole origin with one exact local
  return signature.

Round232 issues `2,220` whole-origin local return-signature and positive-3D
occurrence credits. It issues zero known-block incidence, membership,
physical-component, maximal-component, or global exact-key-fibre credit.

## Independent verification

The independent Round232 verifier reconstructs the 2,220 full-root universe
from pinned Rounds 179, 220, and 231; checks every partition, identity, row ID,
signature, and rational volume equality; and independently reruns the pinned
interval classification kernel on all `6,804` promoted descendants.

Result: `PASS_INDEPENDENT_ROUND232`.

## Frozen hashes

- Round231 producer: `5afa1bc6fc6faec4c9b13be707c93714acdf5dbd09f2fafeefff07c445c517ad`;
- Round231 certificate: `7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374`;
- Round231 result: `83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a`;
- Round232 producer: `a6da65e3c70f335225c91aa4b121164320d3d506975038c3303e87ee4ad1ca88`;
- Round232 certificate: `a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0`;
- Round232 result: `7cbaaba7964555eee3018927688d8c6aa2cdabbf354125ec2b389e92301cb313`;
- verifier: `3d2891de6d809d571a89d00ab77bdbf0a0a6e21949188e1f3416cc5e1cbdf6d6`;
- verification: `a417a0061df3e20153d202f7a4be0eac46a36ef13f1a6839fd70800ab41a1a6e`;
- verification result: `e172ebc533eb18a7f4076fee4c3620801455013698cd4eb29037e6536522ebb8`.

Producer and verifier cold replays reproduce the frozen hashes.

## Gate impact and next route

This closes the local geometric remainder on 2,220 outgoing-seam origins but
does not attach them to the 7,404 frozen known blocks. Official global state
therefore remains: occurrence/block incidence `35,896 / 53,968`, maximal
components `0 / 53,968`, exhausted key fibres `0 / 116`, exact-key
dispositions `0 / 224,580`, Gate 5 `10 / 18`, CM2 `NO-GO_FOR_CLAIM`.

The remaining `3,148` outgoing-seam roots must not be attacked by deeper
uniform dyadic splitting. Their pinned equation has strict t derivative, so
the next route is a parametric interval-Newton/Krawczyk graph certificate for
`target_normal_x^2-target_normal_y^2=0` over each p/s base, followed by exact
two-side return-signature and chart-transition accounting. After this channel
is exhausted, proceed to the `2,640` wall endpoint/count-transition roots.
