#!/usr/bin/env python3
"""Correct the Source-G endpoint cover and close its exact lower-dimensional glues.

Round252 deliberately left 248 t-face contacts fail-closed.  Those contacts
come from 400 Round235 single-endpoint cells.  On every such cell the active
factor is the Source-G wall coordinate itself:

    G:E/G:W : source_y = (9/25)*t,
    G:N/G:S : source_x = (9/25)*t.

Thus one of the two materialized branch bulks is identically empty on the
strict one-sided cell.  This producer removes the 400 empty bulk nodes,
deletes 216 empty EVENT_PRESENT singleton phantom components, and removes
184 invalid EVENT_ABSENT sheet-owner edges while retaining the exact t=0
sheets.  The retained endpoint sheets on the two sides of each of the 248
contacts have an exact positive-area common refinement and supply 184
rank-reducing plus 64 redundant sheet-identity edges.

Round204 also contains 32 fully materialized EMPTY--EVENT--EMPTY tail glues.
Their 3D regions, source and target 2D sheets, and exact 1D intersections
cross-check byte-for-byte and supply four further rank reductions plus 28
redundant edges.  Starting from the frozen 68,716-component Round262
quotient, the corrected quotient therefore has 68,312 components.

This producer independently reconstructs the complete component,
occurrence, exact-key, and valid virtual-node frontiers.  It does not import
or execute an upstream producer.  It awards no maximality, fibre-exhaustion,
global-disposition, Gate5, D02, or CM2 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = (
    "cm2.round264.source-g-lower-dimensional-endpoint-correction-"
    "and-glue-closure.v1"
)

ROUND204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
ROUND234 = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
ROUND235 = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
ROUND248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
ROUND250 = "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
ROUND251 = "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
ROUND252 = "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json"
ROUND254 = "cm2_round254_source_g_seed_block_quotient_closure_certificate.json"
ROUND258 = "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
ROUND259 = "cm2_round259_source_g_curved_region_full_face_saturation_certificate.json"
ROUND260 = "cm2_round260_source_g_curved_region_common_face_refinement_certificate.json"
ROUND261 = "cm2_round261_source_g_adaptive_common_face_strict_separation_certificate.json"
ROUND262 = "cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json"
ROUND263 = "cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_certificate.json"

INPUTS = {
    ROUND204: (
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
    ),
    ROUND234: (
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
        "d05d6bbc590157e855a577f411668d0f3b7486ccdbea8e47ed30299194b5ba08",
        "cm2.round234.source-g-wall-endpoint-order-depth6-materialization.v1",
    ),
    ROUND235: (
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
        "5bbcf6780338c9a40fa9c131b0270e4fb934de022cf597d2f82d6b85af68dca2",
        "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1",
    ),
    ROUND248: (
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
        "d3dc5783fcaaa308f069e1be232a9b96eeb8b0efc5a4df6cbee70d110d7df1e9",
        "cm2.round248.source-g-wall-finite-key-retained-quotient.v1",
    ),
    ROUND250: (
        "07eb8ab4f5fbcec7df4a891f3e55b3990c8400a01bbbff8950f05519e886ca8a",
        "b20244ff28ef3f545977ac2bc9f2afa496be1aee414acc779f11a6486d4421dc",
        "cm2.round250.source-g-wall-t-chain-patch-saturation.v1",
    ),
    ROUND251: (
        "a1f1d04466585cc8b97fceaa98c1507b293696933af4a58dea3c76d92a0c480f",
        "712a2666ca5db31fcbd047dfc7556402d92d38a3258407bc844601f4a3f1d3a4",
        "cm2.round251.source-g-wall-p-face-patch-saturation.v1",
    ),
    ROUND252: (
        "8ffc927ca3bcefc48581bdb8b66c00f95c302f737692d14ba4cc6dc2e1ad7794",
        "af41bdfa496ff9411a472f258f8be5234d3d11b3fcff0273fa186192aa591f4c",
        "cm2.round252.source-g-wall-s-t-face-patch-saturation.v1",
    ),
    ROUND254: (
        "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf",
        "202544c68006f271152d18dc64a56d36cbfd3f67ebf679eb9104784b06109766",
        "cm2.round254.source-g-seed-block-quotient-closure.v1",
    ),
    ROUND258: (
        "11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb",
        "257c999bb77d1f9e8993898ec2a51675e83e27879b750a160b515a60bb1e13a8",
        "cm2.round258.source-g-whole-box-boundary-face-saturation.v1",
    ),
    ROUND259: (
        "799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039",
        "03f3542ba4d51e6938d098b6822ea76a8ec6225e9bf590e1a96a7c5c67f8eba3",
        "cm2.round259.source-g-curved-region-full-face-saturation.v1",
    ),
    ROUND260: (
        "a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b",
        "5b3d3ec045c5ef5baa9cab9838b019a583ec4077b0867cce2a5c151131ba2f09",
        "cm2.round260.source-g-curved-region-common-face-refinement.v1",
    ),
    ROUND261: (
        "6b69453c869d07737152c851d7716434dca16184433ef8be9023cb56027b162c",
        "5a7ee517842aeec8be03acd1152015560d9abbdf2a54d6e9eb7d0d46d772048a",
        "cm2.round261.source-g-adaptive-common-face-strict-separation.v1",
    ),
    ROUND262: (
        "d9cac69017dd3247428492bdee6402da9868a7d97db3574f41ba25a1b49005de",
        "33d54f038b066d66119bb401c98a0a34b308743ba81932b5693e7a9e69238d6e",
        "cm2.round262.source-g-monotone-deep-common-face-closure.v1",
    ),
    ROUND263: (
        "e6c524db031ce3cac88fece6ca874e9b47290d345e8abe21736697c7dc4fb54c",
        "8e10297d0091abcf9d5bfecf7bd6c6fcb74a3166e06a5c4f1c661ecc92f2ed33",
        "cm2.round263.source-g-complete-occurrence-cross-chart-transition-exhaustion.v1",
    ),
}

EXPECTED_AREA_HISTOGRAM = {
    "1/102400": 48,
    "1/51200": 16,
    "1/25600": 40,
    "1/12800": 88,
    "1/6400": 48,
    "1/3200": 8,
}
EXPECTED_KEY_REDUCTION_HISTOGRAM = {"0": 80, "2": 24, "4": 8, "27": 4}
EXPECTED_SHEET_PAIR_MULTIPLICITY_HISTOGRAM = {"1": 144, "2": 32, "5": 8}


class Round264Error(RuntimeError):
    """A fail-closed Round264 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round264Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def qtext(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def closed(row: dict[str, Any]) -> dict[str, Any]:
    output = dict(row)
    need("row_sha256" not in output, "row already carries closure")
    output["row_sha256"] = digest(output)
    return output


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(
        len(rows) == len({row[id_field] for row in rows}),
        f"unique ledger ids:{id_field}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int = 800_000_000) -> bytes:
    need(path.parent == HERE, f"unexpected input parent:{path.name}")
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"regular nonlinked input:{path.name}",
    )
    need(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable input open:{path.name}",
        )
        pieces: list[bytes] = []
        total = 0
        while True:
            piece = os.read(descriptor, 1024 * 1024)
            if not piece:
                break
            total += len(piece)
            need(total <= maximum, f"bounded input read:{path.name}")
            pieces.append(piece)
        after = os.fstat(descriptor)
        need(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable input read:{path.name}",
        )
        return b"".join(pieces)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict encoding:{label}",
    )

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, f"duplicate JSON key:{label}:{key}")
            output[key] = value
        return output

    def reject(token: str) -> None:
        raise Round264Error(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Round264Error(f"strict JSON:{label}") from error
    need(isinstance(value, dict), f"top-level JSON object:{label}")
    return value


def load_result(name: str) -> dict[str, Any]:
    file_sha256, result_sha256, schema = INPUTS[name]
    raw = regular_bytes(HERE / name)
    need(hashlib.sha256(raw).hexdigest() == file_sha256, f"file pin:{name}")
    document = strict_json(raw, name)
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(document["schema"] == schema, f"schema pin:{name}")
    need(
        document["result_sha256"] == result_sha256
        and digest(document["result"]) == result_sha256,
        f"result pin:{name}",
    )
    need(isinstance(document["result"], dict), f"result object:{name}")
    return document["result"]


def check_closed_rows(
    value: dict[str, Any],
    id_field: str,
    expected_count: int | None = None,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    need(isinstance(rows, list), f"ledger rows:{id_field}")
    need(value["row_count"] == len(rows), f"ledger count:{id_field}")
    if expected_count is not None:
        need(len(rows) == expected_count, f"expected ledger count:{id_field}")
    need(
        len({row[id_field] for row in rows}) == len(rows),
        f"unique ledger ids:{id_field}",
    )
    need(value["rows_sha256"] == digest(rows), f"ledger digest:{id_field}")
    for row in rows:
        body = dict(row)
        expected = body.pop("row_sha256")
        need(expected == digest(body), f"row closure:{id_field}")
    return rows


def checked_plain_rows(
    result: dict[str, Any],
    rows_field: str,
    digest_field: str,
) -> list[dict[str, Any]]:
    rows = result[rows_field]
    need(isinstance(rows, list), f"plain rows:{rows_field}")
    need(result[digest_field] == digest(rows), f"plain rows digest:{rows_field}")
    return rows


def input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": values[0],
            "result_sha256": values[1],
            "schema": values[2],
        }
        for name, values in sorted(INPUTS.items())
    }


class DSU:
    def __init__(self, members: Iterable[str]) -> None:
        values = list(members)
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in values}

    def find(self, value: str) -> str:
        need(value in self.parent, f"DSU member:{value}")
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            parent = self.parent[value]
            self.parent[value] = root
            value = parent
        return root

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if (
            self.size[left_root] < self.size[right_root]
            or (
                self.size[left_root] == self.size[right_root]
                and left_root > right_root
            )
        ):
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.size[left_root] += self.size[right_root]
        return True


def exact_box(values: Any, label: str) -> tuple[Fraction, ...]:
    need(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"exact box:{label}",
    )
    try:
        box = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise Round264Error(f"exact rational box:{label}") from error
    need(all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)), f"box:{label}")
    return box


def rectangle_intersection(
    left: list[str],
    right: list[str],
    label: str,
) -> tuple[list[str], Fraction]:
    need(len(left) == len(right) == 4, f"base rectangles:{label}")
    a = [Fraction(value) for value in left]
    b = [Fraction(value) for value in right]
    rectangle = [
        max(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        min(a[3], b[3]),
    ]
    area = (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])
    need(area > 0, f"positive common rectangle:{label}")
    return [qtext(value) for value in rectangle], area


def component_chain_maps() -> list[dict[str, str]]:
    round254 = load_result(ROUND254)
    rows = check_closed_rows(
        round254["formal_Round252_to_Round254_component_map_ledger"],
        "Round252_to_Round254_component_map_id",
    )
    maps: list[dict[str, str]] = [{
        row["Round252_mixed_sheet_quotient_component_id"]:
        row["post_Round254_mixed_sheet_quotient_component_id"]
        for row in rows
    }]
    del round254, rows
    gc.collect()

    specifications = [
        (
            ROUND258,
            "formal_Round257_to_Round258_component_map_ledger",
            "Round257_quotient_component_id",
            "post_Round258_quotient_component_id",
            "Round257_to_Round258_component_map_row_id",
        ),
        (
            ROUND259,
            "formal_Round258_to_Round259_component_map_ledger",
            "Round258_quotient_component_id",
            "post_Round259_quotient_component_id",
            "Round258_to_Round259_component_map_row_id",
        ),
        (
            ROUND260,
            "formal_Round259_to_Round260_component_map_ledger",
            "Round259_quotient_component_id",
            "post_Round260_quotient_component_id",
            "Round259_to_Round260_component_map_row_id",
        ),
        (
            ROUND261,
            "formal_Round260_to_Round261_component_map_ledger",
            "Round260_quotient_component_id",
            "post_Round261_quotient_component_id",
            "Round260_to_Round261_component_map_row_id",
        ),
        (
            ROUND262,
            "formal_Round261_to_Round262_component_map_ledger",
            "Round261_quotient_component_id",
            "post_Round262_quotient_component_id",
            "Round261_to_Round262_component_map_row_id",
        ),
    ]
    for name, ledger_name, old_field, new_field, row_field in specifications:
        result = load_result(name)
        value = result[ledger_name]
        rows = check_closed_rows(value, row_field)
        mapping = {row[old_field]: row[new_field] for row in rows}
        need(len(mapping) == len(rows), f"component map function:{name}")
        maps.append(mapping)
        del result, value, rows
        gc.collect()
    return maps


def build(producer_sha256: str) -> dict[str, Any]:
    # Round252 supplies both the 248 residual contacts and the complete
    # 133,684-node virtual-stratum universe.
    round252 = load_result(ROUND252)
    rejected = check_closed_rows(
        round252["formal_rejected_axis_face_contact_ledger"],
        "rejected_axis_face_contact_id",
        248,
    )
    need(
        all(
            row["face_axis"] == "t"
            and row["shared_full_return_signature_count"] == 2
            and row["physical_glue_credit"] == 0
            for row in rejected
        ),
        "Round252 residual contract",
    )
    source_ids = {
        row[field]
        for row in rejected
        for field in (
            "left_source_partition_row_id",
            "right_source_partition_row_id",
        )
    }
    need(len(source_ids) == 400, "400 unique residual endpoint cells")

    node_to_252: dict[str, str] = {}
    component252: dict[str, dict[str, Any]] = {}
    component_rows252 = check_closed_rows(
        round252["formal_post_Round252_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
        65_740,
    )
    for row in component_rows252:
        component_id = row["mixed_sheet_quotient_component_id"]
        need(component_id not in component252, f"unique Round252 component:{component_id}")
        nodes = tuple(row["virtual_stratum_node_ids"])
        edges = tuple(row["mixed_sheet_edge_ids"])
        need(
            row["virtual_stratum_node_count"] == len(nodes)
            and row["mixed_sheet_edge_count"] == len(edges),
            f"Round252 component census:{component_id}",
        )
        component252[component_id] = {
            "nodes": nodes,
            "edges": frozenset(edges),
            "materialized_member_count": row["materialized_member_count"],
            "resolved_child_count": row["member_Round179_resolved_child_count"],
            "official_key_id": row["official_key_id"],
        }
        for node_id in nodes:
            need(node_id not in node_to_252, f"unique virtual node:{node_id}")
            node_to_252[node_id] = component_id
    need(len(node_to_252) == 133_684, "Round252 virtual node universe")

    accepted_incident_nodes: set[str] = set()
    accepted252 = check_closed_rows(
        round252["formal_wall_axis_face_positive_patch_edge_ledger"],
        "wall_axis_face_edge_id",
        22_016,
    )
    for row in accepted252:
        accepted_incident_nodes.add(row["left_wall_bulk_node_id"])
        accepted_incident_nodes.add(row["right_wall_bulk_node_id"])
    del component_rows252, accepted252, round252
    gc.collect()

    # Round234 binds every selected endpoint partition to its exact one-sided
    # t,p,s cell.
    round234 = load_result(ROUND234)
    rows234 = checked_plain_rows(
        round234,
        "depth6_frontier_rows",
        "depth6_frontier_rows_sha256",
    )
    frontier_ids = {
        row["Round234_frontier_row_id"]
        for row in []  # populated after Round235 below
    }
    frontier234_all = {row["frontier_row_id"]: row for row in rows234}
    need(len(frontier234_all) == len(rows234), "unique Round234 frontier")
    del round234, rows234
    gc.collect()

    round235 = load_result(ROUND235)
    rows235 = checked_plain_rows(
        round235,
        "single_endpoint_graph_partition_rows",
        "single_endpoint_graph_partition_rows_sha256",
    )
    selected235 = {
        row["endpoint_graph_partition_row_id"]: row
        for row in rows235
        if row["endpoint_graph_partition_row_id"] in source_ids
    }
    need(set(selected235) == source_ids, "selected Round235 endpoint metadata")
    frontier_ids = {row["Round234_frontier_row_id"] for row in selected235.values()}
    need(frontier_ids <= set(frontier234_all), "Round234 frontier references")
    selected234 = {key: frontier234_all[key] for key in frontier_ids}
    del round235, rows235, frontier234_all
    gc.collect()

    round248 = load_result(ROUND248)
    bulk_rows248 = check_closed_rows(
        round248["formal_wall_positive_volume_bulk_ledger"],
        "wall_bulk_node_id",
        88_936,
    )
    bulks_by_source: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in bulk_rows248:
        source_id = row["source_partition_row_id"]
        if source_id in source_ids:
            label = row["branch_label"]
            need(label not in bulks_by_source[source_id], f"unique branch:{source_id}:{label}")
            bulks_by_source[source_id][label] = row
    need(
        set(bulks_by_source) == source_ids
        and all(set(rows) == {"EVENT_ABSENT", "EVENT_PRESENT"} for rows in bulks_by_source.values()),
        "two Round248 bulk branches per endpoint cell",
    )
    sheet_rows248 = check_closed_rows(
        round248["formal_wall_half_open_sheet_owner_ledger"],
        "wall_sheet_node_id",
        38_360,
    )
    sheets_by_source: dict[str, dict[str, Any]] = {}
    for row in sheet_rows248:
        source_id = row["source_partition_row_id"]
        if source_id in source_ids:
            need(source_id not in sheets_by_source, f"unique endpoint sheet:{source_id}")
            sheets_by_source[source_id] = row
    need(set(sheets_by_source) == source_ids, "one retained sheet per endpoint cell")
    del round248, bulk_rows248, sheet_rows248
    gc.collect()

    # No accepted strict edge in R250, R251, or R252 may touch an empty node.
    for name, ledger_name, id_field in (
        (ROUND250, "formal_wall_t_chain_positive_patch_edge_ledger", "wall_chain_edge_id"),
        (ROUND251, "formal_wall_p_face_positive_patch_edge_ledger", "wall_p_face_edge_id"),
    ):
        result = load_result(name)
        rows = check_closed_rows(result[ledger_name], id_field)
        for row in rows:
            accepted_incident_nodes.add(row["left_wall_bulk_node_id"])
            accepted_incident_nodes.add(row["right_wall_bulk_node_id"])
        del result, rows
        gc.collect()

    # Map every Round252 virtual node to the frozen Round262 quotient.
    maps = component_chain_maps()

    def current_component_for_252(component_id: str) -> str:
        value = component_id
        for mapping in maps:
            need(value in mapping, f"component chain coverage:{value}")
            value = mapping[value]
        return value

    node_to_current = {
        node_id: current_component_for_252(component_id)
        for node_id, component_id in node_to_252.items()
    }

    # Recheck Round263's exact identity freeze before mutating the quotient.
    round263 = load_result(ROUND263)
    need(
        round263["census"]["post_Round263_component_count"] == 68_716
        and round263["census"]["occurrence_frontier_count"] == 53_968
        and round263["census"]["exact_key_frontier_count"] == 116
        and round263["census"]["true_source_chart_seam_candidate_count"] == 0
        and round263["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round263 frozen precondition",
    )
    del round263
    gc.collect()

    # Load the frozen frontier itself.  ROUND262 was already checked in the
    # chain; loading it again is intentional because this pass verifies the
    # complete frontier rows independently of the component-map pass.
    round262 = load_result(ROUND262)
    component_rows262 = check_closed_rows(
        round262["formal_post_Round262_component_commitment_ledger"],
        "post_Round262_component_row_id",
        68_716,
    )
    occurrence_rows262 = check_closed_rows(
        round262["formal_post_Round262_occurrence_frontier_ledger"],
        "post_frontier_row_id",
        53_968,
    )
    key_rows262 = check_closed_rows(
        round262["formal_post_Round262_key_frontier_ledger"],
        "post_Round262_key_frontier_row_id",
        116,
    )
    base_component = {
        row["post_Round262_quotient_component_id"]: {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "source_row_id": row["post_Round262_component_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in component_rows262
    }
    need(len(base_component) == 68_716, "unique frozen Round262 components")
    base_occurrence = {
        row["local_occurrence_row_id"]: {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "current_component_id": row["post_Round262_quotient_component_id"],
            "source_row_id": row["post_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in occurrence_rows262
    }
    need(len(base_occurrence) == 53_968, "unique Round262 occurrence frontier")
    base_key = {
        row["official_key_id"]: {
            "official_key_ordinal": row["official_key_ordinal"],
            "pre_component_count": row["post_Round262_quotient_component_count"],
            "occurrence_count": row["local_occurrence_count"],
            "source_row_id": row["post_Round262_key_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in key_rows262
    }
    need(len(base_key) == 116, "unique Round262 exact-key frontier")
    del component_rows262, occurrence_rows262, key_rows262, round262
    gc.collect()

    # Exact one-sided empty-branch correction.
    correction_rows: list[dict[str, Any]] = []
    empty_nodes: set[str] = set()
    phantom_components: set[str] = set()
    invalid_owner_edges_by_component: dict[str, list[str]] = defaultdict(list)
    removed_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    retained_sheets_by_component: dict[str, list[str]] = defaultdict(list)
    empty_label_histogram: Counter[str] = Counter()
    chart_cell_histogram: Counter[str] = Counter()
    invalid_owner_edges: set[str] = set()

    for source_id in sorted(source_ids):
        metadata = selected235[source_id]
        need(
            metadata["active_endpoint_factor"] == "source"
            and metadata["active_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE",
            f"source active factor:{source_id}",
        )
        chart = metadata["source_chart"]
        reason = metadata["reason_label"]
        reason_parts = reason.split(":")
        need(
            chart in {"G:E", "G:N", "G:S", "G:W"}
            and len(reason_parts) == 3
            and reason_parts[0] == "wall_endpoint_or_count_transition",
            f"endpoint reason:{source_id}",
        )
        expected_axis = "Y" if chart in {"G:E", "G:W"} else "X"
        need(reason_parts[1] == expected_axis and reason_parts[2] == "0", f"chart axis:{source_id}")
        frontier = selected234[metadata["Round234_frontier_row_id"]]
        need(
            frontier["chart"] == chart
            and frontier["owner_target"] == metadata["target_lift"]
            and frontier["Round220_split_interface_id"] == metadata["Round220_split_interface_id"]
            and reason in frontier["reason_labels"],
            f"Round234/Round235 binding:{source_id}",
        )
        box = exact_box(frontier["box"], source_id)
        if box[1] == 0 and box[0] < 0:
            side = "STRICT_NEGATIVE_T_SIDE"
            source_sign = "STRICT_NEGATIVE"
        elif box[0] == 0 and box[1] > 0:
            side = "STRICT_POSITIVE_T_SIDE"
            source_sign = "STRICT_POSITIVE"
        else:
            raise Round264Error(f"one-sided t=0 cell:{source_id}")
        sheet = sheets_by_source[source_id]
        need(
            sheet["endpoint_factor"] == "source"
            and sheet["exact_closed_base_rectangle"] == frontier["box"][2:6]
            and sheet["sheet_three_dimensional_coordinate_volume"] == "0"
            and sheet["exact_positive_2D_sheet_area"] != "0",
            f"exact endpoint sheet base:{source_id}",
        )
        fixed_sign = metadata["fixed_endpoint_factor_sign"]
        need(fixed_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, f"fixed sign:{source_id}")
        present_nonempty = source_sign != fixed_sign
        nonempty_label = "EVENT_PRESENT" if present_nonempty else "EVENT_ABSENT"
        empty_label = "EVENT_ABSENT" if present_nonempty else "EVENT_PRESENT"
        empty = bulks_by_source[source_id][empty_label]
        nonempty = bulks_by_source[source_id][nonempty_label]
        need(
            empty["exact_positive_3D_box"] is None
            and empty["exact_positive_3D_volume"] is None
            and nonempty["exact_positive_3D_box"] is None
            and nonempty["exact_positive_3D_volume"] is None
            and empty["positive_volume_proof_kind"]
            == f"ROUND235_STRICT_MONOTONE_GRAPH_{empty_label.removeprefix('EVENT_')}_OPEN_SIDE"
            and nonempty["positive_volume_proof_kind"]
            == f"ROUND235_STRICT_MONOTONE_GRAPH_{nonempty_label.removeprefix('EVENT_')}_OPEN_SIDE",
            f"Round248 nullable branch encoding and proof labels:{source_id}",
        )
        empty_node = empty["wall_bulk_node_id"]
        nonempty_node = nonempty["wall_bulk_node_id"]
        need(
            empty_node in node_to_252
            and nonempty_node in node_to_252
            and sheet["wall_sheet_node_id"] in node_to_252,
            f"materialized virtual nodes:{source_id}",
        )
        need(empty_node not in accepted_incident_nodes, f"empty accepted-edge incidence:{source_id}")
        empty_current = node_to_current[empty_node]
        nonempty_current = node_to_current[nonempty_node]
        need(
            base_component[empty_current]["official_key_id"] == empty["official_key_id"]
            and base_component[nonempty_current]["official_key_id"] == nonempty["official_key_id"],
            f"current exact-key binding:{source_id}",
        )
        invalid_edge: str | None = None
        if empty_label == "EVENT_PRESENT":
            statistics = component252[node_to_252[empty_node]]
            need(
                statistics["nodes"] == (empty_node,)
                and len(statistics["edges"]) == 0
                and statistics["materialized_member_count"] == 1
                and statistics["resolved_child_count"] == 0,
                f"empty EVENT_PRESENT singleton:{source_id}",
            )
            phantom_components.add(empty_current)
            disposition = "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT"
        else:
            invalid_edge = sheet["owner_mixed_sheet_edge_id"]
            need(
                sheet["owner_wall_bulk_node_id"] == empty_node
                and invalid_edge in component252[node_to_252[empty_node]]
                ["edges"],
                f"invalid empty EVENT_ABSENT owner edge:{source_id}",
            )
            need(
                node_to_252[empty_node] == node_to_252[sheet["wall_sheet_node_id"]],
                f"empty absent sheet component:{source_id}",
            )
            invalid_owner_edges.add(invalid_edge)
            invalid_owner_edges_by_component[empty_current].append(invalid_edge)
            retained_sheets_by_component[empty_current].append(sheet["wall_sheet_node_id"])
            disposition = "PRUNE_EMPTY_ABSENT_BULK_NODE_AND_INVALID_OWNER_EDGE__RETAIN_T0_SHEET"
        empty_nodes.add(empty_node)
        removed_nodes_by_component[empty_current].append(empty_node)
        empty_label_histogram[empty_label] += 1
        chart_cell_histogram[chart] += 1
        correction_rows.append(closed({
            "endpoint_empty_branch_disposition_row_id":
                "round264-endpoint-empty-branch:" + digest([source_id]),
            "source_partition_row_id": source_id,
            "Round234_frontier_row_id": metadata["Round234_frontier_row_id"],
            "Round220_split_interface_id": metadata["Round220_split_interface_id"],
            "source_chart": chart,
            "target_lift": metadata["target_lift"],
            "exact_one_sided_cell_box": frontier["box"],
            "reason_label": reason,
            "transition_event": metadata["transition_event"],
            "transition_event_order_position": metadata["transition_event_order_position"],
            "active_endpoint_factor": "source",
            "active_factor_strict_t_derivative_sign": "STRICT_POSITIVE",
            "relevant_source_coordinate":
                "source_y" if expected_axis == "Y" else "source_x",
            "exact_relevant_source_coordinate_formula": "(9/25)*t",
            "exact_zero_set": "t=0",
            "strict_open_cell_side": side,
            "strict_source_factor_sign_on_open_cell": source_sign,
            "fixed_target_endpoint_factor_sign": fixed_sign,
            "nonempty_branch_label": nonempty_label,
            "nonempty_wall_bulk_node_id": nonempty_node,
            "nonempty_official_key_id": nonempty["official_key_id"],
            "empty_branch_label": empty_label,
            "empty_wall_bulk_node_id": empty_node,
            "empty_official_key_id": empty["official_key_id"],
            "empty_branch_proof":
                "EXACT_SIGN_OF_(9/25)*t_AGAINST_FIXED_ENDPOINT_SIGN_ON_STRICT_OPEN_SIDE",
            "empty_branch_Round250_Round251_Round252_accepted_edge_incidence_count": 0,
            "pre_Round264_empty_node_component_id": empty_current,
            "pre_Round264_nonempty_node_component_id": nonempty_current,
            "retained_t0_sheet_node_id": sheet["wall_sheet_node_id"],
            "invalid_Round248_owner_edge_id": invalid_edge,
            "disposition": disposition,
            "component_credit": -1 if empty_label == "EVENT_PRESENT" else 0,
            "maximality_credit": 0,
        }))
    correction_rows.sort(key=lambda row: row["endpoint_empty_branch_disposition_row_id"])

    need(len(empty_nodes) == 400, "400 distinct empty bulk nodes")
    need(len(phantom_components) == 216, "216 phantom singleton components")
    need(len(invalid_owner_edges) == 184, "184 invalid absent owner edges")
    need(dict(sorted(empty_label_histogram.items())) == {"EVENT_ABSENT": 184, "EVENT_PRESENT": 216}, "empty label census")
    need(dict(sorted(chart_cell_histogram.items())) == {"G:E": 100, "G:N": 100, "G:S": 100, "G:W": 100}, "endpoint cell chart census")
    need(not (set(removed_nodes_by_component) - set(base_component)), "corrected components exist")
    occurrence_current_ids = {row["current_component_id"] for row in base_occurrence.values()}
    need(phantom_components.isdisjoint(occurrence_current_ids), "phantoms have no occurrence")

    retained_base_ids = sorted(set(base_component) - phantom_components)
    need(len(retained_base_ids) == 68_500, "post-pruning base component count")
    dsu = DSU(retained_base_ids)

    # Exact endpoint sheet identity edges.
    sheet_edge_rows: list[dict[str, Any]] = []
    sheet_area_histogram: Counter[str] = Counter()
    sheet_area_sum = Fraction(0)
    sheet_pair_multiplicity: Counter[tuple[str, str]] = Counter()
    contact_chart_histogram: Counter[str] = Counter()
    for contact in sorted(rejected, key=lambda row: row["rejected_axis_face_contact_id"]):
        left_id = contact["left_source_partition_row_id"]
        right_id = contact["right_source_partition_row_id"]
        left_meta = selected235[left_id]
        right_meta = selected235[right_id]
        left_frontier = selected234[left_meta["Round234_frontier_row_id"]]
        right_frontier = selected234[right_meta["Round234_frontier_row_id"]]
        left_box = exact_box(left_frontier["box"], left_id)
        right_box = exact_box(right_frontier["box"], right_id)
        need(
            left_box[1] == right_box[0] == 0
            and left_box[0] < 0 < right_box[1],
            f"exact shared t=0 face:{contact['rejected_axis_face_contact_id']}",
        )
        need(
            left_meta["source_chart"] == right_meta["source_chart"]
            and left_meta["target_lift"] == right_meta["target_lift"]
            and left_meta["transition_event"] == right_meta["transition_event"]
            and left_meta["reason_label"] == right_meta["reason_label"],
            f"same endpoint identity data:{contact['rejected_axis_face_contact_id']}",
        )
        left_sheet = sheets_by_source[left_id]
        right_sheet = sheets_by_source[right_id]
        need(
            left_sheet["owner_signature_sha256"] == right_sheet["owner_signature_sha256"]
            and left_sheet["owner_official_key_id"] == right_sheet["owner_official_key_id"]
            and left_sheet["half_open_owner_rule"] == right_sheet["half_open_owner_rule"],
            f"same absent sheet signature:{contact['rejected_axis_face_contact_id']}",
        )
        common_rectangle, area = rectangle_intersection(
            left_sheet["exact_closed_base_rectangle"],
            right_sheet["exact_closed_base_rectangle"],
            contact["rejected_axis_face_contact_id"],
        )
        left_current = node_to_current[left_sheet["owner_wall_bulk_node_id"]]
        right_current = node_to_current[right_sheet["owner_wall_bulk_node_id"]]
        need(
            left_current != right_current
            and left_current not in phantom_components
            and right_current not in phantom_components
            and base_component[left_current]["official_key_id"]
            == base_component[right_current]["official_key_id"]
            == left_sheet["owner_official_key_id"],
            f"cross-component exact-key-pure sheet identity:{contact['rejected_axis_face_contact_id']}",
        )
        pair = tuple(sorted((left_current, right_current)))
        rank_reducing = dsu.union(*pair)
        sheet_pair_multiplicity[pair] += 1
        area_text = qtext(area)
        sheet_area_histogram[area_text] += 1
        sheet_area_sum += area
        contact_chart_histogram[left_meta["source_chart"]] += 1
        sheet_edge_rows.append(closed({
            "endpoint_sheet_identity_edge_row_id":
                "round264-endpoint-sheet-identity:" + digest([
                    contact["rejected_axis_face_contact_id"],
                    left_sheet["wall_sheet_node_id"],
                    right_sheet["wall_sheet_node_id"],
                ]),
            "source_Round252_rejected_axis_face_contact_id":
                contact["rejected_axis_face_contact_id"],
            "left_source_partition_row_id": left_id,
            "right_source_partition_row_id": right_id,
            "left_t0_sheet_node_id": left_sheet["wall_sheet_node_id"],
            "right_t0_sheet_node_id": right_sheet["wall_sheet_node_id"],
            "exact_shared_t_coordinate": "0",
            "source_chart": left_meta["source_chart"],
            "target_lift": left_meta["target_lift"],
            "transition_event": left_meta["transition_event"],
            "owner_signature_sha256": left_sheet["owner_signature_sha256"],
            "official_key_id": left_sheet["owner_official_key_id"],
            "half_open_owner_rule": left_sheet["half_open_owner_rule"],
            "left_exact_closed_base_rectangle":
                left_sheet["exact_closed_base_rectangle"],
            "right_exact_closed_base_rectangle":
                right_sheet["exact_closed_base_rectangle"],
            "exact_positive_area_common_refinement_rectangle": common_rectangle,
            "exact_positive_area_common_refinement_area": area_text,
            "pre_Round264_component_pair": list(pair),
            "edge_kind": "EXACT_SAME_PHYSICAL_T0_ENDPOINT_SHEET_IDENTITY",
            "rank_reducing_edge": rank_reducing,
            "component_union_credit": 1 if rank_reducing else 0,
            "maximality_credit": 0,
        }))
    sheet_edge_rows.sort(key=lambda row: row["endpoint_sheet_identity_edge_row_id"])
    need(sum(row["rank_reducing_edge"] for row in sheet_edge_rows) == 184, "184 sheet rank reductions")
    need(len(sheet_edge_rows) == 248, "248 exact sheet identity edges")
    need(dict(sorted(sheet_area_histogram.items())) == EXPECTED_AREA_HISTOGRAM, "sheet area histogram")
    need(sheet_area_sum == Fraction(123, 6400), "sheet common-refinement area sum")
    multiplicity_histogram = Counter(sheet_pair_multiplicity.values())
    need(
        {str(key): value for key, value in sorted(multiplicity_histogram.items())}
        == EXPECTED_SHEET_PAIR_MULTIPLICITY_HISTOGRAM,
        "sheet pair multiplicity histogram",
    )
    need(
        dict(sorted(contact_chart_histogram.items()))
        == {"G:E": 62, "G:N": 62, "G:S": 62, "G:W": 62},
        "contact chart histogram",
    )
    need(len({dsu.find(value) for value in retained_base_ids}) == 68_316, "post-sheet quotient")

    # Consume the Round204 EMPTY--EVENT--EMPTY tail glue rows and cross-check
    # their full dimensional lineage.
    round204 = load_result(ROUND204)
    tail_rows204 = check_closed_rows(
        round204["tail_pair_signature_glue_ledger"],
        "pair_glue_row_id",
        32,
    )
    open_rows204 = check_closed_rows(
        round204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    )
    open_by_id = {row["region_row_id"]: row for row in open_rows204}
    source_sheets = {
        row["sheet_row_id"]: row
        for row in round204["formal_2D_sheet_lineage"]["source_sheet_rows"]
    }
    target_sheets = {
        row["sheet_row_id"]: row
        for row in round204["formal_2D_sheet_lineage"]["target_sheet_rows"]
    }
    one_dimensional = {
        row["edge_row_id"]: row
        for row in round204["formal_1D_boundary_and_intersection_lineage"]["rows"]
    }
    tail_geometry = {
        row["tail_pair_row_id"]: row
        for row in round204["tail_geometry_evidence_ledger"]["pair_rows"]
    }
    tail_edge_rows: list[dict[str, Any]] = []
    tail_pairs: Counter[tuple[str, str]] = Counter()
    sheet_pair_set = set(sheet_pair_multiplicity)
    for row in sorted(tail_rows204, key=lambda item: item["pair_glue_row_id"]):
        need(
            row["pair_glue_status"] == "UNIQUE_EXPECTED_EMPTY_EVENT_EMPTY"
            and row["materialized_local_open_region_count"] == 3
            and len(row["outer_empty_region_row_ids"]) == 2
            and row["unexpected_signature_change_count"] == 0,
            f"Round204 tail glue contract:{row['pair_glue_row_id']}",
        )
        outer = [open_by_id[value] for value in row["outer_empty_region_row_ids"]]
        need(
            all(
                item["graph_classification"] == "RESIDUAL_3D"
                and item["signed_wall_word"] == []
                and item["wall_crossing_count"] == 0
                and item["tail_region"] is True
                and item["region_kind"] in {
                    "TAIL_BOUNDARY_ONLY_SINGLE_REGION",
                    "TAIL_TARGET_GRAPH_SAME_SIGN_OUTER_REGION",
                }
                and item["strict_open_region"] is True
                and item["positive_coordinate_volume"] is True
                and item["official_key_id"] == row["outer_empty_official_key_id"]
                for item in outer
            ),
            f"Round204 outer empty regions:{row['pair_glue_row_id']}",
        )
        source_sheet = source_sheets[row["source_sheet_2D_row_id"]]
        target_sheet = target_sheets[row["target_sheet_2D_row_id"]]
        intersection = one_dimensional[row["source_target_intersection_1D_row_id"]]
        geometry = tail_geometry[row["tail_pair_row_id"]]
        need(
            source_sheet["ambient_dimension"] == 2
            and source_sheet["source_wall_factor_exact"] == "(9/25)*t"
            and source_sheet["source_wall_factor_exact_zero_set"] == "t=0"
            and row["source_target_intersection_1D_row_id"]
            in source_sheet["source_target_intersection_1D_row_ids"]
            and target_sheet["ambient_dimension"] == 2
            and target_sheet["exact_source_target_intersection_on_p0_boundary"] is True
            and row["source_target_intersection_1D_row_id"]
            in target_sheet["source_target_intersection_1D_row_ids"]
            and intersection["ambient_dimension"] == 1
            and intersection["exact_source_target_intersection"] is True
            and set((row["source_sheet_2D_row_id"], row["target_sheet_2D_row_id"]))
            <= set(intersection["incident_sheet_row_ids"])
            and geometry["common_t0_face_byte_for_byte_equal"] is True
            and geometry["local_lineage_materialized"] is True
            and geometry["negative_t_leaf_row_id"] == row["negative_t_leaf_row_id"]
            and geometry["positive_t_leaf_row_id"] == row["positive_t_leaf_row_id"],
            f"Round204 3D/2D/1D/tail cross-check:{row['pair_glue_row_id']}",
        )
        occurrence_ids = row["outer_empty_region_row_ids"]
        need(all(value in base_occurrence for value in occurrence_ids), f"tail occurrence frontier:{row['pair_glue_row_id']}")
        components = tuple(sorted(
            base_occurrence[value]["current_component_id"] for value in occurrence_ids
        ))
        need(
            components[0] != components[1]
            and components[0] not in phantom_components
            and components[1] not in phantom_components
            and base_component[components[0]]["official_key_id"]
            == base_component[components[1]]["official_key_id"]
            == row["outer_empty_official_key_id"],
            f"tail exact-key-pure current pair:{row['pair_glue_row_id']}",
        )
        need(components not in sheet_pair_set, f"edge-family pair disjoint:{row['pair_glue_row_id']}")
        rank_reducing = dsu.union(*components)
        tail_pairs[components] += 1
        tail_edge_rows.append(closed({
            "Round204_tail_glue_closure_edge_row_id":
                "round264-Round204-tail-glue:" + digest([row["pair_glue_row_id"]]),
            "source_Round204_pair_glue_row_id": row["pair_glue_row_id"],
            "source_Round204_tail_pair_row_id": row["tail_pair_row_id"],
            "outer_empty_region_row_ids": occurrence_ids,
            "outer_empty_official_key_id": row["outer_empty_official_key_id"],
            "source_sheet_2D_row_id": row["source_sheet_2D_row_id"],
            "target_sheet_2D_row_id": row["target_sheet_2D_row_id"],
            "source_target_intersection_1D_row_id":
                row["source_target_intersection_1D_row_id"],
            "source_sheet_exact_base_rectangle":
                source_sheet["base_p_s_exact_bounds"],
            "target_sheet_exact_base_rectangle":
                target_sheet["base_p_s_exact_bounds"],
            "exact_1D_intersection_geometry_key": intersection["geometry_key"],
            "pre_Round264_component_pair": list(components),
            "edge_kind":
                "ROUND204_MATERIALIZED_EMPTY_EVENT_EMPTY_TAIL_GLUE",
            "rank_reducing_edge": rank_reducing,
            "component_union_credit": 1 if rank_reducing else 0,
            "maximality_credit": 0,
        }))
    tail_edge_rows.sort(key=lambda row: row["Round204_tail_glue_closure_edge_row_id"])
    need(len(tail_pairs) == 4 and set(tail_pairs.values()) == {8}, "four tail pairs times eight")
    need(sum(row["rank_reducing_edge"] for row in tail_edge_rows) == 4, "four tail rank reductions")
    need(len({dsu.find(value) for value in retained_base_ids}) == 68_312, "final corrected quotient")
    del round204, tail_rows204, open_rows204, open_by_id
    gc.collect()

    # Corrected constituent descriptors make the new IDs sensitive to every
    # removed empty node and every invalid owner edge, while phantom
    # components are absent from the descriptor universe entirely.
    descriptor_by_base: dict[str, dict[str, Any]] = {}
    for component_id in retained_base_ids:
        descriptor_by_base[component_id] = {
            "post_Round262_quotient_component_id": component_id,
            "source_Round262_component_row_id":
                base_component[component_id]["source_row_id"],
            "source_Round262_component_row_sha256":
                base_component[component_id]["source_row_sha256"],
            "removed_empty_bulk_node_ids":
                sorted(removed_nodes_by_component.get(component_id, [])),
            "removed_invalid_Round248_owner_edge_ids":
                sorted(invalid_owner_edges_by_component.get(component_id, [])),
            "retained_exact_t0_endpoint_sheet_node_ids":
                sorted(retained_sheets_by_component.get(component_id, [])),
        }

    classes: dict[str, list[str]] = defaultdict(list)
    for component_id in retained_base_ids:
        classes[dsu.find(component_id)].append(component_id)
    need(len(classes) == 68_312, "corrected DSU class count")
    post_id_by_base: dict[str, str] = {}
    class_descriptors: dict[str, tuple[str, list[dict[str, Any]]]] = {}
    for root, members in classes.items():
        members.sort()
        descriptors = [descriptor_by_base[value] for value in members]
        post_id = "round264-corrected-component:" + digest(descriptors)
        need(post_id not in class_descriptors, f"unique post component id:{post_id}")
        class_descriptors[post_id] = (root, descriptors)
        for value in members:
            post_id_by_base[value] = post_id

    # Full corrected occurrence frontier.
    occurrence_rows: list[dict[str, Any]] = []
    occurrence_count_by_post: Counter[str] = Counter()
    occurrence_count_by_key: Counter[str] = Counter()
    for occurrence_id in sorted(base_occurrence):
        item = base_occurrence[occurrence_id]
        current_id = item["current_component_id"]
        need(current_id not in phantom_components, f"occurrence not assigned to phantom:{occurrence_id}")
        post_id = post_id_by_base[current_id]
        occurrence_count_by_post[post_id] += 1
        occurrence_count_by_key[item["official_key_id"]] += 1
        occurrence_rows.append(closed({
            "post_Round264_occurrence_frontier_row_id":
                "round264-occurrence-frontier:" + digest([occurrence_id]),
            "local_occurrence_row_id": occurrence_id,
            "official_key_id": item["official_key_id"],
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round262_occurrence_frontier_row_id": item["source_row_id"],
            "source_Round262_occurrence_frontier_row_sha256":
                item["source_row_sha256"],
            "post_Round262_quotient_component_id": current_id,
            "post_Round264_quotient_component_id": post_id,
            "corrected_quotient_assignment_credit": 1,
            "maximal_physical_component_assignment_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    need(len(occurrence_rows) == 53_968, "complete corrected occurrence frontier")

    # Full 133,284-node corrected virtual frontier.
    virtual_rows: list[dict[str, Any]] = []
    virtual_count_by_post: Counter[str] = Counter()
    virtual_count_by_key: Counter[str] = Counter()
    virtual_kind_histogram: Counter[str] = Counter()
    for node_id in sorted(node_to_252):
        if node_id in empty_nodes:
            continue
        current_id = node_to_current[node_id]
        need(current_id not in phantom_components, f"valid virtual node not phantom:{node_id}")
        post_id = post_id_by_base[current_id]
        if node_id.startswith("round248-wall-bulk:"):
            kind = "ROUND248_WALL_BULK"
        elif node_id.startswith("round248-wall-sheet:"):
            kind = "ROUND248_WALL_SHEET"
        else:
            kind = "INHERITED_ROUND247_VIRTUAL_STRATUM"
        key_id = base_component[current_id]["official_key_id"]
        virtual_count_by_post[post_id] += 1
        virtual_count_by_key[key_id] += 1
        virtual_kind_histogram[kind] += 1
        virtual_rows.append(closed({
            "post_Round264_valid_virtual_node_frontier_row_id":
                "round264-valid-virtual-node:" + digest([node_id]),
            "valid_virtual_stratum_node_id": node_id,
            "virtual_node_kind": kind,
            "source_Round252_mixed_sheet_quotient_component_id":
                node_to_252[node_id],
            "post_Round262_quotient_component_id": current_id,
            "post_Round264_quotient_component_id": post_id,
            "official_key_id": key_id,
            "valid_after_endpoint_empty_branch_correction": True,
            "maximality_credit": 0,
        }))
    need(len(virtual_rows) == 133_284, "complete valid virtual-node frontier")

    sheet_edge_count_by_post: Counter[str] = Counter()
    sheet_rank_count_by_post: Counter[str] = Counter()
    for row in sheet_edge_rows:
        post_id = post_id_by_base[row["pre_Round264_component_pair"][0]]
        need(
            post_id == post_id_by_base[row["pre_Round264_component_pair"][1]],
            "sheet edge post assignment",
        )
        sheet_edge_count_by_post[post_id] += 1
        sheet_rank_count_by_post[post_id] += int(row["rank_reducing_edge"])
    tail_edge_count_by_post: Counter[str] = Counter()
    tail_rank_count_by_post: Counter[str] = Counter()
    for row in tail_edge_rows:
        post_id = post_id_by_base[row["pre_Round264_component_pair"][0]]
        need(
            post_id == post_id_by_base[row["pre_Round264_component_pair"][1]],
            "tail edge post assignment",
        )
        tail_edge_count_by_post[post_id] += 1
        tail_rank_count_by_post[post_id] += int(row["rank_reducing_edge"])

    component_rows: list[dict[str, Any]] = []
    component_count_by_key: Counter[str] = Counter()
    B_count_by_key: Counter[str] = Counter()
    Z_count_by_key: Counter[str] = Counter()
    class_size_histogram: Counter[int] = Counter()
    for post_id in sorted(class_descriptors):
        _, descriptors = class_descriptors[post_id]
        members = [
            descriptor["post_Round262_quotient_component_id"]
            for descriptor in descriptors
        ]
        keys = {base_component[value]["official_key_id"] for value in members}
        ordinals = {base_component[value]["official_key_ordinal"] for value in members}
        need(len(keys) == len(ordinals) == 1, f"post exact-key purity:{post_id}")
        key_id = next(iter(keys))
        ordinal = next(iter(ordinals))
        occurrence_count = occurrence_count_by_post[post_id]
        component_class = "B_OCCURRENCE_BEARING" if occurrence_count else "Z_ZERO_OCCURRENCE_CARRIER"
        component_count_by_key[key_id] += 1
        (B_count_by_key if occurrence_count else Z_count_by_key)[key_id] += 1
        class_size_histogram[len(members)] += 1
        component_rows.append(closed({
            "post_Round264_component_frontier_row_id":
                "round264-component-row:" + digest([post_id]),
            "post_Round264_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "corrected_constituent_descriptor_count": len(descriptors),
            "corrected_constituent_descriptors_sha256": digest(descriptors),
            "corrected_constituent_descriptors": descriptors,
            "constituent_Round262_component_ids": members,
            "constituent_Round262_component_ids_sha256": digest(members),
            "removed_empty_bulk_node_count":
                sum(len(item["removed_empty_bulk_node_ids"]) for item in descriptors),
            "removed_invalid_Round248_owner_edge_count":
                sum(len(item["removed_invalid_Round248_owner_edge_ids"]) for item in descriptors),
            "retained_exact_t0_endpoint_sheet_count":
                sum(len(item["retained_exact_t0_endpoint_sheet_node_ids"]) for item in descriptors),
            "endpoint_sheet_identity_edge_count": sheet_edge_count_by_post[post_id],
            "endpoint_sheet_identity_rank_reduction_count":
                sheet_rank_count_by_post[post_id],
            "Round204_tail_glue_edge_count": tail_edge_count_by_post[post_id],
            "Round204_tail_glue_rank_reduction_count":
                tail_rank_count_by_post[post_id],
            "local_occurrence_count": occurrence_count,
            "valid_virtual_stratum_node_count": virtual_count_by_post[post_id],
            "component_class": component_class,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    need(len(component_rows) == 68_312, "complete corrected component frontier")
    B_count = sum(occurrence_count_by_post[post_id] > 0 for post_id in class_descriptors)
    Z_count = len(class_descriptors) - B_count
    need((B_count, Z_count) == (10_904, 57_408), "B/Z corrected component census")

    # Full old-to-new correction map, including explicit DROP_EMPTY rows.
    component_map_rows: list[dict[str, Any]] = []
    for current_id in sorted(base_component):
        if current_id in phantom_components:
            disposition = "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT"
            post_id: str | None = None
        elif removed_nodes_by_component.get(current_id):
            disposition = "PRUNE_EMPTY_ABSENT_NODE_AND_INVALID_EDGE__RETAIN_SHEET"
            post_id = post_id_by_base[current_id]
        else:
            disposition = "RETAIN_AND_REQUOTIENT_BY_CERTIFIED_LOWER_DIMENSIONAL_EDGES"
            post_id = post_id_by_base[current_id]
        component_map_rows.append(closed({
            "Round262_to_Round264_component_correction_map_row_id":
                "round264-component-map:" + digest([current_id]),
            "post_Round262_quotient_component_id": current_id,
            "official_key_id": base_component[current_id]["official_key_id"],
            "source_Round262_component_row_id":
                base_component[current_id]["source_row_id"],
            "source_Round262_component_row_sha256":
                base_component[current_id]["source_row_sha256"],
            "removed_empty_bulk_node_ids":
                sorted(removed_nodes_by_component.get(current_id, [])),
            "removed_invalid_Round248_owner_edge_ids":
                sorted(invalid_owner_edges_by_component.get(current_id, [])),
            "retained_exact_t0_endpoint_sheet_node_ids":
                sorted(retained_sheets_by_component.get(current_id, [])),
            "component_correction_disposition": disposition,
            "post_Round264_quotient_component_id": post_id,
            "component_count_credit": -1 if post_id is None else 0,
            "maximality_credit": 0,
        }))
    need(len(component_map_rows) == 68_716, "complete component correction map")

    # Complete exact-key frontier with exact reduction conservation.
    key_rows: list[dict[str, Any]] = []
    reduction_histogram: Counter[int] = Counter()
    total_reduction_histogram: Counter[int] = Counter()
    phantom_count_by_key: Counter[str] = Counter(
        base_component[component_id]["official_key_id"]
        for component_id in phantom_components
    )
    for key_id in sorted(base_key):
        item = base_key[key_id]
        post_count = component_count_by_key[key_id]
        post_pruning_count = (
            item["pre_component_count"] - phantom_count_by_key[key_id]
        )
        reduction = post_pruning_count - post_count
        total_reduction = item["pre_component_count"] - post_count
        need(
            occurrence_count_by_key[key_id] == item["occurrence_count"],
            f"occurrence key conservation:{key_id}",
        )
        reduction_histogram[reduction] += 1
        total_reduction_histogram[total_reduction] += 1
        key_rows.append(closed({
            "post_Round264_key_frontier_row_id":
                "round264-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round262_key_frontier_row_id": item["source_row_id"],
            "source_Round262_key_frontier_row_sha256": item["source_row_sha256"],
            "local_occurrence_count": occurrence_count_by_key[key_id],
            "valid_virtual_stratum_node_count": virtual_count_by_key[key_id],
            "post_Round262_quotient_component_count": item["pre_component_count"],
            "dropped_empty_EVENT_PRESENT_singleton_component_count":
                phantom_count_by_key[key_id],
            "post_empty_branch_pruning_component_count": post_pruning_count,
            "post_Round264_quotient_component_count": post_count,
            "lower_dimensional_glue_rank_reduction": reduction,
            "total_Round262_to_Round264_component_reduction": total_reduction,
            "post_Round264_B_occurrence_bearing_component_count":
                B_count_by_key[key_id],
            "post_Round264_Z_zero_occurrence_carrier_component_count":
                Z_count_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    need(
        {str(key): value for key, value in sorted(reduction_histogram.items())}
        == EXPECTED_KEY_REDUCTION_HISTOGRAM,
        "per-key reduction histogram",
    )
    need(
        total_reduction_histogram[0] == 40
        and sum(
            value
            for key, value in total_reduction_histogram.items()
            if key > 0
        ) == 76,
        "total changed/unchanged key census",
    )
    need(sum(component_count_by_key.values()) == 68_312, "component/key conservation")
    need(sum(occurrence_count_by_key.values()) == 53_968, "occurrence/key conservation")
    need(sum(virtual_count_by_key.values()) == 133_284, "virtual/key conservation")

    class_size_text = {
        str(key): value for key, value in sorted(class_size_histogram.items())
    }
    virtual_kind_text = dict(sorted(virtual_kind_histogram.items()))
    need(sum(virtual_kind_histogram.values()) == 133_284, "virtual kind census")

    census = {
        "Round252_residual_t_face_contact_count": 248,
        "unique_Round235_endpoint_cell_count": 400,
        "empty_endpoint_bulk_node_count": 400,
        "empty_EVENT_ABSENT_bulk_node_count": 184,
        "empty_EVENT_PRESENT_bulk_node_count": 216,
        "invalid_Round248_sheet_owner_edge_count": 184,
        "dropped_empty_EVENT_PRESENT_singleton_component_count": 216,
        "pre_Round264_component_count": 68_716,
        "post_empty_branch_pruning_component_count": 68_500,
        "endpoint_sheet_identity_edge_count": 248,
        "endpoint_sheet_identity_rank_reduction_count": 184,
        "endpoint_sheet_identity_redundant_edge_count": 64,
        "endpoint_sheet_distinct_current_pair_count": 184,
        "endpoint_sheet_current_pair_multiplicity_histogram":
            EXPECTED_SHEET_PAIR_MULTIPLICITY_HISTOGRAM,
        "endpoint_sheet_exact_common_area_histogram": EXPECTED_AREA_HISTOGRAM,
        "endpoint_sheet_exact_common_area_sum": "123/6400",
        "post_endpoint_sheet_identity_component_count": 68_316,
        "Round204_tail_glue_edge_count": 32,
        "Round204_tail_glue_distinct_current_pair_count": 4,
        "Round204_tail_glue_rank_reduction_count": 4,
        "Round204_tail_glue_redundant_edge_count": 28,
        "post_Round264_component_count": 68_312,
        "post_Round264_B_occurrence_bearing_component_count": B_count,
        "post_Round264_Z_zero_occurrence_carrier_component_count": Z_count,
        "post_Round264_component_class_size_histogram": class_size_text,
        "complete_occurrence_frontier_count": 53_968,
        "complete_exact_key_frontier_count": 116,
        "complete_valid_virtual_node_frontier_count": 133_284,
        "valid_virtual_node_kind_histogram": virtual_kind_text,
        "per_key_lower_dimensional_glue_rank_reduction_histogram":
            EXPECTED_KEY_REDUCTION_HISTOGRAM,
        "per_key_total_Round262_to_Round264_component_reduction_histogram": {
            str(key): value
            for key, value in sorted(total_reduction_histogram.items())
        },
        "lower_dimensional_glue_compressed_exact_key_count": 36,
        "lower_dimensional_glue_unchanged_exact_key_count": 80,
        "total_Round262_to_Round264_changed_exact_key_count": 76,
        "total_Round262_to_Round264_unchanged_exact_key_count": 40,
        "maximal_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_SOURCE_G_LOWER_DIMENSIONAL_ENDPOINT_COVER_CORRECTION__"
            "400_EMPTY_BULKS_REMOVED__248_ENDPOINT_SHEET_IDENTITIES_AND_"
            "32_ROUND204_TAIL_GLUES_CLOSED__POST_ROUND264_COMPONENTS_68312"
        ),
        "formal_input_binding": input_binding(),
        "formal_endpoint_empty_branch_correction_disposition_ledger": ledger(
            correction_rows,
            "endpoint_empty_branch_disposition_row_id",
        ),
        "formal_endpoint_sheet_identity_common_refinement_ledger": ledger(
            sheet_edge_rows,
            "endpoint_sheet_identity_edge_row_id",
        ),
        "formal_Round204_tail_pair_glue_closure_ledger": ledger(
            tail_edge_rows,
            "Round204_tail_glue_closure_edge_row_id",
        ),
        "formal_Round262_to_Round264_component_correction_map_ledger": ledger(
            component_map_rows,
            "Round262_to_Round264_component_correction_map_row_id",
        ),
        "formal_post_Round264_component_frontier_ledger": ledger(
            component_rows,
            "post_Round264_component_frontier_row_id",
        ),
        "formal_post_Round264_occurrence_frontier_ledger": ledger(
            occurrence_rows,
            "post_Round264_occurrence_frontier_row_id",
        ),
        "formal_post_Round264_key_frontier_ledger": ledger(
            key_rows,
            "post_Round264_key_frontier_row_id",
        ),
        "formal_post_Round264_valid_virtual_node_frontier_ledger": ledger(
            virtual_rows,
            "post_Round264_valid_virtual_node_frontier_row_id",
        ),
        "census": census,
        "scope_contract": {
            "all_248_Round252_t_face_residuals_exactly_revisited": True,
            "all_400_distinct_Round235_endpoint_cells_exactly_classified": True,
            "source_G_relevant_coordinate_is_exactly_9_over_25_times_t": True,
            "source_G_chart_axis_rule":
                "G:E,G:W->source_y=0__G:N,G:S->source_x=0",
            "all_400_empty_branch_bulks_have_exact_zero_physical_support": True,
            "all_400_empty_nodes_have_zero_Round250_Round251_Round252_accepted_edge_incidence": True,
            "all_216_empty_EVENT_PRESENT_components_are_singleton_phantoms": True,
            "all_184_invalid_EVENT_ABSENT_owner_edges_are_removed_but_sheets_retained": True,
            "all_248_endpoint_sheet_pairs_have_exact_positive_area_identity_common_refinement": True,
            "all_32_Round204_tail_glues_cross_checked_through_3D_2D_1D_lineage": True,
            "endpoint_sheet_and_Round204_tail_edge_families_have_disjoint_pre_component_pairs": True,
            "complete_component_occurrence_key_and_valid_virtual_node_frontiers_rebuilt": True,
            "post_component_ids_are_based_on_corrected_constituent_descriptors_without_phantoms": True,
            "component_maximality_not_proved": True,
            "exact_key_fibre_exhaustion_not_proved": True,
        },
        "strict_nonpromotion": {
            "certified_lower_dimensional_identity_or_glue_edge_count": 280,
            "new_component_union_credit": 188,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "audit every remaining attachment channel against the corrected "
            "68,312-component and 133,284-valid-virtual-node frontiers, prove "
            "physical component maximality, then exhaust all 116 exact-key "
            "fibres without granting Jx/Jy same-point glue credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "fractions.Fraction exact rational",
            "seed_affects_output": False,
        },
    }


def safe_write(data: bytes) -> None:
    need(OUTPUT.parent == HERE, "output parent")
    if OUTPUT.exists() or OUTPUT.is_symlink():
        information = OUTPUT.lstat()
        need(
            stat.S_ISREG(information.st_mode)
            and not OUTPUT.is_symlink()
            and information.st_nlink == 1,
            "safe existing output",
        )
    descriptor, name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
        directory_descriptor = os.open(
            HERE,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=264_071)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    need(
        isinstance(arguments.seed, int) and not isinstance(arguments.seed, bool),
        "integral seed",
    )
    producer_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__).resolve(), 5_000_000)
    ).hexdigest()
    result = build(producer_sha256)
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    encoded = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"producer_sha256={producer_sha256}")
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(
        "empty_nodes=400 phantom_components=216 invalid_owner_edges=184 "
        "sheet_edges=248(184+64) tail_edges=32(4+28)"
    )
    print(
        "post_Round264_components=68312 B/Z=10904/57408 "
        "frontiers=53968/116/133284 strict_nonpromotion=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
