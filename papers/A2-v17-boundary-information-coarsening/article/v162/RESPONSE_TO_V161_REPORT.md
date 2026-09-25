# A2 revision 162 — response to the complete v161 report

## Objects and substantive change

Controlling report: `reviews/a2-v161-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`, commit `3d22c10f34d889081000232bb8f2241d5988fc37`. Complete reviewed predecessor: v161, final tip `9e3b6639021a5f1fdb725961c7a7b6bb9cf55779`, mathematical source `da3ce030046e2651cf81a76be472329214373c88`, materialization `5c3aaa92ce605a43ae31a98ed9cf652202a161dd`. This revision is written on the new branch `revision/a2-v162-versal-contact-neighborhoods-2026-09-25`, based on the report commit. No older branch is overwritten.

The central mathematical request is not answered by another two-parameter slice. Paper II now supplies the full formal contact parameters, an open Hilbert chart with a regular inverse, a collision law within ambient neighbourhoods, and an actual non-equidimensional Hilbert fibre. The core new statements are:

- **Theorem 6.2:** ambient realization of contact parameters for regular symmetric pencils, including arbitrary positive Smith exponents in the formal normal-coordinate statement. At corank two with exponents a <= b the residual matrix is `[f,g;g,fk+r]` with **2a+b** independent parameters. The original balanced two-constant-parameter slices are not versal.
- **Theorem 7.1:** the Euclidean map `(f,g,w) -> (f,g,rem_f(gw))` is an **open chart of the reduced Hilbert graph** near every primitive thick-line lift. A cohomological coefficient-recovery map supplies a regular inverse; pointwise injectivity alone is not used as a substitute.
- **Theorem 7.2:** these are neighbourhoods in the actual pencil Hilbert problem. The primitive line-tail locus over a fixed corank-two pencil is the product of `J_(a_i-1)(P^1)`. The exact gcd law describes mixed thicknesses and collisions in these charts, not only reduced supports.
- **Theorem 8.1:** at one contact with exponents `(2,2)`, the normalized Hilbert fibre has a dimension-two component with open part `J_1(P^1)` and a distinct component of dimension at least four. Reduced conics through the attaching point supply the latter family. This is an ambient fibre statement, not a selected parameter-slice fibre.

The full miniversal principle for symmetric pencil congruence is classical and is credited to Dmytryshyn. The new claims concern the specified embedded Hilbert charts, their ambient comparison, fibre law and different-dimensional components. The target stays fixed; embedded tails are never identified by an ambient automorphism quotient. The normal-coordinate comparison retains the pencil parameter in the incidence target, treats x-dependent congruence there rather than as a constant global target automorphism, and uses the actual Rees image. The open jet morphism is also constructed algebraically from its line subbundle and attaching scheme.

These results do not classify every component of every proper fibre, do not replace the all-pencil inverse by a regular-pencil inverse, and do not assert that an internal operation on a closed finite algebra bypasses reconstruction. They respond to the report's requests for versal information and actual ambient boundary components with stated results and written proofs.

## Responses to the 38 requests

### 1. Finite/unramified criterion and empty fibres

Paper II, Proposition T.1, proves in one place that a finite complex algebra has zero Kähler differentials exactly when it is a product of copies of C. The proof uses the cotangent space of each local Artin factor and Nakayama. The geometric-residue-field version is stated. Empty fibres are admitted and `Fitt_0(0)=O` is explicit.

### 2. Openness and finiteness

Proposition T.1 treats the regular pencil open avoiding corank at least three. A nonzero determinant polynomial makes the incidence quasi-finite; properness makes it finite. Removing the finite closed image of the support of relative differentials gives exactly `U_red`. No flatness of the finite incidence algebra is assumed.

### 3. Tangent-normal sequence

Equation (T.1) writes `0 -> T_R Sigma_p -> T_R G -> N_(Z/P,p)/image(T_p L_R) -> 0`. The map is restriction `Hom(R,M/R) -> Hom(ell,M/R)` followed by the normal quotient. Motion of the incidence point identifies its kernel. This also locates the two normal equations of each centre.

### 4. Strict henselization and étale descent

Proposition T.1 separates splitting idempotents after strict henselization from descent of those finite idempotents and their equations to an étale neighbourhood. Nakayama is applied to the unit-map cokernel of each length-one factor, followed by shrinking. The result is a closed immersion of that factor, not just a labelling of geometric points.

### 5. Codimension

The same proposition computes `dim G + 1 - 3 = dim G - 2` using smooth universal-line evaluation and the three symmetric Schur-complement equations of the smooth rank locus. The tangent sequence gives the same codimension two.

### 6. Nonsemisimplicity

Distinct primary eigenspaces of a self-adjoint operator have direct sum without diagonalizability. Proposition T.1 uses precisely this directness for joint normal surjectivity. Theorem 6.2 independently treats Jordan blocks and proves that actual constant pencil perturbations span every contact deformation coefficient. Semisimplicity is not introduced as an extra hypothesis.

### 7. Projective twists

Proposition T.1 records the one-dimensional factor `ell^*` in the normal representation and identifies it on both sides of the restriction map. It states the radical/dual convention for symmetric maps `V^* -> V`. A frame changes both maps by the same unit; it is not used to suppress an untracked twist. Proposition T.4 separately treats the original line twist on an Artin support and the graph line bundle on its thick tail.

### 8. Independent-centre product blow-up

Lemma T.2 states the independent regular-parameter-pair hypotheses explicitly and proves the fibre-product identity by affine ratio charts. It does not assert that an arbitrary blow-up of a product is an arbitrary fibre product without these hypotheses.

### 9. Proj, diagonal and MultiProj

Lemma T.2 gives the multi-Rees relations, shows the diagonal algebra is standard graded and is exactly the ordinary Rees algebra of the product, and computes the degree-zero localized rings. The ordinary Proj of that diagonal is separated from MultiProj of the full multigraded algebra.

### 10. Unlabelled exceptional boundary

Proposition T.1 and Lemma T.2 describe permutation of the local factors on étale overlaps. The Fitting centre and product modification descend without a global ordering. The new contact coordinates are likewise independent at distinct spectral supports; their labelling is an atlas, not an extra marking on the unlabelled problem.

### 11. Integrality of the Hilbert graph

Both the universal polynomial graph at the start of Section 7 and the reduced-incidence normalization argument in Lemma T.2 state integrality as the reduced closure of the graph over an integral dense open. The shared dense open identifies the function fields before normalization is used.

### 12. Finite geometric fibres

Lemma T.2 collects the argument that restriction to each fixed exceptional plane recovers the chosen embedded tail, so fibres of the proper map to the Hilbert graph are finite. The division-chart theorem uses the stronger regular inverse rather than relying only on a finite-fibre argument.

### 13. Fixed target versus automorphisms

The paper fixes complete quadrics as the target of the Hilbert functor. Different embedded lines or conics define different Hilbert points. Source frame changes are atlas changes; they do not quotient the fixed fibre by the stabilizer of the pencil. Section 7 explicitly distinguishes an x-dependent automorphism of the incidence target over a parameter disc from a constant automorphism of the projective target.

### 14. Finiteness and normalization

The proper-plus-quasi-finite input is Stacks Tag 02LS. Lemma T.2 applies it first; only then does a finite birational morphism from a normal integral source identify the normalization. Theorem 8.1 instead takes the finite surjective inverse image of the conic family under normalization, without claiming that an arbitrary nondominant normal family lifts.

### 15. Polarizations

The revised introduction defines `H_q` and the product polarization with Hilbert polynomial `binom(n,2) l + 1` before the pencil graph. Section 7 independently defines the polynomial-graph target `P^1 x P^2`, its `O(1,1)` polarization and polynomial `(a+1)l+1`. Theorem 7.2 explains the translation back to the exterior multidegrees.

### 16. Jordan signs and Schur complement

Lemma T.3 proves both complementary and reversal determinants equal `(-1)^(m(m-1)/2)`, making the scalar Schur complement exactly `x^m` and the two-block determinant constant one. Theorem 6.2 also writes the exact kernel-lifting vector identity and its Schur derivative, which realizes all missing miniversal coefficients.

### 17. Infinity

Lemma T.3 computes the homogenized pencil at infinity as `E_m direct-sum E_m`, hence nonsingular. The polynomial-graph model has monic f and smaller-degree g,r, so its infinity value is `[1:0:0]` and has no base ideal. These are separate checks for the two constructions.

### 18. Flatness of nonreduced Rees charts

The fibrewise locally-principal Cartier criterion is now cited exactly as Stacks Tag 062Y, part (3). Its hypotheses are stated: flat finite-presentation smooth ambient space, one equation, and a nonzerodivisor in every geometric fibre. The chart `x^m=tz` additionally has a direct free-module proof using the monic x-equation. The division graph satisfies the same criterion because f is monic.

### 19. Serre normality

Lemma T.3 states that the singular chart is a hypersurface domain, hence Cohen–Macaulay and S2, with singular locus of codimension two, hence R1. The other chart is smooth. The general Hilbert charts of Theorem 7.1 are smooth by their regular inverse, not by an unsupported fibrewise normality inference.

### 20. Associated primes

Lemma T.3 gives `(x^m y)=(x^m) intersection (y)`, with associated primes `(x)` and `(y)`; the other chart has only `(x)`. Theorem 7.1 extends the scheme-union calculation to `d(g_1 U-f_1 V)` for an arbitrary gcd, using coprimeness and Cohen–Macaulayness, so mixed thick fibres have no embedded associated points.

### 21. Coefficient module over the Artin base

Proposition T.4 isolates the A-linear coefficient surjection to `H^0(P^1_A,O(delta_j))`. It composes split multiplication by the unit-block socle, the residual ternary coefficient module from the universal ideal identity, removal of its determinant factor, and restriction to a split primitive line. This retains nilpotent coefficients over the whole Artin algebra rather than checking only geometric fibres.

### 22. Thick-tail twists

Proposition T.4 explicitly trivializes the original `O(j)` on the affine Artin support and distinguishes it from the graph bundle `O_T(delta_j)`. Invertible Gaussian transformations act on the entire coefficient module. No degree claim is obtained by dropping these twists.

### 23. The transverse surface

Proposition T.5 fixes `S_m=Bl_(x^m,t) A^2_(x,t)` with its proper exceptional curve F. The exceptional Cartier ideal is `O(-mF)` and restricts to degree one on F, so `mF.F=-1`. This defines and proves `F^2=-1/m` even though the surface is not proper, since F is proper.

### 24. Orientation of the resolution chain

Proposition T.5 identifies the ray meeting F and the ordered multiplicities `m-1,...,1`. The main component meets F at the other smooth point, corresponding to `z=infinity`. The far end faces the horizontal strict transform `z=0`, not the main special-fibre component. This makes the earlier local ray computation unambiguous.

### 25. Deformation categories

The abstract `T^1` calculation continues to concern only the total hypersurface singularity. The new relative class is an Ext class for the relative cotangent complex with a base deformation fixed. The embedded Hilbert functor retains its fixed target, and the transported failure-family assertions remain on the effective image. No equivalence among these or a separate Q-Gorenstein versality theorem is asserted.

### 26. Marking and stable-map automorphisms

Proposition T.5 marks the attachment `[1:0]` on the degree-m tail `[X:S] -> [X^m:S^m]`. Automorphisms over the fixed map are precisely multiplication of the affine ratio by an mth root of unity. Their finiteness makes the nonconstant component stable with that single attachment.

### 27. Ramified normalization

Proposition T.5 gives the common field `C(x,s)`. The two normal rings adjoin `s/x` and `x/s`, integral because their mth powers are the old graph coordinates. The resulting finite regular charts glue to the ordinary point blow-up. Normalization is not inferred solely from a set-theoretic parameterization.

### 28. Invariant relative obstruction

Paper I, Proposition F.2, gives `L_(B/U)=[O e -> O dw]` with differential `-u` on `v=uw`. On the overlap `z=w^-1`, the frames are `e'=-z e` and `dz=-z^2 dw`. The relation defects and tangent corrections transform accordingly. Their cokernels represent the same Ext^1 class; independent contact factors form a direct sum with étale permutation descent.

### 29. Algebraic envelope target

Paper I, Proposition F.1, constructs the finite-type affine automorphism group of the specified projective-space bundle, graded algebra and power diagram. Its fppf forms are the algebraic classifying stack BH. This is a positive algebraicity statement for the actual target used; it is not a boundedness claim for all algebra bundles on arbitrary total sources.

### 30. Effective-stack scope

The new abstracts, introductions and Corollary F.3 state the effective limitation. The contact parameters and Hilbert families transfer through the family-level inverse on the effectively rigidified image. They are not statements about all raw Artin algebras of the same length.

### 31. Rees algebra versus new geometric content

The revision does not count the notation `direct sum I^d` as a new result. The new content lies in a complete embedded Hilbert chart with inverse, its exact fibre law, its ambient realization, and the existence of different-dimensional components. The actual Rees and coefficient equations are supplied where used.

### 32. Distinguished exponent

The exponent-free intrinsic application uses h=1, especially `J_(n-1)=I_(n-1)` on the rank open. Larger h remains an auxiliary integer producing the same graph and different coefficient systems. Nothing in the envelope's descent removes that numerical choice.

### 33. Slices and versal neighbourhoods

The old Jordan slice theorem remains unchanged and explicitly scoped as a slice. Theorem 6.2 now proves the additional ambient realization and gives 3a parameters in the balanced case, rather than two. Theorem 7.2 computes full neighbourhoods of primitive line-tail lifts. Theorem 8.1 shows why those neighbourhoods still do not exhaust the proper fibre. This is an extension by separate proved assertions, not a relabelling of the old slice as universal.

### 34. Expanded literature comparison

The paper now compares the precise moduli objects in Dmytryshyn's congruence-miniversal theorem, Hu–Lin–Shao's compactification of parameterized maps by resultant strata, and Chung–Hong–Kiem's Hilbert/Simpson/Kontsevich comparisons. These are primary sources, alongside the inherited Li and Gathmann comparisons. The literature audit states what was inspected and does not use a missing search hit as a nonanticipation argument.

### 35. Ballico limitation

The 1993 theorem/proof-level comparison remains incomplete. The legitimate publisher PDF route checked in this round did not provide a readable full text. This is disclosed inside both submitted papers, not only metadata. The separately available 1996 theorem remains distinguished; no unsupported historical priority conclusion is drawn.

### 36. Finite checks

The new script audits actual tangent ranks, centralizer dimensions, Jordan constants, Euclidean identities, resultant multiplication matrices, Fitting minors, Rees equations, inverse coefficient ranks, conic ideals and Artin overlap equations. They test finite instances of written proofs. The full remote build invokes the inherited v161 suite. Neither passing checks nor preservation receipts are called general proof certificates.

### 37. Focus and preservation

Paper II's principal route is now power ideals -> full contact parameters -> open Hilbert charts -> non-equidimensional fibre. Reduced-incidence and exact slice results are retained, with older spectral, reciprocal-fibre and collision extensions in appendices. Paper I retains its sharp inverse as the principal route. No predecessor mathematical environment is deleted; the revised front matter is archived. The enlarged total page count is not represented as a shortening.

### 38. Independent proof audit of Paper I

No new external independent referee or formal proof verifier was obtained in this interaction. This request is **not marked closed**. The complete source, theorem dependency descriptions, inherited proofs and preservation records are supplied for that audit. The present revision's manual proof analysis and finite checks are not misrepresented as an independent external verification of the long sharp inverse.

## Preservation and next review priorities

The complete v161 master has 453 labels and 299 mathematical environment blocks. The v162 assembler checks their exact retention and partitions the mathematical body exactly once between the companions. It archives all three predecessor front matters and replaces the root reading entry only after successful build publication. Source, output and verification-seal commits are recorded separately.

The next referee should focus on the formal ambient comparison in Theorem 7.2, the cohomological regular inverse in Theorem 7.1, and the two component arguments in Theorem 8.1. The latter uses a finite inverse image under normalization rather than an automatic lifting claim. The open primitive locus is not the whole proper fibre. Full component classification outside these charts, singular-pencil Hilbert geometry, the pre-reconstruction internal operation, the Ballico full-text comparison and an external audit of Paper I are not claimed completed. These boundaries do not alter the original all-pencil inverse or remove the inherited results.
