# Post-publication provenance and concurrent General Theta R75 scope

## Result

The fresh remote snapshot taken from **2026-10-21T01:24:45.727845+00:00 to 2026-10-21T01:24:46.046360+00:00** contains **1,300 branch heads**. Relative to the 1,299-head pre-push snapshot, its only addition is `revision/a2-dyn-physical-roof-variation-2026-10-21` at `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`. No pre-push head moved or disappeared. The full raw head receipt has SHA256 `cb505b15cbbdad49e250dfe02c427562238c41fefebcc651344c773cd897eb06`.

Relative to the initial 1,298-head snapshot, exactly two branches were added: the concurrent General Theta R75 branch at `bc2952aa9a9695fe9985d491a4156b8975024285` and this A2-DYN source branch. All 1,298 initial heads are unchanged. The intermediate General Theta addition was already present in the pre-push snapshot and was not created by this A2-DYN publication.

## A2-DYN scope

There are **434 A2-DYN-named refs and 218 distinct head commits**: 247 revision refs, 178 review refs, four referee-copy refs, four referee-response refs and one research ref. All 433 pre-existing A2-DYN heads, including all 178 review heads, are unchanged. The only new A2-DYN ref points to the published source commit above. No newer controlling A2-DYN report is introduced by the concurrent R75 branch.

## Exact General Theta R75 delta

The verified first-parent chain is:

`c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0` → `a05bed516b86ea1273ff542e1b2988cd326da214` → `c09682b410148263268a4e7ca3e9a6fed54ed9b9` → `20a3e069a9d7c2dfc0c09852c835ed1863748600` → `bc2952aa9a9695fe9985d491a4156b8975024285`.

The R74 root is `a3e43594b1dec08385c48880906c2c88d5b451ff`; the R75 root is `33a5fd053b8a32995c907df7e2a80a26fcc2bb9d`. Six complete, nonrecursive tree reads, independently rehashed from their Git entries, establish the entire final delta:

**Added:** `papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory`, tree `497886b8961cf12001bbea66909757f93bb8d1ee`.

All **139 other root entries**, all **55 other `papers/` siblings**, and all **29 pre-existing General Theta child entries** have identical mode, type and object SHA. In particular, the `reviews/`, `revision/`, `.github/`, archive and other paper subtrees are unchanged. There is no A2-DYN source, referee, response, CI or publication modification in this R74-to-R75 delta.

The General Theta roots retain the older `A2-sinai-homological-pressure` sibling at tree `e0b5394c9b2e10d81a5b667ef37b3d74efa84027`. They contain no contemporary A2-DYN article directory. They therefore cannot be substituted for the actual A2-DYN author baseline, and their mathematical or review status is not imported into A2-DYN.

This audit establishes tree scope and ref preservation. It does not certify the General Theta mathematics, builds or CI. The commit messages are retained as metadata, not adopted as proof.

## Receipts and method

`POST_PUBLICATION_HEADS.tsv` is the complete 1,300-ref snapshot; `POST_PUBLICATION_HEADS_RECEIPT.json` records its actual command, start/end times, exit code and SHA256. The exact initial and pre-push raw snapshots and their receipts are retained alongside it as `INITIAL_HEADS.*` and `PRE_PUSH_HEADS.*`. `REMOTE_REF_DELTA.json` compares both earlier snapshots. `POST_PUBLICATION_A2_DYN_HEADS.json` records all 434 A2-DYN refs. `R75_SCOPE.json` records the exact ancestry and three-level tree comparison; `TREE_*.json` retains all six untruncated responses. `COMMIT_*.tool.json` retains the five GitHub commit read responses.

The local missing-object read failed because the sandbox proxy connection was unavailable. The successful GitHub-plugin reads replaced that read attempt; `LOCAL_READ_ATTEMPT.json` retains the distinction. The fresh head census used read-only public `git ls-remote --heads`. No ref, index, commit, manuscript or repository file was changed by this audit, and no whole-repository recursive query was made.

`verify_provenance_receipts.py` reconstructs the saved ancestry, all six tree hashes, the scope comparison and head receipt identity. CI is audited separately; this report makes no claim that the newly queued run has completed.
