# C65s18 aggregate cold self-test v1 — terminal rejection

Status: `REJECTED_PRE_CLOSE_VERIFIER_SOURCE_DRIFT__UNBOUND_SELF_TEST__ZERO_CREDIT`

The file `cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1.json`
is a development-stage self-test and is terminally rejected.  It must never be
used as a prerequisite, verification result, release member, manifest member,
or credit input.

- Rejected self-test file SHA-256:
  `babd294faeaea9db0e5433527ad3a4688f3b22ae8ab053fbd0400feb10c3ce2b`
- Rejected self-test object SHA-256:
  `90f1b65d2b0361b3116919235d081430603cfff53e7aa63d646c7a8dc7422dca`
- Rejected self-test status:
  `PASS_53_OF_53_EXECUTED_COHERENT_FILE_TOCTOU_GZIP_AND_RECEIPT_BARRIER_ATTACKS`
- The rejected object contains no `verifier_file_sha256` field.
- A contemporaneous post-generation verifier source observation was
  `6e1307e97cb17f7678abe6bdec17729b622c3b513ebd36c9f7d9f83af43b504d`;
  the verifier source subsequently changed.

The formal successor is v2.  It is valid only if it embeds the SHA-256 of the
final frozen verifier source, passes two isolated byte-identical cold runs,
and is published no-replace after source freeze.  This marker does not grant
formal, whole-parent, or D02 gate credit; all remain zero.
