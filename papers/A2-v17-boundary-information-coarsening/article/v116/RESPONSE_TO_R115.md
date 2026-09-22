# Response to the independent referee report on A2 revision 115

Report frozen at `1cb4e00c86699247454d21dbec2dcce01a9c6b8b`; reviewed manuscript head `acfd3d57e0053e1b03df53020fd8e79e14599c03`.

We thank the referee for distinguishing the mathematical improvements in v115 from the remaining breadth, scheme-structure, and priority questions. Revision 116 responds with a new central theorem and full proofs, not a change of venue target. It retains the previous mathematical development and all application appendices. Neither the finite calculations nor the repository build is represented as a verification of the universal proofs or of historical originality.

## 1–3. A stronger mathematical center beyond hyperplanes

**Action: a complete higher-product classification for generating contact pencils of arbitrarily large codimension.** The new introduction and `parts/00c-conductor-reduction.tex` through `00e-moving-contact-normalization.tex` supply the following chain.

For any length-d effective divisor D, including any nonreduced divisor, and n >= 2d-1, let W_D be all degree-n sections vanishing on D. For a generating subspace A of the restricted series, put U_A = res_D^{-1}(A). Theorem `thm:conductor-reduction` identifies the coherent cokernel of Sym^m U_A -> V_mn with that of Sym^m A -> H^0(O_D(mn)), for all m >= 2, over the entire relative generating Grassmannian and after arbitrary base change. This gives equality of all Fitting schemes, not only tangent dimensions or fibre ranks.

For a pencil A, the subseries U_A has codimension d-2, not codimension one. Lemma `lem:contact-power-basis`, Theorems `thm:contact-factorization` and `thm:contact-layers`, and Corollary `cor:contact-multiplicity-strata` determine the entire failure scheme: all components, all primary weights, absence of embedded primes, exact nilpotency, the successive nilradical quotients, every corank, and component descent on every multiplicity stratum. No failure component inside this parameter space is omitted. The integer d is arbitrary.

Theorem `thm:moving-normalization` then treats all contact collisions in the total relative space. The total failure divisor is integral, with an explicit smooth finite normalization. Proposition `prop:moving-singular-test` supplies a necessary-and-sufficient test for its singular support. This is the central synthesis of the revision.

The parameter space is stated exactly. It consists of all generating subseries containing W_D, not all subseries of the same dimension in the unrestricted Grassmannian. This is a geometric hypothesis defining a full family, not a preselection of points known to fail. The marked length-two subdivisor appears only in the normalization of the resulting failure divisor.

## 4. Classical local matrix geometry versus multiplication-specific content

**Action: the distinction is retained and sharpened.** The entire intrinsic residual-germ section is preserved. It explicitly attributes the intrinsic normal derivative, Schur reduction, and transverse determinantal normal form to classical matrix geometry, with the cited precise locations in Frühbis-Krüger–Zach. The new main theorem does not rest its novelty claim on any of these normal forms.

The new multiplication-specific step is the surjectivity W_D U_A^{m-1} = H^0(I_D(mn)). Its proof first fills the double-vanishing ideal by a pencil multiplication argument and then fills the first normal quotient. It yields a coherent cokernel isomorphism over the full family. The power-basis determinant, confluent Vandermonde identity, and discriminant change-of-basis identity are identified as classical tools; they are proved in the text to fix the scheme multiplicities, not claimed as new identities.

## 5. Closest historical comparison

**Action: the nearest-result audit is extended; the Ballico 1993 comparison is not claimed closed.** The official Ballico 1996 PDF was inspected at Theorem 0.2, Proposition 2.2, and Remark 2.3, including the page images. The specified statements concern failure on finite linear sections of a fixed completely embedded surface, rather than the primary classification on the present contact-pencil parameter space. The audit also identifies the precise Hankel/secant input in Conca–Mostafazadehfard–Singh–Varbaro, Section 1 and Section 2, equation (2.0.1), and the exact Fitting and associated-prime references.

For Ballico 1993, the publisher supplies bibliographic and reference material, but the DOI full/PDF/ePDF routes did not yield the theorem pages. Targeted searches did not produce a usable author copy. Accordingly, the table in `LITERATURE_AUDIT.md` marks its parameter-space and theorem-level implications as undetermined. The new results do not make that historical question disappear. The response does not infer non-anticipation from a title, first page, unsuccessful search, or different terminology.

## 6. The original quadratic excess scheme

**Action: the previous theorem is preserved, and a different complete excess family is proved.** Theorem `thm:all-dimension` and all its proofs remain in the active article. Its b<a clause still classifies maximal-dimensional components, exactly as before. We do not assert a newly proved primary decomposition for that unrestricted quadratic scheme.

The new result instead follows the referee's alternative Routes A and D: a uniform scheme-level transport theorem, verified on all generating contact pencils and on every multiplicity stratum, with a complete moving-divisor normalization. This is additional mathematics rather than a deletion or weakening of the quadratic program.

## 7. Connecting breadth and depth in higher products

**Action: the same theorem now has both a uniform parameter range and full scheme content.** The conductor theorem permits arbitrary generating rank k on a length-d divisor and every m >= 2. The rank-two quotient case is then solved completely, for every d >= 4 and n >= 2d-1. It contains reduced multipoint, mixed-multiplicity, and single higher-contact families. The coefficient-ring proof, rather than a fibrewise argument alone, is essential to the multiplicity and collision assertions.

For 2 <= m < d-1 the maximal-minor ideal is zero, so the entire parameter space is the reduced failure scheme; all coranks still have an explicit formula. For m >= d-1 the ideal stabilizes exactly. This degree threshold is part of the classification, not an omitted range.

## 8. Primary ideals, exact nilpotency, and infinitesimal layers

**Action: these are fully determined for the new contact-pencil family.** On a smooth frame chart write v_i = lambda_i + c_i1 z_i + ... on C[z_i]/(z_i^{d_i}). The ideal is generated by

`product_i c_i1^(binomial(d_i,2)) * product_(i<j) (lambda_j-lambda_i)^(d_i*d_j)`.

The prime powers in this factorization are the complete primary decomposition. At a given point retain its vanishing factors f_alpha with exponents b_alpha. With P = product f_alpha, the nilradical is (P)/(product f_alpha^b_alpha), its exact index is max b_alpha, and its q-th successive quotient has the local presentation

`B / (P, product f_alpha^max(b_alpha-q,0))`, with generator `P^q`.

The exact completed frame equation and tangent cone are the same weighted linear arrangement; no unproved normal-crossing replacement is made at braid intersections. The full singular scheme is its Jacobian ideal. The moving total space is separately proved integral, so nonreduced fixed-contact fibres are not misidentified as embedded components of the total space.

These statements do **not** identify the I_C-primary component of the old hyperplane scheme. Its actual v115 lower bound remains unchanged. The distinction is explicit in the new introduction, proof audit, and main text.

## 9. Four proof-presentation requests for the hyperplane theorem

**9.1 — Plane derivative.** New Lemma `lem:hyperplane-explicit-matrix` specifies bases, complement vectors, graph coordinates, and annihilators in both split and tangent normal forms. The n-by-n quotient matrix is kappa*diag(m,1,...,1), with kappa=lambda^(m-1) or 1. Every remaining source monomial is shown to give zero.

**9.2 — Residual image.** The same lemma gives the split propagation starting at degree 2n-4 >= n-1 and checks every successive degree. For the tangent case it proves the integer-interval induction [4,kn] + ({0} union [2,n]) = [4,(k+1)n], starting at k=2.

**9.3 — Rank-two Hankel forms.** New Lemma `lem:hyperplane-confluent-radical` identifies the precise classical secant input and supplies the length-two quotient argument. For a double point its pairing matrix is [[alpha,beta],[beta,0]], nondegenerate exactly when beta is nonzero. Thus the radical assertion includes the nonreduced length-two case.

**9.4 — Associated points.** New Lemma `lem:equivariant-associated-curve` isolates the argument. Its references are Stacks Section 10.63, Lemma 10.63.3 (submodules), Lemma 10.63.5 (finiteness), and Proposition 10.63.6 (minimal support points). The transitive-curve argument excluding closed embedded points is written out.

The original hyperplane theorem and proof are retained as well, so these expansions do not remove earlier material.

## 10–11. Article identity and the application program

**Action: the introduction now states one central contact-scheme theorem and its proof chain.** The conductor reduction, primary classification, and normalization are placed first. The earlier quadratic/polar framework follows as a preserved complementary development, rather than providing rhetorical support in place of the new theorem. The abstract states the actual parameter family and the exact scheme conclusions.

The geometry copy is independent of the application proofs. The application copy and the complete archival manuscript preserve the existing information-recovery, native-realization, likelihood, boundary, and finite-precision arguments. No statistical interpretation is used to inflate the algebraic novelty claim or to supply an unproved algebraic hypothesis.

## 12. Source and generated evidence

All 24 reviewed TeX sources are archived with hashes; 17 active files remain byte-identical. Every one of the 158 old theorem/proof environments, all 201 old labels, and all 27 old bibliography keys are retained. The v115 finite diagnostics are rerun in a temporary copy. The new tests include 272 exact modular multiplication/conductor cases, seven symbolic confluent determinant identities, and exact normalization and nilradical checks.

The workflow first commits the fully materialized mathematical sources on the isolated v116 branch. It then builds all three PDFs and writes source-bound receipts before committing the generated evidence. The final PDFs and logs must exist before the next review head is frozen. No generated-evidence claim is made from a pending workflow.

## 13. Which requested structural route is taken

The revision takes **Routes A and D**, with a full primary and infinitesimal classification in the new family. Its reduction is verified uniformly for all finite-contact divisors, the complete pencil case, every moving multiplicity stratum, and the unrestricted moving-divisor total space. It does not relabel the old arbitrary-beta normal form as that structural theorem, and it does not claim that the separate unrestricted quadratic and hyperplane-primary problems have been solved.

## 14–15. Status for the next referee

The manuscript supplies the new universal proofs and all four requested proof expansions while retaining the previous results. The classical-input distinction and application separation are explicit. The uncompleted Ballico 1993 theorem-level comparison is disclosed without substituting speculation for a scholarly comparison. The appropriate venue assessment and the assessment of these new proofs remain with the next independent referee; neither is asserted by the build receipt.
