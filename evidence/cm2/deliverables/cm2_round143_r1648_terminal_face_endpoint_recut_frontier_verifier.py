#!/usr/bin/env python3
"""Fail-closed verifier for the Round143 terminal-face endpoint frontier.

The verifier does not import the producer.  It independently checks the
closed JSON envelope, every frozen dependency, the endpoint/rank/mesh/recut
algebra, all null historical fields, and a mutation suite.  It then executes
the byte-pinned producer in a clean temporary directory target under a
different hash seed and requires a byte-identical certificate.  This gives an
independent semantic checker plus an end-to-end rerun of the validated Arb
dual/recentered-affine proof.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round143.r1648-terminal-face-endpoint-recut-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round143.r1648-terminal-face-endpoint-recut-frontier-verification.v1"
)
PRODUCER_SHA256 = (
    "bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38"
)
CERTIFICATE_SHA256 = (
    "74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67"
)
CERTIFICATE_RESULT_SHA256 = (
    "35a9f8e0437086a2feaf294c10c621ce21319dc93aac88f33dbc4024e4507e92"
)
MAX_CERTIFICATE_BYTES = 1_000_000
MAX_JSON_INTEGER_DIGITS = 4096
RETURN_DEPTH = 1648

INPUT_PINS = {
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py":
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json":
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py":
        "cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json":
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    "cm2-one-hundred-thirty-ninth-direct-assault-manifest-2026-07-24.sha256":
        "f8f13619b07ff8d5d0bc238335722f1951abc81e1d8ad07ccb325f95aab9a198",
    "cm2_round140_fixed_s_adaptive_component_identity_bridge.py":
        "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json":
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    "cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py":
        "4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json":
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    "cm2-one-hundred-fortieth-direct-assault-manifest-2026-07-24.sha256":
        "d46c15f7823f78719b505365e0f9c4c3e70103a3bc09fb075a3032b366639748",
    "cm2_round140_round35_parent_w_r1648_materialization_audit.py":
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json":
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py":
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json":
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-direct-assault-manifest-2026-07-24.sha256":
        "f3b80bfd794087b395be83fc8e94f7e2ba5201db576337858d9b69c939dd1ed9",
    "cm2_round137_seed_independent_dyadic_basis_rank_contract.py":
        "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac",
    "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json":
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    "cm2-gate34-round55-global-image-recut-cap-natural-mesh-frontier-manifest-2026-07-20.json":
        "12270ccbdea2b3c6bf203529e94b31a298061d6b057ddc14757853763059e95e",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path, maximum_bytes: int) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink()
        and metadata.st_size <= maximum_bytes,
        "safe bounded JSON input",
    )
    document = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_int=lambda text: (
            int(text)
            if len(text.lstrip("-")) <= MAX_JSON_INTEGER_DIGITS
            else (_ for _ in ()).throw(ValueError("oversized JSON integer"))
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite:{token}")
        ),
    )
    require(type(document) is dict, "JSON root object")
    return document


def interval_pair_count(level: int) -> int:
    require(level >= 0, "nonnegative level")
    return 0 if level < 2 else (2**level - 1) * (2**level - 2) // 2


def pair_lex_rank(level: int, left: int, right: int) -> int:
    maximum = 2**level - 1
    require(1 <= left < right <= maximum, "pair range")
    return (left - 1) * maximum - (left - 1) * left // 2 + right - left - 1


def even_pair_count_before(level: int, left: int, right: int) -> int:
    half_maximum = 2 ** (level - 1) - 1
    even_left_before = (left - 1) // 2
    total = (
        even_left_before * half_maximum
        - even_left_before * (even_left_before + 1) // 2
    )
    if left % 2 == 0:
        total += max(0, (right - 1) // 2 - left // 2)
    return total


def rank_1d(row: list[int]) -> int:
    require(
        len(row) == 3 and all(type(value) is int for value in row),
        "rank row",
    )
    level, left, right = row
    require(level >= 2 and (left % 2 or right % 2), "primitive row")
    return (
        interval_pair_count(level - 1)
        + pair_lex_rank(level, left, right)
        - even_pair_count_before(level, left, right)
    )


def encoded_integer_matches(record: dict[str, Any], value: int) -> bool:
    decimal = str(value)
    return record == {
        "decimal": decimal,
        "hexadecimal": "0x" + format(value, "x"),
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def validate_coordinate_rank(record: dict[str, Any]) -> None:
    require(
        set(record) == {
            "coordinate",
            "endpoint_fixed_dyadic_outers",
            "contained_primitive_basis_row",
            "contained_primitive_basis_rank",
            "rank_unrank_roundtrip_exact",
            "minimal_level_with_two_strict_grid_points",
            "lex_first_consecutive_pair_at_that_level",
            "least_Round137_v1_rank_for_this_declared_coordinate_interval",
            "historical_Round35_coordinate_crosswalk",
        },
        "coordinate rank keys",
    )
    row = record["contained_primitive_basis_row"]
    level, left, right = row
    require(right == left + 1, "consecutive rank pair")
    endpoint = record["endpoint_fixed_dyadic_outers"]
    lower = tuple(Q(value) for value in endpoint["left"])
    upper = tuple(Q(value) for value in endpoint["right"])
    denominator = 2**level
    require(
        Q(0) < lower[0] < lower[1]
        < Q(left, denominator) < Q(right, denominator)
        < upper[0] < upper[1] < Q(1),
        "strict rank containment",
    )
    previous = 2 ** (level - 1)
    first_previous = (
        lower[1].numerator * previous // lower[1].denominator + 1
    )
    require(
        not (
            Q(first_previous, previous) > lower[1]
            and Q(first_previous + 1, previous) < upper[0]
        ),
        "rank level minimal",
    )
    expected_first = (
        lower[1].numerator * denominator // lower[1].denominator + 1
    )
    require(left == expected_first, "lex first pair")
    numeric_rank = rank_1d(row)
    require(
        encoded_integer_matches(
            record["contained_primitive_basis_rank"], numeric_rank
        ),
        "encoded 1D rank",
    )
    require(
        record["rank_unrank_roundtrip_exact"] is True
        and record["minimal_level_with_two_strict_grid_points"] is True
        and record["lex_first_consecutive_pair_at_that_level"] is True
        and record[
            "least_Round137_v1_rank_for_this_declared_coordinate_interval"
        ] is True
        and record["historical_Round35_coordinate_crosswalk"] is False,
        "rank claims",
    )


def validate_result(result: dict[str, Any]) -> None:
    require(
        result["status"]
        == "CERTIFIED_LOCAL_R1648_TERMINAL_FACE_ENDPOINT_WITH_PROSPECTIVE_RECUT_FRONTIER",
        "status",
    )
    provenance = result["provenance"]
    require(
        provenance["producer_sha256"] == PRODUCER_SHA256
        and provenance["dependency_sha256"] == dict(sorted(INPUT_PINS.items()))
        and provenance["append_only"] is True
        and provenance["Round139_or_Round140_files_modified"] is False
        and provenance["Round141_or_Round142_files_modified"] is False,
        "provenance",
    )
    branch = result["frozen_branch"]
    require(
        branch["return_depth"] == RETURN_DEPTH
        and branch["owner_sequence_sha256"]
        == "c50277af0c038521b8933672d2a5a2b9035473895694c3c2878842274337cac3"
        and branch["official_sequence_sha256"]
        == "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
        and branch["compact_path_sha256"]
        == "c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17"
        and branch["terminal_absolute_owner"] == "G[-7,-13]"
        and branch["destination_core_id"]
        == "core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2",
        "frozen branch",
    )
    endpoint = result["terminal_face_endpoint"]
    lambda_lower, lambda_upper = map(Q, endpoint["lambda_bracket"])
    require(
        Q(1) < lambda_lower < lambda_upper < Q(2)
        and lambda_upper - lambda_lower == Q(1, 2**1535)
        and endpoint["lambda_between_one_and_two"] is True
        and endpoint["unique_root_in_bracket"] is True
        and endpoint["local_full_radius4_owner_sequence_certified"] is True
        and endpoint["local_preterminal_nonreturn_certified"] is True
        and endpoint["local_terminal_only_active_face_certified"] is True,
        "endpoint root",
    )
    proof = endpoint["proof"]
    require(
        proof["left_endpoint_sign"] == 1
        and proof["right_endpoint_sign"] == -1
        and proof["whole_derivative_sign"] == -1
        and proof["whole_derivative_dyadic_depth"] == 7
        and proof["preterminal_strict_nonreturn_count"] == 1647
        and len(proof["newton_rows"]) == 4,
        "endpoint signs and derivative",
    )
    ledger = proof["complete_radius4_owner_audit"]
    histogram = ledger["margin_kind_histogram"]
    require(
        ledger["strict_margin_count"] == sum(histogram.values())
        and ledger["strict_margin_count"] == 292473
        and ledger["worst_dyadic_depth"] == 4284
        and histogram["candidate_miss_discriminant"] == 249435
        and histogram["candidate_behind_far_root"] == 7937
        and histogram["candidate_future_root_positive"] == 7956
        and histogram["winner_pairwise_root_gap"] == 6308,
        "complete owner audit ledger",
    )
    candidate = result["candidate_full_leaf_interval"]
    require(
        candidate["positive_width"] is True
        and candidate["source_adapted_length_below_delta_14"] is True
        and candidate["source_adapted_length_below_1e_minus_90"] is True
        and candidate["whole_interval_owner_corridor_certified"] is False
        and candidate[
            "whole_interval_equals_maximal_U_intersection_leaf_certified"
        ] is False
        and "intervening scale-2^-4289 corridor"
        in candidate["exact_first_blocker"],
        "candidate interval frontier",
    )
    source_length = tuple(
        Q(value) for value in candidate["source_adapted_length_outer"]
    )
    require(
        Q(0) < source_length[0] < source_length[1]
        < Q(1, 10**90) < Q(1, 2**23),
        "source length bounds",
    )
    ranks = result["coordinate_explicit_Round137_v1_leaf_ranks"]
    validate_coordinate_rank(ranks["canonical_H1_x_candidate"])
    validate_coordinate_rank(ranks["Round140_normalized_t_candidate"])
    require(
        ranks["canonical_H1_x_candidate"][
            "contained_primitive_basis_row"
        ][0] == 4290
        and ranks["Round140_normalized_t_candidate"][
            "contained_primitive_basis_row"
        ][0] == 4283
        and ranks["coordinate_dependence_witnessed_by_different_levels"]
        is True
        and ranks["historical_Round35_leaf_coordinate_frozen"] is False
        and ranks["historical_Round35_source_interval_rank"] is None,
        "coordinate underdetermination",
    )
    mesh = result["B14_source_mesh_frontier"]
    require(
        mesh["incidence_rank_B"] == 14
        and mesh["delta_14"] == "1/8388608"
        and mesh["candidate_interval_is_one_clipped_B14_cell"] is True
        and mesh[
            "candidate_interval_is_one_clipped_1e_minus_90_source_cell"
        ] is True
        and mesh["prospective_left_anchored_natural_short_cell_k"] == 0
        and mesh["historical_natural_short_cell_k"] is None
        and mesh["historical_source_parent_W_id"] is None,
        "source mesh frontier",
    )
    image = result["formal_image_recut_frontier"]
    image_outer = tuple(Q(value) for value in image["formal_adapted_length_outer"])
    count = int(image["conditional_image_recut_count"]["decimal"])
    require(
        Q(0) < image_outer[0] < image_outer[1] < Q(1)
        and image_outer[0] * 10**90 > count - 1
        and image_outer[1] * 10**90 < count
        and encoded_integer_matches(
            image["conditional_image_recut_count"], count
        )
        and image["conditional_image_recut_rank_range"]
        == [0, str(count - 1)]
        and image["conditional_first_image_recut_rank"] == 0
        and image["conditional_last_image_recut_rank"] == str(count - 1)
        and image["full_connected_physical_image_parent_certified"] is False
        and image["historical_image_recut_rank"] is None
        and image["historical_Round35_restriction_id"] is None,
        "conditional image recut ledger",
    )
    strict = result["strict_nonpromotion"]
    historical_nulls = [
        "historical_Round27_canonical_component_rank",
        "historical_Round27_c24_component_id",
        "historical_Round35_source_interval_rank",
        "historical_Round35_natural_short_cell_k",
        "historical_Round35_source_parent_W_id",
        "historical_Round35_image_recut_rank",
        "historical_Round35_rn_restriction_id",
    ]
    require(
        all(strict[key] is None for key in historical_nulls)
        and strict["Round50_owner_key_count"] == 0
        and strict["Round54_t54_token_count"] == 0
        and strict["Round67_q_j_output_count"] == 0
        and strict["global_gate5_maturity"] == "10/18"
        and strict["global_complete_18_field_block_count"] == 0
        and strict["Gate5"] == "NOT_CERTIFIED"
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )
    counts = result["count_ledger"]
    require(
        counts["local_terminal_face_endpoint_count"] == 1
        and counts["complete_radius4_candidate_test_count"] == 265328
        and counts["preterminal_strict_nonreturn_count"] == 1647
        and counts["coordinate_explicit_prospective_leaf_rank_count"] == 2
        and counts["historical_leaf_rank_count"] == 0
        and counts["historical_parent_W_count"] == 0
        and counts["historical_image_recut_rank_count"] == 0,
        "count ledger",
    )


def mutate_at(value: Any, path: tuple[Any, ...], replacement: Any) -> Any:
    result = copy.deepcopy(value)
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


def semantic_attack_suite(result: dict[str, Any]) -> dict[str, Any]:
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("status", ("status",), "CERTIFIED_HISTORICAL_PARENT_W"),
        ("lambda lower", ("terminal_face_endpoint", "lambda_bracket", 0), "2"),
        ("lambda uniqueness", ("terminal_face_endpoint", "unique_root_in_bracket"), False),
        ("derivative", ("terminal_face_endpoint", "proof", "whole_derivative_sign"), 1),
        ("owner audit", ("terminal_face_endpoint", "local_full_radius4_owner_sequence_certified"), False),
        ("nonreturn", ("terminal_face_endpoint", "proof", "preterminal_strict_nonreturn_count"), 1646),
        ("margin count", ("terminal_face_endpoint", "proof", "complete_radius4_owner_audit", "strict_margin_count"), 292472),
        ("margin depth", ("terminal_face_endpoint", "proof", "complete_radius4_owner_audit", "worst_dyadic_depth"), 4283),
        ("corridor promotion", ("candidate_full_leaf_interval", "whole_interval_owner_corridor_certified"), True),
        ("component promotion", ("candidate_full_leaf_interval", "whole_interval_equals_maximal_U_intersection_leaf_certified"), True),
        ("x level", ("coordinate_explicit_Round137_v1_leaf_ranks", "canonical_H1_x_candidate", "contained_primitive_basis_row", 0), 4289),
        ("u level", ("coordinate_explicit_Round137_v1_leaf_ranks", "Round140_normalized_t_candidate", "contained_primitive_basis_row", 0), 4282),
        ("x rank", ("coordinate_explicit_Round137_v1_leaf_ranks", "canonical_H1_x_candidate", "contained_primitive_basis_rank", "decimal"), "0"),
        ("historical rank", ("coordinate_explicit_Round137_v1_leaf_ranks", "historical_Round35_source_interval_rank"), 0),
        ("B", ("B14_source_mesh_frontier", "incidence_rank_B"), 15),
        ("delta", ("B14_source_mesh_frontier", "delta_14"), "1/4194304"),
        ("historical k", ("B14_source_mesh_frontier", "historical_natural_short_cell_k"), 0),
        ("historical parent", ("B14_source_mesh_frontier", "historical_source_parent_W_id"), "forged"),
        ("image count", ("formal_image_recut_frontier", "conditional_image_recut_count", "decimal"), "1"),
        ("image rank", ("formal_image_recut_frontier", "conditional_last_image_recut_rank"), "0"),
        ("image physical", ("formal_image_recut_frontier", "full_connected_physical_image_parent_certified"), True),
        ("historical image", ("formal_image_recut_frontier", "historical_image_recut_rank"), 0),
        ("restriction", ("formal_image_recut_frontier", "historical_Round35_restriction_id"), "forged"),
        ("Gate5", ("strict_nonpromotion", "Gate5"), "CERTIFIED"),
        ("maturity", ("strict_nonpromotion", "global_gate5_maturity"), "11/18"),
        ("CM2", ("strict_nonpromotion", "CM2"), "CERTIFIED"),
        ("component id", ("strict_nonpromotion", "historical_Round27_c24_component_id"), "forged"),
        ("owner count", ("strict_nonpromotion", "Round50_owner_key_count"), 1),
        ("q count", ("strict_nonpromotion", "Round67_q_j_output_count"), 1),
        ("candidate tests", ("count_ledger", "complete_radius4_candidate_test_count"), 265327),
    ]
    rejected: list[str] = []
    for name, path, replacement in attacks:
        candidate = mutate_at(result, path, replacement)
        try:
            validate_result(candidate)
        except Exception:
            rejected.append(name)
    require(len(rejected) == len(attacks), "semantic attacks")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "rejected_names": rejected,
    }


def clean_producer_replay(certificate: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="cm2-r143-verifier-") as directory:
        output = Path(directory) / "replay.json"
        environment = {
            **os.environ,
            "PYTHONHASHSEED": "987654321",
            "LC_ALL": "C",
            "TZ": "UTC",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(HERE),
        }
        completed = subprocess.run(
            [
                sys.executable,
                str(PRODUCER),
                "--output",
                str(output),
            ],
            cwd=HERE,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=1800,
            check=False,
        )
        require(
            completed.returncode == 0
            and output.is_file()
            and not output.is_symlink(),
            "clean producer replay",
        )
        require(output.read_bytes() == certificate.read_bytes(), "byte replay")
        return {
            "exit_code": completed.returncode,
            "hash_seed": environment["PYTHONHASHSEED"],
            "stdout_sha256":
                hashlib.sha256(completed.stdout.encode()).hexdigest(),
            "stderr_sha256":
                hashlib.sha256(completed.stderr.encode()).hexdigest(),
            "replay_sha256": sha256(output),
            "byte_identical_to_certificate": True,
        }


def build_verification(certificate_path: Path) -> dict[str, Any]:
    require(
        sha256(PRODUCER) == PRODUCER_SHA256
        and sha256(certificate_path) == CERTIFICATE_SHA256,
        "producer/certificate pins",
    )
    for name, expected in INPUT_PINS.items():
        path = HERE / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"dependency pin:{name}",
        )
    document = strict_json(certificate_path, MAX_CERTIFICATE_BYTES)
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and document["result_sha256"] == CERTIFICATE_RESULT_SHA256
        and document["result_sha256"] == digest(document["result"]),
        "certificate closure",
    )
    validate_result(document["result"])
    attacks = semantic_attack_suite(document["result"])
    replay = clean_producer_replay(certificate_path)
    result = {
        "status": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "dependency_sha256": dict(sorted(INPUT_PINS.items())),
        "independent_semantic_checks": {
            "strict_closed_envelope": True,
            "dependency_pins": True,
            "lambda_root_bracket_width_and_order": True,
            "complete_radius4_ledger_reconciled": True,
            "preterminal_nonreturn_and_terminal_face_scope": True,
            "two_coordinate_Round137_v1_ranks_recomputed": True,
            "coordinate_underdetermination_preserved": True,
            "B14_and_corrected_source_recut_frontier": True,
            "conditional_image_count_and_rank_range_recomputed": True,
            "all_historical_identifiers_null": True,
            "Gate5_and_CM2_nonpromotion": True,
        },
        "semantic_attack_suite": attacks,
        "clean_producer_replay": replay,
        "strict_scope":
            "local terminal-face endpoint and prospective recut frontier only",
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    require(not path.is_symlink(), "output symlink")
    resolved = path.resolve()
    protected = {
        VERIFIER,
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        *((HERE / name).resolve() for name in INPUT_PINS),
    }
    require(resolved not in protected, "output aliases protected input")
    require(
        resolved.name not in {"", ".", ".."}
        and resolved.parent.is_dir()
        and not path.parent.is_symlink(),
        "safe output directory",
    )
    if path.exists():
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink()
            and all(
                not item.exists() or not os.path.samefile(path, item)
                for item in protected
            ),
            "safe existing output",
        )
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{resolved.name}.",
        suffix=".tmp",
        dir=resolved.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    envelope = build_verification(args.certificate)
    write_atomic(args.output, envelope)
    print(canonical({
        "status": envelope["result"]["status"],
        "semantic_attacks":
            envelope["result"]["semantic_attack_suite"]["rejected_count"],
        "byte_identical_replay":
            envelope["result"]["clean_producer_replay"][
                "byte_identical_to_certificate"
            ],
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
