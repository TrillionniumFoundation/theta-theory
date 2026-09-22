# A2 revision 116 — primary structure and residual geometry

**Primary structure and residual geometry of multiplication failure schemes**  
Qian Qi · September 22, 2026

Revision branch: `revision/a2-v116-higher-product-structure-2026-09-22`.
Controlling report: `reviews/a2-v115-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md`, frozen at `1cb4e00c86699247454d21dbec2dcce01a9c6b8b`.
Reviewed v115 head: `acfd3d57e0053e1b03df53020fd8e79e14599c03`.

## Reading copies

- `geometry.pdf` / `geometry.tex`: the journal-facing algebraic-geometry article (47 pages in the verified build).
- `paper.pdf` / `paper.tex`: the complete archival article, including every retained information-recovery and statistical appendix (72 pages).
- `applications.pdf` / `applications.tex`: the separate application reading copy (27 pages). Its references to the geometry are exported from the complete article.

The manuscript is not a replacement abstract or a plan. It contains two new global ideal-identification proofs, a general cokernel reduction, exact infinitesimal descriptions, and expanded proofs of the v115 hyperplane theorem. The original v115 manuscript and report remain unchanged in their original paths and Git history.

## New mathematical center

Put `T_m=m(m+1)/2`. For hyperplanes in the complete **quartic** binary series, in every symmetric degree `m>=2`, Theorem 11.1 (`thm:quartic-primary`) proves the actual ideal-sheaf identities

`J_m = I_{S_4} I_{C_4}^{T_m-2} = I_{S_4} intersect I_{C_4}^{T_m}`.

This is a complete primary decomposition, not just a support statement. The transverse completed equation is `(AC-B^2)(A,B,C)^{T_m-2}`. The nilpotency index is exactly `ceil(m(m+1)/4)`. Corollary 11.5 determines every infinitesimal layer and the normal cone. A row-filtration argument also proves exact order `T_m` along the evaluation curve for **every binary degree n>=4**, and strengthens the old linear nilpotency lower bound to the same quadratic lower bound. The ideal equality itself is asserted for `n=4`, not for arbitrary `n`.

Theorem 12.1 (`thm:conductor-reduction`) identifies the actual multiplication cokernel, and hence every Fitting ideal, with multiplication in a finite contact algebra for divisor-conditioned subseries with `n>=2 deg(Z)-1`. For two-dimensional residues and arbitrary multiplicities `Z=sum e_i p_i`, Theorem 12.2 (`thm:contact-pencil-primary`) gives the complete primary decomposition, every corank and the degree wall. Above `m=deg(Z)-1`, the equation on a smooth frame chart is

`product c_{i1}^{binom(e_i,2)} * product_{i<j}(lambda_j-lambda_i)^{e_i e_j}`.

These are non-hyperplane Grassmannian families of subseries of unbounded codimension `deg(Z)-2`. Their complete local singularities and nilradical layers are in Corollary 12.4. The theorem concerns these explicitly defined families, not the entire ambient Grassmannian of all subseries.

## Referee response and scholarly checks

`RESPONSE_TO_R115.md` maps each objection to a theorem, proof expansion or precisely delimited remaining issue. `PROOF_AUDIT.md` gives the new proof dependencies. `LITERATURE_AUDIT.md` identifies the primary sources actually inspected. The full theorem-by-theorem comparison with Ballico (1993) is **not represented as completed**: the publisher's first page was inspected, but the remaining theorem pages were not obtained. No priority claim is deduced from the paper's title or first-page definitions.

`PRESERVATION_AND_DEPENDENCIES.md` records the no-deletion checks. The active v115 sources are also frozen under `history/v115_source/`; their original SHA-256 digests are in `evidence/V115_SOURCE_MANIFEST.json`.

## Rebuild and evidence

Run `bash build.sh` from this directory or from the repository root using its full path. Requirements: Python 3, SymPy, TeX Live with AMS/Latin Modern packages, and Poppler (`pdfinfo`). The script first runs both diagnostic suites, then compiles all three reading copies and writes source-bound receipts.

`python3 verify_v116.py --source-only --git-baseline` checks the source archive against the frozen review Git object; a full checkout containing that object is needed. The ordinary `verify_v116.py` also runs exact algebra and original-multiplication diagnostics. Optional `--extended` adds the substantially slower quartic `m=4` full-minor comparison.

Read `evidence/SOURCE_RECEIPT.json` for the **mathematical source commit** and source hashes. Read `evidence/BUILD_RECEIPT.json` for PDF hashes, page counts, final-log checks and diagnostic hashes. The generated-evidence commit is necessarily later than the source commit; the receipt does not pretend otherwise. `evidence/GIT_BASELINE_CHECK.json` records the remote frozen-object check.

Source checks preserve **158 old theorem/proof blocks verbatim, 201 labels and 27 bibliography keys**; 17 active TeX files are byte-identical to v115. The new suite includes exact quartic minor-ideal checks in degrees 2 and 3, 6 symbolic confluent determinant identities, 27 direct polynomial-multiplication rank cases, and the finite combinatorial checks accompanying the uniform induction. The inherited suite includes 80 hyperplane rank/polar cases and the earlier diagnostics. These computations are reproducible checks, **not a proof-assistant certificate or an editorial assessment**. The universal results rest on the written proofs.
