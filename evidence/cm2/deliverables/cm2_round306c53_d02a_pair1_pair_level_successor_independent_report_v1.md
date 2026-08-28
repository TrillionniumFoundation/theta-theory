# C53 pair1 pair-level successor independent audit report v1

Date: 2026-08-12 (Asia/Shanghai)

## Conclusion

The frozen C53 pair1 candidate passes the cold independent verifier. The
verifier consumed the C53/C51/C50a producer artifacts as inert pinned bytes;
it did not import or execute those producers and performed no runtime,
pointer, claim, receipt, seal, or canonical writes.

This result independently derives the prospective post-seal pair-level
promotion. It is not authority by itself. Formal effect exists only if the
installer atomically commits the predecessor-keyed C50d claim and an
authority seal that binds the frozen candidate, this independent audit, the
promotion derivation, and the effective checkpoint. Until that seal exists,
formal credit and D02 gate credit remain zero and CM2 remains NO-GO_FOR_CLAIM.

## Frozen outputs

- Verifier source SHA-256: `ac6ae0eed9841df386785194bdbb3927736207cef0641dc2f462c9892932b136`
- Audit file SHA-256: `b58a6ba170e43be02ca414208e7197e746183dd335a49982b9ae28dab919497b`
- Audit object SHA-256: `a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c`
- Promotion derivation object SHA-256: `760bbb0098a88995ec9a0e5e340058e72a4074d386a352eb0d34c076b1ea462c`
- Effective checkpoint object SHA-256: `b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab`
- C50d predecessor identity P: `10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41`

The installer-facing JSON field paths are:

- `object_sha256`
- `post_seal_promotion_derivation.promotion_derivation_object_sha256`
- `post_seal_promotion_derivation.effective_post_seal_checkpoint.effective_checkpoint_object_sha256`
- `global_CAS_protocol.predecessor_identity.predecessor_identity_sha256`

## Frozen candidate pins

- Candidate source SHA-256: `c251d1d8bd7ae8f4988824021b0533dc796672939dcb1385d9cafa41fa1152e4`
- Candidate result file SHA-256: `a145e8a67a8f715f61d06c22943c9be40c2470e22da074add440253b9df794d3`
- Candidate object SHA-256: `996b1f213e7fc5a315348a9698960d29a07fd45c0e52c54680961007a28ef052`
- Successor checkpoint object SHA-256: `a1566f78ec92d431aad6ef8f495947e204304a75ebdc81d558031e4dd83fe6a7`
- Pair transaction object SHA-256: `f235583e44679fa19ed470dfe40a884378bd322dc4bb852d34b9e3a246470fb2`
- Global claim template object SHA-256: `abeb575fa8aa4e93f207412ba7450ad91bd444e93403b68d6c60c51ca9363a3d`

## Independent replay results

- Pure verifier self-test: 15/15 PASS.
- C46 public plan: all 64 pair-preserving shards replayed; 575 pending
  representatives and 33,641 default tasks are disjoint and complete.
- Shard 9 genesis: all 589 task states replayed; pair1 is uniquely tasks 0
  and 1; candidate states 2 through 588 remain identical to genesis.
- Pair1 route: two tasks, nine logical terminal leaves, eighteen physical
  sides, two prefix-free frontiers with Kraft sum one.
- Owner bridge: all eighteen C51 physical leaves biject to C50a target
  occurrences; the frozen 52-face/36-corner owner ledger is replayed.
- C42 formal ledger: all 862 parent rows replayed and self-hashed.
- C48 predecessor: the installed logical successor seal and installation
  receipt bind the exact C42 predecessor while preserving zero coarse credit.
- Pair-level projection: pair1 changes from 74 leaves (72 terminal, two
  residual) to 81 terminal leaves and zero residual leaves.
- Prospective coarse census: 574 to 576 paired cells, 1,150 to 1,148
  unresolved cells, and 575 to 574 remaining representatives.
- Prospective four-class census: strict exclusions 75,386 to 75,388;
  typed events remain 296; connected and cemetery classes remain zero; total
  remains 76,832.
- Coherent adversarial promotion mutations: 28/28 rejected fail-closed after
  nested and top-level hashes were recomputed.

## Reproduction

```text
python3 -B deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_independent_verifier_v1.py \
  --verify \
  --expect-verifier-sha256 ac6ae0eed9841df386785194bdbb3927736207cef0641dc2f462c9892932b136
```

The verifier emits one canonical JSON line. The emitted bytes are exactly
1,244,437 bytes and hash to the frozen audit file SHA-256 above.
