# Source lineage — R51

The new research branch was first created at canonical `18000b21e4bfd89180ccb069e46ac0f21621f34d`. Retention commit `76e232120883128f46abb196e83d33a93d00b098` has canonical as first parent and R50 `c86a43498aceb75355b7e9e810b4efc04a03c61f` as second parent. Its root tree is exactly `e84a14081e05eba86bfce2024ead86ec93045466`, the complete R49 artifact tree. This is preservation, not a new proof or an external endorsement.

The new ordinary source is written under `papers/General-Theta-Foundations-I-restart/r51-causal-acquisition/`. It is not a copy of v96. Its native theorem and full proofs are new files; historical mathematics remains at its original paths. `verify.py` is the unchanged generic R49 source verifier; `build.py` adapts the R49 read-only workflow and calls the unchanged R49 build for the full companion chain. Report input bytes are checked against the original blob.

A compressed transport, when used for GitHub API publication, is only a checksum-verified transport. The publication workflow materializes and commits ordinary UTF-8 mathematical source **before** building. That source commit is separately bound to the artifact commit. The final evidence commit must only add evidence/referee entries and must not modify the already built source or PDF. A source projection hash excludes artifacts and evidence but includes the complete ordinary-source manifest.

No source/artifact/final SHA is guessed in this pre-publication document. The resulting immutable values belong in `artifacts/PUBLICATION_RECEIPT.json` and `evidence/REFEREE_PACKET.md` once observed. All ref updates are fast-forward or create-only; a changed expected head is a failure requiring reinspection.
