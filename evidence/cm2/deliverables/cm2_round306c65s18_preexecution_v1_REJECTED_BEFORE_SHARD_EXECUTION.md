# C65s18 preexecution v1 rejection

Status: `REJECTED_BEFORE_ANY_SHARD_EXECUTION__ZERO_CREDIT`

The v1 assignment is deterministic and bound to a stable C61 aggregate row
identity plus its exact path, but the runner is not eligible for execution:

1. JSON result and receipt publication used an existence check followed by
   `write_bytes`, rather than a single exclusive-create operation.  A pathname
   substitution race therefore remained between the check and the write.
2. The contract did not freeze the two filtered C61 residual sequence hashes,
   the exact 21-bit source-path rule, or the C61 independent self-test object.
3. The assignment preimage had no explicit C65 assignment-domain literal.

Consequently the v1 contract, runner, assignment inventory/result, and local
preexecution verification are historical preexecution diagnostics only.  No
v1 shard was run; they have zero assignment, formal, whole-parent, and D02 gate
credit and must never be consumed by a C65 aggregate.
