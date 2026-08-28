#!/usr/bin/env python3
"""Independent verifier for the Round130 positive-Borel local 18-field family.

This verifier never imports or executes the Round130 producer.  It reuses the
byte-pinned independent Round129 verifier for the lambda root sheet and the
Round122 independent Jet2 layer, then independently checks the widened
stage-3 family, the F14/F15 relative-cemetery boundary, the lambda-by-s F17
geometry and typed trace cancellation, and the fibre-local F18 registry.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import tempfile
from collections import Counter, defaultdict
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_round129_rank3_positive_borel_recut_field_bridge_verifier as v129
import cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier as v122
from cm2_round76_r2_numeric_fields_generator import aq, interval


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round130_rank3_positive_borel_local_18_field_completion.py"
CERTIFICATE = (
    HERE
    / "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round130-rank3-positive-borel-local-18-field-completion-verification-2026-07-24.json"
)
ROUND129_CERTIFICATE = (
    HERE
    / "cm2-round129-rank3-positive-borel-recut-field-bridge-2026-07-24.json"
)
ROUND129_VERIFIER = (
    HERE / "cm2_round129_rank3_positive_borel_recut_field_bridge_verifier.py"
)
ROUND129_VERIFICATION = (
    HERE
    / "cm2-round129-rank3-positive-borel-recut-field-bridge-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round130.rank3-positive-borel-local-18-field-completion.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round130.rank3-positive-borel-local-18-field-completion-verification.v1"
)

PRODUCER_SHA256 = (
    "441b714c6795646a1eeafe94be7419c9b91e14838ea0c321878cde2e11efff31"
)
CERTIFICATE_SHA256 = (
    "5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5"
)
CERTIFICATE_RESULT_SHA256 = (
    "6f5af2315002ab6d382028793bbe0ae0c0058196364d9c215f56c1c82c0ee1b0"
)
ROUND129_VERIFIER_SHA256 = (
    "64c20bae8ea2944cb8487b253f9e0ff0a1a68a0c11fe0cd8d6d2206427981ea7"
)
ROUND129_CERTIFICATE_SHA256 = (
    "1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762"
)
ROUND129_VERIFICATION_SHA256 = (
    "4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db"
)

VERIFIER_PRECISION_BITS = 4096
DELTA = Q(1, 10**90)
STAGE3_GUARD_RADIUS = Q(1, 2**180)
ENCLOSURE_GUARD = DELTA / 10**6
S_EPSILON = Q(1, 2**512)
F14_ONE_STEP = 34
F15_ONE_STEP = 34
F17_BY_STAGE = {0: 4_915_200, 1: 2_457_600, 2: 2_457_600}
RAW_INCIDENCE_RANK = {0: 15, 1: 14, 2: 14}
RELATIVE_CENTER_ETA = {0: 1, 1: -1, 2: 0}
TARGET_RADII = {0: Q(4, 25), 1: Q(9, 25), 2: Q(9, 25)}
ADAPTED_X_DERIVATIVE_BOUND = {
    0: DELTA,
    1: 7 * DELTA,
    2: 18 * DELTA,
}
STAGE_RETURN_LENGTH = {0: 2, 1: 1, 2: 2}
STAGE_OWNER = {0: "W[-1,-1]", 1: "G[0,0]", 2: "G[-1,-2]"}
STAGE_CHART = {0: "N", 1: "S", 2: "N"}
SOURCE_COMPONENT = {0: "G:W", 1: "W:N", 2: "G:S"}
TARGET_COMPONENT = {0: "W:N", 1: "G:S", 2: "G:N"}
RECIPIENT_COMPONENTS = (
    ("G:W", "G[0,0]", "W"),
    ("W:N", "W[-1,-1]", "N"),
    ("G:S", "G[0,0]", "S"),
    ("G:N", "G[-1,-2]", "N"),
)
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

ROW_GROUPS = {
    "uniform_stage3_endpoint_guard_template_rows": 192,
    "parameterized_stage3_natural_cell_template_rows": 193,
    "parameterized_merged_cut_template_rows": 215,
    "parameterized_stage3_output_fragment_template_rows": 216,
    "parameterized_child_output_partition_template_rows": 24,
    "parameterized_accepted_norm_leg_template_rows": 72,
    "parameterized_F14_slot_template_rows": 120,
    "parameterized_relative_zero_cemetery_template_rows": 72,
    "parameterized_standard_family_operator_template_rows": 72,
    "parameterized_F15_slot_template_rows": 120,
    "parameterized_input_artificial_trace_template_rows": 144,
    "parameterized_input_trace_incidence_template_rows": 69,
    "parameterized_stage3_output_trace_template_rows": 432,
    "parameterized_stage3_output_incidence_template_rows": 215,
    "parameterized_source_injection_contract_template_rows": 3,
    "parameterized_graph_current_leg_template_rows": 72,
    "parameterized_recipient_component_template_rows": 4,
    "parameterized_recipient_pullback_map_template_rows": 72,
    "parameterized_source_injection_derivation_template_rows": 3,
    "parameterized_F17_slot_template_rows": 120,
    "parameterized_F1_F17_same_key_map_template_rows": 120,
    "parameterized_F18_slot_template_rows": 120,
    "parameterized_local_18_field_level_block_template_rows": 120,
    "parameterized_local_18_field_child_packet_template_rows": 24,
}

PRIMARY_ID_KEYS = {
    "uniform_stage3_endpoint_guard_template_rows":
        "stage3_endpoint_template_id",
    "parameterized_stage3_natural_cell_template_rows":
        "stage3_natural_cell_template_id",
    "parameterized_merged_cut_template_rows": "merged_cut_template_id",
    "parameterized_stage3_output_fragment_template_rows":
        "output_fragment_template_id",
    "parameterized_child_output_partition_template_rows":
        "child_output_partition_template_id",
    "parameterized_accepted_norm_leg_template_rows":
        "accepted_norm_leg_template_id",
    "parameterized_F14_slot_template_rows": "field_slot_template_id",
    "parameterized_relative_zero_cemetery_template_rows":
        "relative_zero_cemetery_template_id",
    "parameterized_standard_family_operator_template_rows":
        "standard_family_operator_template_id",
    "parameterized_F15_slot_template_rows": "field_slot_template_id",
    "parameterized_input_artificial_trace_template_rows":
        "input_artificial_trace_template_id",
    "parameterized_input_trace_incidence_template_rows":
        "input_trace_incidence_template_id",
    "parameterized_stage3_output_trace_template_rows":
        "stage3_output_trace_template_id",
    "parameterized_stage3_output_incidence_template_rows":
        "stage3_output_incidence_template_id",
    "parameterized_source_injection_contract_template_rows":
        "source_injection_contract_template_id",
    "parameterized_graph_current_leg_template_rows":
        "graph_current_leg_template_id",
    "parameterized_recipient_component_template_rows":
        "recipient_component_template_id",
    "parameterized_recipient_pullback_map_template_rows":
        "recipient_pullback_map_template_id",
    "parameterized_source_injection_derivation_template_rows":
        "source_injection_derivation_template_id",
    "parameterized_F17_slot_template_rows": "field_slot_template_id",
    "parameterized_F1_F17_same_key_map_template_rows":
        "same_key_map_template_id",
    "parameterized_F18_slot_template_rows": "field_slot_template_id",
    "parameterized_local_18_field_level_block_template_rows":
        "level_block_template_id",
    "parameterized_local_18_field_child_packet_template_rows":
        "child_packet_template_id",
}

RESULT_KEYSET_SHA256 = (
    "8da6838a3f26723fee01af8a9592a414902b485f854c138b11f166b3e201889d"
)
ROW_KEYSET_SHA256 = {
    "parameterized_F14_slot_template_rows":
        "2227369897244da7819ab1019a1eb19d8d756db73eaff4751cb049260170cd90",
    "parameterized_F15_slot_template_rows":
        "3abd80bbbdcf3572e25a3d86de4298160e1695c82c8a3992c705a5903021082e",
    "parameterized_F17_slot_template_rows":
        "b46e082cdb51636c48e6242ce770158832ec003286591b76e5183e2032c1a9a7",
    "parameterized_F18_slot_template_rows":
        "8fed0c8ea5e8b3478dd2807327d2b4b50cb6916f5b7847f943f78831910f4d32",
    "parameterized_F1_F17_same_key_map_template_rows":
        "e942763c2c9d496df30fa4f1e9c627a4e612e12835f98eb9acf9a79302ac9f8f",
    "parameterized_accepted_norm_leg_template_rows":
        "5352819a982f9b99f37c349e0659d1f631b1d7c93791487de6c7f6adfd456d29",
    "parameterized_child_output_partition_template_rows":
        "8959576af998f78695b7b90cb3fb40425968d1b5a1ec8d64b66f4bd915ccb1fc",
    "parameterized_graph_current_leg_template_rows":
        "98688736990431c66832eead0d2aa8c6607566d6a128b3b181bde3d0e6392888",
    "parameterized_input_artificial_trace_template_rows":
        "3b00d963bdad2dbffc0041883023010c7cf025ef8cb016b7a1d294b22f5b87c5",
    "parameterized_input_trace_incidence_template_rows":
        "d0a5dad5139e32fa82e6e468ce6fc93d336b98629989ef6409cc614d869b5f06",
    "parameterized_local_18_field_child_packet_template_rows":
        "5087e18fea8d3658792702625367f08fb17a449b32931b97293faee138a111b4",
    "parameterized_local_18_field_level_block_template_rows":
        "32a9032c78af49d1e7f24061bbf9929798b9027bcaeca7a55438f4664d15842d",
    "parameterized_merged_cut_template_rows":
        "378ac068e54834c0fc349496c3fe5aedf53441303246768bf5f8f9e5394eec3b",
    "parameterized_recipient_component_template_rows":
        "8392dc665177f2b3ee2bef975574f879af4ba2042f75a8e6b17384b9b235a9bd",
    "parameterized_recipient_pullback_map_template_rows":
        "9ed69b3fe8967b890401555424252695ca44bb380a01209fe9d3dc0409ce69c4",
    "parameterized_relative_zero_cemetery_template_rows":
        "fb328693419b185c2cbb75f39bcc28c12de13e3d7f1b14c1f2c99b985bc095f2",
    "parameterized_source_injection_contract_template_rows":
        "d7131eb6ca7d9e102858907a81290f34adc0e69fc305b847d4b006a9af567856",
    "parameterized_source_injection_derivation_template_rows":
        "5eb470f8eb0d7d6e39f8d76972a0aa90b4c302390f16bb724349a2fc4677c525",
    "parameterized_stage3_natural_cell_template_rows":
        "2cfaee87481d533c72e287606261791f455dff599fed32d2c419d9f090b6c1b5",
    "parameterized_stage3_output_fragment_template_rows":
        "daf58c6d7ae7571713e88338a738657b8ca7e2e5c5e39f194f7ea9402408a8d0",
    "parameterized_stage3_output_incidence_template_rows":
        "35b8a279771c1ca75dd0f64eda00b42252236321f023152398f2aa714732aa25",
    "parameterized_stage3_output_trace_template_rows":
        "325bb2030a440b96f8dd7cbe8882a5a37b9c54229d7a838992eaeab71474df6b",
    "parameterized_standard_family_operator_template_rows":
        "27118dd1fdcb514b7c29bd4364a27f67a11803494913c908d8ad3f6c57e82586",
    "uniform_stage3_endpoint_guard_template_rows":
        "a4cae7591657ed5196004fe739f6066cd41fea2cf2629452a3ac37f455168f36",
}
NESTED_KEYSET_SHA256 = {
    "frozen_input_contract":
        "1bc95eb874b205c0a9bfb7e1daaac8410f2d1a44ccab663ed1164bde0c986074",
    "exact_lambda_instance_contract":
        "7e99e94c3c6f4717a9665a27548ce6615832884e387994df748c6c235d1fef4f",
    "family_stage3_geometry_contract":
        "ba327a1799133220e78f97893b8b5b8c1022a2893fa19427738ce483791556c5",
    "per_fibre_F14_contract":
        "cd3125970df840fcf12cabc78b312fc0b98a1b8c4ca0c274b753f2c27e8bfaf2",
    "per_fibre_F15_and_cemetery_contract":
        "f307868d226bfb2e6c9ea73ce3ec5fc514fafaaf66d02bcdd42ea6f68364452e",
    "per_fibre_F17_graph_current_contract":
        "c01668473b18ada605a9ef4a6d8c45d381cf88482085b248e5ef739a4aabde91",
    "per_fibre_F18_phase_contract":
        "d252e420331f2285a217ec913d916d6f02fb516f8c026007341e2b4f1cfbc2f7",
    "combined_template_registry":
        "8738d554ba0fff63d3da5826c86d838c7c2d2ab671df978dec2f53ac14b6c9df",
    "count_ledger":
        "154656fc4bf012910433fefbed9f2e73cb24fc018c6641a0a441a9a300b3ced8",
}


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


def require(condition: Any, label: str) -> None:
    if not bool(condition):
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    return str(Q(value))


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise VerificationError(f"non-finite JSON number:{token}")


def reject_float(token: str) -> Any:
    raise VerificationError(f"JSON float forbidden:{token}")


def strict_integer(token: str) -> int:
    require(token != "-0", "negative zero forbidden")
    require(len(token.lstrip("-")) <= 1024, "oversized integer")
    return int(token)


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


def parse_bytes(raw: bytes, *, certificate_mode: bool = True) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM forbidden")
    require(b"\x00" not in raw, "NUL byte forbidden")
    if certificate_mode:
        require(len(raw) <= 32_000_000, "certificate size bound")
    text = raw.decode("utf-8")
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=reject_float,
        parse_int=strict_integer,
    )
    require(type(value) is dict, "top-level JSON object")
    reject_surrogates(value)
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str, f"{label}:fraction type")
    require(
        re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value)
        is not None,
        f"{label}:canonical fraction syntax",
    )
    result = Q(value)
    require(str(result) == value, f"{label}:reduced fraction")
    return result


def qinterval(value: Any, label: str) -> tuple[Q, Q]:
    require(
        type(value) is list and len(value) == 2,
        f"{label}:interval pair",
    )
    lower, upper = qvalue(value[0], f"{label}:lower"), qvalue(
        value[1], f"{label}:upper"
    )
    require(lower <= upper, f"{label}:ordered")
    return lower, upper


def arb_pair(value: arb) -> tuple[Q, Q]:
    return v122.arb_pair(value)


def interval_contains(stored: Any, actual: arb, label: str) -> None:
    stored_lower, stored_upper = qinterval(stored, label)
    actual_lower, actual_upper = arb_pair(actual)
    require(
        stored_lower <= actual_lower <= actual_upper <= stored_upper,
        f"{label}:contains independent interval",
    )


def interval_overlaps(stored: Any, actual: arb, label: str) -> None:
    stored_lower, stored_upper = qinterval(stored, label)
    actual_lower, actual_upper = arb_pair(actual)
    require(
        max(stored_lower, actual_lower) <= min(stored_upper, actual_upper),
        f"{label}:overlaps independent interval",
    )


def row_id(kind: str, payload: list[Any]) -> str:
    return f"round130-{kind}:" + digest([f"round130-{kind}-v1", *payload])


def row_digest(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict, f"{label}:row object")
    require(type(row.get("row_sha256")) is str, f"{label}:row hash")
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    require(row["row_sha256"] == digest(payload), f"{label}:row digest")


def closed_document(path: Path, schema: str | None = None) -> dict[str, Any]:
    document = parse_bytes(path.read_bytes())
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"{path.name}:closed envelope",
    )
    if schema is not None:
        require(document["schema"] == schema, f"{path.name}:schema")
    require(type(document["result"]) is dict, f"{path.name}:result object")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"{path.name}:result digest",
    )
    return document


def safe_input_path(path: Path) -> None:
    require(path.parent.resolve().is_dir(), "certificate parent directory")
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), "certificate regular file")
    require(not path.is_symlink(), "certificate symlink forbidden")
    require(info.st_nlink == 1, "certificate hardlink forbidden")
    protected = [
        PRODUCER,
        VERIFIER,
        *[
            HERE / name
            for name in {
                **v129.UPSTREAM_PINS,
                **v129.MATH_HELPER_PINS,
            }
        ],
    ]
    for protected_path in protected:
        try:
            require(
                not os.path.samefile(path, protected_path),
                "certificate aliases protected source",
            )
        except FileNotFoundError:
            pass


def safe_output_path(path: Path, certificate_path: Path) -> None:
    parent = path.parent.resolve()
    require(parent.is_dir(), "output parent directory")
    candidate = (parent / path.name).resolve()
    protected = [
        PRODUCER,
        VERIFIER,
        CERTIFICATE,
        certificate_path,
        ROUND129_CERTIFICATE,
        ROUND129_VERIFIER,
        ROUND129_VERIFICATION,
        *[
            HERE / name
            for name in {
                **v129.UPSTREAM_PINS,
                **v129.MATH_HELPER_PINS,
            }
        ],
    ]
    require(
        all(candidate != item.resolve() for item in protected),
        "output aliases protected path",
    )
    if path.exists() or path.is_symlink():
        info = path.lstat()
        require(not path.is_symlink(), "output symlink forbidden")
        require(stat.S_ISREG(info.st_mode), "output regular file")
        require(info.st_nlink == 1, "output hardlink forbidden")
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(path, protected_path),
                    "output hardlink to protected input/source forbidden",
                )
            except FileNotFoundError:
                pass


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    data = (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent.resolve()),
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def validate_upstream() -> tuple[
    dict[int, dict[str, dict[str, Any]]],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    require(
        sha256(ROUND129_VERIFIER) == ROUND129_VERIFIER_SHA256,
        "Round129 verifier byte pin",
    )
    require(
        sha256(ROUND129_CERTIFICATE) == ROUND129_CERTIFICATE_SHA256,
        "Round129 certificate byte pin",
    )
    require(
        sha256(ROUND129_VERIFICATION) == ROUND129_VERIFICATION_SHA256,
        "Round129 verification byte pin",
    )
    documents = v129.validate_pins()
    core = v129.independent_math_core(documents)
    round129_document = v129.parse_bytes(ROUND129_CERTIFICATE.read_bytes())
    summary = v129.validate_document(round129_document, documents, core)
    require(summary["local_maturity"] == "14/18", "Round129 local maturity")
    require(summary["global_maturity"] == "10/18", "Round129 global maturity")
    require(summary["cm2"] == "NO-GO_FOR_CLAIM", "Round129 CM2")
    verification = closed_document(
        ROUND129_VERIFICATION,
        "cm2.round129.rank3-positive-borel-recut-field-bridge-verification.v1",
    )
    require(verification["result"]["verdict"] == "PASS", "Round129 PASS")
    return documents, core, round129_document["result"], verification["result"]


def adapted3(theta_guard: arb, x: v122.Jet2, s: v122.Jet2) -> v122.Jet2:
    state = v122.source_and_collisions(theta_guard, x, s)
    third = state["actual_third"]
    return (
        v122.Jet2(arb.pi() / 2)
        - third[4].asin()
        + third[6].asin()
    )


def u3_jet(
    theta_guard: arb,
    lower: Q,
    upper: Q,
    *,
    s_collar: bool = False,
) -> v122.Jet2:
    s = (
        v122.Jet2(interval(-S_EPSILON, S_EPSILON), s=arb(1))
        if s_collar
        else v122.Jet2(arb(0))
    )
    zero = adapted3(theta_guard, v122.Jet2(arb(0)), s)
    current = adapted3(
        theta_guard,
        v122.Jet2(interval(lower, upper), x=arb(1)),
        s,
    )
    return zero - current


def guarded_abs_upper(value: arb) -> Q:
    lower, upper = arb_pair(value)
    return max(
        abs(lower - ENCLOSURE_GUARD),
        abs(upper + ENCLOSURE_GUARD),
    )


def validate_closed_registries(result: dict[str, Any]) -> None:
    require(
        digest(sorted(result)) == RESULT_KEYSET_SHA256,
        "certificate result closed schema",
    )
    primary_ids: set[str] = set()
    total = 0
    for group, expected_count in ROW_GROUPS.items():
        rows = result.get(group)
        require(
            type(rows) is list and len(rows) == expected_count,
            f"{group}:row census",
        )
        total += len(rows)
        keyset_pin = ROW_KEYSET_SHA256[group]
        local_ids: set[str] = set()
        primary_key = PRIMARY_ID_KEYS[group]
        for index, row in enumerate(rows):
            require(
                digest(sorted(row)) == keyset_pin,
                f"{group}:{index}:closed row schema",
            )
            row_digest(row, f"{group}:{index}")
            identifier = row.get(primary_key)
            require(type(identifier) is str, f"{group}:{index}:primary ID")
            require(identifier not in local_ids, f"{group}:unique primary ID")
            require(identifier not in primary_ids, "global unique primary ID")
            local_ids.add(identifier)
            primary_ids.add(identifier)
        require(
            result.get(f"{group}_sha256") == digest(rows),
            f"{group}:group digest",
        )
    require(total == 2814, "finite Round130 row census")
    for name, expected in NESTED_KEYSET_SHA256.items():
        value = result.get(name)
        require(type(value) is dict, f"{name}:object")
        require(
            digest(sorted(value)) == expected,
            f"{name}:closed schema",
        )


def validate_frozen_inputs(
    result: dict[str, Any],
    round129: dict[str, Any],
    round129_verification: dict[str, Any],
) -> None:
    frozen = result["frozen_input_contract"]
    require(
        frozen["Round129_primary_byte_pins"]
        == {
            "cm2_round129_rank3_positive_borel_recut_field_bridge.py":
                v129.PRODUCER_SHA256,
            ROUND129_CERTIFICATE.name: ROUND129_CERTIFICATE_SHA256,
            ROUND129_VERIFIER.name: ROUND129_VERIFIER_SHA256,
            ROUND129_VERIFICATION.name: ROUND129_VERIFICATION_SHA256,
        },
        "Round129 primary pins",
    )
    require(
        frozen["Round129_certificate_result_sha256"] == digest(round129),
        "Round129 result pin",
    )
    require(
        frozen["Round129_verification_result_sha256"]
        == digest(round129_verification),
        "Round129 verification result pin",
    )
    require(
        frozen["Round129_verification_verdict"] == "PASS",
        "Round129 verification verdict",
    )
    exact_seed_pins = frozen[
        "Round123_through_Round126_exact_seed_model_byte_pins"
    ]
    expected_names = {
        name
        for round_index in range(123, 127)
        for name in (
            v129.CERTIFICATE_FILES[round_index][0],
            v129.CERTIFICATE_FILES[round_index][1],
            next(
                key
                for key in v129.UPSTREAM_PINS
                if key.startswith(f"cm2_round{round_index}_")
                and key.endswith(".py")
                and "_verifier" not in key
            ),
        )
    }
    require(set(exact_seed_pins) == expected_names, "Round123-126 pin names")
    for name, expected in exact_seed_pins.items():
        require(v129.UPSTREAM_PINS[name] == expected, f"frozen pin:{name}")
    require(
        frozen["Round123_through_Round126_verifications_PASS"] is True,
        "Round123-126 PASS",
    )
    helper_pins = frozen["helper_byte_pins"]
    for name, expected in helper_pins.items():
        require(
            sha256(HERE / name) == expected,
            f"helper byte pin:{name}",
        )


def isolate_lambda_root(lambda_value: Q, root: dict[str, Any]) -> tuple[Q, Q]:
    lower, upper = map(Q, root["uniform_t_guard"])
    source = replace(
        v129.core_cert.physical_cores()[v122.SEED_BRANCH[0]],
        chart_id=v122.SEED_SOURCE_CHART,
    )

    def equation(value: Q) -> arb:
        return v129.round113.equation_value(
            source,
            v122.SEED_BRANCH,
            1,
            "BYPASS",
            value,
            v129.FIXED_C0,
            v129.FIXED_C0,
            lambda_value,
            lambda_value,
        )

    lower_sign = v129.strict_sign(equation(lower))
    upper_sign = v129.strict_sign(equation(upper))
    require((lower_sign, upper_sign) == (1, -1), "lambda test root signs")
    for _ in range(64):
        middle = (lower + upper) / 2
        sign = v129.strict_sign(equation(middle))
        require(sign != 0, "lambda test root bisection")
        if sign == lower_sign:
            lower = middle
        else:
            require(sign == upper_sign, "lambda test root orientation")
            upper = middle
    return lower, upper


def canonical_lambda_test_vectors(
    root: dict[str, Any],
) -> list[dict[str, Any]]:
    family_root_id = root["family_root_id"]
    lower, upper = map(Q, root["lambda_exact_dyadic_closed_collar"])
    require(lower < upper, "canonical lambda collar")
    version = "round130-canonical-exact-lambda-key-v1"
    vectors = (
        (Q(0), "0 followed by infinitely many 0 digits", "NORMALIZED_BINARY"),
        (Q(1, 2), "1 followed by infinitely many 0 digits", "NORMALIZED_BINARY"),
        (Q(1), None, "UPPER_ENDPOINT"),
    )
    result: list[dict[str, Any]] = []
    b_intervals: list[tuple[Q, Q]] = []
    for u, digits, case in vectors:
        lambda_value = lower + u * (upper - lower)
        t_lower, t_upper = isolate_lambda_root(lambda_value, root)
        t_ball = interval(t_lower, t_upper)
        b_ball = aq(v129.FIXED_C0).acos() - aq(Q(36, 25)) * (
            arb.pi() - t_ball.asin()
        )
        b_lower, b_upper = arb_pair(b_ball)
        b_intervals.append((b_lower, b_upper))
        payload: list[Any] = [version, family_root_id, case]
        if case == "NORMALIZED_BINARY":
            payload.append(digits)
        key = "round130-canonical-exact-lambda-key-test:" + digest(payload)
        result.append({
            "normalized_u": qstr(u),
            "exact_lambda": qstr(lambda_value),
            "canonical_case": case,
            "canonical_binary_sequence": digits,
            "nonterminating_eventually_one_alternative_rejected":
                u in (Q(1, 2), Q(1)),
            "test_key": key,
            "derived_b_enclosure": [qstr(b_lower), qstr(b_upper)],
            "independently_supplied_b_key_used": False,
        })
    require(
        b_intervals[0][1] < b_intervals[1][0]
        < b_intervals[1][1] < b_intervals[2][0],
        "lambda to b strict monotone test vectors",
    )
    require(
        len({row["test_key"] for row in result}) == 3,
        "canonical lambda test key uniqueness",
    )
    return result


def validate_exact_lambda_contract(
    result: dict[str, Any],
    *,
    cached_vectors: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    contract = result["exact_lambda_instance_contract"]
    expected = {
        "parameter": "lambda=b3",
        "canonical_exact_lambda_key_version":
            "round130-canonical-exact-lambda-key-v1",
        "mathematical_fibre_key": "(family_root_id, exact real lambda)",
        "closed_collar_endpoint_symbols": {
            "L":
                "positive_Borel_family_root_contract."
                "lambda_exact_dyadic_closed_collar[0]",
            "U":
                "positive_Borel_family_root_contract."
                "lambda_exact_dyadic_closed_collar[1]",
            "strict_order": "L<U",
        },
        "normalized_coordinate": {
            "symbol": "u",
            "definition": "u=(lambda-L)/(U-L)",
            "range": "[0,1]",
        },
        "canonical_exact_lambda_key_case_split": {
            "0<=u<1": {
                "payload":
                    "[round130-canonical-exact-lambda-key-v1,"
                    "family_root_id,NORMALIZED_BINARY,"
                    "the exact binary digit sequence of u]",
                "uniqueness_rule":
                    "use the unique binary expansion that is not eventually all 1",
                "dyadic_rule":
                    "use the terminating expansion, equivalently the expansion "
                    "eventually all 0",
            },
            "u=1": {
                "payload":
                    "[round130-canonical-exact-lambda-key-v1,"
                    "family_root_id,UPPER_ENDPOINT]",
                "binary_digit_sequence_forbidden": True,
            },
        },
        "noncanonical_lambda_locator_rejected": True,
        "canonical_key_determines_one_exact_real_lambda": True,
        "one_exact_real_lambda_has_one_canonical_key": True,
        "derived_exact_b_key":
            "derive b(lambda) only by the strictly increasing Round129 "
            "analytic map from this same canonical exact-lambda key",
        "independently_supplied_b_locator_or_b_key_accepted": False,
        "all_actual_objects_require_one_shared_canonical_exact_lambda_key": True,
        "actual_constructor_key_token_semantics":
            "every canonical-exact-lambda-key token in an actual constructor "
            "means the versioned mathematical fibre key defined here",
        "whole_uncountable_family_finitely_serializable": False,
        "per_exact_lambda_mathematical_template_theorem_requires_finite_serialization":
            False,
        "finite_rows_are_templates_not_uncountably_many_actual_rows": True,
        "cross_fibre_object_identification_or_cancellation_forbidden": True,
    }
    require(contract == expected, "canonical exact-lambda contract")
    return (
        canonical_lambda_test_vectors(
            result["positive_Borel_family_root_contract"]
        )
        if cached_vectors is None
        else cached_vectors
    )


def point_state(theta_guard: arb, x: Q) -> dict[str, Any]:
    return v122.source_and_collisions(
        theta_guard,
        v122.Jet2(aq(x)),
        v122.Jet2(arb(0)),
    )


def validate_stage3_geometry(
    result: dict[str, Any],
    round129: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
) -> dict[str, Any]:
    family_root_id = round129["positive_Borel_family_root_contract"][
        "family_root_id"
    ]
    require(
        result["positive_Borel_family_root_contract"]
        == round129["positive_Borel_family_root_contract"],
        "Round129 family root inherited exactly",
    )
    theta_guard = core["theta_guard"]
    stage3_whole = u3_jet(theta_guard, Q(0), Q(1))
    stage3_end = u3_jet(theta_guard, Q(1), Q(1))
    ratio = stage3_end.value / aq(DELTA)
    derivative_ratio = stage3_whole.x / aq(DELTA)
    ratio_lower, ratio_upper = arb_pair(ratio)
    derivative_lower, derivative_upper = arb_pair(derivative_ratio)
    require(
        192 < ratio_lower <= ratio_upper < 193,
        "independent U3 length",
    )
    require(
        192 < derivative_lower <= derivative_upper < 193,
        "independent U3 derivative",
    )

    geometry_contract = result["family_stage3_geometry_contract"]
    interval_contains(
        geometry_contract["U3_length_over_delta_enclosure"],
        ratio,
        "U3 length contract",
    )
    interval_contains(
        geometry_contract["U3_x_over_delta_enclosure"],
        derivative_ratio,
        "U3 derivative contract",
    )
    require(
        geometry_contract["Round123_240_bisection_exact_seed_brackets_reused"]
        is False,
        "Round123 narrow guards not reused",
    )
    require(
        qvalue(
            geometry_contract["family_guard_radius_each_side"],
            "stage3 guard radius",
        )
        == STAGE3_GUARD_RADIUS,
        "stage3 guard radius",
    )

    frozen_endpoints = sorted(
        documents[123]["certificate"]["result"]["stage3_endpoint_rows"],
        key=lambda row: row["natural_index_j"],
    )
    endpoint_rows = sorted(
        result["uniform_stage3_endpoint_guard_template_rows"],
        key=lambda row: row["natural_index_j"],
    )
    require(
        [row["natural_index_j"] for row in frozen_endpoints]
        == [row["natural_index_j"] for row in endpoint_rows]
        == list(range(1, 193)),
        "192 ordered stage3 endpoint levels",
    )
    endpoint_by_id: dict[str, dict[str, Any]] = {}
    endpoint_guard: dict[str, tuple[Q, Q]] = {}
    for frozen, row in zip(frozen_endpoints, endpoint_rows):
        level = row["natural_index_j"]
        frozen_lower, frozen_upper = map(Q, frozen["x_dyadic_bracket"])
        center = (frozen_lower + frozen_upper) / 2
        expected_guard = (
            center - STAGE3_GUARD_RADIUS,
            center + STAGE3_GUARD_RADIUS,
        )
        stored_guard = qinterval(
            row["uniform_x_dyadic_guard"],
            f"stage3 guard:{level}",
        )
        require(stored_guard == expected_guard, f"stage3 widened guard:{level}")
        left = u3_jet(theta_guard, stored_guard[0], stored_guard[0])
        right = u3_jet(theta_guard, stored_guard[1], stored_guard[1])
        target = aq(level * DELTA)
        require(
            bool(left.value - target < 0)
            and bool(right.value - target > 0),
            f"stage3 endpoint signs:{level}",
        )
        local = u3_jet(theta_guard, *stored_guard)
        local_derivative = local.x / aq(DELTA)
        local_lower, local_upper = arb_pair(local_derivative)
        require(
            192 < local_lower <= local_upper < 193,
            f"stage3 endpoint derivative:{level}",
        )
        expected_id = row_id(
            "stage3-endpoint-template",
            [family_root_id, level],
        )
        require(
            row["stage3_endpoint_template_id"] == expected_id,
            f"stage3 endpoint ID:{level}",
        )
        require(
            row["family_root_id"] == family_root_id
            and row["stage"] == 3
            and row["exact_level_equation"]
            == f"U3(lambda,x)={level}*10^-90",
            f"stage3 endpoint metadata:{level}",
        )
        require(
            row["Round123_exact_seed_endpoint_id"] == frozen["endpoint_id"],
            f"stage3 frozen endpoint crosslink:{level}",
        )
        require(
            row["all_lambda_left_function_sign"] == -1
            and row["all_lambda_right_function_sign"] == 1,
            f"stage3 stored signs:{level}",
        )
        interval_contains(
            row["all_lambda_normalized_U3_x_strict_enclosure"],
            local_derivative,
            f"stage3 stored derivative:{level}",
        )
        require(
            row["unique_root_for_every_exact_lambda"] is True
            and row["unique_analytic_lambda_graph_by_IFT"] is True
            and row[
                "canonical_exact_lambda_key_required_for_actual_endpoint_ID"
            ]
            is True
            and row["numeric_guard_text_participates_in_actual_endpoint_ID"]
            is False,
            f"stage3 endpoint semantics:{level}",
        )
        endpoint_by_id[expected_id] = row
        endpoint_guard[expected_id] = stored_guard

    outer_left = "round129-family-source-outer-left"
    outer_right = "round129-family-source-outer-right"
    natural_rows = sorted(
        result["parameterized_stage3_natural_cell_template_rows"],
        key=lambda row: row["natural_index_j"],
    )
    endpoint_ids = [
        outer_left,
        *(row["stage3_endpoint_template_id"] for row in endpoint_rows),
        outer_right,
    ]
    require(len(natural_rows) == 193, "stage3 natural cells")
    stored_ratio_lower, stored_ratio_upper = qinterval(
        geometry_contract["U3_length_over_delta_enclosure"],
        "stored U3 ratio",
    )
    for index, row in enumerate(natural_rows):
        expected_length = (
            ["1", "1"]
            if index < 192
            else [
                qstr(stored_ratio_lower - 192),
                qstr(stored_ratio_upper - 192),
            ]
        )
        require(
            row["stage3_natural_cell_template_id"]
            == row_id(
                "stage3-natural-cell-template",
                [family_root_id, index],
            ),
            f"stage3 natural cell ID:{index}",
        )
        require(
            row["family_root_id"] == family_root_id
            and row["lower_endpoint_template_id"] == endpoint_ids[index]
            and row["upper_endpoint_template_id"] == endpoint_ids[index + 1]
            and row["normalized_adapted_length_enclosure"]
            == expected_length
            and row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["terminal_partial_cell"] == (index == 192)
            and row[
                "canonical_exact_lambda_key_required_for_actual_recut_ID"
            ]
            is True,
            f"stage3 natural cell:{index}",
        )

    cut_specs: list[dict[str, Any]] = []
    round129_faces = {
        row["face_template_id"]: row
        for row in round129["uniform_pullback_face_guard_rows"]
    }
    for row in round129_faces.values():
        guard = tuple(map(Q, row["uniform_x_dyadic_guard"]))
        u3 = u3_jet(theta_guard, *guard).value / aq(DELTA)
        cut_specs.append({
            "endpoint": row["face_template_id"],
            "origin": "ROUND121_EXISTING_INPUT_CUT",
            "stage": row["stage"],
            "natural_index_j": row["natural_index_j"],
            "guard": guard,
            "u3": u3,
        })
    for row in endpoint_rows:
        level = row["natural_index_j"]
        identifier = row["stage3_endpoint_template_id"]
        cut_specs.append({
            "endpoint": identifier,
            "origin": "ROUND123_STAGE3_OUTPUT_CUT",
            "stage": 3,
            "natural_index_j": level,
            "guard": endpoint_guard[identifier],
            "u3": None,
        })
    cut_specs.sort(key=lambda item: item["guard"][0])
    require(len(cut_specs) == 215, "combined cut census")
    gaps = [
        right["guard"][0] - left["guard"][1]
        for left, right in zip(cut_specs, cut_specs[1:])
    ]
    require(len(gaps) == 214 and min(gaps) > 0, "combined cut ordering")
    merged_rows = sorted(
        result["parameterized_merged_cut_template_rows"],
        key=lambda row: row["merged_rank"],
    )
    for rank, (spec, row) in enumerate(zip(cut_specs, merged_rows)):
        expected_id = row_id(
            "merged-cut-template",
            [
                family_root_id,
                spec["origin"],
                spec["stage"],
                spec["natural_index_j"],
                spec["endpoint"],
            ],
        )
        require(
            row["merged_cut_template_id"] == expected_id
            and row["merged_rank"] == rank
            and row["family_root_id"] == family_root_id
            and row["endpoint_template_id"] == spec["endpoint"]
            and row["origin"] == spec["origin"]
            and row["stage"] == spec["stage"]
            and row["natural_index_j"] == spec["natural_index_j"]
            and tuple(map(Q, row["uniform_x_dyadic_guard"]))
            == spec["guard"]
            and row[
                "canonical_exact_lambda_key_required_for_actual_cut_ID"
            ]
            is True,
            f"merged cut:{rank}",
        )
        if spec["u3"] is None:
            require(
                row["U3_over_delta_enclosure"]
                == [
                    str(spec["natural_index_j"]),
                    str(spec["natural_index_j"]),
                ],
                f"stage3 exact cut level:{rank}",
            )
        else:
            interval_overlaps(
                row["U3_over_delta_enclosure"],
                spec["u3"],
                f"existing cut U3:{rank}",
            )
    require(
        geometry_contract["combined_internal_cut_count"] == 215
        and geometry_contract["minimum_combined_x_gap"] == qstr(min(gaps)),
        "combined cut contract",
    )

    boundary_specs = [
        {
            "endpoint": outer_left,
            "origin": "SOURCE_OUTER_LEFT",
            "guard": (Q(0), Q(0)),
        },
        *cut_specs,
        {
            "endpoint": outer_right,
            "origin": "SOURCE_OUTER_RIGHT",
            "guard": (Q(1), Q(1)),
        },
    ]
    common_rows = {
        row["common_rank"]: row
        for row in round129["parameterized_common_rank_template_rows"]
    }
    fragments = sorted(
        result["parameterized_stage3_output_fragment_template_rows"],
        key=lambda row: row["fragment_rank"],
    )
    fragments_by_rank: dict[int, list[dict[str, Any]]] = defaultdict(list)
    input_rank = 0
    stage3_index = 0
    minimum_stage3_length: Q | None = None
    for fragment_rank, (lower_spec, upper_spec, row) in enumerate(
        zip(boundary_specs, boundary_specs[1:], fragments)
    ):
        lower_inside = lower_spec["guard"][1]
        upper_inside = upper_spec["guard"][0]
        require(lower_inside < upper_inside, f"fragment gap:{fragment_rank}")
        upper_u3 = u3_jet(theta_guard, upper_inside, upper_inside).value
        lower_u3 = u3_jet(theta_guard, lower_inside, lower_inside).value
        output_length = (upper_u3 - lower_u3) / aq(DELTA)
        length_lower, length_upper = arb_pair(output_length)
        require(
            Q(4, 125) < length_lower <= length_upper,
            f"independent stage3 fragment length:{fragment_rank}",
        )
        minimum_stage3_length = (
            length_lower
            if minimum_stage3_length is None
            else min(minimum_stage3_length, length_lower)
        )
        expected_id = row_id(
            "stage3-output-fragment-template",
            [
                family_root_id,
                input_rank,
                lower_spec["endpoint"],
                upper_spec["endpoint"],
                stage3_index,
            ],
        )
        common = common_rows[input_rank]
        require(
            row["output_fragment_template_id"] == expected_id
            and row["fragment_rank"] == fragment_rank
            and row["family_root_id"] == family_root_id
            and row["common_rank"] == input_rank
            and row["common_rank_template_id"]
            == common["common_rank_template_id"]
            and row["source_x_lower_endpoint_template_id"]
            == lower_spec["endpoint"]
            and row["source_x_upper_endpoint_template_id"]
            == upper_spec["endpoint"]
            and row["stage3_natural_index_j"] == stage3_index
            and row["stage3_natural_cell_template_id"]
            == natural_rows[stage3_index][
                "stage3_natural_cell_template_id"
            ]
            and qvalue(
                row["source_x_open_gap_strict_lower"],
                f"fragment gap stored:{fragment_rank}",
            )
            == upper_inside - lower_inside
            and row[
                "canonical_exact_lambda_key_required_for_actual_fragment"
            ]
            is True
            and row["finite_row_is_a_template_not_an_actual_fibre_fragment"]
            is True,
            f"stage3 fragment metadata:{fragment_rank}",
        )
        interval_contains(
            row["normalized_stage3_output_length_strict_enclosure"],
            output_length,
            f"stage3 fragment length stored:{fragment_rank}",
        )
        fragments_by_rank[input_rank].append(row)
        crossed = upper_spec["origin"]
        if crossed == "ROUND121_EXISTING_INPUT_CUT":
            input_rank += 1
        elif crossed == "ROUND123_STAGE3_OUTPUT_CUT":
            stage3_index += 1
    require(
        input_rank == 23 and stage3_index == 192,
        "terminal fragment indices",
    )

    partitions = sorted(
        result["parameterized_child_output_partition_template_rows"],
        key=lambda row: row["common_rank"],
    )
    histogram: Counter[str] = Counter()
    for rank, row in enumerate(partitions):
        parts = fragments_by_rank[rank]
        ids = [item["output_fragment_template_id"] for item in parts]
        histogram[str(len(parts))] += 1
        require(
            row["child_output_partition_template_id"]
            == row_id(
                "child-output-partition-template",
                [family_root_id, rank, ids],
            )
            and row["family_root_id"] == family_root_id
            and row["common_rank"] == rank
            and row["common_rank_template_id"]
            == common_rows[rank]["common_rank_template_id"]
            and row["output_fragment_template_ids"] == ids
            and row["output_fragment_count"] == len(ids)
            and row["stage3_natural_index_span"]
            == [
                parts[0]["stage3_natural_index_j"],
                parts[-1]["stage3_natural_index_j"],
            ]
            and row["source_partition_lower_endpoint_template_id"]
            == parts[0]["source_x_lower_endpoint_template_id"]
            and row["source_partition_upper_endpoint_template_id"]
            == parts[-1]["source_x_upper_endpoint_template_id"]
            and row[
                "disjoint_half_open_union_equals_actual_input_child_per_exact_lambda"
            ]
            is True
            and row[
                "canonical_exact_lambda_key_required_for_actual_partition"
            ]
            is True,
            f"child partition:{rank}",
        )
    expected_histogram = {
        "2": 1,
        "3": 1,
        "4": 2,
        "5": 1,
        "6": 2,
        "7": 1,
        "8": 1,
        "9": 2,
        "10": 1,
        "11": 1,
        "12": 11,
    }
    require(dict(histogram) == expected_histogram, "fragment histogram")

    face_guard = {
        row["face_template_id"]: tuple(map(Q, row["uniform_x_dyadic_guard"]))
        for row in round129["uniform_pullback_face_guard_rows"]
    }
    face_guard[outer_left] = (Q(0), Q(0))
    face_guard[outer_right] = (Q(1), Q(1))
    base_rows = round129["parameterized_base_key_template_rows"]
    bases_by_rank_stage: dict[tuple[int, int], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for base in base_rows:
        bases_by_rank_stage[(base["common_rank"], base["stage"])].append(base)
    legs = {
        (row["common_rank"], row["stage"]): row
        for row in result["parameterized_accepted_norm_leg_template_rows"]
    }
    stage_minima: dict[int, Q | None] = {0: None, 1: None, 2: None}
    for rank in range(24):
        common = common_rows[rank]
        lower_inside = face_guard[common["lower_face_template_id"]][1]
        upper_inside = face_guard[common["upper_face_template_id"]][0]
        lower_state = point_state(theta_guard, lower_inside)
        upper_state = point_state(theta_guard, upper_inside)
        independent_lengths = {
            0: lower_state["a1"].value - upper_state["a1"].value,
            1: upper_state["a2"].value - lower_state["a2"].value,
        }
        for stage in range(3):
            row = legs[(rank, stage)]
            bases = sorted(
                bases_by_rank_stage[(rank, stage)],
                key=lambda item: item["roof_level_j"],
            )
            input_recut = (
                common["source_recut_template_id"],
                common["first_image_recut_template_id"],
                common["second_image_recut_template_id"],
            )[stage]
            if stage == 0:
                expected_outputs = [common["first_image_recut_template_id"]]
            elif stage == 1:
                expected_outputs = [common["second_image_recut_template_id"]]
            else:
                expected_outputs = [
                    item["output_fragment_template_id"]
                    for item in fragments_by_rank[rank]
                ]
            require(
                row["accepted_norm_leg_template_id"]
                == row_id(
                    "accepted-norm-leg-template",
                    [family_root_id, rank, stage],
                )
                and row["family_root_id"] == family_root_id
                and row["common_rank"] == rank
                and row["common_rank_template_id"]
                == common["common_rank_template_id"]
                and row["official_word_key_id"]
                == bases[0]["official_word_key_id"]
                and row["roof_level_js"]
                == [item["roof_level_j"] for item in bases]
                and row["roof_level_count"] == STAGE_RETURN_LENGTH[stage]
                and row["materialized_input_recut_template_id"] == input_recut
                and row["actual_collision_owner"] == STAGE_OWNER[stage]
                and row["actual_collision_chart"] == STAGE_CHART[stage]
                and row["output_geometry_member_template_ids"]
                == expected_outputs
                and row["output_member_count"] == len(expected_outputs)
                and row[
                    "canonical_exact_lambda_key_required_for_all_actual_objects"
                ]
                is True,
                f"accepted leg:{rank}:{stage}",
            )
            if stage < 2:
                normalized = independent_lengths[stage] / aq(DELTA)
                require(
                    len(row[
                        "normalized_output_member_length_strict_enclosures"
                    ])
                    == 1,
                    f"accepted leg singleton:{rank}:{stage}",
                )
                interval_contains(
                    row[
                        "normalized_output_member_length_strict_enclosures"
                    ][0],
                    normalized,
                    f"accepted leg length:{rank}:{stage}",
                )
                lower_bound = arb_pair(normalized)[0]
            else:
                require(
                    row[
                        "normalized_output_member_length_strict_enclosures"
                    ]
                    == [
                        item[
                            "normalized_stage3_output_length_strict_enclosure"
                        ]
                        for item in fragments_by_rank[rank]
                    ],
                    f"accepted stage3 member lengths:{rank}",
                )
                lower_bound = min(
                    Q(pair[0])
                    for pair in row[
                        "normalized_output_member_length_strict_enclosures"
                    ]
                )
            threshold = (Q(3, 100), Q(17, 200), Q(4, 125))[stage]
            require(lower_bound > threshold, f"accepted threshold:{rank}:{stage}")
            stage_minima[stage] = (
                lower_bound
                if stage_minima[stage] is None
                else min(stage_minima[stage], lower_bound)
            )
    require(
        geometry_contract["stage3_output_fragment_count"] == 216
        and geometry_contract["fragment_count_histogram"]
        == expected_histogram
        and geometry_contract["strict_thresholds_by_stage"]
        == {"0": "3/100", "1": "17/200", "2": "4/125"},
        "geometry summary census",
    )
    for stage in range(3):
        stored_stage_minimum = min(
            Q(pair[0])
            for row in legs.values()
            if row["stage"] == stage
            for pair in row[
                "normalized_output_member_length_strict_enclosures"
            ]
        )
        require(
            qvalue(
                geometry_contract["minimum_normalized_output_length_by_stage"][
                    str(stage)
                ],
                f"stage minimum:{stage}",
            )
            == stored_stage_minimum,
            f"stage minimum crosslink:{stage}",
        )
    return {
        "theta_guard": theta_guard,
        "family_root_id": family_root_id,
        "endpoint_rows": endpoint_rows,
        "natural_rows": natural_rows,
        "merged_rows": merged_rows,
        "cut_specs": cut_specs,
        "fragment_rows": fragments,
        "fragments_by_rank": fragments_by_rank,
        "partition_rows": partitions,
        "leg_rows": legs,
        "common_rows": common_rows,
        "base_rows": base_rows,
        "bases_by_rank_stage": bases_by_rank_stage,
        "face_guard": face_guard,
        "u3_ratio": [qstr(ratio_lower), qstr(ratio_upper)],
        "u3_derivative": [qstr(derivative_lower), qstr(derivative_upper)],
        "minimum_combined_gap": qstr(min(gaps)),
        "minimum_stage3_length": qstr(minimum_stage3_length),
        "stage_minima": {
            str(stage): qstr(value)  # type: ignore[arg-type]
            for stage, value in stage_minima.items()
        },
    }


def source_field_map(
    round129: dict[str, Any],
) -> dict[tuple[str, int], dict[str, Any]]:
    rows = round129["parameterized_F1_F13_F16_slot_template_rows"]
    result = {
        (row["base_key_template_id"], row["field_index"]): row
        for row in rows
    }
    require(len(result) == 1680, "Round129 field source map")
    require(
        {field for _, field in result}
        == set(range(1, 14)) | {16},
        "Round129 field source indices",
    )
    return result


def base_metadata(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["common_rank"],
        row["stage"],
        row["official_word_key_id"],
        row["roof_level_j"],
        row["materialized_input_recut_template_id"],
    )


def validate_f14_f15(
    result: dict[str, Any],
    round129: dict[str, Any],
    geometry: dict[str, Any],
) -> dict[str, Any]:
    family_root_id = geometry["family_root_id"]
    bases = {
        row["base_key_template_id"]: row for row in geometry["base_rows"]
    }
    fields = source_field_map(round129)
    legs = geometry["leg_rows"]
    f14_rows = {
        row["base_key_template_id"]: row
        for row in result["parameterized_F14_slot_template_rows"]
    }
    require(set(f14_rows) == set(bases), "F14 base coverage")
    for key, base in bases.items():
        row = f14_rows[key]
        leg = legs[(base["common_rank"], base["stage"])]
        require(
            row["field_slot_template_id"]
            == row_id("field14-slot-template", [family_root_id, key])
            and row["base_key_template_id"] == key
            and row["family_root_id"] == family_root_id
            and base_metadata(row) == base_metadata(base)
            and row["field_index"] == 14
            and row["field_name"] == FIELD_NAMES[14]
            and row["field_value_or_contract"] == str(F14_ONE_STEP)
            and row["field_bound_semantics"] == "STRICT_UPPER"
            and row["accepted_norm_leg_template_id"]
            == leg["accepted_norm_leg_template_id"]
            and row["accepted_norm_leg_template_sha256"]
            == leg["row_sha256"]
            and row["output_geometry_member_template_ids"]
            == leg["output_geometry_member_template_ids"]
            and row["output_member_count"] == leg["output_member_count"]
            and row["same_key_F10_slot_template_id"]
            == fields[(key, 10)]["field_slot_template_id"]
            and row["same_key_F13_slot_template_id"]
            == fields[(key, 13)]["field_slot_template_id"]
            and row["same_key_F16_slot_template_id"]
            == fields[(key, 16)]["field_slot_template_id"]
            and row[
                "Round129_F10_zero_is_dependency_only_not_F14_payment"
            ]
            is True
            and row["signed_Jordan_extension_installed"] is True
            and row["roof_slot_value_is_one_step_not_path_product"] is True
            and row["transparent_wall_roof_split_adds_no_F14_factor"] is True
            and row[
                "canonical_exact_lambda_key_required_for_actual_slot"
            ]
            is True
            and row["finite_row_is_a_template_not_an_actual_fibre_slot"]
            is True,
            f"F14 slot:{key}",
        )

    cemetery_rows = {
        (row["common_rank"], row["stage"]): row
        for row in result[
            "parameterized_relative_zero_cemetery_template_rows"
        ]
    }
    operator_rows = {
        (row["common_rank"], row["stage"]): row
        for row in result[
            "parameterized_standard_family_operator_template_rows"
        ]
    }
    require(
        len(cemetery_rows) == len(operator_rows) == 72,
        "F15 carrier census",
    )
    for rank in range(24):
        for stage in range(3):
            leg = legs[(rank, stage)]
            cemetery = cemetery_rows[(rank, stage)]
            cemetery_id = row_id(
                "relative-zero-cemetery-template",
                [family_root_id, rank, stage],
            )
            require(
                cemetery["relative_zero_cemetery_template_id"]
                == cemetery_id
                and cemetery["family_root_id"] == family_root_id
                and cemetery["common_rank"] == rank
                and cemetery["stage"] == stage
                and cemetery["materialized_input_recut_template_id"]
                == leg["materialized_input_recut_template_id"]
                and cemetery["output_geometry_member_template_ids"]
                == leg["output_geometry_member_template_ids"]
                and cemetery[
                    "partition_is_disjoint_half_open_and_exhaustive_per_exact_lambda"
                ]
                is True
                and cemetery[
                    "endpoint_set_has_adapted_length_measure_zero"
                ]
                is True
                and cemetery["accepted_densities_are_absolutely_continuous"]
                is True
                and cemetery["input_mass_equals_sum_of_tagged_output_masses"]
                is True
                and cemetery["discarded_relative_domain_complement"] == "EMPTY"
                and cemetery["restricted_relative_cemetery_arrival_kernel"]
                == "ZERO"
                and cemetery["ambient_pre_regularization_cemetery"]
                == "NOT_INSTALLED"
                and cemetery["all_time_owner_cemetery"] == "NOT_INSTALLED"
                and cemetery["cross_child_cross_tag_deduplication"]
                == "FORBIDDEN"
                and cemetery[
                    "canonical_exact_lambda_key_required_for_actual_cemetery_row"
                ]
                is True,
                f"relative cemetery:{rank}:{stage}",
            )

            bases_for_leg = sorted(
                geometry["bases_by_rank_stage"][(rank, stage)],
                key=lambda row: row["roof_level_j"],
            )
            operator = operator_rows[(rank, stage)]
            expected_f14 = [
                f14_rows[base["base_key_template_id"]][
                    "field_slot_template_id"
                ]
                for base in bases_for_leg
            ]
            expected_f7 = [
                fields[(base["base_key_template_id"], 7)][
                    "field_slot_template_id"
                ]
                for base in bases_for_leg
            ]
            require(
                operator["standard_family_operator_template_id"]
                == row_id(
                    "standard-family-operator-template",
                    [family_root_id, rank, stage],
                )
                and operator["family_root_id"] == family_root_id
                and operator["common_rank"] == rank
                and operator["stage"] == stage
                and operator["official_word_key_id"]
                == leg["official_word_key_id"]
                and operator["roof_level_js"] == leg["roof_level_js"]
                and operator["materialized_input_recut_template_id"]
                == leg["materialized_input_recut_template_id"]
                and operator["accepted_norm_leg_template_id"]
                == leg["accepted_norm_leg_template_id"]
                and operator["same_key_F14_slot_template_ids"]
                == expected_f14
                and operator["same_key_F7_slot_template_ids"] == expected_f7
                and operator["output_geometry_member_template_ids"]
                == leg["output_geometry_member_template_ids"]
                and operator["output_member_count"] == leg["output_member_count"]
                and operator["memberwise_strong_norm_cost_strict_upper"]
                == "34"
                and operator["relative_zero_cemetery_template_id"]
                == cemetery_id
                and operator[
                    "tag_preserving_and_no_cross_member_deduplication"
                ]
                is True
                and operator[
                    "canonical_exact_lambda_key_required_for_actual_operator"
                ]
                is True,
                f"standard family operator:{rank}:{stage}",
            )
            tags = operator["output_member_tag_templates"]
            require(
                type(tags) is list
                and len(tags) == leg["output_member_count"]
                and operator["output_member_tag_templates_sha256"]
                == digest(tags),
                f"operator output tags:{rank}:{stage}",
            )
            for tag, output_id in zip(
                tags, leg["output_geometry_member_template_ids"]
            ):
                require(
                    tag["geometry_output_member_template_id"] == output_id
                    and tag["same_canonical_exact_lambda_key_required"]
                    is True
                    and tag["geometry_coincidence_does_not_identify_tags"]
                    is True
                    and "canonical-exact-lambda-key"
                    in tag["actual_tag_constructor"],
                    f"operator tag:{rank}:{stage}",
                )

    f15_rows = {
        row["base_key_template_id"]: row
        for row in result["parameterized_F15_slot_template_rows"]
    }
    require(set(f15_rows) == set(bases), "F15 base coverage")
    for key, base in bases.items():
        row = f15_rows[key]
        operator = operator_rows[(base["common_rank"], base["stage"])]
        require(
            row["field_slot_template_id"]
            == row_id("field15-slot-template", [family_root_id, key])
            and row["family_root_id"] == family_root_id
            and base_metadata(row) == base_metadata(base)
            and row["field_index"] == 15
            and row["field_name"] == FIELD_NAMES[15]
            and row["field_value_or_contract"] == str(F15_ONE_STEP)
            and row["field_bound_semantics"] == "STRICT_UPPER"
            and row["same_key_F7_slot_template_id"]
            == fields[(key, 7)]["field_slot_template_id"]
            and row["same_key_F14_slot_template_id"]
            == f14_rows[key]["field_slot_template_id"]
            and row["standard_family_operator_template_id"]
            == operator["standard_family_operator_template_id"]
            and row["standard_family_operator_template_sha256"]
            == operator["row_sha256"]
            and row["relative_zero_cemetery_template_id"]
            == operator["relative_zero_cemetery_template_id"]
            and row[
                "finite_positive_family_then_countable_Tonelli_completion"
            ]
            is True
            and row[
                "signed_Jordan_standard_family_extension_installed"
            ]
            is True
            and row[
                "canonical_exact_lambda_key_required_for_actual_slot"
            ]
            is True
            and row["finite_row_is_a_template_not_an_actual_fibre_slot"]
            is True,
            f"F15 slot:{key}",
        )

    f14_contract = result["per_fibre_F14_contract"]
    require(
        f14_contract
        == {
            "status": "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE",
            "accepted_norm": "N(W,M,rho)=M*(1+Reg_1/3(rho)+1/L)",
            "one_step_F14_strict_upper": "34",
            "stagewise_output_length_strict_lowers":
                ["3/100", "17/200", "4/125"],
            "family_inverse_length_bound":
                "sum_j M_j/ell_j<(100/(3*delta))*M",
            "fragment_count_multiplier": "NONE",
            "arbitrary_positive_density": True,
            "signed_Jordan_extension": True,
        },
        "F14 family contract",
    )
    cp_delta = Q(1_441_974_652, 358_863)
    source_coefficients = [Q(200), Q(100, 3), Q(200, 17)]
    output_coefficients = [Q(100, 3), Q(200, 17), Q(125, 4)]
    require(
        all(
            cp_delta > value
            for value in source_coefficients + output_coefficients
        ),
        "independent F15 properness arithmetic",
    )
    f15_contract = result["per_fibre_F15_and_cemetery_contract"]
    require(
        f15_contract["status"]
        == "CERTIFIED_ON_EVERY_ACCEPTED_FAMILY_IN_EVERY_EXACT_LAMBDA_FIBRE"
        and f15_contract["one_step_F15_strict_upper"] == "34"
        and f15_contract["Tonelli_mass_identity"]
        == "sum_(a,j) M_aj=sum_a M_a"
        and f15_contract["countable_projective_completion"] is True
        and f15_contract["signed_Jordan_completion"] is True
        and f15_contract["fragment_or_member_count_multiplier"] == "NONE"
        and f15_contract["adapted_Cp_star_times_delta"] == qstr(cp_delta)
        and f15_contract["source_inverse_length_coefficients"]
        == [qstr(value) for value in source_coefficients]
        and f15_contract["output_inverse_length_coefficients"]
        == [qstr(value) for value in output_coefficients]
        and f15_contract["all_stage_inputs_and_outputs_strictly_proper"]
        is True
        and f15_contract["per_fibre_recovery_clock"] == 0
        and f15_contract["restricted_relative_cemetery"] == "ZERO"
        and f15_contract["ambient_pre_regularization_cemetery"]
        == "NOT_INSTALLED"
        and f15_contract["all_time_owner_cemetery"] == "NOT_INSTALLED"
        and f15_contract["global_raw_Z_Orlicz_owner_drift_claimed"] is False,
        "F15 and cemetery scope",
    )
    return {
        "fields": fields,
        "f14_rows": f14_rows,
        "cemetery_rows": cemetery_rows,
        "operator_rows": operator_rows,
        "f15_rows": f15_rows,
    }


def validate_f17(
    result: dict[str, Any],
    round129: dict[str, Any],
    geometry: dict[str, Any],
    f14_f15: dict[str, Any],
) -> dict[str, Any]:
    family_root_id = geometry["family_root_id"]
    fields = f14_f15["fields"]
    operator_rows = f14_f15["operator_rows"]
    f15_rows = f14_f15["f15_rows"]
    artificial = round129["parameterized_artificial_face_registry"]
    incidence129 = {
        row["common_rank"]: row
        for row in artificial["child_face_incidence_template_rows"]
    }
    face129 = {
        row["face_template_id"]: row
        for row in (
            artificial["moving_artificial_face_template_rows"]
            + artificial["stationary_outer_face_template_rows"]
        )
    }
    require(
        len(incidence129) == 24 and len(face129) == 25,
        "Round129 artificial registry",
    )

    input_rows = result[
        "parameterized_input_artificial_trace_template_rows"
    ]
    input_map: dict[tuple[int, int, str], dict[str, Any]] = {}
    for row in input_rows:
        key = (row["common_rank"], row["stage"], row["side"])
        require(key not in input_map, "unique input trace key")
        input_map[key] = row
    require(
        set(input_map)
        == {
            (rank, stage, side)
            for rank in range(24)
            for stage in range(3)
            for side in ("lower", "upper")
        },
        "input trace key census",
    )
    for rank in range(24):
        incidence = incidence129[rank]
        for stage in range(3):
            operator = operator_rows[(rank, stage)]
            for side, orientation in (("lower", -1), ("upper", 1)):
                row = input_map[(rank, stage, side)]
                source_trace = incidence[f"{side}_trace_template_id"]
                source_face = incidence[f"{side}_face_template_id"]
                speed = Q(face129[source_face][
                    "implicit_x_s_first_derivative_actual_abs_upper"
                ])
                jacobian = ADAPTED_X_DERIVATIVE_BOUND[stage]
                coefficient = speed * jacobian
                require(speed < 13 and coefficient < 13, "trace speed bounds")
                expected_tag = row_id(
                    "input-family-tag-domain-template",
                    [
                        family_root_id,
                        operator["standard_family_operator_template_id"],
                        stage,
                    ],
                )
                require(
                    row["input_artificial_trace_template_id"]
                    == row_id(
                        "input-artificial-trace-template",
                        [
                            family_root_id,
                            rank,
                            stage,
                            side,
                            source_trace,
                        ],
                    )
                    and row["family_root_id"] == family_root_id
                    and row["orientation_sign"] == orientation
                    and row["common_rank_template_id"]
                    == geometry["common_rows"][rank][
                        "common_rank_template_id"
                    ]
                    and row["standard_family_operator_template_id"]
                    == operator["standard_family_operator_template_id"]
                    and row["materialized_input_recut_template_id"]
                    == operator["materialized_input_recut_template_id"]
                    and row["source_family_tag_domain_template_id"]
                    == expected_tag
                    and row["Round129_source_trace_template_id"]
                    == source_trace
                    and row["Round129_source_face_template_id"] == source_face
                    and Q(row["source_face_speed_actual_abs_upper"]) == speed
                    and Q(row[
                        "stage_adapted_coordinate_x_derivative_bound"
                    ])
                    == jacobian
                    and Q(row[
                        "source_x_to_adapted_trace_coefficient_actual_upper"
                    ])
                    == coefficient
                    and row["adapted_jacobian_factor_is_present"] is True
                    and row["artificial_not_physical"] is True
                    and row[
                        "physical_empty_crosswalk_does_not_erase_this_trace"
                    ]
                    is True
                    and row["cross_family_member_tag_cancellation_allowed"]
                    is False
                    and row[
                        "canonical_exact_lambda_key_required_for_actual_trace"
                    ]
                    is True,
                    f"input trace:{rank}:{stage}:{side}",
                )

    input_incidence_rows = sorted(
        result["parameterized_input_trace_incidence_template_rows"],
        key=lambda row: (row["stage"], row["lower_common_rank"]),
    )
    require(len(input_incidence_rows) == 69, "input incidence census")
    for row in input_incidence_rows:
        stage = row["stage"]
        rank = row["lower_common_rank"]
        left = input_map[(rank, stage, "upper")]
        right = input_map[(rank + 1, stage, "lower")]
        require(
            left["Round129_source_face_template_id"]
            == right["Round129_source_face_template_id"],
            f"input shared face:{rank}:{stage}",
        )
        require(
            left["source_family_tag_domain_template_id"]
            != right["source_family_tag_domain_template_id"],
            f"input distinct tags:{rank}:{stage}",
        )
        require(
            row["input_trace_incidence_template_id"]
            == row_id(
                "input-trace-incidence-template",
                [family_root_id, stage, rank],
            )
            and row["family_root_id"] == family_root_id
            and row["upper_common_rank"] == rank + 1
            and row["shared_face_template_id"]
            == left["Round129_source_face_template_id"]
            and row["left_upper_trace_template_id"]
            == left["input_artificial_trace_template_id"]
            and row["right_lower_trace_template_id"]
            == right["input_artificial_trace_template_id"]
            and row["orientations_are_opposite"] is True
            and row["distinct_actual_children_and_input_tag_domains"] is True
            and row["unconditional_cancellation_claimed"] is False
            and row["both_traces_remain_typed"] is True
            and row["cross_tag_and_cross_lambda_cancellation_forbidden"]
            is True
            and "canonical-exact-lambda-key"
            in row["actual_incidence_id_constructor"],
            f"input incidence:{rank}:{stage}",
        )

    merged_by_endpoint = {
        row["endpoint_template_id"]: row
        for row in geometry["merged_rows"]
    }
    output_rows = result[
        "parameterized_stage3_output_trace_template_rows"
    ]
    output_map: dict[tuple[int, str], dict[str, Any]] = {
        (row["fragment_rank"], row["side"]): row for row in output_rows
    }
    require(len(output_map) == 432, "output trace key census")
    for fragment in geometry["fragment_rows"]:
        fragment_rank = fragment["fragment_rank"]
        rank = fragment["common_rank"]
        operator = operator_rows[(rank, 2)]
        source_incidence = incidence129[rank]
        for side, orientation in (("lower", -1), ("upper", 1)):
            row = output_map[(fragment_rank, side)]
            endpoint = fragment[f"source_x_{side}_endpoint_template_id"]
            cut = merged_by_endpoint.get(endpoint)
            new_stage3_cut = (
                cut is not None
                and cut["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
            )
            if new_stage3_cut:
                source_face = source_trace = None
                cut_evidence = cut["row_sha256"]
            else:
                source_face = source_incidence[f"{side}_face_template_id"]
                source_trace = source_incidence[f"{side}_trace_template_id"]
                cut_evidence = (
                    cut["row_sha256"]
                    if cut is not None
                    else face129[source_face]["row_sha256"]
                )
            velocity = row_id(
                "stage3-endpoint-velocity-template",
                [family_root_id, endpoint, cut_evidence],
            )
            density = row_id(
                "stage3-unnormalized-density-template",
                [
                    family_root_id,
                    rank,
                    operator["standard_family_operator_template_id"],
                    endpoint,
                ],
            )
            require(
                row["stage3_output_trace_template_id"]
                == row_id(
                    "stage3-output-trace-template",
                    [
                        family_root_id,
                        fragment["output_fragment_template_id"],
                        side,
                    ],
                )
                and row["family_root_id"] == family_root_id
                and row["output_fragment_template_id"]
                == fragment["output_fragment_template_id"]
                and row["common_rank"] == rank
                and row["orientation_sign"] == orientation
                and row["source_endpoint_template_id"] == endpoint
                and row["merged_cut_origin"]
                == (cut["origin"] if cut is not None else None)
                and row["Round129_source_face_template_id"] == source_face
                and row["Round129_source_trace_template_id"] == source_trace
                and row["standard_family_operator_template_id"]
                == operator["standard_family_operator_template_id"]
                and row["endpoint_velocity_witness_template_id"] == velocity
                and row["unnormalized_density_witness_template_id"]
                == density
                and row[
                    "conditional_normalization_is_undone_by_fragment_mass"
                ]
                is True
                and row["Jacobian_factor_is_present"] is True
                and row["source_family_member_tag_is_preserved"] is True
                and row["cross_family_member_tag_cancellation_allowed"]
                is False
                and row[
                    "same_exact_lambda_and_source_tag_required_for_witness_comparison"
                ]
                is True
                and all(
                    "canonical-exact-lambda-key" in row[key]
                    for key in (
                        "family_actual_trace_id_constructor",
                        "family_actual_velocity_witness_id_constructor",
                        "family_actual_density_witness_id_constructor",
                    )
                ),
                f"output trace:{fragment_rank}:{side}",
            )

    output_incidence_rows = sorted(
        result["parameterized_stage3_output_incidence_template_rows"],
        key=lambda row: row["cut_rank"],
    )
    cancelled = retained = 0
    for rank, row in enumerate(output_incidence_rows):
        left = output_map[(rank, "upper")]
        right = output_map[(rank + 1, "lower")]
        endpoint = left["source_endpoint_template_id"]
        require(
            endpoint == right["source_endpoint_template_id"],
            f"output shared cut:{rank}",
        )
        cut = merged_by_endpoint[endpoint]
        same_input = left["common_rank"] == right["common_rank"]
        new_stage3 = cut["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
        velocity_equal = (
            left["endpoint_velocity_witness_template_id"]
            == right["endpoint_velocity_witness_template_id"]
        )
        density_equal = (
            left["unnormalized_density_witness_template_id"]
            == right["unnormalized_density_witness_template_id"]
        )
        require(
            same_input == new_stage3
            and velocity_equal is True
            and density_equal == same_input,
            f"output cancellation witnesses:{rank}",
        )
        cancelled += int(same_input)
        retained += int(not same_input)
        require(
            row["stage3_output_incidence_template_id"]
            == row_id(
                "stage3-output-incidence-template",
                [family_root_id, rank, endpoint],
            )
            and row["family_root_id"] == family_root_id
            and row["endpoint_template_id"] == endpoint
            and row["cut_origin"] == cut["origin"]
            and row["left_upper_trace_template_id"]
            == left["stage3_output_trace_template_id"]
            and row["right_lower_trace_template_id"]
            == right["stage3_output_trace_template_id"]
            and row["same_input_common_rank"] == same_input
            and row["same_input_iff_new_stage3_cut"] is True
            and row["endpoint_velocity_witness_templates_equal"]
            == velocity_equal
            and row["unnormalized_density_witness_templates_equal"]
            == density_equal
            and row["cancelled_before_total_variation"] == same_input
            and row["retained_as_two_typed_traces_when_not_matched"]
            == (not same_input)
            and row[
                "cancellation_is_fibrewise_in_one_source_family_tag"
            ]
            is True
            and row[
                "equal_canonical_exact_lambda_key_and_source_tag_required"
            ]
            is True
            and row["cross_lambda_and_cross_tag_cancellation_forbidden"]
            is True,
            f"output incidence:{rank}",
        )
    require(
        (cancelled, retained) == (192, 23),
        "output cancellation split",
    )

    injection_rows = {
        row["stage"]: row
        for row in result[
            "parameterized_source_injection_contract_template_rows"
        ]
    }
    require(set(injection_rows) == {0, 1, 2}, "source injections")
    for stage, row in injection_rows.items():
        rank_bound = RAW_INCIDENCE_RANK[stage]
        bulk = 25 * (1 << rank_bound)
        total = bulk + 27
        require(
            row["source_injection_contract_template_id"]
            == row_id(
                "source-injection-contract-template",
                [family_root_id, stage],
            )
            and row["family_root_id"] == family_root_id
            and row["incidence_rank_B"] == rank_bound
            and row["bulk_generator_budget_per_M_rho_infinity"]
            == str(bulk)
            and row["two_artificial_trace_budget_per_M_rho_infinity"]
            == "27"
            and row["source_graph_current_injection_strict_upper"]
            == str(total)
            and row["source_injection_formula"]
            == f"25*2^{rank_bound}+27={total}"
            and row[
                "all_actual_legs_require_same_canonical_exact_lambda_key"
            ]
            is True,
            f"source injection:{stage}",
        )

    boundary_rows = {
        (row["common_rank"], row["stage"]): row
        for row in round129["uniform_physical_face_empty_audit"][
            "family_child_stage_boundary_rows"
        ]
    }
    graph_rows = {
        (row["common_rank"], row["stage"]): row
        for row in result["parameterized_graph_current_leg_template_rows"]
    }
    require(len(boundary_rows) == len(graph_rows) == 72, "graph leg census")
    independent_max = {0: Q(0), 1: Q(0), 2: Q(0)}
    independent_min_cosine: dict[int, Q | None] = {
        0: None, 1: None, 2: None
    }
    for rank in range(24):
        common = geometry["common_rows"][rank]
        x_lower = geometry["face_guard"][common["lower_face_template_id"]][0]
        x_upper = geometry["face_guard"][common["upper_face_template_id"]][1]
        state = v122.source_and_collisions(
            geometry["theta_guard"],
            v122.Jet2(interval(x_lower, x_upper), x=arb(1)),
            v122.Jet2(interval(-S_EPSILON, S_EPSILON), s=arb(1)),
        )
        for stage in range(3):
            row = graph_rows[(rank, stage)]
            operator = operator_rows[(rank, stage)]
            boundary = boundary_rows[(rank, stage)]
            nx, ny, momentum, cosine = state["collisions"][stage + 1]
            eta = Q(RELATIVE_CENTER_ETA[stage])
            radius = TARGET_RADII[stage]
            x_r = aq(eta) * (
                ny - (momentum / cosine) * nx
            )
            x_p = aq(eta / radius) * (
                cosine * ny - momentum * nx
            )
            if stage == 2:
                require(
                    arb_pair(x_r.value) == (Q(0), Q(0))
                    and arb_pair(x_p.value) == (Q(0), Q(0)),
                    "stage2 exact zero generator",
                )
                x_r_upper = x_p_upper = Q(0)
            else:
                x_r_upper = guarded_abs_upper(x_r.value)
                x_p_upper = guarded_abs_upper(x_p.value)
            l1_upper = x_r_upper + x_p_upper
            diagnostic = (Q(8), Q(2), Q(0))[stage]
            require(
                l1_upper < diagnostic if stage < 2 else l1_upper == 0,
                f"independent generator diagnostic:{rank}:{stage}",
            )
            independent_max[stage] = max(
                independent_max[stage], l1_upper
            )
            cosine_lower = arb_pair(cosine.value)[0] - ENCLOSURE_GUARD
            require(cosine_lower > 0, "independent positive target cosine")
            independent_min_cosine[stage] = (
                cosine_lower
                if independent_min_cosine[stage] is None
                else min(independent_min_cosine[stage], cosine_lower)
            )
            require(
                Q(1) / cosine_lower
                <= 1 << RAW_INCIDENCE_RANK[stage],
                f"independent incidence rank:{rank}:{stage}",
            )
            bases = sorted(
                geometry["bases_by_rank_stage"][(rank, stage)],
                key=lambda item: item["roof_level_j"],
            )
            f11 = [fields[(base["base_key_template_id"], 11)] for base in bases]
            f13 = [fields[(base["base_key_template_id"], 13)] for base in bases]
            f15 = [f15_rows[base["base_key_template_id"]] for base in bases]
            require(
                all(
                    Q(item["field_value_or_contract"])
                    == F17_BY_STAGE[stage]
                    for item in f11
                )
                and all(item["field_value_or_contract"] == "0" for item in f13),
                f"F11/F13 graph crosswalk:{rank}:{stage}",
            )
            injection = injection_rows[stage]
            require(
                row["graph_current_leg_template_id"]
                == row_id(
                    "graph-current-leg-template",
                    [family_root_id, rank, stage],
                )
                and row["family_root_id"] == family_root_id
                and row["official_word_key_id"]
                == operator["official_word_key_id"]
                and row["roof_level_js"] == operator["roof_level_js"]
                and row["materialized_input_recut_template_id"]
                == operator["materialized_input_recut_template_id"]
                and row["standard_family_operator_template_id"]
                == operator["standard_family_operator_template_id"]
                and row["source_collision_owner"] == boundary["source_owner"]
                and row["source_collision_chart"] == boundary["source_chart"]
                and row["target_collision_owner"]
                == boundary["actual_next_owner"]
                and row["target_collision_chart"] == STAGE_CHART[stage]
                and row["source_recipient_component_key"]
                == SOURCE_COMPONENT[stage]
                and row["target_recipient_component_key"]
                == TARGET_COMPONENT[stage]
                and Q(row["target_radius"]) == radius
                and row["relative_center_velocity_eta"] == int(eta)
                and row["uniform_over_lambda_times_Round122_s_collar"]
                is True
                and row["raw_incidence_rank_B"]
                == RAW_INCIDENCE_RANK[stage]
                and row["incidence_rank_paid_directly_by_cosine_guard"]
                is True
                and Q(row["actual_abs_X_r_upper"]) >= x_r_upper
                and Q(row["actual_abs_X_p_upper"]) >= x_p_upper
                and Q(row["actual_l1_generator_upper"]) >= l1_upper
                and Q(row[
                    "actual_l1_generator_diagnostic_strict_upper"
                ])
                == diagnostic
                and row["actual_same_colour_generator_is_zero"]
                == (stage == 2)
                and row["input_artificial_trace_template_ids"]
                == [
                    input_map[(rank, stage, side)][
                        "input_artificial_trace_template_id"
                    ]
                    for side in ("lower", "upper")
                ]
                and row["same_key_F11_slot_template_ids"]
                == [item["field_slot_template_id"] for item in f11]
                and row["same_key_F13_slot_template_ids"]
                == [item["field_slot_template_id"] for item in f13]
                and row["same_key_F15_slot_template_ids"]
                == [item["field_slot_template_id"] for item in f15]
                and row["physical_trace_count"] == 0
                and row[
                    "physical_trace_zero_only_by_Round129_family_empty_audit"
                ]
                is True
                and row["artificial_traces_are_not_physical_F13_traces"]
                is True
                and row["source_injection_contract_template_id"]
                == injection["source_injection_contract_template_id"]
                and row["source_graph_current_injection_strict_upper"]
                == injection["source_graph_current_injection_strict_upper"]
                and row["dynamic_test_suffix_strict_upper"]
                == str(F17_BY_STAGE[stage])
                and row[
                    "canonical_exact_lambda_key_required_for_actual_graph_leg"
                ]
                is True,
                f"graph leg metadata:{rank}:{stage}",
            )
            for name, actual in (
                ("target_normal_x_enclosure", nx.value),
                ("target_normal_y_enclosure", ny.value),
                ("target_momentum_enclosure", momentum.value),
                ("target_cosine_enclosure", cosine.value),
                ("X_r_enclosure", x_r.value),
                ("X_p_enclosure", x_p.value),
            ):
                interval_contains(
                    row[name],
                    actual,
                    f"graph interval:{rank}:{stage}:{name}",
                )
            stored_cosine_lower = Q(
                row["guarded_target_cosine_strict_lower"]
            )
            require(
                0 < stored_cosine_lower <= cosine_lower
                and Q(row["guarded_reciprocal_cosine_upper"])
                == Q(1) / stored_cosine_lower,
                f"graph cosine arithmetic:{rank}:{stage}",
            )

    component_rows = {
        row["component_key"]: row
        for row in result[
            "parameterized_recipient_component_template_rows"
        ]
    }
    require(set(component_rows) == {row[0] for row in RECIPIENT_COMPONENTS},
            "recipient component keys")
    for component_key, owner, chart in RECIPIENT_COMPONENTS:
        row = component_rows[component_key]
        require(
            row["recipient_component_template_id"]
            == row_id(
                "recipient-component-template",
                [family_root_id, component_key],
            )
            and row["family_root_id"] == family_root_id
            and row["collision_owner"] == owner
            and row["collision_chart"] == chart
            and row["dual_recipient"]
            == "vector-current plus typed boundary traces"
            and row[
                "canonical_exact_lambda_key_required_for_actual_component"
            ]
            is True,
            f"recipient component:{component_key}",
        )

    pullback_rows = {
        (row["common_rank"], row["stage"]): row
        for row in result[
            "parameterized_recipient_pullback_map_template_rows"
        ]
    }
    require(len(pullback_rows) == 72, "recipient pullback census")
    for rank in range(24):
        for stage in range(3):
            row = pullback_rows[(rank, stage)]
            graph = graph_rows[(rank, stage)]
            operator = operator_rows[(rank, stage)]
            source = component_rows[SOURCE_COMPONENT[stage]]
            target = component_rows[TARGET_COMPONENT[stage]]
            require(
                row["recipient_pullback_map_template_id"]
                == row_id(
                    "recipient-pullback-map-template",
                    [family_root_id, rank, stage],
                )
                and row["family_root_id"] == family_root_id
                and row["official_word_key_id"]
                == operator["official_word_key_id"]
                and row["roof_level_js"] == operator["roof_level_js"]
                and row["source_recipient_component_template_id"]
                == source["recipient_component_template_id"]
                and row["target_recipient_component_template_id"]
                == target["recipient_component_template_id"]
                and row["physical_branch_map"]
                == f"{source['component_key']}->{target['component_key']}"
                and row["materialized_input_recut_template_id"]
                == operator["materialized_input_recut_template_id"]
                and row["standard_family_operator_template_id"]
                == operator["standard_family_operator_template_id"]
                and row["graph_current_leg_template_id"]
                == graph["graph_current_leg_template_id"]
                and row[
                    "full_phase_C1_dynamic_Holder_pullback_strict_upper"
                ]
                == str(F17_BY_STAGE[stage])
                and row["area_coordinate_determinant"] == "1"
                and row["both_Eulerian_vector_components_are_received"]
                is True
                and row[
                    "physical_and_artificial_traces_are_separately_typed"
                ]
                is True
                and row["transparent_roof_levels_share_one_physical_map"]
                is True
                and row[
                    "canonical_exact_lambda_key_required_for_actual_map"
                ]
                is True,
                f"recipient pullback:{rank}:{stage}",
            )

    derivation_rows = {
        row["stage"]: row
        for row in result[
            "parameterized_source_injection_derivation_template_rows"
        ]
    }
    require(set(derivation_rows) == {0, 1, 2}, "injection derivations")
    for stage, row in derivation_rows.items():
        legs = [
            graph_rows[(rank, stage)] for rank in range(24)
        ]
        injection = injection_rows[stage]
        require(
            row["source_injection_derivation_template_id"]
            == row_id(
                "source-injection-derivation-template",
                [family_root_id, stage],
            )
            and row["family_root_id"] == family_root_id
            and row["leg_count_per_exact_lambda"] == 24
            and row["graph_current_leg_template_ids"]
            == [item["graph_current_leg_template_id"] for item in legs]
            and row["graph_current_leg_template_sha256s"]
            == [item["row_sha256"] for item in legs]
            and row["source_injection_contract_template_id"]
            == injection["source_injection_contract_template_id"]
            and row["incidence_rank_B"] == RAW_INCIDENCE_RANK[stage]
            and row["source_graph_current_injection_strict_upper"]
            == injection["source_graph_current_injection_strict_upper"]
            and row[
                "all_24_actual_legs_share_one_canonical_exact_lambda_key"
            ]
            is True,
            f"injection derivation:{stage}",
        )
        stored_max = max(
            Q(item["actual_l1_generator_upper"]) for item in legs
        )
        stored_min_cosine = min(
            Q(item["guarded_target_cosine_strict_lower"]) for item in legs
        )
        require(
            Q(row["maximum_actual_l1_generator_upper"]) == stored_max
            and Q(row["minimum_guarded_target_cosine_lower"])
            == stored_min_cosine,
            f"injection derivation extrema:{stage}",
        )

    f17_rows = {
        row["base_key_template_id"]: row
        for row in result["parameterized_F17_slot_template_rows"]
    }
    bases = {
        row["base_key_template_id"]: row for row in geometry["base_rows"]
    }
    require(set(f17_rows) == set(bases), "F17 base coverage")
    for key, base in bases.items():
        rank, stage = base["common_rank"], base["stage"]
        row = f17_rows[key]
        graph = graph_rows[(rank, stage)]
        pullback = pullback_rows[(rank, stage)]
        derivation = derivation_rows[stage]
        require(
            row["field_slot_template_id"]
            == row_id("field17-slot-template", [family_root_id, key])
            and row["family_root_id"] == family_root_id
            and base_metadata(row) == base_metadata(base)
            and row["field_index"] == 17
            and row["field_name"] == FIELD_NAMES[17]
            and row["field_value_or_contract"] == str(F17_BY_STAGE[stage])
            and row["field_bound_semantics"] == "STRICT_UPPER"
            and row["same_key_F11_slot_template_id"]
            == fields[(key, 11)]["field_slot_template_id"]
            and row["same_key_F15_slot_template_id"]
            == f15_rows[key]["field_slot_template_id"]
            and row["graph_current_leg_template_id"]
            == graph["graph_current_leg_template_id"]
            and row["graph_current_leg_template_sha256"]
            == graph["row_sha256"]
            and row["recipient_pullback_map_template_id"]
            == pullback["recipient_pullback_map_template_id"]
            and row["recipient_pullback_map_template_sha256"]
            == pullback["row_sha256"]
            and row["source_injection_contract_template_id"]
            == graph["source_injection_contract_template_id"]
            and row["source_injection_derivation_template_id"]
            == derivation["source_injection_derivation_template_id"]
            and row["both_Eulerian_vector_components_included"] is True
            and row["physical_trace_zero_crosswalk_included"] is True
            and row["artificial_trace_registry_retained"] is True
            and row["F17_is_not_a_rename_of_F11"] is True
            and row[
                "canonical_exact_lambda_key_required_for_actual_slot"
            ]
            is True
            and row["finite_row_is_a_template_not_an_actual_fibre_slot"]
            is True,
            f"F17 slot:{key}",
        )

    contract = result["per_fibre_F17_graph_current_contract"]
    stored_stage_max = {
        str(stage): qstr(max(
            Q(row["actual_l1_generator_upper"])
            for (rank, row_stage), row in graph_rows.items()
            if row_stage == stage
        ))
        for stage in range(3)
    }
    stored_stage_min_cosine = {
        str(stage): qstr(min(
            Q(row["guarded_target_cosine_strict_lower"])
            for (rank, row_stage), row in graph_rows.items()
            if row_stage == stage
        ))
        for stage in range(3)
    }
    require(
        contract["status"]
        == "CERTIFIED_OVER_LAMBDA_TIMES_ROUND122_S_COLLAR"
        and contract["maximum_actual_l1_generator_upper_by_stage"]
        == stored_stage_max
        and contract["minimum_guarded_target_cosine_lower_by_stage"]
        == stored_stage_min_cosine
        and contract["incidence_rank_B_by_stage"]
        == {"0": 15, "1": 14, "2": 14}
        and contract["dynamic_F17_strict_upper_by_stage"]
        == {"0": "4915200", "1": "2457600", "2": "2457600"}
        and contract["input_artificial_trace_count_per_exact_lambda"] == 144
        and contract[
            "input_inter_child_incidence_count_per_exact_lambda"
        ]
        == 69
        and contract["stage3_output_trace_count_per_exact_lambda"] == 432
        and contract["stage3_output_incidence_count_per_exact_lambda"] == 215
        and contract[
            "stage3_same_input_cancelled_incidence_count_per_exact_lambda"
        ]
        == 192
        and contract[
            "stage3_inter_child_retained_incidence_count_per_exact_lambda"
        ]
        == 23
        and contract[
            "cancellation_requires_same_exact_lambda_and_source_tag"
        ]
        is True
        and contract["cross_lambda_or_cross_tag_cancellation_forbidden"]
        is True
        and contract[
            "Piola_intertwining_is_fibrewise_on_the_actual_branch_map"
        ]
        is True,
        "F17 family contract",
    )
    return {
        "input_rows": input_map,
        "input_incidence_rows": input_incidence_rows,
        "output_rows": output_map,
        "output_incidence_rows": output_incidence_rows,
        "injection_rows": injection_rows,
        "graph_rows": graph_rows,
        "component_rows": component_rows,
        "pullback_rows": pullback_rows,
        "derivation_rows": derivation_rows,
        "f17_rows": f17_rows,
        "independent_max_l1": {
            str(stage): qstr(value)
            for stage, value in independent_max.items()
        },
        "independent_min_cosine": {
            str(stage): qstr(value)  # type: ignore[arg-type]
            for stage, value in independent_min_cosine.items()
        },
        "cancelled": cancelled,
        "retained": retained,
    }


def actual_slot_crosswalk_test(
    round129: dict[str, Any],
    geometry: dict[str, Any],
    lambda_vectors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    family_root_id = geometry["family_root_id"]
    angular_lift_id = round129["positive_Borel_family_root_contract"][
        "angular_lift_id"
    ]
    operator_cell_id = round129["positive_Borel_family_root_contract"][
        "round117_operator_cell_id"
    ]
    source_fields = source_field_map(round129)
    result: list[dict[str, Any]] = []
    all_vector_slots: set[str] = set()
    for vector in lambda_vectors:
        lambda_key = vector["test_key"]
        derived_b_key = "round130-derived-exact-b-key-test:" + digest([
            "round130-derived-exact-b-key-v1",
            family_root_id,
            lambda_key,
            "Round129-strictly-increasing-analytic-b-of-lambda",
        ])
        typed_parent = "round129-parent-W-test:" + digest([
            family_root_id,
            angular_lift_id,
            derived_b_key,
        ])
        slot_ids: set[str] = set()
        block_digests: list[str] = []
        for base in geometry["base_rows"]:
            rank = base["common_rank"]
            refined = "round129-refined-subbranch-test:" + digest([
                typed_parent,
                operator_cell_id,
                "source-k=0",
                rank,
            ])
            actual_base = [
                base["official_word_key_id"],
                refined,
                base["roof_level_j"],
            ]
            fields_for_block: list[str] = []
            for field in range(1, 19):
                if field in set(range(1, 14)) | {16}:
                    source = source_fields[
                        (base["base_key_template_id"], field)
                    ]
                    require(
                        source[
                            "exact_lambda_locator_and_derived_exact_b_locator_required"
                        ]
                        is True
                        and "refined-subbranch-id(exact-b-locator)"
                        in source["parameterized_actual_slot_id_constructor"],
                        f"upstream actual slot constructor:F{field}",
                    )
                    actual_id = "round129-slot-test:" + digest([
                        *actual_base,
                        FIELD_NAMES[field],
                    ])
                else:
                    actual_id = "round130-slot-test:" + digest([
                        *actual_base,
                        FIELD_NAMES[field],
                        lambda_key,
                    ])
                require(actual_id not in slot_ids, "per-fibre actual slot unique")
                slot_ids.add(actual_id)
                fields_for_block.append(actual_id)
            require(len(fields_for_block) == 18, "actual block 18 fields")
            block_digests.append(digest([
                base["base_key_template_id"],
                actual_base,
                fields_for_block,
                lambda_key,
            ]))
        require(len(slot_ids) == 2160, "test fibre actual slot census")
        require(
            not (slot_ids & all_vector_slots),
            "canonical test fibres have disjoint actual slot IDs",
        )
        all_vector_slots.update(slot_ids)
        result.append({
            "normalized_u": vector["normalized_u"],
            "canonical_lambda_test_key": lambda_key,
            "derived_b_key": derived_b_key,
            "independently_supplied_b_key_used": False,
            "actual_base_key_count": 120,
            "actual_field_slot_count": len(slot_ids),
            "actual_complete_18_field_level_block_count":
                len(block_digests),
            "actual_slot_ids_sha256": digest(sorted(slot_ids)),
            "actual_level_blocks_sha256": digest(block_digests),
        })
    require(len(all_vector_slots) == 6480, "three-fibre slot disjointness")
    return result


def validate_f18_and_safety(
    result: dict[str, Any],
    round129: dict[str, Any],
    geometry: dict[str, Any],
    f14_f15: dict[str, Any],
    f17: dict[str, Any],
    lambda_vectors: list[dict[str, Any]],
) -> dict[str, Any]:
    family_root_id = geometry["family_root_id"]
    bases = {
        row["base_key_template_id"]: row for row in geometry["base_rows"]
    }
    source_fields = f14_f15["fields"]
    new_fields = {
        14: f14_f15["f14_rows"],
        15: f14_f15["f15_rows"],
        17: f17["f17_rows"],
    }
    operators = f14_f15["operator_rows"]
    same_key_rows = {
        row["base_key_template_id"]: row
        for row in result[
            "parameterized_F1_F17_same_key_map_template_rows"
        ]
    }
    f18_rows = {
        row["base_key_template_id"]: row
        for row in result["parameterized_F18_slot_template_rows"]
    }
    block_rows = {
        row["base_key_template_id"]: row
        for row in result[
            "parameterized_local_18_field_level_block_template_rows"
        ]
    }
    require(
        set(same_key_rows) == set(f18_rows) == set(block_rows) == set(bases),
        "F18 base coverage",
    )
    block_by_id: dict[str, dict[str, Any]] = {}
    for key, base in bases.items():
        rank, stage, roof = (
            base["common_rank"],
            base["stage"],
            base["roof_level_j"],
        )
        operator = operators[(rank, stage)]
        bindings: list[dict[str, Any]] = []
        for field in range(1, 18):
            source = (
                new_fields[field][key]
                if field in new_fields
                else source_fields[(key, field)]
            )
            require(
                source["field_index"] == field
                and source["field_name"] == FIELD_NAMES[field],
                f"F18 source field:{key}:F{field}",
            )
            bindings.append({
                "field_index": field,
                "field_name": FIELD_NAMES[field],
                "field_slot_template_id":
                    source["field_slot_template_id"],
                "field_slot_template_row_sha256": source["row_sha256"],
            })
        same_key = same_key_rows[key]
        map_id = row_id(
            "same-key-F1-F17-map-template",
            [family_root_id, key],
        )
        require(
            same_key["same_key_map_template_id"] == map_id
            and same_key["family_root_id"] == family_root_id
            and same_key["common_rank"] == rank
            and same_key["common_rank_template_id"]
            == geometry["common_rows"][rank]["common_rank_template_id"]
            and same_key["stage"] == stage
            and same_key["official_word_key_id"]
            == base["official_word_key_id"]
            and same_key["roof_level_j"] == roof
            and same_key["materialized_input_recut_template_id"]
            == base["materialized_input_recut_template_id"]
            and same_key["standard_family_operator_template_id"]
            == operator["standard_family_operator_template_id"]
            and same_key["standard_family_operator_template_sha256"]
            == operator["row_sha256"]
            and same_key["bound_preexisting_field_indices"]
            == list(range(1, 18))
            and same_key["bound_preexisting_field_count"] == 17
            and same_key["bound_preexisting_field_slot_templates"]
            == bindings
            and same_key[
                "bound_preexisting_field_slot_templates_sha256"
            ]
            == digest(bindings)
            and same_key["each_preexisting_field_bound_exactly_once"] is True
            and same_key[
                "all_fields_share_family_root_common_rank_stage_recut_and_operator"
            ]
            is True
            and same_key[
                "canonical_exact_lambda_key_required_for_actual_map"
            ]
            is True,
            f"same-key map:{key}",
        )

        return_length = STAGE_RETURN_LENGTH[stage]
        suffix = return_length - roof
        require(0 <= roof < return_length and suffix > 0, "phase exponents")
        f18 = f18_rows[key]
        f18_id = row_id("field18-slot-template", [family_root_id, key])
        require(
            f18["field_slot_template_id"] == f18_id
            and f18["family_root_id"] == family_root_id
            and base_metadata(f18) == base_metadata(base)
            and f18["field_index"] == 18
            and f18["field_name"] == FIELD_NAMES[18]
            and f18["field_value_or_contract"]
            == "DIRECT_STANDARD_N_STRUCTURAL_PHASE_REGISTRATION"
            and f18["field_bound_semantics"] == "EXACT_STRUCTURAL_IDENTITY"
            and f18["standard_family_operator_template_id"]
            == operator["standard_family_operator_template_id"]
            and f18["same_key_F1_F17_map_template_id"] == map_id
            and f18["same_key_F1_F17_map_template_sha256"]
            == same_key["row_sha256"]
            and f18["bound_preexisting_field_count"] == 17
            and f18["phase_route"] == "direct_standard_N"
            and f18["stage_return_length_r"] == return_length
            and f18["prefix_length_j"] == roof
            and f18["suffix_length_r_minus_j"] == suffix
            and f18["prefix_operator_monomial"] == f"z^{roof}"
            and f18["suffix_operator_monomial"] == f"z^{suffix}"
            and f18["stage_block_operator_monomial"]
            == f"z^{return_length}"
            and f18["prefix_suffix_block_identity"]
            == f"z^{roof}*z^{suffix}=z^{return_length}"
            and f18["child_stage_block_exponents"] == [2, 1, 2]
            and f18["child_path_exponent"] == 5
            and f18["child_path_operator_monomial"] == "z^5"
            and f18[
                "child_path_uses_one_block_per_stage_not_one_per_roof_split"
            ]
            is True
            and f18["structural_registration_only"] is True
            and f18["operator_Wiener_invertibility_claimed"] is False
            and f18["operator_Wiener_aperiodicity_claimed"] is False
            and f18["Kac_closure_claimed"] is False
            and f18["global_operator_phase_block_claimed"] is False
            and f18["CM2_claimed"] is False
            and f18[
                "canonical_exact_lambda_key_required_for_actual_slot"
            ]
            is True
            and f18["finite_row_is_a_template_not_an_actual_fibre_slot"]
            is True,
            f"F18 slot:{key}",
        )
        all_slots = [
            *bindings,
            {
                "field_index": 18,
                "field_name": FIELD_NAMES[18],
                "field_slot_template_id": f18_id,
                "field_slot_template_row_sha256": f18["row_sha256"],
            },
        ]
        block = block_rows[key]
        require(
            block["level_block_template_id"]
            == row_id(
                "local-18-field-level-block-template",
                [family_root_id, key],
            )
            and block["family_root_id"] == family_root_id
            and block["common_rank"] == rank
            and block["stage"] == stage
            and block["official_word_key_id"]
            == base["official_word_key_id"]
            and block["roof_level_j"] == roof
            and block["materialized_input_recut_template_id"]
            == base["materialized_input_recut_template_id"]
            and block["standard_family_operator_template_id"]
            == operator["standard_family_operator_template_id"]
            and block["field_slot_templates"] == all_slots
            and block["field_slot_templates_sha256"] == digest(all_slots)
            and block["field_indices"] == list(range(1, 19))
            and block["field_count"] == 18
            and block["each_field_bound_exactly_once"] is True
            and block["fibre_local_complete_18_field_level_block"] is True
            and block["global_complete_18_field_block"] is False
            and block[
                "canonical_exact_lambda_key_required_for_actual_level_block"
            ]
            is True
            and block["finite_row_is_a_template_not_an_actual_fibre_block"]
            is True,
            f"level block:{key}",
        )
        block_by_id[block["level_block_template_id"]] = block
    require(
        Counter(row["stage"] for row in f18_rows.values())
        == Counter({0: 48, 1: 24, 2: 48}),
        "F18 stage census",
    )

    packet_rows = sorted(
        result[
            "parameterized_local_18_field_child_packet_template_rows"
        ],
        key=lambda row: row["common_rank"],
    )
    seen_blocks: list[str] = []
    for rank, packet in enumerate(packet_rows):
        blocks = [
            block_by_id[identifier]
            for identifier in packet["level_block_template_ids"]
        ]
        require(
            [row["stage"] for row in blocks] == [0, 0, 1, 2, 2]
            and [row["roof_level_j"] for row in blocks] == [0, 1, 0, 0, 1],
            f"packet block ordering:{rank}",
        )
        common = geometry["common_rows"][rank]
        require(
            packet["child_packet_template_id"]
            == row_id(
                "local-18-field-child-packet-template",
                [family_root_id, rank],
            )
            and packet["family_root_id"] == family_root_id
            and packet["common_rank"] == rank
            and packet["common_rank_template_id"]
            == common["common_rank_template_id"]
            and packet["official_path_id"] == common["official_path_id"]
            and packet["level_block_template_sha256s"]
            == [row["row_sha256"] for row in blocks]
            and packet["level_block_count"] == 5
            and packet["stage_block_exponents"] == [2, 1, 2]
            and packet["child_path_operator_monomial"] == "z^5"
            and packet[
                "all_five_level_blocks_share_one_actual_common_child_and_exact_lambda"
            ]
            is True
            and packet["fibre_local_complete_18_field_child_packet"] is True
            and packet["global_complete_18_field_block"] is False
            and packet[
                "canonical_exact_lambda_key_required_for_actual_packet"
            ]
            is True
            and packet[
                "finite_row_is_a_template_not_an_actual_fibre_packet"
            ]
            is True,
            f"child packet:{rank}",
        )
        seen_blocks.extend(packet["level_block_template_ids"])
    require(
        len(seen_blocks) == len(set(seen_blocks)) == 120,
        "packets partition level blocks",
    )

    phase = result["per_fibre_F18_phase_contract"]
    require(
        phase
        == {
            "status": "STRUCTURAL_F18_ON_EVERY_EXACT_LAMBDA_FIBRE",
            "phase_route": "direct_standard_N",
            "stage_block_rule": "z^j*z^(r-j)=z^r",
            "child_stage_block_exponents": [2, 1, 2],
            "child_path_rule": "z^2*z^1*z^2=z^5",
            "roof_levels_are_symbolic_factorizations_not_extra_collisions":
                True,
            "operator_Wiener_theorem": "NOT_CLAIMED",
            "operator_Wiener_aperiodicity": "NOT_CLAIMED",
            "Kac_return_wide_closure": "NOT_CLAIMED",
            "global_operator_phase_registration": "NOT_CLAIMED",
        },
        "F18 phase scope",
    )

    for group in ROW_GROUPS:
        for row in result[group]:
            for key, value in row.items():
                if "constructor" in key and type(value) is str:
                    require(
                        "canonical-exact-lambda-key" in value,
                        f"actual constructor canonical token:{group}:{key}",
                    )

    registry = result["combined_template_registry"]
    new_field_rows = [
        *result["parameterized_F14_slot_template_rows"],
        *result["parameterized_F15_slot_template_rows"],
        *result["parameterized_F17_slot_template_rows"],
        *result["parameterized_F18_slot_template_rows"],
    ]
    require(
        registry
        == {
            "Round129_F1_F13_F16_slot_template_count": 1680,
            "Round130_new_F14_F15_F17_F18_slot_template_count": 480,
            "combined_field_slot_template_count": 2160,
            "new_field_slot_template_ids_sha256": digest([
                row["field_slot_template_id"] for row in new_field_rows
            ]),
            "same_key_map_template_count": 120,
            "local_18_field_level_block_template_count": 120,
            "local_18_field_child_packet_template_count": 24,
            "each_same_key_map_binds_F1_F17_exactly_once": True,
            "each_level_block_binds_F1_F18_exactly_once": True,
            "each_child_packet_binds_five_level_blocks_exactly_once": True,
        },
        "combined template registry",
    )

    expected_ledger = {
        "exact_lambda_fibre_count": "UNCOUNTABLE_PARAMETERIZED_REGISTRY",
        **{
            {
                "uniform_stage3_endpoint_guard_template_rows":
                    "finite_stage3_endpoint_guard_template_count",
                "parameterized_stage3_natural_cell_template_rows":
                    "finite_stage3_natural_cell_template_count",
                "parameterized_merged_cut_template_rows":
                    "finite_merged_cut_template_count",
                "parameterized_stage3_output_fragment_template_rows":
                    "finite_stage3_output_fragment_template_count",
                "parameterized_child_output_partition_template_rows":
                    "finite_child_output_partition_template_count",
                "parameterized_accepted_norm_leg_template_rows":
                    "finite_accepted_norm_leg_template_count",
                "parameterized_F14_slot_template_rows":
                    "finite_F14_slot_template_count",
                "parameterized_relative_zero_cemetery_template_rows":
                    "finite_relative_zero_cemetery_template_count",
                "parameterized_standard_family_operator_template_rows":
                    "finite_standard_family_operator_template_count",
                "parameterized_F15_slot_template_rows":
                    "finite_F15_slot_template_count",
                "parameterized_input_artificial_trace_template_rows":
                    "finite_input_artificial_trace_template_count",
                "parameterized_input_trace_incidence_template_rows":
                    "finite_input_trace_incidence_template_count",
                "parameterized_stage3_output_trace_template_rows":
                    "finite_stage3_output_trace_template_count",
                "parameterized_stage3_output_incidence_template_rows":
                    "finite_stage3_output_incidence_template_count",
                "parameterized_source_injection_contract_template_rows":
                    "finite_source_injection_contract_template_count",
                "parameterized_graph_current_leg_template_rows":
                    "finite_graph_current_leg_template_count",
                "parameterized_recipient_component_template_rows":
                    "finite_recipient_component_template_count",
                "parameterized_recipient_pullback_map_template_rows":
                    "finite_recipient_pullback_map_template_count",
                "parameterized_source_injection_derivation_template_rows":
                    "finite_source_injection_derivation_template_count",
                "parameterized_F17_slot_template_rows":
                    "finite_F17_slot_template_count",
                "parameterized_F1_F17_same_key_map_template_rows":
                    "finite_F1_F17_same_key_map_template_count",
                "parameterized_F18_slot_template_rows":
                    "finite_F18_slot_template_count",
                "parameterized_local_18_field_level_block_template_rows":
                    "finite_level_block_template_count",
                "parameterized_local_18_field_child_packet_template_rows":
                    "finite_child_packet_template_count",
            }[group]: count
            for group, count in ROW_GROUPS.items()
        },
        "finite_Round130_template_row_count": 2814,
        "per_exact_lambda_fibre_actual_child_count": 24,
        "per_exact_lambda_fibre_actual_base_key_count": 120,
        "per_exact_lambda_fibre_actual_field_slot_count": 2160,
        "per_exact_lambda_fibre_actual_complete_18_field_level_block_count":
            120,
        "per_exact_lambda_fibre_actual_complete_18_field_child_packet_count":
            24,
        "whole_family_actual_child_row_count": None,
        "whole_family_actual_slot_row_count": None,
        "whole_family_actual_block_row_count": None,
        "global_complete_18_field_block_count": 0,
    }
    require(result["count_ledger"] == expected_ledger, "count ledger")
    require(
        result["positive_Borel_family_every_exact_fibre_local_field_maturity"]
        == "18/18"
        and result[
            "per_exact_lambda_fibre_local_complete_18_field_level_block_count"
        ]
        == 120
        and result[
            "per_exact_lambda_fibre_local_complete_18_field_child_packet_count"
        ]
        == 24
        and result["global_complete_18_field_block_count"] == 0
        and result["complete_18_field_block_count"] == 0
        and result["gate5_block_count"] == 0
        and result["gate5_global_maturity"] == "10/18"
        and result["gate5_status"] == "NOT_CERTIFIED"
        and result["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "local versus global safety",
    )
    require(
        round129["gate5_global_maturity"] == "10/18"
        and round129["global_complete_18_field_block_count"] == 0
        and round129["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round129 safety inheritance",
    )
    expected_nonclaims = [
        "finite template rows are not actual rows for the whole uncountable family",
        "per-fibre local 18/18 is not global Gate5 18/18",
        "no coverage of the remaining global return-word universe",
        "restricted relative cemetery zero is not ambient or all-time cemetery",
        "no global raw-Z, power-Orlicz, cemetery or owner-drift theorem",
        "no cross-lambda or cross-family-tag trace cancellation",
        "direct-standard-N F18 is structural phase bookkeeping only",
        "no operator Wiener invertibility or aperiodicity theorem",
        "no Kac return-wide closure theorem",
        "no global complete 18-field block and no CM2 claim",
    ]
    require(result["strict_nonclaims"] == expected_nonclaims, "strict nonclaims")
    require(
        result["strict_scope"]
        == "one Round129 positive-Borel lambda collar, one Round113 parent, "
           "one Round117 operator cell, three official words, 24 common "
           "ranks and 120 word/rank/roof keys per exact lambda fibre",
        "strict scope",
    )
    actual_crosswalk = actual_slot_crosswalk_test(
        round129, geometry, lambda_vectors
    )
    return {
        "same_key_map_count": len(same_key_rows),
        "F18_slot_count": len(f18_rows),
        "level_block_count": len(block_rows),
        "child_packet_count": len(packet_rows),
        "actual_slot_crosswalk_test_vectors": actual_crosswalk,
        "global_maturity": result["gate5_global_maturity"],
        "global_complete_blocks":
            result["global_complete_18_field_block_count"],
        "cm2": result["cm2_verdict"],
    }


GEOMETRY_GROUPS = (
    "uniform_stage3_endpoint_guard_template_rows",
    "parameterized_stage3_natural_cell_template_rows",
    "parameterized_merged_cut_template_rows",
    "parameterized_stage3_output_fragment_template_rows",
    "parameterized_child_output_partition_template_rows",
    "parameterized_accepted_norm_leg_template_rows",
)
F17_CARRIER_GROUPS = (
    "parameterized_input_artificial_trace_template_rows",
    "parameterized_input_trace_incidence_template_rows",
    "parameterized_stage3_output_trace_template_rows",
    "parameterized_stage3_output_incidence_template_rows",
    "parameterized_source_injection_contract_template_rows",
    "parameterized_graph_current_leg_template_rows",
    "parameterized_recipient_component_template_rows",
    "parameterized_recipient_pullback_map_template_rows",
    "parameterized_source_injection_derivation_template_rows",
    "parameterized_F17_slot_template_rows",
)


def validate_document(
    document: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
    round129: dict[str, Any],
    round129_verification: dict[str, Any],
    *,
    cache: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(type(document) is dict, "certificate top object")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate closed envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(type(document["result"]) is dict, "certificate result object")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    result = document["result"]
    require(result["precision_bits"] == 4096, "certificate precision")
    require(
        result["status"]
        == "CERTIFIED_POSITIVE_BOREL_EVERY_EXACT_FIBRE_LOCAL_18_OF_18"
           "__NO_GLOBAL_PROMOTION",
        "certificate status",
    )
    validate_closed_registries(result)
    validate_frozen_inputs(result, round129, round129_verification)
    lambda_vectors = validate_exact_lambda_contract(
        result,
        cached_vectors=(
            None if cache is None else cache["lambda_vectors"]
        ),
    )

    if cache is None:
        geometry = validate_stage3_geometry(
            result, round129, documents, core
        )
    else:
        official_result = cache["official_result"]
        require(
            result["positive_Borel_family_root_contract"]
            == official_result["positive_Borel_family_root_contract"],
            "cached family root freeze",
        )
        require(
            result["family_stage3_geometry_contract"]
            == official_result["family_stage3_geometry_contract"],
            "cached independent geometry contract freeze",
        )
        for group in GEOMETRY_GROUPS:
            require(
                result[group] == official_result[group],
                f"cached independent geometry registry freeze:{group}",
            )
        geometry = cache["geometry"]

    f14_f15 = validate_f14_f15(result, round129, geometry)
    if cache is None:
        f17 = validate_f17(result, round129, geometry, f14_f15)
    else:
        official_result = cache["official_result"]
        require(
            result["per_fibre_F17_graph_current_contract"]
            == official_result["per_fibre_F17_graph_current_contract"],
            "cached independent F17 contract freeze",
        )
        for group in F17_CARRIER_GROUPS:
            require(
                result[group] == official_result[group],
                f"cached independent F17 registry freeze:{group}",
            )
        f17 = cache["f17"]
    f18 = validate_f18_and_safety(
        result,
        round129,
        geometry,
        f14_f15,
        f17,
        lambda_vectors,
    )
    summary = {
        "positive_Borel_family_root_id": geometry["family_root_id"],
        "canonical_lambda_test_vector_count": len(lambda_vectors),
        "stage3_endpoint_guard_count": 192,
        "stage3_output_fragment_count": 216,
        "F14_slot_count": len(f14_f15["f14_rows"]),
        "F15_slot_count": len(f14_f15["f15_rows"]),
        "F17_slot_count": len(f17["f17_rows"]),
        "F18_slot_count": f18["F18_slot_count"],
        "same_key_map_count": f18["same_key_map_count"],
        "local_level_block_count_per_exact_lambda":
            f18["level_block_count"],
        "local_child_packet_count_per_exact_lambda":
            f18["child_packet_count"],
        "local_maturity": "18/18",
        "global_maturity": f18["global_maturity"],
        "global_complete_blocks": f18["global_complete_blocks"],
        "cm2": f18["cm2"],
    }
    validation_cache = {
        "official_result": result,
        "lambda_vectors": lambda_vectors,
        "geometry": geometry,
        "f17": f17,
        "actual_slot_crosswalk_test_vectors":
            f18["actual_slot_crosswalk_test_vectors"],
    }
    return summary, validation_cache


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def close_rows(result: dict[str, Any], group: str) -> None:
    rows = result[group]
    for row in rows:
        row["row_sha256"] = digest({
            key: value for key, value in row.items() if key != "row_sha256"
        })
    result[f"{group}_sha256"] = digest(rows)


def resign_document(document: dict[str, Any]) -> None:
    result = document["result"]
    for group in GEOMETRY_GROUPS:
        close_rows(result, group)
    leg_hash = {
        row["accepted_norm_leg_template_id"]: row["row_sha256"]
        for row in result["parameterized_accepted_norm_leg_template_rows"]
    }
    for row in result["parameterized_F14_slot_template_rows"]:
        row["accepted_norm_leg_template_sha256"] = leg_hash[
            row["accepted_norm_leg_template_id"]
        ]
    close_rows(result, "parameterized_F14_slot_template_rows")
    close_rows(
        result, "parameterized_relative_zero_cemetery_template_rows"
    )
    for row in result["parameterized_standard_family_operator_template_rows"]:
        row["output_member_tag_templates_sha256"] = digest(
            row["output_member_tag_templates"]
        )
    close_rows(result, "parameterized_standard_family_operator_template_rows")
    operator_hash = {
        row["standard_family_operator_template_id"]: row["row_sha256"]
        for row in result[
            "parameterized_standard_family_operator_template_rows"
        ]
    }
    for row in result["parameterized_F15_slot_template_rows"]:
        row["standard_family_operator_template_sha256"] = operator_hash[
            row["standard_family_operator_template_id"]
        ]
    close_rows(result, "parameterized_F15_slot_template_rows")

    for group in (
        "parameterized_input_artificial_trace_template_rows",
        "parameterized_input_trace_incidence_template_rows",
        "parameterized_stage3_output_trace_template_rows",
        "parameterized_stage3_output_incidence_template_rows",
        "parameterized_source_injection_contract_template_rows",
        "parameterized_graph_current_leg_template_rows",
        "parameterized_recipient_component_template_rows",
        "parameterized_recipient_pullback_map_template_rows",
    ):
        close_rows(result, group)
    graph_hash = {
        row["graph_current_leg_template_id"]: row["row_sha256"]
        for row in result["parameterized_graph_current_leg_template_rows"]
    }
    for row in result[
        "parameterized_source_injection_derivation_template_rows"
    ]:
        row["graph_current_leg_template_sha256s"] = [
            graph_hash[identifier]
            for identifier in row["graph_current_leg_template_ids"]
        ]
    close_rows(
        result, "parameterized_source_injection_derivation_template_rows"
    )
    pullback_hash = {
        row["recipient_pullback_map_template_id"]: row["row_sha256"]
        for row in result[
            "parameterized_recipient_pullback_map_template_rows"
        ]
    }
    for row in result["parameterized_F17_slot_template_rows"]:
        row["graph_current_leg_template_sha256"] = graph_hash[
            row["graph_current_leg_template_id"]
        ]
        row["recipient_pullback_map_template_sha256"] = pullback_hash[
            row["recipient_pullback_map_template_id"]
        ]
    close_rows(result, "parameterized_F17_slot_template_rows")

    slot_hash: dict[str, str] = {}
    round129 = closed_document(
        ROUND129_CERTIFICATE,
        v129.CERTIFICATE_SCHEMA,
    )["result"]
    for row in round129["parameterized_F1_F13_F16_slot_template_rows"]:
        slot_hash[row["field_slot_template_id"]] = row["row_sha256"]
    for group in (
        "parameterized_F14_slot_template_rows",
        "parameterized_F15_slot_template_rows",
        "parameterized_F17_slot_template_rows",
    ):
        for row in result[group]:
            slot_hash[row["field_slot_template_id"]] = row["row_sha256"]
    for row in result["parameterized_F1_F17_same_key_map_template_rows"]:
        row["standard_family_operator_template_sha256"] = operator_hash[
            row["standard_family_operator_template_id"]
        ]
        for binding in row["bound_preexisting_field_slot_templates"]:
            binding["field_slot_template_row_sha256"] = slot_hash[
                binding["field_slot_template_id"]
            ]
        row["bound_preexisting_field_slot_templates_sha256"] = digest(
            row["bound_preexisting_field_slot_templates"]
        )
    close_rows(
        result, "parameterized_F1_F17_same_key_map_template_rows"
    )
    map_hash = {
        row["same_key_map_template_id"]: row["row_sha256"]
        for row in result[
            "parameterized_F1_F17_same_key_map_template_rows"
        ]
    }
    for row in result["parameterized_F18_slot_template_rows"]:
        row["same_key_F1_F17_map_template_sha256"] = map_hash[
            row["same_key_F1_F17_map_template_id"]
        ]
    close_rows(result, "parameterized_F18_slot_template_rows")
    for row in result["parameterized_F18_slot_template_rows"]:
        slot_hash[row["field_slot_template_id"]] = row["row_sha256"]
    for row in result[
        "parameterized_local_18_field_level_block_template_rows"
    ]:
        for binding in row["field_slot_templates"]:
            binding["field_slot_template_row_sha256"] = slot_hash[
                binding["field_slot_template_id"]
            ]
        row["field_slot_templates_sha256"] = digest(
            row["field_slot_templates"]
        )
    close_rows(
        result, "parameterized_local_18_field_level_block_template_rows"
    )
    block_hash = {
        row["level_block_template_id"]: row["row_sha256"]
        for row in result[
            "parameterized_local_18_field_level_block_template_rows"
        ]
    }
    for row in result[
        "parameterized_local_18_field_child_packet_template_rows"
    ]:
        row["level_block_template_sha256s"] = [
            block_hash[identifier]
            for identifier in row["level_block_template_ids"]
        ]
    close_rows(
        result, "parameterized_local_18_field_child_packet_template_rows"
    )
    new_fields = [
        *result["parameterized_F14_slot_template_rows"],
        *result["parameterized_F15_slot_template_rows"],
        *result["parameterized_F17_slot_template_rows"],
        *result["parameterized_F18_slot_template_rows"],
    ]
    result["combined_template_registry"][
        "new_field_slot_template_ids_sha256"
    ] = digest([row["field_slot_template_id"] for row in new_fields])
    document["result_sha256"] = digest(result)


def mutation_cases(document: dict[str, Any]) -> list[
    tuple[str, tuple[Any, ...], Any]
]:
    r = ("result",)
    cases: list[tuple[str, tuple[Any, ...], Any]] = [
        ("status_promote", r + ("status",), "CERTIFIED_GLOBAL_18_OF_18"),
        ("precision_lower", r + ("precision_bits",), 2048),
        (
            "frozen_round129_verdict",
            r + ("frozen_input_contract", "Round129_verification_verdict"),
            "FAIL",
        ),
        (
            "lambda_version",
            r + (
                "exact_lambda_instance_contract",
                "canonical_exact_lambda_key_version",
            ),
            "round130-canonical-exact-lambda-key-v2",
        ),
        (
            "lambda_mathematical_key",
            r + ("exact_lambda_instance_contract", "mathematical_fibre_key"),
            "(family_root_id, locator text)",
        ),
        (
            "lambda_normalized_range",
            r + (
                "exact_lambda_instance_contract",
                "normalized_coordinate",
                "range",
            ),
            "[0,1)",
        ),
        (
            "lambda_dyadic_nonterminating",
            r + (
                "exact_lambda_instance_contract",
                "canonical_exact_lambda_key_case_split",
                "0<=u<1",
                "dyadic_rule",
            ),
            "use nonterminating eventually all 1",
        ),
        (
            "lambda_upper_binary",
            r + (
                "exact_lambda_instance_contract",
                "canonical_exact_lambda_key_case_split",
                "u=1",
                "binary_digit_sequence_forbidden",
            ),
            False,
        ),
        (
            "lambda_noncanonical_accept",
            r + (
                "exact_lambda_instance_contract",
                "noncanonical_lambda_locator_rejected",
            ),
            False,
        ),
        (
            "lambda_nonunique",
            r + (
                "exact_lambda_instance_contract",
                "one_exact_real_lambda_has_one_canonical_key",
            ),
            False,
        ),
        (
            "lambda_independent_b",
            r + (
                "exact_lambda_instance_contract",
                "independently_supplied_b_locator_or_b_key_accepted",
            ),
            True,
        ),
        (
            "lambda_finite_family",
            r + (
                "exact_lambda_instance_contract",
                "whole_uncountable_family_finitely_serializable",
            ),
            True,
        ),
        (
            "geometry_reuse_narrow_guard",
            r + (
                "family_stage3_geometry_contract",
                "Round123_240_bisection_exact_seed_brackets_reused",
            ),
            True,
        ),
        (
            "geometry_cut_count",
            r + ("family_stage3_geometry_contract", "combined_internal_cut_count"),
            214,
        ),
        (
            "endpoint_sign",
            r + (
                "uniform_stage3_endpoint_guard_template_rows",
                0,
                "all_lambda_left_function_sign",
            ),
            1,
        ),
        (
            "endpoint_canonical_key",
            r + (
                "uniform_stage3_endpoint_guard_template_rows",
                0,
                "canonical_exact_lambda_key_required_for_actual_endpoint_ID",
            ),
            False,
        ),
        (
            "natural_cell_terminal",
            r + (
                "parameterized_stage3_natural_cell_template_rows",
                0,
                "terminal_partial_cell",
            ),
            True,
        ),
        (
            "merged_cut_origin",
            r + (
                "parameterized_merged_cut_template_rows",
                0,
                "origin",
            ),
            "UNVERIFIED_CUT",
        ),
        (
            "fragment_common_rank",
            r + (
                "parameterized_stage3_output_fragment_template_rows",
                0,
                "common_rank",
            ),
            23,
        ),
        (
            "fragment_actual_not_template",
            r + (
                "parameterized_stage3_output_fragment_template_rows",
                0,
                "finite_row_is_a_template_not_an_actual_fibre_fragment",
            ),
            False,
        ),
        (
            "partition_not_exhaustive",
            r + (
                "parameterized_child_output_partition_template_rows",
                0,
                "disjoint_half_open_union_equals_actual_input_child_per_exact_lambda",
            ),
            False,
        ),
        (
            "leg_arbitrary_density",
            r + (
                "parameterized_accepted_norm_leg_template_rows",
                0,
                "arbitrary_positive_normalized_density_scope",
            ),
            False,
        ),
        (
            "F14_value_improve",
            r + (
                "parameterized_F14_slot_template_rows",
                0,
                "field_value_or_contract",
            ),
            "33",
        ),
        (
            "F14_pay_with_empty_F10",
            r + (
                "parameterized_F14_slot_template_rows",
                0,
                "Round129_F10_zero_is_dependency_only_not_F14_payment",
            ),
            False,
        ),
        (
            "F14_no_canonical_key",
            r + (
                "parameterized_F14_slot_template_rows",
                0,
                "canonical_exact_lambda_key_required_for_actual_slot",
            ),
            False,
        ),
        (
            "cemetery_nonexhaustive",
            r + (
                "parameterized_relative_zero_cemetery_template_rows",
                0,
                "partition_is_disjoint_half_open_and_exhaustive_per_exact_lambda",
            ),
            False,
        ),
        (
            "cemetery_relative_positive",
            r + (
                "parameterized_relative_zero_cemetery_template_rows",
                0,
                "restricted_relative_cemetery_arrival_kernel",
            ),
            "POSITIVE",
        ),
        (
            "cemetery_ambient_installed",
            r + (
                "parameterized_relative_zero_cemetery_template_rows",
                0,
                "ambient_pre_regularization_cemetery",
            ),
            "ZERO",
        ),
        (
            "cemetery_all_time_installed",
            r + (
                "parameterized_relative_zero_cemetery_template_rows",
                0,
                "all_time_owner_cemetery",
            ),
            "ZERO",
        ),
        (
            "operator_cross_dedup",
            r + (
                "parameterized_standard_family_operator_template_rows",
                0,
                "tag_preserving_and_no_cross_member_deduplication",
            ),
            False,
        ),
        (
            "operator_tag_cross_lambda",
            r + (
                "parameterized_standard_family_operator_template_rows",
                0,
                "output_member_tag_templates",
                0,
                "same_canonical_exact_lambda_key_required",
            ),
            False,
        ),
        (
            "F15_value_improve",
            r + (
                "parameterized_F15_slot_template_rows",
                0,
                "field_value_or_contract",
            ),
            "33",
        ),
        (
            "F15_no_Tonelli",
            r + (
                "parameterized_F15_slot_template_rows",
                0,
                "finite_positive_family_then_countable_Tonelli_completion",
            ),
            False,
        ),
        (
            "F15_global_raw_Z",
            r + (
                "per_fibre_F15_and_cemetery_contract",
                "global_raw_Z_Orlicz_owner_drift_claimed",
            ),
            True,
        ),
        (
            "F15_ambient_cemetery",
            r + (
                "per_fibre_F15_and_cemetery_contract",
                "ambient_pre_regularization_cemetery",
            ),
            "ZERO",
        ),
        (
            "input_trace_physical",
            r + (
                "parameterized_input_artificial_trace_template_rows",
                0,
                "artificial_not_physical",
            ),
            False,
        ),
        (
            "input_trace_cross_tag",
            r + (
                "parameterized_input_artificial_trace_template_rows",
                0,
                "cross_family_member_tag_cancellation_allowed",
            ),
            True,
        ),
        (
            "input_incidence_cancel",
            r + (
                "parameterized_input_trace_incidence_template_rows",
                0,
                "unconditional_cancellation_claimed",
            ),
            True,
        ),
        (
            "output_trace_drop_jacobian",
            r + (
                "parameterized_stage3_output_trace_template_rows",
                0,
                "Jacobian_factor_is_present",
            ),
            False,
        ),
        (
            "output_incidence_cross_lambda",
            r + (
                "parameterized_stage3_output_incidence_template_rows",
                0,
                "cross_lambda_and_cross_tag_cancellation_forbidden",
            ),
            False,
        ),
        (
            "output_incidence_uncancel",
            r + (
                "parameterized_stage3_output_incidence_template_rows",
                0,
                "cancelled_before_total_variation",
            ),
            False,
        ),
        (
            "source_injection_rank",
            r + (
                "parameterized_source_injection_contract_template_rows",
                0,
                "incidence_rank_B",
            ),
            14,
        ),
        (
            "graph_eta",
            r + (
                "parameterized_graph_current_leg_template_rows",
                0,
                "relative_center_velocity_eta",
            ),
            0,
        ),
        (
            "graph_physical_trace",
            r + (
                "parameterized_graph_current_leg_template_rows",
                0,
                "physical_trace_count",
            ),
            1,
        ),
        (
            "graph_crosswalk_erase_artificial",
            r + (
                "parameterized_graph_current_leg_template_rows",
                0,
                "artificial_traces_are_not_physical_F13_traces",
            ),
            False,
        ),
        (
            "recipient_scalar_only",
            r + (
                "parameterized_recipient_component_template_rows",
                0,
                "dual_recipient",
            ),
            "scalar distribution",
        ),
        (
            "pullback_bad_determinant",
            r + (
                "parameterized_recipient_pullback_map_template_rows",
                0,
                "area_coordinate_determinant",
            ),
            "2",
        ),
        (
            "pullback_one_component",
            r + (
                "parameterized_recipient_pullback_map_template_rows",
                0,
                "both_Eulerian_vector_components_are_received",
            ),
            False,
        ),
        (
            "derivation_leg_count",
            r + (
                "parameterized_source_injection_derivation_template_rows",
                0,
                "leg_count_per_exact_lambda",
            ),
            23,
        ),
        (
            "F17_rename_F11",
            r + (
                "parameterized_F17_slot_template_rows",
                0,
                "F17_is_not_a_rename_of_F11",
            ),
            False,
        ),
        (
            "F17_value_improve",
            r + (
                "parameterized_F17_slot_template_rows",
                0,
                "field_value_or_contract",
            ),
            "4915199",
        ),
        (
            "F17_contract_cross_lambda",
            r + (
                "per_fibre_F17_graph_current_contract",
                "cross_lambda_or_cross_tag_cancellation_forbidden",
            ),
            False,
        ),
        (
            "same_key_field_count",
            r + (
                "parameterized_F1_F17_same_key_map_template_rows",
                0,
                "bound_preexisting_field_count",
            ),
            16,
        ),
        (
            "same_key_shared_operator",
            r + (
                "parameterized_F1_F17_same_key_map_template_rows",
                0,
                "all_fields_share_family_root_common_rank_stage_recut_and_operator",
            ),
            False,
        ),
        (
            "same_key_no_canonical",
            r + (
                "parameterized_F1_F17_same_key_map_template_rows",
                0,
                "canonical_exact_lambda_key_required_for_actual_map",
            ),
            False,
        ),
        (
            "F18_phase_route",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "phase_route",
            ),
            "Wiener",
        ),
        (
            "F18_bad_suffix",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "suffix_length_r_minus_j",
            ),
            1,
        ),
        (
            "F18_Wiener",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "operator_Wiener_invertibility_claimed",
            ),
            True,
        ),
        (
            "F18_aperiodic",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "operator_Wiener_aperiodicity_claimed",
            ),
            True,
        ),
        (
            "F18_Kac",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "Kac_closure_claimed",
            ),
            True,
        ),
        (
            "F18_global",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "global_operator_phase_block_claimed",
            ),
            True,
        ),
        (
            "F18_CM2",
            r + (
                "parameterized_F18_slot_template_rows",
                0,
                "CM2_claimed",
            ),
            True,
        ),
        (
            "level_block_field_count",
            r + (
                "parameterized_local_18_field_level_block_template_rows",
                0,
                "field_count",
            ),
            17,
        ),
        (
            "level_block_global",
            r + (
                "parameterized_local_18_field_level_block_template_rows",
                0,
                "global_complete_18_field_block",
            ),
            True,
        ),
        (
            "packet_level_count",
            r + (
                "parameterized_local_18_field_child_packet_template_rows",
                0,
                "level_block_count",
            ),
            4,
        ),
        (
            "packet_global",
            r + (
                "parameterized_local_18_field_child_packet_template_rows",
                0,
                "global_complete_18_field_block",
            ),
            True,
        ),
        (
            "phase_contract_Wiener",
            r + (
                "per_fibre_F18_phase_contract",
                "operator_Wiener_theorem",
            ),
            "CLAIMED",
        ),
        (
            "registry_combined_count",
            r + (
                "combined_template_registry",
                "combined_field_slot_template_count",
            ),
            2161,
        ),
        (
            "ledger_whole_family_finite",
            r + ("count_ledger", "whole_family_actual_slot_row_count"),
            2160,
        ),
        (
            "ledger_global_block",
            r + ("count_ledger", "global_complete_18_field_block_count"),
            120,
        ),
        (
            "local_maturity_globalize",
            r + (
                "positive_Borel_family_every_exact_fibre_local_field_maturity",
            ),
            "GLOBAL_18/18",
        ),
        (
            "global_complete_blocks",
            r + ("global_complete_18_field_block_count",),
            120,
        ),
        ("complete_blocks", r + ("complete_18_field_block_count",), 120),
        ("gate5_blocks", r + ("gate5_block_count",), 120),
        ("gate5_maturity", r + ("gate5_global_maturity",), "18/18"),
        ("gate5_status", r + ("gate5_status",), "CERTIFIED"),
        ("cm2_promote", r + ("cm2_verdict",), "GO_FOR_CLAIM"),
        (
            "remove_nonclaim",
            r + ("strict_nonclaims", 9),
            "global complete 18-field blocks installed",
        ),
    ]
    return cases


def semantic_mutations(
    document: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
    round129: dict[str, Any],
    round129_verification: dict[str, Any],
    cache: dict[str, Any],
) -> list[str]:
    rejected: list[str] = []
    for label, path, replacement in mutation_cases(document):
        mutant = copy.deepcopy(document)
        require(
            get_path(mutant, path) != replacement,
            f"mutation changes value:{label}",
        )
        set_path(mutant, path, replacement)
        resign_document(mutant)
        try:
            validate_document(
                mutant,
                documents,
                core,
                round129,
                round129_verification,
                cache=cache,
            )
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(raw: bytes) -> list[str]:
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate_top_schema",
            b'{"schema":"a","schema":"b","result":{},"result_sha256":"x"}',
        ),
        (
            "duplicate_nested_key",
            b'{"schema":"a","result":{"x":1,"x":2},"result_sha256":"x"}',
        ),
        ("NaN", b'{"x":NaN}'),
        ("Infinity", b'{"x":Infinity}'),
        ("negative_Infinity", b'{"x":-Infinity}'),
        ("decimal_float", b'{"x":1.5}'),
        ("exponent_float", b'{"x":1e2}'),
        ("negative_zero", b'{"x":-0}'),
        ("oversized_integer", b'{"x":' + b"1" * 1025 + b"}"),
        ("UTF8_BOM", b"\xef\xbb\xbf{}"),
        ("invalid_UTF8", b'{"x":"\xff"}'),
        ("NUL_byte", b'{"x":"\x00"}'),
        ("top_level_array", b"[]"),
        ("trailing_garbage", b"{} trailing"),
        ("unpaired_surrogate", b'{"x":"\\ud800"}'),
        ("truncated_JSON", raw[:100]),
    ]
    rejected: list[str] = []
    for label, payload in attacks:
        try:
            value = parse_bytes(payload)
            require(
                set(value) == {"schema", "result", "result_sha256"},
                "strict attack closed envelope",
            )
            require(
                type(value["result"]) is dict
                and value["result_sha256"] == digest(value["result"]),
                "strict attack closure",
            )
        except (
            VerificationError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def verification_result(
    document: dict[str, Any],
    summary: dict[str, Any],
    cache: dict[str, Any],
    mutation_labels: list[str],
    strict_labels: list[str],
) -> dict[str, Any]:
    geometry = cache["geometry"]
    f17 = cache["f17"]
    lambda_vectors = cache["lambda_vectors"]
    crosswalk_vectors = cache["actual_slot_crosswalk_test_vectors"]
    return {
        "verdict": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": sha256(VERIFIER),
        "verification_precision_bits": VERIFIER_PRECISION_BITS,
        "frozen_independent_inputs": {
            "Round129_verifier_sha256": ROUND129_VERIFIER_SHA256,
            "Round129_certificate_sha256": ROUND129_CERTIFICATE_SHA256,
            "Round129_verification_sha256": ROUND129_VERIFICATION_SHA256,
            "Round122_Jet2_verifier_sha256":
                v129.UPSTREAM_PINS[
                    "cm2_round122_rank3_exact_seed_"
                    "physical_face_field_bridge_verifier.py"
                ],
        },
        "independence_contract": {
            "Round130_producer_imported": False,
            "Round130_producer_executed": False,
            "Round130_producer_used_only_as_byte_pinned_input": True,
            "Round129_independent_verifier_reused_under_byte_pin": True,
            "Round129_certificate_independently_revalidated": True,
            "Round122_independent_Jet2_layer_reused_under_byte_pin": True,
            "canonical_exact_lambda_key_case_split_independently_checked": True,
            "canonical_exact_lambda_test_vectors_replayed": True,
            "lambda_to_b_mapping_replayed_in_one_way_derived_direction": True,
            "independently_supplied_b_locator_or_key_used": False,
            "uniform_stage3_family_independently_replayed": True,
            "lambda_by_s_F17_physical_geometry_independently_replayed": True,
            "actual_18_field_slot_crosswalk_independently_rebuilt": True,
            "global_nonpromotion_independently_checked": True,
        },
        "canonical_exact_lambda_key_test_vectors": lambda_vectors,
        "independent_geometry": {
            "U3_length_over_delta_strict_enclosure":
                geometry["u3_ratio"],
            "U3_x_over_delta_strict_enclosure":
                geometry["u3_derivative"],
            "minimum_combined_cut_gap_strict_lower":
                geometry["minimum_combined_gap"],
            "minimum_stage3_fragment_length_strict_lower":
                geometry["minimum_stage3_length"],
            "minimum_accepted_normalized_output_length_by_stage":
                geometry["stage_minima"],
            "stage3_endpoint_guard_count": 192,
            "stage3_natural_cell_count": 193,
            "merged_cut_count": 215,
            "stage3_output_fragment_count": 216,
            "accepted_norm_leg_count": 72,
        },
        "independent_F17": {
            "maximum_actual_l1_generator_upper_by_stage":
                f17["independent_max_l1"],
            "minimum_guarded_target_cosine_lower_by_stage":
                f17["independent_min_cosine"],
            "input_artificial_trace_count": len(f17["input_rows"]),
            "input_inter_child_incidence_count":
                len(f17["input_incidence_rows"]),
            "stage3_output_trace_count": len(f17["output_rows"]),
            "stage3_output_incidence_count":
                len(f17["output_incidence_rows"]),
            "stage3_same_input_cancelled_incidence_count":
                f17["cancelled"],
            "stage3_inter_child_retained_incidence_count":
                f17["retained"],
            "graph_current_leg_count": len(f17["graph_rows"]),
            "recipient_component_count": len(f17["component_rows"]),
            "recipient_pullback_map_count": len(f17["pullback_rows"]),
            "source_injection_derivation_count":
                len(f17["derivation_rows"]),
        },
        "actual_slot_crosswalk_test_vectors": crosswalk_vectors,
        "registry_summary": summary,
        "semantic_resigned_mutation_count": len(mutation_labels),
        "semantic_resigned_mutation_rejection_labels": mutation_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "fail_closed_safety": {
            "positive_Borel_every_exact_fibre_local_maturity": "18/18",
            "local_complete_18_field_level_block_count_per_exact_lambda": 120,
            "local_complete_18_field_child_packet_count_per_exact_lambda": 24,
            "whole_uncountable_family_finitely_serialized": False,
            "global_Gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_status": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        safe_input_path(args.certificate)
        safe_output_path(args.output, args.certificate)
        require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
        require(
            sha256(args.certificate) == CERTIFICATE_SHA256,
            "official certificate byte pin",
        )
        raw = args.certificate.read_bytes()
        document = parse_bytes(raw)
        require(
            document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
            "official certificate result pin",
        )
        ctx.prec = VERIFIER_PRECISION_BITS
        documents, core, round129, round129_verification = validate_upstream()
        summary, cache = validate_document(
            document,
            documents,
            core,
            round129,
            round129_verification,
        )
        mutation_labels = semantic_mutations(
            document,
            documents,
            core,
            round129,
            round129_verification,
            cache,
        )
        strict_labels = strict_json_attacks(raw)
        result = verification_result(
            document,
            summary,
            cache,
            mutation_labels,
            strict_labels,
        )
        envelope = {
            "schema": VERIFICATION_SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        atomic_write(args.output, envelope)
        print("PASS")
        print(
            "canonical_exact_lambda_test_vectors="
            f"{summary['canonical_lambda_test_vector_count']}"
        )
        print(
            "actual_slot_crosswalk_test_vectors="
            f"{len(cache['actual_slot_crosswalk_test_vectors'])}"
        )
        print(f"semantic_resigned_mutations={len(mutation_labels)}")
        print(f"strict_json_attacks={len(strict_labels)}")
        print(f"local_maturity={summary['local_maturity']}")
        print(f"global_maturity={summary['global_maturity']}")
        print(f"global_complete_blocks={summary['global_complete_blocks']}")
        print(f"CM2={summary['cm2']}")
        print(f"result_sha256={envelope['result_sha256']}")
        return 0
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
