# Response to the independent A2 v19 referee report — v20 revision

**Revision branch:** `revision/a2-v20-raw-physical-multirate-lan-2026-09-11`  
**Controlling report:** `reviews/a2-v19-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Reviewed v19 head:** `837d785dc92c22253aa8809e32d97dd6579aef3c`  
**Review commit:** `f394a2822e748c3a40c1b1718c6afeb91bde0677`

## Revision principle

The v19 report accepts the signed-endpoint rigidity theorem as a genuine strengthening and finds no direct contradiction in the abstract vector moving-support LAN theorem. Its decisive objection is the last step: v19 wrote the billiard LAN in parameter-dependent centered time/contact coordinates and then interpreted it as a raw unknown-table physical experiment. It also observed that the endpoint information-kernel proof did not include the independent gap/onset direction.

V20 does not respond by weakening the deterministic theorem, deleting the nonregular statistics, or retreating to a known-gap model. It changes the physical local experiment itself. The main statistical theorem is now formulated on **fixed physical time windows and fixed registered endpoint coordinates**, with the unknown gap assigned its natural faster local scale. This closes the gap/onset direction inside the same moving-support information matrix. A separate charged pilot theorem is retained only as an optional route back to centered windows.

No reviewed mathematical result is deleted. Historical modules remain in the auxiliary compendium. The main theorem chain is sharpened to

`relative boundary law -> signed local rigidity -> fixed-window physical local experiment`.

## C19-M1 — parameter-dependent observation coordinates

### Referee objection

V19 fixed the centered excess `d` while varying the geometry, so physical time was `t = j g(eta) + d`. It also wrote endpoint coordinates in frames attached to the perturbed table. A genuine unknown-parameter statistical experiment requires a common observation space and parameter-independent acquisition rule, or a calibration/equivalence theorem.

### V20 repair

New file:

- `article/18b_raw_physical_multirate_v20.tex`

The physical design is now programmed at

` t_{j,l} = j g_0 + d_l `

for a specified reference registered geometry. These physical times do not change with the local alternative. The two contact labels and the signed transverse coordinate are fixed registration variables. Absolute Euclidean pose, label exchange and unknown frame construction are **not silently included** in the parameter; this scope is stated explicitly in the theorem, introduction and final registration remark.

The unknown local geometry is

`g_n(a) = g_0 + delta_n a / j_n`,  `vartheta_n(h) = delta_n h`.

Consequently the actual excess of the fixed physical window is

`d_l - delta_n a`.

The support velocity therefore contains a constant gap component together with the signed-action velocities. No parameter-dependent time centering is used.

The acquisition policy is also common: at each preassigned physical window it uses a deterministic preparation cap and stops at the target success count or the cap. Every raw trial is generated on the same failure/endpoint record space. The cap makes the policy satisfy the bounded-stopping hypotheses of the historical adaptive-transfer theorem exactly.

### Optional centered route

V20 additionally proves `Corollary (Pilot-centered asymptotic equivalence)`. The historical charged self-calibration theorem gives

`j_n |g_hat - g| <= C r_n^{m+1}`.

If

`k_n r_n^{2m+2} log(1/r_n) -> 0`,

the post-pilot design `t = j_n g_hat + d_l` is at vanishing Le Cam distance from the oracle centered design. The pilot cost remains explicit. Thus the centered formulation is justified by a theorem rather than by treating the unknown gap as observed.

## C19-M2 — missing gap/onset information direction

### Referee objection

The v19 kernel proof used only derivatives of the endpoint actions. The signed-rigidity theorem itself needed onset to recover `g`, so the argument did not establish positive definiteness on a geometry family that also varied the gap.

### V20 repair

At the fixed physical window the local gap perturbation contributes the support velocity

`a`.

For a same-type endpoint design the full local support velocity is

`U_b(u,v)(a,h) = a + D_h S_b(u) + D_h S_b(v)`.

The new information matrix is

`K_{b,d} = integral A_{b,d} U_b^T U_b / |grad(S_b \oplus S_b)| d sigma`.

The common-kernel proof now includes the gap direction. If `(a,h)` lies in every kernel, positivity gives

`a + D_h S_b(u) + D_h S_b(v) = 0`

on every small support level. Taking `v=0`, then letting `u -> 0`, first gives `a=0`; the same identity then gives `D_h S_b=0` for both contact labels. At fixed gap, the leading reconstruction formulas and the determinant-one signed jet recursion force every contact-jet component of `h` to vanish. Hence the full common kernel on `(gap, labelled contact jets)` is trivial.

Compactness of the unit sphere then selects finitely many positive same-type windows with a positive-definite weighted matrix. This is the finite physical information design promoted in the abstract.

## C19-M3 — finite-bridge LAN transfer was not an experiment theorem

### Referee objection

The v19 sentence `k_n tau^{j_n} -> 0` was plausible but did not state the uniform local alternative, common raw sample space, failure atom and experiment-level conclusion.

### V20 repair

New theorem:

- `Theorem (Uniform stopped local-experiment transfer)` in `article/18b_raw_physical_multirate_v20.tex`.

Let `P^{fin}_{n,z}` be the **complete actual stopped transcript**, retaining failures, successes, designs and stopping times, and let `Q^{partial}_{n,z}` be the boundary transcript under the identical capped policy. For every compact local parameter set `K`,

`sup_{z in K} || P^{fin}_{n,z} - Q^{partial}_{n,z} ||_TV <= C k_n tau^{j_n}`.

Therefore `k_n tau^{j_n} -> 0` gives uniform asymptotic equivalence of the stopped experiments. The proof is a direct specialization of the already proved `Theorem v16 adaptive physical transfer`, now with the v20 fixed physical windows and local alternatives inserted explicitly. The deterministic caps remove the bounded-stopping ambiguity; the probability that a cap prevents the target number of successes is exponentially small in the target count.

Any common Markov coarsening inherits the same TV bound. In particular the endpoint-output experiment inherits the boundary LAN theorem. The preparation cost is still the raw number of trials, and the manuscript prints its uniform expectation/cap bounds.

The revision also states explicitly that the waiting transcript need not be ancillary. Retaining it can add a faster information channel through `sinh(j gamma)^{-1}`. The LAN/minimax statement is for the declared endpoint-output coarsening, while the entire failure cost is charged.

## C19-M4 — local central-sequence estimator was overinterpreted

The new vector theorem contains an explicit remark: `J^{-1} Delta_n` is a **local central-sequence estimator around a specified reference parameter**. It is not called a globally implementable estimator of an arbitrary unknown table.

The physical theorem now supplies the actual local acquisition rule. For centered windows, the charged pilot corollary gives the additional localization route. This removes the interpretation error without reducing the local asymptotic conclusion.

## Blocker 5 — vector LAN proof needed theorem-level self-containment

V20 replaces the active v19 vector source by

- `article/18a_vector_boundary_information_v20.tex`.

The new source promotes the compressed arguments into explicit statements:

1. `Uniform vector collar estimates`: logarithmic covariance, third and fourth truncated moments, collar mass and truncated-score centering.
2. `Uniform truncated likelihood expansion`: compact-uniform support exclusion, likelihood Taylor expansion, central sequence, quadratic term and their limits.
3. `Vector boundary LAN and local minimax bound`: Gaussian shift, testing profile, local estimator, truncated quadratic minimax theorem and the uniform-integrability passage to quadratic risk.

This addresses the report's request that the vector theorem stand on its own rather than refer generically to scalar bookkeeping.

## Blocker 6 — top-four positioning and information hierarchy

The active introduction is now

- `article/01_introduction_v20.tex`.

It is organized around one theorem package only. It makes the comparison with modern billiard rigidity at the level of information content:

- marked-length results use global periodic-orbit data and obtain global conclusions under their own analytic/symmetry/genericity hypotheses;
- the signed endpoint law is globally narrower (one registered closest-pair channel) but locally richer (a continuum of signed endpoint-support data) and recovers arbitrary smooth labelled contact jets without reflection symmetry or supplied curvature;
- neither data set is claimed to be a formal coarsening of the other.

The introduction also states explicitly that classical nonregular endpoint asymptotics, generic parameter-dependent support, Le Cam methods and generic optimal testing are not priority claims of this paper. The claimed contribution is the coupled boundary-law/rigidity/physical-experiment chain.

The auxiliary historical dossier is retained because the author requested no arbitrary deletion; it is not used to broaden the headline theorem package.

## Blocker 7 — native build

A v20 native-build workflow is added only after the source graph and version documents are finalized, so that the workflow targets the actual final revision head rather than an intermediate commit. The authoritative v20 manifest and verification record will report the resulting run honestly. A failed-before-runner workflow is not represented as a successful LaTeX build.

## Strength retained from v19

The following v19 advances remain active and are not weakened:

- signed endpoint support recovers the unsymmetrized actions;
- onset plus action Hessians recover both contact curvatures;
- the arbitrary-degree signed last-jet block has determinant one;
- odd and even labelled contact jets are recursively recovered without reflection symmetry;
- analytic signed endpoint-law germs determine the participating analytic contact germs;
- the regular-hypersurface logarithmic information coefficient and its vector matrix form remain;
- fixed-table complete/endpoint/success-bit coarsening results remain.

The statistical conclusion is stronger than in v19 in one important sense: the unknown gap is now part of the fixed-window physical local experiment rather than a hidden calibration coordinate.
