# C1 complete transport and C2 CI-trigger transport: exact evidence snapshot

This package preserves all files present in `current-transport` and `current-transport-operations` at the recorded snapshot cutoff **2026-10-19T16:00:49.204947+00:00**. The directory name is historical; the manifest explicitly labels **C1**, **C2**, and shared local preparation. C2 operations are never counted as C1 operations.

The archive contains **957 original files**, totaling **126,338,988 uncompressed bytes**. Every original full request payload, all base64 chunks, both staged-tree plans and complete inventories, the unchanged sealed planner, independent replay, root-timeout diagnosis and all actual operation records at this cutoff are retained byte for byte. No redundant source file was silently dropped. The deterministic tar headers retain original file modes and fix owner/time metadata; the documented member order places each complete blob request immediately before its exact chunks. XZ with a 16 MiB dictionary compresses those duplicate bytes without changing any member.

`C1_C2_TRANSPORT_SNAPSHOT.tar.xz` is **30,438,628 bytes**, SHA-256 **`4971853efc8648407331ad7e714cefc5783a8f2f546af0d41c84da03be601c3e`**. The archive was reopened and **every member** was read, size/hash/Git-blob checked and compared with its original source. No archive code was executed or extracted during verification.

## Files and their meanings

- `SOURCE_FILE_IDENTITIES.json`: every original member path, bytes, SHA-256, Git blob, permissions, phase and evidence class.
- `ACTUAL_OPERATION_INDEX.json`: exact file and JSON-pointer locators for each saved outer MCP response. Nested duplicate content representations are counted once. Generated payloads and the prepared but unexecuted GitHub-only incremental root plan do not become execution receipts.
- `ARCHIVE_VERIFICATION_RECEIPT.json`: actual execution times, archive identity, all-member verification, C1 request/response matching and original commit/root/ref GET linkage, deterministic compression settings, and the explicit snapshot cutoff.
- `PHASE_EVENTS.jsonl`: the actual packaging phases as they occurred.
- `build_transport_evidence.py`: the exact new standard-library packaging source.
- `PACKAGE_FILE_IDENTITIES.json`: identities of this package's files except the identity file itself, avoiding a fictitious self-reference.

The complete C1 scientific commit is **`409fc85c84a5f239d071b8452da48cb73694365f`**, with root **`753cfd8589bc0b7c93942a727ed6925abc214bc2`** and sole parent **`0933e9b44f5b0fd1d1a624d37ffd881d352496f8`**. This packager independently matched the 98 actual base64 blob responses and 28 actual article-tree responses to the generated plan, and parsed the saved actual C1 commit/root/three-ref GET readbacks. The 336 inline blob creations are contents inside tree requests, not 336 separate `create_blob` calls.

All root failures remain: the tree-base immediate-pointer timeout, the baseless all-root-entries timeout, the additional commit-base timeout, and the root lookup that returned 404 before success. The exact successful C1 nested-path request returned the originally expected root. The earlier unchanged diagnosis was written before this combined snapshot; the later commit-base retry is additionally preserved and separately indexed here. No absent historical successful request fields are invented.

C2 uses its own plan and actual response records, including the full-article-path root request. Its expected root is **`b5d618b8a4b356f8ca07f1c9f1238e35d879ede8`** and expected article tree **`b4add0580cc8211223dfa57e6e618e2bf9546d09`**. The manifest and operation index identify all C2 files actually present at the snapshot cutoff. Later files, if any appeared during packaging, are listed separately in the verification receipt and must be archived in the later evidence package; their bytes are not fabricated here.

This is an exact **transport evidence** package. It does not claim that either a prepared request or a created tree constitutes completed CI. Actual CI observation and artifact verification have their separate receipts. This script made no network request, Git change, article/index modification, commit or ref update. Successful finite transport checks do not complete the Lorentz-gas continuum proof obligations.
