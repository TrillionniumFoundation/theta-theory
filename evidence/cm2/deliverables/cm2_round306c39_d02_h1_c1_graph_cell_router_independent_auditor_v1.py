#!/usr/bin/env python3
"""Independent formal-credit auditor for the C39 graph-cell router."""

from __future__ import annotations

import argparse
import copy
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
from flint import ctx

import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c39.d02-h1-c1-graph-cell-router.independent-audit.v1"
PRODUCER = DELIVERABLES / "cm2_round306c39_d02_h1_c1_graph_cell_router_v1.py"
EXPECTED_PRODUCER_SOURCE = (
    "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae"
)
EXPECTED_CANDIDATE_OBJECT = (
    "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02"
)
EXPECTED_CANDIDATE_STATUS = (
    "PASS_C39_H1_C1_GRAPH_ROUTER__2896_TARGETED_LEAVES__"
    "322_WHOLE_CELLS_TERMINAL__1402_FORMAL_UNRESOLVED"
)
EXPECTED_C38_OBJECT = "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434"
EXPECTED_C38_AUDIT_OBJECT = (
    "5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2"
)
PRECISION_BITS = 384
WORKER_BATCH_SIZE = 40
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


def semantic_guard(result: dict[str, Any]) -> None:
    require(result["schema"] == "cm2.round306c39.d02-h1-c1-graph-cell-router.v1", "schema")
    require(result["status"] == EXPECTED_CANDIDATE_STATUS, "status")
    require(result["C38_authority"]["object_sha256"] == EXPECTED_C38_OBJECT, "C38")
    require(
        result["C38_authority"]["independent_audit_object_sha256"]
        == EXPECTED_C38_AUDIT_OBJECT,
        "C38 audit",
    )
    census = result["router_census"]
    require(
        census["C38_child_pair_count"] == 10486
        and census["targeted_H1_leaf_count"] == 738
        and census["targeted_collision1_leaf_count"] == 2158
        and census["targeted_leaf_count"] == 2896
        and census["whole_terminal_representative_parent_count"] == 161
        and census["whole_terminal_paired_coarse_cell_count"] == 322
        and census["newly_whole_terminal_representative_parent_count"] == 5
        and census["newly_whole_terminal_paired_coarse_cell_count"] == 10
        and census["partial_representative_parent_count"] == 311
        and census["zero_progress_representative_parent_count"] == 390
        and census["representative_terminal_parent_equivalent"] == "2355/8"
        and census["representative_unresolved_parent_equivalent"] == "4541/8",
        "router census",
    )
    terminal = result["round144_terminal_census"]
    require(
        terminal
        == {
            "CONNECTED_TO_KNOWN": 0,
            "EARLIEST_PREFIX_EXCLUDED": 75134,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": 1402,
            "terminal_total": 76832,
            "unresolved_zero": False,
        },
        "terminal census",
    )
    nonpromotion = result["strict_nonpromotion"]
    require(
        nonpromotion["C34_common_refined_cell_count"] == 322
        and nonpromotion["C34_unresolved_R1648_continuations"] == 1402
        and nonpromotion["D02"]
        == "BLOCKED_BY_1402_COMPLETE_R1648_CONTINUATIONS"
        and nonpromotion["D03"] == "UNAUTHORIZED"
        and nonpromotion["D04"] == "NOT_MINTED"
        and nonpromotion["Gate5"] == "10/18"
        and nonpromotion["complete_global_18_field_blocks"] == 0
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "nonpromotion",
    )
    require(
        result["numeric_authority"]["precision_bits"] == PRECISION_BITS
        and result["numeric_authority"]["flint_version"] == "0.9.0"
        and result["numeric_authority"]["worker_batch_size"] == 40,
        "numeric authority",
    )
    require(
        result["ledgers"]["routed_child_pairs"]["row_count"] == 10486
        and result["ledgers"]["parent_conservation"]["row_count"] == 862,
        "ledger counts",
    )


def attack_suite(result: dict[str, Any]) -> dict[str, bool]:
    mutations = {
        "status": lambda item: item.__setitem__("status", "PASS_CM2"),
        "C38": lambda item: item["C38_authority"].__setitem__("object_sha256", "0" * 64),
        "target_count": lambda item: item["router_census"].__setitem__("targeted_leaf_count", 2895),
        "full_count": lambda item: item["router_census"].__setitem__("whole_terminal_representative_parent_count", 162),
        "new_full_count": lambda item: item["router_census"].__setitem__("newly_whole_terminal_representative_parent_count", 6),
        "partial_count": lambda item: item["router_census"].__setitem__("partial_representative_parent_count", 310),
        "terminal_volume": lambda item: item["router_census"].__setitem__("representative_terminal_parent_equivalent", "2363/8"),
        "excluded": lambda item: item["round144_terminal_census"].__setitem__("EARLIEST_PREFIX_EXCLUDED", 75136),
        "unresolved": lambda item: item["round144_terminal_census"].__setitem__("UNRESOLVED_R1648_CONTINUATION", 1400),
        "unresolved_zero": lambda item: item["round144_terminal_census"].__setitem__("unresolved_zero", True),
        "D02": lambda item: item["strict_nonpromotion"].__setitem__("D02", "PASS"),
        "D03": lambda item: item["strict_nonpromotion"].__setitem__("D03", "AUTHORIZED"),
        "D04": lambda item: item["strict_nonpromotion"].__setitem__("D04", "MINTED"),
        "Gate5": lambda item: item["strict_nonpromotion"].__setitem__("Gate5", "18/18"),
        "CM2": lambda item: item["strict_nonpromotion"].__setitem__("CM2", "GO"),
        "precision": lambda item: item["numeric_authority"].__setitem__("precision_bits", 192),
        "leaf_rows": lambda item: item["ledgers"]["routed_child_pairs"].__setitem__("row_count", 10485),
        "parent_rows": lambda item: item["ledgers"]["parent_conservation"].__setitem__("row_count", 861),
    }
    outcomes: dict[str, bool] = {}
    for name, mutate in mutations.items():
        attacked = copy.deepcopy(result)
        mutate(attacked)
        try:
            semantic_guard(attacked)
        except Exception:
            outcomes[name] = True
        else:
            outcomes[name] = False
    require(all(outcomes.values()) and len(outcomes) == 18, "attack suite")
    return outcomes


def box_from_source(row: dict[str, Any]) -> Any:
    payload = row["representative_box"]
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


def collision0_delta(parent_key: str, box: Any, target: str) -> Any:
    return round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)[
        "Delta"
    ]


def collision0_distance(parent_key: str, box: Any, target: str) -> Any:
    raw = round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)
    return raw["ell"] * raw["ell"] - raw["Delta"]


def independent_h1_chart(parent_key: str, box: Any) -> str | None:
    full, nx, ny = round185.collision1_h1_ad(parent_key, box, FROZEN_OWNER)
    centered = round185.centered_enclosure(
        round185.collision1_h1_ad,
        parent_key,
        box,
        FROZEN_OWNER,
        full,
    )
    sign = round185.strict_sign(centered)
    if sign == 0:
        for axis, (lower, upper) in enumerate(
            ((box.t0, box.t1), (box.p0, box.p1))
        ):
            if round185.strict_sign(full.derivative[axis]) == 0:
                continue
            low = round185.collision1_h1_ad(
                parent_key,
                round185.fixed_axis_box(box, axis, lower, ".audit-low"),
                FROZEN_OWNER,
            )[0].value
            high = round185.collision1_h1_ad(
                parent_key,
                round185.fixed_axis_box(box, axis, upper, ".audit-high"),
                FROZEN_OWNER,
            )[0].value
            low_sign = round185.strict_sign(low)
            high_sign = round185.strict_sign(high)
            if low_sign != 0 and low_sign == high_sign:
                sign = low_sign
                break
    if sign > 0 and round185.strict_sign(nx.value) != 0:
        return "E" if round185.strict_sign(nx.value) > 0 else "W"
    if sign < 0 and round185.strict_sign(ny.value) != 0:
        return "N" if round185.strict_sign(ny.value) > 0 else "S"
    return None


def reconstruct_box(cell: dict[str, Any], path: str) -> tuple[Any, tuple[str, ...]]:
    t_values = cell["physical_t_interval"]
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
    active = tuple(cell["source_lineage"]["active_candidates"])
    for bit in path:
        stage, _records = c38.round166.classify_active(
            cell["gate3_chart"], box, active
        )
        if stage.classification == "unique_first":
            active = (FROZEN_OWNER,)
        elif stage.classification != "tangency_graph":
            active = stage.active_targets
        box = c38.round166.split_axis(
            box, c38.round166.longest_axis(box)
        )[int(bit)]
    return box, active


def independent_enhance(parent_key: str, box: Any, record: Any) -> Any:
    if record.classification not in {
        "unresolved_discriminant",
        "unresolved_root_sign",
    }:
        return record
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
    if delta_sign < 0:
        return c38.round166.ge.RootRecord(
            record.target_id,
            "no_real_intersection",
            raw["ell"].value,
            delta,
            None,
            None,
            raw["transverse"].value,
        )
    if delta_sign == 0:
        return record
    radical = delta.sqrt()
    ell = raw["ell"].value
    near = ell - radical
    far = ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        full = collision0_distance(parent_key, box, record.target_id)
        distance = round185.centered_enclosure(
            collision0_distance,
            parent_key,
            box,
            record.target_id,
            full,
        )
        if bool(ell > 0) and bool(far > 0) and bool(distance > 0):
            classification = "strict_future_root"
            near = distance / far
        else:
            classification = "unresolved_root_sign"
    return c38.round166.ge.RootRecord(
        record.target_id,
        classification,
        ell,
        delta,
        near,
        far,
        raw["transverse"].value,
    )


def downstream(
    source: dict[str, Any], box: Any, config: dict[str, Any]
) -> str:
    chart_id = ":".join(source["representative_origin_key"].split(":")[:2])
    route, _witness, _collision = c38.stage_two_route(
        chart_id,
        box,
        config["original_path"],
        config["reflected_path"],
        config["pair_index"],
        config["pattern_index"],
        config["cores"],
    )
    return route


def expected_terminal(task: dict[str, Any], config: dict[str, Any]) -> str:
    source = task["source"]
    parent_key = source["representative_origin_key"]
    if source["classification"] == TARGET_H1:
        box = box_from_source(source)
        chart = independent_h1_chart(parent_key, box)
        if chart is not None and chart != "W":
            return "EXCLUDED_C39_H1_OUTGOING_CHART_MISMATCH"
        require(chart == "W", "terminal H1 chart")
        route = downstream(source, box, config)
        require(route.startswith("EXCLUDED_"), "terminal H1 downstream")
        return "EXCLUDED_C39_H1_W_SIDE_" + route.removeprefix("EXCLUDED_")
    cell = task["cell"]
    box, active = reconstruct_box(cell, source["path"])
    _stage, records = c38.round166.classify_active(
        cell["gate3_chart"], box, active
    )
    enhanced = [independent_enhance(parent_key, box, record) for record in records]
    leaf = c38.round166.classify_from_records(
        cell["gate3_chart"], box, enhanced
    )
    if leaf.classification == "no_future_root":
        return "EXCLUDED_C39_C1_NO_FUTURE_ROOT"
    if leaf.classification == "unique_first" and leaf.owner_target != FROZEN_OWNER:
        return "EXCLUDED_C39_C1_UNIQUE_FIRST_OWNER_MISMATCH"
    require(
        leaf.classification == "unique_first" and leaf.owner_target == FROZEN_OWNER,
        "terminal C1 owner",
    )
    chart = independent_h1_chart(parent_key, box)
    if chart is not None and chart != "W":
        return "EXCLUDED_C39_C1_OUTGOING_CHART_MISMATCH"
    require(chart == "W", "terminal C1 chart")
    route = downstream(source, box, config)
    require(route.startswith("EXCLUDED_"), "terminal C1 downstream")
    return "EXCLUDED_C39_C1_ENHANCED_W_SIDE_" + route.removeprefix("EXCLUDED_")


def encode_tuple_map(value: dict[tuple[str, ...], int]) -> dict[str, int]:
    return {"\u001f".join(key): item for key, item in value.items()}


def worker(input_path: Path, output_path: Path) -> None:
    require(file_sha256(PRODUCER) == EXPECTED_PRODUCER_SOURCE, "producer source")
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
    rows = [
        {
            "task_id": task["task_id"],
            "classification": expected_terminal(task, config),
        }
        for task in payload["tasks"]
    ]
    write_json(output_path, {"schema": SCHEMA + ".worker", "rows": rows})


def run_workers(
    tasks: list[dict[str, Any]], config: dict[str, Any], work: Path
) -> dict[str, str]:
    work.mkdir()
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(DELIVERABLES) + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH")
        else ""
    )
    results: dict[str, str] = {}
    try:
        for batch_index, start in enumerate(range(0, len(tasks), WORKER_BATCH_SIZE)):
            input_path = work / f"input-{batch_index:03d}.json"
            output_path = work / f"output-{batch_index:03d}.json"
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
            for row in strict_json(output_path)["rows"]:
                require(row["task_id"] not in results, "duplicate task")
                results[row["task_id"]] = row["classification"]
        require(len(results) == len(tasks), "worker census")
        return results
    finally:
        shutil.rmtree(work, ignore_errors=True)


def audit(candidate: Path, output: Path) -> dict[str, Any]:
    require(file_sha256(PRODUCER) == EXPECTED_PRODUCER_SOURCE, "producer source pin")
    require(flint.__version__ == "0.9.0", "python-flint version")
    validate_manifest(candidate)
    result = strict_json(candidate / "result.json")
    validate_object(result, "object_sha256", EXPECTED_CANDIDATE_OBJECT, "C39")
    semantic_guard(result)
    lock = (candidate / "PARTIAL_GRAPH_ROUTER_ONLY.lock").read_text(
        encoding="utf-8"
    )
    require(
        "partial volume" in lock
        and "D02/D03/D04/Gate5/CM2 credit is forbidden" in lock,
        "candidate lock",
    )
    c38_candidate = (ROOT / result["C38_authority"]["path"]).resolve()
    c38_audit = (ROOT / result["C38_authority"]["independent_audit_path"]).resolve()
    validate_manifest(c38_candidate)
    c38_result = strict_json(c38_candidate / "result.json")
    c38_audit_result = strict_json(c38_audit)
    validate_object(c38_result, "object_sha256", EXPECTED_C38_OBJECT, "C38")
    validate_object(
        c38_audit_result,
        "object_sha256",
        EXPECTED_C38_AUDIT_OBJECT,
        "C38 audit",
    )
    source_rows = c38.read_ledger(
        c38_candidate, c38_result["ledgers"]["collision1_2_child_pairs"]
    )
    source_parents = c38.read_ledger(
        c38_candidate, c38_result["ledgers"]["representative_parent_conservation"]
    )
    routed_rows = c38.read_ledger(
        candidate, result["ledgers"]["routed_child_pairs"]
    )
    parent_rows = c38.read_ledger(
        candidate, result["ledgers"]["parent_conservation"]
    )
    require(
        len(source_rows) == len(routed_rows) == 10486
        and len(source_parents) == len(parent_rows) == 862,
        "row census",
    )
    source_by_sha = {row["row_sha256"]: row for row in source_rows}
    source_parent_index = {row["pair_index"]: row for row in source_parents}
    routed_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    terminal_tasks: list[dict[str, Any]] = []
    classifications: Counter[str] = Counter()
    methods: Counter[str] = Counter()
    targeted_cell_ids: set[str] = set()
    for row in routed_rows:
        source = source_by_sha[row["c38_child_row_sha256"]]
        require(
            row["pair_index"] == source["pair_index"]
            and row["representative_cell_id"] == source["representative_cell_id"]
            and row["reflected_cell_id"] == source["reflected_cell_id"]
            and row["relative_depth"] == source["relative_depth"]
            and row["path"] == source["path"]
            and row["parent_volume_fraction"] == source["parent_volume_fraction"]
            and row["representative_box"] == source["representative_box"]
            and row["reflected_box"] == source["reflected_box"]
            and row["source_classification"] == source["classification"],
            "source binding",
        )
        terminal = row["classification"].startswith("EXCLUDED_")
        require(
            row["round144_terminal_class"]
            == (
                "EARLIEST_PREFIX_EXCLUDED"
                if terminal
                else "UNRESOLVED_R1648_CONTINUATION"
            )
            and row["local_round144_terminal_credit"] == (1 if terminal else 0)
            and row["C34_common_refinement_credit"] == 0
            and row["D02_gate_credit"] == 0,
            "row credit",
        )
        if source["classification"] not in {TARGET_H1, *TARGET_C1}:
            require(
                row["classification"] == source["classification"]
                and row["surface_evidence"] is None,
                "untouched row",
            )
        if terminal and not source["classification"].startswith("EXCLUDED_"):
            terminal_tasks.append(
                {
                    "task_id": row["c39_routed_child_pair_id"],
                    "source": source,
                    "claimed_classification": row["classification"],
                }
            )
            if source["classification"] in TARGET_C1:
                targeted_cell_ids.add(source["representative_cell_id"])
        routed_by_pair[row["pair_index"]].append(row)
        classifications[row["classification"]] += 1
        methods[row["route_method"]] += 1
    require(len(terminal_tasks) == 320, f"new terminal task census:{len(terminal_tasks)}")

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
    cells = {
        row["cell_id"]: row
        for row in c38.read_ledger(c32, c32_result["ledgers"]["cells"])
        if row["cell_id"] in targeted_cell_ids
    }
    require(set(cells) == targeted_cell_ids, "terminal C1 cells")
    for task in terminal_tasks:
        source = task["source"]
        if source["classification"] in TARGET_C1:
            task["cell"] = cells[source["representative_cell_id"]]
    original_path = c38.read_ledger(
        c35, c35_result["ledgers"]["path_occurrences"]
    )[:2]
    reflected_path = c38.read_ledger(
        c37, c37_result["ledgers"]["reflected_r1648_occurrences"]
    )[:2]
    pair_index, pattern_index, _registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    config = {
        "original_path": original_path,
        "reflected_path": reflected_path,
        "pair_index": encode_tuple_map(pair_index),
        "pattern_index": encode_tuple_map(pattern_index),
    }
    work = output.parent / (output.stem + f".worker-{os.getpid()}")
    reconstructed = run_workers(terminal_tasks, config, work)
    require(
        all(
            reconstructed[task["task_id"]] == task["claimed_classification"]
            for task in terminal_tasks
        ),
        "independent terminal classifications",
    )

    full_count = 0
    partial_count = 0
    zero_count = 0
    newly_full = 0
    terminal_equivalent = Q(0)
    unresolved_equivalent = Q(0)
    for pair_number, parent in enumerate(parent_rows):
        require(parent["pair_index"] == pair_number, "parent order")
        rows = routed_by_pair[pair_number]
        terminal = sum(
            (
                Q(row["parent_volume_fraction"])
                for row in rows
                if row["classification"].startswith("EXCLUDED_")
            ),
            Q(0),
        )
        unresolved = Q(1) - terminal
        source_parent = source_parent_index[pair_number]
        whole = terminal == 1
        require(
            parent["c38_parent_row_sha256"] == source_parent["row_sha256"]
            and parent["leaf_count"] == len(rows)
            and parent["terminal_excluded_parent_volume"] == str(terminal)
            and parent["unresolved_parent_volume"] == str(unresolved)
            and parent["parent_volume_conservation"] == "1"
            and parent["whole_representative_parent_terminal"] is whole
            and parent["whole_reflected_parent_terminal"] is whole
            and parent["C34_common_refinement_credit"] == (2 if whole else 0)
            and parent["D02_gate_credit"] == 0,
            "parent reconstruction",
        )
        if whole:
            full_count += 1
        elif terminal == 0:
            zero_count += 1
        else:
            partial_count += 1
        if whole and not source_parent["whole_representative_parent_terminal"]:
            newly_full += 1
        terminal_equivalent += terminal
        unresolved_equivalent += unresolved
    require(
        full_count == 161
        and partial_count == 311
        and zero_count == 390
        and newly_full == 5
        and terminal_equivalent == Q(2355, 8)
        and unresolved_equivalent == Q(4541, 8)
        and result["router_census"]["classification_census"]
        == dict(sorted(classifications.items()))
        and result["router_census"]["route_method_census"]
        == dict(sorted(methods.items())),
        "global reconstruction",
    )
    attacks = attack_suite(result)
    audit_result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": (
            "PASS_INDEPENDENT_C39_FORMAL_CREDIT_RECONSTRUCTION__"
            "320_NEW_TERMINAL_ROUTES__18_OF_18_ATTACKS_FAIL_CLOSED"
        ),
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "reconstructed_formal_credit": {
            "routed_child_pair_count": len(routed_rows),
            "new_terminal_route_count": len(terminal_tasks),
            "whole_terminal_representative_parent_count": full_count,
            "newly_whole_terminal_representative_parent_count": newly_full,
            "whole_terminal_paired_coarse_cell_count": 2 * full_count,
            "newly_whole_terminal_paired_coarse_cell_count": 2 * newly_full,
            "terminal_parent_equivalent": str(terminal_equivalent),
            "unresolved_parent_equivalent": str(unresolved_equivalent),
            "formal_unresolved_after_C39": 1402,
        },
        "attacks": attacks,
        "strict_nonpromotion": result["strict_nonpromotion"],
    }
    audit_result["object_sha256"] = digest(audit_result)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + f".tmp-{os.getpid()}")
    write_json(temporary, audit_result)
    temporary.replace(output)
    return audit_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
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
        / (RUNTIME / "c39-current-token").read_text(encoding="utf-8").strip()
    )
    result = audit(candidate.resolve(), arguments.output.resolve())
    print(canonical(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
