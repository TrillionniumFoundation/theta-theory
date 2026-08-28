# C65s18 64-shard aggregate independent cold verifier v2 — terminal rejection

Status: `REJECTED_PROTOCOL_AND_RUNTIME_CAPTURE_GAPS__SYNTHETIC_ONLY__ZERO_CREDIT`

The verifier source
`cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v2.py`
is terminally rejected.  Its exact rejected SHA-256 is:

`497da169e255f1382965bc867cdf15525f1cfb60934c8ee746ccb2238b4a8f52`

The only completed test claim was a synthetic/static self-test of `85/85`.
That claim is not a numerical cold replay, an installation, a release, a
manifest, or any form of formal evidence.  At rejection time all eleven v2
formal targets were absent: the two seed projections, their two completion
receipts, verification and its completion receipt, self-test and its
completion receipt, postpublication replay, manifest, and outer receipt.

The source is rejected for all of the following audit blockers:

- a legitimate authority-DAG revisit was treated as an error, so the real
  authority closure could not pass;
- the concrete sealed Python/python-flint runtime and its native-library
  closure were not frozen;
- the documented isolated worker flags did not match the actual launch flags;
- the executed verifier bytes were not bound to the held pre-capture file
  descriptor, leaving an exec-path replacement window;
- executable capture, parent-directory identity, exact authority directory
  membership, and the authority edge closure were not one atomic, replayed
  evidence set;
- the private numerical mirror remained writable and lacked exact mirror
  recapture plus a live-workspace open guard;
- installation did not independently repeat the complete formal validation
  needed to bind projections to the current frozen snapshot, and it did not
  fully validate and pair-recapture its newly published result and receipt;
- the two nominal seed workers were drained serially rather than released and
  drained as one parallel dual-run protocol.
- projection validation weakly bound status, aggregate hashes, census, route,
  and whole-source/whole-pair facts, so a coherent rehash was not categorically
  excluded;
- the self-test accepted any at-least-80 truthy mapping instead of one exact
  key set of exact booleans, and release did not byte-recompute it from the
  captured verifier source;
- the eleven-target workflow lacked an exact phase grammar, allowing mixed or
  future-stage artifacts to escape mandatory orphan/supersession rejection;
- the manifest and member set were not captured together after manifest
  publication and again together with the outer receipt after final
  publication, leaving cross-file recapture gaps;
- the numerical context did not explicitly set and attest `flint.ctx.prec=384`
  (the observed import side effect happened to do so, but was not a protocol
  guarantee), nor did it bind the related dps/cap/thread context and restore it
  in `finally`.

The rejected source and any output derived from it must never be used as a
prerequisite, verifier input, release member, manifest member, authority,
terminal disposition, formal credit, whole-parent credit, or D02 gate credit.
All such credits remain exactly zero.  Any successor must use a new version,
must include and validate this marker, and must not import or execute the
rejected v2 source.
