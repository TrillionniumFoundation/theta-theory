# R76 theorem dependencies, hypotheses and claim boundaries

This is the author dependency addendum for General Theta Foundations I. The actual paired native index has **220 statement labels**: all **209 inherited R75 labels** and **11 additions** (11 main, 0 supplement). Supporting lemmas and corollaries are included; this is not a novelty count. The independent R58 companion keeps its separate source and numbering.

## Reading the map

Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.

The actual compiled index and every new proof source are hashed in `provenance/R76_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.

## 1. Finite-group convex-specification normal form

**Native locator:** main, theorem 4.1, page 10; `thm:r76-convex-normal-form` in `sections/45-convex-specifications.tex`.

**Hypotheses.** A finite command alphabet A, finite group G, a supplied surjective homomorphism gamma:A*->G, and finite output set C. For every g, a closed convex subset K_g of the fixed probability simplex Delta(C); empty constraints are permitted. The original arbitrary stochastic controller satisfies e_o Q_w D_0 in K_gamma(w) for every word, including the empty word. It is not assumed to satisfy group relations on its hidden or observable states. Pure starts count their prescribed initial label; mixed starts allow a free initial probability row.

**Conclusion.** The complete all-word convex specification is realizable with at most M labels exactly when a finite G-set X, a probability preparation lambda and stochastic decoder D meet all finite constraints lambda P_g D in K_g with cost |X|+1_{lambda nonpoint}<=M for pure starts, or |X|<=M for mixed starts. The approximating action may be nonfaithful.

**Direct logical prerequisites.** `lem:r73-lazy-convergence`

**Inherited mechanisms and contextual authorities.** `thm:r73-normal-form`

**Proof mechanism.** A finite identity-word edge cover yields a lazy stochastic average and recurrent projection E. Every identity word preserves its closed classes and satisfies E Q_l E=E. Inverse-word sandwiches give simplex automorphisms, representative independence and the group law. Two-sided identity-word averaging keeps the output inside each closed convex K_g, without assuming exact output factorization in the original machine. Closed-class counting preserves the initializer cost; a direct initializer gives the converse.

**Classical ingredients and priority boundary.** Finite Markov-chain recurrent classes and lazy convergence; Affine automorphisms of a finite simplex permute its vertices; Closed convex sets are preserved under finite averaging and limits. A convex-specification extension of the retained exact stochastic normal form, with arbitrary original stochastic controllers and explicit pure/mixed resource accounting. Classical stochastic-semigroup and simplex structure is credited rather than claimed as new.

**Limits.** All words representing each group element are constrained; checking only one representative per group element on the original machine is insufficient. Convexity and closedness are used in the limiting argument. This is not a classification of arbitrary nonrigid optimal stopping or feedback.

## 2. Attained finite optimization for infinite-word error

**Native locator:** main, theorem 4.2, page 11; `thm:r76-minimax-normal-form` in `sections/45-convex-specifications.tex`.

**Hypotheses.** A supplied target b:G->Delta(C) on a finite group and an integer label budget M>=1. Error is the supremum of total variation over every command word representing G; the pure and mixed start conventions are separate. For computability only, the target table is given exactly by real algebraic entries.

**Conclusion.** The unrestricted stochastic uniform-error optimum equals a finite minimum over G-actions of bounded degree. Mixed starts minimize d_X over |X|<=M; pure starts minimize point preparations on |X|<=M and arbitrary preparations on |X|<=M-1. The minima are attained and 1-Lipschitz in the target table. Algebraic targets admit computable optimal values and realizing tables by real quantifier elimination.

**Direct logical prerequisites.** `thm:r76-convex-normal-form`

**Inherited mechanisms and contextual authorities.** `thm:r73-algebraic-synthesis`

**Proof mechanism.** Use closed total-variation balls as the convex specifications, then enumerate the finitely many finite G-actions up to the given degree. Compact preparations and decoders give attainment; the triangle inequality gives Lipschitz continuity and robustness. Polynomial inequalities with auxiliary absolute-value variables encode each finite optimization, and elimination plus algebraic sample points give the stated effective synthesis.

**Classical ingredients and priority boundary.** Compactness of finite products of probability simplexes; Finite permutation-action enumeration; Triangle inequality; Real algebraic quantifier elimination and sample-point construction. An exact reduction of a synthesis optimum over all stochastic machines and all words to finite compact optimization, including the initializer alternative. The algebraic elimination machinery is classical.

**Limits.** This is a supplied finite-group target synthesis theorem. It does not decide cutpoint, isolation or equivalence problems for an arbitrary supplied probabilistic automaton. No polynomial-time complexity, executed general quantifier elimination, or matching bit/precision/workspace bound is claimed.

## 3. Robust multiplicity and initialization certificates

**Native locator:** main, theorem 4.3, page 12; `thm:r76-robust-multiplicity` in `sections/45-convex-specifications.tex`.

**Hypotheses.** The finite-group target and all-word total-variation error convention of the preceding theorems, with the retained normalized stacked Fourier blocks A_rho(b). For the strengthened pure-start bound, N>1 distinct residual tables, their minimum nonzero max-total-variation separation Delta_b, error delta<Delta_b/2, and total label count less than N. The integer cover contains at least one orbit; multiplicities include any irreducible representation type.

**Conclusion.** A realizing action of multiplicity m_rho has sigma_{m_rho+1}(A_rho(b))<=sqrt(2) delta; for a binary scalar block the bound is delta. Thresholded singular-value ranks give an integer permutation-module covering lower bound for every approximating stochastic controller. Below half the residual separation, a pure controller with fewer than N labels requires one additional initializer beyond that lower bound.

**Direct logical prerequisites.** `thm:r76-convex-normal-form`, `lem:r75-fourier-multiplicity`

**Inherited mechanisms and contextual authorities.** `thm:r75-orbit-multiplicity`

**Proof mechanism.** The positive and negative parts of each probability-row error have mass at most delta, giving stacked Euclidean norm at most sqrt(2)delta. Averaging against unitary representations bounds Fourier operator error. A nullspace/right-singular-vector intersection proves the rank approximation inequality directly. Orbit multiplicity counting gives the cover; a point preparation would merge two separated target residuals if its orbit were too small, proving the initialization charge.

**Classical ingredients and priority boundary.** Fourier averaging over a finite group; Singular values and rank-nullity; Frobenius reciprocity; Triangle inequality for residual separation. Explicit robustness and initialization certificates for arbitrary all-word approximating stochastic machines after the new convex normal form. The matrix rank inequality and representation-theoretic ingredients are classical and proved or credited directly.

**Limits.** These are rigorous lower bounds, not claimed sharp uniform-error constants for every target. The half-separation and fewer-than-N hypotheses are essential to the additional pure-start charge; it is not an unconditional +1 theorem for every approximation.

## 4. Uniform error cannot replace a prime orbit

**Native locator:** main, corollary 4.4, page 13; `cor:r76-prime-error` in `sections/45-convex-specifications.tex`.

**Hypotheses.** G=C_p for a prime p, any probability target b, and integer memory budget M>=1, with uniform error over all words.

**Conclusion.** For either initialization convention the error is the Chebyshev radius of the set of target rows when M<p, and zero when M>=p. For binary outputs that radius is half the range of the first-coordinate response.

**Direct logical prerequisites.** `thm:r76-minimax-normal-form`

**Inherited mechanisms and contextual authorities.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Proof mechanism.** A prime cyclic group has only point or p-point orbits. Below p labels every action is trivial and gives a constant response; a one-label Chebyshev center attains its best error. A point-prepared regular p-orbit realizes any target exactly.

**Classical ingredients and priority boundary.** Orbit-stabilizer theorem for a prime cyclic group; Chebyshev center of a real interval. An exact error frontier illustrating the arbitrary-controller minimax reduction; the elementary orbit classification is not a new group theorem.

**Limits.** The statement is for prime cyclic groups and the fixed all-word error. It is not an expected-cost approximation or the original general-M squared-sign decision-risk curve.

## 5. Sharp simultaneous positivity inequality

**Native locator:** main, lemma 5.1, page 13; `lem:r76-simultaneous-positivity` in `sections/46-mean-contrast.tex`.

**Hypotheses.** n>=5, real vectors v,c,d with sum(v)=1, v.c=v.d=0, and c_i>=v_j-delta_ij, d_i>=delta_ij-v_j for every i,j. gamma>=2(n-2)/(n-4); no sign assumption on v or symmetry of any associated coefficient matrix.

**Conclusion.** The weighted sum gamma C+D is at least [gamma(n+1)+n^2-2n-1+2 sqrt(n(gamma-1)(gamma+n-2))]/(n-1). Equality is exactly the stated simultaneous permutation of v=(M,...,M,-m) and its unique c,d, with m=sqrt((gamma+n-2)/(n(gamma-1))) and M=(1+m)/(n-1).

**Direct logical prerequisites.** `lem:r75-singular-coefficient`

**Inherited mechanisms and contextual authorities.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Proof mechanism.** A common null vector gives simultaneous lower bounds for both outcome sums. Bounding squared coordinates between their extreme values and combining with the retained first-outcome estimate reduces the weighted sum to a strictly concave quadratic in its largest coordinate. The left endpoint is minimized by AM-GM; an explicit positive polynomial separates the other endpoint for all n>=5 and gamma in the stated range. Equality in each step fixes the unique negative coordinate and all excess supports.

**Classical ingredients and priority boundary.** Extreme-coordinate inequalities; Concave quadratic endpoint minimization; Arithmetic-geometric mean inequality; Elementary polynomial positivity. A sharp joint positivity inequality and full equality classification extending the retained one-outcome singular extremum. It is proved explicitly and is not asserted to be an exhaustively priority-cleared classical matrix theorem.

**Limits.** The shared null vector and the gamma range are part of the theorem. Two unrelated nonnegative singular matrices do not automatically satisfy this common-preparation constraint.

## 6. Sharp synthesis for bounded centered coefficients

**Native locator:** main, theorem 5.2, page 15; `thm:r76-bounded-coefficients` in `sections/46-mean-contrast.tex`.

**Hypotheses.** n>=5, 0<p<1, a>0 and P=I-J/n. Existential coefficient pairs (A,u) with u a probability column, 0<=A<=u 1^T, total entry sum np, PAP=aP, and joined ordinary rank rank[A u]<n. The proposed positive factors use n-1 probability preparations, a probability orbit-weight row and first-output decoder rows in [0,1]^n.

**Conclusion.** Existence of a joined-rank-deficient bounded centered pair, existence of such a pair with a common positive factorization of width n-1, and a<=F_n(p) are equivalent. F_n has the three explicitly matched branches with junctions p0=1/(n-sqrt(n)) and p1=2/n. All width-(n-1) boundary factorizations are classified on the low and middle intervals; the middle-interval coefficient pair is unique up to simultaneous coordinate permutation.

**Direct logical prerequisites.** `lem:r76-simultaneous-positivity`, `lem:r75-singular-coefficient`

**Inherited mechanisms and contextual authorities.** `thm:r75-symmetric-return`

**Proof mechanism.** Joined rank gives one normalized common left null vector for A and its complementary outcome B=u1^T-A, producing the simultaneous vector inequalities and C=p/a,D=(1-p)/a. The retained singular bound controls low means; a tuned weighted joint bound controls middle means; direct feasibility controls large means. Explicit common positive factors attain each boundary and decoder mixing fills the smaller contrasts. Equality and nonnegative zero-pattern/ratio arguments classify the boundary factors and force equal weights in the middle interval.

**Classical ingredients and priority boundary.** Common left nullspace and double centering; Nonnegative rank-one support constraints; Convex decoder mixing; Ordinary rank lower bounds for positive factorizations. An exact parameter-feasibility region for a bounded centered matrix problem, with matching positive synthesis and the stated boundary rigidity. Standard nonnegative-factor support reasoning is credited as an ingredient.

**Limits.** The equivalence is existential: it does not say every feasible off-boundary matrix pair admits width n-1. Joined rank is stronger than separate singularity of the two outcomes. Full factorization classification is asserted only on the specified low/middle boundary, not on every feasible matrix or every stochastic implementation.

## 7. Exact memory throughout the mean--contrast plane

**Native locator:** main, corollary 5.3, page 17; `thm:r76-mean-contrast` in `sections/46-mean-contrast.tex`.

**Hypotheses.** n>=5 and binary S_n table beta_{p,a}=p+a(chi_n-1) satisfying 0<=p-a<=1 and 0<=p+(n-1)a<=1. All finite stochastic exact controllers are allowed. The positive-core reduction permits every finite action, and pure initialization is counted. The mean p is an average terminal probability over G, not a prior on an unknown model.

**Conclusion.** At a=0 both minima are one. Otherwise with q=p for a>0 and q=1-p for a<0, the exact core is n(n-1) for |a|<=F_n(q), and n^2 above; the pure count adds one. Every nonconstant table keeps observable group S_n, residual count n!, and dimension 1+(n-1)^2. The nontrivial low/middle transition has precisely the classified minimum permutation-core factors; for positive contrast and p>=2/n all feasible contrasts use the smaller core.

**Direct logical prerequisites.** `thm:r76-bounded-coefficients`, `thm:r75-symmetric-return`, `thm:r73-memory-formula`

**Inherited mechanisms and contextual authorities.** `lem:r75-fourier-multiplicity`

**Proof mechanism.** The faithful full standard block preserves the observable invariants and the retained subgroup-index lower bounds at every nonzero contrast. Any core below n^2 reduces to n-1 natural orbits after absorbing noncarrying constant contributions. Its common preparation gives the bounded joined-rank coefficient problem, so the matrix theorem gives the exact threshold. Explicit n-orbit decoders give the upper throughout feasibility; output complementation handles negative contrast, and the retained pure-start formula supplies the counted initializer.

**Classical ingredients and priority boundary.** Character orthogonality and the standard S_n representation; Subgroup index bounds; Permutation-sum centering; Output complementation. A complete two-parameter exact resource law derived from the new joint-positivity matrix theorem and retained arbitrary-core reduction. It extends the old fixed-mean model without relabelling its special case as new.

**Limits.** Boundary factor rigidity concerns minimum permutation cores. This is not a full high-contrast classification for every finite group, an unknown-model recovery theorem, an arbitrary-prior decision-risk solution, or a claim of minimal quantum dimension.

## 8. Sharp expected-cost excursion bound

**Native locator:** main, lemma 7.1, page 20; `lem:r76-excursion-budget` in `sections/47-rare-branch-approximation.tex`.

**Hypotheses.** Sequential reports split into continuing and returning, with conditional continuation probability at most a fixed 0<r<1 after the entire past, current command and private randomization. The policy may stop before calling; its call count tau has target expectation at most finite B. Eta_L is the first completion of L consecutive continuing reports, L>=1.

**Conclusion.** P(eta_L<=tau)<=min{1,(1-r)B/(r^{-L}-1)}. The coefficient is sharp: independent Bernoulli continuation of probability r and an initial randomized choice whether to run until eta_L attain the stated supremum.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Proof mechanism.** The run-length potential u(k)=(r^{-k}-1)/(1-r) has conditional drift at most one before completion. Sum at the bounded stopping time min(tau,eta_L,H), then take the monotone event limit. For Bernoulli continuation, the drift is exactly one and bounded/monotone convergence gives E eta_L=u(L). Initial randomization provides every expected budget below that mean.

**Classical ingredients and priority boundary.** Pattern-waiting-time potentials and martingale drift; Bounded and monotone convergence; Initial randomization under an expected-cost constraint. A sharp adaptive expected-budget event bound built from a classical waiting-time potential. It is not claimed as invention of the Bernoulli run waiting-time formula.

**Limits.** Sharpness concerns the exceptional-run probability, not a lower bound on every simulator's approximation error. The target expected budget is not a tail or cost assertion about a second process.

## 9. Finite-memory approximation from return geometry

**Native locator:** main, theorem 7.2, page 22; `thm:r76-return-approximation` in `sections/47-rare-branch-approximation.tex`.

**Hypotheses.** Finite-dimensional quantum instruments for a fixed finite nonempty command alphabet, with finite report sets; a fixed invariant closed convex state set C contains all prescribed seeds. A finite seed polytope P contains the initial state. For every state in C and every command, total continuing-report mass is at most r<1, and every positive-mass returning normalized branch lies in P. The theorem uses 0<r<1. Policies share only the visible record and their classical randomness, may choose commands/stopping/terminal POVMs, and have target expected call count at most B. No additional entangled quantum register is present.

**Conclusion.** One policy-independent G(L)-label mixed model, where G(L) counts distinct normalized seed images under fewer than L continuation branches, approximates every complete stopped law and stopped classical-quantum record within min{1,(1-r)B/(r^{-L}-1)}. A counted pure start uses at most G(L)+1. General growth is bounded by k sum_{j<L} b^j; pairwise commuting continuation maps give k binomial(L+b-1,b), and any independently proved polynomial orbit growth yields a polylogarithmic label upper.

**Direct logical prerequisites.** `lem:r76-excursion-budget`

**Inherited mechanisms and contextual authorities.** `thm:r75-stopped-approximation`

**Proof mechanism.** A countable exact seed/continuation refinement supplies a proof coupling. The finite dictionary realizes every returning branch through seed mixtures and every represented continuing image exactly; only an overflowing continuation is redirected. First coupling failure requires L consecutive continuing reports, so the sharp event bound controls the full positive terminal-block mass. Truncation and a scalar nontermination limit yield the complete stopped classical-quantum estimate. An initializer executes the first actual command; counting words or commuting multi-indices gives the resource bounds.

**Classical ingredients and priority boundary.** Polyhedral positive realization; Convex decomposition of normalized instrument outputs; Coupling/common positive mass; Trace norm contraction for terminal measurements; Counting free words and commuting multi-indices. A constructive uniform stopped-law approximation theorem combining a finite return polytope, continuation-semigroup growth and an expected-cost exceptional-run bound. The positive-realization and coupling ingredients are credited separately.

**Limits.** The return geometry is an explicit hypothesis, not a consequence of average-channel mixing. The countable refinement is only a proof device. The theorem gives an upper, does not assert necessary +1 initialization or stationarity of the approximation, and does not preserve its expected duration. External policy storage and computation costs are separate.

## 10. Uniform finite-alphabet approximation

**Native locator:** main, corollary 7.3, page 23; `cor:r76-qubit-polylog` in `sections/47-rare-branch-approximation.tex`.

**Hypotheses.** The retained complete three-report qubit instrument at alpha=1, initial state I/2, and a fixed known finite angle alphabet of size a>=1. The same visible adaptive stopping/command/terminal-POVM policies and target expected budget as in the return-geometry theorem; no extra entangled register. For the exact coefficient claim only, every supplied angle has algebraic sine and cosine.

**Conclusion.** One common model uses at most 3 binomial(L+a-1,a) mixed or one more pure labels and has complete stopped-law/classical-quantum error at most min{1,7B/[8(8^L-1)]}. Choosing L=max{1,ceil(log_8(1+7B/(8delta)))} gives error delta. A single angle needs at most 3L+1 pure labels, uniformly in its value; fixed finite alphabets have a polylogarithmic upper. The explicit table is algebraic under algebraic rotation data.

**Direct logical prerequisites.** `thm:r76-return-approximation`, `lem:r75-full-instrument-bounds`

**Inherited mechanisms and contextual authorities.** `thm:r75-stopped-approximation`, `thm:r74-depolarizing-obstruction`

**Proof mechanism.** Three equilateral-triangle seeds contain the radius-1/2 Bloch disk; the reset branch is one seed and the complementary branch stays within radius 5/11. The real Bloch plane is an invariant convex state set. Commuting angle rotations identify continuation words by their multi-index. Explicit return masses reconstruct the correct Bloch vector and have margin at least 1/48; only the Lth successive zero overflow is altered. Apply r=1/8 to the general theorem and account for the initializer.

**Classical ingredients and priority boundary.** Equilateral-triangle barycentric coordinates; Commuting rotations and multi-index counting; Exact field operations with algebraic rotation entries. An explicit complete-instrument consequence of the new general return-geometry theorem. It separates exact noisy-memory scaling from approximation of target-budget-bounded stopped laws, without declaring the earlier exact noise law a new result.

**Limits.** The angle alphabet is fixed and finite; this dictionary does not uniformly cover a continuum of command angles. No unrestricted classical lower approximation rate or expected-duration bound for the approximation is proved; the subsequent matching physical-dictionary theorem imposes a fixed Born-decoder representation and a badly approximable single phase. Algebraic tables do not give free exact sampling, program bits or working storage. At B=0 the separate one-label zero-call realization applies.

## 11. Sharp leading order for a fixed badly approximable phase

**Native locator:** main, theorem 7.4, page 25; `thm:r76-physical-logarithm` in `sections/48-physical-approximation-lower.tex`.

**Hypotheses.** The retained complete undamped three-report qubit instrument, initial state I/2, and one fixed commanded angle theta=2 pi omega, where irrational omega has a supplied constant c>0 satisfying ||q omega||_(R/Z)>=c/q for every positive integer q. A fixed finite physical dictionary of qubit density matrices sigma_i with terminal decoder tr(E sigma_i) for every requested effect E. Report-transition tables may be arbitrary stochastic tables; they need not implement each quantum branch on every dictionary state. One simulator approximates every common visible stopping and terminal-POVM policy within total variation delta at target expected-call budget B>0, with no extra entangled quantum register. The sharp asymptotic holds with B and omega fixed as delta decreases to zero.

**Conclusion.** Let zeta=min{1,7B/8}. For J>=2 and 0<delta<=zeta/[8^J(1+J^2/c^2)], at least J mixed-start physical labels and J+1 counted-pure-start labels are necessary. Some finite K_omega, independent of B and delta, gives matching uppers K_omega+L-1 mixed and K_omega+L pure, with L=max{1,ceil(log_8(1+7B/(8delta)))}. Thus N_phys(delta;B)/log_8(1/delta) tends to 1 for either start convention. The golden phase admits c=1/3 and K=5. The separate original algebraic rotation admits K=7 and rational tables for the upper; no badly approximable certificate for that phase is asserted.

**Direct logical prerequisites.** `thm:r76-return-approximation`, `lem:r75-full-instrument-bounds`

**Inherited mechanisms and contextual authorities.** `cor:r76-qubit-polylog`, `thm:r75-stopped-approximation`

**Proof mechanism.** A randomized prefix-testing policy for 1 followed by n zero reports has target expected cost bounded by zeta 8/7, uniformly in n. Joint prefix-mass and zero-probability terminal-failure events force one fixed physical dictionary state to have fidelity at least 1-delta/(p_n-delta) with the prepared orbit pure state. Badly approximable phase separation yields disjoint Bloch-vector balls, requiring J states; zero-call tests exclude the counted pure initializer. A finite orbit-prefix polygon contains the return disk; extending this one orbit through depth L-1 uses K+L-1 states and cannot overflow before L continuations. The return-geometry estimate gives the upper. Logarithmic comparison gives the common leading constant. An elementary quadratic norm argument and exact five-point gaps prove the golden constants; exact rational orbit coordinates and barycentric rows prove the original-phase rational upper.

**Classical ingredients and priority boundary.** Trace-distance duality and qubit Bloch-ball geometry; Packing by pairwise Euclidean separation; Elementary Diophantine approximation and the quadratic algebraic norm; Convex hulls of finitely many orbit points and barycentric coordinates; The preceding expected-cost excursion and return-geometry upper. A matching leading approximation law within an explicitly restricted physical-state representation class, with a separately proved counted-initialization lower and explicit quadratic-irrational instance. The classical metric and Diophantine ingredients are not claimed as new, and the result does not certify priority over all prior approximation literature.

**Limits.** The packing proof needs fixed physical density states and their Born terminal decoders. It supplies no lower for arbitrary classical hidden-state decoder tables, no uniform two-parameter asymptotic as B varies, and no asserted badly approximable certificate for the earlier algebraic rotation. The golden rotation does not satisfy the separate algebraic sine/cosine premise merely because omega is quadratic irrational. The K=7 rational construction is an upper for the original algebraic phase only. Exact-model impossibility and approximate-memory growth remain different statements.

## Retained authority and unresolved questions

All 209 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74/R75 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R76.

The original general-M squared-sign risk frontier, arbitrary nonrigid tied control/stopping, unrestricted high-contrast classification for every finite group, unrestricted classical approximation lower bounds, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The new matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.

## Evidence categories

The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R76.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.
