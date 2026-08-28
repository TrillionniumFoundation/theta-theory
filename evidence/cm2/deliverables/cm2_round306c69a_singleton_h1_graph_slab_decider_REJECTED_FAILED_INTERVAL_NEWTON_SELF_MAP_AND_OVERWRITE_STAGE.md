# C69a prepublication stage rejected

This marker rejects every current `cm2_round306c69a_singleton_h1_graph_slab_decider_*`
contract/decision/blocker byte artifact produced before a final result, independent
verification, and manifest existed. None of these bytes is a published capability,
an authority, or credit-bearing evidence.

Exact terminal failure from the last run:

```text
FAIL_CLOSED:FailClosed:full graph certificate:
da447793ee1708d0fbe7d91c3ddd3bbd9a3c90c806f0ece3d225680779206049:
{"full_face_bracket":true,
 "newton_axis":true,
 "newton_image":true,
 "newton_self_map":false,
 "newton_strict_derivative":true,
 "nonempty":true,
 "strict_derivative":true}
```

Thus `REGULAR_FULL_FACE_GRAPH` plus a strict monotone derivative and an
opposite-sign full-face bracket does **not** imply that the existing midpoint
interval-Newton image is a strict interior self-map on every one of the 2,356
tasks. The attempted all-2,356 contract is false and is rejected.

The prepublication writer also used direct `path.open("wb")` targets. Failed
retries replaced earlier partial bytes, so these files do not satisfy no-replace
first-publication semantics. They must never be consumed or placed in a manifest.

Frozen rejected-byte inventory after the final failed run:

```text
producer source sha256  a1720425718a4791504c9dac2fe35178db47b6f746be44b9a096ff1145fedba5
contract file sha256    15d1b9f7cb04630ea139057eab6e30b3950cd3d8c0f5e12b5c18f2753aa3dfc9
contract object sha256  26d6bed3d532185f2866504031c974de3604b5864d22d41472dff09810248f5f
decision file sha256    218aa4ff5be27d9f31e8cc05907b855883f818a1a02faee91acf6a2befa4a63d
decision rows           70
blocker file sha256     fcfacf77b3b6c8ac9cd7429393eb0b8a1fe951da2c4a964c7138e580ad39aa84
blocker rows            3361
result                   ABSENT
independent verification ABSENT
manifest                 ABSENT
formal/D02 credit        0 / 0
```

The replacement implementation must write only into two fresh temporary staging
directories, complete two deterministic runs, compare all semantic/file hashes,
and then publish fresh final filenames through exclusive/no-replace creation.
Its decision census must be measured rather than assumed: tasks without a strict
interval-Newton self-map remain fail-closed unless a different independently
proved root enclosure is supplied.
