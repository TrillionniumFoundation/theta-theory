# A2 revision 157 — complete referee reading entry

Branch: `revision/a2-v157-universal-power-ideals-2026-09-25`.

This revision responds to the complete-materialized v153 report at `52ebb8183433ad398f61958219b2af809f721824`. Its mathematical source is the complete v155 manuscript at `54b3a37bb8349fbba089dd0b7cdaa2ba0aa74414`. The new branch preserves all existing revision and review branches, including the undecodable v156 source package; that package is not a mathematical input.

## Read the complete papers

| Review object | Complete PDF | Independently compiling source | Local pages |
|---|---|---|---:|
| I. Finite failure schemes and the reconstruction of quadratic pencils | [reconstruction.pdf](reconstruction.pdf) | [reconstruction.tex](reconstruction.tex) | 60 |
| II. Reciprocal power ideals, complete quadrics, and pencil degenerations | [divisor-geometry.pdf](divisor-geometry.pdf) | [divisor-geometry.tex](divisor-geometry.tex) | 43 |
| Complete paired preservation master | [geometry.pdf](geometry.pdf) | [geometry.tex](geometry.tex) | 98 |

The native [build receipt](BUILD_RECEIPT_V157.json) records actual remote source/PDF hashes and page counts. These links refer to complete standalone objects, not source-lock notes or encoded fragments. Cross-paper numbering is embedded in each source; an external companion `.aux` file is not required.

The [point-by-point response](RESPONSE_TO_V153_REPORT.md) addresses all 24 specific requests and the report's global boundary objection. The two focused papers are the reading submissions; the full master is retained for complete-content comparison.

## Main new results in Paper II

Section 3 proves the universal formula `J_(hq+s)(A)=I_q(A)^(h-s) I_(q+1)(A)^s` over every commutative complex algebra, including nonreduced bases. Section 4 identifies the entire simultaneous power graph, as a scheme, with complete quadrics independently of h and gives its exact boundary principalization. Section 5 recovers regular-pencil Segre data from boundary contact divisors. Section 6 gives a normal projective incidence compactification carrying flat resolved-pencil curves and the original finite failure algebra. Section 7 records all universal power-zero multiplier ideals and thresholds as consequences of the classical rank-locus resolution.

Classical determinantal balancing, determinant-apolar representation theory and the geometry of complete quadrics are explicitly credited. The new assertions concern their exact realization by reciprocal normalization-fibre multiplication and its native pencil geometry. The full cotangent-coordinate common collapse is not confused with this native boundary.

## Preservation and checks

[NONDELETION_V157.json](NONDELETION_V157.json) verifies preservation of all 322 predecessor labels and all 219 predecessor mathematical environment blocks. The master has 352 labels and 236 mathematical blocks. Every body block is allocated exactly once across the companions; [PAPER_MAP_V157.json](PAPER_MAP_V157.json) gives the allocation. Replaced frontmatter is archived in `PREVIOUS_FRONTMATTER_V155.tex`.

[EXACT_CHECKS_V157.json](EXACT_CHECKS_V157.json) records 34 exact rational coefficient-space comparisons, 40 boundary/graph parameter pairs, 375 spectral contact profiles and a nonreduced-base example. The v155 suite, including its inherited checks, is executed again; its current receipt is [INHERITED_V155_CHECKS_RERUN.json](INHERITED_V155_CHECKS_RERUN.json). The distinct historical 28-check suite is not claimed as rerun. Finite checks are not certificates of the general proofs.

## Reproduce

From this directory in the checked-out branch, using Python 3 with SymPy 1.14.0, TeX Live and Poppler:

```sh
python3 check_v157.py
python3 assemble_v157.py --build
```

The assembler pins the v155 manuscript by SHA-256, preserves its proof blocks and labels, creates all three complete sources, compiles the PDFs, stabilizes companion references, and rejects undefined citations/references, duplicated labels and horizontal formula overflows. The branch-specific GitHub workflow runs the same build and publishes the complete outputs to this branch only, without force-pushing.

## Scope for the next referee

The universal ideal, complete-quadric graph and contact-divisor statements are the new general theorems to scrutinize. A contact arc retains more than its limiting boundary point. The projective incidence compactification is not a proper quotient stack, and no classification of all its limiting Hilbert fibres is asserted. Whole reciprocal fibres are not identified with their quadratic Gorenstein sections. The theorem-level Ballico 1993 comparison remains documentary-limited; the article does not infer nonanticipation from unavailable text. No editorial acceptance or formal proof certification is asserted.
