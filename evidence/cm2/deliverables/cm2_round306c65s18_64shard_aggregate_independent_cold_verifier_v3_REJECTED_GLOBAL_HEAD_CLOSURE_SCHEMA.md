# C65s18 aggregate cold verifier v3 terminal rejection

Status: `REJECTED_V3_GLOBAL_HEAD_OBJECT_FIELD_MISMATCH_BEFORE_FORMAL_PUBLICATION__ZERO_CREDIT`

The v3 verifier source with SHA-256
`f799b40c9d5c6a12df74b2b8c7c87d0b6911c9d7c289eaa3a538a81a76a60a22`
is terminally rejected.

Its pinned held-script formal preflight correctly ran before any formal output
was published, but rejected the live C53 global head with reason
`global head: closed object claim`.  The source incorrectly routed this
authority-seal schema through the generic `object_sha256` parser.  The exact
live head instead closes under its schema-defined
`authority_seal_object_sha256` field.  Removing that field and hashing the
remaining compact canonical object reproduces
`cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb`;
the head file SHA-256 remains
`f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3`.

A second independent pre-publication audit also found that v3 required the
contiguous sentence `eleven v2 formal targets were absent`, while the pinned
v2 rejection file contains the same sentence split by a canonical Markdown
newline after `v2`.  Consequently v3 would have rejected that valid pinned
input as well.  Both defects are superseded together; neither may be bypassed
inside the rejected source.

All eleven v3 formal targets were absent both before and after the failed
preflight.  No shard, aggregate, runtime, canonical, authority, credit, or
successor file was written or changed.  The 64 sealed shard pairs and the
zero-credit aggregate remain byte-for-byte inputs only.

The rejected v3 source must never be imported, executed as a prerequisite,
used as verification evidence, or included as a release-manifest member.
Only a separately versioned successor that independently validates the
schema-specific head closure and explicitly manifests this rejection may be
considered.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
