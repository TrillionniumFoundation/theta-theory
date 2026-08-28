# CM2 Round236 — wall residual closure and whole-root finite key partitions

## Verdict

`PASS_PARTIAL_FORMAL_ROUND236`.

Round236 closes the final `16` double-endpoint boxes and `32` crossing-time
boxes left by Rounds 234–235.  Double-endpoint boxes have no prior events and
split into event-absent, positive-event, and negative-event regions.  The two
endpoint graphs have zero three-dimensional volume.  Crossing-time boxes have
strictly opposite endpoint signs, which proves an actual time in `(0,1)`
despite interval dependency; the event is strictly last against all prior
events.

Combining the `12,200` Round234 resolved descendants, `38,328` Round235
single-endpoint partitions, and the Round236 residual closures gives exhaustive
finite exact-key partitions for all `2,640` original wall roots:

- `408` roots use one key;
- `2,216` roots use two keys;
- `16` roots use three keys.

The unclassified wall frontier is exactly zero and the union uses `92` exact
keys.

## Verification and boundary

The independent verifier reconstructs every residual box and all `2,640`
whole-root ledgers without importing or executing the producer.  Result:
`PASS_INDEPENDENT_ROUND236`.  Hash seeds `236071` and `236929` reproduce the
frozen certificate and verification result.

Round236 issues local whole-root finite-key partition credit only.  It does not
issue known-block, component, maximality, or global-fibre credit.  CM2 remains
`NO-GO_FOR_CLAIM`.

## Frozen hashes

- producer: `6eb2641df1b64676f145c922dc074d935813e15ce62fe1bee64309da0e509514`;
- certificate: `b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217`;
- result: `ac436f309e253bc7f727accb8f0b20a6836c239e22e47061633e018670002257`;
- verifier: `b40f558b7ae2bab82f2d4737192967685a136a3f44c3e351760c0b5331d7f175`;
- verification: `153238a6a6678565b58c376c890b6f962af7b59d5572fd949836756c947cec55`;
- verification result: `bd0d9d6983855e8ad06c54e8302feff7ae783a4b1b807eb3cff57478336515c1`.
