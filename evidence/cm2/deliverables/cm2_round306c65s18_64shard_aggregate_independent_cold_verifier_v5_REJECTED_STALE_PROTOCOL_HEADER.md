# C65s18 aggregate cold verifier v5 terminal rejection

Status: `REJECTED_V5_STALE_V4_PROTOCOL_HEADER_BEFORE_PUBLICATION__ZERO_CREDIT`

The v5 verifier source with SHA-256
`e77f7e28ca3553c3523bdd07d03ecd47f6565c2f6c7bb1ab55772b30e38a3dc6`
is terminally rejected.

Its 100/100 self-test, synthetic ordinal publication simulation, and formal
held-script preflight passed.  A separate read-only release audit then found
that the source's opening protocol declaration still said `protocol v4`, while
its schema, paths, status vector, and state machine declared v5 and v4 had
already been terminally rejected.  Publishing a bundle with that contradictory
version declaration would leave the authority contract ambiguous.

The active v5 dual launch was interrupted before either worker completed and
before any publication.  All eleven v5 formal targets were absent immediately
after termination; no staging directory or verifier process remained.  No
shard, aggregate, runtime, canonical, authority, credit, or successor file was
written or changed.

The rejected v5 source must never be imported, resumed, executed as a
prerequisite, used as verification evidence, or included as a release-manifest
member.  Only a separately versioned successor that binds its header, schema,
paths, statuses, bootstrap, and self-test to one exact version may be used.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
