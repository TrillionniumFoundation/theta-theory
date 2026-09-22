# Response to the independent referee of A2 revision 113

Controlling report: `reviews/a2-v113-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md`, commit `63daaeee1da5a1ee3ac569584e06f55081073da0`.
Reviewed mathematical source: `c604b9d444db281ea8d662cd15e9bc7822ad55df`; reviewed evidence head: `f352be19dd524a6c5ff640289cd00b4bf87049e1`.
New branch: `revision/a2-v114-global-residual-singularities-2026-09-22`.
Principal manuscript: `paper.tex`, **Residual geometry and singularities of multiplication failure schemes**.

We thank the referee for distinguishing the advances of revision 113 from its remaining proof obligations. This revision keeps the all-dimensional component theorem, every exceptional case, the wall normal form, the higher-product phase theorem, and the full information/statistical developments. It does not replace those statements with conjectures or a venue-based negative conclusion. The new central result is a global singularity and cotangent-Fitting theorem for arbitrary symmetric linear systems, specialized back to every annihilator rank of the binary problem.

The statements and proofs below are submitted for independent verification. The word “supplied” identifies a proof now present in the manuscript; it is not a claim that a referee has certified it. The final section separates the work supplied from the priority question and global analytic classifications not established here.

## 1. Sections 4 and 9: a general theorem beyond quadratic binary multiplication

**Theorem 2.1 (`thm:polar-tangent`)** treats an arbitrary linear map `beta: Sym^m V -> F`, with arbitrary `m >= 2` and potentially different contact dimensions. At an annihilator, let `B` be the derivative in the Grassmannian directions, let `Q = ker B*`, and let `tau = mu|Q`. The incidence tangent sequence and dimension formula are proved directly:

`0 -> ker B -> T incidence -> (mu Q)^perp / C ell -> 0`,

`dim T incidence = M - (e-p+1) + dim ker tau`.

For quadratics, the proof identifies `Q` with the direct sum of the symmetric squares of the intersections with the radical. This identification does not use binary forms. For higher products, the polar kernel is the correct object; no unsupported identification with a quadratic radical is imposed.

**Theorem 2.2 (`thm:global-polar-singularities`)** then determines the full singular support whenever the maximal-minor scheme has pure expected codimension. It also identifies the pullbacks of all cotangent Fitting ideals on constant-rank polar strata. Examples include section multiplication on arbitrary projective varieties and multivariate polynomial systems. The expected-codimension assumption is explicit; it is not asserted automatically for those examples.

The two-point phase calculation remains a concrete calculation inside this general theory. We have not represented it as a full enumeration of higher-product components. Its statement, rationality conclusion and count are retained.

## 2. Sections 5.1–5.2 and 12B: a global singularity statement

The new global theorem says that, in expected codimension, the full singular support consists exactly of:

- original multiplication corank at least two;
- original corank one with a noninjective polar residual map.

The first part follows because all maximal minors vanish to order at least two on an appropriate Schur chart. The second is an equality of tangent dimension and actual local dimension, not an inference from membership in one selected component.

The stronger scheme assertion is equation `eq:global-fitting-recursion`. If `d=M-a`, `h=rank Q`, and `T` is a constant-rank polar stratum in the original corank-one locus, then

`Fitt_(d+j-1)(Omega_D) O_T = I_(h-j+1)(tau)` for every `j >= 1`.

The proof splits an invertible block of the plane derivative in the actual cotangent presentation. After eliminating that block the remaining map is the dual residual multiplication. Fitting ideals commute with base change and are unchanged by the transition matrices. The statement concerns the pullback of the singular scheme of `D`, not the intrinsic singular scheme of `T` and not a product neighbourhood transverse to `T`.

To specify the full scheme, including the infinitesimal structure across changes of polar rank, equation `eq:schur-singular-scheme` gives open-chart Schur–Jacobian presentations at **every** original corank `rho >= 1`. We do not infer global scheme structure from restrictions to locally closed strata alone.

**Corollary 2.3 (`cor:global-binary-singularities`)** specializes this theorem to all quadratic binary annihilator ranks when `a <= b`. It does not impose distinct support or uniqueness of a signed family. Thus colliding-support points and simultaneous-component intersections are covered by the singularity criterion, although their individual analytic types need not be nodes.

**Corollary 2.4 (`cor:whole-residual-wall`)** identifies the entire residual rank stratification on the original corank-one signed wall. The singular ideal is the residual determinant ideal, and higher tangent-excess ideals are the corresponding smaller minors. This applies at every residual corank, including the complement of the node open set.

This is the global statement we have chosen to prove. It is not advertised as a global normalization/conductor theorem or a classification of every analytic germ. The original node theorem remains an additional, more precise local-type theorem on its stated nonempty dense open.

## 3. Section 5.3: the excess regime

**Proposition 2.5 (`prop:excess-polar`)** gives the exact residual Fitting formula without assuming expected codimension:

`Fitt_(M-t)(Omega_D) O_T = I_(h-a+t)(tau)`.

Where the actual local dimension is `M-t`, smoothness is equivalent to `dim ker tau = a-t`. At every corank-one point lying on a maximal-dimensional component in the binary excess regime, the full local scheme has dimension `M-b`; one may therefore take `t=b` even when smaller components also pass through the point.

This adds a local scheme-level criterion in the excess range. It does not turn the existing maximal-dimensional component classification into an unproved enumeration of every smaller component or every associated prime. The fixed-annihilator embedded prime remains explicitly distinguished from an embedded prime of the global excess scheme.

## 4. Sections 6.1–6.2: orientation descent and the exceptional cases

**Proposition 5.1 (`prop:orientation-descent`)** specifies the orientation double cover of a line-valued nondegenerate quadratic bundle, including its frame-change rule. It describes the two geometric maximal-isotropic families, the determinant character of their interchange, their irreducibility, and the descent of their products.

An important distinction is made explicit: for `L` maximal-isotropic factors a connected orientation cover gives `2^(L-1)` descended components, not automatically one. The cases where the component theorem needs irreducibility have `L=1`.

**Proposition 5.2 (`prop:exceptional-orientation-base`)** gives the precise ordered affine support/nonzero-weight chart, normalized by `alpha_r=1`; the relevant function field; the valuation proving nonsquareness; the cover; and the unordered quotient argument. The radical recovers the support polynomial, and a Vandermonde system recovers the weights. Irreducibility of the ordered incidence therefore gives irreducibility of its image and closure, rather than an unexplained appeal to monodromy.

The `(7,14,1)` case is handled separately. The proof explains why the universal Hankel determinant has a simple prime corank-one divisor and why even rank makes the discriminant square class projectively well defined. This formally supplies the descent used in the all-dimensional component proof.

## 5. Sections 6.3–6.5: the wall proof package

**Proposition 7.4 (`prop:relative-residual-divisor`)** constructs the support line bundle `G`, the radical bundle `R=G tensor V_(n-2)`, and the residual target `T=G^2 tensor V_(2n-4)`. On the relative Grassmannian product it specifies the determinant line

`det T tensor (det direct-sum Sym^2 W_nu)^(-1)`.

Local trivializations identify its zero scheme with a product with the already proved integral residual determinant divisor. The proof gives the global irreducibility, reducedness and Cartier arguments, and then pulls this divisor back along the affine lift torsor.

**Proposition 7.5 (`prop:normal-block-factorization`)** gives the exact normal-bundle sequence. Its plane-normal block is an isomorphism onto the kernel of restriction of the equation bundle to the residual source. The quotient block is the dual residual multiplication, with the annihilator-line twist. The determinant identity is consequently an identity of determinant lines; after taking local frames it differs by a unit. Its compatibility under changes of splitting and frame is proved explicitly.

**Lemma 7.6 (`lem:wall-open-nonempty`)** supplies the simultaneous nonemptiness. It first proves the hyperplane-containment codimension bound on the residual orthogonal Grassmannian, excludes the pencil of bad evaluation hyperplanes, and intersects the resulting open with the known corank-one open in an irreducible incidence. It then varies an actual affine lift parameter to fill the missing residual direction. The functional used for this variation is shown to vanish on redundant frame changes, so the argument takes place on the lift torsor itself.

The node theorem is retained as **Theorem 7.7 (`thm:wall-node`)**. Its proof now explicitly invokes these three results. The analytic equation and the completed local-ring assertion remain separate. The conductor and logarithmic conditioning conclusions are retained.

## 6. Section 6.6: algebraic phase descent

**Proposition 8.1 (`prop:algebraic-phase-descent`)** replaces the loop-based justification with a finite etale cover. On the dense affine support chart the cover has coordinates `(x,y,t)` with `x != y`, `t != 0`. Its deck group is generated by `(x,y,t) -> (x,y,zeta t)` and `(x,y,t) -> (y,x,t^(-1))`, with the dihedral relation.

The proof identifies the quotient with the two-point annihilator base, proves that this is the entire deck group, descends the integral relative Grassmannian components by its orbits, and treats stabilizers explicitly. An inversion-fixed relative sector does not split merely because its stabilizer is nontrivial. The original orbit formula and rationality proof are preserved.

## 7. Section 6.7: explicit fibre algebra

**Proposition 7.3 (`prop:fibre-primary-decomposition`)** supplements the original fibre calculation with the irredundant decomposition, for `c >= 2`,

`J_c = (a_1,...,a_c) intersect (b_1,...,b_c) intersect (J_c + m^3)`.

The proof verifies the identity degree by degree using the vanishing of mixed cubics. It proves that the last ideal is maximal-primary and supplies witnesses for irredundancy. The Hilbert series is

`2/(1-t)^c - 1 + binom(c,2)t^2`.

This proves the asserted list of associated primes independently of a finite diagnostic. The `c=1` reduced case is also identified.

## 8. Sections 7 and 12D: primary-source comparison

Section 9 of the manuscript now contains a result-by-result comparison table and explicitly distinguishes classical inputs from the statements proved here. The current primary-source work rechecked the full Ballico 1996 article, including Theorem 0.2 and Proposition 2.2, the Hankel determinantal discussion of Conca–Mostafazadehfard–Singh–Varbaro, and the exact Stacks reducedness lemma.

For **Ballico 1993**, the publisher's actual first-page image was inspected, beyond bibliographic confirmation. Pages 6–13 and their theorem statements were not obtained from the accessible primary text. Neither the paper nor this response claims a completed theorem-level nonoverlap comparison. This request is therefore **partially addressed, not closed**. `LITERATURE_AUDIT.md` records the exact checked material and retrieval limitation. No inaccessible theorem statement has been guessed or attributed to that paper.

## 9. Sections 8, 10 and 11: organization and minor corrections

The principal article now begins with multiplication failure and the general residual theorem. The component and singularity arguments precede the information application. All native, contact, statistical, finite-precision and finite-sample arguments remain in the same manuscript's appendices, not an omitted or promised companion manuscript. The stable-range proof is also preserved.

The reference to the reducedness criterion now uses **Stacks Tag 031R, Lemma 10.157.3**. The signed-normalization heading specifies same-annihilator intersections over the split rank-two base. Every excess summary retains “maximal-dimensional.” No numerical diagnostic is cited as a proof of a universal theorem.

The preservation checks retain all **134** old labels and all **25** old bibliography keys. The revised source has **169** labels. Six substantive inherited parts are byte-for-byte unchanged. The relocated introductory codimension theorem has the same statement and label. The new source, PDF and diagnostics are bound together by repository receipts.

## 10. Status for renewed review

This is a substantive new mathematical manuscript with a general residual theorem, a full expected-codimension singular-support theorem, precise Fitting identities, and the requested standalone descent and wall proofs. No existing principal theorem has been replaced by a no-go statement or weakened to avoid its proof.

The remaining limits are stated rather than silently promoted into conclusions: the Ballico 1993 theorem-level priority comparison is incomplete; all excess associated primes and every smaller excess component are not classified; and global normalization/conductor data and every local analytic type are not asserted. The new global singularity theorem is not a claim that these different classifications are equivalent. The revision is ready to be read and tested by another referee; mathematical correctness, novelty, author approval and venue suitability still require their own assessments.
