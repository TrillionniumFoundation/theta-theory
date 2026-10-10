# A2-DYN v73 revision index

Paper: **Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**.

Active manuscript: [papers/A2-DYN-v73-referee-response/main.tex](papers/A2-DYN-v73-referee-response/main.tex). Start with the [revision README](papers/A2-DYN-v73-referee-response/README.md), [response to the referee](papers/A2-DYN-v73-referee-response/RESPONSE_TO_REFEREE.md), [proof ledger](papers/A2-DYN-v73-referee-response/PROOF_LEDGER.md) and [reading route](papers/A2-DYN-v73-referee-response/JOURNAL_ROUTE.md).

Controlling review: `review/a2-dyn-v72-external-top4-review-2026-10-11` at `fad5823b36f2c68595c6b17bebf62c70032d30a9`. Reviewed paper tree: `bd761b97e603b666ed97b27241f9ab83c7f2550b`.

Revision branches: `revision/a2-dyn-v73-referee-response-2026-10-11` and `revision/a2-dyn-v73-referee-copy-2026-10-11`. The copy branch is to be pinned to the same final revision commit. The initial mathematical checkpoint is `a00e7a814041f3cb4b990324ec706dd1a02e2729`; the assembled handoff follows it by fast-forward commits.

New proofs: common finite roof kernels and physical interfaces; full original scalar-source BV at each fixed collision count by exact threshold mixtures; paired directed-flux capacity; equality of scalar and BL-dual path-numerator ordered errors. The original pointwise LLT target, exact labels, source normalization and zero arithmetic classes remain unchanged. Uniform paired-flux decay and the unconditional endpoint are not asserted.

All 159 inherited core modules remain byte-identical and compiled, together with four new modules. The exact old master, manifest and build script are preserved. `bash papers/A2-DYN-v73-referee-response/build.sh` generates the archival body and opening deterministically, then compiles the full manuscript and emits exact-SHA source, finite-fixture and rendering evidence.

Qualification workflow: `.github/workflows/a2-dyn-v73-qualification.yml`. Only the actual run result and its recorded checkout SHA establish a passing build. Build success is not formal proof certification or independent human review. The original v72 manuscript, report and unrelated paper directories are unchanged.
