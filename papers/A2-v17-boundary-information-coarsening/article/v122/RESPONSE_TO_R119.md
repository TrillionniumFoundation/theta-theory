# Response to the A2 v119 Round-3 referee

Manuscript: **Conductor boundaries and primary structures in multiplication failure**, revision 120.

Controlling report: `reviews/a2-v119-independent-harsh-top4-r3-2026-09-22/REFEREE_REPORT.md`, frozen at `b409ec5eb4dfbb75850d90bff69a78604d3a512b`.
Reviewed mathematical source: `59437d7eb88b4791769eaf856bb6dd0f9c6c3a2b`.
New branch: `revision/a2-v120-loewy-boundary-primary-2026-09-22`.

The report distinguishes exact equations for the full failure scheme from its primary geometry along the subalgebra boundary. We agree with that mathematical distinction and respond by proving a boundary classification for an entire Hilbert-function class. No earlier theorem is withdrawn. All inherited mathematical part files are retained byte-for-byte in the active complete manuscript; the frozen v119 source is also preserved independently for the build audit.

## E119.2 and E119.3: full boundary geometry and a structural class

**Response: new theorems and full proofs in `parts/03c-loewy-boundary-primary.tex`.**

First, for every split augmented algebra `B=O+V+S_2` with augmentation cube zero, multiplication is determined by `gamma: Sym^2 V -> S_2`. On the full frame space of unital `(dim V+1)`-planes, let `M` be the tangent matrix and `H` the higher-layer coefficients. The complete multiplication presentation gives

`Fitt_0 = (det M) I_q(gamma Sym^2 M)`.

The identity retains all higher-layer frame coordinates and holds before taking a radical or deleting the extreme-corank locus. It is valid after arbitrary coefficient-ring substitution. This is the structural factorization, not a primary-decomposition claim for arbitrary `gamma`.

We then resolve it for **every complex local algebra with Hilbert function `(1,2,2)`**, not just a chosen test family. Its quadratic relation is either a square or a product of independent factors. These are the only isomorphism types because the augmentation cube is zero. Put `delta=ad-bc`, `P=(a,c)`, `Q=(b,d)` and `n=P+Q`.

For the square type the full ideal is

`I_sq = delta^2 P^2 = (delta^2) intersect P^4`.

Its associated primes are `(delta)` and the embedded prime `P`. We also determine every ordinary power: `I_sq^j = (delta^(2j)) intersect P^(4j)`.

For the two-factor type put `J=(ab,ad+bc,cd)`, `Q_0=J+P^2+Q^2` and `Q_*=delta^2 Q_0+n^7`. Then

`I_tf = delta^2 J = (delta^2) intersect P^3 intersect Q^3 intersect Q_*`.

All four components are necessary; the associated primes are `(delta), P, Q, n`. The last three are embedded. The proof supplies the primary nature of each displayed ideal, the colon identities, and explicit nonzero annihilator classes. Polynomial extension by the free `H` variables, localization to the frame open, and descent to the Grassmannian are justified. Thus these are local rings of the **whole** failure scheme, not transverse slices or corank-one charts.

The reduced support is an integral normal determinant divisor with one singular point, generic multiplicity two, and exact nilradical index four in both types. The factor lines of the quadratic relation index embedded projective planes. A double factor gives an embedded surface lying entirely in the extreme-corank locus. Distinct factors give two embedded surfaces and an additional embedded point at the quadratic layer. This directly answers the request for associated primes supported in the boundary.

The conductor theorem identifies, on the exact tangent-rank-one locus, the subalgebra equation `gamma(L^2)=0 in S_2/H_0` and the actual kernel

`cond_B(W) = ker(K -> Hom(V,S_2/H_0))`.

It specifies action-rank-one and action-rank-two strata, their base-change behavior, and their position on the primary components. Numerical action rank alone is insufficient: the quadratic relation is essential structural data. This is a positive conductor-to-primary statement for a complete natural class, not a claim that numerical conductor ranks classify every finite algebra.

Finally the free rank-five algebra family with relation `y^2=tau xy` has the exact full failure ideal

`delta^2 (a(a+tau b), 2ac+tau(ad+bc), c(c+tau d))`.

Its square and distinct-factor fibres realize both classifications in one fixed-Hilbert-function family. We do not assume that the failure family is flat or that a chosen embedded primary representative commutes with specialization. For the corresponding projective schemes the regularity is three, so the complete boundary classification transports to global section multiplication for `n>=5` and every symmetric degree at least two.

This resolves E119.2--E119.3 in the stated complete class. It does not claim a global primary classification for all finite algebras or identify the general proper incidence with a normalization. The broader presentation and incidence results of v119 remain unchanged.

## E119.4: optimality and algebra length

**Response: Proposition `prop:codimension-sharpness`, `parts/01e-length-sharpness.tex`.**

For every `r>=1` and `k>=2` we construct a connected local algebra of dimension `r+k` with a unital `k`-plane whose product length is exactly `r+1`:

`B=C[z,epsilon_1,...,epsilon_(k-2)]/(z^(r+2), z epsilon_i, epsilon_i epsilon_j)`.

Take `W=span(1,z,epsilon_i)`. The basis of `W^j` is written explicitly for every `1<=j<=r+1`, and `z^(r+1)` witnesses strictness at the last step. Thus the universal codimension bound is optimal even at fixed generating rank.

The field-level dimension argument is classical and is now proved and explicitly separated from the coefficient-ring statement. Pappacena and Markova are added as algebra-length context; no unverified specialized numerical estimate from those works is used. The relative theorem's role is equality of image submodules and stability of Fitting ideals over nonreduced coefficient rings, not a claim to invent the field dimension count.

## E119.6: relative precision

**Response: expanded proofs in `parts/02l-relative-incidence.tex` and `parts/01f-relative-cohomology.tex`.**

For the rank-two incidence fibre we give both constructions on every test scheme: a character of `C` defines `I=ker chi`, the line subbundle `IM`, and its hyperplane-algebra inverse image; conversely the quotient line defines the character and recovers `IM`. The line-bundle isomorphisms, multiplicative closure and arbitrary-pullback compatibility are all proved. The notation `D minus |T|` is defined as the open complement of the support.

For relative transport, restriction is proved surjective from degree `max(0,r-1)`. Its kernel is locally free and the restriction sequence locally split. All higher direct images vanish in that range. The proof gives the same exact sequence after arbitrary base change. The ordinary-square regularity bound is used on geometric fibres only; no flatness or base-change assertion about the square ideal or conormal module is silently assumed. The kernel-filling map is a morphism of vector bundles with zero coherent cokernel and stays surjective under any pullback.

## E119.5: actual source and reproducible products

**Response: materialized new source, vendored checks, isolated branch build.**

The missing v118 verifier is now physically present at `inherited-v118/verify_revision.py`. The runner imports all four mathematical v119 check groups, all three v118 groups, and the new primary/deformation/sharpness tests. It does not catch a missing dependency and skip its tests. Preservation is checked against the complete vendored frozen v119 source, not a stale nominal version number.

The canonical build compiles the complete manuscript, geometry article and application appendices. The source manifest records every TeX/Python/shell input, exact diagnostic output and PDF hashes. Source and product commits are distinct, and the publication pointer is written after the product commit to avoid a self-referential hash. The workflow refuses to overwrite concurrent work and verifies that no earlier revision or report was modified. Actual success must be read from the run conclusion and `evidence/BUILD_RECEIPT.json` / `evidence/PUBLISHED.json`; this response is not itself a claim that an unexecuted build passed.

## E119.7: role in the theta-theory sequence

**Response: `DEPENDENCY_MAP.md` and the article's logical-dependencies subsection.**

The current finite-algebra core is self-contained: it has no unstated dependency on an A1 theorem. Its interfaces for later applications are the canonical global/finite cokernel comparison, Fitting ideals, exact-action conductor flags and primary boundary structures. A downstream manuscript must verify the hypotheses of whichever interface it uses. The note distinguishes available results from a verified citation by a specific later manuscript; it does not invent an A3 dependency. All historical polar, residual, wall and statistical sections are retained as complementary results, not retroactively made premises of the new algebraic core.

## E119.1: source comparison and remaining limitation

**Response: strengthened comparison, but the complete Ballico item remains unverified.**

The ABHS citation is updated to its published 2023 version. The comparison explicitly acknowledges both the closed non-monogenerator index-form scheme and the polygenerator maximal-minor construction; it no longer treats that literature merely as representability of an open. The algebra-length context is added, and Sidman's ordinary-product regularity theorem is identified as a classical input rather than a new assertion.

The complete theorem text of Ballico 1993 was not obtained from the checked publisher full-text/PDF routes. We therefore cannot supply a truthful theorem-by-theorem anticipation table. The audit records each requested comparison dimension as unverified, rather than inferring disjointness from a title or access failure. E119.1 is **not marked closed**. The new proofs and the stated boundary classification are delivered without certifying exhaustive priority or a top-four editorial outcome.

## Preservation and review order

Read the boundary roadmap, the quadratic-layer and full primary theorems, the conductor-kernel theorem and collision family, then the sharpness proposition and relative proofs. All inherited mathematical part files and labels are checked automatically against the frozen source. The complete manuscript retains the previous results and appendices; the new geometry is additive. Finite computer checks corroborate explicit identities but do not replace the written proofs or the next independent referee review.
