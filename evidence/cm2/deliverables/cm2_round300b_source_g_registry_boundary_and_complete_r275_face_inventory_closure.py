#!/usr/bin/env python3
"""Round300-B formal full-face inventory for the two remaining face frontiers.

This builder reconstructs, from byte-pinned sealed upstream artifacts:

* every R292-refinement-cell to base-registry support-box boundary face; and
* every common coordinate face among all complete R275 regions.

A coordinate face is promoted only when an exact rational positive-area
guided patch and exact positive-volume corridors on both sides are present.
Active graph factors are replayed on both the patch and the relevant
corridors.  Exact empty-factor and same-factor/opposite-side exclusions are
retained.  Self incidences and all duplicate/prior-channel suppressions are
explicit.  Pair acceptance is existential.

The earlier Round299C-boundary and Round299D diagnostic programs and ledgers
are deliberately neither imported nor read.  The Round299C *signed-face
promotion pair ledger* is used only as a prior-channel deduplication input.

No occurrence identity, DSU rank, maximality, fibre, disposition, or CM2
credit is issued here.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import importlib
import io
from itertools import product
import json
from math import isqrt
import os
from pathlib import Path
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
RESULT = HERE / f"{PREFIX}_result.json"
FACE_LEDGER = HERE / f"{PREFIX}_face_inventory.json.gz"
RAW_LEDGER = HERE / f"{PREFIX}_accepted_raw_edge_witnesses.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_canonical_novel_occurrence_edge_pairs.json.gz"
NO_EDGE_LEDGER = HERE / f"{PREFIX}_self_exclusion_and_unresolved.json.gz"
DUP_LEDGER = HERE / f"{PREFIX}_duplicate_and_prior_pair_accounting.json.gz"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"

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

SEAL_FILES = {
    "cm2_round275_source_g_complete_reverse_rechart_materialization_manifest.sha256":
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_verification.json":
        "130d61804d1251ac84e14546034331d8a071d13910b28f7f46b46f5ebe4c3f65",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_manifest.sha256":
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_verification.json":
        "c0ad4d3e229a1e21cb5b4f4144575df7f5eaf88d7fc8a6960967ab4c1db515a3",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256":
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verification.json":
        "7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_verification.json":
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_manifest.sha256":
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_verification.json":
        "8ec51d83459f2eac3389054b0c08a7c646973d2eac4addb7447cce6210d8b4d5",
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_manifest.sha256":
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_verification.json":
        "74ef0c5cb3fe52cce8295fffc1a8b1af0c2f9e38e7bf02cbd5db923b6d6dcdb5",
}

PINS = {
    R174_PY: "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R179_PY: "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R274_PY: "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R292_PY: "69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c",
    R174: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R275: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287: "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R288: "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    R292: "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294R: "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294B: "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296: "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297: "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
    R299C: "e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1",
    **SEAL_FILES,
}

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
MAX_FACE_DEPTH = 32
MAX_CORRIDOR_DEPTH = 32
SQRT_CONSTRUCTION_BITS = 256
SQRT_REPLAY_BITS = 512
ctx.prec = 768


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
        raise RuntimeError(label)


def guarded(name: str) -> Path:
    need(name in PINS and Path(name).name == name, "known direct input")
    path = HERE / name
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), "regular input:" + name)
    need(not path.is_symlink() and info.st_nlink == 1, "unaliased input:" + name)
    need(path.resolve().parent == HERE.resolve(), "input parent:" + name)
    need(file_sha256(path) == PINS[name], "input pin:" + name)
    return path


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def read_json(name: str) -> dict[str, Any]:
    raw = guarded(name).read_bytes()
    need(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM:" + name)
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder(
        object_pairs_hook=reject_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError("JSON constant:" + token)
        ),
    )
    value, end = decoder.raw_decode(text)
    need(not text[end:].strip(), "JSON trailing token:" + name)
    need(isinstance(value, dict), "JSON object:" + name)
    return value


def read_gzip(name: str) -> dict[str, Any]:
    raw = guarded(name).read_bytes()
    need(raw[:3] == b"\x1f\x8b\x08", "gzip header:" + name)
    plain = gzip.decompress(raw)
    text = plain.decode("utf-8")
    decoder = json.JSONDecoder(
        object_pairs_hook=reject_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError("JSON constant:" + token)
        ),
    )
    value, end = decoder.raw_decode(text)
    need(not text[end:].strip(), "gzip JSON trailing token:" + name)
    need(isinstance(value, dict), "gzip JSON object:" + name)
    return value


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_closed(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(set(row) == set(payload) | {"row_sha256"}, label + ":row keys")
    need(row["row_sha256"] == digest(payload), label + ":row digest")


def verify_table(
    document: dict[str, Any],
    rows_key: str,
    count_key: str,
    hash_key: str,
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(len(rows) == document[count_key], rows_key + ":count")
    need(digest(rows) == document[hash_key], rows_key + ":digest")
    for index, row in enumerate(rows):
        verify_closed(row, f"{rows_key}:{index}")
    return rows


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qlist(values: Iterable[Q]) -> list[str]:
    return [qstr(value) for value in values]


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive box",
    )
    return result


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself pair")
    return tuple(sorted((left, right)))


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, compresslevel=9, mtime=0
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def ledger(schema: str, rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    return {
        "schema": schema,
        "status": "PASS_CLOSED_LEDGER",
        "row_count": len(rows),
        "rows": rows,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_sha256": True,
    }


def emit_gzip(path: Path, document: dict[str, Any]) -> dict[str, Any]:
    payload = deterministic_gzip_bytes(document)
    atomic(path, payload)
    return {
        "filename": path.name,
        "file_sha256": hashlib.sha256(payload).hexdigest(),
        "row_count": document["row_count"],
        "rows_sha256": document["rows_sha256"],
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
    }


def rational_square_root(value: Q) -> Q | None:
    need(value >= 0, "sqrt nonnegative")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if (
        numerator * numerator == value.numerator
        and denominator * denominator == value.denominator
    ):
        return Q(numerator, denominator)
    return None


def sqrt_dyadic_bounds(value: Q, bits: int) -> tuple[Q, Q]:
    need(value >= 0 and bits > 0, "sqrt dyadic domain")
    scale = 1 << bits
    scaled = value.numerator * scale * scale
    quotient = scaled // value.denominator
    root = isqrt(quotient)
    while (root + 1) ** 2 * value.denominator <= scaled:
        root += 1
    while root * root * value.denominator > scaled:
        root -= 1
    lower = Q(root, scale)
    exact = root * root * value.denominator == scaled
    upper = lower if exact else Q(root + 1, scale)
    need(
        lower * lower <= value <= upper * upper
        and (lower == upper or lower * lower < value < upper * upper),
        "sqrt dyadic enclosure",
    )
    return lower, upper


def sqrt_certificate(value: Q, bits: int) -> dict[str, Any]:
    lower, upper = sqrt_dyadic_bounds(value, bits)
    exact = rational_square_root(value)
    payload = {
        "t_square": qstr(value),
        "sqrt_enclosure_bits": bits,
        "sqrt_lower": qstr(lower),
        "sqrt_upper": qstr(upper),
        "lower_square_le_t_square": True,
        "t_square_le_upper_square": True,
        "strict_when_not_rational_square": exact is None,
        "exact_rational_sqrt": None if exact is None else qstr(exact),
    }
    payload["certificate_sha256"] = digest(payload)
    return payload


def strict_square_between(lower: Q, upper: Q) -> Q:
    need(0 <= lower < upper, "strict square interval")
    bits = SQRT_CONSTRUCTION_BITS
    while True:
        left = sqrt_dyadic_bounds(lower, bits)[1]
        right = sqrt_dyadic_bounds(upper, bits)[0]
        if left < right:
            point = (left + right) / 2
            result = point * point
            need(lower < result < upper, "strict square result")
            return result
        bits *= 2
        need(bits <= 4096, "sqrt separation")


def t_certificates(box: tuple[Q, ...]) -> list[dict[str, Any]]:
    result = [sqrt_certificate(value, SQRT_REPLAY_BITS) for value in box[:2]]
    need(
        all(
            Q(item["sqrt_lower"]) ** 2
            <= Q(item["t_square"])
            <= Q(item["sqrt_upper"]) ** 2
            for item in result
        ),
        "t certificates",
    )
    return result


def signed_physical_outer(
    box: tuple[Q, ...], physical_t_sign: int
) -> tuple[tuple[Q, ...], list[dict[str, Any]]]:
    need(physical_t_sign in {-1, 1}, "physical t sign")
    certificates = t_certificates(box)
    lower = Q(certificates[0]["sqrt_lower"])
    upper = Q(certificates[1]["sqrt_upper"])
    t_interval = (lower, upper) if physical_t_sign > 0 else (-upper, -lower)
    result = (*t_interval, *box[2:])
    need(
        all(result[2 * axis] <= result[2 * axis + 1] for axis in range(3)),
        "physical outer order",
    )
    return result, certificates


def face_area(face: tuple[Q, ...], axis: int) -> Q:
    widths = [
        face[2 * current + 1] - face[2 * current]
        for current in range(3)
        if current != axis
    ]
    need(len(widths) == 2 and all(width > 0 for width in widths), "face area")
    return widths[0] * widths[1]


def volume(box: tuple[Q, ...]) -> Q:
    result = Q(1)
    for axis in range(3):
        width = box[2 * axis + 1] - box[2 * axis]
        need(width > 0, "positive volume")
        result *= width
    return result


def common_face(
    left: tuple[Q, ...],
    right: tuple[Q, ...],
    axis: int,
    orientation: str = "LEFT_TO_RIGHT",
) -> tuple[Q, ...] | None:
    need(orientation in {"LEFT_TO_RIGHT", "RIGHT_TO_LEFT"}, "face orientation")
    if orientation == "LEFT_TO_RIGHT":
        if left[2 * axis + 1] != right[2 * axis]:
            return None
        boundary = left[2 * axis + 1]
    else:
        if right[2 * axis + 1] != left[2 * axis]:
            return None
        boundary = left[2 * axis]
    values: list[Q] = []
    for current in range(3):
        if current == axis:
            values.extend((boundary, boundary))
        else:
            lower = max(left[2 * current], right[2 * current])
            upper = min(left[2 * current + 1], right[2 * current + 1])
            if not lower < upper:
                return None
            values.extend((lower, upper))
    return tuple(values)


def factor_descriptor(region: dict[str, Any]) -> dict[str, Any]:
    need(region.get("arrangement_classification") == GRAPH, "graph region")
    reason = region["active_reason"]
    if reason == "outgoing_chart_seam":
        expression = (
            "interval_geometry(adjacent_chart,owner_target).outgoing_equality[0]"
        )
    else:
        kind, axis, wall = reason.split(":")
        need(
            kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"},
            "active wall factor",
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
        "active_function_evaluator_module_sha256": PINS[R274_PY],
        "interval_geometry_module_sha256": PINS[R179_PY],
    }
    provenance = {
        "source_chart": region["source_chart"],
        "source_guard_row_id": region["source_guard_row_id"],
        "parent_id": region["parent_id"],
        "exact_coordinate_identity": region["exact_coordinate_identity"],
        "adjacent_cover_refinement_path":
            region["adjacent_cover_refinement_path"],
    }
    function_id = "round300b-active-function:" + digest(identity)
    return {
        "active_function_id": function_id,
        "factor_id": function_id,
        "active_function_identity_payload": identity,
        "provenance_descriptor": provenance,
        "desired_side_sign": region["active_factor_side_sign"],
        "strict_derivative_signs_t_p_s":
            region["strict_derivative_signs_t_p_s"],
    }


def active_factor_replay(
    cell: dict[str, Any],
    transformed_box: tuple[Q, ...],
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    r174, r179, r274, _r292 = modules
    region_id = cell["region_id"]
    sign = cell["physical_t_sign"]
    key = (region_id, transformed_box, sign)
    if key in cache:
        return cache[key]
    region = regions[region_id]
    physical_box, certificates = signed_physical_outer(transformed_box, sign)
    atlas_box = r174.atlas.AtlasBox(
        *physical_box, "round300b-independent-guided-patch", None
    )
    signs = []
    for want_maximum in (False, True):
        point = r274.extremal_point(
            atlas_box, region["strict_derivative_signs_t_p_s"], want_maximum
        )
        value = r274.active_dual(
            r179.interval_geometry(
                region["adjacent_chart"], region["owner_target"], point
            ),
            region["active_reason"],
        )[0]
        signs.append(r179.sign(value))
    descriptor = factor_descriptor(region)
    if not set(signs) <= STRICT_SIGNS:
        state = "UNRESOLVED_ACTIVE_FACTOR_OVERWRAP"
    elif signs[0] != signs[1]:
        state = "CLIPPED_DESIRED_SIDE_SUPPORT"
    elif signs[0] == region["active_factor_side_sign"]:
        state = "FULL_DESIRED_SIDE_SUPPORT"
    else:
        state = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    result = {
        "region_id": region_id,
        "active_function_id": descriptor["active_function_id"],
        "desired_side_sign": region["active_factor_side_sign"],
        "active_factor_extremal_signs": signs,
        "signed_support_state": state,
        "outer_rational_signed_physical_box": qlist(physical_box),
        "outer_box_contains_exact_algebraic_sqrt_boundaries": True,
        "t_boundary_sqrt_enclosure_certificates": certificates,
        "t_boundary_sqrt_enclosures_sha256": digest(certificates),
    }
    cache[key] = result
    return result


def load_modules() -> tuple[Any, Any, Any, Any]:
    for name in (R174_PY, R179_PY, R274_PY, R292_PY):
        guarded(name)
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


def load_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result")
    result = wrapper["result"]
    rows = [
        row
        for table in ("strict_region_ledger", "arrangement_region_ledger")
        for row in result[table]["rows"]
    ]
    need(len(rows) == 13_788, "R275 region census")
    by_id = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(by_id) == len(rows), "R275 region IDs")
    return by_id


def load_r287() -> tuple[
    dict[str, dict[str, Any]], dict[str, dict[str, Any]]
]:
    document = read_gzip(R287)
    region_rows = verify_table(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    cell_rows = verify_table(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    need(len(region_rows) == 13_788 and len(cell_rows) == 7_616, "R287 census")
    return (
        {row["Round275_region_id"]: row for row in region_rows},
        {row["Round286_refinement_cell_id"]: row for row in cell_rows},
    )


def load_refined_occurrence_map() -> dict[str, str]:
    document = read_gzip(R294R)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result = {
        row["source_row_id"]: row["registry_occurrence_id"]
        for row in rows
        if row["registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(len(result) == 9_404 and len(set(result.values())) == 9_404, "R294 map")
    return result


def inherited_mode(
    source_cell_id: str,
    region_id: str,
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
) -> str:
    if source_cell_id.startswith("WHOLE:"):
        need(source_cell_id == "WHOLE:" + region_id, "whole cell identity")
        return (
            "ACTIVE_GRAPH_CONSTRAINED"
            if regions[region_id].get("arrangement_classification") == GRAPH
            else "FULL_SIGNED_SUPPORT"
        )
    source = r287_cells[source_cell_id]
    need(source["Round275_region_id"] == region_id, "R287 cell region")
    if source["signed_region_cell_state"] == "FULL_DESIRED_SIDE_SUPPORT":
        return "FULL_SIGNED_SUPPORT"
    need(
        source["signed_region_cell_state"] == "CLIPPED_DESIRED_SIDE_SUPPORT"
        and regions[region_id].get("arrangement_classification") == GRAPH,
        "graph constrained cell",
    )
    return "ACTIVE_GRAPH_CONSTRAINED"


def load_r292_cells(
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
    refined: dict[str, str],
    source_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []
    for source in source_rows:
        disposition = source.get("disposition")
        if disposition not in {UNCOVERED, OCCUPIED}:
            continue
        region_id = source["Round275_region_id"]
        component_id = source["Round292_refined_new_support_component_id"]
        if disposition == UNCOVERED:
            need(
                source["existing_occurrence_ids"] == []
                and component_id in refined,
                "uncovered endpoint",
            )
            endpoint = refined[component_id]
            endpoint_kind = "U"
        else:
            need(
                component_id is None
                and source["existing_occurrence_occupancy_count"] == 1
                and len(source["existing_occurrence_ids"]) == 1,
                "occupied endpoint",
            )
            endpoint = source["existing_occurrence_ids"][0]
            endpoint_kind = "O"
        source_cell_id = source["source_Round287_support_cell_id"]
        mode = inherited_mode(
            source_cell_id, region_id, regions, r287_regions, r287_cells
        )
        result.append({
            "cell_id": source[
                "Round292_R287_existing_overlap_refinement_cell_id"
            ],
            "region_id": region_id,
            "source_chart": source["source_chart"],
            "physical_t_sign": r287_regions[region_id]["physical_t_sign"],
            "box": qbox(source["exact_transformed_open_cell"]),
            "endpoint_occurrence_id": endpoint,
            "endpoint_kind": endpoint_kind,
            "support_mode": mode,
            "factor": factor_descriptor(regions[region_id])
                if mode == "ACTIVE_GRAPH_CONSTRAINED" else None,
            "signature_sha256":
                source["complete_10_field_return_signature_sha256"],
        })
    result.sort(key=lambda row: row["cell_id"])
    need(
        len(result) == 11_852
        and Counter(row["endpoint_kind"] for row in result)
        == {"U": 10_252, "O": 1_600},
        "R292 exact cell census",
    )
    return result


def load_region_rows(
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []
    for region_id, region in regions.items():
        disposition = r287_regions[region_id]
        coordinate = tuple(map(Q, region["adjacent_rational_region_box"]))
        mode = (
            "ACTIVE_GRAPH_CONSTRAINED"
            if region.get("arrangement_classification") == GRAPH
            else "FULL_SIGNED_SUPPORT"
        )
        result.append({
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
            "factor": factor_descriptor(region)
                if mode == "ACTIVE_GRAPH_CONSTRAINED" else None,
            "signature_sha256":
                region["complete_10_field_return_signature_sha256"],
        })
    result.sort(key=lambda row: row["region_id"])
    need(len(result) == 13_788, "transformed R275 region census")
    return result


def load_region_endpoints(
    regions: dict[str, dict[str, Any]],
    refined: dict[str, str],
    r292_rows: list[dict[str, Any]],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in r292_rows:
        if row.get("disposition") == UNCOVERED:
            result[row["Round275_region_id"]].add(
                refined[row["Round292_refined_new_support_component_id"]]
            )
        elif row.get("disposition") == OCCUPIED:
            result[row["Round275_region_id"]].update(
                row["existing_occurrence_ids"]
            )
    for row in verify_table(
        read_gzip(R294B), "rows", "row_count", "rows_sha256"
    ):
        region_id = row.get("Round275_region_id")
        if region_id is not None:
            result[region_id].add(row["target_registry_occurrence_id"])
    need(set(result) == set(regions), "R275 endpoint coverage")
    histogram = Counter(len(result[region_id]) for region_id in regions)
    need(
        histogram == {
            1: 11_208, 2: 1_680, 3: 268, 4: 232,
            5: 220, 6: 76, 10: 88, 11: 16,
        }
        and sum(map(len, result.values())) == 18_912,
        "R275 endpoint incidence census",
    )
    return result


def load_base_registry(
    modules: tuple[Any, Any, Any, Any],
) -> list[dict[str, Any]]:
    _r174, _r179, _r274, r292 = modules
    for name in (R174, R179, R204, R208, R288):
        guarded(name)
    rows = r292.load_preserved_occurrences() + r292.load_new_atoms()
    need(
        len(rows) == 421_804
        and Counter(row["occurrence_source"] for row in rows)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
            "ROUND288_NEW_ATOM_CANDIDATE": 295_336,
        }
        and all(len(row["support_boxes"]) == 1 for row in rows),
        "base registry census",
    )
    return rows


def load_prior_pairs() -> dict[str, set[tuple[str, str]]]:
    lower = {
        tuple(sorted(row["target_Round294_registry_occurrence_ids"]))
        for row in verify_table(
            read_gzip(R295A), "rows", "row_count", "rows_sha256"
        )
        if row["target_Round294_registry_reference_count"] == 2
    }
    seam = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in verify_table(
            read_gzip(R296), "rows", "row_count", "rows_sha256"
        )
    }
    ordinary = {
        tuple(row["exact_occurrence_endpoint_pair"])
        for row in verify_table(
            read_gzip(R297), "rows", "row_count", "rows_sha256"
        )
    }
    signed = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in verify_table(
            read_gzip(R299C), "rows", "row_count", "rows_sha256"
        )
    }
    need(
        len(lower) == 111_524
        and len(seam) == 15_316
        and len(ordinary) == 330_724
        and len(signed) == 25_452,
        "prior channel pair censuses",
    )
    return {
        "R295A_LOWER": lower,
        "R296_TRUE_SEAM": seam,
        "R297_ORDINARY": ordinary,
        "R299C_SIGNED_FACE": signed,
    }


def inset_face(face: tuple[Q, ...], axis: int) -> tuple[Q, ...]:
    values: list[Q] = []
    for current in range(3):
        lower, upper = face[2 * current:2 * current + 2]
        if current == axis:
            values.extend((lower, upper))
            continue
        if current == 0:
            middle = strict_square_between(lower, upper)
            values.extend((
                strict_square_between(lower, middle),
                strict_square_between(middle, upper),
            ))
        else:
            width = upper - lower
            values.extend((lower + width / 4, upper - width / 4))
    result = tuple(values)
    need(face_area(result, axis) > 0, "inset face")
    return result


def targeted_interval(
    lower: Q,
    upper: Q,
    direction: str,
    depth: int,
    transformed_t: bool,
) -> tuple[Q, Q]:
    need(
        lower < upper and direction in {"LOWER", "UPPER", "CENTER"} and depth > 0,
        "target interval",
    )
    if transformed_t:
        outer_lower, outer_upper = lower, upper
        for _ in range(depth):
            middle = strict_square_between(outer_lower, outer_upper)
            if direction == "LOWER":
                outer_upper = middle
            elif direction == "UPPER":
                outer_lower = middle
            else:
                outer_lower = strict_square_between(outer_lower, middle)
                outer_upper = strict_square_between(middle, outer_upper)
        middle = strict_square_between(outer_lower, outer_upper)
        return (
            strict_square_between(outer_lower, middle),
            strict_square_between(middle, outer_upper),
        )
    width = upper - lower
    divisor = 1 << depth
    if direction == "LOWER":
        a, b = lower, lower + width / divisor
    elif direction == "UPPER":
        a, b = upper - width / divisor, upper
    else:
        middle = (lower + upper) / 2
        radius = width / (1 << (depth + 2))
        a, b = middle - radius, middle + radius
    inner = (a + (b - a) / 4, b - (b - a) / 4)
    need(lower < inner[0] < inner[1] < upper, "strict target interval")
    return inner


def targeted_patch(
    face: tuple[Q, ...],
    axis: int,
    seed: dict[str, Any],
    regions: dict[str, dict[str, Any]],
    depth: int,
) -> tuple[Q, ...]:
    region = regions[seed["region_id"]]
    desired = region["active_factor_side_sign"]
    derivatives = region["strict_derivative_signs_t_p_s"]
    values: list[Q] = []
    for current in range(3):
        lower, upper = face[2 * current:2 * current + 2]
        if current == axis:
            values.extend((lower, upper))
            continue
        derivative = derivatives[current]
        if derivative not in STRICT_SIGNS:
            direction = "CENTER"
        else:
            higher_physical = (
                (desired == "STRICT_POSITIVE")
                == (derivative == "STRICT_POSITIVE")
            )
            higher_transformed = (
                not higher_physical
                if current == 0 and seed["physical_t_sign"] < 0
                else higher_physical
            )
            direction = "UPPER" if higher_transformed else "LOWER"
        values.extend(targeted_interval(
            lower, upper, direction, depth, current == 0
        ))
    result = tuple(values)
    need(face_area(result, axis) > 0, "target patch")
    return result


def contact_class(left: dict[str, Any], right: dict[str, Any]) -> str:
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


def corridor_candidate(
    cell: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    side: str,
    depth: int,
) -> tuple[Q, ...]:
    need(side in {"LOWER_SIDE", "UPPER_SIDE"}, "corridor side")
    box = cell["box"]
    boundary = patch[2 * axis]
    values = list(patch)
    if side == "LOWER_SIDE":
        need(box[2 * axis + 1] == boundary, "lower-side boundary")
        if axis == 0:
            lower = box[0]
            for _ in range(depth):
                lower = strict_square_between(lower, boundary)
        else:
            lower = boundary - (boundary - box[2 * axis]) / (1 << depth)
        values[2 * axis:2 * axis + 2] = [lower, boundary]
    else:
        need(box[2 * axis] == boundary, "upper-side boundary")
        if axis == 0:
            upper = box[1]
            for _ in range(depth):
                upper = strict_square_between(boundary, upper)
        else:
            upper = boundary + (box[2 * axis + 1] - boundary) / (1 << depth)
        values[2 * axis:2 * axis + 2] = [boundary, upper]
    result = tuple(values)
    need(volume(result) > 0, "corridor volume")
    return result


def certify_corridor(
    cell: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    side: str,
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any] | None:
    trace = []
    depths = (
        [1]
        if cell["support_mode"] == "FULL_SIGNED_SUPPORT"
        else range(1, MAX_CORRIDOR_DEPTH + 1)
    )
    for depth in depths:
        box = corridor_candidate(cell, patch, axis, side, depth)
        certificates = t_certificates(box)
        replay = (
            None
            if cell["support_mode"] == "FULL_SIGNED_SUPPORT"
            else active_factor_replay(cell, box, regions, modules, cache)
        )
        state = (
            "INHERITED_FULL_SIGNED_SUPPORT"
            if replay is None else replay["signed_support_state"]
        )
        trace.append({
            "corridor_depth": depth,
            "transformed_corridor_sha256": digest(qlist(box)),
            "signed_support_state": state,
            "t_boundary_sqrt_enclosures_sha256": digest(certificates),
        })
        if replay is None or state == "FULL_DESIRED_SIDE_SUPPORT":
            return {
                "corridor_side": side,
                "corridor_depth": depth,
                "exact_positive_volume_transformed_corridor": qlist(box),
                "exact_transformed_corridor_volume": qstr(volume(box)),
                "t_boundary_sqrt_enclosure_certificates": certificates,
                "t_boundary_sqrt_enclosures_sha256": digest(certificates),
                "inward_shrink_trace": trace,
                "inward_shrink_trace_sha256": digest(trace),
                "signed_support_replay": replay,
                "support_basis": (
                    "EXACT_FULL_SIGNED_SUPPORT_BOX"
                    if replay is None
                    else "ACTIVE_FACTOR_STRICT_CORRIDOR_REPLAY"
                ),
            }
    return None


def classify_face(
    left: dict[str, Any],
    right: dict[str, Any],
    face: tuple[Q, ...],
    axis: int,
    left_side: str,
    right_side: str,
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    classification = contact_class(left, right)
    graph_cells = [
        cell for cell in (left, right)
        if cell["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED"
    ]
    if classification == "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE":
        return {
            "contact_class": classification,
            "decision": "REJECT_EXACT_SAME_FACTOR_OPPOSITE_STRICT_SIDES",
            "decision_reason": "{f>0} INTERSECT {f<0} = EMPTY",
            "face_initial_replays": [],
            "accepted_patch": None,
            "accepted_patch_area": None,
            "patch_replays": [],
            "patch_search_depth": 0,
            "patch_seed_region_id": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": {
                "active_function_id": left["factor"]["active_function_id"],
                "left_desired_side_sign":
                    left["factor"]["desired_side_sign"],
                "right_desired_side_sign":
                    right["factor"]["desired_side_sign"],
                "exact_set_identity": "{f>0} INTERSECT {f<0} = EMPTY",
                "positive_area_common_strict_patch_possible": False,
            },
        }
    initial = [
        active_factor_replay(cell, face, regions, modules, cache)
        for cell in graph_cells
    ]
    empty = [
        replay for replay in initial
        if replay["signed_support_state"]
        == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    ]
    if empty:
        return {
            "contact_class": classification,
            "decision": "REJECT_EXACT_WHOLE_FACE_EMPTY_SUPPORT_EXTREMA",
            "decision_reason": "ACTIVE_FACTOR_STRICT_OPPOSITE_ON_WHOLE_FACE",
            "face_initial_replays": initial,
            "accepted_patch": None,
            "accepted_patch_area": None,
            "patch_replays": [],
            "patch_search_depth": 0,
            "patch_seed_region_id": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": {
                "exact_face": qlist(face),
                "empty_region_ids":
                    sorted(replay["region_id"] for replay in empty),
                "strict_opposite_extremal_signs": [
                    replay["active_factor_extremal_signs"]
                    for replay in empty
                ],
                "positive_area_common_strict_patch_possible": False,
            },
        }
    patch: tuple[Q, ...] | None = None
    patch_replays: list[dict[str, Any]] = []
    depth = 0
    seed_region: str | None = None
    if classification == "FULL_FULL" or all(
        replay["signed_support_state"] == "FULL_DESIRED_SIDE_SUPPORT"
        for replay in initial
    ):
        patch = inset_face(face, axis)
        patch_replays = [
            active_factor_replay(cell, patch, regions, modules, cache)
            for cell in graph_cells
        ]
    else:
        for depth_value in range(1, MAX_FACE_DEPTH + 1):
            for seed in graph_cells:
                candidate = targeted_patch(
                    face, axis, seed, regions, depth_value
                )
                replays = [
                    active_factor_replay(
                        cell, candidate, regions, modules, cache
                    )
                    for cell in graph_cells
                ]
                if all(
                    replay["signed_support_state"]
                    == "FULL_DESIRED_SIDE_SUPPORT"
                    for replay in replays
                ):
                    patch, patch_replays = candidate, replays
                    depth, seed_region = depth_value, seed["region_id"]
                    break
            if patch is not None:
                break
    if patch is None:
        return {
            "contact_class": classification,
            "decision": "UNRESOLVED_FAIL_CLOSED",
            "decision_reason": "GUIDED_PATCH_DEPTH_EXHAUSTED",
            "face_initial_replays": initial,
            "accepted_patch": None,
            "accepted_patch_area": None,
            "patch_replays": [],
            "patch_search_depth": MAX_FACE_DEPTH,
            "patch_seed_region_id": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": None,
        }
    left_corridor = certify_corridor(
        left, patch, axis, left_side, regions, modules, cache
    )
    right_corridor = certify_corridor(
        right, patch, axis, right_side, regions, modules, cache
    )
    if left_corridor is None or right_corridor is None:
        return {
            "contact_class": classification,
            "decision": "UNRESOLVED_FAIL_CLOSED",
            "decision_reason": "TWO_SIDED_CORRIDOR_DEPTH_EXHAUSTED",
            "face_initial_replays": initial,
            "accepted_patch": qlist(patch),
            "accepted_patch_area": qstr(face_area(patch, axis)),
            "patch_replays": patch_replays,
            "patch_search_depth": depth,
            "patch_seed_region_id": seed_region,
            "left_corridor": left_corridor,
            "right_corridor": right_corridor,
            "exclusion_evidence": None,
        }
    return {
        "contact_class": classification,
        "decision":
            "ACCEPT_EXACT_POSITIVE_AREA_GUIDED_PATCH_AND_TWO_POSITIVE_VOLUME_CORRIDORS",
        "decision_reason": (
            "DIRECT_STRICT_INSET"
            if depth == 0 else "TARGETED_MONOTONE_GUIDED_PATCH"
        ),
        "face_initial_replays": initial,
        "accepted_patch": qlist(patch),
        "accepted_patch_area": qstr(face_area(patch, axis)),
        "accepted_patch_t_boundary_sqrt_enclosure_certificates":
            t_certificates(patch),
        "patch_replays": patch_replays,
        "patch_search_depth": depth,
        "patch_seed_region_id": seed_region,
        "left_corridor": left_corridor,
        "right_corridor": right_corridor,
        "exclusion_evidence": None,
    }


def tangent_rectangle(box: tuple[Q, ...], axis: int) -> tuple[Q, Q, Q, Q]:
    other = [current for current in range(3) if current != axis]
    return (
        box[2 * other[0]], box[2 * other[0] + 1],
        box[2 * other[1]], box[2 * other[1] + 1],
    )


def pseudo_box(rectangle: tuple[Q, Q, Q, Q]) -> tuple[Q, ...]:
    return (
        Q(0), Q(1), rectangle[0], rectangle[1],
        rectangle[2], rectangle[2], rectangle[3],
    )


def boundary_face_rows(
    cells: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> list[dict[str, Any]]:
    _r174, _r179, _r274, r292 = modules
    queries: dict[tuple[str, int, int, Q, str], list[int]] = defaultdict(list)
    for index, cell in enumerate(cells):
        for axis in range(3):
            queries[(
                cell["source_chart"], cell["physical_t_sign"], axis,
                cell["box"][2 * axis + 1], "LOW",
            )].append(index)
            queries[(
                cell["source_chart"], cell["physical_t_sign"], axis,
                cell["box"][2 * axis], "HIGH",
            )].append(index)

    buckets: dict[
        tuple[str, int, int, Q, str],
        list[tuple[tuple[Q, ...], dict[str, Any]]],
    ] = defaultdict(list)
    transformed_count = 0
    for source in base_rows:
        rational_box = source["support_boxes"][0]
        for sign in (-1, 1):
            transformed = r292.transformed_registry_box(rational_box, sign)
            if transformed is None:
                continue
            transformed_count += 1
            for axis in range(3):
                for endpoint, coordinate_index in (
                    ("LOW", 2 * axis), ("HIGH", 2 * axis + 1)
                ):
                    key = (
                        source["source_chart"], sign, axis,
                        transformed[coordinate_index], endpoint,
                    )
                    if key not in queries:
                        continue
                    rectangle = tangent_rectangle(transformed, axis)
                    buckets[key].append((
                        pseudo_box(rectangle),
                        {
                            "cell_id":
                                "base-registry-support:"
                                + source["occurrence_id"],
                            "occurrence_id": source["occurrence_id"],
                            "region_id": None,
                            "source_chart": source["source_chart"],
                            "physical_t_sign": sign,
                            "box": transformed,
                            "rational_box": rational_box,
                            "tangent_rectangle": rectangle,
                            "endpoint_occurrence_id": source["occurrence_id"],
                            "occurrence_source": source["occurrence_source"],
                            "support_mode": "FULL_SIGNED_SUPPORT",
                            "factor": None,
                            "signature_sha256": source["signature_sha256"],
                        },
                    ))
    need(transformed_count == 421_804, "one transformed base support")

    rows = []
    for key in sorted(buckets):
        _chart, _sign, axis, _boundary, endpoint = key
        tree = r292.PIntervalNode(buckets[key])
        for cell_index in queries[key]:
            cell = cells[cell_index]
            rectangle = tangent_rectangle(cell["box"], axis)
            candidates: list[tuple[tuple[Q, ...], dict[str, Any]]] = []
            tree.query(rectangle[0], rectangle[1], candidates)
            for _pseudo, base in candidates:
                base_rectangle = base["tangent_rectangle"]
                if not (
                    max(rectangle[2], base_rectangle[2])
                    < min(rectangle[3], base_rectangle[3])
                ):
                    continue
                orientation = (
                    "LEFT_TO_RIGHT" if endpoint == "LOW" else "RIGHT_TO_LEFT"
                )
                face = common_face(cell["box"], base["box"], axis, orientation)
                need(face is not None, "boundary exact face")
                if endpoint == "LOW":
                    left_side, right_side = "LOWER_SIDE", "UPPER_SIDE"
                else:
                    left_side, right_side = "UPPER_SIDE", "LOWER_SIDE"
                proof = classify_face(
                    cell, base, face, axis, left_side, right_side,
                    regions, modules, cache,
                )
                same = (
                    cell["endpoint_occurrence_id"]
                    == base["endpoint_occurrence_id"]
                )
                endpoint_pair = (
                    None if same else list(pair(
                        cell["endpoint_occurrence_id"],
                        base["endpoint_occurrence_id"],
                    ))
                )
                face_id = "round300b-boundary-face:" + digest([
                    cell["cell_id"], base["endpoint_occurrence_id"],
                    axis, endpoint, qlist(face),
                ])
                payload = {
                    "Round300B_face_inventory_row_id": face_id,
                    "face_channel": "R292_TO_BASE_REGISTRY_BOUNDARY",
                    "left_support_id": cell["cell_id"],
                    "right_support_id": base["cell_id"],
                    "left_Round275_region_id": cell["region_id"],
                    "right_Round275_region_id": None,
                    "source_chart": cell["source_chart"],
                    "physical_t_sign": cell["physical_t_sign"],
                    "common_face_axis": axis,
                    "boundary_orientation": endpoint,
                    "exact_positive_area_coordinate_face_t2_p_s": qlist(face),
                    "exact_coordinate_face_area": qstr(face_area(face, axis)),
                    "face_t_boundary_sqrt_enclosure_certificates":
                        t_certificates(face),
                    "left_exact_support_box_t2_p_s": qlist(cell["box"]),
                    "right_exact_support_box_t2_p_s": qlist(base["box"]),
                    "left_support_mode": cell["support_mode"],
                    "right_support_mode": base["support_mode"],
                    "left_active_factor_descriptor": cell["factor"],
                    "right_active_factor_descriptor": None,
                    "left_formal_occurrence_endpoints": [
                        cell["endpoint_occurrence_id"]
                    ],
                    "right_formal_occurrence_endpoints": [
                        base["endpoint_occurrence_id"]
                    ],
                    "left_endpoint_ids_sha256":
                        digest([cell["endpoint_occurrence_id"]]),
                    "right_endpoint_ids_sha256":
                        digest([base["endpoint_occurrence_id"]]),
                    "same_formal_occurrence_endpoint": same,
                    "unordered_nonself_formal_occurrence_endpoint_pair":
                        endpoint_pair,
                    "same_complete_10_field_return_signature":
                        cell["signature_sha256"] == base["signature_sha256"],
                    "left_complete_10_field_return_signature_sha256":
                        cell["signature_sha256"],
                    "right_complete_10_field_return_signature_sha256":
                        base["signature_sha256"],
                    "base_registry_occurrence_source":
                        base["occurrence_source"],
                    "base_registry_rational_support_box":
                        qlist(base["rational_box"]),
                    **proof,
                    "formal_positive_face_patch_credit":
                        int(proof["decision"].startswith("ACCEPT_")),
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                    "formal_fibre_credit": 0,
                    "formal_global_disposition_credit": 0,
                    "formal_CM2_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(key=lambda row: row["Round300B_face_inventory_row_id"])
    need(len(rows) == 6_616, "complete boundary face scope")
    return rows


def r275_face_rows(
    region_rows: list[dict[str, Any]],
    endpoints: dict[str, set[str]],
    regions: dict[str, dict[str, Any]],
    modules: tuple[Any, Any, Any, Any],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> list[dict[str, Any]]:
    lower: dict[tuple[str, int, int, Q], list[int]] = defaultdict(list)
    for index, row in enumerate(region_rows):
        for axis in range(3):
            lower[(
                row["source_chart"], row["physical_t_sign"], axis,
                row["box"][2 * axis],
            )].append(index)
    rows = []
    for left in region_rows:
        for axis in range(3):
            key = (
                left["source_chart"], left["physical_t_sign"], axis,
                left["box"][2 * axis + 1],
            )
            for right_index in lower.get(key, []):
                right = region_rows[right_index]
                face = common_face(
                    left["box"], right["box"], axis, "LEFT_TO_RIGHT"
                )
                if face is None:
                    continue
                proof = classify_face(
                    left, right, face, axis, "LOWER_SIDE", "UPPER_SIDE",
                    regions, modules, cache,
                )
                left_endpoints = sorted(endpoints[left["region_id"]])
                right_endpoints = sorted(endpoints[right["region_id"]])
                face_id = "round300b-r275-region-face:" + digest([
                    left["region_id"], right["region_id"], axis, qlist(face),
                ])
                payload = {
                    "Round300B_face_inventory_row_id": face_id,
                    "face_channel": "COMPLETE_R275_REGION_FRONTIER",
                    "left_support_id": left["region_id"],
                    "right_support_id": right["region_id"],
                    "left_Round275_region_id": left["region_id"],
                    "right_Round275_region_id": right["region_id"],
                    "source_chart": left["source_chart"],
                    "physical_t_sign": left["physical_t_sign"],
                    "common_face_axis": axis,
                    "boundary_orientation": "LEFT_TO_RIGHT",
                    "exact_positive_area_coordinate_face_t2_p_s": qlist(face),
                    "exact_coordinate_face_area": qstr(face_area(face, axis)),
                    "face_t_boundary_sqrt_enclosure_certificates":
                        t_certificates(face),
                    "left_exact_support_box_t2_p_s": qlist(left["box"]),
                    "right_exact_support_box_t2_p_s": qlist(right["box"]),
                    "left_support_mode": left["support_mode"],
                    "right_support_mode": right["support_mode"],
                    "left_active_factor_descriptor": left["factor"],
                    "right_active_factor_descriptor": right["factor"],
                    "left_formal_occurrence_endpoints": left_endpoints,
                    "right_formal_occurrence_endpoints": right_endpoints,
                    "left_endpoint_ids_sha256": digest(left_endpoints),
                    "right_endpoint_ids_sha256": digest(right_endpoints),
                    "same_formal_occurrence_endpoint": None,
                    "unordered_nonself_formal_occurrence_endpoint_pair": None,
                    "same_complete_10_field_return_signature":
                        left["signature_sha256"] == right["signature_sha256"],
                    "left_complete_10_field_return_signature_sha256":
                        left["signature_sha256"],
                    "right_complete_10_field_return_signature_sha256":
                        right["signature_sha256"],
                    "base_registry_occurrence_source": None,
                    "base_registry_rational_support_box": None,
                    **proof,
                    "formal_positive_face_patch_credit":
                        int(proof["decision"].startswith("ACCEPT_")),
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                    "formal_fibre_credit": 0,
                    "formal_global_disposition_credit": 0,
                    "formal_CM2_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(key=lambda row: row["Round300B_face_inventory_row_id"])
    need(len(rows) == 55_932, "complete R275 face scope")
    return rows


def derive_edge_ledgers(
    faces: list[dict[str, Any]],
    prior: dict[str, set[tuple[str, str]]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    raw_rows: list[dict[str, Any]] = []
    no_edge_rows: list[dict[str, Any]] = []
    evidence: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    channel_pairs: dict[str, set[tuple[str, str]]] = defaultdict(set)
    accepted_faces = Counter()
    excluded_faces = Counter()
    unresolved_faces = Counter()
    self_incidences = Counter()

    for face in faces:
        face_id = face["Round300B_face_inventory_row_id"]
        channel = face["face_channel"]
        decision = face["decision"]
        if decision.startswith("REJECT_"):
            excluded_faces[channel] += 1
            no_edge_rows.append(closed({
                "Round300B_no_edge_row_id":
                    "round300b-exclusion:" + digest([face_id, decision]),
                "no_edge_kind": "EXACT_FACE_EXCLUSION",
                "source_face_inventory_row_id": face_id,
                "face_channel": channel,
                "formal_occurrence_id": None,
                "decision": decision,
                "decision_reason": face["decision_reason"],
                "exclusion_evidence": face["exclusion_evidence"],
                "unresolved_obligation": None,
                "formal_component_edge_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
            }))
            continue
        if decision == "UNRESOLVED_FAIL_CLOSED":
            unresolved_faces[channel] += 1
            no_edge_rows.append(closed({
                "Round300B_no_edge_row_id":
                    "round300b-unresolved:" + digest([face_id, decision]),
                "no_edge_kind": "UNRESOLVED_ZERO_CREDIT_OBLIGATION",
                "source_face_inventory_row_id": face_id,
                "face_channel": channel,
                "formal_occurrence_id": None,
                "decision": decision,
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
        need(decision.startswith("ACCEPT_"), "known face decision")
        accepted_faces[channel] += 1
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
            self_incidences[channel] += multiplicity
            no_edge_rows.append(closed({
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
            raw_id = "round300b-raw-edge-witness:" + digest([
                channel, face_id, list(endpoint_pair)
            ])
            raw = closed({
                "Round300B_accepted_raw_edge_witness_row_id": raw_id,
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
            raw_rows.append(raw)
            evidence[endpoint_pair].append(raw)
            channel_pairs[channel].add(endpoint_pair)

    raw_rows.sort(
        key=lambda row: row["Round300B_accepted_raw_edge_witness_row_id"]
    )
    no_edge_rows.sort(key=lambda row: row["Round300B_no_edge_row_id"])
    prior_union = set().union(*prior.values())
    boundary = channel_pairs["R292_TO_BASE_REGISTRY_BOUNDARY"]
    r275 = channel_pairs["COMPLETE_R275_REGION_FRONTIER"]
    all_pairs = boundary | r275
    boundary_new = boundary - prior_union
    r275_incremental = r275 - prior_union - boundary
    novel = boundary_new | r275_incremental

    canonical_rows = []
    accounting_rows = []
    for endpoint_pair in sorted(all_pairs):
        witnesses = sorted(
            evidence[endpoint_pair],
            key=lambda row:
                row["Round300B_accepted_raw_edge_witness_row_id"],
        )
        witness_ids = [
            row["Round300B_accepted_raw_edge_witness_row_id"]
            for row in witnesses
        ]
        channels = sorted({row["face_channel"] for row in witnesses})
        prior_membership = {
            name: endpoint_pair in values
            for name, values in sorted(prior.items())
        }
        if endpoint_pair in boundary_new:
            disposition = "PROMOTE_NEW__FIRST_CHANNEL_BOUNDARY"
        elif endpoint_pair in r275_incremental:
            disposition = "PROMOTE_NEW__FIRST_CHANNEL_COMPLETE_R275"
        else:
            disposition = "SUPPRESS_ALREADY_PRESENT_IN_PRIOR_CHANNEL"
        promoted = endpoint_pair in novel
        accounting_rows.append(closed({
            "Round300B_duplicate_prior_accounting_row_id":
                "round300b-pair-accounting:" + digest(list(endpoint_pair)),
            "unordered_formal_occurrence_endpoint_pair": list(endpoint_pair),
            "accepted_raw_witness_count": len(witness_ids),
            "accepted_raw_witness_row_ids": witness_ids,
            "accepted_raw_witness_row_ids_sha256": digest(witness_ids),
            "witness_channels": channels,
            "witness_channels_sha256": digest(channels),
            "duplicate_raw_witness_count": len(witness_ids) - 1,
            "cross_Round300B_channel_duplicate":
                len(channels) == 2,
            "prior_channel_membership": prior_membership,
            "prior_channel_membership_sha256": digest(prior_membership),
            "pair_accounting_disposition": disposition,
            "canonical_novel_edge_emitted": promoted,
            "rejected_face_never_negates_accepted_witness": True,
            "pair_acceptance_semantics": "EXISTS_ACCEPTED_PHYSICAL_FACE_WITNESS",
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
        }))
        if not promoted:
            continue
        canonical_rows.append(closed({
            "Round300B_canonical_novel_occurrence_edge_row_id":
                "round300b-canonical-novel-edge:"
                + digest(list(endpoint_pair)),
            "unordered_formal_occurrence_endpoint_pair": list(endpoint_pair),
            "first_new_face_channel": (
                "R292_TO_BASE_REGISTRY_BOUNDARY"
                if endpoint_pair in boundary_new
                else "COMPLETE_R275_REGION_FRONTIER"
            ),
            "accepted_raw_witness_count": len(witness_ids),
            "accepted_raw_witness_row_ids": witness_ids,
            "accepted_raw_witness_row_ids_sha256": digest(witness_ids),
            "selected_canonical_witness_row_id": witness_ids[0],
            "pair_acceptance_semantics": "EXISTS_ACCEPTED_PHYSICAL_FACE_WITNESS",
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
    canonical_rows.sort(
        key=lambda row: row["Round300B_canonical_novel_occurrence_edge_row_id"]
    )
    accounting_rows.sort(
        key=lambda row: row["Round300B_duplicate_prior_accounting_row_id"]
    )
    census = {
        "accepted_face_count_by_channel":
            dict(sorted(accepted_faces.items())),
        "excluded_face_count_by_channel":
            dict(sorted(excluded_faces.items())),
        "unresolved_face_count_by_channel":
            dict(sorted(unresolved_faces.items())),
        "self_endpoint_incidence_count_by_channel":
            dict(sorted(self_incidences.items())),
        "accepted_raw_edge_witness_count": len(raw_rows),
        "accepted_boundary_distinct_pair_count": len(boundary),
        "accepted_complete_R275_distinct_pair_count": len(r275),
        "accepted_cross_channel_pair_intersection_count":
            len(boundary & r275),
        "accepted_Round300B_distinct_pair_union_count": len(all_pairs),
        "boundary_new_beyond_R295A_R296_R297_R299C_count":
            len(boundary_new),
        "complete_R275_incremental_new_beyond_prior_and_boundary_count":
            len(r275_incremental),
        "canonical_novel_occurrence_edge_pair_count": len(novel),
        "prior_suppressed_distinct_pair_count": len(all_pairs - novel),
        "duplicate_raw_witness_count":
            sum(len(values) - 1 for values in evidence.values()),
        "canonical_novel_pairs_sha256":
            digest([list(value) for value in sorted(novel)]),
    }
    return raw_rows, canonical_rows, no_edge_rows, accounting_rows, census


def attack_suite() -> dict[str, Any]:
    specifications = [
        ("SEMANTIC_PATCH_ZERO_AREA", "SEMANTIC"),
        ("SEMANTIC_PATCH_OUTSIDE_FACE", "SEMANTIC"),
        ("SEMANTIC_PATCH_WRONG_NORMAL_COORDINATE", "SEMANTIC"),
        ("SEMANTIC_LEFT_CORRIDOR_ZERO_VOLUME", "SEMANTIC"),
        ("SEMANTIC_RIGHT_CORRIDOR_ZERO_VOLUME", "SEMANTIC"),
        ("SEMANTIC_LEFT_CORRIDOR_WRONG_SIDE", "SEMANTIC"),
        ("SEMANTIC_RIGHT_CORRIDOR_OUTSIDE_SUPPORT", "SEMANTIC"),
        ("SEMANTIC_GRAPH_PATCH_REPLAY_NOT_FULL", "SEMANTIC"),
        ("SEMANTIC_GRAPH_CORRIDOR_REPLAY_NOT_FULL", "SEMANTIC"),
        ("SEMANTIC_OPPOSITE_FACTOR_EXCLUSION_FLIPPED", "SEMANTIC"),
        ("SEMANTIC_EMPTY_EXTREMA_EXCLUSION_FLIPPED", "SEMANTIC"),
        ("SEMANTIC_UNRESOLVED_PROMOTED", "SEMANTIC"),
        ("SEMANTIC_SELF_PROMOTED", "SEMANTIC"),
        ("SEMANTIC_ENDPOINT_PAIR_UNSORTED", "SEMANTIC"),
        ("SEMANTIC_PRIOR_PAIR_REPROMOTED", "SEMANTIC"),
        ("SEMANTIC_DUPLICATE_PAIR_REPROMOTED", "SEMANTIC"),
        ("SEMANTIC_REJECT_OVERRIDES_ACCEPT_EXISTS", "SEMANTIC"),
        ("SEMANTIC_RAW_WITNESS_FACE_HASH_TAMPER", "SEMANTIC"),
        ("SEMANTIC_CANONICAL_WITNESS_SET_TAMPER", "SEMANTIC"),
        ("SEMANTIC_ROW_HASH_STALE", "SEMANTIC"),
        ("SEMANTIC_ROWS_HASH_STALE", "SEMANTIC"),
        ("JSON_DUPLICATE_KEY", "JSON_BOUNDARY"),
        ("JSON_TRAILING_TOKEN", "JSON_BOUNDARY"),
        ("JSON_NAN_CONSTANT", "JSON_BOUNDARY"),
        ("JSON_UTF8_BOM", "JSON_BOUNDARY"),
        ("GZIP_CONCATENATED_MEMBER", "GZIP_BOUNDARY"),
        ("GZIP_TRAILING_BYTES", "GZIP_BOUNDARY"),
        ("GZIP_NONCANONICAL_MTIME", "GZIP_BOUNDARY"),
        ("GZIP_JSON_DUPLICATE_KEY", "GZIP_BOUNDARY"),
        ("PATH_SYMLINK_INPUT", "PATH_BOUNDARY"),
        ("PATH_HARDLINK_INPUT", "PATH_BOUNDARY"),
        ("PATH_DIRECTORY_INPUT", "PATH_BOUNDARY"),
        ("PATH_PARENT_ESCAPE", "PATH_BOUNDARY"),
        ("COORDINATED_RESIGN_FACE_AND_RAW", "COORDINATED_RESIGN"),
        ("COORDINATED_RESIGN_RAW_AND_CANONICAL", "COORDINATED_RESIGN"),
        ("COORDINATED_RESIGN_ALL_CANDIDATE_OUTPUTS", "COORDINATED_RESIGN"),
    ]
    rows = [
        {
            "attack_id": attack_id,
            "attack_category": category,
            "expected_verifier_disposition": "REJECT",
        }
        for attack_id, category in specifications
    ]
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "ATTACK_SPECIFICATIONS_FOR_INDEPENDENT_EXECUTION",
        "attack_count": len(rows),
        "attacks": rows,
        "attacks_sha256": digest(rows),
    }
    payload["attack_suite_sha256"] = digest(payload)
    return payload


def build() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    for name in sorted(PINS):
        guarded(name)
    modules = load_modules()
    regions = load_regions()
    r287_regions, r287_cells = load_r287()
    refined = load_refined_occurrence_map()
    r292_document = read_gzip(R292)
    r292_source_rows = verify_table(
        r292_document, "rows", "row_count", "rows_sha256"
    )
    cells = load_r292_cells(
        regions, r287_regions, r287_cells, refined, r292_source_rows
    )
    region_rows = load_region_rows(regions, r287_regions)
    endpoints = load_region_endpoints(
        regions, refined, r292_source_rows
    )
    base_rows = load_base_registry(modules)
    prior = load_prior_pairs()
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]] = {}
    boundary = boundary_face_rows(
        cells, base_rows, regions, modules, cache
    )
    complete_r275 = r275_face_rows(
        region_rows, endpoints, regions, modules, cache
    )
    faces = sorted(
        boundary + complete_r275,
        key=lambda row: row["Round300B_face_inventory_row_id"],
    )
    raw, edges, no_edge, duplicate, edge_census = derive_edge_ledgers(
        faces, prior
    )
    unresolved = sum(
        row["decision"] == "UNRESOLVED_FAIL_CLOSED" for row in faces
    )
    expected_closed_counts = (
        unresolved == 0
        and edge_census[
            "boundary_new_beyond_R295A_R296_R297_R299C_count"
        ] == 2_824
        and edge_census[
            "complete_R275_incremental_new_beyond_prior_and_boundary_count"
        ] == 7_592
        and edge_census["canonical_novel_occurrence_edge_pair_count"] == 10_416
    )
    face_document = ledger(
        SCHEMA + ".face-inventory-ledger.v1",
        faces,
        "Round300B_face_inventory_row_id",
    )
    raw_document = ledger(
        SCHEMA + ".accepted-raw-edge-witness-ledger.v1",
        raw,
        "Round300B_accepted_raw_edge_witness_row_id",
    )
    edge_document = ledger(
        SCHEMA + ".canonical-novel-occurrence-edge-ledger.v1",
        edges,
        "Round300B_canonical_novel_occurrence_edge_row_id",
    )
    no_edge_document = ledger(
        SCHEMA + ".self-exclusion-unresolved-ledger.v1",
        no_edge,
        "Round300B_no_edge_row_id",
    )
    duplicate_document = ledger(
        SCHEMA + ".duplicate-prior-pair-accounting-ledger.v1",
        duplicate,
        "Round300B_duplicate_prior_accounting_row_id",
    )
    attacks = attack_suite()
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_FORMAL_FULL_FACE_INVENTORY_CLOSED__"
            "10416_CANONICAL_NOVEL_COMPONENT_EDGES__ZERO_DSU_RANK_CREDIT"
            if expected_closed_counts
            else "PASS_FAIL_CLOSED_WITH_EXACT_UNRESOLVED_OR_CENSUS_OBLIGATIONS"
        ),
        "python_flint_version": FLINT_VERSION,
        "input_file_pins": dict(sorted(PINS.items())),
        "scope_census": {
            "Round292_exact_refinement_cell_count": len(cells),
            "base_registry_occurrence_count": len(base_rows),
            "complete_R275_region_count": len(region_rows),
            "complete_R275_region_endpoint_incidence_count":
                sum(map(len, endpoints.values())),
            "raw_R292_registry_boundary_face_count": len(boundary),
            "raw_complete_R275_region_face_count": len(complete_r275),
            "raw_complete_face_inventory_count": len(faces),
            "face_decision_histogram": dict(sorted(Counter(
                row["decision"] for row in faces
            ).items())),
            "face_channel_decision_histogram": dict(sorted(Counter(
                row["face_channel"] + "|" + row["decision"]
                for row in faces
            ).items())),
            **edge_census,
            "audited_2824_boundary_candidate_pairs_accounted": (
                edge_census[
                    "boundary_new_beyond_R295A_R296_R297_R299C_count"
                ] == 2_824
            ),
            "audited_7592_R275_candidate_pairs_accounted": (
                edge_census[
                    "complete_R275_incremental_new_beyond_prior_and_boundary_count"
                ] == 7_592
            ),
        },
        "proof_contract": {
            "every_accepted_face_has_exact_positive_area_guided_patch": all(
                Q(row["accepted_patch_area"]) > 0
                for row in faces if row["decision"].startswith("ACCEPT_")
            ),
            "every_accepted_face_has_two_exact_positive_volume_corridors": all(
                Q(row[side]["exact_transformed_corridor_volume"]) > 0
                for row in faces if row["decision"].startswith("ACCEPT_")
                for side in ("left_corridor", "right_corridor")
            ),
            "every_rejected_face_has_exact_exclusion": all(
                row["exclusion_evidence"] is not None
                for row in faces if row["decision"].startswith("REJECT_")
            ),
            "all_unresolved_faces_fail_closed": True,
            "pair_acceptance_semantics": "EXISTS_ACCEPTED_PHYSICAL_FACE_WITNESS",
            "global_pair_deduplication_channels": [
                "R295A_LOWER", "R296_TRUE_SEAM", "R297_ORDINARY",
                "R299C_SIGNED_FACE",
                "R300B_R292_TO_BASE_REGISTRY_BOUNDARY",
                "R300B_COMPLETE_R275_REGION_FRONTIER",
            ],
        },
        "strict_nonclaims": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_CM2_credit": 0,
            "component_edge_pair_count_does_not_imply_DSU_rank": True,
            "CM2": "NO_GO_PENDING_FINAL_DSU_AND_DOWNSTREAM_GATES",
        },
        "artifacts": {},
        "attack_suite": {
            "filename": ATTACKS.name,
            "attack_count": attacks["attack_count"],
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
    }
    return (
        face_document, raw_document, edge_document, no_edge_document,
        duplicate_document, attacks, result,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--face-ledger", type=Path, default=FACE_LEDGER)
    parser.add_argument("--raw-ledger", type=Path, default=RAW_LEDGER)
    parser.add_argument("--edge-ledger", type=Path, default=EDGE_LEDGER)
    parser.add_argument("--no-edge-ledger", type=Path, default=NO_EDGE_LEDGER)
    parser.add_argument("--duplicate-ledger", type=Path, default=DUP_LEDGER)
    parser.add_argument("--attacks", type=Path, default=ATTACKS)
    arguments = parser.parse_args()
    (
        face_document, raw_document, edge_document, no_edge_document,
        duplicate_document, attacks, result,
    ) = build()
    result["artifacts"] = {
        "face_inventory": emit_gzip(arguments.face_ledger, face_document),
        "accepted_raw_edge_witnesses":
            emit_gzip(arguments.raw_ledger, raw_document),
        "canonical_novel_occurrence_edge_pairs":
            emit_gzip(arguments.edge_ledger, edge_document),
        "self_exclusion_and_unresolved":
            emit_gzip(arguments.no_edge_ledger, no_edge_document),
        "duplicate_and_prior_pair_accounting":
            emit_gzip(arguments.duplicate_ledger, duplicate_document),
    }
    attack_bytes = canonical(attacks) + b"\n"
    atomic(arguments.attacks, attack_bytes)
    result["attack_suite"]["file_sha256"] = hashlib.sha256(
        attack_bytes
    ).hexdigest()
    result["result_sha256"] = digest(result)
    atomic(arguments.result, canonical(result) + b"\n")
    print(result["status"])
    print("result_sha256=" + result["result_sha256"])
    for name, metadata in sorted(result["artifacts"].items()):
        print(name + "_file_sha256=" + metadata["file_sha256"])


if __name__ == "__main__":
    main()
