# Response to the referee on A2 revision 118

**Revised manuscript:** *Codimension bounds and primary structures in multiplication failure*  
**Author:** Qian Qi  
**Revision:** 119, September 22, 2026  
**Controlling report:** `review/a2-v118-independent-harsh-top4-2026-09-22`, commit `d4254d9b01405ad02c64d2ff591503d4cc7a6aa7`  
**Reviewed mathematical source:** `c87bfdad8d97e68637d269e656b46c4cce85551e`  
**Reviewed product:** `44bfc648ead008896a6981a7302a6d5ab8b21bb8`  
**Intended new branch:** `revision/a2-v119-codimension-primary-conductor-2026-09-22`

The report is an owner-requested, AI-assisted referee-style assessment, not a report commissioned by a journal. This response addresses its mathematical objections and does not represent an editorial decision or a certificate of acceptance.

## 1. What has changed

The revision supplies a new chain of results rather than enlarging a determinant exponent. A coefficient-ring codimension bound gives a degree-three presentation of the entire codimension-two failure scheme. A conductor incidence identifies its corank-one open with a relative Grassmannian over the rank-two quotient scheme, and describes its fibres over both codimension-two conductor strata. That incidence realizes explicit embedded primary rings on the full multigenerator failure scheme of a connected local algebra family. A general regularity-controlled conductor theorem then transports these rings to global section multiplication for arbitrary finite projective schemes in a specified degree range.

Every inherited theorem and equation label remains present. The complete manuscript retains the quadratic, polar, wall, unrestricted-hyperplane and statistical developments; no such result is removed to improve the narrative. The separate geometry edition contains the new proofs and all the previous primary-article results. Classical inputs are identified where used.

The one source-access item **E118.1 remains unresolved**. Neither a successful build nor the new mathematical results are used to infer priority over an unread source.

## 2. Item-by-item disposition

| Item | Revision and precise location | Status in this delivery |
|---|---|---|
| E118.1: Ballico 1993 theorem-level comparison | `LITERATURE_AUDIT.md`, Section 1; final paragraphs of `sec:finite-prior-comparison` | Open: complete article not obtained; no claim of non-anticipation |
| E118.2: separate the three schemes | Abstract, introduction, `thm:full-codimension-two`, equations `eq:full-codim-two-ideals` | Implemented; the full Fitt0 ideal and extreme-corank Fitt1 ideal are distinct |
| E118.3: full codimension-two failure geometry | `thm:codimension-stabilization`, `thm:full-codimension-two`, `prop:codim-two-incidence-fibres` | Full equations in degree three; exact corank-one normal form; proper incidence and conductor-stratum fibres proved |
| E118.4: non-Cartier nonreduced multigenerator family | `thm:embedded-multigenerator`, `cor:three-generator-embedded` | Connected arbitrary-order family with an explicit embedded primary component; separate three-generator member supplied |
| E118.5: connect conductor and nonreduced mechanisms | `eq:codim-two-incidence` to `eq:fork-local-ring`, then `cor:global-embedded-multigenerator` | One incidence transfers actual local rings; its boundary is organized by the conductor action |
| E118.6: general global transport | `thm:regularity-conductor`, `thm:relative-regularity-conductor` | Arbitrary zero-dimensional projective schemes and finite flat families under uniform regularity bounds |
| E118.7: formal cleanups | Quotient-flag statement; `lem:relative-cyclic-vector`; Schubert and moving-jet constructions in `thm:fat-primary`/`cor:global-fat-primary`; low-degree statements | Implemented explicitly; diagnostics kept separate from proofs |

“Implemented” means that the stated change and its proof are in the manuscript. It does not mean that an independent referee has approved the argument or its significance.

## 3. E118.2–E118.3: the full failure scheme, not only conductor flags

Let W contain 1 and have locally free quotient of rank r in B. The new stabilization theorem proves

`W^(r+1) = O[W]`

over the coefficient ring, including nonreduced bases. A fibrewise dimension-growth argument would not suffice. The proof instead compresses multiplication to B/W. The compressed matrices need not commute; their commutators land in the quadratic residual module. Adjacent interchanges in a word are therefore controlled modulo the lower residual filtration. Polarized Cayley–Hamilton, with r! invertible, proves stabilization.

In codimension two, choose a splitting B = W + M and let beta be the two-row quadratic residual matrix. If C_i are the compressed multiplication operators, set

`K = [beta | C_1 beta | ... | C_(d-2) beta]`.

For every m >= 3, the normalized multiplication cokernel is coker(K). The entire failure scheme is defined by I_2(K), while its extreme-corank subalgebra scheme T is defined by I_1(beta) = I_1(K). Thus the defining equation theorem applies also along T; it is not a theorem stated only after an exact-rank restriction.

On D minus |T| a quadratic pivot produces a hyperplane algebra E = W^2. The scheme is exactly the quadratic-generation open of the relative Grassmannian over Hilb^2(B). This identification holds on nonreduced test schemes. It gives the local rings and the cokernel line, not merely a bijection of points.

The full relative Grassmannian gives a proper incidence Z -> D, an isomorphism over this corank-one open and surjective on geometric points. Its fibres over the exact-action-rank strata of T connect to the previous quotient dichotomy:

- Rank-one action: the fibre is Hilb^2(Q) for a rank-three quotient algebra Q. It is the binary-cubic square condition on P(Q/O), and may be the entire projective line when that cubic is zero.
- Rank-two action: the fibre is Spec(C), where C is the quadratic algebra in the rank-four conductor quotient tower. It is a finite flat double cover, including its possible nonreduced structure.

The square condition in the rank-three case is necessary. Scalar invariance alone would incorrectly give P^1 for Q = C^3, whose actual fibre consists of three points. This distinction is made explicit in the proof and in the exact diagnostics.

### Scope retained precisely

We do not claim that every primary component along T has now been classified for every finite algebra. Nor do we claim that the proper incidence is automatically a normalization, a blow-up, or scheme-theoretically surjective. What is proved is an equation theorem for the whole D, an exact scheme isomorphism on its corank-one open, and the stated fibres over T. No density claim is made for components lying entirely in T.

## 4. E118.4: primary geometry beyond a determinant power

For every h >= 5 the connected local algebra

`B_h = C[x,y]/(x^2, xy, y^h)`

has length h+1 and embedding dimension two. On an entire open chart of Hilb^2(B_h), write y^2 = u y + v and x = b(y-u). Its quotient relations give the exact ideal

`I_h = (F_h, v F_(h-1), b v, b^2 u)`,

where F_1=1 and F_(j+1)=u F_j+v F_(j-1). The revision proves the irredundant primary decomposition

`I_h = (u,v) intersect (b^2, b v, F_h, v F_(h-1))`.

The associated primes are (u,v) and the embedded (b,u,v). The nilradical has index 2h-3. The displayed embedded primary quotient has length binomial(h,2)+h-1; the nilradical of the coefficient ring has dimension binomial(h,2)+h-3. The primary ideal for an embedded prime need not be uniquely determined; the theorem specifies the exact choice whose colength is computed.

This chart is then realized on the **full** codimension-two multiplication failure scheme, not on a test slice. At

`W_0 = <1,x,y^2,y^3,y^5,...,y^(h-1)>`,

one has W_0^2 equal to the conductor hyperplane, because (y^2)^2=y^4. The incidence theorem gives a genuine open neighbourhood with coordinate ring a localization of `(C[b,u,v]/I_h)[t_1,...,t_(h-2)]`. Its support has codimension h-3 >= 2 in the unital Grassmannian, so the scheme is non-Cartier. Both associated strata meet the chosen neighbourhood. A smooth unit cover gives the corresponding assertion for unrestricted generating planes.

For h=5 the embedded primary quotient has length 14 and the nilradical has dimension 12 and index 7. The equations depend on the higher contact coefficients and their interaction with b; this is not a change in the power of a fixed tangent determinant.

A second corollary uses `(C[x,y]/(x^2,y^2)) x C^s`, s >= 1, and gives actual `(s+2)`-generator charts with ideal `(ab,b^2)`. At s=1 this is a three-generator full failure scheme with an embedded component. This supplementary construction is distinguished from the connected arbitrary-order family, rather than presented as a substitute for it.

## 5. E118.5: one conductor incidence, rather than parallel computations

The new embedded schemes are obtained by applying the conductor incidence to an exact quotient-algebra chart. The relative Grassmannian description is what proves that its primary ring occurs on the ambient multigenerator failure scheme. The higher-defect conductor strata describe the exceptional fibres of that same incidence over T. The roles are deliberately separated: the rank-three/rank-four flags govern the boundary, while the hyperplane conductor identifies the corank-one local rings.

The global conductor theorem is then applied to the same B_h family. Thus the chain is: codimension stabilization; full Fitting presentation; conductor incidence; embedded local rings; global section-multiplication cokernels. No step is replaced by a finite numerical test.

## 6. E118.6: all finite projective schemes in a regularity range

Let I be the saturated homogeneous ideal of any nonempty zero-dimensional Z in P^e. Put r = reg(I) and s = reg(I^2), with the square interpreted as the **ordinary homogeneous ideal square**. The revision proves the comparison for

`n >= max(r, s-1)`.

Since the classical product-regularity theorem gives s <= 2r, the uniform sufficient range is `n >= 2r-1`. Sidman's Theorems 1.3 and 1.8 are cited for the regularity, saturation and square bounds; these are not claimed as new.

For any generating restricted series A and its inverse-image U, the proof establishes the strong kernel identity

`H^0(I_Z(n)) U^(m-1) = H^0(I_Z(mn))`, for every m >= 2.

Choose a section of U invertible on Z. Its multiplication fills the conormal layer using H^1(I_Z^2(t))=0. In the remaining ordinary-square layer, generation in degrees at most r gives `(I^2)_(t+n)=I_n I_t`; saturation in degree t+n identifies this with the needed sheaf sections. Iteration fills the entire kernel. The actual cokernels are then canonically identified by restriction.

For finite flat families with uniform geometric-fibre regularity bounds, restriction bundles commute with base change. The kernel-filling map is surjective on fibres and hence globally by Nakayama. This proves the arbitrary-base-change statement without assuming flatness of the doubled finite scheme or of a selected primary component.

The result includes mixed supports, nonmonomial schemes and finite flat deformations. The plane scheme `(X^2,XY,Y^h)` has reg(I)=h and reg(I^2)=2h; consequently it transports the new connected embedded family for n >= 2h-1. The sharp monomial fat-point theorem and its boundary counterexample remain present as a complementary result. Rank-specific sharpness is not claimed for every finite scheme.

## 7. E118.7 and Section 11 of the report

The abstract and introduction now distinguish the stable-image flag, the extreme-corank Fitting scheme and the full failure scheme. The quotient-flag theorem explicitly requires a quotient **algebra**, a unital subalgebra subbundle, a locally free quotient and the specified locally split action injection.

The cyclic-vector argument is isolated as `lem:relative-cyclic-vector`. For T = [[a,b],[c,d]], the principal opens D(c), D(b), D(c+d-a-b) and vectors (1,0), (0,1), (1,1) exhibit the invertible cyclic determinants and their base-change compatibility.

The fixed fat determinant is identified globally as the pullback of the standard Schubert divisor for K -> m/m^2. For moving support, the manuscript defines the infinitesimal diagonal algebra, the twisted jet module, its augmentation kernel and the determinant line map to `det(Omega^1_P tensor O(n))`. The lift space is correctly described as an affine-bundle torsor, not assumed to be a canonically split vector bundle.

Both low-degree statements say explicitly that the zero Fitting ideal defines the whole parameter space. Exact diagnostics remain in the evidence directory and carry explicit non-certification statements.

## 8. Preservation, reproducibility and limits

`evidence/PRESERVATION.json` records every inherited TeX source, its hashes, all 293 inherited labels and the absence of missing labels/files. The old v118 directory is untouched. `build.sh` compiles the complete manuscript, exports the needed cross-references and compiles the geometry and application editions. It never reruns an authoring script over the revised sources.

`verify_revision.py` checks exact primary intersections and nilpotency for h=5,...,9; a nonreduced quotient chart with all its nonduplicate two-minors at specified Grassmannian coordinates; quadratic and cubic image ranks and ordinary-square staircases; the noncommuting compressed-matrix identity; and the inherited fat-point and action-rank regressions. They detect finite regressions but do not establish the general theorems or priority.

The manuscript has been revised substantively for renewed independent mathematical review. No statement here predicts a top-four editorial decision. The general primary classification along the extreme-corank locus remains distinct from the results proved, and the full-text Ballico 1993 comparison remains an explicit open scholarly obligation.

## Delivery status

This session could read the connected repository and download its source-bound build artifact, but supplied no repository-write action. The terminal could not resolve GitHub. The new source, PDFs, response and exact-diagnostic package are delivered locally with an application script and Git patch for the named new branch. **No remote branch creation or push is claimed.** The application script starts from the pinned R118 review commit and changes only the new v119 directory and its new root index.
