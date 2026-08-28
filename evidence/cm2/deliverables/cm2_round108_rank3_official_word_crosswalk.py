#!/usr/bin/env python3
"""Crosswalk every Round107 local rank-three germ to frozen Gate-5 words.

An official Gate-5 word describes one straight flight, not a three-collision
owner tuple.  Consequently each Round107 germ is mapped to an ordered path of
three official keys.  The certificate is deliberately fixed-s=0 and local to
the stored rational witness box.  It does not create homogeneous subbranches,
operator slots, or whole-side tube coverage.
"""
from __future__ import annotations

import argparse
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
SCHEMA = "cm2.round108.rank3-official-word-crosswalk.v1"
PRECISION_BITS = 512
ROUND107 = HERE / "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json"
ROUND107_SCHEMA = "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1"
REGISTRY_MANIFEST = HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
REGISTRY_ROWS_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"

PINS = {
    ROUND107.name: "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    REGISTRY_MANIFEST.name: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
}

ROUND107_RESULT_KEYS = {
    "F5_installation_status", "F6_installation_status", "atlas_completion_status",
    "canonical_anchor_port_count", "cell_germ_rows", "cell_germ_rows_sha256",
    "complete_18_field_operator_block_count", "complete_two_sided_face_pair_count",
    "face_pair_rows", "face_pair_rows_sha256", "global_Gate5",
    "input_corrected_face_count", "materialized_adjacent_side_germ_count",
    "materialized_complete_smooth_operator_child_count",
    "materialized_face_trace_incidence_count", "new_immutable_F5_slot_count",
    "new_immutable_F6_slot_count", "partial_topological_side_germ_skeleton_count",
    "positive_dimensional_open_smooth_cell_germ_count", "precision_bits",
    "rank3_cell_local_maturity", "rank3_face_local_maturity", "side_label_histogram",
    "strict_nonclaims", "strict_scope", "third_owner_histogram", "upstream_pins",
}

REQUIRED_GERM_KEYS = {
    "cell_germ_id", "face_id", "trace_side_label", "discriminant_side_sign",
    "cell_word_key", "ordered_collision_owner_ids", "first_owner_id",
    "second_owner_id", "third_owner_id", "source_core_index",
    "source_coordinate_witness_box", "positive_dimensional_open_smooth_cell_germ",
    "maximal_global_cell_asserted", "grazing_endpoint_included_in_closed_cell",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"non-object JSON document: {path.name}")
    return value


def validate_pins() -> None:
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"byte pin mismatch: {name}")


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    validate_pins()
    round107 = strict_load(ROUND107)
    if set(round107) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("Round107 top-level schema is not closed")
    if round107["schema"] != ROUND107_SCHEMA:
        raise RuntimeError("Round107 schema mismatch")
    if not isinstance(round107["result"], dict) or set(round107["result"]) != ROUND107_RESULT_KEYS:
        raise RuntimeError("Round107 result schema mismatch")
    if round107["result_sha256"] != digest(round107["result"]):
        raise RuntimeError("Round107 result digest mismatch")
    result = round107["result"]
    if (
        result["precision_bits"] != 512
        or result["materialized_adjacent_side_germ_count"] != 24
        or result["complete_two_sided_face_pair_count"] != 12
        or result["rank3_cell_local_maturity"] != "0/18"
        or result["new_immutable_F5_slot_count"] != 0
        or result["new_immutable_F6_slot_count"] != 0
        or result["cell_germ_rows_sha256"] != digest(result["cell_germ_rows"])
        or result["face_pair_rows_sha256"] != digest(result["face_pair_rows"])
    ):
        raise RuntimeError("Round107 semantic contract mismatch")
    if len(result["cell_germ_rows"]) != 24:
        raise RuntimeError("Round107 germ accounting mismatch")
    for row in result["cell_germ_rows"]:
        if not isinstance(row, dict) or not REQUIRED_GERM_KEYS <= set(row):
            raise RuntimeError("Round107 germ row schema mismatch")

    registry = strict_load(REGISTRY_MANIFEST)
    if set(registry) != {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"}:
        raise RuntimeError("official registry manifest schema is not closed")
    if registry["schema"] != "cm2.gate5.return-word-three-norm-frontier.manifest.v1":
        raise RuntimeError("official registry manifest schema mismatch")
    immutable = registry["result"]["immutable_candidate_key_registry"]
    if (
        immutable["candidate_return_word_key_count"] != 441280
        or immutable["candidate_word_key_rows_sha256"] != REGISTRY_ROWS_SHA256
        or immutable["domain_contract"]["word_key"]
        != "(source normal chart, retained target lift, monotone clean-wall record)"
    ):
        raise RuntimeError("official registry semantic mismatch")
    return round107, registry


def official_leg(
    leg_index: int,
    key: dict[str, Any],
    absolute_target: str,
    relative_target: str,
    crossings: list[str],
) -> dict[str, Any]:
    row = key["row"]
    if row != [row[0], relative_target, crossings, len(crossings) + 1]:
        raise RuntimeError(f"official leg {leg_index} row mismatch")
    if key["row_sha256"] != digest(row):
        raise RuntimeError(f"official leg {leg_index} row digest mismatch")
    return {
        "leg_index": leg_index,
        "source_chart_id": row[0],
        "absolute_selected_target_id": absolute_target,
        "relative_frozen_target_id": relative_target,
        "ordered_clean_wall_record": crossings,
        "roof_height": row[3],
        "ordinal_zero_based": key["ordinal_zero_based"],
        "official_word_key_id": key["word_key_id"],
        "registry_row": row,
        "registry_row_sha256": key["row_sha256"],
        "official_registry_membership": True,
        "whole_local_witness_box_regular": True,
    }


def crosswalk_row(
    germ: dict[str, Any],
    cores: tuple[Any, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    source_index = germ["source_core_index"]
    source = cores[source_index]
    box = tuple(Q(value) for value in germ["source_coordinate_witness_box"])
    if len(box) != 4 or not box[0] < box[1] or not box[2] < box[3]:
        raise RuntimeError("invalid Round107 witness box")
    atom = step1.Atom(source_index, source, *box, Q(0), Q(0), "round108")

    first = component_cert.word_key(
        source.chart_id, source.target_id, tuple(source.crossings), pair_index, pattern_index,
    )
    second, second_error = component_cert.second_word_for_atom(
        atom, germ["second_owner_id"], pair_index, pattern_index,
    )
    if second is None or second_error is not None:
        raise RuntimeError(f"second official word unresolved: {germ['cell_germ_id']}:{second_error}")
    geometry = time3_cert.classify_time3(atom, cores, pair_index, pattern_index)
    if geometry["classification"] == "UNRESOLVED_TIME3_OUTER" or geometry.get("word3") is None:
        raise RuntimeError(f"third official word unresolved: {germ['cell_germ_id']}:{geometry.get('blocker')}")
    third = geometry["word3"]

    owners = list(germ["ordered_collision_owner_ids"])
    rebuilt_owners = [
        source.target_id,
        second["absolute_selected_target_id"],
        third["absolute_selected_target_id"],
    ]
    if owners != rebuilt_owners or geometry["owner3"]["selected_target_id"] != owners[2]:
        raise RuntimeError(f"owner-chain mismatch: {germ['cell_germ_id']}")

    legs = [
        official_leg(1, first, source.target_id, source.target_id, list(source.crossings)),
        official_leg(
            2, second["key"], second["absolute_selected_target_id"],
            second["relative_frozen_target_id"], second["ordered_clean_wall_record"],
        ),
        official_leg(
            3, third["key"], third["absolute_selected_target_id"],
            third["relative_frozen_target_id"], third["ordered_clean_wall_record"],
        ),
    ]
    key_ids = [leg["official_word_key_id"] for leg in legs]
    prefix_id = "gate5-rank3-local-two-leg-prefix:" + digest(key_ids[:2])
    path_id = "gate5-rank3-local-path:" + digest({
        "cell_germ_id": germ["cell_germ_id"], "official_word_key_ids": key_ids,
    })
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
        "official_word_key_ids": key_ids,
        "official_two_leg_prefix_id": prefix_id,
        "official_path_id": path_id,
        "official_path_length": 3,
        "owner_chain_exact_match": True,
        "whole_local_witness_box_word_strict": True,
        "word_crosswalk_scope": "FIXED_S0_LOCAL_RATIONAL_WITNESS_BOX_ONLY",
    }


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 256:
        raise RuntimeError("insufficient producer precision")
    ctx.prec = precision_bits
    round107, _registry = load_inputs()
    cores = core_cert.physical_cores()
    pair_index, pattern_index, registry_sha = component_cert.key_index_tables()
    if registry_sha != REGISTRY_ROWS_SHA256:
        raise RuntimeError("official registry replay digest mismatch")

    rows = [
        crosswalk_row(germ, cores, pair_index, pattern_index)
        for germ in round107["result"]["cell_germ_rows"]
    ]
    rows.sort(key=lambda row: row["cell_germ_id"])
    if len(rows) != 24 or len({row["official_path_id"] for row in rows}) != 24:
        raise RuntimeError("path accounting mismatch")
    by_face: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_face.setdefault(row["face_id"], []).append(row)
    pair_rows: list[dict[str, Any]] = []
    for face_id, paired in sorted(by_face.items()):
        if len(paired) != 2 or {row["trace_side_label"] for row in paired} != {
            "BYPASS_SIDE", "DESIGNATED_COLLISION_SIDE",
        }:
            raise RuntimeError(f"invalid face pair: {face_id}")
        paired.sort(key=lambda row: row["trace_side_label"])
        first, second = paired
        common_prefix = first["official_word_key_ids"][:2]
        if common_prefix != second["official_word_key_ids"][:2]:
            raise RuntimeError(f"face pair lacks common two-leg prefix: {face_id}")
        if first["official_word_key_ids"][2] == second["official_word_key_ids"][2]:
            raise RuntimeError(f"face pair lacks distinct third word: {face_id}")
        if first["official_two_leg_prefix_id"] != second["official_two_leg_prefix_id"]:
            raise RuntimeError(f"face pair prefix ID mismatch: {face_id}")
        pair_rows.append({
            "face_id": face_id,
            "cell_germ_ids": [row["cell_germ_id"] for row in paired],
            "trace_side_labels": [row["trace_side_label"] for row in paired],
            "official_two_leg_prefix_id": first["official_two_leg_prefix_id"],
            "common_official_prefix_word_key_ids": common_prefix,
            "distinct_official_third_word_key_ids": [
                row["official_word_key_ids"][2] for row in paired
            ],
            "common_two_leg_prefix_verified": True,
            "distinct_third_word_verified": True,
        })

    all_keys = [key for row in rows for key in row["official_word_key_ids"]]
    roof_histogram = Counter(
        str(leg["roof_height"])
        for row in rows for leg in row["official_leg_rows"]
    )
    per_leg_roof = {
        str(index): dict(sorted(Counter(
            str(row["official_leg_rows"][index - 1]["roof_height"]) for row in rows
        ).items()))
        for index in (1, 2, 3)
    }
    if (
        len(pair_rows) != 12
        or len(all_keys) != 72
        or len(set(all_keys)) != 44
        or roof_histogram != Counter({"1": 36, "2": 36})
        or per_leg_roof != {
            "1": {"1": 16, "2": 8},
            "2": {"1": 16, "2": 8},
            "3": {"1": 4, "2": 20},
        }
    ):
        raise RuntimeError("official word accounting mismatch")

    result = {
        "producer_precision_bits": precision_bits,
        "fixed_parameter": "s=0",
        "input_local_cell_germ_count": 24,
        "official_path_crosswalk_count": 24,
        "official_leg_row_count": 72,
        "unique_official_word_key_count": 44,
        "unique_official_path_count": 24,
        "paired_face_count": 12,
        "paired_common_two_leg_prefix_count": 12,
        "paired_distinct_third_word_count": 12,
        "official_registry_candidate_key_count": 441280,
        "official_registry_rows_sha256": REGISTRY_ROWS_SHA256,
        "roof_height_histogram": dict(sorted(roof_histogram.items())),
        "per_leg_roof_height_histogram": per_leg_roof,
        "path_rows": rows,
        "path_rows_sha256": digest(rows),
        "face_pair_rows": pair_rows,
        "face_pair_rows_sha256": digest(pair_rows),
        "crosswalk_status": "CERTIFIED_FIXED_S0_LOCAL_WITNESS_PATH_CROSSWALK",
        "rank3_cell_local_maturity": "0/18",
        "new_immutable_F5_slot_count": 0,
        "new_immutable_F6_slot_count": 0,
        "complete_18_field_operator_block_count": 0,
        "global_Gate5": "NOT_CERTIFIED__10/18_BLOCKS_0",
        "strict_scope": (
            "twenty-four fixed-s=0 local rational witness boxes mapped to ordered "
            "three-leg paths in the frozen official Gate-5 word registry"
        ),
        "strict_nonclaims": [
            "an ordered three-collision owner tuple is not one official Gate-5 word",
            "no whole-face or whole-side word constancy is certified",
            "no parameter-neighbourhood guard is certified",
            "no homogeneous_subbranch_id or roof-level operator slot is materialized",
            "the collision index is not used as the official roof_level_j",
            "face-local F1-F4 fields are not inherited by these local cell germs",
            "F5 and F6 remain uninstalled",
            "the global Gate5 state is unchanged",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(canonical_json(result))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
