# Response to the v110 referee report — A2-DYN revision 111

**Qian Qi — October 14, 2026**  
**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**

The controlling report is the v110 persistent-guard review at commit `fb1240d2f8c0562a148d559df5a8d9c3bd2d5e39`, report blob `d57761aeb65b42940a974c8009f13ee47ffd6fce`. The reviewed author commit is `0abce3fcfbc735ff5cc6d085279abea5f32a7a22`. Its complete manuscript tree, `89ec727b370bf21d66d7086041f75d7868671d4b`, is preserved exactly in `archive/v110`. No original manuscript path or referee report is modified.

## 1. The principal objection and the new mathematical result

The report asks for a collision-uniform estimate on the persistent positive source, rather than another scalar certificate or an unscaled small-mass statement. Revision 111 proves a target-roof weighted physical summation theorem and uses it to pay specified original source classes in the required collision-normalized essential-height topology. This is a new summation argument, not a direct sum of the per-itinerary exponential bound from v109/v110.

The missing geometric step is that momentum-fiber multiplicity one does not imply roof-fiber multiplicity one. Theorem 9.2 proves the latter. For two actual trajectories of one lifted itinerary, convexity of the Cartesian length gives two support inequalities. When their endpoint gradients lie on a common ray, their physical lengths are strictly ordered by gradient magnitude. Equal roof and Gauss angle therefore force equal trajectories, even across disconnected regular components. The proof uses no continuation through a forbidden collision and no convexity of an angular word domain.

This yields at most one original physical trajectory per word at each roof–angle target. Theorem 10.2 then applies the retained uniform physical-word pressure bound at those targets. Removing any set S of marked stable factors gives

    || dF_#(prod_{i in S} c_i^(-1) 1_Pi nu_R^*) / dt ||_infinity
        <= C_star K_star^(|S|).

A full word is reconstructed from the unmarked blocks and the deleted physical step symbols. The latter have only D^(|S|) possibilities; each unmarked block is paid by its genuine stable-Jacobian pressure. Adjacent marks and empty blocks are explicitly included. No homogeneity-strip count and no unconstrained word-count multiplier is inserted.

Corollary 10.3 controls a changing family of incidence witnesses by elementary symmetric polynomials. If their thresholds are eta_i and A is their sum, the original roof density of the event that at least s witnesses occur is at most

    C_star (K_star A)^s / s!.

The original depth thresholds eta_i=2 epsilon q_0^(d_i/4) have bounded total sum, uniformly in m. This handles the changing witness without selecting one witness for a whole physical segment.

## 2. What is now paid in the actual normalized topology

Lemma 11.1 proves the exact domination c_per <= f <= A at every target roof. It uses the surviving coefficient c_per=(c-gamma V)_+, not the original coefficient c. Thus the new target-roof estimates apply directly to the original persistent positive submeasure.

Theorem 11.2 proves, for every finite count and every depth threshold L,

    || U_per[an incidence witness has depth >= L] ||_infinity
        <= C epsilon q_0^(L/4).

Taking L_m=ceil(4(2+eta) log(m+1)/|log q_0|) in this finite-count inequality gives the fully normalized bound

    sup_{R,n,k} m^2 || U_per[deep incidence witness] ||_infinity
        <= C epsilon(B) (m+1)^(-eta).

It therefore has zero collision-limsup height for each fixed B. The factorial estimate similarly pays states with at least s_m=ceil(4 log(m+e)/log log(m+e^e)) incidence witnesses. Their normalized upper bound is m^(-2+o(1)) at every fixed outer B.

These classifications depend on m, but no spectral window or outer band does. Both substitutions are made in inequalities already proved at every finite m for every L and s. They do not substitute a collision-dependent width into a fixed-window asymptotic estimate.

The original source is preserved by the exact nonnegative identity U_per=U_exc+U_loc. Corollary 11.3 shows that the old and new scalar residuals differ by a term with collision-normalized height zero, with the full original nongrazing capacity pool retained. No original coefficient is discarded without this payment.

## 3. What this revision does not infer

The target-roof pressure bound is unscaled. Its all-incidence consequence C epsilon cannot be multiplied by m^2 and called small at fixed B. The proof pays the collision-deep and high-multiplicity incidence classes because their finite-count bounds contain additional vanishing depth or factorial factors.

The retained source may still have shallow incidence witnesses and arbitrary-depth clearance witnesses, including tangency to an unvisited disk. A clearance is not a visited incidence, and no inverse-clearance estimate is obtained by substituting it into the marked stable-factor argument. Original critical entrances, section cuts and capacity deficiencies remain wherever the proved payments do not apply.

Accordingly the remaining estimate is equation (11.12), `eq:v111-remaining`, for the same exact-label raw pointwise theorem. Its full vanishing is not proved in this revision. The primary referee request is therefore not marked closed. This is a statement of the supplied proof's precise endpoint, not a change to the target, a negative theorem about the model, or an averaged substitute.

Relative to the report's proposed routes, revision 111 establishes the incidence part of Route C by a genuine target-roof weighted-summation theorem, and pays explicit classes in the required topology. It does not claim that every incidence/clearance class has thereby been paid.

## 4. Historical mathematical inputs and their boundary

The new geometric uniqueness argument is independent of a connected angular domain. It extends the convex Cartesian comparison in historical module 238 from equal momenta to a common momentum ray and then to equal roof–angle data.

The stable optical comparison omega <= C_0 c_m J^s T^m and the one-step inequality J^s T/c <= C_1 are precisely those of module 238. The finite physical alphabet and word-block decomposition come from module 239. The uniform pressure bound P_l(R)<=Q_star is the v100 theorem in module 241, not an interchange of a fixed-radius bound with a radius supremum. Exact copies of all three sources are included in `provenance` with their Git blob hashes recorded in the manifest.

The new pressure argument drops occupation, displacement and roof tests only in a positive upper bound. The original exact event and its normalization remain on the left side of every source estimate. A Gaussian m^(-2) factor is never imported into the unconditioned pressure constant.

The global roof–angle change-of-variables argument is supplied explicitly, including the null critical set and the null complement of the infinite-time regular set. The original positive pairing, variation payment and scalar reduction are retained as stated, rather than claimed to have received an independent full historical recertification.

## 5. Responses to the six presentation requests in report Section 14

**Joint Borel endpoint completion.** The proof of Lemma 7.1 now writes the endpoint values as limits of the Borel interior evaluations at a+ell/j and b-ell/j. The rational-partition total-variation argument therefore starts from an explicitly jointly Borel function on the closed normalized segment.

**Positive optical factor at a critical endpoint.** The proof of Theorem 8.1 now cites the exact denominator omega=R c_0 c_m/b_m and the positive coarea denominator chi. Its assertion includes the fixed Gauss direction at a critical endpoint and does not assign one direction-independent value there.

**Actual surviving coefficient.** The definition of P_B continues to be followed immediately by the statement that the coefficient is c-gamma_B V, not c. Lemma 11.1 uses exactly that coefficient in the new physical sum.

**Changing witnesses.** Corollary 10.3 states directly that witnesses can change with the target roof and angle and that no witness is chosen for an entire segment. The final source description distinguishes incidence-depth localization from clearance witnesses at any depth.

**Later v110 qualification.** A versioned provenance file, `provenance/v110-ci-observed-2026-10-14.json`, records that run 38528720288 subsequently completed successfully at the exact reviewed SHA, updated at 2026-10-14T07:55:16Z. The review's original queued-at-freeze statement is unchanged. This observation is v110 evidence only.

**Per-itinerary versus summed bounds.** The old multi-mark optical polynomial remains per itinerary. The new target-roof theorem has a separate proof using global roof–angle uniqueness, stable-cocycle factor removal and bounded physical-word pressure. The two statements are not conflated.

## 6. Manuscript and validation

The revised article is a standalone `amsart` manuscript. The original model, section, guard, arithmetic transition reference and governing pointwise assertion are unchanged. Sections 1–8 retain the preceding article; the two requested clarifications are local additions to its proofs. Sections 9–11 contain the new mathematics. Both preceding appendices remain in place. The full reviewed source and its historical derivations are preserved under `archive/v110`; original repository paths are not rewritten.

The active manuscript compiles to 25 pages. The final local log has no unresolved references, duplicate labels or overfull boxes. All pages were rendered for visual inspection. The new diagnostics passed 10,922 exact marked-word reconstruction cases, 1,641 exact witness-insertion cases, 702 exact depth-tail cases, and 144 pairs of actual two-disk trajectories with the original endpoint section tests. The trajectory calculations use double-precision Newton solves; the combinatorial checks use exact rational arithmetic. Normal and optimized Python outputs agree. The preceding optical/source diagnostic suite was also rerun successfully.

These are diagnostic and reproducibility checks, not a formal certificate of the continuum proof. The new GitHub workflow verifies its exact checkout, unchanged original tree, exact archived tree, frozen report and historical proof anchors before building the current article. It does not claim a successful v111 run before one is actually observed, and it does not describe archival tree preservation as a new compilation of all historical supplements.
