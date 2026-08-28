#!/usr/bin/env python3
"""Independent cacheless verifier for the Round300-A frontier diagnostic.

This verifier does not import, execute, tokenize, AST-parse, or otherwise
inspect the producer.  The producer is read only as an inert byte string for
one fixed SHA-256 check.  Expected source rows, canonical endpoint-pair rows,
ledger bytes, and result bytes are reconstructed before candidate artifacts
are opened.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
PRODUCER = f"{PREFIX}.py"
CANDIDATE_LEDGER = f"{PREFIX}_ledger.json.gz"
CANDIDATE_RESULT = f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

# Replaced only after the producer source is final.
PRODUCER_PIN = "f61dccfb8a20328c80bcfaa3458a10988dae73985a2ba23daa7491f4306f5e65"

R275_MANIFEST = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "manifest.sha256"
)
R275_CERTIFICATE = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R287_MANIFEST = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "manifest.sha256"
)
R287_LEDGER = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "ledger.json.gz"
)
R287_RESULT = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "result.json"
)
R287_VERIFICATION = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "verification.json"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "representation_binding_ledger.json.gz"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R295A_MANIFEST = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "manifest.sha256"
)
R295A_INCIDENCE = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R295A_RESULT = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "result.json"
)
R295A_VERIFICATION = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verification.json"
)

MANIFEST_PINS = {
    R275_MANIFEST:
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    R287_MANIFEST:
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    R295A_MANIFEST:
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
}
INPUT_PINS = {
    R275_CERTIFICATE:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287_LEDGER:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R287_RESULT:
        "1265475e5d27f99eda35b16f13ba342e0d270ca1bc064df215a018d3ffae89f9",
    R287_VERIFICATION:
        "c0ad4d3e229a1e21cb5b4f4144575df7f5eaf88d7fc8a6960967ab4c1db515a3",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294_BINDINGS:
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R294_RESULT:
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R295A_INCIDENCE:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R295A_RESULT:
        "0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d",
    R295A_VERIFICATION:
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
}
R294_REGISTRY_COMMITMENT = {
    "row_count": 431_208,
    "row_ids_sha256":
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256":
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "rows_sha256":
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "occurrence_ids_sha256":
        "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}
R294_BINDING_COMMITMENT = {
    "row_count": 46_288,
    "row_ids_sha256":
        "1a03d7c6d95d6144d4b271e46eb6b83ab4c577f7eb5b9f94d34de692247e50ff",
    "row_hashes_sha256":
        "538ddd3aaa79da6ff5dd0738523bcc7bb6c6c192051ada1f96131053fd8190b3",
    "rows_sha256":
        "ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7",
}
R295A_INCIDENCE_COMMITMENT = {
    "row_count": 113_452,
    "row_ids_sha256":
        "a0f471c84148d57eba4511efd8b343eb152c9378a24e018b9f0be10e41525805",
    "row_hashes_sha256":
        "7eab57334f6f5170ffaef60316250078cd6774cdabdb7279d3585267345e5258",
    "rows_sha256":
        "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
}

SCHEMA = "cm2.round300a.source-g-r287-graph-zero-lower-frontier-exhaustion.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
SOURCE_ROW_ID = "Round300A_R287_source_pair_expansion_row_id"
FRONTIER_ROW_ID = "Round300A_canonical_occurrence_pair_row_id"
REFINED_KIND = (
    "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
)
R295A_WITNESSED = (
    "PRIOR_R295A_EXPLICIT_LOWER_GRAPH_SHEET_WITNESS__"
    "NO_NEW_COMPONENT_EDGE_CREDIT"
)
UNRESOLVED = (
    "UNRESOLVED_ENDPOINT_SPECIFIC_COMMON_ZERO_TRACE__"
    "OUTER_OVERLAP_AND_CLOSURE_ZERO_SET_INSUFFICIENT__ZERO_CREDIT"
)
PIN_RE = re.compile(r"^[0-9a-f]{64}$")


class VerificationError(RuntimeError):
    """Independent fail-closed verifier error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for part in ENCODER.iterencode(value):
        yield part.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def sha_object(value: Any) -> str:
    state = hashlib.sha256()
    for part in pieces(value):
        state.update(part)
    return state.hexdigest()


def sha_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1 << 20), b""):
            state.update(part)
    return state.hexdigest()


def regular_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    require(path.parent.resolve() == HERE.resolve(), "parent:" + path.name)
    require(path.exists() and not path.is_symlink(), "exists:" + path.name)
    info = path.stat()
    require(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "regular/link/size:" + path.name,
    )
    return path.read_bytes()


def decode_object(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict bytes:" + label,
    )

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "duplicate key:" + label + ":" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise VerificationError("noninteger JSON:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs_hook,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("JSON:" + label) from error
    require(type(value) is dict, "top object:" + label)
    return value


def json_file(name: str) -> dict[str, Any]:
    return decode_object(regular_bytes(HERE / name), name)


def gzip_json_file(name: str) -> dict[str, Any]:
    try:
        raw = gzip.decompress(regular_bytes(HERE / name))
    except Exception as error:
        raise VerificationError("gzip:" + name) from error
    return decode_object(raw, name)


def check_closed_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    require(
        type(claimed) is str and sha_object(payload) == claimed,
        "row closure:" + label,
    )


def make_row(
    prefix: str,
    domain: str,
    id_field: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {id_field: prefix + sha_object([domain, payload]), **payload}
    row["row_sha256"] = sha_object(row)
    return row


class SequenceCommitment:
    def __init__(self) -> None:
        self._state = hashlib.sha256(b"[")
        self.count = 0

    def push(self, value: Any) -> None:
        if self.count:
            self._state.update(b",")
        for part in pieces(value):
            self._state.update(part)
        self.count += 1

    def value(self) -> str:
        state = self._state.copy()
        state.update(b"]")
        return state.hexdigest()


def table_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    require(len(ids) == len(set(ids)), "output IDs:" + id_field)
    return {
        "row_count": len(rows),
        "row_ids_sha256": sha_object(ids),
        "row_hashes_sha256": sha_object(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": sha_object(rows),
    }


def parse_manifest(name: str) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in regular_bytes(HERE / name, 200_000).decode().splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        require(match is not None, "manifest syntax:" + name)
        sha256, filename = match.groups()
        require(
            Path(filename).name == filename and filename not in output,
            "manifest member:" + name,
        )
        output[filename] = sha256
    require(bool(output), "manifest empty:" + name)
    return output


def check_input_boundary() -> None:
    require(
        PIN_RE.fullmatch(PRODUCER_PIN) is not None,
        "producer pin placeholder",
    )
    # Producer is inert bytes only.  No text decoding or code inspection.
    require(sha_file(HERE / PRODUCER) == PRODUCER_PIN, "producer byte pin")
    for name, expected in MANIFEST_PINS.items():
        require(sha_file(HERE / name) == expected, "manifest pin:" + name)
    for name, expected in INPUT_PINS.items():
        require(sha_file(HERE / name) == expected, "input pin:" + name)
    selections = {
        R275_MANIFEST: [R275_CERTIFICATE],
        R287_MANIFEST: [R287_LEDGER, R287_RESULT, R287_VERIFICATION],
        R294_MANIFEST: [
            R294_REGISTRY, R294_BINDINGS, R294_RESULT, R294_VERIFICATION
        ],
        R295A_MANIFEST: [
            R295A_INCIDENCE, R295A_RESULT, R295A_VERIFICATION
        ],
    }
    for manifest_name, members in selections.items():
        manifest = parse_manifest(manifest_name)
        for member in members:
            require(
                manifest.get(member) == INPUT_PINS[member],
                "manifest selection:" + manifest_name + ":" + member,
            )


def stream_array(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        part = stream.read(1 << 20)
        require(bool(part), "rows marker")
        buffer += part
    buffer = buffer.split(marker, 1)[1]

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "stream duplicate key:" + key)
            output[key] = value
        return output

    decoder = json.JSONDecoder(
        object_pairs_hook=pairs_hook,
        parse_float=lambda token: (_ for _ in ()).throw(
            VerificationError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            part = stream.read(1 << 20)
            require(bool(part), "stream EOF")
            buffer = part
            continue
        if buffer.startswith(","):
            buffer = buffer[1:]
            continue
        if buffer.startswith("]"):
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                part = stream.read(1 << 20)
                require(bool(part), "truncated streamed row")
                buffer += part
        require(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]


def scan_rows(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    consume: Callable[[dict[str, Any]], None],
) -> None:
    rows = SequenceCommitment()
    ids = SequenceCommitment()
    hashes = SequenceCommitment()
    occurrence_ids = (
        SequenceCommitment()
        if "occurrence_ids_sha256" in expected
        else None
    )
    with gzip.open(HERE / name, "rt", encoding="utf-8", newline="") as stream:
        for row in stream_array(stream):
            check_closed_row(row, name)
            rows.push(row)
            ids.push(row[id_field])
            hashes.push(row["row_sha256"])
            if occurrence_ids is not None:
                occurrence_ids.push(row["registry_occurrence_id"])
            consume(row)
    actual = {
        "row_count": rows.count,
        "row_ids_sha256": ids.value(),
        "row_hashes_sha256": hashes.value(),
        "rows_sha256": rows.value(),
    }
    if occurrence_ids is not None:
        actual["occurrence_ids_sha256"] = occurrence_ids.value()
    require(actual == expected, "complete stream commitment:" + name)


def embedded_rows(
    document: dict[str, Any],
    rows_name: str,
    count_name: str,
    digest_name: str,
) -> list[dict[str, Any]]:
    rows = document.get(rows_name)
    require(
        type(rows) is list
        and len(rows) == document.get(count_name)
        and sha_object(rows) == document.get(digest_name),
        "embedded table:" + rows_name,
    )
    for row in rows:
        check_closed_row(row, rows_name)
    return rows


def check_self_result(document: dict[str, Any], label: str) -> None:
    claimed = document.get("result_sha256")
    payload = dict(document)
    payload.pop("result_sha256", None)
    require(
        type(claimed) is str and sha_object(payload) == claimed,
        "self result:" + label,
    )


def recover_source_universe() -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
]:
    wrapper = json_file(R275_CERTIFICATE)
    require(
        sha_object(wrapper["result"]) == wrapper["result_sha256"],
        "Round275 wrapper",
    )
    result = wrapper["result"]
    regions: dict[str, dict[str, Any]] = {}
    for table_name, count in (
        ("strict_region_ledger", 5_288),
        ("arrangement_region_ledger", 8_500),
    ):
        table = result[table_name]
        rows = table["rows"]
        require(
            len(rows) == table["row_count"] == count
            and sha_object(rows) == table["rows_sha256"]
            and sha_object(
                [row["reverse_rechart_region_row_id"] for row in rows]
            ) == table["row_ids_sha256"]
            and sha_object([row["row_sha256"] for row in rows])
            == table["row_hashes_sha256"],
            "Round275 table:" + table_name,
        )
        for row in rows:
            check_closed_row(row, table_name)
            row_id = row["reverse_rechart_region_row_id"]
            require(row_id not in regions, "Round275 duplicate region")
            regions[row_id] = row
    require(len(regions) == 13_788, "Round275 region census")

    # Independent grouping: the refinement path and guard identify one parent
    # graph cell; the two side rows must conserve every non-side field.
    graph_cells: dict[tuple[Any, ...], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in result["arrangement_region_ledger"]["rows"]:
        if row["arrangement_classification"] != "REGULAR_GRAPH_CROSSING":
            continue
        key = (
            row["source_guard_row_id"],
            tuple(row["adjacent_cover_refinement_path"]),
            tuple(row["adjacent_rational_region_box"]),
            row["adjacent_chart"],
            row["active_reason"],
        )
        sign = row["active_factor_side_sign"]
        require(sign not in graph_cells[key], "duplicate graph side")
        graph_cells[key][sign] = row
    require(len(graph_cells) == 3_488, "graph cell census")

    document = gzip_json_file(R287_LEDGER)
    require(document["schema"].endswith(".ledger.v1"), "Round287 schema")
    region_rows = embedded_rows(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    embedded_rows(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    embedded_rows(
        document,
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
    )
    embedded_rows(
        document,
        "valid_internal_physical_face_rows",
        "valid_internal_physical_face_row_count",
        "valid_internal_physical_face_rows_sha256",
    )
    actual_pairs = embedded_rows(
        document,
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
    )
    require(
        (
            len(region_rows),
            document["refinement_cell_row_count"],
            document["potential_new_support_union_row_count"],
            document["valid_internal_physical_face_row_count"],
            len(actual_pairs),
        )
        == (13_788, 7_616, 10_020, 648, 3_488),
        "Round287 census",
    )
    dispositions = {
        row["Round275_region_id"]: row for row in region_rows
    }
    require(set(dispositions) == set(regions), "Round287 region coverage")

    expected_pairs: list[dict[str, Any]] = []
    for key in sorted(graph_cells):
        sides = graph_cells[key]
        require(
            set(sides) == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
            "opposite graph sides",
        )
        negative = sides["STRICT_NEGATIVE"]
        positive = sides["STRICT_POSITIVE"]
        left_id, right_id = sorted([
            negative["reverse_rechart_region_row_id"],
            positive["reverse_rechart_region_row_id"],
        ])
        require(
            negative["source_guard_row_id"] == positive["source_guard_row_id"]
            and negative["parent_id"] == positive["parent_id"]
            and negative["owner_target"] == positive["owner_target"]
            and negative["source_chart"] == positive["source_chart"]
            and negative["adjacent_chart"] == positive["adjacent_chart"]
            and negative["adjacent_rational_region_box"]
            == positive["adjacent_rational_region_box"]
            and negative["strict_derivative_signs_t_p_s"]
            == positive["strict_derivative_signs_t_p_s"]
            and negative["complete_10_field_return_signature_sha256"]
            != positive["complete_10_field_return_signature_sha256"],
            "graph side field conservation",
        )
        pair = {
            "Round287_mutually_exclusive_outer_overlap_pair_row_id":
                "round287-mutually-exclusive-pair:"
                + sha_object([left_id, right_id]),
            "left_Round275_region_id": left_id,
            "right_Round275_region_id": right_id,
            "adjacent_chart": negative["adjacent_chart"],
            "source_guard_row_id": negative["source_guard_row_id"],
            "active_reason": negative["active_reason"],
            "active_factor_side_signs": [
                "STRICT_NEGATIVE", "STRICT_POSITIVE"
            ],
            "exact_positive_physical_overlap": False,
            "reason": "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES",
            "occurrence_identity_collapse_credit": 0,
            "component_edge_credit": 0,
        }
        pair["row_sha256"] = sha_object(pair)
        expected_pairs.append(pair)
    expected_pairs.sort(
        key=lambda row: row[
            "Round287_mutually_exclusive_outer_overlap_pair_row_id"
        ]
    )
    actual_pairs.sort(
        key=lambda row: row[
            "Round287_mutually_exclusive_outer_overlap_pair_row_id"
        ]
    )
    require(actual_pairs == expected_pairs, "Round287 exact pair table")

    result287 = json_file(R287_RESULT)
    check_self_result(result287, "Round287")
    require(
        result287["census"][
            "R275_pairwise_outer_positive_overlap_pair_count"
        ] == 3_488
        and result287["census"][
            "R275_pairwise_actual_positive_overlap_pair_count"
        ] == 0,
        "Round287 result contract",
    )
    verification287 = json_file(R287_VERIFICATION)
    require(
        verification287["status"].startswith("PASS_INDEPENDENT_ROUND287"),
        "Round287 independent seal",
    )
    return dispositions, expected_pairs


def recover_endpoint_map(
    region_ids: set[str],
) -> tuple[dict[str, set[str]], dict[str, int]]:
    result = json_file(R294_RESULT)
    check_self_result(result, "Round294")
    require(
        result["registry_ledger"]["file_sha256"] == INPUT_PINS[R294_REGISTRY]
        and result["representation_binding_ledger"]["file_sha256"]
        == INPUT_PINS[R294_BINDINGS],
        "Round294 selected ledgers",
    )
    verification = json_file(R294_VERIFICATION)
    require(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round294 independent seal",
    )

    endpoints: dict[str, set[str]] = defaultdict(set)
    binding_kinds: Counter[str] = Counter()

    def binding(row: dict[str, Any]) -> None:
        kind = row["alias_source_kind"]
        binding_kinds[kind] += 1
        region_id = row.get("Round275_region_id")
        if region_id is None:
            require(
                kind == "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE",
                "binding null region",
            )
        else:
            require(region_id in region_ids, "binding region")
            endpoints[region_id].add(row["target_registry_occurrence_id"])

    scan_rows(
        R294_BINDINGS,
        "Round294_occurrence_representation_binding_row_id",
        R294_BINDING_COMMITMENT,
        binding,
    )
    require(
        binding_kinds == {
            "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE": 36_680,
            "ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476,
            "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 5_532,
            "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL": 1_600,
        },
        "Round294 binding kinds",
    )

    occurrence_ids: set[str] = set()
    registry_kinds: Counter[str] = Counter()

    def registry(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        require(occurrence not in occurrence_ids, "registry occurrence unique")
        occurrence_ids.add(occurrence)
        kind = row["registry_entry_kind"]
        registry_kinds[kind] += 1
        if kind == REFINED_KIND:
            region_id = row["Round275_region_id"]
            require(region_id in region_ids, "refined region")
            endpoints[region_id].add(occurrence)

    scan_rows(
        R294_REGISTRY,
        "Round294_occurrence_registry_row_id",
        R294_REGISTRY_COMMITMENT,
        registry,
    )
    require(
        registry_kinds == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            REFINED_KIND: 9_404,
        },
        "Round294 registry kinds",
    )
    require(
        set(endpoints) == region_ids
        and all(
            endpoint in occurrence_ids
            for values in endpoints.values()
            for endpoint in values
        ),
        "normalized endpoint coverage",
    )
    histogram = Counter(len(values) for values in endpoints.values())
    require(
        histogram == {
            1: 11_208,
            2: 1_680,
            3: 268,
            4: 232,
            5: 220,
            6: 76,
            10: 88,
            11: 16,
        },
        "endpoint multiplicity",
    )
    return endpoints, {
        str(key): value for key, value in sorted(histogram.items())
    }


def recover_lower_witnesses() -> tuple[
    dict[tuple[str, str], list[dict[str, Any]]],
    dict[str, int],
]:
    result = json_file(R295A_RESULT)
    check_self_result(result, "Round295A")
    require(
        result["physical_witness_incidence_binding_ledger"]["file_sha256"]
        == INPUT_PINS[R295A_INCIDENCE],
        "Round295A incidence attachment",
    )
    verification = json_file(R295A_VERIFICATION)
    require(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        ),
        "Round295A independent seal",
    )
    witnesses: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    arities: Counter[int] = Counter()

    def consume(row: dict[str, Any]) -> None:
        count = row["target_Round294_registry_reference_count"]
        targets = row["target_Round294_registry_occurrence_ids"]
        require(
            len(targets) == count and len(targets) == len(set(targets)),
            "Round295A arity",
        )
        arities[count] += 1
        if count != 2:
            return
        pair = tuple(sorted(targets))
        require(pair[0] != pair[1], "Round295A self pair")
        witnesses[pair].append({
            "row_id":
                row["Round295A_R291_physical_incidence_binding_row_id"],
            "row_sha256": row["row_sha256"],
            "canonical_support_kind": row["canonical_support_kind"],
            "local_disposition": row["local_disposition"],
            "witness_kind": row["witness_kind"],
            "binding_classification":
                row["Round295A_binding_classification"],
            "exact_coverage":
                row["exact_witness_covered_by_named_registry_supports"],
            "formal_incidence_credit":
                row["formal_physical_witness_incidence_binding_credit"],
        })

    scan_rows(
        R295A_INCIDENCE,
        "Round295A_R291_physical_incidence_binding_row_id",
        R295A_INCIDENCE_COMMITMENT,
        consume,
    )
    require(
        arities == {1: 1_600, 2: 111_852}
        and len(witnesses) == 111_524,
        "Round295A witness census",
    )
    return witnesses, {
        "two_target_raw_witness_row_count": 111_852,
        "two_target_unique_pair_count": 111_524,
        "two_target_duplicate_witness_row_count": 328,
    }


def canonical_pair_id(pair: tuple[str, str]) -> str:
    return "round300a-canonical-occurrence-pair:" + sha_object([
        "ROUND300A_CANONICAL_UNORDERED_OCCURRENCE_PAIR_V1",
        list(pair),
    ])


def gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=buffer,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        for part in pieces(value):
            stream.write(part)
    return buffer.getvalue()


def reconstruct_expected() -> tuple[dict[str, Any], dict[str, Any]]:
    check_input_boundary()
    dispositions, source_pairs = recover_source_universe()
    endpoints, mapping_histogram = recover_endpoint_map(set(dispositions))
    witnesses, witness_census = recover_lower_witnesses()

    source_rows: list[dict[str, Any]] = []
    provenance: dict[tuple[str, str], list[str]] = defaultdict(list)
    raw_count = 0
    self_count = 0
    endpoint_histogram: Counter[tuple[int, int]] = Counter()

    for source in source_pairs:
        left_region = source["left_Round275_region_id"]
        right_region = source["right_Round275_region_id"]
        left_ids = sorted(endpoints[left_region])
        right_ids = sorted(endpoints[right_region])
        endpoint_histogram[(len(left_ids), len(right_ids))] += 1
        local: list[tuple[str, str]] = []
        for left in left_ids:
            for right in right_ids:
                raw_count += 1
                if left == right:
                    self_count += 1
                    continue
                pair = tuple(sorted((left, right)))
                local.append(pair)
                provenance[pair].append(
                    source[
                        "Round287_mutually_exclusive_outer_overlap_pair_row_id"
                    ]
                )
        require(len(local) == len(set(local)), "local pair injectivity")
        payload = {
            "source_Round287_pair_row_id":
                source[
                    "Round287_mutually_exclusive_outer_overlap_pair_row_id"
                ],
            "source_Round287_pair_row_sha256": source["row_sha256"],
            "left_Round275_region_id": left_region,
            "left_Round287_region_row_sha256":
                dispositions[left_region]["row_sha256"],
            "right_Round275_region_id": right_region,
            "right_Round287_region_row_sha256":
                dispositions[right_region]["row_sha256"],
            "adjacent_chart": source["adjacent_chart"],
            "source_guard_row_id": source["source_guard_row_id"],
            "active_reason": source["active_reason"],
            "active_factor_side_signs":
                source["active_factor_side_signs"],
            "left_Round294_registry_occurrence_ids": left_ids,
            "right_Round294_registry_occurrence_ids": right_ids,
            "left_endpoint_occurrence_count": len(left_ids),
            "right_endpoint_occurrence_count": len(right_ids),
            "raw_occurrence_pair_expansion_count": len(local),
            "canonical_occurrence_pair_row_ids":
                sorted(canonical_pair_id(pair) for pair in local),
            "exact_positive_open_support_intersection": False,
            "mutual_exclusion_reason":
                "SAME_CONTINUOUS_ACTIVE_FACTOR__OPPOSITE_STRICT_OPEN_SIDES__"
                "SET_INTERSECTION_EMPTY",
            "regular_graph_zero_present_in_parent_cell_closure": True,
            "source_outer_overlap_is_endpoint_specific_zero_trace_witness":
                False,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
        }
        source_rows.append(make_row(
            "round300a-source-pair-expansion:",
            "ROUND300A_R287_SOURCE_PAIR_EXPANSION_V1",
            SOURCE_ROW_ID,
            payload,
        ))
    source_rows.sort(key=lambda row: row[SOURCE_ROW_ID])
    require(
        raw_count == 6_292 and self_count == 0 and len(provenance) == 3_232,
        "expanded frontier census",
    )
    prior = set(provenance) & set(witnesses)
    require(len(prior) == 128, "prior witness intersection")

    frontier_rows: list[dict[str, Any]] = []
    statuses: Counter[str] = Counter()
    for pair in sorted(provenance):
        references = sorted(
            witnesses.get(pair, []), key=lambda item: item["row_id"]
        )
        witnessed = bool(references)
        if witnessed:
            require(len(references) == 1, "frontier witness uniqueness")
            witness = references[0]
            require(
                witness["canonical_support_kind"]
                == "NOMINAL_REGULAR_ZERO_SET_IF_PRESENT"
                and witness["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
                and witness["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
                and witness["binding_classification"]
                == "FORMAL_ROUND294_REGISTRY_REBIND__"
                "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
                and witness["exact_coverage"] is True
                and witness["formal_incidence_credit"] == 1,
                "explicit graph sheet witness",
            )
        status = R295A_WITNESSED if witnessed else UNRESOLVED
        statuses[status] += 1
        source_ids = sorted(provenance[pair])
        payload = {
            "canonical_unordered_Round294_registry_occurrence_ids":
                list(pair),
            "left_Round294_registry_occurrence_id": pair[0],
            "right_Round294_registry_occurrence_id": pair[1],
            "self_pair": False,
            "source_Round287_pair_row_ids": source_ids,
            "source_expansion_provenance_count": len(source_ids),
            "duplicate_source_expansion_count": len(source_ids) - 1,
            "exact_positive_open_support_intersection": False,
            "opposite_strict_side_exclusion_proved": True,
            "parent_regular_graph_zero_in_closure_is_not_itself_an_edge":
                True,
            "R295A_explicit_lower_graph_sheet_witness_present": witnessed,
            "R295A_physical_incidence_binding_row_ids":
                [item["row_id"] for item in references],
            "R295A_physical_incidence_binding_row_sha256s":
                [item["row_sha256"] for item in references],
            "endpoint_specific_common_positive_area_zero_trace_proved":
                witnessed,
            "frontier_disposition": status,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_maximality_credit": 0,
        }
        frontier_rows.append(make_row(
            "round300a-canonical-occurrence-pair:",
            "ROUND300A_CANONICAL_OCCURRENCE_PAIR_DISPOSITION_V1",
            FRONTIER_ROW_ID,
            payload,
        ))
    frontier_rows.sort(key=lambda row: row[FRONTIER_ROW_ID])
    require(
        statuses == {R295A_WITNESSED: 128, UNRESOLVED: 3_104}
        and sum(
            row["duplicate_source_expansion_count"] for row in frontier_rows
        ) == 3_060,
        "frontier disposition/duplicate census",
    )

    source_commitment = table_commitment(source_rows, SOURCE_ROW_ID)
    frontier_commitment = table_commitment(frontier_rows, FRONTIER_ROW_ID)
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "EXHAUSTIVE_FAIL_CLOSED_ZERO_CREDIT__3488_R287_SOURCE_PAIRS__"
            "3232_CANONICAL_OCCURRENCE_PAIRS__128_PRIOR_WITNESSED__"
            "3104_ENDPOINT_SPECIFIC_ZERO_TRACE_OBLIGATIONS",
        "source_pair_expansion_row_count": len(source_rows),
        "source_pair_expansion_row_ids_sha256":
            source_commitment["row_ids_sha256"],
        "source_pair_expansion_row_hashes_sha256":
            source_commitment["row_hashes_sha256"],
        "source_pair_expansion_rows_sha256":
            source_commitment["rows_sha256"],
        "source_pair_expansion_rows": source_rows,
        "canonical_occurrence_pair_row_count": len(frontier_rows),
        "canonical_occurrence_pair_row_ids_sha256":
            frontier_commitment["row_ids_sha256"],
        "canonical_occurrence_pair_row_hashes_sha256":
            frontier_commitment["row_hashes_sha256"],
        "canonical_occurrence_pair_rows_sha256":
            frontier_commitment["rows_sha256"],
        "canonical_occurrence_pair_rows": frontier_rows,
    }
    ledger_raw = gzip_bytes(ledger)
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
            "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION",
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "producer_sha256": PRODUCER_PIN,
        "seed_affects_output": False,
        "reconstruction_census": {
            "R275_region_count": 13_788,
            "R287_regular_graph_source_pair_count": 3_488,
            "Round294_region_endpoint_multiplicity_histogram":
                mapping_histogram,
            "source_pair_endpoint_multiplicity_histogram": {
                f"{left}x{right}": count
                for (left, right), count in sorted(endpoint_histogram.items())
            },
            "raw_occurrence_pair_expansion_count": 6_292,
            "canonical_unordered_occurrence_pair_count": 3_232,
            "self_occurrence_pair_count": 0,
            "duplicate_source_expansion_count": 3_060,
            "R295A_two_target_raw_witness_row_count":
                witness_census["two_target_raw_witness_row_count"],
            "R295A_two_target_unique_pair_count":
                witness_census["two_target_unique_pair_count"],
            "R295A_two_target_duplicate_witness_row_count":
                witness_census["two_target_duplicate_witness_row_count"],
            "frontier_pair_with_R295A_explicit_lower_witness_count": 128,
            "frontier_pair_without_endpoint_specific_zero_trace_count":
                3_104,
        },
        "semantic_boundary": {
            "R287_source_relation":
                "SAME_REGULAR_GRAPH_CELL_OPPOSITE_STRICT_OPEN_FACTOR_SIDES",
            "positive_open_support_intersection":
                "PROVED_EMPTY_FOR_EVERY_SOURCE_PAIR",
            "parent_cell_graph_zero":
                "PRESENT_IN_THE_TWO_OPEN_SIDE_CLOSURES",
            "closure_contact_implies_component_edge": False,
            "outer_box_overlap_implies_component_edge": False,
            "source_level_endpoint_cross_product_implies_component_edge":
                False,
            "minimum_missing_evidence_for_each_of_3104":
                "ENDPOINT_SPECIFIC_COMMON_POSITIVE_AREA_ZERO_TRACE_PLUS_"
                "TWO_SIDED_POSITIVE_VOLUME_CORRIDOR_OR_SEALED_GLUE_LEMMA",
            "counterexample_model":
                "f=x; U={x<0}; V={x>0}; closures share x=0 but "
                "U_intersection_V_is_empty_and_U_union_V_is_disconnected",
            "canonical_3232_are_not_all_promoted_candidates": True,
        },
        "prior_witness_partition": {
            "R295A_explicit_lower_graph_sheet_witness_pair_count": 128,
            "R295A_witness_kind": "ROUND182_GRAPH_SHEET_LEAF",
            "prior_witnesses_recredited_by_Round300A": False,
            "unresolved_exact_pair_count": 3_104,
        },
        "formal_credit_transition": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "required_next": [
            "Construct endpoint-specific zero-trace incidence witnesses for "
            "the exact 3,104 unresolved canonical occurrence pairs.",
            "Require a common positive-area graph-zero patch and two-sided "
            "positive-volume corridor, or a separately sealed glue lemma.",
            "Do not infer edges from outer boxes, closure contact, source "
            "cross-products, occurrence identity, or DSU rank/maximality.",
        ],
        "frontier_ledger": {
            "filename": CANDIDATE_LEDGER,
            "schema": LEDGER_SCHEMA,
            "source_pair_expansion_row_count": len(source_rows),
            "source_pair_expansion_rows_sha256":
                source_commitment["rows_sha256"],
            "canonical_occurrence_pair_row_count": len(frontier_rows),
            "canonical_occurrence_pair_rows_sha256":
                frontier_commitment["rows_sha256"],
            "file_sha256": hashlib.sha256(ledger_raw).hexdigest(),
        },
        "result_sha256": "",
    }
    payload = dict(result)
    payload.pop("result_sha256")
    result["result_sha256"] = sha_object(payload)
    return ledger, result


def validate_candidate_semantics(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> None:
    require(ledger.get("schema") == LEDGER_SCHEMA, "candidate ledger schema")
    source_rows = ledger.get("source_pair_expansion_rows")
    frontier_rows = ledger.get("canonical_occurrence_pair_rows")
    require(
        type(source_rows) is list
        and len(source_rows)
        == ledger.get("source_pair_expansion_row_count") == 3_488,
        "candidate source count",
    )
    require(
        type(frontier_rows) is list
        and len(frontier_rows)
        == ledger.get("canonical_occurrence_pair_row_count") == 3_232,
        "candidate frontier count",
    )
    for row in source_rows:
        check_closed_row(row, "candidate source")
        require(
            row["active_factor_side_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            and row["exact_positive_open_support_intersection"] is False
            and row["source_outer_overlap_is_endpoint_specific_zero_trace_witness"]
            is False
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "candidate source semantics",
        )
    statuses: Counter[str] = Counter()
    duplicate_count = 0
    for row in frontier_rows:
        check_closed_row(row, "candidate frontier")
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        require(
            len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and row["self_pair"] is False
            and row["exact_positive_open_support_intersection"] is False
            and row["opposite_strict_side_exclusion_proved"] is True
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0
            and row["formal_maximality_credit"] == 0,
            "candidate frontier semantics",
        )
        status = row["frontier_disposition"]
        statuses[status] += 1
        duplicate_count += row["duplicate_source_expansion_count"]
        witnessed = row[
            "R295A_explicit_lower_graph_sheet_witness_present"
        ]
        require(
            witnessed
            == row[
                "endpoint_specific_common_positive_area_zero_trace_proved"
            ]
            and bool(row["R295A_physical_incidence_binding_row_ids"])
            == witnessed,
            "candidate witness semantics",
        )
    require(
        statuses == {R295A_WITNESSED: 128, UNRESOLVED: 3_104}
        and duplicate_count == 3_060,
        "candidate frontier partition",
    )
    source_commitment = table_commitment(source_rows, SOURCE_ROW_ID)
    frontier_commitment = table_commitment(frontier_rows, FRONTIER_ROW_ID)
    require(
        ledger["source_pair_expansion_row_ids_sha256"]
        == source_commitment["row_ids_sha256"]
        and ledger["source_pair_expansion_row_hashes_sha256"]
        == source_commitment["row_hashes_sha256"]
        and ledger["source_pair_expansion_rows_sha256"]
        == source_commitment["rows_sha256"]
        and ledger["canonical_occurrence_pair_row_ids_sha256"]
        == frontier_commitment["row_ids_sha256"]
        and ledger["canonical_occurrence_pair_row_hashes_sha256"]
        == frontier_commitment["row_hashes_sha256"]
        and ledger["canonical_occurrence_pair_rows_sha256"]
        == frontier_commitment["rows_sha256"],
        "candidate ledger commitments",
    )
    check_self_result(result, "candidate")
    require(
        result["schema"] == SCHEMA
        and result["producer_sha256"] == PRODUCER_PIN
        and result["semantic_boundary"][
            "canonical_3232_are_not_all_promoted_candidates"
        ] is True
        and result["formal_credit_transition"][
            "formal_component_edge_credit"
        ] == 0
        and result["formal_credit_transition"][
            "formal_DSU_rank_reduction_credit"
        ] == 0
        and result["reconstruction_census"][
            "frontier_pair_without_endpoint_specific_zero_trace_count"
        ] == 3_104,
        "candidate result semantics",
    )


def reclose_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = sha_object(row)


def reclose_ledger(ledger: dict[str, Any]) -> None:
    source = ledger["source_pair_expansion_rows"]
    frontier = ledger["canonical_occurrence_pair_rows"]
    source_commitment = table_commitment(source, SOURCE_ROW_ID)
    frontier_commitment = table_commitment(frontier, FRONTIER_ROW_ID)
    ledger["source_pair_expansion_row_count"] = len(source)
    ledger["source_pair_expansion_row_ids_sha256"] = source_commitment[
        "row_ids_sha256"
    ]
    ledger["source_pair_expansion_row_hashes_sha256"] = source_commitment[
        "row_hashes_sha256"
    ]
    ledger["source_pair_expansion_rows_sha256"] = source_commitment[
        "rows_sha256"
    ]
    ledger["canonical_occurrence_pair_row_count"] = len(frontier)
    ledger["canonical_occurrence_pair_row_ids_sha256"] = frontier_commitment[
        "row_ids_sha256"
    ]
    ledger["canonical_occurrence_pair_row_hashes_sha256"] = (
        frontier_commitment["row_hashes_sha256"]
    )
    ledger["canonical_occurrence_pair_rows_sha256"] = frontier_commitment[
        "rows_sha256"
    ]


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = sha_object(result)


def attack_suite(
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]] = []

    def attack(
        label: str,
        mutation: Callable[[dict[str, Any], dict[str, Any]], None],
    ) -> None:
        attacks.append((label, mutation))

    attack("DROP_SOURCE_ROW", lambda l, r: l[
        "source_pair_expansion_rows"
    ].pop())
    attack("DUPLICATE_SOURCE_ROW", lambda l, r: l[
        "source_pair_expansion_rows"
    ].append(copy.deepcopy(l["source_pair_expansion_rows"][0])))
    attack("REORDER_SOURCE_ROWS", lambda l, r: l[
        "source_pair_expansion_rows"
    ].reverse())
    attack("DROP_FRONTIER_ROW", lambda l, r: l[
        "canonical_occurrence_pair_rows"
    ].pop())
    attack("DUPLICATE_FRONTIER_ROW", lambda l, r: l[
        "canonical_occurrence_pair_rows"
    ].append(copy.deepcopy(l["canonical_occurrence_pair_rows"][0])))
    attack("REORDER_FRONTIER_ROWS", lambda l, r: l[
        "canonical_occurrence_pair_rows"
    ].reverse())

    def mutate_frontier(
        ledger: dict[str, Any],
        field: str,
        value: Any,
        index: int = 0,
    ) -> None:
        row = ledger["canonical_occurrence_pair_rows"][index]
        row[field] = value
        reclose_row(row)

    attack(
        "PROMOTE_UNRESOLVED_COMPONENT_EDGE",
        lambda l, r: mutate_frontier(l, "formal_component_edge_credit", 1),
    )
    attack(
        "GRANT_DSU_RANK",
        lambda l, r: mutate_frontier(
            l, "formal_DSU_rank_reduction_credit", 1
        ),
    )
    attack(
        "GRANT_IDENTITY_COLLAPSE",
        lambda l, r: mutate_frontier(
            l, "formal_occurrence_identity_collapse_credit", 1
        ),
    )
    attack(
        "GRANT_MAXIMALITY",
        lambda l, r: mutate_frontier(l, "formal_maximality_credit", 1),
    )
    attack(
        "CLAIM_POSITIVE_OPEN_INTERSECTION",
        lambda l, r: mutate_frontier(
            l, "exact_positive_open_support_intersection", True
        ),
    )
    attack(
        "ERASE_STRICT_SIDE_EXCLUSION",
        lambda l, r: mutate_frontier(
            l, "opposite_strict_side_exclusion_proved", False
        ),
    )
    attack(
        "CLAIM_CLOSURE_ZERO_IS_EDGE",
        lambda l, r: mutate_frontier(
            l, "parent_regular_graph_zero_in_closure_is_not_itself_an_edge",
            False,
        ),
    )
    attack(
        "FORGE_SELF_PAIR",
        lambda l, r: mutate_frontier(l, "self_pair", True),
    )
    attack(
        "ERASE_SOURCE_PROVENANCE",
        lambda l, r: mutate_frontier(l, "source_Round287_pair_row_ids", []),
    )
    attack(
        "FORGE_DUPLICATE_COUNT",
        lambda l, r: mutate_frontier(
            l,
            "duplicate_source_expansion_count",
            l["canonical_occurrence_pair_rows"][0][
                "duplicate_source_expansion_count"
            ] + 1,
        ),
    )

    def source_positive(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        row = ledger["source_pair_expansion_rows"][0]
        row["exact_positive_open_support_intersection"] = True
        reclose_row(row)

    attack("SOURCE_CLAIM_POSITIVE_INTERSECTION", source_positive)

    def source_signs(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        row = ledger["source_pair_expansion_rows"][0]
        row["active_factor_side_signs"] = [
            "STRICT_POSITIVE", "STRICT_POSITIVE"
        ]
        reclose_row(row)

    attack("SOURCE_FORGE_SAME_SIGNS", source_signs)

    def source_promote(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        row = ledger["source_pair_expansion_rows"][0]
        row["formal_component_edge_credit"] = 1
        reclose_row(row)

    attack("SOURCE_GRANT_COMPONENT_EDGE", source_promote)

    def result_count(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["reconstruction_census"][
            "frontier_pair_without_endpoint_specific_zero_trace_count"
        ] = 3_103
        reclose_result(result)

    attack("RESULT_FORGE_3104_COUNT", result_count)

    def result_promote(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["formal_credit_transition"][
            "formal_component_edge_credit"
        ] = 3_104
        reclose_result(result)

    attack("RESULT_PROMOTE_3104_EDGES", result_promote)

    def result_claim_all(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["semantic_boundary"][
            "canonical_3232_are_not_all_promoted_candidates"
        ] = False
        reclose_result(result)

    attack("RESULT_CLAIM_ALL_3232_PROMOTED", result_claim_all)

    def result_pin(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["input_file_pins"][R287_LEDGER] = "0" * 64
        reclose_result(result)

    attack("RESULT_FORGE_INPUT_PIN", result_pin)

    def result_producer(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["producer_sha256"] = "f" * 64
        reclose_result(result)

    attack("RESULT_FORGE_PRODUCER_PIN", result_producer)

    def result_hash(ledger: dict[str, Any], result: dict[str, Any]) -> None:
        result["result_sha256"] = "0" * 64

    attack("RESULT_BREAK_SELF_CLOSURE", result_hash)

    records: list[dict[str, Any]] = []
    semantic_reclosed_count = 0
    for label, mutation in attacks:
        ledger = copy.deepcopy(expected_ledger)
        result = copy.deepcopy(expected_result)
        mutation(ledger, result)
        if label.startswith(("DROP_", "DUPLICATE_", "REORDER_")):
            try:
                reclose_ledger(ledger)
            except VerificationError:
                pass
        semantic_reclosed = label not in {"RESULT_BREAK_SELF_CLOSURE"}
        semantic_reclosed_count += int(semantic_reclosed)
        rejected = False
        reason = ""
        try:
            validate_candidate_semantics(ledger, result)
            require(
                ledger == expected_ledger and result == expected_result,
                "expected equality",
            )
        except (VerificationError, KeyError, IndexError, TypeError) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        require(rejected, "attack accepted:" + label)
        records.append({
            "attack_label": label,
            "semantic_payload_reclosed": semantic_reclosed,
            "rejected": True,
            "rejection_reason": reason,
        })
    require(len(records) == 25, "attack census")
    suite = {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_ALL_INDEPENDENT_ATTACKS_REJECTED",
        "attack_count": len(records),
        "rejected_count": len(records),
        "semantic_reclosed_attack_count": semantic_reclosed_count,
        "all_attacks_rejected": True,
        "producer_attack_suite_imported_or_trusted": False,
        "attacks": records,
        "attack_suite_sha256": "",
    }
    payload = dict(suite)
    payload.pop("attack_suite_sha256")
    suite["attack_suite_sha256"] = sha_object(payload)
    return suite


def atomic_write(path: Path, raw: bytes) -> None:
    require(not path.is_symlink(), "output symlink:" + str(path))
    parent = path.parent.resolve()
    require(parent.is_dir(), "output parent:" + str(path))
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=parent,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="300311")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--attacks", type=Path, default=ATTACKS)
    parser.add_argument("--verification", type=Path, default=VERIFICATION)
    args = parser.parse_args()
    require(bool(args.seed), "nonempty seed")

    # Expected objects are fully reconstructed before either candidate opens.
    expected_ledger, expected_result = reconstruct_expected()
    expected_ledger_raw = gzip_bytes(expected_ledger)
    expected_result_raw = canonical(expected_result) + b"\n"

    candidate_ledger_raw = regular_bytes(HERE / CANDIDATE_LEDGER)
    candidate_result_raw = regular_bytes(HERE / CANDIDATE_RESULT)
    candidate_ledger = decode_object(
        gzip.decompress(candidate_ledger_raw), CANDIDATE_LEDGER
    )
    candidate_result = decode_object(candidate_result_raw, CANDIDATE_RESULT)
    validate_candidate_semantics(candidate_ledger, candidate_result)
    require(
        candidate_ledger == expected_ledger
        and candidate_result == expected_result
        and candidate_ledger_raw == expected_ledger_raw
        and candidate_result_raw == expected_result_raw,
        "candidate full object/byte equality",
    )

    attacks = attack_suite(expected_ledger, expected_result)
    attack_bytes = canonical(attacks) + b"\n"
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND300A_FAIL_CLOSED_FRONTIER_"
            "EXHAUSTION__3488_TO_6292_TO_3232__128_PRIOR_WITNESSED__"
            "3104_UNRESOLVED__ZERO_COMPONENT_EDGE_CREDIT",
        "pins": {
            PRODUCER: PRODUCER_PIN,
            CANDIDATE_LEDGER:
                hashlib.sha256(candidate_ledger_raw).hexdigest(),
            CANDIDATE_RESULT:
                hashlib.sha256(candidate_result_raw).hexdigest(),
            **dict(sorted(INPUT_PINS.items())),
        },
        "independence_contract": {
            "producer_imported_or_executed": False,
            "producer_tokenized_AST_parsed_or_text_decoded": False,
            "producer_used_only_as_inert_fixed_SHA256_bytes": True,
            "expected_reconstruction_completed_before_candidate_open": True,
            "complete_Round294_registry_rows_streamed": 431_208,
            "complete_Round294_binding_rows_streamed": 46_288,
            "complete_Round295A_incidence_rows_streamed": 113_452,
            "candidate_ledger_result_object_and_byte_equality": True,
            "deterministic_gzip_byte_equality": True,
            "seed_affects_output": False,
        },
        "reconstruction": expected_result["reconstruction_census"],
        "semantic_conclusion": {
            "canonical_3232_are_not_all_promoted_candidates": True,
            "R295A_explicit_prior_witness_pair_count": 128,
            "exact_unresolved_endpoint_specific_zero_trace_pair_count":
                3_104,
            "positive_open_support_intersection_count": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_maximality_credit": 0,
        },
        "semantic_attack_suite": {
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "semantic_reclosed_attack_count":
                attacks["semantic_reclosed_attack_count"],
            "all_attacks_rejected": True,
            "attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
        "verification_sha256": "",
    }
    payload = dict(verification)
    payload.pop("verification_sha256")
    verification["verification_sha256"] = sha_object(payload)
    verification_bytes = canonical(verification) + b"\n"
    if not args.no_write:
        atomic_write(args.attacks, attack_bytes)
        atomic_write(args.verification, verification_bytes)
    print(verification["status"])
    print(json.dumps(verification["reconstruction"], sort_keys=True))
    print("attack_suite_file_sha256=" + hashlib.sha256(attack_bytes).hexdigest())
    print("attack_suite_sha256=" + attacks["attack_suite_sha256"])
    print(
        "verification_file_sha256="
        + hashlib.sha256(verification_bytes).hexdigest()
    )
    print("verification_sha256=" + verification["verification_sha256"])


if __name__ == "__main__":
    main()
