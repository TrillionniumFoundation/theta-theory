# Response to the independent report on A2 revision 134

**Revision 135 — Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes**  
Qian Qi · 23 September 2026

Controlling report: `reviews/a2-v134-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, immutable commit `a08b157800c27c0f73f0c5c9a52155265ef4f395`. Reviewed published manuscript: `74b1aa9ffb95557f63e993e428a22e491a1edd0f`. The report is owner-requested and AI-assisted, not a decision issued by a journal.

The theorem retains its full scope: **every basepoint-free web with smooth Jacobian** is reconstructed, up to one projective transformation, from the abstract full nonreduced multiplication-failure scheme. No additional generic open or weaker substitute theorem is introduced. The article and its complete technical supplement are separate reading objects. The response below describes written repairs, not referee acceptance or formal machine verification.

## Report §2.1: singular contraction kernels

New Lemma `lem:shear-descent` is stated for arbitrary degree and an arbitrary invariant subspace of `det(V) ⊗ Sym^m(A ⊕ B)`. It specifies the actual torus weights `dim(B)+m-k`. Projection to A-degree k is therefore legitimate before differentiation. For a nonzero coefficient `f_beta`, choose `alpha=beta-e_i`; the coefficient of `a_i` in `partial^alpha F` is exactly `beta! f_beta`, and no other monomial contributes. This explicitly excludes cancellation.

All infinitesimal rank-one shears may use any fixed nonzero `b ∈ B`. Their product is `b^(k-1) partial^alpha`; polynomial-domain injectivity gives a nonzero vector of exact degree one in A. Thus its weight-graded image also stays nonzero. The determinant factor contributes `dim(B)` to the torus weight but is trivial under the unipotent shears. This addresses both the filtration and determinant-twist objections.

The proof of `lem:schur-contraction-kernel` applies the lemma to singular ranks 1, 2 and 3. It explains irreducibility for the full O(A) factor also in dimensions one and two: the O₂ reflection exchanges the two SO₂ weight lines. Nonvanishing on the degree-one summand follows from the explicit identity `4 kappa_q(epsilon ⊗ a b^3)=(b x_2)∧(b x_3)∧b²`. The exact kernel theorem is unchanged.

## Report §2.2: the nondegenerate character calculation

New Lemma `lem:orthogonal-exterior-cube` gives the full restriction of `Λ³ Sym² V` to `SL₂ × SL₂ → SO₄`. With `[a,b]=Sym^a U ⊗ Sym^b U'`, it is

`[6,0] + [0,6] + [4,4] + 2[4,2] + 2[2,4] + [2,2] + 2[2,0] + 2[0,2]`.

The proof derives both degree-two and degree-three skew Cauchy formulas and every required one-factor character, including the `(2,1)` Schur functor. Dimensions total 120; there is no trivial SO₄ summand. The O₄ determinant character restricts trivially to SO₄, so it cannot occur. No choice of O₄ extensions of nontrivial summands is needed.

Consequently the line `det(V) ⊗ C(q^{-1})²` is killed. The harmonic source decomposition now displays the determinant twist on all summands. The coefficients 2 and 2/3 on the other two summands are retained and derived term by term; nonisomorphism prevents their images from cancelling. The older coordinate-reflection argument remains in the supplement as an alternative, not the load-bearing proof.

## S134.1: primary literature and a sharper geometric statement

Section `sec:support-literature` distinguishes classical tools from the specialized calculation. The comparisons identify Boralevi Lemma 2.1 (Grassmannian tangents), Carlini Proposition 1 (essential variables and the first catalecticant), and Landsberg–Weyman Definition 1/Theorem 3.1 (tensor-product subspace varieties and flattenings). The last is not misrepresented as an alternating-tensor theorem. The required exterior-support rank identity is proved directly. Multiplicity-one plethysm, Cauchy formulas and the basic representation operations are explicitly treated as classical.

New Proposition `prop:schur-subspace-pullbacks` gives exact **reduced** inverse images under the quartic Schur embedding. Support at most 4 pulls back to one-variable quartics; support at most 7 or 8 pulls back to quartics with at most two essential variables; support at most 9 pulls back to the union of the three-variable locus and the quadratic-square locus. Hence quartics with at least three essential variables lie outside even the **closed second secant variety**, including limiting secants. This uses the closed contraction-rank condition.

These reduced equalities do not assert radicality of pulled-back minors. The reconstruction rank-defect locus is still only contained over binary quartics, not identified with the whole inverse image. Exterior support is distinguished from decomposable tensor rank, border rank, and a full orbit classification. The bounded primary-source comparison is recorded in `LITERATURE_AUDIT_V135.md`; it is not an exhaustive priority certificate.

## Report §4.1: residual involution on the determinantal scheme

Lemma `lem:residual-cartier-sections` fixes `T=D₁\D₀` with its determinantal scheme structure, without reduction. On a rank-one chart the residual coefficient pair `(c,d)` is unimodular and the closed-pencil ideal sheaf is `((b-a)(ca+db))`. Where `c d (c+d)` is invertible, `[1:1]` and `[d:-c]` are disjoint effective Cartier sections.

Monic linear equations work over arbitrary coefficient rings. Comaximal ideal sheaves and the Chinese remainder isomorphism prove the disjoint-union assertion over nonreduced bases and after arbitrary base change. An invertible diagonal change of component frames verifies that the residual section factors back through the rank-one determinantal scheme. Exchanging the two Cartier factors twice gives the identity as a morphism. Their disjointness gives an empty fixed-point scheme. This replaces a geometric-point argument with a scheme-level one.

## Report §§4.2–4.3 and §9: precise terminology and scope

The Fitting ramification locus of the quasi-finite part is now defined as `V(Fitt₀ Ω_{X×/Y})` restricted to `X×\D₀`. The same Fitting ideal is defined globally, but no globally finite flat double cover is asserted. Its rank-one equation remains `c+d`, and it is empty on the rank-two stratum; the text cites the differential criterion for unramified morphisms.

The proof of `G₄^rec=G₄°` explicitly uses the reduced open-subscheme structure on `G₄°` and the minors defining its determinantal complement. A finite-type closed C-scheme with no geometric points is empty, regardless of potential nilpotents in its presentation. Essential-variable space lies in V; exterior-support space lies in `Sym²V`. The abstract states only containment of the ambient rank-defect support over binary quartics. The full smooth-locus theorem is unchanged.

## S134.2: article, technical supplement, and preservation

`geometry.tex` is the principal reconstruction article and contains all its load-bearing proofs. The deepest-cone reduction is proved directly using surjectivity at invertible matrices and the Nullstellensatz, rather than apparently depending on the extensive primary-boundary machinery. The component-line argument uses the restricted quadratic ideal directly, without requiring the ambient classification first.

`supplement.tex` retains the complete relative-power, nilpotent-depth, Reye, ambient-pencil, primary-boundary, collision, higher-corank, incidence, relative-specialization, and exact-certificate results. `complete.tex` compiles both bodies into one archival reading object. All **241 inherited mathematical labels** remain compiled. The accepted universal-readout and common-g proof files remain byte-identical. The manifest verifies every v134 source hash before assembly and records preservation explicitly. Cross-PDF references import mathematical labels without AMS-internal table-of-contents data or bibliography keys.

No earlier article or report is rewritten. The revision is published only on its newly created branch, without merging or modifying main or unrelated branches.

## M134.1: Ballico 1993 remains a documentary issue

**The complete theorem-level comparison remains open.** The full text of *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI `10.1002/mana.19931630102`, was not obtained through the accessible lawful routes. Publisher DOI/PDF requests and an institutional-repository query did not return readable complete text. Exact-title/DOI Library retrieval returned earlier A2 patches and audit records, not this primary article.

The audit retains six unresolved axes: parameter space; reduced versus Fitting structure; varied multiplication; nilpotent/colon information; base change; inverse reconstruction. None is filled from the title or later citations. The inspected 1996 paper is distinct and is not substituted for the missing source. Strengthening the proofs and article structure does not certify priority. Neither anticipation nor nonanticipation is claimed.

## Reproduction and evidence

Run `python revisions/a2-v135/assemble.py`, then `bash papers/A2-v17-boundary-information-coarsening/article/v135/build.sh`. The branch-restricted workflow executes all nine inherited exact scripts and the new character/shear/dual-number checks, compiles all three PDFs, and writes `evidence/BUILD_RECEIPT.json` bound to the actual assembly commit and source hashes. The receipt is the authority for executed checks and page counts. These finite checks do not formally certify the structural proofs, historical priority, or any journal decision.
