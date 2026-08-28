#!/usr/bin/env python3
"""Round178 bounded later-return bridge on the sixteen Round177 live strata.

The exact collision-1 recentering is global on every strict live stratum.
Collision-2 dynamics are materialized only on strict three-dimensional
dyadic inner boxes.  A finite adaptive outer retains every Delta/H/source
seam/root/wall/chart collar.  Observed point keys are explicitly local and
never become global Gate5 dispositions or whole-parent credit.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

import flint
from flint import arb

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round177_tangency_boundary_and_source_seam_ledger as r177


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round178_later_return_exact_key_bridge_certificate.json"
SCHEMA = "cm2.round178.later-return-exact-key-bridge.v1"
MAX_INPUT_BYTES = 32 * 1024 * 1024
PHASE_A_DEPTH = 6
PHASE_B_EXTRA_DEPTH = 10
CURRENT_OWNER = "W[0,0]"
COLLISION1_OWNER = "W[1,0]"
COLLISION1_OUTGOING = "W"
RADIUS = {key: base.arbq(value) for key, value in base.RADIUS.items()}
GATE5_REGISTRY_DIGEST = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)

BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
OWNERSHIP = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
GATE5_SOURCE = "cm2_gate5_actual_phase_graph_cert.py"
GATE5_MANIFEST = "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"
REGISTRY_SOURCE = "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py"
REGISTRY_MANIFEST = (
    "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
)
R162_PRODUCER = "cm2_round162_compact_gate3_coordinate_bridge.py"
R162_CERT = "cm2_round162_compact_gate3_coordinate_bridge_certificate.json"
R162_VERIFIER = "cm2_round162_compact_gate3_coordinate_bridge_verifier.py"
R162_VER = "cm2_round162_compact_gate3_coordinate_bridge_verification.json"
R177_PRODUCER = "cm2_round177_tangency_boundary_and_source_seam_ledger.py"
R177_CERT = "cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json"
R177_VERIFIER = "cm2_round177_tangency_boundary_and_source_seam_ledger_verifier.py"
R177_VER = "cm2_round177_tangency_boundary_and_source_seam_ledger_verification.json"

PINS: dict[str, str] = {
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GE_SOURCE:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    OWNERSHIP:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    GATE5_SOURCE:
        "7ec30f8a51abdb651cf1fdba0dfba755c356272f9058149b974a3149fe2f1a0c",
    GATE5_MANIFEST:
        "ab914a9274b9365defaed5d8808b7a33bacefcce2fc56342881350665c811642",
    REGISTRY_SOURCE:
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    REGISTRY_MANIFEST:
        "120a3f1cba9f23cc4b2a9753491022f8143175810b19f1a9f9d8ee0214d66b60",
    R162_PRODUCER:
        "52efd57078f7ba2b1f99d7ae9a9d76f1ab2424b597f0cd66cf1c6e5e98cde228",
    R162_CERT:
        "7a9889bd306567d8f68b203cab54e6fd821dd303f801e61bd82d9f32e012e4fe",
    R162_VERIFIER:
        "107041d53c74d274ae26e93d1e827993e03fb390fe8e2950a40e4f3f9a0ff63c",
    R162_VER:
        "99b443650b5f74c508e25d982aa09b06632432bd9dd880f1364c69ff7afa1583",
    R177_PRODUCER:
        "729136747872d2a0f8f4bfc0d1c635ca94b6c61df0da1e0f2340ac243616a2ab",
    R177_CERT:
        "8e0a7d3d093026932d847657d737f7f1dfc5aaea3727ff4d3e202728aa64c7cc",
    R177_VERIFIER:
        "56082c686a5f45ca13fdd644b3f7fdd62310b708337a822cff623ddcd5a278f1",
    R177_VER:
        "2b56c96af9d6d284ee39d71636bf43425431183da8ae19df63eaa6b90a6df4b3",
}
R162_RESULT = "5a327f96ecc8183af76695123dcf6fc4ccbf443e4bd7427cef38090c06bcfe86"
R162_VER_RESULT = "3d74d45804c8cef12782eeda57e7f770e6d8b9f962f97d1f28c54c92b27c6421"
R177_RESULT = "9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f"
R177_VER_RESULT = "6968d5b50037457e546c06fbe2f7f620fbbfbb73f354f78b7035afb23426934e"
CROSS_KEYS = (
    "W:E:00.15.0000000",
    "W:E:07.00.1111111",
)


class Round178Error(RuntimeError):
    """Fail-closed Round178 error."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round178Error(label)


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(value)
    row["row_sha256"] = digest(row)
    return row


def read_regular(path: Path, expected: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"hardlink:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise Round178Error(f"noninteger number:{value}")


def strict_json(data: bytes, label: str) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"NUL:{label}")
    value = json.loads(
        data.decode("utf-8", "strict"),
        object_pairs_hook=unique_pairs,
        parse_float=reject_number,
        parse_constant=reject_number,
    )
    require(type(value) is dict, f"top:{label}")
    return value


def load_envelope(name: str) -> dict[str, Any]:
    value = strict_json(read_regular(HERE / name, PINS[name]), name)
    require(
        set(value) == {"schema", "result", "result_sha256"}
        and value["result_sha256"] == digest(value["result"]),
        f"envelope:{name}",
    )
    return value


def validate_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        flint.__version__ == "0.9.0"
        and Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve()
        and Path(ge.__file__).resolve() == (HERE / GE_SOURCE).resolve()
        and Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve()
        and Path(registry.__file__).resolve() == (HERE / REGISTRY_SOURCE).resolve()
        and Path(r177.__file__).resolve() == (HERE / R177_PRODUCER).resolve(),
        "module identity",
    )
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    ownership = strict_json(
        read_regular(HERE / OWNERSHIP, PINS[OWNERSHIP]), OWNERSHIP
    )
    require(
        ownership["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes",
        "ownership",
    )
    r162 = load_envelope(R162_CERT)
    v162 = load_envelope(R162_VER)
    r177_certificate = load_envelope(R177_CERT)
    v177 = load_envelope(R177_VER)
    require(
        r162["result_sha256"] == R162_RESULT
        and v162["result_sha256"] == R162_VER_RESULT
        and v162["result"]["status"] == "PASS"
        and r177_certificate["result_sha256"] == R177_RESULT
        and v177["result_sha256"] == R177_VER_RESULT
        and v177["result"]["status"] == "PASS",
        "verified chain",
    )
    return r162, r177_certificate


def parse_target(identifier: str) -> tuple[str, int, int]:
    obstacle = identifier[0]
    require(
        obstacle in {"G", "W"}
        and identifier[1] == "["
        and identifier[-1] == "]",
        f"target:{identifier}",
    )
    x, y = identifier[2:-1].split(",")
    return obstacle, int(x), int(y)


def target_id(obstacle: str, x: int, y: int) -> str:
    return f"{obstacle}[{x},{y}]"


def translated_candidates(chart_id: str, shift: tuple[int, int]) -> tuple[str, ...]:
    result = []
    for relative in base.candidate_ids(chart_id):
        obstacle, x, y = parse_target(relative)
        result.append(target_id(obstacle, x + shift[0], y + shift[1]))
    return tuple(result)


def target_center(identifier: str, s: Any) -> tuple[Any, Any]:
    obstacle, x, y = parse_target(identifier)
    if obstacle == "G":
        return arb(x), arb(y)
    return (
        arb(x) + base.arbq(Q(1, 2)) + s,
        arb(y) + base.arbq(Q(1, 2)),
    )


def root_record(
    qx: Any,
    qy: Any,
    ux: Any,
    uy: Any,
    s: Any,
    identifier: str,
) -> tuple[str, dict[str, Any] | None]:
    ax, ay = target_center(identifier, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = RADIUS[identifier[0]]
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return "NO_REAL_INTERSECTION", None
    if not bool(discriminant > 0):
        return "UNRESOLVED_DELTA", None
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far < 0):
        return "INTERSECTION_BEHIND", None
    if not bool(near > 0):
        return "UNRESOLVED_ROOT_SIGN", None
    return "STRICT_FUTURE", {
        "near": near,
        "radical": radical,
        "transverse": transverse,
        "radius": radius,
    }


def select_owner(
    geometry: tuple[Any, Any, Any, Any, Any],
    candidates: tuple[str, ...],
    required: str | None = None,
) -> tuple[str, tuple[str, dict[str, Any]] | str | None]:
    qx, qy, ux, uy, s = geometry
    rows = {
        identifier: root_record(qx, qy, ux, uy, s, identifier)
        for identifier in candidates
    }
    if required is not None:
        kind, data = rows[required]
        if kind in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND"}:
            return "STRICT_NOT_LIVE_OWNER_ABSENT", None
        if kind != "STRICT_FUTURE":
            return "COLLISION1_DELTA_ROOT_COLLAR", kind
        assert data is not None
        for identifier, (other_kind, other) in rows.items():
            if (
                identifier != required
                and other_kind == "STRICT_FUTURE"
                and other is not None
                and bool(other["near"] < data["near"])
            ):
                return "STRICT_NOT_LIVE_EARLIER_COMPETITOR", identifier
        if all(
            identifier == required
            or other_kind in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND"}
            or (
                other_kind == "STRICT_FUTURE"
                and other is not None
                and bool(data["near"] < other["near"])
            )
            for identifier, (other_kind, other) in rows.items()
        ):
            return "STRICT_REQUIRED_OWNER", (required, data)
        return "COLLISION1_ROOT_ORDER_COLLAR", None
    future = [
        (identifier, data)
        for identifier, (kind, data) in rows.items()
        if kind == "STRICT_FUTURE" and data is not None
    ]
    winners = [
        (identifier, data)
        for identifier, data in future
        if all(
            identifier == other_identifier
            or bool(data["near"] < other["near"])
            for other_identifier, other in future
        )
    ]
    if (
        len(winners) == 1
        and all(
            kind not in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}
            for kind, _data in rows.values()
        )
    ):
        return "STRICT_UNIQUE_OWNER", winners[0]
    return "COLLISION2_CANDIDATE_ROOT_ORDER_COLLAR", None


def collision_state(
    geometry: tuple[Any, Any, Any, Any, Any],
    owner: tuple[str, dict[str, Any]],
) -> dict[str, Any]:
    qx, qy, ux, uy, s = geometry
    identifier, data = owner
    ax, ay = target_center(identifier, s)
    radical = data["radical"]
    transverse = data["transverse"]
    radius = data["radius"]
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    p = transverse / radius
    cosine = radical / radius
    return {
        "contact_x": ax + radius * nx,
        "contact_y": ay + radius * ny,
        "outgoing_x": cosine * nx - p * ny,
        "outgoing_y": cosine * ny + p * nx,
        "normal_x": nx,
        "normal_y": ny,
        "p": p,
        "cosine": cosine,
        "s": s,
        "root": data["near"],
    }


def strict_chart(nx: Any, ny: Any) -> str | None:
    abs_x, abs_y = abs(nx), abs(ny)
    if bool(abs_x > abs_y):
        if bool(nx > 0):
            return "E"
        if bool(nx < 0):
            return "W"
    if bool(abs_y > abs_x):
        if bool(ny > 0):
            return "N"
        if bool(ny < 0):
            return "S"
    return None


def box_volume(box: Any) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "volume": str(box_volume(box)),
    }


def source_chart_for_box(key: str, box: Any) -> str | None:
    if key not in CROSS_KEYS:
        return key.split(":")[1]
    maximum = max(abs(box.t0), abs(box.t1))
    minimum = min(abs(box.t0), abs(box.t1))
    if 2 * maximum * maximum < 1:
        return "E"
    if 2 * minimum * minimum > 1:
        return "S" if box.t1 < 0 else "N"
    return None


def initial_geometry(chart_id: str, box: Any) -> tuple[Any, Any, Any, Any, Any]:
    qx, qy, ux, uy, s, _cp = atlas.geometry(chart_id, box)
    return qx, qy, ux, uy, s


def collision1_classification(
    key: str,
    chart_id: str,
    box: Any,
) -> tuple[str, dict[str, Any] | None]:
    source_cell = source_chart_for_box(key, box)
    if source_cell is None:
        return "SOURCE_CHART_SEAM_COLLAR", None
    geometry = initial_geometry(chart_id, box)
    status, selected = select_owner(
        geometry,
        translated_candidates(f"W:{source_cell}", (0, 0)),
        COLLISION1_OWNER,
    )
    if status != "STRICT_REQUIRED_OWNER":
        return status, None
    assert isinstance(selected, tuple)
    state = collision_state(geometry, selected)
    outgoing = strict_chart(state["normal_x"], state["normal_y"])
    if outgoing is None:
        return "COLLISION1_OUTGOING_CHART_COLLAR", None
    if outgoing != COLLISION1_OUTGOING:
        return "STRICT_NOT_LIVE_OUTGOING_MISMATCH", None
    state["source_chart_used"] = source_cell
    return "STRICT_COLLISION1_LIVE", state


def gate5_key(
    state: dict[str, Any],
    collision2_owner: tuple[str, dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any] | None, str | None]:
    identifier, data = collision2_owner
    hit_x = state["contact_x"] + data["near"] * state["outgoing_x"]
    hit_y = state["contact_y"] + data["near"] * state["outgoing_y"]
    x_events, reason = registry.ordered_axis_events(
        state["contact_x"] - 1, hit_x - 1, "X"
    )
    if x_events is None:
        return None, f"WALL_X:{reason}"
    y_events, reason = registry.ordered_axis_events(
        state["contact_y"], hit_y, "Y"
    )
    if y_events is None:
        return None, f"WALL_Y:{reason}"
    crossings, reason = registry.strict_event_order(x_events + y_events)
    if crossings is None:
        return None, f"WALL_ORDER:{reason}"
    relative = registry.relative_target(COLLISION1_OWNER, identifier)
    try:
        key = registry.word_key(
            "W:W", relative, crossings, pair_index, pattern_index
        )
    except RuntimeError as exc:
        return None, f"GATE5_REGISTRY:{exc}"
    return {
        "absolute_collision2_owner": identifier,
        "relative_target": relative,
        "ordered_clean_wall_record": list(crossings),
        "official_gate5_key": key,
    }, None


def collision2_classification(
    state: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[str, dict[str, Any] | None]:
    geometry = (
        state["contact_x"], state["contact_y"],
        state["outgoing_x"], state["outgoing_y"], state["s"],
    )
    status, selected = select_owner(
        geometry,
        translated_candidates("W:W", (1, 0)),
    )
    if status != "STRICT_UNIQUE_OWNER":
        return status, None
    assert isinstance(selected, tuple)
    official, reason = gate5_key(state, selected, pair_index, pattern_index)
    if official is None:
        return "COLLISION2_WALL_OR_CORNER_COLLAR", {"reason": reason}
    next_state = collision_state(geometry, selected)
    outgoing = strict_chart(next_state["normal_x"], next_state["normal_y"])
    if outgoing is None:
        return "COLLISION2_OUTGOING_CHART_COLLAR", None
    official["collision2_outgoing_chart"] = outgoing
    return "COLLISION2_EXACT_KEY_RESOLVED", official


def terminal_row(
    parent_key: str,
    box: Any,
    phase: str,
    status: str,
    relative_depth: int,
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return closed_row({
        "parent_key": parent_key,
        "terminal_path": box.path,
        "phase": phase,
        "relative_depth": relative_depth,
        "box": box_payload(box),
        "status": status,
        "detail": detail,
        "integer_whole_parent_credit": 0,
    })


def phase_a_partition(
    parent_key: str,
    chart_id: str,
    parent: Any,
) -> tuple[list[dict[str, Any]], list[tuple[Any, dict[str, Any]]]]:
    pending = [(parent, 0)]
    terminal: list[dict[str, Any]] = []
    live: list[tuple[Any, dict[str, Any]]] = []
    while pending:
        box, depth = pending.pop()
        status, state = collision1_classification(parent_key, chart_id, box)
        if status == "STRICT_COLLISION1_LIVE":
            assert state is not None
            live.append((box, state))
            continue
        if (
            status.endswith("COLLAR")
            and depth < PHASE_A_DEPTH
        ):
            left, right = ge.split(box)
            pending.extend(((right, depth + 1), (left, depth + 1)))
            continue
        terminal.append(terminal_row(
            parent_key, box, "A_COLLISION1_DOMAIN", status, depth
        ))
    return terminal, live


def phase_b_partition(
    parent_key: str,
    chart_id: str,
    initial_live: list[tuple[Any, dict[str, Any]]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> list[dict[str, Any]]:
    pending = [
        (box, PHASE_A_DEPTH, 0) for box, _state in initial_live
    ]
    terminal: list[dict[str, Any]] = []
    while pending:
        box, inherited_depth, extra_depth = pending.pop()
        status1, state = collision1_classification(parent_key, chart_id, box)
        require(
            status1 == "STRICT_COLLISION1_LIVE" and state is not None,
            f"live inheritance:{parent_key}:{box.path}",
        )
        status, detail = collision2_classification(
            state, pair_index, pattern_index
        )
        if (
            status != "COLLISION2_EXACT_KEY_RESOLVED"
            and extra_depth < PHASE_B_EXTRA_DEPTH
        ):
            left, right = ge.split(box)
            pending.extend((
                (right, inherited_depth + 1, extra_depth + 1),
                (left, inherited_depth + 1, extra_depth + 1),
            ))
            continue
        terminal.append(terminal_row(
            parent_key,
            box,
            "B_COLLISION2",
            status,
            inherited_depth,
            detail,
        ))
    return terminal


def point_box(parent: Any, point: dict[str, str]) -> Any:
    return atlas.AtlasBox(
        Q(point["t"]), Q(point["t"]),
        Q(point["p"]), Q(point["p"]),
        Q(point["s"]), Q(point["s"]),
        parent.depth, parent.path + ".observed-point",
    )


def observed_point_row(
    parent_row: dict[str, Any],
    chart_id: str,
    parent: Any,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    point = parent_row["strict_live_open_witness"]["point"]
    box = point_box(parent, point)
    status1, state = collision1_classification(
        parent_row["ambient_leaf_key"], chart_id, box
    )
    require(
        status1 == "STRICT_COLLISION1_LIVE" and state is not None,
        f"observed collision1:{parent_row['ambient_leaf_key']}",
    )
    status2, detail = collision2_classification(
        state, pair_index, pattern_index
    )
    require(
        status2 == "COLLISION2_EXACT_KEY_RESOLVED" and detail is not None,
        f"observed collision2:{parent_row['ambient_leaf_key']}",
    )
    return closed_row({
        "parent_key": parent_row["ambient_leaf_key"],
        "point": point,
        "collision1_owner": COLLISION1_OWNER,
        "collision1_outgoing_chart": COLLISION1_OUTGOING,
        **detail,
        "scope": "LOCAL_STRICT_POINT_OBSERVATION_ONLY",
        "global_gate5_disposition_credit": 0,
        "whole_stratum_or_parent_credit": 0,
    })


def bridge_contract() -> dict[str, Any]:
    return {
        "collision1_physical_data": {
            "source_owner": CURRENT_OWNER,
            "selected_owner": COLLISION1_OWNER,
            "source_radius": "4/25",
            "eta": "cross(u0,center(W[1,0])-q0)",
            "Delta": "(4/25)^2-eta^2",
            "flight": "ell-sqrt(Delta)",
            "normal_n1": (
                "(-sqrt(Delta)*u0_x+eta*u0_y,"
                "-sqrt(Delta)*u0_y-eta*u0_x)/(4/25)"
            ),
            "phase_p1": "eta/(4/25)",
            "phase_radial1": "sqrt(Delta)/(4/25)",
        },
        "deck_recenter": {
            "absolute_selected_owner": "W[1,0]",
            "integer_deck_shift_removed": [1, 0],
            "contact_after_shift": "center_W(s)+(4/25)*n1",
            "velocity_unchanged_by_deck_translation": True,
            "parameter_s_unchanged": True,
        },
        "next_source_W_gate3_chart": {
            "chart_id": "W:W",
            "strict_chart_condition": "-n1_x>|n1_y|",
            "t1": "n1_y",
            "p1": "eta/(4/25)",
            "s1": "s",
            "half_open_diagonal_seam_owner": "W",
        },
        "next_source_W_compact_chart": {
            "compact_chart": "W",
            "q1": "eta/(4/25+sqrt(Delta))",
            "z1": "-n1_y/(1-n1_x)",
            "inverse_gate3_relations": {
                "p1": "2*q1/(1+q1^2)",
                "t1": "-2*z1/(1+z1^2)",
            },
            "denominators_strictly_positive_on_live_strata": True,
            "pinned_Round162_state_map_used": True,
        },
        "analytic_regular_scope": {
            "Delta_strictly_positive": True,
            "collision1_not_grazing": True,
            "outgoing_W_chart_strict_on_3D_live_interior": True,
            "billiard_map_local_analytic_diffeomorphism": True,
            "collision_area_Jacobian": "1",
            "lower_dimensional_boundaries_retained_separately": True,
        },
    }


def guard_rechart_rows(r177_result: dict[str, Any]) -> list[dict[str, Any]]:
    by_key = {
        row["ambient_leaf_key"]: row
        for row in r177_result["exact_parent_rows"]
    }
    rows = []
    for key in CROSS_KEYS:
        source = by_key[key]
        negative = key == CROSS_KEYS[0]
        adjacent = "W:S" if negative else "W:N"
        intersections = source["distinguished_intersections"][
            "source_seam_intersections"
        ]
        rows.append(closed_row({
            "parent_key": key,
            "source_coordinate_chart": "W:E",
            "adjacent_coordinate_chart": adjacent,
            "guard_side": (
                "t_E<-1/sqrt(2)" if negative else "t_E>1/sqrt(2)"
            ),
            "exact_rechart": {
                "t_adjacent": "sqrt(1-t_E^2)",
                "p_adjacent": "p_E",
                "s_adjacent": "s_E",
                "physical_normal_identity": True,
                "physical_quarter_turn_identity": True,
                "physical_velocity_identity": True,
                "Jacobian_determinant":
                    "-t_E/sqrt(1-t_E^2)",
                "Jacobian_strictly_nonzero_on_open_guard_slice": True,
                "Jacobian_on_selected_seam":
                    "+1" if negative else "-1",
                "open_guard_map_is_bijective": True,
            },
            "half_open_gluing": {
                "two_dimensional_source_seam_owner": "E",
                "adjacent_N_or_S_representation_excluded_on_seam": True,
                "open_3D_guard_slice_counted_once_in_adjacent_chart": True,
                "lost_physical_points": 0,
                "duplicated_physical_points": 0,
            },
            "seam_strata": {
                "source_seam_dimension": 2,
                "source_seam_intersect_Delta":
                    intersections["source_seam_intersect_Delta"],
                "source_seam_intersect_H":
                    intersections["source_seam_intersect_H"],
                "source_seam_Delta_H_triple":
                    intersections[
                        "source_seam_intersect_Delta_intersect_H"
                    ],
                "all_integer_credit": 0,
            },
            "guard_outside_exterior_or_whole_parent_credit": 0,
        }))
    return rows


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {key: str(item) for key, item in sorted(value.items())}


def build_result(producer_sha256: str) -> dict[str, Any]:
    r162, r177_certificate = validate_chain()
    pair_index, pattern_index, registry_digest = registry.key_index_tables()
    require(registry_digest == GATE5_REGISTRY_DIGEST, "Gate5 registry")
    r177_result = r177_certificate["result"]
    parent_rows = r177_result["exact_parent_rows"]
    require(len(parent_rows) == 16, "Round177 parent count")
    all_terminal: list[dict[str, Any]] = []
    observed: list[dict[str, Any]] = []
    per_parent: list[dict[str, Any]] = []
    for parent_row in parent_rows:
        key = parent_row["ambient_leaf_key"]
        chart_id, parent = r177.r175.decode_parent_box(key)
        phase_a, live = phase_a_partition(key, chart_id, parent)
        phase_b = phase_b_partition(
            key, chart_id, live, pair_index, pattern_index
        )
        terminal = sorted(
            phase_a + phase_b,
            key=lambda row: row["terminal_path"],
        )
        expected_volume = box_volume(parent)
        observed_volume = sum(
            Q(row["box"]["volume"]) for row in terminal
        )
        require(observed_volume == expected_volume, f"volume:{key}")
        status_counts = Counter(row["status"] for row in terminal)
        status_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
        for row in terminal:
            status_volumes[row["status"]] += Q(row["box"]["volume"])
        resolved_rows = [
            row for row in terminal
            if row["status"] == "COLLISION2_EXACT_KEY_RESOLVED"
        ]
        exact_keys = sorted({
            row["detail"]["official_gate5_key"]["word_key_id"]
            for row in resolved_rows
        })
        per_parent.append(closed_row({
            "parent_key": key,
            "parent_volume": str(expected_volume),
            "phase_A_depth": PHASE_A_DEPTH,
            "phase_B_extra_depth": PHASE_B_EXTRA_DEPTH,
            "terminal_box_count": len(terminal),
            "status_counts": dict(sorted(status_counts.items())),
            "status_volumes": fraction_map(status_volumes),
            "volume_conservation": (
                "+".join(
                    f"{name}:{status_volumes[name]}"
                    for name in sorted(status_volumes)
                )
                + f"={expected_volume}"
            ),
            "resolved_collision2_3D_box_count": len(resolved_rows),
            "resolved_local_gate5_key_ids": exact_keys,
            "full_live_stratum_collision2_closed": False,
            "bridge_status": "PARTIAL",
            "whole_stratum_or_parent_credit": 0,
            "terminal_rows_sha256": digest(terminal),
        }))
        all_terminal.extend(terminal)
        observed.append(observed_point_row(
            parent_row, chart_id, parent, pair_index, pattern_index
        ))
    all_terminal.sort(key=lambda row: (
        row["parent_key"], row["terminal_path"]
    ))
    observed.sort(key=lambda row: row["parent_key"])
    total_parent_volume = sum(
        Q(row["parent_volume"]) for row in per_parent
    )
    global_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    global_counts: Counter[str] = Counter()
    for row in all_terminal:
        global_counts[row["status"]] += 1
        global_volumes[row["status"]] += Q(row["box"]["volume"])
    require(
        sum(global_volumes.values()) == total_parent_volume,
        "global volume conservation",
    )
    observed_ids = sorted({
        row["official_gate5_key"]["word_key_id"] for row in observed
    })
    observed_ordinals = sorted({
        row["official_gate5_key"]["ordinal_zero_based"] for row in observed
    })
    resolved_ids = sorted({
        row["detail"]["official_gate5_key"]["word_key_id"]
        for row in all_terminal
        if row["status"] == "COLLISION2_EXACT_KEY_RESOLVED"
    })
    require(
        observed_ordinals == [289591, 291560, 321111, 322097],
        "four observed keys",
    )
    guard_rows = guard_rechart_rows(r177_result)
    return {
        "status": (
            "PARTIAL_16_GLOBAL_COLLISION1_RECENTERING_BRIDGES_WITH_BOUNDED_"
            "COLLISION2_EXACT_KEY_INNER_BOXES__NO_GLOBAL_DISPOSITION"
        ),
        "bridge_parent_census": {
            "input_strict_collision1_live_strata": 16,
            "global_collision1_coordinate_bridges_fully_closed": 16,
            "collision2_fully_closed_live_strata": 0,
            "collision2_partial_live_strata": 16,
            "whole_parent_or_whole_stratum_promotions": 0,
        },
        "global_collision1_bridge_contract": bridge_contract(),
        "Round162_binding": {
            "certificate_result_sha256": R162_RESULT,
            "compact_chart": "W",
            "gate3_chart": "W:W",
            "source_W_coordinate_bridge_reused_exactly": True,
            "new_dynamical_disposition_inferred_from_Round162": False,
        },
        "guard_adjacent_chart_recoordinates": {
            "row_count": len(guard_rows),
            "rows_sha256": digest(guard_rows),
            "rows": guard_rows,
            "two_dimensional_seams_counted_once": 2,
            "one_dimensional_Delta_or_H_seam_intersections_counted_once": 4,
            "lost_or_duplicated_physical_points": 0,
        },
        "collision2_observed_local_exact_keys": {
            "point_row_count": len(observed),
            "distinct_key_count": len(observed_ids),
            "distinct_ordinals_zero_based": observed_ordinals,
            "distinct_key_ids": observed_ids,
            "rows_sha256": digest(observed),
            "rows": observed,
            "scope": "LOCAL_POINT_OBSERVATIONS_ONLY",
            "global_Gate5_disposition_count": 0,
            "whole_stratum_or_parent_credit": 0,
        },
        "bounded_full_parent_3D_ledger": {
            "phase_A_max_relative_depth": PHASE_A_DEPTH,
            "phase_B_max_extra_depth": PHASE_B_EXTRA_DEPTH,
            "parent_count": len(per_parent),
            "parent_rows_sha256": digest(per_parent),
            "parent_rows": per_parent,
            "terminal_box_count": len(all_terminal),
            "terminal_status_counts": dict(sorted(global_counts.items())),
            "terminal_status_volumes": fraction_map(global_volumes),
            "total_parent_volume": str(total_parent_volume),
            "exact_volume_conservation": (
                "+".join(
                    f"{name}:{global_volumes[name]}"
                    for name in sorted(global_volumes)
                )
                + f"={total_parent_volume}"
            ),
            "resolved_collision2_3D_box_count": global_counts[
                "COLLISION2_EXACT_KEY_RESOLVED"
            ],
            "resolved_local_gate5_key_ids": resolved_ids,
            "resolved_boxes_are_strict_inner_subsets_only": True,
            "residual_boxes_cover_all_unresolved_Delta_H_source_seam_"
            "root_wall_corner_and_outgoing_chart_collars": True,
            "terminal_rows_sha256": digest(all_terminal),
            "terminal_rows": all_terminal,
        },
        "lower_dimensional_ledger": {
            "Delta_2D_graph_pieces": 18,
            "H_2D_graph_pieces": 18,
            "H_parent_face_clipping_1D_rows": 14,
            "physical_source_seam_2D_rows": 2,
            "source_seam_Delta_1D_rows": 2,
            "source_seam_H_1D_rows": 2,
            "Delta_H_1D_rows": 0,
            "source_seam_Delta_H_0D_rows": 0,
            "all_lower_dimensional_integer_credit": 0,
        },
        "official_Gate5_registry_binding": {
            "chart_target_pair_count": 448,
            "clean_wall_pattern_count": 985,
            "global_key_count": 441280,
            "registry_rows_sha256": registry_digest,
            "official_key_rows_materialized_on_strict_inner_3D_boxes":
                global_counts["COLLISION2_EXACT_KEY_RESOLVED"],
            "global_key_dispositions_materialized": 0,
        },
        "dimension_safe_nonpromotion": {
            "observed_point_to_global_key_credit": 0,
            "resolved_inner_box_to_whole_stratum_credit": 0,
            "resolved_inner_box_to_whole_parent_credit": 0,
            "guard_slice_to_exterior_credit": 0,
            "two_or_one_dimensional_stratum_to_integer_credit": 0,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "replace the finite Delta/H/root/wall/chart collar outer by "
            "parametric interval-Newton graph cells and exact wall-order "
            "arrangements until every one of the sixteen collision2 live "
            "strata is closed"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "arb_precision_bits": atlas.ctx.prec,
            "Round177_files_modified": False,
            "observed_local_rows_promoted_globally": False,
        },
    }


def safe_write(path: Path, data: bytes, protected: set[Path]) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output directory")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(st.st_nlink == 1, "output hardlink")
    require(path.resolve(strict=False) not in protected, "protected alias")
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    source_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    safe_write(
        arguments.output,
        canonical_bytes(envelope) + b"\n",
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
