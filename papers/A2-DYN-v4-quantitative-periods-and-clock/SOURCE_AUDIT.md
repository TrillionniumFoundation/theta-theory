# A2-DYN v4: sources, report discovery, and preservation

## Exact manuscript inputs

The remote v3 author and referee-copy branches were used as the latest dynamics baseline. The author head is `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191`, repository tree `b3ddcd3b21ec4b6c5c1375aec3232a630f397620`, core tree `6e77aa7666558fb71810bc02194a2da8f66e8ac2`. The mathematical files were read together with the v3 response, source audit, references and analytical requirements.

The v1 baseline is `36f1365041de95ca478739a1e2984734c72f95aa`, paper tree `f1feba6b26237efd5a796a5c224c845aab095b53`. Its specialist handoff was read in full. The mounted v2 delivery archive supplied the unchanged native source and finite diagnostic scripts; matching Git blob hashes were verified against v3. A mounted archive was not interpreted as a remote commit.

The frozen A2-GEOM author source remains `4557df22f5c72bc80943690ecd6c2e39de3734ab`. The located geometry report is `reviews/a2-v43-external-top4-final-rereview-2026-10-04/REFEREE_REPORT.md`, blob `d91833561bb85fcb1b4ac44f4de10482a1e17949`, at review head `af2390e3073acf8ccd90b10d7566e30cbf18c425`. Its title, reviewed source and scope were inspected and exclude its use as an A2-DYN review.

## Report discovery boundary

Branch searches for `a2-dyn` were exhausted through the returned cursors. Before this execution created v4, they returned v1 research/referee-copy and v3 author/referee-copy branches, not a dynamics review branch. A broader `dyn` search and the A2 portion of the `review` branch listing likewise did not identify an A2-DYN report. Default-branch code search and repository commit search for `A2-DYN referee` returned no result. These are recorded search scopes, not a proof that no report exists under an unlocated name or path.

The actual v1 specialist handoff explicitly disclaims independent review. Consequently this revision responds to verified review items and author-side analytical requirements. It does not invent a controlling referee report, quote imaginary criticisms, or import the geometry report's recommendation.

## New source and publication boundary

The new mathematical core is `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`. This SHA was computed independently from the local Git tree encoding and matched the tree returned by the GitHub write action. All v3 proof bodies and labels remain active. All nine old proof-bearing core files are byte-identical to their baseline blobs; new proofs are confined to files 12 and 13.

New manuscript/support files are placed only in `papers/A2-DYN-v4-quantitative-periods-and-clock/`. A dedicated build workflow may be added under `.github/workflows/`. The repository main branch, old manuscript paths and old reports are not edited. Author and referee-copy branches are separately checked against the published commit. Remote publication and remote CI are distinct from the local source-bound build receipt.
