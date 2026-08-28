# C65s18 depth-18 64-shard preexecution report v3

Status: `PASS_PREEXECUTION_V3__AWAITING_SECOND_REVIEW__ZERO_OF_64_SHARDS`

The v2 executor failed closed before creating any shard output because it read
the residual count from a nonexistent contract field.  Its exact source and
preexecution manifest are rejected by the companion zero-write marker.

The corrected v3 executor is frozen at SHA-256
`170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef`.
Its output schema is v3; it deliberately continues to consume the already
frozen v2 assignment domain, inventory, result, and authorization seal.

Before any shard execution, the real `--smoke` path loaded all frozen C61/C58
inputs, replayed the complete 20,879-row assignment bijection, confirmed 330
shard-0 inputs, loaded the full C40 numeric context, and replayed one exact
route.  It created no shard files.  Its closed object is
`41af8efe4211a807264860a6917bcc9091184151c783d5ca17451afad88e948e`.
The C50d/C53/canonical authority snapshot was identical before and after, with
object `c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf`.

The no-import independent v3 verifier pins the exact executor and smoke bytes,
replays the 20,879-row source/inventory bijection, checks every live contract,
assignment, and authorization field path, confirms v3 schemas/targets and the
frozen-v2 assignment domain, and AST-audits the atomic output protocol.  Its
verification object is
`ea4b1c29c7da8094536739ada8e3e1374c5ec2dcd1aa8de2b303c6de890d49b6`.
The real-smoke plus atomic/race/symlink/hardlink/schema/invariant self-test is
59/59 PASS; object
`a60f859f7190f8c113956ead021b73000d3138344b635b47563b99a4b2065055`.

No v3 shard ledger or receipt exists.  Partial statistics and all formal,
whole-parent, and D02 gate credits remain zero.  Shard 0 stays unauthorized
until a second reviewer passes this exact manifest.
