#!/usr/bin/env python3
"""Round303-A: bind issued occurrence anchors to connected signed sides.

For the Round288/Round288 part of the still-cross-Round301 Round300-D
frontier, this gate proves a deliberately weak bridge:

    a nonempty strict rational subbox B0 of the issued Round294 occurrence
    inner support lies in the uniquely bound formal connected source signed
    region A.

It does *not* claim that the complete support of the issued occurrence equals
A.  It does not promote a component edge.  Eight Round271 W-tail endpoints
lack a serialized connected-side extension and are emitted separately as
unresolved, never as exclusions or nonedges.

All large ledgers are streamed.  Both output ledgers and the result are fully
staged before replacement; the result is replaced last and is the atomic
commit point.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as Q
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, BinaryIO, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge"
BRIDGE_LEDGER = HERE / f"{PREFIX}_bridge_ledger.json.gz"
UNRESOLVED_LEDGER = HERE / f"{PREFIX}_unresolved_bridge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round303a.source-g-occurrence-anchor-connected-side-bridge.v1"
BRIDGE_SCHEMA = SCHEMA + ".materialized-bridge-ledger.v1"
UNRESOLVED_SCHEMA = SCHEMA + ".unresolved-bridge-ledger.v1"
BRIDGE_ID = "Round303A_occurrence_anchor_source_side_bridge_row_id"
UNRESOLVED_ID = "Round303A_unresolved_occurrence_anchor_bridge_row_id"
THEOREM_ID = (
    "ROUND294_CANONICAL_ATOM_OCCURRENCE_ANCHOR_TO_"
    "CONNECTED_SOURCE_SIDE_BRIDGE_V1"
)
UNRESOLVED_DISPOSITION = (
    "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING"
)

R288_KIND = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
PRESERVED_KIND = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
R301_R300D_RELATION = (
    "R300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE"
)
R301_R300D_RESIDUAL_DISPOSITION = (
    "INELIGIBLE_INCIDENCE_ONLY__NO_STRONGER_GATE_PROOF"
)
EXPECTED_R301_R300D_DISPOSITION_HISTOGRAM = {
    R301_R300D_RESIDUAL_DISPOSITION: 110_516,
    (
        "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
        "PAIR_RECLOSED_BY_STRONGER_LEGAL_EDGE"
    ): 736,
    (
        "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
        "AUDITED_FAIL_CLOSED_NO_EDGE"
    ): 272,
}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

EXPECTED_R300D_COUNT = 111_524
EXPECTED_RESIDUAL_R300D_COUNT = 110_516
EXPECTED_CROSS_R301_COUNT = 44_108
EXPECTED_R288_PAIR_COUNT = 43_916
EXPECTED_SELECTED_ENDPOINT_COUNT = 87_832
EXPECTED_BRIDGE_COUNT = 87_824
EXPECTED_UNRESOLVED_COUNT = 8
EXPECTED_SUPPORT_KIND_HISTOGRAM = {
    "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT": 72_712,
    "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT": 15_120,
}
EXPECTED_CONNECTED_CONTRACT_HISTOGRAM = {
    "ROUND269_DIRECT_WHOLE_LEAF_F_SIGN_SIDE": 12_864,
    "ROUND270_DIRECT_WHOLE_LEAF_F_SIGN_SIDE": 26_144,
    "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_WHOLE_F_SIGN_SIDE":
        48_752,
    "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_WHOLE_F_SIGN_SIDE":
        64,
}

MAX_ANCHOR_SPLIT_DEPTH = 18
MAX_ANCHOR_SEARCH_NODES = 4096
PIN_RE = re.compile(r"^[0-9a-f]{64}$")

THEOREM = {
    "conclusion": (
        "A nonempty strict rational subbox B0 of the issued Round294 "
        "occurrence inner support is contained in the uniquely bound formal "
        "connected source signed region A; B0 may be consumed only as an "
        "occurrence anchor for a later separately proved attachment theorem."
    ),
    "credit_boundary": {
        "formal_occurrence_anchor_connected_side_bridge_credit": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
        "formal_component_edge_credit": 0,
        "formal_component_union_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "formal_Jx_Jy_same_point_glue_credit": 0,
    },
    "hypotheses": {
        "A0_exact_provenance_pins_and_row_closures": (
            "The cross-Round301 Round300D scope, Round294 occurrence row, "
            "Round288 disposition, Round279 atom, source-side rows, leaf, "
            "active equation, support-source row, and interval kernel are "
            "all exactly content pinned and row closed."
        ),
        "A1_Round294_issued_occurrence_has_nonempty_inner_anchor": (
            "The formally issued Round294 occurrence carries an exact "
            "positive-volume rational inner-support box B."
        ),
        "A2_strict_anchor_subbox_inside_issued_inner_support": (
            "Independent interval replay constructs a positive-volume "
            "rational B0 contained in B on which the exact active scalar has "
            "the strict sign bound by the source signed-region row."
        ),
        "A3_occurrence_atom_source_side_provenance_exactly_closed": (
            "The Round294 occurrence ID, Round288 disposition, Round279 "
            "canonical atom, leaf, chart, signature, and source-side row all "
            "close to one exact signed-region provenance chain."
        ),
        "A4_unique_formal_connected_source_signed_region_materialized": (
            "The non-W-tail source row materializes the complete connected "
            "active-factor sign side A in the pinned leaf, and B0 has that "
            "same exact active-factor sign."
        ),
    },
    "nonclaims": {
        "full_occurrence_support_equals_connected_source_side": False,
        "component_connectivity_edge": False,
        "occurrence_identity_or_official_key_merge": False,
        "DSU_rank_or_quotient_change": False,
        "maximality_fibre_or_global_disposition": False,
    },
    "theorem_id": THEOREM_ID,
}


ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit",
    "formal_component_edge_credit",
    "formal_component_union_credit",
    "formal_component_quotient_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


INPUT_PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256":
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round179_source_g_residual_tube_arrangement_verification.json":
        "37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256":
        "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_manifest.sha256":
        "99d8eb8260775b3f2e00bfb51790a6db45a1307753183d61173a2307033c407d",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json":
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_verification.json":
        "3435ad2ad0d76f881e7b49fd052fb64035776a991b0f92a542b054f224860982",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_manifest.sha256":
        "a23fc6c40b6a29314a9ed7eded86e10242d88a657a321df0c6cfd1b081a8e851",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json":
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_verification.json":
        "6af01780481224f8c9fd690c46886321be4f5b294c33e3f6515cf20dc7cb0513",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_manifest.sha256":
        "6c6b710b3d04c24f962ecb00399ea7d2bccf64650b5e78af36a59c2a754f0697",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json":
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verification.json":
        "26eed04f887f8b6a4ec8fcc88f1112f7382e079d9c53a33dd37a53f7417a29f9",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256":
        "82124ccbc3fa88fadb1f2a3239634dca332ccc959f7338c44cd27908e4957e5a",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json":
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_verification.json":
        "a40f79823dcf07155eec1ecd12cc367dae6b7bdc7a6e8e7cf8680d29d4dade10",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_manifest.sha256":
        "dc726fde4395c23bd528ef4fc674289bb224c42e023520487676c3deafca12ac",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz":
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz":
        "bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json":
        "a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256":
        "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz":
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json":
        "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23",
    "cm2_round290_source_g_isolated_atom_inner_support_closure_manifest.sha256":
        "e4e4b0614d810bb0516902e173ea7c816f1cecdea162d202ff058200b3d83189",
    "cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz":
        "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025",
    "cm2_round290_source_g_isolated_atom_inner_support_closure_verification.json":
        "94a8b1a3a0274bfb14d6f9e9b00d896673792548220e309b0211f2f2e3367b51",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256":
        "8dd3907a363ae0c4fe7d524061a02b4c70944ce870ded941d5d617911ea1124e",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz":
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_verification.json":
        "a5bd12b10103b4785574bd4633e608c7fd5107369ba8f2343ebffe7e08eba1c7",
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256":
        "5789b23e74b6e0db9a1b4e311fb22ebe5e3612e4972d2fc3547957230fda214c",
    "cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz":
        "88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93",
    "cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz":
        "5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e",
    "cm2_round301_source_g_legal_component_dsu_application_verification.json":
        "31db1fd416c12a384bcfc7dd08d0a6ecf1cba5a9390b47227847f5c7852f376a",
}


class BridgeError(RuntimeError):
    """Fail-closed bridge producer error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise BridgeError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("ascii")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


THEOREM_SHA256 = digest(THEOREM)


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def guard_input(path: Path, maximum: int = 4_000_000_000) -> None:
    need(path.parent.resolve() == HERE.resolve(), "input parent:" + path.name)
    need(path.exists() and not path.is_symlink(), "input exists:" + path.name)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "input regular/link/size:" + path.name,
    )


def input_path(name: str) -> Path:
    need(name in INPUT_PINS, "declared input:" + name)
    return HERE / name


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_number(token: str) -> Any:
    raise BridgeError("noninteger JSON number:" + token)


def json_decoder() -> json.JSONDecoder:
    return json.JSONDecoder(
        object_pairs_hook=strict_object,
        parse_float=reject_number,
        parse_constant=reject_number,
    )


def verify_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "row SHA closure:" + label,
    )


def close_row(
    id_field: str,
    prefix: str,
    domain: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {id_field: prefix + digest([domain, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


def open_text(path: Path) -> TextIO:
    guard_input(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("rt", encoding="utf-8", newline="")


def iter_array(
    path: Path,
    marker: str,
    *,
    first_value_prefix: str | None = None,
) -> Iterator[Any]:
    with open_text(path) as stream:
        buffer = ""
        while True:
            while marker not in buffer:
                part = stream.read(1 << 20)
                need(
                    bool(part),
                    "array marker:" + path.name + ":" + marker,
                )
                buffer += part
                if len(buffer) > len(marker) + (1 << 21):
                    buffer = buffer[-(len(marker) + (1 << 21)):]
            buffer = buffer.split(marker, 1)[1]
            while not buffer.lstrip():
                part = stream.read(1 << 20)
                need(bool(part), "array first value:" + path.name)
                buffer += part
            if (
                first_value_prefix is None
                or buffer.lstrip().startswith(first_value_prefix)
            ):
                break
        decoder = json_decoder()
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                part = stream.read(1 << 20)
                need(bool(part), "array EOF:" + path.name)
                buffer = part
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            while True:
                try:
                    value, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    part = stream.read(1 << 20)
                    need(bool(part), "truncated array value:" + path.name)
                    buffer += part
            yield value
            buffer = buffer[end:]


def iter_named_rows(path: Path, ledger_name: str) -> Iterator[dict[str, Any]]:
    token = json.dumps(ledger_name, separators=(",", ":")) + ":{"
    with open_text(path) as stream:
        buffer = ""
        while token not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "ledger token:" + ledger_name)
            buffer += part
            if len(buffer) > len(token) + (1 << 21):
                buffer = buffer[-(len(token) + (1 << 21)):]
        buffer = buffer.split(token, 1)[1]
        marker = '"rows":['
        while marker not in buffer:
            part = stream.read(1 << 20)
            need(bool(part), "ledger rows marker:" + ledger_name)
            buffer += part
        buffer = buffer.split(marker, 1)[1]
        decoder = json_decoder()
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                part = stream.read(1 << 20)
                need(bool(part), "ledger rows EOF:" + ledger_name)
                buffer = part
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            while True:
                try:
                    row, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    part = stream.read(1 << 20)
                    need(bool(part), "ledger row truncation:" + ledger_name)
                    buffer += part
            need(type(row) is dict, "named ledger row object")
            yield row
            buffer = buffer[end:]


def canonical_pair(value: Any, label: str) -> tuple[str, str]:
    need(
        type(value) is list
        and len(value) == 2
        and all(type(item) is str for item in value)
        and value[0] < value[1],
        "canonical pair:" + label,
    )
    return value[0], value[1]


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def box_values(box: Any) -> list[str]:
    return [
        qstr(box.t0), qstr(box.t1),
        qstr(box.p0), qstr(box.p1),
        qstr(box.s0), qstr(box.s1),
    ]


def exact_volume(values: list[str]) -> Q:
    need(type(values) is list and len(values) == 6, "six box bounds")
    bounds = [Q(value) for value in values]
    return (
        (bounds[1] - bounds[0])
        * (bounds[3] - bounds[2])
        * (bounds[5] - bounds[4])
    )


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for chunk in chunks(value):
            self.state.update(chunk)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


class RowSpool:
    def __init__(self, path: Path, id_field: str) -> None:
        self.path = path
        self.id_field = id_field
        self.handle: BinaryIO = path.open("wb")
        self.rows = ListHasher()
        self.ids = ListHasher()
        self.hashes = ListHasher()
        self.seen: set[str] = set()

    def add(self, row: dict[str, Any]) -> None:
        row_id = row[self.id_field]
        need(row_id not in self.seen, "duplicate output row ID")
        self.seen.add(row_id)
        self.handle.write(canonical(row) + b"\n")
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])

    def close(self) -> dict[str, Any]:
        self.handle.flush()
        self.handle.close()
        return {
            "row_count": self.rows.count,
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
            "rows_sha256": self.rows.finish(),
        }


MANIFEST_MEMBERS = {
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256": [
        "cm2_round179_source_g_residual_tube_arrangement.py",
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "cm2_round179_source_g_residual_tube_arrangement_verification.json",
    ],
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256": [
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json",
    ],
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_manifest.sha256": [
        "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json",
        "cm2_round269_source_g_closed_collar_direct_signature_materialization_verification.json",
    ],
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_manifest.sha256": [
        "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json",
        "cm2_round270_source_g_outgoing_g_factor_signature_materialization_verification.json",
    ],
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_manifest.sha256": [
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json",
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verification.json",
    ],
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256": [
        "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json",
        "cm2_round272_source_g_boundary_dual_factor_wall_closure_verification.json",
    ],
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_manifest.sha256": [
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz",
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json",
    ],
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256": [
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz",
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json",
    ],
    "cm2_round290_source_g_isolated_atom_inner_support_closure_manifest.sha256": [
        "cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz",
        "cm2_round290_source_g_isolated_atom_inner_support_closure_verification.json",
    ],
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256": [
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json",
    ],
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256": [
        "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_ledger.json.gz",
        "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_verification.json",
    ],
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256": [
        "cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz",
        "cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz",
        "cm2_round301_source_g_legal_component_dsu_application_verification.json",
    ],
}


def parse_manifest(name: str) -> dict[str, str]:
    path = input_path(name)
    guard_input(path, 500_000)
    output: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        member_hash, member_name = match.groups()
        need(
            Path(member_name).name == member_name
            and member_name not in output,
            "manifest member confinement/uniqueness:" + name,
        )
        output[member_name] = member_hash
    need(bool(output), "nonempty manifest:" + name)
    return output


def validate_inputs() -> None:
    for name, expected in sorted(INPUT_PINS.items()):
        need(PIN_RE.fullmatch(expected) is not None, "pin syntax:" + name)
        path = input_path(name)
        guard_input(path)
        need(file_sha256(path) == expected, "file pin:" + name)
    for manifest_name, members in MANIFEST_MEMBERS.items():
        manifest = parse_manifest(manifest_name)
        for member in members:
            need(
                manifest.get(member) == INPUT_PINS[member],
                "manifest/member pin:" + manifest_name + ":" + member,
            )


R300D = (
    "cm2_round300d_source_g_lower_physical_witness_component_edge_"
    "promotion_ledger.json.gz"
)
R301_MEMBERS = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "member_component_ledger.json.gz"
)
R301_INELIGIBLE = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "ineligible_source_consumption_ledger.json.gz"
)
R294 = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R288 = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_"
    "audit_atom_dispositions.json.gz"
)
R279_ATOMS = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
)
R279_EDGES = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz"
)
R290 = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "inner_support_ledger.json.gz"
)
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_KERNEL = "cm2_round179_source_g_residual_tube_arrangement.py"


def collect_scope() -> tuple[
    list[dict[str, Any]],
    set[str],
]:
    records: dict[str, dict[str, Any]] = {}
    marker = '"canonical_incidence_edge_rows":['
    for row in iter_array(input_path(R300D), marker):
        need(type(row) is dict, "R300D row object")
        row_id = row["Round300D_lower_physical_witness_incidence_edge_row_id"]
        verify_row(row, row_id)
        need(row_id not in records, "duplicate R300D row")
        pair = canonical_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            row_id,
        )
        left = row["left_endpoint"]
        right = row["right_endpoint"]
        need(
            [left["registry_occurrence_id"], right["registry_occurrence_id"]]
            == list(pair)
            and row["formal_component_edge_credit"] == 0
            and row["eligible_for_component_DSU_application"] is False
            and row["included_stratum_gluing_lemma_pinned"] is False,
            "R300D incidence-only contract:" + row_id,
        )
        tranche = (
            left["registry_entry_kind"]
            + "|"
            + right["registry_entry_kind"]
        )
        records[row_id] = {
            "source_id": row_id,
            "source_sha256": row["row_sha256"],
            "pair": pair,
            "tranche": tranche,
            "registry_refs": {
                left["registry_occurrence_id"]: {
                    "row_id": left["Round294_occurrence_registry_row_id"],
                    "row_sha256":
                        left["Round294_occurrence_registry_row_sha256"],
                },
                right["registry_occurrence_id"]: {
                    "row_id": right["Round294_occurrence_registry_row_id"],
                    "row_sha256":
                        right["Round294_occurrence_registry_row_sha256"],
                },
            },
        }
    need(len(records) == EXPECTED_R300D_COUNT, "R300D census")

    residual_refs: dict[str, dict[str, Any]] = {}
    all_r300d_seen: set[str] = set()
    disposition_histogram: Counter[str] = Counter()
    for row in iter_array(input_path(R301_INELIGIBLE), '"rows":['):
        need(type(row) is dict, "R301 ineligible row object")
        if row.get("source_relation") != R301_R300D_RELATION:
            continue
        source_id = row["source_row_id"]
        verify_row(row, source_id)
        need(
            source_id in records
            and source_id not in all_r300d_seen
            and row["source_row_sha256"]
            == records[source_id]["source_sha256"]
            and canonical_pair(
                row["canonical_occurrence_endpoint_pair"], source_id
            ) == records[source_id]["pair"]
            and row["source_row_fed_to_DSU"] is False
            and row["eligible_for_component_DSU_application"] is False
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R301/R300D ineligible closure:" + source_id,
        )
        need(
            row["formal_component_edge_application_credit"] == 0
            and row["formal_component_union_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0,
            "R301/R300D zero-credit closure:" + source_id,
        )
        all_r300d_seen.add(source_id)
        disposition = row["disposition"]
        disposition_histogram[disposition] += 1
        stronger_gates = row["stronger_gate_names"]
        legal_edges = row["legal_stronger_edge_references"]
        exact_gate_refs = row["exact_gate_provenance_references"]
        if disposition == R301_R300D_RESIDUAL_DISPOSITION:
            need(
                stronger_gates == []
                and legal_edges == []
                and exact_gate_refs == [],
                "R301 residual incidence-only contract:" + source_id,
            )
            residual_refs[source_id] = {
                "row_id":
                    row["Round301_ineligible_source_consumption_row_id"],
                "row_sha256": row["row_sha256"],
            }
        elif disposition.endswith(
            "PAIR_RECLOSED_BY_STRONGER_LEGAL_EDGE"
        ):
            need(
                stronger_gates != []
                and legal_edges != []
                and exact_gate_refs != [],
                "R301 stronger-edge reclosure contract:" + source_id,
            )
        elif disposition.endswith("AUDITED_FAIL_CLOSED_NO_EDGE"):
            need(
                stronger_gates != []
                and legal_edges == []
                and exact_gate_refs != [],
                "R301 audited fail-closed contract:" + source_id,
            )
        else:
            raise BridgeError(
                "unexpected R301/R300D disposition:"
                + str(disposition)
            )
    need(
        all_r300d_seen == set(records),
        "complete R301/R300D ineligible source coverage",
    )
    need(
        dict(disposition_histogram)
        == EXPECTED_R301_R300D_DISPOSITION_HISTOGRAM,
        "R301/R300D disposition histogram",
    )
    need(
        len(residual_refs) == EXPECTED_RESIDUAL_R300D_COUNT,
        f"residual R301-ineligible R300D census:{len(residual_refs)}",
    )

    residual_records = [
        records[source_id] for source_id in sorted(residual_refs)
    ]
    residual_endpoints = {
        endpoint
        for record in residual_records
        for endpoint in record["pair"]
    }

    members: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_path(R301_MEMBERS), '"rows":['):
        need(type(row) is dict, "R301 member row object")
        endpoint = row.get("registry_or_frontier_member_id")
        if endpoint not in residual_endpoints:
            continue
        verify_row(row, str(endpoint))
        need(
            endpoint not in members
            and row["member_kind"] in {
                "EXPANDED_OCCURRENCE", R288_KIND, PRESERVED_KIND
            }
            and row["member_identity_preserved"] is True,
            "R301 selected member:" + str(endpoint),
        )
        members[endpoint] = {
            "row_id": row["Round301_member_to_component_row_id"],
            "row_sha256": row["row_sha256"],
            "component_id": row["final_Round301_component_id"],
        }
    need(
        set(members) == residual_endpoints,
        "R301 residual endpoint member coverage",
    )

    cross: list[dict[str, Any]] = []
    for record in residual_records:
        left, right = record["pair"]
        if members[left]["component_id"] == members[right]["component_id"]:
            continue
        record["member_refs"] = {
            left: members[left],
            right: members[right],
        }
        cross.append(record)
    cross.sort(key=lambda record: record["source_id"])
    need(
        len(cross) == EXPECTED_CROSS_R301_COUNT,
        f"cross-R301 census:{len(cross)}",
    )

    selected_pairs = [
        record for record in cross
        if record["tranche"] == R288_KIND + "|" + R288_KIND
    ]
    need(
        len(selected_pairs) == EXPECTED_R288_PAIR_COUNT,
        "R288/R288 cross pair census",
    )
    for record in selected_pairs:
        record["r301_ineligible_ref"] = residual_refs[
            record["source_id"]
        ]
    endpoints = {
        endpoint
        for record in selected_pairs
        for endpoint in record["pair"]
    }
    need(
        len(endpoints) == EXPECTED_SELECTED_ENDPOINT_COUNT,
        "R303A distinct endpoint census",
    )
    return selected_pairs, endpoints


def scope_by_endpoint(
    pairs: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for record in pairs:
        for endpoint in record["pair"]:
            need(endpoint not in output, "endpoint reused in selected scope")
            output[endpoint] = {
                "source_Round300D_row_id": record["source_id"],
                "source_Round300D_row_sha256": record["source_sha256"],
                "source_Round301_ineligible_row_id":
                    record["r301_ineligible_ref"]["row_id"],
                "source_Round301_ineligible_row_sha256":
                    record["r301_ineligible_ref"]["row_sha256"],
                "opposite_endpoint": (
                    record["pair"][1]
                    if endpoint == record["pair"][0]
                    else record["pair"][0]
                ),
                "this_Round301_member_row":
                    record["member_refs"][endpoint],
            }
    need(len(output) == EXPECTED_SELECTED_ENDPOINT_COUNT, "scope endpoint map")
    return output


def collect_registry(
    pairs: list[dict[str, Any]],
    endpoints: set[str],
) -> dict[str, dict[str, Any]]:
    expected = {
        endpoint: record["registry_refs"][endpoint]
        for record in pairs
        for endpoint in record["pair"]
    }
    selected: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_path(R294), '"rows":['):
        need(type(row) is dict, "R294 row object")
        endpoint = row.get("registry_occurrence_id")
        if endpoint not in endpoints:
            continue
        verify_row(row, str(endpoint))
        reference = expected[endpoint]
        need(
            endpoint not in selected
            and row["Round294_occurrence_registry_row_id"]
            == reference["row_id"]
            and row["row_sha256"] == reference["row_sha256"]
            and row["registry_entry_kind"] == R288_KIND
            and row["registry_identity_status"]
            == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
            and row["registry_promotion_status"]
            == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
            and row["formal_new_expanded_occurrence_credit"] == 1
            and row["outer_envelope_used_as_inner_support"] is False
            and exact_volume(
                row["positive_volume_rational_inner_support_box"]
            ) == Q(row["exact_inner_support_volume"]) > 0,
            "R294 issued occurrence anchor:" + str(endpoint),
        )
        selected[endpoint] = row
    need(set(selected) == endpoints, "R294 selected endpoint coverage")
    need(
        Counter(
            row["support_representation_kind"] for row in selected.values()
        ) == EXPECTED_SUPPORT_KIND_HISTOGRAM,
        "R294 selected support-kind census",
    )
    return selected


def collect_dispositions(
    registry: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    endpoint_by_row = {
        row["source_row_id"]: endpoint
        for endpoint, row in registry.items()
    }
    selected: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_path(R288), '"rows":['):
        need(type(row) is dict, "R288 row object")
        row_id = row.get("Round288_atom_disposition_row_id")
        endpoint = endpoint_by_row.get(row_id)
        if endpoint is None:
            continue
        verify_row(row, str(row_id))
        registry_row = registry[endpoint]
        need(
            endpoint not in selected
            and row["row_sha256"] == registry_row["source_row_sha256"]
            and row["reserved_candidate_occurrence_id__not_issued"]
            == endpoint
            and row["existing_local_occurrence_row_id"] is None
            and row["canonical_atom_id"] == registry_row["canonical_atom_id"]
            and row["Round182_leaf_row_id"]
            == registry_row["Round182_leaf_row_id"]
            and row["complete_10_field_return_signature_sha256"]
            == registry_row["complete_10_field_return_signature_sha256"]
            and row["source_chart"]
            == registry_row["physical_support_chart"]
            and row["source_signature_row_ids"]
            == registry_row["source_signature_row_ids"]
            and row["source_proof_classes"]
            == registry_row["source_proof_classes"]
            and row["formal_component_credit"] == 0
            and row["true_chart_retained_child_owner_verified"] is True,
            "R294/R288 exact binding:" + endpoint,
        )
        if registry_row["support_representation_kind"].startswith(
            "ROUND279_"
        ):
            selected_inner = row["selected_Round279_strict_inner_corridor"]
            need(
                type(selected_inner) is dict
                and selected_inner[
                    "exact_positive_volume_rational_inner_support_box"
                ]
                == registry_row["positive_volume_rational_inner_support_box"]
                and selected_inner["exact_inner_support_volume"]
                == registry_row["exact_inner_support_volume"]
                and selected_inner["formal_face_edge_witness_row_id"]
                == registry_row["support_source_row_id"],
                "Round279 anchor binding:" + endpoint,
            )
        else:
            need(
                registry_row["support_representation_kind"]
                == "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT"
                and row["selected_Round279_strict_inner_corridor"] is None,
                "Round290 anchor partition:" + endpoint,
            )
        selected[endpoint] = row
    need(set(selected) == set(registry), "R288 selected coverage")
    return selected


def collect_atoms(
    dispositions: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    endpoint_by_atom = {
        row["canonical_atom_id"]: endpoint
        for endpoint, row in dispositions.items()
    }
    need(
        len(endpoint_by_atom) == len(dispositions),
        "canonical atom uniqueness in scope",
    )
    selected: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_path(R279_ATOMS), '"rows":['):
        need(type(row) is dict, "R279 atom row object")
        atom_id = row.get("canonical_atom_id")
        endpoint = endpoint_by_atom.get(atom_id)
        if endpoint is None:
            continue
        verify_row(row, str(atom_id))
        disposition = dispositions[endpoint]
        need(
            endpoint not in selected
            and atom_id == (
                "round279-collar-atom:"
                + digest([
                    row["Round182_leaf_row_id"],
                    row["complete_10_field_return_signature_sha256"],
                ])
            )
            and row["Round182_leaf_row_id"]
            == disposition["Round182_leaf_row_id"]
            and row["complete_10_field_return_signature_sha256"]
            == disposition["complete_10_field_return_signature_sha256"]
            and row["source_signature_row_ids"]
            == disposition["source_signature_row_ids"]
            and row["source_rounds"] == disposition["source_rounds"]
            and row["source_chart"] == disposition["source_chart"]
            and row["new_occurrence_region_atom_candidate"] is True
            and row["component_credit"] == 0,
            "R288/R279 atom closure:" + endpoint,
        )
        selected[endpoint] = row
    need(set(selected) == set(dispositions), "R279 selected atom coverage")
    return selected


def collect_support_sources(
    registry: dict[str, dict[str, Any]],
    dispositions: dict[str, dict[str, Any]],
    atoms: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    dynamic_by_edge: dict[str, list[str]] = {}
    for endpoint, row in registry.items():
        if row["support_representation_kind"].startswith("ROUND279_"):
            dynamic_by_edge.setdefault(
                row["support_source_row_id"], []
            ).append(endpoint)
    need(
        sum(map(len, dynamic_by_edge.values()))
        == EXPECTED_SUPPORT_KIND_HISTOGRAM[
            "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT"
        ],
        "Round279 selected edge reference census",
    )
    selected: dict[str, dict[str, Any]] = {}
    for edge in iter_array(input_path(R279_EDGES), '"rows":['):
        need(type(edge) is dict, "R279 edge row object")
        edge_id = edge.get("formal_face_edge_witness_row_id")
        edge_endpoints = dynamic_by_edge.get(edge_id)
        if edge_endpoints is None:
            continue
        verify_row(edge, str(edge_id))
        for endpoint in edge_endpoints:
            registry_row = registry[endpoint]
            atom = atoms[endpoint]
            endpoint_atoms = [
                item for item in edge["endpoint_atoms"]
                if item["canonical_atom_id"] == atom["canonical_atom_id"]
            ]
            corridors = [
                item for item in edge["two_inward_corridors"]
                if item["leaf_row_id"] == atom["Round182_leaf_row_id"]
            ]
            need(
                endpoint not in selected
                and len(endpoint_atoms) == len(corridors) == 1
                and edge["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and edge["source_chart"] == atom["source_chart"]
                and edge["owner_target"] == atom["owner_target"]
                and corridors[0]["exact_corridor_box"]
                == registry_row[
                    "positive_volume_rational_inner_support_box"
                ]
                and exact_volume(corridors[0]["exact_corridor_box"])
                == Q(registry_row["exact_inner_support_volume"]) > 0,
                "R279 edge/corridor anchor closure:" + endpoint,
            )
            selected[endpoint] = {
                "support_source_kind": "ROUND279_DYNAMIC_CORRIDOR",
                "support_source_row_id": edge_id,
                "support_source_row_sha256": edge["row_sha256"],
                "corridor_leaf_row_id": corridors[0]["leaf_row_id"],
                "corridor_geometric_side": corridors[0]["geometric_side"],
                "corridor_dyadic_normal_depth":
                    corridors[0]["dyadic_normal_depth"],
            }

    isolated_by_row = {
        row["support_source_row_id"]: endpoint
        for endpoint, row in registry.items()
        if row["support_representation_kind"].startswith("ROUND290_")
    }
    for support in iter_array(input_path(R290), '"rows":['):
        need(type(support) is dict, "R290 row object")
        row_id = support.get("Round290_inner_support_row_id")
        endpoint = isolated_by_row.get(row_id)
        if endpoint is None:
            continue
        verify_row(support, str(row_id))
        registry_row = registry[endpoint]
        disposition = dispositions[endpoint]
        atom = atoms[endpoint]
        need(
            endpoint not in selected
            and registry_row["support_source_row_sha256"]
            == support["row_sha256"]
            and support["Round288_atom_disposition_row_id"]
            == disposition["Round288_atom_disposition_row_id"]
            and support["canonical_atom_id"] == atom["canonical_atom_id"]
            and support["Round182_leaf_row_id"]
            == atom["Round182_leaf_row_id"]
            and support["complete_10_field_return_signature_sha256"]
            == atom["complete_10_field_return_signature_sha256"]
            and support["exact_positive_volume_rational_inner_support_box"]
            == registry_row["positive_volume_rational_inner_support_box"]
            and support["exact_inner_support_volume"]
            == registry_row["exact_inner_support_volume"]
            and support["dynamic_signature_constant_on_whole_inner_box"]
            is True
            and support[
                "independent_source_signed_region_side_proof"
            ]["active_factor_or_graph_side_strict_on_whole_inner_box"]
            is True,
            "R290 isolated anchor closure:" + endpoint,
        )
        selected[endpoint] = {
            "support_source_kind": "ROUND290_ISOLATED_INNER_SUPPORT",
            "support_source_row_id": row_id,
            "support_source_row_sha256": support["row_sha256"],
            "source_signature_row_id": support["source_signature_row_id"],
            "source_round": support["source_round"],
        }
    need(set(selected) == set(registry), "support-source endpoint coverage")
    return selected


SOURCE_SPECS = {
    269: (
        "cm2_round269_source_g_closed_collar_direct_signature_"
        "materialization_certificate.json",
        "formal_direct_side_signature_ledger",
    ),
    270: (
        "cm2_round270_source_g_outgoing_g_factor_signature_"
        "materialization_certificate.json",
        "formal_direct_side_signature_ledger",
    ),
    271: (
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
        "materialization_certificate.json",
        "formal_side_signature_ledger",
    ),
    272: (
        "cm2_round272_source_g_boundary_dual_factor_wall_"
        "closure_certificate.json",
        "formal_side_signature_ledger",
    ),
}


def round_from_source_id(row_id: str) -> int:
    for round_number in SOURCE_SPECS:
        if row_id.startswith(f"round{round_number}-"):
            return round_number
    raise BridgeError("unrecognized source row ID:" + row_id)


def active_source_sign(round_number: int, row: dict[str, Any]) -> str:
    if round_number in {269, 270}:
        sign = row["region_factor_sign"]
    elif round_number == 271 and row["collar_kind"] == "OUTGOING":
        sign = row["region_product_sign"]
    else:
        need(row["collar_kind"] == "WALL", "source collar wall")
        sign = row["witness_target_factor_sign"]
    need(sign in STRICT_SIGNS, "source active-factor strict sign")
    return sign


def materialize_source_contract(
    round_number: int,
    row: dict[str, Any],
) -> dict[str, Any]:
    row_id = row["signed_region_row_id"]
    signature_sha256 = digest(row["local_return_signature"])
    need(
        signature_sha256
        == row["complete_10_field_return_signature_sha256"]
        and row["component_edge_credit"] == 0,
        "source row signature/nonpromotion:" + row_id,
    )
    sign = active_source_sign(round_number, row)
    base = {
        "source_round": round_number,
        "source_signature_row_id": row_id,
        "source_signature_row_sha256": row["row_sha256"],
        "Round182_leaf_row_id": row["Round182_leaf_row_id"],
        "source_chart": row["local_return_signature"]["source_chart"],
        "complete_10_field_return_signature_sha256": signature_sha256,
        "active_factor_strict_sign": sign,
        "occurrence_row_id": row.get("occurrence_row_id"),
        "retained_child_row_id": row.get("retained_child_row_id"),
        "equation": row.get("equation"),
    }
    if round_number in {269, 270}:
        region_id = row["Round182_leaf_row_id"] + ":" + sign
        need(
            row["candidate_region_id"] == region_id
            and row["direct_whole_leaf_base_certified"] is True
            and row["side_specific_signature_credit"] == 1
            and row["HPLUS_sign"] in STRICT_SIGNS
            and row["HMINUS_sign"] in STRICT_SIGNS,
            "Round269/270 full connected sign side:" + row_id,
        )
        return {
            **base,
            "connected_contract":
                f"ROUND{round_number}_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
            "formal_connected_source_signed_region_id": region_id,
            "formal_connected_source_signed_region_definition":
                "{x in exact pinned Round182 leaf: active_F(x) has "
                + sign
                + "}",
            "connected_side_extension_materialized": True,
            "relative_open_excluded_face": None,
            "W_tail_connected_extension_missing": False,
        }
    if round_number == 271:
        need(row["side_signature_credit"] == 1, "Round271 side credit")
        if row["collar_kind"] == "OUTGOING":
            need(
                row_id.startswith("round271-W-tail-side:")
                and type(row.get("t_child_box")) is list
                and exact_volume(row["t_child_box"]) > 0,
                "Round271 W-tail signed child",
            )
            return {
                **base,
                "connected_contract":
                    "MISSING__ROUND271_W_TAIL_SIGNED_CHILD_ONLY",
                "formal_connected_source_signed_region_id": None,
                "formal_connected_source_signed_region_definition": None,
                "connected_side_extension_materialized": False,
                "relative_open_excluded_face":
                    row.get("excluded_transition_face"),
                "W_tail_connected_extension_missing": True,
                "signed_t_child_box": row["t_child_box"],
            }
        need(
            row["collar_kind"] == "WALL"
            and row["region_product_sign"] in STRICT_SIGNS
            and row["witness_source_factor_sign"] in STRICT_SIGNS
            and row["witness_target_factor_sign"] in STRICT_SIGNS
            and row["connected_side_extension"]
            == "ROUND182_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_GRAPH_SIDE",
            "Round271 wall connected side extension",
        )
        return {
            **base,
            "connected_contract":
                "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_"
                "WHOLE_F_SIGN_SIDE",
            "formal_connected_source_signed_region_id":
                row["Round182_leaf_row_id"] + ":TARGET_F:" + sign,
            "formal_connected_source_signed_region_definition":
                "{x in exact pinned Round182 wall leaf: active target_F(x) "
                "has " + sign + "}",
            "connected_side_extension_materialized": True,
            "relative_open_excluded_face": None,
            "W_tail_connected_extension_missing": False,
        }
    need(
        round_number == 272
        and row["side_signature_credit"] == 1
        and row["connected_side_extension"] == (
            "ONE_SIDED_SOURCE_FACTOR_STRICT_ON_OPEN_INTERIOR__"
            "TARGET_FACTOR_IS_THE_ONLY_ACTIVE_GRAPH"
        )
        and row["exact_source_factor_identity"].startswith(
            "source transverse wall factor = (9/25)*t"
        )
        and row["excluded_zero_face"] == "t=0"
        and row["witness_source_factor_sign"] in STRICT_SIGNS
        and row["witness_target_factor_sign"] in STRICT_SIGNS,
        "Round272 exact relative-open connected side",
    )
    return {
        **base,
        "connected_contract":
            "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
            "WHOLE_F_SIGN_SIDE",
        "formal_connected_source_signed_region_id":
            row["Round182_leaf_row_id"]
            + ":RELATIVE_OPEN_TARGET_F:"
            + sign,
        "formal_connected_source_signed_region_definition":
            "{x in relative-open pinned Round182 wall leaf excluding t=0: "
            "active target_F(x) has " + sign + "}",
        "connected_side_extension_materialized": True,
        "relative_open_excluded_face": "t=0",
        "closed_box_source_factor_strictness_required": False,
        "W_tail_connected_extension_missing": False,
    }


def collect_source_contracts(
    dispositions: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
]:
    wanted: dict[int, set[str]] = {
        round_number: set() for round_number in SOURCE_SPECS
    }
    for disposition in dispositions.values():
        source_ids = disposition["source_signature_row_ids"]
        need(
            set(disposition["source_rounds"])
            == {round_from_source_id(row_id) for row_id in source_ids},
            "R288 source round/ID agreement",
        )
        for row_id in source_ids:
            wanted[round_from_source_id(row_id)].add(row_id)
    selected: dict[str, dict[str, Any]] = {}
    for round_number, (name, ledger_name) in SOURCE_SPECS.items():
        found: set[str] = set()
        for row in iter_named_rows(input_path(name), ledger_name):
            row_id = row.get("signed_region_row_id")
            if row_id not in wanted[round_number]:
                continue
            verify_row(row, str(row_id))
            need(row_id not in selected, "duplicate selected source row")
            selected[row_id] = materialize_source_contract(
                round_number, row
            )
            found.add(row_id)
        need(found == wanted[round_number], f"Round{round_number} coverage")
    by_endpoint: dict[str, list[dict[str, Any]]] = {}
    for endpoint, disposition in dispositions.items():
        rows = [
            selected[row_id]
            for row_id in disposition["source_signature_row_ids"]
        ]
        need(
            len({row["active_factor_strict_sign"] for row in rows}) == 1
            and all(
                row["Round182_leaf_row_id"]
                == disposition["Round182_leaf_row_id"]
                and row["source_chart"] == disposition["source_chart"]
                and row["complete_10_field_return_signature_sha256"]
                == disposition[
                    "complete_10_field_return_signature_sha256"
                ]
                for row in rows
            ),
            "endpoint source alias closure:" + endpoint,
        )
        by_endpoint[endpoint] = rows
    return selected, by_endpoint


R182_LEAF_COLUMNS = [
    "row_id", "occurrence_row_id", "retained_child_row_id",
    "base_refinement_path", "box", "coordinate_volume",
    "base_coordinate_area", "lower_t_face_status", "upper_t_face_status",
    "graph_classification", "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "closed_3d_side_union_volume", "residual_3d_collar_volume",
]
R182_COLLAR_COLUMNS = [
    "row_id", "Round179_occurrence_row_id", "origin_row_id", "parent_id",
    "chart", "owner_target", "kind", "reason_label", "equation",
    "target_obstacle", "strict_t_derivative_sign",
    "Round179_origin_already_fully_replaced",
    "Round179_retained_child_count", "Round179_retained_coordinate_volume",
    "bounded_base_split_axis", "bounded_base_split_depth",
    "closed_leaf_count", "closed_coordinate_volume", "residual_leaf_count",
    "residual_coordinate_volume", "full_base_graph_leaf_count",
    "absent_graph_leaf_count", "clipped_graph_leaf_count",
    "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "fully_clipped_over_Round179_retained_children", "leaf_rows_sha256",
    "whole_original_tube_credit", "global_exact_key_disposition_credit",
    "provenance",
]
R179_ORIGIN_COLUMNS = [
    "origin_row_id", "parent_id", "chart", "owner_target",
    "original_refinement_path", "original_box",
    "original_coordinate_volume", "original_reason_labels", "reason_count",
    "chosen_split_axis", "resolved_child_count",
    "resolved_child_coordinate_volume", "guard_child_count",
    "guard_child_coordinate_volume", "retained_child_count",
    "retained_child_coordinate_volume", "fully_replaced_by_bounded_children",
    "released_exact_key_count", "released_exact_key_ordinals_sha256",
    "provenance",
]
R179_OUTGOING_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "equation",
    "gradient_axis", "gradient_sign", "regularity_certification",
    "lower_t_face_sign", "upper_t_face_sign", "face_classification",
    "zero_set_dimension_account", "existence_over_full_base",
    "two_open_3d_sides_retained", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
R179_WALL_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "reason_label",
    "axis", "integer_wall", "zero_equation",
    "source_factor_classification", "source_gradient_axis",
    "source_gradient_sign", "target_factor_classification",
    "target_gradient_axis", "target_gradient_sign",
    "target_lower_face_sign", "target_upper_face_sign",
    "target_face_classification", "zero_set_dimension_account",
    "crossing_time_dependency_overwrap_discharged", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]


def unpack_selected(
    path: Path,
    table: str,
    columns: list[str],
    id_field: str,
    wanted: set[str],
) -> dict[str, dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    marker = json.dumps(table, separators=(",", ":")) + ":["
    for packed in iter_array(path, marker, first_value_prefix="["):
        need(
            type(packed) is list and len(packed) == len(columns),
            "packed row arity:" + table,
        )
        row = dict(zip(columns, packed, strict=True))
        row_id = row[id_field]
        if row_id not in wanted:
            continue
        need(row_id not in selected, "duplicate packed row:" + str(row_id))
        selected[row_id] = row
    need(set(selected) == wanted, "packed table coverage:" + table)
    return selected


def collect_geometry(
    atoms: dict[str, dict[str, Any]],
    contracts: dict[str, list[dict[str, Any]]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    leaf_ids = {row["Round182_leaf_row_id"] for row in atoms.values()}
    leaves = unpack_selected(
        input_path(R182),
        "collar_leaf_rows",
        R182_LEAF_COLUMNS,
        "row_id",
        leaf_ids,
    )
    occurrence_ids = {
        leaf["occurrence_row_id"] for leaf in leaves.values()
    }
    collars = unpack_selected(
        input_path(R182),
        "collar_occurrence_rows",
        R182_COLLAR_COLUMNS,
        "Round179_occurrence_row_id",
        occurrence_ids,
    )
    origin_ids = {
        collar["origin_row_id"] for collar in collars.values()
    }
    origins = unpack_selected(
        input_path(R179),
        "origin_tube_rows",
        R179_ORIGIN_COLUMNS,
        "origin_row_id",
        origin_ids,
    )
    outgoing_ids = {
        occurrence_id
        for occurrence_id, collar in collars.items()
        if collar["kind"] == "OUTGOING"
    }
    wall_ids = occurrence_ids - outgoing_ids
    outgoing = unpack_selected(
        input_path(R179),
        "outgoing_normal_form_rows",
        R179_OUTGOING_COLUMNS,
        "row_id",
        outgoing_ids,
    ) if outgoing_ids else {}
    walls = unpack_selected(
        input_path(R179),
        "wall_normal_form_rows",
        R179_WALL_COLUMNS,
        "row_id",
        wall_ids,
    ) if wall_ids else {}
    active_meta = {**outgoing, **walls}
    need(set(active_meta) == occurrence_ids, "active geometry coverage")

    for endpoint, atom in atoms.items():
        leaf = leaves[atom["Round182_leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        origin = origins[collar["origin_row_id"]]
        need(
            atom["Round182_occurrence_row_id"]
            == leaf["occurrence_row_id"]
            and atom["origin_row_id"] == collar["origin_row_id"]
            and atom["source_chart"] == collar["chart"] == origin["chart"]
            and atom["owner_target"]
            == collar["owner_target"]
            == origin["owner_target"]
            and exact_volume(leaf["box"]) > 0,
            "atom/R182/R179 geometry lineage:" + endpoint,
        )
        for contract in contracts[endpoint]:
            need(
                contract["Round182_leaf_row_id"] == leaf["row_id"]
                and contract["source_chart"] == collar["chart"]
                and (
                    contract["occurrence_row_id"] is None
                    or contract["occurrence_row_id"]
                    == leaf["occurrence_row_id"]
                )
                and (
                    contract["retained_child_row_id"] is None
                    or contract["retained_child_row_id"]
                    == leaf["retained_child_row_id"]
                )
                and (
                    contract["equation"] is None
                    or contract["equation"] == collar["equation"]
                ),
                "source contract/active geometry alignment:" + endpoint,
            )
    return leaves, collars, origins, active_meta


def import_kernel() -> Any:
    sys.path.insert(0, str(HERE))
    name = R179_KERNEL.removesuffix(".py")
    kernel = importlib.import_module(name)
    need(
        Path(kernel.__file__).resolve() == input_path(R179_KERNEL).resolve()
        and kernel.FLINT_VERSION == "0.9.0"
        and kernel.PRECISION_BITS == 256,
        "pinned Round179 kernel/runtime",
    )
    kernel.ctx.prec = kernel.PRECISION_BITS
    return kernel


def active_scalar(
    kernel: Any,
    origin: dict[str, Any],
    collar: dict[str, Any],
    metadata: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = kernel.interval_geometry(
        origin["chart"], origin["owner_target"], box
    )
    if collar["kind"] == "OUTGOING":
        return geometry["outgoing_equality"]
    need(collar["kind"] == "WALL", "known collar kind")
    target_name = "hit_x" if metadata["axis"] == "X" else "hit_y"
    return kernel.subtract_wall(
        geometry[target_name], metadata["integer_wall"]
    )


def contains(outer: Any, inner: Any) -> bool:
    return (
        outer.t0 <= inner.t0 <= inner.t1 <= outer.t1
        and outer.p0 <= inner.p0 <= inner.p1 <= outer.p1
        and outer.s0 <= inner.s0 <= inner.s1 <= outer.s1
    )


def volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def strict_anchor_subbox(
    kernel: Any,
    origin: dict[str, Any],
    collar: dict[str, Any],
    metadata: dict[str, Any],
    inner_support: Any,
    expected_sign: str,
) -> tuple[Any, int, int]:
    queue = deque([(inner_support, 0)])
    visited = 0
    while queue:
        candidate, depth = queue.popleft()
        visited += 1
        if visited > MAX_ANCHOR_SEARCH_NODES:
            break
        observed_sign = kernel.sign(
            active_scalar(
                kernel, origin, collar, metadata, candidate
            )[0]
        )
        if observed_sign == expected_sign:
            need(volume(candidate) > 0, "positive strict anchor subbox")
            return candidate, depth, visited
        need(
            observed_sign in {expected_sign, "OVERWRAP"},
            "inner anchor contradicts source-side sign",
        )
        if depth == MAX_ANCHOR_SPLIT_DEPTH:
            continue
        widths = (
            candidate.t1 - candidate.t0,
            candidate.p1 - candidate.p0,
            candidate.s1 - candidate.s0,
        )
        axis = max(range(3), key=lambda index: (widths[index], -index))
        for child in kernel.r174.bisect(candidate, axis):
            queue.append((child, depth + 1))
    raise BridgeError("strict anchor subbox search cap")


def source_reference_rows(
    contracts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "source_round": contract["source_round"],
            "source_signature_row_id":
                contract["source_signature_row_id"],
            "source_signature_row_sha256":
                contract["source_signature_row_sha256"],
            "connected_contract": contract["connected_contract"],
            "active_factor_strict_sign":
                contract["active_factor_strict_sign"],
            "formal_connected_source_signed_region_id":
                contract["formal_connected_source_signed_region_id"],
            "connected_side_extension_materialized":
                contract["connected_side_extension_materialized"],
            "relative_open_excluded_face":
                contract["relative_open_excluded_face"],
        }
        for contract in contracts
    ]


def common_payload(
    *,
    endpoint: str,
    scope: dict[str, Any],
    registry: dict[str, Any],
    disposition: dict[str, Any],
    atom: dict[str, Any],
    support_source: dict[str, Any],
    leaf: dict[str, Any],
    collar: dict[str, Any],
    origin: dict[str, Any],
    metadata: dict[str, Any],
    contracts: list[dict[str, Any]],
    inner_box: Any,
    anchor_subbox: Any,
    search_depth: int,
    search_nodes: int,
    active_sign: str,
) -> dict[str, Any]:
    source_rows = source_reference_rows(contracts)
    return {
        "A0_exact_provenance_pins_and_row_closures": True,
        "A1_Round294_issued_occurrence_has_nonempty_inner_anchor": True,
        "A2_strict_anchor_subbox_inside_issued_inner_support": True,
        "A3_occurrence_atom_source_side_provenance_exactly_closed": True,
        "Round179_active_geometry_reference": {
            "Round179_origin_row_id": origin["origin_row_id"],
            "Round179_active_normal_form_row_id": metadata["row_id"],
            "active_collar_kind": collar["kind"],
            "active_factor_equation": collar["equation"],
            "source_chart": collar["chart"],
            "owner_target": collar["owner_target"],
            "interval_kernel_filename": R179_KERNEL,
            "interval_kernel_sha256": INPUT_PINS[R179_KERNEL],
            "python_flint_version": "0.9.0",
            "interval_precision_bits": 256,
        },
        "Round182_leaf_reference": {
            "Round182_leaf_row_id": leaf["row_id"],
            "Round182_occurrence_row_id": leaf["occurrence_row_id"],
            "retained_child_row_id": leaf["retained_child_row_id"],
            "exact_leaf_box": leaf["box"],
            "graph_classification": leaf["graph_classification"],
        },
        "Round279_atom_reference": {
            "canonical_atom_id": atom["canonical_atom_id"],
            "row_sha256": atom["row_sha256"],
            "Round182_leaf_row_id": atom["Round182_leaf_row_id"],
            "complete_10_field_return_signature_sha256":
                atom["complete_10_field_return_signature_sha256"],
            "source_signature_row_ids":
                atom["source_signature_row_ids"],
            "support_classification": atom["support_classification"],
            "frozen_true_support_boxes":
                atom["frozen_true_support_boxes"],
        },
        "Round288_disposition_reference": {
            "Round288_atom_disposition_row_id":
                disposition["Round288_atom_disposition_row_id"],
            "row_sha256": disposition["row_sha256"],
            "occurrence_identity_disposition":
                disposition["occurrence_identity_disposition"],
            "reserved_candidate_occurrence_id__not_issued":
                disposition[
                    "reserved_candidate_occurrence_id__not_issued"
                ],
            "source_proof_classes": disposition["source_proof_classes"],
        },
        "Round294_registry_reference": {
            "Round294_occurrence_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "row_sha256": registry["row_sha256"],
            "registry_identity_status":
                registry["registry_identity_status"],
            "registry_promotion_status":
                registry["registry_promotion_status"],
            "registry_source_identity":
                registry["registry_source_identity"],
        },
        "Round300D_Round301_scope_reference": scope,
        "active_factor_equation": collar["equation"],
        "active_factor_strict_sign": active_sign,
        "canonical_atom_id": atom["canonical_atom_id"],
        "exact_issued_inner_support_box": box_values(inner_box),
        "exact_strict_anchor_subbox": box_values(anchor_subbox),
        "full_occurrence_support_equality_claimed": False,
        "registry_occurrence_id": endpoint,
        "source_side_row_references": source_rows,
        "strict_anchor_search": {
            "algorithm":
                "DETERMINISTIC_BREADTH_FIRST_LONGEST_AXIS_RATIONAL_BISECTION",
            "configured_max_split_depth": MAX_ANCHOR_SPLIT_DEPTH,
            "configured_max_search_nodes": MAX_ANCHOR_SEARCH_NODES,
            "selected_split_depth": search_depth,
            "visited_node_count": search_nodes,
            "strict_active_factor_sign": active_sign,
            "subbox_contained_in_issued_inner_support":
                contains(inner_box, anchor_subbox),
            "subbox_exact_positive_volume": qstr(volume(anchor_subbox)),
        },
        "support_representation_kind":
            registry["support_representation_kind"],
        "support_source_reference": support_source,
        "theorem_id": THEOREM_ID,
        "theorem_sha256": THEOREM_SHA256,
    }


def build_rows(
    *,
    endpoints_to_process: list[str],
    scopes: dict[str, dict[str, Any]],
    registry: dict[str, dict[str, Any]],
    dispositions: dict[str, dict[str, Any]],
    atoms: dict[str, dict[str, Any]],
    support_sources: dict[str, dict[str, Any]],
    contracts: dict[str, list[dict[str, Any]]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active_meta: dict[str, dict[str, Any]],
    kernel: Any,
    bridge_spool: RowSpool,
    unresolved_spool: RowSpool,
) -> dict[str, Any]:
    connected_histogram: Counter[str] = Counter()
    support_histogram: Counter[str] = Counter()
    source_round_histogram: Counter[str] = Counter()
    depth_histogram: Counter[str] = Counter()
    bridge_count = 0
    unresolved_count = 0
    for ordinal, endpoint in enumerate(endpoints_to_process, start=1):
        registry_row = registry[endpoint]
        disposition = dispositions[endpoint]
        atom = atoms[endpoint]
        endpoint_contracts = contracts[endpoint]
        leaf = leaves[atom["Round182_leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        origin = origins[collar["origin_row_id"]]
        metadata = active_meta[leaf["occurrence_row_id"]]
        signs = {
            contract["active_factor_strict_sign"]
            for contract in endpoint_contracts
        }
        need(len(signs) == 1, "unique endpoint active sign")
        active_sign = next(iter(signs))

        leaf_box = kernel.box_from(
            leaf["box"],
            len(leaf["base_refinement_path"]),
            leaf["row_id"],
        )
        inner_box = kernel.box_from(
            registry_row["positive_volume_rational_inner_support_box"],
            0,
            "Round294-inner-anchor:" + endpoint,
        )
        need(
            volume(inner_box)
            == Q(registry_row["exact_inner_support_volume"]) > 0
            and contains(leaf_box, inner_box),
            "issued inner anchor inside exact leaf:" + endpoint,
        )
        if any(
            contract["source_round"] == 272
            for contract in endpoint_contracts
        ):
            need(
                not (inner_box.t0 <= 0 <= inner_box.t1),
                "Round272 anchor excludes relative-open t=0 face",
            )
        anchor_subbox, search_depth, search_nodes = strict_anchor_subbox(
            kernel,
            origin,
            collar,
            metadata,
            inner_box,
            active_sign,
        )
        need(
            contains(inner_box, anchor_subbox)
            and volume(anchor_subbox) > 0,
            "strict B0 inside issued B:" + endpoint,
        )
        common = common_payload(
            endpoint=endpoint,
            scope=scopes[endpoint],
            registry=registry_row,
            disposition=disposition,
            atom=atom,
            support_source=support_sources[endpoint],
            leaf=leaf,
            collar=collar,
            origin=origin,
            metadata=metadata,
            contracts=endpoint_contracts,
            inner_box=inner_box,
            anchor_subbox=anchor_subbox,
            search_depth=search_depth,
            search_nodes=search_nodes,
            active_sign=active_sign,
        )
        support_histogram[registry_row["support_representation_kind"]] += 1
        depth_histogram[str(search_depth)] += 1
        for contract in endpoint_contracts:
            source_round_histogram[str(contract["source_round"])] += 1

        missing = [
            contract for contract in endpoint_contracts
            if not contract["connected_side_extension_materialized"]
        ]
        if missing:
            need(
                all(
                    contract["W_tail_connected_extension_missing"]
                    for contract in missing
                ),
                "only W-tail may be unresolved",
            )
            payload = {
                **common,
                "A4_unique_formal_connected_source_signed_region_materialized":
                    False,
                "disposition": UNRESOLVED_DISPOSITION,
                "eligible_as_R303B_G1_bridge_input": False,
                "formal_occurrence_anchor_connected_side_bridge_credit": 0,
                "missing_obligation":
                    "ROUND271_W_TAIL_ROW_HAS_STRICT_SIGNED_CHILD_BUT_NO_"
                    "FORMAL_CONNECTED_SOURCE_SIDE_EXTENSION",
                "nonedge_or_exclusion_claimed": False,
                **{field: 0 for field in ZERO_FIELDS},
            }
            unresolved_spool.add(close_row(
                UNRESOLVED_ID,
                "round303a-unresolved-anchor-bridge:",
                "ROUND303A_W_TAIL_CONNECTED_SIDE_UNRESOLVED_V1",
                payload,
            ))
            unresolved_count += 1
        else:
            region_ids = {
                contract["formal_connected_source_signed_region_id"]
                for contract in endpoint_contracts
            }
            need(
                len(region_ids) == 1
                and all(
                    contract["connected_side_extension_materialized"]
                    for contract in endpoint_contracts
                ),
                "unique materialized connected source side:" + endpoint,
            )
            contract_name = endpoint_contracts[0]["connected_contract"]
            need(
                all(
                    contract["connected_contract"] == contract_name
                    for contract in endpoint_contracts
                ),
                "source alias connected-contract agreement",
            )
            connected_histogram[contract_name] += 1
            payload = {
                **common,
                "A4_unique_formal_connected_source_signed_region_materialized":
                    True,
                "anchor_bridge_semantics":
                    "STRICT_ISSUED_OCCURRENCE_ANCHOR_SUBBOX_B0_IS_"
                    "CONTAINED_IN_UNIQUELY_BOUND_FORMAL_CONNECTED_"
                    "SOURCE_SIGNED_REGION_A__NO_FULL_SUPPORT_EQUALITY",
                "connected_source_side_witness": {
                    "formal_connected_source_signed_region_id":
                        next(iter(region_ids)),
                    "formal_connected_source_signed_region_definition":
                        endpoint_contracts[0][
                            "formal_connected_source_signed_region_definition"
                        ],
                    "connected_contract": contract_name,
                    "relative_open_excluded_face":
                        endpoint_contracts[0][
                            "relative_open_excluded_face"
                        ],
                    "connected": True,
                    "strict_anchor_subbox_has_same_active_factor_sign":
                        True,
                },
                "eligible_as_R303B_G1_bridge_input": True,
                "formal_occurrence_anchor_connected_side_bridge_credit": 1,
                **{field: 0 for field in ZERO_FIELDS},
            }
            bridge_spool.add(close_row(
                BRIDGE_ID,
                "round303a-occurrence-anchor-source-side-bridge:",
                "ROUND303A_OCCURRENCE_ANCHOR_CONNECTED_SIDE_BRIDGE_V1",
                payload,
            ))
            bridge_count += 1
        if ordinal % 4_000 == 0:
            print(
                f"Round303A endpoint replay {ordinal}/"
                f"{len(endpoints_to_process)}",
                flush=True,
            )
    return {
        "bridge_count": bridge_count,
        "unresolved_count": unresolved_count,
        "connected_contract_histogram":
            dict(sorted(connected_histogram.items())),
        "support_representation_kind_histogram":
            dict(sorted(support_histogram.items())),
        "source_round_reference_histogram":
            dict(sorted(source_round_histogram.items())),
        "strict_anchor_split_depth_histogram":
            dict(sorted(depth_histogram.items())),
    }


def write_gzip_ledger(
    output_path: Path,
    row_spool_path: Path,
    table_name: str,
    commitment: dict[str, Any],
    schema: str,
    status: str,
) -> None:
    prefix = (
        "materialized_bridge"
        if table_name == "materialized_bridge_rows"
        else "unresolved_bridge"
    )
    values: dict[str, Any] = {
        "every_row_closed_by_own_SHA256": True,
        f"{prefix}_row_count": commitment["row_count"],
        f"{prefix}_row_hashes_sha256":
            commitment["row_hashes_sha256"],
        f"{prefix}_row_ids_sha256": commitment["row_ids_sha256"],
        table_name: None,
        f"{prefix}_rows_sha256": commitment["rows_sha256"],
        "schema": schema,
        "status": status,
    }
    with output_path.open("wb") as raw_stream:
        with gzip.GzipFile(
            filename="",
            fileobj=raw_stream,
            mode="wb",
            mtime=0,
            compresslevel=9,
        ) as stream:
            stream.write(b"{")
            first_key = True
            for key in sorted(values):
                if not first_key:
                    stream.write(b",")
                first_key = False
                stream.write(canonical(key) + b":")
                if key != table_name:
                    stream.write(canonical(values[key]))
                    continue
                stream.write(b"[")
                first_row = True
                with row_spool_path.open("rb") as rows:
                    for raw_row in rows:
                        raw_row = raw_row.rstrip(b"\n")
                        if not first_row:
                            stream.write(b",")
                        first_row = False
                        stream.write(raw_row)
                stream.write(b"]")
            stream.write(b"}")


def output_guard(path: Path, expected_name: str) -> None:
    need(
        path.parent.resolve() == HERE.resolve()
        and path.name == expected_name
        and not path.is_symlink(),
        "output confinement:" + expected_name,
    )


def finalize_result(result: dict[str, Any]) -> bytes:
    value = dict(result)
    value["result_sha256"] = ""
    payload = dict(value)
    payload.pop("result_sha256")
    value["result_sha256"] = digest(payload)
    return canonical(value) + b"\n"


def atomic_replace(staged: Path, target: Path) -> None:
    with staged.open("rb") as stream:
        os.fsync(stream.fileno())
    os.replace(staged, target)


def run(
    *,
    producer_sha256: str,
    sample_count: int | None,
    no_write: bool,
) -> dict[str, Any]:
    validate_inputs()
    selected_pairs, endpoints = collect_scope()
    scopes = scope_by_endpoint(selected_pairs)
    registry = collect_registry(selected_pairs, endpoints)
    dispositions = collect_dispositions(registry)
    atoms = collect_atoms(dispositions)
    support_sources = collect_support_sources(
        registry, dispositions, atoms
    )
    _source_rows, contracts = collect_source_contracts(dispositions)
    leaves, collars, origins, active_meta = collect_geometry(
        atoms, contracts
    )
    kernel = import_kernel()

    ordered_endpoints = sorted(endpoints)
    complete = sample_count is None
    if sample_count is not None:
        need(
            0 < sample_count <= len(ordered_endpoints),
            "sample-count range",
        )
        ordered_endpoints = ordered_endpoints[:sample_count]
    with tempfile.TemporaryDirectory(
        dir=HERE,
        prefix=f".{PREFIX}.stage.",
    ) as stage_directory_text:
        stage_directory = Path(stage_directory_text)
        bridge_rows_path = stage_directory / "bridge.rows"
        unresolved_rows_path = stage_directory / "unresolved.rows"
        bridge_spool = RowSpool(bridge_rows_path, BRIDGE_ID)
        unresolved_spool = RowSpool(
            unresolved_rows_path, UNRESOLVED_ID
        )
        statistics = build_rows(
            endpoints_to_process=ordered_endpoints,
            scopes=scopes,
            registry=registry,
            dispositions=dispositions,
            atoms=atoms,
            support_sources=support_sources,
            contracts=contracts,
            leaves=leaves,
            collars=collars,
            origins=origins,
            active_meta=active_meta,
            kernel=kernel,
            bridge_spool=bridge_spool,
            unresolved_spool=unresolved_spool,
        )
        bridge_commitment = bridge_spool.close()
        unresolved_commitment = unresolved_spool.close()

        if complete:
            need(
                statistics["bridge_count"] == EXPECTED_BRIDGE_COUNT
                and statistics["unresolved_count"]
                == EXPECTED_UNRESOLVED_COUNT
                and statistics["connected_contract_histogram"]
                == EXPECTED_CONNECTED_CONTRACT_HISTOGRAM
                and statistics[
                    "support_representation_kind_histogram"
                ] == EXPECTED_SUPPORT_KIND_HISTOGRAM,
                "complete Round303A promotion census",
            )
        bridge_stage = stage_directory / BRIDGE_LEDGER.name
        unresolved_stage = stage_directory / UNRESOLVED_LEDGER.name
        write_gzip_ledger(
            bridge_stage,
            bridge_rows_path,
            "materialized_bridge_rows",
            bridge_commitment,
            BRIDGE_SCHEMA,
            (
                "FORMAL_87824_ROUND294_OCCURRENCE_ANCHORS_BOUND_TO_"
                "CONNECTED_SOURCE_SIGNED_REGIONS__NO_SUPPORT_EQUALITY_"
                "OR_COMPONENT_EDGE_CREDIT"
                if complete
                else "DIAGNOSTIC_SAMPLE__NO_FORMAL_PROMOTION"
            ),
        )
        write_gzip_ledger(
            unresolved_stage,
            unresolved_rows_path,
            "unresolved_bridge_rows",
            unresolved_commitment,
            UNRESOLVED_SCHEMA,
            (
                "EIGHT_ROUND271_W_TAIL_ENDPOINTS_UNRESOLVED__"
                "CONNECTED_SOURCE_SIDE_EXTENSION_MISSING__"
                "NOT_NONEDGES_OR_EXCLUSIONS"
                if complete
                else "DIAGNOSTIC_SAMPLE__NO_FORMAL_PROMOTION"
            ),
        )
        bridge_file_sha256 = file_sha256(bridge_stage)
        unresolved_file_sha256 = file_sha256(unresolved_stage)
        status = (
            "PASS_ROUND303A_87824_OCCURRENCE_ANCHOR_CONNECTED_SIDE_"
            "BRIDGES__8_W_TAIL_ENDPOINTS_UNRESOLVED__"
            "ZERO_COMPONENT_EDGE_AND_DOWNSTREAM_CREDIT"
            if complete
            else "DIAGNOSTIC_ROUND303A_SAMPLE__NO_FORMAL_PROMOTION"
        )
        result = {
            "schema": SCHEMA,
            "status": status,
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "complete_formal_run": complete,
            "input_file_pins": dict(sorted(INPUT_PINS.items())),
            "theorem": THEOREM,
            "theorem_sha256": THEOREM_SHA256,
            "scope_reconstruction": {
                "complete_Round300D_incidence_edge_count":
                    EXPECTED_R300D_COUNT,
                "residual_Round301_ineligible_Round300D_pair_count":
                    EXPECTED_RESIDUAL_R300D_COUNT,
                "cross_Round301_Round300D_pair_count":
                    EXPECTED_CROSS_R301_COUNT,
                "selected_R288_R288_cross_pair_count":
                    EXPECTED_R288_PAIR_COUNT,
                "selected_distinct_Round294_occurrence_endpoint_count":
                    EXPECTED_SELECTED_ENDPOINT_COUNT,
                "sample_endpoint_count":
                    None if complete else len(ordered_endpoints),
                "old_63224_component_result_reused": False,
                "Round301_partition_reopened_exactly": True,
            },
            "bridge_census": {
                **statistics,
                "materialized_bridge_row_count":
                    bridge_commitment["row_count"],
                "unresolved_bridge_row_count":
                    unresolved_commitment["row_count"],
                "full_occurrence_support_equality_claim_count": 0,
                "component_edge_credit_count": 0,
                "W_tail_nonedge_or_exclusion_count": 0,
            },
            "predicate_contract": {
                "all_materialized_rows_A0_through_A4_true": complete,
                "all_unresolved_rows_fail_only_A4_connected_extension":
                    complete,
                "Round272_relative_open_t0_excluded_face_contract_used":
                    True,
                "Round272_closed_box_source_factor_strictness_required":
                    False,
                "inner_support_is_anchor_not_full_support_definition":
                    True,
            },
            "materialized_bridge_ledger": {
                "filename": BRIDGE_LEDGER.name,
                "schema": BRIDGE_SCHEMA,
                **bridge_commitment,
                "file_sha256": bridge_file_sha256,
            },
            "unresolved_bridge_ledger": {
                "filename": UNRESOLVED_LEDGER.name,
                "schema": UNRESOLVED_SCHEMA,
                **unresolved_commitment,
                "file_sha256": unresolved_file_sha256,
            },
            "formal_credit_transition": {
                "formal_occurrence_anchor_connected_side_bridge_credit":
                    bridge_commitment["row_count"] if complete else 0,
                **{field: 0 for field in ZERO_FIELDS},
            },
            "strict_nonclaims": {
                "full_occurrence_support_equality_claimed": False,
                "component_connectivity_edge_promoted": False,
                "occurrence_identity_collapsed": False,
                "official_key_identity_merged": False,
                "Round301_DSU_mutated_or_reused": False,
                "maximality_rebuilt": False,
                "fibre_exhaustion_claimed": False,
                "global_disposition_claimed": False,
                "W_tail_unresolved_rows_are_nonedges_or_exclusions": False,
            },
            "atomicity_contract": {
                "both_ledgers_staged_before_any_replacement": True,
                "result_replaced_last_as_atomic_commit_point": True,
                "partial_formal_promotion_permitted": False,
                "any_row_or_numerical_replay_failure_aborts_before_commit":
                    True,
            },
            "required_next": [
                "Seal this producer with an independent cacheless verifier, "
                "targeted re-signed attacks, dual-seed replay, cold replay, "
                "and a manifest.",
                "Only a later Round303-B edge gate may combine a sealed "
                "Round303-A bridge with an independently included connected "
                "graph patch and two closure attachments.",
                "Keep the eight W-tail endpoints unresolved until a dedicated "
                "connected-side extension is proved.",
            ],
            "result_sha256": "",
        }
        result_bytes = finalize_result(result)
        staged_result = stage_directory / RESULT.name
        with staged_result.open("wb") as stream:
            stream.write(result_bytes)
            stream.flush()
            os.fsync(stream.fileno())

        if not no_write:
            need(complete, "sample run cannot write formal outputs")
            output_guard(BRIDGE_LEDGER, BRIDGE_LEDGER.name)
            output_guard(UNRESOLVED_LEDGER, UNRESOLVED_LEDGER.name)
            output_guard(RESULT, RESULT.name)
            atomic_replace(bridge_stage, BRIDGE_LEDGER)
            atomic_replace(unresolved_stage, UNRESOLVED_LEDGER)
            atomic_replace(staged_result, RESULT)
        printed = json.loads(result_bytes)
        printed["result_file_sha256"] = hashlib.sha256(
            result_bytes
        ).hexdigest()
        return printed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="303101")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--sample-count", type=int)
    arguments = parser.parse_args()
    need(bool(arguments.seed), "nonempty seed bookkeeping")
    need(
        arguments.sample_count is None or arguments.no_write,
        "--sample-count requires --no-write",
    )
    producer_sha256 = file_sha256(Path(__file__).resolve())
    result = run(
        producer_sha256=producer_sha256,
        sample_count=arguments.sample_count,
        no_write=arguments.no_write,
    )
    print("invocation_seed=" + arguments.seed)
    print(result["status"])
    print(json.dumps(result["bridge_census"], sort_keys=True))
    print("producer_sha256=" + producer_sha256)
    print(
        "bridge_ledger_file_sha256="
        + result["materialized_bridge_ledger"]["file_sha256"]
    )
    print(
        "unresolved_ledger_file_sha256="
        + result["unresolved_bridge_ledger"]["file_sha256"]
    )
    print("result_sha256=" + result["result_sha256"])
    print("result_file_sha256=" + result["result_file_sha256"])


if __name__ == "__main__":
    main()
