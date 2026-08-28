# C65s18 executor v2 rejection after zero-write shard-0 attempt

Status: `REJECTED_AFTER_FAIL_CLOSED_ZERO_WRITE_SHARD0_SCHEMA_KEY_FAIL__ZERO_CREDIT`

Frozen rejected executor SHA-256:
`fdb3e4eea8f0e45f5a332e3d153109663f9e31d1661e16c63fd27d6736d582ba`.

Frozen rejected preexecution manifest SHA-256:
`f64f2312513c823a7850c8901e0117b84d701e60b024172dce92800ac1ddf821`.

The first real shard-0 invocation failed closed before any output creation.
`inputs()` attempted to read `contract["assignment"]["source_input_count"]`,
but the frozen v2 contract stores the count at
`contract["selection"]["exact_count"]`.

Post-failure checks found zero v2 shard ledgers and zero v2 receipts.  Runtime,
canonical, authority heads, and seals were not written.  The rejected executor,
its preexecution verification/self-test, report, and manifest are historical
diagnostics only and authorize no shard execution or credit.
