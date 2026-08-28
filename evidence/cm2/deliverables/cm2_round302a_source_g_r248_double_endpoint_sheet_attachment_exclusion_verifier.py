#!/usr/bin/env python3
"""Independent verifier for the Round302-A double-sheet exclusion gate.

The candidate producer is never imported, executed, tokenized, or parsed.
Its bytes are treated only as a fixed SHA-256 commitment.  Expected rows and
bytes are reconstructed first from the complete pinned upstream frontiers.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round302a_source_g_r248_double_endpoint_sheet_"
    "attachment_exclusion"
)
PRODUCER = PREFIX + ".py"
LEDGER = PREFIX + "_ledger.json.gz"
RESULT = PREFIX + "_result.json"
ATTACKS = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
SCHEMA = (
    "cm2.round302a.source-g-r248-double-endpoint-sheet-"
    "attachment-exclusion.v1"
)
PRODUCER_SHA256 = (
    "8b1feab487ea333ccdfce3051db623f303b674d8dccc5ac36039208ca4e8171f"
)

R234 = (
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_certificate.json"
)
R236 = (
    "cm2_round236_source_g_wall_residual_closure_and_"
    "root_key_partition_certificate.json"
)
R248 = (
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_certificate.json"
)
R266 = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R291 = (
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_ledger.json.gz"
)
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R300C = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_witness_ledger.json.gz"
)

FILE_PINS = {
    R234:
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    R236:
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248:
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    R266:
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R291:
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R295A:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R300C:
        "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2",
}
MANIFEST_PINS = {
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_manifest.sha256":
        "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432",
    "cm2_round236_source_g_wall_residual_closure_and_"
    "root_key_partition_manifest.sha256":
        "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_manifest.sha256":
        "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256":
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_manifest.sha256":
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_manifest.sha256":
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
}
COMMITMENTS = {
    "R248": (
        38_360,
        "fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61",
        "be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0",
        "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b",
    ),
    "R266": (
        133_284,
        "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
        "8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5",
    ),
    "R291": (
        55_428,
        "dc1abc74dde77cf7d114cacbd942a55527d90cf722efc6c679de58beffe8d11e",
        "3c47783f6e00c7c0aa3c1ee577f31ba6ca37a4a73ddea420e1211705fc8576fa",
        "a347c5423b857d4b8aeaae6f48e5d2f6ef81caf15a9329ff0909df77258a4279",
    ),
    "R295A": (
        113_452,
        "a0f471c84148d57eba4511efd8b343eb152c9378a24e018b9f0be10e41525805",
        "7eab57334f6f5170ffaef60316250078cd6774cdabdb7279d3585267345e5258",
        "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
    ),
    "R300C": (
        6_322,
        "54147f135d32ab8326d2bee9d75994086cb7e137dd3350d75a9a2663d56699b6",
        "b1c09d20d57ff7f4fee44a0f915929be5810fcbdc6d3014e66467a6e747f5800",
        "849b2b8d51571c2be4280354b7b260d8d9f52e2793ae08cd393d1dcf9e97e5b2",
    ),
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def tokens(value: Any) -> Iterable[bytes]:
    for token in ENCODER.iterencode(value):
        yield token.encode("utf-8")


def encode(value: Any) -> bytes:
    return b"".join(tokens(value))


def sha_obj(value: Any) -> str:
    state = hashlib.sha256()
    for token in tokens(value):
        state.update(token)
    return state.hexdigest()


def sha_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def guarded(path: Path, maximum: int = 3_000_000_000) -> None:
    require(path.parent.resolve() == HERE.resolve(), "guard:HERE")
    info = os.lstat(path)
    require(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "guard:file:" + path.name,
    )


def strict_json_bytes(
    raw: bytes,
    label: str,
    *,
    expected_canonical: bytes | None = None,
) -> dict[str, Any]:
    require(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "json:strict-bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "json:duplicate-key:" + label)
            output[key] = value
        return output

    def reject_number(token: str) -> Any:
        raise VerificationError("json:noninteger:" + label)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("json:decode:" + label) from error
    require(type(value) is dict, "json:top-object:" + label)
    if expected_canonical is not None:
        require(
            raw == expected_canonical == encode(value),
            "json:canonical-bytes:" + label,
        )
    return value


def strict_gzip_candidate(
    raw: bytes,
    expected_gzip: bytes,
    expected_json: bytes,
    label: str,
) -> dict[str, Any]:
    # Exact deterministic gzip equality rejects alternate headers, multiple
    # members, trailing bytes, truncation, and recompression variants.
    require(raw == expected_gzip, "gzip:canonical-bytes:" + label)
    try:
        expanded = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise VerificationError("gzip:decode:" + label) from error
    return strict_json_bytes(
        expanded,
        label,
        expected_canonical=expected_json,
    )


def boundary_path_guard(path: Path, allowed: Path) -> None:
    require(path.parent.resolve() == allowed.resolve(), "path:escape")
    info = os.lstat(path)
    require(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1,
        "path:not-regular-single-link",
    )


def row_closed(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    claimed = payload.pop("row_sha256", None)
    require(
        isinstance(claimed, str) and sha_obj(payload) == claimed,
        "closure:" + label,
    )


class ArrayCommit:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def push(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for token in tokens(value):
            self.state.update(token)
        self.count += 1

    def final(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def scan_array(
    stream: TextIO,
    marker: str,
    nested: bool,
) -> Iterator[dict[str, Any]]:
    data = ""
    while marker not in data:
        block = stream.read(1 << 20)
        require(bool(block), "scan:marker")
        data = (data + block)[-(len(marker) + (2 << 20)) :]
    data = data.split(marker, 1)[1]
    if nested:
        while '"rows":[' not in data:
            block = stream.read(1 << 20)
            require(bool(block), "scan:nested")
            data += block
        data = data.split('"rows":[', 1)[1]
    decoder = json.JSONDecoder(
        parse_float=lambda value: (_ for _ in ()).throw(
            VerificationError("scan:float:" + value)
        ),
        parse_constant=lambda value: (_ for _ in ()).throw(
            VerificationError("scan:constant:" + value)
        ),
    )
    while True:
        data = data.lstrip()
        if not data:
            block = stream.read(1 << 20)
            require(bool(block), "scan:truncated")
            data = block
            continue
        if data[0] == ",":
            data = data[1:]
            continue
        if data[0] == "]":
            return
        while True:
            try:
                row, end = decoder.raw_decode(data)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                require(bool(block), "scan:row")
                data += block
        require(type(row) is dict, "scan:object")
        yield row
        data = data[end:]


def rows_from(
    filename: str,
    id_field: str,
    expected: tuple[int, str, str, str],
    table: str | None = None,
) -> Iterator[dict[str, Any]]:
    row_state = ArrayCommit()
    id_state = ArrayCommit()
    hash_state = ArrayCommit()
    seen: set[str] = set()
    opener = (
        (lambda: gzip.open(HERE / filename, "rt", encoding="utf-8"))
        if filename.endswith(".gz")
        else (lambda: (HERE / filename).open("rt", encoding="utf-8"))
    )
    with opener() as stream:
        for row in scan_array(
            stream,
            f'"{table}":' if table else '"rows":[',
            table is not None,
        ):
            row_closed(row, filename)
            row_id = row[id_field]
            require(
                isinstance(row_id, str) and row_id not in seen,
                "scan:unique:" + filename,
            )
            seen.add(row_id)
            row_state.push(row)
            id_state.push(row_id)
            hash_state.push(row["row_sha256"])
            yield row
    require(
        (
            row_state.count,
            id_state.final(),
            hash_state.final(),
            row_state.final(),
        ) == expected,
        "scan:commit:" + filename,
    )


def wrapped_result(filename: str) -> dict[str, Any]:
    guarded(HERE / filename)
    document = json.loads((HERE / filename).read_text(encoding="utf-8"))
    require(type(document.get("result")) is dict, "wrapper:" + filename)
    require(
        document.get("result_sha256") == sha_obj(document["result"]),
        "wrapper:self:" + filename,
    )
    return document["result"]


def rectangle_relation(a: list[str], b: list[str]) -> str:
    left = [Fraction(value) for value in a]
    right = [Fraction(value) for value in b]
    dp = min(left[1], right[1]) - max(left[0], right[0])
    ds = min(left[3], right[3]) - max(left[2], right[2])
    if left == right:
        return "EXACT_EQUAL"
    if dp > 0 and ds > 0:
        return "STRICT_POSITIVE_AREA_INTERSECTION"
    if dp >= 0 and ds >= 0:
        return "CLOSED_BOUNDARY_CONTACT_ONLY"
    return "DISJOINT"


def seal_row(payload: dict[str, Any]) -> dict[str, Any]:
    output = dict(payload)
    output["row_sha256"] = sha_obj(payload)
    return output


def verify_inputs() -> None:
    for filename, pin in {**FILE_PINS, **MANIFEST_PINS}.items():
        guarded(HERE / filename)
        require(sha_file(HERE / filename) == pin, "pin:" + filename)


def independent_rebuild() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    verify_inputs()
    source236 = wrapped_result(R236)
    doubles_list = source236["double_endpoint_partition_rows"]
    require(
        len(doubles_list) == 16
        and sha_obj(doubles_list)
        == "68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6",
        "R236:double",
    )
    doubles = {
        row["double_endpoint_partition_row_id"]: row
        for row in doubles_list
    }
    require(len(doubles) == 16, "R236:unique")

    source234 = wrapped_result(R234)
    all_frontiers = source234["depth6_frontier_rows"]
    require(
        len(all_frontiers) == 38_376
        and sha_obj(all_frontiers)
        == "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6",
        "R234:frontiers",
    )
    wanted = {row["Round234_frontier_row_id"] for row in doubles_list}
    frontiers = {
        row["frontier_row_id"]: row
        for row in all_frontiers
        if row["frontier_row_id"] in wanted
    }
    require(len(frontiers) == 16, "R234:join")

    selected: list[dict[str, Any]] = []
    kinds: Counter[str] = Counter()
    for row in rows_from(
        R248,
        "wall_sheet_node_id",
        COMMITMENTS["R248"],
        "formal_wall_half_open_sheet_owner_ledger",
    ):
        kinds[row["source_partition_kind"]] += 1
        if (
            row["source_partition_kind"]
            == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"
        ):
            selected.append(row)
    require(
        kinds
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        }
        and len(selected) == 32,
        "R248:partition",
    )

    records: dict[str, dict[str, Any]] = {}
    lineage: dict[tuple[str, str], list[str]] = defaultdict(list)
    factors: dict[str, set[str]] = defaultdict(set)
    for sheet in selected:
        source = doubles[sheet["source_partition_row_id"]]
        frontier = frontiers[source["Round234_frontier_row_id"]]
        require(
            sheet["Round220_split_interface_id"]
            == source["Round220_split_interface_id"]
            == frontier["Round220_split_interface_id"],
            "lineage:interface",
        )
        require(
            sheet["endpoint_factor"] in {"source", "target"}
            and sheet["owner_signature_sha256"]
            == sha_obj(source["same_sign_event_absent_signature"])
            and sheet["owner_official_key_id"]
            == source["same_sign_event_absent_signature"]["official_key_id"],
            "lineage:owner",
        )
        require(
            sheet["exact_closed_base_rectangle"] == frontier["box"][2:6]
            and Fraction(sheet["exact_positive_2D_sheet_area"]) > 0
            and sheet["sheet_three_dimensional_coordinate_volume"] == "0",
            "lineage:geometry",
        )
        sheet_id = sheet["wall_sheet_node_id"]
        records[sheet_id] = {
            "sheet": sheet,
            "source": source,
            "frontier": frontier,
        }
        lineage[(
            frontier["Round179_retained_child_row_id"],
            frontier["chart"],
        )].append(sheet_id)
        factors[source["double_endpoint_partition_row_id"]].add(
            sheet["endpoint_factor"]
        )
    require(
        len(records) == 32
        and len(factors) == 16
        and all(value == {"source", "target"} for value in factors.values()),
        "lineage:factors",
    )

    node_ids = set(records)
    node_ids.update(
        value["sheet"]["owner_wall_bulk_node_id"]
        for value in records.values()
    )
    virtual: dict[str, dict[str, Any]] = {}
    for row in rows_from(
        R266,
        "post_Round266_valid_virtual_node_frontier_row_id",
        COMMITMENTS["R266"],
        "formal_post_Round266_valid_virtual_node_frontier_ledger",
    ):
        if row["valid_virtual_stratum_node_id"] in node_ids:
            virtual[row["valid_virtual_stratum_node_id"]] = row
    require(len(virtual) == 48, "R266:selected")
    for sheet_id, value in records.items():
        sheet = value["sheet"]
        srow = virtual[sheet_id]
        brow = virtual[sheet["owner_wall_bulk_node_id"]]
        require(
            srow["virtual_node_kind"] == "ROUND248_WALL_SHEET"
            and brow["virtual_node_kind"] == "ROUND248_WALL_BULK"
            and srow["post_Round266_quotient_component_id"]
            == brow["post_Round266_quotient_component_id"],
            "R266:internal-owner",
        )
        value["sheet_virtual"] = srow
        value["bulk_virtual"] = brow

    lineage_hit: Counter[str] = Counter()
    positive_hit: Counter[str] = Counter()
    closed_hit: Counter[str] = Counter()
    physical_keys: set[tuple[str, int]] = set()
    for disposition in rows_from(
        R291,
        "complete_lower_stratum_local_disposition_row_id",
        COMMITMENTS["R291"],
    ):
        did = disposition[
            "complete_lower_stratum_local_disposition_row_id"
        ]
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            box = cell.get("exact_box")
            if not isinstance(box, list) or len(box) != 6:
                continue
            for sheet_id in lineage.get((
                cell["retained_child_row_id"],
                disposition["source_chart"],
            ), []):
                lineage_hit[sheet_id] += 1
                kind = rectangle_relation(
                    records[sheet_id]["sheet"][
                        "exact_closed_base_rectangle"
                    ],
                    box[2:6],
                )
                if kind in {
                    "EXACT_EQUAL",
                    "STRICT_POSITIVE_AREA_INTERSECTION",
                }:
                    positive_hit[sheet_id] += 1
                    physical_keys.add((did, index))
                elif kind == "CLOSED_BOUNDARY_CONTACT_ONLY":
                    closed_hit[sheet_id] += 1
    require(
        not lineage_hit
        and not positive_hit
        and not closed_hit
        and not physical_keys,
        "R291:no-candidate",
    )

    binding_count = 0
    for row in rows_from(
        R295A,
        "Round295A_R291_physical_incidence_binding_row_id",
        COMMITMENTS["R295A"],
    ):
        if (
            row["Round291_local_disposition_row_id"],
            row["physical_witness_cell_index"],
        ) in physical_keys:
            binding_count += 1
    require(binding_count == 0, "R295A:no-candidate")

    direct: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bulk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bulk_ids = {
        value["sheet"]["owner_wall_bulk_node_id"]
        for value in records.values()
    }
    for row in rows_from(
        R300C,
        "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        COMMITMENTS["R300C"],
    ):
        node = row["virtual_stratum_node_id"]
        if node in records:
            direct[node].append(row)
        if node in bulk_ids:
            bulk[node].append(row)
    require(
        not direct
        and len(bulk) == 8
        and sum(map(len, bulk.values())) == 8
        and all(len(value) == 1 for value in bulk.values()),
        "R300C:context",
    )

    output: list[dict[str, Any]] = []
    reason = (
        "NO_ROUND291_SAME_LINEAGE_PHYSICAL_CELL__"
        "NO_R295A_OCCURRENCE_CANDIDATE__"
        "NO_R300C_DIRECT_SHEET_WITNESS"
    )
    for sheet_id in sorted(records):
        value = records[sheet_id]
        sheet = value["sheet"]
        source = value["source"]
        frontier = value["frontier"]
        srow = value["sheet_virtual"]
        brow = value["bulk_virtual"]
        context = bulk.get(sheet["owner_wall_bulk_node_id"], [])
        payload = {
            "Round302A_double_endpoint_sheet_exclusion_row_id":
                "round302a-double-endpoint-sheet-exclusion:"
                + sha_obj([sheet_id, sheet["row_sha256"]]),
            "source_Round248_wall_sheet_node_id": sheet_id,
            "source_Round248_wall_sheet_row_sha256": sheet["row_sha256"],
            "source_Round236_double_endpoint_partition_row_id":
                source["double_endpoint_partition_row_id"],
            "source_Round234_frontier_row_id": frontier["frontier_row_id"],
            "Round220_split_interface_id":
                sheet["Round220_split_interface_id"],
            "Round179_retained_child_row_id":
                frontier["Round179_retained_child_row_id"],
            "source_chart": frontier["chart"],
            "endpoint_factor": sheet["endpoint_factor"],
            "exact_closed_base_rectangle":
                sheet["exact_closed_base_rectangle"],
            "owner_signature_sha256": sheet["owner_signature_sha256"],
            "owner_official_key_id": sheet["owner_official_key_id"],
            "owner_wall_bulk_node_id": sheet["owner_wall_bulk_node_id"],
            "post_Round266_sheet_component_id":
                srow["post_Round266_quotient_component_id"],
            "post_Round266_owner_bulk_component_id":
                brow["post_Round266_quotient_component_id"],
            "sheet_owner_bulk_already_internal_in_Round266": True,
            "R291_same_retained_child_and_chart_cell_count": 0,
            "R291_strict_positive_area_or_equal_base_candidate_count": 0,
            "R291_closed_boundary_contact_only_count": 0,
            "R295A_occurrence_attachment_candidate_count": 0,
            "R300C_direct_sheet_positive_volume_witness_count": 0,
            "R300C_owner_bulk_context_witness_count": len(context),
            "R300C_owner_bulk_context_witness_row_ids": [
                row[
                    "Round300C_virtual_occurrence_"
                    "positive_volume_witness_row_id"
                ]
                for row in context
            ],
            "R300C_owner_bulk_context_occurrence_ids": [
                row["Round294_registry_occurrence_id"] for row in context
            ],
            "owner_bulk_witness_transfer_to_sheet_credit": 0,
            "raw_owner_edge_reissued_as_occurrence_attachment_credit": 0,
            "attachment_exclusion_reason": reason,
            "eligible_for_component_DSU_application": False,
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        output.append(seal_row(payload))

    ledger_meta = {
        "filename": LEDGER,
        "row_count": 32,
        "row_ids_sha256": sha_obj([
            row["Round302A_double_endpoint_sheet_exclusion_row_id"]
            for row in output
        ]),
        "row_hashes_sha256": sha_obj([
            row["row_sha256"] for row in output
        ]),
        "rows_sha256": sha_obj(output),
        "schema": SCHEMA + ".ledger.v1",
    }
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND302A_EXACT_32_R248_DOUBLE_ENDPOINT_SHEETS__"
            "ALL_OCCURRENCE_ATTACHMENTS_EXCLUDED_FAIL_CLOSED",
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(FILE_PINS.items())),
        "complete_frontier_census": {
            "Round236_double_endpoint_partition_count": 16,
            "Round248_complete_wall_sheet_count": 38_360,
            "Round248_single_endpoint_sheet_count": 38_328,
            "Round248_double_endpoint_sheet_count": 32,
            "Round248_double_endpoint_owner_bulk_count": 16,
            "Round266_selected_virtual_node_count": 48,
            "Round266_sheet_owner_internal_component_pair_count": 32,
            "Round291_same_retained_child_and_chart_cell_count": 0,
            "Round291_positive_area_or_equal_base_candidate_count": 0,
            "Round291_closed_boundary_contact_only_count": 0,
            "Round295A_occurrence_attachment_candidate_count": 0,
            "Round300C_direct_sheet_positive_volume_witness_count": 0,
            "Round300C_owner_bulk_context_witness_count": 8,
            "Round300C_owner_bulk_context_witnessed_bulk_count": 8,
            "unresolved_sheet_count": 0,
        },
        "scope_contract": {
            "all_32_double_endpoint_sheets_reconstructed_from_R248": True,
            "both_source_and_target_factor_sheets_per_R236_partition": True,
            "R291_complete_physical_cell_frontier_streamed": True,
            "R295A_complete_physical_binding_frontier_streamed": True,
            "R300C_complete_positive_volume_witness_frontier_streamed": True,
            "R300E_legal_graph_attachment_predicate_reopened": True,
            "same_retained_child_and_source_chart_are_mandatory_first_stage":
                True,
            "exact_base_predicate_equation_and_owner_signature_are_required_"
            "after_first_stage": True,
            "first_stage_candidate_count_is_zero_so_later_predicates_cannot_"
            "be_bypassed": True,
            "owner_bulk_positive_volume_witness_is_not_sheet_attachment":
                True,
            "Round266_internal_sheet_owner_edge_is_not_occurrence_attachment":
                True,
            "no_spike_import_execute_or_parse": True,
        },
        "formal_credit_transition": {
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "ledger": ledger_meta,
        "provenance": {
            "seed_affects_output": False,
            "Round301_or_R302_maximality_artifact_read": False,
            "spike_imported_executed_or_parsed": False,
        },
    }
    result["result_sha256"] = sha_obj(result)
    return output, result


def ledger_document(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "every_row_closed_by_own_SHA256": True,
        "row_count": len(rows),
        "row_hashes_sha256": sha_obj([
            row["row_sha256"] for row in rows
        ]),
        "row_ids_sha256": sha_obj([
            row["Round302A_double_endpoint_sheet_exclusion_row_id"]
            for row in rows
        ]),
        "rows": rows,
        "rows_sha256": sha_obj(rows),
        "schema": SCHEMA + ".ledger.v1",
        "status": "COMPLETE_32_ROW_FAIL_CLOSED_EXCLUSION",
    }


def gzip_bytes(document: dict[str, Any]) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(encode(document))
    return output.getvalue()


ZERO_FIELDS = (
    "R291_same_retained_child_and_chart_cell_count",
    "R291_strict_positive_area_or_equal_base_candidate_count",
    "R291_closed_boundary_contact_only_count",
    "R295A_occurrence_attachment_candidate_count",
    "R300C_direct_sheet_positive_volume_witness_count",
    "owner_bulk_witness_transfer_to_sheet_credit",
    "raw_owner_edge_reissued_as_occurrence_attachment_credit",
    "formal_component_edge_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_occurrence_identity_collapse_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


def semantic_audit(
    rows: list[dict[str, Any]],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    expected_result: dict[str, Any],
) -> None:
    require(len(rows) == 32, "semantic:row-count")
    require(
        len({
            row["source_Round248_wall_sheet_node_id"] for row in rows
        }) == 32,
        "semantic:sheet-partition",
    )
    reason = (
        "NO_ROUND291_SAME_LINEAGE_PHYSICAL_CELL__"
        "NO_R295A_OCCURRENCE_CANDIDATE__"
        "NO_R300C_DIRECT_SHEET_WITNESS"
    )
    context_total = 0
    for row in rows:
        row_closed(row, "semantic")
        require(
            row["sheet_owner_bulk_already_internal_in_Round266"] is True
            and row["post_Round266_sheet_component_id"]
            == row["post_Round266_owner_bulk_component_id"],
            "semantic:base-internal",
        )
        require(
            row["attachment_exclusion_reason"] == reason
            and row["eligible_for_component_DSU_application"] is False,
            "semantic:exclusion",
        )
        require(
            all(row[field] == 0 for field in ZERO_FIELDS),
            "semantic:zero-credit",
        )
        count = row["R300C_owner_bulk_context_witness_count"]
        require(
            count in {0, 1}
            and len(row["R300C_owner_bulk_context_witness_row_ids"]) == count
            and len(row["R300C_owner_bulk_context_occurrence_ids"]) == count,
            "semantic:bulk-context",
        )
        context_total += count
    require(context_total == 16, "semantic:two-sheets-per-eight-bulks")
    payload = dict(result)
    claimed = payload.pop("result_sha256", None)
    require(claimed == sha_obj(payload), "semantic:result-closure")
    require(
        result["complete_frontier_census"]["unresolved_sheet_count"] == 0
        and result["formal_credit_transition"]
        == expected_result["formal_credit_transition"],
        "semantic:result-nonclaim",
    )
    require(rows == expected_rows, "semantic:independent-row-equality")
    require(result == expected_result, "semantic:independent-result-equality")


def reseal(
    rows: list[dict[str, Any]],
    result: dict[str, Any],
) -> None:
    for index, row in enumerate(rows):
        payload = dict(row)
        payload.pop("row_sha256", None)
        rows[index] = seal_row(payload)
    result["ledger"]["row_count"] = len(rows)
    result["ledger"]["row_ids_sha256"] = sha_obj([
        row["Round302A_double_endpoint_sheet_exclusion_row_id"]
        for row in rows
    ])
    result["ledger"]["row_hashes_sha256"] = sha_obj([
        row["row_sha256"] for row in rows
    ])
    result["ledger"]["rows_sha256"] = sha_obj(rows)
    result.pop("result_sha256", None)
    result["result_sha256"] = sha_obj(result)


def run_attacks(
    expected_rows: list[dict[str, Any]],
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[
        tuple[str, Callable[[list[dict[str, Any]], dict[str, Any]], None]]
    ] = [
        ("inherit_sheet_to_bulk_witness",
         lambda r, s: r[0].__setitem__(
             "owner_bulk_witness_transfer_to_sheet_credit", 1)),
        ("raw_owner_edge_credit",
         lambda r, s: r[0].__setitem__(
             "raw_owner_edge_reissued_as_occurrence_attachment_credit", 1)),
        ("closed_contact_as_2d_attachment",
         lambda r, s: r[0].__setitem__(
             "R291_closed_boundary_contact_only_count", 1)),
        ("positive_area_candidate_forgery",
         lambda r, s: r[0].__setitem__(
             "R291_strict_positive_area_or_equal_base_candidate_count", 1)),
        ("same_lineage_cell_forgery",
         lambda r, s: r[0].__setitem__(
             "R291_same_retained_child_and_chart_cell_count", 1)),
        ("R295A_occurrence_candidate_forgery",
         lambda r, s: r[0].__setitem__(
             "R295A_occurrence_attachment_candidate_count", 1)),
        ("direct_sheet_witness_forgery",
         lambda r, s: r[0].__setitem__(
             "R300C_direct_sheet_positive_volume_witness_count", 1)),
        ("wrong_chart",
         lambda r, s: r[0].__setitem__("source_chart", "G:FORGED")),
        ("wrong_retained_child",
         lambda r, s: r[0].__setitem__(
             "Round179_retained_child_row_id", "forged-child")),
        ("wrong_R236_partition",
         lambda r, s: r[0].__setitem__(
             "source_Round236_double_endpoint_partition_row_id",
             "forged-partition")),
        ("wrong_R248_sheet_hash",
         lambda r, s: r[0].__setitem__(
             "source_Round248_wall_sheet_row_sha256", "0" * 64)),
        ("wrong_base_rectangle",
         lambda r, s: r[0].__setitem__(
             "exact_closed_base_rectangle", ["0", "1", "0", "1"])),
        ("wrong_owner_signature",
         lambda r, s: r[0].__setitem__(
             "owner_signature_sha256", "0" * 64)),
        ("wrong_owner_key",
         lambda r, s: r[0].__setitem__(
             "owner_official_key_id", "forged-key")),
        ("wrong_owner_bulk",
         lambda r, s: r[0].__setitem__(
             "owner_wall_bulk_node_id", "forged-bulk")),
        ("component_mismatch",
         lambda r, s: r[0].__setitem__(
             "post_Round266_sheet_component_id", "forged-component")),
        ("grant_edge_credit",
         lambda r, s: r[0].__setitem__("formal_component_edge_credit", 1)),
        ("grant_union_credit",
         lambda r, s: r[0].__setitem__("formal_component_union_credit", 1)),
        ("grant_rank_credit",
         lambda r, s: r[0].__setitem__(
             "formal_DSU_rank_reduction_credit", 1)),
        ("grant_identity_credit",
         lambda r, s: r[0].__setitem__(
             "formal_occurrence_identity_collapse_credit", 1)),
        ("grant_maximality_credit",
         lambda r, s: r[0].__setitem__("formal_maximality_credit", 1)),
        ("grant_fibre_credit",
         lambda r, s: r[0].__setitem__("formal_fibre_credit", 1)),
        ("grant_disposition_credit",
         lambda r, s: r[0].__setitem__(
             "formal_global_disposition_credit", 1)),
        ("feed_to_DSU",
         lambda r, s: r[0].__setitem__(
             "eligible_for_component_DSU_application", True)),
        ("erase_exclusion_reason",
         lambda r, s: r[0].__setitem__(
             "attachment_exclusion_reason", "FORGED")),
        ("drop_sheet", lambda r, s: r.pop()),
        ("duplicate_sheet", lambda r, s: r.append(deepcopy(r[0]))),
        ("swap_endpoint_factor",
         lambda r, s: r[0].__setitem__(
             "endpoint_factor",
             "target" if r[0]["endpoint_factor"] == "source" else "source")),
        ("forge_bulk_context_count",
         lambda r, s: r[0].__setitem__(
             "R300C_owner_bulk_context_witness_count", 2)),
        ("grant_result_maximality",
         lambda r, s: s["formal_credit_transition"].__setitem__(
             "formal_maximality_credit", 1)),
        ("claim_unresolved",
         lambda r, s: s["complete_frontier_census"].__setitem__(
             "unresolved_sheet_count", 1)),
        ("erase_no_spike_boundary",
         lambda r, s: s["scope_contract"].__setitem__(
             "no_spike_import_execute_or_parse", False)),
    ]
    outcomes: list[dict[str, Any]] = []
    for label, mutate in attacks:
        rows = deepcopy(expected_rows)
        result = deepcopy(expected_result)
        mutate(rows, result)
        reseal(rows, result)
        rejected = False
        guard = ""
        try:
            semantic_audit(rows, result, expected_rows, expected_result)
        except VerificationError as error:
            rejected = True
            guard = str(error)
        require(rejected, "attack accepted:" + label)
        outcomes.append({
            "attack": label,
            "rejected": True,
            "guard": guard,
        })
    suite = {
        "schema": SCHEMA + ".attack-suite.v1",
        "attack_count": len(outcomes),
        "rejected_attack_count": len(outcomes),
        "all_attacks_rejected": True,
        "semantic_reclosed_attack_count": len(outcomes),
        "attacks": outcomes,
    }
    suite["attack_suite_sha256"] = sha_obj(suite)
    return suite


def run_boundary_attacks(
    expected_ledger_gzip: bytes,
    expected_ledger_json: bytes,
) -> list[dict[str, Any]]:
    cases: list[tuple[str, Callable[[], None]]] = []

    def expect_json(raw: bytes, label: str) -> Callable[[], None]:
        return lambda: strict_json_bytes(raw, label)

    cases.extend([
        (
            "json_duplicate_key",
            expect_json(b'{"a":1,"a":2}', "attack"),
        ),
        (
            "json_float",
            expect_json(b'{"a":1.5}', "attack"),
        ),
        (
            "json_NaN",
            expect_json(b'{"a":NaN}', "attack"),
        ),
        (
            "json_NUL",
            expect_json(b'{"a":1}\x00', "attack"),
        ),
        (
            "json_trailing_token",
            expect_json(b'{"a":1}x', "attack"),
        ),
        (
            "json_BOM",
            expect_json(b'\xef\xbb\xbf{"a":1}', "attack"),
        ),
    ])

    def gzip_case(raw: bytes) -> Callable[[], None]:
        return lambda: strict_gzip_candidate(
            raw,
            expected_ledger_gzip,
            expected_ledger_json,
            "attack",
        )

    cases.extend([
        ("gzip_truncated", gzip_case(expected_ledger_gzip[:-1])),
        ("gzip_trailing_byte", gzip_case(expected_ledger_gzip + b"x")),
        (
            "gzip_multi_member",
            gzip_case(expected_ledger_gzip + expected_ledger_gzip),
        ),
        (
            "gzip_noncanonical_header_mtime",
            gzip_case(
                expected_ledger_gzip[:4]
                + b"\x01\x00\x00\x00"
                + expected_ledger_gzip[8:]
            ),
        ),
    ])

    path_labels: list[tuple[str, str]] = [
        ("path_symlink", "symlink"),
        ("path_hardlink", "hardlink"),
        ("path_directory", "directory"),
        ("path_parent_escape", "escape"),
    ]
    for label, kind in path_labels:
        def run_path(kind: str = kind) -> None:
            with tempfile.TemporaryDirectory(
                dir=HERE,
                prefix=".r302a-boundary-",
            ) as temporary:
                allowed = Path(temporary)
                source = allowed / "source"
                source.write_bytes(b"x")
                if kind == "symlink":
                    candidate = allowed / "candidate"
                    candidate.symlink_to(source.name)
                elif kind == "hardlink":
                    candidate = allowed / "candidate"
                    os.link(source, candidate)
                elif kind == "directory":
                    candidate = allowed / "candidate"
                    candidate.mkdir()
                else:
                    candidate = HERE / "outside-r302a-boundary"
                    candidate.write_bytes(b"x")
                    try:
                        boundary_path_guard(candidate, allowed)
                    finally:
                        candidate.unlink()
                    return
                boundary_path_guard(candidate, allowed)
        cases.append((label, run_path))

    outcomes: list[dict[str, Any]] = []
    for label, action in cases:
        rejected = False
        guard = ""
        try:
            action()
        except (VerificationError, OSError) as error:
            rejected = True
            if isinstance(error, VerificationError):
                guard = str(error)
            else:
                guard = "path:operating-system-rejection"
        require(rejected, "boundary attack accepted:" + label)
        outcomes.append({
            "attack": label,
            "rejected": True,
            "guard": guard,
        })
    return outcomes


def write_json(name: str, value: dict[str, Any]) -> None:
    path = HERE / name
    work = HERE / (name + ".incomplete")
    if work.exists():
        work.unlink()
    work.write_bytes(encode(value))
    os.replace(work, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="302173")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    require(bool(args.seed), "seed")
    guarded(HERE / PRODUCER)
    require(
        sha_file(HERE / PRODUCER) == PRODUCER_SHA256,
        "producer-fixed-byte-pin",
    )

    expected_rows, expected_result = independent_rebuild()
    expected_ledger = ledger_document(expected_rows)
    expected_ledger_bytes = gzip_bytes(expected_ledger)
    expected_result_bytes = encode(expected_result)

    # Candidate artifacts are opened only after the independent rebuild.
    guarded(HERE / LEDGER)
    guarded(HERE / RESULT)
    require(
        (HERE / LEDGER).read_bytes() == expected_ledger_bytes,
        "candidate-ledger-exact-bytes",
    )
    require(
        (HERE / RESULT).read_bytes() == expected_result_bytes,
        "candidate-result-exact-bytes",
    )
    parsed_ledger = strict_gzip_candidate(
        (HERE / LEDGER).read_bytes(),
        expected_ledger_bytes,
        encode(expected_ledger),
        "candidate-ledger",
    )
    candidate_rows = parsed_ledger["rows"]
    candidate_result = strict_json_bytes(
        (HERE / RESULT).read_bytes(),
        "candidate-result",
        expected_canonical=expected_result_bytes,
    )
    semantic_audit(
        candidate_rows,
        candidate_result,
        expected_rows,
        expected_result,
    )
    attack_suite = run_attacks(expected_rows, expected_result)
    boundary_attacks = run_boundary_attacks(
        expected_ledger_bytes,
        encode(expected_ledger),
    )
    attack_suite.pop("attack_suite_sha256")
    attack_suite["attacks"].extend(boundary_attacks)
    attack_suite["boundary_attack_count"] = len(boundary_attacks)
    attack_suite["parser_and_path_attack_count"] = len(boundary_attacks)
    attack_suite["attack_count"] = len(attack_suite["attacks"])
    attack_suite["rejected_attack_count"] = len(
        attack_suite["attacks"]
    )
    attack_suite["attack_suite_sha256"] = sha_obj(attack_suite)
    verification = {
        "schema": SCHEMA + ".verification.v1",
        "status":
            "PASS_INDEPENDENT_ROUND302A_EXACT_32_SHEET_"
            "FAIL_CLOSED_EXCLUSION__46_OF_46_ATTACKS_REJECTED",
        "producer_treated_only_as_fixed_byte_string": True,
        "producer_imported_executed_tokenized_or_parsed": False,
        "producer_sha256": PRODUCER_SHA256,
        "verifier_file_sha256": sha_file(Path(__file__).resolve()),
        "candidate_file_pins": {
            LEDGER: sha_file(HERE / LEDGER),
            RESULT: sha_file(HERE / RESULT),
        },
        "independent_reconstruction": {
            "expected_row_count": 32,
            "expected_rows_sha256": sha_obj(expected_rows),
            "candidate_exact_bytes_equal": True,
            "complete_R248_R266_R291_R295A_R300C_frontiers_streamed":
                True,
            "direct_sheet_witness_count": 0,
            "owner_bulk_context_witness_count": 8,
            "owner_bulk_context_credit_transferred_to_sheet": 0,
            "unresolved_sheet_count": 0,
        },
        "attack_suite": {
            "filename": ATTACKS,
            "attack_count": attack_suite["attack_count"],
            "rejected_attack_count":
                attack_suite["rejected_attack_count"],
            "semantic_reclosed_attack_count":
                attack_suite["semantic_reclosed_attack_count"],
            "parser_and_path_attack_count":
                attack_suite["parser_and_path_attack_count"],
            "attack_suite_sha256":
                attack_suite["attack_suite_sha256"],
            "attack_suite_file_sha256":
                hashlib.sha256(encode(attack_suite)).hexdigest(),
        },
        "seed_affects_output": False,
    }
    verification["verification_sha256"] = sha_obj(verification)
    if args.write:
        write_json(ATTACKS, attack_suite)
        write_json(VERIFICATION, verification)
    print(encode({
        "status": verification["status"],
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_sha256": attack_suite["attack_suite_sha256"],
        "artifact_written": args.write,
        "seed_affects_output": False,
    }).decode("utf-8"))


if __name__ == "__main__":
    main()
