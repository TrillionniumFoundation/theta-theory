#!/usr/bin/env python3
"""Round-28 executable nonempty adaptive component registry.

This append-only leaf turns two finite physical inner registries into actual
nonempty connected regular component *cells*.  It deliberately does not call
the 441,280 symbolic candidate words nonempty.  A registered cell is the open
interior of a positive dyadic source box on which every collision owner, wall
word and core predicate used by its finite path is strict.

The depth-one registry is complete on all 4,216 frozen R1-inner atoms.  The
depth-two registry starts from all 114,006 frozen Q2-inner atoms and resolves
the second frozen Gate-5 word, including the ordered clean-wall record, with
an optional bounded adaptive recut.  Finite unresolved recuts, if any, remain
an explicitly positive parameter-averaged coordinate-base outer mass and are
never declared null.  Only the
limiting physical wall/corner/owner boundary has collision measure zero.

These adaptive cells are connected components of the finite open cell
registry obtained after removing their artificial dyadic faces.  They are
not claimed to be maximal connected components of an entire physical path
fibre, and no arbitrary-n registry or strong operator payload is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2_cert
import cm2_gate5_return_word_three_norm_frontier_cert as gate5_cert


Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round28-nonempty-adaptive-component-registry.v1"
MANIFEST_SCHEMA = (
    "cm2.gate34.round28-nonempty-adaptive-component-registry.manifest.v1"
)
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
)
MAX_EXTRA_WALL_BINARY_DEPTH = 6
PARAMETER_WIDTH = core_cert.S_UPPER - core_cert.S_LOWER
TARGET_PATTERN = re.compile(r"([GW])\[(-?\d+),(-?\d+)\]")

DEPENDENCIES = {
    "cm2_gate5_return_word_three_norm_frontier_cert.py": (
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json": (
        "a6d7c9dad800a7df7aa17b4f94f9bf45363d2839ff3711f35075ea998de07089"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def stream_update(digest: Any, row: dict[str, Any]) -> None:
    digest.update(canonical_json(row).encode("utf-8"))
    digest.update(b"\n")


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value

    gate5 = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["immutable_candidate_key_registry"]
    require(gate5["candidate_return_word_key_count"] == 441280, "key count")
    require(gate5["domain_contract"]["regular_domain_partition"] is True,
            "key partition")
    require(gate5["exact_nonempty_candidate_key_count"] is None,
            "old nonempty frontier")

    step1 = loaded[
        "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    ]
    registry1 = step1["result"]["adaptive_full_core_step1_registry"]
    require(registry1["classification_histogram"]["RETURN_AT_1_INNER"] == 4216,
            "R1 count")
    require(
        step1["result"]["collision_mass_inner_outer_frontier"]
        ["return_inner_base_mass"] == "6473/256000000",
        "R1 mass",
    )

    time2 = loaded[
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    ]
    registry2 = time2["result"]["Q1_time2_adaptive_registry"]
    require(registry2["strict_Q2_inner_atom_count"] == 114006, "Q2 count")
    require(
        time2["result"]["Q1_time2_mass_frontier"]["Q2_inner_base_mass"]
        == "5257799/5120000000",
        "Q2 mass",
    )

    limit2 = loaded[
        "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json"
    ]
    require(
        limit2["verdict"][
            "limiting_full_physical_R2_Q2_partition_mod_collision_null_set"
        ] == "CERTIFIED",
        "limiting R2/Q2",
    )

    schema = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    require(
        schema["verdict"]["arbitrary_n_regular_connected_component_existence_schema"]
        == "CERTIFIED_NONCONSTRUCTIVE",
        "component existence schema",
    )
    require(
        schema["verdict"]["nonempty_component_enumeration_and_numeric_payload"]
        == "NOT_CERTIFIED",
        "old nonempty frontier",
    )

    q2 = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]
    require(
        q2["result"]["Q2_exact_mass_and_restriction_registry"]
        ["common_forward_reverse_restriction_id_count"] == 114006,
        "Q2 restriction count",
    )
    require(
        q2["result"]["Q2_exact_mass_and_restriction_registry"]
        ["restriction_is_smooth_and_invertible_on_each_regular_fixed_s_slice"]
        is True,
        "Q2 regular restrictions",
    )
    return loaded


def key_index_tables() -> tuple[
    dict[tuple[str, str], int], dict[tuple[str, ...], int], str
]:
    pairs = gate5_cert.retained_chart_target_pairs()
    patterns = tuple(gate5_cert.crossing_patterns())
    require(len(pairs) == 448 and len(patterns) == 985, "key factor counts")
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    pattern_index = {pattern: index for index, pattern in enumerate(patterns)}
    require(len(pair_index) == 448 and len(pattern_index) == 985,
            "key factor uniqueness")
    digest = hashlib.sha256()
    count = 0
    for chart, target in pairs:
        for crossings in patterns:
            row = gate5_cert.registry_key_row(chart, target, crossings)
            digest.update(canonical_json(row).encode("utf-8"))
            digest.update(b"\n")
            count += 1
    require(count == 441280, "key replay count")
    require(
        digest.hexdigest()
        == "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9",
        "key replay digest",
    )
    return pair_index, pattern_index, digest.hexdigest()


def word_key(
    chart: str,
    target: str,
    crossings: tuple[str, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    require((chart, target) in pair_index, "unregistered chart-target pair")
    require(crossings in pattern_index, "unregistered crossing pattern")
    ordinal = pair_index[(chart, target)] * 985 + pattern_index[crossings]
    require(0 <= ordinal < 441280, "key ordinal")
    row = [chart, target, list(crossings), len(crossings) + 1]
    return {
        "ordinal_zero_based": ordinal,
        "word_key_id": f"gate5-word:{ordinal:06d}:" + canonical_digest(row),
        "row": row,
        "row_sha256": canonical_digest(row),
    }


def box_payload(atom: Any) -> dict[str, list[str]]:
    return {
        "t": [qstr(atom.t0), qstr(atom.t1)],
        "p": [qstr(atom.p0), qstr(atom.p1)],
        "s": [qstr(atom.s0), qstr(atom.s1)],
    }


def exact_mass_payload(atom: Any) -> dict[str, str]:
    require(atom.t0 < atom.t1 and atom.p0 < atom.p1 and atom.s0 < atom.s1,
            "positive adaptive cell")
    radius = time2_cert.first_hit.RADIUS[atom.source_core.source]
    base = time2_cert.step1.base_mass(atom)
    coefficient = (
        radius * (atom.p1 - atom.p0) * (atom.s1 - atom.s0) / PARAMETER_WIDTH
    )
    require(
        base
        == radius * (atom.t1 - atom.t0) * (atom.p1 - atom.p0)
        * (atom.s1 - atom.s0) / PARAMETER_WIDTH,
        "base mass formula",
    )
    return {
        "parameter_averaged_coordinate_base_mass_exact_rational": qstr(base),
        "parameter_averaged_coordinate_base_measure_type": (
            "R_source*dt*dp times normalized ds/parameter_window_width"
        ),
        "parameter_averaged_coordinate_base_mass_formula": (
            "R_source*(t1-t0)*(p1-p0)*(s1-s0)/(1/200)"
        ),
        "parameter_averaged_unnormalized_collision_area_mass_exact": (
            f"{qstr(coefficient)}*(asin({qstr(atom.t1)})-asin({qstr(atom.t0)}))"
        ),
    }


def parse_target(identifier: str) -> tuple[str, int, int]:
    match = TARGET_PATTERN.fullmatch(identifier)
    require(match is not None, f"bad target: {identifier}")
    assert match is not None
    return match.group(1), int(match.group(2)), int(match.group(3))


def relative_target(current: str, selected: str) -> str:
    _source, ix, iy = parse_target(current)
    obstacle, jx, jy = parse_target(selected)
    return f"{obstacle}[{jx - ix},{jy - iy}]"


def ordered_axis_events(
    q: arb, h: arb, axis: str
) -> tuple[list[tuple[arb, str, int]] | None, str | None]:
    # All retained flights have length <3; [-7,7] safely contains endpoints
    # even after translating a second retained lift from a physical core.
    if not (bool(q > -7) and bool(q < 7) and bool(h > -7) and bool(h < 7)):
        return None, f"{axis}_endpoint_outside_audit_range"
    events: list[tuple[arb, str, int]] = []
    for wall in range(-6, 7):
        wall_arb = arb(wall)
        plus = bool(q < wall_arb) and bool(h > wall_arb)
        minus = bool(q > wall_arb) and bool(h < wall_arb)
        same_lower = bool(q < wall_arb) and bool(h < wall_arb)
        same_upper = bool(q > wall_arb) and bool(h > wall_arb)
        if plus or minus:
            alpha = (wall_arb - q) / (h - q)
            if not (bool(alpha > 0) and bool(alpha < 1)):
                return None, f"{axis}_crossing_time_not_strict"
            events.append((alpha, axis + ("+" if plus else "-"), wall))
        elif not (same_lower or same_upper):
            return None, f"{axis}_endpoint_on_integer_wall_outer"
    if len(events) > 4:
        return None, f"{axis}_more_than_four_crossings"
    return events, None


def strict_event_order(
    events: list[tuple[arb, str, int]],
) -> tuple[tuple[str, ...] | None, str | None]:
    remaining = list(events)
    ordered: list[str] = []
    while remaining:
        minima = [
            index
            for index, (alpha, _token, _wall) in enumerate(remaining)
            if all(
                index == other_index or bool(alpha < other_alpha)
                for other_index, (other_alpha, _other_token, _other_wall)
                in enumerate(remaining)
            )
        ]
        if len(minima) != 1:
            return None, "vertical_horizontal_corner_time_tie_outer"
        index = minima[0]
        _alpha, token, _wall = remaining.pop(index)
        ordered.append(token)
    return tuple(ordered), None


def second_word_for_atom(
    atom: Any,
    expected_selected_target: str,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any] | None, str | None]:
    state = time2_cert.first_collision_outgoing(atom)
    if state is None:
        return None, "time1_outgoing_geometry_outer"
    owner, status = time2_cert.strict_second_owner(atom)
    if owner is None or status != "strict_unique_second_collision_owner":
        return None, status
    if owner["selected_target_id"] != expected_selected_target:
        return None, "selected_second_target_not_inherited"
    qx, qy = state["contact_x"], state["contact_y"]
    ux, uy = state["outgoing_x"], state["outgoing_y"]
    root = owner["selected_root"]
    assert all(isinstance(value, arb) for value in (qx, qy, ux, uy, root))
    hx, hy = qx + root * ux, qy + root * uy
    x_events, reason = ordered_axis_events(qx, hx, "X")
    if x_events is None:
        return None, reason
    y_events, reason = ordered_axis_events(qy, hy, "Y")
    if y_events is None:
        return None, reason
    crossings, reason = strict_event_order(x_events + y_events)
    if crossings is None:
        return None, reason
    chart = owner["time1_chart_id"]
    target = relative_target(atom.source_core.target_id, expected_selected_target)
    if target not in time2_cert.first_hit.candidate_ids(chart):
        return None, "relative_target_not_in_frozen_retained_pair"
    key = word_key(chart, target, crossings, pair_index, pattern_index)
    return {
        "key": key,
        "absolute_selected_target_id": expected_selected_target,
        "relative_frozen_target_id": target,
        "ordered_clean_wall_record": list(crossings),
        "no_wall_endpoint_or_corner_tie_on_whole_box": True,
    }, None


def common_component_row(
    *,
    level: str,
    origin_atom_id: str,
    recut_suffix: str,
    atom: Any,
    source_core_id: str,
    keys: list[dict[str, Any]],
    terminal_predicate: str,
    destination_core_id: str | None,
) -> dict[str, Any]:
    box = box_payload(atom)
    key_ids = [key["word_key_id"] for key in keys]
    identity = {
        "schema": "c24-adaptive-connected-component-cell.v1",
        "level": level,
        "origin_atom_id": origin_atom_id,
        "adaptive_recut_suffix": recut_suffix,
        "source_core_id": source_core_id,
        "source_box": box,
        "frozen_path_prefix_word_key_ids": key_ids,
        "terminal_predicate": terminal_predicate,
        "destination_core_id": destination_core_id,
    }
    mass = exact_mass_payload(atom)
    return {
        "adaptive_component_id": "c24-adaptive-component:" + canonical_digest(identity),
        **identity,
        "frozen_path_prefix_key_ordinals_zero_based": [
            key["ordinal_zero_based"] for key in keys
        ],
        "path_prefix_owner_id": "c24-prefix-owner:" + canonical_digest(key_ids),
        **mass,
        "positive_2D_open_rectangle_for_every_s_strictly_inside_open_s_interval": True,
        "connected_component_of_finite_open_adaptive_registry": True,
        "regular_analytic_local_diffeomorphism_for_every_s_strictly_inside_open_s_interval": True,
        "t_and_p_dyadic_faces_collision_area_null_on_every_fixed_s_slice": True,
        "s_endpoint_faces_parameter_averaged_product_null": True,
        "s_endpoint_face_collision_area_null_on_exceptional_slice_s_equals_endpoint_claimed": False,
        "fixed_s_slice_claim_includes_cell_s_endpoints": False,
        "maximal_connected_component_of_full_physical_path_fibre_claimed": False,
    }


def r1_registry(
    step1_manifest: dict[str, Any],
    cores: tuple[Any, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    rows = step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    return_rows = [row for row in rows if row["classification"] == "RETURN_AT_1_INNER"]
    require(len(return_rows) == 4216, "R1 replay count")
    digest = hashlib.sha256()
    ids: set[str] = set()
    key_histogram: Counter[int] = Counter()
    destination_histogram: Counter[str] = Counter()
    representatives: list[dict[str, Any]] = []
    total = Q(0)
    source_paths: dict[int, list[str]] = {}
    for index, row in enumerate(return_rows):
        core = cores[row["source_core_index"]]
        atom = time2_cert.atom_from_step1_row(row, cores)
        key = word_key(
            core.chart_id, core.target_id, tuple(core.crossings),
            pair_index, pattern_index,
        )
        component = common_component_row(
            level="R_1_INNER",
            origin_atom_id=row["atom_id"],
            recut_suffix="",
            atom=atom,
            source_core_id=row["source_core_id"],
            keys=[key],
            terminal_predicate="strict_first_return_to_exactly_one_C24_core_at_time1",
            destination_core_id=row["destination_core_id"],
        )
        require(component["adaptive_component_id"] not in ids, "duplicate R1 ID")
        ids.add(component["adaptive_component_id"])
        stream_update(digest, component)
        mass = Q(component["parameter_averaged_coordinate_base_mass_exact_rational"])
        require(mass == Q(row["parameter_averaged_unnormalized_base_mass"]),
                "R1 row mass")
        total += mass
        key_histogram[key["ordinal_zero_based"]] += 1
        destination_histogram[str(row["destination_core_id"])] += 1
        source_paths.setdefault(row["source_core_index"], []).append(row["dyadic_path"])
        if index in (0, len(return_rows) // 2, len(return_rows) - 1):
            representatives.append(component)
    for source_index, paths in source_paths.items():
        ordered = sorted(paths)
        require(
            not any(right.startswith(left) for left, right in zip(ordered, ordered[1:])),
            f"R1 prefix overlap: {source_index}",
        )
    require(len(ids) == 4216, "R1 unique ID count")
    require(total == Q(6473, 256000000), "R1 mass conservation")
    return {
        "finite_source_registry": "all frozen strict R1-inner atoms",
        "origin_atom_count": 4216,
        "materialized_nonempty_adaptive_component_count": len(ids),
        "component_rows_sha256": digest.hexdigest(),
        "component_ids_sha256": canonical_digest(sorted(ids)),
        "distinct_frozen_word_key_count": len(key_histogram),
        "word_key_ordinal_histogram_sha256": canonical_digest(
            {str(key): value for key, value in sorted(key_histogram.items())}
        ),
        "destination_core_histogram_sha256": canonical_digest(
            dict(sorted(destination_histogram.items()))
        ),
        "parameter_averaged_coordinate_base_mass_exact": qstr(total),
        "parameter_averaged_coordinate_base_mass_sum_equals_frozen_R1_inner_coordinate_base_mass": True,
        "all_origin_dyadic_paths_prefix_free_within_source_core": True,
        "every_registered_cell_has_one_exact_frozen_depth1_word_owner": True,
        "every_registered_cell_is_nonempty_not_merely_a_candidate_word": True,
        "representative_rows": representatives,
    }


def q2_registry(
    q1_rows: list[dict[str, Any]],
    q2_rows: list[dict[str, Any]],
    cores: tuple[Any, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    q1_by_id = {row["atom_id"]: row for row in q1_rows}
    require(len(q1_by_id) == 2868, "Q1 parent ID uniqueness")
    digest = hashlib.sha256()
    unresolved_digest = hashlib.sha256()
    ids: set[str] = set()
    prefix_histogram: Counter[str] = Counter()
    blocker_histogram: Counter[str] = Counter()
    recut_depth_histogram: Counter[int] = Counter()
    representatives: list[dict[str, Any]] = []
    unresolved_representatives: list[dict[str, Any]] = []
    admitted_mass = Q(0)
    unresolved_mass = Q(0)
    terminal_count = 0

    for origin_index, row in enumerate(q2_rows):
        parent = q1_by_id[row["Q1_parent_atom_id"]]
        core = cores[row["source_core_index"]]
        box = row["source_box"]
        root_path = parent["dyadic_path"] + row["refinement_suffix"]
        root = time2_cert.step1.Atom(
            row["source_core_index"], core,
            Q(box["t"][0]), Q(box["t"][1]),
            Q(box["p"][0]), Q(box["p"][1]),
            Q(box["s"][0]), Q(box["s"][1]),
            root_path,
        )
        first_key = word_key(
            core.chart_id, core.target_id, tuple(core.crossings),
            pair_index, pattern_index,
        )
        stack: list[tuple[Any, int]] = [(root, 0)]
        terminal_suffixes: list[str] = []
        origin_mass = Q(0)
        while stack:
            atom, extra_depth = stack.pop()
            second, reason = second_word_for_atom(
                atom, row["selected_second_target_id"], pair_index, pattern_index
            )
            suffix = atom.path[len(root.path):]
            if second is None and extra_depth < MAX_EXTRA_WALL_BINARY_DEPTH:
                left, right = time2_cert.step1.split_atom(atom)
                stack.append((right, extra_depth + 1))
                stack.append((left, extra_depth + 1))
                continue
            mass = time2_cert.step1.base_mass(atom)
            origin_mass += mass
            terminal_count += 1
            terminal_suffixes.append(suffix)
            recut_depth_histogram[extra_depth] += 1
            if second is None:
                blocker = str(reason)
                blocker_histogram[blocker] += 1
                unresolved_mass += mass
                unresolved = {
                    "origin_time2_atom_id": row["time2_atom_id"],
                    "adaptive_recut_suffix": suffix,
                    "source_box": box_payload(atom),
                    "parameter_averaged_coordinate_base_mass_exact_rational": qstr(mass),
                    "parameter_averaged_coordinate_base_measure_type": (
                        "R_source*dt*dp times normalized ds/parameter_window_width"
                    ),
                    "parameter_averaged_coordinate_base_mass_formula": (
                        "R_source*(t1-t0)*(p1-p0)*(s1-s0)/(1/200)"
                    ),
                    "first_frozen_word_key_id": first_key["word_key_id"],
                    "first_blocker": blocker,
                    "finite_outer_box_is_declared_collision_null": False,
                }
                stream_update(unresolved_digest, unresolved)
                if len(unresolved_representatives) < 3:
                    unresolved_representatives.append(unresolved)
                continue

            second_key = second["key"]
            component = common_component_row(
                level="Q_2_INNER",
                origin_atom_id=row["time2_atom_id"],
                recut_suffix=suffix,
                atom=atom,
                source_core_id=time2_cert.step1.core_id(core),
                keys=[first_key, second_key],
                terminal_predicate="strict_C24_avoidance_at_collision_times1_and2",
                destination_core_id=None,
            )
            component["second_word_absolute_selected_target_id"] = second[
                "absolute_selected_target_id"
            ]
            component["second_word_relative_frozen_target_id"] = second[
                "relative_frozen_target_id"
            ]
            component["second_word_ordered_clean_wall_record"] = second[
                "ordered_clean_wall_record"
            ]
            require(component["adaptive_component_id"] not in ids,
                    "duplicate Q2 component ID")
            ids.add(component["adaptive_component_id"])
            stream_update(digest, component)
            admitted_mass += mass
            prefix_histogram[
                f"{first_key['ordinal_zero_based']},{second_key['ordinal_zero_based']}"
            ] += 1
            if origin_index in (0, len(q2_rows) // 2, len(q2_rows) - 1) and suffix == "":
                representatives.append(component)

        ordered = sorted(terminal_suffixes)
        require(
            not any(right.startswith(left) for left, right in zip(ordered, ordered[1:])),
            f"Q2 recut prefix overlap: {row['time2_atom_id']}",
        )
        require(
            origin_mass == Q(row["parameter_averaged_unnormalized_base_mass"]),
            f"Q2 origin mass conservation: {row['time2_atom_id']}",
        )

    total = admitted_mass + unresolved_mass
    require(total == Q(5257799, 5120000000), "Q2 anchor mass conservation")
    require(len(ids) > 0, "no Q2 nonempty component")
    return {
        "finite_source_registry": "all frozen strict Q2-inner depth<=16 atoms",
        "origin_atom_count": len(q2_rows),
        "maximum_additional_wall_recut_binary_depth": MAX_EXTRA_WALL_BINARY_DEPTH,
        "terminal_adaptive_cell_count": terminal_count,
        "materialized_nonempty_depth2_adaptive_component_count": len(ids),
        "component_rows_sha256": digest.hexdigest(),
        "component_ids_sha256": canonical_digest(sorted(ids)),
        "distinct_depth2_frozen_word_prefix_count": len(prefix_histogram),
        "depth2_word_prefix_histogram_sha256": canonical_digest(
            dict(sorted(prefix_histogram.items()))
        ),
        "recut_depth_histogram": {
            str(key): value for key, value in sorted(recut_depth_histogram.items())
        },
        "parameter_averaged_admitted_coordinate_base_mass_exact": qstr(admitted_mass),
        "finite_wall_unresolved_outer_cell_count": sum(blocker_histogram.values()),
        "parameter_averaged_finite_wall_unresolved_outer_coordinate_base_mass_exact": qstr(unresolved_mass),
        "finite_wall_unresolved_rows_sha256": unresolved_digest.hexdigest(),
        "finite_wall_first_blocker_histogram": dict(sorted(blocker_histogram.items())),
        "parameter_averaged_admitted_plus_unresolved_equals_frozen_Q2_inner_coordinate_base_mass": True,
        "every_registered_cell_has_one_exact_frozen_depth2_word_prefix_owner": True,
        "every_registered_cell_is_nonempty_not_merely_a_candidate_word": True,
        "complete_frozen_Q2_inner_anchor_depth2_key_ownership": unresolved_mass == 0,
        "finite_unresolved_outer_boxes_promoted_to_collision_null": False,
        "representative_rows": representatives[:3],
        "unresolved_representative_rows": unresolved_representatives,
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    pair_index, pattern_index, alphabet_digest = key_index_tables()
    step1_manifest = time2_cert.load_step1_manifest()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "core replay count")
    r1 = r1_registry(step1_manifest, cores, pair_index, pattern_index)

    q1_rows = [
        row
        for row in step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    require(len(q1_rows) == 2868, "Q1 replay count")
    all_time2_rows = time2_cert.adaptive_time2_rows(q1_rows, cores)
    time2_cert.verify_prefix_and_mass(q1_rows, all_time2_rows)
    require(len(all_time2_rows) == 416994, "time2 replay leaf count")
    q2_rows = [
        row
        for row in all_time2_rows
        if row["classification"] == "SURVIVE_THROUGH_2_INNER"
    ]
    require(len(q2_rows) == 114006, "Q2 replay count")
    q2 = q2_registry(q1_rows, q2_rows, cores, pair_index, pattern_index)

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "precision_bits": 384,
            "full_441280_word_alphabet_replayed": True,
            "frozen_word_alphabet_rows_sha256": alphabet_digest,
            "limiting_physical_R2_Q2_partition_dependency": (
                "CERTIFIED_MOD_COLLISION_NULL"
            ),
        },
        "adaptive_component_contract": {
            "registered_object": (
                "open interior of a positive dyadic source box with one strict "
                "finite collision-word prefix"
            ),
            "fixed_parameter_slice_dimension": 2,
            "fixed_parameter_slice_scope": (
                "every s strictly inside each cell open s-interval; global "
                "parameterwise statements are only outside the finite/countable "
                "set of adaptive s endpoints, hence for a.e. s"
            ),
            "nonempty_witness": "strict positive rational t-width and p-width",
            "connectedness_witness": "open rectangle in the source collision chart",
            "component_scope": (
                "connected component of the finite open adaptive registry after "
                "removing all dyadic faces"
            ),
            "maximal_component_of_entire_path_fibre": False,
            "candidate_word_alone_is_a_nonempty_component": False,
            "immutable_id_payload": (
                "schema, level, origin atom, recut suffix, source core, exact box, "
                "frozen key prefix, terminal predicate and destination"
            ),
            "artificial_t_and_p_dyadic_faces": (
                "collision-area null on every fixed-s two-dimensional slice"
            ),
            "artificial_s_endpoint_faces": (
                "null only for parameter-averaged three-dimensional product measure; "
                "at the exceptional slice s=c the section can be a positive-area rectangle"
            ),
            "physical_owner_wall_core_boundaries": (
                "limiting grazing/corner/owner/core-face carrier is collision-null"
            ),
            "finite_unresolved_outer_boxes_are_null": False,
        },
        "R1_nonempty_adaptive_component_registry": r1,
        "Q2_nonempty_adaptive_component_registry": q2,
        "first_remaining_arbitrary_n_blocker": {
            "first_unmaterialized_extension_depth_from_certified_Q2_inner_anchors": 3,
            "object": (
                "complete physical nonempty Q3/R3 adaptive registry with inherited "
                "strict word prefixes"
            ),
            "reason": (
                "no finite Q2-to-time3 whole-box collision-owner/core classifier and "
                "no arbitrary-n uniform adaptive termination certificate"
            ),
            "Q1_nonempty_component_registry_materialized_by_this_leaf": False,
            "limiting_physical_R2_component_enumeration_materialized": False,
            "depth16_R2_admitted_zero_implies_physical_R2_empty": False,
            "maximal_path_fibre_component_merging_also_open": True,
            "numeric_unstable_Jacobian_distortion_and_strong_q_also_open": True,
        },
        "strict_nonpromotion": {
            "complete_limiting_R1_component_enumeration": "NOT_CERTIFIED",
            "Q1_nonempty_component_registry": "NOT_CERTIFIED",
            "limiting_physical_R2_component_enumeration": "NOT_CERTIFIED",
            "complete_limiting_R2_Q2_component_enumeration": "NOT_CERTIFIED",
            "arbitrary_n_nonempty_component_registry": "NOT_CERTIFIED",
            "maximal_connected_path_fibre_components": "NOT_CERTIFIED",
            "homogeneity_child_and_canonical_recut_registry": "NOT_CERTIFIED",
            "numeric_unstable_Jacobian_and_distortion": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    q2 = result["Q2_nonempty_adaptive_component_registry"]
    return {
        "R1_inner_nonempty_adaptive_components": "CERTIFIED_4216",
        "Q2_inner_nonempty_depth2_adaptive_components": (
            f"CERTIFIED_{q2['materialized_nonempty_depth2_adaptive_component_count']}"
        ),
        "Q2_inner_anchor_depth2_key_ownership": (
            "CERTIFIED_COMPLETE"
            if q2["complete_frozen_Q2_inner_anchor_depth2_key_ownership"]
            else "FINITE_OUTER_REMAINS"
        ),
        "finite_anchor_parameter_averaged_coordinate_base_mass_conservation": "CERTIFIED",
        "maximal_path_fibre_component_enumeration": "NOT_CERTIFIED",
        "arbitrary_n_nonempty_component_registry": "NOT_CERTIFIED",
        "strong_q_weighted_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round28_nonempty_adaptive_component_registry_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    r1 = result["R1_nonempty_adaptive_component_registry"]
    q2 = result["Q2_nonempty_adaptive_component_registry"]
    print("NONEMPTY_ADAPTIVE_COMPONENT_REGISTRY: CERTIFIED_FINITE_ANCHORS")
    print(f"R1_COMPONENTS: {r1['materialized_nonempty_adaptive_component_count']}")
    print(
        "Q2_COMPONENTS: "
        f"{q2['materialized_nonempty_depth2_adaptive_component_count']}"
    )
    print(
        "Q2_PARAMETER_AVERAGED_WALL_OUTER_COORDINATE_BASE_MASS: "
        f"{q2['parameter_averaged_finite_wall_unresolved_outer_coordinate_base_mass_exact']}"
    )
    print("ARBITRARY_N_NONEMPTY_COMPONENT_REGISTRY: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
