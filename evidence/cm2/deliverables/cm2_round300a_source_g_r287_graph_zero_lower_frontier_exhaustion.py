#!/usr/bin/env python3
"""Round300-A: exhaust the R287 graph-zero lower frontier, fail closed.

The 3,488 R287 rows are pairs of opposite *open* factor sides of one
regular-graph cell.  After the complete Round294 representation map is
applied they yield 6,292 raw endpoint expansions and 3,232 canonical
unordered occurrence pairs.  A complete scan of the Round295-A physical
witness ledger finds explicit lower graph-sheet witnesses for 128 of those
pairs.  The remaining 3,104 pairs do not have endpoint-specific common
zero-trace witnesses.

This package is deliberately diagnostic.  Outer-box overlap and a common
zero set in the closures do not imply intersection of the two strict open
supports.  No component edge, DSU rank, identity, seam, maximality, fibre,
or global-disposition credit is issued.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

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


class ClosureError(RuntimeError):
    """Fail-closed construction error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ClosureError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for piece in chunks(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def guarded_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    need(path.parent.resolve() == HERE.resolve(), "path parent:" + path.name)
    need(path.exists() and not path.is_symlink(), "path exists:" + path.name)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "path regular/link/size:" + path.name,
    )
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate key:" + label + ":" + key)
            result[key] = value
        return result

    def reject(token: str) -> Any:
        raise ClosureError("noninteger JSON token:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ClosureError("strict JSON:" + label) from error
    need(type(value) is dict, "top object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(guarded_bytes(HERE / name), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    try:
        raw = gzip.decompress(guarded_bytes(HERE / name))
    except Exception as error:
        raise ClosureError("gzip:" + name) from error
    return strict_decode(raw, name)


def validate_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "row closure:" + label,
    )


def close_row(
    prefix: str,
    domain: str,
    id_field: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {id_field: prefix + digest([domain, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


class ListHasher:
    """Incremental canonical-JSON commitment to a list."""

    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for piece in chunks(value):
            self.state.update(piece)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def rows_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique row IDs:" + id_field)
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
    }


def parse_manifest(name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    raw = guarded_bytes(HERE / name, 200_000)
    for line in raw.decode("utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        sha256, filename = match.groups()
        need(
            Path(filename).name == filename and filename not in result,
            "manifest path/duplicate:" + name,
        )
        result[filename] = sha256
    need(bool(result), "empty manifest:" + name)
    return result


def validate_input_boundary() -> None:
    for name, expected in MANIFEST_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "manifest pin syntax")
        need(file_sha256(HERE / name) == expected, "manifest pin:" + name)
    for name, expected in INPUT_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "input pin syntax")
        need(file_sha256(HERE / name) == expected, "input pin:" + name)
    memberships = {
        R275_MANIFEST: [R275_CERTIFICATE],
        R287_MANIFEST: [R287_LEDGER, R287_RESULT, R287_VERIFICATION],
        R294_MANIFEST: [
            R294_REGISTRY, R294_BINDINGS, R294_RESULT, R294_VERIFICATION
        ],
        R295A_MANIFEST: [
            R295A_INCIDENCE, R295A_RESULT, R295A_VERIFICATION
        ],
    }
    for manifest_name, members in memberships.items():
        manifest = parse_manifest(manifest_name)
        for member in members:
            need(
                manifest.get(member) == INPUT_PINS[member],
                "manifest selected member:" + manifest_name + ":" + member,
            )


def iterate_array(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        piece = stream.read(1 << 20)
        need(bool(piece), "array marker:" + marker)
        buffer += piece
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "stream duplicate key:" + key)
            result[key] = value
        return result

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            ClosureError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ClosureError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), "unexpected streamed EOF")
            buffer = piece
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
                piece = stream.read(1 << 20)
                need(bool(piece), "malformed streamed row")
                buffer += piece
        need(type(value) is dict, "streamed row object")
        yield value
        buffer = buffer[end:]


def scan_gzip_rows(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    rows_hash = ListHasher()
    ids_hash = ListHasher()
    row_hashes_hash = ListHasher()
    occurrence_ids_hash = (
        ListHasher() if "occurrence_ids_sha256" in expected else None
    )
    with gzip.open(
        HERE / name, "rt", encoding="utf-8", newline=""
    ) as stream:
        for row in iterate_array(stream):
            validate_row(row, name)
            rows_hash.add(row)
            ids_hash.add(row[id_field])
            row_hashes_hash.add(row["row_sha256"])
            if occurrence_ids_hash is not None:
                occurrence_ids_hash.add(row["registry_occurrence_id"])
            visit(row)
    actual = {
        "row_count": rows_hash.count,
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": row_hashes_hash.finish(),
        "rows_sha256": rows_hash.finish(),
    }
    if occurrence_ids_hash is not None:
        actual["occurrence_ids_sha256"] = occurrence_ids_hash.finish()
    need(
        actual == expected,
        "stream commitment:" + name
        + ":actual=" + json.dumps(actual, sort_keys=True)
        + ":expected=" + json.dumps(expected, sort_keys=True),
    )


def verify_embedded_table(
    document: dict[str, Any],
    rows_name: str,
    count_name: str,
    digest_name: str,
) -> list[dict[str, Any]]:
    rows = document.get(rows_name)
    need(
        type(rows) is list
        and len(rows) == document.get(count_name)
        and digest(rows) == document.get(digest_name),
        "R287 table commitment:" + rows_name,
    )
    for row in rows:
        validate_row(row, "R287:" + rows_name)
    return rows


def validate_result_self(document: dict[str, Any], label: str) -> None:
    claimed = document.get("result_sha256")
    payload = dict(document)
    payload.pop("result_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "result self closure:" + label,
    )


def reconstruct_r275_r287() -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
]:
    certificate = read_json(R275_CERTIFICATE)
    need(
        digest(certificate["result"]) == certificate["result_sha256"],
        "Round275 wrapper closure",
    )
    result = certificate["result"]
    all_regions: list[dict[str, Any]] = []
    for table_name, expected_count in (
        ("strict_region_ledger", 5_288),
        ("arrangement_region_ledger", 8_500),
    ):
        table = result[table_name]
        rows = table["rows"]
        need(
            len(rows) == table["row_count"] == expected_count
            and digest(rows) == table["rows_sha256"]
            and digest(
                [row["reverse_rechart_region_row_id"] for row in rows]
            ) == table["row_ids_sha256"]
            and digest([row["row_sha256"] for row in rows])
            == table["row_hashes_sha256"],
            "Round275 table:" + table_name,
        )
        for row in rows:
            validate_row(row, "Round275:" + table_name)
        all_regions.extend(rows)
    regions = {
        row["reverse_rechart_region_row_id"]: row for row in all_regions
    }
    need(len(regions) == 13_788, "Round275 unique regions")

    crossing_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in result["arrangement_region_ledger"]["rows"]:
        if row["arrangement_classification"] != "REGULAR_GRAPH_CROSSING":
            continue
        key = (
            row["source_guard_row_id"],
            row["parent_id"],
            row["owner_target"],
            row["source_chart"],
            row["adjacent_chart"],
            tuple(row["adjacent_cover_refinement_path"]),
            tuple(row["adjacent_rational_region_box"]),
            row["active_reason"],
            tuple(row["strict_derivative_signs_t_p_s"]),
        )
        crossing_groups[key].append(row)
    need(len(crossing_groups) == 3_488, "Round275 crossing group census")

    r287 = read_gzip_json(R287_LEDGER)
    need(
        r287["schema"]
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition."
        "ledger.v1",
        "Round287 schema",
    )
    region_rows = verify_embedded_table(
        r287, "region_rows", "region_row_count", "region_rows_sha256"
    )
    verify_embedded_table(
        r287,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    verify_embedded_table(
        r287,
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
    )
    verify_embedded_table(
        r287,
        "valid_internal_physical_face_rows",
        "valid_internal_physical_face_row_count",
        "valid_internal_physical_face_rows_sha256",
    )
    candidate_pairs = verify_embedded_table(
        r287,
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
    )
    need(
        (
            len(region_rows),
            r287["refinement_cell_row_count"],
            r287["potential_new_support_union_row_count"],
            r287["valid_internal_physical_face_row_count"],
            len(candidate_pairs),
        )
        == (13_788, 7_616, 10_020, 648, 3_488),
        "Round287 complete census",
    )
    dispositions = {
        row["Round275_region_id"]: row for row in region_rows
    }
    need(set(dispositions) == set(regions), "Round287 region coverage")

    expected_pairs: list[dict[str, Any]] = []
    for key in sorted(crossing_groups):
        sides = crossing_groups[key]
        need(len(sides) == 2, "Round275 crossing side multiplicity")
        sides.sort(key=lambda row: row["reverse_rechart_region_row_id"])
        left, right = sides
        left_id = left["reverse_rechart_region_row_id"]
        right_id = right["reverse_rechart_region_row_id"]
        need(
            {
                left["active_factor_side_sign"],
                right["active_factor_side_sign"],
            }
            == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            and left["complete_10_field_return_signature_sha256"]
            != right["complete_10_field_return_signature_sha256"],
            "Round275 crossing side contract",
        )
        payload = {
            "Round287_mutually_exclusive_outer_overlap_pair_row_id":
                "round287-mutually-exclusive-pair:"
                + digest(sorted([left_id, right_id])),
            "left_Round275_region_id": min(left_id, right_id),
            "right_Round275_region_id": max(left_id, right_id),
            "adjacent_chart": left["adjacent_chart"],
            "source_guard_row_id": left["source_guard_row_id"],
            "active_reason": left["active_reason"],
            "active_factor_side_signs": [
                "STRICT_NEGATIVE", "STRICT_POSITIVE"
            ],
            "exact_positive_physical_overlap": False,
            "reason": "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES",
            "occurrence_identity_collapse_credit": 0,
            "component_edge_credit": 0,
        }
        payload["row_sha256"] = digest(payload)
        expected_pairs.append(payload)
    expected_pairs.sort(
        key=lambda row: row[
            "Round287_mutually_exclusive_outer_overlap_pair_row_id"
        ]
    )
    candidate_pairs.sort(
        key=lambda row: row[
            "Round287_mutually_exclusive_outer_overlap_pair_row_id"
        ]
    )
    need(expected_pairs == candidate_pairs, "Round287 pair reconstruction")

    r287_result = read_json(R287_RESULT)
    validate_result_self(r287_result, "Round287")
    need(
        r287_result["census"][
            "R275_pairwise_outer_positive_overlap_pair_count"
        ] == 3_488
        and r287_result["census"][
            "R275_pairwise_actual_positive_overlap_pair_count"
        ] == 0,
        "Round287 pair result contract",
    )
    r287_verification = read_json(R287_VERIFICATION)
    need(
        r287_verification["status"].startswith(
            "PASS_INDEPENDENT_ROUND287"
        ),
        "Round287 verification status",
    )
    return dispositions, candidate_pairs


def reconstruct_round294_map(
    region_ids: set[str],
) -> tuple[dict[str, set[str]], dict[str, int]]:
    result = read_json(R294_RESULT)
    validate_result_self(result, "Round294")
    need(
        result["status"].startswith(
            "PASS_ROUND294_ATOMIC_STAGE_A_OCCURRENCE_REGISTRY_PROMOTION"
        )
        and result["registry_ledger"]["file_sha256"]
        == INPUT_PINS[R294_REGISTRY]
        and result["representation_binding_ledger"]["file_sha256"]
        == INPUT_PINS[R294_BINDINGS],
        "Round294 sealed result contract",
    )
    verification = read_json(R294_VERIFICATION)
    need(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round294 verification status",
    )

    region_to_occurrences: dict[str, set[str]] = defaultdict(set)
    binding_kind_histogram: Counter[str] = Counter()

    def visit_binding(row: dict[str, Any]) -> None:
        kind = row["alias_source_kind"]
        binding_kind_histogram[kind] += 1
        region_id = row.get("Round275_region_id")
        if region_id is None:
            need(
                kind == "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE",
                "Round294 null-region binding kind",
            )
            return
        need(region_id in region_ids, "Round294 binding region")
        region_to_occurrences[region_id].add(
            row["target_registry_occurrence_id"]
        )

    scan_gzip_rows(
        R294_BINDINGS,
        "Round294_occurrence_representation_binding_row_id",
        R294_BINDING_COMMITMENT,
        visit_binding,
    )
    need(
        binding_kind_histogram == {
            "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE": 36_680,
            "ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476,
            "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 5_532,
            "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL": 1_600,
        },
        "Round294 binding kind census",
    )

    all_occurrences: set[str] = set()
    registry_kind_histogram: Counter[str] = Counter()

    def visit_registry(row: dict[str, Any]) -> None:
        occurrence_id = row["registry_occurrence_id"]
        need(
            occurrence_id not in all_occurrences,
            "Round294 duplicate occurrence ID",
        )
        all_occurrences.add(occurrence_id)
        kind = row["registry_entry_kind"]
        registry_kind_histogram[kind] += 1
        if kind == REFINED_KIND:
            region_id = row["Round275_region_id"]
            need(region_id in region_ids, "Round294 refined region")
            region_to_occurrences[region_id].add(occurrence_id)

    scan_gzip_rows(
        R294_REGISTRY,
        "Round294_occurrence_registry_row_id",
        R294_REGISTRY_COMMITMENT,
        visit_registry,
    )
    need(
        registry_kind_histogram == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            REFINED_KIND: 9_404,
        },
        "Round294 registry kind census",
    )
    need(
        set(region_to_occurrences) == region_ids
        and all(
            occurrence in all_occurrences
            for values in region_to_occurrences.values()
            for occurrence in values
        ),
        "Round294 complete normalized endpoint map",
    )
    mapping_histogram = Counter(
        len(values) for values in region_to_occurrences.values()
    )
    need(
        mapping_histogram
        == {
            1: 11_208,
            2: 1_680,
            3: 268,
            4: 232,
            5: 220,
            6: 76,
            10: 88,
            11: 16,
        },
        "Round294 endpoint multiplicity histogram",
    )
    return region_to_occurrences, {
        str(key): value for key, value in sorted(mapping_histogram.items())
    }


def reconstruct_round295a_witnesses() -> tuple[
    dict[tuple[str, str], list[dict[str, Any]]],
    dict[str, int],
]:
    result = read_json(R295A_RESULT)
    validate_result_self(result, "Round295A")
    need(
        result["status"].startswith(
            "PASS_ROUND295A_ATOMIC_R291_POSITIVE_T_CONTINUATION_CLOSURE"
        )
        and result["physical_witness_incidence_binding_ledger"][
            "file_sha256"
        ] == INPUT_PINS[R295A_INCIDENCE],
        "Round295A sealed result contract",
    )
    verification = read_json(R295A_VERIFICATION)
    need(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        ),
        "Round295A verification status",
    )

    pair_witnesses: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    reference_histogram: Counter[int] = Counter()

    def visit(row: dict[str, Any]) -> None:
        reference_count = row["target_Round294_registry_reference_count"]
        target_ids = row["target_Round294_registry_occurrence_ids"]
        need(
            len(target_ids) == reference_count
            and len(target_ids) == len(set(target_ids)),
            "Round295A target reference arity",
        )
        reference_histogram[reference_count] += 1
        if reference_count != 2:
            return
        pair = tuple(sorted(target_ids))
        need(pair[0] != pair[1], "Round295A two-target self pair")
        pair_witnesses[pair].append({
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

    scan_gzip_rows(
        R295A_INCIDENCE,
        "Round295A_R291_physical_incidence_binding_row_id",
        R295A_INCIDENCE_COMMITMENT,
        visit,
    )
    need(
        reference_histogram == {1: 1_600, 2: 111_852}
        and len(pair_witnesses) == 111_524,
        "Round295A pair census",
    )
    return pair_witnesses, {
        "two_target_raw_witness_row_count": 111_852,
        "two_target_unique_pair_count": 111_524,
        "two_target_duplicate_witness_row_count": 328,
    }


def pair_id(pair: tuple[str, str]) -> str:
    return "round300a-canonical-occurrence-pair:" + digest([
        "ROUND300A_CANONICAL_UNORDERED_OCCURRENCE_PAIR_V1",
        list(pair),
    ])


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=buffer,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def atomic_write(path: Path, payload: bytes) -> None:
    parent = path.parent.resolve()
    need(parent.is_dir(), "output parent:" + str(path))
    need(not path.is_symlink(), "output symlink:" + str(path))
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=parent,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def build(
    producer_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_input_boundary()
    dispositions, source_pairs = reconstruct_r275_r287()
    region_ids = set(dispositions)
    region_to_occurrences, mapping_histogram = reconstruct_round294_map(
        region_ids
    )
    r295a_witnesses, r295a_census = reconstruct_round295a_witnesses()

    source_rows: list[dict[str, Any]] = []
    provenance: dict[tuple[str, str], list[str]] = defaultdict(list)
    raw_expansion_count = 0
    self_pair_count = 0
    source_endpoint_histogram: Counter[tuple[int, int]] = Counter()

    for source in source_pairs:
        left_region = source["left_Round275_region_id"]
        right_region = source["right_Round275_region_id"]
        left_occurrences = sorted(region_to_occurrences[left_region])
        right_occurrences = sorted(region_to_occurrences[right_region])
        source_endpoint_histogram[
            (len(left_occurrences), len(right_occurrences))
        ] += 1
        local_pairs: list[tuple[str, str]] = []
        for left in left_occurrences:
            for right in right_occurrences:
                raw_expansion_count += 1
                if left == right:
                    self_pair_count += 1
                    continue
                pair = tuple(sorted((left, right)))
                local_pairs.append(pair)
                provenance[pair].append(
                    source[
                        "Round287_mutually_exclusive_outer_overlap_pair_row_id"
                    ]
                )
        need(
            len(local_pairs) == len(set(local_pairs)),
            "source-local expansion injectivity",
        )
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
            "left_Round294_registry_occurrence_ids": left_occurrences,
            "right_Round294_registry_occurrence_ids": right_occurrences,
            "left_endpoint_occurrence_count": len(left_occurrences),
            "right_endpoint_occurrence_count": len(right_occurrences),
            "raw_occurrence_pair_expansion_count": len(local_pairs),
            "canonical_occurrence_pair_row_ids":
                sorted(pair_id(pair) for pair in local_pairs),
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
        source_rows.append(close_row(
            "round300a-source-pair-expansion:",
            "ROUND300A_R287_SOURCE_PAIR_EXPANSION_V1",
            SOURCE_ROW_ID,
            payload,
        ))
    source_rows.sort(key=lambda row: row[SOURCE_ROW_ID])

    need(
        raw_expansion_count == 6_292
        and self_pair_count == 0
        and len(provenance) == 3_232,
        "frontier expansion census",
    )
    witnessed_frontier = set(provenance) & set(r295a_witnesses)
    need(len(witnessed_frontier) == 128, "Round295A intersection census")

    frontier_rows: list[dict[str, Any]] = []
    status_histogram: Counter[str] = Counter()
    for pair in sorted(provenance):
        witness_refs = sorted(
            r295a_witnesses.get(pair, []),
            key=lambda item: item["row_id"],
        )
        witnessed = bool(witness_refs)
        if witnessed:
            need(
                len(witness_refs) == 1,
                "frontier explicit witness multiplicity",
            )
            witness = witness_refs[0]
            need(
                witness["canonical_support_kind"]
                == "NOMINAL_REGULAR_ZERO_SET_IF_PRESENT"
                and witness["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
                and witness["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
                and witness["binding_classification"]
                == "FORMAL_ROUND294_REGISTRY_REBIND__"
                "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
                and witness["exact_coverage"] is True
                and witness["formal_incidence_credit"] == 1,
                "frontier explicit lower graph-sheet witness contract",
            )
        status = R295A_WITNESSED if witnessed else UNRESOLVED
        status_histogram[status] += 1
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
                [item["row_id"] for item in witness_refs],
            "R295A_physical_incidence_binding_row_sha256s":
                [item["row_sha256"] for item in witness_refs],
            "endpoint_specific_common_positive_area_zero_trace_proved":
                witnessed,
            "frontier_disposition": status,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_maximality_credit": 0,
        }
        frontier_rows.append(close_row(
            "round300a-canonical-occurrence-pair:",
            "ROUND300A_CANONICAL_OCCURRENCE_PAIR_DISPOSITION_V1",
            FRONTIER_ROW_ID,
            payload,
        ))
    frontier_rows.sort(key=lambda row: row[FRONTIER_ROW_ID])
    need(
        status_histogram == {
            R295A_WITNESSED: 128,
            UNRESOLVED: 3_104,
        },
        "frontier disposition census",
    )
    duplicate_expansion_count = sum(
        row["duplicate_source_expansion_count"] for row in frontier_rows
    )
    need(duplicate_expansion_count == 3_060, "duplicate expansion census")

    source_commitment = rows_commitment(source_rows, SOURCE_ROW_ID)
    frontier_commitment = rows_commitment(frontier_rows, FRONTIER_ROW_ID)
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

    source_histogram = {
        f"{left}x{right}": count
        for (left, right), count in sorted(source_endpoint_histogram.items())
    }
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
            "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION",
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "producer_sha256": producer_sha256,
        "seed_affects_output": False,
        "reconstruction_census": {
            "R275_region_count": 13_788,
            "R287_regular_graph_source_pair_count": 3_488,
            "Round294_region_endpoint_multiplicity_histogram":
                mapping_histogram,
            "source_pair_endpoint_multiplicity_histogram":
                source_histogram,
            "raw_occurrence_pair_expansion_count": 6_292,
            "canonical_unordered_occurrence_pair_count": 3_232,
            "self_occurrence_pair_count": 0,
            "duplicate_source_expansion_count": 3_060,
            "R295A_two_target_raw_witness_row_count":
                r295a_census["two_target_raw_witness_row_count"],
            "R295A_two_target_unique_pair_count":
                r295a_census["two_target_unique_pair_count"],
            "R295A_two_target_duplicate_witness_row_count":
                r295a_census["two_target_duplicate_witness_row_count"],
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
            "filename": LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "source_pair_expansion_row_count": len(source_rows),
            "source_pair_expansion_rows_sha256":
                source_commitment["rows_sha256"],
            "canonical_occurrence_pair_row_count": len(frontier_rows),
            "canonical_occurrence_pair_rows_sha256":
                frontier_commitment["rows_sha256"],
            "file_sha256": "",
        },
        "result_sha256": "",
    }
    return ledger, result


def finalize_result(
    result: dict[str, Any],
    ledger_file_sha256: str,
) -> dict[str, Any]:
    value = json.loads(canonical(result))
    value["frontier_ledger"]["file_sha256"] = ledger_file_sha256
    value["result_sha256"] = ""
    payload = dict(value)
    payload.pop("result_sha256")
    value["result_sha256"] = digest(payload)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="300101")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    args = parser.parse_args()
    need(bool(args.seed), "nonempty seed bookkeeping")
    producer_sha256 = file_sha256(Path(__file__).resolve())
    ledger, result = build(producer_sha256)
    ledger_bytes = deterministic_gzip(ledger)
    result = finalize_result(result, hashlib.sha256(ledger_bytes).hexdigest())
    result_bytes = canonical(result) + b"\n"
    atomic_write(args.ledger, ledger_bytes)
    atomic_write(args.result, result_bytes)
    print(result["status"])
    print(json.dumps(result["reconstruction_census"], sort_keys=True))
    print("producer_sha256=" + producer_sha256)
    print("ledger_file_sha256=" + hashlib.sha256(ledger_bytes).hexdigest())
    print("result_file_sha256=" + hashlib.sha256(result_bytes).hexdigest())
    print("result_sha256=" + result["result_sha256"])


if __name__ == "__main__":
    main()
