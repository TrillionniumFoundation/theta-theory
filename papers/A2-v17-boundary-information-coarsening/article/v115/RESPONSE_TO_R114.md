# Response to the independent report on A2 revision 114

Controlling report: `reviews/a2-v114-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md`, commit `09869129e16fd43bd2420fa3573a09cd5cbbdff9`, report blob `4d1c5c929f175bc2c4c64451eb37a35b4c785b2a`.

Reviewed v114 source: `d58d4ad0546487f4313cf8ed2f05ad9321b54e63`.

Revision 115 retains all previous mathematical results and complete proofs. It does not answer R114 by repeating that the proof-completeness issues from R113 have been fixed: the report already recognizes those repairs. The principal new result is a global theorem for a natural higher-product family, including an embedded associated curve. The new exact residual-germ section states explicitly which constructions are classical.

## 1. Sections 3, 7 and 13B: the general theory must produce geometry beyond quadratic multiplication

**Change:** a new full section, `parts/02j-higher-hyperplane-classification.tex`, headed “A global higher-product family with embedded structure.”

For every n >= 4, let U run through all hyperplanes of H^0(P^1,O(n)), and let m >= 2. Theorem `thm:higher-hyperplane-global` determines the entire reduced failure locus of Sym^m U -> H^0(P^1,O(mn)), not merely a two-point incidence family. It is the secant threefold S_n of the evaluation rational normal curve C_n. The coranks are exactly 0 off S_n, 1 on S_n minus C_n (including tangent secants), and m on C_n.

The proof excludes every additional reduced component: quadratic surjectivity propagates in degree by a base-point-free pencil argument, while the quadratic failure hyperplanes are characterized by rank-at-most-two Hankel annihilators. Explicit split and tangent calculations give the remaining coranks. The polar derivative computation proves that the scheme is regular at every point outside C_n, not just at a general distinct-support point.

This is a natural complete linear-system/subseries family in every symmetric degree. It is not the artificially chosen beta realization example of the exact-germ section, and it is not claimed to classify every higher-product contact configuration.

## 2. Sections 6 and 13C: control the embedded structure in an excess family

**Change:** the same theorem gives, for every m >= 3,

    Ass(O_{D_m}) = {eta_{S_n}, eta_{C_n}}.

There is one reduced irreducible component and precisely one embedded associated subvariety, the evaluation curve. Further,

    J_m : I_{C_n}^infinity = I_{S_n},

and the nilradical N_m has N_m^j nonzero at every evaluation point whenever 2j < m. Thus the local nilpotency index is at least ceil(m/2), while the reduced support stays fixed.

The associated-point argument is global. Smoothness away from C_n confines the possible embedded support; the order-m maximal minors at an evaluation, compared with an order-two secant equation, produce a nonzero nilradical there. Equivariance and transitivity on C_n exclude additional closed associated points. The generic point of the nonzero coherent nilradical is then an associated point of the complete scheme.

This directly addresses the request for an excess-scheme theorem with associated-prime content. It does not purport to determine the embedded primary ideal itself or to settle every smaller component of the earlier all-c, all-L quadratic excess scheme. Those general questions are not marked closed in the status table below.

## 3. Sections 4, 5 and 13A: exact germs, not only Fitting strata; identify the classical input

**Change:** new Section `sec:intrinsic-residual-germs`, with four levels kept distinct.

The joint polar relation proposition identifies the dual intrinsic normal derivative on the entire annihilator space:

    partial*: K_U tensor C_U* -> T_U*X,
    sum q_i tensor ell_i -> sum B_{ell_i}*(q_i).

A relation involving several annihilators need not arise from a kernel for one fixed annihilator. The symmetric 2-by-2 example records this distinction explicitly.

Theorem `thm:residual-matrix-germ` gives exact convergent and completed equations at every corank, without an expected-codimension assumption:

    completed O_{D,U} = C[[y,x]] / I_rho(L(y) + Psi(y,x)),

with Psi in the complementary normal space and no constant or linear terms. The full nonlinear term is retained. Nested rank ideals are identified in the same chart. This is an exact presentation, not a claim that every germ is a smaller multiplication scheme of the original type.

The transverse corollary gives a generic determinantal model under a checkable surjectivity condition. The corank-one theorem reduces to a minimal presentation with delta = dim ker tau equations; in expected codimension these form a regular sequence. The written quadratic obstruction pairs with the polar kernel. A cubic cusp example demonstrates why quadratic or Fitting data cannot replace higher-order equations.

**Priority correction:** intrinsic normal derivatives, Schur elimination, rank-stratum products, and transverse determinantal models are classical. The article now compares them explicitly with Frühbis-Krüger–Zach, Lemma 1.3, Remark 1.18, Section 1.3.2 (13), and Definition 2.11/Proposition 2.12; Fitting presentation independence and base change are compared with Stacks Tags 07Z8 and 07ZA. They are not presented as the newly discovered contribution. The specific polar identifications and the new hyperplane associated-point theorem are distinguished from these inputs.

The Ballico 1993 full theorem comparison remains unverified. No nonoverlap or originality claim is inferred from an unavailable theorem text. This limitation is stated in the article itself, not only in this response.

## 4. Sections 2, 8 and 12: retain the repairs the referee already credits

The relative orientation descent, exceptional orientation incidences, relative residual divisor, normal derivative factorization, simultaneous nonempty wall open, higher-product algebraic dihedral descent, and fixed rank-two fibre primary decomposition are retained. Their statements and proofs have not been dropped to improve the response superficially.

A new standalone simple-normal-determinant lemma supplies a reusable proof of the local equation uv = 0 from a smooth contained branch and a simple normal determinant. It makes no prior reducedness assumption, and computes the local normalization and conductor. This addition supports the existing wall proof; we do not misrepresent the generic node as a still-unanswered R114 proof gap.

## 5. Sections 10 and 13D: a focused article without deleting the application program

The package includes a geometry-only reading copy, `geometry.pdf`, and a companion `applications.pdf`. Both are compiled from the same section sources as `paper.pdf`, the complete archival revision. The applications retain their full proofs and appendix numbering. Cross-references between the two reading copies are generated from the full manuscript's labels and do not redefine the other part's labels.

Thus the journal-facing geometric sequence is readable without the long statistical apparatus, while the full contact, native realization, Poisson/Gaussian, finite-precision, finite-offset and estimation work remains available without abridgement. The main geometric proofs do not acquire new dependencies on those appendices.

## 6. Sections 1, 11 and 13E: build and provenance

The exact v114 workflow was checked. It failed before compilation with a missing baseline dictionary entry caused by a nested-directory `git ls-tree` pathspec. Revision 115 uses explicit repository-root object paths and checks nonempty baseline retrieval. A temporary-repository regression reproduces the old failure and verifies the corrected behavior without depending on GitHub.

The delivery contains actual compiled PDFs, final logs, source hashes, finite-diagnostic receipts, and a build receipt. Mathematical source and generated evidence are separate local commits. The receipts distinguish the upstream review/source objects from the local patch-generation commits, and state that the revision has not been pushed remotely. The source-only intermediate commit is not described as a completed PDF delivery.

## 7. Current closure ledger

| Referee issue | Revision 115 action | Status |
|---|---|---|
| Concrete geometry in degree m >= 3 | Global hyperplane failure/corank theorem, including tangent and evaluation strata | Proved in the revision; requires independent review |
| Excess associated structure | Complete associated-point set and saturation in that family; unbounded nilpotency lower bound | Proved in the revision; not an all-c, all-L classification |
| Exact germs beyond Fitting restrictions | Joint polar normal derivative and exact nonlinear residual matrix presentations | Explicit statements and proofs supplied |
| Classical determinantal novelty boundary | Exact prior-result comparison and attribution in the article | Substantially expanded; not an exhaustive priority certification |
| Ballico 1993 theorem comparison | Bibliographic/source-access audit retained; no unsupported novelty claim | Unresolved full-text comparison |
| All general quadratic excess components/primary ideals | Earlier maximal-component theorem preserved; new family-specific global scheme theorem added | General classification remains unproved |
| Geometry versus statistics architecture | Geometry reading copy plus full companion, no proof deletion | Implemented |
| Build/source mismatch | Actual PDFs, root-independent verification, source-bound receipts | Implemented locally |
| Remote revision branch | Additions-only patch targeting the R114 review commit | Not published remotely in this session |

Finite tests check bounded examples and exact symbolic identities. They are not proofs of the universal theorem statements or substitutes for referee review.
