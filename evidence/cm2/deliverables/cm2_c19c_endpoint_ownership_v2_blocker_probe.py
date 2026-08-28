#!/usr/bin/env python3
"""Audit whether C19C's six endpoint-inclusion bits are recoverable.

This is deliberately a zero-credit, fail-closed probe.  It consumes the
primitive C19C/C5/R234/R179/R174 lineage plus the C15/C25/C26 bindings.  It
does not read C27 FAMILIES or any historical transition-edge ledger.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
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
    "t_lower_closed", "t_upper_closed",
    "p_lower_closed", "p_upper_closed",
    "s_lower_closed", "s_upper_closed",
]


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json(path: Path) -> Any:
    raw = path.read_bytes()
    value = json.loads(raw)
    # Historical pinned JSON packages use both canonical one-line and pretty
    # printed encodings.  The byte pin above is the immutable serialization
    # authority; semantic canonicalization is used for committed row refs.
    return value


def closed_rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        for line in handle:
            need(line.endswith(b"\n"), "unterminated row:" + path.name)
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "noncanonical row:" + path.name)
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == objsha(body), "row closure:" + path.name)
            yield row


def table(document: dict[str, Any], name: str) -> list[dict[str, Any]]:
    result = document["result"]
    columns = result["row_column_schemas"][name]
    return [dict(zip(columns, packed, strict=True)) for packed in result[name]]


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def split_box(values: list[str], axis: str, child: int) -> list[str]:
    box = list(map(Q, values))
    index = {"t": 0, "p": 1, "s": 2}[axis]
    lo, hi = 2 * index, 2 * index + 1
    middle = (box[lo] + box[hi]) / 2
    if child == 0:
        box[hi] = middle
    else:
        box[lo] = middle
    return [qstr(value) for value in box]


def replay(values: list[str], tokens: Iterable[str | int], forced_axis: str | None = None) -> list[str]:
    current = values
    for token in tokens:
        if forced_axis is None:
            need(type(token) is str and len(token) == 2, "split token")
            axis, child_text = token[0], token[1]
            need(axis in "tps" and child_text in "01", "split token value")
            child = int(child_text)
        else:
            need(type(token) is int and token in {0, 1}, "binary t token")
            axis, child = forced_axis, token
        current = split_box(current, axis, child)
    return current


def row_ref(row: dict[str, Any], key: str) -> str:
    need(type(row.get(key)) is str, "row ref key")
    return row[key]


def build(candidate_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "real positive seed")
    for name, expected in PINS.items():
        need(filesha(HERE / name) == expected, "input pin:" + name)

    c19_rows = list(closed_rows(HERE / C19))
    need(len(c19_rows) == 33_344, "C19C census")
    targets: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(c19_rows):
        need(row["ordinal"] == ordinal, "C19C order")
        ast = row["support_ast"]
        need(
            ast == {
                "kind": "HALF_OPEN_RATIONAL_BOX",
                "coordinates": ["t", "p", "s"],
                "bounds": ast["bounds"],
                "exact_volume": ast["exact_volume"],
                "lineage": "R234_DEPTH6_FRONTIER",
            }
            and len(ast["bounds"]) == 6
            and all(bit not in ast for bit in BITS),
            "C19C endpoint fields absent",
        )
        mid = row["member_id"]
        need(mid not in targets, "C19C member uniqueness")
        targets[mid] = row

    c5: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C5):
        semantic = row["semantic_classification"]
        mid = semantic.get("surviving_side_member")
        if mid not in targets:
            continue
        domain = semantic["complete_parameter_domain"]
        need(
            semantic["classification"] == "EMPTY_GRAPH"
            and domain == {
                "box": domain["box"],
                "coordinate_parameter": "TPS",
                "half_open_owner_lineage": "R234_DEPTH6_FRONTIER",
            },
            "C5 domain has bounds and lineage only",
        )
        need(mid not in c5, "C5 uniqueness")
        c5[mid] = row
    need(set(c5) == set(targets), "C19C/C5 exact join")

    r234_doc = strict_json(HERE / R234_CERT)
    r234_rows = r234_doc["result"]["depth6_frontier_rows"]
    r234_index = {row["frontier_row_id"]: (i, row) for i, row in enumerate(r234_rows)}
    need(len(r234_index) == len(r234_rows) == 38_376, "R234 frontier uniqueness")

    r235_doc = strict_json(HERE / R235_CERT)
    r235_rows = r235_doc["result"]["single_endpoint_graph_partition_rows"]
    r235_index = {row["endpoint_graph_partition_row_id"]: (i, row) for i, row in enumerate(r235_rows)}
    need(len(r235_index) == len(r235_rows) == 38_328, "R235 partition uniqueness")

    needed_retained: set[str] = set()
    needed_origins: set[str] = set()
    frontier_by_mid: dict[str, dict[str, Any]] = {}
    for mid, source in c5.items():
        commitment = source["canonical_input_commitment"]
        front_ref = commitment["R234_frontier_row"]
        part_ref = commitment["R235_partition_row"]
        need(len(front_ref) == len(part_ref) == 3, "commitment tuple shape")
        front_ordinal, front_id, front_sha = front_ref
        part_ordinal, part_id, part_sha = part_ref
        need(front_id in r234_index and part_id in r235_index, "commitment ids")
        got_front_ordinal, front = r234_index[front_id]
        got_part_ordinal, part = r235_index[part_id]
        need(
            front_ordinal == got_front_ordinal
            and front_sha == objsha(front)
            and part_ordinal == got_part_ordinal
            and part_sha == objsha(part)
            and source["graph_id"] == part_id
            and part["Round234_frontier_row_id"] == front_id,
            "C5 canonical commitment closure",
        )
        need(
            source["semantic_classification"]["complete_parameter_domain"]["box"] == front["box"]
            and targets[mid]["support_ast"]["bounds"] == front["box"],
            "C19C/C5/R234 exact bounds",
        )
        frontier_by_mid[mid] = front
        needed_retained.add(front["Round179_retained_child_row_id"])
        needed_origins.add(front["origin_row_id"])

    r179_doc = strict_json(HERE / R179_ROWS)
    r179_schema = r179_doc["result"]["row_column_schemas"]["retained_3d_child_rows"]
    forbidden = set(BITS) | {"endpoint_ownership", "endpoint_inclusion_bits"}
    need(forbidden.isdisjoint(r179_schema), "R179 schema has no endpoint bits")
    retained = {
        row["row_id"]: row for row in table(r179_doc, "retained_3d_child_rows")
        if row["row_id"] in needed_retained
    }
    need(set(retained) == needed_retained, "R179 retained exact join")

    r174_doc = strict_json(HERE / R174_ROWS)
    r174_schema = r174_doc["result"]["row_column_schemas"]["residual_3d_tube_rows"]
    need(forbidden.isdisjoint(r174_schema), "R174 schema has no endpoint bits")
    origins = {
        row["row_id"]: row for row in table(r174_doc, "residual_3d_tube_rows")
        if row["row_id"] in needed_origins
    }
    need(set(origins) == needed_origins, "R174 origin exact join")
    r174_cert = strict_json(HERE / R174_CERT)["result"]
    need(
        r174_cert["adaptive_recut_contract"]["source_chart_diagonal_half_open_rule"]
        == "E or W owns; N or S excludes",
        "only declared R174 half-open rule is chart seam ownership",
    )

    c15: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C15):
        mid = row["registry_member_id"]
        if mid in targets:
            need(mid not in c15, "C15 uniqueness")
            c15[mid] = row
    need(set(c15) == set(targets), "C15 join")

    c25: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C25):
        mid = row["member_id"]
        if mid in targets:
            need(mid not in c25, "C25 uniqueness")
            c25[mid] = row
    need(set(c25) == set(targets), "C25 join")

    c26: dict[tuple[str, str], dict[str, Any]] = {}
    for row in closed_rows(HERE / C26):
        mid = row["owner_member_id"]
        if mid in targets:
            key = (mid, row["representation_id"])
            need(key not in c26, "C26 handle uniqueness")
            c26[key] = row

    output_rows: list[dict[str, Any]] = []
    for ordinal, mid in enumerate(sorted(targets, key=lambda value: value.encode())):
        c19 = targets[mid]
        source = c5[mid]
        front = frontier_by_mid[mid]
        retained_row = retained[front["Round179_retained_child_row_id"]]
        origin = origins[front["origin_row_id"]]
        part_ref = source["canonical_input_commitment"]["R235_partition_row"]
        front_ref = source["canonical_input_commitment"]["R234_frontier_row"]

        need(
            retained_row["origin_row_id"] == origin["row_id"] == front["origin_row_id"]
            and retained_row["parent_id"] == origin["parent_id"] == front["parent_id"]
            and retained_row["chart"] == origin["chart"] == front["chart"],
            "R174/R179/R234 lineage ids",
        )
        path174 = origin["refinement_path"]
        path179 = retained_row["refinement_path"]
        need(len(path174) == 6 and path179[:-1] == path174 and len(path179) == 7, "R174/R179 paths")
        need(replay(origin["box"], [path179[-1]]) == retained_row["box"], "R179 exact split replay")
        binary_path = front["binary_t_path"]
        need(len(binary_path) == 6, "R234 depth-six path")
        need(replay(retained_row["box"], binary_path, "t") == front["box"], "R234 exact split replay")

        key26 = (mid, c19["representation_id"])
        need(key26 in c26, "C26 primary representation handle")
        need(
            c15[mid]["fresh_component_id"] == c19["fresh_component_id"]
            and c25[mid]["normalized_support_ast_sha256"] == c19["support_ast_sha256"]
            and c25[mid]["source_bindings"]["support_kernel"] == "C19C"
            and c25[mid]["source_bindings"]["support_kernel_row_sha256"] == c19["row_sha256"]
            and c26[key26]["owner_normalized_support_ast_sha256"] == c19["support_ast_sha256"],
            "C15/C25/C26 hash-only propagation",
        )

        parent_before_last = replay(retained_row["box"], binary_path[:-1], "t")
        midpoint = qstr((Q(parent_before_last[0]) + Q(parent_before_last[1])) / 2)
        child = binary_path[-1]
        ambiguous_bit = "t_upper_closed" if child == 0 else "t_lower_closed"
        left_owns = True if child == 0 else False
        right_owns = not left_owns
        body = {
            "schema": "cm2.c19c-endpoint-ownership-v2.unrecoverable-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "C19C_row_sha256": c19["row_sha256"],
            "C5_row_sha256": source["row_sha256"],
            "C15_member_row_sha256": c15[mid]["row_sha256"],
            "C25_member_row_sha256": c25[mid]["row_sha256"],
            "C26_primary_handle_row_sha256": c26[key26]["row_sha256"],
            "R174_origin_row_id": origin["row_id"],
            "R179_retained_child_row_id": retained_row["row_id"],
            "R234_frontier_row_ref": front_ref,
            "R235_partition_row_ref": part_ref,
            "bounds": front["box"],
            "lineage_replay": {
                "R174_refinement_path": path174,
                "R179_refinement_path": path179,
                "R234_binary_t_path": binary_path,
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
                "ambiguous_bit": ambiguous_bit,
                "LEFT_CHILD_OWNS_INTERNAL_FACE": left_owns,
                "RIGHT_CHILD_OWNS_INTERNAL_FACE": right_owns,
                "both_models_preserve_all_serialized_rows_and_exact_volumes": True,
            },
            "formal_credit": 0,
        }
        output_rows.append({**body, "row_sha256": objsha(body)})

    need(len(output_rows) == 33_344, "output census")
    raw_rows = b"".join(canonical(row) + b"\n" for row in output_rows)
    candidate_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = candidate_dir / LEDGER
    with ledger_path.open("wb") as raw_handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_handle, mtime=0) as handle:
            handle.write(raw_rows)

    row_sequence_sha = objsha([row["row_sha256"] for row in output_rows])
    semantic = {
        "schema": "cm2.c19c-endpoint-ownership-v2.blocker-result.v1",
        "status": "BLOCKED_ENDPOINT_OWNERSHIP_BITS_NOT_RECOVERABLE_FROM_PINNED_PRIMITIVES",
        "execution_seed": seed,
        "input_pins": {name: PINS[name] for name in sorted(PINS)},
        "census": {
            "C19C_half_open_rational_box_rows": 33_344,
            "requested_endpoint_ownership_bits_per_row": 6,
            "requested_endpoint_ownership_bit_slots": 200_064,
            "materialized_endpoint_ownership_bit_slots": 0,
            "rows_with_a_constructive_final_t_split_nonidentifiability_witness": 33_344,
            "fully_recoverable_six_bit_vectors": 0,
        },
        "ledger": {
            "filename": LEDGER,
            "row_count": 33_344,
            "sha256": filesha(ledger_path),
            "size": ledger_path.stat().st_size,
            "row_sequence_sha256": row_sequence_sha,
        },
        "blocker": {
            "minimal_missing_commitment": "DYADIC_RECTANGULAR_FACE_OWNER_OR_EXPLICIT_SIX_ENDPOINT_INCLUSION_BITS",
            "exact_bounds_and_all_R174_R179_R234_paths_reconstruct": True,
            "C5_canonical_commitments_to_R234_and_R235_close": True,
            "R174_declared_half_open_rule_scope": "SOURCE_CHART_DIAGONAL_ONLY",
            "R179_and_R234_dyadic_split_face_owner_rule_materialized": False,
            "C15_C25_C26_additional_endpoint_bits_materialized": False,
            "two_distinct_internal_face_owner_models_preserve_every_pinned_serialized_field": True,
            "therefore_full_C19C_half_open_set_equality_is_not_derivable": True,
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "SAME_CHART_RELATIVE_CELLS_totality": False,
            "twenty_family_gate": "OPEN",
            "C27": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED",
            "C28": "REJECT",
            "C29": "REJECT",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "MINT_AN_APPEND_ONLY_UPSTREAM_ENDPOINT_OWNER_LEDGER_AND_REPLAY_C19C_C25_C26_BEFORE_ANY_TOTALITY_CREDIT",
    }
    result = {**semantic, "result_sha256": objsha(semantic)}
    (candidate_dir / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve(), args.seed)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
