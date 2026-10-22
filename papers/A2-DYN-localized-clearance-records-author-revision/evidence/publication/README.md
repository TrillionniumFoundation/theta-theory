# Actual publication and exact-source CI

This directory retains observed publication actions and independently reconstructed identities. It is an author evidence packet, not an external referee report or a continuum proof certificate.

## Published source

| Object | Actual identity |
|---|---|
| Branch | `revision/a2-dyn-localized-clearance-records-2026-10-21` |
| Complete source commit | `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` |
| Source commit parent | `03d651b8709d28d90aa435fc12d608ad9c945e23` |
| Source root tree | `d7a4a55f8b5b485bf766eb1fe8bf660618a20902` |
| Complete source article tree | `1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc` |
| Unchanged predecessor subtree | `3010c90e2363dfe1808101a3e992eb02643c28f1` |
| Frozen mathematical/build source digest | `cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0` |

The actual remote source SHA above governs publication. Earlier scratch-local commit identities in retained preparations are not substituted for it. The source commit added only this article and its dedicated root workflow. Existing articles, review branches and companions were preserved.

`ARTICLE_TREE_CREATE.json`, `ROOT_TREE_CREATE.json`, `SOURCE_COMMIT_CREATE.json`, `BRANCH_CREATE.json` and `PUBLISHED_BRANCH_READBACK.json` retain the actual GitHub results. Text and binary object creation receipts are separate from the subsequent branch publication. The complete article tree was independently reconstructed from its exact nonarchive file identities and the unchanged predecessor tree before publication.

## Publication scope and source freshness

`PUBLICATION_TREE_CHECK.json` retains complete original Git tree API objects, the independently reconstructed parent-tree changes, the published commit readback and a fresh check of all five A2-DYN reference prefixes. It found exactly one added A2-DYN ref, this branch. All 434 earlier A2-DYN refs and all 178 review heads retained their original SHAs; the post-publication A2-DYN census is 435 refs at 219 distinct commits. This was an A2-DYN-prefix freshness check, not another full-repository census.

The offline program, actual stdout/stderr and execution receipt are retained here. From the article directory, its read-only reconstruction is reproducible with:

```bash
python3 -B evidence/publication/verify_publication_tree.py \
  --report evidence/publication/PUBLICATION_TREE_CHECK.json \
  --snapshot audit/current-provenance/ALL_REMOTE_HEADS.txt
```

The program recomputes canonical Git objects and the recorded reference differences. Its evidence is explicitly separate from mathematical verification and CI artifact reconstruction.

## The actual source CI

The [source run 39712256295](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39712256295), job `119606068910`, completed successfully on the exact source commit above. The actual clean-checkout `bash build.sh` wrapper ran, and the recorded post-build Git status is empty.

The `ci-39712256295/` directory preserves the run, jobs and artifact API records, the original decoded GitHub job log and artifact `12397079374`. The original ZIP is retained permanently in Git, independently of the Actions retention period:

- Size: 11,054,196 bytes; 247 file members.
- SHA-256: `6ad292d68d0f16743ad222adfd34b6260b67d50d9c2a0205954bc3ed026e2ac0`, identical to the GitHub artifact digest.
- Git blob: `49781fe1085f27e54883cc109f79c28be19e374a`.

The `independent/` directory contains the independent reconstruction program, original execution receipts and results, and retained development corrections to that audit program. The checker reads the actual ZIP, current fixed-source manifest and available committed local execution evidence; its report specifies every comparison and every scope limitation. It does not import or execute the manuscript's own validation driver. CI's own normal/optimized comparisons are distinguished from cross-environment output comparisons. The unchanged predecessor tree mapping can be recomputed from its complete anchor; this does not pretend to rehash predecessor file bytes absent from the temporary post-reset workspace.

## Source run versus its evidence carrier

These receipts necessarily enter Git after the source run. Their carrier is an evidence-only descendant of the named source commit. The 140 frozen mathematical/build inputs, the dedicated workflow and the full predecessor subtree remain unchanged. A carrier's own workflow result must be read under its actual head SHA; the successful source run is never relabeled as a test of another commit. No self-referential carrier SHA is put into its own content.

The full raw pointwise local limit theorem, endpoint same-roof shortage and four-coordinate inverse retain the exact open dependencies stated in the manuscript, response and proof ledger. Neither the publication reconstruction nor a successful CI supplies those missing mathematical conclusions.
