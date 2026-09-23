# Response to the independent report on A2 revision 133

**Controlling report:** `reviews/a2-v133-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`  
**Immutable report commit:** `a75f534c6694513ae6c493166d1cba1ea56a98fd`  
**Reviewed manuscript head:** `bbbb697e852d1ca93b88eb7d3bfe6fbd15f396a7`  
**New manuscript:** *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*, revision 134.  
**Branch:** `revision/a2-v134-global-schur-support-reconstruction-2026-09-23`.

This response concerns an owner-requested AI-assisted external-referee-style report, not a journal-issued decision. The arguments below are submitted for independent mathematical verification; an executed coordinate certificate is not a formal verification of the structural proofs.

## Principal change: the reconstruction open is the entire smooth locus

The main theorem is strengthened, not restricted. For every two basepoint-free webs R and R' with smooth Jacobian quartics, an abstract isomorphism of their full nonreduced multiplication-failure schemes forces R'=gR for one projective linear transformation g. The former additional condition R in G4rec is removed: **G4rec = G4circ**.

The reason is not an additional chosen invariant or an assertion that a coarse invariant always determines an arbitrary failure scheme. It is a structural theorem excluding every coarse-invariant ambiguity on the entire geometric family in the report.

The new proof has four steps.

1. Polarize the four-vector `(ell*x1) wedge ... wedge (ell*x4)` to obtain the equivariant embedding j of det(V) tensor Sym^4(V) in wedge^4 Sym^2(V), with Cj=2 and Q=jC/2.
2. For a symmetric bilinear functional q, compute the kernel of contraction i_q j. If q is singular, this is exactly the quartics in rad(q). If q is nondegenerate, it is the line spanned by the square of its inverse quadratic. The proof uses stabilizer shears in the singular case and an orthogonal decomposition in the nondegenerate case. It is not inferred from the four canonical matrix ranks.
3. The exterior support of j(f) has dimensions 4, 7, 9 when f has respectively one, two, three essential variables. With four essential variables it has support 10, except for a nondegenerate quadratic square, which has support 9. In particular a smooth Jacobian quartic has support 10.
4. A sum of two decomposable four-vectors, or any affine tangent vector to Gr(4,W), has support at most 8. Hence the Jacobian component cannot lie on a secant, a tangent, or a flag line of the kind needed for an exceptional recombination. Three essential variables already suffice.

The new principal statements are `lem:schur-contraction-kernel`, `prop:exact-schur-support`, `lem:secant-tangent-support`, `thm:global-schur-recombination`, and the strengthened `thm:generic-intrinsic-web` (also labelled `thm:smooth-intrinsic-web`). The old theorem label remains usable, but the statement is no longer merely generic.

## S133.1 — actual exceptional inverse geometry, not candidate reduction

**Response:** addressed in the smooth geometric family by exclusion of the entire exceptional locus.

The referee correctly distinguished the two-component invariant from the abstract full failure scheme. That distinction remains explicit outside the smooth family. Within G4circ, however, the new support theorem proves that every component pencil has just one reduced Grassmannian point. There are no genuine secant pairs and no flag fibres there whose full-scheme isomorphism classes still need to be compared.

The already repaired universal readout and common-g lemma then give the full inverse theorem on all G4circ: an abstract scheme isomorphism transports both coefficient lines through one g; the new support theorem forces the unique recombination to be gR. In particular the finite Torelli packet is separated without shrinking to a further reconstruction open.

This does not claim that every pair of arbitrary singular webs with equal component pairs has isomorphic failure schemes. No such converse is used.

## S133.2 — incidence with G4circ

**Response:** determined completely for the fibre types named in the report.

| Pencil type | Intersection with G4circ | Dimension/codimension conclusion |
|---|---|---|
| Rank-two, one reduced point | The whole nonempty G4circ | Smooth, dimension 24; codimension 0 in Gr(4,10) |
| Rank-one, two distinct candidates | Empty | No exceptional stratum in the geometric family |
| Rank-one, double point | Empty | No ramification stratum in that family |
| Rank-one, discarded pure endpoint | Empty | No such boundary inside G4circ |
| Rank-zero, flag line | Empty | No positive-dimensional ambiguity inside G4circ |

An empty stratum has no generic singularity or finite codimension to report. This is an emptiness theorem, not a missing numerical estimate. The previous flag example is retained as an ambient example outside the geometric family.

## S133.3 — geometric meaning of the former genericity condition

**Response:** the rank defect is confined to a named invariant boundary.

`cor:exceptional-binary-jacobian` places every ambient rank-defect point of Xcross over a quartic with at most two essential variables. Equivalently the first catalecticant has rank at most two. The support obstruction therefore has an invariant description, and cannot induce a Noether–Lefschetz divisor, secant involution or ramification locus within the smooth quartic family.

We assert containment in this binary-Jacobian inverse image, not equality, and do not manufacture dimensions or irreducible components for the entire ambient boundary. Those additional ambient questions are distinct from the now complete incidence question within G4circ.

## M133.1 — Ballico 1993

**Response:** documentary-open; not falsely marked resolved.

The publisher issue metadata again identifies the paper and pages. Actual attempts to retrieve the publisher full text, first-page endpoint and PDF did not yield the complete article in this session. Searching a research-reading integration did not grant an authenticated full-text connection. No theorem-level comparison with the 1993 text can be certified from these results.

`LITERATURE_AUDIT_V134.md` records the exact access boundary and preserves the earlier theorem-level comparisons with the sources previously inspected. The six requested comparison dimensions remain explicitly unfilled for the unread 1993 article. We do not infer either anticipation or nonanticipation, or substitute the distinct Ballico 1996 paper for it.

The mathematical theorem has been strengthened while this separate historical obligation remains open. Consequently neither this response nor the issue matrix says that every scholarly obligation is closed.

## S133.4 — scope and the higher primary atlas

**Response:** adopt Route A in the report, without discarding the primary program.

The new title and main proof concern intrinsic reconstruction. The primary and relative-algebra results remain in substantial appendices in the same full manuscript, not in an absent companion. Every inherited compiled LaTeX input and every inherited mathematical label is retained. The completed corank-two tables, collision formulas, quotient-induced primary models, global minimal supports and index-five laws remain stated and proved.

A complete W3/W4 embedded-primary atlas at coranks three and four is not newly claimed. It is also not used as a hypothesis of the inverse proof. This is the route the report explicitly offered as an alternative to computing such an atlas.

## S133.5 — architecture

**Response:** reconstruct the proof hierarchy rather than accumulate another appendix-only repair.

The main logical sequence is now: relation model; Fitting presentation; intrinsic filtration; deepest normal cone; universal coefficient readout; common-g functoriality; pencil classification; support exclusion; global rank and ramification; the full smooth-locus inverse theorem. Polarized-K3 and classical inverse-data comparisons follow.

The long introductory boundary statements are relocated intact to `parts/14-boundary-overview.tex`. Universal determinant completion, coefficient tables, boundary collisions and relative packet descent are in the appendices. The five-coordinate square-web witness and the independently smooth integral witness are both retained in `parts/14-separating-pencils.tex`. Neither is the logical basis for nonemptiness or global uniqueness. No inherited mathematical theorem is removed.

## Technical comments 8.1–8.5

**8.1.** The rank strata are now defined by minors of the global vector-bundle morphism `eq:global-pencil-bundle-morphism`, with a rank-two target. The residual section and involution are constructed on the named rank-one stratum, including its locally defined scheme structure.

**8.2.** The new table separately records closed pencil intersections and fibres after deleting endpoints. A pure-endpoint intersection has closed length two but actual fibre length one; a double point retains length two.

**8.3.** `prop:global-pencil-rank-strata` identifies the ramification ideal as Fitt0 of the relative differentials. Locally it is generated by ell_F(1,1); on rank one it is exactly the double-point ideal c+d. The flag locus is removed when speaking of the quasi-finite part. No unjustified finite-double-cover or divisorial assertion is made.

**8.4.** The smooth integral Cstar witness is now the leading arithmetic witness and is checked to have exterior support ten. The square web remains a transparent normalization and five-coordinate illustration in the appendix.

**8.5.** The new executed script independently constructs all 35 columns of j by polarization and compares them with the Fischer embedding, checks the four canonical contraction kernels, harmonic nonvanishing coefficients, support representatives and the smooth witness. The build receipt expressly excludes the written structural arguments from machine-certification claims.

## Repairs already accepted in the report

The entire files `parts/12a-universal-readout.tex` and `parts/12b-functoriality.tex` are retained byte-for-byte. Their proofs are not compressed back to the statements criticized in revision 132. The provenance manifest records these identities along with the inherited-input and label preservation checks.

## Submission status

Revision 134 submits a stronger global inverse theorem, a structural description of the ambient obstruction, and a reorganized complete manuscript for renewed independent review. Its exact tests and source-bound build are reproducible. The unread Ballico 1993 priority comparison remains the explicitly unresolved documentary item; no journal acceptance or independent verification of the new structural proof is represented as having occurred.
