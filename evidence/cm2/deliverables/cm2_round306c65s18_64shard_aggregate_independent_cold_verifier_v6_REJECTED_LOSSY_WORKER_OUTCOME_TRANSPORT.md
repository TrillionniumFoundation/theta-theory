# C65s18 aggregate cold verifier v6 terminal rejection

Status: `REJECTED_V6_PREPUBLICATION_LOSSY_WORKER_OUTCOME_TRANSPORT__ZERO_CREDIT`

The v6 verifier source with SHA-256
`27e0783a00f3fa63df8a8b64d1cb3e48789635580b0d9e073832bbfc7b1c0700`
is terminally rejected.

Its formal dual-worker launch completed no publication.  The launcher returned
the exact outer failure line
`{"reason":"worker successful single projection line:","status":"FAIL_CLOSED"}`.
The diagnostic held-script wrapper had SHA-256
`fb10ee065f17ae90da3bda9eb644d864c6315e74eae5e7ea927007148dfcde1d`;
its captured output log had SHA-256
`305d753748fa0c5823b421f11624777d12d3ff0a0833c94157c1214f36a984ee`,
and its exit-status file had SHA-256
`4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`.
These temporary diagnostic files are audit facts only and must not become a
successor prerequisite or release-manifest member.

The failure was lossy: an internal worker reports a caught fail-closed reason
on stdout and exits one, while the v6 launcher discards that stdout on the
failure branch and retains only stderr.  A separate read-only post-numeric
probe then reproduced the deterministic late worker rejection
`projection frozen vector: nonempty vector`: `verify_once()` retained the
ordered frozen vector as a Python tuple, while the in-worker projection
validator required a list before JSON serialization could normalize it.

This rejection does not prove that the numerical replay is invalid.  It proves
that v6 cannot preserve a worker outcome and that its in-memory projection
boundary is internally inconsistent.  All eleven v6 formal targets were
absent after the failed launch.  No shard, aggregate, runtime, canonical,
authority, credit, or successor file was replaced or promoted.

The rejected v6 source must never be imported, resumed, executed as a
prerequisite, used as verification evidence, or included as a release-manifest
member.  Only a separately versioned successor that fixes both the frozen-vector
type boundary and the bounded worker-outcome transport may be used.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
