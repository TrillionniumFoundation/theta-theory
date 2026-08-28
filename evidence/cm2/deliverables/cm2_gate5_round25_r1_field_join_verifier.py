#!/usr/bin/env python3
"""Fail-closed verifier for the round-25 Gate-5 R1 candidate-field join.

The verifier pins the producer and all declared dependencies, replays the
producer deterministically, and then independently audits every one of the
4,216 candidate packets against the frozen adaptive raw-leaf registry.  The
only accepted conclusion is candidate/local F1--F6 maturity 6/18, with zero
F7 slots, zero complete 18-field blocks, and no change to global Gate 5.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Any, Callable


Q = Fraction
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate5_round25_r1_field_join_cert.py"
MANIFEST = HERE / "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
REPORT = HERE / "cm2-gate5-round25-r1-field-join-assault-2026-07-18.md"
EXPECTED_CERTIFICATE_SHA256 = (
    "50b4b5f79f4ad71ba02038290f5737eb5a8cd5be1a1067fa12f4a684374db811"
)
MANIFEST_SCHEMA = "cm2.gate5.round25-r1-field-join.manifest.v1"
RESULT_SCHEMA = "cm2.gate5.round25-r1-field-join.v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_DEPENDENCIES = {
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json":
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate25_selected_component_chart_field_slots_cert.py":
        "666e7f1ea4198528b143b522d2c5daf55ba4fecfd127d86663b23e0bb38a477f",
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json":
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271",
    "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json":
        "75de341183ef7fbcc7937f69bc7c6f276d06db0883397a7c99e4d54bbc5dc91a",
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json":
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json":
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}

ADAPTIVE_MANIFEST = (
    HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
)
SCHEMA_MANIFEST = (
    HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
CANDIDATE_LOCAL_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)
FIELD7 = "one_step_cut_growth_Z_sum"
PARAMETER_UPPER = Q(1, 400)

TOP_KEYS = {
    "schema", "date", "certificate_sha256", "verifier_sha256",
    "report_sha256", "dependencies", "result", "verdict",
}
RESULT_KEYS = {
    "schema", "provenance", "R1_source_component_binding_registry",
    "R1_field_template_registry", "R1_inner_field_join_registry",
    "R1_inner_candidate_field_packet_rows",
    "Gate5_R1_inner_18_field_maturity", "strict_nonpromotion",
    "internal_replay_digest",
}
PACKET_KEYS = {
    "atom_id", "source_core_id", "destination_core_id", "source_binding_id",
    "maximal_component_id", "parent_selected_homogeneous_component_row_id",
    "physical_homogeneity_subbranch_id", "roof", "roof_level_j",
    "parameter_guard", "source_box_sha256", "candidate_local_fields",
    "candidate_local_slots", "F7_parent_provenance",
    "r1_candidate_field_packet_id",
}


class VerificationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise VerificationError(code, detail)


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError("NONFINITE_JSON", token)


def parse_json_text(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_constant,
        )
    except VerificationError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise VerificationError("MALFORMED_JSON", str(exc)) from exc


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_regular_file(path: Path, code: str) -> None:
    require(path.parent.resolve() == HERE, code, f"escaped parent: {path.name}")
    require(not path.is_symlink(), code, f"symlink: {path.name}")
    require(path.is_file(), code, f"missing: {path.name}")


def load_certificate() -> ModuleType:
    require(sys.flags.optimize == 0, "OPTIMIZED_PYTHON")
    safe_regular_file(CERTIFICATE, "CERTIFICATE_PATH")
    require(
        sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
        "CERTIFICATE_HASH",
    )
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        safe_regular_file(path, "DEPENDENCY_PATH")
        require(sha256_path(path) == expected, "DEPENDENCY_HASH", name)
    spec = importlib.util.spec_from_file_location(
        "cm2_gate5_round25_r1_field_join_cert_frozen", CERTIFICATE
    )
    require(spec is not None and spec.loader is not None, "IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    require(Path(module.__file__).resolve() == CERTIFICATE, "IMPORT_PATH")
    require(
        sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
        "CERTIFICATE_REHASH",
    )
    require(module.DEPENDENCIES == EXPECTED_DEPENDENCIES, "PRODUCER_DEPENDENCIES")
    return module


def result_digest(result: dict[str, Any]) -> str:
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def template_digest(template: dict[str, Any], label: str) -> str:
    payload = dict(template)
    payload.pop("template_id", None)
    return f"template:{label}:" + digest(payload)


def packet_digest(packet: dict[str, Any]) -> str:
    payload = dict(packet)
    payload.pop("r1_candidate_field_packet_id", None)
    return "r1-candidate-field-packet:" + digest(payload)


def independent_semantic_audit(result: dict[str, Any]) -> None:
    require(type(result) is dict and set(result) == RESULT_KEYS, "RESULT_KEYS")
    require(result["schema"] == RESULT_SCHEMA, "RESULT_SCHEMA")
    require(result["internal_replay_digest"] == result_digest(result), "RESULT_DIGEST")
    provenance = result["provenance"]
    require(type(provenance) is dict, "PROVENANCE_TYPE")
    require(provenance["dependency_sha256"] == EXPECTED_DEPENDENCIES,
            "PROVENANCE_DEPENDENCIES")
    require(provenance["old_artifacts_modified"] is False, "OLD_ARTIFACTS")
    require(provenance["join_policy"] == "independent_fieldwise_fail_closed",
            "JOIN_POLICY")

    templates = result["R1_field_template_registry"]
    require(type(templates) is dict and set(templates) == {"F1", "F2", "F5", "F6"},
            "TEMPLATE_KEYS")
    for label in ("F1", "F2", "F5", "F6"):
        require(templates[label]["template_id"] == template_digest(templates[label], label),
                "TEMPLATE_ID", label)
    require(templates["F5"]["universal_adapted_inverse_strict_upper"]
            == "144000/180337", "F5_TEMPLATE_BOUND")
    require(templates["F6"]["canonical_curve_log_variation_strict_upper"]
            == "3/200000", "F6_TEMPLATE_BOUND")
    require(templates["F5"]["invariant_area_Jacobian_used"] is False,
            "F5_AREA_MISUSE")
    require(templates["F6"]["invariant_area_Jacobian_used"] is False,
            "F6_AREA_MISUSE")

    binding_registry = result["R1_source_component_binding_registry"]
    require(binding_registry["all_source_binding_count"] == 24, "BINDING_COUNT")
    require(binding_registry["used_roof_one_source_binding_count"] == 16,
            "USED_BINDING_COUNT")
    used_bindings = binding_registry["used_roof_one_source_binding_rows"]
    require(type(used_bindings) is list and len(used_bindings) == 16,
            "USED_BINDING_ROWS")
    require(binding_registry["used_roof_one_source_binding_rows_sha256"]
            == digest(used_bindings), "USED_BINDING_DIGEST")
    binding_by_source: dict[str, dict[str, Any]] = {}
    for binding in used_bindings:
        require(binding["source_core_id"] not in binding_by_source,
                "DUPLICATE_BINDING")
        require(binding["roof"] == 1 and len(binding["level_rows"]) == 1,
                "ROOF_ONE_BINDING")
        require(binding["source_and_target_central_homogeneity"] is True,
                "CENTRAL_BINDING")
        binding_by_source[binding["source_core_id"]] = binding

    adaptive = parse_json_text(ADAPTIVE_MANIFEST.read_text(encoding="utf-8"))
    raw_rows = adaptive["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    return_rows = [row for row in raw_rows if row["classification"] == "RETURN_AT_1_INNER"]
    require(len(return_rows) == 4216, "UPSTREAM_R1_COUNT")
    adaptive_by_atom = {row["atom_id"]: row for row in return_rows}
    require(len(adaptive_by_atom) == 4216, "UPSTREAM_R1_UNIQUE")
    require(adaptive["verdict"]["unresolved_step1_outer_cover"] == "NONEMPTY",
            "UPSTREAM_OUTER_COVER")

    packets = result["R1_inner_candidate_field_packet_rows"]
    require(type(packets) is list and len(packets) == 4216, "PACKET_COUNT")
    require([packet["atom_id"] for packet in packets]
            == sorted(adaptive_by_atom), "PACKET_ORDER_OR_COVER")

    slot_ids: set[str] = set()
    h_ids: set[str] = set()
    source_histogram: Counter[str] = Counter()
    destination_histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    for packet in packets:
        require(type(packet) is dict and set(packet) == PACKET_KEYS, "PACKET_KEYS")
        atom_id = packet["atom_id"]
        upstream = adaptive_by_atom[atom_id]
        require(packet["source_core_id"] == upstream["source_core_id"],
                "PACKET_SOURCE", atom_id)
        require(packet["destination_core_id"] == upstream["destination_core_id"],
                "PACKET_DESTINATION", atom_id)
        require(upstream["depth"] > 0, "ARTIFICIAL_FACE", atom_id)
        require(upstream["positive_two_dimensional_source_rectangle_at_each_s"] is True,
                "POSITIVE_PHASE", atom_id)
        require(upstream["positive_parameter_interval"] is True,
                "POSITIVE_PARAMETER", atom_id)
        require(packet["roof"] == 1 and packet["roof_level_j"] == 0,
                "PACKET_ROOF", atom_id)
        require(packet["candidate_local_fields"] == list(CANDIDATE_LOCAL_FIELDS),
                "CANDIDATE_FIELD_LIST", atom_id)
        require(FIELD7 not in packet["candidate_local_slots"], "F7_INSTALLED", atom_id)

        binding = binding_by_source.get(packet["source_core_id"])
        require(binding is not None, "MISSING_BINDING", atom_id)
        require(packet["source_binding_id"] == binding["source_binding_id"],
                "SOURCE_BINDING", atom_id)
        require(packet["maximal_component_id"] == binding["maximal_component_id"],
                "COMPONENT_BINDING", atom_id)
        require(packet["parent_selected_homogeneous_component_row_id"]
                == binding["parent_selected_homogeneous_component_row_id"],
                "PARENT_H_BINDING", atom_id)

        h_payload = {
            "atom_id": atom_id,
            "source_core_id": packet["source_core_id"],
            "destination_core_id": packet["destination_core_id"],
            "source_label": "H0:abs(p)<3/10",
            "target_label": "H0:abs(p)<3/10",
            "intermediate_solid_collision_count": 0,
            "transparent_wall_level_count": 0,
            "complete_table_row_count": 1,
        }
        h_id = "h:r1:" + digest(h_payload)
        require(packet["physical_homogeneity_subbranch_id"] == h_id,
                "HOMOGENEITY_ID", atom_id)
        require(h_id not in h_ids, "DUPLICATE_HOMOGENEITY_ID", atom_id)
        h_ids.add(h_id)

        source_box = upstream["source_box"]
        require(packet["source_box_sha256"] == digest(source_box),
                "SOURCE_BOX_DIGEST", atom_id)
        s0, s1 = Q(source_box["s"][0]), Q(source_box["s"][1])
        expected_guard = {
            "s_lower": str(s0),
            "s_upper": str(s1),
            "lower_closed": True,
            "upper_closed": s1 == PARAMETER_UPPER,
            "internal_boundary_owner":
                "right_leaf_via_lower_closed_upper_open_convention",
        }
        require(packet["parameter_guard"] == expected_guard,
                "PARAMETER_GUARD", atom_id)

        slots = packet["candidate_local_slots"]
        require(type(slots) is dict and set(slots) == set(CANDIDATE_LOCAL_FIELDS),
                "CANDIDATE_SLOT_KEYS", atom_id)
        for field in CANDIDATE_LOCAL_FIELDS:
            slot = slots[field]
            require(type(slot) is dict and set(slot) == {"immutable_slot_id", "payload"},
                    "SLOT_KEYS", field)
            slot_payload = {
                "atom_id": atom_id,
                "physical_homogeneity_subbranch_id": h_id,
                "roof_level_j": 0,
                "field_name": field,
                "field_payload": slot["payload"],
            }
            expected_slot_id = "slot:r1:" + digest(slot_payload)
            require(slot["immutable_slot_id"] == expected_slot_id,
                    "SLOT_ID", field)
            require(expected_slot_id not in slot_ids, "DUPLICATE_SLOT_ID", field)
            slot_ids.add(expected_slot_id)

        f1 = slots[CANDIDATE_LOCAL_FIELDS[0]]["payload"]
        require(f1["template_id"] == templates["F1"]["template_id"],
                "F1_TEMPLATE", atom_id)
        require(f1["parameter_guard"] == expected_guard, "F1_GUARD", atom_id)
        domain = f1["candidate_domain"]
        require(domain["closed_box_provenance"] == source_box,
                "F1_BOX", atom_id)
        require(domain["candidate_domain_is_complete_global_R1_partition"] is False,
                "F1_NONPROMOTION", atom_id)
        require(domain["positive_phase_rectangle_at_each_guarded_parameter"] is True
                and domain["positive_parameter_interval"] is True,
                "F1_POSITIVITY", atom_id)

        f2 = slots[CANDIDATE_LOCAL_FIELDS[1]]["payload"]
        require(f2 == {
            "template_id": templates["F2"]["template_id"],
            "physical_homogeneity_subbranch_id": h_id,
            "table_rows_sha256": digest([h_payload]),
        }, "F2_PAYLOAD", atom_id)
        level = binding["level_rows"][0]
        f3 = slots[CANDIDATE_LOCAL_FIELDS[2]]["payload"]
        f4 = slots[CANDIDATE_LOCAL_FIELDS[3]]["payload"]
        require(f3["parent_slot_id"] == level["parent_F3_slot_id"]
                and f3["field_value"] == level["parent_F3_prefix_chart"]
                and f3["restriction_inherits_chart"] is True,
                "F3_BINDING", atom_id)
        require(f4["parent_slot_id"] == level["parent_F4_slot_id"]
                and f4["field_value"] == level["parent_F4_suffix_chart"]
                and f4["restriction_inherits_chart"] is True,
                "F4_BINDING", atom_id)
        f5 = slots[CANDIDATE_LOCAL_FIELDS[4]]["payload"]
        f6 = slots[CANDIDATE_LOCAL_FIELDS[5]]["payload"]
        require(f5["template_id"] == templates["F5"]["template_id"]
                and f5["adapted_inverse_strict_upper"] == "144000/180337"
                and f5["Euclidean_inverse_strict_upper"] == "27410400/180337"
                and f5["invariant_area_Jacobian_used"] is False,
                "F5_PAYLOAD", atom_id)
        require(f6["template_id"] == templates["F6"]["template_id"]
                and f6["Holder_exponent"] == "1/3"
                and f6["canonical_log_variation_strict_upper"] == "3/200000"
                and f6["invariant_area_Jacobian_used"] is False,
                "F6_PAYLOAD", atom_id)

        f7 = packet["F7_parent_provenance"]
        require(f7 == {
            "parent_slot_id": level["parent_F7_slot_id"],
            "parent_multiplier_upper": level["parent_F7_multiplier_upper"],
            "adaptive_atom_has_artificial_dyadic_face": True,
            "destination_core_preimage_boundary_materialized": False,
            "destination_core_test_role": "strict_whole_rectangle_classification_only",
            "adaptive_restriction_boundary_Z_bound": "NOT_CERTIFIED",
            "R1_atom_F7_slot": "NOT_MATERIALIZED",
        }, "F7_NONTRANSFER", atom_id)
        require(packet["r1_candidate_field_packet_id"] == packet_digest(packet),
                "PACKET_ID", atom_id)
        source_histogram[packet["source_core_id"]] += 1
        destination_histogram[packet["destination_core_id"]] += 1
        depth_histogram[upstream["depth"]] += 1

    registry = result["R1_inner_field_join_registry"]
    require(registry["R1_inner_atom_count"] == 4216, "REGISTRY_COUNT")
    require(registry["R1_inner_candidate_local_roof_histogram"] == {"1": 4216},
            "ROOF_HISTOGRAM")
    require(registry["R1_inner_source_core_count"] == len(source_histogram) == 16,
            "SOURCE_COUNT")
    require(registry["R1_inner_destination_core_count"] == len(destination_histogram) == 16,
            "DESTINATION_COUNT")
    require(registry["R1_inner_source_histogram_sha256"]
            == digest(dict(sorted(source_histogram.items()))), "SOURCE_HISTOGRAM")
    require(registry["R1_inner_destination_histogram_sha256"]
            == digest(dict(sorted(destination_histogram.items()))), "DESTINATION_HISTOGRAM")
    require(registry["R1_inner_depth_histogram"]
            == {str(k): v for k, v in sorted(depth_histogram.items())},
            "DEPTH_HISTOGRAM")
    require(registry["materialized_candidate_local_F1_to_F6_slot_count"]
            == len(slot_ids) == 25296, "SLOT_COUNT")
    require(registry["materialized_candidate_local_physical_homogeneity_table_count"]
            == len(h_ids) == 4216, "H_TABLE_COUNT")
    require(registry["materialized_R1_F7_slot_count"] == 0, "REGISTRY_F7")
    require(registry["R1_candidate_field_packet_rows_sha256"] == digest(packets),
            "PACKET_DIGEST")

    schema = parse_json_text(SCHEMA_MANIFEST.read_text(encoding="utf-8"))
    schema_fields = schema["result"]["required_operator_field_schema"]["required_fields"]
    require(len(schema_fields) == 18, "SCHEMA_FIELD_COUNT")
    maturity = result["Gate5_R1_inner_18_field_maturity"]
    require(maturity["candidate_local_maturity"] == "6/18", "LOCAL_MATURITY")
    require(maturity["candidate_local_field_count_per_R1_inner_atom"] == 6,
            "LOCAL_FIELD_COUNT")
    require(maturity["global_Gate5_maturity_before_round25_leaf"] == "4/18"
            and maturity["global_Gate5_maturity_after_round25_leaf"] == "4/18",
            "GLOBAL_MATURITY")
    require(maturity["global_Gate5_field_credit_added"] == 0,
            "GLOBAL_CREDIT")
    require(maturity["materialized_R1_inner_F7_candidate_local_slot_count"] == 0,
            "MATURITY_F7")
    require(maturity["complete_18_field_R1_inner_operator_block_count"] == 0,
            "COMPLETE_BLOCK")
    rows = maturity["rows"]
    require(len(rows) == 18 and maturity["rows_sha256"] == digest(rows),
            "MATURITY_ROWS")
    require([row["field"] for row in rows] == schema_fields,
            "MATURITY_FIELD_ORDER")
    require(sum(row["candidate_local_R1_inner_atom_slot_count"] > 0 for row in rows)
            == 6, "MATURITY_SIX")
    require(all(row["global_complete_roof_level_slot_count_added"] == 0
                for row in rows), "MATURITY_NO_GLOBAL_CREDIT")

    nonpromotion = result["strict_nonpromotion"]
    require(nonpromotion["parent_F7_slot_survives_unpriced_adaptive_restriction"]
            is False, "NONPROMOTION_F7")
    require(nonpromotion["materialized_R1_inner_F7_candidate_local_slot_count"] == 0,
            "NONPROMOTION_F7_COUNT")
    require(nonpromotion["complete_18_field_R1_inner_operator_block_count"] == 0,
            "NONPROMOTION_BLOCK")
    require(nonpromotion["global_Gate5_maturity_before_and_after"] == "4/18 -> 4/18"
            and nonpromotion["global_Gate5_field_credit_added"] == 0,
            "NONPROMOTION_GLOBAL")
    require(nonpromotion["Gate5"] == "NOT_CERTIFIED", "GATE5_PROMOTION")
    require(nonpromotion["CM2"] == "NO-GO_FOR_CLAIM", "CM2_PROMOTION")


def validate_manifest(
    manifest: Any,
    expected_result: dict[str, Any],
    expected_result_sha256: str,
    *,
    run_semantic_audit: bool = True,
) -> None:
    require(type(manifest) is dict, "TOP_TYPE")
    require(set(manifest) == TOP_KEYS, "TOP_KEYS")
    for key in ("schema", "date", "certificate_sha256", "verifier_sha256",
                "report_sha256", "verdict"):
        require(type(manifest[key]) is str, "FIELD_TYPE", key)
    require(type(manifest["dependencies"]) is dict, "FIELD_TYPE", "dependencies")
    require(type(manifest["result"]) is dict, "FIELD_TYPE", "result")
    require(manifest["schema"] == MANIFEST_SCHEMA, "MANIFEST_SCHEMA")
    require(manifest["date"] == "2026-07-18", "DATE")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        require(HEX64.fullmatch(manifest[key]) is not None, "MALFORMED_SHA", key)
    require(manifest["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_PIN")
    require(manifest["dependencies"] == EXPECTED_DEPENDENCIES, "DEPENDENCY_MAP")
    require(digest(manifest["result"]) == expected_result_sha256,
            "RESULT_MISMATCH")
    require(canonical_bytes(manifest["result"]) == canonical_bytes(expected_result),
            "RESULT_REPLAY_MISMATCH")
    require(manifest["verdict"] == (
        "4216 R1-INNER CANDIDATES HAVE LOCAL F1-F6 PACKETS (6/18); "
        "F7 SLOTS 0; COMPLETE 18-FIELD BLOCKS 0; GLOBAL GATE 5 REMAINS 4/18 "
        "AND NOT CERTIFIED"
    ), "VERDICT")
    if run_semantic_audit:
        independent_semantic_audit(manifest["result"])


def load_and_validate() -> tuple[dict[str, Any], dict[str, Any], str]:
    safe_regular_file(MANIFEST, "MANIFEST_PATH")
    safe_regular_file(REPORT, "REPORT_PATH")
    safe_regular_file(Path(__file__).resolve(), "VERIFIER_PATH")
    certificate = load_certificate()
    expected_result = certificate.build_result()
    expected_result_sha256 = digest(expected_result)
    manifest = parse_json_text(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest, expected_result, expected_result_sha256)
    require(sha256_path(CERTIFICATE) == manifest["certificate_sha256"],
            "CERTIFICATE_HASH")
    require(sha256_path(Path(__file__).resolve()) == manifest["verifier_sha256"],
            "VERIFIER_HASH")
    require(sha256_path(REPORT) == manifest["report_sha256"], "REPORT_HASH")
    require(sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_REHASH")
    for name, expected in EXPECTED_DEPENDENCIES.items():
        require(sha256_path(HERE / name) == expected, "DEPENDENCY_REHASH", name)
    gc.collect()
    return manifest, expected_result, expected_result_sha256


def set_path(root: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> Any:
    cursor: Any = root
    for key in path[:-1]:
        cursor = cursor[key]
    old = cursor[path[-1]]
    cursor[path[-1]] = replacement
    return old


def run_self_test(
    valid: dict[str, Any],
    expected: dict[str, Any],
    expected_sha256: str,
) -> int:
    passed = 0

    def expect_rejected(
        name: str,
        expected_code: str,
        mutate: Callable[[], Callable[[], None]],
    ) -> None:
        nonlocal passed
        undo = mutate()
        try:
            validate_manifest(
                valid, expected, expected_sha256, run_semantic_audit=False
            )
        except VerificationError as exc:
            require(exc.code == expected_code, "SELF_TEST_WRONG_CODE",
                    f"{name}: {exc.code} != {expected_code}")
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", name)
        finally:
            undo()

    def replace(path: tuple[Any, ...], value: Any) -> Callable[[], Callable[[], None]]:
        def mutation() -> Callable[[], None]:
            old = set_path(valid, path, value)
            return lambda: set_path(valid, path, old)
        return mutation

    def remove_top(key: str) -> Callable[[], Callable[[], None]]:
        def mutation() -> Callable[[], None]:
            old = valid.pop(key)
            return lambda: valid.__setitem__(key, old)
        return mutation

    def extra_top() -> Callable[[], Callable[[], None]]:
        valid["extra"] = False
        return lambda: valid.pop("extra")

    expect_rejected("missing top", "TOP_KEYS", remove_top("date"))
    expect_rejected("extra top", "TOP_KEYS", extra_top)
    expect_rejected("schema", "MANIFEST_SCHEMA", replace(("schema",), "v2"))
    expect_rejected("date", "DATE", replace(("date",), "2026-07-17"))
    expect_rejected("cert malformed", "MALFORMED_SHA",
                    replace(("certificate_sha256",), "0"))
    expect_rejected("verifier malformed", "MALFORMED_SHA",
                    replace(("verifier_sha256",), "g" * 64))
    expect_rejected("report malformed", "MALFORMED_SHA",
                    replace(("report_sha256",), ""))
    expect_rejected("cert pin", "CERTIFICATE_PIN",
                    replace(("certificate_sha256",), "0" * 64))
    expect_rejected("dependencies type", "FIELD_TYPE",
                    replace(("dependencies",), []))
    dependency_name = next(iter(EXPECTED_DEPENDENCIES))
    expect_rejected("dependency hash", "DEPENDENCY_MAP",
                    replace(("dependencies", dependency_name), "0" * 64))
    expect_rejected("result type", "FIELD_TYPE", replace(("result",), []))
    expect_rejected("verdict", "VERDICT", replace(("verdict",), "CERTIFIED"))

    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("result schema", ("result", "schema"), "v2"),
        ("old artifacts", ("result", "provenance", "old_artifacts_modified"), True),
        ("join policy", ("result", "provenance", "join_policy"), "global"),
        ("all bindings", ("result", "R1_source_component_binding_registry", "all_source_binding_count"), 23),
        ("used bindings", ("result", "R1_source_component_binding_registry", "used_roof_one_source_binding_count"), 17),
        ("binding digest", ("result", "R1_source_component_binding_registry", "used_roof_one_source_binding_rows_sha256"), "0" * 64),
        ("F5 template bound", ("result", "R1_field_template_registry", "F5", "universal_adapted_inverse_strict_upper"), "1"),
        ("F5 area misuse", ("result", "R1_field_template_registry", "F5", "invariant_area_Jacobian_used"), True),
        ("F6 bound", ("result", "R1_field_template_registry", "F6", "canonical_curve_log_variation_strict_upper"), "0"),
        ("atom count", ("result", "R1_inner_field_join_registry", "R1_inner_atom_count"), 4215),
        ("roof histogram", ("result", "R1_inner_field_join_registry", "R1_inner_candidate_local_roof_histogram", "1"), 4215),
        ("source count", ("result", "R1_inner_field_join_registry", "R1_inner_source_core_count"), 24),
        ("destination count", ("result", "R1_inner_field_join_registry", "R1_inner_destination_core_count"), 24),
        ("h table count", ("result", "R1_inner_field_join_registry", "materialized_candidate_local_physical_homogeneity_table_count"), 4215),
        ("slot count", ("result", "R1_inner_field_join_registry", "materialized_candidate_local_F1_to_F6_slot_count"), 25295),
        ("registry F7", ("result", "R1_inner_field_join_registry", "materialized_R1_F7_slot_count"), 1),
        ("packet digest", ("result", "R1_inner_field_join_registry", "R1_candidate_field_packet_rows_sha256"), "0" * 64),
        ("local maturity", ("result", "Gate5_R1_inner_18_field_maturity", "candidate_local_maturity"), "7/18"),
        ("local field count", ("result", "Gate5_R1_inner_18_field_maturity", "candidate_local_field_count_per_R1_inner_atom"), 7),
        ("global before", ("result", "Gate5_R1_inner_18_field_maturity", "global_Gate5_maturity_before_round25_leaf"), "5/18"),
        ("global after", ("result", "Gate5_R1_inner_18_field_maturity", "global_Gate5_maturity_after_round25_leaf"), "6/18"),
        ("global credit", ("result", "Gate5_R1_inner_18_field_maturity", "global_Gate5_field_credit_added"), 2),
        ("maturity F7", ("result", "Gate5_R1_inner_18_field_maturity", "materialized_R1_inner_F7_candidate_local_slot_count"), 4216),
        ("complete block", ("result", "Gate5_R1_inner_18_field_maturity", "complete_18_field_R1_inner_operator_block_count"), 4216),
        ("first missing", ("result", "Gate5_R1_inner_18_field_maturity", "first_missing_field"), "none"),
        ("F7 transfer", ("result", "Gate5_R1_inner_18_field_maturity", "F7_parent_slot_is_R1_restricted_slot"), True),
        ("nonpromotion F7", ("result", "strict_nonpromotion", "parent_F7_slot_survives_unpriced_adaptive_restriction"), True),
        ("nonpromotion F7 count", ("result", "strict_nonpromotion", "materialized_R1_inner_F7_candidate_local_slot_count"), 1),
        ("nonpromotion block", ("result", "strict_nonpromotion", "complete_18_field_R1_inner_operator_block_count"), 1),
        ("full R1", ("result", "strict_nonpromotion", "complete_full_R1_operator"), "CERTIFIED"),
        ("outer cover", ("result", "strict_nonpromotion", "upstream_unresolved_outer_cover_nonempty"), False),
        ("global maturity promotion", ("result", "strict_nonpromotion", "global_Gate5_maturity_before_and_after"), "4/18 -> 6/18"),
        ("Gate5 promotion", ("result", "strict_nonpromotion", "Gate5"), "CERTIFIED"),
        ("CM2 promotion", ("result", "strict_nonpromotion", "CM2"), "GO"),
        ("digest", ("result", "internal_replay_digest"), "0" * 64),
    ]
    packet_indices = (0, 2108, 4215)
    for index in packet_indices:
        base = ("result", "R1_inner_candidate_field_packet_rows", index)
        mutations.extend([
            (f"packet {index} source", base + ("source_core_id",), "core:forged"),
            (f"packet {index} destination", base + ("destination_core_id",), "core:forged"),
            (f"packet {index} roof", base + ("roof",), 2),
            (f"packet {index} F7", base + ("F7_parent_provenance", "R1_atom_F7_slot"), "MATERIALIZED"),
            (f"packet {index} adaptive face", base + ("F7_parent_provenance", "adaptive_atom_has_artificial_dyadic_face"), False),
            (f"packet {index} packet id", base + ("r1_candidate_field_packet_id",), "r1-candidate-field-packet:" + "0" * 64),
            (f"packet {index} F5", base + ("candidate_local_slots", CANDIDATE_LOCAL_FIELDS[4], "payload", "adapted_inverse_strict_upper"), "1"),
            (f"packet {index} F6", base + ("candidate_local_slots", CANDIDATE_LOCAL_FIELDS[5], "payload", "canonical_log_variation_strict_upper"), "0"),
        ])
    for name, path, value in mutations:
        expect_rejected(name, "RESULT_MISMATCH", replace(path, value))

    try:
        parse_json_text('{"schema":"x","schema":"y"}')
    except VerificationError as exc:
        require(exc.code == "DUPLICATE_JSON_KEY", "SELF_TEST_WRONG_CODE")
        passed += 1
    else:
        raise VerificationError("SELF_TEST_ACCEPTED", "duplicate JSON")
    for token in ("NaN", "Infinity", "-Infinity"):
        try:
            parse_json_text('{"x":' + token + '}')
        except VerificationError as exc:
            require(exc.code == "NONFINITE_JSON", "SELF_TEST_WRONG_CODE", token)
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", token)

    print(f"SELF-TEST PASS: {passed}/{passed} hostile mutations rejected")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not (args.integrity_only or args.replay or args.self_test):
        print(
            "LIVE VERDICT: candidate/local 6/18 only; F7=0; complete block=0; "
            "global Gate 5 remains 4/18 and NOT_CERTIFIED (fail-closed)"
        )
        return 2
    try:
        manifest, expected, expected_sha256 = load_and_validate()
        if args.self_test:
            run_self_test(manifest, expected, expected_sha256)
        elif args.replay:
            print(
                "REPLAY PASS: 4216 upstream R1-inner atoms; 25296 candidate-local "
                "F1-F6 slots; F7=0; complete blocks=0; Gate5=4/18 unchanged"
            )
        else:
            print(
                "INTEGRITY PASS: certificate, dependencies, report, verifier, manifest"
            )
        return 0
    except VerificationError as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
