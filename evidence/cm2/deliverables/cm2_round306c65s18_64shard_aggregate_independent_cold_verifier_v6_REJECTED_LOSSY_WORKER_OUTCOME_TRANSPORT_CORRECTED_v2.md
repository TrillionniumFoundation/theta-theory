# C65s18 aggregate cold verifier v6 corrected terminal rejection

Status: `REJECTED_V6_PREPUBLICATION_LOSSY_WORKER_OUTCOME_AND_NONBOOLEAN_VECTOR_GATE__ZERO_CREDIT`

This marker supersedes the uninstalled draft rejection marker with SHA-256
`d0fb9600fce65f144c6a785730fa376977de79d0303354dbc2bd416259580fe1`.
That draft correctly rejected the lossy worker-outcome transport but incorrectly
described the late vector failure as a tuple/list mismatch.  The tuple claim is
terminally rejected and must not be consumed.

The rejected v6 verifier source has SHA-256
`27e0783a00f3fa63df8a8b64d1cb3e48789635580b0d9e073832bbfc7b1c0700`.
Its formal dual-worker launcher returned the exact outer failure line
`{"reason":"worker successful single projection line:","status":"FAIL_CLOSED"}`.
The diagnostic held-script wrapper had SHA-256
`fb10ee065f17ae90da3bda9eb644d864c6315e74eae5e7ea927007148dfcde1d`;
its captured output log had SHA-256
`305d753748fa0c5823b421f11624777d12d3ff0a0833c94157c1214f36a984ee`,
and its exit-status file had SHA-256
`4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`.
These temporary diagnostic files are audit facts only and must not become a
successor prerequisite or release-manifest member.

Two independent read-only post-numeric probes reproduced the exact late label
`projection frozen vector: nonempty vector`.  Source-level reconciliation shows
that `snapshot_vector()` correctly returns a nonempty list.  The actual bug is
the validator expression `type(value) is list and value`: for a nonempty list,
Python returns the list object rather than a boolean, while v6 `need()` rejects
every condition whose exact type is not `bool`.  The correct boundary is an
explicit boolean such as `type(value) is list and len(value) > 0`.

Separately, an internal worker reports its caught fail-closed reason on stdout
and exits one, while the v6 launcher discards that stdout on the failure branch
and retains only stderr.  Thus the formal launcher irreversibly erased the
reason that the read-only probes later reconstructed.

All eleven v6 formal targets were absent after the failed launch.  No shard,
aggregate, runtime, canonical, authority, credit, or successor file was
replaced or promoted.  The rejected v6 source and the superseded draft marker
must never be imported, resumed, executed as prerequisites, used as
verification evidence, or included as release-manifest members.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
