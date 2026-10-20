# Independent C2 remote preservation audit

**Result: PASS.** This independent read-only audit checks the actual immutable C2 publication objects against the exact staged inventory and the separately sealed C1 remote objects. It does not claim that CI has completed or that an unproved mathematical theorem is established.

| Object | Actual identity |
|---|---|
| C2 commit | `efde9fa6c45e7835989b653622a9870e59027530` |
| C2 root tree | `b5d618b8a4b356f8ca07f1c9f1238e35d879ede8` |
| C2 article tree | `b4add0580cc8211223dfa57e6e618e2bf9546d09` |
| Sole parent C1 | `409fc85c84a5f239d071b8452da48cb73694365f` |

## Actual complete-tree checks

GitHub's recursive C2 article response is explicitly untruncated. All **3,596 file paths, types, modes, Git blob hashes and byte lengths** match the supplied C2 staged inventory. All **156 directory identities, including the article root**, match the inventory and were independently reconstructed from the actual immediate entries using Git's canonical tree serialization. No file or directory mismatch remains.

The actual C2 root and papers trees were fetched separately and compared with the actual immutable C1 responses. All 186 non-papers root entries are unchanged, including the entire `.github` subtree. Within `papers`, all 213 other article entries are unchanged; only the new A2-DYN article identity advances. Thus the workflow remains the exact C1 object, blob `56e44c7a4e978494c5dba8df023bef5fc8b7cfa4`, with no workflow change in C2. The immediate root and papers hashes were independently reconstructed as well.

## Exact C1-to-C2 delta

There are **exactly 13 file changes and no deletions**:

- Three modified publication/transport metadata files: `PUBLICATION_RECEIPT.json`, `PUBLICATION_STATUS.json`, and `REMOTE_TRANSPORT_STATUS.md`.
- Ten new evidence files under `delivery/publication/marked-boundary-source-20261019/c1-ref-creation/`.

The exact old blob of each of the three modified metadata files is retained under that archive's `prepublication-metadata/` directory. The detailed receipt lists every changed path and old/new Git identity. No mathematical source, proof index, source manifest, original history anchor, or workflow appears in the delta.

All **107 root/core TeX and tool Python mathematical source files** retain their exact C1 Git blob identities and modes. Their path set is unchanged. They therefore preserve the previously independently checked frozen mathematical fingerprint `ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5`. This is byte identity of the same source, not an invented new build or mathematical validation run.

## Actual head observations and scope

Three separate actual Git-ref GETs returned C2 for the author, referee-copy and referee-response branch refs. These are stored moving-head observations. They do not claim that a later evidence-only C3 head is still C2.

As requested, this C2 audit reuses the immutable C1 tree responses and does not repeat the 1,293-old-branch census. That completed C1 census remains its separately timed record; a final C3 head/census should be recorded separately. No current CI-success claim is made here. A workflow result must identify its actual tested commit, even when subsequent evidence-only commits preserve all mathematical source bytes.

## Retained actual evidence

`readbacks/` contains the exact content of seven actual C2 GET responses, each with request/response timestamps and tool metadata. The exact staged expected inventory and copies of the four immutable C1 responses used in this comparison are retained in `inputs/`, with source-path and SHA256 provenance. C1 copies are explicitly identified as reused immutable responses, not new C2 requests.

`verify_remote_c2.py` performs the complete saved-object audit. Its actual exit-zero execution, stdout and stderr are retained in `VERIFY_PROGRAM_EXECUTION.json` and the accompanying logs. `INDEPENDENT_C2_PUBLICATION_AUDIT.json` contains the complete directory checks, exact 13-path delta, all 107 source comparisons, old-metadata retention checks and observed heads. `RAW_RESPONSE_MANIFEST.json` fixes the actual response identities.

No scientific file, index, remote object, branch ref or workflow was modified by this audit. The C1 audit directory was left unchanged. This C2 packet is now sealed and remains distinct from any later publication or CI evidence.
