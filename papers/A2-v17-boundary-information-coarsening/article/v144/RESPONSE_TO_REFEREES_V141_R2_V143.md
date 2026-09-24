# Response to the second independent v141 report — revision 143

## Exact baselines and principal change

We respond to `reviews/a2-v141-independent-harsh-top4-r2-2026-09-24/REFEREE_REPORT.md` at **3afecca5e65d7fe9c6784020ea6e813122938140**, which reviews **8cd389f4048a1047be9aa8e8e4f642595175a555**. We do not answer the obsolete restoration-only v141 review as if it described the current mathematics. Our mathematical predecessor is the already published v142 state **4deb7a35f4488a0c8b686261569ce4ef324ca750**. All its results, including the mixed Jacobian identity, Casimir spectrum and fixed-spectral-stratum development, are retained.

The principal theorem is now unmistakably the all-pencil, finite, unmarked reconstruction theorem. The principal article proves that result, its actual relative realization, and its spectral consequences. The new critical-correspondence section supplies the precise mathematical bridge requested in Section 10 of the report. Web/contraction and boundary developments remain fully proved in the technical supplement and complete compilation. Neither the hypotheses nor conclusions of an inherited mathematical theorem have been weakened.

## 1. Sections 1–3: source state, finite order, and actual relative gluing

We retain the native v141/v142 sources and the complete relative-neighbourhood proof. The new introductory Theorem `thm:principal-finite-v143` gathers the exact statements, pointing to their full proofs. It distinguishes the unmarked isomorphism-class theorem from the fixed-tensor closed immersion and the relative construction.

The integer d is the degree of the first homogeneous relation, not a mysterious constant independent of the presentation. Its significance is that the *abstract unmarked* order-d scheme reconstructs the coefficient line and pencil. We retain “smallest uniform order classifying all pencils”; we do not replace it by a claim about every particular inequivalent pair. The assertion that lower truncations are independent of the pencil remains exactly the inherited theorem.

The gluing proof in `parts/22-relative-spectral-strata.tex` is unchanged. The relative socle ideal remains specified over a nonreduced base; it is not identified with the absolute nilradical. The flat family is the actual finite ideal-adic neighbourhood family, not the unrestricted full failure scheme.

## 2. Sections 4–6: spectral proofs, families, and reduced rank data

The spectral-sheaf/similarity and Artinian polynomial-square-root lemmas remain active in the principal article, including the nonsemisimple case and the complex-field scope. The arbitrary-pencil inverse theorem and the regular-pencil spectral theorem are explicitly distinguished.

The truncated-presentation lemma and all spectral Fitting ideals remain unchanged. The closed immersion realizes classical Segre-stratum closures inside the first-relation parameter scheme; transporting intersections through a closed immersion is not advertised as a new classification theorem. The genuine construction is the realization by finite failure neighbourhoods and the relative spectral Fitting readout.

The rank-preserving four-dimensional specialization, partitions (3,1) and (2,2), and its extension in v142 are retained. Every narrative summary says **reduced** rank loci: the higher determinantal/Fitting structures may change. No flatness of reciprocal curves or full failure schemes is inferred from finite-neighbourhood flatness.

## 3. Section 7 and Section 10: the precise likelihood bridge

We agree that the root-interlacing proof of the published FMS Conjecture 4.5 does not use the failure-neighbourhood theorem. Its elementary independence is retained and stated, not hidden by an artificial dependency arrow. The v141 proof appears unchanged in the principal article.

The new Section `sec:critical-correspondence-v143` proves a different, connecting statement. For a regular symmetric pencil R it defines the reciprocal critical correspondence by the zero ideal of

    eta_(K,S)(H) = -tr(K^-1 H) + tr(S K^-1 H K^-1),   H in R.

Simultaneous congruence identifies these sections and their zero ideals. Intrinsic finite reconstruction therefore recovers the *entire data-to-critical correspondence*, up to simultaneous congruence, not merely a numerical ML degree. The universal construction uses a section of the dual tautological pencil bundle on the determinant open. Formation of its zero scheme commutes with every complex base change, including nonreduced bases. This is a functorial consequence of reconstruction, not a claim that arbitrary unmarked moduli stacks have become equivalent.

For a supplied real definite pair (A,B), put C=A^-1 B. The spectral projectors P_i define the surjective map

    tau_C(S)_i = tr(P_i A^-1 S).

The congruence-covariant right inverse is

    S_0 = A sum_i (sigma_i/m_i) P_i.

All data in S_0+ker(tau_C) have the same critical scheme. This lifts the grouped residue construction to the full symmetric data space without choosing an eigenbasis. Supplying a real definite realization is essential; it is not recovered from an abstract complex invariant.

The second new theorem strengthens the fibrewise real-root conclusion to an explicitly presented relative critical algebra. On the separated-root chamber, put D=product(t-alpha_i), Q=c product(t-beta_j), with c>0 and every beta_j>alpha_r. For

    F=n D Q' - Q sum_i (n-m_i) D/(t-alpha_i),
    a=c[n sum_j beta_j - sum_i (n-m_i) alpha_i],

the degree is 2r-3 and a>0. Alternation at the alpha string and beta string supplies all roots, each simple. We localize the algebraic spectral base at a, the discriminant and the resultant with DQ, as well as the required spectral differences. On this explicit open the critical scheme is

    Spec B[t]/(F/a),
    x=-Q/(nD),   y=tQ/(nD).

This algebra is finite free of rank 2r-3 and etale; the monic quotient and unit derivative persist under arbitrary base change. The omitted x=0 locus is excluded as a *scheme*: its score quotient forces a=0, while a is a unit. Thus the proof does not simply count closed points and overlook nilpotents or a missing chart. The Hessian is handled by the nonzero x-x entry and the Schur factor -F'/(DQ).

Every critical root has one of the prescribed disjoint interval labels. Uniqueness and the implicit function theorem glue the local real analytic roots into globally labelled semialgebraic sections. This holds on a nonempty open set in the full symmetric data space, including all kernel directions of tau_C. It is a real chamber inside a specified algebraic finite-etale open, not a global flatness theorem about the unrestricted correspondence.

This provides a precise common object: **finite failure invariant -> reconstructed pencil -> universal critical correspondence -> explicitly split real critical family**. The supplementary contraction calculation supports the web extension of coefficient extraction; it is not falsely made a logical prerequisite of the pencil inverse theorem.

## 4. Section 8 / B140.2: Ballico 1993

This documentary request is **not marked closed**. We rechecked lawful public bibliographic and publisher routes but did not obtain the complete theorem/proof text of E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102. A title or table-of-contents record does not answer any of the requested theorem-level comparison axes.

LITERATURE_AUDIT_V143.md records all six axes and the exact present assertion to be compared, while leaving the historical column explicitly unverified. We make neither an anticipation nor a nonanticipation claim. No theorem number, hypothesis, or conclusion from the inaccessible paper is invented. The manuscript and active issue matrix agree on this limitation. This revision therefore does not claim to have satisfied every condition of the referee's requested fresh editorial recommendation.

## 5. Section 9 / B140.3: map-specific comparison without weakening the theorem

The full all-rank contraction theorem, including the singular radical kernel, odd nondegenerate injectivity and even scalar exception, is retained unchanged. So are the v142 mixed Jacobian identity, Casimir Gram identity, normalized singular values and inverse.

The new supplementary dictionary compares the actual composite kappa_(n,q)=iota_q o j_n, not unrestricted contraction or a vaguely similar harmonic operator. It gives the coefficientwise relation with the mixed angular Jacobian and the exact nondegenerate Casimir identity. Thus the relationship between this restricted exterior map and inspected classical angular differentiation is stated at equality level. The singular-rank argument is retained separately rather than inferred from a nondegenerate orthogonal decomposition.

The checked classical ingredients receive their precise credit. We do not claim that a finite search proves no equivalent formula occurs elsewhere. The paper's principal inverse theorem no longer depends on an unresolved assertion of historical priority for this auxiliary operator. This is a change of proof hierarchy, not a reduction of the all-dimensional theorem, and it follows the referee's request that the web/contraction development support rather than compete with the principal pencil narrative. The issue matrix distinguishes the completed explicit comparison from still-unverified exhaustive priority.

## 6. Sections 10 and 13: architecture and dependency map

The abstract now contains one main theorem and two structural consequences. The introduction states the principal theorem before the supporting machinery. An in-paper dependency table separates classical inputs, intrinsic coefficient reconstruction, the finite theorem, actual relative realization, spectral readout, the elementary likelihood theorem and the new critical correspondence. The whole all-rank web, K3, polar and boundary development is in the supplement, not deleted.

Moving the web proof required an exact split of its rank-one Fano/orientation foundation: that shared argument is now proved early in the principal article. The full structural coefficient criterion also remains in the principal article; its web and polar applications are in the supplement. This removes a fake web-contraction dependency from the pencil chain without dropping a proof. The complete compilation remains the single place to read both networks continuously.

## 7. Section 11 / B141-R2.1: canonical routing

The active matrix says revision 143 and pins the controlling second-v141 report, the substantive reviewed manuscript and the later v142 predecessor. SOURCE_LOCK_V143.json pins the actual native v143 source commit, run, manifest and PDF hashes. The root CURRENT_REVIEW_ENTRY.md is updated to the same source object when the source-bound build is published. Historical matrices remain accessible in history/v142 and their original version directories; they are not current authorities. The old v141 and v142 branches are not rewritten.

The bootstrap commit and publication commit, when present, are not confused with the exact mathematical source commit. The reading guide instructs the next referee to identify the source SHA, rather than review a moving branch name.

## 8. Section 12 and minimum condition 7: evidence and nondeletion

Nineteen scripts are executed: all eighteen predecessor scripts, byte-identical, and a new exact critical-algebra regression. The latter covers rational non-diagonal congruences, spectral projectors, full data fibres, residue identities, Sturm counts, polynomial Bezout units, and original score equations over Q[epsilon]/epsilon^2. These are regression checks of the written proof, not formal verification.

The native build produces principal, supplement and complete PDFs. Verification checks every inherited mathematical label remains active; every inherited theorem/lemma/proposition/corollary/proof and numbered equation block remains active unchanged; all inherited part and check files are byte-identical; the complete predecessor source archive is exact; the principal/supplement labels partition the complete set; and the source equals the pinned commit. PDF checks cover metadata, bounds, overfull boxes, unresolved citations/references and LaTeX errors.

The results are recorded only after execution in BUILD_RECEIPT_V143.json and NONDELETION_V143.json. No inherited green receipt is relabelled as a v143 result. The record explicitly excludes certification of formal proof, exhaustive priority or journal acceptance.

## Status for re-review

The mathematical and architectural revisions are offered for independent re-review. Source/routing consistency, proof preservation, and executed tests have concrete machine-readable evidence. The full Ballico theorem-level comparison and exhaustive historical priority remain explicitly unverified. All substantive theorem statements are maintained, and the new connecting theorems are accompanied by complete proofs rather than a prospective plan.
