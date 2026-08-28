# CM2 Round306 C52 pair-1 cold independent route audit v1

Status: **PASS COLD INDEPENDENT ROUTE/MARGIN/REFLECTION/KRAFT AND C50a
REQUEST CORRELATION; ZERO FORMAL/D02 CREDIT**.

## Frozen result

- Verifier source SHA-256:
  `6f7ab24f0439b2965e2f406cd9ee2e5078cd43020763a8b658fedf2bd34caeff`
- Full audit file SHA-256:
  `ff4ffe3862722d2ff6a00829cc4fb5f2e0ce691e823bd0f6f1918d783f7c7203`
- Full audit object SHA-256:
  `1667032a6fbbc56cd53983275d8203c2480a2d31c3d4dc3f39b7efaed77ccec4`
- Pure self-test: `PASS_10_OF_10`; object
  `67dca190167e2aeb74c7c4fd396c802045b4a9db1a0a1604499420e758472586`.
- Byte-exact reconstructed C51 route object SHA-256:
  `187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e`.
  Its frozen C52-prefixed file SHA-256 is
  `a560cdae560ce06879e3df3b0265aa97249d879011c7844394da73ea6fb32976`.

## Independence boundary

The verifier does not import or execute the C51 probe producer or the C48
closure producer.  Their files are read only through stable byte reads for
hash pins.  Task selection is rebuilt from frozen C46; C41 and the C32-backed
authority context provide the frozen upstream cells; the separate C40
independent auditor supplies the second numerical C39/C40 implementation.

All pinned sources and C32/C41 authority files are read with `O_NOFOLLOW`,
single-link and pre/post-`fstat` stability checks.  The complete pinned set is
read before imports and again after all numerical work.  Both snapshots are
identical.  The source AST also rejects forbidden producer imports and any
duplicate literal dictionary key.

## Exact result

The frozen C46 64-shard plan selects pair 1 at shard 9, task indices 0 and 1.
Their bindings and independently discovered frontiers are:

```text
daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b
  0, 1

e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6
  00, 01, 10, 110, 1110, 11110, 11111
```

Both frontiers are prefix-free with exact Kraft sum one.  The replay closes
9 logical leaves and 18 physical sides.  Every physical side independently
passes its collision-one strict margin and its collision-two 55-candidate
root/order/screening reconstruction; there are zero unscreened competitors
and 972 positive obstacle-boundary separation rows.  Exact reflected-child
matching gives nine reflection pairs and passes the involution check.  The
terminal owner census is `G[1,0]: 9`, `G[1,1]: 9`.

The reconstructed task-probe hashes are byte exact:

```text
12cf9404b26241f9ce04fe1ba0563cc7e86912b31a7c417dfa7d3c7fac915c30
b24e1872af4fbda8194717fab20d7f8d3b3a93f630c0868a423db845f2665894
```

Together they rebuild the complete C51 object to its frozen hash
`187344a3...`.  The C50a pair-1 candidate/request bindings
`da4557c6...` / `db6292e0...` are consumed as data.  All 18 replacements and
14 two-sided split decisions match the cold replay field for field.  The
separate C50a owner audit object remains `c037b3b1...`.

## Hostile tests and strict boundary

Twenty coherently re-signed candidate/request mutations and two source or
late-authority snapshot mutations fail closed: 22/22.  The audit creates no
candidate, authority, pointer, receipt, seal, canonical update, or runtime
write.  It grants no formal or D02 gate credit.  CM2 remains
`NO-GO_FOR_CLAIM`; a later pair-level successor and no-replace installation
must bind this audit separately.

## Replay

```bash
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c52_d02a_pair1_no_producer_cold_route_verifier_v1.py \
  --self-test

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c52_d02a_pair1_no_producer_cold_route_verifier_v1.py \
  --verify
```
