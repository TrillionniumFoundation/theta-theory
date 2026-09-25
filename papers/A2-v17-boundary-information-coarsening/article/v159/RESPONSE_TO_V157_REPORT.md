# Response to the referee on A2 revision 157

**Revision submitted:** 159.  
**Controlling report:** `reviews/a2-v157-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`, commit `b81ba4a2fac700f17b26163079bd17ef54947509`.  
**Complete reviewed predecessor:** revision 157 at `a6d34cd2bb2075c64015f3667dbf3f391665cefd` (mathematical source `b1cde8e304c0572bdb436d8484f1c9b70333fd77`).  
**Additional preserved derivations:** revision 158 source at `61c7a13fa1ce2c65777b9ca7a8e5f6c17dd6ca48`. That locked tip contained derivation files, not complete materialized v158 PDFs. They have been inspected and integrated into the present complete papers; the old branch is unchanged.

## The principal mathematical response

The report distinguishes three questions: an intrinsic construction from the original failure algebra, a boundary theory which contains more information than algebra pullback, and an extension from regular pencils to singular pencils. We address them separately, with explicit dependencies.

**Intrinsic extraction.** Paper I, Theorem 10.1, begins with the cotangent space and first relation of the unmarked algebra. The determinant support and coefficient-support asymmetry select the source ruling before the pencil coefficient line is recovered. On this intrinsic projective space the bundle `Hom(J^1 L,L)` is independent of the choice of the ample generator. Its rank-one nilpotence quotient is an honest algebra bundle with scalar-trivial descent. Proposition 11.1 specifies its universal property. Its projective power diagram is functorial under all ungraded isomorphisms. At `h=1` it requires no exponent choice. No `n`-plane is selected inside the auxiliary `n^2-1` dimensional coefficient complement.

This is a functor constructed from multiplication, not a preferred subquotient of the original finite algebra. An untwisted coefficient representation at a point would have a genuine scalar obstruction; the source normalization removes that obstruction instead of suppressing it. The construction uses the first-relation source before the final reconstruction step, rather than starting from a chosen congruence representative of a reconstructed pencil.

**A computed modular boundary.** Paper II, Theorem 11.3, computes simultaneous ordinary transverse spectral collisions of arbitrary multiplicities. The entire graph on the two-dimensional total base is the blow-up of the collision points. Its special fibre is a reduced nodal tree with one tail per cluster, with no embedded components. The local equalities are ordinary ideals:

`J_p(A) = (z_a,tau)^(delta_(a,p)) (det S_a)^(s_p)`,

where `s_p=(p-h(n-1))_+`, `b_a=(p-h(n-c_a))_+`, and `delta_(a,p)=b_a-c_a s_p`.

In particular, `J_(h(n-c_a)+1)=(z_a,tau)`. Thus multiplication selects the centre. Every tail power map is the complete Veronese system of degree `delta_(a,p)`; this is a coefficient-space assertion, not just a numerical degree. The calculation remains valid for higher-order perturbations with the special pencil and first normal jets fixed.

Paper II, Theorem 11.4, then constructs algebraic flat families of distinct embedded limits over the same semisimple pencil. Their parameter spaces are opens in products of `P(Sym^2 W_a/<C_a>)`, and every member is realized by a smoothing. Consequently

`dim rho^(-1)(R_0) >= sum_a [binom(c_a+1,2)-2]`.

A triple collision gives a four-dimensional family. The proof passes through the finite normalization preimage; it does not incorrectly lift a nondominant map merely because its source is normal. These are specified families in the incidence fibre, not a claim to classify that entire fibre.

**Every symmetric pencil.** Paper II, Theorems 6.1 and 7.2, keep the highest nonzero power on every rank stratum and recover its image plane. The relative complete-quadric contacts recover elementary divisors, while finite coefficient-syzygy nullities recover minimal indices. A global conservation identity relates the contact degrees and the Grassmannian degree. The classical Kronecker congruence theorem is used as an input, with the power-and-syzygy realization proved here. The ordinary Hilbert-boundary theorem has its own transverse hypotheses; those are not conflated with the all-pencil invariant theorem.

## Responses to the 24 specific requests

### 1. Exact intrinsic status of the apolar algebra

Paper I, Theorem 10.1 and the following exact-status remark, identify a canonical algebra bundle on the intrinsic source, together with a canonical projective diagram. Proposition 11.1 gives its representing property. The auxiliary reciprocal coefficient section remains a section after a splitting. Neither construction is called a preferred linear quotient of the original algebra.

### 2. Native source versus coefficient complement

The native source is denoted `S_A=P(V)`; the reciprocal-fibre complement remains the separate space `W` in its own construction. The actual `n^2-1` complement is explicitly distinguished in both introductions and in the exact-status remark. At a collision the residual space is specifically `(ker A(x_a))^*`, so its variance is also fixed.

### 3. The opening claim

Both focused introductions now state the construction actually proved: source extraction, the first-jet bundle, Cartan quotient, scalar cancellation, and projectivization. The universal property makes the `h=1` construction distinguished. The sharp unmarked inverse remains unchanged, including singular pencils. The opening does not claim that the original algebra contains an unproved preferred subquotient.

### 4. Coefficient-map identification and duals

Paper II, Proposition 2.1, gives `mu_p^*: B_h(V)_p^* -> Sym^p((Sym^2 V)^*)`, with evaluation `phi(A^p)`. It records the socle character `(det V)^(2h)`, the dual Gorenstein pairing, line twists of weight `2p`, and the projective base-ideal map with twist `O(-p)`. The proof fixes polarization rather than silently replacing a representation by its dual.

### 5. Theorem-level invariant-ideal comparison

Paper II, Section 2, compares the universal coefficient identity with the symmetric invariant-ideal material recalled by Henriques--Varbaro, Section 2.4 and Theorems 2.6--2.8. Their Theorem 4.8 is identified as the multiplier-ideal predecessor. The assertion here is the exact multiplication coefficient map and its ordinary-ideal specialization, not a new classification of invariant ideals. The literature record specifies which primary text was inspected and does not certify exhaustive historical nonanticipation.

### 6. Scheme-level complete-quadric reference

Section 2 cites Vainsencher's Theorem 6.3 and Massarenti's Remark 2.5 and Construction 2.6 for the exterior-power graph and symmetric rank blow-ups. The all-rank geometry is compared with Casarotti--Corniani--Massarenti, Definition 2.5, Remark 2.6 and Theorem 2.14. The literature record distinguishes the directly inspected modern primary exposition from the original theorem attributed there.

### 7. Simultaneous graph hypotheses

Lemma 2.2 assumes an integral noetherian complex scheme, nonzero coherent section systems and their common dense domain. The Segre embedding is part of the proof. The graph algebra is the Rees image in a function-field polynomial ring, so it has no extra component; the Segre equations continue to hold. This proves the graph scheme with its maps, not only its normalization.

### 8. Projective twists

Proposition 2.1 and Lemma 2.2 identify the power and exterior twists as `O(p)` and `O(q)`. Multiplication by an invertible ideal twists the degree pieces of the Rees algebra without changing relative Proj. A positive power gives a Veronese subalgebra. Determinant divisors are retained when computing contacts even though their invertible factors do not change the graph modification.

### 9. Congruence over a discrete valuation ring

Paper II, Lemma 7.1, proves symmetric diagonalization over `C[[t]]`, including a kernel. A least-valuation diagonal pivot is obtained by a quadratic change of basis when necessary; symmetric elimination then proceeds over the ring. Units have square roots. This establishes the congruence step directly and explains its relation to Smith exponents, rather than citing left-right Smith form alone.

### 10. Full Segre data

Theorem 7.2 includes the projective positions of the supported spectral points and the positive local partitions. Equivalence allows a single projective reparametrization of the parameter line. The minimal indices are included for singular pencils. An unordered list of partitions with their positions erased is not called full spectral data.

### 11. Singular pencils and minimal indices

Theorem 7.2 removes the regularity restriction for the invariant theorem. For the coefficient-syzygy maps `C_j`, the nullity satisfies `kappa_j=sum_a(j-epsilon_a+1)_+`. Second differences recover the minimal-index multiplicities; the finite bound is `j<=floor((n-1)/2)`. The example `S_0+S_2` versus `S_1+S_1` shows why contacts alone are insufficient. The independent regular/transverse assumption of Theorem 11.3 is displayed, not hidden.

### 12. Classical orbit stratification

The complete-quadric orbit description is explicitly recalled as classical interpretation. It is not listed as an independent originality result. The new rank-graph statement identifies the image-plane map and the full scheme through powers in a fixed algebra.

### 13. Universal property and boundary computation

Proposition 10.1 gives the normal, integral, dominant main-component embedded-flat-closure property of the normalized Hilbert graph. The dominance qualification is essential. Theorems 11.3 and 11.4 add actual schematic boundary computations and residual-pencil moduli over a fixed pencil. Thus the construction is no longer presented only as existence of a graph-closure container.

### 14. Interaction beyond algebra pullback

The original finite flat algebra pulled to an exceptional tail can be constant; the paper says so. The new interaction concerns the total family: its extracted envelope has the point ideal `J_(h(n-c_a)+1)`, whose graph blow-up creates the tail. All remaining products prescribe its linear systems, and the degree-one residual system recovers the residual pencil. Information in a smoothing arc is not confused with information in its closed algebra.

### 15. Nontrivial limiting Hilbert fibres

Theorem 10.2 retains the full corank-two calculation. Theorem 11.3 proves the simultaneous arbitrary-multiplicity ordinary version, including higher-order perturbations, all component multidegrees, all power systems, flatness, reducedness and absence of embedded components. Theorem 11.4 constructs varying residual tails, realizes them by smoothings and gives the incidence-fibre dimension bound. Example 11.5 treats a triple collision explicitly.

### 16. Multiplier ideals

The multiplier formula is presented as substitution of the universal power exponents into the classical symmetric-determinantal formula of Henriques--Varbaro, Theorem 4.8. The abstract and main significance discussion do not count it as a separate new multiplier-ideal theorem.

### 17. Root review entry

`CURRENT_REVIEW_ENTRY.md` is updated on this revision branch. It identifies revision 159, the controlling v157 report, the complete v157 baseline and the additional locked v158 derivations. Publication records distinguish the mathematical source commit, the output materialization and the final reading-entry commit. The previously stale v155 entry is not used as the controlling object.

### 18. Two distinct review objects

The root and directory entries name Paper I (`reconstruction.pdf`) and Paper II (`divisor-geometry.pdf`) separately, with independently compiling complete sources. The unified master is expressly a preservation/comparison object, not a third submission.

### 19. Source versus materialization

The build receipt records the exact source commit supplied by the workflow. The final root entry separately pins the complete-output materialization commit. An output commit is not described as the author source commit. The v158 source-only state is also recorded accurately rather than retrospectively called a complete PDF submission.

### 20. Finite checks

The ordinary-collision proofs use polarization, Nakayama, Rees graphs, the local blow-up charts, coefficient-space identification and the Hilbert functor. Finite rational computations are supplementary consistency audits only. The scripts record exact fields and comparisons, rerun inherited suites, and explicitly deny certification of the general proofs. The distinct historical 28-check suite is not represented as rerun.

### 21. Ballico limitation

Both submitted PDFs retain the theorem/proof-level documentary limitation for Ballico 1993. Bibliographic access is not treated as full-text access. The article does not infer nonanticipation from the missing document or claim that the historical comparison has been completed.

### 22. Paper I architecture without arbitrary deletion

The sharp inverse and its prerequisites remain in the main argument. The source envelope is a consequence with its dependencies isolated. Recognition, covering, rigidification and spectral extensions remain in the appendices with complete statements and proofs; they are not advertised as prerequisites of the sharp inverse. The preservation master retains all earlier mathematical blocks. This preserves valid results while clarifying which argument the reader must follow.

### 23. Logical independence of the two cores

Each introduction gives the dependency direction. The inverse and source descent do not use the power-graph, spectral or Hilbert-boundary theorems. The power-ideal and given-pencil theorems do not use the inverse. Only their interpretation for an abstract unmarked failure algebra invokes the source-envelope theorem. Embedded cross-reference maps solve compilation; this explicit dependency statement addresses the separate logical question.

### 24. Choice-free versus chosen objects

The reciprocal coefficient section is still stated with its required splitting. The source-normalized envelope and its projective diagram have a proved scalar-trivial cocycle and universal property; those are the objects called intrinsic. A collision residual pencil is defined by restricting the first normal derivative to the radical, independent of a Schur complement. A smoothing direction remains genuine moduli data and is not called canonically determined by the special algebra alone.

## Reading route and preservation

The direct response to the central extraction criticism is Paper I, Sections 10--11. The all-pencil extension is Paper II, Sections 6--7. The total-base and modular boundary argument is Paper II, Sections 10--11. Section 2 of Paper II fixes the conventions and the classical-source comparisons.

The complete v157 mathematical body and all locked v158 mathematical additions are preserved in the new master. Replaced front matter is archived, and the mathematical blocks are allocated exactly once between the two focused bodies. Compilation, source hashes and preservation manifests identify the review object; they are not arguments for originality or journal acceptance.
