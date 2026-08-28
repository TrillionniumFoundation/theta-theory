#!/usr/bin/env python3
"""Seal the ten C12 rerouted source-shared side incidences and traces."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c12a_source_g_rerouted_shared_side_kernel"
SCHEMA: Final = "cm2.round306c12a.source-g-rerouted-shared-side-kernel.v1"
ROW_SCHEMA: Final = SCHEMA + ".kernel-row.v1"
LEDGER: Final = PREFIX + "_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def row_ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("KERNEL_LIBRARY", "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_producer.py", 69_208, "2af17cb8f626949dc48824ffb53561f61d3de130438c15c5a20faf5619137485"),
    Pin("C12_MANIFEST", "cm2_round306c12_source_g_local_shared_relation_reroute_manifest.sha256", 1_093, "c5fb926229bdc2179b51b0e7a2842c3239936acc1e1cd48e7fcccbe06fa6745a"),
    Pin("C12_RESULT", "cm2_round306c12_source_g_local_shared_relation_reroute_result.json", 3_866, "da77e963ec0a1e2bfef84dd5cf333484e47fd5ffe9ca946c6b77c1a762c10661"),
    Pin("C12_LEDGER", "cm2_round306c12_source_g_local_shared_relation_reroute_ledger.jsonl.gz", 8_566, "37c99c69907d57375d07803d651ac9b878db8bb25c33501b8b7846ccc45bbef5"),
    Pin("C10_SUPPORT", "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz", 19_958_893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C4_LEDGER", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz", 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R236_CERT", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    Pin("R248_CERT", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in PINS}
DOWNSTREAM_ZERO: Final = {
    "graph_sheet_set_equality": 0,
    "representation_pullback": 0,
    "member_normalized_support": 0,
    "global_normalized_support": 0,
    "DSU_edge": 0,
    "DSU_union": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "CM2": 0,
}


def read_pin(pin: Pin) -> bytes:
    path = ROOT / pin.filename
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_size == pin.size, "pin size:" + pin.role)
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin.sha256, "pin sha:" + pin.role)
    return raw


def load_library() -> Any:
    pin = PIN_BY_ROLE["KERNEL_LIBRARY"]
    read_pin(pin)
    spec = importlib.util.spec_from_file_location("c11a_kernel_library", ROOT / pin.filename)
    need(spec is not None and spec.loader is not None, "kernel library spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rows(raw: bytes, label: str) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), f"row closure:{label}:{ordinal}")
            yield row


def closed_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    core = dict(value)
    claimed = core.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "document closure:" + label)
    return value


def legacy_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(value["result_sha256"] == object_sha(value["result"]), "legacy document closure:" + label)
    return value


def gzip_rows(output: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(canonical(row) + b"\n" for row in output)
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=buffer, mtime=0) as stream:
        stream.write(plain)
    return buffer.getvalue(), plain


def build() -> tuple[dict[str, Any], bytes]:
    K = load_library()
    raw = {pin.role: read_pin(pin) for pin in PINS if pin.role != "KERNEL_LIBRARY"}
    c12_result = closed_document(raw["C12_RESULT"], "C12")
    need(c12_result["scoped_credit"] == {"relation_reroute_disposition": 10}, "C12 scope")
    need(all(value == 0 for value in c12_result["formal_credit"].values()), "C12 zero theorem credit")
    c12_rows = list(rows(raw["C12_LEDGER"], "C12"))
    need(len(c12_rows) == 10, "C12 row exhaustion")

    wanted_graphs = {row["positive_source_graph_id"] for row in c12_rows}
    supports = {row["graph_id"]: row for row in rows(raw["C10_SUPPORT"], "C10") if row["graph_id"] in wanted_graphs}
    bridges = {row["bridge_row_id"]: row for row in rows(raw["C4_LEDGER"], "C4")}
    need(len(supports) == len(wanted_graphs) == 10 and len(bridges) == 16, "support/bridge exhaustion")

    r236_doc = legacy_document(raw["R236_CERT"], "R236")
    r236_rows = r236_doc["result"]["double_endpoint_partition_rows"]
    r236_by_id = {row["double_endpoint_partition_row_id"]: (ordinal, row) for ordinal, row in enumerate(r236_rows)}
    r248_doc = legacy_document(raw["R248_CERT"], "R248")
    bulk_rows = r248_doc["result"]["formal_wall_positive_volume_bulk_ledger"]["rows"]
    wanted_sides = {row["side_member_id"] for row in c12_rows}
    bulk_by_id = {row["wall_bulk_node_id"]: row for row in bulk_rows if row["wall_bulk_node_id"] in wanted_sides}
    need(len(bulk_by_id) == 10, "R248 selected bulk exhaustion")

    output: list[dict[str, Any]] = []
    seen_graphs: set[str] = set()
    seen_sides: set[str] = set()
    for reroute in sorted(c12_rows, key=lambda row: row["reroute_ordinal"]):
        graph_id = reroute["positive_source_graph_id"]
        side_id = reroute["side_member_id"]
        need(graph_id not in seen_graphs and side_id not in seen_sides, "subject uniqueness")
        seen_graphs.add(graph_id)
        seen_sides.add(side_id)
        need(reroute["side_role"] == "source:SAME_SIGN_EVENT_ABSENT", "reroute role")
        need(reroute["local_graph_side_physical_incidence_proved"] is False and reroute["one_sided_trace_proved"] is False, "reroute zero theorem boundary")
        need(all(value == 0 for value in reroute["formal_credit"].values()), "reroute downstream zero")

        support = supports[graph_id]
        need(support["graph_class"] == "R235D_SOURCE_EXACT_FACE_FULL_BASE", "R235D support class")
        need(support["sheet_member_id"] == reroute["sheet_member_id"], "sheet binding")
        bridge = bridges[reroute["C4_bridge_ref"]["row_id"]]
        need(reroute["C4_bridge_ref"] == row_ref(bridge, "bridge_row_id"), "C12-C4 binding")
        reconstruction = bridge["semantic_reconstruction"]
        need(reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0", "source zero set")
        need(reconstruction["complete_domain_partition_verified"] is True, "complete source domain")
        need(K.q(reconstruction["source_t_derivative_exact_interval"]["lower"]) == K.q(reconstruction["source_t_derivative_exact_interval"]["upper"]) == K.Q(9, 25), "exact source derivative")
        c10_ref = support["legacy_source_refs"]["C4_exact_source_semantic_authority"]
        need(c10_ref["row_id"] == bridge["bridge_row_id"] and c10_ref["row_sha256"] == bridge["row_sha256"], "C10-C4 authority")

        r236_ref = bridge["canonical_input_commitment"]["R236_double_endpoint_partition_row"]
        need(r236_ref[1] in r236_by_id, "R236 row existence")
        r236_ordinal, r236 = r236_by_id[r236_ref[1]]
        need(r236_ref[0] == r236_ordinal and object_sha(r236) == r236_ref[2], "C4-R236 exact binding")
        need(r236["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "R236 derivative")
        need(reroute["source_incidence_row_commitment"]["row_id"] == bridge["canonical_input_commitment"]["B1G0_source_shared_side_row"][1], "source-shared relation binding")

        eta = K.sign_number(reconstruction["target_factor_fixed_sign"])
        desired_sign = 1
        signature = r236["same_sign_event_absent_signature"]
        bulk = bulk_by_id[side_id]
        side_identity = K.validate_r248_bulk(
            bulk,
            side_id,
            r236["Round220_split_interface_id"],
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
            r236["double_endpoint_partition_row_id"],
            "SAME_SIGN_EVENT_ABSENT",
            signature,
        )
        need(bulk["positive_volume_proof_kind"] == "ROUND236_TWO_ENDPOINT_GRAPHS_SAME_SIGN_OPEN_REGION", "R248 branch semantics")
        partition_ref = {
            "kind": "R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE",
            "row_id": r236["double_endpoint_partition_row_id"],
            "ordinal": r236_ordinal,
            "full_row_sha256": object_sha(r236),
            "C4_bridge_ref": row_ref(bridge, "bridge_row_id"),
            "Round220_split_interface_id": r236["Round220_split_interface_id"],
            "active_endpoint_factor": "source",
            "fixed_target_factor_sign": reconstruction["target_factor_fixed_sign"],
            "source_factor_strict_t_derivative_sign": r236["source_factor_strict_t_derivative_sign"],
        }
        factor = K.exact_factor(support)
        side_ast = K.and_ast(support["carrier_domain_ast"], K.sign_relation_ast(factor, eta, "GT"))
        K.validate_primitive_ast(side_ast, "C12a side stratum")
        branch = K.branch_equivalence_certificate(
            "R235D_SOURCE_EXACT_FACE_FULL_BASE",
            "source:SAME_SIGN_EVENT_ABSENT",
            partition_ref,
            side_identity,
            eta,
            desired_sign,
            side_ast,
        )
        trace = K.face_trace_atlas(
            "R235D_SOURCE_EXACT_INWARD_SHARED_FACE_TRACE_V1",
            reconstruction["source_zero_face"],
            eta,
            desired_sign,
            support["carrier_domain_ast"],
        )
        closure = K.closure_certificate("R235D_SOURCE_EXACT_FACE_FULL_BASE", support, side_ast, branch, trace, None)
        need(closure["closure_incidence_complete"] is True and trace["every_graph_point_has_a_side_approach_path"] is True, "theorem completeness")

        core = {
            "schema": ROW_SCHEMA,
            "row_id": PREFIX + ":kernel-row:" + object_sha([reroute["row_id"], graph_id, side_id]),
            "kernel_ordinal": len(output),
            "graph_id": graph_id,
            "graph_class": "R235D_SOURCE_EXACT_FACE_FULL_BASE",
            "sheet_member_id": support["sheet_member_id"],
            "side_member_id": side_id,
            "side_role": "source:SAME_SIGN_EVENT_ABSENT",
            "C12_reroute_ref": row_ref(reroute),
            "C10_exact_graph_support_ref": row_ref(support),
            "C4_bridge_ref": row_ref(bridge, "bridge_row_id"),
            "partition_semantic_ref": partition_ref,
            "R248_side_member_identity": side_identity,
            "coordinate_parameter": "TPS",
            "fixed_other_endpoint_eta": eta,
            "desired_eta_times_active_factor_sign": "STRICT_POSITIVE",
            "exact_side_stratum_ast": side_ast,
            "exact_side_stratum_ast_sha256": object_sha(side_ast),
            "exact_graph_boundary_ast_sha256": support["ast_sha256"]["exact_support_ast_sha256"],
            "partition_branch_to_side_member_equivalence_certificate": branch,
            "closure_incidence_certificate": closure,
            "one_sided_trace_certificate": trace,
            "scoped_credit": {"local_graph_side_physical_incidence": 1, "one_sided_trace": 1},
            "strict_nonpromotion": {
                "R248_positive_volume_label_used_as_support_geometry": False,
                **DOWNSTREAM_ZERO,
            },
        }
        output.append(closed_row(core))

    need(len(output) == len(seen_graphs) == len(seen_sides) == 10, "output exhaustion")
    wire, plain = gzip_rows(output)
    descriptor = {
        "filename": LEDGER,
        "compression": "gzip-level9-mtime-zero",
        "row_count": 10,
        "compressed_size": len(wire),
        "compressed_sha256": hashlib.sha256(wire).hexdigest(),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "ordered_rows_sha256": object_sha(output),
    }
    source = Path(__file__).read_bytes()
    body = {
        "schema": SCHEMA,
        "status": "PASS_10_REROUTED_SOURCE_SHARED_PHYSICAL_INCIDENCES_AND_ONE_SIDED_TRACES__ZERO_PULLBACK_AND_DOWNSTREAM_CREDIT",
        "producer_source": {"filename": Path(__file__).name, "size": len(source), "sha256": hashlib.sha256(source).hexdigest()},
        "source_pins": [pin.__dict__ for pin in PINS],
        "census": {
            "C12_rerouted_relations": 10,
            "local_graph_side_physical_incidences_proved": 10,
            "one_sided_traces_proved": 10,
            "distinct_positive_source_graphs": 10,
            "distinct_shared_side_members": 10,
        },
        "scoped_credit": {"local_graph_side_physical_incidence": 10, "one_sided_trace": 10},
        "formal_credit": DOWNSTREAM_ZERO,
        "strict_nonpromotion": {
            "graph_sheet_set_equality_proved": False,
            "representation_pullback_proved": False,
            "DSU_edge_or_union_authorized": False,
            "normalized_support_sealed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "kernel_ledger": descriptor,
        "updated_graph_side_census": {
            "corrected_graph_side_denominator": 10_128,
            "previously_sealed_C11a_C11b": 9_950,
            "newly_sealed_C12a": 10,
            "total_local_theorem_credit": 9_960,
            "remaining_blocked": 168,
        },
        "required_next": "CLOSE_168_BLOCKED_GRAPH_SIDE_RELATIONS_AND_PROVE_5264_GRAPH_TO_SHEET_SET_EQUALITIES",
    }
    return {**body, "result_sha256": object_sha(body)}, wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "no clobber:" + filename)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    need((args.candidate_dir is not None) != args.publish, "exactly one output mode")
    result, wire = build()
    result_wire = canonical(result)
    directory = ROOT if args.publish else Path(args.candidate_dir).resolve()
    if not args.publish:
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    write_once(directory, LEDGER, wire)
    write_once(directory, RESULT, result_wire)
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
