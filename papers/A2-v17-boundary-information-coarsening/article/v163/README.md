# A2 revision 163 — controlling review entry

Branch: `revision/a2-v163-embedded-comparison-contact-fibres-2026-09-25`.
Authored source commit: `ac347307add8b5a620beea2464bbf0c1f29ae1b8`.
Controlling v162 report: `7e9c057907cc4502858a54f32ab0c0cfa264680f`.
Complete reviewed baseline: `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`.

## Complete reading objects

**Paper I: Finite failure schemes and the reconstruction of quadratic pencils** — 72 pages. [PDF](reconstruction.pdf); [independent complete LaTeX](reconstruction.tex).

**Paper II: Power ideals and the Hilbert boundary of quadratic pencils** — 85 pages. [PDF](divisor-geometry.pdf); [independent complete LaTeX](divisor-geometry.tex).

**Complete preservation master, not a third submission** — 149 pages. [PDF](geometry.pdf); [independent complete LaTeX](geometry.tex).

## Main revision

The fixed-target comparison is stated separately as an equivalence of
completed embedded quotient functors, retaining the coefficient base and
undoing parameter-dependent congruences. A Hilbert–Burch chart with a
regular inverse identifies the whole first nonreduced fibre: its reduced
components are P^4 and F_2, meeting along the doubled-line P^1. The exact
local ideal `(eA,eB,e^2C)` also records a nonzero square-zero nilradical.
The proof exhausts the proper fibre by connectedness; it is not another
selected family of limits.

For r distinct length-two contacts and s length-one contacts, with
arbitrary larger Smith exponents and no higher corank, the complete
actual pencil fibre is `X_2^r x (P^1)^s`. All `2^r` reduced components,
their dimensions and intersections, and the exact nilpotence order `r+1`
are determined. Higher lengths have a separately labelled conjecture,
not an asserted full classification. The failure-family application is
explicitly through the effective inverse, not the raw Artin-algebra stack.

[All 44 responses](RESPONSE_TO_V162_REPORT.md).
[Theorem/page index](THEOREM_INDEX_V163.json).
[Build receipt](BUILD_RECEIPT_V163.json).
[Preservation](NONDELETION_V163.json).
[Exact audits](EXACT_CHECKS_V163.json).
[Primary-source record](LITERATURE_AUDIT_V163.md).

All 490 predecessor labels and 325 mathematical environment blocks are
retained; the current master has 520 labels and 348 blocks. Preservation
of the predecessor mathematical blocks is checked byte for byte and the
body is allocated exactly once between the two companions. Replaced
front matter and the old root entry are archived. The sources embed
stable companion references; no external companion auxiliary file is needed.

The authored source commit precedes the separate materialization commit
containing complete sources, PDFs and receipts. Remote read-back is bound
to that output commit in `papers/A2-v17-boundary-information-coarsening/article/v163/PUBLICATION_SEAL_V163.json` after verification.
No file claims to know its own future commit hash.

The full inherited v162 check chain was executed by this build. Tests
are exact finite audits, not certificates of general proofs, novelty or
editorial acceptance. No new external independent proof audit of Paper I
has been obtained. Ballico 1993 remains unavailable at theorem/proof level;
this limitation is retained in both papers. The original all-pencil
sharp inverse and singular-pencil invariant results have not been restricted.
