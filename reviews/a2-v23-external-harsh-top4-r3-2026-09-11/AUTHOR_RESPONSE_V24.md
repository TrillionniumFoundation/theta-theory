# Author response to the R3 external referee report

**Manuscript:** A2 — *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Revision branch:** `revision/a2-v24-uniform-physical-global-top4-2026-09-11`  
**Response date:** 11 September 2026

We thank the referee for isolating the remaining structural gaps.  We followed the report's preferred positive route: the scope and principal claims have not been reduced.  Instead the revision adds the missing physical uniform-estimability theorem, removes the prescribed lattice Gram metric from the deterministic flagship theorem, adds quantitative gluing hypotheses and a global inverse modulus, supplies explicit two-sided Markov kernels for the non-dominated Poisson experiment, and reformulates the count--endpoint limit invariantly.

## M1. Global statistical reconstruction was conditional on an unproved uniform-estimability hypothesis

**Resolved by a new physical theorem, not by weakening the claim.**

New Section `25a_uniform_physical_global_v24.tex` proves the following chain.

1. **Uniform finite positive design at each fixed jet order.**  The tangent inverse shows that every unit tangent direction at every table is detected by some positive-offset endpoint design.  Compactness of the unit tangent bundle over the compact analytic class gives a finite design list common to the entire class and a uniform positive lower information bound.
2. **Finite statistical separator atlas.**  For fixed order `M` and separation `eta`, the compact set of parameter pairs whose `D_M`-vectors differ by at least `eta` is covered by finitely many boundary-law separators.  Thus a finite, table-independent acquisition atlas separates every globally distinct finite coordinate vector at that resolution.
3. **Charged global centering pilot.**  Compactness supplies a common gap interval and threshold collar.  A deterministic timing scan gives a coarse onset bracket; the existing onset-zero interpolation then refines the gap.  Pilot records and preparation cost are retained.
4. **Actual finite-bridge fixed-order estimator.**  The post-pilot designs stop after fixed successful-record targets, use deterministic caps, and are compared at the complete stopped-transcript level by the existing adaptive physical transfer.  The common flight number is chosen so that `C R k tau^J` is arbitrarily small.  A minimum-distance estimator based on the finite separators is uniformly consistent for `D_M`.
5. **Growing-order physical reconstruction.**  The new global theorem chooses `M_s`, the finite design size `L_s`, success allocation `k_s`, flight number `J_s`, pilots and caps in that order and imposes `C L_s k_s tau^{J_s} <= 2^{-s}`.  Combining this with the finite-data inverse modulus yields uniform `C^q` table consistency for every fixed `q`.

Thus the earlier phrase “whenever uniformly consistent fixed-order estimators exist” is no longer the logical bridge supporting the main claim.  Such estimators are constructed from the declared physical experiment.

## M2. The previous intrinsic rigidity theorem assumed the full Euclidean Gram form of the marked lattice

**Strengthened.**  New Section `23d_rank_two_lattice_recovery_v24.tex` begins with only an oriented marked free abelian deck group `Lambda_top ~= Z^2`; no inner product, lattice shape, scale or direction is supplied.

For a signature-rigid cycle the data determine a Euclidean translation holonomy `v_c`, while the marked covering determines its combinatorial deck displacement `eta_c`.  The metric-free identity is

`R_0 v_c = L eta_c`,

where `L : Lambda_top tensor R -> R^2` is the unknown Euclidean realization.  Two cycles based in one channel frame with linearly independent `eta_1, eta_2` determine `L` uniquely after fixing the one global rotational gauge.  Consequently `G=L^T L` is recovered, including absolute scale.  A rooted signature-rigid spanning tree then determines all obstacle placements.  This is now the deterministic flagship theorem in the Introduction.

The deck label is stated operationally: it is a combinatorial lift label in the marked covering and part of the acquisition design; its Euclidean vector is not supplied.  Unknown/corrupted deck labels are a different inverse problem.

## M3. Singleton gluing was qualitative and did not give statistical stability

**Resolved on an explicit robust analytic class.**  New Section `23e_quantitative_gluing_stability_v24.tex` separates exact rigidity from stability and assumes uniform quantities that are statistically meaningful:

- a fixed holomorphic collar and analytic norm bound;
- positive curvature/separation bounds;
- a positive selected-channel persistence margin against competing contacts;
- a finite-signature separation margin at every incidence used in the anchoring cycles/spanning tree, modulo declared exact obstacle symmetries;
- a positive lower singular-value bound for the two rank-two holonomy vectors.

The section proves persistence of the prescribed gluing under finite-data perturbations and defines an explicit complete-data metric.  Compact injectivity then gives a uniform inverse modulus `omega_q(t) -> 0`; truncation at jet order `M` satisfies

`d_q(T,T') <= omega_q(C ||D_M(T)-D_M(T')|| + r_M)`, with `r_M = O(2^{-M})`.

The text now explicitly says that the identity theorem is used for exact uniqueness only; stable reconstruction is asserted only on this quantitatively compact holomorphic-collar class.

## M4. Reverse deficiency in the endpoint--time Poisson theorem was too compressed

**Resolved with explicit parameter-independent kernels and a Le Cam bound.**  New Section `18c1_endpoint_time_deficiency_v24.tex` defines a fixed reference ceiling layer and proves uniform layer/bulk estimates, including the symmetric-difference mass caused by the `o(k^{-1})` moving-support remainder.

- The forward kernel extracts the parameter-independent reference layer and rescales its slack.
- The reverse kernel takes the Poisson layer, maps its points back to records, fills the remaining sample slots from the **reference bulk conditional law**, and randomly interleaves the records.  It is independent of the unknown local parameter.
- Binomial--Poisson coupling controls layer counts/locations; product Hellinger control gives `O(k^{-1/2})` total-variation error for replacing the true bulk conditional law by the reference bulk.

The resulting theorem gives a uniform two-sided bound of the form

`Delta(E_{n,K}, P_K^R) <= C_K (epsilon_{n,K} + k^{-1/2}) + o_K(1)`.

The projective experiment is defined on locally finite point measures with the vague topology and the finite-window restriction kernels are stated explicitly.

## M5. The count--endpoint splitting depended on a noncanonical representative and `d gamma != 0` was asserted rather than proved

**Resolved invariantly.**  New Section `18d1_intrinsic_count_geometry_v24.tex` sets

`V = T_theta Theta_M`, `lambda = d gamma`, `H = ker lambda`, `N = V/H`.

The count factor lives canonically on the one-dimensional normal quotient `N`; `lambda` induces `N -> R`, and its information is `|lambda([v])|^2`.  Endpoint information is the restriction of the endpoint quadratic tensor to `R_gap direct-sum H`.  The theorem proves invariance under a `C^2` reparameterization and under changing the splitting vector `v_gamma`.

Nonvanishing is explicit.  From `c_b=1+g kappa_b` and `c_0 c_1=cosh^2 gamma`,

`partial gamma / partial kappa_0 = g c_1 /(2 sqrt(c_0 c_1) sinh gamma) > 0`,

and similarly for `kappa_1`.

## M6. The theorem hierarchy obscured the main contribution

**Reorganized.**  `main.tex` now uses `01_introduction_v24.tex`.  The Introduction identifies exactly two flagship results:

1. the deterministic uncalibrated periodic-rigidity theorem, including lattice-metric recovery; and
2. the statistical actual-finite-bridge global reconstruction theorem.

The Poisson/count/endpoint limits are presented as information-theoretic refinements for nested sigma-fields.  Revision history is not part of the theorem narrative; the response/provenance material remains outside the mathematical article.

## M7. Exact-head build certification

A dedicated v24 native-build workflow is added after the mathematical revision.  It checks out the exact revision head, runs the repository's canonical A2 submission builder, runs the boundary-information diagnostics under normal and optimized Python, rejects unresolved references/citations and fatal LaTeX diagnostics, and records source/PDF hashes as workflow artifacts.  The workflow status is the build certificate for the exact revision commit.

## Detailed comments D1--D4 and S1--S4

- **D1:** deck-class observability is now stated explicitly as a marked-cover acquisition label; its Euclidean realization is reconstructed.
- **D2:** the text distinguishes formal gluing classification from actual rigidity: rank-two holonomy and signature-rigid propagation are the substantive uniqueness mechanisms.
- **D3:** finite-signature, channel-persistence and holonomy singular-value margins are explicit hypotheses of the uniform statistical class.
- **D4:** exact analytic continuation is separated from stable reconstruction; the latter uses a fixed holomorphic collar and the uniform inverse modulus.
- **S1:** the statistical flagship theorem is stated first at the complete actual finite-bridge transcript level.  Conditional successful laws are used as factorizations inside the proof, not as the physical experiment itself.
- **S2:** the growing-order design is now chosen constructively as `M_s -> L_s -> k_s -> J_s -> caps`, with exponentially small transfer budget.
- **S3:** the compatible-rate construction is explicitly described as a feasibility/consistency schedule; no optimal/minimax rate is claimed.
- **S4:** all local fastest-scale claims are restricted to the declared stopped endpoint--time transcript.  The manuscript explicitly does not identify the still richer full growing collision array.

No accepted all-order contact derivation or local statistical theorem was deleted.  The revision adds the missing bridges and strengthens the global deterministic statement rather than reducing the manuscript's scope.
