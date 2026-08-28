# C65s18 aggregate cold verifier v4 terminal rejection

Status: `REJECTED_V4_CROSS_PHASE_OUTPUT_PARENT_IDENTITY_SELF_DRIFT_BEFORE_PUBLICATION__ZERO_CREDIT`

The v4 verifier source with SHA-256
`11fe4170702a5f50ab2b3eddec6e8ba81be9759ac95642f1730f865f45c0f0fa`
is terminally rejected.

Its held-script preflight and independent 98/98 self-test passed.  A subsequent
static state-machine audit, while the dual workers were still computing,
proved that the protocol could not safely progress across publication phases.
The frozen input vector records the full seven-field identity of each input's
parent directory.  Most inputs and all eleven formal targets share
`deliverables/`.  Any legitimate no-replace target creation changes that
directory's size, modification time, and change time, so the next phase would
necessarily reject its own valid predecessor evidence.  The same defect would
recur after replay, manifest, and outer-receipt publication.  The release path
also selected the release-round recomputed frozen object instead of the seed
projection's immutable frozen object for replay and outer binding.

The active v4 dual launch was interrupted before either worker completed and
before any publication.  All eleven v4 formal targets were absent immediately
after termination; no staging directory or verifier process remained.  No
shard, aggregate, runtime, canonical, authority, credit, or successor file was
written or changed.

The rejected v4 source must never be imported, resumed, executed as a
prerequisite, used as verification evidence, or included as a release-manifest
member.  Only a separately versioned successor with an explicit publication
directory anchor, exact baseline inventory, ordinal no-replace transitions,
and immutable seed-frozen-object binding may be considered.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
