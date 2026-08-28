# CM2 Round189 source-G endpoint-p refinement spike report

## Question

Can bounded bisection in the existing `p` coordinate close the 288
Round188 factor faces that:

- remain after the exact Round188 census
  `16,132 = 15,844 resolved + 288 residual`;
- touch exactly one atlas endpoint, `p = -1` or `p = +1`;
- have an unavailable full-face `dp` enclosure at that endpoint; and
- retain a strict `ds` enclosure?

This is a face-level feasibility question only. It is not a request for
whole-leaf, side-specific return-signature, source-G global-disposition, or
CM2 claim credit.

## Method

The read-only probe is:

`cm2_round189_source_g_endpoint_p_refinement_probe.py`

It pins and checks the current inputs before using their data:

| Input | SHA256 |
|---|---|
| Round186 probe source | `5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64` |
| Round188 probe source | `11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de` |
| Round182 manifest | `32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5` |
| Round182 result | `e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d` |
| Round182 verification result | `61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797` |

The complete seven-entry Round182 manifest is checked for exact entries and
all seven file hashes are rechecked. The Round182 verification must remain
`PASS`.

This is still a probe-only trust boundary: Python imports Round188, which
imports Round186, before Round189 can check their hashes. The checks therefore
detect an unexpected workspace after import, but they are not an adversarial
import sandbox. A formal verifier must pin inert bytes before loading any
independent evaluator.

The probe performs the following steps:

1. Reconstruct all 18,324 outgoing-W residual leaves from the pinned Round182
   rows.
2. Rebuild the exact Round186 unresolved-face census and the Round188 split
   `16,132 = 15,844 + 288`.
3. Require every selected residual face to have `dp = UNAVAILABLE`, strict
   `ds`, graph axis `s`, and exactly one endpoint at `p = -1` or `p = +1`.
4. Adaptively bisect only unresolved faces along `p`, with requested maximum
   depth 2.
5. On every node, apply Round186 resolution first. Only a Round186
   `ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET` node is passed to the
   Round188 boundary-arrangement test.
6. Treat only the following as face-level resolved:
   `BOTH_FACTORS_STRICT`, `ONE_ACTIVE_FACTOR_ABSENT`,
   `ONE_ACTIVE_FACTOR_FULL_GRAPH`, and
   `UNIQUE_TWO_ENDPOINT_FACTOR_CURVE`.
7. Check exact `p-s` area conservation separately for every original face,
   exact child bounds, coincident internal split edges, and the complete
   binary-tree census.

The requested run was:

```bash
cd deliverables
/usr/bin/time -v -o /tmp/cm2_round189_depth2.time \
  env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=189052 \
  ../.venv-neurips/bin/python -B \
  cm2_round189_source_g_endpoint_p_refinement_probe.py \
  --p-depth 2 \
  > /tmp/cm2_round189_depth2.json \
  2> /tmp/cm2_round189_depth2.stderr
```

The script has no output-path option and performs no runtime filesystem
writes. The files under `/tmp` above are shell redirections used to retain
the diagnostic result and resource measurements.

Static checks also passed:

- Python compilation succeeded.
- An AST read-only audit found no file-writing API in the probe.
- `--p-depth 5` was rejected before computation with exit status 2 and empty
  stdout; legal depths are exactly 0 through 4.

## Evidence

### Pinned artifacts and run identity

| Artifact or result | SHA256 |
|---|---|
| Round189 probe source | `118f0ec0333562026294ba4667cf7498403c4b6274378921afaa3819ef9323e4` |
| `/tmp/cm2_round189_depth2.json` bytes | `a124a7f95d71eeadcb41bad4bfed9a5a82ee56197b34dabc7a8296f7fbae9d46` |
| Canonical `probe_result` | `459d8c019a49ae844e6f83c127f0b1a418f557eba460a3d659d4a76b24cc7eca` |

The canonical result digest was recomputed independently from the retained
JSON and matched its embedded digest.

Resource measurements:

- exit status: `0`;
- wall time: `2:57.94`;
- user CPU time: `176.90 s`;
- maximum resident set size: `671,156 KiB`.

### Exact cohort reconstruction

Round186 was reconstructed as:

| Round186 face class | Count |
|---|---:|
| `BOTH_FACTORS_STRICT` | 4 |
| `ONE_ACTIVE_FACTOR_ABSENT` | 1,172 |
| `ONE_ACTIVE_FACTOR_FULL_GRAPH` | 1,104 |
| `ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET` | 16,132 |

Round188 then reconstructed exactly:

| Round188 disposition within the 16,132 faces | Count |
|---|---:|
| `UNIQUE_TWO_ENDPOINT_FACTOR_CURVE` | 15,844 |
| `BOUNDARY_ENDPOINT_COUNT_RESIDUAL` | 288 |

The 288-face endpoint cohort has:

- 288 distinct leaves and 8 distinct origins;
- 144 lower-t faces and 144 upper-t faces;
- 144 faces touching `p = -1` and 144 touching `p = +1`;
- derivative pair `UNAVAILABLE|STRICT_NEGATIVE` on all 288 faces;
- zero faces belonging to a two-sided U|U leaf.

The last fact does not discharge the separate U|U obligation. All 88
two-sided U|U leaves remain outside this endpoint cohort and still require
cross-t curve ordering. The 64 wall-G residual leaves also remain outside the
probe.

### Depth-2 refinement result

At depth 0 all 288 roots are Round188
`BOUNDARY_ENDPOINT_COUNT_RESIDUAL`.

| Depth | `BOTH_FACTORS_STRICT` nodes | Endpoint-residual nodes |
|---:|---:|---:|
| 0 | 0 | 288 |
| 1 | 320 | 256 |
| 2 | 256 | 256 |

Consequently:

- 32 of the 288 original faces are fully resolved;
- 256 original faces remain residual;
- the 256 depth-2 residual terminals split evenly between the two endpoint
  sides: 128 at `p = -1` and 128 at `p = +1`;
- every newly resolved node is `BOTH_FACTORS_STRICT`;
- no new node was closed by an absent-factor, full-graph, or unique
  two-endpoint-curve classification.

The tree census is exact:

| Quantity | Count |
|---|---:|
| split nodes | 544 |
| child nodes | 1,088 |
| terminal nodes | 832 |

The checked identities are:

- `1,088 = 2 × 544`;
- `832 = 544 + 288 roots`;
- split nodes by depth are 288 at depth 0 and 256 at depth 1.

Exact `p-s` area is conserved both globally and separately for every original
face:

```text
input     = 1/655360
resolved  = 1/819200
residual  = 1/3276800

1/655360 = 1/819200 + 1/3276800
```

Thus depth 2 removes 80% of the selected face area but leaves a nonempty 20%
endpoint strip.

All 544 internal p-split edges were checked for exact child-edge
coincidence and measure-additive area conservation. Their half-open ownership
and signature glue were deliberately not materialized:

`PENDING_FORMAL_HALF_OPEN_EDGE_OWNERSHIP_AND_SIGNATURE_GLUE`

## Verdict: PARTIAL

Bounded p refinement works as a geometric narrowing mechanism, but it does
not close this endpoint cohort.

At each refinement level the interior sibling becomes
`BOTH_FACTORS_STRICT`, while a one-sided child that still touches
`p = ±1` remains. After depth 2, 256 of 288 original faces still retain that
endpoint branch. This is evidence against treating additional fixed finite
`p` depth as the completion mechanism.

This verdict is restricted to the 288-face feasibility subquestion. It does
not invalidate factorization or the Round188 boundary arrangement, both of
which remain useful away from the endpoint singularity.

## What worked

- The exact Round186 and Round188 censuses were reproduced from the pinned
  chain.
- The endpoint residual was isolated to only 8 origins with a perfectly
  symmetric `p = -1` / `p = +1` and lower / upper distribution.
- Adaptive p splitting certified a large strict interior region.
- Exact per-face area, child-bound, split-edge, and binary-tree invariants
  all held.
- The probe made no whole-leaf or global promotion.

## What failed or remains open

- Fixed finite p depth did not remove the branch that contains the exact
  endpoint.
- No side-specific local return signatures were materialized.
- The 544 internal split edges have no formal half-open owner or signature
  glue.
- The exact endpoint edge is still a lower-dimensional carrier rather than a
  certified absence or curve object.
- The 88 U|U leaves still need cross-t curve ordering.
- The 64 wall-G leaves remain untreated.
- The probe imports before checking hashes and therefore is not a formal,
  adversarially independent certificate/verifier pair.

## Recommendation

Do not continue by merely increasing fixed `p` depth. Instead, investigate a
one-sided rational endpoint chart, separately for
`sigma ∈ {-1, +1}`:

```text
p   = sigma (1 - u^2) / (1 + u^2)
r_p = 2u / (1 + u^2)
u >= 0
```

Here `u = 0` represents the exact endpoint `p = sigma`, and the square-root
identity becomes rational:

```text
1 - p^2 = 4u^2 / (1 + u^2)^2.
```

This chart is a recommendation only. Round189 did **not** implement, run, or
validate its interval behavior, derivative bounds, orientation, atlas
coverage, or glue semantics.

A follow-up spike should first test whether the 256 persistent endpoint
branches become strict absence, a regular one-sided graph, or an explicit
`u = 0` incidence under that chart. A formal round would then need:

1. complete per-child and per-endpoint evidence rows;
2. an explicit lower-dimensional `u = 0` carrier;
3. half-open ownership of internal edges and side-specific return-signature
   glue;
4. separate U|U cross-t ordering and wall-G treatment;
5. a verifier that pins all producer and upstream bytes before import and
   independently reconstructs every row.

Until those obligations are met, the strict global state remains:

- whole-leaf credit issued by Round189: `0`;
- source-G global dispositions: `0 / 224,580`;
- D02: `BLOCKED`;
- Gate5: `10 / 18`;
- CM2: `NO-GO`.
