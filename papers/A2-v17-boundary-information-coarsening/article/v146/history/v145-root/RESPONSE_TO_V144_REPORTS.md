# Response to the two independent reports on A2 v144

Revision 145, 24 September 2026. This response addresses the latest report at `d8376b5dbb47422d93a474add8362d39cf2a68c1` (review/a2-v144-independent-harsh-top4-r2-2026-09-24) and the earlier report at `e392e7ba5f04a94444831140b22638ae42aa2972`. The preserved v144 publication is `542bcd5027e96ca41568f3eb9c3481dc0f296fed`; its mathematical source is `fb4e7c4d00167e422fdb7ee73876a74f6649fb68`. The new mathematical source is identified by SOURCE_LOCK_V145.json, not by a movable branch name or an old receipt.

We thank the referees for separating the mathematical inverse from the documentary and editorial questions. We have not weakened the all-pencil theorem, discarded nilpotents, imposed genericity, or deleted the independent theories. The changes below distinguish mathematical repair, genuinely stronger reconstruction, the publication decision, and the one outstanding source-access obligation.

## 1. The publication object is now one article, not a 130-page certification request

The principal submission is **geometry.tex / geometry.pdf only**: intrinsic finite reconstruction, reconstruction on a projective curve, the actual relative neighbourhood, and its spectral readout. Every proof and equation reference needed by this article is internal. It imports no external-document labels and uses neither the exterior contraction theorem nor the likelihood theorem.

**applications.tex / applications.pdf** is a separately reviewable manuscript. It preserves the real reciprocal-likelihood existence theorem, the reconstructed critical correspondence, the finite-flat projective critical divisor, Hessian ramification, the trace discriminant, and the triple collision. It uses the reconstruction results as inputs; the converse dependency does not occur. This is a publication-scope decision, not a claim that the real-root proof logically depends on the inverse.

**archive-v144.tex / archive-v144.pdf** is explicitly **non-submitted archival material**, not a supplement of the principal submission. It retains the complete v144 mathematical compilation, including all web, operator, K3, polarized, polar and primary-boundary statements and proofs. The archive is available for separate specialist review. A referee of geometry.pdf is not being asked to certify it. Its original source parts and checks are preserved byte for byte; NONDELETION_V145.json records the preservation audit. The previous version directories and review branches remain unchanged.

The first report proposed retaining the projective critical continuation within the main hierarchy; the second emphasized separating independent likelihood work. We resolve this tension explicitly: the continuation is retained in full, but in the applications manuscript. Its use of the reconstructed pencil is stated there, while the principal paper has the single inverse problem and its directly informative spectral readout.

## 2. The central mechanism now yields a curve-supported inverse

The new section `parts/29-curve-reconstruction-v145.tex` proves **Curve-supported reconstruction** (`thm:curve-reconstruction-v145`) and **One Schubert line suffices** (`cor:schubert-line-reconstruction-v145`).

For any smooth connected projective complex curve C and rank-n bundle U whose projectivization is nontrivial, the homogeneous determinant-times-quadratic-minor construction gives order-d neighbourhoods Y[R,C], with d=n^2+2n-4. For fixed (C,U,V), their **abstract unmarked scheme isomorphism classes classify all pencils**, including singular pencils; every order below d is independent of the pencil. The sufficient numerical obstruction deg(det U) not divisible by n makes the hypothesis concrete. In particular U=O_C(-P)+O_C^(n-1) works on every such pointed curve.

Taking C to be one Schubert line in the original socle gives U=O(-1)+O^(n-1). The reduced support of the invariant is thereby compressed from dimension n(p-n) to dimension one, with the same smallest uniform order. The proof uses the intrinsic first relation, scheme-theoretic rank-one rulings, their global orientation, constancy of a map from a projective curve to PGL, determinant cancellation and the irreducible coefficient line. It does not follow merely by recognizing the coordinate Pluecker embedding. An automorphism of the reduced curve is allowed in the proof.

The scope is precise. The construction uses a chosen Schubert line; it does not canonically select a line from an abstract full neighbourhood. The isomorphism of restricted neighbourhoods is nevertheless unmarked, and its reduced curve is intrinsic. We make no assertion that one unmarked Artinian slice suffices, nor that projective triviality is a necessary obstruction for every conceivable inverse method.

This is a stronger geometric conclusion of the same intrinsic mechanism, not a new unrelated theorem cluster. Whether that mechanism has the significance expected by a particular journal remains a matter for a fresh referee assessment.

## 3. Framed encoding is no longer presented as the conceptual bottleneck

The introduction now separates the unmarked inverse from the framed first-relation parameterization. The closed immersion still holds on the full pencil Grassmannian and over nonreduced parameter schemes. Its proof remains the factorization through the classical Pluecker embedding, tensoring a line with a fixed space and a fixed coefficient inclusion. We explicitly call this the framed encoding consequence, not a new unmarked moduli theorem.

The actual universal ideal-adic neighbourhood and arbitrary complex base change remain unchanged. The supplied relative socle is not identified with the absolute nilradical after a nonreduced base change. No unmarked stack or deformation-groupoid equivalence is asserted.

## 4. Exact classical orthogonal references and the missing component detail

The new lemma `lem:orthogonal-orbits-v145` states the classical input with the acting group O(A) and the self-adjoint operator space fixed. We obtained the original Ohta 1986 article through the publisher's J-STAGE PDF and inspected the relevant mathematical page images. The citations are now:

* Ohta, Section 1.1, p.443: the group and self-adjoint convention; Proposition 1 and Remark 1, p.444: the partition classification for epsilon=1.
* Ohta, Theorem 1, p.447, with the order defined in Section 1.4, p.446, and proof on pp.447–451: full-orthogonal closure order.
* Ohta, Section 2.4, Remark 8(i), p.456: the orbit-dimension identity. The section and page matter because the article has another Remark 8 later.

The manuscript also supplies its own dimension calculation using the trace-pairing adjointness of the two commutator maps and the cyclic-module centralizer dimension. The O-versus-SO component assertion is proved explicitly through the determinant character of the commuting isometries on the primitive multiplicity spaces. An odd Jordan block prevents splitting; all-even blocks give two SO-orbits. We do not infer irreducibility of the full O-orbit or identify the closures of those two components.

The fixed-spectrum proof now invokes this precise lemma, rather than a loose citation to the paragraph following equation (2) of Trevisiol. The orbit theory is credited as classical. Its transport into flat families of the finite failure neighbourhoods, and the first distinguishing order, remain the application proved here.

## 5. Both requested critical-scheme proof clarifications are included

In `parts/28-projective-critical-divisor-v145.tex`, the finite-flat argument now says explicitly that every characteristic-zero residue field contains Q, whereas a nonzero binary form has only finitely many zeros. A Q-rational point outside them defines a constant section whose evaluation becomes a unit after shrinking. Sending it to infinity gives the monic presentation, also after nonreduced base change.

The Hessian argument now includes the full chain rule H_y=J^t H_x J+sum_a s_a Hess(x_a). The first scores s_a vanish in the **critical quotient**, not merely on its reduction. The Hessian determinant therefore changes by (det J)^2, a unit, even on a nonreduced critical scheme. The additional regression checks this mechanism in a quotient with a nonzero nilpotent Hessian class; it is evidence for the formula, not a replacement for the proof.

## 6. Scope is kept at each theorem's actual level

All complex pencils remain in the finite and curve-supported inverse. Regularity enters the spectral sheaf and critical correspondence. The projective finite-flat divisor requires supplied split semisimple projectors, distinct spectral values and simple projective Q-roots disjoint from the spectral poles. The score discriminant is not inverted, so critical collisions remain. The real theorem requires a supplied definite real realization and appropriate data; positivity of all data or all critical points is not asserted.

Reduced rank loci remain distinct from higher Fitting schemes. Finite-neighbourhood flatness is not promoted to flatness of unrestricted failure schemes or reciprocal curves. The trace-discriminant ideal is not identified with the arbitrary scheme-theoretic image of the ramification locus.

## 7. Ballico 1993: still an explicit documentary obligation

The report correctly requires complete theorem text, not title-level inference. We renewed the publisher/full-text and available Library checks. The Library results were earlier A2 patches and access audits, not the 1993 article. None of the inspected routes supplied the complete theorem text. LITERATURE_AUDIT_V145.md records the exact six comparison axes and their status. No source number or conclusion has been fabricated, and the inspected 1996 paper is not used as a substitute for the distinct 1993 paper.

Accordingly this item remains **documentary-open**, not closed by the curve theorem or by a change of publication scope. The mathematical theorem is neither weakened nor declared no-go for that reason. We do not claim that the article has cleared the referee's historical-priority condition or deserves acceptance regardless of the missing comparison.

## 8. The auxiliary operator's priority is not silently certified

The full contraction and Jacobian–Casimir theory remains preserved in the unsubmitted archive, with its existing map-specific comparison. Exhaustive historical priority of that separate theory remains an obligation for its eventual standalone submission. It is no longer used as a principal-paper novelty pillar while being disclaimed as irrelevant to its proof.

## 9. Source integrity and checks

The new branch, SOURCE_LOCK_V145.json and evidence/BUILD_RECEIPT_V145.json identify the new review object. The source is committed before compilation; the following publication commit adds native PDFs and source-bound receipts. The full twenty-script inherited sequence is executed again, together with the new exact regression. The build checks all main references internally, application references against the main article, all archival mathematical blocks and labels, original part/check hashes, and final LaTeX references and boxes.

These checks are not formal verification of the geometric theorems, exhaustive literature clearance, or a top-four editorial certificate. The source lock remains the authority for the mathematical revision, and the receipt records the actual executed build rather than a planned run.
