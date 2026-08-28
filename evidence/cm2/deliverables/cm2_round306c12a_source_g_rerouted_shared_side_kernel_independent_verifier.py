#!/usr/bin/env python3
"""Independent verifier for the ten C12a rerouted shared-side theorems."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c12a_source_g_rerouted_shared_side_kernel"
LEDGER: Final = PREFIX + "_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"
MANIFEST: Final = PREFIX + "_manifest.sha256"
PRODUCER_SHA: Final = "d30d6458ca528bdcf5a6bf2ea20cb8eafd6a0822c48a2238f44e90667af74c7d"


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1_048_576):
            digest.update(block)
    return digest.hexdigest()


def ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C12_LEDGER", "cm2_round306c12_source_g_local_shared_relation_reroute_ledger.jsonl.gz", 8_566, "37c99c69907d57375d07803d651ac9b878db8bb25c33501b8b7846ccc45bbef5"),
    Pin("C10_SUPPORT", "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz", 19_958_893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C4_LEDGER", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz", 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R236_CERT", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    Pin("R248_CERT", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
)
DOWNSTREAM_KEYS: Final = {
    "graph_sheet_set_equality",
    "representation_pullback",
    "member_normalized_support",
    "global_normalized_support",
    "DSU_edge",
    "DSU_union",
    "B1A",
    "B2",
    "maximality",
    "CM2",
}


def checked_bytes(pin: Pin) -> bytes:
    path = ROOT / pin.filename
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_size == pin.size, "pin size:" + pin.role)
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin.sha256, "pin sha:" + pin.role)
    return raw


def rows(raw: bytes, label: str) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), f"row closure:{label}:{ordinal}")
            yield row


def q(value: Any) -> Fraction:
    if type(value) is str:
        return Fraction(value)
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational wire type")
    return Fraction(value["numerator"], value["denominator"])


def factor_from_support(support: dict[str, Any]) -> dict[str, Any]:
    equation = support["equation_ast"]
    need(equation["op"] == "EQ" and equation["right"] == {"op": "RATIONAL_CONSTANT", "value": "0"}, "zero equation")
    return equation["left"]


def expected_side_ast(support: dict[str, Any], eta: int) -> dict[str, Any]:
    return {
        "op": "AND",
        "args": [
            support["carrier_domain_ast"],
            {
                "op": "GT",
                "left": {"op": "MUL", "args": [{"op": "RATIONAL_CONSTANT", "value": str(eta)}, factor_from_support(support)]},
                "right": {"op": "RATIONAL_CONSTANT", "value": "0"},
            },
        ],
    }


def carrier_bounds(carrier: dict[str, Any]) -> dict[str, tuple[Fraction, Fraction]]:
    need(carrier["op"] == "AND", "carrier conjunction")
    output: dict[str, tuple[Fraction, Fraction]] = {}
    for node in carrier["args"]:
        if node.get("op") == "CLOSED_INTERVAL":
            output[node["coordinate"]] = (q(node["lower"]), q(node["upper"]))
    need(set(output) == {"t", "p", "s"}, "TPS carrier")
    need(all(lower < upper for lower, upper in output.values()), "positive carrier")
    return output


def verify_certificate(row: dict[str, Any], support: dict[str, Any], bridge: dict[str, Any], r236: dict[str, Any], bulk: dict[str, Any]) -> None:
    reconstruction = bridge["semantic_reconstruction"]
    need(reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and reconstruction["complete_domain_partition_verified"] is True, "C4 graph theorem")
    need(q(reconstruction["source_t_derivative_exact_interval"]["lower"]) == q(reconstruction["source_t_derivative_exact_interval"]["upper"]) == Fraction(9, 25), "C4 derivative")
    eta = 1 if reconstruction["target_factor_fixed_sign"] == "STRICT_POSITIVE" else -1
    need(row["fixed_other_endpoint_eta"] == eta and row["desired_eta_times_active_factor_sign"] == "STRICT_POSITIVE", "sign target")
    side_ast = expected_side_ast(support, eta)
    need(row["exact_side_stratum_ast"] == side_ast and row["exact_side_stratum_ast_sha256"] == object_sha(side_ast), "side AST reconstruction")
    need(row["exact_graph_boundary_ast_sha256"] == support["ast_sha256"]["exact_support_ast_sha256"], "graph boundary binding")

    partition = row["partition_semantic_ref"]
    need(partition["kind"] == "R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE", "partition kind")
    need(partition["row_id"] == r236["double_endpoint_partition_row_id"] and partition["full_row_sha256"] == object_sha(r236), "partition binding")
    need(partition["C4_bridge_ref"] == ref(bridge, "bridge_row_id"), "partition bridge binding")
    need(partition["active_endpoint_factor"] == "source" and partition["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "source derivative semantics")

    signature_sha = object_sha(r236["same_sign_event_absent_signature"])
    natural_key = ["ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH", r236["double_endpoint_partition_row_id"], "SAME_SIGN_EVENT_ABSENT", signature_sha]
    expected_member = "round248-wall-bulk:" + object_sha(natural_key)
    identity = row["R248_side_member_identity"]
    need(expected_member == row["side_member_id"] == identity["recomputed_side_member_id"] == bulk["wall_bulk_node_id"], "side natural key")
    need(identity["natural_key_preimage"] == natural_key and identity["natural_key_preimage_sha256"] == object_sha(natural_key), "side natural key preimage")
    need(bulk["source_partition_kind"] == natural_key[0] and bulk["source_partition_row_id"] == natural_key[1] and bulk["branch_label"] == natural_key[2], "R248 lineage")
    need(bulk["exact_positive_3D_box"] is None and bulk["exact_positive_3D_volume"] is None and identity["support_geometry_taken_from_R248"] is False, "R248 nongeometry")

    branch = row["partition_branch_to_side_member_equivalence_certificate"]
    branch_core = dict(branch)
    branch_claimed = branch_core.pop("certificate_sha256", None)
    need(branch_claimed == object_sha(branch_core), "branch certificate closure")
    need(branch["partition_rule"] == "SAME_SIGN_EVENT_ABSENT_IFF_FIXED_TARGET_FACTOR_TIMES_SOURCE_FACTOR_IS_STRICT_POSITIVE", "branch rule")
    need(branch["R248_recomputed_side_member_id"] == expected_member and branch["exact_side_stratum_ast_sha256"] == object_sha(side_ast), "branch subject")
    need(branch["side_member_exact_support_equivalence_proved"] is True and branch["R248_null_positive_box_used_as_support_geometry"] is False, "branch theorem boundary")

    bounds = carrier_bounds(support["carrier_domain_ast"])
    zero_face = reconstruction["source_zero_face"]
    if zero_face == "LOWER":
        need(bounds["t"][0] == 0 < bounds["t"][1], "lower zero face")
        direction = 1
        margin = bounds["t"][1]
    else:
        need(bounds["t"][0] < 0 == bounds["t"][1], "upper zero face")
        direction = -1
        margin = -bounds["t"][0]
    trace = row["one_sided_trace_certificate"]
    need(trace["kind"] == "R235D_SOURCE_EXACT_INWARD_SHARED_FACE_TRACE_V1" and trace["every_graph_point_has_a_side_approach_path"] is True, "trace theorem")
    need(trace["coverage_rule"] == {"rule": "EXPLICIT_t_EQUALS_ZERO_FULL_BASE_FACE", "zero_face": zero_face, "full_closed_p_s_base": True, "all_exact_graph_points_covered": True}, "trace coverage")
    need(len(trace["charts"]) == 1, "trace chart census")
    chart = trace["charts"][0]
    chart_core = dict(chart)
    chart_claimed = chart_core.pop("chart_sha256", None)
    need(chart_claimed == object_sha(chart_core), "trace chart closure")
    need(chart["axis"] == "t" and chart["direction"] == direction and chart["local_strict_sign_conclusion"] == "GT_ZERO", "inward trace direction")
    need(q(chart["carrier_margin_basis"]["uniform_rational_margin"]) == margin, "trace margin")

    closure = row["closure_incidence_certificate"]
    closure_core = dict(closure)
    closure_claimed = closure_core.pop("certificate_sha256", None)
    need(closure_claimed == object_sha(closure_core), "closure certificate closure")
    need(closure["exact_side_stratum_ast_sha256"] == object_sha(side_ast), "closure side binding")
    need(closure["partition_branch_equivalence_certificate_sha256"] == branch_claimed and closure["trace_atlas_sha256"] == object_sha(trace), "closure proof binding")
    need(closure["zero_projection_rule"] == "EXPLICIT_t_EQUALS_ZERO_FULL_BASE_EQUIVALENCE", "closure zero rule")
    need(closure["closure_incidence_complete"] is True and closure["strict_side_and_graph_are_disjoint"] is True and closure["graph_subset_of_relative_side_closure_by_trace_atlas"] is True, "closure theorem")


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--manifest-first", action="store_true")
    args = parser.parse_args()
    output_dir = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()

    if args.manifest_first:
        manifest_entries: dict[str, str] = {}
        for line in (ROOT / MANIFEST).read_text("ascii").splitlines():
            digest, separator, filename = line.partition("  ")
            need(separator == "  " and len(digest) == 64 and filename not in manifest_entries, "manifest syntax")
            manifest_entries[filename] = digest
        need(len(manifest_entries) == 8, "manifest member count")
        for filename, digest in manifest_entries.items():
            need(file_sha(ROOT / filename) == digest, "manifest member:" + filename)

    raw = {pin.role: checked_bytes(pin) for pin in PINS}
    result_path = output_dir / RESULT
    ledger_path = output_dir / LEDGER
    result_raw = result_path.read_bytes()
    result = json.loads(result_raw)
    core = dict(result)
    claimed = core.pop("result_sha256", None)
    need(result_raw == canonical(result) and claimed == object_sha(core), "result closure")
    need(result["producer_source"]["sha256"] == PRODUCER_SHA, "producer binding")
    need(result["census"] == {"C12_rerouted_relations": 10, "local_graph_side_physical_incidences_proved": 10, "one_sided_traces_proved": 10, "distinct_positive_source_graphs": 10, "distinct_shared_side_members": 10}, "result census")
    need(result["scoped_credit"] == {"local_graph_side_physical_incidence": 10, "one_sided_trace": 10}, "result scoped credit")
    need(set(result["formal_credit"]) == DOWNSTREAM_KEYS and all(value == 0 for value in result["formal_credit"].values()), "result downstream zero")
    descriptor = result["kernel_ledger"]
    need(ledger_path.stat().st_size == descriptor["compressed_size"] and file_sha(ledger_path) == descriptor["compressed_sha256"], "ledger descriptor")

    c12 = {row["row_id"]: row for row in rows(raw["C12_LEDGER"], "C12")}
    wanted_graphs = {row["positive_source_graph_id"] for row in c12.values()}
    supports = {row["graph_id"]: row for row in rows(raw["C10_SUPPORT"], "C10") if row["graph_id"] in wanted_graphs}
    bridges = {row["bridge_row_id"]: row for row in rows(raw["C4_LEDGER"], "C4")}
    r236_doc = json.loads(raw["R236_CERT"])
    need(r236_doc["result_sha256"] == object_sha(r236_doc["result"]), "R236 closure")
    r236 = {row["double_endpoint_partition_row_id"]: row for row in r236_doc["result"]["double_endpoint_partition_rows"]}
    r248_doc = json.loads(raw["R248_CERT"])
    need(r248_doc["result_sha256"] == object_sha(r248_doc["result"]), "R248 closure")
    wanted_sides = {row["side_member_id"] for row in c12.values()}
    bulk = {row["wall_bulk_node_id"]: row for row in r248_doc["result"]["formal_wall_positive_volume_bulk_ledger"]["rows"] if row["wall_bulk_node_id"] in wanted_sides}
    need(len(c12) == len(supports) == len(bulk) == 10 and len(bridges) == 16, "input exhaustion")

    output = list(rows(ledger_path.read_bytes(), "C12a"))
    need(len(output) == 10, "output row count")
    seen_graphs: set[str] = set()
    seen_sides: set[str] = set()
    for ordinal, row in enumerate(output):
        need(row["kernel_ordinal"] == ordinal, "kernel order")
        reroute = c12[row["C12_reroute_ref"]["row_id"]]
        support = supports[row["graph_id"]]
        bridge = bridges[row["C4_bridge_ref"]["row_id"]]
        partition = row["partition_semantic_ref"]
        r236_row = r236[partition["row_id"]]
        bulk_row = bulk[row["side_member_id"]]
        need(row["C12_reroute_ref"] == ref(reroute), "C12 reference")
        need(row["C10_exact_graph_support_ref"] == ref(support) and row["C4_bridge_ref"] == ref(bridge, "bridge_row_id"), "authority references")
        need(row["graph_id"] == reroute["positive_source_graph_id"] and row["side_member_id"] == reroute["side_member_id"], "subject binding")
        need(row["graph_class"] == "R235D_SOURCE_EXACT_FACE_FULL_BASE" and row["side_role"] == "source:SAME_SIGN_EVENT_ABSENT", "subject class/role")
        need(row["scoped_credit"] == {"local_graph_side_physical_incidence": 1, "one_sided_trace": 1}, "row credit")
        nonpromotion = row["strict_nonpromotion"]
        need(nonpromotion["R248_positive_volume_label_used_as_support_geometry"] is False, "row R248 boundary")
        need(set(nonpromotion) - {"R248_positive_volume_label_used_as_support_geometry"} == DOWNSTREAM_KEYS and all(nonpromotion[key] == 0 for key in DOWNSTREAM_KEYS), "row downstream zero")
        verify_certificate(row, support, bridge, r236_row, bulk_row)
        need(row["graph_id"] not in seen_graphs and row["side_member_id"] not in seen_sides, "output uniqueness")
        seen_graphs.add(row["graph_id"])
        seen_sides.add(row["side_member_id"])
    need(len(seen_graphs) == len(seen_sides) == 10, "output exhaustion")
    status = "PASS_MANIFEST_FIRST_NO_WRITE_C12A_10_LOCAL_THEOREMS" if args.manifest_first else "PASS_INDEPENDENT_C12A_10_LOCAL_THEOREMS"
    print(json.dumps({"status": status, "result_sha256": claimed}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
