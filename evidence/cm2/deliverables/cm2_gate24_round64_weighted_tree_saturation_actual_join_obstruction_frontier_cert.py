#!/usr/bin/env python3
"""Round-64 Gate-2/4 weighted-tree saturation and actual-join frontier.

This append-only producer certifies exact finite weighted-tree L1 calculus,
an actual pinned-data anti-join, a root-to-tree distortion interface, and a
strong-assembly nonimplication.  It does not certify a physical stable tree,
Gate 2, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round64-weighted-tree-saturation-actual-join-obstruction-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_gate24_round64_weighted_tree_saturation_actual_join_obstruction_frontier_verifier.py"

PINNED_FILES = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-2026-07-21.md":
        "b30aff208e9e5707e443f59abd07507f7f9d93d765ecaf3fd675f4150c5bf978",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2_round63_independent_core_frontier_audit_cert.py":
        "5b07b546047fbfa6f71bd3decc85b7e3a45af78b5a5c2ff2964b20f9b8d82ae8",
    "cm2_round63_independent_core_frontier_audit_verifier.py":
        "6b0c96f483977cb6bd0917da094841fb771bd1b5edcf1d0b2bdfe078d5b245ae",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-assault-2026-07-21.md":
        "e57ba8db9a7ab0a8dc7643b575d02de99a10377ce36ba0efd1ba8ae75477325c",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json":
        "955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256":
        "a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870",
    "cm2_gate24_round63_stable_saturation_holonomy_square_frontier_cert.py":
        "53d65a825b8f32b3320ed30383d89a3f49387735afec0f6680bfe74f0b003804",
    "cm2_gate24_round63_stable_saturation_holonomy_square_frontier_verifier.py":
        "4413e242251a8f5ef6e7572fcba872eaf7780585b820b181ee90044bc1a5e907",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json":
        "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json":
        "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
}

PHYSICAL_MANIFESTS = {
    "round58_owner": "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json",
    "round59_inverse": "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json",
    "round60_marker": "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json",
    "round61_curve": "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json",
    "round62_branch": "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json",
}

CP = Q(4 * 10**90 * 360493663, 358863)

STRICT = {
    "finite_weighted_tree_median_formula": "CERTIFIED_EXACT",
    "pairwise_dispersion_sandwich": "CERTIFIED_EXACT_SHARP",
    "zero_saturation_iff_all_spanning_tree_edge_defects_zero": "CERTIFIED_EXACT",
    "whole_tree_branch_holonomy_square_transport": "CERTIFIED_EXACT_INTERFACE",
    "actual_branch_owner_landing_fragments": "CERTIFIED_PINNED_5_OF_5",
    "actual_physical_stable_tree_and_common_root_law": "NOT_CERTIFIED",
    "actual_marker_zero_defect": "NOT_CERTIFIED",
    "root_to_all_plaques_path_distortion_budget": "CERTIFIED_CONDITIONAL",
    "actual_FRthetaL_edge_mM_strict_budget": "NOT_CERTIFIED",
    "strict_scalar_rows_imply_uniform_BV_strong_assembly": "FALSE_BY_CERTIFIED_SEPARATOR",
    "physical_invariant_product_rectangles": "NOT_CERTIFIED",
    "physical_stable_projection_and_two_sided_J_hol": "NOT_CERTIFIED",
    "physical_strong_restriction_and_assembly": "NOT_CERTIFIED",
    "seven_field_landing_join": "1/7_COMPLETE__FIELDS_1_4_7_PARTIAL",
    "official_immutable_Gate2_fields": "0/17",
    "proper_physical_same_ID_first_return_kernel": "NOT_CERTIFIED",
    "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
    "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
    "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
    "strong_singular_current_cemetery": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CertificateError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CertificateError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise CertificateError(f"non-finite JSON: {token}")


def strict_json_path(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON root: {path.name}")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def qlist(values: list[Q]) -> list[str]:
    return [qstr(value) for value in values]


def qmatrix(rows: list[list[Q]]) -> list[list[str]]:
    return [qlist(row) for row in rows]


def l1_uniform(values: list[Q]) -> Q:
    return sum((abs(value) for value in values), Q(0)) / len(values)


def dynamic_transfer(values: list[Q], image: list[int]) -> list[Q]:
    require(sorted(image) == list(range(len(values))), "dynamic permutation")
    inverse = [image.index(j) for j in range(len(image))]
    return [values[inverse[j]] for j in range(len(image))]


def weighted_median(values: list[Q], weights: list[Q]) -> Q:
    require(len(values) == len(weights) and sum(weights, Q(0)) == 1, "weighted median input")
    cumulative = Q(0)
    for value, index in sorted((value, index) for index, value in enumerate(values)):
        cumulative += weights[index]
        if cumulative >= Q(1, 2):
            return value
    raise CertificateError("weighted median exhausted")


def weighted_median_cost(markers: list[list[Q]], weights: list[Q]) -> tuple[list[Q], Q]:
    atom_count = len(markers[0])
    require(all(len(marker) == atom_count for marker in markers), "marker dimensions")
    medians: list[Q] = []
    cost = Q(0)
    for column in zip(*markers):
        median = weighted_median(list(column), weights)
        medians.append(median)
        cost += sum((weight * abs(value - median) for weight, value in zip(weights, column)), Q(0)) / atom_count
    return medians, cost


def weighted_tree_replay() -> dict[str, Any]:
    weights = [Q(1, 10), Q(2, 10), Q(3, 10), Q(4, 10)]
    markers = [
        [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)],
        [Q(1, 4), Q(1, 4), Q(1, 2), Q(1, 2), Q(3, 4)],
        [Q(0), Q(1, 2), Q(1, 2), Q(3, 4), Q(3, 4)],
        [Q(1, 2), Q(0), Q(1, 4), Q(1), Q(1, 2)],
    ]
    median, delta = weighted_median_cost(markers, weights)
    require(median == [Q(1, 4), Q(1, 4), Q(1, 2), Q(3, 4), Q(3, 4)], "median replay")
    require(delta == Q(3, 20), "delta replay")

    pair_rows: list[dict[str, Any]] = []
    pairwise = Q(0)
    for i in range(len(markers)):
        for j in range(i + 1, len(markers)):
            distance = l1_uniform([x - y for x, y in zip(markers[i], markers[j])])
            weighted = weights[i] * weights[j] * distance
            pairwise += weighted
            pair_rows.append({
                "i": i,
                "j": j,
                "L1_distance": qstr(distance),
                "weighted_pair_contribution": qstr(weighted),
            })
    require(pairwise == Q(19, 200), "pairwise replay")
    require(pairwise <= delta <= 2 * pairwise, "pairwise sandwich")

    edge_specs = [
        (0, 1, [1]),
        (0, 2, [2, 3]),
        (2, 3, [3]),
    ]
    edge_rows: list[dict[str, Any]] = []
    root_bound = Q(0)
    pair_tree_bound = Q(0)
    lower = Q(0)
    for parent, child, subtree in edge_specs:
        distance = l1_uniform([x - y for x, y in zip(markers[parent], markers[child])])
        subtree_weight = sum((weights[index] for index in subtree), Q(0))
        root_term = subtree_weight * distance
        pair_term = 2 * subtree_weight * (1 - subtree_weight) * distance
        lower_term = min(weights[parent], weights[child]) * distance
        root_bound += root_term
        pair_tree_bound += pair_term
        lower = max(lower, lower_term)
        edge_rows.append({
            "parent": parent,
            "child": child,
            "subtree_nodes": subtree,
            "subtree_weight_W_e": qstr(subtree_weight),
            "edge_defect_L1": qstr(distance),
            "root_competitor_term_W_e_d_e": qstr(root_term),
            "pair_path_term_2W_e_1minusW_e_d_e": qstr(pair_term),
            "lower_obstruction_min_endpoint_weight_d_e": qstr(lower_term),
        })
    require(root_bound == Q(6, 25), "root tree bound")
    require(pair_tree_bound == Q(129, 500), "pair tree bound")
    require(lower == Q(21, 200), "edge lower bound")
    require(lower <= delta <= min(root_bound, pair_tree_bound), "tree bounds")

    image = [1, 2, 3, 4, 0]
    landing = [dynamic_transfer(marker, image) for marker in markers]
    landing_median, landing_delta = weighted_median_cost(landing, weights)
    landing_pairwise = Q(0)
    for i in range(len(landing)):
        for j in range(i + 1, len(landing)):
            landing_pairwise += weights[i] * weights[j] * l1_uniform(
                [x - y for x, y in zip(landing[i], landing[j])]
            )
    require(landing_median == dynamic_transfer(median, image), "dynamic median")
    require(landing_delta == delta and landing_pairwise == pairwise, "dynamic whole-tree isometry")

    replay = {
        "root_reference_law": ["1/5"] * 5,
        "outer_weights": qlist(weights),
        "tree_edges": [[0, 1], [0, 2], [2, 3]],
        "source_root_pulled_markers": qmatrix(markers),
        "pointwise_weighted_median": qlist(median),
        "delta_T_source": qstr(delta),
        "pair_rows": pair_rows,
        "pairwise_dispersion_P": qstr(pairwise),
        "twice_pairwise_dispersion_2P": qstr(2 * pairwise),
        "edge_rows": edge_rows,
        "root_competitor_tree_bound": qstr(root_bound),
        "pairwise_tree_path_bound": qstr(pair_tree_bound),
        "edge_lower_obstruction": qstr(lower),
        "common_dynamic_branch_image": image,
        "landing_markers": qmatrix(landing),
        "landing_weighted_median": qlist(landing_median),
        "delta_T_landing": qstr(landing_delta),
        "pairwise_dispersion_P_landing": qstr(landing_pairwise),
        "all_edge_commutator_norms": "0",
    }
    return {
        "definition": "delta_T=inf_f sum_i w_i||g_i-P_ri f||_1 on a finite rooted holonomy tree",
        "exact_median_formula": "delta_T=integral min_t sum_i w_i|P_ri^-1 g_i-t| dmu_r, attained by a measurable pointwise weighted median",
        "pairwise_dispersion": "P=sum_(i<j)w_i*w_j||P_ri^-1 g_i-P_rj^-1 g_j||_1",
        "sharp_sandwich": "P<=delta_T<=2P; both constants are sharp",
        "tree_upper": "delta_T<=min(sum_e W_e*d_e,2*sum_e W_e*(1-W_e)*d_e)",
        "tree_lower": "delta_T>=max_e min(w_parent,w_child)*d_e",
        "zero_criterion": "delta_T=0 iff every spanning-tree edge marker defect d_e is zero",
        "shortened_interface": "one root law plus a spanning tree of positive onto L1 isometries and zero edge defects automatically constructs the global quotient marker as a weighted median",
        "scope_guard": "exact finite abstract L1 theorem; no physical billiard stable tree is asserted",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_FINITE_WEIGHTED_TREE_MEDIAN_PAIRWISE_AND_EDGE_CALCULUS",
    }


def tree_square_transport(tree: dict[str, Any]) -> dict[str, Any]:
    replay0 = tree["finite_replay"]
    edge_rows = replay0["edge_rows"]
    replay = {
        "edge_count": len(edge_rows),
        "source_edge_defect_norms": [row["edge_defect_L1"] for row in edge_rows],
        "landing_edge_defect_norms": [row["edge_defect_L1"] for row in edge_rows],
        "edge_commutator_action_norms": ["0"] * len(edge_rows),
        "delta_T_source": replay0["delta_T_source"],
        "delta_T_landing": replay0["delta_T_landing"],
        "P_source": replay0["pairwise_dispersion_P"],
        "P_landing": replay0["pairwise_dispersion_P_landing"],
    }
    require(replay["delta_T_source"] == replay["delta_T_landing"] == "3/20", "tree square delta")
    require(replay["P_source"] == replay["P_landing"] == "19/200", "tree square pairwise")
    return {
        "edge_identity": "Delta_e^L=D_child*Delta_e^S+C_e(a_parent), C_e=D_child*P_e^S-P_e^L*D_parent",
        "edge_two_sided_bound": "||Delta_e^S||_1-||C_e(a_parent)||_1<=||Delta_e^L||_1<=||Delta_e^S||_1+||C_e(a_parent)||_1",
        "landing_upper": "delta_T^L<=2*sum_e W_e*(1-W_e)*(||Delta_e^S||_1+||C_e(a_parent)||_1)",
        "landing_lower": "delta_T^L>=max_e min(w_parent,w_child)*(||Delta_e^S||_1-||C_e(a_parent)||_1)_+",
        "commuting_tree_theorem": "if every edge square commutes, D_i*P_ri^S=P_ri^L*D_r and the onto L1 isometry D_r gives delta_T^L=delta_T^S and P_L=P_S",
        "debt_guard": "commuting dynamics transports the whole multi-plaque saturation debt and does not force it to vanish",
        "physical_guard": "the actual source/landing stable tree and its edge commutators are not constructed",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_EXACT_WHOLE_TREE_BRANCH_SQUARE_TRANSPORT__PHYSICAL_TREE_ABSENT",
    }


def tree_quantitative_budget() -> dict[str, Any]:
    root = {"F_r": Q(3), "R_r": Q(4), "theta_r": Q(1, 2), "L_r": Q(2)}
    edge_bounds = {
        "0->1": (Q(1, 2), Q(3, 2)),
        "0->2": (Q(2, 3), Q(4, 3)),
        "2->3": (Q(3, 4), Q(5, 4)),
    }
    paths = {
        0: [],
        1: ["0->1"],
        2: ["0->2"],
        3: ["0->2", "2->3"],
    }
    rows: list[dict[str, Any]] = []
    expected = [Q(12), Q(72), Q(36), Q(80)]
    for node, path in paths.items():
        m_path = Q(1)
        M_path = Q(1)
        for edge in path:
            m_edge, M_edge = edge_bounds[edge]
            m_path *= m_edge
            M_path *= M_edge
        bound = root["F_r"] * root["R_r"] * M_path / (
            m_path * m_path * root["theta_r"] * root["L_r"]
        )
        require(bound == expected[node] and bound < CP, f"tree quantitative node {node}")
        rows.append({
            "node": node,
            "path": path,
            "m_path": qstr(m_path),
            "M_path": qstr(M_path),
            "z_upper": qstr(bound),
            "strictly_below_C_p": True,
        })
    max_ratio = max(Q(row["M_path"]) / Q(row["m_path"])**2 for row in rows)
    replay = {
        "C_p": qstr(CP),
        "root_tuple": {key: qstr(value) for key, value in root.items()},
        "edge_metric_derivative_bounds": {
            edge: {"m_e": qstr(bounds[0]), "M_e": qstr(bounds[1])}
            for edge, bounds in edge_bounds.items()
        },
        "node_rows": rows,
        "max_path_M_over_m_squared": qstr(max_ratio),
        "all_node_strict_budget": True,
    }
    return {
        "hypotheses": "on every edge h_e is orientation-preserving C1 in one adapted arclength, E_child=h_e(E_parent), f_child(h_e x)=c_e*f_parent(x)/lambda_e(x) with c_e>0, 0<m_e<=lambda_e=dh_e/ds<=M_e, and the marker tree has zero edge defect",
        "path_products": "m_i=product_path m_e and M_i=product_path M_e",
        "transport_rows": "F_i=F_r, |E_i|>=m_i*theta_r*L_r, R_i<=R_r*M_i/m_i",
        "node_bound": "z_i<=F_r*R_r*M_i/(m_i^2*theta_r*L_r)",
        "single_root_strict_budget": "F_r*R_r*max_i(M_i/m_i^2)<C_p*theta_r*L_r",
        "shortening": "one root F,R,theta,L tuple and two derivative constants per edge replace six unrelated inputs on every plaque",
        "physical_guard": "no pinned actual artifact supplies the physical tree, root tuple, or edge adapted-arclength m_e,M_e",
        "finite_replay": replay,
        "finite_replay_sha256": digest(replay),
        "status": "CERTIFIED_CONDITIONAL_ROOT_TO_ALL_PLAQUES_PATH_DISTORTION_BUDGET__ACTUAL_INPUTS_ABSENT",
    }


def load_result(name: str) -> dict[str, Any]:
    data = strict_json_path(HERE / name)
    result = data.get("result")
    require(isinstance(result, dict), f"manifest result: {name}")
    return result


def actual_data_join() -> dict[str, Any]:
    sources = {key: load_result(name) for key, name in PHYSICAL_MANIFESTS.items()}
    r58 = sources["round58_owner"]
    r59 = sources["round59_inverse"]
    r60 = sources["round60_marker"]
    r61 = sources["round61_curve"]
    r62 = sources["round62_branch"]

    require(r59["same_graph_rokhlin_reconditioning"]["status"] ==
            "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE",
            "Round59 inverse")
    require(r60["actual_landing_RN_marker_bridge"]["status"] ==
            "CERTIFIED_ACTUAL_RN_MARKER_AND_CONDITIONAL_SAME_MEASURE_BAYES_FORMULA__FIELD4_PARTIAL_ONLY",
            "Round60 marker")
    require(r61["actual_marker_weighted_curve_lift"]["status"] ==
            "CERTIFIED_EXACT_ACTUAL_MARKER_WEIGHTED_CONE_CURVE_MEASURE_LIFT__NOT_REGULAR_STANDARD_FAMILY_OR_PHYSICAL_ROKHLIN_HOLONOMY_PRODUCT",
            "Round61 curve lift")
    require(r62["actual_branch_RN_covariance"]["status"] ==
            "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE",
            "Round62 branch covariance")
    require(r58["physical_same_owner_extended_clearance_ledger"]["status"] ==
            "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE", "Round58 owner law")
    require(r62["strict_nonpromotion"]["physical_invariant_product_quotient_and_J_hol"] ==
            "NOT_CERTIFIED", "Round62 physical product guard")
    require(r61["strict_nonpromotion"]["physical_invariant_unstable_Rokhlin_and_stable_holonomy"] ==
            "NOT_CERTIFIED", "Round61 physical holonomy guard")
    require(r60["seven_field_materialization_audit"]["actual_complete_rows"] == "1/7",
            "Round60 landing count")
    require(r59["seven_field_materialization_audit"]["actual_complete_rows"] == "1/7",
            "Round59 landing count")
    require(r58["physical_same_owner_extended_clearance_ledger"]["coverage_not_certified"] ==
            "nu(A_col^c)=0 is NOT_CERTIFIED", "Round58 coverage guard")

    fragments = [
        {
            "id": 1,
            "artifact": PHYSICAL_MANIFESTS["round59_inverse"],
            "fragment": "tagged Borel first-return branch inverse",
            "carrier": "same graph law Gamma_cap disintegrated over a supplied weak quotient eta",
            "payload": "source/landing/n/path/physical-ID/half-open-owner identities Gamma_u-a.s.",
            "state": "CERTIFIED_PINNED",
        },
        {
            "id": 2,
            "artifact": PHYSICAL_MANIFESTS["round60_marker"],
            "fragment": "actual landing RN marker",
            "carrier": "collision-SRB landing law mu_C restricted to C_s",
            "payload": "g_B=d kappa_B/d mu_C with 0<=g_B<=1",
            "state": "CERTIFIED_PINNED",
        },
        {
            "id": 3,
            "artifact": PHYSICAL_MANIFESTS["round61_curve"],
            "fragment": "actual tagged cone-curve marker lift",
            "carrier": "countable tagged finite-depth cone-curve measure representation",
            "payload": "positive marked landing curve measures retaining branch tags",
            "state": "CERTIFIED_PINNED_PARTIAL_PRODUCT_ONLY",
        },
        {
            "id": 4,
            "artifact": PHYSICAL_MANIFESTS["round62_branch"],
            "fragment": "actual dynamic branch RN covariance",
            "carrier": "each frozen invertible tagged raw first-return branch",
            "payload": "g_B=a o H^-1 before n/path/ID/owner/once tags are forgotten",
            "state": "CERTIFIED_PINNED_DYNAMIC_NOT_STABLE",
        },
        {
            "id": 5,
            "artifact": PHYSICAL_MANIFESTS["round58_owner"],
            "fragment": "finite physical owner/root law",
            "carrier": "standard-Borel owner/root base law nu restricted without normalization to A_col",
            "payload": "Borel owner, clearance and extended clock registry",
            "state": "CERTIFIED_PINNED_COVERAGE_AND_FINITE_MOMENT_OPEN",
        },
    ]

    missing = [
        {
            "id": 1,
            "required_key": "stable_tree_id/root_plaque/common_root_reference_law",
            "evidence": "Round61 denies an invariant Rokhlin/stable-holonomy product and Round62 keeps the physical quotient/J_hol NOT_CERTIFIED",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 2,
            "required_key": "positive_outer_weights_on_actual_tree_nodes",
            "evidence": "no pinned actual artifact gives a common stable-tree plaque index and its outer disintegration weights",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 3,
            "required_key": "source_and_landing_stable_edge_maps_with_two_sided_RN_Jacobians",
            "evidence": "actual dynamic branch covariance is explicitly not stable-holonomy covariance",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 4,
            "required_key": "same-branch edge_commutator_and_collision_SRB_marker_defect",
            "evidence": "Round63 supplies exact formulas only; no actual edge registry or zero defect is materialized",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 5,
            "required_key": "root_F_R_theta_L_and_edge_adapted_arclength_m_M",
            "evidence": "tagged cone-curve marking permits arbitrary fragmentation/oscillation and supplies no stable-tree metric derivative",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 6,
            "required_key": "strict_root_to_all_plaques_C_p_budget",
            "evidence": "the seven-field physical boundary row remains NOT_CERTIFIED",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
        {
            "id": 7,
            "required_key": "endpoint_preserving_transfer_intertwining_Piola_strong_recipient",
            "evidence": "the graph/current recipient is explicitly not the required physical anisotropic strong assembly",
            "state": "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN",
        },
    ]
    replay = {
        "pinned_fragment_rows": fragments,
        "missing_cross_plaque_key_rows": missing,
        "pinned_fragments_replayed": "5/5",
        "physical_tree_instantiation_rows_complete": "0/7",
        "first_failed_cross_plaque_key": missing[0]["required_key"],
    }
    return {
        "method": "strict-JSON field-level join over five pinned actual manifests",
        "positive_join": "the branch inverse, landing marker, curve lift, dynamic RN covariance, and owner/root law all replay on their declared carriers",
        "anti_join": "no pinned row keys those carriers into one physical stable holonomy tree",
        "measure_law_guard": "the owner law nu, landing collision-SRB law mu_C, and weak quotient law eta are not identified by a certified stable-tree crosswalk",
        "shortest_zero_route": "materialize one root law and spanning stable tree and prove every actual edge marker defect zero; the weighted median then constructs the quotient marker automatically",
        "falsification_route": "one certified positive edge defect d_e gives delta_T>=min(w_parent,w_child)*d_e>0",
        "scope_guard": "the anti-join certifies missing keys in the pinned chain, not impossibility of a future physical construction",
        "replay": replay,
        "replay_sha256": digest(replay),
        "status": "CERTIFIED_ACTUAL_FIELD_LEVEL_ANTI_JOIN__FIVE_FRAGMENTS_PRESENT_ZERO_OF_SEVEN_TREE_INSTANTIATION_ROWS",
    }


def strong_assembly_separator() -> dict[str, Any]:
    frequencies = [1, 2, 17, 257, 4096]
    rows = []
    for frequency in frequencies:
        rows.append({
            "frequency_N": frequency,
            "marker": "g_N(x)=1/2+(1/4)sin(2*pi*N*x)",
            "marker_range": "[1/4,3/4]",
            "F": 1,
            "R": 3,
            "theta": 1,
            "L": 1,
            "scalar_z_upper": "3",
            "scalar_z_upper_below_C_p": True,
            "weighted_tree_delta_T": "0",
            "all_edge_marker_defects": "0",
            "all_edge_square_commutators": "0",
            "BV_variation_integral_abs_derivative": str(frequency),
        })
    require(CP > 3 and rows[-1]["BV_variation_integral_abs_derivative"] == "4096",
            "strong separator")
    return {
        "model": "four identity product plaques with arbitrary positive weights, identity stable holonomies, identity dynamic branches, and the same smooth marker g_N",
        "simultaneous_weak_rows": "delta_T=0, every square commutes, every marker defect is zero, and F*R/(theta*L)=3<C_p",
        "exact_variation": "integral_0^1 |g_N'(x)| dx=N",
        "conclusion": "whole-tree zero defect plus the strict scalar properness budget does not imply a uniform plaque-BV/derivative strong bound",
        "scope_guard": "exact smooth logical nonimplication; not a billiard realization and not a refutation of every possible anisotropic norm",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_SMOOTH_FOUR_PLAQUE_ZERO_DEFECT_STRICT_BUDGET_STRONG_VARIATION_SEPARATOR",
    }


def seven_fields() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical invariant product rectangles", "state": "PARTIAL_TAGGED_FINITE_DEPTH_CONE_CURVE_ATLAS_ONLY__NO_INVARIANT_TREE"},
        {"field": 2, "name": "stable projection and two-sided J_hol", "state": "NOT_CERTIFIED__EXACT_WEIGHTED_TREE_CALCULUS_ONLY"},
        {"field": 3, "name": "full span or marker fragmentation", "state": "NOT_CERTIFIED__ROOT_TO_TREE_CONDITIONAL_TRANSPORT_ONLY"},
        {"field": 4, "name": "same-law conditionals and density bounds", "state": "PARTIAL_ACTUAL_LANDING_RN_MARKER_AND_DYNAMIC_BRANCH_COVARIANCE__NO_STABLE_QUOTIENT"},
        {"field": 5, "name": "physical boundary charge below C_p", "state": "NOT_CERTIFIED__NO_ACTUAL_INPUTS_TO_ROOT_TREE_BUDGET"},
        {"field": 6, "name": "tagged Borel branch inverse", "state": "CERTIFIED_PINNED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "state": "PARTIAL_GRAPH_CURRENT_LEDGER_ONLY__PHYSICAL_STRONG_MAP_ABSENT"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "complete_rows": "1/7",
        "partial_rows": [1, 4, 7],
        "official_immutable_Gate2_fields": "0/17",
        "status": "CERTIFIED_ROUND64_SEVEN_FIELD_AUDIT__ONE_COMPLETE_THREE_PARTIAL__NO_GATE_PROMOTION",
    }


def round63_replay() -> dict[str, Any]:
    audit = load_result("cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json")
    leaf = load_result("cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json")
    require(audit["strict_final_state"]["audit_verdict"] ==
            "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED", "Round63 audit verdict")
    require(audit["strict_final_state"]["Gate2"] ==
            "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17", "Round63 Gate2")
    require(audit["strict_final_state"]["Gate4"] ==
            "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL", "Round63 Gate4")
    require(leaf["strict_nonpromotion"]["Gate2"] ==
            leaf["strict_nonpromotion"]["Gate4"] == "NOT_CERTIFIED", "Round63 leaf state")
    require(leaf["two_plaque_stable_saturation"]["finite_replay"]["delta_sat"] == "1/12",
            "Round63 two-plaque replay")
    return {
        "recursive_root_report_sha256": PINNED_FILES["cm2-sixty-third-direct-assault-2026-07-21.md"],
        "recursive_root_ledger_sha256": PINNED_FILES["cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256"],
        "independent_audit": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
        "Round63_two_plaque_delta_sat": "1/12",
        "Round63_Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Round63_Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "status": "PINNED_AND_REPLAYED",
    }


def latest_technology_audit() -> dict[str, Any]:
    return {
        "checked_on": "2026-07-21",
        "source": "official arXiv API",
        "arXiv_2604_25881v1": {
            "title": "Every finite horizon Sinai billiard map has a unique measure of maximal entropy",
            "verified_claim": "the unique MME is obtained as the product of Hausdorff measures on one-sided subshifts associated to the billiard map",
            "type_guard": "MME/Hausdorff subshift product is not the frozen collision-SRB/owner law mu_C and cannot instantiate this actual stable quotient",
        },
        "arXiv_2606_10155v1": {
            "title": "Recent Progress in the Application of Transfer Operators to Dispersing Billiards",
            "verified_type": "review paper",
            "type_guard": "a review does not materialize the pinned branch/owner/landing tree or physical strong assembly",
        },
        "new_direct_closure_found": False,
        "external_theorem_promoted": False,
        "status": "AUDITED_WRONG_LAW_MME_AND_REVIEW_DO_NOT_CLOSE_ACTUAL_TYPED_JOIN",
    }


def verify_pins() -> None:
    for name, expected in PINNED_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin file/type: {name}")
        require(path.resolve().parent == HERE, f"pin parent: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")


def build_result() -> dict[str, Any]:
    verify_pins()
    tree = weighted_tree_replay()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "claim_type": "exact finite weighted-tree L1 saturation calculus, whole-tree branch-square transport, actual physical field anti-join, and strong-assembly obstruction",
            "pinned_file_sha256": dict(PINNED_FILES),
            "Round63_recursive_root_pinned": True,
            "Round63_independent_audit_pinned": True,
            "Round63_relevant_leaf_pinned": True,
            "used_actual_physical_artifacts_pinned": True,
            "old_artifacts_modified": False,
            "external_theorem_promoted": False,
        },
        "Round63_recursive_replay": round63_replay(),
        "finite_weighted_tree_saturation": tree,
        "whole_tree_branch_square_transport": tree_square_transport(tree),
        "root_to_all_plaques_quantitative_budget": tree_quantitative_budget(),
        "actual_branch_owner_landing_join": actual_data_join(),
        "strong_assembly_separator": strong_assembly_separator(),
        "seven_field_materialization_audit": seven_fields(),
        "latest_official_technology_audit": latest_technology_audit(),
        "strict_nonpromotion": dict(STRICT),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink() and verifier.parent == HERE,
            "verifier path")
    require(DEFAULT_REPORT.is_file() and not DEFAULT_REPORT.is_symlink() and
            DEFAULT_REPORT.resolve().parent == HERE, "report path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": dict(PINNED_FILES),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        data = build_manifest(args.verifier)
        payload = render_manifest(data)
        if args.write_manifest is not None:
            target = args.write_manifest.resolve()
            require(target.parent == HERE, "manifest output parent")
            target.write_text(payload, encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(payload, end="")
            return 0
        if args.audit:
            result = data["result"]
            print("AUDIT: PASS")
            print("PINNED_FILES:", f"{len(PINNED_FILES)}/{len(PINNED_FILES)}")
            print("RESULT_SHA256:", result["internal_replay_digest"])
            return 0
    except (CertificateError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError) as exc:
        print(f"ROUND64_GATE24_WEIGHTED_TREE_CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1

    frontier = data["result"]["strict_nonpromotion"]
    print("WEIGHTED_TREE_MEDIAN:", frontier["finite_weighted_tree_median_formula"])
    print("ACTUAL_PHYSICAL_STABLE_TREE:", frontier["actual_physical_stable_tree_and_common_root_law"])
    print("PHYSICAL_STRONG_ASSEMBLY:", frontier["physical_strong_restriction_and_assembly"])
    print("GATE2:", frontier["Gate2"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
