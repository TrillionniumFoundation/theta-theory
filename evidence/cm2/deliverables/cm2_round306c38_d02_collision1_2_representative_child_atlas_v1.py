#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as round139
import cm2_round166_multi_candidate_refinement_prototype as round166


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c38.d02-collision1-2-representative-child-atlas.v1"
LEAF_SCHEMA = "cm2.round306c38.collision1-2-child-pair.v1"
PARENT_SCHEMA = "cm2.round306c38.representative-parent-conservation.v1"
EXTRA_DEPTH = 4
PRECISION_BITS = 192

EXPECTED_C37_OBJECT = "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b"
EXPECTED_C37_AUDIT_OBJECT = (
    "b5be1e8d97337ff90f514695f06bbb1156c606324a50b05766ed080a261d8044"
)
EXPECTED_C36_OBJECT = "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167"
EXPECTED_C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
EXPECTED_ROUND139_SOURCE = (
    "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b"
)
EXPECTED_ROUND166_SOURCE = (
    "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c"
)

CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
FROZEN_OWNER = "W[1,0]"


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


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


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.is_file()
        and path.stat().st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger bytes:{path}",
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            semantic = dict(row)
            row_sha = semantic.pop("row_sha256", None)
            require(row_sha == digest(semantic), f"row closure:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(
        len(rows) == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor:{path}",
    )
    return rows


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> LedgerWriter:
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


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir() if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def rational_t_interval(cell: dict[str, Any]) -> tuple[Q, Q] | None:
    values = cell["physical_t_interval"]
    if any(value["kind"] != "RATIONAL" for value in values):
        return None
    return Q(values[0]["value"]), Q(values[1]["value"])


def box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
        "relative_depth": box.depth,
        "path": box.path,
    }


def reflected_box(chart: str, box: Any) -> dict[str, Any]:
    if chart in {"E", "W"}:
        reflected_chart = chart
        t_interval = [-box.t1, -box.t0]
    else:
        reflected_chart = {"N": "S", "S": "N"}[chart]
        t_interval = [box.t0, box.t1]
    return {
        "compact_chart": reflected_chart,
        "t": [qstr(value) for value in t_interval],
        "p": [qstr(-box.p1), qstr(-box.p0)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def first_owner(chart_id: str, box: Any) -> dict[str, Any] | None:
    record = round166.root_record_fast(chart_id, box, FROZEN_OWNER)
    if record.classification != "strict_future_root" or record.near is None:
        return None
    contact_x, contact_y, outgoing_x, outgoing_y, shear, _radial = (
        round166.atlas.geometry(chart_id, box)
    )
    radical = record.discriminant.sqrt()
    transverse = record.transverse
    radius = round166.base.arbq(round166.base.RADIUS["W"])
    return {
        "selected_target_id": FROZEN_OWNER,
        "selected_root": record.near,
        "normal_x": (-radical * outgoing_x + transverse * outgoing_y) / radius,
        "normal_y": (-radical * outgoing_y - transverse * outgoing_x) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
        "source_geometry": (contact_x, contact_y, outgoing_x, outgoing_y, shear),
    }


def stage_two_route(
    chart_id: str,
    box: Any,
    original_path: list[dict[str, Any]],
    reflected_path: list[dict[str, Any]],
    pair_index: dict[Any, Any],
    pattern_index: dict[Any, Any],
    cores: tuple[Any, ...],
) -> tuple[str, str, int]:
    owner_one = first_owner(chart_id, box)
    if owner_one is None:
        return "UNRESOLVED_COLLISION1_OWNER_GEOMETRY", "OWNER_GEOMETRY", 1
    atom = round139.lower.step1.Atom(
        CORE_INDEX[chart_id],
        cores[CORE_INDEX[chart_id]],
        box.t0,
        box.t1,
        box.p0,
        box.p1,
        Q(0),
        Q(0),
        "c38",
    )
    state = round139.lower.round136.initial_state(atom)
    next_state = round139.lower.time3.second_outgoing_state(atom, state, owner_one)
    if next_state is None:
        return "UNRESOLVED_COLLISION1_OUTGOING_STATE", "OUTGOING_STATE", 1
    try:
        word_one, error_one = (
            round139.lower.round136.translation_normalized_official_word(
                state,
                "W[0,0]",
                owner_one,
                pair_index,
                pattern_index,
            )
        )
    except RuntimeError as error:
        return "UNRESOLVED_COLLISION1_WORD", str(error), 1
    if word_one is None:
        return "UNRESOLVED_COLLISION1_WORD", str(error_one), 1
    word_one_id = round139.lower.round136.compact_key(word_one["key"])[
        "official_word_key_id"
    ]
    if word_one_id != original_path[0]["official_word_key_id"]:
        return "EXCLUDED_COLLISION1_WORD_MISMATCH", word_one_id, 1

    owner_two, owner_error = round139.lower.time3.strict_next_owner(
        next_state, FROZEN_OWNER
    )
    if owner_two is None:
        return "UNRESOLVED_COLLISION2_OWNER", owner_error, 2
    selected = owner_two["selected_target_id"]
    expected_by_owner = {
        original_path[1]["selected_absolute_owner_id"]: original_path[1],
        reflected_path[1]["selected_absolute_owner_id"]: reflected_path[1],
    }
    if selected not in expected_by_owner:
        return "EXCLUDED_COLLISION2_OWNER_MISMATCH", selected, 2
    expected = expected_by_owner[selected]
    outgoing_two = round139.lower.time3.second_outgoing_state(
        atom, next_state, owner_two
    )
    if outgoing_two is None:
        return "UNRESOLVED_COLLISION2_OUTGOING_STATE", "OUTGOING_STATE", 2
    if outgoing_two["chart"] != expected["outgoing_chart"]:
        return "EXCLUDED_COLLISION2_CHART_MISMATCH", outgoing_two["chart"], 2
    try:
        word_two, error_two = (
            round139.lower.round136.translation_normalized_official_word(
                next_state,
                FROZEN_OWNER,
                owner_two,
                pair_index,
                pattern_index,
            )
        )
    except RuntimeError as error:
        return "UNRESOLVED_COLLISION2_WORD", str(error), 2
    if word_two is None:
        return "UNRESOLVED_COLLISION2_WORD", str(error_two), 2
    word_two_id = round139.lower.round136.compact_key(word_two["key"])[
        "official_word_key_id"
    ]
    if word_two_id != expected["official_word_key_id"]:
        return "EXCLUDED_COLLISION2_WORD_MISMATCH", word_two_id, 2
    branch = "ORIGINAL" if selected == original_path[1]["selected_absolute_owner_id"] else "REFLECTED"
    return f"LIVE_COLLISION2_{branch}_MATCH", selected, 2


def is_exclusion(classification: str) -> bool:
    return classification.startswith("EXCLUDED_")


def is_live(classification: str) -> bool:
    return classification.startswith("LIVE_")


def refine_parent(
    pair: dict[str, Any],
    representative: dict[str, Any],
    reflected: dict[str, Any],
    original_path: list[dict[str, Any]],
    reflected_path: list[dict[str, Any]],
    pair_index: dict[Any, Any],
    pattern_index: dict[Any, Any],
    cores: tuple[Any, ...],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    t_interval = rational_t_interval(representative)
    if t_interval is None:
        leaf = {
            "schema": LEAF_SCHEMA,
            "pair_index": pair["pair_index"],
            "representative_cell_id": representative["cell_id"],
            "representative_origin_key": representative["origin_key"],
            "reflected_cell_id": reflected["cell_id"],
            "reflected_origin_key": reflected["origin_key"],
            "representative_parent_row_sha256": representative["row_sha256"],
            "reflected_parent_row_sha256": reflected["row_sha256"],
            "representative_parent_physical_t_interval": representative[
                "physical_t_interval"
            ],
            "representative_parent_physical_p_interval": representative[
                "physical_p_interval"
            ],
            "relative_depth": 0,
            "path": "",
            "representative_box": None,
            "reflected_box": None,
            "parent_volume_fraction": "1",
            "classification": "UNRESOLVED_ALGEBRAIC_CHART_BOUNDARY_PARENT",
            "witness": "EXACT_ALGEBRAIC_ENDPOINT_REQUIRES_GRAPH_CELL",
            "first_decision_collision": 1,
            "round144_terminal_class": "UNRESOLVED_R1648_CONTINUATION",
            "local_round144_terminal_credit": 0,
            "reflection_transport_materialized": False,
            "C34_common_refinement_credit": 0,
            "D02_gate_credit": 0,
        }
        parent = {
            "schema": PARENT_SCHEMA,
            "pair_index": pair["pair_index"],
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "leaf_count": 1,
            "terminal_excluded_parent_volume": "0",
            "unresolved_parent_volume": "1",
            "parent_volume_conservation": "1",
            "whole_representative_parent_terminal": False,
            "whole_reflected_parent_terminal": False,
            "classification_census": {leaf["classification"]: 1},
            "maximum_relative_depth": 0,
            "C34_common_refinement_credit": 0,
            "D02_gate_credit": 0,
        }
        return [leaf], parent

    p_interval = tuple(Q(value) for value in representative["physical_p_interval"])
    root_box = round166.ge.AtlasBox(
        t_interval[0],
        t_interval[1],
        p_interval[0],
        p_interval[1],
        Q(0),
        Q(0),
        0,
        "",
    )
    chart_id = representative["gate3_chart"]
    pending: list[tuple[Any, tuple[str, ...]]] = [
        (root_box, tuple(representative["source_lineage"]["active_candidates"]))
    ]
    leaves: list[dict[str, Any]] = []
    terminal_volume = Q(0)
    unresolved_volume = Q(0)
    classification_census: Counter[str] = Counter()
    while pending:
        box, active_targets = pending.pop()
        stage_one, records = round166.classify_active(chart_id, box, active_targets)
        disposition, seam_margins = round166.terminal_disposition(chart_id, stage_one)
        if disposition is not None and disposition != "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH":
            classification = disposition
            witness = disposition
            collision_index = 1
        elif disposition == "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH":
            classification, witness, collision_index = stage_two_route(
                chart_id,
                box,
                original_path,
                reflected_path,
                pair_index,
                pattern_index,
                cores,
            )
        else:
            classification = "UNRESOLVED_COLLISION1_" + round166.unresolved_failure(
                chart_id, stage_one, records, seam_margins
            )
            witness = classification
            collision_index = 1

        terminal = is_exclusion(classification)
        if not terminal and not is_live(classification) and box.depth < EXTRA_DEPTH:
            if stage_one.classification == "unique_first":
                inherited = (FROZEN_OWNER,)
            elif stage_one.classification == "tangency_graph":
                inherited = active_targets
            else:
                inherited = stage_one.active_targets
            children = round166.split_axis(box, round166.longest_axis(box))
            for child in reversed(children):
                pending.append((child, inherited))
            continue

        volume = Q(1, 2**box.depth)
        if terminal:
            terminal_volume += volume
            terminal_class = "EARLIEST_PREFIX_EXCLUDED"
            local_credit = 1
        else:
            unresolved_volume += volume
            terminal_class = "UNRESOLVED_R1648_CONTINUATION"
            local_credit = 0
        classification_census[classification] += 1
        representative_box = box_payload(box)
        reflected_payload = reflected_box(representative["compact_chart"], box)
        semantic = {
            "schema": LEAF_SCHEMA,
            "pair_index": pair["pair_index"],
            "representative_cell_id": representative["cell_id"],
            "representative_origin_key": representative["origin_key"],
            "reflected_cell_id": reflected["cell_id"],
            "reflected_origin_key": reflected["origin_key"],
            "representative_parent_row_sha256": representative["row_sha256"],
            "reflected_parent_row_sha256": reflected["row_sha256"],
            "representative_parent_physical_t_interval": representative[
                "physical_t_interval"
            ],
            "representative_parent_physical_p_interval": representative[
                "physical_p_interval"
            ],
            "relative_depth": box.depth,
            "path": box.path,
            "representative_box": representative_box,
            "reflected_box": reflected_payload,
            "parent_volume_fraction": qstr(volume),
            "classification": classification,
            "witness": witness,
            "first_decision_collision": collision_index,
            "round144_terminal_class": terminal_class,
            "local_round144_terminal_credit": local_credit,
            "reflection_transport_materialized": True,
            "C34_common_refinement_credit": 0,
            "D02_gate_credit": 0,
        }
        semantic["refinement_child_pair_id"] = "c38-child-pair:" + digest(semantic)
        leaves.append(semantic)

    require(terminal_volume + unresolved_volume == 1, "parent volume conservation")
    leaves.sort(key=lambda row: row["path"])
    parent = {
        "schema": PARENT_SCHEMA,
        "pair_index": pair["pair_index"],
        "representative_cell_id": representative["cell_id"],
        "reflected_cell_id": reflected["cell_id"],
        "leaf_count": len(leaves),
        "terminal_excluded_parent_volume": qstr(terminal_volume),
        "unresolved_parent_volume": qstr(unresolved_volume),
        "parent_volume_conservation": "1",
        "whole_representative_parent_terminal": terminal_volume == 1,
        "whole_reflected_parent_terminal": terminal_volume == 1,
        "classification_census": dict(sorted(classification_census.items())),
        "maximum_relative_depth": max(row["relative_depth"] for row in leaves),
        "C34_common_refinement_credit": 2 if terminal_volume == 1 else 0,
        "D02_gate_credit": 0,
    }
    return leaves, parent


def build(output: Path, c37: Path, c37_audit: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    require(
        file_sha256(Path(round139.__file__).resolve()) == EXPECTED_ROUND139_SOURCE,
        "Round139 source pin",
    )
    require(
        file_sha256(Path(round166.__file__).resolve()) == EXPECTED_ROUND166_SOURCE,
        "Round166 source pin",
    )
    round166_chain = round166.check_pins()
    validate_manifest(c37)
    c37_result = strict_json(c37 / "result.json")
    validate_object(c37_result, "object_sha256", EXPECTED_C37_OBJECT, "C37")
    c37_audit_result = strict_json(c37_audit)
    validate_object(
        c37_audit_result,
        "object_sha256",
        EXPECTED_C37_AUDIT_OBJECT,
        "C37 audit",
    )
    require(
        c37_audit_result["candidate_object_sha256"] == EXPECTED_C37_OBJECT
        and c37_audit_result["status"]
        == "PASS_INDEPENDENT_C37_RECONSTRUCTION__18_OF_18_ATTACKS_FAIL_CLOSED",
        "C37 audit binding",
    )
    c36 = (ROOT / c37_result["C36_authority"]["path"]).resolve()
    validate_manifest(c36)
    c36_result = strict_json(c36 / "result.json")
    validate_object(c36_result, "object_sha256", EXPECTED_C36_OBJECT, "C36")
    c35 = (ROOT / c36_result["C35_authority"]["path"]).resolve()
    c34 = (ROOT / c36_result["C34_authority"]["path"]).resolve()
    validate_manifest(c35)
    validate_manifest(c34)
    c35_result = strict_json(c35 / "result.json")
    c34_result = strict_json(c34 / "result.json")
    validate_object(c35_result, "object_sha256", EXPECTED_C35_OBJECT, "C35")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")
    c32 = (ROOT / c34_result["C32_authority"]["path"]).resolve()
    validate_manifest(c32)
    c32_result = strict_json(c32 / "result.json")
    validate_object(c32_result, "object_sha256", EXPECTED_C32_OBJECT, "C32")

    pairs = read_ledger(
        c37, c37_result["ledgers"]["ordinary_cell_reflection_pairs"]
    )
    original_path = read_ledger(c35, c35_result["ledgers"]["path_occurrences"])
    reflected_path = read_ledger(
        c37, c37_result["ledgers"]["reflected_r1648_occurrences"]
    )
    require(
        len(pairs) == 862
        and len(original_path) == len(reflected_path) == 1648,
        "authority census",
    )
    required_ids = {
        cell_id
        for pair in pairs
        for cell_id in (pair["representative_cell_id"], pair["reflected_cell_id"])
    }
    cells = {
        row["cell_id"]: row
        for row in read_ledger(c32, c32_result["ledgers"]["cells"])
        if row["cell_id"] in required_ids
    }
    require(len(cells) == 1724, "paired cell census")

    ctx.prec = PRECISION_BITS
    pair_index, pattern_index, _registry_sha = (
        round139.lower.component_cert.key_index_tables()
    )
    round166.install_fast_readonly_replay()
    cores = tuple(round139.lower.core_cert.physical_cores())

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        leaf_writer = LedgerWriter(
            stage / "collision1_2_child_pairs.jsonl.gz",
            "PAIR_INDEX_THEN_LOCAL_PATH",
        )
        parent_writer = LedgerWriter(
            stage / "representative_parent_conservation.jsonl.gz",
            "PAIR_INDEX_ASCENDING",
        )
        global_classifications: Counter[str] = Counter()
        terminal_equivalent = Q(0)
        unresolved_equivalent = Q(0)
        partial_parent_count = 0
        zero_progress_parent_count = 0
        fully_terminal_parent_count = 0
        algebraic_parent_count = 0
        with leaf_writer, parent_writer:
            for expected_pair_index, pair in enumerate(pairs):
                require(pair["pair_index"] == expected_pair_index, "pair order")
                representative = cells[pair["representative_cell_id"]]
                reflected = cells[pair["reflected_cell_id"]]
                leaves, parent = refine_parent(
                    pair,
                    representative,
                    reflected,
                    original_path,
                    reflected_path,
                    pair_index,
                    pattern_index,
                    cores,
                )
                for leaf in leaves:
                    leaf_writer.write(leaf)
                    global_classifications[leaf["classification"]] += 1
                parent_writer.write(parent)
                terminal = Q(parent["terminal_excluded_parent_volume"])
                unresolved = Q(parent["unresolved_parent_volume"])
                terminal_equivalent += terminal
                unresolved_equivalent += unresolved
                if terminal == 1:
                    fully_terminal_parent_count += 1
                elif terminal == 0:
                    zero_progress_parent_count += 1
                else:
                    partial_parent_count += 1
                if "UNRESOLVED_ALGEBRAIC_CHART_BOUNDARY_PARENT" in parent[
                    "classification_census"
                ]:
                    algebraic_parent_count += 1
        require(terminal_equivalent + unresolved_equivalent == 862, "global volume")
        require(
            fully_terminal_parent_count == 156
            and partial_parent_count == 304
            and zero_progress_parent_count == 402
            and algebraic_parent_count == 29,
            "parent frontier census:"
            f"{fully_terminal_parent_count}:"
            f"{partial_parent_count}:"
            f"{zero_progress_parent_count}:"
            f"{algebraic_parent_count}",
        )
        require(
            leaf_writer.count == 10486
            and terminal_equivalent == Q(2195, 8)
            and unresolved_equivalent == Q(4701, 8),
            "leaf and volume census:"
            f"{leaf_writer.count}:"
            f"{qstr(terminal_equivalent)}:"
            f"{qstr(unresolved_equivalent)}",
        )
        (stage / "PARTIAL_CHILD_ATLAS_ONLY.lock").write_text(
            "C38 materializes exact collision-one/two dyadic child pairs and strict earliest-"
            "prefix exclusions. Graph collars, algebraic chart faces, and every collision-"
            "three-through-1648 obligation remain unresolved. Exactly 156 representative "
            "parents and their 156 reflected partners receive earliest-prefix terminal credit; "
            "no D02/D03/D04/Gate5/CM2 gate credit is granted.\n",
            encoding="utf-8",
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C38_COLLISION1_2_CHILD_ATLAS__10486_REPRESENTATIVE_LEAVES__"
                "2195_OVER_8_PARENT_EQUIVALENT_STRICT_EXCLUSIONS__"
                "312_WHOLE_CELLS_TERMINAL"
            ),
            "C37_authority": {
                "path": str(c37.resolve().relative_to(ROOT)),
                "object_sha256": c37_result["object_sha256"],
                "independent_audit_path": str(c37_audit.resolve().relative_to(ROOT)),
                "independent_audit_object_sha256": c37_audit_result["object_sha256"],
            },
            "numeric_authority": {
                "Round139_source_sha256": EXPECTED_ROUND139_SOURCE,
                "Round166_source_sha256": EXPECTED_ROUND166_SOURCE,
                "Round166_dimension_safe_chain": round166_chain,
                "precision_bits": PRECISION_BITS,
                "maximum_relative_dyadic_depth": EXTRA_DEPTH,
                "source_slice": "s=0",
            },
            "refinement_census": {
                "ordinary_cell_pair_count": 862,
                "paired_coarse_cell_count": 1724,
                "representative_child_pair_count": leaf_writer.count,
                "materialized_reflected_child_count": leaf_writer.count,
                "representative_terminal_excluded_parent_equivalent": qstr(
                    terminal_equivalent
                ),
                "full_paired_atlas_terminal_excluded_parent_equivalent": qstr(
                    2 * terminal_equivalent
                ),
                "representative_unresolved_parent_equivalent": qstr(
                    unresolved_equivalent
                ),
                "full_paired_atlas_unresolved_parent_equivalent": qstr(
                    2 * unresolved_equivalent
                ),
                "fully_terminal_representative_parent_count": fully_terminal_parent_count,
                "partial_representative_parent_count": partial_parent_count,
                "zero_progress_representative_parent_count": zero_progress_parent_count,
                "algebraic_chart_boundary_parent_count": algebraic_parent_count,
                "classification_census": dict(sorted(global_classifications.items())),
            },
            "ledgers": {
                "collision1_2_child_pairs": leaf_writer.descriptor(),
                "representative_parent_conservation": parent_writer.descriptor(),
            },
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "EARLIEST_PREFIX_EXCLUDED": 75124,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": 1412,
                "terminal_total": 76832,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "C34_common_refined_cell_count": 312,
                "C34_unresolved_R1648_continuations": 1412,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": "BLOCKED_BY_1412_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "replace the collision-one/two discriminant, outgoing-chart-seam, source-"
                "grazing, and algebraic-chart collars with exact interval-Newton graph "
                "cells and their off-graph slabs on the remaining 706 representative pairs; "
                "continue each surviving original/reflected branch through collisions 3--1648 "
                "until every coarse pair is terminal"
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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--c37", type=Path)
    parser.add_argument("--c37-audit", type=Path)
    arguments = parser.parse_args()
    c37 = arguments.c37 or (
        RUNTIME / "candidates" / (RUNTIME / "c37-current-token").read_text().strip()
    )
    c37_audit = arguments.c37_audit or (
        RUNTIME
        / "audit"
        / (RUNTIME / "c37-current-audit-token").read_text().strip()
        / "independent_audit.json"
    )
    result = build(arguments.output, c37.resolve(), c37_audit.resolve())
    print(canonical(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
