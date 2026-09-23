# Response to the controlling A2 v137 report — revision 139

23 September 2026. Controlling report: `reviews/a2-v137-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, immutable commit `ba24a0b2d062897ee2d7a6b02add81c504fe0e71`. Immediate mathematical predecessor: v138, commit `cf4925b91608b806580bc0cd4fd8ce2441870c08`. The report is retained verbatim in `review_inputs/V137_CONTROLLING_REFEREE_REPORT.md`. This is a response to that report, not a claim that a new independent v138 report exists.

## Main mathematical change

We retain the full smooth-web theorem, the all-dimensional contraction theorem, the intrinsic all-pencil theorem, and every inherited proof. We add a sharp finite-neighbourhood theorem for the original multiplication-failure schemes. For n>=3, N=n(n+1)/2, p=N-2 and d=n+2p=n^2+2n-4, every neighbourhood of order k<d of the socle Grassmannian is independent of the pencil, while its d-th neighbourhood determines the pencil up to projective equivalence. Here order k means quotient by the (k+1)-st power of the stratum ideal, not an arc-space jet construction.

The proof does not put an extra relation block into a new presentation. The actual multiplication minors generate a homogeneous ideal in degree d. The nilradical of the unmarked d-th neighbourhood recovers its degree-one conormal and the kernel of its degree-d multiplication map. That first relation space reconstructs the full graded normal cone. The global oriented ruling and intrinsic determinant colon then recover the pencil. No extension of a cone isomorphism to the ambient Grassmannian is assumed.

A second theorem proves that, in fixed tensor coordinates, the degree-d relation spaces give a closed immersion of the entire pencil Grassmannian into a coefficient Grassmannian. This is scheme-theoretic, includes singular pencils and nonreduced bases, and detects every first-order parameter direction. We explicitly distinguish this statement from an equivalence of unmarked moduli stacks or an unmarked single-slice Torelli theorem.

## B137.1 — Ballico 1993, full-text comparison

The publisher volume record was checked again and confirms volume 163 (1993), pages **5–13**, DOI `10.1002/mana.19931630102`. Repeated publisher PDF and institutional-repository access attempts did not yield the complete article. The available Library search did not return it. Plugin discovery exposed no already connected institutional full-text route. We have not submitted a library request, incurred a charge, or pretended to possess inaccessible pages.

Accordingly, the six requested theorem-level comparisons remain explicitly unverified in `LITERATURE_AUDIT_V139.md`. The new results are proved in the paper; we do not turn these proofs into a claim of exhaustive historical nonanticipation. This documentary issue remains open and is not recorded as a completed blocker. The bibliography and the mathematical claims are not weakened or removed.

## B137.2 — a natural, independently meaningful second family

The v138 natural multiplication family is retained verbatim in `parts/18-natural-pencils.tex`. Its schemes arise from failure of a generating plane to generate a cube-zero algebra under multiplication; they do not contain an auxiliary polar coefficient block.

The new response is `thm:sharp-finite-pencil` and `cor:finite-hyperelliptic` in `parts/20-finite-neighbourhoods.tex`. These specify exactly how much of this intrinsic failure geometry is needed. For genus g>=2, all neighbourhoods below order 4g^2+12g+4 are identical while that order separates the 2g-1-dimensional family of hyperelliptic curve classes. This is an explicit information-loss/reconstruction statement for a classical moduli family, not a conjecture about the size of a web-to-K3 packet.

## B137.3 — the structural criterion versus an automatic theorem

We retain the criterion with its stated hypotheses; we do not rename an assumed coefficient decomposition as a theorem. The automatic calculation for the entire relation-space range 1<=r<N-n is proved in `thm:automatic-quadratic-coefficients`. The new finite-order result uses the literal degree-d ideal from that calculation.

`lem:first-relation-cone` gives the exact intrinsic input, namely the kernel of Sym^d(n/n^2) -> n^d/n^(d+1). `thm:finite-parameter-immersion` then proves the actual family morphism is a closed immersion. The proof factors the morphism into Pluecker, line-to-subspace, and fixed linear Grassmannian closed immersions; `lem:line-subspace-immersion` proves the middle step on affine charts over arbitrary complex algebras. This supplies a full parameter-scheme assertion rather than a closed-point dimension count.

## B137.4 — one external significance narrative

The primary additional narrative is now precise: natural multiplication-failure neighbourhoods have a sharp order at which they retain the full classical pencil, including parameters and elementary divisors that their reduced geometry does not retain. The hyperelliptic application and the same-discriminant/different-Jordan-data example are consequences of that theorem. The web-to-K3 map is not asserted to have degree greater than one, and we do not invent an established open problem or claim to settle a separately named one.

`cor:finite-flat-family` provides a finite locally free family of normal algebras, of rank binomial(n^2+d,d)-binomial(N,2), in fixed coordinates. Its lower truncations are constant; the first relation is a faithful parameter invariant. This makes the geometric assertion testable at an exact finite order. Whether this contribution meets a particular journal's significance threshold is an editorial judgment, not a condition a build receipt can certify.

## B137.5 — map-specific invariant-theoretic comparison

The entire v138 comparison in `parts/19-operator-comparison.tex` is preserved byte for byte, including the classical harmonic decomposition, binary transvectant, apolar differential signature, exterior-contraction signature, and the additional singular-radical argument. The six comparison sources and their inspected locations remain in `LITERATURE_AUDIT_V138.md` and the current audit.

The new finite-order theorem makes no novelty claim for Pluecker embeddings, Cauchy decomposition, irreducibility of wedge^2 Sym^2, or the line-to-subspace embedding. Its additional assertion is the recovery of those coordinate coefficients from the nilradical of an unmarked finite neighbourhood of the original failure scheme. No reference is represented as exhaustively audited solely because its title or representation vocabulary matches.

## Section 7 — local clarifications

The full tangent polarization of the rank-one Fano restriction equations, the compact-real to complex orthogonal implication, and the literal polar block matrix were added in v138 and remain unchanged. Reduced-support and scheme-theoretic equalities retain their separate formulations. The new proof uses an equality of homogeneous ideals; it never substitutes the radical for the degree-d relation space.

## Sections 8–10 — exposition, preservation, and reproducibility

The polar-Fitting family remains as a further coefficient construction, not the principal significance example. The finished AMS-style article contains definitions, theorem statements and proofs, rather than revision-history narration. The technical supplement and complete compilation are retained. No previous section or theorem statement has been deleted. The addition to the introduction is additive, and all changed predecessor source files are archived verbatim under `history/v138/`.

Fourteen exact scripts are run, including a new n=3 full-rank coefficient witness modulo 1009, independent complementary-minor checks, degree-11 scaling checks, an eight-direction Pluecker-chart differential check, and exact order/Hilbert-length identities. These are finite regression evidence, not formal proof verification in all dimensions. `evidence/BUILD_RECEIPT.json` records actual execution and distinguishes structural proofs, source integrity, and the uncompleted historical audit.
