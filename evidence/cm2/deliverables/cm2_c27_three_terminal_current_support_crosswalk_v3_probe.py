#!/usr/bin/env python3
"""C27-independent v3 identity/chart/sign crosswalk and withheld audit.

No C27 artifact and no edge ledger is opened.  The probe joins the 51,172
current C19A/B/C exact support rows back to their explicit R234--R248 and C5
semantic sources, materializing chart, complete signature, and available sign
authority.  It also gives an identity-level disposition for every R300C
withheld sheet and every R300C nonincident occurrence.  Geometry that still
requires a current-full-support all-pairs scan is kept explicitly open.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import random
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent

FILES = {
    "R234": "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json",
    "R235": "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json",
    "R236": "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
    "R245": "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
    "R246": "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
    "R247": "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
    "R248": "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",
    "C5": "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz",
    "C6I": "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_invalidation_ledger.jsonl.gz",
    "C15": "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
    "C19A": "cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz",
    "C19B": "cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz",
    "C19C": "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz",
    "C22A": "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz",
    "C23A": "cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz",
    "C24A": "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz",
    "C25": "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz",
    "R300C_W": "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_witness_ledger.json.gz",
}

PINS = {
    FILES["R234"]: "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    FILES["R235"]: "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    FILES["R236"]: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    FILES["R245"]: "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    FILES["R246"]: "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    FILES["R247"]: "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    FILES["R248"]: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    FILES["C5"]: "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",
    FILES["C6I"]: "7f4c361b5039b9adac60cdb08405f384dc4a05bbe66b4ae2eac49ac02204e3db",
    FILES["C15"]: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    FILES["C19A"]: "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3",
    FILES["C19B"]: "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798",
    FILES["C19C"]: "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    FILES["C22A"]: "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    FILES["C23A"]: "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",
    FILES["C24A"]: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    FILES["C25"]: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    FILES["R300C_W"]: "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def close_check(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":closure")


def jsonl(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"{name}:newline:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw,
                 f"{name}:canonical:{ordinal}")
            close_check(row, f"{name}:{ordinal}")
            yield row


def rows_after_marker(
    stream: Any,
    marker: str,
    label: str,
    require_row_closure: bool = True,
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        piece = stream.read(1 << 20)
        need(bool(piece), label + ":marker")
        buffer += piece
        if len(buffer) > len(marker) + (4 << 20):
            buffer = buffer[-(len(marker) + (2 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder()
    ordinal = 0
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), label + ":EOF")
            buffer = piece
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        try:
            row, end = decoder.raw_decode(buffer)
        except json.JSONDecodeError:
            piece = stream.read(1 << 20)
            need(bool(piece), label + ":malformed")
            buffer += piece
            continue
        need(type(row) is dict, label + ":row object")
        if require_row_closure:
            close_check(row, f"{label}:{ordinal}")
        yield row
        ordinal += 1
        buffer = buffer[end:]


def certificate_rows(name: str, table: str) -> Iterator[dict[str, Any]]:
    marker = f'"{table}":{{'
    with (ROOT / name).open("rt", encoding="utf-8") as stream:
        # Enter the named object, then enter its rows array.
        buffer = ""
        while marker not in buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), name + ":table marker:" + table)
            buffer += piece
            if len(buffer) > len(marker) + (4 << 20):
                buffer = buffer[-(len(marker) + (2 << 20)):]
        tail = buffer.split(marker, 1)[1]
        rows_marker = '"rows":['
        while rows_marker not in tail:
            piece = stream.read(1 << 20)
            need(bool(piece), name + ":rows marker:" + table)
            tail += piece
        # Reuse a tiny stream facade carrying the already-read tail.
        class Prefix:
            def __init__(self, prefix: str, base: Any):
                self.prefix = prefix
                self.base = base
            def read(self, amount: int) -> str:
                if self.prefix:
                    value, self.prefix = self.prefix[:amount], self.prefix[amount:]
                    return value
                return self.base.read(amount)
        prefixed = Prefix(tail, stream)
        yield from rows_after_marker(prefixed, rows_marker, name + ":" + table)


def certificate_direct_array(name: str, table: str) -> Iterator[dict[str, Any]]:
    """Stream a canonical certificate table stored directly as an array."""
    with (ROOT / name).open("rt", encoding="utf-8") as stream:
        yield from rows_after_marker(
            stream,
            f'"{table}":[',
            name + ":" + table,
            require_row_closure=False,
        )


def gzip_document_rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        yield from rows_after_marker(stream, '"rows":[', name)


def box(values: Iterable[str]) -> tuple[Fraction, ...]:
    result = tuple(Fraction(value) for value in values)
    need(len(result) == 6 and all(result[2*i] < result[2*i+1] for i in range(3)),
         "positive box")
    return result


def t_sign(bounds: tuple[Fraction, ...]) -> str:
    if bounds[1] <= 0:
        return "NONPOSITIVE_T_INTERVAL"
    if bounds[0] >= 0:
        return "NONNEGATIVE_T_INTERVAL"
    return "CROSSES_T_ZERO"


def contains(outer: tuple[Fraction, ...], inner: tuple[Fraction, ...]) -> bool:
    return all(
        outer[2 * axis] <= inner[2 * axis]
        and inner[2 * axis + 1] <= outer[2 * axis + 1]
        for axis in range(3)
    )


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "fresh row")
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def write_rows(path: Path, values: Iterable[dict[str, Any]]) -> tuple[str, str, int]:
    state = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for value in values:
                payload = canonical(value)
                state.update(payload)
                stream.write(payload + b"\n")
                count += 1
    return file_hash(path), state.hexdigest(), count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    for name, expected in PINS.items():
        need(file_hash(ROOT / name) == expected, "pin:" + name)

    # Complete current identity/support family maps.
    c15: dict[str, tuple[str, str, str]] = {}
    for ordinal, row in enumerate(jsonl(FILES["C15"])):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        c15[row["registry_member_id"]] = (
            row["fresh_component_id"], row["official_key_id"], row["row_sha256"]
        )
    need(len(c15) == 502_204, "C15 census")
    c25: dict[str, tuple[str, str]] = {}
    for ordinal, row in enumerate(jsonl(FILES["C25"])):
        need(row["member_ordinal"] == ordinal, "C25 ordinal")
        member = row["member_id"]
        need(member in c15, "C25 current identity")
        c25[member] = (
            row["source_bindings"]["support_kernel"], row["support_semantic_kind"]
        )
    need(len(c25) == 502_204, "C25 census")
    c24a: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(jsonl(FILES["C24A"])):
        need(row["ordinal"] == ordinal, "C24A ordinal")
        member = row["member_id"]
        need(member in c15 and member in c25 and member not in c24a, "C24A join")
        need(c25[member][0] == "C24A", "C24A C25 kernel")
        c24a[member] = row
    need(len(c24a) == 15_224, "C24A census")

    # Explicit signature/chart sources.
    retained: dict[str, dict[str, Any]] = {}
    r245_2d: list[dict[str, Any]] = []
    retained_specs = [
        ("R245", "formal_retained_stratum_node_ledger", "strict_positive_3D_witness_box"),
        ("R246", "formal_new_whole_signature_retained_stratum_node_ledger", "strict_positive_3D_witness_box"),
        ("R247", "formal_new_crossing_and_source_seam_retained_stratum_node_ledger", "strict_positive_3D_physical_witness_box"),
    ]
    for round_name, table, box_field in retained_specs:
        for row in certificate_rows(FILES[round_name], table):
            node = row["retained_stratum_node_id"]
            need(node not in retained, "retained node unique")
            retained[node] = {"round": round_name, "row": row, "box_field": box_field}
            if row["local_dimension"] == 2:
                need(round_name == "R245" and row[box_field] is None, "inherited 2D scope")
                r245_2d.append(row)
    need(len(retained) == 6_388 and len(r245_2d) == 264, "retained source census")

    resolved: dict[str, dict[str, Any]] = {}
    for row in certificate_direct_array(FILES["R234"], "resolved_descendant_rows"):
        resolved[row["materialized_row_id"]] = row
    need(len(resolved) == 12_200, "R234 resolved census")
    r235: dict[str, dict[str, Any]] = {}
    for row in certificate_direct_array(FILES["R235"], "single_endpoint_graph_partition_rows"):
        r235[row["endpoint_graph_partition_row_id"]] = row
    need(len(r235) == 38_328, "R235 graph census")
    double: dict[str, dict[str, Any]] = {}
    for row in certificate_direct_array(FILES["R236"], "double_endpoint_partition_rows"):
        double[row["double_endpoint_partition_row_id"]] = row
    crossing: dict[str, dict[str, Any]] = {}
    for row in certificate_direct_array(FILES["R236"], "crossing_dependency_discharge_rows"):
        crossing[row["crossing_dependency_discharge_row_id"]] = row
    need(len(double) == 16 and len(crossing) == 32, "R236 source census")

    c5_by_sha: dict[str, dict[str, Any]] = {}
    c5_by_graph: dict[str, dict[str, Any]] = {}
    for row in jsonl(FILES["C5"]):
        c5_by_sha[row["row_sha256"]] = row
        need(row["graph_id"] not in c5_by_graph, "C5 graph unique")
        c5_by_graph[row["graph_id"]] = row
    need(len(c5_by_sha) == len(c5_by_graph) == 38_608, "C5 census")
    r248_bulk: dict[str, dict[str, Any]] = {}
    for row in certificate_rows(FILES["R248"], "formal_wall_positive_volume_bulk_ledger"):
        r248_bulk[row["wall_bulk_node_id"]] = row
    need(len(r248_bulk) == 88_936, "R248 bulk census")

    crosswalk: list[dict[str, Any]] = []
    chart_census: Counter[str] = Counter()
    source_census: Counter[str] = Counter()
    interval_sign_census: Counter[str] = Counter()
    fixed_factor_census: Counter[str] = Counter()
    external_box_relation_census: Counter[str] = Counter()
    for source in random.Random(args.seed).sample(["C19A", "C19B", "C19C"], 3):
        for ordinal, row in enumerate(jsonl(FILES[source])):
            need(row["ordinal"] == ordinal, source + ":ordinal")
            member = row["member_id"]
            need(member in c15 and c25[member][0] == source, source + ":C15/C25 join")
            current_box = box(row["support_ast"]["bounds"])
            signature: dict[str, Any]
            external_row_sha: str
            authority: str
            fixed_factor_sign = None
            if source == "C19A":
                item = retained[member]
                upstream = item["row"]
                need(upstream[item["box_field"]] is not None, "C19A 3D upstream")
                upstream_box = box(upstream[item["box_field"]])
                if upstream_box == current_box:
                    external_box_relation = "CURRENT_EXACT_SUPPORT_EQUALS_UPSTREAM_POSITIVE_WITNESS"
                else:
                    need(
                        row["construction_certificate"].get(
                            "exact_full_support_not_witness_box"
                        ) is True
                        and contains(current_box, upstream_box),
                        "C19A exact full support contains upstream witness",
                    )
                    external_box_relation = (
                        "CURRENT_EXACT_FULL_SUPPORT_STRICTLY_CONTAINS_"
                        "UPSTREAM_POSITIVE_WITNESS"
                    )
                signature = upstream["local_return_signature"]
                external_row_sha = upstream["row_sha256"]
                authority = item["round"] + "_EXACT_RETAINED_STRATUM_SIGNATURE_AND_BOX"
            elif source == "C19B":
                upstream = r248_bulk[member]
                need(upstream["exact_positive_3D_box"] is not None, "C19B R248 exact box")
                need(box(upstream["exact_positive_3D_box"]) == current_box, "C19B box equality")
                external_box_relation = "CURRENT_EXACT_SUPPORT_EQUALS_UPSTREAM_EXACT_BOX"
                kind = upstream["source_partition_kind"]
                source_id = upstream["source_partition_row_id"]
                if kind == "ROUND234_RESOLVED_DESCENDANT":
                    signature = resolved[source_id]["local_return_signature"]
                else:
                    need(kind == "ROUND236_CROSSING_DISCHARGE_BULK", "C19B source kind")
                    signature = crossing[source_id]["local_return_signature"]
                need(digest(signature) == upstream["local_return_signature_sha256"],
                     "C19B signature join")
                external_row_sha = upstream["row_sha256"]
                authority = "R248_EXACT_POSITIVE_BOX_PLUS_SOURCE_SIGNATURE"
            else:
                semantic = c5_by_sha[row["construction_certificate"]["C5_row_sha256"]]
                need(semantic["graph_id"] == row["construction_certificate"]["graph_id"],
                     "C19C graph join")
                need(box(semantic["semantic_classification"]["complete_parameter_domain"]["box"])
                     == current_box, "C19C complete-domain box")
                external_box_relation = "CURRENT_EXACT_SUPPORT_EQUALS_C5_COMPLETE_DOMAIN"
                graph = r235[semantic["graph_id"]]
                role = row["construction_certificate"]["surviving_side_role"]
                signature = graph[
                    "event_absent_signature" if role == "EVENT_ABSENT"
                    else "event_present_signature"
                ]
                external_row_sha = semantic["row_sha256"]
                fixed_factor_sign = row["construction_certificate"]["fixed_factor_sign"]
                fixed_factor_census[fixed_factor_sign] += 1
                authority = "C5_EMPTY_GRAPH_COMPLETE_DOMAIN_PLUS_R235_SIDE_SIGNATURE"
            need(signature["official_key_id"] == c15[member][1], source + ":official key")
            chart = signature["source_chart"]
            chart_census[chart] += 1
            source_census[source] += 1
            interval_sign_census[t_sign(current_box)] += 1
            external_box_relation_census[external_box_relation] += 1
            crosswalk.append(closed({
                "authority": authority,
                "complete_10_field_return_signature": signature,
                "complete_10_field_return_signature_sha256": digest(signature),
                "current_C15_component_id": c15[member][0],
                "current_C19_source": source,
                "current_C19_support_row_sha256": row["row_sha256"],
                "current_C25_support_semantic_kind": c25[member][1],
                "external_identity_row_sha256": external_row_sha,
                "external_box_relation": external_box_relation,
                "fixed_factor_sign": fixed_factor_sign,
                "member_id": member,
                "official_key_id": c15[member][1],
                "physical_t_interval_sign_class": t_sign(current_box),
                "source_chart": chart,
                "support_bounds_t_p_s": row["support_ast"]["bounds"],
            }))
    crosswalk.sort(key=lambda row: row["member_id"])
    need(len(crosswalk) == 51_172 and source_census == {
        "C19A": 5_596, "C19B": 12_232, "C19C": 33_344,
    }, "C19 crosswalk census")
    crosswalk_path = out / "current_C19_51172_chart_sign_identity_crosswalk.jsonl.gz"
    crosswalk_file, crosswalk_rows, crosswalk_count = write_rows(crosswalk_path, crosswalk)
    need(crosswalk_count == 51_172, "crosswalk output")

    invalid_sheet: dict[str, dict[str, Any]] = {}
    invalid_roles: Counter[str] = Counter()
    for row in jsonl(FILES["C6I"]):
        invalid_roles[row["invalidation_role"]] += 1
        if row["invalidation_role"] == "EMPTY_GRAPH_SHEET":
            invalid_sheet[row["registry_member_id"]] = row
    need(invalid_roles == {"EMPTY_GRAPH_SHEET": 33_344, "EMPTY_GRAPH_SIDE": 33_344},
         "C6 invalidation census")

    sheet_payloads: list[dict[str, Any]] = []
    sheet_source_kind: Counter[str] = Counter()
    for row in certificate_rows(FILES["R248"], "formal_wall_half_open_sheet_owner_ledger"):
        member = row["wall_sheet_node_id"]
        sheet_source_kind[row["source_partition_kind"]] += 1
        if member in invalid_sheet:
            disposition = "INVALIDATED_BY_C6_EMPTY_GRAPH_SHEET"
            kernel = None
            component = None
            disposition_row_sha = invalid_sheet[member]["row_sha256"]
        elif member in c15:
            kernel = c25[member][0]
            need(kernel in {"C19D", "C24A"}, "current wall sheet kernel")
            disposition = (
                "CURRENT_C15_EXACT_PARTIAL_SHEET_C19D"
                if kernel == "C19D"
                else "CURRENT_C15_RELATION_BACKED_SHEET_C24A"
            )
            component = c15[member][0]
            disposition_row_sha = c15[member][2]
        else:
            disposition = "NOT_IN_CURRENT_C15_AND_NOT_C6_INVALIDATION"
            kernel = None
            component = None
            disposition_row_sha = None
        sheet_payloads.append({
            "current_C15_component_id": component,
            "current_C25_support_kernel": kernel,
            "disposition": disposition,
            "disposition_authority_row_sha256": disposition_row_sha,
            "endpoint_factor": row["endpoint_factor"],
            "exact_closed_base_rectangle": row["exact_closed_base_rectangle"],
            "half_open_owner_rule": row["half_open_owner_rule"],
            "owner_mixed_sheet_edge_id": row["owner_mixed_sheet_edge_id"],
            "owner_official_key_id": row["owner_official_key_id"],
            "owner_signature_sha256": row["owner_signature_sha256"],
            "owner_wall_bulk_node_id": row["owner_wall_bulk_node_id"],
            "R248_sheet_row_sha256": row["row_sha256"],
            "Round220_split_interface_id": row["Round220_split_interface_id"],
            "assigned_mixed_sheet_quotient_component_id": row[
                "assigned_mixed_sheet_quotient_component_id"
            ],
            "source_partition_kind": row["source_partition_kind"],
            "source_partition_row_id": row["source_partition_row_id"],
            "wall_sheet_node_id": member,
        })

    # Each of the sixteen initially-unmatched Round236 target-factor sheets is
    # the exact endpoint-factor alias of the one current C24A source-factor
    # sibling from the same double-endpoint source.  Prove the pairing from
    # the R248 rows themselves rather than treating either identity as absent.
    double_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for payload in sheet_payloads:
        if payload["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET":
            double_groups[payload["source_partition_row_id"]].append(payload)
    alias_fields = (
        "Round220_split_interface_id",
        "assigned_mixed_sheet_quotient_component_id",
        "exact_closed_base_rectangle",
        "half_open_owner_rule",
        "owner_official_key_id",
        "owner_signature_sha256",
        "owner_wall_bulk_node_id",
    )
    need(len(double_groups) == 16, "R236 double sheet source census")
    for source_id, siblings in double_groups.items():
        need(len(siblings) == 2, "R236 exact two endpoint-factor siblings:" + source_id)
        current = [
            row for row in siblings
            if row["disposition"] == "CURRENT_C15_RELATION_BACKED_SHEET_C24A"
        ]
        unmatched = [
            row for row in siblings
            if row["disposition"] == "NOT_IN_CURRENT_C15_AND_NOT_C6_INVALIDATION"
        ]
        need(len(current) == len(unmatched) == 1, "R236 current/unmatched sibling split")
        current_row, alias_row = current[0], unmatched[0]
        upstream_double = double[source_id]
        current_c24a = c24a[current_row["wall_sheet_node_id"]]
        current_c5 = c5_by_graph[current_c24a["graph_id"]]
        support_args = {
            item["coordinate"]: (item["lower"], item["upper"])
            for item in current_c24a["normalized_support_ast"]["args"]
        }
        rectangle = current_row["exact_closed_base_rectangle"]
        need(
            {current_row["endpoint_factor"], alias_row["endpoint_factor"]}
            == {"source", "target"}
            and all(current_row[field] == alias_row[field] for field in alias_fields)
            and upstream_double["source_factor_strict_t_derivative_sign"]
            == upstream_double["target_factor_strict_t_derivative_sign"]
            == "STRICT_POSITIVE"
            and digest(upstream_double["same_sign_event_absent_signature"])
            == current_row["owner_signature_sha256"]
            and upstream_double["same_sign_event_absent_signature"]["official_key_id"]
            == current_row["owner_official_key_id"]
            and current_c24a["row_kind"]
            == "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
            and current_c24a["official_key_id"] == current_row["owner_official_key_id"]
            and current_c24a["normalized_support_ast"]["op"] == "AND"
            and support_args == {
                "p": (rectangle[0], rectangle[1]),
                "s": (rectangle[2], rectangle[3]),
            }
            and current_c5["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"
            and current_c5["semantic_classification"]["classification"]
            == "POSITIVE_GRAPH"
            and current_row["wall_sheet_node_id"] not in invalid_sheet,
            "R236 exact endpoint-factor alias",
        )
        alias_row.update({
            "current_C15_component_id": current_row["current_C15_component_id"],
            "current_C25_support_kernel": current_row["current_C25_support_kernel"],
            "disposition": (
                "EXACT_ENDPOINT_FACTOR_ALIAS_OF_CURRENT_C24A_SIBLING_"
                "SAME_R236_SOURCE_AND_PHYSICAL_SHEET"
            ),
            "disposition_authority_row_sha256": current_row[
                "disposition_authority_row_sha256"
            ],
            "current_C24A_sibling_R248_sheet_row_sha256": current_row[
                "R248_sheet_row_sha256"
            ],
            "current_C24A_sibling_wall_sheet_node_id": current_row[
                "wall_sheet_node_id"
            ],
            "current_C24A_sibling_row_sha256": current_c24a["row_sha256"],
            "current_C24A_sibling_graph_id": current_c24a["graph_id"],
            "current_C5_positive_graph_row_sha256": current_c5["row_sha256"],
            "upstream_R236_double_endpoint_row_sha256": digest(upstream_double),
        })

    sheet_disposition = Counter(row["disposition"] for row in sheet_payloads)
    sheet_rows = [closed(payload) for payload in sheet_payloads]
    sheet_rows.sort(key=lambda row: row["wall_sheet_node_id"])
    need(len(sheet_rows) == 38_360, "R248 withheld sheet census")
    need(sheet_disposition == {
        "INVALIDATED_BY_C6_EMPTY_GRAPH_SHEET": 33_344,
        "CURRENT_C15_EXACT_PARTIAL_SHEET_C19D": 4_432,
        "CURRENT_C15_RELATION_BACKED_SHEET_C24A": 568,
        "EXACT_ENDPOINT_FACTOR_ALIAS_OF_CURRENT_C24A_SIBLING_SAME_R236_SOURCE_AND_PHYSICAL_SHEET": 16,
    }, "R248 sheet identity disposition")
    sheet_path = out / "R300C_withheld_38360_wall_sheet_current_identity_disposition.jsonl.gz"
    sheet_file, sheet_rows_sha, sheet_count = write_rows(sheet_path, sheet_rows)

    inherited_rows: list[dict[str, Any]] = []
    inherited_disposition: Counter[str] = Counter()
    for row in r245_2d:
        member = row["retained_stratum_node_id"]
        need(member in c15 and member in c25, "R245 2D current identity")
        kernel, semantic = c25[member]
        disposition = "CURRENT_C15_RELATION_BACKED_C24A" if kernel == "C24A" else "OTHER"
        inherited_disposition[disposition] += 1
        inherited_rows.append(closed({
            "complete_10_field_return_signature_sha256": digest(row["local_return_signature"]),
            "current_C15_component_id": c15[member][0],
            "current_C25_support_kernel": kernel,
            "current_C25_support_semantic_kind": semantic,
            "disposition": disposition,
            "exact_positive_2D_sheet_area": row["exact_positive_2D_sheet_area"],
            "member_id": member,
            "R245_row_sha256": row["row_sha256"],
            "source_chart": row["local_return_signature"]["source_chart"],
            "stratum_kind": row["stratum_kind"],
        }))
    inherited_rows.sort(key=lambda row: row["member_id"])
    need(len(inherited_rows) == 264 and inherited_disposition == {
        "CURRENT_C15_RELATION_BACKED_C24A": 264,
    }, "R245 inherited 2D disposition")
    inherited_path = out / "R300C_withheld_264_inherited_2D_current_identity_disposition.jsonl.gz"
    inherited_file, inherited_rows_sha, inherited_count = write_rows(
        inherited_path, inherited_rows
    )

    # R300C incident identity set, reconstructed from witnesses rather than an
    # edge ledger.  Current exact-support geometry remains a separate v3 gate.
    incident: set[str] = set()
    for row in gzip_document_rows(FILES["R300C_W"]):
        need(row["positive_volume_physical_overlap"] is True, "R300C witness")
        incident.add(row["Round294_registry_occurrence_id"])
    need(len(incident) == 6_314, "R300C incident occurrence census")

    occurrence: dict[str, dict[str, Any]] = {}
    for source in ("C22A", "C23A"):
        for row in jsonl(FILES[source]):
            member = row["owner_member_id"]
            need(member in c15 and member in c25, "occurrence current join")
            item = occurrence.setdefault(member, {
                "atom_count": 0,
                "charts": set(),
                "kernel": c25[member][0],
                "semantic": c25[member][1],
            })
            item["atom_count"] += 1
            support = row["support_ast"]
            item["charts"].add(support.get("coordinate_chart", support.get("recharted_target_chart")))
    need(len(occurrence) == 304_740, "current new occurrence census")
    nonincident_rows: list[dict[str, Any]] = []
    current_incident = 0
    for member in sorted(occurrence):
        item = occurrence[member]
        need(len(item["charts"]) == 1, "occurrence unique chart")
        if member in incident:
            current_incident += 1
            continue
        nonincident_rows.append(closed({
            "current_C15_component_id": c15[member][0],
            "current_C25_support_kernel": item["kernel"],
            "current_C25_support_semantic_kind": item["semantic"],
            "current_exact_support_atom_count": item["atom_count"],
            "disposition": "NO_EXPLICIT_R300C_WITNESS__PENDING_CURRENT_FULL_SUPPORT_ALL_C19_PAIR_SCAN",
            "member_id": member,
            "source_chart": next(iter(item["charts"])),
        }))
    need(current_incident == 6_314 and len(nonincident_rows) == 298_426,
         "R300C incident/nonincident identity partition")
    nonincident_path = out / "R300C_298426_nonincident_current_identity_disposition.jsonl.gz"
    nonincident_file, nonincident_rows_sha, nonincident_count = write_rows(
        nonincident_path, nonincident_rows
    )

    unresolved_sheet_ids = [
        row["wall_sheet_node_id"] for row in sheet_rows
        if row["disposition"] == "NOT_IN_CURRENT_C15_AND_NOT_C6_INVALIDATION"
    ]
    result: dict[str, Any] = {
        "C27_FAMILIES_imported_or_read": False,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "invocation_seed": args.seed,
        "input_pins": dict(sorted(PINS.items())),
        "current_C19_external_crosswalk": {
            "row_count": crosswalk_count,
            "source_census": dict(sorted(source_census.items())),
            "source_chart_census": dict(sorted(chart_census.items())),
            "physical_t_interval_sign_census": dict(sorted(interval_sign_census.items())),
            "external_box_relation_census": dict(sorted(external_box_relation_census.items())),
            "C19C_fixed_factor_sign_census": dict(sorted(fixed_factor_census.items())),
            "identity_chart_signature_gap": 0,
            "ledger_filename": crosswalk_path.name,
            "ledger_file_sha256": crosswalk_file,
            "ledger_rows_sha256": crosswalk_rows,
        },
        "R300C_withheld_disposition": {
            "wall_sheet_count": sheet_count,
            "wall_sheet_source_kind_census": dict(sorted(sheet_source_kind.items())),
            "wall_sheet_current_identity_disposition_census": dict(sorted(sheet_disposition.items())),
            "wall_sheet_unresolved_identity_count": len(unresolved_sheet_ids),
            "wall_sheet_unresolved_identity_ids_sha256": digest(unresolved_sheet_ids),
            "wall_sheet_ledger_filename": sheet_path.name,
            "wall_sheet_ledger_file_sha256": sheet_file,
            "wall_sheet_ledger_rows_sha256": sheet_rows_sha,
            "inherited_2D_count": inherited_count,
            "inherited_2D_current_identity_disposition_census": dict(sorted(inherited_disposition.items())),
            "inherited_2D_ledger_filename": inherited_path.name,
            "inherited_2D_ledger_file_sha256": inherited_file,
            "inherited_2D_ledger_rows_sha256": inherited_rows_sha,
        },
        "R300C_occurrence_identity_disposition": {
            "current_new_occurrence_count": len(occurrence),
            "explicit_R300C_incident_occurrence_count": current_incident,
            "explicit_R300C_nonincident_occurrence_count": nonincident_count,
            "identity_and_current_support_kernel_crosswalk_gap": 0,
            "current_full_support_all_C19_pair_scan_complete": False,
            "nonincident_ledger_filename": nonincident_path.name,
            "nonincident_ledger_file_sha256": nonincident_file,
            "nonincident_ledger_rows_sha256": nonincident_rows_sha,
        },
        "minimal_remaining_blockers": {
            "R248_wall_sheet_not_current_and_not_C6_invalidated_count": len(unresolved_sheet_ids),
            "R300C_nonincident_occurrences_pending_current_full_support_scan": nonincident_count,
            "three_terminal_total_candidate_universe_materialized": False,
            "three_terminal_unique_priority_assignment_closed": False,
        },
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
        },
        "status": "PASS_C19_51172_EXTERNAL_CHART_SIGN_IDENTITY_CROSSWALK_AND_ALL_WITHHELD_SHEET_IDENTITIES__REJECT_PENDING_CURRENT_FULL_SUPPORT_SCAN__ZERO_CREDIT",
    }
    semantic = dict(result)
    semantic.pop("invocation_seed")
    result["semantic_projection_sha256"] = digest(semantic)
    result["result_sha256"] = digest(result)
    (out / "result.json").write_bytes(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
