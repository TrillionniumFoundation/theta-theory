# Response to the independent report on A2 revision 122

**Revision 123: Polarized ramification and higher-corank structure in multiplication failure**  
Qian Qi · 23 September 2026

## Identity and object of this response

This response addresses the 23 September report in `review/a2-v122-independent-harsh-top4-2026-09-23`, commit `14dcc67aced0a92d178ba7fd688b0c8b54111aad`. The report's principal reading object was the 63-page v122 geometry article. The revision retains its entire 130-page complete mathematical companion and all editable sources. It does not represent the owner-requested, AI-assisted external-referee-style report as a report commissioned by any journal.

The new principal article has 16 pages. Its proofs are organized by their mathematical dependencies rather than by the chronology of previous revisions. References below use the new article's numbers; historical labels and pages remain unchanged in the archival portion of the complete companion.

## Principal changes

The revised argument makes three substantive additions. First, it reconstructs the **quartic polarization**, not only the abstract K3. Second, it proves that the actual polarized ramification surfaces have a **nine-dimensional moduli image**, with generically finite ambiguity for relation spaces up to projective equivalence. Third, it calculates the fixed-tensor primary ideal on a nonempty open part of **projection corank two**, including a new embedded associated support and a nilradical of index three.

These changes do not rely on a claimed specialization of a generic primary decomposition. The finite certificates verify the explicit examples and rank calculations used in the proofs; they do not certify all of the general proofs or resolve priority.

## B1 and E122.1 — Ballico 1993

**Status: the full-text documentary comparison remains outstanding.** The complete text of *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102, was not obtained through the accessible lawful sources. The publisher record and later citations do not establish its precise theorem statements.

The introduction therefore continues to disclose this limitation. `LITERATURE_AUDIT.md` records the source actually inspected and preserves the referee's nine comparison axes: parameter Grassmannian; complete versus incomplete series; multiplication map; scheme/cycle/Fitting structure; moving versus fixed contacts; embedded components; conductor or quotient-algebra mechanism; higher-order embedding/jet conditions; and global hypotheses and degree ranges. None is filled with an inference from the title.

The revision makes no claim that this source anticipates the new results, and no claim that it does not. `priority_certified` remains false. Strengthening the mathematics is not offered as a substitute for reading that text. The separate determinantal part of E122.1 is addressed below.

## B2 and E122.2 — the first higher-corank stratum

**New result:** Theorem 1.3, proved in §6, crosses projection corank two for a fixed relation tensor. Definition 6.1 specifies admissible pairs `(R,H)`: the restriction to `Sym²H` is injective, the quotient mixed map is surjective with a rank-two kernel tensor, and the pencil of hyperplanes containing `H` meets the ramification quartic in four distinct points. Lemma 6.2 proves that these pairs form a nonempty open. For every `R` in its nonempty open image, the admissible `H` form a dense open in `Gr(2,V)`.

After Gaussian elimination and quotienting the three independent quadratic columns, the exact residual matrix is `[L(T), C Sym²T]`, where `T` is a general 2-by-2 transverse matrix and `C` depends only on smooth auxiliary parameters. No leading-term approximation is used. The determinant divisor has equation `δ=ad−bc`. Let `m=(a,b,c,d)` and let `P_i` be the four plane ideals determined by the simple ramification lines after an étale root splitting. The calculation proves

```
J = I_3[L(T), C Sym²T]
  = (intersection_i P_i) intersection m³,
I_Dhat = δJ = (δ) intersection P_1² intersection ... intersection P_4² intersection m⁵.
```

All components in the displayed intersection are primary and the intersection is irredundant. The rank-two stratum is an additional associated support. If `Nhat` denotes the nilradical, then `Nhat³=0`, `Nhat²≠0`, and the annihilator of `Nhat²` is exactly the ideal of that stratum in the failure ring. Its transverse length is one.

This directly answers the objection that codimension cannot justify ignoring embedded structure: the first higher-corank calculation actually produces new embedded structure. The main text does not claim that the exceptional non-admissible part of corank two or corank at least three has been classified. The four root branches are étale-local branches; monodromy need not give four globally distinct irreducible components.

Independently, Proposition 3.1 identifies the whole failure scheme's reduction and its intrinsic smooth locus. Thus the reconstruction theorem is now explicitly a theorem about abstract isomorphisms of the failure scheme on **all** of `X_R`, even though the primary stratification theorem has the more limited stated scope.

## B3, E122.3, and M9 — actual K3 variation

**New result:** Theorem 1.2 and §5 replace the orbit-deficit argument by a computation of the differential of the actual Jacobian map. On the 24-dimensional Grassmannian chart, the quadrics are `q_i=x_i²+Σ_k C_ki m_k`. Their Jacobian determinant is `F_C`. At the explicit rational matrix `C_*`, the 35-by-25 coefficient matrix of `F` and its 24 parameter derivatives has a nonzero 25-by-25 minor:

```
4279473148893659522379284480  (residue 41 modulo 101).
```

This proves projective differential rank 24. The embedded image therefore has dimension 24 and the map is generically finite onto that image. A smooth quartic K3 has finite projective stabilizer, so quotienting its 15-dimensional projective-coordinate orbits gives an actual polarized K3 image of dimension `24−15=9`. This is not inferred from the dimension of the algebra parameter space alone.

The same witness lies in the smooth basepoint-free class: homogeneous Macaulay matrices of degrees five and nine have full row rank, certified by integral minors with nonzero residues modulo 101. The proof explains why these finite-field nonvanishing facts imply the asserted statements over `Q` and `C`.

The result gives more than one non-isotrivial pencil: it computes the image dimension of the full family. Corollary 5.3 supplies a flat family of failure schemes with that canonical polarized invariant. The earlier Hesse family and its nonconstant `j`-invariant are retained unchanged in the complete companion. The two cases are no longer parallel only at the level of an algebra orbit count.

The revision does not claim that a nine-dimensional web-of-quadrics family is historically new. Its role here is to prove genuine variation of the invariant extracted from the failure scheme.

## B4 and the determinantal part of E122.1 — classical primary theory

**New comparison:** Appendix A writes the De Concini–Eisenbud–Procesi order profile explicitly. For a product of minors of shape `ρ`, it states the classical symbolic-power intersection with exponents `γ_j(ρ)`. The inspected theorem source is Bruns–Conca, *Gröbner bases and determinantal ideals*, Proposition 2.2 and Theorem 2.4, printed pages 13–14 of arXiv:math/0302058. Their theorem supplies the characteristic-zero statement and its attribution to the classical theory. The audit does not pretend that the entire De Concini–Eisenbud–Procesi article or Bruns–Vetter monograph was independently reread.

The additional scalar is handled by an explicit coefficient rule:

```
Σ_u t^u f_u in (t,I_j)^(b)
iff f_u in I_j^(max(b−u,0)) for every u.
```

For coefficient degree `u≥1`, the retained weighted formula is exactly the one-factor classical profile with `k=q+1−u`. The appendix proves equality, primaryness, irredundancy, and the local nilradical order. This answers the referee's four questions as follows.

The special block `[A,tI]` is a scalar-identity substitution in a larger matrix, but substitution alone does not prove preservation of components or flatness. The required intersection **can** be recovered coefficientwise from the classical `γ` profile. The repeated scalar organizes the coefficient filtration; it is not advertised as a new straightening mechanism. The retained weighted identity is accordingly credited as a consequence, while its multiplication-failure interpretation and the independent fixed-tensor corank-two calculation are kept distinct.

This is a strengthened proof of the priority boundary, not a deletion of the old theorem. Its earlier full derivation remains in the archival companion.

## M1 and E122.4 — polarized reconstruction and finite tensor ambiguity

**New result:** Theorem 1.1 replaces the stable-birational conclusion by a graded section-ring reconstruction. The nilradical `N` and its annihilator scheme `E` are intrinsic to `D`. On `E`, form

```
L = ω_E tensor N^(-(p+e−1)).
```

The graph-bundle description and its relative cotangent sequence give two determinant-line identities. Their exponents cancel the projective socle direction and produce `L=ρ*O_Y(e)`. Lemma 4.1 proves `ρ_*O_E=O_Y`: a positive-degree polynomial section would have to be invariant under translations through every one-dimensional subspace of the socle, hence be constant. This eliminates the otherwise problematic extra functions in an affine-bundle total space.

It follows, compatibly with multiplication, that

```
⊕_n H⁰(E,L^n) = ⊕_n H⁰(Y,O_Y(en)).
```

Taking `Proj` reconstructs `(Y,O_Y(e))`. For a K3 the Picard group has no torsion; the supplied Riemann–Roch argument proves this particular fact. The fourth root is therefore unique, and the intrinsic data recover the actual quartic polarization and its projective model. This is not a polarization assumed to be preserved by the initial isomorphism.

Proposition 3.1 makes the corank-one restriction intrinsic inside the whole failure scheme, so an abstract isomorphism of whole failure schemes gives the same polarized reconstruction. Theorem 1.2 then yields finitely many possible algebra classes over a general polarized point. The revision does not assert a unique quadratic map, a unique algebra, or uniform finite fibres at exceptional points.

## M2 — ordinary powers

The power identities now appear as **Corollary 3.4**, following the normal-form theorem. Their complete local proofs, nilradical indices, generic multiplicities, torsion lengths, and arbitrary ordinary powers are retained. They are not presented as an independent source of depth comparable to the new reconstruction mechanism. All references to powers distinguish ideal powers from multiplication degrees.

## M3 — linear systems of quadrics and the classical incidence surface

Section 7 defines the common bilinear incidence surface

```
Z_R = {([x],[y]) in P(V*) × P(V*): q(x,y)=0 for every q in R}.
```

The constant-corank-one Jacobian gives a kernel line, proving that its projection identifies `Z_R` scheme-theoretically with `Y_R`. Symmetry gives an involution without fixed points; a fixed point would be a base point of the quadrics. This is compared directly with the web-of-quadrics construction recalled in Ingalls–Kuznetsov §4.

The target-web symmetroid `det(Σ λ_i A_i)=0` and the source Jacobian `det J_R(x)=0` are distinguished: they live in different projective spaces and have different displayed equations. The text does not assume they are the same embedded quartic. The new information is the polarization as an invariant of the multiplication scheme and the additional corank-two torsion, not the existence of the classical incidence K3, the free involution, or the notion of ramification.

## M4 — relative existence, Cartierness, and descent

Proposition 2.3 is rewritten as a relative-geometric proposition. It displays the tensor parameter `Hom(Sym²V,S)`, the universal matrix evaluation, the codimension-four and codimension-`e` incidences, their proper images, the auxiliary nonzero-determinant open, and the subsequent frame quotient to the Grassmannian of kernels.

The universal determinant is a relative effective Cartier divisor. Its flatness follows from the fibrewise injectivity of the line-bundle map and the fibrewise flatness criterion. The total smoothness, regular generic fibre in characteristic zero, and proper image of the nonsmooth locus give the smooth parameter open. The proof explains why the conditions and determinant ideal descend along the faithfully flat quotient-frame bundle. The auxiliary fixed-hyperplane condition is not silently added to the final definition of the class.

## M5 — coherent intrinsic torsion

Lemma 3.3 defines the generic torsion as the kernel of the sheaf morphism to the pushforward from `Spec O_{Z,η}`. It proves coherence, gluing, maximality among generically zero coherent submodules, and invariance under scheme isomorphisms. Corollary 3.4 identifies its annihilator with the full ordinary-power neighbourhood `E^[n]`. No embedded primary representative enters the definition.

## M6 — arbitrary base change

Lemma 3.5 isolates the smooth relative flag `E⊂Δ⊂U`. Its conormal and principal filtrations prove base flatness of both outer terms of the relevant extension. The proof displays the exact obstruction `Tor_1^A(O_U/L^n,A')` and its vanishing for every base algebra. The sequences defining the powers likewise remain exact, identifying the base-changed ideals rather than merely their supports. Corollary 3.6 applies the lemma to the universal family. Primaryness itself is checked on each complex fibre; no blanket primary-specialization theorem is invoked.

## M7 — an explicit member in the manuscript

Equation (5.2) gives all 24 coefficients of the four quadrics. Appendix B prints the four quadrics, all 35 coefficients of the quartic in a fixed monomial order, the complete matrix construction recipes, and the nonzero minors. The JSON files add the exact pivot row and column lists. Equations (6.1)–(6.2) give the same member's quotient matrices, kernel determinant `−7`, binary quartic, and discriminant `−632301/4`. The example is therefore visible in the paper, not only in diagnostics.

## M8 — MRC cancellation

Remark 4.4 places the preceding stable-birational argument in the language of maximal rationally connected quotients and cites Kollár, Chapter IV, §5. The full old cancellation proof remains in the archival companion. The new polarized reconstruction uses the section ring instead, so no strengthened conclusion is being extracted without justification from the old birational cancellation argument.

## Expository and minor points

The principal article now follows four main proof blocks: relative ramification; the Fitting normal form and intrinsic torsion; polarized reconstruction and actual moduli variation; and the new corank-two calculation. The classical comparison and finite certificates follow separately. All preceding mathematical parts and their labels survive in the complete companion and untouched v122 sources.

The notation distinguishes `D` on the corank-one open from `Dhat` on the whole Grassmannian. The whole-scheme reconstruction is proved rather than obtained by renaming `D`. Algebra moduli and K3 moduli are separated. The nilradical and its annihilator are introduced before choosing primary components. Ordinary powers are explicit. Classical determinantal sources appear at the symbolic-order calculation. Build and finite-computation receipts do not claim a general proof certificate.

## E122.1–E122.5: review disposition

E122.1 is partially addressed: the determinantal comparison is supplied, but the Ballico theorem-text comparison remains outstanding. E122.2 is addressed by a fixed-tensor theorem on a specified, proven nonempty open part of corank two; the remaining exceptional strata are not silently included. E122.3 is answered by the actual nine-dimensional polarized image calculation. E122.4 is answered by polarized reconstruction, with generic finite tensor ambiguity as a consequence. E122.5 is addressed by the global relative lemmas, the intrinsic torsion definition, the MRC positioning, and the explicit witness.

These are the claims submitted for the next independent mathematical review. No journal acceptance, exhaustive originality certification, or mechanized verification of all general proofs is asserted.

## Delivery and preservation

The source overlay contains only a new `article/v123/` directory and a new root reading index. It does not edit a previous manuscript, review branch, or other paper. The complete companion contains the new 16 pages, one explanatory leaf, and the exact 130 historical pages. The build receipt records the page-by-page text-preservation test as well as source and PDF hashes.

The packet was produced in the working container. A last repository read found the named revision ref still at the controlling review commit. No revision-source commit or PDF publication commit has been pushed by this execution environment. The included safe apply script is the integration mechanism for a connected checkout, not evidence that a remote write has already occurred.
