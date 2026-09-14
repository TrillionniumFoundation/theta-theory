# A2 v42 — preservation and historical proof dependencies

## Baseline and exact preserved objects

The baseline is the v41 referee commit `e162532115071265cf73b97a5069f33628347cfe`, whose parent is reviewed submission `c730a60bbc8af2a4c6e432813c31dccc897828e7`. The new branch descends from that baseline; it does not overwrite the review branch or merge into `main`.

| Preserved object | Git blob |
|---|---|
| Preceding complete `main.tex`, copied to `history/v41-review-baseline/main.tex` | `1a7a0e4aeba4fda2bdccd54894cd0c7869caa400` |
| Preceding root README, copied to `history/v41-review-baseline/ROOT_README.md` | `3dea5fd278c24291822aaaa49feb6781d28898fc` |
| Preceding paper README, copied to `history/v41-review-baseline/PAPER_README.md` | `dd02e43f8ceb40631e87ad4dfcd3b12a76453383` |
| Original single-offset chapter, retained at its original path | `63ed36efd417cd23e6f869952627719de00e6ef7` |
| Rerooting lemma, unchanged | `a658cbed21f80dd1b79b97e0c026b2127833a239` |
| Complete auxiliary compendium, unchanged | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| Native preamble, unchanged | `7e0de97c08dd2e12187193aff89f3ca4712f430f` |
| v41 introduction, unchanged | `94e056a79877b6a9087534a61627ca4838deb775` |
| v41 proof architecture, unchanged | `8272dc991e74b2c33c38a0106a1da088ce6017ab` |

The archived main retains relative paths interpreted from the original manuscript root. It is an exact historical snapshot, not a replacement build entry from inside its history directory.

## Mathematical delta

The active single-offset chapter is copied in full to `article/23f_single_offset_law_inverse_v42.tex` and its detailed global proof is expanded. The source statements of both theorems, the stability proposition and the finite-flight corollary remain byte-identical. The local density identities, all formulas for the contact-jet inverse, the finite-flight error estimate and the scope paragraphs are retained. The global theorem's hypotheses and conclusion are not changed.

The expanded proof invokes the already proved v40 rerooting lemma at the precise point where the tree must be placed in the anchoring frame. It then gives an explicit same-gauge comparison of two admissible realizations, including cycle holonomies, lattice recovery, tree propagation and all lattice translates. Realizability supplies existence and compatibility with channels outside the selected tree. No extra observation or registration condition is introduced.

The only active main-input substitution at the source-revision checkpoint is `23f_single_offset_law_inverse_v26` to `23f_single_offset_law_inverse_v42`; revision/date metadata are updated. All 54 literal direct inputs, including preamble and bibliography, remain represented. The full 36-input auxiliary wrapper is unchanged. The old inverse chapter, old main, all historical reports and all other programme workstreams are preserved.

## Historical derivations examined and their role

The full v41 report and its source-coverage ledger were read. The v38 historical dependency audit was also read as a historical account, not relabelled as a fresh examination of every file it mentions. The current native introduction, proof architecture, formal geometric setting, observation hierarchy and protocol scope were examined directly. The complete single-offset inverse and the complete v40 rerooting lemma were read together before revising their composition.

The relevant historical chain is: relative finite-flight law and half-line factorization; finite smooth-jet factorization and signed triangular contact inversion; single-offset density cancellation; analytic boundary-image continuation and intrinsic signature matching; common-frame rank-two holonomy recovery; rerooted spanning-tree propagation. The v42 proof makes the last three steps occur visibly in one gauge. The statement is not inferred from the determinant-one jet block or from the final lattice matrix identity alone.

The retained statistical chain remains separate: normalized likelihood limits and noncircular contiguity; original-alternative moment estimates for unbounded quadratic loss; finite likelihood-vector experiments; a uniform moving-boundary modulus and finite-net upgrade to compact two-sided Le Cam convergence. Physical acquisition retains its charged pilot and its observable common-record implementation. These are preserved dependencies, not new universal certificates in this document.

## Preservation is not delivery certification

Preserving the complete Git tree and checking a source delta do not prove that every native input has been compiled. Actual source recovery, compiler execution and PDF inspection are recorded only in `VERIFICATION_V42.md`. In particular, C2 is not closed by the preservation counts above.
