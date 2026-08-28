# C58s2 singleton collision-2 handoff depth-six refinement

## Strict result

`PASS_EXACT_DEPTH6_CONTINUATION__319_INPUT_HANDOFFS__5548_LEAVES__2949_TERMINAL__0_C3_READY__2599_EXACT_C2_HANDOFFS__ZERO_WHOLE_SINGLETON_CLOSED`

C58s2 consumes exactly the 319 frozen C57s1 collision-2 handoffs and continues each exact rational box through at most six further deterministic dyadic levels. It emits 5,548 prefix-free leaves: 2,949 strict exclusions, zero collision-3-ready leaves, and 2,599 exact residual collision-2 handoffs.

This census is intentionally fail-closed. The remaining rows are collision-1 H1, regular multi-graph, or outgoing-H1 equality strata. They are not relabelled collision-3-ready, and no unrelated C40 collision-2 row is attached to them.

## Frozen core

- Producer: `b6f399392fb9a042960d7231aeedf49a083198967e6a40d5c703a8a60e20262a`
- Result file: `ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc`
- Result object: `038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30`
- Leaf ledger: `15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df`
- Atomic face/corner owner ledger: `f3e9e60b2b0be82fbbceb5a41a3b49547b03080cd414f146146722f5d7c3370f`
- Handoff summary ledger: `d7fa7095dfc5c44d699adf30e19971ddc0be722ddddaf096e0ece0d9bc6cec9c`
- Parent summary ledger: `6f3a8fa4501cb872a33d7446a14d804eeb352bb6d049158f3c7ee88893b7872d`

## Exact coverage

- Input handoffs: 319, drawn from exactly 97 C40 source rows.
- Exact route evaluations: 10,777.
- Output leaves: 5,548 = 2,949 terminal + 0 collision-3-ready + 2,599 collision-2 handoffs.
- Fully terminal input handoffs: 38/319; 281 still have at least one exact residual descendant.
- Atomic face/corner owner rows: 21,227. Every boundary was resegmented at all rational endpoints, and every incidence set, lexicographic owner, and leaf reference set is complete.
- All 319 source partitions are prefix-free and conserve their exact input volume.
- After combining the new leaves with the 462 C57s1 carried terminal leaves, all 12 reflection-pair parents remain prefix-free with exact Kraft sum `1`.
- Whole pairs closed: 0; whole singletons closed: 0; whole singletons remaining: 24.

## Independent cold verification

The independent verifier did not import or execute the C58s2 producer. It independently replayed all 10,777 numeric routes and matched every exact box, classification, witness, method, and disposition. It also reconstructed every handoff closure/history binding, all 21,227 exact owner atoms, all 319 source partitions, and all 12 combined parent Kraft equations.

- Independent verifier: `3a3c57c0f3aa84b2b8b0f12518a144c53a6959f760822accbf3b68e0dea17cbb`
- Verification file: `054f219baae59fd713fb91718c683e09a660f135aeec0c347cf66465c42a0a89`
- Verification object: `6a2a44da030eabf43ace42d28c55001e61a6c6e4f0de66a09cbfe65eafdf337a`
- Self-test file: `7e8902eb969a6e4cbed47f6af18da335f643b1fe713c3c52a1ab283709201ce3`
- Self-test object: `13bd1b690f745ce7637f78524599480a05f4da3dd325395f903b5c2e7f4eb4ed`
- Coherent hostile tests: 38/38 PASS.

The frozen dependency chain binds C57s1 result object `8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58`, C57s1 verification object `cec8d9bbe3345552b7cb1734c84ed3c1026dc02276780cb6fca9f502118953d6`, C57a audit object `f7984162bdb64c7cbb828e9d3733103637898007c91c89292b64717145b818c0`, and C40 object `397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba`.

## Formal boundary and next dependency

C58s2 is a zero-credit development checkpoint. Candidate authority is false; formal, whole-parent, owner, collision-3-ready, and D02 gate credits are all zero. No runtime, canonical, pointer, seal, or pre-existing file was written. CM2 remains `NO-GO_FOR_CLAIM`.

The next exact step is to continue only the 2,599 residual handoffs using an equality-carrier-aware strict decider. A depth-twelve continuation must consume this frozen checkpoint by deterministic disjoint shards and must independently re-establish full coverage, mutual exclusion, and source/parent Kraft conservation.
