# R77 theorem dependencies, hypotheses and claim boundaries

This is the author dependency addendum for General Theta Foundations I. The actual paired native index has **235 statement labels**: all **220 inherited R76 labels** and **15 additions** (15 main, 0 supplement). Supporting lemmas and corollaries are included; this is not a novelty count. The independent R58 companion keeps its separate source and numbering.

## Reading the map

Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.

The actual compiled index and every new proof source are hashed in `provenance/R77_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.

## 1. Shared normal form and exact initialization charge

**Native locator:** main, theorem 5.1, page 13; `thm:r77-shared-normal-form` in `sections/49-shared-preparation.tex`.

**Hypotheses.** A finite group G, finite command alphabet A with a supplied surjection gamma:A*->G, finite output set C and nonempty finite preparation set I. A closed convex probability constraint K_(i,g) for each preparation/group pair, imposed for every representative word, including the empty word; empty constraint sets are permitted. One transition family and one terminal decoder are shared by all preparations. Neither the preparation identity nor an uncounted history is freely available to the decoder. In the pure convention each preparation selects a prescribed counted label, possibly shared when laws agree. In the mixed convention an external probability row is free.

**Conclusion.** Every all-word closed-convex shared specification is realizable on at most M counted pure-start labels iff one finite permutation core X, one decoder and preparation rows Lambda satisfy all finite group constraints with |X|+iota(Lambda)<=M, where iota counts distinct nonpoint rows once. For freely mixed preparations the exact criterion is |X|<=M. The projected action may have a kernel.

**Direct logical prerequisites.** `thm:r76-convex-normal-form`

**Inherited mechanisms and contextual authorities.** `thm:r73-normal-form`

**Proof mechanism.** The identity-word averaging matrix, idempotent recurrent projection and closed classes depend only on the common command matrices. Apply that same projection to each initial preparation, preserving its own closed convex constraints under averaging and limits. The inherited sandwiched matrices permute the common closed classes. A pure initial label in a class projects to a point mass; distinct nonpoint projected rows need distinct labels outside the classes. Conversely add one transient label per distinct nonpoint row, giving its decoder and first-command transition explicitly. The empty word and first actual command are both matched.

**Classical ingredients and priority boundary.** Finite Markov-chain recurrent classes and lazy convergence; Affine automorphisms of finite simplexes; Closed convexity under finite averaging and limits. A simultaneous extension of the inherited finite-group convex normal form, with an exact count of distinct mixed projected initializations. Classical stochastic-projection structure is inherited and credited.

**Limits.** No free preparation identity for the decoder; no test of only one representative word per group element; no faithful-action requirement. All labels including initialization are counted in the pure convention; mixed external preparation is a different stated resource. Convexity and the every-word requirement are essential.

## 2. Invariant-polytope resource formulas

**Native locator:** main, theorem 5.2, page 14; `thm:r77-shared-polytope` in `sections/49-shared-preparation.tex`.

**Hypotheses.** A finite group and a nonempty finite family of exact response tables b_i:G->Delta(C), with duplicate target tables identified. The same shared-device and pure/mixed conventions as the common normal form. The containing polytope is nonempty and invariant in the full product probability simplex; it may extend beyond the span of the supplied target family.

**Conclusion.** For any finite target family B, mixed shared memory is min_P v(P) over group-invariant containing polytopes in the full response simplex. Pure shared memory is min_P[v(P)+|B\vertices(P)|]. Both minima are attained; vertex labels and one transient label for each distinct prescribed nonvertex target realize an optimum.

**Direct logical prerequisites.** `thm:r77-shared-normal-form`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Associate a complete response profile to every permutation-core label and take their invariant convex hull. Vertex reduction gives the mixed lower and upper. For pure starts, nonvertex target profiles already occurring at continuing labels use distinct nonvertex profile slots; remaining distinct nonvertex targets require distinct mixed rows and therefore transient initializers. This prevents double charging. Conversely realize the vertices by the group action and every distinct prescribed nonvertex by one initializer. Nonempty integer-valued possible costs yield attained minima; no compactness of a space of all polytopes is presumed.

**Classical ingredients and priority boundary.** Classical invariant-cone and positive-realization geometry; Finite group actions on polytope vertices; Convex combinations and finite integer minima. An exact common-device mixed/pure resource invariant, including the prescribed-nonvertex initialization term. The classical connection between positive realization and invariant convex geometry is not claimed as a new discovery.

**Limits.** The containing polytope need not stay in the target span; no polynomial-time global synthesis claim; do not charge an already counted nonvertex profile twice. Polytopes may extend beyond the target span. The formula does not identify ordinary linear rank with positive memory and is not a compactness theorem for a fixed polytope parameterization.

## 3. Joint multiplicity

**Native locator:** main, lemma 5.3, page 15; `lem:r77-joint-multiplicity` in `sections/49-shared-preparation.tex`.

**Hypotheses.** A finite group and finite family of probability-valued response tables. The real joint residual module is the span of every translate of every preparation, using the inherited stacked Fourier convention. For the resource conclusion, a simultaneous positive factorization on a single finite G-set with one common decoder.

**Conclusion.** The multiplicity of each irreducible rho in the complexification of the real joint residual module equals rank_C[A_rho(b_1) ... A_rho(b_r)]. Every simultaneous factorization on a G-set X has this rank at most m_rho(X). The joint rank may exceed d_rho.

**Direct logical prerequisites.** `lem:r75-fourier-multiplicity`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The inherited group-algebra block decomposition sends translates to A_rho(b_i)rho(h). Independent group-algebra combinations for different preparations allow independent right matrix factors. Their sum has arbitrary columns in the sum of the column spaces, whose dimension is the concatenated rank. A common positive realization maps its reachable preparation submodule onto the joint response module; complete reducibility gives the permutation-module multiplicity bound.

**Classical ingredients and priority boundary.** Group-algebra matrix-block decomposition; Complete reducibility of finite-group representations. The joint preparation module formulation needed for the shared-device theory; the group-algebra and representation-theoretic ingredients are classical.

**Limits.** Joint rank is not the maximum individual rank; joint rank may exceed the irreducible degree. The multiplicity statement alone does not guarantee positive synthesis at every contrast or for different means.

## 4. Exact noncyclic memory at small common contrast

**Native locator:** main, theorem 5.4, page 15; `thm:r77-shared-low-contrast` in `sections/49-shared-preparation.tex`.

**Hypotheses.** A finite group and a finite nonempty exact target family. All target laws have the same group-averaged probability row pi. The common-contrast family is b_i,t=pi+t(b_i-pi), with 0<=t<=1. For the equality, 0<t<=t0 with the explicit positive threshold constructed in the proof; the zero-module and zero-contrast cases are handled separately.

**Conclusion.** For a shared family with common group mean pi and b_i,t=pi+t(b_i-pi), an explicit t0>0 gives mixed shared memory exactly nu_G(V_B) for 0<t<=t0. The joint module and multiplicities are unchanged for positive contrast. Pure memory has the exact invariant-polytope formula and lies between nu_G(V_B) and min(N,nu_G(V_B)+r). At zero contrast both minima are one.

**Direct logical prerequisites.** `lem:r77-joint-multiplicity`, `lem:r75-fourier-multiplicity`, `thm:r77-shared-normal-form`, `thm:r77-shared-polytope`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Delete zero-mean output columns, which positivity makes identically zero, and split off the common invariant probability line. Embed the remaining module W equivariantly in a minimum permutation module. Orthogonal projection followed by the inverse embedding yields an equivariant left inverse F that annihilates invariant rows. With a_i=j(b_i-pi), uniform p, and T(x,c)=F(e_x)(e,c), one has a_i1=0, T1=0, pT=0 and a_iP_gT=b_i(g)-pi. Let A=max_i||a_i||_infinity, epsilon=1/(2kA), B=max|T(x,c)|/pi_c and t0=min(1,epsilon/B). Then lambda_i=p+epsilon a_i and D_t=pi+(t/epsilon)T are stochastic and simultaneously realize the family; preparations have margin 1/(2k). The zero-module case is separate. For t>0 contrast is invertible on W, so the joint cover gives the matching mixed lower. The exact initializer formula and deterministic residual machine give the pure bounds.

**Classical ingredients and priority boundary.** Frobenius reciprocity and orbit decomposition; Invariant inner products and complete reducibility; Real descent for complexified finite-group modules; Positivity by bounded perturbation. A simultaneous positive-synthesis and matching resource theorem for arbitrary finite groups and common-mean preparation families, including noncyclic modules. It is not a rediscovery of classical complete reducibility.

**Limits.** Common mean cannot be removed unconditionally; no general high-contrast equality; no universal pure-start surcharge. A different-means four-row example has rank three but positive-realization cost four. Zero contrast is treated separately. Exact pure memory is the polytope minimum, not asserted equal to the mixed integer cover.

## 5. Joint robust multiplicity certificate

**Native locator:** main, theorem 5.5, page 17; `thm:r77-joint-robust` in `sections/49-shared-preparation.tex`.

**Hypotheses.** A finite group and a single shared stochastic controller approximating every preparation and every word in TV by at most delta. Nonnegative preparation weights alpha_i summing to one in the displayed horizontal Fourier block; weights may be chosen separately for different irreducibles. All pure preparation labels are counted; the mixed start convention is stated separately.

**Conclusion.** For a common device with uniform all-word, all-preparation TV error delta, every singular value of the weighted horizontal joint Fourier block exceeding sqrt(2)delta forces one corresponding irreducible multiplicity in the same permutation core. The resulting simultaneous orbit-cover lower applies to both start conventions, with weights chosen independently for different irreducibles if desired.

**Direct logical prerequisites.** `thm:r77-shared-normal-form`, `lem:r77-joint-multiplicity`, `thm:r76-robust-multiplicity`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Apply the shared normal form to the closed convex TV balls for every preparation. The inherited stacked Fourier estimate bounds each preparation error by sqrt(2)delta. Horizontal concatenation with square-root weights summing in square to one preserves this operator bound by Cauchy-Schwarz. The approximating joint block has rank at most the multiplicity of that same core; the singular-value/rank inequality gives the necessary multiplicities. Zero weights can only reduce the represented target span.

**Classical ingredients and priority boundary.** Cauchy-Schwarz inequality; Operator-norm Fourier estimate; Singular-value perturbation and rank inequality. A quantitative necessary shared-memory certificate using weighted joint blocks, with an explicit error bound independent of the preparation count.

**Limits.** No multiplicative error factor from the number of preparations; no automatic pure initializer; not necessarily a sharp error law. The same core is used for all preparations. Preparation weights may vary between irreducibles, but no freely preparation-dependent decoder is permitted.

## 6. Unbounded joint multiplicity for a fixed group

**Native locator:** main, proposition 5.6, page 17; `prop:r77-shared-involution` in `sections/49-shared-preparation.tex`.

**Hypotheses.** G=C2, q>=1 preparations, and q+1 outcomes indexed by 0,...,q. Uniform common mean pi and target contrasts epsilon(e_i-e_0), with 0<epsilon<1/(q+1). For the robust lower, uniform all-word and all-preparation TV error delta<epsilon/sqrt(2q).

**Conclusion.** For every q>=1 the stated C2 family has individual memory two for each preparation but exact shared mixed and pure memory 2q. The count remains necessary at error delta<epsilon/sqrt(2q). Rational strictly positive target response probabilities are available.

**Direct logical prerequisites.** `thm:r77-shared-normal-form`, `lem:r77-joint-multiplicity`, `thm:r77-joint-robust`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The C2 sign block is epsilon[e_i-e_0] with Gram epsilon^2(I+11^T), hence rank q. Every sign copy in a C2 permutation module needs a two-cycle, forcing 2q labels after the common normal form. q explicit disjoint cycles attain that count and a single cycle realizes each separate preparation. Equal preparation weights give least singular value at least epsilon/sqrt(q); the robust threshold follows.

**Classical ingredients and priority boundary.** Trivial/sign decomposition of C2 permutation modules; Positive Gram matrix rank. A sharp unbounded separation between separately optimized and shared realizations for one fixed group, with explicit robust constants.

**Limits.** Strict positivity is asserted for target responses, not permutation transition entries. The increasing parameter q counts preparations/outcomes; the group remains C2. The robust singular-value threshold is sufficient and is not claimed optimal in delta.

## 7. An unbounded pure initialization cost

**Native locator:** main, proposition 5.7, page 18; `prop:r77-many-initializers` in `sections/49-shared-preparation.tex`.

**Hypotheses.** G=C2 and binary terminal output. r>=1 distinct amplitudes 0<t_1<...<t_r<1/2, with each table taking the two reversed Bernoulli laws. One common controller, and either externally mixed starts or prescribed counted pure labels as separately stated.

**Conclusion.** For r distinct positive binary amplitudes in the stated C2 family, shared mixed memory is two and shared pure memory is exactly r+1, although each preparation separately has pure memory two.

**Direct logical prerequisites.** `thm:r77-shared-normal-form`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The two extreme binary decoder rows form a mixed core. Every distinct empty-word law needs a distinct pure initial label, and all r initial decoder rows have first coordinate greater than one half. If they were the only labels, every stochastic image after the involution would still lie above one half, contrary to the reflected target. One negative extreme core label plus the other extreme and r-1 transient initializers attain r+1.

**Classical ingredients and priority boundary.** Convexity of stochastic images; Separation of binary probability rows at one half. A sharp family showing an unbounded exact pure-initialization surcharge for shared preparations.

**Limits.** Does not contradict the inherited single-preparation initializer theorem. The external choice of a preparation is not an uncounted decoder input. This example measures counted labels, not the number of bits in a preparation-selection message.

## 8. Exact optimal-memory formula with ties

**Native locator:** main, theorem 7.1, page 22; `thm:r77-reset-cover` in `sections/52-optimal-reset-memory.tex`.

**Hypotheses.** finite-dimensional finite-command reset instrument I_ai(rho)=tr(E_ai rho)sigma_i every failure effect E_ai is positive definite no closed failure set positive bounded call-cost operators success requires immediate commitment and no extra free observation/measurement/reset fixed-program autonomous controller with prescribed counted pure start and inherited terminal-decoder convention

**Conclusion.** m_*=1+min_(p in P_*)t([s]\I(p)); arbitrary ties and stochastic transitions do not improve it. Event stopping uses m_* total labels and state stopping m_*+1. Algebraic data admit a finite exact procedure.

**Direct logical prerequisites.** `thm:reset-control`, `prop:reset-rigidity`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** An optimal first row lies in P_*. At a dual maximizing preparation all first failure reports are exposed; residual equality forces a continuing row supported on each optimal-action set. One support action per used row yields a transversal. Conversely pure transversal rows and deterministic post-report routing give Bellman equality and properness from the cost floor.

**Classical ingredients and priority boundary.** Bellman verification; finite transversals; real-algebraic quantifier elimination. An exact tied-action optimal-memory invariant in an exposed finite reset class, with arbitrary stochastic autonomous updates and explicit initialization/termination accounting. Bellman verification and finite-controller search are classical ingredients.

**Limits.** Not arbitrary nonreset back-action or inaccessible reports; no action-uniqueness assumption; no polynomial-time algorithm or executed general elimination. Positive effects can be weakened to positive exposure of every action/report at one attaining dual preparation, as stated in the text. Merely semidefinite effects need not suffice. Report routing depends only on counted information, and success/commitment conventions remain fixed.

## 9. Attained certificate of a strict optimality gap

**Native locator:** main, theorem 7.2, page 23; `thm:r77-reset-gap` in `sections/52-optimal-reset-memory.tex`.

**Hypotheses.** all reset-cover assumptions M>=1 live labels robustly proper controller; infinite worst-state cost satisfies the lower trivially

**Conclusion.** Worst-state cost>=V_*+D_M; D_M is attained and D_M>0 iff M<m_*. Algebraic data give finite exact computability.

**Direct logical prerequisites.** `thm:reset-control`, `prop:reset-rigidity`, `thm:r77-reset-cover`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Keep only the first post-failure residual minimum over M rows to form K_M. Minimize its largest eigenvalue over a compact product of simplexes. Zero gap and strict exposure force every residual minimum to vanish, giving an optimal controller with those rows. An optimal row family gives the converse.

**Classical ingredients and priority boundary.** compactness and continuity; positive-semidefinite order; semialgebraic optimization. An attained finite-dimensional lower certificate whose positivity exactly detects insufficient optimal-memory budget in the stated reset class.

**Limits.** D_M is a lower certificate, not the full constrained cost frontier; not the original squared-sign minimax-risk gap; floating optimization does not certify exact zeros. No general-M squared-sign risk formula follows. The lower retains only one continuing residual, so it is not claimed to attain the full constrained-control optimum.

## 10. Universality of the optimal-memory covering problem

**Native locator:** main, theorem 7.3, page 24; `thm:r77-reset-universality` in `sections/52-optimal-reset-memory.tex`.

**Hypotheses.** q>=2 actions and finite nonempty proper sets A_i subset [q] fixed rational 0<r<1 intermediate basis outcome and realized cost are not observations at the controller port

**Conclusion.** V_*=3+r/(1-r)+1/q and m_*=t+1 for an actual rational reset experiment with positive effects and constant success probability; exact optimal memory is NP-hard on this family.

**Direct logical prerequisites.** `thm:r77-reset-cover`, `thm:reset-control`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Use s+q basis states, reset effects (r/s)I, and diagonal costs in [1,4] encoding the optimal sets. The constant Bellman vector and additional basis coordinates give spectral value 3+r/(1-r)+max_j p_j, uniquely minimized by the uniform row. Exact memory is the transversal number plus one. Polynomial encoding length yields an explicit classical transversal reduction.

**Classical ingredients and priority boundary.** measure-and-prepare instruments; classical transversal complexity. A constructive physical realization of every finite optimal-action cover and an explicit complexity reduction for its exact optimum memory. Classical transversal hardness is credited rather than claimed as new.

**Limits.** Only cost/effect operators commute; CP maps need not commute; no claim resolving P versus NP; not a generic POMDP hardness assertion. The intermediate basis outcome and realized cost are hidden at the control port. Only the cost/effect operators commute, not the completely positive reset maps.

## 11. Why positive reachability cannot be dropped

**Native locator:** main, example 7.4, page 25; `ex:r77-reset-exposure` in `sections/52-optimal-reset-memory.tex`.

**Hypotheses.** two-dimensional Hilbert space and one reset state |0><0| E_a=E_b=diag(1/2,0) G_a=diag(1,6) and G_b=diag(2,5) failure effects are semidefinite, not definite

**Conclusion.** Without positive exposure the all-reset cover expression would give two labels while one is robustly optimal.

**Direct logical prerequisites.** `thm:reset-control`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Direct Bellman and diagonal calculations give v=2, L_a=diag(2,6), L_b=diag(3,5), robust value five and unique initial action b. Constant b has cost operator diag(4,5) and one label; its worst-case state never sees the reset report.

**Classical ingredients and priority boundary.** geometric waiting-time expectation; largest diagonal eigenvalue. An exact primitive-data sharpness example showing that the positive-exposure premise of the reset cover theorem cannot simply be dropped.

**Limits.** Does not contradict the reset-cover theorem at its hypotheses; not a classification of all semidefinite-effect experiments. The worst-case initial state never reaches a failure report; this explains how a locally nonoptimal continuation can remain below the robust value.

## 12. Robust antichain factorization certificate

**Native locator:** main, lemma 8.1, page 25; `lem:r77-robust-antichain` in `sections/51-unrestricted-approximation.tex`.

**Hypotheses.** J probability rows lambda_n on M labels arbitrary decoder columns d_m in [0,1]^M diagonal responses at most epsilon and off-diagonal responses at least 0<b<=1 epsilon<b^2/(2M^2)

**Conclusion.** J<=binom(M,floor(M/2)); all equal-size subsets give a sharp abstract cardinality example.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Threshold at b/(2M). An off-diagonal sum has one summand at least b/M; the diagonal bound forces that coordinate outside the other thresholded support. Ordered witnesses give an antichain. A random-permutation proof gives the central-binomial bound.

**Classical ingredients and priority boundary.** nonnegative-factorization support arguments; Sperner/Lubell counting. An explicit stable-margin version of a classical support-antichain bound, proved self-containedly. The exact zero-pattern counting principle is credited to earlier nonnegative-rank work.

**Limits.** No Born, quantum-state or decoder-linearity assumption; abstract extremality is not a chronological qubit simulator; the exact support-antichain argument is classical.

## 13. Memory lower bound from approximately exposing tests

**Native locator:** main, theorem 8.2, page 26; `thm:r77-operational-antichain` in `sections/51-unrestricted-approximation.tex`.

**Hypotheses.** J causal preparation procedures with observable herald probabilities p_n>=p_*>0 terminal test and its future policy code unavailable before the herald fixed decoder depends only on counted current label and requested test own-test rejection zero and cross-test rejection at least 0<s<=1 each specified experiment has target expected cost at most B TV approximation of every complete stopped record at error delta

**Conclusion.** delta<=p_*s^2/(32M^2) implies J<=binom(M,floor(M/2)); delta<=p_*s^2/(32J^2) implies M>=a(J).

**Direct logical prerequisites.** `lem:r77-robust-antichain`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Joint-event TV controls herald mass and herald-plus-rejection mass before normalization. Causality gives one conditional hidden-label row shared by all later tests. Diagonal response is at most 2delta/p_* and cross response at least s/2, leaving a strict factor-two margin in the antichain condition.

**Classical ingredients and priority boundary.** event characterization of total variation; causal nonanticipation. A general causal preparation/test memory certificate derived from full joint stopped-record error, without physical decoder restrictions or unjustified rare-event conditioning.

**Limits.** Both mixed and pure starts without an extra pure surcharge; no uncounted-history decoder access; no unconditional-to-conditional TV shortcut.

## 14. Unrestricted finite certificates and arithmetic rates

**Native locator:** main, theorem 8.3, page 27; `thm:r77-unrestricted-qubit` in `sections/51-unrestricted-approximation.tex`.

**Hypotheses.** undamped R75 qubit instrument with initial I/2 and fixed Bloch angle theta visible adaptive stopped experiments with target expected calls at most fixed B>0 cost-free terminal POVMs and no additional entangled register arbitrary causal classical decoder tables with no advance access to later terminal requests non-root phase for separated finite certificates; original z=(3+4i)/5 or stated badly-approximable hypothesis for explicit growth

**Conclusion.** delta<=zeta*8^(-J)*s_J^2/(32J^2) gives both unrestricted classical minima at least a(J). At the original phase delta<=25*zeta/(128*200^J*J^2) suffices. Fixed-B growth has liminf coefficient at least one relative to log_2 log_8(1/delta) in the stated arithmetic cases.

**Direct logical prerequisites.** `thm:r77-operational-antichain`, `lem:r75-noisy-physical`, `thm:r76-physical-logarithm`

**Inherited mechanisms and contextual authorities.** `thm:r76-return-approximation`

**Proof mechanism.** Early-abort prefixes 1 0^n have controlled target cost and prepare pure orbit states. Terminal complement projectors expose them with separation s_J. Integer real numerators give exponential separation for the original phase; a separate sine/Diophantine argument handles badly approximable phases. Inherited orbit-seed dictionaries give the upper.

**Classical ingredients and priority boundary.** integer numerator separation; root-of-unity integrality; elementary sine inequality. A quantitative unrestricted classical-memory lower for the actual stopped experiment, including the original algebraic Bloch phase. It complements rather than extends the stronger restricted physical-dictionary lower.

**Limits.** Unrestricted log-log lower does not match the logarithmic upper; no badly-approximable assertion for the original angle; no report-only approximate lower; no additional pure-start lower; no simulator expected-duration bound or continuum-command rate. The unit-circle phase is the Bloch rotation; the actual unitary uses the corresponding half angle. The original algebraic phase has an inherited rational seven-seed upper. The logarithmic upper versus log-log lower gap remains open.

## 15. Every non-root algebraic phase has the same lower order

**Native locator:** main, corollary 8.4, page 29; `cor:r77-algebraic-unrestricted` in `sections/51-unrestricted-approximation.tex`.

**Hypotheses.** algebraic unit phase z not a root of unity same causal qubit simulation and fixed-B assumptions as the preceding theorem degree D and integer A>0 with Az integral H>=max(2,A^D product_(j=2)^D max(1,|z_j|))

**Conclusion.** s_J>=4^(-D)*H^(-2(J-1)); delta<=zeta*H^4/[32*16^D*(8H^4)^J*J^2] implies N_cl>=a(J), and the fixed-B log-log liminf coefficient is at least one.

**Direct logical prerequisites.** `thm:r77-unrestricted-qubit`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The norm of the nonzero algebraic integer A^q(z^q-1) is a nonzero integer. Bounding the other conjugates gives exponential separation; substitute it in the preceding finite certificate.

**Classical ingredients and priority boundary.** integrality and multiplicativity of algebraic norms. An application of the classical algebraic norm to obtain explicit unrestricted-memory divergence for every non-root algebraic unit phase.

**Limits.** No polynomial Diophantine separation or sharp exponent; no matching unrestricted logarithmic lower. The algebraic norm estimate is classical and exponential; its priority keys refer to the inherited antichain ingredient, not a claim that those papers supplied the norm estimate.

## Retained authority and unresolved questions

All 220 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74/R75/R76 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R77.

The original general-M squared-sign risk frontier, arbitrary nonrigid tied control/stopping, unrestricted high-contrast classification for every finite group, the matching unrestricted-decoder approximation rate, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The inherited R76 matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.

## Evidence categories

The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R77.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.
