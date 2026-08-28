#!/usr/bin/env python3
"""Compose the sealed Round295-A and Round295-B all-stratum scope.

Round295-C does not create occurrences, seam edges, components, or a DSU.
It atomically:

* normalizes every Round295-B physical target to an actual Round294
  ``registry_occurrence_id``;
* closes one canonical row for each of the 9,528 Round289 relations, with
  complete child references and exact rational area conservation; and
* freezes an eight-row inventory of the complete Round294/Round295-A/
  Round295-B scope that must precede seam pairing and the expanded DSU.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from fractions import Fraction as Q
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round295c_source_g_all_stratum_scope_composition_closure"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

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
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)

A_ALIASES = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "representation_alias_ledger.json.gz"
)
A_PHYSICAL = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
A_ABSENCE = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "absence_no_binding_ledger.json.gz"
)
A_RESULT = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "result.json"
)
A_VERIFICATION = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verification.json"
)
A_ATTACKS = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "attack_suite.json"
)
A_MANIFEST = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "manifest.sha256"
)

B_LEDGER = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_ledger.json.gz"
)
B_RESULT = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_result.json"
)
B_VERIFICATION = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_"
    "verification.json"
)
B_MANIFEST = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_"
    "manifest.sha256"
)

INPUT_PINS = {
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294_BINDINGS:
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R294_RESULT:
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    A_ALIASES:
        "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    A_PHYSICAL:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    A_ABSENCE:
        "9e28ee87b5a031a7f1c457d3fa26601925dbdf07dd5857c8e2108891891243b0",
    A_RESULT:
        "0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d",
    A_VERIFICATION:
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
    A_ATTACKS:
        "ecf3da6b5be1d6e790d39240ee93f5457651f7e3605c6388e05a69c9027ece16",
    A_MANIFEST:
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    B_LEDGER:
        "1714945c470607a68c9fb5e323319899faabd187ecbccd00d266ea6f9361007c",
    B_RESULT:
        "b10c5caf9813887b06f2ed49796e02befc8abdc048e6909c2146bfc120e6334a",
    B_VERIFICATION:
        "f823fd7c7a34d39163bc887d6544ea670915e9ecb93fc2a94947f4ee777180a1",
    B_MANIFEST:
        "09cec800efc3c7dd21bebab4a226d384f51ec1273040c548bfa54834a25c8331",
}

SCHEMA = "cm2.round295c.source-g-all-stratum-scope-composition-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ZERO_FIELDS = (
    "formal_new_occurrence_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)

EXPECTED_TARGET_MULTIPLICITY_HISTOGRAM = {
    1: 2388, 2: 632, 3: 312, 4: 40, 5: 32, 6: 16, 8: 72,
    9: 4, 10: 4, 11: 8, 12: 64, 14: 4, 16: 84, 18: 72,
    20: 8, 24: 8, 32: 8, 56: 8, 65: 8, 83: 8,
}


class ClosureError(RuntimeError):
    """Fail-closed Round295-C construction error."""


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


def guard_path(path: Path, maximum: int = 2_000_000_000) -> bytes:
    need(path.parent == HERE, f"path parent:{path}")
    need(path.exists() and not path.is_symlink(), f"path exists:{path}")
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"path regular/link/size:{path.name}",
    )
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict bytes:{label}",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            need(key not in value, f"duplicate key:{label}:{key}")
            value[key] = item
        return value

    def reject(token: str) -> Any:
        raise ClosureError(f"non-integral JSON token:{label}:{token}")

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, f"top object:{label}")
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(guard_path(HERE / name), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    raw = guard_path(HERE / name)
    try:
        payload = gzip.decompress(raw)
    except Exception as error:
        raise ClosureError(f"gzip decode:{name}") from error
    return strict_decode(payload, name)


def verify_self_digest(
    value: dict[str, Any], field: str, label: str
) -> None:
    claimed = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    need(
        isinstance(claimed, str) and claimed == digest(payload),
        f"self digest:{label}",
    )


def validate_row_hash(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        isinstance(claimed, str) and claimed == digest(payload),
        f"row hash:{label}",
    )


def close_row(
    prefix: str, domain: str, id_field: str, payload: dict[str, Any]
) -> dict[str, Any]:
    row = {
        id_field: prefix + digest([domain, payload]),
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


def parse_manifest(name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in guard_path(HERE / name, 100_000).decode().splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in result, f"manifest duplicate:{name}:{filename}")
        result[filename] = sha256
    return result


class ListCommitment:
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
        result = self.state.copy()
        result.update(b"]")
        return result.hexdigest()


def commitment_for_rows(
    rows: list[dict[str, Any]], id_field: str
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique IDs:{id_field}")
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
    }


def validate_nested_table(
    table: dict[str, Any],
    id_field: str,
    expected_count: int,
    label: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = table["rows"]
    need(
        type(rows) is list
        and len(rows) == table["row_count"] == expected_count,
        f"table count:{label}",
    )
    for row in rows:
        validate_row_hash(row, label)
    commitment = commitment_for_rows(rows, id_field)
    need(
        all(table[key] == commitment[key] for key in commitment),
        f"table commitments:{label}",
    )
    return rows, commitment


def scan_large_gzip_ledger(
    name: str, visit: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    path = HERE / name
    guard_path(path)
    decoder = json.JSONDecoder(
        object_pairs_hook=lambda pairs: dict(pairs),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    marker = '"rows":['
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        prefix = ""
        while marker not in prefix:
            piece = stream.read(1 << 20)
            need(bool(piece), f"rows marker:{name}")
            prefix += piece
        before, buffer = prefix.split(marker, 1)
        count = 0
        while True:
            buffer = buffer.lstrip()
            if buffer.startswith(","):
                buffer = buffer[1:].lstrip()
            if buffer.startswith("]"):
                buffer = buffer[1:]
                break
            while True:
                try:
                    row, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    piece = stream.read(1 << 20)
                    need(bool(piece), f"truncated rows:{name}:{count}")
                    buffer += piece
            need(type(row) is dict, f"row object:{name}:{count}")
            visit(row)
            count += 1
            buffer = buffer[end:]
        suffix = buffer + stream.read()
    metadata = strict_decode(
        (before + '"rows":[]' + suffix).encode(),
        f"{name}:metadata",
    )
    need(metadata["rows"] == [], f"empty metadata rows:{name}")
    metadata["streamed_row_count"] = count
    return metadata


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def rectangle_area(values: list[str]) -> Q:
    need(len(values) == 4, "rectangle arity")
    p0, p1, s0, s1 = map(Q, values)
    need(p0 < p1 and s0 < s1, "positive rectangle")
    return (p1 - p0) * (s1 - s0)


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", fileobj=buffer, mode="wb", mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), f"output parent:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=HERE, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def validate_packages() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any]
]:
    for name, expected in INPUT_PINS.items():
        need(
            file_sha256(HERE / name) == expected,
            f"frozen input pin:{name}",
        )
    manifest294 = parse_manifest(R294_MANIFEST)
    for name in (
        R294_REGISTRY, R294_BINDINGS, R294_RESULT, R294_VERIFICATION
    ):
        need(
            manifest294.get(name) == INPUT_PINS[name],
            f"Round294 manifest:{name}",
        )
    manifest_a = parse_manifest(A_MANIFEST)
    for name in (
        A_ALIASES, A_PHYSICAL, A_ABSENCE, A_RESULT,
        A_VERIFICATION, A_ATTACKS,
    ):
        need(
            manifest_a.get(name) == INPUT_PINS[name],
            f"Round295-A manifest:{name}",
        )
    manifest_b = parse_manifest(B_MANIFEST)
    for name in (B_LEDGER, B_RESULT, B_VERIFICATION):
        need(
            manifest_b.get(name) == INPUT_PINS[name],
            f"Round295-B manifest:{name}",
        )

    result294 = read_json(R294_RESULT)
    result_a = read_json(A_RESULT)
    result_b = read_json(B_RESULT)
    verification294 = read_json(R294_VERIFICATION)
    verification_a = read_json(A_VERIFICATION)
    verification_b = read_json(B_VERIFICATION)
    verify_self_digest(result294, "result_sha256", "Round294 result")
    verify_self_digest(result_a, "result_sha256", "Round295-A result")
    verify_self_digest(result_b, "result_sha256", "Round295-B result")
    verify_self_digest(
        verification294, "verification_sha256", "Round294 verification"
    )
    verify_self_digest(
        verification_a, "verification_sha256", "Round295-A verification"
    )
    verify_self_digest(
        verification_b, "verification_sha256", "Round295-B verification"
    )
    need(
        result294["census"]["formal_occurrence_registry_row_count"]
        == 431_208
        and result294["census"]["formal_representation_binding_count"]
        == 46_288
        and result_a["formal_credit_transition"][
            "formal_representation_binding_count_after"
        ] == 46_564
        and result_a["atomic_R291_binding_census"][
            "formal_unresolved_physical_witness_count"
        ] == 0
        and result_b["corrected_relation_census"][
            "remaining_R289_terminal_face_frontier_count"
        ] == 0
        and result_b["strict_nonpromotion"][
            "true_seam_directed_endpoint_cell_count"
        ] == 152
        and result_b["strict_nonpromotion"][
            "formal_true_seam_edge_count"
        ] == 0
        and verification294["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        )
        and verification_a["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        )
        and verification_b["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295B"
        ),
        "sealed package semantics",
    )
    return result294, result_a, result_b


def build(producer_sha256: str) -> tuple[dict[str, Any], dict[str, Any]]:
    result294, result_a, result_b = validate_packages()

    aliases_doc = read_gzip_json(A_ALIASES)
    alias_rows, alias_commitment = validate_nested_table(
        aliases_doc,
        "Round295A_retained_continuation_alias_row_id",
        276,
        "Round295-A aliases",
    )

    physical_a_doc = read_gzip_json(A_PHYSICAL)
    physical_a_rows, physical_a_commitment = validate_nested_table(
        physical_a_doc,
        "Round295A_R291_physical_incidence_binding_row_id",
        113_452,
        "Round295-A physical incidence",
    )
    physical_a_reference_count = sum(
        row["target_Round294_registry_reference_count"]
        for row in physical_a_rows
    )
    physical_a_target_count_histogram = Counter(
        row["target_Round294_registry_reference_count"]
        for row in physical_a_rows
    )
    need(
        physical_a_reference_count == 225_304
        and physical_a_target_count_histogram == {1: 1_600, 2: 111_852}
        and all(
            row["formal_occurrence_ID_issued"] is False
            for row in physical_a_rows
        ),
        "Round295-A physical census",
    )
    del physical_a_rows, physical_a_doc

    absence_a_doc = read_gzip_json(A_ABSENCE)
    absence_a_rows, absence_a_commitment = validate_nested_table(
        absence_a_doc,
        "Round295A_R291_absence_no_binding_row_id",
        28_016,
        "Round295-A absence",
    )
    need(
        all(
            row["target_Round294_registry_reference_count"] == 0
            for row in absence_a_rows
        ),
        "Round295-A absence zero targets",
    )
    del absence_a_rows, absence_a_doc

    b = read_gzip_json(B_LEDGER)
    relation_rows_b, relation_commitment_b = validate_nested_table(
        b["corrected_relation_disposition_ledger"],
        "Round295B_corrected_relation_disposition_row_id",
        9_528,
        "Round295-B relations",
    )
    physical_rows_b, physical_commitment_b = validate_nested_table(
        b["physical_incidence_binding_ledger"],
        "Round295B_physical_incidence_binding_row_id",
        11_448,
        "Round295-B physical",
    )
    wrong_rows_b, wrong_commitment_b = validate_nested_table(
        b["wrong_signed_empty_no_binding_ledger"],
        "Round295B_wrong_signed_empty_no_binding_row_id",
        468,
        "Round295-B wrong-sign",
    )
    graph_rows_b, graph_commitment_b = validate_nested_table(
        b["graph_separated_no_binding_ledger"],
        "Round295B_graph_separated_no_binding_row_id",
        288,
        "Round295-B graph",
    )

    raw_target_by_physical_id = {
        row["Round295B_physical_incidence_binding_row_id"]:
            row["formal_Round294_occurrence_id"]
        for row in physical_rows_b
    }
    raw_target_set = set(raw_target_by_physical_id.values())
    need(len(raw_target_set) == 3_780, "Round295-B raw target unique census")

    registry_ids: set[str] = set()
    source_matches: dict[str, list[str]] = {}
    registry_target_rows: dict[str, dict[str, Any]] = {}
    registry_occurrences = ListCommitment()
    registry_row_ids = ListCommitment()
    registry_hashes = ListCommitment()
    registry_rows = ListCommitment()

    def visit_registry(row: dict[str, Any]) -> None:
        validate_row_hash(row, "Round294 registry")
        occurrence_id = row["registry_occurrence_id"]
        source_id = row["source_row_id"]
        need(occurrence_id not in registry_ids, "unique registry occurrence")
        registry_ids.add(occurrence_id)
        registry_occurrences.add(occurrence_id)
        registry_row_ids.add(row["Round294_occurrence_registry_row_id"])
        registry_hashes.add(row["row_sha256"])
        registry_rows.add(row)
        if occurrence_id in raw_target_set or source_id in raw_target_set:
            registry_target_rows[occurrence_id] = {
                "registry_occurrence_id": occurrence_id,
                "Round294_occurrence_registry_row_id":
                    row["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    row["row_sha256"],
                "registry_entry_kind": row["registry_entry_kind"],
                "source_occurrence_class": row["source_occurrence_class"],
                "source_row_id": source_id,
            }
        if source_id in raw_target_set:
            source_matches.setdefault(source_id, []).append(occurrence_id)

    registry_metadata = scan_large_gzip_ledger(
        R294_REGISTRY, visit_registry
    )
    registry_summary = result294["registry_ledger"]
    registry_commitment = {
        "row_count": registry_metadata["streamed_row_count"],
        "occurrence_ids_sha256": registry_occurrences.finish(),
        "row_ids_sha256": registry_row_ids.finish(),
        "row_hashes_sha256": registry_hashes.finish(),
        "rows_sha256": registry_rows.finish(),
    }
    need(
        registry_metadata["streamed_row_count"]
        == registry_metadata["row_count"] == 431_208
        and all(
            registry_commitment[key] == registry_summary[key]
            for key in registry_commitment
        ),
        "complete Round294 registry commitment",
    )

    canonical_raw = raw_target_set & registry_ids
    source_raw = raw_target_set - registry_ids
    need(
        len(canonical_raw) == 356
        and len(source_raw) == 3_424
        and set(source_matches) == source_raw
        and all(len(source_matches[value]) == 1 for value in source_raw),
        "unique Round294 source-row normalization map",
    )
    normalized_by_raw = {
        raw: (
            raw if raw in canonical_raw else source_matches[raw][0]
        )
        for raw in raw_target_set
    }
    converted_target_set = {
        normalized_by_raw[raw] for raw in source_raw
    }
    already_target_set = set(canonical_raw)
    normalized_target_set = converted_target_set | already_target_set
    need(
        len(converted_target_set) == 3_424
        and len(already_target_set) == 356
        and not (converted_target_set & already_target_set)
        and len(normalized_target_set) == 3_780
        and normalized_target_set <= registry_ids
        and normalized_target_set <= set(registry_target_rows),
        "normalized Round295-B target set closure",
    )

    normalized_target_by_physical_id = {
        row_id: normalized_by_raw[raw]
        for row_id, raw in raw_target_by_physical_id.items()
    }
    converted_row_count = sum(
        raw not in canonical_raw
        for raw in raw_target_by_physical_id.values()
    )
    already_row_count = len(physical_rows_b) - converted_row_count
    normalized_use_count = Counter(
        normalized_target_by_physical_id.values()
    )
    multiplicity_histogram = Counter(normalized_use_count.values())
    target_prefix_histogram = Counter(
        target.split(":", 1)[0] for target in normalized_target_set
    )
    need(
        converted_row_count == 5_292
        and already_row_count == 6_156
        and multiplicity_histogram
        == EXPECTED_TARGET_MULTIPLICITY_HISTOGRAM,
        "normalized Round295-B target multiplicity census",
    )
    need(
        target_prefix_histogram
        == {
            "source-g-expanded-occurrence": 3_728,
            "round182-collar-leaf": 32,
            "round179-resolved-child": 20,
        },
        "normalized Round295-B target prefix census",
    )

    # Recommit all 46,288 Round294 binding rows and the 276 Round295-A
    # continuation aliases as one ordered 46,564-row representation scope.
    binding_ids = ListCommitment()
    binding_hashes = ListCommitment()
    binding_rows = ListCommitment()
    composite_ids = ListCommitment()
    composite_hashes = ListCommitment()
    composite_rows = ListCommitment()

    def visit_binding(row: dict[str, Any]) -> None:
        validate_row_hash(row, "Round294 representation binding")
        row_id = row[
            "Round294_occurrence_representation_binding_row_id"
        ]
        binding_ids.add(row_id)
        binding_hashes.add(row["row_sha256"])
        binding_rows.add(row)
        composite_ids.add(row_id)
        composite_hashes.add(row["row_sha256"])
        composite_rows.add(row)

    binding_metadata = scan_large_gzip_ledger(
        R294_BINDINGS, visit_binding
    )
    prior_binding_summary = result294["representation_binding_ledger"]
    need(
        binding_metadata["streamed_row_count"]
        == binding_metadata["row_count"] == 46_288
        and binding_ids.finish()
        == prior_binding_summary["row_ids_sha256"]
        and binding_hashes.finish()
        == prior_binding_summary["row_hashes_sha256"]
        and binding_rows.finish()
        == prior_binding_summary["rows_sha256"],
        "complete Round294 binding commitment",
    )
    for row in alias_rows:
        composite_ids.add(
            row["Round295A_retained_continuation_alias_row_id"]
        )
        composite_hashes.add(row["row_sha256"])
        composite_rows.add(row)
    representation_commitment = {
        "row_count": 46_564,
        "row_ids_sha256": composite_ids.finish(),
        "row_hashes_sha256": composite_hashes.finish(),
        "rows_sha256": composite_rows.finish(),
    }

    physical_by_id = {
        row["Round295B_physical_incidence_binding_row_id"]: row
        for row in physical_rows_b
    }
    wrong_by_id = {
        row["Round295B_wrong_signed_empty_no_binding_row_id"]: row
        for row in wrong_rows_b
    }
    graph_by_id = {
        row["Round295B_graph_separated_no_binding_row_id"]: row
        for row in graph_rows_b
    }
    need(
        len(physical_by_id) == 11_448
        and len(wrong_by_id) == 468
        and len(graph_by_id) == 288,
        "unique Round295-B child IDs",
    )

    canonical_relation_rows: list[dict[str, Any]] = []
    covered_physical: set[str] = set()
    covered_wrong: set[str] = set()
    covered_graph: set[str] = set()
    disposition_histogram: Counter[str] = Counter()
    assignment_pairs: list[list[str]] = []
    covered_patch_ids: set[str] = set()
    covered_patch_sides: set[tuple[str, int]] = set()

    for source in sorted(
        relation_rows_b,
        key=lambda row: row["Round289_region_cell_relation_id"],
    ):
        relation_id = source["Round289_region_cell_relation_id"]
        covered_patch_ids.add(source["Round268_true_seam_patch_row_id"])
        covered_patch_sides.add((
            source["Round268_true_seam_patch_row_id"],
            source["side_index"],
        ))
        physical_ids = source["physical_row_ids"]
        wrong_ids = source["wrong_signed_empty_no_binding_row_ids"]
        graph_ids = source["graph_no_binding_proof_ids"]
        need(
            len(physical_ids)
            == source["physical_incidence_binding_row_count"]
            and len(wrong_ids)
            == source["wrong_signed_empty_no_binding_row_count"]
            and len(graph_ids)
            == source["graph_separated_no_binding_row_count"]
            and len(physical_ids) == len(set(physical_ids))
            and len(wrong_ids) == len(set(wrong_ids))
            and len(graph_ids) == len(set(graph_ids))
            and set(physical_ids) <= set(physical_by_id)
            and set(wrong_ids) <= set(wrong_by_id)
            and set(graph_ids) <= set(graph_by_id),
            f"relation child list closure:{relation_id}",
        )

        physical_children = []
        physical_area = Q(0)
        for child_id in physical_ids:
            child = physical_by_id[child_id]
            need(
                child["Round289_region_cell_relation_id"] == relation_id
                and child_id not in covered_physical,
                f"physical child ownership:{child_id}",
            )
            covered_physical.add(child_id)
            area = rectangle_area(child["exact_physical_ps_subcell"])
            need(
                area == Q(child["exact_physical_ps_area"]),
                f"physical child exact area:{child_id}",
            )
            physical_area += area
            raw_target = child["formal_Round294_occurrence_id"]
            canonical_target = normalized_by_raw[raw_target]
            assignment_pairs.append([child_id, canonical_target])
            target = registry_target_rows[canonical_target]
            physical_children.append({
                "source_Round295B_physical_incidence_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "source_field_formal_Round294_occurrence_id":
                    raw_target,
                "target_normalization_classification": (
                    "CONVERTED_FROM_ROUND294_SOURCE_ROW_ID"
                    if raw_target in source_raw
                    else "ALREADY_CANONICAL_ROUND294_REGISTRY_OCCURRENCE_ID"
                ),
                "canonical_Round294_registry_occurrence_id":
                    canonical_target,
                "Round294_occurrence_registry_row_id":
                    target["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    target["Round294_occurrence_registry_row_sha256"],
                "Round294_registry_entry_kind":
                    target["registry_entry_kind"],
                "exact_physical_ps_subcell":
                    child["exact_physical_ps_subcell"],
                "exact_physical_ps_area":
                    child["exact_physical_ps_area"],
            })

        wrong_children = []
        wrong_area = Q(0)
        for child_id in wrong_ids:
            child = wrong_by_id[child_id]
            need(
                child["Round289_region_cell_relation_id"] == relation_id
                and child_id not in covered_wrong
                and child["terminal_registry_target_reference_count"] == 0,
                f"wrong-sign child ownership:{child_id}",
            )
            covered_wrong.add(child_id)
            area = rectangle_area(
                child["exact_empty_intersection_ps_rectangle"]
            )
            need(
                area == Q(child["exact_empty_intersection_ps_area"]),
                f"wrong-sign child exact area:{child_id}",
            )
            wrong_area += area
            wrong_children.append({
                "source_Round295B_wrong_signed_empty_no_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "exact_empty_intersection_ps_rectangle":
                    child["exact_empty_intersection_ps_rectangle"],
                "exact_empty_intersection_ps_area":
                    child["exact_empty_intersection_ps_area"],
                "no_binding_classification":
                    child["no_binding_classification"],
            })

        graph_children = []
        graph_area = Q(0)
        for child_id in graph_ids:
            child = graph_by_id[child_id]
            need(
                child["Round289_region_cell_relation_id"] == relation_id
                and child_id not in covered_graph
                and child["terminal_registry_target_reference_count"] == 0,
                f"graph child ownership:{child_id}",
            )
            covered_graph.add(child_id)
            area = rectangle_area(child["exact_relation_ps_rectangle"])
            need(
                area == Q(child["exact_relation_ps_area"]),
                f"graph child exact area:{child_id}",
            )
            graph_area += area
            graph_children.append({
                "source_Round295B_graph_separated_no_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "exact_graph_separated_ps_rectangle":
                    child["exact_relation_ps_rectangle"],
                "exact_graph_separated_ps_area":
                    child["exact_relation_ps_area"],
                "no_binding_classification":
                    child["no_binding_classification"],
            })

        relation_area = rectangle_area(source["exact_relation_ps_rectangle"])
        need(
            relation_area == Q(source["exact_relation_ps_area"])
            and physical_area == Q(source["exact_physical_ps_area"])
            and wrong_area == Q(source["exact_wrong_signed_empty_ps_area"])
            and graph_area == Q(source["exact_graph_separated_ps_area"])
            and relation_area
            == physical_area + wrong_area + graph_area
            and source["exact_terminal_face_area_conserved"] is True
            and source["remaining_terminal_face_frontier_cell_count"] == 0
            and source["remaining_terminal_face_frontier_ps_area"] == "0",
            f"per-relation exact area conservation:{relation_id}",
        )

        disposition = source["corrected_relation_disposition"]
        disposition_histogram[disposition] += 1
        payload = {
            "source_Round295B_corrected_relation_disposition_row_id":
                source["Round295B_corrected_relation_disposition_row_id"],
            "source_Round295B_row_sha256": source["row_sha256"],
            "Round289_region_cell_relation_id": relation_id,
            "Round268_true_seam_patch_row_id":
                source["Round268_true_seam_patch_row_id"],
            "Round275_region_id": source["Round275_region_id"],
            "side_index": source["side_index"],
            "source_relation_classification":
                source["source_relation_classification"],
            "canonical_relation_disposition": disposition,
            "exact_relation_ps_rectangle":
                source["exact_relation_ps_rectangle"],
            "exact_relation_ps_area": qstr(relation_area),
            "exact_physical_ps_area": qstr(physical_area),
            "exact_wrong_signed_empty_ps_area": qstr(wrong_area),
            "exact_graph_separated_ps_area": qstr(graph_area),
            "physical_children": physical_children,
            "wrong_signed_empty_children": wrong_children,
            "graph_separated_children": graph_children,
            "physical_child_count": len(physical_children),
            "wrong_signed_empty_child_count": len(wrong_children),
            "graph_separated_child_count": len(graph_children),
            "canonical_Round294_target_reference_count":
                len(physical_children),
            "canonical_Round294_target_occurrence_ids": [
                child["canonical_Round294_registry_occurrence_id"]
                for child in physical_children
            ],
            "per_relation_child_lists_complete": True,
            "per_relation_exact_ps_area_conserved": True,
            "remaining_relation_scope_frontier_count": 0,
            "formal_existing_occurrence_physical_incidence_binding_credit":
                len(physical_children),
            **{field: 0 for field in ZERO_FIELDS},
        }
        canonical_relation_rows.append(close_row(
            "round295c-canonical-r289-relation:",
            "ROUND295C_CANONICAL_R289_RELATION_V1",
            "Round295C_canonical_R289_relation_disposition_row_id",
            payload,
        ))

    canonical_relation_rows.sort(
        key=lambda row: row[
            "Round295C_canonical_R289_relation_disposition_row_id"
        ]
    )
    need(
        covered_physical == set(physical_by_id)
        and covered_wrong == set(wrong_by_id)
        and covered_graph == set(graph_by_id)
        and len(covered_patch_ids) == 24
        and len(covered_patch_sides) == 40
        and len(assignment_pairs) == 11_448
        and disposition_histogram == {
            "WHOLE_PHYSICAL_EXISTING_OCCURRENCE_INCIDENCE": 8_844,
            "MIXED_PHYSICAL_EXISTING_OCCURRENCE_AND_WRONG_SIGNED_EMPTY_"
            "ABSENCE": 392,
            "WHOLE_WRONG_SIGNED_EMPTY_ABSENCE__NO_BINDING": 4,
            "GRAPH_SEPARATED_ABSENCE__NO_BINDING": 288,
        },
        "complete canonical relation/child partition",
    )
    relation_commitment_c = commitment_for_rows(
        canonical_relation_rows,
        "Round295C_canonical_R289_relation_disposition_row_id",
    )
    assignment_pairs.sort()

    def inventory_row(slot: int, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        return close_row(
            "round295c-all-stratum-inventory:",
            "ROUND295C_ALL_STRATUM_SCOPE_INVENTORY_V1",
            "Round295C_all_stratum_scope_inventory_row_id",
            {
                "scope_slot": slot,
                "scope_table_name": name,
                **payload,
                "unresolved_scope_row_count": 0,
                **{field: 0 for field in ZERO_FIELDS},
            },
        )

    inventory_rows = [
        inventory_row(1, "ROUND294_OCCURRENCE_REGISTRY", {
            **registry_commitment,
            "channel_provenance": "SEALED_ROUND294_OCCURRENCE_IDENTITY",
            "source_artifact": R294_REGISTRY,
            "formal_target_reference_count": 0,
        }),
        inventory_row(2, "COMPOSED_REPRESENTATION_BINDINGS_AND_ALIASES", {
            **representation_commitment,
            "channel_provenance":
                "ROUND294_46288_BINDINGS_PLUS_ROUND295A_276_ALIASES",
            "source_artifacts": [R294_BINDINGS, A_ALIASES],
            "formal_prior_representation_binding_count": 46_288,
            "formal_Round295A_alias_delta": 276,
            "formal_target_reference_count": 0,
        }),
        inventory_row(3, "ROUND291_PHYSICAL_INCIDENCE", {
            **physical_a_commitment,
            "channel_provenance":
                "ROUND295A_COMPLETE_R291_PHYSICAL_INCIDENCE",
            "source_artifact": A_PHYSICAL,
            "formal_target_reference_count": 225_304,
            "unique_target_witness_row_count": 1_600,
            "multi_target_witness_row_count": 111_852,
        }),
        inventory_row(4, "ROUND291_ABSENCE_NO_BINDING", {
            **absence_a_commitment,
            "channel_provenance":
                "ROUND295A_COMPLETE_R291_ABSENCE_EVIDENCE",
            "source_artifact": A_ABSENCE,
            "formal_target_reference_count": 0,
        }),
        inventory_row(5, "CANONICAL_ROUND289_RELATIONS", {
            **relation_commitment_c,
            "source_Round295B_row_ids_sha256":
                relation_commitment_b["row_ids_sha256"],
            "source_Round295B_row_hashes_sha256":
                relation_commitment_b["row_hashes_sha256"],
            "source_Round295B_rows_sha256":
                relation_commitment_b["rows_sha256"],
            "channel_provenance":
                "ROUND295C_CANONICAL_RELATION_COMPOSITION",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 11_448,
        }),
        inventory_row(6, "NORMALIZED_ROUND289_PHYSICAL_INCIDENCE", {
            **physical_commitment_b,
            "channel_provenance":
                "ROUND295B_PHYSICAL_WITH_ROUND295C_CANONICAL_TARGETS",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 11_448,
            "canonical_target_assignments_sha256":
                digest(assignment_pairs),
            "canonical_unique_target_ids_sha256":
                digest(sorted(normalized_target_set)),
            "canonical_unique_target_count": 3_780,
        }),
        inventory_row(7, "ROUND289_WRONG_SIGNED_ABSENCE", {
            **wrong_commitment_b,
            "channel_provenance":
                "ROUND295B_WRONG_SIGNED_EMPTY_NO_BINDING_EVIDENCE",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 0,
        }),
        inventory_row(8, "ROUND289_GRAPH_SEPARATED_ABSENCE", {
            **graph_commitment_b,
            "channel_provenance":
                "ROUND295B_GRAPH_SEPARATED_NO_BINDING_EVIDENCE",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 0,
        }),
    ]
    inventory_rows.sort(key=lambda row: row["scope_slot"])
    inventory_commitment = commitment_for_rows(
        inventory_rows,
        "Round295C_all_stratum_scope_inventory_row_id",
    )
    need(
        len(inventory_rows) == 8
        and [row["row_count"] for row in inventory_rows]
        == [431_208, 46_564, 113_452, 28_016, 9_528, 11_448, 468, 288],
        "eight-row all-stratum inventory census",
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "PASS_ROUND295C_CANONICAL_R289_RELATIONS_AND_ALL_STRATUM_"
            "SCOPE_INVENTORY__9528_RELATIONS__8_INVENTORY_ROWS__"
            "ALL_TARGETS_CANONICAL_ROUND294_IDS__UNRESOLVED_SCOPE_ZERO",
        "canonical_R289_relation_disposition_ledger": {
            **relation_commitment_c,
            "rows": canonical_relation_rows,
        },
        "all_stratum_scope_inventory_ledger": {
            **inventory_commitment,
            "rows": inventory_rows,
        },
    }

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND295C_ALL_STRATUM_SCOPE_COMPOSITION_CLOSURE__"
            "R291_576_TO_ZERO__R289_396_TO_ZERO__"
            "NORMALIZED_R289_TARGETS_3780__UNRESOLVED_SCOPE_ZERO__"
            "NO_SEAM_COMPONENT_OR_DSU_PROMOTION",
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "sealed_package_consumption": {
            "Round294_registry_row_count": 431_208,
            "Round294_representation_binding_count": 46_288,
            "Round295A_alias_delta": 276,
            "post_Round295A_representation_binding_count": 46_564,
            "Round295A_manifest_sha256": INPUT_PINS[A_MANIFEST],
            "Round295B_manifest_sha256": INPUT_PINS[B_MANIFEST],
            "complete_Round294_registry_streamed_and_recommitted": True,
            "complete_Round294_binding_ledger_streamed_and_recommitted":
                True,
        },
        "Round289_target_normalization": {
            "physical_row_count": 11_448,
            "converted_from_Round294_source_row_id_count": 5_292,
            "converted_unique_source_row_id_count": 3_424,
            "already_canonical_registry_occurrence_id_count": 6_156,
            "already_canonical_unique_target_count": 356,
            "converted_and_already_canonical_target_set_overlap_count": 0,
            "canonical_unique_Round294_target_count": 3_780,
            "all_canonical_targets_present_in_complete_Round294_registry":
                True,
            "canonical_target_prefix_histogram": {
                key: value
                for key, value in sorted(target_prefix_histogram.items())
            },
            "canonical_target_use_multiplicity_histogram": {
                str(key): value
                for key, value
                in sorted(multiplicity_histogram.items())
            },
            "misnamed_source_field_copied_as_occurrence_ID": False,
            "normalization_source":
                "INDEPENDENT_COMPLETE_ROUND294_SOURCE_ROW_TO_"
                "REGISTRY_OCCURRENCE_ID_MAP",
            "number_5784_belongs_only_to":
                "ROUND296_COMBINED_STRICT_PLUS_B_SEAM_ENDPOINT_UNIVERSE",
            "number_5784_used_as_Round295C_B_target_count": False,
        },
        "canonical_R289_relation_census": {
            "relation_count": 9_528,
            "physical_relation_count": 9_236,
            "whole_physical_relation_count": 8_844,
            "mixed_physical_and_empty_relation_count": 392,
            "absent_relation_count": 292,
            "whole_wrong_signed_empty_relation_count": 4,
            "graph_separated_absent_relation_count": 288,
            "physical_child_count": 11_448,
            "wrong_signed_empty_child_count": 468,
            "graph_separated_child_count": 288,
            "all_child_IDs_covered_exactly_once": True,
            "all_relations_exact_ps_area_conserved": True,
            "remaining_R289_relation_scope_frontier_count": 0,
        },
        "all_stratum_scope_census": {
            "inventory_row_count": 8,
            "formal_occurrence_registry_row_count": 431_208,
            "formal_representation_binding_and_alias_count": 46_564,
            "Round291_physical_incidence_row_count": 113_452,
            "Round291_target_reference_count": 225_304,
            "Round291_absence_no_binding_row_count": 28_016,
            "Round289_relation_row_count": 9_528,
            "Round289_physical_incidence_row_count": 11_448,
            "Round289_wrong_signed_no_binding_row_count": 468,
            "Round289_graph_no_binding_row_count": 288,
            "formal_physical_incidence_channel_total": 124_900,
            "formal_no_binding_evidence_channel_total": 28_772,
            "physical_channels_merged_as_identity_aliases": False,
            "no_binding_channels_merged_as_occurrences": False,
            "Round291_gap_before": 576,
            "Round291_gap_after": 0,
            "Round289_gap_before": 396,
            "Round289_gap_after": 0,
            "unresolved_all_stratum_scope_count": 0,
        },
        "strict_nonpromotion": {
            "formal_registry_delta": 0,
            "formal_alias_delta_from_Round294": 276,
            "formal_new_occurrence_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "distinct_Round268_true_seam_patch_IDs_in_relation_scope": 24,
            "distinct_Round268_patch_side_pairs_in_relation_scope": 40,
            "true_seam_directed_endpoint_cell_relation_scope_count": 152,
            "directed_endpoint_cell_count_source":
                "SEALED_ROUND295B_RESULT_STRICT_NONPROMOTION",
            "directed_endpoint_cells_are_seam_edges": False,
            "all_152_true_seam_patch_edge_pairing_status":
                "DEFERRED_TO_INDEPENDENT_ROUND296",
            "true_seam_endpoint_pairing_status":
                "DEFERRED_TO_INDEPENDENT_ROUND296",
            "post_Round294_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "post_Round295C_quotient_component_count": None,
            "legacy_pre_Round294_quotient_component_count": 63_224,
            "legacy_count_is_current_post_Round294_quotient": False,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledger": {
            "filename": LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "canonical_R289_relation_row_count": 9_528,
            "canonical_R289_relation_rows_sha256":
                relation_commitment_c["rows_sha256"],
            "all_stratum_scope_inventory_row_count": 8,
            "all_stratum_scope_inventory_rows_sha256":
                inventory_commitment["rows_sha256"],
        },
        "required_next": [
            "Independently verify the complete Round295-C composition and "
            "target normalization before consuming it.",
            "Pair all 152 true-seam patches/edges only in the independent "
            "Round296 seam-edge closure; do not reinterpret the separate "
            "Round295-B 152 directed endpoint-cell census as edges.",
            "Build the expanded all-stratum component/DSU edge ledger only "
            "after the seam pairing is sealed.",
        ],
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "Round295A_or_Round295B_producer_imported_or_executed": False,
            "Round296_input_used": False,
        },
    }
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--seed", default="295301")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    producer_sha256 = file_sha256(Path(__file__).resolve())
    ledger, result = build(producer_sha256)
    ledger_bytes = deterministic_gzip(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(
        ledger_bytes
    ).hexdigest()
    result["seed_affects_output"] = False
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    if not arguments.no_write:
        safe_write(arguments.ledger, ledger_bytes)
        safe_write(arguments.result, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "ledger_file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "target_normalization": result["Round289_target_normalization"],
        "all_stratum_scope_census": result["all_stratum_scope_census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
