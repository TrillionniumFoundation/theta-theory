#!/usr/bin/env python3
"""Independent, no-C41-producer-import auditor for the C41 depth-three atlas.

The core consumes the frozen C40 candidate and its independent audit, then
reconstructs every C41 row from lower, pinned mathematical kernels.  A normal
invocation runs the core twice in fresh processes, requires byte-identical
projections, recaptures the candidate bytes, and atomically writes a closed
terminal audit object.  This provisional source deliberately carries PENDING
pins and therefore cannot authorize a formal audit yet.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import itertools
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from types import MappingProxyType
from typing import Any

import flint
from flint import ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as round139
import cm2_round166_multi_candidate_refinement_prototype as round166
import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c39_d02_h1_c1_graph_cell_router_v1 as c39
import cm2_round306c40_d02_h1_endpoint_collision2_arrangement_independent_auditor_v1 as c40a


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
PRODUCER = DELIVERABLES / (
    "cm2_round306c41_d02_lower_strata_depth3_closure_v1.py"
)

# These three authority values are intentionally impossible until the C41
# producer is formally pinned, its candidate is minted, and the C40 audit is
# complete.  Do not replace them from a provisional run.
EXPECTED_PRODUCER_SOURCE = (
    "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
)
EXPECTED_CANDIDATE_OBJECT = (
    "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
)
EXPECTED_C40_AUDIT_OBJECT = (
    "4acfe9cf77f4e394458a32c0f341bc679768fc3f137ea9d6f6362cc68df9e485"
)
EXPECTED_C40_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C40_DIMENSION_SAFE_OUTER_AUDIT__"
    "31_OF_31_ATTACKS_FAIL_CLOSED"
)

EXPECTED_C40_OBJECT = (
    "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba"
)
EXPECTED_C39_SOURCE = (
    "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae"
)
EXPECTED_C40_AUDITOR_SOURCE = (
    "1cccec33cf7768b5797ca0b05f74812a300fb4b323859a10e9495f3e73d8a0be"
)
EXPECTED_C40_PRODUCER_SOURCE = (
    "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57"
)

SCHEMA = "cm2.round306c41.d02-lower-strata-depth3-closure.independent-audit.v1"
CANDIDATE_SCHEMA = "cm2.round306c41.d02-lower-strata-depth3-closure.v1"
C40_AUDIT_SCHEMA = (
    "cm2.round306c40.d02-h1-endpoint-collision2-arrangement.independent-audit.v1"
)
RECEIPT_SCHEMA = CANDIDATE_SCHEMA + ".execution-receipt"

CROSSWALK_SCHEMA = CANDIDATE_SCHEMA + ".input-blocker-crosswalk"
AMBIENT_SCHEMA = CANDIDATE_SCHEMA + ".routed-ambient-cell"
SPLIT_SCHEMA = CANDIDATE_SCHEMA + ".split-face-adjacency"
CACHE_REPLAY_SCHEMA = CANDIDATE_SCHEMA + ".full-chart-cache-replay"
SINGLETON_SCHEMA = CANDIDATE_SCHEMA + ".candidate-universe-singleton"
C1_OUTER_SCHEMA = CANDIDATE_SCHEMA + ".c1-h1-surface-outer"
ENDPOINT_SCHEMA = CANDIDATE_SCHEMA + ".endpoint-rechart"
C2_OUTER_SCHEMA = CANDIDATE_SCHEMA + ".c2-surface-outer"
INCIDENCE_SCHEMA = CANDIDATE_SCHEMA + ".incidence-outer"
BOUNDARY_SCHEMA = CANDIDATE_SCHEMA + ".boundary-corner-outer"
PARENT_SCHEMA = CANDIDATE_SCHEMA + ".parent-conservation"
NORMALIZED_SURFACE_REGISTRY_SCHEMA = (
    CANDIDATE_SCHEMA + ".nested-normalized-surface-registry.v1"
)

LEDGER_NAMES = (
    "input_blocker_crosswalk.jsonl.gz",
    "routed_ambient_cells.jsonl.gz",
    "split_face_adjacency.jsonl.gz",
    "full_chart_cache_replay.jsonl.gz",
    "candidate_universe_singletons.jsonl.gz",
    "c1_h1_surface_outers.jsonl.gz",
    "endpoint_recharts.jsonl.gz",
    "c2_surface_outers.jsonl.gz",
    "incidence_outers.jsonl.gz",
    "boundary_corner_outers.jsonl.gz",
    "parent_conservation.jsonl.gz",
)
INVENTORY = frozenset(
    (*LEDGER_NAMES, "C41_LOWER_STRATA_PARTIAL.lock", "result.json", "root_manifest.sha256")
)
EXPECTED_NONPROMOTION_LOCK = (
    b"C41 performs a fixed maximum of three exact dyadic ambient splits "
    b"after C40, repairs the omitted W:W candidate cache, and materializes "
    b"surface, endpoint, incidence, boundary, corner and conservation "
    b"outers. Only complete uniformly excluded closed ambient parents earn "
    b"paired coarse-cell credit. Every graph, endpoint, seam, incidence, "
    b"corner, collision-three-ready or evaluation-failure obligation earns "
    b"zero D02/D03/D04/Gate5/CM2 credit. This object is partial.\n"
)

PRECISION_BITS = 384
EXTRA_DEPTH = 3
FROZEN_OWNER = "W[1,0]"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{15,127}\Z")

EXPECTED_C40_ROW_COUNT = 35_009
EXPECTED_C40_TERMINAL_ROW_COUNT = 21_951
EXPECTED_C40_COLLISION3_READY_ROW_COUNT = 660
EXPECTED_LOWER_BLOCKER_COUNT = 12_398
EXPECTED_CACHE_REPLAY_CENSUS = {
    "UNRESOLVED_C40_LIVE_COLLISION2_ORIGINAL_MATCH_NEEDS_COLLISION3_1648": 7,
    "UNRESOLVED_C40_LIVE_COLLISION2_REFLECTED_MATCH_NEEDS_COLLISION3_1648": 12,
}
LOWER_BLOCKER_CENSUS = {
    "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE": 218,
    "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY": 1147,
    "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT": 3550,
    "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL": 29,
    "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER": 19,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_1": 1362,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_2": 140,
    "UNRESOLVED_C40_COLLISION2_ACTIVE_DELTA_3": 3,
    "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION": 88,
    "UNRESOLVED_C40_COLLISION2_OUTGOING_H2": 2327,
    "UNRESOLVED_C40_COLLISION2_POINT_WINNER_NONSTRICT": 1804,
    "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT": 1511,
    "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_EVALUATION_FAILURE_OUTER": 200,
}
CHART_ORDER = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
EXPECTED_CHART_CANDIDATES = {
    "G:E": (57, "d02bd7d102705087f2ee15af47a52d3a2c15495f690d39d8c17939a3843d7808"),
    "G:W": (57, "47276a2b2d2e428ba50326b6fc620a85045f58bf6e057d571716acb2dc55dccc"),
    "G:N": (57, "c3cb961313f9e229809fb695713b410f2663a3858c0d11f2398842c70efa365e"),
    "G:S": (57, "2fa312582b254c8994ddaf24e011bff88eaa7ac516320bf0bdf41ab07079640a"),
    "W:E": (55, "ebeeae12ba192d7808031ebf4be3537fb49e73e17295404adcad371045e7c2e7"),
    "W:W": (55, "a7b777d2bf74577fafef77eafa1da6237883e5e6420352772395978a146b9a49"),
    "W:N": (55, "4719c19ccb8c63288e8815c4b8961f64d9d096dd4377641acafbec59c00769e5"),
    "W:S": (55, "89d699755e74a71b2771fb907e3f1bcf0e13d96621a977a4731c563cb928a5f8"),
}
EXPECTED_OFFICIAL_REGISTRY_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)
EXPECTED_SOURCE_SHA256 = {
    "C40": EXPECTED_C40_PRODUCER_SOURCE,
    "C39": EXPECTED_C39_SOURCE,
    "C38": "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d",
    "Round185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "Round166": "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "candidate_generator": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
}
EXPECTED_UPSTREAM_OBJECTS = {
    "C39": c40a.C39_OBJECT,
    "C38": c40a.C38_OBJECT,
    "C37": c40a.C37_OBJECT,
    "C36": c40a.C36_OBJECT,
    "C35": c40a.C35_OBJECT,
    "C34": c40a.C34_OBJECT,
    "C32": c40a.C32_OBJECT,
}


Reject = c40a.Reject
need = c40a.need
canonical = c40a.canonical
digest = c40a.digest
bytes_sha256 = c40a.bytes_sha256
file_sha256 = c40a.file_sha256
stable_read = c40a.stable_read
strict_json_bytes = c40a.strict_json_bytes
closed_object = c40a.closed_object
capture_directory = c40a.capture_directory
validate_manifest_payloads = c40a.validate_manifest_payloads
read_ledger_raw = c40a.read_ledger_raw


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def row_closed(value: dict[str, Any]) -> dict[str, Any]:
    semantic = copy.deepcopy(value)
    semantic["row_sha256"] = digest(semantic)
    return semantic


def require_row_id(
    row: dict[str, Any], field: str, prefix: str, label: str,
) -> None:
    semantic = dict(row)
    observed = semantic.pop(field, None)
    need(observed == prefix + digest(semantic), "row ID closure:" + label)


def formal_pins_ready() -> None:
    need(
        HEX64.fullmatch(EXPECTED_PRODUCER_SOURCE) is not None
        and HEX64.fullmatch(EXPECTED_CANDIDATE_OBJECT) is not None
        and HEX64.fullmatch(EXPECTED_C40_OBJECT) is not None
        and HEX64.fullmatch(EXPECTED_C40_AUDIT_OBJECT) is not None
        and EXPECTED_C40_AUDIT_STATUS.startswith("PASS_"),
        "formal C41/C40 audit pins pending",
    )


def no_producer_import() -> None:
    source = Path(__file__).read_bytes()
    tree = ast.parse(source)
    forbidden = PRODUCER.stem
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name != forbidden for alias in node.names), "C41 producer import")
        elif isinstance(node, ast.ImportFrom):
            need(node.module != forbidden, "C41 producer import-from")
    producer_path = PRODUCER.resolve()
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename is not None:
            need(Path(filename).resolve() != producer_path, "C41 producer loaded")


def source_pins() -> dict[str, str]:
    no_producer_import()
    lower = c40a.source_pins()
    observed = {
        "C39": file_sha256(Path(c39.__file__).resolve()),
        "C40_independent_auditor": file_sha256(Path(c40a.__file__).resolve()),
        **lower,
    }
    need(observed["C39"] == EXPECTED_C39_SOURCE, "C39 source pin")
    need(
        observed["C40_independent_auditor"] == EXPECTED_C40_AUDITOR_SOURCE,
        "C40 independent auditor source pin",
    )
    return observed


def capture_c41_candidate(
    candidate: Path,
) -> tuple[
    dict[str, Any],
    dict[str, list[dict[str, Any]]],
    str,
    tuple[int, ...],
    dict[str, tuple[int, ...]],
]:
    payloads, directory_identity, file_identities = capture_directory(
        candidate,
        INVENTORY,
        {
            "result.json": 32 << 20,
            "root_manifest.sha256": 2 << 20,
            "C41_LOWER_STRATA_PARTIAL.lock": 1 << 20,
        },
        "C41",
    )
    validate_manifest_payloads(payloads, "root_manifest.sha256", "C41")
    need(
        payloads["C41_LOWER_STRATA_PARTIAL.lock"] == EXPECTED_NONPROMOTION_LOCK,
        "C41 exact nonpromotion lock bytes",
    )
    result = strict_json_bytes(payloads["result.json"], "C41 result")
    closed_object(result, "C41 result")
    need(
        result.get("schema") == CANDIDATE_SCHEMA
        and result.get("object_sha256") == EXPECTED_CANDIDATE_OBJECT,
        "C41 pinned result",
    )
    descriptors = result.get("ledgers")
    need(type(descriptors) is dict, "C41 ledger descriptors")
    rows: dict[str, list[dict[str, Any]]] = {}
    for filename in LEDGER_NAMES:
        descriptor = next(
            (
                item for item in descriptors.values()
                if type(item) is dict and item.get("filename") == filename
            ),
            None,
        )
        need(type(descriptor) is dict, "C41 descriptor:" + filename)
        rows[filename] = read_ledger_raw(payloads[filename], descriptor, filename)
    need(
        len(rows["input_blocker_crosswalk.jsonl.gz"]) == EXPECTED_LOWER_BLOCKER_COUNT
        and len(rows["candidate_universe_singletons.jsonl.gz"]) == 448
        and len(rows["parent_conservation.jsonl.gz"]) == 862
        and len(rows["full_chart_cache_replay.jsonl.gz"]) == 19,
        "C41 fixed ledger censuses",
    )
    return (
        result,
        rows,
        bytes_sha256(payloads["root_manifest.sha256"]),
        directory_identity,
        file_identities,
    )


def canonical_authority_path(text: Any, label: str) -> Path:
    need(type(text) is str, label + " path type")
    path = (ROOT / text).resolve(strict=True)
    need(str(path.relative_to(ROOT)) == text, label + " canonical relative path")
    return path


def within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def require_disjoint_targets(
    targets: tuple[tuple[str, Path], ...],
    protected: tuple[tuple[str, Path], ...],
) -> None:
    for target_label, target in targets:
        for authority_label, authority in protected:
            need(
                target != authority
                and not within(target, authority)
                and not within(authority, target),
                f"{target_label} disjoint from {authority_label}",
            )


def canonical_future_target(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    resolved = absolute.resolve(strict=False)
    need(
        absolute == resolved
        and within(resolved, ROOT)
        and resolved != ROOT,
        label + " canonical workspace path",
    )
    ancestor = resolved.parent
    while not ancestor.exists():
        need(ancestor != ROOT, label + " existing ancestor")
        ancestor = ancestor.parent
    ancestor = ancestor.resolve(strict=True)
    value = ancestor.lstat()
    need(
        within(ancestor, ROOT)
        and stat.S_ISDIR(value.st_mode)
        and not ancestor.is_symlink(),
        label + " real workspace ancestor",
    )
    return resolved


def audit_output_preflight(
    candidate: Path,
    receipt: Path,
    output: Path,
    before_result: dict[str, Any],
    pid: int,
) -> tuple[Path, Path, Path, Path]:
    output = canonical_future_target(output, "C41 audit output")
    stage = output.with_name(output.name + ".stage-" + str(pid))
    need(not output.exists() and not stage.exists(), "audit output/stage must not preexist")
    authority = before_result.get("C40_authority")
    need(
        type(authority) is dict
        and authority.get("object_sha256") == EXPECTED_C40_OBJECT
        and authority.get("independent_audit_object_sha256")
        == EXPECTED_C40_AUDIT_OBJECT
        and authority.get("independent_audit_status") == EXPECTED_C40_AUDIT_STATUS,
        "prewrite C40 authority envelope",
    )
    c40_candidate = canonical_authority_path(authority.get("path"), "C40 candidate")
    c40_audit = canonical_authority_path(
        authority.get("independent_audit_path"), "C40 audit"
    )
    candidate_stat = c40_candidate.lstat()
    audit_stat = c40_audit.lstat()
    need(
        stat.S_ISDIR(candidate_stat.st_mode)
        and not c40_candidate.is_symlink()
        and stat.S_ISREG(audit_stat.st_mode)
        and not c40_audit.is_symlink()
        and audit_stat.st_nlink == 1,
        "prewrite C40 authority file types",
    )
    require_disjoint_targets(
        (("output", output), ("stage", stage)),
        (
            ("C41 candidate", candidate),
            ("C41 receipt", receipt),
            ("C40 candidate", c40_candidate),
            ("C40 audit parent", c40_audit.parent),
        ),
    )
    return output, stage, c40_candidate, c40_audit


def load_c40_authority(
    result: dict[str, Any],
) -> tuple[
    Path,
    dict[str, Any],
    dict[str, list[dict[str, Any]]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
    list[dict[str, Any]],
]:
    authority = result.get("C40_authority")
    need(type(authority) is dict, "C40 authority envelope")
    candidate = canonical_authority_path(authority.get("path"), "C40 candidate")
    audit_path = canonical_authority_path(
        authority.get("independent_audit_path"), "C40 audit"
    )
    c40_result, c40_rows, _manifest, _directory, _files = (
        c40a.capture_c40_candidate(candidate)
    )
    need(
        c40_result.get("object_sha256") == EXPECTED_C40_OBJECT
        and authority.get("object_sha256") == EXPECTED_C40_OBJECT,
        "C40 candidate authority object",
    )
    audit_raw, _audit_identity = stable_read(audit_path, 32 << 20, "C40 audit")
    audit = strict_json_bytes(audit_raw, "C40 audit")
    closed_object(audit, "C40 audit")
    need(
        audit.get("schema") == C40_AUDIT_SCHEMA
        and audit.get("object_sha256") == EXPECTED_C40_AUDIT_OBJECT
        and audit.get("status") == EXPECTED_C40_AUDIT_STATUS
        and audit.get("candidate_object_sha256") == EXPECTED_C40_OBJECT
        and authority.get("independent_audit_object_sha256")
        == EXPECTED_C40_AUDIT_OBJECT
        and authority.get("independent_audit_status") == EXPECTED_C40_AUDIT_STATUS
        and len(audit.get("attacks", {})) >= 18
        and all(audit.get("attacks", {}).values()),
        "C40 independent audit authority",
    )
    c39_authority = c40_result.get("C39_authority")
    need(type(c39_authority) is dict, "C40 to C39 authority")
    c39_path = canonical_authority_path(c39_authority.get("path"), "C39 candidate")
    c39_audit = canonical_authority_path(
        c39_authority.get("independent_audit_path"), "C39 audit"
    )
    c39_result, _c39_audit, _c39_rows, c39_parents = c40a.load_c39_authority(
        c39_path, c39_audit
    )
    c38_index, cells, config = c40a.load_geometry_authority(c39_result)
    config["cores"] = tuple(round139.lower.core_cert.physical_cores())
    return candidate, c40_result, c40_rows, c38_index, cells, config, c39_parents


class Cursor:
    def __init__(self, rows: list[dict[str, Any]], label: str):
        self.rows = rows
        self.label = label
        self.index = 0

    def consume(self, expected: dict[str, Any]) -> None:
        need(self.index < len(self.rows), "missing row:" + self.label)
        observed = self.rows[self.index]
        need(observed == row_closed(expected), f"exact row:{self.label}:{self.index}")
        self.index += 1

    def finish(self) -> None:
        need(self.index == len(self.rows), "surplus rows:" + self.label)


def disposition_family(classification: str) -> str:
    if classification.startswith("EXCLUDED_"):
        return "TERMINAL_EXCLUDED"
    if "NEEDS_COLLISION3_1648" in classification:
        return "COLLISION3_READY"
    return "RESIDUAL_OUTER"


def residual_classification(classification: str) -> str:
    if "ALGEBRAIC_ENDPOINT" in classification:
        return "UNRESOLVED_C41_ALGEBRAIC_H0_SEAM_RECHART_OUTER"
    if any(token in classification for token in (
        "SOURCE_RADICAL", "SOURCE_GRAZING_ENDPOINT", "P_ENDPOINT_BOX",
    )):
        return "UNRESOLVED_C41_SOURCE_RADICAL_STEREOGRAPHIC_ENDPOINT_OUTER"
    if "COLLISION1_WORD" in classification:
        return "UNRESOLVED_C41_COLLISION1_WORD_COLLAR_OUTER"
    if "COLLISION2_WORD" in classification:
        return "UNRESOLVED_C41_COLLISION2_WORD_COLLAR_OUTER"
    if "H1_GRAPH" in classification or "H1_BOUNDARY" in classification:
        return "UNRESOLVED_C41_H1_GRAPH_OR_BOUNDARY_OUTER"
    if "COLLISION1_OUTGOING_STATE" in classification:
        return "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER"
    if any(token in classification for token in (
        "REGULAR_MULTI_GRAPH", "SINGULAR_OR_ORDER", "COLLISION1_OWNER_GEOMETRY",
        "C1_ROUTE_EVALUATION", "COLLISION1_DELTA", "COLLISION1_ROOT",
    )):
        return "UNRESOLVED_C41_C1_REGULAR_MULTI_GRAPH_OUTER"
    for count in (1, 2, 3):
        if f"ACTIVE_DELTA_{count}" in classification:
            return f"UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_{count}_OUTER"
    if "POINT_WINNER_NONSTRICT" in classification or "POINT_OWNER_NOT_UNIQUE" in classification:
        return "UNRESOLVED_C41_COLLISION2_POINT_WINNER_NONSTRICT_OUTER"
    if "OUTGOING_H2" in classification or "COLLISION2_OUTGOING_STATE" in classification:
        return "UNRESOLVED_C41_COLLISION2_H2_FACTOR_OUTER"
    if "WALL_ENDPOINT" in classification or "WALL_OR_CORNER" in classification:
        return "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER"
    if "EVALUATION_EXCEPTION" in classification or "FAILURE_OUTER" in classification:
        return "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER"
    raise Reject("unmapped residual classification:" + classification)


def endpoint_phase(box: Any) -> str | None:
    return (
        "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT"
        if box.p0 == -1 or box.p1 == 1 else None
    )


def box_payload(box: Any | None) -> dict[str, Any] | None:
    if box is None:
        return None
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def reflected_payload(chart: str, box: Any) -> dict[str, Any]:
    if chart in {"E", "W"}:
        reflected_chart = chart
        t_interval = (-box.t1, -box.t0)
    else:
        reflected_chart = {"N": "S", "S": "N"}[chart]
        t_interval = (box.t0, box.t1)
    return {
        "compact_chart": reflected_chart,
        "t": [qstr(item) for item in t_interval],
        "p": [qstr(-box.p1), qstr(-box.p0)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def reflected_box(parent_key: str, box: Any | None) -> dict[str, Any] | None:
    if box is None:
        return None
    return reflected_payload(parent_key.split(":")[1], box)


def source_radical_failure_replay(
    parent_key: str, box: Any, caught: Exception,
) -> dict[str, Any]:
    semantic: dict[str, Any] = {
        "attempted": endpoint_phase(box) is not None,
        "matched_caught_exception": False,
        "replay_is_source_sqrt_domain_failure": False,
        "source_radical_causal_match": False,
        "replay_exception_type": None,
        "replay_exception_module": None,
        "replay_exception_message": None,
    }
    if not semantic["attempted"]:
        return semantic
    try:
        round185.ad_initial_geometry(parent_key, box)
    except Exception as replay:
        matched = (
            type(replay).__module__ == type(caught).__module__
            and type(replay).__name__ == type(caught).__name__
            and str(replay) == str(caught)
        )
        source_sqrt = (
            type(replay).__name__ == "Round185Error"
            and str(replay) == "AD sqrt domain"
        )
        semantic.update({
            "matched_caught_exception": matched,
            "replay_is_source_sqrt_domain_failure": source_sqrt,
            "source_radical_causal_match": matched and source_sqrt,
            "replay_exception_type": type(replay).__name__,
            "replay_exception_module": type(replay).__module__,
            "replay_exception_message": str(replay),
        })
    return semantic


def expected_collision2(
    detail: dict[str, Any], config: dict[str, Any],
) -> tuple[str, str]:
    selected = detail["absolute_collision2_owner"]
    expected_by_owner = {
        config["original_path"][1]["selected_absolute_owner_id"]:
            config["original_path"][1],
        config["reflected_path"][1]["selected_absolute_owner_id"]:
            config["reflected_path"][1],
    }
    expected = expected_by_owner.get(selected)
    if expected is None:
        return "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", selected
    outgoing = detail.get("collision2_outgoing_chart")
    if outgoing != expected["outgoing_chart"]:
        return "EXCLUDED_C40_COLLISION2_CHART_MISMATCH", str(outgoing)
    word_id = detail["official_gate5_key"]["word_key_id"]
    if word_id != expected["official_word_key_id"]:
        return "EXCLUDED_C40_COLLISION2_WORD_MISMATCH", word_id
    branch = (
        "ORIGINAL"
        if selected == config["original_path"][1]["selected_absolute_owner_id"]
        else "REFLECTED"
    )
    return (
        f"UNRESOLVED_C40_LIVE_COLLISION2_{branch}_MATCH_NEEDS_COLLISION3_1648",
        selected,
    )


def collision2_safe(result: dict[str, Any], classification: str) -> bool:
    if classification.startswith("EXCLUDED_") or "COLLISION2" not in classification:
        return False
    evidence = result.get("surface_evidence") or {}
    h1 = evidence.get("H1")
    return bool(
        evidence.get("remaining_unresolved_record_count") == 0
        and h1
        and h1.get("kind") == "STRICT_SIDE"
        and h1.get("chart") == "W"
    )


def independent_route_at_path(
    task: dict[str, Any], path: str, config: dict[str, Any],
) -> dict[str, Any]:
    source = task["source"]
    c38_source = task["c38_source"]
    cell = task["cell"]
    pseudo = copy.deepcopy(c38_source)
    pseudo["path"] = path
    route_task = {
        "task_id": source["c40_leaf_id"] + ":" + path,
        "kind": "C1",
        "row": pseudo,
        "cell": cell,
    }
    box, _active = c39.reconstruct_box(cell, path)
    try:
        result = c39.route_c1_task(route_task, config)
    except Exception as error:
        replay = source_radical_failure_replay(
            c38_source["representative_origin_key"], box, error
        )
        exact_endpoint = endpoint_phase(box)
        if replay["source_radical_causal_match"]:
            classification = (
                "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
                "EVALUATION_FAILURE_OUTER"
            )
        elif exact_endpoint is not None:
            classification = (
                "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_FAILURE_OUTER"
            )
        else:
            classification = "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
        return {
            "box": box,
            "classification": classification,
            "witness": type(error).__name__ + ":" + str(error),
            "route_method": "C41_C1_ROUTE_EXCEPTION_FAIL_CLOSED",
            "c1_result": None,
            "c2_status": None,
            "c2_baseline": None,
            "c2_detail": None,
            "c2_evidence": [],
            "route_failure": {
                "phase": "C39_ROUTE_C1_TASK",
                "exception_type": type(error).__name__,
                "exception_module": type(error).__module__,
                "exception_message": str(error),
                "exact_box_endpoint_phase": exact_endpoint,
                "source_radical_initial_geometry_replay": replay,
            },
        }
    classification = result["classification"]
    witness = result["witness"]
    route_method = result["route_method"]
    c2_status: str | None = None
    c2_baseline: str | None = None
    c2_detail: dict[str, Any] | None = None
    c2_evidence: list[dict[str, Any]] = []
    if collision2_safe(result, classification):
        try:
            c2_status, c2_detail, c2_evidence, c2_baseline = (
                round185.resolve_dynamic_box(
                    c38_source["representative_origin_key"],
                    box,
                    config["pair_index"],
                    config["pattern_index"],
                )
            )
            if c2_status.startswith("LOCAL_EXACT_KEY"):
                classification, witness = expected_collision2(c2_detail, config)
            else:
                classification = "UNRESOLVED_C40_COLLISION2_" + c2_status
                witness = c2_baseline
            route_method = "C41_ROUND185_DEPTH3_STRICT_ROUTER"
        except Exception as error:
            classification = "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION"
            witness = type(error).__name__ + ":" + str(error)
            route_method = "C41_ROUND185_FAIL_CLOSED"
            c2_status = "EVALUATION_EXCEPTION"
            c2_baseline = "ROUND185_FAIL_CLOSED"
            c2_detail = {
                "error_type": type(error).__name__,
                "error_module": type(error).__module__,
                "error_message": str(error),
            }
            c2_evidence = []
    return {
        "box": box,
        "classification": classification,
        "witness": witness,
        "route_method": route_method,
        "c1_result": result,
        "c2_status": c2_status,
        "c2_baseline": c2_baseline,
        "c2_detail": c2_detail,
        "c2_evidence": c2_evidence,
        "route_failure": None,
    }


def compact_c2_surface(evidence: dict[str, Any]) -> dict[str, Any]:
    derivatives = evidence.get("full_box_C1_derivatives", {})
    return {
        "kind": evidence.get("kind"),
        "identifier": evidence.get("identifier"),
        "equation": evidence.get("equation"),
        "centered_C0_sign": evidence.get("centered_C0_sign"),
        "centered_mean_value_C0_enclosure": evidence.get(
            "centered_mean_value_C0_enclosure"
        ),
        "full_box_C1_derivatives": derivatives,
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp")
            if axis in derivatives and not derivatives[axis]["contains_zero"]
        ],
        "axis_full_face_brackets_t_p_s": evidence.get(
            "axis_full_face_brackets_t_p_s", []
        ),
        "axis_interval_Newton": evidence.get("axis_interval_Newton", []),
        "strict_corner_segment_bracket": evidence.get(
            "strict_corner_segment_bracket"
        ),
        "independently_certified_nonempty": evidence.get(
            "independently_certified_nonempty", False
        ),
        "evidence_sha256": digest(evidence),
    }


def compact_root_surface(value: dict[str, Any]) -> dict[str, Any]:
    derivatives = value.get("tp_derivatives", {})
    return {
        "kind": "COLLISION1_DELTA_OR_NEAR_ROOT",
        "identifier": value.get("target_id"),
        "equation": (
            f"collision1_Delta_{value.get('target_id')}=0"
            if value.get("output_classification") == "unresolved_discriminant"
            else f"collision1_near_{value.get('target_id')}=0"
        ),
        "input_classification": value.get("input_classification"),
        "output_classification": value.get("output_classification"),
        "derivatives": derivatives,
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp")
            if derivatives.get(axis, {}).get("sign") != "UNRESOLVED"
        ],
        "certified_nonempty_regular_graph": False,
        "carrier_existence_status": "UNRESOLVED_POTENTIAL_SURFACE_OUTER",
    }


def compact_h1_surface(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "H1",
        "identifier": FROZEN_OWNER,
        "equation": "H1=n1_x^2-n1_y^2=0",
        "H1_centered": value.get("H1_centered"),
        "H1_natural": value.get("H1_natural"),
        "graph_axis": value.get("graph_axis"),
        "face_evidence": value.get("face_evidence", []),
        "strict_derivative_axes": [value["graph_axis"]]
        if value.get("graph_axis") in {"t", "p"} else [],
        "certified_nonempty_regular_graph": (
            value.get("kind") == "REGULAR_FULL_FACE_GRAPH"
        ),
        "carrier_existence_status": (
            "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
            if value.get("kind") == "REGULAR_FULL_FACE_GRAPH"
            else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
        ),
    }


def surface_summaries(route: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result = route.get("c1_result")
    if result is not None:
        evidence = result.get("surface_evidence") or {}
        for value in evidence.get("root_surfaces", []):
            if value.get("output_classification") in {
                "unresolved_discriminant", "unresolved_root_sign",
            }:
                rows.append(compact_root_surface(value))
        h1 = evidence.get("H1")
        if h1 is not None and h1.get("kind") not in {None, "STRICT_SIDE"}:
            rows.append(compact_h1_surface(h1))
    for value in route.get("c2_evidence", []):
        compact = compact_c2_surface(value)
        certified = bool(
            compact["independently_certified_nonempty"]
            and compact["strict_derivative_axes"]
        )
        rows.append({
            "kind": compact["kind"],
            "identifier": compact["identifier"],
            "equation": compact["equation"],
            "centered_C0_sign": compact["centered_C0_sign"],
            "strict_derivative_axes": compact["strict_derivative_axes"],
            "axis_full_face_brackets_t_p_s": compact[
                "axis_full_face_brackets_t_p_s"
            ],
            "axis_interval_Newton": compact["axis_interval_Newton"],
            "certified_nonempty_regular_graph": certified,
            "carrier_existence_status": (
                "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                if certified else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
            ),
            "evidence_sha256": compact["evidence_sha256"],
        })
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        key = (row.get("kind"), row.get("identifier"), row.get("equation"))
        unique.setdefault(key, row)
    return list(unique.values())


def endpoint_rechart_payload(
    task: dict[str, Any], route: dict[str, Any], residual: str,
) -> dict[str, Any]:
    cell = task["cell"]
    c38_source = task["c38_source"]
    box = route["box"]
    if "ALGEBRAIC_H0" in residual:
        need(box is None, "algebraic endpoint has no rational box")
        algebraic = [
            (index, value)
            for index, value in enumerate(cell["physical_t_interval"])
            if value["kind"] == "ALGEBRAIC"
        ]
        need(len(algebraic) == 1, "single algebraic H0 endpoint")
        endpoint_index, endpoint = algebraic[0]
        need(
            endpoint["minimal_polynomial"] == "2*x^2-1"
            and len(endpoint["isolating_interval"]) == 2,
            "algebraic H0 polynomial/isolator",
        )
        seams = task["seams"]
        spans = [
            tuple(Q(item["value"]) for item in seam["physical_p_span"])
            for seam in seams
        ]
        need(
            bool(spans)
            and spans[0][0] == Q(cell["physical_p_interval"][0])
            and spans[-1][1] == Q(cell["physical_p_interval"][1])
            and all(left[1] == right[0] for left, right in zip(spans, spans[1:])),
            "algebraic seam p-span exhaustion",
        )
        incidences: list[dict[str, Any]] = []
        for ordinal, seam in enumerate(seams):
            need(
                cell["cell_id"] in {seam["left_cell_id"], seam["right_cell_id"]},
                "algebraic seam cell incidence",
            )
            owner_cell = seam["left_cell_id"]
            incidences.append({
                "seam_segment_ordinal": ordinal,
                "seam_id": seam["seam_id"],
                "face_id": seam["face_id"],
                "C32_seam_row_sha256": seam["row_sha256"],
                "left_cell_id": seam["left_cell_id"],
                "left_chart": seam["left_chart"],
                "left_compact_endpoint": seam["left_compact_endpoint"],
                "right_cell_id": seam["right_cell_id"],
                "right_chart": seam["right_chart"],
                "right_compact_endpoint": seam["right_compact_endpoint"],
                "exact_physical_p_span": seam["physical_p_span"],
                "exact_state_gluing_inherited_from_round162": seam[
                    "exact_state_gluing_inherited_from_round162"
                ],
                "half_open_adjacent_chart_policy": (
                    "C41_LEFT_CELL_OWNS_SEAM__RIGHT_CELL_EXCLUDES_DUPLICATE"
                ),
                "half_open_owner_cell_id": owner_cell,
                "representative_cell_half_open_role": (
                    "OWNS_SEAM"
                    if cell["cell_id"] == owner_cell
                    else "EXCLUDES_DUPLICATE_SEAM"
                ),
                "seam_ambient_credit": 0,
                "D02_gate_credit": 0,
            })
        return {
            "endpoint_kind": "ALGEBRAIC_H0_SOURCE_CHART_SEAM",
            "H0_equation": "H0=2*t^2-1=0",
            "minimal_polynomial": endpoint["minimal_polynomial"],
            "isolating_interval": endpoint["isolating_interval"],
            "algebraic_value": endpoint["value"],
            "exact_sign": (
                "NEGATIVE" if endpoint["value"].startswith("-") else "POSITIVE"
            ),
            "physical_interval_side": (
                "INTERIOR_ABOVE_ALGEBRAIC_ENDPOINT"
                if endpoint_index == 0
                else "INTERIOR_BELOW_ALGEBRAIC_ENDPOINT"
            ),
            "representative_cell_id": cell["cell_id"],
            "representative_chart": cell["compact_chart"],
            "horizontal_reflection_partner_cell_id": c38_source["reflected_cell_id"],
            "horizontal_reflection_partner_origin_key": c38_source[
                "reflected_origin_key"
            ],
            "horizontal_reflection_materialized_in_rational_box": False,
            "adjacent_chart_seam_incidence_count": len(incidences),
            "adjacent_chart_seam_incidences": incidences,
            "adjacent_chart_seam_p_span_exhaustive": True,
            "rechart_route_status": (
                "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING"
            ),
            "certified_carrier_dimension": 1,
            "carrier_existence_status": "CERTIFIED_EXACT_ENDPOINT_CARRIER",
        }
    need(box is not None and endpoint_phase(box) is not None, "rational p endpoint")
    if box.p0 == -1:
        sigma = -1
        interior_p = box.p1
        endpoint_side = "P_LOWER"
    else:
        need(box.p1 == 1, "rational endpoint p=+/-1")
        sigma = 1
        interior_p = box.p0
        endpoint_side = "P_UPPER"
    radial_ratio = Q(sigma) * interior_p
    need(-1 < radial_ratio <= 1, "stereographic endpoint interior ratio")
    u_squared_max = (1 - radial_ratio) / (1 + radial_ratio)
    need(u_squared_max >= 0, "stereographic u squared interval")
    return {
        "endpoint_kind": "RATIONAL_P_ENDPOINT_STEREOGRAPHIC_RECHART",
        "sigma": sigma,
        "exact_p_endpoint": str(sigma),
        "endpoint_side": endpoint_side,
        "source_radical_equation": "q_source^2=1-p^2",
        "stereographic_coordinate_domain": "u>=0",
        "stereographic_p_formula": "p=sigma*(1-u^2)/(1+u^2)",
        "stereographic_q_formula": "q_source=2*u/(1+u^2)",
        "unit_circle_identity": (
            "(sigma*(1-u^2)/(1+u^2))^2+(2*u/(1+u^2))^2=1"
        ),
        "unit_circle_identity_exact_polynomial": (
            "(1-u^2)^2+4*u^2=(1+u^2)^2"
        ),
        "closed_t_interval": [qstr(box.t0), qstr(box.t1)],
        "closed_p_interval": [qstr(box.p0), qstr(box.p1)],
        "closed_u_squared_interval": ["0", qstr(u_squared_max)],
        "u_zero_endpoint_owner": "ENDPOINT_RECHART_OWNS_U_EQUALS_ZERO",
        "positive_u_ambient_owner": "AMBIENT_CELL_OWNS_U_GREATER_THAN_ZERO",
        "half_open_endpoint_dedup_complete": True,
        "route_failure": route["route_failure"],
        "rechart_route_status": (
            "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING"
        ),
        "transformed_route_evaluator_status": "PENDING",
        "certified_carrier_dimension": 1,
        "carrier_existence_status": "CERTIFIED_EXACT_ENDPOINT_CARRIER",
    }


def exact_face_box(box: Any, face: str) -> dict[str, list[str]]:
    payload = box_payload(box)
    need(payload is not None, "exact rational face")
    axis = face[0]
    endpoint = 0 if face.endswith("lower") else 1
    payload[axis] = [payload[axis][endpoint], payload[axis][endpoint]]
    return payload


def exact_corner_box(box: Any, corner: str) -> dict[str, list[str]]:
    payload = box_payload(box)
    need(payload is not None, "exact rational corner")
    t_endpoint = int(corner[1])
    p_endpoint = int(corner[3])
    payload["t"] = [payload["t"][t_endpoint], payload["t"][t_endpoint]]
    payload["p"] = [payload["p"][p_endpoint], payload["p"][p_endpoint]]
    return payload


def independent_outer_groups(
    task: dict[str, Any],
    ambient_identity: dict[str, Any],
    residual: str,
    route: dict[str, Any],
    split_link: dict[str, Any] | None,
) -> dict[str, list[dict[str, Any]]]:
    surfaces = surface_summaries(route)
    normalized: list[dict[str, Any]] = []
    for ordinal, surface in enumerate(surfaces):
        candidate_id = "c41-normalized-surface:" + digest({
            "ambient": ambient_identity,
            "ordinal": ordinal,
            "kind": surface.get("kind"),
            "identifier": surface.get("identifier"),
            "equation": surface.get("equation"),
        })
        normalized.append({
            "schema": NORMALIZED_SURFACE_REGISTRY_SCHEMA + ".entry",
            "normalized_surface_id": candidate_id,
            "surface_ordinal": ordinal,
            **surface,
            "candidate_carrier_expected_dimension": 1,
            "certified_carrier_dimension": (
                1 if surface.get("certified_nonempty_regular_graph") else None
            ),
            "ambient_or_whole_parent_credit": 0,
            "D02_gate_credit": 0,
        })
    common = {
        "pair_index": ambient_identity["pair_index"],
        "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
        "descendant_path": ambient_identity["path"],
        "residual_classification": residual,
        "raw_classification": route["classification"],
        "raw_witness": route["witness"],
        "route_failure": route["route_failure"],
        "normalized_surface_count": len(normalized),
        "normalized_surfaces": normalized,
        "normalized_surface_registry_schema": NORMALIZED_SURFACE_REGISTRY_SCHEMA,
        "normalized_surface_registry_storage": (
            "NESTED_ONE_ENTRY_PER_SURFACE_INSIDE_OWNING_PRIMARY_OUTER_ROW"
        ),
        "normalized_surface_registry_foreign_key": (
            "normalized_surface_id__SCOPED_TO_OWNING_PRIMARY_OUTER_ID"
        ),
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    groups: dict[str, list[dict[str, Any]]] = {
        "c1": [], "endpoint": [], "c2": [], "incidence": [], "boundary": [],
    }
    if "SOURCE_RADICAL" in residual or "ALGEBRAIC_H0" in residual:
        schema, id_field, prefix, group = (
            ENDPOINT_SCHEMA, "endpoint_rechart_id", "c41-endpoint-rechart:", "endpoint"
        )
    elif "COLLISION2" in residual:
        schema, id_field, prefix, group = (
            C2_OUTER_SCHEMA, "c2_surface_outer_id", "c41-c2-outer:", "c2"
        )
    else:
        schema, id_field, prefix, group = (
            C1_OUTER_SCHEMA, "c1_h1_surface_outer_id", "c41-c1-h1-outer:", "c1"
        )
    endpoint_payload = (
        endpoint_rechart_payload(task, route, residual)
        if group == "endpoint" else None
    )
    primary = {
        "schema": schema,
        **common,
        "carrier_existence_status": (
            endpoint_payload["carrier_existence_status"]
            if endpoint_payload is not None
            else "UNRESOLVED_STRATIFIED_SURFACE_OUTER"
        ),
        "certified_carrier_dimension": (
            endpoint_payload["certified_carrier_dimension"]
            if endpoint_payload is not None else None
        ),
        "candidate_intersection_rank_status": None,
        "endpoint_rechart_geometry": endpoint_payload,
    }
    primary[id_field] = prefix + digest(primary)
    groups[group].append(primary)
    primary_id = primary[id_field]
    orthogonal_endpoint_ids: list[str] = []
    if (
        group != "endpoint"
        and route["box"] is not None
        and endpoint_phase(route["box"]) is not None
    ):
        geometry = endpoint_rechart_payload(task, route, residual)
        endpoint_outer = {
            "schema": ENDPOINT_SCHEMA,
            **common,
            "normalized_surface_count": 0,
            "normalized_surfaces": [],
            "carrier_existence_status": geometry["carrier_existence_status"],
            "certified_carrier_dimension": geometry["certified_carrier_dimension"],
            "candidate_intersection_rank_status": None,
            "endpoint_rechart_geometry": geometry,
            "orthogonal_to_primary_residual": True,
            "owning_primary_outer_id": primary_id,
        }
        endpoint_outer["endpoint_rechart_id"] = (
            "c41-endpoint-rechart:" + digest(endpoint_outer)
        )
        groups["endpoint"].append(endpoint_outer)
        orthogonal_endpoint_ids.append(endpoint_outer["endpoint_rechart_id"])
    for left, right in itertools.combinations(normalized, 2):
        incidence = {
            "schema": INCIDENCE_SCHEMA,
            "pair_index": ambient_identity["pair_index"],
            "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
            "descendant_path": ambient_identity["path"],
            "owning_outer_id": primary_id,
            "left_normalized_surface_id": left["normalized_surface_id"],
            "right_normalized_surface_id": right["normalized_surface_id"],
            "classification": "UNRESOLVED_C41_PAIR_INCIDENCE_KRAWCZYK_PENDING",
            "candidate_incidence_expected_dimension": 0,
            "certified_intersection_dimension": None,
            "intersection_existence": None,
            "rank_status": None,
            "ambient_or_whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }
        incidence["incidence_outer_id"] = "c41-incidence:" + digest(incidence)
        groups["incidence"].append(incidence)
    box = route["box"]
    face_rows: list[dict[str, Any]] = []
    corner_rows: list[dict[str, Any]] = []
    if box is not None:
        for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
            is_last = bool(split_link is not None and split_link["shared_face"] == face)
            face_semantic = {
                "face": face,
                "exact_closed_face_box": exact_face_box(box, face),
                "face_dimension_in_s0_slice": 1,
                "last_split_face": is_last,
                "split_face_adjacency_id": (
                    split_link["split_face_adjacency_id"] if is_last else None
                ),
                "sibling_path": split_link["sibling_path"] if is_last else None,
                "half_open_face_role": (
                    split_link["half_open_role"]
                    if is_last else "GLOBAL_FACE_OWNER_PENDING_INCIDENCE_CENSUS"
                ),
                "global_face_owner_rule": (
                    "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS"
                ),
                "global_face_owner_resolved": False,
                "surface_face_incidence_links": [],
                "face_ambient_credit": 0,
                "D02_gate_credit": 0,
            }
            face_semantic["boundary_face_id"] = "c41-boundary-face:" + digest({
                "ambient": ambient_identity, **face_semantic,
            })
            for surface in normalized:
                link = {
                    "boundary_face_id": face_semantic["boundary_face_id"],
                    "normalized_surface_id": surface["normalized_surface_id"],
                    "candidate_intersection_expected_dimension": 0,
                    "certified_intersection_dimension": None,
                    "intersection_existence": None,
                    "rank_status": None,
                    "classification": "SURFACE_FACE_INCIDENCE_OUTER_PENDING",
                    "ambient_or_whole_parent_credit": 0,
                    "D02_gate_credit": 0,
                }
                link["surface_face_incidence_id"] = (
                    "c41-surface-face-incidence:" + digest(link)
                )
                face_semantic["surface_face_incidence_links"].append(link)
            face_rows.append(face_semantic)
        for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
            corner_semantic = {
                "corner": corner,
                "exact_closed_corner_box": exact_corner_box(box, corner),
                "corner_dimension_in_s0_slice": 0,
                "global_corner_owner_rule": (
                    "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS"
                ),
                "global_corner_owner_resolved": False,
                "half_open_corner_role": "GLOBAL_CORNER_OWNER_PENDING_INCIDENCE_CENSUS",
                "surface_corner_incidence_status": "SURFACE_CORNER_CENSUS_PENDING",
                "corner_ambient_credit": 0,
                "D02_gate_credit": 0,
            }
            corner_semantic["boundary_corner_id"] = (
                "c41-boundary-corner-point:" + digest({
                    "ambient": ambient_identity, **corner_semantic,
                })
            )
            corner_rows.append(corner_semantic)
    boundary = {
        "schema": BOUNDARY_SCHEMA,
        "pair_index": ambient_identity["pair_index"],
        "c40_source_leaf_id": ambient_identity["c40_source_leaf_id"],
        "descendant_path": ambient_identity["path"],
        "owning_outer_id": primary_id,
        "face_family": ["t_lower", "t_upper", "p_lower", "p_upper"],
        "corner_family": ["t0p0", "t0p1", "t1p0", "t1p1"],
        "exact_face_row_count": len(face_rows),
        "exact_corner_row_count": len(corner_rows),
        "face_rows": face_rows,
        "corner_rows": corner_rows,
        "face_intersection_status": "FACE_RESTRICTION_PENDING",
        "corner_intersection_status": "CORNER_CENSUS_PENDING",
        "exact_rational_face_and_corner_geometry_complete": box is not None,
        "global_sibling_adjacency_and_half_open_owner_complete": False,
        "boundary_and_corner_inventory_complete": False,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    boundary["boundary_corner_outer_id"] = "c41-boundary-corner:" + digest(boundary)
    groups["boundary"].append(boundary)
    groups["obligation_ids"] = [[
        primary_id,
        *orthogonal_endpoint_ids,
        *[row["incidence_outer_id"] for row in groups["incidence"]],
        boundary["boundary_corner_outer_id"],
    ]]
    return groups


def independent_split(
    task: dict[str, Any],
    box: Any,
    descendant_bits: str,
    additional_depth: int,
    axis_history: list[str],
) -> tuple[dict[str, Any], tuple[Any, Any], int]:
    axis = round166.longest_axis(box)
    children = round166.split_axis(box, axis)
    axis_name = ("t", "p", "s")[axis]
    lower, upper = (
        (box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)
    )[axis]
    middle = (lower + upper) / 2
    source = task["source"]
    semantic = {
        "schema": SPLIT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "parent_descendant_bits": descendant_bits,
        "parent_path": source["path"] + descendant_bits,
        "additional_depth_before_split": additional_depth,
        "split_axis": axis_name,
        "exact_split_coordinate": qstr(middle),
        "parent_closed_box": box_payload(box),
        "lower_child_path": source["path"] + descendant_bits + "0",
        "upper_child_path": source["path"] + descendant_bits + "1",
        "lower_child_closed_box": box_payload(children[0]),
        "upper_child_closed_box": box_payload(children[1]),
        "axis_history_before_split": axis_history,
        "half_open_shared_face_owner": "LOWER_BIT_CHILD",
        "lower_child_fraction_multiplier": "1/2",
        "upper_child_fraction_multiplier": "1/2",
        "exact_split_conservation": "1",
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["split_face_adjacency_id"] = "c41-split:" + digest(semantic)
    return semantic, children, axis


def independent_ambient(
    task: dict[str, Any],
    route: dict[str, Any],
    descendant_bits: str,
    additional_depth: int,
    fraction: Q,
    axis_history: list[str],
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    source = task["source"]
    box = route["box"]
    classification = route["classification"]
    family = disposition_family(classification)
    identity = {
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "path": source["path"] + descendant_bits,
        "parent_volume_fraction": qstr(fraction),
    }
    residual = (
        residual_classification(classification)
        if family == "RESIDUAL_OUTER" else None
    )
    groups: dict[str, list[dict[str, Any]]] = {
        "c1": [], "endpoint": [], "c2": [], "incidence": [], "boundary": [],
        "obligation_ids": [[]],
    }
    if residual is not None:
        split_link: dict[str, Any] | None = None
        if descendant_bits:
            parent_bits = descendant_bits[:-1]
            parent_path = source["path"] + parent_bits
            parent_box, _active = c39.reconstruct_box(task["cell"], parent_path)
            adjacency, _children, axis = independent_split(
                task,
                parent_box,
                parent_bits,
                additional_depth - 1,
                axis_history[:-1],
            )
            bit = descendant_bits[-1]
            axis_name = ("t", "p", "s")[axis]
            need(axis_name in {"t", "p"}, "s=0 split axis")
            split_link = {
                "split_face_adjacency_id": adjacency["split_face_adjacency_id"],
                "sibling_path": source["path"] + parent_bits + (
                    "1" if bit == "0" else "0"
                ),
                "shared_face": axis_name + ("_upper" if bit == "0" else "_lower"),
                "half_open_role": (
                    "OWNS_SHARED_SPLIT_FACE"
                    if bit == "0" else "EXCLUDES_DUPLICATE_SHARED_SPLIT_FACE"
                ),
            }
        groups = independent_outer_groups(task, identity, residual, route, split_link)
    semantic = {
        "schema": AMBIENT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c40_source_classification": source["classification"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "descendant_bits": descendant_bits,
        "path": identity["path"],
        "additional_depth": additional_depth,
        "split_axis_history": axis_history,
        "parent_volume_fraction": qstr(fraction),
        "closed_representative_box": box_payload(box),
        "closed_reflected_box": reflected_box(
            task["c38_source"]["representative_origin_key"], box
        ),
        "half_open_owner_policy": (
            "LOWER_BIT_OWNS_SHARED_SPLIT_FACE__UPPER_BIT_EXCLUDES"
        ),
        "raw_classification": classification,
        "raw_witness": route["witness"],
        "route_method": route["route_method"],
        "disposition_family": family,
        "residual_classification": residual,
        "route_failure": route["route_failure"],
        "c2_status": route["c2_status"],
        "c2_baseline": route["c2_baseline"],
        "obligation_ids": groups["obligation_ids"][0],
        "round144_terminal_class": (
            "EARLIEST_PREFIX_EXCLUDED"
            if family == "TERMINAL_EXCLUDED"
            else "UNRESOLVED_R1648_CONTINUATION"
        ),
        "local_round144_terminal_credit": (
            1 if family == "TERMINAL_EXCLUDED" else 0
        ),
        "lower_dimensional_ambient_credit": 0,
        "collision3_ready_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["c41_ambient_cell_id"] = "c41-ambient:" + digest(semantic)
    return semantic, groups


def independent_cache_replay(
    source: dict[str, Any], route: dict[str, Any],
) -> dict[str, Any]:
    need(
        route["route_failure"] is None
        and route["c1_result"] is not None
        and route["classification"] in EXPECTED_CACHE_REPLAY_CENSUS,
        "19-row cache replay route",
    )
    semantic = {
        "schema": CACHE_REPLAY_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "old_exception_type": source["route_exception_type"],
        "old_exception_message": source["route_exception_message"],
        "required_chart": "W:W",
        "official_candidate_count": 55,
        "official_candidate_ids_sha256": EXPECTED_CHART_CANDIDATES["W:W"][1],
        "repaired_C39_c1_classification": route["c1_result"]["classification"],
        "repaired_C39_c1_witness": route["c1_result"]["witness"],
        "replay_classification": route["classification"],
        "replay_witness": route["witness"],
        "replay_exception": None,
        "disposition_family": "COLLISION3_READY",
        "collision3_ready_credit": 0,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["cache_replay_id"] = "c41-cache-replay:" + digest(semantic)
    return semantic


def independent_task_packet(
    task: dict[str, Any], config: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    source = task["source"]
    source_fraction = Q(source["parent_volume_fraction"])
    packet: dict[str, list[dict[str, Any]]] = {
        "ambient": [], "split": [], "cache_replay": [],
        "c1": [], "endpoint": [], "c2": [], "incidence": [], "boundary": [],
    }
    if source["representative_box"] is None:
        route = {
            "box": None,
            "classification": "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL",
            "witness": source["witness"],
            "route_method": "C41_EXACT_ALGEBRAIC_H0_RECHART_OUTER",
            "c1_result": None,
            "c2_status": None,
            "c2_baseline": None,
            "c2_detail": None,
            "c2_evidence": [],
            "route_failure": None,
        }
        ambient, groups = independent_ambient(task, route, "", 0, source_fraction, [])
        packet["ambient"].append(ambient)
        for key in ("c1", "endpoint", "c2", "incidence", "boundary"):
            packet[key].extend(groups[key])
        return packet
    original = independent_route_at_path(task, source["path"], config)
    need(
        box_payload(original["box"]) == source["representative_box"],
        "C40 source exact box replay",
    )
    if source["classification"] == "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER":
        packet["cache_replay"].append(independent_cache_replay(source, original))
    stack: list[tuple[str, int, Q, list[str], dict[str, Any] | None]] = [
        ("", 0, source_fraction, [], original)
    ]
    while stack:
        bits, depth, fraction, history, cached = stack.pop()
        path = source["path"] + bits
        route = cached or independent_route_at_path(task, path, config)
        family = disposition_family(route["classification"])
        if family == "TERMINAL_EXCLUDED" or depth == EXTRA_DEPTH:
            ambient, groups = independent_ambient(
                task, route, bits, depth, fraction, history
            )
            packet["ambient"].append(ambient)
            for key in ("c1", "endpoint", "c2", "incidence", "boundary"):
                packet[key].extend(groups[key])
            continue
        adjacency, children, axis = independent_split(task, route["box"], bits, depth, history)
        packet["split"].append(adjacency)
        axis_name = ("t", "p", "s")[axis]
        for bit in ("1", "0"):
            child_path = path + bit
            child_route = independent_route_at_path(task, child_path, config)
            need(
                box_payload(child_route["box"]) == box_payload(children[int(bit)]),
                "exact split child reconstruction",
            )
            stack.append((
                bits + bit,
                depth + 1,
                fraction / 2,
                history + [axis_name],
                child_route,
            ))
    packet["ambient"].sort(key=lambda row: row["path"])
    paths = [row["path"] for row in packet["ambient"]]
    need(
        len(paths) == len(set(paths))
        and not any(
            left != right and right.startswith(left)
            for left, right in itertools.product(paths, repeat=2)
        )
        and sum(Q(row["parent_volume_fraction"]) for row in packet["ambient"])
        == source_fraction,
        "independent packet prefix/Kraft closure",
    )
    return packet


def task_for_source(
    ordinal: int,
    source: dict[str, Any],
    c38_index: dict[str, dict[str, Any]],
    cells: dict[str, dict[str, Any]],
    seams: list[dict[str, Any]],
) -> dict[str, Any]:
    c38_source = c38_index.get(source["c38_source_row_sha256"])
    cell = cells.get(source["representative_cell_id"])
    need(c38_source is not None and cell is not None, "C40 geometry foreign keys")
    by_cell = [
        row for row in seams
        if cell["cell_id"] in {row["left_cell_id"], row["right_cell_id"]}
    ]
    by_cell.sort(key=lambda row: (
        Q(row["physical_p_span"][0]["value"]),
        Q(row["physical_p_span"][1]["value"]),
        row["row_sha256"],
    ))
    return {
        "source_ordinal": ordinal,
        "source": source,
        "c38_source": c38_source,
        "cell": cell,
        "seams": by_cell if source["representative_box"] is None else [],
    }


def independent_crosswalk(ordinal: int, source: dict[str, Any]) -> dict[str, Any]:
    semantic = {
        "schema": CROSSWALK_SCHEMA,
        "c40_source_ordinal": ordinal,
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": source["c38_source_row_sha256"],
        "pair_index": source["pair_index"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "source_parent_volume_fraction": source["parent_volume_fraction"],
        "source_classification": source["classification"],
        "normalized_residual_classification": residual_classification(
            source["classification"]
        ),
        "route_exception_phase": source["route_exception_phase"],
        "route_exception_type": source["route_exception_type"],
        "route_exception_message": source["route_exception_message"],
        "selected_exactly_once": True,
        "depth_policy": (
            "STRICT_EXCLUSION_EARLY_STOP_OTHERWISE_EXACTLY_THREE_DYADIC_SPLITS"
        ),
        "maximum_additional_depth": EXTRA_DEPTH,
        "input_ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["input_crosswalk_id"] = "c41-input:" + digest(semantic)
    return semantic


def independent_carry(source: dict[str, Any]) -> dict[str, Any]:
    family = disposition_family(source["classification"])
    need(family in {"TERMINAL_EXCLUDED", "COLLISION3_READY"}, "carry family")
    semantic = {
        "schema": AMBIENT_SCHEMA,
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "c40_source_row_sha256": source["row_sha256"],
        "c40_source_classification": source["classification"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "descendant_bits": "",
        "path": source["path"],
        "additional_depth": 0,
        "split_axis_history": [],
        "parent_volume_fraction": source["parent_volume_fraction"],
        "closed_representative_box": source["representative_box"],
        "closed_reflected_box": source["reflected_box"],
        "half_open_owner_policy": "C40_FROZEN_PREFIX_CARRY",
        "raw_classification": source["classification"],
        "raw_witness": source["witness"],
        "route_method": "C41_C40_FROZEN_PREFIX_CARRY",
        "disposition_family": family,
        "residual_classification": None,
        "route_failure": source["route_failure"],
        "c2_status": None,
        "c2_baseline": None,
        "obligation_ids": [],
        "round144_terminal_class": source["round144_terminal_class"],
        "local_round144_terminal_credit": 1 if family == "TERMINAL_EXCLUDED" else 0,
        "lower_dimensional_ambient_credit": 0,
        "collision3_ready_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["c41_ambient_cell_id"] = "c41-ambient:" + digest(semantic)
    return semantic


def install_complete_cache() -> dict[str, tuple[str, ...]]:
    base = round166.base
    generator = base.candidate_ids
    generated = {chart: tuple(generator(chart)) for chart in CHART_ORDER}
    for chart, (count, expected_digest) in EXPECTED_CHART_CANDIDATES.items():
        need(
            len(generated[chart]) == count
            and digest(list(generated[chart])) == expected_digest,
            "full chart candidate cache:" + chart,
        )
    candidate_cache = MappingProxyType(dict(generated))
    target_cache = MappingProxyType({target.target_id: target for target in base.TARGETS})

    def candidate_ids(chart_id: str) -> list[str]:
        need(chart_id in candidate_cache, "uncached chart:" + chart_id)
        return list(candidate_cache[chart_id])

    def target_by_id(target_id: str) -> Any:
        need(target_id in target_cache, "uncached target:" + target_id)
        return target_cache[target_id]

    round166._candidate_cache = candidate_cache
    round166._target_cache = target_cache
    base.candidate_ids = candidate_ids
    base.target_by_id = target_by_id
    round166.atlas.records = round166.records_full
    round166.atlas.root_record = round166.root_record_fast
    return generated


def independent_singletons(
    generated: dict[str, tuple[str, ...]],
) -> list[dict[str, Any]]:
    pair_index, _pattern_index, registry_sha = (
        round139.lower.component_cert.key_index_tables()
    )
    need(
        len(pair_index) == 448 and registry_sha == EXPECTED_OFFICIAL_REGISTRY_SHA256,
        "official singleton registry",
    )
    rows: list[dict[str, Any]] = []
    for chart in CHART_ORDER:
        for ordinal, target_id in enumerate(generated[chart]):
            key = (chart, target_id)
            need(key in pair_index, "singleton registry foreign key")
            semantic = {
                "schema": SINGLETON_SCHEMA,
                "chart_id": chart,
                "chart_candidate_ordinal": ordinal,
                "target_id": target_id,
                "official_pair_key_index": pair_index[key],
                "chart_candidate_count": len(generated[chart]),
                "chart_candidate_ids_sha256": EXPECTED_CHART_CANDIDATES[chart][1],
                "official_registry_sha256": registry_sha,
                "immutable_full_chart_cache": True,
                "singleton_ambient_or_whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            semantic["candidate_singleton_id"] = (
                "c41-candidate-singleton:" + digest(semantic)
            )
            rows.append(semantic)
    need(len(rows) == 448, "singleton census")
    return rows


def accumulate_parent(
    accumulators: dict[int, dict[str, Any]], ambient: dict[str, Any],
) -> None:
    value = accumulators[ambient["pair_index"]]
    fraction = Q(ambient["parent_volume_fraction"])
    need(fraction > 0, "positive ambient fraction")
    value["paths"].append(ambient["path"])
    value["total"] += fraction
    if ambient["disposition_family"] == "TERMINAL_EXCLUDED":
        value["terminal"] += fraction
        value["terminal_leaf_count"] += 1
        value["terminal_reflection_materialized"] = bool(
            value["terminal_reflection_materialized"]
            and ambient["closed_reflected_box"] is not None
        )
    else:
        value["nonterminal_leaf_count"] += 1


def validate_parent_rows(
    cursor: Cursor,
    accumulators: dict[int, dict[str, Any]],
    prior_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    prior = {row["pair_index"]: row for row in prior_rows}
    need(len(prior) == 862, "C40 parent index")
    full = partial = zero = newly_full = 0
    terminal_equivalent = Q(0)
    unresolved_equivalent = Q(0)
    for pair in range(862):
        value = accumulators[pair]
        paths = sorted(value["paths"])
        need(
            bool(paths)
            and len(paths) == len(set(paths))
            and not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
            "parent prefix-free:" + str(pair),
        )
        total = value["total"]
        terminal = value["terminal"]
        unresolved = total - terminal
        need(total == 1 and unresolved >= 0, "parent exact Kraft:" + str(pair))
        old = prior[pair]
        prior_terminal = Q(old["terminal_excluded_parent_volume"])
        need(terminal >= prior_terminal, "parent terminal monotonicity")
        whole = (
            terminal == 1
            and value["nonterminal_leaf_count"] == 0
            and value["terminal_reflection_materialized"]
        )
        if terminal == 1:
            need(whole, "whole parent reflection transport")
        if whole:
            full += 1
        elif terminal == 0:
            zero += 1
        else:
            partial += 1
        newly = whole and not old["whole_representative_parent_terminal"]
        newly_full += int(newly)
        terminal_equivalent += terminal
        unresolved_equivalent += unresolved
        cursor.consume({
            "schema": PARENT_SCHEMA,
            "pair_index": pair,
            "c40_parent_row_sha256": old["row_sha256"],
            "leaf_count": len(paths),
            "terminal_leaf_count": value["terminal_leaf_count"],
            "nonterminal_leaf_count": value["nonterminal_leaf_count"],
            "path_prefix_free": True,
            "terminal_excluded_parent_volume": qstr(terminal),
            "unresolved_parent_volume": qstr(unresolved),
            "parent_Kraft_conservation": "1",
            "whole_representative_parent_terminal": whole,
            "whole_reflected_parent_terminal": whole,
            "terminal_reflection_transport_materialized": value[
                "terminal_reflection_materialized"
            ],
            "newly_whole_terminal_vs_C40": newly,
            "C34_common_refinement_credit": 2 if whole else 0,
            "lower_dimensional_credit": 0,
            "D02_gate_credit": 0,
        })
    need(
        full + partial + zero == 862
        and full >= 250
        and newly_full == full - 250
        and terminal_equivalent + unresolved_equivalent == 862,
        "global parent conservation",
    )
    cursor.finish()
    return {
        "whole_terminal_representative_parent_count": full,
        "whole_terminal_paired_coarse_cell_count": 2 * full,
        "newly_whole_terminal_representative_parent_count": newly_full,
        "newly_whole_terminal_paired_coarse_cell_count": 2 * newly_full,
        "partial_representative_parent_count": partial,
        "zero_progress_representative_parent_count": zero,
        "representative_terminal_parent_equivalent": qstr(terminal_equivalent),
        "representative_unresolved_parent_equivalent": qstr(unresolved_equivalent),
    }


def validate_full_reconstruction(
    rows: dict[str, list[dict[str, Any]]],
    c40_rows: dict[str, list[dict[str, Any]]],
    c38_index: dict[str, dict[str, Any]],
    cells: dict[str, dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    generated = install_complete_cache()
    singleton_cursor = Cursor(
        rows["candidate_universe_singletons.jsonl.gz"], "singletons"
    )
    for singleton in independent_singletons(generated):
        singleton_cursor.consume(singleton)
    singleton_cursor.finish()
    cursors = {
        "crosswalk": Cursor(rows["input_blocker_crosswalk.jsonl.gz"], "crosswalk"),
        "ambient": Cursor(rows["routed_ambient_cells.jsonl.gz"], "ambient"),
        "split": Cursor(rows["split_face_adjacency.jsonl.gz"], "split"),
        "cache_replay": Cursor(rows["full_chart_cache_replay.jsonl.gz"], "cache"),
        "c1": Cursor(rows["c1_h1_surface_outers.jsonl.gz"], "c1"),
        "endpoint": Cursor(rows["endpoint_recharts.jsonl.gz"], "endpoint"),
        "c2": Cursor(rows["c2_surface_outers.jsonl.gz"], "c2"),
        "incidence": Cursor(rows["incidence_outers.jsonl.gz"], "incidence"),
        "boundary": Cursor(rows["boundary_corner_outers.jsonl.gz"], "boundary"),
    }
    accumulators: dict[int, dict[str, Any]] = {
        pair: {
            "paths": [],
            "total": Q(0),
            "terminal": Q(0),
            "terminal_leaf_count": 0,
            "nonterminal_leaf_count": 0,
            "terminal_reflection_materialized": True,
        }
        for pair in range(862)
    }
    source_census: Counter[str] = Counter()
    raw_census: Counter[str] = Counter()
    disposition_census: Counter[str] = Counter()
    residual_census: Counter[str] = Counter()
    cache_census: Counter[str] = Counter()
    endpoint_census: Counter[str] = Counter()
    algebraic_seams = terminal = ready = selected = 0
    sources = c40_rows["routed_leaf_cells.jsonl.gz"]
    need(len(sources) == EXPECTED_C40_ROW_COUNT, "C40 row count")
    seams = config["source_chart_seams"]
    for ordinal, source in enumerate(sources):
        classification = source["classification"]
        source_census[classification] += 1
        family = disposition_family(classification)
        if family == "TERMINAL_EXCLUDED":
            terminal += 1
            ambient_rows = [independent_carry(source)]
            packet = {key: [] for key in (
                "split", "cache_replay", "c1", "endpoint", "c2", "incidence", "boundary"
            )}
        elif family == "COLLISION3_READY":
            ready += 1
            ambient_rows = [independent_carry(source)]
            packet = {key: [] for key in (
                "split", "cache_replay", "c1", "endpoint", "c2", "incidence", "boundary"
            )}
        else:
            need(classification in LOWER_BLOCKER_CENSUS, "unexpected C40 residual")
            selected += 1
            cursors["crosswalk"].consume(independent_crosswalk(ordinal, source))
            task = task_for_source(ordinal, source, c38_index, cells, seams)
            packet = independent_task_packet(task, config)
            ambient_rows = packet["ambient"]
        for ambient in ambient_rows:
            cursors["ambient"].consume(ambient)
            accumulate_parent(accumulators, ambient)
            raw_census[ambient["raw_classification"]] += 1
            disposition_census[ambient["disposition_family"]] += 1
            if ambient["residual_classification"] is not None:
                residual_census[ambient["residual_classification"]] += 1
        for group in (
            "split", "cache_replay", "c1", "endpoint", "c2", "incidence", "boundary"
        ):
            for item in packet[group]:
                cursors[group].consume(item)
                if group == "cache_replay":
                    cache_census[item["replay_classification"]] += 1
                elif group == "endpoint":
                    geometry = item["endpoint_rechart_geometry"]
                    endpoint_census[geometry["endpoint_kind"]] += 1
                    algebraic_seams += geometry.get(
                        "adjacent_chart_seam_incidence_count", 0
                    )
    need(
        terminal == EXPECTED_C40_TERMINAL_ROW_COUNT
        and ready == EXPECTED_C40_COLLISION3_READY_ROW_COUNT
        and selected == EXPECTED_LOWER_BLOCKER_COUNT
        and {key: source_census[key] for key in LOWER_BLOCKER_CENSUS}
        == LOWER_BLOCKER_CENSUS
        and dict(sorted(cache_census.items())) == EXPECTED_CACHE_REPLAY_CENSUS
        and endpoint_census["ALGEBRAIC_H0_SOURCE_CHART_SEAM"] == 29
        and algebraic_seams == 33,
        "full C40 partition and C41 fixed censuses",
    )
    for cursor in cursors.values():
        cursor.finish()
    parent_cursor = Cursor(rows["parent_conservation.jsonl.gz"], "parent")
    parents = validate_parent_rows(
        parent_cursor, accumulators, c40_rows["parent_conservation.jsonl.gz"]
    )
    return {
        "C40_classification_census": dict(sorted(source_census.items())),
        "raw_classification_census": dict(sorted(raw_census.items())),
        "disposition_family_census": dict(sorted(disposition_census.items())),
        "normalized_residual_classification_census": dict(sorted(residual_census.items())),
        "cache_replay_census": dict(sorted(cache_census.items())),
        "endpoint_kind_census": dict(sorted(endpoint_census.items())),
        "algebraic_seam_incidence_count": algebraic_seams,
        "input": {
            "C40_routed_leaf_count": len(sources),
            "C40_terminal_carry_count": terminal,
            "C40_collision3_ready_carry_count": ready,
            "selected_lower_blocker_count": selected,
        },
        "parents": parents,
    }


def validate_result_semantics(
    result: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
    reconstructed: dict[str, Any],
) -> None:
    parents = reconstructed["parents"]
    full = parents["whole_terminal_representative_parent_count"]
    formal_excluded = 74_812 + 2 * full
    formal_unresolved = 1_724 - 2 * full
    need(
        formal_excluded + 296 + formal_unresolved == 76_832
        and 0 <= formal_unresolved <= 1_224,
        "terminal census arithmetic",
    )
    need(
        result.get("status") == (
            "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__"
            f"{len(rows['routed_ambient_cells.jsonl.gz'])}_AMBIENT_LEAVES__"
            f"{2 * full}_WHOLE_CELLS_TERMINAL__"
            f"{formal_unresolved}_FORMAL_UNRESOLVED"
        ),
        "C41 result status",
    )
    numeric = result.get("numeric_authority")
    need(
        type(numeric) is dict
        and numeric.get("source_sha256") == EXPECTED_SOURCE_SHA256
        and numeric.get("flint_version") == flint.__version__ == "0.9.0"
        and numeric.get("precision_bits") == PRECISION_BITS
        and numeric.get("maximum_additional_dyadic_depth") == EXTRA_DEPTH
        and numeric.get("strict_exclusion_early_stop") is True
        and numeric.get("official_registry_sha256")
        == EXPECTED_OFFICIAL_REGISTRY_SHA256
        and numeric.get("upstream_authority_object_sha256")
        == EXPECTED_UPSTREAM_OBJECTS
        and numeric.get("full_chart_candidate_count") == 448
        and numeric.get("candidate_cache_immutable") is True
        and numeric.get("tuple_codec")
        == "CANONICAL_JSON_LIST_OF_STRINGS_COLLISION_FREE"
        and numeric.get("source_slice") == "s=0",
        "C41 numeric authority",
    )
    need(
        numeric.get("full_chart_candidate_cache") == {
            chart: {
                "candidate_count": EXPECTED_CHART_CANDIDATES[chart][0],
                "candidate_ids_sha256": EXPECTED_CHART_CANDIDATES[chart][1],
            }
            for chart in CHART_ORDER
        },
        "C41 chart cache authority",
    )
    input_census = result.get("input_census")
    need(
        type(input_census) is dict
        and all(
            input_census.get(key) == value
            for key, value in reconstructed["input"].items()
        )
        and input_census.get("C40_classification_census")
        == reconstructed["C40_classification_census"]
        and input_census.get("selected_lower_blocker_classification_census")
        == LOWER_BLOCKER_CENSUS,
        "C41 input census",
    )
    routing = result.get("routing_census")
    need(
        type(routing) is dict
        and routing.get("routed_ambient_cell_count")
        == len(rows["routed_ambient_cells.jsonl.gz"])
        and routing.get("split_face_adjacency_count")
        == len(rows["split_face_adjacency.jsonl.gz"])
        and routing.get("raw_classification_census")
        == reconstructed["raw_classification_census"]
        and routing.get("disposition_family_census")
        == reconstructed["disposition_family_census"]
        and routing.get("normalized_residual_classification_census")
        == reconstructed["normalized_residual_classification_census"]
        and routing.get("full_chart_cache_replay_count") == 19
        and routing.get("full_chart_cache_replay_census")
        == reconstructed["cache_replay_census"]
        and all(routing.get(key) == value for key, value in parents.items()),
        "C41 routing census",
    )
    lower = result.get("lower_strata_census")
    need(
        type(lower) is dict
        and lower.get("normalized_surface_registry_schema")
        == NORMALIZED_SURFACE_REGISTRY_SCHEMA
        and lower.get("normalized_surface_registry_storage")
        == "NESTED_ONE_ENTRY_PER_SURFACE_INSIDE_OWNING_PRIMARY_OUTER_ROW"
        and lower.get("candidate_universe_singleton_count") == 448
        and lower.get("c1_h1_surface_outer_count")
        == len(rows["c1_h1_surface_outers.jsonl.gz"])
        and lower.get("endpoint_rechart_count")
        == len(rows["endpoint_recharts.jsonl.gz"])
        and lower.get("endpoint_rechart_kind_census")
        == reconstructed["endpoint_kind_census"]
        and lower.get("algebraic_H0_endpoint_rechart_count") == 29
        and lower.get("algebraic_C32_seam_incidence_count") == 33
        and lower.get("c2_surface_outer_count")
        == len(rows["c2_surface_outers.jsonl.gz"])
        and lower.get("incidence_outer_count")
        == len(rows["incidence_outers.jsonl.gz"])
        and lower.get("boundary_corner_outer_count")
        == len(rows["boundary_corner_outers.jsonl.gz"])
        and lower.get("certified_zero_dimensional_intersection_count") == 0
        and lower.get("lower_dimensional_ambient_credit") == 0
        and lower.get("D02_gate_credit") == 0,
        "C41 lower-strata census",
    )
    need(
        result.get("round144_terminal_census") == {
            "CONNECTED_TO_KNOWN": 0,
            "EARLIEST_PREFIX_EXCLUDED": formal_excluded,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": formal_unresolved,
            "terminal_total": 76_832,
            "unresolved_zero": formal_unresolved == 0,
        },
        "C41 terminal census",
    )
    need(
        result.get("strict_nonpromotion") == {
            "lower_dimensional_graph_credit": 0,
            "endpoint_seam_incidence_corner_ambient_credit": 0,
            "collision3_ready_credit": 0,
            "four_class_terminal_census_unresolved_zero": False,
            "D02": f"BLOCKED_BY_{formal_unresolved}_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "C41 strict nonpromotion",
    )
    need(
        "out-of-band" in result.get("execution_receipt_policy", "")
        and "collisions 3--1648" in result.get("required_next", ""),
        "C41 policy statements",
    )


def receipt_closure(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    claimed = body.pop("receipt_object_sha256", None)
    need(
        type(claimed) is str
        and HEX64.fullmatch(claimed) is not None
        and claimed == digest(body),
        "receipt closure:" + label,
    )


def validate_receipt(
    path: Path,
    invocation_id: str,
    candidate: Path,
    result: dict[str, Any],
    manifest_sha256: str,
) -> dict[str, Any]:
    raw, _identity = stable_read(path, 4 << 20, "C41 receipt")
    receipt = strict_json_bytes(raw, "C41 receipt")
    receipt_closure(receipt, "C41 receipt")
    expected_keys = {
        "schema", "status", "InvocationID", "producer_pid", "producer_parent_pid",
        "producer_proc_start_ticks", "producer_executable", "producer_source_sha256",
        "candidate_path", "candidate_object_sha256", "root_manifest_sha256",
        "candidate_inventory_count", "receipt_object_sha256",
    }
    executable = receipt.get("producer_executable")
    need(
        set(receipt) == expected_keys
        and receipt.get("schema") == RECEIPT_SCHEMA
        and receipt.get("status") == "PASS_LIVE_PID_INVOCATION_BOUND_TO_C41_OBJECT"
        and TOKEN.fullmatch(invocation_id) is not None
        and receipt.get("InvocationID") == invocation_id
        and type(receipt.get("producer_pid")) is int
        and receipt["producer_pid"] > 1
        and type(receipt.get("producer_parent_pid")) is int
        and receipt["producer_parent_pid"] > 0
        and type(receipt.get("producer_proc_start_ticks")) is int
        and receipt["producer_proc_start_ticks"] > 0
        and type(executable) is str
        and Path(executable).resolve() == Path(sys.executable).resolve()
        and receipt.get("producer_source_sha256") == EXPECTED_PRODUCER_SOURCE
        and receipt.get("candidate_path") == str(candidate.relative_to(ROOT))
        and receipt.get("candidate_object_sha256") == result["object_sha256"]
        and receipt.get("root_manifest_sha256") == manifest_sha256
        and receipt.get("candidate_inventory_count") == len(INVENTORY),
        "C41 receipt PID/InvocationID/object/manifest binding",
    )
    receipt_absolute = path.resolve()
    need(
        receipt_absolute.parent != candidate
        and candidate not in receipt_absolute.parents,
        "C41 receipt out of band",
    )
    return receipt


def reclose_domain_row(row: dict[str, Any], field: str, prefix: str) -> None:
    row.pop("row_sha256", None)
    row.pop(field, None)
    row[field] = prefix + digest(row)
    row["row_sha256"] = digest(row)


def reject_mutation(label: str, operation: Any) -> bool:
    try:
        operation()
    except (Reject, KeyError, IndexError, TypeError, ValueError):
        return True
    raise Reject("integrity mutation accepted:" + label)


def mutation_suite(
    result: dict[str, Any],
    receipt: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
    invocation_id: str,
    manifest_sha256: str,
) -> dict[str, bool]:
    def changed(reference: Any, mutator: Any, label: str) -> None:
        forged = copy.deepcopy(reference)
        mutator(forged)
        need(forged == reference, "mutation:" + label)

    ambient = rows["routed_ambient_cells.jsonl.gz"][0]
    split = rows["split_face_adjacency.jsonl.gz"][0]
    crosswalk = rows["input_blocker_crosswalk.jsonl.gz"][0]
    cache = rows["full_chart_cache_replay.jsonl.gz"][0]
    singleton = rows["candidate_universe_singletons.jsonl.gz"][0]
    parent = rows["parent_conservation.jsonl.gz"][0]
    primary_rows = (
        rows["c1_h1_surface_outers.jsonl.gz"]
        + rows["c2_surface_outers.jsonl.gz"]
        + rows["endpoint_recharts.jsonl.gz"]
    )
    primary = next(row for row in primary_rows if row.get("normalized_surfaces"))
    endpoint = rows["endpoint_recharts.jsonl.gz"][0]
    incidence = rows["incidence_outers.jsonl.gz"][0]
    boundary = rows["boundary_corner_outers.jsonl.gz"][0]

    def result_object() -> None:
        forged = copy.deepcopy(result)
        forged["status"] += "_MUTATED"
        body = dict(forged)
        body.pop("object_sha256", None)
        forged["object_sha256"] = digest(body)
        need(forged["object_sha256"] == EXPECTED_CANDIDATE_OBJECT, "mutation:result")

    def receipt_field(field: str, value: Any) -> Any:
        def operation() -> None:
            forged = copy.deepcopy(receipt)
            forged[field] = value
            body = dict(forged)
            body.pop("receipt_object_sha256", None)
            forged["receipt_object_sha256"] = digest(body)
            need(
                forged[field] == receipt[field],
                "mutation:receipt:" + field,
            )
        return operation

    def domain_change(
        reference: dict[str, Any], field: str, value: Any,
        id_field: str, prefix: str, label: str,
    ) -> Any:
        def operation() -> None:
            forged = copy.deepcopy(reference)
            forged[field] = value
            reclose_domain_row(forged, id_field, prefix)
            need(forged == reference, "mutation:" + label)
        return operation

    cases: dict[str, Any] = {
        "result_object": result_object,
        "manifest_binding": lambda: need("0" * 64 == manifest_sha256, "mutation:manifest"),
        "receipt_invocation": receipt_field("InvocationID", invocation_id + ".changed"),
        "receipt_pid": receipt_field("producer_pid", receipt["producer_pid"] + 1),
        "receipt_candidate_object": receipt_field("candidate_object_sha256", "0" * 64),
        "receipt_manifest": receipt_field("root_manifest_sha256", "0" * 64),
        "crosswalk_source": domain_change(
            crosswalk, "c40_source_leaf_id", "c40-leaf:" + "0" * 64,
            "input_crosswalk_id", "c41-input:", "crosswalk source",
        ),
        "crosswalk_ordinal": domain_change(
            crosswalk, "c40_source_ordinal", crosswalk["c40_source_ordinal"] + 1,
            "input_crosswalk_id", "c41-input:", "crosswalk ordinal",
        ),
        "ambient_fraction": domain_change(
            ambient, "parent_volume_fraction", "999",
            "c41_ambient_cell_id", "c41-ambient:", "ambient fraction",
        ),
        "ambient_box": lambda: changed(
            ambient,
            lambda row: row["closed_representative_box"].update({"t": ["0", "999"]})
            if row["closed_representative_box"] is not None
            else row.update({"closed_representative_box": {"t": ["0", "1"]}}),
            "ambient box",
        ),
        "ambient_obligation": lambda: changed(
            next(row for row in rows["routed_ambient_cells.jsonl.gz"] if row["obligation_ids"]),
            lambda row: row["obligation_ids"].append("c41-incidence:" + "0" * 64),
            "ambient obligation",
        ),
        "split_axis": domain_change(
            split, "split_axis", "p" if split["split_axis"] == "t" else "t",
            "split_face_adjacency_id", "c41-split:", "split axis",
        ),
        "split_child_box": lambda: changed(
            split,
            lambda row: row["lower_child_closed_box"]["t"].__setitem__(0, "999"),
            "split child box",
        ),
        "split_child_path": domain_change(
            split, "lower_child_path", split["lower_child_path"] + "0",
            "split_face_adjacency_id", "c41-split:", "split child path",
        ),
        "primary_pair": lambda: changed(
            primary, lambda row: row.update({"pair_index": row["pair_index"] + 1}),
            "primary pair",
        ),
        "normalized_surface_id": lambda: changed(
            primary,
            lambda row: row["normalized_surfaces"][0].update(
                {"normalized_surface_id": "c41-normalized-surface:" + "0" * 64}
            ),
            "normalized surface id",
        ),
        "normalized_surface_credit": lambda: changed(
            primary,
            lambda row: row["normalized_surfaces"][0].update({"D02_gate_credit": 1}),
            "normalized surface credit",
        ),
        "incidence_owner": domain_change(
            incidence, "owning_outer_id", "c41-c1-h1-outer:" + "0" * 64,
            "incidence_outer_id", "c41-incidence:", "incidence owner",
        ),
        "incidence_surface": domain_change(
            incidence, "left_normalized_surface_id", "c41-normalized-surface:" + "0" * 64,
            "incidence_outer_id", "c41-incidence:", "incidence surface",
        ),
        "incidence_source": domain_change(
            incidence, "c40_source_leaf_id", "c40-leaf:" + "0" * 64,
            "incidence_outer_id", "c41-incidence:", "incidence source",
        ),
        "incidence_pair": domain_change(
            incidence, "pair_index", incidence["pair_index"] + 1,
            "incidence_outer_id", "c41-incidence:", "incidence pair",
        ),
        "boundary_owner": domain_change(
            boundary, "owning_outer_id", "c41-c1-h1-outer:" + "0" * 64,
            "boundary_corner_outer_id", "c41-boundary-corner:", "boundary owner",
        ),
        "boundary_source": domain_change(
            boundary, "c40_source_leaf_id", "c40-leaf:" + "0" * 64,
            "boundary_corner_outer_id", "c41-boundary-corner:", "boundary source",
        ),
        "boundary_path": domain_change(
            boundary, "descendant_path", boundary["descendant_path"] + "0",
            "boundary_corner_outer_id", "c41-boundary-corner:", "boundary path",
        ),
        "boundary_face_box": lambda: changed(
            next(row for row in rows["boundary_corner_outers.jsonl.gz"] if row["face_rows"]),
            lambda row: row["face_rows"][0]["exact_closed_face_box"]["t"].__setitem__(0, "999"),
            "boundary face box",
        ),
        "boundary_face_link": lambda: changed(
            next(
                row for row in rows["boundary_corner_outers.jsonl.gz"]
                if any(face["surface_face_incidence_links"] for face in row["face_rows"])
            ),
            lambda row: row["face_rows"][0]["surface_face_incidence_links"][0].update(
                {"normalized_surface_id": "c41-normalized-surface:" + "0" * 64}
            ),
            "boundary face link",
        ),
        "endpoint_geometry": lambda: changed(
            endpoint,
            lambda row: row["endpoint_rechart_geometry"].update(
                {"carrier_existence_status": "UNRESOLVED"}
            ),
            "endpoint geometry",
        ),
        "endpoint_credit": lambda: changed(
            endpoint, lambda row: row.update({"D02_gate_credit": 1}), "endpoint credit"
        ),
        "cache_candidate_count": domain_change(
            cache, "official_candidate_count", 54,
            "cache_replay_id", "c41-cache-replay:", "cache candidate count",
        ),
        "cache_disposition": domain_change(
            cache, "replay_classification", "EXCLUDED_MUTATED",
            "cache_replay_id", "c41-cache-replay:", "cache disposition",
        ),
        "singleton_registry": domain_change(
            singleton, "official_pair_key_index", singleton["official_pair_key_index"] + 1,
            "candidate_singleton_id", "c41-candidate-singleton:", "singleton registry",
        ),
        "parent_kraft": lambda: changed(
            parent, lambda row: row.update({"parent_Kraft_conservation": "0"}),
            "parent Kraft",
        ),
        "parent_credit": lambda: changed(
            parent, lambda row: row.update({"D02_gate_credit": 1}), "parent credit"
        ),
        "nonpromotion_lock": lambda: need(
            EXPECTED_NONPROMOTION_LOCK + b"x" == EXPECTED_NONPROMOTION_LOCK,
            "mutation:lock",
        ),
    }
    need(len(cases) >= 24, "at least 24 integrity mutations")
    return {
        label: reject_mutation(label, operation)
        for label, operation in cases.items()
    }


def core_projection(
    candidate: Path, receipt_path: Path, invocation_id: str,
) -> dict[str, Any]:
    formal_pins_ready()
    no_producer_import()
    need(
        file_sha256(PRODUCER) == EXPECTED_PRODUCER_SOURCE,
        "frozen C41 producer source",
    )
    pins = source_pins()
    ctx.prec = PRECISION_BITS
    candidate = candidate.resolve(strict=True)
    receipt_path = receipt_path.resolve(strict=True)
    result, rows, manifest_sha256, directory_identity, file_identities = (
        capture_c41_candidate(candidate)
    )
    (
        c40_candidate,
        c40_result,
        c40_rows,
        c38_index,
        cells,
        config,
        _c39_parents,
    ) = load_c40_authority(result)
    reconstructed = validate_full_reconstruction(
        rows, c40_rows, c38_index, cells, config
    )
    validate_result_semantics(result, rows, reconstructed)
    receipt = validate_receipt(
        receipt_path, invocation_id, candidate, result, manifest_sha256
    )
    mutations = mutation_suite(
        result, receipt, rows, invocation_id, manifest_sha256
    )
    second_result, _rows, second_manifest, second_directory, second_files = (
        capture_c41_candidate(candidate)
    )
    need(
        second_result == result
        and second_manifest == manifest_sha256
        and second_directory == directory_identity
        and second_files == file_identities,
        "terminal C41 candidate recapture",
    )
    return {
        "schema": SCHEMA + ".core-projection.v1",
        "candidate_path": str(candidate.relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "root_manifest_sha256": manifest_sha256,
        "execution_receipt_object_sha256": receipt["receipt_object_sha256"],
        "InvocationID": invocation_id,
        "C40_candidate_path": str(c40_candidate.relative_to(ROOT)),
        "C40_object_sha256": c40_result["object_sha256"],
        "C40_independent_audit_object_sha256": EXPECTED_C40_AUDIT_OBJECT,
        "independent_source_sha256": pins,
        "ledger_row_counts": {
            filename: len(rows[filename]) for filename in LEDGER_NAMES
        },
        "reconstructed": reconstructed,
        "round144_terminal_census": result["round144_terminal_census"],
        "strict_nonpromotion": result["strict_nonpromotion"],
        "integrity_mutations": mutations,
    }


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(DELIVERABLES)
        if not existing else str(DELIVERABLES) + os.pathsep + existing
    )
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "0"
    return environment


def cold_replay_bytes(
    candidate: Path, receipt: Path, invocation_id: str,
) -> tuple[bytes, bytes]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--core-projection",
        "--candidate", str(candidate.resolve()),
        "--receipt", str(receipt.resolve()),
        "--invocation-id", invocation_id,
    ]
    outputs: list[bytes] = []
    for _ordinal in range(2):
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=child_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        need(
            completed.returncode == 0
            and completed.stderr == b""
            and completed.stdout.endswith(b"\n"),
            "fresh cold core process",
        )
        strict_json_bytes(completed.stdout, "cold C41 core")
        outputs.append(completed.stdout)
    need(outputs[0] == outputs[1], "byte-identical cold C41 cores")
    return outputs[0], outputs[1]


def fsync_directory(path: Path) -> None:
    before = path.lstat()
    need(stat.S_ISDIR(before.st_mode) and not path.is_symlink(), "audit directory")
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write_audit(path: Path, value: dict[str, Any]) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(not absolute.exists(), "audit output exists")
    absolute.parent.mkdir(parents=True, exist_ok=True)
    need(
        absolute.parent.resolve(strict=True) == absolute.parent
        and not absolute.parent.is_symlink(),
        "canonical audit parent",
    )
    stage = absolute.with_name(absolute.name + ".stage-" + str(os.getpid()))
    need(not stage.exists(), "audit stage exists")
    raw = canonical(value) + b"\n"
    descriptor = os.open(
        stage,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
        0o600,
    )
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            need(written > 0, "audit short write")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        os.replace(stage, absolute)
        fsync_directory(absolute.parent)
    except Exception:
        if stage.exists():
            stage.unlink()
            fsync_directory(stage.parent)
        raise
    replay, _identity = stable_read(absolute, 64 << 20, "terminal C41 audit")
    observed = strict_json_bytes(replay, "terminal C41 audit")
    closed_object(observed, "terminal C41 audit")
    need(replay == raw and observed == value, "terminal C41 audit byte replay")
    return replay


def run_audit(
    candidate: Path,
    receipt: Path,
    invocation_id: str,
    output: Path,
) -> dict[str, Any]:
    formal_pins_ready()
    candidate = candidate.resolve(strict=True)
    receipt = receipt.resolve(strict=True)
    before_payloads, before_directory, before_files = capture_directory(
        candidate,
        INVENTORY,
        {
            "result.json": 32 << 20,
            "root_manifest.sha256": 2 << 20,
            "C41_LOWER_STRATA_PARTIAL.lock": 1 << 20,
        },
        "C41 outer-before",
    )
    before_result = strict_json_bytes(
        before_payloads["result.json"], "C41 outer-before result"
    )
    closed_object(before_result, "C41 outer-before result")
    need(
        before_result.get("schema") == CANDIDATE_SCHEMA
        and before_result.get("object_sha256") == EXPECTED_CANDIDATE_OBJECT,
        "C41 outer-before pinned result",
    )
    output_absolute, _stage, _c40_candidate, _c40_audit = audit_output_preflight(
        candidate, receipt, output, before_result, os.getpid()
    )
    first, second = cold_replay_bytes(candidate, receipt, invocation_id)
    projection = strict_json_bytes(first, "selected C41 cold core")
    after_payloads, after_directory, after_files = capture_directory(
        candidate,
        INVENTORY,
        {
            "result.json": 32 << 20,
            "root_manifest.sha256": 2 << 20,
            "C41_LOWER_STRATA_PARTIAL.lock": 1 << 20,
        },
        "C41 outer-after",
    )
    need(
        before_payloads == after_payloads
        and before_directory == after_directory
        and before_files == after_files,
        "two-cold C41 candidate recapture",
    )
    mutations = dict(projection["integrity_mutations"])
    mutations["cold_core_byte_identity"] = first == second
    mutations["terminal_candidate_byte_replay"] = before_payloads == after_payloads
    mutations["terminal_audit_byte_replay"] = True
    need(len(mutations) >= 27 and all(mutations.values()), "complete mutation suite")
    audit = {
        "schema": SCHEMA,
        "status": (
            "PASS_INDEPENDENT_C41_DEPTH3_CLOSURE_AUDIT__"
            f"{len(mutations)}_OF_{len(mutations)}_MUTATIONS_REJECTED"
        ),
        "candidate_path": projection["candidate_path"],
        "candidate_object_sha256": projection["candidate_object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "execution_receipt_path": str(receipt.relative_to(ROOT)),
        "execution_receipt_object_sha256": projection[
            "execution_receipt_object_sha256"
        ],
        "InvocationID": invocation_id,
        "C40_object_sha256": EXPECTED_C40_OBJECT,
        "C40_independent_audit_object_sha256": EXPECTED_C40_AUDIT_OBJECT,
        "cold_core_projection_sha256": bytes_sha256(first),
        "cold_core_projection_byte_count": len(first),
        "reconstructed": {
            "ledger_row_counts": projection["ledger_row_counts"],
            **projection["reconstructed"],
            "round144_terminal_census": projection["round144_terminal_census"],
        },
        "mutations": mutations,
        "strict_nonpromotion": projection["strict_nonpromotion"],
        "method": (
            "no C41 producer import; exact 14-file FD capture; independent C40 "
            "authority replay; complete 35,009-row partition and 12,398-task "
            "depth-three reconstruction; exact surface/endpoint/incidence/boundary/"
            "parent foreign keys; two fresh cold cores; atomic terminal byte replay"
        ),
    }
    audit["object_sha256"] = digest(audit)
    atomic_write_audit(output_absolute, audit)
    return audit


def prewrite_regression_suite() -> dict[str, bool]:
    fixture = ROOT / ".cm2-runtime" / "prewrite-regression-fixture"
    c41_candidate = fixture / "c41-candidate"
    receipt = fixture / "receipts" / "c41-receipt.json"
    c40_candidate = fixture / "c40-candidate"
    c40_audit_parent = fixture / "audit" / "c40-authority"
    protected = (
        ("C41 candidate", c41_candidate),
        ("C41 receipt", receipt),
        ("C40 candidate", c40_candidate),
        ("C40 audit parent", c40_audit_parent),
    )

    def rejected(label: str, output: Path, stage: Path) -> bool:
        return reject_mutation(
            label,
            lambda: require_disjoint_targets(
                (("output", output), ("stage", stage)), protected
            ),
        )

    valid_output = fixture / "independent-audit" / "audit.json"
    valid_stage = fixture / "independent-audit" / "audit.json.stage-1"
    require_disjoint_targets(
        (("output", valid_output), ("stage", valid_stage)), protected
    )
    cases = {
        "output_equals_C41_candidate": rejected(
            "output_equals_C41_candidate", c41_candidate, valid_stage
        ),
        "output_inside_C41_candidate": rejected(
            "output_inside_C41_candidate", c41_candidate / "audit.json", valid_stage
        ),
        "output_inside_C40_candidate": rejected(
            "output_inside_C40_candidate", c40_candidate / "audit.json", valid_stage
        ),
        "output_inside_C40_audit_parent": rejected(
            "output_inside_C40_audit_parent", c40_audit_parent / "audit.json", valid_stage
        ),
        "stage_inside_C40_audit_parent": rejected(
            "stage_inside_C40_audit_parent", valid_output, c40_audit_parent / "stage"
        ),
        "output_collides_receipt": rejected(
            "output_collides_receipt", receipt, valid_stage
        ),
        "output_ancestor_of_C40_candidate": rejected(
            "output_ancestor_of_C40_candidate", fixture, valid_stage
        ),
    }
    need(all(cases.values()), "prewrite regression suite")
    return cases


def self_test() -> dict[str, Any]:
    pins = source_pins()
    need(
        HEX64.fullmatch(EXPECTED_C40_OBJECT) is not None,
        "fixed upstream C40 candidate object pin",
    )
    pending = (
        EXPECTED_PRODUCER_SOURCE.startswith("PENDING_")
        and EXPECTED_CANDIDATE_OBJECT.startswith("PENDING_")
        and EXPECTED_C40_AUDIT_OBJECT.startswith("PENDING_")
        and EXPECTED_C40_AUDIT_STATUS.startswith("PENDING_")
    )
    formally_pinned = (
        HEX64.fullmatch(EXPECTED_PRODUCER_SOURCE) is not None
        and HEX64.fullmatch(EXPECTED_CANDIDATE_OBJECT) is not None
        and HEX64.fullmatch(EXPECTED_C40_AUDIT_OBJECT) is not None
        and EXPECTED_C40_AUDIT_STATUS.startswith("PASS_")
    )
    need(
        pending != formally_pinned,
        "authority pins must be consistently all-PENDING or all-formal",
    )
    need(
        residual_classification("UNRESOLVED_COLLISION1_WORD")
        == "UNRESOLVED_C41_COLLISION1_WORD_COLLAR_OUTER"
        and residual_classification("UNRESOLVED_COLLISION2_WORD")
        == "UNRESOLVED_C41_COLLISION2_WORD_COLLAR_OUTER",
        "word collar mappings",
    )
    generated = install_complete_cache()
    singletons = independent_singletons(generated)
    need(
        len(singletons) == len({row["candidate_singleton_id"] for row in singletons})
        == 448,
        "singleton self-test",
    )
    probe = {"value": 1}
    need(
        reject_mutation(
            "self-test",
            lambda: need({"value": 2} == probe, "self-test mutation"),
        ),
        "mutation harness self-test",
    )
    prewrite = prewrite_regression_suite()
    return {
        "status": (
            "PASS_C41_AUDITOR_FORMAL_PIN_SELF_TEST"
            if formally_pinned
            else "PASS_C41_AUDITOR_PROVISIONAL_SELF_TEST__FORMAL_PINS_PENDING"
        ),
        "formal_pin_state": "FORMALLY_PINNED" if formally_pinned else "PENDING",
        "no_C41_producer_import": True,
        "source_sha256": pins,
        "chart_candidate_counts": {
            chart: len(generated[chart]) for chart in CHART_ORDER
        },
        "full_chart_candidate_count": 448,
        "singleton_count": len(singletons),
        "minimum_integrity_mutation_count": 24,
        "prewrite_regressions": prewrite,
        "formal_pins": {
            "producer_source": EXPECTED_PRODUCER_SOURCE,
            "candidate_object": EXPECTED_CANDIDATE_OBJECT,
            "C40_candidate_object": EXPECTED_C40_OBJECT,
            "C40_audit_object": EXPECTED_C40_AUDIT_OBJECT,
            "C40_audit_status": EXPECTED_C40_AUDIT_STATUS,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--core-projection", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            print(canonical(self_test()).decode("utf-8"))
            return 0
        need(
            arguments.candidate is not None
            and arguments.receipt is not None
            and arguments.invocation_id is not None,
            "candidate/receipt/InvocationID required",
        )
        if arguments.core_projection:
            print(canonical(core_projection(
                arguments.candidate,
                arguments.receipt,
                arguments.invocation_id,
            )).decode("utf-8"))
            return 0
        need(arguments.output is not None, "audit output required")
        print(canonical(run_audit(
            arguments.candidate,
            arguments.receipt,
            arguments.invocation_id,
            arguments.output,
        )).decode("utf-8"))
        return 0
    except Reject as error:
        if arguments.core_projection:
            return 1
        print("REJECT:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
