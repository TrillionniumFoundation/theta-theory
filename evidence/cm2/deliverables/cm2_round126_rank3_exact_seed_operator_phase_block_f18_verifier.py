#!/usr/bin/env python3
"""Independent verifier for the Round126 exact-seed F18 certificate.

This verifier does not import or execute the Round126 producer.  It
strict-parses byte-pinned Round121, Round122 and Round125 certificates as
data, independently rebuilds the 120 complete F1--F17 same-key maps and the
120 direct-standard-N F18 registrations, and then checks the chained
2160-slot registry.  Mutation tests re-sign affected rows, aggregate
digests, and the outer document before verification.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-2026-07-23.json"
)
OUTPUT = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-verification-2026-07-23.json"
)
ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)
ROUND125 = (
    HERE
    / "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json"
)
ROUND125_VERIFICATION = (
    HERE
    / "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-verification-2026-07-23.json"
)
ROUND126_PRODUCER = (
    HERE / "cm2_round126_rank3_exact_seed_operator_phase_block_f18.py"
)

CERTIFICATE_SCHEMA = (
    "cm2.round126.rank3-exact-seed-operator-phase-block-f18.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round126.rank3-exact-seed-operator-phase-block-f18-verification.v1"
)
ROUND126_PRODUCER_SHA256 = (
    "db5a3a4250e26bdeeb6ac4a2a6abade5014073b5901339e30d5c4b4907fcba68"
)
ROUND121_RESULT_SHA256 = (
    "962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8"
)
ROUND122_RESULT_SHA256 = (
    "e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb"
)
ROUND125_RESULT_SHA256 = (
    "b75c0574aa337c7ea5f9659e04980d0e415c30a2dd1a2b81b3774ed0577053ba"
)

UPSTREAM_PINS = {
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py":
        "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json":
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge.py":
        "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json":
        "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    "deliverables/cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17.py":
        "e360c511c87f10483ee19cf566d9542f123a2fbdf37585d9954a9c33575b940b",
    "deliverables/cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json":
        "cecae7d1b864abcb62215c317bb87bbf392848c70b6affca253d350a9f687579",
    "deliverables/cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17_verifier.py":
        "15f5313fc9f9593a0e1d41b95a9c09f7cc204f3471e177c17b1355b9a3f13737",
    "deliverables/cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-verification-2026-07-23.json":
        "919c50840eee75bcebb7ed8d870f2300d6a47466055bd4d25d95645dbbc6bd62",
}

PRODUCER_INPUT_PINS = {
    key: value
    for key, value in UPSTREAM_PINS.items()
    if "verifier" not in key and "verification" not in key
}

FIELD_NAMES = {
    1: "nonempty_or_empty_domain_proof",
    2: "physical_homogeneity_subbranch_table",
    3: "homogeneous_prefix_chart",
    4: "homogeneous_suffix_chart",
    5: "inverse_Jacobian_bound",
    6: "log_Jacobian_distortion_sum",
    7: "one_step_cut_growth_Z_sum",
    8: "face_transversality_lower",
    9: "face_C2_atlas_bound",
    10: "coarea_density_regular_bound",
    11: "dynamic_Holder_test_pullback_bound",
    12: "C1_face_trace_pullback_bound",
    13: "moving_boundary_DQ_current_and_two_traces",
    14: "regular_density_operator_cost",
    15: "standard_family_operator_cost",
    16: "flux_face_operator_cost",
    17: "dynamic_test_operator_cost",
    18: "operator_phase_block",
}
SOURCE_ROUND_BY_FIELD = {
    **{field: 121 for field in range(1, 7)},
    **{field: 122 for field in list(range(7, 14)) + [16]},
    14: 125,
    15: 125,
    17: 125,
}
STAGE_RETURN_LENGTH = {0: 2, 1: 1, 2: 2}
ROOF_LEVELS_BY_STAGE = {0: [0, 1], 1: [0], 2: [0, 1]}
STAGE_RECUT_KEY = {
    0: "source_recut_instance_id",
    1: "first_image_recut_instance_id",
    2: "second_image_recut_instance_id",
}
EXPECTED_STAGE_LEVEL_COUNTS = {0: 48, 1: 24, 2: 48}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_float(_value: str) -> Any:
    raise VerificationError("JSON floating-point numbers are forbidden")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_surrogates(value: Any) -> None:
    if type(value) is str:
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            "unpaired surrogate",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key)
            reject_surrogates(item)


def parse_strict_bytes(raw: bytes) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM")
    value = json.loads(
        raw.decode("utf-8", errors="strict"),
        object_pairs_hook=strict_pairs,
        parse_float=reject_float,
        parse_constant=reject_float,
    )
    reject_surrogates(value)
    return value


def strict_document(path: Path, schema: str) -> dict[str, Any]:
    document = parse_strict_bytes(path.read_bytes())
    require(type(document) is dict, f"top object:{path.name}")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == schema, f"schema:{path.name}")
    require(type(document["result"]) is dict, f"result:{path.name}")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"result digest:{path.name}",
    )
    return document


def validate_row(row: Any, label: str) -> None:
    require(type(row) is dict, f"{label} type")
    if "row_sha256" in row:
        require(type(row["row_sha256"]) is str, f"{label} hash type")
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        require(row["row_sha256"] == digest(payload), f"{label} hash")


def verify_pins() -> None:
    require(
        ROUND126_PRODUCER.is_file() and not ROUND126_PRODUCER.is_symlink(),
        "Round126 producer file",
    )
    require(
        sha256(ROUND126_PRODUCER) == ROUND126_PRODUCER_SHA256,
        "Round126 producer byte pin",
    )
    for relative, expected in UPSTREAM_PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")


def coordinate(row: dict[str, Any]) -> tuple[str, str, int]:
    word = row.get("official_word_key_id")
    subbranch = row.get("refined_homogeneous_subbranch_id")
    roof = row.get("roof_level_j")
    require(type(word) is str and type(subbranch) is str, "coordinate strings")
    require(type(roof) is int, "coordinate roof integer")
    return word, subbranch, roof


def map_row_id(base_key: tuple[str, str, int]) -> str:
    return "round126-preexisting-f1-f17-map:" + digest(
        ["round126-preexisting-f1-f17-map-v1", list(base_key)]
    )


def f18_slot_id(immutable_key: list[Any]) -> str:
    return "round126-gate5-f18-slot:" + digest(
        ["round126-gate5-f18-slot-v1", immutable_key]
    )


def load_upstream() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    verify_pins()
    d121 = strict_document(
        ROUND121,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )
    d122 = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )
    d125 = strict_document(
        ROUND125,
        "cm2.round125.rank3-exact-seed-graph-current-dynamic-test-f17.v2",
    )
    d125v = strict_document(
        ROUND125_VERIFICATION,
        "cm2.round125.rank3-exact-seed-graph-current-dynamic-test-f17-verification.v1",
    )
    require(d121["result_sha256"] == ROUND121_RESULT_SHA256, "Round121 result pin")
    require(d122["result_sha256"] == ROUND122_RESULT_SHA256, "Round122 result pin")
    require(d125["result_sha256"] == ROUND125_RESULT_SHA256, "Round125 result pin")
    require(d125v["result"]["status"] == "PASS", "Round125 verification PASS")
    require(
        d125v["result"]["certificate_sha256"]
        == PRODUCER_INPUT_PINS[
            "deliverables/cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json"
        ],
        "Round125 verification certificate crosslink",
    )
    r125 = d125["result"]
    require(
        r125["rank3_seed_child_field_maturity"] == "17/18"
        and r125["remaining_uninstalled_child_fields"] == ["F18"]
        and r125["count_ledger"]["combined_child_local_slot_count"] == 2040,
        "Round125 local frontier",
    )
    require(
        r125["gate5_global_maturity"] == "10/18"
        and r125["complete_18_field_block_count"] == 0
        and r125["gate5_block_count"] == 0
        and r125["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round125 global safety",
    )
    return d121["result"], d122["result"], r125, d125v["result"]


def source_rows_by_coordinate(
    r121: dict[str, Any],
    r122: dict[str, Any],
    r125: dict[str, Any],
) -> dict[tuple[str, str, int], dict[int, dict[str, Any]]]:
    sources = (
        (121, r121["gate5_F1_F6_slot_rows"]),
        (122, r122["gate5_F7_F13_F16_slot_rows"]),
        (125, r125["gate5_F14_slot_rows"]),
        (125, r125["gate5_F15_slot_rows"]),
        (125, r125["gate5_F17_slot_rows"]),
    )
    by_coordinate: dict[
        tuple[str, str, int], dict[int, dict[str, Any]]
    ] = {}
    slot_ids: set[str] = set()
    immutable_keys: set[str] = set()
    field_count: Counter[int] = Counter()
    for source_round, rows in sources:
        require(type(rows) is list, f"Round{source_round} source rows")
        for row in rows:
            validate_row(row, f"Round{source_round} source slot")
            field = row.get("field_index")
            require(type(field) is int and 1 <= field <= 17, "source field")
            require(
                SOURCE_ROUND_BY_FIELD[field] == source_round,
                "source round by field",
            )
            require(row.get("field_name") == FIELD_NAMES[field], "source field name")
            base_key = coordinate(row)
            require(
                row.get("immutable_slot_key")
                == [*base_key, FIELD_NAMES[field]],
                "source immutable key",
            )
            slot_id = row.get("slot_id")
            require(type(slot_id) is str and slot_id not in slot_ids, "source slot ID")
            slot_ids.add(slot_id)
            immutable = canonical(row["immutable_slot_key"])
            require(immutable not in immutable_keys, "source immutable uniqueness")
            immutable_keys.add(immutable)
            bucket = by_coordinate.setdefault(base_key, {})
            require(field not in bucket, "one source field per base key")
            bucket[field] = row
            field_count[field] += 1
    require(len(slot_ids) == len(immutable_keys) == 2040, "2040 source slots")
    require(
        field_count == Counter({field: 120 for field in range(1, 18)}),
        "17 by 120 source census",
    )
    require(
        len(by_coordinate) == 120
        and all(set(rows) == set(range(1, 18)) for rows in by_coordinate.values()),
        "120 complete F1-F17 maps",
    )
    return by_coordinate


def rebuild_map_rows(
    r121: dict[str, Any],
    r122: dict[str, Any],
    r125: dict[str, Any],
) -> list[dict[str, Any]]:
    source_map = source_rows_by_coordinate(r121, r122, r125)
    child_rows: dict[str, dict[str, Any]] = {}
    child_ranks: set[int] = set()
    for child in r121["common_refinement_rows"]:
        validate_row(child, "Round121 child")
        child_id = child.get("common_child_id")
        rank = child.get("common_rank")
        require(type(child_id) is str and type(rank) is int, "child identity")
        require(child_id not in child_rows and rank not in child_ranks, "child unique")
        child_rows[child_id] = child
        child_ranks.add(rank)
    require(child_ranks == set(range(24)), "child ranks")

    incidences: dict[str, dict[str, Any]] = {}
    for incidence in r122["child_face_incidence_rows"]:
        validate_row(incidence, "Round122 incidence")
        child_id = incidence.get("common_child_id")
        require(
            type(child_id) is str and child_id not in incidences,
            "incidence child unique",
        )
        incidences[child_id] = incidence
    require(set(incidences) == set(child_rows), "incidence child coverage")

    operators: dict[tuple[str, int], dict[str, Any]] = {}
    for operator in r125["standard_family_leg_operator_rows"]:
        validate_row(operator, "Round125 operator")
        child_id = operator.get("common_child_id")
        stage = operator.get("stage")
        require(
            type(child_id) is str
            and type(stage) is int
            and stage in STAGE_RETURN_LENGTH,
            "operator key",
        )
        key = (child_id, stage)
        require(key not in operators, "operator key unique")
        operators[key] = operator
    require(
        set(operators)
        == {(child, stage) for child in child_rows for stage in range(3)},
        "72 operator carriers",
    )

    ordered_coordinates = sorted(
        source_map,
        key=lambda key: (
            child_rows[source_map[key][1]["common_child_id"]]["common_rank"],
            source_map[key][1]["stage"],
            key[2],
        ),
    )
    rows: list[dict[str, Any]] = []
    child_levels: Counter[str] = Counter()
    child_stage_levels: Counter[tuple[str, int]] = Counter()
    stage_levels: Counter[int] = Counter()
    for base_key in ordered_coordinates:
        source = source_map[base_key]
        first = source[1]
        child_id = first["common_child_id"]
        stage = first["stage"]
        require(type(stage) is int and stage in STAGE_RETURN_LENGTH, "map stage")
        child = child_rows[child_id]
        rank = child["common_rank"]
        input_recut = child[STAGE_RECUT_KEY[stage]]
        require(type(input_recut) is str, "map input recut")
        operator = operators[(child_id, stage)]
        require(
            operator["official_word_key_id"] == base_key[0]
            and operator["refined_homogeneous_subbranch_id"] == base_key[1]
            and operator["common_rank"] == rank,
            "operator coordinate",
        )
        require(
            operator["input_materialized_recut_instance_id"] == input_recut,
            "operator recut",
        )
        require(
            operator["roof_level_count"] == STAGE_RETURN_LENGTH[stage]
            and operator["roof_level_js"] == ROOF_LEVELS_BY_STAGE[stage]
            and base_key[2] in operator["roof_level_js"],
            "operator roofs",
        )
        require(
            operator["transparent_wall_roof_split_adds_no_family_operator_factor"]
            is True,
            "operator roof split adds no family factor",
        )
        for field, source_row in source.items():
            require(
                source_row["common_child_id"] == child_id
                and source_row["stage"] == stage,
                "source same child stage",
            )
            if field <= 6:
                require(
                    source_row["materialized_input_recut_instance_id"]
                    == input_recut,
                    "F1-F6 recut",
                )
            if field in (14, 15):
                require(
                    source_row["input_materialized_recut_instance_id"]
                    == input_recut,
                    "F14-F15 recut",
                )
            if field in list(range(7, 14)) + [16]:
                require(
                    source_row["child_face_incidence_row_sha256"]
                    == incidences[child_id]["row_sha256"],
                    "F7-F13/F16 incidence",
                )
        require(
            source[14]["round122_same_key_F10_slot_id"] == source[10]["slot_id"]
            and source[14]["round122_same_key_F13_slot_id"]
            == source[13]["slot_id"]
            and source[14]["round122_same_key_F16_slot_id"]
            == source[16]["slot_id"],
            "F14 same-key links",
        )
        require(
            source[15]["round122_same_key_F7_slot_id"] == source[7]["slot_id"]
            and source[15]["round123_same_key_F14_slot_id"]
            == source[14]["slot_id"]
            and source[15]["standard_family_leg_operator_row_id"]
            == operator["standard_family_leg_operator_row_id"],
            "F15 same-key links",
        )
        require(
            source[17]["round122_same_key_F11_slot_id"] == source[11]["slot_id"]
            and source[17]["round124_same_key_F15_slot_id"]
            == source[15]["slot_id"],
            "F17 same-key links",
        )
        bindings = [
            {
                "field_index": field,
                "field_name": FIELD_NAMES[field],
                "slot_id": source[field]["slot_id"],
                "source_certificate_round": SOURCE_ROUND_BY_FIELD[field],
                "source_slot_canonical_sha256": digest(source[field]),
            }
            for field in range(1, 18)
        ]
        row = {
            "same_key_map_row_id": map_row_id(base_key),
            "immutable_base_key": list(base_key),
            "official_word_key_id": base_key[0],
            "refined_homogeneous_subbranch_id": base_key[1],
            "roof_level_j": base_key[2],
            "common_child_id": child_id,
            "common_rank": rank,
            "stage": stage,
            "input_materialized_recut_instance_id": input_recut,
            "standard_family_leg_operator_row_id":
                operator["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256": operator["row_sha256"],
            "bound_preexisting_field_indices": list(range(1, 18)),
            "bound_preexisting_field_count": 17,
            "bound_preexisting_F1_F17_slots": bindings,
            "bound_preexisting_F1_F17_slots_sha256": digest(bindings),
            "each_preexisting_field_bound_exactly_once": True,
            "all_preexisting_fields_share_child_stage_input_and_operator_carrier":
                True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
        child_levels[child_id] += 1
        child_stage_levels[(child_id, stage)] += 1
        stage_levels[stage] += 1
    require(len(rows) == 120, "120 rebuilt maps")
    require(
        len({row["same_key_map_row_id"] for row in rows}) == 120,
        "map ID uniqueness",
    )
    require(
        child_levels == Counter({child: 5 for child in child_rows}),
        "five levels per child",
    )
    require(
        child_stage_levels
        == Counter(
            {
                (child, stage): STAGE_RETURN_LENGTH[stage]
                for child in child_rows
                for stage in sorted(STAGE_RETURN_LENGTH)
            }
        ),
        "per-child stage level census 2/1/2",
    )
    require(
        stage_levels == Counter(EXPECTED_STAGE_LEVEL_COUNTS),
        "map stage census",
    )
    return rows


def rebuild_f18_rows(map_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered_stages = sorted(STAGE_RETURN_LENGTH)
    child_stage_block_exponents = [
        STAGE_RETURN_LENGTH[stage] for stage in ordered_stages
    ]
    child_path_exponent = sum(child_stage_block_exponents)
    rows: list[dict[str, Any]] = []
    for map_row in map_rows:
        stage = map_row["stage"]
        roof = map_row["roof_level_j"]
        return_length = STAGE_RETURN_LENGTH[stage]
        suffix_length = return_length - roof
        require(0 <= roof < return_length and suffix_length > 0, "phase range")
        immutable_key = [
            map_row["official_word_key_id"],
            map_row["refined_homogeneous_subbranch_id"],
            roof,
            FIELD_NAMES[18],
        ]
        row = {
            "slot_id": f18_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": map_row["official_word_key_id"],
            "refined_homogeneous_subbranch_id":
                map_row["refined_homogeneous_subbranch_id"],
            "roof_level_j": roof,
            "field_index": 18,
            "field_name": FIELD_NAMES[18],
            "field_bound_semantics": "STRUCTURAL_REGISTRATION",
            "field_value_or_contract": (
                f"direct_standard_N:z^{roof}*z^{suffix_length}"
                f"=z^{return_length}"
            ),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": map_row["common_child_id"],
            "common_rank": map_row["common_rank"],
            "stage": stage,
            "input_materialized_recut_instance_id":
                map_row["input_materialized_recut_instance_id"],
            "standard_family_leg_operator_row_id":
                map_row["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256":
                map_row["standard_family_leg_operator_row_sha256"],
            "preexisting_F1_F17_same_key_map_row_id":
                map_row["same_key_map_row_id"],
            "preexisting_F1_F17_same_key_map_row_sha256":
                map_row["row_sha256"],
            "bound_preexisting_field_count": 17,
            "phase_route": "direct_standard_N",
            "stage_return_length_r": return_length,
            "prefix_length_j": roof,
            "suffix_length_r_minus_j": suffix_length,
            "prefix_operator_monomial": f"z^{roof}",
            "suffix_operator_monomial": f"z^{suffix_length}",
            "stage_block_operator_monomial": f"z^{return_length}",
            "prefix_suffix_block_identity":
                f"z^{roof}*z^{suffix_length}=z^{return_length}",
            "child_stage_block_exponents": child_stage_block_exponents,
            "child_path_exponent": child_path_exponent,
            "child_path_operator_monomial": f"z^{child_path_exponent}",
            "child_path_uses_one_block_per_stage_not_one_per_roof_split": True,
            "seed_local_18_field_level_block_status":
                "COMPLETE_ON_THIS_EXACT_SEED_LEVEL",
            "structural_registration_only": True,
            "operator_Wiener_invertibility_claimed": False,
            "operator_Wiener_aperiodicity_claimed": False,
            "Kac_closure_claimed": False,
            "global_operator_phase_block_claimed": False,
            "CM2_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 120, "120 rebuilt F18 rows")
    require(len({row["slot_id"] for row in rows}) == 120, "F18 ID uniqueness")
    require(
        Counter(row["stage"] for row in rows)
        == Counter(EXPECTED_STAGE_LEVEL_COUNTS),
        "F18 stage census",
    )
    rows_by_child: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        rows_by_child.setdefault(row["common_child_id"], []).append(row)
    require(len(rows_by_child) == 24, "F18 child census")
    for child_id, child_rows in rows_by_child.items():
        require(len(child_rows) == 5, f"five F18 levels:{child_id}")
        stage_roofs = {
            stage: sorted(
                row["roof_level_j"]
                for row in child_rows
                if row["stage"] == stage
            )
            for stage in ordered_stages
        }
        require(
            stage_roofs == ROOF_LEVELS_BY_STAGE,
            f"per-child F18 roof census:{child_id}",
        )
        require(
            all(
                row["child_stage_block_exponents"]
                == child_stage_block_exponents
                and row["child_path_exponent"] == child_path_exponent
                and row["child_path_operator_monomial"]
                == f"z^{child_path_exponent}"
                for row in child_rows
            ),
            f"derived child phase identity:{child_id}",
        )
    return rows


def phase_registration_contract() -> dict[str, Any]:
    ordered_stages = sorted(STAGE_RETURN_LENGTH)
    stage_exponents = [STAGE_RETURN_LENGTH[stage] for stage in ordered_stages]
    child_exponent = sum(stage_exponents)
    return {
        "status": (
            "CERTIFIED_FINITE_EXACT_SEED_DIRECT_STANDARD_N"
            "_STRUCTURAL_PHASE_REGISTRATION"
        ),
        "route": "direct_standard_N",
        "registration_scope": "STRUCTURAL_ONLY",
        "stage_return_length_by_stage": {
            str(stage): STAGE_RETURN_LENGTH[stage] for stage in ordered_stages
        },
        "roof_level_js_by_stage": {
            str(stage): ROOF_LEVELS_BY_STAGE[stage] for stage in ordered_stages
        },
        "prefix_rule": "prefix exponent is j",
        "suffix_rule": "suffix exponent is r-j",
        "stage_block_rule": "z^j*z^(r-j)=z^r",
        "child_stage_block_exponents": stage_exponents,
        "child_path_rule": (
            "*".join(f"z^{exponent}" for exponent in stage_exponents)
            + f"=z^{child_exponent}"
        ),
        "child_path_exponent": child_exponent,
        "roof_levels_are_symbolic_prefix_suffix_factorizations": True,
        "one_stage_block_per_stage_in_child_path": True,
        "symbolic_roof_level_factorization_count": 120,
        "seed_local_complete_18_field_level_block_count": 120,
        "seed_local_complete_18_field_child_packet_count": 24,
        "operator_Wiener_theorem": "NOT_CLAIMED",
        "operator_Wiener_aperiodicity": "NOT_CLAIMED",
        "Kac_return_wide_closure": "NOT_CLAIMED",
        "global_operator_phase_registration": "NOT_CLAIMED",
        "global_Gate5_upgrade": "NOT_CLAIMED",
        "CM2": "NOT_CLAIMED",
    }


def expected_result(
    r121: dict[str, Any],
    r122: dict[str, Any],
    r125: dict[str, Any],
) -> dict[str, Any]:
    map_rows = rebuild_map_rows(r121, r122, r125)
    f18_rows = rebuild_f18_rows(map_rows)
    preexisting_ids = [
        binding["slot_id"]
        for map_row in map_rows
        for binding in map_row["bound_preexisting_F1_F17_slots"]
    ]
    new_ids = [row["slot_id"] for row in f18_rows]
    require(
        len(preexisting_ids) == len(set(preexisting_ids)) == 2040,
        "expected preexisting ID census",
    )
    require(
        len(new_ids) == len(set(new_ids)) == 120
        and set(preexisting_ids).isdisjoint(new_ids),
        "expected F18 ID separation",
    )
    prior_registry = r125[
        "combined_installed_child_local_slot_registry_after_F17"
    ]
    require(
        prior_registry["combined_slot_count"] == 2040
        and prior_registry["certified_field_indices"] == list(range(1, 18))
        and prior_registry["uninstalled_field_indices"] == [18],
        "Round125 registry frontier",
    )
    gate_status = dict(r125["gate5_actual_child_field_status"])
    gate_status["F18"] = "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    require(
        set(gate_status) == {f"F{field}" for field in range(1, 19)}
        and all(
            type(value) is str
            and value.startswith("CERTIFIED_ON_ALL_24_")
            for value in gate_status.values()
        ),
        "18 local field statuses",
    )
    count_ledger = dict(r125["count_ledger"])
    count_ledger.update(
        {
            "preexisting_F1_F17_same_key_map_row_count": 120,
            "new_F18_slot_count": 120,
            "inherited_Round125_slot_count": 2040,
            "combined_child_local_slot_count": 2160,
            "certified_child_local_field_count": 18,
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
        }
    )
    return {
        "status": (
            "CERTIFIED_EXACT_SEED_DIRECT_STANDARD_N_OPERATOR_PHASE_BLOCK"
            "__F18_INSTALLED"
        ),
        "round125_contract": {
            "producer_sha256": PRODUCER_INPUT_PINS[
                "deliverables/cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17.py"
            ],
            "certificate_sha256": PRODUCER_INPUT_PINS[
                "deliverables/cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json"
            ],
            "result_sha256": ROUND125_RESULT_SHA256,
            "actual_child_count": 24,
            "stage_level_slot_counts": {"0": 48, "1": 24, "2": 48},
            "roof_level_js_by_stage": {
                "0": [0, 1],
                "1": [0],
                "2": [0, 1],
            },
            "inherited_slot_count": 2040,
            "inherited_child_local_maturity": "17/18",
            "remaining_uninstalled_child_fields": ["F18"],
        },
        "direct_standard_N_phase_registration": phase_registration_contract(),
        "preexisting_F1_F17_same_key_map_rows": map_rows,
        "preexisting_F1_F17_same_key_map_rows_sha256": digest(map_rows),
        "gate5_F18_slot_rows": f18_rows,
        "gate5_F18_slot_rows_sha256": digest(f18_rows),
        "combined_installed_child_local_slot_registry_after_F18": {
            "Round125_inherited_slot_count": 2040,
            "Round125_combined_registry_chain_sha256":
                prior_registry["combined_registry_chain_sha256"],
            "Round125_new_F17_slot_ids_sha256":
                prior_registry["new_F17_slot_ids_sha256"],
            "rebuilt_preexisting_F1_F17_slot_count": 2040,
            "rebuilt_preexisting_F1_F17_slot_ids_sha256":
                digest(preexisting_ids),
            "preexisting_F1_F17_same_key_map_rows_sha256":
                digest(map_rows),
            "new_F18_slot_count": 120,
            "new_F18_slot_ids_sha256": digest(new_ids),
            "combined_slot_count": 2160,
            "combined_slot_ids_sha256": digest(preexisting_ids + new_ids),
            "combined_registry_chain_sha256": digest(
                [
                    prior_registry["combined_registry_chain_sha256"],
                    digest(map_rows),
                    new_ids,
                ]
            ),
            "slot_count_per_certified_field": 120,
            "certified_field_indices": list(range(1, 19)),
            "uninstalled_field_indices": [],
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "all_keys_are_full_word_subbranch_roof_field_keys": True,
            "each_F18_slot_binds_one_complete_F1_F17_same_key_map": True,
            "global_registry_or_block_inferred": False,
        },
        "count_ledger": count_ledger,
        "gate5_actual_child_field_status": gate_status,
        "rank3_seed_child_field_maturity": "18/18",
        "seed_local_complete_18_field_level_block_count": 120,
        "seed_local_complete_18_field_child_packet_count": 24,
        "remaining_uninstalled_child_fields": [],
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "global_complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "one Round121 exact-b seed, its 24 materialized common children,"
            " 120 full word/subbranch/roof keys, 120 rebuilt F1-F17 same-key"
            " maps, and 120 direct-standard-N structural F18 registrations"
        ),
        "strict_nonclaims": [
            "no operator Wiener invertibility theorem",
            "no operator Wiener aperiodicity theorem",
            "no Kac return-wide closure theorem",
            "no claim that five symbolic roof levels are five collisions",
            "no arbitrary-return-depth or all-Borel-key phase registration",
            "no global complete 18-field block",
            "no global Gate5 maturity upgrade",
            "no change to the frozen global complete_18_field_block_count semantics",
            "no global power-Orlicz, owner drift, or strong cemetery theorem",
            "no CM2 claim",
        ],
        "upstream_and_helper_pins": dict(sorted(PRODUCER_INPUT_PINS.items())),
    }


def evaluate_document(
    document: Any,
    expected: dict[str, Any],
) -> dict[str, Any]:
    require(type(document) is dict, "certificate top object")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate closed envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result object")
    require(document["result_sha256"] == digest(result), "certificate result digest")
    require(set(result) == set(expected), "certificate result closed schema")

    maps = result["preexisting_F1_F17_same_key_map_rows"]
    slots = result["gate5_F18_slot_rows"]
    require(type(maps) is list and type(slots) is list, "certificate row lists")
    for index, row in enumerate(maps):
        validate_row(row, f"map row {index}")
    for index, row in enumerate(slots):
        validate_row(row, f"F18 row {index}")
    require(
        result["preexisting_F1_F17_same_key_map_rows_sha256"] == digest(maps),
        "map rows aggregate digest",
    )
    require(
        result["gate5_F18_slot_rows_sha256"] == digest(slots),
        "F18 rows aggregate digest",
    )
    require(result == expected, "independent exact reconstruction")

    return {
        "actual_child_count": 24,
        "preexisting_F1_F17_same_key_map_row_count": len(maps),
        "rebuilt_preexisting_slot_count": sum(
            len(row["bound_preexisting_F1_F17_slots"]) for row in maps
        ),
        "F18_slot_count": len(slots),
        "F18_stage_slot_counts": {
            str(stage): Counter(row["stage"] for row in slots)[stage]
            for stage in range(3)
        },
        "combined_child_local_slot_count":
            result["count_ledger"]["combined_child_local_slot_count"],
        "seed_local_complete_18_field_level_block_count":
            result["seed_local_complete_18_field_level_block_count"],
        "seed_local_complete_18_field_child_packet_count":
            result["seed_local_complete_18_field_child_packet_count"],
        "rank3_seed_child_field_maturity":
            result["rank3_seed_child_field_maturity"],
        "remaining_uninstalled_child_fields":
            result["remaining_uninstalled_child_fields"],
        "gate5_global_maturity": result["gate5_global_maturity"],
        "complete_18_field_block_count":
            result["complete_18_field_block_count"],
        "global_complete_18_field_block_count":
            result["global_complete_18_field_block_count"],
        "gate5_block_count": result["gate5_block_count"],
        "cm2_verdict": result["cm2_verdict"],
    }


def resign_document(document: dict[str, Any]) -> None:
    result = document["result"]
    maps = result.get("preexisting_F1_F17_same_key_map_rows", [])
    slots = result.get("gate5_F18_slot_rows", [])
    if type(maps) is list:
        for row in maps:
            if type(row) is not dict:
                continue
            bindings = row.get("bound_preexisting_F1_F17_slots")
            if type(bindings) is list:
                row["bound_preexisting_F1_F17_slots_sha256"] = digest(bindings)
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {key: value for key, value in row.items() if key != "row_sha256"}
                )
        result["preexisting_F1_F17_same_key_map_rows_sha256"] = digest(maps)
    map_by_id = {
        row.get("same_key_map_row_id"): row
        for row in maps
        if type(row) is dict and type(row.get("same_key_map_row_id")) is str
    }
    if type(slots) is list:
        for row in slots:
            if type(row) is not dict:
                continue
            linked = map_by_id.get(
                row.get("preexisting_F1_F17_same_key_map_row_id")
            )
            if type(linked) is dict:
                row["preexisting_F1_F17_same_key_map_row_sha256"] = linked.get(
                    "row_sha256"
                )
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {key: value for key, value in row.items() if key != "row_sha256"}
                )
        result["gate5_F18_slot_rows_sha256"] = digest(slots)
    registry = result.get(
        "combined_installed_child_local_slot_registry_after_F18"
    )
    if type(registry) is dict and type(maps) is list and type(slots) is list:
        preexisting_ids = [
            binding.get("slot_id")
            for row in maps
            if type(row) is dict
            for binding in row.get("bound_preexisting_F1_F17_slots", [])
            if type(binding) is dict
        ]
        new_ids = [
            row.get("slot_id") for row in slots if type(row) is dict
        ]
        registry["rebuilt_preexisting_F1_F17_slot_count"] = len(preexisting_ids)
        registry["rebuilt_preexisting_F1_F17_slot_ids_sha256"] = digest(
            preexisting_ids
        )
        registry["preexisting_F1_F17_same_key_map_rows_sha256"] = digest(maps)
        registry["new_F18_slot_count"] = len(new_ids)
        registry["new_F18_slot_ids_sha256"] = digest(new_ids)
        registry["combined_slot_count"] = len(preexisting_ids) + len(new_ids)
        registry["combined_slot_ids_sha256"] = digest(preexisting_ids + new_ids)
        registry["combined_registry_chain_sha256"] = digest(
            [
                registry.get("Round125_combined_registry_chain_sha256"),
                digest(maps),
                new_ids,
            ]
        )
    document["result_sha256"] = digest(result)


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    target = root
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value


def delete_path(root: Any, path: tuple[Any, ...]) -> None:
    target = root
    for part in path[:-1]:
        target = target[part]
    del target[path[-1]]


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    """Reject re-signed semantic attacks, not merely stale digest attacks."""
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def setter(label: str, path: tuple[Any, ...], value: Any) -> None:
        cases.append((label, lambda d, p=path, v=value: set_path(d, p, v)))

    def deleter(label: str, path: tuple[Any, ...]) -> None:
        cases.append((label, lambda d, p=path: delete_path(d, p)))

    result = ("result",)
    phase = result + ("direct_standard_N_phase_registration",)
    registry = result + (
        "combined_installed_child_local_slot_registry_after_F18",
    )
    first_map = result + ("preexisting_F1_F17_same_key_map_rows", 0)
    first_binding = first_map + ("bound_preexisting_F1_F17_slots", 0)
    first_f18 = result + ("gate5_F18_slot_rows", 0)

    setter("schema swap", ("schema",), "cm2.round126.mutant.v1")
    deleter("missing result field", result + ("status",))
    setter("unknown result field", result + ("mutant_unknown",), True)
    setter("certificate status downgrade", result + ("status",), "FRONTIER_ONLY")
    setter("phase route promoted to Wiener", phase + ("route",), "Wiener")
    setter(
        "phase registration promoted to theorem",
        phase + ("registration_scope",),
        "GLOBAL_OPERATOR_THEOREM",
    )
    setter(
        "stage zero return length altered",
        phase + ("stage_return_length_by_stage", "0"),
        3,
    )
    setter("child path exponent altered", phase + ("child_path_exponent",), 6)
    setter(
        "Wiener theorem falsely claimed",
        phase + ("operator_Wiener_theorem",),
        "CERTIFIED",
    )
    setter(
        "Kac closure falsely claimed",
        phase + ("Kac_return_wide_closure",),
        "CERTIFIED",
    )
    setter(
        "global phase falsely claimed",
        phase + ("global_operator_phase_registration",),
        "CERTIFIED",
    )
    setter(
        "map immutable word altered",
        first_map + ("immutable_base_key", 0),
        "mutant-word",
    )
    setter(
        "map field count reduced",
        first_map + ("bound_preexisting_field_count",),
        16,
    )
    setter(
        "map carrier digest altered",
        first_map + ("standard_family_leg_operator_row_sha256",),
        "0" * 64,
    )
    setter(
        "binding field index altered",
        first_binding + ("field_index",),
        18,
    )
    setter(
        "binding source digest altered",
        first_binding + ("source_slot_canonical_sha256",),
        "0" * 64,
    )
    setter(
        "F18 field semantics promoted",
        first_f18 + ("field_bound_semantics",),
        "GLOBAL_OPERATOR_THEOREM",
    )
    setter(
        "F18 suffix length altered",
        first_f18 + ("suffix_length_r_minus_j",),
        3,
    )
    setter(
        "F18 monomial altered",
        first_f18 + ("stage_block_operator_monomial",),
        "z^3",
    )
    setter(
        "F18 Wiener invertibility falsely claimed",
        first_f18 + ("operator_Wiener_invertibility_claimed",),
        True,
    )
    setter(
        "F18 Kac closure falsely claimed",
        first_f18 + ("Kac_closure_claimed",),
        True,
    )
    setter(
        "F18 global block falsely claimed",
        first_f18 + ("global_operator_phase_block_claimed",),
        True,
    )
    setter(
        "F18 CM2 falsely claimed",
        first_f18 + ("CM2_claimed",),
        True,
    )
    setter(
        "registry global inference enabled",
        registry + ("global_registry_or_block_inferred",),
        True,
    )
    setter(
        "registry certified fields truncated",
        registry + ("certified_field_indices",),
        list(range(1, 18)),
    )
    setter(
        "seed local level count inflated",
        result + ("seed_local_complete_18_field_level_block_count",),
        121,
    )
    setter(
        "seed local child packet count inflated",
        result + ("seed_local_complete_18_field_child_packet_count",),
        25,
    )
    setter(
        "global complete count smuggled through ledger",
        result + ("count_ledger", "global_complete_18_field_block_count"),
        1,
    )
    setter(
        "global maturity falsely upgraded",
        result + ("gate5_global_maturity",),
        "18/18",
    )
    setter(
        "complete block falsely materialized",
        result + ("complete_18_field_block_count",),
        1,
    )
    setter(
        "global complete block falsely materialized",
        result + ("global_complete_18_field_block_count",),
        1,
    )
    setter(
        "Gate5 block falsely materialized",
        result + ("gate5_block_count",),
        1,
    )
    setter("CM2 falsely promoted", result + ("cm2_verdict",), "GO_FOR_CLAIM")
    setter(
        "scope broadened to arbitrary returns",
        result + ("strict_scope",),
        "all return depths and all Borel keys",
    )
    setter(
        "global Gate5 field status promoted",
        result + ("gate5_actual_child_field_status", "F18"),
        "GLOBAL_COMPLETE_BLOCK_CERTIFIED",
    )
    setter(
        "upstream producer pin altered",
        result
        + (
            "upstream_and_helper_pins",
            "deliverables/cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17.py",
        ),
        "0" * 64,
    )
    cases.append(
        (
            "map row order swapped",
            lambda d: d["result"]["preexisting_F1_F17_same_key_map_rows"].__setitem__(
                slice(0, 2),
                list(
                    reversed(
                        d["result"]["preexisting_F1_F17_same_key_map_rows"][:2]
                    )
                ),
            ),
        )
    )
    cases.append(
        (
            "F18 row order swapped",
            lambda d: d["result"]["gate5_F18_slot_rows"].__setitem__(
                slice(0, 2),
                list(reversed(d["result"]["gate5_F18_slot_rows"][:2])),
            ),
        )
    )

    rejected: list[str] = []
    for label, mutate in cases:
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        resign_document(candidate)
        try:
            evaluate_document(candidate, expected)
        except Exception:
            rejected.append(label)
            continue
        raise VerificationError(f"re-signed semantic mutation accepted:{label}")
    require(
        len(rejected) == len(cases) == len(set(rejected)),
        "semantic mutation census",
    )
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    """Exercise the strict byte parser and the closed certificate envelope."""
    base = canonical(certificate).encode("utf-8")
    require(b'"combined_slot_count":2160' in base, "strict attack count anchor")
    require(b'"gate5_block_count":0' in base, "strict attack zero anchor")
    require(b'"status":' in base, "strict attack status anchor")

    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level schema key",
            base.replace(b"{", b'{"schema":"duplicate",', 1),
        ),
        (
            "duplicate nested status key",
            base.replace(b'"status":', b'"status":"duplicate","status":', 1),
        ),
        (
            "floating-point integer",
            base.replace(
                b'"combined_slot_count":2160',
                b'"combined_slot_count":2160.0',
                1,
            ),
        ),
        (
            "NaN constant",
            base.replace(b'"gate5_block_count":0', b'"gate5_block_count":NaN', 1),
        ),
        (
            "positive Infinity constant",
            base.replace(
                b'"gate5_block_count":0',
                b'"gate5_block_count":Infinity',
                1,
            ),
        ),
        (
            "negative Infinity constant",
            base.replace(
                b'"gate5_block_count":0',
                b'"gate5_block_count":-Infinity',
                1,
            ),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + base),
        ("invalid UTF-8", base[:-1] + b"\xff}"),
        (
            "unpaired surrogate",
            b'{"result":{},"result_sha256":"","schema":"\\ud800"}',
        ),
        ("top-level array", b"[" + base + b"]"),
        ("trailing second document", base + b"{}"),
        (
            "closed envelope extra field",
            base[:-1] + b',"unknown":true}',
        ),
    ]
    rejected: list[str] = []
    for label, raw in attacks:
        try:
            value = parse_strict_bytes(raw)
            evaluate_document(value, expected)
        except Exception:
            rejected.append(label)
            continue
        raise VerificationError(f"strict JSON attack accepted:{label}")
    require(
        len(rejected) == len(attacks) == len(set(rejected)),
        "strict JSON attack census",
    )
    return rejected


def verification_document(
    certificate_path: Path,
    certificate: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    r125: dict[str, Any],
    r125_verification: dict[str, Any],
) -> dict[str, Any]:
    expected = expected_result(r121, r122, r125)
    counts = evaluate_document(certificate, expected)
    semantic_labels = semantic_mutations(certificate, expected)
    strict_labels = strict_json_attacks(certificate, expected)
    result = {
        "status": "PASS",
        "independence_contract": {
            "imports_Round126_producer": False,
            "executes_Round126_producer": False,
            "Round126_producer_is_byte_pinned_only": True,
            "imports_upstream_producer_modules": False,
            "Round121_Round122_Round125_certificates_strict_parsed_as_data":
                True,
            "Round125_independent_verification_required_PASS": True,
            "all_120_F1_F17_same_key_maps_rebuilt_from_upstream_rows": True,
            "all_120_F18_rows_rebuilt_from_exact_integer_stage_lengths": True,
            "all_2160_child_local_slot_ids_reaccounted": True,
            "re_signed_semantic_mutations_required_rejected": True,
            "strict_JSON_attacks_required_rejected": True,
        },
        "producer_sha256": ROUND126_PRODUCER_SHA256,
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "certificate_sha256": sha256(certificate_path),
        "certificate_result_sha256": certificate["result_sha256"],
        "upstream_byte_pin_count": len(UPSTREAM_PINS),
        "upstream_result_sha256_pins": {
            "Round121": ROUND121_RESULT_SHA256,
            "Round122": ROUND122_RESULT_SHA256,
            "Round125": ROUND125_RESULT_SHA256,
        },
        "Round125_verification_crosslink": {
            "status": r125_verification["status"],
            "certificate_sha256": r125_verification["certificate_sha256"],
            "verification_result_sha256":
                strict_document(
                    ROUND125_VERIFICATION,
                    (
                        "cm2.round125.rank3-exact-seed-graph-current"
                        "-dynamic-test-f17-verification.v1"
                    ),
                )["result_sha256"],
        },
        "reconstructed_counts": counts,
        "exact_phase_arithmetic_audit": {
            "route": "direct_standard_N",
            "stage_return_lengths": {"0": 2, "1": 1, "2": 2},
            "stage_level_slot_counts": {"0": 48, "1": 24, "2": 48},
            "prefix_suffix_identity": "z^j*z^(r-j)=z^r",
            "child_stage_block_identity": "z^2*z^1*z^2=z^5",
            "structural_registration_only": True,
            "operator_Wiener_invertibility_proved": False,
            "operator_Wiener_aperiodicity_proved": False,
            "Kac_return_wide_closure_proved": False,
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "determinism_contract": {
            "canonical_JSON":
                "sort_keys=True, indent=2, allow_nan=False, final newline",
            "stable_map_and_F18_order": "common_rank,stage,roof_level_j",
            "PYTHONHASHSEED_independent": True,
        },
        "safety_state": {
            "rank3_seed_child_field_maturity": "18/18",
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    certificate_value = parse_strict_bytes(args.certificate.read_bytes())
    require(type(certificate_value) is dict, "certificate top object")
    r121, r122, r125, r125_verification = load_upstream()
    verification = verification_document(
        args.certificate,
        certificate_value,
        r121,
        r122,
        r125,
        r125_verification,
    )
    text = json.dumps(
        verification,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(canonical({
        "status": verification["result"]["status"],
        "output": str(args.output),
        "result_sha256": verification["result_sha256"],
        "semantic_mutation_test_count":
            verification["result"]["semantic_mutation_test_count"],
        "strict_json_attack_count":
            verification["result"]["strict_json_attack_count"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
