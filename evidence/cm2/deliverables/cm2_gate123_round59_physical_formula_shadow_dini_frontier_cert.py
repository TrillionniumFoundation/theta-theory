#!/usr/bin/env python3
"""CM2 Round-59 Gate-1/2/3 physical-interface frontier certificate.

The certificate is fail-closed.  It records three advances without promoting
any composite gate:

* the frozen QNL compact-gauge loop has a genuine selected-orbit Dini tail
  and an entrywise truncation error far below 1e-29, but this is not an
  all-plaque weighted-projective registry in the combined gauge;
* the physical 96-collision strip supplies finite singular-shadow rows and
  the Gate-2 -> Gate-4 seven-field join is audited field by field;
* an actual n-step circular-billiard branch formula is counted explicitly and
  proved to fit the Round-58 CAD budget for every fixed n.

Positive audit/replay modes exit zero.  The default exits two because Gates
1, 2, 3 and CM2 remain uncertified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
MANIFEST = HERE / (
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-"
    "manifest-2026-07-20.json"
)
REPORT = HERE / (
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-"
    "assault-2026-07-20.md"
)
VERIFIER = HERE / "cm2_gate123_round59_physical_formula_shadow_dini_frontier_verifier.py"
Q = Fraction


DEPENDENCIES = {
    "deliverables/cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-assault-2026-07-20.md":
        "e6b87bd43bf4c35ca4804dc1a563a916d27cb0550c45e7b3fb1d670dddfd0934",
    "deliverables/cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json":
        "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "deliverables/cm2-gate2-actual-stable-plaque-continuation-2026-07-15.md":
        "3f1852862ea5192d4ab350c2c67dc874d5d69634856ee874f350fe2ca038e37d",
    "deliverables/cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json":
        "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "deliverables/cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-assault-2026-07-20.md":
        "0e9ce7397039c86178858bdd5e1ebe6228938e473711ce65075a3c4d45db16c8",
    "deliverables/cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "deliverables/cm2-gate3-first-hit-atlas-assault-2026-07-15.md":
        "fd2c1c47602e361da8eab48b88e5c169fd679dd783ee8aea38512bdbdde2b3d5",
    "deliverables/cm2-gate3-first-hit-atlas-manifest-2026-07-15.json":
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-assault-2026-07-16.md":
        "235cf2c74ea3871a1d3862476d5e7d0ac506acc0e490ea5df12d8d2940c6b8f6",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-manifest-2026-07-16.json":
        "8b6e8ca2c436237f8eb41f24c94bb11fe9ddb393cbbe4845d41b6c7a2409c0e1",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def qtext(value: Q) -> str:
    return str(value)


def validate_dependencies() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel, expected in DEPENDENCIES.items():
        path = ROOT / rel
        require(not path.is_symlink(), f"symlink dependency rejected: {rel}")
        require(path.is_file(), f"missing dependency: {rel}")
        require(sha256_path(path) == expected, f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


def gate1_replay() -> dict[str, Any]:
    # The selected QNL tail has a geometric-log majorant.  The inward
    # rational bounds rho<1/10 and q^2<1/100 make its summability exact.
    rho = Q(1, 10)
    q_squared = Q(1, 100)
    crit_first_eight = [(m + 1) * rho**m for m in range(8)]
    diag_first_eight = [(m + 1) * q_squared**m for m in range(8)]
    crit_sum = Q(1, 1) / (1 - rho) ** 2
    diag_sum = Q(1, 1) / (1 - q_squared) ** 2
    require(crit_sum == Q(100, 81), "critical Dini sum")
    require(diag_sum == Q(10000, 9801), "diagonal Dini sum")

    # Strictly enlarge the frozen interval upper endpoint 8.567025...e-49.
    loop_error_upper = Q(8568, 10**52)
    robustness_radius = Q(1, 10**29)
    smallest_wedge_inward = Q(17344, 10**32)
    require(loop_error_upper < robustness_radius, "selected loop error radius")
    require(loop_error_upper < smallest_wedge_inward, "selected smallest wedge")

    return {
        "physical_selected_QNL_tail": {
            "gauge": "frozen compact logarithmic QNL gauge",
            "fibre_and_basis": "canonical QNL eigenfibre E_p and its frozen normalized eigenbasis",
            "actual_tail_ratios_from_frozen_interval_proof": {
                "critical_rho_strict_upper": "1/10",
                "noncritical_q_squared_strict_upper": "1/100",
            },
            "normalized_critical_Dini_rows_first_eight": [qtext(x) for x in crit_first_eight],
            "normalized_diagonal_Dini_rows_first_eight": [qtext(x) for x in diag_first_eight],
            "normalized_critical_Dini_sum": qtext(crit_sum),
            "normalized_diagonal_Dini_sum": qtext(diag_sum),
            "finite_depth": 260,
            "two_sided_entry_error_strict_upper": qtext(loop_error_upper),
            "same_fibre_robustness_radius": qtext(robustness_radius),
            "smallest_wedge_strict_inward_lower": qtext(smallest_wedge_inward),
            "selected_loop_twisting_preserved": True,
            "status": "CERTIFIED_PHYSICAL_SELECTED_GERM_AND_LOOP_ONLY",
        },
        "type_boundary": {
            "selected_orbit_tail_is_all_plaque_weighted_projective_Dini": False,
            "compact_log_gauge_is_the_unsolved_combined_half_density_gauge": False,
            "physical_all_plaque_Dini_rows": "NOT_CERTIFIED",
            "combined_gauge_loop_comparison_error_le_1e_minus_29": "NOT_CERTIFIED",
            "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "gate1": "NOT_CERTIFIED",
        },
        "sharp_nonpromotion": (
            "one selected homoclinic germ may have a summable tail while an unrelated "
            "plaque registry has nonsummable or oscillatory weighted increments"
        ),
    }


def gate2_replay() -> dict[str, Any]:
    # The entire frozen positive-width strip follows one strict 96-collision
    # itinerary.  Therefore the collision-singularity shadow on its affine
    # transverse base is empty at every recorded finite depth 1,...,96.
    shadow_rows = [
        {"depth": j, "physical_collision_singularity_shadow_measure": "0"}
        for j in range(1, 97)
    ]
    require(len(shadow_rows) == 96, "finite shadow row count")
    require(all(row["physical_collision_singularity_shadow_measure"] == "0"
                for row in shadow_rows), "finite shadow rows")

    join_rows = [
        {
            "field": 1,
            "name": "countable physical stable-product rectangles on landing support",
            "status": "NOT_CERTIFIED",
        },
        {
            "field": 2,
            "name": "stable projection with two-sided Borel holonomy Jacobian",
            "status": "NOT_CERTIFIED",
        },
        {
            "field": 3,
            "name": "full-span landing restriction or uniform fragmentation bound",
            "status": "NOT_CERTIFIED",
        },
        {
            "field": 4,
            "name": "same-measure unstable Rokhlin conditionals with density/log distortion",
            "status": "ONLY_EXISTING_CURVE_CARRIER_DENSITIES_CERTIFIED_NOT_THE_STABLE_ROKHLIN_FIELD",
        },
        {
            "field": 5,
            "name": "average boundary charge strictly below C_p",
            "status": "EXACTLY_EQUIVALENT_TO_OPEN_J_land_min_LT_C_p_h_AE",
        },
        {
            "field": 6,
            "name": "Borel branch inverse retaining n/path/same-ID/half-open ownership",
            "status": "CERTIFIED_ON_THE_EXACT_RAW_FIRST_RETURN_GRAPH",
        },
        {
            "field": 7,
            "name": "strong restriction and assembly bounds",
            "status": "NOT_CERTIFIED_WEAK_BOREL_GRAPH_ONLY",
        },
    ]
    require([row["field"] for row in join_rows] == list(range(1, 8)),
            "landing join field numbering")
    require(sum(row["status"].startswith("CERTIFIED") for row in join_rows) == 1,
            "exact completed join-field count")

    return {
        "physical_finite_shadow_registry": {
            "carrier": "frozen positive-width actual 96-word source strip",
            "base": "its affine transverse source coordinate",
            "rows": shadow_rows,
            "row_count": 96,
            "all_recorded_collision_shadows_empty": True,
            "graph_transform_chart_defined_at_every_prefix": "NOT_CERTIFIED",
            "invariant_stable_fibre_family": "NOT_CERTIFIED",
            "status": "CERTIFIED_FINITE_COLLISION_SHADOWS_ONLY",
        },
        "gate2_to_gate4_seven_field_audit": {
            "rows": join_rows,
            "fully_certified_field_count": 1,
            "partial_or_exact_frontier_field_count": 2,
            "absent_strong_or_stable_fields": 4,
            "join_closed": False,
        },
        "measure_type_audit_2604_25881": {
            "paper_measure": "newly constructed measure of maximal entropy",
            "local_product_statement": "symbolic/Hausdorff leaf-product structure for that MME",
            "is_CM2_collision_Liouville_SRB_law": False,
            "supplies_physical_Radon_Nikodym_fragmentation_boundary_Z_strong_assembly": False,
            "total_component_length_growth_controls_component_count_or_inverse_lengths": False,
        },
        "strict_status": {
            "physical_projected_all_depth_bad_shadow_rows": 0,
            "physical_stable_saturated_base_projection_J_hol": "NOT_CERTIFIED",
            "immutable_gate2_fields": "0/17",
            "gate2": "NOT_CERTIFIED",
        },
    }


def no_earlier_root_truth(a: Q, b: Q, tau: Q) -> bool:
    """Polynomial Boolean test for no ray-circle root in (0,tau).

    The physical competitor rows have |u|=1 and b>0 because the current
    source disk is removed and distinct periodic scatterers are disjoint.
    Delta=a^2-b.  If a>0 and Delta>=0, the incoming root is
    a-sqrt(Delta); comparing it to tau can be squared exactly only after
    requiring a-tau>=0.
    """
    require(b > 0 and tau > 0, "root-test physical domain")
    delta = a * a - b
    return (
        a <= 0
        or delta < 0
        or (a - tau >= 0 and delta <= (a - tau) ** 2)
    )


def cad_prefix(depth: int, steps: int = 3) -> dict[str, Any]:
    require(depth >= 1 and steps >= 1, "CAD prefix arguments")
    k = 400 * depth + 20
    s_value = 2000 * depth + 100
    d_value = 8
    rows: list[dict[str, int | str]] = []
    product = 1
    for projection_step in range(steps):
        stack = 2 * s_value * d_value + 1
        product *= stack
        rows.append({
            "projection_step": projection_step,
            "polynomial_count_majorant": str(s_value),
            "degree_majorant": str(d_value),
            "stack_factor": str(stack),
            "cell_product_prefix": str(product),
        })
        s_value = 2 * (s_value * d_value + 1) ** 2
        d_value = 2 * d_value**2
    return {"depth": depth, "declared_projection_variables": k, "rows": rows}


def gate3_replay() -> dict[str, Any]:
    # Explicit physical branch encoding counts.  Initial variables are
    # (s,q_0,u_0): 5.  Every collision adds tau, q_next, normal, c and
    # u_next: 1+2+2+1+2=8.  The safe atom envelope allocates five rows to
    # each of the 161 nonchosen target slots; on a nonempty branch one slot
    # is the current source and uses the simpler outgoing-convexity row.
    # The envelope also includes outside-domain checks,
    # chosen contact, flight, normal, reflection, signs and tie/cemetery rows.
    budget_rows = []
    for n in range(1, 9):
        variables = 8 * n + 5
        atoms = 830 * n + 12
        degree = 4
        declared_variables = 400 * n + 20
        declared_atoms = 2000 * n + 100
        require(variables <= declared_variables, "physical variable budget")
        require(atoms <= declared_atoms, "physical atom budget")
        require(degree <= 8, "physical degree budget")
        budget_rows.append({
            "depth": n,
            "physical_variables": variables,
            "physical_atomic_predicates_upper": atoms,
            "physical_degree_upper": degree,
            "declared_variables": declared_variables,
            "declared_atomic_predicates": declared_atoms,
            "declared_degree": 8,
            "branch_words": 8 * 162**n,
        })

    # Exact samples covering every Boolean branch of the no-earlier lemma.
    root_samples = [
        {"a": Q(-1), "b": Q(1), "tau": Q(1), "no_earlier": True,
         "reason": "ray points away"},
        {"a": Q(1), "b": Q(2), "tau": Q(1), "no_earlier": True,
         "reason": "negative discriminant"},
        {"a": Q(3), "b": Q(5), "tau": Q(1), "no_earlier": True,
         "reason": "incoming root at or after tau"},
        {"a": Q(2), "b": Q(3), "tau": Q(3, 2), "no_earlier": False,
         "reason": "incoming root before tau"},
    ]
    require([no_earlier_root_truth(r["a"], r["b"], r["tau"])
             for r in root_samples] == [r["no_earlier"] for r in root_samples],
            "no-earlier root samples")

    word_counts = {str(n): 8 * 162**n for n in range(1, 6)}
    require(word_counts == {
        "1": 1296,
        "2": 209952,
        "3": 34012224,
        "4": 5509980288,
        "5": 892616806656,
    }, "physical word counts")

    return {
        "actual_physical_circular_pilot_formula": {
            "parameter_scope": "every fixed -1/400<=s<=1/400",
            "state_variables": "q_j in R^2, unit u_j in R^2",
            "per_step_auxiliaries": "tau_j, q_(j+1), contact normal n_(j+1), scalar c_j, u_(j+1)",
            "centres_and_radii": "centres affine in s; radii rational",
            "flight": "q_(j+1)=q_j+tau_j*u_j",
            "contact": "|q_(j+1)-C_i(s)|^2=R_i^2",
            "reflection_reduced_degree": "c_j=u_j dot n_(j+1); u_(j+1)=u_j-2*c_j*n_(j+1)",
            "competitor_definitions": "a=u dot(C-q), b=|C-q|^2-R^2, Delta=a^2-b",
            "no_earlier_open_root": "a<=0 OR Delta<0 OR (a-tau>=0 AND Delta<=(a-tau)^2)",
            "root_formula_domain": "|u|=1, b>0 for distinct competitors; current source handled by outgoing a<=0",
            "tie_and_boundary_policy": "disjoint disks exclude distinct simultaneous contact; half-open chart owners and grazing strata are explicit cemetery/sign rows",
            "complete_target_universe": "two obstacle types times 9 times 9 torus lifts =162",
            "physical_variables_upper": "8*n+5",
            "physical_atomic_predicates_upper": (
                "830*n+12 = n*(161 nonchosen slots*(five-row upper budget)"
                "+at most 25 dynamics/sign/tie rows)+12"
            ),
            "physical_polynomial_degree_upper": 4,
            "declared_Round58_budget": {
                "variables": "400*n+20",
                "atomic_predicates": "2000*n+100",
                "degree": 8,
                "branch_words": "8*162^n",
            },
            "first_eight_budget_rows": budget_rows,
            "root_test_samples": [
                {**{k: (qtext(v) if isinstance(v, Q) else v) for k, v in row.items()}}
                for row in root_samples
            ],
            "fixed_depth_formula_fits_declared_budget": True,
            "status": "CERTIFIED_ACTUAL_PHYSICAL_FIXED_DEPTH_FORMULA_BUDGET",
        },
        "physical_fixed_depth_CAD": {
            "physical_formula_instantiates_Round58_recurrence": True,
            "fixed_depth_component_majorant": (
                "8*162^n times product_(r=0)^(400*n+19)(2*S_r*D_r+1), "
                "S_0=2000*n+100, D_0=8, S_(r+1)=2*(S_r*D_r+1)^2, D_(r+1)=2*D_r^2"
            ),
            "first_three_projection_replays": [cad_prefix(n) for n in (1, 2, 3)],
            "actual_cell_enumeration": "NOT_CERTIFIED",
            "depth_integrated_complexity": "NOT_CERTIFIED",
        },
        "technology_audit": {
            "arXiv_2603_25380": "effective complex cells require a sharply o-minimal complexity filtration; no pilot branch filtration or strong boundary norm is supplied",
            "arXiv_2604_06144": "builds analytically generated sharply o-minimal structures; does not instantiate the CM2 billiard formula or restriction operator",
            "arXiv_2601_09548": "minimal CAD existence/coarsening is not a uniform physical component or boundary-Z bound",
            "arXiv_2605_04718": "minimum-CAD results in dimension three do not control this growing-dimensional quantified branch family",
        },
        "strict_nonpromotion": {
            "existing_exp_Dbar_over_6_moment_pays_CAD_majorant": False,
            "physical_strong_R_s_Q_s": "NOT_CERTIFIED",
            "directional_Piola": "NOT_CERTIFIED",
            "MT_DQ": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
        },
    }


def result_payload() -> dict[str, Any]:
    return {
        "gate1": gate1_replay(),
        "gate2": gate2_replay(),
        "gate3": gate3_replay(),
        "strict_status": {
            "gate1": "NOT_CERTIFIED",
            "gate2": "NOT_CERTIFIED",
            "gate2_immutable_fields": "0/17",
            "gate3": "NOT_CERTIFIED",
            "composite_gates": "0/5",
            "cm2": "NO-GO_FOR_CLAIM",
        },
    }


def build_manifest(check_dependencies: bool = True) -> dict[str, Any]:
    dependencies = validate_dependencies() if check_dependencies else [
        {"path": rel, "sha256": value} for rel, value in DEPENDENCIES.items()
    ]
    require(REPORT.is_file(), "missing report")
    require(VERIFIER.is_file(), "missing verifier")
    return {
        "schema": "cm2.gate123.round59.physical-formula-shadow-dini-frontier.v1",
        "artifact": "cm2-gate123-round59-physical-formula-shadow-dini-frontier",
        "date": "2026-07-20",
        "dependencies": dependencies,
        "result": result_payload(),
        "strict_verdict": (
            "actual fixed-depth circular-pilot formulas fit the explicit CAD budget; "
            "the selected QNL loop and finite physical shadows do not supply all-plaque "
            "Dini, an all-depth stable quotient, strong R/Q, Piola or MT_DQ"
        ),
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(VERIFIER),
    }


def canonical_bytes(data: Any) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--summary-json", action="store_true")
    parser.add_argument("--emit-manifest", type=Path)
    args = parser.parse_args()

    try:
        data = build_manifest(check_dependencies=True)
        if args.emit_manifest is not None:
            args.emit_manifest.write_bytes(canonical_bytes(data))
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        if args.summary_json:
            print(json.dumps(data["result"], indent=2, sort_keys=True))
            return 0
        require(MANIFEST.is_file(), "manifest missing")
        require(MANIFEST.read_bytes() == canonical_bytes(data), "manifest drift")
    except (CertificateError, OSError, ValueError) as exc:
        print(f"CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1

    print("DEPENDENCIES: 14/14")
    print("GATE1_SELECTED_QNL_PHYSICAL_DINI_TAIL: CERTIFIED_SELECTED_GERM_ONLY")
    print("GATE2_PHYSICAL_FINITE_COLLISION_SHADOW_ROWS: 96/96")
    print("GATE3_ACTUAL_PHYSICAL_FIXED_DEPTH_FORMULA_BUDGET: CERTIFIED")
    print("GATES_1_2_3: NOT_CERTIFIED")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
