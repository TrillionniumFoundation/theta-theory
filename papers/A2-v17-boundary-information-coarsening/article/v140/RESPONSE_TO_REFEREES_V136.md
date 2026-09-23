# Response to the report on A2 revision 136

**Revision 137 — Intrinsic reconstruction from nonreduced failure schemes**  
Qian Qi · 23 September 2026

This response concerns `reviews/a2-v136-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, immutable commit `d15c9bcabdfc31070b773e2c8014601e75d4e641`. The reviewed manuscript head is `731729b9e391b507d27994f6db8d71d61cfca577`. The report is owner-requested and AI-assisted, not a journal-issued editorial decision. The revised article is `geometry.tex`; `supplement.tex` retains the boundary theory and `complete.tex` compiles all mathematics together. References below use stable LaTeX labels, also resolved in the compiled article.

## Principal mathematical change

The primary problem is now stated as recovering defining equations or relation spaces from an abstract nonreduced failure scheme whose reduction loses those data. The original theorem for **every** basepoint-free four-dimensional web with smooth Jacobian is retained. The all-dimensional contraction theorem is also retained with exactly its original scope. Neither is converted into a conditional result or restricted to a smaller generic locus.

In addition, Section `sec:structural-coefficient-principle` proves an intrinsic coefficient reconstruction criterion and a second family of geometric inverse theorems. For any dimension n >= 2, degree d >= 1 and nonzero linear system L in Sym^d(V*), a concrete block polar-restriction map defines a zeroth-Fitting failure scheme Z_L. Its reduction is the same generic determinant hypersurface for all L. Nevertheless, an **abstract** isomorphism Z_L ≅ Z_L' determines L up to one projective coordinate transformation. This is not an assertion that the original cube-zero multiplication construction already works in every dimension; it is a different, explicitly defined and fully verified instance of the intrinsic mechanism.

## B136.1 — Ballico 1993

**The complete-paper comparison remains documentary-open.** Renewed publisher full/PDF/EPDF routes and exact-title/DOI searches did not provide readable complete theorem text. Library retrieval returned earlier A2 patches and responses, not Ballico's article. The predecessor's first-page inspection is recorded as such and is not upgraded to a full reading. `LITERATURE_AUDIT_V137.md` retains all six requested axes and identifies the precise present objects, while marking the Ballico theorem-level entries unverified. No claim of anticipation or nonanticipation is inferred from the title. The flags `all_referee_issues_closed`, `Ballico_1993_full_text_obtained`, and `priority_certified` remain false. The mathematical additions below do not substitute for that documentary comparison.

## B136.2 — Intrinsic generalization, Route B

Theorem `thm:structural-coefficient-reconstruction` gives sufficient conditions on an **intrinsically selected deepest base**, its graded normal-cone algebra, the oriented rank-one ruling, the determinant ideal line, and its residual Cauchy coefficient module. The conditions do not assume that a scheme isomorphism extends to an ambient variety or is already induced by a common linear map. The proof reconstructs that common projective map before comparing coefficient subspaces.

Corollary `cor:structural-web-instance` verifies every hypothesis for the original (1,4,6) web problem on its full stated smooth locus. Theorem `thm:polar-system-torelli` then verifies them independently for all nonzero homogeneous systems L, with arbitrary n and d. The second verification includes the Fitting map, intrinsic recovery of the base by reduced singular loci, the degree-one conormal before tensor splitting, the nontrivial-ruling Schubert-line test, the actual polar Cauchy inclusion, and the reverse implication. For n=3,d=4 this includes all plane quartics, smooth or singular; larger systems give positive-dimensional parameter families rather than a single witness plus openness. No moduli-stack equivalence or classification of every automorphism is claimed.

Example `ex:polar-nilpotence-three` calculates a genuine nilpotent layer: for a nondegenerate binary quadratic the nilradical in a polar chart has index exactly three. Thus the second family is not merely the reduced determinant locus under another name.

## B136.3 — Representation-theoretic boundary

The expanded article discussion `sec:support-literature`, final subsection distinguishes three layers. The multiplicity-free plethysm is classical and is compared with Cheng–Wang, Theorem 3.5. The Fischer decomposition and harmonic representation input are classical and compared with De Bie–Eelbode–Roels, Section 1, equations (1)–(3); that source's dimension convention does not cover all the low-dimensional cases needed here. The cofactor-divergence cancellation is attributed to the Piola identity, compared with Kupferman–Shachar, equation (1.1) and Section 3.1.

These classical structures do not by themselves calculate contraction on the specified Jacobian inclusion. The article exhibits the additional map-specific nonvanishing coefficient and scalar cancellation, distinguishes the singular-radical argument, and separates those calculations from the intrinsic geometric application. This is a bounded comparison with exact statements inspected, not a claim of exhaustive historical nonanticipation. The earlier exterior/skew-flattening attribution remains intact.

## S136.1 — The relative ruling parameter scheme

Lemma `lem:rank-one-fano-scheme` defines the closed relative Grassmann parameter scheme by the restriction of the universal quadratic rank-one equations. Both projective-bundle maps are shown to be closed immersions, using their Veronese–Pluecker realizations. Their images cover all geometric points and are disjoint. The linearized equations give tangent dimension n−1 at every closed point. The immersed projective space supplies the matching lower bound for local dimension; hence the target local rings are regular. Reducedness and the vanishing ideal of a surjective closed immersion exclude nilpotent thickening and hidden embedded structure. For an arbitrary complex base, local trivializations identify the entire equation-defined construction with base change of the proved constant model. The proof does not infer arbitrary-base validity merely from fibrewise smoothness.

## S136.2 — The complete intrinsic chain

Equation `eq:full-intrinsic-chain` now presents the whole construction in one diagram, and explicitly says that its arrows denote functorial assignments, not morphisms or retractions of schemes. The degree-one object is first identified as the conormal; the matrix bundle is its **dual**. The oriented relative Fano scheme then recovers the uniquely trivial projective factor. Comparing the resulting trivial bundles gives a regular PGL-valued morphism, constant because the base is projective with only constant global functions.

The determinant line and intrinsic colon precede all coefficient-frame choices. The naturality square confines the right-coordinate transformation to the right Cauchy factor. Line-bundle transitions act in the common homogeneous degree twelve, and exterior duality contributes the same (det V)^(-5) twist to both components. No ambient extension of the original scheme isomorphism is invoked.

## S136.3 — Full orthogonal harmonics

Lemma `lem:full-orthogonal-harmonics` supplies a self-contained proof in every n >= 2. The Laplacian recurrence proves the Fischer decomposition. A stabilizer-fixed-space calculation on the real unit sphere and the reproducing evaluation vectors prove irreducibility for the full orthogonal group. The invariant angular operator distinguishes all harmonic degrees. The n=2 reflection and common determinant twist are treated explicitly. Thus the general theorem no longer hinges on an unspecified textbook reference or on the finite n <= 7 regression checks.

## Further comments and preservation

Example `ex:nondiagonal-uniform-web` gives non-diagonal relation spaces in each n >= 4, with an explicit Jacobian and a projective invariant distinguishing them from the diagonal web. It belongs to the component-pair theorem, not to the smooth-Jacobian theorem: its Jacobian is squarefree but reducible. The singular contraction proof now states explicitly why its shears and scaling torus preserve q and why the determinant character only shifts weights. Reduced support equalities remain reduced statements; no radicality of the pulled-back minors or classification of the entire binary-Jacobian boundary has been added.

The main article contains the proof spine and new intrinsic examples; the long primary-boundary archive remains supplementary. Every inherited mathematical label is checked in the combined compilation. Modified predecessor sources are preserved verbatim under `history/v136-modified-source/`, and the entire v136 directory and all reviews remain unchanged in the branch ancestry. All twelve exact scripts and all PDF/reference/source checks are executed by `build.sh`; only `evidence/BUILD_RECEIPT.json` records completed results. These computations do not certify the general proofs, priority, or journal suitability.
