#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as round139
import cm2_round166_multi_candidate_refinement_prototype as round166


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c38.d02-collision1-2-representative-child-atlas.independent-audit.v1"
EXPECTED_CANDIDATE_OBJECT = (
    "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434"
)
EXPECTED_CANDIDATE_STATUS = (
    "PASS_C38_COLLISION1_2_CHILD_ATLAS__10486_REPRESENTATIVE_LEAVES__"
    "2195_OVER_8_PARENT_EQUIVALENT_STRICT_EXCLUSIONS__312_WHOLE_CELLS_TERMINAL"
)
EXPECTED_PRODUCER_SOURCE = (
    "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d"
)
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
PRODUCER = DELIVERABLES / (
    "cm2_round306c38_d02_collision1_2_representative_child_atlas_v1.py"
)
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
FROZEN_OWNER = "W[1,0]"
EXTRA_DEPTH = 4
PRECISION_BITS = 192


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
    entries = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for entry in entries:
        expected, name = entry.split("  ", 1)
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


def rational_t_interval(cell: dict[str, Any]) -> tuple[Q, Q] | None:
    values = cell["physical_t_interval"]
    if any(value["kind"] != "RATIONAL" for value in values):
        return None
    return Q(values[0]["value"]), Q(values[1]["value"])


def expected_box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
        "relative_depth": box.depth,
        "path": box.path,
    }


def expected_reflected_box(chart: str, box: Any) -> dict[str, Any]:
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


def reconstruct_box(cell: dict[str, Any], path: str) -> tuple[Any, tuple[str, ...]]:
    t_interval = rational_t_interval(cell)
    require(t_interval is not None, "rational reconstruction")
    p_interval = tuple(Q(value) for value in cell["physical_p_interval"])
    box = round166.ge.AtlasBox(
        t_interval[0],
        t_interval[1],
        p_interval[0],
        p_interval[1],
        Q(0),
        Q(0),
        0,
        "",
    )
    active_targets = tuple(cell["source_lineage"]["active_candidates"])
    for bit in path:
        require(bit in "01", "path bit")
        stage_one, _records = round166.classify_active(
            cell["gate3_chart"], box, active_targets
        )
        if stage_one.classification == "unique_first":
            active_targets = (FROZEN_OWNER,)
        elif stage_one.classification != "tangency_graph":
            active_targets = stage_one.active_targets
        children = round166.split_axis(box, round166.longest_axis(box))
        box = children[int(bit)]
    return box, active_targets


def first_owner(chart_id: str, box: Any) -> dict[str, Any] | None:
    record = round166.root_record_fast(chart_id, box, FROZEN_OWNER)
    if record.classification != "strict_future_root" or record.near is None:
        return None
    _contact_x, _contact_y, outgoing_x, outgoing_y, _shear, _radial = (
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
    }


def route_stage_two(
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
        "c38-independent",
    )
    state = round139.lower.round136.initial_state(atom)
    next_state = round139.lower.time3.second_outgoing_state(atom, state, owner_one)
    if next_state is None:
        return "UNRESOLVED_COLLISION1_OUTGOING_STATE", "OUTGOING_STATE", 1
    try:
        word_one, error_one = round139.lower.round136.translation_normalized_official_word(
            state, "W[0,0]", owner_one, pair_index, pattern_index
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
        word_two, error_two = round139.lower.round136.translation_normalized_official_word(
            next_state, FROZEN_OWNER, owner_two, pair_index, pattern_index
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


def expected_leaf_classification(
    cell: dict[str, Any],
    box: Any,
    active_targets: tuple[str, ...],
    original_path: list[dict[str, Any]],
    reflected_path: list[dict[str, Any]],
    pair_index: dict[Any, Any],
    pattern_index: dict[Any, Any],
    cores: tuple[Any, ...],
) -> tuple[str, str, int]:
    stage_one, records = round166.classify_active(
        cell["gate3_chart"],
        box,
        active_targets,
    )
    disposition, seam_margins = round166.terminal_disposition(
        cell["gate3_chart"], stage_one
    )
    if disposition is not None and disposition != "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH":
        return disposition, disposition, 1
    if disposition == "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH":
        return route_stage_two(
            cell["gate3_chart"],
            box,
            original_path,
            reflected_path,
            pair_index,
            pattern_index,
            cores,
        )
    failure = round166.unresolved_failure(
        cell["gate3_chart"], stage_one, records, seam_margins
    )
    return "UNRESOLVED_COLLISION1_" + failure, "UNRESOLVED_COLLISION1_" + failure, 1


def semantic_guard(result: dict[str, Any]) -> None:
    census = result["refinement_census"]
    strict = result["strict_nonpromotion"]
    terminal = result["round144_terminal_census"]
    require(result["status"] == EXPECTED_CANDIDATE_STATUS, "semantic status")
    require(
        census["ordinary_cell_pair_count"] == 862
        and census["paired_coarse_cell_count"] == 1724
        and census["representative_child_pair_count"] == 10486
        and census["materialized_reflected_child_count"] == 10486
        and census["representative_terminal_excluded_parent_equivalent"] == "2195/8"
        and census["full_paired_atlas_terminal_excluded_parent_equivalent"] == "2195/4"
        and census["representative_unresolved_parent_equivalent"] == "4701/8"
        and census["full_paired_atlas_unresolved_parent_equivalent"] == "4701/4"
        and census["fully_terminal_representative_parent_count"] == 156
        and census["partial_representative_parent_count"] == 304
        and census["zero_progress_representative_parent_count"] == 402
        and census["algebraic_chart_boundary_parent_count"] == 29,
        "semantic census",
    )
    require(
        terminal == {
            "CONNECTED_TO_KNOWN": 0,
            "EARLIEST_PREFIX_EXCLUDED": 75124,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": 1412,
            "terminal_total": 76832,
            "unresolved_zero": False,
        },
        "semantic terminal",
    )
    require(
        strict["C34_common_refined_cell_count"] == 312
        and strict["C34_unresolved_R1648_continuations"] == 1412
        and strict["four_class_terminal_census_unresolved_zero"] is False
        and strict["D02"] == "BLOCKED_BY_1412_COMPLETE_R1648_CONTINUATIONS"
        and strict["D03"] == "UNAUTHORIZED"
        and strict["D04"] == "NOT_MINTED"
        and strict["Gate5"] == "10/18"
        and strict["complete_global_18_field_blocks"] == 0
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "semantic nonpromotion",
    )


def attack_census(result: dict[str, Any]) -> dict[str, bool]:
    attacks = {
        "status_promotion": ("status", "PASS_D02"),
        "pair_count": ("ordinary_cell_pair_count", 861),
        "leaf_count": ("representative_child_pair_count", 10485),
        "reflected_leaf_count": ("materialized_reflected_child_count", 10485),
        "terminal_volume": ("representative_terminal_excluded_parent_equivalent", "2200/8"),
        "unresolved_volume": ("representative_unresolved_parent_equivalent", "4696/8"),
        "whole_parent_count": ("fully_terminal_representative_parent_count", 157),
        "partial_parent_count": ("partial_representative_parent_count", 303),
        "algebraic_parent_count": ("algebraic_chart_boundary_parent_count", 28),
        "terminal_exclusion_count": ("EARLIEST_PREFIX_EXCLUDED", 75125),
        "formal_unresolved": ("UNRESOLVED_R1648_CONTINUATION", 1411),
        "common_refined": ("C34_common_refined_cell_count", 313),
        "false_unresolved_zero": ("four_class_terminal_census_unresolved_zero", True),
        "false_D02": ("D02", "PASS"),
        "false_D03": ("D03", "AUTHORIZED"),
        "false_CM2": ("CM2", "GO"),
    }
    outcomes: dict[str, bool] = {}
    for name, (field, replacement) in attacks.items():
        mutant = copy.deepcopy(result)
        if field == "status":
            mutant[field] = replacement
        elif field in mutant["refinement_census"]:
            mutant["refinement_census"][field] = replacement
        elif field in mutant["round144_terminal_census"]:
            mutant["round144_terminal_census"][field] = replacement
        else:
            mutant["strict_nonpromotion"][field] = replacement
        try:
            semantic_guard(mutant)
        except RuntimeError:
            outcomes[name] = True
        else:
            outcomes[name] = False
    require(len(outcomes) == 16 and all(outcomes.values()), "attack census")
    return outcomes


def audit(candidate: Path, output: Path) -> dict[str, Any]:
    require(file_sha256(PRODUCER) == EXPECTED_PRODUCER_SOURCE, "producer source pin")
    require(
        file_sha256(Path(round139.__file__).resolve()) == EXPECTED_ROUND139_SOURCE,
        "Round139 source pin",
    )
    require(
        file_sha256(Path(round166.__file__).resolve()) == EXPECTED_ROUND166_SOURCE,
        "Round166 source pin",
    )
    round166.check_pins()
    validate_manifest(candidate)
    result = strict_json(candidate / "result.json")
    validate_object(result, "object_sha256", EXPECTED_CANDIDATE_OBJECT, "C38")
    semantic_guard(result)
    lock = (candidate / "PARTIAL_CHILD_ATLAS_ONLY.lock").read_text(encoding="utf-8")
    require(
        "Exactly 156 representative parents" in lock
        and "no D02/D03/D04/Gate5/CM2 gate credit" in lock,
        "candidate lock",
    )

    c37 = (ROOT / result["C37_authority"]["path"]).resolve()
    c37_audit = (ROOT / result["C37_authority"]["independent_audit_path"]).resolve()
    validate_manifest(c37)
    c37_result = strict_json(c37 / "result.json")
    c37_audit_result = strict_json(c37_audit)
    validate_object(c37_result, "object_sha256", EXPECTED_C37_OBJECT, "C37")
    validate_object(
        c37_audit_result,
        "object_sha256",
        EXPECTED_C37_AUDIT_OBJECT,
        "C37 audit",
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
    child_rows = read_ledger(
        candidate, result["ledgers"]["collision1_2_child_pairs"]
    )
    parent_rows = read_ledger(
        candidate, result["ledgers"]["representative_parent_conservation"]
    )
    require(len(pairs) == len(parent_rows) == 862 and len(child_rows) == 10486, "row census")
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
    require(len(cells) == 1724, "cell census")

    ctx.prec = PRECISION_BITS
    pair_index, pattern_index, _registry_sha = round139.lower.component_cert.key_index_tables()
    round166.install_fast_readonly_replay()
    cores = tuple(round139.lower.core_cert.physical_cores())
    children_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for child in child_rows:
        children_by_pair[child["pair_index"]].append(child)

    global_classifications: Counter[str] = Counter()
    terminal_equivalent = Q(0)
    unresolved_equivalent = Q(0)
    full_count = 0
    partial_count = 0
    zero_count = 0
    algebraic_count = 0
    for pair, parent in zip(pairs, parent_rows, strict=True):
        pair_number = pair["pair_index"]
        require(parent["pair_index"] == pair_number, "parent order")
        representative = cells[pair["representative_cell_id"]]
        reflected = cells[pair["reflected_cell_id"]]
        leaves = children_by_pair[pair_number]
        require(parent["leaf_count"] == len(leaves), "parent leaf count")
        path_set = {leaf["path"] for leaf in leaves}
        require(len(path_set) == len(leaves), "duplicate child path")
        require(
            not any(
                left != right and right.startswith(left)
                for left in path_set
                for right in path_set
            ),
            "prefix-free partition",
        )
        terminal_volume = Q(0)
        unresolved_volume = Q(0)
        parent_census: Counter[str] = Counter()
        if rational_t_interval(representative) is None:
            require(
                len(leaves) == 1
                and leaves[0]["classification"]
                == "UNRESOLVED_ALGEBRAIC_CHART_BOUNDARY_PARENT"
                and leaves[0]["relative_depth"] == 0
                and leaves[0]["representative_box"] is None
                and leaves[0]["reflected_box"] is None,
                "algebraic parent",
            )
            algebraic_count += 1
        for leaf in leaves:
            require(
                leaf["representative_cell_id"] == representative["cell_id"]
                and leaf["reflected_cell_id"] == reflected["cell_id"]
                and leaf["representative_parent_row_sha256"]
                == representative["row_sha256"]
                and leaf["reflected_parent_row_sha256"] == reflected["row_sha256"],
                "leaf parent binding",
            )
            volume = Q(leaf["parent_volume_fraction"])
            require(volume == Q(1, 2 ** leaf["relative_depth"]), "leaf volume")
            classification = leaf["classification"]
            if rational_t_interval(representative) is not None:
                box, active_targets = reconstruct_box(representative, leaf["path"])
                require(
                    leaf["relative_depth"] == len(leaf["path"])
                    and leaf["representative_box"] == expected_box_payload(box)
                    and leaf["reflected_box"]
                    == expected_reflected_box(representative["compact_chart"], box)
                    and leaf["reflection_transport_materialized"] is True,
                    "child geometry",
                )
                expected_class, expected_witness, expected_collision = (
                    expected_leaf_classification(
                        representative,
                        box,
                        active_targets,
                        original_path,
                        reflected_path,
                        pair_index,
                        pattern_index,
                        cores,
                    )
                )
                require(
                    classification == expected_class
                    and leaf["witness"] == expected_witness
                    and leaf["first_decision_collision"] == expected_collision,
                    f"numeric replay:{pair_number}:{leaf['path']}",
                )
            terminal_leaf = classification.startswith("EXCLUDED_")
            if terminal_leaf:
                terminal_volume += volume
                require(
                    leaf["round144_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED"
                    and leaf["local_round144_terminal_credit"] == 1,
                    "terminal leaf credit",
                )
            else:
                unresolved_volume += volume
                require(
                    leaf["round144_terminal_class"]
                    == "UNRESOLVED_R1648_CONTINUATION"
                    and leaf["local_round144_terminal_credit"] == 0,
                    "unresolved leaf credit",
                )
            require(
                leaf["C34_common_refinement_credit"] == 0
                and leaf["D02_gate_credit"] == 0,
                "leaf nonpromotion",
            )
            parent_census[classification] += 1
            global_classifications[classification] += 1
        require(terminal_volume + unresolved_volume == 1, "parent Kraft conservation")
        require(
            parent["terminal_excluded_parent_volume"] == qstr(terminal_volume)
            and parent["unresolved_parent_volume"] == qstr(unresolved_volume)
            and parent["parent_volume_conservation"] == "1"
            and parent["classification_census"] == dict(sorted(parent_census.items()))
            and parent["maximum_relative_depth"]
            == max(leaf["relative_depth"] for leaf in leaves),
            "parent summary",
        )
        if terminal_volume == 1:
            full_count += 1
            require(
                parent["whole_representative_parent_terminal"] is True
                and parent["whole_reflected_parent_terminal"] is True
                and parent["C34_common_refinement_credit"] == 2,
                "full parent credit",
            )
        elif terminal_volume == 0:
            zero_count += 1
            require(parent["C34_common_refinement_credit"] == 0, "zero parent credit")
        else:
            partial_count += 1
            require(parent["C34_common_refinement_credit"] == 0, "partial parent credit")
        terminal_equivalent += terminal_volume
        unresolved_equivalent += unresolved_volume

    census = result["refinement_census"]
    require(
        terminal_equivalent == Q(2195, 8)
        and unresolved_equivalent == Q(4701, 8)
        and full_count == 156
        and partial_count == 304
        and zero_count == 402
        and algebraic_count == 29
        and census["classification_census"]
        == dict(sorted(global_classifications.items())),
        "reconstructed global census",
    )
    attacks = attack_census(result)
    audit_result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_INDEPENDENT_C38_RECONSTRUCTION__16_OF_16_ATTACKS_FAIL_CLOSED",
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "reconstructed_census": {
            "representative_child_pair_count": len(child_rows),
            "parent_pair_count": len(parent_rows),
            "terminal_parent_equivalent": qstr(terminal_equivalent),
            "unresolved_parent_equivalent": qstr(unresolved_equivalent),
            "whole_terminal_representative_parent_count": full_count,
            "whole_terminal_paired_coarse_cell_count": 2 * full_count,
            "formal_unresolved_after_C38": 1412,
            "classification_census": dict(sorted(global_classifications.items())),
        },
        "attacks": attacks,
        "strict_nonpromotion": result["strict_nonpromotion"],
    }
    audit_result["object_sha256"] = digest(audit_result)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + f".tmp-{os.getpid()}")
    temporary.write_bytes(canonical(audit_result) + b"\n")
    temporary.replace(output)
    return audit_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    candidate = arguments.candidate or (
        RUNTIME / "candidates" / (RUNTIME / "c38-current-token").read_text().strip()
    )
    result = audit(candidate.resolve(), arguments.output.resolve())
    print(canonical(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
