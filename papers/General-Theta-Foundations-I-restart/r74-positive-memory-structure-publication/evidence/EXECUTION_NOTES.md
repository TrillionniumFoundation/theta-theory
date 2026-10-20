# Execution record and evidence boundaries

The final successful run is the unchanged `BUILD_RECEIPT.json` in this publication directory. It ran against actual Git HEAD `29b999abf11c43709e64be58765aa1984d13ac91` in strict mode from 2026-10-20 13:39:44 UTC to 13:41:16 UTC. Its source and PDF hashes, 18 diagnostic suites, ordinary/optimized output identity and native LaTeX logs are preserved.

The earlier strict attempt at 13:38:27 UTC stopped while trying to authenticate the source Git object because the default network route could not fetch it. `PRE_FETCH_BUILD_FAILURE.json` preserves that failure. No mathematical diagnostic ran in that attempt. After a successful read-only fetch of the actual remote Git object, a fresh strict output directory produced the final PASS. The failure is not renamed or counted as success.

The precommit draft compile recorded in the source has its own explicitly limited draft status. It is not substituted for the final strict execution. Existing historical CI belongs to its actual historical SHA. The current GitHub Actions query returned zero matching runs for the R74 source; no R74 hosted CI success is claimed. The retained R72 workflow hardcodes a different source path and was not dispatched as if it validated this revision.

`remote-refresh/` contains complete branch-head snapshots and the actual comparison receipts. The 13:41 scan added this R74 source branch and one A2-DYN branch to the original 1,296-head inventory. Both new A2 commits and all 4,403 changed paths were inspected; they concern A2-DYN and its own workflow, not a new General Theta manuscript or report. The fresh delivery scan at 18:33 UTC found the same 1,298 heads, with no new, changed or deleted heads. Those bounded observations are not claims about future repository activity.

The publication changes add only the new sibling publication directory. They leave the verified source tree and all predecessor manuscript/review branches unchanged. The final containing Git commit provides publication identity; this packet binds execution to the earlier source commit deliberately, avoiding a self-referential commit claim.

The validation ZIP carries the complete successful build files, exact finite outputs and native logs, the failed-attempt receipt, remote observations, original visual reports, all 20 contact sheets and the actually inspected full-page details. Full rasterization can be reproduced from the final PDFs with Poppler. All evidence categories remain distinct from formal verification, independent human review and editorial judgment.
