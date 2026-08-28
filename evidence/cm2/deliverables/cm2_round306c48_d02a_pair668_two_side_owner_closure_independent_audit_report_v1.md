# C48 pair-668 two-side closure independent audit v1

Date: 2026-08-11 (Asia/Shanghai)

Status: `PASS_INDEPENDENT_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_FULL_GLOBAL_OWNER_AND_GEN1_SUCCESSOR_AUDIT__ZERO_FORMAL_CREDIT`

This audit accepted the frozen C48 candidate as a zero-credit generation-1
successor candidate for the selected pair-668 owner-prerequisite task. It did
not install a pointer, receipt, seal, or formal D02 credit. D02-A and D02-B
remain incomplete; D02-C and D03 remain unstarted; CM2 remains
`NO-GO_FOR_CLAIM`.

## Frozen bindings

- Producer source SHA-256:
  `a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8`
- Candidate file SHA-256:
  `5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e`
- Candidate object SHA-256:
  `61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab`
- Generation-1 successor checkpoint object SHA-256:
  `bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984`
- Independent verifier source SHA-256:
  `e407758719341b69579dec3c73527c441c467b68f9e838dae7c7c4e0cf750a49`
- Independent audit file SHA-256:
  `9c06b31de75e8c751b3d3315f6f9be55e99f5551ae922ab01fdbb01e21327879`
- Independent audit object SHA-256:
  `cf0531127a5cd29625f9bf301646845a3b777d5f2ea973a6d2e085e9ffec380c`

## Independence boundary

The verifier never imported, executed, or called a decision function from the
C48 producer. It treated the candidate as canonical JSON data. It rebuilt the
selection and C46 shard/genesis state from the frozen C41/C46 authorities,
used the older no-C40-producer-import independent numerical implementation as
an additional route oracle, and reconstructed the full C41 physical occurrence
universe twice in opposite traversal orders. Hash/shape agreement alone was
never accepted as proof.

## Cold replay results

- Both physical sides and all six physical leaves were independently
  reconstructed and routed.
- The representative leaves terminated at strict owner mismatch `G[1,0]`;
  reflected leaves terminated at strict owner mismatch `G[1,1]`.
- All six C1/H1 and C2 strict terminal-margin certificates were reproduced.
- Relative frontier `0, 10, 11` is prefix-free with exact Kraft sum `1`.
- Exact reflected leaf boxes, paths, face/corner geometry, incident semantic
  roots, and owner paths form bijections and pass reflection involution.
- Each of two owner sweeps read all 91,879 C41 ambient rows, materialized
  183,758 baseline physical occurrences, and checked the 183,762-occurrence
  replacement overlay.
- The overlay has 20 complete degree-two face atoms and 16 complete corner
  entities. There are 10 full-universe three-way junctions; exactly two are
  internal junctions at which all three selected frontier leaves meet.
- All face and corner incident sets are complete and every lexicographic
  semantic-path owner is unique.
- The generation-1 checkpoint contains all 514 states. Index 0 is the selected
  candidate-closed, zero-credit successor; indices 1 through 513 are canonical
  byte-for-byte equal to the frozen genesis checkpoint.
- Progress arithmetic was independently checked as 33,641 authoritative
  logical tasks pending before C48 and 33,640 after this candidate, while the
  formal C42 coarse census remains `574 paired / 1,150 unresolved / 575 reps`.
- Eighty nested self-hash or sequence bindings passed.

## Hostile tests

All 32 attacks failed closed. Thirty attacks reclosed the top object hash after
semantic mutations, covering source/predecessor drift, route/path/box/C2/margin
tampering, face and corner incidence/owner tampering, successor and genesis
state tampering, progress off-by-one errors, credit escalation, false CM2
promotion, and a runtime-write claim. Duplicate-key and noncanonical-JSON byte
attacks were also rejected.

The first development replay correctly stopped on an auditor assertion that
conflated the 10 full-universe three-way junctions with the two selected-
frontier internal T-junctions. The assertion was corrected to preserve both
separate censuses; the verifier source was then frozen and the full cold replay
was rerun from the beginning to the PASS result bound above.

## Exact replay

```bash
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_verifier_v1.py \
  --verify \
  --candidate deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json
```

The verifier writes nothing and emits one canonical, self-hashed JSON object on
stdout. Any later installer must independently pin the exact producer,
candidate, successor, verifier, audit, and report bytes above and remain
fail-closed on any drift.
