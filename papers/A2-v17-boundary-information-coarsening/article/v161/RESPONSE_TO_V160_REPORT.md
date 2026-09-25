# A2 revision 161 — response to the complete v160 report

Controlling report: `reviews/a2-v160-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`, commit `596df442f9155c79b6b33378c0a208259385b2ae`.

Complete predecessor: revision 160 at `58c33453bf01d1f73083cb744d0479ecdc3dcf2f`; its mathematical master has SHA-256 `ebe53861e6313880a01b8bda8e80930f209c1b20c7c9ed1e6b78b52cffa27d73`. The revision branch is `revision/a2-v161-multiple-incidence-contact-singularities-2026-09-25`. Every predecessor mathematical statement and proof is retained. Old introductions are archived separately; the main texts are reorganized around their central theorems, with all other results in complete appendices.

## The mathematical response

The report identifies three substantive directions: enlarge the single-incidence open, compute nonreduced boundary phenomena, and replace a merely formal Rees recovery by actual equations and deformation information. This revision addresses all three.

**Full multiple reduced incidence.** The main boundary theorem now holds on the entire open of regular pencils avoiding corank at least three and having reduced corank-two incidence, with no restriction to a single point. The exact centre is `Fitt_0(q_* O_D)`. At a pencil with k incidences, the entire normalized Hilbert fibre is `(P^1)^k`; the universal curve has k independent nodal tails and the boundary has étale normal crossings. The independence of the local incidence centres is proved for every pencil in this open from the direct sum of radicals at distinct spectral points. It is not imposed as an additional genericity assumption. In particular the full double-incidence fibre, including its scheme structure, is computed as `P^1 x P^1`.

**Nonreduced contact of every order.** For each m >= 2, the paper constructs genuine symmetric linear pencils in dimension 2m with residual Schur complement `[[x^m+u,v],[v,x^m-u]]`. Their incidence ideal is exactly `(x^m,u,v)`. The normalized Hilbert graph of the complete two-parameter slice is the point blow-up of the parameter plane. Its special curve is a main component with the thick tail `P^1_(C[x]/x^m)`, meeting along a length-m scheme; there are no embedded points. The total multiplication graph has Rees equation `tU-x^mV=0` and transverse surface singularity `x^m=tz`, of type A_(m-1). Its local cotangent deformation space has dimension m-1. After the ramified base change t=s^m and normalization, the stable-map tail is reduced and covers the same residual line with degree m. This gives an explicit Hilbert-versus-stable-map distinction rather than conflating the two compactifications.

**Effective moduli and relative lifting.** The envelope is formulated as a morphism from the specified effectively rigidified failure stack to a stack of graded algebra bundles. The multiple-incidence modification descends as a representable proper birational morphism of smooth Artin stacks. The local multi-Rees algebra is presented by `v_i U_i-u_i V_i`; its diagonal is the ordinary Rees algebra of the Fitting ideal. Relative lifting across a square-zero extension with kernel J is governed by the exact classes `[v_i'-u_i' wtilde_i]` in `J/u_i'J`. These are relative obstructions for a fixed base deformation, not absolute obstructions on the smooth effective stack or claims about every deformation of a raw Artin algebra.

The first result is global over the stated reduced-incidence open. The second computes the whole graph of each specified nonreduced slice, not the full ambient fibre outside that open. The distinction is explicit. Neither result replaces or restricts the original all-pencil sharp inverse or the retained singular-pencil and ordinary higher-corank theories.

## Point-by-point responses

The identifiers below are stable LaTeX labels. `THEOREM_INDEX_V161.json` supplies the actual paper, number and page in the compiled reading objects.

### 1. General transverse-incidence lemma

`lem:general-incidence-v161` states the result for a smooth family of embedded curves meeting a smooth codimension-c centre. It spells out finite unramified incidence and the joint normal-evaluation hypothesis. Its local ideals are `(x_i,u_i1,...,u_i,c-1)`. The independent-centre arrangement calculation is explicitly credited as classical; `lem:independent-radicals-v161` proves the pencil-specific hypothesis rather than disguising it as general blow-up geometry.

### 2. Precise finite-incidence open

The construction first restricts to regular pencils and removes the proper image of incidence with the lower-rank locus. On this open a positive-dimensional intersection with the corank-two locus would contain the whole line and contradict regularity. The proper incidence projection is therefore quasi-finite, hence finite. The image of the support of relative differentials is then removed to obtain `U_red`. Each excluded set and its closed-image justification is stated before the theorem.

### 3. Finite base change in the unit-map argument

The general lemma splits the finite algebra after strict henselization and descends its idempotents to an étale neighbourhood. Finite base change identifies each residue algebra with the corresponding length-one fibre. The coherent cokernel of the unit map has zero fibre, so Nakayama gives a surjection after shrinking. This proves each incidence branch is a closed immersion using its algebra, not merely its point set.

### 4. Length versus reducedness

The new open is defined by the unramified finite incidence condition. A finite algebra over a complex geometric point is unramified precisely when it is a product of copies of the residue field. The proof separately notes that a length-one factor is reduced. It does not infer reducedness from an arbitrary higher length. The nonreduced slices retain length m explicitly and are treated by a different theorem.

### 5. Local Hilbert graph conventions

Immediately before `thm:multiple-incidence-v161`, the paper defines the reduced graph closure in `U_red x Hilb^{P_H}(CQ(V))`, its polarization and Hilbert polynomial, and its normalization. The slice object Gamma_m is defined separately before `thm:contact-hilbert-v161`. The latter is not assumed to be the normalization of an arbitrary base change of the global graph.

### 6. Actual Rees quotient

Equation `eq:rees-surjection-v161` displays `f^*(direct sum K^d) -> direct sum (K O_X)^d` as a graded surjection. The target is the image algebra inside `O_X[T]`. Its Proj supplies the closed embedding. The contact slice has the exact saturated kernel `(tU-x^mV)`; the multiple-incidence multi-Rees kernel is `(v_iU_i-u_iV_i)_i`. These are proofs of presentations, not inferences from a finite saturation computation.

### 7. Twists and coefficient maps

The first section retains the universal coefficient-map and twisting conventions. A degree-j power has the original `O(j)` twist on the pencil line; removing its common Cartier factor yields the graph system. In the contact calculation this original twist is trivial on the local Artin thickening, while the graph line bundle restricts to `O(delta_j)`. Equality of base ideals alone is not used to identify the full linear system; its coefficient span is computed separately.

### 8. Flatness

The new nodal and contact families are treated as relative Cartier hypersurfaces in smooth relative affine planes. Their defining equations remain nonzerodivisors on every fibre, giving flatness by the fibrewise Cartier criterion. The higher-contact chart is singular but flat; the smoothness of the parameter modification is not confused with smoothness of the universal curve.

### 9. Distinct Hilbert points

The exceptional map has image the line spanned by the tangent-normal vector and a chosen quotient direction. Its homogeneous ideal is the corresponding linear annihilator. Distinct quotient directions give distinct embedded closed lines, hence distinct Hilbert subschemes; tails over different incidence points are distinguishable by their ambient projection. In the thick-contact family, distinct support lines already distinguish the thickened closed subschemes. This establishes the finite-fibre claim needed for normalization.

### 10. Normalization localizes

The open restriction uses Stacks Project Section 29.55, Lemmas 29.55.3–4, with the localization statement identified explicitly. The nonreduced slice theorem intentionally avoids the stronger and unjustified assertion that normalization commutes with its nonflat slice restriction.

### 11. Scope of the modification

The former single-contact result is preserved in an appendix. The new main theorem is explicitly over `U_red`, a larger open allowing every number of reduced corank-two points. The quotient is called a modular modification over that open, not a proper compactification of all pencil moduli. The complete two-parameter nonreduced slices supply further computed boundary without claiming to cover every global complement.

### 12. Exceptional plane and parameter product

At each incidence the ambient exceptional fibre in complete quadrics is P^2. Its lines through the fixed tangent-normal point are parametrized by P^1. With k incidences the full parameter fibre is `(P^1)^k`; the universal curve has k one-dimensional tails. These three objects are named separately in the statements and introductions.

### 13. The full coefficient span

`cor:multi-powers-v161` expands the missing step: an ideal generated by degree-b coefficients has degree-b part equal to their linear span. In the binary residual ring that part is the determinant factor times all degree-delta forms. Removing that factor therefore gives the complete system. `thm:contact-hilbert-v161` extends the assertion over `C[x]/x^m`, using invertible congruence frames and a split unit-block socle injection; it is stronger than a check on reduced points.

### 14. Precise stack home

`prop:envelope-stack-v161` defines the target stack of pairs consisting of a projective source bundle and its finite graded algebra bundle with power diagram. The source is the fppf stack obtained after dividing out the nonlinear tangent-identity kernel and the ineffective right factor, as in the retained stack-equivalence theorem. It is equivalent to `[G/PGL(V)]`, not to a stack of all length-matched Artin algebras. The associated-bundle construction handles Brauer-nonsplit sources without a global O(1).

### 15. The distinguished exponent

The statements and both introductions foreground h=1. Larger h gives an additional chosen exponent with the same underlying projective graph. At h=1 the incidence is cut out by the fixed power `J_(n-1)`, and no further integer choice is needed.

### 16. No fictitious subquotient

The envelope is consistently described as an algebra bundle constructed from the recovered source. It is not asserted to be contained in, or a quotient of, the original finite algebra. The native source remains distinct from the auxiliary reciprocal coefficient complement.

### 17. Rees recovery now includes equations

The paper does not count the definition `direct sum I^d` as another independent theorem. It computes the entire local multi-Rees presentation, its absence of additional torsion, and the diagonal algebra. For nonreduced contacts it computes the relation `tU-x^mV`, normalization charts, singularity and local cotangent module. These are concrete structural data beyond taking formal powers of a known ideal.

### 18. Deformation functor

Before `prop:relative-obstructions-v161`, a deformation is defined over a local Artin complex base with identified closed fibre, and a source framing identifies it with a point of the completed effective pencil image. Boundary deformations include a lift of the boundary point. The proposition gives necessary and sufficient lifting conditions for a fixed square-zero base extension, and the torsor of choices. It distinguishes this from the smooth absolute quotient-stack deformation problem.

### 19. Nonlinear generators over dual numbers

The proof works explicitly over `C[epsilon]/epsilon^2`: substituting a quadratic-or-higher generator term into a degree-d sharp relation produces generator degree at least d+1 and therefore vanishes in the sharp truncation. This filtration calculation is separate from powers of epsilon. The surviving degree-d action is exactly the linear one. Hence an ineffective generator change is not confused with a genuine first-order pencil deformation.

### 20. Accessible symmetric classification theorem

The full primary preprint by De Terán, Dmytryshyn and Dopico, arXiv:1808.03118, was inspected at Theorem 2.1 and its preceding explicit blocks. It supplies the accessible theorem-level congruence classification requested by the report. The paper retains Thompson's classical attribution, and does not pretend that bibliographic access to Thompson was a new proof audit.

### 21. Finite Toeplitz range

The accessible theorem displays a minimal-index block of size `2 epsilon + 1`. Thus epsilon cannot exceed `floor((n-1)/2)` in dimension n. This explains the finite range rather than leaving it implicit. The retained nullity and second-difference formulas then recover all multiplicities.

### 22. Positions as well as partitions

The complete pencil data are the projective spectral points with their local exponent partitions, together with minimal indices for the singular part. Equivalence uses one common projective reparametrization of the pencil line. A list of local Smith partitions without point positions is not described as complete.

### 23. Ordinary versus arbitrary collisions

The earlier theorem is retained with its ordinary transverse and squarefree residual hypotheses. The new arbitrary-order contact result is a separately specified Jordan-slice theorem and does not rename the ordinary-collision theorem as an arbitrary-collision theorem.

### 24. What lies beyond v160 tangencies

The new family has original intersection scheme length m and Smith exponents m,m for every m >= 2. Its Hilbert tail is nonreduced and its total graph has an A_(m-1) singularity. This is distinct from the old reduced-incidence family whose residual line happens to be tangent to a determinant conic. Both results remain present, with different hypotheses.

### 25. Strict-transform and incidence literature

The revised introduction compares the arrangement part with Li's Theorems 1.2–1.3, the image-Rees/strict-transform step with Stacks Project Tag 080C, and the stable-map/tangency object with Gathmann's Theorem 7.1. `LITERATURE_AUDIT_V161.md` records the inspected primary passages and also distinguishes the recent logarithmic Hilbert scheme of points on a pointed curve from our embedded pencil-curve Hilbert graph. The general arrangement or stable-map machinery is not claimed as new. No exhaustive nonanticipation certificate is inferred from this search.

### 26. Boundary invariants beyond the simple open

The full double-incidence fibre is a smooth P^1 x P^1 with its explicit Chow ring and independent nodal parameters. For every m >= 2, the nonreduced slice yields a thick tail of multiplicity m, a length-m attachment, a transverse A_(m-1) graph singularity, local T1 dimension m-1, an explicit resolution chain, and a degree-m stable-map tail after ramified base change. These are written general calculations, not extrapolations from tests.

### 27. Is the pencil line essential?

Yes. The incidence ideal is intrinsic to the effective family with its recovered pencil line. The revision explicitly retains that intermediate object. It does not assert that the original multiplication supplies a preferred boundary direction or an unproved internal subquotient before reconstruction. The positive additional result is the exact modular, Rees and relative deformation description once these intrinsic recovered objects are specified.

### 28. Ballico limitation in both papers

The 1993 theorem/proof text is still unavailable through the legitimate route checked. The limitation is stated in both submitted introductions. The separately accessible 1996 paper was inspected at Theorem 0.2 and compared on its actual existence-of-failure-subschemes statement. It is not substituted for the missing 1993 text. No broad historical priority conclusion is claimed.

### 29. Finite checks and proofs

The new exact suite audits symmetric Jordan Schur complements, full submaximal minors in small dimensions, multi-Rees elimination, Fitting products, thick-fibre ideals, Jacobian quotients, ramified normalization charts, degree identities and Artin lifting equations. The inherited v160 chain is actually invoked in the full run. These checks are explicitly finite and separate from the written proofs. They are not used to establish a universal theorem or an editorial verdict.

### 30. Focus of Paper I

Its main text is now the seven-section sharp inverse route. The source-envelope and boundary applications, all covering and rigidification extensions, and all detailed historical mathematical blocks are in complete appendices. Paper II likewise has a six-section main route ending in the multiple-incidence and higher-contact theorems, with all prior extensions retained afterwards. The unified master and preservation audit retain every predecessor label and mathematical block. Focus is achieved by a reading hierarchy, not by arbitrary deletion.

## Validation and limits of the claims

The build pins the complete v160 master and rejects any missing label or mathematical environment block. Both independently compiling papers embed their stable numerical cross-references; the preservation master is not a third submission. The publication receipt distinguishes authored input from the following materialization commit. The remote branch and complete output objects are read back after publication.

The principal new result exhausts the normalized Hilbert boundary over the full reduced corank-two open. The nonreduced result exhausts each displayed two-parameter Jordan slice, but is not a classification of the whole ambient fibre at a general nonreduced or higher-corank pencil. The effective-stack application specifies its rigidifications and deformation category. The original all-pencil reconstruction and singular-pencil invariant statements retain their full scopes. Historical priority beyond the inspected sources, the unavailable Ballico 1993 comparison, formal proof certification, and journal acceptance are not asserted.
