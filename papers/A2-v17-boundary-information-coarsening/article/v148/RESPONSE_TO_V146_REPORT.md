# Response to the independent A2 v146 referee report

**Manuscript:** Finite failure schemes and the reconstruction of quadratic pencils.  
**Revision:** 147.  
**Controlling report:** `855c73b3a0381bebd8d5e0d382fa06125904a73f`, `reviews/a2-v146-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`.

We thank the referee for distinguishing the correctness of the proposed inverse from its conceptual positioning. This revision retains every all-pencil statement, including singular pencils, and every principal mathematical block of v146. It develops the moving-family mechanism into a general coefficient-descent theorem rather than replacing it by a generic statement. The response below gives source labels, which remain stable if final pagination changes.

## 1. General first-relation mechanism (§3, 12.1)

`prop:first-relation-orbit-v147` treats arbitrary algebras Sym(E)/(K+m^(d+1)) with K in pure degree d. It recovers the cotangent space and K intrinsically from multiplication, proves the equivalence between ungraded isomorphisms and the linear orbit of K, and describes every higher-order generator correction. No canonical-grading claim for arbitrary filtered deformations is made.

The local pencil theorem is retained. Its specific content is now explicitly the recovery of matrix factors and pencil coefficients from the unrestricted linear orbit of K_R. The fact that degree-d relations are insensitive to higher substitutions is proved once as a general algebraic fact, not presented as a separate nonlinear Torelli phenomenon. The smallest uniform degree statement is unchanged; it remains a uniform threshold, not a pairwise minimality claim.

## 2. Actual source-bundle descent (§5, 12.2)

`lem:actual-factor-descent-v147` proves the missing global step. After fixing the constant left linear lift, the actual normal-bundle map commutes with End(V). The canonical sheaf isomorphism Hom_End(V)(V⊗A1,V⊗A2)=Hom(A1,A2) produces the right bundle map as a global section. The proof establishes its invertibility and uniqueness and explains precisely why an isomorphism of projectivizations alone would be insufficient. It uses reducedness only where fibrewise vanishing is promoted to vanishing of a bundle morphism.

`thm:general-moving-coefficients-v147` applies this lemma to the actual map obtained from the dual of n/n². The original scheme isomorphism need not preserve the graph projection: its action on the first nilradical quotient is nevertheless linear over the recovered reduction. Thus the argument does not silently add a marking or an O_B-linearity hypothesis on the original unmarked map.

## 3. A broader global inverse, with a separating example (§§10, 14)

The new theorem reconstructs simultaneously varying coefficient subspaces in several multiplicity-one Schur modules. The coefficient ranks need not be one. A nonzero proper support in one summand orients the two factors, without any projective-bundle nontriviality assumption. The conclusion recovers the whole coefficient maps, one common constant left transformation, and the actual right vector bundle. Its local freeness, radical calculation, determinant cancellation, orientation, global descent and converse are all proved in the principal manuscript.

`ex:isotrivial-covers-v147` demonstrates a genuinely global distinction. It gives two Zariski locally trivial rank-712 thickenings of P1 with isomorphic Artin fibres and isomorphic nilradical graded vector bundles in every degree. The abstract first-relation bundles also agree. Their unmarked total schemes are nevertheless different, because coefficient descent would identify the degree-three maps z^3 and z^3+z, whose ramification profiles are (3,3) and (3,2,2). The graded algebra structures, unlike the underlying vector bundles, do not agree.

This example is not a spectral readout after a pencil has already been recovered. It exhibits information invisible to both fibrewise algebra classification and the underlying graded bundles. The q=1 example belongs to the general coefficient theorem, with order four; it does not alter the quadratic-pencil order d. Whether this conceptual extension warrants a particular journal remains for independent judgment.

## 4. The category of the automorphism sequence (§4, 12.3)

`prop:first-relation-group-v147` represents the full local automorphism functor as a closed subgroup scheme of GL(A). The augmentation is recovered from normalized regular trace; this handles arbitrary commutative complex coefficient algebras, including nonreduced ones, without identifying an augmentation ideal with the absolute nilradical. The linear-part map, its homogeneous section, and the polynomial parameterization of the kernel are morphisms of schemes. The kernel is embedded in a unitriangular group.

The intrinsic description is a simply transitive action on the space of splittings of n→n/n². An affine-space underlying scheme is not asserted to have an additive group law. `cor:pencil-group-scheme-v147` identifies the pencil stabilizer quotient with (G_R×GL(U))/G_m, with the diagonal scalar subgroup, and supplies the algebraic-group interpretation of the retained point-local exact sequence. Cartier smoothness in characteristic zero is cited precisely.

For positive-dimensional projective reductions the retained sequence is explicitly a sequence of groups of complex scheme automorphisms, with its original filtered kernel. No finite-type affine representability or equivalence of all deformation groupoids is asserted for that sequence.

## 5. Classical preserver theory (§2, 12.4)

`lem:linear-preserver-v147` states the exact square, invertible, complex-linear hypothesis. It proves the reduction from determinant preservation through successive rank loci to the rank-one Segre cone, and then proves the left-right/transposed alternatives. Marcus–Moyls, Theorem 1, printed pages 1218–1219, is cited as the classical input. Unequal residual support ranks supply the pencil-specific exclusion of transposition. The elementary preserver classification itself is not claimed as new.

## 6. Inverse systems and canonical grading (§9, 12.5)

The principal manuscript now gives the exact apolar description I^perp=(⊕_{j<d}Sym^j E*)⊕K^perp and proves it. It compares Elias–Rossi's short Gorenstein theorem (Theorem 3.3; Corollaries 3.4–3.5 in arXiv:0911.3565v1) and the compressed Gorenstein theorem (Theorem 3.1 and boundary examples in arXiv:1207.6919v1). Their nonlinear elimination of lower-degree inverse-system terms is distinguished from our already homogeneous truncation. The pencil algebras have socle degree at least eleven and a top socle subspace of dimension greater than one, so they are not in those Gorenstein classes. Difference of hypotheses is not used as a blanket priority argument.

## 7. Ballico 1993 (§8, 12.6)

There is a limited but real documentary advance: the publisher's first-page image, printed page 5, has been inspected. It introduces higher-order embedding properties for projective varieties, finite subschemes, and restriction maps. This permits a partial comparison of setup; it is no longer accurate to describe access as metadata-only.

The publisher PDF/ePDF links still did not provide pages 6–13 or complete theorem/proof text in this examination. Therefore the complete six-axis comparison requested by the referee has **not** been completed. The ledger records which statements are actually visible and leaves all uninspected theorem-level cells unresolved. No absence of a Fitting structure, relative construction or inverse theorem is inferred from the opening page, and the distinct 1996 article is not used as a substitute. The mathematical revisions above do not discharge this documentary obligation.

## 8. Publication object, preservation and evidence (§§7, 11, 12.7, 13–14)

The main object remains geometry.pdf. Applications and the historical archive remain separate. The inherited all-pencil, point-local, curve-supported, moving-family, arbitrary marked-base-change and regular-spectral statements retain their respective hypotheses. No extra condition is imposed on the pencil. All predecessor part files and all principal theorem/proof/equation blocks are preserved; root sources have exact copies in history/v146-root.

The source-bound receipt records all 24 executed scripts, native PDF hashes, reference and label checks and source preservation. The source lock names the immutable mathematical source commit, not merely the final evidence-publication commit. Exact regressions include nonreduced coefficient substitutions, normalized trace, commutants, transition compatibility, support ranks and the global example. They are finite checks, not proofs of universal geometry, literature completeness or editorial significance.
