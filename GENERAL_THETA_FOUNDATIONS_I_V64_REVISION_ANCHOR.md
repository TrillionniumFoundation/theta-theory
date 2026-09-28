# General Theta Foundations I — Revision 64 work anchor

Date: 28 September 2026.

The controlling external report is `GENERAL_THETA_FOUNDATIONS_I_V61_REFEREE_REPORT_R40.md` at `4a99da0aab823418d95631d5dbbd8e9b8178994d`; its companion proof/pipeline audit is `GENERAL_THETA_FOUNDATIONS_I_V61_PROOF_PIPELINE_AUDIT_R40.md` at `02c642d3c08774d2dbaee939ffb2eee57b545f92`. Both review v61, not later revisions.

The base for this revision is the already published v63 candidate `f5c1e5d6eacecc1597fba18697a715f8e7844e09`. Revision 62's return-free occupation and causal strong converse, and Revision 63's exponential accuracy crossover, are inherited rather than advertised as new work. No predecessor branch is overwritten.

Work branch: `revision/general-theta-foundations-i-v64-uniform-streaming-2026-09-28`.
Planned referee branch: `revision/general-theta-foundations-i-v64-referee-ready-2026-09-28`.

The principal new objective is a fully uniform, one-pass numerical streaming theorem for the fixed six rational LPS Bloch rotations: writable bit-space of order `min(N, log(N+1)+L)` at Frobenius mean error `2^(-L)`. The lower bound must be derived from the existing return-free entropy budget; the upper bound must account explicitly for legal outputs, finite integer arithmetic, temporary storage, parameter handling, and per-command time, without a real-table oracle or exact sampler. Written proofs and executable exact-arithmetic regression are separate deliverables.

The full current mathematical development and all historical material remain in the repository. A minimal new journal-facing package will contain the active proofs, not recursively duplicated historical evidence. The response will address the r40 resource and priority objections without changing the journal target or treating CI as proof or acceptance.

This file is a work anchor, not a completed-manuscript, successful-build, independent-priority, or journal-acceptance claim.
