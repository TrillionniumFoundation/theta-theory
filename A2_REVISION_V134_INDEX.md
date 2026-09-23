# A2 revision 134 — global reconstruction by Schur support

**Branch:** `revision/a2-v134-global-schur-support-reconstruction-2026-09-23`  
**Immutable controlling review:** `a75f534c6694513ae6c493166d1cba1ea56a98fd`  
**Reviewed v133 publication:** `bbbb697e852d1ca93b88eb7d3bfe6fbd15f396a7`.

## Referee entry points

The complete new article is in `papers/A2-v17-boundary-information-coarsening/article/v134/`:

- [Complete manuscript PDF](papers/A2-v17-boundary-information-coarsening/article/v134/geometry.pdf).
- [Complete LaTeX source](papers/A2-v17-boundary-information-coarsening/article/v134/geometry.tex).
- [Response to the v133 report](papers/A2-v17-boundary-information-coarsening/article/v134/RESPONSE_TO_REFEREE_V133.md).
- [Issue matrix](papers/A2-v17-boundary-information-coarsening/article/v134/ISSUE_MATRIX.json).
- [Executed source-bound receipt](papers/A2-v17-boundary-information-coarsening/article/v134/evidence/BUILD_RECEIPT.json).
- [Literature audit](papers/A2-v17-boundary-information-coarsening/article/v134/LITERATURE_AUDIT_V134.md).

## Mathematical advance

The reconstruction open is the entire smooth basepoint-free Jacobian locus:
`G_4^rec = G_4^circ`. Thus an isomorphism of abstract full nonreduced
multiplication-failure schemes reconstructs the relation web up to one
projective transformation on that whole locus, not just a further generic open.

The new contraction-kernel lemma and exterior-support theorem prove that a
Schur component with at least three essential Jacobian variables cannot belong
to a secant or tangent space of decomposable four-vectors. All rank-one and
rank-zero component-fibre types are therefore absent from the smooth locus.
The ambient rank strata are globalized; the double-point locus is identified
with the ramification scheme on the quasi-finite part, with endpoint deletion
kept separate from closed pencil-intersection length.

Principal new labels: `lem:schur-contraction-kernel`,
`prop:exact-schur-support`, `lem:secant-tangent-support`,
`thm:global-schur-recombination`, `prop:global-pencil-rank-strata`, and
`cor:exceptional-binary-jacobian`. The accepted universal Schur readout and
common-projective-transformation proof files are unchanged byte-for-byte.

## Preservation, reproduction and limits

All 30 inherited compiled inputs and 219 mathematical labels are retained;
24 inherited LaTeX files are byte-identical. The main narrative is the inverse
theorem. The complete primary-boundary machinery and explicit certificates
remain in substantial appendices, rather than being deleted or presented as
a complete higher-corank W3/W4 primary atlas.

Run `python revisions/a2-v134/assemble.py` and then
`bash papers/A2-v17-boundary-information-coarsening/article/v134/build.sh`.
The branch-restricted workflow independently reruns all nine exact scripts,
three LaTeX passes and 30 mechanical checks before publishing the expanded
article and receipt. Consult the receipt for actual execution and source hashes;
finite coordinate checks do not constitute formal verification of the written
structural proofs. No main/review/other-paper branch is updated.

**M133.1 remains documentary-open:** Ballico 1993 was not obtained at full-text
theorem level. No priority clearance or journal acceptance is claimed. The
controlling report is an owner-requested AI-assisted referee-style report, not
a journal-issued decision.
