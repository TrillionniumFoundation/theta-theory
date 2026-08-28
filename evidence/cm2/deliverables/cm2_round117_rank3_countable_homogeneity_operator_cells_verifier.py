#!/usr/bin/env python3
"""Independent verifier for the Round117 countable homogeneity schema."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round117_rank3_countable_homogeneity_operator_cells.py"
CERTIFICATE = HERE / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND113_MANIFEST = HERE / "cm2-one-hundred-thirteenth-direct-assault-manifest-2026-07-23.sha256"
SCHEMA = "cm2.round117.rank3-countable-homogeneity-operator-cells.v1"
VERIFY_SCHEMA = "cm2.round117.rank3-countable-homogeneity-operator-cells-verification.v1"
PRODUCER_SHA256 = "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c"
CERTIFICATE_SHA256 = "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0"
N0 = 128
OUTER = Q(1, 16384)
QUERY_INDICES = (128, 129, 255, 256, 1024, 10**6)
UPSTREAM_PINS = {
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND113_MANIFEST.name: "245857f51b8da2fb1707cdfaa9d0cb2d76f13e2d03ddb3e53e415b5cdca69ac7",
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py": "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    require(isinstance(value, dict), "top-level object")
    return value


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * Q(2) ** int(exponent)


def directed_boundary(index: int) -> tuple[Q, Q, arb]:
    value = (arb(1) / arb(index * index)).sin()
    return exact_dyadic(value.lower()), exact_dyadic(value.upper()), value


def label_code(label: str) -> int:
    if label == "H0_CENTRAL_OUTER":
        return 0
    require(label.startswith("H") and label[1:].isdigit(), "label syntax")
    index = int(label[1:])
    require(index >= N0, "label range")
    return index - 127


def cantor(left: int, right: int) -> int:
    return (left + right) * (left + right + 1) // 2 + right


def hit_cell_id(parent: str, sigma0: int, source: str, third: str, sigma3: int) -> str:
    payload = [
        parent, "HIT", sigma0, source,
        sigma3, third, cantor(label_code(source), label_code(third)),
    ]
    return "round117-operator-cell:" + digest(payload)


def bypass_cell_id(parent: str, sigma0: int, source: str, owner: str, sigma: int) -> str:
    payload = [parent, "BYPASS", sigma0, source, label_code(source), owner, sigma, "H0_CENTRAL"]
    return "round117-operator-cell:" + digest(payload)


def static_contract(document: dict[str, Any]) -> dict[str, Any]:
    require(set(document) == {"schema", "result", "result_sha256"}, "document keys")
    require(document["schema"] == SCHEMA, "schema")
    result = document["result"]
    require(document["result_sha256"] == digest(result), "result digest")
    require(result["precision_bits"] == 512, "producer precision")
    require(result["minimum_homogeneity_tail_index"] == 128, "tail index")
    require(result["local_rational_outer_cosine_coordinate"] == "1/16384", "outer coordinate")
    require(result["round113_parent_proof_box_count"] == 72, "parent count")
    require(result["hit_parent_proof_box_count"] == 8, "HIT count")
    require(result["bypass_parent_proof_box_count"] == 64, "BYPASS count")
    require(result["finite_generator_family_template_instance_count"] == 112, "family count")
    require(result["parent_rows_with_nonempty_source_central_outer_child"] == 24, "outer child count")
    require(result["bypass_actual_winner_whole_parent_cell_H0_count"] == 64, "BYPASS H0 count")
    require(result["common_refinement_rows_sha256"] == digest(result["common_refinement_rows"]), "row digest")
    require(result["boundary_ownership_ledger_sha256"] == digest(result["boundary_ownership_ledger"]), "ledger digest")
    require(result["directed_boundary_query_rows_sha256"] == digest(result["directed_boundary_query_rows"]), "query digest")
    require(result["countable_tail_paid_by_symbolic_generator_not_finite_cutoff"] is True, "symbolic tail")
    require(result["operator_cell_schema_installed"] is True, "operator schema")
    require(result["actual_parent_W_standard_curve_join_installed"] is False, "W join nonclaim")
    require(result["actual_standard_curve_child_count"] == 0, "child nonclaim")
    require(result["canonical_curve_recut_instance_count"] == 0, "recut nonclaim")
    require(result["gate5_child_field_counts"] == {f"F{i}": 0 for i in range(1, 7)}, "Gate5 fields")
    require(result["gate5_global_maturity"] == "10/18", "Gate5 maturity")
    require(result["gate5_block_count"] == 0, "Gate5 blocks")
    require(result["whole_trace_collar_installed"] is False, "collar nonclaim")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "CM2 verdict")
    require(result["upstream_pins"] == UPSTREAM_PINS, "pin map")
    require(len(result["common_refinement_rows"]) == 72, "row length")
    return result


def verify_boundaries(result: dict[str, Any]) -> None:
    rows = result["directed_boundary_query_rows"]
    require([row["index"] for row in rows] == list(QUERY_INDICES), "query indices")
    previous_lower: Q | None = None
    for row in rows:
        lower, upper, value = directed_boundary(row["index"])
        stored_lower = Q(row["directed_lower_rational"])
        stored_upper = Q(row["directed_upper_rational"])
        require(stored_lower <= lower <= upper <= stored_upper, "directed enclosure")
        require(bool(value > 0) and bool(value < aq(Q(1, row["index"] ** 2))), "sine inequality")
        if previous_lower is not None:
            require(stored_upper < previous_lower, "sample monotonicity")
        previous_lower = stored_lower
    b128_upper = Q(result["b128_directed_enclosure"]["directed_upper_rational"])
    require(Q(result["central_outer_sliver_strict_rational_lower_width"]) == OUTER - b128_upper, "outer sliver width")
    require(OUTER > b128_upper, "outer sliver positive")
    theorem = result["exact_symbolic_tail_theorem"]
    require(theorem["tail_is_symbolic_and_not_finitely_enumerated"] is True, "infinite tail")
    for test in theorem["finite_interface_test_rows"]:
        index = test["index"]
        left = Q(1, (index + 1) ** 2)
        right = Q(1, index**2)
        require(Q(test["left_angle"]) == left, "test left")
        require(Q(test["right_angle"]) == right, "test right")
        require(Q(test["interior_test_angle"]) == (left + right) / 2, "test midpoint")


def verify_rows(result: dict[str, Any], doc112: dict[str, Any], doc113: dict[str, Any]) -> tuple[int, int]:
    input_sheets = {row["sheet_id"]: row for row in doc112["result"]["sheet_rows"]}
    audited_sheets = {row["sheet_id"]: row for row in doc113["result"]["sheet_rows"]}
    parents = {
        cell["cell_id"]: (sheet, cell)
        for sheet in doc113["result"]["sheet_rows"]
        for cell in sheet["certified_cells"]
    }
    rows = result["common_refinement_rows"]
    require({row["parent_round113_cell_id"] for row in rows} == set(parents), "parent bijection")
    b128_upper = Q(result["b128_directed_enclosure"]["directed_upper_rational"])
    cores = core_cert.physical_cores()
    hit_count = 0
    bypass_count = 0
    for row in rows:
        sheet, parent = parents[row["parent_round113_cell_id"]]
        input_sheet = input_sheets[sheet["sheet_id"]]
        require(row["parent_round113_sheet_id"] == sheet["sheet_id"], "sheet join")
        require(row["sheet_kind"] == sheet["sheet_kind"], "sheet kind")
        require(row["branch_key"] == sheet["branch_key"], "branch key")
        require(row["parent_parameter_box"] == parent["parameter_box"], "parameter box")
        require(row["parent_implicit_t_root_enclosure"] == parent["implicit_t_root_enclosure"], "root enclosure")
        require(row["official_path_id_inherited"] == parent["official_path_id"], "path inheritance")
        require(row["official_word_key_ids_inherited"] == parent["official_word_key_ids"], "key inheritance")
        require(row["actual_standard_curve_child_installed"] is False, "row child nonclaim")
        require(row["gate5_F1_through_F6_installed"] is False, "row Gate5 nonclaim")
        sigma0 = input_sheet["source_grazing_sign_sigma0"]
        sigma3 = input_sheet["designated_third_transverse_sign_sigma3"]
        require(row["source_grazing_sign_sigma0"] == sigma0, "source sign")
        require(row["designated_third_grazing_sign_sigma3"] == sigma3, "third sign")
        if row["sheet_kind"] == "HIT":
            hit_count += 1
            require(parent["ordered_regular_relative_interior_owner_ids"][2] == row["actual_third_collision_owner_id"], "HIT owner")
            require(row["central_outer_source_child_nonempty"] is True, "HIT source outer")
            require(row["central_outer_actual_third_child_nonempty"] is True, "HIT third outer")
            require(len(row["generator_families"]) == 4, "HIT families")
            for family in row["generator_families"]:
                sample = family["stable_id_interface_sample"]
                require(
                    sample["operator_cell_id"] == hit_cell_id(
                        parent["cell_id"], sigma0, sample["source_label"], sample["third_label"], sigma3,
                    ),
                    "HIT stable ID",
                )
        else:
            bypass_count += 1
            coordinate = "b3"
            c00, c01 = map(Q, parent["parameter_box"]["c0"])
            z0, z1 = map(Q, parent["parameter_box"][coordinate])
            t0, t1 = map(Q, parent["implicit_t_root_enclosure"])
            source = replace(cores[row["branch_key"][0]], chart_id=input_sheet["source_chart"])
            geometry = round113.path_geometry(source, tuple(row["branch_key"]), sigma0, "BYPASS", t0, t1, c00, c01, z0, z1)
            owner = parent["ordered_regular_relative_interior_owner_ids"][2]
            winner = round113.candidate_geometry(geometry["states"][2], owner)
            require(winner.get("classification") == "STRICT_FUTURE_NEAR_ROOT", "BYPASS winner")
            radius = aq(round112.radius(owner))
            cosine = winner["radical"].value / radius
            momentum = winner["transverse"].value / radius
            require(bool(cosine > aq(b128_upper)), "BYPASS H0 margin")
            require((cosine * cosine + momentum * momentum - arb(1)).contains(0), "collision identity")
            actual_sigma = strict_sign(momentum)
            require(row["actual_third_collision_owner_id"] == owner, "BYPASS owner")
            require(row["actual_third_collision_momentum_sign_sigma_actual"] == actual_sigma, "BYPASS sign")
            require(row["actual_third_collision_H0_strict_whole_parent_cell"] is True, "BYPASS H0 flag")
            source_outer = c01 > b128_upper and max(c00, b128_upper) < c01
            require(row["central_outer_source_child_nonempty"] is source_outer, "BYPASS outer child")
            require(len(row["generator_families"]) == 1 + int(source_outer), "BYPASS families")
            for family in row["generator_families"]:
                sample = family["stable_id_interface_sample"]
                require(
                    sample["operator_cell_id"] == bypass_cell_id(
                        parent["cell_id"], sigma0, sample["source_label"], owner, actual_sigma,
                    ),
                    "BYPASS stable ID",
                )
    return hit_count, bypass_count


def verify_ledger(result: dict[str, Any], doc113: dict[str, Any]) -> None:
    ledger = result["boundary_ownership_ledger"]
    natural = ledger["natural_trace_rows"]
    require(ledger["natural_trace_rows_sha256"] == digest(natural), "natural ledger digest")
    upstream = doc113["result"]["natural_boundary_trace_rows"]
    require(len(natural) == len(upstream) == 8, "natural trace count")
    for row, source in zip(natural, upstream):
        require(row["corner_index"] == source["corner_index"], "trace corner")
        require(row["round113_trace_id"] == source["trace_id"], "trace ID")
        require(row["regular_operator_child_owns_natural_boundary"] is False, "natural boundary nonclaim")


def hostile_tests(document: dict[str, Any]) -> int:
    mutations = [
        ("operator_cell_schema_installed", False),
        ("actual_standard_curve_child_count", 1),
        ("gate5_global_maturity", "18/18"),
        ("cm2_verdict", "GO"),
        ("round113_parent_proof_box_count", 71),
        ("bypass_actual_winner_whole_parent_cell_H0_count", 63),
    ]
    rejected = 0
    for key, value in mutations:
        attack = copy.deepcopy(document)
        attack["result"][key] = value
        attack["result_sha256"] = digest(attack["result"])
        try:
            static_contract(attack)
        except RuntimeError:
            rejected += 1
    require(rejected == len(mutations), "hostile rejection")
    return rejected


def verify(precision_bits: int) -> dict[str, Any]:
    require(precision_bits >= 640, "verification precision")
    ctx.prec = precision_bits
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer pin")
    require(sha256(CERTIFICATE) == CERTIFICATE_SHA256, "certificate pin")
    for name, expected in UPSTREAM_PINS.items():
        require(sha256(HERE / name) == expected, f"upstream pin:{name}")
    document = strict_json(CERTIFICATE.read_text(encoding="utf-8"))
    result = static_contract(document)
    doc112 = strict_json(ROUND112.read_text(encoding="utf-8"))
    doc113 = strict_json(ROUND113.read_text(encoding="utf-8"))
    require(doc112["result_sha256"] == digest(doc112["result"]), "Round112 digest")
    require(doc113["result_sha256"] == digest(doc113["result"]), "Round113 digest")
    verify_boundaries(result)
    hit_count, bypass_count = verify_rows(result, doc112, doc113)
    verify_ledger(result, doc113)
    semantic_attacks = hostile_tests(document)
    strict_attacks = 0
    for text in ('{"a":1,"a":2}', '{"x":NaN}', '[]'):
        try:
            strict_json(text)
        except (RuntimeError, ValueError):
            strict_attacks += 1
    require(strict_attacks == 3, "strict JSON rejection")
    output = {
        "verdict": "PASS",
        "verification_precision_bits": precision_bits,
        "producer_module_imported": False,
        "independently_rechecked_boundary_query_count": len(QUERY_INDICES),
        "independently_rejoined_parent_region_count": hit_count + bypass_count,
        "independently_rechecked_HIT_parent_count": hit_count,
        "independently_recomputed_BYPASS_H0_parent_count": bypass_count,
        "independently_rechecked_symbolic_generator_family_count": result["finite_generator_family_template_instance_count"],
        "natural_boundary_trace_rows_rechecked": 8,
        "hostile_semantic_mutations_rejected": semantic_attacks,
        "strict_json_attacks_rejected": strict_attacks,
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
    }
    return {"schema": VERIFY_SCHEMA, "result": output, "result_sha256": digest(output)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=640)
    args = parser.parse_args()
    print(json.dumps(verify(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
