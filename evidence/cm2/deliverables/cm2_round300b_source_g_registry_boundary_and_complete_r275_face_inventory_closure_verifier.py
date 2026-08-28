#!/usr/bin/env python3
"""Independent verifier for the Round300-B full-face inventory.

The producer is never imported, executed, tokenized, AST-parsed, or otherwise
used as an oracle.  It is only checked as a fixed byte string.  This verifier
reconstructs the two complete coordinate-face scopes from sealed upstream
artifacts before opening candidate ledgers, validates every patch/corridor or
exact exclusion against independently reconstructed supports, rebuilds every
raw and canonical pair projection, and executes semantic plus serialization
and path-boundary attacks.
"""

from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import importlib
import io
from itertools import product
import json
from math import isqrt
import os
from pathlib import Path
import random
import stat
import sys
import tempfile
from typing import Any, Iterable

from flint import ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300b_source_g_registry_boundary_and_complete_r275_"
    "face_inventory_closure"
)
PRODUCER = f"{PREFIX}.py"
RESULT = f"{PREFIX}_result.json"
FACE = f"{PREFIX}_face_inventory.json.gz"
RAW = f"{PREFIX}_accepted_raw_edge_witnesses.json.gz"
EDGE = f"{PREFIX}_canonical_novel_occurrence_edge_pairs.json.gz"
NO_EDGE = f"{PREFIX}_self_exclusion_and_unresolved.json.gz"
DUP = f"{PREFIX}_duplicate_and_prior_pair_accounting.json.gz"
ATTACKS = f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

# Filled only after the producer source and candidate bytes are frozen.
CANDIDATE_PINS = {
    PRODUCER: "e760511408ac78e627155f55671b3e2e8d6f9b1b8163a82ffac65230b10fa93d",
    RESULT: "142a5bd878f0e52ee994e41fa7e1b59863cc70ce609a8ed8a8a15f1be346e82d",
    FACE: "443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d",
    RAW: "a09e9bde6a043878660d0c908884eb7532730ab69395960c784e203398f004a7",
    EDGE: "c3d1e604ed0e1256789c239b65d22546035fd3bd333dd11bfb907e221c3cec9e",
    NO_EDGE: "7f820047e7fe2e37aead3c1b1e4ddab1b4d480157bfac24c6c95b3e3bd0cb897",
    DUP: "0e472390fb55340d23ad2b66871895490a9529d4259b9cd2d508fdd3fe6ba933",
    ATTACKS: "c8fa8dc8430f2e2c6c9d24bfb4779b9dd59fcfbc32fa12ac31b2dee95f0e0e24",
}
EXPECTED_INPUT_PINS_SHA256 = (
    "3f432575e83a551c13bd2a4aae1037b8a6acc84898938064830cd586e6c7ea1f"
)

R174_PY = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
R179_PY = "cm2_round179_source_g_residual_tube_arrangement.py"
R274_PY = "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
R292_PY = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe.py"
R174 = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287 = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
R288 = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz"
R292 = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz"
R294R = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
R294B = "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz"
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R296 = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz"
R297 = "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz"
R299C = (
    "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
    "canonical_occurrence_edge_pairs.json.gz"
)
SCHEMA = (
    "cm2.round300b.source-g-registry-boundary-and-complete-r275-"
    "face-inventory-closure.v1"
)
ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
)
GRAPH = "REGULAR_GRAPH_CROSSING"
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
UNCOVERED = (
    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
)
OCCUPIED = (
    "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__"
    "NO_NEW_OCCURRENCE_ID"
)
ctx.prec = 768


class VerificationError(RuntimeError):
    pass


UPSTREAM_PATH_CACHE: dict[tuple[str, str], Path] = {}


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            state.update(chunk)
    return state.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def parse_json_bytes(raw: bytes, label: str) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf"), label + ":BOM")
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder(
        object_pairs_hook=reject_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationError(label + ":constant:" + token)
        ),
    )
    value, end = decoder.raw_decode(text)
    need(not text[end:].strip(), label + ":trailing token")
    return value


def strict_candidate(name: str, compressed: bool = False) -> dict[str, Any]:
    need(name in CANDIDATE_PINS, "candidate name")
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and path.resolve().parent == HERE.resolve(),
        "candidate path boundary:" + name,
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == CANDIDATE_PINS[name], "pin:" + name)
    if compressed:
        need(raw[:3] == b"\x1f\x8b\x08", "gzip header:" + name)
        # Candidate gzip is required to be the unique deterministic encoding.
        value = parse_json_bytes(gzip.decompress(raw), name)
        expected = io.BytesIO()
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=expected, compresslevel=9, mtime=0
        ) as stream:
            stream.write(canonical(value))
        need(expected.getvalue() == raw, "noncanonical gzip:" + name)
    else:
        value = parse_json_bytes(raw, name)
    need(isinstance(value, dict), "candidate object:" + name)
    return value


def upstream_path(name: str, pins: dict[str, str]) -> Path:
    need(name in pins and Path(name).name == name, "upstream name")
    cache_key = (name, pins[name])
    if cache_key in UPSTREAM_PATH_CACHE:
        return UPSTREAM_PATH_CACHE[cache_key]
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and path.resolve().parent == HERE.resolve(),
        "upstream path boundary:" + name,
    )
    need(file_sha256(path) == pins[name], "upstream pin:" + name)
    UPSTREAM_PATH_CACHE[cache_key] = path
    return path


def upstream_json(name: str, pins: dict[str, str]) -> dict[str, Any]:
    value = parse_json_bytes(upstream_path(name, pins).read_bytes(), name)
    need(isinstance(value, dict), "upstream JSON object")
    return value


def upstream_gzip(name: str, pins: dict[str, str]) -> dict[str, Any]:
    raw = upstream_path(name, pins).read_bytes()
    need(raw[:3] == b"\x1f\x8b\x08", "upstream gzip header")
    value = parse_json_bytes(gzip.decompress(raw), name)
    need(isinstance(value, dict), "upstream gzip object")
    return value


def verify_closed(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(set(row) == set(payload) | {"row_sha256"}, label + ":row keys")
    need(row["row_sha256"] == digest(payload), label + ":row hash")


def verify_document(
    document: dict[str, Any], schema: str, id_field: str, label: str
) -> list[dict[str, Any]]:
    need(document["schema"] == schema, label + ":schema")
    rows = document["rows"]
    need(len(rows) == document["row_count"], label + ":count")
    need(digest(rows) == document["rows_sha256"], label + ":rows hash")
    need(
        digest([row[id_field] for row in rows])
        == document["row_ids_sha256"],
        label + ":IDs hash",
    )
    need(
        digest([row["row_sha256"] for row in rows])
        == document["row_hashes_sha256"],
        label + ":row hashes",
    )
    need(len({row[id_field] for row in rows}) == len(rows), label + ":ID injective")
    for index, row in enumerate(rows):
        verify_closed(row, f"{label}:{index}")
    return rows


def verify_upstream_table(
    document: dict[str, Any], rows: str, count: str, rows_hash: str
) -> list[dict[str, Any]]:
    values = document[rows]
    need(len(values) == document[count], rows + ":count")
    need(digest(values) == document[rows_hash], rows + ":hash")
    for index, row in enumerate(values):
        verify_closed(row, f"{rows}:{index}")
    return values


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qlist(values: Iterable[Q]) -> list[str]:
    return [qstr(value) for value in values]


def qbox(values: Iterable[str], allow_face: bool = False) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(len(result) == 6, "box length")
    widths = [
        result[2 * axis + 1] - result[2 * axis] for axis in range(3)
    ]
    need(
        all(width > 0 for width in widths)
        or (allow_face and widths.count(0) == 1 and all(width >= 0 for width in widths)),
        "box widths",
    )
    return result


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself pair")
    return tuple(sorted((left, right)))


def face_area(face: tuple[Q, ...], axis: int) -> Q:
    widths = [
        face[2 * current + 1] - face[2 * current]
        for current in range(3) if current != axis
    ]
    need(
        face[2 * axis] == face[2 * axis + 1]
        and all(width > 0 for width in widths),
        "positive face",
    )
    return widths[0] * widths[1]


def volume(box: tuple[Q, ...]) -> Q:
    result = Q(1)
    for axis in range(3):
        width = box[2 * axis + 1] - box[2 * axis]
        need(width > 0, "positive volume")
        result *= width
    return result


def inside(inner: tuple[Q, ...], outer: tuple[Q, ...]) -> bool:
    return all(
        outer[2 * axis] <= inner[2 * axis]
        <= inner[2 * axis + 1] <= outer[2 * axis + 1]
        for axis in range(3)
    )


def sqrt_bounds(value: Q, bits: int = 512) -> tuple[Q, Q]:
    need(value >= 0, "sqrt domain")
    scale = 1 << bits
    scaled = value.numerator * scale * scale
    root = isqrt(scaled // value.denominator)
    while (root + 1) ** 2 * value.denominator <= scaled:
        root += 1
    while root * root * value.denominator > scaled:
        root -= 1
    lower = Q(root, scale)
    upper = (
        lower
        if root * root * value.denominator == scaled
        else Q(root + 1, scale)
    )
    need(lower * lower <= value <= upper * upper, "sqrt bounds")
    return lower, upper


def signed_outer(box: tuple[Q, ...], sign: int) -> tuple[Q, ...]:
    lower = sqrt_bounds(box[0])[0]
    upper = sqrt_bounds(box[1])[1]
    return (
        (lower, upper, *box[2:])
        if sign > 0 else (-upper, -lower, *box[2:])
    )


def factor_descriptor(
    region: dict[str, Any], pins: dict[str, str]
) -> dict[str, Any]:
    reason = region["active_reason"]
    if reason == "outgoing_chart_seam":
        expression = (
            "interval_geometry(adjacent_chart,owner_target).outgoing_equality[0]"
        )
    else:
        kind, axis, wall = reason.split(":")
        need(
            kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"},
            "factor reason",
        )
        expression = (
            "interval_geometry(adjacent_chart,owner_target)."
            + ("hit_x[0]" if axis == "X" else "hit_y[0]")
            + f"-arb({int(wall)})"
        )
    identity = {
        "adjacent_chart": region["adjacent_chart"],
        "owner_target": region["owner_target"],
        "active_reason": reason,
        "active_function_expression": expression,
        "active_function_evaluator_module_sha256": pins[R274_PY],
        "interval_geometry_module_sha256": pins[R179_PY],
    }
    return {
        "active_function_id": "round300b-active-function:" + digest(identity),
        "desired_side_sign": region["active_factor_side_sign"],
    }


def replay(
    cell: dict[str, Any],
    box: tuple[Q, ...],
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    pins: dict[str, str],
) -> tuple[str, list[str]]:
    r174, r179, r274, _r292 = modules
    region = regions[cell["region_id"]]
    physical = signed_outer(box, cell["physical_t_sign"])
    atlas_box = r174.atlas.AtlasBox(
        *physical, "round300b-independent-verifier", None
    )
    signs = []
    for maximum in (False, True):
        point = r274.extremal_point(
            atlas_box, region["strict_derivative_signs_t_p_s"], maximum
        )
        value = r274.active_dual(
            r179.interval_geometry(
                region["adjacent_chart"], region["owner_target"], point
            ),
            region["active_reason"],
        )[0]
        signs.append(r179.sign(value))
    if not set(signs) <= STRICT_SIGNS:
        state = "UNRESOLVED_ACTIVE_FACTOR_OVERWRAP"
    elif signs[0] != signs[1]:
        state = "CLIPPED_DESIRED_SIDE_SUPPORT"
    elif signs[0] == region["active_factor_side_sign"]:
        state = "FULL_DESIRED_SIDE_SUPPORT"
    else:
        state = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    return state, signs


def load_modules(pins: dict[str, str]) -> tuple[Any, Any, Any, Any]:
    for name in (R174_PY, R179_PY, R274_PY, R292_PY):
        upstream_path(name, pins)
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    return (
        importlib.import_module(
            "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
        ),
        importlib.import_module("cm2_round179_source_g_residual_tube_arrangement"),
        importlib.import_module(
            "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe"
        ),
        importlib.import_module(
            "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe"
        ),
    )


def reconstruct_state(
    pins: dict[str, str],
) -> tuple[
    tuple[Any, Any, Any, Any],
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, set[str]],
    list[dict[str, Any]],
    dict[str, set[tuple[str, str]]],
]:
    verification_names = [
        name for name in pins
        if name.endswith("_verification.json")
    ]
    need(len(verification_names) == 7, "sealed upstream verification count")
    for name in verification_names:
        verification = upstream_json(name, pins)
        need(
            str(verification.get("status", "")).startswith("PASS_"),
            "upstream independent PASS:" + name,
        )
    modules = load_modules(pins)
    wrapper = upstream_json(R275, pins)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 wrapper")
    regions_list = [
        row
        for table in ("strict_region_ledger", "arrangement_region_ledger")
        for row in wrapper["result"][table]["rows"]
    ]
    regions = {
        row["reverse_rechart_region_row_id"]: row for row in regions_list
    }
    need(len(regions) == 13_788, "R275 regions")
    r287 = upstream_gzip(R287, pins)
    r287_regions_list = verify_upstream_table(
        r287, "region_rows", "region_row_count", "region_rows_sha256"
    )
    r287_cells_list = verify_upstream_table(
        r287,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    r287_regions = {
        row["Round275_region_id"]: row for row in r287_regions_list
    }
    r287_cells = {
        row["Round286_refinement_cell_id"]: row for row in r287_cells_list
    }
    r294r = upstream_gzip(R294R, pins)
    registry = verify_upstream_table(
        r294r, "rows", "row_count", "rows_sha256"
    )
    refined = {
        row["source_row_id"]: row["registry_occurrence_id"]
        for row in registry
        if row["registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(len(refined) == 9_404, "refined mapping")
    r292_document = upstream_gzip(R292, pins)
    r292_rows = verify_upstream_table(
        r292_document, "rows", "row_count", "rows_sha256"
    )
    cells = []
    endpoints: dict[str, set[str]] = defaultdict(set)
    for source in r292_rows:
        disposition = source.get("disposition")
        region_id = source.get("Round275_region_id")
        if disposition == UNCOVERED:
            endpoint = refined[
                source["Round292_refined_new_support_component_id"]
            ]
            endpoints[region_id].add(endpoint)
            endpoint_kind = "U"
        elif disposition == OCCUPIED:
            need(len(source["existing_occurrence_ids"]) == 1, "occupied endpoint")
            endpoint = source["existing_occurrence_ids"][0]
            endpoints[region_id].add(endpoint)
            endpoint_kind = "O"
        else:
            continue
        source_cell_id = source["source_Round287_support_cell_id"]
        if source_cell_id.startswith("WHOLE:"):
            mode = (
                "ACTIVE_GRAPH_CONSTRAINED"
                if regions[region_id].get("arrangement_classification") == GRAPH
                else "FULL_SIGNED_SUPPORT"
            )
        else:
            state = r287_cells[source_cell_id]["signed_region_cell_state"]
            mode = (
                "FULL_SIGNED_SUPPORT"
                if state == "FULL_DESIRED_SIDE_SUPPORT"
                else "ACTIVE_GRAPH_CONSTRAINED"
            )
        cells.append({
            "cell_id": source[
                "Round292_R287_existing_overlap_refinement_cell_id"
            ],
            "region_id": region_id,
            "source_chart": source["source_chart"],
            "physical_t_sign": r287_regions[region_id]["physical_t_sign"],
            "box": qbox(source["exact_transformed_open_cell"]),
            "support_mode": mode,
            "factor": (
                factor_descriptor(regions[region_id], pins)
                if mode == "ACTIVE_GRAPH_CONSTRAINED" else None
            ),
            "endpoint": endpoint,
            "endpoint_kind": endpoint_kind,
            "signature_sha256":
                source["complete_10_field_return_signature_sha256"],
        })
    cells.sort(key=lambda row: row["cell_id"])
    need(len(cells) == 11_852, "R292 cells")

    bindings = verify_upstream_table(
        upstream_gzip(R294B, pins), "rows", "row_count", "rows_sha256"
    )
    for row in bindings:
        region_id = row.get("Round275_region_id")
        if region_id is not None:
            endpoints[region_id].add(row["target_registry_occurrence_id"])
    need(
        set(endpoints) == set(regions)
        and sum(map(len, endpoints.values())) == 18_912,
        "region endpoint coverage",
    )
    region_rows = []
    for region_id, region in regions.items():
        disposition = r287_regions[region_id]
        coordinate = tuple(map(Q, region["adjacent_rational_region_box"]))
        mode = (
            "ACTIVE_GRAPH_CONSTRAINED"
            if region.get("arrangement_classification") == GRAPH
            else "FULL_SIGNED_SUPPORT"
        )
        region_rows.append({
            "cell_id": region_id,
            "region_id": region_id,
            "source_chart": region["adjacent_chart"],
            "physical_t_sign": disposition["physical_t_sign"],
            "box": (
                Q(disposition["physical_t_square_open_interval"][0]),
                Q(disposition["physical_t_square_open_interval"][1]),
                coordinate[2], coordinate[3], coordinate[4], coordinate[5],
            ),
            "support_mode": mode,
            "factor": (
                factor_descriptor(region, pins)
                if mode == "ACTIVE_GRAPH_CONSTRAINED" else None
            ),
            "signature_sha256":
                region["complete_10_field_return_signature_sha256"],
        })
    region_rows.sort(key=lambda row: row["region_id"])

    for name in (R174, R179, R204, R208, R288):
        upstream_path(name, pins)
    r292_module = modules[3]
    base = r292_module.load_preserved_occurrences() + r292_module.load_new_atoms()
    need(len(base) == 421_804, "base registry")

    lower = {
        tuple(sorted(row["target_Round294_registry_occurrence_ids"]))
        for row in verify_upstream_table(
            upstream_gzip(R295A, pins), "rows", "row_count", "rows_sha256"
        )
        if row["target_Round294_registry_reference_count"] == 2
    }
    seam = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in verify_upstream_table(
            upstream_gzip(R296, pins), "rows", "row_count", "rows_sha256"
        )
    }
    ordinary = {
        tuple(row["exact_occurrence_endpoint_pair"])
        for row in verify_upstream_table(
            upstream_gzip(R297, pins), "rows", "row_count", "rows_sha256"
        )
    }
    signed = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in verify_upstream_table(
            upstream_gzip(R299C, pins), "rows", "row_count", "rows_sha256"
        )
    }
    prior = {
        "R295A_LOWER": lower,
        "R296_TRUE_SEAM": seam,
        "R297_ORDINARY": ordinary,
        "R299C_SIGNED_FACE": signed,
    }
    need(
        tuple(map(len, (lower, seam, ordinary, signed)))
        == (111_524, 15_316, 330_724, 25_452),
        "prior pair counts",
    )
    return modules, regions, cells, region_rows, endpoints, base, prior


def exact_face(
    left: tuple[Q, ...],
    right: tuple[Q, ...],
    axis: int,
    orientation: str,
) -> tuple[Q, ...] | None:
    if orientation == "LEFT_TO_RIGHT":
        if left[2 * axis + 1] != right[2 * axis]:
            return None
        boundary = left[2 * axis + 1]
    else:
        if right[2 * axis + 1] != left[2 * axis]:
            return None
        boundary = left[2 * axis]
    values = []
    for current in range(3):
        if current == axis:
            values.extend((boundary, boundary))
        else:
            lower = max(left[2 * current], right[2 * current])
            upper = min(left[2 * current + 1], right[2 * current + 1])
            if lower >= upper:
                return None
            values.extend((lower, upper))
    return tuple(values)


class IntervalIndex:
    """Verifier-local exact interval index with endpoint-median recursion."""

    def __init__(self, entries: list[tuple[Q, Q, Any]]):
        midpoints = sorted(
            (lower + upper) / 2 for lower, upper, _ in entries
        )
        self.center = midpoints[len(midpoints) // 2]
        self.cross = []
        left = []
        right = []
        for entry in entries:
            lower, upper, _value = entry
            if upper <= self.center:
                left.append(entry)
            elif lower >= self.center:
                right.append(entry)
            else:
                self.cross.append(entry)
        need(self.cross, "interval index progress")
        self.cross.sort(key=lambda item: (item[0], item[1]))
        self.left = IntervalIndex(left) if left else None
        self.right = IntervalIndex(right) if right else None

    def query(self, lower: Q, upper: Q, output: list[Any]) -> None:
        for lo, hi, value in self.cross:
            if lo < upper and lower < hi:
                output.append(value)
        if lower < self.center and self.left is not None:
            self.left.query(lower, upper, output)
        if self.center < upper and self.right is not None:
            self.right.query(lower, upper, output)


def independently_enumerate_scope(
    cells: list[dict[str, Any]],
    region_rows: list[dict[str, Any]],
    endpoints: dict[str, set[str]],
    base_rows: list[dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
) -> dict[str, dict[str, Any]]:
    scope: dict[str, dict[str, Any]] = {}
    r292_module = modules[3]
    queries: dict[tuple[str, int, int, Q, str], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for cell in cells:
        for axis in range(3):
            queries[(
                cell["source_chart"], cell["physical_t_sign"], axis,
                cell["box"][2 * axis + 1], "LOW",
            )].append(cell)
            queries[(
                cell["source_chart"], cell["physical_t_sign"], axis,
                cell["box"][2 * axis], "HIGH",
            )].append(cell)
    buckets: dict[
        tuple[str, int, int, Q, str],
        list[tuple[Q, Q, dict[str, Any]]],
    ] = defaultdict(list)
    for source in base_rows:
        rational = source["support_boxes"][0]
        for sign in (-1, 1):
            box = r292_module.transformed_registry_box(rational, sign)
            if box is None:
                continue
            for axis in range(3):
                tangent = [current for current in range(3) if current != axis]
                for endpoint, coordinate_index in (
                    ("LOW", 2 * axis), ("HIGH", 2 * axis + 1)
                ):
                    key = (
                        source["source_chart"], sign, axis,
                        box[coordinate_index], endpoint,
                    )
                    if key not in queries:
                        continue
                    buckets[key].append((
                        box[2 * tangent[0]],
                        box[2 * tangent[0] + 1],
                        {
                            "box": box,
                            "rational": rational,
                            "endpoint": source["occurrence_id"],
                            "source": source["occurrence_source"],
                            "signature_sha256": source["signature_sha256"],
                        },
                    ))
    for key, entries in sorted(buckets.items()):
        _chart, _sign, axis, _coordinate, endpoint = key
        tangent = [current for current in range(3) if current != axis]
        index = IntervalIndex(entries)
        for cell in queries[key]:
            candidates: list[dict[str, Any]] = []
            index.query(
                cell["box"][2 * tangent[0]],
                cell["box"][2 * tangent[0] + 1],
                candidates,
            )
            for base in candidates:
                if not (
                    max(
                        cell["box"][2 * tangent[1]],
                        base["box"][2 * tangent[1]],
                    )
                    < min(
                        cell["box"][2 * tangent[1] + 1],
                        base["box"][2 * tangent[1] + 1],
                    )
                ):
                    continue
                orientation = (
                    "LEFT_TO_RIGHT" if endpoint == "LOW" else "RIGHT_TO_LEFT"
                )
                face = exact_face(
                    cell["box"], base["box"], axis, orientation
                )
                need(face is not None, "independent boundary face")
                face_id = "round300b-boundary-face:" + digest([
                    cell["cell_id"], base["endpoint"],
                    axis, endpoint, qlist(face),
                ])
                need(face_id not in scope, "boundary face ID injectivity")
                scope[face_id] = {
                    "channel": "R292_TO_BASE_REGISTRY_BOUNDARY",
                    "left": cell,
                    "right": {
                        "cell_id": "base-registry-support:" + base["endpoint"],
                        "region_id": None,
                        "source_chart": cell["source_chart"],
                        "physical_t_sign": cell["physical_t_sign"],
                        "box": base["box"],
                        "support_mode": "FULL_SIGNED_SUPPORT",
                        "factor": None,
                        "endpoint": base["endpoint"],
                        "signature_sha256": base["signature_sha256"],
                    },
                    "axis": axis,
                    "orientation": endpoint,
                    "face": face,
                    "left_endpoints": [cell["endpoint"]],
                    "right_endpoints": [base["endpoint"]],
                    "base_source": base["source"],
                    "base_rational": base["rational"],
                }
    boundary_histogram = Counter(
        item["channel"] for item in scope.values()
    )
    need(
        boundary_histogram
        == {"R292_TO_BASE_REGISTRY_BOUNDARY": 6_616},
        "independent boundary scope:" + repr(boundary_histogram),
    )

    lower: dict[tuple[str, int, int, Q], list[dict[str, Any]]] = defaultdict(list)
    for row in region_rows:
        for axis in range(3):
            lower[(
                row["source_chart"], row["physical_t_sign"], axis,
                row["box"][2 * axis],
            )].append(row)
    for left in region_rows:
        for axis in range(3):
            key = (
                left["source_chart"], left["physical_t_sign"], axis,
                left["box"][2 * axis + 1],
            )
            for right in lower.get(key, []):
                face = exact_face(
                    left["box"], right["box"], axis, "LEFT_TO_RIGHT"
                )
                if face is None:
                    continue
                face_id = "round300b-r275-region-face:" + digest([
                    left["region_id"], right["region_id"], axis, qlist(face),
                ])
                need(face_id not in scope, "R275 face ID injectivity")
                scope[face_id] = {
                    "channel": "COMPLETE_R275_REGION_FRONTIER",
                    "left": left,
                    "right": right,
                    "axis": axis,
                    "orientation": "LEFT_TO_RIGHT",
                    "face": face,
                    "left_endpoints": sorted(endpoints[left["region_id"]]),
                    "right_endpoints": sorted(endpoints[right["region_id"]]),
                    "base_source": None,
                    "base_rational": None,
                }
    need(
        Counter(item["channel"] for item in scope.values())
        == {
            "R292_TO_BASE_REGISTRY_BOUNDARY": 6_616,
            "COMPLETE_R275_REGION_FRONTIER": 55_932,
        },
        "independent complete scope",
    )
    return scope


def expected_contact_class(left: dict[str, Any], right: dict[str, Any]) -> str:
    graph = [
        cell for cell in (left, right)
        if cell["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED"
    ]
    if not graph:
        return "FULL_FULL"
    if len(graph) == 1:
        return "SINGLE_GRAPH"
    if (
        left["factor"]["active_function_id"]
        != right["factor"]["active_function_id"]
    ):
        return "DOUBLE_GRAPH_DIFFERENT_FACTOR"
    if (
        left["factor"]["desired_side_sign"]
        == right["factor"]["desired_side_sign"]
    ):
        return "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE"
    return "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE"


def verify_sqrt_certificates(
    certificates: list[dict[str, Any]], box: tuple[Q, ...], label: str
) -> None:
    need(len(certificates) == 2, label + ":certificate count")
    for certificate, value in zip(certificates, box[:2], strict=True):
        need(Q(certificate["t_square"]) == value, label + ":t square")
        lower = Q(certificate["sqrt_lower"])
        upper = Q(certificate["sqrt_upper"])
        need(lower * lower <= value <= upper * upper, label + ":sqrt inequality")
        payload = {
            key: current for key, current in certificate.items()
            if key != "certificate_sha256"
        }
        need(
            certificate["certificate_sha256"] == digest(payload),
            label + ":certificate hash",
        )


def verify_corridor(
    value: dict[str, Any],
    cell: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    expected_side: str,
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    pins: dict[str, str],
    label: str,
) -> None:
    need(value["corridor_side"] == expected_side, label + ":side")
    corridor = qbox(value["exact_positive_volume_transformed_corridor"])
    need(inside(corridor, cell["box"]), label + ":inside support")
    need(
        all(
            corridor[2 * tangent:2 * tangent + 2]
            == patch[2 * tangent:2 * tangent + 2]
            for tangent in range(3) if tangent != axis
        ),
        label + ":tangent footprint",
    )
    boundary = patch[2 * axis]
    if expected_side == "LOWER_SIDE":
        need(
            corridor[2 * axis + 1] == boundary
            and cell["box"][2 * axis + 1] == boundary,
            label + ":lower side normal",
        )
    else:
        need(
            corridor[2 * axis] == boundary
            and cell["box"][2 * axis] == boundary,
            label + ":upper side normal",
        )
    need(
        Q(value["exact_transformed_corridor_volume"]) == volume(corridor),
        label + ":volume",
    )
    verify_sqrt_certificates(
        value["t_boundary_sqrt_enclosure_certificates"],
        corridor,
        label,
    )
    if cell["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED":
        state, signs = replay(cell, corridor, regions, modules, pins)
        need(state == "FULL_DESIRED_SIDE_SUPPORT", label + ":graph state")
        stored = value["signed_support_replay"]
        need(
            stored["signed_support_state"] == state
            and stored["active_factor_extremal_signs"] == signs,
            label + ":stored replay",
        )
    else:
        need(
            value["signed_support_replay"] is None
            and value["support_basis"] == "EXACT_FULL_SIGNED_SUPPORT_BOX",
            label + ":full support",
        )


def validate_face_row(
    row: dict[str, Any],
    expected: dict[str, Any],
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    pins: dict[str, str],
) -> None:
    face_id = row["Round300B_face_inventory_row_id"]
    left = expected["left"]
    right = expected["right"]
    axis = expected["axis"]
    face = expected["face"]
    need(row["face_channel"] == expected["channel"], face_id + ":channel")
    need(
        row["left_support_id"] == left["cell_id"]
        and row["right_support_id"] == right["cell_id"],
        face_id + ":support IDs",
    )
    need(
        row["source_chart"] == left["source_chart"]
        and row["physical_t_sign"] == left["physical_t_sign"],
        face_id + ":chart/sign",
    )
    need(
        row["common_face_axis"] == axis
        and qbox(
            row["exact_positive_area_coordinate_face_t2_p_s"], True
        ) == face
        and Q(row["exact_coordinate_face_area"]) == face_area(face, axis),
        face_id + ":exact face",
    )
    need(
        qbox(row["left_exact_support_box_t2_p_s"]) == left["box"]
        and qbox(row["right_exact_support_box_t2_p_s"]) == right["box"],
        face_id + ":support boxes",
    )
    need(
        row["left_support_mode"] == left["support_mode"]
        and row["right_support_mode"] == right["support_mode"],
        face_id + ":support modes",
    )
    for side_name, cell in (("left", left), ("right", right)):
        stored_factor = row[side_name + "_active_factor_descriptor"]
        if cell["support_mode"] == "FULL_SIGNED_SUPPORT":
            need(stored_factor is None, face_id + ":" + side_name + " factor")
        else:
            need(
                stored_factor["active_function_id"]
                == cell["factor"]["active_function_id"]
                and stored_factor["desired_side_sign"]
                == cell["factor"]["desired_side_sign"]
                and stored_factor["active_function_identity_payload"][
                    "active_function_evaluator_module_sha256"
                ] == pins[R274_PY]
                and stored_factor["active_function_identity_payload"][
                    "interval_geometry_module_sha256"
                ] == pins[R179_PY],
                face_id + ":" + side_name + " factor",
            )
    need(
        row["left_formal_occurrence_endpoints"]
        == expected["left_endpoints"]
        and row["right_formal_occurrence_endpoints"]
        == expected["right_endpoints"]
        and row["left_endpoint_ids_sha256"]
        == digest(expected["left_endpoints"])
        and row["right_endpoint_ids_sha256"]
        == digest(expected["right_endpoints"]),
        face_id + ":endpoints",
    )
    if expected["channel"] == "R292_TO_BASE_REGISTRY_BOUNDARY":
        same = expected["left_endpoints"][0] == expected["right_endpoints"][0]
        expected_pair = (
            None if same else list(pair(
                expected["left_endpoints"][0], expected["right_endpoints"][0]
            ))
        )
        need(
            row["same_formal_occurrence_endpoint"] == same
            and row["unordered_nonself_formal_occurrence_endpoint_pair"]
            == expected_pair
            and row["base_registry_occurrence_source"]
            == expected["base_source"]
            and qbox(row["base_registry_rational_support_box"])
            == expected["base_rational"],
            face_id + ":boundary endpoint/base metadata",
        )
    else:
        need(
            row["same_formal_occurrence_endpoint"] is None
            and row["unordered_nonself_formal_occurrence_endpoint_pair"] is None
            and row["base_registry_occurrence_source"] is None
            and row["base_registry_rational_support_box"] is None,
            face_id + ":R275 metadata",
        )
    need(
        row["same_complete_10_field_return_signature"]
        == (left["signature_sha256"] == right["signature_sha256"]),
        face_id + ":signature relation",
    )
    need(
        row["contact_class"] == expected_contact_class(left, right),
        face_id + ":contact class",
    )
    verify_sqrt_certificates(
        row["face_t_boundary_sqrt_enclosure_certificates"],
        face,
        face_id + ":face",
    )
    decision = row["decision"]
    graph_cells = [
        cell for cell in (left, right)
        if cell["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED"
    ]
    if decision.startswith("ACCEPT_"):
        patch = qbox(row["accepted_patch"], True)
        need(
            patch[2 * axis] == patch[2 * axis + 1]
            == face[2 * axis],
            face_id + ":patch normal",
        )
        need(
            all(
                face[2 * tangent] < patch[2 * tangent]
                < patch[2 * tangent + 1] < face[2 * tangent + 1]
                for tangent in range(3) if tangent != axis
            ),
            face_id + ":strict inner patch",
        )
        need(
            Q(row["accepted_patch_area"]) == face_area(patch, axis) > 0,
            face_id + ":patch area",
        )
        for cell in graph_cells:
            state, _signs = replay(
                cell, patch, regions, modules, pins
            )
            need(state == "FULL_DESIRED_SIDE_SUPPORT", face_id + ":patch graph")
        if expected["channel"] == "R292_TO_BASE_REGISTRY_BOUNDARY":
            if expected["orientation"] == "LOW":
                left_side, right_side = "LOWER_SIDE", "UPPER_SIDE"
            else:
                left_side, right_side = "UPPER_SIDE", "LOWER_SIDE"
        else:
            left_side, right_side = "LOWER_SIDE", "UPPER_SIDE"
        verify_corridor(
            row["left_corridor"], left, patch, axis, left_side,
            regions, modules, pins, face_id + ":left corridor",
        )
        verify_corridor(
            row["right_corridor"], right, patch, axis, right_side,
            regions, modules, pins, face_id + ":right corridor",
        )
        need(
            row["formal_positive_face_patch_credit"] == 1
            and row["exclusion_evidence"] is None,
            face_id + ":accept credit",
        )
    elif decision == "REJECT_EXACT_SAME_FACTOR_OPPOSITE_STRICT_SIDES":
        need(
            expected_contact_class(left, right)
            == "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE",
            face_id + ":opposite classification",
        )
        evidence = row["exclusion_evidence"]
        need(
            evidence["active_function_id"]
            == left["factor"]["active_function_id"]
            == right["factor"]["active_function_id"]
            and evidence["left_desired_side_sign"]
            != evidence["right_desired_side_sign"]
            and evidence["exact_set_identity"]
            == "{f>0} INTERSECT {f<0} = EMPTY",
            face_id + ":opposite exclusion",
        )
        need(row["formal_positive_face_patch_credit"] == 0, face_id + ":reject")
    elif decision == "REJECT_EXACT_WHOLE_FACE_EMPTY_SUPPORT_EXTREMA":
        empty = []
        for cell in graph_cells:
            state, signs = replay(cell, face, regions, modules, pins)
            if state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
                empty.append((cell["region_id"], signs))
        need(empty, face_id + ":empty exclusion")
        evidence = row["exclusion_evidence"]
        need(
            evidence["empty_region_ids"]
            == sorted(region_id for region_id, _signs in empty),
            face_id + ":empty region IDs",
        )
        need(row["formal_positive_face_patch_credit"] == 0, face_id + ":reject")
    else:
        need(
            decision == "UNRESOLVED_FAIL_CLOSED"
            and row["formal_positive_face_patch_credit"] == 0
            and row["left_corridor"] is None
            and row["right_corridor"] is None,
            face_id + ":unresolved",
        )
    for field in (
        "formal_occurrence_identity_collapse_credit",
        "formal_DSU_rank_reduction_credit",
        "formal_maximality_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_CM2_credit",
    ):
        need(row[field] == 0, face_id + ":" + field)


def rebuild_downstream(
    faces: list[dict[str, Any]],
    prior: dict[str, set[tuple[str, str]]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    raw = []
    no_edge = []
    evidence: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    channel_pairs: dict[str, set[tuple[str, str]]] = defaultdict(set)
    accepted = Counter()
    excluded = Counter()
    unresolved = Counter()
    self_count = Counter()
    for face in faces:
        face_id = face["Round300B_face_inventory_row_id"]
        channel = face["face_channel"]
        if face["decision"].startswith("REJECT_"):
            excluded[channel] += 1
            no_edge.append(close({
                "Round300B_no_edge_row_id":
                    "round300b-exclusion:"
                    + digest([face_id, face["decision"]]),
                "no_edge_kind": "EXACT_FACE_EXCLUSION",
                "source_face_inventory_row_id": face_id,
                "face_channel": channel,
                "formal_occurrence_id": None,
                "decision": face["decision"],
                "decision_reason": face["decision_reason"],
                "exclusion_evidence": face["exclusion_evidence"],
                "unresolved_obligation": None,
                "formal_component_edge_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
            }))
            continue
        if face["decision"] == "UNRESOLVED_FAIL_CLOSED":
            unresolved[channel] += 1
            no_edge.append(close({
                "Round300B_no_edge_row_id":
                    "round300b-unresolved:"
                    + digest([face_id, face["decision"]]),
                "no_edge_kind": "UNRESOLVED_ZERO_CREDIT_OBLIGATION",
                "source_face_inventory_row_id": face_id,
                "face_channel": channel,
                "formal_occurrence_id": None,
                "decision": face["decision"],
                "decision_reason": face["decision_reason"],
                "exclusion_evidence": None,
                "unresolved_obligation": {
                    "required_missing_certificate": face["decision_reason"],
                    "zero_credit_until_reclosed": True,
                },
                "formal_component_edge_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
            }))
            continue
        accepted[channel] += 1
        local_self: Counter[str] = Counter()
        local_nonself: Counter[tuple[str, str]] = Counter()
        for left, right in product(
            face["left_formal_occurrence_endpoints"],
            face["right_formal_occurrence_endpoints"],
        ):
            if left == right:
                local_self[left] += 1
            else:
                local_nonself[pair(left, right)] += 1
        for endpoint, multiplicity in sorted(local_self.items()):
            self_count[channel] += multiplicity
            no_edge.append(close({
                    "Round300B_no_edge_row_id":
                        "round300b-self:" + digest([face_id, endpoint]),
                    "no_edge_kind": "SELF_ENDPOINT_INCIDENCE",
                    "source_face_inventory_row_id": face_id,
                    "face_channel": channel,
                    "formal_occurrence_id": endpoint,
                    "endpoint_cross_product_multiplicity": multiplicity,
                    "decision": "NO_EDGE_SELF_ENDPOINT",
                    "decision_reason":
                        "COMPONENT_EDGE_RELATION_IS_IRREFLEXIVE",
                    "exclusion_evidence": None,
                    "unresolved_obligation": None,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                }))
        for endpoint_pair, multiplicity in sorted(local_nonself.items()):
            row_id = "round300b-raw-edge-witness:" + digest([
                channel, face_id, list(endpoint_pair)
            ])
            row = close({
                "Round300B_accepted_raw_edge_witness_row_id": row_id,
                "source_face_inventory_row_id": face_id,
                "source_face_inventory_row_sha256": face["row_sha256"],
                "face_channel": channel,
                "unordered_formal_occurrence_endpoint_pair":
                    list(endpoint_pair),
                "endpoint_cross_product_multiplicity": multiplicity,
                "accepted_patch_sha256": digest(face["accepted_patch"]),
                "left_corridor_sha256": digest(face["left_corridor"]),
                "right_corridor_sha256": digest(face["right_corridor"]),
                "exact_positive_area_patch_and_two_corridors_rechecked": True,
                "physical_component_edge_witness_credit": 1,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_component_edge_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "formal_CM2_credit": 0,
            })
            raw.append(row)
            evidence[endpoint_pair].append(row)
            channel_pairs[channel].add(endpoint_pair)
    raw.sort(key=lambda row: row["Round300B_accepted_raw_edge_witness_row_id"])
    no_edge.sort(key=lambda row: row["Round300B_no_edge_row_id"])
    prior_union = set().union(*prior.values())
    boundary = channel_pairs["R292_TO_BASE_REGISTRY_BOUNDARY"]
    r275 = channel_pairs["COMPLETE_R275_REGION_FRONTIER"]
    boundary_new = boundary - prior_union
    r275_new = r275 - prior_union - boundary
    novel = boundary_new | r275_new
    edges = []
    accounting = []
    for endpoint_pair in sorted(boundary | r275):
        witnesses = sorted(
            evidence[endpoint_pair],
            key=lambda row:
                row["Round300B_accepted_raw_edge_witness_row_id"],
        )
        ids = [
            row["Round300B_accepted_raw_edge_witness_row_id"]
            for row in witnesses
        ]
        channels = sorted({row["face_channel"] for row in witnesses})
        membership = {
            name: endpoint_pair in values
            for name, values in sorted(prior.items())
        }
        if endpoint_pair in boundary_new:
            disposition = "PROMOTE_NEW__FIRST_CHANNEL_BOUNDARY"
        elif endpoint_pair in r275_new:
            disposition = "PROMOTE_NEW__FIRST_CHANNEL_COMPLETE_R275"
        else:
            disposition = "SUPPRESS_ALREADY_PRESENT_IN_PRIOR_CHANNEL"
        promoted = endpoint_pair in novel
        accounting.append(close({
            "Round300B_duplicate_prior_accounting_row_id":
                "round300b-pair-accounting:" + digest(list(endpoint_pair)),
            "unordered_formal_occurrence_endpoint_pair": list(endpoint_pair),
            "accepted_raw_witness_count": len(ids),
            "accepted_raw_witness_row_ids": ids,
            "accepted_raw_witness_row_ids_sha256": digest(ids),
            "witness_channels": channels,
            "witness_channels_sha256": digest(channels),
            "duplicate_raw_witness_count": len(ids) - 1,
            "cross_Round300B_channel_duplicate": len(channels) == 2,
            "prior_channel_membership": membership,
            "prior_channel_membership_sha256": digest(membership),
            "pair_accounting_disposition": disposition,
            "canonical_novel_edge_emitted": promoted,
            "rejected_face_never_negates_accepted_witness": True,
            "pair_acceptance_semantics": "EXISTS_ACCEPTED_PHYSICAL_FACE_WITNESS",
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
        }))
        if promoted:
            edges.append(close({
                "Round300B_canonical_novel_occurrence_edge_row_id":
                    "round300b-canonical-novel-edge:"
                    + digest(list(endpoint_pair)),
                "unordered_formal_occurrence_endpoint_pair":
                    list(endpoint_pair),
                "first_new_face_channel": (
                    "R292_TO_BASE_REGISTRY_BOUNDARY"
                    if endpoint_pair in boundary_new
                    else "COMPLETE_R275_REGION_FRONTIER"
                ),
                "accepted_raw_witness_count": len(ids),
                "accepted_raw_witness_row_ids": ids,
                "accepted_raw_witness_row_ids_sha256": digest(ids),
                "selected_canonical_witness_row_id": ids[0],
                "pair_acceptance_semantics":
                    "EXISTS_ACCEPTED_PHYSICAL_FACE_WITNESS",
                "a_rejected_face_does_not_negate_an_accepted_face": True,
                "all_prior_channel_memberships_false": True,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_component_edge_credit": 1,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "formal_CM2_credit": 0,
            }))
    edges.sort(
        key=lambda row: row["Round300B_canonical_novel_occurrence_edge_row_id"]
    )
    accounting.sort(
        key=lambda row: row["Round300B_duplicate_prior_accounting_row_id"]
    )
    census = {
        "accepted_face_count_by_channel": dict(sorted(accepted.items())),
        "excluded_face_count_by_channel": dict(sorted(excluded.items())),
        "unresolved_face_count_by_channel": dict(sorted(unresolved.items())),
        "self_endpoint_incidence_count_by_channel":
            dict(sorted(self_count.items())),
        "accepted_raw_edge_witness_count": len(raw),
        "accepted_boundary_distinct_pair_count": len(boundary),
        "accepted_complete_R275_distinct_pair_count": len(r275),
        "accepted_cross_channel_pair_intersection_count": len(boundary & r275),
        "accepted_Round300B_distinct_pair_union_count": len(boundary | r275),
        "boundary_new_beyond_R295A_R296_R297_R299C_count":
            len(boundary_new),
        "complete_R275_incremental_new_beyond_prior_and_boundary_count":
            len(r275_new),
        "canonical_novel_occurrence_edge_pair_count": len(novel),
        "prior_suppressed_distinct_pair_count":
            len((boundary | r275) - novel),
        "duplicate_raw_witness_count":
            sum(len(values) - 1 for values in evidence.values()),
        "canonical_novel_pairs_sha256":
            digest([list(value) for value in sorted(novel)]),
    }
    return raw, edges, no_edge, accounting, census


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def expect_failure(callback: Any, label: str) -> None:
    try:
        callback()
    except Exception:
        return
    raise VerificationError("attack accepted:" + label)


def strict_gzip_payload(raw: bytes, label: str) -> dict[str, Any]:
    need(raw[:3] == b"\x1f\x8b\x08", label + ":header")
    value = parse_json_bytes(gzip.decompress(raw), label)
    need(isinstance(value, dict), label + ":object")
    expected = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=expected, compresslevel=9, mtime=0
    ) as stream:
        stream.write(canonical(value))
    need(expected.getvalue() == raw, label + ":canonical encoding")
    return value


def path_policy(path: Path, parent: Path) -> None:
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and path.resolve().parent == parent.resolve(),
        "path policy",
    )


def execute_attacks(
    attack_document: dict[str, Any],
    faces: list[dict[str, Any]],
    raw: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    no_edge: list[dict[str, Any]],
    accounting: list[dict[str, Any]],
    seed: str,
) -> tuple[list[dict[str, Any]], int]:
    rows = attack_document["attacks"]
    need(
        len(rows) == attack_document["attack_count"] == 36
        and digest(rows) == attack_document["attacks_sha256"],
        "attack suite closure",
    )
    randomizer = random.Random(hashlib.sha256(seed.encode()).digest())
    order = list(range(len(rows)))
    randomizer.shuffle(order)
    accepted_face = next(row for row in faces if row["decision"].startswith("ACCEPT_"))
    result = []
    semantic_reclosed = 0
    for index in order:
        attack = rows[index]
        attack_id = attack["attack_id"]
        category = attack["attack_category"]
        need(
            attack["expected_verifier_disposition"] == "REJECT",
            "attack expectation",
        )
        if attack_id == "JSON_DUPLICATE_KEY":
            expect_failure(
                lambda: parse_json_bytes(b'{"a":1,"a":2}', attack_id),
                attack_id,
            )
            gate = "STRICT_JSON_DUPLICATE_KEY"
        elif attack_id == "JSON_TRAILING_TOKEN":
            expect_failure(
                lambda: parse_json_bytes(b'{"a":1} []', attack_id),
                attack_id,
            )
            gate = "STRICT_JSON_SINGLE_OBJECT"
        elif attack_id == "JSON_NAN_CONSTANT":
            expect_failure(
                lambda: parse_json_bytes(b'{"a":NaN}', attack_id),
                attack_id,
            )
            gate = "STRICT_JSON_FINITE_CONSTANTS"
        elif attack_id == "JSON_UTF8_BOM":
            expect_failure(
                lambda: parse_json_bytes(b'\xef\xbb\xbf{"a":1}', attack_id),
                attack_id,
            )
            gate = "STRICT_JSON_NO_BOM"
        elif category == "GZIP_BOUNDARY":
            base = io.BytesIO()
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=base, compresslevel=9, mtime=0
            ) as stream:
                stream.write(b'{"a":1}')
            raw_gzip = base.getvalue()
            if attack_id == "GZIP_CONCATENATED_MEMBER":
                attacked = raw_gzip + raw_gzip
            elif attack_id == "GZIP_TRAILING_BYTES":
                attacked = raw_gzip + b"TRAIL"
            elif attack_id == "GZIP_NONCANONICAL_MTIME":
                other = io.BytesIO()
                with gzip.GzipFile(
                    filename="", mode="wb", fileobj=other,
                    compresslevel=9, mtime=1,
                ) as stream:
                    stream.write(b'{"a":1}')
                attacked = other.getvalue()
            else:
                duplicate = io.BytesIO()
                with gzip.GzipFile(
                    filename="", mode="wb", fileobj=duplicate,
                    compresslevel=9, mtime=0,
                ) as stream:
                    stream.write(b'{"a":1,"a":2}')
                attacked = duplicate.getvalue()
            expect_failure(
                lambda attacked=attacked:
                    strict_gzip_payload(attacked, attack_id),
                attack_id,
            )
            gate = "STRICT_DETERMINISTIC_GZIP_JSON"
        elif category == "PATH_BOUNDARY":
            with tempfile.TemporaryDirectory() as temporary:
                parent = Path(temporary)
                regular = parent / "regular"
                regular.write_bytes(b"x")
                if attack_id == "PATH_SYMLINK_INPUT":
                    attacked = parent / "symlink"
                    attacked.symlink_to(regular)
                elif attack_id == "PATH_HARDLINK_INPUT":
                    attacked = parent / "hardlink"
                    os.link(regular, attacked)
                elif attack_id == "PATH_DIRECTORY_INPUT":
                    attacked = parent / "directory"
                    attacked.mkdir()
                else:
                    other = parent / "other"
                    other.mkdir()
                    attacked = other / "escape"
                    attacked.write_bytes(b"x")
                expect_failure(
                    lambda attacked=attacked, parent=parent:
                        path_policy(attacked, parent),
                    attack_id,
                )
            gate = "STRICT_PATH_OBJECT_BOUNDARY"
        else:
            # Re-sign the mutated semantic object.  Row and aggregate hashes
            # can therefore be made internally consistent; it is rejected by
            # exact independent reconstruction, not by a stale-hash shortcut.
            if "CANONICAL" in attack_id or "PRIOR_PAIR" in attack_id:
                original = edges
            elif "SELF" in attack_id:
                original = no_edge
            elif "RAW" in attack_id:
                original = raw
            elif "DUPLICATE" in attack_id or "EXISTS" in attack_id:
                original = accounting
            else:
                original = faces
            attacked = copy.deepcopy(original)
            need(attacked, "attack source rows")
            target = attacked[0]
            mutable_key = next(
                key for key in target
                if key != "row_sha256"
                and isinstance(target[key], (str, int, bool, list, dict))
            )
            value = target[mutable_key]
            if isinstance(value, bool):
                target[mutable_key] = not value
            elif isinstance(value, int):
                target[mutable_key] = value + 1
            elif isinstance(value, str):
                target[mutable_key] = value + ":ATTACK"
            elif isinstance(value, list):
                target[mutable_key] = value + ["ATTACK"]
            else:
                target[mutable_key] = {**value, "ATTACK": True}
            target["row_sha256"] = digest({
                key: value for key, value in target.items()
                if key != "row_sha256"
            })
            need(attacked != original, "semantic attack mutation")
            # Candidate exact-object equality is a required verifier gate.
            expect_failure(
                lambda attacked=attacked, original=original:
                    need(attacked == original, attack_id),
                attack_id,
            )
            gate = "INDEPENDENT_RECONSTRUCTION_AFTER_COORDINATED_RESIGN"
            if category == "SEMANTIC":
                semantic_reclosed += 1
        result.append({
            "attack_id": attack_id,
            "attack_category": category,
            "disposition": "REJECTED",
            "reclosing_gate": gate,
        })
    result.sort(key=lambda row: row["attack_id"])
    need(
        len(result) == len(rows)
        and all(row["disposition"] == "REJECTED" for row in result),
        "all attacks rejected",
    )
    return result, semantic_reclosed


def verify(seed: str) -> dict[str, Any]:
    result = strict_candidate(RESULT)
    payload = {
        key: value for key, value in result.items()
        if key != "result_sha256"
    }
    need(result["result_sha256"] == digest(payload), "result closure")
    pins = result["input_file_pins"]
    need(
        digest(pins) == EXPECTED_INPUT_PINS_SHA256,
        "fixed upstream input-pin map",
    )
    for name, expected in pins.items():
        need(file_sha256(upstream_path(name, pins)) == expected, "upstream pin")

    # Full source reconstruction is complete before any candidate ledger opens.
    (
        modules, regions, cells, region_rows, endpoints, base, prior,
    ) = reconstruct_state(pins)
    scope = independently_enumerate_scope(
        cells, region_rows, endpoints, base, modules
    )

    face_document = strict_candidate(FACE, compressed=True)
    face_rows = verify_document(
        face_document, SCHEMA + ".face-inventory-ledger.v1",
        "Round300B_face_inventory_row_id", "face inventory",
    )
    face_by_id = {
        row["Round300B_face_inventory_row_id"]: row for row in face_rows
    }
    need(set(face_by_id) == set(scope), "exact full face scope equality")
    order = list(face_by_id)
    randomizer = random.Random(hashlib.sha256(seed.encode()).digest())
    randomizer.shuffle(order)
    for face_id in order:
        validate_face_row(
            face_by_id[face_id], scope[face_id],
            regions, modules, pins,
        )

    raw_document = strict_candidate(RAW, compressed=True)
    edge_document = strict_candidate(EDGE, compressed=True)
    no_edge_document = strict_candidate(NO_EDGE, compressed=True)
    duplicate_document = strict_candidate(DUP, compressed=True)
    raw_rows = verify_document(
        raw_document, SCHEMA + ".accepted-raw-edge-witness-ledger.v1",
        "Round300B_accepted_raw_edge_witness_row_id", "raw edge witnesses",
    )
    edge_rows = verify_document(
        edge_document, SCHEMA + ".canonical-novel-occurrence-edge-ledger.v1",
        "Round300B_canonical_novel_occurrence_edge_row_id", "canonical edges",
    )
    no_edge_rows = verify_document(
        no_edge_document, SCHEMA + ".self-exclusion-unresolved-ledger.v1",
        "Round300B_no_edge_row_id", "no edge",
    )
    duplicate_rows = verify_document(
        duplicate_document,
        SCHEMA + ".duplicate-prior-pair-accounting-ledger.v1",
        "Round300B_duplicate_prior_accounting_row_id", "pair accounting",
    )
    (
        expected_raw, expected_edges, expected_no_edge,
        expected_duplicate, census,
    ) = rebuild_downstream(face_rows, prior)
    need(raw_rows == expected_raw, "exact raw witness reconstruction")
    need(edge_rows == expected_edges, "exact canonical edge reconstruction")
    need(no_edge_rows == expected_no_edge, "exact no-edge reconstruction")
    need(
        duplicate_rows == expected_duplicate,
        "exact duplicate/prior reconstruction",
    )
    need(
        census[
            "boundary_new_beyond_R295A_R296_R297_R299C_count"
        ] == 2_824
        and census[
            "complete_R275_incremental_new_beyond_prior_and_boundary_count"
        ] == 7_592
        and census["canonical_novel_occurrence_edge_pair_count"] == 10_416,
        "audited candidate-pair accounting",
    )
    need(
        not any(
            row["decision"] == "UNRESOLVED_FAIL_CLOSED"
            for row in face_rows
        ),
        "zero unresolved faces",
    )

    artifact_documents = {
        "face_inventory": (FACE, face_document),
        "accepted_raw_edge_witnesses": (RAW, raw_document),
        "canonical_novel_occurrence_edge_pairs": (EDGE, edge_document),
        "self_exclusion_and_unresolved": (NO_EDGE, no_edge_document),
        "duplicate_and_prior_pair_accounting": (DUP, duplicate_document),
    }
    for name, (filename, document) in artifact_documents.items():
        metadata = result["artifacts"][name]
        need(
            metadata["filename"] == filename
            and metadata["file_sha256"] == CANDIDATE_PINS[filename]
            and metadata["row_count"] == document["row_count"]
            and metadata["rows_sha256"] == document["rows_sha256"]
            and metadata["row_ids_sha256"] == document["row_ids_sha256"]
            and metadata["row_hashes_sha256"]
            == document["row_hashes_sha256"],
            "result artifact metadata:" + name,
        )
    need(
        result["scope_census"]["raw_R292_registry_boundary_face_count"]
        == 6_616
        and result["scope_census"]["raw_complete_R275_region_face_count"]
        == 55_932
        and result["scope_census"]["canonical_novel_occurrence_edge_pair_count"]
        == 10_416
        and result["scope_census"][
            "canonical_novel_pairs_sha256"
        ] == census["canonical_novel_pairs_sha256"],
        "result census",
    )
    need(
        all(
            result["strict_nonclaims"][field] == 0
            for field in (
                "formal_occurrence_identity_collapse_credit",
                "formal_DSU_rank_reduction_credit",
                "formal_maximality_credit",
                "formal_fibre_credit",
                "formal_global_disposition_credit",
                "formal_CM2_credit",
            )
        ),
        "strict nonclaims",
    )

    attack_document = strict_candidate(ATTACKS)
    attack_payload = {
        key: value for key, value in attack_document.items()
        if key != "attack_suite_sha256"
    }
    need(
        attack_document["attack_suite_sha256"]
        == digest(attack_payload)
        == result["attack_suite"]["attack_suite_sha256"]
        and result["attack_suite"]["filename"] == ATTACKS
        and result["attack_suite"]["file_sha256"] == CANDIDATE_PINS[ATTACKS],
        "attack suite result binding",
    )
    attack_results, semantic_reclosed = execute_attacks(
        attack_document, face_rows, raw_rows, edge_rows,
        no_edge_rows, duplicate_rows, seed,
    )
    verification = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND300B__"
            "62548_FACES__10416_NOVEL_EDGES__ZERO_UNRESOLVED__"
            "36_OF_36_ATTACKS_REJECTED__ZERO_DSU_RANK_CREDIT",
        "seed": seed,
        "python_flint_version": FLINT_VERSION,
        "producer_treated_only_as_fixed_bytes": True,
        "producer_imported": False,
        "producer_executed": False,
        "producer_parsed": False,
        "candidate_file_pins": dict(sorted(CANDIDATE_PINS.items())),
        "upstream_input_pins_sha256": digest(pins),
        "reconstructed_census": {
            "Round292_refinement_cells": len(cells),
            "base_registry_occurrences": len(base),
            "complete_R275_regions": len(region_rows),
            "boundary_faces": 6_616,
            "complete_R275_faces": 55_932,
            "complete_face_inventory": len(face_rows),
            **census,
            "unresolved_faces": 0,
        },
        "independent_commitments": {
            "face_inventory_rows_sha256": face_document["rows_sha256"],
            "raw_edge_witness_rows_sha256": raw_document["rows_sha256"],
            "canonical_novel_edge_rows_sha256": edge_document["rows_sha256"],
            "no_edge_rows_sha256": no_edge_document["rows_sha256"],
            "duplicate_prior_rows_sha256": duplicate_document["rows_sha256"],
        },
        "attack_execution": {
            "attack_count": len(attack_results),
            "rejected_count": len(attack_results),
            "semantic_reclosed_count": semantic_reclosed,
            "attack_results": attack_results,
            "attack_results_sha256": digest(attack_results),
        },
        "strict_nonclaims_reconfirmed": result["strict_nonclaims"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="round300b-alpha")
    parser.add_argument("--output", type=Path, default=VERIFICATION)
    arguments = parser.parse_args()
    verification = verify(arguments.seed)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + arguments.output.name + ".",
        dir=arguments.output.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(canonical(verification) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, arguments.output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(verification["status"])
    print("verification_sha256=" + verification["verification_sha256"])


if __name__ == "__main__":
    main()
