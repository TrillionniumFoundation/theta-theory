#!/usr/bin/env python3
"""Independent source-direct verifier for the C19C endpoint-bit blocker."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_c19c_endpoint_ownership_v2"
LEDGER = PREFIX + "_unrecoverable_rows.jsonl.gz"
RESULT = PREFIX + "_blocker_result.json"
C19 = "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz"
C5 = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
R174_ROWS = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R174_CERT = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json"
R174_PRODUCER = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
R174_VERIFIER = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py"
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_PRODUCER = "cm2_round179_source_g_residual_tube_arrangement.py"
R234_CERT = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R234_PRODUCER = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization.py"
R235_CERT = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_transition_ready_handle_ledger.jsonl.gz"
PINS = {
    C19: "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    C5: "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",
    R174_ROWS: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R174_CERT: "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
    R174_PRODUCER: "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R174_VERIFIER: "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    R179_ROWS: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R179_PRODUCER: "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R234_CERT: "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    R234_PRODUCER: "4bc6867e660cfe1ec936f03fd5543a12a8d69d3dab480366e4a9c3fbd3768d89",
    R235_CERT: "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "498088be8302efdf0ed95fb5eca6847fa5d7d3b004af45b9efdf77deaaf80575",
}
BITS = [
    "t_lower_closed", "t_upper_closed", "p_lower_closed",
    "p_upper_closed", "s_lower_closed", "s_upper_closed",
]


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        for line in handle:
            need(line.endswith(b"\n"), "row newline:" + path.name)
            raw = line[:-1]
            value = json.loads(raw)
            need(canonical(value) == raw, "row canonical:" + path.name)
            body = dict(value)
            need(body.pop("row_sha256", None) == objsha(body), "row closure:" + path.name)
            yield value


def unpack(document: dict[str, Any], name: str) -> Iterable[dict[str, Any]]:
    result = document["result"]
    columns = result["row_column_schemas"][name]
    for packed in result[name]:
        yield dict(zip(columns, packed, strict=True))


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def cut(values: list[str], axis: str, child: int) -> list[str]:
    box = list(map(Q, values))
    offset = 2 * {"t": 0, "p": 1, "s": 2}[axis]
    middle = (box[offset] + box[offset + 1]) / 2
    box[offset + 1 if child == 0 else offset] = middle
    return [qstr(value) for value in box]


def replay(values: list[str], path: Iterable[str | int], forced_t: bool = False) -> list[str]:
    current = values
    for token in path:
        if forced_t:
            need(type(token) is int and token in {0, 1}, "binary path")
            current = cut(current, "t", token)
        else:
            need(type(token) is str and len(token) == 2 and token[0] in "tps" and token[1] in "01", "adaptive path")
            current = cut(current, token[0], int(token[1]))
    return current


def verify(candidate_dir: Path) -> dict[str, Any]:
    for name, expected in PINS.items():
        need(filesha(HERE / name) == expected, "source pin:" + name)

    raw_result = (candidate_dir / RESULT).read_bytes()
    result = json.loads(raw_result)
    need(canonical(result) == raw_result, "result canonical")
    body = dict(result)
    claimed = body.pop("result_sha256")
    need(claimed == objsha(body), "result closure")
    need(type(result["execution_seed"]) is int and result["execution_seed"] > 0, "real seed")
    need(result["input_pins"] == {name: PINS[name] for name in sorted(PINS)}, "pins")
    need(
        result["status"] == "BLOCKED_ENDPOINT_OWNERSHIP_BITS_NOT_RECOVERABLE_FROM_PINNED_PRIMITIVES"
        and result["census"] == {
            "C19C_half_open_rational_box_rows": 33_344,
            "requested_endpoint_ownership_bits_per_row": 6,
            "requested_endpoint_ownership_bit_slots": 200_064,
            "materialized_endpoint_ownership_bit_slots": 0,
            "rows_with_a_constructive_final_t_split_nonidentifiability_witness": 33_344,
            "fully_recoverable_six_bit_vectors": 0,
        },
        "result census",
    )
    ledger_path = candidate_dir / LEDGER
    need(
        result["ledger"]["filename"] == LEDGER
        and result["ledger"]["row_count"] == 33_344
        and result["ledger"]["sha256"] == filesha(ledger_path)
        and result["ledger"]["size"] == ledger_path.stat().st_size,
        "ledger descriptor",
    )

    candidate_rows = list(rows(ledger_path))
    need(len(candidate_rows) == 33_344, "candidate row census")
    need(result["ledger"]["row_sequence_sha256"] == objsha([row["row_sha256"] for row in candidate_rows]), "row sequence")
    by_mid = {row["member_id"]: row for row in candidate_rows}
    need(len(by_mid) == 33_344, "candidate member uniqueness")

    c19: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(rows(HERE / C19)):
        need(row["ordinal"] == ordinal, "C19 order")
        mid = row["member_id"]
        ast = row["support_ast"]
        need(ast["kind"] == "HALF_OPEN_RATIONAL_BOX" and ast["lineage"] == "R234_DEPTH6_FRONTIER", "C19 kind")
        need(set(BITS).isdisjoint(ast), "C19 bits absent")
        c19[mid] = row
    need(set(c19) == set(by_mid), "candidate/C19 member set")

    c5: dict[str, dict[str, Any]] = {}
    for row in rows(HERE / C5):
        semantic = row["semantic_classification"]
        mid = semantic.get("surviving_side_member")
        if mid in by_mid:
            domain = semantic["complete_parameter_domain"]
            need(set(domain) == {"box", "coordinate_parameter", "half_open_owner_lineage"}, "C5 domain key set")
            need(semantic["classification"] == "EMPTY_GRAPH", "C5 empty")
            c5[mid] = row
    need(set(c5) == set(by_mid), "C5 join")

    r234_rows = load(HERE / R234_CERT)["result"]["depth6_frontier_rows"]
    r234 = {row["frontier_row_id"]: (ordinal, row) for ordinal, row in enumerate(r234_rows)}
    r235_rows = load(HERE / R235_CERT)["result"]["single_endpoint_graph_partition_rows"]
    r235 = {row["endpoint_graph_partition_row_id"]: (ordinal, row) for ordinal, row in enumerate(r235_rows)}
    need(len(r234) == 38_376 and len(r235) == 38_328, "frontier/partition census")

    needed_front_ids = {
        c5[mid]["canonical_input_commitment"]["R234_frontier_row"][1]
        for mid in by_mid
    }
    needed_retained = {
        row["Round179_retained_child_row_id"] for _ordinal, row in r234.values()
        if row["frontier_row_id"] in needed_front_ids
    }
    needed_origins = {
        row["origin_row_id"] for _ordinal, row in r234.values()
        if row["frontier_row_id"] in needed_front_ids
    }
    r179_doc = load(HERE / R179_ROWS)
    need(set(BITS).isdisjoint(r179_doc["result"]["row_column_schemas"]["retained_3d_child_rows"]), "R179 bits absent")
    retained = {row["row_id"]: row for row in unpack(r179_doc, "retained_3d_child_rows") if row["row_id"] in needed_retained}
    r174_doc = load(HERE / R174_ROWS)
    need(set(BITS).isdisjoint(r174_doc["result"]["row_column_schemas"]["residual_3d_tube_rows"]), "R174 bits absent")
    origins = {row["row_id"]: row for row in unpack(r174_doc, "residual_3d_tube_rows") if row["row_id"] in needed_origins}
    need(set(retained) == needed_retained and set(origins) == needed_origins, "R179/R174 joins")
    need(load(HERE / R174_CERT)["result"]["adaptive_recut_contract"]["source_chart_diagonal_half_open_rule"] == "E or W owns; N or S excludes", "chart-only half-open rule")

    c15: dict[str, dict[str, Any]] = {}
    for row in rows(HERE / C15):
        if row["registry_member_id"] in by_mid:
            c15[row["registry_member_id"]] = row
    c25: dict[str, dict[str, Any]] = {}
    for row in rows(HERE / C25):
        if row["member_id"] in by_mid:
            c25[row["member_id"]] = row
    c26: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows(HERE / C26):
        if row["owner_member_id"] in by_mid:
            c26[(row["owner_member_id"], row["representation_id"])] = row
    need(set(c15) == set(c25) == set(by_mid), "C15/C25 joins")

    for ordinal, mid in enumerate(sorted(by_mid, key=lambda value: value.encode())):
        row = by_mid[mid]
        source19, source5 = c19[mid], c5[mid]
        need(row["ordinal"] == ordinal, "ledger order")
        fref = source5["canonical_input_commitment"]["R234_frontier_row"]
        pref = source5["canonical_input_commitment"]["R235_partition_row"]
        need(len(fref) == len(pref) == 3, "ref tuple")
        ford, front = r234[fref[1]]
        pord, part = r235[pref[1]]
        need(fref == [ford, front["frontier_row_id"], objsha(front)], "R234 commitment")
        need(pref == [pord, part["endpoint_graph_partition_row_id"], objsha(part)], "R235 commitment")
        need(part["Round234_frontier_row_id"] == front["frontier_row_id"], "R235/R234 join")
        rr = retained[front["Round179_retained_child_row_id"]]
        oo = origins[front["origin_row_id"]]
        need(rr["refinement_path"][:-1] == oo["refinement_path"] and replay(oo["box"], [rr["refinement_path"][-1]]) == rr["box"], "R179 replay")
        need(replay(rr["box"], front["binary_t_path"], True) == front["box"] == source19["support_ast"]["bounds"], "R234 replay")
        parent = replay(rr["box"], front["binary_t_path"][:-1], True)
        midpoint = qstr((Q(parent[0]) + Q(parent[1])) / 2)
        child = front["binary_t_path"][-1]
        ambiguous = "t_upper_closed" if child == 0 else "t_lower_closed"
        key26 = (mid, source19["representation_id"])
        need(key26 in c26, "C26 handle")

        expected = {
            "schema": "cm2.c19c-endpoint-ownership-v2.unrecoverable-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "C19C_row_sha256": source19["row_sha256"],
            "C5_row_sha256": source5["row_sha256"],
            "C15_member_row_sha256": c15[mid]["row_sha256"],
            "C25_member_row_sha256": c25[mid]["row_sha256"],
            "C26_primary_handle_row_sha256": c26[key26]["row_sha256"],
            "R174_origin_row_id": oo["row_id"],
            "R179_retained_child_row_id": rr["row_id"],
            "R234_frontier_row_ref": fref,
            "R235_partition_row_ref": pref,
            "bounds": front["box"],
            "lineage_replay": {
                "R174_refinement_path": oo["refinement_path"],
                "R179_refinement_path": rr["refinement_path"],
                "R234_binary_t_path": front["binary_t_path"],
                "exact_bounds_reconstructed": True,
            },
            "endpoint_ownership_audit": {
                "requested_bit_names": BITS,
                "materialized_requested_bit_count": 0,
                "unmaterialized_requested_bit_count": 6,
                "six_bit_vector_status": "UNRECOVERABLE_FROM_PINNED_PROVENANCE",
            },
            "minimal_countermodel": {
                "final_R234_t_split_midpoint": midpoint,
                "selected_child": child,
                "ambiguous_bit": ambiguous,
                "LEFT_CHILD_OWNS_INTERNAL_FACE": child == 0,
                "RIGHT_CHILD_OWNS_INTERNAL_FACE": child != 0,
                "both_models_preserve_all_serialized_rows_and_exact_volumes": True,
            },
            "formal_credit": 0,
        }
        candidate_body = dict(row)
        candidate_body.pop("row_sha256")
        need(candidate_body == expected, "exact candidate row:" + str(ordinal))

    need(result["blocker"] == {
        "minimal_missing_commitment": "DYADIC_RECTANGULAR_FACE_OWNER_OR_EXPLICIT_SIX_ENDPOINT_INCLUSION_BITS",
        "exact_bounds_and_all_R174_R179_R234_paths_reconstruct": True,
        "C5_canonical_commitments_to_R234_and_R235_close": True,
        "R174_declared_half_open_rule_scope": "SOURCE_CHART_DIAGONAL_ONLY",
        "R179_and_R234_dyadic_split_face_owner_rule_materialized": False,
        "C15_C25_C26_additional_endpoint_bits_materialized": False,
        "two_distinct_internal_face_owner_models_preserve_every_pinned_serialized_field": True,
        "therefore_full_C19C_half_open_set_equality_is_not_derivable": True,
    }, "blocker statement")
    need(result["strict_nonpromotion"]["formal_credit"] == 0 and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM", "nonpromotion")
    return {
        "schema": "cm2.c19c-endpoint-ownership-v2.blocker-verification.v1",
        "status": "PASS_INDEPENDENT_BLOCKER_RECONSTRUCTION",
        "candidate_result_sha256": claimed,
        "verified_rows": 33_344,
        "verified_requested_bit_slots": 200_064,
        "verified_constructive_nonidentifiability_rows": 33_344,
        "formal_credit": 0,
    }


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python flags")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    value = verify(Path(args.candidate_dir).resolve())
    body = {**value, "result_sha256": objsha(value)}
    raw = canonical(body)
    if args.output:
        Path(args.output).resolve().write_bytes(raw)
    print(raw.decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
