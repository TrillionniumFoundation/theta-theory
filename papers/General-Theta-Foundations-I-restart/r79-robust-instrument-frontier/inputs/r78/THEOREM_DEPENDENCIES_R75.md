# R75 theorem dependencies, hypotheses and claim boundaries

This is an author dependency addendum for General Theta Foundations I. It keeps the full 197-entry predecessor catalog and its proof authority at `inputs/r74/THEOREM_DEPENDENCIES.json`; the current complete catalog has 209 entries. Eleven of the twelve current additions are in the main article, and the stopped-approximation theorem is in the supplement. A supporting classical lemma is counted as a statement without being claimed as a new classical theorem.

## How to read the map

**Direct logical prerequisites** are results actually used as premises in the current proof. **Inherited mechanisms and contextual authorities** identify a reused construction, a special case or a related retained theorem, including a mechanism proved again here. Definition labels and internal proof facts are recorded separately. Automatically extracted statement/immediate-proof references in the JSON are syntactic evidence, not a substitute for this mathematical analysis.

The compiled locations below are taken from the actual paired native index. The index and current source hashes are pinned in `provenance/R75_PROOF_DEPENDENCIES.json`. The final Git identity is assigned by the source/publication handshake. No unexecuted computation, human review or editorial decision is asserted by this map.

## 1. Fourier multiplicity and real descent

**Native locator:** main, lemma 6.1, page 17; `lem:r75-fourier-multiplicity` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** A finite group G, a finite nonempty output set C, and a probability table b:G->Delta(C); the action on the table need not be faithful. All output Fourier matrices are stacked vertically, and V_b is the real cyclic span of the left translates. For the descent assertion, U and V are arbitrary finite-dimensional real G-modules.

**Conclusion.** The multiplicity of rho in V_b complexified is rank A_rho(b); the trivial multiplicity is one. A real equivariant injection exists exactly when all complex irreducible multiplicities are dominated, including complex and quaternionic real types.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** None beyond the classical framework credited below.

**Proof mechanism.** Classical Fourier decomposition identifies the rho cyclic block with {A_rho M}, which has rank(A_rho) row copies. A complex injection A+iB descends because a nonzero maximal minor of A+zB is a real polynomial nonzero at i and therefore at some real z; the degree bound gives a finite candidate list.

**Classical ingredients and priority boundary.** Complete reducibility and finite group-algebra decomposition; Matrix-coefficient orthogonality; A nonzero polynomial has finitely many roots. Classical representation-theoretic mechanism stated and proved in the precise multi-output conventions required here; not a claim to invent Fourier decomposition or real descent.

**Limits.** A linear multiplicity criterion alone is not a positive factorization. The next theorem separately proves stochastic positivity.

## 2. Exact orbit multiplicity at small contrast

**Native locator:** main, theorem 6.2, page 18; `thm:r75-orbit-multiplicity` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** Finite G and C, b:G->Delta(C), group mean pi, and b_t=pi+t(b-pi), 0<=t<=1. For the restricted count, a prescribed subgroup H and disjoint copies of H\G; missing active irreducible types give infinite copy number. For the unrestricted cover, one representative of every subgroup conjugacy class; the pure-start formula is applied only when G is the observable group.

**Conclusion.** For every positive contrast, q_H(b_t)>=max_rho ceil(r_rho/m_rho(H)); this is attained on an explicit positive interval whenever finite. The integer multiplicity cover gives the exact permutation-module minimum and the unrestricted positive core at sufficiently small positive contrast.

**Direct logical prerequisites.** `lem:r75-fourier-multiplicity`, `thm:r73-memory-formula`

**Inherited mechanisms and contextual authorities.** `thm:r74-low-contrast`, `eq:r73-module-bounds`

**Proof mechanism.** Semisimplicity embeds the response subquotient in every realizing permutation module. Frobenius reciprocity counts each coset orbit. A real embedding of the centered response, invariant orthogonal projection, a uniform preparation perturbation, and a bounded decoder perturbation give the matching positive factorization on any prescribed adequate action. Zero-mean output columns are restored as zero columns.

**Classical ingredients and priority boundary.** Frobenius reciprocity; Invariant inner products and complete reducibility; Finite integer covering; Positivity by mixing with a strictly positive average. Exact action-restricted resource count and its unrestricted multiplicity-cover form. The positivity mechanism extends the retained R74 construction and is reproduced explicitly.

**Limits.** Small positive contrast only for matching general synthesis; q_H is not kappa/[G:H] in general. At t=0 one copy suffices. No arbitrary full-contrast nonnormal-group LP is asserted.

## 3. Normality is the exact single-orbit convexity boundary

**Native locator:** main, theorem 6.3, page 19; `thm:r75-normality-convexity` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** A finite group G, subgroup H, and transitive right action X=H\G of degree d. Binary terminal responses on exactly this one orbit, with arbitrary probability preparation and stochastic decoder; no additional hidden orbit or mixture label is supplied.

**Conclusion.** The binary single-orbit response set is convex exactly when H is normal. In the nonnormal case the averaged return character witnesses failure at every positive contrast; an irreducible block with 0<m_rho(H)<d_rho gives sup-norm distance at least t*m_rho(H)/(d*d_rho).

**Direct logical prerequisites.** `lem:r75-fourier-multiplicity`

**Inherited mechanisms and contextual authorities.** `lem:r74-normal-orbits`

**Proof mechanism.** Normal H gives exactly all H-invariant probability tables by a point preparation. If H is nonnormal, its group-algebra averaging projection is noncentral, so some irreducible fixed-space rank is strictly between zero and full degree. The normalized permutation character has a full scalar Fourier block there, which a single orbit cannot carry. A kernel vector of every competing rank-deficient block yields the quantitative margin.

**Classical ingredients and priority boundary.** Centrality of the subgroup average iff the subgroup is normal; Permutation characters and Frobenius reciprocity; Operator-norm separation from rank-deficient matrices. Necessary and sufficient convexity classification for a fixed transitive probability-response action, with an explicit positive-contrast obstruction.

**Limits.** The displayed distance is a rigorous lower bound, not a claimed sharp distance for all actions. The result concerns the specified action and does not preclude other formulations or larger positive cores.

## 4. Full-contrast return-law rigidity

**Native locator:** main, lemma 6.4, page 20; `lem:r75-return-rigidity` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** A finite mixture of positive-weight components on copies of one fixed transitive d-point G-action X, with probability preparations and scalar decoders in [0,1]. The mixed response has value one at the identity and uniform group average 1/d.

**Conclusion.** Each active component has a point preparation and the matching point-indicator decoder, hence is a pure return law.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** None beyond the classical framework credited below.

**Proof mechanism.** Identity value one forces each decoder to equal one throughout its preparation support. Transitivity makes its group average the decoder average, at least 1/d. Equality of the mixture average forces support size one and zeros off that point in each active component.

**Classical ingredients and priority boundary.** Equality in a convex combination of numbers bounded by one; Uniform averaging on a transitive action. Elementary equality lemma used to certify the full-contrast endpoint; no separate broad novelty claim.

**Limits.** The common orbit degree and positive mixture weights are essential. The symmetric-group theorem separately excludes other orbit types before applying it.

## 5. A sharp singular-coefficient bound and its equality case

**Native locator:** main, lemma 6.5, page 20; `lem:r75-singular-coefficient` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** n>=5, t>0, and P=I-11^T/n. A is a real entrywise nonnegative n by n matrix with rank(A)<n, total entry sum one, and PAP=(t/n)P. No symmetry or positive-semidefiniteness of A is assumed.

**Conclusion.** t<=(sqrt(n)-1)/(sqrt(n)+1). Equality holds precisely, up to simultaneous row/column permutation, for A_*=(n-1)^(-1) sum_{i<n} ell_i^T ell_i, ell_i=(1-1/sqrt(n))e_i+(1/sqrt(n))e_n; extremal symmetry is forced.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** None beyond the classical framework credited below.

**Proof mechanism.** A normalized left null vector gives A=(t/n)(I+c1^T-1v^T), v.c=0 and sum(c)=1/t. Entrywise positivity yields lower bounds controlled by the largest, second largest and most negative v coordinates. A strictly concave one-variable bound reduces to two endpoints; AM-GM gives the sharp constant. Equality forces one negative null coordinate and a unique slack support, hence A_*. Orthogonal centered probability rows prove attainment.

**Classical ingredients and priority boundary.** Rank-one row/column decomposition under centering; Left null vectors; A concave quadratic attains its minimum at an endpoint; Arithmetic-geometric mean inequality. Sharp inequality and complete equality classification proved in this revision for a nonsymmetric nonnegative singular-matrix class. This is an author claim with a full elementary proof, not an exhaustive priority certificate.

**Limits.** The stated dimension restriction n>=5 is used in strict equality separation; no extension of this uniqueness assertion to n<=4 is claimed. The lemma does not assume or classify a chosen hidden implementation.

## 6. The exact two-level nonabelian memory law

**Native locator:** main, theorem 6.6, page 22; `thm:r75-symmetric-return` in `sections/42-nonabelian-memory.tex`.

**Hypotheses.** n>=5 and binary S_n response beta_t(g)=(1-t)/n+t*chi_n(g)/n for 0<=t<=1. For positive contrast, arbitrary finite exact stochastic controllers under the retained prepared-response interface; all finite G-set orbit types are permitted in the positive-core reduction. The equality classification concerns minimum permutation cores at the attained threshold, not all unreduced stochastic implementations.

**Conclusion.** For t>0, observable group S_n, residual count n!, dimension 1+(n-1)^2 and module bound n(n-1). With tau=(sqrt(n)-1)/(sqrt(n)+1), kappa is n(n-1) on 0<t<=tau and n^2 above; pure memory adds one. At tau every minimum core has n-1 natural orbits and precisely the stated ell_i preparations and D_i=ell_i/((n-1)w_i), with sum(w_i)=1 and w_i>=(1-1/sqrt(n))/(n-1). At t=0 both minima are one.

**Direct logical prerequisites.** `lem:r75-fourier-multiplicity`, `lem:r75-return-rigidity`, `lem:r75-singular-coefficient`, `thm:r73-memory-formula`

**Inherited mechanisms and contextual authorities.** `thm:r73-normal-form`, `thm:r74-contrast-thresholds`

**Proof mechanism.** The full standard Fourier block fixes the observable invariants. Counting natural point-orbits of every subgroup gives the unrestricted index lower and a strict penalty for nonnatural standard carriers. Any core below n^2 therefore has exactly n-1 natural carriers; all extra-orbit contributions are constant and can be absorbed into their decoders. Its coefficient matrix is nonnegative singular with PAP=(t/n)P, so the sharp lemma gives the exact lower. A_* gives the threshold controller and decoder mixing all smaller contrasts; n natural return orbits give the upper above threshold. Nonnegative rank-one support/ratio rigidity classifies every minimum threshold factorization. The retained pure-start formula completes the count.

**Classical ingredients and priority boundary.** Standard representation of S_n and character orthogonality; Subgroup index and factorial-product bounds; Nonnegative rank-one factorization support; Permutation-sum row/column swaps. Exact all-contrast resource law, matching constructions and endpoint rigidity for an unbounded nonabelian family. The rational low-contrast and full-contrast arguments are retained as additional explicit results.

**Limits.** The equality classification stops at the permutation-core level. The two-command prepared quantum realization proves physical availability, not minimal Hilbert dimension or a common-resource quantum advantage. The relative gap tends to one. No A1/A2 or full Theta-pipeline completion follows.

## 7. Stationary initialization law

**Native locator:** main, theorem 9.1, page 31; `thm:r75-stationary-initializer` in `sections/43-stationary-initialization.tex`.

**Hypotheses.** A nonempty finite command alphabet with finite report sets and an observable response predictively stationary under a full-support command mixture. All future-word stationarity equalities are required; when terminal decoders are part of the experiment, all word/readout identities include the empty word. Mixed and pure minima use arbitrary real nonnegative edge-emitting tables, with a prescribed pure initial label counted; no irreducibility or minimal linear-state assumption.

**Conclusion.** The minima are both one for a one-label response, and otherwise n_pure=n_mix+1, with infinity+1=infinity. A stationary hidden row for the averaged command can be chosen without enlarging a mixed realization.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** None beyond the classical framework credited below.

**Proof mechanism.** Predictive stationarity writes the initial future function as a convex combination of hidden future functions. Unless the one-label exception holds, eliminate the initial label and redirect every transition into it using the same normalized coefficients; induction includes zero-length terminal readout. Conversely one counted initializer executes the first actual command into any mixed core. Cesaro averaging preserves every future response and supplies a stationary averaged-command hidden row.

**Classical ingredients and priority boundary.** Positive realizations and future-response functions; Convex elimination; Cesaro averaging of finite stochastic matrices. A general exact relation between two initialization conventions in the classical positive-realization framework; neither that framework nor stationarity itself is newly claimed.

**Limits.** Full-support observable stationarity and all terminal quantifiers are material. This is an edge-emitting process theorem. External policy memory, coefficient bit length and exact sampling cost are separate.

## 8. Stationary processes

**Native locator:** main, corollary 9.2, page 31; `cor:r75-stationary-process` in `sections/43-stationary-initialization.tex`.

**Hypotheses.** An ordinary stationary finite-alphabet process that is not i.i.d. Edge-emitting HMM realizations, with freely mixed initialization compared to a counted prescribed pure label.

**Conclusion.** The minimum pure-start HMM has exactly one more label than the minimum mixed-start HMM, with the infinite-value convention.

**Direct logical prerequisites.** `thm:r75-stationary-initializer`

**Inherited mechanisms and contextual authorities.** `thm:r74-depolarizing-obstruction`

**Proof mechanism.** Specialize the general controlled initialization theorem to one command. The same-source Cesaro argument identifies the freely mixed convention with a stationary hidden-row convention.

**Classical ingredients and priority boundary.** One-command specialization of observable stationarity. A corollary of the general R75 initialization theorem; the previous q/q+1 example is an application, not a premise needed for this proof.

**Limits.** Not a new solution of the unrestricted minimum positive-state realization problem, and not a claim for a different state-emitting model convention.

## 9. Physical margins and predictive rank

**Native locator:** main, lemma 10.1, page 32; `lem:r75-noisy-physical` in `sections/44-noisy-instruments.tex`.

**Hypotheses.** The displayed complete three-report qubit instrument, retention parameter 0<=alpha<=1 and any real angle theta; initial state I/2. For rank three, alpha>0 and sin(theta)!=0; the zero-retention endpoint is handled separately.

**Conclusion.** All branches are completely positive with the displayed report floors, sum exactly to depolarization, and give fixed-command stationarity and one-dependence. The explicit cylinder has three independent modes and predictive rank three at nonreal positive retention, and rank two at zero retention; the response is never one-label.

**Direct logical prerequisites.** None; the proof is given directly from the listed hypotheses and classical ingredients.

**Inherited mechanisms and contextual authorities.** `thm:r74-depolarizing-obstruction`

**Proof mechanism.** Choi-matrix norm bounds give a positive I/16 margin for the complement branch. The rank-one report resets to tau, allowing direct iteration of the damped rotation and the cylinder formula. A nonzero Vandermonde minor gives rank three; the zero-retention two-by-two Hankel minor gives rank two, with a matching two-dimensional reachable diagonal space.

**Classical ingredients and priority boundary.** Choi positivity; Vandermonde independence; Finite response/Hankel rank. Physical and rank verification for this complete damped family, extending the retained undamped example. Low-rank non-HMM phase mechanisms and one-dependent examples have prior antecedents.

**Limits.** Fixed-command stationarity and one-dependence are not claims about feedback-controlled records. The pure-reset branch violates the R68 every-posterior interior hypothesis at every block length, so that theorem is not being applied here.

## 10. Relative cylinder obstruction and polygon realization

**Native locator:** main, lemma 10.2, page 33; `lem:r75-full-instrument-bounds` in `sections/44-noisy-instruments.tex`.

**Hypotheses.** The complete instrument of the preceding lemma; alpha>0 and sin(theta)!=0 for the arbitrary-HMM lower. For the upper, a regular q-gon of actual pure qubit states, q>=3, with a reset vertex and alpha*exp(i*theta) in that polygon; the same condition may hold for a whole command family.

**Conclusion.** Every M-label mixed realization forces alpha*exp(i*theta) into the M-state stochastic eigenvalue region. Conversely the polygon supplies an exact q-label realization of all report branches, word states, terminal POVMs and common adaptive policies, using one dictionary for all eligible commands.

**Direct logical prerequisites.** `lem:r75-noisy-physical`, `prop:r70-relative-spectrum`

**Inherited mechanisms and contextual authorities.** `lem:r70-core`

**Proof mechanism.** Positive entrance/exit paths bound the productive zero-report core by C*8^(-n). Cayley-Hamilton forces the observed nonreal eigenvalue into a productive irreducible block; Perron normalization there and a stationary-row contraction yield the exact normalized stochastic eigenvalue. For the upper, branch zero preserves the polygon, branch one resets to its vertex and branch two has normalized Bloch norm at most 5/11, inside every eligible polygon. Barycentric branch interpolation proves the full subnormalized-state identities.

**Classical ingredients and priority boundary.** Perron-Frobenius normalization on one irreducible block; Cayley-Hamilton; Invariant physical-state dictionaries and barycentric interpolation. A matched necessary spectral obstruction and sufficient complete-instrument construction; the relative-spectrum mechanism is inherited and its reducible-core proof is explicitly carried through here.

**Limits.** The entire stochastic eigenvalue region is only a necessary condition, not proved sufficient for arbitrary full instruments. The upper is restricted to the actual invariant polygon and its qualifying angle family.

## 11. Sharp noisy-instrument memory

**Native locator:** main, theorem 10.3, page 34; `thm:r75-noisy-memory` in `sections/44-noisy-instruments.tex`.

**Hypotheses.** The displayed complete noisy qubit instrument; first sector M>=3, 0<theta<=2*pi/M, 0<alpha<=1. For the common all-angle count, 0<alpha<1; a finite alphabet has the same upper and a matching lower when it contains a worst phase. Pure-start counts use the stationary-response theorem; zero-retention and undamped endpoints are stated separately.

**Conclusion.** Exact first-sector mixed feasibility alpha<=1/(cos(theta)+sin(theta)tan(pi/M)), with exact M/M+1 counts and zero-report lazy-cycle Perron rigidity at equality. The simultaneous all-angle mixed optimum is K=max(3,ceil(pi/arccos(alpha))), with pure optimum K+1. At alpha=0 the counts are 2/3; at alpha=1 the full family is infinite, with inherited fixed-phase finite/infinite alternatives.

**Direct logical prerequisites.** `lem:r75-noisy-physical`, `lem:r75-full-instrument-bounds`, `lem:r69-sector`, `thm:r75-stationary-initializer`, `thm:r74-depolarizing-obstruction`

**Inherited mechanisms and contextual authorities.** `thm:r69-sector-phase`, `thm:r69-worst-phase`

**Proof mechanism.** The necessary spectrum and actual polygon upper meet on the classical first-sector chord. Strict smaller-size sector exclusion forces the full carrying block, and applying the sector bound before radial contraction fixes its Perron root at 1/8 and the normalized lazy cycle. A polygon containing the whole radius-alpha disk gives one all-command dictionary; one critical phase gives its matching lower. Explicit two-state rational branch tables settle zero retention. The general initializer theorem gives every pure charge.

**Classical ingredients and priority boundary.** Classical stochastic sector inequality and boundary equality case; Regular-polygon inradius; Perron normalization. Exact complete-instrument and simultaneous-command realization results using inherited spectral geometry. The sector curve and inverse-square-root worst-phase exponent are not claimed as new classical spectral discoveries.

**Limits.** Rigidity is for the zero-report matrix up to diagonal similarity, cyclic relabeling and orientation; the other branches are not uniquely classified. No full fixed-angle formula outside the proved regimes is claimed. The R71 arithmetic lift is inherited reasoning, not a new number-theoretic theorem.

## 12. Stopped-law approximation from conditional damping

**Native locator:** supplement, theorem S1.1, page 1; `thm:r75-stopped-approximation` in `supplement-r75-conditional.tex`.

**Hypotheses.** A finite angle command alphabet, initial qubit I/2 and target retention alpha=1. One class of common randomized command/stopping/terminal-POVM policies, each with target expected calls E_1^pi(tau)<=B<infinity; no external quantum register entangled with the qubit. One approximate model with retention 1-epsilon, 0<epsilon<1, is chosen independently of the policy; the epsilon=1 and B=0 cases are explicit.

**Conclusion.** Uniform complete stopped-law total variation, including the nontermination atom, is at most epsilon*B/8. The stronger terminal classical-quantum trace-distance estimate holds with a scalar nontermination block. Pure memory at tolerance delta is at most 1+max(3,ceil(pi/arccos(1-8*delta/B)))=(pi/4)*sqrt(B/delta)+O(1) in the stated regime; an L-label policy adds the explicit product-core account.

**Direct logical prerequisites.** `thm:r75-noisy-memory`, `lem:r75-full-instrument-bounds`

**Inherited mechanisms and contextual authorities.** None beyond the classical framework credited below.

**Proof mechanism.** The two opposite branch perturbations have one-call flagged trace distance at most epsilon*tr(X)/8 for a positive single-qubit input. Finite-horizon telescoping keeps every changed-call prefix entirely target, weighting error by target survival probabilities. Common positive trace-preserving tails contract the difference. Retaining all finite stopped blocks and merging unfinished histories into a scalar block yields the infinite-horizon limit, including nontermination. The exact noisy dictionary and initializer provide the memory upper.

**Classical ingredients and priority boundary.** Trace-norm contraction of positive trace-preserving maps on Hermitian inputs; Hybrid telescoping; Tail-sum formula for expected stopping time; Monotone limits of stopped blocks. A uniform bounded-target-cost implementation upper for the complete controlled stopped experiment, with a counted memory construction; not a new generic telescoping principle.

**Limits.** The budget is under the target, not the approximation. The latter may have nontermination mass and unbounded expected cost. No matching approximation lower or optimal exponent is proved, and the one-call constant excludes an entangled external quantum register.

## Retained mathematics and unresolved scope

The old R74 dependency records, including the normal-subgroup LP, dual certificates, algebraic synthesis, fixed four-bit model, constructive contraction theorem and undamped instrument theorem, remain unaltered as mathematical authorities. Their actual compiled document/number/page fields are updated in the complete catalog. Every one of the 197 inherited labels remains present. The exact symmetric-group threshold is now proved in closed form; the earlier interim statement that only an attained algebraic threshold was known is superseded by the sharp coefficient lemma, not left as a current open problem.

The general full-contrast nonnormal-group synthesis problem, optimal fixed-angle complete-instrument memory outside the proved regimes, sharp approximation lower bounds, common-resource quantum/classical comparisons, unknown-model identification, A1/A2 and the broader Theta pipeline are not solved by these statements. The R71 arithmetic envelope and exponents transferred to the complete instrument are inherited reasoning, not additional new numbered arithmetic theorems.

## Evidence categories

The written proofs are ordinary author arguments. The author-team AI challenge is a separate source-hashed reading, not independent human refereeing. Finite exact and floating diagnostics test named fixtures and identities; native LaTeX checks source closure and locators. None of these is a formal proof certificate, a priority clearance or an editorial decision. The controlling deposited R65 report has not been reclassified as a review of R75.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. The process requires the actual 209-entry compiled index, validates every current named dependency, preserves each predecessor proof record, and refuses missing or duplicate labels.
