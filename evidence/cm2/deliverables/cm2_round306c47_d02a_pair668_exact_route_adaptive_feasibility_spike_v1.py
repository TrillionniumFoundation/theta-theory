#!/usr/bin/env python3
"""C47 read-only D02-A exact-route adaptive feasibility spike, version 1.

This program deliberately has no producer, installer, receipt, pointer, seal,
or runtime-write mode.  It reconstructs the frozen C46-A 64-shard plan,
selects its deterministic first ``OWNER_PREREQUISITE`` task for pair 668,
cross-binds that task to C41 and C40, and calls the frozen C41 exact routing
and exact dyadic split primitives on the actual rational box.

There is no mathematical depth cutoff.  ``--event-budget`` is only a resource
budget: when it is exhausted every leaf remains in a prefix-free,
Kraft-conserving ``RESUMABLE_PENDING_ZERO_CREDIT`` checkpoint.  A route that
looks terminal is not emitted as a candidate exit because the existing helper
surface does not supply the complete two-side terminal margin and global
lower-strata owner certificate required by D02-A.

Normal use (stdout only)::

  python3.12 -I -B THIS.py --self-test
  python3.12 -I -B THIS.py --probe --event-budget 4
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c47.d02-a-pair668-exact-route-adaptive-spike.v1"
CHECKPOINT_SCHEMA = SCHEMA + ".prefix-free-pending-checkpoint"

C46_NAME = (
    "cm2_round306c46_d02a_general_adaptive_lower_strata_"
    "closure_engine_v1"
)
C41_NAME = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
C46_SOURCE = DELIVERABLES / (C46_NAME + ".py")
C41_SOURCE = DELIVERABLES / (C41_NAME + ".py")
C46_SOURCE_SHA256 = (
    "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea"
)
C46_PLAN_OBJECT_SHA256 = (
    "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
)
C41_SOURCE_SHA256 = (
    "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
)
C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_DIR = RUNTIME / "candidates" / C41_TOKEN
C41_OBJECT_SHA256 = (
    "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
)
C42_SEAL_OBJECT_SHA256 = (
    "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
)
C43_TOKEN = "c43-sole-deficit-owner-closure-20260811T082400Z-f1"
C43_DIR = RUNTIME / "candidates" / C43_TOKEN
C43_OBJECT_SHA256 = (
    "79831178f4450c41540b7ff0f51bde96e61517cbc36a2287efbf0a100cba5bbc"
)

DEFAULT_PAIR = 668
EXPECTED_PAIR_TASK_COUNT = 43
EXPECTED_FIRST_TASK_BINDING = (
    "64400932860d6f224a90204e56a5614bf982eb3a1b87f37f04b86ba112a3ff9f"
)
EXPECTED_FIRST_PATH = "010111011"
EXPECTED_FIRST_AMBIENT_ID = (
    "c41-ambient:a828b4c95611e3e12ab8b3131f19f801ce8e1f1541106010ea94f34ba981a351"
)
EXPECTED_FIRST_PRIMARY_ID = (
    "c41-c2-outer:4037ee276cf83fdf894f563b3967beba1dc5889764f951a8b8d2c4441b3258e4"
)

HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Rejected(RuntimeError):
    """Fail-closed input, replay, or conservation rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def sequence_digest(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def load_frozen_modules() -> tuple[Any, Any]:
    need(file_sha256(C46_SOURCE) == C46_SOURCE_SHA256,
         "frozen C46-A source SHA-256")
    need(file_sha256(C41_SOURCE) == C41_SOURCE_SHA256,
         "frozen C41 source SHA-256")
    sys.path.insert(0, str(DELIVERABLES))
    try:
        c46 = importlib.import_module(C46_NAME)
        c41 = importlib.import_module(C41_NAME)
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    need(Path(c46.__file__).absolute() == C46_SOURCE,
         "C46-A imported from pinned path")
    need(Path(c41.__file__).absolute() == C41_SOURCE,
         "C41 imported from pinned path")
    return c46, c41


def row_id(row: dict[str, Any], field: str, prefix: str) -> str:
    value = row.get(field)
    body = dict(row)
    body.pop(field, None)
    need(type(value) is str and value == prefix + digest(body),
         "derived row id:" + field)
    return value


def row_sha(row: dict[str, Any]) -> str:
    return digest(row)


def primary_rows(groups: dict[str, list[dict[str, Any]]]) \
        -> list[tuple[str, dict[str, Any], str, str]]:
    result: list[tuple[str, dict[str, Any], str, str]] = []
    for family, field, prefix in (
        ("C1_H1", "c1_h1_surface_outer_id", "c41-c1-h1-outer:"),
        ("ENDPOINT_RECHART", "endpoint_rechart_id", "c41-endpoint-rechart:"),
        ("C2", "c2_surface_outer_id", "c41-c2-outer:"),
    ):
        for row in groups[{"C1_H1": "c1", "ENDPOINT_RECHART": "endpoint",
                           "C2": "c2"}[family]]:
            # Endpoint rows orthogonal to a C1/C2 primary are dependencies,
            # not a second primary.
            if family == "ENDPOINT_RECHART" and row.get(
                    "orthogonal_to_primary_residual") is True:
                continue
            result.append((family, row, field, prefix))
    return result


def compact_surface(surface: dict[str, Any]) -> dict[str, Any]:
    return {
        "normalized_surface_id": surface["normalized_surface_id"],
        "kind": surface.get("kind"),
        "identifier": surface.get("identifier"),
        "equation": surface.get("equation"),
        "strict_derivative_axes": surface.get("strict_derivative_axes"),
        "certified_nonempty_regular_graph": surface.get(
            "certified_nonempty_regular_graph"
        ),
        "carrier_existence_status": surface.get("carrier_existence_status"),
        "entry_sha256": digest(surface),
    }


def compact_endpoint(row: dict[str, Any]) -> dict[str, Any]:
    endpoint_id = row_id(
        row, "endpoint_rechart_id", "c41-endpoint-rechart:"
    )
    geometry = row.get("endpoint_rechart_geometry") or {}
    return {
        "endpoint_rechart_id": endpoint_id,
        "row_sha256": row_sha(row),
        "orthogonal_to_primary_residual": row.get(
            "orthogonal_to_primary_residual", False
        ),
        "endpoint_kind": geometry.get("endpoint_kind"),
        "carrier_existence_status": row.get("carrier_existence_status"),
        "rechart_route_status": geometry.get("rechart_route_status"),
        "transformed_route_evaluator_status": geometry.get(
            "transformed_route_evaluator_status"
        ),
    }


def compact_incidence(row: dict[str, Any]) -> dict[str, Any]:
    incidence_id = row_id(
        row, "incidence_outer_id", "c41-incidence:"
    )
    return {
        "incidence_outer_id": incidence_id,
        "row_sha256": row_sha(row),
        "left_normalized_surface_id": row[
            "left_normalized_surface_id"
        ],
        "right_normalized_surface_id": row[
            "right_normalized_surface_id"
        ],
        "classification": row.get("classification"),
        "intersection_existence": row.get("intersection_existence"),
        "certified_intersection_dimension": row.get(
            "certified_intersection_dimension"
        ),
        "rank_status": row.get("rank_status"),
    }


def compact_boundary(
    row: dict[str, Any], ambient_identity: dict[str, Any],
) -> dict[str, Any]:
    boundary_id = row_id(
        row, "boundary_corner_outer_id", "c41-boundary-corner:"
    )
    faces: list[dict[str, Any]] = []
    for index, face in enumerate(row["face_rows"]):
        face_id = face.get("boundary_face_id")
        face_body = dict(face)
        face_body.pop("boundary_face_id", None)
        need(
            type(face_id) is str
            and face_id == "c41-boundary-face:" + digest({
                "ambient": ambient_identity, **face_body,
            }),
            "boundary face exact id:" + str(index),
        )
        links = []
        for link_index, link in enumerate(face["surface_face_incidence_links"]):
            link_id = row_id(
                link, "surface_face_incidence_id",
                "c41-surface-face-incidence:"
            )
            links.append({
                "surface_face_incidence_id": link_id,
                "classification": link.get("classification"),
                "intersection_existence": link.get("intersection_existence"),
                "certified_intersection_dimension": link.get(
                    "certified_intersection_dimension"
                ),
                "rank_status": link.get("rank_status"),
                "link_ordinal": link_index,
            })
        faces.append({
            "face_ordinal": index,
            "face": face["face"],
            "boundary_face_id": face_id,
            "exact_closed_face_box": face["exact_closed_face_box"],
            "last_split_face": face["last_split_face"],
            "half_open_face_role": face["half_open_face_role"],
            "global_face_owner_rule": face["global_face_owner_rule"],
            "global_face_owner_resolved": face[
                "global_face_owner_resolved"
            ],
            "surface_face_incidence_links": links,
        })
    corners: list[dict[str, Any]] = []
    for index, corner in enumerate(row["corner_rows"]):
        corner_id = corner.get("boundary_corner_id")
        corner_body = dict(corner)
        corner_body.pop("boundary_corner_id", None)
        need(
            type(corner_id) is str
            and corner_id == "c41-boundary-corner-point:" + digest({
                "ambient": ambient_identity, **corner_body,
            }),
            "boundary corner exact id:" + str(index),
        )
        corners.append({
            "corner_ordinal": index,
            "corner": corner["corner"],
            "boundary_corner_id": corner_id,
            "exact_closed_corner_box": corner["exact_closed_corner_box"],
            "global_corner_owner_rule": corner["global_corner_owner_rule"],
            "global_corner_owner_resolved": corner[
                "global_corner_owner_resolved"
            ],
            "surface_corner_incidence_status": corner[
                "surface_corner_incidence_status"
            ],
        })
    return {
        "boundary_corner_outer_id": boundary_id,
        "row_sha256": row_sha(row),
        "face_intersection_status": row["face_intersection_status"],
        "corner_intersection_status": row["corner_intersection_status"],
        "global_sibling_adjacency_and_half_open_owner_complete": row[
            "global_sibling_adjacency_and_half_open_owner_complete"
        ],
        "boundary_and_corner_inventory_complete": row[
            "boundary_and_corner_inventory_complete"
        ],
        "faces": faces,
        "corners": corners,
    }


def obligation_summary(
    c41: Any, ctask: dict[str, Any], route: dict[str, Any], path: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, list[dict[str, Any]]]]:
    source = ctask["source"]
    need(path.startswith(source["path"]), "route path extends C40 source")
    bits = path[len(source["path"]):]
    history = c41.exact_axis_history(ctask, bits)
    fraction = Q(source["parent_volume_fraction"]) / (2 ** len(bits))
    ambient, groups = c41.make_ambient_row(
        ctask, route, bits, len(bits), fraction, history
    )
    need(ambient["path"] == path, "C41 generated ambient path")
    identity = {
        "pair_index": source["pair_index"],
        "c40_source_leaf_id": source["c40_leaf_id"],
        "path": path,
        "parent_volume_fraction": c41.qstr(fraction),
    }
    primary = primary_rows(groups)
    family = c41.disposition_family(route["classification"])
    if family == "RESIDUAL_OUTER":
        need(len(primary) == 1, "one residual primary outer")
        primary_family, primary_row, primary_field, primary_prefix = primary[0]
        primary_id = row_id(primary_row, primary_field, primary_prefix)
        surfaces = [compact_surface(row) for row in primary_row[
            "normalized_surfaces"
        ]]
    else:
        need(not primary and not groups["incidence"] and not groups["boundary"],
             "terminal route has no residual lower-strata rows")
        primary_family = None
        primary_row = None
        primary_id = None
        surfaces = []
    endpoints = [compact_endpoint(row) for row in groups["endpoint"] if row
                 is not primary_row]
    incidences = [compact_incidence(row) for row in groups["incidence"]]
    boundaries = [compact_boundary(row, identity) for row in groups["boundary"]]
    need(len(boundaries) in {0, 1}, "zero or one boundary outer")

    route_blockers: list[str] = []
    if family == "RESIDUAL_OUTER":
        if route.get("c2_status") is not None:
            route_blockers.append(
                "C41.route_at_path.c2_status=" + str(route["c2_status"])
            )
        else:
            route_blockers.append(
                "C41.route_at_path.classification=" + route["classification"]
            )
    global_owner_blockers: list[str] = []
    for index, endpoint in enumerate(endpoints):
        if endpoint["transformed_route_evaluator_status"] in {None, "PENDING"}:
            global_owner_blockers.append(
                f"endpoint_recharts[{index}].transformed_route_evaluator_status="
                + str(endpoint["transformed_route_evaluator_status"])
            )
    for index, incidence in enumerate(incidences):
        if incidence["rank_status"] is None:
            global_owner_blockers.append(
                f"incidences[{index}].rank_status=null"
            )
    if boundaries:
        boundary = boundaries[0]
        if not boundary[
                "global_sibling_adjacency_and_half_open_owner_complete"]:
            global_owner_blockers.append(
                "boundary.global_sibling_adjacency_and_half_open_owner_complete=false"
            )
        for index, face in enumerate(boundary["faces"]):
            if not face["global_face_owner_resolved"]:
                global_owner_blockers.append(
                    f"boundary.faces[{index}].global_face_owner_resolved=false"
                )
            for link_index, link in enumerate(
                    face["surface_face_incidence_links"]):
                if link["rank_status"] is None:
                    global_owner_blockers.append(
                        f"boundary.faces[{index}].surface_face_incidence_links"
                        f"[{link_index}].rank_status=null"
                    )
        for index, corner in enumerate(boundary["corners"]):
            if not corner["global_corner_owner_resolved"]:
                global_owner_blockers.append(
                    f"boundary.corners[{index}].global_corner_owner_resolved=false"
                )
    certificate_blockers = [
        "physical_sides.REFLECTED.independent_exact_route_certificate=absent",
        "terminal.strict_margin=absent",
    ]
    first_missing = (
        route_blockers[0] if route_blockers
        else global_owner_blockers[0] if global_owner_blockers
        else certificate_blockers[0]
    )
    summary = {
        "primary_family": primary_family,
        "primary_outer_id": primary_id,
        "primary_row_sha256": (
            row_sha(primary_row) if primary_row is not None else None
        ),
        "normalized_graphs": surfaces,
        "endpoint_recharts": endpoints,
        "pair_incidences": incidences,
        "boundary": boundaries[0] if boundaries else None,
        "ordered_obligation_ids": groups["obligation_ids"][0],
        "route_blockers": route_blockers,
        "global_owner_blockers": global_owner_blockers,
        "certificate_blockers": certificate_blockers,
        "first_missing_field": first_missing,
        "all_real_certificates_complete": False,
        "candidate_exit_emitted": False,
        "formal_credit": 0,
    }
    return ambient, summary, groups


def route_observation(c41: Any, route: dict[str, Any]) -> dict[str, Any]:
    surfaces = c41.surface_summaries(route)
    return {
        "classification": route["classification"],
        "disposition_family": c41.disposition_family(route["classification"]),
        "route_method": route["route_method"],
        "witness": route["witness"],
        "witness_sha256": hashlib.sha256(
            str(route["witness"]).encode("utf-8")
        ).hexdigest(),
        "C1_result_object_sha256": (
            digest(route["c1_result"])
            if route["c1_result"] is not None else None
        ),
        "C2_status": route["c2_status"],
        "C2_baseline": route["c2_baseline"],
        "C2_detail_object_sha256": (
            digest(route["c2_detail"])
            if route["c2_detail"] is not None else None
        ),
        "C2_evidence_count": len(route["c2_evidence"]),
        "C2_evidence_sequence_sha256": sequence_digest([
            digest(row) for row in route["c2_evidence"]
        ]),
        "normalized_surface_count": len(surfaces),
        "normalized_surface_sequence_sha256": sequence_digest([
            digest(row) for row in surfaces
        ]),
        "route_failure": route["route_failure"],
    }


def find_selected_inputs(c46: Any, c41: Any) -> dict[str, Any]:
    plan, tasks, _shards = c46.build_read_only_plan(64)
    need(plan.get("plan_object_sha256") == C46_PLAN_OBJECT_SHA256,
         "frozen C46-A 64-shard plan object")
    need(plan["authority_baseline"]["authority_seal_object_sha256"]
         == C42_SEAL_OBJECT_SHA256,
         "installed C42 seal object baseline")
    selected_group = sorted(
        [row for row in tasks
         if row["pair_index"] == DEFAULT_PAIR
         and row["queue"]["priority_class"] == "OWNER_PREREQUISITE"],
        key=lambda row: (row["descendant_path"], row["primary_outer_id"]),
    )
    need(len(selected_group) == EXPECTED_PAIR_TASK_COUNT,
         "exact pair-668 prerequisite task census")
    selected = selected_group[0]
    need(
        selected["task_binding_sha256"] == EXPECTED_FIRST_TASK_BINDING
        and selected["descendant_path"] == EXPECTED_FIRST_PATH
        and selected["ambient_cell_id"] == EXPECTED_FIRST_AMBIENT_ID
        and selected["primary_outer_id"] == EXPECTED_FIRST_PRIMARY_ID,
        "deterministic first pair-668 task pins",
    )

    result = c41.strict_json(C41_DIR / "result.json")
    c41.validate_object(result, C41_OBJECT_SHA256, "C41 candidate")
    ambient = None
    for row in c41.iter_ledger(
            C41_DIR, result["ledgers"]["routed_ambient_cells"]):
        if row["c41_ambient_cell_id"] == selected["ambient_cell_id"]:
            need(ambient is None, "selected C41 ambient uniqueness")
            ambient = row
    need(ambient is not None, "selected C41 ambient exists")
    need(
        ambient["row_sha256"] == selected["ambient_row_sha256"]
        and ambient["path"] == selected["descendant_path"]
        and ambient["pair_index"] == DEFAULT_PAIR,
        "selected C46 task to C41 ambient exact binding",
    )

    c40_dir = ROOT / result["C40_authority"]["path"]
    c40_audit = ROOT / result["C40_authority"]["independent_audit_path"]
    c40_result = c41.strict_json(c40_dir / "result.json")
    source = None
    source_ordinal = None
    for ordinal, row in enumerate(c41.iter_ledger(
            c40_dir, c40_result["ledgers"]["routed_leaf_cells"])):
        if row["c40_leaf_id"] == ambient["c40_source_leaf_id"]:
            need(source is None, "selected C40 source uniqueness")
            source = row
            source_ordinal = ordinal
    need(source is not None and type(source_ordinal) is int,
         "selected C40 source exists")
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    config = c41.decode_worker_config(context["config"])
    ctask = c41.task_for_row(source_ordinal, source, context)
    need(selected["descendant_path"].startswith(source["path"]),
         "selected path extends C40 source path")
    return {
        "plan": plan,
        "selected": selected,
        "selected_group": selected_group,
        "C41_result": result,
        "ambient": ambient,
        "C40_dir": c40_dir,
        "C40_result": c40_result,
        "source": source,
        "source_ordinal": source_ordinal,
        "context": context,
        "config": config,
        "C41_task": ctask,
    }


def validate_frozen_root(
    selected: dict[str, Any], ambient_ledger: dict[str, Any],
    generated_ambient: dict[str, Any], obligations: dict[str, Any],
) -> None:
    need(
        generated_ambient["c41_ambient_cell_id"] == selected["ambient_cell_id"]
        and digest(generated_ambient) == selected["ambient_row_sha256"]
        == ambient_ledger["row_sha256"],
        "fresh C41 route reproduces frozen selected ambient row",
    )
    need(
        obligations["primary_outer_id"] == selected["primary_outer_id"]
        and obligations["primary_row_sha256"]
        == selected["primary_outer_row_sha256"],
        "fresh C41 route reproduces frozen selected primary row",
    )
    dependencies = selected["lower_strata_dependencies"]
    need(
        len(obligations["normalized_graphs"])
        == dependencies["normalized_surface_count"]
        and digest([row["normalized_surface_id"]
                    for row in obligations["normalized_graphs"]])
        == dependencies["normalized_surface_ids_sha256"]
        and len(obligations["endpoint_recharts"])
        == dependencies["endpoint_rechart_count"]
        and digest([row["endpoint_rechart_id"]
                    for row in obligations["endpoint_recharts"]])
        == dependencies["endpoint_rechart_ids_sha256"]
        and len(obligations["pair_incidences"])
        == dependencies["pair_incidence_count"]
        and digest([row["incidence_outer_id"]
                    for row in obligations["pair_incidences"]])
        == dependencies["pair_incidence_ids_sha256"],
        "fresh root graph/endpoint/incidence dependency census",
    )
    boundary = obligations["boundary"]
    need(
        boundary is not None
        and boundary["boundary_corner_outer_id"]
        == dependencies["boundary_outer_id"]
        and boundary["row_sha256"] == dependencies["boundary_outer_row_sha256"]
        and digest([row["boundary_face_id"] for row in boundary["faces"]])
        == dependencies["face_ids_sha256"]
        and digest([row["boundary_corner_id"] for row in boundary["corners"]])
        == dependencies["corner_ids_sha256"],
        "fresh root boundary/face/corner dependency census",
    )


def c43_capability_check(c41: Any, plan: dict[str, Any]) -> dict[str, Any]:
    result = c41.strict_json(C43_DIR / "result.json")
    c41.validate_object(result, C43_OBJECT_SHA256, "C43 conditional candidate")
    exact_pairs = [
        row["pair_index"] for row in c41.iter_ledger(
            C43_DIR, result["ledgers"]["exact_sources"]
        )
    ]
    preflight_pairs = [
        row["pair_index"] for row in c41.iter_ledger(
            C43_DIR, result["ledgers"]["source_preflight"]
        )
    ]
    need(exact_pairs == [592, 715], "C43 exact-source subset")
    need(sorted(preflight_pairs) == [97, 211, 592, 664, 715],
         "C43 sole-deficit preflight scope")
    overlay = plan["C43_conditional_rejected_overlay"]
    need(
        overlay["candidate_object_sha256"] == C43_OBJECT_SHA256
        and overlay["authority_status"]
        == "REJECTED_FOR_AUTHORITY__ZERO_FORMAL_CREDIT",
        "C43 rejected overlay boundary",
    )
    return {
        "candidate_object_sha256": C43_OBJECT_SHA256,
        "authority_status": overlay["authority_status"],
        "exact_source_pairs": exact_pairs,
        "source_preflight_pairs": sorted(preflight_pairs),
        "pair_668_exact_source_certificate_present": DEFAULT_PAIR in exact_pairs,
        "pair_668_within_C43_source_preflight_scope": DEFAULT_PAIR in preflight_pairs,
        "global_owner_certificate_available_for_selected_pair668_task": False,
        "formal_credit": 0,
    }


def prefix_free(paths: list[str]) -> bool:
    return len(paths) == len(set(paths)) and not any(
        right.startswith(left)
        for left in paths for right in paths if left != right
    )


def run_probe(event_budget: int) -> dict[str, Any]:
    need(type(event_budget) is int and 1 <= event_budget <= 64,
         "event budget in [1,64]")
    c46, c41 = load_frozen_modules()
    frozen = find_selected_inputs(c46, c41)
    selected = frozen["selected"]
    ctask = frozen["C41_task"]
    config = frozen["config"]
    root_path = selected["descendant_path"]
    source_path = frozen["source"]["path"]

    frontier = [""]
    observations: dict[str, dict[str, Any]] = {}
    split_events: list[dict[str, Any]] = []
    while len(split_events) < event_budget:
        split_relative = None
        split_route = None
        for relative in sorted(frontier):
            absolute = root_path + relative
            route = c41.route_at_path(ctask, absolute, config)
            if relative not in observations:
                ambient, obligations, _groups = obligation_summary(
                    c41, ctask, route, absolute
                )
                if relative == "":
                    validate_frozen_root(
                        selected, frozen["ambient"], ambient, obligations
                    )
                observations[relative] = {
                    "relative_path": relative,
                    "absolute_path": absolute,
                    "relative_fraction": str(Q(1, 2 ** len(relative))),
                    "absolute_parent_fraction": ambient[
                        "parent_volume_fraction"
                    ],
                    "closed_representative_box": ambient[
                        "closed_representative_box"
                    ],
                    "closed_reflected_box": ambient["closed_reflected_box"],
                    "fresh_ambient_cell_id": ambient[
                        "c41_ambient_cell_id"
                    ],
                    "fresh_ambient_row_sha256": digest(ambient),
                    "route": route_observation(c41, route),
                    "lower_strata_obligations": obligations,
                }
            if c41.disposition_family(route["classification"]) \
                    == "RESIDUAL_OUTER":
                split_relative = relative
                split_route = route
                break
        if split_relative is None:
            break
        absolute = root_path + split_relative
        bits = absolute[len(source_path):]
        history = c41.exact_axis_history(ctask, bits)
        adjacency, children, _axis = c41.split_row(
            ctask, split_route["box"], bits, len(bits), history
        )
        for bit in ("0", "1"):
            child_route = c41.route_at_path(ctask, absolute + bit, config)
            need(
                c41.box_payload(child_route["box"])
                == c41.box_payload(children[int(bit)]),
                "exact split child equals fresh reconstructed route box",
            )
        event_body = {
            "event_ordinal": len(split_events),
            "relative_path": split_relative,
            "absolute_path": absolute,
            "C41_split_face_adjacency": adjacency,
            "C41_split_face_adjacency_row_sha256": digest(adjacency),
            "reason": "RESIDUAL_ROUTE_REQUIRES_ADAPTIVE_REFINEMENT",
            "mathematical_fixed_depth_cap": None,
            "formal_credit": 0,
        }
        split_events.append({
            **event_body, "split_event_object_sha256": digest(event_body)
        })
        frontier.remove(split_relative)
        frontier.extend([split_relative + "0", split_relative + "1"])
        frontier.sort()

    # Ensure every final frontier leaf has a fresh route/obligation transcript.
    for relative in sorted(frontier):
        if relative in observations:
            continue
        absolute = root_path + relative
        route = c41.route_at_path(ctask, absolute, config)
        ambient, obligations, _groups = obligation_summary(
            c41, ctask, route, absolute
        )
        observations[relative] = {
            "relative_path": relative,
            "absolute_path": absolute,
            "relative_fraction": str(Q(1, 2 ** len(relative))),
            "absolute_parent_fraction": ambient["parent_volume_fraction"],
            "closed_representative_box": ambient[
                "closed_representative_box"
            ],
            "closed_reflected_box": ambient["closed_reflected_box"],
            "fresh_ambient_cell_id": ambient["c41_ambient_cell_id"],
            "fresh_ambient_row_sha256": digest(ambient),
            "route": route_observation(c41, route),
            "lower_strata_obligations": obligations,
        }

    final_paths = sorted(frontier)
    need(prefix_free(final_paths), "final adaptive frontier prefix-free")
    kraft = sum((Q(1, 2 ** len(path)) for path in final_paths), Q(0))
    need(kraft == 1, "final adaptive frontier exact relative Kraft one")
    leaves = []
    for relative in final_paths:
        observation = observations[relative]
        obligations = observation["lower_strata_obligations"]
        leaves.append({
            **observation,
            "state": "RESUMABLE_PENDING_ZERO_CREDIT",
            "pending_reason": obligations["first_missing_field"],
            "candidate_exit_emitted": False,
            "formal_credit": 0,
        })
    split_paths = {row["relative_path"] for row in split_events}
    evaluated_nodes = []
    for relative in sorted(observations, key=lambda value: (len(value), value)):
        observation = observations[relative]
        evaluated_nodes.append({
            **observation,
            "adaptive_action": (
                "SPLIT" if relative in split_paths
                else "RETAIN_PENDING_ZERO_CREDIT"
            ),
            "candidate_exit_emitted": False,
            "formal_credit": 0,
        })
    checkpoint_body = {
        "schema": CHECKPOINT_SCHEMA,
        "task_id": selected["task_id"],
        "task_binding_sha256": selected["task_binding_sha256"],
        "event_budget": event_budget,
        "event_budget_exhausted": len(split_events) == event_budget,
        "mathematical_fixed_depth_cap": None,
        "maximum_observed_additional_depth": max(map(len, final_paths)),
        "split_event_count": len(split_events),
        "split_events": split_events,
        "evaluated_node_count": len(evaluated_nodes),
        "evaluated_nodes": evaluated_nodes,
        "frontier_leaf_count": len(leaves),
        "frontier": leaves,
        "relative_paths": final_paths,
        "relative_Kraft_sum": "1",
        "prefix_free": True,
        "all_leaves_pending_zero_credit": True,
        "candidate_exit_count": 0,
        "formal_credit": 0,
    }
    checkpoint = {
        **checkpoint_body,
        "checkpoint_object_sha256": digest(checkpoint_body),
    }
    c43 = c43_capability_check(c41, frozen["plan"])
    result_body = {
        "schema": SCHEMA,
        "status": (
            "PASS_READ_ONLY_C47_PAIR668_EXACT_ROUTE_ADAPTIVE_FEASIBILITY__"
            "PREFIX_FREE_PENDING__ZERO_CREDIT"
        ),
        "source": {
            "path": str(SELF.relative_to(ROOT)),
            "sha256": file_sha256(SELF),
        },
        "frozen_inputs": {
            "C46_A_source_sha256": C46_SOURCE_SHA256,
            "C46_A_64_shard_plan_object_sha256": C46_PLAN_OBJECT_SHA256,
            "C41_source_sha256": C41_SOURCE_SHA256,
            "C41_candidate_object_sha256": C41_OBJECT_SHA256,
            "C42_authority_seal_object_sha256": C42_SEAL_OBJECT_SHA256,
        },
        "selection": {
            "rule": (
                "LEXICOGRAPHIC_FIRST_TASK_IN_PAIR668_OWNER_PREREQUISITE_SUBQUEUE"
            ),
            "pair_index": DEFAULT_PAIR,
            "pair_owner_prerequisite_task_count": len(
                frozen["selected_group"]
            ),
            "task_id": selected["task_id"],
            "task_binding_sha256": selected["task_binding_sha256"],
            "primary_family": selected["primary_family"],
            "primary_outer_id": selected["primary_outer_id"],
            "ambient_cell_id": selected["ambient_cell_id"],
            "descendant_path": root_path,
            "C40_source_leaf_id": frozen["source"]["c40_leaf_id"],
            "C40_source_row_sha256": frozen["source"]["row_sha256"],
            "C40_source_path": source_path,
            "unblocks_sole_deficit_pairs": selected["queue"][
                "unblocks_sole_deficit_pairs"
            ],
        },
        "C43_existing_helper_scope": c43,
        "adaptive_probe": checkpoint,
        "exact_stop": {
            "selected_root_first_missing_field": observations[""][
                "lower_strata_obligations"
            ]["first_missing_field"],
            "first_live_frontier_path": next(
                (row["absolute_path"] for row in leaves
                 if row["route"]["disposition_family"] == "RESIDUAL_OUTER"),
                None,
            ),
            "first_live_route_blocker": next(
                (row["lower_strata_obligations"]["route_blockers"][0]
                 for row in leaves
                 if row["lower_strata_obligations"]["route_blockers"]),
                None,
            ),
            "first_explicit_global_owner_blocker": next(
                (row["lower_strata_obligations"]["global_owner_blockers"][0]
                 for row in evaluated_nodes
                 if row["lower_strata_obligations"][
                     "global_owner_blockers"]),
                None,
            ),
            "first_terminal_certificate_blocker": next(
                (row["lower_strata_obligations"]["certificate_blockers"][0]
                 for row in leaves
                 if row["lower_strata_obligations"][
                     "certificate_blockers"]),
                None,
            ),
            "existing_C41_C43_global_owner_certificate_available": False,
            "resource_budget_may_only_return_pending": True,
            "candidate_exit_emitted": False,
            "formal_credit": 0,
        },
        "strict_nonpromotion": {
            "runtime_write_code_path_exists": False,
            "runtime_writes_performed": False,
            "candidate_created": False,
            "pointer_receipt_seal_or_status_changed": False,
            "producer_or_auditor_run": False,
            "formal_credit": 0,
            "D02_A_complete": False,
        },
    }
    return {**result_body, "object_sha256": digest(result_body)}


def expect_rejected(function: Any, label: str) -> None:
    try:
        function()
    except Rejected:
        return
    raise Rejected("self-test expected rejection:" + label)


def self_test() -> dict[str, Any]:
    tests: list[str] = []
    need(digest({"b": 1, "a": 2}) == digest({"a": 2, "b": 1}),
         "canonical key order")
    tests.append("canonical JSON key order")
    need(prefix_free(["0", "10", "11"]), "prefix-free positive")
    tests.append("prefix-free positive")
    need(not prefix_free(["0", "01"]), "prefix-free negative")
    tests.append("prefix-free negative")
    need(sum((Q(1, 2), Q(1, 4), Q(1, 4)), Q(0)) == 1,
         "exact Fraction Kraft")
    tests.append("exact Fraction Kraft")
    expect_rejected(lambda: need(False, "synthetic"), "need false")
    tests.append("fail-closed need")
    expect_rejected(lambda: run_probe(0), "zero event budget")
    tests.append("zero event budget rejected before full replay")
    expect_rejected(lambda: run_probe(65), "oversized event budget")
    tests.append("oversized event budget rejected before full replay")
    need(HEX64.fullmatch(C46_SOURCE_SHA256) is not None
         and HEX64.fullmatch(C46_PLAN_OBJECT_SHA256) is not None,
         "frozen C46 pins shape")
    tests.append("frozen C46 pin shape")
    need(DEFAULT_PAIR == 668 and EXPECTED_PAIR_TASK_COUNT == 43,
         "default owner-prerequisite selection")
    tests.append("pair-668 selection constants")
    need(file_sha256(C46_SOURCE) == C46_SOURCE_SHA256
         and file_sha256(C41_SOURCE) == C41_SOURCE_SHA256,
         "frozen source bytes")
    tests.append("frozen source byte pins")
    body = {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C47_READ_ONLY_ZERO_CREDIT_SELF_TEST",
        "test_count": len(tests),
        "tests": tests,
        "full_inventory_read": False,
        "numerical_probe_run": False,
        "runtime_writes_performed": False,
        "formal_credit": 0,
    }
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--probe", action="store_true")
    parser.add_argument("--event-budget", type=int, default=4)
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            need(arguments.event_budget == 4,
                 "self-test does not accept a probe event budget")
            value = self_test()
        else:
            value = run_probe(arguments.event_budget)
        emit(value)
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError) as error:
        body = {
            "schema": SCHEMA + ".fail-closed-error",
            "status": "REJECTED",
            "error_class": type(error).__name__,
            "reason": str(error),
            "runtime_writes_performed": False,
            "formal_credit": 0,
        }
        emit({**body, "error_object_sha256": digest(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
