# A2 revision 151 — referee reading guide

**Principal article:** `geometry.tex` / `geometry.pdf`, *Finite failure schemes and the reconstruction of quadratic pencils*, Qian Qi, September 24, 2026.

This revision addresses the complete independent report on v149 at review tip `ddcef32b3cf491aacb293e466c393ec4af3caecd`, report blob `2878e4dd16cf49e631b933b8c34bafdc896eed8f`. The report is owner-requested, not a journal editorial decision. The v149 mathematical source was published at `4af97058186974234e2669677818956781a67a08`. A separately existing v150 branch was at the same review tip when inspected; this revision does not overwrite that branch or claim its work.

## Principal additions

The principal article retains all v149 mathematical blocks and adds three integrated sections:

1. **Canonical common-divisor boundary.** Proposition `prop:incidence-v151`, Lemma `lem:fibre-equations-v151`, and Theorem `thm:boundary-normalization-v151` prove representability of the divisor incidence over arbitrary bases, finite normalization of its scheme-theoretic image, full local equations of the normalization fibres, and the exact normal/smooth-locus criterion. Examples separate a length-three nonreduced fibre, two reduced normalization lifts, and a normal point with a higher gcd degree. Corollary `cor:algebra-boundary-v151` supplies the natural first-relation algebra boundary without imposing pencil image equations.
2. **Canonical rigidification.** Theorem `thm:rigidification-v151` and Corollary `cor:two-rigidifications-v151` prove the universal properties of the nonlinear and right-factor inertia quotients, including their twisted subgroup stacks and all 2-isomorphisms.
3. **Explicit all-pencil specialization.** Theorem `thm:closed-pencil-v151` constructs a uniform one-parameter degeneration to the flag orbit, proves that it is the unique closed pencil orbit, and Corollary `cor:closed-failure-v151` gives the actual finite-flat failure-algebra family.

The new boundary is the locus of a **degree-prescribed divisor**, not the potentially different condition “gcd degree at least g.” Arbitrary base-change statements concern incidence and its pulled-back fibres, not a false claim that normalization or scheme-theoretic image always commutes with nonflat base change.

## Reading and verification

Start with the introduction, then the new boundary section following the inherited common-divisor stratum, then the two new sections following the pencil stack theorem. All old all-pencil inverse proofs, moving-family descent, exact determinant multiplicity, transverse families, and spectral statements remain in the principal article. The main article has no external-document proof dependency.

`RESPONSE_TO_V149_REPORT.md` gives the point-by-point response. `ISSUE_MATRIX_V151.json` separates mathematical changes supplied for re-review from the unresolved documentary comparison. `PROOF_SCOPE_AUDIT_V151.md` records proof dependencies and what the results do not claim.

Build with `python revision_v151.py assemble` followed by `python revision_v151.py build` from a checkout containing the pinned v149 directory. Dependencies are Python 3, SymPy 1.14.0, NumPy 2.3.5, pdflatex with the AMS/Latin Modern/geometry/microtype packages, and Poppler's pdfinfo. The script runs the 26 inherited scripts and the new exact-witness script, builds the three PDFs, verifies references/layout and source retention, and writes source-bound evidence. `evidence/BUILD_RECEIPT_V151.json` is the sole completed-build claim; successful finite checks do not certify all mathematical proofs.

`applications.tex` and `archive-v144.tex` are separate companions with unchanged mathematical drivers. The archive remains non-submitted; its older front matter is historical, not the v151 submission front matter. No result is deleted merely to shorten the new principal article. Original source bytes are recorded in `INHERITED_SOURCE_V151.json` and `NONDELETION_V151.json`.

## Documentary status

The complete theorem/proof text of Ballico (1993), DOI `10.1002/mana.19931630102`, was not obtained. No claim of anticipation, nonanticipation, priority clearance, or satisfaction of a top-four journal's significance standard follows from this revision. The all-pencil theorem is unchanged; bibliographic uncertainty is kept separate from its mathematical statement. See `LITERATURE_AUDIT_V151.md` for inspected sources and the six comparison axes.
