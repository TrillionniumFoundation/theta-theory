# CM2 Round306C50 P0 C49 v4 quality review

Status: **PATCHED V4 RUNTIME QUALITY CHECKS PASS; SOURCE BYTES PINNED BY THIS P0 REVIEW; NOT AN INDEPENDENT NUMERIC IMPLEMENTATION; ZERO CREDIT**.

## Outcome

The exact reviewed v4 source is
`cm2_round306c49_d02b_pure_advance_one_collision_v4.py`, SHA-256
`80bb67a46ae4f8a10195aa6b1b17f539708eafc83be4b39bc7724624fd64295f`.
This P0 bundle records that byte pin.  It does not turn v4 into a standalone
C49 release authority: no pre-existing v4-adjacent hash companion, result,
manifest, or independent numeric verifier existed.

The patched source passed all executed runtime checks:

- `py_compile`: PASS;
- producer self-test: `15/15` PASS, repeated twice with object
  `d11ae806d90053a939133c8e1c1fb52580cfcb82c05c2a3a5456110ea8ff0762`;
- complete pair-9 regression: PASS through collisions `3,4,5`, repeated twice
  with object
  `9a39a43907651235a216977a097615aad098be10989617088a6295043857fb17`;
- exact prior numeric-body replay: true;
- split-decision replay: true;
- non-enum `selected_child_bit`: rejected with the expected enum reason;
- non-384-bit public call: rejected with the expected runtime-pin reason.

Both regression and all emitted steps remain `formal_credit=0` and
`D02_credit=0`.  The two global oracles remain absent:

1. `GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE`;
2. `GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE`.

## Version history and source boundary

The formal v2 rejection / v3 diagnostic supersession report exists and its
companion hash is valid.  All nine legacy C49 companions checked by this
review match their target bytes.

The pre-patch v4 observation is retained only for provenance:

- superseded source SHA-256:
  `c4457b66dc1fdf05848011db2e5eb5369a2f90cb57b5b3b2fb99f5026b8bf860`;
- a non-enum right-child marker had been accepted as an unresolved,
  zero-credit object
  `f1d0cf6e29513cdda5ca7ca8e7874bebec0526baab826b37794d609490611644`;
- the same input at 384 and 128 bits had produced distinct zero-credit objects
  `6ceacf1d5eb7d2cca4b169a4a40466a9b5e919602c96eb955b4debbc27340d1d`
  and
  `545361becf0fb89e8dae17393895ede431a814bee47778bd2386fdb06c10eae7`.

The patched v4 closes both of those validation gaps.  They are now covered by
the retained 15-item self-test and by a separate two-check directed runner.

## Independent-implementation boundary

The read-only quality verifier in this bundle imports no C49 producer.  Its
scope is static/file consistency plus verification of recorded runtime
evidence.  It performs no numeric reconstruction and is explicitly classified
as `NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION`.

The directed runtime test imports v4 and is also explicitly classified
`NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION`.

V4 itself directly imports v3 and v2 and reuses:

- `v3.local_numeric_context`, `v3.numeric_step`, and
  `v3.simple_numeric_inputs`;
- `v2.sensitivity_split`, `v2.split_box`, `v2.atlas_box`, and
  `v2.public_box`.

Therefore the P0 no-producer-import independent numeric verifier gate is
`FAIL_NOT_IMPLEMENTED`.  The passing producer regression cannot satisfy that
gate.

## Split replay and runtime consistency

Static inspection and directed execution agree that patched v4 now:

- rebuilds each unresolved split parent;
- recomputes the numeric split decision and exact coordinate;
- checks the selected child box and suffix;
- requires `selected_child_bit` to be exactly `0` or `1`;
- checks `python-flint==0.9.0` and `ctx.prec==384` at both public entries,
  `advance_one_collision` and `adaptive_advance`.

The review-run producer self-test took `2:04.68` with peak RSS `664,848 KiB`.
The review-run complete regression took `3:03.58` with peak RSS
`1,616,940 KiB`.

## File and canonical consistency

The patched v4 bytes match the P0 pin.  The nine legacy C49 companions and
`CM2_LATEST_STATUS.sha256` all verify.  This review did not run an extended
concurrent-replacement, short-read, truncation, or permission-failure matrix;
its file conclusion is limited to deterministic hash consistency.

Canonical remains byte-untouched at SHA-256
`c4d77168b85070ab20c20d64c26d0c0cfcf0b9e3d0ef0acd2fad3006d08e9be9`,
timestamped `2026-08-11 22:15:21 CST (+0800)`.  It contains no C49/v4 entry.
No pointer, authority, seal, or canonical file was edited by this review.

## Reproduction commands

The system interpreter does not contain `python-flint`; numeric runs must use
the pinned workspace environment.

```bash
python -m py_compile \
  deliverables/cm2_round306c50_p0_c49_v4_quality_verifier.py \
  deliverables/cm2_round306c50_p0_c49_v4_directed_runtime_tests.py

python -B \
  deliverables/cm2_round306c50_p0_c49_v4_quality_verifier.py

.cm2-runtime/python-flint-0.9.0/bin/python -B \
  deliverables/cm2_round306c50_p0_c49_v4_directed_runtime_tests.py

.cm2-runtime/python-flint-0.9.0/bin/python -B \
  deliverables/cm2_round306c49_d02b_pure_advance_one_collision_v4.py \
  --self-test

.cm2-runtime/python-flint-0.9.0/bin/python -B \
  deliverables/cm2_round306c49_d02b_pure_advance_one_collision_v4.py \
  --regression

cd deliverables
sha256sum -c cm2_round306c50_p0_c49_v4_quality_audit_manifest.sha256
```

The frozen quality-review object is
`ef464d068810cc3fb447d6496eecfb2036ee97dd19167b1dfbf7398b591fca44`.
It records `formal_credit=0`, `D02_credit=0`, and
`P0_no_producer_import_independent_numeric_verifier_gate=FAIL_NOT_IMPLEMENTED`.
