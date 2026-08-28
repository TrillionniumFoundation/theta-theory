# C57a independent audit of the frozen C57s1 singleton collision-1 candidate

## Strict result

`PASS_INDEPENDENT_C57S1_12_PARENT_781_LEAF_3141_OWNER_AND_C2_HANDOFF_AUDIT__ZERO_FORMAL_CREDIT`

The verifier reconstructed the frozen candidate without importing or executing the C57s1 producer. It consumed the producer only as pinned inert bytes and an AST used to prove the absence of a producer import/dynamic-execution path. All authority inputs and candidate ledgers were held through single-link, no-follow file descriptors and re-read against device/inode/mode/link-count/size/mtime/ctime fingerprints.

The initially observed pre-freeze owner ledger was replaced while C57s1 was still being finalized. Those bytes were rejected and never used as audit evidence. After an explicit freeze handoff and an additional delayed snapshot, the final candidate remained stable at 3,141 atomic owner rows. Thus 3,141, not the stale pre-freeze count of 3,493, is the exact audited final census.

## Frozen candidate pins

- Producer file: `52184b7211176dcd8b3321d77ac33143457e0be912769d0486d822a57eef0b13`
- Result file: `9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c`
- Result object: `8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58`
- Leaf ledger: `918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6`
- Atomic face/corner owner ledger: `72d4dd688378166bfd8dbf9ded56ef091014803f80777ea21847a831b4c3f884`
- Parent ledger: `8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510`

## Independent reconstruction

- Rebuilt all 12 selected parent chains through exact C38, C39, C40, and C41 row identities: 164 C38 children, 164 C39 routed rows, 299 C40 leaves, 781 C41 ambient leaves, and 482 C41 split-face rows.
- Recomputed all 781 exact leaf boxes, dispositions, and parent-volume fractions. The census is exactly 462 strict terminal leaves and 319 residual leaves carrying exact collision-2 handoffs.
- Reconstructed every collision-2 handoff object from its open fields and bound it to the exact C35 collision-1 history, C41 outer row, C41 boundary/corner row, exact representative/reflected boxes, and normalized surface IDs.
- Independently checked prefix-freeness and exact Kraft sum `1` for each of the 12 parents.
- Independently atomized all exact box boundaries at every rational endpoint. The resulting geometry is exactly 3,141 atomic face/corner rows. Every incident-leaf set, leaf-to-owner reference set, unique lexicographic owner, and zero-credit field agrees exactly.
- Reconstructed the pinned upstream result objects: C38 `fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434`, C39 `821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02`, C40 `397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba`, and C41 `b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24`.

## Hostile tests

The executable self-test passed 16/16 checks. It rejected coherent mutations of formal credit, D02 credit, terminal/handoff/owner censuses, prefix-freeness, Kraft conservation, and whole-parent closure. It also rejected duplicate-key JSON, NaN, BOM input, symlinks, hardlinks, and a live TOCTOU replacement, and confirmed that the C57s1 producer was absent from imported modules and was never executed.

## Formal boundary

This audit validates a development candidate only. No selected singleton is wholly closed: `whole_singletons_closed=0`, `whole_singletons_remaining=24`. Candidate authority is false, formal credit is 0, whole-parent credit is 0, and D02 gate credit is 0. No runtime, canonical, pointer, seal, or pre-existing file was written. CM2 remains `NO-GO_FOR_CLAIM`.

## Frozen C57a artifacts

- Independent verifier SHA-256: `afa648cc29a1ba627b2e41f7cd45f2d62d1135df212d6483c2c5f7da6e203d1e`
- Independent audit file SHA-256: `9fdbb28605e81de75949486416851f4d2bb233c4953650fcbadd024c12dccbdc`
- Independent audit object: `f7984162bdb64c7cbb828e9d3733103637898007c91c89292b64717145b818c0`
- Self-test file SHA-256: `171d67782e0de1822bf7e069a614c2783ccad08d82a0b353d13e4d96b45111fb`
- Self-test object: `208dd829af13da4ab28691020e9d4012fc3648c86f53ca601b55bcd1ec6e026f`
