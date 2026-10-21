# Actual source publication and remote execution observations

The mathematical source was pushed on the sole new revision branch at commit 86c947eccea6029258d9a362624866a475118a66. Its exact source, parent and tree identities are given in ../../PUBLICATION_RECEIPT.json and in the immutable-source audit at ../post-publication-source/.

SOURCE_PUBLICATION_OBSERVATION.json contains the complete tool-returned data from actual GitHub reads between 2026-10-20 13:01:36 UTC and 2026-10-20 13:01:37 UTC: the immutable Git commit, the new branch ref, push workflow run 39424256218, the latest attempt's job summaries, and its artifact list. It records the real run as queued, job 118632668769 as queued with no step summaries, and an empty artifact list. No completed checkout, remote mathematical command, compiler pass or success is inferred from those values. No explanation for the queue was supplied by these readbacks.

POST_SOURCE_REMOTE_HEADS.txt is a fresh complete git ls-remote --heads result after the source push. POST_SOURCE_REMOTE_REF_AUDIT.json compares it with the original 1,296-head census: the only addition is the requested new revision branch at the source SHA; no preexisting head changed or disappeared.

The original source-commit PUBLICATION_STATUS.json described preparation before its own publication and is preserved unchanged in ../post-publication-source/source-commit-explanatory/. The current ../../PUBLICATION_STATUS.json records actual publication and the explicitly timed remote observation. A later observation, if recorded, has a separate file rather than overwriting the earlier result. The current documentation/evidence carrier is a descendant of the source commit; it does not claim to be a CI-tested checkout.

The 62 completed local mathematical commands, actual native and historical compiler executions, original failure logs and scoped rendered-PDF checks remain in the separately indexed evidence packet. These actual local executions and their frozen-source identity do not depend on a queued remote job completing.

LATEST_CI_OBSERVATION.json separately records fresh reads between 2026-10-20 13:09:40 UTC and 2026-10-20 13:09:41 UTC. The same source run and job remain queued; the step-summary endpoint returns an empty list, and the artifact list is empty. The original13:01:37UTC observation remains intact. The focused documentation readback at ../carrier-document-readback/ fixes the preceding prepared-document snapshot; the later status readback changes no mathematics or execution claim.
