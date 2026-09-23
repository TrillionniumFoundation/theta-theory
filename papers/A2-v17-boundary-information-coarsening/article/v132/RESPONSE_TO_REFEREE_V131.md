# Response to the A2 revision-131 referee report

**Revision 132 — September 23, 2026**  
**Article:** *Intrinsic web reconstruction and primary boundary laws for multiplication-failure schemes*  
**Controlling report:** `reviews/a2-v131-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, frozen at `f0ac12d5ce2084fffec3a6245e3cbe8c2e2b39ff`.  
**New branch:** `revision/a2-v132-galois-descent-higher-residual-2026-09-23`.

The report is the repository's owner-requested independent, AI-assisted referee-style assessment, not a journal-issued decision. This revision retains the inherited results, proofs, primary tables, computations, and classical comparisons. Its two principal additions are a complete construction of the closed packets on the original base and a generic intrinsic reconstruction theorem for the original web. The latter supplies the inverse-theorem alternative explicitly requested in the report's concluding criterion for a substantive revision.

## E131.1 — Closed packets on the original base

**Disposition: complete new proof supplied for referee verification.** The former finite-image sentence has been replaced, not retained as a justification.

The new `parts/09e-packet-descent.tex` contains three results. The geometric-assassin stratification lemma now invokes them.

**Effective Galois descent (`lem:galois-packet-descent`).** In characteristic zero a finite splitting field is enlarged to a Galois extension and modelled, after shrinking, by a finite etale torsor. The object carrying descent is the actual ideal sheaf `I'_O = intersection(P_i)` of a full orbit. Its strict semilinear invariance identifies the two pullbacks on each component of the double overlap. Composition of the group action proves the cocycle on the triple overlap. The equivariant inclusion in the structure sheaf descends by effective fpqc descent. The descended ideal is identified by contraction, and its extension is proved equal to the orbit ideal.

**The fibre assertion.** The proof does not commute intersections with base change by assertion. It flattens the cokernel in `0 -> B/I'_O -> direct_sum(B/P_i) -> C_O -> 0`. This preserves the diagonal injection under arbitrary base change and proves the intersection identity. Geometric integralness and the inherited noncontainment witnesses identify exactly the intended distinct components. A geometric lift over the same algebraically closed field identifies the fibre downstairs with that computed upstairs, excluding additional components.

**Arbitrary characteristic (`lem:power-certified-packets`).** The original noetherian-base theorem is retained, rather than restricted to characteristic zero or to conclusions on covers. For a generic prime `q`, the closure ideal `Q = ker(A -> A_K/q)` is constructed on the original ring. Over a finite splitting cover, finite generation and clearing denominators give `(intersection P_i)^n subset QB subset intersection P_i`. The exact diagonal sequence makes these inclusions certify the precise radical on every geometric fibre. Purely inseparable fibres may be nonreduced; the original packet statement did not require geometrically reduced packets. Finite images are used solely for shrinking, never as a substitute for ideal descent.

**Refinement and gluing.** Schematic closures agree on affine overlaps. Empty generic restrictions are removed by a common shrinking. Packet intersections are defined downstairs by sums of ideals. Their flatness, dimensions, incidence, and nonemptiness are refined after construction of the ideals. Previously established exactness and inclusions survive further restriction. Noetherian induction treats the complement with kernels re-formed on each stratum.

**Torsion downstairs (`prop:descended-packet-torsion`).** For each descended ideal `I`, `T=H^0_I(M)` is constructed on the original base. The sequence defining `M/T`, the relation `I^n T=0`, and an `I`-element regular on `M/T` are spread and flattened. Regularity excludes all new torsion after arbitrary base change. At a geometric component's generic point, the localized packet ideal has maximal-ideal radical, so this is exactly the canonical local torsion module. Lengths are transported using geometric fibres over the same algebraically closed field, not by an invalid assertion about rational lengths under inseparable extension.

The accepted split primary quotients, diagonal injection into them, associated-element injections, and prime-filtration length proof remain intact. Exhaustion has not been replaced by constructibility.

## S131.3 — The full nonreduced scheme recovers the web generically

**Disposition: a new generic intrinsic Torelli theorem and separation corollary.** See `thm:main-web-reconstruction`, `thm:generic-intrinsic-web`, and `cor:separate-torelli-packet`, with the full proof in `parts/12-intrinsic-web-reconstruction.tex`.

On a nonempty invariant open `G_4^rec` in the smooth Jacobian locus, an abstract isomorphism of full failure schemes forces projective equivalence of the relation webs. The second web need only lie in the original smooth Jacobian open. Thus the full scheme determines the cube-zero algebra generically.

The proof has five separately inspectable steps.

1. Three iterated reduced singular loci recover `Sigma_0 = Gr(4,S_R)` intrinsically. Its normal cone has equation `det(T) I_6(gamma_R Sym^2 T)`, homogeneous of degree sixteen and independent of the eight smooth coordinates along the stratum.
2. A single square determinant cone permits transposition. The relative cone resolves this ambiguity: its rank-one Segre rulings are parameterized by the trivial `P(V)`-bundle and the nontrivial `P(K_0^*)`-bundle. On a Schubert line the latter comes from `O^3 + O(1)`, whose determinant degree is not divisible by four. Abstract isomorphisms must preserve the `V`-factor, without extending to the ambient Grassmannian.
3. Dividing the degree-sixteen cone ideal by the recovered determinant extracts the degree-twelve residual coefficient space. Its multiplicity-one Cauchy summands identify the projective components in `S_(4,3,1,0)V` and `S_(5,1,1,1)V`. The second is the Jacobian covariant; the first is additional information retained by the nonreduced failure cone.
4. Recombination of two fixed nonzero components gives a projective line. The possible webs are exactly its decomposable points away from the endpoints. An explicit rank-two condition on the restricted Pluecker quadrics defines the reconstruction open.
5. At the web of four squares, two restrictions are `-2(b-a)(b+2a)/9` and `-4(b-a)^2/9`. Their linear quotients are independent, so the intersection is one reduced point, not just one point set-theoretically. This proves a nonempty open; irreducibility gives intersection with the smooth Jacobian open. Additionally, the same smooth integral web `C_*` already certified in the inherited manuscript satisfies this condition, with quotient determinant `27787/432`.

This does not assert that the K3-only map has degree one. It proves that the full failure scheme separates its generic finite fibre. The corollary removes the finite image of the exceptional reconstruction locus from the finite etale K3 cover, so every web in each remaining fibre is separated. On the regular locus, the Reye/Enriques data are also determined.

## S131.1 and the cross-corank request — Higher residual primary geometry

**Disposition: the actual deepest transverse ideal now yields the inverse theorem; the complete W3/W4 primary atlas is not claimed.** The generic corank-two atlas, first/second global minimal supports, sharp corank-three/four index, and seven-component incidence pullback are retained.

The new theorem is not another quotient-induced example and does not replace the failure ideal by the incidence pullback. It reads the actual degree-sixteen ideal and proves that its additional coefficient component separates the original webs. This answers the report's request for a conceptual connection between deeper nonreduced structure and the inverse problem, by its explicitly permitted inverse-theorem alternative.

A complete associated-prime and embedded-multiplicity classification of W3/W4 at all higher-corank transverse strata, and its full specialization across the two-parameter incidence family, are not proved here. Those stronger atlas requests are not marked closed. They are not prerequisites for the new generic reconstruction proof. The scope distinction in the incidence theorem remains explicit.

## The quotient-induced control family

The Bruns--Vasconcelos-based theorem and proof are retained as an exact benchmark, with classical attribution unchanged. They are not promoted to the main significance claim. The principal new geometric endpoint is intrinsic generic web reconstruction.

## M131.1 — Ballico 1993

**Disposition: documentary item remains open; no fabricated full-text comparison.** The publisher's volume contents and DOI metadata were rechecked. Its PDF link redirected to the abstract/first-page/reference page, not the nine-page article. Direct PDF/EPDF retrieval and a Trento institutional search did not supply full text. `LITERATURE_AUDIT_V132.md` records the precise scope and addresses.

The inherited 1996 comparison is preserved and identified as such. No theorem-level nonanticipation claim is inferred from the 1993 title, first-page link, or reference list. This unresolved documentary item is not a completed priority audit.

## M131.2 — One current theorem hierarchy

Historical revision prose is removed from the article proper and retained in response/provenance history. The deformation section now states exact index five at corank three on `G_4^circ`, consistently with the sharp global theorem. The five-or-six alternative is confined to general coefficient data outside that open. The universal range through the fifth positive layer is retained, with an explicit note that the fifth layer vanishes on the smooth Jacobian open.

The title, abstract, introduction, moduli comparison, and final novelty discussion distinguish the K3-only finite map from generic reconstruction by the full scheme. The normal cone along the reduction and the different cone along the deepest stratum are distinguished explicitly.

## Preservation and verification

All inherited mathematical labels, tables, and local input sections are retained. The new build re-executes all six inherited exact scripts plus `revision132_exact.py`, then compiles the complete local source three times. New exact checks include the 35-by-210 Jacobian matrix, `CC*=48 I`, the rank-35 idempotent, all sixteen matrix-unit equivariance identities, both printed pencil witnesses, and their nonzero quotient determinants.

`evidence/BUILD_RECEIPT.json` is generated only by an actual build and tied to source hashes and the assembly commit. It checks inherited-label preservation, local TeX inputs, references, citations, and exact evidence. Structural proofs are expressly excluded from machine certification. No journal acceptance decision is asserted.
