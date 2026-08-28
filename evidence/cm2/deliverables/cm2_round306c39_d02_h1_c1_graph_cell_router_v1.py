#!/usr/bin/env python3
"""C39: exact H1 and collision-one graph-cell routing over the C38 frontier."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import flint
from flint import arb, ctx

import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c39.d02-h1-c1-graph-cell-router.v1"
LEAF_SCHEMA = "cm2.round306c39.routed-child-pair.v1"
PARENT_SCHEMA = "cm2.round306c39.parent-conservation.v1"
PRECISION_BITS = 384
WORKER_BATCH_SIZE = 40

EXPECTED_C38_OBJECT = "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434"
EXPECTED_C38_AUDIT_OBJECT = (
    "5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2"
)
EXPECTED_C38_SOURCE = "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d"
EXPECTED_ROUND185_SOURCE = (
    "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
)
EXPECTED_NUMERIC_SOURCES = {
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
}
FROZEN_OWNER = "W[1,0]"
TARGET_H1 = "UNRESOLVED_COLLISION1_OUTGOING_CHART_SEAM_OVERWRAP"
TARGET_C1 = {
    "UNRESOLVED_COLLISION1_UNTYPED_DISCRIMINANT_COLLAR",
    "UNRESOLVED_COLLISION1_TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
    "UNRESOLVED_COLLISION1_TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{path}:{key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda item: (_ for _ in ()).throw(ValueError(item)),
        parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)),
    )
    require(type(value) is dict, f"top object:{path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def validate_object(
    value: dict[str, Any], field: str, expected: str, label: str,
) -> None:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(recorded == expected == digest(semantic), f"object:{label}")


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"manifest duplicate:{name}")
        names.append(name)
        path = directory / name
        require(path.is_file() and file_sha256(path) == expected, f"manifest:{path}")
    require(names == sorted(names), f"manifest order:{directory}")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir() if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> "LedgerWriter":
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> None:
        require("row_sha256" not in row, "writer row open")
        row_sha = digest(row)
        self.stream.write(canonical({**row, "row_sha256": row_sha}) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


def source_pins() -> dict[str, str]:
    values = {
        "C38": file_sha256(Path(c38.__file__).resolve()),
        "Round185": file_sha256(Path(round185.__file__).resolve()),
        "r178": file_sha256(Path(round185.r178.__file__).resolve()),
        "atlas": file_sha256(Path(round185.atlas.__file__).resolve()),
        "ge": file_sha256(Path(round185.ge.__file__).resolve()),
        "registry": file_sha256(Path(round185.registry.__file__).resolve()),
    }
    require(values["C38"] == EXPECTED_C38_SOURCE, "C38 source pin")
    require(values["Round185"] == EXPECTED_ROUND185_SOURCE, "Round185 source pin")
    for name, expected in EXPECTED_NUMERIC_SOURCES.items():
        require(values[name] == expected, f"numeric source pin:{name}")
    require(flint.__version__ == "0.9.0", "python-flint version")
    return values


def box_from_child(row: dict[str, Any]) -> Any:
    payload = row["representative_box"]
    require(payload is not None, "rational child box")
    return round185.atlas.AtlasBox(
        Q(payload["t"][0]),
        Q(payload["t"][1]),
        Q(payload["p"][0]),
        Q(payload["p"][1]),
        Q(payload["s"][0]),
        Q(payload["s"][1]),
        row["relative_depth"],
        row["path"],
    )


def sign_name(value: arb) -> str:
    sign = round185.strict_sign(value)
    return "POSITIVE" if sign > 0 else "NEGATIVE" if sign < 0 else "UNRESOLVED"


def arb_payload(value: arb) -> dict[str, Any]:
    return {
        "lower": str(value.lower()),
        "upper": str(value.upper()),
        "sign": sign_name(value),
    }


def collision0_delta(parent_key: str, box: Any, target: str) -> Any:
    return round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)[
        "Delta"
    ]


def collision0_distance_margin(parent_key: str, box: Any, target: str) -> Any:
    raw = round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)
    return raw["ell"] * raw["ell"] - raw["Delta"]


def h1_route(parent_key: str, box: Any) -> dict[str, Any]:
    try:
        full, normal_x, normal_y = round185.collision1_h1_ad(
            parent_key, box, FROZEN_OWNER
        )
        centered = round185.centered_enclosure(
            round185.collision1_h1_ad,
            parent_key,
            box,
            FROZEN_OWNER,
            full,
        )
    except Exception as error:
        return {
            "kind": "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED",
            "error_type": type(error).__name__,
            "chart": None,
        }
    side_sign = round185.strict_sign(centered)
    method = "CENTERED_MEAN_VALUE_STRICT_SIDE" if side_sign else None
    graph_axis: str | None = None
    face_evidence: list[dict[str, Any]] = []
    for axis, (name, lower, upper) in enumerate(
        (("t", box.t0, box.t1), ("p", box.p0, box.p1))
    ):
        derivative = full.derivative[axis]
        derivative_sign = round185.strict_sign(derivative)
        if derivative_sign == 0:
            continue
        low = round185.collision1_h1_ad(
            parent_key,
            round185.fixed_axis_box(box, axis, lower, f".c39-{name}-lower"),
            FROZEN_OWNER,
        )[0].value
        high = round185.collision1_h1_ad(
            parent_key,
            round185.fixed_axis_box(box, axis, upper, f".c39-{name}-upper"),
            FROZEN_OWNER,
        )[0].value
        low_sign = round185.strict_sign(low)
        high_sign = round185.strict_sign(high)
        face_evidence.append(
            {
                "axis": name,
                "derivative": arb_payload(derivative),
                "lower_face": arb_payload(low),
                "upper_face": arb_payload(high),
            }
        )
        if side_sign == 0 and low_sign != 0 and low_sign == high_sign:
            side_sign = low_sign
            method = f"MONOTONE_{name.upper()}_SAME_SIGN_STRICT_SIDE"
        if graph_axis is None and low_sign * high_sign < 0:
            graph_axis = name
    normal_signs = {
        "nx": sign_name(normal_x.value),
        "ny": sign_name(normal_y.value),
    }
    chart: str | None = None
    if side_sign > 0 and normal_signs["nx"] != "UNRESOLVED":
        chart = "E" if normal_signs["nx"] == "POSITIVE" else "W"
    elif side_sign < 0 and normal_signs["ny"] != "UNRESOLVED":
        chart = "N" if normal_signs["ny"] == "POSITIVE" else "S"
    if side_sign != 0:
        kind = "STRICT_SIDE" if chart is not None else "STRICT_H1_UNKNOWN_NORMAL_SIGN"
    elif graph_axis is not None:
        kind = "REGULAR_FULL_FACE_GRAPH"
    elif any(
        round185.strict_sign(full.derivative[index]) != 0 for index in (0, 1)
    ):
        kind = "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED"
    else:
        kind = "SINGULAR_OR_MULTI_GRAPH_ARRANGEMENT_REQUIRED"
    return {
        "kind": kind,
        "method": method,
        "chart": chart,
        "H1_centered": arb_payload(centered),
        "H1_natural": arb_payload(full.value),
        "normal_signs": normal_signs,
        "graph_axis": graph_axis,
        "face_evidence": face_evidence,
    }


def reconstruct_box(cell: dict[str, Any], path: str) -> tuple[Any, tuple[str, ...]]:
    t_values = cell["physical_t_interval"]
    require(all(value["kind"] == "RATIONAL" for value in t_values), "rational C1 cell")
    box = c38.round166.ge.AtlasBox(
        Q(t_values[0]["value"]),
        Q(t_values[1]["value"]),
        Q(cell["physical_p_interval"][0]),
        Q(cell["physical_p_interval"][1]),
        Q(0),
        Q(0),
        0,
        "",
    )
    active_targets = tuple(cell["source_lineage"]["active_candidates"])
    for bit in path:
        stage_one, _records = c38.round166.classify_active(
            cell["gate3_chart"], box, active_targets
        )
        if stage_one.classification == "unique_first":
            active_targets = (FROZEN_OWNER,)
        elif stage_one.classification != "tangency_graph":
            active_targets = stage_one.active_targets
        box = c38.round166.split_axis(
            box, c38.round166.longest_axis(box)
        )[int(bit)]
    return box, active_targets


def enhanced_record(
    parent_key: str, box: Any, record: Any,
) -> tuple[Any, dict[str, Any] | None]:
    if record.classification not in {
        "unresolved_discriminant",
        "unresolved_root_sign",
    }:
        return record, None
    raw = round185.ad_root(
        round185.ad_initial_geometry(parent_key, box), record.target_id
    )
    delta = round185.centered_enclosure(
        collision0_delta,
        parent_key,
        box,
        record.target_id,
        raw["Delta"],
    )
    delta_sign = round185.strict_sign(delta)
    evidence: dict[str, Any] = {
        "target_id": record.target_id,
        "input_classification": record.classification,
        "centered_Delta": arb_payload(delta),
        "tp_derivatives": {
            "dt": arb_payload(raw["Delta"].derivative[0]),
            "dp": arb_payload(raw["Delta"].derivative[1]),
        },
        "output_classification": record.classification,
        "stable_near_margin": None,
    }
    if delta_sign < 0:
        replacement = c38.round166.ge.RootRecord(
            record.target_id,
            "no_real_intersection",
            raw["ell"].value,
            delta,
            None,
            None,
            raw["transverse"].value,
        )
        evidence["output_classification"] = replacement.classification
        return replacement, evidence
    if delta_sign == 0:
        return record, evidence
    radical = delta.sqrt()
    ell = raw["ell"].value
    near = ell - radical
    far = ell + radical
    stable_margin_payload: dict[str, Any] | None = None
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        distance_full = collision0_distance_margin(
            parent_key, box, record.target_id
        )
        distance = round185.centered_enclosure(
            collision0_distance_margin,
            parent_key,
            box,
            record.target_id,
            distance_full,
        )
        stable_margin_payload = arb_payload(distance)
        if bool(ell > 0) and bool(far > 0) and bool(distance > 0):
            classification = "strict_future_root"
            near = distance / far
        else:
            classification = "unresolved_root_sign"
    replacement = c38.round166.ge.RootRecord(
        record.target_id,
        classification,
        ell,
        delta,
        near,
        far,
        raw["transverse"].value,
    )
    evidence["output_classification"] = classification
    evidence["stable_near_margin"] = stable_margin_payload
    return replacement, evidence


def downstream_route(
    row: dict[str, Any],
    box: Any,
    original_path: list[dict[str, Any]],
    reflected_path: list[dict[str, Any]],
    pair_index: dict[Any, Any],
    pattern_index: dict[Any, Any],
    cores: tuple[Any, ...],
) -> tuple[str, str, int]:
    chart_id = ":".join(row["representative_origin_key"].split(":")[:2])
    return c38.stage_two_route(
        chart_id,
        box,
        original_path,
        reflected_path,
        pair_index,
        pattern_index,
        cores,
    )


def routed_classification(prefix: str, route: str) -> str:
    if route.startswith("EXCLUDED_"):
        return "EXCLUDED_C39_" + prefix + "_" + route.removeprefix("EXCLUDED_")
    if route.startswith("LIVE_"):
        return "UNRESOLVED_C39_" + prefix + "_" + route + "_NEEDS_COLLISION3_1648"
    return "UNRESOLVED_C39_" + prefix + "_" + route.removeprefix("UNRESOLVED_")


def route_h1_task(task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    row = task["row"]
    box = box_from_child(row)
    evidence = h1_route(row["representative_origin_key"], box)
    chart = evidence["chart"]
    if evidence["kind"] == "STRICT_SIDE" and chart != "W":
        classification = "EXCLUDED_C39_H1_OUTGOING_CHART_MISMATCH"
        witness = f"strict collision-one outgoing chart {chart}"
    elif evidence["kind"] == "STRICT_SIDE" and chart == "W":
        route, witness, _collision = downstream_route(
            row,
            box,
            config["original_path"],
            config["reflected_path"],
            config["pair_index"],
            config["pattern_index"],
            config["cores"],
        )
        classification = routed_classification("H1_W_SIDE", route)
    elif evidence["kind"] == "REGULAR_FULL_FACE_GRAPH":
        classification = "UNRESOLVED_C39_H1_REGULAR_FULL_FACE_GRAPH_CELL"
        witness = f"implicit H1 graph over {evidence['graph_axis']}"
    elif evidence["kind"] == "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED":
        classification = "UNRESOLVED_C39_H1_SOURCE_GRAZING_ENDPOINT_CHART"
        witness = evidence["error_type"]
    else:
        classification = "UNRESOLVED_C39_H1_BOUNDARY_ARRANGEMENT"
        witness = evidence["kind"]
    return {
        "task_id": task["task_id"],
        "classification": classification,
        "route_method": evidence["kind"],
        "witness": witness,
        "surface_evidence": evidence,
    }


def route_c1_task(task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    row = task["row"]
    cell = task["cell"]
    box, active_targets = reconstruct_box(cell, row["path"])
    stage_one, records = c38.round166.classify_active(
        cell["gate3_chart"], box, active_targets
    )
    enhanced: list[Any] = []
    evidence_rows: list[dict[str, Any]] = []
    for record in records:
        replacement, evidence = enhanced_record(
            row["representative_origin_key"], box, record
        )
        enhanced.append(replacement)
        if evidence is not None:
            evidence_rows.append(evidence)
    leaf = c38.round166.classify_from_records(
        cell["gate3_chart"], box, enhanced
    )
    unresolved_records = [
        record
        for record in enhanced
        if record.classification in {
            "unresolved_discriminant",
            "unresolved_root_sign",
        }
    ]
    h1_evidence: dict[str, Any] | None = None
    witness = leaf.reason
    if leaf.classification == "no_future_root":
        classification = "EXCLUDED_C39_C1_NO_FUTURE_ROOT"
        method = "CENTERED_C1_STAGE_ONE_EXCLUSION"
    elif leaf.classification == "unique_first" and leaf.owner_target != FROZEN_OWNER:
        classification = "EXCLUDED_C39_C1_UNIQUE_FIRST_OWNER_MISMATCH"
        method = "CENTERED_C1_STAGE_ONE_EXCLUSION"
        witness = str(leaf.owner_target)
    elif leaf.classification == "unique_first" and leaf.owner_target == FROZEN_OWNER:
        h1_evidence = h1_route(row["representative_origin_key"], box)
        chart = h1_evidence["chart"]
        if h1_evidence["kind"] == "STRICT_SIDE" and chart != "W":
            classification = "EXCLUDED_C39_C1_OUTGOING_CHART_MISMATCH"
            method = "CENTERED_C1_H1_EXCLUSION"
            witness = f"strict collision-one outgoing chart {chart}"
        elif h1_evidence["kind"] == "STRICT_SIDE" and chart == "W":
            route, witness, _collision = downstream_route(
                row,
                box,
                config["original_path"],
                config["reflected_path"],
                config["pair_index"],
                config["pattern_index"],
                config["cores"],
            )
            classification = routed_classification("C1_ENHANCED_W_SIDE", route)
            method = "CENTERED_C1_TO_DOWNSTREAM_ROUTE"
        else:
            classification = "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY"
            method = "CENTERED_C1_H1_GRAPH_ROUTER"
            witness = h1_evidence["kind"]
    else:
        regular_surfaces = sum(
            any(
                item["tp_derivatives"][axis]["sign"] != "UNRESOLVED"
                for axis in ("dt", "dp")
            )
            for item in evidence_rows
            if item["output_classification"]
            in {"unresolved_discriminant", "unresolved_root_sign"}
        )
        if unresolved_records and regular_surfaces == len(unresolved_records):
            classification = "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT"
            method = "CENTERED_C1_REGULAR_GRAPH_REGISTRY"
        else:
            classification = "UNRESOLVED_C39_C1_SINGULAR_OR_ORDER_ARRANGEMENT"
            method = "CENTERED_C1_RESIDUAL_REGISTRY"
    return {
        "task_id": task["task_id"],
        "classification": classification,
        "route_method": method,
        "witness": witness,
        "surface_evidence": {
            "input_stage_one_classification": stage_one.classification,
            "enhanced_stage_one_classification": leaf.classification,
            "enhanced_owner_target": leaf.owner_target,
            "remaining_unresolved_record_count": len(unresolved_records),
            "root_surfaces": evidence_rows,
            "H1": h1_evidence,
        },
    }


def worker(input_path: Path, output_path: Path) -> None:
    source_pins()
    ctx.prec = PRECISION_BITS
    c38.round166.install_fast_readonly_replay()
    payload = strict_json(input_path)
    config = payload["config"]
    config["pair_index"] = {
        tuple(key.split("\u001f")): value
        for key, value in config["pair_index"].items()
    }
    config["pattern_index"] = {
        tuple(key.split("\u001f")): value
        for key, value in config["pattern_index"].items()
    }
    config["cores"] = tuple(c38.round139.lower.core_cert.physical_cores())
    rows = []
    for task in payload["tasks"]:
        if task["kind"] == "H1":
            rows.append(route_h1_task(task, config))
        else:
            rows.append(route_c1_task(task, config))
    write_json(output_path, {"schema": SCHEMA + ".worker", "rows": rows})


def encode_tuple_map(value: dict[tuple[str, ...], int]) -> dict[str, int]:
    return {"\u001f".join(key): item for key, item in value.items()}


def run_workers(
    stage: Path,
    tasks: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    work = stage / ".worker"
    work.mkdir()
    results: dict[str, dict[str, Any]] = {}
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(DELIVERABLES) + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH")
        else ""
    )
    for batch_index, start in enumerate(range(0, len(tasks), WORKER_BATCH_SIZE)):
        input_path = work / f"input-{batch_index:04d}.json"
        output_path = work / f"output-{batch_index:04d}.json"
        write_json(
            input_path,
            {
                "schema": SCHEMA + ".worker-input",
                "config": config,
                "tasks": tasks[start : start + WORKER_BATCH_SIZE],
            },
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker-input",
                str(input_path),
                "--worker-output",
                str(output_path),
            ],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            completed.returncode == 0,
            "worker failure:"
            + str(batch_index)
            + ":"
            + completed.stderr.decode("utf-8", "replace")[-2000:],
        )
        output = strict_json(output_path)
        for row in output["rows"]:
            require(row["task_id"] not in results, "duplicate worker task")
            results[row["task_id"]] = row
    require(len(results) == len(tasks), "worker result census")
    shutil.rmtree(work)
    return results


def build(output: Path, candidate: Path, audit_path: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    pins = source_pins()
    validate_manifest(candidate)
    c38_result = strict_json(candidate / "result.json")
    validate_object(c38_result, "object_sha256", EXPECTED_C38_OBJECT, "C38")
    audit = strict_json(audit_path)
    validate_object(audit, "object_sha256", EXPECTED_C38_AUDIT_OBJECT, "C38 audit")
    require(
        audit["candidate_object_sha256"] == EXPECTED_C38_OBJECT
        and audit["status"]
        == "PASS_INDEPENDENT_C38_RECONSTRUCTION__16_OF_16_ATTACKS_FAIL_CLOSED",
        "C38 audit binding",
    )
    c38_children = c38.read_ledger(
        candidate, c38_result["ledgers"]["collision1_2_child_pairs"]
    )
    c38_parents = c38.read_ledger(
        candidate, c38_result["ledgers"]["representative_parent_conservation"]
    )
    require(len(c38_children) == 10486 and len(c38_parents) == 862, "C38 census")
    c37 = (ROOT / c38_result["C37_authority"]["path"]).resolve()
    c37_result = strict_json(c37 / "result.json")
    c36 = (ROOT / c37_result["C36_authority"]["path"]).resolve()
    c36_result = strict_json(c36 / "result.json")
    c35 = (ROOT / c36_result["C35_authority"]["path"]).resolve()
    c34 = (ROOT / c36_result["C34_authority"]["path"]).resolve()
    c35_result = strict_json(c35 / "result.json")
    c34_result = strict_json(c34 / "result.json")
    c32 = (ROOT / c34_result["C32_authority"]["path"]).resolve()
    c32_result = strict_json(c32 / "result.json")
    original_path = c38.read_ledger(
        c35, c35_result["ledgers"]["path_occurrences"]
    )[:2]
    reflected_path = c38.read_ledger(
        c37, c37_result["ledgers"]["reflected_r1648_occurrences"]
    )[:2]
    targeted_ids = {
        row["representative_cell_id"]
        for row in c38_children
        if row["classification"] in TARGET_C1
    }
    cells = {
        row["cell_id"]: row
        for row in c38.read_ledger(c32, c32_result["ledgers"]["cells"])
        if row["cell_id"] in targeted_ids
    }
    require(set(cells) == targeted_ids, "targeted cell inventory")
    pair_index, pattern_index, registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    config = {
        "original_path": original_path,
        "reflected_path": reflected_path,
        "pair_index": encode_tuple_map(pair_index),
        "pattern_index": encode_tuple_map(pattern_index),
    }
    tasks: list[dict[str, Any]] = []
    for row in c38_children:
        classification = row["classification"]
        if classification == TARGET_H1:
            tasks.append(
                {
                    "task_id": row["refinement_child_pair_id"],
                    "kind": "H1",
                    "row": row,
                }
            )
        elif classification in TARGET_C1:
            tasks.append(
                {
                    "task_id": row["refinement_child_pair_id"],
                    "kind": "C1",
                    "row": row,
                    "cell": cells[row["representative_cell_id"]],
                }
            )
    require(len(tasks) == 2896, f"target task census:{len(tasks)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        worker_results = run_workers(stage, tasks, config)
        routed_writer = LedgerWriter(
            stage / "routed_child_pairs.jsonl.gz",
            "C38_CHILD_LEDGER_ORDER",
        )
        parent_writer = LedgerWriter(
            stage / "parent_conservation.jsonl.gz",
            "PAIR_INDEX_ASCENDING",
        )
        rows_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
        classifications: Counter[str] = Counter()
        methods: Counter[str] = Counter()
        with routed_writer:
            for source in c38_children:
                task_id = source.get(
                    "refinement_child_pair_id", "c38-row:" + source["row_sha256"]
                )
                replacement = worker_results.get(task_id)
                if replacement is None:
                    classification = source["classification"]
                    method = (
                        "C38_EXISTING_TERMINAL"
                        if classification.startswith("EXCLUDED_")
                        else "C38_UNTOUCHED_RESIDUAL"
                    )
                    witness = source["witness"]
                    evidence = None
                else:
                    classification = replacement["classification"]
                    method = replacement["route_method"]
                    witness = replacement["witness"]
                    evidence = replacement["surface_evidence"]
                terminal = classification.startswith("EXCLUDED_")
                semantic = {
                    "schema": LEAF_SCHEMA,
                    "pair_index": source["pair_index"],
                    "c38_child_pair_id": task_id,
                    "c38_child_row_sha256": source["row_sha256"],
                    "representative_cell_id": source["representative_cell_id"],
                    "reflected_cell_id": source["reflected_cell_id"],
                    "relative_depth": source["relative_depth"],
                    "path": source["path"],
                    "parent_volume_fraction": source["parent_volume_fraction"],
                    "representative_box": source["representative_box"],
                    "reflected_box": source["reflected_box"],
                    "source_classification": source["classification"],
                    "classification": classification,
                    "route_method": method,
                    "witness": witness,
                    "surface_evidence": evidence,
                    "reflection_transport_materialized": source[
                        "reflection_transport_materialized"
                    ],
                    "round144_terminal_class": (
                        "EARLIEST_PREFIX_EXCLUDED"
                        if terminal
                        else "UNRESOLVED_R1648_CONTINUATION"
                    ),
                    "local_round144_terminal_credit": 1 if terminal else 0,
                    "C34_common_refinement_credit": 0,
                    "D02_gate_credit": 0,
                }
                semantic["c39_routed_child_pair_id"] = "c39-routed:" + digest(semantic)
                routed_writer.write(semantic)
                rows_by_pair[source["pair_index"]].append(semantic)
                classifications[classification] += 1
                methods[method] += 1

        c38_parent_index = {row["pair_index"]: row for row in c38_parents}
        full_count = 0
        partial_count = 0
        zero_count = 0
        terminal_equivalent = Q(0)
        unresolved_equivalent = Q(0)
        newly_full = 0
        with parent_writer:
            for pair_number in range(862):
                rows = rows_by_pair[pair_number]
                require(bool(rows), f"pair rows:{pair_number}")
                terminal = sum(
                    (
                        Q(row["parent_volume_fraction"])
                        for row in rows
                        if row["classification"].startswith("EXCLUDED_")
                    ),
                    Q(0),
                )
                unresolved = Q(1) - terminal
                require(terminal >= 0 and unresolved >= 0, "parent conservation")
                whole = terminal == 1
                if whole:
                    full_count += 1
                elif terminal == 0:
                    zero_count += 1
                else:
                    partial_count += 1
                c38_parent = c38_parent_index[pair_number]
                if whole and not c38_parent["whole_representative_parent_terminal"]:
                    newly_full += 1
                terminal_equivalent += terminal
                unresolved_equivalent += unresolved
                parent_writer.write(
                    {
                        "schema": PARENT_SCHEMA,
                        "pair_index": pair_number,
                        "c38_parent_row_sha256": c38_parent["row_sha256"],
                        "leaf_count": len(rows),
                        "terminal_excluded_parent_volume": str(terminal),
                        "unresolved_parent_volume": str(unresolved),
                        "parent_volume_conservation": "1",
                        "whole_representative_parent_terminal": whole,
                        "whole_reflected_parent_terminal": whole,
                        "newly_whole_terminal_vs_C38": (
                            whole
                            and not c38_parent[
                                "whole_representative_parent_terminal"
                            ]
                        ),
                        "C34_common_refinement_credit": 2 if whole else 0,
                        "D02_gate_credit": 0,
                    }
                )
        require(
            full_count + partial_count + zero_count == 862
            and terminal_equivalent + unresolved_equivalent == 862,
            "global conservation",
        )
        require(full_count >= 156 and newly_full == full_count - 156, "monotone credit")
        formal_excluded = 74812 + 2 * full_count
        formal_unresolved = 1724 - 2 * full_count
        (stage / "PARTIAL_GRAPH_ROUTER_ONLY.lock").write_text(
            "C39 routes only the current H1 and collision-one discriminant collars. "
            "Whole-parent terminal credit is granted only after exact C38 Kraft "
            "conservation; partial volume, regular graph cells, collision-two owner "
            "collars, algebraic chart boundaries, and collisions three through 1648 "
            "remain nonpromotional. D02/D03/D04/Gate5/CM2 credit is forbidden.\n",
            encoding="utf-8",
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                f"PASS_C39_H1_C1_GRAPH_ROUTER__{len(tasks)}_TARGETED_LEAVES__"
                f"{2 * full_count}_WHOLE_CELLS_TERMINAL__"
                f"{formal_unresolved}_FORMAL_UNRESOLVED"
            ),
            "C38_authority": {
                "path": str(candidate.resolve().relative_to(ROOT)),
                "object_sha256": c38_result["object_sha256"],
                "independent_audit_path": str(audit_path.resolve().relative_to(ROOT)),
                "independent_audit_object_sha256": audit["object_sha256"],
            },
            "numeric_authority": {
                "source_sha256": pins,
                "flint_version": flint.__version__,
                "precision_bits": PRECISION_BITS,
                "worker_batch_size": WORKER_BATCH_SIZE,
                "official_registry_sha256": registry_sha,
                "source_slice": "s=0",
            },
            "router_census": {
                "C38_child_pair_count": len(c38_children),
                "targeted_H1_leaf_count": sum(
                    row["classification"] == TARGET_H1 for row in c38_children
                ),
                "targeted_collision1_leaf_count": sum(
                    row["classification"] in TARGET_C1 for row in c38_children
                ),
                "targeted_leaf_count": len(tasks),
                "classification_census": dict(sorted(classifications.items())),
                "route_method_census": dict(sorted(methods.items())),
                "representative_terminal_parent_equivalent": str(
                    terminal_equivalent
                ),
                "representative_unresolved_parent_equivalent": str(
                    unresolved_equivalent
                ),
                "whole_terminal_representative_parent_count": full_count,
                "whole_terminal_paired_coarse_cell_count": 2 * full_count,
                "newly_whole_terminal_representative_parent_count": newly_full,
                "newly_whole_terminal_paired_coarse_cell_count": 2 * newly_full,
                "partial_representative_parent_count": partial_count,
                "zero_progress_representative_parent_count": zero_count,
            },
            "ledgers": {
                "routed_child_pairs": routed_writer.descriptor(),
                "parent_conservation": parent_writer.descriptor(),
            },
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "EARLIEST_PREFIX_EXCLUDED": formal_excluded,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": formal_unresolved,
                "terminal_total": 76832,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "C34_common_refined_cell_count": 2 * full_count,
                "C34_unresolved_R1648_continuations": formal_unresolved,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": f"BLOCKED_BY_{formal_unresolved}_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "complete the H1 boundary/intersection cells, source-grazing and "
                "algebraic endpoint charts, then construct the collision-two multi-Delta "
                "graph arrangement for every surviving representative and continue "
                "collisions 3--1648"
            ),
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        stage.rename(output)
        return result
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--worker-input", type=Path)
    parser.add_argument("--worker-output", type=Path)
    arguments = parser.parse_args()
    if arguments.worker_input is not None:
        require(arguments.worker_output is not None, "worker output")
        worker(arguments.worker_input.resolve(), arguments.worker_output.resolve())
        return 0
    require(arguments.output is not None, "output")
    candidate = arguments.candidate or (
        RUNTIME
        / "candidates"
        / (RUNTIME / "c38-current-token").read_text(encoding="utf-8").strip()
    )
    audit_path = arguments.audit or (
        RUNTIME
        / "audit"
        / (RUNTIME / "c38-current-audit-token").read_text(encoding="utf-8").strip()
        / "independent_audit.json"
    )
    result = build(
        arguments.output.resolve(), candidate.resolve(), audit_path.resolve()
    )
    print(canonical(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
