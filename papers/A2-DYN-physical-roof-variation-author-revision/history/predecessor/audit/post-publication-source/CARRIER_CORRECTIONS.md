# Documentation corrections following the immutable-source audit

The retained POST_PUBLICATION_SOURCE_AUDIT.md was written against the immutable source commit 86c947eccea6029258d9a362624866a475118a66. Its findings remain unchanged. AUDIT_COPY_INDEX.json fixes the exact copies of its outputs and the original source-commit explanatory files; the scratch mathematical extraction remains reproducible from that source commit.

The documentation/evidence carrier makes these corrections:

1. VALIDATION.md again names the real SOURCE_MANIFEST.json file. The actual source-manifest digest remains 775943e1aa70d53e725956c8ab9eb01edb710c555b89cdcc5f1f9064d463f6c1.
2. The accidentally replaced word PDF/PDFs is restored. The actual compiled main hash remains 8eb1f67c250590ee5dc6c78994f710743ad5bf2f442c5071f7c0d60671235efb.
3. Response 18.2 states that the l−2 intermediate-collision count applies for l≥2 and names the separately proved one-hit case. The native proof already had that case distinction; its bytes do not change.
4. MATHEMATICAL_AUDIT.md and PROOF_LEDGER.md add the actual audit/current-census/319_RECONSTRUCTION.md and audit/current-census/320_RECONSTRUCTION.md paths. LITERATURE_AUDIT.md gives the full audit/current-census/literature/ paths of the two primary-source JSON records.
5. README.md, SOURCE_MANIFEST.md, VALIDATION.md, PUBLICATION_STATUS.json, PUBLICATION_RECEIPT.json and Response 21.9 now identify actual source publication and the inspected CI state. Preparation records at the source commit are retained as preparation; unstarted CI is not relabelled as completed verification.

The carrier's frozen-source verification and separate delivery manifest record its precise scope. This correction note is author-side delivery evidence, not a new referee report or an additional mathematical theorem.
