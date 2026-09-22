# Response to the primary-contact R116 report

**Manuscript:** Finite quotients and primary structures of multiplication failure schemes.
**Revision:** A2-v117-finite-quotient, on `revision/a2-v117-finite-quotient-primary-structure-2026-09-22`.
**Controlling report:** `a65e0e92b24fe6882e60ebcf678bb2f9f5048312`, reviewing `fadcfaa11a1939625177eb12e97569b63b7a1a9d`.

We thank the referee for distinguishing correctness, proof architecture and venue-level significance. This response adds structural results rather than a claim of acceptance. We do not treat finite tests as proofs or inaccessible literature as evidence of priority.

## The structural advance requested in Sections 3, 6, 7 and 16

The revision pursues Routes B, C and E. Its principal result is no longer a rank-two power-basis calculation. Theorem `thm:universal-hyperplane` treats generating hyperplanes in an arbitrary finite locally free algebra B, with no curvilinearity or monogenic assumption. The entire higher-multiplication failure scheme is identified, on arbitrary test schemes, with rank-two quotient algebras carrying a generating line. The key algebraic statement is Lemma `lem:hyperplane-subalgebra`: the conductor of a unital hyperplane subalgebra has locally free rank d-2. A cyclic residual presentation proves equality of all degree-m Fitting ideals, not merely equality of closed points.

Theorem `thm:contact-hyperplane-primary` solves the resulting genuinely multigenerator problem for k=d-1 on every fixed multiplicity partition. It determines every primary component, exact transverse algebra, length and nilradical index. Its transverse algebras include the classical cohomology ring of Gr(2,r), but the multiplication-scheme identification is proved through the quotient functor and again by explicit residual equations. The moving theorem `thm:moving-hyperplane` identifies the failure scheme itself with a smooth open projective-line bundle over a nested-divisor space. It is not merely a normalization assertion. Proposition `prop:noncurvilinear-embedded` gives an exact embedded primary chart outside the curvilinear setting.

Theorem `thm:three-plane-primary` supplies a second multigenerator family: on a reduced divisor, every stable ideal and every power is determined by the pair diagonals. Haiman's deep diagonal-ideal theorem is explicitly the input; the added proof is a polynomial, base-change-compatible total-degree truncation and its transport to the original multiplication cokernel.

The sharp binary range is n >= 2d-k. Theorem `thm:sharp-conductor` proves both sufficiency and a degree-two boundary family at n=2d-k-1. Proposition `prop:curve-kernel-test` gives the exact cohomological obstruction on a curve; Theorem `thm:curve-conductor` gives structural sufficient hypotheses and the uniform bound deg L >= 2d+2g-1.

These advances do not assert that every question about an unrestricted Grassmannian has been solved. They provide complete new scheme theorems in entire stated families and a universal finite-algebra identification, rather than changing the labels attached to old results.

## E116.1 — unique identity

**Addressed for this delivery.** A single previously unused v117 branch and identity are used. `IDENTITY.json` fixes the review base, the reviewed manuscript and the excluded divergent v116 head. Existing v116 branches are not renamed or rewritten: their pinned history is preserved. The workflow records a committed mathematical source separately from the actual generated-PDF commit. A future referee can freeze one immutable head instead of relying on timestamps or the ambiguous label “v116”.

## E116.2 — Ballico 1993

**Not completed.** The complete theorem pages of the 1993 article were not obtained. Publisher metadata and an abstract/TOC/PDF landing route are not a theorem-level comparison. The main article and `AUDIT.md` state this explicitly. We neither assert disjointness nor infer novelty from unsuccessful access. The new mathematics does not remove this scholarly obligation, and this response does not mark it closed.

## E116.3 — primitive-element, index-form and discriminant literature

**Addressed by theorem-level attribution, subject to E116.2.** Arpin–Bozlee–Herr–Smith, *The Scheme of Monogenic Generators I*, Proposition 3.6, Definition 3.12 and Proposition 3.14, are compared with the generator functor, index form and polygenerator minors. The text states literally that Delta is the classical local index form in the chosen monogenic presentation. Haiman Corollary 3.8.3 and the Grassmannian presentation/Schur basis in Grinberg Theorem 2.7 are identified precisely. Green–Lazarsfeld's introduction, p.73, is the cited source for the classical sufficient normal-generation degree. These citations separate classical ingredients from the exact global multiplication-cokernel transport and the hyperplane quotient identification; they do not certify global priority.

## E116.4 — primary descent

**Addressed.** Lemma `lem:etale-primary-descent` separately proves descent of the invariant invertible orbit ideal, irreducibility and reducedness of its downstairs Cartier divisor, powers, intersections and absence of embedded primes. The proof works at every point; it makes no normal-crossing hypothesis. It explains why a descended prime divisor need not be smooth or geometrically unibranched. Corollary `cor:contact-multiplicity-strata` now invokes this lemma rather than treating these facts as a one-paragraph descent shorthand.

## E116.5 — normalization novelty boundary

**Addressed.** The index-form discriminant identity appears in the introduction. The scalar-pair normalization is explicitly positioned within that model, and its finite/birational and differential arguments remain in full. The new hyperplane quotient incidence is distinguished from it: it equals the entire failure scheme and is smooth when contacts move, while an explicit noncurvilinear chart has embedded structure. No independent novelty is attributed to the classical discriminant identity or Vandermonde determinant.

## E116.6 — exact scope

**Addressed without weakening a theorem.** The abstract and first paragraphs specify conductor-containing series and the dimensions of the finite quotient series. Unbounded ambient codimension is not used as a proxy for arbitrary high-rank generality. Rank-dependent improvements and the multigenerator theorems replace that rhetorical comparison with new statements. The original pencil family and all its results remain.

## E116.7 — article identity and preservation

**Addressed by separate reading editions, not deletion.** `geometry.tex` is the coherent finite-contact article. Its proofs do not depend on the quadratic excess, polar residual or statistical theories. `paper.tex` retains all those developments and their full proofs as complementary geometry and appendices. `applications.tex` remains independently readable with exported cross-references into the complete paper. All 28 reviewed TeX files are additionally preserved byte-for-byte and hashed. Every old part label is present in the complete manuscript; unchanged old parts are checked byte-for-byte. The dependency diagram in the introduction states actual proof dependencies rather than inventing a logical dependence between independent results.

## E116.8 — conductor threshold

**Addressed with a sharp uniform bound and structural generalization.** The evaluation-kernel splitting gives a_max <= d-k+1, hence n-d >= d-k suffices. The explicit monomial family at n=2d-k-1 omits t^(2d-1) from U^2 although it lies in the vanishing ideal. This proves sharpness for all D,A and all m simultaneously; no separate sharpness claim is made for each m>2. The earlier two-layer proof is retained in the complete edition. The curve theorem states hypotheses, a numerical sufficient range and an exact H^1 obstruction rather than claiming an optimal positive-genus bound.

## Smaller requests, Section 18

1. `thm:contact-main` expressly states that for 2 <= m < d-1 the pencil zeroth Fitting ideal is zero and the failure scheme is the whole base.
2. The descent lemma and its application distinguish integrality, smoothness and geometric unibranchedness.
3. Every complete primary statement identifies its base: fixed divisor, multiplicity stratum, reduced moving stratum, or moving total scheme.
4–5. The index form and discriminant identity are in the introduction with explicit classical terminology.
6. Section `sec:pencil-collision-types` distinguishes a unique reduced pair, intersecting pairs, smooth total points with primary fixed fibres, and a unique-preimage ramified normalization point. It does not infer a cusp normal form merely from a singular differential.
7. The introduction includes the dependency diagram and points to the exact main theorem and its proof.
8. Applications remain separate from the finite-contact proof spine.

## Remaining older questions and editorial assessment

The old unrestricted quadratic excess associated-prime problem and the exact embedded evaluation-curve primary ideal are not silently declared solved. Their established theorems remain unchanged in the complete edition. The new fixed-contact hyperplane theorem applies on the generating open and states exactly what it classifies. We ask that the new quotient theorem, full multigenerator primary fibres, smooth moving total scheme and sharp/curve conductor results be assessed on their proofs and scope. We make no claim that an author revision or a successful build establishes top-four acceptance, universal proof certification or unresolved bibliographic priority.
