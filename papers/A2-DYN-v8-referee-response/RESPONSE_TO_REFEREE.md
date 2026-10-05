# Response to the A2-DYN referee — revision 8

We thank the referee for distinguishing the value of the physical arithmetic, raw-edge and clock arguments from the missing analytic steps in the central local limit problem. We retain the original raw, parameter-uniform mixed-density endpoint and the entire preceding mathematical development. We do not adopt the suggested alternative of a lower-scope module paper. This revision adds four proved statements, rather than relabeling the v6 source or asserting the missing estimates.

## Frozen source and actual chronology

The controlling report is the 5 October 2026 report at `reviews/a2-dyn-v4-external-top4-review-2026-10-05/REFEREE_REPORT.md`, commit `a81eb226c013ca062a6901bb472a90668de29eec`, blob `1af8fb198d0361782cdca21f1d91a81d48ec1300`. It reviewed `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`, whose v5 branch name was an alias for v4 mathematics. The later v6 source already contains new phase, return-tail, moving-chart and conditioned-clock arguments; the subsequent v7 at `52278437b6313f1ad5eb53dd95c306f2651f30cb` merely preserves it. We therefore revise that latest complete source, not the older reviewed article. All nineteen v6/v7 core files remain byte-for-byte identical. All eight historical v6 diagnostic scripts are also retained; new diagnostics are additional.

## 1. The paper's endpoint

The endpoint is unchanged: the full parameter-uniform raw local limit for the actual joint displacement, collision count and flight time, with conditioned physical-time consequences. The title and physical table are unchanged. The original Fourier inversion and downstream statements remain present.

The new cumulative-return theorem proves `Pr(N_n>L) <= A exp(an-cL)` uniformly in the radius and both integer parameters. The proof compares the number of actual section visits with the fixed smooth killing weight, then applies the already established collision-space estimate to a single trajectory. It does not multiply dependent return probabilities. It gives a fixed complex exponential-moment domain for the entire record, where the earlier Holder bound had a domain shrinking as `1/n`.

The new finite-band proposition changes the sufficient collision cutoff from `n log(V/epsilon)` to `n + log(V/epsilon)`, including polynomially weighted insertions and fixed-order Fourier derivatives. In particular, on exponentially expanding bands the required physical collision count is linear in the return count. These are estimates for the actual unsmoothed measure. The full raw LLT is not announced as proved: the remaining anisotropic, covariance/cohomology and all-branch estimates are identified precisely below, not silently promoted to consequences of these new bounds.

## 2. Moving-domain continuity

The complete moving-domain/coarea development in `11_return_stability.tex` and `16_common_charts.tex` is preserved, including excluded singular neighborhoods, regular chart matching and domination. The v6 moment upgrades are retained.

The new common-scale theorem adds strong parameter continuity of the actual weighted n-return transfer operators `L^p -> L^q`, `q<p`, at every fixed complex parameter in the proved tube. Its proof explicitly removes forward and backward collision singularities and finite iterates of the moving section boundary, stabilizes the finite backward return itinerary, obtains pointwise convergence first for continuous inputs, and uses an exponent with slack for uniform integrability. General inputs are obtained by density. For `p=infinity`, approximation is made in a sufficiently large finite exponent, not by the false claim that smooth functions are norm dense in `L^infinity`.

This is strong continuity for a fixed input, not operator-norm continuity in the radius, and it is not used to bypass the coarea analysis of the raw densities.

## 3. Phase separation and the operator estimate

The existing one-step coercivity and Fredholm phase-reconstruction criterion in `17_operator_bridge.tex` remain in theorem form, with their regularity and nonvanishing hypotheses visible.

The new renewal theorem supplies an actual common realization on `L^1(M,nu)` with the hard section projection, for which that projection is genuinely bounded. It proves the chronological first-return decomposition, the exact damped renewal identity and the Schur-complement formula. At the damping boundary, convergence is strong for each input; operator-norm convergence is not asserted. Its iterates pair to the true n-return physical record, not an independent block model.

The new holomorphy theorem then constructs the unbounded twists directly on a common Lebesgue scale across the damping boundary. Its fixed complex domain comes from the new cumulative exponential moments. We explicitly distinguish this construction from a quasi-compact anisotropic endomorphism. At real frequencies the induced `L^1` operator is an isometry; neither spectral contraction nor a resolvent bound follows from its existence. Compatibility with these exact physical operators is now an explicit requirement for the anisotropic realization still to be proved. In particular, approximate spectral vectors are not asserted to possess regular, nonvanishing phases without proof.

## 4. Individual and all-branch edges

Every original critical-word, jump-coefficient and exact-subtraction proof in `04_raw_edges.tex` remains unchanged. The absolute second-derivative summation criterion in `19_raw_closure_contracts.tex` is retained. No symbolic word count is hidden in a coefficient bound.

The new physical-count truncation includes all discarded trajectories, regardless of itinerary multiplicity, because it is a total-variation estimate before pushforward. It therefore improves the finite-band budget without an uncontrolled count of words. It does not bound the variation of inverse coarea Jacobians or sum all remaining critical and singular branches. We explicitly do not infer a pointwise density estimate or an infinite-frequency integral from this finite-band total-variation bound. Verification of the all-branch residual derivative sum remains necessary for the full raw LLT.

## 5. First-order and square-root clocks

The first-order clock section is preserved. The later v6 `18_conditioned_clock.tex` is also preserved: it proves an exponential maximal-block bound over a growing stationary interval, including the initial length-biased block, and the logarithmic bound after conditioning on events with polynomially small probability. The square-root path-comparison estimate is thus retained as an actual later improvement over the reviewed v4.

The v8 cumulative-count estimate concerns a different object, the total collision time of n returns. It is not presented as a second proof of an already available maximal-block theorem. Nor is either estimate treated as a completed functional Gaussian theorem for the completed blocks, or as authority to replace an exact lattice conditioning event without controlling the symmetric difference relative to its probability.

## 6. Version identity

The manuscript date, directory, source manifest, author branch, referee-copy branch and qualification workflow all identify revision 8. The nineteen preserved core files are audited by exact SHA-256 identity and their common preceding Git tree, while the two new mathematical files are included in the article. This prevents another v4/v5-style alias from being mistaken for mathematical progress. The exact-source workflow records the tested commit, all TeX source hashes, PDF hash, diagnostics and recorder log. Earlier manuscripts and unrelated repository paths remain unchanged.

## 7. Dynamics-specific independent proof review

We have not represented author-side calculations, finite tests or successful typesetting as independent human verification. No independent billiards specialist has been contacted through this revision. The referee-copy branch supplies the full article, detailed response, proof ledger and exact-source evidence for the requested subsequent review. The main load-bearing passages for that review are the collision-space spectral input and soft killing, the moving return-domain coarea argument, the periodic action/coercivity argument, and the new cumulative-count and common-scale operator proofs.

## Present mathematical status

The four new statements are Theorem `thm:cumulative-return-tail`, Proposition `prop:linear-count-budget`, Theorem `thm:common-renewal`, and Theorem `thm:common-scale-holomorphy`. Their proofs appear in the full article. Their continuum conclusion is not inferred from the finite diagnostics.

The full LLT still requires an anisotropic induced realization compatible with the actual renewal operators; regular phase reconstruction/measurable-cohomology input; covariance summability and period-evaluable zero-variance rigidity; and estimates for the full raw critical/singular residual decomposition. The earlier conditional inversion theorem remains the route to the original endpoint. This revision advances its cumulative integrability, exact operator identification and finite-band truncation steps without changing the endpoint or deleting any earlier argument.
