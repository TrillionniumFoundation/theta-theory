#!/usr/bin/env python3
"""Independent verifier for the Round127 global-registry/exact-seed crosswalk.

The verifier never imports or executes the Round127 producer.  It independently
replays the exact-rational 448-pair by 985-pattern symbolic registry, recovers
the three Round113 official word rows, rebuilds the 24 Round121 half-open
children and refined subbranches, and reaccounts the Round126 72 carriers,
120 base keys, and 2,160 exact-once field slots.  It keeps symbolic registry
incidence separate from physical/domain coverage and preserves the frozen
global Gate5 fail-closed state.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterator


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round127_global_return_word_exact_seed_crosswalk.py"
CERTIFICATE = (
    HERE / "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json"
)
GLOBAL_PRODUCER = HERE / "cm2_gate5_return_word_three_norm_frontier_cert.py"
GLOBAL_VERIFIER = HERE / "cm2_gate5_return_word_three_norm_frontier_verifier.py"
GLOBAL_MANIFEST = (
    HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
ROUND113 = (
    HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
)
ROUND113_VERIFICATION = (
    HERE
    / "cm2-round113-rank3-endpoint-sheet-owner-ordering-verification-2026-07-23.json"
)
ROUND117 = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
)
ROUND117_VERIFICATION = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-verification-2026-07-23.json"
)
ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND121_VERIFICATION = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
)
ROUND126_PRODUCER = (
    HERE / "cm2_round126_rank3_exact_seed_operator_phase_block_f18.py"
)
ROUND126 = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-2026-07-23.json"
)
ROUND126_VERIFIER = (
    HERE / "cm2_round126_rank3_exact_seed_operator_phase_block_f18_verifier.py"
)
ROUND126_VERIFICATION = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-verification-2026-07-23.json"
)

CERTIFICATE_SCHEMA = "cm2.round127.global-return-word-exact-seed-crosswalk.v1"
VERIFICATION_SCHEMA = (
    "cm2.round127.global-return-word-exact-seed-crosswalk-verification.v1"
)
PRODUCER_SHA256 = (
    "ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd"
)

BYTE_PINS = {
    GLOBAL_PRODUCER.name:
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    GLOBAL_VERIFIER.name:
        "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    GLOBAL_MANIFEST.name:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    ROUND113.name:
        "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND113_VERIFICATION.name:
        "bcd3f5ddf1763d58a256b117a757f3db076d03b1b7a8441c34dfa7b467a55bc0",
    ROUND117.name:
        "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND117_VERIFICATION.name:
        "06647b5b6f81ad0e8098f5885e9aa2b2c926991faaa34102e0646c058da0764f",
    ROUND121.name:
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    ROUND121_VERIFICATION.name:
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    ROUND126_PRODUCER.name:
        "db5a3a4250e26bdeeb6ac4a2a6abade5014073b5901339e30d5c4b4907fcba68",
    ROUND126.name:
        "5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e",
    ROUND126_VERIFIER.name:
        "2fa8136e0c07457486515bc7c342a4857ed61705f33c7a91bf681ab02905a9ec",
    ROUND126_VERIFICATION.name:
        "bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b",
}

SCHEMAS = {
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND113_VERIFICATION.name:
        "cm2.round113.rank3-endpoint-sheet-owner-ordering.verification.v1",
    ROUND117.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND117_VERIFICATION.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells-verification.v1",
    ROUND121.name:
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    ROUND121_VERIFICATION.name:
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1",
    ROUND126.name:
        "cm2.round126.rank3-exact-seed-operator-phase-block-f18.v1",
    ROUND126_VERIFICATION.name:
        "cm2.round126.rank3-exact-seed-operator-phase-block-f18-verification.v1",
}

RESULT_PINS = {
    ROUND113.name:
        "33f564bd6afea1ba346ed0048a4bc61fa1a1bf91ebbbac546a32b051643bda67",
    ROUND113_VERIFICATION.name:
        "c87d20aee8d652f45a52ca4bd8e9b58753de536036ec6373b2067ef381c972b9",
    ROUND117.name:
        "d8e759c9397c595a011476661cb6144130f708116198886645366288788d2b0f",
    ROUND117_VERIFICATION.name:
        "eb2f83bbf6b0a08e2b803e40b7422688339852eae3f840c6936ac0cd56e769d2",
    ROUND121.name:
        "962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8",
    ROUND121_VERIFICATION.name:
        "8c830e2e26d9b4cce6f034ad382420bf7c7aac0b422979b14e88888fe1b888e5",
    ROUND126.name:
        "0a15b8afe9e6434fa2766ffa55159b5f7944eb7d2a3d3a39a31d67261effd63a",
    ROUND126_VERIFICATION.name:
        "6ac2ff5a80d08b1e0a133599ca35836bd087b9c8a831ce9128a7225c0dba63fd",
}

GLOBAL_STREAM_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)
GLOBAL_PAIR_ROWS_SHA256 = (
    "ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75"
)
GLOBAL_PATTERN_ROWS_SHA256 = (
    "2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d"
)
GLOBAL_FIELD_SCHEMA_SHA256 = (
    "bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5"
)

PARENT_ID = (
    "round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
)
SHEET_ID = (
    "round112-bypass-sheet:82388860fd9a24f85561682533f70ba8789125b13ea29deb027aa3bcb293201f"
)
PATH_ID = (
    "gate5-rank3-endpoint-sheet-path:9f335e832599b906ffef1f29b1751e5250309a48501b948598115a92ac44b5f7"
)
OPERATOR_CELL_ID = (
    "round117-operator-cell:dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1"
)
EXACT_SEED_ID = (
    "round121-exact-parent-W:41462c4f6815ad00fd5d4456e5c13885feeab5e8343b009b8872b72d15cf18c8"
)
EXPECTED_BRANCH = [7, "G[0,0]", "W[-1,-2]", 1]
EXPECTED_OWNERS = ["W[-1,-1]", "G[0,0]", "G[-1,-2]"]
EXPECTED_RELATIVE_TARGETS = ["W[-1,-1]", "G[1,1]", "G[-1,-2]"]
EXPECTED_COLLISION_CHARTS = ["N", "S", "N"]
EXPECTED_WORD_ORDINALS = [102441, 346720, 180256]
EXPECTED_CUT_ORDER = [
    (2, 1), (2, 2), (1, 1), (2, 3), (2, 4), (2, 5),
    (1, 2), (2, 6), (2, 7), (1, 3), (2, 8), (2, 9),
    (2, 10), (1, 4), (2, 11), (2, 12), (1, 5), (2, 13),
    (2, 14), (2, 15), (1, 6), (2, 16), (2, 17),
]

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
    18: 126,
}
STAGE_RETURN_LENGTH = {0: 2, 1: 1, 2: 2}
ROOF_LEVELS_BY_STAGE = {0: [0, 1], 1: [0], 2: [0, 1]}
STAGE_RECUT_KEY = {
    0: "source_recut_instance_id",
    1: "first_image_recut_instance_id",
    2: "second_image_recut_instance_id",
}
EXPECTED_STAGE_BASE_COUNTS = Counter({0: 48, 1: 24, 2: 48})

Q = Fraction
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)
SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)


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


def row_id(prefix: str, payload: Any) -> str:
    return f"{prefix}:{digest([prefix, payload])}"


def reject_float(token: str) -> Any:
    raise VerificationError(f"floating-point JSON token forbidden:{token}")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise VerificationError(f"duplicate JSON key:{key}")
        value[key] = item
    return value


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


def strict_document(path: Path, schema: str, result_pin: str) -> dict[str, Any]:
    document = parse_strict_bytes(path.read_bytes())
    require(type(document) is dict, f"top-level object:{path.name}")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == schema, f"schema:{path.name}")
    require(type(document["result"]) is dict, f"result object:{path.name}")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"result digest:{path.name}",
    )
    require(document["result_sha256"] == result_pin, f"result pin:{path.name}")
    return document


def validate_hashed_row(
    row: Any, label: str, hash_key: str = "row_sha256"
) -> None:
    require(type(row) is dict, f"{label}:object")
    require(type(row.get(hash_key)) is str, f"{label}:{hash_key} type")
    payload = {key: value for key, value in row.items() if key != hash_key}
    require(row[hash_key] == digest(payload), f"{label}:{hash_key}")


def verify_byte_pins() -> None:
    require(
        PRODUCER.is_file() and not PRODUCER.is_symlink(),
        "Round127 producer regular file",
    )
    require(sha256(PRODUCER) == PRODUCER_SHA256, "Round127 producer byte pin")
    for name, expected in BYTE_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"regular input:{name}")
        require(sha256(path) == expected, f"byte pin:{name}")


def target_id(target: tuple[str, int, int]) -> str:
    return f"{target[0]}[{target[1]},{target[2]}]"


def vector_interval(
    source: str, target: tuple[str, int, int]
) -> tuple[Q, Q, Q, Q]:
    obstacle, ix, iy = target
    if source == "G" and obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and obstacle == "W":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    if source == "W" and obstacle == "G":
        x = Q(2 * ix - 1, 2)
        return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def dominant_support_upper(
    cell: str, x0: Q, x1: Q, y0: Q, y1: Q
) -> Q:
    if cell == "E":
        a_upper, b_abs = x1, max(abs(y0), abs(y1))
    elif cell == "W":
        a_upper, b_abs = -x0, max(abs(y0), abs(y1))
    elif cell == "N":
        a_upper, b_abs = y1, max(abs(x0), abs(x1))
    elif cell == "S":
        a_upper, b_abs = -y0, max(abs(x0), abs(x1))
    else:
        raise VerificationError("source chart cell")
    if a_upper >= 0:
        return a_upper + b_abs * INV_SQRT2_UPPER
    return a_upper * INV_SQRT2_LOWER + b_abs * INV_SQRT2_UPPER


def retained_pair(chart: str, target: tuple[str, int, int]) -> bool:
    source, cell = chart.split(":")
    obstacle, ix, iy = target
    if obstacle == source and ix == 0 and iy == 0:
        return False
    x0, x1, y0, y1 = vector_interval(source, target)
    threshold = TAU_MAX + RADIUS[source] + RADIUS[obstacle]
    distance_squared = (
        square_min_abs(x0, x1) + square_min_abs(y0, y1)
    )
    if distance_squared >= threshold * threshold:
        return False
    support = dominant_support_upper(cell, x0, x1, y0, y1)
    return support >= RADIUS[source] - RADIUS[obstacle]


def orientation_choices(count: int) -> tuple[int, ...]:
    return (0,) if count == 0 else (-1, 1)


def crossing_patterns() -> Iterator[tuple[str, ...]]:
    for nx in range(5):
        for ny in range(5):
            length = nx + ny
            for sx in orientation_choices(nx):
                for sy in orientation_choices(ny):
                    for x_positions in itertools.combinations(range(length), nx):
                        x_set = set(x_positions)
                        x_token = "X+" if sx > 0 else "X-"
                        y_token = "Y+" if sy > 0 else "Y-"
                        yield tuple(
                            x_token if index in x_set else y_token
                            for index in range(length)
                        )


def replay_global_registry() -> dict[str, Any]:
    targets = tuple(
        (obstacle, ix, iy)
        for obstacle in ("G", "W")
        for ix in range(-4, 5)
        for iy in range(-4, 5)
    )
    require(len(targets) == 162, "162 target lifts")
    pairs = tuple(
        (chart, target_id(target))
        for chart in SOURCE_CHARTS
        for target in targets
        if retained_pair(chart, target)
    )
    patterns = tuple(crossing_patterns())
    require(
        len(pairs) == len(set(pairs)) == 448,
        "448 retained chart-target pairs",
    )
    require(
        len(patterns) == len(set(patterns)) == 985,
        "985 monotone wall patterns",
    )
    pair_digest = digest(pairs)
    pattern_digest = digest(patterns)
    require(pair_digest == GLOBAL_PAIR_ROWS_SHA256, "pair rows digest")
    require(pattern_digest == GLOBAL_PATTERN_ROWS_SHA256, "pattern rows digest")

    stream = hashlib.sha256()
    roof_count = 0
    roof_histogram: Counter[int] = Counter()
    selected: dict[int, dict[str, Any]] = {}
    wanted = set(EXPECTED_WORD_ORDINALS)
    for pair_index, (chart, target) in enumerate(pairs):
        for pattern_index, pattern in enumerate(patterns):
            ordinal = pair_index * len(patterns) + pattern_index
            row = [chart, target, list(pattern), len(pattern) + 1]
            stream.update(canonical(row).encode("utf-8"))
            stream.update(b"\n")
            roof_count += row[3]
            roof_histogram[row[3]] += 1
            if ordinal in wanted:
                row_hash = digest(row)
                selected[ordinal] = {
                    "ordinal_zero_based": ordinal,
                    "retained_chart_target_pair_ordinal_zero_based": pair_index,
                    "crossing_pattern_ordinal_zero_based": pattern_index,
                    "row": row,
                    "row_sha256": row_hash,
                    "word_key_id":
                        f"gate5-word:{ordinal:06d}:{row_hash}",
                }
    require(stream.hexdigest() == GLOBAL_STREAM_SHA256, "global stream digest")
    require(roof_count == 3286976, "global symbolic roof count")
    expected_histogram = {
        1: 448,
        2: 1792,
        3: 5376,
        4: 12544,
        5: 26880,
        6: 53760,
        7: 89600,
        8: 125440,
        9: 125440,
    }
    require(dict(sorted(roof_histogram.items())) == expected_histogram, "roof histogram")
    expected_rows = [
        ["G:W", "W[-1,-1]", ["Y-"], 2],
        ["W:N", "G[1,1]", [], 1],
        ["G:S", "G[-1,-2]", ["Y-"], 2],
    ]
    official = [selected[ordinal] for ordinal in EXPECTED_WORD_ORDINALS]
    require(
        [row["row"] for row in official] == expected_rows,
        "independent official registry rows",
    )
    return {
        "source_chart_count": len(SOURCE_CHARTS),
        "target_lift_count": len(targets),
        "retained_pair_count": len(pairs),
        "crossing_pattern_count": len(patterns),
        "candidate_word_count": len(pairs) * len(patterns),
        "candidate_word_rows_stream_sha256": stream.hexdigest(),
        "chart_target_pair_rows_sha256": pair_digest,
        "crossing_pattern_rows_sha256": pattern_digest,
        "roof_level_position_count": roof_count,
        "roof_histogram": {str(k): v for k, v in expected_histogram.items()},
        "official_words": official,
    }


def validate_global_manifest(
    manifest: Any, replay: dict[str, Any]
) -> dict[str, Any]:
    require(type(manifest) is dict, "global manifest object")
    require(
        set(manifest)
        == {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        },
        "global manifest closed top level",
    )
    require(
        manifest["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1",
        "global manifest schema",
    )
    require(
        manifest["certificate_sha256"] == BYTE_PINS[GLOBAL_PRODUCER.name]
        and manifest["verifier_sha256"] == BYTE_PINS[GLOBAL_VERIFIER.name],
        "global embedded executable pins",
    )
    result = manifest["result"]
    require(
        type(result) is dict
        and result.get("schema")
        == "cm2.gate5.return-word-three-norm-frontier.v1",
        "global manifest result",
    )
    registry = result["immutable_candidate_key_registry"]
    factor = registry["prefix_suffix_factor_contract"]
    fields = result["required_operator_field_schema"]
    require(
        registry["source_chart_count"] == replay["source_chart_count"]
        and registry["conservative_target_lift_count"]
        == replay["target_lift_count"]
        and registry["retained_chart_target_pair_count"]
        == replay["retained_pair_count"]
        and registry["crossing_pattern_count_per_pair"]
        == replay["crossing_pattern_count"]
        and registry["candidate_return_word_key_count"]
        == replay["candidate_word_count"]
        and registry["candidate_word_key_rows_sha256"]
        == replay["candidate_word_rows_stream_sha256"]
        and registry["chart_target_pair_rows_sha256"]
        == replay["chart_target_pair_rows_sha256"]
        and registry["roof_histogram"] == replay["roof_histogram"],
        "global registry versus independent replay",
    )
    require(
        factor["roof_level_prefix_suffix_factor_pair_count"]
        == replay["roof_level_position_count"]
        and factor["roof_level_index"] == "0<=j<r(w)"
        and factor["symbolic_factorisation_complete_on_every_candidate_key"]
        is True
        and factor["homogeneous_subbranch_index_instantiated"] is False,
        "global symbolic roof contract",
    )
    require(
        fields["required_field_count_per_physical_homogeneous_level"] == 18
        and fields["required_fields"]
        == [FIELD_NAMES[field] for field in range(1, 19)]
        and fields["required_field_schema_sha256"]
        == GLOBAL_FIELD_SCHEMA_SHA256
        and fields["homogeneous_subbranch_ids_materialized"] is False
        and fields["all_required_fields_populated"] is False,
        "global field frontier",
    )
    completion = result["completion"]
    require(
        registry["exact_nonempty_candidate_key_count"] is None
        and registry["complete_physical_operator_block_count"] == 0
        and completion["complete_nonempty_return_word_domain_decisions"] is False
        and completion["physical_homogeneous_subbranch_registry"] is False
        and completion["immutable_complete_return_word_operator_registry"] is False
        and completion["gate5_certified"] is False
        and manifest["verdict"]["gate5"] == "NOT_CERTIFIED",
        "global registry fail-closed frontier",
    )
    return result


def validate_verification_inputs(
    documents: dict[str, dict[str, Any]]
) -> None:
    v113 = documents[ROUND113_VERIFICATION.name]["result"]
    v117 = documents[ROUND117_VERIFICATION.name]["result"]
    v121 = documents[ROUND121_VERIFICATION.name]["result"]
    v126 = documents[ROUND126_VERIFICATION.name]["result"]
    require(
        v113["verification_status"] == "PASS"
        and v113["certificate_sha256"] == BYTE_PINS[ROUND113.name]
        and v113["independent_verifier_does_not_import_round113_producer_or_engine"]
        is True,
        "Round113 verification PASS",
    )
    require(
        v117["verdict"] == "PASS"
        and v117["certificate_sha256"] == BYTE_PINS[ROUND117.name]
        and v117["producer_module_imported"] is False,
        "Round117 verification PASS",
    )
    require(
        v121["verdict"] == "PASS"
        and v121["certificate_sha256"] == BYTE_PINS[ROUND121.name]
        and v121["upstream_R113_R117_R120_seed_crosswalk_verified"] is True
        and v121["official_candidate_registry_rows_sha256"]
        == GLOBAL_STREAM_SHA256
        and v121["independently_replayed_common_child_count"] == 24
        and v121["independently_replayed_refined_subbranch_count"] == 24
        and v121["independently_replayed_full_key_slot_count"] == 720,
        "Round121 verification PASS",
    )
    safety = v126["safety_state"]
    require(
        v126["status"] == "PASS"
        and v126["certificate_sha256"] == BYTE_PINS[ROUND126.name]
        and v126["certificate_result_sha256"] == RESULT_PINS[ROUND126.name]
        and v126["reconstructed_counts"]["actual_child_count"] == 24
        and v126["reconstructed_counts"]["rebuilt_preexisting_slot_count"]
        == 2040
        and v126["reconstructed_counts"]["F18_slot_count"] == 120
        and v126["reconstructed_counts"]["combined_child_local_slot_count"]
        == 2160
        and safety["rank3_seed_child_field_maturity"] == "18/18"
        and safety["seed_local_complete_18_field_level_block_count"] == 120
        and safety["seed_local_complete_18_field_child_packet_count"] == 24
        and safety["global_complete_18_field_block_count"] == 0
        and safety["complete_18_field_block_count"] == 0
        and safety["gate5_block_count"] == 0
        and safety["gate5_global_maturity"] == "10/18"
        and safety["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round126 verification PASS and safety",
    )


def load_inputs() -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    verify_byte_pins()
    replay = replay_global_registry()
    manifest = parse_strict_bytes(GLOBAL_MANIFEST.read_bytes())
    global_result = validate_global_manifest(manifest, replay)
    documents = {
        path.name: strict_document(path, SCHEMAS[path.name], RESULT_PINS[path.name])
        for path in (
            ROUND113,
            ROUND113_VERIFICATION,
            ROUND117,
            ROUND117_VERIFICATION,
            ROUND121,
            ROUND121_VERIFICATION,
            ROUND126,
            ROUND126_VERIFICATION,
        )
    }
    validate_verification_inputs(documents)
    return global_result, documents, replay


def exact_path_inputs(
    r113: dict[str, Any], replay: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    require(
        r113["official_registry_candidate_key_count"]
        == replay["candidate_word_count"]
        and r113["official_registry_rows_sha256"]
        == replay["candidate_word_rows_stream_sha256"]
        and r113["sheet_rows_sha256"] == digest(r113["sheet_rows"]),
        "Round113 registry and sheet aggregate crosslink",
    )
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for sheet in r113["sheet_rows"]:
        require(type(sheet) is dict, "Round113 sheet row")
        for cell in sheet["certified_cells"]:
            if cell.get("cell_id") == PARENT_ID:
                matches.append((sheet, cell))
    require(len(matches) == 1, "unique Round113 parent cell")
    sheet, cell = matches[0]
    require(
        sheet["sheet_id"] == SHEET_ID
        and sheet["sheet_kind"] == "BYPASS"
        and sheet["source_chart"] == "G:W"
        and sheet["branch_key"] == EXPECTED_BRANCH,
        "Round113 parent root",
    )
    replay_words = replay["official_words"]
    expected_ids = [word["word_key_id"] for word in replay_words]
    require(
        cell["official_path_id"] == PATH_ID
        and cell["official_word_key_ids"] == expected_ids
        and cell["ordered_regular_relative_interior_owner_ids"]
        == EXPECTED_OWNERS
        and len(cell["leg_audits"]) == 3,
        "Round113 exact path contract",
    )
    legs: list[dict[str, Any]] = []
    for stage, (leg, independent) in enumerate(
        zip(cell["leg_audits"], replay_words, strict=True)
    ):
        official = leg["official_word_key"]
        require(
            set(official)
            == {"ordinal_zero_based", "row", "row_sha256", "word_key_id"},
            f"Round113 closed official word:{stage}",
        )
        require(
            official["ordinal_zero_based"] == independent["ordinal_zero_based"]
            and official["row"] == independent["row"]
            and official["row_sha256"] == independent["row_sha256"]
            and official["word_key_id"] == independent["word_key_id"],
            f"Round113 word equals independent registry row:{stage}",
        )
        require(
            official["row_sha256"] == digest(official["row"])
            and official["word_key_id"]
            == (
                f"gate5-word:{official['ordinal_zero_based']:06d}:"
                f"{official['row_sha256']}"
            ),
            f"Round113 official word stable ID:{stage}",
        )
        pair_ordinal = independent[
            "retained_chart_target_pair_ordinal_zero_based"
        ]
        pattern_ordinal = independent[
            "crossing_pattern_ordinal_zero_based"
        ]
        require(
            official["ordinal_zero_based"] == pair_ordinal * 985 + pattern_ordinal,
            f"official word ordinal decomposition:{stage}",
        )
        require(
            leg["official_relative_target_id"] == EXPECTED_RELATIVE_TARGETS[stage]
            and leg["selected_collision_chart"]
            == EXPECTED_COLLISION_CHARTS[stage]
            and leg["ordered_clean_wall_record"] == official["row"][2],
            f"Round113 leg semantics:{stage}",
        )
        legs.append(
            {
                "stage": stage,
                "official": official,
                "relative_registry_target_id":
                    leg["official_relative_target_id"],
                "absolute_owner_id": EXPECTED_OWNERS[stage],
                "selected_collision_chart":
                    leg["selected_collision_chart"],
                "retained_pair_ordinal": pair_ordinal,
                "pattern_ordinal": pattern_ordinal,
            }
        )
    require(
        legs[1]["relative_registry_target_id"] == "G[1,1]"
        and legs[1]["absolute_owner_id"] == "G[0,0]"
        and legs[1]["relative_registry_target_id"]
        != legs[1]["absolute_owner_id"],
        "second-leg relative/absolute namespace separation",
    )
    return cell, legs


def validate_round117_join(
    r117: dict[str, Any], word_ids: list[str]
) -> dict[str, Any]:
    require(
        r117["common_refinement_rows_sha256"]
        == digest(r117["common_refinement_rows"]),
        "Round117 common refinement aggregate",
    )
    parents = [
        row
        for row in r117["common_refinement_rows"]
        if row.get("parent_round113_cell_id") == PARENT_ID
    ]
    require(len(parents) == 1, "unique Round117 parent")
    parent = parents[0]
    require(
        parent["parent_round113_sheet_id"] == SHEET_ID
        and parent["branch_key"] == EXPECTED_BRANCH
        and parent["sheet_kind"] == "BYPASS"
        and parent["official_path_id_inherited"] == PATH_ID
        and parent["official_word_key_ids_inherited"] == word_ids
        and parent["actual_third_collision_owner_id"] == "G[-1,-2]"
        and parent["actual_third_collision_homogeneity_label"]
        == "H0_CENTRAL",
        "Round117 inherited root",
    )
    samples = [
        family
        for family in parent["generator_families"]
        if family.get("stable_id_interface_sample", {}).get("operator_cell_id")
        == OPERATOR_CELL_ID
    ]
    require(len(samples) == 1, "unique Round117 operator-cell sample")
    sample = samples[0]
    require(
        sample["family"]
        == "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0"
        and sample["source_label_domain"] == "H0_CENTRAL_OUTER"
        and sample["stable_id_interface_sample"][
            "sample_is_certified_nonempty_for_this_parent"
        ]
        is True,
        "Round117 nonempty sample semantics",
    )
    return parent


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def source_boundary_id(which: str) -> str:
    require(which in {"left", "right"}, "source boundary side")
    return f"round121-source-{which}-endpoint:" + digest(
        ["round121-source-boundary-v1", EXACT_SEED_ID, which]
    )


def recut_instance_id(stage: int, natural_index: int) -> str:
    return "round121-recut-instance:" + digest(
        [
            "round121-materialized-adapted-input-recut-v1",
            EXACT_SEED_ID,
            stage,
            natural_index,
        ]
    )


def rebuild_round121_subbranches(
    r121: dict[str, Any], word_ids: list[str]
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    expected_seed_id = "round121-exact-parent-W:" + digest(
        [
            "round121-exact-parent-W-v1",
            PARENT_ID,
            OPERATOR_CELL_ID,
            "round120-angular-lift:G:W:k0",
            "c0=1/16384",
            "b3=3/65536",
            "unique-root:F_BYPASS(t,c0,b3)=0",
        ]
    )
    require(expected_seed_id == EXACT_SEED_ID, "independent exact-seed ID")
    seed = r121["exact_seed_contract"]
    replay = r121["whole_seed_owner_candidate_replay"]
    require(
        seed["round113_parent_id"] == PARENT_ID
        and seed["round117_operator_cell_id"] == OPERATOR_CELL_ID
        and seed["exact_parent_W_seed_id"] == expected_seed_id
        and seed["branch_key"] == EXPECTED_BRANCH
        and seed["sheet_kind"] == "BYPASS"
        and seed["source_chart"] == "G:W"
        and replay["official_path_id"] == PATH_ID
        and replay["official_word_key_ids"] == word_ids
        and replay["ordered_owner_ids"] == EXPECTED_OWNERS
        and replay["selected_collision_charts"]
        == EXPECTED_COLLISION_CHARTS,
        "Round121 exact seed/path root",
    )

    endpoints = r121["pullback_endpoint_rows"]
    require(
        type(endpoints) is list
        and len(endpoints) == 23
        and r121["pullback_endpoint_rows_sha256"] == digest(endpoints),
        "Round121 endpoint aggregate",
    )
    endpoint_index: dict[tuple[int, int], dict[str, Any]] = {}
    previous_upper: Q | None = None
    actual_order: list[tuple[int, int]] = []
    for endpoint in endpoints:
        validate_hashed_row(
            endpoint, "Round121 pullback endpoint", "evidence_sha256"
        )
        stage = endpoint["stage"]
        natural = endpoint["natural_index_j"]
        require(
            type(stage) is int
            and type(natural) is int
            and stage in (1, 2)
            and 1 <= natural <= (6 if stage == 1 else 17)
            and (stage, natural) not in endpoint_index,
            "Round121 endpoint index",
        )
        expected_id = "round121-pullback-endpoint:" + digest(
            [
                "round121-pullback-endpoint-v1",
                EXACT_SEED_ID,
                f"U{stage}(x)={natural}*delta",
                stage,
                natural,
            ]
        )
        require(
            endpoint["endpoint_id"] == expected_id
            and endpoint["exact_parent_W_seed_id"] == EXACT_SEED_ID
            and endpoint["exact_root_equation_id"]
            == f"round121-U{stage}-equals-{natural}-delta"
            and endpoint["exact_root_equation"]
            == f"U{stage}(x)={natural}*10^-90"
            and endpoint["left_function_sign"] == -1
            and endpoint["right_function_sign"] == 1
            and endpoint["derivative_sign"] == 1
            and endpoint["unique_root_certified"] is True
            and endpoint[
                "numeric_bracket_or_Arb_text_participates_in_endpoint_ID"
            ]
            is False,
            "Round121 endpoint stable semantics",
        )
        bracket = endpoint["x_dyadic_bracket"]
        require(
            type(bracket) is list and len(bracket) == 2,
            "Round121 endpoint bracket",
        )
        lower, upper = Q(bracket[0]), Q(bracket[1])
        width = Q(endpoint["x_bracket_width_upper"])
        require(
            Q(0) < lower < upper < Q(1)
            and upper - lower == width
            and width == Q(1, 2**200),
            "Round121 exact dyadic endpoint bracket",
        )
        if previous_upper is not None:
            require(lower - previous_upper > Q(1, 200), "endpoint separation")
        previous_upper = upper
        endpoint_index[(stage, natural)] = endpoint
        actual_order.append((stage, natural))
    require(actual_order == EXPECTED_CUT_ORDER, "independent pullback cut order")
    require(
        set(endpoint_index)
        == {(1, index) for index in range(1, 7)}
        | {(2, index) for index in range(1, 18)},
        "complete endpoint index universe",
    )

    left_boundary = source_boundary_id("left")
    right_boundary = source_boundary_id("right")
    expected_recuts: list[dict[str, Any]] = []
    counts = (1, 7, 18)
    for stage, count in enumerate(counts):
        for natural in range(count):
            lower_endpoint = (
                left_boundary
                if natural == 0
                else endpoint_index[(stage, natural)]["endpoint_id"]
            )
            upper_endpoint = (
                right_boundary
                if natural == count - 1
                else endpoint_index[(stage, natural + 1)]["endpoint_id"]
            )
            normalized = Q(9, 10)
            if natural == count - 1 and stage == 1:
                normalized = Q(4, 5)
            if natural == count - 1 and stage == 2:
                normalized = Q(2, 5)
            row = {
                "recut_instance_id": recut_instance_id(stage, natural),
                "exact_parent_W_seed_id": EXACT_SEED_ID,
                "stage": stage,
                "natural_index_j": natural,
                "adapted_coordinate_id":
                    "source-u0-exact-delta-x"
                    if stage == 0
                    else f"image-U{stage}",
                "adapted_lower": "0" if stage == 0 else f"{natural}e-90",
                "adapted_upper":
                    "1e-90"
                    if stage == 0
                    else (
                        f"{natural + 1}e-90"
                        if natural < count - 1
                        else f"U{stage}(1)"
                    ),
                "adapted_length_upper": "1e-90",
                "normalized_adapted_length_strict_lower": qstr(normalized),
                "lower_endpoint_id": lower_endpoint,
                "upper_endpoint_id": upper_endpoint,
                "lower_closed": True,
                "upper_closed": False,
                "source_parent_right_endpoint_is_open": True,
                "internal_cut_owned_by_right_natural_cell": True,
                "official_word_key_id": word_ids[stage],
                "roof_level_count": STAGE_RETURN_LENGTH[stage],
                "actual_materialized_input_recut": True,
            }
            row["row_sha256"] = digest(row)
            expected_recuts.append(row)
    require(
        len(expected_recuts) == 26
        and r121["stage_recut_rows_sha256"] == digest(r121["stage_recut_rows"])
        and r121["stage_recut_rows"] == expected_recuts,
        "independent reconstruction of 26 materialized recuts",
    )
    recut_index = {
        (row["stage"], row["natural_index_j"]): row["recut_instance_id"]
        for row in expected_recuts
    }

    boundary_rows: list[dict[str, Any]] = [
        {
            "endpoint_id": left_boundary,
            "x_dyadic_bracket": ["0", "0"],
            "stage": 0,
            "natural_index_j": 0,
        },
        *endpoints,
        {
            "endpoint_id": right_boundary,
            "x_dyadic_bracket": ["1", "1"],
            "stage": 0,
            "natural_index_j": 1,
        },
    ]
    stage_indices = [0, 0, 0]
    expected_children: list[dict[str, Any]] = []
    expected_refined: list[dict[str, Any]] = []
    for rank, (lower, upper) in enumerate(
        zip(boundary_rows, boundary_rows[1:])
    ):
        separation = (
            Q(upper["x_dyadic_bracket"][0])
            - Q(lower["x_dyadic_bracket"][1])
        )
        require(separation > Q(1, 200), "common child positive interval")
        refined_id = "round121-refined-subbranch:" + digest(
            [
                "round121-refined-subbranch-v1",
                OPERATOR_CELL_ID,
                EXACT_SEED_ID,
                "source-k=0",
                rank,
            ]
        )
        child_id = "round121-common-child:" + digest(
            ["round121-common-child-v1", refined_id, EXACT_SEED_ID, rank]
        )
        child = {
            "common_rank": rank,
            "common_child_id": child_id,
            "refined_homogeneous_subbranch_id": refined_id,
            "source_x_lower_endpoint_id": lower["endpoint_id"],
            "source_x_upper_endpoint_id": upper["endpoint_id"],
            "lower_closed": True,
            "upper_closed": False,
            "source_parent_right_endpoint_is_open": True,
            "covering_stage_indices": list(stage_indices),
            "source_recut_instance_id": recut_index[(0, 0)],
            "first_image_recut_instance_id":
                recut_index[(1, stage_indices[1])],
            "second_image_recut_instance_id":
                recut_index[(2, stage_indices[2])],
            "all_three_inputs_contained_in_one_materialized_canonical_cell":
                True,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "official_path_id": PATH_ID,
            "positive_source_x_length_strict_lower": "1/200",
            "actual_standard_curve_child_installed": True,
        }
        child["row_sha256"] = digest(child)
        refined = {
            "refined_homogeneous_subbranch_id": refined_id,
            "common_child_id": child_id,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "exact_parent_W_seed_id": EXACT_SEED_ID,
            "source_adapted_index_k": 0,
            "common_rank": rank,
            "physical_homogeneity": {
                "source": "H0_CENTRAL_OUTER",
                "collision_1": "H0_CENTRAL",
                "collision_2": "H0_CENTRAL",
                "actual_BYPASS_collision_3": "H0_CENTRAL",
                "designated_b3_is_a_collision_angle": False,
            },
        }
        refined["row_sha256"] = digest(refined)
        expected_children.append(child)
        expected_refined.append(refined)
        if rank < len(endpoints):
            crossed_stage = upper["stage"]
            require(crossed_stage in (1, 2), "internal cut stage")
            stage_indices[crossed_stage] += 1
    require(stage_indices == [0, 6, 17], "terminal natural indices")
    require(
        r121["common_refinement_rows_sha256"]
        == digest(r121["common_refinement_rows"])
        and r121["refined_homogeneous_subbranch_rows_sha256"]
        == digest(r121["refined_homogeneous_subbranch_rows"])
        and r121["common_refinement_rows"] == expected_children
        and r121["refined_homogeneous_subbranch_rows"] == expected_refined,
        "independent reconstruction of 24 children and subbranches",
    )
    child_by_id = {row["common_child_id"]: row for row in expected_children}
    refined_by_id = {
        row["refined_homogeneous_subbranch_id"]: row
        for row in expected_refined
    }
    require(
        len(child_by_id) == len(refined_by_id) == 24,
        "24 unique independently rebuilt subbranches",
    )
    return refined_by_id, child_by_id, expected_children, expected_refined


def reaccount_round126(
    r126: dict[str, Any],
    official_words: list[dict[str, Any]],
    refined_by_id: dict[str, dict[str, Any]],
    child_by_id: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str, int], dict[str, Any]],
    list[str],
]:
    maps_raw = r126["preexisting_F1_F17_same_key_map_rows"]
    f18_raw = r126["gate5_F18_slot_rows"]
    require(
        type(maps_raw) is list
        and type(f18_raw) is list
        and len(maps_raw) == len(f18_raw) == 120
        and r126["preexisting_F1_F17_same_key_map_rows_sha256"]
        == digest(maps_raw)
        and r126["gate5_F18_slot_rows_sha256"] == digest(f18_raw),
        "Round126 map/F18 aggregate",
    )
    require(
        r126["rank3_seed_child_field_maturity"] == "18/18"
        and r126["seed_local_complete_18_field_level_block_count"] == 120
        and r126["seed_local_complete_18_field_child_packet_count"] == 24
        and r126["global_complete_18_field_block_count"] == 0
        and r126["complete_18_field_block_count"] == 0
        and r126["gate5_block_count"] == 0
        and r126["gate5_global_maturity"] == "10/18"
        and r126["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round126 safety state",
    )

    word_ids = [word["word_key_id"] for word in official_words]
    word_stage = {word: stage for stage, word in enumerate(word_ids)}
    refined_by_rank = {
        row["common_rank"]: row for row in refined_by_id.values()
    }
    expected_bases = {
        (
            word_ids[stage],
            refined_by_rank[rank]["refined_homogeneous_subbranch_id"],
            roof,
        )
        for rank in range(24)
        for stage in range(3)
        for roof in ROOF_LEVELS_BY_STAGE[stage]
    }
    require(len(expected_bases) == 120, "independent expected base-key set")

    maps: dict[tuple[str, str, int], dict[str, Any]] = {}
    map_ids: set[str] = set()
    source_slot_ids: set[str] = set()
    field_census: Counter[int] = Counter()
    child_census: Counter[str] = Counter()
    stage_census: Counter[int] = Counter()
    carrier_roots: dict[tuple[str, str], tuple[Any, ...]] = {}
    for map_row in maps_raw:
        validate_hashed_row(map_row, "Round126 F1-F17 map")
        base = map_row["immutable_base_key"]
        require(
            type(base) is list
            and len(base) == 3
            and type(base[0]) is str
            and type(base[1]) is str
            and type(base[2]) is int,
            "Round126 base key shape",
        )
        key = (base[0], base[1], base[2])
        stage = map_row["stage"]
        require(
            key in expected_bases
            and key not in maps
            and stage == word_stage[key[0]]
            and key[2] in ROOF_LEVELS_BY_STAGE[stage],
            "Round126 expected unique base key",
        )
        expected_map_id = "round126-preexisting-f1-f17-map:" + digest(
            ["round126-preexisting-f1-f17-map-v1", list(key)]
        )
        require(
            map_row["same_key_map_row_id"] == expected_map_id
            and expected_map_id not in map_ids,
            "Round126 stable map ID",
        )
        refined = refined_by_id[key[1]]
        child = child_by_id[refined["common_child_id"]]
        expected_recut = child[STAGE_RECUT_KEY[stage]]
        require(
            map_row["official_word_key_id"] == key[0]
            and map_row["refined_homogeneous_subbranch_id"] == key[1]
            and map_row["roof_level_j"] == key[2]
            and map_row["common_child_id"] == child["common_child_id"]
            and map_row["common_rank"] == refined["common_rank"]
            and map_row["input_materialized_recut_instance_id"]
            == expected_recut
            and map_row["each_preexisting_field_bound_exactly_once"] is True
            and map_row[
                "all_preexisting_fields_share_child_stage_input_and_operator_carrier"
            ]
            is True,
            "Round126 base root linkage",
        )
        operator_id = map_row["standard_family_leg_operator_row_id"]
        operator_hash = map_row["standard_family_leg_operator_row_sha256"]
        require(
            type(operator_id) is str
            and type(operator_hash) is str
            and len(operator_hash) == 64,
            "Round126 operator carrier identity",
        )
        carrier_key = (key[0], key[1])
        carrier_root = (
            stage,
            child["common_child_id"],
            refined["common_rank"],
            expected_recut,
            operator_id,
            operator_hash,
        )
        if carrier_key in carrier_roots:
            require(
                carrier_roots[carrier_key] == carrier_root,
                "same carrier across symbolic roof splits",
            )
        else:
            carrier_roots[carrier_key] = carrier_root

        bindings = map_row["bound_preexisting_F1_F17_slots"]
        require(
            type(bindings) is list
            and len(bindings) == 17
            and map_row["bound_preexisting_field_count"] == 17
            and map_row["bound_preexisting_field_indices"]
            == list(range(1, 18))
            and map_row["bound_preexisting_F1_F17_slots_sha256"]
            == digest(bindings),
            "Round126 F1-F17 binding aggregate",
        )
        seen_fields: set[int] = set()
        for binding in bindings:
            require(
                type(binding) is dict
                and set(binding)
                == {
                    "field_index",
                    "field_name",
                    "slot_id",
                    "source_certificate_round",
                    "source_slot_canonical_sha256",
                },
                "Round126 closed field binding",
            )
            field = binding["field_index"]
            slot_id = binding["slot_id"]
            require(
                type(field) is int
                and 1 <= field <= 17
                and field not in seen_fields
                and binding["field_name"] == FIELD_NAMES[field]
                and binding["source_certificate_round"]
                == SOURCE_ROUND_BY_FIELD[field]
                and type(slot_id) is str
                and slot_id not in source_slot_ids
                and type(binding["source_slot_canonical_sha256"]) is str
                and len(binding["source_slot_canonical_sha256"]) == 64,
                "Round126 field binding identity",
            )
            seen_fields.add(field)
            source_slot_ids.add(slot_id)
            field_census[field] += 1
        require(seen_fields == set(range(1, 18)), "F1-F17 exactly once")
        maps[key] = map_row
        map_ids.add(expected_map_id)
        child_census[child["common_child_id"]] += 1
        stage_census[stage] += 1
    require(
        set(maps) == expected_bases
        and len(map_ids) == 120
        and len(source_slot_ids) == 2040
        and field_census == Counter({field: 120 for field in range(1, 18)})
        and child_census
        == Counter({child: 5 for child in child_by_id})
        and stage_census == EXPECTED_STAGE_BASE_COUNTS
        and len(carrier_roots) == 72,
        "Round126 independent F1-F17 census",
    )
    require(
        len({root[4] for root in carrier_roots.values()}) == 72
        and len({
            (root[1], root[0]) for root in carrier_roots.values()
        }) == 72,
        "72 unique operator rows on 24 child by 3 stage carriers",
    )

    f18_by_base: dict[tuple[str, str, int], dict[str, Any]] = {}
    f18_slot_ids: set[str] = set()
    for f18 in f18_raw:
        validate_hashed_row(f18, "Round126 F18 row")
        immutable = f18["immutable_slot_key"]
        require(
            type(immutable) is list
            and len(immutable) == 4
            and immutable[3] == FIELD_NAMES[18],
            "Round126 F18 immutable key",
        )
        key = (immutable[0], immutable[1], immutable[2])
        require(
            key in maps
            and key not in f18_by_base
            and f18["slot_id"] not in f18_slot_ids,
            "Round126 unique F18 key",
        )
        expected_slot_id = "round126-gate5-f18-slot:" + digest(
            ["round126-gate5-f18-slot-v1", immutable]
        )
        map_row = maps[key]
        stage = map_row["stage"]
        roof = key[2]
        return_length = STAGE_RETURN_LENGTH[stage]
        suffix = return_length - roof
        require(
            f18["slot_id"] == expected_slot_id
            and f18["official_word_key_id"] == key[0]
            and f18["refined_homogeneous_subbranch_id"] == key[1]
            and f18["roof_level_j"] == roof
            and f18["field_index"] == 18
            and f18["field_name"] == FIELD_NAMES[18]
            and f18["common_child_id"] == map_row["common_child_id"]
            and f18["common_rank"] == map_row["common_rank"]
            and f18["stage"] == stage
            and f18["input_materialized_recut_instance_id"]
            == map_row["input_materialized_recut_instance_id"]
            and f18["standard_family_leg_operator_row_id"]
            == map_row["standard_family_leg_operator_row_id"]
            and f18["standard_family_leg_operator_row_sha256"]
            == map_row["standard_family_leg_operator_row_sha256"]
            and f18["preexisting_F1_F17_same_key_map_row_id"]
            == map_row["same_key_map_row_id"]
            and f18["preexisting_F1_F17_same_key_map_row_sha256"]
            == map_row["row_sha256"],
            "Round126 F18 same-root linkage",
        )
        require(
            f18["stage_return_length_r"] == return_length
            and f18["prefix_length_j"] == roof
            and f18["suffix_length_r_minus_j"] == suffix
            and f18["prefix_operator_monomial"] == f"z^{roof}"
            and f18["suffix_operator_monomial"] == f"z^{suffix}"
            and f18["stage_block_operator_monomial"]
            == f"z^{return_length}"
            and f18["prefix_suffix_block_identity"]
            == f"z^{roof}*z^{suffix}=z^{return_length}"
            and f18["field_bound_semantics"] == "STRUCTURAL_REGISTRATION"
            and f18["structural_registration_only"] is True
            and f18["operator_Wiener_invertibility_claimed"] is False
            and f18["operator_Wiener_aperiodicity_claimed"] is False
            and f18["Kac_closure_claimed"] is False
            and f18["global_operator_phase_block_claimed"] is False
            and f18["CM2_claimed"] is False,
            "Round126 structural-only F18 arithmetic and nonpromotion",
        )
        f18_by_base[key] = f18
        f18_slot_ids.add(f18["slot_id"])
    require(
        set(f18_by_base) == expected_bases
        and len(f18_slot_ids) == 120
        and source_slot_ids.isdisjoint(f18_slot_ids),
        "Round126 complete disjoint F1-F18 census",
    )

    ordered_keys = sorted(
        expected_bases,
        key=lambda key: (
            maps[key]["common_rank"],
            maps[key]["stage"],
            key[2],
        ),
    )
    all_slot_ids = [
        slot_id
        for key in ordered_keys
        for slot_id in (
            [
                binding["slot_id"]
                for binding in maps[key]["bound_preexisting_F1_F17_slots"]
            ]
            + [f18_by_base[key]["slot_id"]]
        )
    ]
    require(
        len(all_slot_ids) == len(set(all_slot_ids)) == 2160,
        "2160 unique base-major field slots",
    )
    return [maps[key] for key in ordered_keys], f18_by_base, all_slot_ids


def base_crosswalk_id(base: tuple[str, str, int]) -> str:
    return row_id("round127-seed-local-base-key", list(base))


def carrier_crosswalk_id(word: str, subbranch: str) -> str:
    return row_id("round127-word-subbranch-carrier", [word, subbranch])


def build_base_crosswalk_rows(
    map_rows: list[dict[str, Any]],
    f18_by_base: dict[tuple[str, str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for map_row in map_rows:
        base_list = map_row["immutable_base_key"]
        base = (base_list[0], base_list[1], base_list[2])
        f18 = f18_by_base[base]
        bindings = [
            {
                "field_index": binding["field_index"],
                "field_name": binding["field_name"],
                "slot_id": binding["slot_id"],
                "source_certificate_round":
                    binding["source_certificate_round"],
                "source_slot_canonical_sha256":
                    binding["source_slot_canonical_sha256"],
            }
            for binding in map_row["bound_preexisting_F1_F17_slots"]
        ]
        bindings.append(
            {
                "field_index": 18,
                "field_name": FIELD_NAMES[18],
                "slot_id": f18["slot_id"],
                "source_certificate_round": 126,
                "source_slot_canonical_sha256": f18["row_sha256"],
            }
        )
        require(
            [binding["field_index"] for binding in bindings]
            == list(range(1, 19)),
            "ordered F1-F18 bindings",
        )
        row = {
            "seed_local_base_key_crosswalk_id": base_crosswalk_id(base),
            "immutable_seed_local_base_key": list(base),
            "official_word_key_id": base[0],
            "refined_homogeneous_subbranch_id": base[1],
            "roof_level_j": base[2],
            "stage": map_row["stage"],
            "stage_return_length_r": STAGE_RETURN_LENGTH[map_row["stage"]],
            "common_child_id": map_row["common_child_id"],
            "common_rank": map_row["common_rank"],
            "input_materialized_recut_instance_id":
                map_row["input_materialized_recut_instance_id"],
            "word_subbranch_operator_carrier_crosswalk_id":
                carrier_crosswalk_id(base[0], base[1]),
            "standard_family_leg_operator_row_id":
                map_row["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256":
                map_row["standard_family_leg_operator_row_sha256"],
            "round126_preexisting_F1_F17_same_key_map_row_id":
                map_row["same_key_map_row_id"],
            "round126_preexisting_F1_F17_same_key_map_row_sha256":
                map_row["row_sha256"],
            "round126_F18_slot_id": f18["slot_id"],
            "round126_F18_slot_row_sha256": f18["row_sha256"],
            "field_slot_bindings": bindings,
            "field_slot_bindings_sha256": digest(bindings),
            "field_indices_exactly_once": list(range(1, 19)),
            "field_slot_count": 18,
            "all_18_fields_share_word_subbranch_roof_child_stage_recut_and_operator_carrier":
                True,
            "scope": "ROUND121_EXACT_SEED_LOCAL_LEVEL_ONLY",
            "global_level_or_block_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["seed_local_base_key_crosswalk_id"] for row in rows})
        == 120,
        "120 base crosswalk rows",
    )
    return rows


def build_carrier_crosswalk_rows(
    base_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for base in base_rows:
        grouped[
            (
                base["official_word_key_id"],
                base["refined_homogeneous_subbranch_id"],
            )
        ].append(base)
    require(len(grouped) == 72, "72 independently grouped carriers")
    rows: list[dict[str, Any]] = []
    for (word, subbranch), levels in grouped.items():
        levels.sort(key=lambda row: row["roof_level_j"])
        first = levels[0]
        stage = first["stage"]
        roofs = [row["roof_level_j"] for row in levels]
        require(roofs == ROOF_LEVELS_BY_STAGE[stage], "carrier roof census")
        invariant_keys = (
            "stage",
            "common_child_id",
            "common_rank",
            "input_materialized_recut_instance_id",
            "standard_family_leg_operator_row_id",
            "standard_family_leg_operator_row_sha256",
        )
        require(
            all(
                all(level[key] == first[key] for key in invariant_keys)
                for level in levels
            ),
            "carrier invariant root",
        )
        row = {
            "word_subbranch_operator_carrier_crosswalk_id":
                carrier_crosswalk_id(word, subbranch),
            "official_word_key_id": word,
            "refined_homogeneous_subbranch_id": subbranch,
            "stage": stage,
            "stage_return_length_r": STAGE_RETURN_LENGTH[stage],
            "roof_level_js": roofs,
            "common_child_id": first["common_child_id"],
            "common_rank": first["common_rank"],
            "input_materialized_recut_instance_id":
                first["input_materialized_recut_instance_id"],
            "standard_family_leg_operator_row_id":
                first["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256":
                first["standard_family_leg_operator_row_sha256"],
            "seed_local_base_key_crosswalk_ids": [
                level["seed_local_base_key_crosswalk_id"]
                for level in levels
            ],
            "seed_local_base_key_count": len(levels),
            "seed_local_field_slot_count": 18 * len(levels),
            "one_operator_carrier_shared_across_its_symbolic_roof_splits":
                True,
            "scope": "ONE_WORD_ON_ONE_ROUND121_EXACT_SEED_SUBBRANCH",
            "global_physical_carrier_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    rows.sort(key=lambda row: (row["common_rank"], row["stage"]))
    require(
        len(rows) == 72
        and len({
            row["word_subbranch_operator_carrier_crosswalk_id"]
            for row in rows
        }) == 72
        and Counter(row["stage"] for row in rows)
        == Counter({0: 24, 1: 24, 2: 24}),
        "72 carrier row census",
    )
    return rows


def build_subbranch_crosswalk_rows(
    refined_by_id: dict[str, dict[str, Any]],
    child_by_id: dict[str, dict[str, Any]],
    carrier_rows: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    carriers_by_subbranch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bases_by_subbranch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for carrier in carrier_rows:
        carriers_by_subbranch[
            carrier["refined_homogeneous_subbranch_id"]
        ].append(carrier)
    for base in base_rows:
        bases_by_subbranch[
            base["refined_homogeneous_subbranch_id"]
        ].append(base)
    rows: list[dict[str, Any]] = []
    for subbranch, refined in refined_by_id.items():
        child = child_by_id[refined["common_child_id"]]
        carriers = sorted(
            carriers_by_subbranch[subbranch], key=lambda row: row["stage"]
        )
        bases = sorted(
            bases_by_subbranch[subbranch],
            key=lambda row: (row["stage"], row["roof_level_j"]),
        )
        require(
            [row["stage"] for row in carriers] == [0, 1, 2]
            and len(bases) == 5
            and sum(row["field_slot_count"] for row in bases) == 90,
            "per-subbranch carrier/base/slot census",
        )
        row = {
            "refined_subbranch_crosswalk_id":
                row_id("round127-refined-subbranch", subbranch),
            "refined_homogeneous_subbranch_id": subbranch,
            "common_child_id": refined["common_child_id"],
            "common_rank": refined["common_rank"],
            "exact_parent_W_seed_id": EXACT_SEED_ID,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "round121_refined_subbranch_row_sha256": refined["row_sha256"],
            "round121_common_child_row_sha256": child["row_sha256"],
            "physical_homogeneity": refined["physical_homogeneity"],
            "word_subbranch_operator_carrier_crosswalk_ids": [
                carrier["word_subbranch_operator_carrier_crosswalk_id"]
                for carrier in carriers
            ],
            "seed_local_base_key_crosswalk_ids": [
                base["seed_local_base_key_crosswalk_id"] for base in bases
            ],
            "word_subbranch_operator_carrier_count": 3,
            "seed_local_base_key_count": 5,
            "seed_local_field_slot_count": 90,
            "child_interval_ownership": "[lower,upper)",
            "scope": "ONE_ROUND121_EXACT_SEED_COMMON_CHILD",
            "global_homogeneous_subbranch_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    rows.sort(key=lambda row: row["common_rank"])
    require(
        len(rows) == 24
        and [row["common_rank"] for row in rows] == list(range(24)),
        "24 subbranch crosswalk row census",
    )
    return rows


def build_word_crosswalk_rows(
    legs: list[dict[str, Any]],
    carrier_rows: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    carriers_by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bases_by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for carrier in carrier_rows:
        carriers_by_word[carrier["official_word_key_id"]].append(carrier)
    for base in base_rows:
        bases_by_word[base["official_word_key_id"]].append(base)
    rows: list[dict[str, Any]] = []
    for leg in legs:
        stage = leg["stage"]
        official = leg["official"]
        word = official["word_key_id"]
        carriers = sorted(
            carriers_by_word[word], key=lambda row: row["common_rank"]
        )
        bases = sorted(
            bases_by_word[word],
            key=lambda row: (row["common_rank"], row["roof_level_j"]),
        )
        return_length = official["row"][3]
        require(
            len(carriers) == 24
            and len(bases) == 24 * return_length
            and all(carrier["stage"] == stage for carrier in carriers)
            and all(base["stage"] == stage for base in bases),
            "per-word incidence census",
        )
        row = {
            "official_word_registry_incidence_row_id":
                row_id("round127-official-word-registry-incidence", word),
            "path_position_zero_based": stage,
            "stage": stage,
            "official_word_key_id": word,
            "global_candidate_registry_ordinal_zero_based":
                official["ordinal_zero_based"],
            "retained_chart_target_pair_ordinal_zero_based":
                leg["retained_pair_ordinal"],
            "crossing_pattern_ordinal_zero_based": leg["pattern_ordinal"],
            "global_word_row": official["row"],
            "global_word_row_sha256": official["row_sha256"],
            "source_normal_chart": official["row"][0],
            "relative_registry_target_id":
                leg["relative_registry_target_id"],
            "absolute_physical_owner_id": leg["absolute_owner_id"],
            "relative_registry_target_and_absolute_owner_are_distinct_namespaces":
                True,
            "ordered_clean_wall_record": official["row"][2],
            "selected_collision_chart": leg["selected_collision_chart"],
            "return_length_r": return_length,
            "symbolic_roof_level_js": list(range(return_length)),
            "global_registry_membership_basis":
                "PINNED_ROUND113_OFFICIAL_WORD_ROW_AND_GLOBAL_STREAM_DIGEST",
            "word_subbranch_operator_carrier_crosswalk_ids": [
                carrier["word_subbranch_operator_carrier_crosswalk_id"]
                for carrier in carriers
            ],
            "seed_local_base_key_crosswalk_ids": [
                base["seed_local_base_key_crosswalk_id"] for base in bases
            ],
            "round121_exact_seed_refined_subbranch_incidence_count": 24,
            "round126_word_subbranch_operator_carrier_count": 24,
            "round126_seed_local_base_key_count": len(bases),
            "round126_seed_local_field_slot_count": 18 * len(bases),
            "complete_global_domain_decision_claimed": False,
            "global_physical_coverage_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows) == 3
        and sum(len(row["symbolic_roof_level_js"]) for row in rows) == 5
        and sum(
            row["round126_word_subbranch_operator_carrier_count"]
            for row in rows
        ) == 72
        and sum(row["round126_seed_local_base_key_count"] for row in rows)
        == 120
        and sum(row["round126_seed_local_field_slot_count"] for row in rows)
        == 2160,
        "three-word incidence totals",
    )
    return rows


def expected_result() -> tuple[dict[str, Any], dict[str, Any]]:
    global_result, documents, replay = load_inputs()
    r113 = documents[ROUND113.name]["result"]
    r117 = documents[ROUND117.name]["result"]
    r121 = documents[ROUND121.name]["result"]
    r126 = documents[ROUND126.name]["result"]

    _cell, legs = exact_path_inputs(r113, replay)
    word_ids = [leg["official"]["word_key_id"] for leg in legs]
    _parent117 = validate_round117_join(r117, word_ids)
    refined_by_id, child_by_id, _children, _refined = (
        rebuild_round121_subbranches(r121, word_ids)
    )
    map_rows, f18_by_base, all_slot_ids = reaccount_round126(
        r126,
        replay["official_words"],
        refined_by_id,
        child_by_id,
    )
    base_rows = build_base_crosswalk_rows(map_rows, f18_by_base)
    carrier_rows = build_carrier_crosswalk_rows(base_rows)
    subbranch_rows = build_subbranch_crosswalk_rows(
        refined_by_id, child_by_id, carrier_rows, base_rows
    )
    word_rows = build_word_crosswalk_rows(legs, carrier_rows, base_rows)

    base_stage_counts = Counter(row["stage"] for row in base_rows)
    slot_field_counts = Counter(
        binding["field_index"]
        for base in base_rows
        for binding in base["field_slot_bindings"]
    )
    require(
        base_stage_counts == EXPECTED_STAGE_BASE_COUNTS
        and slot_field_counts
        == Counter({field: 120 for field in range(1, 19)}),
        "final stage/field census",
    )
    certificate_input_names = (
        GLOBAL_MANIFEST.name,
        ROUND113.name,
        ROUND113_VERIFICATION.name,
        ROUND117.name,
        ROUND117_VERIFICATION.name,
        ROUND121.name,
        ROUND121_VERIFICATION.name,
        ROUND126.name,
        ROUND126_VERIFICATION.name,
    )
    certificate_byte_pins = {
        name: BYTE_PINS[name] for name in sorted(certificate_input_names)
    }
    certificate_result_pins = dict(sorted(RESULT_PINS.items()))
    global_registry = global_result["immutable_candidate_key_registry"]
    global_roof_count = global_registry[
        "prefix_suffix_factor_contract"
    ]["roof_level_prefix_suffix_factor_pair_count"]
    result = {
        "status": "REGISTRY_MEMBERSHIP_AND_SEED_LOCAL_SLOT_CENSUS",
        "symbolic_registry_incidence": {
            "terminology":
                "MEMBERSHIP_AND_INCIDENCE_NOT_DOMAIN_MEASURE_OR_PHYSICAL_COVERAGE",
            "global_symbolic_candidate_word_key_count": 441280,
            "exact_seed_path_referenced_unique_word_key_count": 3,
            "word_key_registry_incidence_fraction": "3/441280",
            "word_keys_unjoined_to_this_exact_seed_path_incidence": 441277,
            "unjoined_word_semantics":
                "not present in this exact-seed path incidence; no emptiness or uncovered-domain conclusion",
            "global_symbolic_word_roof_position_count": global_roof_count,
            "exact_seed_path_referenced_unique_symbolic_word_roof_position_count":
                5,
            "word_roof_registry_incidence_fraction": "5/3286976",
            "word_roof_positions_unjoined_to_this_exact_seed_path_incidence":
                3286971,
            "unjoined_word_roof_semantics":
                "not present in this exact-seed path incidence; no physical coverage conclusion",
            "round126_seed_local_word_subbranch_roof_base_key_count": 120,
            "seed_local_base_keys_are_not_divided_by_global_word_roof_positions":
                True,
            "reason_120_has_no_global_incidence_denominator":
                "each local base key includes one of 24 Round121 exact-seed refined subbranches",
            "global_exact_nonempty_candidate_key_count":
                global_registry["exact_nonempty_candidate_key_count"],
            "global_complete_nonempty_or_empty_domain_decisions": False,
            "global_physical_or_measure_coverage_claimed": False,
        },
        "exact_path_root_contract": {
            "round113_parent_cell_id": PARENT_ID,
            "round113_parent_sheet_id": SHEET_ID,
            "round113_official_path_id": PATH_ID,
            "round113_branch_key": EXPECTED_BRANCH,
            "round113_ordered_absolute_owner_ids": EXPECTED_OWNERS,
            "round113_relative_registry_target_ids":
                EXPECTED_RELATIVE_TARGETS,
            "round113_selected_collision_charts":
                EXPECTED_COLLISION_CHARTS,
            "second_leg_relative_registry_target_id": "G[1,1]",
            "second_leg_absolute_owner_id": "G[0,0]",
            "second_leg_relative_target_is_not_relabelled_as_absolute_owner":
                True,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "round117_family":
                "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0",
            "round121_exact_parent_W_seed_id": EXACT_SEED_ID,
            "round121_actual_common_child_count": 24,
            "round121_refined_homogeneous_subbranch_count": 24,
            "stage_return_lengths": {"0": 2, "1": 1, "2": 2},
            "stage_symbolic_roof_levels":
                {"0": [0, 1], "1": [0], "2": [0, 1]},
        },
        "exact_path_official_word_registry_incidence_rows": word_rows,
        "exact_path_official_word_registry_incidence_rows_sha256":
            digest(word_rows),
        "seed_local_refined_subbranch_crosswalk_rows": subbranch_rows,
        "seed_local_refined_subbranch_crosswalk_rows_sha256":
            digest(subbranch_rows),
        "word_subbranch_operator_carrier_crosswalk_rows": carrier_rows,
        "word_subbranch_operator_carrier_crosswalk_rows_sha256":
            digest(carrier_rows),
        "seed_local_base_key_crosswalk_rows": base_rows,
        "seed_local_base_key_crosswalk_rows_sha256": digest(base_rows),
        "slot_census": {
            "round126_preexisting_F1_F17_slot_count": 2040,
            "round126_F18_slot_count": 120,
            "round126_total_seed_local_slot_count": 2160,
            "round127_materialized_slot_binding_count": sum(
                row["field_slot_count"] for row in base_rows
            ),
            "round127_base_major_all_slot_ids_sha256": digest(
                [
                    binding["slot_id"]
                    for base in base_rows
                    for binding in base["field_slot_bindings"]
                ]
            ),
            "round126_validated_unique_slot_id_count": len(set(all_slot_ids)),
            "slot_count_per_field": {
                str(field): slot_field_counts[field]
                for field in range(1, 19)
            },
            "all_18_fields_exactly_once_on_each_of_120_seed_local_base_keys":
                True,
            "all_fields_share_same_word_subbranch_roof_child_stage_recut_and_operator_carrier_per_base":
                True,
        },
        "count_ledger": {
            "exact_path_count": 1,
            "exact_path_unique_official_word_count": 3,
            "exact_path_symbolic_word_roof_position_count": 5,
            "round121_exact_seed_common_child_count": 24,
            "round121_exact_seed_refined_subbranch_count": 24,
            "word_subbranch_operator_carrier_count": 72,
            "word_subbranch_operator_carrier_stage_counts":
                {"0": 24, "1": 24, "2": 24},
            "seed_local_base_key_count": 120,
            "seed_local_base_key_stage_counts":
                {"0": 48, "1": 24, "2": 48},
            "seed_local_field_slot_count": 2160,
            "seed_local_field_slot_count_per_field": 120,
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
        },
        "root_separation_and_nonpromotion": {
            "symbolic_global_registry_root":
                "441280 candidate word keys; empty fibres allowed; no materialized homogeneous subbranches",
            "round113_root":
                "one verified regular relative-interior rank-three path on one endpoint-sheet cell",
            "round117_root":
                "one nonempty source/operator-cell sample inherited from the Round113 parent",
            "round121_root":
                "one exact rational-anchor parent-W seed with 24 half-open common children",
            "round126_root":
                "120 exact-seed local word/subbranch/roof levels and their structural direct-standard-N carriers",
            "installed_identifications": [
                "the three Round113 official word IDs and rows are pinned symbolic-registry members",
                "Round117 inherits the same Round113 parent, path, and three word IDs",
                "Round121 pins the Round113 parent and Round117 operator-cell sample",
                "Round126 pins the same three words on all 24 Round121 refined subbranches",
                "each of 120 seed-local base keys binds F1 through F18 exactly once",
            ],
            "forbidden_identifications": [
                "seed-local refined subbranch is not a global homogeneous-subbranch registry entry",
                "seed-local level block is not a global physical complete block",
                "24 derived child packets are not materialized global blocks",
                "symbolic word membership is not a full D_w domain decision",
                "symbolic word/roof incidence is not domain, measure, or physical coverage",
                "relative registry target IDs are not absolute physical owner IDs",
            ],
        },
        "global_safety_state": {
            "rank3_seed_child_field_maturity": "18/18",
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_status": "NOT_CERTIFIED",
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "strict_scope": (
            "symbolic-registry membership for the three-word Round113 path and "
            "an exact census/crosswalk of its Round121--Round126 one-seed local "
            "subbranches, carriers, base keys, and field slots"
        ),
        "strict_nonclaims": [
            "no complete nonempty-or-empty decision for all 441280 candidate word domains",
            "no claim that the three referenced D_w are covered maximally or over their full parameter fibres",
            "no all-homogeneity-subbranch or all-parameter-fibre registry",
            "no arbitrary-return-depth or all-Borel-key physical registration",
            "no domain, measure, probability, or physical coverage ratio",
            "no division of 120 seed-local base keys by 3286976 global symbolic word-roof positions",
            "no claim that five symbolic roof positions are five collisions",
            "no global inverse-Jacobian or all-record distortion theorem",
            "no global dynamic-test embedding or common strong recipient",
            "no global raw-Z, power-Orlicz, owner-drift, or positive all-time cemetery theorem",
            "no global all-input oriented vector-current recipient",
            "no operator Wiener invertibility or aperiodicity theorem",
            "no Kac return-wide closure theorem",
            "no global complete 18-field block",
            "no global Gate5 maturity upgrade",
            "no CM2 claim",
        ],
        "upstream_artifact_byte_pins": certificate_byte_pins,
        "upstream_closed_result_sha256_pins": certificate_result_pins,
        "global_manifest_embedded_pins": {
            "producer_sha256": BYTE_PINS[GLOBAL_PRODUCER.name],
            "verifier_sha256": BYTE_PINS[GLOBAL_VERIFIER.name],
            "candidate_word_rows_stream_sha256": GLOBAL_STREAM_SHA256,
            "required_18_field_schema_sha256":
                GLOBAL_FIELD_SCHEMA_SHA256,
        },
    }
    audit = {
        "global_registry_replay": {
            key: value for key, value in replay.items() if key != "official_words"
        },
        "official_word_ids": word_ids,
        "official_word_ordinals":
            [word["ordinal_zero_based"] for word in replay["official_words"]],
        "second_leg_relative_registry_target_id": "G[1,1]",
        "second_leg_absolute_owner_id": "G[0,0]",
        "independently_rebuilt_child_count": len(child_by_id),
        "independently_rebuilt_refined_subbranch_count": len(refined_by_id),
        "independently_grouped_carrier_count": len(carrier_rows),
        "independently_rebuilt_base_key_count": len(base_rows),
        "independently_reaccounted_slot_count": len(all_slot_ids),
        "field_slot_count_per_field": {
            str(field): slot_field_counts[field] for field in range(1, 19)
        },
    }
    return result, audit


def evaluate_document(
    document: Any, expected: dict[str, Any]
) -> dict[str, Any]:
    require(type(document) is dict, "certificate top object")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate closed envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result object")
    require(
        document["result_sha256"] == digest(result),
        "certificate result digest",
    )
    require(set(result) == set(expected), "certificate result closed schema")

    row_specs = (
        (
            "exact_path_official_word_registry_incidence_rows",
            "exact_path_official_word_registry_incidence_rows_sha256",
            3,
        ),
        (
            "seed_local_refined_subbranch_crosswalk_rows",
            "seed_local_refined_subbranch_crosswalk_rows_sha256",
            24,
        ),
        (
            "word_subbranch_operator_carrier_crosswalk_rows",
            "word_subbranch_operator_carrier_crosswalk_rows_sha256",
            72,
        ),
        (
            "seed_local_base_key_crosswalk_rows",
            "seed_local_base_key_crosswalk_rows_sha256",
            120,
        ),
    )
    for rows_key, aggregate_key, expected_count in row_specs:
        rows = result[rows_key]
        require(
            type(rows) is list and len(rows) == expected_count,
            f"certificate row count:{rows_key}",
        )
        for index, row in enumerate(rows):
            validate_hashed_row(row, f"{rows_key}:{index}")
        require(
            result[aggregate_key] == digest(rows),
            f"certificate aggregate:{rows_key}",
        )

    word_rows = result["exact_path_official_word_registry_incidence_rows"]
    require(
        [row["global_candidate_registry_ordinal_zero_based"] for row in word_rows]
        == EXPECTED_WORD_ORDINALS
        and word_rows[1]["relative_registry_target_id"] == "G[1,1]"
        and word_rows[1]["absolute_physical_owner_id"] == "G[0,0]"
        and word_rows[1]["relative_registry_target_id"]
        != word_rows[1]["absolute_physical_owner_id"],
        "certificate official word/namespace audit",
    )
    base_rows = result["seed_local_base_key_crosswalk_rows"]
    base_ids: set[str] = set()
    immutable_bases: set[str] = set()
    slot_ids: set[str] = set()
    field_census: Counter[int] = Counter()
    for row in base_rows:
        base_id = row["seed_local_base_key_crosswalk_id"]
        immutable = canonical(row["immutable_seed_local_base_key"])
        require(
            base_id not in base_ids and immutable not in immutable_bases,
            "certificate unique base crosswalk",
        )
        base_ids.add(base_id)
        immutable_bases.add(immutable)
        bindings = row["field_slot_bindings"]
        require(
            type(bindings) is list
            and len(bindings) == 18
            and row["field_slot_bindings_sha256"] == digest(bindings)
            and [binding["field_index"] for binding in bindings]
            == list(range(1, 19))
            and row["field_indices_exactly_once"] == list(range(1, 19))
            and row["field_slot_count"] == 18,
            "certificate exact-once base bindings",
        )
        for binding in bindings:
            field = binding["field_index"]
            slot_id = binding["slot_id"]
            require(
                type(slot_id) is str
                and slot_id not in slot_ids
                and binding["field_name"] == FIELD_NAMES[field]
                and binding["source_certificate_round"]
                == SOURCE_ROUND_BY_FIELD[field],
                "certificate unique typed slot binding",
            )
            slot_ids.add(slot_id)
            field_census[field] += 1
    require(
        len(base_ids) == len(immutable_bases) == 120
        and len(slot_ids) == 2160
        and field_census == Counter({field: 120 for field in range(1, 19)}),
        "certificate 120 by 18 slot census",
    )
    require(result == expected, "independent exact reconstruction")

    return {
        "official_word_registry_incidence_row_count": len(word_rows),
        "refined_subbranch_crosswalk_row_count":
            len(result["seed_local_refined_subbranch_crosswalk_rows"]),
        "word_subbranch_operator_carrier_crosswalk_row_count":
            len(result["word_subbranch_operator_carrier_crosswalk_rows"]),
        "seed_local_base_key_crosswalk_row_count": len(base_rows),
        "seed_local_field_slot_count": len(slot_ids),
        "slot_count_per_field": {
            str(field): field_census[field] for field in range(1, 19)
        },
        "seed_local_complete_18_field_level_block_count":
            result["global_safety_state"][
                "seed_local_complete_18_field_level_block_count"
            ],
        "seed_local_complete_18_field_child_packet_count":
            result["global_safety_state"][
                "seed_local_complete_18_field_child_packet_count"
            ],
        "gate5_global_maturity":
            result["global_safety_state"]["gate5_global_maturity"],
        "global_complete_18_field_block_count":
            result["global_safety_state"][
                "global_complete_18_field_block_count"
            ],
        "complete_18_field_block_count":
            result["global_safety_state"]["complete_18_field_block_count"],
        "gate5_block_count":
            result["global_safety_state"]["gate5_block_count"],
        "gate5_status": result["global_safety_state"]["gate5_status"],
        "cm2_verdict": result["global_safety_state"]["cm2_verdict"],
    }


def evaluate_bytes(raw: bytes, expected: dict[str, Any]) -> dict[str, Any]:
    return evaluate_document(parse_strict_bytes(raw), expected)


def resign_document(document: dict[str, Any]) -> None:
    result = document.get("result")
    if type(result) is not dict:
        return
    row_specs = (
        (
            "exact_path_official_word_registry_incidence_rows",
            "exact_path_official_word_registry_incidence_rows_sha256",
        ),
        (
            "seed_local_refined_subbranch_crosswalk_rows",
            "seed_local_refined_subbranch_crosswalk_rows_sha256",
        ),
        (
            "word_subbranch_operator_carrier_crosswalk_rows",
            "word_subbranch_operator_carrier_crosswalk_rows_sha256",
        ),
        (
            "seed_local_base_key_crosswalk_rows",
            "seed_local_base_key_crosswalk_rows_sha256",
        ),
    )
    for rows_key, aggregate_key in row_specs:
        rows = result.get(rows_key)
        if type(rows) is not list:
            continue
        for row in rows:
            if type(row) is not dict:
                continue
            bindings = row.get("field_slot_bindings")
            if type(bindings) is list:
                row["field_slot_bindings_sha256"] = digest(bindings)
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {
                        key: value
                        for key, value in row.items()
                        if key != "row_sha256"
                    }
                )
        result[aggregate_key] = digest(rows)
    document["result_sha256"] = digest(result)


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def delete_path(root: Any, path: tuple[Any, ...]) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    del target[path[-1]]


def semantic_mutations(
    document: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        (
            "schema swap",
            lambda d: set_path(d, ("schema",), "cm2.round127.invalid"),
        ),
        (
            "missing result field",
            lambda d: delete_path(d, ("result", "strict_scope")),
        ),
        (
            "unknown result field",
            lambda d: set_path(d, ("result", "unexpected"), True),
        ),
        (
            "status promoted to physical coverage",
            lambda d: set_path(
                d, ("result", "status"), "GLOBAL_PHYSICAL_COVERAGE_CERTIFIED"
            ),
        ),
        (
            "word incidence promoted to coverage terminology",
            lambda d: set_path(
                d,
                ("result", "symbolic_registry_incidence", "terminology"),
                "PHYSICAL_COVERAGE",
            ),
        ),
        (
            "global physical coverage claimed",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "global_physical_or_measure_coverage_claimed",
                ),
                True,
            ),
        ),
        (
            "global domain decisions falsely completed",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "global_complete_nonempty_or_empty_domain_decisions",
                ),
                True,
            ),
        ),
        (
            "unknown nonempty census promoted to three",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "global_exact_nonempty_candidate_key_count",
                ),
                3,
            ),
        ),
        (
            "120 local bases assigned global denominator",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "seed_local_base_keys_are_not_divided_by_global_word_roof_positions",
                ),
                False,
            ),
        ),
        (
            "word incidence numerator altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "exact_seed_path_referenced_unique_word_key_count",
                ),
                4,
            ),
        ),
        (
            "word incidence fraction altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "word_key_registry_incidence_fraction",
                ),
                "4/441280",
            ),
        ),
        (
            "word-roof incidence numerator altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "symbolic_registry_incidence",
                    "exact_seed_path_referenced_unique_symbolic_word_roof_position_count",
                ),
                120,
            ),
        ),
        (
            "second leg relative target relabelled as owner",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_root_contract",
                    "second_leg_relative_registry_target_id",
                ),
                "G[0,0]",
            ),
        ),
        (
            "second leg namespace safety flag disabled",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_root_contract",
                    "second_leg_relative_target_is_not_relabelled_as_absolute_owner",
                ),
                False,
            ),
        ),
        (
            "root path ID altered",
            lambda d: set_path(
                d,
                ("result", "exact_path_root_contract", "round113_official_path_id"),
                "gate5-rank3-endpoint-sheet-path:tampered",
            ),
        ),
        (
            "root operator cell altered",
            lambda d: set_path(
                d,
                ("result", "exact_path_root_contract", "round117_operator_cell_id"),
                "round117-operator-cell:tampered",
            ),
        ),
        (
            "root exact seed altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_root_contract",
                    "round121_exact_parent_W_seed_id",
                ),
                "round121-exact-parent-W:tampered",
            ),
        ),
        (
            "global registry ordinal tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    0,
                    "global_candidate_registry_ordinal_zero_based",
                ),
                102442,
            ),
        ),
        (
            "retained pair ordinal tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    0,
                    "retained_chart_target_pair_ordinal_zero_based",
                ),
                105,
            ),
        ),
        (
            "crossing pattern ordinal tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    0,
                    "crossing_pattern_ordinal_zero_based",
                ),
                0,
            ),
        ),
        (
            "global word row target tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    1,
                    "global_word_row",
                    1,
                ),
                "G[0,0]",
            ),
        ),
        (
            "global word row digest tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    2,
                    "global_word_row_sha256",
                ),
                "0" * 64,
            ),
        ),
        (
            "word row relative target changed to absolute owner",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    1,
                    "relative_registry_target_id",
                ),
                "G[0,0]",
            ),
        ),
        (
            "word row namespace claim disabled",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    1,
                    "relative_registry_target_and_absolute_owner_are_distinct_namespaces",
                ),
                False,
            ),
        ),
        (
            "word row return length altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    1,
                    "return_length_r",
                ),
                2,
            ),
        ),
        (
            "word row global domain decision claimed",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    0,
                    "complete_global_domain_decision_claimed",
                ),
                True,
            ),
        ),
        (
            "word row physical coverage claimed",
            lambda d: set_path(
                d,
                (
                    "result",
                    "exact_path_official_word_registry_incidence_rows",
                    0,
                    "global_physical_coverage_claimed",
                ),
                True,
            ),
        ),
        (
            "word row order swapped",
            lambda d: d["result"][
                "exact_path_official_word_registry_incidence_rows"
            ].__setitem__(
                slice(0, 2),
                list(reversed(d["result"][
                    "exact_path_official_word_registry_incidence_rows"
                ][:2])),
            ),
        ),
        (
            "subbranch common rank altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_refined_subbranch_crosswalk_rows",
                    0,
                    "common_rank",
                ),
                1,
            ),
        ),
        (
            "subbranch physical homogeneity altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_refined_subbranch_crosswalk_rows",
                    0,
                    "physical_homogeneity",
                    "source",
                ),
                "H1",
            ),
        ),
        (
            "subbranch promoted to global registry entry",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_refined_subbranch_crosswalk_rows",
                    0,
                    "global_homogeneous_subbranch_claimed",
                ),
                True,
            ),
        ),
        (
            "carrier stage altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "word_subbranch_operator_carrier_crosswalk_rows",
                    0,
                    "stage",
                ),
                1,
            ),
        ),
        (
            "carrier roof split truncated",
            lambda d: set_path(
                d,
                (
                    "result",
                    "word_subbranch_operator_carrier_crosswalk_rows",
                    0,
                    "roof_level_js",
                ),
                [0],
            ),
        ),
        (
            "carrier operator digest altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "word_subbranch_operator_carrier_crosswalk_rows",
                    0,
                    "standard_family_leg_operator_row_sha256",
                ),
                "0" * 64,
            ),
        ),
        (
            "carrier promoted to global physical carrier",
            lambda d: set_path(
                d,
                (
                    "result",
                    "word_subbranch_operator_carrier_crosswalk_rows",
                    0,
                    "global_physical_carrier_claimed",
                ),
                True,
            ),
        ),
        (
            "base immutable roof altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "immutable_seed_local_base_key",
                    2,
                ),
                1,
            ),
        ),
        (
            "base stage altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "stage",
                ),
                1,
            ),
        ),
        (
            "base operator carrier altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "standard_family_leg_operator_row_id",
                ),
                "round124-standard-family-leg-operator:tampered",
            ),
        ),
        (
            "base F18 source row hash altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "round126_F18_slot_row_sha256",
                ),
                "0" * 64,
            ),
        ),
        (
            "field index duplicated",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_bindings",
                    1,
                    "field_index",
                ),
                1,
            ),
        ),
        (
            "field source round altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_bindings",
                    17,
                    "source_certificate_round",
                ),
                125,
            ),
        ),
        (
            "field source row hash altered and fully resigned",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_bindings",
                    0,
                    "source_slot_canonical_sha256",
                ),
                "f" * 64,
            ),
        ),
        (
            "slot ID duplicated across fields",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_bindings",
                    1,
                    "slot_id",
                ),
                d["result"]["seed_local_base_key_crosswalk_rows"][0][
                    "field_slot_bindings"
                ][0]["slot_id"],
            ),
        ),
        (
            "slot ID orphan injected",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_bindings",
                    0,
                    "slot_id",
                ),
                "round127-orphan-slot",
            ),
        ),
        (
            "base field count reduced",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "field_slot_count",
                ),
                17,
            ),
        ),
        (
            "base promoted to global block",
            lambda d: set_path(
                d,
                (
                    "result",
                    "seed_local_base_key_crosswalk_rows",
                    0,
                    "global_level_or_block_claimed",
                ),
                True,
            ),
        ),
        (
            "slot census reduced",
            lambda d: set_path(
                d,
                ("result", "slot_census", "round126_total_seed_local_slot_count"),
                2159,
            ),
        ),
        (
            "field exact-once census disabled",
            lambda d: set_path(
                d,
                (
                    "result",
                    "slot_census",
                    "all_18_fields_exactly_once_on_each_of_120_seed_local_base_keys",
                ),
                False,
            ),
        ),
        (
            "same-root slot linkage disabled",
            lambda d: set_path(
                d,
                (
                    "result",
                    "slot_census",
                    "all_fields_share_same_word_subbranch_roof_child_stage_recut_and_operator_carrier_per_base",
                ),
                False,
            ),
        ),
        (
            "120 local levels promoted to global blocks in ledger",
            lambda d: set_path(
                d,
                ("result", "count_ledger", "global_complete_18_field_block_count"),
                120,
            ),
        ),
        (
            "complete block count promoted",
            lambda d: set_path(
                d,
                ("result", "count_ledger", "complete_18_field_block_count"),
                120,
            ),
        ),
        (
            "Gate5 block count promoted",
            lambda d: set_path(
                d, ("result", "count_ledger", "gate5_block_count"), 120
            ),
        ),
        (
            "global maturity promoted",
            lambda d: set_path(
                d,
                ("result", "global_safety_state", "gate5_global_maturity"),
                "18/18",
            ),
        ),
        (
            "global complete blocks promoted",
            lambda d: set_path(
                d,
                (
                    "result",
                    "global_safety_state",
                    "global_complete_18_field_block_count",
                ),
                120,
            ),
        ),
        (
            "Gate5 status promoted",
            lambda d: set_path(
                d,
                ("result", "global_safety_state", "gate5_status"),
                "CERTIFIED",
            ),
        ),
        (
            "CM2 promoted",
            lambda d: set_path(
                d,
                ("result", "global_safety_state", "cm2_verdict"),
                "GO_FOR_CLAIM",
            ),
        ),
        (
            "scope broadened to all Borel keys",
            lambda d: set_path(
                d,
                ("result", "strict_scope"),
                "all Borel keys and arbitrary return depths",
            ),
        ),
        (
            "nonclaim removed",
            lambda d: d["result"]["strict_nonclaims"].pop(),
        ),
        (
            "global registry stream digest tampered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "global_manifest_embedded_pins",
                    "candidate_word_rows_stream_sha256",
                ),
                "0" * 64,
            ),
        ),
        (
            "upstream Round126 certificate pin altered",
            lambda d: set_path(
                d,
                (
                    "result",
                    "upstream_artifact_byte_pins",
                    ROUND126.name,
                ),
                "0" * 64,
            ),
        ),
        (
            "base row order swapped",
            lambda d: d["result"]["seed_local_base_key_crosswalk_rows"].__setitem__(
                slice(0, 2),
                list(reversed(
                    d["result"]["seed_local_base_key_crosswalk_rows"][:2]
                )),
            ),
        ),
    ]
    rejected: list[str] = []
    for label, mutate in mutations:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        resign_document(candidate)
        try:
            evaluate_document(candidate, expected)
        except Exception:
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(
    document: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    raw = (
        json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    attacks: list[tuple[str, bytes]] = []
    attacks.append(
        (
            "duplicate top-level schema key",
            raw.replace(
                b'{\n  "result":',
                b'{\n  "schema": "duplicate",\n  "result":',
                1,
            ),
        )
    )
    attacks.append(
        (
            "duplicate result status key",
            raw.replace(
                b'"result": {',
                b'"result": {"status":"duplicate",',
                1,
            ),
        )
    )
    extra_top = copy.deepcopy(document)
    extra_top["extra"] = True
    attacks.append(
        (
            "closed envelope extra key",
            canonical(extra_top).encode("utf-8"),
        )
    )
    extra_result = copy.deepcopy(document)
    extra_result["result"]["extra"] = True
    extra_result["result_sha256"] = digest(extra_result["result"])
    attacks.append(
        (
            "closed result extra key",
            canonical(extra_result).encode("utf-8"),
        )
    )
    attacks.append(
        (
            "floating-point integer",
            raw.replace(
                b'"global_symbolic_candidate_word_key_count": 441280',
                b'"global_symbolic_candidate_word_key_count": 441280.0',
                1,
            ),
        )
    )
    attacks.append(
        (
            "NaN constant",
            raw.replace(
                b'"global_symbolic_candidate_word_key_count": 441280',
                b'"global_symbolic_candidate_word_key_count": NaN',
                1,
            ),
        )
    )
    attacks.append(
        (
            "positive Infinity constant",
            raw.replace(
                b'"global_symbolic_candidate_word_key_count": 441280',
                b'"global_symbolic_candidate_word_key_count": Infinity',
                1,
            ),
        )
    )
    attacks.append(
        (
            "negative Infinity constant",
            raw.replace(
                b'"global_symbolic_candidate_word_key_count": 441280',
                b'"global_symbolic_candidate_word_key_count": -Infinity',
                1,
            ),
        )
    )
    attacks.append(("UTF-8 BOM", b"\xef\xbb\xbf" + raw))
    attacks.append(("invalid UTF-8", raw[:-2] + b"\xff}\n"))
    surrogate = copy.deepcopy(document)
    surrogate["result"]["strict_scope"] = "\ud800"
    surrogate["result_sha256"] = digest(surrogate["result"])
    attacks.append(
        (
            "unpaired surrogate",
            json.dumps(surrogate, sort_keys=True).encode("utf-8"),
        )
    )
    attacks.append(("top-level array", b"[]\n"))
    attacks.append(("trailing second document", raw + b"{}\n"))
    stale = copy.deepcopy(document)
    stale["result"]["status"] = "TAMPERED_WITH_STALE_OUTER_DIGEST"
    attacks.append(
        (
            "stale outer result digest",
            (
                json.dumps(stale, sort_keys=True, indent=2, allow_nan=False)
                + "\n"
            ).encode("utf-8"),
        )
    )
    rejected: list[str] = []
    for label, attack in attacks:
        try:
            evaluate_bytes(attack, expected)
        except Exception:
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def verification_document(
    certificate_path: Path,
    certificate: dict[str, Any],
    audit: dict[str, Any],
    reconstructed: dict[str, Any],
    mutation_labels: list[str],
    strict_labels: list[str],
) -> dict[str, Any]:
    registry = audit["global_registry_replay"]
    result = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": sha256(VERIFIER),
        "certificate_sha256": sha256(certificate_path),
        "certificate_result_sha256": certificate["result_sha256"],
        "exact_rational_global_registry_replay": {
            "source_chart_count": registry["source_chart_count"],
            "conservative_target_lift_count": registry["target_lift_count"],
            "retained_chart_target_pair_count":
                registry["retained_pair_count"],
            "chart_target_pair_rows_sha256":
                registry["chart_target_pair_rows_sha256"],
            "crossing_pattern_count": registry["crossing_pattern_count"],
            "crossing_pattern_rows_sha256":
                registry["crossing_pattern_rows_sha256"],
            "candidate_return_word_key_count":
                registry["candidate_word_count"],
            "candidate_word_key_row_stream_sha256":
                registry["candidate_word_rows_stream_sha256"],
            "roof_level_prefix_suffix_position_count":
                registry["roof_level_position_count"],
            "roof_histogram": registry["roof_histogram"],
            "arithmetic": "exact fractions and integers only",
        },
        "official_path_registry_membership_audit": {
            "official_word_ordinals_zero_based":
                audit["official_word_ordinals"],
            "official_word_key_ids": audit["official_word_ids"],
            "official_word_count": 3,
            "symbolic_word_roof_position_count": 5,
            "symbolic_word_incidence": "3/441280",
            "symbolic_word_roof_incidence": "5/3286976",
            "incidence_is_not_domain_measure_or_physical_coverage": True,
            "second_leg_relative_registry_target_id":
                audit["second_leg_relative_registry_target_id"],
            "second_leg_absolute_owner_id":
                audit["second_leg_absolute_owner_id"],
            "second_leg_relative_and_absolute_namespaces_kept_distinct": True,
        },
        "reconstructed_counts": reconstructed,
        "independent_rebuild_audit": {
            "Round121_half_open_common_children":
                audit["independently_rebuilt_child_count"],
            "Round121_refined_homogeneous_subbranches":
                audit["independently_rebuilt_refined_subbranch_count"],
            "Round126_word_subbranch_operator_carriers":
                audit["independently_grouped_carrier_count"],
            "Round126_seed_local_word_subbranch_roof_base_keys":
                audit["independently_rebuilt_base_key_count"],
            "Round126_seed_local_field_slots":
                audit["independently_reaccounted_slot_count"],
            "field_slot_count_per_field":
                audit["field_slot_count_per_field"],
            "each_base_key_has_F1_through_F18_exactly_once": True,
        },
        "safety_state": {
            "rank3_seed_child_field_maturity": "18/18",
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_status": "NOT_CERTIFIED",
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "independence_contract": {
            "imports_Round127_producer": False,
            "executes_Round127_producer": False,
            "Round127_producer_is_byte_pinned_only": True,
            "imports_global_registry_producer": False,
            "executes_global_registry_producer": False,
            "imports_upstream_producer_or_verifier_modules": False,
            "Round113_Round117_Round121_Round126_artifacts_strict_parsed_as_data":
                True,
            "retained_pairs_replayed_with_exact_rational_filter": True,
            "all_441280_symbolic_word_rows_streamed_independently": True,
            "all_24_subbranch_and_child_IDs_rebuilt": True,
            "all_72_carriers_grouped_from_same-root level rows": True,
            "all_120_base_keys_derived_before_certificate_comparison": True,
            "all_2160_slots_reaccounted_exactly_once": True,
            "re_signed_semantic_mutations_required_rejected": True,
            "strict_JSON_attacks_required_rejected": True,
        },
        "determinism_contract": {
            "PYTHONHASHSEED_independent": True,
            "canonical_JSON":
                "sort_keys=True, indent=2, allow_nan=False, final newline",
            "stable_base_order": "common_rank,stage,roof_level_j",
            "stable_carrier_order": "common_rank,stage",
            "stable_subbranch_order": "common_rank",
            "stable_word_order": "path_position_zero_based",
        },
        "semantic_mutation_test_count": len(mutation_labels),
        "semantic_mutation_rejection_labels": mutation_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "byte_pinned_input_count": len(BYTE_PINS) + 1,
        "upstream_closed_result_sha256_pins": dict(sorted(RESULT_PINS.items())),
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
    try:
        require(
            args.certificate.is_file() and not args.certificate.is_symlink(),
            "certificate regular file",
        )
        require(not args.output.is_symlink(), "output symlink refused")
        certificate = parse_strict_bytes(args.certificate.read_bytes())
        expected, audit = expected_result()
        reconstructed = evaluate_document(certificate, expected)
        mutation_labels = semantic_mutations(certificate, expected)
        strict_labels = strict_json_attacks(certificate, expected)
        verification = verification_document(
            args.certificate,
            certificate,
            audit,
            reconstructed,
            mutation_labels,
            strict_labels,
        )
        args.output.write_text(
            json.dumps(
                verification,
                sort_keys=True,
                indent=2,
                allow_nan=False,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.output}")
        print(f"result_sha256={verification['result_sha256']}")
        print(f"semantic_mutations={len(mutation_labels)}")
        print(f"strict_json_attacks={len(strict_labels)}")
        print("status=PASS")
        return 0
    except Exception as exc:
        print(
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
