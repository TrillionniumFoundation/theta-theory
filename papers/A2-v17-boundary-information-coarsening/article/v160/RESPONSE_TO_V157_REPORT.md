# Response to the complete v157 referee report — A2 revision 160

## Controlling objects and scope of this response

The controlling report is `reviews/a2-v157-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md` at `b81ba4a2fac700f17b26163079bd17ef54947509`. Its complete reviewed manuscript is v157 at `a6d34cd2bb2075c64015f3667dbf3f391665cefd`. We retain and integrate the subsequent v158 and v159 derivations through `a27bd7fcea5c4ef04cdd8748411cdeab7ba42855`. The v159 workflow compiled the manuscripts and passed its checks but failed to publish the PDFs because they were ignored by Git. Revision 160 addresses that publication failure on this new branch; it does not rewrite the v159 branch or equate a successful compilation with successful remote publication.

The report's central distinction is accepted as a mathematical distinction requiring a theorem: an arbitrarily selected coefficient section is not an intrinsic part of an unmarked failure algebra, and the mere pullback of a finite algebra does not explain a Hilbert boundary. The revision supplies an intrinsic algebra-bundle construction and a computed modification selected by its multiplication. It keeps the sharp inverse for every pencil and the full inherited reciprocal-fibre theory. It neither substitutes a restricted inverse theorem nor deletes the previous results.

There are two submitted reading objects. Paper I concerns the sharp inverse and its intrinsic algebraic constructions. Paper II concerns universal power ideals and pencil boundary geometry. The unified master preserves their entire mathematical content and is not a third submission. Exact theorem and page numbers in the compiled objects are also recorded in `THEOREM_INDEX_V160.json`.

## The additional structural theorem

The new v160 result identifies a whole open part of the normalized Hilbert incidence space, not just a family mapping into a fibre. For every dimension n >= 3, let U consist of regular pencil lines avoiding rank at most n-3 and meeting rank at most n-2 in at most one reduced scheme point. The incident locus Sigma_2 is smooth of codimension two. Paper II, Lemma 10.1 and Theorem 10.2, prove

`widehat G |_U = Bl_(Sigma_2) U`.

This determines the entire exceptional projective line, its normal bundle, discrepancy one, and its universal nodal curve. Every exceptional direction is classified: the limit is the strict transform of the pencil plus a line through its tangent-normal point in the exceptional projective plane. Directions tangent to the residual determinant conic, including double residual contacts, remain in the theorem. Its hypothesis does not require the squarefree residual pencil assumed in the ordinary-collision theorem.

Paper II, Proposition 10.3, identifies every resolved power on that full exceptional plane as a complete Veronese system of degree

`delta_j = (j-h(n-2))_+ - 2(j-h(n-1))_+`.

Paper I, Theorem 12.1, recovers the centre ideal and its Rees algebra from the failure multiplication diagram: the zero scheme of `J_(h(n-2)+1)` on the intrinsic pencil line maps by a closed immersion onto Sigma_2. Its unit-map kernel is the exact centre ideal. Its Rees Proj is the modification just identified. The first normal jet of a failure-algebra family selects the actual embedded Hilbert limit. Thus the connection is not supplied by pulling an unrelated algebra back along a graph closure.

These statements add to, rather than replace, the integrated v158 all-pencil invariant theorem and the v159 simultaneous arbitrary-multiplicity ordinary-collision and residual-moduli theorems. The former includes singular pencils and minimal indices; the latter remains useful outside the simple corank-two open. The new theorem does not claim a classification over the complement of U.

## Responses to the 24 specific requests

### 1. Exact intrinsic status of B_(n,h)

Paper I, Theorem 10.1 and Proposition 11.1, give the source-normalized algebra bundle and its universal property. The source is extracted from the sharp first relation and its oriented ruling, before the final pencil-coefficient reconstruction. On a split source, the first-jet construction is `E_A = Hom(J^1 L,L) = V tensor O(1)`. The Cartan quotient on this bundle has the determinant-apolar fibres. Scalar changes of a linear lift cancel against the line-bundle twist, and the bundle and projectivized power diagram descend. At h=1 there is no choice of a further integer. This is a canonical functorial bundle, not an asserted preferred untwisted linear quotient of A. The older coefficient section after a chosen splitting remains explicitly distinguished from it.

### 2. Separate the native source and the large coefficient complement

The native source has dimension n, whereas the complementary coefficient space in the common reciprocal boundary example has dimension n^2-1. No n-dimensional subspace of that complement is chosen or alleged to be intrinsic. The first-jet envelope is constructed on the intrinsically recovered source. The new incidence normal space has dimension three and arises from the actual corank-two determinantal stratum, not from the unrelated coefficient complement.

### 3. Prove the stronger connection rather than relying on the opening suggestion

The introductions now distinguish the bundle construction, its power graph, and the additional information in an algebra family. Theorem 12.1 of Paper I connects failure multiplication with the exact centre ideal and Rees algebra of the computed Hilbert modification. It also states precisely that a closed algebra determines the whole exceptional parameter space, not a preferred tail. The stronger positive connection is therefore formulated as an explicit construction with a proof and a specified domain, rather than as an identification of the original algebra with an auxiliary section.

### 4. Isolate the coefficient map, duals and determinant character

The integrated power-foundations section fixes `M = Sym^2 V`, the polynomial coordinate ring `Sym(M^*)`, the multiplication quotient and its dual coefficient map. The determinant character belongs to the top socle representation; it is not silently removed from an affine coefficient identification. The proposition treats the perfect symmetric-power pairing and the resulting nonzero polarization constants. The projectivized maps and their twisting line bundles are then defined separately. The universal ideal proof invokes this fixed convention.

### 5. Theorem-level comparison with invariant-ideal literature

Paper II's foundations and `LITERATURE_AUDIT_V160.md` distinguish the known invariant-ideal decomposition, determinantal balancing, and multiplier formulas from the realization by the particular multiplication coefficient map. The inherited comparison identifies Henriques–Varbaro, Section 2.4 and Theorems 2.6–2.8, and its multiplier Theorem 4.8. The present result is not advertised as a new classification of invariant ideals. The new incidence theorem is proved directly; its significance is not inferred from an unsuccessful title search. No exhaustive nonanticipation conclusion is asserted.

### 6. Exact complete-quadric graph and blow-up reference

The graph/blow-up input is located at Massarenti, Remark 2.5 and Construction 2.6, which explicitly attributes the construction to Vainsencher, Theorem 6.3. The literature record distinguishes direct inspection of this primary exposition from access to the original Vainsencher proof. Paper II, Theorem 10.2, uses precisely the consequence that over rank at least n-2 the complete-quadric map is the blow-up of the smooth rank-(n-2) centre. Its identification of the pencil Hilbert modification requires the separate proof given there.

### 7. Full hypotheses of the simultaneous graph lemma

The integrated foundations state the lemma for an integral base and nonzero finitely generated ideal systems, with a common dense domain of definition. The Segre embedding replaces the simultaneous coordinates by products of generators. The image satisfies the Segre equations on a dense open, and the closed graph lies in that product. The Rees charts give the scheme graph. In the new boundary proof the actual image Rees algebra is used after base change; it is not replaced without justification by a tensor product of Rees algebras.

### 8. Projective twists

The power coefficient map has degree p on `P(Sym^2 V)` and is a section of the degree-p twist with its coefficient space. Its base ideal is distinguished from that twisted evaluation map. The foundations explain why an invertible ideal factor and a positive Veronese power do not alter the blow-up. In the new theorem the determinant factor is Cartier on the integral total space and may be removed for the graph calculation; its vanishing is not declared irrelevant to contact divisors.

### 9. Symmetric diagonalization over a DVR

Paper II, Lemma 7.1, supplies the congruence argument over `C[[t]]` directly: select a least-valuation nonisotropic pivot, split it orthogonally, iterate, and absorb unit factors by square roots. It does not infer congruence diagonalization from arbitrary left-right Smith operations. The classical complex symmetric-pencil canonical form is credited separately to Thompson. Bibliographic access to that paper is not described as a new verification of its full proof.

### 10. Full Segre symbol

The data consist of the projective spectral points together with the local partitions of positive elementary-divisor exponents, considered modulo a common projective reparametrization of the pencil line. The local exponent lists are not presented as sufficient without the point positions. In the singular theorem these data are supplemented by minimal indices. Congruence and pencil-parameter equivalences remain distinct from general changes of cotangent coordinates in the failure presentation.

### 11. Singular pencils and minimal indices

The regular contact theorem retains its visible regularity hypothesis. The integrated Paper II, Theorem 7.2, separately covers arbitrary symmetric pencils. The kernel dimensions of finite coefficient maps determine the minimal-index multiplicities by second differences, while power contacts determine the elementary divisors. The source/image degree conservation identity is retained. The new Hilbert theorem concerns a regular-pencil open; it does not purport to replace this independent all-pencil theorem or extend its boundary classification to singular pencils without proof.

### 12. Classical orbit stratification

The complete-quadric orbit statement remains interpretive classical background, with its established references. It is not counted as a new orbit classification. The new fibre classification concerns embedded limiting pencil curves over U, and follows from the incidence blow-up identification rather than merely from the ambient orbit list.

### 13. Universal property and boundary of the compactification

Paper II, Theorem 10.2, provides both on U. The normalized Hilbert graph is the blow-up of the exact codimension-two centre. It has the effective-Cartier image-ideal universal property; the theorem explicitly includes the hypothesis needed on a test base. Its exceptional divisor, normal bundle and discrepancy are computed, and the full fibres and universal family are identified. The statement does not extend this local identification to all of G.

### 14. An interaction beyond algebra pullback

The exact multiplication power `J_(h(n-2)+1)` is `I_(n-1)` on the rank-open under consideration. Its zero scheme on the intrinsic line is the incidence centre, including its scheme structure. Paper I, Theorem 12.1, constructs the centre's ideal by the unit-map kernel and then its ordinary-power Rees algebra. The first-relation closed immersion identifies this construction on the effective algebra image. The first normal deformation of that algebra selects the tail. These operations identify a modification selected by multiplication, not merely an algebra that exists after arbitrary pullback.

### 15. Classify nontrivial limiting Hilbert fibres

The new theorem classifies every fibre over U: a point off Sigma_2 and a full projective line over Sigma_2. Every member of the latter represents one strict-transform component and one embedded line, meeting in a single node, with no embedded points or extra components. The universal equation is `xy=t`. Example 12.2 of Paper I explicitly includes the two tangential residual directions `[1:i]` and `[1:-i]`; their determinants have double zeros but their Hilbert tails remain reduced. The arbitrary-corank ordinary-collision theorem and its residual-moduli families are also preserved.

### 16. Multiplier formulas

The multiplier-ideal corollary is retained as a specialization of the known symmetric-determinantal formula after substitution of the exponents in the universal power identity. It is not used as an independent originality pillar. The new exceptional coefficient systems use exact coefficient spaces and are not deduced merely from equality of radicals or multiplier ideals.

### 17. Current review entry

The publication procedure replaces the stale v155 root entry only on the v160 branch, after complete checks and compilation. The previous entry is archived as `PREVIOUS_ROOT_ENTRY.md`. The new root names revision 160, the actual authored source commit, the controlling review, the two complete sources and PDFs, and the generated receipts. Its existence is verified again after the publication commit.

### 18. Pin the two reading objects

The root and article README list Paper I and Paper II individually. Each has a complete source and PDF with its own page count. The master is identified as a preservation object, not a third submitted paper. The theorem index identifies the companion and page for the new and principal integrated results.

### 19. Source versus materialization

The authored input commit, the subsequent CI materialization commit, and the final verification seal are distinct objects. `BUILD_RECEIPT_V160.json` records the authored source commit; `PUBLICATION_SEAL_V160.json` binds it to the actual materialization commit after remote read-back. No file claims to contain its own future commit hash. The v159 publication failure is disclosed rather than hidden behind its successful compilation logs.

### 20. Finite checks are not proof certificates

The new suite checks exact local incidence ideals, a Rees saturation, full exceptional coefficient spaces, restrictions to tangent lines, and multidegree identities. It actually reruns the inherited chain in the full repository checkout. These are finite audits of equations whose general proofs are in the papers. Neither the scripts nor the summaries infer a universal identity, journal suitability, or formal correctness from passing computations.

### 21. Ballico limitation inside both papers

The theorem/proof-level text of Ballico's 1993 paper has still not been obtained through the legitimate routes inspected. The limitation remains in the front matter of both submitted papers, as well as the literature record. We neither invent its theorem statements nor infer nonanticipation from this access limitation. This documentary comparison is explicitly not marked closed.

### 22. Focus Paper I without deleting its mathematics

The main route runs from the sharp relation to the inverse and the intrinsic source, then to the incidence application. Covering, rigidification, and extended moving-family material remains in the preserved supplementary sections rather than being treated as prerequisites for the sharp inverse. The mathematical blocks are not deleted. This revision does not claim a reduced total page count: it adds proofs and retains the full earlier content. Logical organization and explicit dependency statements, not arbitrary excision, address the request for focus.

### 23. Logical independence of the two papers

Paper I's sharp inverse does not require the complete-quadric or Hilbert results. Paper II's universal coefficient identity and its incidence computation can be read for an independently given vector space and pencil. The interpretation in terms of an unmarked failure family explicitly invokes Paper I's source/first-relation construction; Paper I's final incidence application explicitly invokes the computed geometry of Paper II. These are named applications, not hidden dependencies in either core proof. Embedded numerical cross-references support reading but are not offered as a substitute for this dependency distinction.

### 24. Canonicity and remaining choices

The raw reciprocal coefficient section selected by a splitting is not declared canonical under its full automorphism group. The intrinsic bundle construction proves cancellation of the relevant lift twists and descent. The incidence ideal is a kernel of a specified morphism and its blow-up has a universal property; the isomorphism with the normalized Hilbert graph is fixed on a dense open. Local Schur complements and coordinate charts are only proof devices. An exceptional direction is supplied by a normal deformation, never selected canonically from the closed algebra alone.

## Preservation, validation and remaining scope

The locked v159 master has 405 labels and 268 mathematical environment blocks. Revision 160 retains all of them byte for byte in the master, which has 421 labels and 277 blocks, and allocates the mathematical body exactly once across the companions. This transitively retains the complete v157 and v158 mathematics. Replaced front matter is archived. The root entry and publication files are the only changes outside the new article directory and its isolated workflows.

The new structural claim is the full simple-incidence modification theorem and its intrinsic Rees construction. The predecessor ordinary-collision theory supplies a different and complementary range of boundary calculations. Neither a classification of every Hilbert fibre over all of G nor a completed historical priority audit is asserted. The papers contain proofs for the stated results and are submitted for independent scrutiny; no editorial acceptance or formal proof certification is claimed.
