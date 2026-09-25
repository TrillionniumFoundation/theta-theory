# A2 revision 158 — complete referee reading entry

Branch: `revision/a2-v158-intrinsic-boundary-singular-pencils-2026-09-25`.

Controlling report: `review/a2-v157-independent-harsh-top4-2026-09-25`, commit `b81ba4a2fac700f17b26163079bd17ef54947509`. Mathematical predecessor: the complete v157 package at `a6d34cd2bb2075c64015f3667dbf3f391665cefd`, whose source commit was `b1cde8e304c0572bdb436d8484f1c9b70333fd77`.

## The two submitted reading objects

| Paper | Complete PDF | Independently compiling source |
|---|---|---|
| I. Finite failure schemes and the reconstruction of quadratic pencils | [reconstruction.pdf](reconstruction.pdf) | [reconstruction.tex](reconstruction.tex) |
| II. Intrinsic power geometry and singular quadratic pencils | [divisor-geometry.pdf](divisor-geometry.pdf) | [divisor-geometry.tex](divisor-geometry.tex) |

The [unified preservation master](geometry.pdf), with [source](geometry.tex), is for full-content comparison and is not a third submission. Each focused source embeds its companion numbering; an external `.aux` file is not needed. The [native build receipt](BUILD_RECEIPT_V158.json) gives the actual source commit, page counts and source/PDF hashes. The repository root `CURRENT_REVIEW_ENTRY.md` is the controlling entry and distinguishes source from output materialization.

## Principal new results

Paper I, Theorem 10.1, constructs the source-normalized apolar algebra bundle and its projective power diagram from the first relation before recovering the pencil coefficient line. Scalar twists cancel under `PGL(V)` descent. The construction does not select an `n`-plane inside the auxiliary `n^2-1` dimensional reciprocal-fibre complement, and it is not a claimed preferred subquotient of the original algebra.

Paper II, Theorem 6.1, identifies the exact power graph at every normal rank with relative complete quadrics over the image-plane Grassmannian; the highest nonzero power recovers the image plane. Theorem 7.2 recovers both elementary divisors and minimal indices of arbitrary symmetric pencils and proves their contact/image-degree conservation law. Theorem 10.2 computes a transverse corank-two Hilbert limit in every dimension at least three: a reduced nodal main curve and one exceptional tail, selected by a single power ideal, with all its power maps determined.

The coefficient-map conventions, simultaneous graph lemma and precise classical-source comparisons are in Section 2 of Paper II. The sharp inverse remains unchanged, including singular pencils. Core logical dependencies and the roles of the appendices are stated separately in both introductions.

## Response, preservation and exact checks

The [point-by-point response](RESPONSE_TO_V157_REPORT.md) answers all 24 specific requests and the main intrinsic-boundary objection. The [literature comparison](LITERATURE_AUDIT_V158.md) identifies exactly which primary-source statements were checked and which historical access limitation remains.

[NONDELETION_V158.json](NONDELETION_V158.json) and [PAPER_MAP_V158.json](PAPER_MAP_V158.json) record preservation and allocation of the 352 predecessor labels and all 236 predecessor mathematical environment blocks. Replaced front matter is archived in `PREVIOUS_FRONTMATTER_V157.tex`. No prior revision/review branch is overwritten.

[EXACT_CHECKS_V158.json](EXACT_CHECKS_V158.json) records rational Toeplitz-nullity tests, image-plane Pluecker calculations, power-ideal Groebner comparisons and complete tail coefficient-space tests. [INHERITED_V157_CHECKS_RERUN.json](INHERITED_V157_CHECKS_RERUN.json) records the actual rerun of v157 and the suites it invokes. The separate historical 28-check suite is not claimed as rerun. Finite checks are not certificates of the general proofs.

## Reproduction

In this directory of the checked-out branch, using Python 3 with SymPy 1.14.0, TeX Live and Poppler:

```sh
python3 check_v158.py
python3 assemble_v158.py --build
```

The assembler pins the complete predecessor by SHA-256, produces all three full manuscripts, preserves the old mathematical blocks, stabilizes companion references and rejects missing citations/references, duplicate labels and horizontal overflows. The branch-specific workflow checks the input hashes, reruns the exact suites, compiles and publishes only this revision directory and its root reading entry, without force-pushing.

## Precise scope

The intrinsic object is an algebra bundle on the recovered source projective space and a canonical projective power diagram, not an untwisted linear algebra canonically based at a point. Complete quadrics and the complex Kronecker congruence form are credited as classical inputs. The computed Hilbert fibre is the stated corank-two family, not a classification of all fibres or a proper quotient-stack compactification. The Ballico 1993 theorem/proof comparison remains documentary-limited in both PDFs. No historical nonanticipation, general proof certification or editorial acceptance is asserted from missing documents or finite computations.
