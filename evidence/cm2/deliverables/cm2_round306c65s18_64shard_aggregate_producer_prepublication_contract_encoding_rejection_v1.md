# C65s18 aggregate producer pre-publication rejection

- Recorded: `2026-08-12T15:48:40+08:00`
- Terminally rejected producer file SHA-256: `208b305dc2bae74b2e7db61fe5ad5341b598afb8bba3f26cef85999a9c3b7a68`
- Superseding producer file SHA-256: `345eeb2465951c933893f2e372249e8bcc8d8c072784fa6c6eb2915d5c5a0dd8`
- Failed command: `--aggregate`
- Fail-closed result: `{"reason":"contract canonical compact bytes","status":"FAIL_CLOSED"}`

The rejected source incorrectly required the already frozen, file-hash-pinned
C65s18 v2 contract to use compact canonical serialization.  That historical
contract is strict pretty-printed JSON; its frozen file SHA-256 is
`e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287`
and its semantic object closure remains independently checked.

The failure occurred before either staging build or formal publication.  All
four aggregate output targets were confirmed absent and no staging directory
remained.  No shard, authority, runtime, canonical file, or credit field was
changed.  The rejected source must not be used as a producer, verifier input,
manifest member, prerequisite, or credit source.

The superseding source changes only the frozen-contract parser boundary: the
contract is accepted at its exact pinned file bytes with strict UTF-8,
duplicate-key, nonfinite, JSON syntax, and semantic object-closure checks;
all other closed JSON inputs remain compact-canonical.  Its `py_compile`,
20/20 synthetic/static self-test, exact-64 receipt preflight, controller-exit
gate, and four-target absence check passed.  It remains zero-credit and still
requires independent cold replay after a successful no-replace publication.
