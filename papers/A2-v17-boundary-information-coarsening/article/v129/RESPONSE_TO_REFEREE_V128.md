# Response to the A2 v128 referee report

**Manuscript:** *Universal determinant completion, effective Pieri multiplication, and intrinsic primary boundary laws in multiplication failure*  
**Revision:** 129  
**Controlling report:** `review/a2-v128-independent-harsh-top4-2026-09-23`, `reviews/a2-v128-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`.

We thank the referee for isolating four sharply local proof obligations in revision 128. Revision 129 addresses those obligations without deleting or weakening the existing theorem package. The main conceptual change is that the universal determinant exponent and the relative primary atlas are now proved as one mechanism: a bounded principal power gives a finite colon tower, and a two-short-exact-sequence flattening argument makes that tower commute with arbitrary base change before relative associated points are considered.

## E128.1 — colon formation and base change

**Resolved by replacing the incorrect four-term Tor inference.**

Let (B=A/J), (C_q=B/f^qB), (I_q=f^qB), and (K_q=(J:f^q)). The proof now uses
[
0\to I_q\to B\to C_q\to0,
\qquad
0\to K_q\to A\to I_q\to0,
]
together with (0\to J\to A\to B\to0).
The base is refined so that (B) and every (C_q) are flat. Hence every (I_q) is flat. Since (A) is flat, the second short exact sequence remains exact after arbitrary base change, and its fibre kernel is exactly ((J_T:f_T^q)). The proof explicitly notes that flatness of (C_q) alone is insufficient.

This is stated and proved in the new theorem “Bounded principal-colon primary stratification.”

## E128.2 — finite geometric associated-point stratification

**Resolved with an explicit constructibility lemma and geometric-fibre formulation.**

Revision 129 adds Lemma “Finite geometric-assassin stratification.” It uses the Stacks Project relative-assassin base-change formalism (Tag 05AS), persistence for flat modules (Tag 0GSJ), and, crucially, the constructibility theorem of Section 37.25, Lemma 37.25.5 (Tag 05KR). The theorem tracks finite support packets rather than pretending that geometrically conjugate components must descend individually. On every geometric fibre, the associated points are exactly the generic points of the irreducible components of the nonempty packets.

Embedded multiplicity is defined canonically by
[
\operatorname{length} H^0_{p\mathcal O_{X,p}}(\mathcal F_p),
]
which is finite at an associated generic point. A finite power filtration of this torsion module, followed by generic freeness and Noetherian induction, makes the length constant on the final strata. Incidence and minimal-versus-embedded status are refined simultaneously.

## E128.3 — generic ruling factors on the nontrivial rank-drop slices

**Resolved over the same rational-function fields as the Groebner calculations.**

For the one-parameter ((a,b)=(2,2)) slice, the exact generic-field common factor is, up to a unit,
[
u_0u_1\bigl((s+9)u_0^2+(3s+6)u_0u_1-7u_1^2\bigr).
]
The quadratic discriminant is (9s^2+64s+288), so away from the explicit noncollision divisor ((s+9)(9s^2+64s+288)=0) the support is four distinct ruling lines.

For ((a,b)=(1,3)), the generic factor is
[
10u_0^2+u_0u_1-4u_1^2
]
with discriminant (161). The generic saturation over (mathbf Q(t)) is
[
(\delta,,
10a^2+ac-4c^2,,
10ab+ad-4cd,,
10b^2+bd-4d^2).
]
The layer Hilbert function differs from the saturated two-line divisor only by three dimensions in degree two; the saturation quotient therefore has length three. The checked-in script now performs these fraction-field and saturation calculations.

## E128.4 / M128.1 — corank-four ideal membership

**Resolved by separating multiplication nonvanishing from ideal projection.**

Revision 129 adds right-(GL(V)) stability of (J=I_6(\gamma_R\operatorname{Sym}^2T)): under (T\mapsto Tg), the matrix is postmultiplied by the invertible matrix (operatorname{Sym}^2g), so the maximal-minor ideal is unchanged. Thus every (J_m) is a (GL(V))-subrepresentation.

The Pieri lemma is also made explicit in standard-bitableau notation. The product
[
[123\mid123]^4[4\mid4]^4
]
straightens with coefficient one on
[
[1234\mid1234]^4=(\det T)^4,
]
the unique ((4,4,4,4)) Cauchy line. Having produced an element of (J_{16}) with nonzero (
u)-projection, complete reducibility in characteristic zero now shows that the equivariant projection remains inside (J_{16}). Since the full left-right Cauchy summand is one-dimensional, (d^4\in J).

The computational receipt no longer describes the Pieri proof as machine-certified; the script records only the horizontal-strip combinatorics, while the nonzero structure constant and projection are labelled structural proofs.

## E128.5 — higher-corank primary geometry

**Strengthened without narrowing the theorem.**

The corank-two tables remain fully explicit. At coranks three and four we retain the exact determinant-depth statements, but the family statement is no longer an informal existence sketch: the bounded principal-colon theorem supplies, on every projection-rank chart, a finite base-change-compatible geometric primary stratification, including associated support packets, embedded multiplicities and multiplication ranks. Thus higher corank is governed by the same intrinsic finite primary mechanism even where the paper does not attach a classical geometric name to every packet.

No headline theorem is weakened or removed.

## E128.6 / S128.4 — genuinely global consequence

**Resolved by linking determinant completion to the full primary atlas.**

The universal determinant theorem is no longer used only to deduce (d^5\in J). Its exponent is the finiteness input for the new bounded principal-colon theorem. In any finite-presentation family in which (f^N\in J), all residual colons ((J:f^q)), (q<N), admit a simultaneous finite stratification with arbitrary-base-change compatibility and geometric associated-point control. The general determinant identity therefore produces a general primary-structure theorem, and the ((1,4,6)) atlas is its geometric specialization.

## S128.2 — specialization across boundary strata

The explicit corank-two one-parameter families are retained. In addition, the new family theorem is stated for arbitrary base change on each final stratum and the support objects are geometric packets, so specialization is formulated at the level of the intrinsic graded algebra rather than by comparison of unrelated normal forms. The existing deformation-to-the-normal-cone theorem remains the canonical global specialization package.

## S128.3 — inverse problem

The polarized-K3 reconstruction theorem and the generically finite web-to-K3 statement are preserved verbatim. We continue not to assert generic injectivity without proof. The new global consequence is independent of that unresolved finite degree.

## M128.2 — source architecture

**Resolved.** The referee-facing v129 tree is self-contained. The v123/v125/v126 proof files used by v128 are mounted byte-for-byte into the v129 source directory, and `geometry.tex` has only local includes. `PROVENANCE_MANIFEST.md` records each inherited path and blob identity. The historical branches remain untouched.

## M128.3 — Ballico 1993

The documentary boundary is unchanged: the paper cites Ballico 1993 but makes no theorem-level nonanticipation claim from an unverified full text.

## Evidence discipline

The v129 build receipt separates three categories: scripts actually executed; exact algebraic identities checked by those scripts; and structural proofs that are source-level mathematics and are not machine-certified. This prevents a source-presence Boolean from being read as theorem certification.

## Preservation

Revision 129 is based directly on the v128 review head. The v128 manuscript and the controlling referee report are unchanged. No theorem or proof block from the reviewed article is deleted. The branch adds the corrected homological proof, the constructibility lemma, generic-field support certificates, the invariant-projection step, the general bounded principal-colon theorem, and a self-contained submission tree.
