# A2 revision 147 — referee reading guide

The principal manuscript is **geometry.pdf**, built from **geometry.tex**, with theorem/proof-centred AMS mathematical typography. The controlling referee report is `reviews/a2-v146-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md` at commit `855c73b3a0381bebd8d5e0d382fa06125904a73f`. This revision is isolated on `revision/a2-v147-intrinsic-family-descent-2026-09-24`.

## Mathematical reading order

Read the introduction, **First relations, ungraded isomorphisms, and inverse systems**, the inherited tensor-ruling foundations, and **Actual factor descent and moving coefficient spaces**. Then read the retained pencil and finite-neighbourhood proofs, moving-pencil theorem and local inverse. The spectral consequences remain consequences, not independent claims of novelty.

The first-relation proposition identifies exactly what an ungraded isomorphism sees. Its automorphism sequence is represented on every commutative complex algebra; normalized trace recovers the augmentation even over a nonreduced coefficient algebra. The commutant lemma upgrades projective factor information to the actual right vector bundle. The general coefficient theorem allows several varying Schur coefficient subspaces of arbitrary fixed ranks, with one nonzero proper support sufficient to orient the factors.

The new global example consists of two Zariski locally trivial rank-712 thickenings of P1. All their Artin fibres and all nilradical graded vector bundles agree, but their abstract total schemes differ. The reconstructed coefficient maps z^3 and z^3+z have different ramification profiles. This example concerns the general coefficient theorem; its order four is not the order d=n^2+2n-4 of the quadratic-pencil theorem.

All v146 all-pencil, singular-pencil, sharp uniform order, point-local, Schubert-line, moving-family, marked-base-change and spectral results remain in the principal manuscript. Every inherited mathematical part is unchanged. Original root files are preserved under `history/v146-root`; the v146 directory and older branches are unchanged.

## Review and reproducibility

`RESPONSE_TO_V146_REPORT.md` gives the point-by-point response. `ISSUE_MATRIX_V147.json` separates new arguments from verification and editorial questions. `LITERATURE_AUDIT_V147.md` records exact theorem pins and the limited Ballico access. `SOURCE_LOCK_V147.json`, `PROVENANCE_MANIFEST_V147.json` and `evidence/BUILD_RECEIPT_V147.json` bind the sources, executed checks and native PDFs. `NONDELETION_V147.json` records source and mathematical-block preservation.

Run `bash build.sh` here with Python, SymPy, NumPy, native pdflatex and Poppler installed. It runs all 23 inherited scripts plus `check_v147.py`, then compiles all three native PDFs three times and audits references, labels and overfull boxes. The tests check finite algebraic examples; they do not formally certify the global proofs or historical priority.

The separate **applications.pdf** retains its original scope. **archive-v144.pdf** remains a non-submitted historical research archive, not an additional submission supplement. Neither is needed to supply missing proofs of the principal manuscript.

## Literature status

Elias–Rossi's two full texts and Marcus–Moyls's original theorem were checked. Their statements and the distinction from the present first-relation orbit problem are cited in the principal manuscript. Ballico 1993 has progressed from metadata-only access to an inspected publisher first-page image, but the remaining theorem/proof text has not been obtained. The required complete six-axis comparison is therefore still open. Neither mathematical strengthening nor a successful build is claimed to clear that priority question or determine a top-four editorial decision.
