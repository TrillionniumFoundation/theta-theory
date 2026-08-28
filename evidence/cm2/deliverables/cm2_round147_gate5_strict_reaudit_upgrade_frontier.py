#!/usr/bin/env python3
"""Round147: fail-closed Gate5 18-field strict re-audit.

This producer deliberately separates three notions that older local artifacts
can otherwise blur:

* global Gate5 field credit;
* prospective/local-v1 evidence on an exact fibre; and
* versioned Round137-v1 identifier migration.

The output is an audit/frontier certificate.  It mints no historical or v1
component, parent-W, restriction, owner, t54, Omega_j, or q_j identifier.
Round145 and Round146 are excluded from the sealed search snapshot and appear
only as null future input slots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
SCHEMA = "cm2.round147.gate5-strict-reaudit-upgrade-frontier.v1"
DATE = "2026-07-24"
DEFAULT_OUTPUT = (
    BASE / "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json"
)

PINS: dict[str, str] = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json":
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json":
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json":
        "fa35f45bd9d31976b62d7dfd988b774ec5404a5bd3755994e627711857710cfd",
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json":
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    "cm2-round70-selected-nonempty-face-incidence-all-gate-manifest-2026-07-21.json":
        "057f60f2583134b765cec47756f766a591497e1898cbec9b89afd7febbfe99ad",
    "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json":
        "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json":
        "5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5",
    "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json":
        "a8e4b9dabb30396469f28d4df252c9f5de1d9d1620c0a18d252ef23a12f1f3d6",
    "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json":
        "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
    "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json":
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py":
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json":
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py":
        "cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json":
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    "cm2_round140_fixed_s_adaptive_component_identity_bridge.py":
        "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json":
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    "cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py":
        "4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json":
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    "cm2_round140_round35_parent_w_r1648_materialization_audit.py":
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json":
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py":
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json":
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    "cm2_round141_recentered_affine_k4296_d0_collar_return.py":
        "687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28",
    "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json":
        "a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe",
    "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py":
        "1bb85fdd8dc22aa941084666b5eb9c41154f9e890f6d87c42eaf8808a4748f65",
    "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json":
        "43770a85918cd4986e232cc1e3c401bae9ff8d0ee772b92eea8c46c3c55d4e3c",
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier.py":
        "97477687d0013f5a8b426250b930e845858c624685c1f45f6528c336963b7d4c",
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json":
        "816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0",
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier_verifier.py":
        "ef2d2297aec42ef39a2b0ca352f05659a2fbb72435283333713f393193dbbad5",
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-verification-2026-07-24.json":
        "3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170",
    "cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py":
        "bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38",
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json":
        "74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67",
    "cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py":
        "197be350c4a6bed80a1c413822c5b838c2d0bc7da88360998fd7ad939da85601",
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-verification-2026-07-24.json":
        "3ee6fe0e48bdf05a6f76726ded302aa4d632c306a4a260f444e1c2a66dfd9bd7",
    "cm2_round144_round137_v1_superseding_migration_schema.py":
        "3665730d98b23ea952d352910a2dd0a5410d6697d14604a087cf0cd12caea80b",
    "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json":
        "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    "cm2_round144_round137_v1_superseding_migration_schema_verifier.py":
        "413c85a68d2a6623b1250cfbbc502ea13a2036f084ac483c96eb044a16db9265",
    "cm2-round144-round137-v1-superseding-migration-schema-verification-2026-07-24.json":
        "dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5",
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
OPEN_FIELDS = {
    5: "no global inverse-Jacobian row on the full return-word registry",
    6: "no all-record global log-Jacobian distortion sum",
    10: "no all-face owner-root coarea row with actual marks and tails",
    11: "no branch-uniform physical dynamic-test pullback",
    14: "global F10 and a bounded recovered strong block are absent",
    15: "raw-Z, power-Orlicz, recovery, and cemetery sectors are not jointly paid",
    17: "no physical oriented carrier/all-input current",
    18: "F1--F17 do not coexist on one global block",
}
SATISFIED_FIELDS = sorted(set(FIELD_NAMES) - set(OPEN_FIELDS))

MINIMUM_CLOSERS = {
    5: "materialize and verify an inverse-Jacobian bound for every row of a complete global block registry",
    6: "prove and serialize the finite all-record distortion sum on that same registry",
    10: "materialize complete active owner/root fibres and all physical-face coarea density rows",
    11: "prove one physical branch-uniform pullback bound over the complete registry",
    14: "close global F10, then certify the recovered regular-density strong block and its cost",
    15: "certify finite raw-Z/power-Orlicz/recovery/cemetery debt on the same owner law",
    17: "join the oriented physical carrier, all-input current, and dynamic-test operator on identical keys",
    18: "serialize one immutable global key carrying verified F1--F17 plus the phase block",
}

TOKEN_PATTERNS = {
    "historical_parent_W_shaped": re.compile(rb"rn-parent-W:[0-9a-f]{64}"),
    "historical_restriction_shaped": re.compile(rb"rn-restriction:[0-9a-f]{64}"),
    "v1_parent_W_shaped": re.compile(rb"rn-v1-parent-W:[0-9a-f]{64}"),
    "v1_restriction_shaped": re.compile(rb"rn-v1-restriction:[0-9a-f]{64}"),
    "round50_owner_shaped": re.compile(
        rb"(?:round50(?:-v1)?-owner|round50-owner-key):[0-9a-f]{64}"
    ),
    "round54_t54_shaped": re.compile(rb"round54(?:-v1)?-t54:[0-9a-f]{64}"),
    "round67_qj_shaped": re.compile(rb"round67(?:-v1)?-qj:[0-9a-f]{64}"),
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def load_json(name: str) -> dict[str, Any]:
    raw = (BASE / name).read_bytes()
    value = json.loads(raw.decode("utf-8"))
    require(isinstance(value, dict), f"{name}: object")
    return value


def verify_pins() -> None:
    for name, expected in sorted(PINS.items()):
        path = BASE / name
        require(path.is_file(), f"missing pin: {name}")
        require(file_sha256(path) == expected, f"pin mismatch: {name}")


def include_in_sealed_snapshot(path: Path) -> bool:
    name = path.name
    if not path.is_file() or name.startswith("."):
        return False
    if path.suffix.lower() not in {".json", ".py", ".md", ".sha256"}:
        return False
    lower = name.lower()
    if "round147" in lower:
        return False
    match = re.search(r"round(\d+)", lower)
    if match and int(match.group(1)) >= 145:
        return False
    if "one-hundred-forty-" in lower:
        # These prose assault names are ambiguous under concurrent Round145+
        # production.  Their sealed R139--R144 sources/certs/verifications are
        # pinned explicitly above, so excluding the prose family loses no
        # semantic evidence.
        return False
    return True


def sealed_repository_snapshot() -> dict[str, Any]:
    entries: list[list[Any]] = []
    hits: dict[str, dict[str, set[str]]] = {
        key: {} for key in TOKEN_PATTERNS
    }
    total_bytes = 0
    for path in sorted(BASE.iterdir(), key=lambda item: item.name):
        if not include_in_sealed_snapshot(path):
            continue
        raw = path.read_bytes()
        total_bytes += len(raw)
        entries.append([path.name, hashlib.sha256(raw).hexdigest(), len(raw)])
        for label, pattern in TOKEN_PATTERNS.items():
            for match in pattern.finditer(raw):
                token = match.group(0).decode("ascii")
                hits[label].setdefault(token, set()).add(path.name)
    hit_rows = []
    for label in sorted(hits):
        for token in sorted(hits[label]):
            hit_rows.append(
                {
                    "pattern_class": label,
                    "token": token,
                    "source_files": sorted(hits[label][token]),
                }
            )
    return {
        "scope": (
            "top-level .json/.py/.md/.sha256 sealed snapshot through Round144; "
            "Round145+, Round147, dot-temporaries, and ambiguous concurrent "
            "one-hundred-forty-* prose assault files excluded"
        ),
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "path_sha_size_rows_sha256": digest(entries),
        "identifier_pattern_hit_rows": hit_rows,
        "identifier_pattern_hit_rows_sha256": digest(hit_rows),
    }


def field_rows() -> list[dict[str, Any]]:
    rows = []
    for index in range(1, 19):
        globally_open = index in OPEN_FIELDS
        row = {
            "field_index": index,
            "field": f"F{index}",
            "field_name": FIELD_NAMES[index],
            "global_credit_classification": (
                "STRICTLY_BLOCKED" if globally_open else "STRICTLY_SATISFIED"
            ),
            "global_field_credit": not globally_open,
            "best_available_non_global_evidence": (
                "PROSPECTIVE_LOCAL_V1_ONLY__ROUND130_EVERY_EXACT_FIBRE"
                if globally_open
                else "NOT_NEEDED_FOR_EXISTING_GLOBAL_CREDIT"
            ),
            "prospective_evidence_is_Round144_identifier_migration": False,
            "minimum_evidence": (
                "Round67 frozen global open-eight ledger; F-index is absent "
                "from that open set"
                if not globally_open
                else "Round67 frozen open-eight ledger plus Round130 local "
                "per-exact-fibre 18/18 nonpromotion"
            ),
            "strict_blocker": OPEN_FIELDS.get(index),
            "minimum_closing_evidence": MINIMUM_CLOSERS.get(index),
            "upgrade_credit_now": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def verify_input_semantics(values: dict[str, dict[str, Any]]) -> None:
    g67 = values[
        "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json"
    ]["result"]
    open_rows = g67["remaining_eight_fields"]["rows"]
    require(
        [row["field"] for row in open_rows]
        == [f"F{i}" for i in sorted(OPEN_FIELDS)],
        "Round67 open-eight order",
    )
    require(g67["strict_status"]["Gate5_maturity"] == "10/18", "Round67 maturity")
    require(g67["strict_status"]["complete_18_field_blocks"] == 0, "Round67 blocks")

    r130 = values[
        "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json"
    ]["result"]
    require(
        r130["status"]
        == "CERTIFIED_POSITIVE_BOREL_EVERY_EXACT_FIBRE_LOCAL_18_OF_18__NO_GLOBAL_PROMOTION",
        "Round130 local-only status",
    )
    require(r130["gate5_global_maturity"] == "10/18", "Round130 maturity")
    require(r130["global_complete_18_field_block_count"] == 0, "Round130 blocks")

    r140 = values[
        "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
    ]["result"]
    status = r140["maximal_legal_Round35_field_status"]
    require(status["Round35_source_parent_W_id_materialized"] is False, "R140 W")
    require(status["Round35_rn_restriction_id_materialized"] is False, "R140 restriction")
    require(status["natural_short_cell_k_materialized"] is False, "R140 k")

    r142 = values[
        "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json"
    ]["result"]
    audit = r142["historical_definition_and_crosswalk_audit"]
    require(audit["Round27_component_coordinates_enumerated"] is False, "R142 enum")
    require(audit["absent_executable_field_count"] == 9, "R142 missing enum fields")

    r144 = values[
        "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
    ]["result"]
    require(all(value is None for value in r144["current_identifier_values"].values()), "R144 null IDs")
    require(r144["first_exact_blocker"]["node_id"] == "D02", "R144 first blocker")
    dag = {row["node_id"]: row for row in r144["migration_DAG_rows"]}
    require(dag["D00"]["status"] == "READY" and dag["D01"]["status"] == "READY", "R144 ready")
    require(dag["D05"]["status"] == "AWAITING_FUTURE_CERTIFICATE", "R144 D05")
    require(dag["D08"]["status"] == "AWAITING_FUTURE_CERTIFICATE", "R144 D08")

    r133 = values[
        "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
    ]["result"]
    require(r133["count_ledger"]["owner_key_count"] == 0, "R133 owner")
    require(r133["count_ledger"]["q_j_recordwise_output_count"] == 0, "R133 qj")
    require(
        r133["count_ledger"]["certified_or_materialized_Round67_owned_Omega_j_record_count"]
        == 0,
        "R133 Omega",
    )

    r60 = values[
        "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
    ]["result"]["owner_root_crosswalk_and_coverage_frontier"]
    require(
        r60["Round50_to_Round54_same_ID_crosswalk"]
        == "CERTIFIED_EXACT_BOREL_PROJECTION",
        "Round60 projection",
    )
    require(len(r60["token_rows"]) == 7, "Round60 token schema")

    r131 = values[
        "cm2-round131-round67-r1-typed-incidence-crosswalk-2026-07-24.json"
    ]["result"]
    require(
        r131["source_census"]["Round67_materialized_recordwise_identifier_count"] == 0,
        "R131 recordwise IDs",
    )
    require(
        r131["source_census"]["Round67_materialized_twelve_field_record_count"] == 0,
        "R131 records",
    )

    r128 = values[
        "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
    ]["result"]
    require(
        r128["D_global_safety_and_nonpromotion"]["Round67_owner_to_path_crosswalk_row_count"]
        == 0,
        "R128 owner path",
    )


def historical_census(
    values: dict[str, dict[str, Any]], snapshot: dict[str, Any]
) -> dict[str, Any]:
    r70 = values[
        "cm2-round70-selected-nonempty-face-incidence-all-gate-manifest-2026-07-21.json"
    ]["result"]
    germ = r70["compact_parameterized_face_germ"]
    restriction_payload = {
        "component_id": r70["selected_actual_path_cell"]["component_id"],
        "t_interval": germ["t_interval"],
        "s_interval": germ["s_interval"],
        "physical_word": [
            r70["selected_actual_path_cell"]["source_chart"],
            r70["selected_actual_path_cell"]["target_lift"],
        ],
    }
    local_restriction = "rn-restriction:" + digest(restriction_payload)
    require(local_restriction == germ["restriction_id"], "Round70 local restriction replay")

    shaped = [
        row
        for row in snapshot["identifier_pattern_hit_rows"]
        if row["pattern_class"] == "historical_restriction_shaped"
    ]
    require(len(shaped) == 1, "one shaped restriction")
    require(shaped[0]["token"] == local_restriction, "shaped restriction identity")
    require(
        not [
            row
            for row in snapshot["identifier_pattern_hit_rows"]
            if row["pattern_class"] != "historical_restriction_shaped"
        ],
        "no other shaped identifiers",
    )

    r60 = values[
        "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
    ]["result"]["owner_root_crosswalk_and_coverage_frontier"]
    r67 = values[
        "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
    ]["result"]
    r133 = values[
        "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
    ]["result"]

    return {
        "Round35": {
            "historical_parent_W_materialized_count": 0,
            "historical_schema_compatible_restriction_materialized_count": 0,
            "namespace_shaped_restriction_false_positive_count": 1,
            "false_positive": {
                "identifier": local_restriction,
                "source": (
                    "cm2-round70-selected-nonempty-face-incidence-all-gate-"
                    "manifest-2026-07-21.json"
                ),
                "replayed_payload": restriction_payload,
                "why_not_Round35": (
                    "payload omits historical component ID, source parent-W ID, "
                    "source interval rank, incidence-rank path, short-cell k, and "
                    "image-recut rank; it is a Round70 local germ namespace"
                ),
            },
        },
        "Round50": {
            "recordwise_owner_key_count": r133["count_ledger"]["owner_key_count"],
            "complete_candidate_fibre_count":
                r133["count_ledger"]["Round50_complete_candidate_fibre_count"],
            "active_regular_representation_crosswalk_count":
                r133["count_ledger"][
                    "Round50_active_regular_representation_crosswalk_count"
                ],
            "best_available": "standard-Borel owner rule plus 64 null-owner candidate requests",
            "strict_status": "NO_MATERIALIZED_OWNER",
        },
        "Round54": {
            "token_schema_field_count": len(r60["token_rows"]),
            "pi50_projection_schema_status":
                r60["Round50_to_Round54_same_ID_crosswalk"],
            "pi50_projection": r60["exact_projection"],
            "materialized_owner_t54_token_count": 0,
            "same_root_word_side_crosswalk_count":
                r133["count_ledger"]["Round54_same_root_word_side_crosswalk_count"],
            "strict_status": "SCHEMA_MAP_ONLY__NO_RECORDWISE_TOKEN",
        },
        "Round67": {
            "abstract_Omega_j_formula": r67["actual_fixed_j_subroot"]["root"],
            "abstract_q_j_status": r67["actual_fixed_j_subroot"]["owner_view"],
            "materialized_owned_Omega_j_record_count":
                r133["count_ledger"][
                    "certified_or_materialized_Round67_owned_Omega_j_record_count"
                ],
            "materialized_q_j_output_count":
                r133["count_ledger"]["q_j_recordwise_output_count"],
            "owner_to_path_crosswalk_count": 0,
            "strict_status": "ABSTRACT_FORMULA_ONLY__NO_RECORDWISE_OUTPUT",
        },
    }


def build_result() -> dict[str, Any]:
    verify_pins()
    values = {
        name: load_json(name)
        for name in PINS
        if name.endswith(".json")
    }
    verify_input_semantics(values)
    snapshot = sealed_repository_snapshot()
    rows = field_rows()
    census = historical_census(values, snapshot)

    r144 = values[
        "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
    ]["result"]
    future_slots = [
        {
            "slot": "Round145_leaf_corridor_atlas",
            "source_sha256": None,
            "certificate_sha256": None,
            "verifier_sha256": None,
            "verification_sha256": None,
            "verification_result_sha256": None,
            "admissible_DAG_nodes_after_atomic_acceptance": ["D05", "D06", "D08"],
            "status": "UNBOUND_NULL_FUTURE_INPUT",
        },
        {
            "slot": "Round146_two_generator_outer_atlas",
            "source_sha256": None,
            "certificate_sha256": None,
            "verifier_sha256": None,
            "verification_sha256": None,
            "verification_result_sha256": None,
            "admissible_DAG_nodes_after_atomic_acceptance": ["D02", "D03", "D04"],
            "status": "UNBOUND_NULL_FUTURE_INPUT",
        },
    ]
    for slot in future_slots:
        slot["row_sha256"] = digest(slot)

    result = {
        "status": (
            "CERTIFIED_GATE5_18_FIELD_STRICT_REAUDIT__"
            "10_SATISFIED__8_PROSPECTIVE_LOCAL_ONLY_AND_STRICTLY_BLOCKED__"
            "0_UPGRADES"
        ),
        "audit_date": DATE,
        "provenance": {
            "strict_byte_pins": dict(sorted(PINS.items())),
            "latest_sealed_rounds": [139, 140, 141, 142, 143, 144],
            "round145_or_round146_dependency_bytes_in_certificate": False,
            "sealed_snapshot_excludes_round145_and_round146": True,
            "historical_identity_guessing_used": False,
        },
        "sealed_repository_search_snapshot": snapshot,
        "gate5_field_rows": rows,
        "gate5_field_rows_sha256": digest(rows),
        "gate5_global_ledger": {
            "strictly_satisfied_field_indices": SATISFIED_FIELDS,
            "strictly_blocked_field_indices": sorted(OPEN_FIELDS),
            "prospective_local_v1_only_field_indices": sorted(OPEN_FIELDS),
            "prospective_local_v1_is_not_Round144_identifier_migration": True,
            "newly_promoted_field_indices": [],
            "global_maturity_before": "10/18",
            "global_maturity_after": "10/18",
            "global_complete_18_field_block_count_before": 0,
            "global_complete_18_field_block_count_after": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "historical_identifier_and_map_census": census,
        "Round142_underdetermination_pin": {
            "proof_id": (
                "round142-historical-enumeration-underdetermination:"
                "6d68f69bd4f7774b417bbeb5a7481636f3dc72c780b205deb8f18bce88ef649f"
            ),
            "historical_component_rank_identified": False,
            "historical_component_ID_identified": False,
            "absent_executable_enumeration_field_count": 9,
        },
        "Round144_atomic_migration_frontier": {
            "migration_registry_id": r144["migration_registry_id"],
            "first_exact_blocker": r144["first_exact_blocker"],
            "ready_DAG_nodes": ["D00", "D01"],
            "current_identifier_values": r144["current_identifier_values"],
            "future_input_slots": future_slots,
            "future_input_slots_sha256": digest(future_slots),
            "atomic_acceptance_guards": [
                *r144["future_certificate_acceptance_contract"]["acceptance_guards"],
                "all five hashes in one future slot become non-null in one new superseding certificate",
                "the future verification result is PASS before any DAG node or Gate5 row is re-audited",
                "Round147 remains immutable; accepted future inputs create a new audit generation",
                "a local/prospective field packet never receives global credit without complete registry coverage",
            ],
        },
        "executable_upgrade_frontier": [
            {
                "priority": 1,
                "target": "versioned component/leaf/restriction prerequisites",
                "action": "atomically admit independently verified Round145/146 outputs under the Round144 guards",
                "does_not_by_itself_upgrade_Gate5": True,
            },
            {
                "priority": 2,
                "target": "Round50 owner chain",
                "action": (
                    "complete the 17-field Round133 replacement contract, prove "
                    "same-event fibre completeness and active regular membership, "
                    "then select the least primitive"
                ),
                "does_not_by_itself_upgrade_Gate5": True,
            },
            {
                "priority": 3,
                "target": "Round54/Round67 recordwise chain",
                "action": (
                    "instantiate the certified t50->t54 projection on the same "
                    "owned root, serialize Omega_j and q_j, and join exact path keys"
                ),
                "does_not_by_itself_upgrade_Gate5": True,
            },
            {
                "priority": 4,
                "target": "open Gate5 F5,F6,F10,F11,F14,F15,F17,F18",
                "action": (
                    "satisfy each row's minimum_closing_evidence on one complete "
                    "global immutable block registry, then rerun this 18-row audit"
                ),
                "does_not_by_itself_upgrade_Gate5": False,
            },
        ],
        "strict_nonclaims": [
            "no Round70 local rn-restriction is renamed as a historical Round35 restriction",
            "no historical component, parent-W, source interval, short-cell, image-recut or restriction ID is inferred",
            "Round60 certifies a token projection schema, not an actual owner-bound t54 row",
            "the Round67 Omega_j and q_j formulas are not recordwise materializations",
            "Round130 per-exact-fibre local 18/18 is not global Gate5 credit",
            "Round137-v1 does not reinterpret historical Round27/35/50/54/67 identifiers",
            "Round145 and Round146 are not pinned or partially admitted as certificate dependencies",
            "no Gate5 field, complete block, composite gate, or CM2 theorem is promoted",
        ],
    }
    return result


def envelope(result: dict[str, Any]) -> dict[str, Any]:
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def atomic_write(path: Path, payload: bytes) -> None:
    path = path.resolve()
    require(path.parent == BASE or path.parent == Path(tempfile.gettempdir()).resolve(),
            "output parent")
    require(not path.exists() or path.is_file(), "output target type")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    value = envelope(build_result())
    atomic_write(args.output, canonical_bytes(value) + b"\n")
    print(json.dumps({
        "status": "PASS",
        "output": str(args.output),
        "result_sha256": value["result_sha256"],
        "certificate_sha256": file_sha256(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
