#!/usr/bin/env python3
"""Independent cacheless verifier for the Round296 true-seam edge ledger.

This verifier never imports or executes the Round296 producer.  It opens the
eight byte-pinned input packages, independently rebuilds the exact half-open
p-s refinement, formal endpoint atoms, edge ledger, and cell ledger, and only
then compares the three candidate artifacts.
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
import re
import stat
import tempfile
from typing import Any, Callable, Iterable
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure"
PRODUCER = HERE / f"{PREFIX}.py"
EDGE = HERE / f"{PREFIX}_edge_ledger.json.gz"
CELL = HERE / f"{PREFIX}_cell_coverage_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"

SCHEMA = "cm2.round296.source-g-true-seam-occurrence-edge-ledger-closure.v1"
EDGE_SCHEMA = "cm2.round296.source-g-true-seam-occurrence-edge-ledger.v1"
CELL_SCHEMA = (
    "cm2.round296.source-g-true-seam-exact-cell-coverage-ledger.v1"
)
PRODUCER_SHA256 = (
    "7a9771e0896550f597cfd472dafb1a378b33a3e2a02e83414d79cc29962cb843"
)
MAX_FILE_BYTES = 1_100_000_000
MAX_GZIP_BYTES = 2_000_000_000

MANIFEST_PINS = {
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256":
        "d2d4c0c34cc25dd92626a656e3a08abb031190f168f4acfe11cd451d886a538f",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_manifest.sha256":
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_manifest.sha256":
        "c93d7982b036126ea4fcae761316d86863051d19c9fa9a3008b82ef9c6d44081",
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_manifest.sha256":
        "260065c2a0253516ebda73ba68db8bd76cd3d6e68fade0535d81b77e1471b952",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_manifest.sha256":
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    "cm2_round289_source_g_outgoing_seam_tail_child_materialization_manifest.sha256":
        "4786efc0d7f0f060de0702e324176a8e6ea0634288cc71d78c86d7913640036d",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_manifest.sha256":
        "09cec800efc3c7dd21bebab4a226d384f51ec1273040c548bfa54834a25c8331",
}

R268_CERT = (
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_"
    "certificate.json"
)
R275_CERT = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R282_LEDGER = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "ledger.json.gz"
)
R285_LEDGER = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "ledger.json.gz"
)
R287_LEDGER = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "ledger.json.gz"
)
R289_LEDGER = (
    "cm2_round289_source_g_outgoing_seam_tail_child_materialization_"
    "ledger.json.gz"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "representation_binding_ledger.json.gz"
)
R295B_LEDGER = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_ledger.json.gz"
)
R295B_RESULT = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_result.json"
)

EXPECTED_PREVIEW = {
    "exact_cell_count": 3_444,
    "full_patch_exact_cell_count": 148,
    "tail_patch_exact_cell_count": 3_296,
    "formal_true_seam_edge_count": 48_444,
    "full_patch_edge_count": 504,
    "tail_patch_edge_count": 47_940,
    "distinct_unordered_endpoint_pair_count": 15_316,
    "distinct_occurrence_target_count": 5_784,
    "self_edge_count": 0,
    "common_payload_count_per_cell_histogram": {"1": 2_880, "2": 564},
    "tail_patch_cell_count_histogram": {"8": 8, "104": 8, "300": 8},
}
ZERO_FIELDS = (
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


class VerificationError(RuntimeError):
    """Fail-closed verifier error."""


def ensure(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
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
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(piece)
    return state.hexdigest()


def safe_regular(path: Path, cap: int = MAX_FILE_BYTES) -> None:
    ensure(path.parent.resolve() == HERE.resolve(), f"HERE-only path:{path}")
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationError(f"missing file:{path}") from error
    ensure(
        stat.S_ISREG(metadata.st_mode)
        and not path.is_symlink()
        and metadata.st_nlink == 1
        and 0 < metadata.st_size <= cap,
        f"safe regular single-link bounded file:{path}",
    )


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        ensure(key not in output, f"duplicate JSON key:{key}")
        output[key] = value
    return output


def strict_integer(text: str) -> int:
    ensure(
        re.fullmatch(r"-?(?:0|[1-9][0-9]*)", text) is not None
        and len(text.lstrip("-")) <= 128,
        "strict bounded JSON integer",
    )
    return int(text)


def reject_float(text: str) -> Any:
    raise VerificationError(f"JSON float rejected:{text}")


def reject_constant(text: str) -> Any:
    raise VerificationError(f"nonfinite JSON number rejected:{text}")


def strict_json_bytes(payload: bytes) -> Any:
    try:
        return json.loads(
            payload,
            object_pairs_hook=unique_object,
            parse_int=strict_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("strict single JSON document") from error


def scan_gzip_bytes(payload: bytes, cap: int = MAX_GZIP_BYTES) -> bytes:
    decoder = zlib.decompressobj(wbits=31)
    try:
        output = decoder.decompress(payload, cap + 1)
        output += decoder.flush()
    except zlib.error as error:
        raise VerificationError("valid gzip member") from error
    ensure(
        decoder.eof
        and not decoder.unused_data
        and not decoder.unconsumed_tail
        and len(output) <= cap,
        "bounded single-member gzip without trailing bytes",
    )
    return output


def scan_gzip_file(path: Path, cap: int = MAX_GZIP_BYTES) -> None:
    safe_regular(path)
    decoder = zlib.decompressobj(wbits=31)
    total = 0
    with path.open("rb") as stream:
        while True:
            piece = stream.read(1024 * 1024)
            if not piece:
                break
            ensure(not decoder.eof, f"trailing gzip member:{path.name}")
            try:
                output = decoder.decompress(piece)
            except zlib.error as error:
                raise VerificationError(f"valid gzip:{path.name}") from error
            total += len(output)
            ensure(
                total <= cap and not decoder.unused_data,
                f"bounded single gzip member:{path.name}",
            )
    total += len(decoder.flush())
    ensure(
        decoder.eof and not decoder.unused_data and total <= cap,
        f"complete single gzip member:{path.name}",
    )


def read_json(path: Path, canonical_required: bool = False) -> dict[str, Any]:
    safe_regular(path)
    payload = path.read_bytes()
    value = strict_json_bytes(payload)
    ensure(isinstance(value, dict), f"JSON object:{path.name}")
    if canonical_required:
        ensure(payload == canonical(value), f"canonical JSON:{path.name}")
    return value


def read_gzip(path: Path) -> dict[str, Any]:
    scan_gzip_file(path)
    with gzip.open(path, "rb") as stream:
        try:
            value = json.load(
                stream,
                object_pairs_hook=unique_object,
                parse_int=strict_integer,
                parse_float=reject_float,
                parse_constant=reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise VerificationError(f"strict gzip JSON:{path.name}") from error
    ensure(isinstance(value, dict), f"gzip JSON object:{path.name}")
    return value


def parse_manifest(name: str) -> dict[str, str]:
    path = HERE / name
    safe_regular(path)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        ensure(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        ensure(filename not in entries, f"manifest duplicate:{name}")
        entries[filename] = sha256
    ensure(entries, f"nonempty manifest:{name}")
    return entries


def verify_packages() -> dict[str, dict[str, str]]:
    safe_regular(PRODUCER)
    ensure(
        file_sha256(PRODUCER) == PRODUCER_SHA256,
        "Round296 producer byte pin",
    )
    packages: dict[str, dict[str, str]] = {}
    for manifest, sha256 in sorted(MANIFEST_PINS.items()):
        safe_regular(HERE / manifest)
        ensure(file_sha256(HERE / manifest) == sha256, f"manifest pin:{manifest}")
        entries = parse_manifest(manifest)
        for filename, expected in entries.items():
            safe_regular(HERE / filename)
            ensure(
                file_sha256(HERE / filename) == expected,
                f"package member pin:{manifest}:{filename}",
            )
        packages[manifest] = entries
    return packages


def closed(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    expected = payload.pop("row_sha256", None)
    ensure(expected == digest(payload), f"closed row:{label}")


def table_rows(
    table: dict[str, Any], count: int, id_field: str, label: str
) -> list[dict[str, Any]]:
    rows = table.get("rows")
    ensure(
        table.get("row_count") == count
        and isinstance(rows, list)
        and len(rows) == count,
        f"table envelope:{label}",
    )
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    ensure(
        len(set(ids)) == count
        and table.get("row_ids_sha256") == digest(ids)
        and table.get("row_hashes_sha256") == digest(hashes)
        and table.get("rows_sha256") == digest(rows),
        f"table commitments:{label}",
    )
    for row in rows:
        closed(row, f"{label}:{row[id_field]}")
    return rows


def ps_box(values: list[str], label: str) -> tuple[Fraction, ...]:
    try:
        box = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationError(f"exact rational box:{label}") from error
    ensure(
        len(box) == 4 and box[0] < box[1] and box[2] < box[3],
        f"positive p-s box:{label}",
    )
    return box


def box_text(box: tuple[Fraction, ...]) -> list[str]:
    return [str(value) for value in box]


def overlap(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...] | None:
    value = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return value if value[0] < value[1] and value[2] < value[3] else None


def contains(
    outer: tuple[Fraction, ...], inner: tuple[Fraction, ...]
) -> bool:
    return (
        outer[0] <= inner[0] <= inner[1] <= outer[1]
        and outer[2] <= inner[2] <= inner[3] <= outer[3]
    )


def area(box: tuple[Fraction, ...]) -> Fraction:
    return (box[1] - box[0]) * (box[3] - box[2])


def payload_for(region: dict[str, Any]) -> dict[str, Any]:
    signature = region["local_return_signature"]
    value = {
        "target_chart": signature["target_chart"],
        "target_lift": signature["target_lift"],
        "outgoing_cell": signature["outgoing_cell"],
        "ordered_integer_wall_events":
            signature["ordered_integer_wall_events"],
        "roof": signature["roof"],
        "signed_wall_word": signature["signed_wall_word"],
    }
    ensure(
        list(value) == [
            "target_chart", "target_lift", "outgoing_cell",
            "ordered_integer_wall_events", "roof", "signed_wall_word",
        ],
        "complete six-field physical payload",
    )
    return value


def point_interval_distance(
    point: Fraction, lower: Fraction, upper: Fraction
) -> Fraction:
    if lower <= point <= upper:
        return Fraction(0)
    return min(abs(point - lower), abs(point - upper))


def make_ledger(
    rows: list[dict[str, Any]], schema: str, status: str, id_field: str
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    ensure(len(ids) == len(set(ids)), f"unique rebuilt IDs:{id_field}")
    return {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def reconstruct() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Rebuild both candidate ledgers directly from the frozen packages."""
    package_entries = verify_packages()

    r268_outer = read_json(HERE / R268_CERT)
    patches = table_rows(
        r268_outer["result"]["formal_true_source_seam_positive_patch_ledger"],
        152,
        "true_seam_patch_row_id",
        "R268 positive seam patches",
    )
    patches_by_id = {row["true_seam_patch_row_id"]: row for row in patches}

    r275_outer = read_json(HERE / R275_CERT)["result"]
    strict_regions = table_rows(
        r275_outer["strict_region_ledger"],
        5_288,
        "reverse_rechart_region_row_id",
        "R275 strict regions",
    )
    arrangement_regions = table_rows(
        r275_outer["arrangement_region_ledger"],
        8_500,
        "reverse_rechart_region_row_id",
        "R275 arrangement regions",
    )
    regions = {
        row["reverse_rechart_region_row_id"]: row
        for row in strict_regions + arrangement_regions
    }
    ensure(len(regions) == 13_788, "R275 region injectivity")

    r282_outer = read_gzip(HERE / R282_LEDGER)
    ensure(
        r282_outer.get("schema")
        == "cm2.round282.source-g-strict-true-seam-normal-corridor-probe."
        "v1.ledger",
        "R282 schema",
    )
    corridors = table_rows(
        r282_outer, 152, "Round282_seam_corridor_row_id", "R282 corridors"
    )
    corridors_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row for row in corridors
    }
    ensure(set(corridors_by_patch) == set(patches_by_id), "R282 exhaustion")

    r285_outer = read_gzip(HERE / R285_LEDGER)
    ensure(
        r285_outer.get("schema")
        == "cm2.round285.source-g-true-seam-safe-pairing-contract-probe."
        "v1.ledger",
        "R285 schema",
    )
    safe_rows = table_rows(
        r285_outer, 152, "Round285_safe_pairing_row_id", "R285 safe pairing"
    )
    safe_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row for row in safe_rows
    }
    ensure(set(safe_by_patch) == set(patches_by_id), "R285 exhaustion")
    safe_classes: Counter[str] = Counter()
    safe_class_areas: Counter[str] = Counter()
    for patch_id in sorted(patches_by_id):
        patch = patches_by_id[patch_id]
        probe = corridors_by_patch[patch_id]
        safe = safe_by_patch[patch_id]
        patch_box = ps_box([
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ], f"R268:{patch_id}")
        cells = [
            ps_box(
                row["exact_p_s_box"],
                f"R285:{patch_id}:{row['cell_index']}",
            )
            for row in safe["exact_cells"]
        ]
        for cell_row, cell_box in zip(safe["exact_cells"], cells):
            safe_classes[cell_row["classification"]] += 1
            safe_class_areas[cell_row["classification"]] += area(cell_box)
            expected_intersection = (
                cell_row["classification"]
                == "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED"
            )
            ensure(
                cell_row["classification"] in {
                    "GEOMETRIC_PAIR_PRESENT__"
                    "OCCURRENCE_IDENTITIES_UNISSUED",
                    "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED",
                }
                and cell_row[
                    "transported_physical_payload_intersection_nonempty"
                ] is expected_intersection
                and Fraction(cell_row["exact_positive_area"])
                == area(cell_box) > 0,
                f"R285 cell class semantics:{patch_id}",
            )
        ensure(
            patch["same_physical_source_point"] is True
            and patch["Round171_normal_position_velocity_identity"] is True
            and patch["owner_shadow_half_open_pair"] is True
            and safe["same_physical_source_point"] is True
            and safe["Round171_normal_position_velocity_identity"] is True
            and safe["transported_owner_target_sets_equal"] is True
            and safe["owner_shadow_half_open_pair"] is True
            and safe["cyclic_transition_identity"]
            == patch["cyclic_transition_identity"]
            and safe["Round282_geometry_classification"]
            == probe["classification"]
            and safe["exact_common_p_interval"]
            == patch["exact_common_p_interval"]
            and safe["exact_common_s_interval"]
            == patch["exact_common_s_interval"]
            and Fraction(safe["exact_positive_common_area"])
            == Fraction(patch["exact_positive_common_area"])
            == area(patch_box)
            and safe["exact_cell_count"] == len(cells)
            and all(contains(patch_box, cell) for cell in cells)
            and sum(map(area, cells), Fraction(0)) == area(patch_box)
            and all(
                overlap(left, right) is None
                for index, left in enumerate(cells)
                for right in cells[index + 1:]
            )
            and safe["left_Round182_source_seam_row_id"]
            == patch["left_Round182_source_seam_row_id"]
            and safe["right_Round182_source_seam_row_id"]
            == patch["right_Round182_source_seam_row_id"]
            and safe["left_chart"] == patch["left_chart"]
            and safe["right_chart"] == patch["right_chart"]
            and safe["left_local_t_root"] == patch["left_local_t_root"]
            and safe["right_local_t_root"] == patch["right_local_t_root"],
            f"R285 patch semantic contract:{patch_id}",
        )
    ensure(
        safe_classes == {
            "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED": 464,
            "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED": 876,
        }
        and safe_class_areas == {
            "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED":
                Fraction(1139, 102400),
            "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED":
                Fraction(141, 102400),
        },
        "R285 exhaustive cell class/area census",
    )

    r287_outer = read_gzip(HERE / R287_LEDGER)
    ensure(
        r287_outer.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition."
        "ledger.v1",
        "R287 schema",
    )
    r287_rows = r287_outer.get("region_rows")
    ensure(
        isinstance(r287_rows, list)
        and len(r287_rows) == 13_788
        and r287_outer.get("region_rows_sha256") == digest(r287_rows),
        "R287 region table",
    )
    r287_by_region = {
        row["Round275_region_id"]: row for row in r287_rows
    }
    ensure(len(r287_by_region) == 13_788, "R287 region injectivity")
    for row in r287_rows:
        closed(row, row["Round287_region_disposition_row_id"])

    r289_outer = read_gzip(HERE / R289_LEDGER)
    ensure(
        r289_outer.get("schema")
        == "cm2.round289.source-g-outgoing-seam-tail-child-materialization."
        "v1.ledger",
        "R289 schema",
    )
    relation_rows = table_rows(
        r289_outer["region_cell_relation_ledger"],
        9_528,
        "Round289_region_cell_relation_id",
        "R289 relations",
    )
    relations = {
        row["Round289_region_cell_relation_id"]: row
        for row in relation_rows
    }

    registry_outer = read_gzip(HERE / R294_REGISTRY)
    ensure(
        registry_outer.get("schema")
        == "cm2.round294.source-g-occurrence-registry-ledger.v1",
        "R294 registry schema",
    )
    registry_rows = table_rows(
        registry_outer,
        431_208,
        "Round294_occurrence_registry_row_id",
        "R294 registry",
    )
    formal_ids = {row["registry_occurrence_id"] for row in registry_rows}
    ensure(len(formal_ids) == 431_208, "R294 occurrence injectivity")
    source_to_occurrence: dict[str, str] = {}
    for row in registry_rows:
        reference = row["source_row_id"]
        ensure(
            reference not in source_to_occurrence,
            f"unique R294 source reference:{reference}",
        )
        source_to_occurrence[reference] = row["registry_occurrence_id"]

    bindings_outer = read_gzip(HERE / R294_BINDINGS)
    ensure(
        bindings_outer.get("schema")
        == "cm2.round294.source-g-occurrence-representation-binding-ledger.v1",
        "R294 binding schema",
    )
    binding_rows = table_rows(
        bindings_outer,
        46_288,
        "Round294_occurrence_representation_binding_row_id",
        "R294 representation bindings",
    )

    r295_result = read_json(HERE / R295B_RESULT)
    ensure(
        r295_result.get("status", "").startswith(
            "PASS_ROUND295B_R289_TERMINAL_FACE_ABSENCE_CLOSURE"
        )
        and r295_result["corrected_relation_census"][
            "remaining_R289_terminal_face_frontier_count"
        ] == 0,
        "R295B closure status",
    )
    r295_outer = read_gzip(HERE / R295B_LEDGER)
    ensure(
        r295_outer.get("schema")
        == "cm2.round295b.source-g-r289-terminal-face-absence-closure."
        "v1.ledger.v1",
        "R295B schema",
    )
    physical_rows = table_rows(
        r295_outer["physical_incidence_binding_ledger"],
        11_448,
        "Round295B_physical_incidence_binding_row_id",
        "R295B physical incidences",
    )
    wrong_rows = table_rows(
        r295_outer["wrong_signed_empty_no_binding_ledger"],
        468,
        "Round295B_wrong_signed_empty_no_binding_row_id",
        "R295B wrong-sign negatives",
    )
    graph_rows = table_rows(
        r295_outer["graph_separated_no_binding_ledger"],
        288,
        "Round295B_graph_separated_no_binding_row_id",
        "R295B graph-separated negatives",
    )

    region_representations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in registry_rows:
        if (
            row["registry_entry_kind"]
            != "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
        ):
            continue
        for member in row["member_refinement_cells"]:
            region_representations[row["Round275_region_id"]].append({
                "box": tuple(
                    Fraction(value)
                    for value in member["exact_transformed_open_cell"]
                ),
                "occurrence": row["registry_occurrence_id"],
                "kind": "ROUND294_REFINED_COMPONENT_MEMBER",
                "row_id": row["Round294_occurrence_registry_row_id"],
                "row_sha": row["row_sha256"],
                "subrow_id": member["Round292_refinement_cell_id"],
            })
    for row in binding_rows:
        kind = row["alias_source_kind"]
        if kind == "ROUND287_R275_REGION_INCLUSION_SUBCOVER":
            support: tuple[Fraction, ...] | None = None
        elif kind == "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER":
            support = tuple(
                Fraction(value)
                for value in row["exact_support_representation_box"]
            )
        elif kind == "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL":
            support = tuple(
                Fraction(value)
                for value in row["exact_transformed_open_cell"]
            )
        else:
            continue
        region_representations[row["Round275_region_id"]].append({
            "box": support,
            "occurrence": row["target_registry_occurrence_id"],
            "kind": kind,
            "row_id":
                row["Round294_occurrence_representation_binding_row_id"],
            "row_sha": row["row_sha256"],
            "subrow_id": row["source_representation_id"],
        })

    fragments: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    used_regions: set[str] = set()
    for patch_id in sorted(patches_by_id):
        patch = patches_by_id[patch_id]
        corridor_row = corridors_by_patch[patch_id]
        ensure(
            corridor_row["exact_common_p_interval"]
            == patch["exact_common_p_interval"]
            and corridor_row["exact_common_s_interval"]
            == patch["exact_common_s_interval"],
            f"R268/R282 geometry:{patch_id}",
        )
        for side in corridor_row["side_corridors"]:
            ensure(side["side"] in {"left", "right"}, f"R282 side:{patch_id}")
            side_index = 0 if side["side"] == "left" else 1
            for corridor_index, corridor in enumerate(
                side["accepted_strict_corridors"]
            ):
                region_id = corridor["Round275_region_id"]
                used_regions.add(region_id)
                region = regions[region_id]
                disposition = r287_by_region[region_id]
                ensure(
                    region["complete_10_field_return_signature_sha256"]
                    == corridor["complete_10_field_return_signature_sha256"]
                    == disposition[
                        "complete_10_field_return_signature_sha256"
                    ],
                    f"corridor signature:{region_id}",
                )
                representations = region_representations.get(region_id, [])
                ensure(representations, f"R294 region mapping:{region_id}")
                whole = [
                    value for value in representations
                    if value["box"] is None
                ]
                seam_t = Fraction(corridor["seam_dyadic_outer_endpoint"])
                seam_square = seam_t * seam_t
                if whole:
                    ensure(
                        len(whole) == len(representations) == 1,
                        f"unique whole mapping:{region_id}",
                    )
                    selected = whole
                    minimum_distance: Fraction | None = None
                else:
                    distances = [
                        point_interval_distance(
                            seam_square, value["box"][0], value["box"][1]
                        )
                        for value in representations
                    ]
                    minimum_distance = min(distances)
                    selected = [
                        value for value, distance
                        in zip(representations, distances)
                        if distance == minimum_distance
                    ]
                footprint = ps_box(
                    corridor["positive_ps_footprint"],
                    f"R282 corridor:{patch_id}:{side_index}:{corridor_index}",
                )
                for representation in selected:
                    mapped_ps = (
                        footprint
                        if representation["box"] is None
                        else representation["box"][2:]
                    )
                    exact_box = overlap(footprint, mapped_ps)
                    if exact_box is None:
                        continue
                    occurrence = representation["occurrence"]
                    ensure(occurrence in formal_ids, "strict formal endpoint")
                    physical = payload_for(region)
                    fragment_payload = {
                        "patch_id": patch_id,
                        "side_index": side_index,
                        "source_kind":
                            "ROUND282_STRICT_CORRIDOR_TERMINAL_SLICE",
                        "Round282_seam_corridor_row_id":
                            corridor_row["Round282_seam_corridor_row_id"],
                        "corridor_index": corridor_index,
                        "Round275_region_id": region_id,
                        "Round275_region_row_sha256": region["row_sha256"],
                        "seam_dyadic_endpoint":
                            corridor["seam_dyadic_outer_endpoint"],
                        "seam_dyadic_endpoint_t_square": str(seam_square),
                        "terminal_interval_selection_rule":
                            "EXACT_NEAREST_T2_INTERVAL_CLOSURE",
                        "minimum_terminal_interval_distance":
                            (
                                None if minimum_distance is None
                                else str(minimum_distance)
                            ),
                        "mapping_source_kind": representation["kind"],
                        "mapping_source_row_id": representation["row_id"],
                        "mapping_source_row_sha256":
                            representation["row_sha"],
                        "mapping_source_subrow_id":
                            representation["subrow_id"],
                        "mapping_t_square_interval":
                            (
                                None
                                if representation["box"] is None
                                else [
                                    str(representation["box"][0]),
                                    str(representation["box"][1]),
                                ]
                            ),
                        "exact_ps_box": box_text(exact_box),
                        "physical_payload_sha256": digest(physical),
                        "formal_occurrence_id": occurrence,
                    }
                    fragment_id = "round296-seam-fragment:" + digest([
                        "ROUND296_STRICT_TERMINAL_FRAGMENT_V1",
                        fragment_payload,
                    ])
                    fragments[(patch_id, side_index)].append({
                        **fragment_payload,
                        "fragment_id": fragment_id,
                        "box": exact_box,
                        "payload": physical,
                        "occurrence_id": occurrence,
                    })

    canonicalized_count = 0
    already_canonical_count = 0
    raw_noncanonical_sample: str | None = None
    for row in physical_rows:
        relation = relations[row["Round289_region_cell_relation_id"]]
        region_id = row["Round275_region_id"]
        region = regions[region_id]
        raw_reference = row["formal_Round294_occurrence_id"]
        if raw_reference in formal_ids:
            occurrence = raw_reference
            resolution = (
                "ALREADY_CANONICAL_ROUND294_REGISTRY_OCCURRENCE_ID"
            )
            already_canonical_count += 1
        else:
            if raw_noncanonical_sample is None:
                raw_noncanonical_sample = raw_reference
            occurrence = source_to_occurrence.get(raw_reference)
            ensure(
                occurrence is not None,
                f"R295B source-row canonicalization:{raw_reference}",
            )
            resolution = (
                "CANONICALIZED_ROUND294_SOURCE_ROW_ID_TO_REGISTRY_"
                "OCCURRENCE_ID"
            )
            canonicalized_count += 1
        ensure(
            relation["actual_seam_incidence"] is True
            and relation["Round268_true_seam_patch_row_id"]
            == row["Round268_true_seam_patch_row_id"]
            and relation["Round275_region_id"] == region_id
            and occurrence in formal_ids
            and row["binding_classification"]
            == "FORMAL_EXISTING_ROUND294_OCCURRENCE_PHYSICAL_TERMINAL_FACE_INCIDENCE"
            and row["formal_existing_physical_incidence_binding_credit"] == 1
            and row["formal_seam_edge_credit"] == 0,
            f"R295B physical row:{row['Round295B_physical_incidence_binding_row_id']}",
        )
        exact_box = ps_box(
            row["exact_physical_ps_subcell"],
            row["Round295B_physical_incidence_binding_row_id"],
        )
        physical = payload_for(region)
        fragment_payload = {
            "patch_id": row["Round268_true_seam_patch_row_id"],
            "side_index": row["side_index"],
            "source_kind": "ROUND295B_PHYSICAL_TERMINAL_FACE_INCIDENCE",
            "Round295B_physical_incidence_binding_row_id":
                row["Round295B_physical_incidence_binding_row_id"],
            "Round295B_row_sha256": row["row_sha256"],
            "Round289_region_cell_relation_id":
                row["Round289_region_cell_relation_id"],
            "Round289_relation_row_sha256": relation["row_sha256"],
            "Round275_region_id": region_id,
            "Round275_region_row_sha256": region["row_sha256"],
            "terminal_face_physical_t_square":
                row["terminal_face_physical_t_square"],
            "raw_Round295B_formal_Round294_occurrence_id_field":
                raw_reference,
            "Round294_target_reference_resolution": resolution,
            "exact_ps_box": box_text(exact_box),
            "physical_payload_sha256": digest(physical),
            "formal_occurrence_id": occurrence,
        }
        fragment_id = "round296-seam-fragment:" + digest([
            "ROUND296_R295B_PHYSICAL_FRAGMENT_V1", fragment_payload
        ])
        fragments[(
            row["Round268_true_seam_patch_row_id"], row["side_index"]
        )].append({
            **fragment_payload,
            "fragment_id": fragment_id,
            "box": exact_box,
            "payload": physical,
            "occurrence_id": occurrence,
        })

    negatives: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    negative_sample: dict[str, Any] | None = None
    for rows, id_field, box_field in (
        (
            wrong_rows,
            "Round295B_wrong_signed_empty_no_binding_row_id",
            "exact_empty_intersection_ps_rectangle",
        ),
        (
            graph_rows,
            "Round295B_graph_separated_no_binding_row_id",
            "exact_relation_ps_rectangle",
        ),
    ):
        for row in rows:
            ensure(
                row["terminal_registry_target_reference_count"] == 0
                and not row["terminal_registry_target_references"]
                and row["formal_existing_physical_incidence_binding_credit"]
                == 0
                and row["formal_seam_edge_credit"] == 0,
                f"R295B negative row:{row[id_field]}",
            )
            evidence = {
                "row_id": row[id_field],
                "row_sha256": row["row_sha256"],
                "classification": row["no_binding_classification"],
                "box": ps_box(row[box_field], row[id_field]),
            }
            negatives[(
                row["Round268_true_seam_patch_row_id"], row["side_index"]
            )].append(evidence)
            if negative_sample is None:
                negative_sample = evidence

    source_names = (
        "ROUND282_STRICT_CORRIDOR_TERMINAL_SLICE",
        "ROUND295B_PHYSICAL_TERMINAL_FACE_INCIDENCE",
    )
    raw_by_source: Counter[str] = Counter()
    local_keys: dict[str, Counter[tuple[Any, ...]]] = {
        source: Counter() for source in source_names
    }
    union_keys: Counter[tuple[Any, ...]] = Counter()
    key_sources: dict[tuple[Any, ...], Counter[str]] = defaultdict(Counter)
    fragment_ids: set[str] = set()
    for patch_side, rows in fragments.items():
        for fragment in rows:
            source = fragment["source_kind"]
            ensure(source in source_names, f"fragment source:{source}")
            atom = (
                patch_side[0],
                patch_side[1],
                tuple(fragment["exact_ps_box"]),
                fragment["physical_payload_sha256"],
                fragment["occurrence_id"],
            )
            raw_by_source[source] += 1
            local_keys[source][atom] += 1
            union_keys[atom] += 1
            key_sources[atom][source] += 1
            ensure(
                fragment["fragment_id"] not in fragment_ids,
                "raw fragment evidence injectivity",
            )
            fragment_ids.add(fragment["fragment_id"])

    def mult_hist(counter: Counter[tuple[Any, ...]]) -> dict[str, int]:
        return {
            str(key): value for key, value in sorted(
                Counter(counter.values()).items()
            )
        }

    source_audit: dict[str, dict[str, Any]] = {}
    for source in source_names:
        raw = raw_by_source[source]
        distinct = len(local_keys[source])
        source_audit[source] = {
            "raw_evidence_fragment_count": raw,
            "distinct_formal_endpoint_atom_count": distinct,
            "duplicate_evidence_excess_count": raw - distinct,
            "formal_atom_evidence_multiplicity_histogram":
                mult_hist(local_keys[source]),
        }
    reasons: dict[str, Counter[str]] = defaultdict(Counter)
    for atom, multiplicity in union_keys.items():
        source_counts = key_sources[atom]
        if len(source_counts) == 2:
            reason = (
                "CROSS_ROUND282_ROUND295B_EVIDENCE_FOR_SAME_"
                "OCCURRENCE_BOX_PAYLOAD"
            )
        elif multiplicity == 1:
            reason = "UNIQUE_FORMAL_ENDPOINT_ATOM_EVIDENCE"
        elif source_names[0] in source_counts:
            reason = (
                "MULTIPLE_ROUND282_CORRIDOR_OR_MAPPING_EVIDENCE_FOR_"
                "SAME_OCCURRENCE_BOX_PAYLOAD"
            )
        else:
            reason = (
                "MULTIPLE_ROUND295B_INCIDENCE_ROWS_FOR_SAME_"
                "OCCURRENCE_BOX_PAYLOAD"
            )
        reasons[reason]["formal_endpoint_atom_count"] += 1
        reasons[reason]["raw_evidence_fragment_count"] += multiplicity
        reasons[reason]["duplicate_evidence_excess_count"] += multiplicity - 1
    fragment_audit = {
        "formal_endpoint_atom_key_fields": [
            "Round268_true_seam_patch_row_id",
            "side_index",
            "exact_ps_box",
            "complete_physical_payload_sha256",
            "actual_Round294_registry_occurrence_id",
        ],
        "raw_evidence_fragment_count": sum(raw_by_source.values()),
        "distinct_formal_endpoint_atom_count": len(union_keys),
        "duplicate_evidence_excess_count":
            sum(raw_by_source.values()) - len(union_keys),
        "formal_atom_evidence_multiplicity_histogram": mult_hist(union_keys),
        "by_fragment_source": source_audit,
        "same_occurrence_box_payload_reason_strata": {
            reason: dict(sorted(values.items()))
            for reason, values in sorted(reasons.items())
        },
        "raw_evidence_is_retained_only_as_provenance": True,
        "cell_payload_occurrence_maps_deduplicate_formal_atoms": True,
        "edge_keys_derive_from_deduplicated_cell_payload_occurrence_maps":
            True,
    }
    ensure(
        len(used_regions) == 2_636
        and len(fragments) == 304
        and fragment_audit["raw_evidence_fragment_count"] == 14_980
        and fragment_audit["distinct_formal_endpoint_atom_count"] == 10_588
        and fragment_audit["duplicate_evidence_excess_count"] == 4_392
        and source_audit[source_names[0]] == {
            "raw_evidence_fragment_count": 3_532,
            "distinct_formal_endpoint_atom_count": 3_004,
            "duplicate_evidence_excess_count": 528,
            "formal_atom_evidence_multiplicity_histogram": {
                "1": 2_652, "2": 240, "3": 48, "4": 64,
            },
        }
        and source_audit[source_names[1]] == {
            "raw_evidence_fragment_count": 11_448,
            "distinct_formal_endpoint_atom_count": 7_584,
            "duplicate_evidence_excess_count": 3_864,
            "formal_atom_evidence_multiplicity_histogram": {
                "1": 5_856, "2": 640, "3": 40, "4": 1_048,
            },
        }
        and canonicalized_count == 5_292
        and already_canonical_count == 6_156,
        "independent fragment/canonicalization census",
    )
    ensure(
        fragment_audit["same_occurrence_box_payload_reason_strata"] == {
            "MULTIPLE_ROUND282_CORRIDOR_OR_MAPPING_EVIDENCE_FOR_SAME_"
            "OCCURRENCE_BOX_PAYLOAD": {
                "duplicate_evidence_excess_count": 528,
                "formal_endpoint_atom_count": 352,
                "raw_evidence_fragment_count": 880,
            },
            "MULTIPLE_ROUND295B_INCIDENCE_ROWS_FOR_SAME_"
            "OCCURRENCE_BOX_PAYLOAD": {
                "duplicate_evidence_excess_count": 3_864,
                "formal_endpoint_atom_count": 1_728,
                "raw_evidence_fragment_count": 5_592,
            },
            "UNIQUE_FORMAL_ENDPOINT_ATOM_EVIDENCE": {
                "duplicate_evidence_excess_count": 0,
                "formal_endpoint_atom_count": 8_508,
                "raw_evidence_fragment_count": 8_508,
            },
        },
        "independent same occurrence/box/payload reason strata",
    )

    edge_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    edge_classes: Counter[str] = Counter()
    common_payload_hist: Counter[int] = Counter()
    tail_cell_hist: Counter[int] = Counter()
    pair_multiplicity: Counter[tuple[str, str]] = Counter()
    occurrence_targets: set[str] = set()
    self_edges = 0
    for patch_id in sorted(patches_by_id):
        patch = patches_by_id[patch_id]
        patch_class = (
            "FULL"
            if corridors_by_patch[patch_id]["classification"]
            == "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER"
            else "TAIL"
        )
        patch_box = ps_box([
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ], patch_id)
        p_cuts = {patch_box[0], patch_box[1]}
        s_cuts = {patch_box[2], patch_box[3]}
        for side_index in (0, 1):
            for fragment in fragments[(patch_id, side_index)]:
                ensure(
                    contains(patch_box, fragment["box"]),
                    f"fragment inside patch:{fragment['fragment_id']}",
                )
                p_cuts.update(fragment["box"][:2])
                s_cuts.update(fragment["box"][2:])
        p_values = sorted(p_cuts)
        s_values = sorted(s_cuts)
        exact_cells = [
            (p0, p1, s0, s1)
            for p0, p1 in zip(p_values, p_values[1:])
            for s0, s1 in zip(s_values, s_values[1:])
        ]
        ensure(
            all(area(cell_box) > 0 for cell_box in exact_cells)
            and sum(map(area, exact_cells), Fraction(0)) == area(patch_box),
            f"independent exact-cell area partition:{patch_id}",
        )
        if patch_class == "TAIL":
            tail_cell_hist[len(exact_cells)] += 1

        for cell_index, cell_box in enumerate(exact_cells):
            cell_id = "round296-true-seam-cell:" + digest([
                "ROUND296_TRUE_SEAM_EXACT_HALF_OPEN_PS_CELL_V1",
                patch_id,
                cell_index,
                box_text(cell_box),
            ])
            side_maps: list[dict[str, dict[str, Any]]] = []
            for side_index in (0, 1):
                payload_map: dict[str, dict[str, Any]] = {}
                for fragment in fragments[(patch_id, side_index)]:
                    if not contains(fragment["box"], cell_box):
                        continue
                    payload_sha = fragment["physical_payload_sha256"]
                    value = payload_map.setdefault(payload_sha, {
                        "physical_payload": fragment["payload"],
                        "occurrence_evidence": defaultdict(set),
                    })
                    ensure(
                        value["physical_payload"] == fragment["payload"],
                        f"physical payload SHA collision:{payload_sha}",
                    )
                    value["occurrence_evidence"][
                        fragment["occurrence_id"]
                    ].add(fragment["fragment_id"])
                normalized: dict[str, dict[str, Any]] = {}
                for payload_sha, value in payload_map.items():
                    normalized[payload_sha] = {
                        "physical_payload": value["physical_payload"],
                        "occurrence_evidence": {
                            occurrence: sorted(evidence)
                            for occurrence, evidence in sorted(
                                value["occurrence_evidence"].items()
                            )
                        },
                    }
                side_maps.append(normalized)
            common = sorted(set(side_maps[0]) & set(side_maps[1]))
            common_payload_hist[len(common)] += 1
            ensure(len(common) in {1, 2}, f"common payload count:{cell_id}")

            cell_edge_ids: list[str] = []
            for payload_sha in common:
                physical = side_maps[0][payload_sha]["physical_payload"]
                ensure(
                    physical == side_maps[1][payload_sha]["physical_payload"],
                    f"complete payload match:{cell_id}:{payload_sha}",
                )
                left = side_maps[0][payload_sha]["occurrence_evidence"]
                right = side_maps[1][payload_sha]["occurrence_evidence"]
                for left_occurrence in sorted(left):
                    for right_occurrence in sorted(right):
                        if left_occurrence == right_occurrence:
                            self_edges += 1
                            continue
                        endpoint_pair = tuple(sorted((
                            left_occurrence, right_occurrence
                        )))
                        edge_payload = {
                            "Round268_true_seam_patch_row_id": patch_id,
                            "Round296_true_seam_cell_id": cell_id,
                            "cell_index": cell_index,
                            "exact_half_open_ps_cell": box_text(cell_box),
                            "physical_payload": physical,
                            "physical_payload_sha256": payload_sha,
                            "left_formal_occurrence_id": left_occurrence,
                            "right_formal_occurrence_id": right_occurrence,
                            "unordered_formal_occurrence_endpoint_pair":
                                list(endpoint_pair),
                        }
                        edge_id = (
                            "round296-true-seam-occurrence-edge:" + digest([
                                "ROUND296_TRUE_SEAM_OCCURRENCE_EDGE_KEY_V1",
                                edge_payload,
                            ])
                        )
                        edge_row = {
                            "Round296_true_seam_occurrence_edge_row_id":
                                edge_id,
                            **edge_payload,
                            "patch_class": patch_class,
                            "cyclic_transition_identity":
                                patch["cyclic_transition_identity"],
                            "left_endpoint_evidence_fragment_ids":
                                left[left_occurrence],
                            "right_endpoint_evidence_fragment_ids":
                                right[right_occurrence],
                            "repeated_endpoint_pair_across_cells_preserved":
                                True,
                            "occurrence_identity_collapsed": False,
                            "formal_true_seam_edge_credit": 1,
                            **{field: 0 for field in ZERO_FIELDS},
                        }
                        edge_row["row_sha256"] = digest(edge_row)
                        edge_rows.append(edge_row)
                        cell_edge_ids.append(edge_id)
                        edge_classes[patch_class] += 1
                        pair_multiplicity[endpoint_pair] += 1
                        occurrence_targets.update(endpoint_pair)

            def side_document(side_index: int) -> list[dict[str, Any]]:
                output: list[dict[str, Any]] = []
                for payload_sha, value in sorted(
                    side_maps[side_index].items()
                ):
                    output.append({
                        "physical_payload_sha256": payload_sha,
                        "physical_payload": value["physical_payload"],
                        "formal_occurrence_ids":
                            sorted(value["occurrence_evidence"]),
                        "occurrence_evidence_fragment_ids": {
                            occurrence: evidence
                            for occurrence, evidence in sorted(
                                value["occurrence_evidence"].items()
                            )
                        },
                    })
                return output

            negative_evidence: list[dict[str, Any]] = []
            for side_index in (0, 1):
                for evidence in negatives[(patch_id, side_index)]:
                    if contains(evidence["box"], cell_box):
                        negative_evidence.append({
                            "side_index": side_index,
                            "source_row_id": evidence["row_id"],
                            "source_row_sha256": evidence["row_sha256"],
                            "classification": evidence["classification"],
                        })
            common_document = [{
                "physical_payload_sha256": payload_sha,
                "physical_payload":
                    side_maps[0][payload_sha]["physical_payload"],
                "left_formal_occurrence_ids": sorted(
                    side_maps[0][payload_sha]["occurrence_evidence"]
                ),
                "right_formal_occurrence_ids": sorted(
                    side_maps[1][payload_sha]["occurrence_evidence"]
                ),
            } for payload_sha in common]
            cell_row = {
                "Round296_true_seam_cell_coverage_row_id": cell_id,
                "Round268_true_seam_patch_row_id": patch_id,
                "Round268_patch_row_sha256": patch["row_sha256"],
                "Round282_seam_corridor_row_id":
                    corridors_by_patch[patch_id][
                        "Round282_seam_corridor_row_id"
                    ],
                "Round285_safe_pairing_row_id":
                    safe_by_patch[patch_id]["Round285_safe_pairing_row_id"],
                "patch_class": patch_class,
                "cell_index": cell_index,
                "exact_half_open_ps_cell": box_text(cell_box),
                "exact_positive_cell_area": str(area(cell_box)),
                "half_open_p_upper_included":
                    cell_box[1] == patch_box[1],
                "half_open_s_upper_included":
                    cell_box[3] == patch_box[3],
                "left_payload_occurrence_bindings": side_document(0),
                "right_payload_occurrence_bindings": side_document(1),
                "common_physical_payload_count": len(common),
                "common_physical_payload_bindings": common_document,
                "formal_edge_row_count": len(cell_edge_ids),
                "formal_edge_row_ids": sorted(cell_edge_ids),
                "wrong_sign_or_graph_separated_no_bind_evidence": sorted(
                    negative_evidence,
                    key=lambda value: (
                        value["side_index"], value["source_row_id"]
                    ),
                ),
                "wrong_sign_or_graph_separated_rows_used_as_endpoints": 0,
                "formal_true_seam_edge_credit": 0,
                **{field: 0 for field in ZERO_FIELDS},
            }
            cell_row["row_sha256"] = digest(cell_row)
            cell_rows.append(cell_row)

    edge_rows.sort(
        key=lambda row: row["Round296_true_seam_occurrence_edge_row_id"]
    )
    cell_rows.sort(
        key=lambda row: row["Round296_true_seam_cell_coverage_row_id"]
    )
    edge_ids = [
        row["Round296_true_seam_occurrence_edge_row_id"] for row in edge_rows
    ]
    ensure(
        len(edge_rows) == len(set(edge_ids))
        and sum(row["formal_true_seam_edge_credit"] for row in edge_rows)
        == len(edge_rows)
        and all(
            row[field] == 0
            for row in edge_rows + cell_rows
            for field in ZERO_FIELDS
        )
        and all(
            row["left_formal_occurrence_id"] in formal_ids
            and row["right_formal_occurrence_id"] in formal_ids
            for row in edge_rows
        ),
        "edge-only credit and formal endpoint domain",
    )
    pair_hist = Counter(pair_multiplicity.values())
    preview = {
        "exact_cell_count": len(cell_rows),
        "full_patch_exact_cell_count":
            sum(row["patch_class"] == "FULL" for row in cell_rows),
        "tail_patch_exact_cell_count":
            sum(row["patch_class"] == "TAIL" for row in cell_rows),
        "formal_true_seam_edge_count": len(edge_rows),
        "full_patch_edge_count": edge_classes["FULL"],
        "tail_patch_edge_count": edge_classes["TAIL"],
        "distinct_unordered_endpoint_pair_count": len(pair_multiplicity),
        "distinct_occurrence_target_count": len(occurrence_targets),
        "self_edge_count": self_edges,
        "common_payload_count_per_cell_histogram": {
            str(key): value
            for key, value in sorted(common_payload_hist.items())
        },
        "tail_patch_cell_count_histogram": {
            str(key): value for key, value in sorted(tail_cell_hist.items())
        },
    }
    ensure(
        preview == EXPECTED_PREVIEW,
        f"post-reconstruction preview countercheck:{preview}",
    )
    edge_ledger = make_ledger(
        edge_rows,
        EDGE_SCHEMA,
        "FORMAL_48444_TRUE_SEAM_OCCURRENCE_EDGE_ROWS__"
        "NO_DSU_OR_QUOTIENT_EXECUTED",
        "Round296_true_seam_occurrence_edge_row_id",
    )
    cell_ledger = make_ledger(
        cell_rows,
        CELL_SCHEMA,
        "EXACT_3444_HALF_OPEN_PS_COMMON_REFINEMENT_CELLS__"
        "ALL_152_TRUE_SEAM_PATCHES_COVERED",
        "Round296_true_seam_cell_coverage_row_id",
    )

    def attachment(
        value: dict[str, Any], filename: str
    ) -> dict[str, Any]:
        return {
            "filename": filename,
            "schema": value["schema"],
            "row_count": value["row_count"],
            "row_ids_sha256": value["row_ids_sha256"],
            "row_hashes_sha256": value["row_hashes_sha256"],
            "rows_sha256": value["rows_sha256"],
        }

    expected_result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND296_FORMAL_TRUE_SEAM_OCCURRENCE_EDGE_LEDGER__"
            "152_PATCHES__3444_EXACT_CELLS__48444_FORMAL_EDGES__"
            "DSU_NOT_RUN__QUOTIENT_NOT_COMPUTED"
        ),
        "input_package_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_package_entry_count": sum(map(len, package_entries.values())),
        "source_reconstruction_contract": {
            "preview_used_as_construction_oracle": False,
            "preview_consulted_only_after_complete_reconstruction": True,
            "Round282_strict_corridor_terminal_mapping_rule":
                "per-corridor exact nearest t^2 interval closure to the "
                "dyadic seam endpoint",
            "Round295B_physical_incidence_rows_consumed": 11_448,
            "total_terminal_endpoint_evidence_fragment_count": 14_980,
            "Round282_strict_terminal_evidence_fragment_count": 3_532,
            "fragment_raw_vs_formal_atom_dedup_audit": fragment_audit,
            "Round295B_target_references_canonicalized_from_Round294_"
            "source_row_id": canonicalized_count,
            "Round295B_target_references_already_canonical_occurrence_ID":
                already_canonical_count,
            "every_edge_endpoint_is_actual_Round294_registry_occurrence_ID":
                True,
            "Round295B_wrong_signed_empty_rows_excluded": 468,
            "Round295B_graph_separated_rows_excluded": 288,
            "wrong_sign_or_graph_separated_row_ever_used_as_endpoint": False,
            "complete_transported_physical_payload_fields": [
                "target_chart", "target_lift", "outgoing_cell",
                "ordered_integer_wall_events", "roof", "signed_wall_word",
            ],
            "pair_only_payloads_common_to_both_sides": True,
            "Round285_safe_pairing_semantics_validated_for_all_152_"
            "patches": True,
            "Round285_validated_semantic_fields": [
                "same_physical_source_point",
                "Round171_normal_position_velocity_identity",
                "transported_owner_target_sets_equal",
                "owner_shadow_half_open_pair",
                "cyclic_transition_identity_matches_Round268",
                "Round282_geometry_classification_matches_Round282",
                "exact_cells_positive_disjoint_and_area_conservative",
            ],
            "Round285_exact_cell_class_histogram": {
                key: value for key, value in sorted(safe_classes.items())
            },
            "Round285_exact_cell_class_area_partition": {
                key: str(value)
                for key, value in sorted(safe_class_areas.items())
            },
            "Round285_uncovered_negative_cells_used_as_edge_endpoints": 0,
        },
        "census": {
            **preview,
            "true_seam_patch_count": 152,
            "formal_edge_row_count": len(edge_rows),
            "edge_key_count": len(edge_ids),
            "edge_key_collision_count": 0,
            "unordered_endpoint_pair_edge_multiplicity_histogram": {
                str(key): value for key, value in sorted(pair_hist.items())
            },
            "repeated_endpoint_pairs_across_cells_preserved": True,
        },
        "preview_counterevidence_crosscheck": {
            "source_reconstruction_completed_before_comparison": True,
            "computed_values": preview,
            "preview_values": EXPECTED_PREVIEW,
            "exact_match": True,
        },
        "edge_ledger": attachment(edge_ledger, EDGE.name),
        "cell_coverage_ledger": attachment(cell_ledger, CELL.name),
        "formal_credit_transition": {
            "formal_true_seam_edge_credit": len(edge_rows),
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "strict_nonpromotion": {
            "component_DSU_executed": False,
            "quotient_computed": False,
            "quotient_component_count": None,
            "ordinary_face_edges_consumed_or_promoted": False,
            "maximality_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "fibre_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "global_disposition_status":
                "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "scope_contract": {
            "registry_scope": "ROUND294_FORMAL_STAGE_A_OCCURRENCE_REGISTRY",
            "true_seam_scope":
                "ALL_152_FROZEN_ROUND268_POSITIVE_AREA_PATCHES",
            "edge_evidence_frozen_without_connectivity_claim": True,
            "future_DSU_must_consume_all_48444_edge_rows": True,
        },
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "seed_affects_output": False,
            "upstream_producer_imported_or_executed": False,
        },
        "required_next": [
            "Independently reconstruct both ledgers cachelessly without "
            "importing or executing this producer.",
            "Only a later explicit DSU round may turn edge evidence into "
            "rank reduction or a quotient-component census.",
        ],
    }
    edge_bytes = deterministic_gzip(edge_ledger)
    cell_bytes = deterministic_gzip(cell_ledger)
    expected_result["edge_ledger"]["file_sha256"] = hashlib.sha256(
        edge_bytes
    ).hexdigest()
    expected_result["cell_coverage_ledger"]["file_sha256"] = hashlib.sha256(
        cell_bytes
    ).hexdigest()
    expected_result["seed_affects_output"] = False
    expected_result["result_sha256"] = digest(expected_result)

    context = {
        "formal_ids": formal_ids,
        "raw_noncanonical_reference": raw_noncanonical_sample,
        "negative_sample": negative_sample,
        "fragment_audit": fragment_audit,
        "preview": preview,
        "safe_class_histogram": dict(safe_classes),
        "safe_class_areas": {
            key: str(value) for key, value in safe_class_areas.items()
        },
        "canonical_source_map_count": len(source_to_occurrence),
        "expected_edge_bytes": edge_bytes,
        "expected_cell_bytes": cell_bytes,
        "expected_result_bytes": canonical(expected_result),
    }
    return edge_ledger, cell_ledger, expected_result, context


def validate_edge_row(
    row: dict[str, Any], formal_ids: set[str]
) -> None:
    closed(row, row["Round296_true_seam_occurrence_edge_row_id"])
    payload = {
        "Round268_true_seam_patch_row_id":
            row["Round268_true_seam_patch_row_id"],
        "Round296_true_seam_cell_id": row["Round296_true_seam_cell_id"],
        "cell_index": row["cell_index"],
        "exact_half_open_ps_cell": row["exact_half_open_ps_cell"],
        "physical_payload": row["physical_payload"],
        "physical_payload_sha256": row["physical_payload_sha256"],
        "left_formal_occurrence_id": row["left_formal_occurrence_id"],
        "right_formal_occurrence_id": row["right_formal_occurrence_id"],
        "unordered_formal_occurrence_endpoint_pair":
            row["unordered_formal_occurrence_endpoint_pair"],
    }
    left = row["left_formal_occurrence_id"]
    right = row["right_formal_occurrence_id"]
    ensure(
        row["Round296_true_seam_occurrence_edge_row_id"]
        == "round296-true-seam-occurrence-edge:" + digest([
            "ROUND296_TRUE_SEAM_OCCURRENCE_EDGE_KEY_V1", payload
        ])
        and set(row["physical_payload"]) == {
            "target_chart", "target_lift", "outgoing_cell",
            "ordered_integer_wall_events", "roof", "signed_wall_word",
        }
        and row["physical_payload_sha256"] == digest(row["physical_payload"])
        and left in formal_ids
        and right in formal_ids
        and left != right
        and row["unordered_formal_occurrence_endpoint_pair"]
        == sorted((left, right))
        and row["formal_true_seam_edge_credit"] == 1
        and all(row[field] == 0 for field in ZERO_FIELDS)
        and all(
            evidence.startswith("round296-seam-fragment:")
            for evidence in (
                row["left_endpoint_evidence_fragment_ids"]
                + row["right_endpoint_evidence_fragment_ids"]
            )
        ),
        f"semantic edge row:{row['Round296_true_seam_occurrence_edge_row_id']}",
    )


def validate_cell_row(row: dict[str, Any]) -> None:
    closed(row, row["Round296_true_seam_cell_coverage_row_id"])
    box = ps_box(
        row["exact_half_open_ps_cell"],
        row["Round296_true_seam_cell_coverage_row_id"],
    )
    left_payloads = {
        item["physical_payload_sha256"]
        for item in row["left_payload_occurrence_bindings"]
    }
    right_payloads = {
        item["physical_payload_sha256"]
        for item in row["right_payload_occurrence_bindings"]
    }
    common_payloads = {
        item["physical_payload_sha256"]
        for item in row["common_physical_payload_bindings"]
    }
    ensure(
        Fraction(row["exact_positive_cell_area"]) == area(box) > 0
        and common_payloads == left_payloads & right_payloads
        and row["common_physical_payload_count"] == len(common_payloads)
        and row["formal_edge_row_count"] == len(row["formal_edge_row_ids"])
        and len(set(row["formal_edge_row_ids"]))
        == len(row["formal_edge_row_ids"])
        and row[
            "wrong_sign_or_graph_separated_rows_used_as_endpoints"
        ] == 0
        and row["formal_true_seam_edge_credit"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        f"semantic cell row:{row['Round296_true_seam_cell_coverage_row_id']}",
    )


def validate_candidate(
    edge_path: Path,
    cell_path: Path,
    result_path: Path,
    expected_edge: dict[str, Any],
    expected_cell: dict[str, Any],
    expected_result: dict[str, Any],
    context: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidate_edge = read_gzip(edge_path)
    candidate_cell = read_gzip(cell_path)
    candidate_result = read_json(result_path, canonical_required=True)
    ensure(
        edge_path.read_bytes() == context["expected_edge_bytes"],
        "byte-exact deterministic edge gzip",
    )
    ensure(
        cell_path.read_bytes() == context["expected_cell_bytes"],
        "byte-exact deterministic cell gzip",
    )
    ensure(
        result_path.read_bytes() == context["expected_result_bytes"],
        "byte-exact canonical result",
    )
    ensure(candidate_edge == expected_edge, "exact independently rebuilt edges")
    ensure(candidate_cell == expected_cell, "exact independently rebuilt cells")
    ensure(
        candidate_result == expected_result,
        "exact independently rebuilt result",
    )
    formal_ids = context["formal_ids"]
    for row in candidate_edge["rows"]:
        validate_edge_row(row, formal_ids)
    for row in candidate_cell["rows"]:
        validate_cell_row(row)
    result_payload = dict(candidate_result)
    result_digest = result_payload.pop("result_sha256", None)
    ensure(
        result_digest == digest(result_payload)
        and candidate_result["strict_nonpromotion"] == {
            "component_DSU_executed": False,
            "quotient_computed": False,
            "quotient_component_count": None,
            "ordinary_face_edges_consumed_or_promoted": False,
            "maximality_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "fibre_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "global_disposition_status":
                "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "result self digest and zero-DSU scope",
    )
    return candidate_edge, candidate_cell, candidate_result


def reclose_edge(row: dict[str, Any]) -> None:
    row["unordered_formal_occurrence_endpoint_pair"] = sorted((
        row["left_formal_occurrence_id"],
        row["right_formal_occurrence_id"],
    ))
    edge_payload = {
        "Round268_true_seam_patch_row_id":
            row["Round268_true_seam_patch_row_id"],
        "Round296_true_seam_cell_id": row["Round296_true_seam_cell_id"],
        "cell_index": row["cell_index"],
        "exact_half_open_ps_cell": row["exact_half_open_ps_cell"],
        "physical_payload": row["physical_payload"],
        "physical_payload_sha256": row["physical_payload_sha256"],
        "left_formal_occurrence_id": row["left_formal_occurrence_id"],
        "right_formal_occurrence_id": row["right_formal_occurrence_id"],
        "unordered_formal_occurrence_endpoint_pair":
            row["unordered_formal_occurrence_endpoint_pair"],
    }
    row["Round296_true_seam_occurrence_edge_row_id"] = (
        "round296-true-seam-occurrence-edge:" + digest([
            "ROUND296_TRUE_SEAM_OCCURRENCE_EDGE_KEY_V1", edge_payload
        ])
    )
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)


def reclose_ledger(
    ledger: dict[str, Any], id_field: str
) -> None:
    rows = ledger["rows"]
    ledger["row_count"] = len(rows)
    ledger["row_ids_sha256"] = digest([row[id_field] for row in rows])
    ledger["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in rows]
    )
    ledger["rows_sha256"] = digest(rows)


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def build_attack_suite(
    expected_edge: dict[str, Any],
    expected_cell: dict[str, Any],
    expected_result: dict[str, Any],
    candidate_edge: dict[str, Any],
    candidate_cell: dict[str, Any],
    candidate_result: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[dict[str, Any]] = []

    def reject(
        attack_id: str,
        classification: str,
        action: Callable[[], None],
        *,
        reclosed: bool = False,
    ) -> None:
        rejected = False
        reason = ""
        try:
            action()
        except VerificationError:
            rejected = True
            reason = f"FAIL_CLOSED_BY_{classification}"
        attacks.append({
            "attack_id": attack_id,
            "classification": classification,
            "fully_reclosed": reclosed,
            "rejected": rejected,
            "rejection_reason": reason,
        })
        ensure(rejected, f"attack must be rejected:{attack_id}")

    def require_object(payload: bytes) -> None:
        ensure(isinstance(strict_json_bytes(payload), dict), "JSON object")

    reject(
        "json_duplicate_key",
        "STRICT_JSON",
        lambda: require_object(b'{"a":1,"a":2}'),
    )
    reject(
        "json_float",
        "STRICT_JSON",
        lambda: require_object(b'{"a":1.25}'),
    )
    reject(
        "json_nonfinite",
        "STRICT_JSON",
        lambda: require_object(b'{"a":NaN}'),
    )
    reject(
        "json_huge_integer",
        "STRICT_JSON",
        lambda: require_object(
            ('{"a":' + '9' * 129 + '}').encode("ascii")
        ),
    )
    reject(
        "json_trailing_document",
        "STRICT_JSON",
        lambda: require_object(b'{"a":1}{"b":2}'),
    )
    reject(
        "json_invalid_utf8",
        "STRICT_JSON",
        lambda: require_object(b'{"a":"\\xff"}'.replace(b"\\\\xff", b"\\xff")),
    )
    reject(
        "json_array_root",
        "STRICT_JSON",
        lambda: require_object(b"[]"),
    )

    def canonical_small(payload: bytes) -> None:
        value = strict_json_bytes(payload)
        ensure(payload == canonical(value), "canonical JSON bytes")

    reject(
        "json_leading_whitespace",
        "STRICT_JSON_CANONICALITY",
        lambda: canonical_small(b' {"a":1}'),
    )
    small_gzip = deterministic_gzip({"a": 1})
    reject(
        "gzip_concatenated_members",
        "STRICT_GZIP",
        lambda: scan_gzip_bytes(small_gzip + small_gzip, 1024),
    )
    reject(
        "gzip_trailing_bytes",
        "STRICT_GZIP",
        lambda: scan_gzip_bytes(small_gzip + b"x", 1024),
    )
    reject(
        "gzip_truncated",
        "STRICT_GZIP",
        lambda: scan_gzip_bytes(small_gzip[:-3], 1024),
    )
    reject(
        "gzip_invalid_header",
        "STRICT_GZIP",
        lambda: scan_gzip_bytes(b"not-gzip", 1024),
    )
    reject(
        "gzip_uncompressed_cap",
        "STRICT_GZIP",
        lambda: scan_gzip_bytes(deterministic_gzip("x" * 2048), 32),
    )

    temporary_paths: list[Path] = []
    try:
        missing = HERE / f".{PREFIX}.attack-missing-{os.getpid()}"
        reject(
            "path_missing",
            "STRICT_PATH",
            lambda: safe_regular(missing),
        )
        with tempfile.NamedTemporaryFile(
            dir=HERE, prefix=f".{PREFIX}.attack-empty-", delete=False
        ) as stream:
            empty = Path(stream.name)
        temporary_paths.append(empty)
        reject(
            "path_empty",
            "STRICT_PATH",
            lambda: safe_regular(empty),
        )

        symlink = HERE / f".{PREFIX}.attack-symlink-{os.getpid()}"
        symlink.symlink_to(RESULT.name)
        temporary_paths.append(symlink)
        reject(
            "path_symlink",
            "STRICT_PATH",
            lambda: safe_regular(symlink),
        )

        with tempfile.NamedTemporaryFile(
            dir=HERE, prefix=f".{PREFIX}.attack-hard-src-", delete=False
        ) as stream:
            stream.write(b"x")
            hard_source = Path(stream.name)
        hard_link = HERE / f".{PREFIX}.attack-hardlink-{os.getpid()}"
        os.link(hard_source, hard_link)
        temporary_paths.extend([hard_source, hard_link])
        reject(
            "path_hardlink",
            "STRICT_PATH",
            lambda: safe_regular(hard_link),
        )

        fifo = HERE / f".{PREFIX}.attack-fifo-{os.getpid()}"
        os.mkfifo(fifo)
        temporary_paths.append(fifo)
        reject(
            "path_fifo",
            "STRICT_PATH",
            lambda: safe_regular(fifo),
        )

        directory = Path(tempfile.mkdtemp(
            dir=HERE, prefix=f".{PREFIX}.attack-directory-"
        ))
        temporary_paths.append(directory)
        reject(
            "path_directory",
            "STRICT_PATH",
            lambda: safe_regular(directory),
        )

        with tempfile.NamedTemporaryFile(
            dir=HERE, prefix=f".{PREFIX}.attack-oversize-", delete=False
        ) as stream:
            oversize = Path(stream.name)
            stream.truncate(MAX_FILE_BYTES + 1)
        temporary_paths.append(oversize)
        reject(
            "path_oversize",
            "STRICT_PATH",
            lambda: safe_regular(oversize),
        )

        outside = Path(tempfile.gettempdir()) / (
            f"{PREFIX}.attack-outside-{os.getpid()}"
        )
        reject(
            "path_parent_escape",
            "STRICT_PATH",
            lambda: safe_regular(outside),
        )
    finally:
        for path in reversed(temporary_paths):
            try:
                if path.is_dir() and not path.is_symlink():
                    path.rmdir()
                else:
                    path.unlink()
            except FileNotFoundError:
                pass

    raw_reference = context["raw_noncanonical_reference"]
    ensure(
        isinstance(raw_reference, str)
        and raw_reference not in context["formal_ids"],
        "noncanonical R295B attack witness",
    )
    reject(
        "raw_r295b_source_row_treated_as_occurrence_id",
        "TARGET_REFERENCE_CANONICALIZATION",
        lambda: ensure(
            raw_reference in context["formal_ids"],
            "raw R295B source row is not a formal occurrence ID",
        ),
    )
    reject(
        "missing_source_row_mapping",
        "TARGET_REFERENCE_CANONICALIZATION",
        lambda: ensure(
            raw_reference in {},
            "missing R294 source-row mapping",
        ),
    )

    def duplicate_mapping() -> None:
        mapping: dict[str, str] = {}
        for key, value in (("x", "a"), ("x", "b")):
            ensure(key not in mapping, "duplicate R294 source-row mapping")
            mapping[key] = value

    reject(
        "duplicate_source_row_mapping",
        "TARGET_REFERENCE_CANONICALIZATION",
        duplicate_mapping,
    )

    edge0 = candidate_edge["rows"][0]

    def forged_edge(
        mutate: Callable[[dict[str, Any]], None],
        semantic: bool = True,
    ) -> None:
        row = dict(edge0)
        row["physical_payload"] = dict(row["physical_payload"])
        row["left_endpoint_evidence_fragment_ids"] = list(
            row["left_endpoint_evidence_fragment_ids"]
        )
        row["right_endpoint_evidence_fragment_ids"] = list(
            row["right_endpoint_evidence_fragment_ids"]
        )
        mutate(row)
        reclose_edge(row)
        closed(row, row["Round296_true_seam_occurrence_edge_row_id"])
        if semantic:
            validate_edge_row(row, context["formal_ids"])
        ensure(row == expected_edge["rows"][0], "independent exact edge row")

    reject(
        "external_occurrence_endpoint",
        "EDGE_SEMANTICS",
        lambda: forged_edge(
            lambda row: row.__setitem__(
                "left_formal_occurrence_id",
                "round294-occurrence:external-domain-forgery",
            )
        ),
        reclosed=True,
    )
    reject(
        "self_edge",
        "EDGE_SEMANTICS",
        lambda: forged_edge(
            lambda row: row.__setitem__(
                "right_formal_occurrence_id",
                row["left_formal_occurrence_id"],
            )
        ),
        reclosed=True,
    )

    def drop_payload_field(row: dict[str, Any]) -> None:
        row["physical_payload"].pop("signed_wall_word")
        row["physical_payload_sha256"] = digest(row["physical_payload"])

    reject(
        "drop_complete_payload_field",
        "COMPLETE_PHYSICAL_PAYLOAD",
        lambda: forged_edge(drop_payload_field),
        reclosed=True,
    )

    def alter_payload(row: dict[str, Any]) -> None:
        row["physical_payload"]["target_chart"] = "G:FORGED"
        row["physical_payload_sha256"] = digest(row["physical_payload"])

    reject(
        "alter_complete_payload",
        "COMPLETE_PHYSICAL_PAYLOAD",
        lambda: forged_edge(alter_payload),
        reclosed=True,
    )
    reject(
        "swap_oriented_endpoints",
        "EDGE_KEY",
        lambda: forged_edge(
            lambda row: (
                row.__setitem__(
                    "left_formal_occurrence_id",
                    edge0["right_formal_occurrence_id"],
                ),
                row.__setitem__(
                    "right_formal_occurrence_id",
                    edge0["left_formal_occurrence_id"],
                ),
            ),
        ),
        reclosed=True,
    )

    negative_id = context["negative_sample"]["row_id"]
    reject(
        "wrong_sign_or_graph_negative_promoted",
        "NO_BIND_EXCLUSION",
        lambda: forged_edge(
            lambda row: row["left_endpoint_evidence_fragment_ids"].append(
                negative_id
            )
        ),
        reclosed=True,
    )
    reject(
        "dsu_credit_on_edge",
        "ZERO_DSU_SCOPE",
        lambda: forged_edge(
            lambda row: row.__setitem__(
                "formal_DSU_rank_reduction_credit", 1
            )
        ),
        reclosed=True,
    )
    reject(
        "component_credit_on_edge",
        "ZERO_DSU_SCOPE",
        lambda: forged_edge(
            lambda row: row.__setitem__("formal_component_union_credit", 1)
        ),
        reclosed=True,
    )
    reject(
        "evidence_fragment_deleted",
        "EDGE_PROVENANCE",
        lambda: forged_edge(
            lambda row: row.__setitem__(
                "left_endpoint_evidence_fragment_ids", []
            ),
            semantic=False,
        ),
        reclosed=True,
    )

    cell0 = candidate_cell["rows"][0]

    def forged_cell(mutate: Callable[[dict[str, Any]], None]) -> None:
        row = dict(cell0)
        row["common_physical_payload_bindings"] = [
            dict(value)
            for value in row["common_physical_payload_bindings"]
        ]
        mutate(row)
        row.pop("row_sha256", None)
        row["row_sha256"] = digest(row)
        closed(row, row["Round296_true_seam_cell_coverage_row_id"])
        validate_cell_row(row)
        ensure(row == expected_cell["rows"][0], "independent exact cell row")

    reject(
        "pair_payload_not_common_to_both_sides",
        "COMMON_PAYLOAD_PAIRING",
        lambda: forged_cell(
            lambda row: row["common_physical_payload_bindings"].append({
                "physical_payload_sha256": "0" * 64,
                "physical_payload": {},
                "left_formal_occurrence_ids": [],
                "right_formal_occurrence_ids": [],
            })
        ),
        reclosed=True,
    )
    reject(
        "negative_cell_endpoint_count",
        "NO_BIND_EXCLUSION",
        lambda: forged_cell(
            lambda row: row.__setitem__(
                "wrong_sign_or_graph_separated_rows_used_as_endpoints", 1
            )
        ),
        reclosed=True,
    )
    reject(
        "nonpositive_exact_cell",
        "EXACT_CELL_GEOMETRY",
        lambda: forged_cell(
            lambda row: row.__setitem__(
                "exact_half_open_ps_cell", ["0", "0", "0", "1"]
            )
        ),
        reclosed=True,
    )

    def removed_repeated_edge() -> None:
        forged = dict(candidate_edge)
        forged["rows"] = list(candidate_edge["rows"][:-1])
        reclose_ledger(
            forged, "Round296_true_seam_occurrence_edge_row_id"
        )
        ensure(
            forged["row_count"] == 48_444,
            "repeated endpoint-pair edge row cannot be deduplicated",
        )

    reject(
        "deduplicate_repeated_endpoint_pair_across_cells",
        "EDGE_MULTIPLICITY",
        removed_repeated_edge,
        reclosed=True,
    )

    def forged_result(
        mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        value = deepcopy(candidate_result)
        mutate(value)
        reclose_result(value)
        payload = dict(value)
        expected_digest = payload.pop("result_sha256")
        ensure(expected_digest == digest(payload), "reclosed forged result")
        ensure(value == expected_result, "independent exact result")

    reject(
        "forged_quotient_count",
        "ZERO_DSU_SCOPE",
        lambda: forged_result(
            lambda value: (
                value["strict_nonpromotion"].__setitem__(
                    "quotient_computed", True
                ),
                value["strict_nonpromotion"].__setitem__(
                    "quotient_component_count", 140_836
                ),
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_raw_fragment_3700",
        "FRAGMENT_CENSUS",
        lambda: forged_result(
            lambda value: value["source_reconstruction_contract"].__setitem__(
                "Round282_strict_terminal_evidence_fragment_count", 3_700
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_fragment_distinct_count",
        "FRAGMENT_DEDUP",
        lambda: forged_result(
            lambda value: value["source_reconstruction_contract"][
                "fragment_raw_vs_formal_atom_dedup_audit"
            ].__setitem__("distinct_formal_endpoint_atom_count", 10_589)
        ),
        reclosed=True,
    )
    reject(
        "preview_used_as_oracle",
        "POST_HOC_PREVIEW",
        lambda: forged_result(
            lambda value: value["source_reconstruction_contract"].__setitem__(
                "preview_used_as_construction_oracle", True
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_edge_count",
        "CENSUS",
        lambda: forged_result(
            lambda value: value["census"].__setitem__(
                "formal_true_seam_edge_count", 48_443
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_pair_count",
        "CENSUS",
        lambda: forged_result(
            lambda value: value["census"].__setitem__(
                "distinct_unordered_endpoint_pair_count", 15_315
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_r285_uncovered_endpoint",
        "R285_NEGATIVE_CELL",
        lambda: forged_result(
            lambda value: value["source_reconstruction_contract"].__setitem__(
                "Round285_uncovered_negative_cells_used_as_edge_endpoints", 1
            )
        ),
        reclosed=True,
    )
    reject(
        "forged_r285_geometry_histogram",
        "R285_SAFE_PAIRING",
        lambda: forged_result(
            lambda value: value["source_reconstruction_contract"][
                "Round285_exact_cell_class_histogram"
            ].__setitem__(
                "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED",
                465,
            )
        ),
        reclosed=True,
    )
    reject(
        "seed_dependence_claim",
        "DETERMINISM",
        lambda: forged_result(
            lambda value: value.__setitem__("seed_affects_output", True)
        ),
        reclosed=True,
    )

    attack_suite = {
        "schema": (
            "cm2.round296.source-g-true-seam-occurrence-edge-ledger-"
            "closure.attack-suite.v1"
        ),
        "status": "PASS_ALL_TARGETED_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "reclosed_attack_count": sum(
            row["fully_reclosed"] for row in attacks
        ),
        "all_attacks_rejected": all(row["rejected"] for row in attacks),
        "attacks": attacks,
    }
    attack_suite["attack_suite_sha256"] = digest(attack_suite)
    return attack_suite


def safe_write(path: Path, payload: bytes) -> None:
    ensure(path.parent.resolve() == HERE.resolve(), f"output HERE-only:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=HERE, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-ledger", type=Path, default=EDGE)
    parser.add_argument("--cell-coverage-ledger", type=Path, default=CELL)
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--verification", type=Path, default=VERIFICATION)
    parser.add_argument("--attack-suite", type=Path, default=ATTACKS)
    parser.add_argument("--seed", default="296173")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    expected_edge, expected_cell, expected_result, context = reconstruct()
    candidate_edge, candidate_cell, candidate_result = validate_candidate(
        arguments.edge_ledger,
        arguments.cell_coverage_ledger,
        arguments.result,
        expected_edge,
        expected_cell,
        expected_result,
        context,
    )
    attack_suite = build_attack_suite(
        expected_edge,
        expected_cell,
        expected_result,
        candidate_edge,
        candidate_cell,
        candidate_result,
        context,
    )
    attack_bytes = canonical(attack_suite)
    verifier_sha = file_sha256(Path(__file__).resolve())
    verification = {
        "schema": (
            "cm2.round296.source-g-true-seam-occurrence-edge-ledger-"
            "closure.independent-verification.v1"
        ),
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND296_TRUE_SEAM_EDGE_LEDGER__"
            "EXACT_3444_CELLS__EXACT_48444_EDGES__ZERO_DSU_CREDIT"
        ),
        "candidate_artifacts": {
            "producer": {
                "filename": PRODUCER.name,
                "file_sha256": PRODUCER_SHA256,
            },
            "edge_ledger": {
                "filename": arguments.edge_ledger.name,
                "file_sha256": hashlib.sha256(
                    context["expected_edge_bytes"]
                ).hexdigest(),
                "schema": EDGE_SCHEMA,
                "row_count": 48_444,
                "rows_sha256": expected_edge["rows_sha256"],
            },
            "cell_coverage_ledger": {
                "filename": arguments.cell_coverage_ledger.name,
                "file_sha256": hashlib.sha256(
                    context["expected_cell_bytes"]
                ).hexdigest(),
                "schema": CELL_SCHEMA,
                "row_count": 3_444,
                "rows_sha256": expected_cell["rows_sha256"],
            },
            "result": {
                "filename": arguments.result.name,
                "file_sha256": hashlib.sha256(
                    context["expected_result_bytes"]
                ).hexdigest(),
                "result_sha256": expected_result["result_sha256"],
            },
        },
        "independent_cacheless_reconstruction": {
            "producer_imported_or_executed": False,
            "candidate_ledgers_read_before_source_reconstruction": False,
            "eight_manifest_packages_byte_pinned": True,
            "true_seam_patch_count": 152,
            "exact_half_open_ps_cell_count": 3_444,
            "formal_true_seam_edge_count": 48_444,
            "distinct_unordered_endpoint_pair_count": 15_316,
            "distinct_occurrence_target_count": 5_784,
            "self_edge_count": 0,
            "full_patch_edge_count": 504,
            "tail_patch_edge_count": 47_940,
            "fragment_raw_vs_formal_atom_dedup_audit":
                context["fragment_audit"],
            "Round295B_source_reference_canonicalization_count": 5_292,
            "Round295B_already_canonical_reference_count": 6_156,
            "every_endpoint_in_Round294_formal_registry_domain": True,
            "wrong_sign_or_graph_negative_endpoint_count": 0,
            "Round285_safe_pairing_cell_class_histogram":
                context["safe_class_histogram"],
            "Round285_safe_pairing_cell_class_area_partition":
                context["safe_class_areas"],
            "Round285_uncovered_negative_endpoint_count": 0,
            "post_hoc_preview_exact_match": True,
            "edge_ledger_object_and_bytes_exact_match": True,
            "cell_ledger_object_and_bytes_exact_match": True,
            "result_object_and_bytes_exact_match": True,
        },
        "strict_input_contract": {
            "HERE_only": True,
            "regular_file_only": True,
            "symlink_rejected": True,
            "hardlink_rejected": True,
            "fifo_and_directory_rejected": True,
            "bounded_file_size": True,
            "duplicate_JSON_keys_rejected": True,
            "floats_nonfinite_and_huge_integers_rejected": True,
            "canonical_result_JSON_required": True,
            "single_member_GZIP_required": True,
            "GZIP_trailing_bytes_rejected": True,
            "bounded_GZIP_expansion": True,
        },
        "formal_scope": {
            "formal_true_seam_edge_credit": 48_444,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "quotient_computed": False,
            "quotient_component_count": None,
            "ordinary_face_edges_consumed": False,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "targeted_attacks": {
            "filename": arguments.attack_suite.name,
            "file_sha256": hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "attack_count": attack_suite["attack_count"],
            "reclosed_attack_count": attack_suite[
                "reclosed_attack_count"
            ],
            "all_attacks_rejected": attack_suite["all_attacks_rejected"],
        },
        "determinism": {
            "seed_affects_output": False,
            "producer_seed_replay_required": True,
            "verifier_seed_replay_required": True,
        },
        "provenance": {
            "verifier_sha256": verifier_sha,
            "Round296_producer_sha256": PRODUCER_SHA256,
            "upstream_producer_imported_or_executed": False,
        },
    }
    verification["verification_sha256"] = digest(verification)
    verification_bytes = canonical(verification)
    if not arguments.no_write:
        safe_write(arguments.attack_suite, attack_bytes)
        safe_write(arguments.verification, verification_bytes)
    print(json.dumps({
        "status": verification["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "verification_file_sha256":
            hashlib.sha256(verification_bytes).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_file_sha256":
            hashlib.sha256(attack_bytes).hexdigest(),
        "attack_count": attack_suite["attack_count"],
        "edge_count": 48_444,
        "cell_count": 3_444,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
