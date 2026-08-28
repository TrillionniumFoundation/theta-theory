#!/usr/bin/env python3
"""Independent verifier for the CM2 Round264 endpoint correction package.

The verifier never imports or executes the Round264 producer.  It pins the
producer only as inert bytes and reconstructs the complete expected Round264
result from the frozen Round204/234/235/248/250/251/252/254/258--263
certificates before opening the candidate certificate.
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
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
PRODUCER_SHA256 = (
    "72eb667b7f98fc6ed10f8617b8f8a289c4cc127b494b8777fa4cb1d99dace34c"
)
CANDIDATE_SHA256 = (
    "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"
)
CANDIDATE_RESULT_SHA256 = (
    "712a4eeae512e6370c642635a6d80090c15789612cb1745d0844282cc02f9ae1"
)
CANDIDATE_SCHEMA = (
    "cm2.round264.source-g-lower-dimensional-endpoint-correction-"
    "and-glue-closure.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round264.source-g-lower-dimensional-endpoint-correction-"
    "and-glue-closure-verification.v1"
)

R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R234 = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R235 = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R250 = "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
R251 = "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
R252 = "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json"
R254 = "cm2_round254_source_g_seed_block_quotient_closure_certificate.json"
R258 = "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
R259 = "cm2_round259_source_g_curved_region_full_face_saturation_certificate.json"
R260 = "cm2_round260_source_g_curved_region_common_face_refinement_certificate.json"
R261 = "cm2_round261_source_g_adaptive_common_face_strict_separation_certificate.json"
R262 = "cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json"
R263 = "cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion_certificate.json"

UPSTREAM = {
    R204: (
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
    ),
    R234: (
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
        "d05d6bbc590157e855a577f411668d0f3b7486ccdbea8e47ed30299194b5ba08",
        "cm2.round234.source-g-wall-endpoint-order-depth6-materialization.v1",
    ),
    R235: (
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
        "5bbcf6780338c9a40fa9c131b0270e4fb934de022cf597d2f82d6b85af68dca2",
        "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1",
    ),
    R248: (
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
        "d3dc5783fcaaa308f069e1be232a9b96eeb8b0efc5a4df6cbee70d110d7df1e9",
        "cm2.round248.source-g-wall-finite-key-retained-quotient.v1",
    ),
    R250: (
        "07eb8ab4f5fbcec7df4a891f3e55b3990c8400a01bbbff8950f05519e886ca8a",
        "b20244ff28ef3f545977ac2bc9f2afa496be1aee414acc779f11a6486d4421dc",
        "cm2.round250.source-g-wall-t-chain-patch-saturation.v1",
    ),
    R251: (
        "a1f1d04466585cc8b97fceaa98c1507b293696933af4a58dea3c76d92a0c480f",
        "712a2666ca5db31fcbd047dfc7556402d92d38a3258407bc844601f4a3f1d3a4",
        "cm2.round251.source-g-wall-p-face-patch-saturation.v1",
    ),
    R252: (
        "8ffc927ca3bcefc48581bdb8b66c00f95c302f737692d14ba4cc6dc2e1ad7794",
        "af41bdfa496ff9411a472f258f8be5234d3d11b3fcff0273fa186192aa591f4c",
        "cm2.round252.source-g-wall-s-t-face-patch-saturation.v1",
    ),
    R254: (
        "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf",
        "202544c68006f271152d18dc64a56d36cbfd3f67ebf679eb9104784b06109766",
        "cm2.round254.source-g-seed-block-quotient-closure.v1",
    ),
    R258: (
        "11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb",
        "257c999bb77d1f9e8993898ec2a51675e83e27879b750a160b515a60bb1e13a8",
        "cm2.round258.source-g-whole-box-boundary-face-saturation.v1",
    ),
    R259: (
        "799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039",
        "03f3542ba4d51e6938d098b6822ea76a8ec6225e9bf590e1a96a7c5c67f8eba3",
        "cm2.round259.source-g-curved-region-full-face-saturation.v1",
    ),
    R260: (
        "a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b",
        "5b3d3ec045c5ef5baa9cab9838b019a583ec4077b0867cce2a5c151131ba2f09",
        "cm2.round260.source-g-curved-region-common-face-refinement.v1",
    ),
    R261: (
        "6b69453c869d07737152c851d7716434dca16184433ef8be9023cb56027b162c",
        "5a7ee517842aeec8be03acd1152015560d9abbdf2a54d6e9eb7d0d46d772048a",
        "cm2.round261.source-g-adaptive-common-face-strict-separation.v1",
    ),
    R262: (
        "d9cac69017dd3247428492bdee6402da9868a7d97db3574f41ba25a1b49005de",
        "33d54f038b066d66119bb401c98a0a34b308743ba81932b5693e7a9e69238d6e",
        "cm2.round262.source-g-monotone-deep-common-face-closure.v1",
    ),
    R263: (
        "e6c524db031ce3cac88fece6ca874e9b47290d345e8abe21736697c7dc4fb54c",
        "8e10297d0091abcf9d5bfecf7bd6c6fcb74a3166e06a5c4f1c661ecc92f2ed33",
        "cm2.round263.source-g-complete-occurrence-cross-chart-transition-exhaustion.v1",
    ),
}

AREA_HISTOGRAM = {
    "1/102400": 48,
    "1/51200": 16,
    "1/25600": 40,
    "1/12800": 88,
    "1/6400": 48,
    "1/3200": 8,
}
KEY_REDUCTION_HISTOGRAM = {"0": 80, "2": 24, "4": 8, "27": 4}
PAIR_MULTIPLICITY_HISTOGRAM = {"1": 144, "2": 32, "5": 8}


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationFailure(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded_chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


def encoded(value: Any) -> bytes:
    return b"".join(encoded_chunks(value))


def fingerprint(value: Any) -> str:
    state = hashlib.sha256()
    for piece in encoded_chunks(value):
        state.update(piece)
    return state.hexdigest()


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def seal(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    require("row_sha256" not in result, "row closure field absent")
    result["row_sha256"] = fingerprint(result)
    return result


def make_ledger(rows: list[dict[str, Any]], identity: str) -> dict[str, Any]:
    require(
        len(rows) == len({row[identity] for row in rows}),
        f"unique output ledger identity:{identity}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": fingerprint(rows),
        "row_ids_sha256": fingerprint([row[identity] for row in rows]),
        "row_hashes_sha256": fingerprint([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def guarded_read(
    path: Path,
    maximum: int,
    required_parent: Path | None = HERE,
) -> bytes:
    if required_parent is not None:
        require(path.parent == required_parent, f"input parent:{path.name}")
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"regular nonlinked input:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable open:{path.name}",
        )
        pieces: list[bytes] = []
        total = 0
        while True:
            piece = os.read(descriptor, 1024 * 1024)
            if not piece:
                break
            total += len(piece)
            require(total <= maximum, f"bounded read:{path.name}")
            pieces.append(piece)
        after = os.fstat(descriptor)
        require(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable read:{path.name}",
        )
        return b"".join(pieces)
    finally:
        os.close(descriptor)


def parse_strict(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict encoding:{label}",
    )

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key:{label}:{key}")
            result[key] = value
        return result

    def reject_number(token: str) -> None:
        raise VerificationFailure(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationFailure(f"strict JSON:{label}") from error
    require(isinstance(value, dict), f"top-level JSON object:{label}")
    return value


def upstream_result(name: str) -> dict[str, Any]:
    file_hash, result_hash, schema = UPSTREAM[name]
    raw = guarded_read(HERE / name, 800_000_000)
    require(hashlib.sha256(raw).hexdigest() == file_hash, f"upstream file pin:{name}")
    document = parse_strict(raw, name)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"upstream envelope:{name}",
    )
    require(document["schema"] == schema, f"upstream schema:{name}")
    require(
        document["result_sha256"] == result_hash
        and fingerprint(document["result"]) == result_hash,
        f"upstream result pin:{name}",
    )
    require(isinstance(document["result"], dict), f"upstream result object:{name}")
    return document["result"]


def closed_rows(
    table: dict[str, Any],
    identity: str,
    expected: int | None = None,
) -> list[dict[str, Any]]:
    rows = table["rows"]
    require(isinstance(rows, list), f"ledger rows:{identity}")
    require(table["row_count"] == len(rows), f"ledger count:{identity}")
    if expected is not None:
        require(len(rows) == expected, f"expected count:{identity}")
    require(
        len(rows) == len({row[identity] for row in rows}),
        f"unique ledger identity:{identity}",
    )
    require(table["rows_sha256"] == fingerprint(rows), f"rows digest:{identity}")
    for row in rows:
        body = dict(row)
        closure = body.pop("row_sha256")
        require(closure == fingerprint(body), f"row closure:{identity}")
    return rows


def plain_rows(
    result: dict[str, Any],
    field: str,
    hash_field: str,
) -> list[dict[str, Any]]:
    rows = result[field]
    require(isinstance(rows, list), f"plain rows:{field}")
    require(result[hash_field] == fingerprint(rows), f"plain digest:{field}")
    return rows


def expected_input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": values[0],
            "result_sha256": values[1],
            "schema": values[2],
        }
        for name, values in sorted(UPSTREAM.items())
    }


class UnionFind:
    def __init__(self, values: Iterable[str]) -> None:
        members = list(values)
        self.parent = {value: value for value in members}
        self.weight = {value: 1 for value in members}

    def root(self, value: str) -> str:
        require(value in self.parent, f"union member:{value}")
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            following = self.parent[value]
            self.parent[value] = root
            value = following
        return root

    def join(self, left: str, right: str) -> bool:
        a, b = self.root(left), self.root(right)
        if a == b:
            return False
        if self.weight[a] < self.weight[b] or (
            self.weight[a] == self.weight[b] and a > b
        ):
            a, b = b, a
        self.parent[b] = a
        self.weight[a] += self.weight[b]
        return True


def rational_box(values: Any, label: str) -> tuple[Fraction, ...]:
    require(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"box encoding:{label}",
    )
    try:
        result = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationFailure(f"rational box:{label}") from error
    require(
        all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        f"positive box:{label}",
    )
    return result


def common_rectangle(
    left: list[str],
    right: list[str],
    label: str,
) -> tuple[list[str], Fraction]:
    require(len(left) == len(right) == 4, f"rectangle encoding:{label}")
    a = [Fraction(value) for value in left]
    b = [Fraction(value) for value in right]
    bounds = [
        max(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        min(a[3], b[3]),
    ]
    area = (bounds[1] - bounds[0]) * (bounds[3] - bounds[2])
    require(area > 0, f"positive common rectangle:{label}")
    return [fraction_text(value) for value in bounds], area


def quotient_lineage_maps() -> list[dict[str, str]]:
    result254 = upstream_result(R254)
    rows254 = closed_rows(
        result254["formal_Round252_to_Round254_component_map_ledger"],
        "Round252_to_Round254_component_map_id",
    )
    maps: list[dict[str, str]] = [{
        row["Round252_mixed_sheet_quotient_component_id"]:
            row["post_Round254_mixed_sheet_quotient_component_id"]
        for row in rows254
    }]
    del result254, rows254
    gc.collect()

    specifications = (
        (
            R258,
            "formal_Round257_to_Round258_component_map_ledger",
            "Round257_quotient_component_id",
            "post_Round258_quotient_component_id",
            "Round257_to_Round258_component_map_row_id",
        ),
        (
            R259,
            "formal_Round258_to_Round259_component_map_ledger",
            "Round258_quotient_component_id",
            "post_Round259_quotient_component_id",
            "Round258_to_Round259_component_map_row_id",
        ),
        (
            R260,
            "formal_Round259_to_Round260_component_map_ledger",
            "Round259_quotient_component_id",
            "post_Round260_quotient_component_id",
            "Round259_to_Round260_component_map_row_id",
        ),
        (
            R261,
            "formal_Round260_to_Round261_component_map_ledger",
            "Round260_quotient_component_id",
            "post_Round261_quotient_component_id",
            "Round260_to_Round261_component_map_row_id",
        ),
        (
            R262,
            "formal_Round261_to_Round262_component_map_ledger",
            "Round261_quotient_component_id",
            "post_Round262_quotient_component_id",
            "Round261_to_Round262_component_map_row_id",
        ),
    )
    for name, table, old_field, new_field, identity in specifications:
        result = upstream_result(name)
        rows = closed_rows(result[table], identity)
        mapping = {row[old_field]: row[new_field] for row in rows}
        require(len(mapping) == len(rows), f"lineage function:{name}")
        maps.append(mapping)
        del result, rows
        gc.collect()
    return maps


def reconstruct_expected() -> dict[str, Any]:
    # Recover the complete Round252 residual and virtual-node universes.
    result252 = upstream_result(R252)
    residuals = closed_rows(
        result252["formal_rejected_axis_face_contact_ledger"],
        "rejected_axis_face_contact_id",
        248,
    )
    require(
        all(
            row["face_axis"] == "t"
            and row["shared_full_return_signature_count"] == 2
            and row["physical_glue_credit"] == 0
            for row in residuals
        ),
        "Round252 residual semantics",
    )
    source_ids = {
        row[field]
        for row in residuals
        for field in (
            "left_source_partition_row_id",
            "right_source_partition_row_id",
        )
    }
    require(len(source_ids) == 400, "residual source census")

    node_to_252: dict[str, str] = {}
    component252: dict[str, dict[str, Any]] = {}
    rows252 = closed_rows(
        result252["formal_post_Round252_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
        65_740,
    )
    for row in rows252:
        component_id = row["mixed_sheet_quotient_component_id"]
        require(component_id not in component252, f"unique R252 component:{component_id}")
        nodes = tuple(row["virtual_stratum_node_ids"])
        edges = frozenset(row["mixed_sheet_edge_ids"])
        require(
            row["virtual_stratum_node_count"] == len(nodes)
            and row["mixed_sheet_edge_count"] == len(edges),
            f"R252 component counts:{component_id}",
        )
        component252[component_id] = {
            "nodes": nodes,
            "edges": edges,
            "materialized_member_count": row["materialized_member_count"],
            "resolved_child_count": row["member_Round179_resolved_child_count"],
            "official_key_id": row["official_key_id"],
        }
        for node_id in nodes:
            require(node_id not in node_to_252, f"virtual partition:{node_id}")
            node_to_252[node_id] = component_id
    require(len(node_to_252) == 133_684, "R252 virtual-node census")

    strict_edge_nodes: set[str] = set()
    rows = closed_rows(
        result252["formal_wall_axis_face_positive_patch_edge_ledger"],
        "wall_axis_face_edge_id",
        22_016,
    )
    for row in rows:
        strict_edge_nodes.update(
            (row["left_wall_bulk_node_id"], row["right_wall_bulk_node_id"])
        )
    del rows252, rows, result252
    gc.collect()

    # Bind selected endpoint cells to exact upstream geometry.
    result234 = upstream_result(R234)
    rows234 = plain_rows(
        result234,
        "depth6_frontier_rows",
        "depth6_frontier_rows_sha256",
    )
    all_frontiers = {row["frontier_row_id"]: row for row in rows234}
    require(len(all_frontiers) == len(rows234), "unique R234 frontier")
    del result234, rows234
    gc.collect()

    result235 = upstream_result(R235)
    rows235 = plain_rows(
        result235,
        "single_endpoint_graph_partition_rows",
        "single_endpoint_graph_partition_rows_sha256",
    )
    endpoint = {
        row["endpoint_graph_partition_row_id"]: row
        for row in rows235
        if row["endpoint_graph_partition_row_id"] in source_ids
    }
    require(set(endpoint) == source_ids, "selected R235 endpoint rows")
    selected_frontier_ids = {
        row["Round234_frontier_row_id"] for row in endpoint.values()
    }
    require(selected_frontier_ids <= set(all_frontiers), "R234 references")
    frontiers = {
        identifier: all_frontiers[identifier]
        for identifier in selected_frontier_ids
    }
    del result235, rows235, all_frontiers
    gc.collect()

    result248 = upstream_result(R248)
    rows248 = closed_rows(
        result248["formal_wall_positive_volume_bulk_ledger"],
        "wall_bulk_node_id",
        88_936,
    )
    branches: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows248:
        source_id = row["source_partition_row_id"]
        if source_id in source_ids:
            label = row["branch_label"]
            require(label not in branches[source_id], f"unique branch:{source_id}:{label}")
            branches[source_id][label] = row
    require(
        set(branches) == source_ids
        and all(set(value) == {"EVENT_ABSENT", "EVENT_PRESENT"} for value in branches.values()),
        "two branches per selected endpoint",
    )
    sheet_rows = closed_rows(
        result248["formal_wall_half_open_sheet_owner_ledger"],
        "wall_sheet_node_id",
        38_360,
    )
    sheets: dict[str, dict[str, Any]] = {}
    for row in sheet_rows:
        source_id = row["source_partition_row_id"]
        if source_id in source_ids:
            require(source_id not in sheets, f"unique sheet:{source_id}")
            sheets[source_id] = row
    require(set(sheets) == source_ids, "selected endpoint sheets")
    del result248, rows248, sheet_rows
    gc.collect()

    for name, table, identity in (
        (R250, "formal_wall_t_chain_positive_patch_edge_ledger", "wall_chain_edge_id"),
        (R251, "formal_wall_p_face_positive_patch_edge_ledger", "wall_p_face_edge_id"),
    ):
        result = upstream_result(name)
        rows = closed_rows(result[table], identity)
        for row in rows:
            strict_edge_nodes.update(
                (row["left_wall_bulk_node_id"], row["right_wall_bulk_node_id"])
            )
        del result, rows
        gc.collect()

    maps = quotient_lineage_maps()

    def current_for_component(component_id: str) -> str:
        value = component_id
        for mapping in maps:
            require(value in mapping, f"lineage coverage:{value}")
            value = mapping[value]
        return value

    node_to_current = {
        node_id: current_for_component(component_id)
        for node_id, component_id in node_to_252.items()
    }

    result263 = upstream_result(R263)
    require(
        result263["census"]["post_Round263_component_count"] == 68_716
        and result263["census"]["occurrence_frontier_count"] == 53_968
        and result263["census"]["exact_key_frontier_count"] == 116
        and result263["census"]["true_source_chart_seam_candidate_count"] == 0
        and result263["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "R263 identity freeze",
    )
    del result263
    gc.collect()

    result262 = upstream_result(R262)
    component_rows262 = closed_rows(
        result262["formal_post_Round262_component_commitment_ledger"],
        "post_Round262_component_row_id",
        68_716,
    )
    occurrence_rows262 = closed_rows(
        result262["formal_post_Round262_occurrence_frontier_ledger"],
        "post_frontier_row_id",
        53_968,
    )
    key_rows262 = closed_rows(
        result262["formal_post_Round262_key_frontier_ledger"],
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
    require(len(base_component) == 68_716, "R262 component function")
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
    require(len(base_occurrence) == 53_968, "R262 occurrence function")
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
    require(len(base_key) == 116, "R262 key function")
    del (
        component_rows262,
        occurrence_rows262,
        key_rows262,
        result262,
    )
    gc.collect()

    # Reclassify each one-sided endpoint cell directly from exact signs.
    correction_rows: list[dict[str, Any]] = []
    empty_nodes: set[str] = set()
    phantom_components: set[str] = set()
    invalid_edges: set[str] = set()
    invalid_edges_by_component: dict[str, list[str]] = defaultdict(list)
    removed_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    retained_sheets_by_component: dict[str, list[str]] = defaultdict(list)
    empty_labels: Counter[str] = Counter()
    chart_cells: Counter[str] = Counter()

    for source_id in sorted(source_ids):
        metadata = endpoint[source_id]
        require(
            metadata["active_endpoint_factor"] == "source"
            and metadata["active_factor_strict_t_derivative_sign"]
            == "STRICT_POSITIVE",
            f"active source factor:{source_id}",
        )
        chart = metadata["source_chart"]
        reason = metadata["reason_label"]
        parts = reason.split(":")
        require(
            chart in {"G:E", "G:N", "G:S", "G:W"}
            and len(parts) == 3
            and parts[0] == "wall_endpoint_or_count_transition",
            f"endpoint reason:{source_id}",
        )
        axis = "Y" if chart in {"G:E", "G:W"} else "X"
        require(parts[1:] == [axis, "0"], f"chart/axis rule:{source_id}")
        frontier = frontiers[metadata["Round234_frontier_row_id"]]
        require(
            frontier["chart"] == chart
            and frontier["owner_target"] == metadata["target_lift"]
            and frontier["Round220_split_interface_id"]
            == metadata["Round220_split_interface_id"]
            and reason in frontier["reason_labels"],
            f"R234/R235 binding:{source_id}",
        )
        box = rational_box(frontier["box"], source_id)
        if box[0] < 0 and box[1] == 0:
            cell_side = "STRICT_NEGATIVE_T_SIDE"
            source_sign = "STRICT_NEGATIVE"
        elif box[0] == 0 and box[1] > 0:
            cell_side = "STRICT_POSITIVE_T_SIDE"
            source_sign = "STRICT_POSITIVE"
        else:
            raise VerificationFailure(f"one-sided t cell:{source_id}")
        sheet = sheets[source_id]
        require(
            sheet["endpoint_factor"] == "source"
            and sheet["exact_closed_base_rectangle"] == frontier["box"][2:6]
            and sheet["sheet_three_dimensional_coordinate_volume"] == "0"
            and Fraction(sheet["exact_positive_2D_sheet_area"]) > 0,
            f"sheet geometry:{source_id}",
        )
        fixed_sign = metadata["fixed_endpoint_factor_sign"]
        require(
            fixed_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
            f"fixed sign:{source_id}",
        )
        present_nonempty = source_sign != fixed_sign
        nonempty_label = "EVENT_PRESENT" if present_nonempty else "EVENT_ABSENT"
        empty_label = "EVENT_ABSENT" if present_nonempty else "EVENT_PRESENT"
        empty = branches[source_id][empty_label]
        nonempty = branches[source_id][nonempty_label]
        require(
            empty["exact_positive_3D_box"] is None
            and empty["exact_positive_3D_volume"] is None
            and nonempty["exact_positive_3D_box"] is None
            and nonempty["exact_positive_3D_volume"] is None
            and empty["positive_volume_proof_kind"]
            == (
                "ROUND235_STRICT_MONOTONE_GRAPH_"
                f"{empty_label.removeprefix('EVENT_')}_OPEN_SIDE"
            )
            and nonempty["positive_volume_proof_kind"]
            == (
                "ROUND235_STRICT_MONOTONE_GRAPH_"
                f"{nonempty_label.removeprefix('EVENT_')}_OPEN_SIDE"
            ),
            f"R248 branch encoding:{source_id}",
        )
        empty_node = empty["wall_bulk_node_id"]
        nonempty_node = nonempty["wall_bulk_node_id"]
        sheet_node = sheet["wall_sheet_node_id"]
        require(
            empty_node in node_to_252
            and nonempty_node in node_to_252
            and sheet_node in node_to_252,
            f"virtual-node binding:{source_id}",
        )
        require(empty_node not in strict_edge_nodes, f"empty strict edge:{source_id}")
        empty_current = node_to_current[empty_node]
        nonempty_current = node_to_current[nonempty_node]
        require(
            base_component[empty_current]["official_key_id"]
            == empty["official_key_id"]
            and base_component[nonempty_current]["official_key_id"]
            == nonempty["official_key_id"],
            f"current key binding:{source_id}",
        )
        invalid_edge: str | None = None
        if empty_label == "EVENT_PRESENT":
            statistics = component252[node_to_252[empty_node]]
            require(
                statistics["nodes"] == (empty_node,)
                and not statistics["edges"]
                and statistics["materialized_member_count"] == 1
                and statistics["resolved_child_count"] == 0,
                f"present singleton phantom:{source_id}",
            )
            phantom_components.add(empty_current)
            disposition = "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT"
        else:
            invalid_edge = sheet["owner_mixed_sheet_edge_id"]
            statistics = component252[node_to_252[empty_node]]
            require(
                sheet["owner_wall_bulk_node_id"] == empty_node
                and invalid_edge in statistics["edges"]
                and node_to_252[empty_node] == node_to_252[sheet_node],
                f"invalid absent owner edge:{source_id}",
            )
            invalid_edges.add(invalid_edge)
            invalid_edges_by_component[empty_current].append(invalid_edge)
            retained_sheets_by_component[empty_current].append(sheet_node)
            disposition = (
                "PRUNE_EMPTY_ABSENT_BULK_NODE_AND_INVALID_OWNER_EDGE__"
                "RETAIN_T0_SHEET"
            )
        empty_nodes.add(empty_node)
        removed_nodes_by_component[empty_current].append(empty_node)
        empty_labels[empty_label] += 1
        chart_cells[chart] += 1
        correction_rows.append(seal({
            "endpoint_empty_branch_disposition_row_id":
                "round264-endpoint-empty-branch:" + fingerprint([source_id]),
            "source_partition_row_id": source_id,
            "Round234_frontier_row_id": metadata["Round234_frontier_row_id"],
            "Round220_split_interface_id":
                metadata["Round220_split_interface_id"],
            "source_chart": chart,
            "target_lift": metadata["target_lift"],
            "exact_one_sided_cell_box": frontier["box"],
            "reason_label": reason,
            "transition_event": metadata["transition_event"],
            "transition_event_order_position":
                metadata["transition_event_order_position"],
            "active_endpoint_factor": "source",
            "active_factor_strict_t_derivative_sign": "STRICT_POSITIVE",
            "relevant_source_coordinate":
                "source_y" if axis == "Y" else "source_x",
            "exact_relevant_source_coordinate_formula": "(9/25)*t",
            "exact_zero_set": "t=0",
            "strict_open_cell_side": cell_side,
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
            "empty_branch_Round250_Round251_Round252_accepted_edge_incidence_count":
                0,
            "pre_Round264_empty_node_component_id": empty_current,
            "pre_Round264_nonempty_node_component_id": nonempty_current,
            "retained_t0_sheet_node_id": sheet_node,
            "invalid_Round248_owner_edge_id": invalid_edge,
            "disposition": disposition,
            "component_credit": -1 if empty_label == "EVENT_PRESENT" else 0,
            "maximality_credit": 0,
        }))
    correction_rows.sort(
        key=lambda row: row["endpoint_empty_branch_disposition_row_id"]
    )
    require(len(empty_nodes) == 400, "empty node census")
    require(len(phantom_components) == 216, "phantom component census")
    require(len(invalid_edges) == 184, "invalid owner-edge census")
    require(
        dict(sorted(empty_labels.items()))
        == {"EVENT_ABSENT": 184, "EVENT_PRESENT": 216},
        "empty-label census",
    )
    require(
        dict(sorted(chart_cells.items()))
        == {"G:E": 100, "G:N": 100, "G:S": 100, "G:W": 100},
        "endpoint chart census",
    )
    require(
        not (set(removed_nodes_by_component) - set(base_component)),
        "removed-node component coverage",
    )
    occurrence_components = {
        row["current_component_id"] for row in base_occurrence.values()
    }
    require(
        phantom_components.isdisjoint(occurrence_components),
        "phantoms occurrence-free",
    )

    retained_base_ids = sorted(set(base_component) - phantom_components)
    require(len(retained_base_ids) == 68_500, "post-pruning components")
    quotient = UnionFind(retained_base_ids)

    # Build every exact t=0 sheet identity in the frozen candidate universe.
    sheet_edges: list[dict[str, Any]] = []
    area_histogram: Counter[str] = Counter()
    area_sum = Fraction(0)
    pair_multiplicity: Counter[tuple[str, str]] = Counter()
    contact_charts: Counter[str] = Counter()
    for contact in sorted(
        residuals,
        key=lambda row: row["rejected_axis_face_contact_id"],
    ):
        left_id = contact["left_source_partition_row_id"]
        right_id = contact["right_source_partition_row_id"]
        left_meta = endpoint[left_id]
        right_meta = endpoint[right_id]
        left_frontier = frontiers[left_meta["Round234_frontier_row_id"]]
        right_frontier = frontiers[right_meta["Round234_frontier_row_id"]]
        left_box = rational_box(left_frontier["box"], left_id)
        right_box = rational_box(right_frontier["box"], right_id)
        require(
            left_box[0] < 0
            and left_box[1] == right_box[0] == 0
            and right_box[1] > 0,
            f"shared t=0 face:{contact['rejected_axis_face_contact_id']}",
        )
        require(
            left_meta["source_chart"] == right_meta["source_chart"]
            and left_meta["target_lift"] == right_meta["target_lift"]
            and left_meta["transition_event"] == right_meta["transition_event"]
            and left_meta["reason_label"] == right_meta["reason_label"],
            f"endpoint identity:{contact['rejected_axis_face_contact_id']}",
        )
        left_sheet = sheets[left_id]
        right_sheet = sheets[right_id]
        require(
            left_sheet["owner_signature_sha256"]
            == right_sheet["owner_signature_sha256"]
            and left_sheet["owner_official_key_id"]
            == right_sheet["owner_official_key_id"]
            and left_sheet["half_open_owner_rule"]
            == right_sheet["half_open_owner_rule"],
            f"sheet owner identity:{contact['rejected_axis_face_contact_id']}",
        )
        rectangle, area = common_rectangle(
            left_sheet["exact_closed_base_rectangle"],
            right_sheet["exact_closed_base_rectangle"],
            contact["rejected_axis_face_contact_id"],
        )
        left_current = node_to_current[left_sheet["owner_wall_bulk_node_id"]]
        right_current = node_to_current[right_sheet["owner_wall_bulk_node_id"]]
        require(
            left_current != right_current
            and left_current not in phantom_components
            and right_current not in phantom_components
            and base_component[left_current]["official_key_id"]
            == base_component[right_current]["official_key_id"]
            == left_sheet["owner_official_key_id"],
            f"sheet exact-key pair:{contact['rejected_axis_face_contact_id']}",
        )
        pair = tuple(sorted((left_current, right_current)))
        rank_reducing = quotient.join(*pair)
        pair_multiplicity[pair] += 1
        area_text = fraction_text(area)
        area_histogram[area_text] += 1
        area_sum += area
        contact_charts[left_meta["source_chart"]] += 1
        sheet_edges.append(seal({
            "endpoint_sheet_identity_edge_row_id":
                "round264-endpoint-sheet-identity:" + fingerprint([
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
            "exact_positive_area_common_refinement_rectangle": rectangle,
            "exact_positive_area_common_refinement_area": area_text,
            "pre_Round264_component_pair": list(pair),
            "edge_kind": "EXACT_SAME_PHYSICAL_T0_ENDPOINT_SHEET_IDENTITY",
            "rank_reducing_edge": rank_reducing,
            "component_union_credit": int(rank_reducing),
            "maximality_credit": 0,
        }))
    sheet_edges.sort(
        key=lambda row: row["endpoint_sheet_identity_edge_row_id"]
    )
    require(len(sheet_edges) == 248, "sheet-edge census")
    require(
        sum(row["rank_reducing_edge"] for row in sheet_edges) == 184,
        "sheet rank census",
    )
    require(
        dict(sorted(area_histogram.items())) == AREA_HISTOGRAM,
        "sheet area histogram",
    )
    require(area_sum == Fraction(123, 6400), "sheet area sum")
    multiplicity_histogram = Counter(pair_multiplicity.values())
    require(
        {
            str(key): value
            for key, value in sorted(multiplicity_histogram.items())
        }
        == PAIR_MULTIPLICITY_HISTOGRAM,
        "sheet-pair multiplicity",
    )
    require(
        dict(sorted(contact_charts.items()))
        == {"G:E": 62, "G:N": 62, "G:S": 62, "G:W": 62},
        "sheet contact chart census",
    )
    require(
        len({quotient.root(value) for value in retained_base_ids}) == 68_316,
        "post-sheet quotient",
    )

    # Independently consume and recheck the complete Round204 tail lineage.
    result204 = upstream_result(R204)
    tail_source_rows = closed_rows(
        result204["tail_pair_signature_glue_ledger"],
        "pair_glue_row_id",
        32,
    )
    open_rows = closed_rows(
        result204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    )
    open_region = {row["region_row_id"]: row for row in open_rows}
    source_sheet_204 = {
        row["sheet_row_id"]: row
        for row in result204["formal_2D_sheet_lineage"]["source_sheet_rows"]
    }
    target_sheet_204 = {
        row["sheet_row_id"]: row
        for row in result204["formal_2D_sheet_lineage"]["target_sheet_rows"]
    }
    one_dimensional = {
        row["edge_row_id"]: row
        for row in result204[
            "formal_1D_boundary_and_intersection_lineage"
        ]["rows"]
    }
    tail_geometry = {
        row["tail_pair_row_id"]: row
        for row in result204["tail_geometry_evidence_ledger"]["pair_rows"]
    }
    tail_edges: list[dict[str, Any]] = []
    tail_pairs: Counter[tuple[str, str]] = Counter()
    sheet_pair_set = set(pair_multiplicity)
    for source in sorted(
        tail_source_rows,
        key=lambda row: row["pair_glue_row_id"],
    ):
        require(
            source["pair_glue_status"] == "UNIQUE_EXPECTED_EMPTY_EVENT_EMPTY"
            and source["materialized_local_open_region_count"] == 3
            and len(source["outer_empty_region_row_ids"]) == 2
            and source["unexpected_signature_change_count"] == 0,
            f"tail contract:{source['pair_glue_row_id']}",
        )
        outer = [
            open_region[value]
            for value in source["outer_empty_region_row_ids"]
        ]
        require(
            all(
                row["graph_classification"] == "RESIDUAL_3D"
                and row["signed_wall_word"] == []
                and row["wall_crossing_count"] == 0
                and row["tail_region"] is True
                and row["region_kind"] in {
                    "TAIL_BOUNDARY_ONLY_SINGLE_REGION",
                    "TAIL_TARGET_GRAPH_SAME_SIGN_OUTER_REGION",
                }
                and row["strict_open_region"] is True
                and row["positive_coordinate_volume"] is True
                and row["official_key_id"]
                == source["outer_empty_official_key_id"]
                for row in outer
            ),
            f"tail outer regions:{source['pair_glue_row_id']}",
        )
        source_sheet = source_sheet_204[source["source_sheet_2D_row_id"]]
        target_sheet = target_sheet_204[source["target_sheet_2D_row_id"]]
        intersection = one_dimensional[
            source["source_target_intersection_1D_row_id"]
        ]
        geometry = tail_geometry[source["tail_pair_row_id"]]
        require(
            source_sheet["ambient_dimension"] == 2
            and source_sheet["source_wall_factor_exact"] == "(9/25)*t"
            and source_sheet["source_wall_factor_exact_zero_set"] == "t=0"
            and source["source_target_intersection_1D_row_id"]
            in source_sheet["source_target_intersection_1D_row_ids"]
            and target_sheet["ambient_dimension"] == 2
            and target_sheet[
                "exact_source_target_intersection_on_p0_boundary"
            ] is True
            and source["source_target_intersection_1D_row_id"]
            in target_sheet["source_target_intersection_1D_row_ids"]
            and intersection["ambient_dimension"] == 1
            and intersection["exact_source_target_intersection"] is True
            and {
                source["source_sheet_2D_row_id"],
                source["target_sheet_2D_row_id"],
            }
            <= set(intersection["incident_sheet_row_ids"])
            and geometry["common_t0_face_byte_for_byte_equal"] is True
            and geometry["local_lineage_materialized"] is True
            and geometry["negative_t_leaf_row_id"]
            == source["negative_t_leaf_row_id"]
            and geometry["positive_t_leaf_row_id"]
            == source["positive_t_leaf_row_id"],
            f"tail dimensional lineage:{source['pair_glue_row_id']}",
        )
        occurrence_ids = source["outer_empty_region_row_ids"]
        require(
            all(value in base_occurrence for value in occurrence_ids),
            f"tail occurrence coverage:{source['pair_glue_row_id']}",
        )
        component_pair = tuple(sorted(
            base_occurrence[value]["current_component_id"]
            for value in occurrence_ids
        ))
        require(
            component_pair[0] != component_pair[1]
            and component_pair[0] not in phantom_components
            and component_pair[1] not in phantom_components
            and base_component[component_pair[0]]["official_key_id"]
            == base_component[component_pair[1]]["official_key_id"]
            == source["outer_empty_official_key_id"],
            f"tail exact-key pair:{source['pair_glue_row_id']}",
        )
        require(
            component_pair not in sheet_pair_set,
            f"edge family disjoint:{source['pair_glue_row_id']}",
        )
        rank_reducing = quotient.join(*component_pair)
        tail_pairs[component_pair] += 1
        tail_edges.append(seal({
            "Round204_tail_glue_closure_edge_row_id":
                "round264-Round204-tail-glue:"
                + fingerprint([source["pair_glue_row_id"]]),
            "source_Round204_pair_glue_row_id": source["pair_glue_row_id"],
            "source_Round204_tail_pair_row_id": source["tail_pair_row_id"],
            "outer_empty_region_row_ids": occurrence_ids,
            "outer_empty_official_key_id":
                source["outer_empty_official_key_id"],
            "source_sheet_2D_row_id": source["source_sheet_2D_row_id"],
            "target_sheet_2D_row_id": source["target_sheet_2D_row_id"],
            "source_target_intersection_1D_row_id":
                source["source_target_intersection_1D_row_id"],
            "source_sheet_exact_base_rectangle":
                source_sheet["base_p_s_exact_bounds"],
            "target_sheet_exact_base_rectangle":
                target_sheet["base_p_s_exact_bounds"],
            "exact_1D_intersection_geometry_key": intersection["geometry_key"],
            "pre_Round264_component_pair": list(component_pair),
            "edge_kind":
                "ROUND204_MATERIALIZED_EMPTY_EVENT_EMPTY_TAIL_GLUE",
            "rank_reducing_edge": rank_reducing,
            "component_union_credit": int(rank_reducing),
            "maximality_credit": 0,
        }))
    tail_edges.sort(
        key=lambda row: row["Round204_tail_glue_closure_edge_row_id"]
    )
    require(
        len(tail_pairs) == 4 and set(tail_pairs.values()) == {8},
        "tail pair multiplicity",
    )
    require(
        sum(row["rank_reducing_edge"] for row in tail_edges) == 4,
        "tail rank census",
    )
    require(
        len({quotient.root(value) for value in retained_base_ids}) == 68_312,
        "corrected quotient",
    )
    del (
        result204,
        tail_source_rows,
        open_rows,
        open_region,
        source_sheet_204,
        target_sheet_204,
        one_dimensional,
        tail_geometry,
    )
    gc.collect()

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
                sorted(invalid_edges_by_component.get(component_id, [])),
            "retained_exact_t0_endpoint_sheet_node_ids":
                sorted(retained_sheets_by_component.get(component_id, [])),
        }

    classes: dict[str, list[str]] = defaultdict(list)
    for component_id in retained_base_ids:
        classes[quotient.root(component_id)].append(component_id)
    require(len(classes) == 68_312, "corrected class census")
    post_id_by_base: dict[str, str] = {}
    class_descriptors: dict[
        str, tuple[str, list[dict[str, Any]]]
    ] = {}
    for root, members in classes.items():
        members.sort()
        descriptors = [descriptor_by_base[value] for value in members]
        post_id = "round264-corrected-component:" + fingerprint(descriptors)
        require(post_id not in class_descriptors, f"unique post id:{post_id}")
        class_descriptors[post_id] = (root, descriptors)
        for member in members:
            post_id_by_base[member] = post_id

    occurrence_rows: list[dict[str, Any]] = []
    occurrence_count_by_post: Counter[str] = Counter()
    occurrence_count_by_key: Counter[str] = Counter()
    for occurrence_id in sorted(base_occurrence):
        item = base_occurrence[occurrence_id]
        current_id = item["current_component_id"]
        require(
            current_id not in phantom_components,
            f"occurrence not phantom:{occurrence_id}",
        )
        post_id = post_id_by_base[current_id]
        occurrence_count_by_post[post_id] += 1
        occurrence_count_by_key[item["official_key_id"]] += 1
        occurrence_rows.append(seal({
            "post_Round264_occurrence_frontier_row_id":
                "round264-occurrence-frontier:" + fingerprint([occurrence_id]),
            "local_occurrence_row_id": occurrence_id,
            "official_key_id": item["official_key_id"],
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round262_occurrence_frontier_row_id":
                item["source_row_id"],
            "source_Round262_occurrence_frontier_row_sha256":
                item["source_row_sha256"],
            "post_Round262_quotient_component_id": current_id,
            "post_Round264_quotient_component_id": post_id,
            "corrected_quotient_assignment_credit": 1,
            "maximal_physical_component_assignment_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    require(len(occurrence_rows) == 53_968, "occurrence frontier census")

    virtual_rows: list[dict[str, Any]] = []
    virtual_count_by_post: Counter[str] = Counter()
    virtual_count_by_key: Counter[str] = Counter()
    virtual_kinds: Counter[str] = Counter()
    for node_id in sorted(node_to_252):
        if node_id in empty_nodes:
            continue
        current_id = node_to_current[node_id]
        require(
            current_id not in phantom_components,
            f"valid virtual not phantom:{node_id}",
        )
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
        virtual_kinds[kind] += 1
        virtual_rows.append(seal({
            "post_Round264_valid_virtual_node_frontier_row_id":
                "round264-valid-virtual-node:" + fingerprint([node_id]),
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
    require(len(virtual_rows) == 133_284, "valid virtual frontier census")

    sheet_edge_count_by_post: Counter[str] = Counter()
    sheet_rank_count_by_post: Counter[str] = Counter()
    for row in sheet_edges:
        post_id = post_id_by_base[row["pre_Round264_component_pair"][0]]
        require(
            post_id
            == post_id_by_base[row["pre_Round264_component_pair"][1]],
            "sheet post assignment",
        )
        sheet_edge_count_by_post[post_id] += 1
        sheet_rank_count_by_post[post_id] += int(row["rank_reducing_edge"])
    tail_edge_count_by_post: Counter[str] = Counter()
    tail_rank_count_by_post: Counter[str] = Counter()
    for row in tail_edges:
        post_id = post_id_by_base[row["pre_Round264_component_pair"][0]]
        require(
            post_id
            == post_id_by_base[row["pre_Round264_component_pair"][1]],
            "tail post assignment",
        )
        tail_edge_count_by_post[post_id] += 1
        tail_rank_count_by_post[post_id] += int(row["rank_reducing_edge"])

    component_rows: list[dict[str, Any]] = []
    component_count_by_key: Counter[str] = Counter()
    B_count_by_key: Counter[str] = Counter()
    Z_count_by_key: Counter[str] = Counter()
    class_size_histogram: Counter[int] = Counter()
    for post_id in sorted(class_descriptors):
        _root, descriptors = class_descriptors[post_id]
        members = [
            descriptor["post_Round262_quotient_component_id"]
            for descriptor in descriptors
        ]
        keys = {base_component[value]["official_key_id"] for value in members}
        ordinals = {
            base_component[value]["official_key_ordinal"] for value in members
        }
        require(
            len(keys) == len(ordinals) == 1,
            f"component key purity:{post_id}",
        )
        key_id = next(iter(keys))
        ordinal = next(iter(ordinals))
        occurrence_count = occurrence_count_by_post[post_id]
        component_class = (
            "B_OCCURRENCE_BEARING"
            if occurrence_count
            else "Z_ZERO_OCCURRENCE_CARRIER"
        )
        component_count_by_key[key_id] += 1
        (
            B_count_by_key if occurrence_count else Z_count_by_key
        )[key_id] += 1
        class_size_histogram[len(members)] += 1
        component_rows.append(seal({
            "post_Round264_component_frontier_row_id":
                "round264-component-row:" + fingerprint([post_id]),
            "post_Round264_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "corrected_constituent_descriptor_count": len(descriptors),
            "corrected_constituent_descriptors_sha256":
                fingerprint(descriptors),
            "corrected_constituent_descriptors": descriptors,
            "constituent_Round262_component_ids": members,
            "constituent_Round262_component_ids_sha256":
                fingerprint(members),
            "removed_empty_bulk_node_count": sum(
                len(item["removed_empty_bulk_node_ids"])
                for item in descriptors
            ),
            "removed_invalid_Round248_owner_edge_count": sum(
                len(item["removed_invalid_Round248_owner_edge_ids"])
                for item in descriptors
            ),
            "retained_exact_t0_endpoint_sheet_count": sum(
                len(item["retained_exact_t0_endpoint_sheet_node_ids"])
                for item in descriptors
            ),
            "endpoint_sheet_identity_edge_count":
                sheet_edge_count_by_post[post_id],
            "endpoint_sheet_identity_rank_reduction_count":
                sheet_rank_count_by_post[post_id],
            "Round204_tail_glue_edge_count":
                tail_edge_count_by_post[post_id],
            "Round204_tail_glue_rank_reduction_count":
                tail_rank_count_by_post[post_id],
            "local_occurrence_count": occurrence_count,
            "valid_virtual_stratum_node_count":
                virtual_count_by_post[post_id],
            "component_class": component_class,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    require(len(component_rows) == 68_312, "component frontier census")
    B_count = sum(
        occurrence_count_by_post[post_id] > 0
        for post_id in class_descriptors
    )
    Z_count = len(class_descriptors) - B_count
    require((B_count, Z_count) == (10_904, 57_408), "component B/Z census")

    component_map_rows: list[dict[str, Any]] = []
    for current_id in sorted(base_component):
        if current_id in phantom_components:
            disposition = (
                "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT"
            )
            post_id: str | None = None
        elif removed_nodes_by_component.get(current_id):
            disposition = (
                "PRUNE_EMPTY_ABSENT_NODE_AND_INVALID_EDGE__RETAIN_SHEET"
            )
            post_id = post_id_by_base[current_id]
        else:
            disposition = (
                "RETAIN_AND_REQUOTIENT_BY_CERTIFIED_LOWER_DIMENSIONAL_EDGES"
            )
            post_id = post_id_by_base[current_id]
        component_map_rows.append(seal({
            "Round262_to_Round264_component_correction_map_row_id":
                "round264-component-map:" + fingerprint([current_id]),
            "post_Round262_quotient_component_id": current_id,
            "official_key_id":
                base_component[current_id]["official_key_id"],
            "source_Round262_component_row_id":
                base_component[current_id]["source_row_id"],
            "source_Round262_component_row_sha256":
                base_component[current_id]["source_row_sha256"],
            "removed_empty_bulk_node_ids":
                sorted(removed_nodes_by_component.get(current_id, [])),
            "removed_invalid_Round248_owner_edge_ids":
                sorted(invalid_edges_by_component.get(current_id, [])),
            "retained_exact_t0_endpoint_sheet_node_ids":
                sorted(retained_sheets_by_component.get(current_id, [])),
            "component_correction_disposition": disposition,
            "post_Round264_quotient_component_id": post_id,
            "component_count_credit": -1 if post_id is None else 0,
            "maximality_credit": 0,
        }))
    require(len(component_map_rows) == 68_716, "component-map census")

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
        require(
            occurrence_count_by_key[key_id] == item["occurrence_count"],
            f"occurrence/key conservation:{key_id}",
        )
        reduction_histogram[reduction] += 1
        total_reduction_histogram[total_reduction] += 1
        key_rows.append(seal({
            "post_Round264_key_frontier_row_id":
                "round264-key-frontier:" + fingerprint([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round262_key_frontier_row_id": item["source_row_id"],
            "source_Round262_key_frontier_row_sha256":
                item["source_row_sha256"],
            "local_occurrence_count": occurrence_count_by_key[key_id],
            "valid_virtual_stratum_node_count":
                virtual_count_by_key[key_id],
            "post_Round262_quotient_component_count":
                item["pre_component_count"],
            "dropped_empty_EVENT_PRESENT_singleton_component_count":
                phantom_count_by_key[key_id],
            "post_empty_branch_pruning_component_count": post_pruning_count,
            "post_Round264_quotient_component_count": post_count,
            "lower_dimensional_glue_rank_reduction": reduction,
            "total_Round262_to_Round264_component_reduction":
                total_reduction,
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
    require(
        {
            str(key): value
            for key, value in sorted(reduction_histogram.items())
        }
        == KEY_REDUCTION_HISTOGRAM,
        "per-key glue reduction histogram",
    )
    require(
        total_reduction_histogram[0] == 40
        and sum(
            value
            for key, value in total_reduction_histogram.items()
            if key > 0
        )
        == 76,
        "changed-key census",
    )
    require(sum(component_count_by_key.values()) == 68_312, "key/component sum")
    require(sum(occurrence_count_by_key.values()) == 53_968, "key/occurrence sum")
    require(sum(virtual_count_by_key.values()) == 133_284, "key/virtual sum")

    class_size_text = {
        str(key): value for key, value in sorted(class_size_histogram.items())
    }
    virtual_kind_text = dict(sorted(virtual_kinds.items()))
    require(sum(virtual_kinds.values()) == 133_284, "virtual-kind sum")

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
            PAIR_MULTIPLICITY_HISTOGRAM,
        "endpoint_sheet_exact_common_area_histogram": AREA_HISTOGRAM,
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
            KEY_REDUCTION_HISTOGRAM,
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
        "formal_input_binding": expected_input_binding(),
        "formal_endpoint_empty_branch_correction_disposition_ledger":
            make_ledger(
                correction_rows,
                "endpoint_empty_branch_disposition_row_id",
            ),
        "formal_endpoint_sheet_identity_common_refinement_ledger":
            make_ledger(
                sheet_edges,
                "endpoint_sheet_identity_edge_row_id",
            ),
        "formal_Round204_tail_pair_glue_closure_ledger":
            make_ledger(
                tail_edges,
                "Round204_tail_glue_closure_edge_row_id",
            ),
        "formal_Round262_to_Round264_component_correction_map_ledger":
            make_ledger(
                component_map_rows,
                "Round262_to_Round264_component_correction_map_row_id",
            ),
        "formal_post_Round264_component_frontier_ledger":
            make_ledger(
                component_rows,
                "post_Round264_component_frontier_row_id",
            ),
        "formal_post_Round264_occurrence_frontier_ledger":
            make_ledger(
                occurrence_rows,
                "post_Round264_occurrence_frontier_row_id",
            ),
        "formal_post_Round264_key_frontier_ledger":
            make_ledger(
                key_rows,
                "post_Round264_key_frontier_row_id",
            ),
        "formal_post_Round264_valid_virtual_node_frontier_ledger":
            make_ledger(
                virtual_rows,
                "post_Round264_valid_virtual_node_frontier_row_id",
            ),
        "census": census,
        "scope_contract": {
            "all_248_Round252_t_face_residuals_exactly_revisited": True,
            "all_400_distinct_Round235_endpoint_cells_exactly_classified":
                True,
            "source_G_relevant_coordinate_is_exactly_9_over_25_times_t":
                True,
            "source_G_chart_axis_rule":
                "G:E,G:W->source_y=0__G:N,G:S->source_x=0",
            "all_400_empty_branch_bulks_have_exact_zero_physical_support":
                True,
            "all_400_empty_nodes_have_zero_Round250_Round251_Round252_accepted_edge_incidence":
                True,
            "all_216_empty_EVENT_PRESENT_components_are_singleton_phantoms":
                True,
            "all_184_invalid_EVENT_ABSENT_owner_edges_are_removed_but_sheets_retained":
                True,
            "all_248_endpoint_sheet_pairs_have_exact_positive_area_identity_common_refinement":
                True,
            "all_32_Round204_tail_glues_cross_checked_through_3D_2D_1D_lineage":
                True,
            "endpoint_sheet_and_Round204_tail_edge_families_have_disjoint_pre_component_pairs":
                True,
            "complete_component_occurrence_key_and_valid_virtual_node_frontiers_rebuilt":
                True,
            "post_component_ids_are_based_on_corrected_constituent_descriptors_without_phantoms":
                True,
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
            "schema": CANDIDATE_SCHEMA,
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "fractions.Fraction exact rational",
            "seed_affects_output": False,
        },
    }


def canonical_line(raw: bytes, value: Any) -> bool:
    offset = 0
    for piece in encoded_chunks(value):
        following = offset + len(piece)
        if raw[offset:following] != piece:
            return False
        offset = following
    return raw[offset:] == b"\n"


def candidate_matches(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> bool:
    try:
        require(
            set(document) == {"schema", "result", "result_sha256"},
            "candidate envelope",
        )
        require(document["schema"] == CANDIDATE_SCHEMA, "candidate schema")
        require(isinstance(document["result"], dict), "candidate result object")
        # Compare the fully reconstructed semantics first.  A mismatching
        # candidate never gets to rely on its self-supplied digest.
        require(document["result"] == expected, "candidate expected equality")
        require(
            document["result_sha256"] == fingerprint(document["result"]),
            "candidate result closure",
        )
        return True
    except (VerificationFailure, KeyError, TypeError, ValueError):
        return False


def assign_path(root: Any, path: tuple[Any, ...], value: Any) -> Any:
    target = root
    for part in path[:-1]:
        target = target[part]
    old = target[path[-1]]
    target[path[-1]] = value
    return old


def resign_small_ledger(ledger: dict[str, Any]) -> None:
    rows = ledger["rows"]
    for row in rows:
        body = dict(row)
        body.pop("row_sha256")
        row["row_sha256"] = fingerprint(body)
    ledger["rows_sha256"] = fingerprint(rows)
    ledger["row_hashes_sha256"] = fingerprint(
        [row["row_sha256"] for row in rows]
    )


def semantic_attack_suite(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[tuple[str, tuple[Any, ...], Any, str | None]] = [
        (
            "invent_component",
            ("result", "census", "post_Round264_component_count"),
            68_313,
            None,
        ),
        (
            "promote_maximality",
            (
                "result",
                "strict_nonpromotion",
                "maximal_physical_component_credit",
            ),
            1,
            None,
        ),
        (
            "erase_empty_bulk_contract",
            (
                "result",
                "scope_contract",
                "all_400_empty_branch_bulks_have_exact_zero_physical_support",
            ),
            False,
            None,
        ),
        (
            "forge_producer_pin",
            ("result", "provenance", "producer_sha256"),
            "0" * 64,
            None,
        ),
        (
            "flip_empty_branch_disposition",
            (
                "result",
                "formal_endpoint_empty_branch_correction_disposition_ledger",
                "rows",
                0,
                "disposition",
            ),
            "KEEP_PHANTOM",
            "formal_endpoint_empty_branch_correction_disposition_ledger",
        ),
        (
            "invent_sheet_area",
            (
                "result",
                "formal_endpoint_sheet_identity_common_refinement_ledger",
                "rows",
                0,
                "exact_positive_area_common_refinement_area",
            ),
            "1",
            "formal_endpoint_sheet_identity_common_refinement_ledger",
        ),
        (
            "cross_key_tail_glue",
            (
                "result",
                "formal_Round204_tail_pair_glue_closure_ledger",
                "rows",
                0,
                "outer_empty_official_key_id",
            ),
            "gate5-word:forged",
            "formal_Round204_tail_pair_glue_closure_ledger",
        ),
        (
            "retain_dropped_component",
            (
                "result",
                "formal_Round262_to_Round264_component_correction_map_ledger",
                "rows",
                0,
                "component_count_credit",
            ),
            7,
            None,
        ),
        (
            "promote_component_row",
            (
                "result",
                "formal_post_Round264_component_frontier_ledger",
                "rows",
                0,
                "maximal_physical_component_claimed",
            ),
            True,
            None,
        ),
        (
            "redirect_occurrence",
            (
                "result",
                "formal_post_Round264_occurrence_frontier_ledger",
                "rows",
                0,
                "post_Round264_quotient_component_id",
            ),
            "round264-corrected-component:forged",
            None,
        ),
        (
            "exhaust_key",
            (
                "result",
                "formal_post_Round264_key_frontier_ledger",
                "rows",
                0,
                "global_exact_key_fibre_exhausted",
            ),
            True,
            None,
        ),
        (
            "promote_virtual_node",
            (
                "result",
                "formal_post_Round264_valid_virtual_node_frontier_ledger",
                "rows",
                0,
                "maximality_credit",
            ),
            1,
            None,
        ),
    ]
    rejected = 0
    for label, path, replacement, small_ledger in attacks:
        old = assign_path(candidate, path, replacement)
        if small_ledger is not None:
            resign_small_ledger(candidate["result"][small_ledger])
        candidate["result_sha256"] = fingerprint(candidate["result"])
        rejected += int(not candidate_matches(candidate, expected))
        assign_path(candidate, path, old)
        if small_ledger is not None:
            resign_small_ledger(candidate["result"][small_ledger])
        candidate["result_sha256"] = fingerprint(candidate["result"])
        require(candidate_matches(candidate, expected), f"attack restore:{label}")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_attacks_resigned_at_result_level": True,
        "small_ledger_attacks_reclosed_at_row_and_ledger_levels": 3,
        "attack_labels": [label for label, *_rest in attacks],
    }


def strict_json_attack_suite() -> dict[str, Any]:
    attacks: list[tuple[str, bytes]] = [
        ("duplicate_key", b'{"a":1,"a":2}'),
        ("float", b'{"a":1.5}'),
        ("exponent", b'{"a":1e2}'),
        ("nan", b'{"a":NaN}'),
        ("infinity", b'{"a":Infinity}'),
        ("negative_infinity", b'{"a":-Infinity}'),
        ("bom", b'\xef\xbb\xbf{"a":1}'),
        ("nul", b'{"a":"\\u0000"}\x00'),
        ("trailing", b'{"a":1} x'),
        ("two_documents", b'{"a":1}{"b":2}'),
        ("top_array", b"[]"),
        ("top_string", b'"x"'),
        ("top_integer", b"1"),
        ("invalid_utf8", b'{"a":"\xff"}'),
        ("truncated", b'{"a":'),
        ("unquoted_key", b"{a:1}"),
        ("comment", b'{"a":1/*x*/}'),
    ]
    rejected = 0
    for label, raw in attacks:
        try:
            parse_strict(raw, f"attack:{label}")
        except VerificationFailure:
            rejected += 1
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "attack_labels": [label for label, _raw in attacks],
    }


def file_attack_suite() -> dict[str, Any]:
    rejected = 0
    labels: list[str] = []
    with tempfile.TemporaryDirectory(prefix="round264-verifier-files-") as name:
        root = Path(name)
        regular = root / "regular"
        regular.write_bytes(b"x")

        cases: list[tuple[str, Path, int, Path | None]] = []
        cases.append(("wrong_parent", regular, 100, HERE))

        empty = root / "empty"
        empty.write_bytes(b"")
        cases.append(("empty", empty, 100, None))

        directory = root / "directory"
        directory.mkdir()
        cases.append(("directory", directory, 100, None))

        missing = root / "missing"
        cases.append(("missing", missing, 100, None))

        symlink = root / "symlink"
        symlink.symlink_to(regular)
        cases.append(("symlink", symlink, 100, None))

        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        cases.append(("hardlink", hardlink, 100, None))

        oversized = root / "oversized"
        oversized.write_bytes(b"xx")
        cases.append(("oversized", oversized, 1, None))

        fifo = root / "fifo"
        os.mkfifo(fifo)
        cases.append(("fifo", fifo, 100, None))

        for label, path, maximum, parent in cases:
            labels.append(label)
            try:
                guarded_read(path, maximum, parent)
            except (VerificationFailure, FileNotFoundError):
                rejected += 1
    return {
        "attack_count": len(labels),
        "rejected_count": rejected,
        "attack_labels": labels,
    }


def atomic_write(raw: bytes) -> None:
    require(OUTPUT.parent == HERE, "output parent")
    if OUTPUT.exists() or OUTPUT.is_symlink():
        info = OUTPUT.lstat()
        require(
            stat.S_ISREG(info.st_mode)
            and not OUTPUT.is_symlink()
            and info.st_nlink == 1,
            "safe existing output",
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        dir=HERE,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=264_071)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    require(isinstance(arguments.seed, int), "integer seed")

    producer_raw = guarded_read(PRODUCER, 5_000_000)
    require(
        hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    del producer_raw

    # Expected semantics are complete before candidate bytes are opened.
    expected = reconstruct_expected()
    expected_result_sha256 = fingerprint(expected)
    require(
        expected_result_sha256 == CANDIDATE_RESULT_SHA256,
        "independently reconstructed result pin",
    )

    candidate_raw = guarded_read(CANDIDATE, 800_000_000)
    require(
        hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA256,
        "candidate file pin",
    )
    candidate = parse_strict(candidate_raw, CANDIDATE.name)
    require(canonical_line(candidate_raw, candidate), "canonical candidate bytes")
    require(candidate_matches(candidate, expected), "complete expected equality")
    require(
        candidate["result_sha256"] == CANDIDATE_RESULT_SHA256,
        "candidate result fixed pin",
    )
    del candidate_raw
    gc.collect()

    semantic = semantic_attack_suite(candidate, expected)
    require(
        semantic["rejected_count"] == semantic["attack_count"],
        "semantic attacks",
    )
    require(candidate_matches(candidate, expected), "candidate restored")
    strict_attacks = strict_json_attack_suite()
    require(
        strict_attacks["rejected_count"] == strict_attacks["attack_count"],
        "strict JSON attacks",
    )
    file_attacks = file_attack_suite()
    require(
        file_attacks["rejected_count"] == file_attacks["attack_count"],
        "file attacks",
    )

    census = expected["census"]
    verification = {
        "status": "PASS_INDEPENDENT_ROUND264",
        "producer_file_sha256": PRODUCER_SHA256,
        "candidate_file_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "independently_reconstructed_result_sha256":
            expected_result_sha256,
        "verified_census": {
            "empty_endpoint_bulk_node_count":
                census["empty_endpoint_bulk_node_count"],
            "dropped_singleton_component_count":
                census[
                    "dropped_empty_EVENT_PRESENT_singleton_component_count"
                ],
            "endpoint_sheet_identity_edge_count":
                census["endpoint_sheet_identity_edge_count"],
            "endpoint_sheet_identity_rank_reduction_count":
                census["endpoint_sheet_identity_rank_reduction_count"],
            "Round204_tail_glue_edge_count":
                census["Round204_tail_glue_edge_count"],
            "Round204_tail_glue_rank_reduction_count":
                census["Round204_tail_glue_rank_reduction_count"],
            "post_Round264_component_count":
                census["post_Round264_component_count"],
            "occurrence_frontier_count":
                census["complete_occurrence_frontier_count"],
            "exact_key_frontier_count":
                census["complete_exact_key_frontier_count"],
            "valid_virtual_node_frontier_count":
                census["complete_valid_virtual_node_frontier_count"],
        },
        "verified_ledger_row_counts": {
            key: value["row_count"]
            for key, value in expected.items()
            if isinstance(value, dict) and "rows" in value
        },
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_attacks,
        "file_attack_suite": file_attacks,
        "independence_contract": {
            "Round264_producer_imported_or_executed": False,
            "expected_object_reconstructed_before_candidate_open": True,
            "complete_expected_object_equality_required": True,
            "complete_candidate_canonical_bytes_required": True,
            "all_upstream_files_schema_result_and_file_pinned": True,
            "exact_arithmetic": "fractions.Fraction",
            "seed_affects_output": False,
        },
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": fingerprint(verification),
    }
    raw = encoded(envelope) + b"\n"
    if not arguments.no_write:
        atomic_write(raw)
    print(verification["status"])
    print(
        "components=68716_to_68312 empty_nodes=400 "
        "sheet_edges=248 tail_edges=32 frontiers=53968/116/133284"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (VerificationFailure, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL_CLOSED_ROUND264_VERIFIER:{error}", file=sys.stderr)
        raise SystemExit(1)
