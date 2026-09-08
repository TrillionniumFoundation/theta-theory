# Publication scope and byte identity

The work branch is based on main commit `c04845b6613208406703695c9c184ae461f95805`. It changes the previously empty root README and adds this workstream only. It does not modify any existing manuscript, review report, workflow or permission.

The new technical sources and independent diagnostic program were built/executed locally before publication. Their returned Git blob identities exactly match locally computed Git blob hashes:

| File | Git blob |
|---|---|
| research/A2_Two_Collision_Response.tex | df44402b17031525c087d39dfedf8dac3ada611d |
| research/B2_Chronological_Contact_Reduction.tex | 32d5b6aa9d1df865e6523d4f1309ab305e6164d1 |
| audit/DYN_A1_Proof_Audit.md | fe1f8e751d5291154b986dbcb91717d1ab9be9dc |
| tools/verify_new_results.py | 456ee220fa7c10ab9c7060e63d3a9f774c33646d |

The two technical manuscripts are native single-file TeX and can be built directly from this directory. The audit's complete text is committed as Markdown. Its typeset TeX/PDF, original DYN source snapshot and inherited test/build tree, current raw logs, rendered pages, and the three compiled new PDFs are in the full conversation archive. That archive is larger than this native Git publication subset. The `--include-audit` build option is for that complete archive, not a claim that its formatted audit source is duplicated here.

Statistical A1 v36 is not copied into this directory: its entire existing native tree is available at the separate pinned release reference and immutable author commit. Its mathematics was not revised or rebuilt in this execution.

No remote CI success, journal submission, formal proof verification, worldwide priority, or whole-series closure is claimed. The next proof obligations are retained in README.md and in the technical manuscripts.
