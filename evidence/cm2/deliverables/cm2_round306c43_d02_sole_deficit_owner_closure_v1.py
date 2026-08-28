#!/usr/bin/env python3
"""C43 producer-only closure for the owner-eligible sole-deficit subset.

The installed C42 authority is the only baseline.  The producer derives the
five post-C42 sole-deficit sources, recomputes their adaptive trees, and then
rebuilds the complete global boundary-owner census.  Only pairs 592 and 715
pass that census.  Pairs 97, 211, and 664 are retained as zero-credit
preflight blockers because a canonical exterior face or point owner is still
residual.

Formal output is a candidate plus an out-of-band execution receipt.  This
program has no code path that installs a C43 token, audit token, seal, or other
authority pointer.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from contextlib import ExitStack
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time
from typing import Any, Iterable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
sys.path.insert(0, str(SELF.parent))

from flint import arb, ctx, fmpq

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41
import cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1 as c42p
import cm2_round306c42_f1_authority_transaction_independent_auditor_v1 as c42tx
import cm2_round306c43b0_d02_sole_deficit_adaptive_pilot_v1 as pilot
import cm2_round306c43b0_d02_zero_surface_shard_planner_v1 as planner


RUNTIME = ROOT / ".cm2-runtime"
CANDIDATE_ROOT = RUNTIME / "candidates"
AUDIT_ROOT = RUNTIME / "audit"

SCHEMA = "cm2.round306c43.d02-sole-deficit-owner-closure.v1"
RECEIPT_SCHEMA = SCHEMA + ".execution-receipt"
SOURCE_PREFLIGHT_SCHEMA = SCHEMA + ".source-preflight"
SOURCE_SCHEMA = SCHEMA + ".exact-source"
SPLIT_SCHEMA = SCHEMA + ".adaptive-split"
LEAF_SCHEMA = SCHEMA + ".closed-leaf-certificate"
REFLECTION_SCHEMA = SCHEMA + ".reflection-transport"
INTERNAL_SCHEMA = SCHEMA + ".internal-strata-incidence"
FACE_SCHEMA = SCHEMA + ".source-face-owner-incidence"
CORNER_SCHEMA = SCHEMA + ".source-corner-owner-incidence"
PARENT_SCHEMA = SCHEMA + ".representative-parent-conservation"
CENSUS_SCHEMA = SCHEMA + ".round144-census"

TARGET_PAIRS = (97, 211, 592, 664, 715)
EXPECTED_ELIGIBLE = (592, 715)
EXPECTED_BLOCKED = (97, 211, 664)
INSTALLED_C42_PAIR = 391
SOURCE_FRACTION = Q(1, 512)
MAX_OPERATIONAL_DEPTH = 32
MAX_OPERATIONAL_ROUTES_PER_PAIR = 8191
EXPECTED_PROFILES = {
    97: (3, 2, 2),
    211: (3, 2, 2),
    592: (2, 1, 1),
    664: (4, 3, 3),
    715: (2, 1, 1),
}
EXPECTED_LEAF_CLASS = {
    97: "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
    211: "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
    592: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
    664: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
    715: "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
}

EXPECTED_PLANNER_SOURCE = (
    "a7c22208b859979ee4cc9ccd460865d0fee517d2348ca3d59322cc5da90f0522"
)
EXPECTED_PILOT_SOURCE = (
    "00c03e5a9f869a917649d49137f2aece69357e0e9a073e59f9e2d990b0365609"
)
EXPECTED_C40_SOURCE = (
    "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57"
)
EXPECTED_C40_AUDITOR_SOURCE = (
    "1cccec33cf7768b5797ca0b05f74812a300fb4b323859a10e9495f3e73d8a0be"
)
EXPECTED_C41_SOURCE = pilot.EXPECTED_C41_SOURCE_SHA256
EXPECTED_C41_AUDITOR_SOURCE = (
    "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c"
)
EXPECTED_C42_PRODUCER_SOURCE = (
    "4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78"
)
EXPECTED_C42_AUDITOR_SOURCE = (
    "6da5c8a3f2960ec9f763e314be01e909722b6b03bcd2817e5030295dcd6086eb"
)
EXPECTED_C42_INSTALLER_SOURCE = (
    "66f88bc5913af695691c5ae58be7938f94f3f68a9eeeeed32bcd96b37938c276"
)
EXPECTED_C42_TX_AUDITOR_SOURCE = (
    "a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2"
)
EXPECTED_C40_MANIFEST = (
    "4c1b1786d1d724c2c43a9115e4a564b16b61445712b341ff027b8da24f55651d"
)
EXPECTED_C41_MANIFEST = (
    "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
)
EXPECTED_C42_MANIFEST = (
    "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058"
)

C40_TOKEN = "c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C40_DIR = CANDIDATE_ROOT / C40_TOKEN
C41_DIR = pilot.C41_DIR
C42_DIR = pilot.C42_DIR
C42_AUDIT_PATH = (
    AUDIT_ROOT / pilot.C42_AUDIT_TOKEN / "independent_audit.json"
)
C42_RECEIPT_PATH = pilot.C42_RECEIPT

INVENTORY = (
    "C43_SUBSET_CLOSURE.lock",
    "adaptive_splits.jsonl.gz",
    "closed_leaf_certificates.jsonl.gz",
    "exact_sources.jsonl.gz",
    "internal_strata_incidence.jsonl.gz",
    "reflection_transport.jsonl.gz",
    "representative_parent_conservation.jsonl.gz",
    "result.json",
    "root_manifest.sha256",
    "round144_census.json",
    "source_corner_owner_incidence.jsonl.gz",
    "source_face_owner_incidence.jsonl.gz",
    "source_preflight.jsonl.gz",
)

EXTRA_PINNED_FILES = {
    "planner_source": (
        "deliverables/cm2_round306c43b0_d02_zero_surface_shard_planner_v1.py",
        EXPECTED_PLANNER_SOURCE,
    ),
    "pilot_source": (
        "deliverables/cm2_round306c43b0_d02_sole_deficit_adaptive_pilot_v1.py",
        EXPECTED_PILOT_SOURCE,
    ),
    "C40_source": (
        "deliverables/cm2_round306c40_d02_h1_endpoint_collision2_arrangement_v1.py",
        EXPECTED_C40_SOURCE,
    ),
    "C40_auditor_source": (
        "deliverables/cm2_round306c40_d02_h1_endpoint_collision2_arrangement_independent_auditor_v1.py",
        EXPECTED_C40_AUDITOR_SOURCE,
    ),
    "C41_auditor_source": (
        "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1.py",
        EXPECTED_C41_AUDITOR_SOURCE,
    ),
    "C42_producer_source": (
        "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1.py",
        EXPECTED_C42_PRODUCER_SOURCE,
    ),
    "C42_auditor_source": (
        "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_independent_auditor_v1.py",
        EXPECTED_C42_AUDITOR_SOURCE,
    ),
    "C42_installer_source": (
        "deliverables/cm2_round306c42_f1_authority_transaction_installer_v1.py",
        EXPECTED_C42_INSTALLER_SOURCE,
    ),
    "C40_manifest": (
        f".cm2-runtime/candidates/{C40_TOKEN}/root_manifest.sha256",
        EXPECTED_C40_MANIFEST,
    ),
    "C42_manifest": (
        f".cm2-runtime/candidates/{pilot.C42_TOKEN}/root_manifest.sha256",
        EXPECTED_C42_MANIFEST,
    ),
}


class C43Error(RuntimeError):
    """Fail-closed C43 producer error."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise C43Error(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def qstr(value: Any) -> str:
    value = Q(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def box_payload(box: Any) -> dict[str, list[str]]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def box_from_payload(value: dict[str, Any], label: str = "") -> Any:
    atlas_box = c41.c38.round166.ge.AtlasBox
    return atlas_box(
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
        Q(value["s"][0]), Q(value["s"][1]), 0, label,
    )


def exact_payload(value: Any) -> Any:
    if isinstance(value, arb):
        return c41.c39.arb_payload(value)
    if isinstance(value, (Q, fmpq)):
        return qstr(value)
    if value is None or type(value) in {str, int, bool}:
        return value
    if isinstance(value, dict):
        return {str(key): exact_payload(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_payload(item) for item in value]
    raise C43Error("unsupported exact payload type:" + type(value).__name__)


def record_payload(record: Any) -> dict[str, Any]:
    return {
        "target_id": record.target_id,
        "classification": record.classification,
        "ell": exact_payload(record.ell),
        "discriminant": exact_payload(record.discriminant),
        "near": exact_payload(record.near),
        "far": exact_payload(record.far),
        "transverse": exact_payload(record.transverse),
    }


def stat_fingerprint(path: Path) -> list[int]:
    value = os.stat(path, follow_symlinks=False)
    return [
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
        value.st_uid, value.st_gid,
    ]


def no_c43_authority_pointers() -> None:
    for name in (
        "c43-current-token",
        "c43-current-audit-token",
        "c43-current-authority-seal",
    ):
        require(not (RUNTIME / name).exists(), "C43 pointer must not exist:" + name)


def capture_inputs() -> dict[str, pilot.Capture]:
    captures: dict[str, pilot.Capture] = {
        "self": pilot.Capture(SELF, None, "C43 producer source", 8 << 20)
    }
    merged = dict(pilot.PINNED_FILES)
    merged.update(EXTRA_PINNED_FILES)
    for label, (relative, expected) in merged.items():
        if label in captures:
            continue
        captures[label] = pilot.Capture(
            ROOT / relative, expected, "C43 input " + label
        )
    return captures


def close_captures(captures: dict[str, pilot.Capture]) -> None:
    for capture in reversed(list(captures.values())):
        capture.close()


def validate_installed_c42() -> dict[str, Any]:
    value = c42tx.audit_installed(EXPECTED_C42_TX_AUDITOR_SOURCE)
    require(
        value["authority_installed"] is True
        and value["candidate_object_sha256"] == pilot.EXPECTED_C42_OBJECT
        and value["independent_audit_object_sha256"]
        == pilot.EXPECTED_C42_AUDIT_OBJECT
        and value["authority_seal_object_sha256"]
        == pilot.EXPECTED_C42_SEAL_OBJECT
        and value["installation_receipt_object_sha256"]
        == pilot.EXPECTED_C42_RECEIPT_OBJECT,
        "installed C42 f1 authority transaction",
    )
    return value


def load_inputs() -> dict[str, Any]:
    installed = validate_installed_c42()
    c41.validate_manifest(C41_DIR)
    c41_result = c41.strict_json(C41_DIR / "result.json")
    c41.validate_object(c41_result, pilot.EXPECTED_C41_OBJECT, "C41")
    c41.validate_manifest(C42_DIR)
    c42_result = c41.strict_json(C42_DIR / "result.json")
    c41.validate_object(c42_result, pilot.EXPECTED_C42_OBJECT, "C42")

    inventory, planner_tasks = planner.build_inventory(C41_DIR)
    sole = [
        row for row in planner_tasks
        if row["b0_closure_would_make_whole_pair"]
        and row["pair_b0_task_count"] == 1
        and not row["already_closed_by_C42"]
    ]
    require(
        [row["pair_index"] for row in sole] == list(TARGET_PAIRS),
        "derived post-C42 five sole-deficit tranche",
    )
    planner_by_pair = {row["pair_index"]: row for row in sole}

    c41_rows, c42_parents = pilot.validate_target_rows(c41_result, c42_result)
    for pair in TARGET_PAIRS:
        expected = pilot.EXPECTED_TARGETS[pair]
        planned = planner_by_pair[pair]
        require(
            planned["source_ambient_id"]
            == c41_rows[pair]["c41_ambient_cell_id"]
            and planned["source_ambient_row_sha256"]
            == expected["c41_ambient_row_sha256"]
            and planned["descendant_path"] == expected["descendant_path"]
            and planned["source_parent_volume_fraction"] == "1/512",
            "planner/C41 target binding:" + str(pair),
        )

    c40_dir = (ROOT / c41_result["C40_authority"]["path"]).resolve()
    c40_audit = (
        ROOT / c41_result["C40_authority"]["independent_audit_path"]
    ).resolve()
    require(c40_dir == C40_DIR.resolve(), "pinned C40 authority path")
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    context["_C43B0_C40_directory"] = c40_dir
    tasks = pilot.load_c40_tasks(context, c41_rows)

    c41.ctx.prec = c41.PRECISION_BITS
    generated = c41.install_complete_immutable_cache()
    require(
        sum(len(rows) for rows in generated.values()) == 448,
        "complete immutable candidate cache",
    )
    config = c41.decode_worker_config(context["config"])

    ambient_rows = list(c41.iter_ledger(
        C41_DIR, c41_result["ledgers"]["routed_ambient_cells"]
    ))
    require(len(ambient_rows) == 91_879, "C41 ambient census")
    ambient_by_id = {
        row["c41_ambient_cell_id"]: row for row in ambient_rows
    }
    require(len(ambient_by_id) == len(ambient_rows), "ambient id uniqueness")

    boundary_by_pair: dict[int, dict[str, Any]] = {}
    for row in c41.iter_ledger(
        C41_DIR, c41_result["ledgers"]["boundary_corner_outers"]
    ):
        pair = row["pair_index"]
        if pair in TARGET_PAIRS and row["descendant_path"] == c41_rows[pair]["path"]:
            require(pair not in boundary_by_pair, "unique target boundary:" + str(pair))
            boundary_by_pair[pair] = row
    require(set(boundary_by_pair) == set(TARGET_PAIRS), "five target boundaries")

    c42_parent_rows = list(c41.iter_ledger(
        C42_DIR, c42_result["ledgers"]["parent_conservation"]
    ))
    require(
        len(c42_parent_rows) == 862
        and {row["pair_index"] for row in c42_parent_rows} == set(range(862)),
        "C42 862 parent baseline",
    )
    c42_source = next(c41.iter_ledger(
        C42_DIR, c42_result["ledgers"]["exact_source"]
    ))

    return {
        "installed": installed,
        "C41_result": c41_result,
        "C42_result": c42_result,
        "planner_inventory": inventory,
        "planner_by_pair": planner_by_pair,
        "C41_rows": c41_rows,
        "C42_target_parents": c42_parents,
        "C42_parent_rows": c42_parent_rows,
        "C42_source": c42_source,
        "context": context,
        "config": config,
        "tasks": tasks,
        "ambient_rows": ambient_rows,
        "ambient_by_id": ambient_by_id,
        "boundary_by_pair": boundary_by_pair,
    }


def route_semantic(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "closed_box": box_payload(route["box"]),
        "classification": route["classification"],
        "witness": route["witness"],
        "route_method": route["route_method"],
        "c1_result": route["c1_result"],
        "c2_status": route["c2_status"],
        "c2_baseline": route["c2_baseline"],
        "c2_detail": route["c2_detail"],
        "c2_evidence": route["c2_evidence"],
        "route_failure": route["route_failure"],
    }


def adaptive_tree(task: dict[str, Any], start_path: str,
                  config: dict[str, Any]) -> dict[str, Any]:
    initial = c41.route_at_path(task, start_path, config)
    stack: list[tuple[str, int, Q, dict[str, Any]]] = [
        (start_path, 0, Q(1), initial)
    ]
    leaves: list[dict[str, Any]] = []
    splits: list[dict[str, Any]] = []
    route_count = 1
    while stack:
        path, depth, relative_fraction, route = stack.pop()
        family = c41.disposition_family(route["classification"])
        if family == "TERMINAL_EXCLUDED":
            leaves.append({
                "path": path,
                "additional_depth": depth,
                "relative_fraction": relative_fraction,
                "route": route,
            })
            continue
        require(
            family != "COLLISION3_READY",
            "sole-deficit formal tranche cannot hand off collision3:" + path,
        )
        require(
            depth < MAX_OPERATIONAL_DEPTH
            and route_count + 2 <= MAX_OPERATIONAL_ROUTES_PER_PAIR,
            "adaptive operational budget exhausted before semantic terminal:" + path,
        )
        parent_box = route["box"]
        axis = c41.c38.round166.longest_axis(parent_box)
        require(axis in {0, 1}, "s=0 split axis")
        children = c41.c38.round166.split_axis(parent_box, axis)
        child_routes = []
        for bit in ("0", "1"):
            child_path = path + bit
            child_route = c41.route_at_path(task, child_path, config)
            require(
                box_payload(child_route["box"])
                == box_payload(children[int(bit)]),
                "route child equals exact rational split",
            )
            child_routes.append(child_route)
        route_count += 2
        axis_name = ("t", "p")[axis]
        lower = (parent_box.t0, parent_box.p0)[axis]
        upper = (parent_box.t1, parent_box.p1)[axis]
        splits.append({
            "parent_path": path,
            "additional_depth_before_split": depth,
            "relative_parent_fraction": relative_fraction,
            "parent_box": parent_box,
            "axis": axis,
            "axis_name": axis_name,
            "midpoint": (lower + upper) / 2,
            "children": children,
            "child_paths": (path + "0", path + "1"),
            "child_route_hashes": (
                digest(route_semantic(child_routes[0])),
                digest(route_semantic(child_routes[1])),
            ),
        })
        for bit in ("1", "0"):
            stack.append((
                path + bit, depth + 1, relative_fraction / 2,
                child_routes[int(bit)],
            ))
    leaves.sort(key=lambda row: row["path"])
    splits.sort(key=lambda row: row["parent_path"])
    paths = [row["path"] for row in leaves]
    require(
        len(paths) == len(set(paths))
        and not any(
            right.startswith(left)
            for left in paths for right in paths if left != right
        )
        and sum(row["relative_fraction"] for row in leaves) == 1,
        "adaptive prefix-free Kraft cover",
    )
    return {
        "leaves": leaves,
        "splits": splits,
        "route_count": route_count,
        "deepest": max(row["additional_depth"] for row in leaves),
    }


def reflected_path_and_box(task: dict[str, Any], path: str,
                           cells: dict[str, dict[str, Any]]) \
        -> tuple[str, Any, Any]:
    representative = task["cell"]
    reflected = cells[task["c38_source"]["reflected_cell_id"]]
    rep_box, _ = c41.c39.reconstruct_box(representative, "")
    ref_box, _ = c41.c39.reconstruct_box(reflected, "")
    chart = representative["gate3_chart"].split(":")[1]
    reflected_path = ""
    for bit in path:
        rep_axis = c41.c38.round166.longest_axis(rep_box)
        ref_axis = c41.c38.round166.longest_axis(ref_box)
        require(rep_axis == ref_axis, "reflection split-axis equality")
        reversed_axis = (
            rep_axis == 1 or (rep_axis == 0 and chart in {"E", "W"})
        )
        reflected_bit = str(1 - int(bit)) if reversed_axis else bit
        rep_box = c41.c38.round166.split_axis(rep_box, rep_axis)[int(bit)]
        ref_box = c41.c38.round166.split_axis(ref_box, ref_axis)[
            int(reflected_bit)
        ]
        reflected_path += reflected_bit
    expected = c41.c40.reflected_payload(chart, rep_box)
    require(
        box_payload(ref_box)["t"] == expected["t"]
        and box_payload(ref_box)["p"] == expected["p"],
        "exact Jy reflected endpoint order",
    )
    return reflected_path, rep_box, ref_box


def make_reflected_task(task: dict[str, Any],
                        cells: dict[str, dict[str, Any]]) -> dict[str, Any]:
    value = copy.deepcopy(task)
    source = value["c38_source"]
    source["representative_origin_key"], source["reflected_origin_key"] = (
        source["reflected_origin_key"], source["representative_origin_key"]
    )
    source["representative_cell_id"], source["reflected_cell_id"] = (
        source["reflected_cell_id"], source["representative_cell_id"]
    )
    value["cell"] = cells[source["representative_cell_id"]]
    return value


def cell_for_box(cell: dict[str, Any], box: Any) -> dict[str, Any]:
    value = copy.deepcopy(cell)
    value["physical_t_interval"] = [
        {"kind": "RATIONAL", "value": qstr(box.t0)},
        {"kind": "RATIONAL", "value": qstr(box.t1)},
    ]
    value["physical_p_interval"] = [qstr(box.p0), qstr(box.p1)]
    return value


def c1_closed_box_certificate(
    pair: int,
    orientation: str,
    path: str,
    origin_key: str,
    cell: dict[str, Any],
    box: Any,
    config: dict[str, Any],
    scope: str,
    *,
    terminal_credit: int,
) -> dict[str, Any]:
    route_task = {
        "task_id": f"c43-direct:{pair}:{orientation}:{path}:{scope}",
        "kind": "C1",
        "row": {"path": "", "representative_origin_key": origin_key},
        "cell": cell_for_box(cell, box),
    }
    routed = c41.c39.route_c1_task(route_task, config)
    require(
        routed["classification"]
        == "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH",
        "direct closed-box strict C1 word mismatch:"
        + str(pair) + ":" + orientation + ":" + path + ":" + scope,
    )

    active = tuple(cell["source_lineage"]["active_candidates"])
    stage_one, raw_records = c41.c38.round166.classify_active(
        cell["gate3_chart"], box, active
    )
    enhanced_records = []
    enhancement_evidence = []
    for record in raw_records:
        replacement, evidence = c41.c39.enhanced_record(
            origin_key, box, record
        )
        enhanced_records.append(replacement)
        if evidence is not None:
            enhancement_evidence.append(evidence)
    enhanced_leaf = c41.c38.round166.classify_from_records(
        cell["gate3_chart"], box, enhanced_records
    )
    require(
        enhanced_leaf.classification == "unique_first"
        and enhanced_leaf.owner_target == c41.c39.FROZEN_OWNER
        and all(
            record.classification not in {
                "unresolved_discriminant", "unresolved_root_sign"
            }
            for record in enhanced_records
        ),
        "strict collision-one owner on entire closed box",
    )
    h1 = c41.c39.h1_route(origin_key, box)
    require(
        h1["kind"] == "STRICT_SIDE"
        and h1["chart"] == "W"
        and h1["H1_centered"]["sign"] != "UNRESOLVED",
        "strict H1 W side on entire closed box",
    )

    chart_id = ":".join(origin_key.split(":")[:2])
    owner = c41.c38.first_owner(chart_id, box)
    require(
        owner is not None
        and owner["selected_target_id"] == c41.c39.FROZEN_OWNER,
        "materialized strict first owner",
    )
    lower = c41.c38.round139.lower
    core_index = c41.c38.CORE_INDEX[chart_id]
    atom = lower.step1.Atom(
        core_index, config["cores"][core_index],
        box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "c43",
    )
    initial_state = lower.round136.initial_state(atom)
    outgoing_state = lower.time3.second_outgoing_state(
        atom, initial_state, owner
    )
    require(
        outgoing_state is not None and outgoing_state["chart"] == "W",
        "defined collision-one outgoing state",
    )
    word, word_error = lower.round136.translation_normalized_official_word(
        initial_state,
        "W[0,0]",
        owner,
        config["pair_index"],
        config["pattern_index"],
    )
    require(word is not None and word_error is None, "defined official word")
    compact = lower.round136.compact_key(word["key"])
    expected = config["original_path"][0]
    require(
        compact["official_word_key_id"] != expected["official_word_key_id"],
        "literal official-word key inequality",
    )
    record_rows = [record_payload(item) for item in enhanced_records]
    record_census = dict(sorted(Counter(
        item["classification"] for item in record_rows
    ).items()))
    semantic = {
        "schema": LEAF_SCHEMA + ".direct-restriction",
        "pair_index": pair,
        "orientation": orientation,
        "path": path,
        "scope": scope,
        "parent_key": origin_key,
        "cell_id": cell["cell_id"],
        "closed_box": box_payload(box),
        "closed_box_scope": "ENTIRE_CLOSED_RATIONAL_BOX_INCLUDING_ALL_FACES",
        "active_target_universe": list(active),
        "input_stage_one_classification": stage_one.classification,
        "enhanced_stage_one_classification": enhanced_leaf.classification,
        "enhanced_unique_owner": enhanced_leaf.owner_target,
        "ordered_collision1_candidate_records": record_rows,
        "collision1_candidate_record_census": record_census,
        "enhancement_evidence": enhancement_evidence,
        "H1_closed_box_evidence": h1,
        "strict_first_owner": exact_payload(owner),
        "initial_state": exact_payload(initial_state),
        "outgoing_state": exact_payload(outgoing_state),
        "official_word": word,
        "official_word_compact_key": compact,
        "expected_lineage_word": expected,
        "official_word_key_inequality": {
            "calculated": compact["official_word_key_id"],
            "expected": expected["official_word_key_id"],
            "operands_are_distinct": True,
        },
        "endpoint_phase": c41.c40.endpoint_phase(box),
        "homogeneity": {
            "s_interval": [qstr(box.s0), qstr(box.s1)],
            "s_is_exactly_zero": box.s0 == box.s1 == 0,
            "physical_core_index": core_index,
        },
        "route_result": routed,
        "strict_disposition": routed["classification"],
        "strict_terminal_on_entire_closed_box": True,
        "local_round144_terminal_credit": terminal_credit,
        "lower_dimensional_ambient_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["certificate_id"] = "c43-cert:" + digest(semantic)
    return semantic


def make_face_box(box: Any, face: str, lo: Q | None = None,
                  hi: Q | None = None) -> Any:
    atlas_box = type(box)
    t0, t1, p0, p1 = box.t0, box.t1, box.p0, box.p1
    if face == "t_lower":
        t1 = t0
        if lo is not None:
            p0, p1 = lo, hi
    elif face == "t_upper":
        t0 = t1
        if lo is not None:
            p0, p1 = lo, hi
    elif face == "p_lower":
        p1 = p0
        if lo is not None:
            t0, t1 = lo, hi
    elif face == "p_upper":
        p0 = p1
        if lo is not None:
            t0, t1 = lo, hi
    else:
        raise C43Error("unknown face:" + face)
    return atlas_box(t0, t1, p0, p1, box.s0, box.s1, 0, face)


def make_point_box(box: Any, corner: str) -> Any:
    atlas_box = type(box)
    t = box.t0 if corner.startswith("t0") else box.t1
    p = box.p0 if corner.endswith("p0") else box.p1
    return atlas_box(t, t, p, p, box.s0, box.s1, 0, corner)


def parsed_box(row: dict[str, Any], orientation: str) \
        -> tuple[Q, Q, Q, Q] | None:
    field = (
        "closed_representative_box"
        if orientation == "REPRESENTATIVE"
        else "closed_reflected_box"
    )
    value = row[field]
    if value is None:
        return None
    return (
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
    )


def owner_key(row: dict[str, Any]) -> tuple[str, int, str]:
    return row["path"], row["pair_index"], row["c41_ambient_cell_id"]


def effective_incident(row: dict[str, Any], terminal_ids: set[str]) \
        -> dict[str, Any]:
    terminal = (
        row["disposition_family"] == "TERMINAL_EXCLUDED"
        or row["c41_ambient_cell_id"] in terminal_ids
    )
    return {
        "pair_index": row["pair_index"],
        "path": row["path"],
        "representative_cell_id": row["representative_cell_id"],
        "reflected_cell_id": row["reflected_cell_id"],
        "c41_ambient_cell_id": row["c41_ambient_cell_id"],
        "c41_row_sha256": row["row_sha256"],
        "C41_disposition_family": row["disposition_family"],
        "terminal_after_C43_subset": terminal,
    }


def point_incidents(ambient_geometry: list[tuple[dict[str, Any], Any, Any]],
                    orientation: str, t: Q, p: Q,
                    terminal_ids: set[str]) -> list[dict[str, Any]]:
    index = 1 if orientation == "REPRESENTATIVE" else 2
    rows = []
    for item in ambient_geometry:
        box = item[index]
        if box is not None and box[0] <= t <= box[1] and box[2] <= p <= box[3]:
            rows.append(effective_incident(item[0], terminal_ids))
    rows.sort(key=owner_key)
    require(bool(rows), "nonempty global point incidence")
    return rows


def face_partition(
    ambient_geometry: list[tuple[dict[str, Any], Any, Any]],
    orientation: str,
    box: Any,
    face: str,
    terminal_ids: set[str],
) -> dict[str, Any]:
    index = 1 if orientation == "REPRESENTATIVE" else 2
    if face.startswith("t_"):
        fixed = box.t0 if face == "t_lower" else box.t1
        lo, hi = box.p0, box.p1
        transverse = 0
    else:
        fixed = box.p0 if face == "p_lower" else box.p1
        lo, hi = box.t0, box.t1
        transverse = 1
    candidates = []
    points = {lo, hi}
    for row, rep, ref in ambient_geometry:
        value = rep if index == 1 else ref
        if value is None:
            continue
        t0, t1, p0, p1 = value
        contains_fixed = (
            t0 <= fixed <= t1 if transverse == 0 else p0 <= fixed <= p1
        )
        along0, along1 = (
            (p0, p1) if transverse == 0 else (t0, t1)
        )
        if contains_fixed and max(lo, along0) <= min(hi, along1):
            candidates.append((row, value))
            points.add(max(lo, along0))
            points.add(min(hi, along1))
    ordered = sorted(points)
    require(
        ordered[0] == lo and ordered[-1] == hi
        and all(left < right for left, right in zip(ordered, ordered[1:])),
        "exact face breakpoint partition",
    )
    segments = []
    for left, right in zip(ordered, ordered[1:]):
        middle = (left + right) / 2
        incident = []
        for row, value in candidates:
            along0, along1 = (
                (value[2], value[3]) if transverse == 0
                else (value[0], value[1])
            )
            if along0 <= middle <= along1:
                incident.append(effective_incident(row, terminal_ids))
        incident.sort(key=owner_key)
        require(bool(incident), "nonempty open-face segment incidence")
        segments.append({
            "interval": [qstr(left), qstr(right)],
            "midpoint": qstr(middle),
            "incident_ambient_cells": incident,
            "canonical_owner": incident[0],
            "canonical_owner_terminal_after_C43_subset": incident[0][
                "terminal_after_C43_subset"
            ],
        })
    interior_points = []
    for point in ordered[1:-1]:
        t, p = (
            (fixed, point) if transverse == 0 else (point, fixed)
        )
        incident = point_incidents(
            ambient_geometry, orientation, t, p, terminal_ids
        )
        interior_points.append({
            "coordinate": {"t": qstr(t), "p": qstr(p), "s": "0"},
            "incident_ambient_cells": incident,
            "canonical_owner": incident[0],
            "canonical_owner_terminal_after_C43_subset": incident[0][
                "terminal_after_C43_subset"
            ],
        })
    return {
        "fixed_coordinate": qstr(fixed),
        "longitudinal_interval": [qstr(lo), qstr(hi)],
        "breakpoint_count": len(ordered),
        "breakpoints": [qstr(value) for value in ordered],
        "segments": segments,
        "interior_breakpoints": interior_points,
        "global_candidate_incident_count": len(candidates),
        "global_incident_census_complete": True,
        "all_required_segment_and_breakpoint_owners_terminal": (
            all(row["canonical_owner_terminal_after_C43_subset"]
                for row in segments)
            and all(row["canonical_owner_terminal_after_C43_subset"]
                    for row in interior_points)
        ),
    }


def target_orientation(
    pair: int,
    orientation: str,
    task: dict[str, Any],
    source_row: dict[str, Any],
    context: dict[str, Any],
) -> tuple[str, dict[str, Any], Any, str]:
    if orientation == "REPRESENTATIVE":
        return (
            task["c38_source"]["representative_origin_key"],
            task["cell"],
            box_from_payload(source_row["closed_representative_box"], "rep"),
            source_row["path"],
        )
    reflected = make_reflected_task(task, context["context"]["cells"])
    reflected_path, _rep, ref_box = reflected_path_and_box(
        task, source_row["path"], context["context"]["cells"]
    )
    return (
        reflected["c38_source"]["representative_origin_key"],
        reflected["cell"],
        ref_box,
        reflected_path,
    )


def build_boundary_preflight(context: dict[str, Any],
                             provisional_terminal_ids: set[str]) \
        -> tuple[dict[int, dict[str, Any]], list[tuple[Any, Any, Any]]]:
    geometry = [
        (
            row,
            parsed_box(row, "REPRESENTATIVE"),
            parsed_box(row, "REFLECTED"),
        )
        for row in context["ambient_rows"]
    ]
    rows: dict[int, dict[str, Any]] = {}
    for pair in TARGET_PAIRS:
        source = context["C41_rows"][pair]
        task = context["tasks"][pair]
        face_obligations = []
        corner_obligations = []
        blockers = []
        for orientation in ("REPRESENTATIVE", "REFLECTED"):
            _origin, _cell, box, path = target_orientation(
                pair, orientation, task, source, context
            )
            for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
                partition = face_partition(
                    geometry, orientation, box, face,
                    provisional_terminal_ids,
                )
                obligation = {
                    "orientation": orientation,
                    "face": face,
                    "target_path": path,
                    "partition": partition,
                }
                face_obligations.append(obligation)
                for segment in partition["segments"]:
                    if not segment[
                        "canonical_owner_terminal_after_C43_subset"
                    ]:
                        blockers.append({
                            "orientation": orientation,
                            "stratum": "FACE_SEGMENT",
                            "face_or_corner": face,
                            "exact_key": segment["interval"],
                            "canonical_owner": segment["canonical_owner"],
                        })
                for point in partition["interior_breakpoints"]:
                    if not point[
                        "canonical_owner_terminal_after_C43_subset"
                    ]:
                        blockers.append({
                            "orientation": orientation,
                            "stratum": "FACE_BREAKPOINT",
                            "face_or_corner": face,
                            "exact_key": point["coordinate"],
                            "canonical_owner": point["canonical_owner"],
                        })
            for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
                point = make_point_box(box, corner)
                incidents = point_incidents(
                    geometry, orientation, point.t0, point.p0,
                    provisional_terminal_ids,
                )
                obligation = {
                    "orientation": orientation,
                    "corner": corner,
                    "target_path": path,
                    "coordinate": {
                        "t": qstr(point.t0), "p": qstr(point.p0), "s": "0"
                    },
                    "incident_ambient_cells": incidents,
                    "canonical_owner": incidents[0],
                    "canonical_owner_terminal_after_C43_subset": incidents[0][
                        "terminal_after_C43_subset"
                    ],
                }
                corner_obligations.append(obligation)
                if not obligation[
                    "canonical_owner_terminal_after_C43_subset"
                ]:
                    blockers.append({
                        "orientation": orientation,
                        "stratum": "SOURCE_CORNER",
                        "face_or_corner": corner,
                        "exact_key": obligation["coordinate"],
                        "canonical_owner": incidents[0],
                    })
        rows[pair] = {
            "pair_index": pair,
            "face_obligations": face_obligations,
            "corner_obligations": corner_obligations,
            "canonical_residual_owner_blockers": blockers,
            "canonical_residual_owner_blocker_count": len(blockers),
            "boundary_owner_eligible": len(blockers) == 0,
        }
    return rows, geometry


def source_preflight_rows(context: dict[str, Any],
                          trees: dict[int, dict[str, Any]],
                          boundary: dict[int, dict[str, Any]]) \
        -> list[dict[str, Any]]:
    rows = []
    for pair in TARGET_PAIRS:
        tree = trees[pair]
        profile = EXPECTED_PROFILES[pair]
        require(
            len(tree["leaves"]) == profile[0]
            and len(tree["splits"]) == profile[1]
            and tree["deepest"] == profile[2]
            and all(
                leaf["route"]["classification"] == EXPECTED_LEAF_CLASS[pair]
                for leaf in tree["leaves"]
            ),
            "fresh adaptive profile:" + str(pair),
        )
        expected = pilot.EXPECTED_TARGETS[pair]
        source = context["C41_rows"][pair]
        row = {
            "schema": SOURCE_PREFLIGHT_SCHEMA,
            "pair_index": pair,
            "derived_from_planner": True,
            "planner_task_id": context["planner_by_pair"][pair]["task_id"],
            "C41_ambient_cell_id": source["c41_ambient_cell_id"],
            "C41_ambient_row_sha256": source["row_sha256"],
            "C42_parent_row_sha256":
                context["C42_target_parents"][pair]["row_sha256"],
            "descendant_path": source["path"],
            "source_fraction": source["parent_volume_fraction"],
            "fresh_route_count": tree["route_count"],
            "fresh_split_count": len(tree["splits"]),
            "fresh_terminal_leaf_count": len(tree["leaves"]),
            "fresh_deepest_additional_depth": tree["deepest"],
            "fresh_leaf_path_sequence": [
                leaf["path"] for leaf in tree["leaves"]
            ],
            "fresh_leaf_classification_census": dict(sorted(Counter(
                leaf["route"]["classification"] for leaf in tree["leaves"]
            ).items())),
            "relative_Kraft_sum": qstr(sum(
                leaf["relative_fraction"] for leaf in tree["leaves"]
            )),
            "canonical_residual_owner_blocker_count":
                boundary[pair]["canonical_residual_owner_blocker_count"],
            "canonical_residual_owner_blockers":
                boundary[pair]["canonical_residual_owner_blockers"],
            "eligible_for_C43_credit":
                boundary[pair]["boundary_owner_eligible"],
            "expected_regression_guard": expected,
            "local_round144_terminal_credit": (
                1 if boundary[pair]["boundary_owner_eligible"] else 0
            ),
            "blocked_input_credit": 0,
            "lower_dimensional_ambient_credit": 0,
            "D02_gate_credit": 0,
        }
        row["source_preflight_id"] = "c43-preflight:" + digest(row)
        rows.append(row)
    return rows


def exact_source_rows(context: dict[str, Any],
                      preflight: dict[int, dict[str, Any]]) \
        -> list[dict[str, Any]]:
    rows = []
    for pair in EXPECTED_ELIGIBLE:
        source = context["C41_rows"][pair]
        task = context["tasks"][pair]
        boundary = context["boundary_by_pair"][pair]
        planned = context["planner_by_pair"][pair]
        require(
            boundary["owning_outer_id"] == planned["source_outer_id"]
            and boundary["exact_face_row_count"] == 4
            and boundary["exact_corner_row_count"] == 4,
            "eligible C41 outer/boundary binding:" + str(pair),
        )
        row = {
            "schema": SOURCE_SCHEMA,
            "pair_index": pair,
            "installed_C42_candidate_object_sha256":
                pilot.EXPECTED_C42_OBJECT,
            "installed_C42_audit_object_sha256":
                pilot.EXPECTED_C42_AUDIT_OBJECT,
            "installed_C42_seal_object_sha256":
                pilot.EXPECTED_C42_SEAL_OBJECT,
            "installed_C42_receipt_object_sha256":
                pilot.EXPECTED_C42_RECEIPT_OBJECT,
            "C42_candidate_path": str(C42_DIR.relative_to(ROOT)),
            "C42_parent_row_sha256":
                context["C42_target_parents"][pair]["row_sha256"],
            "C41_candidate_object_sha256": pilot.EXPECTED_C41_OBJECT,
            "C41_root_manifest_sha256": EXPECTED_C41_MANIFEST,
            "C41_ambient_cell_id": source["c41_ambient_cell_id"],
            "C41_ambient_row_sha256": source["row_sha256"],
            "C41_primary_outer_id": planned["source_outer_id"],
            "C41_primary_outer_row_sha256":
                planned["source_outer_row_sha256"],
            "C41_boundary_outer_id": boundary["boundary_corner_outer_id"],
            "C41_boundary_outer_row_sha256": boundary["row_sha256"],
            "C40_source_leaf_id": source["c40_source_leaf_id"],
            "C40_source_row_sha256": source["c40_source_row_sha256"],
            "C38_source_row_sha256": task["source"]["c38_source_row_sha256"],
            "representative_origin_key":
                task["c38_source"]["representative_origin_key"],
            "reflected_origin_key":
                task["c38_source"]["reflected_origin_key"],
            "representative_cell_id": source["representative_cell_id"],
            "reflected_cell_id": source["reflected_cell_id"],
            "descendant_path": source["path"],
            "closed_representative_box": source["closed_representative_box"],
            "closed_reflected_box": source["closed_reflected_box"],
            "source_fraction": source["parent_volume_fraction"],
            "source_residual_classification":
                source["residual_classification"],
            "preflight_row_sha256": preflight[pair]["row_sha256"],
            "unique_post_C42_residual_descendant": True,
            "boundary_owner_eligible": True,
            "source_binding_complete": True,
            "producer_output_is_authority": False,
            "D02_gate_credit": 0,
        }
        row["exact_source_id"] = "c43-source:" + digest(row)
        rows.append(row)
    return rows


def split_rows(trees: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for pair in EXPECTED_ELIGIBLE:
        start = pilot.EXPECTED_TARGETS[pair]["descendant_path"]
        for split in trees[pair]["splits"]:
            row = {
                "schema": SPLIT_SCHEMA,
                "pair_index": pair,
                "source_descendant_path": start,
                "parent_path": split["parent_path"],
                "additional_depth_before_split":
                    split["additional_depth_before_split"],
                "relative_parent_fraction":
                    qstr(split["relative_parent_fraction"]),
                "absolute_parent_fraction": qstr(
                    SOURCE_FRACTION * split["relative_parent_fraction"]
                ),
                "longest_axis_rule": "ROUND166_PINNED_LONGEST_AXIS_TIE_ORDER",
                "split_axis": split["axis_name"],
                "exact_split_midpoint": qstr(split["midpoint"]),
                "parent_closed_box": box_payload(split["parent_box"]),
                "lower_child_path": split["child_paths"][0],
                "upper_child_path": split["child_paths"][1],
                "lower_child_closed_box": box_payload(split["children"][0]),
                "upper_child_closed_box": box_payload(split["children"][1]),
                "child_route_semantic_sha256":
                    list(split["child_route_hashes"]),
                "lower_child_fraction_multiplier": "1/2",
                "upper_child_fraction_multiplier": "1/2",
                "exact_fraction_conservation": "1",
                "closed_cover_equality": True,
                "half_open_shared_face_owner": "LOWER_BIT_CHILD",
                "ambient_or_whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            row["adaptive_split_id"] = "c43-split:" + digest(row)
            rows.append(row)
    rows.sort(key=lambda row: (row["pair_index"], row["parent_path"]))
    require(len(rows) == 2, "eligible adaptive split census")
    return rows


def build_leaf_and_reflection_rows(
    context: dict[str, Any],
    trees: dict[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           dict[tuple[int, str, str], dict[str, Any]]]:
    leaf_rows = []
    reflection_rows = []
    by_key: dict[tuple[int, str, str], dict[str, Any]] = {}
    cells = context["context"]["cells"]
    config = context["config"]
    for pair in EXPECTED_ELIGIBLE:
        task = context["tasks"][pair]
        reflected_task = make_reflected_task(task, cells)
        for leaf in trees[pair]["leaves"]:
            path = leaf["path"]
            reflected_path, rep_box, ref_box = reflected_path_and_box(
                task, path, cells
            )
            require(
                box_payload(rep_box) == box_payload(leaf["route"]["box"]),
                "leaf representative replay",
            )
            reflected_route = c41.route_at_path(
                reflected_task, reflected_path, config
            )
            require(
                reflected_route["classification"] == EXPECTED_LEAF_CLASS[pair]
                and box_payload(reflected_route["box"]) == box_payload(ref_box),
                "independently recomputed reflected terminal leaf",
            )
            rep_cert = c1_closed_box_certificate(
                pair, "REPRESENTATIVE", path,
                task["c38_source"]["representative_origin_key"],
                task["cell"], rep_box, config, "AMBIENT_TERMINAL_LEAF",
                terminal_credit=1,
            )
            ref_cert = c1_closed_box_certificate(
                pair, "REFLECTED", reflected_path,
                reflected_task["c38_source"]["representative_origin_key"],
                reflected_task["cell"], ref_box, config,
                "AMBIENT_TERMINAL_LEAF", terminal_credit=1,
            )
            for orientation, cert, cert_path in (
                ("REPRESENTATIVE", rep_cert, path),
                ("REFLECTED", ref_cert, reflected_path),
            ):
                row = {
                    "schema": LEAF_SCHEMA,
                    "pair_index": pair,
                    "orientation": orientation,
                    "path": cert_path,
                    "source_relative_fraction":
                        qstr(leaf["relative_fraction"]),
                    "absolute_parent_fraction": qstr(
                        SOURCE_FRACTION * leaf["relative_fraction"]
                    ),
                    "full_closed_box_certificate": cert,
                    "strict_terminal_excluded": True,
                    "local_round144_terminal_credit": 1,
                    "lower_dimensional_ambient_credit": 0,
                    "D02_gate_credit": 0,
                }
                row["closed_leaf_certificate_id"] = (
                    "c43-leaf:" + digest(row)
                )
                leaf_rows.append(row)
                by_key[(pair, orientation, cert_path)] = row
            transport = {
                "schema": REFLECTION_SCHEMA,
                "pair_index": pair,
                "representative_path": path,
                "reflected_path": reflected_path,
                "representative_certificate_id":
                    by_key[(pair, "REPRESENTATIVE", path)][
                        "closed_leaf_certificate_id"
                    ],
                "reflected_certificate_id":
                    by_key[(pair, "REFLECTED", reflected_path)][
                        "closed_leaf_certificate_id"
                    ],
                "representative_closed_box": box_payload(rep_box),
                "reflected_closed_box": box_payload(ref_box),
                "exact_map": "Jy:(t,p,s)->chart-dependent(-t,-p,s)",
                "endpoint_order_reversal_materialized": True,
                "reflected_route_recomputed_independently": True,
                "representative_classification":
                    rep_cert["strict_disposition"],
                "reflected_classification":
                    ref_cert["strict_disposition"],
                "transport_carries_no_independent_credit": True,
                "D02_gate_credit": 0,
            }
            transport["reflection_transport_id"] = (
                "c43-reflection:" + digest(transport)
            )
            reflection_rows.append(transport)
    leaf_rows.sort(key=lambda row: (
        row["pair_index"], row["orientation"], row["path"]
    ))
    reflection_rows.sort(key=lambda row: (
        row["pair_index"], row["representative_path"]
    ))
    require(
        len(leaf_rows) == 8 and len(reflection_rows) == 4,
        "eligible 4+4 leaf and 4 reflection census",
    )
    return leaf_rows, reflection_rows, by_key


def box_contains_point(box: dict[str, Any], t: Q, p: Q) -> bool:
    return (
        Q(box["t"][0]) <= t <= Q(box["t"][1])
        and Q(box["p"][0]) <= p <= Q(box["p"][1])
    )


def internal_rows(
    context: dict[str, Any],
    trees: dict[int, dict[str, Any]],
    leaf_by_key: dict[tuple[int, str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    cells = context["context"]["cells"]
    config = context["config"]
    for pair in EXPECTED_ELIGIBLE:
        task = context["tasks"][pair]
        reflected_task = make_reflected_task(task, cells)
        for split in trees[pair]["splits"]:
            orientation_rows = []
            for orientation, current_task in (
                ("REPRESENTATIVE", task),
                ("REFLECTED", reflected_task),
            ):
                if orientation == "REPRESENTATIVE":
                    parent_path = split["parent_path"]
                    lower_path, upper_path = split["child_paths"]
                    parent_box = split["parent_box"]
                    child_boxes = split["children"]
                    axis = split["axis"]
                    origin = task["c38_source"]["representative_origin_key"]
                else:
                    parent_path, _x, parent_box = reflected_path_and_box(
                        task, split["parent_path"], cells
                    )
                    child0, _a, box0 = reflected_path_and_box(
                        task, split["child_paths"][0], cells
                    )
                    child1, _b, box1 = reflected_path_and_box(
                        task, split["child_paths"][1], cells
                    )
                    mapped = sorted(((child0, box0), (child1, box1)))
                    lower_path, upper_path = (
                        parent_path + "0", parent_path + "1"
                    )
                    mapping = {path: box for path, box in mapped}
                    require(
                        set(mapping) == {lower_path, upper_path},
                        "reflected binary child path cover",
                    )
                    child_boxes = (
                        mapping[lower_path], mapping[upper_path]
                    )
                    axis = c41.c38.round166.longest_axis(parent_box)
                    origin = reflected_task[
                        "c38_source"
                    ]["representative_origin_key"]
                axis_name = ("t", "p")[axis]
                face_name = axis_name + "_upper"
                shared = make_face_box(child_boxes[0], face_name)
                direct = c1_closed_box_certificate(
                    pair, orientation, parent_path + ".shared",
                    origin, current_task["cell"], shared, config,
                    "INTERNAL_SPLIT_FACE", terminal_credit=0,
                )
                if axis == 0:
                    endpoints = [
                        type(shared)(
                            shared.t0, shared.t0, shared.p0, shared.p0,
                            shared.s0, shared.s1, 0, "endpoint0"
                        ),
                        type(shared)(
                            shared.t0, shared.t0, shared.p1, shared.p1,
                            shared.s0, shared.s1, 0, "endpoint1"
                        ),
                    ]
                else:
                    endpoints = [
                        type(shared)(
                            shared.t0, shared.t0, shared.p0, shared.p0,
                            shared.s0, shared.s1, 0, "endpoint0"
                        ),
                        type(shared)(
                            shared.t1, shared.t1, shared.p0, shared.p0,
                            shared.s0, shared.s1, 0, "endpoint1"
                        ),
                    ]
                endpoint_rows = []
                orientation_leaf_rows = [
                    row for (p, o, _path), row in leaf_by_key.items()
                    if p == pair and o == orientation
                ]
                for ordinal, point in enumerate(endpoints):
                    incidents = [
                        row["path"] for row in orientation_leaf_rows
                        if box_contains_point(
                            row["full_closed_box_certificate"]["closed_box"],
                            point.t0, point.p0,
                        )
                    ]
                    incidents.sort()
                    require(bool(incidents), "internal vertex incidents")
                    point_cert = c1_closed_box_certificate(
                        pair, orientation,
                        parent_path + f".vertex{ordinal}",
                        origin, current_task["cell"], point, config,
                        "INTERNAL_SPLIT_VERTEX", terminal_credit=0,
                    )
                    endpoint_rows.append({
                        "coordinate": {
                            "t": qstr(point.t0),
                            "p": qstr(point.p0),
                            "s": "0",
                        },
                        "incident_terminal_leaf_paths": incidents,
                        "canonical_owner_path": incidents[0],
                        "direct_closed_point_certificate": point_cert,
                        "vertex_ambient_credit": 0,
                    })
                midpoint_t = (shared.t0 + shared.t1) / 2
                midpoint_p = (shared.p0 + shared.p1) / 2
                incidents = [
                    row["path"] for row in orientation_leaf_rows
                    if box_contains_point(
                        row["full_closed_box_certificate"]["closed_box"],
                        midpoint_t, midpoint_p,
                    )
                ]
                incidents.sort()
                require(
                    incidents == [lower_path, upper_path],
                    "internal face two-child complete incidence",
                )
                orientation_rows.append({
                    "orientation": orientation,
                    "parent_path": parent_path,
                    "split_axis": axis_name,
                    "shared_face_closed_box": box_payload(shared),
                    "incident_terminal_leaf_paths": incidents,
                    "half_open_owner_path": lower_path,
                    "upper_bit_excludes_duplicate_face": True,
                    "direct_closed_face_certificate": direct,
                    "endpoint_vertices": endpoint_rows,
                    "lower_dimensional_ambient_credit": 0,
                })
            row = {
                "schema": INTERNAL_SCHEMA,
                "pair_index": pair,
                "representative_split_parent_path": split["parent_path"],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "physical_dimension_credit": 0,
                "D02_gate_credit": 0,
            }
            row["internal_strata_incidence_id"] = (
                "c43-internal:" + digest(row)
            )
            rows.append(row)
    rows.sort(key=lambda row: (
        row["pair_index"], row["representative_split_parent_path"]
    ))
    require(len(rows) == 2, "eligible internal split incidence census")
    return rows


def external_rows(
    context: dict[str, Any],
    boundary: dict[int, dict[str, Any]],
    geometry: list[tuple[Any, Any, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    face_rows = []
    corner_rows = []
    config = context["config"]
    terminal_ids = {
        context["C42_source"]["C41_target_ambient_cell_id"],
        *(
            context["C41_rows"][pair]["c41_ambient_cell_id"]
            for pair in EXPECTED_ELIGIBLE
        ),
    }
    for pair in EXPECTED_ELIGIBLE:
        task = context["tasks"][pair]
        source = context["C41_rows"][pair]
        for face in ("t_lower", "t_upper", "p_lower", "p_upper"):
            orientation_rows = []
            for orientation in ("REPRESENTATIVE", "REFLECTED"):
                origin, cell, box, path = target_orientation(
                    pair, orientation, task, source, context
                )
                partition = face_partition(
                    geometry, orientation, box, face, terminal_ids
                )
                require(
                    partition[
                        "all_required_segment_and_breakpoint_owners_terminal"
                    ],
                    "eligible external face owner remains residual",
                )
                direct_segments = []
                for ordinal, segment in enumerate(partition["segments"]):
                    lo, hi = map(Q, segment["interval"])
                    restricted = make_face_box(box, face, lo, hi)
                    direct_segments.append(c1_closed_box_certificate(
                        pair, orientation,
                        path + "." + face + f".segment{ordinal}",
                        origin, cell, restricted, config,
                        "SOURCE_EXTERIOR_FACE_SEGMENT", terminal_credit=0,
                    ))
                direct_breakpoints = []
                for ordinal, point in enumerate(
                    partition["interior_breakpoints"]
                ):
                    value = point["coordinate"]
                    restricted = type(box)(
                        Q(value["t"]), Q(value["t"]),
                        Q(value["p"]), Q(value["p"]),
                        Q(0), Q(0), 0, "breakpoint",
                    )
                    direct_breakpoints.append(c1_closed_box_certificate(
                        pair, orientation,
                        path + "." + face + f".breakpoint{ordinal}",
                        origin, cell, restricted, config,
                        "SOURCE_FACE_INTERNAL_BREAKPOINT", terminal_credit=0,
                    ))
                orientation_rows.append({
                    "orientation": orientation,
                    "target_path": path,
                    "source_face": face,
                    "global_incidence_partition": partition,
                    "direct_closed_segment_certificates": direct_segments,
                    "direct_internal_breakpoint_certificates":
                        direct_breakpoints,
                    "all_canonical_owners_terminal_after_C43_subset": True,
                    "face_ambient_credit": 0,
                })
            row = {
                "schema": FACE_SCHEMA,
                "pair_index": pair,
                "source_face": face,
                "C41_boundary_outer_id":
                    context["boundary_by_pair"][pair][
                        "boundary_corner_outer_id"
                    ],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "global_owner_rule":
                    "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)",
                "D02_gate_credit": 0,
            }
            row["source_face_owner_incidence_id"] = (
                "c43-face:" + digest(row)
            )
            face_rows.append(row)
        for corner in ("t0p0", "t0p1", "t1p0", "t1p1"):
            orientation_rows = []
            for orientation in ("REPRESENTATIVE", "REFLECTED"):
                origin, cell, box, path = target_orientation(
                    pair, orientation, task, source, context
                )
                point = make_point_box(box, corner)
                incidents = point_incidents(
                    geometry, orientation, point.t0, point.p0, terminal_ids
                )
                require(
                    incidents[0]["terminal_after_C43_subset"],
                    "eligible external corner owner remains residual",
                )
                direct = c1_closed_box_certificate(
                    pair, orientation, path + "." + corner,
                    origin, cell, point, config,
                    "SOURCE_EXTERIOR_CORNER", terminal_credit=0,
                )
                orientation_rows.append({
                    "orientation": orientation,
                    "target_path": path,
                    "coordinate": {
                        "t": qstr(point.t0),
                        "p": qstr(point.p0),
                        "s": "0",
                    },
                    "global_incident_ambient_cells": incidents,
                    "canonical_owner": incidents[0],
                    "canonical_owner_terminal_after_C43_subset": True,
                    "direct_closed_point_certificate": direct,
                    "corner_ambient_credit": 0,
                })
            row = {
                "schema": CORNER_SCHEMA,
                "pair_index": pair,
                "source_corner": corner,
                "C41_boundary_outer_id":
                    context["boundary_by_pair"][pair][
                        "boundary_corner_outer_id"
                    ],
                "orientation_restrictions": orientation_rows,
                "representative_and_reflected_restrictions_explicit": True,
                "global_owner_rule":
                    "LEXICOGRAPHIC_MINIMUM_(PATH,PAIR_INDEX,AMBIENT_ID)",
                "D02_gate_credit": 0,
            }
            row["source_corner_owner_incidence_id"] = (
                "c43-corner:" + digest(row)
            )
            corner_rows.append(row)
    face_rows.sort(key=lambda row: (row["pair_index"], row["source_face"]))
    corner_rows.sort(key=lambda row: (
        row["pair_index"], row["source_corner"]
    ))
    require(
        len(face_rows) == 8 and len(corner_rows) == 8,
        "eligible source face/corner slot census",
    )
    return face_rows, corner_rows


def parent_rows(context: dict[str, Any],
                trees: dict[int, dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    newly = 0
    for prior in context["C42_parent_rows"]:
        pair = prior["pair_index"]
        eligible = pair in EXPECTED_ELIGIBLE
        gain = SOURCE_FRACTION if eligible else Q(0)
        terminal = Q(prior["terminal_excluded_parent_volume"]) + gain
        unresolved = Q(prior["unresolved_parent_volume"]) - gain
        extra_leaves = (
            len(trees[pair]["leaves"]) - 1 if eligible else 0
        )
        terminal_leaf_gain = (
            len(trees[pair]["leaves"]) if eligible else 0
        )
        leaf_count = prior["leaf_count"] + extra_leaves
        terminal_leaf_count = (
            prior["terminal_leaf_count"] + terminal_leaf_gain
        )
        nonterminal_leaf_count = (
            prior["nonterminal_leaf_count"] - int(eligible)
        )
        whole = (
            terminal == 1 and unresolved == 0
            and nonterminal_leaf_count == 0
        )
        new = whole and not (
            prior["whole_representative_parent_terminal"]
            and prior["whole_reflected_parent_terminal"]
        )
        newly += int(new)
        row = {
            "schema": PARENT_SCHEMA,
            "pair_index": pair,
            "C42_parent_row_sha256": prior["row_sha256"],
            "C42_terminal_excluded_parent_volume":
                prior["terminal_excluded_parent_volume"],
            "C42_unresolved_parent_volume":
                prior["unresolved_parent_volume"],
            "C42_leaf_count": prior["leaf_count"],
            "C42_terminal_leaf_count": prior["terminal_leaf_count"],
            "C42_nonterminal_leaf_count": prior["nonterminal_leaf_count"],
            "C43_terminal_gain": qstr(gain),
            "terminal_excluded_parent_volume": qstr(terminal),
            "unresolved_parent_volume": qstr(unresolved),
            "parent_Kraft_conservation": "1",
            "leaf_count": leaf_count,
            "terminal_leaf_count": terminal_leaf_count,
            "nonterminal_leaf_count": nonterminal_leaf_count,
            "newly_whole_terminal_vs_C42": new,
            "whole_representative_parent_terminal": whole,
            "whole_reflected_parent_terminal": whole,
            "terminal_reflection_recomputation_materialized": (
                True if eligible
                else prior["terminal_reflection_transport_materialized"]
            ),
            "canonical_boundary_owner_eligible":
                (True if eligible else None),
            "blocked_source_zero_credit": pair in EXPECTED_BLOCKED,
            "C34_common_refinement_credit": 2 if whole else 0,
            "D02_gate_credit": 0,
        }
        require(
            terminal + unresolved == 1
            and leaf_count == terminal_leaf_count + nonterminal_leaf_count
            and nonterminal_leaf_count >= 0,
            "C43 parent conservation:" + str(pair),
        )
        if pair == INSTALLED_C42_PAIR:
            require(
                gain == 0
                and prior["row_sha256"]
                == "09ea54b6e2be756ba7a3f45f66492c98919b0d5b9722894b4028030514b50047",
                "C42 pair391 immutable carry",
            )
        rows.append(row)
    require(newly == 2, "exact two newly whole representatives")
    whole_count = sum(
        row["whole_representative_parent_terminal"]
        and row["whole_reflected_parent_terminal"]
        for row in rows
    )
    require(whole_count == 289, "C43 whole representative census")
    return rows, {
        "whole_representative_parent_count": whole_count,
        "whole_paired_coarse_cell_count": 2 * whole_count,
        "newly_whole_representative_parent_count": newly,
        "newly_whole_paired_coarse_cell_count": 2 * newly,
        "remaining_representative_parent_count": 862 - whole_count,
        "parent_row_count": len(rows),
    }


def round144_census() -> dict[str, Any]:
    semantic = {
        "schema": CENSUS_SCHEMA,
        "baseline": "INSTALLED_C42_F1_AUTHORITY",
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75_390,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": 1_146,
        "terminal_total": 76_832,
        "unresolved_zero": False,
        "eligible_representative_delta": 2,
        "paired_terminal_delta": 4,
        "blocked_zero_credit_pairs": list(EXPECTED_BLOCKED),
        "D02_gate_credit": 0,
    }
    require(
        semantic["EARLIEST_PREFIX_EXCLUDED"]
        + semantic["TYPED_EVENT_GRAPH"]
        + semantic["UNRESOLVED_R1648_CONTINUATION"] == 76_832,
        "round144 exact census",
    )
    semantic["census_object_sha256"] = digest(semantic)
    return semantic


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir()
        if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def validate_manifest(directory: Path) -> None:
    require(
        tuple(sorted(path.name for path in directory.iterdir())) == INVENTORY,
        "exact C43 candidate inventory",
    )
    raw = (directory / "root_manifest.sha256").read_text(encoding="utf-8")
    expected = "".join(
        f"{file_sha256(path)}  {path.name}\n"
        for path in sorted(directory.iterdir())
        if path.name != "root_manifest.sha256"
    )
    require(raw == expected, "C43 manifest replay")


def validate_published_candidate(
    directory: Path, expected_result: dict[str, Any]
) -> None:
    value = directory.lstat()
    require(
        stat.S_ISDIR(value.st_mode) and not directory.is_symlink(),
        "published C43 candidate real directory",
    )
    validate_manifest(directory)
    for member in directory.iterdir():
        c41.require_regular_single_link(member, "published C43 member")
    result = c41.strict_json(directory / "result.json")
    observed = result.get("object_sha256")
    semantic = dict(result)
    semantic.pop("object_sha256", None)
    require(
        observed == digest(semantic) and result == expected_result,
        "published C43 result self-hash and recapture",
    )
    for descriptor in result["ledgers"].values():
        for _row in c41.iter_ledger(directory, descriptor):
            pass
    census = c41.strict_json(directory / "round144_census.json")
    census_object = census.pop("census_object_sha256", None)
    require(
        census_object == digest(census),
        "published C43 round144 census self-hash",
    )


def preflight(*, capture: bool = True) -> dict[str, Any]:
    no_c43_authority_pointers()
    captures: dict[str, pilot.Capture] = {}
    directories = (
        RUNTIME, CANDIDATE_ROOT, AUDIT_ROOT, C40_DIR, C41_DIR, C42_DIR
    )
    before = {str(path): stat_fingerprint(path) for path in directories}
    try:
        if capture:
            captures = capture_inputs()
        context = load_inputs()
        trees = {
            pair: adaptive_tree(
                context["tasks"][pair],
                context["C41_rows"][pair]["path"],
                context["config"],
            )
            for pair in TARGET_PAIRS
        }
        provisional_terminal_ids = {
            context["C42_source"]["C41_target_ambient_cell_id"],
            *(
                context["C41_rows"][pair]["c41_ambient_cell_id"]
                for pair in TARGET_PAIRS
            ),
        }
        first_boundary, geometry = build_boundary_preflight(
            context, provisional_terminal_ids
        )
        eligible = tuple(
            pair for pair in TARGET_PAIRS
            if first_boundary[pair]["boundary_owner_eligible"]
        )
        require(eligible == EXPECTED_ELIGIBLE, "derived eligible subset")
        actual_terminal_ids = {
            context["C42_source"]["C41_target_ambient_cell_id"],
            *(
                context["C41_rows"][pair]["c41_ambient_cell_id"]
                for pair in eligible
            ),
        }
        boundary, geometry = build_boundary_preflight(
            context, actual_terminal_ids
        )
        require(
            tuple(pair for pair in TARGET_PAIRS
                  if boundary[pair]["boundary_owner_eligible"])
            == EXPECTED_ELIGIBLE,
            "stable eligible subset after blocked-source zero-credit removal",
        )
        preflight_semantic = source_preflight_rows(context, trees, boundary)
        report = {
            "schema": SCHEMA + ".preflight",
            "status":
                "PASS_C43_SUBSET_PREFLIGHT__ELIGIBLE_592_715__"
                "BLOCKED_97_211_664_ZERO_CREDIT",
            "installed_C42_authority_valid": True,
            "derived_sole_deficit_pairs": list(TARGET_PAIRS),
            "eligible_pairs": list(EXPECTED_ELIGIBLE),
            "blocked_pairs": list(EXPECTED_BLOCKED),
            "blocked_owner_census": {
                str(pair): boundary[pair][
                    "canonical_residual_owner_blockers"
                ]
                for pair in EXPECTED_BLOCKED
            },
            "adaptive_route_count": sum(
                tree["route_count"] for tree in trees.values()
            ),
            "adaptive_split_count": sum(
                len(tree["splits"]) for tree in trees.values()
            ),
            "adaptive_terminal_leaf_count": sum(
                len(tree["leaves"]) for tree in trees.values()
            ),
            "candidate_expected": {
                "whole_representatives": 289,
                "paired_coarse_cells_terminal": 578,
                "unresolved": 1_146,
                "remaining_representatives": 573,
            },
            "runtime_writes_performed": False,
            "authority_pointer_installed": False,
            "source_preflight_semantic_sha256": digest(preflight_semantic),
        }
        report["preflight_object_sha256"] = digest(report)
        if capture:
            for guard in captures.values():
                guard.unchanged("terminal C43 preflight")
            after = {str(path): stat_fingerprint(path) for path in directories}
            require(after == before, "preflight runtime tree unchanged")
        return {
            "report": report,
            "context": context,
            "trees": trees,
            "boundary": boundary,
            "geometry": geometry,
            "preflight_semantic": preflight_semantic,
            "captures": captures,
        }
    except Exception:
        close_captures(captures)
        raise


def build_formal(output: Path, receipt_output: Path,
                 invocation_id: str) -> dict[str, Any]:
    require(
        c42p.TOKEN.fullmatch(invocation_id) is not None,
        "InvocationID syntax",
    )
    output = c42p.workspace_path(output, "C43 output", must_exist=False)
    receipt_output = c42p.workspace_path(
        receipt_output, "C43 receipt", must_exist=False
    )
    stage, receipt_stage = c42p.initial_target_preflight(
        C42_DIR, C42_RECEIPT_PATH, C42_AUDIT_PATH,
        output, receipt_output,
    )
    no_c43_authority_pointers()
    state = preflight(capture=True)
    captures = state["captures"]
    context = state["context"]
    trees = state["trees"]
    boundary = state["boundary"]
    geometry = state["geometry"]
    preflight_semantic = state["preflight_semantic"]
    try:
        leaf_rows, reflection_rows, leaf_by_key = (
            build_leaf_and_reflection_rows(context, trees)
        )
        internal = internal_rows(context, trees, leaf_by_key)
        faces, corners = external_rows(context, boundary, geometry)
        split = split_rows(trees)
        parents, parent_census = parent_rows(context, trees)
        census = round144_census()

        stage.mkdir(mode=0o755)
        c42p.fsync_directory(CANDIDATE_ROOT)
        writers: dict[str, c41.LedgerWriter] = {}
        try:
            with ExitStack() as stack:
                specifications = (
                    ("source_preflight", "source_preflight.jsonl.gz",
                     "PAIR_INDEX_ASCENDING"),
                    ("source", "exact_sources.jsonl.gz",
                     "PAIR_INDEX_ASCENDING"),
                    ("split", "adaptive_splits.jsonl.gz",
                     "PAIR_INDEX_THEN_PARENT_PATH"),
                    ("leaf", "closed_leaf_certificates.jsonl.gz",
                     "PAIR_INDEX_ORIENTATION_PATH"),
                    ("reflection", "reflection_transport.jsonl.gz",
                     "PAIR_INDEX_REPRESENTATIVE_PATH"),
                    ("internal", "internal_strata_incidence.jsonl.gz",
                     "PAIR_INDEX_SPLIT_PARENT_PATH"),
                    ("face", "source_face_owner_incidence.jsonl.gz",
                     "PAIR_INDEX_FACE_ENUM"),
                    ("corner", "source_corner_owner_incidence.jsonl.gz",
                     "PAIR_INDEX_CORNER_ENUM"),
                    ("parent", "representative_parent_conservation.jsonl.gz",
                     "PAIR_INDEX_ASCENDING"),
                )
                for key, filename, order in specifications:
                    writers[key] = stack.enter_context(
                        c41.LedgerWriter(stage / filename, order)
                    )
                for semantic in preflight_semantic:
                    writers["source_preflight"].write(semantic)
                preflight_by_pair = {
                    row["pair_index"]: {
                        **row,
                        "row_sha256": digest(row),
                    }
                    for row in preflight_semantic
                }
                for semantic in exact_source_rows(
                    context, preflight_by_pair
                ):
                    writers["source"].write(semantic)
                for key, rows in (
                    ("split", split),
                    ("leaf", leaf_rows),
                    ("reflection", reflection_rows),
                    ("internal", internal),
                    ("face", faces),
                    ("corner", corners),
                    ("parent", parents),
                ):
                    for semantic in rows:
                        writers[key].write(semantic)

            write_json(stage / "round144_census.json", census)
            lock_text = (
                "C43 is a producer-only non-authority candidate. It grants "
                "credit only to owner-eligible pairs 592 and 715. Pairs 97, "
                "211, and 664 remain canonical residual-owner blockers with "
                "zero credit. The candidate cannot install C43 pointers. D02 "
                "remains blocked by 1146 complete R1648 continuations; D03, "
                "D04, Gate5 promotion, and every CM2 claim remain unauthorized.\n"
            )
            (stage / "C43_SUBSET_CLOSURE.lock").write_text(
                lock_text, encoding="utf-8"
            )
            descriptors = {
                "source_preflight": writers["source_preflight"].descriptor(),
                "exact_sources": writers["source"].descriptor(),
                "adaptive_splits": writers["split"].descriptor(),
                "closed_leaf_certificates": writers["leaf"].descriptor(),
                "reflection_transport": writers["reflection"].descriptor(),
                "internal_strata_incidence": writers["internal"].descriptor(),
                "source_face_owner_incidence": writers["face"].descriptor(),
                "source_corner_owner_incidence": writers["corner"].descriptor(),
                "representative_parent_conservation":
                    writers["parent"].descriptor(),
            }
            result = {
                "schema": SCHEMA,
                "status":
                    "FORMAL_PRODUCER_PASS_C43_OWNER_ELIGIBLE_SUBSET_"
                    "592_715__578_PAIRED__1146_UNRESOLVED__"
                    "PENDING_INDEPENDENT_C43_AUDIT",
                "formal_producer_run": True,
                "producer_output_is_authority": False,
                "formal_authority": False,
                "authority_pointer_installed": False,
                "independent_C43_audit_outstanding": True,
                "producer_source_sha256": captures["self"].sha256,
                "installed_C42_authority": {
                    "candidate_object_sha256": pilot.EXPECTED_C42_OBJECT,
                    "independent_audit_object_sha256":
                        pilot.EXPECTED_C42_AUDIT_OBJECT,
                    "authority_seal_object_sha256":
                        pilot.EXPECTED_C42_SEAL_OBJECT,
                    "installation_receipt_object_sha256":
                        pilot.EXPECTED_C42_RECEIPT_OBJECT,
                    "root_manifest_sha256": EXPECTED_C42_MANIFEST,
                },
                "target_discovery": {
                    "derived_post_C42_sole_deficit_pairs":
                        list(TARGET_PAIRS),
                    "owner_eligible_pairs": list(EXPECTED_ELIGIBLE),
                    "canonical_residual_owner_blocked_pairs":
                        list(EXPECTED_BLOCKED),
                    "blocked_pairs_receive_credit": False,
                },
                "closure_census": {
                    "source_preflight_count": 5,
                    "eligible_exact_source_count": 2,
                    "blocked_zero_credit_source_count": 3,
                    "adaptive_split_count": len(split),
                    "representative_terminal_leaf_count": 4,
                    "reflected_terminal_leaf_count": 4,
                    "closed_leaf_certificate_count": len(leaf_rows),
                    "reflection_transport_count": len(reflection_rows),
                    "internal_split_incidence_count": len(internal),
                    "source_face_slot_count": len(faces),
                    "source_corner_slot_count": len(corners),
                    **parent_census,
                },
                "ledgers": descriptors,
                "round144_census": {
                    "filename": "round144_census.json",
                    "sha256": file_sha256(
                        stage / "round144_census.json"
                    ),
                    "object_sha256": census["census_object_sha256"],
                    "EARLIEST_PREFIX_EXCLUDED": 75_390,
                    "TYPED_EVENT_GRAPH": 296,
                    "UNRESOLVED_R1648_CONTINUATION": 1_146,
                    "unresolved_zero": False,
                },
                "nonpromotion_lock": {
                    "filename": "C43_SUBSET_CLOSURE.lock",
                    "sha256": file_sha256(
                        stage / "C43_SUBSET_CLOSURE.lock"
                    ),
                    "producer_output_is_authority": False,
                },
                "strict_nonpromotion": {
                    "D02":
                        "BLOCKED_BY_1146_COMPLETE_R1648_CONTINUATIONS",
                    "D03": "UNAUTHORIZED",
                    "D04": "NOT_MINTED",
                    "Gate5": "10/18",
                    "complete_global_18_field_blocks": 0,
                    "CM2": "NO-GO_FOR_CLAIM",
                },
                "required_next":
                    "independent C43 audit before any separate authority "
                    "installation transaction; continue blocked boundary "
                    "owners and the remaining 573 representatives",
            }
            result["object_sha256"] = digest(result)
            write_json(stage / "result.json", result)
            write_manifest(stage)
            validate_manifest(stage)
            validate_published_candidate(stage, result)
            for path in sorted(stage.iterdir()):
                c42p.fsync_file(path)
            c42p.fsync_directory(stage)

            receipt = {
                "schema": RECEIPT_SCHEMA,
                "status":
                    "FORMAL_PRODUCER_PASS_C43_RECEIPT__"
                    "PENDING_INDEPENDENT_C43_AUDIT__NO_AUTHORITY",
                "InvocationID": invocation_id,
                "pid": os.getpid(),
                "proc_start_ticks": c42p.proc_start_ticks(os.getpid()),
                "producer_source_sha256": captures["self"].sha256,
                "candidate_path": str(output.relative_to(ROOT)),
                "candidate_object_sha256": result["object_sha256"],
                "root_manifest_sha256": file_sha256(
                    stage / "root_manifest.sha256"
                ),
                "installed_C42_candidate_object_sha256":
                    pilot.EXPECTED_C42_OBJECT,
                "eligible_pairs": list(EXPECTED_ELIGIBLE),
                "blocked_zero_credit_pairs": list(EXPECTED_BLOCKED),
                "producer_output_is_authority": False,
                "authority_pointer_installed": False,
                "created_unix_ns": time.time_ns(),
            }
            receipt["receipt_object_sha256"] = digest(receipt)
            receipt_payload = canonical(receipt) + b"\n"
            for guard in captures.values():
                guard.unchanged("prepublication C43")
            no_c43_authority_pointers()
            c42p.publish_candidate_and_receipt(
                stage, output, receipt_output, receipt_payload
            )
            validate_published_candidate(output, result)
            c42p.validate_published_receipt(receipt_output, receipt)
            no_c43_authority_pointers()
            for guard in captures.values():
                guard.unchanged("postpublication C43")
            return {
                "candidate_path": str(output.relative_to(ROOT)),
                "candidate_object_sha256": result["object_sha256"],
                "root_manifest_sha256": receipt["root_manifest_sha256"],
                "receipt_path": str(receipt_output.relative_to(ROOT)),
                "receipt_object_sha256":
                    receipt["receipt_object_sha256"],
                "authority_pointer_installed": False,
                "whole_paired_coarse_cells": 578,
                "whole_representatives": 289,
                "unresolved": 1_146,
                "remaining_representatives": 573,
            }
        except Exception:
            if stage.exists():
                shutil.rmtree(stage)
                c42p.fsync_directory(CANDIDATE_ROOT)
            raise
    finally:
        close_captures(captures)


def self_test() -> dict[str, Any]:
    require(
        file_sha256(Path(planner.__file__).resolve())
        == EXPECTED_PLANNER_SOURCE
        and file_sha256(Path(pilot.__file__).resolve())
        == EXPECTED_PILOT_SOURCE
        and file_sha256(Path(c41.__file__).resolve())
        == EXPECTED_C41_SOURCE
        and file_sha256(Path(c42p.__file__).resolve())
        == EXPECTED_C42_PRODUCER_SOURCE
        and file_sha256(Path(c42tx.__file__).resolve())
        == EXPECTED_C42_TX_AUDITOR_SOURCE,
        "self-test source pins",
    )
    fake = {
        "path": "010",
        "pair_index": 7,
        "c41_ambient_cell_id": "cell",
    }
    require(owner_key(fake) == ("010", 7, "cell"), "owner key order")
    census = round144_census()
    require(
        census["UNRESOLVED_R1648_CONTINUATION"] == 1_146
        and census["EARLIEST_PREFIX_EXCLUDED"] == 75_390,
        "subset census fixture",
    )
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C43_PRODUCER_STATIC_SELF_TEST",
        "eligible_pairs": list(EXPECTED_ELIGIBLE),
        "blocked_zero_credit_pairs": list(EXPECTED_BLOCKED),
        "expected_whole_paired": 578,
        "expected_whole_representatives": 289,
        "expected_unresolved": 1_146,
        "producer_installs_pointer": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--pilot", action="store_true")
    mode.add_argument("--formal", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt-output", type=Path)
    parser.add_argument("--invocation-id")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            require(
                arguments.output is None
                and arguments.receipt_output is None
                and arguments.invocation_id is None,
                "self-test takes no output arguments",
            )
            value = self_test()
        elif arguments.preflight or arguments.pilot:
            require(
                arguments.output is None
                and arguments.receipt_output is None
                and arguments.invocation_id is None,
                "read-only preflight takes no output arguments",
            )
            state = preflight(capture=True)
            value = state["report"]
            close_captures(state["captures"])
        else:
            require(
                arguments.output is not None
                and arguments.receipt_output is not None
                and arguments.invocation_id is not None,
                "formal output/receipt/InvocationID required",
            )
            value = build_formal(
                arguments.output,
                arguments.receipt_output,
                arguments.invocation_id,
            )
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 0
    except Exception as error:
        failure = {
            "schema": SCHEMA + ".failure",
            "status": "FAIL_CLOSED_C43_PRODUCER",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "candidate_published": False,
            "authority_pointer_installed": False,
        }
        sys.stderr.buffer.write(canonical(failure) + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
