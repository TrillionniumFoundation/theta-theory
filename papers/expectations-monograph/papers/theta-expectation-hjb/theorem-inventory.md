# Paper 2 Theorem Inventory

This inventory maps the HJB/theta-expectation paper to the master source
`../../main.tex` and to the companion Paper 1 response theorem.

## Imported Theorem

`Companion response theorem`

Imported from `../response-theory/main.tex`:

- `thm:main_response_package`: First-principles response package;
- `thm:primitive_spectral_resolvent`: primitive spectral and resolvent theorem;
- `lem:suspension_laplace_contour`: suspension Laplace contour and frequency
  partition;
- `thm:smooth_deterministic_response`: smooth deterministic response;
- `thm:moving_singularity_response`: moving-singularity response theorem;
- `lem:trace_resolvent_insertion`: trace insertion into resolvent words;
- `prop:uniform_multiresponse_bounds`: uniform multi-response bounds;
- `thm:regularity_loss_budget`: finite regularity-loss budget.

## Core Theorem Chain

| Order | Paper 2 role | Master label/source | Master line | Status |
| --- | --- | --- | --- | --- |
| 1 | First-principles interface | `thm:intro_structure_corrected` | `main.tex:236` | compress in introduction |
| 2 | Finite-response mechanics | finite-response section | `main.tex:1364-2245` | extract definitions |
| 3 | Effective Hamiltonian | `def:effective_hamiltonian_normalized` | `main.tex:4560` | keep in main text |
| 4 | Coefficient structure | `prop:coefficient_structure` | `main.tex:4848` | keep in main text |
| 5 | Residual identity | `lem:deterministic_residual_identity` | `main.tex:5642` | proof core |
| 6 | Sub/sup residual bounds | `prop:subsuper_residuals_full_branch` | `main.tex:6102` | proof core |
| 7 | Main homogenization | `thm:main_homogenization` | `main.tex:6133` | central theorem |
| 8 | Nonconvexity | `thm:non_convexity_proven` | `main.tex:7260` | keep in main text |
| 9 | Constructive example | `thm:constructive_nonconvex_example` | `main.tex:7329` | required main-text example |
| 10 | Non-subadditivity | `cor:non_subadditivity` | `main.tex:7464` | keep in main text |
| 11 | theta-expectation properties | `thm:theta_expectation_properties` | `main.tex:7652` | final section |

## Local Extraction Labels Added in Paper 2

| Local label | Purpose |
| --- | --- |
| `def:corrector_hierarchy` | Standalone corrector hierarchy and perturbed test function. |
| `lem:deterministic_residual_identity` | Corrector-cancellation residual identity for the contact-frozen test. |
| `lem:contact_frozen_perturbed_tests` | Contact selection and normalized gauge lemma for half-relaxed limits. |
| `prop:subsuper_residuals` | Half-relaxed subsolution/supersolution reduction. |
| `prop:comparison_modulus` | Crandall-Ishii continuity modulus for the derived HJB operator. |
| `thm:comparison_derived_hjb` | Comparison and uniqueness theorem for the effective HJB. |
| `def:triangular_lorentz_cell` | Concrete finite-horizon base billiard table. |
| `def:two_mode_port_example` | Concrete two-mode finite-response port on the base table. |
| `def:concrete_eta_dominance` | Explicit observable bump and nonconvexity dominance inequality. |
| `def:Cresp_bound` | Paper 1 exported response-bound formula tied to exact Paper 1 theorem labels. |
| `prop:Cresp_controls_response_terms` | Provenance claim that the exact Paper 1 constants bound the response-corrector terms. |
| `prop:inspectable_nonconvexity_coefficient` | Taylor-coefficient test for nonconvexity. |

## Technical Appendix Labels Added in Paper 2

| Appendix label | Purpose |
| --- | --- |
| `def:supp_hjb_dependency_order` | Dependency order for the finite-response HJB proof. |
| `def:supp_micro_action_port` | Microscopic finite-response port before effective coefficients. |
| `prop:supp_no_effective_feedback` | Non-circularity from port data to correctors to coefficients. |
| `lem:supp_exact_endpoint_jets` | Exact finite endpoint jets from a compact deterministic port. |
| `prop:supp_endpoint_reciprocity` | Action reciprocity relations among table, force, and action read-outs. |
| `def:supp_prelimit_operator` | Prelimit viscosity-duality operator in fast/action scales. |
| `def:supp_branchwise_action_graph` | Exact branchwise action graph data before effective coefficients. |
| `prop:supp_closed_action_graph` | Closure of the prelimit jet graph under deterministic branch transforms. |
| `thm:supp_exact_prelimit_hj` | Exact prelimit Hamilton-Jacobi identity for the finite-response action graph. |
| `lem:supp_universal_bundle_covector` | Contact covector and endpoint-variation lift in the universal response bundle. |
| `lem:supp_specular_endpoint_variation` | Cancellation of physical reflection endpoint work. |
| `prop:supp_moving_branch_boundary_ledger` | Moving branch-boundary trace terms and high-strip tail. |
| `def:supp_first_corrector_gk` | First corrector and Green-Kubo tensor ledger. |
| `lem:supp_first_order_cancellation` | Scale-\(\varepsilon^{-1}\) cancellation at the actual contact jet. |
| `def:supp_contact_frozen_test` | Contact-frozen first corrector and full slow-gradient increment. |
| `def:supp_order_one_work` | Complete order-one finite-response work observable. |
| `prop:supp_second_cell_average` | Order-one invariant average and second cell equation. |
| `def:supp_full_corrector_hierarchy` | Recursive zero-mean corrector hierarchy on the response window. |
| `prop:supp_corrector_hierarchy_closure` | Corrector hierarchy closure and branch summability. |
| `def:supp_residual_constant_ledger` | Named residual constants and branch-loss margins. |
| `lem:supp_residual_identity` | Normalized-gauge residual identity and residual bound. |
| `lem:supp_branch_residual_summation` | Summation of branch residuals after the strip cutoff. |
| `def:supp_branch_residual_family` | Decomposition of the residual into central, word, trace, endpoint, and tail families. |
| `lem:supp_central_branch_residual_check` | Central-branch Taylor, word, and endpoint residual bound. |
| `lem:supp_trace_branch_residual_check` | Moving-boundary trace residual check in central strips. |
| `prop:supp_high_strip_residual_cutoff` | High-strip residual cutoff and terminal-child summability. |
| `prop:supp_full_branch_residual_check` | Full branch residual modulus after central, trace, endpoint, and tail summation. |
| `prop:supp_uniform_subsuper_modulus` | Uniform viscosity modulus for sub/sup residual inequalities. |
| `prop:supp_four_scale_ledger` | Four-scale deterministic perturbed-test ledger. |
| `lem:supp_admissible_density_smoothing` | Smooth approximation of admissible densities in the weak topology. |
| `prop:supp_perturbed_test_smoothing` | Smooth branchwise approximation of microscopic perturbed tests. |
| `cor:supp_smooth_approximation_closure` | Closure of the HJB argument under the smoothing/cutoff approximation. |
| `lem:supp_contact_selection` | Half-relaxed contact selection for normalized gauges. |
| `prop:supp_subsuper_passage` | Subsolution/supersolution passage. |
| `lem:supp_density_to_state` | Admissible-density convergence to Liouville-a.e. state convergence. |
| `thm:supp_detailed_hjb_closure` | Detailed HJB closure theorem. |
| `prop:supp_coefficient_differentiability` | Coefficient differentiability through resolvent words. |
| `def:supp_correlation_hilbert_bundle` | Correlation Hilbert bundle and drift-factor ledger. |
| `lem:supp_gk_coboundary_kernel` | Green-Kubo positivity and coboundary-kernel criterion. |
| `prop:supp_correlation_factor_transport` | Transport and continuity of Green-Kubo correlation factors. |
| `prop:supp_gk_comparison_trace` | Green-Kubo trace estimate for doubled-variable comparison. |
| `prop:supp_comparison_modulus_ledger` | Comparison modulus for the derived operator. |
| `prop:supp_terminal_stability` | Terminal-value stability, cash additivity, and zero-energy gauge. |
| `lem:supp_synchronized_density_doubling` | Synchronized admissible density in doubled contacts. |
| `prop:supp_doubled_variable_comparison` | Doubled-variable comparison refinement. |
| `prop:supp_concrete_parameter_window` | Concrete two-mode parameter window for the nonconvex port. |
| `cor:supp_concrete_parameter_recipe` | Concrete parameter-choice recipe for nonconvex dominance. |
| `def:supp_dimensionless_parameter_audit` | Dimensionless parameter audit table for the concrete port. |
| `prop:supp_parameter_audit_verification` | Verification that the audit table preserves the nonconvexity certificate after smoothing and strip cutoff. |
| `def:supp_normalized_numerical_certificate` | Normalized numerical parameter certificate for the concrete-port inequalities. |
| `prop:supp_numerical_certificate_margin` | Stability margin for the normalized numerical certificate under small smooth port changes. |
| `lem:supp_directional_nonconvexity` | Directional nonconvexity certificate. |
| `lem:supp_subadditivity_obstruction` | Generator-level obstruction to subadditivity. |
| `prop:supp_hjb_crosswalk` | Crosswalk from appendix blocks to main-paper assertions. |

## Bibliography/Provenance Pass

- `main.tex` now cites the standard PDE and nonlinear-expectation literature
  used by the macroscopic argument:
  `CrandallIshiiLions1992`, `FlemingSoner2006`, `BarlesSouganidis1991`,
  `BensoussanLionsPapanicolaou1978`, `Evans1992`,
  `PavliotisStuart2008`, and `Peng2019`.
- The visible theorem map has been converted from source-line provenance to a
  journal-facing proof-role map.  Exact Paper 1 labels remain tracked in this
  inventory rather than printed as internal source references in the article.

## Main-Text Candidates

- Companion response theorem interface.
- Finite-response prelimit data.
- Effective coefficients and HJB operator.
- Deterministic HJB convergence theorem.
- Concrete nonconvex billiard/port example.
- Basic theta-expectation properties.

## Appendix Candidates

- Corrector cancellation details.
- Half-relaxed limits and viscosity comparison.
- Smooth approximation details in anisotropic weak topology.
- Technical coefficient differentiability checks that are not already in
  Paper 1.

First seven technical appendix passes completed in `technical-appendix.tex`:
finite-response micro-action, endpoint-jet realization, endpoint reciprocity,
exact prelimit action graph, specular endpoint variation, moving-boundary
trace control, contact-frozen corrector hierarchy, recursive corrector closure,
branch residual constants, full branch residual checks, four-scale residual
identity, smooth approximation closure, half-relaxed viscosity passage,
synchronized doubled-variable comparison, density-to-state upgrade, coefficient
comparison, Green-Kubo correlation factorization, terminal-value stability,
concrete nonconvex parameter window and recipe, dimensionless parameter audit
table, normalized numerical certificate with stability margin, and
nonconvexity/subadditivity algebra now have standalone
referee-facing ledgers.  Remaining Paper 2 migration items are narrower:
venue-specific proof polish or a true numerical orbit experiment if a venue
asks for one.

## Keep Out

- Singular billiard response proof.
- BSDE representation.
- Girsanov/Cameron-Martin formulae.
- Repeated dependency-ledger prose from the master source.
