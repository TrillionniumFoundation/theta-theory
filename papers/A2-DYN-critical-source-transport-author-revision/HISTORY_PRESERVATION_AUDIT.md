# Complete history and isolation audit

The immutable predecessor is the entire article tree a1d21789f9d7c1be801ff4a54d1befad2a47340f at author commit 6cdd9ae88cd358d524ecb89092361ac1522ba351. Its new placement is history/predecessor/. The fixed CURRENT_SOURCE_ANCHOR.json contains every original path, mode, Git blob, byte count and freshly computed SHA-256.

The standalone tools/check_source_preservation.py reconstructs that exact Git tree independently of Git, checks the complete path set and every file's bytes and mode, and then checks the inherited active proofs, all earlier preservation anchors, complete report identities and compressed census manifests. Missing and extra history files both fail. The result is **3,864 files and 485,851,107 bytes** preserved exactly, not just selected mathematical excerpts.

All 59 core proof bodies 260–318 and unchanged model.tex/inputs.tex remain active, byte for byte, and occur exactly once in the native input graph. Earlier main.tex and exposition remain in the immutable predecessor while current author exposition is revised. The old 390-file historical assembly and its original assembler remain unchanged and are rebuilt only in a separate execution copy.

All 91 distinct reports in the freshly exhausted 178-ref census have original-byte placements in this preserved tree. The source audit additionally fixes 370 distinct numbered proof blobs covering every identifier 1–318; one appears under two historical names. Variants, unsuccessful proposals, original model conditions, counterexamples and real execution evidence are retained rather than collapsed into a single latest label.

The four older preservation anchors were independently rechecked: 2,765 complete full-physical-source placements, 2,088 physical-tube-source placements, 74 global-minimizer placements and 1,048 earlier-source placements. These overlap; their counts are not added as if unique.

The scoped Git-tree DAG and branch-source index preserve complete recursively reachable article/review/history/workflow identities, without expanding each of the repository's 1,716,797 latest paths again. Five large inventories are stored as deterministic gzip files with round-trip and identity checks. The full 1,296-head snapshot, 432 A2-DYN refs and 178 review refs identify the read scope. Naming-only exceptions are distinguished from true missing main sources; generated historical v73 inputs were resolved from their retained assembler.

Only the new article directory and its dedicated exact-branch workflow may appear in the revision delta. A final Git comparison records all changed paths and rejects modifications or deletions of any previously existing path. The exact new archive subtree must equal the old article tree. No existing author, review, referee-copy, response, companion or unrelated branch is moved. New remote evidence records actual checked commits rather than rewriting historical receipts.
