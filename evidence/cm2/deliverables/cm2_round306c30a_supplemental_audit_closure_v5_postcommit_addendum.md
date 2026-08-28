# C30a supplemental v5 post-publication replay addendum

The first v5 final commit and all evidence it binds are retained unchanged.
It is not, by itself, downstream authority because the original generic
`validate_core()` re-invoked a stage-10 *freshness* predicate after
publication.  Stage 10 correctly recorded that all official targets were
absent then; after publication those targets must instead be present.  The
same predicate cannot describe both times.

This additive closure separates the two facts:

- retained stage 10 proves the targets were absent at the real preflight and
  pins the exact static tool table;
- post-publication replay requires the six targets and original final commit
  to exist and match, then independently recomputes the complete core,
  attacks, trace audit, stages 95--101, pipeline receipt, and original commit.

Two Docker `network=none`, read-only-rootfs invocations must emit
byte-identical semantic replay receipts.  An additive manifest then binds the
new checker and this addendum, both complete replay-stage evidence trees, the
official replay receipt, the six original publication files, the original
final commit, and the pipeline precommit receipt.  Only a separately pinned
`final_commit_v2_receipt.json` that closes that manifest and both replay exits
is downstream supplemental authority.

No replay receipt, manifest, or v2 commit changes mathematical credit.  C30a
remains exactly `252 -> 92`; `252 -> 90` is forbidden; supplemental additional
whole-origin exclusion credit is zero; D02 is blocked and CM2 remains
`NO-GO_FOR_CLAIM`.
