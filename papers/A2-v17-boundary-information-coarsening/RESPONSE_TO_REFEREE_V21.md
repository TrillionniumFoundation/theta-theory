# Response to the independent A2 v20 referee — revision v21

**Revision branch:** `revision/a2-v21-nondominated-registered-transfer-2026-09-11`  
**Controlling report:** `review/a2-v20-independent-harsh-top4-2026-09-11/reviews/a2-v20-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Canonical article entry point:** `main.tex` in this directory.

This revision treats the v20 report as a request to expose and strengthen the proof interfaces, not to weaken the theorem package. No historical derivation file is deleted. The v20 sources remain in the tree; `main.tex` selects new v21 theorem modules.

## R20-1 — Non-dominated vector moving-support LAN

**Referee issue.** V20 wrote a global Radon–Nikodym derivative of the local alternative with respect to the reference experiment even when an outward support motion creates alternative-only mass.

**V21 repair.** `article/18a_vector_boundary_information_v21.tex` removes that finite-sample identity. The original local family is explicitly allowed to be non-dominated. We introduce the parameter-independent reference collar

`q_n = delta_n (log(1/delta_n))^(1/4)`

and a Markov map that keeps the common core `w_0 >= q_n` and collapses every other successful point to one collar atom. Uniformly over compact local parameter sets,

`Delta(E_n^K, Etilde_n^K) <= C_K n p_n q_n^2 = o(1)`.

The collapsed family is genuinely dominated by its reference law. The uniform likelihood expansion is proved only for that dominated family. The vector Gaussian shift, bounded-local mutual contiguity, testing profile and local asymptotic minimax bound are then transferred back to the original experiment by the explicit experiment comparison. A final remark states that no artificial likelihood value is assigned to support-exclusive observations.

This route also fixes the smaller v20 comments about the parsing of `L_n`, compact-uniform LAN versus fixed-`h` convergence, contiguity before third-lemma arguments, and uniform integrability under local alternatives.

## R20-2 — Parameter-independent spatial observation model

**Referee issue.** V20 said the channel was registered but did not make the fixed spatial record space a theorem-level hypothesis. A contact-centered coordinate would ordinarily move with a generic table.

**V21 repair.** `article/18b_raw_physical_multirate_v21.tex` begins by defining an anchored registered local family in one Euclidean laboratory chart:

`Gamma_0,vartheta = {(-psi_0,vartheta(u),u)}`,

`Gamma_1,g,vartheta = {(g+psi_1,vartheta(v),v)}`,

with `psi_b,vartheta(0)=psi'_b,vartheta(0)=0` for every parameter value. The contact origins and tangent axes are fixed model data; the unknowns are the gap and graph shapes in those fixed axes. Recorded `(u,v)` are literal common laboratory coordinates, not re-centered coordinates.

The section explicitly overrides the default channel-centered derivative convention of the forward theorem: statistical derivatives are taken at fixed laboratory endpoint coordinates and fixed programmed physical time. The acquisition times remain `t_{j,l}=j g_0+d_l` under every local alternative.

The deterministic relative-law and signed-rigidity results remain valid on their more general geometric classes. The anchored hypothesis is the exact common-record-space realization for the statistical theorem. A closing remark explains how absolute pose/frame variables must instead be included as nuisance coordinates or supplied by a charged registration pilot; they are not treated as free.

## R20-3 — Quantitative abstract-to-billiard transfer

**Referee issue.** V20 asserted that the abstract likelihood proof was uniform under an `o(delta_n)` support perturbation and an `O(delta_n)` amplitude perturbation without proving an experiment-distance estimate.

**V21 repair.** Two new results make the transfer quantitative.

1. `article/18a_vector_boundary_information_v21.tex` proves a general support-remainder estimate

   `H^2 <= C { epsilon^2 log(e/epsilon) + eta^2 }`

   for linearly vanishing densities whose defining functions differ by `epsilon` in `C^1` and whose amplitudes differ by `eta`.

2. `article/18b_raw_physical_multirate_v21.tex` defines the exact normalized fixed-window boundary endpoint density and an ideal normalized first-order moving-boundary density on the same fixed endpoint box. If

   `r_n(K)=sup_z ||R_{n,z}||_{C^2}=o(delta_n)`,

   then one record satisfies

   `H^2(exact,ideal) <= C_K { r_n(K)^2 log(e/r_n(K)) + delta_n^2 }`.

   Under `k_n delta_n^2 log(1/delta_n) -> 1`, tensorization gives product Hellinger and hence Le Cam distance `o(1)` uniformly on compact local sets.

The physical Gaussian experiment is therefore obtained by a genuine chain of experiment comparisons: exact billiard endpoint law -> ideal moving-boundary law -> dominated collar-collapsed ULAN law.

## R20-4 — Tangent-level finite-design nonsingularity

**Referee issue.** V20 used nonlinear signed-rigidity injectivity to conclude that a tangent vector vanishing in both action derivatives must be zero. Nonlinear injectivity alone does not imply injectivity of the derivative.

**V21 repair.** `article/23a_signed_endpoint_rigidity_v21.tex` adds `Differential signed-jet inverse`. At fixed gap and any finite labelled jet order, the action-jet map has injective differential and a uniformly bounded left inverse on compact positive sets. The proof differentiates the leading curvature recovery and then the determinant-one triangular recursion degree by degree.

`article/18b_raw_physical_multirate_v21.tex` now invokes this tangent proposition in the information-kernel argument. The finite positive-offset design lemma also states explicitly that the finite design may depend on the chosen finite jet order; no universal finite set for the infinite jet is asserted.

## R20-5 — Standalone signed all-order recursion

**Referee issue.** The determinant-one arbitrary-degree signed jet block was promising but too compressed for a central theorem.

**V21 repair.** `article/23a_signed_endpoint_rigidity_v21.tex` is rewritten as a standalone proof. It now:

- writes the stationary half-line Euler–Lagrange equations in a weighted sequence space;
- records the explicit half-line Green kernel and uniform inverse bound;
- proves that the same nonlinear Jacobi operator multiplies the highest orbit derivative at every differentiation order;
- proves finite-jet dependence without analyticity;
- derives the infinite-dimensional stationary envelope identity by finite truncation plus weighted convergence;
- proves that replacing the nonlinear stationary orbit by its linear part cannot alter the first new homogeneous degree;
- evaluates the own-contact and opposite-contact geometric sums with boundary/interior multiplicities explicit;
- obtains the matrix

  `[[coth(n gamma), r_0^n csch(n gamma)], [r_1^n csch(n gamma), coth(n gamma)]]`

  and its determinant one;
- gives the explicit recursive inverse and compact finite-order Lipschitz bounds;
- states the oriented-coordinate dependence of odd jets;
- differentiates the recursion to obtain the tangent inverse used by the statistical theorem.

A finite registered channel-network corollary is added: signed data on finitely many registered channels determine every incident analytic contact germ, and, when the network meets every obstacle under consideration, the corresponding connected analytic boundary images in the common frame.

## R20-6 — Endpoint-output versus complete stopped experiment

**Referee issue.** The Gaussian information/minimax theorem applies to a deliberate endpoint-output coarsening, not to the richest waiting transcript.

**V21 repair.** The distinction now governs the abstract, introduction and theorem names. The Gaussian theorem is the `Fixed-window multirate endpoint Gaussian experiment`. The separate stopped-transfer theorem compares the complete finite and boundary transcripts, with failures, designs and stopping times retained. A dedicated remark states that cost accounting does not make the endpoint minimax bound an efficiency bound for the complete transcript and that waiting counts may carry faster information through the long-bridge exponent.

The pilot corollary also states its sigma-field explicitly: both compared experiments retain the same pilot transcript and the post-pilot successful endpoint outputs. Programmed post-pilot times and waiting counts are not silently included in that endpoint-output comparison.

## R20-7 — Canonical source and native build

V21 adds a dedicated canonical source pointer and a v21 native-build workflow. The old `A2-v17-boundary-information-coarsening` directory name is retained to avoid breaking the historical dependency tree; the canonical pointer identifies the exact active v21 entry point and modules. Historical v18/v19/v20 files remain provenance sources rather than competing active manuscripts.

The native workflow targets the exact v21 revision branch and invokes the repository's existing submission builder and boundary-information diagnostics. Build success is not predeclared in this response; the workflow run is the external certificate.

## Additional presentation changes

The v21 abstract and introduction are rewritten around the repaired proof architecture. In particular:

- no finite-sample likelihood ratio is written for the original non-dominated family;
- `L_n=(log(1/delta_n))^(1/4)` is parenthesized unambiguously;
- the anchored graph family is a theorem hypothesis rather than registration prose;
- exact-to-ideal transfer is a standalone proposition;
- compact-uniform LAN, experiment convergence, contiguity and minimax transfer are kept logically separate;
- the main proof dependency graph is visible from the active source manifest and proof ledger.

## Preservation policy

Nothing in the v20 mathematical development is deleted merely because v21 supersedes it. The previous vector theorem, physical theorem, signed-rigidity source, response letters, audits, ledgers and auxiliary compendium remain in repository history and, where already present, in the source tree. The v21 entry point selects the strengthened replacements.
