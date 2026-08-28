#!/usr/bin/env python3
"""Second, explicit quotient-map implementation of the C27 alias subgate.

This implementation does not import, execute, or read the first alias probe.
It reconstructs the 16 source sheets and all 113,452 R291 physical cells,
then solves equality in the primitive global source-G phase map

    Phi(chart,t,p,s) = (n, q=(9/25)n,
                        u=sqrt(1-p^2)n+p*n_perp, s).

Only equality of Phi is a chart-representation quotient.  Jx, Jy, and JxJy
are separately applied as physical actions and their fixed-set equations are
checked on every source sheet; Round227's pinned non-glue contract is also
reverified.  A nonidentity physical-symmetry orbit is never treated as an
atlas identification.

All candidate generation is independent of Round306C27 and of any edge
ledger.  All inputs use one O_NOFOLLOW byte capture whose bytes are both
hashed and parsed.  PASS is diagnostic, awards zero credit, and leaves the
unconditional C27/C28/C29 decision at REJECT.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import ctypes
import errno
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
from typing import Any, Iterator, TextIO


ROOT = Path(__file__).resolve().parent
AUDIT_ROOT = ROOT.parent / ".cm2-runtime" / "audit"
PREFIX = "cm2_c27_explicit_quotient_map_alias_zero_credit_v2"
LEDGER = PREFIX + "_equation_cohort_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
MANIFEST = PREFIX + "_manifest.json"

PRIMITIVE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
R171_CERT = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171_VERIFY = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
R227_CERT = "cm2_round227_source_g_sheet_symmetry_non_glue_audit_certificate.json"
R227_VERIFY = "cm2_round227_source_g_sheet_symmetry_non_glue_audit_verification.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R291 = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz"
R295A = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"

INPUT_PINS = {
    PRIMITIVE: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    R171_CERT: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    R171_VERIFY: "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    R227_CERT: "fa8d518239d2f2d4eb993ac58c66ffe2b7d222fa8efd4d916689cebd05201461",
    R227_VERIFY: "a0446082bb4f7c9b2f35885ce085237dfd2eec4789aa8447c0b0e85864d500e6",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    R291: "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
}

SEED_FINGERPRINT_TEXT = "cm2-c27-alias-v2-seed-fingerprint"
SEED_FINGERPRINTS = {
    "30627301": 5962881712184152749,
    "30627981": 8912850494244237458,
}

FORBIDDEN_INPUT_NAME_MARKERS = (
    "cm2_c27_alias_rechart_handoff_zero_credit_probe",
    "cm2_round306c27",
    "edge_ledger",
)
FORBIDDEN_MODULE_NAME_MARKERS = (
    "cm2_c27_alias_rechart_handoff_zero_credit_probe",
    "cm2_round306c27",
)

CHARTS = ("G:E", "G:W", "G:N", "G:S")
CELLS = ("E", "W", "N", "S")
SOURCE_RADIUS = Fraction(9, 25)
EXPECTED_KINDS = {
    "ROUND182_GRAPH_SHEET_LEAF": 111_524,
    "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
    "SOURCE_EXACT_T0_SHEET_CELL": 224,
    "ROUND182_TRANSVERSE_1D_LINE": 112,
}
GRAPH_BOUND_ROLE = "CONSERVATIVE_CONTAINING_R182_LEAF_BOX__ACTUAL_GRAPH_SUPPORT_SUBSET"
GRAPH_SIDE_BOUND_ROLE = "CONSERVATIVE_CONTAINING_R208_LEAF_BOX__ACTUAL_REGION_SUPPORT_SUBSET"
T0_BOUND_ROLE = "EXACT_LOWER_DIMENSIONAL_CELL_BOUNDS__ACTUAL_SUPPORT_EQUAL"
TRANSVERSE_BOUND_ROLE = "CONSERVATIVE_CONTAINING_R179_RETAINED_BOX__ACTUAL_TRANSVERSE_SUPPORT_SUBSET"
BOUND_ROLE_BY_KIND = {
    "ROUND182_GRAPH_SHEET_LEAF": GRAPH_BOUND_ROLE,
    "ROUND208_DIRECT_GRAPH_SIDE_REGION": GRAPH_SIDE_BOUND_ROLE,
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": T0_BOUND_ROLE,
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": T0_BOUND_ROLE,
    "SOURCE_EXACT_T0_SHEET_CELL": T0_BOUND_ROLE,
    "ROUND182_TRANSVERSE_1D_LINE": TRANSVERSE_BOUND_ROLE,
}
EXPECTED_BOUND_ROLE_CENSUS = {
    GRAPH_BOUND_ROLE: 111_524,
    GRAPH_SIDE_BOUND_ROLE: 608,
    T0_BOUND_ROLE: 1_208,
    TRANSVERSE_BOUND_ROLE: 112,
}
R179_COLUMNS = (
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "reason_labels",
    "ambient_dimension", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
)


class GateFailure(RuntimeError):
    pass


CAPTURE_RECORDS: dict[str, dict[str, Any]] = {}
CAPTURE_FDS: dict[str, int] = {}


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise GateFailure(label)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_float(token: str) -> Any:
    raise GateFailure("JSON float forbidden:" + token)


def reject_constant(token: str) -> Any:
    raise GateFailure("JSON constant forbidden:" + token)


DECODER = json.JSONDecoder(
    object_pairs_hook=strict_pairs,
    parse_float=reject_float,
    parse_constant=reject_constant,
)


def strict_loads(payload: bytes | bytearray) -> Any:
    need(bytes(payload[:3]) != b"\xef\xbb\xbf", "JSON BOM forbidden")
    text = bytes(payload).decode("utf-8", "strict")
    value, end = DECODER.raw_decode(text)
    need(not text[end:].strip(), "trailing JSON content")
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def metadata_tuple(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode), info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def capture_input(name: str) -> bytearray:
    need(name in INPUT_PINS and name not in CAPTURE_RECORDS, "unique approved input capture:" + name)
    lowered = name.lower()
    need(
        not any(marker in lowered for marker in FORBIDDEN_INPUT_NAME_MARKERS),
        "forbidden semantic-authority input:" + name,
    )
    path = ROOT / name
    need(path.parent == ROOT and path.parent.resolve(strict=True) == ROOT.resolve(strict=True), "direct input:" + name)
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            "nofollow regular input:" + name,
        )
        payload = bytearray()
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            payload.extend(block)
            state.update(block)
        after = os.fstat(descriptor)
        need(metadata_tuple(opened) == metadata_tuple(after), "stable input capture:" + name)
        need(len(payload) == opened.st_size, "captured size:" + name)
        actual = state.hexdigest()
        need(actual == INPUT_PINS[name], "captured byte pin:" + name)
        CAPTURE_RECORDS[name] = {
            "device": opened.st_dev,
            "inode": opened.st_ino,
            "mode": stat.S_IMODE(opened.st_mode),
            "nlink": opened.st_nlink,
            "size": opened.st_size,
            "mtime_ns": opened.st_mtime_ns,
            "ctime_ns": opened.st_ctime_ns,
            "sha256": actual,
            "open_count": 1,
            "content_read_count": 1,
            "hash_and_parse_source": "SAME_CAPTURED_BYTES",
        }
        CAPTURE_FDS[name] = descriptor
        return payload
    except BaseException:
        os.close(descriptor)
        raise


def recheck_capture_metadata() -> None:
    need(set(CAPTURE_RECORDS) == set(INPUT_PINS), "complete input capture set")
    for name in sorted(INPUT_PINS):
        opened = os.fstat(CAPTURE_FDS[name])
        path_info = os.lstat(ROOT / name)
        expected = CAPTURE_RECORDS[name]
        for field, actual in (
            ("device", opened.st_dev), ("inode", opened.st_ino),
            ("mode", stat.S_IMODE(opened.st_mode)), ("nlink", opened.st_nlink),
            ("size", opened.st_size), ("mtime_ns", opened.st_mtime_ns),
            ("ctime_ns", opened.st_ctime_ns),
        ):
            need(expected[field] == actual, "stable open input metadata:" + name + ":" + field)
        need(metadata_tuple(path_info) == metadata_tuple(opened), "stable path/fd identity:" + name)


def close_capture_fds() -> None:
    for descriptor in CAPTURE_FDS.values():
        try:
            os.close(descriptor)
        except OSError:
            pass
    CAPTURE_FDS.clear()


def validate_seed_runtime() -> dict[str, Any]:
    seed = os.environ.get("PYTHONHASHSEED")
    need(seed in SEED_FINGERPRINTS, "true seed selected")
    need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.hash_randomization == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1
        and sys.dont_write_bytecode is True,
        "clean non-isolated seed runtime",
    )
    need(
        hash(SEED_FINGERPRINT_TEXT) == SEED_FINGERPRINTS[seed],
        "active PYTHONHASHSEED fingerprint",
    )
    return {
        "invocation_must_not_use_python_I": True,
        "required_flags": {
            "isolated": 0,
            "ignore_environment": 0,
            "hash_randomization": 1,
            "dont_write_bytecode": 1,
            "no_user_site": 1,
        },
        "PYTHONHASHSEED_is_observed_by_runtime": True,
        "accepted_true_seed_fingerprints": dict(sorted(SEED_FINGERPRINTS.items())),
        "fingerprint_text_sha256": hashlib.sha256(SEED_FINGERPRINT_TEXT.encode("ascii")).hexdigest(),
        "active_seed_intentionally_omitted_for_byte_identical_outputs": True,
    }


def validate_independent_input_boundary() -> dict[str, Any]:
    approved = sorted(INPUT_PINS)
    need(len(approved) == 11 and len(set(approved)) == 11, "exact approved input allowlist")
    forbidden_approved = [
        name for name in approved
        if any(marker in name.lower() for marker in FORBIDDEN_INPUT_NAME_MARKERS)
    ]
    need(not forbidden_approved, "approved inputs exclude alias-v1/C27/edge ledger")
    forbidden_loaded = [
        name for name in sorted(sys.modules)
        if any(marker in name.lower() for marker in FORBIDDEN_MODULE_NAME_MARKERS)
    ]
    need(not forbidden_loaded, "alias-v1/C27 modules absent")
    need(set(CAPTURE_RECORDS).issubset(INPUT_PINS), "captured inputs remain inside exact allowlist")
    return {
        "approved_input_basename_count": len(approved),
        "approved_input_basenames": approved,
        "forbidden_input_name_markers": list(FORBIDDEN_INPUT_NAME_MARKERS),
        "forbidden_module_name_markers": list(FORBIDDEN_MODULE_NAME_MARKERS),
        "forbidden_approved_input_count": len(forbidden_approved),
        "forbidden_loaded_module_count": len(forbidden_loaded),
        "all_application_authority_reads_must_use_capture_input_allowlist": True,
        "alias_v1_C27_and_edge_ledger_are_outside_the_allowlist": True,
    }


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "row closure:" + label)


def closed_wrapper(payload: bytes | bytearray, name: str) -> dict[str, Any]:
    document = strict_loads(payload)
    need(type(document) is dict and type(document.get("result")) is dict, "closed wrapper:" + name)
    need(document.get("result_sha256") == digest(document["result"]), "wrapper closure:" + name)
    return document["result"]


def stream_array(
    stream: TextIO, *, marker: str, nested_rows: bool,
    expected_type: type = dict,
) -> Iterator[Any]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing marker:" + marker)
        buffer = (buffer + block)[-(len(marker) + (2 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    if nested_rows:
        while '"rows":[' not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing nested rows:" + marker)
            buffer += block
        buffer = buffer.split('"rows":[', 1)[1]
    else:
        while not buffer.lstrip().startswith("["):
            block = stream.read(1 << 20)
            need(bool(block), "missing array opener:" + marker)
            buffer += block
        buffer = buffer.lstrip()[1:]
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated array:" + marker)
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated array row:" + marker)
                buffer += block
        need(type(value) is expected_type, "array row type:" + marker)
        yield value
        buffer = buffer[end:]


def plain_array(
    payload: bytes | bytearray, marker: str, *, nested_rows: bool = False,
    expected_type: type = dict,
) -> Iterator[Any]:
    with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8", errors="strict", newline="") as stream:
        yield from stream_array(stream, marker=marker, nested_rows=nested_rows, expected_type=expected_type)


def gzip_array(payload: bytes | bytearray) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as compressed:
        with io.TextIOWrapper(compressed, encoding="utf-8", errors="strict", newline="") as stream:
            yield from stream_array(stream, marker='"rows":', nested_rows=False)


def gzip_jsonl(payload: bytes | bytearray) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "JSONL newline")
            row = strict_loads(raw[:-1])
            need(type(row) is dict, "JSONL object")
            yield row


def assignment_expression(function: ast.FunctionDef, name: str) -> str:
    matches = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and ast.unparse(node.targets[0]) == name:
            matches.append(ast.unparse(node.value))
    need(len(matches) == 1, "unique primitive assignment:" + name)
    return matches[0]


def branch_normal_assignments(function: ast.FunctionDef) -> dict[str, tuple[str, str]]:
    output: dict[str, tuple[str, str]] = {}
    for node in ast.walk(function):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        if ast.unparse(node.test.left) != "cell" or len(node.test.comparators) != 1:
            continue
        comparator = node.test.comparators[0]
        if not isinstance(comparator, ast.Constant) or comparator.value not in CELLS:
            continue
        assignments = [
            item for item in node.body
            if isinstance(item, ast.Assign)
            and len(item.targets) == 1
            and ast.unparse(item.targets[0]) == "(nx, ny)"
        ]
        need(len(assignments) == 1 and isinstance(assignments[0].value, ast.Tuple), "primitive normal tuple branch")
        output[str(comparator.value)] = tuple(ast.unparse(value) for value in assignments[0].value.elts)  # type: ignore[assignment]
    return output


def validate_geometry_authorities() -> dict[str, Any]:
    primitive_bytes = capture_input(PRIMITIVE)
    source = bytes(primitive_bytes).decode("utf-8", "strict")
    tree = ast.parse(source, filename=PRIMITIVE)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    need("geometry" in functions, "primitive geometry function")
    geometry = functions["geometry"]
    normals = branch_normal_assignments(geometry)
    need(normals == {
        "E": ("radical_n", "t"),
        "W": ("-radical_n", "t"),
        "N": ("t", "radical_n"),
        "S": ("t", "-radical_n"),
    }, "primitive normal branch AST")
    need(
        assignment_expression(geometry, "ux") == "radical_p * nx - p * ny"
        and assignment_expression(geometry, "uy") == "radical_p * ny + p * nx",
        "primitive velocity AST",
    )
    returns = [node for node in ast.walk(geometry) if isinstance(node, ast.Return)]
    need(
        len(returns) == 1
        and ast.unparse(returns[0].value)
        == "(cx + radius * nx, cy + radius * ny, ux, uy, s, radical_p)",
        "primitive phase-map return AST",
    )
    del primitive_bytes

    r171_bytes = capture_input(R171_CERT)
    r171 = closed_wrapper(r171_bytes, R171_CERT)
    del r171_bytes
    bridge = r171["exact_source_G_coordinate_bridge"]
    need(
        r171["status"] == "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__NO_RETURN_KEY_OR_D02_PROMOTION"
        and bridge["source_G_center"] == ["0", "0"]
        and bridge["source_G_radius"] == "9/25"
        and bridge["source_state_is_exactly_s_independent"] is True
        and bridge["s_is_retained_as_product_and_target_shift_parameter"] is True
        and bridge["t_map_absolute_endpoint"] == "1/sqrt(2)"
        and len(bridge["seam_rows"]) == 4
        and all(
            row["normal_glues_exactly"] is True
            and row["source_G_position_glues_exactly"] is True
            and row["quarter_turn_and_velocity_glue_for_every_q"] is True
            for row in bridge["seam_rows"]
        ),
        "R171 global phase quotient contract",
    )
    r171v_bytes = capture_input(R171_VERIFY)
    r171v = closed_wrapper(r171v_bytes, R171_VERIFY)
    del r171v_bytes
    need(
        r171v["status"] == "PASS"
        and r171v["certificate_sha256"] == INPUT_PINS[R171_CERT]
        and r171v["certificate_result_sha256"] == digest(r171)
        and r171v["producer_imported_or_executed"] is False
        and r171v["source_G_center_radius_position_independently_rebuilt"] is True
        and r171v["all_four_source_G_seams_independently_reduced_in_Q_kappa"] is True,
        "R171 independent verification",
    )

    r227_bytes = capture_input(R227_CERT)
    r227 = closed_wrapper(r227_bytes, R227_CERT)
    del r227_bytes
    contract = r227["map_contract"]
    need(
        r227["status"] == "CERTIFIED_COMPLETE_SHEET_KLEIN_EQUIVARIANCE__SYMMETRY_IS_NOT_GLUE__ZERO_COMPONENT_PROMOTION"
        and contract == {
            "Jx_physical_reflection": "(x,y,s,p)->(-x,y,-s,-p)",
            "Jy_physical_reflection": "(x,y,s,p)->(x,-y,s,-p)",
            "both_maps_nonidentity_on_physical_space": True,
            "equivariance_does_not_authorize_union_find_edge": True,
            "symmetry_partner_is_same_physical_point_atlas_transition": False,
        }
        and r227["census"]["fixed_sheet_count_Jx"] == 0
        and r227["census"]["fixed_sheet_count_Jy"] == 0
        and r227["census"]["physical_glue_credit"] == 0
        and r227["census"]["component_union_credit"] == 0,
        "R227 non-glue action contract",
    )
    r227v_bytes = capture_input(R227_VERIFY)
    r227v = closed_wrapper(r227v_bytes, R227_VERIFY)
    del r227v_bytes
    need(
        r227v["status"] == "PASS_PARTIAL_FORMAL_ROUND227"
        and r227v["candidate_file_sha256"] == INPUT_PINS[R227_CERT]
        and r227v["candidate_result_sha256"] == digest(r227)
        and r227v["producer_imported_or_executed"] is False
        and r227v["independent_reconstruction"]["component_union_credit"] == 0,
        "R227 independent verification",
    )
    return {
        "primitive_source_sha256": INPUT_PINS[PRIMITIVE],
        "primitive_geometry_AST_reconstructed": True,
        "global_phase_map": {
            "normal": {
                "E": "(+sqrt(1-t^2),t)",
                "W": "(-sqrt(1-t^2),t)",
                "N": "(t,+sqrt(1-t^2))",
                "S": "(t,-sqrt(1-t^2))",
            },
            "source_position": "q=(9/25)*n",
            "velocity": "u=sqrt(1-p^2)*n+p*(-n_y,n_x)",
            "retained_parameter": "s",
            "quotient_equivalence": "EQUALITY_OF_(n,q,u,s)_ONLY",
        },
        "R171_certificate_sha256": INPUT_PINS[R171_CERT],
        "R171_verification_sha256": INPUT_PINS[R171_VERIFY],
        "R227_certificate_sha256": INPUT_PINS[R227_CERT],
        "R227_verification_sha256": INPUT_PINS[R227_VERIFY],
        "physical_actions": {
            "Jx": "(n_x,n_y,q_x,q_y,s,p)->(-n_x,n_y,-q_x,q_y,-s,-p)",
            "Jy": "(n_x,n_y,q_x,q_y,s,p)->(n_x,-n_y,q_x,-q_y,s,-p)",
            "JxJy": "(n_x,n_y,q_x,q_y,s,p)->(-n_x,-n_y,-q_x,-q_y,-s,p)",
        },
        "nonidentity_action_orbits_are_quotient_equivalences": False,
    }


def cardinal_normal(chart: str) -> tuple[int, int]:
    cell = chart.split(":", 1)[1]
    return {"E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1)}[cell]


def reconstruct_source_sheets() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r236_bytes = capture_input(R236)
    r236 = closed_wrapper(r236_bytes, R236)
    del r236_bytes
    partitions = r236["double_endpoint_partition_rows"]
    need(len(partitions) == 16, "R236 double partition count")
    partition_charts: dict[str, str] = {}
    for row in partitions:
        pid = row["double_endpoint_partition_row_id"]
        charts = {
            row[name]["source_chart"]
            for name in (
                "negative_to_positive_signature", "positive_to_negative_signature",
                "same_sign_event_absent_signature",
            )
        }
        need(len(charts) == 1 and next(iter(charts)) in CHARTS, "R236 chart")
        chart = next(iter(charts))
        cell = chart.split(":", 1)[1]
        need(
            row["wall"] == 0
            and row["axis"] == ("Y" if cell in {"E", "W"} else "X")
            and row["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE",
            "R236 source t=0 factor",
        )
        need(pid not in partition_charts, "R236 partition uniqueness")
        partition_charts[pid] = chart

    r248_bytes = capture_input(R248)
    sheets: list[dict[str, Any]] = []
    kinds: Counter[str] = Counter()
    for row in plain_array(r248_bytes, '"formal_wall_half_open_sheet_owner_ledger":', nested_rows=True):
        kind = row["source_partition_kind"]
        kinds[kind] += 1
        if kind == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET" and row["endpoint_factor"] == "source":
            check_row(row, "R248 source double sheet")
            pid = row["source_partition_row_id"]
            need(pid in partition_charts, "R248/R236 join")
            chart = partition_charts[pid]
            p0, p1, s0, s1 = map(Fraction, row["exact_closed_base_rectangle"])
            need((p1 < 0 or p0 > 0) and s0 <= 0 <= s1, "source sheet p excludes zero and s may meet zero")
            nx, ny = cardinal_normal(chart)
            sheets.append({
                "member_id": row["wall_sheet_node_id"],
                "partition_row_id": pid,
                "chart": chart,
                "source_t": "0",
                "source_normal": [str(nx), str(ny)],
                "source_position": [str(SOURCE_RADIUS * nx), str(SOURCE_RADIUS * ny)],
                "closed_p_s_rectangle": [str(p0), str(p1), str(s0), str(s1)],
                "p_zero_in_sheet": False,
                "s_zero_in_sheet": True,
                "owner_official_key_id": row["owner_official_key_id"],
                "owner_signature_sha256": row["owner_signature_sha256"],
                "R248_row_sha256": row["row_sha256"],
            })
    del r248_bytes
    need(kinds == {
        "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
        "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
    }, "R248 sheet census")
    need(len(sheets) == 16 and len({row["member_id"] for row in sheets}) == 16, "16 source sheets")
    need(Counter(row["chart"] for row in sheets) == {chart: 4 for chart in CHARTS}, "four sheets per chart")
    sheets.sort(key=canonical)
    return sheets, {
        "source_sheet_count": len(sheets),
        "source_sheet_chart_census": dict(sorted(Counter(row["chart"] for row in sheets).items())),
        "all_source_sheet_t_values": ["0"],
        "all_source_sheet_p_intervals_exclude_zero": True,
        "source_sheet_rows_sha256": digest(sheets),
    }


def extract_cell_bounds(cell: dict[str, Any]) -> tuple[list[str] | None, str | None, str]:
    kind = cell["witness_kind"]
    if kind == "ROUND182_GRAPH_SHEET_LEAF":
        return cell.get("exact_box"), None, GRAPH_BOUND_ROLE
    if kind == "ROUND208_DIRECT_GRAPH_SIDE_REGION":
        return cell.get("exact_leaf_box"), None, GRAPH_SIDE_BOUND_ROLE
    if kind in {
        "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
        "ROUND179_POSITIVE_T0_RETAINED_OWNER",
        "SOURCE_EXACT_T0_SHEET_CELL",
    }:
        return cell.get("exact_ambient_bounds", cell.get("exact_bounds")), None, T0_BOUND_ROLE
    need(kind == "ROUND182_TRANSVERSE_1D_LINE", "known R291 witness kind")
    retained = cell.get("containing_retained_child_row_id")
    need(type(retained) is str, "transverse retained child")
    return None, retained, TRANSVERSE_BOUND_ROLE


def load_physical_cells() -> tuple[list[dict[str, Any]], dict[str, Any], set[str]]:
    payload = capture_input(R291)
    cells: list[dict[str, Any]] = []
    keys: set[tuple[str, int]] = set()
    transverse_ids: set[str] = set()
    kinds: Counter[str] = Counter()
    bound_roles: Counter[str] = Counter()
    charts: Counter[str] = Counter()
    disposition_count = 0
    sequence = hashlib.sha256()
    for disposition in gzip_array(payload):
        check_row(disposition, "R291 disposition")
        disposition_count += 1
        did = disposition["complete_lower_stratum_local_disposition_row_id"]
        chart = disposition["source_chart"]
        need(chart in CHARTS, "R291 chart")
        for index, physical in enumerate(disposition["physical_witness_cells"]):
            key = (did, index)
            need(key not in keys, "R291 physical-key uniqueness")
            keys.add(key)
            bounds, retained, bound_role = extract_cell_bounds(physical)
            need(bound_role == BOUND_ROLE_BY_KIND[physical["witness_kind"]], "declared support-bound role")
            if bounds is None:
                need(retained not in transverse_ids, "transverse retained uniqueness")
                transverse_ids.add(retained)
                normalized = None
            else:
                need(type(bounds) is list and len(bounds) == 6, "R291 exact cell bounds")
                normalized = [str(Fraction(value)) for value in bounds]
            kind = physical["witness_kind"]
            kinds[kind] += 1
            bound_roles[bound_role] += 1
            charts[chart] += 1
            cell_hash = digest(physical)
            sequence.update(canonical([did, index, cell_hash]))
            cells.append({
                "key": key,
                "disposition_row_id": did,
                "disposition_row_sha256": disposition["row_sha256"],
                "physical_witness_cell_index": index,
                "chart": chart,
                "witness_kind": kind,
                "cell_sha256": cell_hash,
                "exact_containing_t_p_s_bounds": normalized,
                "support_bound_role": bound_role,
                "transverse_retained_child_row_id": retained,
            })
    del payload
    need(disposition_count == 55_428 and len(cells) == len(keys) == 113_452, "R291 complete frontier")
    need(kinds == EXPECTED_KINDS and len(transverse_ids) == 112, "R291 kind census")
    need(bound_roles == EXPECTED_BOUND_ROLE_CENSUS, "complete exact/containing support-bound role census")
    return cells, {
        "R291_disposition_count": disposition_count,
        "R291_physical_cell_count": len(cells),
        "R291_witness_kind_census": dict(sorted(kinds.items())),
        "support_bound_role_census": dict(sorted(bound_roles.items())),
        "all_113452_cells_have_an_explicit_exact_or_conservative_containing_bound_role": True,
        "R291_source_chart_census": dict(sorted(charts.items())),
        "R291_reduced_cell_sequence_sha256": sequence.hexdigest(),
    }, transverse_ids


def bind_transverse_boxes(cells: list[dict[str, Any]], transverse_ids: set[str]) -> dict[str, Any]:
    payload = capture_input(R179)
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    for packed in plain_array(payload, '"retained_3d_child_rows":', expected_type=list):
        count += 1
        need(len(packed) == len(R179_COLUMNS), "R179 packed width")
        if packed[0] in transverse_ids:
            need(packed[0] not in selected, "R179 selected uniqueness")
            selected[packed[0]] = dict(zip(R179_COLUMNS, packed, strict=True))
    del payload
    need(count == 106_680 and set(selected) == transverse_ids, "R179 transverse exact cover")
    for cell in cells:
        retained = cell["transverse_retained_child_row_id"]
        if retained is None:
            continue
        row = selected[retained]
        need(row["chart"] == cell["chart"], "R179/R291 chart")
        box = [str(Fraction(value)) for value in row["box"]]
        need(len(box) == 6, "R179 transverse box")
        cell["exact_containing_t_p_s_bounds"] = box
        cell["R179_retained_row_sha256"] = digest(row)
        need(cell["support_bound_role"] == TRANSVERSE_BOUND_ROLE, "R179 transverse containing-bound role")
    return {
        "R179_retained_row_count": count,
        "selected_transverse_retained_row_count": len(selected),
        "all_112_transverse_cells_bound_to_conservative_containing_R179_boxes": True,
    }


def load_bindings(
    physical_keys: set[tuple[str, int]],
) -> tuple[dict[tuple[str, int], dict[str, Any]], set[str], dict[str, Any]]:
    payload = capture_input(R295A)
    bindings: dict[tuple[str, int], dict[str, Any]] = {}
    target_ids: set[str] = set()
    refs: Counter[int] = Counter()
    classes: Counter[str] = Counter()
    for binding in gzip_array(payload):
        check_row(binding, "R295A binding")
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        need(key in physical_keys and key not in bindings, "R295A/R291 unique join")
        targets = binding["target_Round294_registry_rows"]
        ids = binding["target_Round294_registry_occurrence_ids"]
        need(
            ids == [row["registry_occurrence_id"] for row in targets]
            and len(ids) == binding["target_Round294_registry_reference_count"]
            and len(ids) > 0,
            "R295A target closure",
        )
        reduced = []
        for row in targets:
            need(row["physical_support_chart"] in CHARTS, "R295A target chart")
            reduced.append({
                "registry_occurrence_id": row["registry_occurrence_id"],
                "official_key_id": row["official_key_id"],
                "complete_10_field_return_signature_sha256": row["complete_10_field_return_signature_sha256"],
                "physical_support_chart": row["physical_support_chart"],
                "Round294_occurrence_registry_row_sha256": row["Round294_occurrence_registry_row_sha256"],
            })
            target_ids.add(row["registry_occurrence_id"])
        bindings[key] = {
            "binding_row_id": binding["Round295A_R291_physical_incidence_binding_row_id"],
            "binding_row_sha256": binding["row_sha256"],
            "binding_classification": binding["Round295A_binding_classification"],
            "source_binding_classification": binding["source_Round293_binding_classification"],
            "witness_kind": binding["witness_kind"],
            "source_chart": binding["source_chart"],
            "targets": reduced,
        }
        refs[len(ids)] += 1
        classes[binding["Round295A_binding_classification"]] += 1
    del payload
    need(len(bindings) == 113_452 and set(bindings) == physical_keys, "R295A complete bijection")
    return bindings, target_ids, {
        "R295A_binding_count": len(bindings),
        "R295A_distinct_target_occurrence_count": len(target_ids),
        "target_reference_count_census": {str(key): value for key, value in sorted(refs.items())},
        "binding_classification_census": dict(sorted(classes.items())),
    }


def load_components(selected_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    payload = capture_input(C15)
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    for row in gzip_jsonl(payload):
        count += 1
        member = row["registry_member_id"]
        if member in selected_ids:
            check_row(row, "selected C15 member")
            need(member not in selected, "C15 selected uniqueness")
            selected[member] = {
                "component_id": row["fresh_component_id"],
                "official_key_id": row["official_key_id"],
                "C15_row_sha256": row["row_sha256"],
            }
    del payload
    need(count == 502_204 and set(selected) == selected_ids, "C15 selected exact cover")
    return selected, {
        "C15_member_count": count,
        "C15_selected_member_count": len(selected),
        "C15_selected_component_count": len({row["component_id"] for row in selected.values()}),
    }


def component_relation(source: str, targets: list[dict[str, Any]]) -> str:
    same = sum(target["component_id"] == source for target in targets)
    if same == len(targets):
        return "ALL_TARGETS_SAME_C15_COMPONENT"
    if same == 0:
        return "ALL_TARGETS_CROSS_C15_COMPONENT"
    return "MIXED_SAME_AND_CROSS_C15_COMPONENT_TARGETS"


def owner_relation(sheet: dict[str, Any], targets: list[dict[str, Any]]) -> str:
    keys = [target for target in targets if target["official_key_id"] == sheet["owner_official_key_id"]]
    exact = [
        target for target in keys
        if target["complete_10_field_return_signature_sha256"] == sheet["owner_signature_sha256"]
    ]
    if exact:
        return "AT_LEAST_ONE_EXACT_OFFICIAL_KEY_AND_SIGNATURE_MATCH"
    if keys:
        return "OFFICIAL_KEY_MATCH_WITH_SIGNATURE_MISMATCH"
    return "NO_OFFICIAL_KEY_MATCH"


def action_fixed_set_audit(sheets: list[dict[str, Any]]) -> dict[str, Any]:
    action_counts: Counter[str] = Counter()
    rows = []
    for sheet in sheets:
        nx, ny = map(Fraction, sheet["source_normal"])
        qx, qy = map(Fraction, sheet["source_position"])
        p0, p1, s0, s1 = map(Fraction, sheet["closed_p_s_rectangle"])
        p_zero = p0 <= 0 <= p1
        s_zero = s0 <= 0 <= s1
        fixed = {
            "Jx": qx == nx == 0 and p_zero and s_zero,
            "Jy": qy == ny == 0 and p_zero,
            "JxJy": qx == qy == nx == ny == 0 and s_zero,
        }
        need(not any(fixed.values()), "nontrivial physical action fixed source-sheet point")
        for word, value in fixed.items():
            action_counts[word] += int(value)
        rows.append({
            "source_sheet_member_id": sheet["member_id"],
            "chart": sheet["chart"],
            "source_normal": sheet["source_normal"],
            "source_position": sheet["source_position"],
            "p_zero_in_sheet": p_zero,
            "s_zero_in_sheet": s_zero,
            "fixed_set_intersection": fixed,
            "Jx_fixed_equations": ["n_x=0", "q_x=0", "s=0", "p=0"],
            "Jy_fixed_equations": ["n_y=0", "q_y=0", "p=0"],
            "JxJy_fixed_equations": ["n_x=0", "n_y=0", "q_x=0", "q_y=0", "s=0"],
        })
    rows.sort(key=canonical)
    need(action_counts == {"Jx": 0, "Jy": 0, "JxJy": 0}, "empty nontrivial action fixed sets")
    return {
        "source_sheet_count": len(sheets),
        "Jx_fixed_sheet_point_family_count": 0,
        "Jy_fixed_sheet_point_family_count": 0,
        "JxJy_fixed_sheet_point_family_count": 0,
        "fixed_set_rows_sha256": digest(rows),
        "decisive_p_fact": "ALL_16_SOURCE_SHEET_P_INTERVALS_EXCLUDE_ZERO",
        "unit_normal_fact": "N_X_AND_N_Y_CANNOT_BOTH_BE_ZERO",
        "physical_actions_are_not_quotient_identifications": True,
    }


def solve_global_position_equation(
    source_chart: str, target_chart: str,
    t_lower: Fraction, t_upper: Fraction,
) -> dict[str, Any]:
    need(source_chart != target_chart, "cross-chart equation")
    need(-1 < t_lower <= t_upper < 1, "target t support strictly inside unit interval")
    source_cell = source_chart.split(":", 1)[1]
    target_cell = target_chart.split(":", 1)[1]
    sx, sy = cardinal_normal(source_chart)
    opposite = {"E": "W", "W": "E", "N": "S", "S": "N"}[source_cell]
    max_abs = max(abs(t_lower), abs(t_upper))
    radical_square_margin = Fraction(1) - max_abs * max_abs
    need(radical_square_margin > 0, "strict target radical-square margin")
    if target_cell == opposite:
        dominant_axis = "x" if source_cell in {"E", "W"} else "y"
        source_sign = sx if dominant_axis == "x" else sy
        target_sign = -source_sign
        return {
            "relation": "OPPOSITE_DOMINANT_CHART",
            "source_normal": [str(sx), str(sy)],
            "target_normal_formula": {
                "E": ["+sqrt(1-t^2)", "t"],
                "W": ["-sqrt(1-t^2)", "t"],
                "N": ["t", "+sqrt(1-t^2)"],
                "S": ["t", "-sqrt(1-t^2)"],
            }[target_cell],
            "decisive_equation_axis": dominant_axis,
            "source_dominant_coordinate_sign": "POSITIVE" if source_sign > 0 else "NEGATIVE",
            "target_dominant_coordinate_sign": "POSITIVE" if target_sign > 0 else "NEGATIVE",
            "target_radical_square_minimum_margin": str(radical_square_margin),
            "normal_equality_solution_set": "EMPTY_BY_OPPOSITE_STRICT_SIGN",
            "position_equality_solution_set": "EMPTY_BECAUSE_Q=(9/25)N_AND_9/25_IS_NONZERO",
            "required_target_t": None,
            "target_t_solution_intersects_support": False,
            "route": "EXACT_NONINCIDENCE__GLOBAL_NORMAL_AND_POSITION_OPPOSITE_STRICT_SIGN",
        }

    need(target_cell not in {source_cell, opposite}, "perpendicular target chart")
    required = Fraction(sx if source_cell in {"E", "W"} else sy)
    need(required in {Fraction(-1), Fraction(1)}, "unit target endpoint")
    gap = required - t_upper if required == 1 else t_lower - required
    need(gap > 0, "required target endpoint excluded")
    return {
        "relation": "PERPENDICULAR_DOMINANT_CHART",
        "source_normal": [str(sx), str(sy)],
        "target_normal_formula": {
            "E": ["+sqrt(1-t^2)", "t"],
            "W": ["-sqrt(1-t^2)", "t"],
            "N": ["t", "+sqrt(1-t^2)"],
            "S": ["t", "-sqrt(1-t^2)"],
        }[target_cell],
        "component_equation_forces_target_t": str(required),
        "remaining_component_equation_forces_sqrt_1_minus_t_squared": "0",
        "normal_equality_solution_set": "SINGLE_FORMAL_UNIT_ENDPOINT",
        "position_equality_solution_set": "SAME_FORMAL_UNIT_ENDPOINT_BECAUSE_Q=(9/25)N",
        "required_target_t": str(required),
        "target_t_support": [str(t_lower), str(t_upper)],
        "exact_gap_from_required_endpoint": str(gap),
        "target_t_solution_intersects_support": False,
        "route": "EXACT_NONINCIDENCE__GLOBAL_NORMAL_AND_POSITION_EQUALITY_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT",
    }


def closed_row(body: dict[str, Any]) -> dict[str, Any]:
    row = dict(body)
    row["row_sha256"] = digest(row)
    return row


def build_cohorts(
    sheets: list[dict[str, Any]], cells: list[dict[str, Any]],
    bindings: dict[tuple[str, int], dict[str, Any]],
    components: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    for sheet in sheets:
        member = sheet["member_id"]
        need(member in components, "source sheet C15 binding")
        need(components[member]["official_key_id"] == sheet["owner_official_key_id"], "source sheet C15 key")
        sheet["component_id"] = components[member]["component_id"]
        sheet["C15_row_sha256"] = components[member]["C15_row_sha256"]

    states: dict[tuple[Any, ...], dict[str, Any]] = {}
    routes: Counter[str] = Counter()
    relations: Counter[str] = Counter()
    component_census: Counter[str] = Counter()
    owner_census: Counter[str] = Counter()
    bound_role_pair_census: Counter[str] = Counter()
    cross_count = 0
    same_chart_count = 0
    direct_solution_count = 0
    cross_component_witness_count = 0
    global_lower: Fraction | None = None
    global_upper: Fraction | None = None
    minimum_endpoint_gap: Fraction | None = None
    minimum_radical_margin: Fraction | None = None

    for cell in cells:
        bounds = cell["exact_containing_t_p_s_bounds"]
        bound_role = cell["support_bound_role"]
        need(
            bound_role == BOUND_ROLE_BY_KIND[cell["witness_kind"]]
            and bound_role in EXPECTED_BOUND_ROLE_CENSUS,
            "cell support-bound role/kind closure",
        )
        need(type(bounds) is list and len(bounds) == 6, "all cells exact-or-containing bounds")
        t_lower, t_upper = Fraction(bounds[0]), Fraction(bounds[1])
        need(-1 < t_lower <= t_upper < 1, "cell strict t support")
        global_lower = t_lower if global_lower is None else min(global_lower, t_lower)
        global_upper = t_upper if global_upper is None else max(global_upper, t_upper)
        binding = bindings[cell["key"]]
        need(
            binding["source_chart"] == cell["chart"]
            and binding["witness_kind"] == cell["witness_kind"],
            "R291/R295A cell semantics",
        )
        targets = []
        for target in binding["targets"]:
            member = target["registry_occurrence_id"]
            need(member in components, "target C15 binding")
            need(
                target["physical_support_chart"] == cell["chart"]
                and components[member]["official_key_id"] == target["official_key_id"],
                "target chart/key/component consistency",
            )
            targets.append({**target, **components[member]})

        for sheet in sheets:
            if sheet["chart"] == cell["chart"]:
                same_chart_count += 1
                continue
            cross_count += 1
            bound_role_pair_census[bound_role] += 1
            proof = solve_global_position_equation(sheet["chart"], cell["chart"], t_lower, t_upper)
            same_position_possible = proof["target_t_solution_intersects_support"]
            direct_solution_count += int(same_position_possible)
            if proof["relation"] == "PERPENDICULAR_DOMINANT_CHART":
                gap = Fraction(proof["exact_gap_from_required_endpoint"])
                minimum_endpoint_gap = gap if minimum_endpoint_gap is None else min(minimum_endpoint_gap, gap)
            else:
                margin = Fraction(proof["target_radical_square_minimum_margin"])
                minimum_radical_margin = margin if minimum_radical_margin is None else min(minimum_radical_margin, margin)

            comp = component_relation(sheet["component_id"], targets)
            own = owner_relation(sheet, targets)
            any_cross = any(target["component_id"] != sheet["component_id"] for target in targets)
            if same_position_possible and any_cross:
                sheet_ps = tuple(Fraction(value) for value in sheet["closed_p_s_rectangle"])
                target_ps = tuple(Fraction(value) for value in bounds[2:6])
                p_overlap = min(sheet_ps[1], target_ps[1]) >= max(sheet_ps[0], target_ps[0])
                s_overlap = min(sheet_ps[3], target_ps[3]) >= max(sheet_ps[2], target_ps[2])
                if p_overlap and s_overlap:
                    cross_component_witness_count += 1
                    raise GateFailure(
                        "LEGAL_CROSS_COMPONENT_GLOBAL_PHASE_QUOTIENT_WITNESS:"
                        + sheet["member_id"] + ":" + cell["disposition_row_id"]
                    )

            representative = {
                "source_sheet_member_id": sheet["member_id"],
                "source_sheet_chart": sheet["chart"],
                "source_sheet_component_id": sheet["component_id"],
                "source_sheet_normal": sheet["source_normal"],
                "source_sheet_position": sheet["source_position"],
                "source_sheet_p_s_rectangle": sheet["closed_p_s_rectangle"],
                "R291_disposition_row_id": cell["disposition_row_id"],
                "physical_witness_cell_index": cell["physical_witness_cell_index"],
                "physical_witness_cell_sha256": cell["cell_sha256"],
                "target_cell_chart": cell["chart"],
                "target_cell_witness_kind": cell["witness_kind"],
                "target_exact_containing_t_p_s_bounds": bounds,
                "R295A_binding_row_id": binding["binding_row_id"],
                "target_registry_occurrence_ids": [target["registry_occurrence_id"] for target in targets],
                "target_component_ids": [target["component_id"] for target in targets],
                "global_phase_position_solution_intersects_target_support": same_position_possible,
            }
            key = (
                sheet["chart"], cell["chart"], cell["witness_kind"],
                proof["relation"], proof["route"], comp, own,
                len(targets), binding["binding_classification"],
            )
            state = states.get(key)
            if state is None:
                state = {
                    "multiplicity": 0,
                    "representative": representative,
                    "representative_bytes": canonical(representative),
                    "proof": proof,
                    "minimum_t_lower": t_lower,
                    "maximum_t_upper": t_upper,
                    "minimum_endpoint_gap": (
                        None if proof["relation"] != "PERPENDICULAR_DOMINANT_CHART"
                        else Fraction(proof["exact_gap_from_required_endpoint"])
                    ),
                    "minimum_radical_margin": (
                        None if proof["relation"] != "OPPOSITE_DOMINANT_CHART"
                        else Fraction(proof["target_radical_square_minimum_margin"])
                    ),
                }
                states[key] = state
            else:
                encoded = canonical(representative)
                if encoded < state["representative_bytes"]:
                    state["representative"] = representative
                    state["representative_bytes"] = encoded
                state["minimum_t_lower"] = min(state["minimum_t_lower"], t_lower)
                state["maximum_t_upper"] = max(state["maximum_t_upper"], t_upper)
                if proof["relation"] == "PERPENDICULAR_DOMINANT_CHART":
                    gap = Fraction(proof["exact_gap_from_required_endpoint"])
                    state["minimum_endpoint_gap"] = min(state["minimum_endpoint_gap"], gap)
                else:
                    margin = Fraction(proof["target_radical_square_minimum_margin"])
                    state["minimum_radical_margin"] = min(state["minimum_radical_margin"], margin)
            state["multiplicity"] += 1
            routes[proof["route"]] += 1
            relations[proof["relation"]] += 1
            component_census[comp] += 1
            owner_census[own] += 1

    need(cross_count == 1_361_424 and same_chart_count == 453_808, "complete cross/same chart partition")
    need(direct_solution_count == cross_component_witness_count == 0, "zero global phase quotient solutions")
    need(routes == {
        "EXACT_NONINCIDENCE__GLOBAL_NORMAL_AND_POSITION_OPPOSITE_STRICT_SIGN": 453_808,
        "EXACT_NONINCIDENCE__GLOBAL_NORMAL_AND_POSITION_EQUALITY_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT": 907_616,
    }, "explicit equation route census")
    need(relations == {
        "OPPOSITE_DOMINANT_CHART": 453_808,
        "PERPENDICULAR_DOMINANT_CHART": 907_616,
    }, "explicit equation relation census")
    need(minimum_endpoint_gap is not None and minimum_radical_margin is not None, "global exact margins")
    need(
        bound_role_pair_census
        == Counter({role: count * 12 for role, count in EXPECTED_BOUND_ROLE_CENSUS.items()}),
        "every cross-chart proof evaluated on its declared exact-or-containing support envelope",
    )

    rows = []
    for key, state in states.items():
        body = {
            "schema": "cm2.c27-semantic-counterexample-gate.explicit-quotient-map-alias.zero-credit.v2.equation-cohort-row.v1",
            "cohort_id": "c27-explicit-quotient-cohort:" + digest(list(key)),
            "source_sheet_chart": key[0],
            "target_cell_chart": key[1],
            "target_cell_witness_kind": key[2],
            "global_chart_relation": key[3],
            "route": key[4],
            "C15_component_relation": key[5],
            "owner_key_signature_relation": key[6],
            "target_reference_count": key[7],
            "R295A_binding_classification": key[8],
            "multiplicity": state["multiplicity"],
            "cohort_t_lower_minimum": str(state["minimum_t_lower"]),
            "cohort_t_upper_maximum": str(state["maximum_t_upper"]),
            "minimum_exact_endpoint_gap": (
                None if state["minimum_endpoint_gap"] is None
                else str(state["minimum_endpoint_gap"])
            ),
            "minimum_exact_radical_square_margin": (
                None if state["minimum_radical_margin"] is None
                else str(state["minimum_radical_margin"])
            ),
            "explicit_global_phase_equation_proof": state["proof"],
            "canonical_representative": state["representative"],
            "p_s_equations_can_only_restrict_and_cannot_restore_an_empty_normal_position_solution": True,
            "same_physical_point_witness_count": 0,
            "formal_component_edge_credit": 0,
            "formal_maximality_credit": 0,
        }
        rows.append(closed_row(body))
    rows.sort(key=canonical)
    need(sum(row["multiplicity"] for row in rows) == cross_count, "cohort multiplicity exact cover")
    need(len(rows) == 128 and len({row["cohort_id"] for row in rows}) == 128, "128 injective cohorts")
    return rows, {
        "complete_source_sheet_by_R291_physical_cell_product": 16 * 113_452,
        "same_chart_pair_count": same_chart_count,
        "cross_chart_pair_count": cross_count,
        "cross_chart_identity": "113452 physical cells * 12 nonmatching-chart source sheets",
        "explicit_equation_route_census": dict(sorted(routes.items())),
        "global_chart_relation_census": dict(sorted(relations.items())),
        "C15_component_relation_census": dict(sorted(component_census.items())),
        "owner_key_signature_relation_census": dict(sorted(owner_census.items())),
        "support_bound_role_pair_census": dict(sorted(bound_role_pair_census.items())),
        "exact_lower_dimensional_support_pair_count": bound_role_pair_census[T0_BOUND_ROLE],
        "conservative_containing_envelope_pair_count": (
            cross_count - bound_role_pair_census[T0_BOUND_ROLE]
        ),
        "proof_evaluated_on_declared_t_envelope_for_every_cross_chart_pair": True,
        "actual_support_is_equal_to_or_a_subset_of_each_declared_envelope": True,
        "nonincidence_on_each_containing_envelope_implies_nonincidence_on_its_actual_support_subset": True,
        "global_exact_t_lower_minimum": str(global_lower),
        "global_exact_t_upper_maximum": str(global_upper),
        "minimum_exact_gap_from_required_unit_endpoint": str(minimum_endpoint_gap),
        "minimum_exact_opposite_chart_radical_square_margin": str(minimum_radical_margin),
        "direct_global_phase_quotient_solution_count": direct_solution_count,
        "confirmed_cross_component_same_physical_point_witness_count": cross_component_witness_count,
        "unresolved_cross_chart_pair_count": 0,
        "equation_cohort_count": len(rows),
        "equation_cohort_multiplicity_sum": sum(row["multiplicity"] for row in rows),
        "equation_cohort_rows_sha256": digest(rows),
        "each_cross_chart_pair_has_exactly_one_route": True,
    }


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    runtime_seed_contract = validate_seed_runtime()
    independence_audit = validate_independent_input_boundary()
    authority = validate_geometry_authorities()
    sheets, sheet_audit = reconstruct_source_sheets()
    fixed_audit = action_fixed_set_audit(sheets)
    cells, cell_audit, transverse_ids = load_physical_cells()
    transverse_audit = bind_transverse_boxes(cells, transverse_ids)
    physical_keys = {cell["key"] for cell in cells}
    bindings, target_ids, binding_audit = load_bindings(physical_keys)
    selected_ids = target_ids | {sheet["member_id"] for sheet in sheets}
    components, component_audit = load_components(selected_ids)
    rows, equation_audit = build_cohorts(sheets, cells, bindings, components)
    independence_audit_after = validate_independent_input_boundary()
    need(independence_audit_after == independence_audit, "independent input boundary stable through reconstruction")
    result = {
        "schema": "cm2.c27-semantic-counterexample-gate.explicit-quotient-map-alias.zero-credit.v2",
        "status": "PASS_ZERO_CREDIT__EXPLICIT_GLOBAL_PHASE_QUOTIENT_MAP_CLOSES_1361424_CROSS_CHART_PAIRS__JX_JY_JXJY_NONGLUE_FIXED_SETS_EMPTY_ON_16_SOURCE_SHEETS__C27_REJECT_UNCHANGED",
        "subgate_decision": "PASS_DIAGNOSTIC_ZERO_CREDIT__NO_GLOBAL_PHASE_QUOTIENT_WITNESS",
        "unconditional_C27_C28_C29_decision": "REJECT_REMAINS_IN_FORCE",
        "scope_contract": {
            "semantic_family": "ALIAS_RECHART_HANDOFF",
            "candidate_universe": "COMPLETE_16_SOURCE_SHEETS_X_COMPLETE_113452_R291_PHYSICAL_CELLS_PARTITIONED_BY_EQUAL_OR_UNEQUAL_CHART",
            "Round306C27_imported_or_executed": False,
            "Round306C27_FAMILIES_copied": False,
            "edge_ledger_used_as_candidate_universe": False,
            "first_alias_probe_imported_executed_or_read": False,
            "first_alias_chart_relation_function_reused": False,
            "first_alias_result_or_conclusion_used": False,
            "all_inputs_O_NOFOLLOW_single_byte_capture": True,
            "input_hashing_and_parsing_use_identical_captured_bytes": True,
            "input_path_content_reread_count": 0,
            "runtime_input_and_import_boundary": independence_audit,
        },
        "runtime_seed_contract": runtime_seed_contract,
        "primitive_global_phase_map_authority": authority,
        "source_sheet_reconstruction": sheet_audit,
        "nontrivial_physical_action_fixed_set_audit": fixed_audit,
        "physical_cell_reconstruction": {**cell_audit, **transverse_audit},
        "registry_component_binding": {**binding_audit, **component_audit},
        "explicit_global_phase_equation_certificate": equation_audit,
        "counterexample_gate": {
            "counterexample_first": True,
            "global_phase_quotient_equation_is_the_only_same_point_test": True,
            "physical_symmetry_orbit_used_as_same_point_test": False,
            "confirmed_legal_cross_component_witness_count": 0,
            "verdict": "NO_WITNESS_IN_THE_EXACT_1361424_CROSS_CHART_PAIR_DENOMINATOR",
        },
        "independent_implementation_boundary": {
            "semantic_code_path_is_distinct_from_alias_v1": True,
            "explicit_n_q_u_s_equations_replace_chart_relation_labels": True,
            "Jx_Jy_JxJy_actions_applied_and_fixed_sets_solved": True,
            "shared_frozen_inputs_do_not_make_the_semantic_implementations_identical": True,
            "double_seed_byte_identity_proves_hash_order_determinism_only": True,
        },
        "diagnostic_composition_only": {
            "alias_cross_chart_pairs_closed_here": 1_361_424,
            "same_chart_transverse_pairs_closed_by_separate_subgate": 448,
            "lower_owner_contacts_remain_REJECT_unresolved": 24,
            "current_graph_side_cross_chart_pairs_remaining": 192,
            "remaining_REJECT_residual_sum": 216,
            "not_formal_C27_authority": True,
        },
        "formal_credit": {
            "whole_origin_credit": 0,
            "component_edge_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "maximality_credit": 0,
            "C27_credit": 0,
            "C28_credit": 0,
            "C29_credit": 0,
        },
        "strict_nonpromotion": {
            "CM2": "NO-GO_FOR_CLAIM",
            "D02": "BLOCKED",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_18_field_global_blocks": 0,
        },
        "required_next": [
            "independently route the 192 current-graph-side cross-chart pairs with exact support rather than containing boxes",
            "materialize the missing p/s lower-owner physical-support-to-C15 handoff for the 24 rejected contacts",
            "extend the counterexample-first semantic gate to every remaining C27 transition family",
        ],
        "input_capture_records": {name: CAPTURE_RECORDS[name] for name in sorted(CAPTURE_RECORDS)},
    }
    return rows, result


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    target = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=target, mtime=0) as stream:
        stream.write(raw)
    return target.getvalue()


def result_bytes(result: dict[str, Any]) -> bytes:
    return canonical({
        "result": result,
        "result_sha256": digest(result),
        "schema": "cm2.c27-semantic-counterexample-gate.explicit-quotient-map-alias.zero-credit.v2.wrapper.v1",
    }) + b"\n"


def manifest_bytes(ledger: bytes, result: bytes) -> bytes:
    members = [
        {"name": LEDGER, "sha256": hashlib.sha256(ledger).hexdigest(), "size": len(ledger)},
        {"name": RESULT, "sha256": hashlib.sha256(result).hexdigest(), "size": len(result)},
    ]
    body = {
        "schema": "cm2.c27-semantic-counterexample-gate.explicit-quotient-map-alias.zero-credit.v2.manifest.v1",
        "member_count": 2,
        "members": members,
        "members_sha256": digest(members),
        "formal_credit": 0,
    }
    return canonical({"manifest": body, "manifest_sha256": digest(body)}) + b"\n"


def exclusive_write(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def read_output(path: Path) -> bytes:
    before = os.lstat(path)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            "nofollow output:" + path.name,
        )
        chunks = []
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            chunks.append(block)
        data = b"".join(chunks)
        need(len(data) == opened.st_size, "output size:" + path.name)
        return data
    finally:
        os.close(descriptor)


def verify_directory(directory: Path, expected: dict[str, bytes]) -> None:
    info = os.lstat(directory)
    need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode), "output directory")
    need(sorted(path.name for path in directory.iterdir()) == sorted(expected), "exact output graph")
    for name, payload in expected.items():
        need(read_output(directory / name) == payload, "output bytes:" + name)
    wrapper = strict_loads(expected[RESULT])
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "result closure")
    wrapper = strict_loads(expected[MANIFEST])
    manifest = wrapper["manifest"]
    need(wrapper["manifest_sha256"] == digest(manifest), "manifest closure")
    need(manifest["members_sha256"] == digest(manifest["members"]), "manifest member closure")
    for member in manifest["members"]:
        payload = expected[member["name"]]
        need(member["size"] == len(payload) and member["sha256"] == hashlib.sha256(payload).hexdigest(), "manifest member:" + member["name"])


def rename_noreplace(source: Path, destination: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    rc = function(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    if rc != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise GateFailure("output exists:" + destination.name)
        raise OSError(code, os.strerror(code), str(destination))


def cleanup_staging(directory: Path) -> None:
    if not directory.exists():
        return
    for name in (LEDGER, RESULT, MANIFEST):
        path = directory / name
        try:
            if path.exists() or path.is_symlink():
                os.chmod(path, 0o600, follow_symlinks=False)
                os.unlink(path)
        except OSError:
            pass
    try:
        os.chmod(directory, 0o700)
        os.rmdir(directory)
    except OSError:
        pass


def publish(output: Path, rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    ledger = gzip_rows(rows)
    result_payload = result_bytes(result)
    manifest_payload = manifest_bytes(ledger, result_payload)
    expected = {LEDGER: ledger, RESULT: result_payload, MANIFEST: manifest_payload}
    staging = AUDIT_ROOT / f".{PREFIX}.staging-{os.getpid()}-{secrets.token_hex(8)}"
    need(not staging.exists() and staging.parent == AUDIT_ROOT, "fresh direct staging")
    os.mkdir(staging, 0o700)
    try:
        for name, payload in expected.items():
            exclusive_write(staging / name, payload)
        verify_directory(staging, expected)
        recheck_capture_metadata()
        for name in expected:
            os.chmod(staging / name, 0o444, follow_symlinks=False)
        os.chmod(staging, 0o555)
        rename_noreplace(staging, output)
    except BaseException:
        cleanup_staging(staging)
        raise
    verify_directory(output, expected)
    recheck_capture_metadata()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,126}[a-z0-9]", args.output_tag) is not None, "safe output tag")
    AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
    need(AUDIT_ROOT.is_dir() and not AUDIT_ROOT.is_symlink(), "audit root")
    output = AUDIT_ROOT / args.output_tag
    need(output.parent == AUDIT_ROOT and output.resolve(strict=False).parent == AUDIT_ROOT.resolve(strict=True), "direct output")
    need(not output.exists() and not output.is_symlink(), "fresh output")
    try:
        rows, result = reconstruct()
        recheck_capture_metadata()
        publish(output, rows, result)
        print(canonical({
            "status": result["status"],
            "result_sha256": digest(result),
            "equation_cohort_count": len(rows),
            "cross_chart_pair_count": 1_361_424,
            "confirmed_witness_count": 0,
            "unresolved_pair_count": 0,
            "formal_credit": 0,
        }).decode("ascii"))
        return 0
    finally:
        close_capture_fds()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as error:
        close_capture_fds()
        print("GATE_FAILURE:" + str(error), file=sys.stderr)
        raise SystemExit(2)
