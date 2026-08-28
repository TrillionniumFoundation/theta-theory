#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round-64 Gate-2/4 tree leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round64-weighted-tree-saturation-actual-join-obstruction-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
LEDGER = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
CERT = HERE / "cm2_gate24_round64_weighted_tree_saturation_actual_join_obstruction_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "83b95101ebea318396beb04609551ae7bd48edc8bdee4da3c50747e2a656278f"

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

EXPECTED_STRICT = {
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

CP = Q(4 * 10**90 * 360493663, 358863)


class VerifyError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerifyError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerifyError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise VerifyError(f"non-finite JSON: {token}")


def strict_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def l1_uniform(values: list[Q]) -> Q:
    return sum((abs(value) for value in values), Q(0)) / len(values)


def weighted_median(values: list[Q], weights: list[Q]) -> Q:
    cumulative = Q(0)
    for value, index in sorted((value, index) for index, value in enumerate(values)):
        cumulative += weights[index]
        if cumulative >= Q(1, 2):
            return value
    raise VerifyError("weighted median exhausted")


def weighted_cost(markers: list[list[Q]], weights: list[Q]) -> tuple[list[Q], Q]:
    medians: list[Q] = []
    total = Q(0)
    atom_count = len(markers[0])
    for column in zip(*markers):
        median = weighted_median(list(column), weights)
        medians.append(median)
        total += sum((weight * abs(value - median) for weight, value in zip(weights, column)), Q(0)) / atom_count
    return medians, total


def dynamic(values: list[Q], image: list[int]) -> list[Q]:
    require(sorted(image) == list(range(len(values))), "dynamic permutation")
    inverse = [image.index(j) for j in range(len(image))]
    return [values[inverse[j]] for j in range(len(image))]


def load_manifest() -> dict[str, Any]:
    require(MANIFEST.is_file() and not MANIFEST.is_symlink() and MANIFEST.resolve().parent == HERE,
            "manifest path")
    value = strict_json(MANIFEST.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "manifest root")
    return value


def load_source(name: str) -> dict[str, Any]:
    value = strict_json((HERE / name).read_text(encoding="utf-8"))
    require(isinstance(value, dict) and isinstance(value.get("result"), dict),
            f"source manifest: {name}")
    return value["result"]


def check_files() -> None:
    for name, expected in PINNED_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
                f"pin path: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")
    for path in (CERT, VERIFIER, REPORT, MANIFEST):
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
                f"artifact path: {path.name}")


def integrity(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_files()
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    require(data.get("pins") == PINNED_FILES, "manifest pins")
    require(data.get("certificate_sha256") == sha256_path(CERT), "certificate hash")
    require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
    require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == recorded,
            "result digest")
    require(data.get("verdict") == result.get("strict_nonpromotion"), "verdict alias")


def replay_tree(result: dict[str, Any]) -> None:
    section = result["finite_weighted_tree_saturation"]
    replay = section["finite_replay"]
    require(digest(replay) == section["finite_replay_sha256"], "tree replay digest")
    weights = [Q(value) for value in replay["outer_weights"]]
    markers = [[Q(value) for value in row] for row in replay["source_root_pulled_markers"]]
    require(weights == [Q(1, 10), Q(1, 5), Q(3, 10), Q(2, 5)] and sum(weights) == 1,
            "tree weights")
    medians, delta = weighted_cost(markers, weights)
    require([qstr(value) for value in medians] == replay["pointwise_weighted_median"],
            "tree medians")
    require(delta == Q(replay["delta_T_source"]) == Q(3, 20), "tree delta")

    pairwise = Q(0)
    expected_pair_rows = []
    for i in range(len(markers)):
        for j in range(i + 1, len(markers)):
            distance = l1_uniform([x - y for x, y in zip(markers[i], markers[j])])
            weighted = weights[i] * weights[j] * distance
            pairwise += weighted
            expected_pair_rows.append((i, j, distance, weighted))
    require(pairwise == Q(19, 200) == Q(replay["pairwise_dispersion_P"]), "tree pairwise")
    require(Q(replay["twice_pairwise_dispersion_2P"]) == 2 * pairwise and
            pairwise <= delta <= 2 * pairwise, "sharp sandwich")
    require(len(replay["pair_rows"]) == len(expected_pair_rows) == 6, "pair rows")
    for row, expected in zip(replay["pair_rows"], expected_pair_rows):
        i, j, distance, weighted = expected
        require(row["i"] == i and row["j"] == j and
                Q(row["L1_distance"]) == distance and
                Q(row["weighted_pair_contribution"]) == weighted, "pair replay row")

    edge_specs = [(0, 1, [1]), (0, 2, [2, 3]), (2, 3, [3])]
    root_bound = Q(0)
    pair_tree = Q(0)
    lower = Q(0)
    require(len(replay["edge_rows"]) == 3, "edge rows")
    for row, (parent, child, subtree) in zip(replay["edge_rows"], edge_specs):
        distance = l1_uniform([x - y for x, y in zip(markers[parent], markers[child])])
        W = sum((weights[index] for index in subtree), Q(0))
        root_term = W * distance
        pair_term = 2 * W * (1 - W) * distance
        lower_term = min(weights[parent], weights[child]) * distance
        require(row["parent"] == parent and row["child"] == child and
                row["subtree_nodes"] == subtree and Q(row["subtree_weight_W_e"]) == W,
                "edge identity")
        require(Q(row["edge_defect_L1"]) == distance and
                Q(row["root_competitor_term_W_e_d_e"]) == root_term and
                Q(row["pair_path_term_2W_e_1minusW_e_d_e"]) == pair_term and
                Q(row["lower_obstruction_min_endpoint_weight_d_e"]) == lower_term,
                "edge arithmetic")
        root_bound += root_term
        pair_tree += pair_term
        lower = max(lower, lower_term)
    require(root_bound == Q(6, 25) == Q(replay["root_competitor_tree_bound"]),
            "root competitor bound")
    require(pair_tree == Q(129, 500) == Q(replay["pairwise_tree_path_bound"]),
            "pair tree bound")
    require(lower == Q(21, 200) == Q(replay["edge_lower_obstruction"]),
            "tree lower obstruction")
    require(lower <= delta <= min(root_bound, pair_tree), "tree inequalities")

    image = replay["common_dynamic_branch_image"]
    landing = [dynamic(marker, image) for marker in markers]
    landing_median, landing_delta = weighted_cost(landing, weights)
    require([[qstr(value) for value in row] for row in landing] == replay["landing_markers"],
            "landing markers")
    require([qstr(value) for value in landing_median] == replay["landing_weighted_median"],
            "landing median")
    require(landing_delta == delta == Q(replay["delta_T_landing"]), "landing delta")
    require(section["status"] ==
            "CERTIFIED_EXACT_FINITE_WEIGHTED_TREE_MEDIAN_PAIRWISE_AND_EDGE_CALCULUS",
            "tree status")


def replay_square(result: dict[str, Any]) -> None:
    section = result["whole_tree_branch_square_transport"]
    replay = section["finite_replay"]
    require(digest(replay) == section["finite_replay_sha256"], "square replay digest")
    require(replay["edge_count"] == 3 and replay["edge_commutator_action_norms"] == ["0"] * 3,
            "square edges")
    require(replay["source_edge_defect_norms"] == replay["landing_edge_defect_norms"] ==
            ["3/20", "1/10", "7/20"], "square edge norms")
    require(Q(replay["delta_T_source"]) == Q(replay["delta_T_landing"]) == Q(3, 20),
            "square deltas")
    require(Q(replay["P_source"]) == Q(replay["P_landing"]) == Q(19, 200),
            "square pairwise")
    require("does not force" in section["debt_guard"] and
            section["status"] ==
            "CERTIFIED_EXACT_WHOLE_TREE_BRANCH_SQUARE_TRANSPORT__PHYSICAL_TREE_ABSENT",
            "square status/guard")


def replay_budget(result: dict[str, Any]) -> None:
    section = result["root_to_all_plaques_quantitative_budget"]
    require("orientation-preserving C1" in section["hypotheses"] and
            "zero edge defect" in section["hypotheses"], "budget hypotheses")
    replay = section["finite_replay"]
    require(digest(replay) == section["finite_replay_sha256"], "budget replay digest")
    root = replay["root_tuple"]
    F, R, theta, length = Q(root["F_r"]), Q(root["R_r"]), Q(root["theta_r"]), Q(root["L_r"])
    require((F, R, theta, length) == (Q(3), Q(4), Q(1, 2), Q(2)), "budget root")
    edge_bounds = replay["edge_metric_derivative_bounds"]
    expected_paths = {0: [], 1: ["0->1"], 2: ["0->2"], 3: ["0->2", "2->3"]}
    expected_bounds = [Q(12), Q(72), Q(36), Q(80)]
    require(len(replay["node_rows"]) == 4, "budget node rows")
    max_ratio = Q(0)
    for row in replay["node_rows"]:
        node = row["node"]
        require(row["path"] == expected_paths[node], "budget path")
        m_path = Q(1)
        M_path = Q(1)
        for edge in row["path"]:
            m_path *= Q(edge_bounds[edge]["m_e"])
            M_path *= Q(edge_bounds[edge]["M_e"])
        bound = F * R * M_path / (m_path * m_path * theta * length)
        require(Q(row["m_path"]) == m_path and Q(row["M_path"]) == M_path,
                "budget path products")
        require(Q(row["z_upper"]) == bound == expected_bounds[node] and bound < CP and
                row["strictly_below_C_p"] is True, "budget node bound")
        max_ratio = max(max_ratio, M_path / (m_path * m_path))
    require(Q(replay["max_path_M_over_m_squared"]) == max_ratio and
            replay["all_node_strict_budget"] is True, "budget maximum")
    require(section["status"] ==
            "CERTIFIED_CONDITIONAL_ROOT_TO_ALL_PLAQUES_PATH_DISTORTION_BUDGET__ACTUAL_INPUTS_ABSENT",
            "budget status")


def replay_actual_join(result: dict[str, Any], *, source_files: bool = True) -> None:
    section = result["actual_branch_owner_landing_join"]
    replay = section["replay"]
    require(digest(replay) == section["replay_sha256"], "actual join digest")
    fragments = replay["pinned_fragment_rows"]
    missing = replay["missing_cross_plaque_key_rows"]
    require(len(fragments) == 5 and [row["id"] for row in fragments] == list(range(1, 6)),
            "fragment rows")
    require([row["artifact"] for row in fragments] == [
        PHYSICAL_MANIFESTS["round59_inverse"], PHYSICAL_MANIFESTS["round60_marker"],
        PHYSICAL_MANIFESTS["round61_curve"], PHYSICAL_MANIFESTS["round62_branch"],
        PHYSICAL_MANIFESTS["round58_owner"],
    ], "fragment artifacts")
    require(len(missing) == 7 and [row["id"] for row in missing] == list(range(1, 8)),
            "missing rows")
    require(all(row["state"] == "NOT_CERTIFIED_IN_PINNED_ACTUAL_CHAIN" for row in missing),
            "missing states")
    require(replay["pinned_fragments_replayed"] == "5/5" and
            replay["physical_tree_instantiation_rows_complete"] == "0/7" and
            replay["first_failed_cross_plaque_key"] ==
            "stable_tree_id/root_plaque/common_root_reference_law", "actual anti-join summary")
    require("not identified" in section["measure_law_guard"] and
            section["status"] ==
            "CERTIFIED_ACTUAL_FIELD_LEVEL_ANTI_JOIN__FIVE_FRAGMENTS_PRESENT_ZERO_OF_SEVEN_TREE_INSTANTIATION_ROWS",
            "actual join guard/status")
    if not source_files:
        return
    sources = {key: load_source(name) for key, name in PHYSICAL_MANIFESTS.items()}
    require(sources["round59_inverse"]["same_graph_rokhlin_reconditioning"]["status"] ==
            "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE",
            "source Round59")
    require(sources["round60_marker"]["actual_landing_RN_marker_bridge"]["status"] ==
            "CERTIFIED_ACTUAL_RN_MARKER_AND_CONDITIONAL_SAME_MEASURE_BAYES_FORMULA__FIELD4_PARTIAL_ONLY",
            "source Round60")
    require(sources["round61_curve"]["actual_marker_weighted_curve_lift"]["status"] ==
            "CERTIFIED_EXACT_ACTUAL_MARKER_WEIGHTED_CONE_CURVE_MEASURE_LIFT__NOT_REGULAR_STANDARD_FAMILY_OR_PHYSICAL_ROKHLIN_HOLONOMY_PRODUCT",
            "source Round61")
    require(sources["round62_branch"]["actual_branch_RN_covariance"]["status"] ==
            "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE",
            "source Round62")
    require(sources["round58_owner"]["physical_same_owner_extended_clearance_ledger"]["status"] ==
            "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE", "source Round58")


def replay_separator(result: dict[str, Any]) -> None:
    section = result["strong_assembly_separator"]
    rows = section["rows"]
    require(digest(rows) == section["rows_sha256"], "separator digest")
    frequencies = [1, 2, 17, 257, 4096]
    require(len(rows) == len(frequencies), "separator rows")
    for row, frequency in zip(rows, frequencies):
        require(row["frequency_N"] == frequency and row["marker_range"] == "[1/4,3/4]",
                "separator frequency/range")
        require((row["F"], row["R"], row["theta"], row["L"]) == (1, 3, 1, 1),
                "separator scalar tuple")
        require(Q(row["scalar_z_upper"]) == 3 < CP and
                row["scalar_z_upper_below_C_p"] is True, "separator strict budget")
        require(Q(row["weighted_tree_delta_T"]) == 0 and
                Q(row["all_edge_marker_defects"]) == 0 and
                Q(row["all_edge_square_commutators"]) == 0, "separator zero defects")
        require(Q(row["BV_variation_integral_abs_derivative"]) == frequency,
                "separator variation")
    require("not a refutation" in section["scope_guard"] and
            section["status"] ==
            "CERTIFIED_SMOOTH_FOUR_PLAQUE_ZERO_DEFECT_STRICT_BUDGET_STRONG_VARIATION_SEPARATOR",
            "separator guard/status")


def semantic_check(result: dict[str, Any], *, source_files: bool = True,
                   fixed_digest: bool = True) -> None:
    require(result.get("schema") == RESULT_SCHEMA, "result schema")
    provenance = result["provenance"]
    require(provenance["pinned_file_sha256"] == PINNED_FILES and
            provenance["Round63_recursive_root_pinned"] is True and
            provenance["Round63_independent_audit_pinned"] is True and
            provenance["Round63_relevant_leaf_pinned"] is True and
            provenance["used_actual_physical_artifacts_pinned"] is True,
            "provenance pins")
    require(provenance["old_artifacts_modified"] is False and
            provenance["external_theorem_promoted"] is False, "provenance guards")
    r63 = result["Round63_recursive_replay"]
    require(r63["independent_audit"] == "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED" and
            r63["Round63_two_plaque_delta_sat"] == "1/12" and
            r63["status"] == "PINNED_AND_REPLAYED", "Round63 replay")
    replay_tree(result)
    replay_square(result)
    replay_budget(result)
    replay_actual_join(result, source_files=source_files)
    replay_separator(result)
    fields = result["seven_field_materialization_audit"]
    require(fields["complete_rows"] == "1/7" and fields["partial_rows"] == [1, 4, 7] and
            fields["official_immutable_Gate2_fields"] == "0/17" and len(fields["rows"]) == 7,
            "seven fields")
    require(digest(fields["rows"]) == fields["rows_sha256"], "seven field digest")
    tech = result["latest_official_technology_audit"]
    require(tech["source"] == "official arXiv API" and tech["checked_on"] == "2026-07-21",
            "technology source/date")
    require("unique MME" in tech["arXiv_2604_25881v1"]["verified_claim"] and
            "not the frozen collision-SRB/owner law" in tech["arXiv_2604_25881v1"]["type_guard"],
            "MME wrong-law guard")
    require(tech["arXiv_2606_10155v1"]["verified_type"] == "review paper" and
            tech["new_direct_closure_found"] is False and
            tech["external_theorem_promoted"] is False, "review/technology guard")
    require(result["strict_nonpromotion"] == EXPECTED_STRICT, "strict frontier")
    if fixed_digest:
        replay = copy.deepcopy(result)
        replay.pop("internal_replay_digest", None)
        require(digest(replay) == EXPECTED_RESULT_DIGEST, "fixed semantic digest")


def deterministic_regeneration(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=180,
    )
    require(proc.returncode == 0,
            f"producer regeneration: {proc.stderr.decode('utf-8', 'replace').strip()}")
    require(proc.stdout == MANIFEST.read_bytes(), "producer regeneration bytes")
    regenerated = strict_json(proc.stdout.decode("utf-8"))
    require(regenerated == data, "producer regeneration object")


def check_sidecar() -> None:
    require(LEDGER.is_file() and not LEDGER.is_symlink() and LEDGER.resolve().parent == HERE,
            "SHA sidecar path")
    rows = [line.split() for line in LEDGER.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    require(len(rows) == 4, "SHA sidecar rows")
    expected_names = {REPORT.name, MANIFEST.name, CERT.name, VERIFIER.name}
    require({parts[-1] for parts in rows} == expected_names, "SHA sidecar names")
    for parts in rows:
        require(len(parts) == 2 and sha256_path(HERE / parts[1]) == parts[0],
                f"SHA sidecar mismatch: {parts[-1]}")


def run_audit(data: dict[str, Any], *, regenerate: bool = True, sidecar: bool = True) -> None:
    integrity(data)
    semantic_check(data["result"])
    if regenerate:
        deterministic_regeneration(data)
    if sidecar:
        check_sidecar()


def deep_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    out: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            if key != "internal_replay_digest":
                out.extend(deep_paths(value[key], prefix + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            out.extend(deep_paths(child, prefix + (index,)))
    else:
        out.append(prefix)
    return out


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    node = root
    for step in path:
        node = node[step]
    return node


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    node = root
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


def hostile_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "__HOSTILE"
    if value is None:
        return "HOSTILE"
    return {"hostile": True}


def self_test(data: dict[str, Any]) -> int:
    paths = deep_paths(data["result"])
    require(len(paths) >= 200, "hostile path count")
    rejected = 0
    for path in paths:
        mutant = copy.deepcopy(data)
        result = mutant["result"]
        set_path(result, path, hostile_value(get_path(result, path)))
        replay = copy.deepcopy(result)
        replay.pop("internal_replay_digest", None)
        result["internal_replay_digest"] = digest(replay)
        mutant["verdict"] = result["strict_nonpromotion"]
        try:
            semantic_check(result, source_files=False)
        except (VerifyError, ValueError, KeyError, TypeError, IndexError, ArithmeticError):
            rejected += 1
    require(rejected == len(paths), f"hostile semantic accepted: {rejected}/{len(paths)}")

    hostile_json = ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}']
    json_rejected = 0
    for payload in hostile_json:
        try:
            strict_json(payload)
        except (VerifyError, ValueError):
            json_rejected += 1
    require(json_rejected == len(hostile_json), "hostile JSON accepted")
    print(f"HOSTILE_SEMANTIC_MUTATIONS_REJECTED: {rejected}/{len(paths)}")
    print(f"STRICT_JSON_PAYLOADS_REJECTED: {json_rejected}/{len(hostile_json)}")
    return rejected + json_rejected


def reemit(path: Path, data: dict[str, Any]) -> None:
    target = path.resolve()
    require(target.parent == HERE, "reemit parent")
    protected = set(PINNED_FILES) | {REPORT.name, MANIFEST.name, CERT.name, VERIFIER.name, LEDGER.name}
    require(target.name not in protected, "reemit protected target")
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=180,
    )
    require(proc.returncode == 0, "reemit producer failure")
    target.write_bytes(proc.stdout)
    require(target.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
    reloaded = strict_json(target.read_text(encoding="utf-8"))
    require(reloaded == data, "reemit object")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        if args.audit:
            run_audit(data)
            print("AUDIT_MODE: PASS")
            return 0
        if args.self_test:
            run_audit(data)
            self_test(data)
            print("SELF_TEST: PASS")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            reemit(args.reemit, data)
            print(f"REEMIT: {args.reemit}")
            return 0
    except (VerifyError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print(f"ROUND64_GATE24_WEIGHTED_TREE_VERIFY_ERROR: {exc}", file=sys.stderr)
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
