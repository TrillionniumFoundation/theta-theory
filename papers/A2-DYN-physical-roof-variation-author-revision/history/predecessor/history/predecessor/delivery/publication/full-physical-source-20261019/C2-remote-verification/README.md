# Independent C2 remote identity and frozen-source verification

**Result: passed at 2026-10-19 09:24:29 UTC.** The verifier independently
reconstructed the complete actual remote article and control-tree identities
from the C2 readbacks collected at 09:21:02--09:21:03 UTC. It then checked the
exact C1-to-C2 file delta and all frozen mathematical inputs. It uses its own
canonical Git tree implementation and does not import the transport adapter.
There were no network calls, article writes, or ref operations.

## Published identities and complete coverage

| Object | Identity |
| --- | --- |
| Actual C2 commit | `228ec6a639d4d195a1a8b869a04dae6f49fece0e` |
| Exact sole parent C1 | `694952d7d6b886d0087e8560da721bfc980adbc3` |
| Root tree | `431dfd86fcd60e50a1469af38343afc470527752` |
| Article tree | `826219579509e91c87c8dfb0c6348e2c42dba178` |
| `papers` tree | `5e7a2dac0fd79daab41e8ed6fa98fca2b7af2531` |
| `.github` tree | `0c90f99589321b38edc49b2b48e109833ef514c4` |
| Workflow tree | `20857a3823e1c4d0b310305fa78d1320e1de2558` |

The full recursive article response is explicitly nontruncated and contains
2,823 entries: **2,710 blob files and 113 descendant trees**. All file paths,
Git modes, blob identities and byte sizes match the exact C2 inventory, totaling
**292,904,889 bytes**. The verifier reconstructs all 113 descendant hashes plus
the article root directly from the actual child entries and compares each with
both the returned identity and the frozen subtree inventory.

The actual revision, referee-response, and referee-copy refs with suffix
`a2-dyn-full-physical-source-2026-10-19` all point to this C2. The parent and
root-to-article/workflow linkages match exactly. All four control trees are
canonical and match the declared C2 construction. Compared with the original
fdf baseline, all 212 older article entries, all 174 older workflows and all
other root siblings remain preserved.

## Exact C1-to-C2 metadata-only delta

The verifier derives the delta from the complete C1 and C2 file identities and
also checks the saved actual C1 file observations. **There are no deletions.**
The only modified existing paths are:

- `PUBLICATION_RECEIPT.json`
- `PUBLICATION_STATUS.json`
- `REMOTE_TRANSPORT_STATUS.md`

All three are explicitly excluded by the unchanged, pinned source manifest.
There are exactly **22 added files**, all under either
`delivery/publication/full-physical-source-20261019/` or
`evidence/current-execution/full-physical-publication-source/`.
The complete list is in `C1_TO_C2_DELTA_CHECKS.json`.

The C1-to-C2 repository scope is narrower than the original-baseline-to-C2
construction:

| Tree | Entry count in both C1 and C2 | C1-to-C2 change |
| --- | ---: | --- |
| Root | 187 | Only the `papers` pointer |
| `papers` | 213 | Only the current new article pointer |
| `.github` | 4 | None; the entire tree is identical |
| Workflows | 175 | None; the entire tree is identical |

Thus the current workflow and all its siblings are also unchanged from C1.

## Frozen source and mathematical fingerprint

The exact manifest is archived in `inputs/SOURCE_MANIFEST.json` and has SHA256
`13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997`.
Its actual Git blob and SHA256 agree with both C1 and C2. Every one of its
**1,668 source inputs**, totaling **122,736,124 bytes**, retains the same Git
blob, local SHA256, size and Git mode across both carriers. The manifest's
complete native core remains 56 files numbered 260--315, and all reachable
native TeX files belong to the checked frozen inputs.

The verifier separately reconstructs the driver's mathematical fingerprint
from the sorted root `.tex`, direct `core/*.tex`, and direct `tools/*.py`
path/SHA256 rows. Both C1 and C2 contain the same 101 rows and yield:

```text
ebe48d08b94fc0dceecce96ecef8e0bc81d91918521ee1ba24558d549d558b26
```

This is an exact source-identity check, not a rerun or replacement of the
mathematical programs. No compilation or mathematical execution was repeated.

## Evidence and reproduction

`inputs/` holds six complete byte-exact inputs: the C2 actual readbacks, C2 file
inventory, C2 expected control trees, C1 actual readbacks, C1 file inventory and
the frozen source manifest. Every input is SHA256-pinned inside the script.

Run:

```sh
python -B /workspace/scratch/b5cc344d4c8e/iteration-20261019b/remote-verification-C2/verify_c2_remote.py
```

Outputs include the summary receipt, all 2,710 file results, all 114
article-inclusive subtree results, every control-tree sibling check, all 1,668
frozen-input results, the 101 mathematical fingerprint rows, and the complete
C1-to-C2 delta. These files are reproducible solely from the archived inputs.

## CI observation and verification limits

The saved actual C2 lookup identifies run **39229329979**, the correct dedicated
workflow and exact C2 head. At **09:21:03 UTC** its status was `in_progress` and
its conclusion was `null`. This receipt intentionally preserves that observation;
it does not assert that CI has completed or succeeded. Any subsequent actual
completion and artifact verification belongs in the separately dated CI packet.

Remote blob identities are checked against complete locally hashed bytes; this
does not claim a second download of every blob body or a continuous-mathematical
proof certificate. The three new refs were checked, but the entire old branch
census was not repeated in this task. Preservation of sibling trees does not
assert that unrelated branches elsewhere in the repository remained stationary.
