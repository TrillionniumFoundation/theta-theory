# Response to the independent report on A2 revision 149

**Revision 151: Finite failure schemes and the reconstruction of quadratic pencils**  
Qian Qi · September 24, 2026

## Source identity and reading object

This response addresses `reviews/a2-v149-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`, at controlling tip `ddcef32b3cf491aacb293e466c393ec4af3caecd`, report blob `2878e4dd16cf49e631b933b8c34bafdc896eed8f`. Its principal reading object was the 55-page v149 article. The report is an owner-requested independent-referee-style assessment, not a decision commissioned by a journal. We have not represented its recommendation as an actual journal decision.

The revised principal article is `geometry.pdf`, with all its proofs internal to `geometry.tex`. The applications manuscript and research archive remain separate. Every inherited principal theorem/proof/equation block and label is retained; the preservation check tests their presence in the expanded new principal article, not just in an archive. Number/page mappings for the new results are generated as `evidence/THEOREM_LOCATOR_V151.json` after the verified build. Labels below remain stable across pagination.

The main change is not another rephrasing of the Pluecker image. We now define a divisor incidence on arbitrary first relations, prove that its finite map normalizes its canonical scheme-theoretic image, compute the full scheme fibres, and characterize its normal and smooth points. We separately prove the universal properties of the two rigidifications and construct an explicit closed specialization of every quadratic pencil.

## §16.1 — Full Ballico 1993 comparison

**Status: documentary comparison remains open.** The complete 1993 article was not obtained. The current session checked the publisher/issue routes, attempted the PDF and enhanced-PDF endpoints, used exact-title/DOI and author-institution searches, and searched the available user Library. The Library supplied earlier A2 patches recording the same missing full text, not Ballico's article. A repeated metadata request also failed; no response is presented as a complete reading.

`LITERATURE_AUDIT_V151.md` preserves the requested comparison of objects, nonreduced structure, infinitesimal order, family hypotheses, forgotten markings, and inverse conclusions. The uninspected side of each comparison is explicitly unverified. We do not infer absence of reconstruction from a title, first page, citation list, or the distinct 1996 paper. The introduction continues to state the limitation without changing the all-pencil theorem. New mathematics is not a substitute for this historical check, and we do not label this item resolved.

## §16.2 — A canonical intrinsic stratum and genuine nonreduced parameters

**Change supplied for mathematical re-review.** The new Section `sec:canonical-boundary-v151` begins with an actual functor on all complex schemes. Its data are a relation subbundle K and a line subbundle L of degree-g divisors; its equation is the vanishing of K in the cokernel of multiplication L ⊗ S_h → S_D. This is not a fibrewise divisibility test.

Proposition `prop:incidence-v151` proves that this functor is represented by P(S_g) × Gr(r,S_h) with its full scheme structure. It also proves finiteness of the forgetful map: projectivity and unique factorization give finite geometric fibres, hence a finite morphism. The target Y_g is its scheme-theoretic image, defined by the kernel of the map of structure sheaves. Integrality, and therefore reducedness, is deduced from the integral source rather than imposed on an initially selected set.

Corollary `cor:canonical-exact-v151` identifies the old reduced exact-gcd stratum with the exact-degree open of this canonical image. Its proof includes the missing finite-local argument: a single reduced fibre implies generation by 1 via Nakayama, hence an actual local isomorphism, not merely a bijection of points. This gives the previous common-divisor inverse a precise incidence universal property.

For the jump boundary, Lemma `lem:fibre-equations-v151` gives the complete coefficient equations C_B − M_B(f) M_A(f)^{-1} C_A = 0 on a multiplication-minor chart. They describe the entire scheme fibre over arbitrary coefficient rings on that chart, without taking its radical. The example K = <x²y,x²z> has a unique geometric linear divisor but fibre Spec C[a,b]/(a,b)², of length three. The family x<xy+t y²,xz+t z²> realizes it as an actual limit of the exact-gcd stratum. This directly distinguishes geometric constancy of a gcd from infinitesimal divisibility.

The scope is exact: Y_g means existence of a divisor of degree g, not “gcd degree at least g” in several variables. We do not assert that normalization or scheme-theoretic image commutes with arbitrary nonflat base change. The all-base assertion is proved for the incidence functor and the base change of its representing morphism.

## §16.3 — A geometric theorem beyond the encoded pencil image

**Change supplied for mathematical re-review.** Theorem `thm:boundary-normalization-v151` proves

P(S_g) × Gr(r,S_h) → Y_g

is the finite normalization and that dim Y_g = dim S_g − 1 + r(dim S_h − r). At a geometric point K, Y_g is normal, equivalently smooth, exactly when the gcd F_K has a unique degree-g divisor f and gcd(f,F_K/f)=1. At a specified lift, putting c=gcd(f,F_K/f), k=deg c, the exact kernel of the tangent map is S_k/Cc. This is a global criterion on the canonical boundary, not only a tangent calculation at the pencil locus.

The proof separates two obstructions: different divisor choices give distinct normalization lifts; overlap produces nonreduced fibre directions. The examples show two reduced lifts, a length-three one-point fibre, and a normal point despite a gcd-degree jump. Thus neither fibre cardinality nor gcd degree alone gives the criterion. Corollary `cor:algebra-boundary-v151` turns this construction into the normalization of the intrinsic effective first-relation boundary. There are no factor-invariance, Cauchy-support, or Pluecker conditions in this theorem.

The independent pencil-side Theorem `thm:closed-pencil-v151` constructs, rather than merely transports, a degeneration of every pencil to <x1²,x1x2>. The construction finds a point where d(q1/q0) is nonzero, makes the x1² coefficient of q1 vanish, and uses diag(1,t,t²,...,t²). Its two normalized generators remain polynomial and independent at zero. It proves that the flag variety Fl(1,2;V) is the unique closed orbit in the full pencil Grassmannian, including its singular pencils. Corollary `cor:closed-failure-v151` explicitly constructs the finite-flat failure algebra along this family and verifies that its exact determinant gcd is unchanged.

We do not claim that this elementary highest-weight specialization is itself a new classification of pencils; its proof is supplied as a concrete universal adjacency and failure-family consequence. We likewise do not relabel the inherited spectral classification, arbitrary restrictions to invariant Q, or standard rigidification as separate innovations. The substantive broad boundary theorem is the normalization, exact normal locus, and scheme-fibre calculation for arbitrary divisorial first relations. Its final significance and novelty remain for independent mathematical and literature review.

## §16.4 — Standard and canonical rigidification

**Change supplied for mathematical re-review.** Theorem `thm:rigidification-v151` characterizes the first-relation quotient by its mapping property: maps from the relation stack to any target stack are equivalent, including 2-isomorphisms, to maps from the algebra stack killing the tangent-identity inertia. The proof gives local lifts, independence under the kernel, the cocycle calculation, and effective descent. The kernel is a smooth affine normal subgroup with underlying local scheme Hom(E,N²); its group law is not declared additive.

Corollary `cor:two-rigidifications-v151` applies the same property to [P/G°] → [P/PGL(V)]. It identifies the right GL(U) kernel over a torsor as the conjugation-associated subgroup scheme, not an erroneously constant group on every base. No global group splitting is assumed. Genuine projective pencil stabilizers remain. The standard literature on normal, not necessarily central, inertia rigidification is acknowledged; the new text proves the needed universal property directly rather than treating quotienting arrows as an unexplained convention.

## §16.5 — Preserve the previous strengthening and documentation

**Preserved and checked by source comparison.** The revision leaves the all-pencil local inverse, exact gcd det(T)^(n−1), primitive support asymmetry, nonreduced-base pencil comparison, moving-pencil actual-bundle recovery, one constant left transformation, sharp reconstruction order, transverse fixed-radical families, and covering-map/spectral results in the principal article. All inherited part files are byte-identical. Root files which needed updated routing or prose have their predecessor bytes separately preserved. No arbitrary theorem deletion or conversion of the all-pencil assertion into a generic theorem has occurred.

The abstract is self-contained and below 200 words. Main exposition is theorem/proof oriented rather than a revision diary. Technical proofs stay next to the theorems that use them; independent historical research remains in the existing non-submitted companion. AI assistance is acknowledged with the specific locations of the new mathematical ideas, in addition to the inherited disclosure. No AI system is listed as author.

The build runs 26 inherited regression scripts plus the new exact script, native LaTeX builds of the three documents, source/block/label retention, and reference/overfull-box checks. Source-commit and PDF hashes are recorded only after execution. Computation is finite-witness evidence; it does not certify the universal proofs, the Ballico comparison, or acceptance by any journal.
