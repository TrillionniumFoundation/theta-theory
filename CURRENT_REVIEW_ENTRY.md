# A2 revision 164 — controlling review entry

Branch: `revision/a2-v164-collision-wall-crossing-2026-09-26`.
Authored source commit: `7a855e8cec0eb570ab2a1fa68a989644e876323a`.
Latest controlling v162 referee report: `7e9c057907cc4502858a54f32ab0c0cfa264680f`.
Complete post-report v163 baseline: `40a72ddfd85e16363385a1b64b922d61055e875c`.
The reviewed v162 tip is `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`.

## Complete reading objects

**Paper I: Finite failure schemes and the reconstruction of quadratic pencils** — 73 pages. [PDF](papers/A2-v17-boundary-information-coarsening/article/v164/reconstruction.pdf); [independent complete LaTeX](papers/A2-v17-boundary-information-coarsening/article/v164/reconstruction.tex).

**Paper II: Power ideals and the Hilbert boundary of quadratic pencils** — 89 pages. [PDF](papers/A2-v17-boundary-information-coarsening/article/v164/divisor-geometry.pdf); [independent complete LaTeX](papers/A2-v17-boundary-information-coarsening/article/v164/divisor-geometry.tex).

**Complete preservation master, not a third submission** — 155 pages. [PDF](papers/A2-v17-boundary-information-coarsening/article/v164/geometry.pdf); [independent complete LaTeX](papers/A2-v17-boundary-information-coarsening/article/v164/geometry.tex).

## Main revision

The collision family separates the full pullback of the normalized total
Hilbert graph from the schematic closure of its generic fibres. The
horizontal space is a smooth quotient of the blow-up of the ordered
direction product along its central diagonal. Its special divisor is
`F_2 + 2 P^2`; the full pullback has an additional vertical `P^4`, attached
along the singular-conic plane. Its exact base-torsion is that plane's
ideal sheaf inside `P^4`. Ordering the roots and normalizing gives the
reduced normal-crossing model. This is a degeneration of parameter spaces,
not a replacement of nonreduced Hilbert curves by stable maps.

The nilradical of the complete first-contact fibre is identified globally
as `j_* O_(P^2)(-1)`, with square zero; no splitting of the algebra extension
is asserted. Independent collisions have explicit component multiplicities.
An explicit 4-by-4 symmetric pencil realizes the collision in a fixed
complete-quadric target. Its application to failure algebras remains through
the effective inverse, not the unrestricted raw Artin-algebra stack.

[All 44 current referee responses](papers/A2-v17-boundary-information-coarsening/article/v164/RESPONSE_TO_V162_REPORT.md).
[Archived v163 response](papers/A2-v17-boundary-information-coarsening/article/v164/PREVIOUS_RESPONSE_V163.md).
[Theorem/page index](papers/A2-v17-boundary-information-coarsening/article/v164/THEOREM_INDEX_V164.json).
[Build receipt](papers/A2-v17-boundary-information-coarsening/article/v164/BUILD_RECEIPT_V164.json).
[Preservation audit](papers/A2-v17-boundary-information-coarsening/article/v164/NONDELETION_V164.json).
[Exact finite audits](papers/A2-v17-boundary-information-coarsening/article/v164/EXACT_CHECKS_V164.json).
[Primary-source comparison](papers/A2-v17-boundary-information-coarsening/article/v164/LITERATURE_AUDIT_V164.md).

All 520 predecessor labels and 348
mathematical environment blocks are retained. The current master has
539 labels and 358 blocks. Preservation
is checked byte for byte for mathematical blocks; the body is partitioned
exactly once across the companions. Replaced front matter and the old root
entry are archived. Each complete source embeds stable companion references.

The authored source commit above precedes the separate materialization
commit with complete PDFs, sources and receipts. The latter is recorded
in `papers/A2-v17-boundary-information-coarsening/article/v164/PUBLICATION_SEAL_V164.json` only after actual remote read-back.
No file asserts its own future commit hash. The workflow renders pages
for inspection but rendering alone is not recorded as visual inspection.

## Reproduce

From a full checkout of this branch, run:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v164/check_v164.py
python3 papers/A2-v17-boundary-information-coarsening/article/v164/assemble_v164.py --build
```

The three complete `.tex` files also compile individually without external
companion auxiliary files. The scripts require the preserved historical
inputs in the repository; the independently compiling sources do not.

The remote build actually runs the inherited v163 chain. Finite audits do
not certify general proofs, novelty or journal acceptance. No new external
independent audit of Paper I has been obtained. The Ballico 1993 full-text
comparison remains incomplete and is disclosed inside both papers. The
higher-contact and higher-corank full Hilbert classification is not claimed
complete; the original all-pencil inverse and singular-pencil invariants
retain their domains.
