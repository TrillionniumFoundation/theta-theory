# Independent verification of the actual C1 publication

**Result: passed.** At 2026-10-19 09:18:53 UTC, the independent local verifier
reconstructed the complete article and repository control trees from the saved
actual GitHub readbacks collected at 09:16:02 UTC. It does not import or reuse the
transport adapter's hashing functions. No network call, repository mutation,
article edit, or ref operation was performed during this verification.

## Fixed published identities

| Object | Identity |
| --- | --- |
| Published C1 commit | `694952d7d6b886d0087e8560da721bfc980adbc3` |
| Exact sole parent | `fdf2603c8bf422314f199fa431086485a0d1ebb5` |
| Repository root | `56031be3c69251f8eadce010b38d576eaf9497e6` |
| New article | `f0e29499f0d5de75103b6f52cc464945071ea04b` |
| `papers` tree | `adc9a9861cfe39adf7028a9bd9110b97b1858a27` |
| `.github` tree | `0c90f99589321b38edc49b2b48e109833ef514c4` |
| `.github/workflows` tree | `20857a3823e1c4d0b310305fa78d1320e1de2558` |

The article path is `papers/A2-DYN-full-physical-source-author-revision`.
The following actual new-ref readbacks all identify this exact C1 commit:

- `revision/a2-dyn-full-physical-source-2026-10-19`
- `referee-response/a2-dyn-full-physical-source-2026-10-19`
- `referee-copy/a2-dyn-full-physical-source-2026-10-19`

## Complete article and sibling checks

The actual recursive article response reports `truncated: false` and contains
2,796 entries: **2,688 blob files and 108 descendant trees**. Every file path,
Git mode, blob SHA, and byte size agrees with the frozen C1 inventory, for a
total of **285,948,269 bytes**. The frozen inventory also supplies the independently
computed local SHA256 for each matching blob. No file is extra or missing.

The verifier groups the actual recursive entries by their immediate parent and
computes each canonical Git tree object using Git's directory-aware byte order.
Every one of the 108 descendant hashes, plus the article root, agrees both with
the returned remote identity and with the corresponding frozen subtree hash.
The four control trees are independently reconstructed from their complete
nonrecursive responses and compared entry by entry with the expected C1 trees.

The repository scope is exactly:

| Tree | Before | After | Authorized change |
| --- | ---: | ---: | --- |
| Repository root | 187 | 187 | `papers` and `.github` tree pointers |
| `papers` | 212 | 213 | One new full-physical-source article |
| `.github` | 4 | 4 | `workflows` tree pointer |
| `.github/workflows` | 174 | 175 | One new dedicated workflow |

All **212 existing paper entries** and **174 existing workflows** retain their
exact modes, types, and Git identities. All other root and `.github` siblings
remain exact. The dedicated new workflow and its article-local `ci/` copy have
the same mode, blob identity, and byte size. The commit's sole parent and every
root-to-article/root-to-workflow path linkage were also checked explicitly.

## Evidence and reproduction

The `inputs/` directory contains byte-exact copies of the three complete evidence
inputs, with their SHA256 identities pinned inside `verify_c1_remote.py`:

- `C1_FINAL_REMOTE_READBACKS.json`: actual commit, three refs, four control
  trees, full recursive article tree, and the contemporaneous C1 run lookup.
- `C1_TRANSPORT_TO_PUBLISH.json`: complete frozen local file and subtree
  identities against which the actual remote entries are compared.
- `C1_ROOT_EXPECTED.json`: exact planned control trees and their pinned
  preceding baseline siblings.

Run from any working directory:

```sh
python -B /workspace/scratch/b5cc344d4c8e/iteration-20261019b/remote-verification/verify_c1_remote.py
```

The successful execution produced:

- `C1_REMOTE_VERIFICATION_RECEIPT.json`: outcome, scope, pins, commit/ref and
  control-tree results.
- `C1_REMOTE_FILE_CHECKS.json`: all 2,688 path-level file results.
- `C1_REMOTE_SUBTREE_CHECKS.json`: all 109 article-inclusive canonical tree
  reconstructions.
- `C1_REMOTE_SIBLING_CHECKS.json`: every existing entry in the four control
  trees and the explicitly authorized pointer changes.

## Exact limits of this receipt

This verifies the saved actual remote Git identities against fully hashed local
bytes. It does not claim to have independently downloaded all 2,688 blob bodies
again, and does not turn source transport integrity into a continuous-mathematical
proof certificate.

The actual run lookup at **09:16:02 UTC** returned `total_count: 0`. Consequently
this receipt makes **no C1 CI-success claim**. Any later C2/C3 carrier or completed
CI result requires its own actual readback and must be identified separately.

Only the three new refs were read in this C1 packet. Old branch-ref movement was
not rechecked by this verifier. The complete earlier branch census retains its
separate observation time and scope; preservation of old tree siblings is not a
claim that every unrelated branch in the repository stayed stationary.
