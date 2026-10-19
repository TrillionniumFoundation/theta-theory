# Independent C1 remote publication verification

**Source publication: PASS.** Verified at 2026-10-19T01:57:10.142779Z.

Commit `706aa8d1bca33b0d6268806cca873d57511ad8d9` has parent `15ad3962de63f50911b765fe6608e722fe9b8c82`, root tree `ae3eca89e4210f2a9a44d52493c22df111b75d66`, and new article tree `b0c173ad4f974576d0f639e18b77fe16fbab6ff6`.

| Verification | Result |
| --- | --- |
| Remote article files compared with the exact transport list | 1,964 |
| Remote article bytes represented | 196,803,466 |
| Distinct article subtrees fetched nonrecursively | 60 |
| Canonical tree hashes recomputed, including current and baseline top trees | 68; all match |
| Missing, extra, or mismatched article file identities | 0 |
| Existing paper subtrees changed or removed | 0 |
| Existing workflows changed or removed | 0 |
| Papers | 211 → 212; the new A2-DYN article is the sole addition |
| Workflows | 173 → 174; the new dedicated workflow is the sole addition |

The root changes only the `papers` and `.github` tree pointers. Within `.github`, only the `workflows` tree pointer changes. Every pre-existing sibling entry remains exact, including the complete predecessor article and all companion papers. The newly added workflow blob matches the copy carried inside the article.

## Branch census

The saved branch census contains 1,290 distinct refs, compared with 1,287 in the initial census. It observes exactly the three authorized new A2-DYN refs, each at C1. All 423 pre-existing A2-DYN refs remain unchanged, and no pre-existing ref is missing.

A movement of a pre-existing unrelated-named ref was also observed and is explicitly retained:

| Ref | Initial head | Later observed head |
| --- | --- | --- |
| `revision/general-theta-r73-reversible-memory-normal-form-20261018` | `f3f3f4b521e866a49a567558f41ecd1a98d26363` | `39980d65d6665e52c30aa340cfb0e2eb199c0f9a` |

The receipt makes no attribution for that movement and does not claim that all repository refs were stationary.

## Scope and reproduction

The file comparison uses remotely returned modes, sizes, and Git blob IDs against the transport list computed from the publication bytes. Canonical recomputation verifies all returned tree identities. It does not claim a second download of every blob body, a new mathematical validation, a current-head CI pass, or validation of later metadata-only commits.

Reproduce the saved-response checks with:

```bash
python verify_c1_remote_publication.py --work-dir '/workspace/scratch/b5cc344d4c8e/iteration-20261019'
```

Full path-level result SHA-256: `0acdc3977dc2591626685a10b43ebbc4ab7194a3d57f8f336b3884d649787fcb`.
