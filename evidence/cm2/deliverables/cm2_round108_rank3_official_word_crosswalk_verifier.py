#!/usr/bin/env python3
"""Independent 640-bit verifier for the Round108 official-word crosswalk."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component_cert
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3_cert


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round108-rank3-official-word-crosswalk-2026-07-22.json"
ROUND107 = HERE / "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json"
SCHEMA = "cm2.round108.rank3-official-word-crosswalk.v1"
VERIFY_SCHEMA = "cm2.round108.rank3-official-word-crosswalk-verification.v1"
PRECISION_BITS = 640
REGISTRY_ROWS_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
PINS = {
    ROUND107.name: "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
}

RESULT_KEYS = {
    "complete_18_field_operator_block_count", "crosswalk_status", "face_pair_rows",
    "face_pair_rows_sha256", "fixed_parameter", "global_Gate5",
    "input_local_cell_germ_count", "new_immutable_F5_slot_count",
    "new_immutable_F6_slot_count", "official_leg_row_count",
    "official_path_crosswalk_count", "official_registry_candidate_key_count",
    "official_registry_rows_sha256", "paired_common_two_leg_prefix_count",
    "paired_distinct_third_word_count", "paired_face_count", "path_rows",
    "path_rows_sha256", "per_leg_roof_height_histogram", "producer_precision_bits",
    "rank3_cell_local_maturity", "roof_height_histogram", "strict_nonclaims",
    "strict_scope", "unique_official_path_count", "unique_official_word_key_count",
    "upstream_pins",
}
PATH_KEYS = {
    "cell_germ_id", "discriminant_side_sign", "face_id", "fixed_parameter",
    "official_leg_rows", "official_path_id", "official_path_length",
    "official_two_leg_prefix_id", "official_word_key_ids", "owner_chain_exact_match",
    "provisional_cell_word_key", "provisional_ordered_collision_owner_ids",
    "source_coordinate_witness_box", "trace_side_label",
    "whole_local_witness_box_word_strict", "word_crosswalk_scope",
}
LEG_KEYS = {
    "absolute_selected_target_id", "leg_index", "official_registry_membership",
    "official_word_key_id", "ordered_clean_wall_record", "ordinal_zero_based",
    "registry_row", "registry_row_sha256", "relative_frozen_target_id",
    "roof_height", "source_chart_id", "whole_local_witness_box_regular",
}
PAIR_KEYS = {
    "cell_germ_ids", "common_official_prefix_word_key_ids",
    "common_two_leg_prefix_verified", "distinct_official_third_word_key_ids",
    "distinct_third_word_verified", "face_id", "official_two_leg_prefix_id",
    "trace_side_labels",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate key: {key}")
        output[key] = value
    return output


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite number: {token}")


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise ValueError("document is not an object")
    return value


def make_leg(index: int, key: dict[str, Any], absolute: str, relative: str, walls: list[str]) -> dict[str, Any]:
    row = key["row"]
    if row != [row[0], relative, walls, len(walls) + 1]:
        raise ValueError("official registry row mismatch")
    if key["row_sha256"] != digest(row):
        raise ValueError("official registry row digest mismatch")
    return {
        "leg_index": index,
        "source_chart_id": row[0],
        "absolute_selected_target_id": absolute,
        "relative_frozen_target_id": relative,
        "ordered_clean_wall_record": walls,
        "roof_height": row[3],
        "ordinal_zero_based": key["ordinal_zero_based"],
        "official_word_key_id": key["word_key_id"],
        "registry_row": row,
        "registry_row_sha256": key["row_sha256"],
        "official_registry_membership": True,
        "whole_local_witness_box_regular": True,
    }


def rebuild_path(germ: dict[str, Any], cores: tuple[Any, ...], pair_index: dict[Any, int], pattern_index: dict[Any, int]) -> dict[str, Any]:
    source = cores[germ["source_core_index"]]
    q0, q1, p0, p1 = (Q(value) for value in germ["source_coordinate_witness_box"])
    atom = step1.Atom(germ["source_core_index"], source, q0, q1, p0, p1, Q(0), Q(0), "round108-verify")
    first = component_cert.word_key(
        source.chart_id, source.target_id, tuple(source.crossings), pair_index, pattern_index,
    )
    second, error = component_cert.second_word_for_atom(
        atom, germ["second_owner_id"], pair_index, pattern_index,
    )
    if second is None or error is not None:
        raise ValueError(f"second word unresolved: {error}")
    event = time3_cert.classify_time3(atom, cores, pair_index, pattern_index)
    if event["classification"] == "UNRESOLVED_TIME3_OUTER" or event.get("word3") is None:
        raise ValueError(f"third word unresolved: {event.get('blocker')}")
    third = event["word3"]
    owners = list(germ["ordered_collision_owner_ids"])
    rebuilt = [source.target_id, second["absolute_selected_target_id"], third["absolute_selected_target_id"]]
    if owners != rebuilt or event["owner3"]["selected_target_id"] != owners[2]:
        raise ValueError("owner chain mismatch")
    legs = [
        make_leg(1, first, source.target_id, source.target_id, list(source.crossings)),
        make_leg(2, second["key"], second["absolute_selected_target_id"], second["relative_frozen_target_id"], second["ordered_clean_wall_record"]),
        make_leg(3, third["key"], third["absolute_selected_target_id"], third["relative_frozen_target_id"], third["ordered_clean_wall_record"]),
    ]
    keys = [leg["official_word_key_id"] for leg in legs]
    return {
        "cell_germ_id": germ["cell_germ_id"],
        "face_id": germ["face_id"],
        "trace_side_label": germ["trace_side_label"],
        "discriminant_side_sign": germ["discriminant_side_sign"],
        "fixed_parameter": "s=0",
        "source_coordinate_witness_box": germ["source_coordinate_witness_box"],
        "provisional_cell_word_key": germ["cell_word_key"],
        "provisional_ordered_collision_owner_ids": owners,
        "official_leg_rows": legs,
        "official_word_key_ids": keys,
        "official_two_leg_prefix_id": "gate5-rank3-local-two-leg-prefix:" + digest(keys[:2]),
        "official_path_id": "gate5-rank3-local-path:" + digest({"cell_germ_id": germ["cell_germ_id"], "official_word_key_ids": keys}),
        "official_path_length": 3,
        "owner_chain_exact_match": True,
        "whole_local_witness_box_word_strict": True,
        "word_crosswalk_scope": "FIXED_S0_LOCAL_RATIONAL_WITNESS_BOX_ONLY",
    }


def rebuild_pairs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["face_id"], []).append(row)
    output = []
    for face_id, pair in sorted(grouped.items()):
        pair.sort(key=lambda row: row["trace_side_label"])
        if len(pair) != 2 or [row["trace_side_label"] for row in pair] != ["BYPASS_SIDE", "DESIGNATED_COLLISION_SIDE"]:
            raise ValueError("face pair mismatch")
        prefix = pair[0]["official_word_key_ids"][:2]
        if prefix != pair[1]["official_word_key_ids"][:2] or pair[0]["official_word_key_ids"][2] == pair[1]["official_word_key_ids"][2]:
            raise ValueError("face path split mismatch")
        output.append({
            "face_id": face_id,
            "cell_germ_ids": [row["cell_germ_id"] for row in pair],
            "trace_side_labels": [row["trace_side_label"] for row in pair],
            "official_two_leg_prefix_id": pair[0]["official_two_leg_prefix_id"],
            "common_official_prefix_word_key_ids": prefix,
            "distinct_official_third_word_key_ids": [row["official_word_key_ids"][2] for row in pair],
            "common_two_leg_prefix_verified": True,
            "distinct_third_word_verified": True,
        })
    return output


def validate(document: dict[str, Any], geometry: bool = True) -> str:
    if set(document) != {"schema", "result", "result_sha256"} or document.get("schema") != SCHEMA:
        raise ValueError("closed top-level schema mismatch")
    result = document["result"]
    if not isinstance(result, dict) or set(result) != RESULT_KEYS or digest(result) != document["result_sha256"]:
        raise ValueError("closed result schema or digest mismatch")
    rows, pairs = result["path_rows"], result["face_pair_rows"]
    if digest(rows) != result["path_rows_sha256"] or digest(pairs) != result["face_pair_rows_sha256"]:
        raise ValueError("nested digest mismatch")
    if any(set(row) != PATH_KEYS for row in rows) or any(set(leg) != LEG_KEYS for row in rows for leg in row["official_leg_rows"]):
        raise ValueError("closed path schema mismatch")
    if any(set(pair) != PAIR_KEYS for pair in pairs):
        raise ValueError("closed pair schema mismatch")
    if result["upstream_pins"] != PINS or result["official_registry_rows_sha256"] != REGISTRY_ROWS_SHA256:
        raise ValueError("pin ledger mismatch")
    expected_counts = (
        len(rows), sum(len(row["official_leg_rows"]) for row in rows), len(pairs),
        len({key for row in rows for key in row["official_word_key_ids"]}),
        len({row["official_path_id"] for row in rows}),
    )
    if expected_counts != (24, 72, 12, 44, 24):
        raise ValueError("crosswalk accounting mismatch")
    if (
        result["rank3_cell_local_maturity"] != "0/18"
        or result["new_immutable_F5_slot_count"] != 0
        or result["new_immutable_F6_slot_count"] != 0
        or result["complete_18_field_operator_block_count"] != 0
        or result["global_Gate5"] != "NOT_CERTIFIED__10/18_BLOCKS_0"
    ):
        raise ValueError("illegal field or gate promotion")
    if not geometry:
        return digest(rows)
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"byte pin mismatch: {name}")
    round107 = strict_load(ROUND107)
    if round107["result_sha256"] != digest(round107["result"]):
        raise ValueError("Round107 digest mismatch")
    ctx.prec = PRECISION_BITS
    cores = tuple(core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = component_cert.key_index_tables()
    if registry_sha != REGISTRY_ROWS_SHA256:
        raise ValueError("registry replay digest mismatch")
    rebuilt = sorted(
        (rebuild_path(germ, cores, pair_index, pattern_index) for germ in round107["result"]["cell_germ_rows"]),
        key=lambda row: row["cell_germ_id"],
    )
    rebuilt_pairs = rebuild_pairs(rebuilt)
    if rebuilt != rows or rebuilt_pairs != pairs:
        raise ValueError("independent 640-bit reconstruction mismatch")
    roofs = Counter(str(leg["roof_height"]) for row in rows for leg in row["official_leg_rows"])
    if roofs != Counter({"1": 36, "2": 36}):
        raise ValueError("roof histogram mismatch")
    return digest(rebuilt)


def mutation_rejections(document: dict[str, Any]) -> int:
    mutations = []
    wrong_leg = copy.deepcopy(document)
    wrong_leg["result"]["path_rows"][0]["official_word_key_ids"][2] = wrong_leg["result"]["path_rows"][1]["official_word_key_ids"][2]
    mutations.append(wrong_leg)
    promoted = copy.deepcopy(document)
    promoted["result"]["rank3_cell_local_maturity"] = "1/18"
    mutations.append(promoted)
    installed = copy.deepcopy(document)
    installed["result"]["new_immutable_F5_slot_count"] = 1
    mutations.append(installed)
    same_third = copy.deepcopy(document)
    same_third["result"]["face_pair_rows"][0]["distinct_official_third_word_key_ids"][1] = same_third["result"]["face_pair_rows"][0]["distinct_official_third_word_key_ids"][0]
    mutations.append(same_third)
    bad_owner = copy.deepcopy(document)
    bad_owner["result"]["path_rows"][0]["provisional_ordered_collision_owner_ids"][2] = "G[999,999]"
    mutations.append(bad_owner)
    bad_registry = copy.deepcopy(document)
    bad_registry["result"]["path_rows"][0]["official_leg_rows"][0]["official_registry_membership"] = False
    mutations.append(bad_registry)
    rejected = 0
    for mutation in mutations:
        mutation["result"]["path_rows_sha256"] = digest(mutation["result"]["path_rows"])
        mutation["result"]["face_pair_rows_sha256"] = digest(mutation["result"]["face_pair_rows"])
        mutation["result_sha256"] = digest(mutation["result"])
        try:
            validate(mutation, geometry=True)
        except (ValueError, RuntimeError):
            rejected += 1
    return rejected


def json_attack_rejections() -> int:
    raw = CERTIFICATE.read_text(encoding="utf-8").rstrip()
    attacks = [
        raw[:-1] + ',"schema":"duplicate"}',
        raw.replace('"producer_precision_bits": 512', '"producer_precision_bits": NaN', 1),
        raw[:-1] + ',"unknown":0}',
    ]
    rejected = 0
    for attack in attacks:
        try:
            value = json.loads(attack, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
            validate(value, geometry=False)
        except (ValueError, RuntimeError):
            rejected += 1
    return rejected


def main() -> int:
    document = strict_load(CERTIFICATE)
    projection = validate(document, geometry=True)
    semantic = mutation_rejections(document)
    json_attacks = json_attack_rejections()
    if semantic != 6 or json_attacks != 3:
        raise RuntimeError("attack rejection accounting mismatch")
    result = {
        "verification_precision_bits": PRECISION_BITS,
        "producer_module_imported": False,
        "independent_path_reconstruction_count": 24,
        "independent_leg_reconstruction_count": 72,
        "independent_face_pair_reconstruction_count": 12,
        "unique_official_word_key_count": 44,
        "semantic_projection_sha256": projection,
        "hostile_semantic_mutations_rejected": "6/6",
        "strict_json_attacks_rejected": "3/3",
        "gate_promotion_detected": False,
        "verdict": "VERIFIED_FIXED_S0_LOCAL_OFFICIAL_PATH_CROSSWALK",
    }
    output = {"schema": VERIFY_SCHEMA, "result": result, "result_sha256": digest(result)}
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
