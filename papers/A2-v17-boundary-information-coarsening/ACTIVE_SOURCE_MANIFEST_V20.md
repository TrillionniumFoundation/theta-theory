# A2 v20 active-source manifest

**Revision branch:** `revision/a2-v20-raw-physical-multirate-lan-2026-09-11`  
**Review base:** `review/a2-v19-independent-harsh-top4-2026-09-11`  
**Review commit at branch creation:** `f394a2822e748c3a40c1b1718c6afeb91bde0677`  
**Article entry point:** `main.tex`

This manifest is authoritative for v20. The containing directory retains the historical name `A2-v17-boundary-information-coarsening` in order to preserve source history; active version identity is determined by this branch, `main.tex`, and this manifest.

## Main theorem chain

1. `article/01_introduction_v20.tex` — theorem-first v20 introduction and information-set comparison.
2. `article/01c_geometric_setup_v18.tex` — formal billiard family and principal relative theorem.
3. `article/01a_protocol_scope.tex`, `article/01b_observation_hierarchy.tex` — raw protocol and fixed-table coarsening hierarchy.
4. Forward chain: `article/02_finite_results.tex`, `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, `v5/15_differentiated_operators.tex`, `article/15_operator_comparison.tex`, `article/16_hyperbolic_coordinates.tex`, `article/16c_strict_margin.tex`.
5. `v6/10_experiment_transfer.tex`, `article/17_adaptive_experiments.tex` — common physical record space and stopped finite-to-boundary transfer.
6. `article/20_boundary_compatibility.tex` — general smooth scalar/profile inverse.
7. `article/23_two_contact_rigidity.tex` — predecessor even-contact all-jet calculation.
8. `article/23a_signed_endpoint_rigidity_v19.tex` — signed endpoint support and determinant-one arbitrary-degree labelled jet recursion.
9. `article/24_physical_image.tex`, `article/29_two_flight_benchmark.tex` — physical realization and finite benchmark.
10. `article/18_boundary_information_v18.tex` — scalar moving-boundary logarithmic information.
11. **`article/18a_vector_boundary_information_v20.tex` — self-contained vector boundary LAN/minimax theorem.**
12. **`article/18b_raw_physical_multirate_v20.tex` — fixed-window multirate gap/contact LAN, finite positive-offset design, capped stopped transfer, charged pilot-centered equivalence.**
13. `article/19_endpoint_critical.tex` — fixed-table endpoint critical experiment.
14. `article/21_abel_stability.tex`, `article/22_deautoconvolution.tex`, `article/28_regularized_observation.tex` — retained downstream inverse/acquisition results.

## Auxiliary compendium

`article/99_auxiliary_compendium_v19.tex` remains the single appendix entry point for historical auxiliary mathematics. It is retained rather than deleted. The v20 headline claims do not rely on the auxiliary modules to broaden their scope; the main conceptual chain is stated above.

## Bibliography

`v5/references_v18.tex` remains the compiled bibliography. Current comparison/priority notes are recorded in `LITERATURE_VERIFICATION_V20.md`. The article introduction cites the compiled billiard-rigidity benchmarks already present in the bibliography.

## Revision evidence

Authoritative v20 audit documents:

- `HISTORICAL_DERIVATION_AUDIT_V20.md`
- `PROOF_LEDGER_V20.md`
- `LITERATURE_VERIFICATION_V20.md`
- `RESPONSE_TO_REFEREE_V20.md`
- `VERIFICATION_V20.json` after the final native-build run has been inspected

V19 audit documents remain historical records and are not the authoritative v20 status documents.

## Scope fixed in v20

The main statistical theorem is for a **registered labelled channel**. The gap and finite participating contact-jet geometry are unknown local coordinates. Absolute Euclidean pose, label exchange and unknown construction of endpoint frames are fixed calibration/nuisance quantities and are not silently added to the parameter. The theorem uses parameter-independent physical times `j g_0+d_l`; the local gap is `g_0+delta a/j`.

The raw stopped transcript may retain failures and stopping times. The LAN/minimax theorem is promoted for the explicitly declared endpoint-output coarsening. The paper does not call waiting counts ancillary and does not claim that the richer transcript has no additional faster information.

## Build status rule

No manifest statement counts as compilation evidence. A successful workflow must build the exact final revision head. `VERIFICATION_V20.json` must distinguish:

- success after runner steps execute and PDFs are produced;
- workflow infrastructure/runner failure before build steps;
- a genuine LaTeX or diagnostic failure.

Only the first is a successful native build.

## Preservation rule

No reviewed v19 mathematical source is deleted. V20 adds replacement introduction/vector/physical-experiment sources and selects them in `main.tex`; predecessor sources remain recoverable both in-tree and from Git history. This revision addresses the referee by strengthening the theorem chain rather than shrinking it.
